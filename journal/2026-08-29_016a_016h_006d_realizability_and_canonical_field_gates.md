# Research Journal — 2026-08-29

## 006D Physical Realizability Program: Thickness Optimization, Gauge/Winding Constraints, Canonical Euler-Lagrange No-Go, and Explicit Field-Model Gravity Gate

## Objective

The primary scientific question investigated in this research slice was:

> **Can the project’s constructive 006D positive-energy repulsive stress-energy configuration be promoted from an engineered linearized-GR source toward a physically realizable, stable local relativistic field configuration that retains an outward gravitational field?**

The 006D result had already established that static linearized general relativity permits an explicit finite-radius, finite-thickness, nonsingular, positive-energy, locally conserved type-I stress-energy configuration satisfying NEC, WEC, and DEC whose calculated near gravitational field points outward while its far-field active mass remains positive.

The unresolved problem was no longer the sign of gravity.

The unresolved problem was **matter realization**.

This research slice therefore investigated, in sequence:

```text
016A
PRACTICALITY-OPTIMIZED 006D THICKNESS

016B
THICK-SOURCE FIXED-CHARGE / GAUGE CAPACITY

016C
GLOBAL ELECTROSTATIC GAUGE INTEGRABILITY

016D
SMOOTH EXPONENTIAL-TAIL 006D REALIZABILITY

016E
TWO-SECTOR GAUGED-SCALAR TAIL ASYMPTOTICS

016F
SIMULTANEOUS CHARGE / WINDING COEXISTENCE

016G
ASYMPTOTIC CANONICAL EULER-LAGRANGE COMPATIBILITY

016H
EXPLICIT HEALTHY CANONICAL FIELD-MODEL GRAVITY GATE
```

The research strategy was deliberately conservative.

At each stage, the cheapest decisive prerequisite was tested before escalating to a full nonlinear field-equation solve.

The result is a substantially sharper picture of what is required for a physical realization of 006D.

The strongest established positive result remains 006D.

The strongest realizability-oriented positive preflight obtained in this slice is 016F.

The strongest new negative results are 016G and 016H.

The principal new physical conclusion is:

> **Producing negative active gravitational density is not sufficient to produce outward gravity. The spatial organization of negative and positive active stress relative to the gravitational Green-function kernel is essential.**

This journal does **not** claim:

* an exact nonlinear Einstein solution;
* a full Euler-Lagrange realization of 006D;
* full dynamical stability;
* a known material realization;
* finite-payload lift;
* experimental accessibility;
* practical antigravity;
* reactionless propulsion;
* discovery of new physics.

---

## Starting State

### Strongest established project result

Before this research slice, Simulation 006D had established:

> **Within static linearized general relativity, there exists an explicit finite-radius, finite-thickness, nonsingular, positive-energy, locally conserved type-I stress-energy configuration satisfying NEC, WEC, and DEC whose calculated near gravitational field points outward while its far-field active mass remains positive.**

The best tested finite coefficient was

```math
C_{\rm finite}
=
23.591586299249
```

in the scaling

```math
M_{\rm equiv}
=
C\frac{ah^2}{G}.
```

The independently obtained thin conserved reference was

```math
C_{\rm thin}
=
23.426710175391.
```

The 006D result therefore solved the following problem within its stated approximation:

```text
POSITIVE_ENERGY=
YES

NEC=
PASS

WEC=
PASS

DEC=
PASS

FINITE_RADIUS=
YES

FINITE_THICKNESS=
YES

LOCAL_CONSERVATION_LINEARIZED_ORDER=
YES

OUTWARD_LOCAL_GRAVITATIONAL_FIELD=
YES

POSITIVE_FAR_FIELD_ACTIVE_MASS=
YES
```

But it did not solve:

```text
ACTUAL_FIELD_REALIZATION=
NO

FULL_DYNAMIC_STABILITY=
NO

FULL_EULER_LAGRANGE_SOLUTION=
NO

NONLINEAR_EINSTEIN_MATTER_SOLUTION=
NO

FINITE_PAYLOAD_LIFT=
NO

PRACTICAL_ENERGY=
NO
```

---

## Relevant 006D Mathematics

For a local orthonormal type-I stress tensor,

```math
T_{\hat\mu\hat\nu}
=
\mathrm{diag}
\left(
\epsilon,
p_r,
p_\phi,
p_z
\right),
```

static linearized GR gives

```math
\nabla^2\Phi
=
\frac{4\pi G}{c^2}
\left(
\epsilon+p_r+p_\phi+p_z
\right).
```

Define the active gravitational source

```math
S
=
\epsilon+p_r+p_\phi+p_z.
```

The physical acceleration is

```math
\mathbf a
=
-\nabla\Phi.
```

For an axisymmetric source and an on-axis target at height $h$,

```math
a_z(h)
=
-\frac{2\pi G}{c^2}
\int dz
\int_0^\infty dr\,
rS(r,z)
\frac{h-z}
{\left[
r^2+(h-z)^2
\right]^{3/2}}.
```

Repository sign convention:

```text
a_z > 0
OUTWARD

a_z < 0
INWARD
```

Define the positive kernel

```math
K_h(r,z)
=
\frac{h-z}
{\left[
r^2+(h-z)^2
\right]^{3/2}}.
```

Then outward gravity requires

```math
\boxed{
\int S K_h\,dV<0
}
```

while positive far-field active mass requires

```math
\boxed{
\int S\,dV>0.
}
```

The fact that both can hold simultaneously is the key spatial mechanism behind 006D.

---

## Existing Field-Realization Context Before 016A

The 008 series had already established several important constraints.

### Canonical scalar algebraic representability

For static canonical real scalars,

```math
T_{ij}
=
M_{ij}
-
\rho\delta_{ij},
```

with local Gram entries

```math
M_{ii}
=
\rho+p_i.
```

Because 006D satisfies DEC, the local scalar Gram matrix can be positive semidefinite.

Therefore:

```text
LOCAL_CANONICAL_SCALAR_ALGEBRAIC_REPRESENTABILITY=
YES
```

but this did not imply a global field solution.

### Pure static canonical Derrick instability

For a static canonical scalar configuration,

```math
E(\lambda)
=
\frac{K}{\lambda}
+
\frac{U}{\lambda^3}.
```

At the stationary point,

```math
E''(1)
=
-3E.
```

For positive total energy,

```text
PURE_STATIC_CANONICAL_SCALAR_DERRICK_STABLE=
NO
```

so some stabilizing sector was required.

### Fixed-charge stabilization capacity

For a stationary charged scalar,

```math
D
=
\sum_a \dot\phi_a^2,
```

and

```math
T
=
\frac{D}{2}.
```

At fixed conserved charge,

```math
E_Q(\lambda)
=
\lambda^3T
+
\frac{K}{\lambda}
+
\frac{U}{\lambda^3}.
```

The dilation curvature is

```math
E_Q''(1)
=
24T-3E-5P.
```

With approximately vanishing integrated pressure,

```math
P\approx0,
```

one-mode stability requires

```math
\boxed{
\frac{T}{E}
>
\frac18
}.
```

The original fine 006D source had

```text
TMAX/E≈0.186185265139
```

which exceeded the threshold

```text
0.125
```

by a meaningful margin.

This established only **capacity** against one Derrick mode.

It did not establish full dynamic stability.

### Charge and winding must be separated

A single stationary winding complex scalar

```math
\Phi
=
f
e^{i(n\phi-\omega t)}
```

generates a nonzero temporal-angular stress component

```math
T_{t\phi}\neq0.
```

Because the 006D target is static and diagonal, the project concluded:

```text
ONE_CHARGED_WINDING_SCALAR_EXACT_REALIZATION=
INSUFFICIENT

TEMPORAL_CHARGE_AND_ANGULAR_WINDING_SECTORS=
MUST_BE_SEPARATED
```

### Ungauged compact winding termination fails

The original exact compact outer collar required a winding burden that diverged near the edge.

Therefore:

```text
FINITE_UNGAUGED_WINDING_SET_EXACT_COMPACT_TERMINATION=
NO

GAUGE_OR_OTHER_COMPENSATING_SECTOR_REQUIRED=
YES
```

### Local gauge takeover exists

A local scalar-plus-gauge stress decomposition was found in 008F.

A finite interval of gauge takeover remained compatible with the fixed-charge Derrick capacity.

However:

```text
GLOBAL_SMOOTH_GAUGE_POTENTIALS=
NOT_ESTABLISHED
```

This unresolved global issue became a principal focus of the 016 series.

---

# Work Performed

# 1. Simulation 016A — practicality-optimized thickness

## Scientific question

The original 006D source approached the thin conserved optimum as its thickness decreased.

But the mathematically optimal thin limit also produced the most extreme peak stresses and smallest geometric features.

016A asked:

> **Is the thin limit actually the best target for physical realization?**

The answer was:

```text
NO
```

---

## Thickness scan

The finite 006D source was re-evaluated at larger thicknesses.

Results:

```text
DELTA=0.40000

C=
38.037638025730

C_PENALTY_VS_FINE=
1.612339x

PEAK_STRESS_RELIEF=
2635.703x

FEATURE_WIDTH_GAIN=
64x
```

```text
DELTA=0.20000

C=
29.559369544823

C_PENALTY_VS_FINE=
1.252962x

PEAK_STRESS_RELIEF=
832.525x

FEATURE_WIDTH_GAIN=
32x
```

```text
DELTA=0.10000

C=
26.258214373557

C_PENALTY_VS_FINE=
1.113033x

PEAK_STRESS_RELIEF=
232.093x

FEATURE_WIDTH_GAIN=
16x
```

For comparison:

```text
DELTA=0.00625

C=
23.591586299249
```

The peak stress scales approximately as

```math
\epsilon_{\rm peak}
\propto
\frac{1}{h\delta^2}.
```

Thus increasing $\delta$ from the original fine value can reduce the local stress requirement by hundreds or thousands of times while increasing $C$ only by an order-unity factor.

The practical realization bracket was therefore shifted toward

```text
DELTA≈0.10_TO_0.20.
```

---

## 016A macroscopic area-energy result

A single 006D cell has energy

```math
E_{\rm cell}
=
C\frac{ah^2c^2}{G}.
```

Its geometric footprint is approximately

```math
A_{\rm cell}
=
\pi x_{\max}^2h^2.
```

Therefore

```math
\boxed{
\frac{E_{\rm cell}}
{A_{\rm cell}}
=
\frac{
Cac^2
}{
\pi x_{\max}^2G
}
}.
```

The factor $h^2$ cancels exactly.

This proves an important no-free-lunch result for simple geometric tiling:

> **Reducing the stand-off distance decreases the energy per individual cell, but increases the number of cells required to cover a fixed macroscopic area by the same inverse factor.**

Thus simple microstandoff does not solve the macroscopic energy problem.

The tested $1g$ source class remains of order

```text
~4.5e27 TO 5.2e27 J/m^2
```

of covered area.

This corresponds to an equivalent mass surface density of order

```text
~5e10 kg/m^2.
```

### 016A result

```text
THIN_LIMIT_IS_BEST_PRACTICAL_REALIZATION_TARGET=
NO

PREFERRED_THICKNESS_REGION=
DELTA_0P10_TO_0P20

MICROSTANDOFF_SOLVES_MACROSCOPIC_AREA_ENERGY=
NO

PURE_GR_AH2_OVER_G_SCALING=
PRESERVED
```

---

# 2. Simulation 016B — thick charge/gauge capacity

## Scientific question

016A greatly reduced peak stress, but the thicker geometry could have destroyed the earlier fixed-charge stabilization or gauge-support window.

016B therefore asked:

> **Does the more physically realizable thick 006D source retain the stabilization capacity found in 008C/008F?**

The answer was:

```text
YES
```

Representative results:

```text
DELTA=0.10

TMAX/E=
0.185636803730
```

```text
DELTA=0.20

TMAX/E=
0.185067450146
```

Both remain above

```math
\frac18
=
0.125.
```

The 30% and 35% gauge-takeover windows also survived.

Representative 30% takeover:

```text
DELTA=.10

T/E≈0.14566

CURVATURE/E≈0.49586
```

```text
DELTA=.20

T/E≈0.14533

CURVATURE/E≈0.48804
```

Therefore the hundreds-fold peak-stress reduction did not materially consume the fixed-charge stabilization budget.

### 016B result

```text
THICK_006D_FIXED_CHARGE_STABILITY_WINDOW=
SURVIVES

THICK_006D_GAUGE_WINDOW=
SURVIVES

016A_THICK_REALIZATION_TARGET=
PROMOTED
```

---

# 3. Simulation 016C — global gauge integrability

## Scientific question

008F had established a local gauge stress decomposition.

016C asked whether the simplest exact global electrostatic realization could exist.

The tested local gauge target was

```math
T_g
=
(g,0,g,0)
```

in the ordering

```text
(epsilon, p_r, p_phi, p_z).
```

For two independent electrostatic potentials, exact stress matching requires

```math
\sum_a E_{r,a}^2
=
g,
```

```math
\sum_a E_{z,a}^2
=
g,
```

and

```math
\sum_a E_{r,a}E_{z,a}
=
0.
```

Therefore the Jacobian $J$ of the two potentials satisfies

```math
J^TJ
=
gI.
```

This is a local conformal map with scale

```math
\sqrt g.
```

A necessary integrability condition is

```math
\boxed{
\left(
\partial_r^2
+
\partial_z^2
\right)
\ln g
=
0
}
```

where $g>0$.

---

## Application to the compact 006D collar

The original outer-collar gauge target has the form

```math
g(r,z)
\propto
\frac{
v(1-v)
}{r}
y^2(1-y)^2
```

with radial transition coordinate $v$ and vertical coordinate $y$.

Then

```math
\Delta\ln g
=
\frac1{r^2}
-
\frac1{\delta^2}
\left[
\frac1{v^2}
+
\frac1{(1-v)^2}
+
\frac2{y^2}
+
\frac2{(1-y)^2}
\right].
```

At

```math
v=y=\frac12,
```

this becomes

```math
\boxed{
\Delta\ln g
=
\frac1{r^2}
-
\frac{24}{\delta^2}
<
0.
}
```

Thus the harmonicity condition fails.

Numerical finite differences independently reproduced the analytic result.

Representative values:

```text
DELTA=.10

MAX_DELTA_LOG_G≈
-2.39996e3
```

```text
DELTA=.20

MAX_DELTA_LOG_G≈
-5.99957e2
```

```text
DELTA=.40

MAX_DELTA_LOG_G≈
-1.49958e2
```

### 016C result

```text
TWO_INDEPENDENT_STATIC_ELECTROSTATIC_U1_EXACT_GLOBAL_TARGET=
REJECTED_BY_CONFORMAL_INTEGRABILITY

008F_LOCAL_GAUGE_STRESS_DECOMPOSITION=
PRESERVED

006D_GRAVITATIONAL_CONSTRUCTION=
NOT_INVALIDATED
```

This rejected only the simplest exact electrostatic realization.

It did not reject general gauged scalar sectors, magnetic configurations, time-dependent fields, or larger gauge multiplets.

---

# 4. Simulation 016D — exponential-tail realizability

## Scientific question

The exact compact boundary itself could be creating much of the field-realization difficulty.

016D therefore relaxed exact compact support while preserving:

* local conservation;
* finite total energy;
* outward gravitational field;
* integrated stress balance;
* fixed-charge capacity.

The original 006D theorem remained unchanged.

016D defined a separate realization-oriented stress target.

---

## Radial exponential tail

Let

```math
x
=
\frac{r-\beta}{\ell}.
```

Define

```math
f(x)
=
\exp
\left[
-\frac{x^3}
{1+x^2}
\right].
```

This satisfies

```math
f(0)=1,
```

```math
f'(0)=0,
```

```math
f''(0)=0,
```

and asymptotically

```math
f(x)\sim e^{-x}.
```

Use

```math
q(r)
=
-\frac{\alpha^2}{r}
f
\left(
\frac{r-\beta}{\ell}
\right).
```

The stress construction remains

```math
p_r
=
\frac qr
```

and

```math
p_\phi
=
q'.
```

Therefore radial conservation remains exact at the linearized flat-background level.

Because

```math
q(r)\rightarrow0
```

exponentially,

```math
\int
r(p_r+p_\phi)
\,dr
=
[rq]_0^\infty
=
0.
```

Thus integrated spatial stress cancellation survives.

---

## Smooth vertical profile

The original compact polynomial vertical profile was replaced by

```math
\varphi(z)
=
\frac1{2w}
\mathrm{sech}^2
\left(
\frac{z-z_0}{w}
\right)
```

with

```math
z_0
=
-\frac\delta2
```

and

```math
w
=
\frac\delta4.
```

This profile has finite logarithmic derivatives and exponential vertical localization.

---

## 016D results

All tested cases retained:

```text
OUTWARD_GRAVITATIONAL_FIELD=
YES

INTEGRATED_STRESS_TRACE=
PASS

FIXED_CHARGE_DERRICK_WINDOW=
SURVIVES

FINITE_TOTAL_ENERGY=
YES
```

Representative candidate:

```text
DELTA=.20

ELL=.40

C=
29.47048944

TMAX/E=
0.179076443

PEAK_STRESS_RELIEF_VS_FINE_006D≈
1868x
```

At this stage the exponential tail appeared to be a strong physical-realization target.

016E then identified a deeper asymptotic gauge-energy obstruction.

