"""EIS-CRC-BUDGET-001 shared-fixture regression."""
from pathlib import Path
import json
import unittest

from harness.crc_budget_gate import (
    BudgetRejected,
    DEFAULT_FIXTURE,
    execute_with_budget_gate,
    load_fixture,
)

ROOT = Path(__file__).resolve().parents[1]
LEAN_SOURCE = ROOT / "formal" / "lean4" / "EISVLPI.lean"


class CRCBudget001Tests(unittest.TestCase):
    def test_fixture_arithmetic_and_kka_is_sole_budget_crossing(self):
        fixture = load_fixture()
        stages = fixture["stages"]
        total = sum(stage["latency_ps"] for stage in stages)
        self.assertEqual(total, 228)
        self.assertEqual(total, fixture["expected_total_ps"])
        self.assertEqual(total - fixture["budget_ps"], 28)
        self.assertEqual(total - fixture["budget_ps"], fixture["expected_overrun_ps"])
        cumulative = 0
        first_over = None
        for stage in stages:
            cumulative += stage["latency_ps"]
            if cumulative > fixture["budget_ps"]:
                first_over = stage["name"]
                break
        self.assertEqual(first_over, "KKA")

    def test_rejects_at_kka_before_flexagent_dispatch(self):
        fixture = load_fixture()
        calls = []

        def flexagent_dispatch(_payload):
            calls.append("dispatched")
            return {"status": "dispatched"}

        with self.assertRaises(BudgetRejected) as caught:
            execute_with_budget_gate(fixture, flexagent_dispatch)

        self.assertEqual(caught.exception.stage, "KKA")
        self.assertEqual(caught.exception.total_ps, 205)
        self.assertEqual(caught.exception.budget_ps, 200)
        self.assertIn("pipeline_latency_budget_exceeded", str(caught.exception))
        self.assertEqual(calls, [], "FlexAgent side-effect boundary must not be called")

    def test_lean_constants_match_shared_json_fixture(self):
        fixture = load_fixture()
        source = LEAN_SOURCE.read_text(encoding="utf-8")
        # Guard against drift between the fixture consumed by Python and the
        # concrete Lean theorem inputs. Lean then proves the concrete values.
        expected_list = "[" + ", ".join(str(s["latency_ps"]) for s in fixture["stages"]) + "]"
        self.assertIn(f"def budget001StageLatencies : List Picoseconds := {expected_list}", source)
        self.assertIn(f"def budget001Limit : Picoseconds := {fixture['budget_ps']}", source)
        self.assertEqual(fixture["timing_model"], "serial_additive")
        self.assertFalse(fixture["physical_validation"])


if __name__ == "__main__":
    unittest.main()
