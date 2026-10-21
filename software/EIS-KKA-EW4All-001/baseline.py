"""EIS-KKA-EW4All-001 software baseline.

Input is a prepared CSV with one row per grid cell, issue time and horizon.
This module does not download or fabricate meteorological data.
Requires pandas, numpy and scikit-learn.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Sequence

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score, brier_score_loss, confusion_matrix,
    precision_score, recall_score,
)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

REQUIRED_COLUMNS = {"issue_time", "event_id", "target"}
DEFAULT_FEATURES = [
    "rain_15m", "rain_30m", "rain_60m", "rain_180m",
    "rain_rate_delta_30m", "antecedent_rain_24h",
]
FORBIDDEN_TOKENS = ("target", "label", "future", "event_outcome", "flood_report")


def validate_frame(frame: pd.DataFrame, features: Sequence[str]) -> None:
    missing = (REQUIRED_COLUMNS | set(features)) - set(frame.columns)
    if missing:
        raise ValueError(f"missing required columns: {sorted(missing)}")
    if not features:
        raise ValueError("at least one pre-registered feature is required")
    suspicious = [c for c in features if any(t in c.lower() for t in FORBIDDEN_TOKENS)]
    if suspicious:
        raise ValueError(f"feature allowlist includes suspicious leakage columns: {suspicious}")
    if frame["issue_time"].isna().any() or frame["event_id"].isna().any():
        raise ValueError("issue_time and event_id must be non-null")
    if frame["target"].isna().any():
        raise ValueError("target must be labeled for the selected task")
    values = set(frame["target"].unique().tolist())
    if not values.issubset({0, 1, False, True}):
        raise ValueError(f"target must be binary 0/1, got {sorted(map(str, values))}")


def chronological_event_split(frame: pd.DataFrame, train_end: str, validation_end: str):
    """Chronological split with event leakage guard.

    Events crossing a cutoff are excluded from every split. Cutoffs are ISO
    timestamps. Event identity should correspond to a storm episode, not a row.
    """
    data = frame.copy()
    data["issue_time"] = pd.to_datetime(data["issue_time"], utc=True, errors="raise")
    t1, t2 = pd.Timestamp(train_end), pd.Timestamp(validation_end)
    t1 = t1.tz_localize("UTC") if t1.tzinfo is None else t1.tz_convert("UTC")
    t2 = t2.tz_localize("UTC") if t2.tzinfo is None else t2.tz_convert("UTC")
    if not t1 < t2:
        raise ValueError("train_end must be earlier than validation_end")
    raw_train = data[data.issue_time < t1]
    raw_valid = data[(data.issue_time >= t1) & (data.issue_time < t2)]
    raw_test = data[data.issue_time >= t2]
    sets = [set(part.event_id) for part in (raw_train, raw_valid, raw_test)]
    overlap = (sets[0] & sets[1]) | (sets[0] & sets[2]) | (sets[1] & sets[2])
    if overlap:
        raw_train = raw_train[~raw_train.event_id.isin(overlap)]
        raw_valid = raw_valid[~raw_valid.event_id.isin(overlap)]
        raw_test = raw_test[~raw_test.event_id.isin(overlap)]
    if any(part.empty for part in (raw_train, raw_valid, raw_test)):
        raise ValueError("a split is empty after event-leakage exclusion")
    return raw_train, raw_valid, raw_test


def build_models(random_state: int = 2026) -> dict:
    return {
        "logistic_regression": make_pipeline(
            SimpleImputer(strategy="median"), StandardScaler(),
            LogisticRegression(max_iter=2000, class_weight="balanced", random_state=random_state),
        ),
        "hist_gradient_boosting": make_pipeline(
            SimpleImputer(strategy="median"),
            HistGradientBoostingClassifier(max_iter=150, learning_rate=0.08, random_state=random_state),
        ),
    }


def evaluate_binary(y_true, probability) -> dict:
    y_true = np.asarray(y_true, dtype=int)
    probability = np.asarray(probability, dtype=float)
    predicted = probability >= 0.5
    tn, fp, fn, tp = confusion_matrix(y_true, predicted, labels=[0, 1]).ravel()
    return {
        "n": int(len(y_true)),
        "prevalence": float(np.mean(y_true)),
        "pod_recall_at_0_5": float(recall_score(y_true, predicted, zero_division=0)),
        "precision_at_0_5": float(precision_score(y_true, predicted, zero_division=0)),
        "false_alarm_ratio_at_0_5": float(fp / (fp + tp)) if (fp + tp) else None,
        "csi_at_0_5": float(tp / (tp + fp + fn)) if (tp + fp + fn) else None,
        "brier_score": float(brier_score_loss(y_true, probability)),
        "pr_auc": float(average_precision_score(y_true, probability)) if len(set(y_true)) > 1 else None,
        "confusion": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
    }


def persistence_probability(frame: pd.DataFrame, feature: str, threshold: float) -> np.ndarray:
    """Simple transparent persistence/event-state baseline.

    The feature and threshold must have compatible units and be frozen in the
    experiment manifest. This is a deterministic alert probability (0 or 1),
    not a calibrated probabilistic forecast.
    """
    if feature not in frame.columns:
        raise ValueError(f"persistence feature not found: {feature}")
    values = pd.to_numeric(frame[feature], errors="coerce")
    if values.isna().any():
        raise ValueError(f"persistence feature {feature} contains missing/non-numeric values")
    return (values.to_numpy(dtype=float) >= threshold).astype(float)


def run_baselines(
    csv_path: str,
    output_path: str,
    features: Sequence[str],
    persistence_feature: str,
    persistence_threshold: float,
) -> dict:
    frame = pd.read_csv(csv_path)
    validate_frame(frame, features)
    train, validation, test = chronological_event_split(
        frame, train_end="2020-01-01T00:00:00Z", validation_end="2022-01-01T00:00:00Z"
    )
    if persistence_feature not in frame.columns:
        raise ValueError(f"persistence feature not found: {persistence_feature}")
    results = {
        "artifact": "EIS-KKA-EW4All-001",
        "spec_version": "0.1.0",
        "status": "software_baseline_run",
        "input_csv": str(Path(csv_path)),
        "features": list(features),
        "persistence": {
            "feature": persistence_feature,
            "threshold": persistence_threshold,
            "threshold_units": "must match the declared units of the persistence feature",
            "probability_interpretation": "deterministic 0/1 event-state baseline; not calibrated",
        },
        "split_rows": {"train": len(train), "validation": len(validation), "test": len(test)},
        "split_events": {"train": int(train.event_id.nunique()),
                         "validation": int(validation.event_id.nunique()),
                         "test": int(test.event_id.nunique())},
        "models": {},
        "claim_boundary": (
            "Metrics apply only to this supplied CSV and split. They do not establish "
            "operational warning readiness or photonic energy savings."
        ),
    }
    val_persistence = persistence_probability(validation, persistence_feature, persistence_threshold)
    test_persistence = persistence_probability(test, persistence_feature, persistence_threshold)
    results["models"]["persistence"] = {
        "validation": evaluate_binary(validation.target, val_persistence),
        "test": evaluate_binary(test.target, test_persistence),
        "threshold_note": "Feature threshold is supplied by the operator and must match label/feature units; not a calibrated probability.",
    }
    for name, model in build_models().items():
        model.fit(train[list(features)], train.target.astype(int))
        val_prob = model.predict_proba(validation[list(features)])[:, 1]
        test_prob = model.predict_proba(test[list(features)])[:, 1]
        results["models"][name] = {
            "validation": evaluate_binary(validation.target, val_prob),
            "test": evaluate_binary(test.target, test_prob),
            "threshold_note": "0.5 is diagnostic only; alert threshold must be frozen on validation data.",
        }
    Path(output_path).write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Prepared feature/label CSV; no raw data are downloaded.")
    parser.add_argument("--out", default="baseline-results.json")
    parser.add_argument("--features", nargs="+", default=DEFAULT_FEATURES)
    parser.add_argument("--persistence-feature", default="rain_60m")
    parser.add_argument("--persistence-threshold", type=float, required=True,
                        help="Threshold in the same units as --persistence-feature; freeze in manifest.")
    args = parser.parse_args()
    print(json.dumps(run_baselines(
        args.csv, args.out, args.features,
        args.persistence_feature, args.persistence_threshold
    ), indent=2))


if __name__ == "__main__":
    main()
