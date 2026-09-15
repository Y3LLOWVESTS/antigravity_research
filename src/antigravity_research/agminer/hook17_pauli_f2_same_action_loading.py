"""032H17A12D1 — same-action finite-matter loading and Pauli overlap gate.

PURPOSE
-------
Test a missing same-action consistency condition in the frozen
A12B + A12C + A12D0 backbone before authorizing another BVP or attempting
detailed Pauli UV engineering.

SCIENTIFIC QUESTION
-------------------
A12C used the universal physical metric

    g_phys(mu,nu) = exp(2*sigma) g(mu,nu)

with

    sigma = F_X^2 / (2 M_X^4).

Its finite-payload field solve explicitly did not include loaded matter
backreaction.

The question here is:

    When the same universal matter action is varied with respect to X_mu,
    how strongly does the finite payload itself load the X-field equation?

This gate then asks whether the existing optimistic electron-Pauli
sub-10-MJ source corridor overlaps even a necessary condition for weak
payload loading.

SAME-ACTION VARIATION
---------------------
Using

    delta S_m
        =
    int sqrt(-g_phys) T_phys delta_sigma

and

    delta sigma
        =
    2 F_X^(mu nu) nabla_mu(delta X_nu) / M_X^4,

the vector equation contains

    nabla_mu[
        (
            1
            -
            2 exp(4 sigma) T_phys / M_X^4
        )
        F_X^(mu nu)
    ]
    =
    J_X^nu

up to the declared current-sign convention.

For nonrelativistic massive matter in mostly-plus signature,

    T_phys ~= -rho_E,

where rho_E is the local rest-energy density.

At quadratic order about the off state,

    Z_matter
        =
    1 + 2 rho_E / M_X^4.

An independent nonrelativistic matter-action expansion gives

    L_m
        ~= -rho_E exp(sigma)

and therefore

    L_quad
        =
    -(1/4)
    (
        1 + 2 rho_E/M_X^4
    )
    F_X^2.

Thus the factor of two and the magnitude of the matter loading have two
independent derivations.

DISTRIBUTION-INDEPENDENT DENSITY BOUND
--------------------------------------
A12C specifies:

    payload mass       = 1 kg
    torus major radius = 1.0 m
    torus minor radius = 0.2 m.

For any nonnegative matter-density distribution occupying that finite torus,

    max(rho_E) >= average(rho_E).

Therefore

    max(epsilon_load)
        >=
    2 average(rho_E) / M_X^4.

This run uses only that lower bound.

Consequently:

- if the average-density lower bound already exceeds one, globally weak
  loading is impossible;

- if the lower bound is below one, weak loading is merely NOT RULED OUT.
  It is not proved, because a nonuniform payload has a larger local maximum.

This distinction is permanent and intentional.

SCIENTIFIC SCOPE
----------------
This is an analytic theorem/scale-overlap gate.

It does not rerun the A12C BVP.

A red result closes only:

    minimal electron Pauli source
    +
    perturbative/unloaded A12C-kernel reuse
    +
    strict sub-10-MJ partial energy.

It does not close:

- A12B's exact protected massless carrier;
- the gauge-invariant conformal F_X^2 metric mechanism;
- a genuinely loaded nonlinear solution;
- composite magnetization;
- bound/interacting Dirac matter;
- flavor-selective currents;
- other A12D0 completions;
- HOOK17 globally.

Likewise, a surviving loading-controlled portal interval is only a target
window for future source physicalization. It is not a physical model.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_SAME_ACTION_LOADING_AND_SCALE_OVERLAP_GATE
"""

from __future__ import annotations

import math
from functools import lru_cache
from typing import Any

