"""PH15-P10 free-source, exact conservation and exterior Ward tests."""

import numpy as np
import pytest

from scipy.integrate import quad

from antigravity_research.agminer.hook17_ph15_p10_free_space import (
    CoulombSource,
    Spec,
)


@pytest.fixture(scope="module")
def base():
    model = CoulombSource(Spec(nr=18, L=12))
    result, fields = model.solve(350)
    return model, result, fields


@pytest.fixture(scope="module")
def large():
    model = CoulombSource(Spec(nr=24, L=16))
    result, fields = model.solve(350)
    return model, result, fields


@pytest.fixture(scope="module")
def fine():
    model = CoulombSource(Spec(nr=36, L=16))
    result, fields = model.solve(350)
    return model, result, fields


@pytest.fixture(scope="module")
def far():
    model = CoulombSource(Spec(nr=30, L=20))
    result, fields = model.solve(350)
    return model, result, fields


def test_kernel_reciprocity_and_FD_gradient(base):
    model, _, _ = base

    assert model.kernel_symmetry_inf < 1e-12
    assert model.mag_kernel_symmetry_inf < 1e-12

    assert max(
        x["abs_error"]
        for x in model.fd_gradient()
    ) < 3e-7


def test_independent_ring_kernels_vs_direct_angle_quadrature(base):
    model, _, _ = base

    a, b = 7, 9

    r1, z1 = model.rho[a], model.z[a]
    r2, z2 = model.rho[b], model.z[b]

    def distance(phi):
        return np.sqrt(
            r1*r1+r2*r2
            -2*r1*r2*np.cos(phi)
            +(z1-z2)**2
        )

    reference0 = (
        quad(
            lambda p: 1/distance(p),
            0, 2*np.pi,
            epsabs=1e-11,
        )[0]/(8*np.pi**2)
    )

    reference1 = (
        quad(
            lambda p: np.cos(p)/distance(p),
            0, 2*np.pi,
            epsabs=1e-11,
        )[0]/(8*np.pi**2)
    )

    assert np.isclose(
        model.kernel[a, b],
        reference0,
        rtol=1e-10,
    )

    assert np.isclose(
        model.magkernel[a, b],
        reference1,
        rtol=1e-8,
        atol=1e-12,
    )


def test_stationary_source_gauss_and_individual_noether(base):
    _, result, _ = base

    assert max(abs(
        np.asarray(result["individual_Noether"])-400
    )) < 1e-8

    assert abs(result["net_X_charge"]) < 1e-9
    assert result["free_coulomb_residual_inf"] < 1e-9

    assert max(
        result["scalar_equation_weighted_L2"]
    ) < 2e-5

    assert result["optimizer"]["gradient_inf"] < 2e-5
    assert 2.7 < result["source_separation"] < 3.05


def test_multiple_seeds_and_same_action_overlap_competitor(base):
    _, reference, _ = base

    options = []

    for start in (0, .5, 6):
        model = CoulombSource(Spec(
            nr=18,
            L=12,
            seed_separation=start,
        ))

        result, _ = model.solve(350)
        options.append(result)

    assert options[0]["source_separation"] == pytest.approx(
        0, abs=1e-7
    )

    assert (
        options[0]["canonical_energy_NOT_J"]
        >reference["canonical_energy_NOT_J"]+.25
    )

    assert abs(
        options[1]["source_separation"]
        -options[2]["source_separation"]
    ) < 1e-4

    assert abs(
        options[1]["canonical_energy_NOT_J"]
        -options[2]["canonical_energy_NOT_J"]
    ) < 1e-5


def test_zero_contact_repulsion_control():
    model = CoulombSource(Spec(
        nr=18, L=12, g=0
    ))

    result, fields = model.solve(350)
    y = model.induced_Y_free_space(fields)

    assert abs(result["source_separation"]) < .005
    assert y["Y_current_L2"] < 1e-4


def test_stronger_X_charge_collapse_control():
    model = CoulombSource(Spec(
        nr=18, L=12, e=.14
    ))

    result, fields = model.solve(350)
    y = model.induced_Y_free_space(fields)

    assert abs(result["source_separation"]) < .005
    assert y["Y_current_L2"] < 1e-4


