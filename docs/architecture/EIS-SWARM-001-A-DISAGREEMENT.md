# EIS-SWARM-001-A-DISAGREEMENT

**Status:** Discovery artifact — not an ontology decision  
**Experiment:** EIS-SWARM-001-A  
**Evidence baseline:** GitHub2VLPI-002 frozen empirical evidence  
**Independent derivations:** EURIA, Claude, Grok

## 1. Purpose

This document compares three independent derivations of the admissible transformation population from the frozen GitHub2VLPI-002 evidence.

The purpose is not to choose the best LLM answer. It is to identify which claims are:

1. Forced by frozen evidence
2. Valid alternative decomposition
3. Unsupported assumption
4. Unresolved contract
5. New experimentally testable question

No candidate population, field algebra, compiler architecture, or formal ontology is selected by this document.

## 2. Source boundary

The frozen experiment establishes five executed phase observations from the RU-001 reference model, residual structure including cancellation at 0 and maximum residual near pi, PDK capability classifications, explicit not-run status, and no physical validation, fabrication, measurement, PVR PASS, or BIST PASS.

EURIA, Claude, and Grok were treated as independent derivations. No prior EIS-SWARM-001 candidate population or dependency graph was used as an expected answer.

## 3. Three-way disagreement matrix

| Question | EURIA | Claude | Grok | Classification |
|---|---|---|---|---|
| Residual computation | PhaseShift | ResidualReferenceMap | ResidualReferenceMap | Forced at functional level; naming/decomposition is alternative |
| Phase sweep | folded into FieldSweeper | separate PhaseSweep | separate PhaseSweep | Valid alternative decomposition |
| Power calculation | separate PowerCalc | exact observation functional left unresolved | exact observation functional left unresolved | EURIA decomposition not forced; exact functional is unresolved |
| Residual structure interpretation | InvariantChecker | ResidualStructureCheck | ResidualStructureCheck | Interpretation is evidenced; agent boundary is alternative |
| Evidence classification | implicit | EvidenceLabeler | EvidenceLabeler | Evidence rule is forced; separate agent is not |
| PDK capability classification | CapabilityCheck / CompatibilityValidator | PdkCapabilityProbe | PdkCapabilityProbe | Operation is forced; agent boundary is alternative |
| Not-run preservation | status in capability result | explicit | explicit | Status is forced; primitive/agent status unresolved |
| Next-state planning | absent | optional NextStateEmitter | optional NextStateEmitter | Not forced by frozen run |

### Finding

The three derivations converge on a residual observation, sweep/aggregation, interpretation, evidence classification, and an independent PDK capability classification. They disagree mainly on how finely these operations should be factored.

Therefore the evidence does not determine a swarm cardinality.

## 4. Exact residual / field transformation

EURIA proposes the specific complex-field expression r = (a - exp(i phi)b) / sqrt(2), followed by P = |r|^2.

Claude and Grok refuse to infer a unique closed-form field function from the five observations. They identify field encoding, amplitude versus power, normalization, units/norm, tolerance, exact residual functional, and the relationship of 0 and 2pi as unresolved.

**Classification:**

- Existence of a reproducible residual observation transformation: **FORCED BY FROZEN EVIDENCE**.
- EURIA's specific complex formula as forced by the five samples: **UNSUPPORTED ASSUMPTION**.
- Exact mathematical observation functional: **UNRESOLVED CONTRACT**.

This is the strongest ontology-discovery result so far.

## 5. Candidate agent population

EURIA compresses the residual path into FieldValidator plus CapabilityValidator. Claude/Grok separate ResidualReferenceMap, PhaseSweep, ResidualStructureCheck, EvidenceLabeler, and PdkCapabilityProbe, with NextStateEmitter optional.

Classification: **VALID ALTERNATIVE DECOMPOSITION.**

No population cardinality is forced by the freeze. The evidence forces operations and evidence boundaries, not a particular number of agents.

## 6. Dependency graph

All three derivations support the dependency that single-phase residual evaluation precedes a multi-phase sweep. They also support independence between residual computation and PDK capability classification.

Whether structure checking, evidence labeling, and next-state planning must be separate agents is not forced.

Classification: **PARTLY FORCED, PARTLY DECOMPOSITION CHOICE.**

## 7. Invariant disagreement

EURIA introduces Pmax <= 2, Pmin >= 0, P(pi) approximately 2, P(0) approximately 0, and characterizes the reference transformation as unitary / energy-conserving.

Claude/Grok restrict interpretation to model-relative structure: cancellation near 0, maximum residual near pi, and checks over the observed table.

Classification:

- Energy conservation/unitarity as demonstrated physical evidence: **UNSUPPORTED ASSUMPTION**.
- Model-relative structure checks: **FORCED** if the frozen qualitative interpretation is to be machine-checked.

Do not promote energy conservation into the formal ontology from SWARM-001-A.

## 8. Constraint vocabulary

EURIA proposes Constraint as a primitive because compatibility is effectively constraint satisfaction. Claude/Grok do not promote Constraint yet; they identify the precise reference observation functional as the more immediate missing specification.

Classification:

- Constraint as a useful concept: **VALID CANDIDATE**.
- Constraint as a primitive forced by this freeze: **NOT ESTABLISHED**.
- Reference observation functional: **UNRESOLVED CONTRACT**.

