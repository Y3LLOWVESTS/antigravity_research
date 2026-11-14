"""B17-M5A: theorem-first, oracle-guided inverse source design.

The reduced static R3X1 Lorentzian carrier equations are linear
in the two source currents for any fixed material distribution.

Consequently, the stationary action and positive elliptic
carrier-gradient norm are quadratic in source amplitudes x:

    S_int(x) = x.T S x
    Q_E(x)   = x.T Q_E x
    Q_C(x)   = x.T Q_C x
    H(x)     = x.T H x

The actual two-current source family can be optimized exactly
using generalized eigenvalues, without a blind parameter scan.

The reciprocal-translation necessary condition is:

    x.T (Q_E + Q_C) x = 0

An independent artificial oracle imposes the desired signed
Earth/craft action slopes and identifies missing terms.

IMPORTANT:
- The oracle is guaranteed to succeed algebraically ONLY.
- These action derivatives are NOT certified mechanical forces.
- H is a positive discrete elliptic carrier-gradient norm,
  NOT certified complete or source-hardware energy.
- M4B1 is an approximate R3B-aligned source, not exact B7.
- Virtual source translations do not satisfy a derived moving-
  current Ward/continuity equation.
- Exterior metric transmission, full matter/gravity equations,
  boundary convergence, source reaction, quantum consistency,
  and whole-craft lift are not established.
- Preserve original 1.542916 J R3B field-capacity result.
"""

from __future__ import annotations

import math

import numpy as np
from scipy.linalg import eigh

from .hook17_r3b_m4b1_source_recovery import (
    assemble_original_aligned_source,
)
from .hook17_r3b_m4b2_earth_variational_audit import (
    _weights,
    _on_shell_action,
)
from .hook17_r3b_m4b4_paired_translation import (
    shifted_source,
    shifted_material,
    source_support_check,
)
from .hook17_r3b_m4b_sparse_earth_loading import (
    _solve_fixed_sources,
)

BRANCH = "032H17A12D1R3X3B17-M5A"
ORIGINAL_R3B_J = 1.5429162116460216
ENERGY_BUDGET_J = 10_000_000.0


def _quadratic_matrix(x0, x1, xsum):
    """Recover a symmetric quadratic matrix by polarization."""
    cross = 0.5 * (xsum - x0 - x1)

    return np.array(
        [[x0, cross], [cross, x1]],
        dtype=float,
    )


def _carrier_gradient_norm(state, source, weights):
    """Positive elliptic norm, not complete canonical device energy."""
    wp, wa, normalization = weights
    operators = source["operators"]

    phi = state["phi"][1:-1, :-1].reshape(-1)
    a = state["a"][1:-1, 1:-1].reshape(-1)

    return float(
        0.5 * normalization * (
            np.dot(
                wp * phi,
                operators["k_phi"] @ phi,
            )
            + np.dot(
                wa * a,
                operators["k_a"] @ a,
            )
        )
    )


def _action_and_norm_matrix(
    source,
    portal_ev,
    earth_z,
    craft_z,
    earth_present,
    weights,
):
    """Re-solve for electric-only, magnetic-only, and both.

    The third solve independently establishes the off-diagonal
    cross-source response. This includes matter-induced carrier
    mixing through the existing corrected Lorentzian operator.
    """
    base = shifted_source(
        source,
        portal_ev,
        craft_z,
    )

    beta, _, _ = shifted_material(
        source,
        earth_z,
        craft_z,
        portal_ev,
        earth_present=earth_present,
    )

    actions = []
    norms = []
    residuals = []

    for electric, magnetic in (
        (1.0, 0.0),
        (0.0, 1.0),
        (1.0, 1.0),
    ):
        currents = {
            **base,
            "j_phi": electric * base["j_phi"],
            "j_a": magnetic * base["j_a"],
        }

        state = _solve_fixed_sources(
            currents,
            beta,
            1.0,
        )

        actions.append(
            _on_shell_action(
                state,
                currents,
                weights,
            )
        )

        norms.append(
            _carrier_gradient_norm(
                state,
                source,
                weights,
            )
        )

        residuals.append(float(state["residual"]))

    return (
        _quadratic_matrix(*actions),
        _quadratic_matrix(*norms),
        max(residuals),
    )