---

# 5. Simulation 016E — two-sector gauge-tail asymptotic preflight

## Scientific question

For a winding scalar with amplitude $F(r)$ and gauge-covariant winding mismatch

```math
k(r)
=
n-eA_\phi(r),
```

the angular-gradient stress is

```math
A(r)
=
\frac{
k(r)^2F(r)^2
}{r^2}.
```

Let the available radial gradient budget be

```math
G_r(r).
```

Because

```math
F'^2
\le
G_r
```

and finite energy requires

```math
F(\infty)=0,
```

one has the amplitude bound

```math
F(r)
\le
I(r)
```

where

```math
I(r)
=
\int_r^\infty
\sqrt{G_r(s)}
\,ds.
```

Therefore exact angular-stress matching requires

```math
\boxed{
|k(r)|
\ge
K_{\min}(r)
=
\frac{
r\sqrt{A(r)}
}{
I(r)
}
}.
```

This is a necessary kinematic condition independent of the detailed self-potential.

---

# 6. 016E exponential-tail obstruction

For the 016D exponential tail,

```math
f(r)
\sim
e^{-r/\ell}.
```

The target asymptotically gives

```math
G_r
\sim
C
\frac{
e^{-r/\ell}
}{r}
```

and approximately

```math
A
\sim
2G_r.
```

The amplitude integral behaves as

```math
I(r)
\sim
2\ell
\sqrt{G_r}.
```

Therefore

```math
\boxed{
K_{\min}(r)
\sim
\frac{
r
}{
\sqrt2\,\ell
}
}.
```

Hence

```math
K_{\min}'(r)
\rightarrow
\frac1{\sqrt2\,\ell}.
```

For cylindrical gauge mismatch

```math
k
=
n-eA_\phi,
```

the axial magnetic field contains

```math
B_z
\propto
-\frac{k'}{er}.
```

The magnetic energy therefore contains an asymptotic contribution proportional to

```math
\int
\frac{
k'(r)^2
}{r}
\,dr.
```

If $k'$ approaches a nonzero constant, this behaves as

```math
\int^\infty
\frac{dr}{r}
```

and diverges logarithmically.

Therefore the exact 016D exponential tail cannot be realized by the tested minimal single gauged-winding sector with finite asymptotic magnetic energy.

### 016E exponential result

```text
EXPONENTIAL_TAIL_SINGLE_GAUGED_WINDING_FINITE_ENERGY_ASYMPTOTIC=
REJECTED
```

This did not invalidate the 016D stress-energy construction.

It rejected that tail only as the exact target for the minimum gauged-winding realization.

---

# 7. 016E power-law-tail escape

A new $C^2$ power-law tail was introduced:

```math
f_m(x)
=
\left(
1+x^3
\right)^{-m/3}.
```

It satisfies

```math
f_m(0)=1,
```

```math
f_m'(0)=0,
```

```math
f_m''(0)=0,
```

and

```math
f_m(x)
\sim
x^{-m}
```

for large $x$.

For this class the asymptotic required gauge mismatch tends to a finite constant:

```math
\boxed{
K_\infty
=
\sqrt{
\frac{
m(m+1)
}{2}
}
}.
```

Examples:

```text
M=2

K_INFINITY=
sqrt(3)
≈1.73205
```

```text
M=3

K_INFINITY=
sqrt(6)
≈2.44949
```

```text
M=4

K_INFINITY=
sqrt(10)
≈3.16228
```

The asymptotic magnetic-energy obstruction found for the exponential tail is therefore absent.

All tested power-law cases retained:

```text
OUTWARD_GRAVITATIONAL_FIELD=
YES

INTEGRATED_STRESS_TRACE=
PASS

FIXED_CHARGE_DERRICK_WINDOW=
SURVIVES
```

Representative $m=2$ candidate:

```text
DELTA=.20

ELL=.40

C=
29.552822107488

TMAX/E=
0.177926001088

K_INFINITY=
1.732050807569

PEAK_STRESS_RELIEF_VS_FINE_006D=
1874.913x
```

### 016E result

```text
EXPONENTIAL_TAIL=
DEMOTED_AS_MINIMAL_GAUGED_WINDING_TARGET

C2_POWER_LAW_TAIL=
PROMOTED_KINEMATICALLY
```

This remained a stress-level preflight.

It was not yet a solution of the matter Euler-Lagrange equations.

---

# 8. Simulation 016F — simultaneous charge/winding coexistence

## Scientific question

The fixed-charge stabilization and winding-sector tests had previously been treated mostly independently.

But in a genuine matter configuration they compete for the same stress-energy budget.

After allocating temporal kinetic energy $D$ to the charged stabilizer, the remaining radial and angular scalar Gram budgets become

```math
G_r
=
\epsilon+p_r-D
```

and

```math
A
=
\epsilon+p_\phi-D.
```

This coupling had to be tested before a field-equation solve.

---

## Inner winding turn-on

If the winding amplitude starts from zero at the beginning of the inner transition,

```math
F(r_-)=0,
```

and

```math
F'^2\le G_r,
```

then

```math
F(r)
\le
\int_{r_-}^{r}
\sqrt{G_r(s)}
\,ds.
```

Angular stress matching requires

```math
\frac{k^2F^2}{r^2}
=
A.
```

Therefore

```math
\boxed{
K_{\rm inner}(r)
=
\frac{
r\sqrt{A(r)}
}{
\displaystyle
\int_{r_-}^{r}
\sqrt{G_r(s)}
\,ds
}
}
```

is a necessary mismatch bound.

---

## Outer decay

Finite energy requires the winding amplitude to return to zero asymptotically.

Therefore

```math
F(r)
\le
\int_r^\infty
\sqrt{G_r(s)}
\,ds
```

and hence

```math
\boxed{
K_{\rm outer}(r)
=
\frac{
r\sqrt{A(r)}
}{
\displaystyle
\int_r^\infty
\sqrt{G_r(s)}
\,ds
}
}.
```

The global minimum required mismatch is therefore at least

```math
\boxed{
K_{\rm required}
=
\max
\left(
K_{\rm inner},
K_{\rm outer}
\right).
}
```

---

# 9. 016F hidden narrow-transition bottleneck

For the narrow inherited transition

```text
W=.05

ELL=.40
```

and target stabilization

```text
T/E=.14,
```

016F found

```text
INNER_K_MAX≈
130.6109

OUTER_K_MAX≈
13.0870

K_REQUIRED≈
130.6109
```

which corresponds to a conservative nonovershooting integer winding

```text
N≈131.
```

This showed that the far tail was no longer the dominant problem.

The dominant difficulty was the **rapid inner turn-on of the angular stress**.

---

# 10. 016F transition-broadening result

The old inner smoothing half-width was freed from

```math
W=\frac\delta4.
```

The source was scanned over substantially broader inner transitions.

This allowed the winding amplitude to grow gradually over a larger radial region.

The required gauge mismatch fell dramatically.

Preferred low-complexity tested point:

```text
W=
1.000000000000

ELL=
0.600000000000

M=
2

C=
40.749886771113

TMAX/E=
0.180278569163

TARGET_T/E=
0.140000000000

ETA_FOR_TARGET_CHARGE=
0.776575943831

DERRICK_CURVATURE/E=
+0.360000

K_REQUIRED=
9.589406109611

CONSERVATIVE_INTEGER_WINDING=
10

PEAK_STRESS_RELIEF_VS_FINE_006D=
1400.489001x
```

Thus the hardest tested charge/winding requirement fell from approximately

```text
K≈130
```

to approximately

```text
K≈9.59
```

while preserving:

* outward gravitational field;
* integrated stress balance;
* positive energy;
* DEC construction;
* a meaningful fixed-charge margin;
* approximately $1400\times$ peak-stress relief.

This was a strong constructive improvement.

### 016F result

```text
FINITE_CHARGE_WINDING_COEXISTENCE_WINDOW=
YES_IN_TESTED_KINEMATIC_ALLOCATION

LOWER_COMPLEXITY_NONOVERSHOOT_TARGET=
YES

PREFERRED_CONSERVATIVE_WINDING=
10
```

However, 016F remained a **kinematic stress-budget result**.

It did not prove that an actual canonical field satisfying its Euler-Lagrange equations could realize the target.

That question became 016G.

---

# 11. Simulation 016G — asymptotic Euler-Lagrange gate

## Scientific question

016G asked:

> **Can the exact 016E/016F power-law target satisfy the asymptotic Euler-Lagrange equation of the minimum asymptotically decoupled canonical winding field with a regular stable vacuum?**

This was tested analytically before launching a large PDE solve.

The result was a clean asymptotic no-go under the stated assumptions.

---

# 12. 016G mathematical proof

Consider an $m$-power target tail.

Asymptotically,

```math
q(r)
\propto
-r^{-m-1}.
```

