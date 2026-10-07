#!/usr/bin/env python3
"""Deterministic smoke test for HARNESS-001."""

import math
import threading
import urllib.request
import json
from http.server import ThreadingHTTPServer
from experiment_a_service import Handler, ExperimentState


def call(method, path, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(
        "http://127.0.0.1:18787" + path,
        data=data,
        method=method,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=3) as r:
        return json.loads(r.read())


server = ThreadingHTTPServer(("127.0.0.1", 18787), Handler)
server.state = ExperimentState()
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()

assert call("GET", "/discover")["experiment"] == "OPENLLM-GITHUB2VLPI-002"
call("POST", "/create_state", {"state_id": "S0", "amplitude": 1.0, "phase": 0.0})
t1 = call("POST", "/transition", {"state_id": "S0", "phase_delta": math.pi})["result"]
o1 = call("POST", "/observe", {"state_id": t1["output_state"]["state_id"]})["result"]
c1 = call("POST", "/evaluate_contract", {"observation_id": o1["observation_id"], "name": "bounded_reference_power"})["result"]
assert c1["verdict"] == "PASS"
comp = call("POST", "/compose", {"first_state_id": "S0", "second_phase_delta": math.pi / 2})["result"]
assert comp["accepted_interface"] is True

print("HARNESS-001 SELFTEST: PASS")
server.shutdown()