def _defect_null_directions(qe, qc, h):
    """Solve reciprocal-action condition on unit H-norm circle.

    Whitening by positive H converts the homogeneous quadratic
    condition into a two-dimensional spectral problem.

    An indefinite defect has two distinct unoriented null rays.
    A definite defect has no nonzero exact null direction.
    """
    eigen_h, vectors_h = np.linalg.eigh(h)

    if np.min(eigen_h) <= 0:
        return []

    inv_root = (
        vectors_h * eigen_h**(-0.5)
    ) @ vectors_h.T

    d = inv_root @ (qe + qc) @ inv_root
    eigen_d, vectors_d = np.linalg.eigh(
        0.5 * (d + d.T)
    )

    if eigen_d[0] < 0 < eigen_d[1]:
        a = math.sqrt(
            eigen_d[1] /
            (eigen_d[1] - eigen_d[0])
        )
        b = math.sqrt(
            -eigen_d[0] /
            (eigen_d[1] - eigen_d[0])
        )

        directions = [
            a * vectors_d[:, 0] + b * vectors_d[:, 1],
            a * vectors_d[:, 0] - b * vectors_d[:, 1],
        ]

    elif max(abs(eigen_d)) < 1e-12:
        directions = [
            np.array([1.0, 0.0]),
            np.array([0.0, 1.0]),
        ]

    elif abs(eigen_d[0]) < 1e-12:
        directions = [vectors_d[:, 0]]

    elif abs(eigen_d[1]) < 1e-12:
        directions = [vectors_d[:, 1]]

    else:
        return []

    output = []

    for direction in directions:
        x = inv_root @ direction

        x /= math.sqrt(
            float(x @ h @ x)
        )

        earth = float(x @ qe @ x)
        craft = float(x @ qc @ x)

        output.append({
            "source_amplitude_direction": x.tolist(),
            "earth_slope_per_quadratic_norm": earth,
            "craft_slope_per_quadratic_norm": craft,
            "reciprocity_defect_per_norm": earth + craft,
        })

    return output


def _inverse_extremes(qe, qc, h, target):
    """Exact optimal signed response per unit positive norm."""
    if (
        np.max(np.abs(qe - qe.T)) > 1e-8
        or np.max(np.abs(h - h.T)) > 1e-8
    ):
        raise ArithmeticError(
            "Broken source quadratic symmetry"
        )

    eigenvalues, vectors = eigh(
        qe,
        h,
        check_finite=True,
    )

    if not np.isfinite(eigenvalues).all():
        raise ArithmeticError(
            "Nonfinite response eigenvalues"
        )

    optimal = {}

    for label, sign in (
        ("earth_slope_negative", -1.0),
        ("earth_slope_positive", +1.0),
    ):
        index = int(np.argmax(sign * eigenvalues))
        response = float(sign * eigenvalues[index])

        direction = vectors[:, index].copy()

        if direction[0] < 0:
            direction *= -1

        if response <= 0:
            optimal[label] = {
                "exists": False,
                "reason": "Requested sign absent in two-source space",
            }
            continue

        required_norm = abs(target) / response
        scaled = math.sqrt(required_norm) * direction

        optimal[label] = {
            "exists": True,
            "unit_norm_optimal_source_ratio":
                direction.tolist(),
            "response_per_quadratic_norm":
                float(eigenvalues[index]),
            "quadratic_norm_needed_for_target_j":
                required_norm,
            "required_electric_magnetic_current_multipliers":
                scaled.tolist(),
            "craft_slope_at_target_j_per_m":
                float(scaled @ qc @ scaled),
            "reciprocity_defect_at_target_j_per_m":
                float(scaled @ (qe + qc) @ scaled),
            "norm_under_10mj_not_complete_energy":
                bool(required_norm < ENERGY_BUDGET_J),
        }

    return {
        "eigenvalues_per_norm": [
            float(v) for v in eigenvalues
        ],
        "optimal_signs": optimal,
        "exact_reciprocal_null_directions":
            _defect_null_directions(qe, qc, h),
    }


def _shape_source(source, bias):
    """Pre-registered fore/aft source-shaping hypothesis.

    Positive bias increases source participation toward negative z
    (the Earth-facing side). Negative bias emphasizes the upper side.

    Remove the induced net electric monopole using a compact
    onboard compensation profile. The magnetic current remains
    a toroidal axisymmetric source control.

    No microscopic realization is claimed.
    """
    wp, _, _ = _weights(source)

    if bias == 0:
        jp = np.asarray(source["j_phi"])

        neutrality = (
            abs(float(wp @ jp))
            / max(float(wp @ abs(jp)), 1e-200)
        )

        return source, neutrality

    field = source["field"]
    z = field["z_grid"]
    r = field["rho_grid"]

    jp0 = np.asarray(source["j_phi"])
    ja0 = np.asarray(source["j_a"])

    ze = z[1:-1, :-1].reshape(-1)
    za = z[1:-1, 1:-1].reshape(-1)

    jp = jp0 * (1.0 - bias * ze / 2.0)
    ja = ja0 * (1.0 - bias * za / 2.0)

    radius = r[1:-1, :-1].reshape(-1)

    compensator = np.where(
        radius < 1.75,
        (1.0 - (radius / 1.75)**2)**2,
        0.0,
    )

    denominator = float(wp @ compensator)

    if denominator <= 0:
        raise ArithmeticError(
            "Missing compact monopole compensator"
        )

    jp -= compensator * (
        float(wp @ jp) / denominator
    )

    neutrality = (
        abs(float(wp @ jp))
        / max(float(wp @ abs(jp)), 1e-200)
    )

    return {
        **source,
        "j_phi": jp,
        "j_a": ja,
    }, neutrality


