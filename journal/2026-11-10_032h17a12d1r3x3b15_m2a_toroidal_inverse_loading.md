# Research Journal — November 10, 2026

## B15-M2A — Three-Dimensional Toroidal Inverse-Loading Preflight

### Objective

Test whether physically rotating the original R3B exterior
electric-magnetic source relative to the finite neutral payload
reduces the reciprocal interface-source compensation required
to preserve the preloaded field.

### Previous gates

B15-M0:
- 6 focused tests passed on the local Mac.
- R3B original 0.050 m energy reproduced exactly as recorded.
- Proper rotational covariance established.
- New non-axisymmetric source orientations demonstrated.

B15-M1:
- 5 focused tests passed on the local Mac.
- n=5,7,9 discrete Lorentzian action identities passed.
- Independent U(1) gauge and reciprocity tests passed.
- No fully loaded field solution was established.

### Physical density profile

The original OPTIMISTIC_FLAT_C1 profile is used.

Payload:
- 1 kg neutral torus
- Major radius: 1.0 m
- Minor radius: 0.2 m
- True external source-to-payload gap: >=1 m

Leading physical material-loading coefficient:

    theta = -beta = 2 rho c² / M⁴

with the energy density converted to the original eV^4
convention and M = 1000 eV.

### Incremental source-current equations

For the frozen static Lorentzian topological action:

    delta_j_phi = div(theta B_Y)
    delta_j_A   = curl(theta E_X)

These are incremental Euler-Lagrange terms associated with
preserving prescribed preloaded fields, not actual constructed
microscopic currents.

The finite computational box contains the payload but no
source material. The theta-weighted field products vanish
on the padded-box boundaries.

This deliberately avoids the old finite-box source-audit
artifact repaired by R3X3B6.

### Independent calculation

Five focused tests passed in the isolated environment.

R3B source amplitudes were independently reconstructed
from the original codebundle's field modules.

Numerically integrated payload mass:

    h=0.075 m: 0.9988186895488075 kg
    h=0.050 m: 1.0023630128081136 kg
    h=0.040 m: 1.0001368678888616 kg

Leading theta peak:

    18987.283771593688

Incremental current conservation residuals were near
floating-point precision.

### Relative inverse-loading current demand

Each eligible source geometry is normalized to the same
sampled PRELOADED 1g floor.

Ratios relative to the aligned R3B exterior construction:

Configuration            h=0.075      h=0.050      h=0.040
----------------------------------------------------------------
Aligned                  1.000000     1.000000     1.000000
30-degree tilt           1.180752     1.180757     1.180759
60-degree tilt           1.285991     1.286022     1.286033
90-degree tilt           1.056778     1.056831     1.056850
Perpendicular pair       1.401929     1.401907     1.401904

The electric-sector-only perpendicular source has
negative local preloaded axial acceleration and cannot
be normalized to the positive everywhere-1g criterion
by positive common amplitude rescaling.

### Numerical precision caution

The relative inverse-loading demand is stable across
the three checked grids.

The absolute aligned inverse-loading norm changes:

    h=0.075 m: approximately 4.0952e9
    h=0.050 m: approximately 4.7445e9
    h=0.040 m: approximately 4.9876e9

in the reduced model's unnormalized Euler-Lagrange units.

Absolute continuum convergence has NOT been established.

No physical source-energy inference should be made from
these current-demand units.

### Scientific finding

The tested relative source orientations do not reduce
the frozen-preloaded inverse-loading current norm
relative to aligned R3B at equal sampled preloaded 1g.

This is scoped negative evidence against a simple
orientation-only preservation of the original fields.

It is NOT an exclusion of changed self-consistent loaded
solutions or untested physical 3D source families.

### Claim boundaries

The calculation has NOT demonstrated:

- Physical microscopic source currents.
- Complete matter-source same-action dynamics.
- Fully loaded three-dimensional fields.
- A converged whole-payload outward force.
- Source reaction or whole-craft lift.
- Pulsed finite-payload impulse.
- Healthy dynamic modes or stability.
- Complete energy strictly below 10 MJ.
- A new physical antigravity mechanism.

### Decision

B15-M2A:
SCOPED_INVERSE_LOADING_ORIENTATION_PREFLIGHT_COMPLETE

ORIENTATION_ONLY_FROZEN_FIELD_COMPENSATION_IMPROVEMENT:
NO_IN_TESTED_SET

ABSOLUTE_CURRENT_CONTINUUM_CONVERGENCE:
NOT_CERTIFIED

FULLY_LOADED_3D_SOLUTION:
NO

B15_CLOSED:
NO

006D_REPLACED:
NO

### Next research

B15-M2B must construct the boundary-compatible 3D
same-action loaded solver and recover the historical
aligned R3X1/B0 loaded failure before interpreting
any rotated loaded force.

Retain the 1 kg payload and >=1 m source-to-payload gap.

If that gate passes, test a bounded set of genuinely
non-axisymmetric configurations with full reciprocal loading.

Return to B11-M6 physically sourced dynamical response
after B15's decisive loaded-field investigation.

### Permanent numerical references

R3B original preloaded capacity:
1.5429162116460216 J

B7 10 cm charge-layer preloaded capacity:
1.5473042949759672 J

006D conservative linearized-GR coefficient:
23.591586299249

No complete physical antigravity model or certified
sub-10-MJ device exists.
