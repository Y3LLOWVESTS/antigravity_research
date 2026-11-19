# GAMMA1-00R7 — Ring Green to weighted finite-volume Maxwell bridge

This is an operator representation test, NOT a new gravitational model.
The original PH16-04R2 stationary action, R3 real stationary native profile,
and R6 negative results remain immutable. No PH16 source solution is rerun.

## The actual self-adjoint free-space Green construction

The original source kernels are axisymmetric 3D Coulomb m=0 and azimuthal
m=1 Green integrals, with finite-cell self quadrature. Define G=G_ring W,
where W=diag(2 pi rho h^2). The source field action is

    E_G[v] = (1/2) v.T K v
    K = W^(1/2) [ W^(1/2) G W^(-1/2) ]^(-1) W^(1/2)

This implies K G = W and reciprocity K=K.T, as verified independently.
These are finite-matrix identities, not a continuum/exterior theorem.

## Correct physical cylindrical finite-volume comparator

The original PH15-P8 operator L approximates the scalar cylindrical
negative Laplacian in its weighted finite-volume weak form. For the
orthonormal azimuthal m=1 vector potential, the extra rho^-2 term is
mandatory:

    L_X,FV = W L
    L_Y,FV = W (L + diag(rho^-2))

Both are symmetric quadratic energies with the original P8 outer Dirichlet
boundary penalty. The Green action has an infinite-domain boundary
condition encoded nonlocally. Their finite matrices need not coincide.

## Falsifiable numeric checks

- Lock P8/P10/PH16 source SHAs and R3/R6 result chain.
- Compare K with best constant-scaled FV operators over full grid and
  boundary-excluded interior, and check weighted self-adjointness.
- Compare actual Green and FV energies on three prescribed C-infinity
  compact, smooth test profiles at nr = 8, 12, 16, 20, same box L=12.
- X trial is an axisymmetric smooth scalar potential; Y trial has an
  extra rho factor enforcing regular A_phi at the symmetry axis.
- Deliberately omit the m=1 rho^-2 term as a negative control.
- Compare K and weighted FV gradients ON THE ACTUAL R3 profiles. These
  remain discrete on-shell source data, unlike the manufactured trials.

A sequence of four decreasing manufactured-profile energy differences
is evidence of limited weak-form compatibility, NOT continuum convergence
of the actual solved source, full spectra, exterior, stress, or gravity.
No source-free exterior Dirichlet-to-Neumann boundary operator is computed.
A physically matched exterior Schur complement remains an open derivation.

## Decision and physical no-promotion

If smooth energy ratios approach unity while the native field gradients
mismatch, record the split explicitly. Do not claim that a better finite-
volume comparison erases the R6 nodal mismatch, or that PH16 is a
Lorentzian Maxwell discretization at a finite lattice size.

The unique Lorentzian action, constrained healthy modes, Einstein metric,
Earth/support/hull variation, physical true stand-off, complete SI energy
strictly below 10 MJ, empirical/UV consistency and net whole-craft force
remain unproven. GAMMA1-01, PH16-05 and PH17 are not authorized.
006D (C=23.591586299249) is unreplaced.
