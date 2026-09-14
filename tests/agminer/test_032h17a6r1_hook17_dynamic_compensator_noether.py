"""Regressions for 032H17A6R1 dynamical-compensator Noether theorem."""

import math

import numpy as np

from antigravity_research.agminer.hook17_dynamic_compensator_noether import (
    HOOK17_REFERENCE_CAPACITY_RP1E12_J,
    a6_provenance_gate,
    first_divergence_twoform_current,
    h17a6r1_summary,
    massless_twoform_compensator_theorem,
    noether_completion_escape_atlas,
    pure_stueckelberg_noether_theorem,
    twoform_antisymmetry_gate,
    twoform_source_conservation_residual,
    ward_from_twoform_current,
    ward_twoform_identity_gate,
)

from antigravity_research.agminer.hook17_protected_k3_ward import (
    k3_ward_residual,
)


def test_a6_provenance_is_exactly_the_required_starting_state():
    result = a6_provenance_gate()

    assert (
        result[
            "a6_provenance_pass"
        ]
        is True
    )

    assert (
        result[
            "direct_j11_closed"
        ]
        is True
    )

    assert (
        result[
            "general_compensated_current_open"
        ]
        is True
    )

    assert (
        result[
            "productive_1plus_survives"
        ]
        is True
    )


def test_first_divergence_is_an_exact_antisymmetric_twoform():
    q = np.array(
        [
            1.0,
            0.0,
            0.0,
            1.0,
        ]
    )

    source = first_divergence_twoform_current(
        q
    )

    gate = twoform_antisymmetry_gate(
        q
    )

    assert source.shape == (
        4,
        4,
    )

    assert np.allclose(
        source
        +
        source.T,
        0.0,
        atol=
            1.0e-12,
        rtol=
            0.0,
    )

    assert (
        gate[
            "antisymmetric_twoform_current"
        ]
        is True
    )


def test_ward_operator_reconstructs_through_first_divergence():
    q = np.array(
        [
            1.0,
            0.0,
            0.0,
            1.0,
        ]
    )

    reconstructed = ward_from_twoform_current(
        q
    )

    direct = k3_ward_residual(
        q
    )

    assert np.allclose(
        reconstructed,
        direct,
        atol=
            1.0e-12,
        rtol=
            0.0,
    )

    assert np.allclose(
        direct,
        [
            0.0,
            0.0,
            -16.0,
            0.0,
        ],
        atol=
            1.0e-12,
        rtol=
            0.0,
    )


def test_twoform_source_conservation_is_exactly_minus_ward():
    q = np.array(
        [
            1.0,
            0.0,
            0.0,
            1.0,
        ]
    )

    conservation = twoform_source_conservation_residual(
        q
    )

    ward = k3_ward_residual(
        q
    )

    assert np.allclose(
        conservation,
        -ward,
        atol=
            1.0e-12,
        rtol=
            0.0,
    )


def test_lightlike_v24_source_fails_massless_twoform_noether_condition():
    q = np.array(
        [
            1.0,
            0.0,
            0.0,
            1.0,
        ]
    )

    result = ward_twoform_identity_gate(
        q
    )

    assert (
        result[
            "ward_reconstruction_pass"
        ]
        is True
    )

    assert (
        result[
            "twoform_conservation_equals_minus_ward"
        ]
        is True
    )

    assert math.isclose(
        result[
            "ward_direct_norm"
        ],
        16.0,
    )

    assert (
        result[
            "massless_twoform_source_compatible"
        ]
        is False
    )


def test_pure_exact_stueckelberg_still_imposes_original_ward_eom():
    result = pure_stueckelberg_noether_theorem()

    assert (
        result[
            "protected_massless_kinetic_gauge_invariant"
        ]
        is True
    )

    assert (
        result[
            "kinetic_compensator_dependence"
        ]
        ==
        "DROPS_OUT_BY_EXACT_GAUGE_INVARIANCE"
    )

    assert (
        result[
            "compensator_eom"
        ]
        ==
        "W^alpha[J]=0"
    )

    assert (
        result[
            "pure_exact_massless_stueckelberg_can_repair"
        ]
        is False
    )

    assert (
        result[
            "pure_exact_massless_stueckelberg_closed"
        ]
        is True
    )


def test_healthy_massless_twoform_compensator_class_is_scoped_red():
    result = massless_twoform_compensator_theorem()

    assert (
        result[
            "all_noether_identity_reconstructions_pass"
        ]
        is True
    )

    assert (
        result[
            "nonzero_incompatible_witness_count"
        ]
        >=
        1
    )

    assert (
        result[
            "massless_twoform_compensator_can_absorb_v24"
        ]
        is False
    )

    assert (
        result[
            "massless_twoform_compensator_closed"
        ]
        is True
    )


def test_higgsed_and_full_noether_completions_remain_distinct_and_open():
    rows = {
        row[
            "family"
        ]:
        row
        for row in noether_completion_escape_atlas()
    }

    assert (
        rows[
            "FULL_NOETHER_COMPLETE_MATTER_PLUS_COMPENSATOR"
        ][
            "status"
        ]
        ==
        "OPEN"
    )

    assert (
        rows[
            "HIGGSED_OR_MASSIVE_HOOK_COMPLETION"
        ][
            "status"
        ]
        ==
        "OPEN"
    )

    assert (
        rows[
            "MARZO_PROTECTED_ABELIAN_MAG_STUECKELBERG"
        ][
            "status"
        ]
        ==
        "OPEN_INDEPENDENT_FAMILY"
    )


def test_a6r1_does_not_close_hook17_or_productive_oneplus():
    result = h17a6r1_summary()

    assert (
        result[
            "declared_exact_massless_single_compensator_class_closed"
        ]
        is True
    )

    assert (
        result[
            "productive_1plus_representation_survives"
        ]
        is True
    )

    assert (
        result[
            "full_noether_complete_matter_compensator_closed"
        ]
        is False
    )

    assert (
        result[
            "higgsed_or_massive_hook_closed"
        ]
        is False
    )

    assert (
        result[
            "hook17_closed"
        ]
        is False
    )


def test_a6r1_preserves_capacity_and_forbids_premature_energy_or_h17b():
    result = h17a6r1_summary()

    assert math.isclose(
        result[
            "hook17_reference_capacity_rp1e12_j"
        ],
        HOOK17_REFERENCE_CAPACITY_RP1E12_J,
    )

    assert (
        result[
            "hook17_complete_energy_j"
        ]
        is None
    )

    assert (
        result[
            "energy_optimization_authorized"
        ]
        is False
    )

    assert (
        result[
            "sub100j_capacity_tuning_authorized"
        ]
        is False
    )

    assert (
        result[
            "h17b_authorized"
        ]
        is False
    )

    assert (
        result[
            "physical_antigravity_model_found"
        ]
        is False
    )

    assert result[
        "next"
    ].startswith(
        "032H17A6R2_HIGGSED_HOOK_"
    )
