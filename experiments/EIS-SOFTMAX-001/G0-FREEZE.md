# EIS-SOFTMAX-001 — G0 Experimental Input and Control Freeze

**Repository:** EarthICTSPC/eis-open-vlpi-vlsi-conductor  
**Parent:** `docs/EIS-REBOOT-001.md`  
**Experiment plan:** `experiments/EIS-SOFTMAX-001/PLAN.md`  
**State:** `G0-FREEZE-PROPOSED / NOT-PASSED`  
**Scope:** software abstraction comparison only. No photonic simulation, PIC layout, fabrication, or physical-performance claim.

## 1. G0 rule

G0 passes only when every required input below is concretely identified, hashed, and approved. A named dataset or tokenizer without a resolved revision and content hash is not a frozen input. A proposed compute ceiling is not spending authorization. Do not dispatch training while any required field is unresolved.

## 2. Frozen comparison design

| Control | Frozen rule |
|---|---|
| Task | Causal next-token prediction on a small language-modeling dataset |
| Context length | 128 tokens |
| Primary metric | Validation bits per token; perplexity derived from the same token-level loss |
| Secondary metric | Top-1 next-token accuracy |
| Variants | (A) causal scaled dot-product softmax attention; (B) sigmoid attention with explicitly pinned scaling/normalization; (C) KKA-style operator only after its exact contract and finite-channel error model pass G1 |
| Matched controls | Same examples/splits, tokenizer, context, model dimensions, optimizer/schedule, training-token budget, evaluation implementation, and seeds across admitted variants |
| Test-set use | Final evaluation only; no tuning on test data |
| Seeds | Three fixed seeds per admitted variant if within the approved budget; otherwise freeze a smaller count before dispatch and label the result exploratory |
| Parameter matching | Declare tolerance before implementation; report actual trainable parameter counts and any mismatch |
| Reproducibility | Pin source revision, dependency lock, runtime/toolchain, data artifacts, configs, seeds, run IDs, logs, and result hashes |
| Energy | Wall energy only with a calibrated meter; otherwise record `not measured` |
| Failure handling | Preserve failed, partial, blocked, and negative runs; never silently drop them |

## 3. Dataset and tokenizer — unresolved content identities

The plan names TinyStories or an equivalent small dataset, but G0 requires one exact dataset and tokenizer. Do not treat this file as having frozen either identity until these fields are filled with immutable identifiers and verified hashes.

- Dataset repository/source: **UNSET**
- Dataset revision/commit: **UNSET**
- Exact slice/selection manifest: **UNSET**
- Raw dataset artifact SHA-256: **UNSET**
- Train manifest SHA-256: **UNSET**
- Validation manifest SHA-256: **UNSET**
- Test manifest SHA-256: **UNSET**
- Tokenizer repository/name: **UNSET**
- Tokenizer immutable revision: **UNSET**
- Tokenizer files/artifact SHA-256: **UNSET**
- Preprocessing/tokenization code revision and hash: **UNSET**

Required freeze procedure: resolve the source to an immutable revision; materialize the selected slice and deterministic split manifests; hash the actual files; record the tokenizer files and preprocessing code hashes; verify no overlap between train/validation/test example IDs; then commit the manifest. If the artifacts cannot be fetched and hashed, G0 remains blocked.

## 4. Model and training controls — proposed defaults, not yet authorized

The current plan does not specify enough values to reproduce training. Freeze all of these in a versioned machine-readable config before G0 can pass:

- Model family/config and exact dimensions: **UNSET**
- Total parameter-count target and matching tolerance: **UNSET**
- Optimizer and all hyperparameters: **UNSET**
- Learning-rate schedule/warmup: **UNSET**
- Batch size and gradient accumulation: **UNSET**
- Training-token budget / steps: **UNSET**
- Precision and numerical backend: **UNSET**
- Fixed seed list: **UNSET**
- Evaluation batch sizes and timing protocol: **UNSET**
- Dependency lockfile and runtime image/environment hash: **UNSET**

Any change after freeze creates a new config revision and must be recorded before the affected run; do not overwrite prior evidence.

## 5. Compute budget and approval

The experiment plan proposed a ceiling of **24 accelerator-hours total**. This is not confirmed authorization.

- Approved total ceiling: **UNSET — approval required**
- Hardware/backend and availability: **UNSET**
- Per-variant allocation: **UNSET**
- Per-seed allocation and timeout: **UNSET**
- Approval record / approver / date: **UNSET**

No accelerator job may be dispatched until the budget is explicitly approved and allocation is committed. Any increase requires fresh approval.

## 6. Operator admission

- Softmax baseline: admit after its exact implementation revision and conformance tests are recorded.
- Sigmoid variant: admit only after scaling, normalization, masking, and finite-output behavior are precisely specified.
- KKA-style variant: **BLOCKED** until Lean 4 states its exact mathematical operator, input/output contract, parameterization, finite-channel estimator, assumptions, and error bounds. Do not invent a definition from the label “KKA.”
- Other variants: excluded from this first comparison unless added through a pre-run, reviewed freeze revision.

## 7. G0 acceptance checklist

- [ ] Exact dataset source and immutable revision recorded
- [ ] Exact slice materialized; content and split-manifest hashes verified
- [ ] Train/validation/test separation checked
- [ ] Tokenizer revision and file hashes verified
- [ ] Preprocessing code revision/hash recorded
- [ ] Model and all training/evaluation controls committed in a machine-readable config
- [ ] Operator implementations and admission rules pinned
- [ ] Compute hardware and total/per-variant allocations specified
- [ ] Explicit compute-budget approval recorded
- [ ] Fixed seeds and failure/timeout policy committed
- [ ] Evidence-ledger location/schema and artifact hashing rules checked

**G0 status remains NOT-PASSED until every required item is complete.** This is intentional: freezing unknowns as placeholders would create the appearance of reproducibility without actual reproducibility.

## 8. Boundary of the first experiment

This comparison tests software abstractions for a bounded next-token task. Even a positive result supports only further software investigation under this protocol. It does not establish photonic realizability, lower physical energy, lower heat, or performance on general LLM workloads.
