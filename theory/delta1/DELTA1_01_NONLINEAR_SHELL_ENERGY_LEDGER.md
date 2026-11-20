# DELTA1-01 — Exact nonlinear spherical electric-shell transducer

**Scope:** Canonical massless scalar + positive exponential gauge-kinetic
operator; ideal fixed-charge spherical conductor, flat background and
zero bare matter scalar charge. This is a new analytic radial benchmark,
NOT an executable antigravity device or full Lorentzian Einstein model.

The action inventory is Einstein gravity, canonical positive scalar,
U(1) gauge field with `Z(phi)=exp(eta*phi)>0`, and ordinary matter
universally coupled to `g_tilde=exp(2*alpha*phi)*g`.

The shell is a deliberately massless/support-free idealization.
It is NOT a real charged material and does not satisfy project source
realizability conditions. Its X electric field extends outside the shell.

## Exact fixed-charge sector

For shell radius `R=.5 m`, total charge `Q`, radial field `E_X`,
scalar `phi`, vacuum epsilon zero, in the static flat background:

```math
E_X(r)=\frac{Q}{4\pi\epsilon_0 r^2 e^{\eta\phi(r)}}
```

```math
E_{\rm static}=\int_{r\ge R}\left[
\frac{c^4}{8\pi G}|\nabla\phi|^2
+\frac{\epsilon_0 e^{\eta\phi}}2 E_X^2
\right]d^3x
```

Eliminating the electrostatic potential **at fixed Q** yields
`u_E=Q^2 exp(-eta*phi)/(32*pi^2*epsilon0*r^4)`; varying the same
Hamiltonian gives the scalar equation and Gauss law.

At fixed voltage, the full thermodynamic potential includes battery
work rather than varying field-only energy with an arbitrarily
reversed source sign.

Write `s=R/r` and `y=eta*phi`; impose `y(0)=0` and `y_s(1)=0`.

```math
y(s)=2\log\frac{\cos[t(1-s)]}{\cos t},
\quad 0<t<\frac\pi2
```

`Q`, `eta` and `t` obey the exact nonlinear scalar equation.
The finite field source and scalar response are solved together
in this reduced radial subsystem, not superposed or prescribed.

The exact positive exterior energies are:

```math
E_X=\frac{2c^4R}{G\eta^2}\,t\tan t
```

```math
E_{\phi}=\frac{2c^4R}{G\eta^2}(t\tan t-t^2)
```

The outward scalar fifth-force acceleration is:

```math
a_\phi(r)=\frac{2\alpha c^2tR}{\eta r^2}
\tan\left[t\left(1-\frac Rr\right)\right]
```

The radial acceleration has a unique maximum in `r>R`; therefore
the minimum on `[1.5,1.7] m` occurs at an endpoint.

The interval represents radial test locations, not a resolved
1 kg toroidal payload. Shell-to-nearest-matter stand-off is 1 m.

## Decision rule

For fixed positive alpha, choose eta to obtain at least
9.80665 m/s² at every radial location in the interval.
Optimize over the exact one-parameter field family t.

The exterior energy then scales as `1/alpha^2`, leaving an inferred
field-only alpha threshold for strictly less than 10 MJ.

No shell supports, battery, apparatus, Earth, material scalar
charge, switching, photons, UV loops or rest energy are included.
Even exterior energy below 10 MJ is not a physical pass.

The Einstein constraints and gravitational/metric stress
response are not solved. Gauge positivity `Z>0` is necessary,
not full constrained Lorentzian stability.

The static radial second variation is positive in the fixed-charge
scalar subspace, which does not prove that real charged matter,
the shell or all coupled modes are stable.

## Preservation and follow-on

DELTA1-00 and GAMMA N1/C1 remain immutable.
DELTA1-01 does not authorize GAMMA1-01, PH16-05, PH17
or DELTA1-02 automatically.

A massive Yukawa scalar, screened medium or new operator has a
different BVP and empirical burden. This massless radial result
is not a general no-go.

**006D unreplaced. Whole-craft force and Earth-down reaction not
derived. Complete operating energy below 10 MJ not certified.**
