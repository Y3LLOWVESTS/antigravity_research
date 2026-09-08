"""Scientific regressions for 032H17A4 symmetry-first protected rescue."""

import math

from antigravity_research.agminer.hook17_protected_torsionlike_atlas import (
    h17a2_oneplus_spatial_dual_vector_gate,
    h17a4_summary,
    mapped_v24_torsionlike_source_gate,
    protected_family_atlas,
    stueckelberg_vector_metric_gate,
    torsionlike_catalogue_theorem_gate,
)


def test_v24_hook_maps_to_nonzero_pair_antisymmetric_source():
    result = (
        mapped_v24_torsionlike_source_gate()
    )

    assert result[
        "hook_source_nonzero"
    ] is True

    assert result[
        "torsionlike_source_nonzero"
    ] is True

    assert result[
        "first_pair_antisymmetric"
    ] is True


def test_hook_torsionlike_roundtrip_is_exact_on_clean_source():
    result = (
        mapped_v24_torsionlike_source_gate()
    )

    assert result[
        "map_invertible_on_declared_hook_source"
    ] is True

    assert result[
        "hook_roundtrip_relative_error"
    ] < 1.0e-12


def test_hook_torsionlike_map_is_parity_even_algebraic_map():
    result = (
        mapped_v24_torsionlike_source_gate()
    )

    assert result[
        "map_uses_levi_civita"
    ] is False

    assert result[
        "map_parity_even"
    ] is True


def test_clean_mapped_source_obeys_cyclic_identity():
    result = (
        mapped_v24_torsionlike_source_gate()
    )

    assert result[
        "cyclic_identity_zero"
    ] is True

    assert result[
        "cyclic_sum_norm"
    ] < 1.0e-12


def test_clean_mapped_source_has_zero_simple_lorentz_traces():
    result = (
        mapped_v24_torsionlike_source_gate()
    )

    assert result[
        "lorentz_trace_a_zero"
    ] is True

    assert result[
        "lorentz_trace_b_zero"
    ] is True


def test_clean_mapped_source_has_zero_axial_pseudotrace():
    result = (
        mapped_v24_torsionlike_source_gate()
    )

    assert result[
        "axial_pseudotrace_zero"
    ] is True

    assert result[
        "axial_pseudotrace_norm"
    ] < 1.0e-12


def test_trace_zero_does_not_close_all_vector_modes():
    result = (
        mapped_v24_torsionlike_source_gate()
    )

    assert result[
        "trace_zero_closes_all_vector_modes"
    ] is False


def test_h17a2_oneplus_source_has_nonzero_spatial_dual_vector():
    result = (
        h17a2_oneplus_spatial_dual_vector_gate()
    )

    assert result[
        "spatial_dual_vector_nonzero"
    ] is True

    assert math.isclose(
        result[
            "spatial_dual_vector_norm2"
        ],
        64.0,
    )


def test_oneplus_dual_identity_matches_antisymmetric_matrix_norm():
    result = (
        h17a2_oneplus_spatial_dual_vector_gate()
    )

    assert result[
        "dual_norm_identity_pass"
    ] is True

    assert math.isclose(
        result[
            "oneplus_matrix_norm2"
        ],
        128.0,
    )


def test_spatial_dual_witness_is_not_mislabeled_same_action_projector():
    result = (
        h17a2_oneplus_spatial_dual_vector_gate()
    )

    assert result[
        "lorentz_covariant_action_projector_established"
    ] is False

    assert result[
        "same_action_vector_source_identification_established"
    ] is False


def test_torsionlike_catalogue_counts_and_unitary_vector_theorem():
    result = (
        torsionlike_catalogue_theorem_gate()
    )

    assert result[
        "general_quadratic_parameter_count"
    ] == 12

    assert result[
        "gauge_symmetric_specializations"
    ] == 206

    assert result[
        "ghost_tachyon_free_specializations"
    ] == 22

    assert result[
        "unitary_torsion_modes_vector_only"
    ] is True


def test_catalogue_does_not_directly_rescue_2plus_but_keeps_1plus_open():
    result = (
        torsionlike_catalogue_theorem_gate()
    )

    assert result[
        "catalogue_supplies_protected_spin2_carrier"
    ] is False

    assert result[
        "catalogue_rescues_h17_2plus_directly"
    ] is False

    assert result[
        "catalogue_keeps_h17_1plus_representation_target_open"
    ] is True


def test_catalogue_scope_does_not_close_all_protected_2plus_theories():
    result = (
        torsionlike_catalogue_theorem_gate()
    )

    assert result[
        "catalogue_closes_all_protected_hook_2plus_theories"
    ] is False

    assert (
        "NONLINEAR_BACKGROUND"
        in
        result[
            "scope_exclusions"
        ]
    )

    assert (
        "OTHER_MAG_REPRESENTATIONS"
        in
        result[
            "scope_exclusions"
        ]
    )


def test_stueckelberg_invariant_vector_and_metric_are_gauge_invariant():
    result = (
        stueckelberg_vector_metric_gate()
    )

    assert result[
        "gauge_invariant_vector_pass"
    ] is True

    assert result[
        "metric_gauge_invariance_pass"
    ] is True


def test_stueckelberg_quadratic_metric_preserves_active_offstate_separation():
    result = (
        stueckelberg_vector_metric_gate()
    )

    assert result[
        "offstate_linear_silence"
    ] is True

    assert result[
        "active_linear_response_nonzero"
    ] is True

    assert result[
        "one_universal_symmetric_rank2_metric_witness"
    ] is True


def test_stueckelberg_metric_witness_is_not_mislabeled_v24_same_action_match():
    result = (
        stueckelberg_vector_metric_gate()
    )

    assert result[
        "exact_v24_source_matched_to_W"
    ] is False

    assert result[
        "same_action_dirac_source_ward_complete"
    ] is False

    assert result[
        "hook17_17j_capacity_preserved_under_vector_completion"
    ] is False


def test_protected_family_atlas_has_multiple_distinct_rescue_options():
    rows = (
        protected_family_atlas()
    )

    assert len(
        rows
    ) >= 5

    assert rows[
        0
    ][
        "family"
    ] == (
        "BMS2026_TORSIONLIKE_UNITARY_VECTOR_CATALOGUE"
    )

    assert any(
        row[
            "family"
        ]
        ==
        "MARZO2026_NONLINEAR_VECTOR_GRAVITON_NOETHER_COMPLETION"
        for row in rows
    )


def test_h17a4_is_yellow_and_keeps_physical_promotion_closed():
    result = (
        h17a4_summary()
    )

    assert result[
        "decision"
    ].startswith(
        "YELLOW_H17A4_"
    )

    assert result[
        "next"
    ].startswith(
        "032H17A5_EXACT_PROTECTED_TORSIONLIKE_1PLUS_"
    )

    assert result[
        "protected_exact_same_action_survivors"
    ] == 0

    assert result[
        "same_action_provenance_complete"
    ] is False

    assert result[
        "full_noether_completion"
    ] is False

    assert result[
        "h17b_authorized"
    ] is False

    assert result[
        "energy_optimization_authorized"
    ] is False

    assert result[
        "sub100j_efficiency_tuning_authorized"
    ] is False

    assert result[
        "physical_antigravity_model_found"
    ] is False

    assert result[
        "certified_sub10mj_model_found"
    ] is False

    assert result[
        "practical_device_found"
    ] is False
