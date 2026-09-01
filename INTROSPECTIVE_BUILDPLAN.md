
# ANTIGRAVITY_RESEARCH — INTROSPECTIVE BUILDPLAN

## Kernel-Weighted Source Tomography, Gravitational Leverage, and Minimal Repulsive Structure

**Status:** proposed active discovery branch
**Project:** ANTIGRAVITY_RESEARCH
**Branch name:** INTROSPECTIVE
**Primary purpose:** determine which parts of the existing repulsive field actually produce useful outward finite-payload gravity, which parts merely enable the configuration to exist, and whether the useful mechanism can be distilled into a substantially more energy-efficient gravitational source.

---

# 1. Mission

The INTROSPECTIVE branch asks a different question from the existing realization program.

The current program asks:

> Can a complete physically consistent field configuration exist, remain stable, and generate outward finite-payload gravity?

INTROSPECTIVE asks:

> **Why does the successful configuration work, exactly where does its useful gravitational response originate, and what is the minimum physical structure required to preserve that response?**

The working hypothesis is:

> **A small subset of the field configuration may perform most of the useful repulsive gravitational work, while a much larger fraction of the total energy pays for topology, stability, conservation, compensating positive active mass, and other structural requirements.**

This hypothesis is not assumed true.

The purpose of this buildplan is to test and potentially falsify it.

---

# 2. Strategic role

INTROSPECTIVE should occur **before serious Analogue Antigravity model-building**.

The desired sequence becomes:

```text
023C numerical/stability closure
        |
        v
INTROSPECTIVE
identify productive gravitational structure
        |
        +----> improved pure-GR model if large headroom exists
        |
        +----> minimal mechanism theorem
        |
        v
023D/023E self-consistent gravity
        |
        v
Analogue Antigravity
imitate the distilled mechanism rather than the entire Skyrmion
```

INTROSPECTIVE does not supersede the current requirement to obtain a trustworthy stationary unrestricted field.

The latest \(N=73\) field has not yet passed strict stationarity. Therefore the present R6 stationarity closure remains mandatory before treating that field as an optimized physical solution.

However, inexpensive methodology development may begin immediately on:

* the promotion-grade 023BR exact rational-map field;
* the strict-stationary \(N=65\) unrestricted field;
* subsequently the strict \(N=73\) field;
* eventually the \(N=81\) companion.

Results that do not survive the unrestricted stationary resolutions must not be promoted.

---

# 3. Core scientific question

> **Is finite-payload outward gravity generated disproportionately by a geometrically localized subset of the complete positive-energy field configuration?**

If yes:

> **What local field properties distinguish those productive regions from energetically expensive but gravitationally unproductive scaffolding?**

If those properties can be isolated:

> **Can a smaller or different conserved, stable, positive-energy field configuration reproduce the productive source structure with substantially less total energy?**

---

# 4. Primary operational observable

The primary observable remains the actual finite-payload center-of-mass acceleration.

Define the outward direction for payload center \(\mathbf c\) by

```math
\hat{\mathbf n}
=
\frac{\mathbf c}{|\mathbf c|}
```

Write the finite-payload linearized-GR response as

```math
A_{\mathrm{out}}
=
\int_{\Omega}
S(\mathbf x)
K_{\mathrm{out}}(\mathbf x;\mathbf c,R_P)
\,d^3x
```

where

```math
S
=
\epsilon+p_x+p_y+p_z
```

and \(K_{\mathrm{out}}\) includes the complete Green-function sign, projection onto the outward direction, payload-volume averaging, and common gravitational prefactor.

The convention must be chosen so that

```math
A_{\mathrm{out}}>0
```

means outward acceleration.

The calculation must reconstruct the existing finite-payload result to numerical precision before any new interpretation is permitted.

---

# 5. Fundamental new quantity: influence density

Define

```math
\mathcal I(\mathbf x)
=
S(\mathbf x)
K_{\mathrm{out}}(\mathbf x)
```

so that

```math
A_{\mathrm{out}}
=
\int
\mathcal I(\mathbf x)
\,d^3x
```

This is the **kernel-weighted gravitational influence density**.

It is not energy density.

It is not active density alone.

It answers:

> How much does this particular spatial element contribute to the actual finite-payload outward acceleration?

This should become the central diagnostic of INTROSPECTIVE.

---

# 6. Outward and opposing influence

Separate

```math
\mathcal I_+
=
\max(\mathcal I,0)
```

and

```math
\mathcal I_-
=
\min(\mathcal I,0)
```

Define

```math
A_+
=
\int
\mathcal I_+
\,d^3x
```

and

```math
A_-
=
\int
\mathcal I_-
\,d^3x
```

such that

```math
A_{\mathrm{out}}
=
A_+
+
A_-
```

This distinction is critical.

A region with negative active density does not necessarily help the desired acceleration.

Likewise, a region with positive active density does not necessarily oppose it.

