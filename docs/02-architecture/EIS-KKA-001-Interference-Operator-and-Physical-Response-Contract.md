# EIS-KKA-001 — Interference Operator and Physical-Response Contract

**Owner:** Earth ICT, SPC (EIS)  
**Status:** Proposed; not formally verified or physically validated  
**Parent:** EIS-REBOOT-001 / EIS-SOFTMAX-001

> **Evidence boundary:** This contract specifies a testable model. It does not establish that KKA is valid on EIS's intended SiN/TFLN platform, that its amplitude–phase coupling follows a particular curve, or that a physical device realizes the ideal operator.

## 1. Purpose and scope

Define (1) the scalar interference primitive, (2) its input domain and ideal reference, (3) a parameterized interface for nonideal physical response, (4) numerical error metrics, and (5) the evidence gate for authorizing a bounded physical-device simulation.

This artifact does not select a foundry, PDK, layout, or topology. It does not fully specify tensor-level KKA attention. Those decisions require separate versioned contracts.

## 2. Evidence labels

- **E0 — Assumed:** stipulated, not tested.
- **E1 — Formal:** property checked against a formal contract.
- **E2 — Software-tested:** reproducible numerical test.
- **E3 — Simulated:** identified physical-simulator result with configuration provenance.
- **E4 — Measured:** physical measurement with instrument and calibration provenance.
- **E5 — Foundry:** fabrication/process evidence.

Formal proof is not physical validation. Simulation is not measurement. A fitted model is not independent measurement unless supported by measurement data.

## 3. Operator and input domain

### 3.1 Inputs

The primitive accepts coherent complex field amplitudes a,b ∈ ℂ with a defined relative phase. Software tests must declare finite bounds |a| ≤ Amax and |b| ≤ Bmax, numeric dtype, normalization, and tolerance. Unless specified otherwise, the values are dimensionless complex envelopes normalized to a documented reference amplitude.

A physical mapping must additionally declare field units/normalization, wavelength, polarization, spatial mode, reference planes, and coherence assumptions. If a stable phase relationship is not available, the cross term cannot be presumed observable as written.

### 3.2 Ideal total intensity

Iideal(a,b) = |a+b|² = |a|² + |b|² + 2 Re(ab*).

This is the exact mathematical reference for coherent superposition under the declared conventions.

### 3.3 Ideal signed cross term

Define the balanced-interference reference:

**Icross(a,b) = 2 Re(ab*)**

The paper's square operator is expressed as total intensity, a □ b = |a|² + |b|² + 2 Re(ab*). If balanced detection subtracts the self-intensity terms, the remaining signed cross term is Icross. An implementation that instead defines □ as Re(ab*) has a factor-of-two difference; its convention must be explicitly recorded and tested. Never silently mix these definitions.

Balanced detection is a possible physical implementation of cross-term extraction. This contract does not assume perfect cancellation of detector offsets, gain mismatch, common-mode noise, or other imperfections.

### 3.4 Required invariants and corner cases

For finite complex inputs:

- Symmetry: Icross(a,b) = Icross(b,a).
- Conjugation invariance: Icross(a,b) = Icross(a*,b*).
- Phase dependence: if a=A exp(iφa), b=B exp(iφb), then Icross = 2AB cos(φa−φb).
- Relative phase 0 gives +2AB; relative phase π gives −2AB.
- Relative phase ±π/2 gives zero ideal cross term.
- If either input is zero, the cross term is zero.
- Bound: |Icross| ≤ 2|a||b|.
- Total intensity is nonnegative; the signed cross term may be negative and must not be clipped to zero.

Tests must include zero fields, equal and unequal amplitudes, constructive/destructive/quadrature phases, domain boundaries, and a seeded sweep.

## 4. Boundary between scalar interference and KKA attention

Tian et al., *Photonic transformer chip: interference is all you need*, PhotoniX 6, 45 (2025), DOI 10.1186/s43074-025-00182-7, describe an interference primitive and propose a KKA composition such as (Qᵀ □ K) □ V as an approximation to standard softmax attention.

EIS-KKA-001 specifies only the scalar primitive and physical-response interface. It does **not** yet freeze tensor axes, reductions, scaling, head composition, bias/normalization, training semantics, encoding types, conversion boundaries, or a finite-channel estimator. Full KKA attention therefore remains **BLOCKED** for formal/software comparison until those details are captured in a separate versioned contract.

At every composition stage, □ must state whether it consumes complex fields, real balanced-detector values, or encoded values. Type changes and conversion boundaries must be explicit.

## 5. Ideal reference implementation

Maintain two separate reference functions:

- total intensity: abs(a + b)**2
- signed balanced cross term: 2 * real(a * conjugate(b))

Use a declared complex dtype. Test each function against an independent algebraic form and the invariants above. Record tolerances appropriate to that dtype; this document does not prescribe a universal tolerance.

Compare candidate outputs against the ideal reference using identical inputs, ordering, normalization, and output convention. Preserve raw signed outputs. Do not normalize away scale errors before reporting them.

## 6. Parameterized nonideality model

Do not hard-code an assumed Kramers–Kronig or amplitude–phase coupling curve for an uncharacterized EIS platform. Represent candidate response as:

y_candidate = Fθ(a, b; c)

where Fθ is the versioned response model, θ is its parameter set with provenance, and c is operating context (including wavelength, mode/polarization, temperature, controls, and reference planes). The candidate observable must use the same units and convention as the ideal reference, or be mapped through a separately validated calibration.

