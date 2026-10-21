# EIS-KKA-EW4All-001 — Heavy-Rainfall / Flash-Flood Research Pilot

**Version:** 0.1.0  
**Status:** proposed pre-registration candidate; no data experiment run  
**Owner:** Earth ICT, SPC (EIS)

## Objective and claim boundaries

Determine whether a dynamic, KKA-inspired two-input interaction improves heavy-rainfall forecast quality or useful lead time against conventional software baselines.

Keep three claims separate:
1. **Forecast improvement:** quality or useful lead-time gain on held-out historical events.
2. **Operational warning readiness:** data latency, reliability, human procedures, and independent hazard validation.
3. **Photonic energy savings:** measured energy, latency, and quality at a matched service boundary versus a digital baseline.

This pilot can test claim 1. It does not establish claims 2 or 3 and does not issue public warnings.

## 1. Data manifest

**Initial scope:** continental United States, narrowed to a manageable region only after an auditable coverage/latency/label-density check. Do not choose the region by final-test performance.

| ID | Public dataset | Role | Caveat |
|---|---|---|---|
| D1 | NOAA MRMS quantitative precipitation estimate (QPE), exact product to be selected | Primary high-resolution rainfall reference; derive future-accumulation labels and recent-rainfall features | QPE is an estimate; record product, grid, cadence, version, latency and missingness |
| D2 | NASA GPM IMERG, exact product/version recorded | Complementary precipitation input and cross-product robustness analysis | Early/Late/Final products have different latency and retrospective quality |
| D3 | NOAA Storm Events and/or NOAA FLASH database | Documented flash-flood event labels for secondary task | Reports are incomplete and uncertain in space/time; unreported does not mean no flood |
| D4 | USGS Water Data / NWIS gauge observations where available | Independent streamflow or gauge-height evidence | Gauge coverage is uneven; freeze gauge-to-catchment matching and flood-stage provenance |
| D5 | ERA5, optional retrospective context | Antecedent wetness / atmospheric context sensitivity | Delayed reanalysis is not a real-time input unless replaced by a latency-compatible source |

Official entry points:
- MRMS: https://inside.nssl.noaa.gov/mrms/
- IMERG: https://gpm.nasa.gov/data/imerg
- NOAA Storm Events: https://www.ncei.noaa.gov/access/storm-events-database/
- NOAA FLASH: https://inside.nssl.noaa.gov/flash/database/
- USGS Water Data: https://waterdata.usgs.gov/
- ERA5: https://climate.copernicus.eu/climate-reanalysis

For every source file/product, manifest dataset ID, source URL, product/collection/version, retrieval time, valid-time interval, availability/publication time where known, CRS/grid/resolution, cadence, units, missing-value conventions, checksum, license/terms, and preprocessing-code version. Keep raw data immutable; derived datasets reference source checksums and transformation versions. Do not commit large raw datasets or credentials.

## 2. Tasks, labels and forecast horizons

### Primary task: heavy rainfall

At issue time t and grid cell g, predict whether future MRMS accumulation over horizon h exceeds pre-registered threshold q:

    y(g,t,h,q) = 1[ sum(P_MRMS(g,u), u in (t,t+h]) >= q ]

Horizons: **30, 60, and 120 minutes**. Candidate accumulation windows: 1-hour and 3-hour totals, selected to match cadence and operational relevance. Select q from an authoritative local operational threshold or training-period climatology, then freeze it before final-test evaluation. Report each horizon and threshold separately.

### Secondary task: flash-flood event / risk

Predict whether a documented flood event occurs within 1, 3, or 6 hours in a pre-defined area around the forecast grid/catchment. Before evaluation, define event-association radius, time tolerance, and gauge-stage/flow threshold. Store label provenance and uncertainty. Treat non-reported periods as uncertain/unlabeled where reporting completeness is unknown; do not blindly convert every non-event report into a negative label.

### Label integrity

- Inputs must have been available by issue time t, not merely valid at or before t.
- Targets use future valid times strictly after t.
- Keep data availability time separate from meteorological valid time.
- Spatial and temporal joins are explicit and deterministic.
- Missingness is represented; never silently forward-fill across target periods.
- Freeze threshold and event-matching rules before final-test evaluation.

## 3. Input groups and dynamic encoding

At each issue time t:
- **A — storm state:** recent MRMS or latency-compatible precipitation, rolling accumulations, intensity change, and local spatial summaries.
- **B — context:** antecedent precipitation/wetness and, if available by issue time, storm/environment context.

A and B are feature groups, not naturally optical fields. Any mapping into complex values is a model-design hypothesis; fit/define it on training data only, document it, then freeze it before final testing. Do not imply weather measurements themselves possess optical phase.

For a = A exp(i φa), b = B exp(i φb), the scalar signed cross-term is:

    X(a,b) = 2 Re(a conjugate(b)) = 2 A B cos(φa - φb)

For real-valued coordinates a=(ar,ai), b=(br,bi), use X = 2(ar br + ai bi).

