# Antigravity Research — Research Buildplan

This document is the active scientific execution plan for **Antigravity Research**.

Its purpose is to maximize scientific information gain per unit research time while moving the project as efficiently as possible toward the strongest physically defensible form of practical antigravity-like acceleration.

This is a living execution plan.

Update it when:

* a major analytical or numerical gate is completed;
* a major branch is falsified;
* a new physical constraint changes the ranking;
* a substantially better mechanism is identified;
* the active scientific frontier changes;
* a speculative mechanism becomes concrete enough to require a higher verification standard.

Chronological detail belongs in `NOTES.md`.

Durable completed research slices belong in `journal/`.

The README should remain a concise public-facing statement of the strongest established results and current frontier.

This buildplan should remain focused on:

```text
CURRENT_FRONTIER
CURRENT_PROGRESS
ACTIVE_SCIENTIFIC_QUESTION
ACTIVE_TASK
PRIMARY_OBSERVABLE
DECISION_GATES
PATHWAY_RANKING
STOP_RULES
METHOD_REFINEMENT
CLAIM_PROMOTION_REQUIREMENTS
NEXT
```

---

# 1. Central Objective

The central project question is:

> **What physically consistent mechanism offers the shortest credible path from demonstrated local repulsion to stable, finite-payload, experimentally accessible, energetically useful antigravity-like acceleration?**

The project is no longer primarily asking whether equations can contain a repulsive sign.

That question has been answered in several established examples and constructively in the project-derived 006D source.

The research program must now optimize for simultaneous progress in:

```text
OPERATIONAL_REPULSION
THEORY_CONSISTENCY
FINITE_LOCALIZATION
CONSERVATION
STABILITY
MICROPHYSICAL_REALIZATION
FINITE_PAYLOAD_RESPONSE
ENERGY_EFFICIENCY
EMPIRICAL_VIABILITY
CONTROL
EXPERIMENTAL_ACCESSIBILITY
```

These levels must never be conflated.

A mathematically valid repulsive source is not automatically realizable.

A realizable field is not automatically stable.

A stable local field does not automatically lift a finite body.

Finite-payload lift does not automatically imply practical energy requirements.

Practical energy requirements do not automatically imply an experimentally buildable device.

---

# 2. Current Informal Progress

The current project-management estimate is:

```text
CURRENT_INFORMAL_PROJECT_PROGRESS_HEURISTIC=
APPROXIMATELY_44_PERCENT
```

This is **not a probability that practical antigravity exists**.

It is an informal success-ladder measure.

The project has already established or strongly characterized:

```text
MATHEMATICAL_REPULSIVE_SIGN=
SOLVED

EXPLICIT_FINITE_POSITIVE_ENERGY_REPULSIVE_GR_SOURCE=
SOLVED_IN_STATIC_LINEARIZED_GR

NEC_WEC_DEC_COMPATIBILITY=
SOLVED_FOR_006D

LOCAL_CONSERVATION=
SOLVED_AT_LINEARIZED_BACKGROUND_ORDER

POSITIVE_FAR_FIELD_ACTIVE_MASS=
SOLVED_FOR_006D

FINITE_THICKNESS=
SOLVED

PEAK_STRESS_VS_THICKNESS_TRADEOFF=
CHARACTERIZED

ONE_MODE_FIXED_CHARGE_STABILITY_CAPACITY=
ESTABLISHED_AS_CAPACITY

GAUGE_WINDING_REALIZATION_CONSTRAINTS=
SUBSTANTIALLY_CHARACTERIZED

MINIMAL_CANONICAL_EXACT_TARGET_FAILURE=
UNDERSTOOD

GENERIC_COSPATIALLY_LOCALIZED_FIELD_FAILURE=
DEMONSTRATED_IN_TESTED_VARIATIONAL_FAMILY
```

The major unresolved steps are:

```text
ACTUAL_FIELD_EULER_LAGRANGE_SOLUTION=
NOT_ESTABLISHED

FULL_DYNAMIC_STABILITY=
NOT_ESTABLISHED

NONLINEAR_EINSTEIN_MATTER_REALIZATION=
NOT_ESTABLISHED

FINITE_PAYLOAD_OUTWARD_ACCELERATION=
NOT_ESTABLISHED

PRACTICAL_ENERGY_SCALING=
NOT_ESTABLISHED

EXPERIMENTAL_ACCESSIBILITY=
NOT_ESTABLISHED

PRACTICAL_DEVICE=
NO
```

A reduction in the heuristic after a strong falsification result is not scientific regression.

The objective is uncertainty reduction, not preserving a percentage.

---

# 3. Two Mechanism Classes

The project contains two fundamentally different kinds of antigravity-like mechanisms.

## 3.1 Metric / gravitational mechanisms

These produce repulsion through spacetime geometry and stress-energy.

Examples include:

* Kottler / Schwarzschild-de Sitter;
* Reissner-Nordström gravitational repulsion;
* relativistic pressure and tension;
* 006D;
* quantum stress-energy;
* modified-gravity geometries.

For these branches the observable must ultimately be gravitational or geometric.

Examples:

* relative free-fall acceleration;
* proper acceleration;
* geodesic deviation;
* curvature;
* finite-body gravitational acceleration.

## 3.2 Additional-force mechanisms

These generate antigravity-like acceleration through a force beyond ordinary GR.

Examples include:

* vector fifth forces;
* scalar fifth forces;
* disformal forces.

These mechanisms must not be described as ordinary GR antigravity.

Momentum conservation must remain explicit.

A ground-referenced force can accelerate a payload because the Earth or another external source supplies the reaction momentum.

That is not reactionless propulsion.

---

# 4. Operational Target

The ultimate target is not a sign in a field equation.

The operational target is useful outward acceleration of a finite neutral payload.

For a payload with mass density $\rho_P(\mathbf x)$ and total mass $M_P$,

```math
M_P
=
\int
\rho_P(\mathbf x)
\,d^3x
```

define its center-of-mass acceleration by

```math
\mathbf a_{\mathrm{CM}}
=
\frac{
1
}{
M_P
}
\int
\rho_P(\mathbf x)
\mathbf a(\mathbf x)
\,d^3x
```

The primary vertical observable is

```math
a_{\mathrm{CM},z}
```

with convention:

```text
a_CM,z > 0 =
OUTWARD / UPWARD

a_CM,z < 0 =
INWARD / DOWNWARD
```

The principal practical benchmark remains approximately

```math
a_{\mathrm{target}}
\sim
g
```

where

```math
g
=
9.80665\ {\rm m\,s^{-2}}
```

A pointwise acceleration may still be used in inexpensive prerequisite gates.

However, **a branch may not be promoted toward practical relevance based only on a pointwise sign once a finite-payload calculation is computationally affordable**.

This requirement is now permanent because 015C demonstrated that local reversed-force regions need not produce finite-body center-of-mass reversal.

---

# 5. Payload-Weighted Gravitational Kernel

For static linearized GR define

```math
S(\mathbf x)
=
\epsilon
+
p_x
+
p_y
+
p_z
```

or the corresponding principal-pressure expression in the local orthonormal basis.

The vertical acceleration of a point target can be written schematically as

```math
a_z
=
-\frac{G}{c^2}
\int
S(\mathbf x')
K(\mathbf x,\mathbf x')
\,d^3x'
```

For a finite payload define a payload-averaged kernel

```math
\overline{K}_P(\mathbf x')
=
\frac{
1
}{
M_P
}
\int
\rho_P(\mathbf x)
\frac{
z-z'
}{
|\mathbf x-\mathbf x'|^3
}
\,d^3x
```

Then

```math
\boxed{
a_{\mathrm{CM},z}
=
-\frac{G}{c^2}
\int
S(\mathbf x')
\overline{K}_P(\mathbf x')
\,d^3x'
}
```

This is the preferred operational quantity for future GR source optimization.

A point target is a limiting special case.

---

# 6. New Kernel-Leverage Design Principle

Write the active source as

```math
S
=
S_+
-
S_-
```

where

```math
S_+
=
\max(S,0)
```

and

```math
S_-
=
\max(-S,0)
```

so both $S_+$ and $S_-$ are nonnegative.

Define integrated magnitudes:

```math
Q_+
=
\int
S_+
\,dV
```

