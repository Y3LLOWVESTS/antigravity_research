# AGMINER BUILD PLAN

## Physics-Aware Antigravity Model Discovery, Mechanism Learning, Falsification, Rejection Memory, and Certification Control

**Project:** `ANTIGRAVITY_RESEARCH`

**Subsystem:** `AGMINER`

**Date:** 2026-09-06

**Initial development branch:** `032A`

**Current active research program:** `032 — AGMINER-GUIDED KINETIC-CONFORMAL ANTIGRAVITY`

**Current completed phase:** `032V18`

**Immediate next phase:** `032V19_SPHERICAL_BAG_SUPPORT_UV_MATCHING_AND_EMPIRICAL_GATE`

**Current AGMINER mode:** `CANDIDATE_SPECIFIC_FALSIFICATION`

**Current energy leader:** `032V17 OBLATE — ~59.419738 kJ PARTIAL ORACLE`

**Current support-realization leader:** `032V18 SPHERE — ~3.419157493 MJ PARTIAL ORACLE`

**Current hard energy policy:** `E_CONSERVATIVE_COMPLETE_OPERATING < 10 MJ`

**Exactly 10 MJ:** `REJECT`

**Energy policy ID:** `ENERGY_ab8c16e45c837ffc`

**Historical protected regression baseline:** `94 passed`

**Current full regression suite:** `238 passed`

**Current approximate database state:**

```text
MODEL_COUNT               ~101050
REJECTION_COUNT           ~95600
ACTION_ORACLE_COUNT       8
COLLECTIVE_SCALING_COUNT  2
MECHANISM_METRIC_COUNT    0
MECHANISM_PARETO_COUNT    0
CERTIFIED_SURVIVOR_COUNT  0
```

**Physical antigravity model found:** `NO`

**Certified sub-10-MJ model found:** `NO`

**Practical device:** `NO`

**New physics discovery:** `NO`

---

# 0. Purpose

AGMINER is the primary physics-aware model-discovery and falsification engine for `ANTIGRAVITY_RESEARCH`.

It began as a low-compute candidate miner.

It has evolved into a substantially broader scientific system.

Its purpose is now to:

```text
SEARCH
+
CANONICALIZE
+
FALSIFY
+
LEARN MECHANISMS
+
REMEMBER FAILURES
+
IDENTIFY PHYSICAL BOTTLENECKS
+
CONTROL PROMOTION
```

across large antigravity theory spaces.

AGMINER is not merely:

```text
A PARAMETER SCANNER
```

and it is not:

```text
A BLACK-BOX OPTIMIZER.
```

Its central philosophy is:

> **Use physical understanding to eliminate impossible mechanisms before spending computation on them, preserve every durable falsification, and promote only candidates whose apparent efficiency survives progressively more complete physics.**

---

# 1. Current role of AGMINER

The original AGMINER workflow was approximately:

```text
GENERATE MANY PARAMETER POINTS

        ↓

CHEAP FIELD SOLVE

        ↓

ENERGY GATE

        ↓

PAYLOAD / NATURALNESS / STABILITY FILTERS

        ↓

SHORTLIST

        ↓

CERTIFICATION
```

That remains useful for broad parameter families.

However AGMINER now supports a deeper workflow:

```text
THEORY CLASS

        ↓

LOCAL OPERATOR

        ↓

CANONICAL NORMALIZATION

        ↓

ACTION-SPECIFIC ORACLE

        ↓

SOURCE-EXISTENCE THEOREM

        ↓

SIGN / SIDEDNESS

        ↓

MICROSCOPIC SOURCE

        ↓

FINITE PAYLOAD

        ↓

SOURCE REACTION

        ↓

SUPPORT / CONFINEMENT

        ↓

QUANTUM / RG / UV CONTROL

        ↓

STABILITY

        ↓

EMPIRICAL CLOSURE

        ↓

COMPLETE ENERGY LEDGER

        ↓

CERTIFICATION
```

This theorem/oracle architecture supersedes the idea that every problem should be attacked by a larger parameter scan.

---

# 2. Mission

AGMINER's mission is:

> **Search parameterized microscopic and effective antigravity theories for physically meaningful efficiency mechanisms, eliminate impossible realizations as cheaply as possible, preserve the reasons they fail, and identify the smallest number of candidates that deserve expensive physical certification.**

The operative phrase is:

```text
PHYSICALLY MEANINGFUL EFFICIENCY.
```

An apparent gain is not meaningful until it survives:

```text
CANONICAL NORMALIZATION

SOURCE COST

SUPPORT COST

FINITE PAYLOAD

REACTION

NATURALNESS

EFT CONTROL
```

where applicable.

---

# 3. AGMINER success does not require finding antigravity

AGMINER succeeds scientifically if it can show, for example:

```text
AN ENTIRE THEORY FAMILY FAILS BY A PROVEN ENERGY BOUND

OR

A LARGE APPARENT COUPLING IS A FIELD-REDEFINITION ARTIFACT

OR

A SOURCE CANNOT EXIST UNDER THE DECLARED STATIC ASSUMPTIONS

OR

COLLECTIVE RESPONSE GROWS NO FASTER THAN SCAFFOLD ENERGY

OR

THE LOW-ENERGY SOURCE CANNOT SURVIVE SUPPORT OR RG CONTROL
```

A high-quality negative result is a successful AGMINER result.

---

# 4. Strict energy policy

Current policy:

```text
ENERGY_POLICY_ID =
ENERGY_ab8c16e45c837ffc
```

Pass condition:

```math
E_{\rm conservative,\ complete,\ operating}
<
1.0\times10^7\ {\rm J}
```

Therefore:

```text
E < 10 MJ
    ENERGY POLICY MAY PASS

E = 10 MJ
    REJECT

E > 10 MJ
    REJECT
```

The comparison is strictly:

```text
LT
```

not:

```text
LE.
```

Exactly 10 MJ never passes.

---

# 5. Energy target is configuration, not physics identity

The energy target must remain configurable.

Current source:

```text
config/agminer_032a.json
```

Supported energy units should include:

```text
J
kJ
MJ
GJ
TJ
```

A future change in project practicality target must not require changing theory source code.

Permanent rule:

```text
PHYSICAL_CANDIDATE_ID_DEPENDS_ON_ENERGY_TARGET =
NO
```

The physical candidate represents the theory and physical parameters.

Objective decisions belong to a separate policy layer.

---

# 6. Policy-specific objective memory

A candidate can fail because:

```text
THE PHYSICS IS INVALID
```

or merely because:

```text
IT MISSES THE CURRENT PRACTICALITY OBJECTIVE.
```

These must be distinguished.

Example:

```text
PHYSICS:
candidate energy = 20 MJ
otherwise valid

10-MJ policy:
REJECT

100-MJ policy:
MAY CONTINUE
```

Therefore objective rejection memory is:

```text
POLICY_SPECIFIC.
```

Scientific no-go memory is normally:

```text
POLICY_INDEPENDENT.
```

---

# 7. Scientific object hierarchy

AGMINER must permanently distinguish the following objects.

## 7.1 Candidate

A particular physical parameter point in a declared theory/action.

```text
CANDIDATE
```

does not imply a solved field.

---

## 7.2 Analytical bound

A rigorous or conditional bound such as:

```text
ENERGY LOWER BOUND

SOURCE-EXISTENCE NO-GO

SIGN THEOREM

COLLECTIVE SCALING BOUND
```

---

## 7.3 Action oracle

An action-specific result that describes what the underlying action can achieve under a declared relaxation.

Examples:

```text
PROVEN ACTION LOWER BOUND

RELAXED ACTION-SPECIFIC OPTIMUM

PARTIAL FINITE-PAYLOAD ORACLE

SOURCE-SIDE SCALING ORACLE
```

An action oracle is not automatically a realized field.

---

## 7.4 Microscopic realization

A field/source solution of the declared microscopic action.

This still does not imply:

```text
STABILITY

SUPPORT

COMPLETE ENERGY

EMPIRICAL VIABILITY.
```

---

## 7.5 Mechanism metric

A physically meaningful set of efficiency diagnostics measured in a sufficiently complete candidate.

This is more demanding than an action oracle.

---

## 7.6 Survivor

A candidate that has passed the declared AGMINER screening gates.

---

## 7.7 Certified survivor

A candidate that has passed the project's declared physical certification stack.

Current count:

```text
0.
```

---

# 8. No oracle-to-model shortcut

Permanent rule:

> **A low action-oracle energy is evidence about the possible efficiency of an action or relaxation, not evidence that the complete microscopic source has that energy.**

For example:

```text
V17 OBLATE:
~59.42 kJ

V18 SPHERE:
~3.419 MJ
```

are partial action oracles.

They are not:

```text
59-kJ ANTIGRAVITY DEVICE

3.4-MJ ANTIGRAVITY DEVICE.
```

---

# 9. Action-oracle contract

Every action oracle should record, where applicable:

```text
CANONICAL_INVARIANT_ID

THEORY_FAMILY

ACTION_VERSION

ORACLE_TYPE

PROOF_REFERENCE

PROVEN_LOWER_BOUND_J

RELAXED_COMPLETE_ENERGY_J

REALIZED_MICROSCOPIC_ENERGY_J

LEDGER_SCOPE

NORMALIZATION_INVARIANT

NATURALNESS_SCREENED

UNIVERSAL_METRIC_SCREENED

FINITE_PAYLOAD_SCREENED

SUPPORT_INCLUDED

BACKREACTION_INCLUDED

STABILITY_INCLUDED

EMPIRICAL_SCREENED

TRUSTED_FOR_REACHABILITY
```

---

# 10. Ledger classes

Every energy result must carry an explicit ledger class.

Recommended standard classes:

```text
FIELD_ONLY

SOURCE_ONLY

SOURCE_PLUS_FIELD

PARTIAL_OPTIMISTIC

PARTIAL_CONSERVATIVE_FLOOR

MICROSCOPIC_PARTIAL

COMPLETE_STATIC

COMPLETE_OPERATING
```

Current V17/V18 status:

```text
PARTIAL_OPTIMISTIC
or
PARTIAL_CONSERVATIVE_FLOOR

depending on the reported component
```

but never:

```text
COMPLETE_OPERATING.
```

---

# 11. Realization gap

AGMINER must track:

```math
R_{\rm realization}
=
\frac{
E_{\rm realized}
}{
E_{\rm action\ oracle}
}
```

This separates two different scientific problems.