**Kernel geometry determines the actual sign of its payload contribution.**

---

# 7. Cancellation factor

Define the gravitational cancellation factor

```math
\mathcal C
=
\frac{
\int |\mathcal I|\,d^3x
}{
\left|
\int \mathcal I\,d^3x
\right|
}
```

For a perfectly non-cancelling useful source,

```math
\mathcal C=1
```

If

```math
\mathcal C\gg1
```

then the final outward acceleration is a small residual between much larger mutually opposing contributions.

That would be an immediate explanation for poor efficiency.

This quantity should be tracked across every future model.

---

# 8. Gravitational leverage per energy

Let the local positive energy density be

```math
\rho(\mathbf x)
=
T_{00}(\mathbf x)
```

Define a diagnostic leverage density

```math
\Lambda(\mathbf x)
=
\frac{
\mathcal I(\mathbf x)
}{
\rho(\mathbf x)+\rho_{\mathrm{floor}}
}
```

where \(\rho_{\mathrm{floor}}\) is used only to avoid division by numerical zeros and must be reported.

Interpretation:

```text
large positive Lambda:
large useful payload influence per local energy

near-zero Lambda:
energetically present but gravitationally unproductive for this payload

negative Lambda:
energy spent producing an opposing contribution
```

This is a diagnostic quantity only.

Because a physical field is nonlocal and constrained by its equations, one may not delete a low-\(\Lambda\) region and claim the remaining structure is realizable.

---

# 9. The productive skeleton hypothesis

Define the **productive skeleton** as the smallest robust subset of source space that accounts for a specified fraction of gross outward influence.

For example, define \(E_{50}\) as the fraction of total energy contained in the optimally ranked spatial subset responsible for \(50\%\) of

```math
A_+
```

Similarly define

```text
E50
E80
E90
E95
```

for \(50\%\), \(80\%\), \(90\%\), and \(95\%\) of gross outward influence.

The ordering variable should initially be

```math
\frac{\mathcal I_+}{\rho}
```

but results must also be checked under alternative non-singular rankings.

A strong concentration result would look schematically like:

```text
10% of total energy
produces
80% of gross useful outward influence
```

This would support the productive-skeleton hypothesis.

A result such as

```text
80% of energy
is needed for
80% of outward influence
```

would strongly weaken it.

---

# 10. Force-concentration curves

Construct a cumulative curve analogous to a concentration or Lorenz curve.

For the source ordered from largest useful leverage to smallest, calculate

```math
F(E_f)
=
\frac{
\text{gross outward influence contained in the best energy fraction }E_f
}{
A_+
}
```

Plot

```text
F versus E_f
```

for:

* 023BR exact map;
* strict \(N=65\);
* strict \(N=73\);
* later \(N=81\);
* multiple payload orientations;
* multiple payload distances;
* multiple payload radii.

A real structural concentration should survive these changes.

---

# 11. Deadweight-energy diagnostic

Define an energy-weighted measure of regions producing negligible direct payload influence.

Rather than fix one arbitrary threshold, calculate the complete family

```math
D(\lambda)
=
\frac{
\int_{|\Lambda|<\lambda}\rho\,d^3x
}{
\int\rho\,d^3x
}
```

for a logarithmic range of \(\lambda\).

This asks:

> What fraction of the total energy lies in regions having extremely little direct gravitational leverage?

That energy may still be physically mandatory.

Therefore call it:

```text
LOW-DIRECT-LEVERAGE ENERGY
```

not:

```text
WASTED ENERGY
```

until subsequent ablation and re-relaxation tests determine whether it is actually dispensable.

---

# 12. Energy-role decomposition

For the Skyrme branch, decompose the total energy into physically distinct contributions:

```math
E
=
E_2+E_4+E_V
```

or the exact repository convention.

At every spatial location map:

```text
e2
e4
V
rho
S
baryon density
I
Lambda
```

Then compute:

```math
A_{\mathrm{out}}^{(e_2)}
```

```math
A_{\mathrm{out}}^{(e_4)}
```

```math
A_{\mathrm{out}}^{(V)}
```

only when such decomposition is algebraically legitimate for the active-source expression.

The project already has the important identity in the selected branch:

```math
S
=
2(e_4-V)
```

So INTROSPECTIVE should explicitly identify whether useful gravitational influence comes primarily from:

```text
Skyrme quartic-gradient dominance
```

or

```text
potential-energy dominance
```

and where the transition occurs.

---

# 13. Active-source transition surface

Construct the complete 3D surface

```math
\Sigma_0
=
\{
\mathbf x:
S(\mathbf x)=0
\}
```

which for

```math
S=2(e_4-V)
```

satisfies

```math
e_4=V
```

Study:

* surface topology;
* curvature;
* distance from payload;
* relationship to productive hotspots;
* relationship to baryon-density structure;
* relationship to angular-map features.

Do **not** assume the productive set lies on this surface.

Test it.

---

# 14. Geometry and rational-map diagnostics