and

```math
Q_-
=
\int
S_-
\,dV
```

Positive total active mass requires

```math
Q_+
>
Q_-
```

Define average payload-kernel leverage factors:

```math
\kappa_+
=
\frac{
\int
\overline{K}_P
S_+
\,dV
}{
Q_+
}
```

and

```math
\kappa_-
=
\frac{
\int
\overline{K}_P
S_-
\,dV
}{
Q_-
}
```

Outward finite-payload acceleration requires

```math
\kappa_-Q_-
>
\kappa_+Q_+
```

Therefore the necessary leverage condition is

```math
\boxed{
\frac{
\kappa_-
}{
\kappa_+
}
>
\frac{
Q_+
}{
Q_-
}
}
```

This equation should guide the next established-GR source design.

It expresses the central lesson from 006D versus 016H:

> **The negative active source must be placed where gravitational leverage is greater than the leverage experienced by the compensating positive source.**

Future optimization should track this ratio explicitly.

---

# 7. Unified Success Ladder

All candidate mechanisms should be classified using the same ladder.

## Level 0 — Mathematical sign

A repulsive term or sign exists.

## Level 1 — Local operational repulsion

A measurable physical quantity points outward locally.

## Level 2 — Governing-theory consistency

The configuration satisfies the equations of the theory being claimed.

## Level 3 — Complete source / charge characterization

The source, charge, stress, couplings, and signs are specified.

## Level 4 — Finite localization

The source and relevant payload are finite.

## Level 5 — Conservation

Relevant conservation laws are satisfied.

For GR matter:

```math
\nabla_\mu T^{\mu\nu}=0
```

For fifth-force theories this also includes:

* total momentum;
* energy;
* source charge;
* test charge;
* backreaction.

## Level 6 — Stability / naturalness

The mechanism survives all important mechanical, field-theoretic, thermal, quantum, and radiative instabilities.

## Level 7 — Microscopic physical realization

A controlled field or material mechanism generates the needed source.

## Level 8 — Finite-payload operational repulsion

A finite payload has

```math
a_{\mathrm{CM},z}>0
```

under complete source/payload integration.

## Level 9 — Empirical viability

Existing laboratory, astrophysical, and cosmological bounds are satisfied.

## Level 10 — Practical scaling and control

The required energy, fields, stresses, heat load, and control system are physically plausible.

## Level 11 — Experimental demonstration

A reproducible experiment detects the effect with controlled systematics.

## Level 12 — Practical antigravity

A stable, controllable apparatus produces useful macroscopic outward acceleration.

The project is not currently at Level 12.

---

# 8. Regression Integrity Gate

Before extending any major scientific branch:

```text
EXPECTED_KNOWN_SOLUTION_BASELINE=
94_PASSED
```

Run:

```bash
git status --short

ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"

PYTHONPATH="$ROOT/src" \
"$PY" -m pytest -q tests/known_solutions
```

If the expected baseline fails:

```text
NEW_SCIENTIFIC_CLAIMS=
PAUSE
```

until the regression is understood.

If permanent tests are deliberately added, update the expected count.

Do not use test count alone as scientific verification.

---

# 9. Strongest Established Result — 006D

The strongest established project-derived result remains 006D.

The explicit finite source is:

```text
FINITE_RADIUS=
YES

FINITE_THICKNESS=
YES

NONSINGULAR=
YES

POSITIVE_ENERGY=
YES

LOCAL_CONSERVATION_LINEARIZED_ORDER=
YES

NEC=
PASS

WEC=
PASS

DEC=
PASS

LOCAL_OUTWARD_FIELD=
YES

POSITIVE_FAR_FIELD_ACTIVE_MASS=
YES
```

The best tested finite coefficient is

```math
C_{\mathrm{finite}}
=
23.591586299249
```

in

```math
M_{\mathrm{equiv}}
=
C\frac{ah^2}{G}
```

The thin conserved reference is

```math
C_{\mathrm{thin}}
=
23.426710175391
```

The finite source is therefore approximately $0.704%$ above the thin result.

The central project headline remains:

> **We have a mathematical construction for antigravity-like gravitational repulsion.**

Correct limitations:

```text
EXACT_NONLINEAR_GR=
NOT_ESTABLISHED

FULL_DYNAMIC_STABILITY=
NOT_ESTABLISHED

KNOWN_MATERIAL_REALIZATION=
NO

FINITE_PAYLOAD_LIFT=
NOT_ESTABLISHED

ENERGETIC_PRACTICALITY=
NO

PRACTICAL_ANTIGRAVITY=
NO

NEW_PHYSICS_DISCOVERY=
NO
```

For complete reconstruction see:

```text
journal/2026-08-28_006d_constructive_linearized_gr_repulsion.md
```

---

# 10. 016A–016H Frontier Update

The return to the 006D branch materially changed the project ranking.

## 016A — thickness optimization

The mathematically thinnest source was shown not to be the best physical realization target.

At approximately

```text
DELTA=
0.10_TO_0.20
```

peak stresses were reduced by hundreds-fold while the gravitational coefficient increased only by an order-unity amount.

016A also established the tiled-area scaling

```math
\boxed{
\frac{
E
}{
A
}
=
\frac{
Cac^2
}{
\pi x_{\max}^2G
}
}
```

for the simple cell-coverage architecture.

The stand-off scale $h$ cancels.

Thus simple miniaturization does not solve the macroscopic energy problem.

## 016B — thick charge/gauge capacity

The fixed-charge Derrick capacity and local gauge budget survived thickening.

## 016C — electrostatic global integrability

The simplest exact two-potential electrostatic realization was rejected by the necessary conformal condition

```math
\Delta\ln g=0
```

which the tested target violates.

## 016D — smooth exponential target

A smooth noncompact tail retained outward gravity, stress balance, and fixed-charge capacity.

## 016E — asymptotic gauge-energy gate

The exponential tail was rejected for the minimal gauged-winding realization because the required gauge mismatch produces logarithmically divergent asymptotic magnetic energy.

A $C^2$ power-law tail was promoted kinematically.

## 016F — simultaneous charge/winding coexistence

A hidden competition between temporal charge and winding support was exposed.

Broadening the inner transition reduced the required mismatch from approximately

```text
K_REQUIRED≈130
```

to

```text
K_REQUIRED≈9.59
```

with a conservative winding target

```text
N≈10
```

while retaining approximately

```text
1400x
```

peak-stress relief relative to the original fine 006D source.

## 016G — canonical asymptotic no-go

The exact promoted power-law target was rejected for the minimum asymptotically decoupled canonical winding field.

The central identity is

```math
\boxed{
k_\infty^2-s^2
=
\frac{
m(m+2)
}{
4(1-\eta)
}
>0
}
```

under the stated assumptions.

This forces the wrong asymptotic self-potential sign for a regular stable decoupled vacuum.

## 016H — explicit field model

An explicit positive-energy FLS-like counter-winding variational family generated substantial negative active density.

Across

```text
63
```

bound internally consistent configurations:

```text
NEGATIVE_ACTIVE_DENSITY=
YES

MAX_NEGATIVE_ACTIVE_FRACTION_OVER_E≈
0.2666

NEAR_FIELD_REPULSION=
NOT_FOUND

CLEAN_EXTERIOR_REPULSION=
NOT_FOUND
```

Independent force quadrature retained the attractive sign.

This established the current design principle:

```text
NEGATIVE_ACTIVE_DENSITY_ALONE=
INSUFFICIENT

SPATIAL_ACTIVE_STRESS_SEGREGATION=
REQUIRED_DESIGN_VARIABLE
```

For full detail see:

```text
journal/2026-08-29_016a_016h_006d_realizability_and_canonical_field_gates.md
```

---

# 11. Current Frontier

The current frontier is no longer:

```text
CAN_THE_006D_STRESS_TENSOR_BE_EXACTLY_REPRODUCED
```

and it is no longer solely:

```text
CAN_THE_PROTECTED_DINUCLEAR_SCALAR_HAVE_A_UV_COMPLETION
```

The project now has a post-016H global reranking.

The leading established-GR question is:

> **Can an explicit healthy local field configuration spatially concentrate negative active stress in the high-leverage central region while moving the compensating positive support to a lower-leverage outer rim strongly enough to produce finite-payload outward acceleration?**

