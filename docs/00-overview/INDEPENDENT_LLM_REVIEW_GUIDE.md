# Independent LLM Review Guide

**Purpose:** make the EIS Open VLPI-PDK repository independently reviewable by external LLMs and technical collaborators.

This guide is intentionally conservative. It tells a reviewer **where the evidence is** and **what may and may not be inferred from it**. It does not prescribe an ontology, agent population, compiler architecture, or field algebra.

## Repository

The canonical repository is:

https://github.com/EarthICTSPC/eis-open-vlpi-pdk

The repository is public.

If a direct fetch fails, retry the canonical URL and, if necessary, use the raw GitHub file URL for the specific file being reviewed. A transient fetch failure must not be interpreted as evidence that the repository is private or nonexistent.

## Start here

For an independent review, read in this order:

1. `README.md`
2. `docs/00-overview/EIS_Open_VLPI_Disclosure_Doctrine.md`
3. The frozen GitHub2VLPI-002 evidence artifacts under `evidence/github2vlpi-002/`
4. `docs/architecture/EIS-SWARM-001-A-DISAGREEMENT.md`
5. The associated pull request discussion, if reviewing the discovery process.

## Current discovery question

EIS-SWARM-001-A is **not** asking the reviewer to select an agent population.

The current question is:

> What is the smallest formal vocabulary actually required by the observed physical/reference transformation, without importing assumptions from a conventional digital-computing ontology?

In particular, do **not** assume that the five-point phase sweep uniquely determines a complex-field formula.

## Review boundary

Separate these evidence classes:

- **Reference-model / computational evidence:** behavior produced by the executable reference model.
- **Capability compatibility:** whether a declared PDK capability is compatible with a specified requirement.
- **Not-run:** explicitly not executed.
- **Physical evidence:** fabrication, measurement, PVR/PDR/PCT/PTV, BIST, or foundry acceptance.

The repository does not permit computational or capability evidence to be silently promoted to physical evidence.

## Questions for an independent LLM

Please report:

1. What claims are forced by the frozen evidence?
2. What claims are merely alternative decompositions?
3. What assumptions are unsupported by the evidence?
4. What contracts remain unresolved?
5. What next experiment would most efficiently distinguish the competing interpretations?
6. Which terms appear necessary, and which are premature?
7. Does the evidence justify an agent population or compiler architecture yet?

Please explicitly identify uncertainty and disagreement rather than filling gaps with conventional assumptions.

## What not to do

Do not:

- treat a repository artifact as physical validation merely because it exists;
- infer fabrication, measurement, foundry acceptance, or BIST PASS from a reference-model result;
- assume a conventional matrix/vector, Boolean-gate, MAC, or compiler abstraction;
- treat the prior EIS-SWARM-001 population as the expected answer;
- introduce a new field algebra merely to make the current evidence easier to formalize.

## Suggested independent-review response format

### 1. Access
Could you retrieve the canonical repository and the frozen evidence?

### 2. Forced findings
List only claims directly supported by the frozen evidence.

### 3. Disagreements
Identify competing interpretations and classify each as:
- forced by evidence;
- valid alternative decomposition;
- unsupported assumption;
- unresolved contract;
- new experimentally testable question.

### 4. Minimum vocabulary
Propose only terms independently required by the evidence. Explain why each term is necessary.

### 5. Next experiment
Name the smallest experiment that could resolve the most consequential unresolved contract.

### 6. Non-claims
State explicitly what the evidence does **not** establish.

## Important access note

A web search result or LLM fetch error is not itself evidence about repository visibility. The repository currently reports itself as public through GitHub. If one retrieval path fails, record the failure as an **access-path observation** and retry through another GitHub retrieval path before drawing conclusions about repository availability.
