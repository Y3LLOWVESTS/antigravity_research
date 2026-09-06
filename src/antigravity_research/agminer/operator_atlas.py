"""
Local metric-active operator diagnostics for AGMINER.

The purpose is not to generate arbitrary theories.

The atlas classifies explicit operator structures already represented
in scalar-tensor, disformal/DHOST, GR, vector, p-form, torsion and
topological theory classes.

The central new distinction is between:

  pure static disformal:
      g_phys = g + D(X) dphi dphi

which has no static g00 response when d0phi=0, and

  kinetic conformal:
      g_phys = C(X) g + D(X) dphi dphi

which DOES modify g00 for a static spatial scalar gradient.

Exact shift symmetry is compatible with C=C(X), D=D(X).
"""

from __future__ import annotations

from dataclasses import dataclass


C_LIGHT = 299792458.0


@dataclass(frozen=True)
class OperatorRecord:
    operator_id: str
    local_covariant: bool
    one_physical_metric: bool
    static_g00_response: bool
    external_standoff_structurally_possible: bool
    symmetry_protection_available: bool
    separate_propagating_charge_mediator_required: bool
    project_closed: bool

    @property
    def structural_open_score(self) -> int:
        return sum((
            int(self.local_covariant),
            int(self.one_physical_metric),
            int(self.static_g00_response),
            int(self.external_standoff_structurally_possible),
            int(self.symmetry_protection_available),
            int(not self.separate_propagating_charge_mediator_required),
            int(not self.project_closed),
        ))


def canonical_derivative_metric_coefficient(
    raw_kappa: float,
    kinetic_z: float,
) -> float:
    """Return the coefficient after canonical scalar normalization.

    Starting from

        -Z/2 (dphi)^2

    and a metric operator proportional to

        kappa (dphi)^2,

    the canonically normalized physical coefficient is kappa/Z.
    """
    kappa = float(raw_kappa)
    z = float(kinetic_z)

    if z <= 0.0:
        raise ValueError("kinetic_z must be positive")

    return kappa/z


def static_pure_disformal_g00_shift(
    dphi_dt: float,
    disformal_coefficient: float,
) -> float:
    """Return D (d0 phi)^2 contribution to physical g00."""
    return (
        float(disformal_coefficient)
        * float(dphi_dt)**2
    )


def static_kinetic_conformal_acceleration(
    dlnc_dy: float,
    dy_dr_per_m: float,
) -> float:
    """Weak-field radial acceleration from C(Y)g.

    Y is any declared positive dimensionless kinetic invariant.

      a_r = -(c^2/2) d_r ln C
          = -(c^2/2) (d ln C/dY) (dY/dr).
    """
    return (
        -0.5
        * C_LIGHT**2
        * float(dlnc_dy)
        * float(dy_dr_per_m)
    )


def kinetic_conformal_outward_for_localized_gradient(
    dlnc_dy: float,
) -> bool:
    """Assume Y decreases with outward radius: dY/dr < 0."""
    return static_kinetic_conformal_acceleration(
        dlnc_dy,
        -1.0,
    ) > 0.0


def operator_prefield_open(record: OperatorRecord) -> bool:
    return (
        record.local_covariant
        and record.one_physical_metric
        and record.static_g00_response
        and record.external_standoff_structurally_possible
        and record.symmetry_protection_available
        and not record.separate_propagating_charge_mediator_required
        and not record.project_closed
    )
