# OPENLLM-GITHUB2VLPI-002 — Experiment A: S/T/O/C Bounded Vocabulary Test

**Status:** specified experiment; not yet executed  
**Parent objective:** OPENLLM-GITHUB2VLPI

## 1. Purpose

Experiment A tests the candidate vocabulary S/T/O/C:

- **S — State:** representation of a physical configuration or computationally relevant state.
- **T — Transition:** parameterized process mapping an input state to an output state.
- **O — Observation:** recorded result of observing a state or transition under stated conditions.
- **C — Contract:** acceptance predicate over a state, transition, or observation.

This does **not** establish that S/T/O/C is a universal ontology or globally minimal vocabulary.

It tests bounded-task sufficiency, ablation-based necessity, composition, and failure modes.

## 2. Blindness requirement

The independent agent MUST receive only:

1. this experiment specification;
2. the machine-readable task/DSL specification in EIS-OPENLLM-GITHUB2VLPI-002-STOC.yaml;
3. access to the explicitly designated black-box task harness.

The agent MUST NOT be given or use as an expected answer:

- EIS-SWARM-001 candidate populations;
- EIS-SWARM-001-A derivations;
- the SWARM disagreement artifact;
- the prior RU-001 abstraction;
- any EIS-selected agent population;
- a predefined field equation or residual equation;
- SiN, MRR, SOI, TFLN, RISC-V, PRISM;
- the Springer photonic-transformer paper;
- a compiler architecture;
- Boolean-gate, MAC, matrix/vector, tensor, or conventional accelerator abstractions.

The agent may derive concepts independently, but may not import them merely as assumed architecture.

## 3. Bounded VLPI-relevant task

The task is a black-box, bounded **two-stage optical-interference transformation**.

The harness supplies a reference transformation service without exposing its internal physical equation.

The agent must:

1. discover the callable transformation and accepted input state/parameter form;
2. construct an initial state S0;
3. execute transition T1;
4. record observation O1;
5. evaluate contract C1;
6. use the accepted resulting state as input to T2;
7. execute T2;
8. record O2;
9. evaluate C2;
10. demonstrate the composed result T2(T1(S0)) satisfies the stated composition acceptance condition.

The task is deliberately bounded. It is not an LLM, transformer, fabrication, or full photonic-design task.

The harness may expose physically meaningful parameters such as optical input conditions and phase/control values, but must not expose an implementation equation as the task ontology.

## 4. Candidate DSL

Only these primitives exist initially:

    State       ::= record describing a state
    Transition  ::= procedure(State, Parameters) -> State
    Observation ::= record(State-or-Transition, Conditions, Result)
    Contract    ::= predicate(State, Transition, Observation) -> Verdict

The DSL MUST NOT contain separate primitives for:

- matrix;
- vector;
- tensor;
- Boolean gate;
- MAC;
- compiler;
- residual equation;
- field algebra;
- optimizer;
- compatibility relation;
- regeneration;
- constraint-reduction operator.

If an agent believes one is necessary, it must report that as a derived requirement or failure rather than silently adding it.

## 5. No-import rule

An import is any use of a conventional computational abstraction as an assumed primitive rather than a result derived from the permitted vocabulary.

Examples include treating the task as matrix multiplication, a MAC, a gate, or a compiler problem, or importing an externally supplied field equation.

Every potentially architectural imported abstraction MUST be logged as one of:

- derived-from-STOC;
- required-but-forbidden;
- used-as-implementation-mechanism-only.

Ordinary programming-language control flow needed to call the harness is not itself an ontology claim.

## 6. Instrumentation

Record at minimum:

- model identity and version;
- agent identity/version;
- experiment specification revision;
- repository revision;
- complete task prompt;
- vocabulary definition supplied;
- every State creation/mutation;
- every Transition invocation;
- every Observation;
- every Contract evaluation;
- every composition attempt;
- every imported abstraction considered;
- every forbidden-import attempt;
- every failure/retry;
- human intervention;
- final evidence classification.

Raw trace data MUST be published without silently deleting failed attempts.

## 7. Ablation matrix

Run the full candidate set, then every non-empty proper subset:

| Run | S | T | O | C |
|---|---:|---:|---:|---:|
| A-STOC | yes | yes | yes | yes |
| A-STO | yes | yes | yes | no |
| A-STC | yes | yes | no | yes |
| A-SOC | yes | no | yes | yes |
| A-TOC | no | yes | yes | yes |
| A-ST | yes | yes | no | no |
| A-SO | yes | no | yes | no |
| A-SC | yes | no | no | yes |
| A-TO | no | yes | yes | no |
| A-TC | no | yes | no | yes |
| A-OC | no | no | yes | yes |
| A-S | yes | no | no | no |
| A-T | no | yes | no | no |
| A-O | no | no | yes | no |
| A-C | no | no | no | yes |

The empty set is not a meaningful execution condition and is recorded as not-applicable.

A subset is task-successful only if it completes the same task and acceptance criteria without silently replacing the removed primitive under another name.

## 8. Acceptance criteria

### Full-set success

A-STOC succeeds only if the agent:

1. discovers the task interface;
2. represents initial and intermediate states;
3. executes both transitions;
4. records observations;
5. evaluates acceptance contracts;
6. composes the two accepted transitions;
7. produces the evidence record;
8. obeys the no-import rule.

### Composition

Composition succeeds only if:

    S0 --T1--> S1 --T2--> S2
         O1/C1        O2/C2

is represented and executed without a separate compatibility primitive.

If compatibility is required, the agent must show whether it can be expressed as part of an existing Contract.

### Ablation result classes

- PASS — task remains fully executable with no hidden replacement;
- FAIL-MISSING — removed capability is independently required;
- FAIL-AMBIGUOUS — task/specification is insufficient;
- FAIL-IMPORT — completion requires violating the no-import rule;
- FAIL-IMPLEMENTATION — harness/tooling failure unrelated to vocabulary;
- FAIL-AGENT — vocabulary/task appear sufficient but the agent fails to discover or execute them.

## 9. Minimality interpretation

Experiment A may establish that a primitive is necessary or unnecessary **for this bounded task under this specification and execution environment**.

It may establish that the full candidate vocabulary is sufficient for this bounded task.

It MUST NOT be interpreted as establishing that S/T/O/C is the globally minimal ontology for VLPI, photonic computing, agents, or LLM execution.

## 10. Evidence classes

Expected evidence:

- specified;
- computationally-demonstrated;
- derived-metric;
- proposed-hypothesis.

Experiment A does NOT produce:

- physical measurement;
- fabrication evidence;
- PVR PASS;
- BIST PASS;
- foundry acceptance;
- physical validation of an optical device.

## 11. Failure taxonomy

**F1 — Missing vocabulary:** required operation cannot be completed with the permitted subset.

**F2 — Task ambiguity:** insufficient information to determine the required operation or acceptance condition.

**F3 — Import violation:** agent relies on a forbidden conventional abstraction as an assumed primitive.

**F4 — Harness/tool failure:** reference service, runner, transport, or instrumentation fails independently of vocabulary.

**F5 — Agent failure:** vocabulary and task are sufficient in principle, but the particular agent fails.

F5 must not be converted into evidence that the vocabulary itself is insufficient.

## 12. Publication bundle

A completed Experiment A publication MUST contain:

    experiment-a/
      EIS-OPENLLM-GITHUB2VLPI-002-STOC.yaml
      task/task-specification.yaml
      traces/full-set/
      traces/ablations/
      results/ablation-results.yaml
      evidence/evidence-manifest.yaml
      README.md

## 13. Independent replication

At least two independent runs are preferred before interpreting vocabulary necessity.

Where multiple open LLMs are available, models should run independently against the same specification.

Agreement supports reproducibility of the bounded task, not physical truth. Disagreement identifies specification or vocabulary uncertainty.

## 14. Relationship to Experiment B

Experiment A deliberately excludes physical embodiment.

Only after Experiment A should the project introduce a preferred exemplar embodiment such as:

    abstract transformation
            ↓
    photonic interference
            ↓
    SiN + MRR
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

This is Experiment B, not Experiment A.

The preferred EIS embodiment therefore does not contaminate the vocabulary experiment.

## 15. Decision gate

Experiment A is complete when:

1. the full-set run is reproducible;
2. all 15 non-empty subsets have a recorded result, or documented reason they cannot be run;
3. failures are classified;
4. raw traces are published;
5. no physical claim is promoted;
6. an independent reviewer can reproduce the interpretation from the traces.

**Decision rule: Do not select the ontology before the experiment. Let the ablation results determine which capabilities the bounded task actually requires.**

**Working principle: Discover the ontology. Do not design it.**
