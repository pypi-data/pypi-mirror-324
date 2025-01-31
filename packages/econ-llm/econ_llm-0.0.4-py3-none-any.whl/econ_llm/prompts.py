# List of prompts for the AI agnents

def format_prompt(role: str = "user", prompt_text: str = "") -> dict:
    """
    Format the prompt text for the OpenAI API. Used for priority messages.

    Parameters
    ----------
    role : str
        The role of the user generating the prompt (default is "user").
    prompt_text : str
        The text prompt to generate a response for.

    Returns
    -------
    dict
        The formatted prompt for the OpenAI API.

    Examples
    --------
    >>> response = agent.format_dev("Once upon a time")
    """
    # Gaurd against empty prompt text
    if not prompt_text:
        raise ValueError("Prompt text cannot be empty.")
    
    # Validate role
    role = role.lower()
    if role not in ["user", "developer", "assistant"]:
        raise ValueError(f"Invalid role: {role}")
    
    # Format the prompt based on the role
    message = {
        "role": role,
        "content": [
            {
                "type": "text",
                "text": prompt_text
            }
        ]
    }
    return message
