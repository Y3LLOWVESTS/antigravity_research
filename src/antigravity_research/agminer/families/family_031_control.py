"""
Historical 031 objective-control points.

These points are not reopened as active theories.

Their purpose in 032A is to verify that the hard conservative-complete
10 GJ objective rejects known historical energy inventories.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HistoricalEnergyControl:
    name: str
    energy_gj: float

    @property
    def energy_j(self) -> float:
        return self.energy_gj * 1.0e9


def historical_energy_controls() -> list[HistoricalEnergyControl]:
    return [
        HistoricalEnergyControl(
            "031_R4S_PRESCRIBED_ORACLE",
            82.75,
        ),
        HistoricalEnergyControl(
            "031_EDGE_MICROSCOPIC",
            96.141,
        ),
        HistoricalEnergyControl(
            "031_MORPHOLOGY",
            103.0,
        ),
        HistoricalEnergyControl(
            "031_ROBUST_SOURCE",
            121.553840748599,
        ),
        HistoricalEnergyControl(
            "031_ACTIVATED_ON_CONSERVATIVE",
            127.7824385182716,
        ),
        HistoricalEnergyControl(
            "031_CENTERED_QBALL",
            273.464,
        ),
        HistoricalEnergyControl(
            "031_B7_MINIMAL_DRESSING",
            575.0,
        ),
    ]
