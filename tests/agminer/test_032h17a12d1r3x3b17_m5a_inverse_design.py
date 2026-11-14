"""B17-M5A: inverse-design checks and false-positive barriers."""

import math

import numpy as np
import pytest

from antigravity_research.agminer.hook17_r3b_m5a_inverse_design import (
    evaluate,
    _quadratic_matrix,
    _defect_null_directions,
    field_retention_oracle,
    _shape_source,
)
from antigravity_research.agminer.hook17_r3b_m4b1_source_recovery import (
    assemble_original_aligned_source,
)


@pytest.fixture(scope="module")
def baseline():
    return evaluate(0.25, 21147.0, 0.0002)


@pytest.fixture(scope="module")
def facing():
    return evaluate(
        0.25, 21147.0, 0.0002,
        shape_bias=0.5,
    )


def test_quadratic_polarization_exact():
    matrix = _quadratic_matrix(3.0, 5.0, 17.0)
    x = np.array([1.0, 1.0])

    assert x @ matrix @ x == pytest.approx(17.0)


def test_original_source_net_charge_audited():
    _, neutrality = _shape_source(
        assemble_original_aligned_source(0.25), 0.0
    )
    assert math.isfinite(neutrality)
    assert neutrality < 1e-9


def test_source_bias_monopole_compensated():
    for bias in (0.5, -0.5):
        source, neutrality = _shape_source(
            assemble_original_aligned_source(0.25),
            bias,
        )

        assert neutrality < 1e-10
        assert np.isfinite(source["j_phi"]).all()
        assert np.isfinite(source["j_a"]).all()


def test_response_symmetric_and_norm_positive(baseline):
    matrices = baseline["action_slope_source_matrices"]

    for name in (
        "earth_j_per_m",
        "craft_j_per_m",
        "carrier_gradient_norm_j",
    ):
        matrix = np.array(matrices[name])
        assert np.max(abs(matrix - matrix.T)) < 1e-8

    assert min(
        baseline["basis_norm_positive_eigenvalues"]
    ) > 0


def test_reverse_both_polarities_invariant(baseline):
    cases = baseline["polarity_controls"]

    for name in (
        "earth_action_slope_j_per_m",
        "craft_action_slope_j_per_m",
        "gradient_norm_j_not_device_energy",
    ):
        assert cases["both_positive"][name] == pytest.approx(
            cases["both_reversed"][name],
            abs=1e-9,
        )


def test_reverse_one_polarity_quadratic_identity(baseline):
    cases = baseline["polarity_controls"]
    qe = np.array(
        baseline["action_slope_source_matrices"]["earth_j_per_m"]
    )

    difference = (
        cases["both_positive"]["earth_action_slope_j_per_m"]
        - cases["magnetic_reversed"][
            "earth_action_slope_j_per_m"
        ]
    )

    assert difference == pytest.approx(
        4 * qe[0, 1], abs=1e-8
    )


def test_generalized_eigenvalue_scaling(baseline):
    inv = baseline["inverse_source_space"]
    matrices = baseline["action_slope_source_matrices"]

    h = np.array(matrices["carrier_gradient_norm_j"])
    qe = np.array(matrices["earth_j_per_m"])

    for label in (
        "earth_slope_positive",
        "earth_slope_negative",
    ):
        row = inv["optimal_signs"][label]

        if not row["exists"]:
            continue

        x = np.array(
            row["required_electric_magnetic_current_multipliers"]
        )

        assert x @ h @ x == pytest.approx(
            row["quadratic_norm_needed_for_target_j"],
            rel=1e-10,
        )

        assert abs(x @ qe @ x) == pytest.approx(
            9806.65, rel=1e-10
        )


def test_exact_reciprocal_null_identity(baseline):
    m = baseline["action_slope_source_matrices"]

    qe = np.array(m["earth_j_per_m"])
    qc = np.array(m["craft_j_per_m"])
    h = np.array(m["carrier_gradient_norm_j"])

    for row in baseline["inverse_source_space"][
        "exact_reciprocal_null_directions"
    ]:
        x = np.array(row["source_amplitude_direction"])

        assert x @ h @ x == pytest.approx(
            1.0, abs=1e-9
        )
        assert x @ (qe + qc) @ x == pytest.approx(
            0.0, abs=1e-8
        )


def test_definite_reciprocity_defect_has_no_null():
    assert _defect_null_directions(
        np.eye(2), np.eye(2), np.eye(2)
    ) == []


def test_source_shape_changes_the_control(facing, baseline):
    assert facing["pre_registered_source_shape_bias"] == 0.5
    assert facing["net_electric_charge_fraction"] < 1e-10

    assert (
        facing["action_slope_source_matrices"]["earth_j_per_m"]
        != baseline["action_slope_source_matrices"]["earth_j_per_m"]
    )

    assert not facing[
        "source_geometry_is_microscopically_realized"
    ]


def test_artificial_success_cannot_certify_craft(baseline):
    oracle = baseline["artificial_success_oracle"]

    assert oracle["guaranteed_by_algebra"]
    assert not oracle["physical_action_derived"]
    assert not oracle["genuine_lift"]
    assert oracle["reciprocity_defect_j_per_m"] == 0.0

    assert baseline["whole_craft_force_n"] is None
    assert baseline["full_operating_energy_j"] is None
    assert not baseline["strict_sub_10mj_device_certified"]


def test_exterior_portal_not_assumed(baseline):
    theorem = baseline["exterior_transmission_theorem"]

    assert not theorem[
        "outside_enclosure_carriers_solved_and_transmitted"
    ]
    assert not theorem[
        "new_independently_propagating_metric_mode_derived"
    ]


def test_frozen_field_rescue_is_only_a_counterfactual():
    historical = {
        "cases": {
            "1000eV_ground_air": {
                "states": {
                    "0.0": {
                        "earth_ground_tracer_force_n": -80000.0
                    },
                    "1.0": {
                        "earth_ground_tracer_force_n": -8.0
                    },
                }
            }
        }
    }

    result = field_retention_oracle(
        historical, 9806.65
    )

    assert result[
        "hypothetical_uniform_amplitude_retention_needed"
    ] > 0

    assert result[
        "additional_amplitude_gain_needed"
    ] > 1

    assert not result[
        "source_reaction_and_spacecraft_lift_certified"
    ]


def test_invalid_parameters_rejected():
    invalid = (
        (0.15, 21147.0, 0.0002, 1000.0, 0.0),
        (0.25, -1.0, 0.0002, 1000.0, 0.0),
        (0.25, 21147.0, 0.0002, -1.0, 0.0),
        (0.25, 21147.0, 0.0002, 1000.0, 0.75),
    )

    for args in invalid:
        with pytest.raises(ValueError):
            evaluate(*args)


def test_exact_m4b4_original_action_reproduction(baseline):
    from antigravity_research.agminer.hook17_r3b_m4b4_paired_translation import (
        evaluate as old_evaluate,
    )

    previous = old_evaluate(
        0.25, 21147.0, 0.0002
    )

    current = baseline["polarity_controls"]["both_positive"]

    assert current[
        "earth_action_slope_j_per_m"
    ] == pytest.approx(
        previous["earth_resolved_finite_difference_j_m"],
        rel=1e-6,
        abs=1e-6,
    )

    assert current[
        "craft_action_slope_j_per_m"
    ] == pytest.approx(
        previous["craft_resolved_finite_difference_j_m"],
        rel=1e-6,
        abs=1e-6,
    )
