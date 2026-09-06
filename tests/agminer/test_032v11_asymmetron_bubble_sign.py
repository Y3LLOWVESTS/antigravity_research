import math

from antigravity_research.agminer.asymmetron_sign import (
    asymmetron_vacua,
    euclidean_bounce_radius,
    false_inside_outer_side_sign,
    leading_weyl_factor,
    radial_fifth_acceleration,
    static_bubble_critical_radius,
    static_bubble_second_derivative_at_critical,
    true_inside_outer_side_sign,
)


def test_032v11_vacua_are_always_opposite_sign_for_positive_kappa():
    for ratio in (1e-6, 1e-3, 1e-2, 0.1, 1.0, 10.0):
        v = asymmetron_vacua(1.0, ratio)
        assert v.phi_plus > 0.0
        assert v.phi_minus < 0.0


def test_032v11_true_inside_external_side_is_inward():
    assert true_inside_outer_side_sign() == "INWARD"


def test_032v11_false_inside_external_side_is_inward():
    assert false_inside_outer_side_sign() == "INWARD"


def test_032v11_wall_core_is_minimum_of_leading_weyl_factor():
    M = 2.0
    assert leading_weyl_factor(0.0, M) == 1.0
    assert leading_weyl_factor(0.5, M) > 1.0
    assert leading_weyl_factor(-0.5, M) > 1.0


def test_032v11_force_points_toward_wall_on_both_sides():
    # Coordinate increases from true (+phi) interior to false (-phi)
    # exterior, so dphi/dr < 0 across the wall.
    inner = radial_fifth_acceleration(+0.5, -1.0, 2.0)
    outer = radial_fifth_acceleration(-0.5, -1.0, 2.0)
    assert inner > 0.0
    assert outer < 0.0


def test_032v11_free_static_bubble_stationary_point_is_unstable():
    sigma = 3.0
    epsilon = 2.0
    rc = static_bubble_critical_radius(sigma, epsilon)
    rb = euclidean_bounce_radius(sigma, epsilon)
    assert math.isclose(rc, 3.0)
    assert math.isclose(rb, 4.5)
    assert static_bubble_second_derivative_at_critical(sigma) < 0.0
