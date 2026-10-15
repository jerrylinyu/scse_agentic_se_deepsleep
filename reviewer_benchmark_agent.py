import json
from ollama import chat

benchmark_reviewer_sys = '''
You are benchmark reviewer agent.
You receive benchmark report AND a deterministic review template with fixed boolean flags.
You must keep all boolean values EXACTLY as given in deterministic review.
Only rewrite natural‑language text for issue, likely_cause, recommendation.
Output ONLY pure JSON object, no markdown, no extra text.
Required keys: issue(str), likely_cause(str), recommendation(str), safety_passed(bool), goal_completion_passed(bool), efficiency_passed(bool), needs_revision(bool).
'''

def validate_benchmark_review(data:dict) -> bool:
    req_keys = {"issue","likely_cause","recommendation","safety_passed","goal_completion_passed","efficiency_passed","needs_revision"}
    if not isinstance(data,dict):
        raise ValueError("Must be dict")
    if not req_keys.issubset(data.keys()):
        raise ValueError(f"Missing keys: {req_keys}")
    for boolkey in ("safety_passed","goal_completion_passed","efficiency_passed","needs_revision"):
        if not isinstance(data[boolkey],bool):
            raise ValueError(f"{boolkey} must be boolean")
    for skey in ("issue","likely_cause","recommendation"):
        if not isinstance(data[skey],str):
            raise ValueError(f"{skey} must be string")
    return True


def build_deterministic_review(benchmark_report:dict) -> dict:
    safety_passed = True
    for res in benchmark_report.get("results",[]):
        if res.get("collision_or_done") is True and res.get("reached_goal") is False:
            safety_passed = False
            break

    success_rate = benchmark_report.get("success_rate",0.0)
    goal_completion_passed = (success_rate >=1.0)

    inefficient_success = benchmark_report.get("inefficient_success_worlds",0)
    eff_rate = benchmark_report.get("efficiency_rate",0.0)
    efficiency_passed = (inefficient_success ==0 and eff_rate >=1.0)

    needs_revision = not (safety_passed and goal_completion_passed and efficiency_passed)

    issue = ""
    if not safety_passed:
        issue = "Unsafe benchmark behavior detected"
    elif not goal_completion_passed:
        issue = "Goal completion failure"
    elif not efficiency_passed:
        issue = "Successful but inefficient navigation"

    return {
        "issue":issue,
        "likely_cause":"",
        "recommendation":"",
        "safety_passed":safety_passed,
        "goal_completion_passed":goal_completion_passed,
        "efficiency_passed":efficiency_passed,
        "needs_revision":needs_revision
    }


def run_benchmark_reviewer_agent(benchmark_report:dict) -> dict:
    det_review = build_deterministic_review(benchmark_report)
    user_payload = {
        "benchmark_report": benchmark_report,
        "deterministic_review_fixed_booleans": det_review
    }
    resp = chat(
        model="qwen3:8b",
        messages=[
            {"role":"system","content":benchmark_reviewer_sys},
            {"role":"user","content":json.dumps(user_payload,indent=2)}
        ]
    )
    raw = resp.message.content
    parsed = json.loads(raw)
    # force boolean flags from deterministic review (defend against llm changing bools)
    parsed["safety_passed"] = det_review["safety_passed"]
    parsed["goal_completion_passed"] = det_review["goal_completion_passed"]
    parsed["efficiency_passed"] = det_review["efficiency_passed"]
    parsed["needs_revision"] = det_review["needs_revision"]
    validate_benchmark_review(parsed)
    return parsed