Example A:

```text
ACTION ORACLE = 2 MJ
REALIZED SOURCE = 200 MJ

R_realization = 100
```

Interpretation:

```text
UNDERLYING ACTION MAY BE EFFICIENT

REALIZATION / SCAFFOLDING IS BAD.
```

Example B:

```text
ACTION ORACLE = 150 MJ
REALIZED SOURCE = 200 MJ

R_realization ~ 1.33
```

Interpretation:

```text
REALIZATION IS ALREADY NEAR ACTION LIMIT

UNDERLYING PHYSICS MUST CHANGE.
```

This distinction is permanent.

---

# 12. Introspective factorization

The completed Introspective program established that useful response should not be collapsed into one opaque coupling.

AGMINER should conceptually factor useful response per complete joule as:

```math
\frac{
A_{\rm useful}
}{
E_{\rm complete}
}
\sim
q_{\rm prod}
K_{\rm eff}
\frac{
f_{\rm prod}
}{
C_{\rm cancel}
}
```

where:

```text
q_prod
=
productive response or charge per productive joule

K_eff
=
finite-payload kernel leverage

f_prod
=
productive participation

C_cancel
=
destructive cancellation factor
```

Scaffolding should be tracked independently.

This is a guiding decomposition, not a universal exact equation.

---

# 13. Introspective search lessons

AGMINER should preferentially seek:

```text
HIGH INTRINSIC CHARGE / RESPONSE PER JOULE

HIGH PRODUCTIVE PARTICIPATION

HIGH PAYLOAD KERNEL LEVERAGE

LOW CANCELLATION

COMPACT PAYLOAD-ADJACENT PRODUCTIVE STRUCTURE

LOW SCAFFOLDING FRACTION

SHARED SCAFFOLDING

PHYSICAL SOURCE-METRIC COLOCATION
```

Historical Introspective findings include:

```text
~19.7% TEACHER ENERGY
produced
~92.2% GROSS OUTWARD INFLUENCE
```

and:

```text
B7 NEGATIVE-ACTIVE PARTICIPATION
~5.15%

RELAXED TEACHER
~50%

PARTICIPATION GAP
~9.7X.
```

These are mechanism priors.

They are not multiplicative free gains.

---

# 14. Never multiply historical gains blindly

Forbidden reasoning:

```text
INTROSPECTIVE KERNEL GAIN
×
B7 MORPHOLOGY GAIN
×
NEW COUPLING GAIN
×
COLLECTIVE GAIN
=
DEVICE GAIN
```

unless all factors have been measured in the **same self-consistent physical candidate**.

Cross-model factor multiplication is not a scientific energy prediction.

---

# 15. Canonical normalization is a Tier-0 gate

V3–V5 demonstrated that apparently large leverage can disappear under field normalization.

Permanent rule:

> **A raw coupling is not an efficiency lever until canonical normalization proves that the gain is a physical invariant.**

Before promotion, ask whether the apparent lever can be removed by:

```text
FIELD RESCALING

WAVEFUNCTION NORMALIZATION

PARAMETER RENAMING

CUTOFF REDEFINITION

CHANGE OF FIELD COORDINATE
```

If yes:

```text
NO PHYSICAL GAIN.
```

---

# 16. Canonical invariant fingerprint

Every new family should expose:

```python
canonical_invariants(params, config)
```

and preferably:

```python
canonical_invariant_id(params, config)
```

The invariant identity should encode the physically meaningful combinations after canonical normalization.

This is separate from the ordinary candidate fingerprint.

---

# 17. Current canonical invariant lesson

For the active V18 kinetic-conformal source:

```math
\mathcal L
=
-\frac{Z}{2}
(\partial\phi)^2
+
C_1
(\partial\phi)^2
O_{\rm matter}
+
\frac1f
\partial_\mu\phi
J^\mu_5
```

under:

```math
\phi_c
=
\sqrt Z\,\phi,
```

one has:

```math
C_{1,c}
=
\frac{C_1}{Z}
```

and:

```math
f_c
=
f\sqrt Z.
```

Therefore:

```math
C_{1,c}f_c^2
=
C_1f^2.
```

Permanent AGMINER rule:

```text
DELTA_Z
IS NOT
AN AUTOMATIC ENERGY MULTIPLIER.
```

The problem is RG/UV matching of physical invariants.

---

# 18. Collective-scaling gate

For a collective parameter `N`, define:

```math
r
=
\frac{
d\ln A_{\rm useful}
}{
d\ln N
}
```

and:

```math
s
=
\frac{
d\ln E_{\rm complete}
}{
d\ln N
}.
```

Promotion requires:

```math
r>s.
```

If:

```text
r = s
```

there is no asymptotic efficiency improvement.

If:

```text
r < s
```

the architecture becomes less efficient.

This is a mandatory screen for:

```text
MULTIFIELD

MULTIFLAVOR

TOPOLOGICAL CHARGE

COLLECTIVE SOURCE

ARRAY

COHERENT ENSEMBLE
```

proposals.

---

# 19. Collective scaling does not prove a portal

V7 and V8 demonstrated source-side shared-scaffold improvements.

Those results were scientifically useful.

They did **not** prove that the corresponding charge was metric-active.

Therefore every collective-scaling record must distinguish:

```text
SOURCE SCALING =
ESTABLISHED / CONDITIONAL

PORTAL =
ESTABLISHED / NOT ESTABLISHED

FINITE PAYLOAD =
ESTABLISHED / NOT ESTABLISHED.
```

---

# 20. Current AGMINER scientific pipeline

The default physical pipeline is now:

```text
0. PROVENANCE

1. CANONICALIZATION

2. THEORY HEALTH

3. OPERATOR SIGN

4. UNIVERSAL METRIC

5. SOURCE-EXISTENCE THEOREM

6. RANGE / SIDEDNESS

7. ACTION ORACLE

8. COLLECTIVE SCALING

9. NATURALNESS / EFT

10. MICROSCOPIC SOURCE

11. FINITE PAYLOAD

12. SOURCE REACTION

13. COMPLETE SOURCE ENERGY

14. SUPPORT / CONFINEMENT

15. STABILITY

16. RG / UV MATCHING

17. RENORMALIZED VACUUM

18. EMPIRICAL CLOSURE

19. ACTIVATION / OFF STATE

20. NONLINEAR METRIC BACKREACTION

21. COMPLETE OPERATING LEDGER

22. CERTIFICATION
```

Not every theory requires every step in exactly this order.

The governing rule is:

```text
CHEAPEST DECISIVE PHYSICS FIRST.
```

---

# 21. Search mode A — broad discovery

Use broad discovery when:

```text
NO THEORY CLASS HAS CLEAR PRIORITY

OR

THE CURRENT CLASS HAS BEEN CLOSED

OR

A NEW PHYSICS FAMILY HAS BEEN DEFINED
```

Possible tools:

```text
SOBOL

LATIN HYPERCUBE

LOW-DIMENSIONAL RANDOM SEARCH

ANALYTICAL REGION EXCLUSION

SURROGATE PRIORITIZATION
```

Do not use blind rectangular grids unless the parameter space is genuinely small.

---

# 22. Search mode B — mechanism discovery

Use when a theory family is known but the useful efficiency mechanism is unclear.

Focus on:

```text
ACTION ORACLES

CANONICAL INVARIANTS

PRODUCTIVE PARTICIPATION

KERNEL LEVERAGE

COLLECTIVE SCALING

REALIZATION GAP

SCAFFOLDING TAX.
```

This was the role of V6–V10.

---

# 23. Search mode C — operator atlas

Use when source-side mechanisms exist but the physical metric portal is uncertain.

Rank candidate operators by:

```text
LOCALITY

COVARIANCE

STATIC SIGN

UNIVERSALITY

NORMALIZATION INVARIANCE

SOURCE COMPATIBILITY

NATURALNESS

EMPIRICAL PLAUSIBILITY

FINITE-PAYLOAD ACCESS.
```

This was the role of V12.

---

# 24. Search mode D — candidate-specific falsification

Once one architecture clearly dominates structural criteria, stop broad mining.

Attack that candidate sequentially.

Current AGMINER mode:

```text
CANDIDATE_SPECIFIC_FALSIFICATION.
```

Current architecture:

```text
SHIFT-SYMMETRIC
KINETIC-CONFORMAL
UNIVERSAL PHYSICAL METRIC

+

ZERO-NET
HIDDEN-FERMION
AXIAL DERIVATIVE SOURCE.
```

---

# 25. Current best search principle

Prefer an action in which:

```text
1. USEFUL GRAVITATIONAL CHARGE IS LOCAL AND COVARIANT

2. THE PRODUCTIVE DEGREE OF FREEDOM IS ALREADY METRIC-ACTIVE

3. NO SEPARATE EXPENSIVE MEDIATOR MUST BE BOLTED ON

4. THE COUPLING SURVIVES CANONICAL NORMALIZATION

5. A SYMMETRY PROTECTS NECESSARY SMALL / LARGE SCALES

6. PRODUCTIVE PARTICIPATION CAN BE HIGH

7. PRODUCTIVE STRUCTURE CAN SIT NEAR THE PAYLOAD

8. CANCELLATION IS LOW

9. SCAFFOLDING GROWS MORE SLOWLY THAN USEFUL RESPONSE

10. COMPLETE FINITE-PAYLOAD ENERGY CAN PLAUSIBLY ENTER <10 MJ
```

The current kinetic-conformal class was selected because it matched more of these criteria than competing V12 operators.

---

# 26. Standard finite-payload benchmark

Current benchmark:

```text
PAYLOAD_MASS_KG =
1.0

PAYLOAD_RADIUS_M =
0.10

TARGET_ADVERSE_SURFACE_ACCEL_MPS2 =
9.80665
```

The source morphology may vary.

The payload benchmark should not be silently changed to rescue a model.

Primary finite-payload success requires:

```text
PAYLOAD OUTSIDE SOURCE

NO SOURCE-PAYLOAD INTERSECTION

SURFACE MINIMUM >= 9.80665 m/s^2

CENTER-OF-MASS RESPONSE OUTWARD

SOURCE OVERLAP WITH PAYLOAD BELOW DECLARED LIMIT
```

---

# 27. Finite payload beats point response

Do not rank a candidate from:

```text
POINT FORCE

CENTER FORCE

MAXIMUM LOCAL FORCE

SCALAR CHARGE

NEAR-SURFACE FIELD
```

alone.

Track:

