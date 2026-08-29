# Antigravity Research

> # **We have a mathematical construction for antigravity-like gravitational repulsion.**

The exact scientific claim supporting that headline is:

> **Within static linearized general relativity, there exists an explicit finite-radius, finite-thickness, nonsingular, positive-energy, locally conserved type-I stress-energy configuration satisfying NEC, WEC, and DEC whose calculated near gravitational field points outward while its far-field active mass remains positive.**

This is the project's strongest established project-derived result.

The result is a **constructive linearized-GR stress-energy result**.

It is **not** an exact nonlinear Einstein solution, a full stability proof, a known material realization, an experimental observation, or a practical antigravity device.

---

# Current Progress Toward Practical Antigravity

> ## **Informal project-progress heuristic: approximately 44%**

This number is **not a scientific probability that practical antigravity exists**.

It is a project milestone estimate reflecting how much of the logical path from mathematical possibility to an actual device has been addressed.

The project has established:

```text
MATHEMATICAL_REPULSIVE_GRAVITY_SIGN=
YES

EXPLICIT_FINITE_POSITIVE_ENERGY_REPULSIVE_GR_SOURCE=
YES

NEC_WEC_DEC_COMPATIBILITY=
YES

LOCAL_CONSERVATION_LINEARIZED_ORDER=
YES

POSITIVE_FAR_FIELD_ACTIVE_MASS=
YES

FINITE_THICKNESS=
YES

ONE_MODE_FIXED_CHARGE_STABILITY_CAPACITY=
YES

FIELD_REALIZATION_CONSTRAINTS=
SUBSTANTIALLY_CHARACTERIZED
```

The project has **not** established:

```text
ACTUAL_STABLE_MATTER_FIELD_REALIZATION=
NO

FULL_DYNAMIC_STABILITY=
NO

NONLINEAR_EINSTEIN_MATTER_SOLUTION=
NO

FINITE_PAYLOAD_LIFT=
NO

PRACTICAL_ENERGY_SCALING=
NO

EXPERIMENTAL_DEMONSTRATION=
NO

PRACTICAL_ANTIGRAVITY_DEVICE=
NO
```

The estimate was reduced after Simulations 016G and 016H because two of the simplest paths from the mathematical 006D source to actual canonical matter were falsified.

Scientifically, however, those negative results are progress: they substantially narrowed the physical problem.

---

# Current Scientific Position

The project now has three distinct layers.

## 1. Strongest established positive result — 006D

Simulation 006D constructs a finite stress-energy source in static linearized GR with:

```text
FINITE_RADIUS=YES
FINITE_THICKNESS=YES
NONSINGULAR_OUTER_SUPPORT=YES

POSITIVE_ENERGY_DENSITY=YES

LOCAL_CONSERVATION_LINEARIZED_ORDER=YES

NEC=PASS
WEC=PASS
DEC=PASS

OUTWARD_LOCAL_GRAVITATIONAL_FIELD=YES

POSITIVE_FAR_FIELD_ACTIVE_MASS=YES
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
C\frac{ah^2}{G}.
```

The independent thin conserved reference is

```math
C_{\mathrm{thin}}
=
23.426710175391.
```

For the complete derivation and standalone reproducer, see:

[`journal/2026-08-28_006d_constructive_linearized_gr_repulsion.md`](journal/2026-08-28_006d_constructive_linearized_gr_repulsion.md)

---

## 2. Strongest realizability-oriented positive preflight — 016F

The 016A–016F program substantially improved the physical realizability target.

The preferred 016F kinematic coexistence point was:

```text
INNER_TRANSITION_HALF_WIDTH_W=
1.0

POWER_LAW_TAIL_LENGTH_ELL=
0.6

POWER_EXPONENT_M=
2

C=
40.749886771113

TMAX_OVER_E=
0.180278569163

ALLOCATED_T_OVER_E=
0.14

DERRICK_CURVATURE_OVER_E=
+0.36

REQUIRED_GAUGE_MISMATCH_K=
9.589406109611

CONSERVATIVE_INTEGER_WINDING=
10

PEAK_STRESS_RELIEF_VS_FINE_006D=
1400.489x
```

