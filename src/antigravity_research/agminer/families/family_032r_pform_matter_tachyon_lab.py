"""
032R — matter-triggered p-form spontaneous-growth laboratory preflight.

Published tachyonic p-form equation, in the paper normalization:

  nabla F =
    [m_X^2 - 8 pi beta_X T /(p+1)] X

for the conformal choice A_X = exp(beta_X eta_X / 2).

For nonrelativistic matter T approximately -rho, beta_X<0 can generate
a negative effective mass squared.

This preflight uses an intentionally favorable scalar-like first-mode
threshold for a uniform source region:

  |beta| * compactness > (p+1) pi^2 / 24.

This is a trigger benchmark, not an exact p-form stellar eigenvalue.

Declared domain is deliberately extreme:
  E_source <= 10 MJ,
  source radius >= Planck length,
  |beta| <= 100,
  p = 1 or 2.

All 10 MJ is allowed to become gravitating source rest energy.
Planck-scale source size is allowed only as a favorable oracle.

Failure closes only this declared matter-trigger domain.
It does not close arbitrarily large coupling, curvature-triggered growth,
or unknown UV-complete p-form theories.
"""

import math


G = 6.67430e-11
C = 299792458.0
E_SOURCE_J = 1.0e7
L_PLANCK_M = 1.616255e-35


class PFormMatterTachyonLabFamily:
    family_id = "032R_PFORM_MATTER_TACHYON_LAB"
    family_version = "1_10MJ_PLANCK_OR_LARGER_BETA_LE100"
    energy_bound_scope = "PARTIAL_REJECTION_ONLY"

    def sample_bounds(self):
        return {
            "log10_abs_beta": (-2.0, 2.0),
            "log10_source_radius_m": (
                math.log10(L_PLANCK_M),
                -1.0,
            ),
            "p_rank": (1.0, 2.0),
        }

    def canonicalize_params(self, params):
        p_rank = int(round(float(params["p_rank"])))
        p_rank = min(2, max(1, p_rank))
        return {
            "log10_abs_beta": round(float(params["log10_abs_beta"]), 12),
            "log10_source_radius_m": round(float(params["log10_source_radius_m"]), 12),
            "p_rank": float(p_rank),
        }

    def analytic_precheck(self, params, config):
        beta = 10.0 ** float(params["log10_abs_beta"])
        radius = 10.0 ** float(params["log10_source_radius_m"])
        p_rank = int(round(float(params["p_rank"])))

        compactness = G * E_SOURCE_J / (radius * C ** 4)
        trigger = beta * compactness
        threshold = (p_rank + 1.0) * math.pi ** 2 / 24.0

        if trigger >= threshold:
            return {
                "passed": True,
                "trigger": trigger,
                "threshold": threshold,
            }

        return {
            "passed": False,
            "failure_code": "T_PFORM_10MJ_NO_TACHYON_TRIGGER",
            "trigger": trigger,
            "threshold": threshold,
        }

    def naturalness_precheck(self, params, config):
        return {"passed": True}

    def eft_precheck(self, params, config):
        return {"passed": True}

    def energy_lower_bound(self, params, config):
        return {"energy_lower_bound_j": E_SOURCE_J}
