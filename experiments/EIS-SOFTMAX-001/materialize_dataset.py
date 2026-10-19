#!/usr/bin/env python3
"""Materialize the pinned EIS-SOFTMAX-001 dataset inputs and emit SHA-256 hashes.

This script intentionally does not mark G0 passed: split leakage, test-set design,
model/training controls, and compute authorization require separate review.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

from huggingface_hub import hf_hub_download

REPO_ID = "alooboii/pa1-tinystories"
REVISION = "3b0e624a62a320d09c1ef9378b7e4f1b6fed6e38"
FILES = (
    "metadata.json",
    "tokenizer/tokenizer.json",
    "debug/train.bin",
    "debug/validation.bin",
)
ROOT = Path("artifacts/EIS-SOFTMAX-001/dataset")
OUT = Path("experiments/EIS-SOFTMAX-001/dataset-materialization.json")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    records = []
    for filename in FILES:
        cached = Path(
            hf_hub_download(
                repo_id=REPO_ID,
                repo_type="dataset",
                filename=filename,
                revision=REVISION,
            )
        )
        target = ROOT / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(cached.read_bytes())
        records.append({
            "path": filename,
            "materialized_path": str(target),
            "bytes": target.stat().st_size,
            "sha256": sha256_file(target),
        })

    report = {
        "experiment_id": "EIS-SOFTMAX-001",
        "source": {
            "repo_type": "dataset",
            "repo_id": REPO_ID,
            "revision": REVISION,
        },
        "materialized_at_utc": datetime.now(timezone.utc).isoformat(),
        "files": records,
        "status": "MATERIALIZED_HASHED_SPLIT_REVIEW_PENDING",
        "limitations": [
            "Hashing establishes byte identity, not dataset quality or split independence.",
            "Do not mark G0 passed until split identity/leakage and test-set policy are reviewed.",
            "This script does not authorize compute expenditure or launch training.",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
