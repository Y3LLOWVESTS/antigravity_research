"""Fast G01-M effective-source physics tests."""
import numpy as np

from antigravity_research.gravity2.g01m_core import (
    Model, kernels, spectral, find_on_shell,
    shell_current_test, assemble,
)


def parent_fixture():
    model = Model()
    rows = []

    for ell in range(1, 13):
        A, M = kernels(ell)
        b = 149038.0722228661 if ell == 1 else 0.0

        rows.append({
            "ell": ell,
            "b_mode": b,
            "Y_full": M,
            "Y_exterior":
                model.radius / (ell + 1),
            "old_magnetic_energy_proxy":
                0.5*b*b*model.radius/(ell+1),
        })

    return {
        "status":
            "ACTION_INCOMPLETE_G01K_EXTERIOR_ONLY_KERNEL_"
            "NOT_FULL_TWO_SIDED_MAXWELL",
        "physical_survivors": 0,
        "K": model.K,
        "g": model.g,
        "H": model.H,
        "modes": rows,
        "historical_loaded_acceleration_m_s2":
            -129.67185782242464,
        "current_energy_scope":
            "CANONICAL_PROXY_NOT_SI_JOULES",
        "total_mandatory_interior_magnetic_energy_proxy":
            0.5*rows[0]["b_mode"]**2*model.radius,
    }


def test_two_sided_maxwell_modes():
    for ell in range(1, 33):
        A, M = kernels(ell)

        assert abs(A - 2/(2*ell+1)) < 1e-14
        assert abs(
            M - (2/ell + 2/(ell+1))
        ) < 1e-14

        assert Model().D(ell) > 0


def test_positive_kinetic_prefilters():
    m = Model()

    assert m.K*m.H-m.g*m.g > 0
    assert m.Z >= m.kappa > 0
    assert m.gamma > 0
    assert m.r > 0


def test_convex_no_drive_obstruction():
    m = Model()
    a = m.quadratic(32)

    assert np.min(a) > 0
    assert np.dot(
        a, np.ones(33)**2
    ) > 0


def test_magnetized_on_shell_and_positive_hessian():
    s = find_on_shell(20, 128)

    assert s["m_coefficients"][1] > 0.5
    assert s["max_on_shell_equation_residual"] < 1e-10
    assert s["min_full_static_hessian_eigenvalue"] > 0
    assert s["min_offstate_hessian_eigenvalue"] > 0


def test_current_and_wrong_sign_negative_control():
    s = find_on_shell(12, 96)

    j = shell_current_test(
        Model(),
        np.array(s["m_coefficients"]),
        12,
    )

    assert (
        j["max_two_sided_Maxwell_jump_relative_error"]
        < 1e-12
    )

    assert (
        j["wrong_sign_reciprocity_relative_residual"]
        > 0.1
    )


def test_spectral_convergence():
    states = [
        find_on_shell(n, nq)
        for n, nq in (
            (12, 96), (20, 128),
            (32, 160), (32, 224),
        )
    ]

    assert max(
        abs(
            s["m_coefficients"][1]
            - states[-1]["m_coefficients"][1]
        )
        for s in states
    ) < 1e-6

    assert abs(
        states[-1]["on_state_energy_over_B0_squared"]
        - states[-2]["on_state_energy_over_B0_squared"]
    ) < 1e-8


def test_energy_directional_variation():
    state = find_on_shell(20, 128)
    _, _, _, energy, *_ = spectral(
        20, 128, Model()
    )

    x = np.array(state["m_coefficients"])
    eps = 1e-5

    for index in (0, 1, 3, 5, 11, 20):
        dx = np.zeros(21)
        dx[index] = eps

        slope = (
            energy(x + dx) - energy(x - dx)
        ) / (2*eps)

        assert abs(slope) < 2e-7


def test_switching_barrier():
    s = assemble(parent_fixture())
    barrier = s["metastable_source_switching"]

    assert (
        barrier["off_energy_over_B0_squared"]
        == 0
    )

    assert (
        0
        < barrier["on_energy_over_B0_squared"]
        < barrier["saddle_energy_over_B0_squared"]
    )


def test_forced_original_source_not_on_shell():
    s = assemble(parent_fixture())

    assert (
        s[
            "forced_R3B_target_material_Euler_Lagrange_max_residual"
        ] > 1e-4
    )

    assert (
        s["target_mismatch_relative_surface_L2"]
        > 1e-4
    )

    assert s["physical_survivors"] == 0
