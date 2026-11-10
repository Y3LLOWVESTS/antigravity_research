"""R3X3B6: boundary-corrected baseline electric-source audit.

The R3X3B0 baseline source audit applies a homogeneous-Dirichlet
perturbation operator to a preloaded scalar potential whose finite-box
boundary values are nonzero.

Restore those boundary terms before interpreting the resulting
inverse-source residual as a physical source-support diagnostic.

This does not change the original matter-loading operators or prove
a microscopic, conserved, physically affordable source.
"""
from __future__ import annotations

import math

import numpy as np

from .hook17_concurrent_u1_fieldstrength_metric import (
    SOURCE_RADIUS_M,
)
from .hook17_fdual_f_r3c1_validation import (
    _build_baseline_and_prep,
)
from .hook17_fdual_f_r3x3b0_inverse_loading import (
    support_audit,
)


def correct_baseline_source(k_phi, phi, rhos, h):
    phi = np.asarray(phi, dtype=float)
    rhos = np.asarray(rhos, dtype=float)

    if (
        phi.ndim != 2
        or min(phi.shape) < 4
        or phi.shape[1] != len(rhos)
        or not np.isfinite(phi).all()
        or not math.isfinite(h)
        or h <= 0
    ):
        raise ValueError("Invalid potential or grid")

    if not np.isclose(rhos[1] - rhos[0], h):
        raise ValueError("Unexpected radial grid")

    shape = (phi.shape[0] - 2, phi.shape[1] - 1)

    raw = np.asarray(
        k_phi @ phi[1:-1, :-1].reshape(-1)
    ).reshape(shape)

    corrected = raw.copy()

    # Actual nonzero lower and upper z-boundary potentials.
    corrected[0, :] -= phi[0, :-1] / h**2
    corrected[-1, :] -= phi[-1, :-1] / h**2

    # Actual nonzero outer radial boundary.
    rho = float(rhos[-2])

    corrected[:, -1] -= (
        1.0 / h**2 + 1.0 / (2.0 * rho * h)
    ) * phi[1:-1, -1]

    return raw, corrected


def independent_cylindrical_laplacian(phi, rhos, h):
    """Independent -Laplacian with actual full boundary values."""
    phi = np.asarray(phi, dtype=float)
    rhos = np.asarray(rhos, dtype=float)

    if (
        phi.ndim != 2
        or phi.shape[1] != len(rhos)
        or min(phi.shape) < 4
    ):
        raise ValueError("Invalid independent stencil input")

    out = -(
        phi[2:, :-1]
        - 2.0 * phi[1:-1, :-1]
        + phi[:-2, :-1]
    ) / h**2

    # Regular cylindrical axis, rho=0.
    out[:, 0] += (
        4.0
        * (phi[1:-1, 0] - phi[1:-1, 1])
        / h**2
    )

    rho = rhos[1:-1][None, :]

    out[:, 1:] -= (
        (
            phi[1:-1, 2:]
            - 2.0 * phi[1:-1, 1:-1]
            + phi[1:-1, :-2]
        ) / h**2
        + (
            phi[1:-1, 2:] - phi[1:-1, :-2]
        ) / (2.0 * rho * h)
    )

    return out


def norm_fraction(values, outside, weights=None):
    values = np.asarray(values, dtype=float)
    outside = np.asarray(outside, dtype=bool)

    if values.shape != outside.shape:
        raise ValueError("Residual/mask shape mismatch")

    if weights is None:
        weights = np.ones_like(values)
    else:
        weights = np.broadcast_to(weights, values.shape)

    denominator = float(np.sum(weights * values**2))

    if denominator <= 0:
        return 0.0

    return float(
        np.sqrt(
            np.sum(weights[outside] * values[outside]**2)
            / denominator
        )
    )


def audit_grid(h):
    setup = _build_baseline_and_prep(h)

    field = setup["field"]
    prep = setup["prep"]
    phi = setup["phi0"]

    h = float(field["h"])
    rhos = np.asarray(field["rhos"], dtype=float)

    raw, corrected = correct_baseline_source(
        prep["operators"]["k_phi"],
        phi,
        rhos,
        h,
    )

    independent = independent_cylindrical_laplacian(
        phi, rhos, h
    )

    discrepancy = float(
        np.linalg.norm(corrected - independent)
        / max(np.linalg.norm(independent), 1e-300)
    )

    if discrepancy > 1e-11:
        raise RuntimeError(
            "Independent cylindrical stencil disagreement"
        )

    radius = np.hypot(
        field["rho_grid"],
        field["z_grid"],
    )[1:-1, :-1]

    outside = radius > (
        float(SOURCE_RADIUS_M) + 2.0 * h
    )

    # Cylindrical cell-volume proxy weights.
    # The resulting norm is NOT physical charge.
    ring_weights = 2.0 * math.pi * rhos[:-1] * h**2
    ring_weights[0] = math.pi * (h / 2.0)**2 * h

    raw_fraction = norm_fraction(raw, outside)
    corrected_fraction = norm_fraction(corrected, outside)

    old_audit = support_audit(setup)

    channels = {
        c["channel"]: c
        for c in old_audit["channels"]
    }

    electric = channels["electric_static_charge"]
    magnetic = channels["azimuthal_magnetic_source_current"]

    if not math.isclose(
        raw_fraction,
        electric[
            "baseline_current_l2_fraction_outside_buffered_source"
        ],
        rel_tol=1e-10,
    ):
        raise RuntimeError("Historical baseline mismatch")

    return {
        "h_m": h,
        "old_baseline_outside_l2_fraction": raw_fraction,
        "boundary_corrected_outside_l2_fraction":
            corrected_fraction,
        "corrected_cylindrical_weighted_outside_l2_fraction":
            norm_fraction(
                corrected,
                outside,
                ring_weights[None, :],
            ),
        "independent_stencil_relative_error":
            discrepancy,
        "required_electric_interface_rhs_outside_fraction":
            electric[
                "residual_l2_fraction_outside_buffered_support"
            ],
        "required_magnetic_interface_rhs_outside_fraction":
            magnetic[
                "residual_l2_fraction_outside_buffered_support"
            ],
        "electric_interface_rhs_payload_fraction":
            electric[
                "residual_l2_fraction_on_payload_nodes"
            ],
        "magnetic_interface_rhs_payload_fraction":
            magnetic[
                "residual_l2_fraction_on_payload_nodes"
            ],
        "microscopic_source_certified": False,
        "continuum_certified": False,
    }
