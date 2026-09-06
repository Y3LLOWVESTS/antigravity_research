"""
032L — symmetry-preserving soft-DBI universal static branch.

For the minimal universal matter coupling, the calculable long-range
one-loop potential has leading form proportional to
  -alpha^2 m1 m2 / (Lambda^8 r^7).

For positive masses, real alpha and positive Lambda, the force is
universally attractive. Parameter sampling cannot reverse alpha^2.

Only this static minimal branch is closed here.
Driven or non-static backgrounds are not closed by this gate.
"""

class SoftDBIStaticUniversalFamily:
    family_id = "032L_SOFT_DBI_STATIC_UNIVERSAL"
    family_version = "1_STATIC_MINIMAL_SYMMETRY_BRANCH"
    energy_bound_scope = "PARTIAL_REJECTION_ONLY"

    def sample_bounds(self):
        return {
            "log10_abs_alpha": (-12.0, 3.0),
            "log10_lambda_gev": (-9.0, 6.0),
            "distance_m": (0.101, 10.0),
        }

    def canonicalize_params(self, params):
        return {k: round(float(v), 12) for k, v in params.items()}

    def analytic_precheck(self, params, config):
        return {
            "passed": False,
            "failure_code": "T_SOFT_DBI_STATIC_ATTRACTIVE",
        }

    def naturalness_precheck(self, params, config):
        return {"passed": True}

    def eft_precheck(self, params, config):
        return {"passed": True}

    def energy_lower_bound(self, params, config):
        return {"energy_lower_bound_j": 0.0}
