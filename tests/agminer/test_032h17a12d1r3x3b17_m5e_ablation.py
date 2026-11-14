"""M5E interpolation, action and fail-closed regressions."""

import pytest

from antigravity_research.agminer.hook17_r3b_m5e_ablation import (
    evaluate,
)


@pytest.fixture(scope="module")
def result():
    return evaluate(0.25)


def test_solver_residual_and_source_support(result):
    assert result["max_coupled_solver_residual"] < 1e-8
    assert result[
        "source_net_charge_relative_residual"
    ] < 1e-9
    assert all(
        item["inside_enclosure_radius"]
        for item in result[
            "source_support_extreme_shifts"
        ]
    )


def test_interpolation_is_exactly_linear(result):
    row = result[
        "frozen_material_quadratic_midpoint_identity"
    ]
    assert row[
        "source_halfcell_is_linear_interpolant_relative_error_phi"
    ] < 1e-10
    assert row[
        "source_halfcell_is_linear_interpolant_relative_error_a"
    ] < 1e-10


def test_independent_quadratic_identity(result):
    row = result[
        "frozen_material_quadratic_midpoint_identity"
    ]
    assert row["absolute_identity_error_j"] < 1e-6
    assert row[
        "source_only_chord_curvature_j"
    ] == pytest.approx(
        -0.25 * row[
            "independently_solved_increment_current_interaction_action_j"
        ],
        abs=1e-6,
    )


def test_counterfactual_decomposition_is_exact(result):
    center = next(
        row for row in result["samples"]
        if row["translation_m"] == 0
    )["full_interaction_action_j"]

    for sample in result["samples"]:
        reconstructed = (
            sample[
                "source_only_counterfactual_interaction_j"
            ]
            + sample[
                "material_only_counterfactual_interaction_j"
            ]
            + sample[
                "mixed_counterfactual_interaction_j"
            ]
            - center
        )
        assert sample[
            "full_interaction_action_j"
        ] == pytest.approx(
            reconstructed, abs=1e-8
        )


def test_matched_slope_additivity(result):
    rows = result["decomposition"]

    for key in (
        "small_symmetric_slope_j_per_m",
        "one_cell_symmetric_slope_j_per_m",
        "positive_halfcell_deviation_from_endpoint_chord_j",
    ):
        total = (
            rows["source_only"][key]
            + rows["material_only"][key]
            + rows["mixed_difference"][key]
        )
        assert rows["full"][key] == pytest.approx(
            total, abs=1e-7
        )


def test_cannot_certify_thrust(result):
    assert not result[
        "counterfactual_paths_are_physical_motions"
    ]
    assert not result[
        "discrete_current_transport_Ward_certified"
    ]
    assert not result[
        "finite_box_artifact_excluded"
    ]
    assert not result[
        "exterior_metric_transmission_derived"
    ]
    assert result["whole_craft_force_n"] is None
    assert result[
        "complete_operating_energy_j"
    ] is None
    assert not result["006d_replaced"]


@pytest.mark.parametrize(
    "args",
    [
        (0.3, 0.0, False, 0.0002),
        (0.25, -0.5, False, 0.0002),
        (0.25, 0.0, False, 0.1),
    ],
)
def test_invalid_controls_rejected(args):
    with pytest.raises(ValueError):
        evaluate(*args)
