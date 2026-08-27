import math

from antigravity_research.geometry.reissner_nordstrom import (
    electromagnetic_field_energy_mass_outside_kg,
    evaluate_shell_conditions,
    maxwell_energy_density_j_m3,
    neutral_free_tendency_m_s2,
    repulsion_radius_m,
    rn_metric_f,
    solve_source_for_surface_repulsion,
    charged_shell_surface_energy_j_m2,
    charged_shell_surface_pressure_n_m,
)


G0 = 9.80665


def test_zero_charge_reduces_metric_charge_term():
    # Choose M/r large enough that the Schwarzschild correction
    # is safely above IEEE-754 rounding near f=1.
    #
    # The previous values gave
    #
    #     2GM/(c^2 r) ~ 1.5e-17
    #
    # which is below double-precision resolution near 1.0 and
    # therefore legitimately rounded f to exactly 1.0.
    mass = 1.0e20
    radius = 1.0e3

    f = rn_metric_f(
        radius,
        mass,
        0.0,
    )

    assert 0.0 < f < 1.0


def test_repulsion_changes_sign_at_classical_radius():
    mass = 1.0e10
    charge = 1.0e8

    radius = repulsion_radius_m(
        mass,
        charge,
    )

    inside = neutral_free_tendency_m_s2(
        0.9 * radius,
        mass,
        charge,
    )

    outside = neutral_free_tendency_m_s2(
        1.1 * radius,
        mass,
        charge,
    )

    assert inside > 0.0
    assert outside < 0.0


def test_source_solver_reconstructs_one_g_surface_repulsion():
    mass, charge = solve_source_for_surface_repulsion(
        G0,
        1.0,
        1.2,
    )

    result = neutral_free_tendency_m_s2(
        1.0,
        mass,
        charge,
    )

    assert math.isclose(
        result,
        G0,
        rel_tol=1.0e-12,
    )


def test_z_is_reconstructed():
    mass, charge = solve_source_for_surface_repulsion(
        1.0e-6 * G0,
        1.0,
        1.2,
    )

    radius = repulsion_radius_m(
        mass,
        charge,
    )

    assert math.isclose(
        radius,
        1.2,
        rel_tol=1.0e-12,
    )


def test_maxwell_energy_density_is_positive():
    _, charge = solve_source_for_surface_repulsion(
        1.0e-6 * G0,
        1.0,
        1.2,
    )

    energy = maxwell_energy_density_j_m3(
        1.0,
        charge,
    )

    assert energy > 0.0


def test_robust_z_1_2_shell_passes_wec_and_dec():
    mass, charge = solve_source_for_surface_repulsion(
        G0,
        1.0,
        1.2,
    )

    energy = charged_shell_surface_energy_j_m2(
        1.0,
        mass,
        charge,
    )

    pressure = charged_shell_surface_pressure_n_m(
        1.0,
        mass,
        charge,
    )

    conditions = evaluate_shell_conditions(
        energy,
        pressure,
    )

    assert energy > 0.0
    assert pressure < 0.0
    assert conditions.nec
    assert conditions.wec
    assert conditions.dec


def test_z_1_5_shell_fails_nec_and_dec():
    mass, charge = solve_source_for_surface_repulsion(
        G0,
        1.0,
        1.5,
    )

    energy = charged_shell_surface_energy_j_m2(
        1.0,
        mass,
        charge,
    )

    pressure = charged_shell_surface_pressure_n_m(
        1.0,
        mass,
        charge,
    )

    conditions = evaluate_shell_conditions(
        energy,
        pressure,
    )

    assert energy > 0.0
    assert not conditions.nec
    assert not conditions.dec


def test_repulsive_condition_equals_more_than_half_adm_mass_in_field():
    mass, charge = solve_source_for_surface_repulsion(
        G0,
        1.0,
        1.2,
    )

    field_mass = electromagnetic_field_energy_mass_outside_kg(
        1.0,
        charge,
    )

    assert field_mass > 0.5 * mass

    assert math.isclose(
        field_mass / mass,
        0.6,
        rel_tol=1.0e-12,
    )