The competing practicality question remains:

> **If pure GR retains catastrophic energy scaling even after physical realization, can a technically natural stronger interaction reproduce the same operational effect at practical energy cost?**

These questions are linked but should not be attacked simultaneously in one model.

---

# 12. Current Pathway Ranking

The ranking reflects **expected information gain and probability of useful progress**, not certainty that the route will succeed.

## Priority 1 — 006D-inspired spatially separated drum/rim field realization

Status:

```text
ACTIVE
```

Reasons:

* based on established GR;
* anchored by the strongest positive project result;
* 016A–016F substantially reduced several realization problems;
* 016G/H identified specific failure mechanisms rather than generic uncertainty;
* the new spatial-segregation criterion gives a concrete design target;
* the next gates are cheap enough to be highly falsifiable.

Dominant weakness:

```text
PURE_GR_ENERGY_SCALING=
CATASTROPHIC
```

This branch is being pursued to determine whether a **real physical source** exists, not because current energy estimates are practical.

## Priority 2 — protected material-specific scalar fifth force

Status:

```text
PARKED_HIGH_VALUE_ALTERNATIVE
```

Reasons:

* low-energy parametric survivor exists;
* could use an interaction far stronger than gravity;
* therefore has much greater potential to solve the practical energy barrier;
* current dominant uncertainty is the relativistic microscopic protection mechanism.

Dominant weaknesses:

```text
RELATIVISTIC_UV_COMPLETION=
NOT_ESTABLISHED

ONE_BODY_LEAKAGE_PROTECTION=
NOT_ESTABLISHED

ULTRALIGHT_MASS_NATURALNESS=
NOT_ESTABLISHED
```

Reopen when:

* Priority 1 reaches a field-realization stop rule; or
* Priority 1 succeeds physically but the $ah^2/G$ scaling remains irreducible; or
* an independent theoretical insight materially changes the scalar UV problem.

## Priority 3 — 014D disformal finite-payload continuation

Status:

```text
PARKED_CONDITIONAL
```

Positive anchor:

```text
CONTROLLED_LOCAL_TOTAL_FORCE_REVERSAL=
YES
```

Dominant failures:

```text
SIMPLE_ORDINARY_MATTER_BRIDGE=
REJECTED

FINITE_PAYLOAD_REVERSAL=
NOT_ESTABLISHED
```

Highest-value reopen test:

```text
ORIGINAL_014D_GEOMETRY
+
FINITE_PAYLOAD_INTEGRATION
```

followed, if justified, by a dynamic-time payload impulse test.

## Priority 4 — established quantum stress-energy

Status:

```text
REFERENCE_CONSTRAINT_BRANCH
```

No practical macroscopic escape was found in the tested established-QFT route.

## Priority 5 — exact Einstein-Maxwell repulsion

Status:

```text
REFERENCE_SOLUTION
```

Established physically, but catastrophic electric-field requirements prevent current practical relevance.

## Priority 6 — other modified-gravity / fifth-force models

Status:

```text
DEFERRED_UNLESS_NEW_PHYSICAL_PRINCIPLE_APPEARS
```

Do not open large speculative model spaces merely because the active branch becomes difficult.

---

# 13. Active Scientific Question

The single active scientific question is:

> **What is the minimum spatial segregation of negative and positive active stress required for a finite payload to experience outward acceleration, and can a healthy localized field configuration naturally achieve that segregation while remaining approximately stationary and positive in total mass?**

This question deliberately has two stages.

First determine the **geometry requirement**.

Then test an actual field model against that requirement.

Do not reverse this order.

---

# 14. Active Phase

```text
ACTIVE_PHASE=
016I_FINITE_PAYLOAD_KERNEL_LEVERAGE_ENVELOPE
```

The purpose of 016I is not to discover another arbitrary stress tensor.

It is to quantify exactly how much spatial segregation the next field model must achieve.

This is the cheapest decisive step after 016H.

---

# 15. 016I — Finite-Payload Kernel-Leverage Envelope

## Scientific question

For a central negative-active "drum" and outer positive-active "rim", what combinations of:

```text
NEGATIVE_ACTIVE_MAGNITUDE
POSITIVE_ACTIVE_MAGNITUDE
DRUM_RADIUS
DRUM_THICKNESS
RIM_RADIUS
RIM_WIDTH
PAYLOAD_RADIUS
PAYLOAD_HEIGHT
PAYLOAD_THICKNESS
```

permit:

```math
\int S\,dV>0
```

while simultaneously giving:

```math
a_{\mathrm{CM},z}>0
```

for a finite payload?

## Model level

016I is a **geometry/observable prerequisite**, not a matter-field claim.

Use smooth finite source profiles.

Do not optimize arbitrary pixel values.

Use low-dimensional shapes that can later map onto plausible field sectors.

Recommended architecture:

```text
CENTRAL_NEGATIVE_ACTIVE_DRUM
+
OUTER_POSITIVE_ACTIVE_ANNULAR_RIM
```

The negative and positive components should each have explicitly normalized smooth profiles.

## Required primary outputs

```text
TOTAL_ACTIVE_MASS

NEGATIVE_ACTIVE_MAGNITUDE_Q_MINUS

POSITIVE_ACTIVE_MAGNITUDE_Q_PLUS

KAPPA_MINUS

KAPPA_PLUS

KERNEL_LEVERAGE_RATIO=
KAPPA_MINUS/KAPPA_PLUS

REQUIRED_LEVERAGE_RATIO=
Q_PLUS/Q_MINUS

POINT_TARGET_ACCELERATION

FINITE_PAYLOAD_CM_ACCELERATION

REPULSIVE_PAYLOAD_FRACTION

PAYLOAD_ACCELERATION_UNIFORMITY
```

## Primary pass condition

Find a **finite region of parameter space**, not a single tuned point, satisfying:

```math
Q_+>Q_-
```

and:

```math
a_{\mathrm{CM},z}>0
```

with:

```math
\frac{
\kappa_-
}{
\kappa_+
}
>
\frac{
Q_+
}{
Q_-
}
```

by a meaningful margin.

## Strong pass condition

The required negative-active fraction is no more demanding than magnitudes already demonstrated in physically motivated field preflights such as 016H.

This does not prove realizability.

It establishes that the spatial-segregation requirement is numerically plausible enough to justify a field model.

## Fail condition

If finite-payload reversal requires:

* nearly cancelling total active mass;
* pathological geometric separation;
* vanishingly small payload dimensions;
* negative-active fractions far beyond anything available in healthy field models;
* extreme fine tuning;

then:

```text
DRUM_RIM_CANONICAL_REALIZATION=
STRONGLY_DEMOTED
```

before writing another complicated field model.

---

# 16. 016I Method Requirements

Use two independent evaluation routes.

Preferred:

```text
METHOD_A=
DIRECT_AXISYMMETRIC_VOLUME_QUADRATURE

METHOD_B=
INDEPENDENT_MONTE_CARLO_OR_SEPARATE_HIGH_ORDER_QUADRATURE
```

Central sign decisions must agree.

Perform:

```text
GRID_OR_QUADRATURE_REFINEMENT

DOMAIN_SIZE_CHECK

PAYLOAD_GEOMETRY_PERTURBATION

SOURCE_GEOMETRY_PERTURBATION
```

A single isolated positive point is not sufficient.

Require a robust neighborhood.

The output should include a Pareto frontier between:

```text
FINITE_PAYLOAD_ACCELERATION

POSITIVE_TOTAL_ACTIVE_MASS_MARGIN

NEGATIVE_ACTIVE_FRACTION

GEOMETRIC_SEPARATION

SOURCE_SIZE
```

Do not collapse these into one arbitrary weighted objective too early.

---

# 17. 016J — Explicit Spatially Separated Field Variational Gate

Only run 016J if 016I identifies a plausible leverage region.

Suggested field content:

```text
SECTOR_X=
REAL_SYMMETRY_BREAKING_FIELD_FORMING_CENTRAL_DRUM_OR_WALL

SECTOR_QW=
COUNTER_WINDING_CHARGED_COMPLEX_PAIR_CONCENTRATED_TOWARD_OUTER_RIM

OPTIONAL_GAUGE_SECTOR=
DEFERRED_OR_INCLUDED_ONLY_IF_REQUIRED_BY_THE_SELECTED_FIELD_ANSATZ
```

