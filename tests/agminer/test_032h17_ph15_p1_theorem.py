"""Focused PH15-P1 theorem and honest scientific-classification tests.

These tests protect exact action variations, known zero controls,
the restricted counterwinding algebra, and unearned-promotion guards.
They do not establish an on-shell nonspherical physical source.
"""

from functools import lru_cache

from antigravity_research.agminer.hook17_ph15_p1_theorem import run


@lru_cache(maxsize=1)
def result():
    return run()


def test_ph15_p1_exact_variations_and_controls():
    data = result()
    checks = data["checks"]

    assert checks["matter_trace_variation"] == "PASS_EXACT"
    assert checks["Lorentzian_epsilon_contraction"] == "PASS_EXACT"
    assert checks["four_constitutive_signs"] == "PASS_EXACT"
    assert checks["independent_FD_variation"] == "PASS_CONVERGENCE"
    assert checks["axisymmetric_scalar_X_variations"] == "PASS_EXACT"

    assert checks["PH14_spherical_Y"] == "EXACT_ZERO_BY_SYMMETRY"
    assert checks["aligned_electrostatic_induction"] == "EXACT_ZERO"


def test_ph15_p1_no_unearned_physical_promotion():
    data = result()

    assert data["classification"] == "YELLOW_ANALYTIC_CHANNEL_OPEN"
    assert data["on_shell_axisymmetric_existence"] == "NOT_SOLVED"
    assert data["on_shell_Y_response"] == "NOT_SOLVED"
    assert data["whole_spacecraft_force"] == "NOT_DERIVED"
    assert data["006D_replaced"] is False
    assert data["M5V_status"] == "FROZEN"
