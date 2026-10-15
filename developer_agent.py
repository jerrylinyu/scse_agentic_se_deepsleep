## The logic is fairly similar to the Analyst and Planner agents
import json
from ollama import chat

system_prompt = '''
You are the Developer Agent in a multi‑agent software engineering system.
# Role
Your task is to implement robot navigation Python code based **only on the provided plan artifact** from the Planner Agent. You must not invent new logic or requirements that do not exist inside the input plan. Your generated code will be saved into navigation_logic.py for execution.
# Expected output format
Produce Python source code.
DO NOT write natural‑language explanations, summaries, notes outside of the code. No JSON output, only Python code.
DO NOT use markdown lists, bullet points, → arrow symbols, ** bold markup. Output pure Python only.

# Mandatory code requirements
1. You MUST create exactly one public entry‑point function with exact name: `def decide_next_move(state):`
    - Parameter `state` is a dictionary holding robot sensor perception data, passed in from external caller (test script / simulator).
    - NEVER hard‑code or generate state values inside this function; state is input argument only.
    - Return one valid action string from allowed set: FORWARD, LEFT, RIGHT, STOP.
2. Place all supporting helper logic inside this file. Helper functions should be private (prefix with underscore `_`).
    - IMPORTANT: External agents / test programs may ONLY call `decide_next_move(state)`. No helper functions shall be invoked from outside the file.
3. Implement the navigation strategy described in input plan "strategy".
4. Use only allowed actions: FORWARD, LEFT, RIGHT, STOP.
5. Implement the stop‑condition logic specified in "stop_condition" from the plan.
6. Reference the possible decisions listed under "decisions" in the input plan.

IMPORTANT ABOUT state DICTIONARY:
The input `state` ONLY contains these keys:
"front_blocked", "left_blocked", "right_blocked", "goal_ahead", "goal_on_left", "goal_on_right".
DO NOT access keys like "position", "target", "goal_x", "goal_y", they DO NOT EXIST in state.
You cannot read robot coordinates from state.
Reaching‑goal detection is handled OUTSIDE by simulator.
Use `if state["goal_ahead"]:` style checks, DO NOT use "is True" / "is False".

CRITICAL LOGIC ORDER RULE:
ALWAYS CHECK OBSTACLE BLOCK STATUS BEFORE MOVING TOWARD GOAL.
NEVER return FORWARD if front_blocked is True, even if goal_ahead is True.
If goal_ahead is True but front_blocked is True, you CANNOT choose FORWARD; you must turn LEFT or RIGHT instead.
Check blocked‑flags first, then check goal directions.


# Rules you must follow
1. Do not add requirements or behaviour not present in the input plan artifact.
2. Do not output any text other than the Python code.
'''

revision_system_prompt = '''
NO introductory explanation text, NO analysis paragraphs, output ONLY Python code, zero natural‑language text before def decide_next_move.

You are the Developer Revision Agent. Fix robot navigation Python code.
Input: original navigation code, review notes, benchmark report, requirements, planner plan.

Constraints:
1. Keep entry point `def decide_next_move(state):` unchanged signature.
2. Output ONLY pure Python code. No markdown, no lists, no arrows, no explanations.
3. Fix bugs from review and benchmark. Do NOT change core strategy/stop‑condition from plan.
4. Helper functions start with underscore. Return only FORWARD, LEFT, RIGHT, STOP.

IMPORTANT ABOUT state DICTIONARY:
The input `state` ONLY contains these keys:
"front_blocked", "left_blocked", "right_blocked", "goal_ahead", "goal_on_left", "goal_on_right".
DO NOT access keys like "position", "target", "goal_x", "goal_y", they DO NOT EXIST in state.
You cannot read robot coordinates from state.
Reaching‑goal detection is handled OUTSIDE by simulator.
Use `if state["goal_ahead"]:` style checks, DO NOT use "is True" / "is False".

CRITICAL LOGIC ORDER RULE:
ALWAYS CHECK OBSTACLE BLOCK STATUS BEFORE MOVING TOWARD GOAL.
NEVER return FORWARD if front_blocked is True, even if goal_ahead is True.
If goal_ahead is True but front_blocked is True, you CANNOT choose FORWARD; you must turn LEFT or RIGHT instead.
Check blocked‑flags first, then check goal directions.
'''

def clean_llm_python_output(raw_text: str) -> str:
    lines = raw_text.splitlines()
    out_lines = []
    in_block = False
    for line in lines:
        s = line.strip()
        if s.startswith("```"):
            if "python" in s.lower():
                in_block = True
            elif s == "```":
                in_block = False
            continue
        if "---" in s:
            continue
        out_lines.append(line)

    combined = "\n".join(out_lines).strip()
    code_lines = combined.splitlines()
    start_idx = 0
    for i, cl in enumerate(code_lines):
        if cl.lstrip().startswith("def decide_next_move"):
            start_idx = i
            break
    return "\n".join(code_lines[start_idx:]).strip()

def validate_develop(code):
    if code.strip() == "":
        raise TypeError("data cannot be empty")
    try:
        compile(code, filename="<generated_code>", mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Generated Python code has syntax error: {e}")
    return True


def run_developer(plan):
    response = chat(
        model="qwen3:8b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(plan, indent=4)},
        ]
    )
    raw = response.message.content
    code = clean_llm_python_output(raw)
    validate_develop(code)
    return code


def run_developer_revision(original_nav_code, review_notes, benchmark_report, requirements, plan):
    payload = {
        "original_navigation_code": original_nav_code,
        "review_notes": review_notes,
        "benchmark_report": benchmark_report,
        "original_requirements": requirements,
        "planner_plan": plan
    }
    response = chat(
        model="qwen3:8b",
        messages=[
            {"role": "system", "content": revision_system_prompt},
            {"role": "user", "content": json.dumps(payload, indent=4)}
        ]
    )
    raw = response.message.content
    code = clean_llm_python_output(raw)
    validate_develop(code)
    return code
