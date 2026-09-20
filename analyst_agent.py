import json
from ollama import chat

def build_prompt(brief):
    # Let the AI help me modify the system_prompt & user_prompt.
    system_prompt = """
    You are a requirements‑engineering analyst agent for robot navigation.
    Task: Extract navigation requirements from the customer brief and output ONLY pure valid JSON.

    Strict mandatory rules:
    1. Output nothing except JSON. No explanations, no notes, no markdown, no ```json or ``` markers. Zero extra characters outside JSON object.
    2. Your JSON MUST exactly follow this template, exactly four keys, NO missing keys, NO extra keys:
    {
        "goal": "string",
        "allowed_actions": ["FORWARD", "LEFT", "RIGHT", "STOP"],
        "safe_stop": <boolean>,
        "avoid_obstacles": <boolean>
    }
    3. Key‑by‑key rules:
        - "goal": string value: describe robot navigation objective extracted only from brief text.
        - "allowed_actions": list, must contain exactly these four string values: "FORWARD", "LEFT", "RIGHT", "STOP". Do not remove or add items.
        - "safe_stop": boolean true/false (NOT quoted string). Set true if robot must stop when no safe direction available.
        - "avoid_obstacles": boolean true/false (NOT quoted string). Set true if robot must avoid blocked obstacles.
    4. Use only information present in input brief, do NOT invent new requirements.
    """
    user_prompt = f"""
    Customer brief text:
    \"\"\"{brief}\"\"\"

    Generate only the JSON requirements based strictly on the brief content given above.
    """
    return system_prompt, user_prompt

def ask_qwen(system_prompt, user_prompt):
    response = chat(
        model="qwen3:8b",
        messages=[
            {"role":"system", "content": system_prompt},
            {"role":"user", "content": user_prompt}
        ]
    )
    return response.message.content

def validate_requirements(data):
    if not isinstance(data, dict):
        raise ValueError("data must be a dict")

    if "goal" not in data:
        raise ValueError("key goal is missing")
    if "allowed_actions" not in data:
        raise ValueError("key allowed_actions is missing")
    if "safe_stop" not in data:
        raise ValueError("key safe_stop is missing")
    if "avoid_obstacles" not in data:
        raise ValueError("key avoid_obstacles is missing")

    items_list = ["goal", "allowed_actions", "safe_stop", "avoid_obstacles"]
    for item in data:
        if item not in items_list:
            raise ValueError(f"key {item} is invalid")

    if not isinstance(data["goal"], str):
        raise ValueError("goal must be a string")
    if not isinstance(data["allowed_actions"], list):
        raise ValueError("allowed_actions must be a list")
    if not isinstance(data["safe_stop"], bool):
        raise ValueError("safe_stop must be a boolean")
    if not isinstance(data["avoid_obstacles"], bool):
        raise ValueError("avoid_obstacles must be a boolean")

    action_list = ["FORWARD", "LEFT", "RIGHT", "STOP"]
    for action in data["allowed_actions"]:
        if action not in action_list:
            raise ValueError("The value in allowed_actions is illegal")

    return True

def run_analyst(brief):
    system_prompt, user_prompt = build_prompt(brief)
    response = ask_qwen(system_prompt, user_prompt)
    data = json.loads(response)
    validate_requirements(data)
    
    return data