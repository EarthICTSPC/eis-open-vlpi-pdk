# VLPI-PLATFORM-001 — VLPI Programming Model and Runtime Architecture

**Project:** Earth ICT, SPC (EIS)  
**Status:** Proposed architecture / enabling technical disclosure  
**Artifact:** VLPI-PLATFORM-001  
**Scope:** Programming model, intermediate representation, compiler, runtime, libraries, observability, and migration from conventional computational code  
**Related architecture:** RU, CRC, PVR, DesignContext, PDKIdentity, OASIS, BIST, EURIA, MCP, FlexAgent, RISC-V, VLPI  
**Date:** 2026-10-05

---

## 1. Purpose

Earth ICT, SPC (EIS) is developing Very Large Photonic Infrastructure (VLPI) as a programmable physical-computation platform.

A photonic physical substrate is not sufficient to establish a computing platform. A computing platform requires a usable programming abstraction, an intermediate representation, a compiler or lowering system, a runtime, libraries, development tools, verification, deployment mechanisms, and an application path.

This artifact establishes the proposed EIS software architecture for that missing layer.

The central objective is:

> **EIS needs to build the software ecosystem that makes a Replicable Unit (RU) a programmable computational primitive.**

The RU is therefore treated as the fundamental physical-computation object, not merely as a layout block or photonic component.

This document deliberately does not claim that the complete software stack has already been implemented. It defines the architecture and identifies which elements already exist, which are partially implemented, and which remain research and engineering work.

---

## 2. The six platform questions

VLPI-PLATFORM-001 answers six questions exposed by comparison with established accelerator ecosystems.

| Question | VLPI answer | Status |
|---|---|---|
| What is the VLPI equivalent of a CUDA kernel? | **Replicable Unit (RU)** | Existing architecture; RU-001 specified and realized as repository artifact; RU-002 specified as candidate architecture |
| What is the VLPI equivalent of PTX/HLO? | **VLPI-IR** | Proposed; architecture defined here |
| What is the VLPI compiler? | **CRC → physical realization → PVR → OASIS** | Partially established; compiler integration remains development work |
| What is the VLPI runtime? | **State-boundary-aware resource/runtime layer** | Proposed; control/orchestration foundations exist |
| What is the VLPI CUDA-X equivalent? | **Libraries of composable verified physical transformations (“field math” libraries)** | Proposed; first libraries to be defined |
| What is the VLPI Nsight equivalent? | **Physical-state + thermal + evidence + CO₂e/VUT observability** | Architecture established; integrated profiler remains future work |

The comparison is architectural rather than branding-oriented. CUDA is NVIDIA's parallel-computing programming platform; NVIDIA documents PTX as a virtual instruction-set layer and the CUDA runtime/driver as the software interface between applications and GPU hardware. The EIS objective is not to reproduce NVIDIA's implementation, but to learn from the existence of a complete accelerator software stack.

---

## 3. The complete VLPI platform stack

~~~
APPLICATIONS
    │
    │ computational intent
    ▼
VLPI SDK / PROGRAMMING MODEL
    │
    │ high-level physical-computation operations
    ▼
VLPI-IR
    │
    │ explicit state / transformation / RU graph
    ▼
VLPI COMPILER
    │
    ├── CRC constraint reduction
    ├── RU selection/composition
    ├── DesignContext / PDKIdentity
    ├── physics entry
    ├── PVR
    └── OASIS realization
    │
    ▼
VLPI RUNTIME
    │
    ├── resource admission
    ├── state management
    ├── state-boundary scheduling
    ├── configuration
    ├── thermal/power policy
    └── evidence/provenance
    │
    ├──────────────────────┐
    ▼                      ▼
RISC-V CONTROL        PHOTONIC EXECUTION
    │                      │
    ├── I/O                ├── RU
    ├── memory             ├── optical state
    ├── configuration      ├── transformation
    ├── BIST control       ├── composition
    └── external services  └── optical fabric
    │                      │
    └──────────┬───────────┘
               ▼
       VLPI PHYSICAL FABRIC
       RU → tile → wafer → stack
               │
               ▼
       thermal / power / facility
               │
               ▼
           CO₂e / VUT
~~~

MCP, EURIA, FlexAgent, GitHub, physics tools, and controlled PDK environments operate across this stack as orchestration and engineering infrastructure. They are not themselves the physical computing substrate.

---

## 4. The key abstraction: the RU

