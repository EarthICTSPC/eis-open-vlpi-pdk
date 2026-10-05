# MCP / AI-Agent Discovery Layer

This directory is the machine-readable discovery boundary for agents operating on the EIS Open VLPI repository.

Start with:
1. agents/agent-manifest.yaml
2. agents/experiments/VLPI-PDK-001.yaml
3. schema/pdk/pdk-compatibility.schema.yaml
4. verification/pdk/VLPI-PDK-001.yaml

Agent rule: Discover -> inspect -> plan -> execute permitted experiment -> validate evidence -> report.

An agent must never infer physical validation from a schema or capability-harness result.

Controlled PDKs, credentials, proprietary process data, and consequential fabrication actions remain outside the open agent boundary.
