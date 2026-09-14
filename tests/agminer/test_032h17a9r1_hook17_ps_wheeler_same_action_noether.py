"""Regression tests for 032H17A9R1."""

import math

import numpy as np

from antigravity_research.agminer.hook17_ps_wheeler_same_action_noether import (
    HOOK17_REFERENCE_CAPACITY_RP1E12_J,
    a9_provenance_gate,
    clean_a9_special_source_gate,
    clean_local_sigma_completion_gate,
    h17a9r1_summary,
    hermitian_spinor_probe_set,
    local_sigma_ward_witness_gate,
    projective_hermitian_probe_rows,
    ps_torsion_free_source_for_spinor,
    wheeler_projective_source_identity_gate,
)


def test_a9_provenance_is_green():
    result = a9_provenance_gate()

    assert result[
        "a9_provenance_pass"
    ] is True

    assert result[
        "exact_1plus_pole_overlap"
    ] is True

    assert math.isclose(
        result[
            "exact_1plus_pole_numerator"
        ],
        1.44,
    )


def test_hermitian_probe_basis_has_exactly_sixteen_real_directions():
    probes = hermitian_spinor_probe_set()

    assert len(
        probes
    ) == 16

    names = [
        row[
            "name"
        ]
        for row in probes
    ]

    assert len(
        set(
            names
        )
    ) == 16

    assert sum(
        row[
            "kind"
        ]
        ==
        "DIAGONAL"
        for row in probes
    ) == 4

    assert sum(
        row[
            "kind"
        ]
        ==
        "REAL_CROSS"
        for row in probes
    ) == 6

    assert sum(
        row[
            "kind"
        ]
        ==
        "IMAG_CROSS"
        for row in probes
    ) == 6


def test_analytic_projective_trace_formula_reconstructs_all_probes():
    result = wheeler_projective_source_identity_gate()

    assert result[
        "complete_hermitian_probe_basis"
    ] is True

    assert result[
        "analytic_trace_formula_reconstruction_pass"
    ] is True

    assert result[
        "maximum_analytic_reconstruction_error"
    ] <= 1.0e-12


def test_unmodified_wheeler_source_is_not_projective_identity():
    result = wheeler_projective_source_identity_gate()

    assert result[
        "hermitian_probe_count"
    ] == 16

    assert result[
        "projective_compatible_probe_count"
    ] == 3

    assert result[
        "projective_incompatible_probe_count"
    ] == 13

    assert result[
        "unmodified_wheeler_projective_source_identity"
    ] is False


def test_d1_is_exact_projective_counterexample():
    result = wheeler_projective_source_identity_gate()

    assert np.allclose(
        result[
            "d1_trace"
        ],
        [
            0.0,
            2.0,
            0.0,
            0.0,
        ],
        atol=1.0e-12,
        rtol=0.0,
    )

    assert math.isclose(
        result[
            "d1_trace_norm"
        ],
        2.0,
    )


def test_i01_is_maximum_declared_probe_residual():
    result = wheeler_projective_source_identity_gate()

    assert np.allclose(
        result[
            "i01_trace"
        ],
        [
            -0.5,
            2.0,
            0.0,
            0.5,
        ],
        atol=1.0e-12,
        rtol=0.0,
    )

    assert math.isclose(
        result[
            "i01_trace_norm"
        ],
        math.sqrt(
            4.5
        ),
    )

    assert math.isclose(
        result[
            "maximum_projective_trace_norm"
        ],
        math.sqrt(
            4.5
        ),
    )


def test_all_generic_probe_sources_are_torsion_free_projected():
    for probe in hermitian_spinor_probe_set():
        source = ps_torsion_free_source_for_spinor(
            probe[
                "spinor"
            ]
        )

        assert np.allclose(
            source,
            np.swapaxes(
                source,
                0,
                2,
            ),
            atol=1.0e-12,
            rtol=0.0,
        )


