# Automatically Run the Multi-Stage Ultimatum Game through VeconLab as the Second Player

# Import for Interacting with VeconLab
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# Import for Running the Experiment
from pandas import DataFrame
from .agent import Agent
from .prompts import experiment_prompt
import json
import time
import os, sys
import dill as pickle

class VeconLabAutomation:
    """
    A class to automate interactions with VeconLab using Selenium.
    """

    def __init__(self, session_id: str, first_name: str, last_name: str, password: str = "", model: str = "gpt-3.5-turbo"):
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
        # Set up user credentials
        self.session_id = session_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password

        # Set up the WebDriver
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, timeout = 10 * 60) # wait ten minutes

        # Set up AI Agent
        self.agent = Agent(model=model, secrets_file="secrets.txt")
        self.agent.add_context(experiment_prompt)

        # Keep track of previous round results
        self.previous_rounds = DataFrame(columns=["Round", "Offer for Other", "Offer for You", "Your Decision"])

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
        print("Waiting on offer...")
        spinner_chars = ["-", "\\", "|", "/"]
        index = 0
        while "p_decision1" not in self.driver.page_source:
            sys.stdout.write(f"\r{spinner_chars[index]}")
            sys.stdout.flush()
            index = (index + 1) % len(spinner_chars)
            time.sleep(0.5)

        # Get the offer
        offer = 10 - int(self.driver.find_element(By.NAME, "p_decision1").get_attribute("value"))
        print(f"\nResponder got offer of: {offer}")

        # Add the offer to the previous rounds
        round_prompt = f"You are the responder. Previous rounds:\n{self.previous_rounds.to_string(index=False)}\n"
        round_prompt += f"Current Offer for Other: ${10 - offer}. Current Offer for You: ${offer}.\n"
        round_prompt += f"Do you accept or reject the offer?"
        print(f"Round prompt: \n{round_prompt}\n")
        
        # Prompt the agent to make a decision
        offer_json = json.loads(self.agent.prompt(round_prompt))
        choice = offer_json["choice"]
        explanation = offer_json["explanation"]
        self.previous_rounds.loc[round_number - 1] = [round_number, 10 - offer, offer, "Accept" if choice == "a" else "Reject"]
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

    # Log the results
    if not os.path.exists("logs"):
        os.makedirs("logs")
    # pkl veconlab into a log with timestamp (year, month, day, hour, minute)
    with open(f"logs/log_{time.strftime('%Y%m%d%H%M')}.pkl", "wb") as log_file:
        pickle.dump(veconlab, log_file)

# Run the experiment
if __name__ == "__main__":
    run_experiment("xaty1", "Agent", "Prime")
