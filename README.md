</> Markdown
# 🌍 EIS Open VLPI PDK
# eis-open-vlpi-pdk
Open, parameterized photonic design infrastructure with Replicable Units (RUs), CRC contracts, PVR verification, and OASIS generation.
# 🌍 EIS Open VLPI PDK

**Earth ICT, SPC — Open physical-design infrastructure for Very Large Photonic Integration (VLPI)**

[![Status: Draft](https://img.shields.io/badge/Status-Draft-orange.svg)]()
[![Version: 0.1.0](https://img.shields.io/badge/Version-0.1.0--draft-green.svg)]()
[![Schema: JSON](https://img.shields.io/badge/Schema-JSON%20Schema-blue.svg)]()
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

> **Open physical-computing infrastructure for Earth-first ICT.**

Earth ICT, SPC (EIS) is developing an open design and verification framework for very large photonic computing infrastructure — from **Replicable Units (RUs)** and physical transformation contracts through photonic design verification, OASIS realization, fabrication, and measured evidence.

This repository is the open ecosystem layer.

---

## 📖 Table of Contents

* [Overview](#-overview)
* [Why VLPI](#-why-vlpi)
* [The Replicable Unit](#-the-replicable-unit)
* [RU Contract](#-ru-contract)
* [From Physics to Fabrication](#-from-physics-to-fabrication)
* [Evidence and Verification](#-evidence-and-verification)
* [Repository Structure](#-repository-structure)
* [Current Scope: v0.1](#-current-scope-v01)
* [Quick Start](#-quick-start)
* [Schema](#-schema)
* [Reference Technology](#-reference-technology)
* [RU-001 and RU-002](#-ru-001-and-ru-002)
* [Physical Design and OASIS](#-physical-design-and-oasis)
* [Open / Controlled / Verified Boundaries](#-open--controlled--verified-boundaries)
* [Roadmap](#-roadmap)
* [Contributing](#-contributing)
* [License](#-license)
* [Acknowledgments](#-acknowledgments)
* [Contact](#-contact)

---

# 🌺 Overview

Conventional electronic and photonic design flows generally begin with components, cells, or circuits and then assemble increasingly large systems.

EIS is exploring a different abstraction for very large physical computation:

> **Define the physical transformation first. Define the state it operates on. Define the contract that makes the transformation composable. Then realize, verify, fabricate, and measure it.**

The EIS Open VLPI PDK provides the open schemas, contracts, reference models, verification interfaces, and tooling needed to express that approach.

The project is intended to support:

* **Replicable Units (RUs)**
* physical transformation contracts
* **Constraint Reduction Calculus (CRC)**
* parameterized photonic primitives
* physical-design verification
* PVR: Photonic Verification and Realization
* PDR: Photonic Design-Rule Verification
* PCT: Photonic Connectivity and Topology Verification
* PTV: Physical Transformation Verification
* OASIS physical-design output
* Paper2Agent-to-layout workflows
* foundry-specific realization through controlled adapters
* post-fabrication BIST and measured evidence
* wafer-scale and stacked-wafer composition
* open multi-foundry ecosystem development

The goal is **not** to prescribe one photonic architecture or one foundry process.

The goal is to establish an open language in which independently developed physical transformations can become **composable, reproducible, verifiable infrastructure**.

---

# 🌎 Why VLPI?

Photonic integration is often discussed in terms of individual devices, PICs, optical links, or photonic accelerators.

VLPI asks a larger question:

> **What happens when photonic computation is treated as infrastructure rather than as a collection of individual photonic chips?**

At sufficient scale, the design problem includes:

* physical transformation
* state representation
* optical connectivity
* replication
* thermal behavior
* electrical interfaces
* fabrication constraints
* verification
* measurement
* yield
* packaging
* wafer-scale composition
* stacked-wafer composition
* useful computational service

EIS therefore treats the physical design artifact as part of a larger evidence chain:

```text
Physical hypothesis
        ↓
Physical state
        ↓
RU contract
        ↓
Candidate transformation
        ↓
CRC constraint reduction
        ↓
Physics simulation
        ↓
PDK-constrained realization
        ↓
PVR
        ↓
OASIS
        ↓
Foundry review
        ↓
Fabrication
        ↓
BIST / State Boundary measurement
        ↓
Replication evidence
        ↓
Useful computational service
```

This repository concentrates on the **open infrastructure required to make that chain machine-readable and reproducible**.

---

# 🔁 The Replicable Unit

The **Replicable Unit (RU)** is a foundational abstraction of the EIS-VLPI architecture.

However, an RU is **not simply a photonic standard cell**.

An RU is defined by the physical transformation it performs, the state it operates upon, the conditions under which that transformation is accepted, and the evidence supporting its realization.

An RU can therefore be understood as:

> **A bounded, composable physical computation whose transformation, state, contract, realization, verification, and replication evidence are explicitly represented.**

The RU abstraction separates:

1. **What physical transformation is required**
2. **What physical state enters and leaves**
3. **What constraints must be satisfied**
4. **How the transformation is realized**
5. **What evidence supports the realization**
6. **How the unit may be composed and replicated**

---

## RU Definition → Instance → Composition

The earlier three-level concept remains useful, but EIS treats it as part of a larger contract/evidence model.

```text
                 RU Definition
          (transformation + state + contract)
                         │
                         │ instantiate
                         ▼
                    RU Instance
          (specific physical realization)
                         │
                         │ compose
                         ▼
                  RU Composition
        (verified physical transformations)
                         │
                         ▼
                Wafer / Stack / VLPI
```

The geometry of an RU is therefore **not universally fixed**.

A particular RU may occupy 500 × 500 µm, 1 × 1 mm, or another bounded physical region depending on the technology and transformation.

Geometry is an implementation property.

The **contract is the invariant**.

---

# 🧮 RU Contract

The current EIS working abstraction is:

$$
\boxed{
S_{RU}=(H,T,R,B,G,C)
}
$$

where:

| Symbol | Meaning                         |
| ------ | ------------------------------- |
| **H**  | Physical field/state space      |
| **T**  | Physical Transformation Mapping |
| **R**  | Constraint Reduction operator   |
| **B**  | State-Boundary acceptance       |
| **G**  | State-to-field regeneration     |
| **C**  | Machine-checkable contract      |

This model deliberately avoids assuming that photonic computation is inherently a conventional matrix multiply, Boolean gate, or electronic MAC.

A photonic RU may exploit the physical behavior already present in the device — including interference, field superposition, resonance, phase, amplitude, propagation, coupling, or other physical transformations.

The abstraction begins with the **physical transformation**, not with an imposed electronic computing metaphor.

---

# 🧠 Constraint Reduction Calculus

EIS uses **Constraint Reduction Calculus (CRC)** as a framework for reducing the physical search space before expensive physics simulation.

The objective is not to replace physics simulation.

It is to ask:

> **Can physical constraints eliminate unsuitable candidates before full-wave computation is required?**

Conceptually:

```text
Design space
     │
     ▼
CRC constraints
     │
     ├── reject impossible candidates
     │
     ├── reject contract-incompatible candidates
     │
     └── retain physically plausible candidates
                     │
                     ▼
                EM / FDTD
                     │
                     ▼
              physical evidence
```

A central research metric is:

$$
\eta_{CRC}
=
1-
\frac{N_{FDTD,CRC}}
     {N_{FDTD,baseline}}
$$

with preservation of solution quality evaluated separately.

CRC is therefore an **optimization and search-space reduction hypothesis**, not a substitute for physical validation.

---

# 🔬 Evidence and Verification

EIS distinguishes different kinds of evidence.

A schema or Lean proof can establish that a logical contract is internally consistent.

It does **not** establish that a fabricated photonic device physically works.

Accordingly, EIS uses explicit evidence states.

| Evidence state                 | Meaning                                           |
| ------------------------------ | ------------------------------------------------- |
| `draft`                        | Concept or incomplete definition                  |
| `specified`                    | Contract and required behavior formally specified |
| `computationally-demonstrated` | Supported by computational experiment             |
| `experimentally-demonstrated`  | Supported by experimental demonstration           |
| `measur                        |                                                   |
</> Markdown
**Earth ICT, SPC**

*Open physical-computing infrastructure for an Earth-first ICT future.*

🌍 **A hui hou.**
