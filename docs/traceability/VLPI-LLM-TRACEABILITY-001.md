# VLPI-LLM-TRACEABILITY-001: Informal Intent to Physical Acceptance

**Status:** Proposed engineering traceability artifact  
**Owner:** Earth ICT, SPC (EIS)  
**Depends on:** EIS-LEAN4-001; EIS-CRC-BUDGET-001  
**Scope:** Establish a traceable acceptance path. This document does not claim production dispatch enforcement or physical conformance.

## 1. Governing objective

Establish a reproducible chain from an informal VLPI LLM specification to:
1. a reviewed, versioned Lean 4 contract;
2. one or more executable realizations (for example Python prototype, Rust production service, and photonic design artifacts);
3. verification and test evidence tied to those exact revisions;
4. simulation and measured fabrication evidence tied to an identified PDK/device and test conditions; and
5. an explicit production acceptance decision against declared criteria.

The loop is closed only for the declared workload and operating envelope. Evidence must be invalidated or reviewed when a relevant specification, implementation, PDK, device, workload, or operating-condition change occurs.

## 2. Traceability chain

| ID | Artifact / activity | Required record | Acceptance condition | Current status |
|---|---|---|---|---|
| T-01 | Informal intent | Human/LLM requirement text, author/reviewer, version, unresolved ambiguities | Requirements reviewed; ambiguities and assumptions visible | To be established |
| T-02 | Requirement ledger | Stable requirement IDs; semantic meaning; inputs/outputs; performance and safety/environmental constraints | Every requirement has an owner, rationale, and measurable acceptance rule or is explicitly non-testable | To be established |
| T-03 | Lean 4 contract | Definitions, types, preconditions, postconditions, invariants, theorem assumptions | CI builds; required proofs compile; assumptions are reviewed and not misrepresented as conclusions | Lean foundation exists; VLPI-LLM contract not yet specified |
| T-04 | Contract-to-implementation map | Requirement IDs mapped to Lean declarations and Python/Rust/hardware artifacts | No required item is untraced; unproven implementation correspondence is explicitly marked | To be established |
| T-05 | Executable prototype | Versioned Python implementation, test vectors, expected results, deterministic run instructions | Tests exercise actual implementation paths and relevant edge cases | Not established for a complete VLPI LLM |
| T-06 | Production implementation | Versioned Rust/software and interfaces where selected; build provenance; conformance tests | Required tests pass; production dispatch paths enforce relevant gates | Not established |
| T-07 | Photonic design | PDK identity/version, design parameters, layout/netlist hashes, DRC/LVS outputs | Design artifacts bind to the declared PDK and pass applicable checks | Not established for complete VLPI LLM |
| T-08 | Simulation evidence | Simulator/version, model and PDK revision, configuration, seeds, raw outputs, analysis | Results are reproducible and meet declared pre-silicon criteria | No physical validation claimed by budget fixture |
| T-09 | Fabrication and measurement | Device/wafer/lot identity, test setup, calibration, environmental conditions, raw data, uncertainty, acceptance criteria | Attributable measurements meet the declared physical contract | Not established |
| T-10 | Release decision | Traceability report, exceptions, signed approvals, artifact hashes | All mandatory software, formal, and physical gates pass for the declared envelope | Not ready for acceptance |

## 3. Typed interface minimum

Each computational interface shall declare:
- semantic type and meaning;
- representation domain (for example electronic digital, electronic analog, optical field, optical power);
- physical quantity, shape, units where applicable, precision;
- preconditions, validity conditions, and postconditions;
- provenance and version identity;
- explicit typed transformations for representation changes.

Semantic meaning and physical representation are distinct. Semantically digital information may be encoded in an in-flight optical field; this does not imply an electronic representation. Any actual O/E/O transition must be an explicit, declared boundary. CRC should reject incompatible compositions before expensive physical simulation.

Lean 4 can prove properties of the encoded formal model. Such proofs do not establish that the model fully captures human intent, that a Python/Rust implementation refines it, or that a fabricated device conforms. Each claim needs its own evidence.

## 4. Shared latency fixture: exact interpretation

The file fixtures/EIS-CRC-BUDGET-001.json is a **synthetic serial-additive software regression**, not a measured KKA timing result.

