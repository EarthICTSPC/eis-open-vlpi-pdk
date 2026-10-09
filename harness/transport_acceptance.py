#!/usr/bin/env python3
"""MCP Streamable HTTP transport acceptance test for HARNESS-001.

This is a transport/task-interface test only. It does not establish P5
cryptographic provenance and does not claim physical validation.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


REQUIRED_TOOLS = {
    "discover",
    "create_state",
    "transition",
    "observe",
    "evaluate_contract",
    "compose",
}

FORBIDDEN_IMPLEMENTATION_MARKERS = {
    "_reference_transform",
    "math.cos",
    "cos(",
    "1.0 - math.cos",
}


def structured(result):
    value = getattr(result, "structured_content", None)
    if value is not None:
        return value
    blocks = getattr(result, "content", [])
    texts = [getattr(block, "text", "") for block in blocks if getattr(block, "text", None)]
    if len(texts) == 1:
        try:
            return json.loads(texts[0])
        except json.JSONDecodeError:
            return texts[0]
    return texts


async def run(endpoint: str) -> None:
    async with streamablehttp_client(endpoint) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as client:
            await client.initialize()
            await _run_acceptance_checks(client, endpoint)


async def _run_acceptance_checks(client, endpoint: str) -> None:
    tool_result = await client.list_tools()
    names = {tool.name for tool in tool_result.tools}
    missing = REQUIRED_TOOLS - names
    if missing:
        raise AssertionError(f"missing MCP tools: {sorted(missing)}")

    discovery = structured(await client.call_tool("discover", {}))
    serialized = json.dumps(discovery, sort_keys=True)
    if any(marker in serialized for marker in FORBIDDEN_IMPLEMENTATION_MARKERS):
        raise AssertionError("reference implementation marker exposed by discovery")

    assert discovery["experiment"] == "OPENLLM-GITHUB2VLPI-002"
    assert discovery["harness"] == "HARNESS-001"
    assert discovery["physical_validation"] is False

    state_id = "transport_acceptance_s0"
    created = await client.call_tool(
        "create_state",
        {"state_id": state_id, "amplitude": 1.0, "phase": 0.0},
    )
    if getattr(created, "is_error", False):
        raise AssertionError("create_state failed")

    transitioned = await client.call_tool(
        "transition",
        {"state_id": state_id, "phase_delta": 3.141592653589793},
    )
    if getattr(transitioned, "is_error", False):
        raise AssertionError("transition failed")
    transition_data = structured(transitioned)
    output_state_id = transition_data["output_state"]["state_id"]

    observed = await client.call_tool("observe", {"state_id": output_state_id})
    if getattr(observed, "is_error", False):
        raise AssertionError("observe failed")
    observation_data = structured(observed)
    observation_id = observation_data["observation_id"]

    contract = await client.call_tool(
        "evaluate_contract",
        {"observation_id": observation_id, "name": "bounded_reference_power"},
    )
    if getattr(contract, "is_error", False):
        raise AssertionError("evaluate_contract failed")
    if structured(contract)["verdict"] != "PASS":
        raise AssertionError("bounded_reference_power did not PASS")

    composition = await client.call_tool(
        "compose",
        {"first_state_id": state_id, "second_phase_delta": 1.5707963267948966},
    )
    if getattr(composition, "is_error", False):
        raise AssertionError("compose failed")
    if structured(composition)["accepted_interface"] is not True:
        raise AssertionError("composition interface not accepted")

    malformed = await client.call_tool("transition", {"state_id": state_id})
    if not getattr(malformed, "is_error", False):
        raise AssertionError("malformed transition was not rejected")

    print("MCP TRANSPORT ACCEPTANCE: FULL PASS")
    print(f"endpoint={endpoint}")
    print("checks=tool-discovery,interface,blindness,health-contract,composition,malformed-input")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("endpoint", help="MCP Streamable HTTP endpoint, e.g. https://.../mcp")
    args = parser.parse_args()
    try:
        asyncio.run(run(args.endpoint))
    except Exception as exc:
        print(f"MCP TRANSPORT ACCEPTANCE: FAIL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
