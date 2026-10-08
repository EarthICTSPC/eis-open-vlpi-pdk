# Experiment A Freeze Protocol

## Purpose

A frozen Experiment A revision is an explicit provenance boundary. It prevents deployment or harness work from silently changing the scientific task.

"Frozen" does **not** mean "immutable forever." A defect discovered during execution may justify a controlled revision.

## What is frozen

A frozen revision consists of the exact contents and recorded revisions of:

- `docs/experiments/OPENLLM-GITHUB2VLPI-002-EXPERIMENT-A.md`
- `docs/experiments/EIS-OPENLLM-GITHUB2VLPI-002-STOC.yaml`
- `task/task-specification.yaml`

The revision identifiers are recorded in the execution-boundary artifact and every completed trace.

## During a freeze

Changes to the frozen artifacts MUST NOT be bundled with deployment, hosting, transport, or harness changes.

The execution-boundary CI guard enforces this separation for the boundary PR.

## Controlled unfreeze procedure

If an execution reveals a specification defect:

1. Record the defect as an issue or experiment finding.
2. Identify the exact frozen revision affected.
3. Explain why the defect prevents valid execution or interpretation.
4. Obtain explicit EIS approval to revise the experiment.
5. Modify the frozen artifacts in a dedicated revision PR, separate from deployment changes.
6. Assign new revision identifiers/SHA values.
7. Re-run the relevant repository validation.
8. Declare the new revision frozen.
9. Mark all traces produced against the prior revision as belonging to that prior revision; do not silently reinterpret them as runs of the new revision.
10. Update the execution-boundary provenance record to point to the new frozen revision before new independent runs begin.

## What an unfreeze does not permit

An unfreeze MUST NOT be used to:

- edit a result to obtain a desired outcome;
- remove an inconvenient trace;
- change the ontology after seeing an ablation result without recording the change;
- alter evidence classification retroactively;
- modify the deployment boundary in the same change merely for convenience.

## Principle

**Freeze protects provenance; it does not prevent legitimate correction.**

A corrected experiment is a new experiment revision, not a rewritten history.