The first field preflight should use the **minimum field content capable of expressing the geometry identified by 016I**.

Do not add fields because they improve the optimizer.

Every field must have a physical role.

---

# 18. 016J Primary Objective

Do not minimize distance to the 006D stress tensor.

Optimize the physical observables.

Primary requirement:

```math
a_{\mathrm{CM},z}>0
```

for a finite payload.

Secondary requirements:

```text
LOCALIZED_FIELDS=
YES

FINITE_TOTAL_ENERGY=
YES

BOUND_STATE_OR_STATIONARY_VARIATIONAL_STATE=
YES

POSITIVE_TOTAL_ACTIVE_MASS=
YES

NET_T_TPHI≈0

NO_PATHOLOGICAL_PARAMETER_LIMITS=
YES
```

The optimizer should also report the point-target result, but finite-payload acceleration is the promotion variable.

---

# 19. Energy-Efficiency Metric

Every future positive GR configuration should report an effective mass-equivalent cost

```math
M_E
=
\frac{E}{c^2}
```

and define

```math
C_{\mathrm{eff,payload}}
=
\frac{
G M_E
}{
a_{\mathrm{CM},z}h^2
}
```

when

```math
a_{\mathrm{CM},z}>0
```

where $h$ is a clearly defined characteristic source-payload separation.

Lower is better.

Equivalent efficiency may be written

```math
\mathcal R_{\mathrm{payload}}
=
\frac{
a_{\mathrm{CM},z}h^2
}{
GM_E
}
=
\frac{
1
}{
C_{\mathrm{eff,payload}}
}
```

This metric should not replace dimensional engineering metrics, but it provides a consistent comparison across GR architectures.

Future runs should report both:

```text
DOES_IT_REPEL?

HOW_MUCH_OUTWARD_ACCELERATION_PER_UNIT_SOURCE_ENERGY?
```

A sign-only improvement with dramatically worse efficiency should not automatically be treated as progress toward a device.

---

# 20. 016J Pass Conditions

A strong 016J result requires:

```text
FINITE_TOTAL_ENERGY=
YES

BOUND_OR_VARIATIONALLY_STATIONARY=
YES

POSITIVE_TOTAL_ACTIVE_MASS=
YES

NEGATIVE_ACTIVE_REGION=
YES

SPATIAL_SEGREGATION_METRIC=
PASS

POINT_OUTWARD_ACCELERATION=
YES

FINITE_PAYLOAD_CM_OUTWARD_ACCELERATION=
YES

RESULT_PERSISTS_UNDER_PARAMETER_PERTURBATION=
YES

INDEPENDENT_FORCE_RECONSTRUCTION=
PASS
```

A particularly important output is:

```text
FIELD_MODEL_ACHIEVED_KERNEL_LEVERAGE_RATIO
```

compared directly against the 016I requirement.

---

# 21. 016J Stop Rule

If a sufficiently flexible but physically motivated separated variational field family cannot generate finite-payload outward acceleration without:

* extreme parameter boundaries;
* huge cancellation;
* loss of localization;
* unbounded energy;
* obvious instability;
* pathological potentials;

then:

```text
GENERIC_CANONICAL_006D_MATTER_REALIZATION=
DEPRIORITIZED
```

Do **not** automatically escalate to a large nonlinear PDE solver.

Perform the global rerank.

---

# 22. 016K — Independent Reconstruction Gate

If 016J is green, do not immediately promote it.

First independently reconstruct the result.

Use:

```text
INDEPENDENT_FIELD_AND_STRESS_IMPLEMENTATION

INDEPENDENT_GRAVITATIONAL_FORCE_INTEGRATOR

HIGHER_ORDER_QUADRATURE

PARAMETER_NEIGHBORHOOD_SCAN

PAYLOAD_GEOMETRY_VARIATION
```

Required:

```text
FORCE_SIGN=
REPRODUCED

ENERGY=
REPRODUCED

ACTIVE_MASS=
REPRODUCED

KERNEL_LEVERAGE=
REPRODUCED

FINITE_PAYLOAD_RESULT=
REPRODUCED
```

Only then proceed to a full field-equation solve.

---

# 23. 016L — Full Euler-Lagrange Boundary-Value Solve

If 016J/K survive, solve the actual coupled field equations.

This is the first point where a large PDE solve becomes justified.

Required convergence studies:

```text
RADIAL_RESOLUTION

VERTICAL_RESOLUTION

DOMAIN_SIZE

BOUNDARY_LOCATION

INITIAL_GUESS

CONTINUATION_PATH

SOLVER_TOLERANCE
```

Required outputs:

```text
PDE_RESIDUAL

TOTAL_ENERGY

NOETHER_CHARGE

GAUGE_CHARGE_IF_PRESENT

NET_ANGULAR_MOMENTUM

T_TPHI

ACTIVE_SOURCE

TOTAL_ACTIVE_MASS

KERNEL_LEVERAGE_RATIO

POINT_ACCELERATION

FINITE_PAYLOAD_ACCELERATION

BOUNDARY_DECAY
```

Pass condition:

> A globally regular finite-energy field configuration satisfying its own Euler-Lagrange equations produces robust outward finite-payload acceleration.

That would be a major project milestone.

---

# 24. 016M — Full Stability Gate

Only after a genuine field solution exists.

Required perturbation classes:

```text
RADIAL_DILATION

VERTICAL_TRANSLATION

WALL_RIM_RELATIVE_DISPLACEMENT

AZIMUTHAL_MODES

VORTEX_SPLITTING

CHARGE_TRANSFER

GAUGE_MODES

COLLAPSE_OR_EXPANSION

FIELD_AMPLITUDE_MODES
```

A fixed-charge Derrick mode alone is insufficient.

The preferred analysis is an eigenvalue problem for linear perturbations.

Pass condition:

```text
NO_RELEVANT_GROWING_MODE=
FOUND_WITHIN_DECLARED_MODEL_AND_RESOLUTION
```

If an instability exists, determine whether it is:

```text
FUNDAMENTAL

OR

REMOVABLE_BY_A_PHYSICALLY_MOTIVATED_EXISTING_SECTOR
```

Do not add arbitrary stabilizing sectors.

---

# 25. 016N — Nonlinear Einstein-Matter Continuation

Only after field realization and stability are green.

Solve:

```math
G_{\mu\nu}
=
\frac{
8\pi G
}{
c^4
}
T_{\mu\nu}
```

with the actual matter fields.

Required checks:

```text
METRIC_REGULARITY

CURVATURE_INVARIANTS

HORIZONS

COMPACTNESS

FULL_CURVED_STRESS_CONSERVATION

ASYMPTOTIC_MASS

PROPER_ACCELERATION

GEODESIC_RESPONSE

FINITE_PAYLOAD_RESPONSE
```

Low compactness in the old stress construction suggests nonlinear corrections may be small, but this must be demonstrated for the realized source.

---

# 26. 016O — Practical Scaling Gate

Even a successful 016L–N matter solution does not imply a practical device.

This gate asks:

> **Does the actual realized field architecture change the catastrophic pure-GR energy scaling by more than an order-unity coefficient?**

Current baseline:

```math
M
\sim
C\frac{ah^2}{G}
```

and for simple tiled coverage:

```math
\frac EA
\sim
\frac{
Cac^2
}{
\pi x_{\max}^2G
}
```

If the realized source merely changes $C$ from approximately $40$ to $10$, practical antigravity remains nowhere close energetically.

A practical-scale breakthrough requires a **qualitative scaling change**.

Examples of acceptable discoveries would include:

```text
COLLECTIVE_PAYLOAD_COUPLING_THAT_AVOIDS_SIMPLE_AREA_TILING

GEOMETRIC_KERNEL_LEVERAGE_CHANGING_THE_H_SCALING

AN_EXTERNAL_BACKGROUND_SUPPLYING_MOST_OF_THE_REQUIRED_STRESS

A_PHYSICALLY_ALLOWED_STRONGER_EFFECTIVE_INTERACTION

OTHER_DERIVED_SCALING_MECHANISM
```

Do not assume such a mechanism exists.

