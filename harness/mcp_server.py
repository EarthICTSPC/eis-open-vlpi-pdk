"""MCP adapter for OPENLLM-GITHUB2VLPI-002-HARNESS-001.

Transport is supplied by the official MCP Python SDK. The adapter exposes the
same task operations as the reference HTTP service; it does not define the
Experiment A vocabulary.
"""

from mcp.server.fastmcp import FastMCP
from experiment_a_service import ExperimentState

mcp = FastMCP(
    "EIS Experiment A Harness",
    instructions=(
        "Execute the public OPENLLM-GITHUB2VLPI-002 Experiment A bounded task. "
        "Do not treat implementation details as ontology primitives."
    ),
)
state = ExperimentState()


@mcp.tool()
def discover() -> dict:
    """Return the public task interface and evidence boundary."""
    return state.discover()


@mcp.tool()
def create_state(state_id: str, amplitude: float, phase: float) -> dict:
    """Create a task state."""
    return state.create_state(state_id, amplitude, phase)


@mcp.tool()
def transition(state_id: str, phase_delta: float) -> dict:
    """Apply one reference transition to a state."""
    return state.transition(state_id, phase_delta)


@mcp.tool()
def observe(state_id: str) -> dict:
    """Record an observation of a state."""
    return state.observe(state_id)


@mcp.tool()
def evaluate_contract(observation_id: str, name: str) -> dict:
    """Evaluate one task acceptance contract."""
    return state.evaluate_contract(observation_id, name)


@mcp.tool()
def compose(first_state_id: str, second_phase_delta: float) -> dict:
    """Execute the bounded two-stage composition interface."""
    return state.compose(first_state_id, second_phase_delta)


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000, session_idle_timeout=1800)
