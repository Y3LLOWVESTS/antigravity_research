"""Scientific regressions for 032H17A6 J11 / compensator Ward prefilter."""

import math

import numpy as np

from antigravity_research.agminer.hook17_j11_compensated_ward import (
    HOOK17_REFERENCE_CAPACITY_RP1E12_J,
    common_generator_invariance_gate,
    direct_j11_v24_gate,
    evaluate_ward_coefficients,
    h17a6_summary,
    j11_catalogue_gate,
    minimal_vector_improvement_gate,
    pure_stueckelberg_gate,
    ward_coefficient_tensor,
)

from antigravity_research.agminer.hook17_protected_k3_ward import (
    k3_ward_residual,
    v24_bms_current,
)


def test_j11_catalogue_relations_are_encoded_exactly():
    result = (
        j11_catalogue_gate()
    )

    relations = (
        result[
            "j11_relations"
        ]
    )

    assert relations[
        "kappa15_4"
    ] == "0"

    assert relations[
        "kappa16_4"
    ] == "0"

    assert relations[
        "kappa2_4"
    ] == "0"

    assert relations[
        "kappa4_4"
    ] == "-2*kappa3_4"

    assert relations[
        "kappa6_4"
    ] == "-kappa3_4"

    assert relations[
        "kappa7_4"
    ] == "0"

    assert relations[
        "kappa9_4"
    ] == "-0.5*kappa3_4"

    assert relations[
        "kappa1_2"
    ] == "0"

    assert relations[
        "kappa2_2"
    ] == "0"

    assert relations[
        "kappa3_2"
    ] == "0"


def test_k3_is_the_j11_kappa1_zero_specialization():
    result = (
        j11_catalogue_gate()
    )

    assert (
        result[
            "k3_is_j11_kappa1_zero_specialization"
        ]
        is True
    )

    assert (
        result[
            "k3_additional_constraint"
        ]
        ==
        "kappa1_4=0"
    )


def test_common_a5_generator_leaves_extra_j11_operator_invariant():
    result = (
        common_generator_invariance_gate()
    )

    assert (
        result[
            "common_generator_survives_j11_kappa1_operator"
        ]
        is True
    )

    assert (
        result[
            "max_numeric_identity_residual"
        ]
        <=
        1.0e-12
    )


def test_gate_does_not_claim_complete_j11_gauge_reconstruction():
    result = (
        common_generator_invariance_gate()
    )

    assert (
        result[
            "this_is_complete_j11_gauge_reconstruction"
        ]
        is False
    )

    assert (
        result[
            "this_is_one_exact_shared_necessary_generator"
        ]
        is True
    )


def test_v24_ward_polynomial_reconstructs_direct_a5_residual():
    coeff = (
        ward_coefficient_tensor(
            v24_bms_current()
        )
    )

    q = np.array(
        [
            1.0,
            0.0,
            0.0,
            1.0,
        ]
    )

    reconstructed = (
        evaluate_ward_coefficients(
            coeff,
            q,
        )
    )

    direct = (
        k3_ward_residual(
            q
        )
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
        reconstructed,
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


def test_direct_clean_v24_fails_surviving_j11_ward():
    result = (
        direct_j11_v24_gate()
    )

    assert (
        result[
            "common_generator_survives_j11"
        ]
        is True
    )

    assert (
        result[
            "direct_clean_v24_j11_ward_compatible"
        ]
        is False
    )

    assert (
        result[
            "direct_clean_v24_j11_closed"
        ]
        is True
    )

    assert math.isclose(
        result[
            "lightlike_z_residual_norm"
        ],
        16.0,
    )


def test_productive_1plus_representation_is_not_closed_by_j11_failure():
    result = (
        direct_j11_v24_gate()
    )

    assert (
        result[
            "productive_1plus_representation_overlap_survives"
        ]
        is True
    )

    assert math.isclose(
        result[
            "productive_1plus_seed_norm2"
        ],
        128.0,
    )

    assert (
        result[
            "all_protected_1plus_closed"
        ]
        is False
    )


def test_trace_vector_improvement_does_not_hit_v24_ward_polynomial():
    result = (
        minimal_vector_improvement_gate()
    )

    assert (
        result[
            "trace_vector_ward_map_rank"
        ]
        ==
        4
    )

    assert (
        result[
            "trace_vector_exact_repair_exists"
        ]
        is False
    )

    assert (
        result[
            "trace_vector_best_residual_norm"
        ]
        >
        1.0
    )


def test_axial_vector_improvement_is_exactly_ward_silent():
    result = (
        minimal_vector_improvement_gate()
    )

    assert (
        result[
            "axial_vector_is_ward_silent"
        ]
        is True
    )

    assert (
        result[
            "axial_vector_ward_map_norm"
        ]
        <=
        1.0e-12
    )


def test_combined_vector_axial_fixed_tensor_improvement_cannot_repair():
    result = (
        minimal_vector_improvement_gate()
    )

    assert (
        result[
            "combined_exact_repair_exists"
        ]
        is False
    )

    assert (
        result[
            "minimal_vector_axial_fixed_tensor_repair_closed"
        ]
        is True
    )

    assert (
        result[
            "combined_best_residual_norm"
        ]
        >
        1.0
    )


def test_pure_stueckelberg_gauge_image_is_silent_on_lightlike_pole():
    result = (
        pure_stueckelberg_gate()
    )

    assert abs(
        result[
            "q2"
        ]
    ) <= 1.0e-12

    assert math.isclose(
        result[
            "v24_residual_norm"
        ],
        16.0,
    )

    assert (
        result[
            "pure_gauge_image_is_ward_silent_on_massless_pole"
        ]
        is True
    )

    assert (
        result[
            "pure_stueckelberg_gauge_image_can_cancel_v24_pole_residual"
        ]
        is False
    )


def test_dynamical_compensator_and_source_engineering_remain_open():
    minimal = (
        minimal_vector_improvement_gate()
    )

    stueckelberg = (
        pure_stueckelberg_gate()
    )

    summary = (
        h17a6_summary()
    )

    assert (
        minimal[
            "dynamical_hook_compensator_closed"
        ]
        is False
    )

    assert (
        minimal[
            "momentum_dependent_spinor_texture_closed"
        ]
        is False
    )

    assert (
        stueckelberg[
            "dynamical_compensator_with_independent_equations_closed"
        ]
        is False
    )

    assert (
        summary[
            "general_local_same_action_compensated_current_closed"
        ]
        is False
    )


def test_h17a6_preserves_capacity_and_does_not_authorize_energy_or_h17b():
    result = (
        h17a6_summary()
    )

    assert (
        result[
            "decision"
        ].startswith(
            "RED_SCOPED_H17A6_"
        )
    )

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
            "sub100j_efficiency_tuning_authorized"
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

    assert (
        result[
            "certified_sub10mj_model_found"
        ]
        is False
    )

    assert result[
        "next"
    ].startswith(
        "032H17A6R1_DYNAMICAL_SAME_ACTION_"
    )
