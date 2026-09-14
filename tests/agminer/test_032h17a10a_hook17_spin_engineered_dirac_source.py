"""Regression tests for 032H17A10A spin-engineered Dirac source states.

These tests protect the exact rest-basis Wheeler-source theorem only.

They must not be interpreted as proof of a protected same-action carrier,
Ward-compatible localized source, physical metric, finite-payload response,
or complete energy.
"""

from __future__ import annotations

import math

import numpy as np

from antigravity_research.agminer.hook17_spin_engineered_dirac_source import (
    h17a10a_summary,
    rest_pair_state_atlas,
)


def _rows() -> dict[
    str,
    dict,
]:
    return {
        row[
            "pair_id"
        ]:
            row

        for row
        in rest_pair_state_atlas()
    }


def test_complete_two_by_two_rest_pair_basis_is_enumerated():
    rows = _rows()

    assert set(
        rows
    ) == {
        "U1_V1",
        "U1_V2",
        "U2_V1",
        "U2_V2",
    }


def test_historical_clean_pair_reproduces_zero_trace_vector_overlap():
    row = _rows()[
        "U1_V2"
    ]

    assert row[
        "historical_clean_pair"
    ] is True

    assert row[
        "full_wheeler_source_zero"
    ] is False

    assert row[
        "totally_symmetric_trace_nonzero"
    ] is False

    assert row[
        "direct_trace_carrier_overlap_nonzero"
    ] is False


def test_two_spin_engineered_rest_pairs_have_exact_opposite_trace_vectors():
    rows = _rows()

    expected_minus = np.array(
        [
            0.0,
            -8.0 / 3.0,
            0.0,
            0.0,
        ]
    )

    expected_plus = -expected_minus

    minus = np.asarray(
        rows[
            "U1_V1"
        ][
            "totally_symmetric_lorentz_trace_covector"
        ]
    )

    plus = np.asarray(
        rows[
            "U2_V2"
        ][
            "totally_symmetric_lorentz_trace_covector"
        ]
    )

    assert np.allclose(
        minus,
        expected_minus,
        atol=1.0e-12,
        rtol=0.0,
    )

    assert np.allclose(
        plus,
        expected_plus,
        atol=1.0e-12,
        rtol=0.0,
    )

    assert rows[
        "U1_V1"
    ][
        "totally_symmetric_trace_nonzero"
    ] is True

    assert rows[
        "U2_V2"
    ][
        "totally_symmetric_trace_nonzero"
    ] is True


def test_trace_carrier_identity_gives_exact_nonzero_engineered_overlap():
    rows = _rows()

    for pair_id in (
        "U1_V1",
        "U2_V2",
    ):
        row = rows[
            pair_id
        ]

        assert row[
            "trace_carrier_identity_all_pass"
        ] is True

        assert row[
            "direct_trace_carrier_overlap_nonzero"
        ] is True

        assert math.isclose(
            row[
                "maximum_direct_trace_carrier_overlap"
            ],
            8.0,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        )


def test_fourth_rest_pair_is_exact_null_source_in_tested_nonmetricity_formula():
    row = _rows()[
        "U2_V1"
    ]

    assert row[
        "full_wheeler_source_zero"
    ] is True

    assert math.isclose(
        row[
            "full_wheeler_source_component_norm"
        ],
        0.0,
        rel_tol=0.0,
        abs_tol=1.0e-14,
    )


def test_source_state_escape_does_not_reopen_weyl_dilation_trace():
    rows = _rows()

    for row in rows.values():
        assert row[
            "full_weyl_dilation_trace_zero"
        ] is True

        assert np.linalg.norm(
            np.asarray(
                row[
                    "full_weyl_dilation_trace"
                ]
            )
        ) < 1.0e-12


def test_engineered_states_have_nonzero_so3_spin1_screen_but_not_exact_pole_claim():
    rows = _rows()

    for pair_id in (
        "U1_V1",
        "U2_V2",
    ):
        row = rows[
            pair_id
        ]

        assert row[
            "so3_combined_spin1_screen_norm"
        ] > 1.0

        assert row[
            "rest_frame_so3_screen_is_exact_pole_projector"
        ] is False


def test_a10a_promotes_only_the_next_ward_projector_gate_not_energy():
    summary = h17a10a_summary()

    assert summary[
        "partial_green"
    ] is True

    assert summary[
        "historical_clean_pair_trace_zero_reproduced"
    ] is True

    assert summary[
        "spin_engineered_rest_pair_trace_escape_exists"
    ] is True

    assert summary[
        "spin_engineered_nonzero_pair_count"
    ] == 2

    assert summary[
        "engineered_trace_equal_and_opposite"
    ] is True

    assert summary[
        "all_full_weyl_dilation_traces_zero"
    ] is True

    assert summary[
        "microscopic_nonmetricity_source_provenance_preserved_under_state_change"
    ] is True

    assert summary[
        "exact_bms_tensor_gauge_source_ward_evaluated"
    ] is False

    assert summary[
        "exact_bms_physical_pole_projector_evaluated_for_engineered_state"
    ] is False

    assert summary[
        "engineered_pair_torsion_cancellation_established"
    ] is False

    assert summary[
        "canonical_source_charge_per_joule_established"
    ] is False

    assert summary[
        "energy_optimization_authorized"
    ] is False

    assert summary[
        "geometry_optimization_authorized"
    ] is False

    assert summary[
        "physical_antigravity_model_found"
    ] is False

    assert summary[
        "certified_sub10mj_model_found"
    ] is False

    assert summary[
        "hook17_closed"
    ] is False

    assert summary[
        "next"
    ] == (
        "032H17A10B_BMS_PROTECTED_SPIN1_EXACT_WARD_"
        "TORSION_AND_POLE_PROJECTOR_GATE"
    )
