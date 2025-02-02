# Create a script that will automatically interact with veconlab

steps = """
- https://veconlab.econ.virginia.edu/login1.php
    - Enter: xaty4
    - Click submit
- https://veconlab.econ.virginia.edu/login2.php
    - First Name: [First Name]
    - Last Name: [Last Name]
    - Optional password: [Password]
    - Click continue to proceed
- https://veconlab.econ.virginia.edu/inst_0.php
    - Save the instructions as a variable
    - Click continue with instructions
- https://veconlab.econ.virginia.edu/bg/bg_inst1.php
    - Save the instructions as a variable
    - Click continue with instructions
- https://veconlab.econ.virginia.edu/bg/bg_inst2.php
    - Save the instructions as a variable
    - Click continue
- https://veconlab.econ.virginia.edu/bg/bg_inst6.php
    - Save the instructions as a variable
    - Click Finish with instructions
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from .agent import Agent
import json
import time
import os
import threading

class VeconLabAutomation:
    """
    A class to automate interactions with VeconLab using Selenium.
    """

    def __init__(self, session_id: str, first_name: str, last_name: str, password: str = ""):
        """
        Initialize the Selenium WebDriver and user credentials.

        :param session_id: The session ID for the game.
        :param first_name: User's first name.
        :param last_name: User's last name.
        :param password: Optional password for login.
        """
        self.session_id = session_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.instructions = []

        # Set up the WebDriver
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, timeout = 10 * 60) # wait ten minutes

        # Set up AI Agent
        context_text = """
        You are an undergraduate student at the college of William & Mary participating in an economics experiment for money. 
        Your role is to play an ultimatum game with another participant. You will have to make a series of decisions and your payoff is based on your opponent as well
        If the responder accepts the offer, both players receive the amount proposed by the proposer. If the responder rejects the offer, both players receive nothing.
        For all questions you should provide your answer in the following format: {"choice": "YOUR_CHOICE", "explanation": "YOUR_EXPLANATION"}.
        YOUR_CHOICE should be the minimum information needed to answer the question. For example, if asked for a number only put the number in YOUR_CHOICE. For a decision put either 'a' for accept or 'r' for reject.
        YOUR_EXPLANATION should be a short (1-2 sentence) justification for your choice.
        """
        self.agent = Agent(secrets_file="secrets.txt")
        self.agent.add_context(context_text)

        # Log
        print("VeconLabAutomation initialized.")

    def login_step_1(self):
        """
        Navigate to the first login page and submit the session ID.
        """
        url = "https://veconlab.econ.virginia.edu/login1.php"
        self.driver.get(url)

        input_field = self.driver.find_element(By.NAME, "table_name")
        submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        
        input_field.send_keys(self.session_id)

        # Log
        print("Submitting session ID...")
        submit_button.click()

    def login_step_2(self):
        """
        Navigate to the second login page and enter user details.
        """
        self.wait.until(EC.url_contains("login2.php"))
        
        self.driver.find_element(By.NAME, "first_name").send_keys(self.first_name)
        self.driver.find_element(By.NAME, "last_name").send_keys(self.last_name)
        self.driver.find_element(By.NAME, "password").send_keys(self.password)
        self.driver.find_element(By.NAME, "password_check").send_keys(self.password)
        submit_button = self.driver.find_element(By.XPATH, "//input[@type='submit']")
        # Log
        print("Logging in...")
        submit_button.click()

    def save_instructions(self):
        """
        Save instructions from the current page and proceed.
        """
        font_elements = self.driver.find_elements(By.TAG_NAME, "font")
        for element in font_elements:
            instruction_text = element.text
            self.instructions.append(instruction_text)
        print("Moving past instructions...")
        submit_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='submit']"))
        )
        submit_button.click()

    def play_game(self):
        """
        Play the game and save the results.
        """
        def _play_game(id):
            # Get the prompt
            prompt_element = self.driver.find_element(By.TAG_NAME, "font")
            # Get the decision (select element)
            decision_element = self.driver.find_element(By.TAG_NAME, "select")
            # Print choices
            # options = [option.get_attribute("value") for option in decision_element.find_elements(By.TAG_NAME, "option")]
            # Select a random choice
            if id == 0:
                offer_json = json.loads(self.agent.prompt("You are the proposer. How much money do you keep for youself (between $1-10?). Your opponent will receive the rest."))
                choice = offer_json['choice']
                print(f"Selected: {choice} b/c {offer_json['explanation']}")
            elif id == 1:
                response_json = json.loads(self.agent.prompt(f"Your previous offer was rejected. You can make a new offer. How much money do you keep for youself (between $1-10?). Your opponent will receive the rest."))
                choice = response_json['choice'].strip()
                print(f"Selected: {choice} b/c {response_json['explanation']}")
            # Submit the choice
            select = Select(decision_element)
            select.select_by_value(choice)
            # Click submit
            print("Submitting decision...")
            self.driver.find_element(By.XPATH, "//input[@type='submit']").click()
            
            # Wait until new page loads
            self.wait.until(EC.url_contains("bg_p_confirm.php"))
            # Confirm decision
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@value='Confirm Decision']")))
            print("Confirming decision...")
            self.driver.find_element(By.XPATH, "//input[@value='Confirm Decision']").click()

        _play_game(id=0)

        # Wait until the results page loads
        self.wait.until(EC.url_contains("bg_p_results.php"))
        # Wait until a submit button appears
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@value='Begin Round 2']")))
        # Click submit
        print("Starting round 2...")
        self.driver.find_element(By.XPATH, "//input[@value='Begin Round 2']").click()

        # Clear instructions
        self.instructions = []
        # Go through instruction pages
        self.wait.until(EC.url_contains("bg_inst1.php"))
        self.save_instructions()
        self.wait.until(EC.url_contains("bg_inst2.php"))
        self.save_instructions()
        self.wait.until(EC.url_contains("bg_inst6.php"))
        self.save_instructions()

        # Play the game again
        _play_game(id=1)

        # Wait until the results page loads
        self.wait.until(EC.url_contains("bg_p_results.php"))
        # Wait until a submit button appears
        print("Waiting for counter offer...")
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@value='Respond to Counter-Proposal']")))
        # Click submit
        print("Responding to counter offer...")
        self.driver.find_element(By.XPATH, "//input[@value='Respond to Counter-Proposal']").click()

        # Select accept or reject
        print("Waiting on results...")
        self.wait.until(EC.url_contains("bg_p_submit.php"))
        # get counter offer from page
        counter_offer = 3 - int(self.driver.find_element(By.NAME, "r_counter_proposal").get_attribute("value"))
        print(f"counter offer: {counter_offer}")
        # prompt agent
        offer_json = json.loads(self.agent.prompt(f"Do you accept or reject the counter offer of ${counter_offer} for you?"))
        choice = offer_json['choice']
        print(f"Selected: {choice} b/c {offer_json['explanation']}")
        # Select radio button by value
        self.driver.find_element(By.XPATH, f"//input[@value='{choice}']").click()
        # Click submit
        print("Submitting decision...")
        self.driver.find_element(By.XPATH, "//input[@type='submit']").click()

        # Wait until the confirmation page loads
        self.wait.until(EC.url_contains("bg_p_confirm.php"))
        # Click
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@value='Confirm Decision']")))
        print("Confirming decision...")
        self.driver.find_element(By.XPATH, "//input[@value='Confirm Decision']").click()

    def respond_to_offer(self):
        """
        Automation pipelines for the responder.
        """
        # Wait until submit page
        print("Waiting for offer...")
        # Print HTML
        while "p_decision1" not in self.driver.page_source:
            # sleep 1 second
            time.sleep(1)
            print("Waiting on offer...")
        # self.wait.until(EC.presence_of_element_located((By.NAME, "//input[@value='p_decision1']")))
        # Get the offer
        offer = 10 - int(self.driver.find_element(By.NAME, "p_decision1").get_attribute("value"))
        print(f"Responder got offer of: {offer}")
        # Prompt agent
        offer_json = json.loads(self.agent.prompt(f"Do you accept or reject the offer of ${offer} for you?"))
        choice = offer_json['choice']
        print(f"Selected: {choice} b/c {offer_json['explanation']}")
        # Select radio button by value
        self.driver.find_element(By.XPATH, f"//input[@value='{choice}']").click()
        # Submit decision
        print("Submitting decision...")
        self.driver.find_element(By.XPATH, "//input[@value='Submit']").click()
        
        # Wait until confirmation page
        self.wait.until(EC.url_contains("bg_r_confirm.php"))
        # Confirm decision
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@value='Confirm Decision']")))
        print("Confirming decision...")
        self.driver.find_element(By.XPATH, "//input[@value='Confirm Decision']").click()

        # Load results page
        self.wait.until(EC.url_contains("bg_r_results.php"))
        # Begin round 2
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@value='Begin Round 2']")))
        print("Starting round 2...")
        self.driver.find_element(By.XPATH, "//input[@value='Begin Round 2']").click()

        # Clear instructions
        self.instructions = []
        # Go through instruction pages
        self.wait.until(EC.url_contains("bg_inst1.php"))
        self.save_instructions()
        self.wait.until(EC.url_contains("bg_inst2.php"))
        self.save_instructions()
        self.wait.until(EC.url_contains("bg_inst6.php"))
        self.save_instructions()


        # Wait until decision page
        # self.wait.until(EC.url_contains("bg_r_submit.php"))
        # Get new offer
        self.wait.until(EC.presence_of_element_located((By.NAME, "p_decision1")))
        offer = 10 - int(self.driver.find_element(By.NAME, "p_decision1").get_attribute("value"))
        print(f"New offer for responder is: {offer}")
        # Prompt agent
        offer_json = json.loads(self.agent.prompt(f"Do you accept or reject the offer of ${offer} for you?"))
        choice = offer_json['choice']
        print(f"Selected: {choice} b/c {offer_json['explanation']}")
        # Aceept or reject
        self.driver.find_element(By.XPATH, f"//input[@value='{choice}']").click()
        # If reject create counter offer
        if choice == 'r':
            counter_offer_json = json.loads(self.agent.prompt("What is your counter offer? Decide between $1-3 to keep for yourself"))
            counter_offer = counter_offer_json['choice']
            print(f"Counter offer: {counter_offer} b/c {counter_offer_json['explanation']}")
            # Select counter offer
            select = Select(self.driver.find_element(By.NAME, "r_counter_proposal"))
            select.select_by_value(counter_offer)
        # Submit decision
        print("Submitting decision...")
        self.driver.find_element(By.XPATH, "//input[@value='Submit Response']").click()
    
        # Confirm decision
        self.wait.until(EC.url_contains("bg_r_confirm.php"))
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@value='Confirm Decision']")))
        print("Confirming decision...")
        self.driver.find_element(By.XPATH, "//input[@value='Confirm Decision']").click()
    
    def run(self):
        """
        Execute the full automation sequence.
        """
        try:
            self.login_step_1()
            self.wait.until(EC.url_contains("login2.php"))
            self.login_step_2()
            self.wait.until(EC.url_contains("inst_0.php"))

            self.save_instructions()
            self.wait.until(EC.url_contains("bg_inst1.php"))
            self.save_instructions()
            self.wait.until(EC.url_contains("bg_inst2.php"))
            # Check if first mover or second mover
            bold_elements = self.driver.find_elements(By.TAG_NAME, "b")
            first_mover = "Proposer" in " ".join([element.text for element in bold_elements])
            print(f"Agent is First mover: {first_mover}")
            self.save_instructions()
            self.wait.until(EC.url_contains("bg_inst6.php"))
            self.save_instructions()

            print("Reached decision page")
            # print("\n".join(self.instructions))
            if first_mover:
                self.play_game()
            else: # second mover (responder)
                self.respond_to_offer()

        finally:
            self.driver.quit()

def run_ultimatum_experiment(id: str, agents: int, password="pass"):
    """
    Run the ultimatum experiment.
    """
    # Run the automation
    def run_automation(first_name, last_name):
        automation = VeconLabAutomation(session_id=id, first_name=first_name, last_name=last_name, password=password)
        automation.run()

        # Create a log directory if it doesn't exist
        log_dir = os.path.join("logs", f"ult_log_{time.strftime('%Y-%m-%d-%H-%M')}")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Log the results
        with open(os.path.join(log_dir, f"{first_name}_{last_name}.txt"), "w") as log_file:
            # Write the interactions
            log_file.write("Interactions:\n")
            log_file.write(automation.previous_rounds.to_json(index=False))
            log_file.write("\n\n")

            # Write the agent's messages
            log_file.write("Agent Messages:\n")
            for message in automation.agent.messages:
                log_file.write(f"{message}\n")
            log_file.write("\n")
    
    # Start multiple threads for different players
    for i in range(agents):
        first_name = f"Agent"
        last_name = f"{i + 1}"
        thread = threading.Thread(target=run_automation, args=(first_name, last_name))
        thread.start()

# Example usage:
if __name__ == "__main__":
    automation = VeconLabAutomation(session_id="xaty30", first_name="Agent", last_name="One", password="1234")
    automation.run()
