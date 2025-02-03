# Automatically Run the Multi-Round Ultimatum Game through VeconLab as the Second Player

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
from .prompts import proposer_context, responder_context
import json
import time
import os, sys

# Import for debugging
import traceback

class VeconLabAutomation:
    """
    A class to automate interactions with VeconLab using Selenium.
    """

    def __init__(self, session_id: str, user_id: str, model: str = "gpt-4o-2024-08-06", rounds: int = 10):
        """
        Initialize the Selenium WebDriver and user credentials.

        Parameters
        ----------
        session_id: str
            The session ID for the game.
        user_id: str
            The user's ID. Used as user_id user_id for the AI agent.
        password: str
            The user's password.
        """
        # Set up user credentials
        self.session_id = session_id
        self.user_id = user_id

        # Set up the WebDriver
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, timeout = 10 * 60) # wait ten minutes

        # Set up AI Agent
        self.agent = Agent(model=model, secrets_file="secrets.txt")
        self.role = "unknown"

        # Keep track of previous round results
        self.rounds = rounds
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
        self.driver.find_element(By.NAME, "first_name").send_keys(self.user_id)
        self.driver.find_element(By.NAME, "last_name").send_keys(self.user_id)
        self.driver.find_element(By.NAME, "password").send_keys(self.user_id)
        self.driver.find_element(By.NAME, "password_check").send_keys(self.user_id)
        
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

    def propose(self, round_number: int):
        """
        Propose an offer to the responder.

        Parameters
        ----------
        round_number: int
            The current run number.
        """
        # Log
        print(f"Playing game run {round_number}:")
        if round_number == 1:
            print("Proposing an offer...")
        else:
            print("Waiting on response...")
        spinner_chars = ["-", "\\", "|", "/"]
        index = 0
        while "select" not in self.driver.page_source:
            sys.stdout.write(f"\r{spinner_chars[index]}")
            sys.stdout.flush()
            index = (index + 1) % len(spinner_chars)
            time.sleep(0.5)

        # Prompt the agent to make a decision
        if round_number == 1:
            round_prompt = "You are the proposer. Previous rounds: None.\n"
        else:
            round_prompt = f"You are the proposer. Previous rounds:\n{self.previous_rounds.to_string(index=False)}\n"
        round_prompt += "What offer do you want to make to the responder?"
        print(f"Round prompt: \n{round_prompt}\n")

        # Prompt the agent to make a proposal
        offer_json = json.loads(self.agent.prompt(round_prompt))
        offer = offer_json["offer"]
        explanation = offer_json["explanation"]
        print(f"Agent chose offer: {offer} b/c: {explanation}")
        while True: # check if offer is valid
            try:
                num_offer = int(offer)
                if num_offer < 0 or num_offer > 10:
                    raise ValueError("Invalid offer.")
                else: # Offer is valid
                    break
            except:
                print("INVALID OFFER: {offer}.")
                offer_json = json.loads(self.agent.prompt("Invalid offer. Please enter a number between 0 and 10."))

        # Add the offer to the previous rounds
        self.previous_rounds.loc[round_number - 1] = [round_number, 10 - num_offer, num_offer, "Propose"]

        # Execute the decision
        decision_element = self.driver.find_element(By.TAG_NAME, "select")
        Select(decision_element).select_by_value(str(num_offer))
        print(f"Executed decision: {num_offer}.")

        # Submit the decision
        self.driver.find_element(By.XPATH, "//input[@value='Submit']").click()
        print("Decision submitted.")

        # Confirm the decision
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@value='Confirm Decision']")))
        self.driver.find_element(By.XPATH, "//input[@value='Confirm Decision']").click()
        print("Decision confirmed.")

        # Begin next round if needed
        if round_number < self.rounds:
            print(f"\nBeginning round {round_number + 1}.")
            self.wait.until(EC.presence_of_element_located((By.XPATH, f"//input[@value='Begin Round {round_number + 1}']")))
            self.driver.find_element(By.XPATH, f"//input[@value='Begin Round {round_number + 1}']").click()
        else:
            print("\nFinished all rounds!")

    def respond(self, round_number: int):
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
        if round_number == 1:
            round_prompt = "You are the responder. Previous rounds: None.\n"
        else:
            round_prompt = f"You are the responder. Previous rounds:\n{self.previous_rounds.to_string(index=False)}\n"
        round_prompt += f"Current Offer for Other: ${10 - offer}. Current Offer for You: ${offer}.\n"
        round_prompt += f"Do you accept or reject the offer?"
        print(f"Round prompt: \n{round_prompt}\n")
        
        # Prompt the agent to make a decision
        offer_json = json.loads(self.agent.prompt(round_prompt))
        choice = ""
        while choice not in ["a", "r"]:
            choice = offer_json["choice"]
            explanation = offer_json["explanation"]
            if choice not in ["a", "r"]:
                print(f"INVALID CHOICE: {choice}.")
                offer_json = json.loads(self.agent.prompt("Invalid choice. Please enter 'a' to accept or 'r' to reject the offer."))
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

        # Begin next round if needed
        if round_number < self.rounds:
            print(f"\nBeginning round {round_number + 1}.")
            self.wait.until(EC.presence_of_element_located((By.XPATH, f"//input[@value='Begin Round {round_number + 1}']")))
            self.driver.find_element(By.XPATH, f"//input[@value='Begin Round {round_number + 1}']").click()
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
        for idx in range(4):
            if idx == 2: # identify if the agent is the responder
                bold_content = " ".join([element.text for element in self.driver.find_elements(By.TAG_NAME, "b")])
                first_mover = "Proposer" in bold_content
                if first_mover:
                    print("Agent is the proposer.")
                    self.agent.role = "proposer"
                    self.agent.add_context(proposer_context)
                else:
                    print("Agent is the responder.")
                    self.agent.role = "responder"
                    self.agent.add_context(responder_context)
            self.skip_instructions()
        print("Finished skipping instructions.")

        # Play the game
        for round_number in range(1, self.rounds + 1):
            if self.agent.role == "proposer":
                self.propose(round_number)
            else:
                self.respond(round_number)

        # Close the browser
        self.driver.quit()

