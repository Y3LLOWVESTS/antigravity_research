"""R3X3B0 — exact inverse loading and source-support gate.

The R3B ~1.54-J preloaded configuration is retained as a target.

Corrected R3X1 equations:

    [ K_phi   lambda*C ] [phi] = [j_phi]
    [-lambda*D K_a    ] [ A ]   [j_A  ]

For an exactly unchanged global preloaded field at full loading,
the required additional RHS is:

    delta_j_phi = C @ A0
    delta_j_A   = -D @ phi0

These are discrete Euler-Lagrange residuals, not yet physical
currents or a source-energy calculation.

The run also checks L_minus = S L_plus S and finds the first
connected loading interval that fails the finite-payload 1g floor.

Results are scoped to the R3X1 frozen-beta finite-grid action.
No microscopic model, continuum certification or complete-energy
claim is implied.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.ndimage import binary_dilation
from scipy.sparse import bmat, diags

from .hook17_concurrent_u1_fieldstrength_metric import (
    SOURCE_RADIUS_M,
    TARGET_ACCELERATION_M_S2,
)

from .hook17_fdual_f_r3x1_lorentzian_sign_audit import (
    _build_baseline_and_prep,
    _solve_loaded,
    _state,
    _direct_compare,
    constitutive_action_gate,
)

BRANCH = "032H17A12D1R3X3B0"
GRIDS_M = (0.075, 0.05)
TARGET_G = float(TARGET_ACCELERATION_M_S2)

SOURCE_BUFFER_CELLS = 2
LOCAL_NORM_RESOLUTION = 1e-9
SIGN_REL_TOL = 2e-13

SCAN_FRACTIONS = (
    0.0,
    1e-9,
    1e-8,
    1e-7,
    3e-7,
    1e-6,
    3e-6,
    1e-5,
    3e-5,
    1e-4,
    1e-3,
    1e-2,
    0.1,
    1.0,
)


def provenance() -> dict[str, Any]:
    root = Path(__file__).resolve().parents[3] / "results" / "data"

    former = [
        (
            "032h17a12d1r3x1_lorentzian_sign_audit_summary.json",
            "lorentzian_sign_and_direct_solver_pass",
        ),
        (
            "032h17a12d1r3x2r2_energy_budget_dual_summary.json",
            "shell_only_10mj_excluded_fine_grid",
        ),
        (
            "032h17a12d1r3x3a_cross_sign_interface_summary.json",
            "physical_U1_XY_cross_topological_diagonalization",
        ),
    ]

    data = [
        json.loads((root / filename).read_text(encoding="utf-8"))
        for filename, _ in former
    ]

    passed = bool(
        all(
            document.get(key) is True
            for document, (_, key) in zip(data, former)
        )
        and all(
            document.get("006d_replaced") is False
            for document in data
        )
    )

    return {
        "pass": passed,
        "scope": "R3X1_R3X2R2_R3X3A_PROVENANCE_ONLY",
    }


def sign_identity(prep: dict[str, Any]) -> dict[str, Any]:
    """Verify exact signed-sector matrix conjugacy."""

    kp = prep["operators"]["k_phi"]
    ka = prep["operators"]["k_a"]

    c = prep["coupling"]["c"]
    d = prep["coupling"]["d"]

    nphi = kp.shape[0]
    na = ka.shape[0]

    plus = bmat(
        [[kp, c], [-d, ka]],
        format="csr",
    )

    minus = bmat(
        [[kp, -c], [d, ka]],
        format="csr",
    )

    s = diags(
        np.r_[np.ones(nphi), -np.ones(na)],
        format="csr",
    )

    discrepancy = (minus - s @ plus @ s).tocsr()

    residual = (
        float(np.max(np.abs(discrepancy.data)))
        if discrepancy.nnz
        else 0.0
    )

    scale = max(
        float(np.max(np.abs(plus.data))),
        1.0,
    )

    return {
        "conjugacy_max_absolute": residual,
        "conjugacy_relative": residual / scale,
        "sign_conjugacy_pass":
            bool(residual / scale < SIGN_REL_TOL),
        "full_two_sector_enlarges_same_sign_PSD_cone": False,
        "magnetic_source_reversal_required": True,
        "microscopic_source_reversal_certified": False,
        "field_redefinition_equivalence_only_with_symmetric_source_domain":
            True,
    }


def norm_fraction(
    values: np.ndarray,
    mask: np.ndarray,
) -> float:
    values = np.asarray(values, dtype=float).reshape(-1)
    mask = np.asarray(mask, dtype=bool).reshape(-1)

    total = float(np.linalg.norm(values))

    return (
        float(np.linalg.norm(values[mask]) / total)
        if total > 0.0
        else 0.0
    )


def support_audit(setup: dict[str, Any]) -> dict[str, Any]:
    """Find the exact compensating RHS for unchanged preloaded fields."""

    prep = setup["prep"]
    field = setup["field"]

    c = prep["coupling"]["c"]
    d = prep["coupling"]["d"]

    required_phi = np.asarray(
        c @ prep["a0_vec"]
    ).reshape(-1)

    required_a = np.asarray(
        -d @ prep["phi0_vec"]
    ).reshape(-1)

    original_phi = np.asarray(
        prep["operators"]["k_phi"] @ prep["phi0_vec"]
    ).reshape(-1)

    original_a = np.asarray(
        prep["operators"]["k_a"] @ prep["a0_vec"]
    ).reshape(-1)

    radius = np.hypot(
        field["rho_grid"],
        field["z_grid"],
    )

    payload = np.asarray(
        field["payload"],
        dtype=bool,
    )

    interface = binary_dilation(
        payload,
        iterations=2,
    )

    strict_source = radius <= float(SOURCE_RADIUS_M)

    buffered_radius = (
        float(SOURCE_RADIUS_M)
        + SOURCE_BUFFER_CELLS * float(field["h"])
    )

    generous_source = radius <= buffered_radius

    channels = []

    channel_data = (
        (
            "electric_static_charge",
            required_phi,
            original_phi,
            np.s_[1:-1, :-1],
        ),
        (
            "azimuthal_magnetic_source_current",
            required_a,
            original_a,
            np.s_[1:-1, 1:-1],
        ),
    )

    for kind, residual, original, sliced in channel_data:
        source_mask = strict_source[sliced].reshape(-1)
        buffer_mask = generous_source[sliced].reshape(-1)

        payload_mask = payload[sliced].reshape(-1)
        interface_mask = interface[sliced].reshape(-1)

        local_radius = radius[sliced].reshape(-1)
        local_z = field["z_grid"][sliced].reshape(-1)
        local_rho = field["rho_grid"][sliced].reshape(-1)

        if residual.size != source_mask.size:
            raise RuntimeError(
                f"DOF_SOURCE_MASK_MISMATCH: {kind}"
            )

        peak = int(np.argmax(np.abs(residual)))
        peak_value = float(np.max(np.abs(residual)))

        out_of_support = bool(
            np.any(
                np.abs(residual[~buffer_mask])
                >
                LOCAL_NORM_RESOLUTION
                * max(peak_value, 1e-100)
            )
        )

        channels.append({
            "channel": kind,
            "source_dof_count": int(residual.size),

            "required_rhs_l2_unphysical_units":
                float(np.linalg.norm(residual)),

            "required_rhs_max_abs_unphysical_units":
                peak_value,

            "baseline_current_l2_unphysical_units":
                float(np.linalg.norm(original)),

            "baseline_current_l2_fraction_outside_buffered_source":
                norm_fraction(original, ~buffer_mask),

            "residual_l2_fraction_outside_strict_2m_support":
                norm_fraction(residual, ~source_mask),

            "residual_l2_fraction_outside_buffered_support":
                norm_fraction(residual, ~buffer_mask),

            "residual_l2_fraction_on_payload_nodes":
                norm_fraction(residual, payload_mask),

            "residual_l2_fraction_payload_plus_two_cell_interface":
                norm_fraction(residual, interface_mask),

            "required_rhs_peak_rho_m":
                float(local_rho[peak]),

            "required_rhs_peak_z_m":
                float(local_z[peak]),

            "required_rhs_peak_radius_m":
                float(local_radius[peak]),

            "any_required_rhs_outside_buffer_at_rel_1e_minus_9":
                out_of_support,

            "required_physical_energy_j": None,
            "physical_current_normalization_proven": False,
        })

    impossible = any(
        channel[
            "any_required_rhs_outside_buffer_at_rel_1e_minus_9"
        ]
        for channel in channels
    )

    return {
        "channels": channels,
        "extra_source_outside_allowed_support": impossible,

        "exact_global_preloaded_potentials_with_external_only_old_action_ruled_out_on_grid":
            impossible,

        "all_altered_fields_or_metric_invariants_ruled_out":
            False,

        "all_action_derived_compensators_ruled_out":
            False,

        "source_radius_m":
            float(SOURCE_RADIUS_M),

        "buffered_support_radius_m":
            buffered_radius,

        "countercurrents_are_discrete_Euler_Lagrange_residuals_not_joules":
            True,
    }


def linear_loading_sensitivity(
    setup: dict[str, Any],
) -> dict[str, Any]:
    """Locate first loss of 1g under a uniform beta scaling diagnostic."""

    states = []

    for lam in SCAN_FRACTIONS:
        solution = _solve_loaded(
            setup["prep"],
            float(lam),
            1.0,
        )

        if not solution["success"]:
            raise RuntimeError(
                f"LOADED_SOLVE_FAILED_LAMBDA={lam}"
            )

        state = _state(setup, solution)

        minimum = state[
            "minimum_payload_acceleration_m_s2"
        ]

        states.append({
            "lambda": float(lam),
            "minimum_a_m_s2": minimum,
            "canonical_field_j":
                state["canonical_field_energy_j"],

            "worst_rho_m":
                state["worst_payload_rho_m"],

            "worst_z_m":
                state["worst_payload_z_m"],

            "one_g":
                bool(minimum >= TARGET_G - 1e-6),
        })

    first_failure = next(
        (
            i
            for i, row in enumerate(states[1:], start=1)
            if not row["one_g"]
        ),
        None,
    )

    refined = None

    if first_failure is not None:
        low = states[first_failure - 1]["lambda"]
        high = states[first_failure]["lambda"]

        if states[first_failure - 1]["one_g"]:
            for _ in range(18):
                mid = 0.5 * (low + high)

                solution = _solve_loaded(
                    setup["prep"],
                    mid,
                    1.0,
                )

                if not solution["success"]:
                    raise RuntimeError(
                        "HOMOTOPY_BISECTION_SOLVE_FAILED"
                    )

                value = _state(
                    setup,
                    solution,
                )["minimum_payload_acceleration_m_s2"]

                if value >= TARGET_G - 1e-6:
                    low = mid
                else:
                    high = mid

            refined = {
                "last_passing_lambda": float(low),
                "first_failing_lambda": float(high),

                "max_uniform_loading_allowed_in_initial_pass_interval":
                    float(low),

                "necessary_suppression_fraction_in_uniform_beta_rescaling_toy":
                    float(1.0 - high),

                "no_global_monotonicity_claim": True,
                "no_independent_action_parameter": True,
            }

    return {
        "scan": states,
        "first_failing_interval": refined,

        "uniform_beta_scale_is_not_freely_adjustable_in_complete_same_action":
            True,
    }


def action_augmentation_triage(
    audit: dict[str, Any],
) -> list[dict[str, Any]]:
    """Physical mechanism candidates, not completed action models."""

    outside = audit["extra_source_outside_allowed_support"]

    return [
        {
            "mechanism": "additional conserved material 4-current",
            "new_action_term":
                "-J_aux^mu A_mu with partial_mu J_aux^mu=0",
            "key_gate":
                "source location and neutral-payload preservation",
            "status":
                "HOLD_IF_ONLY_EXTERNAL_ALLOWED"
                if outside
                else "OPEN_SOURCE_REALIZATION",
            "complete_energy_j": None,
        },
        {
            "mechanism": "dynamical pseudoscalar compensator",
            "new_action_term":
                "-1/2(da)^2 - V(a) + a F_X tilde(F_Y)",
            "key_gate":
                "coupled axion equation, gradient energy, stability",
            "status":
                "OPEN_NEW_PHYSICS_NOT_YET_ACTION_COMPLETED",
            "complete_energy_j": None,
        },
        {
            "mechanism": "cross-kinetic or polarizable medium",
            "new_action_term":
                "f(psi,n) F_X^{mu nu} F_Y_mu nu",
            "key_gate":
                "new bulk loading, stress tensor, field redefinitions",
            "status":
                "OPEN_NEW_PHYSICS_WITH_NEW_BULK_COST",
            "complete_energy_j": None,
        },
        {
            "mechanism": "independent node-forming topological response",
            "new_action_term":
                "g(psi,n) F_X tilde(F_Y), dynamical psi",
            "key_gate":
                "independent interface response in a single action",
            "status":
                "OPEN_CONSTRAINED_ACTION_CONSTRUCTION",
            "complete_energy_j": None,
        },
        {
            "mechanism": "additional metric or geometric mediator",
            "new_action_term":
                "gauge-invariant geometric coupling",
            "key_gate":
                "healthy modes, Ward identities, empirical bounds",
            "status":
                "OPEN_ONLY_WITH_GENUINELY_NEW_CARRIER",
            "complete_energy_j": None,
        },
    ]


def run_grid(h: float) -> dict[str, Any]:
    setup = _build_baseline_and_prep(h)

    symmetry = sign_identity(setup["prep"])

    if not symmetry["sign_conjugacy_pass"]:
        raise RuntimeError(
            "SIGNED_SECTOR_MATRIX_CONJUGACY_FAILED"
        )

    support = support_audit(setup)

    preloaded = _state(
        setup,
        {
            "delta_phi_vec":
                np.zeros_like(setup["prep"]["phi0_vec"]),
            "delta_a_vec":
                np.zeros_like(setup["prep"]["a0_vec"]),
        },
    )

    solution = _solve_loaded(
        setup["prep"],
        1.0,
        1.0,
    )

    if not solution["success"]:
        raise RuntimeError(
            "FULL_CORRECTED_LOADING_FAILED"
        )

    loaded = _state(setup, solution)

    independent = _direct_compare(
        setup,
        solution,
        1.0,
        1.0,
    )

    if not independent["pass"]:
        raise RuntimeError(
            "DIRECT_SPARSE_VS_WOODBURY_MISMATCH"
        )

    homotopy = linear_loading_sensitivity(setup)

    return {
        "h_m": float(h),

        "preloaded_min_a_m_s2":
            preloaded["minimum_payload_acceleration_m_s2"],

        "preloaded_canonical_field_j":
            preloaded["canonical_field_energy_j"],

        "fully_loaded_min_a_m_s2":
            loaded["minimum_payload_acceleration_m_s2"],

        "fully_loaded_canonical_field_j":
            loaded["canonical_field_energy_j"],

        "full_load_direct_solver_pass":
            bool(independent["pass"]),

        "worst_payload_before": [
            preloaded["worst_payload_rho_m"],
            preloaded["worst_payload_z_m"],
        ],

        "worst_payload_after": [
            loaded["worst_payload_rho_m"],
            loaded["worst_payload_z_m"],
        ],

        "signed_sector_action_conjugacy": symmetry,
        "inverse_counter_source": support,
        "scalar_beta_suppression_diagnostic": homotopy,
    }


def decide(
    grids: list[dict[str, Any]],
    provenance_pass: bool,
    action_pass: bool,
) -> dict[str, Any]:
    accepted = bool(
        provenance_pass
        and action_pass
        and len(grids) == len(GRIDS_M)
        and all(
            grid["signed_sector_action_conjugacy"][
                "sign_conjugacy_pass"
            ]
            and grid["full_load_direct_solver_pass"]
            for grid in grids
        )
    )

    external_failure = bool(
        all(
            grid["inverse_counter_source"][
                "extra_source_outside_allowed_support"
            ]
            for grid in grids
        )
    )

    if not accepted:
        decision = (
            "RED_HOLD_R3X3B0_ACTION_OR_NUMERICAL_PROVENANCE"
        )
        next_run = "REPAIR_INVERSE_LOADING_CERTIFICATE"

    elif external_failure:
        decision = (
            "GREEN_SCOPED_EXACT_MIRROR_"
            "EXTERNAL_ONLY_COUNTERSOURCE_OBSTRUCTION"
        )
        next_run = (
            "R3X3B1_ACTION_DERIVED_INTERFACE_"
            "COMPENSATOR_PREFLIGHT"
        )

    else:
        decision = (
            "YELLOW_EXACT_MIRROR_SOURCE_SUPPORT_UNRESOLVED"
        )
        next_run = (
            "R3X3B1_EXPLICIT_EXTERNAL_"
            "COUNTERSOURCE_ENERGY_AND_WARD"
        )

    return {
        "decision": decision,
        "next": next_run,

        "external_only_exact_global_mirror_excluded_both_grids":
            bool(accepted and external_failure),

        "different_profile_same_metric_acceleration_excluded":
            False,

        "full_action_and_microscopic_currents_certified":
            False,

        "parity_cp_anomaly_completed": False,
        "continuum_certified": False,
        "complete_energy_established": False,

        "field_energy_under_100j_requires_no_further_downward_optimization":
            True,

        "physical_antigravity_model_found": False,
        "certified_sub10mj_model_found": False,
        "006d_replaced": False,
    }
