"""B17-M5C: exact-cell common-translation covariance preflight.

Reuse the M5B compact, net-neutral source and original R3X1
Lorentzian carrier operators without changing their equations.

Translate Earth, onboard source, and vacuum enclosure together
by precisely one z-grid cell in either direction. In an isolated,
translation-invariant continuum theory, the interaction action
cannot depend on such a common displacement.

The existing finite computational domain may violate this
condition. The Earth-free control helps separate source/box
dependence from the finite-Earth material response.

The full quadratic reciprocity operator must vanish for every
source combination. A tuned null direction is NOT a proof of
a Ward/Noether identity.

This source transport is a static nodal construction, not a
continuity-certified moving physical current. No GR source,
exterior metric transmission, complete material stress,
spacecraft force or device energy is certified.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from .hook17_r3b_m4b1_source_recovery import (
    assemble_original_aligned_source,
)
from .hook17_r3b_m4b2_earth_variational_audit import (
    _weights,
)
from .hook17_r3b_m4b4_paired_translation import (
    shifted_material,
    shifted_source,
    source_support_check,
)
from .hook17_r3b_m5a_inverse_design import (
    _action_and_norm_matrix,
)
from .hook17_r3b_m5b_compact_transfer import (
    compact_shaped_source,
)

BRANCH = "032H17A12D1R3X3B17-M5C"


def _quadratic(x, matrix):
    return float(x @ matrix @ x)


def _full_cell_source_transport(source, h):
    """Measure exact one-cell current translation and charge."""

    wp, _, _ = _weights(source)

    field = source["field"]
    nz = len(field["zs"]) - 2

    results = {}

    for sign in (-1, 1):
        moved = shifted_source(
            source, 1000.0, sign*h
        )

        errors = []

        for name, cols in (
            ("j_phi", len(field["rhos"])-1),
            ("j_a", len(field["rhos"])-2),
        ):
            original = np.asarray(
                source[name], dtype=float
            ).reshape(nz, cols)

            actual = np.asarray(
                moved[name], dtype=float
            ).reshape(nz, cols)

            expected = np.zeros_like(original)

            if sign > 0:
                expected[1:, :] = original[:-1, :]
            else:
                expected[:-1, :] = original[1:, :]

            errors.append(float(
                np.linalg.norm(actual-expected)
                / max(
                    np.linalg.norm(original),
                    1e-200,
                )
            ))

        charge = np.asarray(
            moved["j_phi"], dtype=float
        )

        neutrality = (
            abs(float(wp @ charge))
            / max(
                float(wp @ abs(charge)),
                1e-200,
            )
        )

        results[
            "plus" if sign > 0 else "minus"
        ] = {
            "current_shift_relative_l2_errors":
                errors,
            "translated_electric_neutrality":
                neutrality,
            "support": source_support_check(
                source, sign*h
            ),
        }

    return results


def _material_transport_error(
    source, h, portal_ev, earth_present
):
    """Verify exact-cell interior translation of beta."""

    def beta(z):
        return shifted_material(
            source,
            z,
            z,
            portal_ev,
            earth_present=earth_present,
        )[0]

    center = beta(0.0)
    plus = beta(h)
    minus = beta(-h)

    denominator = max(
        float(np.max(abs(center))),
        1.0,
    )

    return {
        "plus_inner_relative_linf": float(
            np.max(abs(
                plus[1:, :] - center[:-1, :]
            )) / denominator
        ),
        "minus_inner_relative_linf": float(
            np.max(abs(
                minus[:-1, :] - center[1:, :]
            )) / denominator
        ),
    }


def _snapshot(
    source, weights, portal_ev, displacement
):
    """Re-solve three source bases in both material settings."""

    on, _, ron = _action_and_norm_matrix(
        source,
        portal_ev,
        displacement,
        displacement,
        True,
        weights,
    )

    off, _, roff = _action_and_norm_matrix(
        source,
        portal_ev,
        displacement,
        displacement,
        False,
        weights,
    )

    return {
        "earth_present": on,
        "earth_absent": off,
        "difference": on-off,
        "max_residual": max(
            float(ron), float(roff)
        ),
    }


def _normalized_defect_eigenvalues(defect, norm):
    """Source-family operator test, not one tuned null ray."""

    eigenvalues, vectors = np.linalg.eigh(norm)

    if np.min(eigenvalues) <= 0:
        raise ArithmeticError(
            "Non-positive carrier-gradient norm"
        )

    invroot = (
        vectors * eigenvalues**(-0.5)
    ) @ vectors.T

    return np.linalg.eigvalsh(
        invroot @ defect @ invroot
    )


def _load_reference(path, h, bias, portal_ev):
    if path is None:
        return None

    saved = json.loads(
        Path(path).read_text(
            encoding="utf-8"
        )
    )

    if saved.get("branch") != (
        "032H17A12D1R3X3B17-M5B"
    ):
        raise ValueError("Expected M5B result JSON")

    if abs(
        float(saved["shape_bias"])-bias
    ) > 1e-12:
        raise ValueError("Reference bias mismatch")

    key = "0.25" if h == 0.25 else "0.2"
    row = saved["grids"][key]

    if (
        abs(float(row["h_m"])-h) > 1e-12
        or abs(
            float(row["portal_ev"])-portal_ev
        ) > 1e-9
    ):
        raise ValueError(
            "Reference grid or portal mismatch"
        )

    return row


def evaluate(
    h=0.25,
    bias=0.0,
    portal_ev=21147.0,
    reference=None,
):
    """Exact one-cell simultaneous translation and box audit."""

    if (
        h not in (0.25, 0.2)
        or bias not in (-0.5, 0.0, 0.5)
        or portal_ev != 21147.0
        or not all(
            math.isfinite(v)
            for v in (h, bias, portal_ev)
        )
    ):
        raise ValueError(
            "Unregistered preflight parameters"
        )

    base = assemble_original_aligned_source(
        float(h)
    )

    source, support = compact_shaped_source(
        base, bias
    )

    transport = _full_cell_source_transport(
        source, h
    )

    for direction in transport.values():
        if not direction["support"][
            "inside_enclosure_radius"
        ]:
            raise ArithmeticError(
                "Translated current escaped enclosure"
            )

    weights = _weights(source)

    center = _snapshot(
        source, weights, portal_ev, 0.0
    )

    plus = _snapshot(
        source, weights, portal_ev, h
    )

    minus = _snapshot(
        source, weights, portal_ev, -h
    )

    slopes = {
        name: (
            plus[name]-minus[name]
        )/(2*h)
        for name in (
            "earth_present",
            "earth_absent",
            "difference",
        )
    }

    np.testing.assert_allclose(
        slopes["difference"],
        slopes["earth_present"]
        - slopes["earth_absent"],
        rtol=1e-10,
        atol=1e-6,
    )

    controls = {}

    for name, values in (
        ("both_positive", (1.0, 1.0)),
        ("magnetic_reversed", (1.0, -1.0)),
        ("electric_only", (1.0, 0.0)),
        ("magnetic_only", (0.0, 1.0)),
    ):
        x = np.asarray(values, dtype=float)

        on = _quadratic(
            x, slopes["earth_present"]
        )
        off = _quadratic(
            x, slopes["earth_absent"]
        )

        controls[name] = {
            "common_shift_earth_present_slope_j_per_m":
                on,
            "common_shift_earth_free_slope_j_per_m":
                off,
            "common_shift_interaction_slope_j_per_m":
                on-off,
            "center_interaction_action_j":
                _quadratic(
                    x, center["difference"]
                ),
            "plus_interaction_action_j":
                _quadratic(
                    x, plus["difference"]
                ),
            "minus_interaction_action_j":
                _quadratic(
                    x, minus["difference"]
                ),
        }

    comparison = None
    previous = _load_reference(
        reference, h, bias, portal_ev
    )

    if previous is not None:
        old = np.asarray(
            previous["matrices"]["defect"],
            dtype=float,
        )

        norm = np.asarray(
            previous["matrices"]["norm"],
            dtype=float,
        )

        current = slopes["difference"]

        comparison = {
            "m5b_subcell_paired_defect_matrix_j_per_m":
                old.tolist(),
            "full_cell_common_slope_matrix_j_per_m":
                current.tolist(),
            "relative_frobenius_difference": float(
                np.linalg.norm(current-old)
                / max(
                    np.linalg.norm(old),
                    1e-200,
                )
            ),
            "m5b_whitened_defect_eigenvalues_per_norm":
                _normalized_defect_eigenvalues(
                    old, norm
                ).tolist(),
            "m5b_defect_matrix_zero_operator":
                False,
            "source_ratio_cancellation_is_noether_proof":
                False,
            "comparison_uses_different_displacement_steps":
                True,
        }

    return {
        "branch": BRANCH,
        "scope":
            "EXACT_ONE_CELL_COMMON_TRANSLATION_NOT_CRAFT_FORCE",
        "h_m": h,
        "shape_bias": bias,
        "portal_ev": portal_ev,
        "common_shift_distance_m": h,
        "source_audit": support,
        "current_transport": transport,
        "earth_present_material_transport":
            _material_transport_error(
                source, h, portal_ev, True
            ),
        "earth_absent_material_transport":
            _material_transport_error(
                source, h, portal_ev, False
            ),
        "common_mode_action_matrices_j_per_m": {
            name: matrix.tolist()
            for name, matrix in slopes.items()
        },
        "common_mode_controls": controls,
        "reference_comparison": comparison,
        "max_coupled_solver_residual": max(
            center["max_residual"],
            plus["max_residual"],
            minus["max_residual"],
        ),
        "exact_one_cell_nodal_shift": True,
        "fixed_outer_boundary_present": True,
        "finite_box_artifact_excluded": False,
        "moving_current_ward_identity_certified":
            False,
        "complete_gravity_metric_matter_action":
            False,
        "exterior_metric_transmission_derived":
            False,
        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
        "006d_replaced": False,
        "warning":
            "Finite-domain action drift, not physical spacecraft force",
    }
