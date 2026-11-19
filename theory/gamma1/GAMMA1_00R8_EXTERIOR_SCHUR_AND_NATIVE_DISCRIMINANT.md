# GAMMA1-00R8 — Exterior Schur reduction on actual PH16 carrier fields

Scope: **finite outer-box, fixed grid spacing, static Maxwell finite-volume
operators only**. The original 12/L12 PH16 Routhian, native R3 solution,
P8/P10/PH16 source, and R7 evidence remain immutable.

## Derivation, not an unconstrained boundary fit

Construct weighted positive finite-volume Maxwell quadratic forms on a
**larger** cylinder with the SAME cell size h=1, centered on the original
(rho,z)=(0,0) axis/symmetry origin:

    M_X = W_ext * L_ext
    M_Y = W_ext * (L_ext + diag(rho_ext^(-2)))

Partition degrees into original 288 cells I (rho centers .5..11.5;
z centers -11.5..11.5) and surrounding cells E. External fields are
eliminated from the identical positive quadratic action:

    E[u_I,u_E] = (1/2) [u_I,u_E]^T M [u_I,u_E]
    u_E,stationary = - M_EE^(-1) M_EI u_I
    M_eff = M_II - M_IE M_EE^(-1) M_EI

No coupling constant or energy scale is fitted in M_eff. The eliminated
exterior is exactly stationary under this finite *Dirichlet outer-box*
linear action. This is a finite-domain approximate DtN boundary treatment;
it is NOT an exact infinite exterior operator and is not an Einstein field.

Only the original 46-cell outer rim can receive a correction; bulk
rows and columns are unchanged. Eliminating E can only lower the positive
quadratic compared with the fixed interior box Dirichlet energy. Verify
symmetry, positive definiteness, boundary support and null zero-field
controls from the raw matrices.

## Scientific discriminants

Compare the original PH16 ring Green inverse matrices K_X/K_Y with the
unfitted Schur reduced FV matrices on the **actual SHA-locked R3 solution**.
Use fixed h=1 and outer extents 14,18,24,30,36,48,60. Keep both raw
native-gradient and scalar-best-fit diagnostic mismatches in every JSON.
**Never use the best-fit scalars to claim exact same-action equivalence.**

The R7 12/L12 hard-Dirichlet baseline is not overwritten. The Y term
rho^-2 remains compulsory. The residual mismatch after boundary elimination
and any persistent nonzero matrix mismatch are explicit negative results.
All extents change *outer-box size*, NOT continuum mesh spacing or
PH16-source equilibrium. No source is re-solved on larger meshes. Do not
reinterpret a diminishing field residual with growing box as continuum
convergence or source-free exterior transmission.

## Missing physical action

Full off-shell charged-scalar/neutral-fluid/Earth/solid variations, matching
of local static FV boundary energy to original nonlocal ring-Green energy,
full Lorentzian constrained health, source-free exterior convergence,
physical Einstein stress and geometry, Earth-down/whole-craft-up total
reaction, full operating cycle, empirical/quantum/UV, SI normalization and
strictly under 10 MJ complete energy are all NOT CERTIFIED. No finite
1 kg neutral torus at >=1m receiving >=1g has been derived.

There is no automatic GAMMA1-01, PH16-05 or PH17 authorization, and 006D
with C=23.591586299249 remains unreplaced.
