"""
032T — healthy symmetric-MAG minimal neutral-matter branch.

Declared branch:
  ghost/tachyon-free propagating nonmetricity,
  ordinary neutral matter minimally coupled only to the physical metric,
  no separately postulated hypermomentum/nonmetricity matter portal.

Published linear structure:
  - graviton propagator is the standard GR propagator;
  - healthy one-extra-state constructions set curvature-nonmetricity
    mixing coefficients b_RQ4 and b_RQ6 to zero;
  - propagating Q modes have their own rank-three source;
  - matter interactions were not supplied as part of the free-spectrum
    classification.

Therefore, with zero direct Q source, the linear Q response vanishes and
ordinary neutral matter sees only the attractive GR metric response.

This closes ONLY the minimal metric-only matter branch.
It does not close theories with a genuinely new universal Q-matter portal.
"""


class SymmetryProtectedMAGMinimalMatterFamily:
    family_id = "032T_HEALTHY_MAG_MINIMAL_METRIC_MATTER"
    family_version = "1_TREE_LEVEL_SOURCE_GATE"
    energy_bound_scope = "PARTIAL_REJECTION_ONLY"

    def sample_bounds(self):
        return {
            "log10_nonmetricity_mass_gev": (-30.0, 18.0),
            "log10_positive_kinetic_norm": (-12.0, 12.0),
            "mode_selector": (0.0, 3.0),
        }

    def canonicalize_params(self, params):
        return {
            k: round(float(v), 12)
            for k, v in params.items()
        }

    def analytic_precheck(self, params, config):
        return {
            "passed": False,
            "failure_code": "T_HEALTHY_MAG_MINIMAL_MATTER_ONLY_GR",
            "graviton_response": "STANDARD_GR",
            "direct_q_source": 0.0,
            "curvature_q_mixing": 0.0,
            "external_q_response": 0.0,
            "neutral_static_repulsion": False,
        }

    def naturalness_precheck(self, params, config):
        return {"passed": True}

    def eft_precheck(self, params, config):
        return {"passed": True}

    def energy_lower_bound(self, params, config):
        return {"energy_lower_bound_j": 0.0}