def test_clean_a9_special_source_and_exact_pole_are_preserved():
    result = clean_a9_special_source_gate()

    assert result[
        "clean_projective_trace_pass"
    ] is True

    assert result[
        "clean_exact_1plus_pole_overlap"
    ] is True

    assert result[
        "clean_exact_1plus_pole_numerator_nonzero"
    ] is True

    assert math.isclose(
        result[
            "clean_exact_1plus_pole_numerator"
        ],
        1.44,
    )

    assert result[
        "clean_source_alone_proves_matter_action_projective_invariance"
    ] is False


def test_local_symmetric_sigma_polynomial_system_has_unique_solution():
    result = clean_local_sigma_completion_gate()

    assert result[
        "equation_count"
    ] == 40

    assert result[
        "unknown_count"
    ] == 40

    assert result[
        "matrix_rank"
    ] == 40

    assert result[
        "unique_solution"
    ] is True

    assert result[
        "local_first_derivative_symmetric_sigma_completion_exists"
    ] is True

    assert result[
        "maximum_polynomial_residual"
    ] <= 1.0e-10


def test_local_sigma_solution_reconstructs_simple_clean_coefficient():
    result = clean_local_sigma_completion_gate()

    assert math.isclose(
        result[
            "s_032"
        ],
        4.0,
        abs_tol=1.0e-10,
    )

    assert math.isclose(
        result[
            "s_302"
        ],
        4.0,
        abs_tol=1.0e-10,
    )

    assert result[
        "maximum_other_s_coefficient"
    ] <= 1.0e-10

    assert result[
        "inverse_q_used"
    ] is False

    assert result[
        "inverse_q_squared_used"
    ] is False

    assert result[
        "nonlocal_repair_used"
    ] is False


def test_local_sigma_cancels_full_ward_polynomial_on_independent_witnesses():
    result = local_sigma_ward_witness_gate()

    assert result[
        "witness_count"
    ] == 4

    assert result[
        "all_witnesses_pass"
    ] is True

    assert result[
        "maximum_witness_residual_norm"
    ] <= 1.0e-10

    assert result[
        "sigma_is_local_first_derivative"
    ] is True

    assert result[
        "sigma_is_symmetric"
    ] is True

    assert result[
        "sigma_was_derived_from_wheeler_metric_variation"
    ] is False


def test_a9r1_scoped_red_closes_only_unmodified_matter_stitching():
    result = h17a9r1_summary()

    assert result[
        "decision"
    ].startswith(
        "RED_SCOPED_A9R1_"
    )

    assert result[
        "direct_unmodified_wheeler_ps_same_action_closed"
    ] is True

    assert result[
        "unmodified_wheeler_projective_source_identity"
    ] is False

    assert result[
        "clean_a9_projective_special_state_pass"
    ] is True

    assert result[
        "a9_exact_1plus_pole_overlap_preserved"
    ] is True

    assert result[
        "local_symmetric_sigma_completion_exists"
    ] is True

    assert result[
        "local_sigma_is_same_action_wheeler_metric_stress"
    ] is False

    assert result[
        "projectively_completed_wheeler_matter_action_closed"
    ] is False

    assert result[
        "same_action_hook17_complete"
    ] is False

    assert result[
        "hook17_closed"
    ] is False


def test_a9r1_preserves_energy_discipline_and_next_rescue():
    result = h17a9r1_summary()

    assert math.isclose(
        result[
            "hook17_reference_capacity_rp1e12_j"
        ],
        HOOK17_REFERENCE_CAPACITY_RP1E12_J,
    )

    assert result[
        "hook17_complete_energy_j"
    ] is None

    assert result[
        "energy_optimization_authorized"
    ] is False

    assert result[
        "capacity_recalculation_authorized"
    ] is False

    assert result[
        "h17b_authorized"
    ] is False

    assert result[
        "physical_antigravity_model_found"
    ] is False

    assert result[
        "certified_sub10mj_model_found"
    ] is False

    assert result[
        "next"
    ] == (
        "032H17A9R2_PROJECTIVELY_COMPLETED_DIRAC_MATTER_ACTION_GATE"
    )
