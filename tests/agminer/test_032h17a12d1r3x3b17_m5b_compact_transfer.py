"""B17-M5B compact-source and held-out-grid regressions."""

import numpy as np
import pytest

from antigravity_research.agminer.hook17_r3b_m4b1_source_recovery import (
    assemble_original_aligned_source,
)
from antigravity_research.agminer.hook17_r3b_m5b_compact_transfer import (
    compact_shaped_source,
    evaluate,
    cross_grid_transfer,
    COMPACT_SUPPORT_LIMIT_M,
    ENCLOSURE_RADIUS_M,
)


@pytest.fixture(scope="module")
def source():
    return assemble_original_aligned_source(0.25)


@pytest.fixture(scope="module")
def grids():
    return evaluate(0.25), evaluate(0.2)


@pytest.mark.parametrize("bias", [-0.5, 0.0, 0.5])
def test_spherical_compensation_and_support(source, bias):
    shaped, audit = compact_shaped_source(
        source, bias
    )

    assert audit["compensation_uses_spherical_radius"]

    assert (
        audit["max_nonzero_source_radius_m"]
        <= COMPACT_SUPPORT_LIMIT_M + 1e-12
    )

    assert (
        audit["compensation_source_max_radius_m"]
        < COMPACT_SUPPORT_LIMIT_M
    )

    assert (
        audit["net_electric_charge_relative_residual"]
        < 1e-10
    )

    assert np.isfinite(shaped["j_phi"]).all()
    assert np.isfinite(shaped["j_a"]).all()


def test_shaping_changes_currents(source):
    original, _ = compact_shaped_source(
        source, 0.0
    )

    earth, _ = compact_shaped_source(
        source, 0.5
    )

    sky, _ = compact_shaped_source(
        source, -0.5
    )

    assert np.linalg.norm(
        original["j_phi"] - earth["j_phi"]
    ) > 0

    assert np.linalg.norm(
        original["j_phi"] - sky["j_phi"]
    ) > 0


def test_translated_current_inside_enclosure(grids):
    for row in grids:
        for sign in ("plus", "minus"):
            support = row[
                "source_support_" + sign
            ]

            assert support["inside_enclosure_radius"]

            assert (
                support["max_nodal_source_radius_m"]
                <= ENCLOSURE_RADIUS_M + 1e-12
            )


def test_null_is_not_noether_identity(grids):
    for row in grids:
        defect = np.asarray(
            row["matrices"]["defect"]
        )

        norm = np.asarray(
            row["matrices"]["norm"]
        )

        assert np.linalg.eigvalsh(norm).min() > 0

        for mode in row["null_modes"]:
            x = np.asarray(
                mode["source_amplitude_direction"]
            )

            assert abs(
                float(x @ defect @ x)
            ) < 1e-8

            assert float(
                x @ norm @ x
            ) == pytest.approx(
                1.0, abs=1e-8
            )

        assert not row[
            "source_translation_current_Ward_certified"
        ]

        assert row["whole_craft_force_n"] is None


def test_cross_grid_and_claim_limits(grids):
    row = cross_grid_transfer(*grids)

    assert len(row["cross_grid_rows"]) == sum(
        len(result["null_modes"])
        for result in grids
    )

    assert all(
        result["held_out_relative_defect"] >= 0
        for result in row["cross_grid_rows"]
    )

    assert row["whole_craft_force_n"] is None
    assert row["test_is_not_full_Noether_identity"]

    with pytest.raises(ValueError):
        cross_grid_transfer(grids[0], grids[0])


def test_physical_claims_fail_closed(grids):
    for row in grids:
        assert not row[
            "artificial_oracle_physically_realized"
        ]
        assert not row[
            "exterior_metric_transmission_derived"
        ]
        assert not row[
            "finite_box_artifact_excluded"
        ]
        assert row["complete_operating_energy_j"] is None
        assert not row["006d_replaced"]


def test_unregistered_bias_rejected(source):
    with pytest.raises(ValueError):
        compact_shaped_source(source, 0.75)