---

# 27. Trigger for Returning to the Protected Scalar Branch

If the GR field-realization program reaches either:

```text
FIELD_REALIZATION_STOP_RULE
```

or:

```text
FIELD_REALIZATION_SUCCESS_BUT_PRACTICAL_SCALING_FAILURE
```

then Priority 2 becomes active.

The active question becomes:

> **Can the protected two-body scalar response be generated by a technically natural relativistic microscopic theory while suppressing ordinary one-body scalar charge and preserving the ultralight mediator?**

Do not restart material optimization.

Resume at the UV-protection gate.

---

# 28. Protected Scalar Reference State

The surviving low-energy target remains schematically

```math
\mathcal H_{\phi,2}
=
C_\phi
\phi
A^\dagger
B^\dagger
BA
```

with representative

```math
C_\phi
\approx
9.54\times10^{-20}\ {\rm eV^{-3}}
```

for the selected normalization.

The conservative ordinary-matter leakage allowance is approximately

```math
f_{\mathrm{leak}}
\approx
5.77\times10^{-7}
```

of the target-equivalent activated response.

The working mediator mass is approximately

```math
m_\phi
\approx
3.95\times10^{-11}\ {\rm eV}
```

The branch remains:

```text
LOW_ENERGY_PARAMETRIC_SURVIVOR=
YES

RELATIVISTIC_MICROSCOPIC_COMPLETION=
NO
```

---

# 29. Protected Scalar Gate Sequence

When reactivated:

```text
A.
RELATIVISTIC_OPERATOR_BASIS

B.
EXACT_OR_TECHNICALLY_NATURAL_PROTECTION

C.
TREE_LEVEL_ONE_BODY_OPERATOR_CHECK

D.
ONE_LOOP_AND_RG_MIXING

E.
ULTRALIGHT_SCALAR_MASS_NATURALNESS

F.
INDEPENDENT_NR_MATCHING

G.
CURRENT_EXPERIMENTAL_FORCE_BOUND

H.
STELLAR_AND_COSMOLOGICAL_CONSTRAINTS

I.
REAL_MATERIAL_MATCH
```

Stop immediately if one-body leakage or scalar-mass instability is unavoidable.

Do not protect sunk effort with arbitrary hidden fields.

---

# 30. Disformal Reopen Rule

014D should not be rerun as a local sign test.

Its important positive result is already preserved.

If the disformal branch becomes active, the next test must be operational:

```text
ORIGINAL_014D_VALIDATED_SOURCE_GEOMETRY
+
FINITE_PAYLOAD_CENTER_OF_MASS_INTEGRATION
```

If justified after that:

```text
TIME_DEPENDENT_PAYLOAD_IMPULSE
```

The relevant quantity is

```math
\Delta v_{\mathrm{CM}}
=
\int
a_{\mathrm{CM}}(t)
\,dt
```

not merely a transient local reversed cell.

If the original validated geometry fails to produce meaningful finite-body reversal, demote the branch strongly.

---

# 31. Research Method Refinement — Impact-First Run Design

Every major future run should be designed in the following order.

## Step 1 — State one uncertainty

Do not begin with:

```text
LET_US_SCAN_PARAMETERS
```

Begin with:

```text
WHAT_SINGLE_UNKNOWN_CURRENTLY_BLOCKS_PROMOTION_OR_REJECTION?
```

## Step 2 — State the operational observable

For current GR work:

```text
PRIMARY=
FINITE_PAYLOAD_CM_ACCELERATION

SECONDARY=
SOURCE_ENERGY_EFFICIENCY

TERTIARY=
STABILITY_AND_CONSERVATION_MARGIN
```

## Step 3 — Derive the cheapest necessary condition

Before simulation, attempt:

```text
SIGN_THEOREM

BOUND

DIMENSIONAL_ARGUMENT

INTEGRABILITY_CONDITION

ASYMPTOTIC_CONDITION

VIRIAL_CONDITION

ENERGY_CONDITION_BOUND
```

If algebra kills the model, stop.

## Step 4 — Use the minimum numerical model

Only enough complexity to test the specific condition.

## Step 5 — Search a region, not a single point

A positive result must survive a finite parameter neighborhood.

## Step 6 — Independently reconstruct

Use an implementation that does not call the same production function.

## Step 7 — Adversarially falsify

Try to break the result.

## Step 8 — Promote only after robustness

Do not promote a result merely because an optimizer found it.

---

# 32. Three-Axis Run Score

Before spending significant time on a simulation, score it qualitatively on:

```text
AXIS_A=
PHYSICAL_VALIDITY_GAIN

AXIS_B=
OPERATIONAL_REPULSION_GAIN

AXIS_C=
PRACTICALITY_GAIN
```

A run with:

```text
HIGH_A
LOW_B
LOW_C
```

may still be useful if it closes a major uncertainty.

A run with:

```text
LOW_A
HIGH_B
HIGH_C
```

is not useful if the model is physically inconsistent.

The most valuable runs improve at least two axes or decisively falsify a route.

---

# 33. Practicality-Weighted Observable Set

Future candidate comparisons should preserve at least:

```text
POINT_ACCELERATION

FINITE_PAYLOAD_CM_ACCELERATION

PAYLOAD_ACCELERATION_UNIFORMITY

TOTAL_SOURCE_ENERGY

MASS_EQUIVALENT_ENERGY

EFFECTIVE_C_PAYLOAD

NEGATIVE_ACTIVE_MAGNITUDE

POSITIVE_ACTIVE_MAGNITUDE

KERNEL_LEVERAGE_RATIO

TOTAL_ACTIVE_MASS_MARGIN

LOCAL_CONSERVATION_RESIDUAL

FIELD_EQUATION_RESIDUAL

STABILITY_MARGIN

SOURCE_SIZE

PAYLOAD_SIZE

CONTROL_PARAMETER_SCALE
```

Do not compare mechanisms only by their strongest acceleration value.

---

# 34. Robustness Neighborhood Rule

A positive result should not be promoted if it exists only at one tuned optimizer point.

For important continuous parameters $\theta_i$, perturb them around the candidate.

Require the desired qualitative result to survive a finite neighborhood.

Recommended minimum local robustness tests:

```text
PARAMETER_MINUS_5_PERCENT

PARAMETER_PLUS_5_PERCENT

PARAMETER_MINUS_10_PERCENT

PARAMETER_PLUS_10_PERCENT
```

where physically sensible.

For highly sensitive parameters, report the actual allowed interval.

This turns:

```text
OPTIMIZER_FOUND_A_POINT
```

into the stronger statement:

```text
A_FINITE_OPERATING_REGION_EXISTS
```

when justified.

---

# 35. Discovery / Validation Split

For numerical optimization:

```text
DISCOVERY_STAGE=
LOWER_COST_SCAN_AND_OPTIMIZATION

VALIDATION_STAGE=
INDEPENDENT_HIGHER_ACCURACY_RECONSTRUCTION
```

Do not use the same numerical settings for both.

The validation stage should increase at least one of:

```text
GRID_RESOLUTION

QUADRATURE_ORDER

DOMAIN_SIZE

SOLVER_TOLERANCE

IMPLEMENTATION_INDEPENDENCE
```

A result should be considered provisional until it survives validation.

---

# 36. Pareto-Front Rule

Do not optimize only one composite scalar objective when multiple physical requirements compete.

Maintain a Pareto front across quantities such as:

```text
OUTWARD_ACCELERATION

ENERGY

STABILITY

KERNEL_LEVERAGE

FIELD_COMPLEXITY

PEAK_STRESS

PAYLOAD_UNIFORMITY
```

This prevented the project from incorrectly treating the thin 006D limit as automatically best.

The same discipline should continue.

---

# 37. No Order-Unity Victory Rule

When the practical gap is many orders of magnitude, an order-unity coefficient improvement is not a practical breakthrough.

Examples:

```text
C=40 -> C=20

OR

ENERGY_REDUCTION=3X
```

may be scientifically useful but should not meaningfully raise the practical-device outlook unless they reveal a new scaling mechanism.

Practicality promotion should prefer:

```text
ORDERS_OF_MAGNITUDE

OR

QUALITATIVE_SCALING_CHANGE
```

over small coefficient gains.

---

# 38. Independent Verification Rule

