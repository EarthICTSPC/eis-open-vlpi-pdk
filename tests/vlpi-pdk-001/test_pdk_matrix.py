#!/usr/bin/env python3
"""VLPI-PDK-001: executable cross-PDK RU realization matrix."""

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT = ROOT / "verification" / "pdk" / "VLPI-PDK-001.yaml"
PDK_DIR = ROOT / "examples" / "vlpi-pdk-001" / "pdks"

CAPABILITY_KEYS = [
    "ruInstantiation", "opticalState", "physicalTransformation",
    "stateBoundary", "regeneration", "thermalModel", "waferComposition"
]

def load(path):
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def evaluate(pdk):
    c = pdk["pdk"]["capabilities"]
    failures = []
    for key in CAPABILITY_KEYS:
        if not c.get(key, False):
            failures.append(key)
    if not c.get("pdr", False):
        failures.append("PDR")
    if not c.get("pct", False):
        failures.append("PCT")
    if not c.get("ptv", False):
        failures.append("PTV")
    return failures

def main():
    exp = load(EXPERIMENT)
    for env in exp["experiment"]["environments"]:
        pdk = load(ROOT / env["fixture"])
        failures = evaluate(pdk)

        if env["id"] == "OPEN-PDK-CONTROL-NOT-RUN":
            assert pdk["pdk"]["execution"]["status"] == "not-run"
            assert env["expectedDisposition"] == "not-run"
            continue

        expected = env["expectedDisposition"]
        if expected == "compatible":
            assert failures == [], f"Reference PDK unexpectedly failed: {failures}"
        else:
            assert failures, f"Hostile mock did not fail: {env['id']}"
            assert env["expectedFailureDimension"] in failures, (
                f"Expected {env['expectedFailureDimension']} in {failures}"
            )

    results = []
    for env in exp["experiment"]["environments"]:
        pdk = load(ROOT / env["fixture"])
        failures = evaluate(pdk)
        disposition = "not-run" if env["expectedDisposition"] == "not-run" else (
            "compatible" if not failures else "incompatible"
        )
        results.append((env["id"], disposition, failures))

    print("VLPI-PDK-001 PASS: cross-PDK capability matrix executed.")
    for row in results:
        print(f"  {row[0]}: {row[1]} {row[2]}")

if __name__ == "__main__":
    main()
