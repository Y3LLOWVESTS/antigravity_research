"""PH6 focused source–carrier–neutral action and conservation tests."""
from dataclasses import replace

import numpy as np
import pytest

from antigravity_research.agminer.hook17_ph6_same_action_bridge import (
    Spec, shape, D, initial, state_data, rhs, run_case,
    action_lagrangian, action_legendre_residual,
    symbolic_checks, provenance, run,
)


def sample_state():
    spec = Spec(n=96)
    y = initial(spec)
    n = spec.n
    x = np.arange(n)*spec.length/n-spec.length/2

    y[:n] = .02*np.sin(2*np.pi*x/spec.length)
    y[n:2*n] = .01*np.cos(4*np.pi*x/spec.length)
    y[2*n:3*n] = .013*np.sin(4*np.pi*x/spec.length)
    y[3*n:4*n] = .02*np.cos(2*np.pi*x/spec.length)
    y[4*n+1] = .021
    y[4*n+3] = .15
    y[4*n+5] = .012

    return spec, y


def L_of_state(spec, y, override=None):
    d = state_data(y, spec)

    Z, pZ, qx, vx, X, Ux, qy, vy, Y, Uy = d["tail"]

    args = {
        "a": d["a"].copy(),
        "b": d["b"].copy(),
        "ua": d["ua"].copy(),
        "ub": d["ub"].copy(),
        "Z": float(Z), "V": d["V"],
        "qx": float(qx), "vx": float(vx),
        "X": float(X), "Ux": float(Ux),
        "qy": float(qy), "vy": float(vy),
        "Y": float(Y), "Uy": float(Uy),
    }

    if override:
        args.update(override)

    return action_lagrangian(spec=spec, **args)


def finite_difference(name, value, spec, y, h=2e-6):
    if isinstance(value, np.ndarray):
        plus = value.copy()
        minus = value.copy()
        plus[0] += h
        minus[0] -= h
    else:
        plus, minus = value+h, value-h

    return (
        L_of_state(spec, y, {name: plus})
        - L_of_state(spec, y, {name: minus})
    ) / (2*h)


def test_exact_symbolic_variations():
    result = symbolic_checks()
    assert result["first_variations"] == 4
    assert result["matter_curvature"] == "PASS_EXACT"


def test_discrete_derivative_is_skew_adjoint():
    rng = np.random.default_rng(17)
    a = rng.normal(size=80)
    b = rng.normal(size=80)

    assert abs(
        np.dot(a, D(b, .1))
        + np.dot(D(a, .1), b)
    ) < 1e-12


@pytest.mark.parametrize("n", [96, 144, 256])
def test_source_shape_normalization_and_center_derivative(n):
    spec = replace(Spec(), n=n)
    dx = spec.length/n
    x = np.arange(n)*dx-spec.length/2

    f, fx = shape(x, -1.23, spec.width, dx)

    assert np.all(f >= 0)
    assert dx*np.sum(f) == pytest.approx(1, abs=1e-12)
    assert abs(dx*np.sum(fx)) < 1e-12

    h = 1e-5
    fp = shape(x, -1.23+h, spec.width, dx)[0]
    fm = shape(x, -1.23-h, spec.width, dx)[0]

    assert np.max(
        abs((fp-fm)/(2*h)+fx)
    ) < 1e-5


def test_independent_action_legendre_energy():
    spec, y = sample_state()
    assert abs(action_legendre_residual(y, spec)) < 1e-12


def test_field_and_neutral_canonical_momenta():
    spec, y = sample_state()
    d = state_data(y, spec)
    n = spec.n
    dx = spec.length/n

    assert finite_difference(
        "ua", d["ua"], spec, y
    ) == pytest.approx(dx*y[2*n], abs=2e-8)

    assert finite_difference(
        "ub", d["ub"], spec, y
    ) == pytest.approx(dx*y[3*n], abs=2e-8)

    assert finite_difference(
        "V", d["V"], spec, y
    ) == pytest.approx(y[4*n+1], abs=2e-8)


def test_neutral_and_source_center_forces_from_same_action():
    spec, y = sample_state()
    n = spec.n
    d = state_data(y, spec)
    f = rhs(0, y, spec)

    Z, pZ, qx, vx, X, Ux, qy, vy, Y, Uy = d["tail"]

    for name, value, index, mass in (
        ("Z", Z, 4*n+1, 1.),
        ("X", X, 4*n+5, spec.source_mass),
        ("Y", Y, 4*n+9, spec.source_mass),
    ):
        assert finite_difference(
            name, float(value), spec, y
        ) == pytest.approx(mass*f[index], abs=1e-7)


