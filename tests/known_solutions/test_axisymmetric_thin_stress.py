"""Regression tests for the first geometry-aware 006B thin-source model.

These tests protect the analytical local-conservation identities, DEC-saturated
stress profile, and independent reconstruction of the Simulation 005B
benchmark.  They also verify the project-derived lower-coefficient annular
candidate found by the first 006B optimization slice.

Passing these tests does not establish a finite-thickness realization, exact
nonlinear GR solution, stability, material realizability, or practical device.
"""

import math

from scipy.optimize import minimize, minimize_scalar

from antigravity_research.geometry.axisymmetric_thin_stress import (
    conserved_annular_integrated_stress_trace_factor,
    conserved_annular_mass_coefficient,
    radial_kernel_primitive,
    uniform_disk_ring_mass_coefficient,
)


def test_radial_kernel_primitive_by_centered_difference():
    x = 1.7
    step = 1.0e-6

    derivative = (
        radial_kernel_primitive(x + step)
        - radial_kernel_primitive(x - step)
    ) / (2.0 * step)

    expected = 1.0 / (x * (1.0 + x * x) ** 1.5)

    assert math.isclose(
        derivative,
        expected,
        rel_tol=2.0e-9,
        abs_tol=1.0e-12,
    )


def test_complete_annular_stress_trace_cancels_exactly():
    trace = conserved_annular_integrated_stress_trace_factor(
        1.4,
        4.7,
    )

    assert trace == 0.0


def test_inner_and_annular_profiles_satisfy_local_conservation_and_dec():
    u0 = 3.0
    a = 1.4

    # Inner disk: U=U0, p_r=p_phi=-U0.
    r_inner = 0.8
    u_inner = u0
    pr_inner = -u0
    pphi_inner = -u0
    dpr_dr_inner = 0.0

    residual_inner = (
        dpr_dr_inner
        + (pr_inner - pphi_inner) / r_inner
    )

    assert abs(residual_inner) < 1.0e-14
    assert abs(pr_inner) <= u_inner
    assert abs(pphi_inner) <= u_inner

    # Stress-transfer annulus: U=U0*a^2/r^2, p_r=-U, p_phi=+U.
    r_annulus = 2.3
    u_annulus = u0 * a * a / (r_annulus * r_annulus)
    pr_annulus = -u_annulus
    pphi_annulus = +u_annulus
    dpr_dr_annulus = 2.0 * u_annulus / r_annulus

    residual_annulus = (
        dpr_dr_annulus
        + (pr_annulus - pphi_annulus) / r_annulus
    )

    assert abs(residual_annulus) < 1.0e-14
    assert abs(pr_annulus) <= u_annulus
    assert abs(pphi_annulus) <= u_annulus


def test_independent_uniform_disk_reconstructs_005b_coefficient():
    result = minimize_scalar(
        uniform_disk_ring_mass_coefficient,
        bounds=(2.0, 8.0),
        method="bounded",
        options={"xatol": 1.0e-13},
    )

    assert result.success

    assert math.isclose(
        result.x,
        4.006149670781,
        rel_tol=2.0e-8,
    )

    assert math.isclose(
        result.fun,
        79.753148116012,
        rel_tol=2.0e-12,
    )


def test_conserved_annular_candidate_optimizes_below_005b():
    def objective(values):
        alpha, beta = values

        if alpha <= 0.0 or beta <= alpha:
            return 1.0e9

        return conserved_annular_mass_coefficient(
            float(alpha),
            float(beta),
        )

    result = minimize(
        objective,
        x0=(1.4, 4.7),
        method="Nelder-Mead",
        options={
            "xatol": 1.0e-12,
            "fatol": 1.0e-12,
            "maxiter": 5000,
        },
    )

    assert result.success

    alpha, beta = result.x

    assert math.isclose(
        alpha,
        1.43750055633834,
        rel_tol=2.0e-8,
    )

    assert math.isclose(
        beta,
        4.70143745159373,
        rel_tol=2.0e-8,
    )

    assert math.isclose(
        result.fun,
        23.4267101753911,
        rel_tol=2.0e-10,
    )

    assert result.fun < 79.753148116012
