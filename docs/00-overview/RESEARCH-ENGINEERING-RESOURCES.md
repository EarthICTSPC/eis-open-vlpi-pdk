# EIS Open VLPI — Research & Engineering Resources

This page collects public resources useful to the openLLM-GitHub2VLPI program. They are grouped by role so reviewers can distinguish scientific references, execution infrastructure, formal methods, and future physical embodiment.

## Scientific / photonic-computing references

### Photonic transformer chip: interference is all you need

Springer Nature / PhotoniX (2025):
https://link.springer.com/article/10.1186/s43074-025-00182-7

Relevant external reference for interference-based photonic transformer computation. It reports a silicon photonic transformer chip using an optical-interference attention mechanism and discusses MZI and MRR photonic computing approaches.

**EIS use:** external scientific reference and future embodiment input. It is intentionally **not an Experiment A input**.

### PRISM — Photonic Similarity Engine for KV Cache Block Selection in Long-Context LLM Inference

arXiv:
https://arxiv.org/html/2603.21576v2

Relevant external reference for future photonic LLM/KV-cache work and later embodiment experiments. It is intentionally **not an Experiment A input**.

## Agent / execution infrastructure

### Model Context Protocol (MCP)

Official site:
https://modelcontextprotocol.io/

**EIS use:** machine-discoverable and machine-executable interface between agents and external tools/services.

### FlexCompute / FlexAgent

FlexAgent:
https://www.flexcompute.com/resources/ai-agent/

PhotonForge:
https://www.flexcompute.com/photonforge

FlexCompute:
https://www.flexcompute.com/

**EIS use:** physics-aware agent execution, photonic simulation, optimization, PDK-aware design, verification, and eventual Experiment B/C integration.

### GitHub2VLPI

EIS Open VLPI PDK:
https://github.com/EarthICTSPC/eis-open-vlpi-pdk

**EIS use:** open coordination, reproducibility, evidence publication, and the bridge between open LLM/agent workflows and VLPI design/verification.

## Photonic fabrication / technology

### LIGENTEC

https://www.ligentec.com/

**EIS use:** preferred future SiN/TFLN fabrication ecosystem and controlled PDK boundary for EIS physical embodiments.

LIGENTEC describes low-loss integrated photonics based on silicon nitride, with TFLN and III-V heterogeneous integration options, and supports MPW, dedicated runs, design/layout assistance, and testing.

**Important:** LIGENTEC-specific controlled PDK contents do not belong in the open repository unless publication is authorized.

## Open hardware / I/O

### RISC-V International

https://riscv.org/

Ratified specifications:
https://docs.riscv.org/

**EIS use:** candidate open processor/I/O/control layer for concrete VLPI embodiments. RISC-V is an implementation/system resource, not an Experiment A ontology primitive.

## Formal methods

### Lean 4

https://lean-lang.org/

Theorem Proving in Lean 4:
https://lean-lang.org/theorem_proving_in_lean4/

**EIS use:** machine-checkable contracts, formal state/transition properties, verification artifacts, and later proof boundaries.

## EIS research repositories

### Art Scott — reversible photonic computing

https://github.com/Art/reversible-photonic-computing

### ORCID — Art Scott

https://orcid.org/0000-0002-4353-5561

ORCID: **0000-0002-4353-5561**

## Resource-use rule

External resources do not automatically become EIS architecture.

A resource may be:
- **reference** — scientific context;
- **tool** — execution support;
- **technology** — physical embodiment;
- **formal method** — verification machinery;
- **future experiment input** — deliberately introduced later.

Experiment A is intentionally insulated from the photonic embodiment resources above.

## Preferred EIS embodiment — future Experiment B

EIS expects eventually to demonstrate a complete worked embodiment, potentially including:

    abstract transformation
            ↓
    photonic interference
            ↓
    SiN + MRR embodiment
            ↓
    control / I/O
            ↓
    PDK-specific design
            ↓
    DRC / LVS / BIST
            ↓
    OASIS
            ↓
    fabrication boundary

This is an **embodiment example**, not a claim that SiN + MRR is the only valid realization.

The open GitHub architecture is intended to support many PIC/VLPI projects and technology supply chains. A project becomes concrete when its abstract contracts are instantiated against a selected technology, PDK, physical geometry, verification flow, and fabrication process.
