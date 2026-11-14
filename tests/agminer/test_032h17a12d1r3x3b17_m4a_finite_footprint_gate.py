"""B17-M4A necessary-condition regression tests."""

import pytest

from antigravity_research.agminer.hook17_r3b_m4a_finite_footprint_gate import (
    local_column,
    r3b_normal_flux_integral,
    finite_footprint,
)
from antigravity_research.agminer.hook17_r3b_exterior_transmission import (
    normalized_r3b_fit,
)
from antigravity_research.agminer.hook17_r3b_earth_interface import (
    theta_for_density,
)
from antigravity_research.agminer.hook17_r3b_layer_variational_gate import (
    axial_slab_variational,
    Layer,
)


@pytest.fixture(scope="module")
def fit():
    return normalized_r3b_fit(0.05)


def test_column_recovers_m2():
    a = theta_for_density(1.2)
    b = theta_for_density(2000)

    local = local_column(a, b, 0.01, 0.01, 17.0, 17.0)
    m2 = axial_slab_variational(
        (
            Layer("air", 0.01, 1.2),
            Layer("ground", 0.01, 2000),
        ),
        17.0,
        1000.0,
        17.0,
    )

    assert local["optimized_j_per_m2"] == pytest.approx(
        m2["optimal"]["carrier_energy_j_per_m2"],
        rel=1e-12,
    )
    assert local["fixed_j_per_m2"] == pytest.approx(
        m2["fixed_source"]["carrier_energy_j_per_m2"],
        rel=1e-12,
    )


def test_optimal_source_adjustment_lower():
    x = local_column(0, -125, 0.02, 0.01, 3, 3)
    assert x["optimized_j_per_m2"] < x["fixed_j_per_m2"]


def test_zero_field_no_energy():
    x = local_column(0, -300, 0.01, 0.02, 0, 0)
    assert x["optimized_j_per_m2"] == 0
    assert x["fixed_j_per_m2"] == 0


def test_metric_response_sign_and_huge_ratio():
    x = local_column(
        theta_for_density(1.2),
        theta_for_density(2000),
        0.01,
        0.01,
        1,
        1,
    )
    assert x["optimized_metric_ratio_air_to_r3b"] < -1e6
    assert x["optimized_metric_ratio_ground_to_r3b"] > 1e6


def test_radial_integral_positive_and_monotonic(fit):
    values = [
        r3b_normal_flux_integral(fit, r, 3, 64)
        for r in (0.5, 1.0, 2.0, 4.0)
    ]
    assert all(v > 0 for v in values)
    assert all(b > a for a, b in zip(values, values[1:]))


def test_quadrature_refinement(fit):
    a = r3b_normal_flux_integral(fit, 2, 3, 40)
    b = r3b_normal_flux_integral(fit, 2, 3, 80)
    assert abs(a-b)/b < 1e-8


def test_altitude_attenuation(fit):
    low = finite_footprint(
        fit, 2, 0
    )["optimized_conditional_carrier_j"]

    high = finite_footprint(
        fit, 2, 5
    )["optimized_conditional_carrier_j"]

    assert low > high > 0


def test_field_sign_invariance(fit):
    a = r3b_normal_flux_integral(fit, 2, 3)

    flipped = {
        **fit,
        "coefficients": -fit["coefficients"],
    }

    b = r3b_normal_flux_integral(flipped, 2, 3)
    assert a == pytest.approx(b, rel=1e-13)


def test_portal_scale_and_metric_not_preserved(fit):
    low = finite_footprint(fit, 2, 0, 1000)
    high = finite_footprint(
        fit, 2, 0, 21147, matched_sigma=True
    )

    assert (
        low["optimized_conditional_carrier_j"]
        > high["optimized_conditional_carrier_j"]
    )
    assert not low["retains_original_metric_response"]
    assert not high["retains_original_metric_response"]
    assert low["whole_craft_force_n"] is None


def test_input_validation(fit):
    for arguments in (
        {"radius_m": 0},
        {"portal_scale_ev": -1},
        {"clearance_m": -1},
        {"air_depth_m": 0},
        {"order": 1},
    ):
        with pytest.raises(ValueError):
            finite_footprint(fit, **arguments)


def test_full_simulation_claims_fail_closed():
    import importlib.util
    import sys
    from pathlib import Path

    path = (
        Path(__file__).resolve().parents[2]
        / "simulations"
        / "032h17a12d1r3x3b17_m4a_finite_footprint_gate.py"
    )

    spec = importlib.util.spec_from_file_location(
        "b17_m4a_sim", path
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    result = module.run(0.05, 40)

    assert result["preloaded_r3b_j"] == pytest.approx(
        1.5429162116460216,
        abs=5e-8,
    )
    assert result["whole_craft_force_n"] is None
    assert result["gravity_cancellation"] is None
    assert result["pure_field_lift"] is None
    assert not result["complete_energy_lt_10mj_certified"]
    assert not result["006d_replaced"]