Therefore

```math
p_r
\sim
-C_\infty
r^{-m-2}
```

and

```math
p_\phi
\sim
(m+1)
C_\infty
r^{-m-2}.
```

In the target tail,

```math
\epsilon
=
p_\phi.
```

Therefore the unallocated radial scalar Gram capacity is

```math
\epsilon+p_r
\sim
mC_\infty
r^{-m-2}.
```

Allocate a fraction $\eta$ of that capacity to temporal charge:

```math
D
=
\eta
mC_\infty
r^{-m-2}.
```

The remaining radial gradient capacity is

```math
\boxed{
G_r
\sim
(1-\eta)
mC_\infty
r^{-m-2}
}.
```

The required remaining angular Gram component is

```math
\boxed{
A
\sim
\left[
2(m+1)
-
\eta m
\right]
C_\infty
r^{-m-2}.
}
```

---

## Slowest possible finite-energy amplitude

The winding amplitude obeys

```math
F'^2
\le
G_r.
```

Finite energy requires

```math
F(\infty)=0.
```

Therefore

```math
F(r)
\le
\int_r^\infty
\sqrt{G_r(s)}
\,ds.
```

Since

```math
\sqrt{G_r}
\propto
r^{-(m+2)/2},
```

the integral behaves as

```math
r^{-m/2}.
```

Thus the slowest allowed finite-energy power-law amplitude is

```math
F
\propto
r^{-s}
```

with

```math
\boxed{
s=\frac m2.
}
```

Any faster power-law decay has

```math
s>\frac m2.
```

---

## Minimum asymptotic winding mismatch

The angular-gradient requirement is

```math
\frac{
k^2F^2
}{r^2}
=
A.
```

Using the largest kinematically allowed amplitude gives the smallest possible asymptotic mismatch.

This yields

```math
\boxed{
k_\infty^2
\ge
\frac{
m
\left[
2(m+1)-\eta m
\right]
}{
4(1-\eta)
}.
}
```

Because

```math
s^2
=
\frac{m^2}{4},
```

subtracting gives

```math
k_\infty^2-s^2
=
\frac{
m
\left[
2(m+1)-\eta m
\right]
}{
4(1-\eta)
}
-
\frac{m^2}{4}.
```

Using a common denominator,

```math
k_\infty^2-s^2
=
\frac{
m
\left[
2(m+1)
-
\eta m
-
m(1-\eta)
\right]
}{
4(1-\eta)
}.
```

The $\eta m$ terms cancel:

```math
2(m+1)-\eta m-m+\eta m
=
m+2.
```

Therefore

```math
\boxed{
k_\infty^2-s^2
=
\frac{
m(m+2)
}{
4(1-\eta)
}.
}
```

For

```math
m>0
```

and

```math
0\le\eta<1,
```

both numerator and denominator are positive.

Therefore

```math
\boxed{
k_\infty^2>s^2.
}
```

This result is exact within the stated asymptotic assumptions.

---

# 13. 016G Euler-Lagrange sign conflict

For a gapless canonical asymptotically decoupled winding amplitude,

```math
F''
+
\frac1rF'
-
\frac{k^2}{r^2}F
-
U_{\rm eff}'(F)
=
0.
```

For

```math
F
=
Ar^{-s},
```

one has

```math
F'
=
-sAr^{-s-1}
```

and

```math
F''
=
s(s+1)Ar^{-s-2}.
```

Therefore

```math
F''
+
\frac1rF'
=
s^2Ar^{-s-2}
=
\frac{s^2}{r^2}F.
```

The Euler-Lagrange equation then requires

```math
U_{\rm eff}'(F)
=
\frac{
s^2-k^2
}{r^2}
F.
```

But the previous identity gives

```math
k^2>s^2.
```

Therefore

```math
\boxed{
U_{\rm eff}'(F)<0
}
```

for sufficiently small positive $F$.

For a regular asymptotically decoupled canonical scalar whose vacuum at $F=0$ is a stable local minimum, the leading restoring potential force sufficiently near the vacuum has the opposite sign.

Thus the exact power-law target is incompatible with that minimal field class.

---

# 14. Preferred 016F numerical specialization

For the preferred 016F point,

```text
M=
2

ETA≈
0.77657594383
```

and therefore

```math
s
=
\frac m2
=
1.
```

The reconstructed asymptotic mismatch was

```text
K_INFINITY≈
3.154613692967.
```

Hence

```text
K_INFINITY^2-S^2≈
+8.951587551854
```

and

```text
S^2-K_INFINITY^2≈
-8.951587551854.
```

For $m=2$, the corresponding lowest matching local nonlinearity is quartic.

The required effective quartic coefficient has the negative sign.

A stable standalone decoupled quartic vacuum requires the positive sign.

The finite-difference Euler-Lagrange check independently recovered approximately

```text
-8.95158755
```

at radii

```text
10
100
1000
10000
```

with relative errors approximately $10^{-10}$ to $10^{-9}$.

Therefore the sign conflict was not a symbolic algebra artifact.

---

# 15. Charge does not create the 016G obstruction

The no-charge control used

```text
ETA=0.
```

For $m=2$,

```text
K_INFINITY=
1.732050807569
```

and

```text
K^2-S^2=
2.
```

Thus the asymptotic obstruction already exists without temporal charge.

Temporal charge increases the mismatch but does not create the no-go.

Therefore:

```text
TEMPORAL_CHARGE_CREATES_OBSTRUCTION=
NO

TEMPORAL_CHARGE_WORSENS_OBSTRUCTION=
YES
```

Removing the stabilizing charge alone cannot rescue the exact power-law target.

---

# 16. Faster power-law decay does not rescue the exact target

If

```math
s>\frac m2,
```

exact angular matching requires

```math
k^2
\propto
r^{2s-m}.
```

Because

```math
2s-m>0,
```

the angular term eventually dominates the positive radial-Laplacian contribution.

The 016G controls showed increasingly negative residuals for faster decays.

Therefore:

```text
FASTER_POWER_LAW_DECAY_RESCUES_STABLE_SELF_POTENTIAL=
NO
```

under the tested assumptions.

---

# 17. 016G result

The proper classification is narrow:

```text
MINIMAL_ASYMPTOTICALLY_DECOUPLED_CANONICAL_WINDING_EXACT_POWER_LAW_TARGET=
REJECTED

REJECTION_REASON=
EULER_LAGRANGE_FORCE_SIGN_CONFLICT

006D_GRAVITATIONAL_CONSTRUCTION=
PRESERVED

016F_KINEMATIC_CHARGE_WINDING_COEXISTENCE=
PRESERVED

GLOBAL_FIELD_SOLUTION=
NOT_ESTABLISHED
```

This is **not** a universal no-go theorem against canonical field realizations of repulsive gravity.

It rejects the exact tested power-law target in the minimum asymptotically decoupled canonical winding class.

Possible logical escapes include:

* relax exact stress matching;
* allow an additional asymptotically coupled field;
* enlarge the field multiplet;
* introduce justified noncanonical kinetic structure;
* alter the spatial stress architecture;
* solve the actual field equations with outward gravity as the optimization objective rather than exact $T_{\mu\nu}$ matching.

016H tested the most conservative next escape:

```text
RELAX_EXACT_STRESS_MATCHING.
```

---

# 18. Simulation 016H — explicit canonical field gravity gate

## Scientific question

016H asked:

> **If an explicit healthy local relativistic field model is allowed to determine its own stress-energy by fixed-charge energy minimization, can it naturally generate an outward gravitational field without being forced to reproduce the engineered 006D tensor?**

This represented an important methodological change.

The matter equations were allowed to choose the stress tensor.

The observable of interest was the gravitational field itself.

---

# 19. 016H model

The tested model was inspired by the general logic of Friedberg-Lee-Sirlin/Q-ball-type scalar localization.

It contained:

1. one real symmetry-breaking scalar $X$;
2. two complex fields with equal temporal frequency and opposite winding.

The counter-winding ansatz was

```math
\Phi_+
=
Y(r,z)
e^{i(\omega t+n\phi)}
```

and

```math
\Phi_-
=
Y(r,z)
e^{i(\omega t-n\phi)}.
```

Their angular momentum densities cancel, giving

```math
T_{t\phi,\rm total}=0.
```

The potential was chosen nonnegative:

```math
V
=
\frac{\mu}{4}
\left(
1-X^2
\right)^2
+
X^2
\left(
|\Phi_+|^2
+
|\Phi_-|^2
\right).
```

The vacuum is

```math
X=\pm1,
```

```math
\Phi_\pm=0.
```

The gauge field was deliberately omitted.

This makes 016H an optimistic gravitational-sign preflight because ordinary Maxwell field energy would add additional positive active gravitational source.

---

# 20. 016H variational fields

The real scalar used

