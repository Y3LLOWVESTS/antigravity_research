"""B16 — finite-mass response and exact homotopy equivalence."""

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest


MODULE = (
    Path(__file__).resolve().parents[2]
    / "simulations"
    / "032h17a12d1r3x3b16_weak_loading_mass_response.py"
)

spec = importlib.util.spec_from_file_location(
    "b16_mass_response",
    MODULE,
)

m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)


@pytest.fixture(scope="module")
def response():
    return m.Response(0.075)


def test_finite_mass_and_zero_mass_control(response):
    null = response.evaluate(0.0)

    assert null["actual_payload_mass_kg"] == 0.0
    assert null["massless_control"] is True
    assert null["density_weighted_com_m_s2"] is None
    assert null["net_force_n"] == 0.0
    assert null["everywhere_outward"] is False

    assert abs(
        null["min_loaded_m_s2"] - m.TARGET
    ) < 1e-5

    assert abs(response.ref_mass - 1.0) < 0.005

    assert abs(
        m.physical_standoff_m() - 1.0
    ) < 1e-12


def test_force_identity_and_com_weighting(response):
    for f in (1e-6, 1e-4, 0.1, 1.0):
        result = response.evaluate(f)

        assert abs(
            result["net_force_n"]
            - (
                result["positive_force_n"]
                + result["negative_force_n"]
            )
        ) < 1e-10

        assert abs(
            result["net_force_n"]
            / result["actual_payload_mass_kg"]
            - result["density_weighted_com_m_s2"]
        ) < 1e-9

        assert (
            0.0
            <= result["negative_mass_fraction"]
            <= 1.0
        )

        assert (
            result["loaded_solver_relative_residual"]
            < 1e-8
        )


def test_weak_finite_matter_and_heavy_failure(response):
    weak = response.evaluate(1e-6)
    heavy = response.evaluate(1.0)

    assert weak["everywhere_outward"] is True
    assert weak["everywhere_ge_1g"] is True

    assert weak["positive_force_n"] > 0.0
    assert weak["negative_force_n"] == 0.0

    assert heavy["min_loaded_m_s2"] < 0.0
    assert heavy["everywhere_outward"] is False
    assert heavy["negative_mass_fraction"] > 0.0


def test_independent_density_matches_homotopy(response):
    result = response.direct_scaled_operator_equivalence(
        1e-4
    )

    assert (
        result["relative_beta_difference"]
        < 1e-12
    )

    assert (
        result["relative_solution_difference"]
        < 1e-10
    )

    assert (
        result["independent_operator_residual"]
        < 1e-8
    )


def test_scoped_threshold_and_historical_overlap(response):
    one_g = response.bracket_first_transition(
        "min_loaded_m_s2",
        m.TARGET,
    )

    outward = response.bracket_first_transition(
        "min_loaded_m_s2",
        0.0,
    )

    assert one_g is not None
    assert outward is not None

    assert (
        1e-5
        < one_g["last_passing_fraction"]
        < 1.2e-5
    )

    assert (
        2.5e-5
        < outward["last_passing_fraction"]
        < 3e-5
    )

    assert (
        one_g["first_failing_fraction"]
        < outward["last_passing_fraction"]
    )


def test_invalid_density_fractions_fail_closed(response):
    with pytest.raises(ValueError):
        response.evaluate(-1e-5)

    with pytest.raises(ValueError):
        response.evaluate(1.1)

    with pytest.raises(ValueError):
        response.evaluate(np.nan)
