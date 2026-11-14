"""B17-M5B: corrected onboard source and cross-grid inverse transfer.

M5A mistakenly used cylindrical rho alone to construct its net-charge
compensator. This produced an electric source extending throughout the
finite z-domain rather than being confined to the spacecraft.

M5B uses spherical radius sqrt(z*z + rho*rho), tapers both M4B1
current sectors inside an onboard support, and compensates the electric
monopole only in an interior spherical region.

The objective is to test whether M5A's fitted reciprocal directions
survive:
  1. genuine source compactness on the simulation grid;
  2. charge conservation at the level of total discrete net charge;
  3. held-out transfer to a different spatial grid.

A vanishing quadratic reciprocity defect is NOT a Ward identity.
The positive carrier-gradient norm is NOT complete device energy.
No full metric/GR action, physical craft thrust, enclosure
transmission or microscopic source is established.
"""

from __future__ import annotations

import math
import numpy as np

from .hook17_r3b_m4b1_source_recovery import (
    assemble_original_aligned_source,
)
from .hook17_r3b_m4b4_paired_translation import (
    source_support_check,
)
from .hook17_r3b_m4b2_earth_variational_audit import (
    _weights,
)
from .hook17_r3b_m5a_inverse_design import (
    _action_and_norm_matrix,
    _inverse_extremes,
)

BRANCH = "032H17A12D1R3X3B17-M5B"
ENCLOSURE_RADIUS_M = 2.25
COMPACT_SUPPORT_LIMIT_M = 1.82
COMPACT_TAPER_START_M = 1.65
COMPENSATION_LIMIT_M = 1.50


def _spherical_support(
    r,
    inner=COMPACT_TAPER_START_M,
    outer=COMPACT_SUPPORT_LIMIT_M,
):
    """C1 taper with zero support outside a finite onboard sphere."""
    r = np.asarray(r, dtype=float)

    if not (
        0 < inner < outer <= ENCLOSURE_RADIUS_M
    ):
        raise ValueError("Invalid onboard support radii")

    t = np.clip((r-inner)/(outer-inner), 0, 1)

    return 1.0 - t*t*(3 - 2*t)


def compact_shaped_source(base, bias):
    """Apply fore/aft shaping and compact electric charge compensation.

    Positive bias favors negative z (Earth-facing).
    This intentionally changes the M4B1 source geometry: none of
    these compact variants inherits R3B/B7's field-energy result.
    """
    if bias not in (-0.5, 0.0, 0.5):
        raise ValueError("Unregistered source-shaping bias")

    field = base["field"]
    z = field["z_grid"]
    rho = field["rho_grid"]

    re = np.hypot(
        z[1:-1, :-1],
        rho[1:-1, :-1],
    ).reshape(-1)

    ra = np.hypot(
        z[1:-1, 1:-1],
        rho[1:-1, 1:-1],
    ).reshape(-1)

    ze = z[1:-1, :-1].reshape(-1)
    za = z[1:-1, 1:-1].reshape(-1)

    wp, _, _ = _weights(base)

    electric = (
        np.asarray(base["j_phi"], dtype=float)
        * (1.0 - bias * ze/2.0)
        * _spherical_support(re)
    )

    magnetic = (
        np.asarray(base["j_a"], dtype=float)
        * (1.0 - bias * za/2.0)
        * _spherical_support(ra)
    )

    # Charge compensation is LOCAL to the spacecraft.
    compensation = np.zeros_like(re)
    mask = re < COMPENSATION_LIMIT_M

    compensation[mask] = (
        1.0 - (re[mask]/COMPENSATION_LIMIT_M)**2
    )**3

    norm = float(wp @ compensation)

    if norm <= 0:
        raise ArithmeticError(
            "Missing compact electric compensator"
        )

    charge_before = float(wp @ electric)

    electric -= (
        compensation * (charge_before/norm)
    )

    neutrality = (
        abs(float(wp @ electric))
        / max(
            float(wp @ np.abs(electric)),
            1e-200,
        )
    )

    if (
        not np.isfinite(electric).all()
        or not np.isfinite(magnetic).all()
    ):
        raise ArithmeticError(
            "Nonfinite compact source current"
        )

    if neutrality > 1e-10:
        raise ArithmeticError(
            "Electric charge compensation failed"
        )

    max_r = max(
        (
            float(np.max(re[np.abs(electric) > 0]))
            if np.any(electric) else 0.0
        ),
        (
            float(np.max(ra[np.abs(magnetic) > 0]))
            if np.any(magnetic) else 0.0
        ),
    )

    if max_r > COMPACT_SUPPORT_LIMIT_M + 1e-12:
        raise ArithmeticError(
            "Source current escaped onboard support"
        )

    return {
        **base,
        "j_phi": electric,
        "j_a": magnetic,
    }, {
        "net_electric_charge_relative_residual":
            neutrality,
        "max_nonzero_source_radius_m": max_r,
        "compensation_source_max_radius_m":
            float(
                np.max(
                    re[np.abs(compensation) > 0]
                )
            ),
        "compensation_charge_before":
            charge_before,
        "source_tapered_relative_to_original_m4b1":
            True,
        "compensation_uses_spherical_radius":
            True,
    }


