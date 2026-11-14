"""ALPHA-1R7/B17-M5L: fixed-loading weighted variational audit.

SCIENTIFIC QUESTION
-------------------
Does the M5I/M5K matched current couple to the corrected R3B
carrier through one quadratic stationary functional at fixed
material loading?

MATHEMATICAL MODEL
------------------
Let u=(phi,a) and j=(j_phi,j_a).

    A u = j
    A = [[K_phi, C], [-D, K_a]]
    W = diag(W_phi,-W_a)
    H = W A

If H is symmetric, construct

    Q(u;j) = 0.5*u.T@H@u - u.T@W@j

Its Euler-Lagrange equation is H u = W j. On shell,

    Q_star = -0.5*u.T@W@j

The minus sign in the vector-sector weight is essential to
the tested Lorentzian cross-coupling convention.

INTERPRETATION
--------------
Q is in native solver units, NOT joules. Constructing Q does
not demonstrate a complete physical source action or the
same-action coupling of source, matter, carrier, metric and
gravity. No derivative of Q is certified as spacecraft force.

VALIDATION
----------
Full matrix self-adjointness, exact variational residual,
on-shell source-conjugacy identity, negative sign controls,
and reproduction of M5K carrier energies.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.sparse import bmat, diags


BRANCH = "032H17A12D1R3X3B17-ALPHA1R7-M5L"


def maxabs(matrix):
    """Return the largest stored sparse-entry magnitude."""
    if matrix.nnz == 0:
        return 0.0
    return float(np.max(np.abs(matrix.data)))


def assemble_variational_matrix(
    ops, coupling, rhos, h
):
    """Reconstruct the live operator and its signed pairing."""
    if not np.isfinite(h) or h <= 0:
        raise ValueError("Invalid grid spacing")

    nz = int(ops["nz_inner"])

    scalar_r = np.asarray(
        rhos[:-1], dtype=float
    ).copy()

    scalar_r[0] = h / 8.0

    vector_r = np.asarray(
        rhos[1:-1], dtype=float
    )

    wp = np.tile(scalar_r, nz)
    wa = np.tile(vector_r, nz)

    A = bmat(
        [
            [ops["k_phi"], coupling["c"]],
            [-coupling["d"], ops["k_a"]],
        ],
        format="csr",
    )

    weights = np.r_[wp, -wa]

    if (
        A.shape != (
            len(weights), len(weights)
        )
        or not np.all(weights != 0)
    ):
        raise ArithmeticError(
            "Operator-weight layout mismatch"
        )

    H = (
        diags(weights, format="csr") @ A
    ).tocsr()

    antisymmetric = (H - H.T).tocsr()

    relative_asymmetry = (
        maxabs(antisymmetric)
        / max(maxabs(H), 1e-300)
    )

    return A, H, weights, relative_asymmetry


def on_shell_quadratic(u, source, H, weights):
    """Audit stationarity and the source-conjugacy identity."""
    u = np.asarray(u, dtype=float)
    source = np.asarray(source, dtype=float)
    weights = np.asarray(weights, dtype=float)

    if (
        u.shape != source.shape
        or source.shape != weights.shape
    ):
        raise ValueError(
            "Invalid quadratic source pairing"
        )

    if not (
        np.isfinite(u).all()
        and np.isfinite(source).all()
    ):
        raise ArithmeticError(
            "Nonfinite source or carrier field"
        )

    linear = float(
        np.dot(u, weights * source)
    )

    quadratic = 0.5 * float(
        np.dot(u, H @ u)
    )

    Q = quadratic - linear

    gradient = (
        0.5 * (H @ u + H.T @ u)
        - weights * source
    )

    variation_residual = float(
        np.linalg.norm(gradient)
        / max(
            np.linalg.norm(weights * source),
            1.0,
        )
    )

    identity_defect = (
        abs(Q + 0.5 * linear)
        / max(
            abs(Q), abs(linear), 1.0
        )
    )

    return {
        "native_quadratic_functional": Q,
        "native_source_conjugacy": linear,
        "native_on_shell_half_source_conjugacy":
            -0.5 * linear,
        "relative_action_variation_residual":
            variation_residual,
        "relative_on_shell_identity_defect":
            identity_defect,
    }


def evaluate_case(h, reverse, historical):
    """Audit the same source and solution used in M5K."""
    from .hook17_r3b_m4b1_source_recovery import (
        assemble_original_aligned_source,
    )

    from .hook17_r3b_m5i_continuum_source import (
        SourceSpec,
    )

    from .hook17_r3b_m5k_matched_coupling import (
        build_matched_source,
    )

    from .hook17_r3b_m4b4_paired_translation import (
        shifted_material,
    )

    from .hook17_r3b_m4b_sparse_earth_loading import (
        _solve_fixed_sources,
    )

    if historical.get("branch") != (
        "032H17A12D1R3X3B17-ALPHA1R6-M5K"
    ):
        raise ValueError("Incorrect M5K reference")

    if (
        historical["grid_m"] != h
        or historical["reversed_magnetic"] != reverse
        or not all(
            historical["diagnostic_gates"].values()
        )
    ):
        raise ValueError(
            "Historical M5K control mismatch"
        )

    if h not in (0.2, 0.25):
        raise ValueError("Unregistered grid")

    scale_ev = float(
        historical["coupled_response"][
            "portal_scale_ev"
        ]
    )

    amplitude = float(
        historical["source_audit"][
            "native_rhs_amplitude"
        ]
    )

    if scale_ev != 21147.0 or amplitude != 1e6:
        raise ValueError(
            "Historical source normalization changed"
        )

    spec = SourceSpec(
        azimuthal_current_amplitude=(
            -1.0 if reverse else 1.0
        )
    )

    base = assemble_original_aligned_source(h)

    source, audit = build_matched_source(
        base,
        spec,
        order=6,
        amplitude=amplitude,
    )

    amplifier = (
        scale_ev / 1000.0
    ) ** 2

    active = {
        **source,
        "j_phi":
            amplifier * source["j_phi"],
        "j_a":
            amplifier * source["j_a"],
    }

    results = {}

    for label, earth_present, fraction in (
        ("unloaded", False, 0.0),
        ("earth_loaded", True, 1.0),
        ("earth_free_air_loaded", False, 1.0),
    ):
        beta, _, _ = shifted_material(
            source,
            0.0,
            0.0,
            scale_ev,
            earth_present=earth_present,
        )

        state = _solve_fixed_sources(
            active,
            beta,
            fraction=fraction,
        )

        coupling = state["coupling"]

        if fraction == 0.0:
            coupling = {
                "c": 0 * coupling["c"],
                "d": 0 * coupling["d"],
            }

        A, H, weights, symmetry_defect = (
            assemble_variational_matrix(
                source["operators"],
                coupling,
                source["field"]["rhos"],
                h,
            )
        )

        phi = state["phi"][
            1:-1, :-1
        ].ravel()

        a = state["a"][
            1:-1, 1:-1
        ].ravel()

        u = np.r_[phi, a]

        j = np.r_[
            active["j_phi"],
            active["j_a"],
        ]

        row = on_shell_quadratic(
            u, j, H, weights
        )

        row[
            "relative_weighted_matrix_asymmetry"
        ] = symmetry_defect

        row[
            "relative_source_equation_residual"
        ] = float(
            np.linalg.norm(A @ u - j)
            / max(np.linalg.norm(j), 1.0)
        )

        row["carrier_field_energy_j"] = float(
            state["carrier_energy_j"]
        )

        expected = float(
            historical["coupled_response"][
                "solves"
            ][label]["carrier_field_energy_j"]
        )

        row[
            "carrier_energy_reference_difference_j"
        ] = abs(
            row["carrier_field_energy_j"]
            - expected
        )

        row["matrix_dimension"] = A.shape[0]
        row["full_coupling_fraction"] = fraction

        results[label] = row

    max_asymmetry = max(
        row["relative_weighted_matrix_asymmetry"]
        for row in results.values()
    )

    max_variation = max(
        row["relative_action_variation_residual"]
        for row in results.values()
    )

    max_identity = max(
        row["relative_on_shell_identity_defect"]
        for row in results.values()
    )

    max_energy_error = max(
        row["carrier_energy_reference_difference_j"]
        for row in results.values()
    )

    native_difference = (
        results["earth_loaded"][
            "native_quadratic_functional"
        ]
        - results["earth_free_air_loaded"][
            "native_quadratic_functional"
        ]
    )

    return {
        "branch": BRANCH,
        "h_m": h,
        "reverse_magnetic": reverse,
        "fixed_beta_variational_audit": results,
        "earth_minus_air_native_functional":
            native_difference,
        "M5K_reduced_interaction_action_j":
            historical["coupled_response"][
                "paired_reduced_interaction_action_j"
            ],
        "source_audit": audit,
        "diagnostic_gates": {
            "full_weighted_matrix_symmetry_below_1e_minus_9":
                max_asymmetry < 1e-9,
            "on_shell_variation_below_1e_minus_8":
                max_variation < 1e-8,
            "native_half_conjugacy_below_1e_minus_9":
                max_identity < 1e-9,
            "M5K_carrier_energies_reproduced_within_1e_minus_6_j":
                max_energy_error < 1e-6,
        },
        "native_functional_is_SI_action": False,
        "native_functional_is_complete_action": False,
        "native_functional_derivative_is_mechanical_force":
            False,
        "physical_source_action_certified": False,
        "complete_source_matter_metric_gravity_action":
            False,
        "source_energy_j": None,
        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
        "006d_replaced": False,
    }
