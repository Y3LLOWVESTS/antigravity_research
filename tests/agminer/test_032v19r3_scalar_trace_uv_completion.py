"""Scientific regressions for 032V19R3 scalar-trace UV falsification.

These tests protect:

- positive-C1 tree matching;
- the unavoidable rank-one X^2/T^2 companion relation;
- absence of tree-level j=2/spin-2 companions in this template;
- absence of negative-mass assumptions;
- the maximally optimistic NDA-boundary matter coupling;
- exact finite-sphere Yukawa field inventory;
- the direct 1-nm experimental conflict;
- the payload-only strict-10-MJ mediator mass ceiling;
- the fact that the whole optimistic practical window lies inside the
  deliberately conservative neutron-scattering graphical scout range.

A red result closes only this single canonical linear unscreened scalar UV
template.
"""

import math

from antigravity_research.agminer.scalar_trace_uv_completion import (
    HBARC_EV_M,
    KAMIYA_ULTRACONSERVATIVE_GRAPHICAL_ENVELOPE_GEV_M2,
    graphical_empirical_scout,
    kamiya_exact_anchor,
    practical_mediator_mass_ceiling_ev,
    scalar_trace_tree_match,
    uniform_source_x_field_energy_j,
    uniform_sphere_trace_field_energy_j,
    uniform_sphere_yukawa_factor,
    weak_single_scalar_best_case,
)


C1 = 1.5142715050689224e-18

HARD_EV = 56.92491792612398
DECLARED_CUTOFF_EV = 285.3351934758513

STATIC_PREFLIGHT_J = 3681919.075350863
TARGET_J = 1.0e7

PAYLOAD_MASS_KG = 1.0
PAYLOAD_RADIUS_M = 0.10

B_EV = 6.123454611098919
F_PSI_EV = 22.70625323988203
SOURCE_RADIUS_M = 0.10


def weak_at_hard():
    return (
        weak_single_scalar_best_case(
            mediator_mass_ev=
                HARD_EV,

            target_c1_ev_m4=
                C1,
        )
    )


def test_tree_match_recovers_positive_c1():
    state = (
        weak_single_scalar_best_case(
            mediator_mass_ev=
                DECLARED_CUTOFF_EV,

            target_c1_ev_m4=
                C1,
        )
    )

    match = (
        scalar_trace_tree_match(
            mediator_mass_ev=
                DECLARED_CUTOFF_EV,

            f_x_ev=
                state[
                    "f_x_ev"
                ],

            f_t_ev=
                state[
                    "f_t_ev"
                ],
        )
    )

    assert math.isclose(
        match[
            "c1_ev_m4"
        ],
        C1,
        rel_tol=2.0e-15,
    )

    assert (
        match[
            "cross_xt_coefficient_ev_m4"
        ]
        <
        0.0
    )

    assert (
        match[
            "static_outward_sign_target"
        ]
        is True
    )


def test_rank_one_companion_identity():
    state = weak_at_hard()

    match = (
        scalar_trace_tree_match(
            mediator_mass_ev=
                HARD_EV,

            f_x_ev=
                state[
                    "f_x_ev"
                ],

            f_t_ev=
                state[
                    "f_t_ev"
                ],
        )
    )

    assert (
        match[
            "rank_one_psd_companion_identity"
        ]
        is True
    )

    assert (
        match[
            "rank_one_identity_relative_error"
        ]
        <
        1.0e-14
    )


def test_no_tree_spin2_and_no_negative_mass():
    state = weak_at_hard()

    assert (
        state[
            "tree_spin2_companion"
        ]
        is False
    )

    assert (
        state[
            "negative_mass_required"
        ]
        is False
    )


def test_best_case_hard_scale_numbers():
    state = weak_at_hard()

    assert math.isclose(
        state[
            "f_x_ev"
        ],
        4.529941036521538,
        rel_tol=2.0e-14,
    )

    assert math.isclose(
        state[
            "f_t_gev"
        ],
        44988.22666544808,
        rel_tol=2.0e-14,
    )

    assert math.isclose(
        state[
            "mass_force_g2_gev_m2"
        ],
        4.94085661597683e-10,
        rel_tol=2.0e-14,
    )

    assert math.isclose(
        state[
            "interaction_range_nm"
        ],
        3.4664429495723996,
        rel_tol=2.0e-14,
    )


