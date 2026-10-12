"""Typed reference pre-dispatch latency gate for EIS-CRC-BUDGET-001.

This module defines a reusable gate/dispatch adapter. It is not evidence that
all production FlexAgent/FlexCompute paths are already wired through it.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Protocol

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FIXTURE = ROOT / "fixtures" / "EIS-CRC-BUDGET-001.json"


class BudgetRejected(RuntimeError):
    def __init__(self, stage: str, cumulative_ps: int, budget_ps: int):
        self.stage = stage
        self.total_ps = cumulative_ps
        self.cumulative_ps = cumulative_ps
        self.budget_ps = budget_ps
        super().__init__(
            f"pipeline_latency_budget_exceeded at {stage}: "
            f"{cumulative_ps} ps > {budget_ps} ps"
        )


class PreDispatchGate(Protocol):
    """Contract for a synchronous gate that must pass before side-effect dispatch."""

    def check(self, stages: list[dict[str, Any]], budget_ps: int) -> None:
        """Return only if accepted; raise a typed rejection otherwise."""
        ...


class SerialAdditiveBudgetGate:
    """Reject at the first stage whose cumulative integer-ps latency exceeds budget."""

    def check(self, stages: list[dict[str, Any]], budget_ps: int) -> None:
        if type(budget_ps) is not int or budget_ps < 0:
            raise ValueError("budget_ps must be a non-negative integer")
        cumulative = 0
        for stage in stages:
            latency = stage.get("latency_ps")
            if type(latency) is not int or latency < 0:
                raise ValueError(f"{stage.get('name', '<unnamed>')}: latency_ps must be a non-negative integer")
            cumulative += latency
            if cumulative > budget_ps:
                raise BudgetRejected(stage["name"], cumulative, budget_ps)


def load_fixture(path: Path = DEFAULT_FIXTURE) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def execute_with_budget_gate(
    fixture: dict[str, Any],
    flexagent_dispatch: Callable[[dict[str, Any]], Any],
    gate: PreDispatchGate | None = None,
) -> Any:
    """Gate the complete serial pipeline before invoking the dispatch callback.

    The callback is the side-effect boundary. A rejection prevents it from
    running. Production integration must route every dispatch path through
    this adapter; this repository currently tests the adapter as a reference.
    """
    (gate or SerialAdditiveBudgetGate()).check(fixture["stages"], fixture["budget_ps"])
    return flexagent_dispatch(fixture)
