"""ALPHA-1R1/M5F mathematical and fail-closed tests."""

import math

import pytest

from antigravity_research.agminer.hook17_r3b_m5f_phase_reciprocity import (
    evaluate,
    phase_positions,
)


def test_phase_ensemble_grid_positions():
    phases = phase_positions(0.25, 8)

    assert len(phases) == len(set(phases)) == 8

    assert all(
        -0.125 < phase < 0.125
        for phase in phases
    )

    assert abs(sum(phases)) < 1e-12


def test_phase_origin_control_includes_center():
    assert 0.0 in phase_positions(
        0.25, 4, 0.0
    )


@pytest.mark.parametrize(
    "bins, offset",
    [
        (0, 0.5),
        (100, 0.5),
        (8, -0.1),
        (8, 1.0),
    ],
)
def test_bad_phase_quadratures_fail_closed(
    bins, offset
):
    with pytest.raises(ValueError):
        phase_positions(
            0.25, bins, offset
        )


@pytest.fixture(scope="module")
def run():
    return evaluate(
        0.25, 0.0, False
    )


def test_m5d_aligned_phase_reproduction(run):
    center = next(
        row
        for row in run[
            "quadratures"
        ]["node4"]["phase_rows"]
        if row["phase_m"] == 0.0
    )

    slope = center[
        "slopes"
    ]["interaction_action_j"][
        "common_shift_j_per_m"
    ]

    assert slope == pytest.approx(
        1540.3635913753533,
        abs=0.1,
    )


def test_exact_path_decomposition(run):
    for q in run["quadratures"].values():
        for p in q["phase_rows"]:
            for action in p["slopes"].values():
                assert action[
                    "paired_sum_j_per_m"
                ] == pytest.approx(
                    action[
                        "earth_only_j_per_m"
                    ]
                    + action[
                        "craft_only_j_per_m"
                    ],
                    abs=1e-8,
                )

                assert action[
                    "nonlinear_path_difference_j_per_m"
                ] == pytest.approx(
                    action[
                        "common_shift_j_per_m"
                    ]
                    - action[
                        "paired_sum_j_per_m"
                    ],
                    abs=1e-8,
                )


def test_mean_matches_pointwise_mean(run):
    q = run[
        "quadratures"
    ]["midpoint8"]

    expected = sum(
        p["slopes"][
            "interaction_action_j"
        ]["earth_only_j_per_m"]
        for p in q["phase_rows"]
    ) / 8

    assert q["average_slopes"][
        "interaction_action_j"
    ]["earth_only_j_per_m"] == pytest.approx(
        expected
    )


def test_finite_numerics_and_charge_neutrality(run):
    assert run["source_audit"][
        "net_electric_charge_relative_residual"
    ] < 1e-9

    assert all(
        s["inside_enclosure_radius"]
        for s in run["source_audit"][
            "support_extremes"
        ]
    )

    for q in run["quadratures"].values():
        for p in q["phase_rows"]:
            assert math.isfinite(
                p["center_interaction_action_j"]
            )


def test_physical_success_is_not_misreported(run):
    assert not run[
        "phase_averaged_gradient_is_physical_force"
    ]
    assert not run[
        "interface_action_discretization_certified"
    ]
    assert not run[
        "full_Earth_craft_Noether_identity_certified"
    ]
    assert not run[
        "exterior_metric_transmission_derived"
    ]
    assert run["whole_craft_force_n"] is None
    assert run[
        "complete_operating_energy_j"
    ] is None
    assert not run["006d_replaced"]


@pytest.mark.parametrize(
    "parameters",
    [
        (0.3, 0.0, False, 0.0002),
        (0.25, -0.5, False, 0.0002),
        (0.25, 0.0, False, 0.1),
    ],
)
def test_invalid_physical_controls(parameters):
    with pytest.raises(ValueError):
        evaluate(*parameters)