This showed that simultaneous charge stabilization and winding support are **kinematically compatible** in a much less extreme geometry.

It did **not** establish an actual matter-field solution.

016G then showed that the exact promoted power-law target cannot be realized by the minimum asymptotically decoupled canonical winding field under the stated assumptions.

---

## 3. Current physical frontier after 016H

016H stopped forcing matter to reproduce the engineered 006D tensor and instead allowed an explicit healthy canonical field model to determine its own stress-energy.

Across:

```text
63
```

bound and internally consistent variational states, substantial negative active gravitational density was generated.

The largest tested negative-active contribution was approximately:

```text
26.66%
```

of the total energy scale.

Nevertheless:

```text
NEAR_FIELD_OUTWARD_ACCELERATION=
NOT_FOUND

CLEAN_EXTERIOR_OUTWARD_ACCELERATION=
NOT_FOUND
```

The attractive force sign remained stable under independent quadrature refinement.

The central new conclusion is therefore:

> **Negative active gravitational density is not sufficient for outward gravity. The negative and positive active-stress contributions must be spatially organized correctly relative to the gravitational Green-function kernel.**

The leading established-GR realization idea is now a deliberately **spatially separated drum-plus-rim/vorton architecture**, rather than a generic co-spatial Q-ball-like object.

The complete 016A–016H record is preserved in:

[`journal/2026-08-29_016a_016h_006d_realizability_and_canonical_field_gates.md`](journal/2026-08-29_016a_016h_006d_realizability_and_canonical_field_gates.md)

For detailed chronology, rejected branches, and numerical context, see [`NOTES.md`](NOTES.md).

For the active decision tree and branch ranking, see [`RESEARCH_BUILDPLAN.md`](RESEARCH_BUILDPLAN.md).

---

# Proof of the 006D Headline Claim

## 1. Active gravitational source in static linearized GR

Use metric signature $(-,+,+,+)$.

For a type-I source in a local orthonormal frame,

```math
T_{\hat\mu\hat\nu}
=
\mathrm{diag}
\left(
\epsilon,
p_r,
p_\phi,
p_z
\right).
```

In harmonic gauge,

```math
\Box\bar h_{\mu\nu}
=
-\frac{16\pi G}{c^4}T_{\mu\nu}.
```

For a static source,

```math
\nabla^2\bar h_{\mu\nu}
=
-\frac{16\pi G}{c^4}T_{\mu\nu}.
```

Writing

```math
g_{00}
=
-\left(
1+\frac{2\Phi}{c^2}
\right)
```

gives

```math

\nabla^2\Phi
=
\frac{4\pi G}{c^2}
\left(
\epsilon+p_r+p_\phi+p_z
\right).

```

Define

```math
S
=
\epsilon+p_r+p_\phi+p_z.
```

The Green-function solution is

```math
\Phi(\mathbf x)
=
-\frac{G}{c^2}
\int
\frac{
S(\mathbf x')
}{
|\mathbf x-\mathbf x'|
}
\,d^3x'.
```

The physical weak-field acceleration is

```math
\mathbf a
=
-\nabla\Phi.
```

For an axisymmetric source and target on the axis at $z=h$,

```math
a_z(h)
=
-\frac{2\pi G}{c^2}
\int dz
\int_0^\infty dr\,
rS(r,z)
\frac{
h-z
}{
\left[
r^2+(h-z)^2
\right]^{3/2}
}.
```

Repository convention:

```text
a_z > 0  -> outward

a_z < 0  -> inward
```

---

## 2. Explicit finite conserved source

Define

```math
x=\frac rh
```

and

```math
\zeta=\frac zh.
```

Use:

```text
ALPHA=
1.437500564637

BETA=
4.701437405300

DELTA=
0.00625

INNER_WIDTH=
DELTA/4

OUTER_WIDTH=
DELTA
```

Define

```math
q(x)
=
x p_r(x)
```