The rational-map literature gives a concrete geometric structure against which the gravitational influence can be compared.

For the exact \(B=7\) map, calculate locally:

```text
J
J^2
J^4
Wronskian magnitude
baryon density
energy density
S
I
Lambda
```

The rational-map angular energy contains strongly nonlinear dependence on angular stretching, including fourth powers through the angular functional. The literature also establishes that Wronskian zeros correspond to low baryon and energy density and generate the familiar polyhedral holes. ([ResearchGate][1])

Therefore explicitly test competing hypotheses:

```text
H_FACE:
productive influence is face-centered

H_EDGE:
productive influence is edge-centered

H_VERTEX:
productive influence is vertex-centered

H_TRANSITION:
productive influence follows S=0 interfaces

H_HIGH_J:
productive influence follows extreme angular stretching

H_LOW_J:
productive influence follows low-stretch holes

H_RADIAL:
angular geometry is secondary and radial placement dominates

H_DIFFUSE:
there is no localized productive skeleton
```

No hypothesis receives priority because of the generated infographic.

---

# 15. Influence ridges instead of “emission points”

Do not use the phrase **emission point** as a scientific claim.

Gravity is not being emitted from isolated vertices in the current static model.

Instead identify:

```text
INFLUENCE MAXIMA
INFLUENCE RIDGES
INFLUENCE SHEETS
PRODUCTIVE CONNECTED COMPONENTS
```

of

```math
\mathcal I_+
```

and

```math
\Lambda_+
```

If the field genuinely contains robust line-like or point-like productive structures, the analysis should discover them automatically.

Use:

* 3D ridge extraction;
* connected-component analysis;
* local maxima;
* persistence under threshold variation;
* optionally persistent-homology diagnostics if needed.

A feature that disappears under small resolution or threshold changes is not physical evidence.

---

# 16. Spherical-harmonic decomposition

At fixed radius decompose the active source and influence density:

```math
S(r,\theta,\phi)
=
\sum_{\ell,m}
S_{\ell m}(r)
Y_{\ell m}(\theta,\phi)
```

and similarly

```math
\mathcal I(r,\theta,\phi)
=
\sum_{\ell,m}
I_{\ell m}(r)
Y_{\ell m}(\theta,\phi)
```

Determine which angular multipoles actually generate the outward finite-payload response.

This may reveal that the complicated \(B=7\) structure reduces gravitationally to only a few important modes.

If, for example,

```text
>95% of the operational response
```

can be reconstructed from a small set of low-order multipoles, that is a major simplification.

Conversely, if high-\(\ell\) structure is essential, that tells us the topology-induced fine structure matters directly.

---

# 17. Radial-versus-angular leverage

Separate the question:

> Is the antigravity effect primarily caused by **where the source sits radially**, or by the full topological angular pattern?

Construct several controlled surrogate sources:

```text
RADIAL_AVERAGE
ANGULAR_AVERAGE
LOW_MULTIPOLE_RECONSTRUCTION
FULL_SOURCE
```

All must preserve the same integrated quantities when possible.

Compare their finite-payload accelerations.

This gives a cheap and decisive mechanism test.

Possible outcomes:

```text
RADIAL_STRUCTURE_DOMINATES
```

or

```text
TOPOLOGICAL_ANGULAR_STRUCTURE_IS_OPERATIONALLY_ESSENTIAL
```

or a quantified combination.

---

# 18. INT-0 — reference-state freeze

## Scientific question

Which existing states are sufficiently trustworthy to use for introspection?

## Actions

Freeze and checksum:

```text
023BR promotion-grade exact rational-map source

023CR4R strict-stationary N65 source

strict-stationary N73 source when available

N81 companion when available
```

## Required metadata

For each:

```text
source SHA
field artifact SHA
grid
domain
energy
topology
gradient RMS
gradient max
payload geometry
payload orientation
active total
minimum active fraction
DEC margin
```

## Stop rule

Do not promote conclusions derived solely from the currently non-strict \(N=73\) checkpoint.

---

# 19. INT-1 — influence tomography

This is the **highest-information first experiment**.

No optimization.

No new physics.

No altered field equations.

## Compute

For every grid element:

```text
rho
S
kernel K_out
I
I_positive
I_negative
Lambda
radius
payload distance
baryon density
e2
e4
V
```

## Required identities

Numerically verify:

```math
\int\mathcal I\,d^3x
=
A_{\mathrm{existing}}
```

within the expected discretization tolerance.

Independently reconstruct the force using a second implementation.

## Outputs

Produce:

```text
3D arrays
radial bins
angular bins
percentile tables
cumulative concentration curves
slice figures
isosurfaces
```

## Promotion

`INTROSPECTIVE_INFLUENCE_TOMOGRAPHY=GREEN`

only if the influence integral reproduces the trusted payload-force result independently.

---

# 20. INT-2 — concentration and cancellation audit

Compute:

