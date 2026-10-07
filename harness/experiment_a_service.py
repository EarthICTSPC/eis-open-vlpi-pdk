#!/usr/bin/env python3
"""OPENLLM-GITHUB2VLPI-002 Experiment A reference harness.

The service exposes only task operations. The reference transformation is an
implementation detail and is not returned by discovery or any task response.
This is computational reference evidence only; it is not physical validation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

EXPERIMENT = "OPENLLM-GITHUB2VLPI-002"
HARNESS_VERSION = "HARNESS-001"
TASK_VERSION = "A-1"
PHASES = [0.0, math.pi / 2.0, math.pi, 3.0 * math.pi / 2.0, 2.0 * math.pi]


def _reference_transform(amplitude: float, phase: float) -> float:
    # Deliberately private to the service contract. Do not expose this formula
    # through discovery or the task API.
    return amplitude * (1.0 - math.cos(phase))


def _token(value: Any) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


class ExperimentState:
    def __init__(self) -> None:
        self.states: dict[str, dict[str, Any]] = {}
        self.transitions: list[dict[str, Any]] = []
        self.observations: list[dict[str, Any]] = []
        self.contracts: list[dict[str, Any]] = []
        self.compositions: list[dict[str, Any]] = []

    def discover(self) -> dict[str, Any]:
        return {
            "experiment": EXPERIMENT,
            "harness": HARNESS_VERSION,
            "task": TASK_VERSION,
            "operations": [
                "discover",
                "create_state",
                "transition",
                "observe",
                "evaluate_contract",
                "compose",
            ],
            "input_state_schema": {
                "state_id": "string",
                "amplitude": "number",
                "phase": "number",
            },
            "transition_schema": {
                "state_id": "string",
                "phase_delta": "number",
            },
            "observation_schema": {
                "state_id": "string",
            },
            "contract_schema": {
                "observation_id": "string",
                "name": "string",
            },
            "composition_schema": {
                "first_state_id": "string",
                "second_phase_delta": "number",
            },
            "evidence": "computationally-demonstrated",
            "physical_validation": False,
        }

    def create_state(self, state_id: str, amplitude: float, phase: float) -> dict[str, Any]:
        if state_id in self.states:
            raise ValueError("state_id already exists")
        state = {
            "state_id": state_id,
            "amplitude": float(amplitude),
            "phase": float(phase),
        }
        self.states[state_id] = state
        return {"state": state, "state_token": _token(state)}

    def transition(self, state_id: str, phase_delta: float) -> dict[str, Any]:
        if state_id not in self.states:
            raise ValueError("unknown state_id")
        source = self.states[state_id]
        output = {
            "state_id": f"{state_id}.t{len(self.transitions)+1}",
            "amplitude": _reference_transform(source["amplitude"], source["phase"] + phase_delta),
            "phase": source["phase"] + phase_delta,
        }
        self.states[output["state_id"]] = output
        event = {
            "transition_id": f"T{len(self.transitions)+1}",
            "input_state_id": state_id,
            "phase_delta": float(phase_delta),
            "output_state_id": output["state_id"],
        }
        self.transitions.append(event)
        return {"transition": event, "output_state": output}

    def observe(self, state_id: str) -> dict[str, Any]:
        if state_id not in self.states:
            raise ValueError("unknown state_id")
        state = self.states[state_id]
        result = {
            "state_id": state_id,
            "residual_power": float(state["amplitude"]),
            "phase": state["phase"],
        }
        event = {
            "observation_id": f"O{len(self.observations)+1}",
            "state_id": state_id,
            "conditions": {"reference_model": True},
            "result": result,
        }
        self.observations.append(event)
        return event

    def evaluate_contract(self, observation_id: str, name: str) -> dict[str, Any]:
        obs = next((x for x in self.observations if x["observation_id"] == observation_id), None)
        if obs is None:
            raise ValueError("unknown observation_id")
        value = obs["result"]["residual_power"]
        if name == "finite_nonnegative":
            accepted = math.isfinite(value) and value >= 0.0
        elif name == "bounded_reference_power":
            accepted = math.isfinite(value) and 0.0 <= value <= 2.0
        else:
            raise ValueError("unknown contract name")
        event = {
            "contract_id": f"C{len(self.contracts)+1}",
            "observation_id": observation_id,
            "name": name,
            "verdict": "PASS" if accepted else "FAIL",
        }
        self.contracts.append(event)
        return event

    def compose(self, first_state_id: str, second_phase_delta: float) -> dict[str, Any]:
        first = self.transition(first_state_id, 0.0)
        second = self.transition(first["output_state"]["state_id"], second_phase_delta)
        event = {
            "composition_id": f"COMP{len(self.compositions)+1}",
            "first_transition_id": first["transition"]["transition_id"],
            "second_transition_id": second["transition"]["transition_id"],
            "result_state_id": second["output_state"]["state_id"],
            "accepted_interface": True,
        }
        self.compositions.append(event)
        return event


class Handler(BaseHTTPRequestHandler):
    server_version = "EIS-Experiment-A-Harness/001"

    def _write(self, status: int, payload: Any) -> None:
        body = json.dumps(payload, sort_keys=True).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path in ("/", "/discover"):
            self._write(200, self.server.state.discover())
        elif self.path == "/health":
            self._write(200, {"status": "ok", "experiment": EXPERIMENT, "harness": HARNESS_VERSION})
        else:
            self._write(404, {"error": "not_found"})

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", "0"))
        try:
            request = json.loads(self.rfile.read(length) or b"{}")
            op = self.path.rstrip("/").split("/")[-1]
            if op == "create_state":
                result = self.server.state.create_state(request["state_id"], request["amplitude"], request["phase"])
            elif op == "transition":
                result = self.server.state.transition(request["state_id"], request["phase_delta"])
            elif op == "observe":
                result = self.server.state.observe(request["state_id"])
            elif op == "evaluate_contract":
                result = self.server.state.evaluate_contract(request["observation_id"], request["name"])
            elif op == "compose":
                result = self.server.state.compose(request["first_state_id"], request["second_phase_delta"])
            else:
                self._write(404, {"error": "unknown_operation"})
                return
            self._write(200, {"result": result, "timestamp": time.time()})
        except Exception as exc:
            self._write(400, {"error": type(exc).__name__, "message": str(exc)})


def run(host: str, port: int) -> None:
    server = ThreadingHTTPServer((host, port), Handler)
    server.state = ExperimentState()
    print(f"EIS Experiment A harness listening on http://{host}:{port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    args = parser.parse_args()
    run(args.host, args.port)
