# ENERGY OBJECTIVE SUPERSESSION — 2026-09-05

> **This section supersedes older hard-coded 10-GJ AGMINER objective language below.**

```text
CURRENT_HARD_OBJECTIVE =
E_CONSERVATIVE_COMPLETE_OPERATING < 10 MJ

EXACT_10_MJ =
REJECT

CONFIG_SOURCE =
config/agminer_032a.json

SUPPORTED_UNITS =
J kJ MJ GJ TJ

PHYSICAL_CANDIDATE_ID_DEPENDS_ON_TARGET =
NO

OBJECTIVE_REJECTION_MEMORY =
POLICY_SPECIFIC
```

Future energy-target changes are configuration changes and do not require rewriting the miner source.

---

# AGMINER BUILD PLAN

## Automated Antigravity Model Discovery, Rejection Memory, and Certification Shortlisting

**Project:** ANTIGRAVITY_RESEARCH
**Subsystem:** AGMINER
**Initial branch:** 032A
**Purpose:** Automated low-compute discovery and screening of antigravity model candidates before expensive certification
**Primary hard objective:** Complete conservative operating energy at or below **10 GJ**

---

# 1. Mission

AGMINER is an automated candidate-discovery and screening system for ANTIGRAVITY_RESEARCH.

Its job is **not** to certify models.

Its job is to:

1. generate large numbers of candidate parameter points cheaply;
2. reject impossible or unattractive models as early as possible;
3. permanently remember rejected candidates so exact failures are not repeatedly evaluated;
4. preserve only compact numerical metadata for ordinary failures;
5. retain richer data only for exceptionally promising candidates;
6. identify the lowest-energy physically credible survivors;
7. produce a small ranked shortlist for later manual or automated certification.

The intended workflow is:

```text
CHEAP THEORY FILTERS
        ↓
CHEAP MODEL GENERATION
        ↓
CHEAP FIELD SOLVE
        ↓
HARD 10-GJ ENERGY GATE
        ↓
FINITE-PAYLOAD / CONSERVATION / NATURALNESS FILTERS
        ↓
CHEAP STABILITY PROXIES
        ↓
PARETO FRONTIER
        ↓
SMALL HIGH-QUALITY SHORTLIST
        ↓
EXPENSIVE CERTIFICATION OUTSIDE AGMINER
```

AGMINER must optimize for **information gained per unit compute**, not for the number of simulations completed.

---

# 2. Permanent 10 GJ Rule

The central AGMINER rule is:

```text
ENERGY_LIMIT_J = 1.0e10
ENERGY_LIMIT_GJ = 10.0
```

The primary energy quantity is:

```text
E_CONSERVATIVE_COMPLETE_OPERATING
```

A model survives the energy gate only when:

```math
E_{\rm conservative,complete}
\le
10^{10}\ {\rm J}.
```

Therefore:

```text
E <= 10.000000 GJ
    MAY CONTINUE

E > 10.000000 GJ
    REJECT
```

A candidate exceeding 10 GJ is classified:

```text
REJECTED_ENERGY_GT_10GJ
```

and its exact candidate fingerprint is permanently entered in the rejection database.

AGMINER must never automatically reconsider that exact rejected candidate.

The candidate may only be reconsidered if:

```text
THE THEORY CHANGES
THE ENERGY LEDGER CHANGES
THE IMPLEMENTATION VERSION CHANGES IN A PHYSICALLY MATERIAL WAY
OR THE USER EXPLICITLY REQUESTS REOPENING
```

Changing only numerical resolution does not create a new physical model.

---

# 3. What Counts Toward the 10 GJ Limit

The energy limit is deliberately conservative.

The primary ranking ledger must include all positive energy that must physically exist in the operating configuration.

Where applicable:

```text
SOURCE FIELD ENERGY
MEDIATOR / SCALAR SELF-ENERGY
ACTIVATION FIELD ENERGY
RESERVOIR ENERGY
GATE FIELD ENERGY
CONTROL FIELD INVENTORY
MANDATORY SUPPORT ENERGY
MANDATORY STABILIZATION ENERGY
GAUGE-FIELD ENERGY
TOPOLOGICAL SECTOR ENERGY
SELF-FIELD ENERGY
REACTION / BACKREACTION CONTRIBUTIONS
UNAVOIDABLE CONFINEMENT ENERGY
OTHER PHYSICAL SCAFFOLDING
```

The miner must preserve a separate exact Hamiltonian ledger where useful, but:

> **Negative binding or interaction energy must not be used to sneak a candidate under the 10 GJ objective if the conservative complete inventory remains above 10 GJ.**

This follows the lesson from 031D3D2-R.

Store at minimum:

```text
E_EXACT_HAMILTONIAN_J
E_CONSERVATIVE_COMPLETE_J
E_SOURCE_J
E_MEDIATOR_J
E_ACTIVATION_J
E_RESERVOIR_J
E_CONTROL_J
E_SUPPORT_J
E_OTHER_J
```

The hard AGMINER energy gate uses:

```text
E_CONSERVATIVE_COMPLETE_J
```

not the most optimistic ledger available.

---

# 4. Lower-Bound Early Rejection

AGMINER should avoid solving a PDE if algebra already proves the model cannot beat 10 GJ.

Every family must expose:

```python
energy_lower_bound(params)
```

If:

```text
ENERGY_LOWER_BOUND_J > 1.0e10
```

then immediately classify:

```text
REJECTED_ANALYTIC_ENERGY_LOWER_BOUND_GT_10GJ
```

No field solve is performed.

This is one of the highest-value efficiency features in the entire miner.

Similarly, if one unavoidable component alone exceeds 10 GJ:

```text
E_SOURCE_LOWER_BOUND > 10 GJ

or

E_MEDIATOR_LOWER_BOUND > 10 GJ

or

E_ACTIVATION_LOWER_BOUND > 10 GJ

or

E_SUPPORT_LOWER_BOUND > 10 GJ
```

then the complete model is automatically impossible under the current objective.

Reject immediately.

---

# 5. Historical Models Under the New Objective

Existing models must not be forgotten, but AGMINER must distinguish:

```text
SCIENTIFICALLY FALSIFIED

from

OBJECTIVE-REJECTED
```

Historical examples such as:

```text
~82.75 GJ prescribed-source oracle
~96.14 GJ microscopic edge source
~103 GJ morphology source
~121.55 GJ robust microscopic source
~127.78 GJ activated conservative ON configuration
~273.46 GJ centered Q-ball
~575 GJ minimal B7 scalar dressing
```

are not all physically falsified.

They are, however, all above the AGMINER objective.

Preload their fingerprints or representative parameter records as:

```text
REJECTED_ENERGY_GT_10GJ
HISTORICAL_OBJECTIVE_REJECTION=TRUE
```

The miner may use them as training/control data.

It must not promote them to the new shortlist.

---

# 6. AGMINER Is a Discovery System, Not an Unbounded Theory Generator

AGMINER cannot intelligently search arbitrary mathematical laws.

It searches **parameterized theory families**.

Every theory family must be explicitly defined before AGMINER searches it.

Examples might eventually include:

```text
032_PROTECTED_PNGB_METRIC_SCALAR

032_TWIN_PROTECTED_QUADRATIC_SCALAR

032_MULTISCALAR_PROTECTED_CHARGE

032_SHIFT_SYMMETRIC_ACTIVATION

OTHER_EXPLICITLY_DEFINED_PROTECTED_FAMILY
```

The old 031 family should be included as a control implementation.

That is useful because AGMINER should correctly rediscover that:

```text
031 CAN LOOK EXCELLENT CLASSICALLY
BUT
031 FAILS THE NEW <=10-GJ OBJECTIVE
AND
031 FAILS RADIATIVE NATURALNESS
```

This becomes a powerful regression test for the miner itself.

---

# 7. Theory-Family Plugin Contract

All searchable families must implement a common interface.

Suggested package:

```text
src/antigravity_research/agminer/
```

Suggested family interface:

```python
class TheoryFamily:

    family_id()
    family_version()

    parameter_schema()

    sample_bounds()

    canonicalize_params(params)

    analytic_precheck(params)

    energy_lower_bound(params)

    naturalness_precheck(params)

    eft_precheck(params)

    build_initial_guess(params, neighbor=None)

    solve_coarse(params, initial_guess=None)

    reconstruct_observables(solution, params)

    estimate_complete_energy(solution, params)

    finite_payload_response(solution, params)

    conservation_checks(solution, params)

    cheap_stability_checks(solution, params)

    leakage_checks(solution, params)

    backreaction_checks(solution, params)

    serialize_survivor(solution, params)

    certify_not_implemented()
```

