import math

from antigravity_research.agminer.shift_source import (
    compact_derivative_source_net_monopole,
    dipole_axial_acceleration_m_s2,
    dipole_b_m6_for_axis_target,
    dipole_exterior_energy_j,
    dipole_y,
    m4_energy_rescale,
    regular_static_monopole_requires_evasion,
    scale_ev_for_m4_energy,
)


G = 9.80665


def test_m4_energy_rescaling():
    assert math.isclose(
        m4_energy_rescale(
            2.0,
            1.0e5,
            2.0e5,
        ),
        32.0,
        rel_tol=1.0e-15,
    )


def test_dipole_far_axis_reconstructs_one_g():
    b_m6 = dipole_b_m6_for_axis_target(
        G,
        0.40,
    )

    acceleration = (
        dipole_axial_acceleration_m_s2(
            b_m6,
            0.0,
            0.40,
        )
    )

    assert math.isclose(
        acceleration,
        G,
        rel_tol=2.0e-15,
    )


def test_dipole_off_axis_is_outward_above_source():
    b_m6 = dipole_b_m6_for_axis_target(
        G,
        0.40,
    )

    assert (
        dipole_axial_acceleration_m_s2(
            b_m6,
            0.05,
            0.30,
        )
        > 0.0
    )


def test_dipole_100kev_exterior_energy():
    result = dipole_exterior_energy_j(
        scale_ev=1.0e5,
        source_radius_m=0.10,
        far_axis_radius_m=0.40,
        target_acceleration_m_s2=G,
    )

    assert math.isclose(
        result[
            "exterior_scalar_energy_j"
        ],
        1.3012404512548992e5,
        rel_tol=2.0e-12,
    )


def test_dipole_exact_10mj_scale_is_about_296kev():
    reference = dipole_exterior_energy_j(
        scale_ev=1.0e5,
        source_radius_m=0.10,
        far_axis_radius_m=0.40,
        target_acceleration_m_s2=G,
    )

    scale = scale_ev_for_m4_energy(
        target_energy_j=1.0e7,
        reference_energy_j=reference[
            "exterior_scalar_energy_j"
        ],
        reference_scale_ev=1.0e5,
    )

    assert (
        2.95e5
        <
        scale
        <
        2.97e5
    )


def test_compact_derivative_source_has_zero_monopole():
    assert (
        compact_derivative_source_net_monopole()
        ==
        0.0
    )


def test_regular_static_monopole_requires_an_evasion():
    assert (
        regular_static_monopole_requires_evasion()
        is True
    )

    assert (
        regular_static_monopole_requires_evasion(
            time_dependent=True
        )
        is False
    )


def test_dipole_source_surface_remains_weak_y():
    b_m6 = dipole_b_m6_for_axis_target(
        G,
        0.40,
    )

    y_source = dipole_y(
        b_m6,
        0.0,
        0.10,
    )

    assert (
        y_source
        <
        1.0e-12
    )
