# EIS-KKA-EW4All-001 software baseline

Version 0.1.0. This is an executable baseline harness for a prepared tabular dataset, not a claim that public data were downloaded or a forecast experiment was run.

## Input CSV

Required columns:
- issue_time: ISO-8601 timestamp; timezone strongly recommended.
- event_id: stable storm/event identifier used to prevent event leakage.
- target: binary label defined by the experiment specification.
- Feature columns: default allowlist is rain_15m, rain_30m, rain_60m, rain_180m, rain_rate_delta_30m, antecedent_rain_24h.

Feature values must be computed strictly from input data available by issue_time. Preserve source product, version, availability time, spatial joins, units, and checksums in a separate manifest. Do not include future observations or label-derived fields.

## Run

Install pandas, numpy and scikit-learn in a dedicated environment, prepare the input CSV, then:

    python baseline.py --csv prepared-rainfall.csv --out baseline-results.json --persistence-threshold 10.0

The harness uses starter chronological cutoffs (training before 2020; validation 2020–2021; test 2022 onward). Before a real study, choose cutoffs after auditing coverage, freeze them in the manifest, and update the spec/version if they change. Events crossing split boundaries are excluded from all splits.

The harness reports thresholded POD/recall, precision, false-alarm ratio, CSI, Brier score, PR-AUC and event counts. The 0.5 threshold is diagnostic, not an operational alert threshold. Alert threshold selection must use training/validation only.

## Not yet implemented

- Dataset acquisition and product-specific parsers.
- Exact MRMS/IMERG product manifest and latency audit.
- Rainfall-label generation and catchment/event association.
- KKA dynamic/static/shuffled ablations, spatial-temporal model, event-level lead-time metrics and confidence intervals.
- Lean-to-Python proof of correspondence.
- Operational warning integration or photonic energy measurement.

Do not interpret this harness's existence as experimental results.

## CI

The follow-on pull request adds GitHub Actions checks for the Lean project and Python baseline contract tests. A passing workflow is required before treating either as validated.
