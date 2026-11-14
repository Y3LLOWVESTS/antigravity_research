"""B17-M4B3B source fidelity checks, not lift certification."""

import numpy as np
import pytest

from antigravity_research.agminer.hook17_r3b_m4b3b_cylindrical_source import (
    deposit_b7_to_axisymmetric_nodes,
    r3b_aligned_source_audit,
)


def _axes(h):
    return (
        np.arange(-10, 10+h/4, h),
        np.arange(0, 10+h/4, h),
    )


def _pure(ell, h, order=48, angles=96):
    zs, rs = _axes(h)

    return deposit_b7_to_axisymmetric_nodes(
        zs,
        rs,
        h,
        [0.] * (ell-1) + [1.],
        radial_order=order,
        angular_order=angles,
    )


@pytest.mark.parametrize("ell", [1, 3, 12])
def test_net_neutral_and_compact(ell):
    row = _pure(ell, 0.25)

    assert row["net_charge_relative_residual"] < 1e-11
    assert row["source_outside_support_count"] == 0
    assert row["j_phi"].size == row["cell_charge"].size
    assert row["whole_craft_force_n"] is None


def test_total_charge_dual_volume():
    h = 0.25
    zs, rs = _axes(h)
    row = _pure(1, h)

    weights = np.tile(
        np.r_[h/8, rs[1:-1]],
        len(zs)-2,
    )

    from_current = float(
        np.dot(
            2*np.pi*h*h*weights,
            row["j_phi"],
        )
    )

    from_deposition = float(
        row["cell_charge"].sum()
    )

    assert from_current == pytest.approx(
        from_deposition, abs=1e-10
    )


def test_2d_dipole_not_exact():
    ratio = _pure(1, 0.25)["moment_rows"][0]["moment_ratio"]
    assert 0.85 < ratio < 1.0


def test_high_multipole_distortion_exposed():
    ratio = _pure(12, 0.25)["moment_rows"][11]["moment_ratio"]
    assert 0.2 < ratio < 0.7


def test_refinement_reduces_high_order_error():
    coarse = _pure(12, 0.25)[
        "moment_rows"
    ][11]["relative_moment_error"]

    mid = _pure(12, 0.10)[
        "moment_rows"
    ][11]["relative_moment_error"]

    fine = _pure(12, 0.05)[
        "moment_rows"
    ][11]["relative_moment_error"]

    assert coarse > mid > fine > 0


def test_quadrature_sensitivity_exposed():
    a = _pure(12, 0.25, 48, 96)[
        "moment_rows"
    ][11]["moment_ratio"]

    b = _pure(12, 0.25, 64, 128)[
        "moment_rows"
    ][11]["moment_ratio"]

    assert 1e-6 < abs(a-b) < 0.03


def test_amplitude_sign_invariance():
    zs, rs = _axes(0.25)

    positive = deposit_b7_to_axisymmetric_nodes(
        zs, rs, 0.25, [2.0]
    )

    negative = deposit_b7_to_axisymmetric_nodes(
        zs, rs, 0.25, [-2.0]
    )

    np.testing.assert_allclose(
        positive["j_phi"],
        -negative["j_phi"],
        rtol=0,
        atol=1e-9,
    )


def test_invalid_inputs():
    zs, rs = _axes(0.25)

    for kwargs in (
        {"shell_width_m": 0},
        {"radial_order": 2},
        {"angular_order": 4},
    ):
        with pytest.raises(ValueError):
            deposit_b7_to_axisymmetric_nodes(
                zs, rs, 0.25, [1.0], **kwargs
            )


def test_unresolved_claims_fail_closed():
    row = _pure(1, 0.25)

    assert not row["higher_multipole_fidelity_certified"]
    assert not row["loaded_earth_reaction_certified"]
    assert row["complete_operating_energy_j"] is None


def test_original_r3b_source_audit():
    row = r3b_aligned_source_audit(0.25)

    assert row["normalization_provenance_relative_error"] < 1e-9
    assert row["source"]["net_charge_relative_residual"] < 1e-10
    assert row["source"]["source_outside_support_count"] == 0
    assert not row["loaded_earth_solver_executed"]
    assert not row["outer_boundary_artifact_excluded"]
    assert row["whole_craft_force_n"] is None
    assert row["complete_operating_energy_j"] is None
    assert not row["006d_replaced"]
