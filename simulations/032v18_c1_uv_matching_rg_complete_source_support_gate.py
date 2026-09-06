"""032V18 — universal metric, RG invariants, and support-ready source gate.

V17 found an exact finite-payload oblate partial corridor near 59.42 kJ but
correctly blocked promotion because fixed-order axial canonicalization was not
under control.

V18 performs four high-value corrections:

1. Separate universal-metric provenance from species-level C1 operator
   provenance.
2. Show explicitly that scalar wavefunction rescaling preserves C1 f^2, so a
   large Delta Z is a matching problem rather than an automatic energy
   multiplier.
3. Reject the shortcut of transplanting the V16 oblate loop-0.30 microscopic
   state into a spherical source.
4. Re-optimize a support-friendly spherical source at the same loop-0.30
   criterion and solve its exact finite-payload loading problem.

The spherical support calculation includes the exact integrated canonical
scalar dipole stress anisotropy and the resulting DEC support lower bound.

It still does NOT construct the physical bag wall or UV completion.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from scipy.optimize import (
    differential_evolution,
    minimize_scalar,
)

from antigravity_research.agminer.axial_dirac_meanfield import (
    fixed_density_current_susceptibility_hat,
    meanfield_scaling_metrics,
    payload_trace_load,
    physicalize_dimensionless_state,
)
from antigravity_research.agminer.c1_payload_matching import (
    axial_leading_log_wavefunction_proxy,
    c1_from_metric_scale_ev,
    jiang_nda_scale_from_c1_ev,
    payload_surface_acceleration_metrics,
    payload_volume_average_acceleration_m_s2,
    required_q2_for_payload_surface,
    source_feedback_metrics,
)
from antigravity_research.agminer.candidate import Candidate
from antigravity_research.agminer.normalization import (
    canonical_invariant_fingerprint,
)
from antigravity_research.agminer.oracle import (
    ActionOracle,
    LEDGER_PARTIAL_OPTIMISTIC,
    assess_oracle,
)
from antigravity_research.agminer.policy import (
    current_energy_policy,
)
from antigravity_research.agminer.reporting import (
    rebuild_summaries,
)
from antigravity_research.agminer.storage import Storage
from antigravity_research.agminer.universal_metric_support import (
    canonical_rescaling,
    isotropic_bag_shape_compatible,
    polarized_sphere_incident_coefficients,
    spherical_anisotropic_dec_support_floor_j,
)


ROOT = Path(__file__).resolve().parents[1]

V16 = (
    ROOT
    / "results"
    / "data"
    / "032v16_axial_dirac_meanfield_self_consistency_summary.json"
)

V17 = (
    ROOT
    / "results"
    / "data"
    / "032v17_c1_payload_quantum_control_summary.json"
)

OUT = (
    ROOT
    / "results"
    / "data"
    / "032v18_universal_metric_rg_support_ready_summary.json"
)

SPHERE_OUT = (
    ROOT
    / "results"
    / "data"
    / "032v18_spherical_support_ready_scale_scan.csv"
)

COMPARE_OUT = (
    ROOT
    / "results"
    / "data"
    / "032v18_oblate_sphere_frontier_comparison.csv"
)

DB = (
    ROOT
    / "results"
    / "agminer"
    / "agminer.sqlite3"
)


TARGET_J = 1.0e7
G = 9.80665

REFERENCE_SCALE_EV = 1.0e5

PAYLOAD_MASS_KG = 1.0
PAYLOAD_RADIUS_M = 0.10
PAYLOAD_CENTER_Z_M = 0.20

SOURCE_RADIUS_M = 0.10
SOURCE_CENTER_Z_M = -0.10

CENTER_SEPARATION_M = (
    PAYLOAD_CENTER_Z_M
    - SOURCE_CENTER_Z_M
)

SOURCE_VOLUME_M3 = (
    4.0
    * math.pi
    * SOURCE_RADIUS_M**3
    / 3.0
)

SPHERE_DEMAG_Z = (
    1.0
    / 3.0
)

LOOP_CAP = 0.30
MAX_FLAVORS = 256


# ============================================================
# 0. POLICY / PROVENANCE
# ============================================================

policy = current_energy_policy()

assert float(
    policy[
        "limit_j"
    ]
) == TARGET_J

assert str(
    policy[
        "comparison"
    ]
) == "LT"

assert str(
    policy[
        "policy_id"
    ]
) == "ENERGY_ab8c16e45c837ffc"

assert V16.exists()
assert V17.exists()

v16 = json.loads(
    V16.read_text(
        encoding="utf-8"
    )
)

v17 = json.loads(
    V17.read_text(
        encoding="utf-8"
    )
)

assert (
    v17[
        "decision"
    ]
    ==
    (
        "GREEN_PUBLISHED_C1_OUTWARD_EFT_MATCH_"
        "GREEN_EXACT_FINITE_PAYLOAD_LOWM_PARTIAL_CORRIDOR_"
        "RED_FIXED_ORDER_AXIAL_CANONICALIZATION_CONTROL_"
        "UV_MATCHING_REQUIRED"
    )
)


# ============================================================
# 1. PROVENANCE CORRECTION
# ============================================================

provenance = {
    "jiang_o1_species_level_qed_operator":
        True,

    "jiang_o1_alone_proves_universal_metric":
        False,

    "brax_valageas_universal_kinetic_conformal_metric":
        True,

    "brax_valageas_jordan_metric":
        "g_phys=A(X)^2*g_einstein",

    "all_neutral_matter_one_physical_metric_available_at_action_level":
        True,

    "published_framework_can_have_repulsive_fifth_force":
        True,

    "published_minimal_A_equals_1_plus_chi_has_required_static_sign":
        False,

    "required_outward_A_equals_1_minus_chi_action_level_allowed":
        True,

    "required_outward_sign_universal_uv_completion_proved":
        False,

    "known_jiang_positive_c1_uv_example_used":
        False,

    "reason_known_example_not_promoted":
        "COMPANION_J2_OPERATORS_AND_CLOSED_SPIN2_REALIZATION",
}


# ============================================================
# 2. CANONICAL FIELD-RESCALING INVARIANT
# ============================================================

oblate_context = (
    v17[
        "optimal_eft_context"
    ]
)

rescaling_demo = canonical_rescaling(
    c1_bare_ev_m4=
        float(
            oblate_context[
                "c1_ev_m4"
            ]
        ),

    f_bare_ev=
        float(
            oblate_context[
                "f_psi_ev"
            ]
        ),

    kinetic_z=
        1.0
        + float(
            oblate_context[
                "leading_log_delta_z_proxy"
            ]
        ),
)

assert (
    rescaling_demo[
        "invariant_relative_error"
    ]
    < 1.0e-14
)

canonical_status = {
    "c1_f_squared_rescaling_invariant":
        True,

    "large_delta_z_is_automatic_energy_multiplier":
        False,

    "fixed_order_v17_control":
        "RED",

    "rg_matched_low_energy_eft":
        "OPEN",

    "renormalized_physical_c1_f2_matched":
        False,
}


# ============================================================
# 3. MINIMAL BAG MORPHOLOGY GATE
# ============================================================

oblate_a_m = float(
    v17[
        "exact_payload"
    ].get(
        "source_a_m",
        0.25740088555864965,
    )
)

oblate_c_m = (
    0.09659120999271102
)

oblate_minimal_isotropic_bag = (
    isotropic_bag_shape_compatible(
        a_m=
            oblate_a_m,

        c_m=
            oblate_c_m,
    )
)

sphere_minimal_isotropic_bag = (
    isotropic_bag_shape_compatible(
        a_m=
            SOURCE_RADIUS_M,

        c_m=
            SOURCE_RADIUS_M,
    )
)

assert (
    oblate_minimal_isotropic_bag
    is False
)

assert (
    sphere_minimal_isotropic_bag
    is True
)


# ============================================================
# 4. EXACT SPHERICAL VACUUM SOURCE
# ============================================================

sphere_coefficients = (
    polarized_sphere_incident_coefficients(
        source_radius_m=
            SOURCE_RADIUS_M,

        center_separation_m=
            CENTER_SEPARATION_M,

        lmax=
            32,
    )
)

sphere_coefficients_l28 = (
    polarized_sphere_incident_coefficients(
        source_radius_m=
            SOURCE_RADIUS_M,

        center_separation_m=
            CENTER_SEPARATION_M,

        lmax=
            28,
    )
)

vacuum_requirement = (
    required_q2_for_payload_surface(
        coefficients=
            sphere_coefficients,

        epsilon_trace_load=
            0.0,

        payload_radius_m=
            PAYLOAD_RADIUS_M,

        target_acceleration_m_s2=
            G,

        surface_count=
            1601,
    )
)

sphere_q_vacuum = math.sqrt(
    float(
        vacuum_requirement[
            "q2"
        ]
    )
)

assert math.isclose(
    sphere_q_vacuum,
    3.6616787206413e-7,
    rel_tol=2.0e-10,
)


# ============================================================
# 5. NO SHORTCUT: OBLATE STATE DOES NOT REMAIN LOOP-0.30
# ============================================================

old_selected = (
    v16[
        "selected_positive_band_partial_corridor"
    ]
)

old_r = float(
    old_selected[
        "r_mass_over_b"
    ]
)

old_u = float(
    old_selected[
        "u_mu_over_b"
    ]
)

naive_sphere_reuse = (
    meanfield_scaling_metrics(
        q=
            sphere_q_vacuum,

        metric_scale_ev=
            REFERENCE_SCALE_EV,

        volume_m3=
            SOURCE_VOLUME_M3,

        demag_z=
            SPHERE_DEMAG_Z,

        r_mass_over_b=
            old_r,

        u_mu_over_b=
            old_u,

        order=
            96,
    )
)

naive_sphere_loop = float(
    naive_sphere_reuse[
        "loop_proxy"
    ]
)

assert (
    naive_sphere_loop
    > 0.50
)


# ============================================================
# 6. RE-OPTIMIZE SPHERICAL MICROSCOPIC STATE
# ============================================================

def sphere_support_and_total(
    metrics,
):
    support = (
        spherical_anisotropic_dec_support_floor_j(
            fermion_pressure_perp_inventory_j=
                float(
                    metrics[
                        "pressure_perp_inventory_j"
                    ]
                ),

            fermion_pressure_z_inventory_j=
                float(
                    metrics[
                        "pressure_z_inventory_j"
                    ]
                ),

            scalar_field_energy_j=
                float(
                    metrics[
                        "field_energy_j"
                    ]
                ),
        )
    )

    total = (
        float(
            metrics[
                "band_energy_j"
            ]
        )
        + float(
            metrics[
                "field_energy_j"
            ]
        )
        + float(
            support[
                "support_energy_floor_j"
            ]
        )
    )

    return support, total


def optimization_objective(
    log_values,
) -> float:
    r_value = (
        10.0
        ** float(
            log_values[
                0
            ]
        )
    )

    u_value = (
        10.0
        ** float(
            log_values[
                1
            ]
        )
    )

    try:
        metrics = (
            meanfield_scaling_metrics(
                q=
                    sphere_q_vacuum,

                metric_scale_ev=
                    REFERENCE_SCALE_EV,

                volume_m3=
                    SOURCE_VOLUME_M3,

                demag_z=
                    SPHERE_DEMAG_Z,

                r_mass_over_b=
                    r_value,

                u_mu_over_b=
                    u_value,

                order=
                    48,
            )
        )

    except (
        ValueError,
        RuntimeError,
        FloatingPointError,
    ):
        return 1.0e99

    _, total = sphere_support_and_total(
        metrics
    )

    loop_violation = max(
        0.0,
        float(
            metrics[
                "loop_proxy"
            ]
        )
        / LOOP_CAP
        - 1.0,
    )

    flavor_violation = max(
        0.0,
        float(
            metrics[
                "minimum_flavors_continuous_for_margin5"
            ]
        )
        / MAX_FLAVORS
        - 1.0,
    )

    return (
        total
        * (
            1.0
            + 1.0e7
            * (
                loop_violation**2
                + flavor_violation**2
            )
        )
    )


optimization = differential_evolution(
    optimization_objective,

    bounds=(
        (
            -0.7,
            0.8,
        ),
        (
            -0.1,
            1.2,
        ),
    ),

    seed=
        18180,

    popsize=
        10,

    maxiter=
        75,

    tol=
        1.0e-9,

    polish=
        True,

    workers=
        1,

    updating=
        "immediate",
)


sphere_r = (
    10.0
    ** float(
        optimization.x[
            0
        ]
    )
)

sphere_u = (
    10.0
    ** float(
        optimization.x[
            1
        ]
    )
)


sphere_reference_metrics = (
    meanfield_scaling_metrics(
        q=
            sphere_q_vacuum,

        metric_scale_ev=
            REFERENCE_SCALE_EV,

        volume_m3=
            SOURCE_VOLUME_M3,

        demag_z=
            SPHERE_DEMAG_Z,

        r_mass_over_b=
            sphere_r,

        u_mu_over_b=
            sphere_u,

        order=
            96,
    )
)

sphere_reference_support, sphere_reference_total = (
    sphere_support_and_total(
        sphere_reference_metrics
    )
)


sphere_loop = float(
    sphere_reference_metrics[
        "loop_proxy"
    ]
)

sphere_nf_continuous = float(
    sphere_reference_metrics[
        "minimum_flavors_continuous_for_margin5"
    ]
)

assert (
    sphere_loop
    <
    LOOP_CAP
    * (
        1.0
        + 2.0e-6
    )
)

assert (
    sphere_nf_continuous
    <
    MAX_FLAVORS
)


sphere_susceptibility = (
    fixed_density_current_susceptibility_hat(
        r_mass_over_b=
            sphere_r,

        u_mu_over_b=
            sphere_u,

        order=
            96,
    )
)

assert (
    float(
        sphere_susceptibility[
            "susceptibility_hat"
        ]
    )
    > 0.0
)


# ============================================================
# 7. EXACT FINITE-PAYLOAD SPHERICAL SCALE OPTIMUM
# ============================================================

def evaluate_sphere_scale(
    scale_ev: float,
    *,
    coefficients=sphere_coefficients,
    surface_count: int = 801,
):
    scale = float(
        scale_ev
    )

    trace = (
        payload_trace_load(
            payload_mass_kg=
                PAYLOAD_MASS_KG,

            payload_radius_m=
                PAYLOAD_RADIUS_M,

            metric_scale_ev=
                scale,
        )
    )

    epsilon = float(
        trace[
            "epsilon_trace_load"
        ]
    )

    requirement = (
        required_q2_for_payload_surface(
            coefficients=
                coefficients,

            epsilon_trace_load=
                epsilon,

            payload_radius_m=
                PAYLOAD_RADIUS_M,

            target_acceleration_m_s2=
                G,

            surface_count=
                surface_count,
        )
    )

    q2_value = float(
        requirement[
            "q2"
        ]
    )

    q_value = math.sqrt(
        q2_value
    )

    metrics = (
        meanfield_scaling_metrics(
            q=
                q_value,

            metric_scale_ev=
                scale,

            volume_m3=
                SOURCE_VOLUME_M3,

            demag_z=
                SPHERE_DEMAG_Z,

            r_mass_over_b=
                sphere_r,

            u_mu_over_b=
                sphere_u,

            order=
                96,
        )
    )

    support, total = (
        sphere_support_and_total(
            metrics
        )
    )

    return {
        "metric_scale_ev":
            scale,

        "epsilon_trace_load":
            epsilon,

        "q":
            q_value,

        "q2":
            q2_value,

        "q2_factor_from_vacuum":
            q2_value
            / float(
                vacuum_requirement[
                    "q2"
                ]
            ),

        "field_energy_j":
            float(
                metrics[
                    "field_energy_j"
                ]
            ),

        "occupied_band_energy_j":
            float(
                metrics[
                    "band_energy_j"
                ]
            ),

        "fermion_pressure_perp_inventory_j":
            float(
                metrics[
                    "pressure_perp_inventory_j"
                ]
            ),

        "fermion_pressure_z_inventory_j":
            float(
                metrics[
                    "pressure_z_inventory_j"
                ]
            ),

        "support_energy_floor_j":
            float(
                support[
                    "support_energy_floor_j"
                ]
            ),

        "partial_conservative_floor_j":
            total,

        "limiting_surface_cosine":
            float(
                requirement[
                    "limiting_surface_cosine"
                ]
            ),
    }


scale_optimization = minimize_scalar(
    lambda scale:
        evaluate_sphere_scale(
            scale,
            surface_count=801,
        )[
            "partial_conservative_floor_j"
        ],

    bounds=(
        1.0e4,
        1.0e5,
    ),

    method=
        "bounded",

    options={
        "xatol":
            1.0e-5,
    },
)


optimal_scale_ev = float(
    scale_optimization.x
)

optimal = evaluate_sphere_scale(
    optimal_scale_ev,
    surface_count=1601,
)

optimal_l28 = evaluate_sphere_scale(
    optimal_scale_ev,
    coefficients=
        sphere_coefficients_l28,
    surface_count=1601,
)

multipole_relerr = (
    abs(
        float(
            optimal_l28[
                "q2"
            ]
        )
        - float(
            optimal[
                "q2"
            ]
        )
    )
    /
    float(
        optimal[
            "q2"
        ]
    )
)

assert (
    multipole_relerr
    < 2.0e-8
)


optimal_energy_j = float(
    optimal[
        "partial_conservative_floor_j"
    ]
)

assert (
    optimal_energy_j
    < TARGET_J
)


# ============================================================
# 8. FINITE PAYLOAD / REACTION
# ============================================================

surface = (
    payload_surface_acceleration_metrics(
        coefficients=
            sphere_coefficients,

        epsilon_trace_load=
            float(
                optimal[
                    "epsilon_trace_load"
                ]
            ),

        payload_radius_m=
            PAYLOAD_RADIUS_M,

        q2=
            float(
                optimal[
                    "q2"
                ]
            ),

        surface_count=
            1601,
    )
)

payload_cm_20 = (
    payload_volume_average_acceleration_m_s2(
        coefficients=
            sphere_coefficients,

        epsilon_trace_load=
            float(
                optimal[
                    "epsilon_trace_load"
                ]
            ),

        payload_radius_m=
            PAYLOAD_RADIUS_M,

        q2=
            float(
                optimal[
                    "q2"
                ]
            ),

        order=
            20,
    )
)

payload_cm_24 = (
    payload_volume_average_acceleration_m_s2(
        coefficients=
            sphere_coefficients,

        epsilon_trace_load=
            float(
                optimal[
                    "epsilon_trace_load"
                ]
            ),

        payload_radius_m=
            PAYLOAD_RADIUS_M,

        q2=
            float(
                optimal[
                    "q2"
                ]
            ),

        order=
            24,
    )
)

payload_cm_relerr = (
    abs(
        payload_cm_24
        - payload_cm_20
    )
    /
    payload_cm_24
)

assert (
    float(
        surface[
            "surface_min_m_s2"
        ]
    )
    >= G
    * (
        1.0
        - 2.0e-12
    )
)

assert (
    payload_cm_24
    >= G
)

assert (
    payload_cm_relerr
    < 1.0e-9
)


feedback = (
    source_feedback_metrics(
        coefficients=
            sphere_coefficients,

        epsilon_trace_load=
            float(
                optimal[
                    "epsilon_trace_load"
                ]
            ),

        payload_radius_m=
            PAYLOAD_RADIUS_M,

        payload_center_z_m=
            PAYLOAD_CENTER_Z_M,

        source_a_m=
            SOURCE_RADIUS_M,

        source_c_m=
            SOURCE_RADIUS_M,

        source_demag_z=
            SPHERE_DEMAG_Z,

        surface_count=
            401,
    )
)

assert (
    float(
        feedback[
            "source_surface_max_feedback_ratio"
        ]
    )
    < 0.03
)


# ============================================================
# 9. PHYSICALIZE SPHERICAL SOURCE / QUANTUM CONTROL
# ============================================================

sphere_flavors = max(
    1,
    int(
        math.ceil(
            sphere_nf_continuous
        )
    ),
)

assert (
    sphere_flavors
    <= MAX_FLAVORS
)


physical_source = (
    physicalize_dimensionless_state(
        q=
            float(
                optimal[
                    "q"
                ]
            ),

        metric_scale_ev=
            optimal_scale_ev,

        demag_z=
            SPHERE_DEMAG_Z,

        r_mass_over_b=
            sphere_r,

        u_mu_over_b=
            sphere_u,

        flavors=
            sphere_flavors,

        order=
            96,
    )
)


sphere_leading_log = (
    axial_leading_log_wavefunction_proxy(
        loop_proxy=
            sphere_loop,

        cutoff_ev=
            float(
                physical_source[
                    "nda_cutoff_ev"
                ]
            ),

        mass_ev=
            float(
                physical_source[
                    "m_psi_ev"
                ]
            ),
    )
)

assert (
    sphere_leading_log
    > 1.0
)


optimal_c1 = (
    c1_from_metric_scale_ev(
        optimal_scale_ev
    )
)

optimal_jiang_nda_ev = (
    jiang_nda_scale_from_c1_ev(
        optimal_c1
    )
)


# ============================================================
# 10. EMPIRICAL / UV INTERPRETATION
# ============================================================

# A published universal derivative-conformal model has been constrained with
# collider data in a contact-EFT interpretation at scales of order hundreds of
# GeV. That number is NOT directly transferred here because the present EFT
# cutoff is many orders of magnitude below collider hard energies.
#
# This does not make the candidate empirically safe.
#
# It makes an explicit low-scale UV completion and its laboratory/stellar/
# cosmological phenomenology mandatory.

empirical_uv = {
    "published_universal_derivative_conformal_collider_context":
        True,

    "specific_model_constraint_scale_order_ev":
        2.0e11,

    "candidate_low_energy_metric_scale_ev":
        optimal_scale_ev,

    "candidate_jiang_nda_scale_ev":
        optimal_jiang_nda_ev,

    "contact_eft_constraint_directly_transferable":
        False,

    "reason_not_directly_transferable":
        "CANDIDATE_EFT_BREAKS_DOWN_FAR_BELOW_COLLIDER_HARD_ENERGY",

    "candidate_empirically_closed":
        False,

    "explicit_low_scale_uv_completion_required":
        True,
}


# ============================================================
# 11. SCALE SCAN
# ============================================================

scale_rows: list[
    dict[str, object]
] = []

for scale_ev in (
    1.0e5,
    8.0e4,
    5.0e4,
    4.0e4,
    3.0e4,
    optimal_scale_ev,
    2.0e4,
    1.5e4,
    1.0e4,
):
    state = evaluate_sphere_scale(
        scale_ev,
        surface_count=1201,
    )

    scale_rows.append(
        {
            **state,

            "c1_ev_m4":
                c1_from_metric_scale_ev(
                    scale_ev
                ),

            "under_strict_10mj_partial_only":
                float(
                    state[
                        "partial_conservative_floor_j"
                    ]
                )
                < TARGET_J,

            "complete_operating_ledger":
                False,

            "trusted_energy_oracle":
                False,
        }
    )


# ============================================================
# 12. OBLATE VS SPHERE FRONTIER
# ============================================================

oblate_energy_j = float(
    v17[
        "exact_payload"
    ][
        "partial_energy_j"
    ]
)

comparison_rows = [
    {
        "architecture":
            "V17_OBLATE",

        "partial_energy_j":
            oblate_energy_j,

        "minimal_isotropic_bag_shape_compatible":
            False,

        "loop_proxy":
            float(
                v17[
                    "axial_quantum_control"
                ][
                    "selected_loop_proxy"
                ]
            ),

        "fixed_order_canonicalization_control":
            False,

        "support_realization":
            "OPEN_ANISOTROPIC",
    },
    {
        "architecture":
            "V18_SPHERE",

        "partial_energy_j":
            optimal_energy_j,

        "minimal_isotropic_bag_shape_compatible":
            True,

        "loop_proxy":
            sphere_loop,

        "fixed_order_canonicalization_control":
            False,

        "support_realization":
            "LOWER_BOUND_ONLY_BAG_NOT_CONSTRUCTED",
    },
]


# ============================================================
# 13. AGMINER MEMORY
# ============================================================

storage = Storage(
    DB
)


reuse_candidate = Candidate(
    family_id=
        "032_KINETIC_CONFORMAL_SPHERICAL_AXIAL_SOURCE",

    family_version=
        "V18_NAIVE_OBLATE_STATE_REUSE_V1",

    params={
        "r_mass_over_b":
            old_r,

        "u_mu_over_b":
            old_u,

        "sphere_demag_z":
            SPHERE_DEMAG_Z,

        "resulting_loop_proxy":
            naive_sphere_loop,
    },

    physical_model_version=
        "SPHERE_WITH_UNREOPTIMIZED_OBLATE_MICROSTATE",

    energy_ledger_version=
        "LOOP_REMAP_ANALYTIC_GATE_V1",
)

storage.record_candidate(
    reuse_candidate,

    state=
        "TIER0_RUNNING",

    tier=
        0,

    run_id=
        "032V18",
)

storage.reject(
    reuse_candidate.candidate_id,

    state=
        "REJECTED_NATURALNESS",

    failure_code=
        "N007",

    gate=
        "sphere_geometry_demag_loop_remap",

    energy_j=
        None,

    run_id=
        "032V18",
)


fixed_order_candidate = Candidate(
    family_id=
        "032_KINETIC_CONFORMAL_SPHERICAL_AXIAL_SOURCE",

    family_version=
        "V18_SPHERE_LOOP030_FIXED_ORDER_V1",

    params={
        "loop_proxy":
            sphere_loop,

        "leading_log_delta_z_proxy":
            sphere_leading_log,

        "metric_scale_ev":
            optimal_scale_ev,
    },

    physical_model_version=
        "SPHERICAL_MEANFIELD_FIXED_ORDER_RUNNING",

    energy_ledger_version=
        "QUANTUM_CONTROL_GATE_ONLY_V1",
)

storage.record_candidate(
    fixed_order_candidate,

    state=
        "TIER0_RUNNING",

    tier=
        0,

    run_id=
        "032V18",
)

storage.reject(
    fixed_order_candidate.candidate_id,

    state=
        "REJECTED_NATURALNESS",

    failure_code=
        "N008",

    gate=
        "sphere_fixed_order_wavefunction_running_control",

    energy_j=
        optimal_energy_j,

    run_id=
        "032V18",
)


sphere_candidate = Candidate(
    family_id=
        "032_KINETIC_CONFORMAL_SPHERICAL_SUPPORT_READY",

    family_version=
        "V18_LOOP030_EXACT_PAYLOAD_V1",

    params={
        "metric_scale_ev":
            optimal_scale_ev,

        "q":
            float(
                optimal[
                    "q"
                ]
            ),

        "loop_proxy":
            sphere_loop,

        "flavors":
            sphere_flavors,

        "source_radius_m":
            SOURCE_RADIUS_M,

        "payload_radius_m":
            PAYLOAD_RADIUS_M,
    },

    physical_model_version=
        "UNIVERSAL_METRIC_SPHERICAL_AXIAL_MEANFIELD_PREFIELD",

    energy_ledger_version=
        "BAND_FIELD_ANISOTROPIC_DEC_SUPPORT_FLOOR_PAYLOAD_V1",
)

storage.record_candidate(
    sphere_candidate,

    state=
        "PREFIELD_SUPPORT_READY_UV_BLOCKED",

    tier=
        0,

    run_id=
        "032V18",
)


canonical_id = (
    canonical_invariant_fingerprint(
        family_id=
            sphere_candidate.family_id,

        family_version=
            sphere_candidate.family_version,

        invariants={
            "universal_metric":
                "A_OF_X_JORDAN_METRIC",

            "outward_operator":
                "C1_POSITIVE",

            "canonical_invariant":
                "C1_TIMES_F_SQUARED",

            "source_geometry":
                "SPHERE",

            "loop_proxy":
                sphere_loop,

            "renormalized_uv_matching":
                False,
        },
    )
)


oracle = ActionOracle(
    canonical_invariant_id=
        canonical_id,

    proof_reference=
        "032V18_SPHERE_EXACT_PAYLOAD_ANISOTROPIC_DEC_SUPPORT_FLOOR",

    relaxed_complete_energy_j=
        optimal_energy_j,

    ledger_scope=
        LEDGER_PARTIAL_OPTIMISTIC,

    normalization_invariant=
        False,

    naturalness_screened=
        False,

    universal_metric_screened=
        True,
)


assessment = (
    assess_oracle(
        oracle
    )
)

assert (
    oracle.trusted_for_reachability
    is False
)

storage.record_action_oracle(
    sphere_candidate.candidate_id,
    oracle,
)


reporting = rebuild_summaries(
    storage,
    ROOT
    / "results"
    / "agminer",
)

storage.close()


# ============================================================
# 14. OUTPUTS
# ============================================================

with SPHERE_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=
            list(
                scale_rows[
                    0
                ].keys()
            ),
    )

    writer.writeheader()
    writer.writerows(
        scale_rows
    )


with COMPARE_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=
            list(
                comparison_rows[
                    0
                ].keys()
            ),
    )

    writer.writeheader()
    writer.writerows(
        comparison_rows
    )


decision = (
    "GREEN_UNIVERSAL_KINETIC_CONFORMAL_METRIC_PROVENANCE_"
    "GREEN_SUPPORT_FRIENDLY_SPHERE_PARTIAL_LT10MJ_"
    "RED_FIXED_ORDER_RG_CONTROL_"
    "UV_EMPIRICAL_AND_BAG_REALIZATION_REQUIRED"
)

next_step = (
    "032V19_SPHERICAL_BAG_SUPPORT_UV_MATCHING_AND_EMPIRICAL_GATE"
)


summary = {
    "branch":
        "032V18_C1_UV_MATCHING_RG_AND_COMPLETE_SOURCE_SUPPORT_GATE",

    "claim_class":
        "UNIVERSAL_METRIC_PROVENANCE_RG_INVARIANT_AND_SUPPORT_READY_PREFLIGHT",

    "energy_policy_id":
        str(
            policy[
                "policy_id"
            ]
        ),

    "provenance":
        provenance,

    "canonicalization":
        {
            **canonical_status,

            "rescaling_demo":
                rescaling_demo,
        },

    "support_geometry": {
        "v17_oblate_minimal_isotropic_bag_compatible":
            oblate_minimal_isotropic_bag,

        "sphere_minimal_isotropic_bag_compatible":
            sphere_minimal_isotropic_bag,

        "physical_bag_constructed":
            False,

        "constant_pressure_tension_solution_constructed":
            False,
    },

    "no_shortcut": {
        "v16_oblate_state_loop_proxy":
            float(
                old_selected[
                    "loop_proxy"
                ]
            ),

        "same_state_in_sphere_loop_proxy":
            naive_sphere_loop,

        "same_state_preserves_loop030":
            False,

        "decision":
            "REOPTIMIZATION_REQUIRED",
    },

    "sphere_meanfield": {
        "source_radius_m":
            SOURCE_RADIUS_M,

        "source_demag_z":
            SPHERE_DEMAG_Z,

        "r_mass_over_b":
            sphere_r,

        "u_mu_over_b":
            sphere_u,

        "loop_proxy":
            sphere_loop,

        "fixed_density_susceptibility_hat":
            sphere_susceptibility[
                "susceptibility_hat"
            ],

        "susceptibility_to_current_ratio":
            sphere_susceptibility[
                "susceptibility_to_current_ratio"
            ],

        "minimum_flavors_continuous_for_margin5":
            sphere_nf_continuous,

        "selected_flavors":
            sphere_flavors,

        "reference_100kev_partial_floor_j":
            sphere_reference_total,
    },

    "sphere_exact_payload_optimum": {
        **optimal,

        "multipole_l28_l32_q2_relerr":
            multipole_relerr,

        "surface_min_m_s2":
            surface[
                "surface_min_m_s2"
            ],

        "surface_max_m_s2":
            surface[
                "surface_max_m_s2"
            ],

        "surface_nonuniformity":
            surface[
                "surface_nonuniformity"
            ],

        "payload_cm_volume_average_m_s2":
            payload_cm_24,

        "payload_cm_quadrature_relerr":
            payload_cm_relerr,

        "source_center_feedback_ratio":
            feedback[
                "source_center_feedback_ratio"
            ],

        "source_surface_max_feedback_ratio":
            feedback[
                "source_surface_max_feedback_ratio"
            ],

        "remaining_to_strict_10mj_j":
            TARGET_J
            - optimal_energy_j,

        "complete_operating_ledger":
            False,

        "trusted_energy_oracle":
            False,
    },

    "sphere_physical_source": {
        "flavors":
            sphere_flavors,

        "f_psi_ev":
            physical_source[
                "f_psi_ev"
            ],

        "axial_b_ev":
            physical_source[
                "axial_b_ev"
            ],

        "m_psi_ev":
            physical_source[
                "m_psi_ev"
            ],

        "chemical_potential_ev":
            physical_source[
                "chemical_potential_ev"
            ],

        "nda_cutoff_ev":
            physical_source[
                "nda_cutoff_ev"
            ],

        "hard_scale_margin":
            physical_source[
                "hard_scale_margin"
            ],

        "leading_log_delta_z_proxy":
            sphere_leading_log,

        "fixed_order_canonicalization_control":
            False,
    },

    "outward_operator": {
        "c1_ev_m4":
            optimal_c1,

        "jiang_nda_scale_ev":
            optimal_jiang_nda_ev,

        "universal_metric_action_level":
            True,

        "outward_universal_uv_completion":
            False,
    },

    "empirical_uv":
        empirical_uv,

    "frontier_comparison":
        comparison_rows,

    "open_gates": [
        "RENORMALIZED_RG_OR_UV_MATCHED_CANONICAL_PARAMETERS",
        "OUTWARD_C1_UNIVERSAL_UV_COMPLETION",
        "PHYSICAL_POSITIVE_ENERGY_BAG_OR_ANISOTROPIC_SUPPORT",
        "BAG_WALL_ENERGY",
        "FULL_COUPLED_SOURCE_PAYLOAD_REACTION",
        "ACTIVATION_AND_RESET",
        "NONLINEAR_STABILITY",
        "RADIATION",
        "LABORATORY_COLLIDER_STELLAR_COSMOLOGICAL_EMPIRICAL_CLOSURE",
        "FULL_METRIC_BACKREACTION",
    ],

    "agminer": {
        "naive_sphere_reuse_rejection_candidate_id":
            reuse_candidate.candidate_id,

        "sphere_fixed_order_rejection_candidate_id":
            fixed_order_candidate.candidate_id,

        "sphere_partial_oracle_candidate_id":
            sphere_candidate.candidate_id,

        "sphere_oracle_priority":
            assessment.priority,

        "sphere_oracle_trusted_for_reachability":
            False,

        "mechanism_metrics_recorded":
            False,

        "reporting":
            reporting,
    },

    "physical_antigravity_model_found":
        False,

    "certified_sub10mj_model_found":
        False,

    "decision":
        decision,

    "next":
        next_step,
}


OUT.write_text(
    json.dumps(
        summary,
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
)


# ============================================================
# 15. TERMINAL SUMMARY
# ============================================================

print(
    "=== 032V18 RESULT ==="
)

print(
    "ENERGY_POLICY_ID="
    + str(
        policy[
            "policy_id"
        ]
    )
)

print(
    "PUBLISHED_UNIVERSAL_KINETIC_CONFORMAL_METRIC=YES"
)

print(
    "JIANG_C1_ALONE_PROVES_UNIVERSAL_METRIC=False"
)

print(
    "PUBLISHED_FRAMEWORK_REPULSIVE_RESPONSE_EXISTS=YES"
)

print(
    "OUTWARD_SIGN_UNIVERSAL_UV_COMPLETION_PROVED=False"
)

print(
    "C1_F2_CANONICAL_RESCALING_INVARIANT=True"
)

print(
    "DELTAZ_IS_AUTOMATIC_ENERGY_MULTIPLIER=False"
)

print(
    "RG_MATCHED_LOW_ENERGY_EFT=OPEN"
)

print(
    "V17_OBLATE_MINIMAL_ISOTROPIC_BAG_COMPATIBLE=False"
)

print(
    "SPHERE_MINIMAL_ISOTROPIC_BAG_COMPATIBLE=True"
)

print(
    "NAIVE_SPHERE_REUSE_LOOP_PROXY="
    + format(
        naive_sphere_loop,
        ".12e",
    )
)

print(
    "NAIVE_SPHERE_REUSE_LOOP030=RED"
)

print(
    "SPHERE_OPT_R_MASS_OVER_B="
    + format(
        sphere_r,
        ".12e",
    )
)

print(
    "SPHERE_OPT_U_MU_OVER_B="
    + format(
        sphere_u,
        ".12e",
    )
)

print(
    "SPHERE_LOOP_PROXY="
    + format(
        sphere_loop,
        ".12e",
    )
)

print(
    "SPHERE_NF="
    + str(
        sphere_flavors
    )
)

print(
    "SPHERE_100KEV_PARTIAL_MJ="
    + format(
        sphere_reference_total
        / 1.0e6,
        ".12e",
    )
)

print(
    "SPHERE_EXACT_OPTIMUM_SCALE_KEV="
    + format(
        optimal_scale_ev
        / 1.0e3,
        ".12e",
    )
)

print(
    "SPHERE_EXACT_OPTIMUM_EPSILON="
    + format(
        float(
            optimal[
                "epsilon_trace_load"
            ]
        ),
        ".12e",
    )
)

print(
    "SPHERE_EXACT_Q2_FACTOR="
    + format(
        float(
            optimal[
                "q2_factor_from_vacuum"
            ]
        ),
        ".12e",
    )
)

print(
    "SPHERE_PARTIAL_MJ="
    + format(
        optimal_energy_j
        / 1.0e6,
        ".12e",
    )
)

print(
    "SPHERE_FIELD_KJ="
    + format(
        float(
            optimal[
                "field_energy_j"
            ]
        )
        / 1.0e3,
        ".12e",
    )
)

print(
    "SPHERE_OCCUPIED_BAND_MJ="
    + format(
        float(
            optimal[
                "occupied_band_energy_j"
            ]
        )
        / 1.0e6,
        ".12e",
    )
)

print(
    "SPHERE_DEC_SUPPORT_FLOOR_MJ="
    + format(
        float(
            optimal[
                "support_energy_floor_j"
            ]
        )
        / 1.0e6,
        ".12e",
    )
)

print(
    "SPHERE_REMAINING_TO_10MJ_MJ="
    + format(
        (
            TARGET_J
            - optimal_energy_j
        )
        / 1.0e6,
        ".12e",
    )
)

print(
    "SPHERE_SURFACE_MIN_M_S2="
    + format(
        float(
            surface[
                "surface_min_m_s2"
            ]
        ),
        ".12e",
    )
)

print(
    "SPHERE_SURFACE_MAX_M_S2="
    + format(
        float(
            surface[
                "surface_max_m_s2"
            ]
        ),
        ".12e",
    )
)

print(
    "SPHERE_SURFACE_NONUNIFORMITY="
    + format(
        float(
            surface[
                "surface_nonuniformity"
            ]
        ),
        ".12e",
    )
)

print(
    "SPHERE_PAYLOAD_CM_M_S2="
    + format(
        payload_cm_24,
        ".12e",
    )
)

print(
    "SPHERE_SOURCE_SURFACE_FEEDBACK="
    + format(
        float(
            feedback[
                "source_surface_max_feedback_ratio"
            ]
        ),
        ".12e",
    )
)

print(
    "SPHERE_F_PSI_EV="
    + format(
        float(
            physical_source[
                "f_psi_ev"
            ]
        ),
        ".12e",
    )
)

print(
    "SPHERE_M_PSI_EV="
    + format(
        float(
            physical_source[
                "m_psi_ev"
            ]
        ),
        ".12e",
    )
)

print(
    "SPHERE_MU_PSI_EV="
    + format(
        float(
            physical_source[
                "chemical_potential_ev"
            ]
        ),
        ".12e",
    )
)

print(
    "SPHERE_SOURCE_CUTOFF_EV="
    + format(
        float(
            physical_source[
                "nda_cutoff_ev"
            ]
        ),
        ".12e",
    )
)

print(
    "SPHERE_SOURCE_HARD_MARGIN="
    + format(
        float(
            physical_source[
                "hard_scale_margin"
            ]
        ),
        ".12e",
    )
)

print(
    "SPHERE_LEADING_LOG_DELTAZ_PROXY="
    + format(
        sphere_leading_log,
        ".12e",
    )
)

print(
    "SPHERE_FIXED_ORDER_CANONICALIZATION_CONTROL=RED"
)

print(
    "V17_OBLATE_PARTIAL_KJ="
    + format(
        oblate_energy_j
        / 1.0e3,
        ".12e",
    )
)

print(
    "V17_OBLATE_PARTIAL_STILL_ALIVE=True"
)

print(
    "V17_OBLATE_SUPPORT_REALIZATION=OPEN_ANISOTROPIC"
)

print(
    "SPECIFIC_COLLIDER_CONTACT_BOUND_DIRECTLY_TRANSFERABLE=False"
)

print(
    "LOW_SCALE_UV_EMPIRICAL_CLOSURE=MANDATORY"
)

print(
    "PHYSICAL_BAG_SUPPORT_CONSTRUCTED=NO"
)

print(
    "PHYSICAL_ANTIGRAVITY_MODEL_FOUND=NO"
)

print(
    "CERTIFIED_SUB10MJ_MODEL_FOUND=NO"
)

print(
    "DECISION="
    + decision
)

print(
    "NEXT="
    + next_step
)
