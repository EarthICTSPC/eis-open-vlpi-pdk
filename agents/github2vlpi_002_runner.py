"""GitHub2VLPI-002: execute the cold-start agent through EIS-VLPI-MCP.

The runner is intentionally model-independent: all repository discovery and
experiment execution cross the MCP boundary. It contains no expected results.
"""
from __future__ import annotations
import asyncio, json, math
from pathlib import Path
from typing import Any
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifacts" / "github2vlpi-002-run.json"

def decode(result: Any) -> Any:
    value = getattr(result, "structured_content", None)
    if value is None:
        for block in getattr(result, "content", []) or []:
            text = getattr(block, "text", None)
            if text:
                try:
                    value = json.loads(text)
                except json.JSONDecodeError:
                    value = text
                break
    if value is None:
        raise RuntimeError("MCP tool returned no readable content")

    # Normalize transport wrappers recursively. MCP SDK renderings may expose
    # structured payloads as JSON strings or under a result wrapper. The
    # experiment semantics must not depend on that transport representation.
    for _ in range(6):
        if isinstance(value, dict) and "result" in value:
            value = value["result"]
            continue
        if isinstance(value, str):
            try:
                value = json.loads(value)
                continue
            except json.JSONDecodeError:
                pass
        break
    return value

async def call(session: ClientSession, name: str, args: dict | None = None) -> Any:
    result = await session.call_tool(name, args or {})
    if getattr(result, "is_error", False):
        raise RuntimeError(f"{name}: {decode(result)}")
    return decode(result)

def interpret_phase(results: list[dict]) -> dict:
    by_phase = {float(x["phaseRad"]): float(x["residualPower"]) for x in results}
    zero = by_phase[0.0]
    pi = min(by_phase, key=lambda x: abs(x - math.pi))
    return {
        "cancellationAtZero": zero < 1e-12,
        "maximumResidualNearPi": by_phase[pi] > 1.9,
        "zeroResidualPower": zero,
        "piResidualPower": by_phase[pi],
        "phaseCount": len(results),
    }

async def main() -> None:
    server = StdioServerParameters(
        command="python", args=["agents/mcp_server.py"], cwd=str(ROOT)
    )
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Discovery is performed through MCP, not by importing repo modules.
            tools = await session.list_tools()
            manifest = await call(session, "vlpi_discover")
            pdk_list = await call(session, "vlpi_pdk_list")
            # Normalize MCP structured output at the transport boundary.
            # The runner must tolerate the SDK's representation without
            # confusing a mapping wrapper, a list of environment records, or
            # a model-readable list of IDs.
            pdk_list_raw_type = type(pdk_list).__name__
            if not isinstance(pdk_list, dict) or "environments" not in pdk_list:
                raise TypeError(
                    f"Unexpected vlpi_pdk_list MCP shape: type={type(pdk_list).__name__} "
                    f"value={pdk_list!r}"
                )
            environments = pdk_list["environments"]
            if not isinstance(environments, list) or not all(
                isinstance(x, dict) and "id" in x for x in environments
            ):
                raise TypeError(
                    f"Unexpected vlpi_pdk_list environments shape: type={type(environments).__name__} "
                    f"value={environments!r}"
                )
            pdk_environment_ids = [x["id"] for x in environments]
            assert manifest["agentInterface"]["id"] == "EIS-VLPI-Agent-Interface"

            # Blind phase sweep: the agent supplies inputs and phases, then
            # interprets returned observations. No expected values are encoded.
            phases = [0.0, math.pi / 2, math.pi, 3 * math.pi / 2, 2 * math.pi]
            phase_results = [
                await call(session, "vlpi_run_ru001_reference", {
                    "a_real": 1.0, "a_imag": 0.0,
                    "b_real": 1.0, "b_imag": 0.0, "phase_rad": phase
                })
                for phase in phases
            ]

            # PDK execution also crosses MCP. Interpretation uses returned
            # observations only; the harness remains capability evidence.
            pdk = await call(session, "vlpi_run_pdk001")
            observations = [
                line.strip() for line in pdk.get("stdout", "").splitlines()
                if line.strip() and ":" in line
                and not line.startswith("VLPI-PDK-001 PASS")
            ]

            report = {
                "experiment": "GitHub2VLPI-002",
                "execution": {
                    "boundary": "EIS-VLPI-MCP",
                    "transport": "stdio",
                    "server": "EIS-VLPI-MCP",
                    "toolsDiscovered": [t.name for t in tools.tools],
                    "pdkListRawType": pdk_list_raw_type,
                },
                "discovery": {
                    "agentInterface": manifest["agentInterface"]["id"],
                    "currentExperiment": manifest["agentInterface"]["entrypoints"]["experimentDefinition"],
                    "pdkEnvironments": pdk_environment_ids,
                },
                "invariants": {
                    "controlledRU": "ru/RU-001/ru.yaml",
                    "controlledContract": "ru/RU-001/contract.yaml",
                    "controlledDesignContext": "ru/RU-001/design-context.yaml",
                    "expectedNumericalResultsSupplied": False,
                    "physicalActionTaken": False,
                },
                "reference_model_execution": {
                    "inputs": {"a": "1+0j", "b": "1+0j"},
                    "phasesRad": phases,
                    "results": phase_results,
                    "interpretation": interpret_phase(phase_results),
                },
                "pdk_matrix": {
                    "returnCode": pdk.get("returncode"),
                    "observations": observations,
                    "physicalValidation": False,
                    "resultKind": "capability-compatibility",
                    "openControlPreservedNotRun": any(
                        "OPEN-PDK-CONTROL-NOT-RUN: not-run" in x for x in observations
                    ),
                },
                "evidence_boundary": {
                    "referenceModel": "computationally-demonstrated only",
                    "pdkMatrix": "specified capability compatibility only",
                    "physicalValidation": False,
                    "prohibitedPromotions": [
                        "fabricated", "measured", "PVR PASS", "BIST PASS",
                        "foundry accepted", "physically verified"
                    ],
                },
                "compiler_inference": {
                    "architectureFrozen": False,
                    "observedRequirement": (
                        "Preserve separate semantics for reference behavior, "
                        "capability compatibility, and physical evidence."
                    ),
                },
                "next_experiment": {
                    "name": "GitHub2VLPI-003",
                    "title": "Dual Semantic/Execution Agent",
                    "type": "agent-experiment",
                    "compilerDesign": "hold",
                    "hypothesis": (
                        "A cold-start agent should be tested with semantic/read-only "
                        "and executable MCP surfaces separated, without predesigning a compiler."
                    ),
                },
            }
            OUT.parent.mkdir(parents=True, exist_ok=True)
            OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
            print(json.dumps(report, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
