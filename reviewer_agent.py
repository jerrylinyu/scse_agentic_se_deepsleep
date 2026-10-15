## Create a system prompt for the Reviewer Agent that instructs it to analyze the simulation report and output a JSON object with specific keys.
## The JSON object it outputs must follow a strict schema and contain keys "issue", "likely_cause", "recommendation", and "needs_revision".
## The Reviewer Agent should validate the output to ensure it adheres to the schema and that "needs_revision" is a boolean.
## Create a function to validate the output of the Reviewer Agent.
## It should check that the output is a JSON object with the required keys and that "needs_revision" is a boolean, and the rest of the keys are strings.
## Create a function to run the Reviewer Agent.
## It should take in the simulation report, send it to the Reviewer Agent, and return the validated output.
import json
from ollama import chat

reviewer_sys_prompt = '''
You are simulation reviewer agent. Analyze simulation report.
Output ONLY pure JSON, no markdown, no extra text.
Keys required:
"issue": string describing problem, empty string if no issue.
"likely_cause": string guess root cause.
"recommendation": string improvement advice.
"needs_revision": boolean true/false.
If success_rate >=0.9 set needs_revision false; else true.
'''

def validate_reviewer_output(data:dict) -> bool:
    required_keys = {"issue","likely_cause","recommendation","needs_revision"}
    if not isinstance(data,dict):
        raise ValueError("Review output must be dict")
    if not required_keys.issubset(set(data.keys())):
        raise ValueError(f"Missing keys, need {required_keys}")
    if not isinstance(data["needs_revision"], bool):
        raise ValueError("needs_revision must be boolean")
    for k in ("issue","likely_cause","recommendation"):
        if not isinstance(data[k], str):
            raise ValueError(f"{k} must be string")
    return True


def run_reviewer_agent(simulation_report:dict) -> dict:
    resp = chat(
        model="qwen3:8b",
        messages=[
            {"role":"system","content":reviewer_sys_prompt},
            {"role":"user","content":json.dumps(simulation_report,indent=2)}
        ]
    )
    raw = resp.message.content
    parsed = json.loads(raw)
    validate_reviewer_output(parsed)
    return parsed
