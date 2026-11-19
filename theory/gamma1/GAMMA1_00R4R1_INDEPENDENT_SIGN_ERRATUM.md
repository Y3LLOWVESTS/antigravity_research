# GAMMA1-00R4R1 — Independent fourth-order sign erratum

The original GAMMA1-00R4 scientific JSON reported success, but its
independent verifier FAILED before full regression or final manifest.
That failure remains a historical fact and must not be overwritten.

The original independent verifier already computed:

    pr4 = -d_r(sigma)
    pz4 = -d_z(sigma)

It then incorrectly applied a second negation:

    projected4 = (-R4*pr4-Z4*pz4)/rr

The correct radial projection is:

    projected4 = (R4*pr4+Z4*pz4)/rr

This is a verification-code sign correction, NOT a change to physical
equations, solver data, source parameters, or acceptance thresholds.

The original failed verifier is retained byte-for-byte. Its source
SHA is checked against the original R4 producing-source manifest.

Independent reproduction from the SHA-locked R3 native profile:

- Second-order whole mesh: 248 outward, 40 inward
- Second-order canonical radius >=6: 232 outward, 0 inward
- Fourth-order deep interior radius >=6: 128 outward, 0 inward
- Erroneous original verifier result: 0 outward, 128 inward
- Correct fourth-order minimum: 3.837520985651595e-08
- Correct fourth-order maximum: 2.468153612866706e-06

These values are in canonical model units, NOT SI acceleration.

The computational box is not a proven source-free exterior.
Its boundary retains nonzero source amplitudes.

No Einstein metric was solved. Full Lorentzian stability,
whole-craft lift, Earth reaction, continuum/exterior convergence,
and complete energy remain open.

R4R1 is an append-only verification erratum, not a new physics model.

006D remains unreplaced. GAMMA1-01 remains unauthorized.
