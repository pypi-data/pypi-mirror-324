import sys
from . import experiment as exp # multi round ultimatum game
from . import ultimatum_exp as ult # multi stage ultimatum game
import chromedriver_autoinstaller

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
    elif command == "ult": # ult stands for ultimatum
        print("Running ultimatum game experiment")
        ult.run_ultimatum_experiment()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()