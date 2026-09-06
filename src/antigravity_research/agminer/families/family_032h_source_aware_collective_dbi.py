"""032H — source-aware collective DBI protected scalars."""

from __future__ import annotations

import math

from .frontier_common import MPL_REDUCED_GEV
from .frontier_common import alpha_value
from .frontier_common import basic_eft_gate
from .frontier_common import collective_dbi_payload_floor_j
from .frontier_common import collective_dbi_source_floor_j
from .frontier_common import collective_naturalness_gate
from .frontier_common import cutoff_gev


class SourceAwareCollectiveDBIFamily:
    family_id = "032H_SOURCE_AWARE_COLLECTIVE_DBI"
    family_version = "3_SHARED_SOURCE_VECTOR_CHARGE"
    energy_bound_scope = "COMPLETE_OPERATING_LOWER_BOUND"

    def sample_bounds(self):
        return {
            "log10_alpha": (-8.0, -0.05),
            "log10_cutoff_gev": (2.24, 5.0),
            "range_m": (0.20, 10.0),
            "log10_n_fields": (0.0, 30.0),
            "log10_dbi_scale_ev": (-8.0, 4.0),
        }

    def canonicalize_params(self, params):
        return {k: round(float(v), 12) for k, v in params.items()}

    def n_fields(self, params):
        return max(
            1,
            int(round(10.0 ** float(params["log10_n_fields"]))),
        )

    def analytic_precheck(self, params, config):
        n = self.n_fields(params)
        passed = n >= 1 and alpha_value(params) > 0.0
        return {
            "passed": passed,
            "failure_code": None if passed else "T003",
        }

    def naturalness_precheck(self, params, config):
        return collective_naturalness_gate(
            params,
            self.n_fields(params),
            config,
        )

    def eft_precheck(self, params, config):
        n = self.n_fields(params)
        scale = 10.0 ** float(params["log10_dbi_scale_ev"])
        basic = basic_eft_gate(params, config, scale)
        species_cutoff = MPL_REDUCED_GEV / math.sqrt(float(n))
        passed = (
            bool(basic["passed"])
            and cutoff_gev(params) < 0.1 * species_cutoff
        )
        return {
            "passed": passed,
            "failure_code": None if passed else "N002",
            "species_cutoff_gev": species_cutoff,
        }

    def energy_lower_bound(self, params, config):
        alpha = alpha_value(params)
        n = self.n_fields(params)
        scale = 10.0 ** float(params["log10_dbi_scale_ev"])
        payload = collective_dbi_payload_floor_j(
            alpha,
            n,
            scale,
            config,
        )
        source = collective_dbi_source_floor_j(
            alpha,
            n,
            scale,
            config,
        )
        return {
            "energy_lower_bound_j": payload + source,
            "payload_floor_j": payload,
            "source_floor_j": source,
            "n_fields": float(n),
        }