and impose

```math
p_\phi(x)
=
q'(x),
```

with

```math
p_z=0
```

and

```math
T_{\hat r\hat z}=0.
```

The core branch is

```math
q_{\mathrm{core}}(x)
=
-x.
```

The transfer-annulus branch is

```math
q_{\mathrm{ann}}(x)
=
-\frac{\alpha^2}{x}.
```

The branches are joined with cubic smoothstep

```math
s(u)
=
u^2(3-2u),
```

and the outer collar smoothly drives both $q$ and $q'$ to zero.

The exact piecewise source is implemented in:

```text
simulations/006d_finite_thickness_conserved_source.py
```

and is reproduced independently in the 006D journal.

---

## 3. Local-conservation proof

Because

```math
p_r
=
\frac qx
```

and

```math
p_\phi
=
q',
```

we have

```math
\frac{dp_r}{dx}
=
\frac{q'}x
-
\frac{q}{x^2}.
```

Therefore

```math
\frac{dp_r}{dx}
+
\frac{
p_r-p_\phi
}{x}
=
\frac{q'}x
-
\frac{q}{x^2}
+
\frac{
q/x-q'
}{x}
=
0.
```

Hence

```math

\frac{dp_r}{dx}
+
\frac{
p_r-p_\phi
}{x}
=
0.

```

This is the static cylindrical radial conservation equation.

With

```math
p_z=0
```

and

```math
T_{\hat r\hat z}=0,
```

the remaining static flat-background conservation equation also vanishes.

Thus

```math

\partial_\mu T^{\mu\nu}=0

```

at the linearized/static background order.

This is not yet an exact nonlinear curved-spacetime proof of

```math
\nabla_\mu T^{\mu\nu}=0.
```

---

## 4. Energy-condition proof

Choose

```math

\epsilon
=
\max
\left(
|p_r|,
|p_\phi|
\right).

```

Since $p_z=0$,

```math
\epsilon\ge0,
```

```math
|p_r|\le\epsilon,
```

```math
|p_\phi|\le\epsilon,
```

and

```math
|p_z|\le\epsilon.
```

These are the type-I dominant-energy-condition inequalities.

Also,

```math
\epsilon+p_i
\ge
\epsilon-|p_i|
\ge
0.
```

Therefore:

```text
DEC=PASS
WEC=PASS
NEC=PASS
```

without negative local energy density.

---

## 5. Positive far-field active-mass proof

The dimensionless spatial-stress trace is

```math
\tau
=
2
\int
x
\left(
p_r+p_\phi
\right)
dx.
```

Using $p_r=q/x$ and $p_\phi=q'$,

```math
\tau
=
2
\int
\left(
q+xq'
\right)
dx.
```

But

```math
q+xq'
=
\frac{d}{dx}(xq).
```

Therefore

```math
\tau
=
2[xq]_0^{x_{\max}}.
```

The finite construction satisfies

```math
q(0)=0
```

and

```math
q(x_{\max})=0.
```

Hence

```math

\tau=0.

```

Because

```math
\epsilon\ge0
```

and the source is nonzero,

```math
\int\epsilon\,dV>0.
```

Therefore the integrated active mass is positive.

The construction has an outward near field but an attractive positive-mass far field.

---

## 6. Numerical field sign

Define

```math
A(x)
=
\epsilon+p_r+p_\phi.
```

The normalized finite-thickness kernel is

```math
K_\delta(x)
=
\int_{-\delta}^{0}
\varphi_\delta(\zeta)
\frac{
1-\zeta
}{
\left[
x^2+(1-\zeta)^2
\right]^{3/2}
}
\,d\zeta.
```

The field factor is

```math
F_\delta
=
-
\int
xA(x)K_\delta(x)\,dx.
```

The physical acceleration is

```math
a_z
=
\frac{
2\pi G U_0
}{
c^2
}
F_\delta.
```

The independent numerical evaluations give:

```text
MASS_FACTOR=
1.110076490539830e+01

TRACE_FACTOR=
2.922107000813412e-13

ACTIVE_MASS_FACTOR=
1.110076490539859e+01

FIELD_FACTOR_GL64=
2.352695737495157e-01

FIELD_FACTOR_NESTED=
2.352695737495351e-01

FIELD_METHOD_ABS_DIFFERENCE=
1.942890293094024e-14

MAX_CONTROL_VOLUME_CONSERVATION_RESIDUAL=
3.103073353827313e-14

MAX_DEC_VIOLATION=
0

MIN_NEC_MARGIN=
0
```

Thus

```math

F_\delta
=
0.2352695737495\ldots
>
0

```

and therefore

```math

a_z>0.

```

This establishes the 006D headline claim within static linearized GR.

---

# Practical Scaling Result

The 006D family obeys

```math
M
=
C\frac{ah^2}{G}.
```

For the finest finite source,

```math
C
=
23.591586299249.
```

For $a=g$ and $h=1\ {\mathrm{m}}$,

```math
M_{\mathrm{equiv}}
\approx
3.47\times10^{12}\ {\mathrm{kg}}
```

and

```math
E
\approx
3.12\times10^{29}\ {\mathrm{J}}.
```

This is why the construction is mathematically important but not practical.

016A also established a stronger engineering warning.

For one source cell,

```math
E_{\mathrm{cell}}
=
C\frac{ah^2c^2}{G}.
```

If its footprint is

```math
A_{\mathrm{cell}}
=
\pi x_{\max}^2h^2,
```

then

```math

\frac{
E_{\mathrm{cell}}
}{
A_{\mathrm{cell}}
}
=
\frac{
Cac^2
}{
\pi x_{\max}^2G
}.

```

The stand-off scale $h$ cancels.

Therefore simply miniaturizing and tiling many 006D-like cells does **not** remove the macroscopic energy problem.

---

# Latest Realizability Result: 016G Canonical Asymptotic No-Go

016F found a kinematically viable two-sector charge/winding target.

016G asked whether its exact power-law tail can satisfy the actual asymptotic Euler-Lagrange equation of the minimum asymptotically decoupled canonical winding field.

Under the stated assumptions, the answer is **no**.

## 1. Power-law target

For the promoted $m$-power tail,

```math
q(r)
\propto
-r^{-m-1}.
```

Therefore

```math
p_r
\sim
-C_\infty r^{-m-2}
```

and

```math
p_\phi
\sim
(m+1)C_\infty r^{-m-2}.
```

The target uses

```math
\epsilon
=
p_\phi.
```

Allocate a fraction $\eta$ of the available temporal kinetic capacity to the charged stabilizer.

The remaining radial Gram budget is

```math

G_r
\sim
(1-\eta)
mC_\infty
r^{-m-2}.

```

The required angular Gram component is

```math

A
\sim
\left[
2(m+1)-\eta m
\right]
C_\infty
r^{-m-2}.

```

---

## 2. Maximum possible finite-energy amplitude

For winding amplitude $F(r)$,

```math
F'^2
\le
G_r
```

and finite energy requires

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

the slowest possible finite-energy amplitude is

```math
F
\propto
r^{-s}
```

with

```math

s=\frac m2.

```

---

## 3. Minimum required gauge-covariant winding

Let

```math
k
=
n-eA_\phi.
```

Exact angular matching requires

```math
\frac{
k^2F^2
}{r^2}
=
A.
```

Using the maximum possible $F$ gives the smallest possible asymptotic $k$:

```math
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
```

Since

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

Combining terms,

```math
k_\infty^2-s^2
=
\frac{
m
\left[
2(m+1)-\eta m-m(1-\eta)
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

k_\infty^2-s^2
=
\frac{
m(m+2)
}{
4(1-\eta)
}
>0

```

for every

```math
m>0
```

and

```math
0\le\eta<1.
```

Thus

```math

k_\infty^2>s^2.

```

---

## 4. Euler-Lagrange sign conflict

For a gapless asymptotically decoupled canonical winding amplitude,

