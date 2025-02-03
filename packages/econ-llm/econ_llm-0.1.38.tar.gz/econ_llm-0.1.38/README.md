# econ-llm
A python package that uses LLM agents to automate experiments using the VEcon Lab Website.

## ToDo 
- [ ] Update proposer context in prompts.py 
- [ ] Update readme with new commands

## Installation
To install the package, run the following command:
```bash
pip install econ-llm
```

## Usage
Note: you need a `secrets.txt` in the same directory as execution with the following two lines:
OpenAI_API_KEY
Github_Username Github_Access_Token

## Commands
### Run
Assumes `secrets.txt` is already set. To run an experiment (multi-round ultimatum game), use the following command:
```bash
econ-llm run [experiment_id] [user_id]
```
### Upload
Assumes `secrets.txt` and git credentials are set. To upload the logs directory, use the following command:
```bash
To upload logs directory:
```bash
econ-llm upload
```

### Upgrade
To update the package, use the following command:
```bash
econ-llm upgrade
```

## Output
The output will be saved in the `output` directory in the directory where the command was executed. Run numbers are automatically incremented.

## Specification
The package is currently using `gpt-4o-2024-08-06` as the modeol from OpenAI.

## Dependencies
Assumes you have
```bash
sudo apt install python3
sudo apt install python3-pip
sudo apt install python3-venv
```bash
