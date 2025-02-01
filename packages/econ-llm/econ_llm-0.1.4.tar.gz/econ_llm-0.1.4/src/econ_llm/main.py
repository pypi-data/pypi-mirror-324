import sys
from . import experiment as exp
import chromedriver_autoinstaller

def main():
    # Automatically install the latest version of chromedriver
    chromedriver_autoinstaller.install()

    # Check if the user provided the correct number of arguments
    if len(sys.argv) < 2:
        print("Usage: econ-llm run [experiment_name] [first_name] [last_name]")
        sys.exit(1)
    
    command = sys.argv[1]
    if command == "run":
        args = sys.argv[2:]
        print(f"Running with arguments: {args}")
        exp.run_experiment(*args)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()