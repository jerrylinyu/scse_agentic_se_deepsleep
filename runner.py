import json
from pathlib import Path


def run_simulation():
    from generated.navigation_logic import decide_next_move

    scenarios = [
        {"state":{"front_blocked":False,"left_blocked":False,"right_blocked":False,"goal_ahead":True,"goal_on_left":False,"goal_on_right":False}, "expected":"FORWARD"},
        {"state":{"front_blocked":True,"left_blocked":False,"right_blocked":False,"goal_ahead":True,"goal_on_left":False,"goal_on_right":False}, "expected":"LEFT"},
        {"state":{"front_blocked":True,"left_blocked":True,"right_blocked":False,"goal_ahead":False,"goal_on_left":False,"goal_on_right":True}, "expected":"RIGHT"},
        {"state":{"front_blocked":False,"left_blocked":True,"right_blocked":False,"goal_ahead":False,"goal_on_left":False,"goal_on_right":True}, "expected":"RIGHT"},
        {"state":{"front_blocked":False,"left_blocked":False,"right_blocked":True,"goal_ahead":False,"goal_on_left":True,"goal_on_right":False}, "expected":"LEFT"},
        {"state":{"front_blocked":True,"left_blocked":True,"right_blocked":True,"goal_ahead":False,"goal_on_left":False,"goal_on_right":False}, "expected":"STOP"}
    ]
    results = []
    passed = 0
    failed = 0
    for sc in scenarios:
        act = decide_next_move(sc["state"])
        ok = (act == sc["expected"])
        if ok:
            passed +=1
        else:
            failed +=1
        results.append({
            "state":sc["state"],
            "expected":sc["expected"],
            "actual":act,
            "pass":ok
        })
    total = len(scenarios)
    success_rate = passed / total if total>0 else 0.0
    report = {
        "total_scenarios":total,
        "passed_scenarios":passed,
        "failed_scenarios":failed,
        "success_rate":success_rate,
        "scenario_results":results
    }
    return report