Every central quantitative claim should eventually have at least two genuinely independent verification paths.

Examples:

```text
ANALYTIC_DERIVATION
VS
NUMERICAL_INTEGRATION
```

```text
DIRECT_VOLUME_FORCE
VS
INDEPENDENT_MULTIPOLE_OR_SEPARATE_QUADRATURE
```

```text
EULER_LAGRANGE_SOLVER
VS
VIRIAL_IDENTITY
```

```text
AUXILIARY_DIMER_MATCH
VS
DIRECT_CONTACT_OPERATOR_MATCH
```

```text
PROJECT_CALCULATION
VS
PUBLISHED_EXPERIMENTAL_DATA
```

A unit test invoking the same implementation is not independent scientific verification.

---

# 39. Mandatory Falsification Questions for Every Green GR Run

After any outward-field result, immediately ask:

```text
DOES_THE_SIGN_SURVIVE_A_FINITE_PAYLOAD?

DOES_IT_SURVIVE_PARAMETER_PERTURBATION?

DOES_TOTAL_ACTIVE_MASS_REMAIN_POSITIVE?

IS_THE_SOURCE_FINITE?

IS_THE_SOURCE_ENERGY_FINITE?

IS_THE_SOURCE_LOCALLY_CONSERVED?

DOES_THE_FIELD_MODEL_SATISFY_ITS_OWN_EQUATIONS?

IS_THE_RESULT_STABLE?

DOES_AN_INDEPENDENT_FORCE_INTEGRATOR_AGREE?

DOES_THE_ENERGY_SCALE_IMPROVE_OR_WORSEN?

IS_THE_EFFECT_STILL_PRESENT_AFTER_ALL_SUPPORT_FIELDS_ARE_INCLUDED?
```

Do not postpone these questions unnecessarily.

---

# 40. Mandatory Limiting Cases for Current GR Work

Future drum/rim models should explicitly test:

## Zero-negative-source limit

As

```math
S_-\to0
```

repulsion must disappear.

## Infinite-rim-radius limit

As positive support moves very far away, verify the expected kernel-leverage behavior and energy cost.

## Zero-separation limit

When positive and negative active sources become co-spatial, the 016H-like failure tendency should be recovered where appropriate.

## Zero-charge limit

If charge provides stabilization, recover the appropriate unstabilized limit.

## Zero-winding limit

Recover the nonrotating configuration.

## Vacuum-field limit

All fields should approach the declared vacuum.

## Large-payload limit

Determine whether outward acceleration survives averaging over increasingly large payloads.

## Far-field limit

Positive total active mass should recover ordinary attractive asymptotics for the 006D-style branch.

---

# 41. Current GR Stop Rules

Strongly demote the current canonical drum/rim realization route if any of the following becomes robustly established:

```text
FINITE_PAYLOAD_REVERSAL_REQUIRES_PATHOLOGICAL_FINE_TUNING
```

```text
REQUIRED_KERNEL_LEVERAGE_CANNOT_BE_ACHIEVED_BY_HEALTHY_FIELD_ENERGY_BUDGETS
```

```text
VARIATIONAL_REPULSION_DISAPPEARS_WHEN_ACTUAL_FIELD_EQUATIONS_ARE_ENFORCED
```

```text
ALL_STATIONARY_FIELD_SOLUTIONS_ARE_DYNAMICALLY_UNSTABLE
```

```text
OUTWARD_FIELD_DISAPPEARS_AFTER_REQUIRED_GAUGE_OR_SUPPORT_ENERGY_IS_INCLUDED
```

```text
FINITE_PAYLOAD_REPULSION_DISAPPEARS_IN_THE_NONLINEAR_EINSTEIN_MATTER_SOLUTION
```

Do not add arbitrary compensating sectors merely to avoid a stop rule.

---

# 42. Current Protected-Scalar Stop Rules

When that branch is active, close or strongly demote it if:

```text
ONE_BODY_OPERATOR_INDUCED_ABOVE_LEAKAGE_LIMIT
```

```text
REQUIRED_PROTECTION_IS_FINE_TUNED_CANCELLATION
```

```text
ULTRALIGHT_SCALAR_MASS_DESTABILIZED_WITHOUT_TECHNICAL_PROTECTION
```

```text
RELATIVISTIC_LOCALITY_OR_GAUGE_INVARIANCE_FORBIDS_REQUIRED_MATCH
```

```text
EXPERIMENTAL_FORCE_BOUND_EXCLUDES_USEFUL_REGION
```

```text
STELLAR_OR_COSMOLOGICAL_CONSTRAINTS_ELIMINATE_USEFUL_REGION
```

---

# 43. Anti-Drift Rules

Do not:

* optimize an already-invalid mechanism;
* continue exact 006D tensor matching after 016G without a new reason;
* repeat generic centered FLS/Q-ball scans after 016H without adding genuine spatial segregation;
* mistake negative active density for outward gravity;
* mistake point acceleration for payload acceleration;
* mistake one Derrick mode for full stability;
* mistake low compactness for practical energy requirements;
* add hidden fields simply because an optimizer needs them;
* reopen Casimir searches without a new scaling principle;
* reopen generic vector models without a new theoretically motivated protection mechanism;
* describe a fifth force as ordinary GR;
* describe ground-referenced force as reactionless propulsion;
* tune a bare ultralight mass against huge loops and call it natural;
* proceed to hardware engineering before physical realization and experimental viability;
* raise the practical-progress heuristic because of parameter optimization alone.

---

# 44. Claim Promotion Rules

## 006D-inspired field branch

A candidate can move from:

```text
VARIATIONAL_PREFLIGHT
```

to:

```text
FIELD_THEORETICAL_CANDIDATE
```

only after:

```text
FINITE_ENERGY

GLOBAL_REGULARITY

FULL_EULER_LAGRANGE_EQUATIONS

CONSERVATION

FINITE_PAYLOAD_REPULSION

INDEPENDENT_RECONSTRUCTION
```

A candidate can move to:

```text
STABLE_FIELD_THEORETICAL_CANDIDATE
```

only after a meaningful perturbation spectrum is evaluated.

It can move toward:

```text
PHYSICAL_GR_REALIZATION_CANDIDATE
```

only after nonlinear Einstein-matter continuation.

## Practicality claim

No branch may be called practically promising merely because it produces $1g$ after arbitrary rescaling.

It must have a credible absolute energy and control budget.

---

# 45. Path From Current ~44% Toward 100% Milestone Completion

The percentages below are project-management milestones, not probabilities.

## Current — approximately 44%

Established:

```text
MATHEMATICAL_SIGN
FINITE_POSITIVE_ENERGY_GR_SOURCE
ENERGY_CONDITIONS
LINEARIZED_CONSERVATION
LOCAL_REPULSION
POSITIVE_FAR_FIELD_MASS
MAJOR_REALIZATION_CONSTRAINTS
```

## Approximately 50–55% — operational finite-payload geometry

Required:

```text
ROBUST_SPATIALLY_SEGREGATED_ARCHITECTURE
FINITE_PAYLOAD_OUTWARD_ACCELERATION
REALISTIC_ACTIVE_SOURCE_MAGNITUDES
```

016I targets this efficiently.

## Approximately 55–65% — actual field solution

Required:

```text
HEALTHY_LOCAL_FIELD_MODEL
FULL_EULER_LAGRANGE_SOLUTION
FINITE_ENERGY
GLOBAL_REGULARITY
FINITE_PAYLOAD_OUTWARD_FIELD
```

## Approximately 65–72% — stability

Required:

```text
NO_FATAL_DYNAMICAL_INSTABILITY
```

across the physically important perturbation spectrum.

## Approximately 72–80% — nonlinear gravitational consistency

Required:

```text
SELF_CONSISTENT_EINSTEIN_MATTER_SOLUTION
FINITE_PAYLOAD_REPULSION_PRESERVED
```

## Approximately 80–90% — practical scaling breakthrough

This is likely the hardest step.

Need a qualitative reduction in the absolute energy/control burden.

A pure order-unity reduction in $C$ is insufficient.

This may require:

```text
NEW_GEOMETRIC_SCALING
COLLECTIVE_EFFECT
EXTERNAL_BACKGROUND
STRONGER_ALLOWED_INTERACTION
OR_ANOTHER_PHYSICALLY_DERIVED_MECHANISM
```

