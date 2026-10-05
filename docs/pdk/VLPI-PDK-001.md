# VLPI-PDK-001 — Cross-PDK RU Realization Matrix

**Project:** Earth ICT, SPC (EIS)  
**Milestone:** VLPI-PDK-001  
**Status:** Experimental specification + executable reference/mock experiment  
**Depends on:** VLPI-PLATFORM-002  
**Date:** 2026-10-05

## Purpose

VLPI-PDK-001 is the next major EIS experiment after VLPI-PLATFORM-002.

Its purpose is to determine what a VLPI-compatible photonic PDK must actually provide before EIS writes substantial compiler machinery.

> **EIS is not building an open photonic PDK merely to reproduce conventional PIC design. EIS is building an open, RU-native VLPI PDK as an executable reference model for exploring the physical design space of scalable photonic computation—from Replicable Unit to wafer and beyond.**

The experiment therefore applies the **same RU-001 information model and contract** to multiple PDK environments and records which requirements each environment can satisfy.

## Research question

Can one contract-governed Replicable Unit be instantiated, composed, verified, and scaled through a common VLPI PDK interface without silently changing the physical computation?

The experiment separates:

1. information-model compatibility;
2. physical-realization capability;
3. verification capability;
4. wafer-scale composition capability; and
5. evidence availability.

A PDK that fails a VLPI requirement is not thereby a bad PDK. It is **incompatible with the tested VLPI contract or design requirement**.

## Experimental environments

### A — Open-PDK control

A real open photonic PDK is represented as an external control environment. The initial repository fixture records the expected adapter boundary but does not claim that the external PDK has been installed or executed.

This keeps the experiment reproducible without embedding a third-party PDK.

### B — EIS Reference VLPI PDK

An executable open reference model representing the minimum RU-native capabilities EIS currently proposes to test.

This is a reference model, not a foundry process claim.

### C — Deliberately constrained mock PDKs

Deterministic negative controls are included to prove that the harness can detect distinct incompatibilities:

- state-boundary incompatibility;
- thermal-model insufficiency;
- topology/wafer-density incompatibility.

## Controlled input

The controlled computational object is:

- VLPI-IR RU-001 program;
- RU-001 definition;
- RU-001 Contract;
- RU-001 DesignContext;
- RU-001 Evidence policy.

The experiment must not rewrite the RU to fit a PDK.

## PDK capability dimensions

The initial compatibility dimensions are:

- RU instantiation;
- optical state representation;
- physical transformation;
- state-boundary support;
- regeneration;
- PDR readiness;
- PCT readiness;
- PTV readiness;
- thermal modeling;
- wafer-scale composition;
- evidence generation/provenance.

These dimensions are intentionally broader than conventional component-library compatibility.

## Experimental procedure

For each environment:

1. Load the identical VLPI-IR program.
2. Resolve the identical RU, Contract, and DesignContext.
3. Load the PDK capability declaration.
4. Evaluate required capabilities without modifying the RU.
5. Record each gate as pass, fail, or not-run.
6. Classify every failure by dimension.
7. Emit a machine-readable compatibility result.
8. Preserve provenance.
9. Do not promote a capability result into physical validation.

The EIS Reference and mock environments are executable in this repository.

The external open-PDK control remains explicitly **not-run** until its lawful local toolchain is installed and exercised.

## What this experiment can establish

It can establish:

- whether the VLPI information model can express PDK capabilities;
- whether one RU can be evaluated against multiple PDK capability profiles;
- whether deliberate incompatibilities are detected;
- whether failure reasons are machine-readable;
- which compiler operations appear to be required by the physical model.

## What it cannot establish

It does not establish:

- fabrication success;
- foundry acceptance;
- electromagnetic performance;
- measured device performance;
- PVR PASS;
- BIST PASS;
- compatibility with a commercial foundry;
- suitability of any external PDK for EIS hardware.

Those require domain-specific evidence.

## Compiler hold point

Substantial compiler implementation is intentionally held until VLPI-PDK-001 produces its compatibility matrix.

The compiler should be derived from observed requirements such as:

- instantiate RU;
- preserve physical state;
- compose transformations;
- enforce state boundaries;
- select a compatible technology context;
- tile/compose at wafer scale;
- verify physical constraints;
- emit evidence.

If the experiment demonstrates that a proposed compiler abstraction is wrong, EIS should change the abstraction rather than encode the wrong assumption.

## Success criterion

VLPI-PDK-001 succeeds as an information/architecture experiment when the same RU produces:

- a successful realization against the EIS Reference PDK;
- deterministic, correctly classified failures against the hostile mocks; and
- an explicit **not-run** status for any external PDK not actually executed.

The result is a compatibility matrix, not a claim that the reference PDK is fabrication-ready.

## Next decision

Only after reviewing the matrix should EIS freeze the next compiler/runtime requirements.

The immediate downstream milestone is therefore:

**VLPI-PDK-002 — RU-native reference PDK instantiation and physical-layout model.**

Compiler work remains subordinate to the PDK experiment.
