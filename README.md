# Antigravity Research

> # **We have a mathematical construction for antigravity-like gravitational repulsion.**

The exact scientific claim is:

> **Within static linearized general relativity, there exists an explicit finite-radius, finite-thickness, nonsingular, positive-energy, locally conserved type-I stress-energy configuration satisfying NEC, WEC, and DEC whose calculated near field points outward while its far-field active mass remains positive.**

Everything required to reconstruct the **006D headline calculation** is given below: the linearized-GR field equation, sign convention, exact dimensionless source, smoothing widths, finite-thickness profile, energy density, conservation proof, energy-condition proof, positive far-field proof, numerical integrals, quadrature tolerances, convergence data, expected numerical invariants, and a standalone Python reproducer that imports no project modules.

The result is a **constructive linearized-GR stress-energy result**. It is not an exact nonlinear solution, a stability proof, a material realization, or a practical antigravity device.

```text
HEADLINE_CLAIM=SUPPORTED_WITHIN_STATIC_LINEARIZED_GR
ANALYTIC_CONSERVATION_PROOF=YES
ANALYTIC_ENERGY_CONDITION_PROOF=YES
ANALYTIC_POSITIVE_FAR_FIELD_ACTIVE_MASS_PROOF=YES
FINITE_SOURCE_SPECIFIED_EXPLICITLY=YES
LOCAL_OUTWARD_FIELD=NUMERICALLY_REPRODUCIBLE
TWO_NUMERICAL_Z_INTEGRATION_METHODS=AGREE
EXACT_NONLINEAR_GR=NOT_ESTABLISHED
DYNAMIC_STABILITY=NOT_ESTABLISHED
KNOWN_MATERIAL_REALIZATION=NO
PRACTICAL_ANTIGRAVITY_DEVICE=NO
```

---

# Verification Dossier for the Headline Claim

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

and the weak-field definition

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
\zeta_{\mathrm{target}}=1
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

The exact smoothing widths for the quoted finite result are

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

and the outer support radius is

```math
x_{\max}
=
\beta+\delta_{\mathrm{outer}}
=
4.707687405300
```

These constants are sufficient to reconstruct the finite source used for the quoted value $C_{\mathrm{finite}}=23.591586299249$.

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

and no shear component:

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

The complete finite radial source is:

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

At $x=0$ the regular limiting values are

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

so there is no hidden singular line support.

---

## 4. Exact finite-thickness profile

Let $U_0>0$ be an arbitrary positive surface-energy scale.

Define the normalized vertical bump

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

It also vanishes smoothly at both slab boundaries.

The physical volume stresses are

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
p_z^{\mathrm{phys}}(r,z)=0
```

The physical energy density is

```math
\epsilon^{\mathrm{phys}}(r,z)
=
\frac{U_0}{h}
\epsilon(x)
\varphi_\delta(\zeta)
```

where the dimensionless energy profile is defined below.

Because $U_0>0$, changing $U_0$ rescales the entire source and field without changing any sign statement or the coefficient $C$.

---

## 5. Analytic local-conservation proof

By definition,

```math
p_r(x)
=
\frac{q(x)}{x}
```

for $x>0$, and

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

Thus the flat-background cylindrical radial conservation equation is satisfied identically wherever the source is differentiable.

The smoothing functions make $q$ and $q'$ continuous at the interfaces, so there is no omitted distributional radial force.

Since

```math
p_z=0
```

and

```math
T_{\hat r\hat z}=0
```

the static $z$-directed conservation equation also vanishes.

Multiplication by the common nonnegative vertical profile does not spoil the radial identity, and there are no $z$-indexed stresses whose $z$ derivative would create a new force term.

Therefore

```math
\boxed{
\partial_\mu T^{\mu\nu}=0
}
```

for the static source on the flat background used by the linearized calculation.

This is **linearized-order conservation**, not yet the exact nonlinear statement $\nabla_\mu T^{\mu\nu}=0$ in the self-consistent curved metric.

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

Immediately,

```math
\epsilon\ge0
```

and

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

Therefore:

```text
DEC=SATISFIED
WEC=SATISFIED
NEC=SATISFIED
```

The construction saturates some inequalities at some points; it does not require negative energy density.

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

so

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

Therefore the integrated active gravitational source is

```math
m_{\mathrm{active}}
=
m_\delta+\tau_\delta
=
m_\delta
>
0
```

So the far-field active mass is positive **analytically**, not merely because a program prints a Boolean flag.

---

## 8. Exact finite-source local-field integral

Define the dimensionless active radial profile

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

The physical acceleration at the target is then

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

The total energy-equivalent mass is

```math
M
=
\frac{
\pi U_0 h^2
}{
c^2
}
m_\delta
```

Eliminating $U_0$ between the acceleration and mass expressions gives

```math
M
=
C
\frac{
a_z h^2
}{
G
}
```

with

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

Thus the headline claim reduces to one transparent numerical sign check:

```math
F_\delta>0
```

for the explicit source above.

---

## 9. Numerical method used for the quoted 006D result

For the finest quoted source:

```text
delta                    = 0.00625
inner smoothing width    = delta / 4
outer collar width       = delta
target z/h               = 1
radial support end        = 4.707687405300
```

Radial integration is performed piecewise across the four interfaces

```text
0
alpha - delta/4
alpha + delta/4
beta
beta + delta
```

using adaptive SciPy `quad` with

```text
epsabs = 2e-11
epsrel = 2e-11
limit  = 300 or greater
```

The production 006D calculation averages the vertical kernel using **64-point Gauss-Legendre quadrature**.

The standalone verifier below also evaluates the same vertical integral a second way using nested adaptive `quad`, so the local field sign is not dependent on the Gauss-Legendre implementation.

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

For the explicit finest source, direct evaluation gives:

```text
MASS_FACTOR
= 1.110076490539830e+01

