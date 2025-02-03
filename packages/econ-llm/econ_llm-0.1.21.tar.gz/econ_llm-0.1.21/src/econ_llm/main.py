import sys
from . import experiment as exp # multi round ultimatum game
from . import ultimatum_exp as ult # multi stage ultimatum game
import chromedriver_autoinstaller
import subprocess

# Define repository details
repo_dir = "./logs"

def upload():
    # Read the user's name and email from secrets.txt
    with open("secrets.txt", "r") as f:
        _ = f.readline().strip()
        username, token = f.readline().strip().split(" ")
    # Define the remote repository URL
    remote_url = f"https://{username}:{token}@github.com/JawandS/econ-llm-data.git"
    # Initialize the repository
    subprocess.run(["git", "init"], cwd=repo_dir, check=True)
    # Add the remote url
    subprocess.run(["git", "remote", "add", "origin", remote_url], cwd=repo_dir, check=True)
    # Add all files to the repository
    subprocess.run(["git", "add", "."], cwd=repo_dir, check=True)
    # Commit the changes
    subprocess.run(["git", "commit", "-m", "Upload results"], cwd=repo_dir, check=True)
    # Push the changes to the remote repository
    subprocess.run(["git", "push", "-u", "origin", "master"], cwd=repo_dir, check=True)
    # Print a success message
    print("Results uploaded successfully")

def main():
    # Automatically install the latest version of chromedriver
    chromedriver_autoinstaller.install()

    # Check if the user provided the correct number of arguments
    if len(sys.argv) < 2:
        print("Usage: econ-llm run [experiment_name] [user_id]")
        sys.exit(1)
    
    command = sys.argv[1]
    if command == "run":
        args = sys.argv[2:]
        print(f"Running with arguments: {args}")
        exp.run_experiment(*args)
        print("Results upload started")
        upload()
    elif command == "ult": # ult stands for ultimatum
        print("Running ultimatum game experiment")
        ult.run_ultimatum_experiment()
        print("Results upload started")
        upload()
    elif command == "upload": # upload the results to the server
        print("Results upload started")
        upload()
    elif command == "upgrade":
        print("Upgrading the package")
        subprocess.run(["pip", "install", "--upgrade", "econ-llm"], check=True)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    upload()