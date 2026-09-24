## the logic is similar to the run_planner and run_analyst files
import json
from pathlib import Path
from developer_agent import run_developer


def read_json(filename):
    path = Path("artifacts") / filename
    with open(path, 'r') as file:
        return json.load(file)

def write_json(result, filename):
    path = Path("generated") / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as file:
        file.write(result)

def main():
    plan = read_json("plan.json")

    code = run_developer(plan)

    write_json(code, "navigation_logic.py")


if __name__ == "__main__":
    main()