```text
PAYLOAD_SURFACE_MIN

PAYLOAD_SURFACE_MAX

SURFACE_NONUNIFORMITY

PAYLOAD_VOLUME_AVERAGE

PAYLOAD_CENTER_RESPONSE

SOURCE_REACTION.
```

---

# 28. Sidedness gate

AGMINER must distinguish:

```text
LOCAL REPULSION

EMBEDDED / TWO-SIDED RESPONSE

EXTERNAL TRUE STANDOFF.
```

A candidate that only produces useful sign while the payload intersects or straddles the source does not pass true stand-off.

---

# 29. Complete energy definition

The governing energy quantity is:

```text
E_CONSERVATIVE_COMPLETE_OPERATING.
```

Where applicable include:

```text
SOURCE PARTICLE / FIELD ENERGY

MEDIATOR SELF-ENERGY

PHYSICAL METRIC FIELD ENERGY

SUPPORT

CONFINEMENT

BAG WALL

LOCALIZATION

STABILIZATION

ACTIVATION

CONTROL

RESERVOIR

FORMATION

RESET

REACTION

RADIATION

GR ATTRACTION

PAYLOAD BACKREACTION

SOURCE BACKREACTION

METRIC BACKREACTION

OFF-STATE ENERGY

RANGE CONTROL

RENORMALIZED VACUUM ENERGY

UV-COMPLETION-REQUIRED PHYSICAL SECTORS.
```

---

# 30. Negative interaction energy cannot hide positive inventory

Preserve both:

```text
E_EXACT_HAMILTONIAN_J
```

and:

```text
E_CONSERVATIVE_COMPLETE_J.
```

Negative binding energy cannot be used to make an operating configuration appear practical if the required positive inventory is above the policy limit.

---

# 31. Early energy lower-bound rejection

Every theory family should expose the strongest cheap lower bound available.

Suggested:

```python
energy_lower_bound(params, config)
```

If:

```text
E_LOWER_BOUND >= 10 MJ
```

under a strict lower-bound proof and the policy requires `<10 MJ`:

```text
REJECT.
```

No field solve.

Note the strict inequality.

An exact proven lower bound of exactly:

```text
10 MJ
```

also eliminates the candidate under the current policy.

---

# 32. Component-level short circuit

If an unavoidable nonnegative component satisfies:

```text
E_COMPONENT >= 10 MJ
```

then:

```text
E_COMPLETE >= 10 MJ.
```

Reject immediately.

Examples:

```text
SOURCE REST ENERGY

MANDATORY WALL ENERGY

MEDIATOR SELF-ENERGY

ACTIVATION RESERVOIR

UNAVOIDABLE SUPPORT.
```

Only apply this when nonnegativity and indispensability are established.

---

# 33. Provenance is a Tier-0 gate

V1 demonstrated that stale preliminary database rows can mimic a false low-energy frontier.

Every numerical claim must carry:

```text
FAMILY_VERSION

ACTION_VERSION

IMPLEMENTATION_VERSION

LEDGER_VERSION

PAYLOAD_BENCHMARK_VERSION

RESULT_STATUS

SUPERSEDES

SUPERSEDED_BY

PROVENANCE_REFERENCE.
```

Recommended result status:

```text
ACTIVE

SUPERSEDED

HISTORICAL_CONTROL

INVALID

UNRESOLVED.
```

Only active trusted results may compete in current ranking.

---

# 34. Historical rows never silently compete

Historical results are useful for:

```text
CONTROL

REGRESSION

TRAINING

FAILURE MEMORY

LITERATURE COMPARISON.
```

They should be marked:

```text
HISTORICAL = TRUE
```

and:

```text
ELIGIBLE_FOR_CURRENT_FRONTIER = FALSE
```

unless explicitly revalidated under the current theory and ledger.

---

# 35. Theory-family contract

Generic AGMINER infrastructure should remain theory-independent.

A family may expose a richer interface than the original plan.

Recommended conceptual contract:

```python
class TheoryFamily:

    family_id()
    family_version()
    action_version()

    parameter_schema()
    sample_bounds()
    canonicalize_params(params)

    canonical_invariants(params, config)
    canonical_invariant_id(params, config)

    analytic_precheck(params, config)
    dimensional_precheck(params, config)
    sign_precheck(params, config)
    universality_precheck(params, config)
    source_existence_precheck(params, config)

    naturalness_precheck(params, config)
    eft_precheck(params, config)
    empirical_precheck(params, config)

    energy_lower_bound(params, config)
    action_oracle(params, config)

    collective_scaling_probe(params, config)

    build_initial_guess(params, neighbor=None)
    solve_coarse(params, initial_guess=None)

    reconstruct_observables(solution, params, config)

    estimate_energy_ledger(solution, params, config)

    finite_payload_response(solution, params, config)

    conservation_checks(solution, params, config)
    support_checks(solution, params, config)
    backreaction_checks(solution, params, config)
    leakage_checks(solution, params, config)

    cheap_stability_checks(solution, params, config)

    mechanism_metrics(solution, params, config)

    serialize_checkpoint(solution, params, config)
```

Not every family needs every method.

Unsupported methods should return an explicit:

```text
NOT_APPLICABLE
```

or:

```text
NOT_IMPLEMENTED
```

rather than silently passing.

---

# 36. Generic core versus family physics

Generic infrastructure belongs in:

```text
src/antigravity_research/agminer/
```

Theory-specific equations belong in:

```text
families/

or

clearly named scientific diagnostic modules.
```

The generic scheduler, database, policy, provenance, reporting, and Pareto systems should not depend on one candidate theory.

---

# 37. Current V6 infrastructure

Preserve the V6 architecture:

```text
agminer/mechanism.py

agminer/oracle.py

agminer/normalization.py

agminer/discovery.py
```

plus corresponding integration in:

```text
storage.py

pareto.py

reporting.py

families/base.py

__init__.py
```

These modules represent a permanent evolution of AGMINER.

---

# 38. Current scientific modules

Current later scientific support includes modules such as:

```text
axial_dirac_meanfield.py

c1_payload_matching.py

universal_metric_support.py
```

along with earlier V-series diagnostic families.

These should remain separate from generic infrastructure.

---

# 39. Database architecture

Primary persistent database:

```text
results/agminer/agminer.sqlite3
```

SQLite remains appropriate because it is:

```text
TRANSACTIONAL

QUERYABLE

RESUMABLE

COMPACT RELATIVE TO RAW SIMULATION OUTPUT

AVAILABLE WITHOUT EXTERNAL SERVICES.
```

---

# 40. Core database tables

Retain core tables conceptually equivalent to:

```text
runs

models

rejections

survivors

region_rules
```

and V6 additions:

```text
mechanism_metrics

action_oracles

collective_scaling.
```

Additional provenance tables may be added if cleaner than overloading model rows.

---

# 41. Models table

Store compact candidate identity and latest screening state.

Suggested important fields:

```text
candidate_id

family_id

family_version

action_version

canonical_invariant_id

params_json

state

tier

result_status

ledger_class

energy_j

payload_surface_min

payload_surface_max

payload_cm

naturalness_margin

eft_margin

stability_proxy

leakage

backreaction

runtime_s

created_run_id
```

---

# 42. Rejections table

Recommended fields:

```text
candidate_id

family_id

failure_code

gate

policy_id

policy_specific

energy_j

proof_reference

result_version

run_id

preserve_detail
```

This permits target-dependent energy rejection without conflating it with permanent physical no-goes.

---

# 43. Action-oracle table

Recommended fields:

```text
oracle_id

canonical_invariant_id

family_id

family_version

oracle_type

proof_reference

ledger_class

proven_lower_bound_j

relaxed_energy_j

realized_energy_j

normalization_invariant

finite_payload_screened

naturalness_screened

universal_metric_screened

support_included

stability_included

trusted_for_reachability

result_status
```

---

# 44. Mechanism-metrics table

Do not populate this merely because an action oracle is attractive.

Recommended fields:

```text
candidate_id

productive_charge_per_joule

productive_participation

kernel_leverage

cancellation_factor

scaffolding_fraction

realization_gap

finite_payload_margin

support_fraction

control_fraction

naturalness_margin

stability_margin

metric_response_class

ledger_class
```

Current count:

```text
0
```

is scientifically correct because no sufficiently complete physical 032 realization has earned promotion.

---

# 45. Collective-scaling table

Store:

```text
candidate_or_oracle_id

collective_parameter

response_exponent_r

energy_exponent_s

efficiency_exponent_r_minus_s

scaffold_exponent

portal_status

finite_payload_status

proof_reference.
```

Do not infer a physical antigravity gain solely from:

```text
r > s.
```

The useful charge must also couple to the physical metric.

---

# 46. Candidate identity

A deterministic physical candidate fingerprint should include:

```text
FAMILY_ID

FAMILY_VERSION

ACTION_VERSION

CANONICAL_PARAMETER_VECTOR

CANONICAL_INVARIANT_ID

PHYSICAL_MODEL_VERSION

PAYLOAD_BENCHMARK_VERSION
```

It should not include the current energy target.

---

# 47. Ledger versioning

The candidate's physics identity and its result interpretation must be separate.

If the physical theory stays fixed but the energy ledger becomes more complete:

```text
SAME PHYSICAL CANDIDATE

NEW RESULT / LEDGER VERSION.
```

Do not silently create a fake new theory candidate just because support energy was added.

---

# 48. Failure-memory hierarchy

AGMINER should distinguish:

```text
EXACT CANDIDATE FAILURE

PROVEN PARAMETER-REGION FAILURE

FAMILY-LEVEL THEOREM FAILURE

OBJECTIVE FAILURE

NUMERICAL UNRESOLVED

SUPERSEDED RESULT.
```

These have different meanings and different retry policies.

---

# 49. Exact failure memory

An exact parameter point that physically fails should not be recomputed without a material reason.

Material reasons include:

```text
THE ACTION CHANGED

THE SOURCE MODEL CHANGED

THE PHYSICAL LEDGER CHANGED

A PREVIOUS NUMERICAL BUG WAS FIXED

A DECLARED APPROXIMATION WAS REMOVED.
```

A higher grid alone is generally not a new physical candidate.

---

# 50. Region exclusion

Do not ban neighborhoods based on one failed point.

A region may be excluded only by:

```text
ANALYTIC LOWER BOUND

MONOTONICITY RESULT

NO-GO THEOREM

SIGN THEOREM

GHOST DOMAIN

INVALID KINEMATIC DOMAIN

SOURCE-EXISTENCE THEOREM

PROVEN RANGE LIMIT

EMPIRICAL EXCLUSION
```

with a proof/reference recorded.

---

# 51. Numerical failure is not physics failure

Permanent distinction:

```text
PHYSICS_REJECTED
!=
NUMERICALLY_UNRESOLVED.
```

For a difficult solve:

```text
PRIMARY ATTEMPT

CHEAP ALTERNATE SEED / CONTINUATION

IF BOTH FAIL:
NUMERICALLY_UNRESOLVED
```

unless a separate physical theorem establishes nonexistence.

Do not let the miner spin forever.

---

# 52. Scientific failure codes

The failure taxonomy should remain extensible.

Existing generic classes:

```text
E — ENERGY

T — THEORY / OPERATOR

N — NATURALNESS / EFT / NORMALIZATION

F — FIELD EXISTENCE / LOCALIZATION

P — PAYLOAD / SIGN / SIDEDNESS

C — CONSERVATION / ENERGY CONDITIONS

S — STABILITY

L — LEAKAGE

B — BACKREACTION

R — RANGE

D — DUPLICATE / PROVENANCE

X — NUMERICAL / INFRASTRUCTURE
```

---

# 53. Current durable 032 failure memory

Preserve at minimum:

```text
P001
asymmetron_external_wall_sign
```

Published/tested minimal asymmetron bubble does not provide the required external outward sign in the tested architecture.

```text
P002
kinetic_conformal_static_external_sign
```

The tested minimal published kinetic-conformal static sign is wrong for the desired localized branch.

```text
P003
regular_static_shift_current_no_source
```

Regular isolated positive-current exact-shift static monopole is closed under the stated assumptions.

```text
E003
ordinary_electron_microscopic_source_rest_energy_floor
```

Ordinary-electron implementation catastrophically exceeds the current objective.

```text
N004
axial_dirac_selfconsistent_source_cutoff_margin
```

The old V15 source fails its own EFT cutoff after exact fermion self-response.

```text
N005
controlled_nr_stoner_loop_conflict
```

Controlled nonrelativistic spontaneous polarization conflicts with acceptable loop load.

```text
N006
axial_fixed_order_wavefunction_running_control
```

V17 oblate loop≈0.30 source is not controlled by a small fixed-order wavefunction-running expansion.

```text
N007
sphere_geometry_demag_loop_remap
```

The oblate microscopic state cannot simply be transplanted into the sphere.

```text
N008
sphere_fixed_order_wavefunction_running_control
```

V18 sphere likewise fails small fixed-order canonicalization control.

````

Do not reuse old failure-code names for different physics.

---

# 54. Failure anatomy is itself scientific data

AGMINER should answer:

```text
WHY ARE WE FAILING?
````

not merely:

```text
HOW MANY FAILED?
```

Useful reports include:

```text
FAILURE COUNT BY PHYSICAL GATE

LOWEST-ENERGY FAILURE OF EACH TYPE

MOST COMMON FAMILY NO-GO

CLOSEST ENERGY OBJECTIVE MISS

BEST SOURCE THAT FAILS SUPPORT

BEST SOURCE THAT FAILS RG

BEST SOURCE THAT FAILS STABILITY.
```

This information should guide theory changes.

---

# 55. Hard gates versus ranking metrics

Never merge validity and desirability into one opaque score.

First:

```text
PASS / FAIL / UNRESOLVED
```

then rank.

Hard gates may include:

```text
BOUNDED HAMILTONIAN

NO GHOST

CORRECT PHYSICAL SIGN

UNIVERSAL METRIC

SOURCE EXISTENCE

FINITE-PAYLOAD OUTWARD SIGN

NO SOURCE-PAYLOAD INTERSECTION

LOCALIZATION

CONSERVATION

POSITIVE ENERGY AS CLAIMED

EFT CONTROL

NATURALNESS

LEAKAGE

BACKREACTION

STABILITY AT DECLARED LEVEL

EMPIRICAL NONEXCLUSION

ENERGY POLICY.
```

---

# 56. Ranking metrics

For candidates that are genuinely comparable, rank using vectors such as:

```text
COMPLETE ENERGY

ENERGY MARGIN

ACTION-ORACLE ENERGY

REALIZATION GAP

PRODUCTIVE CHARGE PER JOULE

PRODUCTIVE PARTICIPATION

KERNEL LEVERAGE

CANCELLATION

SCAFFOLDING FRACTION

SUPPORT FRACTION

NATURALNESS MARGIN

EFT MARGIN

STABILITY MARGIN

PAYLOAD MARGIN

FIELD UNIFORMITY

LEAKAGE MARGIN

BACKREACTION MARGIN

DISTANCE FROM PARAMETER BOUNDARIES.
```

---

# 57. No Pareto ranking of incomparable ledger classes

Do not put:

```text
FIELD-ONLY 59 kJ
```

and:

```text
COMPLETE 8 MJ
```

on the same energy Pareto frontier as though the first were superior.

Pareto comparisons must require compatible:

```text
LEDGER CLASS

PHYSICS SCOPE

PAYLOAD BENCHMARK

PROVENANCE STATUS.
```

---

# 58. Current empty mechanism frontier is correct

After V18:

```text
MECHANISM_METRIC_COUNT = 0

MECHANISM_PARETO_COUNT = 0

CERTIFIED_SURVIVOR_COUNT = 0.
```

Do not fill these because the partial energy looks exciting.

This restraint is a feature.

---

# 59. Multi-fidelity pipeline — Level 0

## Analytical / theorem level

Target cost:

```text
MICROSECONDS
TO
SECONDS
```

Possible tests:

```text
PROVENANCE

DIMENSIONAL CONSISTENCY

CANONICAL NORMALIZATION

SIGN

SOURCE-EXISTENCE THEOREM

MONOPOLE / MULTIPOLE TOPOLOGY

HAMILTONIAN BOUNDEDNESS

GHOST

TACHYON

RANGE

COLLECTIVE SCALING

ANALYTIC ENERGY BOUND

NATURALNESS

EFT

EMPIRICAL STRUCTURAL EXCLUSION.
```

If Level 0 kills the theory, stop.

---

# 60. Multi-fidelity pipeline — Level 1

## Reduced action / oracle level

Possible calculations:

```text
ACTION-SPECIFIC RELAXED OPTIMUM

LOW-DIMENSIONAL RESPONSE MATRIX

SOURCE SCALING

FINITE-PAYLOAD APPROXIMATE ORACLE

MEAN-FIELD LOCAL STATE

SUPPORT LOWER BOUND.
```

Purpose:

```text
DETERMINE WHETHER THE UNDERLYING ACTION HAS ENOUGH HEADROOM TO JUSTIFY REALIZATION WORK.
```

---

# 61. Multi-fidelity pipeline — Level 2

## Microscopic source level

Require increasingly explicit:

```text
ACTION

FIELD EQUATIONS

SOURCE CHARGE

MICROSCOPIC ENERGY

SOURCE REACTION

LOCAL CONSERVATION

FIELD LOCALIZATION

EFT MARGIN.
```

Examples:

```text
Q-BALL

DIRAC MEAN FIELD

TOPOLOGICAL SOURCE

BAG / SOLITON.
```

---

# 62. Multi-fidelity pipeline — Level 3

## Exact finite-payload level

Compute:

```text
ACTUAL FINITE PAYLOAD

BOUNDARY TRANSMISSION

MULTIPOLES

SURFACE MINIMUM

VOLUME AVERAGE

SOURCE REACTION

CONVERGENCE.
```

V17 is an example of this level for the active partial architecture.

---

# 63. Multi-fidelity pipeline — Level 4

## Physical support / stability level

Add:

```text
SUPPORT ACTION

CONFINEMENT

WALL ENERGY

LOCAL CONSERVATION

RADIAL STABILITY

SHAPE STABILITY

SOURCE-SUPPORT COUPLING.
```

V19 begins this stage for the spherical source.

---

# 64. Multi-fidelity pipeline — Level 5

## Quantum / UV / empirical level

Require:

```text
RENORMALIZED VACUUM

RG FLOW

CANONICAL LOW-ENERGY MATCH

UV COMPLETION

COMPANION OPERATORS

FIFTH-FORCE / EP / PPN

ASTROPHYSICAL CONSTRAINTS

COSMOLOGICAL CONSTRAINTS.
```

---

# 65. Multi-fidelity pipeline — Level 6

## Full certification level

Eventually require:

```text
FULL COUPLED SOURCE + PAYLOAD + SUPPORT

NONLINEAR STABILITY

ACTIVATION

OFF STATE

RESET

RADIATION

FULL METRIC BACKREACTION

COMPLETE OPERATING ENERGY

INDEPENDENT RECONSTRUCTION.
```

Only then should:

```text
CERTIFIED_SURVIVOR
```

be considered.

---

# 66. Naturalness remains early

031 established that naturalness cannot be postponed until after expensive stability work.

Every family must identify:

```text
LIGHT MODE MASS

COUPLING SCALE

EFT CUTOFF

HEAVY THRESHOLDS

PROTECTION SYMMETRY

PROTECTION BREAKING

EXPECTED LOOP CORRECTIONS

RG BEHAVIOR.
```

A label such as:

```text
PROTECTED
```

is not evidence.

Protection must be calculable.

---

# 67. Fixed-order failure versus full quantum failure

Do not interpret:

```text
FIXED_ORDER_CONTROL = RED
```

as automatically:

```text
THE THEORY IS DEAD.
```

Instead determine whether the failure indicates:

```text
LARGE LOG REQUIRING RG RESUMMATION

GENUINE STRONG COUPLING

LANDAU POLE

GHOST

TACHYON

UV COMPLETION FAILURE.
```

This distinction is central to V17/V18.

---

# 68. Empirical screening moves earlier when scales become low

If AGMINER finds a candidate with an unusually low EFT or metric scale, empirical constraints must move forward in the pipeline.

Current active scale:

```text
M ~ 24 keV.
```

This makes:

```text
FIFTH-FORCE

EQUIVALENCE PRINCIPLE

ATOMIC

STELLAR

COSMOLOGICAL

LOW-ENERGY PRODUCTION

VALID EFT MATCHING
```

high-information gates.

Do not defer them until after months of numerical stability work.

---

# 69. Current V13–V18 discovery chain

Preserve this as a calibration of the new AGMINER workflow.

```text
V13
STATIC KINETIC-CONFORMAL SIGN
+
REGULAR STATIC MONOPOLE NO-GO

