"""
032D — positive polynomial kinetic-screening control family.

Static positive-energy hypothesis:
  rho = 1/2 |grad phi|^2 + |grad phi|^4/(4 M^4).

This family tests whether a simple positive quartic K-mouflage sector can
ever improve the payload energy floor. Because every retained term is
positive, its Tier-0 lower bound is conservative.
"""

from __future__ import annotations

from typing import Any

from .frontier_common import alpha_value
from .frontier_common import basic_eft_gate
from .frontier_common import polynomial_k_payload_floor_j
from .frontier_common import twin_naturalness_gate


class PositivePolynomialKMouflageFamily:
    family_id = "032D_TWIN_PNGB_POSITIVE_K_MOUFLAGE"
    family_version = "1_PRELIMINARY_TIER0"
    energy_bound_scope = "PARTIAL_REJECTION_ONLY"

    def parameter_schema(self) -> dict[str, str]:
        return {
            "log10_alpha": "universal metric coupling",
            "log10_cutoff_gev": "heavy-threshold EFT cutoff",
            "range_m": "scalar range",
            "log10_k_scale_ev": "nonlinear kinetic scale",
        }

    def sample_bounds(self) -> dict[str, tuple[float, float]]:
        return {
            "log10_alpha": (-8.0, 0.0),
            "log10_cutoff_gev": (2.24, 5.0),
            "range_m": (0.20, 10.0),
            "log10_k_scale_ev": (-6.0, 6.0),
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
        passed = alpha_value(params) > 0.0
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
        scale = 10.0 ** float(params["log10_k_scale_ev"])
        return basic_eft_gate(params, config, scale)

    def energy_lower_bound(
        self,
        params: dict[str, float],
        config: dict[str, Any],
    ) -> dict[str, float]:
        alpha = alpha_value(params)
        scale = 10.0 ** float(params["log10_k_scale_ev"])
        return {
            "energy_lower_bound_j": polynomial_k_payload_floor_j(
                alpha,
                scale,
                config,
            )
        }