def test_free_Y_and_alpha_sign_controls(base):
    model, _, fields = base

    plus = model.induced_Y_free_space(
        fields, alpha=1.
    )
    minus = model.induced_Y_free_space(
        fields, alpha=-1.
    )
    zero = model.induced_Y_free_space(
        fields, alpha=0.
    )

    assert plus["Y_current_L2"] > .2
    assert plus["Y_magnetic_energy_CANONICAL_NOT_J"] > .1
    assert plus["portal_P_abs_integral"] > 1

    assert minus["Y_magnetic_dipole"] == pytest.approx(
        -plus["Y_magnetic_dipole"],
        rel=1e-10,
    )

    assert minus["Y_magnetic_energy_CANONICAL_NOT_J"] == pytest.approx(
        plus["Y_magnetic_energy_CANONICAL_NOT_J"],
        rel=1e-10,
    )

    assert zero["Y_current_L2"] < 1e-12
    assert zero["Y_magnetic_energy_CANONICAL_NOT_J"] < 1e-12


def test_fixed_spacing_domain_convergence(large, far):
    _, a, fa = large
    model, b, fb = far

    relative_sep = abs(
        a["source_separation"]-b["source_separation"]
    )/abs(b["source_separation"])

    assert relative_sep < .002

    assert abs(
        a["canonical_energy_NOT_J"]
        -b["canonical_energy_NOT_J"]
    ) < .01

    ya = large[0].induced_Y_free_space(fa)
    yb = model.induced_Y_free_space(fb)

    assert abs(
        ya["Y_current_L2"]-yb["Y_current_L2"]
    ) < .005

    assert b["outer_80pct_scalar_tail"] < 1e-4


def test_refinement_softens_translation_and_rotation_modes(large, fine):
    coarse_model, _, coarse_fields = large
    fine_model, _, fine_fields = fine

    coarse_t = coarse_model.translation_ward(
        coarse_fields
    )["translation_tangent_rayleigh"]

    fine_t = fine_model.translation_ward(
        fine_fields
    )["translation_tangent_rayleigh"]

    coarse_r = coarse_model.rotation_ward(
        coarse_fields
    )["rotation_normalized_curvature"]

    fine_r = fine_model.rotation_ward(
        fine_fields
    )["rotation_normalized_curvature"]

    assert fine_t < coarse_t
    assert fine_r < coarse_r
    assert fine_t < .001
    assert fine_r < .001


def test_k1_Gauss_mode_softens_when_rotation_is_included(large, fine):
    a = large[0].k1_density_screen(large[2])
    b = fine[0].k1_density_screen(fine[2])

    assert a["min_mode"] > 0
    assert b["min_mode"] > 0
    assert b["min_mode"] < a["min_mode"]
    assert b["min_mode"] < .0003

    assert b["included_rigid_rotation"]


def test_diagonal_self_quadrature_convergence():
    separations = []

    for order in (4, 8, 12):
        model = CoulombSource(
            Spec(nr=18, L=12),
            order,
        )
        result, _ = model.solve(350)
        separations.append(result["source_separation"])

    assert abs(
        separations[2]-separations[1]
    ) < abs(
        separations[1]-separations[0]
    )

    assert abs(
        separations[2]-separations[1]
    ) < .002


def test_k1_coupled_electrostatic_density_quadratic(base):
    model, _, fields = base

    a = np.zeros((2, model.cells))

    a[0] = (
        .3*(model.rho/3)
        *np.exp(-(
            (model.rho-3)**2
            +(model.z-2)**2
        )/(2*3**2))
    )

    Q = model.free_density_quadratic(
        fields, 1, a
    )

    assert Q > 0
    assert np.isfinite(Q)


def test_research_scope_remains_explicit(base):
    _, result, _ = base

    assert result["free_space_status"].startswith(
        "SELF_CONSISTENT_DISCRETE"
    )
    assert result["self_quadrature_order"] == 8
    assert result["kernel_symmetry_inf"] < 1e-12
