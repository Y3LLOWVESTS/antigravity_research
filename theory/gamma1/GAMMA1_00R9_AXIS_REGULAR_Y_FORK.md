# GAMMA1-00R9 — Azimuthal axis-regularity and Green self-cell quadrature fork

## Scientific scope

R8 showed that finite exterior elimination resolves much of the original
X operator mismatch while leaving a substantial Y mismatch on the actual
PH16 R3 stationary field profile.

R9 tests two distinct possible explanations: cylindrical-axis
finite-volume representation and original Green self-cell quadrature.

No source solution is rerun.

## Exact continuum identity

For an orthonormal azimuthal gauge potential with regularity

    A_phi = rho*u

where u is finite at the symmetry axis,

    rho[(partial_r A_phi)^2+(partial_z A_phi)^2+A_phi^2/rho^2]
       = rho^3[(partial_r u)^2+(partial_z u)^2]
         +partial_r(rho^2*u^2).

The last term is a genuine boundary contribution. It vanishes on
integration only for appropriate axis regularity and outer boundary
conditions. The term is preserved, not silently discarded.

## Alternative derived finite-volume action

Define u=A_phi/rho on the original and exterior mesh cells.

At h=1, radial face conductance is 2*pi*rho_face^3 and axial face
conductance is 2*pi*rho_cell^3. Outer finite Dirichlet conductance
is doubled at half-cell faces. The axis face has zero flux.

Transform the u quadratic into the physical A_phi coordinates using

    K_A = diag(1/rho) K_u diag(1/rho).

The original R8 construction W*(L+diag(rho^-2)) is preserved.
Both constructions undergo exactly the same finite-domain
Schur-complement elimination.

The 46-cell original-domain interface is unchanged.

No empirical scale is inserted into either operator. Both unfitted
and best-scaled discrepancies are recorded. Best-scaled values are
diagnostic only, never same-action equivalence certificates.

## Original Green self-quadrature

The original PH15-P10 code supports self-cell Gauss quadrature orders
4, 8 and 12.

R9 constructs those original inverse-ring Y operators but evaluates
them on the same immutable R3 Y field.

Order 8 remains the original PH16-04R2 operator. Orders 4 and 12
are fixed-profile counterfactual diagnostics, NOT newly stationary
solutions of the original PH16 action.

Report residual mismatches for all three orders.

## Spatial attribution

Partition the original Green Y gradient and discrepancy into the
first two radial rows, the 46-cell box rim and the remaining interior.

A large fraction of gradient norm near the axis does not prove that
axis discretization explains the entire residual.

## Physical no-promotion rules

Increasing exterior extent at h=1 is not mesh refinement.

The finite exterior does not certify infinite-domain DtN,
actual continuum convergence, or a source-free physical exterior.

Full Lorentzian charged source, X/Y, neutral fluid, Earth, supports,
hull, Einstein variations, constrained healthy modes, full
Ward/Noether/Bianchi, gravitational acceleration, whole-craft force,
empirical/quantum/UV consistency, and complete SI energy remain open.

The benchmark remains at least 1g outward throughout a finite neutral
1kg torus at at least 1m true exterior stand-off, with complete
operating energy strictly below 10 MJ.

No GAMMA1-01, PH16-05 or PH17 automatic authorization.
006D, C=23.591586299249, remains unreplaced.
