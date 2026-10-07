# OPENLLM-GITHUB2VLPI-002-HARNESS-001

This directory makes Experiment A executable without changing the Experiment A specification.

## Boundary

The public Experiment A specification remains the authority:

- `docs/experiments/OPENLLM-GITHUB2VLPI-002-EXPERIMENT-A.md`
- `docs/experiments/EIS-OPENLLM-GITHUB2VLPI-002-STOC.yaml`

The harness is execution infrastructure, not an ontology decision.

It exposes a bounded reference task through these operations:

- `GET /discover`
- `POST /create_state`
- `POST /transition`
- `POST /observe`
- `POST /evaluate_contract`
- `POST /compose`

The reference transformation is an implementation detail of the service. It is intentionally absent from discovery metadata and task responses.

## Run locally

```bash
python3 harness/experiment_a_service.py --host 127.0.0.1 --port 8787
```

Then:

```bash
curl http://127.0.0.1:8787/discover
```

The service returns only computational reference evidence. It does not establish fabrication, measurement, PVR PASS, BIST PASS, foundry acceptance, or physical validation.

## Independent-agent rule

An independent agent should receive the unchanged Experiment A specification plus the public harness endpoint. It should not inspect or import the reference implementation as an expected answer.

## Hosting boundary

The repository now contains the executable harness and a deterministic self-test. A separately hosted endpoint is still required for a conversational agent that cannot clone/run repository code. Hosting is deployment infrastructure and does not change Experiment A.
