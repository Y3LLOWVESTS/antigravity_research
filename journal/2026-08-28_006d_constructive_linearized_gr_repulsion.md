# Research Journal — 2026-08-28

## Constructive Finite Positive-Energy Local Gravitational Repulsion in Static Linearized General Relativity

## Objective

The primary scientific question investigated in this research slice was:

> **Can an explicit finite, nonsingular, positive-energy stress-energy distribution that is locally conserved and satisfies the standard pointwise classical energy conditions produce a locally outward gravitational field within ordinary general relativity?**

A secondary purpose of this journal entry is to permanently preserve the exact construction, mathematical proof obligations, numerical parameters, independent checks, reconstruction procedure, limitations, and later research context so that a scientist encountering the repository without access to prior conversations can independently determine what was and was not established.

The result recorded here is the basis of the project's current public headline:

> **We have a mathematical construction for antigravity-like gravitational repulsion.**

The exact scientific claim is narrower:

> **Within static linearized general relativity, there exists an explicit finite-radius, finite-thickness, nonsingular, positive-energy, locally conserved type-I stress-energy configuration satisfying NEC, WEC, and DEC whose calculated near gravitational field points outward while its far-field active mass remains positive.**

This journal entry does **not** claim:

* an exact nonlinear Einstein solution;
* dynamical stability;
* a known material realization;
* an experimentally observed effect;
* a practical antigravity device;
* reactionless propulsion;
* a discovery of new physics.

The claim classification is:

```text
CLAIM_CLASSIFICATION=
CONSTRUCTIVE_LINEARIZED_GR_STRESS_ENERGY_RESULT
```

---

## Starting State

Before this result was obtained, the project had already established several important facts.

### Local gravitational repulsion is not forbidden in general relativity

Known GR solutions already contain genuine repulsive gravitational behavior in appropriate regimes.

Examples reproduced by the project include:

* Schwarzschild-de Sitter / Kottler repulsion from positive cosmological constant;
* Reissner-Nordström local gravitational repulsion;
* gravitational defocusing from sufficiently negative relativistic pressure;
* domain-wall / tension-driven repulsion.

Therefore the research question was not whether GR can ever contain repulsion.

The harder question was whether a **finite positive-energy source satisfying strong classical matter conditions** could produce a locally outward field without relying on:

* negative total mass;
* an infinite planar source;
* a singular support ring;
* negative local energy density;
* an unconserved stress tensor.

### Relevant weak-field source term

For static weak gravitational fields, relativistic stresses contribute to the active gravitational source.

For a type-I stress tensor in a local orthonormal frame,

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

the static linearized gravitational potential satisfies

```math
\nabla^2\Phi
=
\frac{4\pi G}{c^2}
\left(
\epsilon+p_r+p_\phi+p_z
\right)
```

The active source is therefore

```math
S
=
\epsilon+p_r+p_\phi+p_z
```

Positive energy density alone does not force $S$ to be positive pointwise.

Sufficiently negative relativistic pressure or tension can make the local active source negative while $\epsilon$ remains positive.

### Earlier finite architecture

The earlier 005B finite supported tension-disk architecture had already produced local repulsion with coefficient

```math
C_{005B}
=
79.753148116012
```

in the scaling

```math
M_{\mathrm{equiv}}
=
C\frac{ah^2}{G}
```

Simulation 006C then independently reconstructed that result numerically.

The remaining concern was whether the support idealizations could be replaced by a finite, locally conserved stress-energy distribution without losing the effect.

That became Simulation 006D.

---

# Work Performed

## 1. Linearized-GR field equation reconstructed

Use metric signature $(-,+,+,+)$ and write

```math
g_{\mu\nu}
=
\eta_{\mu\nu}
+
h_{\mu\nu}
```

with

```math
|h_{\mu\nu}|\ll1
```

Define the trace-reversed perturbation

```math
\bar h_{\mu\nu}
=
h_{\mu\nu}
-
\frac12\eta_{\mu\nu}h
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
\frac12
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

\nabla^2\Phi
=
\frac{4\pi G}{c^2}
\left(
\epsilon+p_r+p_\phi+p_z
\right)

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

For an axisymmetric source and target on the symmetry axis at $z=h$,

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

The sign convention used throughout this construction is:

```text
a_z > 0  -> outward, away from the source slab

a_z < 0  -> inward, toward the source slab
```

---

# 2. Dimensionless normalization

Define

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

The target is located at

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

The finest tested source uses

```math

\delta
=
0.00625

```

The optimized radial constants are

```math

\alpha
=
1.437500564637

```

and

```math

\beta
=
4.701437405300

