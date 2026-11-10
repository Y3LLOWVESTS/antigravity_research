"""R3X3B9 exact action-Hessian and conservative-claims tests."""
from pathlib import Path
import importlib.util
import math

import pytest
from sympy import Rational, symbols, diff, simplify

from antigravity_research.agminer.hook17_fdual_f_r3x3b9_reciprocity_gate import (
    result,
    one_auxiliary_gate,
    two_auxiliary_gate,
)

PATH = (
    Path(__file__).resolve().parents[2]
    / "simulations"
    / "032h17a12d1r3x3b9_reciprocity_preflight.py"
)

SPEC = importlib.util.spec_from_file_location(
    "r3x3b9_runner", PATH
)
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


def test_one_aux_schur():
    assert one_auxiliary_gate()["schur_complement_verified"]


def test_matter_loading_reciprocity():
    assert one_auxiliary_gate()[
        "matter_and_carrier_mixed_derivatives_equal"
    ]


def test_cancellation_removes_same_force():
    assert one_auxiliary_gate()[
        "exact_algebraic_cancellation_removes_force_kernel"
    ]


def test_nontrivial_field_sector_leftover():
    row = one_auxiliary_gate()
    assert row["remaining_p_squared_term"]
    assert not row[
        "remaining_nonlinear_field_stability_certified"
    ]


def test_two_aux_schur():
    assert two_auxiliary_gate()[
        "two_auxiliary_schur_complement_verified"
    ]


def test_two_aux_determinant():
    assert two_auxiliary_gate()[
        "hessian_determinant"
    ] == "-k**2 + m1*m2"


def test_two_aux_exact_witness():
    assert two_auxiliary_gate()[
        "rank_two_rational_witness"
    ] == "10/29"


@pytest.mark.parametrize(
    "a,g,h,m2",
    [
        (1, 2, 3, 5),
        (2, 1, -1, 3),
        (0, 1, 7, 3),
        (3, 2, -1, 1),
        (1, 5, 3, 6),
    ],
)
def test_rational_mixed_derivative_identity(a, g, h, m2):
    t, p, chi = symbols("T P chi")

    lagrangian = (
        a*t*p
        + (g*p + h*t)*chi
        - Rational(m2, 2)*chi**2
    )

    chi_star = (g*p + h*t)/m2
    effective = simplify(lagrangian.subs(chi, chi_star))

    assert simplify(
        diff(effective, t, p)
        - diff(effective, p, t)
    ) == 0

    assert simplify(
        diff(effective, t, p)
        - (a + Rational(g*h, m2))
    ) == 0


def test_peak_beta_reference():
    peak = RUNNER.primary_peak_loading_gate()[
        "peak_epsilon_load"
    ]

    assert math.isclose(
        peak,
        18987.283771593688,
        rel_tol=1e-12,
    )


def test_missing_prior_data_is_explicit(tmp_path):
    row = RUNNER.prior_spherical_audit(
        tmp_path / "missing.json"
    )
    assert not row["available"]


def test_claim_scope_preserved():
    row = result()

    assert row[
        "original_r3b_1p542916_j_preloaded_preserved"
    ]
    assert not row["dynamical_derivative_compensators_excluded"]
    assert not row["different_loaded_field_profiles_excluded"]
    assert not row["physical_antigravity_model_found"]


def test_runner_does_not_overclaim(tmp_path):
    row = RUNNER.run(tmp_path)

    assert not row["comparison_to_r3b"][
        "spherical_bound_applies_to_r3b_torus"
    ]
    assert row["r3x3b8_prior"]["available"] is False
    assert not row["006d_replaced"]
