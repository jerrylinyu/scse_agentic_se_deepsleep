import json
from pathlib import Path
from analyst_agent import run_analyst

def load_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print("This file doesn't exist")
    except OSError:
        print("An error occurred when trying to read the file")

def write_file(data):
    path = Path("artifacts") / "requirements.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    brief = load_file("brief.txt")
    data = run_analyst(brief)
    write_file(data)
    print("Successful writing")

if __name__ == "__main__":
    main()
