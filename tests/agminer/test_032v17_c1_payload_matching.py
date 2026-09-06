import math

from antigravity_research.agminer.c1_payload_matching import (
    axial_leading_log_wavefunction_proxy,
    c1_from_metric_scale_ev,
    corrected_laue_trace_support_floor_j,
    jiang_nda_scale_from_c1_ev,
    payload_surface_acceleration_metrics,
    payload_transmission_factor,
    payload_volume_average_acceleration_m_s2,
    required_q2_for_payload_surface,
    source_feedback_metrics,
    spheroid_incident_legendre_coefficients,
    static_outward_metric_sign_from_c1,
)


G = 9.80665
Q = 9.117449122814854e-8
A_M = 0.25740088555864965
C_M = 0.09659120999271102
PAYLOAD_CENTER_Z_M = 0.20
PAYLOAD_RADIUS_M = 0.10
DEMAG_Z = 0.6050030448888295


def coefficients():
    return spheroid_incident_legendre_coefficients(
        a_m=A_M,
        c_m=C_M,
        payload_center_z_m=PAYLOAD_CENTER_Z_M,
        fit_radius_m=PAYLOAD_RADIUS_M,
        lmax=20,
        n_t=40,
        n_phi=60,
        fit_order=120,
    )


def test_c1_mapping_at_one_hundred_kev():
    c1 = c1_from_metric_scale_ev(1.0e5)
    assert math.isclose(c1, 5.0e-21, rel_tol=1.0e-15)
    assert static_outward_metric_sign_from_c1(c1) is True


def test_jiang_nda_mapping_factor():
    c1 = c1_from_metric_scale_ev(1.0e5)
    nda = jiang_nda_scale_from_c1_ev(c1)
    assert math.isclose(
        nda / 1.0e5,
        (32.0 * math.pi**2) ** 0.25,
        rel_tol=1.0e-15,
    )


def test_direct_c1_context_does_not_kill_24kev_point():
    c1 = c1_from_metric_scale_ev(2.42e4)
    assert c1 < 1.0e-10


def test_corrected_scalar_trace_support_floor():
    support = corrected_laue_trace_support_floor_j(
        fermion_mean_pressure_inventory_j=999734.7721903663,
        scalar_field_energy_j=140563.16724446957,
    )
    assert math.isclose(
        support,
        952880.3831088764,
        rel_tol=1.0e-14,
    )


def test_selected_loop030_leading_log_proxy_is_order_one_or_larger():
    proxy = axial_leading_log_wavefunction_proxy(
        loop_proxy=0.300000060963704,
        cutoff_ev=341.110242940734,
        mass_ev=24.96671585947364,
    )
    assert math.isclose(
        proxy,
        3.137595212707212,
        rel_tol=2.0e-14,
    )
    assert proxy > 1.0


def test_l1_transmission_matches_uniform_sphere_formula():
    epsilon = 0.25
    assert math.isclose(
        payload_transmission_factor(1, epsilon),
        3.0 / (3.0 + epsilon),
        rel_tol=1.0e-15,
    )


def test_vacuum_multipole_reconstructs_v15_q():
    result = required_q2_for_payload_surface(
        coefficients=coefficients(),
        epsilon_trace_load=0.0,
        payload_radius_m=PAYLOAD_RADIUS_M,
        target_acceleration_m_s2=G,
        surface_count=801,
    )
    assert math.isclose(
        math.sqrt(result["q2"]),
        Q,
        rel_tol=3.0e-8,
    )


def test_epsilon_three_requires_about_four_times_q_squared():
    result = required_q2_for_payload_surface(
        coefficients=coefficients(),
        epsilon_trace_load=3.0,
        payload_radius_m=PAYLOAD_RADIUS_M,
        target_acceleration_m_s2=G,
        surface_count=801,
    )
    factor = result["q2"] / Q**2
    assert 3.95 < factor < 4.01


def test_epsilon_three_finite_payload_has_minimum_one_g():
    coeff = coefficients()
    result = required_q2_for_payload_surface(
        coefficients=coeff,
        epsilon_trace_load=3.0,
        payload_radius_m=PAYLOAD_RADIUS_M,
        target_acceleration_m_s2=G,
        surface_count=801,
    )
    metrics = payload_surface_acceleration_metrics(
        coefficients=coeff,
        epsilon_trace_load=3.0,
        payload_radius_m=PAYLOAD_RADIUS_M,
        q2=result["q2"],
        surface_count=801,
    )
    assert math.isclose(
        metrics["surface_min_m_s2"],
        G,
        rel_tol=2.0e-12,
    )
    assert metrics["surface_max_m_s2"] > G


def test_epsilon_three_volume_average_is_outward_above_one_g():
    coeff = coefficients()
    result = required_q2_for_payload_surface(
        coefficients=coeff,
        epsilon_trace_load=3.0,
        payload_radius_m=PAYLOAD_RADIUS_M,
        target_acceleration_m_s2=G,
        surface_count=801,
    )
    average = payload_volume_average_acceleration_m_s2(
        coefficients=coeff,
        epsilon_trace_load=3.0,
        payload_radius_m=PAYLOAD_RADIUS_M,
        q2=result["q2"],
        order=16,
    )
    assert average > G


def test_payload_reaction_on_source_is_small_but_nonzero_at_epsilon_three():
    feedback = source_feedback_metrics(
        coefficients=coefficients(),
        epsilon_trace_load=3.0,
        payload_radius_m=PAYLOAD_RADIUS_M,
        payload_center_z_m=PAYLOAD_CENTER_Z_M,
        source_a_m=A_M,
        source_c_m=C_M,
        source_demag_z=DEMAG_Z,
        surface_count=201,
    )
    assert 0.0 < feedback["source_center_feedback_ratio"] < 0.01
    assert 0.0 < feedback["source_surface_max_feedback_ratio"] < 0.03
