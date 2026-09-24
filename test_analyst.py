import json
from pathlib import Path
from run_analyst import *

# ai推荐不直接调用main，而是分开调用，分开测试
def test_analyst():
    brief_path = Path("brief.txt")
    output_path = Path("artifacts") / "requirements.json"

    brief = load_file(brief_path)
    assert brief is not None, "Failed to read the brief.txt file"

    data = run_analyst(brief)

    write_file(data)
    assert output_path.is_file(), "ERROR: The requirements.json file has not been generated."

    with open(output_path, "r") as file:
        content = file.read()
    requirements_result = json.loads(content)
    assert requirements_result, "ERROR: The requirements.json is empty"

    print("nalyst Agent output in requirements.json\n")
    print(json.dumps(requirements_result, indent=4))
    print("\nPASS: Agent smoke tests in test_analyst is pass")


if __name__ == "__main__":
    test_analyst()
