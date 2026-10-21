# EIS-PTC-SOI-001 — PTC Reproducibility Inventory

**Status:** Initial desk inventory; tool and PDK availability not yet verified  
**Version:** 0.1.0  
**Owner:** Earth ICT, SPC (EIS)  
**Target paper:** Tian et al., “Photonic transformer chip: interference is all you need,” *PhotoniX* 6, 45 (2025), https://doi.org/10.1186/s43074-025-00182-7  
**Purpose:** Decide the first evidence-backed experiment. This is an inventory, not a claim of reproduction.

## Four-column reproducibility inventory

| What the paper specifies | What EIS can reproduce directly in software | What requires a PDK, component model, or physical measurement | What FlexAgent can execute today with available tools |
|---|---|---|---|
| **Target architecture:** photonic transformer chip using interference-based Kramers–Kronig attention (KKA), intended to approximate standard attention without a dedicated conventional Softmax block. | Transcribe the paper's equations and data flow into a versioned, language-neutral specification; implement a Python reference; test intermediate outputs against explicit fixtures. | Confirmation that the physical network implements the intended operator requires circuit/device models and eventually measurements. Exact reconstruction also depends on sufficient published topology and parameter details. | Can help turn the inventory into tasks and structured records only if the FlexAgent runtime and relevant integrations are configured. In this ChatGPT session, no FlexAgent/FlexCompute execution endpoint is exposed, so live execution is **not verified**. |
| **Interference primitive:** paper uses field interference and a signed cross term; EIS's current scalar convention is X(a,b) = 2 Re(a conjugate(b)). | Extend the existing EIS-KKA-001 tests and compare the paper's operator against a common Python reference. Freeze conjugation, sign, factor-of-two, complex-field convention, and normalization. | Physical agreement depends on splitter ratios, phase errors, loss, coherence, detector response, and other nonidealities. These need documented models or measurements. | If tool access is confirmed, run deterministic software fixtures and pass/fail checks first. The current scalar contract alone is not a complete attention contract. |
| **Reported photonic implementation:** the paper reports a CUMEC CSiP-180AL silicon-photonics (SOI) platform, an 11-MZI-cell implementation (described as a 10×1 MZI array), MMI splitters, and TiN thermo-optic phase shifters/heaters. | Build an ideal, technology-independent graph of the disclosed topology; record known, derived, and unknown parameters separately. | A foundry-faithful layout needs the actual PDK or sufficiently complete public process data: layer map, geometry rules, component models, heater/phase-shifter models, and relevant design constraints. Do not infer missing values. | First task should be an inventory of installed PDKs, simulation APIs, license/access status, and export formats. No CUMEC PDK or FlexCompute account capability is confirmed by this inventory. |
| **Experimental task and results:** paper reports small-scale MNIST inference and compares physical results with an ideal KKA model. Its headline large-scale throughput/energy numbers are projections, not measured end-to-end LLM-system results. | Recreate the reported data-processing protocol, ideal model, metrics, and any sufficiently specified test fixtures. Clearly label values that cannot be independently recovered from the paper. | Reproducing experimental accuracy requires exact weights, data split/preprocessing, calibration, physical transfer functions, and measurement setup; any missing items must be documented. End-to-end energy claims require measured system-boundary accounting. | Agent may orchestrate tests and evidence capture only after integrations and reproducibility inputs are available. It must not label an ideal simulation as experimental replication. |
| **Device-level behavior:** phase control, splitting/combining, propagation, and detection are necessary for the functional chip. | Create abstract component interfaces and sensitivity sweeps with declared hypothetical parameters; these are useful for software exploration but are not foundry claims. | Reliable physical prediction requires characterized compact models and/or electromagnetic simulations; physical validation requires fabricated devices and measurement. | After baseline reproduction, propose bounded characterization experiments for the largest identified uncertainty; do not launch unconstrained inverse design first. |
| **Layout and manufacturability:** the chip must map to a concrete process and pass that process's constraints. | Represent hierarchy, connectivity, parameter provenance, and intended checks in a tool-independent manifest. | DRC/LVS or equivalent checks require a specific process deck and compatible layout/verification tooling. Fabrication readiness also requires packaging and I/O assumptions. | Verify whether PhotonForge, Tidy3D, KLayout, SiEPIC, and a suitable SOI PDK are actually available to EIS. Tool names alone do not establish access or compatibility. |
| **Reproducibility and provenance:** a claimed reproduction must connect equations, parameters, artifacts, simulations, and results. | Use Git, pinned versions, deterministic tests, machine-readable run manifests, and separate statuses for specified / simulated / measured. | Hardware claims require traceable instrument data, calibration, sample identity, and measurement conditions. | Once access is confirmed, have the agent generate a run manifest, invoke approved tools, capture logs/results, classify evidence, and recommend one next experiment. Until then, orchestration is a proposed workflow, not demonstrated capability. |

## Current facts versus unknowns

### Established by the target paper (desk-level extraction)
- The target is the **PTC system**, not an isolated MZI.
- The attention concept uses optical interference to approximate conventional attention without a dedicated Softmax operation.
- The reported fabrication platform is CUMEC CSiP-180AL silicon photonics / SOI.
- The paper describes an MZI-based implementation with MMI splitters and TiN thermo-optic phase control.
- The paper's small-scale task experiment must be distinguished from its projected large-scale throughput and energy figures.

### Not yet established for EIS
- Access to the exact CUMEC CSiP-180AL PDK, process design kit version, design-rule deck, compact models, or original layout.
- Whether the paper's full netlist, exact device parameters, trained weights, and all experimental preprocessing/calibration details are publicly recoverable.
- Which FlexCompute products and APIs are enabled for EIS; whether the relevant FlexAgent flow can invoke PhotonForge/Tidy3D in the EIS environment.
- Whether an accessible open SOI PDK can represent enough of the architecture for a useful proxy reproduction.
- Which original measurements can be independently recreated from public materials.

## Decision gate: choose the first experiment from evidence

**Do not begin broad optimization yet.** Complete these checks in order:

1. **Paper-to-spec extraction:** map each equation, diagram, parameter, and reported metric to a source location and classify it as explicit, derived, or unknown.
2. **Tool/PDK inventory:** confirm actual account access, APIs, PDK identities/versions, license constraints, simulation limits, and layout verification options.
3. **Software baseline:** implement the ideal attention operator and any fully specified reported test using a common Python reference; do not invent missing data.
4. **Select one branch based on the result:**
   - **Circuit-level PTC reproduction** if topology and a compatible, documented component model are available.
   - **Component characterization** if a specific device uncertainty prevents a credible circuit model.
   - **PDK enablement** if neither the original process nor a suitable open SOI baseline is accessible.

## Acceptance criteria for this inventory

- Every target-paper claim is traceable to the paper or marked as an interpretation.
- Unknown parameters remain explicitly unknown.
- The original CUMEC process is not conflated with any open-SOI proxy.
- Software, simulation, and physical evidence are separate states.
- The next experiment is selected from observed blockers, not from an assumed need to optimize.

## References

- Tian, Y. et al., “Photonic transformer chip: interference is all you need,” *PhotoniX* 6, 45 (2025). https://doi.org/10.1186/s43074-025-00182-7
- EIS-KKA-001 scalar interference contract and conformance work: https://github.com/EarthICTSPC/eis-open-vlpi-vlsi-conductor/pull/37
