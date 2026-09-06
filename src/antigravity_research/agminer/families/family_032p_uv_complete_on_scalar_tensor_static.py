"""
032P — 2026 UV-complete O(N) scalar-tensor static Yukawa branch.

Published weak-field Jordan-frame result:

  V(r) = -G_N m1 m2 / r * [1 + alpha_Y exp(-r/lambda_Y)]

with

  alpha_Y =
    2 x0 f1^2 g0 / (1 + 6 x0 f1^2 g0).

For the physical broken-phase branch x0>0 and g0>0.
Therefore alpha_Y >= 0 independently of the sign of f1.

The static universal fifth force is attractive or zero.

This closes only the published static Yukawa branch.
It does not close arbitrary dynamical extensions of scalar-tensor gravity.
"""

import math


class UVCompleteONScalarTensorStaticFamily:
    family_id = "032P_UV_COMPLETE_ON_SCALAR_TENSOR_STATIC"
    family_version = "1_2026_UV_COMPLETE_YUKAWA_BRANCH"
    energy_bound_scope = "PARTIAL_REJECTION_ONLY"

    def sample_bounds(self):
        return {
            "log10_x0": (-12.0, 12.0),
            "log10_g0": (-60.0, 0.0),
            "f1": (-100.0, 100.0),
            "range_m": (0.001, 10.0),
        }

    def canonicalize_params(self, params):
        return {k: round(float(v), 12) for k, v in params.items()}

    def analytic_precheck(self, params, config):
        x0 = 10.0 ** float(params["log10_x0"])
        g0 = 10.0 ** float(params["log10_g0"])
        f1 = float(params["f1"])

        numerator = 2.0 * x0 * f1 * f1 * g0
        denominator = 1.0 + 6.0 * x0 * f1 * f1 * g0
        alpha_y = numerator / denominator

        if alpha_y < 0.0:
            return {
                "passed": True,
                "alpha_y": alpha_y,
            }

        return {
            "passed": False,
            "failure_code": "T_UV_COMPLETE_ON_YUKAWA_ATTRACTIVE",
            "alpha_y": alpha_y,
        }

    def naturalness_precheck(self, params, config):
        return {"passed": True}

    def eft_precheck(self, params, config):
        return {"passed": True}

    def energy_lower_bound(self, params, config):
        return {"energy_lower_bound_j": 0.0}
