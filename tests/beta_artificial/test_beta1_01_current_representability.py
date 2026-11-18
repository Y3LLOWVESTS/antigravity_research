"""Independent BETA1-01 source/current/multipole/portal tests."""

import math

import numpy as np
import pytest

from antigravity_research.beta_artificial.beta1_01_current_representability import (
    Target,
    target_current,
    exact_target_moments,
    independent_moments,
    potential_boundary_screen,
    exact_symbolic_conditions,
    report,
)

from antigravity_research.agminer.hook17_r3b_m5i_continuum_source import (
    SourceSpec,
    continuum_current,
    reference_moments,
)


@pytest.fixture(scope="module")
def data():
    return report()


def test_01_m5i_exact_source_match():
    s = Target()
    m = SourceSpec()

    r = np.array([.75, 1.0, 1.15, 1.3, 1.57])
    z = np.array([-.25, -.2, .0, .2, .4])

    rho, j = target_current(r, z, s)
    rh0, j0 = continuum_current(r, z, m)

    np.testing.assert_allclose(
        rho, rh0, atol=0., rtol=0.
    )

    np.testing.assert_allclose(
        j, j0, atol=0., rtol=0.
    )


def test_02_charge_parity_and_current_parity():
    r = 1.1
    z = .19

    p, j = target_current(r, z)
    mn, jn = target_current(r, -z)

    assert p > 0
    assert j > 0

    assert abs(p+mn) < 1e-14
    assert j == jn


def test_03_zero_monopole_exact(data):
    assert data[
        "target_exact_moments"
    ]["net_charge"] == 0


def test_04_exact_dipole_positive(data):
    assert data[
        "target_exact_moments"
    ]["electric_dipole_z"] > 0


def test_05_exact_magnetic_moment_positive(data):
    assert data[
        "target_exact_moments"
    ]["magnetic_dipole_z"] > 0


def test_06_independent_analytic_electric_moment():
    s = Target()

    R = s.radial_center_m
    a = s.radial_halfwidth_m
    b = s.axial_halfwidth_m

    expected = math.pi**2*a*b*b*R/42

    assert math.isclose(
        exact_target_moments(s)[
            "electric_dipole_z"
        ],
        expected,
        rel_tol=1e-14,
    )


def test_07_moments_gauss64_close(data):
    errors = data[
        "independent_quadrature_moments"
    ]["64"]["relative_or_absolute_errors"]

    assert max(errors.values()) < 2e-8


def test_08_moments_gauss112_close(data):
    errors = data[
        "independent_quadrature_moments"
    ]["112"]["relative_or_absolute_errors"]

    assert max(errors.values()) < 2e-8


def test_09_legacy_m5i_independent_reference():
    s = SourceSpec()

    ref = reference_moments(
        s, order=100
    )

    a = exact_target_moments()

    assert abs(
        ref["electric_dipole_z_integral"]
        -a["electric_dipole_z"]
    ) < 1e-10

    assert abs(
        ref["magnetic_dipole_z_integral"]
        -a["magnetic_dipole_z"]
    ) < 1e-10


def test_10_target_jphi_norm_strictly_nonzero(data):
    assert data[
        "target_exact_moments"
    ]["azimuthal_current_L2_squared"] > 0


def test_11_p10_microscopic_x_jphi_zero():
    checks, _ = exact_symbolic_conditions()

    assert checks[
        "nonwinding_Aphi0_X_current_exact_null"
    ]


def test_12_finite_energy_Aphi_coercivity():
    checks, _ = exact_symbolic_conditions()

    assert checks[
        "azimuthal_X_energy_positive_coefficient"
    ]

    # Independent finite-dimensional positive
    # operator control, not a full PDE certificate.

    D = np.array([
        [2., -1., 0.],
        [-1., 2., -1.],
        [0., -1., 2.],
    ])

    mass = np.diag([
        .02, .08, .04
    ])

    assert np.linalg.eigvalsh(
        D+mass
    ).min() > 0


def test_13_induced_y_jacobian_vanishes_at_A0_stationary():
    checks, _ = exact_symbolic_conditions()

    assert checks[
        "induced_Y_critical_A0_null"
    ]


def test_14_upper_lobe_interior_margin_coarse(data):
    assert data[
        "potential_interior_extremum_screens"
    ][0]["screen_pass"]


def test_15_upper_lobe_interior_margin_refined(data):
    assert data[
        "potential_interior_extremum_screens"
    ][1]["screen_pass"]


def test_16_boundary_margin_convergence_screen(data):
    assert data[
        "potential_margin_cross_resolution_abs"
    ] < 5e-5


def test_17_potential_z0_null(data):
    assert all(
        abs(row["z0_potential_parity_check"])
        < 1e-9
        for row in data[
            "potential_interior_extremum_screens"
        ]
    )


def test_18_m5i_jphi_nonzero_at_interior(data):
    assert all(
        row["interior_jphi_target"] > .2
        for row in data[
            "potential_interior_extremum_screens"
        ]
    )


def test_19_symbolic_portal_lambda_p_identity():
    checks, _ = exact_symbolic_conditions()

    assert checks[
        "portal_lambda_P0_identity"
    ]


def test_20_frozen_magnetic_eigen_scopes():
    checks, formula = exact_symbolic_conditions()

    assert checks[
        "frozen_magnetic_Y_parallel_eigenvalue"
    ]

    assert checks[
        "beta0_alpha0_free_positive"
    ]

    assert (
        "NOT full constrained"
        in formula[
            "frozen_magnetic_Y_scope"
        ]
    )


def test_21_reject_full_theory_promotion(data):
    status = data["mechanism_status"]

    assert status[
        "P10_original_induced_Y"
    ] == "PRESERVED_NOT_DISPROVEN"

    assert status[
        "earth_force"
    ] == "NOT_DERIVED"

    assert status[
        "physical_transfer"
    ] == "NOT_AUTHORIZED"


def test_22_all_exact_scoped_checks(data):
    checks = data[
        "exact_symbolic_checks"
    ]

    assert len(checks) == 7
    assert all(checks.values())


def test_23_P7_winding_not_repromoted(data):
    assert (
        "P7"
        in data["mechanism_status"][
            "winding_or_new_Y_source"
        ]
    )


def test_24_no_SI_energy_claim(data):
    assert data[
        "source_channels"
    ]["M5I_prescribed"] == (
        "INDEPENDENT_RHO_AND_JPHI_NOT_ONSHELL_MATTER"
    )
