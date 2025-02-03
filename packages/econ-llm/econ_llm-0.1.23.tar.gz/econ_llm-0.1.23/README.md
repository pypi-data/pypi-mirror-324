# econ-llm
A python package that uses LLM agents to automate experiments using the VEcon Lab Website.

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
To run an experiment (multi-round ultimatum game), use the following command:
```bash
econ-llm run [experiment_id] [user_id]
```
### Upload
To upload the logs directory, use the following command:
```bash
To upload logs directory:
```bash
econ-llm upload
```

### Upgrade
To upgrade the package, use the following command:
```bash
econ-llm upgrade
```

## Output
The output will be saved in the `output` directory in the directory where the command was executed. Run numbers are automatically incremented.

## Specification
The package is currently using `gpt-3.5-turbo` as the modeol from OpenAI.