```math
F''
+
\frac1rF'
-
\frac{k^2}{r^2}F
-
U_{\mathrm{eff}}'(F)
=
0.
```

For

```math
F
=
Ar^{-s},
```

we have

```math
F''
+
\frac1rF'
=
\frac{s^2}{r^2}F.
```

Therefore the field equation requires

```math
U_{\mathrm{eff}}'(F)
=
\frac{
s^2-k^2
}{
r^2
}F.
```

But 016G established

```math
k^2>s^2.
```

Hence

```math

U_{\mathrm{eff}}'(F)<0

```

for sufficiently small positive $F$.

A regular asymptotically decoupled canonical scalar whose vacuum $F=0$ is a stable local minimum has the opposite restoring sign sufficiently near the vacuum.

Therefore:

> **The exact promoted power-law stress target is incompatible with the minimum asymptotically decoupled canonical winding field with a regular stable-vacuum self-potential, under the stated assumptions.**

This is a **restricted no-go**, not a theorem against all canonical field realizations.

For the preferred 016F case,

```text
M=
2

ETA≈
0.77657594383

S=
1

K_INFINITY≈
3.15461369297

K_INFINITY^2-S^2≈
+8.95158755185
```

and therefore

```text
S^2-K_INFINITY^2≈
-8.95158755185.
```

A finite-difference implementation independently recovered the same coefficient.

---

# Latest Explicit Field Test: 016H

016H tested the principal escape from 016G:

> **Do not demand exact reproduction of the engineered 006D tensor. Let a healthy field theory determine its own stress tensor and test the gravitational field directly.**

The tested model used one real symmetry-breaking scalar and an equal counter-winding complex pair:

```math
\Phi_\pm
=
Y(r,z)
e^{i(\omega t\pm n\phi)}.
```

The opposite windings cancel net

```math
T_{t\phi}.
```

The potential was

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
\right),
```

which is nonnegative.

For this model the exact active-source combination simplifies to

```math

S
=
\rho+p_r+p_\phi+p_z
=
8\omega^2Y^2-2V.

```

Thus the field model can genuinely generate regions with

```math
S<0
```

through its scalar potential/tension.

The gravitational observable remains

```math
a_z(h)
\propto
-
\int
S(r,z)
\frac{
h-z
}{
\left[
r^2+(h-z)^2
\right]^{3/2}
}
\,dV.
```

The scan produced:

```text
PROMOTED_BOUND_CASES=
63

INTERNALLY_CONSISTENT_BOUND_CASES=
63

NEGATIVE_ACTIVE_DENSITY_EXISTS=
YES

MAX_NEGATIVE_ACTIVE_FRACTION_OVER_E≈
0.266601491354

ANY_NEAR_FIELD_OUTWARD_ACCELERATION=
NO

ANY_CLEAN_EXTERIOR_OUTWARD_ACCELERATION=
NO
```

The best exterior case remained inward:

```text
EXTERIOR_MAX_A_KERNEL≈
-0.77021758
```

and independent quadrature orders

```text
64
96
128
```

all retained the same sign.

Therefore the current supported statement is:

> **The tested healthy co-spatial counter-winding FLS-like variational field family can generate substantial negative active gravitational density, but that alone does not produce outward gravity.**

This is a numerical falsification within the tested ansatz family, not a universal theorem against FLS/Q-ball/vorton physics.

---

# New Design Principle: Spatial Active-Stress Segregation

The 006D and 016H results together sharpen the physical problem.

Define

```math
S
=
\epsilon+p_r+p_\phi+p_z.
```

For positive far-field active mass we need

```math

\int S\,dV>0.

```

For an outward field at the chosen target we need

```math

\int
S K_h
\,dV
<
0,

