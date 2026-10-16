# RU-002: Photonic DeepSeek — Candidate Architecture and Interface Hypotheses

**Project:** Earth ICT, SPC (EIS)  
**Status:** `proposed-hypothesis`  
**Evidence class:** literature-derived hypothesis; not an EIS simulation, measurement, or demonstrated system  
**Scope:** candidate composition of optical cache/state access, Kramers–Kronig activation (KKA), programmable optical thresholding, and an open LLM model such as DeepSeek.

## 1. Hypothesis

A useful subset of an open LLM's inference path may be implemented as a composition of photonic physical transformations in which the information-bearing state remains optical between the cache, activation, and threshold/selection units. The candidate composition is called **Photonic DeepSeek**.

The initial hypothesis is not that the entire DeepSeek model is already photonic, nor that these three device mechanisms alone implement an LLM. It is that an open model's weights, operations, state representation, and control flow can be mapped onto a heterogeneous photonic substrate while preserving defined optical interfaces between selected RUs.

The three literature strands are:

1. **Optical cache / state access:** the cache paper selected by EIS (citation and exact claimed mechanism to be pinned in the evidence manifest before quantitative use).
2. **Programmable optical thresholding:** Huang et al., “Programmable Silicon Photonic Optical Thresholder,” arXiv:1908.07067, DOI: https://doi.org/10.1109/LPT.2019.2948903.
3. **Kramers–Kronig activation (KKA):** the KKA paper selected by EIS; a related published reference is Tian et al., “Photonic Neural Networks with Kramers–Kronig Activation,” *Advanced Photonics Research* (2023), DOI: https://doi.org/10.1002/adpr.202300062.

The exact cache and KKA citations, version, and paper-to-requirement mapping must be recorded before treating the literature review as complete. This document intentionally does not invent a cache citation or assert that one KKA implementation is the only viable implementation.

## 2. Thresholding mechanism extracted as an RU hypothesis

### Source-derived mechanism

Huang et al. report an all-optical programmable thresholder using the power-dependent nonlinear response of a resonator-enhanced Mach–Zehnder interferometer (MZI). The nonlinear phase shift in the resonator changes the interferometric output transfer function, producing a steep power-discrimination response. Their SOI implementation experimentally reports discrimination at a power contrast ratio as low as 1.13, 40× signal-contrast enhancement, a five-orders-of-magnitude bit-error-rate improvement, and an 11 dB receiver-sensitivity improvement. These are results reported for their device and test conditions, not EIS results.

Reference: https://arxiv.org/abs/1908.07067

### Candidate RU-THRESHOLD-001

**Transformation hypothesis:** for an input optical state carrying a scalar or locally recoverable feature (x), the RU produces an optical output state whose measured observable implements a configured threshold/contrast transfer function (y=f_θ(x)). The parameter (θ) identifies the threshold operating point and associated physical configuration. The function, observable, and valid operating region must be defined for each realization; no universal ideal step function is assumed.

**Mechanism candidate:** resonator-assisted MZI, with a power-dependent resonant phase response and interferometric transfer. Alternative technology-compatible mechanisms may be considered only as separately identified candidates; they must not inherit the SOI paper's results.

**EIS target technology:** to be evaluated against the selected EIS PDK and stack, including the intended SiN/TFLN path where appropriate. The paper's SOI nonlinear coefficients, carrier dynamics, losses, operating powers, response time, and measured contrast are not portable assumptions.

### Operating conditions to record

A candidate is not simulation-ready until its DesignContext specifies:

- PDK identity, revision, permitted device stack, and model provenance;
- carrier wavelength(s), optical input-power range, and power reference plane;
- input encoding and the physical observable that represents (x);
- resonator geometry and coupling, MZI topology, phase bias, and tuning mechanism;
- temperature range, optical loss budget, parasitic/reflection assumptions, and relevant noise sources;
- dynamic regime and pulse/modulation conditions;
- threshold setting method, calibration procedure, hysteresis/reset behavior if present, and allowed settling time;
- target transfer curve, contrast definition, insertion loss, extinction ratio, latency, energy per operation, and error/false-decision metrics.

Numerical values remain **TBD by the selected PDK, model, and workload**; they must not be copied from the SOI demonstration merely to fill fields.

## 3. The always-photonic interface principle

The key architecture question is not only whether each block can perform its function optically. It is whether the **information-bearing state crosses from one RU to the next as a compatible optical state**, without an intervening optical-to-electrical-to-optical (O-E-O) conversion.

The RU interface contract must define the following fields without forcing every implementation into one physical encoding:

- **Optical domain:** wavelength band(s), mode/polarization/spatial or time-slot assumptions, and allowed conversion between domains.
- **State meaning:** the semantic object being carried (for example, cached value/state, activation-bearing feature, or threshold/selection result), with dimensions and ordering.
- **Encoding:** which optical observables carry the state, their normalization/reference planes, dynamic range, phase convention where applicable, and calibration identity.
- **Validity:** admissible range, saturation/overflow behavior, invalid-state signaling, and loss/noise tolerance.
- **Timing:** launch/arrival convention, latency budget, synchronization, buffering, and state lifetime.
- **Physical continuity:** an explicit declaration of whether the data path remains optical across the boundary. Any O-E-O crossing must be named, justified, measured, and counted; it cannot be hidden inside an adapter.
- **Control plane:** electrical configuration, bias, calibration, thermal control, and monitoring may be used where necessary, but are distinguished from the information-bearing data path. The hypothesis does not assume all control electronics can be eliminated.
- **Evidence/provenance:** source RU contract, DesignContext, PDK/model version, transformation configuration, and hashes for input/output artifacts and results.