Recompute both representations and X_t at every issue time using only information available then. Compare:
- dynamic A_t and B_t;
- static/time-averaged B;
- temporally shuffled B, preserving its distribution while breaking within-event temporal alignment;
- a conventional learned interaction under a comparable parameter/tuning budget.

## 4. Software baselines

All models share the same event splits, labels, permitted features and comparable tuning budgets.

- **B0 Persistence:** recent observed accumulation/event state as a transparent floor.
- **B1 Logistic regression:** interpretable feature baseline.
- **B2 Gradient-boosted trees:** strong tabular baseline (e.g. scikit-learn HistGradientBoostingClassifier or pinned equivalent).
- **B3 Temporal model:** small temporal convolution/ConvLSTM only after the tabular pipeline and data volume justify it.
- **K1 KKA-inspired interaction:** add the signed cross-term between A and B to a fixed baseline architecture.
- **Ablations:** K1 with static B; K1 with shuffled B; conventional learned interaction.

The first software implementation delivers a reproducible tabular baseline and data/evaluation contract. It must not pretend real data were downloaded or a model trained when no manifest/data are present.

## 5. Split protocol

- Split by chronological blocks and storm/event identity, not random rows.
- Train on earlier events, validate on later events, final test on still-later events.
- Prevent storm episodes and overlapping future-label windows from crossing split boundaries.
- Where feasible, reserve a geographically distinct region for spatial generalization.
- Fit scalers, imputation, feature selection, phase/complex encoding and calibration on training/validation only as pre-specified; never fit them on final test.
- Publish event counts, class prevalence, missingness, region coverage and label uncertainty per split.
- Use event-level/block bootstrap intervals; adjacent frames and grid cells are not independent.

## 6. Metrics and success criteria

Report per horizon, threshold and region:
- probability of detection / recall, false-alarm ratio, critical success index (CSI), precision, PR-AUC, Brier score and reliability/calibration;
- event-level useful lead time, missed events, false alarms per event/day and uncertainty intervals;
- data latency and input availability at issue time;
- software runtime/resource use (descriptive unless measured under a matched protocol).

Before opening the final test set, freeze numeric minimum effects and tolerances based on validation distributions and operational stakeholder input. Candidate gate:
1. K1 improves held-out CSI or a pre-selected proper scoring rule over the strongest eligible baseline, with event-level uncertainty reported.
2. False-alarm rate remains within a pre-registered tolerance.
3. Calibration is no worse than a pre-registered tolerance, or the calibration penalty is explicitly accepted.
4. Any lead-time claim uses a pre-registered event/alert definition and minimum gain, and reports false alarms jointly.
5. Gains recur across independent storms and are not attributable to leakage, a single region or a single threshold.

v0.1.0 intentionally does not invent numeric pass thresholds. They must be set before final-test access, not retrofitted after seeing results.

## 7. Ablation matrix

| Run | Interaction | Context timing | Purpose |
|---|---|---|---|
| R0 | none / standard baseline | aligned | baseline |
| R1 | signed cross-term | dynamic, aligned | candidate |
| R2 | signed cross-term | static/time-averaged B | dynamic contribution |
| R3 | signed cross-term | event-shuffled or approved block-shuffled B | temporal-alignment control |
| R4 | conventional learned interaction | dynamic, aligned | generic-interaction comparison |
| R5 | signed cross-term | alternate pre-registered encoding | encoding sensitivity |

Record config/model hashes, seeds, event split IDs, manifest IDs, metrics, uncertainty intervals and run status. Record failed runs; do not silently remove them.

## 8. Evidence gates

- **G0 data feasibility:** manifest, provenance, coverage, latency, labels and split feasibility reviewed.
- **G1 formal/software semantics:** Lean contract and software reference agree on deterministic fixtures; no full cross-language proof implied.
- **G2 baseline:** conventional baseline results reproducible on frozen splits.
- **G3 KKA ablation:** dynamic candidate and controls evaluated on held-out events.
- **G4 independent review:** methodology, uncertainty and claim language reviewed.
- **G5 photonic feasibility:** only after G3 passes; map the specified operator and encoding to hardware, including E/O conversion, control, detector, loss and service-boundary costs.

Forecast improvement, operational warning readiness and photonic energy savings remain three separate claims. A software metric alone proves neither operational readiness nor energy savings.

## 9. Execution order

1. Audit product access, coverage, timestamps/latency, licensing and event density; publish manifest and feasibility report.
2. Freeze label definitions and chronological/event splits.
3. Implement and test persistence, logistic regression and gradient-boosting baselines on prepared data.
4. Implement KKA operator and dynamic/static/shuffled controls.
5. Evaluate held-out storms; publish positive and negative results.
6. Consider photonic mapping only after a robust predictive result.

**Version history:** v0.1.0 — initial proposed pre-registration candidate. Changes to labels, splits, encoding, metrics or thresholds after test results require a new version and a documented reason.
