# econ-llm
A python package that uses LLM agents to automate experiments using the VEcon Lab Website.

## Installation
To install the package, run the following command:
```bash
pip install econ-llm
```

## Usage
Note: you need a `secrets.txt` in the same directory as execution with an OpenAI API key.
```bash
econ-llm run [experiment_id] [first_name] [last_name] [rounds (optional)]
```

## Output
The output will be saved in the `output` directory in the directory where the command was executed. Run numbers are automatically incremented.

## Specification
The package is currently using `gpt-3.5-turbo` as the modeol from OpenAI.
