"""R3X3B0 algebraic, source-mask, and claim-scope tests."""

import numpy as np
from scipy.sparse import bmat, csr_matrix

from antigravity_research.agminer.hook17_fdual_f_r3x3b0_inverse_loading import (
    BRANCH,
    GRIDS_M,
    TARGET_G,
    provenance,
    sign_identity,
    support_audit,
    norm_fraction,
    action_augmentation_triage,
    decide,
)


def mock():
    rhos = np.array([0.0, 0.25, 0.5, 0.75])
    zs = np.array([2.8, 3.05, 3.3, 3.55])

    rho, z = np.meshgrid(rhos, zs)

    c = csr_matrix(
        ([2.0], ([3], [1])),
        shape=(6, 4),
    )

    d = csr_matrix(
        ([3.0], ([2], [0])),
        shape=(4, 6),
    )

    prep = {
        "operators": {
            "k_phi": csr_matrix(np.eye(6) * 2),
            "k_a": csr_matrix(np.eye(4) * 3),
        },
        "coupling": {
            "c": c,
            "d": d,
        },
        "a0_vec": np.array([0.0, 1.0, 0.0, 0.0]),
        "phi0_vec": np.array(
            [1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        ),
    }

    field = {
        "rho_grid": rho,
        "z_grid": z,
        "payload": np.ones_like(rho, dtype=bool),
        "rhos": rhos,
        "zs": zs,
        "h": 0.25,
    }

    return {
        "prep": prep,
        "field": field,
    }


def test_branch_and_target():
    assert BRANCH == "032H17A12D1R3X3B0"
    assert GRIDS_M == (0.075, 0.05)
    assert TARGET_G == 9.80665


def test_real_provenance():
    assert provenance()["pass"] is True


def test_exact_signed_operator_conjugacy():
    assert sign_identity(
        mock()["prep"]
    )["sign_conjugacy_pass"]


def test_conjugacy_requires_magnetic_source_reversal():
    assert sign_identity(
        mock()["prep"]
    )["magnetic_source_reversal_required"] is True


def test_inverse_source_is_full_block_difference():
    prep = mock()["prep"]

    kp = prep["operators"]["k_phi"]
    ka = prep["operators"]["k_a"]

    c = prep["coupling"]["c"]
    d = prep["coupling"]["d"]

    x = np.r_[
        prep["phi0_vec"],
        prep["a0_vec"],
    ]

    baseline = bmat(
        [[kp, None], [None, ka]],
        format="csr",
    ) @ x

    loaded = bmat(
        [[kp, c], [-d, ka]],
        format="csr",
    ) @ x

    required = np.r_[
        c @ prep["a0_vec"],
        -d @ prep["phi0_vec"],
    ]

    assert np.linalg.norm(
        loaded - baseline - required
    ) < 1e-14


def test_counter_source_outside_allowed_support():
    result = support_audit(mock())

    assert result[
        "extra_source_outside_allowed_support"
    ] is True

    assert result[
        "exact_global_preloaded_potentials_with_external_only_old_action_ruled_out_on_grid"
    ]

    assert any(
        channel[
            "residual_l2_fraction_outside_buffered_support"
        ] > 0.5
        for channel in result["channels"]
    )


def test_support_failure_does_not_close_all_altered_fields():
    result = support_audit(mock())

    assert result[
        "all_altered_fields_or_metric_invariants_ruled_out"
    ] is False

    assert result[
        "all_action_derived_compensators_ruled_out"
    ] is False


def test_zero_norm_fraction():
    assert norm_fraction(
        np.zeros(3),
        np.ones(3, dtype=bool),
    ) == 0.0


def test_magnetic_reversal_preserves_energy():
    er, ez = 1.2, -0.3
    br, bz = 0.7, 2.1

    dot = er * br + ez * bz

    reversed_dot = (
        er * (-br) + ez * (-bz)
    )

    assert abs(dot + reversed_dot) < 1e-14

    energy = er**2 + ez**2 + br**2 + bz**2

    reversed_energy = (
        er**2 + ez**2 + (-br)**2 + (-bz)**2
    )

    assert energy == reversed_energy


def test_atlas_has_no_fabricated_energy_certification():
    atlas = action_augmentation_triage({
        "extra_source_outside_allowed_support": True
    })

    assert len(atlas) >= 4

    assert all(
        row["complete_energy_j"] is None
        for row in atlas
    )


def mock_grid(ok=True, outside=True):
    return {
        "signed_sector_action_conjugacy": {
            "sign_conjugacy_pass": ok
        },
        "full_load_direct_solver_pass": ok,
        "inverse_counter_source": {
            "extra_source_outside_allowed_support": outside
        },
    }


def test_two_grid_scoped_decision():
    result = decide(
        [mock_grid(), mock_grid()],
        True,
        True,
    )

    assert result["decision"].startswith("GREEN_SCOPED")

    assert result[
        "different_profile_same_metric_acceleration_excluded"
    ] is False

    assert result["006d_replaced"] is False


def test_failed_provenance_fails_closed():
    result = decide(
        [mock_grid(), mock_grid()],
        False,
        True,
    )

    assert result["decision"].startswith("RED_HOLD")


def test_single_grid_does_not_close_both():
    result = decide(
        [mock_grid()],
        True,
        True,
    )

    assert result["decision"].startswith("RED_HOLD")


def test_one_grid_source_failure_does_not_close_both():
    result = decide(
        [
            mock_grid(outside=True),
            mock_grid(outside=False),
        ],
        True,
        True,
    )

    assert result[
        "external_only_exact_global_mirror_excluded_both_grids"
    ] is False