from .hook17_concurrent_u1_fieldstrength_metric import (
    C_LIGHT_M_S,
    EV_J,
    HBAR_C_EV_M,
    PAYLOAD_MAJOR_RADIUS_M,
    PAYLOAD_MASS_KG,
    PAYLOAD_MINOR_RADIUS_M,
    STRICT_COMPLETE_OPERATING_TARGET_J,
)
from .hook17_pauli_f2_source_reopen import (
    a12c_artifact,
    pauli_geometry_gate,
    provenance_gate as pauli_provenance_gate,
    source_energy_at_portal_scale,
    strict_partial_energy_boundary,
)


LOADING_EPSILON_ORDER_ONE = 1.0
LOADING_EPSILON_TEN_PERCENT = 0.1
LOADING_EPSILON_ONE_PERCENT = 0.01


def payload_torus_volume_m3() -> float:
    """Return geometric volume of the frozen A12C toroidal payload."""

    return (
        2.0
        *
        math.pi**2
        *
        PAYLOAD_MAJOR_RADIUS_M
        *
        PAYLOAD_MINOR_RADIUS_M**2
    )


def one_ev4_j_m3() -> float:
    """Return SI energy density represented by one natural-unit eV^4."""

    return (
        EV_J
        /
        HBAR_C_EV_M**3
    )


@lru_cache(maxsize=1)
def payload_average_density_gate() -> dict[str, Any]:
    """Return average rest-energy density and its rigorous local implication."""

    volume_m3 = (
        payload_torus_volume_m3()
    )

    average_mass_density_kg_m3 = (
        PAYLOAD_MASS_KG
        /
        volume_m3
    )

    average_rest_energy_density_j_m3 = (
        average_mass_density_kg_m3
        *
        C_LIGHT_M_S**2
    )

    average_rest_energy_density_ev4 = (
        average_rest_energy_density_j_m3
        /
        one_ev4_j_m3()
    )

    return {
        "payload_mass_kg":
            PAYLOAD_MASS_KG,

        "payload_major_radius_m":
            PAYLOAD_MAJOR_RADIUS_M,

        "payload_minor_radius_m":
            PAYLOAD_MINOR_RADIUS_M,

        "payload_geometric_volume_m3":
            volume_m3,

        "average_payload_mass_density_kg_m3":
            average_mass_density_kg_m3,

        "average_payload_rest_energy_density_j_m3":
            average_rest_energy_density_j_m3,

        "one_ev4_j_m3":
            one_ev4_j_m3(),

        "average_payload_rest_energy_density_ev4":
            average_rest_energy_density_ev4,

        "nonnegative_density_implies_max_ge_average":
            True,

        "bound_interpretation":
            (
                "AVERAGE_DENSITY_GIVES_A_RIGOROUS_LOWER_BOUND_"
                "ON_MAXIMUM_LOCAL_MATTER_LOADING"
            ),

        "weak_loading_if_bound_passes_is_sufficient":
            False,
    }


@lru_cache(maxsize=1)
def same_action_variation_gate() -> dict[str, Any]:
    """Record exact variation and independent quadratic reconstruction."""

    return {
        "physical_metric":
            "g_phys=exp(2*sigma)*g",

        "sigma":
            "F_X^2/(2*M_X^4)",

        "matter_variation":
            (
                "deltaS_m="
                "int[sqrt(-g_phys)*T_phys*delta_sigma]"
            ),

        "delta_sigma":
            (
                "2*F_X^(mu_nu)*"
                "nabla_mu(deltaX_nu)/M_X^4"
            ),

        "same_action_vector_equation":
            (
                "nabla_mu["
                "(1-2*exp(4*sigma)*T_phys/M_X^4)"
                "*F_X^(mu_nu)"
                "]=J_X^nu"
            ),

        "mostly_plus_nonrelativistic_trace":
            "T_phys~-rho_E",

        "off_state_quadratic_kinetic_factor":
            "Z_matter=1+2*rho_E/M_X^4",

        "loading_parameter":
            "epsilon_load=2*rho_E/M_X^4",

        "independent_nr_matter_expansion":
            "L_m~-rho_E-rho_E*F_X^2/(2*M_X^4)",

        "independent_total_quadratic_lagrangian":
            (
                "L_quad="
                "-(1/4)*(1+2*rho_E/M_X^4)*F_X^2"
            ),

        "factor_two_independently_reconstructed":
            True,

        "finite_matter_quadratic_loading_present":
            True,

        "metric_portal_has_linear_off_state_source":
            False,
    }


