# EIS-KKA-CRITICAL-PATH-001 — Dependency-Aware KKA Schedule

**Status:** Synthetic schedule model; candidate hypothesis only.  
**Owner:** Earth ICT, SPC (EIS)  
**Purpose:** Compare the existing serial-additive reference with one explicit dependency-aware candidate.  
**Physical validation:** None. No PDK netlist, FDTD/EM simulation, fabrication, or measurement is claimed.

## 1. Narrow service and boundary

The service is a **top-k selected-block KKA operation**: given a query and the KV-block set selected by PRISM and the Thresholder, compute the KKA result and make the result available at the declared ADC output boundary. The modeled end-to-end timing boundary starts at DAC input presentation and ends when ADC output is available. The competition target is 200 ps for this explicitly declared boundary; quality equivalence to a conventional digital implementation remains an acceptance prerequisite and is not yet established.

## 2. Baseline: preserve EIS-CRC-BUDGET-001

The existing fixture remains unchanged as the serial reference:

| Stage | Duration (ps) | Cumulative (ps) |
|---|---:|---:|
| DAC | 10 | 10 |
| Modulator | 5 | 15 |
| PRISM | 40 | 55 |
| Thresholder | 30 | 85 |
| KKA | 120 | 205 |
| Photodetector | 15 | 220 |
| ADC | 8 | 228 |

The serial reference is 228 ps, 28 ps over the 200 ps target. It is synthetic regression data, not a measurement.

## 3. Candidate dependency graph

```text
DAC(10) -> Modulator(5) -> PRISM(40) -> Thresholder(30)
                                               |        |
                                           KKA A(60) KKA B(60)
                                               |        |
                                        Join/route/sync(15)
                                                   |
                                           Photodetector(15)
                                                   |
                                                ADC(8)
```

Dependencies asserted by this model:
- Modulator follows DAC.
- PRISM follows modulation.
- Thresholder follows PRISM results.
- KKA lanes follow the selected-block result from the Thresholder.
- Both KKA lanes can execute concurrently on independent partitions of that selected set.
- Join/routing/synchronization waits for both lanes before photodetection and ADC.

The first four are a proposed logical dependency structure to validate against the actual service implementation. **The two-lane independence and 60 ps per-lane latency are hypotheses**, not demonstrated KKA properties. The 15 ps join/routing/synchronization allowance is also hypothetical. The model excludes queueing, calibration, control settling, retries, thermal throttling, and unmodeled interface delays.

## 4. Arithmetic result

| Quantity | Result |
|---|---:|
| Serial-additive reference | 228 ps |
| Candidate critical path | 183 ps |
| Modeled improvement | 45 ps (19.7% vs. serial reference) |
| 200 ps target margin | 17 ps |
| Candidate target result | Pass in model only |

The candidate path is 10 + 5 + 40 + 30 + 60 + 15 + 15 + 8 = **183 ps**. Both KKA lanes start at 85 ps and finish at 145 ps; the join completes at 160 ps. The second lane adds concurrency and resource demand, not another 60 ps on the critical path. This result depends directly on the unvalidated two-lane assumption.

## 5. What this experiment answers—and does not

1. **Dependencies:** Encoded in the graph, but must be checked against the actual KKA service/dataflow. KKA cannot start before the selected-block output if that output defines its inputs.
2. **Concurrency:** Candidate lanes A and B overlap from 85–145 ps. Whether the operation can actually be partitioned without cross-lane dependencies is unproven.
3. **Overhead:** The candidate explicitly charges 15 ps for join, routing, and synchronization. This is a sensitivity input, not measured overhead. All omitted overhead must be added before acceptance.
4. **200 ps target:** The modeled critical path is 183 ps, with 17 ps margin. This is not evidence that a physical design meets the target.
5. **Energy and peak power:** **Not evaluable from current evidence.** Per-task energy and peak-power values are intentionally null rather than invented. Two concurrent lanes may increase instantaneous power even if latency falls. Populate energy per task, concurrency-aware supply/laser/control overhead, and a peak-power model from identified implementation/PDK data before making an energy or thermal claim.

## 6. Formal and executable checks

- `experiments/EIS-KKA-CRITICAL-PATH-001.json` is the schedule's declared input.
- `experiments/kka_critical_path.py` computes earliest start/finish times, critical path, target margin, and whether energy/power are evaluable. It rejects duplicate IDs, missing dependencies, cycles, and non-integer/negative durations.
- `tests/test_kka_critical_path_001.py` tests the 183 ps arithmetic, lane overlap, explicit missing energy/power data, and cycle rejection.
- `formal/lean4/EISVLPI/Fixtures/EIS_KKA_CRITICAL_PATH_001.lean` proves the declared integer arithmetic. It does not prove that the dependency graph matches the physical device or that parallel execution is implementable.

## 7. Gate decision

**Model gate:** Candidate passes the 200 ps arithmetic target under stated assumptions.  
**Architecture gate:** Open; establish actual KKA data dependencies and partitionability.  
**Energy/thermal gate:** Blocked on attributable energy and concurrency-aware peak-power inputs.  
**Implementation gate:** Open; connect this schedule to the actual photonic design and identified PDK, including routing, control, detectors, conversion, and calibration.  
**Physical gate:** Not run; requires design-bound simulation and then measurement.

Next action: map the selected-block KKA dataflow to the candidate DAG, annotate every task with measured or PDK-supported timing/energy/power bounds, and rerun the model. Do not treat the 183 ps result as a physical performance claim.
