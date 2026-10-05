# EIS VLPI Roadmap — Platform and PDK Sequence

**Date:** 2026-10-05

## Current sequence

1. **VLPI-PLATFORM-001** — Programming Model and Runtime Architecture.
2. **VLPI-PLATFORM-002** — VLPI-IR Schema + Cold-Start Reconstruction.
3. **VLPI-PDK-001** — Cross-PDK RU Realization Matrix.
4. **VLPI-PDK-002** — RU-native reference PDK instantiation and physical-layout model.
5. **VLPI-PDK-003** — Wafer-scale RU composition.
6. **VLPI-PDK-004** — Cross-PDK failure/compatibility matrix expansion.
7. **VLPI-PLATFORM-003** — Adversarial cold-start reconstruction hardening.
8. **VLPI-PLATFORM-004** — Field Math Primitive #001.

## Compiler hold point

Substantial compiler implementation is intentionally paused after VLPI-PLATFORM-002.

VLPI-PDK-001 is the experiment that should determine what the compiler must actually do.

The compiler must not become a software abstraction that silently reproduces conventional PIC assumptions. It should emerge from experimentally observed requirements of RU instantiation, physical-state continuity, composition, verification, wafer-scale constraints, and evidence.

## Foundational proposition

> **EIS is not building an open photonic PDK merely to reproduce conventional PIC design. EIS is building an open, RU-native VLPI PDK as an executable reference model for exploring the physical design space of scalable photonic computation—from Replicable Unit to wafer and beyond.**

The PDK is therefore treated as an executable architectural model, not merely a device library.

## Evidence discipline

A capability-harness PASS means the information model and reference capability declaration passed the experiment. It is not fabrication, measurement, PVR PASS, BIST PASS, or foundry acceptance.

External PDKs remain not-run until their lawful local execution environments are installed and tested.
