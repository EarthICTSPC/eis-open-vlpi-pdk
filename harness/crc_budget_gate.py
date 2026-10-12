"""Reference pre-dispatch latency gate for EIS-CRC-BUDGET-001.

This is a software acceptance boundary, not the production FlexAgent
orchestrator and not physical latency evidence.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE = ROOT / "fixtures" / "EIS-CRC-BUDGET-001.json"


class BudgetRejected(RuntimeError):
    def __init__(self, stage: str, total_ps: int, budget_ps: int):
        self.stage = stage
        self.total_ps = total_ps
        self.budget_ps = budget_ps
        super().__init__(
            f"pipeline_latency_budget_exceeded at {stage}: "
            f"{total_ps} ps > {budget_ps} ps"
        )


def load_fixture(path: Path = DEFAULT_FIXTURE) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def execute_with_budget_gate(
    fixture: dict[str, Any],
    flexagent_dispatch: Callable[[dict[str, Any]], Any],
) -> Any:
    """Reject at the first stage whose cumulative latency exceeds budget.

    The callback is the side-effect boundary. It is called only if the entire
    serial-additive pipeline passes the budget check.
    """
    budget = fixture["budget_ps"]
    total = 0
    for stage in fixture["stages"]:
        total += stage["latency_ps"]
        if total > budget:
            raise BudgetRejected(stage["name"], total, budget)
    return flexagent_dispatch(fixture)
