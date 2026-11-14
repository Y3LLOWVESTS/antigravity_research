"""Synthetic tests of B17-M5N envelope-derivative bookkeeping."""

from types import SimpleNamespace

import numpy as np
import pytest
from scipy.sparse import csr_matrix

from antigravity_research.agminer.hook17_r3b_m5n_earth_interface_audit import (
    envelope_rows,
    zone_attribution,
)


def test_exact_synthetic_stationary_derivative():
    # H(lambda)=2+lambda, j=3; u(0)=3/2.
    # dQstar/dlambda = 1/2*(3/2)^2 = 1.125.
    step = 0.001
    u = np.array([1.5])

    plus = csr_matrix([[2.0 + step]])
    minus = csr_matrix([[2.0 - step]])

    actual = envelope_rows(
        u, plus, minus, step, 1.0
    )

    assert actual.sum() == pytest.approx(
        1.125, abs=1e-12
    )

    def q_star(lam):
        return -0.5 * 9.0 / (2.0 + lam)

    finite = (
        q_star(step) - q_star(-step)
    ) / (2.0 * step)

    assert actual.sum() == pytest.approx(
        finite, abs=1e-6
    )


def test_unvarying_material_yields_zero():
    u = np.array([1.0, 2.0])
    matrix = csr_matrix(np.diag([2.0, 3.0]))

    rows = envelope_rows(
        u, matrix, matrix, 0.001, 1.0
    )

    assert np.array_equal(rows, [0.0, 0.0])


def test_wrong_difference_step_rejected():
    matrix = csr_matrix([[2.0]])

    with pytest.raises(ValueError):
        envelope_rows(
            np.ones(1), matrix, matrix, 0.0, 1.0
        )


def test_spatial_attribution_is_exhaustive():
    h = 0.25
    field = {
        "h": h,
        "rhos": np.arange(0.0, 1.0, h),
        "zs": np.arange(-0.5, 0.75, h),
    }

    nz = len(field["zs"]) - 2
    count = nz * (
        (len(field["rhos"]) - 1)
        + (len(field["rhos"]) - 2)
    )

    rows = np.arange(1, count + 1, dtype=float)

    geometry = SimpleNamespace(
        ground_top_relative_z_m=0.0,
        ground_depth_m=0.5,
        ground_radius_m=0.5,
        interface_width_m=0.1,
    )

    result = zone_attribution(
        rows, field, geometry
    )

    regions = list(result["regions"].values())

    assert sum(
        region["row_count"] for region in regions
    ) == count

    assert sum(
        region["signed_derivative_j_per_m"]
        for region in regions
    ) == pytest.approx(rows.sum())

    assert sum(
        region["fraction_of_absolute_contributions"]
        for region in regions
    ) == pytest.approx(1.0)

    assert not result[
        "attribution_is_unique_physical_stress"
    ]