Potential terms, if relevant and supported, include amplitude-dependent phase response, phase-setting offset/quantization, insertion loss, imbalance, imperfect splitting, propagation loss, reflections, detector responsivity/offset/gain/noise, thermal/electrical crosstalk, settling, wavelength/temperature/fabrication variation, and finite-channel or DAC/ADC quantization.

For every parameter, record value or range, units, provenance, and uncertainty. Label it **assumed**, **fitted**, **simulated**, or **measured**. Unknown parameters remain explicitly unknown. Setting nonidealities to zero is permitted only as an explicitly labelled idealized control.

The Kramers–Kronig relations connect real and imaginary parts of a causal linear response under applicable assumptions; they do not alone provide a device-specific amplitude-to-phase transfer curve. A platform-specific response must be justified by device physics, appropriate simulation, or measurement.

## 7. Error metrics and test protocol

For N paired outputs yi (ideal) and yhat_i (candidate), preserve per-sample records and report:

1. Absolute error ei = yhat_i − yi.
2. MAE = mean(|ei|).
3. RMSE = sqrt(mean(ei²)).
4. NRMSE = RMSE / sy, where sy is a predeclared reference scale (for example, RMS ideal output). If sy is zero or too small, report NRMSE as undefined and provide absolute errors.
5. Maximum absolute error.
6. Signed bias = mean(ei).
7. Optional correlation/cosine similarity, secondary only and never a substitute for scale-sensitive errors.
8. Where available: input/output power, excess loss, reflection, radiation, detector offset, and calibration residuals.

Do not divide by near-zero ideal outputs without a declared denominator floor; report the floor and affected sample count. Freeze seed, sample count, generator, distribution, amplitude/phase ranges, and metrics before candidate scoring. Report results by regime as well as aggregate so a small aggregate error cannot hide phase-specific failure.

**No universal numerical acceptance threshold is set here.** EIS must choose thresholds from downstream useful-task tolerance and known simulation/measurement uncertainty before candidate evaluation. Until then, tests characterize error but cannot declare physical acceptability.

## 8. Mandatory gate before physical-device simulation

A physical-device simulation can be proposed only after all applicable checklist items are complete. Passing the gate permits only a bounded simulation; it does not certify feasibility or authorize fabrication.

### K0 — Mathematical and software readiness

- [ ] Factor-of-two convention and distinction between total intensity and signed cross term frozen.
- [ ] Input types, normalization/units, amplitude bounds, phase convention, and operating context declared.
- [ ] Independent ideal reference and deterministic corner-case vectors implemented.
- [ ] Invariants and tests pass under a stated dtype-specific tolerance.
- [ ] Nonideality model versioned; unknowns remain visible.
- [ ] Error metrics, test distribution, and acceptance thresholds frozen before scoring.
- [ ] If full KKA is in scope, tensor shapes, axes, reductions, encodings, and conversion boundaries specified separately.
- [ ] Reproducible report contains source revision, environment, seed, vectors, raw outputs, metrics, and hashes.

### K1 — Physical question and technology context

- [ ] One falsifiable physical question stated.
- [ ] Target technology and PDK identity declared; mock/unverified PDKs labelled.
- [ ] Material dispersion/loss model, geometry, port/mode definitions, wavelength band, polarization, boundaries, and reference planes documented.
- [ ] Every device parameter labelled PDK-sourced, measured, literature-derived, assumed, or unknown.
- [ ] Simulation observables map explicitly to contract outputs and error metrics.
- [ ] Effects outside the chosen solver's model (e.g. thermal crosstalk or detector electronics) assigned to a separate model or explicitly excluded.

### K2 — Reproducibility, cost, and authorization

- [ ] Geometry and simulation source versioned and hashed.
- [ ] Mesh/grid, domain, boundaries, monitors, runtime/convergence criteria, and solver version recorded.
- [ ] Convergence/sensitivity plan specified; one untested mesh/run is not validation.
- [ ] Cloud cost estimate recorded.
- [ ] Explicit human approval for the bounded spend recorded before submission.
- [ ] Stop conditions and maximum job count/cost declared.
- [ ] Logs, task IDs, configurations, outputs, and result hashes will be retained.

If any mandatory item is missing, status is **BLOCKED**. This artifact itself dispatches no cloud job.

## 9. Required evidence package and decision

Retain the contract revision/hash; reference source and vectors; candidate model and parameter provenance; raw paired outputs; metrics, plots, uncertainty and exclusions; environment and source commit; physical DesignContext and simulation configuration when applicable; cost estimate and approval record; task IDs, logs and result hashes; and one decision: ACCEPT_FOR_NEXT_GATE, REJECT, REFINE, or BLOCKED.

ACCEPT_FOR_NEXT_GATE means only that the named next gate may begin. It does not mean KKA works on EIS's platform.

## 10. Explicit non-claims

This artifact does not claim that KKA is equivalent to standard attention for all inputs/tasks; that amplitude–phase coupling is strong, controllable, or useful on EIS's intended platform; that SOI results transfer to SiN/TFLN; that the scalar primitive defines complete attention; that simulation is measurement; that energy, heat, latency, throughput, or CO₂e advantages have been demonstrated; or that simulation, fabrication, or spending is authorized.

## 11. Immediate next action

Implement and test the ideal scalar reference and deterministic vectors. Freeze the factor-of-two and data-type conventions. Keep unknown physical-response parameters explicit. Do not submit a Flexcompute job until K0 is reviewed and K1/K2 identify a concrete, authorized physical question.
