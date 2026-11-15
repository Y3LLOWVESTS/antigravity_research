"""PH1 symbolic identities and independent frozen-source witnesses."""
import pytest
import numpy as np

from antigravity_research.agminer.hook17_ph1_physicalization_preflight import (
    Reference,
    analytic_checks,
    analytic_shape_moments,
    bump,
    independent_shape_quadrature,
    winding_scalar_current,
    neutral_charge_decomposition,
    run_preflight,
    frozen_dust_electric_hessian_eigenvalue,
)


def test_all_independent_analytic_identities():
    checks = analytic_checks()
    assert len(checks) >= 23
    assert all(
        v["status"] == "PASS_SCOPED"
        for v in checks.values()
    )


@pytest.mark.parametrize(
    "key",
    [
        "monopole",
        "electric_dipole_z",
        "magnetic_dipole_z",
    ],
)
def test_independent_continuum_moments(key):
    exact = analytic_shape_moments(Reference())[key]
    numerical = independent_shape_quadrature(Reference())[key]
    assert abs(exact-numerical) < 1e-10


@pytest.mark.parametrize(
    "x,y",
    [(0., 0.), (.2, .3), (-.4, .6), (.7, -.2), (.96, 0.)],
)
def test_scalar_azimuthal_current_matches_trial_shape(x, y):
    spec = Reference()
    B = float(bump(np.array(x), np.array(y)))
    r = spec.r0+spec.ar*x
    result = winding_scalar_current(r, B)

    assert result["j_phi"] == pytest.approx(
        B, rel=1e-13, abs=1e-14
    )
    assert result["j_time"] == 0
    assert result["angular_gradient_cost"] >= 0


@pytest.mark.parametrize(
    "y",
    [-1., -.75, -.2, 0., .25, .9, 1.],
)
def test_opposite_charges_are_nonnegative_and_match_odd_charge(y):
    B = (1-y*y)**5
    d = neutral_charge_decomposition(y, B)

    assert d["positive_density"] >= 0
    assert d["negative_density"] >= 0
    assert d["signed_charge"] == pytest.approx(
        y*B, abs=1e-14
    )


def test_reject_unphysical_kinematic_inputs():
    with pytest.raises(ValueError):
        winding_scalar_current(0., 1.)
    with pytest.raises(ValueError):
        winding_scalar_current(1., 1., charge=-1.)
    with pytest.raises(ValueError):
        neutral_charge_decomposition(1.1, .1)
    with pytest.raises(ValueError):
        analytic_shape_moments(Reference(power=3))


def test_no_automatic_physical_promotion(tmp_path):
    result = run_preflight(tmp_path)

    assert result["verdict"].startswith("YELLOW_")
    assert result["gates"][
        "PH1_P3_EARTH_DOWN_FULL_CRAFT_UP"
    ] == "NOT_DERIVED"
    assert result["gates"][
        "PH1_COMPLETE_STRICT_LT10MJ"
    ] == "NOT_CERTIFIED"
    assert result["gates"][
        "B11_M6_COMPLETE_SIGNED_IMPULSE"
    ] == "NOT_RUN"
    assert result["m5v_campaign"].startswith("FROZEN_")
    assert result["gates"][
        "PH1_P0_HISTORICAL_REFERENCE_PROVENANCE"
    ] == "UNRESOLVED"


def test_archival_sha_fail_closed_not_forged(tmp_path):
    module = tmp_path/"src/antigravity_research/agminer"
    module.mkdir(parents=True)
    (
        module/"hook17_r3b_m5v_unified_exterior_action.py"
    ).write_text("not the frozen source")

    result = run_preflight(tmp_path)

    assert result["archival"]["frozen_m5v_source"][
        "status"
    ] == "HASH_MISMATCH"
    assert result["gates"][
        "PH1_P0_HISTORICAL_REFERENCE_PROVENANCE"
    ] == "UNRESOLVED"


def test_loaded_kinetic_condition_gates_both_signs():
    eigenvalue = frozen_dust_electric_hessian_eigenvalue

    assert eigenvalue(1, 1, 0, 4) == -3
    assert eigenvalue(1, 1, 0, .0625) == .9375
    assert eigenvalue(0, 1, 0, 1) == 1

    with pytest.raises(ValueError):
        eigenvalue(-1, 1, 0, 1)
    with pytest.raises(ValueError):
        eigenvalue(1, 1, 0, float("nan"))


def test_scalar_winding_is_integer_valued():
    with pytest.raises(ValueError):
        winding_scalar_current(1., 1., winding=.5)
