"""
032C — twin-protected pNGB with DBI-like positive static kinetic sector.

Effective action hypothesis:
  L_phi = M^4 [1 - sqrt(1 + (grad phi)^2/M^4)] - V_pNGB(phi)
with a universal visible Jordan metric and opposite twin source charge.

Only the finite-payload positive DBI kinetic contribution is used as the
energy lower bound. Source, potential, twin, activation and support energy
are omitted, so Tier-0 survival is only permission for further study.
"""

from __future__ import annotations

from typing import Any

from .frontier_common import alpha_value
from .frontier_common import basic_eft_gate
from .frontier_common import dbi_payload_floor_j
from .frontier_common import twin_naturalness_gate


class TwinProtectedDBIMetricFamily:
    family_id = "032C_TWIN_PNGB_DBI_METRIC"
    family_version = "1_PRELIMINARY_TIER0"
    energy_bound_scope = "PARTIAL_REJECTION_ONLY"

    def parameter_schema(self) -> dict[str, str]:
        return {
            "log10_alpha": "universal visible metric coupling",
            "log10_cutoff_gev": "heavy-threshold EFT cutoff",
            "range_m": "scalar range",
            "log10_dbi_scale_ev": "DBI kinetic scale",
        }

    def sample_bounds(self) -> dict[str, tuple[float, float]]:
        return {
            "log10_alpha": (-8.0, 0.0),
            "log10_cutoff_gev": (2.24, 5.0),
            "range_m": (0.20, 10.0),
            "log10_dbi_scale_ev": (-6.0, 4.0),
        }

    def canonicalize_params(
        self,
        params: dict[str, float],
    ) -> dict[str, float]:
        return {
            key: round(float(value), 12)
            for key, value in params.items()
        }

    def analytic_precheck(
        self,
        params: dict[str, float],
        config: dict[str, Any],
    ) -> dict[str, Any]:
        alpha = alpha_value(params)
        passed = alpha > 0.0 and float(params["range_m"]) > 0.0
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
        scale = 10.0 ** float(params["log10_dbi_scale_ev"])
        return basic_eft_gate(params, config, scale)

    def energy_lower_bound(
        self,
        params: dict[str, float],
        config: dict[str, Any],
    ) -> dict[str, float]:
        alpha = alpha_value(params)
        scale = 10.0 ** float(params["log10_dbi_scale_ev"])
        return {
            "energy_lower_bound_j": dbi_payload_floor_j(
                alpha,
                scale,
                config,
            )
        }
