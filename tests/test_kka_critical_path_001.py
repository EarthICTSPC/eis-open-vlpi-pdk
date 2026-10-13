import json
import unittest
from pathlib import Path
from experiments.kka_critical_path import analyze

MODEL_PATH = Path(__file__).parents[1] / "experiments" / "EIS-KKA-CRITICAL-PATH-001.json"


class CriticalPathTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.model = json.loads(MODEL_PATH.read_text(encoding="utf-8"))

    def test_candidate_critical_path_and_budget(self):
        result = analyze(self.model)
        self.assertEqual(result["critical_path_ps"], 183)
        self.assertEqual(result["margin_ps"], 17)
        self.assertTrue(result["target_met_in_model"])
        self.assertFalse(result["physical_validation"])

    def test_parallel_lanes_overlap_after_thresholder(self):
        result = analyze(self.model)
        self.assertEqual(result["start_ps"]["kka_lane_a"], 85)
        self.assertEqual(result["start_ps"]["kka_lane_b"], 85)
        self.assertEqual(result["finish_ps"]["kka_lane_a"], 145)
        self.assertEqual(result["finish_ps"]["kka_lane_b"], 145)
        self.assertEqual(result["start_ps"]["join_route_sync"], 145)
        self.assertEqual(result["finish_ps"]["join_route_sync"], 160)

    def test_energy_and_peak_power_are_not_fabricated(self):
        result = analyze(self.model)
        self.assertFalse(result["energy_evaluable"])
        self.assertFalse(result["peak_power_evaluable"])
        self.assertTrue(result["missing_energy_tasks"])
        self.assertTrue(result["missing_power_tasks"])

    def test_cycle_is_rejected(self):
        model = json.loads(json.dumps(self.model))
        model["tasks"][0]["deps"] = ["adc"]
        with self.assertRaisesRegex(ValueError, "cycle"):
            analyze(model)


if __name__ == "__main__":
    unittest.main()
