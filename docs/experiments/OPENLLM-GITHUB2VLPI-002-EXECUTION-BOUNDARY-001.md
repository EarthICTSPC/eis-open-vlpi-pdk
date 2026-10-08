# OPENLLM-GITHUB2VLPI-002 — EXECUTION-BOUNDARY-001

**Status:** deployment-ready; public endpoint not yet provisioned  
**Experiment:** OPENLLM-GITHUB2VLPI-002 — Experiment A  
**Harness:** HARNESS-001  
**Repository:** `EarthICTSPC/eis-open-vlpi-pdk`

## 1. Purpose

Execution-BOUNDARY-001 crosses the boundary between a repository-runnable experiment and an independently executable experiment.

It does **not** modify Experiment A, its S/T/O/C candidate vocabulary, its task, its ablation matrix, its acceptance criteria, or its evidence rules.

The hosting platform is infrastructure, not experimental ontology.

## 2. Frozen experiment inputs

The external agent must use these exact artifacts from `main`:

- Experiment A specification: `docs/experiments/OPENLLM-GITHUB2VLPI-002-EXPERIMENT-A.md`
- Machine-readable experiment specification: `docs/experiments/EIS-OPENLLM-GITHUB2VLPI-002-STOC.yaml`
- Task interface specification: `task/task-specification.yaml`

At the time this boundary artifact was prepared:

- Experiment A revision: `7cfbf1624658d13f209630803bad4fa3fc7c7821`
- S/T/O/C YAML revision: `c7837e7ee4488112977058a158b7ad2cb7a860df7`
- Task interface revision: `4d6e2545bcb3e297d6022859fc56b77a4e2155a7`
- HARNESS-001 service revision: `c129fe173f0a9913ee110c738e086c2c000afdb0`
- MCP adapter revision: `7bf9567ec4596ae26388e31b9af33b8d2d206e5a`

These references are provenance metadata; they do not change the experiment.

## 3. Runtime classes

Every attempted independent execution MUST declare:

### Class A — MCP-capable execution runtime

The runtime can directly connect to and invoke the public HARNESS-001 MCP Streamable HTTP endpoint.

A Class A run may execute Experiment A.

### Class B — conversational/non-MCP runtime

The runtime cannot directly invoke the public HARNESS-001 MCP endpoint.

A Class B runtime MUST:

1. stop before experiment execution;
2. report F4 — Harness/tool failure;
3. identify the missing MCP-client capability;
4. emit no simulated trace;
5. make no claim about S/T/O/C sufficiency or necessity.

Class B is a deliberate negative control, not a failed vocabulary experiment.

## 4. Public transport boundary

The intended public endpoint is:

`https://<FLY_APP_NAME>.fly.dev/mcp`

The deployed service MUST use MCP Streamable HTTP as the external experiment transport.

The hosted service keeps one Machine running for this first experiment. This is intentional: HARNESS-001 currently holds task state in process memory, so automatic Machine stopping/restarting would create an avoidable session/state-continuity variable. Fly's current autostop/autostart behavior is designed to stop idle Machines and start them on traffic; EIS is deliberately not using that behavior for this stateful first boundary.

The raw HTTP operations implemented by HARNESS-001 are implementation infrastructure and are not an alternative independent-agent protocol.

The public service MUST expose no shell, arbitrary code execution, repository write access, Fly API access, secrets, arbitrary network fetch, agent spawning, or other general-purpose execution capability.

## 5. Fly deployment boundary

Fly.io is used only as hosting infrastructure for HARNESS-001.

The repository contains:

- `harness/Dockerfile`
- `fly.toml`
- `.github/workflows/deploy-harness.yml`

The deployment workflow is manual and targets the protected GitHub Actions environment `fly-production`.

Required EIS-controlled GitHub environment configuration:

- environment: `fly-production`
- secret: `FLY_API_TOKEN`
- variable: `FLY_APP_NAME`
- variable: `FLY_REGION`

Recommended initial application name:

`eis-github2vlpi-harness`

The application name may be changed if Fly requires another globally unique name; the endpoint recorded in the evidence must then use the actual deployed name.

No Fly credential is committed to the repository.

## 6. Transport acceptance gate

Before any independent model is invited to execute Experiment A, EIS MUST verify:

1. the Fly application is deployed;
2. HTTPS is active;
3. `GET /health` returns HTTP success;
4. MCP Streamable HTTP initialization succeeds;
5. MCP discovery succeeds;
6. all six Experiment A operations are callable;
7. malformed/unknown operations fail without exposing implementation internals;
8. the reference transformation remains absent from discovery/task responses;
9. physical validation remains explicitly false.

A successful health check alone does **not** constitute MCP transport acceptance.

## 7. Class-A execution gate

After transport acceptance, run exactly one independent Class-A agent before broad replication.

