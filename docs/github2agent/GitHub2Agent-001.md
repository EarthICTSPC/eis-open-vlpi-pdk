# GitHub2Agent-001: Schema Traversal and Evidence-Gated Reconstruction

## Purpose

This is the first agent-readability test of the EIS Open VLPI information model.

It is deliberately **not** an RU-001 implementation.

The test asks whether an agent entering this repository from the GitHub root can reconstruct a small physical-computation object by traversing four linked schemas:

- **RU** — what physical object is being specified?
- **Contract** — what transformation and acceptance conditions are declared?
- **DesignContext** — in what technological and physical context is it intended to exist?
- **Evidence** — what is actually established, and what remains unverified?

The fixture is intentionally tiny so that failures expose information-model defects rather than domain complexity.

## GitHub2Agent principle

**GitHub2Agent is the repository-side counterpart to Paper2Agent.**

Paper2Agent asks whether a research document can be converted into an executable or structured research workflow.

GitHub2Agent asks whether an open technical repository can be converted into a machine-readable understanding of:

RU → Contract → DesignContext → Evidence → conclusion

The agent must traverse references rather than infer missing facts.

## Test fixture

Start at:

examples/github2agent-001/tiny-ru.yaml

Then resolve:

1. transformation.contractRef
2. verification.evidenceRefs
3. Evidence subject.designContextRef
4. DesignContext interfaces.electroPhotonic.contractRef
5. The evidence status and limitations

The expected reconstruction is:

> TINY-RU-001 is a specified, abstract example of a two-input physical field-combination unit. Its declared mapping is r = a - b. Its technology context is explicitly example-only. Its evidence establishes schema-level specification/traversal only; it does not establish electromagnetic performance, fabrication, PVR acceptance, BIST results, or measured behavior.

## Evidence gate

The agent **must not** upgrade the fixture beyond the evidence status actually declared.

Invalid conclusions include:

- "TINY-RU-001 is fabricated."
- "TINY-RU-001 passed PVR."
- "TINY-RU-001 is experimentally demonstrated."
- "TINY-RU-001 is a 10 GHz device."
- "The example-only technology context is a LIGENTEC/X-FAB PDK."
- "The contract is physically proven because the YAML parses."

## Required agent task

Give a cold-start agent only the public repository and ask:

> Starting from the repository root, identify TINY-RU-001, determine its declared transformation, resolve its Contract, DesignContext, and Evidence, and report what is established versus unverified. Propose the next executable verification step without inventing evidence.

A successful agent should be able to answer without access to the Research Article or prior conversation.

## Pass criteria

A GitHub2Agent implementation passes when it can:

1. Locate the RU fixture.
2. Resolve the RU → Contract reference.
3. Resolve the RU → Evidence reference.
4. Resolve Evidence → DesignContext.
5. Report the declared transformation.
6. Preserve the declared evidence status.
7. Enumerate the explicit limitations.
8. Refuse to infer fabrication, physical performance, PVR PASS, BIST PASS, or foundry acceptance.
9. Propose a next verification step consistent with the declared state.

## Failure criteria

The test fails if the agent:

- treats a declared parameter as a measured result;
- treats a file's presence as proof of execution;
- treats a contract as proof that the physical object satisfies the contract;
- substitutes a known foundry or PDK for the example-only context;
- skips a reference and fills the gap from general knowledge;
- collapses "specified" into "verified" or "measured."

## Why this comes before RU-001

If the four schemas cannot be traversed coherently on a tiny example, adding a real RU implementation only hides the information-model problem under physical-design complexity.

The correct sequence is:

schema → traversal → evidence gate → tiny fixture → RU-001

## Future extension

The next GitHub2Agent test should add a real RU implementation only after this fixture demonstrates that the repository can preserve:

- physical identity,
- transformation identity,
- technology context,
- evidence provenance,
- and unresolved verification gates.

No physical claim is made by this fixture.