# Create a function to run the experiment
def run_experiment(session_id, user_id, rounds=10):
    # Initialize the VeconLabAutomation object
    veconlab = VeconLabAutomation(session_id=session_id, user_id=user_id, rounds=rounds)

    # Log if fails
    try:
        # Run the experiment
        veconlab.run()
    except Exception as e:
        print(f"An error occurred during excution")
        traceback.print_exc()
    finally:
        # get file path
        fp = os.path.join("logs", f"log_{veconlab.session_id}_{veconlab.user_id}_{time.strftime('%Y-%m-%d-%H-%M')}.txt")
        print(f"Experiment completed, logging results to {fp}")
        # Log the results
        if not os.path.exists("logs"):
            os.makedirs("logs")
        # add inormaiton to log file (year, month, day, hour, minute)
        with open(fp, "w") as log_file:
            # Write metadata
            log_file.write("Metadata:\n")
            metadata = {
                "time": time.strftime("%Y-%m-%d %H:%M"),
                "session_id": veconlab.session_id,
                "user_id": veconlab.user_id,
                "ai_role": veconlab.role
            }
            log_file.write(f"{json.dumps(metadata)}\n\n")
            # Write the interactions
            log_file.write("Interactions:\n")
            log_file.write(veconlab.previous_rounds.to_json(index=False))
            log_file.write("\n\n")

            # Write the agent's messages
            log_file.write("Agent Messages:\n")
            for message in veconlab.agent.messages:
                log_file.write(f"{message}\n")
            log_file.write("\n")


# Run the experiment
if __name__ == "__main__":
    run_experiment("xaty1", "Agent", 10)