### 4.1 RU as the VLPI computational primitive

A CUDA kernel is executable device code launched on a GPU.

The proposed VLPI equivalent is the **Replicable Unit (RU)**.

But the analogy has an important limitation:

> A CUDA kernel is primarily software executed by hardware. An RU is a contract-governed physical transformation whose realization spans software, physical design, physics, fabrication, measurement, and evidence.

The RU is therefore defined by its physical transformation and contract rather than by a fixed number of photonic components.

The core EIS representation is:

~~~
S_RU = (H, T, R, B, G, C)
~~~

where:

- **H** = physical field/state space
- **T** = physical transformation mapping
- **R** = constraint-reduction operator
- **B** = state-boundary acceptance
- **G** = state-to-field regeneration
- **C** = machine-checkable contract

An RU may contain multiple physical transformations and internal optical states.

It is not defined by the number of PIC blocks, MZIs, MRRs, electronic interfaces, or other implementation details.

---

## 5. VLPI-IR — the missing intermediate representation

### 5.1 Why an IR is required

A high-level application should not directly encode foundry-specific geometry.

Likewise, a physical designer should not have to reconstruct application semantics from OASIS.

A stable intermediate representation is required between:

~~~
application intent
       ↓
physical-computation program
       ↓
RU graph
       ↓
technology realization
       ↓
physical artifact
~~~

This is the role of **VLPI-IR**.

### 5.2 Proposed VLPI-IR properties

VLPI-IR should represent:

- physical state spaces
- state representations
- transformations
- transformation composition
- constraint reductions
- state boundaries
- regeneration points
- RU references
- contracts
- resource requirements
- topology
- timing
- optical/electrical interfaces
- technology-independent intent
- DesignContext requirements
- evidence requirements
- provenance

VLPI-IR should not encode proprietary PDK content.

Instead:

~~~
VLPI-IR
   +
DesignContext
   +
PDKIdentity
   ↓
technology-specific realization
~~~

### 5.3 Example conceptual IR

~~~yaml
program:
  name: attention_example
  version: "0.1"

state:
  input:
    space: H_QKV
    representation: optical_field

transformations:
  - ru: RU-KKA-CACHE
    input: H_QKV
    output: H_similarity

  - ru: RU-SELECT
    input: H_similarity
    output: H_selected

  - ru: RU-ATTENTION
    input: H_selected
    output: H_attention

boundaries:
  - after: H_attention
    boundary: contract-defined

requirements:
  preserve_optical_state_when:
    next_transformation_accepts: H_optical

technology:
  designContext: DESIGN-CONTEXT-REF

evidence:
  contract: CONTRACT-REF
~~~

This is illustrative architecture, not a frozen schema.

The schema must be developed through machine-checkable examples before being declared stable.

---

## 6. VLPI compiler

### 6.1 Compiler definition

The VLPI compiler is not merely a geometry generator.

Its job is to lower a physical-computation program into a realizable, verifiable physical artifact.

The proposed path is:

~~~
VLPI-IR
   ↓
semantic validation
   ↓
RU resolution
   ↓
CRC constraint reduction
   ↓
resource / state analysis
   ↓
DesignContext + PDKIdentity
   ↓
candidate physical realization
   ↓
physics simulation
   ↓
PVR
   ↓
OASIS
   ↓
foundry review
~~~

### 6.2 CRC's role

CRC is therefore a compiler-stage technology.

CRC should answer questions such as:

- Which candidate transformations are physically admissible?
- Which constraints can be reduced before expensive EM?
- Which candidate RU compositions can proceed?
- Which physical realization is compatible with the contract?
- Which candidates should consume expensive simulation resources?

CRC-FIRST-001 is the initial experimental vehicle for this idea.

### 6.3 FlexAgent's role

FlexAgent is not the compiler itself.

It is an agentic engineering capability operating within the controlled toolchain.

Conceptually:

~~~
VLPI compiler
      │
      ├── deterministic compilation rules
      │
      └── agentic search / physics assistance
                 │
                 ▼
             FlexAgent
                 │
          PhotonForge / Tidy3D
~~~

Agent-generated output must remain subordinate to contracts, evidence rules, PVR, and human authorization boundaries.

---

## 7. VLPI runtime

### 7.1 Runtime definition

The VLPI runtime is the execution layer that manages physical computation after compilation and realization.

It is responsible for:

- RU admission
- resource allocation
- physical-state routing
- configuration
- state-boundary management
- regeneration
- thermal/power limits
- workload scheduling
- provenance
- BIST interaction
- recovery
- external I/O

The runtime should not assume that every operation is a digital instruction executed on a clock.

### 7.2 State-boundary-aware scheduling

This is a fundamental VLPI runtime principle.

A conventional operating system can often preempt a process at a time-slice boundary by saving digital state and restoring it later.

A propagating optical field does not automatically provide an equivalent lossless snapshot mechanism.

Therefore:

> **VLPI scheduling quanta are state boundaries where the physical state can be validly accepted, measured, represented, stored, regenerated, or otherwise handed back to the runtime.**

This makes the existing EIS state-boundary concept operationally important.

~~~
physical transformation
        │
        │ no arbitrary preemption assumed
        ▼
state boundary B
        │
        ├── accept
        ├── measure
        ├── regenerate
        ├── checkpoint
        ├── route
        └── schedule next transformation
~~~

This remains a research architecture. The physical ability, latency, fidelity, and cost of each proposed state boundary must be demonstrated for the relevant implementation.

---

## 8. RISC-V control plane

RISC-V is the proposed general-purpose control and I/O plane for VLPI systems.

It is not the photonic datapath.

The architecture follows a heterogeneous-computing pattern:

~~~
RISC-V
  ├── external I/O
  ├── memory
  ├── configuration
  ├── workload control
  ├── BIST
  ├── health/status
  └── system management

Photonic substrate
  ├── field transformation
  ├── optical state
  ├── composition
  ├── routing
  └── specialized physical computation
~~~

The historical Cray lesson is relevant: specialized numerical hardware can be paired with a separate front-end/control computer rather than forcing the specialized processor to perform general system-management work.

EIS adopts this as an architectural precedent, not as a claim that VLPI is identical to a Cray.

---

## 9. VLPI Field Math Libraries

### 9.1 The missing software ecosystem

The traditional computing ecosystem contains mature numerical libraries for operations such as:

- matrix multiplication
- convolution
- FFT
- linear algebra
- sparse operations
- reductions
- random number generation
- optimization
- tensor operations

A VLPI platform cannot become useful merely by providing physical hardware.

It needs an equivalent library layer.

EIS therefore proposes:

> **VLPI Field Math Libraries**

These libraries should expose useful physical transformations at a level above individual photonic devices and below application frameworks.

The library object should be a verified physical transformation or composition of verified RUs.

### 9.2 Candidate field-math categories

Initial research categories include:

~~~
FIELD
├── superposition
├── addition / subtraction
├── weighted field combination
├── phase transformation
├── amplitude transformation
├── interference / difference
├── correlation / similarity
├── reduction
├── selection / routing
├── normalization
├── spectral transformation
├── convolution-like transformations
├── attention transformations
└── collective communication transformations
~~~

These names describe research targets.

They do not imply that every conventional mathematical operation has a one-to-one physical equivalent or that an implementation already exists.

### 9.3 Field math versus matrix math

EIS should resist the assumption:

~~~
photonic computing
    =
electronic matrix multiplication
    +
light
~~~

Instead:

~~~
photonic field
    ↓
physical transformation
    ↓
state
    ↓
physical reduction
    ↓
next transformation
~~~

Matrix multiplication may be one useful special case.

It should not define the entire programming model.

---

## 10. Can existing libraries and code be converted?

### Short answer

**Sometimes. But translation should not be the primary strategy.**

There are at least four migration classes.

### Class A — Exact semantic preservation

A conventional operation has a known physical realization with equivalent semantics.

Example:

~~~
legacy operation
       ↓
mathematical specification
       ↓
field transformation
       ↓
RU composition
~~~

This can potentially be automatically lowered.

### Class B — Decomposable transformation

A conventional operation can be decomposed into a sequence of physical transformations.

Example:

~~~
legacy algorithm
       ↓
operator graph
       ↓
VLPI-IR
       ↓
RU graph
~~~

The result is not a line-by-line translation of source code.

It is a semantic compilation.

### Class C — Approximate or hardware-aware transformation

The physical implementation changes precision, representation, dynamic range, latency, or state-boundary behavior.

The migration must then carry an explicit approximation/error contract.

It must not silently claim equivalence.

### Class D — Fundamentally mismatched operation

Some conventional operations may depend on:

- arbitrary mutable memory
- unpredictable branching
- pointer-heavy data structures
- exact bit-level semantics
- side effects
- random access patterns
- operating-system services

These may not map naturally to a photonic physical transformation.

The correct answer may be:

> keep this operation in the electronic/control domain.

VLPI is heterogeneous by design.

---

## 11. Therefore: do not “port CUDA libraries to photons”

The first EIS field-math library should not be:

~~~
cuBLAS → photonic BLAS
~~~

That would inherit the assumptions of the old computational substrate.

Instead:

~~~
old algorithm
     ↓
identify mathematical / computational intent
     ↓
identify physical transformations
     ↓
construct VLPI-IR
     ↓
select verified RU compositions
     ↓
compile to physical realization
~~~

This is **semantic migration**, not source-code translation.

A conventional matrix library can therefore be used as:

1. a mathematical reference;
2. a test oracle;
3. a workload generator;
4. a comparison baseline;
5. a source of algorithms to be re-expressed.

It does not have to become the architecture.

---

## 12. The opportunity for AI: coding from new knowledge

Modern AI systems are highly effective at generating conventional code because enormous quantities of conventional code, documentation, examples, and tests exist in their training and retrieval environments.

That creates an important EIS question:

> **Can an AI system generate code for a computational substrate whose programming model did not exist in its historical training data?**

The answer should be:

> **Yes, but only if the new knowledge is made machine-readable, executable, testable, and connected to ground truth.**

An LLM does not need to have memorized VLPI code if the environment provides:

~~~
new knowledge
   +
formal schema
   +
typed interfaces
   +
contracts
   +
examples
   +
reference implementations
   +
tests
   +
physics tools
   +
evidence boundaries
~~~

Then the model can synthesize against the new system.

This is substantially different from asking an LLM to “invent photonic code” from prose.

---

## 13. From code generation to knowledge-grounded physical compilation

The proposed EIS loop is:

~~~
Human / researcher
       ↓
physical-computation intent
       ↓
VLPI schema + contracts
       ↓
AI / agent
       ↓
VLPI-IR
       ↓
schema validation
       ↓
reference-model tests
       ↓
CRC
       ↓
physics simulation
       ↓
PVR
       ↓
physical artifact
       ↓
BIST
       ↓
new knowledge
~~~

The AI therefore does not become the source of truth.

It becomes a **candidate generator and compiler assistant operating against executable knowledge**.

The evidence chain remains authoritative.

---

## 14. This is what “new coding on new knowledge” should mean

EIS should define three generations of agentic coding:

### Generation 1 — Retrieval coding

~~~
known API
+
known library
+
known examples
→
new application code
~~~

This is what current coding agents are particularly good at.

### Generation 2 — Specification-grounded coding

~~~
new schema
+
new contract
+
reference implementation
+
tests
→
new implementation
~~~

This is the GitHub2Agent model EIS is already testing.

### Generation 3 — Physics-grounded coding

~~~
new physical model
+
RU contract
+
VLPI-IR
+
DesignContext
+
physics simulator
+
PVR
→
new physical-computation implementation
~~~

This is the EIS target.

The distinction is important:

> **The agent is not asked to remember the new technology. It is given a machine-checkable environment in which the new technology can be discovered, composed, tested, and rejected.**

---

## 15. Existing EIS artifacts mapped into the platform

| Platform layer | EIS artifact | Role |
|---|---|---|
| Application | LLM / AI agent / scientific workload | Useful computation |
| Programming model | RU + S_RU=(H,T,R,B,G,C) | Physical computational abstraction |
| IR | **VLPI-IR** | Proposed intermediate representation |
| Field math | **VLPI Field Math Libraries** | Proposed verified physical transformation libraries |
| Compiler | CRC / CRC-FIRST | Constraint reduction and candidate admission |
| Physical realization | DesignContext / PDKIdentity | Technology binding |
| Physical verification | PVR | Pre-fabrication physical evidence |
| Artifact generation | OASIS | Physical design artifact |
| Physics execution | FlexAgent + PhotonForge + Tidy3D | Controlled physics workflow |
| Orchestration | EURIA / MCP | Tool and workflow coordination |
| Runtime | **VLPI-RT** | Proposed state/resource runtime |
| Control | RISC-V | I/O, memory, configuration, BIST |
| Physical execution | RU-001 / RU-002 / future RUs | Physical transformations |
| Fabric | VLPI | RU → wafer → stacked wafer → infrastructure |
| Hardware evidence | BIST | Post-fabrication evidence |
| Observability | **VLPI Profiler** | Proposed physical/thermal/evidence observability |
| Environmental accounting | CO₂e/VUT | Useful-work environmental metric |

