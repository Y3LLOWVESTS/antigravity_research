import math

import pytest

from antigravity_research.agminer.kinetic_conformal import (
    StaticShiftCurrentGate,
    counterfactual_spherical_exterior_energy_j,
    goldstone_linear_dlnc_dy,
    goldstone_linear_jacobian_kinetic_eigenvalue,
    required_ln_a_gradient_per_m,
    scale_ev_for_counterfactual_energy,
    sign_flipped_linear_dlnc_dy,
    sign_flipped_linear_jacobian_kinetic_eigenvalue,
    static_acceleration_m_s2,
    static_shift_current_no_source,
    zgb_exponential_dlnc_dy,
    zgb_exponential_jacobian_kinetic_eigenvalue,
    zgb_gaussian_dlnc_dy,
    zgb_gaussian_jacobian_kinetic_eigenvalue,
)


def test_required_ln_a_gradient_matches_one_g_scale():
    value = required_ln_a_gradient_per_m(9.80665)
    assert math.isclose(value, 1.0911369672198218e-16, rel_tol=1e-14)


def test_published_minimal_goldstone_static_spacelike_sign_is_inward():
    y = 1.0e-8
    dy_dr = -1.0e-8
    assert goldstone_linear_jacobian_kinetic_eigenvalue(y) > 0.0
    assert static_acceleration_m_s2(goldstone_linear_dlnc_dy(y), dy_dr) < 0.0


def test_zgb_exponential_static_spacelike_sign_is_inward_and_invertible():
    y = 0.25
    assert zgb_exponential_jacobian_kinetic_eigenvalue(y) > 0.0
    assert static_acceleration_m_s2(zgb_exponential_dlnc_dy(y), -0.1) < 0.0


def test_zgb_gaussian_static_spacelike_sign_is_inward_and_invertible():
    y = 0.25
    assert zgb_gaussian_jacobian_kinetic_eigenvalue(y) > 0.0
    assert static_acceleration_m_s2(zgb_gaussian_dlnc_dy(y), -0.1) < 0.0


def test_sign_flipped_linear_target_has_outward_sign_and_invertible_small_y():
    y = 1.0e-6
    assert sign_flipped_linear_jacobian_kinetic_eigenvalue(y) > 0.0
    assert static_acceleration_m_s2(sign_flipped_linear_dlnc_dy(y), -0.1) > 0.0


def test_positive_shift_current_regular_isolated_static_branch_has_no_source():
    gate = StaticShiftCurrentGate(current_coefficient_min=0.2)
    assert static_shift_current_no_source(gate) is True
    assert gate.nontrivial_localized_static_gradient_allowed is False


def test_shift_current_gate_lists_real_evasions():
    for kwargs in (
        {"explicit_shift_current_source": True},
        {"imposed_boundary_flux": True},
        {"topological_or_defect_sector": True},
        {"time_dependent_shift_background": True},
    ):
        gate = StaticShiftCurrentGate(
            current_coefficient_min=0.2,
            **kwargs,
        )
        assert static_shift_current_no_source(gate) is False
        assert gate.nontrivial_localized_static_gradient_allowed is True


def test_counterfactual_spherical_profile_respects_no_intersection_and_invertibility():
    result = counterfactual_spherical_exterior_energy_j(
        scale_ev=1.0e6,
        source_radius_m=0.10,
        payload_center_m=0.30,
        payload_radius_m=0.10,
        target_acceleration_m_s2=9.80665,
    )
    assert result["y_source_surface"] < 1.0e-12
    assert result["jacobian_kinetic_eigenvalue_min"] > 0.999999999999
    assert result["exterior_scalar_energy_j"] > 1.0e8


def test_counterfactual_energy_scales_as_m_fourth_power():
    low = counterfactual_spherical_exterior_energy_j(
        scale_ev=1.0e5,
        source_radius_m=0.10,
        payload_center_m=0.30,
        payload_radius_m=0.10,
        target_acceleration_m_s2=9.80665,
    )["exterior_scalar_energy_j"]
    high = counterfactual_spherical_exterior_energy_j(
        scale_ev=1.0e6,
        source_radius_m=0.10,
        payload_center_m=0.30,
        payload_radius_m=0.10,
        target_acceleration_m_s2=9.80665,
    )["exterior_scalar_energy_j"]
    assert math.isclose(high / low, 1.0e4, rel_tol=1e-12)


def test_counterfactual_ten_mj_scale_is_about_three_hundred_kev():
    scale = scale_ev_for_counterfactual_energy(
        target_energy_j=1.0e7,
        source_radius_m=0.10,
        payload_center_m=0.30,
        payload_radius_m=0.10,
        target_acceleration_m_s2=9.80665,
    )
    assert 3.0e5 < scale < 4.0e5


def test_counterfactual_profile_rejects_source_payload_intersection():
    with pytest.raises(ValueError):
        counterfactual_spherical_exterior_energy_j(
            scale_ev=1.0e6,
            source_radius_m=0.10,
            payload_center_m=0.15,
            payload_radius_m=0.10,
            target_acceleration_m_s2=9.80665,
        )
