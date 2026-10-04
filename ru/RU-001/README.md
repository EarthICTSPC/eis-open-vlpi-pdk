# RU-001 — First Real EIS Replicable Unit

RU-001 is the first real Replicable Unit to traverse the information/evidence model established by GitHub2Agent-001 and GitHub2Agent-002.

## Definition

RU-001 is specified as a bounded **2x2 MZI physical field transformation** with an explicit state boundary and an optional electro-optic regeneration path.

The repository treats the RU as a physical transformation object rather than as a Boolean gate.

Its machine-readable graph is:

RU → Contract → DesignContext → Evidence

The DesignContext exposes the intended technology identity while keeping controlled PDK contents outside the public repository.

## Current status

**specified**

This commit establishes a coherent reference specification. It does not establish fabrication or physical performance.

Specifically, this artifact does not claim:

- EM/FDTD validation;
- PDR/PCT/PTV PASS;
- fabrication;
- BIST measurement;
- foundry acceptance;
- measured capture/hold/error/energy performance.

The numerical values in the contract are acceptance targets or bounds to be evaluated at later evidence stages.

## State boundary

The state boundary is deliberately explicit.

The optical transformation produces a physical state. Acceptance, measurement, or regeneration occurs only at a declared boundary. This preserves the EIS rule:

> Do not convert the state merely because the next operation has traditionally been electronic.

Whether a later RU implementation can keep the state optical across additional transformations is an experimental question.

## Technology boundary

The DesignContext identifies:

**LIGENTEC_AN800_TFLN / LIGENTEC-X-FAB / SiN with TFLN integration**

as the controlled reference technology identity.

The public repository does not contain proprietary PDK contents, process rules, models, credentials, or other controlled foundry data.

## Evidence gate

The RU remains:

**specified + evidence-bound**

The next promotion requires actual domain-specific evidence. The repository should not promote RU-001 merely because its YAML validates.

## Why this matters

GitHub2Agent-002 proved that the information model itself can be tested from a cold checkout.

RU-001 now tests whether that same discipline survives when the object becomes a genuine EIS physical-computation specification rather than a tiny synthetic fixture.