---

## 16. Proposed VLPI platform repository evolution

The open repository should eventually expose:

~~~
eis-open-vlpi-pdk/
├── schema/
│   ├── ru/
│   ├── contract/
│   ├── evidence/
│   ├── design-context/
│   ├── verification/
│   └── vlpi-ir/                 # future
│
├── ir/                          # future
│   ├── examples/
│   ├── validators/
│   └── lowering/
│
├── libraries/                   # future
│   └── field-math/
│       ├── superposition/
│       ├── interference/
│       ├── reduction/
│       ├── selection/
│       ├── similarity/
│       └── attention/
│
├── runtime/                     # future
│   ├── state/
│   ├── scheduling/
│   ├── resource/
│   └── evidence/
│
├── compiler/                    # future
│   ├── crc/
│   ├── ru-lowering/
│   ├── pvr/
│   └── oasis/
│
├── agents/
│   ├── github2agent/
│   └── physics/
│
├── ru/
│   ├── RU-001/
│   └── RU-002/
│
└── tests/
    ├── schema/
    ├── ir/
    ├── field-math/
    ├── compiler/
    └── runtime/
~~~

This is a roadmap, not a claim that these directories already exist.

---

## 17. Ground truth and evidence

The platform must preserve the evidence discipline already established by GitHub2Agent-001/002 and RU-001/PVR-001.

The following are distinct:

### Information-model validity

> Does the artifact conform to the schema?

### Physical-model validity

> Does the physical model satisfy the stated constraints?

### Computational evidence

> Did the simulator produce the reported result?

### Fabrication evidence

> Was the design fabricated?

### Measurement evidence

> Did the fabricated object produce the measured result?

### Workload evidence

> Did the physical system perform the intended useful computation?

### Environmental evidence

> What was the measured or calculated CO₂e/VUT?

No platform layer may silently promote one category into another.

---

## 18. State boundaries in the programming model

VLPI-IR and VLPI-RT must preserve the EIS state model.

The runtime should be able to represent:

~~~
H_QKV
   ↓
H_similarity
   ↓
H_selected
   ↓
H_attention
~~~

without assuming that every transition requires:

~~~
optical
 ↓
electrical
 ↓
optical
~~~

The runtime question is:

> **Can the next transformation accept the current physical representation?**

If yes, preserve the physical state.

If no, invoke an explicit state boundary.

This rule prevents the software architecture from silently reintroducing the electronic bottleneck that the physical architecture is intended to investigate.

---

## 19. Runtime resource model

A VLPI runtime should eventually treat the following as first-class resources:

~~~
optical_state
wavelength
phase
amplitude
spatial_channel
temporal_window
RU_capacity
state_boundary
regeneration_capacity
electrical_control
memory
thermal_budget
power_budget
optical_loss_budget
communication_bandwidth
evidence_budget
~~~

This is fundamentally different from a conventional CPU scheduler that primarily sees:

~~~
cores
memory
threads
I/O
time
~~~

VLPI-RT therefore requires a physical resource model.

---

## 20. Observability: the VLPI equivalent of Nsight

A mature VLPI platform needs more than conventional software profiling.

The proposed **VLPI Profiler** should eventually correlate:

### Physical

- field/state representation
- transformation sequence
- optical loss
- phase/amplitude behavior
- state-boundary transitions
- regeneration events

### Computational

- useful transformations
- throughput
- latency
- utilization
- queueing
- workload behavior

### Thermal

- dissipated power
- local thermal load
- thermal gradients
- cooling overhead

### Evidence

- contract version
- DesignContext
- PDKIdentity
- simulation provenance
- PVR status
- BIST status
- measurement provenance

### Environmental

- direct energy
- cooling energy
- storage energy
- network energy
- embodied contribution
- CO₂e/VUT

The objective is not merely:

> “How fast is the accelerator?”

It is:

> **“What physical resources were consumed to produce verified useful computation?”**

---

## 21. CO₂e/VUT becomes a runtime metric

This is an important difference from conventional accelerator tooling.

The runtime should eventually be able to associate:

~~~
workload
   ↓
physical transformations
   ↓
