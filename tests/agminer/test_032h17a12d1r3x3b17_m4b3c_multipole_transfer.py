"""B17-M4B3C source-only numerical regression."""

import os
from pathlib import Path

import pytest

from antigravity_research.agminer.hook17_r3b_m4b3c_multipole_transfer import (
    evaluate,
)


def _original(grid):
    folder = Path(
        os.environ.get(
            "B17_M4B3B_RESULTS_DIR",
            "results/data",
        )
    )

    paths = sorted(
        folder.glob(
            f"b17_m4b3b_*_h{grid}.json"
        )
    )

    if not paths:
        raise FileNotFoundError(
            f"Missing original M4B3B grid {grid}"
        )

    return paths[-1]


@pytest.fixture(scope="module")
def offcenter():
    return evaluate(_original(0.3))


@pytest.fixture(scope="module")
def centered():
    return evaluate(
        _original(0.3),
        align_source_axis=True,
    )


def test_original_json_reproduction(offcenter):
    assert (
        offcenter[
            "unshifted_original_json_reproduction_error"
        ] < 1e-9
    )


def test_linear_superposition(offcenter, centered):
    for row in (offcenter, centered):
        assert (
            row["linear_superposition_relative_error"]
            < 1e-9
        )

        assert len(row["transfer_matrix"]) == 12
        assert all(
            len(column) == 12
            for column in row["transfer_matrix"]
        )


def test_source_center_alignment_restores_parity(
    offcenter,
    centered,
):
    assert abs(
        offcenter["original_nearest_source_z_m"]
    ) > 1e-3

    assert (
        offcenter[
            "normalized_odd_input_to_even_output_leakage"
        ] > 1e-3
    )

    assert abs(
        centered["original_nearest_source_z_m"]
        + centered["applied_grid_shift_m"]
    ) < 1e-9

    assert (
        centered[
            "normalized_odd_input_to_even_output_leakage"
        ] < 1e-8
    )


def test_alignment_does_not_solve_all_errors(centered):
    assert (
        centered["normalized_mixed_max_mode_error"]
        > 0.01
    )

    assert not centered[
        "exterior_field_convergence_certified"
    ]


def test_source_support_and_neutrality(
    offcenter,
    centered,
):
    for row in (offcenter, centered):
        assert (
            row["max_source_outside_support_count"]
            == 0
        )

        assert (
            row["max_pure_source_charge_neutrality"]
            < 1e-9
        )

        assert (
            row["mixed_source_charge_neutrality"]
            < 1e-9
        )


def test_aligned_grid_controls():
    for h in (0.25, 0.2):
        row = evaluate(_original(h))

        assert abs(
            row["original_nearest_source_z_m"]
        ) < 1e-8

        assert (
            row[
                "normalized_odd_input_to_even_output_leakage"
            ] < 1e-8
        )

        assert (
            row[
                "unshifted_original_json_reproduction_error"
            ] < 1e-9
        )


def test_device_claims_fail_closed(offcenter):
    assert not offcenter[
        "original_r3b_source_exactly_realized"
    ]
    assert not offcenter["loaded_earth_solver_executed"]
    assert offcenter["whole_craft_force_n"] is None
    assert offcenter["complete_operating_energy_j"] is None
    assert not offcenter["006d_replaced"]