AGMINER itself should contain no theory-specific equations.

Theory physics belongs in family plugins.

---

# 8. Mandatory Theory-Level Preflight

Before numerical field solving, every candidate must pass the cheapest theory checks available.

Possible failure codes:

```text
FAIL_UNBOUNDED_HAMILTONIAN

FAIL_GHOST

FAIL_WRONG_KINETIC_SIGN

FAIL_TACHYONIC_OFF_VACUUM

FAIL_NO_CONSERVED_CHARGE

FAIL_NO_UNIVERSAL_PHYSICAL_METRIC

FAIL_PRESCRIBED_SPATIAL_COUPLING

FAIL_PRESCRIBED_SPATIAL_MEDIATOR_MASS

FAIL_NONLOCAL_UNCONTROLLED_SOURCE

FAIL_WRONG_FORCE_SIGN

FAIL_RANGE

FAIL_ANALYTIC_ENERGY_BOUND

FAIL_EFT

FAIL_NATURALNESS

FAIL_EMPIRICAL_STRUCTURE
```

These should occur before any expensive BVP whenever possible.

---

# 9. Naturalness Moves to the Front

031 demonstrated that naturalness cannot remain a final test.

AGMINER must perform radiative-naturalness screening before expensive stability work.

At minimum, each family must state:

```text
ULTRALIGHT_MODE_MASS
COUPLING_SCALE
DECLARED_EFT_CUTOFF
RELEVANT_HEAVY_THRESHOLDS
RADIATIVE_PROTECTION_MECHANISM
PROTECTION_SYMMETRY
PROTECTION_BREAKING_PARAMETERS
EXPECTED_LOOP_CORRECTION
```

A family cannot pass merely because it labels itself:

```text
PROTECTED
```

Protection must have an explicit calculable mechanism.

Examples of acceptable evidence:

```text
SHIFT SYMMETRY
PNGB STRUCTURE
TWIN / MIRROR CANCELLATION
SUPERSYMMETRIC CANCELLATION
SEQUESTERING
OTHER EXPLICIT LOOP-CANCELLATION MECHANISM
```

The miner must calculate a quantitative naturalness margin such as:

```math
{\cal N}
=
\frac{m_{\rm intended}^2}
{|\delta m^2|}.
```

or equivalently:

```text
DELTA_M2_OVER_M2
```

Suggested initial hard preflight:

```text
DELTA_M2_OVER_M2 <= 10
```

unless an explicit protection mechanism calculates the cancellation rather than assuming it.

Unprotected 031 should fail here immediately.

---

# 10. Standard Physical Benchmark

Candidates must be compared on the same finite-payload target.

Initial AGMINER benchmark:

```text
PAYLOAD_MASS_KG = 1.0

PAYLOAD_RADIUS_M = 0.10

TARGET_ADVERSE_SURFACE_ACCEL_MPS2 = 9.80665

TARGET_CM_ACCEL_MPS2 >= 9.80665
```

The source morphology may vary.

The payload benchmark does not.

Primary finite-payload success requires:

```text
PAYLOAD_CM_OUTWARD = TRUE

PAYLOAD_SURFACE_MIN >= 9.80665 m/s^2

NO_PAYLOAD_INTERSECTION_WITH_SOURCE

SOURCE_OVERLAP BELOW FAMILY LIMIT
```

The miner must optimize the actual finite payload.

Do not rank candidates using only:

```text
POINT FORCE
CENTER FORCE
MAXIMUM LOCAL FORCE
SCALAR CHARGE ALONE
```

---

# 11. Standard Candidate Objective

A candidate must first satisfy all hard gates.

Only then is it ranked.

Primary ranking quantity:

```text
E_CONSERVATIVE_COMPLETE_J
```

Primary goal:

```text
MINIMIZE E_CONSERVATIVE_COMPLETE_J
```

subject to:

```text
E <= 10 GJ

FINITE PAYLOAD >= 1g

POSITIVE HAMILTONIAN

CONSERVATION

REQUIRED ENERGY CONDITIONS

BOUND / LOCALIZED SOURCE

LOW LEAKAGE

ACCEPTABLE PAYLOAD BACKREACTION

NATURALNESS

EFT VALIDITY

NO OBVIOUS INSTABILITY
```

Secondary useful metric:

```math
\eta_{\rm AG}
=
\frac
{a_{\rm useful,payload}}
{E_{\rm conservative,complete}}.
```

Also record:

```text
SCALAR_CHARGE_PER_JOULE
PRODUCTIVE_PARTICIPATION
KERNEL_LEVERAGE
CANCELLATION
SOURCE_TAIL_TAX
MEDIATOR_SELF_ENERGY_TAX
STABILITY_TAX
ACTIVATION_TAX
CONTROL_TAX
SCAFFOLDING_TAX
```

These preserve the useful Introspective lessons.

---

# 12. Hard Gates Versus Ranking Metrics

Never combine physical validity and desirability into one opaque score.

First:

```text
PASS / FAIL
```

Then rank survivors.

Hard gates include:

```text
THEORY_VALIDITY
NATURALNESS
EFT
ENERGY <= 10 GJ
FINITE-PAYLOAD SIGN
SURFACE >= 1g
POSITIVE ENERGY
CONSERVATION
LOCALIZATION
LEAKAGE LIMIT
BACKREACTION LIMIT
CHEAP STABILITY REQUIREMENT
```

Ranking metrics include:

```text
LOWER ENERGY
MORE ENERGY MARGIN
MORE LEAKAGE MARGIN
MORE NATURALNESS MARGIN
MORE STABILITY MARGIN
MORE PAYLOAD MARGIN
LESS CANCELLATION
LESS SCAFFOLDING
LESS CONTROL ENERGY
GREATER DISTANCE FROM PARAMETER BOUNDARIES
```

---

# 13. Multi-Fidelity Screening Pipeline

## Tier 0 — Algebraic / Analytical

Target cost:

```text
MICROSECONDS TO MILLISECONDS
```

Checks:

```text
DEDUPE

KNOWN FAILURE LOOKUP

DIMENSIONAL CONSISTENCY

SIGN CHECK

BOUNDED HAMILTONIAN

GHOST / TACHYON PRECHECK

RANGE

NATURALNESS

EFT

ANALYTIC ENERGY LOWER BOUND

COUPLING LIMITS

OFF-STATE STRUCTURE

UNIVERSAL METRIC STRUCTURE
```

If Tier 0 fails, do not solve a field equation.

---

## Tier 1 — Coarse Field Existence

Target:

```text
CHEAP RADIAL / REDUCED SOLVE
```

Use modest resolution.

No expensive angular spectrum.

No dense stability matrix.

No Einstein solve.

No nonlinear evolution.

Outputs:

```text
FIELD_EXISTENCE

COARSE_ENERGY

NOETHER_CHARGE

E_OVER_QM

LOCALIZATION

SOURCE_RADIUS

TAIL_AMPLITUDE

COARSE_CONSERVATION_RESIDUAL
```

Immediately apply the 10 GJ gate.

If:

```text
E_COMPLETE_ESTIMATE > 10 GJ
```

record:

```text
REJECTED_ENERGY_GT_10GJ
```

and stop.

---

## Tier 1B — Cheap Finite-Payload Physics

For sub-10-GJ field solutions only.

Compute:

```text
PAYLOAD_CM_ACCEL

PAYLOAD_SURFACE_MIN

PAYLOAD_SURFACE_MAX

SOURCE_OVERLAP

LEAKAGE

BACKREACTION_PROXY

PRODUCTIVE_KERNEL_PARTICIPATION

CANCELLATION_RATIO
```

Reject immediately if finite-payload true antigravity fails.

---

## Tier 1C — Cheap Stability

Only after energy and payload success.

Possible tests:

```text
dQ/domega

dE/dQ consistency

LOWEST RADIAL HESSIAN EIGENVALUE

SELECTED LOW-l MODES

NO OBVIOUS TACHYON

TRANSLATIONAL ZERO-MODE SANITY CHECK
```

Do not run the R3-R5 certification stack here.

The purpose is only to remove obviously unstable candidates.

---

## Tier 2 — Shortlist Screening

Only a small fraction of Tier-1 survivors should reach Tier 2.

Suggested target:

```text
TOP 0.1% TO 1%
```

Tier 2 adds:

```text
HIGHER GRID

DOMAIN CHECK

ALTERNATE BOUNDARY CONDITION

PARAMETER PERTURBATIONS

LEAKAGE ROBUSTNESS

BACKREACTION ROBUSTNESS

SEVERAL ANGULAR MODES

ENERGY RECONSTRUCTION

INDEPENDENT FORCE RECONSTRUCTION

NATURALNESS RECHECK

EFT RECHECK
```

A Tier-2 candidate exceeding 10 GJ after better reconstruction is immediately reclassified:

```text
REJECTED_ENERGY_GT_10GJ
```

Tier 1 survival does not grandfather it in.

---

## Tier 3 — Certification Handoff

AGMINER does not perform full Tier 3.

It exports a certification packet.

Possible later gates:

```text
FULL COUPLED SPECTRUM

GOLDSTONE PROJECTION

NONLINEAR STABILITY

ACTIVATION

RESERVOIR

SWITCHING

FULL T_MUNU

EINSTEIN / PHYSICAL METRIC

RADIATION

FULL NATURALNESS

EMPIRICAL CLOSURE

SUPPORT / PRACTICALITY
```

---

# 14. Candidate State Machine

Every model has one persistent state.

Suggested states:

```text
NEW

TIER0_RUNNING

REJECTED_TIER0

TIER1_RUNNING

REJECTED_NUMERICAL

REJECTED_ENERGY_GT_10GJ

REJECTED_PAYLOAD

REJECTED_CONSERVATION

REJECTED_NATURALNESS

REJECTED_EFT

REJECTED_STABILITY

REJECTED_LEAKAGE

REJECTED_BACKREACTION

TIER1_SURVIVOR

TIER2_RUNNING

TIER2_SURVIVOR

CERTIFICATION_READY

CERTIFICATION_IN_PROGRESS

CERTIFIED

INVALIDATED_BY_LATER_GATE
```

Terminal rejection states must be explicit.

---

# 15. Rejection Memory

This is mandatory.

AGMINER must have persistent failure memory.

Each candidate receives a deterministic fingerprint from:

```text
FAMILY_ID
FAMILY_VERSION
CANONICAL_PARAMETER_VECTOR
PHYSICAL_MODEL_VERSION
ENERGY_LEDGER_VERSION
```

Example:

```python
candidate_id = sha256(canonical_bytes).hexdigest()[:24]
```

The hash is an identifier only.

Do not use encoded source code.

Before evaluating any candidate:

```text
LOOK UP candidate_id
```

If the ID already exists with a terminal state:

```text
SKIP
```

Print only:

```text
SKIP_KNOWN=<candidate_id>
```

if useful.

Do not recompute it.

---

# 16. Exact Failure Memory Versus Region Exclusion

One failed point does not automatically prove its neighbors fail.

Therefore AGMINER must distinguish:

```text
EXACT_REJECTION

from

PROVEN_REGION_REJECTION
```

An exact 12-GJ candidate means:

```text
THAT EXACT MODEL IS DEAD FOR AGMINER
```

It does not automatically prove a nearby parameter point cannot reach 9 GJ.

Regions may only be banned when there is a mathematical or monotonic justification.

Examples:

```text
ANALYTIC LOWER BOUND

MONOTONIC ENERGY THEOREM

NO-GO CONDITION

INVALID PARAMETER DOMAIN

GHOST REGION

RANGE IMPOSSIBILITY REGION
```

Otherwise use the failure only to reduce sampling priority, not to ban the neighborhood.

---

# 17. Failure Codes

Use small machine-readable codes.

Suggested core codes:

```text
E001 ENERGY_LOWER_BOUND_GT_10GJ

E002 ENERGY_COARSE_GT_10GJ

E003 ENERGY_REFINED_GT_10GJ

T001 UNBOUNDED_HAMILTONIAN

T002 GHOST

T003 WRONG_KINETIC_SIGN

T004 OFF_TACHYON

T005 NO_UNIVERSAL_METRIC

T006 HAND_PRESCRIBED_LOCAL_PARAMETER

N001 NATURALNESS

N002 EFT_CUTOFF

N003 PROTECTION_UNSPECIFIED

F001 NO_FIELD_SOLUTION

F002 NONLOCALIZED

F003 E_OVER_QM_FAIL

P001 PAYLOAD_CM_SIGN

P002 PAYLOAD_SURFACE_LT_1G

P003 SOURCE_OVERLAP

P004 WRONG_SIDEDNESS

C001 CONSERVATION

C002 POSITIVE_ENERGY

C003 DEC

S001 RADIAL_INSTABILITY

S002 CHEAP_ANGULAR_INSTABILITY

L001 LEAKAGE

B001 BACKREACTION

R001 RANGE

D001 DUPLICATE

X001 TIMEOUT

X002 NUMERICAL_UNRESOLVED
```

A human-readable explanation may be generated from the code when reports are produced.

Do not store large repeated error strings for every candidate.

---

# 18. Numerical Failure Is Not Physics Failure

Distinguish:

```text
PHYSICS_REJECTED

from

NUMERICALLY_UNRESOLVED
```

A failed BVP should not automatically become:

```text
MODEL_PHYSICALLY_IMPOSSIBLE
```

Suggested policy:

1. first solve attempt;
2. one cheap alternate seed / continuation attempt;
3. if both fail, classify:

```text
NUMERICAL_UNRESOLVED
```

AGMINER should not repeatedly retry it during the same mining campaign.

It may be manually revisited later.

Above-10-GJ results, by contrast, are genuine objective rejections and need no retry.

---

# 19. Search Strategy

Do not use a giant rectangular grid.

Initial search mix:

```text
60% GLOBAL EXPLORATION

30% LOCAL EXPLOITATION

10% NOVELTY / BOUNDARY EXPLORATION
```

---

# 20. Global Exploration

Use low-discrepancy sampling.

Preferred:

```python
scipy.stats.qmc.Sobol
```

or:

```python
LatinHypercube
```

Sobol is preferred for reproducible broad coverage.

Benefits:

```text
BETTER COVERAGE THAN RANDOM

DETERMINISTIC

RESUMABLE

CHEAP

NO NEW DEPENDENCY
```

Store:

```text
SAMPLER_SEED

SAMPLE_INDEX
```

so samples can be regenerated.

---

# 21. Local Exploitation

Once promising regions appear, seed local samples around Tier-1 or Tier-2 survivors.

Do not immediately run expensive gradient optimization.

Use cheap adaptive perturbations.

Example:

```text
PARENT = PROMISING CANDIDATE

PARAM_i_NEW
=
PARAM_i_PARENT
+
sigma_i * NORMAL(0,1)
```

Shrink `sigma` gradually when a cluster improves.

Maintain diversity so one basin does not monopolize the run.

---

# 22. Continuation

Continuation is especially important for nonlinear BVP families.

If candidate B is close to solved candidate A:

```text
USE A'S SOLUTION AS B'S INITIAL GUESS
```

This can reduce solve time dramatically.

A small in-memory nearest-neighbor cache may contain only recent successful coarse profiles.

Do not retain all profiles on disk.

---

# 23. Adaptive Search Budget

AGMINER should not have a fixed assumption about candidates per hour.

Measure:

```text
MEDIAN_TIER0_TIME

MEDIAN_TIER1_TIME

MEDIAN_TIER1B_TIME

MEDIAN_TIER1C_TIME
```

Then adapt.

Example target:

```text
>90% OF GENERATED POINTS SHOULD DIE BEFORE EXPENSIVE SCREENING

<10% SHOULD RECEIVE A FIELD SOLVE

<1% SHOULD RECEIVE STABILITY SCREENING

<0.1% SHOULD REACH TIER 2
```

If too many candidates reach expensive gates, strengthen cheap filters.

---

# 24. Pareto Frontier

Do not retain only one scalar score.

Maintain a Pareto frontier over:

```text
ENERGY

ENERGY_MARGIN_TO_10GJ

FINITE_PAYLOAD_MARGIN

NATURALNESS_MARGIN

STABILITY_MARGIN

LEAKAGE_MARGIN

BACKREACTION_MARGIN

EFT_MARGIN

CANCELLATION

CONTROL_ENERGY
```

The primary ordering remains energy.

The Pareto frontier prevents AGMINER from throwing away a slightly higher-energy but dramatically safer model.

Example:

```text
Candidate A:
2.1 GJ
barely stable
barely natural
leak near limit

Candidate B:
2.8 GJ
large stability margin
large naturalness margin
low leakage
```

