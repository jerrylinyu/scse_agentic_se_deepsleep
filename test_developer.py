import json
from pathlib import Path
from run_developer import *

def test_planner():
    input_filename = "plan.json"
    output_path = Path("generated") / "navigation_logic.py"

    plan = read_json(input_filename)

    code = run_developer(plan)

    write_json(code, "navigation_logic.py")
    assert output_path.is_file(), "ERROR: The navigation_logic.py file has not been generated."

    with open(output_path, "r") as file:
        saved_plan = file.read()
    assert saved_plan, "ERROR: The content of navigation_logic.py is empty."

    print("Planner Agent output in navigation_logic.py\n")
    print(saved_plan)
    print("\nPASS: Agent smoke tests in test_developer is pass")

if __name__ == "__main__":
    test_planner()