| Stage | Fixture latency | Cumulative latency |
|---|---:|---:|
| DAC | 10 ps | 10 ps |
| Modulator | 5 ps | 15 ps |
| PRISM | 40 ps | 55 ps |
| Thresholder | 30 ps | 85 ps |
| KKA | 120 ps | 205 ps |
| Photodetector | 15 ps | 220 ps |
| ADC | 8 ps | 228 ps |

Under this fixture's declared serial-additive model, the budget is 200 ps. The cumulative total is 228 ps, exceeding the budget by 28 ps (14%). KKA is the first stage at which the cumulative total exceeds the budget: 205 ps, 5 ps over. The reference gate therefore rejects before invoking its callback.

This proves the regression's arithmetic and reference-gate behavior under the specified model. It does not prove that an actual photonic KKA takes 120 ps, that a real orchestrator enforces the gate, or that a physical system has 228 ps latency. A pipeline with overlap, parallel execution, queueing, or a different timing boundary requires an explicit timing model and new fixture.

## 5. Photonic KKA versus conventional digital KKA: comparison protocol

**Do not treat 200 ps as a universal digital-KKA budget or as a demonstrated photonic advantage.** The current fixture supplies a proposed system budget and synthetic stage values. A defensible comparison must measure or model both alternatives for the same useful computational service.

Before comparing, define the KKA operation precisely (input shapes, attention/reasoning function, precision, quality target, batch/concurrency, and output contract). Then record at least:

| Comparison dimension | Photonic KKA path | Conventional digital KKA path |
|---|---|---|
| Start/end boundary | Declare whether timing starts at optical input, after modulation, or at KKA invocation; define output boundary | Use equivalent logical start/end boundaries; include relevant memory and interconnect movement |
| KKA service latency | Measured or validated simulated latency, with distribution and conditions | Measured latency on named processor/system, with distribution and conditions |
| Conversion overhead | Include DAC/modulator and detector/ADC only if inside the declared service boundary; otherwise report separately | Include host/device transfers and memory movement when inside the same boundary |
| Queueing and concurrency | State load, parallelism, contention, and calibration assumptions | State batch size, utilization, batching, contention, and accelerator configuration |
| Useful-work quality | Same task-level output quality/accuracy and acceptance test | Same task-level output quality/accuracy and acceptance test |
| Energy | Measure/report boundary, instrumentation, and amortized calibration/control energy | Measure/report comparable wall/system energy and memory/interconnect energy |
| Evidence level | Separate analytic estimate, device simulation, fabricated-device measurement | Separate published estimate, benchmark, and directly measured result |

Report end-to-end latency and KKA-only latency separately. A photonic core's propagation time is not the same as the useful service's latency. Likewise, a digital KKA's arithmetic latency alone is not comparable with a photonic path that includes encoding, conversion, calibration, and output selection.

### Required comparison result

For each candidate, publish:
- exact workload and output-quality acceptance;
- hardware/device, PDK, firmware/software, and compiler versions;
- boundary diagram and timing model;
- median and tail latency (such as p95/p99) under stated load;
- energy per accepted useful result and measurement boundary;
- repeatability, uncertainty, and exclusions;
- raw data or reproducible benchmark instructions.

Until these records exist, the only justified statement is: **the synthetic fixture rejects a 228 ps serial-additive path against a 200 ps budget at KKA before reference callback dispatch.** No conclusion about photonic-versus-digital superiority follows from that fixture alone.

## 6. Acceptance gates

- **G1 — Intent/specification review:** requirement ledger reviewed; assumptions and open questions explicit.
- **G2 — Formal contract:** Lean project builds; required theorems prove the stated properties; assumptions reviewed.
- **G3 — Executable correspondence:** implementations are mapped to requirements and pass tests; any unproven refinement gap is disclosed.
- **G4 — Production enforcement:** real dispatch entry points route through required gates; integration tests prove rejected work causes no forbidden side effects.
- **G5 — Design/simulation:** exact PDK/device identity and reproducible design/simulation evidence meet pre-silicon criteria.
- **G6 — Physical conformance:** attributable measurements from fabricated hardware satisfy the physical contract, with uncertainty and test conditions recorded.
- **G7 — Production release:** all mandatory gates are accepted and exceptions are resolved or explicitly approved within a defined scope.

A pass at one gate never implies a pass at a later gate.

## 7. Immediate next actions