Both belong on the frontier.

---

# 25. Certification Candidate Ranking

Produce several rankings.

```text
LOWEST_ENERGY

BEST_ROBUSTNESS

BEST_NATURALNESS

BEST_STABILITY_MARGIN

BEST_PAYLOAD_MARGIN

BEST_OVERALL_PARETO
```

Do not automatically certify only Rank #1.

Recommended final shortlist:

```text
3 TO 10 CANDIDATES
```

if that many genuinely survive.

---

# 26. Disk-Light Storage Architecture

Do not create one log file per candidate.

Do not save full field arrays for rejected candidates.

Do not save solver iteration histories unless debugging.

Primary persistent database:

```text
results/agminer/agminer.sqlite3
```

SQLite is preferred because it is:

```text
COMPACT

TRANSACTIONAL

CRASH RESISTANT

QUERYABLE

STANDARD LIBRARY

EASY TO RESUME

BETTER THAN THOUSANDS OF JSON FILES
```

---

# 27. Database Tables

Suggested tables:

## runs

```text
run_id
start_time
end_time
family_version
config_hash
sampler_seed
candidate_count
reject_count
survivor_count
best_energy_j
```

## models

Store only compact metadata.

```text
candidate_id
family_id
family_version
params_json_compact
state
tier
energy_j
payload_cm
payload_surface_min
naturalness_margin
stability_proxy
leakage
backreaction
runtime_s
created_run_id
```

## rejections

```text
candidate_id
family_id
fail_code
gate
energy_j
run_id
```

## survivors

```text
candidate_id
rank_energy
pareto
checkpoint_path
certification_priority
```

## region_rules

Only mathematically justified exclusions.

```text
family_id
rule_id
rule_type
bounds
reason
proof_reference
```

---

# 28. Compact Parameter Storage

Use compact canonical JSON:

```python
json.dumps(
    params,
    sort_keys=True,
    separators=(",", ":"),
)
```

Do not pretty-print per-candidate JSON.

Pretty reports are generated only for finalists.

---

# 29. Field-Array Retention Policy

Rejected candidate:

```text
KEEP NO FIELD ARRAYS
```

Ordinary Tier-1 survivor:

```text
KEEP NO FIELD ARRAYS AFTER OBSERVABLE EXTRACTION
```

Current Pareto frontier:

```text
OPTIONALLY KEEP DOWNSAMPLED CHECKPOINT
```

Top certification candidates:

```text
KEEP COMPRESSED NUMERICAL CHECKPOINT
```

Suggested cap:

```text
MAX_CHECKPOINTED_CANDIDATES = 25
```

When a new candidate enters the top set:

```text
SAVE IT
```

When one falls out:

```text
DELETE ITS CHECKPOINT
```

Database metadata remains.

---

# 30. Log Policy

No per-model logs.

Main mining log only:

```text
results/agminer/agminer_current.log
```

Use rotating logs.

Suggested:

```text
MAX LOG SIZE = 2 MB

BACKUP COUNT = 2
```

Maximum routine text-log footprint:

```text
~6 MB
```

Log only:

```text
RUN START

RUN END

EVERY N CANDIDATES

NEW BEST

NEW PARETO CANDIDATE

NEW FAILURE CLASS

UNEXPECTED EXCEPTION

DATABASE CHECKPOINT
```

Do not log every solver iteration.

Set numerical solver verbosity to zero during ordinary mining.

---

# 31. Progress Reporting

Terminal progress every:

```text
100 candidates
```

or every:

```text
60 seconds
```

whichever is less noisy.

Example:

```text
AGMINER
tested=12400
tier0_reject=11733
tier1_reject=641
tier1_survivor=26
tier2_survivor=3
best=2.84_GJ
db=18.4_MB
rate=127_candidates_min
```

That is sufficient.

---

# 32. Summary Files

Generate lightweight reports periodically:

```text
results/agminer/top_candidates.csv

results/agminer/pareto_frontier.csv

results/agminer/failure_counts.csv

results/agminer/run_summary.json
```

Overwrite these summaries.

Do not create timestamped copies every few minutes.

Only major campaign closeouts need archival snapshots.

---

# 33. Disk Budget

Initial target:

```text
DATABASE:
< 100 MB PER MAJOR CAMPAIGN

LOGS:
< 10 MB

CHECKPOINTS:
< 250 MB TOTAL

SUMMARY FILES:
< 5 MB
```

Preferred normal footprint:

```text
WELL BELOW 250 MB
```

even after many hours.

If the database exceeds its configured budget:

```text
STOP GENERATING NEW CANDIDATES
COMPACT
REPORT
```

Do not silently fill the drive.

---

# 34. SQLite Maintenance

Suggested operational settings:

```text
WAL MODE DURING ACTIVE RUN

PERIODIC TRANSACTION COMMITS

PERIODIC WAL CHECKPOINT

WAL TRUNCATE AT CLEAN SHUTDOWN
```

Do not commit after every tiny calculation if batching can be used.

Suggested database write batch:

```text
25 TO 100 RESULTS
```

Crash-loss tolerance should remain small.

---

# 35. Parallelism

AGMINER should support multiprocessing.

Do not allow worker processes to write SQLite directly.

Architecture:

```text
MAIN PROCESS
    ├── scheduler
    ├── rejection lookup
    ├── result writer
    └── progress reporter

WORKER 1
WORKER 2
WORKER 3
...
```

Workers return compact result dictionaries.

Only the main process writes the database.

This avoids SQLite lock contention and corrupted mixed logs.

---

# 36. CPU Budget

Default:

```text
WORKERS
=
max(1, CPU_COUNT - 1)
```

but permit a config override.

Do not automatically consume every core.

Leave one core for:

```text
OS
VS CODE
DATABASE WRITER
USER INTERACTION
```

---

# 37. Memory Budget

Workers must not accumulate solutions indefinitely.

After each candidate:

```text
EXTRACT OBSERVABLES

OPTIONALLY SERIALIZE IF TOP CANDIDATE

DELETE SOLUTION

RELEASE LARGE ARRAYS
```

Warm-start caches should be bounded.

Example:

```text
MAX_WARM_STARTS_PER_WORKER = 8
```

---

# 38. Candidate Timeouts

Tier-1 searches are supposed to be cheap.

Set configurable soft limits.

Example initial values:

```text
TIER0_TARGET < 0.01 s

TIER1_SOFT_TARGET < 3 s

TIER1_TIMEOUT = 15 s

TIER1C_TIMEOUT = 30 s

TIER2 = SEPARATE QUEUE
```

A timeout is:

```text
NUMERICAL_UNRESOLVED
```

not a physics falsification.

---

# 39. Search Queues

Use separate queues:

```text
DISCOVERY_QUEUE

LOCAL_REFINEMENT_QUEUE

TIER2_QUEUE
```

The main mining process should prioritize broad cheap discovery.

Tier 2 should never starve Tier 0/1 discovery.

Possible allocation:

```text
70% WORKER TIME = DISCOVERY

20% = LOCAL REFINEMENT

10% = TIER2
```

Adjust based on results.

---

# 40. Fail-Fast Evaluation Order

Every candidate should be processed in approximately this order:

```text
1. CANONICALIZE PARAMETERS

2. GENERATE CANDIDATE ID

3. CHECK DATABASE

4. CHECK PROVEN REGION RULES

5. DIMENSIONAL CHECK

6. THEORY HEALTH

7. NATURALNESS

8. EFT

9. RANGE

10. ENERGY LOWER BOUND

11. COARSE FIELD EXISTENCE

12. COARSE COMPLETE ENERGY

13. HARD <=10-GJ GATE

14. FINITE-PAYLOAD RESPONSE

15. SOURCE / PAYLOAD OVERLAP

16. LEAKAGE

17. CONSERVATION

18. POSITIVE ENERGY / DEC IF REQUIRED

19. BACKREACTION PROXY

20. CHEAP STABILITY

21. ROBUSTNESS MARGIN

22. PARETO / RANKING UPDATE
```

Expensive work must always occur as late as possible.

---

# 41. Energy Short-Circuiting Inside Solvers

If energy can be accumulated during integration, allow early termination.

For example:

```text
PARTIAL POSITIVE ENERGY
>
10 GJ
```

implies:

```text
FULL POSITIVE ENERGY
>
10 GJ
```

if the remaining terms are nonnegative.

Then terminate the solve or postprocessing immediately.

Record:

```text
REJECTED_PARTIAL_ENERGY_GT_10GJ
```

