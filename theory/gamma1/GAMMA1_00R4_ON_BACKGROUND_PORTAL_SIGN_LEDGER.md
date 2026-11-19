# GAMMA1-00R4 — Native on-background portal-gradient and boundary audit

This experiment reads the immutable PH16-04R2 replay field arrays produced
by GAMMA1-00R3 (12x24, 288 canonical grid cells). It does NOT rerun the
original PH16 stationary source, solve Einstein equations, or estimate a
whole-craft gravitational force.

Historical R3 fields are a new stationary representative, not the missing
original solution arrays.

## Restricted mathematical observable

The proposed universal physical metric is conformally related by

    gtilde_munu = exp(2 sigma(P)) g_munu
    P = E_X dot B_Y
    sigma(P) = alpha P - beta P^2
    alpha = 0.05
    beta = 40

The leading portal-only contribution to a static neutral test body's
acceleration divided by c^2 is -grad sigma.

Its projection along the radial vector from the model's symmetry center
(rho,z)=(0,0) is

    A_radial = -(rho d_r sigma + z d_z sigma)/sqrt(rho^2+z^2)

This is NOT full gravitational acceleration. The Einstein contribution
is absent. The model's coordinate unit is NOT established as a metre;
a canonical radial shell is not a physical 1m true stand-off or a finite
1kg neutral torus.

The symmetry center is not a derived spacecraft center of mass.

## Independent numerical audit

- Reconstruct E_X and B_Y from the native potentials using the documented
  PH16 second-order central gradients and one-sided edge derivatives.
- Reproduce P and sigma from those fields.
- Verify the saved positive neutral density against the original
  fixed-number hydrostatic formula.
- Count outward and inward radial portal signs on every cell, including
  the core, outer shell, radial bins and boundary-excluded interior.
- Use an independent fourth-order five-point derivative only in the
  deep interior, rather than assuming the primary stencil is sufficient.
- Report nonzero field and source tails at the outer computational box.
- Include exact zero-operator controls for switched-off portal
  coefficients and carriers. These are NOT self-consistent PH16
  source-off or Earth-off re-solves.

A positive portal sign on a sampled shell is a necessary local
directional property. It is not sufficient for a physical gravitational
response, dynamical health, finite material-free stand-off or whole-craft
lift.

## Missing physics

A unique complete Lorentzian action covering all source modes,
neutral fluid, X/Y, Earth, supports, hull, Einstein geometry and
boundaries remains necessary.

All off-shell Ward/Noether/Bianchi identities, constrained Hamiltonian
and characteristic modes, continuum exterior convergence, complete
finite neutral payload force, Earth-down/whole-craft-up reaction, recoil
and radiation, complete SI energy, empirical consistency and quantum/UV
conditions remain OPEN.

GAMMA1-01, PH16-05 and PH17 are NOT automatically authorized.

006D remains the strongest conservative finite-source GR reference,
with C=23.591586299249 and catastrophic positive-energy cost.

The benchmark remains at least 1g throughout a finite 1kg neutral
torus at at least 1m true stand-off for complete operating energy
strictly less than 10MJ. This experiment certifies neither the
benchmark nor a gravitational device.
