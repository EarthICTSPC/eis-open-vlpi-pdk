# EIS Open VLPI Disclosure Doctrine

**Earth ICT, SPC (EIS)**  
**Status:** Open technical disclosure doctrine  
**Purpose:** Define how this repository functions as an enabling technical disclosure for Very Large Photonic Infrastructure (VLPI).

## 1. Purpose

This repository is the open technical-disclosure layer of the EIS-VLPI project.

It is intentionally organized differently from a research article. A research article primarily records scientific questions, methods, results, interpretation, and evidence. This repository is intended to disclose the architecture, contracts, interfaces, implementation rules, verification path, and reproducible physical-design artifacts needed for an independent implementation.

The governing question is:

> **Can a technically skilled person, using this disclosure and an appropriate open or lawfully obtained technology/PDK, understand how to implement and verify a compatible system?**

The repository therefore follows an **enabling-disclosure** model.

It is not itself a patent, does not grant patent rights, and does not provide legal advice.

## 2. "Make Your Own" Principle

EIS intends the open layer to support independent implementation.

> **Here is the architecture. Here are the contracts. Here are the interfaces. Here are the implementation rules. Here is the verification path. Here is the physical artifact. Make your own.**

An independent implementation does not need to use EIS's preferred foundry, simulator, packaging provider, or physical-design toolchain. Compatibility is established through published contracts, interfaces, schemas, and evidence requirements.

Where a technology-specific parameter is necessary, the open layer should disclose the required interface and semantics rather than reproduce proprietary process information.

## 3. Repository Versus Research Article

The two public artifacts have different purposes.

### Research Article

The research article answers:

- What question was investigated?
- What is established by prior work?
- What did EIS formally specify?
- What was computationally demonstrated?
- What was experimentally demonstrated?
- What remains a hypothesis?
- What conclusions are justified by the evidence?

### Open VLPI Repository

The repository answers:

- What is the architecture?
- What is the physical transformation?
- What is the state?
- What is the RU contract?
- What interfaces are required?
- How can an RU be instantiated?
- How is a technology mapped to the abstraction?
- How is the result verified?
- How is a physical artifact generated?
- What evidence must accompany the artifact?
- How can another party reproduce or independently implement it?

The repository may therefore contain implementation material that would be inappropriate or impractical to place in a journal article.

Conversely, publication of an implementation artifact does not convert a hypothesis into an experimental result.

## 4. Canonical EIS Physical-Transformation Model

The current EIS working RU abstraction is:

S_RU = (H,T,R,B,G,C)

where:

- **H** — physical field/state space
- **T** — physical transformation mapping
- **R** — constraint-reduction operator
- **B** — state-boundary acceptance
- **G** — state-to-field regeneration
- **C** — machine-checkable contract

The abstraction intentionally does not require a Boolean gate, electronic MAC, or matrix-vector interpretation.

A physical phenomenon becomes computationally relevant when its transformation is specified, bounded, composable, and verifiable.

## 5. Enabling-Disclosure Layers

The open disclosure should progressively expose:

1. **Physical principle** — what physical phenomenon is being used.
2. **State** — what physical state carries information.
3. **Transformation** — what mapping changes that state.
4. **Contract** — what conditions make the transformation acceptable.
5. **Primitive** — what physical structures implement the transformation.
6. **Composition** — how transformations are connected.
7. **Technology mapping** — how an implementation technology realizes the primitives.
8. **Verification** — how design and physical behavior are checked.
9. **Physical artifact** — how the design becomes OASIS or another fabrication artifact.
10. **Fabrication boundary** — what must be supplied to a foundry.
11. **BIST/evidence** — how fabricated behavior is measured and accepted.
12. **Replication** — how the unit can be instantiated and composed.

## 6. Open, Controlled, and Verified Boundaries

### Open

Material intentionally published for independent implementation, including schemas, architecture, contracts, non-proprietary primitives, examples, verification methodology, evidence schemas, reproducibility tooling, and public physical artifacts.

### Controlled

Material that may be necessary for a particular realization but is not EIS's to publish, including NDA foundry PDK contents, proprietary process design rules, proprietary compact models, credentials, private simulation environments, pre-release fabrication artifacts, and confidential packaging information.

The open repository must describe the **interface** to controlled technology without disclosing controlled contents.

### Verified

Evidence produced by an accepted verification or measurement process.

A file being present in GitHub does not by itself make the underlying physical claim verified.

## 7. Evidence Discipline

Every material claim should be assigned an evidence state.

The repository uses the following conceptual states:

