"""
032J — shift-symmetric kinetically conformal Goldstone gravity.

Published action class:
  g_phys(mu,nu) = A(X)^2 g_E(mu,nu)
with canonical Goldstone kinetic term and no scalar potential.

Concave coupling functions can generate repulsive fifth-force behavior in
extended density-gradient structures. However, the published mechanism is
ultralocally screened between compact objects.

This plugin tests ONLY the compact source/payload stand-off branch.
Extended-gradient configurations remain a distinct open branch.
"""

from __future__ import annotations



class KineticConformalGoldstoneCompactFamily:
    family_id = "032J_KINETIC_CONFORMAL_GOLDSTONE_COMPACT"
    family_version = "1_COMPACT_BRANCH"
    energy_bound_scope = "PARTIAL_REJECTION_ONLY"

    def sample_bounds(self):
        return {
            "log10_coupling_amplitude": (-12.0, -2.0),
            "log10_kinetic_scale_ev": (-8.0, 6.0),
            "concavity": (-1.0, 1.0),
        }

    def canonicalize_params(self, params):
        return {k: round(float(v), 12) for k, v in params.items()}

    def analytic_precheck(self, params, config):
        concavity = float(params["concavity"])
        if concavity >= 0.0:
            return {
                "passed": False,
                "failure_code": "T_NOT_REPULSIVE_CONCAVITY",
            }
        return {
            "passed": False,
            "failure_code": "T_COMPACT_ULTRALOCAL_SCREENING",
        }

    def naturalness_precheck(self, params, config):
        return {"passed": True}

    def eft_precheck(self, params, config):
        return {"passed": True}

    def energy_lower_bound(self, params, config):
        return {"energy_lower_bound_j": 0.0}
