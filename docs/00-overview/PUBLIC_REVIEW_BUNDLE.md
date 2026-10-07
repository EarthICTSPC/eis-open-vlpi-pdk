# Public Review Bundle

This page exists so an independent LLM can discover the current review artifacts from the canonical `main` branch without knowing EIS's internal branch names.

## EIS goal

EIS is building the GitHub-to-VLPI infrastructure needed to investigate **openLLM-GitHub2VLPI**: MCP-enabled AI agents, including FlexCompute/FlexAgent-style workflows, enabling open LLMs such as open DeepSeek and other open models to discover, execute, verify, and ultimately drive physical photonic computation.

This repository is the open technical infrastructure supporting that goal. It is not yet evidence that an open LLM is running on photonic hardware.

## Review artifacts

### GitHub2VLPI-002 frozen evidence

- `evidence/github2vlpi-002/FROZEN-EMPIRICAL-EVIDENCE.json`
- `evidence/github2vlpi-002/github2vlpi-002-run.json`

These are copies of the frozen records; their experimental content is unchanged.

### SWARM-001-A disagreement analysis

- `docs/architecture/EIS-SWARM-001-A-DISAGREEMENT.md`

This is a discovery artifact, not an ontology decision.

### Independent review protocol

- `docs/00-overview/INDEPENDENT_LLM_REVIEW_GUIDE.md`

## What reviewers should evaluate

1. Can an independent open LLM discover the repository and its evidence without insider branch knowledge?
2. Can it distinguish reference-model computation, capability compatibility, not-run, and physical evidence?
3. Can it identify the minimum transformation vocabulary without being handed an expected ontology?
4. Can it identify what is still missing to move from GitHub/MCP execution toward openLLM-GitHub2VLPI?

## Important boundary

The current artifacts establish software/MCP and reference-model behavior. They do **not** establish fabrication, measurement, BIST PASS, foundry acceptance, or open-LLM execution on photonic hardware.