V14
ZERO-NET DERIVATIVE DIPOLE ESCAPE

V15
EXPLICIT HIDDEN AXIAL MICROSCOPIC SOURCE

V16
EXACT DIRAC MEAN FIELD
+
V15 SOURCE KILLED
+
NR STONER ROUTE KILLED
+
FLAVOR SHORTCUT CLOSED

V17
EXACT FINITE PAYLOAD
+
C1 MATCH
+
SUPPORT-TRACE CORRECTION
+
59.42-kJ PARTIAL CORRIDOR
+
FIXED-ORDER RG CONTROL RED

V18
UNIVERSAL-METRIC PROVENANCE
+
CANONICAL RESCALING INVARIANT
+
SUPPORT-GEOMETRY AUDIT
+
REOPTIMIZED SPHERICAL SOURCE
+
3.419-MJ PARTIAL CORRIDOR
```

This sequence is the template for future candidate-specific AGMINER work.

---

# 70. Current V17 energy leader

Preserve:

```text
SOURCE MORPHOLOGY =
OBLATE

M =
~24.2054 keV

PARTIAL ENERGY =
~59.419738 kJ

SURFACE MIN =
1 g

SURFACE NONUNIFORMITY =
~16.37X

MAX SOURCE REACTION SCOUT =
~2.47%

PHYSICAL ANISOTROPIC SUPPORT =
OPEN

FIXED-ORDER RG =
RED
```

Status:

```text
ACTION ORACLE / PARTIAL REALIZATION

ALIVE

UNTRUSTED FOR COMPLETE REACHABILITY.
```

---

# 71. Current V18 support-realization leader

Preserve:

```text
MORPHOLOGY =
SPHERE

M =
~23.9713 keV

PARTIAL ENERGY =
~3.419157493 MJ

FIELD ENERGY =
~2.5456 kJ

OCCUPIED DIRAC BANDS =
~2.579780 MJ

DEC SUPPORT LOWER BOUND =
~0.836832 MJ

NOMINAL REMAINING TO 10 MJ =
~6.580843 MJ

SURFACE MIN =
1 g

SURFACE NONUNIFORMITY =
~96.24X

MAX SOURCE REACTION SCOUT =
~1.49%

PHYSICAL BAG =
NOT CONSTRUCTED

FIXED-ORDER RG =
RED.
```

Status:

```text
SUPPORT-FRIENDLY PARTIAL ORACLE

ALIVE

UNTRUSTED FOR COMPLETE REACHABILITY.
```

---

# 72. Current active task

Immediate next run:

```text
032V19_SPHERICAL_BAG_SUPPORT_UV_MATCHING_AND_EMPIRICAL_GATE
```

Do not start another broad energy-optimization campaign before V19 closes.

---

# 73. V19 objective

V19 should answer:

> **Can the V18 spherical partial source be upgraded into an explicit positive-energy supported microscopic source with controlled low-energy quantum/UV interpretation and no immediate empirical fatality while retaining finite-payload outward response and a complete energy path below 10 MJ?**

This is a falsification gate.

It is not an optimizer.

---

# 74. V19 support requirements

Construct an explicit support sector with:

```text
ACTION

FINITE WALL THICKNESS

POSITIVE HAMILTONIAN

COMPLETE STRESS TENSOR

LOCAL CONSERVATION

INTERIOR PRESSURE BALANCE

SURFACE TENSION

FINITE TOTAL ENERGY

SOURCE REACTION

NO PRESCRIBED EXTERNAL STRESS.
```

A stress lower bound is not a bag.

---

# 75. V19 stability requirements

At minimum address:

```text
RADIAL EQUILIBRIUM

L=0 RADIAL MODE

L=1 TRANSLATION HANDLING

L=2 SHAPE MODE

WALL-SOURCE RELATIVE MOTION

FERMION DENSITY MODES

FERMION POLARIZATION MODES.
```

Static pressure balance does not prove stability.

---

# 76. V19 RG / UV requirements

At minimum determine:

```text
Z_PHI(mu)

C1(mu)

F_PSI(mu)

COMPANION OPERATORS

LOWEST VALID CUTOFF

STRONG-COUPLING SCALE

OUTWARD-SIGN PRESERVATION

UNIVERSAL-METRIC PRESERVATION.
```

Do not use canonical field rescaling as an artificial efficiency lever.

---

# 77. V19 quantum-vacuum requirement

The current ledger includes occupied positive-energy fermion bands.

It does not yet include a complete renormalized negative-energy Dirac sea.

Need calculate or tightly bound effects on:

```text
VACUUM ENERGY

SCALAR KINETIC NORMALIZATION

PRESSURE

SOURCE EQUILIBRIUM

STABILITY

WILSON COEFFICIENTS.
```

---

# 78. V19 empirical gate

At the actual low scale, investigate:

```text
EQUIVALENCE PRINCIPLE

FIFTH FORCE

PRECISION GRAVITY

ATOMIC / MOLECULAR PHYSICS

STELLAR COOLING

SUPERNOVA

BBN

COSMOLOGY

HIDDEN-FERMION PRODUCTION

COLLIDER MATCHING ONLY WHERE EFT IS VALID

OFF-STATE LEAKAGE.
```

An invalid high-energy contact-EFT extrapolation is not a constraint.

It is also not evidence of safety.

---

# 79. Return-to-broad-search condition

Do not return to giant broad mining merely because V19 is difficult.

Return to broad AGMINER discovery only if:

```text
CURRENT KINETIC-CONFORMAL CLASS IS CLOSED

OR

ITS COMPLETE ENERGY FLOOR IS CLEARLY ABOVE 10 MJ

OR

ITS UV COMPLETION CANNOT PRESERVE THE REQUIRED SIGN

OR

ITS EMPIRICAL CONSTRAINTS ARE FATAL

OR

ITS SOURCE/SUPPORT IS FUNDAMENTALLY UNSTABLE

OR

A NEW THEORY CLASS HAS A CLEARLY BETTER ANALYTIC ORACLE.
```

---

# 80. Broad search strategy when reactivated

Do not use an enormous rectangular grid.

Recommended adaptive mix:

```text
GLOBAL LOW-DISCREPANCY EXPLORATION

LOCAL SURVIVOR REFINEMENT

BOUNDARY / NOVELTY EXPLORATION

THEOREM-GUIDED REGION EXCLUSION.
```

The old 60/30/10 allocation may be used as a starting point, not a permanent law.

---

# 81. Sobol / low-discrepancy search

Preferred global sampler:

```python
scipy.stats.qmc.Sobol
```

Alternative:

```python
LatinHypercube
```

Store:

```text
SAMPLER SEED

SAMPLE INDEX

FAMILY VERSION

CONFIG HASH.
```

Searches must be exactly resumable.

---

# 82. Local exploitation

Around promising physical basins:

```text
PERTURB PARAMETERS

REUSE CONTINUATION

SHRINK LOCAL STEP SIZE IF IMPROVING

MAINTAIN DIVERSITY.
```

Do not let one fragile boundary basin consume all compute.

---

# 83. Continuation

For nonlinear BVP families:

```text
NEARBY SOLVED MODEL
→
INITIAL GUESS FOR NEW MODEL.
```

Keep warm-start caches bounded.

Do not persist every coarse field to disk.

---

# 84. Surrogate models

Surrogates may later predict:

```text
ENERGY

FAILURE PROBABILITY

PAYLOAD RESPONSE

NATURALNESS

STABILITY

REALIZATION GAP.
```

They may:

```text
PRIORITIZE

DEPRIORITIZE

SUGGEST.
```

They may not establish:

```text
SCIENTIFIC PASS

SCIENTIFIC NO-GO
```

without a physical or analytical basis.

---

# 85. Automatic family-stop rules

Stop a family when, for example:

```text
ANALYTIC LOWER BOUND >= 10 MJ THROUGHOUT THE VALID DOMAIN

NO PHYSICAL OUTWARD SIGN EXISTS

NO UNIVERSAL METRIC EXISTS

NATURALNESS FAILS THE ENTIRE FAMILY

COLLECTIVE SCALING HAS r <= s THROUGHOUT

NO LOCALIZED SOURCE EXISTS

ALL PHYSICAL SOURCES FAIL PAYLOAD SIDEDNESS

ALL PROMISING SOURCES ARE TRULY UNSTABLE

EMPIRICAL CONSTRAINTS EXCLUDE THE REQUIRED REGION

NO IMPROVEMENT AFTER ADEQUATE COVERAGE.
```

Record the family-level reason.

---

# 86. Search-budget philosophy

AGMINER should optimize:

```text
INFORMATION GAIN PER COMPUTE
```

not:

```text
CANDIDATES PER HOUR.
```

The best run may evaluate:

```text
ONE ANALYTICAL THEOREM
```

and eliminate:

```text
10^12 PARAMETER POINTS.
```

That is preferable to a giant simulation campaign.

---

# 87. Anti-brute-force rule

Before launching a huge scan ask:

```text
CAN A SIGN THEOREM REMOVE THIS CLASS?

CAN A CANONICAL INVARIANT REMOVE THIS DIMENSION?

CAN AN ENERGY LOWER BOUND REMOVE THIS REGION?

CAN A SOURCE-EXISTENCE THEOREM REMOVE IT?

CAN COLLECTIVE SCALING REMOVE IT?

CAN EMPIRICAL DATA REMOVE IT?

CAN A STABILITY NECESSITY REMOVE IT?
```

Only scan the dimensions that remain physically independent.

---

# 88. Disk-light architecture

Permanent principle:

> **Store knowledge, not simulation clutter.**

Rejected ordinary candidate:

```text
DATABASE ROW ONLY.
```

Ordinary partial candidate:

```text
DATABASE ROW
+
OPTIONAL SMALL SUMMARY.
```

Important oracle:

```text
COMPACT JSON / CSV.
```

Top physical candidate:

```text
CHECKPOINT IF NEEDED.
```

---

# 89. Field-array retention

Default rejected candidate:

```text
NO ARRAY.
```

Ordinary coarse survivor:

```text
NO ARRAY AFTER OBSERVABLE EXTRACTION.
```

Current high-value candidate:

```text
KEEP ONLY NECESSARY REPRODUCIBLE CHECKPOINTS.
```

Manual pinning overrides automatic deletion.

---

# 90. Log policy

No per-candidate routine logs.

Main campaign log may rotate.

Log:

```text
RUN START