def maximum_local_loading_lower_bound(
    portal_scale_ev: float,
) -> dict[str, Any]:
    """Return rigorous lower bound on maximum local payload loading."""

    scale_ev = float(
        portal_scale_ev
    )

    if scale_ev <= 0.0:
        raise ValueError(
            "portal_scale_ev must be positive"
        )

    average_rho_ev4 = float(
        payload_average_density_gate()[
            "average_payload_rest_energy_density_ev4"
        ]
    )

    epsilon_lower_bound = (
        2.0
        *
        average_rho_ev4
        /
        scale_ev**4
    )

    return {
        "portal_scale_ev":
            scale_ev,

        "maximum_local_epsilon_load_lower_bound":
            epsilon_lower_bound,

        "maximum_local_quadratic_z_lower_bound":
            (
                1.0
                +
                epsilon_lower_bound
            ),

        "global_loading_le_1_not_ruled_out":
            epsilon_lower_bound
            <=
            LOADING_EPSILON_ORDER_ONE,

        "global_loading_le_0p1_not_ruled_out":
            epsilon_lower_bound
            <=
            LOADING_EPSILON_TEN_PERCENT,

        "global_loading_le_0p01_not_ruled_out":
            epsilon_lower_bound
            <=
            LOADING_EPSILON_ONE_PERCENT,

        "bound_is_necessary_not_sufficient":
            True,
    }


def necessary_portal_scale_for_global_loading_bound(
    epsilon_max: float,
) -> float:
    """Return necessary M_X scale for max loading to possibly stay below epsilon."""

    epsilon = float(
        epsilon_max
    )

    if epsilon <= 0.0:
        raise ValueError(
            "epsilon_max must be positive"
        )

    average_rho_ev4 = float(
        payload_average_density_gate()[
            "average_payload_rest_energy_density_ev4"
        ]
    )

    return (
        2.0
        *
        average_rho_ev4
        /
        epsilon
    ) ** 0.25


@lru_cache(maxsize=1)
def a12c_reference_gate() -> dict[str, Any]:
    """Load authoritative frozen A12C probe-limit reference quantities."""

    a12c = (
        a12c_artifact()
    )

    production = (
        a12c[
            "massless_f2_finite_payload_bvp"
        ][
            "production"
        ]
    )

    reference_scale_ev = float(
        production[
            "reference_portal_scale_ev"
        ]
    )

    reference_field_energy_j = float(
        production[
            "field_energy_j"
        ]
    )

    reference_source_ev_m = float(
        production[
            "integrated_canonical_source_ev_m"
        ]
    )

    field_only_10mj_scale_ev = (
        reference_scale_ev
        *
        (
            STRICT_COMPLETE_OPERATING_TARGET_J
            /
            reference_field_energy_j
        ) ** 0.25
    )

    return {
        "reference_portal_scale_ev":
            reference_scale_ev,

        "reference_field_energy_j":
            reference_field_energy_j,

        "reference_integrated_canonical_source_ev_m":
            reference_source_ev_m,

        "reference_payload_sigma_max":
            float(
                production[
                    "payload_sigma_max"
                ]
            ),

        "loaded_matter_backreaction_included":
            bool(
                production[
                    "loaded_matter_backreaction_included"
                ]
            ),

        "field_only_strict_10mj_portal_scale_ev":
            field_only_10mj_scale_ev,

        "reference_is_probe_limit_unloaded_payload":
            not bool(
                production[
                    "loaded_matter_backreaction_included"
                ]
            ),
    }