This can save considerable compute.

Only use this when monotonic positivity is mathematically valid.

---

# 42. Candidate Fingerprint Versioning

Candidate identity must include physics-version provenance.

Otherwise an old failure could incorrectly suppress a new theory.

Include:

```text
FAMILY_ID
FAMILY_VERSION
ACTION_VERSION
LEDGER_VERSION
PAYLOAD_BENCHMARK_VERSION
PARAMETER_VECTOR
```

Thus:

```text
031 v1
```

and:

```text
032 protected v1
```

cannot collide even if numerical parameters look similar.

---

# 43. Reproducibility

Every survivor must be reproducible from:

```text
candidate_id

family_id

family_version

parameter vector

sampler seed / sample index if applicable

solver version

screening thresholds

benchmark version
```

Central claims must not depend on terminal logs.

This follows the project's existing documentation rule that central results must be reconstructible without chat history.

---

# 44. Baseline Regression

Before a major AGMINER campaign:

```text
94 KNOWN SOLUTIONS MUST PASS
```

Do not run the full baseline before every candidate.

Run it:

```text
ON CAMPAIGN START

AFTER CODE CHANGES

BEFORE PROMOTING FINALISTS
```

This avoids wasting compute.

---

# 45. AGMINER-Specific Tests

Add unit/regression tests.

Suggested:

```text
test_energy_limit_exact_10gj_passes.py

test_energy_limit_above_10gj_rejects.py

test_candidate_hash_deterministic.py

test_duplicate_candidate_skipped.py

test_rejection_persists_restart.py

test_historical_031_rejected_energy.py

test_031_naturalness_rejected.py

test_sqlite_resume.py

test_pareto_frontier.py

test_no_rejected_checkpoint_retained.py

test_log_rotation.py

test_region_rule_requires_proof_flag.py

test_numerical_failure_not_physics_failure.py
```

---

# 46. Critical 10 GJ Regression Tests

These are mandatory.

Test:

```text
E = 9.999999999 GJ
PASS ENERGY GATE
```

Test:

```text
E = 10.000000000 GJ
PASS ENERGY GATE
```

Test:

```text
E = 10.000000001 GJ
REJECT
```

Avoid ambiguous floating-point comparisons by comparing joules with a clearly documented tolerance policy.

Recommended:

```text
NO PHYSICAL TOLERANCE ABOVE THE LIMIT
```

Numerical uncertainty should be handled separately.

---

# 47. Uncertain Energy Near 10 GJ

A coarse estimate can be uncertain.

Store:

```text
E_ESTIMATE

E_LOWER

E_UPPER
```

Policy:

```text
IF E_LOWER > 10 GJ:
    REJECT IMMEDIATELY

IF E_ESTIMATE > 10 GJ:
    REJECT EXACT CANDIDATE UNDER CURRENT COARSE MODEL

IF E_ESTIMATE <= 10 GJ BUT E_UPPER > 10 GJ:
    BORDERLINE
    REQUIRE REFINEMENT BEFORE SHORTLIST
```

A certification-ready candidate must satisfy:

```text
REFINED CONSERVATIVE COMPLETE ENERGY <= 10 GJ
```

with adequate numerical convergence.

---

# 48. Borderline Candidates

Do not let thousands of 9.99-GJ candidates consume Tier 2.

Give preference to genuine margin.

Define:

```text
ENERGY_MARGIN
=
10 GJ - E
```

Suggested categories:

```text
< 5 GJ
    EXCELLENT ENERGY CLASS

5–8 GJ
    STRONG

8–9.5 GJ
    MARGINAL BUT INTERESTING

9.5–10 GJ
    BORDERLINE
```

All may survive, but lower-energy models receive priority.

---

# 49. Initial AGMINER Campaign Target

The first production campaign should not attempt millions of expensive field solves.

Suggested initial campaign:

```text
TIER0 SAMPLES:
50,000–200,000

ACTUAL FIELD SOLVES:
1,000–10,000

TIER1C STABILITY:
<= 500

TIER2:
<= 50

CERTIFICATION SHORTLIST:
<= 10
```

Actual numbers should adapt to measured runtime.

---

# 50. Validation Campaign Before Real Discovery

Before trusting AGMINER on new physics, run a controlled validation.

Include known historical 031 points.

Expected outcomes:

```text
031 ~96 GJ
REJECT_ENERGY_GT_10GJ

031 ~103 GJ
REJECT_ENERGY_GT_10GJ

031 ~121/128 GJ
REJECT_ENERGY_GT_10GJ

031 ~273 GJ
REJECT_ENERGY_GT_10GJ
```

Also evaluate an unprotected 031-like low-energy synthetic point.

Expected:

```text
REJECT_NATURALNESS
```

This verifies that the exact failure which ended 031 is now caught near the beginning.

---

# 51. Search Metrics to Record

For every field-solved candidate, retain compact values where available:

```text
candidate_id

family_id

energy_exact_j

energy_conservative_j

energy_lower_j

payload_cm_mps2

payload_surface_min_mps2

payload_surface_max_mps2

source_charge

scalar_charge

charge_per_joule

E_over_Qm

source_radius

payload_distance

leakage

source_overlap

payload_backreaction

conservation_residual

DEC_margin

radial_stability_proxy

lowest_eigen_proxy

naturalness_ratio

naturalness_margin

EFT_margin

range_m

productive_participation

cancellation_ratio

kernel_leverage

control_energy_j

activation_energy_j

runtime_s

state

fail_code
```

No field arrays required for rejected candidates.

---

# 52. Search Objective Should Not Be Fooled by Geometry

The miner may vary morphology and source placement, but it must prevent trivial cheating.

Reject configurations that obtain low energy by:

```text
INTERSECTING PAYLOAD

PLACING SOURCE INSIDE PAYLOAD

USING UNPHYSICAL ZERO DISTANCE

USING A POINTLIKE SINGULAR LIMIT

USING A DOMAIN CUT THAT HIDES ENERGY

DROPPING FAR TAIL ENERGY

OMITTING SUPPORT

OMITTING ACTIVATION

OMITTING CONTROL

PRESCRIBING LOCAL COUPLING BY HAND
```

Geometry is a legitimate optimization variable only inside physical constraints.

---

# 53. Useful Introspective Quantities

AGMINER should use mechanism knowledge from Introspective as search features.

Promising candidates tend to seek:

```text
HIGH KERNEL LEVERAGE

PAYLOAD-ADJACENT PRODUCTIVE STRUCTURE

HIGH USEFUL RESPONSE PER JOULE

LOW CANCELLATION

HIGH PRODUCTIVE PARTICIPATION

LOW SCAFFOLDING FRACTION
```

These are ranking features.

They are not substitutes for full field realization.

---

# 54. Surrogate Models

After enough data exists, AGMINER may train lightweight surrogate regressors for:

```text
ENERGY

FAILURE PROBABILITY

PAYLOAD RESPONSE

NATURALNESS MARGIN

STABILITY PROXY
```

Initial implementation should use simple models only.

Possible later choices:

```text
RANDOM FOREST

GRADIENT BOOSTING

GAUSSIAN PROCESS FOR SMALL DATA
```

But surrogate predictions may only:

```text
PRIORITIZE
DEPRIORITIZE
SUGGEST
```

They must not establish scientific PASS.

Hard rejection by surrogate alone is prohibited unless supported by an analytical bound.

---

# 55. Avoid Optimizer Pathology

AGMINER must avoid spending the entire run on a constraint boundary.

Use:

```text
MINIMUM LEAK MARGIN

MINIMUM BACKREACTION MARGIN

MINIMUM NATURALNESS MARGIN

MINIMUM STABILITY MARGIN
```

for the robust-ranking view.

Keep a separate:

```text
ABSOLUTE_LOWEST_ENERGY_VIEW
```

so edge candidates are not hidden.

This reproduces the useful distinction between the historical ~96-GJ edge point and the more conservative ~121-GJ interior point.

---

# 56. Search Diversity

Maintain separate top candidates by family and basin.

Do not let 100 nearly identical candidates occupy all shortlist slots.

Suggested clustering:

```text
NORMALIZED PARAMETER DISTANCE
```

Only retain a limited number from each small neighborhood.

This increases the chance that later certification tests genuinely different solutions.

---

# 57. Robustness Micro-Test

Before Tier-2 promotion, perturb each candidate slightly.

Example:

```text
±0.5%
±1%
```

for a selected subset of sensitive parameters.

If the candidate only works at one numerically razor-thin point, record:

```text
LOW_ROBUSTNESS
```

and deprioritize it.

Do not necessarily reject unless the variation reveals physical invalidity.

---

# 58. Automatic Failure Statistics

AGMINER should report why the search is failing.

Example:

```text
TOTAL TESTED = 100000

68.2% ANALYTIC ENERGY >10GJ

14.7% NATURALNESS

7.8% NO FIELD SOLUTION

4.1% PAYLOAD SIGN

2.2% ENERGY AFTER SOLVE

1.6% LEAKAGE

0.8% STABILITY

0.4% BACKREACTION

0.2% SURVIVE
```

This becomes scientific information.

It tells us which physical gate dominates each family.

---

# 59. Automatic Family Stop Rule

A family should not run forever.

Possible stop conditions:

```text
NO SUB-10-GJ CANDIDATES AFTER BROAD COVERAGE

ANALYTIC LOWER BOUND >10 GJ OVER ENTIRE REGION

NATURALNESS FAILS ENTIRE FAMILY

NO FIELD SOLUTIONS

ALL SUB-10-GJ SOLUTIONS FAIL PAYLOAD SIGN

ALL PROMISING SOLUTIONS ARE UNSTABLE

NO IMPROVEMENT AFTER N ADAPTIVE ROUNDS
```

Then classify the family:

```text
AGMINER_FAMILY_DEMOTED
```

and move compute elsewhere.

---

# 60. Campaign Stop Conditions

A mining campaign ends when any of the following occurs:

```text
USER STOPS RUN

TIME BUDGET REACHED

DISK BUDGET REACHED

CANDIDATE BUDGET REACHED

NO IMPROVEMENT WINDOW REACHED

FAMILY EXHAUSTION RULE REACHED
```

The database must remain valid after interruption.

---

# 61. Crash Recovery

Every candidate evaluation should be transaction-safe.

On restart:

```text
READ DATABASE

FIND RUNNING MODELS

MARK ABANDONED RUNNING MODELS AS INTERRUPTED

RESUME SAMPLER INDEX

REBUILD PARETO FRONTIER

CONTINUE
```

Do not restart the search from zero.

---

# 62. Configuration

Suggested config file:

```text
config/agminer_032a.json
```

Fields:

```text
energy_limit_j

payload_mass_kg

payload_radius_m

target_surface_accel

target_cm_accel

families

parameter_bounds

sampler_seed

worker_count

tier0_budget

tier1_budget

tier2_budget

timeouts

disk_budget_mb

checkpoint_limit

logging_limit_mb

naturalness_threshold

leak_limit

backreaction_limit

robustness_settings
```

The run must copy the effective config hash into the database.

---

# 63. Recommended Source Tree

```text
src/antigravity_research/agminer/
    __init__.py
    config.py
    candidate.py
    fingerprint.py
    storage.py
    failure_codes.py
    gates.py
    energy.py
    payload.py
    naturalness.py
    pareto.py
    sampler.py
    scheduler.py
    reporting.py
    checkpoint.py

    families/
        __init__.py
        base.py
        family_031_control.py
        family_032_protected.py

simulations/
    032a_agminer_validation.py
    032b_agminer_campaign.py

tests/agminer/
    ...
```

Keep theory equations in the family modules.

Keep generic mining infrastructure independent.

---

# 64. Command-Line Interface

Eventually:

```text
python -m antigravity_research.agminer run

python -m antigravity_research.agminer status

python -m antigravity_research.agminer top

python -m antigravity_research.agminer failures

python -m antigravity_research.agminer export

python -m antigravity_research.agminer resume
```

Useful optional filters:

```text
--family

--max-energy-gj

--top

--min-naturalness-margin

--state

--run-id
```

---

# 65. `status` Output

Keep it compact.

Example:

```text
AGMINER STATUS

run_id=032A_0004
elapsed=05:17:33
tested=84291
known_skips=12033

rejected_energy=49102
rejected_naturalness=8120
rejected_field=4031
rejected_payload=920
rejected_stability=72

tier1_survivors=33
tier2_survivors=5

best_energy_gj=2.814
pareto_count=9

database_mb=27.6
checkpoints_mb=61.4
logs_mb=2.1
```

---

# 66. `top` Output

Example:

```text
RANK MODEL       ENERGY  SURFACE  NAT_MARGIN  STAB_MARGIN  LEAK
1    032A-91FE    2.814   10.17g   83.1x       6.2x         0.11x_limit
2    032A-32B1    3.029   11.42g   240x        3.8x         0.05x_limit
3    032A-14C8    3.287   10.02g   900x        18x          0.22x_limit
```

Then we decide which models deserve certification.

---

# 67. Failure Lookup

The user should be able to ask:

```text
Have we already tested this model?
```

AGMINER can query by:

```text
candidate_id
```

or canonical parameter vector.

Return:

```text
TESTED
REJECTED
FAIL_CODE
ENERGY
DATE/RUN
```

This directly satisfies the requirement not to keep going over failed models.

---

# 68. Near-Miss Reporting

Keep compact statistics for useful failures.

Examples:

```text
LOWEST ENERGY NATURALNESS FAILURE

LOWEST ENERGY STABILITY FAILURE

LOWEST ENERGY PAYLOAD FAILURE

CLOSEST >10-GJ FAILURE

BEST ENERGY MARGIN BUT LOW STABILITY
```

These help guide theory changes without keeping huge data files.

---

# 69. Failure Retention Policy

All exact failures remain in the SQLite database.

But only a compact record.

For routine failures:

```text
NO PROFILE

NO NPZ

NO FULL JSON

NO INDIVIDUAL LOG
```

For scientifically interesting failures:

```text
OPTIONALLY MARK preserve_detail=1
```

Examples:

```text
NEW NO-GO

UNEXPECTED SIGN REVERSAL

NEW INSTABILITY CLASS

NEW NATURALNESS BOUND

NEAR-RECORD ENERGY
```

Only these receive richer artifacts.

---

# 70. Candidate Retention Policy

Keep detailed artifacts only for:

```text
CURRENT GLOBAL TOP 10

CURRENT PARETO FRONTIER

TIER2 SURVIVORS

MANUALLY PINNED MODELS
```

Everything else is database metadata.

---

# 71. Historical Import

Implement a one-time importer for known project results.

Purpose:

```text
SEED FAILURE MEMORY

VALIDATE AGMINER

CREATE HISTORICAL CONTROL SET
```

Examples:

```text
006D

B7

031 prescribed 82.75

031 273

031 103

031 96

031 121

031 D3B 127.78

031F0 naturalness RED
```

Use explicit labels:

```text
HISTORICAL
```

and:

```text
DO_NOT_TREAT_AS_NEW_DISCOVERY
```

---

# 72. Model Promotion Rules

AGMINER may mark:

```text
CERTIFICATION_READY
```

only when all of these are true:

```text
REFINED E_CONSERVATIVE_COMPLETE <= 10 GJ

FINITE PAYLOAD CM >= 1g

FINITE PAYLOAD SURFACE MIN >= 1g

FIELD EXISTS

POSITIVE HAMILTONIAN

CONSERVATION PASS

REQUIRED ENERGY CONDITIONS PASS

BOUND / LOCALIZED

LEAKAGE PASS

BACKREACTION PASS

NATURALNESS PASS

EFT PASS

CHEAP STABILITY PASS

NO OBVIOUS EMPIRICAL STRUCTURAL CONFLICT

ROBUSTNESS MICRO-SCAN PASS OR ACCEPTABLE
```

Certification readiness is not certification.

---

# 73. Full Certification Is Separate

Once AGMINER produces candidates, create a separate certification queue.

Never run the full certification stack automatically on every miner survivor.

Suggested workflow:

```text
AGMINER FINDS 100,000 MODELS

~100 SURVIVE CHEAPLY

~10 SURVIVE TIER2

3–5 CHOSEN FOR CERTIFICATION

1 OR FEWER MAY SURVIVE EVERYTHING
```

This is precisely the computational separation we want.

---

# 74. 10 GJ Certification Rule

The 10 GJ ceiling remains active during certification.

If a candidate initially estimated at:

```text
6.2 GJ
```

later reconstructs as:

```text
10.4 GJ
```

then stop certification immediately.

Record:

```text
REJECTED_ENERGY_GT_10GJ_AT_CERTIFICATION
```

Do not continue because time has already been invested.

Sunk compute is irrelevant.

---

# 75. No Target Forcing

Do not tune numerical definitions merely to make a model sub-10-GJ.