1. Create the first versioned VLPI-LLM requirement ledger from the informal specification; mark every unmeasured performance number as a target, assumption, estimate, or measurement.
2. Define the first narrow useful-service contract in Lean 4 before attempting a broad LLM formalization.
3. Map each contract clause to a Python reference implementation and executable test vectors.
4. Identify or create the real orchestration/pre-dispatch entry point; route every relevant FlexAgent/FlexCompute dispatch path through the budget/contract gate and test the actual side-effect boundary.
5. Define a matched conventional digital KKA baseline before claiming latency or energy advantage.
6. Bind physical simulations and future fab measurements to the same contract IDs and versioned artifact identities.

**Non-claims:** This document does not establish that a complete VLPI LLM has been formally specified, that production dispatch is gated, that a photonic KKA meets 200 ps, that conventional digital KKA does or does not meet 200 ps, or that any physical device has passed conformance.

## 8. Market competition requirement: AI service tiers

The 200 ps target is a **market-competition requirement**, but it must be scoped to a defined service tier and timing boundary before it becomes an enforceable acceptance criterion. Model parameter count is a useful descriptor, not a sufficient workload specification: architecture (dense/MoE), active parameters, context length, output length, precision, batching, concurrency, and quality target all affect the work.

The ranges below are **proposed EIS planning bands, not an industry standard**. They are intended to organize market comparisons and should be refined against the first chosen workload and customer use case.

| EIS planning tier | Indicative model scale (parameters) | Example service class | Required benchmark emphasis |
|---|---:|---|---|
| Small / edge | Up to about 10B | Local assistant, classification, extraction, compact coding/reasoning | Single-request latency, memory footprint, joules per accepted result |
| Medium / general purpose | About 10B–70B | General assistant, retrieval-augmented generation, coding assistance | Time to first token, decode throughput, context sensitivity, energy per request |
| Large / high capability | About 70B–200B | Complex coding, longer-context assistance, more demanding reasoning | Tail latency, concurrency, memory movement, energy and cooling under sustained load |
| Frontier | Above about 200B effective/total scale, or a leading-capability model regardless of size | Frontier reasoning, agentic and long-horizon tasks | Same-quality useful work, long-reasoning cost, sustained throughput, facility and thermal limits |

Parameter ranges are not sufficient to classify mixture-of-experts systems; EIS should record both total and active parameters when known. Frontier is also a capability category, not strictly a parameter-count category. A smaller model may be frontier-capable on a particular task, while a large model may not be state of the art.