- **draft** — incomplete or exploratory material.
- **specified** — behavior and acceptance conditions have been explicitly defined.
- **formally-verified** — a logical property has been machine-checked under stated assumptions.
- **computationally-demonstrated** — supported by a documented computational experiment.
- **experimentally-demonstrated** — supported by physical experimental measurement.
- **measured** — a measurement record exists for the identified artifact and condition.
- **proposed-hypothesis** — a research hypothesis or design target not yet demonstrated.
- **derived-metric** — a metric or framework derived from defined inputs rather than directly measured.

Formal verification is not fabrication. Simulation is not measurement. A design target is not a result.

The repository must preserve those distinctions.

## 8. Failure Is Disclosure

A failed candidate is useful technical information when the failure is reproducible and its conditions are recorded.

Implementations and experiments should record input artifact identity, technology identity, parameter set, assumptions, tool and version, result, failure mode, applicable contract, and evidence location.

EIS should not silently modify a design to make a tool accept it.

If an implementation requires a technology-specific change, the change should be explicit and attributable.

## 9. Technology Neutrality

The EIS architecture is intended to survive changes in foundry, material stack, simulator, packaging technology, and implementation tool.

Technology-dependent quantities belong in the technology layer.

Transformation semantics and acceptance contracts belong in the architecture layer.

This separation allows the same RU definition to be mapped to multiple technologies without pretending that their physical capabilities are identical.

## 10. DesignContext as the Integration Boundary

Heterogeneous EIS systems may contain photonic PDKs, electronic PDKs, electro-photonic interfaces, package/carrier definitions, optical interfaces, RF/electrical constraints, and thermal constraints.

These are represented through a common **DesignContext** rather than hidden assumptions.

A DesignContext must identify the technology identities and interfaces used to produce a particular physical artifact.

## 11. Verification and Realization Chain

Physical hypothesis
→ Physical state
→ RU contract
→ Candidate transformation
→ CRC constraint reduction
→ Physics simulation
→ PDK-constrained realization
→ PVR
→ PDR / PCT / PTV
→ OASIS
→ Foundry review
→ Fabrication
→ BIST / State Boundary measurement
→ Replication evidence
→ Useful computational service

Each stage produces evidence for the next. No stage should be represented as having completed a later stage's work.

## 12. Physical Artifact Doctrine

The physical-design artifact is part of the disclosure.

Where legally and technically appropriate, EIS should publish machine-readable RU manifests, contracts, technology mappings, test vectors, evidence manifests, generated OASIS/GDS artifacts, hashes, scripts, reference layouts, and failure examples.

An image of a layout is explanatory evidence. The machine-readable physical artifact is the implementation evidence.

## 13. Proprietary PDK Doctrine

EIS must not publish proprietary foundry PDK contents merely to make the open repository appear complete.

Instead, the repository should disclose required PDK capabilities, expected technology interfaces, layer/port semantics where lawfully publishable, parameter contracts, validation requirements, and adapter structure.

A private foundry PDK may then satisfy the same interface under its own controlled terms.

## 14. Human and Foundry Gates

Automation does not replace engineering responsibility.

Human review remains appropriate for build intent, technology selection, PDK selection, unusual physical assumptions, foundry submission, packaging, safety, and interpretation of ambiguous evidence.

A machine-readable PASS is evidence about the defined test, not authorization to fabricate or deploy.

## 15. Reproducibility

A reference implementation should make it possible to move from a clean checkout toward:

schema validation
→ RU instantiation
→ contract checks
→ reference simulation
→ PVR
→ physical artifact generation
→ evidence manifest

Where proprietary tools or PDKs are required, the open repository should identify the controlled boundary and provide the reproducible interface around it.

## 16. Patent and Public-Disclosure Caution

This doctrine deliberately uses the language of **enabling technical disclosure** and **those skilled in the art and science** as an engineering standard.

It does not assert that GitHub publication is a patent, creates patent rights, preserves patent rights, or substitutes for patent counsel.

Before publicly disclosing an enabling implementation of an invention for which EIS may seek patent protection, EIS should obtain appropriate legal advice regarding applicable jurisdictions, filing strategy, priority, and public-disclosure consequences.

## 17. Quality Test

A contribution is not complete merely because the code runs.

Ask:

> **Could another technically skilled person understand what was done, why it was done, what assumptions were made, what evidence exists, and how to make an independent implementation?**

If not, the disclosure is incomplete.

---

**Earth ICT, SPC (EIS)**  
*Open physical-computing infrastructure for an Earth-first ICT future.*
