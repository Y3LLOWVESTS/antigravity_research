# Antigravity Research

> # **We have a mathematical construction for antigravity-like gravitational repulsion.**

The exact scientific claim supporting that headline is:

> **Within static linearized general relativity, there exists an explicit finite-radius, finite-thickness, nonsingular, positive-energy, locally conserved type-I stress-energy configuration satisfying NEC, WEC, and DEC whose calculated near field points outward while its far-field active mass remains positive.**

This is the project's strongest established project-derived result.

Everything required to reconstruct the **006D headline calculation** is included in this README: the linearized-GR field equation, sign convention, explicit dimensionless source, smoothing widths, finite-thickness profile, energy density, analytic conservation proof, energy-condition proof, positive far-field proof, numerical integrals, quadrature tolerances, convergence data, expected numerical invariants, and a standalone Python reproducer that imports no project modules.

The result is a **constructive linearized-GR stress-energy result**.

It is not an exact nonlinear solution, a stability proof, a material realization, an experimental observation, or a practical antigravity device.

Since establishing 006D, the project has moved substantially further into the question of **physical realizability and practical scaling**. The present leading speculative branch is no longer another modification of the 006D stress tensor. It is a separate hypothesis: a **ground-referenced ultralight scalar fifth force whose large repulsive response appears only in a protected bound material state**.

That fifth-force branch has now advanced through analytical gate **010E-Y**. It has an explicit low-energy nonrelativistic composite construction, but it does **not** yet have a viable relativistic microscopic completion or known material realization.

```text
STRONGEST_ESTABLISHED_PROJECT_RESULT=
006D_FINITE_POSITIVE_ENERGY_LINEARIZED_GR_LOCAL_REPULSION

HEADLINE_CLAIM=
SUPPORTED_WITHIN_STATIC_LINEARIZED_GR

ANALYTIC_CONSERVATION_PROOF=
YES

ANALYTIC_ENERGY_CONDITION_PROOF=
YES

ANALYTIC_POSITIVE_FAR_FIELD_ACTIVE_MASS_PROOF=
YES

FINITE_SOURCE_SPECIFIED_EXPLICITLY=
YES

LOCAL_OUTWARD_FIELD=
NUMERICALLY_REPRODUCIBLE

TWO_NUMERICAL_Z_INTEGRATION_METHODS=
AGREE

EXACT_NONLINEAR_GR=
NOT_ESTABLISHED

DYNAMIC_STABILITY=
NOT_ESTABLISHED

KNOWN_006D_MATERIAL_REALIZATION=
NO

CURRENT_LEADING_SPECULATIVE_BRANCH=
PROTECTED_DINUCLEAR_BOUND_STATE_SCALAR_RESPONSE

CURRENT_LOW_ENERGY_COMPOSITE_EFT=
PARAMETRIC_SURVIVOR

FULL_RELATIVISTIC_UV_COMPLETION=
NOT_ESTABLISHED

KNOWN_REAL_MATERIAL_WITH_REQUIRED_SCALAR_PORTAL=
NO

PRACTICAL_ANTIGRAVITY_DEVICE=
NO

NEW_PHYSICS_DISCOVERY=
NO

NOVELTY=
NOT_ESTABLISHED
```

For detailed chronological research history and negative results, see [`NOTES.md`](NOTES.md).

For active priorities, decision gates, and branch stop rules, see [`RESEARCH_BUILDPLAN.md`](RESEARCH_BUILDPLAN.md).

For dated durable scientific records, see the [`journal/`](journal/) directory.

For repository mathematics and source-code standards, see [`FORMATTING_AND_CODE_STANDARDS.md`](FORMATTING_AND_CODE_STANDARDS.md).

---

# Current Scientific Position

The project now has two scientifically distinct tracks that must not be conflated.

## 1. Established project-derived gravitational result

Simulation 006D constructs an explicit finite stress-energy distribution in **static linearized general relativity** that has:

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

This is a genuine gravitational result: the outward acceleration arises from the metric sourced by the stress-energy tensor.

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

This remains the strongest established project result.

---

## 2. Current speculative practicality branch

The project subsequently asked whether useful antigravity-like acceleration could be obtained without paying the catastrophic classical stress-energy cost of 006D.

The leading surviving speculative mechanism is now:

> **A hypothetical ground-referenced ultralight scalar fifth force whose effective test-body charge becomes extremely large and opposite in sign to the terrestrial source only in a protected bound material state.**

This is **not ordinary general-relativistic antigravity**.

It is an additional force.

The Earth or other source mass acts as an external reaction partner, so the mechanism is not reactionless propulsion.

The leading low-energy architecture currently has the schematic form:

```text
EARTH / GROUND SOURCE
        |
        v
ULTRALIGHT ~5-KM SCALAR
        |
        v
MATERIAL-SPECIFIC TWO-BODY OPERATOR
        |
        v
FIXED BOUND DINUCLEAR MATERIAL IDENTITY
        |
        v
COOPERATIVE HIGH-SPIN INTERNAL STATE
        |
        v
SPIN-LATTICE RESPONSE
        |
        v
MACROSCOPIC PAYLOAD
```

The low-energy construction survives the tests performed through 010E-Y.

Its **relativistic microscopic origin remains unknown**.

---

# Verification Dossier for the 006D Headline Claim

## 1. Conventions and approximation

Use metric signature $(-,+,+,+)$.

In a local orthonormal frame the static type-I source is

```math
T_{\hat\mu\hat\nu}
=
\mathrm{diag}
\left(
\epsilon,
p_r,
p_\phi,
p_z
\right)
```

where $\epsilon$ and the principal pressures have units of energy density.

The calculation is performed in **static linearized general relativity** about Minkowski spacetime.

Write

```math
g_{\mu\nu}
=
\eta_{\mu\nu}
+
h_{\mu\nu}
```

with $|h_{\mu\nu}|\ll1$, and define the trace-reversed perturbation

```math
\bar h_{\mu\nu}
=
h_{\mu\nu}
-
\frac{1}{2}
\eta_{\mu\nu}h
```

In harmonic gauge,

```math
\Box\bar h_{\mu\nu}
=
-\frac{16\pi G}{c^4}
T_{\mu\nu}
```

For a static source,

```math
\nabla^2\bar h_{\mu\nu}
=
-\frac{16\pi G}{c^4}
T_{\mu\nu}
```

Using

```math
h_{00}
=
\frac{1}{2}
\left(
\bar h_{00}
+
\bar h_{11}
+
\bar h_{22}
+
\bar h_{33}
\right)
```

and

```math
g_{00}
=
-\left(
1+\frac{2\Phi}{c^2}
\right)
```

gives

```math
\boxed{
\nabla^2\Phi
=
\frac{4\pi G}{c^2}
\left(
\epsilon+p_r+p_\phi+p_z
\right)
}
```

Define the active source

```math
S
=
\epsilon+p_r+p_\phi+p_z
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
\,d^3x'
```

and the physical weak-field acceleration is

```math
\mathbf a
=
-\nabla\Phi
```

For an axisymmetric source and an on-axis target at $z=h$,

```math
a_z(h)
=
-\frac{2\pi G}{c^2}
\int dz
\int_0^\infty dr\,
r
S(r,z)
\frac{h-z}
{\left[
r^2+(h-z)^2
\right]^{3/2}}
```

The repository convention is:

```text
a_z > 0  -> outward, away from the source slab

a_z < 0  -> inward, toward the source slab
```

---

## 2. Dimensionless normalization

Let

```math
x
=
\frac{r}{h}
```

and

```math
\zeta
=
\frac{z}{h}
```

The target is fixed at

```math
\zeta_{\mathrm{target}}
=
1
```

The finite source occupies

```math
-\delta
\le
\zeta
\le
0
```

with the finest tested regularization

```math
\boxed{
\delta
=
0.00625
}
```

The dimensionless radial constants are

```math
\boxed{
\alpha
=
1.437500564637
}
```

and

```math
\boxed{
\beta
=
4.701437405300
}
```

The smoothing widths for the quoted finite result are

```math
\delta_{\mathrm{inner}}
=
\frac{\delta}{4}
=
0.0015625
```

and

```math
\delta_{\mathrm{outer}}
=
\delta
=
0.00625
```

Therefore

```math
x_-
=
\alpha-\delta_{\mathrm{inner}}
=
1.435938064637
```

```math
x_+
=
\alpha+\delta_{\mathrm{inner}}
=
1.439063064637
```

and

```math
x_{\max}
=
\beta+\delta_{\mathrm{outer}}
=
4.707687405300
```

These constants are sufficient to reconstruct the finite source used for

```math
C_{\mathrm{finite}}
=
23.591586299249
```

---

