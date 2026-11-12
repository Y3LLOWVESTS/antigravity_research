# 032H17A12D1R3X3B15-M2C — Angular Interface Routing

Date: 2026-11-10

## Objective

Test whether changing the incidence angle of the original
1.5429162116460216 J R3B field can suppress destructive
finite-payload interface loading while retaining its
topological physical-metric response.

## Exact result

For the frozen static two-U(1) configuration:

    j_phi = grad(theta).B
    j_A = grad(theta) x E

At nonzero grad(theta), exact cancellation of both terms
implies E.B=0.

In the fitted R3B exterior mirror E=B, giving:

    j_phi^2+|j_A|^2=|grad(theta)|^2|E|^2

This combined leading current demand is independent of
local incidence angle at fixed field magnitude.

## Local field-energy tradeoff

Defining I=E.B, S=E^2+B^2 and
q^2=B_normal^2+|E_tangent|^2:

    I^2 <= q^2*(S-q^2)

At fixed nonzero I, reductions in current amplitude
require a minimum local field-energy premium:

    Current factor 0.50: energy >=2.125x
    Current factor 0.25: energy >=8.03125x
    Current factor 0.10: energy >=50.005x

These bounds do not establish physically achievable
field configurations or complete operating energy.

## Numerical experiment

Actual original R3B fitted multipoles, canonical
two-sector normalization and 1 kg torus were used.

B15-M0 source-support geometries and B15-M2A
equal-preloaded-1g normalizations were preserved.

Grids:

    0.075 m
    0.050 m
    0.040 m

Results:

- All tested joint-axis rotations increased the
  combined interface-current projector relative
  to the aligned control.
- The angular projector reproduced the previous
  discrete M2A current-demand norms through an
  independent reconstruction.
- Finite-difference product-rule errors decreased
  with grid refinement.
- Exact interface inequalities and local equal-field
  identities passed numerically.
- The sector-only perpendicular case has inward
  acceleration and is not an eligible positive-1g
  equal-normalization candidate.

## Crucial physical distinction

The mixed E_X x B_Y quantity is not the kinetic
same-sector Poynting flux.

The original static two-sector construction has no
propagating energy flow that can simply be curved
around a 90-degree bend to divert reaction momentum.

Dynamical guided-wave momentum routing remains a
distinct, untested physical hypothesis.

## Scientific decision

STATIC_EQUAL_FIELD_ANGLE_ONLY_RESCUE:
NOT_FOUND_IN_TESTED_GEOMETRIES

LOCAL_EQUAL_FIELD_INTERFACE_IDENTITY:
ESTABLISHED

UNEQUAL_FIELD_POLARIZATION_AND_ENERGY_TRADEOFF:
MATHEMATICALLY_OPEN

TRUE_DYNAMIC_MOMENTUM_ROUTING:
NOT_TESTED

FULLY_LOADED_3D_FORCE:
NOT_ESTABLISHED

MICROSCOPIC_SOURCES:
NOT_CERTIFIED

COMPLETE_OPERATING_ENERGY_BELOW_10MJ:
NOT_CERTIFIED

006D_REPLACED:
NO

## Next priority

Investigate healthy, causally sourced dynamical modes
capable of changing the electric/magnetic response and
routing actual field momentum.

Do not infer a one-way force or reaction-free source.

Preserve R3B's original 1.5429162116460216 J
preloaded result and all historical loaded exclusions.
