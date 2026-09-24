import json
from pathlib import Path
from run_planner import *

def test_planner():
    input_filename = "requirements.json"
    output_path = Path("artifacts") / "plan.json"

    requirement = read_json(input_filename)

    raw_output = run_planner(requirement)

    plan_data = json.loads(raw_output)

    write_json(plan_data, "plan.json")
    assert output_path.is_file(), "ERROR: The plan.json file has not been generated."

    with open(output_path, "r") as file:
        saved_plan = json.load(file)
    assert saved_plan, "ERROR: The content of plan.json is empty."

    print("Planner Agent output in plan.json\n")
    print(json.dumps(saved_plan, indent=4))
    print("\nPASS: Agent smoke tests in test_planner is pass")

if __name__ == "__main__":
    test_planner()
