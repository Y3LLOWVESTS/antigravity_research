import math

from antigravity_research.agminer.axial_dirac_meanfield import (
    axial_positive_band_integrals,
    fixed_density_current_susceptibility_hat,
    meanfield_scaling_metrics,
    minimum_loop_for_nr_stoner,
    payload_trace_load,
    physicalize_dimensionless_state,
    solve_mu_for_current,
    spheroid_demag_z,
    spheroid_volume_m3,
    stoner_parameter_nr,
)


Q = 9.117449122814854e-8
M_EV = 1.0e5
A_M = 0.25740088555864965
C_M = 0.09659120999271102

NZ = spheroid_demag_z(
    A_M,
    C_M,
)

VOLUME_M3 = spheroid_volume_m3(
    A_M,
    C_M,
)


def test_free_band_thermodynamic_identity_and_isotropy():
    state = axial_positive_band_integrals(
        mass_ev=2.0,
        axial_b_ev=0.0,
        chemical_potential_ev=5.0,
        order=64,
    )

    pressure = state[
        "pressure_z_ev4"
    ]

    assert math.isclose(
        state[
            "pressure_perp_ev4"
        ],
        pressure,
        rel_tol=2.0e-13,
    )

    assert math.isclose(
        5.0
        * state[
            "number_density_ev3"
        ]
        - state[
            "energy_density_ev4"
        ],
        pressure,
        rel_tol=2.0e-13,
    )

    assert abs(
        state[
            "axial_current_ev3"
        ]
    ) < 1.0e-13


def test_old_v15_free_source_fails_after_exact_meanfield_response():
    f_psi_ev = (
        62.661384197111325
    )

    m_psi_ev = (
        157.48523540592993
    )

    b_ev = (
        NZ
        * Q
        * M_EV**2
        / f_psi_ev
    )

    target_current = (
        Q
        * f_psi_ev
        * M_EV**2
    )

    state = solve_mu_for_current(
        mass_ev=
            m_psi_ev,

        axial_b_ev=
            b_ev,

        target_current_ev3=
            target_current,

        order=
            80,
    )

    assert math.isclose(
        state[
            "chemical_potential_ev"
        ],
        1048.9710078164,
        rel_tol=5.0e-10,
    )

    cutoff = (
        4.0
        * math.pi
        * f_psi_ev
    )

    assert (
        cutoff
        / state[
            "chemical_potential_ev"
        ]
        < 0.8
    )


def test_v15_geometry_field_energy_reconstructs_previous_result():
    metrics = meanfield_scaling_metrics(
        q=
            Q,

        metric_scale_ev=
            M_EV,

        volume_m3=
            VOLUME_M3,

        demag_z=
            NZ,

        r_mass_over_b=
            1.228614544,

        u_mu_over_b=
            3.278214004,

        order=
            80,
    )

    assert math.isclose(
        metrics[
            "field_energy_j"
        ],
        140563.1672444695,
        rel_tol=2.0e-12,
    )


def test_flavor_count_does_not_change_energy_or_loop_at_fixed_state():
    metrics = meanfield_scaling_metrics(
        q=
            Q,

        metric_scale_ev=
            M_EV,

        volume_m3=
            VOLUME_M3,

        demag_z=
            NZ,

        r_mass_over_b=
            1.228614544,

        u_mu_over_b=
            3.278214004,

        order=
            80,
    )

    low = physicalize_dimensionless_state(
        q=
            Q,

        metric_scale_ev=
            M_EV,

        demag_z=
            NZ,

        r_mass_over_b=
            1.228614544,

        u_mu_over_b=
            3.278214004,

        flavors=
            14,

        order=
            80,
    )

    high = physicalize_dimensionless_state(
        q=
            Q,

        metric_scale_ev=
            M_EV,

        demag_z=
            NZ,

        r_mass_over_b=
            1.228614544,

        u_mu_over_b=
            3.278214004,

        flavors=
            56,

        order=
            80,
    )

    assert (
        metrics[
            "partial_conservative_floor_j"
        ]
        > 0.0
    )

    assert math.isclose(
        high[
            "hard_scale_margin"
        ]
        / low[
            "hard_scale_margin"
        ],
        2.0,
        rel_tol=2.0e-12,
    )


def test_controlled_nr_stoner_loop_conflict():
    maximum = stoner_parameter_nr(
        demag_z=
            NZ,

        p_f_over_m=
            0.5,

        loop_proxy=
            0.5,
    )

    required = minimum_loop_for_nr_stoner(
        demag_z=
            NZ,

        p_f_over_m=
            0.5,
    )

    assert (
        maximum
        < 1.0
    )

    assert (
        required
        > 0.82
    )


def test_loop_point_three_reference_enters_partial_ten_mj_corridor():
    metrics = meanfield_scaling_metrics(
        q=
            Q,

        metric_scale_ev=
            M_EV,

        volume_m3=
            VOLUME_M3,

        demag_z=
            NZ,

        r_mass_over_b=
            1.228614544,

        u_mu_over_b=
            3.278214004,

        order=
            80,
    )

    assert math.isclose(
        metrics[
            "loop_proxy"
        ],
        0.30000006148,
        rel_tol=2.0e-8,
    )

    assert (
        4.2e6
        < metrics[
            "partial_conservative_floor_j"
        ]
        < 4.4e6
    )


def test_loop_point_three_reference_has_positive_occupied_band_curvature_proxy():
    result = (
        fixed_density_current_susceptibility_hat(
            r_mass_over_b=
                1.228614544,

            u_mu_over_b=
                3.278214004,

            order=
                80,
        )
    )

    assert (
        result[
            "susceptibility_hat"
        ]
        > 0.0
    )

    assert (
        0.0
        < result[
            "susceptibility_to_current_ratio"
        ]
        < 1.0
    )


def test_payload_trace_load_is_small_at_one_hundred_kev():
    result = payload_trace_load(
        payload_mass_kg=
            1.0,

        payload_radius_m=
            0.10,

        metric_scale_ev=
            1.0e5,
    )

    assert math.isclose(
        result[
            "epsilon_trace_load"
        ],
        0.01028967868346,
        rel_tol=2.0e-12,
    )

    assert (
        result[
            "uniform_sphere_transmission_scout"
        ]
        > 0.99
    )


def test_payload_trace_load_blocks_naive_low_scale_extrapolation():
    high = payload_trace_load(
        payload_mass_kg=
            1.0,

        payload_radius_m=
            0.10,

        metric_scale_ev=
            1.0e5,
    )

    low = payload_trace_load(
        payload_mass_kg=
            1.0,

        payload_radius_m=
            0.10,

        metric_scale_ev=
            1.0e4,
    )

    assert (
        low[
            "epsilon_trace_load"
        ]
        > 100.0
    )

    assert (
        low[
            "uniform_sphere_transmission_scout"
        ]
        < 0.03
    )

    assert (
        low[
            "epsilon_trace_load"
        ]
        > high[
            "epsilon_trace_load"
        ]
        * 9999.0
    )