resource consumption
   ↓
energy / heat / cooling / network
   ↓
CO₂e
   ↓
Verified Useful Transformations
~~~

giving:

~~~
CO₂e / VUT
~~~

as a system-level observability metric.

This does not mean that an environmental advantage is currently demonstrated.

It means the platform architecture should make the metric computable and auditable.

---

## 22. Field libraries: migrate or rebuild?

EIS should pursue both strategies, but in the correct order.

### Strategy A — Re-express mature algorithms

Take established algorithms and ask:

> What is the underlying computational transformation?

Then express that transformation in VLPI-IR and implement it using verified RUs.

This allows existing software knowledge to become a test/reference corpus.

### Strategy B — Build native field libraries

Where physical field behavior offers a fundamentally different computational primitive, build a native field library rather than forcing an electronic abstraction onto it.

For example:

~~~
field interference
field reduction
phase coupling
resonant selection
optical similarity
physical routing
~~~

may become native VLPI operations.

### Strategy C — Hybrid libraries

A high-level API can expose one operation while selecting among:

~~~
electronic implementation
photonic implementation
hybrid implementation
~~~

depending on:

- contract
- workload
- precision
- latency
- thermal budget
- available RU
- DesignContext
- physical state
- evidence status

This is likely to be the most practical route during early VLPI development.

---

## 23. The “new coding” test

EIS should establish a concrete test rather than debating whether AI can code for new knowledge.

### Proposed test: FIELD-CODE-001

Give a cold-start coding agent:

1. the VLPI-IR schema;
2. one field-math specification;
3. one RU contract;
4. one reference physical model;
5. one reference implementation;
6. tests;
7. a simulator interface;
8. an evidence schema.

Then ask it to implement a new field-math operation that is **not present in its repository examples**.

Success requires:

- valid VLPI-IR;
- valid RU references;
- passing schema tests;
- passing reference-model tests;
- no invented PDK parameters;
- no invented measurements;
- correct evidence classification;
- successful physics execution when authorized.

This would answer the question empirically.

The experiment should measure:

~~~
agent success rate
reference-test pass rate
physics-model pass rate
contract violations
hallucinated assumptions
human interventions
time-to-valid-implementation
~~~

That is a much stronger scientific question than asking whether an LLM “can code.”

---

## 24. The central EIS proposition

The conventional AI coding loop is approximately:

~~~
human intent
   ↓
LLM
   ↓
known programming language
   ↓
known APIs
   ↓
known hardware
~~~

The EIS target is:

~~~
human intent
   ↓
physical-computation specification
   ↓
VLPI-IR
   ↓
AI / agent
   ↓
RU composition
   ↓
CRC
   ↓
physics
   ↓
PVR
   ↓
physical artifact
   ↓
BIST
   ↓
new knowledge
~~~

The second loop is not simply “AI writing code.”

It is:

> **AI participating in the creation of executable knowledge for a new computational substrate while remaining constrained by machine-checkable contracts and physical evidence.**

---

## 25. Non-claims

This artifact does **not** claim:

- that VLPI-IR has been implemented;
- that a complete VLPI compiler exists;
- that VLPI-RT exists as a production runtime;
- that field-math libraries have demonstrated performance advantages;
- that conventional matrix libraries can be automatically translated to photonic implementations;
- that every algorithm has a useful photonic realization;
- that AI agents can currently design arbitrary VLPI transformations without human intervention;
- that RU-001 or RU-002 has demonstrated the proposed platform-level performance;
- that CO₂e/VUT advantage has been experimentally demonstrated.

These remain engineering and research objectives.

---

## 26. Initial implementation sequence

### PLATFORM-001 — Architecture
This document.

### PLATFORM-002 — VLPI-IR schema
Machine-readable intermediate representation.

### PLATFORM-003 — VLPI-IR cold-start test
GitHub2Agent reconstructs and validates an IR graph from a cold checkout.

### PLATFORM-004 — Field Math Primitive #001
First native field transformation with:

- mathematical definition;
- physical definition;
- RU mapping;
- contract;
- reference model;
- test;
- evidence schema.

### PLATFORM-005 — Field Math Library #001
Composable library with multiple verified physical transformations.

### PLATFORM-006 — Legacy Algorithm Re-expression
Take one conventional matrix-based workload and express its computational intent in VLPI-IR without assuming matrix multiplication is the target physical primitive.

