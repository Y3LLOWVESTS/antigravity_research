"""Independent M5O source, material and action regression controls."""

import numpy as np
import pytest

from antigravity_research.agminer.hook17_r3b_m5o_fixed_box import (
    below,
    below_dedge,
    mesh,
    material,
    evaluate,
    DOMAINS,
)


@pytest.mark.parametrize("profile", ("c1", "c2"))
def test_exact_material_transition_derivative(profile):
    x = np.linspace(-5.0, -2.0, 200)
    width = 0.5
    edge = -3.5
    delta = 1e-5

    finite = (
        below(x, edge + delta, width, profile)
        - below(x, edge - delta, width, profile)
    ) / (2*delta)

    np.testing.assert_allclose(
        below_dedge(x, edge, width, profile),
        finite,
        atol=1e-8,
        rtol=1e-7,
    )


def test_fixed_outer_box():
    f = mesh(0.25, DOMAINS["compact"])

    assert f["zs"][0] == pytest.approx(-6.0)
    assert f["zs"][-1] == pytest.approx(8.0)

    with pytest.raises(ValueError):
        mesh(0.22, DOMAINS["compact"])


def test_translated_material_earth_only_derivative():
    f = mesh(0.25, DOMAINS["compact"])
    beta, dbeta, _ = material(
        f, 0.0625, 0.0, 0.5, "c2"
    )

    delta = 1e-4
    bp = material(f, 0.0625, delta, 0.5, "c2")[0]
    bm = material(f, 0.0625, -delta, 0.5, "c2")[0]

    np.testing.assert_allclose(
        (bp - bm)/(2*delta),
        dbeta,
        atol=1e-4,
        rtol=1e-4,
    )

    air = material(
        f, 0.0625, 0.0, 0.5, "c2", False
    )[0]
    assert np.any(beta != air)


def test_weighted_action_and_independent_derivative():
    r = evaluate(
        h=0.25,
        domain=DOMAINS["compact"],
        width=0.5,
        profile="c2",
        step=0.001,
    )

    assert r["stationarity_residual"] < 1e-9
    assert r["weighted_operator_asymmetry"] < 1e-10
    assert abs(
        r["derivative_resolve_difference_error_j_m"]
    ) < 0.05
    assert abs(
        r["derivative_H_difference_error_j_m"]
    ) < 0.05
    assert (
        r["source"]["net_charge_after_projection_rel"]
        < 1e-12
    )
    assert r["whole_craft_lift_certified"] is False


def test_negative_controls():
    for kwargs in (
        {"earth_present": False},
        {"zero_source": True},
    ):
        r = evaluate(
            h=0.25,
            domain=DOMAINS["compact"],
            width=0.5,
            profile="c2",
            do_resolve=False,
            **kwargs,
        )

        assert abs(r["derivative_analytic_j_m"]) < 1e-10


def test_historical_m5k_m5n_reproduction():
    r = evaluate(
        h=0.25,
        domain=DOMAINS["original"],
        width=0.25,
        profile="c1",
        step=0.001,
        center_action_audit=True,
    )

    assert r["derivative_H_finite_difference_j_m"] == (
        pytest.approx(-1.8335603471034372, abs=2e-6)
    )
    assert r["earth_minus_air_reduced_action_j"] == (
        pytest.approx(-7.743566757, abs=1e-6)
    )
    assert r["derivative_analytic_j_m"] == (
        pytest.approx(-1.8263520183756978, abs=1e-6)
    )


def test_c1_endpoint_derivative_step_bias():
    kwargs = {
        "h": 0.25,
        "domain": DOMAINS["original"],
        "width": 0.25,
        "profile": "c1",
        "do_resolve": False,
    }

    a = evaluate(step=0.001, **kwargs)
    b = evaluate(step=0.0001, **kwargs)

    assert (
        abs(a["derivative_H_difference_error_j_m"])
        > 7*abs(b["derivative_H_difference_error_j_m"])
    )
    assert abs(
        a["derivative_analytic_j_m"]
        - b["derivative_analytic_j_m"]
    ) < 1e-10
