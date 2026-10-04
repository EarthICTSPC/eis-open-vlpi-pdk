#!/usr/bin/env python3
"""RU-001-PVR-001 pre-physics gate test."""

from pathlib import Path
import sys
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]

def load(path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)

def main():
    schema = ROOT / "schema/verification/pvr.schema.yaml"
    instance = ROOT / "verification/PVR/RU-001-PVR-001.yaml"
    errors = sorted(Draft202012Validator(load(schema)).iter_errors(load(instance)), key=lambda e: list(e.path))
    assert not errors, "\n".join(f"{list(e.path)}: {e.message}" for e in errors)
    pvr = load(instance)["pvr"]

    refs = [
        pvr["subject"]["ruRef"],
        pvr["subject"]["contractRef"],
        pvr["subject"]["designContextRef"],
        *[x["ref"] for x in pvr["inputs"]],
        *[x["evidenceRef"] for x in pvr["gates"] if "evidenceRef" in x],
    ]
    for ref in refs:
        assert (ROOT / ref.split("#", 1)[0]).is_file(), f"Unresolved reference: {ref}"

    assert pvr["identity"]["gateType"] == "pre-physics-physical-realization"
    assert pvr["evidenceBoundary"]["currentStatus"] == "specified"
    assert pvr["evidenceBoundary"]["physicsNotRun"] is True
    assert pvr["evidenceBoundary"]["fabricationNotRun"] is True
    assert pvr["evidenceBoundary"]["measurementNotRun"] is True
    assert pvr["disposition"]["status"] == "ready-for-physics"
    assert pvr["disposition"]["nextGate"] == "RU-001-EM-001"
    assert pvr["orchestration"]["orchestrator"] == "EURIA"
    assert pvr["orchestration"]["humanApprovalRequired"] is True
    assert pvr["gates"][-1]["status"] == "not-run"

    print("RU-001-PVR-001 PASS: pre-physics realization gate is schema-valid, reference-complete, and evidence-bounded.")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(f"RU-001-PVR-001 FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