def unloaded_reference_scaling_at_portal_scale(
    portal_scale_ev: float,
) -> dict[str, float]:
    """Scale frozen UNLOADED A12C reference; this is not a loaded solution."""

    scale_ev = float(
        portal_scale_ev
    )

    if scale_ev <= 0.0:
        raise ValueError(
            "portal_scale_ev must be positive"
        )

    reference = (
        a12c_reference_gate()
    )

    reference_scale_ev = float(
        reference[
            "reference_portal_scale_ev"
        ]
    )

    ratio = (
        scale_ev
        /
        reference_scale_ev
    )

    field_energy_j = (
        float(
            reference[
                "reference_field_energy_j"
            ]
        )
        *
        ratio**4
    )

    source_ev_m = (
        float(
            reference[
                "reference_integrated_canonical_source_ev_m"
            ]
        )
        *
        ratio**2
    )

    return {
        "portal_scale_ev":
            scale_ev,

        "unloaded_reference_field_energy_j":
            field_energy_j,

        "unloaded_reference_integrated_source_ev_m":
            source_ev_m,

        "field_only_headroom_to_10mj_j":
            (
                STRICT_COMPLETE_OPERATING_TARGET_J
                -
                field_energy_j
            ),
    }


@lru_cache(maxsize=1)
def provenance_gate() -> dict[str, Any]:
    """Require correct A12C/A12D handoff and confirm missing loading."""

    pauli_provenance = (
        pauli_provenance_gate()
    )

    a12c = (
        a12c_artifact()
    )

    production = (
        a12c[
            "massless_f2_finite_payload_bvp"
        ][
            "production"
        ]
    )

    loaded_backreaction = bool(
        production[
            "loaded_matter_backreaction_included"
        ]
    )

    passed = bool(
        pauli_provenance[
            "pass"
        ]
        is True

        and

        a12c[
            "branch"
        ]
        ==
        "032H17A12C"

        and

        a12c[
            "gauge_invariant_massless_f2_reduced_eft_1g_1m_witness"
        ]
        is True

        and

        a12c[
            "a12b_exact_massless_carrier_closed"
        ]
        is False

        and

        loaded_backreaction
        is False
    )

    return {
        "pass":
            passed,

        "upstream_pauli_provenance_pass":
            pauli_provenance[
                "pass"
            ],

        "a12c_branch":
            a12c[
                "branch"
            ],

        "a12c_loaded_matter_backreaction_included":
            loaded_backreaction,

        "a12c_payload_sigma_max":
            float(
                production[
                    "payload_sigma_max"
                ]
            ),

        "source_shape_reuse_preserved":
            True,

        "same_action_loaded_kernel_reuse_established":
            False,
    }


