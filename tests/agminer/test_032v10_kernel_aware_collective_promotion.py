import math

from antigravity_research.agminer.kernel_scaling import (
    assess_collective_promotion,
    maximum_combined_tax,
    minimum_retention_fraction,
    net_efficiency_exponent,
    required_kernel_exponent,
    source_gain,
)


G10 = 532.4046687159987
G1 = 5324.046687159987


def test_032v10_q1e12_hopf_headroom_for_10mj():
    gain = source_gain(1.0e12, 0.25)
    assert math.isclose(gain, 1000.0, rel_tol=1e-12)
    assert math.isclose(
        maximum_combined_tax(gain, G10),
        1.8782705313454555,
        rel_tol=1e-12,
    )
    assert math.isclose(
        minimum_retention_fraction(gain, G10),
        0.5324046687159987,
        rel_tol=1e-12,
    )


def test_032v10_q1e12_kernel_exponent_floor():
    k = required_kernel_exponent(0.25, G10, 1.0e12)
    assert -0.02282 < k < -0.02280


def test_032v10_q1e15_one_mj_needs_nearly_perfect_retention():
    gain = source_gain(1.0e15, 0.25)
    retention = minimum_retention_fraction(gain, G1)
    assert 0.946 < retention < 0.947


def test_032v10_fixed_productive_segment_diagnostic_is_bad():
    net = net_efficiency_exponent(
        0.25,
        -0.75,
    )
    assert math.isclose(net, -0.5)


def test_032v10_hopf_global_scaling_is_not_promotable():
    a = assess_collective_promotion(
        local_covariant_charge=False,
        physical_vacuum_portal=False,
        finite_payload_response_derived=False,
        complete_portal_energy_scaling_derived=False,
        normalization_invariant=True,
        naturalness_screened=False,
    )
    assert a.promotable is False
    assert "NO_LOCAL_COVARIANT_CHARGE" in a.reasons


def test_032v10_complete_physical_scaling_can_be_promoted():
    a = assess_collective_promotion(
        local_covariant_charge=True,
        physical_vacuum_portal=True,
        finite_payload_response_derived=True,
        complete_portal_energy_scaling_derived=True,
        normalization_invariant=True,
        naturalness_screened=True,
    )
    assert a.promotable is True
    assert a.reasons == ()
