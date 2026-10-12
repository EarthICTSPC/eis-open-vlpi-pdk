"""EIS-CRC-BUDGET-001 shared-fixture regression."""
from pathlib import Path
import subprocess
import sys
import unittest

from harness.crc_budget_gate import (
    BudgetRejected,
    execute_with_budget_gate,
    load_fixture,
)

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "scripts" / "gen_lean_fixture.py"
LEAN_FIXTURE = ROOT / "formal" / "lean4" / "EISVLPI" / "Fixtures" / "EIS_CRC_BUDGET_001.lean"


class CRCBudget001Tests(unittest.TestCase):
    def test_fixture_arithmetic_and_kka_is_first_budget_crossing(self):
        fixture = load_fixture()
        stages = fixture["stages"]
        total = sum(stage["latency_ps"] for stage in stages)
        self.assertEqual(total, fixture["expected_total_ps"])
        self.assertEqual(total, 228)
        self.assertEqual(total - fixture["budget_ps"], fixture["expected_overrun_ps"])
        self.assertEqual(total - fixture["budget_ps"], 28)

        cumulative = 0
        first_over = None
        for stage in stages:
            cumulative += stage["latency_ps"]
            if cumulative > fixture["budget_ps"]:
                first_over = (stage["name"], cumulative)
                break
        self.assertEqual(first_over, ("KKA", 205))
        self.assertEqual(fixture["expected_rejection_stage"], "KKA")
        self.assertEqual(fixture["expected_rejection_phase"], "pre_dispatch")

    def test_rejects_at_kka_before_any_dispatch_side_effect(self):
        fixture = load_fixture()
        side_effects = {
            "flexagent_dispatched": False,
            "pdk_netlist_generated": False,
            "simulation_started": False,
            "fabrication_attempted": False,
        }

        def flexagent_dispatch(_payload):
            side_effects["flexagent_dispatched"] = True
            return {"status": "dispatched"}

        with self.assertRaises(BudgetRejected) as caught:
            execute_with_budget_gate(fixture, flexagent_dispatch)

        self.assertEqual(caught.exception.stage, "KKA")
        self.assertEqual(caught.exception.cumulative_ps, 205)
        self.assertEqual(caught.exception.budget_ps, 200)
        self.assertIn("pipeline_latency_budget_exceeded", str(caught.exception))
        self.assertEqual(side_effects, fixture["expected_side_effects"])
        self.assertFalse(side_effects["pdk_netlist_generated"])
        self.assertFalse(side_effects["simulation_started"])
        self.assertFalse(side_effects["fabrication_attempted"])

    def test_generated_lean_module_is_current(self):
        result = subprocess.run(
            [sys.executable, str(GENERATOR), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_lean_fixture_contains_stagewise_first_exceed_proofs(self):
        source = LEAN_FIXTURE.read_text(encoding="utf-8")
        self.assertIn("theorem cumulative_before_kka_within_budget", source)
        self.assertIn("theorem cumulative_at_kka_exceeds_budget", source)
        self.assertIn('theorem rejection_stage_is_kka : rejectionStage = "KKA"', source)
        self.assertIn("theorem total_matches_fixture", source)


if __name__ == "__main__":
    unittest.main()
