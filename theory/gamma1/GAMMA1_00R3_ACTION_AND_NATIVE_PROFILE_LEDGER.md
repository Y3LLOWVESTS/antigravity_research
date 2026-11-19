# GAMMA1-00R3 — M0 covariant-action hypothesis and native PH16 replay

Scope: a NEW 12/L12 solution by the UNMODIFIED PH16-04R2 stationary code.
This is not the missing historical state, not a Lorentzian mode certificate,
and not a gravitational Einstein or whole-craft-force simulation.

## Candidate common-action hypothesis

Signature (-+++). The physical universal metric is

    gtilde = exp(2 sigma(P)) g

where

    sigma(P) = alpha P - beta P^2
    P = F_X star(F_Y)/2

All physical sources, neutral matter, Earth and supports see gtilde.

The proposed action skeleton is

    S = (c^3 / 16 pi G) integral_M sqrt(-g) R d^4x
        + S_GHY[g]
        - (1/4) integral_M sqrt(-g) (F_X^2 + F_Y^2) d^4x
        + S_charged[gtilde, Phi_plus, Phi_minus, A_X]
        + S_fluid[gtilde, n, u]
        + S_Earth[gtilde, Psi_E]
        + S_supports[gtilde, Psi_S]

Complex charged fields have

    D_mu Phi_s = (nabla_mu - i q_s A_Xmu) Phi_s

The canonical scalar potential follows the stationary PH16 ansatz.
The proposed skeleton has not been shown to reduce exactly to that lattice.

The fluid has epsilon(n) = m n + kappa n^2/2, but the off-shell
number-current constraint, boundary term and solid/support equation of
state have not been fully specified.

The displayed skeleton is NOT a unique complete Lorentzian action.

## Restricted variations

At fixed covariant F, the portal invariant carries Weyl weight -4:

    g_cov -> exp(2z) g_cov
    P -> exp(-4z) P

For physical-metric matter stress Ttilde, the candidate Einstein stress is

    T_E,munu = exp(2 sigma) Ttilde_munu - lambda P g_munu

where

    lambda = exp(4 sigma) trace(Ttilde) sigma_prime(P)

The Maxwell constitutive relations require X and Y variations from the
same action. The restricted conformal trace identity is checked exactly.

These symbolic checks do not replace the full Ward, Noether or Bianchi
identities involving the charged source, real neutral fluid, Earth,
supports, boundaries and gravitational field equations.

## Physical limitations

The charged source's stationary Noether numbers are 400/400.
The canonical Routhian is NOT energy measured in joules.

The weak-field neutral response includes

    a = -grad(Phi_E) - c^2 grad(sigma)

but the Einstein potential Phi_E, physical source orientation,
exterior transmission and Earth reaction have NOT been solved.

No real gravitational lift or complete SI operating energy is inferred.

## Single-mesh replay

R3 replays ONLY 12/L12 with the unchanged PH16 solver:

    CoulombSource.solve(350)
    JointAction.initialize
    JointAction.precondition_Y
    JointAction.solve(pre_seed, maxiter=450)

No alpha, beta, solver tolerance or acceptance threshold is changed.

Native F_plus, F_minus, A_X, A_Y, mesh coordinates, cell weights,
derived E_X and B_Y, portal P, sigma, and neutral density are archived
to a new immutable NPZ with a separate SHA-256.

The historical PH16-04R2 12/L12 diagnostics provide the comparison.

Agreement does not establish identical historical arrays, uniqueness,
continuum/exterior convergence or complete Lorentzian stability.

The historical 18/L12 weak-seed failure remains preserved.

## Decision boundary

The new profiles may support subsequent independent on-background
constraint, health and metric studies after the missing dynamical action
is specified.

The experiment does not automatically authorize GAMMA1-01,
PH16-05 or PH17.

006D remains the conservative finite-source GR reference,
with C = 23.591586299249, unreplaced.

Earth-down/whole-craft-up, at least 1g throughout a finite neutral
1 kg torus at at least 1m true stand-off, and complete operating energy
strictly below 10 MJ remain NOT CERTIFIED.

No candidate is promoted by this replay.