def test_uniform_sphere_factor_is_positive_and_nearly_local():
    x = (
        HARD_EV
        * PAYLOAD_RADIUS_M
        / HBARC_EV_M
    )

    factor = (
        uniform_sphere_yukawa_factor(
            x
        )
    )

    assert (
        0.9999999
        <
        factor
        <
        1.0
    )


def test_hard_endpoint_payload_field_inventory():
    state = weak_at_hard()

    field = (
        uniform_sphere_trace_field_energy_j(
            mediator_mass_ev=
                HARD_EV,

            f_t_ev=
                state[
                    "f_t_ev"
                ],

            source_mass_kg=
                PAYLOAD_MASS_KG,

            source_radius_m=
                PAYLOAD_RADIUS_M,
        )
    )

    assert math.isclose(
        field[
            "conservative_ledger_charge_j"
        ],
        7050.349159521525,
        rel_tol=2.0e-12,
    )


def test_one_nm_anchor_is_inside_energy_window():
    anchor = (
        kamiya_exact_anchor(
            1.0
        )
    )

    state = (
        weak_single_scalar_best_case(
            mediator_mass_ev=
                anchor[
                    "mediator_mass_ev"
                ],

            target_c1_ev_m4=
                C1,
        )
    )

    field = (
        uniform_sphere_trace_field_energy_j(
            mediator_mass_ev=
                anchor[
                    "mediator_mass_ev"
                ],

            f_t_ev=
                state[
                    "f_t_ev"
                ],

            source_mass_kg=
                PAYLOAD_MASS_KG,

            source_radius_m=
                PAYLOAD_RADIUS_M,
        )
    )

    assert (
        STATIC_PREFLIGHT_J
        +
        field[
            "conservative_ledger_charge_j"
        ]
        <
        TARGET_J
    )


def test_one_nm_exact_empirical_ratio_is_enormous():
    anchor = (
        kamiya_exact_anchor(
            1.0
        )
    )

    state = (
        weak_single_scalar_best_case(
            mediator_mass_ev=
                anchor[
                    "mediator_mass_ev"
                ],

            target_c1_ev_m4=
                C1,
        )
    )

    ratio = (
        state[
            "mass_force_g2_gev_m2"
        ]
        /
        anchor[
            "limit_g2_gev_m2"
        ]
    )

    assert (
        ratio
        >
        6.0e9
    )


def test_point_one_nm_anchor_is_already_energy_catastrophic():
    anchor = (
        kamiya_exact_anchor(
            0.1
        )
    )

    state = (
        weak_single_scalar_best_case(
            mediator_mass_ev=
                anchor[
                    "mediator_mass_ev"
                ],

            target_c1_ev_m4=
                C1,
        )
    )

    field = (
        uniform_sphere_trace_field_energy_j(
            mediator_mass_ev=
                anchor[
                    "mediator_mass_ev"
                ],

            f_t_ev=
                state[
                    "f_t_ev"
                ],

            source_mass_kg=
                PAYLOAD_MASS_KG,

            source_radius_m=
                PAYLOAD_RADIUS_M,
        )
    )

    assert (
        field[
            "conservative_ledger_charge_j"
        ]
        >
        1.0e10
    )


def test_declared_cutoff_reference_payload_floor():
    state = (
        weak_single_scalar_best_case(
            mediator_mass_ev=
                DECLARED_CUTOFF_EV,

            target_c1_ev_m4=
                C1,
        )
    )

    field = (
        uniform_sphere_trace_field_energy_j(
            mediator_mass_ev=
                DECLARED_CUTOFF_EV,

            f_t_ev=
                state[
                    "f_t_ev"
                ],

            source_mass_kg=
                PAYLOAD_MASS_KG,

            source_radius_m=
                PAYLOAD_RADIUS_M,
        )
    )

    total = (
        STATIC_PREFLIGHT_J
        +
        field[
            "conservative_ledger_charge_j"
        ]
    )

    assert (
        8.1e6
        <
        total
        <
        8.2e6
    )


def test_declared_cutoff_fx_equals_r1_fpsi_coincidentally():
    state = (
        weak_single_scalar_best_case(
            mediator_mass_ev=
                DECLARED_CUTOFF_EV,

            target_c1_ev_m4=
                C1,
        )
    )

    assert math.isclose(
        state[
            "f_x_ev"
        ],
        F_PSI_EV,
        rel_tol=2.0e-14,
    )


