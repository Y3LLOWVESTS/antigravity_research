"""Scientific regressions for 032H17A5 protected K3 source-Ward gate."""

import math

import numpy as np

from antigravity_research.agminer.hook17_protected_k3_ward import (
    bms_helicity_prefilter,
    h17a5_summary,
    k3_published_model_gate,
    k3_ward_counterexample_gate,
    localized_scalar_envelope_theorem,
    protected_rescue_rerank,
    source_component_gate,
    vector_graviton_identification_gate,
)


def test_mapped_v24_current_has_bms_last_pair_antisymmetry():
    result = (
        source_component_gate()
    )

    assert (
        result[
            "last_pair_antisymmetric"
        ]
        is True
    )


def test_mapped_v24_current_sparse_identity_is_exact():
    result = (
        source_component_gate()
    )

    assert (
        result[
            "nonzero_component_count"
        ]
        ==
        4
    )

    assert (
        result[
            "expected_sparse_identity_pass"
        ]
        is True
    )

    assert math.isclose(
        result[
            "component_norm"
        ],
        16.0,
    )


def test_bms_spin2_helicity_seed_is_zero():
    result = (
        bms_helicity_prefilter()
    )

    assert (
        result[
            "spin2_helicity_seed_zero"
        ]
        is True
    )


def test_bms_zero_helicity_seed_is_zero():
    result = (
        bms_helicity_prefilter()
    )

    assert (
        result[
            "zero_helicity_seed_zero"
        ]
        is True
    )


def test_bms_spin1_helicity_seed_is_nonzero():
    result = (
        bms_helicity_prefilter()
    )

    assert (
        result[
            "spin1_helicity_seed_nonzero"
        ]
        is True
    )

    assert math.isclose(
        result[
            "spin1_helicity_seed_norm2"
        ],
        128.0,
    )


def test_k3_is_published_protected_minimal_axial_vector_model():
    result = (
        k3_published_model_gate()
    )

    assert (
        result[
            "gauge_symmetric"
        ]
        is True
    )

    assert (
        result[
            "ghost_tachyon_free"
        ]
        is True
    )

    assert (
        result[
            "propagating_sector"
        ]
        ==
        "AXIAL_VECTOR_EVEN_PARITY_1PLUS"
    )

    assert (
        result[
            "physical_polarizations"
        ]
        ==
        2
    )


def test_k3_has_twenty_one_published_source_constraints():
    result = (
        k3_published_model_gate()
    )

    assert (
        result[
            "published_source_constraint_count"
        ]
        ==
        21
    )

    assert (
        result[
            "source_constraints_are_ward_conditions"
        ]
        is True
    )


def test_lightlike_z_witness_is_on_massless_pole():
    result = (
        k3_ward_counterexample_gate()
    )[
        "rows"
    ][
        "LIGHTLIKE_Z"
    ]

    assert (
        abs(
            result[
                "q2"
            ]
        )
        <
        1.0e-12
    )


def test_lightlike_z_witness_has_exact_nonzero_ward_residual():
    result = (
        k3_ward_counterexample_gate()
    )[
        "rows"
    ][
        "LIGHTLIKE_Z"
    ]

    assert np.allclose(
        result[
            "residual"
        ],
        [
            0.0,
            0.0,
            -16.0,
            0.0,
        ],
    )

    assert math.isclose(
        result[
            "residual_norm"
        ],
        16.0,
    )

    assert (
        result[
            "passes_necessary_ward"
        ]
        is False
    )


def test_lightlike_y_witness_also_fails():
    result = (
        k3_ward_counterexample_gate()
    )[
        "rows"
    ][
        "LIGHTLIKE_Y"
    ]

    assert math.isclose(
        result[
            "residual_norm"
        ],
        8.0,
    )

    assert (
        result[
            "passes_necessary_ward"
        ]
        is False
    )


def test_lightlike_x_is_an_accidental_zero_direction():
    result = (
        k3_ward_counterexample_gate()
    )[
        "rows"
    ][
        "LIGHTLIKE_X"
    ]

    assert (
        result[
            "passes_necessary_ward"
        ]
        is True
    )


def test_generic_static_diagonal_fourier_mode_fails():
    result = (
        k3_ward_counterexample_gate()
    )[
        "rows"
    ][
        "STATIC_DIAGONAL"
    ]

    assert math.isclose(
        result[
            "residual_norm"
        ],
        8.0,
    )

    assert (
        result[
            "passes_necessary_ward"
        ]
        is False
    )


def test_one_exact_counterexample_closes_direct_k3_source_coupling():
    result = (
        k3_ward_counterexample_gate()
    )

    assert (
        result[
            "at_least_one_ward_counterexample"
        ]
        is True
    )

    assert (
        result[
            "direct_v24_k3_source_ward_compatible"
        ]
        is False
    )

    assert (
        result[
            "one_counterexample_is_sufficient_to_reject_direct_coupling"
        ]
        is True
    )


def test_fixed_tensor_scalar_envelope_cannot_repair_k3_ward_identity():
    result = (
        localized_scalar_envelope_theorem()
    )

    assert (
        result[
            "ward_polynomial_identically_zero"
        ]
        is False
    )

    assert (
        result[
            "compact_scalar_envelope_direct_k3_compatible"
        ]
        is False
    )


def test_source_engineering_and_compensator_rescues_remain_open():
    result = (
        localized_scalar_envelope_theorem()
    )

    assert (
        result[
            "q_dependent_spinor_texture_closed"
        ]
        is False
    )

    assert (
        result[
            "improved_or_compensated_current_closed"
        ]
        is False
    )

    assert (
        result[
            "other_protected_axial_vector_actions_closed"
        ]
        is False
    )


def test_k3_is_not_silently_identified_with_other_vector_actions():
    result = (
        vector_graviton_identification_gate()
    )

    assert (
        result[
            "direct_vector_graviton_identification_pass"
        ]
        is False
    )

    assert (
        result[
            "gauge_invariant_hook17_metric_in_k3_same_action"
        ]
        is False
    )


def test_rerank_moves_to_j11_and_compensated_current():
    rows = (
        protected_rescue_rerank()
    )

    assert (
        rows[
            0
        ][
            "family"
        ]
        ==
        "BMS_J11_LESS_CONSTRAINING_AXIAL_VECTOR"
    )

    assert any(
        "COMPENSATED"
        in
        row[
            "family"
        ]
        for row in rows
    )


def test_h17a5_is_scoped_red_and_requires_journal_without_overclosure():
    result = (
        h17a5_summary()
    )

    assert (
        result[
            "decision"
        ].startswith(
            "RED_SCOPED_H17A5_"
        )
    )

    assert (
        result[
            "k3_direct_v24_source_closed"
        ]
        is True
    )

    assert (
        result[
            "hook17_all_protected_1plus_closed"
        ]
        is False
    )

    assert (
        result[
            "journal_now"
        ]
        is True
    )

    assert (
        result[
            "h17b_authorized"
        ]
        is False
    )

    assert (
        result[
            "energy_optimization_authorized"
        ]
        is False
    )

    assert (
        result[
            "sub100j_efficiency_tuning_authorized"
        ]
        is False
    )

    assert (
        result[
            "hook17_complete_energy_j"
        ]
        is None
    )