def test_field_euler_lagrange_variations():
    spec, y = sample_state()
    d = state_data(y, spec)
    f = rhs(0, y, spec)
    n = spec.n
    dx = spec.length/n

    assert finite_difference(
        "a", d["a"], spec, y
    ) == pytest.approx(dx*f[2*n], abs=2e-8)

    assert finite_difference(
        "b", d["b"], spec, y
    ) == pytest.approx(dx*f[3*n], abs=2e-8)


def test_source_off_equilibrium():
    spec = replace(Spec(), q0_x=0, q0_y=0)
    result = run_case(spec, samples=41)

    assert abs(
        result["neutral_exact_momentum_change"]
    ) < 1e-11

    assert abs(
        result["final"]["field_energy"]
    ) < 1e-11


@pytest.mark.parametrize(
    "spec",
    [
        Spec(),
        replace(Spec(), alpha=0, beta=0),
        replace(Spec(), density_mass=0),
        replace(Spec(), alpha=0),
        replace(Spec(), beta=0),
        replace(Spec(), q0_y=0),
    ],
)
def test_reduced_energy_conservation(spec):
    result = run_case(
        replace(spec, tmax=2.2),
        samples=81,
    )

    assert result["max_energy_drift"] < 1e-9
    assert result["impulse_quadrature_error"] < 1e-5
    assert result["minimum_support_gap"] > 0


def test_mixed_portal_source_driven_neutral_response():
    result = run_case(Spec())

    assert result["neutral_exact_momentum_change"] > 0
    assert result["maximum_chi_neutral"] < 0
    assert result["minimum_K"] > 0
    assert result["minimum_frozen_D"] > 0
    assert result["minimum_sigma_prime_neutral"] > 0
    assert result["maximum_neutral_speed"] < .1
    assert result["max_energy_drift"] < 1e-9
    assert result["max_total_momentum_drift"] < 6e-4


def test_portal_off_and_matter_off_controls():
    for spec in (
        replace(Spec(), alpha=0, beta=0),
        replace(Spec(), density_mass=0),
    ):
        result = run_case(spec)

        assert abs(
            result["neutral_exact_momentum_change"]
        ) < 1e-10


def test_even_portal_negative_impulse_control():
    result = run_case(replace(Spec(), alpha=0))

    assert result["neutral_exact_momentum_change"] < 0
    assert result["neutral_negative_impulse"] < 0


def test_linear_portal_nonzero_force_but_bad_curvature():
    result = run_case(replace(Spec(), beta=0))

    assert result["neutral_exact_momentum_change"] > 0
    assert result["maximum_chi_neutral"] > 0


def test_grid_momentum_residual_refines():
    medium = run_case(replace(Spec(), n=256))
    fine = run_case(replace(Spec(), n=384))

    assert (
        fine["max_total_momentum_drift"]
        < .55*medium["max_total_momentum_drift"]
    )

    assert abs(
        fine["neutral_exact_momentum_change"]
        - medium["neutral_exact_momentum_change"]
    ) < .02*abs(
        fine["neutral_exact_momentum_change"]
    )


def test_fail_closed_bad_setup():
    with pytest.raises(ValueError):
        initial(replace(Spec(), density_mass=-.1))

    with pytest.raises(ValueError):
        initial(replace(Spec(), n=47))

    with pytest.raises(ValueError):
        initial(replace(Spec(), width=50))

    spec, y = sample_state()
    d = state_data(y, spec)

    with pytest.raises(ValueError):
        L_of_state(spec, y, {"V": 1.1})


def test_missing_provenance_does_not_promote(tmp_path):
    record = provenance(tmp_path)
    assert all(
        item["status"] == "MISSING"
        for item in record.values()
    )

    result = run(tmp_path)

    assert result["gates"]["P0_PROVENANCE"] == "UNRESOLVED"
    assert result["gates"]["006D_REPLACED"] == "NO"
    assert result["gates"]["P3_EARTH_DOWN_WHOLE_CRAFT_UP"] == (
        "NOT_DERIVED"
    )
