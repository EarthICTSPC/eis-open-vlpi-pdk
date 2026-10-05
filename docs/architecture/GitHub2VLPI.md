# GitHub2VLPI — From Repository Discovery to Executable Physical Experiment

Earth ICT, SPC (EIS)

GitHub2VLPI is the agent-facing pattern for turning the EIS open technical disclosure into an executable physical-information model.

It is not a compiler. It is the discovery and experiment layer that lets an MCP-orchestrated AI agent start from a cold checkout, discover the current physical-computation model, execute permitted experiments, and report evidence without inventing missing physical facts.

## Core loop

GitHub -> Agent discovery -> VLPI-IR -> RU + Contract + DesignContext + Evidence -> PDK capability environment -> Executable experiment -> Compatibility/failure evidence -> Observed physical-design requirements -> Compiler requirements

The compiler is downstream of the executable physical model.

## VLPI-PDK-001

The first experiment asks what a VLPI PDK must actually provide.

The controlled input is RU-001. The same input is evaluated against an EIS Reference VLPI PDK capability model, deterministic hostile mock PDKs, and an external open-PDK control boundary that remains not-run until actually executed.

## Cold-start agent behavior

A new agent should be able to:
1. read agents/agent-manifest.yaml;
2. read agents/experiments/VLPI-PDK-001.yaml;
3. resolve the controlled inputs;
4. validate referenced schemas;
5. enumerate PDK environments;
6. run the repository-contained experiment;
7. inspect machine-readable results;
8. distinguish expected outcomes from observed results;
9. identify physical-design requirements demonstrated by the experiment;
10. propose compiler requirements only from observed requirements.

## Evidence boundary

Information-model validity != PDK capability compatibility != physics simulation != physical measurement != fabrication acceptance.

A successful experiment can be scientifically useful without claiming a successful fabricated photonic device.

## MCP boundary

MCP supplies tool discovery and orchestration. The repository supplies semantic authority.

Minimum resources:
- current experiment
- RU
- Contract
- DesignContext
- Evidence
- VLPI-IR
- PDK profiles
- schemas
- evidence policy

Minimum tools:
- discover
- resolve
- validate
- list PDKs
- inspect capabilities
- compare PDKs
- run permitted experiment
- emit evidence

Controlled PDK contents, credentials, proprietary process models, and confidential fabrication artifacts are never exposed through the open agent layer.

## Compiler hold point

GitHub2VLPI does not translate conventional source code into photonic code.

Its output is an evidence-backed statement of the physical operations the compiler must eventually support.

Potential operations include RU instantiation, physical-state preservation, transformation composition, state-boundary enforcement, technology selection, topology realization, wafer-scale tiling, thermal constraint propagation, and evidence generation.

These are examples, not frozen compiler requirements.

VLPI-PDK-001 decides which survive.