### Interface contract candidates

| Interface | Optical state carried | Required acceptance condition |
|---|---|---|
| Cache → activation | Selected/retrieved state or feature in a defined optical encoding | Cache result is valid, aligned, normalized, and remains optical at the RU boundary |
| Activation → threshold/selection | Activation-bearing optical state plus its defined reference/scale | Transfer function is characterized over the declared range; no implicit electrical decision is substituted |
| Threshold/selection → next LLM operation | Optical state encoding the accepted/rejected or graded result | Decision semantics, contrast, error rate, and downstream encoding are contract-compatible |
| RU → RU (general) | Versioned optical-state contract | Domain, meaning, timing, validity, and optical continuity match at both ends |

These are semantic interfaces, not a claim that all devices can connect directly without wavelength conversion, amplification, regeneration, or routing. Each such operation is an explicit RU with its own loss, energy, latency, noise, and evidence contract.

## 4. Candidate composition

The initial architecture should remain a hypothesis graph, not a frozen assumption about layer order:

```
Open LLM model + weights + workload
              |
              v
      workload/state mapping
              |
              v
    optical cache / state-access RU
              |
        optical-state contract
              |
              v
       KKA activation RU
              |
        optical-state contract
              |
              v
    optical threshold / selection RU
              |
        optical-state contract
              |
              v
   next photonic operation / RU / mesh
```

The order is a testable starting arrangement, not a universal requirement. The model graph and workload determine where cache access, activation, and thresholding are mathematically appropriate. If evidence supports a different order or a different threshold location, revise the composition with a versioned hypothesis and tests.

“Open LLM” identifies the model/software and weight licensing/provenance layer; it does not mean the model executes optically by itself. The mapping must account for the selected model's actual operators, weights, precision, state, control-flow decisions, and unsupported operations. Unsupported operations may initially remain in an explicitly bounded electronic control/compute island, but their crossings and costs must be measured rather than described as always-photonic.

## 5. Acceptance and evidence plan

Evidence is collected independently at each layer.

### A. Contract and semantic conformance

- Define input/output state meaning and encoding for each RU.
- Check unit, dimension, scale, phase, and wavelength assumptions at interfaces.
- Prove contract-level invariants in Lean where expressible; label assumptions and trusted boundaries.
- Generate shared conformance vectors from the normative contract and replay them in Python and Rust implementations.
- Reject mismatched domain, missing calibration, unsupported units, out-of-range values, and unpinned PDK/model identities.

### B. Numerical/device evidence

For the threshold RU, establish a PDK-specific model and sweep the declared input range, bias/phase setting, temperature, wavelength, and relevant device tolerances. Report the complete transfer curve, not just a best-case contrast number. Include insertion loss, threshold repeatability, sensitivity to drift, dynamic response, energy, noise, and error statistics.

For KKA and cache RUs, record the actual mechanism and paper-derived hypotheses separately from device-specific models. Do not infer end-to-end LLM accuracy from component curves alone.

### C. Composition evidence

- Test every RU-to-RU optical interface against its contract.
- Track optical power/loss and signal quality through the entire composed path.
- Identify and count every O-E-O conversion, electrical control boundary, regeneration event, and wavelength/mode conversion.
- Compare the photonic path with a specified electronic/reference baseline on the same workload and quality criterion.
- Report unsupported operations, fallback paths, end-to-end latency, energy, error/quality metrics, and all model/PDK/tool versions.

### D. Physical measurement

After fabrication, bind measurements to the exact die/device, wafer/process identity where available, calibration instruments, temperature, optical powers, wavelength, configuration, raw-data hashes, and analysis version. Simulation and Lean proof cannot substitute for this evidence.

### Evidence state

Until those stages are performed, RU-THRESHOLD-001 and the Photonic DeepSeek composition remain `proposed-hypothesis`. The paper's SOI results are literature evidence only. No EIS-specific performance, fully photonic LLM execution, energy advantage, or fab readiness is claimed.

## 6. First falsifiable experiment

Before attempting an end-to-end LLM, evaluate the threshold RU as a standalone transformation under one selected target PDK.

1. Freeze the input observable, target transfer function, operating range, and acceptance metrics.
2. Establish the best available PDK-specific compact/electromagnetic model and its provenance.
3. Sweep the threshold operating point and declared environmental/process variations.
4. Measure whether the candidate can meet the predeclared contrast/error, insertion-loss, latency, and energy budgets simultaneously.
5. Compare the output encoding with the next RU's input contract without an O-E-O conversion.
6. Record failure as valid evidence if no candidate meets all requirements.

Only after this gate should the cache → KKA → threshold composition be tested, followed by a small open-LLM workload slice. This ordering tests the physical interface premise before scaling the model.

## 7. Non-claims and decision gates

This proposal does **not** claim:

- that the SOI thresholder transfers unchanged to SiN/TFLN;
- that KKA, cache access, thresholding, and all LLM operations already compose in a real photonic device;
- that every LLM operation can be performed photonic-only;
- that the optical data path is lossless or needs no regeneration;
- any EIS-specific speed, energy, contrast, accuracy, yield, or CO₂e improvement;
- that a model being open-source implies unrestricted rights to all weights, training data, or derivative uses.

Advance the hypothesis only when the relevant contract, tool/model provenance, and evidence gate pass. The primary success criterion is a useful computational service with a measured, traceable optical data path—not photons used for their own sake.