No:

```text
CHANGING PAYLOAD AFTER FAILURE

OMITTING TAIL ENERGY

CHANGING ENERGY LEDGER

OMITTING ACTIVATION

DROPPING SUPPORT

USING EXACT NEGATIVE BINDING INSTEAD OF CONSERVATIVE INVENTORY

WEAKENING LEAK LIMIT AFTER FAILURE

WEAKENING NATURALNESS AFTER FAILURE
```

If a candidate fails:

```text
RECORD IT
MOVE ON
```

---

# 76. First Implementation Milestone — AGMINER Core

Success criteria:

```text
SQLITE DATABASE WORKS

DETERMINISTIC MODEL IDS

10-GJ GATE WORKS

DUPLICATES SKIP

REJECTIONS PERSIST RESTART

PARETO FRONTIER WORKS

ROTATING LOGS WORK

CRASH RESUME WORKS

HISTORICAL IMPORT WORKS
```

No new physics search yet.

---

# 77. Second Milestone — 031 Control Family

Implement enough 031 to verify:

```text
KNOWN 031 CANDIDATES ARE FOUND

KNOWN ENERGIES RECONSTRUCT REASONABLY

ALL >10-GJ POINTS ARE REJECTED EARLY

031 NATURALNESS FAILS EARLY

NO 031 POINT ENTERS CERTIFICATION SHORTLIST
```

This is an AGMINER validation test, not reopening 031.

---

# 78. Third Milestone — First Protected 032 Family

Only after AGMINER infrastructure passes.

Implement one explicitly radiatively protected candidate family.

Before searching it, derive:

```text
ACTION

SYMMETRIES

ENERGY

CHARGES

PHYSICAL METRIC

PROTECTION MECHANISM

LOOP ESTIMATE

PARAMETER DOMAIN
```

Then expose it through the common family API.

---

# 79. Fourth Milestone — Long Mining Campaign

Run unattended for hours.

Desired behavior:

```text
MINIMAL TERMINAL OUTPUT

SMALL ROTATING LOG

CONTINUOUS SQLITE CHECKPOINTING

NO PER-MODEL FILES

AUTOMATIC FAILURE MEMORY

AUTOMATIC PARETO UPDATE

AUTOMATIC TOP-CANDIDATE CHECKPOINT RETENTION
```

At the end:

```text
python -m antigravity_research.agminer top
```

should tell us immediately which models deserve attention.

---

# 80. Fifth Milestone — Tier-2 Screener

Build a second process that consumes:

```text
CERTIFICATION_CANDIDATE
```

records.

It performs:

```text
REFINED BVP

GRID CHECK

DOMAIN CHECK

BETTER FORCE RECONSTRUCTION

SELECTED ANGULAR STABILITY

NATURALNESS RECHECK

ENERGY RECONSTRUCTION

PARAMETER ROBUSTNESS
```

Output:

```text
CERTIFICATION_READY
```

or an explicit rejection.

---

# 81. Sixth Milestone — Certification Export

For each certification-ready candidate generate one compact packet:

```text
candidate_<id>_certification.json

candidate_<id>_checkpoint.npz
```

The JSON contains:

```text
THEORY

PARAMETERS

ENERGY LEDGER

PAYLOAD OBSERVABLES

GATE RESULTS

MARGINS

PROVENANCE

KNOWN LIMITATIONS

NEXT CERTIFICATION TEST
```

Only a few such packets should ever exist.

---

# 82. Scientific Claim Discipline

AGMINER output classifications:

```text
GENERATED

SCREENED

CHEAP_SURVIVOR

TIER2_SURVIVOR

CERTIFICATION_READY
```

Never:

```text
PROVEN

VALIDATED THEORY

ANTIGRAVITY DEVICE

DISCOVERY
```

without the later certification program.

---

# 83. Key Scientific Lessons Built Into AGMINER

Permanent lessons:

```text
LOCAL REPULSION != TRUE FINITE-PAYLOAD STANDOFF

FIELD EXISTENCE != STABILITY

STABILITY != NONLINEAR STABILITY

LOW SOURCE ENERGY != LOW COMPLETE ENERGY

LOW EXACT HAMILTONIAN != LOW CONSERVATIVE INVENTORY

ACTIVATION ENERGY CANNOT BE OMITTED

SUPPORT CANNOT BE OMITTED

RADIATIVE NATURALNESS MUST BE EARLY

ONE GRID DOES NOT ESTABLISH MAGNITUDE

BOUNDARY OPTIMA ARE HIGH RISK

PAYLOAD KERNEL MATTERS

PRODUCTIVE PARTICIPATION MATTERS

CANCELLATION MATTERS

SCAFFOLDING TAX MATTERS
```

---

# 84. AGMINER Success Definition

AGMINER itself succeeds if it can:

```text
SEARCH THOUSANDS OF MODELS

WITHOUT LARGE DISK GROWTH

WITHOUT REPEATING EXACT FAILURES

WITH RESUMABLE STATE

WITH EARLY PHYSICS FALSIFICATION

WITH HARD >10-GJ REJECTION

WITH NATURALNESS BEFORE EXPENSIVE CERTIFICATION

AND

RETURN A SMALL LOW-ENERGY SHORTLIST
```

It does not need to find a viable antigravity model to be scientifically successful.

A result such as:

```text
NO SEARCHED MODEL IN FAMILY 032A
ACHIEVES <=10 GJ
WHILE PASSING NATURALNESS,
FINITE-PAYLOAD,
CONSERVATION,
AND CHEAP STABILITY
```

would be a valuable negative result.

---

# 85. Hard Stop Rules

Permanent AGMINER stop rules:

```text
IF E_CONSERVATIVE_COMPLETE > 10 GJ:
    REJECT
    RECORD
    NEVER CERTIFY

IF ANALYTIC ENERGY LOWER BOUND > 10 GJ:
    REJECT BEFORE FIELD SOLVE

IF NATURALNESS FAILS:
    REJECT BEFORE EXPENSIVE STABILITY

IF HAMILTONIAN UNBOUNDED:
    REJECT

IF GHOST:
    REJECT

IF UNIVERSAL PHYSICAL METRIC FAILS:
    REJECT

IF FINITE PAYLOAD SURFACE < 1g:
    REJECT

IF SOURCE INTERSECTS PAYLOAD:
    REJECT

IF CONSERVATION FAILS:
    REJECT

IF POSITIVE ENERGY REQUIREMENT FAILS:
    REJECT

IF CHEAP TRUE INSTABILITY IS ESTABLISHED:
    REJECT

IF LEAKAGE LIMIT FAILS:
    REJECT

IF BACKREACTION LIMIT FAILS:
    REJECT

IF EXACT CANDIDATE ALREADY FAILED:
    SKIP

IF NUMERICAL SOLVER FAILS TWICE:
    MARK NUMERICALLY_UNRESOLVED
    DO NOT SPIN FOREVER

IF FAMILY IS ANALYTICALLY EXCLUDED:
    STOP FAMILY

IF DISK BUDGET EXCEEDED:
    STOP SAFELY

IF DATABASE IS DAMAGED:
    STOP
    DO NOT CONTINUE BLIND
```

---

# 86. Recommended Next-Session Execution Order

Begin the next session in this exact order.

```text
1.
RECONSTRUCT CURRENT PROJECT STATE

2.
PRESERVE 031F0 RED NATURALNESS CLOSEOUT

3.
READ FORMATTING_AND_CODE_STANDARDS

4.
VERIFY 94-TEST BASELINE

5.
CREATE AGMINER_BUILDPLAN.md

6.
CREATE src/antigravity_research/agminer/

7.
IMPLEMENT CONFIG

8.
IMPLEMENT FAILURE CODES

9.
IMPLEMENT CANDIDATE CANONICALIZATION

10.
IMPLEMENT DETERMINISTIC FINGERPRINTING

11.
IMPLEMENT SQLITE STORAGE

12.
IMPLEMENT REJECTION MEMORY

13.
IMPLEMENT HARD 10-GJ GATE

14.
IMPLEMENT PARETO FRONTIER

15.
IMPLEMENT ROTATING LIGHTWEIGHT LOGGING

16.
IMPLEMENT CRASH RESUME

17.
IMPLEMENT SOBOL SAMPLER

18.
IMPLEMENT GENERIC FAMILY INTERFACE

19.
IMPLEMENT HISTORICAL 031 CONTROL FAMILY

20.
IMPORT KNOWN HISTORICAL FAILURES

21.
ADD AGMINER UNIT TESTS

22.
RUN 94 BASELINE

23.
RUN AGMINER VALIDATION CAMPAIGN

24.
VERIFY KNOWN >10-GJ MODELS ARE REJECTED

25.
VERIFY 031 NATURALNESS IS REJECTED EARLY

26.
VERIFY DUPLICATES SKIP AFTER RESTART

27.
VERIFY DISK USAGE REMAINS SMALL

28.
ONLY THEN DEFINE FIRST NEW 032 PROTECTED FAMILY

29.
RUN SMALL 032 SMOKE SEARCH

30.
IF CLEAN:
    START LONG UNATTENDED MINING CAMPAIGN
```