## 9. Evidence boundary

All three derivations agree that residual results are computational/model evidence, PDK results are capability-compatibility evidence, explicit not-run remains not-run, and physical validation/fabrication/measurement/PVR/BIST/foundry acceptance are not established.

Classification: **FORCED BY FROZEN EVIDENCE.**

The agent responsible for enforcing the boundary is an implementation choice; the boundary itself is not.

## 10. Not-run semantics

Claude/Grok elevate not-run to a first-class concept; EURIA treats it primarily as a capability-check result.

Classification: explicit not-run status is **FORCED BY THE FROZEN RECORD**. Whether Not-run must become a primitive formal concept remains an **UNRESOLVED CONTRACT**.

Silent conversion of not-run into compatible/pass is ruled out.

## 11. Rejected transformations

All derivations exclude fabrication/tape-out, physical measurement/BIST, foundry acceptance, compiler architecture, and physical promotion from the current evidence boundary.

Claude/Grok additionally reject treating the prior EIS agent roster as mandatory ontology.

Classification: evidence boundary is **FORCED**; exact rejected-agent taxonomy is an alternative representation.

## 12. Proposed next experiment disagreement

EURIA proposes resolving state-boundary, thermal, and wafer-topology semantics through a PVR-oriented validation experiment.

Claude/Grok propose first closing the residual observation contract: exact reference implementation/formula or hash, input field encoding, tolerance, repeat the five phases, and add an off-grid phase such as pi/4.

The unresolved state-boundary, thermal, and wafer-topology contracts are forced by the PDK matrix. The unresolved residual observation contract is independently identified by Claude/Grok.

Classification: **NEW EXPERIMENTAL PRIORITY QUESTION.**

The EURIA PVR proposal is a valid testable question, but its priority over closing the residual functional is not established by the freeze.

## 13. Three-way ontology comparison

| Concept | EURIA | Claude | Grok | Current status |
|---|---:|---:|---:|---|
| State | yes | yes | yes | Strong convergence |
| Transformation | yes | yes | yes | Strong convergence |
| Phase | implicit/parameter | explicit | explicit | Evidenced parameter; primitive status open |
| Observation/residual | implicit in power | explicit | explicit | Strong convergence |
| Invariant | yes | yes | yes | Convergent, but model-relative |
| Constraint | yes | not promoted | not promoted | Unresolved candidate |
| Contract | yes | yes | yes | Strong convergence |
| Evidence | yes | yes | yes | Strong convergence |
| Boundary | implicit | explicit | explicit | Boundary forced; primitive status open |
| Not-run | status | explicit | explicit | Status forced; primitive status open |
| Composition | implicit | explicit | explicit | Dependency exists; formal primitive status open |
| Exact observation functional | assumed | unresolved | unresolved | Critical unresolved contract |
| Compiler | not required | not required | not required | Not required by freeze |
| Swarm cardinality | 2 | multiple | multiple | Not determined |

## 14. Classification summary

### Forced by frozen evidence

- A reproducible residual observation is produced by the RU-001 reference execution.
- A finite phase sweep was executed.
- Qualitative residual structure was reported.
- PDK capability classification was executed.
- Explicit not-run information exists.
- Physical validation did not occur.
- Computational/capability evidence must not be promoted to physical evidence.

### Valid alternative decomposition

- One agent versus separate residual-map and sweep agents.
- Separate versus merged structure checking.
- Separate evidence-labeling agent versus a wrapper/process.
- Exact agent names.
- Agent cardinality, absent an additional independence/composition contract.

### Unsupported assumption

- EURIA's specific complex residual formula as something forced by the five observed points.
- Treating the reference result as demonstrated physical unitarity/energy conservation.
- Treating a particular field encoding as established by the freeze.

### Unresolved contract

- Exact residual observation functional.
- Field encoding.
- Units/norm/normalization.
- Tolerance.
- Capability probe semantics.
- Relationship/composition between residual observations and PDK capability state.
- Whether 0 and 2pi are formally identical.
- Whether Constraint, Boundary, or Not-run must become primitive formal vocabulary.

### New experimentally testable questions

- Does an explicit field/reference functional predict an off-grid phase correctly?
- What tolerance is justified by the reference model?
- What precise state-boundary semantics distinguish compatibility from incompatibility?
- What executable capability probe should establish each PDK capability?
- Does finer transformation decomposition provide independently useful verification, or merely duplicate composition?

## 15. What SWARM-001-A has actually discovered

The experiment has not discovered a final EIS ontology.

It has discovered a boundary around what the current evidence can support.

The strongest result is:

> The frozen five-point residual sweep establishes the existence of a reproducible reference-model observation, but does not uniquely determine the field representation or the mathematical functional that generated that observation.

Therefore:

> **Do not formalize the assumed field algebra yet.**

The independent derivations instead point to the need to close the contract of the executable reference observation before claiming that the observed transformation has a unique formal decomposition.

## 16. Current conclusion

**EIS-SWARM-001-A remains open.**

No candidate population is promoted.
No compiler architecture is introduced.
No field algebra is introduced.
No physical claim is promoted.

The working principle is:

> **Discover the ontology. Do not design it.**

The ontology is the smallest formal vocabulary that survives independent derivation, removal of unsupported assumptions, and resolution of experimentally distinguishable alternatives.