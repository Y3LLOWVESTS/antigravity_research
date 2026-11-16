"""PH15-P9: exterior, conservation and independent 3D energy tests."""

import numpy as np
import pytest

from antigravity_research.agminer.hook17_ph15_p8_electric_dipole import (
    Dipole, Spec
)

from antigravity_research.agminer.hook17_ph15_p9_exterior_gauss import (
    free_ring_potential,
    boundary_audit,
    angular_basis,
    density_quadratic,
    density_modes,
    matched_fd_check,
    independent_3d_energy,
    independent_3d_hessian_check,
    examine,
)


@pytest.fixture(scope="module")
def small():
    m = Dipole(Spec(nr=10, L=10, N=220))
    r, f = m.solve(300)
    return m, r, f


@pytest.fixture(scope="module")
def base():
    m = Dipole(Spec(nr=18, L=12))
    r, f = m.solve(400)
    return m, r, f


def test_original_P8_source_unchanged(base):
    m, r, f = base
    assert abs(r["energy_CANONICAL_NOT_J"]-712.2184278085)<1e-3
    assert abs(r["source_separation"]-3.6224944497)<1e-3
    assert abs(r["net_X_charge"])<1e-9
    assert r["gauss_L2"]<1e-9
    assert max(r["scalar_EOM_weighted_L2"])<1e-4


def test_ring_kernel_far_coulomb_limit(small):
    m, r, f = small
    charge = np.zeros(m.cells)
    charge[3] = 1/m.w[3]
    z = 1000.
    potential = free_ring_potential(
        m, charge, [0.], [z]
    )[0]
    assert np.isclose(
        potential, 1/(4*np.pi*z), rtol=.02
    )


def test_ring_kernel_linearity(small):
    m, r, f = small
    charge = f["charge"]
    a = free_ring_potential(
        m, charge, [m.s.L], [0.]
    )[0]
    b = free_ring_potential(
        m, 3*charge, [m.s.L], [0.]
    )[0]
    assert np.isclose(b, 3*a, rtol=1e-9, atol=1e-10)


def test_exterior_boundary_correction_and_residual(base):
    m, r, f = base
    e = boundary_audit(m, f)
    assert e["boundary_harmonic_solver_residual_L2"]<1e-9
    assert e["E_one_shot_free_space_ring_boundary_correction_CANONICAL"]>.3
    assert e["relative_electrostatic_correction"]>.05
    assert e["boundary_dipole_only_approx_rel_L2"]<.08
    assert e["free_space_source_stationarity"]=="NOT_CERTIFIED"


def test_exterior_parity(small):
    m, r, f = small
    charge = f["charge"]

    pp = free_ring_potential(
        m, charge, [2.], [m.s.L]
    )[0]
    pn = free_ring_potential(
        m, charge, [2.], [-m.s.L]
    )[0]

    assert abs(pp+pn)<1e-10


def test_angular_modes_regular(small):
    m, r, f = small

    for k in (1, 2, 3):
        B = angular_basis(m, f, k)
        assert B.shape==(12, 2, m.cells)
        assert np.all(np.isfinite(B))


def test_electric_gauss_response_positive(base):
    m, r, f = base
    a = np.zeros((2, m.cells))
    a[0] = (
        .3*(m.rho/3)
        * np.exp(-(
            (m.rho-2.5)**2+m.z**2
        )/(2*3**2))
    )

    q, detail = density_quadratic(m, f, 1, a)

    assert detail["gauss_k_L2"]<1e-9
    assert detail["Q_electric_positive"]>0
    assert detail["linear_electric_source_L2"]>.01


def test_gauss_relaxed_density_modes(base):
    m, r, f = base
    modes = [
        density_modes(m, f, k)[0]
        for k in (1, 2, 3)
    ]

    assert all(
        x["lowest_density_mode"]>0
        for x in modes
    )
    assert all(
        x["lowest_mode_gauss_L2"]<1e-8
        for x in modes
    )
    assert all(
        x["eigenpair_residual"]<1e-7
        for x in modes
    )
    assert all(
        x["dynamic_constraint_stability"]=="NOT_CERTIFIED"
        for x in modes
    )


def test_independent_P8_azimuthal_quadrature(base):
    m, r, f = base

    h = (
        (m.rho/3)
        * np.exp(-(
            (m.rho-2.5)**2+m.z**2
        )/(2*3**2))
    )

    d = matched_fd_check(m, f, 1, h)

    assert d["Gauss_source_L2"]<1e-10
    assert d["relative_error"]<.001


def test_independent_3D_nonlinear_Gauss_and_Noether(small):
    m, r, f = small
    a = np.zeros((2, m.cells))

    a[0] = (
        .35*(m.rho/3)
        * np.exp(-(
            (m.rho-2.5)**2
            + (m.z-2)**2
        )/(2*3**2))
    )

    zero = independent_3d_energy(
        m, f, 1, a, 0., 16
    )

    assert abs(
        zero["energy"]-r["energy_CANONICAL_NOT_J"]
    )<1e-6

    d = independent_3d_hessian_check(
        m, f, 1, a, .035, 16
    )

    assert d["Gauss_up_L2"]<1e-8
    assert max(
        abs(np.array(d["Noether_up"])-m.s.N)
    )<1e-8
    assert d["rel_error"]<.001
    assert d["Q_electric_from_linearized_Gauss"]>0


def test_3D_angular_resolution(small):
    m, r, f = small
    a = np.zeros((2, m.cells))

    a[0] = (
        .25*(m.rho/3)
        * np.exp(-(
            m.rho**2+m.z**2
        )/(2*4**2))
    )

    e16 = independent_3d_energy(
        m, f, 1, a, .04, 16
    )["energy"]

    e24 = independent_3d_energy(
        m, f, 1, a, .04, 24
    )["energy"]

    assert abs(e16-e24)<1e-7


def test_domain_exterior_is_not_falsely_certified():
    a = examine(
        Spec(nr=12, L=12), full=False
    )
    b = examine(
        Spec(nr=12, L=16), full=False
    )

    assert a["free_space_source_onshell"]=="NOT_SOLVED"
    assert b["free_space_source_onshell"]=="NOT_SOLVED"

    assert (
        a["electrostatic_exterior"][
            "E_one_shot_free_space_ring_boundary_correction_CANONICAL"
        ] > 0
    )
    assert (
        b["electrostatic_exterior"][
            "E_one_shot_free_space_ring_boundary_correction_CANONICAL"
        ] > 0
    )


def test_no_false_reciprocity_or_stability_claim():
    a = examine(
        Spec(nr=10, L=10, N=220), full=False
    )
    assert a["full_reciprocal_X_Y_matter"]=="NOT_SOLVED"
    assert a["full_mode_stability"]=="NOT_CERTIFIED"
    assert a["free_space_source_onshell"]=="NOT_SOLVED"
