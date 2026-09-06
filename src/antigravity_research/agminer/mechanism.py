"""Introspective-factorized mechanism accounting for AGMINER.

This module turns the durable Introspective lessons into explicit,
unit-tested observables. It does not certify a theory and it does not
replace the conservative complete-energy objective.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Any


DECOMPOSITION_VERSION = "INTROSPECTIVE_FACTORIZED_V1"


@dataclass(frozen=True)
class MechanismMetrics:
    """Factor a useful finite-payload response into physical efficiencies.

    The declared quantities obey

        net_response / complete_energy
        = charge_per_productive_joule
          * kernel_effective
          * productive_participation
          / cancellation_ratio.

    ``productive_charge_abs`` may use a family-defined conserved/source
    normalization. Cross-family comparison should therefore use the final
    response-per-joule and normalized kernel metrics rather than raw charge.
    """

    net_response: float
    gross_response: float
    productive_charge_abs: float
    productive_energy_j: float
    complete_energy_j: float
    kernel_geometric_max: float | None = None
    charge_units: str = "FAMILY_DEFINED"
    decomposition_version: str = DECOMPOSITION_VERSION

    def __post_init__(self) -> None:
        values = {
            "net_response": self.net_response,
            "gross_response": self.gross_response,
            "productive_charge_abs": self.productive_charge_abs,
            "productive_energy_j": self.productive_energy_j,
            "complete_energy_j": self.complete_energy_j,
        }

        for name, value in values.items():
            numeric = float(value)
            if not math.isfinite(numeric):
                raise ValueError(name + " must be finite")
            if numeric <= 0.0:
                raise ValueError(name + " must be positive")

        if self.gross_response < self.net_response:
            raise ValueError("gross_response must be >= net_response")

        if self.complete_energy_j < self.productive_energy_j:
            raise ValueError(
                "complete_energy_j must be >= productive_energy_j"
            )

        if self.kernel_geometric_max is not None:
            maximum = float(self.kernel_geometric_max)
            if not math.isfinite(maximum) or maximum <= 0.0:
                raise ValueError(
                    "kernel_geometric_max must be finite and positive"
                )
            if self.kernel_effective > maximum * (1.0 + 1.0e-12):
                raise ValueError(
                    "kernel_effective cannot exceed kernel_geometric_max"
                )

    @property
    def charge_per_productive_joule(self) -> float:
        return self.productive_charge_abs / self.productive_energy_j

    @property
    def productive_participation(self) -> float:
        return self.productive_energy_j / self.complete_energy_j

    @property
    def scaffolding_fraction(self) -> float:
        return 1.0 - self.productive_participation

    @property
    def cancellation_ratio(self) -> float:
        return self.gross_response / self.net_response

    @property
    def kernel_effective(self) -> float:
        return self.gross_response / self.productive_charge_abs

    @property
    def kernel_relative(self) -> float | None:
        if self.kernel_geometric_max is None:
            return None
        return self.kernel_effective / self.kernel_geometric_max

    @property
    def response_per_complete_joule(self) -> float:
        return self.net_response / self.complete_energy_j

    @property
    def factorized_response_per_joule(self) -> float:
        return (
            self.charge_per_productive_joule
            * self.kernel_effective
            * self.productive_participation
            / self.cancellation_ratio
        )

    @property
    def identity_relative_error(self) -> float:
        direct = self.response_per_complete_joule
        reconstructed = self.factorized_response_per_joule
        return abs(reconstructed - direct) / direct

    @property
    def organization_headroom(self) -> float | None:
        """Optimistic gain if placement/participation/cancellation were ideal.

        This does not change intrinsic charge per productive joule and does not
        claim that the ideal organization is microscopically realizable.
        """

        relative = self.kernel_relative
        if relative is None:
            return None
        return self.cancellation_ratio / (
            self.productive_participation * relative
        )

    def to_record(self) -> dict[str, Any]:
        return {
            "net_response": float(self.net_response),
            "gross_response": float(self.gross_response),
            "productive_charge_abs": float(self.productive_charge_abs),
            "productive_energy_j": float(self.productive_energy_j),
            "complete_energy_j": float(self.complete_energy_j),
            "charge_per_productive_joule": (
                self.charge_per_productive_joule
            ),
            "productive_participation": self.productive_participation,
            "scaffolding_fraction": self.scaffolding_fraction,
            "cancellation_ratio": self.cancellation_ratio,
            "kernel_effective": self.kernel_effective,
            "kernel_geometric_max": self.kernel_geometric_max,
            "kernel_relative": self.kernel_relative,
            "response_per_complete_joule": (
                self.response_per_complete_joule
            ),
            "factorized_response_per_joule": (
                self.factorized_response_per_joule
            ),
            "identity_relative_error": self.identity_relative_error,
            "organization_headroom": self.organization_headroom,
            "charge_units": self.charge_units,
            "decomposition_version": self.decomposition_version,
        }


def mechanism_loss_factors(metrics: MechanismMetrics) -> dict[str, float | None]:
    """Return candidate-internal improvement factors without double counting.

    Historical headroom values are deliberately not used here. Every factor is
    measured from the candidate itself.
    """

    relative = metrics.kernel_relative
    return {
        "participation_headroom": 1.0 / metrics.productive_participation,
        "cancellation_headroom": metrics.cancellation_ratio,
        "kernel_headroom": None if relative is None else 1.0 / relative,
        "organization_headroom": metrics.organization_headroom,
    }
