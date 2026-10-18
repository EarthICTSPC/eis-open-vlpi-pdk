# EIS-REBOOT-001 — Useful-Task, Abstraction, and Evidence Charter

**Status:** Draft for review  
**Owner:** Earth ICT, SPC (EIS) Architecture  
**Purpose:** Establish a bounded, evidence-controlled first cycle for the EIS LLM reboot before photonic simulation, fabrication, or joint MCP execution.

## 1. Mission

Establish an open, reproducible route from a useful computational task to efficient physical computation.

The long-term metric is:

> **Energy per accepted useful transformation at a defined quality and latency, with transparent thermal and lifecycle accounting.**

Peak optical operations per second alone is not a sufficient metric.

## 2. Scope of the first cycle

The first cycle is a **software model-abstraction experiment**. It does not claim a photonic result, silicon result, or full-scale LLM result.

In scope:
- one small language-model task;
- matched comparison of attention/operator abstractions;
- a formal contract for admissibility;
- reproducible software evidence;
- a conductor-managed evidence ledger.

Out of scope until later gates:
- FlexCompute/FlexAgent simulation;
- PIC/VLPI layout;
- VLSI controller design;
- fabrication;
- claims of physically demonstrated cool photonic computation.

## 3. Definitions

| Term | Meaning |
|---|---|
| **VLPI** | Very-large-scale photonic integration / photonic computational substrate |
| **VLSI** | Electronic control, memory, conversion, clocking, I/O, and package boundary |
| **EIS Conductor** | Shared authority for candidate identity, budgets, permissions, experiment state, evidence ledger, and stop conditions |
| **Formal lane** | Lean 4 specifications and proof obligations, potentially authored with agent assistance |
| **Physical lane** | Authorized simulation and, later, measurement |
| **Evidence gate** | Gate that classifies and accepts/rejects evidence |
| **Useful transformation** | A defined task output accepted under a fixed quality and workload boundary |

## 4. Evidence classes

Every claim must carry one label:

- **E0 — Assumed:** stated assumption, not tested.
- **E1 — Formal:** checked against a Lean 4 contract.
- **E2 — Software test:** reproducible code/test result.
- **E3 — Simulated:** authorized simulator output, with simulator and configuration pinned.
- **E4 — Measured:** physical measurement with instrument and calibration provenance.
- **E5 — Foundry:** fabrication/process evidence.

Agents may propose. They may not certify. Lean 4 establishes properties of a formal model, not of the physical world. A simulator does not certify its own accuracy. Evidence levels cannot be upgraded by wording, consensus, or an agent's confidence.

## 5. First useful task

**Task:** fixed next-token prediction on a bounded language-modeling dataset.

Initial candidate dataset: a fixed, hashed slice of TinyStories or an equivalent small-text corpus.

- **Context length:** 128 tokens.
- **Primary quality metric:** validation bits-per-token / perplexity.
- **Secondary metric:** top-1 next-token accuracy.
- **Workload:** fixed inference batch sizes and token counts; fixed evaluation split.
- **Data controls:** commit dataset provenance, exact slice manifest/hash, tokenizer revision/hash, and split hashes before execution.

The first accepted useful transformation is a next-token prediction evaluated under this fixed boundary. This is deliberately narrow; it is not a claim of general language understanding.

## 6. First abstraction hypothesis

The first bounded experiment is **EIS-SOFTMAX-001**: compare conventional softmax attention, sigmoid attention, and a precisely specified KKA-style interference-native attention operator under matched data, parameter, and training budgets.

The KKA-style variant remains **BLOCKED** until its exact mathematical operation, input/output semantics, assumptions, and finite-channel/error model are documented and made precise enough to formalize. The paper's physical results must not be assumed to transfer to EIS's target SiN/TFLN platform.

An independent alternative may be added only if its contract and budget are committed before the run.

## 7. Formal admissibility contract

Before any comparison, the candidate operator must have a Lean 4-checkable contract covering at least:

- input/output shapes and dtypes;
- causal-mask behavior and absence of future-token leakage;
- finite outputs under declared input bounds;
- explicit definition of the candidate operation;
- parameter-count accounting and the permitted matching tolerance;
- determinism under a fixed seed where applicable;
- state-boundary and conversion behavior;
- numerical tolerance and metric units.

A successful proof establishes a property of the formal model. It does not establish simulator accuracy, physical feasibility, energy efficiency, or useful language quality. Python and any later Rust implementation must be tested against the same contract and shared conformance vectors.

## 8. Conductor rules

The EIS Conductor must enforce:

- versioned candidate identity and immutable source revision;
- data, tokenizer, and split hashes;
- fixed seeds and hyperparameters;
- budget ceiling;
- job/run IDs and status reconciliation;
- evidence provenance, uncertainty, and artifact hashes;
- stop conditions and explicit BLOCKED outcomes;
- prohibition on unlabeled or evidence-level-upgraded claims.

Human approval remains required for credentials, new tool permissions, budget increases, unknown PDKs, and changes to the experimental contract.

## 9. Success criteria for this charter cycle

The cycle succeeds if it produces a traceable, reproducible comparison and a clear evidence-backed decision: **accept, reject, refine, or request the next bounded experiment**.

The photonic candidate does not need to win. A well-documented rejection is a valid result.

## 10. Non-claims

This charter does not claim:
- that photonic computation has lower total energy;
- that KKA-style attention is superior;
- that a simulator result is a measured result;
- that a small language-model task demonstrates full LLM capability;
- that the EIS loop has already produced a physical device.

## 11. Initial gate

**G0 — Charter and controls.** Before training begins, record acceptance of this charter, dataset/task/metrics, the approved compute budget, and the owner responsible for formalizing the KKA-style operator. If any is missing, the experiment remains BLOCKED.
