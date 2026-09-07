"""Scientific regressions for 032V26B1R1 hook quantum-force preflight."""

from __future__ import annotations

import math

from antigravity_research.agminer.hook_quadratic_quantum_force import (
    HOYLE_2004_BETA3_68_ABS,
    active_coupling_limit_from_beta3,
    beta3_from_active_coupling,
    empirical_capacity_corridor,
    projector_penalty_at_energy_target,
    range_massless_preflight,
    required_background_amplitude,
    required_lapse_change,
    spherical_capacity_energy_j,
    two_mediator_inverse_cube_coefficient,
    v26b1r1_gate,
)


def test_two_mediator_inverse_cube_coefficient():
    assert math.isclose(
        two_mediator_inverse_cube_coefficient(),
        1.0
        /
        (
            64.0
            *
            math.pi**3
        ),
        rel_tol=1.0e-15,
    )


def test_lapse_reference_is_corrected_v26b1_value():
    assert math.isclose(
        required_lapse_change(),
        2.1822739344396436e-17,
        rel_tol=1.0e-15,
    )


def test_beta3_limit_round_trip():
    coupling = (
        active_coupling_limit_from_beta3(
            beta3_abs_limit=
                HOYLE_2004_BETA3_68_ABS,

            projector_penalty=
                1.0,
        )
    )

    beta = (
        beta3_from_active_coupling(
            active_coupling_ev_m2=
                coupling[
                    "active_coupling_max_ev_m2"
                ],

            projector_penalty=
                1.0,
        )
    )

    assert math.isclose(
        beta,
        HOYLE_2004_BETA3_68_ABS,
        rel_tol=2.0e-15,
    )


def test_nominal_empirical_active_coupling_limit():
    result = (
        active_coupling_limit_from_beta3(
            projector_penalty=
                1.0,
        )
    )

    assert math.isclose(
        result[
            "active_coupling_max_ev_m2"
        ],
        9.784321962067051e-25,
        rel_tol=2.0e-12,
    )


def test_nominal_metric_scale_is_about_one_tev():
    result = (
        active_coupling_limit_from_beta3(
            projector_penalty=
                1.0,
        )
    )

    assert (
        1.0
        <
        result[
            "equivalent_active_metric_scale_tev"
        ]
        <
        1.02
    )


def test_required_background_is_kev_scale_at_empirical_boundary():
    coupling = (
        active_coupling_limit_from_beta3(
            projector_penalty=
                1.0,
        )
    )

    result = (
        required_background_amplitude(
            active_coupling_ev_m2=
                coupling[
                    "active_coupling_max_ev_m2"
                ],

            delta_g00=
                required_lapse_change(),
        )
    )

    assert (
        4.7
        <
        result[
            "background_amplitude_kev"
        ]
        <
        4.8
    )


def test_massless_capacity_floor_is_microjoule_scale():
    result = (
        empirical_capacity_corridor(
            projector_penalty=
                1.0,
        )
    )

    assert (
        1.0e-5
        <
        result[
            "massless_capacity_energy_j"
        ]
        <
        1.3e-5
    )


def test_point_two_meter_range_adds_expected_capacity_factor():
    amplitude = (
        4722.688107328991
    )

    massless = (
        spherical_capacity_energy_j(
            background_amplitude_ev=
                amplitude,

            radius_m=
                0.10,
        )
    )

    ranged = (
        spherical_capacity_energy_j(
            background_amplitude_ev=
                amplitude,

            radius_m=
                0.10,

            range_m=
                0.20,
        )
    )

    assert math.isclose(
        ranged[
            "range_factor"
        ],
        1.5,
        rel_tol=0.0,
        abs_tol=0.0,
    )

    assert math.isclose(
        ranged[
            "energy_j"
        ]
        /
        massless[
            "energy_j"
        ],
        1.5,
        rel_tol=2.0e-15,
    )


def test_nominal_range_capacity_floor_is_far_below_10mj():
    result = (
        empirical_capacity_corridor(
            projector_penalty=
                1.0,
        )
    )

    assert (
        result[
            "device_range_capacity_energy_j"
        ]
        <
        2.0e-5
    )

    assert (
        result[
            "capacity_energy_below_strict_10mj"
        ]
        is True
    )


def test_enormous_projector_penalty_1e12_still_below_10mj():
    result = (
        empirical_capacity_corridor(
            projector_penalty=
                1.0e12,
        )
    )

    assert (
        result[
            "device_range_capacity_energy_j"
        ]
        <
        20.0
    )

    assert (
        result[
            "capacity_energy_below_strict_10mj"
        ]
        is True
    )


def test_projector_penalty_needed_to_reach_10mj_is_extreme():
    result = (
        projector_penalty_at_energy_target()
    )

    assert (
        result[
            "projector_penalty_for_target"
        ]
        >
        1.0e23
    )


def test_device_range_mode_is_effectively_massless_at_one_mm():
    result = (
        range_massless_preflight()
    )

    assert math.isclose(
        result[
            "m_times_r"
        ],
        0.005,
        rel_tol=1.0e-15,
    )

    assert (
        result[
            "massless_preflight_valid"
        ]
        is True
    )


def test_gate_keeps_action_construction_open_but_blocks_optimization():
    gate = (
        v26b1r1_gate()
    )

    assert (
        gate[
            "quadratic_metric_has_offstate_two_mediator_force"
        ]
        is True
    )

    assert (
        gate[
            "offstate_linear_response_zero_implies_zero_quantum_force"
        ]
        is False
    )

    assert (
        gate[
            "empirical_inverse_cube_gate_closes_quadratic_hook_portal"
        ]
        is False
    )

    assert (
        gate[
            "explicit_action_construction_authorized"
        ]
        is True
    )

    assert (
        gate[
            "energy_optimization_authorized"
        ]
        is False
    )

    assert (
        gate[
            "action_oracle_authorized"
        ]
        is False
    )

    assert (
        gate[
            "agminer_database_mutation_authorized"
        ]
        is False
    )
