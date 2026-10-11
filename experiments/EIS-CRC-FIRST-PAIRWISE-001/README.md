# EIS-CRC-FIRST-PAIRWISE-001 — Pairwise Score Comparator

**Status:** specified / exploratory behavioral reference only  
**Owner:** Earth ICT, SPC (EIS)  
**Scope:** the first uncertainty-reduction milestone for the proposed PRISM → KKA bridge.

## Objective

Determine whether a candidate physical primitive can compare two encoded PRISM similarity scores and produce a usable winner signal while preserving the identity of the winning KV block. This experiment deliberately stops before a tournament, top-k network, or K/V routing fabric.

The formal contract is architecture-neutral. A physical implementation may be optical, analog optoelectronic, or another candidate architecture, but its selection-domain label must accurately describe the path actually used.

## Hypothesis

Given two candidate score-bearing signals A and B with known reference ordering, a candidate comparator can:

1. identify the higher score when the score gap is outside a pre-registered indifference region;
2. preserve the winning candidate identity in its output;
3. return `INDETERMINATE` rather than fabricate certainty for ties or unsupported conditions;
4. satisfy pre-registered correctness, optical-output usability, latency, loss, and energy criteria over a declared operating envelope.

This is a hypothesis. No physical comparator is validated by this repository artifact.

## First milestone only

Included:
- comparator contract and evidence requirements;
- deterministic behavioral reference and unit tests;
- explicit parameter/evidence provenance;
- a CRC-first screening plan for deciding which candidates merit expensive physics simulation.

Not included:
- a six-stage cascade;
- top-k ranking;
- K/V payload routing;
- a foundry-ready layout;
- validated compact models;
- claims of physical optical selection, latency, energy, or fabricated performance.

## Boundary and terms

The comparator receives two score-bearing inputs, plus candidate identities. The score-to-signal encoding must be documented by each implementation. It is not safe to assume that a PRISM score is already represented as a directly comparable optical power.

The abstract output is one of:
- `A_WINS`
- `B_WINS`
- `INDETERMINATE`
- `FAULT`

A physical B1 candidate passes the *domain* requirement only if the comparison and winner-token output remain optical through the declared comparator boundary. A photodetector or electronic decision in the comparison path is not B1. Interface A is recorded separately as `analog_optoelectronic`; it must not be called all-optical.

## Parameter provenance

Every parameter must carry one of these labels:
- `MEASURED`: measured on an identified physical artifact with conditions and raw evidence;
- `PAPER_REPORTED`: explicitly reported by a cited publication;
- `SIMULATED`: output of a named, versioned simulator/model;
- `MOCKED_FOR_EXPLORATION`: an assumed value used only to exercise the software or explore sensitivity;
- `UNKNOWN`: not established.

Never silently promote a mocked or paper-reported parameter to a measured property. Published component figures are not substitutes for a validated pairwise-comparator model.

## CRC-FIRST screen

Before FDTD/EM simulation, enumerate a small candidate set and reject candidates that cannot meet the abstract contract under their declared assumptions. Keep the initial candidate count and expensive-simulation budget explicit in the run record.

Potential sweep dimensions include:
- score encoding and input dynamic range;
- minimum score separation and tie/indifference band;
- input power imbalance;
- comparator bias/threshold and hysteresis;
- insertion loss and output contrast;
- noise and fabrication variation;
- response / recovery time;
- energy accounting boundary;
- output winner-token separability.

Do not insert assumed “typical” values as if they were foundry data. Begin with symbolic/unknown parameters and labeled synthetic vectors; set numeric ranges only with a source or an explicit experimental rationale.

CRC rejection must preserve the contract: report why a candidate is infeasible and what assumptions caused rejection. A candidate that survives CRC is only eligible for physics simulation; it has not passed physics or physical validation.

## Acceptance criteria — freeze before inspecting candidate results

The following must be filled and versioned before candidate outputs are inspected:
- score encoding and normalization;
- reference ordering and tie policy;
- minimum distinguishable score gap;
- allowed false-winner rate / required test count;
- operating envelope for input power imbalance and noise;
- output optical contrast / separability criterion;
- maximum insertion loss;
- maximum comparator latency / recovery time;
- energy boundary and maximum energy per comparison;
- allowed variation and robustness criteria.

Until populated, the experiment status is `SPECIFIED_NOT_PREREGISTERED`, not PASS. The behavioral tests check software plumbing only and do not choose scientific acceptance thresholds.

## Required evidence

A run record must include:
- source revision and clean/dirty state;
- experiment and candidate IDs;
- model/tool versions;
- parameter values and provenance labels;
- frozen acceptance criteria and their version/hash;
- test vectors and raw results;
- confusion matrix / false-winner counts and indeterminate counts;
- score gap, input imbalance, noise, loss, output contrast, latency and energy results where actually modeled;
- selection domain (`optical`, `analog_optoelectronic`, or `electronic`);
- physical validation state and explicit limitations.

Allowed statuses: `PASS`, `FAIL`, `BLOCKED`, `INCOMPLETE`. Use `BLOCKED` when a required model or evidence source is unavailable. Use `INCOMPLETE` when evidence is insufficient. A behavioral-reference unit test is not an experiment pass.

## Decision gate

- **B1 candidate eligible:** comparator model is independently justified, pairwise contract is preregistered, and the candidate survives CRC. This permits a bounded physics-model validation step; it does not claim B1 is physically viable.
- **Alternative optical architecture:** B1 cannot satisfy the pairwise contract under supported assumptions; retain the failure trace and state the alternative hypothesis.
- **Interface A baseline:** compare analog optoelectronic control using the same workload and explicit electronic/optical boundaries.
- **No decision:** if source parameters or acceptance thresholds remain unresolved, record `BLOCKED` or `INCOMPLETE`.

## Reference context

- PRISM upstream: https://github.com/hyoseokp/PRISM
- KKA paper: https://doi.org/10.1186/s43074-025-00182-7
- SiEPIC EBeam open SOI PDK: https://github.com/SiEPIC/SiEPIC_EBeam_PDK
- Princeton optical-thresholder preprint cited in the proposed review: https://arxiv.org/abs/1908.07067

These sources motivate investigation; they do not, by themselves, establish a validated PRISM-score comparator or top-k network. Verify publication metadata and the exact claimed metrics before using any number as a model parameter.

## Current result

**No physical simulation has been run. No compact model has been validated. No PDK-specific optimization has been run. No physical result is claimed.**
