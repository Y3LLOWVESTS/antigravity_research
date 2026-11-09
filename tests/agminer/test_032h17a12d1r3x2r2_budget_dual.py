"""R3X2R2 floating-point spectral and energy-budget certificates."""

from __future__ import annotations

import numpy as np
import pytest

from antigravity_research.agminer.hook17_fdual_f_r3x2r2_budget_dual import (
    BRANCH,
    GRID_SPACINGS_M,
    BUDGET_J,
    independent_spectrum,
    budget_bound,
    decide,
    _simplex,
    _energy_identity_error,
    provenance_gate,
)


def test_identity_and_budget():
    assert BRANCH == "032H17A12D1R3X2R2"
    assert GRID_SPACINGS_M == (0.075, 0.050)
    assert BUDGET_J == 10_000_000.0


def test_real_r3x2r1_artifact_is_required():
    assert provenance_gate()["pass"] is True


def test_synthetic_strict_negative_witness_three_spectral_methods():
    forms = np.array([
        -np.eye(2),
        -2 * np.eye(2),
    ])

    result = independent_spectrum(
        forms,
        np.array([1.0, 0.0]),
    )

    assert (
        result["conservative_upper_scaled_per_j"]
        < -0.99999
    )

    assert abs(
        result["eigenvalue_mpmath_70dps"] + 1.0
    ) < 1e-13

    assert result["numerical_interval_proof"] is False


def test_positive_dual_can_still_exclude_under_energy_budget():
    result = budget_bound(1e-9, 100.0)

    assert result[
        "field_budget_excludes_one_g_with_5pct_margin"
    ] is True

    assert result[
        "unlimited_energy_outward_excluded"
    ] is False

    assert result[
        "minimum_field_energy_lower_bound_j"
    ] > 10_000_000.0


def test_negative_dual_excludes_all_positive_energy():
    result = budget_bound(
        -1e-8,
        100.0,
        perturb=1e-9,
    )

    assert result["unlimited_energy_outward_excluded"] is True

    assert result[
        "max_min_acceleration_with_budget_m_s2"
    ] == 0.0

    assert result["minimum_field_energy_lower_bound_j"] is None


def test_perturbation_can_remove_a_marginal_certificate():
    good = budget_bound(
        1e-9,
        100.0,
        perturb=0.0,
    )

    bad = budget_bound(
        1e-9,
        100.0,
        perturb=1e-7,
    )

    assert good[
        "field_budget_excludes_one_g_with_5pct_margin"
    ] is True

    assert bad[
        "field_budget_excludes_one_g_with_5pct_margin"
    ] is False


def test_invalid_solver_weights_rejected():
    with pytest.raises(ValueError):
        _simplex(np.array([-0.25, 1.25]))


def test_clipping_tiny_negative_raw_weight_preserves_simplex():
    mu, report = _simplex(
        np.array([-1e-12, 0.7, 0.3])
    )

    assert mu.min() >= 0.0
    assert abs(mu.sum() - 1) < 1e-14

    assert (
        report["negative_weight_mass_clipped"]
        > 0
    )


def test_orthonormal_maxwell_energy_identity():
    result = _energy_identity_error(
        np.diag([1.0, 7.0, 19.0])
    )

    assert result["pass"] is True
    assert result["all_modes_retained"] is True


def _mock(
    h: float,
    shell: bool,
    augmented: bool,
):
    return {
        "h_m": h,
        "catalogs": {
            "shell_only": {
                "grid_10mj_exclusion_at_1e_minus_9_perturbation":
                    shell,
            },
            "baseline_augmented_diagnostic": {
                "grid_10mj_exclusion_at_1e_minus_9_perturbation":
                    augmented,
            },
        },
    }


def test_scoped_two_grid_closure_never_closes_all_physics():
    result = decide([
        _mock(0.075, True, False),
        _mock(0.05, True, True),
    ])

    assert result["decision"].startswith("GREEN_SCOPED")
    assert result["all_source_families_closed"] is False
    assert result["006d_replaced"] is False
    assert result["continuum_certified"] is False


def test_fine_only_requires_yellow():
    result = decide([
        _mock(0.075, False, False),
        _mock(0.05, True, True),
    ])

    assert result["decision"].startswith("YELLOW_SCOPED")


def test_missing_fine_witness_never_closes_shell():
    result = decide([
        _mock(0.075, True, False),
        _mock(0.05, False, False),
    ])

    assert result["decision"].startswith("YELLOW_HOLD")