@lru_cache(maxsize=1)
def controlled_portal_window_gate() -> dict[str, Any]:
    """Derive optimistic source-independent portal intervals after loading bound."""

    reference = (
        a12c_reference_gate()
    )

    field_upper_ev = float(
        reference[
            "field_only_strict_10mj_portal_scale_ev"
        ]
    )

    thresholds = (
        (
            "ORDER_ONE",
            LOADING_EPSILON_ORDER_ONE,
        ),
        (
            "TEN_PERCENT",
            LOADING_EPSILON_TEN_PERCENT,
        ),
        (
            "ONE_PERCENT",
            LOADING_EPSILON_ONE_PERCENT,
        ),
    )

    rows: dict[str, dict[str, Any]] = {}

    for label, epsilon in thresholds:
        lower_ev = (
            necessary_portal_scale_for_global_loading_bound(
                epsilon
            )
        )

        scaled = (
            unloaded_reference_scaling_at_portal_scale(
                lower_ev
            )
        )

        rows[
            label
        ] = {
            "maximum_requested_loading":
                epsilon,

            "necessary_minimum_portal_scale_ev":
                lower_ev,

            "unloaded_reference_field_energy_j_at_lower_bound":
                float(
                    scaled[
                        "unloaded_reference_field_energy_j"
                    ]
                ),

            "unloaded_reference_field_headroom_j":
                float(
                    scaled[
                        "field_only_headroom_to_10mj_j"
                    ]
                ),

            "unloaded_reference_required_source_ev_m":
                float(
                    scaled[
                        "unloaded_reference_integrated_source_ev_m"
                    ]
                ),

            "optimistic_candidate_interval_nonempty":
                lower_ev
                <
                field_upper_ev,

            "necessary_not_sufficient":
                True,
        }

    upper_loading = (
        maximum_local_loading_lower_bound(
            field_upper_ev
        )
    )

    return {
        "field_only_strict_10mj_upper_portal_scale_ev":
            field_upper_ev,

        "maximum_local_loading_lower_bound_at_field_upper":
            float(
                upper_loading[
                    "maximum_local_epsilon_load_lower_bound"
                ]
            ),

        "thresholds":
            rows,

        "order_one_candidate_interval_nonempty":
            rows[
                "ORDER_ONE"
            ][
                "optimistic_candidate_interval_nonempty"
            ],

        "ten_percent_candidate_interval_nonempty":
            rows[
                "TEN_PERCENT"
            ][
                "optimistic_candidate_interval_nonempty"
            ],

        "one_percent_candidate_interval_nonempty":
            rows[
                "ONE_PERCENT"
            ][
                "optimistic_candidate_interval_nonempty"
            ],

        "intervals_are_loaded_solutions":
            False,

        "loaded_bvp_required_for_promotion":
            True,
    }


@lru_cache(maxsize=1)
def pauli_loading_overlap_gate() -> dict[str, Any]:
    """Intersect optimistic Pauli energy corridor with necessary loading control."""

    geometry = (
        pauli_geometry_gate()
    )

    boundary = (
        strict_partial_energy_boundary()
    )

    q_ev = float(
        geometry[
            "q_from_source_radius_ev"
        ]
    )

    pauli_10mj_upper_ev = float(
        boundary[
            "strict_sub10mj_requires_portal_scale_ev_less_than"
        ]
    )

    loading_order_one_ev = (
        necessary_portal_scale_for_global_loading_bound(
            LOADING_EPSILON_ORDER_ONE
        )
    )

    loading_ten_percent_ev = (
        necessary_portal_scale_for_global_loading_bound(
            LOADING_EPSILON_TEN_PERCENT
        )
    )

    loading_one_percent_ev = (
        necessary_portal_scale_for_global_loading_bound(
            LOADING_EPSILON_ONE_PERCENT
        )
    )

    at_q_loading = (
        maximum_local_loading_lower_bound(
            q_ev
        )
    )

    at_boundary_loading = (
        maximum_local_loading_lower_bound(
            pauli_10mj_upper_ev
        )
    )

    pauli_at_order_one = (
        source_energy_at_portal_scale(
            loading_order_one_ev
        )
    )

    pauli_at_ten_percent = (
        source_energy_at_portal_scale(
            loading_ten_percent_ev
        )
    )

    pauli_at_one_percent = (
        source_energy_at_portal_scale(
            loading_one_percent_ev
        )
    )

    no_order_one_overlap = bool(
        pauli_10mj_upper_ev
        <
        loading_order_one_ev
    )

    return {
        "characteristic_q_ev":
            q_ev,

        "optimistic_pauli_partial_10mj_upper_portal_scale_ev":
            pauli_10mj_upper_ev,

        "maximum_local_loading_lower_bound_at_q":
            float(
                at_q_loading[
                    "maximum_local_epsilon_load_lower_bound"
                ]
            ),

        "maximum_local_loading_lower_bound_at_pauli_10mj_boundary":
            float(
                at_boundary_loading[
                    "maximum_local_epsilon_load_lower_bound"
                ]
            ),

        "necessary_order_one_loading_scale_ev":
            loading_order_one_ev,

        "necessary_ten_percent_loading_scale_ev":
            loading_ten_percent_ev,

        "necessary_one_percent_loading_scale_ev":
            loading_one_percent_ev,

        "order_one_loading_scale_over_pauli_10mj_boundary":
            (
                loading_order_one_ev
                /
                pauli_10mj_upper_ev
            ),

        "pauli_partial_energy_at_order_one_loading_scale":
            pauli_at_order_one,

        "pauli_partial_energy_at_ten_percent_loading_scale":
            pauli_at_ten_percent,

        "pauli_partial_energy_at_one_percent_loading_scale":
            pauli_at_one_percent,

        "pauli_sub10mj_and_global_order_one_loading_overlap_exists":
            not no_order_one_overlap,

        "minimal_electron_pauli_perturbative_kernel_reuse_closed":
            no_order_one_overlap,

        "strongly_loaded_pauli_solution_closed":
            False,

        "loaded_nonlinear_bvp_performed":
            False,
    }