```

The inner transition width is

```math
\delta_{\mathrm{inner}}
=
\frac{\delta}{4}
=
0.0015625
```

The outer support-collar width is

```math
\delta_{\mathrm{outer}}
=
\delta
=
0.00625
```

Hence

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

and the maximum radial support is

```math
x_{\max}
=
\beta+\delta_{\mathrm{outer}}
=
4.707687405300
```

These constants, together with the equations below, completely specify the normalized source.

---

# 3. Radial stress construction

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

The cubic smoothstep is

```math
s(u)
=
u^2(3-2u)
```

with derivative

```math
s'(u)
=
6u(1-u)
```

The two basic branches are

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

## Region I — inner tension region

For

```math
0\le x<x_-
```

use

```math
q(x)
=
-x
```

Therefore

```math
p_r=-1
```

and

```math
p_\phi=-1
```

inside the core.

This region has

```math
\epsilon+p_r+p_\phi
=
\epsilon-2
```

and with $\epsilon=1$ it gives a negative active source.

This is the central locally repulsive stress region.

---

## Region II — smooth inner transition

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

and

```math
q(x)
=
\left[
1-s(u)
\right]
q_{\mathrm{core}}(x)
+
s(u)
q_{\mathrm{ann}}(x)
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
s(u)
q'_{\mathrm{ann}}(x)
+
\frac{s'(u)}{x_+-x_-}
\left[
q_{\mathrm{ann}}(x)
-
q_{\mathrm{core}}(x)
\right]
```

---

## Region III — conserved transfer annulus

For

```math
x_+<x<\beta
```

use

```math
q(x)
=
-\frac{\alpha^2}{x}
```

so

```math
p_r
=
-\frac{\alpha^2}{x^2}
```

and

```math
p_\phi
=
+\frac{\alpha^2}{x^2}
```

The two in-plane stresses cancel in the integrated trace in this region.

---

## Region IV — finite outer support collar

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

and

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

This smoothly drives both $q$ and $q'$ to zero.

---

## Region V — vacuum

For

```math
x>x_{\max}
```

use

```math
q(x)=0
```

At the axis,

```math
q(0)=0
```

with regular limiting values

```math
p_r(0)=-1
```

and

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

Therefore there is no hidden singular line force at the radial boundary.

---

# 4. Finite vertical profile

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
-\delta
\le
\zeta
\le
0
```

where

```math
y
=
\frac{\zeta+\delta}{\delta}
```

and set $\varphi_\delta=0$ outside the slab.

The profile is normalized because

```math
\int_{-\delta}^{0}
\varphi_\delta(\zeta)
\,d\zeta
=
1
```

It also vanishes at both vertical boundaries.

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

Because $U_0>0$, changing $U_0$ rescales the source and acceleration but does not change the sign or normalized coefficient.

---

# 5. Analytic local-conservation proof

For $x>0$,

```math
p_r
=
\frac{q}{x}
```

and

```math
p_\phi
=
q'
```

Therefore

```math
\frac{dp_r}{dx}
=
\frac{q'}{x}
-
\frac{q}{x^2}
```

The cylindrical radial conservation equation is

```math
\frac{dp_r}{dx}
+
\frac{p_r-p_\phi}{x}
```

Substituting the definitions gives

```math
\frac{dp_r}{dx}
+
\frac{p_r-p_\phi}{x}
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
```

Therefore

```math

\frac{dp_r}{dx}
+
\frac{p_r-p_\phi}{x}
=
0

```

identically wherever the source is differentiable.

The smoothing construction makes $q$ and $q'$ continuous across the interfaces.

Thus no omitted radial delta-function force is required.

Since

```math
p_z=0
```

and

```math
T_{\hat r\hat z}=0
```

there is no nonzero $z$-indexed stress whose vertical derivative would introduce an additional support force.

The common vertical factor multiplies the entire in-plane conserved stress pattern and therefore does not spoil the radial identity.

Consequently, in the flat background used by the linearized calculation,

```math

\partial_\mu T^{\mu\nu}=0

```

for the constructed static source.

This result must be described as:

```text
LOCAL_CONSERVATION_LINEARIZED_ORDER=ESTABLISHED
```

It is **not** yet the exact curved-spacetime statement

```math
\nabla_\mu T^{\mu\nu}=0
```

for a self-consistently solved nonlinear Einstein geometry.

---

# 6. Positive energy and energy-condition proof

Choose

```math

\epsilon(x)
=
\max
\left(
|p_r(x)|,
|p_\phi(x)|
\right)

```

with $p_z=0$.

Then immediately,

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
|p_z|=0\le\epsilon
```

For diagonal type-I stress-energy, the pointwise dominant energy condition is

```math
\epsilon\ge0
```

and

```math
|p_i|\le\epsilon
```

for every principal pressure.

Therefore

```text
DEC=SATISFIED
```

The weak energy condition requires

```math
\epsilon\ge0
```

and

```math
\epsilon+p_i\ge0
```

The null energy condition requires

```math
\epsilon+p_i\ge0
```

Because

```math
p_i\ge-|p_i|
```

and

```math
\epsilon\ge|p_i|
```

we have

```math
\epsilon+p_i
\ge
\epsilon-|p_i|
\ge
0
```

Therefore

```text
WEC=SATISFIED
NEC=SATISFIED
DEC=SATISFIED
```

Some inequalities are saturated at some points.

The construction does **not** require negative energy density.

---

# 7. Positive far-field active mass proof

Define the dimensionless positive mass factor

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

The integrated spatial stress trace is

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

Using

```math
p_r=\frac{q}{x}
```

and

```math
p_\phi=q'
```

gives

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

But

```math
q+xq'
=
\frac{d}{dx}
\left(
xq
\right)
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

The boundary conditions are

```math
q(0)=0
```

and

```math
q(x_{\max})=0
```

Therefore

```math

\tau_\delta=0

```

The integrated active mass factor is therefore

```math
m_{\mathrm{active}}
=
m_\delta+\tau_\delta
=
m_\delta
```

and hence

```math

m_{\mathrm{active}}>0

```

The source is therefore locally repulsive near the target while retaining positive far-field active mass.

The result is **not** a negative-ADM-mass construction.

---

# 8. Local-field calculation

Define

```math
A(x)
=
\epsilon(x)
+
p_r(x)
+
p_\phi(x)
```

because $p_z=0$.

For the finite-thickness slab define the dimensionless vertical kernel

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

The dimensionless field factor is

```math

F_\delta
=
-
\int_0^{x_{\max}}
xA(x)K_\delta(x)
\,dx

```

The physical axial acceleration is

```math

a_z
=
\frac{
2\pi G U_0
}{
c^2
}
F_\delta

```

Because $U_0>0$,

```math
F_\delta>0
```

is equivalent to an outward acceleration in the adopted sign convention.

The total energy-equivalent mass is

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

Eliminating $U_0$ between $M$ and $a_z$ gives

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

C
=
\frac{
m_\delta
}{
2F_\delta
}

```

Thus the numerical portion of the constructive proof reduces to evaluating the explicitly specified integrals and showing

```math
F_\delta>0
```

---

# 9. Numerical result

For the finest tested source,

```text
ALPHA=1.437500564637
BETA=4.701437405300
DELTA=0.00625000
INNER_WIDTH=0.00156250
OUTER_WIDTH=0.00625000
OUTER_RADIUS=4.707687405300
```

the numerical invariants are:

```text
MASS_FACTOR=
1.110076490539830e+01

INTEGRATED_STRESS_TRACE_FACTOR=
2.922107000813412e-13

ACTIVE_MASS_FACTOR=
1.110076490539859e+01

FIELD_FACTOR_GL64=
2.352695737495157e-01

FIELD_FACTOR_NESTED_ADAPTIVE_QUAD=
2.352695737495351e-01

FIELD_METHOD_ABS_DIFFERENCE=
1.942890293094024e-14

C_GL64=
2.359158629924866e+01

C_NESTED=
2.359158629924672e+01

MAX_CONTROL_VOLUME_CONSERVATION_RESIDUAL=
3.103073353827313e-14

MAX_DEC_VIOLATION=
0

MIN_NEC_MARGIN=
0
```

Therefore

```math

F_\delta
=
0.2352695737495\ldots
>
0

```

and hence

```math

a_z>0

```

for the explicit finite source.

This is not a marginal sign.

The two independent vertical-integration methods differ by only approximately

```math
1.94\times10^{-14}
```

in absolute field factor while the field itself is approximately

```math
2.35\times10^{-1}
```

---

# 10. Finite-thickness convergence

The regularization sequence is:

| $\delta=t/h$ |      $m_\delta$ |     $F_\delta$ | $C=m_\delta/(2F_\delta)$ |
| -----------: | --------------: | -------------: | -----------------------: |
|      0.40000 | 11.369718516276 | 0.149453529535 |          38.037638025730 |
|      0.20000 | 11.233723934208 | 0.190019680852 |          29.559369544823 |
|      0.10000 | 11.165255241660 | 0.212604998246 |          26.258214373557 |
|      0.05000 | 11.130897375158 | 0.224509078286 |          24.789414887263 |
|      0.02500 | 11.113686825672 | 0.230618147495 |          24.095429926871 |
|      0.01250 | 11.105073553053 | 0.233712433325 |          23.757986246352 |
|      0.00625 | 11.100764905398 | 0.235269573750 |          23.591586299249 |

The independently established thin conserved reference is

```math
C_{\mathrm{thin}}
=
23.426710175391
```

The finite sequence approaches the thin value monotonically from above.

For the finest source,

```math
\frac{
C_{\mathrm{finite}}
-
C_{\mathrm{thin}}
}{
C_{\mathrm{thin}}
}
\approx
7.04\times10^{-3}
```

or approximately

```math
0.704\%
```

This is evidence that the outward field is not an artifact of one particular finite smoothing width.

---

# 11. Restoring physical dimensions

The normalized field factor is

```math
F_\delta
\approx
0.2352695737495
```

For a desired acceleration $a_z$, the required positive surface-energy scale is

```math
U_0
=
\frac{
a_zc^2
}{
2\pi GF_\delta
}
```

For

```math
a_z=g
```

this gives approximately

```math
U_0
\approx
8.93\times10^{27}
\ {\mathrm{J}\,m^{-2}}
```

The total mass-equivalent scaling is

```math

M_{\mathrm{equiv}}
=
23.591586299249
\frac{
ah^2
}{
G
}

```

For

```math
a=g
```

and

```math
h=1\ {\mathrm{m}}
```

the equivalent mass is approximately

```math
M_{\mathrm{equiv}}
\approx
3.47\times10^{12}\ {\mathrm{kg}}
```

The equivalent rest energy is

```math
E
=
M_{\mathrm{equiv}}c^2
```

giving approximately

```math
E
\approx
3.12\times10^{29}\ {\mathrm{J}}
```

This is why the construction is not remotely a practical human-scale source.

The dimensionless weak-field compactness is nevertheless tiny:

```math
\frac{
GM
}{
hc^2
}
\sim
2.6\times10^{-15}
```

Therefore the enormous practical cost is not caused by the source producing a strongly curved spacetime.

It is caused by the enormous stress-energy required to generate $1g$ at meter scale.

---

# Result

The central result is:

> **An explicit finite-radius, finite-thickness, nonsingular, positive-energy, locally conserved type-I stress-energy configuration satisfying NEC, WEC, and DEC produces an outward local gravitational field in static linearized general relativity while retaining positive far-field active mass.**

In compact form, the constructed source satisfies

```math
\epsilon\ge0
```

```math
|p_i|\le\epsilon
```

```math
\partial_\mu T^{\mu\nu}=0
```

```math
M_{\mathrm{active}}>0
```

and numerically

```math
F_\delta>0
```

for the explicitly defined finite source.

The strongest project classification is therefore:

```text
MATHEMATICAL_LOCAL_REPULSION=ESTABLISHED

FINITE_POSITIVE_ENERGY_LINEARIZED_GR_CONSTRUCTION=ESTABLISHED

FINITE_RADIUS=YES

FINITE_THICKNESS=YES

NONSINGULAR_OUTER_SUPPORT=YES

LOCAL_CONSERVATION_LINEARIZED_ORDER=ESTABLISHED

NEC=PASS

WEC=PASS

DEC=PASS

OUTWARD_LOCAL_GRAVITATIONAL_FIELD=ESTABLISHED

POSITIVE_FAR_FIELD_ACTIVE_MASS=ESTABLISHED

EXACT_NONLINEAR_GR_REALIZATION=NOT_ESTABLISHED

DYNAMIC_STABILITY=NOT_ESTABLISHED

KNOWN_MATERIAL_REALIZATION=NO

ENERGETIC_PRACTICALITY=NO

PRACTICAL_ANTIGRAVITY_DEVICE=NO

NEW_PHYSICS_DISCOVERY=NO
```

---

# Verification

## Analytical

The following portions do not depend on numerical optimization once the source is specified.

### Local conservation

The identity

```math
p_r=\frac{q}{x}
```

and

```math
p_\phi=q'
```

implies exactly

```math
\frac{dp_r}{dx}
+
\frac{p_r-p_\phi}{x}
=
0
```

### Energy conditions

The choice

```math
\epsilon
=
\max
\left(
|p_r|,
|p_\phi|
\right)
```

with $p_z=0$ proves type-I DEC, and therefore WEC and NEC.

### Positive integrated active mass

The spatial stress trace reduces to a boundary term:

```math
\tau_\delta
=
2
\left[
xq(x)
\right]_0^{x_{\max}}
=
0
```

while

```math
m_\delta>0
```

Therefore

```math
M_{\mathrm{active}}>0
```

analytically.

### Finite support

The source has explicitly finite radial and vertical support and no singular outer ring.

---

## Numerical

The local-field sign was evaluated with two different vertical-integration methods:

```text
METHOD_1=
64_POINT_GAUSS_LEGENDRE

METHOD_2=
NESTED_ADAPTIVE_SCIPY_QUAD
```

They gave

```text
FIELD_FACTOR_GL64=
2.352695737495157e-01

FIELD_FACTOR_NESTED=
2.352695737495351e-01
```

with difference

```text
1.942890293094024e-14
```

Both are positive.

The conservation control-volume residual is

```text
3.103073353827313e-14
```

The DEC violation diagnostic is

```text
0
```

The minimum sampled NEC margin is

```text
0
```

The finite-thickness convergence sequence approaches the independent thin architecture monotonically.

The repository known-solution suite at the end of the research slice was:

```text
94 passed
```

---

## Dimensional

The active source combination

```math
\epsilon+p_r+p_\phi+p_z
```

has units of energy density.

Therefore

```math
\frac{G}{c^2}
S\,d^3x
```

has dimensions

```math
\frac{
{\mathrm{m^3}}
}{
{\mathrm{kg\,s^2}}
}
\frac{
{\mathrm{J}}
}{
{\mathrm{m^3}}
}
\frac{
{\mathrm{kg}}
}{
{\mathrm{J}}/c^2
}
```

consistent with a gravitational potential contribution.

The final mass scaling

```math
M
=
C\frac{ah^2}{G}
```

is dimensionally correct because

```math
\left[
\frac{ah^2}{G}
\right]
=
\frac{
({\mathrm{m}\,s^{-2}})
({\mathrm{m^2}})
}{
{\mathrm{m}^3\,kg^{-1}\,s^{-2}}
}
=
{\mathrm{kg}}
```

The coefficient $C$ is dimensionless.

---

## Limiting cases

### Thin-source limit

As the finite regularization scale decreases,

```math
\delta\rightarrow0
```

the finite coefficient approaches the independently obtained thin conserved value

```math
C_{\mathrm{thin}}
=
23.426710175391
```

### Zero source amplitude

As

```math
U_0\rightarrow0
```

both source stress-energy and acceleration vanish linearly.

### Far field

The vanishing integrated stress trace and positive energy imply positive asymptotic active mass.

Therefore the far field is attractive rather than globally repulsive.

### Weak-field validity

For the $1g$, $1,{\mathrm{m}}$ illustrative normalization, the compactness remains of order

```math
10^{-15}
```

so the metric perturbation remains small even though the required source energy is enormous.

---

## Literature comparison

Known GR already contains gravitationally repulsive regimes, including positive-$\Lambda$ cosmology, domain-wall-like stress, and Reissner-Nordström behavior.

Therefore this journal does not claim that the **existence of gravitational repulsion in GR** is new.

The project-derived contribution is the explicit finite 006D construction satisfying the stated combination of:

```text
FINITE_RADIUS
FINITE_THICKNESS
POSITIVE_ENERGY
LOCAL_CONSERVATION_AT_LINEARIZED_ORDER
NEC
WEC
DEC
LOCAL_OUTWARD_FIELD
POSITIVE_FAR_FIELD_ACTIVE_MASS
```

The novelty of this exact construction relative to the full published literature has **not** been established.

Therefore:

```text
NOVELTY=NOT_ESTABLISHED
```

and

```text
NEW_PHYSICS_DISCOVERY=NO
```

remain mandatory classifications.

---

# Falsification Attempt

The project deliberately tried to identify ways in which the 006D conclusion could be false or overstated.

## 1. Could the outward field be a sign-convention error?

The acceleration convention was explicitly fixed.

The Green-function field was independently evaluated using two vertical-integration methods.

Both returned the same positive field factor.

This reduces, but does not mathematically eliminate, implementation-sign risk.

---

## 2. Could the source fail local conservation?

The radial conservation law is analytic, not merely numerical.

In addition, 150 finite radial control volumes were tested.

Maximum residual:

```text
3.103073353827313e-14
```

This is consistent with numerical integration error.

---

## 3. Could the support contain a hidden singular ring?

The outer smoothstep drives

```math
q(x_{\max})=0
```

and

```math
q'(x_{\max})=0
```

so the regularized source does not require a singular boundary line force.

---

## 4. Could the source secretly use negative energy?

No.

By construction,

```math
\epsilon\ge0
```

pointwise.

---

## 5. Could the source violate DEC?

No within the specified type-I model.

By construction,

```math
|p_i|\le\epsilon
```

for all principal stresses.

---

## 6. Could the far field correspond to negative active mass?

No within the linearized construction.

The integrated stress trace vanishes and the integrated positive energy is strictly positive.

---

## 7. Could the result be a finite-thickness numerical artifact?

The coefficient converges monotonically toward the independent thin conserved reference as $\delta$ decreases.

The sign remains outward throughout the tested convergence sequence.

---

## 8. Could the linearized approximation itself invalidate the result?

This remains an important limitation.

006D proves the construction only at linearized order.

An exact nonlinear solution with self-consistent

```math
\nabla_\mu T^{\mu\nu}=0
```

has not been constructed.

However, the target metric compactness for the illustrative $1g$, $1,{\mathrm{m}}$ scaling is extremely small.

This makes an ordinary strong-curvature failure unlikely to be the leading issue, but it is **not** an exact nonlinear proof.

---

## 9. Could dynamic instability destroy the source?

Yes.

No complete dynamical or constitutive stability proof exists.

The stress tensor was constructed mathematically.

No known matter model has yet been shown to hold these stresses stably.

Therefore:

```text
DYNAMIC_STABILITY=NOT_ESTABLISHED
```

---

## 10. Could a known material realize the source?

No known material realization has been demonstrated.

This is currently one of the major barriers separating the mathematical result from physical engineering.

---

# Standalone Reconstruction

A scientist should not need to trust project modules to reproduce the numerical part of the headline claim.

Create a clean environment:

```bash
python3 -m venv .verify-006d
source .verify-006d/bin/activate

python -m pip install --upgrade pip
python -m pip install numpy scipy
```

Save the following as:

```text
verify_006d_from_journal.py
```

and run:

```bash
python verify_006d_from_journal.py
```

```python
#!/usr/bin/env python3
"""Standalone verifier for the 006D finite-source construction.

This script imports no ANTIGRAVITY_RESEARCH project modules.

It reconstructs the normalized 006D stress source directly from the equations
and constants recorded in the research journal and evaluates:

- positive energy;
- DEC / WEC / NEC;
- local flat-background conservation;
- integrated spatial-stress trace;
- positive far-field active mass;
- outward local axial gravitational field;
- finite-source coefficient C.

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
    """Return q=x*p_r and dq/dx for the exact finite source."""

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
            - sp
            * q_annulus
        )

        return q, qp

    return 0.0, 0.0


def surface_profiles(
    x: float,
) -> tuple[float, float, float]:
    """Return epsilon, p_r, and p_phi."""

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
    """Return normalized finite vertical bump."""

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
    """Evaluate axial field using Gauss-Legendre vertical quadrature."""

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
    """Evaluate same field with adaptive z integration."""

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
    """Check conservation over 150 radial control volumes."""

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
        "=== JOURNAL 006D STANDALONE VERIFICATION ==="
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
=== JOURNAL 006D STANDALONE VERIFICATION ===
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

# Repository Cross-Check

The repository reference implementation is:

```text
simulations/006d_finite_thickness_conserved_source.py
```

The recorded SHA-256 in the codebundle snapshot is:

```text
e303b3bb454d19cc16516e189e6db559d1812dad733f9e02bf1ecafce2594d76
```

Run the repository implementation with:

```bash
ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"

PYTHONPATH="$ROOT/src" \
"$PY" simulations/006d_finite_thickness_conserved_source.py
```

Run the focused regression test with:

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

Current expected baseline:

```text
94 passed
```

A future publication-quality verification should ideally include a separately authored implementation of the complete 006D finite-thickness field calculation.

That has not yet been completed.

---

# Claims Status

The journal records the following project claim as supported within its stated approximation:

> **Within static linearized general relativity, there exists an explicit finite-radius, finite-thickness, nonsingular, positive-energy, locally conserved type-I stress-energy configuration satisfying NEC, WEC, and DEC whose calculated near field points outward while its far-field active mass remains positive.**

Recommended claims ledger:

```text
MATHEMATICAL_LOCAL_REPULSION=
ESTABLISHED_IN_006D_SCOPE

FINITE_POSITIVE_ENERGY_LINEARIZED_GR_CONSTRUCTION=
ESTABLISHED

LOCAL_CONSERVATION_LINEARIZED_ORDER=
ESTABLISHED

NEC=
PASS

WEC=
PASS

DEC=
PASS

OUTWARD_LOCAL_GRAVITATIONAL_FIELD=
ESTABLISHED

POSITIVE_FAR_FIELD_ACTIVE_MASS=
ESTABLISHED

C_FINITE_BEST_TESTED=
23.591586299249

C_THIN_REFERENCE=
23.426710175391

EXACT_NONLINEAR_GR_REALIZATION=
NOT_ESTABLISHED

FULL_CURVED_SPACETIME_CONSERVATION=
NOT_ESTABLISHED

DYNAMIC_STABILITY=
NOT_ESTABLISHED

KNOWN_MATERIAL_REALIZATION=
NO

ENERGETIC_PRACTICALITY=
NO

EXPERIMENTAL_ACCESSIBILITY=
NOT_ESTABLISHED

GLOBAL_POSITIVE_MASS_REPULSION=
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

This journal entry does not assume that `CLAIMS.md` has already been edited.

If `CLAIMS.md` does not currently contain the above classification, it should eventually be synchronized with this record.

---

# Why This Result Matters

The principal conceptual conclusion is:

> **Positive local energy and the standard classical energy conditions do not by themselves forbid a finite locally repulsive gravitational near field in static linearized GR.**

The construction shows explicitly that the sign of the local gravitational field depends on relativistic stress as well as energy density.

The project therefore moved from asking:

> Can positive-energy GR produce local repulsion at all?

to asking:

> Can the required relativistic stress pattern be produced by a stable, realizable, energetically plausible physical system?

The sign problem was solved within the stated mathematical model.

The realizability and energy-scale problems were not.

The severe scaling

```math
M
=
C\frac{ah^2}{G}
```

remains the primary classical obstacle.

Even the theoretical coefficient-one scale would require

```math
M
\sim
1.47\times10^{11}\ {\mathrm{kg}}
```

for $1g$ at $1,{\mathrm{m}}$.

The explicit finite source requires roughly

```math
3.47\times10^{12}\ {\mathrm{kg}}
```

equivalent stress-energy.

This is why the result is scientifically interesting but not presently technologically useful.

---

# Subsequent Research Update — Frontier Through 010E-Y

The research did not stop at 006D.

After establishing the headline classical result, the project deliberately investigated whether another physically consistent mechanism could evade the catastrophic classical $ah^2/G$ scaling.

The major late-session branch became a hypothetical **ground-referenced ultralight scalar fifth force**.

This branch must remain scientifically separate from the 006D GR result.

It is not ordinary general-relativistic antigravity.

---

## Current fifth-force benchmark

The working range is

```math
\lambda
=
5000\ {\mathrm{m}}
```

which corresponds to mediator mass

```math
m_\phi
=
\frac{\hbar c}{\lambda}
=
3.946539608\times10^{-11}\ {\mathrm{eV}}
```

The working Yukawa strength is

```math
\alpha_Y
=
2\times10^{-4}
```

with source coupling

```math
\alpha_{\mathrm{source}}
=
10^{-2}
```

The activated test state needed for approximately $1g$ in the selected half-space benchmark is

```math
\alpha_{\mathrm{activated}}
=
-1.558991777087370\times10^5
```

This is an enormous material-state-dependent scalar response.

The exact current $5,{\mathrm{km}}$ experimental margin has **not** yet been numerically reconstructed from modern exclusion-curve data.

Therefore:

```text
CURRENT_EXACT_5KM_BOUND=
NOT_CLOSED
```

---

# Major negative results after 006D

The following ideas were tested and rejected or superseded:

```text
LIGHT_POINTLIKE_HIDDEN_CARRIER_PER_ATOMIC_CELL=
REJECTED_BY_LOCALIZATION_NATURALNESS_NO_OVERLAP

MATERIAL_CREATED_10KEV_HIDDEN_CONDENSATE=
REJECTED_AS_PRACTICAL_ENERGY_ROUTE

DIRECT_UNPROTECTED_ELECTRON_MASS_PORTAL=
REJECTED_BY_RADIATIVE_NATURALNESS

SIMPLE_FUNDAMENTAL_ELECTRON_CURRENT_MEDIATOR=
REJECTED_BY_ELECTRON_G_MINUS_2_PREFLIGHT

CONTINUOUS_LINEAR_STRUCTURAL_SELECTOR=
REJECTED_BY_SCALAR_POLARIZATION

SIMPLE_EVEN_STRUCTURAL_MONOMIAL_SELECTOR=
REJECTED_BY_ZERO_POINT_AND_THERMAL_LEAKAGE

NORMAL_ORDERED_QUADRATIC_SELECTOR=
REJECTED_BY_FINITE_TEMPERATURE_LEAKAGE

UNIVERSAL_HIGH_SPIN_PORTAL=
REJECTED_BY_ORDINARY_MATTER_LEAKAGE

ACCIDENTALLY_TUNED_POLYNOMIAL_SELECTOR=
REJECTED_AS_UNPROTECTED_FINE_TUNING

FUNDAMENTAL_RELATIVISTIC_DIMER=
REJECTED_BY_ULTRALIGHT_SCALAR_NATURALNESS

GENERIC_UNPROTECTED_RELATIVISTIC_UV_MATCH=
REJECTED_BY_OPERATOR_LEAKAGE
```

These negative results are part of the scientific progress.

They should not be erased simply because the corresponding gate executed successfully.

---

# Finite-size stability correction

A major conceptual correction emerged in 010E-V.

A locally negative scalar effective mass squared,

```math
m_{\mathrm{eff}}^2<0
```

does **not** automatically imply instability for a finite body.

For a spherical region of radius $R$ with interior

```math
m_{\mathrm{in}}^2
=
-\mu^2
```

and exterior scalar mass $m_\phi$, the first static zero mode satisfies

```math
\mu\cot(\mu R)
=
-m_\phi
```

Defining

```math
x=\mu R
```

gives

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

The representative direct-material model gave values below this threshold.

This reopened finite material configurations that had previously been rejected using an infinite-medium condition.

---

# Cooperative dinuclear selector

The material-specific scalar charge was eventually factorized as

```math
Q_N
=
B_{\mathrm{material}}
\prod_{i=1}^{N}
P_{\mathrm{HS},i}
```

where:

* $B_{\mathrm{material}}$ fixes the bound material identity;
* $P_{\mathrm{HS},i}$ selects the activated high-spin internal states.

This separates **what material it is** from **whether it is activated**.

The project found a finite cluster-size window because thermal leakage decreases strongly with $N$ while switching susceptibility increases with $N$.

At $77,{\mathrm{K}}$ the selected one-ton benchmark gives

```text
N_MIN_LEAKAGE=2
N_MAX_STABILITY=5
```

making a dinuclear $N=2$ architecture the current lowest-complexity survivor.

For that benchmark:

```text
DINUCLEAR_STABILITY_T_MIN_K=
28.13102372293623

DINUCLEAR_LEAKAGE_T_MAX_K=
101.8315502857560

DINUCLEAR_77K_ALL_HS_LEAKAGE=
1.989338055378181e-9

DINUCLEAR_77K_LEAKAGE_MARGIN=
290.1950942786034

DINUCLEAR_77K_MU_R=
0.9556137730170507

DINUCLEAR_77K_STABILITY_MARGIN=
1.643839124818559
```

These numbers are **model-side parametric results**, not measured material properties.

---

# 010E-Y local composite result

The strongest current speculative fifth-force result is a local nonrelativistic composite construction.

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

with total conserved number

```math
N
=
N_A+N_B+2N_D
```

The local conversion interaction is

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

and the scalar interaction is

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

Consequently the low-energy model gives

```math
\frac{dE_A}{d\phi}=0
```

```math
\frac{dE_B}{d\phi}=0
```

while the dressed bound state has

```math
\frac{dE_{\mathrm{bound}}}{d\phi}
=
g_DZ_D
```

The explicit Y calculation found

```text
TARGET_DINUCLEAR_COUPLING=
8.638353631211470e-12

BARE_DIMER_SCALAR_COUPLING=
8.904546001587151e-12

DIMER_FRACTION_AT_EARTH_PHI=
0.9701060143517443

ISOLATED_A_SCALAR_CHARGE=
0

ISOLATED_B_SCALAR_CHARGE=
0
```

The independent finite-difference Feynman-Hellmann error was

```text
3.079119804066939e-10
```

Therefore the current low-energy conclusion is:

> **Locality and Feynman-Hellmann do not by themselves force a bound-state-specific scalar response onto the isolated constituents in a strict particle-number-conserving nonrelativistic composite EFT.**

This is a low-energy result only.

---

# Independent two-body representation

The same low-energy response was reproduced using

```math
\mathcal H_{\phi,2}
=
C_\phi
\phi
A^\dagger B^\dagger BA
```

For a representative pair radius of $3,{\mathrm{\AA}}$,

```text
C_PHI=
9.536416387852626e-20 eV^-3
```

The atomic EFT cutoff is approximately

```text
657.7566 eV
```

and the dimensionless Wilson strength is

```text
2.713818830692468e-11
```

Thus the required pair operator is perturbatively small at the selected atomic EFT scale.

Again, this does **not** establish that the Standard Model generates the operator.

---

# Current UV obstruction

If the entire dinuclear object is incorrectly treated as a fundamental relativistic particle, the scalar naturalness problem is catastrophic.

The calculated loop ratios were

```text
RELATIVISTIC_FERMION_DIMER_LOOP_TO_TARGET_MASS2=
1.155053548350539e19

RELATIVISTIC_SCALAR_DIMER_LOOP_TO_TARGET_MASS2=
2.310107096701078e19
```

Therefore

```text
FUNDAMENTAL_RELATIVISTIC_DIMER=
REJECTED
```

Furthermore, generic one-loop mixing is

```math
\frac{1}{16\pi^2}
\approx
6.33\times10^{-3}
```

while the conservative allowed target-equivalent leakage is only

```math
5.772961445324848\times10^{-7}
```

The generic loop factor is therefore larger by approximately

```math
1.10\times10^4
```

Hence

```text
GENERIC_UNPROTECTED_RELATIVISTIC_UV_MATCH=
REJECTED
```

The surviving fifth-force branch requires an exact or technically natural protection mechanism.

---

# Updated Current Scientific Position

The 006D headline result remains the strongest established project result.

Nothing discovered after 006D replaces or weakens it.

The later 010E work addresses a different question: whether an antigravity-like force can be made more practically efficient using speculative new physics.

The current status is therefore:

```text
006D_MATHEMATICAL_LOCAL_GR_REPULSION=
ESTABLISHED_IN_STATED_SCOPE

006D_FINITE_POSITIVE_ENERGY_SOURCE=
ESTABLISHED_IN_STATED_SCOPE

006D_NEC_WEC_DEC=
PASS

006D_LOCAL_CONSERVATION_LINEARIZED_ORDER=
ESTABLISHED

006D_POSITIVE_FAR_FIELD_ACTIVE_MASS=
ESTABLISHED

006D_PRACTICALITY=
NO

GROUND_REFERENCED_ULTRALIGHT_SCALAR_BRANCH=
SPECULATIVE

DINUCLEAR_LOW_ENERGY_COMPOSITE_EFT=
PARAMETRIC_SURVIVOR

BOUND_STATE_SPECIFIC_SCALAR_RESPONSE=
EXPLICIT_LOW_ENERGY_CONSTRUCTION

FULL_RELATIVISTIC_UV_COMPLETION=
NOT_ESTABLISHED

ACTUAL_MICROSCOPIC_ORIGIN_OF_C_PHI=
NOT_ESTABLISHED

KNOWN_REAL_MATERIAL_WITH_REQUIRED_PORTAL=
NO

EXACT_CURRENT_5KM_BOUND=
NOT_CLOSED

PRACTICAL_ANTIGRAVITY_DEVICE=
NO

NEW_PHYSICS_DISCOVERY=
NO

NOVELTY=
NOT_ESTABLISHED
```

---

# Open Questions

## 006D classical construction

1. Does an exact nonlinear Einstein solution continuously connected to the 006D source exist?

2. Can exact curved-spacetime conservation

```math
\nabla_\mu T^{\mu\nu}=0
```

be satisfied by a finite self-consistent matter configuration with the same qualitative near-field sign?

3. Is the source dynamically stable?

4. Can any known field or matter model produce the required principal stresses?

5. Is there a rigorous universal lower bound on the coefficient $C$ for finite conserved DEC sources?

6. Can any physically motivated matter model change the severe

```math
\frac{ah^2}{G}
```

scaling rather than merely improve $C$ by a factor of order unity?

## Current fifth-force frontier

1. Can a local relativistic microscopic theory generate

```math
C_\phi\phi A^\dagger B^\dagger BA
```

while forbidding dangerous one-body scalar operators?

2. What exact symmetry or conservation structure provides the required protection?

3. Does renormalization-group running regenerate one-body charge above

```math
5.77\times10^{-7}
```

of the target response?

4. Can the mediator mass

```math
m_\phi
\approx
3.95\times10^{-11}\ {\mathrm{eV}}
```

remain technically natural?

5. Can the NR coefficient $C_\phi$ be independently derived from a relativistic microscopic amplitude?

6. Does the exact modern $5,{\mathrm{km}}$ fifth-force bound permit the selected working point?

7. Does any surviving relativistic theory pass stellar and cosmological constraints?

8. Does any real spin-crossover or other bound material possess the required protected interaction?

---

# AI Assistance

AI assistant used: **ChatGPT by OpenAI**

Substantial AI-assisted work in the research program included:

* derivation and checking of weak-field GR equations;
* construction and analysis of the conserved stress profile;
* numerical integration design;
* debugging numerical quadrature;
* independent-reconstruction planning;
* dimensional analysis;
* finite-thickness convergence analysis;
* energy-condition checks;
* fifth-force model construction and falsification;
* finite-size scalar stability analysis;
* composite EFT construction;
* Feynman-Hellmann verification;
* literature-search assistance;
* research documentation.

AI-generated mathematics, code, numerical strategies, and physical interpretations are **not assumed correct merely because they were generated by an AI system**.

Important claims remain subject to:

```text
ANALYTIC_CHECK
NUMERICAL_CHECK
INDEPENDENT_RECONSTRUCTION
DIMENSIONAL_CHECK
LIMITING_CASE_CHECK
LITERATURE_COMPARISON
ASSUMPTION_AUDIT
```

Use of ChatGPT does not imply endorsement or sponsorship by OpenAI.

---

# Next Action

The 006D mathematical result should now be treated as a locked historical project result unless a genuine error is found.

Do not repeatedly reopen or re-optimize it without new physical motivation.

The highest-value active theoretical question has moved elsewhere.

The immediate frontier is:

> **Can a technically natural local relativistic microscopic theory generate the required protected two-body scalar response without inducing experimentally forbidden one-body scalar charge or destabilizing the ultralight mediator?**

The next high-information calculation should therefore construct the smallest complete relativistic operator basis and attempt to prove either:

```text
PROTECTED_RELATIVISTIC_TWO_BODY_MATCH=VIABLE
```

or

```text
CURRENT_MATERIAL_SCALAR_BRANCH=CLOSED
```

The branch should be closed rather than rescued with additional arbitrary hidden structure if unavoidable one-body leakage or scalar-mass naturalness failure is demonstrated.

---

# Final Journal Classification

The central historical result being locked in by this entry is:

> **Within static linearized general relativity, an explicit finite, nonsingular, positive-energy, locally conserved, NEC/WEC/DEC-compatible source can produce a locally outward gravitational near field while maintaining positive far-field active mass.**

The key numerical invariant is

```math

C_{\mathrm{finite}}
=
23.591586299249

```

with

```math

F_\delta
=
0.2352695737495\ldots
>
0

```

and conservation residual

```math
3.103073353827313\times10^{-14}
```

The result should remain classified as:

```text
CONSTRUCTIVE_LINEARIZED_GR_STRESS_ENERGY_RESULT
```

not as:

```text
PRACTICAL_ANTIGRAVITY_DEVICE
```

and not as:

```text
NEW_PHYSICS_DISCOVERY
```

The later 010E-Y composite fifth-force work is a distinct speculative continuation whose low-energy branch currently survives but whose relativistic microscopic realization is unresolved.
