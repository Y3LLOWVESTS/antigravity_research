import math

from antigravity_research.agminer.operator_atlas import (
    OperatorRecord,
    canonical_derivative_metric_coefficient,
    kinetic_conformal_outward_for_localized_gradient,
    operator_prefield_open,
    static_kinetic_conformal_acceleration,
    static_pure_disformal_g00_shift,
)


def test_032v12_canonical_metric_coefficient_is_field_rescaling_invariant():
    kappa = 3.0
    z = 2.0
    scale = 7.0

    original = canonical_derivative_metric_coefficient(kappa, z)

    kappa_prime = kappa/(scale*scale)
    z_prime = z/(scale*scale)

    transformed = canonical_derivative_metric_coefficient(
        kappa_prime,
        z_prime,
    )

    assert math.isclose(original, transformed, rel_tol=1e-15)


def test_032v12_static_pure_disformal_has_zero_g00_response():
    assert static_pure_disformal_g00_shift(0.0, 1.0e8) == 0.0


def test_032v12_dynamic_disformal_can_change_g00():
    assert static_pure_disformal_g00_shift(2.0, 3.0) == 12.0


def test_032v12_kinetic_conformal_can_be_outward_for_decaying_gradient():
    accel = static_kinetic_conformal_acceleration(
        +1.0,
        -1.0e-16,
    )
    assert accel > 0.0
    assert kinetic_conformal_outward_for_localized_gradient(+1.0) is True


def test_032v12_wrong_conformal_slope_is_inward():
    accel = static_kinetic_conformal_acceleration(
        -1.0,
        -1.0e-16,
    )
    assert accel < 0.0


def test_032v12_prefield_gate_promotes_only_complete_structure():
    record = OperatorRecord(
        operator_id="KINETIC_CONFORMAL",
        local_covariant=True,
        one_physical_metric=True,
        static_g00_response=True,
        external_standoff_structurally_possible=True,
        symmetry_protection_available=True,
        separate_propagating_charge_mediator_required=False,
        project_closed=False,
    )
    assert operator_prefield_open(record) is True


def test_032v12_prefield_gate_rejects_closed_or_separate_mediator():
    record = OperatorRecord(
        operator_id="BAD",
        local_covariant=True,
        one_physical_metric=True,
        static_g00_response=True,
        external_standoff_structurally_possible=True,
        symmetry_protection_available=True,
        separate_propagating_charge_mediator_required=True,
        project_closed=False,
    )
    assert operator_prefield_open(record) is False