---

# 87. Initial Files Expected After Build

Keep the repository clean.

Expected persistent files:

```text
AGMINER_BUILDPLAN.md

src/antigravity_research/agminer/...

tests/agminer/...

config/agminer_032a.json

results/agminer/agminer.sqlite3

results/agminer/agminer_current.log

results/agminer/top_candidates.csv

results/agminer/pareto_frontier.csv

results/agminer/failure_counts.csv

results/agminer/run_summary.json
```

Do not generate thousands of candidate-specific files.

---

# 88. Major Architecture Principle

The central design rule is:

> **Store knowledge, not simulation clutter.**

A failed candidate should normally cost only one small database row.

A successful coarse candidate should cost only a small database row.

Only a tiny number of finalists deserve field checkpoints.

---

# 89. New Research Philosophy

The old workflow was approximately:

```text
FIND A PROMISING MODEL
        ↓
SPEND MANY RUNS CERTIFYING IT
        ↓
DISCOVER A LATE FAILURE
```

AGMINER changes this to:

```text
SEARCH MANY CHEAPLY
        ↓
FALSIFY EARLY
        ↓
REMEMBER EVERY FAILURE
        ↓
KEEP ONLY <=10-GJ SURVIVORS
        ↓
RANK BY ENERGY + PHYSICAL MARGINS
        ↓
CERTIFY ONLY THE VERY BEST
```

This should become the default ANTIGRAVITY_RESEARCH workflow for future candidate families.

---

# 90. Primary AGMINER Claim

The goal of 032A is not:

```text
FIND ANTIGRAVITY
```

The goal is:

> **Build a reproducible, disk-efficient, failure-aware, multi-fidelity antigravity candidate miner that can search parameterized microscopic theories for complete finite-payload operating configurations at or below 10 GJ, reject known and newly discovered failures cheaply, and return only the strongest candidates for expensive certification.**

---

# 91. Hard 10 GJ Project Statement

Carry this into every AGMINER session:

```text
AGMINER_ENERGY_LIMIT =
10.0 GJ

ENERGY_LEDGER =
CONSERVATIVE_COMPLETE_OPERATING_INVENTORY

IF ENERGY > 10 GJ =
FAIL

FAILURE CODE =
REJECTED_ENERGY_GT_10GJ

FAILED EXACT MODEL =
PERSISTENTLY REMEMBERED

FAILED EXACT MODEL =
NOT AUTOMATICALLY RETESTED

MODEL <= 10 GJ =
ONLY ELIGIBLE FOR FURTHER SCREENING

MODEL <= 10 GJ =
NOT AUTOMATICALLY VALID

FULL CERTIFICATION =
SEPARATE LATER PROCESS
```

---

# 92. Final Next State

```text
CURRENT 031 EFT =
CLOSED RED ON RADIATIVE NATURALNESS

031 CLASSICAL RESULTS =
PRESERVED

031D =
DRIVEN ADIABATIC SWITCHING GREEN

031E =
WEAK-CURVATURE EINSTEIN/JORDAN GREEN

031F0 =
RADIATIVE NATURALNESS RED

CURRENT PRACTICAL DEVICE =
NO

NEW ACTIVE DEVELOPMENT =
AGMINER

AGMINER HARD ENERGY CEILING =
10 GJ

AGMINER FIRST TASK =
BUILD INFRASTRUCTURE BEFORE NEW HEAVY PHYSICS

NEXT =
032A_AGMINER_CORE_VALIDATION_AND_PROTECTED_MODEL_MINING
```
# 93. Manual Stop, Safe Shutdown, and Anytime Results Access

AGMINER must be designed so the user can **stop a mining campaign whenever desired without losing completed work or corrupting the database**.

Manual interruption is a normal operating condition, not an error.

Required behavior:

```text
USER REQUESTS STOP
        ↓
STOP ISSUING NEW CANDIDATES
        ↓
ALLOW CURRENT SHORT WORK UNITS TO FINISH OR CANCEL SAFELY
        ↓
WRITE PENDING RESULTS TO SQLITE
        ↓
CHECKPOINT SAMPLER / RUN STATE
        ↓
REBUILD CURRENT PARETO FRONTIER
        ↓
UPDATE TOP-CANDIDATE AND FAILURE SUMMARIES
        ↓
CHECKPOINT / TRUNCATE SQLITE WAL
        ↓
EXIT CLEANLY
```

AGMINER must handle at minimum:

```text
CTRL+C
SIGTERM
BUILT-IN STOP COMMAND
```

A first interrupt should request a **graceful stop**.

If practical, a second interrupt may force termination while preserving all database transactions already committed.

The miner must never require the user to wait for the entire planned campaign to finish before seeing results.

---

## Results Must Be Viewable at Any Time

The user must be able to inspect current results while AGMINER is:

```text
RUNNING
STOPPED
INTERRUPTED
COMPLETED
```

without modifying or invalidating the active campaign.

Provide commands equivalent to:

```text
python -m antigravity_research.agminer status

python -m antigravity_research.agminer top

python -m antigravity_research.agminer pareto

python -m antigravity_research.agminer failures
```

These should read the SQLite database in a safe read-only manner.

`status` should show compact campaign state:

```text
TOTAL CANDIDATES TESTED
KNOWN CANDIDATES SKIPPED
TOTAL REJECTIONS
>10-GJ REJECTIONS
NATURALNESS REJECTIONS
FIELD-SOLVE FAILURES
PAYLOAD FAILURES
STABILITY FAILURES
TIER-1 SURVIVORS
TIER-2 SURVIVORS
CURRENT BEST ENERGY
PARETO COUNT
ELAPSED TIME
DATABASE SIZE
CHECKPOINT SIZE
CURRENT RUN STATE
```

`top` should display the best surviving models, ordered primarily by conservative complete energy.

`pareto` should show the current Pareto frontier.

`failures` should summarize rejection counts and allow lookup of previously tested candidates.

---

## Explicit Stop Command

Implement a convenient controlled shutdown command such as:

```text
python -m antigravity_research.agminer stop
```

The active miner should periodically check for the stop request and shut down gracefully.

A simple implementation may use a small control file or database flag such as:

```text
STOP_REQUESTED = TRUE
```

The stop mechanism must not require network services or additional infrastructure.

---

## Resume After Stop

A safely stopped campaign must later support:

```text
python -m antigravity_research.agminer resume
```

Resume must:

```text
LOAD EXISTING DATABASE

RESTORE RUN CONFIGURATION

RESTORE SAMPLER POSITION

REBUILD REJECTION MEMORY

REBUILD PARETO FRONTIER

RESTORE SURVIVOR QUEUES

SKIP ALL COMPLETED / TERMINALLY REJECTED MODELS

CONTINUE FROM THE NEXT UNEVALUATED CANDIDATE
```

Stopping and resuming must **not cause already rejected models to be tested again**.

---

## Periodic Live Summaries

While mining, AGMINER should periodically overwrite lightweight live-result files:

```text
results/agminer/top_candidates.csv

results/agminer/pareto_frontier.csv

results/agminer/failure_counts.csv

results/agminer/run_summary.json
```

These files are convenience views only.

The SQLite database remains authoritative.

Because the summaries are overwritten rather than continually timestamped, they should add negligible disk usage.

---

## Manual Candidate Pinning

While reviewing results, the user should be able to mark a promising model:

```text
PINNED = TRUE
```

A pinned candidate must not have its checkpoint automatically deleted even if it later falls outside the automatic top-candidate retention set.

This permits the user to stop a long campaign, inspect interesting models, preserve selected candidates, and resume searching later.

---

## Manual Stop Principle

Permanent AGMINER rule:

> **The miner works for the user; the user never works for the miner.**

At any point the user must be able to stop the search, inspect everything learned so far, preserve promising candidates, and later resume without losing completed work or repeating known failures.
