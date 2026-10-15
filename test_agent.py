import json
from ollama import chat

SYSTEM_PROMPT = """
You are the Test Agent in a multi-agent software engineering system.
# Role
Generate pytest-style test code for the robot navigation function
`decide_next_move(state)`.
# Input
- requirements: JSON object with the navigation requirements
- plan: JSON object with the navigation plan
# MANDATORY OUTPUT RULES
1. Output ONLY pure Python test code. Nothing else.
2. NO explanations, NO markdown, NO ``` fences, NO comments outside the code.
3. The VERY FIRST line of your output MUST be exactly:
   from generated.navigation_logic import decide_next_move
4. Do NOT define the `decide_next_move` function yourself. It already exists.
   You only IMPORT it and TEST it.
5. Every test function name MUST start with `test_`.
6. Each test MUST call `decide_next_move(state)` and use `assert` to check
   the returned action.
# State dictionary keys
- `front_blocked` (bool)
- `left_blocked` (bool)
- `right_blocked` (bool)
- `goal_ahead` (bool)
- `goal_on_left` (bool)
- `goal_on_right` (bool)
- `target_reached` (bool)
# Required test coverage
- Goal reached → STOP
- Goal ahead and clear → FORWARD
- Front blocked but goal on left → LEFT
- Front blocked but goal on right → RIGHT
- All directions blocked → STOP
# Example of the FIRST 3 lines of your output
from generated.navigation_logic import decide_next_move
def test_goal_reached():
    ...
"""


def clean_test_output(raw_text: str) -> str:
    lines = raw_text.splitlines()
    out_lines = []
    in_fence = False
    for line in lines:
        s = line.strip()
        if s.startswith("```"):
            in_fence = not in_fence
            continue
        out_lines.append(line)
    code = "\n".join(out_lines).strip()

    required_import = "from generated.navigation_logic import decide_next_move"
    if not code.startswith(required_import):
        if required_import not in code:
            code = required_import + "\n\n" + code

    final_lines = []
    skip_def = False
    for l in code.splitlines():
        if l.lstrip().startswith("def decide_next_move"):
            skip_def = True
            continue
        if skip_def:
            if l and not l.startswith((" ", "\t")):
                skip_def = False
            else:
                continue
        final_lines.append(l)
    return "\n".join(final_lines).strip()


def validate_test_code(code):
    if not isinstance(code, str):
        raise TypeError("Test code must be a string")
    if code.strip() == "":
        raise ValueError("Test code cannot be empty")
    if "```" in code:
        raise ValueError("Test code must not contain markdown code fences")
    required_keywords = [
        "def test_",
        "from generated.navigation_logic import decide_next_move",
        "decide_next_move(",
        "assert",
    ]
    for keyword in required_keywords:
        if keyword not in code:
            raise ValueError(f"Test code is missing required keyword: {keyword}")
    try:
        compile(code, filename="<generated_test>", mode="exec")
    except SyntaxError as e:
        raise ValueError(f"Generated test code has syntax error: {e}")
    return True


def run_test_agent(requirements, plan):
    user_prompt = (
        "REQUIREMENTS:\n"
        + json.dumps(requirements, indent=4)
        + "\n\nPLAN:\n"
        + json.dumps(plan, indent=4)
        + "\n\nGenerate ONLY the pytest test code. "
        "Start with the import line. No markdown, no explanations."
    )
    response = chat(
        model="qwen3:8b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
    )
    raw_code = response.message.content
    test_code = clean_test_output(raw_code)
    validate_test_code(test_code)
    return test_code