```text
A+
A-
cancellation factor C
E50
E80
E90
E95
low-direct-leverage energy curves
```

across:

```text
multiple payload orientations
multiple payload radii
multiple payload distances
N65
N73
later N81
```

## Strong productive-skeleton evidence

A useful provisional criterion is:

```text
<= 10% of source energy
accounts for
>= 50% of gross useful outward influence
```

and the conclusion remains qualitatively stable across resolution and orientation.

This threshold is a **diagnostic promotion threshold**, not a fundamental physical constant.

Also report the complete concentration curve so the conclusion does not depend on one chosen number.

## Falsifier

If influence tracks energy approximately proportionally across the source and the concentration disappears under resolution changes:

```text
PRODUCTIVE_SKELETON_HYPOTHESIS=
NOT_SUPPORTED
```

That is a useful negative result.

---

# 21. INT-3 — geometric causation audit

Correlate \(\mathcal I\) and \(\Lambda\) against:

```text
J
J^2
J^4
Wronskian magnitude
baryon density
rho
S
|grad S|
distance to S=0 surface
surface curvature
radius
payload distance
```

Use:

```text
Pearson correlations
rank correlations
conditional expectations
mutual-information diagnostics if useful
sector-conditioned histograms
```

Do not promote correlation to causation.

Then perturb one geometric feature at a time in controlled surrogate-source calculations.

---

# 22. INT-4 — face/edge/vertex decomposition

Construct a symmetry-aware decomposition of the \(B=7\) geometry into neighborhoods of:

```text
faces
edges
vertices
Wronskian-zero directions
```

Measure for each sector:

```text
fraction of total energy
fraction of gross outward influence
fraction of opposing influence
mean leverage
maximum leverage
baryon number fraction
```

Repeat under rotations of the payload.

A genuine vertex/edge hotspot should move predictably under symmetry rotations.

---

# 23. INT-5 — frozen-field ablation experiments

These are **diagnostics only**.

Take the trusted source and mathematically suppress or attenuate selected regions when evaluating the gravitational integral.

Examples:

```text
remove highest-energy / lowest-leverage regions

remove individual shells

remove face sectors

remove edge sectors

remove vertex sectors

remove positive-active regions

remove negative-active regions

retain only top 1%, 5%, 10%, 20% by leverage
```

Calculate the instantaneous gravitational response.

This answers:

> If these regions could somehow be removed while everything else remained fixed, how much useful force would remain?

It does **not** answer whether such a source satisfies conservation or field equations.

Every output must state:

```text
COUNTERFACTUAL_SOURCE_ABLATION_ONLY
NOT_A_PHYSICAL_CONFIGURATION
```

---

# 24. INT-6 — field-space localized perturbation audit

A stronger test perturbs the actual field \(\phi\), not the already-derived source \(S\).

Construct smooth local tangent perturbations centered on:

```text
high-leverage productive regions
low-leverage high-energy regions
S=0 surfaces
face centers
edges
vertices
```

For each perturbation measure:

```text
delta E
delta A_payload
delta topology
field-equation residual
DEC change
active-mass change
```

Use symmetric \(\pm\epsilon\) perturbations and an epsilon convergence sweep.

This gives a direct numerical approximation to

```math
\frac{\delta A}{\delta\phi}
```

and

```math
\frac{\delta E}{\delta\phi}
```

in localized directions.

---

# 25. INT-7 — adjoint gravitational design sensitivity

This is potentially the most important mathematical stage.

Let the physical field equations be

```math
F(\phi,\theta)=0
```

and define an operational objective such as

```math
J(\phi,\theta)
=
A_{\mathrm{out}}
```

or

```math
J
=
\frac{A_{\mathrm{out}}}{E}
```

for appropriately normalized comparisons.

For a stationary field, solve the adjoint equation

```math
H^T\lambda
=
\frac{\partial J}{\partial\phi}
```

where \(H\) is the physical field Hessian/Jacobian after exact zero modes are removed.

Because our audited Hessian should be self-adjoint,

```math
H^T
\approx
H
```

giving

```math
H\lambda
=
\frac{\partial J}{\partial\phi}
```

Then for a model/design parameter \(\theta\),

```math
\frac{dJ}{d\theta}
=
\frac{\partial J}{\partial\theta}
-
\lambda^T
\frac{\partial F}{\partial\theta}
```

up to the adopted sign convention.

This is the correct way to ask:

> **If the field is required to remain a solution after we modify some aspect of the model, which modification most efficiently increases outward gravity?**

It incorporates relaxation.

That is fundamentally stronger than deleting voxels.

Adjoint sensitivity is precisely the standard tool used in large PDE-constrained design problems where directly perturbing every design variable would be prohibitive. ([ScienceDirect][2])

---

# 26. Energy-efficiency objective

Define several objectives rather than optimizing one blindly.

Primary:

```math
\eta_G
=
\frac{
A_{\mathrm{out}}
}{
E
}
```

