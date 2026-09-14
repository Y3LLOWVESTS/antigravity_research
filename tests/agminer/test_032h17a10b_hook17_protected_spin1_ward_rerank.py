"""Regressions for 032H17A10B.

These tests protect:

- the exact BMS tensor-gauge Ward closeout in the declared rest-density class;
- the distinction between scoped route closure and global-family closure;
- the reopened engineered totally-symmetric 1- representation support;
- the prohibition on promoting representation support to an exact pole;
- the prohibition on premature energy optimization.
"""

from __future__ import annotations

import math

from antigravity_research.agminer.hook17_spin_engineered_protected_vector_ward import (
    compact_localized_bms_rest_density_closeout,
    engineered_fixed_pair_bms_ward_gate,
    engineered_totally_symmetric_1minus_gate,
    exact_physical_momentum_representatives,
    generic_rest_density_bms_ward_theorem,
    h17a10b_summary,
    rest_density_basis_sources,
)


def test_rest_density_basis_is_complete_eight_real_directions():
    rows = (
        rest_density_basis_sources()
    )

    assert len(
        rows
    ) == 8

    assert [
        label
        for (
            label,
            _,
        )
        in rows
    ] == [
        "P0",
        "P1",
        "PR",
        "PI",
        "A2",
        "A3",
        "AR",
        "AI",
    ]


def test_both_a10a_engineered_fixed_pairs_fail_direct_bms_ward():
    result = (
        engineered_fixed_pair_bms_ward_gate()
    )

    assert (
        result[
            "both_engineered_pairs_fail_direct_bms_ward"
        ]
        is True
    )

    assert (
        result[
            "failure_is_numerical_roundoff"
        ]
        is False
    )

    assert (
        result[
            "minimum_engineered_ward_residual_norm"
        ]
        >
        1.0
    )


def test_generic_symbolic_bms_rest_density_nullspace_is_trace_silent():
    result = (
        generic_rest_density_bms_ward_theorem()
    )

    assert (
        result[
            "symbolic_exact_arithmetic"
        ]
        is True
    )

    assert (
        result[
            "generic_symbolic_ward_rank"
        ]
        ==
        6
    )

    assert (
        result[
            "generic_symbolic_ward_nullity"
        ]
        ==
        2
    )

    assert (
        result[
            "trace_vanishes_on_entire_generic_ward_nullspace"
        ]
        is True
    )

    assert (
        result[
            "generic_nonzero_trace_escape_exists"
        ]
        is False
    )


def test_massless_and_static_representatives_are_exactly_trace_silent():
    result = (
        exact_physical_momentum_representatives()
    )

    assert (
        result[
            "all_physical_representatives_trace_silent"
        ]
        is True
    )

    rows = {
        row[
            "momentum_id"
        ]:
            row
        for row
        in result[
            "rows"
        ]
    }

    assert (
        rows[
            "MASSLESS_NULL_Z"
        ][
            "ward_rank"
        ]
        ==
        6
    )

    assert (
        rows[
            "MASSLESS_NULL_Z"
        ][
            "ward_nullity"
        ]
        ==
        2
    )

    assert (
        rows[
            "STATIC_Z"
        ][
            "ward_rank"
        ]
        ==
        5
    )

    assert (
        rows[
            "STATIC_Z"
        ][
            "ward_nullity"
        ]
        ==
        3
    )


def test_compact_localized_direct_bms_rest_density_trace_route_closes():
    result = (
        compact_localized_bms_rest_density_closeout()
    )

    assert (
        result[
            "generic_open_set_trace_zero"
        ]
        is True
    )

    assert (
        result[
            "compact_support_fourier_amplitudes_analytic"
        ]
        is True
    )

    assert (
        result[
            "exceptional_momentum_strata_can_rescue_compact_trace_source"
        ]
        is False
    )

    assert (
        result[
            "direct_bms_trace_vector_rest_density_route_closed"
        ]
        is True
    )

    assert (
        result[
            "bms_family_globally_closed"
        ]
        is False
    )


def test_u1v1_reopens_totally_symmetric_1minus_representation_support():
    rows = {
        row[
            "pair_id"
        ]:
            row
        for row
        in (
            engineered_totally_symmetric_1minus_gate()[
                "rows"
            ]
        )
    }

    row = rows[
        "U1_V1"
    ]

    assert (
        row[
            "totally_symmetric_1minus_representation_support_nonzero"
        ]
        is True
    )

    assert math.isclose(
        row[
            "spatial_spin1_trace_norm"
        ],
        8.0
        /
        3.0,
        rel_tol=0.0,
        abs_tol=1.0e-12,
    )

    assert (
        row[
            "exact_physical_1minus_pole_projector_evaluated"
        ]
        is False
    )


def test_u2v2_reopens_equal_opposite_1minus_representation_support():
    rows = {
        row[
            "pair_id"
        ]:
            row
        for row
        in (
            engineered_totally_symmetric_1minus_gate()[
                "rows"
            ]
        )
    }

    first = rows[
        "U1_V1"
    ][
        "spatial_spin1_trace_vector"
    ]

    second = rows[
        "U2_V2"
    ][
        "spatial_spin1_trace_vector"
    ]

    assert all(
        abs(
            x
            +
            y
        )
        <
        1.0e-12
        for (
            x,
            y,
        )
        in zip(
            first,
            second,
            strict=True,
        )
    )


def test_marzo_lane_is_only_representation_reopened_not_pole_promoted():
    result = (
        h17a10b_summary()
    )

    assert (
        result[
            "marzo2022_protected_family_published"
        ]
        is True
    )

    assert (
        result[
            "marzo2022_unique_massive_physical_pole_sector"
        ]
        ==
        "1_MINUS"
    )

    assert (
        result[
            "marzo2022_engineered_1minus_representation_reopened"
        ]
        is True
    )

    assert (
        result[
            "marzo2022_exact_same_action_source_ward_established"
        ]
        is False
    )

    assert (
        result[
            "marzo2022_exact_physical_1minus_pole_overlap_established"
        ]
        is False
    )

    assert (
        result[
            "engineered_full_torsion_source_reconstructed"
        ]
        is False
    )


def test_a10b_closes_only_bms_rest_density_route_and_promotes_a10c():
    result = (
        h17a10b_summary()
    )

    assert (
        result[
            "a10a_source_state_escape_preserved"
        ]
        is True
    )

    assert (
        result[
            "bms_compact_localized_rest_density_trace_route_closed"
        ]
        is True
    )

    assert (
        result[
            "bms_global_family_closed"
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
            "geometry_optimization_authorized"
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

    assert (
        result[
            "hook17_closed"
        ]
        is False
    )

    assert (
        result[
            "next"
        ]
        ==
        (
            "032H17A10C_MARZO2022_ENGINEERED_1MINUS_"
            "SAME_ACTION_SOURCE_WARD_TORSION_AND_EXACT_POLE_PROJECTOR_GATE"
        )
    )
