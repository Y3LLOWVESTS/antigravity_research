# GAMMA1-00R6 — Restricted stress-trace bridge versus nodal Maxwell obstruction

**Provenance:** R3 12/L12 native profile, R5 stationary portal multiplier and
original PH16-04R2 producing source are immutable and SHA locked. No PDE is rerun.

## Pre-registered physical discriminant

H_TRACE: Does the fixed-Noether PH16 matter Routhian's cellwise derivative
with respect to its conformal factor equal the *restricted static Weyl trace*
of a candidate charged-scalar-plus-conserved-neutral-fluid action? This would
be a necessary bridge, not proof of a complete Lorentzian action.

H_KERNEL: Does the original reciprocal free-space ring-Green inverse quadratic
K_X/K_Y equal, up to a constant scale per carrier, the energy Hessian of the
local PH16 nodal derivatives used to construct P? This tests one explicit
finite-cell reduction, not arbitrary Galerkin/continuum formulations.

## Candidate trace, signature -+++

For the candidate universal metric g_tilde=exp(2 sigma)g, the charged
scalar's fixed-charge Routhian contains e2 spatial gradient energy,
minus e2*W_s^2*f_s^2, plus e4*U, with W_s=omega_s-q_s*A_X.
The gradient energy is allocated half per endpoint on each original
PH16 scalar edge. Fluid labels n_label=n*exp(3 sigma) are conserved.

At each cell with quadrature weight w, the resulting *restricted
physical-matter Weyl trace density times Einstein-volume factor* is

    tau = -2*K_spatial_cell/w + 2*e2*sum(W_s^2*f_s^2)
          -4*e4*U - mass*n_label*exp(sigma)
          + kappa*n_label^2*exp(-2 sigma)

and the provisional portal multiplier is

    lambda_trace_candidate = tau * (alpha-2 beta P).

R6 compares this independently constructed candidate to the R5
lambda_Routhian on all 288 actual recovered cells. Equality is a
restricted fixed-charge/static/quadrature property only; it does not
supply the full off-shell source, fluid, solid, Earth, boundary or
Einstein variational theory. In particular it is not an independent
measurement of active gravitational mass, pressure, energy or lift.

## Nodal Maxwell comparator

Using the native PH16 source derivative operators and volume weights:

    L_X_nodal = Dr.T W Dr + Dz.T W Dz
    L_Y_nodal = BR.T W BR + BZ.T W BZ

Compare these to the original nonlocal inverse ring-Green operators
K_X and K_Y, independently fitting the best positive or signed
single scaling s = tr(K.T L)/tr(L.T L). Record relative Frobenius
mismatch ||K-sL||_F/||K||_F for whole grid and boundary-excluded 220
cells. Record on-native-field gradient mismatch with its own optimized
scaling, plus positive local-self and factor-seven controls.

**If K != sL, that only rejects the specific direct nodal-quadrature
identification.** It does not rule out the original reciprocal free-space
Green discretization, a different nonlocal Galerkin representation,
convergence to Maxwell in a continuum limit, or another physically
justified action. Such possibilities require explicit matching and
convergence; none may be silently presumed from stationarity.

## Hard limits and decision

No complete Lorentzian constrained spectrum, full off-shell Ward/
Noether/Bianchi, UV/empirical constraints, stable manufactured source,
Einstein stress/exterior metric, Earth-down/whole-craft-up force,
physical 1 kg neutral torus at >=1m receiving >=1g, or complete
SI energy strictly below 10 MJ is established. The canonical Routhian
is not joules. GAMMA1-01, PH16-05 and PH17 remain unauthorized.
006D with C=23.591586299249 remains unreplaced.
