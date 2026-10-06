# GitHub2VLPI-002 — Cold-Start Agent Execution and Evidence Boundary Test

## Purpose

GitHub2VLPI-002 is a blind cold-start experiment for the EIS-VLPI agent interface.

The test asks whether an agent can discover and execute the existing VLPI physical-information model without being given expected physical or PDK results in advance.

## Scientific question

> Can a cold-start agent independently discover, execute, interpret, and report an executable VLPI physical-computation experiment while preserving the boundary between software execution, capability compatibility, and physical validation?

## Agent-visible boundary

The agent begins from the repository and declared discovery interface. It may inspect the manifest, experiment contract, VLPI-IR, RU, Contract, DesignContext, Evidence, executable RU-001 reference model, PDK capability experiment, fixtures, tests, and schemas.

Expected phase-sweep values and expected final classifications are not supplied.

## Required behavior

1. Discover VLPI-PDK-001.
2. Resolve the controlled RU, Contract, VLPI-IR, DesignContext, and Evidence.
3. Verify controlled identities remain unchanged.
4. Execute reference_model/ru001.py.
5. Independently choose or derive a sufficient phase sweep.
6. Analyze the PDK capability matrix.
7. Preserve explicit not-run states.
8. Report evidence without promoting it into physical validation.
9. Propose compiler implications only where observed results support them.
10. Stop before consequential physical action.

## Evidence semantic guardrail

A capability-harness PASS means the declared harness predicates passed. It is not physical validation.

Capability experiment evidence should distinguish result kind from physical-subject status, using the conceptual result kind capability-compatibility and a status that does not imply physical demonstration.

## Hidden oracle

Expected numerical phase behavior and expected classifications belong to the evaluator, not the agent-visible experiment. This prevents the test from becoming instruction following.

## Compiler hold point

The agent must not freeze a conventional compiler architecture. It may identify future requirements when directly supported by observed experiment behavior, including possible needs for explicit physical state, state-boundary conditions, PDK capability constraints, topology, thermal constraints, and evidence provenance.

## Success

Success means the agent can traverse:

GitHub -> discovery -> VLPI-IR -> RU/Contract/DesignContext/Evidence -> executable reference model -> PDK experiment -> evidence classification -> bounded inference

without hallucinating physical reality.

The next major experiment must be derived from what this cold-start execution actually reveals.
