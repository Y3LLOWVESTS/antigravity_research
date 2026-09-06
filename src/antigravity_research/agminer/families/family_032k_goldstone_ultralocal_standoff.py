"""
032K — kinetic-conformal Goldstone published ultralocal matter branch.

The literature branch can produce locally repulsive response for concave
kinetic-conformal coupling functions inside extended density gradients.

However the fifth force is exactly local in the published matter branch.
An isolated external source therefore does not exert this fifth force on
a separated compact payload.

This plugin closes only the published ultralocal TRUE-STANDOFF branch.
It does not close non-ultralocal propagating solutions of a future theory.
"""

class KineticConformalGoldstoneUltralocalStandOff:
    family_id = "032K_GOLDSTONE_ULTRALOCAL_STANDOFF"
    family_version = "1_PUBLISHED_ULTRALOCAL_BRANCH"
    energy_bound_scope = "PARTIAL_REJECTION_ONLY"

    def sample_bounds(self):
        return {
            "log10_alpha": (-12.0, -3.0),
            "log10_gradient_scale_m": (-2.0, 2.0),
            "concavity": (-1.0, 0.0),
        }

    def canonicalize_params(self, params):
        return {k: round(float(v), 12) for k, v in params.items()}

    def analytic_precheck(self, params, config):
        return {
            "passed": False,
            "failure_code": "T_ULTRALOCAL_NO_EXTERNAL_STANDOFF",
        }

    def naturalness_precheck(self, params, config):
        return {"passed": True}

    def eft_precheck(self, params, config):
        return {"passed": True}

    def energy_lower_bound(self, params, config):
        return {"energy_lower_bound_j": 0.0}