## 3. Exact radial stress construction

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
\frac{dq}{dx}
```

with

```math
p_z=0
```

and

```math
T_{\hat r\hat z}=0
```

Define the cubic smoothstep

```math
s(u)
=
u^2(3-2u)
```

with

```math
s'(u)
=
6u(1-u)
```

The core and annular branches are

```math
q_{\mathrm{core}}(x)
=
-x
```

and

```math
q_{\mathrm{ann}}(x)
=
-\frac{\alpha^2}{x}
```

Their derivatives are

```math
q'_{\mathrm{core}}(x)
=
-1
```

and

```math
q'_{\mathrm{ann}}(x)
=
\frac{\alpha^2}{x^2}
```

### Region I — inner tension region

For

```math
0\le x<x_-
```

use

```math
q(x)
=
q_{\mathrm{core}}(x)
```

### Region II — smooth inner transition

For

```math
x_-\le x\le x_+
```

define

```math
u
=
\frac{x-x_-}{x_+-x_-}
```

and use

```math
q(x)
=
\left[
1-s(u)
\right]
q_{\mathrm{core}}(x)
+
s(u)q_{\mathrm{ann}}(x)
```

The exact derivative is

```math
q'(x)
=
\left[
1-s(u)
\right]
q'_{\mathrm{core}}(x)
+
s(u)q'_{\mathrm{ann}}(x)
+
\frac{s'(u)}{x_+-x_-}
\left[
q_{\mathrm{ann}}(x)-q_{\mathrm{core}}(x)
\right]
```

### Region III — conserved transfer annulus

For

```math
x_+<x<\beta
```

use

```math
q(x)
=
q_{\mathrm{ann}}(x)
```

### Region IV — finite outer support collar

For

```math
\beta\le x\le\beta+\delta_{\mathrm{outer}}
```

define

```math
v
=
\frac{x-\beta}{\delta_{\mathrm{outer}}}
```

and use

```math
q(x)
=
\left[
1-s(v)
\right]
q_{\mathrm{ann}}(x)
```

with derivative

```math
q'(x)
=
\left[
1-s(v)
\right]
q'_{\mathrm{ann}}(x)
-
\frac{s'(v)}{\delta_{\mathrm{outer}}}
q_{\mathrm{ann}}(x)
```

### Region V — vacuum

For

```math
x>\beta+\delta_{\mathrm{outer}}
```

use

```math
q(x)=0
```

At $x=0$,

```math
q(0)=0
```

```math
p_r(0)=-1
```

```math
p_\phi(0)=-1
```

At the outer boundary,

```math
q(x_{\max})=0
```

and

```math
q'(x_{\max})=0
```

so no singular outer line support is hidden in the construction.

---

## 4. Exact finite-thickness profile

Let $U_0>0$ be an arbitrary positive surface-energy scale.

Define

```math
\varphi_\delta(\zeta)
=
\frac{30}{\delta}
y^2(1-y)^2
```

for

```math
-\delta\le\zeta\le0
```

where

```math
y
=
\frac{\zeta+\delta}{\delta}
```

and set $\varphi_\delta=0$ outside the slab.

The profile is normalized:

```math
\int_{-\delta}^{0}
\varphi_\delta(\zeta)
\,d\zeta
=
1
```

The physical stresses are

```math
p_r^{\mathrm{phys}}(r,z)
=
\frac{U_0}{h}
p_r(x)
\varphi_\delta(\zeta)
```

```math
p_\phi^{\mathrm{phys}}(r,z)
=
\frac{U_0}{h}
p_\phi(x)
\varphi_\delta(\zeta)
```

```math
p_z^{\mathrm{phys}}(r,z)
=
0
```

and

```math
\epsilon^{\mathrm{phys}}(r,z)
=
\frac{U_0}{h}
\epsilon(x)
\varphi_\delta(\zeta)
```

Because $U_0>0$, changing $U_0$ rescales the entire source and field without changing the normalized sign result.

---

## 5. Analytic local-conservation proof

For $x>0$,

```math
p_r(x)
=
\frac{q(x)}{x}
```

and

```math
p_\phi(x)
=
q'(x)
```

Therefore

```math
\frac{dp_r}{dx}
=
\frac{q'}{x}
-
\frac{q}{x^2}
```

and

```math
\frac{dp_r}{dx}
+
\frac{
p_r-p_\phi
}{x}
=
\left(
\frac{q'}{x}
-
\frac{q}{x^2}
\right)
+
\frac{
q/x-q'
}{x}
=
0
```

Thus

```math
\boxed{
\frac{dp_r}{dx}
+
\frac{
p_r-p_\phi
}{x}
=
0
}
```

identically.

The smoothing construction keeps $q$ and $q'$ continuous across the interfaces.

Since

```math
p_z=0
```

and

```math
T_{\hat r\hat z}=0
```

the static $z$-directed conservation equation also vanishes.

Therefore

```math
\boxed{
\partial_\mu T^{\mu\nu}=0
}
```

for the static source on the flat background used by the linearized calculation.

This is **linearized-order conservation**.

It is not yet the exact nonlinear statement

```math
\nabla_\mu T^{\mu\nu}=0
```

in a self-consistently solved curved metric.

---

## 6. Analytic positive-energy and energy-condition proof

Choose

```math
\boxed{
\epsilon(x)
=
\max
\left(
|p_r(x)|,
|p_\phi(x)|
\right)
}
```

with $p_z=0$.

Then

```math
\epsilon\ge0
```

```math
|p_r|\le\epsilon
```

```math
|p_\phi|\le\epsilon
```

```math
|p_z|\le\epsilon
```

For a diagonal type-I stress-energy tensor these are the pointwise dominant-energy-condition inequalities.

Also,

```math
p_i\ge-|p_i|
```

so

```math
\epsilon+p_i
\ge
\epsilon-|p_i|
\ge
0
```

Therefore:

```text
DEC=SATISFIED
WEC=SATISFIED
NEC=SATISFIED
```

No negative energy density is required.

---

## 7. Analytic proof of positive far-field active mass

The dimensionless positive mass factor is

```math
m_\delta
=
2
\int_0^{x_{\max}}
x\epsilon(x)
\,dx
```

Because $\epsilon\ge0$ and the source is nonzero,

```math
m_\delta>0
```

The integrated dimensionless spatial-stress trace is

```math
\tau_\delta
=
2
\int_0^{x_{\max}}
x
\left(
p_r+p_\phi
\right)
\,dx
```

Using $p_r=q/x$ and $p_\phi=q'$,

```math
\tau_\delta
=
2
\int_0^{x_{\max}}
\left(
q+xq'
\right)
\,dx
```

Therefore

```math
\tau_\delta
=
2
\left[
xq(x)
\right]_0^{x_{\max}}
```

The boundary conditions give

```math
q(0)=0
```

and

```math
q(x_{\max})=0
```

hence

```math
\boxed{
\tau_\delta=0
}
```

The integrated active source is therefore

```math
m_{\mathrm{active}}
=
m_\delta+\tau_\delta
=
m_\delta
>
0
```

Thus the far-field active mass is positive analytically.

---

## 8. Exact finite-source local-field integral

Define

```math
A(x)
=
\epsilon(x)+p_r(x)+p_\phi(x)
```

because $p_z=0$.

For the finite vertical slab define

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
\,d\zeta
```

The dimensionless outward field factor is

```math
\boxed{
F_\delta
=
-
\int_0^{x_{\max}}
xA(x)K_\delta(x)
\,dx
}
```

The physical acceleration at the target is

```math
\boxed{
a_z
=
\frac{
2\pi G U_0
}{
c^2
}
F_\delta
}
```

Therefore:

```text
F_delta > 0  -> outward local gravitational acceleration

F_delta < 0  -> inward local gravitational acceleration
```

The total mass is

```math
M
=
\frac{
\pi U_0h^2
}{
c^2
}
m_\delta
```

Eliminating $U_0$ gives

```math
M
=
C
\frac{
a_zh^2
}{
G
}
```

where

```math
\boxed{
C
=
\frac{
m_\delta
}{
2F_\delta
}
}
```

The final numerical sign question is therefore:

```math
F_\delta>0
```

---

## 9. Numerical method

For the finest quoted source:

```text
delta                  = 0.00625
inner smoothing width  = delta / 4
outer collar width     = delta
target z/h             = 1
radial support end      = 4.707687405300
```

Radial integration is performed piecewise across

```text
0
alpha - delta/4
alpha + delta/4
beta
beta + delta
```

using adaptive SciPy `quad`.

Principal tolerances are:

```text
epsabs = 2e-11
epsrel = 2e-11
limit  >= 300
```

The principal 006D field calculation uses **64-point Gauss-Legendre quadrature** in the finite-thickness direction.

A second standalone route performs the same vertical integration with nested adaptive `quad`.

Pointwise energy conditions are sampled at 4001 radial points.

Local conservation is additionally checked over 150 radial control volumes using

```math
q(b)-q(a)
-
\int_a^b p_\phi(x)
\,dx
```

---

## 10. Reproducible numerical invariants

For the explicit finest source:

```text
MASS_FACTOR=
1.110076490539830e+01

INTEGRATED_STRESS_TRACE_FACTOR=
2.922107000813412e-13

ACTIVE_MASS_FACTOR=
1.110076490539859e+01

FIELD_FACTOR_GAUSS_LEGENDRE_64=
2.352695737495157e-01

FIELD_FACTOR_NESTED_ADAPTIVE_QUAD=
2.352695737495351e-01

ABSOLUTE_DIFFERENCE_BETWEEN_FIELD_METHODS=
1.942890293094024e-14

C_GAUSS_LEGENDRE_64=
23.5915862992487

C_NESTED_ADAPTIVE_QUAD=
23.5915862992467

MAX_CONTROL_VOLUME_CONSERVATION_RESIDUAL=
3.103073353827313e-14

MAX_DEC_VIOLATION=
0

MIN_NEC_MARGIN=
0
```

Hence

```math
\boxed{
F_\delta
=
0.2352695737495\ldots
>
0
}
```

and

```math
\boxed{
a_z>0
}
```

The positive sign is not numerically marginal.

---

## 11. Finite-thickness convergence

| $\delta=t/h$ | Mass factor $m_\delta$ | Field factor $F_\delta$ | $C=m_\delta/(2F_\delta)$ |
| -----------: | ---------------------: | ----------------------: | -----------------------: |
|      0.40000 |        11.369718516276 |          0.149453529535 |          38.037638025730 |
|      0.20000 |        11.233723934208 |          0.190019680852 |          29.559369544823 |
|      0.10000 |        11.165255241660 |          0.212604998246 |          26.258214373557 |
|      0.05000 |        11.130897375158 |          0.224509078286 |          24.789414887263 |
|      0.02500 |        11.113686825672 |          0.230618147495 |          24.095429926871 |
|      0.01250 |        11.105073553053 |          0.233712433325 |          23.757986246352 |
|      0.00625 |        11.100764905398 |          0.235269573750 |          23.591586299249 |

The independently established thin conserved reference is

```math
C_{\mathrm{thin}}
=
23.426710175391
```

At the finest tested regularization,

```math
\frac{
C_{\mathrm{finite}}-C_{\mathrm{thin}}
}{
C_{\mathrm{thin}}
}
\approx
0.00704
```

or approximately $0.704%$.

---

## 12. Physical scale restoration

For the finest source,

```math
F_\delta
\approx
0.2352695737495
```

The positive surface-energy scale required for acceleration $a_z$ is

```math
U_0
=
\frac{
a_zc^2
}{
2\pi GF_\delta
}
```

For $a_z=g$,

```math
U_0
\approx
8.93\times10^{27}
\ {\rm J\,m^{-2}}
```

The mass scaling is

```math
\boxed{
M_{\mathrm{equiv}}
=
23.591586299249
\frac{
ah^2
}{
G
}
}
```

For $a=g$ and $h=1\ {\rm m}$,

```math
M_{\mathrm{equiv}}
\approx
3.466\times10^{12}
\ {\rm kg}
```

and

```math
E
=
M_{\mathrm{equiv}}c^2
\approx
3.115\times10^{29}
\ {\rm J}
```

The characteristic compactness is nevertheless only of order

```math
\frac{
GM_{\mathrm{equiv}}
}{
hc^2
}
\sim
2.6\times10^{-15}
```

The principal practical problem is therefore the extraordinary stress-energy requirement, not strong spacetime curvature.

---

## 13. Standalone reproduction

A scientist does not need to trust project modules to reproduce the numerical claim.

Create a clean Python environment:

```bash
python3 -m venv .verify-006d

source .verify-006d/bin/activate

python -m pip install --upgrade pip
python -m pip install numpy scipy
```

Save the following as `verify_006d_from_readme.py` and run:

```bash
python verify_006d_from_readme.py
```

```python
#!/usr/bin/env python3
"""Standalone README verifier for the 006D finite-source construction.

This script imports no ANTIGRAVITY_RESEARCH project modules.

It reconstructs the exact normalized 006D source from the equations and
constants documented in README.md and evaluates:

- positive energy / DEC / WEC / NEC;
- local flat-background stress conservation;
- integrated spatial-stress trace;
- positive far-field active mass;
- outward local axial field;
- the finite-source coefficient C.

Dependencies:
    numpy
    scipy

Claim scope:
    static linearized general relativity
"""

from __future__ import annotations

import math

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad


ALPHA = 1.437500564637
BETA = 4.701437405300

DELTA = 0.00625

INNER_WIDTH = DELTA / 4.0
OUTER_WIDTH = DELTA

RADIAL_EPS = 2.0e-11
CONTROL_EPS = 1.0e-10

GL_ORDER = 64


def smoothstep(u: float) -> float:
    """Return cubic smoothstep."""

    return u * u * (3.0 - 2.0 * u)


def smoothstep_prime(u: float) -> float:
    """Return derivative of cubic smoothstep."""

    return 6.0 * u * (1.0 - u)


def q_and_prime(x: float) -> tuple[float, float]:
    """Return q=x*p_r and dq/dx for the exact README source."""

    if x <= 0.0:
        return 0.0, -1.0

    x_minus = ALPHA - INNER_WIDTH
    x_plus = ALPHA + INNER_WIDTH

    q_core = -x
    qp_core = -1.0

    q_annulus = -(ALPHA * ALPHA) / x
    qp_annulus = (ALPHA * ALPHA) / (x * x)

    if x < x_minus:
        return q_core, qp_core

    if x <= x_plus:
        u = (
            (x - x_minus)
            / (x_plus - x_minus)
        )

        s = smoothstep(u)

        sp = (
            smoothstep_prime(u)
            / (x_plus - x_minus)
        )

        q = (
            (1.0 - s) * q_core
            + s * q_annulus
        )

        qp = (
            (1.0 - s) * qp_core
            + s * qp_annulus
            + sp * (q_annulus - q_core)
        )

        return q, qp

    if x < BETA:
        return q_annulus, qp_annulus

    if x <= BETA + OUTER_WIDTH:
        u = (
            (x - BETA)
            / OUTER_WIDTH
        )

        s = smoothstep(u)

        sp = (
            smoothstep_prime(u)
            / OUTER_WIDTH
        )

        q = (
            (1.0 - s)
            * q_annulus
        )

        qp = (
            (1.0 - s)
            * qp_annulus
            - sp * q_annulus
        )

        return q, qp

    return 0.0, 0.0


def surface_profiles(
    x: float,
) -> tuple[float, float, float]:
    """Return dimensionless epsilon, p_r, and p_phi."""

    q, qp = q_and_prime(x)

    p_r = (
        -1.0
        if x == 0.0
        else q / x
    )

    p_phi = qp

    epsilon = max(
        abs(p_r),
        abs(p_phi),
    )

    return (
        epsilon,
        p_r,
        p_phi,
    )


def radial_breakpoints() -> list[float]:
    """Return exact radial integration interfaces."""

    return [
        0.0,
        ALPHA - INNER_WIDTH,
        ALPHA + INNER_WIDTH,
        BETA,
        BETA + OUTER_WIDTH,
    ]


def radial_integral(
    function,
    eps: float = RADIAL_EPS,
) -> float:
    """Perform piecewise adaptive radial integration."""

    total = 0.0
    points = radial_breakpoints()

    for lower, upper in zip(
        points[:-1],
        points[1:],
    ):
        value, _ = quad(
            function,
            lower,
            upper,
            epsabs=eps,
            epsrel=eps,
            limit=400,
        )

        total += value

    return float(total)


def vertical_profile(
    zeta: float,
) -> float:
    """Return normalized compact profile in zeta=z/h."""

    if zeta < -DELTA or zeta > 0.0:
        return 0.0

    y = (
        (zeta + DELTA)
        / DELTA
    )

    return (
        30.0
        / DELTA
        * y
        * y
        * (1.0 - y)
        * (1.0 - y)
    )


def field_factor_gauss_legendre(
    order: int = GL_ORDER,
) -> float:
    """Evaluate finite-thickness axial field using GL quadrature in z."""

    z_nodes, z_weights = leggauss(
        order
    )

    y_nodes = 0.5 * (
        z_nodes + 1.0
    )

    y_weights = (
        0.5 * z_weights
    )

    bump_weights = (
        y_weights
        * 30.0
        * y_nodes**2
        * (1.0 - y_nodes)**2
    )

    source_zeta = (
        -DELTA
        + DELTA * y_nodes
    )

    separation = (
        1.0 - source_zeta
    )

    def integrand(
        x: float,
    ) -> float:
        epsilon, p_r, p_phi = (
            surface_profiles(x)
        )

        active = (
            epsilon
            + p_r
            + p_phi
        )

        kernel_average = float(
            np.sum(
                bump_weights
                * separation
                / (
                    x * x
                    + separation * separation
                ) ** 1.5
            )
        )

        return (
            x
            * active
            * kernel_average
        )

    return -radial_integral(
        integrand
    )


def field_factor_nested_quad() -> float:
    """Independent z integration using adaptive quadrature."""

    def kernel_average(
        x: float,
    ) -> float:
        value, _ = quad(
            lambda zeta:
                vertical_profile(zeta)
                * (1.0 - zeta)
                / (
                    x * x
                    + (1.0 - zeta) ** 2
                ) ** 1.5,
            -DELTA,
            0.0,
            epsabs=5.0e-13,
            epsrel=5.0e-13,
            limit=250,
        )

        return float(value)

    def integrand(
        x: float,
    ) -> float:
        epsilon, p_r, p_phi = (
            surface_profiles(x)
        )

        active = (
            epsilon
            + p_r
            + p_phi
        )

        return (
            x
            * active
            * kernel_average(x)
        )

    return -radial_integral(
        integrand,
        eps=5.0e-12,
    )


def conservation_residual() -> float:
    """Check q(b)-q(a)-integral p_phi dx over 150 control volumes."""

    outer_radius = (
        BETA + OUTER_WIDTH
    )

    edges = np.linspace(
        0.0,
        outer_radius,
        151,
    )

    maximum = 0.0

    for left, right in zip(
        edges[:-1],
        edges[1:],
    ):
        q_left = q_and_prime(
            float(left)
        )[0]

        q_right = q_and_prime(
            float(right)
        )[0]

        interior_points = [
            point
            for point
            in radial_breakpoints()[1:-1]
            if left < point < right
        ]

        integral, _ = quad(
            lambda x:
                surface_profiles(x)[2],
            float(left),
            float(right),
            epsabs=CONTROL_EPS,
            epsrel=CONTROL_EPS,
            limit=150,
            points=interior_points,
        )

        residual = (
            q_right
            - q_left
            - integral
        )

        maximum = max(
            maximum,
            abs(float(residual)),
        )

    return maximum


def energy_condition_checks(
) -> tuple[float, float]:
    """Return maximum DEC violation and minimum NEC margin."""

    outer_radius = (
        BETA + OUTER_WIDTH
    )

    sample_x = np.linspace(
        0.0,
        outer_radius,
        4001,
    )

    max_dec_violation = 0.0
    min_nec_margin = math.inf

    for x in sample_x:
        epsilon, p_r, p_phi = (
            surface_profiles(
                float(x)
            )
        )

        max_dec_violation = max(
            max_dec_violation,
            abs(p_r) - epsilon,
            abs(p_phi) - epsilon,
            -epsilon,
        )

        min_nec_margin = min(
            min_nec_margin,
            epsilon + p_r,
            epsilon + p_phi,
            epsilon,
        )

    return (
        max_dec_violation,
        min_nec_margin,
    )


def main() -> None:
    """Run complete standalone verification."""

    mass_factor = (
        2.0
        * radial_integral(
            lambda x:
                x
                * surface_profiles(x)[0]
        )
    )

    trace_factor = (
        2.0
        * radial_integral(
            lambda x:
                x
                * (
                    surface_profiles(x)[1]
                    + surface_profiles(x)[2]
                )
        )
    )

    active_mass_factor = (
        mass_factor
        + trace_factor
    )

    field_gl64 = (
        field_factor_gauss_legendre(
            64
        )
    )

    field_nested = (
        field_factor_nested_quad()
    )

    coefficient_gl64 = (
        mass_factor
        / (
            2.0
            * field_gl64
        )
    )

    coefficient_nested = (
        mass_factor
        / (
            2.0
            * field_nested
        )
    )

    max_control_residual = (
        conservation_residual()
    )

    (
        max_dec_violation,
        min_nec_margin,
    ) = energy_condition_checks()

    print(
        "=== README 006D STANDALONE VERIFICATION ==="
    )

    print(
        f"ALPHA={ALPHA:.12f}"
    )

    print(
        f"BETA={BETA:.12f}"
    )

    print(
        f"DELTA={DELTA:.8f}"
    )

    print(
        f"INNER_WIDTH={INNER_WIDTH:.8f}"
    )

    print(
        f"OUTER_WIDTH={OUTER_WIDTH:.8f}"
    )

    print(
        f"OUTER_RADIUS={BETA + OUTER_WIDTH:.12f}"
    )

    print()

    print(
        f"MASS_FACTOR={mass_factor:.15e}"
    )

    print(
        f"TRACE_FACTOR={trace_factor:.15e}"
    )

    print(
        f"ACTIVE_MASS_FACTOR={active_mass_factor:.15e}"
    )

    print(
        f"FIELD_FACTOR_GL64={field_gl64:.15e}"
    )

    print(
        f"FIELD_FACTOR_NESTED={field_nested:.15e}"
    )

    print(
        "FIELD_METHOD_ABS_DIFFERENCE="
        f"{abs(field_gl64-field_nested):.15e}"
    )

    print(
        f"C_GL64={coefficient_gl64:.15e}"
    )

    print(
        f"C_NESTED={coefficient_nested:.15e}"
    )

    print()

    print(
        "MAX_CONTROL_VOLUME_CONSERVATION_RESIDUAL="
        f"{max_control_residual:.15e}"
    )

    print(
        f"MAX_DEC_VIOLATION={max_dec_violation:.15e}"
    )

    print(
        f"MIN_NEC_MARGIN={min_nec_margin:.15e}"
    )

    print()

    print(
        "LOCAL_CONSERVATION="
        + (
            "PASS"
            if max_control_residual < 1.0e-8
            else "FAIL"
        )
    )

    print(
        "DEC="
        + (
            "PASS"
            if max_dec_violation <= 1.0e-12
            else "FAIL"
        )
    )

    print(
        "NEC_WEC="
        + (
            "PASS"
            if min_nec_margin >= -1.0e-12
            else "FAIL"
        )
    )

    print(
        "POSITIVE_FAR_FIELD_ACTIVE_MASS="
        + (
            "YES"
            if active_mass_factor > 0.0
            else "NO"
        )
    )

    print(
        "OUTWARD_LOCAL_FIELD_GL64="
        + (
            "YES"
            if field_gl64 > 0.0
            else "NO"
        )
    )

    print(
        "OUTWARD_LOCAL_FIELD_NESTED="
        + (
            "YES"
            if field_nested > 0.0
            else "NO"
        )
    )


if __name__ == "__main__":
    main()
```

Expected output:

```text
=== README 006D STANDALONE VERIFICATION ===

ALPHA=1.437500564637
BETA=4.701437405300
DELTA=0.00625000
INNER_WIDTH=0.00156250
OUTER_WIDTH=0.00625000
OUTER_RADIUS=4.707687405300

MASS_FACTOR=1.110076490539830e+01
TRACE_FACTOR=2.922107000813412e-13
ACTIVE_MASS_FACTOR=1.110076490539859e+01

FIELD_FACTOR_GL64=2.352695737495157e-01
FIELD_FACTOR_NESTED=2.352695737495351e-01
FIELD_METHOD_ABS_DIFFERENCE=1.942890293094024e-14

C_GL64=2.359158629924866e+01
C_NESTED=2.359158629924672e+01

MAX_CONTROL_VOLUME_CONSERVATION_RESIDUAL=3.103073353827313e-14
MAX_DEC_VIOLATION=0.000000000000000e+00
MIN_NEC_MARGIN=0.000000000000000e+00

LOCAL_CONSERVATION=PASS
DEC=PASS
NEC_WEC=PASS
POSITIVE_FAR_FIELD_ACTIVE_MASS=YES
OUTWARD_LOCAL_FIELD_GL64=YES
OUTWARD_LOCAL_FIELD_NESTED=YES
```

---

## 14. Repository cross-check

The repository reference implementation is:

```text
simulations/006d_finite_thickness_conserved_source.py
```

The recorded codebundle SHA-256 is:

```text
e303b3bb454d19cc16516e189e6db559d1812dad733f9e02bf1ecafce2594d76
```

Run it with:

```bash
ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"

PYTHONPATH="$ROOT/src" \
"$PY" simulations/006d_finite_thickness_conserved_source.py
```

Run the focused regression:

```bash
ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"

PYTHONPATH="$ROOT/src" \
"$PY" -m pytest -q \
tests/known_solutions/test_006c_006d_regressions.py
```

Run the complete known-solution suite:

```bash
ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"

PYTHONPATH="$ROOT/src" \
"$PY" -m pytest -q tests/known_solutions
```

Current verified baseline:

```text
94 passed
```

Validation distinction:

* 006C independently reconstructs the earlier 005B finite-disk result.
* 006D has analytic conservation and energy-condition structure, finite-volume checks, finite-thickness convergence, regression coverage, and the standalone reproducer above.
* A separately authored publication-grade independent implementation of the **entire 006D finite-thickness calculation** would still strengthen the validation further.

---

## 15. What 006D establishes

For the explicit finite source:

```text
FINITE_RADIUS=YES
FINITE_THICKNESS=YES
NONSINGULAR_OUTER_SUPPORT=YES

POSITIVE_ENERGY_DENSITY=YES

LOCAL_CONSERVATION_LINEARIZED_ORDER=YES

DEC=PASS
WEC=PASS
NEC=PASS

POSITIVE_FAR_FIELD_ACTIVE_MASS=YES

OUTWARD_LOCAL_GRAVITATIONAL_FIELD=YES
```

In compact form:

```math
\boxed{
\begin{gathered}
\epsilon\ge0,
\qquad
|p_i|\le\epsilon,
\qquad
\partial_\mu T^{\mu\nu}=0,
\\
M_{\mathrm{active}}>0,
\qquad
F_\delta>0
\end{gathered}
}
```

for the explicit source in static linearized GR.

---

## 16. What 006D does not establish

```text
EXACT_NONLINEAR_EINSTEIN_SOLUTION=
NOT_ESTABLISHED

FULL_CURVED_SPACETIME_CONSERVATION=
NOT_ESTABLISHED

DYNAMIC_STABILITY=
NOT_ESTABLISHED

CONSTITUTIVE_MATERIAL_MODEL=
NOT_ESTABLISHED

KNOWN_FIELD_THEORY_REALIZATION=
NOT_ESTABLISHED

EXPERIMENTAL_ACCESSIBILITY=
NOT_ESTABLISHED

ENERGETIC_PRACTICALITY=
NO

GLOBAL_POSITIVE_MASS_REPULSION=
NOT_ESTABLISHED

REACTIONLESS_PROPULSION=
NOT_ESTABLISHED

PRACTICAL_ANTIGRAVITY_DEVICE=
NO

NEW_PHYSICS_DISCOVERY=
NO
```

The strongest justified classification remains:

```text
CLAIM_CLASSIFICATION=
CONSTRUCTIVE_LINEARIZED_GR_STRESS_ENERGY_RESULT
```

---

# Why the 006D Result Matters

The project began with a foundational question:

> **Does physically respectable positive-energy stress-energy permit local gravitational repulsion?**

Within the explicit static linearized-GR construction, the answer is yes.

The sign of the local gravitational field is therefore not the fundamental obstacle.

General relativity couples to the full stress-energy tensor, not merely rest-mass density.

Relativistic pressure and tension matter gravitationally.

The central classical obstacle is instead the extraordinary magnitude and physical realization of the required stress-energy.

A useful classical design principle is:

> **Maximize physically realizable relativistic tension per unit positive energy while preserving local conservation and stability.**

However, the project has also established a more general static scaling obstruction.

For a broad one-sided static conserved-DEC source class,

```math
M
\gtrsim
\frac{ah^2}{G}
```

so even an ideal coefficient of order unity requires approximately

```math
1.47\times10^{11}\ {\rm kg}
```

of mass-equivalent stress-energy for $1g$ at a one-meter standoff.

The explicit 006D coefficient is larger.

Small additional improvements in $C$ therefore do not solve practical antigravity.

---

# Important Terminology

## Local gravitational repulsion

A neutral test body in a specified region experiences **gravitational** acceleration away from the source region.

```text
PROJECT_STATUS=
ESTABLISHED_IN_KNOWN_GR_EXAMPLES_AND_006D_MODEL
```

---

## Global gravitational repulsion

The asymptotic field of an isolated positive-total-mass system points outward.

```text
PROJECT_STATUS=
NOT_ESTABLISHED
```

The 006D source has positive far-field active mass.

---

## Ground-referenced antigravity-like fifth force

A body is pushed upward by an additional interaction with an external source such as the Earth.

```text
MOMENTUM_CONSERVATION_PROBLEM=
NO_IF_EXTERNAL_SOURCE_IS_INCLUDED

PRACTICAL_REALIZATION=
NOT_ESTABLISHED
```

This is the category containing the current 010E material-scalar branch.

---

## Self-contained reactionless antigravity

An isolated apparatus changes the motion of its center of energy without an external momentum reservoir.

```text
PROJECT_STATUS=
NOT_ESTABLISHED

INTERNAL_RECIPROCAL_FORCE_SELF_ACCELERATION=
REJECTED
```

---

## Practical antigravity

A finite, controllable, stable apparatus produces useful macroscopic repulsion at physically realizable material and energy scales.

```text
PROJECT_STATUS=
NO
```

---

# Research Program and Major Results

## 001 — Established GR baselines

The repository reproduced:

* Schwarzschild-de Sitter / Kottler attraction-repulsion transition;
* positive-$\Lambda$ geodesic defocusing;
* invariant tidal behavior through geodesic deviation.

For Kottler spacetime,

```math
a(r)
=
-\frac{GM}{r^2}
+
\frac{\Lambda c^2r}{3}
```

The effect is real, but the observed cosmological constant is far too weak for laboratory antigravity.

---

## 002 — Stress-energy sign criterion

For a perfect fluid,

```math
\frac{\ddot{\xi}}{\xi}
=
-\frac{4\pi G}{3c^2}
\left(
\epsilon+3p
\right)
+
\frac{\Lambda c^2}{3}
```

With

```math
p=w\epsilon
```

positive-energy defocusing is possible for

```math
w<-\frac13
```

Negative energy is therefore not required merely to reverse the local gravitational sign.

---

## 003 — Localizing vacuum-like stress

A finite $w=-1$ region cannot simply taper to vacuum without acquiring boundary stresses.

The tested de Sitter-core / Schwarzschild-exterior thin-shell route showed that obtaining a negative-mass exterior requires exotic shell properties incompatible with the ordinary WEC/DEC assumptions used in that search.

---

## 004 — Einstein-Maxwell / Reissner-Nordström

The metric contains

```math
f(r)
=
1
-
\frac{2GM}{c^2r}
+
\frac{GQ^2}{4\pi\epsilon_0c^4r^2}
```

and neutral-particle gravitational behavior changes sign at

```math
r_{\mathrm{rep}}
=
\frac{Q^2}{4\pi\epsilon_0Mc^2}
```

This is an exact established-theory example of local gravitational repulsion with positive Maxwell energy.

Useful laboratory acceleration requires catastrophic electric fields.

---

## 005 — Relativistic tension

For a planar membrane with tangential tension

```math
\tau=qU
```

repulsion occurs for

```math
q>\frac12
```

while DEC permits

```math
q\le1
```

so

```math
\frac12<q\le1
```

contains positive-energy, DEC-compatible repulsive stress.

The finite supported 005B architecture produced

```math
M_{\mathrm{equiv}}
\approx
79.753148116012
\frac{ah^2}{G}
```

and was later independently reconstructed in 006C.

---

## 006 — Finite conserved positive-energy source

006B produced the thin conserved coefficient

```math
C_{\mathrm{thin}}
=
23.426710175391
```

006C independently reconstructed the earlier finite-disk result.

006D then produced the finite-thickness, finite-support source documented above:

```text
FINITE_SOURCE=YES
POSITIVE_ENERGY=YES
LOCAL_CONSERVATION_LINEARIZED_ORDER=YES
NEC_WEC_DEC=PASS
LOCAL_FIELD_DIRECTION=OUTWARD
FAR_FIELD_ACTIVE_MASS=POSITIVE
```

with

```math
C_{\mathrm{finite}}
=
23.591586299249
```

---

## 007 — Established quantum-field routes

The project examined Casimir and quantum-negative-energy routes.

Important conclusions:

* complete apparatus stress-energy must be included;
* negative vacuum energy cannot be counted while ignoring supports and plates;
* static Casimir arrangements did not provide a practical macroscopic escape;
* free-field quantum-energy-inequality scaling makes useful macroscopic acceleration extraordinarily small in the tested established-QFT route.

```text
ESTABLISHED_QFT_MACROSCOPIC_PRACTICAL_ESCAPE=
NOT_FOUND
```

---

## 008 — Field realizability and stability

The project investigated whether known classical fields could realize the 006D stress pattern.

Important results include:

* wall/current-loop support did not materially change the classical scaling;
* canonical scalar fields can locally represent relevant stress structures;
* static scalar configurations face Derrick-type stability problems;
* one charged complex scalar cannot exactly reproduce the target;
* finite ungauged winding constructions fail at termination;
* restricted local gauge-assisted boundary takeover remains mathematically possible but does not solve the energy scale.

```text
KNOWN_PRACTICAL_FIELD_REALIZATION_OF_006D=
NO
```

---

# 009 — Fifth-Force Program

The project then investigated forces beyond ordinary GR.

These mechanisms must not be confused with the 006D gravitational construction.

## Ordinary unscreened vector

The optimistic ordinary-matter half-space ceiling was approximately

```math
\frac{a_{\max}}{g}
\approx
2.21\times10^{-2}
```

under the tested constraints.

That route does not reach practical $1g$ acceleration.

---

## Ordinary opposite-sign scalar preflight

An earlier unscreened, ordinary-matter opposite-sign scalar benchmark reached only approximately

```math
\frac{a_{\max}}{g}
\approx
7.33\times10^{-4}
```

under the stellar-normalized assumptions used there.

This result remains valid for that branch.

It does **not** exclude the later material-state-dependent scalar architecture developed in 010E.

---

## Gold-null vector direction

A material-blind phenomenological vector direction could formally reach large force in a low-energy recast.

Simple UV completions were severely damaged by:

* electroweak $SU(2)_L$ consistency;
* unavoidable axial coupling;
* longitudinal-mode and stellar constraints;
* vectorlike-partner requirements;
* low effective UV scales.

A representative preflight at the $1g$ benchmark found:

```text
UNAVOIDABLE_AXIAL_COUPLING_AT_1G=
1.064556829114e-11

STRONG_NDA_LAMBDA_U_MAX_GEV=
582.021760

STRONG_NDA_LAMBDA_D_MAX_GEV=
601.574737
```

No satisfactory simple healthy UV completion was established.

---

## Momentum conservation

Reciprocal forces internal to an isolated system cannot accelerate its total center of energy.

Therefore:

```text
SELF_CONTAINED_INTERNAL_FIFTH_FORCE_LIFT=
REJECTED

GROUND_REFERENCED_EXTERNAL_SOURCE_FORCE=
NOT_REJECTED_BY_THIS_ARGUMENT
```

---

# 010 — Modified Gravity, Equivalence, and the Material-Specific Scalar Branch

## 010A — Healthy universal scalar-tensor sign gate

A healthy universally coupled canonical scalar adds attraction or screens toward GR.

Metric $f(R)$ gives the familiar short-range limit

```math
\frac{F}{F_{\mathrm{GR}}}
\rightarrow
\frac43
```

rather than repulsion.

---

## 010B — Extra spin-2 and vector sign gate

Healthy positive-residue spin-2 exchange adds attraction.

A healthy spin-1 field can repel like charges, but this requires an independent material charge and therefore returns to fifth-force physics.

Repulsive spin-2 exchange requires pathological sign choices such as negative residue/ghost behavior.

---

## 010C — Scalarization and nonminimal scalar gates

A compactness estimate for spontaneous scalarization gives

```math
|\beta|
\frac{GM}{Rc^2}
=
\frac{\pi^2}{12}
```

A neutron-star compactness of about $0.2$ gives

```math
|\beta|_{\mathrm{crit}}
\approx
4.11
```

whereas laboratory-density matter requires enormous $|\beta|$.

The standard spontaneous-scalarization mechanism therefore does not provide a laboratory escape.

---

## 010D — Equivalence and center-of-energy gate

Define

```math
\chi
=
\frac{
m_{\mathrm{passive}}
}{
m_{\mathrm{inertial}}
}
```

Then

```math
a=\chi g
```

Ordinary free fall corresponds to

```math
\chi=1
```

hovering requires

```math
\chi=0
```

and upward gravitational acceleration of magnitude $g$ would require

```math
\chi=-1
```

Ordinary WEP-preserving internal-energy changes do not provide this switch.

Internal conservative forces also cannot self-accelerate an isolated center of energy.

---

# 010E — Material-State-Dependent Scalar Program

The project then investigated whether a material could possess a **state-dependent scalar charge** that is ordinary in its inactive state and extremely large with the opposite sign in an activated state.

This is currently the leading speculative practicality branch.

The working phenomenological force benchmark is

```math
\lambda
=
5000\ {\rm m}
```

```math
\alpha_Y
=
2.0\times10^{-4}
```

with

```math
\alpha_{\mathrm{source}}
=
10^{-2}
```

The mediator mass is

```math
m_\phi
=
\frac{\hbar c}{\lambda}
=
3.946539608\times10^{-11}\ {\rm eV}
```

For the selected Earth/ground half-space benchmark, approximately $1g$ upward acceleration requires

```math
\alpha_{\mathrm{activated}}
=
-1.558991777087370\times10^5
```

This is an enormous activated response.

The microscopic additional coupling required per nucleon is nevertheless only of order

```math
g_N
\sim
6.01\times10^{-14}
```

because the macroscopic scalar charge is coherent.

---

## Experimental-bound status of the working point

A historical intermediate-range Yukawa constraint provides a conservative numerical anchor.

The selected

```math
\alpha_Y
=
2\times10^{-4}
```

working point is a factor of ten below the historical

```math
\alpha_Y
\sim
2\times10^{-3}
```

ceiling used in the project preflight.

However:

```text
CURRENT_EXACT_MODERN_5KM_NUMERICAL_MARGIN=
NOT_CLOSED
```

The modern exclusion curve has not yet been reconstructed as a machine-readable numerical boundary.

The README therefore does **not** claim a precise current experimental safety margin.

---

# 010E-O through 010E-Y — Current Frontier Development

## 010E-O — Explicit microscopic lattice state

A discrete low-energy $Z_2$-even lattice architecture replaced an arbitrary continuous phenomenological state function.

This established that the desired material-state dependence could be represented by an explicit microscopic low-energy model.

It did not establish a real material or UV completion.

---

## 010E-P / Q — Localized hidden carrier rejected

A light hidden carrier associated with individual atomic-scale cells initially matched the scalar coupling parametrically.

Localization then killed the interpretation.

For a $1,{\rm eV}$ particle localized to an approximately $5.5\times10^{-10},{\rm m}$ cell,

```math
pc
\sim
\frac{\hbar c}{a}
\sim
359\ {\rm eV}
```

which is far outside the intended low-energy EFT.

The required localization-compatible mass and the scalar-naturalness upper mass failed to overlap by roughly two orders of magnitude.

Therefore:

```text
ONE_POINTLIKE_UNPROTECTED_HIDDEN_CARRIER_PER_CELL=
REJECTED_BY_LOCALIZATION_NATURALNESS
```

---

## 010E-Q / R / S — Collective compact phase

A collective compact relative phase replaced the localized carrier.

This produced an explicit low-energy state-dependent scalar source with technically small portal coefficients.

A unique normal vacuum was then constructed and the invariant material-control burden optimized.

These gates were important because they removed arbitrary state functions and quantified the true free-energy burden.

However, the compact hidden phase is **not currently required** in the minimal leading architecture.

Later finite-size analysis reopened a simpler direct material-state scalar coupling.

---

## 010E-T — Gauge-invariant electronic high-spin projector

The project identified a concrete low-energy electronic order parameter.

Within an $S=0,1,2$ subspace, define

```math
x=S(S+1)
```

and

```math
P_{\mathrm{HS}}
=
\frac{
x(x-2)
}{
24
}
```

Then

```math
P_{\mathrm{HS}}(S=0)=0
```

```math
P_{\mathrm{HS}}(S=1)=0
```

```math
P_{\mathrm{HS}}(S=2)=1
```

This supplies a rotationally scalar, time-reversal-even, low-energy electromagnetic-gauge-invariant high-spin projector.

The required host-hidden energy per dense transition-metal-like active site lies below characteristic several-eV electronic interaction scales.

However, a direct unprotected electron-mass scalar portal was rejected by radiative naturalness.

```text
DIRECT_UNPROTECTED_ELECTRON_MASS_PORTAL=
REJECTED
```

---

## 010E-U — Spin-lattice bridge

The required material-dependent energy was mapped onto ordinary spin-lattice structural physics.

A representative $K=20,{\rm eV/\AA^2}$ point required a scalar-induced bond force of approximately

```math
0.97\ {\rm eV/\AA}
```

or

```math
1.55\times10^{-9}\ {\rm N}
```

with induced displacement approximately

```math
0.048\ {\rm \AA}
```

inside the selected model.

These are ordinary chemical-scale quantities.

The fundamental origin of the hidden scalar-to-bond force remained unknown.

A simple fundamental electron-current mediator was also rejected by the electron anomalous magnetic moment preflight.

---

## 010E-V — Finite-size scalar stability

This gate corrected an important earlier assumption.

A negative local infinite-medium effective mass squared does not automatically imply instability in a finite object.

For a spherical body of radius $R$ with

```math
m_{\mathrm{in}}^2
=
-\mu^2
```

the first zero mode satisfies

```math
\mu\cot(\mu R)
=
-m_\phi
```

or, with $x=\mu R$,

```math
x\cot x
=
-m_\phi R
```

For the one-ton benchmark,

```text
FINITE_SPHERE_X_CRITICAL=
1.570875308300910
```

The selected direct-material scalar susceptibility lies below this threshold.

This substantially changed the ranking of the branch.

---

## 010E-W — Off-state purity

Because the activated scalar response is extremely large, only a tiny unwanted population of activated material can be tolerated in the inactive state.

The conservative target-equivalent leakage allowance used by the project is

```math
f_{\mathrm{leak}}
=
5.772961445324848\times10^{-7}
```

A near-coexistence single-site spin-crossover system at room temperature fails badly because thermal high-spin occupation is too large.

Simple continuous structural selectors also fail because:

* scalar-induced displacement generates off-state charge;
* zero-point fluctuations generate charge;
* thermal fluctuations generate charge.

A universal high-spin scalar portal also fails because unrelated high-spin matter would carry the enormous activated charge.

Therefore:

```text
MATERIAL_SELECTIVITY=
DOMINANT_MICROPHYSICAL_REQUIREMENT
```

---

# 010E-X — Cooperative Exact Selector

The material selector was factorized as

```math
Q_N
=
B_{\mathrm{material}}
\prod_{i=1}^{N}
P_{\mathrm{HS},i}
```

where:

* $B_{\mathrm{material}}$ fixes the bound material identity;
* the $P_{\mathrm{HS},i}$ factors select the activated internal state.

This permits

```math
[
B_{\mathrm{material}},
H_{\mathrm{control}}
]
=
0
```

while

```math
[
Q_N,
H_{\mathrm{control}}
]
\ne
0
```

so exact material identity and switchability are not logically incompatible.

Thermal leakage falls rapidly with cluster size, approximately through

```math
W_N
=
5^N
\exp
\left(
-\frac{
NE_s
}{
k_BT
}
\right)
```

while maximal scalar susceptibility grows linearly with $N$:

```math
|\Delta m_\phi^2|
\propto
N
\frac{
n_{\mathrm{site}}
g_{\mathrm{site}}^2
}{
4k_BT
}
```

Therefore a viable cluster requires

```math
N_{\min}
\le
N
\le
N_{\max}
```

The one-ton benchmark gives:

```text
300 K:
N_MIN=11
N_MAX=21

100 K:
N_MIN=2
N_MAX=7

77 K:
N_MIN=2
N_MAX=5

20 K:
N_MIN=1
N_MAX=1

10 K:
NO_WINDOW

4.2 K:
NO_WINDOW
```

This produced a non-intuitive result:

> **Colder is not always better.**

Lower temperature suppresses unwanted thermal activation but increases equilibrium scalar susceptibility as $1/T$.

---

## Dinuclear survivor

The lowest-complexity surviving cluster is $N=2$.

For the one-ton benchmark:

```text
DINUCLEAR_STABILITY_T_MIN_K=
28.13102372293623

DINUCLEAR_LEAKAGE_T_MAX_K=
101.8315502857560
```

At $77,{\rm K}$:

```text
DINUCLEAR_ALL_HS_LEAKAGE=
1.989338055378181e-9

DINUCLEAR_LEAKAGE_MARGIN=
290.1950942786034

DINUCLEAR_MU_R=
0.9556137730170507

FINITE_SPHERE_X_CRITICAL=
1.570875308300910

DINUCLEAR_STABILITY_MARGIN=
1.643839124818559
```

The minimum selected model-side control scale is approximately

```math
0.07919\ {\rm eV/site}
```

or

```math
0.15839\ {\rm eV/dimer}
```

corresponding to an invariant free-energy scale of approximately

```math
1.06\times10^8\ {\rm J}
```

per $1000,{\rm kg}$ benchmark payload.

This is **not** a demonstrated device energy requirement.

It is the free-energy scale of the effective material model.

---

# 010E-Y — Local Composite Matching

010E-Y attacked the strongest remaining low-energy objection:

> Must a large scalar charge on a bound material state necessarily appear as the same large scalar charge on its isolated constituents?

Within a strict particle-number-conserving nonrelativistic composite EFT, the answer is **no**.

Introduce constituent fields $A$ and $B$ and an emergent bound-state field $D$.

Assign

```math
N_A=1
```

```math
N_B=1
```

```math
N_D=2
```

with total number

```math
N
=
N_A+N_B+2N_D
```

Use the local mixing interaction

```math
H_{\mathrm{mix}}
=
h
\left(
D^\dagger AB
+
A^\dagger B^\dagger D
\right)
```

and couple the scalar only to the dimer:

```math
H_\phi
=
g_D\phi D^\dagger D
```

Because

```math
[H,N]=0
```

the isolated one-particle sectors cannot access the dimer state.

Thus in the strict NR EFT,

```math
\frac{dE_A}{d\phi}
=
0
```

and

```math
\frac{dE_B}{d\phi}
=
0
```

while the dressed bound state can have

```math
\frac{dE_{\mathrm{bound}}}{d\phi}
=
g_DZ_D
```

where $Z_D$ is the dimer probability.

---

## Numerical dimer match

The target dinuclear scalar coupling is

```text
TARGET_DINUCLEAR_COUPLING=
8.638353631211470e-12
```

The selected two-channel model used:

```text
DIMER_BARE_DETUNING_EV=
-5.0

DIMER_PAIR_MIXING_EV=
0.8783524469661568
```

and required

```text
BARE_DIMER_SCALAR_COUPLING=
8.904546001587151e-12
```

The dressed bound state remains approximately $97%$ dimer-like:

```text
DIMER_FRACTION_AT_ZERO_PHI=
0.9717316000818251

DIMER_FRACTION_AT_EARTH_PHI=
0.9701060143517443
```

The desired dressed charge is reproduced:

```text
DRESSED_DIMER_CHARGE_AT_EARTH_PHI=
8.638353631211473e-12
```

An independent finite-difference Feynman-Hellmann check gives relative error

```text
3.079119804066939e-10
```

Therefore:

```text
FEYNMAN_HELLMANN=
PASS

ISOLATED_A_EXTRA_SCALAR_CHARGE=
0

ISOLATED_B_EXTRA_SCALAR_CHARGE=
0

BOUND_DIMER_EXTRA_SCALAR_CHARGE=
NONZERO
```

within this strict low-energy EFT.

---

# Independent Two-Body Contact Representation

The same low-energy response was independently represented as

```math
\mathcal H_{\phi,2}
=
C_\phi
\phi
A^\dagger B^\dagger BA
```

This operator vanishes exactly in isolated one-body sectors.

For a representative pair radius

```math
a
=
3\ {\rm \AA}
```

the required coefficient is

```math
C_\phi
=
9.536416387852626\times10^{-20}
\ {\rm eV^{-3}}
```

The atomic EFT cutoff is approximately

```math
\Lambda_{\mathrm{EFT}}
\sim
657.7566\ {\rm eV}
```

and the corresponding dimensionless Wilson strength is

```math
C_\phi
\Lambda_{\mathrm{EFT}}^3
=
2.713818830692468\times10^{-11}
```

The required pair operator is therefore perturbatively small at the selected atomic EFT cutoff.

Correct classification:

```text
BOUND_STATE_SPECIFIC_SCALAR_RESPONSE=
EXPLICIT_LOCAL_LOW_ENERGY_EFT_CONSTRUCTION

INDEPENDENT_DIMER_AND_CONTACT_REPRESENTATIONS=
AGREE
```

This does **not** prove a relativistic microscopic origin.

---

# The Critical UV Problem

The low-energy composite model survives.

Generic high-energy realizations do not.

## Fundamental relativistic dimer is rejected

The mass-equivalent energy of the dinuclear object is approximately

```math
1.34\times10^{11}\ {\rm eV}
```

or about $134,{\rm GeV}$.

Treating it as a fundamental relativistic particle gives corrections to the ultralight scalar mass of order

```text
RELATIVISTIC_FERMION_DIMER_LOOP_TO_TARGET_MASS2=
1.155053548350539e19

RELATIVISTIC_SCALAR_DIMER_LOOP_TO_TARGET_MASS2=
2.310107096701078e19
```

Therefore:

```text
FUNDAMENTAL_RELATIVISTIC_DIMER_CARRIER=
REJECTED_BY_ULTRALIGHT_SCALAR_NATURALNESS
```

The dimer must be understood, if the branch is viable at all, as an **emergent nonrelativistic material degree of freedom**.

---

## Generic unprotected relativistic matching is rejected

A generic loop factor is

```math
\frac{1}{16\pi^2}
\approx
6.3326\times10^{-3}
```

The allowed ordinary-matter target-equivalent leakage is only

```math
f_{\mathrm{leak}}
=
5.77296\times10^{-7}
```

The generic loop scale exceeds the leakage allowance by approximately

```math
1.10\times10^4
```

Therefore:

```text
GENERIC_UNPROTECTED_RELATIVISTIC_UV_MATCH=
REJECTED
```

A successful microscopic theory would require an **exact or technically natural protection mechanism** beyond ordinary loop suppression.

---

# Current Active Frontier

The current highest-information scientific question is now very specific:

> **Can a local relativistic microscopic theory matched to Standard Model constituents and a technically natural ultralight scalar generate the required protected two-body material Wilson coefficient while suppressing all induced one-body ordinary-matter scalar charge below the experimental leakage limit and preserving the ultralight mediator mass?**

The desired low-energy operator is schematically

```math
\mathcal H_{\phi,2}
=
C_\phi
\phi
A^\dagger B^\dagger BA
```

with representative

```math
C_\phi
\approx
9.54\times10^{-20}
\ {\rm eV^{-3}}
```

for the $3,{\rm \AA}$ normalization.

The relativistic theory must **not** generate dangerous ordinary one-body operators above approximately

```math
5.77\times10^{-7}
```

of the target-equivalent activated response.

It must also preserve

```math
m_\phi
\approx
3.95\times10^{-11}\ {\rm eV}
```

without fine-tuned cancellation.

---

# Current Branch Stop Rule

The direct material-scalar branch should be closed or strongly demoted if a robust calculation establishes any of the following:

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
LOCAL_RELATIVISTIC_MATCH_CANNOT_GENERATE_REQUIRED_TWO_BODY_OPERATOR
```

```text
BOUND_STATE_SPECIFIC_RESPONSE_REQUIRES_FORBIDDEN_CONSTITUENT_CHARGE
```

```text
CURRENT_EXACT_5KM_FORCE_BOUND_EXCLUDES_USEFUL_PARAMETER_REGION
```

```text
STELLAR_OR_COSMOLOGICAL_CONSTRAINTS_ELIMINATE_THE_USEFUL_REGION
```

A failed branch should be documented and closed rather than rescued indefinitely by adding new hidden fields or arbitrary tuning.

---

# Major Negative Results Worth Preserving

The following routes have been rejected or strongly disfavored in their tested forms:

```text
NEGATIVE_MASS_THIN_SHELL_ENGINEERING=
REJECTED_UNDER_TESTED_ORDINARY_ENERGY_CONDITIONS

PRACTICAL_REISSNER_NORDSTROM=
REJECTED_BY_ELECTRIC_FIELD_SCALE

STATIC_CASIMIR_PRACTICAL_MACROSCOPIC_ROUTE=
DEPRIORITIZED_OR_CLOSED_IN_TESTED_SCOPE

FREE_FIELD_QEI_MACROSCOPIC_ROUTE=
STRONGLY_DEPRIORITIZED

ORDINARY_UNSCREENED_VECTOR_1G=
NO

ORDINARY_UNSCREENED_OPPOSITE_SIGN_SCALAR_1G=
NO_IN_EARLIER_TESTED_BRANCH

MONOLITHIC_CHAMELEON_TERRESTRIAL_RESCUE=
REJECTED

SIMPLE_GOLD_NULL_VECTOR_UV_COMPLETIONS=
STRONGLY_DISFAVORED

UNIVERSAL_HEALTHY_SCALAR_TENSOR_SIGN_REVERSAL=
NO

HEALTHY_POSITIVE_RESIDUE_SPIN2_SIGN_REVERSAL=
NO

LAB_SPONTANEOUS_SCALARIZATION=
NO

INTERNAL_RECIPROCAL_SELF_THRUST=
NO

LIGHT_LOCALIZED_HIDDEN_CARRIER_PER_CELL=
REJECTED

MATERIAL_CREATED_HIDDEN_CONDENSATE=
REJECTED_AS_PRACTICAL_ROUTE

DIRECT_UNPROTECTED_ELECTRON_MASS_PORTAL=
REJECTED

SIMPLE_FUNDAMENTAL_ELECTRON_CURRENT_MEDIATOR=
REJECTED

LINEAR_CONTINUOUS_STRUCTURAL_SELECTOR=
REJECTED

SIMPLE_EVEN_STRUCTURAL_SELECTOR=
REJECTED

UNIVERSAL_HIGH_SPIN_SCALAR_PORTAL=
REJECTED

ACCIDENTALLY_TUNED_POLYNOMIAL_SELECTOR=
REJECTED

FUNDAMENTAL_RELATIVISTIC_DIMER=
REJECTED

GENERIC_UNPROTECTED_RELATIVISTIC_MATCHING=
REJECTED
```

These negative results are scientifically valuable because they reduce the space of viable mechanisms.

---

# Current Claims Ledger

## Supported or established within stated scope

* Local gravitational repulsion exists in established GR.
* Positive energy does not by itself forbid local gravitational repulsion.
* Negative total mass is not required for a locally repulsive near field.
* Relativistic negative pressure and tension can contribute repulsively.
* Reissner-Nordström provides an exact known example of local gravitational repulsion.
* The 005B finite supported disk result was independently numerically reconstructed.
* The 006B thin locally conserved source has $C_{\mathrm{thin}}=23.426710175391$ within its stated architecture.
* The 006D finite source is positive-energy, finite-radius, finite-thickness, locally conserved at linearized order, NEC/WEC/DEC-compatible, locally repulsive, and positive in far-field active mass.
* The best tested finite 006D coefficient is $C_{\mathrm{finite}}=23.591586299249$.
* Static classical constructions investigated retain severe $ah^2/G$ scaling.
* Internal reciprocal forces cannot self-accelerate an isolated center of energy.
* Finite-size scalar stability is weaker than the corresponding infinite-medium negative-$m^2$ criterion.
* An exact factorized material-selector architecture exists at the low-energy Hilbert-space level.
* A nonempty cooperative cluster-size window exists in the selected material-scalar model.
* A dinuclear cluster is the lowest-complexity survivor in the selected benchmark.
* A strict particle-number-conserving NR composite EFT can give a bound dimer nonzero scalar response while isolated constituents have zero additional scalar response.
* Feynman-Hellmann and an independent two-body-contact representation agree for the selected low-energy model.

---

## Parametric survivors, not discoveries

```text
PROTECTED_DINUCLEAR_BOUND_STATE_SCALAR_RESPONSE=
PARAMETRIC_LOW_ENERGY_SURVIVOR

FINITE_SIZE_DINUCLEAR_SELECTOR_WINDOW=
PASS_IN_SELECTED_MODEL

TWO_BODY_CONTACT_OPERATOR=
LOW_ENERGY_MATCH_PASS
```

These are project-derived theoretical constructions.

They do not demonstrate that Nature contains the required interaction.

---

## Rejected in tested scope

* negative-mass shell engineering under ordinary energy conditions;
* practical RN electric-field scaling;
* practical complete Casimir apparatus route;
* unscreened ordinary-matter vector order-$1g$ route;
* ordinary unscreened opposite-sign scalar order-$1g$ route;
* simple healthy gold-null vector UV realizations;
* standard laboratory spontaneous scalarization;
* WEP-preserving internal-state gravity switching;
* internal fifth-force self-thrust;
* localized light hidden carrier;
* direct electron-mass portal;
* simple electron-current mediator;
* unprotected continuous material selectors;
* universal high-spin scalar charge;
* fundamental relativistic dimer carrier;
* generic unprotected relativistic UV matching.

---

## Not established

```text
EXACT_NONLINEAR_GR_VERSION_OF_006D=
NOT_ESTABLISHED

DYNAMIC_STABILITY_OF_006D=
NOT_ESTABLISHED

KNOWN_006D_MATERIAL_REALIZATION=
NO

UNIVERSAL_LOWER_BOUND_ON_C=
NOT_ESTABLISHED

PROTECTED_RELATIVISTIC_TWO_BODY_SCALAR_COMPLETION=
NOT_ESTABLISHED

ACTUAL_MICROSCOPIC_ORIGIN_OF_C_PHI=
NOT_ESTABLISHED

KNOWN_REAL_MATERIAL_WITH_REQUIRED_SCALAR_PORTAL=
NO

CURRENT_EXACT_5KM_NUMERICAL_BOUND=
NOT_CLOSED

FULL_STELLAR_SAFETY=
NOT_ESTABLISHED

FULL_COSMOLOGICAL_SAFETY=
NOT_ESTABLISHED

GLOBAL_POSITIVE_MASS_ANTIGRAVITY=
NOT_ESTABLISHED

REACTIONLESS_PROPULSION=
NOT_ESTABLISHED

PRACTICAL_ANTIGRAVITY_DEVICE=
NO

NEW_PHYSICS_DISCOVERY=
NO

NOVELTY=
NOT_ESTABLISHED
```

---

# Regression Status

The current verified known-solution regression baseline is:

```text
94 passed
```

Run it from the project root with:

```bash
ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"

PYTHONPATH="$ROOT/src" \
"$PY" -m pytest -q tests/known_solutions
```

The late 009/010 frontier calculations were primarily performed as analytical/literature/preflight gates.

They should not be described as permanent simulation files unless they are deliberately promoted into the repository.

---

# Repository Outputs

Persistent outputs are organized under:

```text
results/data/
results/figures/
results/logs/
```

Important permanent simulations include:

```text
simulations/001_kottler_weak_field.py

simulations/001b_kottler_tidal_eigenvalues.py

simulations/002_required_stress_energy.py

simulations/003a_finite_vacuum_energy_core.py

simulations/003b_israel_shell_mass_search.py

simulations/004a_einstein_maxwell_repulsion.py

simulations/005a_relativistic_tension_wall.py

simulations/005b_finite_supported_antigravity.py

simulations/006a_static_dec_lower_bound.py

simulations/006b_geometry_aware_dec_optimizer.py

simulations/006b_full_rz_decision.py

simulations/006c_independent_finite_disk_field.py

simulations/006d_finite_thickness_conserved_source.py

simulations/008a_wall_current_loop_gate.py

simulations/008b_distributed_field_representability_gate.py
```

See the latest codebundle and `NOTES.md` for the exact implementation state.

---

# Research Philosophy

* Start with established physics.
* Reproduce known results before exploring speculative extensions.
* Separate coordinate effects from measurable physical effects.
* Prefer invariant or operational quantities.
* State assumptions explicitly.
* State approximation level explicitly.
* Check dimensional consistency.
* Check limiting cases.
* Attempt falsification before increasing complexity.
* Preserve negative results.
* Prefer the cheapest decisive experiment or theorem.
* Require conservation where appropriate.
* Distinguish local repulsion from global repulsion.
* Distinguish a gravitational effect from a fifth force.
* Distinguish a fifth force from reactionless propulsion.
* Distinguish a low-energy EFT construction from a microscopic physical realization.
* Distinguish mathematical possibility from experimental accessibility.
* Distinguish experimental accessibility from practical engineering.
* Treat AI-generated mathematics and code as unverified until checked.
* Require independent derivations or implementations for central quantitative claims.
* Never classify an internally generated result as a discovery without independent verification and literature comparison.

---

# Scientific Classification

The project uses conservative classifications such as:

```text
KNOWN_RESULT

REPRODUCED

ANALYTIC_RESULT

NUMERICAL_OBSERVATION

NUMERICAL_OPTIMIZATION_RESULT

INDEPENDENT_NUMERICAL_VERIFICATION

CONSTRUCTIVE_LINEARIZED_GR_STRESS_ENERGY_RESULT

ANALYTIC_SIGN_GATE

ANALYTIC_UV_PREFLIGHT

LOW_ENERGY_EFT_CONSTRUCTION

PARAMETRIC_SURVIVOR

MICROSCOPIC_THEORETICAL_CANDIDATE

CONJECTURE

REJECTED
```

A result is not a discovery merely because the project has not yet found a precedent.

---

# Current Active Question

The current active frontier is:

> **Can a technically natural local relativistic microscopic theory generate the protected material-specific two-body scalar interaction required by the dinuclear NR EFT without generating experimentally forbidden one-body scalar charge or destabilizing the ultralight mediator?**

The next decisive calculation should therefore attack:

```text
RELATIVISTIC_OPERATOR_BASIS

GAUGE_INVARIANCE

EXACT_OR_TECHNICALLY_NATURAL_SYMMETRY

TREE_LEVEL_ONE_BODY_OPERATORS

LOOP_OPERATOR_MIXING

RENORMALIZATION_GROUP_RUNNING

ULTRALIGHT_SCALAR_MASS_CORRECTION

INDEPENDENT_NR_MATCHING
```

The project should **not** begin another material optimization branch until this question is resolved.

If the required protection cannot exist without fine tuning, the present material-scalar branch should be closed.

---

# AI-Assisted Research

Antigravity Research is a human-directed research project using **ChatGPT by OpenAI** as an AI research and development assistant.

AI assistance includes:

* mathematical derivations;
* Python development;
* simulation design;
* debugging;
* numerical analysis;
* literature-search assistance;
* documentation;
* hypothesis generation;
* falsification efforts.

AI-generated material is not assumed correct.

Important results remain subject to analytical, numerical, dimensional, literature, and independent verification.

Use of ChatGPT does not imply endorsement or sponsorship by OpenAI.

See [`AI_ASSISTANCE.md`](AI_ASSISTANCE.md) for the complete disclosure.

---

# Licensing

Antigravity Research uses separate licenses for software and research materials.

* **Software:** MIT OR Apache-2.0, at the user's option.
* **Original research materials, generated data, and original figures:** CC0 1.0 Universal.

See [`LICENSE.md`](LICENSE.md) and the `LICENSES/` directory for the complete licensing policy.

Third-party materials retain their original copyright and licensing terms.

---

# Bottom Line

> # **We have a mathematical construction for antigravity-like gravitational repulsion.**

That statement refers specifically to the 006D static linearized-GR construction.

The source is:

```text
FINITE=YES
POSITIVE_ENERGY=YES
LOCALLY_CONSERVED_AT_LINEARIZED_ORDER=YES
NEC_WEC_DEC=PASS
LOCAL_GRAVITATIONAL_FIELD=OUTWARD
FAR_FIELD_ACTIVE_MASS=POSITIVE
```

The explicit finite coefficient is

```math
C_{\mathrm{finite}}
=
23.591586299249
```

The result proves a mathematical point:

> **Positive-energy, energy-condition-compatible stress-energy can produce a finite locally repulsive gravitational near field in the stated linearized-GR construction.**

It does not solve practical antigravity.

The classical source remains catastrophically expensive.

The project therefore moved on to investigate whether another interaction could provide antigravity-like acceleration at radically lower effective cost.

The strongest current speculative survivor is now a **protected bound dinuclear scalar-response EFT**.

It has passed a substantial set of low-energy consistency checks:

```text
BOUND_STATE_SELECTOR=
PASS_AT_LOW_ENERGY

THERMAL_LEAKAGE_WINDOW=
PASS_IN_SELECTED_MODEL

FINITE_SIZE_STABILITY=
PASS_IN_SELECTED_MODEL

FEYNMAN_HELLMANN=
PASS

INDEPENDENT_TWO_BODY_CONTACT_MATCH=
PASS

ATOMIC_EFT_PERTURBATIVITY=
PASS
```

But the critical microscopic problem remains:

```text
PROTECTED_RELATIVISTIC_UV_COMPLETION=
NOT_ESTABLISHED

GENERIC_RELATIVISTIC_UV_MATCH=
REJECTED

KNOWN_REAL_MATERIAL=
NO

EXACT_CURRENT_5KM_BOUND=
NOT_CLOSED

PRACTICAL_ANTIGRAVITY_DEVICE=
NO

NEW_PHYSICS_DISCOVERY=
NO
```

The project's current scientific position can therefore be summarized as:

```text
MATHEMATICAL_GRAVITATIONAL_REPULSION=
ESTABLISHED_IN_006D_SCOPE

LOW_ENERGY_MATERIAL_SPECIFIC_FIFTH_FORCE_ARCHITECTURE=
PARAMETRIC_SURVIVOR

PHYSICAL_REALIZATION=
NOT_ESTABLISHED

PRACTICAL_ANTIGRAVITY=
NOT_YET
```

The next major advance must come from **microscopic physics**, not another phenomenological tuning step.