def field_retention_oracle(summary, target_force_magnitude_n):
    """Artificial uniform-field-retention approximation.

    Suppose F_tracer(r) = r**2 * F_frozen.
    This ignores the spatial changes caused by material loading.
    The tracer force is not a whole-craft physical force.
    """
    states = summary["cases"][
        "1000eV_ground_air"
    ]["states"]

    frozen = float(
        states["0.0"]["earth_ground_tracer_force_n"]
    )
    loaded = float(
        states["1.0"]["earth_ground_tracer_force_n"]
    )

    needed = (
        math.sqrt(
            target_force_magnitude_n / abs(frozen)
        )
        if frozen else None
    )

    effective = (
        math.sqrt(loaded / frozen)
        if frozen and loaded / frozen >= 0
        else None
    )

    return {
        "frozen_earth_tracer_n": frozen,
        "loaded_earth_tracer_n": loaded,
        "hypothetical_uniform_amplitude_retention_needed":
            needed,
        "hypothetical_uniform_amplitude_retention_current":
            effective,
        "additional_amplitude_gain_needed": (
            needed / effective
            if needed is not None and effective
            else None
        ),
        "frozen_model_can_meet_magnitude_goal":
            abs(frozen) >= target_force_magnitude_n,
        "real_loaded_spatial_fields_rescaled_uniformly":
            False,
        "source_reaction_and_spacecraft_lift_certified":
            False,
    }