```

where

```math
K_h(r,z)
=
\frac{
h-z
}{
\left[
r^2+(h-z)^2
\right]^{3/2}
}
>0.
```

Let

```math
S_+
=
\max(S,0)
```

and

```math
S_-
=
\max(-S,0).
```

Then positive total active mass requires

```math
\int S_+\,dV
>
\int S_-\,dV.
```

But outward near-field gravity requires

```math
\int K_hS_-\,dV
>
\int K_hS_+\,dV.
```

Therefore the negative active source must receive **greater gravitational kernel leverage per unit integrated magnitude** than the compensating positive source.

This gives the new physical design rule:

> **Concentrate negative active stress near the high-kernel target-facing region and move the compensating positive energy, charge, current, and support toward lower-kernel outer regions.**

006D does this by construction.

The largely co-spatial 016H family did not.

This is why the next established-GR realization candidate is a spatially separated architecture such as:

```text
CENTRAL DOMAIN-WALL / MEMBRANE DRUM
+
OUTER CHARGED / COUNTER-WINDING / GAUGED RIM
```

rather than another generic centered Q-ball-like configuration.

---

# Reproduction

From the repository root:

```bash
ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"

set +u 2>/dev/null || true
unsetopt PIPE_FAIL 2>/dev/null || true

PYTHONPATH="$ROOT/src" \
"$PY" -m pytest -q tests/known_solutions
```

Current verified baseline:

```text
94 passed
```

## Reproduce 006D

```bash
ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"

PYTHONPATH="$ROOT/src" \
"$PY" \
  simulations/006d_finite_thickness_conserved_source.py
```

Reference values:

```text
C_FINITE_BEST_TESTED=
23.591586299249

OUTWARD_GRAVITATIONAL_FIELD=
YES

POSITIVE_FAR_FIELD_ACTIVE_MASS=
YES

MAX_DEC_VIOLATION=
0
```

For the complete standalone source reconstruction, use:

[`journal/2026-08-28_006d_constructive_linearized_gr_repulsion.md`](journal/2026-08-28_006d_constructive_linearized_gr_repulsion.md)

---

## Reproduce 016F

```bash
ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"

"$PY" \
  simulations/016f_006d_charge_winding_coexistence.py
```

Reference preferred result:

```text
PREFERRED_W=
1.000000000000

PREFERRED_ELL=
0.600000000000

PREFERRED_C=
40.749886771113

PREFERRED_TMAX_OVER_E=
0.180278569163

PREFERRED_REQUIRED_K=
9.589406109611

PREFERRED_CONSERVATIVE_INTEGER_WINDING=
10

PREFERRED_PEAK_STRESS_RELIEF_VS_FINE_006D≈
1400.489
```

Classification:

```text
KINEMATIC_PREFLIGHT=
GREEN

FULL_FIELD_SOLUTION=
NOT_ESTABLISHED
```

---

## Reproduce 016G

```bash
ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"

"$PY" \
  simulations/016g_006d_asymptotic_euler_lagrange_gate.py
```

Reference result:

```text
ASYMPTOTIC_GAP_IDENTITY=
PASS

K_MIN_GREATER_THAN_AMPLITUDE_EXPONENT=
YES_ALL_TESTED_CASES

FINITE_DIFFERENCE_EULER_LAGRANGE_CHECK=
PASS

MINIMAL_ASYMPTOTICALLY_DECOUPLED_CANONICAL_WINDING_EXACT_POWER_LAW_TARGET=
REJECTED

REJECTION_REASON=
EULER_LAGRANGE_FORCE_SIGN_CONFLICT
```

For the preferred $m=2$ case:

```text
AMPLITUDE_POWER_S=
1

K_INFINITY≈
3.154613693

K_INFINITY_SQUARED_MINUS_S_SQUARED≈
8.951587552
```

---

## Reproduce 016H

```bash
ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"

"$PY" \
  simulations/016h_explicit_canonical_field_gravity_gate.py
```

Reference global result:

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

EXTERIOR_FORCE_SIGN_RESOLUTION_STABLE=
True
```

The successful reference log from the research slice was:

```text
results/logs/016h_explicit_canonical_field_gravity_repaired_20260829-145700.log
```

---

# Current Branches

The project should not presently claim that one speculative path has won.

After 016H, three major routes deserve explicit comparison.

### A — 006D-inspired spatially separated field realization

Advantages:

```text
ESTABLISHED_THEORY=
YES

POSITIVE_REPULSIVE_STRESS_CONSTRUCTION=
YES

SPATIAL_DESIGN_PRINCIPLE=
NOW_CLEAR
```

Dominant problems:

```text
ACTUAL_FIELD_SOLUTION=
NO

FULL_STABILITY=
NO

PURE_GR_ENERGY_SCALING=
CATASTROPHIC
```

Probable next established-GR gate:

```text
016I_SPATIALLY_SEPARATED_DRUM_VORTON_VARIATIONAL_GRAVITY_GATE
```

---

### B — Disformal finite-payload continuation

The disformal branch has demonstrated controlled **local total-force reversal** in a reduced model.

But:

```text
FINITE_PAYLOAD_COM_REVERSAL=
NOT_ESTABLISHED

SIMPLE_ORDINARY_MATTER_BRIDGE=
REJECTED
```

If reopened, the next useful calculation is finite-payload integration using the original validated 014D source geometry and/or a dynamic-time payload search.

See the relevant journal entry for details.

---

### C — Protected material-specific scalar interaction

The low-energy protected two-body scalar branch has a parametric EFT survivor.

But:

```text
RELATIVISTIC_UV_COMPLETION=
NOT_ESTABLISHED

GENERIC_UNPROTECTED_MATCHING=
REJECTED

KNOWN_REAL_MATERIAL=
NO
```

This route is more speculative but has a potentially much better interaction-strength scaling than pure GR.

The next buildplan should formally rerank A, B, and C before a major new research slice.

---

# What Has Not Been Established

The project does **not** currently have:

```text
EXACT_NONLINEAR_GR_006D_SOLUTION=
NO

FULL_DYNAMIC_STABILITY=
NO

KNOWN_MATERIAL_REALIZATION=
NO

GLOBAL_POSITIVE_MASS_REPULSION=
NO

FINITE_PAYLOAD_LIFT=
NO

PRACTICAL_ENERGY_REQUIREMENT=
NO

EXPERIMENTAL_ANTIGRAVITY_SIGNAL=
NO

REACTIONLESS_PROPULSION=
NO

PRACTICAL_ANTIGRAVITY_DEVICE=
NO

NEW_PHYSICS_DISCOVERY=
NO

NOVELTY=
NOT_ESTABLISHED
```

---

# Claims Summary

```text
STRONGEST_ESTABLISHED_PROJECT_RESULT=
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

016A_SIMPLE_MICROSTANDOFF_ENERGY_ESCAPE=
NO

016B_FIXED_CHARGE_CAPACITY=
GREEN

016C_SIMPLE_GLOBAL_ELECTROSTATIC_EXACT_REALIZATION=
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
NOT_FOUND_IN_TESTED_63_STATE_VARIATIONAL_SCAN

CURRENT_GR_DESIGN_PRINCIPLE=
SPATIAL_ACTIVE_STRESS_SEGREGATION

CURRENT_INFORMAL_PROGRESS_TOWARD_PRACTICAL_ANTIGRAVITY=
APPROXIMATELY_44_PERCENT_NOT_A_PROBABILITY

PRACTICAL_ANTIGRAVITY_DEVICE=
NO
```

---

# Repository Navigation

For complete detail rather than README-level summaries:

* [`NOTES.md`](NOTES.md) — chronological research record, calculations, failures, and carry-forward context.
* [`RESEARCH_BUILDPLAN.md`](RESEARCH_BUILDPLAN.md) — active priorities, decision gates, and stop rules.
* [`journal/2026-08-28_006d_constructive_linearized_gr_repulsion.md`](journal/2026-08-28_006d_constructive_linearized_gr_repulsion.md) — complete durable record and standalone reconstruction of 006D.
* [`journal/2026-08-29_016a_016h_006d_realizability_and_canonical_field_gates.md`](journal/2026-08-29_016a_016h_006d_realizability_and_canonical_field_gates.md) — complete 016A–016H physical-realizability program.
* [`journal/`](journal/) — additional durable branch records.
* [`FORMATTING_AND_CODE_STANDARDS.md`](FORMATTING_AND_CODE_STANDARDS.md) — required mathematics and code-documentation conventions.
* [`AI_ASSISTANCE.md`](AI_ASSISTANCE.md) — AI-assistance disclosure.

