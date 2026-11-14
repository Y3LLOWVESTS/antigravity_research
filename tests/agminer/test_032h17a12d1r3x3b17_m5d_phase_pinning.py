"""B17-M5D action-path controls; no physical-force claims."""

import pytest

from antigravity_research.agminer.hook17_r3b_m5d_phase_pinning import (
    _offsets,
    evaluate,
)


def test_symmetrically_registered_offsets():
    offsets = _offsets(
        0.25, 0.0002
    )

    assert offsets[0] == -0.25
    assert offsets[-1] == 0.25
    assert 0.0 in offsets

    assert all(
        -value in offsets
        for value in offsets
    )


def test_invalid_offset_parameter():
    with pytest.raises(ValueError):
        _offsets(0.25, 0.25)


@pytest.fixture(scope="module")
def actual():
    return evaluate(
        0.25, 0.0,
        21147.0, 0.0002
    )


def test_interaction_is_loaded_minus_earth_free(actual):
    for row in actual[
        "common_shift_phase_samples"
    ]:
        assert row[
            "interaction_action_j"
        ] == pytest.approx(
            row["earth_present_action_j"]
            - row["earth_absent_action_j"],
            abs=1e-9,
        )


def test_matched_small_shift_path_identity(actual):
    slopes = actual[
        "matched_earth_and_craft_slopes"
    ]["subcell"]

    for row in slopes.values():
        assert row[
            "path_nonlinearity_difference_j_per_m"
        ] == pytest.approx(
            row["common_shift_slope_j_per_m"]
            - row["paired_sum_slope_j_per_m"],
            abs=1e-9,
        )


def test_one_cell_slope_is_endpoint_secant(actual):
    slope = actual[
        "matched_earth_and_craft_slopes"
    ]["one_cell"]

    assert slope[
        "interaction_action_j"
    ]["common_shift_slope_j_per_m"] == pytest.approx(
        actual[
            "grid_phase_diagnostics"
        ]["one_cell_mean_slope_j_per_m"],
        abs=1e-9,
    )


def test_earth_subtraction_matches_common_slope(actual):
    paired = actual[
        "matched_earth_and_craft_slopes"
    ]["subcell"]

    on = paired[
        "earth_present_action_j"
    ]["common_shift_slope_j_per_m"]

    off = paired[
        "earth_absent_action_j"
    ]["common_shift_slope_j_per_m"]

    interaction = paired[
        "interaction_action_j"
    ]["common_shift_slope_j_per_m"]

    assert interaction == pytest.approx(
        on-off, abs=5e-4
    )


def test_no_device_claims(actual):
    assert actual["source"][
        "net_electric_charge_relative_residual"
    ] < 1e-9

    assert all(
        value["inside_enclosure_radius"]
        for value in actual["source"][
            "support_one_cell"
        ].values()
    )

    assert actual["whole_craft_force_n"] is None
    assert actual["complete_operating_energy_j"] is None
    assert not actual[
        "finite_box_artifact_excluded"
    ]
    assert not actual[
        "exterior_metric_transmission_derived"
    ]
    assert not actual["006d_replaced"]


def test_invalid_runs_fail_closed():
    for args in (
        (0.3, 0.0, 21147.0, 0.0002),
        (0.25, 0.75, 21147.0, 0.0002),
        (0.25, 0.0, 1000.0, 0.0002),
        (0.25, 0.0, 21147.0, 0.1),
    ):
        with pytest.raises(ValueError):
            evaluate(*args)
