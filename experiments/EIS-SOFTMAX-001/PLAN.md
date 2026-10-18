# EIS-SOFTMAX-001 — Learned Attention Without Explicit Softmax

**Parent:** EIS-REBOOT-001  
**Status:** Proposed; blocked until the formal contract, dataset identity, and conductor budget are committed.  
**Target evidence:** E1 formal contract + E2 reproducible software tests. No physical evidence is claimed.

## 1. Hypothesis

A precisely specified interference-native, KKA-style attention operator may retain useful task performance without an explicit softmax stage and may reduce attention memory or inference latency under a matched language-modeling workload.

This is a hypothesis, not a result. If evidence does not support it, the experiment must reject or refine the hypothesis rather than reinterpret a negative result as success.

## 2. Variants

Primary comparison:

1. **Softmax attention** — conventional causal scaled dot-product attention.
2. **Sigmoid attention** — an independently defined softmax-replacement baseline with its scaling and normalization rules pinned.
3. **KKA-style interference-native attention** — only after its exact mathematical definition, trainable parameters, finite-channel estimator, and error bounds are committed.

Optional independent alternative: one linear-attention or cosine-attention variant, but only if its contract and budget are committed before execution.

All variants must use the same data split, tokenizer, context length, training-token budget, optimizer schedule, and evaluation workload. Match total parameter count within a predeclared tolerance; report any unavoidable mismatch rather than hiding it.

## 3. Fixed controls

Before any training run, commit:
- dataset source, exact slice manifest, and cryptographic hash;
- tokenizer name/revision and hash;
- train/validation/test split hashes;
- model depth, width, head count, and context length;
- operator definitions and source revision;
- optimizer, schedule, batch size, training steps/tokens, and fixed seeds;
- evaluation script and metric definitions;
- total compute ceiling and per-variant allocation.

Use at least three fixed seeds per variant if the approved budget supports it. If the budget does not support three seeds, record the reduction before execution and treat uncertainty accordingly. Do not tune on the held-out test split.

## 4. Measurements

Record for every seed and variant:
- validation bits-per-token and perplexity;
- top-1 next-token accuracy;
- training time and inference latency at fixed batch sizes;
- peak accelerator memory;
- parameter count and estimated operation count;
- energy at the wall only if a calibrated meter is available; otherwise label energy **not measured**;
- determinism/reproducibility notes;
- uncertainty across seeds;
- run IDs, logs, source revision, and result hashes.

Do not infer total system energy from FLOPs, accelerator utilization, or a vendor headline. Report estimates separately from measurements.

## 5. Formal gate

Before execution:
- commit the Lean 4 contract for each operator;
- check shapes, causal masking, finite outputs under declared bounds, parameter-count accounting, and determinism requirements;
- record Lean toolchain and source hashes;
- create conformance vectors shared by the reference model and implementations;
- classify KKA-style attention as **BLOCKED** if its definition is not precise enough to formalize.

A proof applies to the stated mathematical model and assumptions. It is not evidence that an optical device realizes the operator.

## 6. Conductor gates

| Gate | Requirement | Failure behavior |
|---|---|---|
| G0 | Charter accepted; task, data, metrics, and budget fixed | BLOCKED |
| G1 | Operator contracts checked; source/toolchain pinned | BLOCKED or candidate REJECTED |
| G2 | Softmax baseline reproduced under the declared protocol | Stop and diagnose; do not compare unmatched results |
| G3 | All admitted variants run under matched budgets and seeds | Record every failed/partial run; no silent omission |
| G4 | Evidence ledger complete with provenance and uncertainty | BLOCKED |
| G5 | Review decision recorded: accept, reject, refine, or defer | No automatic physical claim |

## 7. Budget ceiling

Proposed default ceiling: **24 accelerator-hours total**, or a lower ceiling set by the conductor before G3. This is a proposed cap, not authorization to spend. The conductor must record explicit approval and per-variant allocations before any run. Any increase requires explicit approval and a recorded reason.

## 8. Decision rule

A variant is **promising for further software study** only if:
- it satisfies its formal contract and reproducibility requirements;
- validation perplexity is no worse than the softmax baseline by more than 1% relative under the predeclared evaluation protocol; and
- either peak attention memory or measured inference latency improves by at least 10% under matched conditions.

This is a screening threshold, not proof of statistical significance or physical advantage. Report seed variance and uncertainty. If the thresholds are not met, record **reject** or **refine**. A null result is evidence.

A software win does not authorize a claim of lower photonic energy, lower heat, physical feasibility, or superiority on other tasks.

## 9. Evidence ledger fields

- experiment ID and parent charter;
- candidate/operator ID, source revision, and source hash;
- dataset, tokenizer, and split hashes;
- model configuration, parameter count, and matching tolerance;
- seeds, optimizer, training-token budget, and compute allocation;
- Lean contract revision and toolchain version;
- run IDs, status, logs, artifact paths, and result hashes;
- metrics with units and uncertainty;
- provenance label: assumed, formal, software-tested, simulated, measured, foundry, or missing;
- decision and rationale;
- next bounded experiment or explicit deferral.

## 10. Exit criteria

The experiment exits only when:
- a reproducible report exists;
- every claim is evidence-labeled;
- the conductor ledger is complete;
- failed and blocked runs are retained;
- the review decision is recorded;
- the next experiment is proposed with bounded scope or explicitly deferred.

## 11. Non-claims

EIS-SOFTMAX-001 is a software abstraction experiment. It does not authorize a photonic simulation, PIC layout, VLSI controller claim, fabrication claim, or statement that photonic computation is cooler or more energy-efficient.

## 12. Immediate next action

Complete G0 by fixing the dataset slice and tokenizer, confirming the actual compute budget, and assigning the owner for the formal KKA-style operator definition. Do not dispatch training or FlexCompute work until the formal and budget gates pass.
