"""Deterministic Pareto-frontier reconstruction."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any


def _dominates(left: dict[str, Any], right: dict[str, Any]) -> bool:
    """Return True when left dominates right on the legacy hard-survivor view."""

    left_values = (
        float(left["energy_j"]),
        -float(left["payload_surface_min"]),
        -float(left["naturalness_margin"]),
        -float(left["stability_margin"]),
        float(left["leakage"]),
        float(left["backreaction"]),
    )

    right_values = (
        float(right["energy_j"]),
        -float(right["payload_surface_min"]),
        -float(right["naturalness_margin"]),
        -float(right["stability_margin"]),
        float(right["leakage"]),
        float(right["backreaction"]),
    )

    no_worse = all(a <= b for a, b in zip(left_values, right_values))
    strictly_better = any(a < b for a, b in zip(left_values, right_values))
    return no_worse and strictly_better


def pareto_frontier(
    rows: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    points = list(rows)
    frontier: list[dict[str, Any]] = []

    for index, point in enumerate(points):
        dominated = False

        for other_index, other in enumerate(points):
            if index == other_index:
                continue

            if _dominates(other, point):
                dominated = True
                break

        if not dominated:
            frontier.append(point)

    return sorted(
        frontier,
        key=lambda row: (
            float(row["energy_j"]),
            str(row.get("candidate_id", "")),
        ),
    )


_MECHANISM_REQUIRED = (
    "energy_j",
    "response_per_complete_joule",
    "productive_participation",
    "kernel_relative",
    "cancellation_ratio",
    "scaffolding_fraction",
)


def _mechanism_vector(row: dict[str, Any]) -> tuple[float, ...]:
    return (
        float(row["energy_j"]),
        -float(row["response_per_complete_joule"]),
        -float(row["productive_participation"]),
        -float(row["kernel_relative"]),
        float(row["cancellation_ratio"]),
        float(row["scaffolding_fraction"]),
        float(row.get("realization_gap") or 1.0),
    )


def _mechanism_dominates(
    left: dict[str, Any],
    right: dict[str, Any],
) -> bool:
    left_values = _mechanism_vector(left)
    right_values = _mechanism_vector(right)
    return (
        all(a <= b for a, b in zip(left_values, right_values))
        and any(a < b for a, b in zip(left_values, right_values))
    )


def mechanism_pareto_frontier(
    rows: Iterable[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Pareto frontier for fully factorized candidates only.

    Missing mechanism metrics are not guessed or silently replaced. Legacy
    candidates remain available through ``pareto_frontier``.
    """

    points = [
        dict(row)
        for row in rows
        if all(row.get(name) is not None for name in _MECHANISM_REQUIRED)
    ]
    frontier: list[dict[str, Any]] = []

    for index, point in enumerate(points):
        if any(
            _mechanism_dominates(other, point)
            for other_index, other in enumerate(points)
            if other_index != index
        ):
            continue
        frontier.append(point)

    return sorted(
        frontier,
        key=lambda row: (
            float(row["energy_j"]),
            -float(row["response_per_complete_joule"]),
            str(row.get("candidate_id", "")),
        ),
    )
