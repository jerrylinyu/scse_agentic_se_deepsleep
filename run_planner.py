import json
from pathlib import Path
from planner_agent import run_planner


## Create a function/logic that reads the requirements from requirements.json, 
# then calls the run_planner function with the requirements as input, and finally writes the validated plan to plan.json. 
def read_json(filename):
    path = Path("artifacts") / filename
    with open(path, 'r') as file:
        return json.load(file)

def write_json(result, filename):
    path = Path("artifacts") / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as file:
        json.dump(result, file, indent=4)

def main():
    requirement = read_json("requirements.json")

    data = run_planner(requirement)



    write_json(json.loads(data), "plan.json")


if __name__ == "__main__":
    main()

