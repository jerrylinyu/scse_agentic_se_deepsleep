import json
import sys
from pathlib import Path

from analyst_agent import run_analyst
from planner_agent import run_planner
from developer_agent import run_developer, run_developer_revision
from test_agent import run_test_agent
from runner import run_simulation
from reviewer_agent import run_reviewer_agent
from benchmark_irsim import run_all_benchmark
from reviewer_benchmark_agent import run_benchmark_reviewer_agent

TRACE_LOG = Path("trace.log")

def log_event(message: str):
    line = f"{message}\n"
    print(line.rstrip("\n"))
    with open(TRACE_LOG, "a", encoding="utf-8") as f:
        f.write(line)

def ensure_directories():
    Path("artifacts").mkdir(exist_ok=True)
    Path("generated").mkdir(exist_ok=True)

def read_text_file(filepath: Path) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def write_json_artifact(data: dict, filename: str):
    out = Path("artifacts") / filename
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def write_text_generated(text: str, filename: str):
    out = Path("generated") / filename
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)

def run_full_integration_pipeline():
    ensure_directories()
    if TRACE_LOG.exists():
        TRACE_LOG.unlink()

    log_event("==== Starting Integration & Simulation full pipeline ====")

    log_event("Orchestrator: Loading brief.txt")
    brief_text = read_text_file(Path("brief.txt"))

    log_event("Analyst Agent: executing run_analyst()")
    requirements = run_analyst(brief_text)
    write_json_artifact(requirements, "requirements.json")
    log_event('Analyst Agent created artifacts/requirements.json')

    log_event("Planner Agent: executing run_planner()")
    plan_json_str = run_planner(requirements)
    plan = json.loads(plan_json_str)
    write_json_artifact(plan, "plan.json")
    log_event('Planner Agent created artifacts/plan.json')

    log_event("Developer Agent: executing run_developer()")
    nav_code = run_developer(plan)
    write_text_generated(nav_code, "navigation_logic.py")
    log_event("Developer Agent created generated/navigation_logic.py")

    log_event("Test Agent: executing run_test_agent()")
    generated_test_code = run_test_agent(requirements, plan)
    write_text_generated(generated_test_code, "test_decide_next_move.py")
    log_event("Test Agent created generated/test_decide_next_move.py")

    log_event("Simulation Runner: executing run_simulation()")
    sim_report = run_simulation()
    write_json_artifact(sim_report, "simulation_report.json")
    log_event("Simulation Runner created artifacts/simulation_report.json")

    log_event("Reviewer Agent: executing run_reviewer_agent()")
    sim_review = run_reviewer_agent(sim_report)
    write_json_artifact(sim_review, "sim_review_notes.json")
    log_event("Reviewer Agent created artifacts/sim_review_notes.json")

    log_event("IRSIM Benchmark: executing run_all_benchmark()")
    bench_report = run_all_benchmark()
    log_event("IRSIM Benchmark created artifacts/irsim_benchmark_report.json")

    log_event("Benchmark Reviewer Agent: executing run_benchmark_reviewer_agent()")
    bench_review = run_benchmark_reviewer_agent(bench_report)
    write_json_artifact(bench_review, "benchmark_review_notes.json")
    log_event("Benchmark Reviewer Agent created artifacts/benchmark_review_notes.json")

    log_event("==== Pipeline execution finished ====")


if __name__ == "__main__":
    run_full_integration_pipeline()