RUN END

PROGRESS SUMMARY

NEW ORACLE

NEW PHYSICAL FAILURE CLASS

NEW BEST TRUSTED COMPARABLE RESULT

UNEXPECTED EXCEPTION

DATABASE CHECKPOINT

STOP / RESUME.
```

Do not log every solver iteration.

---

# 91. Scientific result artifacts

Major V-series scientific gates may generate dedicated:

```text
JSON

CSV

LOG
```

files because they are durable research results.

This is distinct from ordinary high-throughput candidate rows.

---

# 92. Live summary files

Maintain lightweight current views such as:

```text
results/agminer/top_candidates.csv

results/agminer/pareto_frontier.csv

results/agminer/failure_counts.csv

results/agminer/run_summary.json

results/agminer/mechanism_frontier.csv

results/agminer/oracle_learning.csv

results/agminer/collective_scaling.csv
```

These are convenience views.

SQLite remains authoritative for miner state.

Scientific result JSON/CSV files remain authoritative for their specific completed run.

---

# 93. Database growth

The current SQLite database is already on the order of tens of megabytes.

Do not allow uncontrolled growth.

Prefer:

```text
COMPACT ROWS

NO REPEATED BLOBS

NO LARGE FIELD ARRAYS IN SQLITE

BATCH COMMITS

PERIODIC WAL CHECKPOINTING.
```

If future campaigns push database size substantially upward, archive historical campaigns or normalize storage rather than silently allowing multi-gigabyte growth.

---

# 94. SQLite write architecture

Worker processes should not independently write SQLite.

Recommended:

```text
MAIN PROCESS
    SCHEDULER
    DEDUPE
    RESULT WRITER
    REPORTER

WORKERS
    PHYSICS EVALUATION ONLY
```

One authoritative writer avoids lock contention.

---

# 95. Crash recovery

On restart:

```text
READ DATABASE

IDENTIFY ABANDONED RUNNING ITEMS

MARK INTERRUPTED

RESTORE CONFIG

RESTORE SAMPLER POSITION

REBUILD CURRENT TRUSTED FRONTIERS

REBUILD FAILURE MEMORY

SKIP TERMINAL PHYSICAL FAILURES

CONTINUE.
```

Do not start from zero.

---

# 96. Manual stop

Manual stop is normal operation.

Required flow:

```text
USER REQUESTS STOP

        ↓

STOP SCHEDULING NEW WORK

        ↓

FINISH OR SAFELY CANCEL CURRENT SMALL WORK UNITS

        ↓

COMMIT PENDING RESULTS

        ↓

SAVE SAMPLER / QUEUE STATE

        ↓

UPDATE REPORTS

        ↓

CHECKPOINT WAL

        ↓

CLEAN STOP.
```

---

# 97. Interrupt handling

At minimum support:

```text
CTRL+C

SIGTERM

CLI STOP COMMAND.
```

First interrupt:

```text
GRACEFUL STOP.
```

A later forced interruption may terminate remaining work while preserving committed transactions.

---

# 98. Anytime result inspection

The user must be able to inspect AGMINER while:

```text
RUNNING

STOPPED

INTERRUPTED

COMPLETED.
```

Read-only commands should support:

```text
status

top

pareto

oracles

mechanisms

scaling

failures

lookup.
```

---

# 99. Recommended CLI

Conceptually:

```text
python -m antigravity_research.agminer run

python -m antigravity_research.agminer status

python -m antigravity_research.agminer top

python -m antigravity_research.agminer pareto

python -m antigravity_research.agminer oracles

python -m antigravity_research.agminer mechanisms

python -m antigravity_research.agminer scaling

python -m antigravity_research.agminer failures

python -m antigravity_research.agminer lookup

python -m antigravity_research.agminer stop

python -m antigravity_research.agminer resume

python -m antigravity_research.agminer export
```

---

# 100. Status output

Current-style status should include more than old candidate counts.

Example fields:

```text
RUN_ID

RUN_MODE

ACTIVE_FAMILY

ACTIVE_CANDIDATE

ENERGY_POLICY

MODELS

REJECTIONS

ACTION_ORACLES

COLLECTIVE_SCALING_RECORDS

MECHANISM_METRICS

SURVIVORS

TRUSTED_PARETO_COUNT

NUMERICAL_UNRESOLVED

CURRENT_ACTIVE_ORACLE

LOWEST_COMPARABLE_ENERGY

CURRENT_PHYSICAL_BOTTLENECK

DATABASE_SIZE

STOP_REQUESTED

ELAPSED_TIME.
```

---

# 101. Top output

`top` must not mix incompatible result classes.

Possible separate views:

```text
TOP COMPLETE CANDIDATES

TOP MICROSCOPIC PARTIALS

TOP ACTION ORACLES

TOP ENERGY LEADERS

TOP ROBUSTNESS LEADERS.
```

If there are no complete candidates, say:

```text
NONE.
```

Do not fill the table with partials under a misleading heading.

---

# 102. Failure lookup

The user should be able to ask:

```text
HAVE WE TESTED THIS?
```

Return:

```text
CANDIDATE_ID

CANONICAL_INVARIANT_ID

TESTED

RESULT_STATUS

FAILURE_CODE

FAILURE_GATE

POLICY_ID

POLICY_SPECIFIC

ENERGY

RUN

SUPERSEDED_STATUS.
```

---

# 103. Manual pinning

Allow:

```text
PINNED = TRUE.
```

Pinned models/oracles should not lose detailed checkpoints automatically.

Pinning does not change scientific status.

---

# 104. Regression philosophy

Two regression concepts now exist.

Historical scientific baseline:

```text
94 PASSED.
```

This preserves the original protected known-solution foundation.

Current complete suite:

```text
238 PASSED.
```

For new major claims:

```text
FULL CURRENT SUITE MUST PASS.
```

Do not say:

```text
94 IS THE CURRENT FULL SUITE.
```

---

# 105. Regression versus independent verification

Passing tests means:

```text
IMPLEMENTATION CONSISTENCY.
```

It does not automatically mean:

```text
INDEPENDENT SCIENTIFIC VERIFICATION.
```

Central scientific results still require independent reconstruction where feasible.

---

# 106. Required independent checks

Examples:

```text
ACTION ORACLE
vs
INDEPENDENT ANALYTICAL BOUND

FIELD ENERGY
vs
DIRECT NUMERICAL INTEGRAL

FINITE-PAYLOAD MULTIPOLES
vs
DIRECT BOUNDARY-VALUE SOLVE

SOURCE CURRENT
vs
ASYMPTOTIC FIELD COEFFICIENT

DIRAC BAND INTEGRAL
vs
INDEPENDENT QUADRATURE

STABILITY EIGENMODE
vs
FINITE-AMPLITUDE CURVATURE

RG RUNNING
vs
MATCHED UV CALCULATION.
```

---

# 107. Candidate state machine

Recommended expanded states:

```text
NEW

CANONICALIZATION_RUNNING

REJECTED_NORMALIZATION

THEORY_PREFLIGHT_RUNNING

REJECTED_THEORY

ORACLE_RUNNING

ORACLE_ONLY

SOURCE_REALIZATION_RUNNING

REJECTED_SOURCE_EXISTENCE

MICROSCOPIC_PARTIAL

PAYLOAD_RUNNING

REJECTED_PAYLOAD

SUPPORT_RUNNING

REJECTED_SUPPORT

RG_UV_RUNNING

REJECTED_RG_UV

STABILITY_RUNNING

REJECTED_STABILITY

EMPIRICAL_RUNNING

REJECTED_EMPIRICAL

NUMERICALLY_UNRESOLVED

PARTIAL_SURVIVOR

CERTIFICATION_READY

CERTIFICATION_IN_PROGRESS

CERTIFIED

INVALIDATED_BY_LATER_GATE

SUPERSEDED.
```

Do not force every old database row into these immediately if migration risks corrupting history.

Backward-compatible mapping is acceptable.

---

# 108. Scientific promotion ladder

A useful internal promotion ladder:

```text
LEVEL 0
THEORY IDEA

LEVEL 1
CANONICAL PHYSICAL OPERATOR

LEVEL 2
ACTION ORACLE

LEVEL 3
SOURCE EXISTENCE

LEVEL 4
MICROSCOPIC SOURCE

LEVEL 5
FINITE-PAYLOAD RESPONSE

LEVEL 6
SUPPORT + STABILITY

LEVEL 7
RG / UV + QUANTUM CONTROL

LEVEL 8
EMPIRICAL CONSISTENCY

LEVEL 9
COMPLETE OPERATING LEDGER

LEVEL 10
CERTIFIED PHYSICAL MODEL.
```

Current V17/V18 do not reach Level 10.

---

# 109. Promotion to mechanism metrics

Only record full `MechanismMetrics` when the candidate has enough physical structure that the measured quantities refer to the same source.

Suggested minimum:

```text
DEFINED ACTION

CANONICAL NORMALIZATION

MICROSCOPIC SOURCE

FINITE PAYLOAD

SOURCE ENERGY

MEDIATOR ENERGY

MEANINGFUL SUPPORT ACCOUNTING

PHYSICAL METRIC RESPONSE.
```

This prevents meaningless cross-model factorization.

---

# 110. Promotion to certification-ready

Under the current project, `CERTIFICATION_READY` should require at minimum:

```text
PHYSICAL ACTION

CANONICAL NORMALIZATION

CORRECT UNIVERSAL METRIC SIGN

MICROSCOPIC SOURCE

FINITE PAYLOAD SURFACE >= 1 g

COMPLETE STATIC SOURCE / FIELD / SUPPORT LEDGER

ENERGY < 10 MJ UNDER CURRENT POLICY

LOCAL CONSERVATION

POSITIVE HAMILTONIAN

EFT CONTROL

NATURALNESS CONTROL

DECLARED LINEAR STABILITY

NO IMMEDIATE EMPIRICAL FATALITY

ROBUSTNESS CHECK

INDEPENDENT RECONSTRUCTION OF CENTRAL OBSERVABLE.
```

Certification-ready is still not certified.

---

# 111. Full certification

A final certified physical model eventually needs substantially more:

```text
FULL COUPLED SOURCE-PAYLOAD-SUPPORT SOLUTION

NONLINEAR STABILITY

ACTIVATION

OFF STATE

RESET

RADIATION

FULL METRIC BACKREACTION