@lru_cache(maxsize=1)
def h17a12d1_summary() -> dict[str, Any]:
    """Return scoped A12D1 decision."""

    provenance = (
        provenance_gate()
    )

    variation = (
        same_action_variation_gate()
    )

    density = (
        payload_average_density_gate()
    )

    window = (
        controlled_portal_window_gate()
    )

    overlap = (
        pauli_loading_overlap_gate()
    )

    scoped_red = bool(
        provenance[
            "pass"
        ]

        and

        variation[
            "finite_matter_quadratic_loading_present"
        ]

        and

        overlap[
            "minimal_electron_pauli_perturbative_kernel_reuse_closed"
        ]
    )

    decision = (
        (
            "RED_SCOPED_A12D1_MINIMAL_ELECTRON_PAULI_"
            "SUB10MJ_CORRIDOR_HAS_NO_OVERLAP_WITH_EVEN_THE_"
            "NECESSARY_ORDER_ONE_FINITE_PAYLOAD_LOADING_BOUND__"
            "UNLOADED_A12C_KERNEL_REUSE_CLOSED_FOR_THIS_REALIZATION__"
            "A12B_AND_F2_MECHANISM_PRESERVED"
        )
        if scoped_red
        else
        "YELLOW_A12D1_SAME_ACTION_LOADING_OVERLAP_REQUIRES_REVIEW"
    )

    return {
        "branch":
            "032H17A12D1",

        "decision":
            decision,

        "provenance":
            provenance,

        "same_action_variation":
            variation,

        "payload_average_density":
            density,

        "controlled_portal_window":
            window,

        "pauli_loading_overlap":
            overlap,

        "a12c_2p656859j_probe_limit_capacity_reference_preserved":
            True,

        "a12c_2p656859j_same_action_loaded_payload_solution":
            False,

        "minimal_electron_pauli_perturbative_kernel_reuse_closed":
            scoped_red,

        "all_electron_pauli_realizations_closed":
            False,

        "strongly_loaded_pauli_rescue_closed":
            False,

        "a12b_exact_massless_carrier_closed":
            False,

        "a12c_gauge_invariant_f2_metric_mechanism_closed":
            False,

        "source_independent_loading_controlled_candidate_window_exists":
            bool(
                window[
                    "one_percent_candidate_interval_nonempty"
                ]
            ),

        "new_bvp_authorized_for_minimal_electron_pauli":
            False,

        "field_efficiency_optimization_authorized":
            False,

        "complete_energy_established":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "practical_device_found":
            False,

        "hook17_closed":
            False,

        "next":
            (
                "A12D0_RANKED_QUEUE_COMPOSITE_MAGNETIZATION_"
                "USING_LOADING_CONTROLLED_PORTAL_REQUIREMENTS"
            ),
    }
