#!/usr/bin/env python3
"""GitHub2Agent-002: schema conformance and evidence-boundary test."""

from pathlib import Path
import sys

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]

SCHEMA_FIXTURES = {
    ROOT / "schema" / "ru" / "ru.schema.yaml": ROOT / "examples" / "github2agent-001" / "tiny-ru.yaml",
    ROOT / "schema" / "contract" / "contract.schema.yaml": ROOT / "examples" / "github2agent-001" / "tiny-contract.yaml",
    ROOT / "schema" / "design-context" / "design-context.schema.yaml": ROOT / "examples" / "github2agent-001" / "tiny-design-context.yaml",
    ROOT / "schema" / "evidence" / "evidence.schema.yaml": ROOT / "examples" / "github2agent-001" / "tiny-evidence.yaml",
}

FIXTURE_ROOTS = {
    "ru": ROOT / "examples" / "github2agent-001" / "tiny-ru.yaml",
    "contract": ROOT / "examples" / "github2agent-001" / "tiny-contract.yaml",
    "design_context": ROOT / "examples" / "github2agent-001" / "tiny-design-context.yaml",
    "evidence": ROOT / "examples" / "github2agent-001" / "tiny-evidence.yaml",
}


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def validate_instance(schema_path: Path, fixture_path: Path):
    schema = load_yaml(schema_path)
    instance = load_yaml(fixture_path)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    assert not errors, "\n".join(
        f"{fixture_path}: {'.'.join(map(str, error.path))}: {error.message}"
        for error in errors
    )
    return instance


def assert_file_ref(ref: str):
    target = ROOT / ref
    assert target.is_file(), f"Unresolved repository reference: {ref}"


def main():
    instances = {
        key: validate_instance(schema, fixture)
        for schema, fixture in SCHEMA_FIXTURES.items()
        for key in [fixture.stem]
    }

    ru = instances["tiny-ru"]
    contract = instances["tiny-contract"]
    context = instances["tiny-design-context"]
    evidence = instances["tiny-evidence"]

    ru_obj = ru["replicableUnit"]
    contract_obj = contract["contract"]
    context_obj = context["designContext"]
    evidence_obj = evidence["evidence"]

    assert ru_obj["transformation"]["contractRef"] == FIXTURE_ROOTS["contract"].relative_to(ROOT).as_posix()
    assert ru_obj["verification"]["contractRef"] == FIXTURE_ROOTS["contract"].relative_to(ROOT).as_posix()
    assert ru_obj["verification"]["evidenceRefs"] == [FIXTURE_ROOTS["evidence"].relative_to(ROOT).as_posix()]
    assert contract_obj["identity"]["ruRef"] == FIXTURE_ROOTS["ru"].relative_to(ROOT).as_posix()
    assert context_obj["interfaces"]["electroPhotonic"]["contractRef"] == FIXTURE_ROOTS["contract"].relative_to(ROOT).as_posix()
    assert evidence_obj["subject"]["ruRef"] == FIXTURE_ROOTS["ru"].relative_to(ROOT).as_posix()
    assert evidence_obj["subject"]["contractRef"] == FIXTURE_ROOTS["contract"].relative_to(ROOT).as_posix()
    assert evidence_obj["subject"]["designContextRef"] == FIXTURE_ROOTS["design_context"].relative_to(ROOT).as_posix()
    assert context_obj["verification"]["evidenceRefs"] == [FIXTURE_ROOTS["evidence"].relative_to(ROOT).as_posix()]

    for ref in [
        ru_obj["transformation"]["contractRef"],
        *ru_obj["verification"]["evidenceRefs"],
        evidence_obj["subject"]["designContextRef"],
        context_obj["interfaces"]["electroPhotonic"]["contractRef"],
    ]:
        assert_file_ref(ref)

    assert ru_obj["verification"]["status"] == "specified"
    assert contract_obj["identity"]["status"] == "specified"
    assert context_obj["verification"]["status"] == "specified"
    assert evidence_obj["status"] == "specified"
    assert evidence_obj["result"]["outcome"] == "not-run"
    assert context_obj["verification"]["pdrRef"] == "not-run"
    assert context_obj["verification"]["pctRef"] == "not-run"
    assert context_obj["verification"]["ptvRef"] == "not-run"
    assert context_obj["verification"]["bistRef"] == "not-run"
    assert context_obj["verification"]["foundryReview"] == "not-requested"

    forbidden_terms = ("fabricated", "measured performance", "PVR PASS", "BIST PASS", "foundry accepted")
    fixture_text = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in FIXTURE_ROOTS.values()
    )
    for term in forbidden_terms:
        assert term.lower() not in fixture_text, f"Evidence-boundary violation: {term}"

    print("GitHub2Agent-002 PASS: schema-conformant, references resolved, evidence boundary preserved.")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(f"GitHub2Agent-002 FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