## Approximately 90–96% — experimentally accessible implementation

Need:

```text
REAL_FIELDS_OR_MATERIALS

FINITE_CONTROL_ENERGY

CURRENT_CONSTRAINTS_PASS

SIGNAL_ABOVE_BACKGROUND

SYSTEMATICS_CONTROLLED
```

## Approximately 96–100% — practical demonstration

100% should require:

```text
REPEATABLE

CONTROLLABLE

STABLE

FINITE_PAYLOAD

USEFUL_MAGNITUDE

INDEPENDENTLY_REPLICATED

COMPLETE_ENERGY_MOMENTUM_ACCOUNTING

NO_CONVENTIONAL_FORCE_EXPLANATION
```

There is no known guaranteed path to 100%.

The buildplan is designed to discover as quickly as possible whether such a path exists.

---

# 46. Practical-Antigravity Strategy

The current best strategic interpretation is that two breakthroughs may ultimately be necessary.

## Breakthrough A — source realization

Find a physically realizable configuration that actually generates outward finite-payload acceleration.

The 006D-derived drum/rim route currently has the highest theoretical confidence for this task.

## Breakthrough B — energy scaling

Find a way to produce the useful effect without catastrophic gravitational-strength source energy.

This may require:

* a qualitatively new GR geometry;
* collective leverage;
* external background coupling;
* a stronger but allowed interaction;
* a hybrid mechanism.

The protected scalar branch remains important primarily because it could potentially address Breakthrough B.

The project should not confuse success at Breakthrough A with completion of Breakthrough B.

---

# 47. Hybrid Long-Term Possibility

A future successful mechanism may combine lessons from multiple branches.

006D may supply the **geometry principle**:

```text
NEGATIVE_OR_REPULSIVE_CONTRIBUTION=
HIGH_KERNEL_REGION

COMPENSATING_POSITIVE_CONTRIBUTION=
LOW_KERNEL_REGION
```

while another interaction supplies greater effective strength.

This possibility should remain conceptual until either:

* a physical 006D-inspired source exists; or
* a stronger interaction passes microscopic consistency.

Do not build a hybrid out of two unresolved mechanisms.

---

# 48. Research-Session Protocol

At the beginning of every substantial research session:

## Step 1 — orient

Read:

```text
RESEARCH_BUILDPLAN.md
NOTES.md
FORMATTING_AND_CODE_STANDARDS.md
LATEST_RELEVANT_JOURNAL
LATEST_CODEBUNDLE
```

## Step 2 — verify regression

Expected current baseline:

```text
94 PASSED
```

unless deliberately updated.

## Step 3 — state one active question

For the next session:

> What kernel leverage is required for a finite payload, and is that requirement compatible with physically motivated active-source budgets?

## Step 4 — write the falsifier before the run

Example:

```text
IF_REQUIRED_NEGATIVE_ACTIVE_FRACTION_OR_SEPARATION_IS_PATHOLOGICAL:
DO_NOT_BUILD_THE_FIELD_MODEL
```

## Step 5 — derive before simulating

Attempt the necessary inequality or scaling argument.

## Step 6 — perform the cheapest numerical test

Use a low-dimensional smooth geometry.

## Step 7 — validate independently

Use a second integration method.

## Step 8 — adversarially perturb

Test parameter neighborhoods and payload geometry.

## Step 9 — interpret

Record:

```text
WHAT_CHANGED
WHAT_WAS_LEARNED
WHAT_WAS_FALSIFIED
WHAT_REMAINS_UNRESOLVED
PRACTICALITY_IMPACT
CLAIM_CLASSIFICATION
NEXT
```

## Step 10 — preserve only durable results

Add permanent tests for conclusions that future work depends upon.

---

# 49. Source-Code Standards for New Scientific Runs

All substantial new simulation files must document at the top:

```text
PURPOSE

SCIENTIFIC_QUESTION

PHYSICAL_MODEL

EQUATIONS

SIGN_CONVENTIONS

UNITS

INPUTS

OUTPUTS

ASSUMPTIONS

APPROXIMATION_LEVEL

ENERGY_CONDITIONS

CONSERVATION

NUMERICAL_METHOD

VALIDATION_STRATEGY

LIMITATIONS

RELATED_FILES

CLAIM_CLASSIFICATION
```

Important equations should be documented near implementation.

Comments should explain **why** a calculation exists.

Central claims should be reconstructible by a future researcher or AI without chat history.

---

# 50. Current Project Checkpoint

```text
CURRENT_INFORMAL_PROGRESS_HEURISTIC=
APPROXIMATELY_44_PERCENT_NOT_A_PROBABILITY

STRONGEST_ESTABLISHED_RESULT=
006D_FINITE_POSITIVE_ENERGY_LINEARIZED_GR_LOCAL_REPULSION

006D_C_FINITE=
23.591586299249

006D_LOCAL_OUTWARD_FIELD=
YES

006D_POSITIVE_FAR_FIELD_ACTIVE_MASS=
YES

006D_NEC_WEC_DEC=
PASS

016A_THICK_REALIZATION_TARGET=
GREEN

016A_SIMPLE_MICROSTANDOFF_MACROSCOPIC_ENERGY_ESCAPE=
NO

016B_FIXED_CHARGE_CAPACITY=
GREEN

016C_SIMPLE_EXACT_ELECTROSTATIC_REALIZATION=
REJECTED

016E_POWER_LAW_GAUGE_ASYMPTOTIC=
GREEN_KINEMATICALLY

016F_CHARGE_WINDING_COEXISTENCE=
GREEN_KINEMATICALLY

016F_CONSERVATIVE_WINDING_TARGET=
10

016G_EXACT_MINIMAL_CANONICAL_POWER_LAW_REALIZATION=
REJECTED_UNDER_STATED_ASSUMPTIONS

016H_NEGATIVE_ACTIVE_DENSITY=
YES

016H_OUTWARD_GRAVITY=
NOT_FOUND_IN_TESTED_63_STATE_VARIATIONAL_FAMILY

NEW_GR_DESIGN_PRINCIPLE=
SPATIAL_ACTIVE_STRESS_SEGREGATION

PROTECTED_SCALAR_LOW_ENERGY_EFT=
PARAMETRIC_SURVIVOR

PROTECTED_SCALAR_RELATIVISTIC_COMPLETION=
NOT_ESTABLISHED

014D_LOCAL_DISFORMAL_TOTAL_FORCE_REVERSAL=
PRESERVED

014D_FINITE_PAYLOAD_REVERSAL=
NOT_ESTABLISHED

PRACTICAL_ANTIGRAVITY_DEVICE=
NO

NOVELTY=
NOT_ESTABLISHED
```

---

# 51. Current Decision Tree

```text
START_POST_016H

  |
  v

016I:
WHAT KERNEL LEVERAGE IS REQUIRED FOR
FINITE-PAYLOAD OUTWARD ACCELERATION?

  |
  +-- PATHOLOGICAL REQUIREMENT
  |       |
  |       v
  |   DEMOTE CANONICAL DRUM/RIM
  |   GLOBAL RERANK
  |
  +-- PLAUSIBLE REQUIREMENT
          |
          v

016J:
CAN AN EXPLICIT HEALTHY SPATIALLY SEPARATED
FIELD ANSATZ ACHIEVE THE REQUIRED LEVERAGE?

          |
          +-- NO
          |    |
          |    v
          |  DEMOTE GENERIC CANONICAL REALIZATION
          |  RERANK SCALAR / DISFORMAL
          |
          +-- YES
                 |
                 v

016K:
INDEPENDENT RECONSTRUCTION

                 |
                 +-- FAIL
                 |    |
                 |    v
                 |  DO NOT PROMOTE
                 |
                 +-- PASS
                        |
                        v

016L:
FULL EULER-LAGRANGE FIELD SOLUTION

                        |
                        +-- NO SOLUTION
                        |    |
                        |    v
                        |  DEMOTE BRANCH
                        |
                        +-- SOLUTION
                               |
                               v

016M:
FULL STABILITY

                               |
                               +-- FATAL INSTABILITY
                               |    |
                               |    v
                               |  DEMOTE / RERANK
                               |
                               +-- STABLE
                                      |
                                      v

016N:
NONLINEAR EINSTEIN-MATTER + FINITE PAYLOAD

                                      |
                                      +-- REPULSION LOST
                                      |    |
                                      |    v
                                      |  DEMOTE
                                      |
                                      +-- REPULSION PRESERVED
                                             |
                                             v

016O:
PRACTICAL SCALING

                                             |
                                             +-- PURE GR REMAINS CATASTROPHIC
                                             |       |
                                             |       v
                                             |   ACTIVATE STRONGER-INTERACTION
                                             |   OR HYBRID SEARCH
                                             |
                                             +-- QUALITATIVE SCALING BREAKTHROUGH
                                                     |
                                                     v

EXPERIMENTAL ACCESSIBILITY
```