def evaluate(
    h=0.25,
    portal_ev=21147.0,
    step_m=0.0002,
    craft_mass_kg=1000.0,
    shape_bias=0.0,
):
    """Solve source-space inverse problem and explicit oracle gap."""
    if (
        not math.isfinite(h)
        or h not in (0.2, 0.25, 0.3)
        or not math.isfinite(portal_ev)
        or portal_ev <= 0
        or not math.isfinite(step_m)
        or not 1e-7 <= step_m <= 0.005
        or not math.isfinite(craft_mass_kg)
        or craft_mass_kg <= 0
    ):
        raise ValueError(
            "Invalid inverse-design parameters"
        )

    if shape_bias not in (0.0, 0.5, -0.5):
        raise ValueError(
            "Only preregistered source biases permitted"
        )

    source, neutrality = _shape_source(
        assemble_original_aligned_source(float(h)),
        shape_bias,
    )

    weights = _weights(source)

    # Earth and craft coordinates move independently.
    # Their source-fixed action is independently re-solved.
    positions = {
        "center": (0.0, 0.0),
        "earth_plus": (+step_m, 0.0),
        "earth_minus": (-step_m, 0.0),
        "craft_plus": (0.0, +step_m),
        "craft_minus": (0.0, -step_m),
    }

    matrices = {}
    residuals = []

    for name, (earth_z, craft_z) in positions.items():
        on, h_on, r_on = _action_and_norm_matrix(
            source, portal_ev,
            earth_z, craft_z,
            True, weights,
        )

        off, _, r_off = _action_and_norm_matrix(
            source, portal_ev,
            earth_z, craft_z,
            False, weights,
        )

        matrices[name] = {
            "interaction": on - off,
            "loaded_norm": h_on,
        }

        residuals.extend((r_on, r_off))

    qe = (
        matrices["earth_plus"]["interaction"]
        - matrices["earth_minus"]["interaction"]
    ) / (2.0 * step_m)

    qc = (
        matrices["craft_plus"]["interaction"]
        - matrices["craft_minus"]["interaction"]
    ) / (2.0 * step_m)

    hnorm = matrices["center"]["loaded_norm"]
    norm_eigenvalues = np.linalg.eigvalsh(hnorm)

    if np.min(norm_eigenvalues) <= 0:
        raise ArithmeticError(
            "Carrier-gradient quadratic norm is not positive"
        )

    controls = {}

    for label, values in (
        ("both_positive", (1.0, 1.0)),
        ("magnetic_reversed", (1.0, -1.0)),
        ("both_reversed", (-1.0, -1.0)),
        ("electric_only", (1.0, 0.0)),
        ("magnetic_only", (0.0, 1.0)),
    ):
        x = np.array(values)

        earth = float(x @ qe @ x)
        craft = float(x @ qc @ x)

        controls[label] = {
            "amplitude_vector": x.tolist(),
            "earth_action_slope_j_per_m": earth,
            "craft_action_slope_j_per_m": craft,
            "reciprocity_defect_j_per_m": earth + craft,
            "gradient_norm_j_not_device_energy":
                float(x @ hnorm @ x),
        }

    # Illustration only: weight of an assumed 1000 kg craft.
    target = 9.80665 * craft_mass_kg

    inverse = _inverse_extremes(
        qe, qc, hnorm, target
    )

    original = controls["both_positive"]

    # This oracle artificially adds the missing interaction.
    # It is not obtained by solving the physical carrier action.
    oracle = {
        "construction":
            "S_oracle = -F_target * (z_E-z_C); freely injected",
        "target_craft_mass_kg": craft_mass_kg,
        "signed_earth_action_slope_j_per_m": -target,
        "signed_craft_action_slope_j_per_m": target,
        "reciprocity_defect_j_per_m": 0.0,
        "guaranteed_by_algebra": True,
        "physical_action_derived": False,
        "requires_unmodeled_external_coupling": True,
        "energy_cost_j": None,
        "source_off_limit_derived": False,
        "genuine_lift": False,
    }

    e = original["earth_action_slope_j_per_m"]
    c = original["craft_action_slope_j_per_m"]

    return {
        "branch": BRANCH,
        "classification":
            "ORACLE_RELAXATION_AND_EXACT_TWO_CURRENT_INVERSE_DIAGNOSTIC",
        "grid_m": float(h),
        "portal_scale_ev": float(portal_ev),
        "translation_step_m": step_m,
        "pre_registered_source_shape_bias": shape_bias,
        "net_electric_charge_fraction": neutrality,
        "source_geometry_is_microscopically_realized":
            False,
        "source_basis": [
            "M4B1 approximate electric source",
            "M4B1 approximate magnetic source",
        ],
        "source_is_original_B7_or_R3B_exact": False,
        "original_R3B_field_capacity_reference_j":
            ORIGINAL_R3B_J,
        "action_slope_source_matrices": {
            "earth_j_per_m": qe.tolist(),
            "craft_j_per_m": qc.tolist(),
            "reciprocity_defect_j_per_m":
                (qe + qc).tolist(),
            "carrier_gradient_norm_j": hnorm.tolist(),
        },
        "basis_norm_positive_eigenvalues":
            norm_eigenvalues.tolist(),
        "max_coupled_solver_residual":
            float(max(residuals)),
        "polarity_controls": controls,
        "inverse_source_space": inverse,
        "artificial_success_oracle": oracle,
        "oracle_correction_for_original_source": {
            "additional_earth_slope_j_per_m": -target - e,
            "additional_craft_slope_j_per_m": target - c,
            "minimum_equal_opposite_projection_pair_j_per_m":
                [0.5 * (e - c), 0.5 * (c - e)],
            "this_is_a_new_physical_coupling": False,
        },
        "exterior_transmission_theorem": {
            "if_both_carrier_field_strengths_vanish_outside_enclosure":
                "local algebraic F_X dual_F_Y portal vanishes outside",
            "outside_enclosure_carriers_solved_and_transmitted":
                False,
            "new_independently_propagating_metric_mode_derived":
                False,
            "whole_craft_lift_deducible": False,
        },
        "source_support_plus":
            source_support_check(source, step_m),
        "source_support_minus":
            source_support_check(source, -step_m),
        "same_action_full_Ward_Noether_certified": False,
        "source_translation_continuity_certified": False,
        "finite_box_artifact_excluded": False,
        "physical_metric_exterior_transmission_derived":
            False,
        "Earth_craft_reaction_physically_closed": False,
        "loaded_force_grid_convergence_certified": False,
        "whole_craft_force_n": None,
        "full_operating_energy_j": None,
        "strict_sub_10mj_device_certified": False,
        "006d_replaced": False,
        "warnings": [
            "Artificial oracle injects the desired interaction",
            "Action derivatives are NOT certified thrust",
            "Carrier norm is NOT complete operating energy",
            "Source scaling requires new physical sourcing checks",
            "No full Noether/momentum or enclosure transmission proof",
        ],
    }
