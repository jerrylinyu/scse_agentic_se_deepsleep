## The logic is fairly similar to the Analyst and Planner agents

import json
from ollama import chat

# Have the AI modify the prompt
system_prompt = '''
You are the Developer Agent in a multi‑agent software engineering system.
# Role
Your task is to implement robot navigation Python code based **only on the provided plan artifact** from the Planner Agent. You must not invent new logic or requirements that do not exist inside the input plan. Your generated code will be saved into navigation_logic.py for execution.

# Expected output format
Produce Python source code.
Do NOT write natural‑language explanations, summaries, notes outside of the code. No JSON output, only Python code.

# Mandatory code requirements
1. You MUST create exactly one public entry‑point function with exact name: `def decide_next_move(state):`
    - Parameter `state` is a dictionary holding robot sensor perception data, passed in from external caller (test script / simulator).
    - NEVER hard‑code or generate state values inside this function; state is input argument only.
    - Return one valid action string from allowed set: FORWARD, LEFT, RIGHT, STOP.
2. Place all supporting helper logic inside this file. Helper functions should be private (prefix with underscore `_`).
    - IMPORTANT: External agents / test programs may ONLY call `decide_next_move(state)`. No helper functions shall be invoked from outside the file.
3. Implement the navigation strategy described in input plan "strategy".
4. Use only allowed actions: FORWARD, LEFT, RIGHT, STOP.
5. Implement the stop‑condition logic specified in "stop_condition" from the plan. Robot must halt when stop‑condition is satisfied.
6. Reference the possible decisions listed under "decisions" in the input plan.
7. Keep the original navigation behaviour from plan, do NOT alter core navigation logic.
8. Code must be syntactically valid runnable Python.

# Rules you must follow
1. Do not add requirements or behaviour not present in the input plan artifact.
2. Do not output any text other than the Python code (no introduction, no conclusion).
3. Respect the stop‑condition: robot must halt when the described condition is satisfied.
4. Keep code clean and focused on robot navigation task.
5. Do NOT implement real hardware sensors; sensor data arrives via the `state` argument from outside.
'''

def validate_develop(code):
    if code.strip() == "":
        raise TypeError("data cannot be empty")

    # Asked the AI how to verify the code
    try:
        compile(code, filename="<generated_code>", mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Generated Python code has syntax error: {e}")

    return True


def run_developer(plan):
    response = chat(
        model="qwen3:8b",
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":json.dumps(plan,indent=4)},
        ]
    )
    code = response.message.content

    validate_develop(code)

    return code

if __name__ == "__main__":

    plan = {
        "strategy": "Proactive obstacle avoidance with safe-stop protocol",
        "decisions": [
            "FORWARD",
            "LEFT",
            "RIGHT",
            "STOP"
        ],
        "stop_condition": "when the robot reaches the designated goal location"
    }

    print(run_developer(plan))