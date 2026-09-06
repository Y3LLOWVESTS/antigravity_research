"""
032E — collective canonical multiscalar twin-pNGB family.

N independently protected canonical scalars contribute coherently to one
universal physical-metric response. For fixed total acceleration, the
minimum canonical gradient energy depends on the Euclidean coupling norm
alpha_eff = sqrt(N) alpha_single.

This Tier-0 model deliberately does not count the microscopic cost of
realizing N protected source sectors. Any survivor therefore requires a
later complete source and scaffolding ledger.
"""

from __future__ import annotations

import math
from typing import Any

from .frontier_common import MPL_REDUCED_GEV
from .frontier_common import alpha_value
from .frontier_common import basic_eft_gate
from .frontier_common import canonical_payload_floor_j
from .frontier_common import cutoff_gev
from .frontier_common import twin_naturalness_gate


class CollectiveMultiscalarTwinFamily:
    family_id = "032E_COLLECTIVE_MULTISCALAR_TWIN_PNGB"
    family_version = "1_PRELIMINARY_TIER0"
    energy_bound_scope = "PARTIAL_REJECTION_ONLY"

    def parameter_schema(self) -> dict[str, str]:
        return {
            "log10_alpha": "coupling per scalar",
            "log10_cutoff_gev": "heavy-threshold EFT cutoff",
            "range_m": "common scalar range",
            "log10_n_fields": "number of protected scalar fields",
        }

    def sample_bounds(self) -> dict[str, tuple[float, float]]:
        return {
            "log10_alpha": (-8.0, -1.0),
            "log10_cutoff_gev": (2.24, 5.0),
            "range_m": (0.20, 10.0),
            "log10_n_fields": (0.0, 10.0),
        }

    def canonicalize_params(
        self,
        params: dict[str, float],
    ) -> dict[str, float]:
        return {
            key: round(float(value), 12)
            for key, value in params.items()
        }

    def n_fields(self, params: dict[str, float]) -> int:
        return max(
            1,
            int(round(10.0 ** float(params["log10_n_fields"]))),
        )

    def analytic_precheck(
        self,
        params: dict[str, float],
        config: dict[str, Any],
    ) -> dict[str, Any]:
        n_fields = self.n_fields(params)
        passed = n_fields >= 1 and alpha_value(params) > 0.0
        return {
            "passed": passed,
            "failure_code": None if passed else "T003",
        }

    def naturalness_precheck(
        self,
        params: dict[str, float],
        config: dict[str, Any],
    ) -> dict[str, Any]:
        return twin_naturalness_gate(params, config)

    def eft_precheck(
        self,
        params: dict[str, float],
        config: dict[str, Any],
    ) -> dict[str, Any]:
        basic = basic_eft_gate(params, config)
        n_fields = self.n_fields(params)
        species_cutoff = MPL_REDUCED_GEV / math.sqrt(float(n_fields))
        passed = (
            bool(basic["passed"])
            and cutoff_gev(params) < 0.1 * species_cutoff
        )
        return {
            "passed": passed,
            "failure_code": None if passed else "N002",
            "species_cutoff_gev": species_cutoff,
        }

    def energy_lower_bound(
        self,
        params: dict[str, float],
        config: dict[str, Any],
    ) -> dict[str, float]:
        n_fields = self.n_fields(params)
        alpha_eff = (
            math.sqrt(float(n_fields))
            * alpha_value(params)
        )
        return {
            "energy_lower_bound_j": canonical_payload_floor_j(
                alpha_eff,
                config,
            ),
            "n_fields": float(n_fields),
            "alpha_effective": alpha_eff,
        }
