"""Exact symbolic tests of the scoped R3X3B5 action gate."""
from sympy import Matrix, simplify, symbols

from antigravity_research.agminer.hook17_r3x3b5_axion_action_gate import (
    all_gates,
    action_variation_gate,
    exact_mirror_no_go,
    tensor_non_degeneracy,
)


def test_tensor():
    assert tensor_non_degeneracy()[
        "det_equals_E_dot_B_squared"
    ]


def test_full_rank_nonzero_eb():
    f = Matrix([
        [0, 0, 0, 2],
        [0, 0, -3, 0],
        [0, 3, 0, 0],
        [-2, 0, 0, 0],
    ])
    assert f.det() == 36


def test_rank_deficient_zero_eb():
    f = Matrix([
        [0, 0, 0, 2],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [-2, 0, 0, 0],
    ])
    assert f.det() == 0


def test_matter_interface_derivative():
    assert action_variation_gate()[
        "maxwell_matter_interface_derivative_of_theta_by_tau"
    ] == "4*a*kappa"


def test_axion_gradient_derivative():
    assert action_variation_gate()[
        "maxwell_axion_derivative_of_theta_by_a"
    ] == "gamma + 4*kappa*tau"


def test_action_scalar_source_linked():
    a, g, k, t, p = symbols("a gamma kappa tau P")
    assert simplify(
        4*a*(g/4+k*t)*p - (g+4*k*t)*a*p
    ) == 0


def test_bare_gamma_vacuum():
    assert exact_mirror_no_go()[
        "vacuum_theta_with_bare_term"
    ] == "a*gamma"


def test_two_point_incompatibility():
    assert exact_mirror_no_go()[
        "bare_gamma_nonzero_varying_P_exact_mirror"
    ] == "INCOMPATIBLE"


def test_no_bare_interface():
    assert "NO_NONZERO_SIGMA" in exact_mirror_no_go()[
        "no_bare_gamma_strict_interface_silence"
    ]


def test_metric_noether_not_certified():
    assert not action_variation_gate()[
        "full_metric_noether_identity_certified"
    ]


def test_alternatives_remain_open():
    assert not exact_mirror_no_go()[
        "different_loaded_field_profiles_excluded"
    ]


def test_claims_are_conservative():
    result = all_gates()
    assert result[
        "original_r3b_preloaded_capacity_preserved"
    ]
    assert not result["006d_replaced"]
    assert not result["physical_antigravity_model_found"]
    assert not result["new_compensator_certified"]