```math
X
=
1
-
A
\exp
\left[
-\frac12
\left(
\frac{r^2}{R_X^2}
+
\frac{z^2}{Z_X^2}
\right)
\right].
```

The winding amplitude used

```math
Y
=
B
\left(
\frac r{R_Y}
\right)^n
\exp
\left[
-\frac12
\left(
\frac{r^2}{R_Y^2}
+
\frac{z^2}{Z_Y^2}
\right)
\right].
```

The factor

```math
r^n
```

enforces regularity on the symmetry axis.

Independent widths

```text
R_X
Z_X
R_Y
Z_Y
```

allowed partial spatial separation between the wall-like and charge/winding sectors.

The total charge was held fixed.

Energy was minimized variationally over the field widths and amplitudes.

The free-particle threshold in the chosen units was

```text
E/Q=1.
```

Promoted bound states required

```math
E/Q<1.
```

---

# 21. 016H active gravitational source identity

For the explicit counter-winding scalar model, the combination

```math
S
=
\rho+p_r+p_\phi+p_z
```

simplifies exactly to

```math
\boxed{
S
=
8\omega^2Y^2
-
2V.
}
```

The spatial gradient terms cancel from the active trace.

This result exposed the gravitational competition directly:

```text
TEMPORAL_CHARGE_ENERGY:
POSITIVE_ACTIVE_SOURCE

SCALAR_POTENTIAL / TENSION:
NEGATIVE_ACTIVE_SOURCE
```

Thus the model genuinely had the ability to create regions with

```math
S<0.
```

The question was whether the spatial distribution generated by equilibrium could make the kernel-weighted integral negative.

---

# 22. 016H gravitational observable

The on-axis gravitational acceleration is proportional to

```math
a_z(h)
\propto
-
\int
S(r,z)
\frac{h-z}
{\left[
r^2+(h-z)^2
\right]^{3/2}}
\,dV.
```

No 006D stress tensor was imposed.

The fields chose their own configuration through variational energy minimization.

Two regions were tested:

```text
NEAR_FIELD
```

and a cleaner exterior region beginning at approximately

```text
H>=3 TIMES THE LARGEST VERTICAL FIELD WIDTH.
```

This separated the questions:

```text
DO_NEGATIVE_ACTIVE_DENSITY_REGIONS_EXIST?

DOES_LOCAL_OUTWARD_GRAVITY_EXIST?

DOES_CLEAN_EXTERIOR_OUTWARD_GRAVITY_EXIST?
```

---

# 23. 016H scan

Parameters were scanned over:

```text
MU=
0.1
0.3
1.0
3.0
```

```text
Q=
1000
3000
10000
30000
```

```text
N=
1
2
3
4
5
```

The variational optimizer produced

```text
63
```

promoted bound states.

All 63 passed the run's internal consistency checks.

---

# 24. 016H results

Global summary:

```text
PROMOTED_BOUND_CASES=
63

INTERNALLY_CONSISTENT_BOUND_CASES=
63

NEGATIVE_ACTIVE_DENSITY_EXISTS=
True

ANY_NEAR_FIELD_OUTWARD_ACCELERATION=
False

ANY_CLEAN_EXTERIOR_OUTWARD_ACCELERATION=
False
```

The largest negative active-density fraction relative to total energy was

```text
0.266601491354
```

or approximately

```text
26.66%.
```

Despite this substantial negative active source, the gravitational field remained inward.

The best exterior case was

```text
MU=
0.1

Q=
1000

N=
1

E/Q=
0.626576773261
```

with

```text
EXTERIOR_MAX_A_KERNEL=
-0.7702175806711
```

which is inward under the repository convention.

---

# 25. Independent 016H force-sign validation

The best exterior case was re-evaluated at quadrature orders:

```text
64
96
128.
```

Results:

```text
ORDER=64

EXTERIOR_MAX_A≈
-0.770217580671
```

```text
ORDER=96

EXTERIOR_MAX_A≈
-0.770217579488
```

```text
ORDER=128

EXTERIOR_MAX_A≈
-0.770217579488
```

The force sign therefore remained stable under substantial quadrature refinement.

The high-order consistency measures were approximately:

```text
ACTIVE_MASS/E≈
0.9999999953
```

and

```text
PRESSURE_TRACE/E≈
-4.66e-9.
```

The direct and closed-form active-source expressions agreed to machine precision.

Therefore the negative 016H force result is not plausibly explained by coarse integration error.

---

# 26. 016H result

```text
EXPLICIT_CANONICAL_FIELD_VARIATIONAL_EXTERIOR_REPULSION=
NOT_FOUND_IN_TESTED_SCAN

EXPLICIT_CANONICAL_FIELD_VARIATIONAL_NEAR_FIELD_REPULSION=
NOT_FOUND_IN_TESTED_SCAN

NEGATIVE_ACTIVE_DENSITY_WITHOUT_REPULSIVE_FIELD=
YES
```

Interpretation:

```text
GENERIC_COUNTERWINDING_FLS_LIKE_EQUILIBRIA=
DO_NOT_AUTOMATICALLY_INHERIT_006D_REPULSION
```

This does not prove a universal theorem against all FLS-like, Q-ball-like, vorton-like, or canonical scalar field configurations.

It is a strong negative result for the tested co-spatial variational family.

---

# Result

The 016A–016H sequence substantially narrowed the physical-realization problem.

## Positive results

```text
016A_THICKER_REALIZATION_TARGET=
GREEN

016A_PEAK_STRESS_RELIEF=
HUNDREDS_TO_THOUSANDS_FOLD

016B_FIXED_CHARGE_CAPACITY=
PRESERVED

016B_LOCAL_GAUGE_WINDOW=
PRESERVED

016D_SMOOTH_NONCOMPACT_STRESS_TARGET=
GREEN

016E_POWER_LAW_GAUGE_ASYMPTOTIC=
GREEN_KINEMATICALLY

016F_SIMULTANEOUS_CHARGE_WINDING_COEXISTENCE=
GREEN_KINEMATICALLY

016F_LOW_COMPLEXITY_TARGET=
N_APPROX_10
```

## Negative results

```text
016C_SIMPLE_GLOBAL_ELECTROSTATIC_EXACT_TARGET=
REJECTED

016E_EXPONENTIAL_MINIMAL_GAUGED_WINDING_TARGET=
REJECTED

016G_EXACT_MINIMAL_CANONICAL_POWER_LAW_TARGET=
REJECTED

016H_GENERIC_COUNTERWINDING_FLS_LIKE_REPULSION=
NOT_FOUND
```

## Preserved central result

```text
006D_CONSTRUCTIVE_LINEARIZED_GR_REPULSION=
PRESERVED
```

Nothing in 016A–016H invalidated the original 006D gravitational construction.

---

# New Physical Principle Identified by 006D vs 016H

The deepest new lesson is not merely that some matter models fail.

It is that **negative active gravitational density alone is insufficient**.

Let

```math
S
=
S_-+S_+
```

with

```math
S_-\le0
```

and

```math
S_+\ge0.
```

Positive asymptotic active mass requires

```math
\int S_+\,dV
>
\left|
\int S_-\,dV
\right|.
```

Yet outward near-field gravity requires

```math
\int K_hS_+\,dV
<
\left|
\int K_hS_-\,dV
\right|.
```

These conditions can coexist only if the negative and positive parts are spatially arranged differently relative to the kernel.

The kernel

```math
K_h(r,z)
=
\frac{h-z}
{\left[
r^2+(h-z)^2
\right]^{3/2}}
```

is largest close to the target-facing source region and weaker at larger radial distance.

Therefore the useful source architecture is qualitatively:

```text
NEGATIVE_ACTIVE_STRESS:
CONCENTRATED NEAR THE HIGH-KERNEL CENTRAL REGION

POSITIVE_COMPENSATING_ENERGY / SUPPORT:
MOVED TO A LOWER-KERNEL OUTER REGION
```

006D achieves this by construction.

016H did not.

016H produced negative active source, but the negative and positive contributions remained too co-spatial for the kernel-weighted integral to reverse sign.

The new design criterion is therefore:

```math
\boxed{
\int S\,dV>0
}
```

while simultaneously

```math
\boxed{
\int S K_h\,dV<0.
}
```

This pair of conditions should guide future established-GR matter models.

---

# Verification

## Analytical

The following major analytical results were established in this research slice.

### 016A coverage scaling

```math
\boxed{
\frac{E}{A}
=
\frac{
Cac^2
}{
\pi x_{\max}^2G
}
}
```

for simple tiled cells.

Thus the stand-off scale cancels from the macroscopic area-energy requirement.

### 016C conformal integrability

For the simplest two-electrostatic-potential exact gauge target:

```math
J^TJ=gI
```

requires

```math
\boxed{
\Delta\ln g=0.
}
```

The compact 006D target violates this condition.

