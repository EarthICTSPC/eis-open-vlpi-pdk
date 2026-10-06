# EIS-SWARM-001 — Derived Agent Population

## Purpose

EIS-SWARM-001 tests whether a formal problem specification can derive an admissible agent population and dependency structure rather than having a human or LLM prescribe a fixed swarm size.

## Bounded demonstration

The initial bounded problem is the RU-001-aligned 2x2 MZI residual-field problem. Required outputs are phase-sweep results and invariant verification. Only mathematical and executable evidence are admissible for this bounded experiment.

## Derived population

Backward chaining from the required outputs produces:

A_FIELD -> A_RESIDUAL -> A_SWEEP -> A_INVARIANT
A_FIELD -> A_ENERGY -> A_INVARIANT
A_FIELD -> A_SWEEP

Selected population:
A_FIELD, A_RESIDUAL, A_ENERGY, A_SWEEP, A_INVARIANT

A_FAB is rejected because physical evidence is outside the bounded admissibility set.

The minimality claim is deliberately bounded: this population is minimal for this problem under these rules, not a claim of general swarm minimality.

## Agent architecture as transformation structure

An agent is treated as a capability-bearing state transformation with input state, output state, contract, evidence class, and dependencies.

Agent count is therefore an output of derivation. The transformation graph is the architecture.

A monolithic LLM agent may implement several transformations internally. A later refinement may split those transformations into cooperating agents, provided the external contract is preserved.

## Verification independence

The first perturbation requires:

verifier != generator

The purpose is to test whether independence is a formal architectural constraint capable of changing the derived population and dependency graph.

## Heterogeneous VLSI + VLPI

VLSI and VLPI are modeled as domains of capabilities, not separate swarm species. A heterogeneous swarm may contain VLSI, VLPI, hybrid, fabrication, and system agents whenever their contracts compose.

## Formalization boundary

The repository includes a machine-readable specification and a Lean4-oriented formal model. The Lean model is a separate EIS-SWARM experiment surface; it does not add Lean execution requirements to GitHub2VLPI-002.

No compiler architecture is frozen by EIS-SWARM-001.

## Evidence boundary

Results from this experiment are mathematical/formal evidence and executable software evidence when actually executed. They are not physical validation, fabrication evidence, measured device performance, PDK acceptance, or foundry acceptance.

## Next experiment

EIS-SWARM-001-A — Verification Independence Perturbation.

Change only the admissibility rule requiring independent verification, then derive the population and dependency graph again. The result, not a preconceived swarm size, determines the next requirement.
