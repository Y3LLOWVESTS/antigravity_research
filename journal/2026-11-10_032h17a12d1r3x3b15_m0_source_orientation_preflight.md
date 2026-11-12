# Research Journal — November 10, 2026

## 032H17A12D1R3X3B15-M0 — Full 3D Source-Orientation Preflight

### Scientific question

Can physically rotating the complete R3B electric–magnetic source
relative to a fixed finite neutral torus generate three-dimensional
field responses inaccessible to the axisymmetric solver?

### Preserved reference

- Flagship: 032H17A12D1R3B
- Original preloaded canonical energy: 1.5429162116460216 J
- Payload: finite neutral 1 kg torus
- True external stand-off: 1.0 m
- Required outward acceleration: 9.80665 m/s² everywhere
- Strongest conservative GR anchor: 006D
- 006D coefficient: 23.591586299249

### Mathematical result

Proper SO(3) rotation of the complete source–payload system leaves
physical scalar observables invariant.

Source rotation relative to the fixed toroidal payload introduces
non-axisymmetric multipole components in the physical-metric response.

The existing axisymmetric solver cannot resolve those components.

Rigid rotation cannot rescue the original failure by itself.
Relative source orientation is a genuine new geometric configuration,
but its loaded physical viability is unknown.

### Reproduction

The original R3B source and global mirror equations were executed
from the November 10, 2026 codebundle in an isolated environment.

At h = 0.050 m:

    R3B reconstructed energy = 1.5429162116460409 J

At h = 0.075 m:

    R3B reconstructed energy = 1.4667459954338506 J

These are finite-grid preloaded results. The reproduction reuses
the original research implementation, rather than an independently
derived numerical field solver.

The exterior-only 3D rotation experiment used the fitted R3B
magnetic-scalar multipoles.

### Selected 3D exterior results — h = 0.050 m anchor

Minimum sampled axial acceleration, m/s²:

    Aligned:                  +9.63361
    Full source tilt 30 deg:  +5.71822
    Full source tilt 60 deg:  +2.81375
    Full source tilt 90 deg:  +2.68207
    Full source tilt 135 deg: +3.88603
    Full source tilt 180 deg: +9.63361
    Electric-only tilt 90:   -6.70781
    Two-source opposed:      +0.0915527
    Two-source perpendicular:+1.40718
    Two-source oblique:      +0.371438

These use fixed amplitudes. They are not global optimization
results or a proof that orientations cannot work after renormalization.

The 3D aligned exterior approximation is not identical to the
original axisymmetric R3B magnetic solution and must not replace it.

### Mathematical verification

Six focused tests passed in the isolated environment:

- Proper SO(3) covariance
- Exact source-support clearance
- Joint and one-sector sign identities
- Axisymmetric versus tilted azimuthal response
- Source-free exterior Maxwell identities
- Explicit prohibition of false loaded/device claims

No full-repository regression was performed in this experiment.

### Failure and limitation memory

No loaded three-dimensional matter equations were solved.

No fully coupled 3D energy, stress-energy or source reaction was
certified. No exact source-current microscopic realization was shown.

The 3D exterior result does not independently establish the full
two-U(1) interacting Ward identities or physical-metric action.

The original B13 finite-grid axisymmetric exclusions remain intact.
The original B14 local inward-acceleration anomaly remains unverified.

### B15-M0 decision

ROTATIONAL_COVARIANCE=PASS

RELATIVE_SOURCE_ORIENTATION_GENUINELY_NONAXISYMMETRIC=YES

ORIGINAL_R3B_FIELD_CAPACITY_REPRODUCED=YES

FULLY_LOADED_3D_SOLUTION=NO

LOADED_1G_EVERYWHERE=NOT_ESTABLISHED

MICROSCOPIC_SOURCE=NOT_CERTIFIED

COMPLETE_OPERATING_ENERGY_BELOW_10MJ=NOT_CERTIFIED

006D_REPLACED=NO

B15_CLOSED=NO

### Next experiment

B15-M1: formulate and verify the fully three-dimensional,
same-action reciprocal-loading operator with exact source-current
constraints before performing an expensive loaded 3D solve.

After B15's bounded loaded test, return to B11-M6 physically sourced
dynamical response and finite-payload impulse.

Preserve R3B, B7, the original journals, all scoped exclusions,
and the strict complete-energy ceiling.
