# Automatically Run the Multi-Stage Ultimatum Game through VeconLab as the Second Player

# Import for Interacting with VeconLab
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# Import for Running the Experiment
from agent import Agent
import json
import time

class VeconLabAutomation:
    """
    A class to automate interactions with VeconLab using Selenium.
    """

    def __init__(self, session_id: str, first_name: str, last_name: str, password: str = ""):
        """
        Initialize the Selenium WebDriver and user credentials.

        Parameters
        ----------
        session_id: str
            The session ID for the game.
        first_name: str
            The user's first name.
        last_name: str
            The user's last name.
        password: str
            The user's password.
        """
        self.session_id = session_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password

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

    def join_session(self):
        """
        Join the VeconLab session.
        """
        # Open the VeconLab login page
        self.driver.get("https://veconlab.econ.virginia.edu/login1.php")

        # Wait until element loaded
        self.wait.until(EC.presence_of_element_located((By.NAME, "table_name")))

        # Fill in the session
        session_input = self.driver.find_element(By.NAME, "table_name")
        session_input.send_keys(self.session_id)

        # Log
        print("Session ID entered.")

        # Continue to the next page
        self.driver.find_element(By.XPATH, "//input[@type='submit']").click()

    def login(self):
        """
        Enter user information (assumes you already joined the session).
        """
        # Make sure we are on the login page
        self.wait.until(EC.url_contains("login2.php"))

        # Fill in the user information
        self.driver.find_element(By.NAME, "first_name").send_keys(self.first_name)
        self.driver.find_element(By.NAME, "last_name").send_keys(self.last_name)
        self.driver.find_element(By.NAME, "password").send_keys(self.password)
        self.driver.find_element(By.NAME, "password_check").send_keys(self.password)
        
        # Log
        print("User information entered.")

        # Continue to the next page
        self.driver.find_element(By.XPATH, "//input[@type='submit']").click()

    def skip_instructions(self):
        """
        Continue past an instructions page.
        """
        # Wait until the instructions are loaded
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='submit']")))
        self.driver.find_element(By.XPATH, "//input[@type='submit']").click()
        print("Instructions skipped.")

    def play_game(self, round_number: int):
        """
        Accepts or rejects an offer.

        Parameters
        ----------
        round_number: int
            The current run number.
        """
        # Log
        print(f"Playing game run {round_number}:")
        # Wait until the an offer is made
        while "p_decision1" not in self.driver.page_source:
            print("Waiting on offer...")
            time.sleep(2)

        # Get the offer
        offer = 10 - int(self.driver.find_element(By.NAME, "p_decision1").get_attribute("value"))
        print(f"Responder got offer of: {offer}")

        # Prompt the agent to make a decision
        offer_json = json.loads(self.agent.prompt(f"Do you accept or reject the offer of ${offer} for you?"))
        choice = offer_json["choice"]
        explanation = offer_json["explanation"]
        print(f"Agent chose: {choice} b/c: {explanation}")

        # Execute the decision
        self.driver.find_element(By.XPATH, f"//input[@value='{choice}']").click()
        self.driver.find_element(By.XPATH, "//input[@value='Submit']").click()
        print("Executed decision.")

        # Confirm the decision
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@value='Confirm Decision']")))
        self.driver.find_element(By.XPATH, "//input[@value='Confirm Decision']").click()
        print("Decision confirmed.")

        # Begin next round
        self.wait.until(EC.presence_of_element_located((By.XPATH, f"//input[@value='Begin Round {round_number + 1}']")))
        self.driver.find_element(By.XPATH, f"//input[@value='Begin Round {round_number + 1}']").click()
        if round_number < 10:
            print(f"\nBeginning round {round_number + 1}.")
        else:
            print("\nFinished all rounds!")

    def run(self):
        """
        Run the experiment using an AI agent as a second player.
        """
        # Join the session
        self.join_session()

        # Login
        self.login()

        # Skip instructions
        for _ in range(4):
            self.skip_instructions()
        print("Finished skipping instructions.")

        # Play the game
        for round_number in range(1, 11):
            self.play_game(round_number)

        # Close the browser
        self.driver.quit()

# Create a function to run the experiment
def run_experiment(session_id, first_name, last_name):
    # Initialize the VeconLabAutomation object
    veconlab = VeconLabAutomation(session_id=session_id, first_name=first_name, last_name=last_name, password="pass")

    # Run the experiment
    veconlab.run()

# Run the experiment
if __name__ == "__main__":
    run_experiment("xaty1", "Agent", "Prime")
