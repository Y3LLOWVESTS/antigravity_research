import math

from antigravity_research.geometry.kottler import C, G

from antigravity_research.geometry.perfect_fluid_defocusing import (
    active_mass_density_kg_m3,
    evaluate_energy_conditions,
    isotropic_defocusing_rate_s2,
    required_active_mass_density_kg_m3,
    required_energy_density_for_w,
)


def test_ordinary_positive_dust_focuses():
    epsilon = 1.0e20

    rate = isotropic_defocusing_rate_s2(
        energy_density_j_m3=epsilon,
        pressure_pa=0.0,
    )

    assert rate < 0.0


def test_positive_vacuum_like_energy_defocuses():
    epsilon = 1.0e20

    rate = isotropic_defocusing_rate_s2(
        energy_density_j_m3=epsilon,
        pressure_pa=-epsilon,
    )

    assert rate > 0.0


def test_vacuum_like_required_density_formula():
    acceleration = 9.80665
    separation = 1.0

    epsilon = required_energy_density_for_w(
        target_relative_acceleration_m_s2=acceleration,
        separation_m=separation,
        w=-1.0,
    )

    rho = epsilon / C**2

    expected = (
        3.0
        * acceleration
        / (
            8.0
            * math.pi
            * G
            * separation
        )
    )

    assert math.isclose(
        rho,
        expected,
        rel_tol=1e-12,
    )


def test_required_solution_reproduces_target():
    target_acceleration = 0.01 * 9.80665
    separation = 2.5
    w = -2.0 / 3.0

    epsilon = required_energy_density_for_w(
        target_acceleration,
        separation,
        w,
    )

    pressure = w * epsilon

    rate = isotropic_defocusing_rate_s2(
        epsilon,
        pressure,
    )

    reconstructed_acceleration = (
        rate
        * separation
    )

    assert math.isclose(
        reconstructed_acceleration,
        target_acceleration,
        rel_tol=1e-12,
    )


def test_vacuum_like_energy_conditions():
    epsilon = 1.0e20
    pressure = -epsilon

    conditions = evaluate_energy_conditions(
        epsilon,
        pressure,
    )

    assert conditions.nec
    assert conditions.wec
    assert not conditions.sec
    assert conditions.dec


def test_quintessence_like_energy_conditions():
    epsilon = 1.0e20
    pressure = -(2.0 / 3.0) * epsilon

    conditions = evaluate_energy_conditions(
        epsilon,
        pressure,
    )

    assert conditions.nec
    assert conditions.wec
    assert not conditions.sec
    assert conditions.dec


def test_phantom_energy_violates_nec():
    epsilon = 1.0e20
    pressure = -1.2 * epsilon

    conditions = evaluate_energy_conditions(
        epsilon,
        pressure,
    )

    assert not conditions.nec
    assert not conditions.wec
    assert not conditions.sec
    assert not conditions.dec


def test_active_density_identity():
    epsilon = 4.0e20
    pressure = -3.0e20

    result = active_mass_density_kg_m3(
        epsilon,
        pressure,
    )

    expected = (
        epsilon
        + 3.0 * pressure
    ) / C**2

    assert math.isclose(
        result,
        expected,
        rel_tol=1e-15,
    )


def test_required_active_density_for_one_g_over_one_meter():
    target = 9.80665

    result = required_active_mass_density_kg_m3(
        target_relative_acceleration_m_s2=target,
        separation_m=1.0,
    )

    expected = (
        -3.0
        * target
        / (
            4.0
            * math.pi
            * G
        )
    )

    assert math.isclose(
        result,
        expected,
        rel_tol=1e-15,
    )