INTEGRATED_STRESS_TRACE_FACTOR
= 2.922107000813412e-13
≈ 0

ACTIVE_MASS_FACTOR
= 1.110076490539859e+01
> 0

FIELD_FACTOR_GAUSS_LEGENDRE_64
= 2.352695737495157e-01
> 0

FIELD_FACTOR_NESTED_ADAPTIVE_QUAD
= 2.352695737495351e-01
> 0

ABSOLUTE_DIFFERENCE_BETWEEN_FIELD_METHODS
≈ 1.94e-14

C_GAUSS_LEGENDRE_64
= 23.5915862992487

C_NESTED_ADAPTIVE_QUAD
= 23.5915862992467

MAX_CONTROL_VOLUME_CONSERVATION_RESIDUAL
= 3.103073353827312e-14

MAX_DEC_VIOLATION
= 0

MIN_NEC_MARGIN
= 0
```

The field factor is approximately $0.235$, while the two independent vertical-integration routes differ by only about $2\times10^{-14}$.

The sign is therefore not numerically marginal.

The conclusion for this explicit source is:

```math
\boxed{
F_\delta
=
0.2352695737495\ldots
>
0
}
```

and consequently

```math
\boxed{
a_z>0
}
```

under the stated sign convention.

---

## 11. Finite-thickness convergence

The regularization sequence is:

| $\delta=t/h$ | Mass factor $m_\delta$ | Field factor $F_\delta$ | $C=m_\delta/(2F_\delta)$ |
|---:|---:|---:|---:|
| 0.40000 | 11.369718516276 | 0.149453529535 | 38.037638025730 |
| 0.20000 | 11.233723934208 | 0.190019680852 | 29.559369544823 |
| 0.10000 | 11.165255241660 | 0.212604998246 | 26.258214373557 |
| 0.05000 | 11.130897375158 | 0.224509078286 | 24.789414887263 |
| 0.02500 | 11.113686825672 | 0.230618147495 | 24.095429926871 |
| 0.01250 | 11.105073553053 | 0.233712433325 | 23.757986246352 |
| 0.00625 | 11.100764905398 | 0.235269573750 | 23.591586299249 |

The independently established thin conserved reference is

```math
C_{\mathrm{thin}}
=
23.426710175391
```

The finite sequence approaches that reference monotonically from above.

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

or approximately $0.704\%$.

---

## 12. Physical scale restoration

For the finest finite source,

```math
F_\delta
\approx
0.2352695737495
```

so the positive surface-energy scale required for a desired outward acceleration is

```math
U_0
=
\frac{
a_z c^2
}{
2\pi G F_\delta
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
a h^2
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

This enormous stress-energy requirement is why the result is a mathematical construction rather than a practical device.

The gravitational field itself is still safely weak-field at this scale. A characteristic compactness based on the total energy-equivalent mass and $h=1\ {\rm m}$ is only of order

```math
\frac{
GM_{\mathrm{equiv}}
}{
hc^2
}
\sim
2.6\times10^{-15}
```

so the failure of practicality is not caused by strong spacetime curvature; it is caused by the extraordinary material/field stress-energy required.

---

## 13. Standalone reproduction from the README alone

A scientist does **not** need to trust the repository implementation to reproduce the numerical claim.

Create a fresh environment with Python, NumPy, and SciPy, copy the following block into `verify_006d_from_readme.py`, and run it.

```bash
python3 -m venv .verify-006d
source .verify-006d/bin/activate
python -m pip install --upgrade pip
python -m pip install numpy scipy
python verify_006d_from_readme.py
```

The complete standalone verifier is below.

```python
#!/usr/bin/env python3
"""Standalone README verifier for the 006D finite-source construction.

This script imports no ANTIGRAVITY_RESEARCH project modules. It reconstructs
the exact normalized 006D source from the equations and constants documented
in README.md and evaluates:

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
    return u * u * (3.0 - 2.0 * u)


def smoothstep_prime(u: float) -> float:
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
        u = (x - x_minus) / (x_plus - x_minus)
        s = smoothstep(u)
        sp = smoothstep_prime(u) / (x_plus - x_minus)

        q = (1.0 - s) * q_core + s * q_annulus
        qp = (
            (1.0 - s) * qp_core
            + s * qp_annulus
            + sp * (q_annulus - q_core)
        )
        return q, qp

    if x < BETA:
        return q_annulus, qp_annulus

    if x <= BETA + OUTER_WIDTH:
        u = (x - BETA) / OUTER_WIDTH
        s = smoothstep(u)
        sp = smoothstep_prime(u) / OUTER_WIDTH

        q = (1.0 - s) * q_annulus
        qp = (1.0 - s) * qp_annulus - sp * q_annulus
        return q, qp

    return 0.0, 0.0


def surface_profiles(x: float) -> tuple[float, float, float]:
    """Return dimensionless epsilon, p_r, p_phi."""

    q, qp = q_and_prime(x)

    p_r = -1.0 if x == 0.0 else q / x
    p_phi = qp
    epsilon = max(abs(p_r), abs(p_phi))

    return epsilon, p_r, p_phi


def radial_breakpoints() -> list[float]:
    return [
        0.0,
        ALPHA - INNER_WIDTH,
        ALPHA + INNER_WIDTH,
        BETA,
        BETA + OUTER_WIDTH,
    ]


def radial_integral(function, eps: float = RADIAL_EPS) -> float:
    total = 0.0

    points = radial_breakpoints()

    for lower, upper in zip(points[:-1], points[1:]):
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


def vertical_profile(zeta: float) -> float:
    """Normalized compact profile in zeta=z/h."""

    if zeta < -DELTA or zeta > 0.0:
        return 0.0

    y = (zeta + DELTA) / DELTA

    return (
        30.0
        / DELTA
        * y * y
        * (1.0 - y) * (1.0 - y)
    )


def field_factor_gauss_legendre(order: int = GL_ORDER) -> float:
    """Evaluate the finite-thickness axial field using GL quadrature in z."""

    z_nodes, z_weights = leggauss(order)

    y_nodes = 0.5 * (z_nodes + 1.0)
    y_weights = 0.5 * z_weights

    bump_weights = (
        y_weights
        * 30.0
        * y_nodes**2
        * (1.0 - y_nodes)**2
    )

    source_zeta = -DELTA + DELTA * y_nodes
    separation = 1.0 - source_zeta

    def integrand(x: float) -> float:
        epsilon, p_r, p_phi = surface_profiles(x)

        active = epsilon + p_r + p_phi

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

        return x * active * kernel_average

    # Positive return value means outward acceleration.
    return -radial_integral(integrand)


def field_factor_nested_quad() -> float:
    """Independent z integration using adaptive quadrature instead of GL."""

    def kernel_average(x: float) -> float:
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

    def integrand(x: float) -> float:
        epsilon, p_r, p_phi = surface_profiles(x)
        active = epsilon + p_r + p_phi
        return x * active * kernel_average(x)

    return -radial_integral(integrand, eps=5.0e-12)


def conservation_residual() -> float:
    """Check q(b)-q(a)-integral p_phi dx over 150 control volumes."""

    outer_radius = BETA + OUTER_WIDTH
    edges = np.linspace(0.0, outer_radius, 151)

    maximum = 0.0

    for left, right in zip(edges[:-1], edges[1:]):
        q_left = q_and_prime(float(left))[0]
        q_right = q_and_prime(float(right))[0]

        interior_points = [
            point
            for point in radial_breakpoints()[1:-1]
            if left < point < right
        ]

        integral, _ = quad(
            lambda x: surface_profiles(x)[2],
            float(left),
            float(right),
            epsabs=CONTROL_EPS,
            epsrel=CONTROL_EPS,
            limit=150,
            points=interior_points,
        )

        residual = q_right - q_left - integral
        maximum = max(maximum, abs(float(residual)))

    return maximum


def energy_condition_checks() -> tuple[float, float]:
    """Return max DEC violation and minimum NEC margin."""

    outer_radius = BETA + OUTER_WIDTH
    sample_x = np.linspace(0.0, outer_radius, 4001)

    max_dec_violation = 0.0
    min_nec_margin = math.inf

    for x in sample_x:
        epsilon, p_r, p_phi = surface_profiles(float(x))

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

    return max_dec_violation, min_nec_margin


def main() -> None:
    mass_factor = (
        2.0
        * radial_integral(
            lambda x: x * surface_profiles(x)[0]
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

    active_mass_factor = mass_factor + trace_factor

    field_gl64 = field_factor_gauss_legendre(64)
    field_nested = field_factor_nested_quad()

    coefficient_gl64 = mass_factor / (2.0 * field_gl64)
    coefficient_nested = mass_factor / (2.0 * field_nested)

    max_control_residual = conservation_residual()
    max_dec_violation, min_nec_margin = energy_condition_checks()

    print("=== README 006D STANDALONE VERIFICATION ===")
    print(f"ALPHA={ALPHA:.12f}")
    print(f"BETA={BETA:.12f}")
    print(f"DELTA={DELTA:.8f}")
    print(f"INNER_WIDTH={INNER_WIDTH:.8f}")
    print(f"OUTER_WIDTH={OUTER_WIDTH:.8f}")
    print(f"OUTER_RADIUS={BETA + OUTER_WIDTH:.12f}")
    print()
    print(f"MASS_FACTOR={mass_factor:.15e}")
    print(f"TRACE_FACTOR={trace_factor:.15e}")
    print(f"ACTIVE_MASS_FACTOR={active_mass_factor:.15e}")
    print(f"FIELD_FACTOR_GL64={field_gl64:.15e}")
    print(f"FIELD_FACTOR_NESTED={field_nested:.15e}")
    print(f"FIELD_METHOD_ABS_DIFFERENCE={abs(field_gl64-field_nested):.15e}")
    print(f"C_GL64={coefficient_gl64:.15e}")
    print(f"C_NESTED={coefficient_nested:.15e}")
    print()
    print(f"MAX_CONTROL_VOLUME_CONSERVATION_RESIDUAL={max_control_residual:.15e}")
    print(f"MAX_DEC_VIOLATION={max_dec_violation:.15e}")
    print(f"MIN_NEC_MARGIN={min_nec_margin:.15e}")
    print()
    print(
        "LOCAL_CONSERVATION="
        + ("PASS" if max_control_residual < 1.0e-8 else "FAIL")
    )
    print(
        "DEC="
        + ("PASS" if max_dec_violation <= 1.0e-12 else "FAIL")
    )
    print(
        "NEC_WEC="
        + ("PASS" if min_nec_margin >= -1.0e-12 else "FAIL")
    )
    print(
        "POSITIVE_FAR_FIELD_ACTIVE_MASS="
        + ("YES" if active_mass_factor > 0.0 else "NO")
    )
    print(
        "OUTWARD_LOCAL_FIELD_GL64="
        + ("YES" if field_gl64 > 0.0 else "NO")
    )
    print(
        "OUTWARD_LOCAL_FIELD_NESTED="
        + ("YES" if field_nested > 0.0 else "NO")
    )


if __name__ == "__main__":
    main()
```

Expected output from the standalone verifier:

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

The two field evaluations use different vertical integration methods:

```text
METHOD_1=64_POINT_GAUSS_LEGENDRE
METHOD_2=NESTED_ADAPTIVE_SCIPY_QUAD
```

Both independently return a positive field factor.

---

## 14. Repository cross-check

The repository reference implementation is:

```text
simulations/006d_finite_thickness_conserved_source.py
```

The codebundle snapshot records its SHA-256 as:

```text
e303b3bb454d19cc16516e189e6db559d1812dad733f9e02bf1ecafce2594d76
```

Run the project implementation from the repository root with:

```bash
ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"

PYTHONPATH="$ROOT/src" \
"$PY" simulations/006d_finite_thickness_conserved_source.py
```

Run the focused regression checks with:

```bash
ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"

PYTHONPATH="$ROOT/src" \
"$PY" -m pytest -q \
tests/known_solutions/test_006c_006d_regressions.py
```

Run the full known-solution suite with:

```bash
ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"

PYTHONPATH="$ROOT/src" \
"$PY" -m pytest -q tests/known_solutions
```

The verified session baseline is:

```text
94 passed
```

Important validation distinction:

- Simulation 006C is an independent Green-function reconstruction of the earlier 005B finite disk.
- Simulation 006D has analytic conservation and energy-condition structure, finite-volume checks, convergence to the independently established 006B thin reference, regression coverage, and the standalone README reproducer above.
- A separately authored, publication-grade independent implementation of the **entire 006D finite-thickness field calculation** would still be an additional desirable validation step.

That limitation does not change the reproducibility of the present claim; it prevents us from overstating the validation level.

---

## 15. What the calculation establishes

For the explicitly specified finite source:

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

The compact mathematical statement is:

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

for the explicit 006D source in static linearized GR.

Therefore the headline is supported:

> # **We have a mathematical construction for antigravity-like gravitational repulsion.**

---

## 16. What the calculation does not establish

The following claims are deliberately **not** made:

```text
EXACT_NONLINEAR_EINSTEIN_SOLUTION=NOT_ESTABLISHED
FULL_CURVED_SPACETIME_CONSERVATION=NOT_ESTABLISHED
DYNAMIC_STABILITY=NOT_ESTABLISHED
CONSTITUTIVE_MATERIAL_MODEL=NOT_ESTABLISHED
KNOWN_FIELD_THEORY_REALIZATION=NOT_ESTABLISHED
EXPERIMENTAL_ACCESSIBILITY=NOT_ESTABLISHED
ENERGETIC_PRACTICALITY=NO
GLOBAL_POSITIVE_MASS_REPULSION=NOT_ESTABLISHED
REACTIONLESS_PROPULSION=NOT_ESTABLISHED
PRACTICAL_ANTIGRAVITY_DEVICE=NO
NEW_PHYSICS_DISCOVERY=NO
```

The strongest justified classification is:

```text
CLAIM_CLASSIFICATION=
CONSTRUCTIVE_LINEARIZED_GR_STRESS_ENERGY_RESULT
```

---

---

# Why the Result Matters

The project began with the question of whether gravitational repulsion itself was forbidden.

That question has been answered.

**The sign of gravity is not the fundamental obstacle.**

General relativity couples to the full stress-energy tensor, not merely rest-mass density. Relativistic pressure and tension contribute gravitationally. A positive-energy source can therefore contain a locally repulsive active-stress region without requiring negative total mass.

The present obstacle is instead the physical realization and cost of the required stress-energy.

The most important classical design principle found so far is:

> **Maximize physically realizable relativistic tension per unit positive energy while preserving local conservation and stability.**

---

# Important Terminology

## Local gravitational repulsion

A neutral test body in a specified region experiences gravitational acceleration away from the source region.

```text
PROJECT_STATUS=YES
```

This is known in GR and is reproduced by several calculations in this repository.

## Global gravitational repulsion

The asymptotic field of an isolated positive-total-mass source points outward.

```text
PROJECT_STATUS=NO
```

The finite 005B/006D architectures retain attractive positive-mass far fields.

## Ground-referenced antigravity-like levitation

A body is pushed upward through interaction with an external source, external field, or reaction partner.

```text
FUNDAMENTALLY_FORBIDDEN=NO
PRACTICAL_REALIZATION=NOT_ESTABLISHED
```

This is distinct from a self-contained craft.

## Self-contained antigravity

An isolated apparatus changes its center-of-energy motion or its passive gravitational response without an external reaction partner.

```text
PROJECT_STATUS=NOT_ESTABLISHED
```

The 009P and 010D analyses reinforce that reciprocal internal forces cannot self-accelerate an isolated center of energy.

## Practical antigravity

A finite, controllable, stable apparatus produces useful gravitational repulsion at physically realizable energy and material scales.

```text
PROJECT_STATUS=NO
```

---

# Research Program and Major Results

## 001 — Established GR baselines

The repository reproduced:

- Schwarzschild-de Sitter / Kottler attraction-repulsion transition;
- positive-$\Lambda$ geodesic defocusing;
- invariant tidal behavior through geodesic deviation.

For Kottler spacetime,

```math
a(r)
=
-\frac{GM}{r^2}
+
\frac{\Lambda c^2r}{3}
```

The effect is real but the observed cosmological constant is useless at laboratory scales.

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

Negative energy is therefore not required for the sign of local gravitational repulsion.

## 003 — Localizing vacuum-like stress

A finite pure $w=-1$ region cannot simply taper to vacuum while retaining the same local equation of state. Boundary stresses are required.

A de Sitter-core / Schwarzschild-exterior thin-shell search showed that forcing a negative-mass exterior in the tested construction requires exotic shell properties incompatible with ordinary WEC/DEC assumptions.

## 004 — Einstein-Maxwell / Reissner-Nordström

The exact metric contains

```math
f(r)
=
1
-
\frac{2GM}{c^2r}
+
\frac{GQ^2}{4\pi\epsilon_0c^4r^2}
```

and the neutral-particle gravitational tendency changes sign at

```math
r_{\mathrm{rep}}
=
\frac{Q^2}{4\pi\epsilon_0Mc^2}
```

This provides an exact established-theory example of positive-energy local gravitational repulsion, but useful laboratory acceleration requires extreme electric fields.

## 005 — Relativistic tension

For a planar membrane with tangential tension

```math
\tau=qU
```

the gravitational field becomes repulsive for

```math
q>\frac12
```

while DEC permits

```math
q\le1
```

so the interval

```math
\frac12<q\le1
```

contains positive-energy, energy-condition-compatible repulsive stress.

The 005B finite membrane-plus-support model yielded

```math
M_{\mathrm{equiv}}
\approx
79.753148116012
\frac{a h^2}{G}
```

and was later independently verified by Simulation 006C to approximately machine precision.

## 006 — Finite conserved positive-energy construction

Simulation 006B reduced the locally conserved thin-source coefficient to

```math
C_{\mathrm{thin}}
=
23.426710175391
```

Simulation 006C independently reconstructed the earlier 005B field and optimum.

Simulation 006D then regularized the optimized architecture to finite thickness and finite radial support while preserving:

```text
FINITE_SPATIAL_SUPPORT=YES
FINITE_THICKNESS=YES
POINTWISE_POSITIVE_ENERGY=YES
POINTWISE_NEC_WEC_DEC=YES
LOCAL_CONSERVATION_LINEARIZED_ORDER=YES
OUTWARD_GRAVITATIONAL_FIELD=YES
POSITIVE_FAR_FIELD_ACTIVE_MASS=YES
```

The best tested finite coefficient is

```math
C_{\mathrm{finite}}
=
23.591586299249
```

This is the mathematical construction highlighted at the top of this README.

## 007 — Established quantum-field routes

The project then tested whether established quantum stress-energy could change the practical scaling.

The main conclusions were:

- a complete Casimir apparatus cannot be evaluated by counting the negative vacuum region alone;
- support and plate stresses must be included;
- the static Casimir route did not provide a practical macroscopic escape;
- free-electromagnetic quantum-energy-inequality bounds make macroscopic negative-energy acceleration extraordinarily small.

```text
ESTABLISHED_QFT_MACROSCOPIC_PRACTICAL_ESCAPE=NOT_FOUND
```

## 008 — Field realizability and stability

The project asked whether known classical fields could realize the 006D stress pattern.

Key outcomes include:

- wall/current-loop support did not materially improve the classical scaling;
- a canonical scalar can locally reproduce relevant stress tensors;
- purely static scalar realizations face Derrick-type instability;
- one charged complex scalar cannot exactly reproduce the full target architecture;
- finite ungauged winding constructions fail at the boundary;
- local gauge-assisted boundary takeover remains mathematically possible in a restricted window but does not solve the basic energy scaling.

```text
KNOWN_PRACTICAL_FIELD_REALIZATION_OF_006D=NO
```

## 009 — Short-range fifth-force program

The project investigated whether a new non-gravitational interaction could provide a much larger force on neutral matter.

### Ordinary unscreened vector benchmark

The optimistic ordinary-matter vector half-space ceiling was approximately

```math
\frac{a_{\max}}{g}
\approx
2.21\times10^{-2}
```

under the tested constraints.

### Opposite-sign scalar benchmark

The optimized neutron-star-normalized opposite-sign scalar preflight gave

```math
\frac{a_{\max}}{g}
\approx
7.33\times10^{-4}
```

even for an optimistic zero-gap infinite osmium half-space acting on hydrogen.

### Material-blind vector direction

A gold-phobic phenomenological vector direction could formally reach order-$1g$ in a low-energy force recast, but the simple UV completions examined failed or became severely stressed by:

- electroweak $SU(2)_L$ consistency;
- unavoidable axial couplings;
- longitudinal-mode / stellar constraints;
- vectorlike-partner mass and mixing requirements;
- low effective UV cutoff scales.

The effective-$Z'$ preflight found, at the $1g$ benchmark,

```text
UNAVOIDABLE_AXIAL_COUPLING_AT_1G=1.064556829114e-11
STRONG_NDA_LAMBDA_U_MAX_GEV=582.021760
STRONG_NDA_LAMBDA_D_MAX_GEV=601.574737
```

and the simple effective-$Z'$ rescue is therefore severely stressed, though not claimed to be a theorem excluding every exotic UV completion.

### Momentum-conservation result

A reciprocal fifth-force stack internal to one isolated craft obeys total momentum conservation.

```text
SELF_CONTAINED_MULTILAYER_FIFTH_FORCE_LIFT=REJECTED
GROUND_REFERENCED_EXTERNAL_SOURCE_FORCE=NOT_REJECTED_BY_THIS_ARGUMENT
```

Thus a new short-range force and self-contained gravitational antigravity are not the same achievement.

## 010 — Modified-gravity and conservation gates

### 010A — Healthy universal scalar-tensor sign gate

A healthy universally coupled canonical scalar adds attraction or screens back toward GR.

Metric $f(R)$ gives the familiar short-range enhancement

```math
\frac{F}{F_{\mathrm{GR}}}
\rightarrow
\frac43
```

rather than repulsion.

Opposite scalar charges return to the already-tested fifth-force class, while wrong-sign kinetic terms introduce ghosts.

### 010B — Vector-tensor and spin-2 sign gate

Healthy positive-residue extra spin-2 exchange adds attraction.

A healthy spin-1 field can repel like charges, but doing so requires an explicit matter current or charge and therefore returns to fifth-force physics.

The tested Einstein-æther Newtonian sign flip requires crossing a singular/pathological parameter region rather than providing a viable laboratory antigravity regime.

### 010C — Nonperturbative and nonminimal scalar gate

A constant-density scalarization estimate gives

```math
|\beta|
\frac{GM}{Rc^2}
=
\frac{\pi^2}{12}
```

For a neutron star with compactness $0.2$,

```math
|\beta|_{\mathrm{crit}}
\approx
4.11
```

consistent with the known strong-field scale.

For a one-meter osmium sphere,

```math
|\beta|_{\mathrm{crit}}
\approx
1.17\times10^{22}
```

so laboratory-density matter is nowhere near the compactness needed for the standard spontaneous-scalarization mechanism.

The same gate showed that healthy general conformal scalar-tensor theories retain positive effective gravitational coupling under the tested stability conditions.

### 010D — Equivalence-principle and center-of-energy gate

Define

```math
\chi
=
\frac{m_{\mathrm{passive}}}
{m_{\mathrm{inertial}}}
```

Then

```math
a
=
\chi g
```

Ordinary free fall corresponds to

```math
\chi=1
```

weight cancellation requires

```math
\chi=0
```

and upward gravitational acceleration of magnitude $g$ requires

```math
\chi=-1
```

Thus true gravitational inversion requires an order-unity change in passive gravitational response.

Within ordinary equivalence-principle bookkeeping, internal energy changes inertial and gravitational mass together and does not provide this switch.

For an isolated system, internal conservative fields also cannot accelerate the total center of energy.

```text
WEP_PRESERVING_INTERNAL_STATE_WEIGHT_MODULATION=REJECTED
ISOLATED_INTERNAL_BACKGROUND_SELF_ACCELERATION=REJECTED
RADIATIVE_MOMENTUM_EXPORT=ORDINARY_REACTION_PROPULSION
KNOWN_PRACTICAL_GRAVITATIONAL_BACKGROUND_ACTUATOR=NO
```

---

# Current Scientific Position

The project has answered one foundational question positively:

> **Can physically respectable stress-energy produce local gravitational repulsion? Yes, within the explicitly tested linearized-GR construction.**

It has not yet answered the engineering question:

> **Can the required stress-energy or an equivalent gravitational-response mechanism be produced stably, controllably, and economically enough for practical antigravity? Not yet.**

The current theoretical landscape is:

```text
CLASSICAL_GR_LOCAL_REPULSION=YES
FINITE_POSITIVE_ENERGY_LINEARIZED_GR_CONSTRUCTION=YES
KNOWN_PRACTICAL_CLASSICAL_SOURCE=NO

STATIC_CASIMIR_PRACTICAL_ROUTE=DEPRIORITIZED
FREE_QFT_MACROSCOPIC_ROUTE=CLOSED_OR_STRONGLY_DEPRIORITIZED

ORDINARY_UNSCREENED_VECTOR_1G=NO
OPPOSITE_SIGN_SCALAR_1G=NO
GOLD_NULL_VECTOR_LOW_ENERGY_FORCE=POTENTIALLY_LARGE
GOLD_NULL_SIMPLE_HEALTHY_UV_COMPLETION=NOT_FOUND

UNIVERSAL_HEALTHY_SCALAR_TENSOR_SIGN_REVERSAL=NO
HEALTHY_POSITIVE_RESIDUE_SPIN2_SIGN_REVERSAL=NO
LAB_SPONTANEOUS_SCALARIZATION=NO

INTERNAL_CONSERVATIVE_SELF_THRUST=NO
SWITCHABLE_NEGATIVE_PASSIVE_GRAVITATIONAL_RESPONSE=NOT_ESTABLISHED

PRACTICAL_ANTIGRAVITY_DEVICE=NO
```

---

# Current Theoretical Frontier

The project should not restart solved coefficient optimization or reopen rejected branches without a genuinely new physical mechanism.

The current theory-side question is:

> **Is there any physically consistent mechanism that changes the practical scaling or the gravitational response itself without requiring ghosts, forbidden material charges, pathological UV structure, astronomical energy, or violation of total energy-momentum conservation?**

The remaining logical possibilities include:

- a new physically realizable source of large relativistic tension with radically improved scaling;
- an observationally viable nonstandard gravitational response not covered by the tested healthy scalar/vector/spin-2 classes;
- a controllable external gravitational or cosmological background interaction;
- genuinely new physics producing state-dependent passive gravitational response.

None of these has yet been established.

The next work should therefore be selected by **information gain**, not by preserving any particular speculative branch.

---

# Claims Ledger

## Supported

- Local gravitational repulsion exists in established GR.
- Positive energy does not forbid local gravitational repulsion.
- Negative total/ADM mass is not required for a locally repulsive near field.
- Relativistic negative pressure and tension can contribute repulsively.
- Reissner-Nordström provides an exact established-theory local repulsion example.
- The 005B finite supported disk result was independently numerically verified.
- The 006B thin locally conserved architecture has $C_{\mathrm{thin}}=23.426710175391$ within its stated class.
- The 006D finite-thickness source is finite, positive-energy, locally conserved at linearized order, NEC/WEC/DEC-compatible, locally repulsive, and positive in far-field active mass.
- The best tested 006D finite coefficient is $C_{\mathrm{finite}}=23.591586299249$.
- The classical sources studied retain the severe $a h^2/G$ scaling.
- Ordinary internal conservative forces cannot self-accelerate an isolated center of energy.

## Strongly disfavored or rejected in tested scope

- negative-mass thin-shell engineering under ordinary energy conditions;
- practical Reissner-Nordström electric-field scaling;
- complete static Casimir apparatus as a practical macroscopic route;
- free-field quantum negative energy as a macroscopic route;
- ordinary unscreened $B-L$-like vector force as an order-$1g$ actuator;
- terrestrial chameleon rescue mechanisms tested in 009I-009K;
- opposite-sign unscreened scalar as an order-$0.1g$ to $1g$ route under the 009O preflight;
- simple gold-null vector UV completions tested in 009M-009Q;
- universal canonical scalar-tensor sign reversal;
- metric $f(R)$ sign reversal;
- standard laboratory spontaneous scalarization;
- self-contained reciprocal fifth-force stacking;
- WEP-preserving internal-state weight switching.

## Not established

- an exact nonlinear-GR version of 006D;
- dynamical stability of 006D;
- a known material or field configuration that realizes 006D;
- a universal lower bound on the coefficient $C$;
- an experimentally allowed healthy order-$1g$ new force on ordinary matter;
- switchable negative passive gravitational mass;
- global positive-mass antigravity;
- reactionless propulsion;
- a practical antigravity device;
- a discovery of new physics.

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

The 009-010 frontier calculations were performed primarily as disposable analytical/literature gates and are documented in `NOTES.md`; they should not be described as permanent simulation files unless and until they are deliberately landed in the repository.

---

# Repository Outputs

Persistent numerical outputs are organized under:

```text
results/data/
results/figures/
results/logs/
```

Important permanent simulations through the classical and field-realizability stages include:

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

See the codebundle and `NOTES.md` for the exact current implementation state.

---

# Research Philosophy

- Start with established physics.
- Reproduce known results before exploring speculative extensions.
- Separate coordinate effects from invariant or operational observables.
- State assumptions and approximation levels explicitly.
- Check dimensions and limiting cases.
- Attempt falsification before increasing model complexity.
- Prefer the cheapest decisive analytical or numerical gate.
- Preserve negative results.
- Require local conservation where the physical model requires it.
- Distinguish mathematical sign, physical observable, theoretical consistency, realizability, experimental accessibility, and practical engineering.
- Never promote an internally generated calculation to a discovery without independent verification and literature comparison.

---

# Scientific Classification

Results should use conservative categories such as:

```text
KNOWN_RESULT
REPRODUCED
NUMERICAL_OBSERVATION
NUMERICAL_OPTIMIZATION_RESULT
INDEPENDENT_NUMERICAL_VERIFICATION
CONSTRUCTIVE_LINEARIZED_GR_STRESS_ENERGY_RESULT
ANALYTIC_SIGN_GATE
ANALYTIC_UV_PREFLIGHT
CONJECTURE
NOVEL_CANDIDATE
REJECTED
```

A result is not a discovery merely because the project has not yet located a precedent.

---

# AI-Assisted Research

Antigravity Research is a human-directed research project that uses **ChatGPT by OpenAI** as an AI research and development assistant.

AI assistance includes:

- mathematical derivations;
- Python development;
- simulation design;
- debugging;
- numerical analysis;
- literature-search assistance;
- documentation;
- hypothesis generation;
- falsification efforts.

AI-generated material is not assumed to be correct. Important results are subject to analytical, numerical, dimensional, literature, and independent verification.

Use of ChatGPT does not imply endorsement or sponsorship by OpenAI.

See [`AI_ASSISTANCE.md`](AI_ASSISTANCE.md) for the complete disclosure.

---

# Licensing

Antigravity Research uses separate licenses for software and research materials.

- **Software:** MIT OR Apache-2.0, at the user's option.
- **Original research materials, generated data, and original figures:** CC0 1.0 Universal.

See [`LICENSE.md`](LICENSE.md) and the `LICENSES/` directory for the complete licensing policy.

Third-party materials retain their original copyright and licensing terms.

---

# Bottom Line

> # **We have a mathematical construction for antigravity-like gravitational repulsion.**

The construction is finite, positive-energy, locally conserved at linearized order, compatible with NEC/WEC/DEC, and produces a verified outward local gravitational field.

The unresolved challenge is no longer whether gravitational repulsion can exist mathematically.

The unresolved challenge is whether Nature provides a **stable, physically realizable, energetically practical mechanism** capable of producing it at useful scales.

```text
THEORETICAL_LOCAL_REPULSION=YES
PRACTICAL_ANTIGRAVITY=NOT_YET
```
