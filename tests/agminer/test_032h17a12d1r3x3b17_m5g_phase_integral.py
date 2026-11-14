"""ALPHA-1R2/M5G mathematical identity regressions."""

import math

import pytest

from antigravity_research.agminer.hook17_r3b_m5g_phase_integral import (
    endpoint_integral,
    phase_mean_slopes,
    phase_nodes,
)


@pytest.mark.parametrize(
    "h,count",
    [
        (0.25, 8),
        (0.25, 16),
        (0.25, 32),
        (0.2, 32),
    ],
)
def test_phase_nodes_symmetric(h, count):
    nodes = phase_nodes(h, count)

    assert len(nodes) == count
    assert len(set(nodes)) == count

    assert abs(sum(nodes)) < 1e-10

    assert nodes[0] > -h/2
    assert nodes[-1] < h/2


@pytest.mark.parametrize(
    "h,count",
    [
        (0.3, 8),
        (0.25, 1),
        (0.25, 0),
        (0.25, True),
    ],
)
def test_invalid_quadratures_rejected(h, count):
    with pytest.raises(ValueError):
        phase_nodes(h, count)


def test_endpoint_integral_linear_action():
    assert endpoint_integral(
        -2.0,
        3.0,
        0.25,
    ) == pytest.approx(20.0)


@pytest.mark.parametrize(
    "values",
    [
        (0.0, 1.0, 0.0),
        (0.0, float("inf"), 0.2),
        (float("nan"), 1.0, 0.25),
    ],
)
def test_invalid_endpoint_inputs(values):
    with pytest.raises(ValueError):
        endpoint_integral(*values)


@pytest.mark.parametrize(
    "count",
    [8, 16, 32],
)
def test_periodic_grid_pinning_cancels_in_mean(
    count,
):
    h = 0.25

    def synthetic_action(earth, craft):
        common = (earth + craft)/2

        return (
            100.0 * (earth - craft)
            + 3.0 * (earth + craft)
            + 2.0 * math.sin(
                2 * math.pi * common / h
            )
        )

    result = phase_mean_slopes(
        synthetic_action,
        h,
        count,
        0.0002,
    )

    assert result[
        "earth_only_j_per_m"
    ] == pytest.approx(
        103.0,
        abs=1e-5,
    )

    assert result[
        "craft_only_j_per_m"
    ] == pytest.approx(
        -97.0,
        abs=1e-5,
    )

    assert result[
        "paired_sum_j_per_m"
    ] == pytest.approx(
        6.0,
        abs=1e-5,
    )

    assert result[
        "common_shift_j_per_m"
    ] == pytest.approx(
        6.0,
        abs=1e-5,
    )

    assert abs(
        result[
            "common_minus_paired_j_per_m"
        ]
    ) < 1e-5


def test_nonfinite_action_fails_closed():
    with pytest.raises(ArithmeticError):
        phase_mean_slopes(
            lambda earth, craft: float("nan"),
            0.25,
            8,
            0.0002,
        )