### PLATFORM-007 — VLPI Compiler Prototype
VLPI-IR → CRC → RU graph → DesignContext → PVR/OASIS.

### PLATFORM-008 — VLPI-RT Prototype
State-boundary-aware scheduling and resource model.

### PLATFORM-009 — VLPI Profiler
Physical-state + thermal + evidence + CO₂e/VUT observability.

### PLATFORM-010 — AI New-Knowledge Coding Experiment
FIELD-CODE-001.

---

## 27. Architectural principle

EIS should not attempt to win by building a faster version of yesterday's software stack.

The objective is:

> **Build the software stack that makes the new physical-computation model programmable.**

The old abstraction is:

~~~
code
→ instruction
→ processor
→ memory
→ result
~~~

The proposed VLPI abstraction is:

~~~
intent
→ physical transformation
→ state
→ verified RU
→ composition
→ physical execution
→ measured useful transformation
~~~

The programming model therefore follows the physics.

Not the other way around.

---

## 28. Final answer to the six questions

### 1. What is the VLPI equivalent of a CUDA kernel?

**RU — Replicable Unit.**

A bounded, contract-governed physical transformation that can be composed into larger physical computations.

### 2. What is the VLPI equivalent of PTX/HLO?

**VLPI-IR.**

A technology-independent representation of physical states, transformations, RU composition, boundaries, constraints, resources, and evidence requirements.

### 3. What is the VLPI compiler?

**CRC → physical realization → PVR → OASIS.**

The compiler lowers physical-computation intent into a technology-constrained, verifiable physical artifact.

### 4. What is the VLPI runtime?

**A state-boundary-aware physical resource runtime.**

It schedules and manages physical computation without assuming arbitrary preemption or mandatory electronic conversion.

### 5. What is the VLPI CUDA-X equivalent?

**Verified Field Math Libraries.**

Libraries of composable physical transformations rather than merely software implementations of conventional mathematical functions.

### 6. What is the VLPI Nsight equivalent?

**Physical-state + thermal + evidence + CO₂e/VUT observability.**

The profiler must show not only execution time, but what physical state changed, what resources were consumed, what evidence supports the result, and what environmental cost was associated with useful computation.

---

## 29. Closing principle

> **EIS is not trying to put CUDA on photons.**
>
> **EIS is trying to make physical field transformation a programmable computational substrate.**

The first generation of VLPI software may use conventional CPUs, RISC-V, Python, LLVM/MLIR, existing ML frameworks, and familiar numerical libraries.

That is acceptable.

The transition occurs when those tools stop being the definition of the computation and become **front ends to a new physical-computation intermediate representation and runtime**.

The long-term objective is therefore not:

> “Can we run old code on photonics?”

It is:

> **“Can we express useful computation in a form that allows the physical substrate to perform the computation it is naturally capable of performing?”**

And the corresponding AI question is:

> **“Can an AI system learn a new computational substrate from its contracts, schemas, examples, tests, and physical evidence—and then create valid new programs for that substrate without pretending that old knowledge is the new architecture?”**

That is the experiment EIS should run.

---

## 30. External architectural references

The CUDA comparison in this document is based on NVIDIA's current public documentation describing CUDA as a programming model/platform, CUDA kernels as device code, PTX as a virtual ISA, and the CUDA driver/runtime/toolkit layers.

- NVIDIA CUDA Programming Guide: https://docs.nvidia.com/cuda/cuda-programming-guide/
- NVIDIA CUDA Programming Model: https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/programming-model.html
- NVIDIA CUDA Platform / PTX / Runtime: https://docs.nvidia.com/cuda/cuda-programming-guide/01-introduction/cuda-platform.html
- NVIDIA CUDA Toolkit documentation: https://docs.nvidia.com/cuda/

Google's current public JAX AI Stack documentation is also relevant as an example of a modern accelerator ecosystem spanning programming framework, compiler, runtime, libraries, kernels, profiling, and production deployment:

- Google Cloud JAX AI Stack: https://docs.cloud.google.com/tpu/docs/jax-ai-stack

These references establish ecosystem patterns, not evidence for EIS performance.

---

**Evidence status:** Proposed architecture / enabling technical disclosure.

**EIS rule:** No layer becomes “real” merely because this document names it. Each layer must acquire machine-readable specifications, executable tests, implementation evidence, and—where physical claims are made—physical or computational evidence appropriate to the claim.