def evaluate(
    h=0.25,
    portal_ev=21147.0,
    step_m=2e-4,
    bias=0.0,
):
    """Compute two-current action matrices for a confined surrogate."""
    if (
        h not in (0.2, 0.25)
        or portal_ev != 21147.0
        or not 1e-6 <= step_m <= 2e-3
        or not math.isfinite(step_m)
    ):
        raise ValueError(
            "Only preregistered grid, scale and step permitted"
        )

    base = assemble_original_aligned_source(h)

    source, support = compact_shaped_source(
        base, bias
    )

    plus = source_support_check(
        source, step_m
    )
    minus = source_support_check(
        source, -step_m
    )

    if not (
        plus["inside_enclosure_radius"]
        and minus["inside_enclosure_radius"]
    ):
        raise ArithmeticError(
            "Translated source leaves onboard enclosure"
        )

    weights = _weights(source)

    positions = {
        "center": (0.0, 0.0),
        "earth_plus": (step_m, 0.0),
        "earth_minus": (-step_m, 0.0),
        "craft_plus": (0.0, step_m),
        "craft_minus": (0.0, -step_m),
    }

    matrices = {}
    residual = 0.0

    for name, (ez, cz) in positions.items():
        on, norm, ron = _action_and_norm_matrix(
            source,
            portal_ev,
            ez,
            cz,
            True,
            weights,
        )

        off, _, roff = _action_and_norm_matrix(
            source,
            portal_ev,
            ez,
            cz,
            False,
            weights,
        )

        matrices[name] = {
            "interaction": on - off,
            "norm": norm,
        }

        residual = max(residual, ron, roff)

    qe = (
        matrices["earth_plus"]["interaction"]
        - matrices["earth_minus"]["interaction"]
    ) / (2 * step_m)

    qc = (
        matrices["craft_plus"]["interaction"]
        - matrices["craft_minus"]["interaction"]
    ) / (2 * step_m)

    hn = matrices["center"]["norm"]

    if np.min(np.linalg.eigvalsh(hn)) <= 0:
        raise ArithmeticError(
            "Carrier-gradient norm not positive"
        )

    inverse = _inverse_extremes(
        qe, qc, hn, 9806.65
    )

    controls = {}

    for label, values in (
        ("original_signs", (1.0, 1.0)),
        ("reverse_magnetic", (1.0, -1.0)),
        ("electric_only", (1.0, 0.0)),
        ("magnetic_only", (0.0, 1.0)),
    ):
        x = np.asarray(values)
        earth = float(x @ qe @ x)
        craft = float(x @ qc @ x)

        controls[label] = {
            "earth_slope_j_per_m": earth,
            "craft_slope_j_per_m": craft,
            "defect_j_per_m": earth + craft,
            "normalized_defect":
                abs(earth + craft)
                / max(abs(earth), abs(craft), 1e-12),
            "gradient_norm_j_not_complete_energy":
                float(x @ hn @ x),
        }

    return {
        "branch": BRANCH,
        "h_m": h,
        "portal_ev": portal_ev,
        "step_m": step_m,
        "bias": bias,
        "source_audit": support,
        "source_support_plus": plus,
        "source_support_minus": minus,
        "source_configuration":
            "COMPACT_TAPERED_M4B1_SURROGATE_NOT_B7",
        "matrices": {
            "earth": qe.tolist(),
            "craft": qc.tolist(),
            "defect": (qe + qc).tolist(),
            "norm": hn.tolist(),
        },
        "controls": controls,
        "null_modes": inverse[
            "exact_reciprocal_null_directions"
        ],
        "inverse_source_space": inverse,
        "max_solver_residual": residual,
        "artificial_oracle_physically_realized": False,
        "original_r3b_preloaded_capacity_reference_j":
            1.5429162116460216,
        "source_translation_current_Ward_certified": False,
        "finite_box_artifact_excluded": False,
        "exterior_metric_transmission_derived": False,
        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
        "006d_replaced": False,
    }


def cross_grid_transfer(first, second):
    """Evaluate reciprocal-null mixtures on a held-out grid.

    A source ratio tuned on grid A is transferred to grid B
    without reoptimization. This is a necessary numerical
    robustness test, NOT a full Noether identity.
    """
    if (
        first["bias"] != second["bias"]
        or first["h_m"] == second["h_m"]
        or first["portal_ev"] != second["portal_ev"]
        or first["step_m"] != second["step_m"]
    ):
        raise ValueError(
            "Need matching model controls on two distinct grids"
        )

    rows = []

    for trained, test in (
        (first, second),
        (second, first),
    ):
        qe = np.array(test["matrices"]["earth"])
        qc = np.array(test["matrices"]["craft"])
        hn = np.array(test["matrices"]["norm"])

        for mode in trained["null_modes"]:
            x = np.array(
                mode["source_amplitude_direction"]
            )

            e = float(x @ qe @ x)
            c = float(x @ qc @ x)

            denominator = max(
                abs(e), abs(c), 1e-12
            )

            ratio = (
                float(x[1] / x[0])
                if abs(x[0]) > 1e-15
                else None
            )

            defect = abs(e + c) / denominator

            rows.append({
                "trained_grid_m":
                    trained["h_m"],
                "evaluated_grid_m":
                    test["h_m"],
                "source_magnetic_to_electric_ratio":
                    ratio,
                "trained_earth_slope_per_norm":
                    mode["earth_slope_per_quadratic_norm"],
                "held_out_earth_slope_j_per_m_at_training_amplitude":
                    e,
                "held_out_craft_slope_j_per_m_at_training_amplitude":
                    c,
                "held_out_relative_defect":
                    defect,
                "held_out_gradient_norm_j":
                    float(x @ hn @ x),
                "pass_5pct_held_out_defect":
                    bool(defect < 0.05),
            })

    return {
        "branch": BRANCH,
        "bias": first["bias"],
        "cross_grid_rows": rows,
        "any_held_out_recipient_under_5pct":
            any(
                row["pass_5pct_held_out_defect"]
                for row in rows
            ),
        "all_modes_stable_under_5pct":
            all(
                row["pass_5pct_held_out_defect"]
                for row in rows
            ),
        "test_is_not_full_Noether_identity": True,
        "whole_craft_force_n": None,
    }