Market evidence reinforces the need to compare the *same useful service*: Stanford's AI Index reports that smaller models have improved substantially, while energy estimates vary widely by model and inference mode. A 2026 analysis reports materially higher energy for long reasoning than standard queries. These sources motivate measurement; they do not establish EIS hardware performance:
- Stanford HAI, [AI Index 2025: State of AI in 10 Charts](https://hai.stanford.edu/news/ai-index-2025-state-ai-10-charts).
- Stanford HAI, [AI Index Report 2026 — Energy and Environmental Impact](https://hai.stanford.edu/assets/files/ai_index_report_2026.pdf).
- Oviedo et al., [Energy use of AI inference, efficiency pathways, and test-time scaling](https://www.sciencedirect.com/science/article/pii/S2542435126001145), 2026.

### Define the 200 ps requirement at the right level

A 200 ps (0.2 ns) target is so short that EIS must explicitly state what event begins the clock and what event ends it. It may be a **subsystem or KKA-stage deadline**, rather than a full LLM request/response deadline. A complete LLM service includes many sequential or iterative operations and cannot be represented by a single KKA-stage timing number.

For the first acceptance record, specify:
1. **Tier and workload:** model/architecture, total and active parameters where applicable, input/context distribution, output or decision contract, precision, batch size, and concurrency.
2. **Service boundary:** named start and stop events; identify which encoding, memory, routing, conversion, calibration, and control costs are inside or outside the budget.
3. **Latency metric:** distinguish KKA-stage latency, request latency, time to first token, inter-token latency, throughput, and tail latency. Do not substitute one for another.
4. **Quality floor:** the same task-level correctness/quality acceptance for photonic and digital candidates.
5. **Thermal/energy budget:** define energy per accepted useful result, average and peak power, sustained thermal state, cooling/control overhead, and the operating environment.
6. **Market baseline:** identify the conventional digital implementation and benchmark version against which the requirement is competitive.

The 200 ps requirement should initially be recorded as a **system-level market target whose exact scope is pending tier/workload definition**. The fixture's 200 ps value is its explicit test budget. These statements are compatible: the fixture tests rejection logic, while the market requirement must be bound to a concrete service before performance claims are made.

## 9. EIS thermal-budget hypothesis and overlap/parallelism

**EIS hypothesis:** a cool VLPI implementation may improve useful computation per joule and reduce thermal-management overhead relative to a conventional VLSI implementation. This is a research hypothesis, not yet a demonstrated result. Optical propagation does not mean zero energy, zero heat, or zero thermal control: lasers, modulators, phase control, detectors, electronic control, memory, and conversion may all contribute energy and heat.

The architecture may permit parallel execution and/or stage overlap. The model must not assume that every stage is serially additive, but it also must not assume overlap is free or feasible. For each proposed parallel/overlapped path, declare:
- dependencies and which operations can execute concurrently;
- resource conflicts, fan-out, synchronization, phase/calibration requirements, and data availability;
- stage service times versus queueing and transfer times;
- whether the measured quantity is critical-path latency or sum of component latencies;
- power and thermal behavior during concurrency, including peak loads;
- output correctness and repeatability under the same workload.

For a strictly serial pipeline, total latency is the sum of stage latencies. For a dependency graph with parallel work, latency is governed by the scheduled critical path plus relevant synchronization, queueing, and interface costs—not the simple sum of all stage latencies. Energy generally still accounts for the energy of all executed operations, even when they overlap in time. Lower latency therefore does not automatically mean lower energy or lower peak temperature.

### Required experiment matrix

| Experiment | Hypothesis under test | Measure | What would count as evidence |
|---|---|---|---|
| A. Serial reference | Reproduce the current fixture and its first-exceed rejection | Per-stage values, cumulative arithmetic, gate outcome | Deterministic software regression only |
| B. Dependency/critical-path model | Some stages can overlap without violating data dependencies | Schedule, critical path, synchronization overhead | Reproducible model with declared assumptions; not physical validation |
| C. Parallel candidate | Concurrent photonic operations improve latency for the same accepted result | End-to-end and KKA latency, throughput, error/quality, peak power | Simulation or measurement tied to a named design and workload |
| D. Thermal/energy comparison | VLPI reduces energy and/or thermal-management cost relative to digital baseline | Joules per accepted result, average/peak power, temperature, cooling/control energy | Matched-boundary, matched-quality data with uncertainty |
| E. Fabricated-device validation | The actual PDK/device meets the formal physical contract | Measured latency, loss, error, power, drift, temperature and operating envelope as applicable | Attributable wafer/device data and passed acceptance criteria |

The existing 228 ps fixture must remain unchanged as the **serial-additive reference regression**. A parallel/overlapped candidate should be a separate fixture with an explicit dependency graph and separately justified stage values. Do not alter the original fixture simply to make it pass.

## 10. Revised next engineering sequence

1. **Freeze the market requirement definition:** retain 200 ps as a competition target, then specify the first tier, useful KKA operation, timing boundary, output-quality floor, and whether 200 ps applies to KKA-only or end-to-end service.
2. **Create the requirement ledger:** classify every number as target, assumption, model estimate, simulation result, or physical measurement. Include a thermal/energy budget beside latency.
3. **Formalize in Lean 4:** express typed stage contracts, timing semantics, dependency/parallelism assumptions, rejection conditions, and energy/thermal quantities where units and models are sufficiently defined.
4. **Preserve the serial fixture:** keep its 228 ps total and KKA first crossing at 205 ps as a regression for the serial-additive model.
5. **Build a separate overlap model:** represent dependencies explicitly and compute critical-path latency; state what the model omits and do not call it physical validation.
6. **Enforce at the real dispatch boundary:** identify the production orchestrator, route every relevant dispatch path through the contract gate, and test that rejected operations produce no forbidden side effects.
7. **Benchmark a matched digital baseline:** same KKA service, quality, timing boundary, concurrency, and declared system overhead.
8. **Validate against the actual PDK and fabricated devices:** bind simulation and measurement records to design/device identity and acceptance criteria before claiming competitive advantage.

**Updated non-claim:** Neither a 200 ps photonic KKA nor a 200 ps conventional digital KKA has been established by the synthetic fixture. The thermal advantage and feasibility of parallelism/overlap remain explicit EIS hypotheses to test.