"""
032F — static induced-metric DBI branch.

The symmetry-preserving universal matter metric is taken schematically as
  g_phys(mu,nu) = g(mu,nu) + d_mu(phi) d_nu(phi)/M^4.

For a strictly static scalar configuration d_0(phi)=0, so this term does
not alter g_phys(00). The static Newtonian payload acceleration therefore
vanishes in this restricted branch. Dynamic backgrounds are not closed by
this plugin.
"""

from __future__ import annotations

from typing import Any


class StaticInducedMetricDBIFamily:
    family_id = "032F_STATIC_INDUCED_METRIC_DBI"
    family_version = "1_STATIC_BRANCH_ONLY"

    def parameter_schema(self) -> dict[str, str]:
        return {
            "log10_dbi_scale_ev": "DBI scale",
            "log10_static_gradient_gev2": "static scalar gradient",
        }

    def sample_bounds(self) -> dict[str, tuple[float, float]]:
        return {
            "log10_dbi_scale_ev": (-6.0, 6.0),
            "log10_static_gradient_gev2": (-20.0, -2.0),
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
        return {
            "passed": False,
            "failure_code": "T_STATIC_G00_ZERO",
        }

    def naturalness_precheck(
        self,
        params: dict[str, float],
        config: dict[str, Any],
    ) -> dict[str, Any]:
        return {"passed": True}

    def eft_precheck(
        self,
        params: dict[str, float],
        config: dict[str, Any],
    ) -> dict[str, Any]:
        return {"passed": True}

    def energy_lower_bound(
        self,
        params: dict[str, float],
        config: dict[str, Any],
    ) -> dict[str, float]:
        return {"energy_lower_bound_j": 0.0}
