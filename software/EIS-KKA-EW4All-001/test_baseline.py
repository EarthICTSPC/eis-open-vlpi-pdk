"""Contract tests for EIS-KKA-EW4All-001 baseline harness."""
import unittest
import pandas as pd

from baseline import (
    chronological_event_split,
    evaluate_binary,
    persistence_probability,
    validate_frame,
)


class BaselineContractTests(unittest.TestCase):
    def test_feature_allowlist_rejects_future_columns(self):
        frame = pd.DataFrame({
            "issue_time": ["2019-01-01T00:00:00Z"],
            "event_id": ["storm-a"],
            "target": [1],
            "future_rain": [12.0],
        })
        with self.assertRaisesRegex(ValueError, "leakage"):
            validate_frame(frame, ["future_rain"])

    def test_chronological_split_excludes_cross_boundary_event(self):
        frame = pd.DataFrame({
            "issue_time": [
                "2019-01-01T00:00:00Z",
                "2019-06-01T00:00:00Z",
                "2020-06-01T00:00:00Z",
                "2021-06-01T00:00:00Z",
                "2022-06-01T00:00:00Z",
                "2023-06-01T00:00:00Z",
            ],
            "event_id": ["train", "crossing", "crossing", "valid", "test", "test-later"],
            "target": [0, 1, 1, 0, 1, 0],
            "rain_60m": [0.0, 10.0, 10.0, 1.0, 15.0, 0.0],
        })
        train, valid, test = chronological_event_split(
            frame, "2020-01-01T00:00:00Z", "2022-01-01T00:00:00Z"
        )
        self.assertEqual(set(train.event_id), {"train"})
        self.assertEqual(set(valid.event_id), {"valid"})
        self.assertEqual(set(test.event_id), {"test", "test-later"})

    def test_persistence_is_explicit_thresholded_state(self):
        frame = pd.DataFrame({"rain_60m": [0.0, 9.9, 10.0, 14.0]})
        got = persistence_probability(frame, "rain_60m", 10.0)
        self.assertEqual(got.tolist(), [0.0, 0.0, 1.0, 1.0])

    def test_metrics_report_false_alarm_ratio_and_csi(self):
        result = evaluate_binary([1, 0, 1, 0], [0.9, 0.8, 0.4, 0.1])
        self.assertEqual(result["confusion"], {"tn": 1, "fp": 1, "fn": 1, "tp": 1})
        self.assertEqual(result["csi_at_0_5"], 1 / 3)
        self.assertEqual(result["false_alarm_ratio_at_0_5"], 0.5)


if __name__ == "__main__":
    unittest.main()
