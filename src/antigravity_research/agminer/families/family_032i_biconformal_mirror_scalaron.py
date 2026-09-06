"""
032I — technically natural bi-conformal mirror scalaron.

Literature mechanism:
visible and mirror sectors couple with opposite scalaron signs through
the difference of trace anomalies. The protected model predicts a weak
Yukawa fifth force at meter/sub-meter range.

Tier-0 question:
can a positive-energy opposite-charge mirror source produce NET repulsion
against its unavoidable ordinary gravitational attraction?

For a Yukawa force strength alpha_F defined relative to Newtonian gravity,
net outward acceleration from the same positive source requires
alpha_F * YukawaFactor > 1.
"""

from __future__ import annotations

import math


class BiconformalMirrorScalaronFamily:
    family_id = "032I_BICONFORMAL_MIRROR_SCALARON"
    family_version = "1_LITERATURE_PROTECTED_BRANCH"
    energy_bound_scope = "COMPLETE_OPERATING_LOWER_BOUND"

    def sample_bounds(self):
        return {
            "log10_force_strength": (-6.0, -3.0),
            "range_m": (0.10, 10.0),
            "source_distance_m": (0.101, 2.0),
        }

    def canonicalize_params(self, params):
        return {k: round(float(v), 12) for k, v in params.items()}

    def analytic_precheck(self, params, config):
        alpha_f = 10.0 ** float(params["log10_force_strength"])
        range_m = float(params["range_m"])
        distance = float(params["source_distance_m"])
        y = (1.0 + distance / range_m) * math.exp(-distance / range_m)
        reversal = alpha_f * y > 1.0
        return {
            "passed": reversal,
            "failure_code": None if reversal else "T_FORCE_REVERSAL_LT_GRAVITY",
        }

    def naturalness_precheck(self, params, config):
        return {"passed": True}

    def eft_precheck(self, params, config):
        return {"passed": True}

    def energy_lower_bound(self, params, config):
        alpha_f = 10.0 ** float(params["log10_force_strength"])
        range_m = float(params["range_m"])
        distance = float(params["source_distance_m"])
        y = (1.0 + distance / range_m) * math.exp(-distance / range_m)
        G = 6.67430e-11
        c = 299792458.0
        a = float(config["target_cm_accel_mps2"])
        net_factor = alpha_f * y - 1.0
        if net_factor <= 0.0:
            return {"energy_lower_bound_j": float("inf")}
        source_mass = a * distance ** 2 / (G * net_factor)
        return {"energy_lower_bound_j": source_mass * c ** 2}
