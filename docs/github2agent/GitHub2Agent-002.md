# GitHub2Agent-002: Schema Conformance and Evidence Boundary Test

## Purpose

GitHub2Agent-001 proved that a cold-start agent can conceptually traverse the tiny RU → Contract → DesignContext → Evidence graph.

It also exposed a more important failure: the four machine-readable schemas and the tiny fixture did not agree on several data types.

GitHub2Agent-002 makes that failure explicit and resolves the fixture/schema boundary before any real RU implementation is added.

## What this test establishes

This test has two separate levels of validity:

1. **Information-model validity** — each fixture instantiates its declared schema and every required cross-reference resolves.
2. **Physical/evidence validity** — the referenced physical object actually satisfies its physical contract.

GitHub2Agent-002 tests **Level 1 only**.

Passing schema conformance does **not** establish Level 2.

## Conformance corrections

The tiny fixture is brought into conformance with the current schemas without silently changing the schema contract:

- Contract state parameters are objects rather than arrays.
- Contract transformation parameters are an object rather than an array.
- Contract transformation composition is represented by the schema's declared array form.
- Constraint-reduction constraints are objects containing name, condition, and severity.
- minimumEvidence is an array using the schema's controlled vocabulary.
- Evidence provenance toolchain is an array of name/version/invocation objects.
- Evidence result.outcome is not-run, because this fixture does not report a physical experiment or physical pass/fail result.

These corrections are deliberately conservative: GitHub2Agent-002 does not infer a new physical model from the mismatch.

## Evidence boundary

The agent must preserve this distinction:

Schema conformance
        |
        v
Information-model validity
        |
        X  NOT physical proof
        |
        v
Physical/evidence validity
        |
        v
EM → PVR → fabrication → BIST → measured evidence

In particular:

- outcome: not-run means no physical result is being claimed.
- status: specified remains specified.
- A valid YAML file is not evidence that the physical object exists.
- A valid contract is not evidence that the physical object satisfies the contract.
- A passing schema test is not a PVR PASS or BIST PASS.
- Example-only technology context must not be replaced by a known foundry/PDK.
- not-run verification gates must remain unresolved.

## Reference graph under test

TINY-RU-001
  ├── transformation.contractRef ──> tiny-contract.yaml
  ├── verification.contractRef ────> tiny-contract.yaml
  └── verification.evidenceRefs ──> tiny-evidence.yaml
                                      └── subject.designContextRef
                                           └──> tiny-design-context.yaml
                                                  └── interfaces.electroPhotonic.contractRef
                                                       └──> tiny-contract.yaml

## Required machine checks

The GitHub2Agent-002 implementation must:

1. Load the four schemas.
2. Load the four fixture instances.
3. Validate each instance against its schema.
4. Resolve every file reference in the graph.
5. Confirm the RU, Contract, DesignContext, and Evidence identifiers agree.
6. Confirm all four evidence/verification statuses remain specified.
7. Confirm PDR/PCT/PTV/BIST and foundry review remain not-run / not-requested.
8. Confirm no fixture asserts measured physical performance.
9. Confirm evidence.result.outcome is not-run.
10. Report failures as information-model failures rather than silently repairing them.

## Ground-truth reconstruction

A cold-start agent should reconstruct:

> TINY-RU-001 is a specified, abstract example of a two-input physical field-combination unit. Its declared mapping is r = a - b. Its technology context is explicitly example-only. The GitHub2Agent-002 fixture is designed to test schema conformance and reference traversal only. No electromagnetic performance, fabrication, PVR acceptance, BIST result, foundry acceptance, or measured behavior is established.

## Stop condition

The agent must stop at:

**specified + schema-conformant + evidence-bound**

It may propose the next verification step, but it may not promote the object to formally verified, computationally demonstrated, experimentally demonstrated, or measured.

## Why this comes before RU-001

The information model is now a testable engineering boundary.

Only after GitHub2Agent-002 is green should the repository add a real RU implementation and ask whether the same evidence discipline survives contact with PDK-specific physical design.
