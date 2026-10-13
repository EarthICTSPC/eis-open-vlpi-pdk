"""Dependency-aware KKA schedule model; not a physical simulator."""
from __future__ import annotations
import json
from pathlib import Path

FIXTURE = Path(__file__).with_name("EIS-KKA-CRITICAL-PATH-001.json")


def analyze(model: dict) -> dict:
    tasks = {task["id"]: task for task in model["tasks"]}
    if len(tasks) != len(model["tasks"]):
        raise ValueError("task IDs must be unique")
    finish: dict[str, int] = {}
    start: dict[str, int] = {}
    visiting: set[str] = set()

    def schedule(task_id: str) -> int:
        if task_id in finish:
            return finish[task_id]
        if task_id in visiting:
            raise ValueError(f"dependency cycle at {task_id}")
        if task_id not in tasks:
            raise ValueError(f"unknown dependency {task_id}")
        visiting.add(task_id)
        task = tasks[task_id]
        deps = task["deps"]
        start[task_id] = max((schedule(dep) for dep in deps), default=0)
        duration = task["duration_ps"]
        if type(duration) is not int or duration < 0:
            raise ValueError(f"{task_id}: duration_ps must be a non-negative integer")
        finish[task_id] = start[task_id] + duration
        visiting.remove(task_id)
        return finish[task_id]

    for task_id in tasks:
        schedule(task_id)

    end_ps = max(finish.values(), default=0)
    target = model["service"]["target_ps"]
    missing_energy = [t["id"] for t in model["tasks"] if t.get("energy_pj") is None]
    missing_power = [t["id"] for t in model["tasks"] if t.get("peak_power_mw") is None]
    return {
        "start_ps": start,
        "finish_ps": finish,
        "critical_path_ps": end_ps,
        "target_ps": target,
        "margin_ps": target - end_ps,
        "target_met_in_model": end_ps <= target,
        "energy_evaluable": not missing_energy,
        "missing_energy_tasks": missing_energy,
        "peak_power_evaluable": not missing_power,
        "missing_power_tasks": missing_power,
        "physical_validation": False,
    }


if __name__ == "__main__":
    model = json.loads(FIXTURE.read_text(encoding="utf-8"))
    print(json.dumps(analyze(model), indent=2))
