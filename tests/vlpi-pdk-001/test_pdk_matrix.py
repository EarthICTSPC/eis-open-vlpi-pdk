#!/usr/bin/env python3
"""VLPI-PDK-001: executable cross-PDK RU realization matrix."""

from pathlib import Path
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
EXPERIMENT = ROOT / "verification" / "pdk" / "VLPI-PDK-001.yaml"
COMPAT_SCHEMA = ROOT / "schema" / "pdk" / "pdk-compatibility.schema.yaml"

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


def build_result(env, pdk, failures):
    disposition = "not-run" if env["expectedDisposition"] == "not-run" else (
        "compatible" if not failures else "incompatible"
    )
    capabilities = pdk["pdk"]["capabilities"]
    result = {
        "compatibility": {
            "identity": {
                "id": env["id"],
                "pdkId": pdk["pdk"]["id"],
                "version": pdk["pdk"]["version"],
                "class": pdk["pdk"]["class"],
            },
            "subject": {
                "ruRef": "ru/RU-001/ru.yaml",
                "contractRef": "ru/RU-001/contract.yaml",
                "irRef": "examples/vlpi-platform-002/ru001-program.yaml",
            },
            "capabilities": {
                key: "pass" if capabilities.get(key, False) else "fail"
                for key in CAPABILITY_KEYS
            },
            "gates": {
                "PDR": "pass" if capabilities.get("pdr", False) else "fail",
                "PCT": "pass" if capabilities.get("pct", False) else "fail",
                "PTV": "pass" if capabilities.get("ptv", False) else "fail",
            },
            "disposition": disposition,
            "evidence": {
                "status": "not-run" if disposition == "not-run" else "computationally-demonstrated",
                "physicalValidationRequired": True,
                "provenanceRequired": True,
                "notes": "Capability-harness result only; not fabrication, measurement, PVR PASS, BIST PASS, or foundry acceptance.",
            },
            "provenance": {
                "experiment": "VLPI-PDK-001",
                "generatedBy": "tests/vlpi-pdk-001/test_pdk_matrix.py",
            },
        }
    }
    failures_out = []
    for dimension in failures:
        failures_out.append({
            "dimension": dimension,
            "class": "capability-incompatibility",
            "reason": f"PDK capability declaration does not satisfy {dimension}.",
        })
    if failures_out:
        result["compatibility"]["failures"] = failures_out
    return result


def main():
    exp = load(EXPERIMENT)
    schema = load(COMPAT_SCHEMA)

    observed = []
    for env in exp["experiment"]["environments"]:
        pdk = load(ROOT / env["fixture"])
        failures = evaluate(pdk)

        if env["id"] == "OPEN-PDK-CONTROL-NOT-RUN":
            assert pdk["pdk"]["execution"]["status"] == "not-run"
            assert env["expectedDisposition"] == "not-run"
        elif env["expectedDisposition"] == "compatible":
            assert failures == [], f"Reference PDK unexpectedly failed: {failures}"
        else:
            assert failures, f"Hostile mock did not fail: {env['id']}"
            assert env["expectedFailureDimension"] in failures, (
                f"Expected {env['expectedFailureDimension']} in {failures}"
            )

        result = build_result(env, pdk, failures)
        errors = sorted(
            Draft202012Validator(schema).iter_errors(result),
            key=lambda e: list(e.path),
        )
        assert not errors, "\n".join(e.message for e in errors)
        observed.append((env["id"], result["compatibility"]["disposition"], failures))

    print("VLPI-PDK-001 PASS: cross-PDK capability matrix executed and result schema validated.")
    for row in observed:
        print(f"  {row[0]}: {row[1]} {row[2]}")


if __name__ == "__main__":
    main()