### 016E gauge mismatch bound

```math
\boxed{
|k(r)|
\ge
\frac{
r\sqrt A
}{
\displaystyle
\int_r^\infty
\sqrt{G_r}\,ds
}.
}
```

### 016E exponential asymptotic

```math
\boxed{
K_{\min}(r)
\sim
\frac r{\sqrt2\,\ell}
}
```

leading to logarithmically divergent minimal magnetic-energy scaling.

### 016E power-law asymptotic

```math
\boxed{
K_\infty
=
\sqrt{
\frac{
m(m+1)
}{2}
}.
}
```

### 016F simultaneous charge/winding requirement

```math
\boxed{
K_{\rm required}
=
\max
\left(
K_{\rm inner},
K_{\rm outer}
\right).
}
```

### 016G asymptotic no-go identity

```math
\boxed{
k_\infty^2-s^2
=
\frac{
m(m+2)
}{
4(1-\eta)
}
>0.
}
```

### 016H active-source identity

```math
\boxed{
S
=
8\omega^2Y^2
-
2V.
}
```

These equations define the core mathematical advances of the slice.

---

## Numerical

The project known-solution baseline remained

```text
94 passed
```

through the 016G run.

The final 016H source compiled after a one-line Python syntax repair and completed successfully.

The 016H syntax failure was not a scientific failure.

The invalid code form was equivalent to placing

```text
**1.5
```

on a new Python statement after a closed parenthesized expression.

The repair moved the exponent back onto the expression.

After repair:

```text
PATCH_RC=0

COMPILE_RC=0

RUN_RC=0
```

The scientific 016H result therefore comes from the repaired successful execution.

Independent 016H force evaluation at orders

```text
64
96
128
```

preserved the attractive sign.

---

## Dimensional

The primary 006D scaling remains

```math
M
=
C\frac{ah^2}{G}.
```

Since

```math
\left[
\frac{ah^2}{G}
\right]
=
{\rm kg},
```

the coefficient $C$ is dimensionless.

For the area-energy scaling,

```math
\frac EA
=
\frac{
Cac^2
}{
\pi x_{\max}^2G
}
```

has units

```math
{\rm J/m^2}.
```

The 016A cancellation of $h$ is therefore dimensionally consistent.

The 016G asymptotic relation

```math
k_\infty^2-s^2
=
\frac{
m(m+2)
}{
4(1-\eta)
}
```

is dimensionless, as required.

---

## Limiting cases

### 016A

As thickness decreases,

```math
\delta\rightarrow0,
```

the finite construction approaches the independent thin conserved coefficient.

Peak stress increases strongly in the same limit.

### 016E exponential tail

As

```math
r\rightarrow\infty,
```

the required gauge mismatch grows linearly, causing logarithmic magnetic-energy divergence in the minimum tested realization.

### 016E power-law tail

For

```math
r\rightarrow\infty,
```

the required gauge mismatch tends to a finite constant.

### 016G no-charge limit

At

```math
\eta=0,
```

the sign obstruction remains.

Thus it is not created by temporal-charge stabilization.

### 016G faster-decay limit

For

```math
s>\frac m2,
```

the angular term becomes increasingly dominant asymptotically and does not repair the sign problem.

### 016H far field

The internally consistent bound configurations had positive integrated active mass and remained gravitationally attractive in the tested exterior.

---

## Literature comparison

This slice focused primarily on project-derived mathematical and numerical tests.

The broad physical ingredients used here have known precedents:

* relativistic domain-wall tension;
* Q-ball / charged-soliton stabilization;
* winding scalar fields;
* gauged vortices and vortons;
* Friedberg-Lee-Sirlin-type localization mechanisms;
* active gravitational mass contributions from pressure.

However, this journal does **not** claim novelty for the exact 006D realization chain or the 016G asymptotic identity relative to the entire published literature.

Before any novelty claim, the following remain necessary:

1. dedicated literature search for finite positive-energy locally repulsive DEC-compatible linearized-GR stress constructions;
2. literature search for stress-moment design in gravitating solitons;
3. comparison of the 016G asymptotic obstruction against known gauged Q-ball/vorton asymptotics;
4. comparison of the 016H negative result against known gravitating FLS/Q-ball families;
5. independent external reconstruction of the principal equations and simulations.

Therefore:

```text
NOVELTY=
NOT_ESTABLISHED

NEW_PHYSICS_DISCOVERY=
NO
```

---

# Falsification Attempt

The research slice intentionally attempted to falsify the promising 006D realization route at increasingly realistic levels.

## 1. Could 006D require an impractically thin mathematical limit?

016A:

```text
NO
```

Thicker sources retained most of the gravitational efficiency while dramatically reducing peak stress.

---

## 2. Could thickening destroy the fixed-charge stabilization capacity?

016B:

```text
NO
```

The $T/E>1/8$ capacity survived with little degradation.

---

## 3. Could the local gauge decomposition simply be integrated into global electrostatic potentials?

016C:

```text
NO
```

The required conformal harmonicity condition fails for the exact tested target.

---

## 4. Could smoothing the compact boundary solve the gauge problem?

Partially.

016D showed:

```text
SMOOTH_TAIL=
YES
```

but 016E showed:

```text
EXPONENTIAL_MINIMAL_GAUGED_WINDING_ASYMPTOTIC=
NO
```

because of logarithmic magnetic-energy divergence.

---

## 5. Could a power-law tail solve the asymptotic gauge-energy problem?

016E:

```text
YES_KINEMATICALLY
```

The required mismatch tends to a finite constant.

---

## 6. Could simultaneous charge and winding consume the entire available stress budget?

016F:

```text
NO
```

A finite coexistence window exists.

A widened transition reduced the conservative winding burden from approximately $131$ to approximately $10$.

---

## 7. Could the exact power-law target satisfy the minimum canonical winding field equation?

016G:

```text
NO
```

The Euler-Lagrange force sign is incompatible with a regular stable decoupled vacuum under the stated assumptions.

---

## 8. Could relaxing exact stress matching allow a healthy field model to repel anyway?

016H tested this directly.

The model generated substantial negative active density.

But:

```text
NEAR_FIELD_REPULSION=
NOT_FOUND

EXTERIOR_REPULSION=
NOT_FOUND
```

in the tested 63-state bound variational family.

Thus negative active density by itself is insufficient.

---

## 9. Could 016H be a quadrature artifact?

The best exterior case was independently recomputed at quadrature orders

```text
64
96
128.
```

All retained the same attractive sign.

Therefore this specific failure mode is strongly disfavored.

---

## 10. Could 016G be merely a charge-allocation artifact?

No.

The no-charge control retained the asymptotic sign obstruction.

---

## 11. Could faster winding-amplitude decay rescue the 016G target?

No in the tested asymptotic argument.

The required angular term becomes even more dominant.

---

# Claims Status

The claims ledger should eventually be synchronized with the following durable records.

```text
CLAIM_ID=006D_FINITE_POSITIVE_ENERGY_LOCAL_REPULSION

TYPE=
PROJECT_DERIVED_CONSTRUCTIVE_LINEARIZED_GR_RESULT

STATUS=
SUPPORTED_WITHIN_STATED_APPROXIMATION
```

```text
CLAIM_ID=016A_THICK_REALIZATION_TARGET

TYPE=
PROJECT_DERIVED_NUMERICAL_DESIGN_RESULT

STATUS=
SUPPORTED
```

```text
CLAIM_ID=016A_MACROSCOPIC_AREA_ENERGY_CANCELLATION

TYPE=
PROJECT_DERIVED_ANALYTIC_SCALING_RESULT

STATUS=
SUPPORTED_WITHIN_SIMPLE_TILING_ARCHITECTURE
```

```text
CLAIM_ID=016B_THICK_FIXED_CHARGE_CAPACITY

TYPE=
PROJECT_DERIVED_NUMERICAL_PREFLIGHT

STATUS=
SUPPORTED
```

```text
CLAIM_ID=016C_SIMPLE_ELECTROSTATIC_GLOBAL_REALIZATION

TYPE=
PROJECT_DERIVED_ANALYTIC_AND_NUMERICAL_NO_GO

STATUS=
REJECTED_FOR_TESTED_TWO_POTENTIAL_CLASS
```

```text
CLAIM_ID=016D_EXPONENTIAL_TAIL_STRESS_TARGET

TYPE=
PROJECT_DERIVED_REALIZABILITY_PREFLIGHT

STATUS=
GRAVITATIONALLY_SUPPORTED_BUT_LATER_DEMOTED_FOR_MINIMAL_GAUGED_WINDING_REALIZATION
```

```text
CLAIM_ID=016E_EXPONENTIAL_GAUGE_ASYMPTOTIC

TYPE=
PROJECT_DERIVED_ANALYTIC_AND_NUMERICAL_NEGATIVE_RESULT

STATUS=
REJECTED_FOR_MINIMAL_SINGLE_GAUGED_WINDING_CLASS
```