---

# 52. Global Reranking Rule

When a major active branch fails, compare surviving routes using:

```text
THEORY_CONFIDENCE

LEVEL_OF_EXISTING_POSITIVE_EVIDENCE

NUMBER_OF_REQUIRED_NEW_ASSUMPTIONS

FINITE_PAYLOAD_PROSPECT

ENERGY_SCALING

EMPIRICAL_CONSTRAINTS

NEXT_CALCULATION_COST

NEXT_CALCULATION_FALSIFICATION_POWER

ABILITY_TO_REACH_EXPERIMENT
```

Do not automatically choose the most exotic surviving route.

Do not automatically remain with the branch that has received the most work.

---

# 53. What Would Count as the Next Major Breakthrough

## Near-term breakthrough

A smooth finite source geometry is found for which:

```text
POSITIVE_TOTAL_ACTIVE_MASS=
YES

FINITE_PAYLOAD_CM_ACCELERATION=
OUTWARD

REQUIRED_NEGATIVE_ACTIVE_FRACTION=
COMPATIBLE_WITH_HEALTHY_FIELD_PREFLIGHTS

ROBUST_PARAMETER_REGION=
YES
```

This would justify 016J.

## Stronger breakthrough

An explicit healthy localized field configuration produces:

```text
FINITE_PAYLOAD_OUTWARD_ACCELERATION=
YES

VARIATIONAL_STATIONARITY=
YES

FINITE_TOTAL_ENERGY=
YES

POSITIVE_TOTAL_ACTIVE_MASS=
YES
```

without exact 006D tensor fitting.

## Major theoretical breakthrough

A globally regular solution of actual matter field equations produces finite-payload outward gravity.

## Major physical breakthrough

The solution is dynamically stable and survives nonlinear Einstein-matter coupling.

## Practical breakthrough

The required absolute source energy or interaction strength is reduced by many orders of magnitude or obeys a qualitatively more favorable scaling.

---

# 54. What Would Count as a Successful Negative Result

A rigorous result such as:

```text
NO_HEALTHY_SPATIALLY_SEPARATED_FIELD_CAN_ACHIEVE_REQUIRED_KERNEL_LEVERAGE
```

or:

```text
FINITE_PAYLOAD_REPULSION_IS_INCOMPATIBLE_WITH_STABILITY_IN_THE_TESTED_FIELD_CLASS
```

would be a major success.

It would close a large part of the search space and move the project rapidly toward the stronger-interaction alternatives.

The buildplan should optimize for discovering truth, not preserving a favored branch.

---

# 55. Documentation Discipline

Repository roles:

```text
README.md

    Public-facing strongest result and concise current frontier.

RESEARCH_BUILDPLAN.md

    Active execution strategy, ranking, gates, stop rules, NEXT.

NOTES.md

    Detailed chronological scientific history.

journal/

    Durable completed research slices and proofs.

CLAIMS.md

    Formal claim classifications when maintained.

FORMATTING_AND_CODE_STANDARDS.md

    Markdown, mathematics, documentation, and code rules.

results/

    Numerical evidence and logs.

tests/

    Preserved known-solution and regression constraints.
```

Do not duplicate exhaustive chronology in this buildplan.

The buildplan controls the next decision.

---

# 56. Immediate Next Action

```text
ACTIVE_FRONTIER=
POST_016H_SPATIAL_ACTIVE_STRESS_SEGREGATION

ACTIVE_PHASE=
016I_FINITE_PAYLOAD_KERNEL_LEVERAGE_ENVELOPE

ACTIVE_TASK=
DERIVE_AND_NUMERICALLY_MAP_THE_MINIMUM_SPATIAL_LEVERAGE_REQUIRED_FOR_A_POSITIVE_TOTAL_ACTIVE_MASS_SOURCE_TO_ACCELERATE_A_FINITE_PAYLOAD_OUTWARD

PRIMARY_SCIENTIFIC_QUESTION=
CAN_A_CENTRAL_NEGATIVE_ACTIVE_DRUM_AND_OUTER_POSITIVE_ACTIVE_RIM_PRODUCE_ROBUST_FINITE_PAYLOAD_REPULSION_WITH_ACTIVE_SOURCE_MAGNITUDES_PLAUSIBLE_FOR_HEALTHY_FIELD_MODELS

PRIMARY_OBSERVABLE=
FINITE_PAYLOAD_CM_ACCELERATION

PRIMARY_DESIGN_METRIC=
KAPPA_MINUS_OVER_KAPPA_PLUS

REQUIRED_INEQUALITY=
KAPPA_MINUS_OVER_KAPPA_PLUS_GREATER_THAN_Q_PLUS_OVER_Q_MINUS

SECONDARY_METRIC=
EFFECTIVE_PAYLOAD_C_OR_ACCELERATION_PER_SOURCE_ENERGY

REGRESSION_BASELINE=
94_PASSED

STRONGEST_ESTABLISHED_RESULT=
006D

CURRENT_INFORMAL_PROGRESS=
APPROXIMATELY_44_PERCENT_NOT_A_PROBABILITY

PRACTICAL_ANTIGRAVITY=
NO

NEXT_IF_016I_GREEN=
016J_EXPLICIT_SPATIALLY_SEPARATED_DRUM_RIM_FIELD_VARIATIONAL_GATE

NEXT_IF_016I_RED=
GLOBAL_RERANK_PROTECTED_SCALAR_VS_DISFORMAL_VS_OTHER_HIGH_CONFIDENCE_ROUTE
```

The first next-session scientific run should therefore **not** begin by writing another complicated matter Lagrangian.

First determine exactly how much finite-payload spatial leverage is required.

If that geometry requirement is physically plausible, build the minimum field model capable of achieving it.

If it is not plausible, stop the branch before investing in a PDE solver.

That is currently the shortest high-information path toward determining whether the 006D mechanism can become physical.

---

# 57. Final Strategic Principle

The project should now operate under the following rule:

> **Optimize for the next missing physical requirement, not for the most visually impressive positive number.**

The strongest path toward practical antigravity is therefore:

```text
1.
QUANTIFY THE OPERATIONAL FINITE-PAYLOAD REQUIREMENT

2.
FIND THE MINIMUM HEALTHY FIELD MODEL THAT CAN MEET IT

3.
FORCE THAT MODEL TO SATISFY ITS ACTUAL FIELD EQUATIONS

4.
ATTACK ITS STABILITY

5.
SOLVE THE NONLINEAR GR / FINITE-PAYLOAD PROBLEM

6.
MEASURE THE ABSOLUTE ENERGY SCALING

7.
IF PURE GR REMAINS CATASTROPHIC,
ACTIVATE THE STRONGEST PHYSICALLY CONTROLLED
INTERACTION-SCALE-CHANGING ROUTE

8.
ONLY THEN MOVE TOWARD EXPERIMENT AND ENGINEERING
```

This sequence is designed to avoid both major failure modes:

```text
FAILURE_MODE_A=
SPENDING_TIME_ON_MATHEMATICALLY_INTERESTING_BUT_PHYSICALLY_UNREALIZABLE_REPULSION

FAILURE_MODE_B=
SPENDING_TIME_ON_SPECULATIVE_STRONG_FORCES_BEFORE_ESTABLISHING_A_MICROSCOPICALLY_CONSISTENT_THEORY
```

The target is not merely another positive simulation.

The target is a sequence of results in which every successful gate removes one of the remaining physical barriers between the current 006D theorem and a reproducible practical device.