The agent receives only:

1. the unchanged Experiment A specification;
2. the machine-readable task/DSL specification;
3. the public HARNESS-001 MCP endpoint;
4. the minimum instructions needed to connect.

The agent MUST NOT receive prior EIS derivations, expected answers, preferred embodiments, or hidden reference implementation details.

The first Class-A run is a boundary test. It does not establish S/T/O/C sufficiency by itself.

## 8. Execution provenance record

Every Class-A attempt MUST record:

```
execution_id
model_identity
model_version
agent_identity
agent_version
runtime_class
mcp_client_identity
experiment_revision
stoc_spec_revision
task_revision
harness_revision
mcp_adapter_revision
endpoint
transport
prompt
supplied_vocabulary
state_events
transition_events
observation_events
contract_events
composition_events
import_attempts
failures
retries
human_interventions
evidence_classification
```

The endpoint is recorded as provenance, not as an experimental variable.

## 9. P5 execution provenance

The execution record MUST distinguish at least:

- **P5a:** execution performed through an independently reachable execution boundary;
- **P5b:** execution record includes sufficient provenance for independent replay/audit;
- **P5c:** externally reproduced execution by another independent runtime.

The exact P5 promotion rules remain those established by the project's existing evidence discipline; this artifact does not redefine them.

## 10. F4 handling

F4 includes failure of:

- public transport;
- MCP initialization;
- task-tool availability;
- required instrumentation;
- execution service availability;

when the failure is independent of the S/T/O/C vocabulary.

A Class B runtime is automatically F4 and MUST NOT attempt offline reconstruction.

## 11. Evidence boundary

HARNESS-001 produces computational reference evidence only.

No execution under this boundary may be promoted to:

- physical measurement;
- fabricated device evidence;
- PVR PASS;
- BIST PASS;
- foundry acceptance;
- physical validation;
- measured energy or thermal performance.

## 12. Deployment acceptance record

The repository contains `harness/transport_acceptance.py`, which is the authoritative transport/task-interface acceptance test for this boundary. It uses the official MCP Python SDK's Streamable HTTP client to verify tool discovery, the six bounded operations, the blindness/evidence boundary, composition, and malformed-input rejection. The SDK supports URL-based Streamable HTTP clients directly.

This test does **not** establish cryptographic P5 provenance. HARNESS-001 currently does not implement Ed25519 transcript signing, replay protection, or cross-session signature validation. Therefore N5/N6/N10-style cryptographic tests are **not** claimed, and no P5a cryptographic status is inferred from this transport test. Experiment A itself defines computational evidence classes and does not require cryptographic signing. Any future cryptographic provenance layer must be a separately specified artifact and must not be silently introduced here.

The first deployment should publish:

- deployed Fly app name;
- public MCP endpoint;
- deployed image/release identifier;
- Git commit;
- HARNESS-001 revision;
- health result;
- MCP initialization result;
- discovery result;
- six-operation availability result;
- timestamp;
- operator/human intervention record;
- evidence classification.

## 13. Independence and replication

Once one Class-A execution passes the execution boundary, replicate using independent runtimes.

Class-B negative controls may continue to be collected, but their F4 results MUST remain separated from Class-A experimental results.

Results MUST be stratified by:

```
runtime_class
model_family
model_version
agent/runtime
```

This prevents transport/runtime limitations from being mistaken for vocabulary findings.

## 14. Non-claims

This artifact does not establish:

- that S/T/O/C is sufficient;
- that any member is necessary;
- that S/T/O/C is minimal;
- that a new primitive is required;
- that the reference transformation represents a fabricated photonic device;
- that Fly.io is part of EIS's computational ontology.

## 15. Deployment/session assumptions

For the first deployment, `fly.toml` sets `auto_stop_machines = false`, `auto_start_machines = false`, and `min_machines_running = 1`. This is a deliberate experimental-continuity choice, not a general EIS hosting policy. Fly documents that `min_machines_running = 1` keeps one Machine warm, while automatic stopping can stop idle Machines.

The MCP Python SDK's current Streamable HTTP implementation also has a 30-minute default legacy-session idle timeout; HARNESS-001 makes that value explicit at 1800 seconds.

The first deployment intentionally uses one Machine. Multi-Machine scaling, shared session state, resumability, or persistent state are outside this boundary.

## 16. Decision gate

Execution-BOUNDARY-001 is complete when:

1. the public endpoint is reachable;
2. MCP Streamable HTTP initialization succeeds;
3. the bounded task interface is callable;
4. one Class-A runtime completes an end-to-end execution;
5. the execution record is captured with provenance;
6. the evidence boundary is preserved.

Only then should OPENLLM-GITHUB2VLPI-002 proceed to broad independent model replication.

**Working principle: Cross the execution boundary without changing the experiment.**