```text
CLAIM_ID=016E_POWER_LAW_GAUGE_ASYMPTOTIC

TYPE=
PROJECT_DERIVED_KINEMATIC_PREFLIGHT

STATUS=
SUPPORTED
```

```text
CLAIM_ID=016F_CHARGE_WINDING_COEXISTENCE

TYPE=
PROJECT_DERIVED_KINEMATIC_OPTIMIZATION_RESULT

STATUS=
SUPPORTED_IN_TESTED_ALLOCATION
```

```text
CLAIM_ID=016G_MINIMAL_DECOUPLED_CANONICAL_EXACT_POWER_LAW_TARGET

TYPE=
PROJECT_DERIVED_ASYMPTOTIC_NO_GO

STATUS=
REJECTED_UNDER_STATED_ASSUMPTIONS
```

```text
CLAIM_ID=016H_GENERIC_COUNTERWINDING_FLS_LIKE_VARIATIONAL_REPULSION

TYPE=
PROJECT_DERIVED_NUMERICAL_NEGATIVE_RESULT

STATUS=
NOT_FOUND_IN_TESTED_63_BOUND_CONFIGURATIONS
```

The following claims remain prohibited:

```text
ACTUAL_006D_MATTER_REALIZATION=
ESTABLISHED

FULL_DYNAMIC_STABILITY=
ESTABLISHED

NONLINEAR_EINSTEIN_MATTER_SOLUTION=
ESTABLISHED

FINITE_PAYLOAD_LIFT=
ESTABLISHED

PRACTICAL_ANTIGRAVITY_DEVICE=
ESTABLISHED

REACTIONLESS_PROPULSION=
ESTABLISHED

NEW_PHYSICS_DISCOVERY=
ESTABLISHED
```

---

# Open Questions

## 1. Can spatial segregation rescue a canonical field realization?

This is now the primary established-GR matter question.

The next candidate architecture should deliberately separate:

```text
CENTRAL NEGATIVE-ACTIVE-STRESS REGION

FROM

OUTER POSITIVE-ENERGY SUPPORT / CHARGE / CURRENT / GAUGE REGION
```

rather than using largely co-spatial centered field profiles.

A natural architecture is:

```text
DOMAIN-WALL / MEMBRANE DRUM
+
CHARGED / COUNTER-WINDING / GAUGED RIM
```

or a vorton-like outer support structure.

---

## 2. Can such a separated architecture be a genuine stationary field solution?

A positive variational preflight would still need to be promoted to a full coupled Euler-Lagrange boundary-value problem.

Required outputs would include:

```text
PDE_RESIDUAL

TOTAL_ENERGY

NOETHER_CHARGE

GAUGE_CHARGE

NET_ANGULAR_MOMENTUM

T_TPHI

ACTIVE_SOURCE

OUTWARD_FIELD

BOUNDARY_DECAY

CONVERGENCE_WITH_DOMAIN_SIZE

CONVERGENCE_WITH_GRID_RESOLUTION
```

---

## 3. Is the separated field configuration dynamically stable?

Even if a stationary field solution exists, the project must test:

* radial expansion/contraction;
* vertical displacement;
* azimuthal perturbations;
* charge-transfer modes;
* vortex splitting;
* wall-rim relative displacement;
* gauge perturbations;
* collapse modes.

The old fixed-charge condition

```math
T/E>1/8
```

is only one-mode evidence.

---

## 4. Does a nonlinear Einstein-matter continuation exist?

If a stable matter solution is found, solve

```math
G_{\mu\nu}
=
\frac{8\pi G}{c^4}
T_{\mu\nu}.
```

Need verify:

```math
\nabla_\mu T^{\mu\nu}=0
```

self-consistently and evaluate invariant/operational gravitational observables.

---

## 5. Does pointwise outward gravity lift a finite payload?

This remains mandatory.

A future finite payload must use

```math
\mathbf a_{\rm CM}
=
\frac{
\int
\rho_P
\mathbf a
\,dV
}{
\int
\rho_P
\,dV
}.
```

The disformal 015C branch already demonstrated that local reversed cells can fail to produce finite-body reversal.

The same discipline must apply to the 006D branch.

---

## 6. Can the catastrophic pure-GR energy scaling be changed?

Even a successful field realization currently inherits approximately

```math
M
\sim
C\frac{ah^2}{G}.
```

Simple tiled coverage inherits

```math
\frac EA
\sim
\frac{
Cac^2
}{
\pi x_{\max}^2G
}.
```

Order-unity changes in $C$ cannot close the practical gap.

A practical device would require a qualitatively different scaling mechanism.

Possibilities include:

* better spatial kernel leverage;
* a collective source interacting with a macroscopic payload without simple cell tiling;
* an external gravitational background;
* a substantially stronger allowed interaction;
* another well-motivated physical mechanism not currently identified.

---

## 7. Should the disformal branch be reopened?

The strongest disformal result remains local total-force reversal in 014D.

015C found no finite-payload center-of-mass reversal in its first tested root-time localized-source domain.

If the canonical 006D realization route fails again, the highest-value disformal follow-up remains:

```text
ORIGINAL_014D_GEOMETRY
+
FINITE_PAYLOAD_INTEGRATION
```

and

```text
DYNAMIC_TIME_FINITE_PAYLOAD_SEARCH.
```

Do not rerun the already validated local 014D sign calculation.

---

## 8. Should the protected scalar-force branch be reranked?

Yes.

Pure GR has high theoretical confidence but catastrophic energy scaling.

A protected material-specific fifth-force branch is theoretically more speculative but has the possibility of a much stronger effective interaction.

After documentation, the project should formally rerank:

```text
A:
SPATIALLY_SEPARATED_006D_INSPIRED_DRUM_VORTON

B:
014D_DISFORMAL_FINITE_PAYLOAD_CONTINUATION

C:
PROTECTED_MATERIAL_SPECIFIC_SCALAR_UV_COMPLETION
```

using:

```text
THEORY_CONFIDENCE

CURRENT_POSITIVE_EVIDENCE

EXPERIMENTAL_CONSTRAINTS

NUMBER_OF_SPECULATIVE_ASSUMPTIONS

FINITE_PAYLOAD_PROSPECT

PRACTICAL_ENERGY_SCALING

NEXT_EXPERIMENT_INFORMATION_GAIN
```

---

# Recommended Next Established-GR Architecture

The strongest direct lesson from 006D and 016H is that the next model should not be a centered co-spatial Q-ball.

The suggested architecture is:

```text
CENTRAL DRUM / MEMBRANE:
domain-wall-like scalar sector
large tension
negative active source
high gravitational kernel

OUTER RIM:
charge
counter-winding
gauge support
positive compensating energy
lower gravitational kernel
```

Possible field sectors:

```text
SECTOR X:
REAL SYMMETRY-BREAKING SCALAR
FOR THE CENTRAL WALL / DRUM

SECTOR Q:
NONWINDING STATIONARY COMPLEX SCALAR
FOR FIXED CHARGE

SECTOR W:
COUNTER-WINDING COMPLEX PAIR
CONCENTRATED TOWARD THE OUTER RIM

GAUGE SECTOR:
U(1) SUPPORT
PRIMARILY ASSOCIATED WITH THE RIM
```

The exact stress tensor should **not** be forced to match 006D.

Instead, optimize the physical observable:

```math
a_z(h)
```

while requiring approximate stationary balance and positive total mass.

---

# Suggested Next Simulation

A reasonable next established-GR simulation identifier is:

```text
016I
```

Suggested title:

```text
016I_SPATIALLY_SEPARATED_DRUM_VORTON_VARIATIONAL_GRAVITY_GATE
```

Scientific question:

> **Can an explicit healthy local field model with a central tension-dominated wall/drum sector and a spatially separated outer charge/current support sector naturally generate a negative kernel-weighted active gravitational moment while remaining a localized approximately stationary bound configuration?**

The first 016I run should still be a finite-dimensional variational preflight.

Do **not** begin with the full PDE.

Suggested variational degrees of freedom:

```text
DRUM_RADIUS

DRUM_VERTICAL_WIDTH

DRUM_RADIAL_EDGE_WIDTH

DRUM_AMPLITUDE

RIM_RADIUS

RIM_WIDTH

RIM_VERTICAL_POSITION

RIM_VERTICAL_WIDTH

CHARGE_AMPLITUDE

WINDING

GAUGE_MISMATCH_PROXY
```

Required observables:

```text
TOTAL_ENERGY

BOUND_STATE_DIAGNOSTIC

VARIATIONAL_GRADIENT

TOTAL_ACTIVE_MASS

NEGATIVE_ACTIVE_VOLUME

NEGATIVE_ACTIVE_WEIGHTED_MOMENT

POSITIVE_ACTIVE_WEIGHTED_MOMENT

NEAR_FIELD_ACCELERATION

CLEAN_EXTERIOR_ACCELERATION
```