---

# Research Standards

The project follows several strict rules:

1. Established physics before speculative extensions.
2. Reproduce known results before building on them.
3. Use invariant or operational observables.
4. State assumptions and approximation levels explicitly.
5. Check dimensions and limiting cases.
6. Attempt falsification before increasing model complexity.
7. Preserve negative results.
8. Require conservation and stability rather than assuming them.
9. Distinguish local repulsion from global repulsion.
10. Distinguish gravitational effects from fifth forces.
11. Distinguish point acceleration from finite-payload acceleration.
12. Distinguish mathematical possibility from physical realization.
13. Distinguish physical realization from engineering practicality.
14. Require independent reconstruction for central quantitative claims.
15. Never classify an internally generated result as a discovery without independent verification and literature comparison.

---

# AI-Assisted Research

Antigravity Research is a human-directed research project using **ChatGPT by OpenAI** as an AI research and development assistant.

AI assistance includes mathematical derivation, simulation design, Python development, debugging, numerical analysis, falsification work, literature-search assistance, and documentation.

AI-generated results are not assumed correct.

Important claims remain subject to analytical, numerical, dimensional, limiting-case, literature, and independent verification.

Use of ChatGPT does not imply endorsement or sponsorship by OpenAI.

See [`AI_ASSISTANCE.md`](AI_ASSISTANCE.md).

---

# Licensing

Antigravity Research uses separate licenses for software and research materials.

**Software:** MIT OR Apache-2.0, at the user's option.

**Original research materials, generated data, and original figures:** CC0 1.0 Universal.

See [`LICENSE.md`](LICENSE.md) and the `LICENSES/` directory.

Third-party materials retain their original copyright and licensing terms.

---

# Bottom Line

> # **We have a mathematical construction for antigravity-like gravitational repulsion.**

The statement refers specifically to the 006D static linearized-GR construction.

It is:

```text
FINITE=
YES

POSITIVE_ENERGY=
YES

LOCALLY_CONSERVED_AT_LINEARIZED_ORDER=
YES

NEC_WEC_DEC=
PASS

LOCAL_GRAVITATIONAL_FIELD=
OUTWARD

FAR_FIELD_ACTIVE_MASS=
POSITIVE
```

The explicit finite coefficient is

```math

C_{\mathrm{finite}}
=
23.591586299249.

```

The project has since made substantial progress toward understanding whether this stress organization can arise from actual matter.

The strongest realizability preflight reduced a combined charge/winding requirement to approximately

```text
n=
10
```

while retaining a large stress-relief margin.

But the exact minimal canonical power-law realization was then rejected by the 016G asymptotic Euler-Lagrange sign proof, and 016H showed that a healthy explicit canonical field family can contain substantial negative active gravitational density without producing outward gravity.

The frontier is therefore no longer:

> Can gravity mathematically point outward?

That has been answered within the stated model.

The frontier is:

> **Can a stable physical field configuration spatially concentrate negative active stress where gravitational leverage is high, place the compensating positive support where leverage is lower, retain positive total mass, lift a finite payload, and do so at an energetically useful scale?**

That question remains open.

```text
MATHEMATICAL_LOCAL_GRAVITATIONAL_REPULSION=
ESTABLISHED_IN_006D_SCOPE

PHYSICAL_FIELD_REALIZATION=
NOT_ESTABLISHED

FINITE_PAYLOAD_LIFT=
NOT_ESTABLISHED

PRACTICAL_ENERGY_SCALING=
NOT_ESTABLISHED

PRACTICAL_ANTIGRAVITY=
NO

CURRENT_INFORMAL_PROJECT_PROGRESS=
APPROXIMATELY_44_PERCENT_NOT_A_PROBABILITY
```
