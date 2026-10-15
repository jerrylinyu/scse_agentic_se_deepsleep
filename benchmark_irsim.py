import json
import subprocess
from pathlib import Path

WORLD_LIST = [
    Path("irsim_worlds") / "world_easy.yaml",
    Path("irsim_worlds") / "world_medium.yaml",
    Path("irsim_worlds") / "world_hard.yaml",
    Path("irsim_worlds") / "world_custom.yaml"
]

def run_single_world(world_file: Path) -> dict:
    proc = subprocess.run(
        ["python","test_irsim_with_agent.py", str(world_file)],
        capture_output=True,
        text=True
    )
    if proc.returncode !=0:
        raise RuntimeError(f"World {world_file} failed run:\nSTDERR:\n{proc.stderr}\nSTDOUT:\n{proc.stdout}")
    with open(Path("artifacts")/"irsim_report.json","r",encoding="utf-8") as f:
        single_report = json.load(f)
    single_report["world_file"] = str(world_file)
    return single_report


def run_all_benchmark():
    results = []
    for w in WORLD_LIST:
        r = run_single_world(w)
        results.append(r)

    total = len(results)
    reached_goal_count = sum(1 for x in results if x["reached_goal"])
    efficient_count = sum(1 for x in results if x["efficiency_status"]=="efficient")
    inefficient_success_count = sum(1 for x in results if x["efficiency_status"]=="acceptable_but_inefficient")
    failed_count = sum(1 for x in results if not x["reached_goal"])
    total_steps = sum(x["steps_taken"] for x in results)

    success_rate = reached_goal_count / total if total>0 else 0.0
    efficiency_rate = efficient_count / total if total>0 else 0.0
    average_steps = total_steps / total if total>0 else 0.0

    benchmark_report = {
        "total_worlds": total,
        "goals_reached": reached_goal_count,
        "success_rate": success_rate,
        "efficient_worlds": efficient_count,
        "inefficient_success_worlds": inefficient_success_count,
        "failed_worlds": failed_count,
        "efficiency_rate": efficiency_rate,
        "average_steps_taken": average_steps,
        "results": results
    }
    out_path = Path("artifacts")/"irsim_benchmark_report.json"
    with open(out_path,"w",encoding="utf-8") as f:
        json.dump(benchmark_report, f, indent=2)
    print(json.dumps(benchmark_report,indent=2))
    return benchmark_report


if __name__ == "__main__":
    run_all_benchmark()