A strong pass requires:

```text
FINITE_TOTAL_ENERGY=
YES

LOCALIZED_FIELDS=
YES

APPROX_STATIONARY=
YES

POSITIVE_TOTAL_ACTIVE_MASS=
YES

NEGATIVE_ACTIVE_REGION=
YES

OUTWARD_GRAVITATIONAL_FIELD=
YES

INDEPENDENT_FORCE_QUADRATURE=
PASS
```

Stop rule:

> **If a sufficiently flexible spatially separated canonical variational architecture still cannot produce outward gravity before approaching obvious pathological parameter limits, deprioritize generic canonical 006D matter realization rather than escalating automatically to a large PDE solve.**

---

# AI Assistance

AI assistant used: ChatGPT by OpenAI

Substantial AI-assisted work in this research slice included:

* identification of the 006D thickness/peak-stress tradeoff;
* derivation of the macroscopic area-energy cancellation;
* reconstruction and checking of the fixed-charge Derrick capacity;
* design of the 016C electrostatic conformal-integrability gate;
* derivation of the exponential-tail gauge mismatch asymptotics;
* design of the $C^2$ power-law replacement;
* derivation of simultaneous charge/winding Gram-budget bounds;
* optimization of the inner transition width;
* derivation of the 016G asymptotic Euler-Lagrange identity;
* independent finite-difference verification design for 016G;
* design of the 016H explicit field-model variational test;
* derivation of the 016H active-source identity;
* interpretation of the 63-case negative field result;
* identification of spatial active-stress segregation as the new design principle;
* preparation of this journal record.

AI-generated mathematics, numerical strategies, code, and physical interpretations are not assumed correct solely because they were generated by an AI system.

All important claims remain subject to:

```text
ANALYTIC_CHECK

NUMERICAL_CHECK

DIMENSIONAL_CHECK

LIMITING_CASE_CHECK

INDEPENDENT_IMPLEMENTATION

LITERATURE_COMPARISON

ASSUMPTION_AUDIT
```

No AI-assisted result should be promoted to a scientific discovery without independent verification and literature comparison.

---

# Next Action

The 016A–016H realization slice should now be considered complete.

Do not run additional 006D realization simulations until the repository documentation and active research ranking are updated.

Immediate next actions:

```text
1.
UPDATE NOTES.md WITH 016A-016H

2.
UPDATE RESEARCH_BUILDPLAN.md

3.
UPDATE README FRONTIER WITHOUT WEAKENING THE 006D HEADLINE

4.
SYNCHRONIZE CLAIMS.md IF PRESENT / STALE

5.
FORMALLY RERANK:
DRUM-VORTON
VS
014D DISFORMAL FINITE PAYLOAD
VS
PROTECTED MATERIAL-SPECIFIC SCALAR

6.
SELECT ONE ACTIVE SCIENTIFIC QUESTION
```

If the established-GR branch remains first-ranked after reranking, the next simulation should be:

```text
016I_SPATIALLY_SEPARATED_DRUM_VORTON_VARIATIONAL_GRAVITY_GATE
```

The principal observable should be:

```math
a_z(h),
```

not exact stress-tensor matching.

The central design condition should be:

```math
\boxed{
\int S\,dV>0
}
```

while

```math
\boxed{
\int S K_h\,dV<0.
}
```

This is the clearest mathematical statement of the current physical frontier.

---

# Final Scientific State at Journal Close

```text
REGRESSION_BASELINE=
94_PASSED_BEFORE_FINAL_016H_VARIATIONAL_RUN

006D_CONSTRUCTIVE_POSITIVE_ENERGY_LINEARIZED_GR_REPULSION=
PRESERVED

006D_NEC=
PASS

006D_WEC=
PASS

006D_DEC=
PASS

006D_LOCAL_CONSERVATION_LINEARIZED_ORDER=
ESTABLISHED

006D_POSITIVE_FAR_FIELD_ACTIVE_MASS=
ESTABLISHED

016A_THICK_REALIZATION_TARGET=
GREEN

016A_MACROSCOPIC_MICROSTANDOFF_AREA_ENERGY_ESCAPE=
NO

016B_THICK_FIXED_CHARGE_CAPACITY=
GREEN

016B_THICK_GAUGE_CAPACITY=
GREEN

016C_SIMPLE_TWO_POTENTIAL_ELECTROSTATIC_EXACT_TARGET=
REJECTED

016D_SMOOTH_EXPONENTIAL_STRESS_TARGET=
GRAVITATIONALLY_GREEN

016E_EXPONENTIAL_MINIMAL_GAUGED_WINDING_REALIZATION=
REJECTED

016E_POWER_LAW_GAUGE_ASYMPTOTIC=
GREEN_KINEMATICALLY

016F_SIMULTANEOUS_CHARGE_WINDING_COEXISTENCE=
GREEN_KINEMATICALLY

016F_PREFERRED_W=
1.0

016F_PREFERRED_ELL=
0.6

016F_PREFERRED_C=
40.749886771113

016F_TARGET_T_OVER_E=
0.14

016F_PREFERRED_K_REQUIRED=
9.589406109611

016F_CONSERVATIVE_WINDING=
10

016F_PEAK_STRESS_RELIEF_VS_FINE_006D=
1400.489x

016G_EXACT_MINIMAL_CANONICAL_POWER_LAW_TARGET=
REJECTED

016G_REJECTION_REASON=
ASYMPTOTIC_EULER_LAGRANGE_FORCE_SIGN_CONFLICT

016G_CORE_IDENTITY=
K_INFINITY_SQUARED_MINUS_S_SQUARED_POSITIVE

016H_PROMOTED_BOUND_CASES=
63

016H_INTERNALLY_CONSISTENT_BOUND_CASES=
63

016H_NEGATIVE_ACTIVE_DENSITY=
YES

016H_MAX_NEGATIVE_ACTIVE_FRACTION_OVER_E=
0.266601491354

016H_NEAR_FIELD_REPULSION=
NOT_FOUND

016H_CLEAN_EXTERIOR_REPULSION=
NOT_FOUND

016H_FORCE_SIGN_RESOLUTION_CHECK=
PASS

NEW_MAJOR_DESIGN_PRINCIPLE=
SPATIALLY_SEGREGATE_NEGATIVE_ACTIVE_STRESS_FROM_POSITIVE_SUPPORT_BY_GRAVITATIONAL_KERNEL_LEVERAGE

FULL_EULER_LAGRANGE_FIELD_REALIZATION=
NOT_ESTABLISHED

FULL_DYNAMIC_STABILITY=
NOT_ESTABLISHED

NONLINEAR_EINSTEIN_MATTER_REALIZATION=
NOT_ESTABLISHED

FINITE_PAYLOAD_LIFT=
NOT_ESTABLISHED

PURE_GR_MACROSCOPIC_AH2_OVER_G_ENERGY_SCALING=
UNCHANGED

PRACTICAL_ANTIGRAVITY_DEVICE=
NO

REACTIONLESS_PROPULSION=
NO_CLAIM

NEW_PHYSICS_DISCOVERY=
NO

NOVELTY=
NOT_ESTABLISHED
```

---

# Final Journal Classification

The strongest established positive result remains:

> **Within static linearized general relativity, an explicit finite, nonsingular, positive-energy, locally conserved, NEC/WEC/DEC-compatible source can produce a locally outward gravitational near field while maintaining positive far-field active mass.**

The 016A–016H research slice does not replace this result.

It clarifies the matter-realization frontier.

The strongest new positive realizability result is:

> **A thick, smoothed 006D-inspired source can retain outward gravity, a fixed-charge stabilization budget, finite-energy power-law gauge asymptotics, and simultaneous charge/winding kinematic compatibility with a conservative winding burden reduced to approximately $n=10$.**

The strongest new realization constraint is:

> **The exact promoted power-law target is incompatible with the asymptotic Euler-Lagrange equation of the minimum decoupled canonical winding field with a stable vacuum under the stated assumptions.**

The strongest new explicit-field falsification result is:

> **A tested family of 63 bound, internally consistent, positive-energy counter-winding FLS-like variational field configurations generated substantial local negative active gravitational density but no outward near or clean-exterior gravitational acceleration.**

The principal new physical design rule is therefore:

> **A realizable antigravity-like source must control not only the sign of the local active gravitational density but its spatial distribution relative to the gravitational Green-function kernel. Negative active stress must be preferentially concentrated where gravitational leverage is high, while the compensating positive support required for finite energy and positive total mass must be displaced toward regions of lower leverage.**

This is the scientific frontier carried forward from the 016A–016H realization program.
