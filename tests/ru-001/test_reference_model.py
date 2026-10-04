#!/usr/bin/env python3
"""RU-001 reference information-model and evidence-boundary test."""

from pathlib import Path
import sys
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = {
    "ru": (ROOT / "schema/ru/ru.schema.yaml", ROOT / "ru/RU-001/ru.yaml"),
    "contract": (ROOT / "schema/contract/contract.schema.yaml", ROOT / "ru/RU-001/contract.yaml"),
    "context": (ROOT / "schema/design-context/design-context.schema.yaml", ROOT / "ru/RU-001/design-context.yaml"),
    "evidence": (ROOT / "schema/evidence/evidence.schema.yaml", ROOT / "ru/RU-001/evidence.yaml"),
}

def load(path):
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)

def validate(schema_path, instance_path):
    schema = load(schema_path)
    instance = load(instance_path)
    errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda e: list(e.path))
    assert not errors, "\n".join(f"{instance_path}: {list(e.path)}: {e.message}" for e in errors)
    return instance

def main():
    x = {k: validate(*v) for k, v in SCHEMAS.items()}
    ru = x["ru"]["replicableUnit"]
    contract = x["contract"]["contract"]
    context = x["context"]["designContext"]
    evidence = x["evidence"]["evidence"]

    refs = [
        ru["transformation"]["contractRef"],
        ru["verification"]["contractRef"],
        *ru["verification"]["evidenceRefs"],
        contract["identity"]["ruRef"],
        *contract["evidencePolicy"]["requiredArtifacts"],
        context["interfaces"]["electroPhotonic"]["contractRef"],
        *context["verification"]["evidenceRefs"],
        evidence["subject"]["artifactRef"],
        evidence["subject"]["ruRef"],
        evidence["subject"]["contractRef"],
        evidence["subject"]["designContextRef"],
    ]
    for ref in refs:
        assert (ROOT / ref.split("#", 1)[0]).is_file(), f"Unresolved reference: {ref}"

    assert ru["identity"]["name"] == "RU-001"
    assert ru["verification"]["status"] == "specified"
    assert ru["metadata"]["evidenceStatus"] == "specified"
    assert contract["identity"]["status"] == "specified"
    assert context["verification"]["status"] == "specified"
    assert evidence["status"] == "specified"
    assert evidence["result"]["outcome"] == "not-run"

    assert context["technologies"]["photonic"]["pdkIdentity"] == "LIGENTEC_AN800_TFLN"
    assert context["technologies"]["photonic"]["controlled"] is True
    assert context["verification"]["pdrRef"] == "not-run"
    assert context["verification"]["pctRef"] == "not-run"
    assert context["verification"]["ptvRef"] == "not-run"
    assert context["verification"]["bistRef"] == "not-run"
    assert context["verification"]["foundryReview"] == "not-requested"

    assert ru["transformation"]["mapping"]
    assert ru["transformation"]["physicalMechanism"]
    assert contract["stateBoundary"]["measurementRequired"] is True
    assert contract["evidencePolicy"]["minimumEvidence"] == ["specification"]

    print("RU-001 PASS: four-schema traversal, reference integrity, and evidence boundary preserved.")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(f"RU-001 FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
