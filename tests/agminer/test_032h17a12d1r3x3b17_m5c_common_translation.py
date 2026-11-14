"""B17-M5C finite-box, transport and Noether safeguards."""

import numpy as np
import pytest

from antigravity_research.agminer.hook17_r3b_m4b1_source_recovery import (
    assemble_original_aligned_source,
)

from antigravity_research.agminer.hook17_r3b_m5b_compact_transfer import (
    compact_shaped_source,
)

from antigravity_research.agminer.hook17_r3b_m5c_common_translation import (
    _full_cell_source_transport,
    _material_transport_error,
    _normalized_defect_eigenvalues,
    evaluate,
)


@pytest.fixture(scope="module")
def source():
    base = assemble_original_aligned_source(0.25)
    return compact_shaped_source(base, 0.0)[0]


def test_null_ray_is_not_zero_noether_operator():
    defect = np.diag([-2.0, 3.0])
    norm = np.eye(2)

    np.testing.assert_allclose(
        _normalized_defect_eigenvalues(
            defect, norm
        ),
        [-2.0, 3.0],
    )

    x = np.array([
        np.sqrt(3.0/5),
        np.sqrt(2.0/5),
    ])

    assert abs(x @ defect @ x) < 1e-12
    assert np.linalg.norm(defect) > 1.0


def test_exact_one_cell_current_transport(source):
    result = _full_cell_source_transport(
        source, 0.25
    )

    for row in result.values():
        assert max(
            row["current_shift_relative_l2_errors"]
        ) < 1e-8

        assert (
            row["translated_electric_neutrality"]
            < 1e-9
        )

        assert row["support"][
            "inside_enclosure_radius"
        ]

        assert not row["support"][
            "translated_source_is_exact_physical_current"
        ]


@pytest.mark.parametrize(
    "earth_present", [True, False]
)
def test_material_transport_on_interior(
    source, earth_present
):
    result = _material_transport_error(
        source,
        0.25,
        21147.0,
        earth_present,
    )

    assert max(result.values()) < 1e-8


def test_common_shift_cannot_certify_force():
    result = evaluate(0.25, 0.0)

    assert (
        result["max_coupled_solver_residual"]
        < 1e-8
    )

    assert result["source_audit"][
        "net_electric_charge_relative_residual"
    ] < 1e-9

    matrices = result[
        "common_mode_action_matrices_j_per_m"
    ]

    np.testing.assert_allclose(
        np.asarray(matrices["difference"]),
        np.asarray(matrices["earth_present"])
        - np.asarray(matrices["earth_absent"]),
        atol=1e-6,
    )

    assert not result[
        "finite_box_artifact_excluded"
    ]

    assert not result[
        "moving_current_ward_identity_certified"
    ]

    assert not result[
        "complete_gravity_metric_matter_action"
    ]

    assert result["whole_craft_force_n"] is None
    assert result["complete_operating_energy_j"] is None
    assert not result["006d_replaced"]


def test_invalid_parameters_rejected():
    for h, bias in (
        (0.3, 0.0),
        (0.25, 0.75),
    ):
        with pytest.raises(ValueError):
            evaluate(h, bias)