At fixed source scale \(L\), this relates directly to improving the coefficient in

```math
E
=
C
\frac{a c^2L^2}{G}
```

Also track:

```math
\eta_{\mathrm{active}}
=
\frac{
|M_{\mathrm{active,negative,useful}}|
}{
E/c^2
}
```

and the cancellation-adjusted measure

```math
\eta_{\mathrm{net}}
=
\frac{
A_{\mathrm{out}}
}{
A_++|A_-|
}
```

No single efficiency measure should determine promotion.

---

# 27. INT-8 — source-level theoretical headroom bound

Before inventing a new field theory, solve a more abstract question:

> Given the desired payload geometry and reasonable local stress constraints, how efficiently could *any source in this broad class* generate the same outward response?

Construct a relaxed optimization problem for \(T_{\mu\nu}\).

Schematically:

```math
\min
\int \epsilon\,d^3x
```

subject to:

```math
\nabla_\mu T^{\mu\nu}=0
```

appropriate staticity/boundary conditions,

```math
\epsilon\ge0
```

and whichever energy conditions are being imposed, together with

```math
A_{\mathrm{out}}
\ge
A_{\mathrm{target}}
```

and

```math
M_{\mathrm{far}}>0
```

This is **not automatically a realizable matter model**.

It gives a source-level bound.

Compare:

```text
CURRENT_SKYRMION_C

versus

RELAXED_SOURCE_BEST_C
```

This tells us whether there is:

```text
2x headroom
10x headroom
100x headroom
```

before spending months engineering another microscopic realization.

---

# 28. INT-9 — physically mandatory scaffolding test

Suppose tomography identifies a region carrying substantial energy but little direct gravitational influence.

Ask why that region exists.

Classify its role:

```text
TOPOLOGY
GRADIENT_REGULARIZATION
DERRICK_BALANCE
CONSERVATION
BOUNDARY_MATCHING
STABILITY
FISSION_RESISTANCE
POSITIVE_FAR_MASS
OTHER
```

Then perform controlled re-relaxations.

Attempt to reduce that region through an allowed model or boundary parameter.

After every modification require:

```text
FIELD_EQUATIONS
TOPOLOGY
CONSERVATION
DEC if claimed
STATIONARITY
STABILITY
POSITIVE_TOTAL_MASS
FINITE_PAYLOAD_FORCE
```

A region is not truly “deadweight” until the system can survive with less of it.

---

# 29. INT-10 — reduced gravitational model

If INT-1 through INT-9 reveal a simple productive structure, construct a reduced model.

Possible representations include:

```text
few radial shells

few angular multipoles

localized productive patches

wall-interface model

edge-network model

vertex-network model

low-rank source decomposition
```

The reduced model should reproduce:

```text
payload acceleration
orientation dependence
active-mass profile
total far-field mass
```

within predefined errors.

An illustrative target:

```text
PAYLOAD_FORCE_RELATIVE_ERROR <= 1%

TOTAL_ACTIVE_MASS_RELATIVE_ERROR <= 1%

ORIENTATION_MARGIN_SIGN = PRESERVED
```

while using dramatically fewer structural degrees of freedom.

The purpose is understanding, not immediate physical realization.

---

# 30. INT-11 — minimal mechanism theorem

At this stage attempt to state the mechanism without mentioning “Skyrmion” unless necessary.

Desired form:

> A finite positive-energy source produces local outward finite-payload gravity when conditions \(X,Y,Z\) on its active-source morphology, kernel leverage, conservation structure, and compensating far-field mass are satisfied.

Distinguish:

```text
NECESSARY CONDITIONS

SUFFICIENT CONDITIONS

MODEL-SPECIFIC CONDITIONS

STABILITY CONDITIONS
```

This may become one of the most important theoretical outputs of the project.

---

# 31. INT-12 — efficient new-model gate

Only after the preceding analysis should we design a newer pure-GR realization.

The input is no longer:

> “Find another exotic field configuration.”

It becomes:

> **Construct the cheapest stable field theory that reproduces the productive skeleton and only the scaffolding that INTROSPECTIVE proved is mandatory.**

Candidate models must be evaluated against the same finite-payload observable.

A new architecture earns serious follow-up only if it achieves one of:

```text
substantial C reduction

substantial beta increase

substantial cancellation-factor reduction

simpler mandatory support structure

qualitatively better scaling
```

---

# 32. Promotion ladder

## INT-A — tomography

May claim:

```text
KERNEL_WEIGHTED_SOURCE_TOMOGRAPHY_RECONSTRUCTED
```

after independent force reconstruction.

## INT-B — productive concentration

May claim:

```text
ROBUST_PRODUCTIVE_SOURCE_CONCENTRATION
```

only after survival across:

```text
resolution
orientation
payload size
payload distance
unrestricted stationary field
```

## INT-C — geometric mechanism

May claim:

```text
PRODUCTIVE_GEOMETRIC_STRUCTURE_IDENTIFIED
```

only after correlation plus controlled perturbation establishes more than visual coincidence.

## INT-D — physically admissible sensitivity

May claim:

```text
FIELD_RELAXED_EFFICIENCY_DIRECTION_IDENTIFIED
```

only after adjoint prediction agrees with independently re-solved perturbations.

## INT-E — source-level headroom

May claim:

```text
PURE_GR_SOURCE_EFFICIENCY_HEADROOM_QUANTIFIED
```

only after an independently reconstructed relaxed bound.

## INT-F — reduced mechanism

May claim:

```text
MINIMAL_OPERATIONAL_REPULSION_MECHANISM_EXTRACTED
```

only if the reduced representation reproduces the full finite-payload behavior robustly.

## INT-G — improved physical model

May claim:

```text
MORE_ENERGY_EFFICIENT_PHYSICAL_GR_REALIZATION
```

only after complete field existence, conservation, stability, energy-condition, finite-payload, and scaling checks.

---

# 33. What would constitute a major discovery inside the project

Any of the following would materially change the frontier:

### Discovery class 1 — extreme concentration

For example:

```text
< 5% of energy
accounts for
> 80% of gross outward influence
```

robustly.

This would imply the current model contains an extremely concentrated gravitationally productive subsystem.

### Discovery class 2 — high cancellation

For example:

```math
\mathcal C
\gg
10
```

showing that the net repulsion is the difference between much larger contributions.

That would reveal a concrete optimization target.

### Discovery class 3 — simple geometric skeleton

For example, almost all useful response reducing to:

```text
one radial interface
+
one or two angular multipoles
```

instead of the complete \(B=7\) field.

### Discovery class 4 — large theoretical headroom

A conserved source-level bound showing the current realization lies:

```text
10x
100x
or more
```

above a mathematically accessible coefficient.

### Discovery class 5 — topology only stabilizes

If topology is found to be crucial for stability but almost irrelevant to the gravitational kernel itself, it may become possible to replace the expensive topological scaffolding with a cheaper stabilizer.

### Discovery class 6 — topology directly generates leverage

Conversely, if high-leverage regions are inseparable from the topology, that would explain why simpler prior sources fail and tell us exactly what future realizations must reproduce.

---

# 34. Important negative results

These outcomes would also be major results:

```text
USEFUL_INFLUENCE_IS_DIFFUSE_THROUGHOUT_THE_FIELD
```

```text
LOW_LEVERAGE_REGIONS_ARE_MANDATORY_FOR_STABILITY
```

```text
REMOVING_COMPENSATING_POSITIVE_STRUCTURE_DESTROYS_CONSERVATION
```

```text
ADJOINT_EFFICIENCY_DIRECTIONS_COLLAPSE_THE_TOPOLOGY
```

```text
CURRENT_MODEL_IS_ALREADY_NEAR_THE_SOURCE_LEVEL_BOUND
```

Any of these would tell us that large pure-GR efficiency improvements are unlikely and strengthen the case for Analogue Antigravity.

Negative results must be preserved rather than optimized around.

---

# 35. The \(1/G\) boundary remains

Even an extraordinarily successful INTROSPECTIVE branch does not by itself eliminate

```math
E
\sim
\frac{a c^2L^2}{G\beta}
```

The existing project analysis indicates that ordinary changes to Skyrme normalization cannot eliminate the fundamental \(1/G\) scaling for fixed macroscopic gravitational acceleration and scale. 

Therefore distinguish:

```text
EFFICIENCY BREAKTHROUGH:
C reduced dramatically

from

SCALING BREAKTHROUGH:
1/G dependence avoided or replaced
```

A reduction from

```text
C ~ 100
```

to

```text
C ~ 1
```

would be scientifically important.

It would still not constitute practical macroscopic antigravity.

The project already requires orders-of-magnitude improvement or a qualitative scaling change before calling something a practical breakthrough. 

---

# 36. Relationship to 023C

The immediate numerical frontier remains strict \(N=73\) closure.

Do not mix the R6 stationarity solver with the first INTROSPECTIVE implementation.

The correct ordering is:

```text
finish R6 decision
        |
        +--> strict N73 available:
        |       use N65 + N73 immediately
        |
        +--> N73 remains numerically incomplete:
                develop INT-1 on N65 and 023BR
                but defer unrestricted-resolution promotion
```

This complies with the repository rule to avoid mixing new physics, major numerical changes, and unrelated research questions inside one slice. 

---

# 37. Relationship to 023D

INTROSPECTIVE does not necessarily have to completely finish before 023D.

But if INTROSPECTIVE uncovers a radically simpler and substantially more efficient field architecture **before** the expensive Einstein-Skyrme continuation, rerank.

There is little value in performing 023D on an obviously superseded inefficient realization.

Decision:

```text
IF_INTROSPECTIVE_FINDS_ROBUST_NEW_MODEL_WITH_MAJOR_C_IMPROVEMENT:
    VALIDATE_NEW_MODEL_THROUGH_023C_EQUIVALENT_GATES
    THEN_RUN_SELF_CONSISTENT_GRAVITY_ON_BEST_MODEL

ELSE:
    CONTINUE_023D_ON_EXISTING_B7_FIELD
```

---

# 38. Relationship to Analogue Antigravity

Analogue Antigravity is deliberately deferred as the main research frontier until INTROSPECTIVE extracts the mechanism.

The desired handoff is:

```text
FULL SKYRMION
        |
        v
INFLUENCE TOMOGRAPHY
        |
        v
PRODUCTIVE SKELETON
        |
        v
MINIMAL MECHANISM
        |
        +--> CHEAPER TRUE-GR REALIZATION
        |
        +--> ANALOGUE ANTIGRAVITY TARGET KERNEL
```

That way the analogue program imitates **what actually causes the useful force**, not a visually similar field configuration.

---

# 39. Independent verification requirements

Every central INTROSPECTIVE result should have at least two paths.

For example:

```text
payload influence:
voxel integration
vs
independent continuous cubature

angular structure:
Cartesian field reconstruction
vs
rational-map analytic evaluation

sensitivity:
adjoint derivative
vs
explicit finite perturbation and re-solve

reduced model:
direct reconstructed force
vs
independent Green-function implementation
```

This is consistent with the project's existing requirement for independent reconstruction of central quantitative claims. 

---

# 40. Resolution requirements

Hotspot localization is particularly vulnerable to discretization artifacts.

Require:

```text
N65
N73
N81 when available
```

and test convergence of:

```text
hotspot position

hotspot integrated influence

E50/E80/E90

cancellation factor

multipole spectrum

S=0 surface location
```

Do not demand pointwise voxel convergence where an integrated regional observable is the physically meaningful quantity.

---

# 41. Blind wildcard diagnostics

The user's established wildcard numbers may be used only as harmless blind robustness probes when appropriate:

```text
0.625
1.6
1.875
3.125
5
```

Examples include:

```text
kernel-distance multipliers

smoothing-width checks

threshold-independent diagnostic samples
```

They must never be optimization targets or treated as physically privileged values.

---

# 42. First implementation: INT-1A

The **first run should be small and decisive**.

Suggested filename:

`simulations/int001a_kernel_weighted_source_influence_tomography.py`

## Active question

> Is the useful finite-payload outward response strongly concentrated in a small fraction of the stationary \(B=7\) field's total energy?

## Inputs

Start with:

```text
strict N65 field
023BR payload geometry
existing exact payload kernel
```

Use strict \(N=73\) automatically when available.

## Compute only

```text
rho
S
K_out
I
Lambda
A+
A-
cancellation factor
E50/E80/E90/E95
radial concentration
angular concentration
```

No optimization.

No adjoint.

No new model.

No expensive Hessian solve.

## Cheapest decisive experiment

Reconstruct the known payload force from

```math
\int\mathcal I\,d^3x
```

then sort the grid by useful influence per unit energy and generate the concentration curve.

That single calculation can immediately tell us whether the central hypothesis has real quantitative support.

---

# 43. INT-1A promotion condition

Promote INT-1A if:

```text
SOURCE_AUDIT=PASS

KNOWN_PAYLOAD_FORCE_RECONSTRUCTION=PASS

ENERGY_RECONSTRUCTION=PASS

ACTIVE_SOURCE_IDENTITY=PASS

INFLUENCE_SIGN_CONVENTION=PASS

INDEPENDENT_FORCE_RECONSTRUCTION=PASS

CONCENTRATION_METRICS=REPORTED

CANCELLATION_FACTOR=REPORTED
```

Then classify the hypothesis as one of:

```text
STRONG_CONCENTRATION

MODERATE_CONCENTRATION

DIFFUSE

UNRESOLVED_BY_RESOLUTION
```

Do not declare a discovery from INT-1A alone.

---

# 44. INT-1A falsifier

The central hypothesis is immediately weakened if:

```text
OUTWARD_INFLUENCE_TRACKS_ENERGY_DENSITY_APPROXIMATELY_PROPORTIONALLY
```

and no robust localized region dominates the gross outward contribution.

If that occurs, skip elaborate hotspot studies and move directly to cancellation/source-bound analysis.

---

# 45. INT-1A stop rule

Do not:

```text
optimize field parameters

change the Lagrangian

modify topology

run a large Hessian

launch a parameter scan
```

until basic tomography answers whether there is anything concentrated to explain.

This is the highest-information-per-compute ordering.

---

# 46. Recommended execution ladder

