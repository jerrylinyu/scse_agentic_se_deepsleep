## A typical test case:
""" {
    "goal_ahead": True,
    "goal_on_left": False,
    "goal_on_right": False,
    "front_blocked": False,
    "left_blocked": False,
    "right_blocked": False
},
"FORWARD" """
## Use the above test case to create more test cases for all the possible states

# test_generated_navigation_logic.py
import importlib.util
from pathlib import Path

def test_generated_navigation_logic():
    gen_file = Path("generated") / "navigation_logic.py"

    assert gen_file.is_file(), "ERROR: The file navigation_logic.py does not exist."
    source_code = gen_file.read_text()
    assert len(source_code.strip()) > 0, "ERROR: The content of the file navigation_logic.py is empty."

    # AI says that `compile()` is a built-in function in Python.
    # It only performs syntax compilation checks and does not run or execute the code.
    compile(source_code, filename=str(gen_file), mode="exec")

    spec = importlib.util.spec_from_file_location("navigation_module", gen_file)
    nav_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(nav_module)

    decide_next_move = nav_module.decide_next_move

    # Let the AI provide me with the test cases it has generated.
    test_cases = [
        ({"target_reached": True, "front_clear": False, "left_clear": False, "right_clear": False}, "STOP"),
        ({"target_reached": False, "front_clear": True, "left_clear": False, "right_clear": False}, "FORWARD"),
        ({"target_reached": False, "front_clear": False, "left_clear": True, "right_clear": False}, "LEFT"),
        ({"target_reached": False, "front_clear": False, "left_clear": False, "right_clear": True}, "RIGHT"),
        ({"target_reached": False, "front_clear": False, "left_clear": False, "right_clear": False}, "STOP"),
    ]

    passed = 0
    failed = 0

    print("Running Level‑2 Behaviour Tests for decide_next_move()")
    for idx, (state, expected) in enumerate(test_cases, start=1):
        try:
            actual = decide_next_move(state)
            assert actual == expected, f"Case{idx}fail：expect={expected}，actual={actual}"
            print(f"PASS: Case {idx} PASS | state={state} | output={actual}")
            passed += 1
        except AssertionError as err:
            print(f"ERROR: Case {idx} FAIL | {err}")
            failed += 1

    print("\n===== Test Summary =====")
    print(f"Total: {len(test_cases)} | Passed: {passed} | Failed: {failed}")
    error_msg = f"{failed} test cases have failed."
    assert failed == 0 , error_msg
    print("PASS: All Level‑2 behaviour tests passed!")


if __name__ == "__main__":
    test_generated_navigation_logic()