def test_declared_source_x_companion_is_small():
    state = (
        weak_single_scalar_best_case(
            mediator_mass_ev=
                DECLARED_CUTOFF_EV,

            target_c1_ev_m4=
                C1,
        )
    )

    x_field = (
        uniform_source_x_field_energy_j(
            mediator_mass_ev=
                DECLARED_CUTOFF_EV,

            f_x_ev=
                state[
                    "f_x_ev"
                ],

            axial_b_ev=
                B_EV,

            f_psi_ev=
                F_PSI_EV,

            source_radius_m=
                SOURCE_RADIUS_M,
        )
    )

    assert (
        x_field[
            "positive_x_field_inventory_j"
        ]
        <
        1.0
    )


def test_strict_10mj_payload_only_mass_ceiling():
    result = (
        practical_mediator_mass_ceiling_ev(
            minimum_mass_ev=
                HARD_EV,

            target_c1_ev_m4=
                C1,

            base_static_energy_j=
                STATIC_PREFLIGHT_J,

            energy_limit_j=
                TARGET_J,

            payload_mass_kg=
                PAYLOAD_MASS_KG,

            payload_radius_m=
                PAYLOAD_RADIUS_M,
        )
    )

    assert (
        result[
            "window_exists"
        ]
        is True
    )

    assert (
        311.0
        <
        result[
            "mass_ceiling_ev"
        ]
        <
        312.0
    )

    assert math.isclose(
        result[
            "energy_at_ceiling_j"
        ],
        TARGET_J,
        rel_tol=2.0e-13,
    )


def test_practical_range_inside_graphical_scout_scope():
    ceiling = (
        practical_mediator_mass_ceiling_ev(
            minimum_mass_ev=
                HARD_EV,

            target_c1_ev_m4=
                C1,

            base_static_energy_j=
                STATIC_PREFLIGHT_J,

            energy_limit_j=
                TARGET_J,

            payload_mass_kg=
                PAYLOAD_MASS_KG,

            payload_radius_m=
                PAYLOAD_RADIUS_M,
        )
    )

    longest = (
        weak_at_hard()[
            "interaction_range_nm"
        ]
    )

    shortest = (
        ceiling[
            "mass_ceiling_range_nm"
        ]
    )

    assert (
        0.60
        <
        shortest
        <
        longest
        <
        3.50
    )


def test_entire_window_fails_ultraconservative_graphical_envelope():
    # At the optimistic NDA boundary:
    #
    #     F_T,max ~ m^-3
    #
    # so
    #
    #     g^2_min ~ m^6.
    #
    # Therefore the minimum predicted coupling in the whole practical mass
    # window occurs at the lowest allowed mediator mass, HARD_EV.
    state = weak_at_hard()

    scout = (
        graphical_empirical_scout(
            interaction_range_nm=
                state[
                    "interaction_range_nm"
                ],

            predicted_g2_gev_m2=
                state[
                    "mass_force_g2_gev_m2"
                ],
        )
    )

    assert (
        scout[
            "within_graphical_scout_scope"
        ]
        is True
    )

    assert (
        scout[
            "excluded_by_graphical_envelope_scout"
        ]
        is True
    )

    assert (
        scout[
            "predicted_over_graphical_envelope"
        ]
        >
        400.0
    )

    assert (
        KAMIYA_ULTRACONSERVATIVE_GRAPHICAL_ENVELOPE_GEV_M2
        ==
        1.0e-12
    )


def test_extra_nda_safety_margin_only_worsens_force():
    boundary = (
        weak_single_scalar_best_case(
            mediator_mass_ev=
                HARD_EV,

            target_c1_ev_m4=
                C1,

            nda_margin=
                1.0,
        )
    )

    safer = (
        weak_single_scalar_best_case(
            mediator_mass_ev=
                HARD_EV,

            target_c1_ev_m4=
                C1,

            nda_margin=
                2.0,
        )
    )

    assert (
        safer[
            "mass_force_g2_gev_m2"
        ]
        >
        boundary[
            "mass_force_g2_gev_m2"
        ]
        * 3.999
    )