```text
CURRENT:
023C2AQS2R6 stationarity closure

NEXT:
INT-1A
kernel-weighted source influence tomography

THEN IF CONCENTRATED:
INT-2
cancellation + productive skeleton

INT-3
geometry/J/Wronskian/S=0 correlations

INT-4
sector decomposition

INT-5
counterfactual ablation

INT-6
physical localized perturbations

INT-7
adjoint field-relaxed sensitivity

INT-8
source-level theoretical headroom

INT-9
mandatory-scaffolding determination

INT-10
reduced source model

INT-11
minimal mechanism theorem

INT-12
new efficient physical realization

THEN:
023D on the best surviving physical model

THEN:
Analogue Antigravity
```

---

# 47. Practicality decision gate

INTROSPECTIVE earns a major practicality rerank only if one of these occurs:

```text
C REDUCED BY ORDERS OF MAGNITUDE

OR

BETA INCREASED BY ORDERS OF MAGNITUDE

OR

CANCELLATION ELIMINATED BY ORDERS OF MAGNITUDE

OR

A QUALITATIVELY BETTER PARAMETRIC SCALING IS DERIVED
```

Factors of two, ten, or even one hundred may be scientifically important without making the system practical.

---

# 48. Claim discipline

INTROSPECTIVE may eventually establish statements like:

> Most of the finite-payload outward response of the tested stationary \(B=7\) field originates from a quantitatively identified subset of its energy distribution.

or:

> The useful repulsive response is controlled predominantly by a specific radial/angular source morphology.

or:

> A reduced source reproduces the operational force of the full field to stated accuracy.

It must **not** automatically claim:

```text
NEW_GRAVITATIONAL_LAW

GRAVITY_EMISSION_POINT

NEGATIVE_MASS_PARTICLE

PRACTICAL_ANTIGRAVITY

NEW_PHYSICS_DISCOVERY
```

unless future evidence independently supports such claims.

---

# 49. What success would mean

The strongest possible INTROSPECTIVE outcome would be something like:

```text
FULL_B7_FIELD
TOTAL_ENERGY = E

PRODUCTIVE_SUBSTRUCTURE
ENERGY FRACTION << 1

PRODUCTIVE_SUBSTRUCTURE
ACCOUNTS FOR MOST OUTWARD PAYLOAD RESPONSE

MANDATORY_STABILITY_SCAFFOLDING
IDENTIFIED

SOURCE-LEVEL HEADROOM
LARGE

NEW CONSERVED FIELD ARCHITECTURE
REPRODUCES PRODUCTIVE STRUCTURE

TOTAL ENERGY
SUBSTANTIALLY REDUCED
```

That would be a genuine advance beyond merely proving that the present Skyrmion works.

It would tell us **why it works**.

---

# 50. Immediate next action

```text
ACTIVE_BRANCH=
INTROSPECTIVE

ACTIVE_PHASE=
INT_1A_KERNEL_WEIGHTED_SOURCE_INFLUENCE_TOMOGRAPHY

PRIMARY_SCIENTIFIC_QUESTION=
IS_THE_FINITE_PAYLOAD_OUTWARD_GRAVITATIONAL_RESPONSE_CONCENTRATED_IN_A_SMALL_ENERGY_FRACTION_OF_THE_CURRENT_STATIONARY_B7_FIELD

PRIMARY_OBSERVABLE=
FINITE_PAYLOAD_OUTWARD_ACCELERATION_CONTRIBUTION_DENSITY

PRIMARY_DIAGNOSTIC=
I_OF_X_EQUALS_S_OF_X_TIMES_K_OUT_OF_X

SECONDARY_DIAGNOSTICS=
LOCAL_LEVERAGE
CANCELLATION_FACTOR
E50
E80
E90
E95

CHEAPEST_DECISIVE_TEST=
RECONSTRUCT_THE_EXISTING_PAYLOAD_FORCE_AS_A_VOXELWISE_INFLUENCE_INTEGRAL_AND_COMPUTE_FORCE_VERSUS_ENERGY_CONCENTRATION

PROMOTION_CONDITION=
INDEPENDENT_FORCE_RECONSTRUCTION_PLUS_RESOLUTION_ROBUST_CONCENTRATION_METRICS

FALSIFIER=
USEFUL_INFLUENCE_IS_DIFFUSE_AND_APPROXIMATELY_PROPORTIONAL_TO_ENERGY_ACROSS_THE_SOURCE

STOP_RULE=
DO_NOT_OPTIMIZE_OR_CHANGE_THE_FIELD_THEORY_UNTIL_TOMOGRAPHY_ESTABLISHES_WHETHER_A_PRODUCTIVE_SUBSTRUCTURE_EXISTS

NEXT_IF_STRONGLY_CONCENTRATED=
INT_2_CANCELLATION_AND_PRODUCTIVE_SKELETON_DECOMPOSITION

NEXT_IF_DIFFUSE=
INT_2B_SOURCE_LEVEL_CANCELLATION_AND_ENERGY_BOUND_ANALYSIS

PRACTICAL_ANTIGRAVITY_DEVICE=
NO

NEW_PHYSICS_DISCOVERY=
NO
```

---