COMPLETE OPERATING ENERGY

EMPIRICAL CLOSURE

EFT / UV COMPLETION

RECIPROCITY

LONG-TIME CONSISTENCY.
```

---

# 112. Current energy-policy regression tests

Mandatory policy tests should now use MJ and strict `<`.

Examples:

```text
E =
9,999,999.999 J

PASS
```

```text
E =
10,000,000.000 J

REJECT
```

```text
E =
10,000,000.001 J

REJECT
```

No physical tolerance above the limit.

Numerical uncertainty must be represented separately.

---

# 113. Uncertain energy

Store where appropriate:

```text
E_ESTIMATE

E_LOWER

E_UPPER.
```

Policy:

```text
IF PROVEN E_LOWER >= 10 MJ:
    REJECT

IF E_UPPER < 10 MJ:
    ENERGY POLICY ROBUSTLY PASSES AT THIS LEDGER LEVEL

IF INTERVAL CROSSES 10 MJ:
    BORDERLINE
    REQUIRE REFINEMENT.
```

Do not hide uncertainty in floating-point tolerance.

---

# 114. Energy-margin categories

For **comparable complete ledgers**, useful current categories might be:

```text
<1 MJ
EXCEPTIONAL

1–5 MJ
STRONG

5–8 MJ
LIMITED BUT USEFUL MARGIN

8–10 MJ
BORDERLINE

>=10 MJ
FAIL CURRENT POLICY.
```

Do not apply these categories to incomplete action oracles without labeling them as partial.

---

# 115. Robustness before promotion

Before expensive promotion perturb sensitive physical parameters.

Possible:

```text
±0.5%

±1%

DOMAIN

BOUNDARY CONDITION

GRID

SOURCE GEOMETRY

EFT SCALE.
```

Record whether the candidate is:

```text
INTERIOR

EDGE

RAZOR-THIN.
```

Do not automatically reject edge candidates, but rank them separately.

---

# 116. Constraint-boundary pathology

Maintain separate views:

```text
ABSOLUTE LOWEST PARTIAL ENERGY

ROBUST LOWEST ENERGY

SUPPORT-FRIENDLY

NATURALNESS-FRIENDLY

STABILITY-FRIENDLY.
```

This is why V17 and V18 are both preserved.

---

# 117. Search diversity

When broad mining resumes, do not allow near-duplicate candidates to occupy every shortlist slot.

Cluster by:

```text
CANONICAL PARAMETER DISTANCE

CANONICAL INVARIANT FAMILY

MORPHOLOGY

PHYSICAL MECHANISM.
```

Retain multiple basins.

---

# 118. Source morphology is physical, not cosmetic

V18 established that changing geometry can alter:

```text
DEMAGNETIZATION FACTOR

LOOP LOAD

MICROSCOPIC SELF-CONSISTENCY.
```

Therefore a source cannot simply be reshaped while holding its microscopic state fixed unless that invariance is proved.

Permanent rule:

> **Geometry changes may require microscopic reoptimization.**

---

# 119. Support is part of the source

Never permit:

```text
SOURCE STRESS
```

without:

```text
THE STRESS THAT HOLDS IT.
```

A lower support bound is useful.

It is not a support realization.

A prescribed external force is not a completed source.

---

# 120. Productive participation versus support tax

Track both:

```math
f_{\rm prod}
=
\frac{
E_{\rm directly\ productive}
}{
E_{\rm total}
}
```

and:

```math
\tau_{\rm scaffold}
=
\frac{
E_{\rm scaffold}
}{
E_{\rm total}
}.
```

When exact decomposition is ambiguous, report the definition used.

---

# 121. Source reaction is mandatory

Any metric-active source must respond to the same mediator/field it creates.

Track:

```text
SOURCE SELF-REACTION

PAYLOAD-INDUCED SOURCE REACTION

ENVIRONMENTAL REACTION.
```

Frozen-source payload oracles are useful only as preflights.

---

# 122. Reciprocity

A universal physical metric implies reciprocal interaction.

Eventually solve:

```text
SOURCE → PAYLOAD

PAYLOAD → SOURCE

EARTH → SOURCE

SOURCE → EARTH / ENVIRONMENT.
```

Do not assume strong payload response and zero source response.

---

# 123. Far-field leakage

Track:

```text
MONOPOLE

DIPOLE

HIGHER MULTIPOLES

FAR-FIELD METRIC RESPONSE

OFF-STATE LEAKAGE.
```

The current derivative source's zero net scalar monopole is useful.

It does not automatically solve empirical constraints.

---

# 124. Stability is multi-sector

Eventually require as relevant:

```text
RADIAL

TRANSLATIONAL

NONAXISYMMETRIC

SHAPE

FRAGMENTATION

FERMION DENSITY

FERMION POLARIZATION

SUPPORT WALL

SOURCE-WALL RELATIVE MOTION

PAYLOAD-COUPLED MODES.
```

018C remains the canonical warning:

```text
FIELD EXISTS
BUT
PHYSICAL REALIZATION DIES BY INSTABILITY.
```

---

# 125. Translation zero modes

For isolated solitons, translational Goldstone modes must be handled analytically before interpreting small `l=1` eigenvalues as instabilities.

The 031B2 experience should remain encoded as a stability-method rule.

---

# 126. No parameter forcing

Never change:

```text
PAYLOAD

ENERGY LEDGER

LEAK LIMIT

BACKREACTION LIMIT

NATURALNESS GATE

SUPPORT DEFINITION

STABILITY DEFINITION

GRID-CONVERGENCE REQUIREMENT
```

because an attractive candidate would otherwise fail.

If the scientific definition changes for an independent reason, version it explicitly.

---

# 127. No target forcing

The formal energy objective is external policy.

A candidate should not be physically redesigned merely to produce a numerically attractive headline.

If the candidate fails:

```text
RECORD

UNDERSTAND

MOVE ON
```

unless a physically motivated new mechanism changes the problem.

---

# 128. No stale-oracle promotion

If a later run adds missing physics and increases energy:

```text
OLD LOWER NUMBER
=
SUPERSEDED FOR THAT CLAIM CLASS.
```

It may remain in the database as a historical oracle.

It must not compete as the current realized energy.

---

# 129. No hidden completeness inflation

Forbidden:

```text
PARTIAL_OPTIMISTIC
→
COMPLETE
```

without adding every omitted physical sector.

Promotion must be explicit and auditable.

---

# 130. Permanent closed shortcuts

Do not reopen without genuinely new physics:

```text
PURE-GR PRACTICAL <10-MJ ROUTE
closed by 1/G burden

PROTECTED VECTOR IMPLEMENTATIONS THROUGH 022A
closed

MINIMAL 031 B7 SCALAR DRESSING
closed

031F0 UNPROTECTED ULTRALIGHT FIELD-VALUE SCALAR
closed

MINIMAL PURE STATIC DISFORMAL g00 ROUTE
closed

GHOST KAPPA RAW-COUPLING GAIN
normalization redundancy

032G/H INDEPENDENT COLLECTIVE SOURCE SCALING
closed in corrected source-aware form

MINIMAL STATIC SCALAR-TENSOR / YUKAWA BRANCHES
attractive / zero in tested class

MINIMAL EINSTEIN-CARTAN TORSION
no external stand-off

DECLARED 032R P-FORM DOMAIN
closed

HOPF GLOBAL SCALING
mechanism knowledge only without viable portal

MINIMAL TESTED ASYMMETRON BUBBLE
no required external sign

WEAK GW / MEMORY / PULSING
does not remove pure-GR 1/G burden

ORDINARY ELECTRON 032 SOURCE
energy closed

CONTROLLED NR STONER SOURCE
closed

FLAVOR MULTIPLICITY ENERGY SHORTCUT
closed

NAIVE OBLATE-TO-SPHERE MICROSTATE REUSE
closed.
```

---

# 131. Historical controls

Import and preserve important historical results such as:

```text
006D

B7

031 prescribed-source ~82.75 GJ

031 Q-ball ~273 GJ

031 optimized ~103 GJ

031 optimized ~96.141 GJ

031 activated higher-energy states

031F0 naturalness failure

V13–V18 partial oracles and rejections.
```

Use labels:

```text
HISTORICAL_CONTROL

NOT_NEW_DISCOVERY.
```

---

# 132. AGMINER report philosophy

Reports should answer three different questions.

## Discovery report

```text
WHAT LOOKS PROMISING?
```

## Failure report

```text
WHY ARE CANDIDATES DYING?
```

## Mechanism report

```text
WHAT PHYSICAL EFFICIENCY LEVER IS WORKING OR FAILING?
```

Do not merge these into one ranking.

---

# 133. Action-oracle report

`oracle_learning.csv` should allow quick inspection of:

```text
ACTION

ORACLE TYPE

ENERGY

LEDGER CLASS

NORMALIZATION STATUS

PORTAL STATUS

FINITE PAYLOAD STATUS

REALIZATION GAP

TRUST.
```

---

# 134. Mechanism-frontier report

Only include sufficiently physical candidates.

Columns should emphasize:

```text
COMPLETE OR NEAR-COMPLETE ENERGY

CHARGE / RESPONSE PER JOULE

PARTICIPATION

KERNEL LEVERAGE

CANCELLATION

SCAFFOLD TAX

STABILITY MARGIN

NATURALNESS MARGIN

PAYLOAD MARGIN.
```

An empty file is preferable to false promotion.

---

# 135. Automatic near-miss analysis

Report useful near misses such as:

```text
LOWEST-ENERGY SUPPORT FAILURE

LOWEST-ENERGY RG FAILURE

LOWEST-ENERGY STABILITY FAILURE

LOWEST-ENERGY EMPIRICAL FAILURE

BEST COMPLETE ENERGY ABOVE 10 MJ

BEST ACTION ORACLE WITH LARGE REALIZATION GAP.
```

These point directly toward the next theoretical bottleneck.

---

# 136. Current next-session execution order

The AGMINER build itself is no longer the task.

Do **not** restart the original infrastructure milestone list.

Current sequence:

```text
1.
VERIFY CURRENT FULL REGRESSION

2.
PRESERVE CURRENT DATABASE / FAILURE MEMORY

3.
PRESERVE V17 AND V18 AS PARTIAL ORACLES

4.
DO NOT PROMOTE THEM TO SURVIVORS

5.
EXECUTE V19 SUPPORT / UV / EMPIRICAL KILL GATE

6.
CONSTRUCT EXPLICIT SPHERICAL SUPPORT ACTION

