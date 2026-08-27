import math

from antigravity_research.geometry.israel_shell import (
    evaluate_shell_energy_conditions,
    exterior_weak_field_acceleration_m_s2,
    gravastar_mass_relation_residual_kg,
    interior_volume_mass_kg,
    shell_energy_mass_kg,
    surface_energy_j_m2,
    surface_pressure_n_m,
)


def test_equal_exterior_and_volume_mass_gives_zero_shell_energy():
    rate = 9.80665
    radius = 1.0

    volume_mass = interior_volume_mass_kg(
        rate,
        radius,
    )

    shell_energy = surface_energy_j_m2(
        rate,
        radius,
        volume_mass,
    )

    scale = abs(
        surface_pressure_n_m(
            rate,
            radius,
            volume_mass,
        )
    )

    assert abs(shell_energy) < max(scale, 1.0) * 1e-12


def test_equal_mass_case_has_positive_surface_pressure():
    rate = 9.80665
    radius = 1.0

    volume_mass = interior_volume_mass_kg(
        rate,
        radius,
    )

    pressure = surface_pressure_n_m(
        rate,
        radius,
        volume_mass,
    )

    assert pressure > 0.0


def test_negative_exterior_mass_requires_negative_shell_energy():
    rate = 9.80665
    radius = 1.0

    volume_mass = interior_volume_mass_kg(
        rate,
        radius,
    )

    exterior_mass = (
        -0.25
        * volume_mass
    )

    shell_energy = surface_energy_j_m2(
        rate,
        radius,
        exterior_mass,
    )

    assert shell_energy < 0.0


def test_negative_exterior_mass_repels_in_weak_field():
    acceleration = (
        exterior_weak_field_acceleration_m_s2(
            2.0,
            -1.0e10,
        )
    )

    assert acceleration > 0.0


def test_positive_shell_energy_implies_exterior_mass_above_core_mass():
    rate = 1.0
    radius = 2.0

    volume_mass = interior_volume_mass_kg(
        rate,
        radius,
    )

    exterior_mass = (
        2.0
        * volume_mass
    )

    shell_energy = surface_energy_j_m2(
        rate,
        radius,
        exterior_mass,
    )

    assert shell_energy > 0.0


def test_mass_relation_reconstructs_exterior_mass():
    rate = 9.80665
    radius = 1.0

    volume_mass = interior_volume_mass_kg(
        rate,
        radius,
    )

    for ratio in (
        -1.0,
        -0.25,
        0.0,
        0.5,
        1.0,
        2.0,
    ):
        exterior_mass = (
            ratio
            * volume_mass
        )

        residual = gravastar_mass_relation_residual_kg(
            rate,
            radius,
            exterior_mass,
        )

        scale = max(
            abs(exterior_mass),
            abs(volume_mass),
            1.0,
        )

        assert abs(residual) < scale * 1e-11


def test_modestly_negative_mass_can_pass_shell_nec_but_not_wec():
    rate = 9.80665
    radius = 1.0

    volume_mass = interior_volume_mass_kg(
        rate,
        radius,
    )

    exterior_mass = (
        -0.25
        * volume_mass
    )

    energy = surface_energy_j_m2(
        rate,
        radius,
        exterior_mass,
    )

    pressure = surface_pressure_n_m(
        rate,
        radius,
        exterior_mass,
    )

    conditions = evaluate_shell_energy_conditions(
        energy,
        pressure,
    )

    assert conditions.nec
    assert not conditions.wec
    assert not conditions.dec


def test_sufficiently_negative_mass_fails_nec():
    rate = 9.80665
    radius = 1.0

    volume_mass = interior_volume_mass_kg(
        rate,
        radius,
    )

    exterior_mass = (
        -1.0
        * volume_mass
    )

    energy = surface_energy_j_m2(
        rate,
        radius,
        exterior_mass,
    )

    pressure = surface_pressure_n_m(
        rate,
        radius,
        exterior_mass,
    )

    conditions = evaluate_shell_energy_conditions(
        energy,
        pressure,
    )

    assert not conditions.nec
    assert not conditions.wec
    assert not conditions.dec
