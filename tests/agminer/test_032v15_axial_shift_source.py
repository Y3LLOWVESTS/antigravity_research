import math

import numpy as np

from antigravity_research.agminer.axial_shift_source import (
    axial_accelerations_m_s2,
    axial_current_efficiency,
    hidden_fermion_inventory_floor,
    ordinary_electron_rest_energy_floor_j,
    required_q2_for_surface,
    spheroid_demag_z,
    spheroid_surface_kernel,
    spheroid_total_scalar_energy_j,
)
from antigravity_research.agminer.kinetic_conformal import (
    C_LIGHT,
)


G = 9.80665
M_EV = 1.0e5


def test_sphere_demag_is_one_third():
    assert math.isclose(
        spheroid_demag_z(
            0.1,
            0.1,
        ),
        1.0 / 3.0,
        rel_tol=1.0e-14,
    )


def test_axial_efficiency_mu_one():
    assert math.isclose(
        axial_current_efficiency(
            1.0
        ),
        0.8661733086868855,
        rel_tol=2.0e-12,
    )


def test_sphere_far_axis_kernel_matches_analytic_dipole():
    points = np.array(
        [
            [
                0.0,
                0.0,
                0.30,
            ]
        ]
    )

    gradient, hessian = (
        spheroid_surface_kernel(
            points,
            a_m=0.10,
            c_m=0.10,
            n_t=48,
            n_phi=72,
        )
    )

    # Source sphere center is z=-0.10, so this point is r=0.40
    # from the source center.
    expected_gradient = (
        2.0
        * 0.10**3
        /
        (
            3.0
            * 0.40**3
        )
    )

    expected_hzz = (
        -2.0
        * 0.10**3
        /
        0.40**4
    )

    assert math.isclose(
        gradient[0, 2],
        expected_gradient,
        rel_tol=2.0e-12,
    )

    assert math.isclose(
        hessian[0, 2, 2],
        expected_hzz,
        rel_tol=2.0e-12,
    )


def test_spherical_v14_surface_requirement_reconstructs_q():
    u = np.linspace(
        -1.0,
        1.0,
        81,
    )

    rho = (
        0.10
        * np.sqrt(
            np.maximum(
                0.0,
                1.0 - u**2,
            )
        )
    )

    z = (
        0.20
        + 0.10 * u
    )

    points = np.stack(
        (
            rho,
            np.zeros_like(rho),
            z,
        ),
        axis=1,
    )

    gradient, hessian = (
        spheroid_surface_kernel(
            points,
            a_m=0.10,
            c_m=0.10,
            n_t=48,
            n_phi=72,
        )
    )

    q2 = required_q2_for_surface(
        gradient,
        hessian,
        target_acceleration_m_s2=G,
    )

    assert math.isclose(
        math.sqrt(q2),
        3.6616787206413e-7,
        rel_tol=2.0e-10,
    )


def test_spherical_total_field_energy_is_v14_exterior_times_three_halves():
    q = 3.6616787206413e-7

    energy = (
        spheroid_total_scalar_energy_j(
            q2=q**2,
            metric_scale_ev=M_EV,
            a_m=0.10,
            c_m=0.10,
        )
    )

    expected = (
        1.5
        * 130124.04512548992
    )

    assert math.isclose(
        energy,
        expected,
        rel_tol=2.0e-10,
    )


def test_hidden_source_margin_is_reconstructed_exactly():
    result = (
        hidden_fermion_inventory_floor(
            q=9.0e-8,
            metric_scale_ev=M_EV,
            a_m=0.25,
            c_m=0.10,
            hard_scale_margin=5.0,
            mass_over_pf=1.0,
        )
    )

    assert math.isclose(
        result[
            "hard_scale_margin"
        ],
        5.0,
        rel_tol=2.0e-13,
    )


def test_hidden_source_has_positive_energy_and_support_floor():
    result = (
        hidden_fermion_inventory_floor(
            q=9.0e-8,
            metric_scale_ev=M_EV,
            a_m=0.25,
            c_m=0.10,
            hard_scale_margin=5.0,
            mass_over_pf=1.0,
        )
    )

    assert (
        result[
            "fermion_energy_j"
        ]
        > 0.0
    )

    assert (
        result[
            "laue_dec_pressure_support_floor_j"
        ]
        > 0.0
    )


def test_ordinary_electron_source_is_far_above_ten_mj():
    result = (
        ordinary_electron_rest_energy_floor_j(
            q=9.0e-8,
            metric_scale_ev=M_EV,
            a_m=0.25,
            c_m=0.10,
            hard_scale_margin=5.0,
        )
    )

    assert (
        result[
            "optimistic_rest_energy_floor_j"
        ]
        > 1.0e12
    )


def test_physical_acceleration_formula_gives_outward_surface():
    point = np.array(
        [
            [
                0.0,
                0.0,
                0.30,
            ]
        ]
    )

    gradient, hessian = (
        spheroid_surface_kernel(
            point,
            a_m=0.10,
            c_m=0.10,
            n_t=48,
            n_phi=72,
        )
    )

    q2 = required_q2_for_surface(
        gradient,
        hessian,
        target_acceleration_m_s2=G,
    )

    acceleration = (
        axial_accelerations_m_s2(
            gradient,
            hessian,
            q2=q2,
        )[0]
    )

    assert math.isclose(
        acceleration,
        G,
        rel_tol=2.0e-12,
    )
