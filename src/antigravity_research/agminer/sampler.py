"""
Deterministic resumable low-discrepancy sampling.
"""

from __future__ import annotations

import warnings
from collections.abc import Mapping

import numpy as np
from scipy.stats import qmc


class SobolSampler:
    def __init__(
        self,
        bounds: Mapping[str, tuple[float, float]],
        *,
        index: int = 0,
    ):
        self.names = tuple(bounds.keys())
        self.bounds = tuple(
            (float(low), float(high))
            for low, high in bounds.values()
        )
        self.index = int(index)

    def sample(
        self,
        count: int,
    ) -> list[dict[str, float]]:
        if count <= 0:
            return []

        engine = qmc.Sobol(
            d=len(self.names),
            scramble=False,
        )

        if self.index > 0:
            engine.fast_forward(self.index)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            unit = engine.random(count)

        lows = np.array(
            [low for low, _ in self.bounds],
            dtype=float,
        )

        highs = np.array(
            [high for _, high in self.bounds],
            dtype=float,
        )

        values = lows + unit * (highs - lows)

        rows: list[dict[str, float]] = []

        for row in values:
            rows.append(
                {
                    name: float(value)
                    for name, value in zip(self.names, row)
                }
            )

        self.index += count
        return rows