7.
CHARGE FULL WALL ENERGY

8.
TEST RADIAL / SHAPE STABILITY

9.
COMPUTE OR BOUND RENORMALIZED AXIAL VACUUM

10.
RG / UV MATCH C1 AND fPsi

11.
TEST COMPANION OPERATORS

12.
RUN EARLY EMPIRICAL FALSIFICATION

13.
RECOMPUTE FINITE PAYLOAD IF SOURCE CHANGES

14.
UPDATE AGMINER FAILURE / ORACLE MEMORY

15.
IF V18 SURVIVES:
    CONTINUE COUPLED CERTIFICATION

16.
IF V18 FAILS BUT A PHYSICAL ANISOTROPIC SUPPORT EXISTS:
    RETURN TO V17 OBLATE FRONTIER

17.
IF KINETIC-CONFORMAL CLASS FAILS FUNDAMENTALLY:
    GLOBAL AGMINER RERANK

18.
ONLY THEN:
    RESUME BROAD DISCOVERY.
```

---

# 137. Current decision tree

```text
CURRENT V18 SPHERE
3.419 MJ PARTIAL
       |
       v
V19
SUPPORT + RG/UV + EMPIRICAL
       |
       +------------------- RED -------------------+
       |                                           |
       |                                           v
       |                                RECORD FAILURE ANATOMY
       |                                           |
       |                    +----------------------+----------------+
       |                    |                                       |
       |                    v                                       v
       |           V17 OBLATE FRONTIER                    GLOBAL AGMINER
       |           if physical anisotropic               RERANK
       |           support exists
       |
      GREEN
       |
       v
FULL COUPLED
SOURCE + SUPPORT + PAYLOAD
       |
       v
FULL STABILITY
       |
       v
ACTIVATION / OFF STATE
       |
       v
NONLINEAR METRIC
       |
       v
EMPIRICAL CLOSURE
       |
       v
COMPLETE OPERATING LEDGER
       |
       +---- >=10 MJ ----> FAIL CURRENT PRACTICAL POLICY
       |
       +---- <10 MJ -----> CERTIFICATION / REALIZATION FRONTIER
```

---

# 138. Current checkpoint

```text
DATE =
2026-09-06

AGMINER_STATUS =
ACTIVE_AND_OPERATIONAL

AGMINER_MODE =
CANDIDATE_SPECIFIC_FALSIFICATION

ENERGY_POLICY_ID =
ENERGY_ab8c16e45c837ffc

ENERGY_TARGET =
E_CONSERVATIVE_COMPLETE_OPERATING < 10 MJ

EXACT_10_MJ =
REJECT

HISTORICAL_REGRESSION_BASELINE =
94_PASSED

CURRENT_FULL_REGRESSION =
238_PASSED

MODEL_COUNT =
~101050

REJECTION_COUNT =
~95600

ACTION_ORACLE_COUNT =
8

COLLECTIVE_SCALING_COUNT =
2

MECHANISM_METRIC_COUNT =
0

MECHANISM_PARETO_COUNT =
0

CERTIFIED_SURVIVOR_COUNT =
0

CURRENT_ACTIVE_CLASS =
SHIFT_SYMMETRIC_KINETIC_CONFORMAL_UNIVERSAL_METRIC

CURRENT_SOURCE =
ZERO_NET_HIDDEN_FERMION_AXIAL_DERIVATIVE_SOURCE

V17_OBLATE_PARTIAL =
~59.419738_KJ

V17_SUPPORT =
OPEN_ANISOTROPIC

V17_FIXED_ORDER_RG =
RED

V18_SPHERE_PARTIAL =
~3.419157493_MJ

V18_SUPPORT_FLOOR =
~0.836832_MJ

V18_PHYSICAL_BAG =
NO

V18_FIXED_ORDER_RG =
RED

OUTWARD_SIGN_UNIVERSAL_UV_COMPLETION =
OPEN

RENORMALIZED_AXIAL_VACUUM =
OPEN

FULL_SOURCE_PAYLOAD_SUPPORT_COUPLING =
OPEN

NONLINEAR_STABILITY =
OPEN

ACTIVATION =
OPEN

EMPIRICAL_CLOSURE =
OPEN

COMPLETE_SUB10MJ_MODEL =
NO

PHYSICAL_ANTIGRAVITY_MODEL =
NO

PRACTICAL_DEVICE =
NO

NEXT =
032V19_SPHERICAL_BAG_SUPPORT_UV_MATCHING_AND_EMPIRICAL_GATE
```

---

# 139. Primary AGMINER claim

The primary AGMINER claim is now:

> **AGMINER is a reproducible, failure-aware, multi-fidelity physics discovery and falsification system that combines analytical no-go tests, canonical normalization, action-specific efficiency oracles, mechanism learning, finite-payload observables, microscopic source realization, persistent rejection memory, and progressively stronger physical gates to identify antigravity candidates worthy of certification under a strict complete operating-energy objective.**

It does not claim:

```text
ANTIGRAVITY DISCOVERED.
```

---

# 140. Major architecture principle

Permanent design rule:

> **Store physical knowledge, not merely candidate outcomes.**

The most useful AGMINER database entry may be:

```text
THIS SOURCE CANNOT EXIST
```

or:

```text
THIS APPARENT COUPLING IS A NORMALIZATION ARTIFACT
```

or:

```text
THIS COLLECTIVE RESPONSE SCALES NO FASTER THAN ITS SCAFFOLD
```

rather than a low-energy candidate.

---

# 141. Major scientific principle

Permanent rule:

> **Optimize the missing physical bottleneck, not the prettiest partial coefficient.**

Examples:

```text
WHEN ENERGY WAS THE BOTTLENECK:
OPTIMIZE ENERGY

WHEN SOURCE EXISTENCE WAS THE BOTTLENECK:
PROVE SOURCE EXISTENCE

WHEN SUPPORT IS THE BOTTLENECK:
BUILD SUPPORT

WHEN RG IS THE BOTTLENECK:
DO RG

WHEN EMPIRICAL CONSISTENCY IS THE BOTTLENECK:
TEST EMPIRICAL CONSISTENCY.
```

This prevents endless optimization of already-solved subproblems.

---

# 142. What AGMINER has learned so far

Permanent high-level lessons:

```text
1.
RAW COUPLING SIZE IS NOT PHYSICAL EFFICIENCY

2.
CANONICAL NORMALIZATION MUST COME EARLY

3.
RESPONSE SCALING WITHOUT SOURCE SCALING IS MISLEADING

4.
COLLECTIVE RESPONSE MUST OUTRUN COMPLETE ENERGY

5.
TOPOLOGICAL CHARGE IS NOT AUTOMATICALLY A METRIC-ACTIVE CHARGE

6.
A STATIC SOURCE MAY BE FORBIDDEN EVEN WHEN THE FIELD SIGN IS GOOD

7.
ZERO-NET MULTIPOLES CAN EVADE MONOPOLE NO-GOES

8.
A MICROSCOPIC SOURCE CAN FAIL ITS OWN EFT AFTER SELF-CONSISTENCY

9.
MORE FLAVORS DO NOT AUTOMATICALLY SAVE ENERGY

10.
FINITE PAYLOAD BACKREACTION CREATES REAL OPTIMA

11.
SUPPORT GEOMETRY CAN CHANGE MICROSCOPIC SELF-CONSISTENCY

12.
FIXED-ORDER RG FAILURE IS NOT AUTOMATICALLY A DEVICE-ENERGY PENALTY

13.
A LOW PARTIAL ORACLE IS NOT A COMPLETE MODEL

14.
FAILURE MEMORY SHOULD STORE THE PHYSICAL REASON

15.
BROAD SEARCH SHOULD STOP WHEN ONE CLASS BECOMES CLEARLY MORE INFORMATIVE.
```

---

# 143. Final operating philosophy

The old AGMINER philosophy was:

```text
SEARCH MANY

FALSIFY EARLY

REMEMBER FAILURES

SHORTLIST THE BEST.
```

That remains correct.

The mature philosophy is now:

```text
UNDERSTAND THE THEORY

        ↓

CANONICALIZE THE PHYSICS

        ↓

DERIVE THE CHEAPEST DECISIVE THEOREM

        ↓

BUILD ACTION-SPECIFIC ORACLES

        ↓

IDENTIFY THE ACTUAL EFFICIENCY MECHANISM

        ↓

SEARCH ONLY PHYSICALLY INDEPENDENT PARAMETERS

        ↓

FALSIFY SOURCE EXISTENCE / SIGN / SCALING

        ↓

REALIZE A MICROSCOPIC SOURCE

        ↓

TEST THE ACTUAL FINITE PAYLOAD

        ↓

CHARGE SUPPORT AND REACTION

        ↓

TEST QUANTUM / RG / UV CONTROL

        ↓

TEST STABILITY AND EMPIRICAL CONSISTENCY

        ↓

ONLY THEN ASK WHETHER THE COMPLETE ENERGY IS <10 MJ

        ↓

CERTIFY ONLY THE SURVIVORS.
```

---

# 144. Final rule

Carry this into every AGMINER session:

> **The miner does not exist to produce low numbers. It exists to identify physically meaningful routes to antigravity and to destroy false ones as efficiently and permanently as possible.**

And:

> **A candidate becomes more interesting as more complete physics fails to kill it—not merely as its partial energy becomes smaller.**

---

# 145. Final next state

```text
AGMINER_INFRASTRUCTURE =
BUILT_AND_OPERATIONAL

AGMINER_V6_MECHANISM_REDESIGN =
COMPLETE

GENERIC_BROAD_MINING =
NOT_CURRENT_PRIORITY

CURRENT_MODE =
CANDIDATE_SPECIFIC_FALSIFICATION

CURRENT_ACTIVE_MODEL_CLASS =
KINETIC_CONFORMAL_UNIVERSAL_METRIC
+
HIDDEN_AXIAL_DERIVATIVE_SOURCE

CURRENT_ENERGY_LEADER =
V17_OBLATE_59P419738_KJ_PARTIAL

CURRENT_SUPPORT_REALIZATION_LEADER =
V18_SPHERE_3P419157493_MJ_PARTIAL

CURRENT_CERTIFIED_SURVIVORS =
0

NEXT =
032V19_SPHERICAL_BAG_SUPPORT_UV_MATCHING_AND_EMPIRICAL_GATE
```

---

## END AGMINER BUILD PLAN
