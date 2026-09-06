"""
032U — universal linear stress-energy-only rank-3 MAG portal.

Declared assumptions:
  - local Lorentz covariance;
  - weak-field linear response;
  - ordinary matter characterized only by symmetric T_munu;
  - no independent hypermomentum charge;
  - no extra baryon/lepton/species current;
  - no preferred vector or Lorentz-breaking background;
  - no nonlinear extraction of a fluid four-velocity from T;
  - portal source linear in T and its derivatives.

A rank-three source cannot be constructed linearly from rank-two T,
the rank-two metric and rank-four epsilon tensor without adding an
odd-rank object. Their tensor ranks are even and index contractions
remove indices in pairs.

The first local possibility therefore contains one derivative.
For a static compact source every one-derivative linear source has
zero integrated monopole: time derivatives vanish and spatial
derivatives reduce to boundary terms.

This rejects only the universal stress-energy-only MONOPOLE portal.
Derivative dipoles/higher multipoles and genuinely new intrinsic
hypermomentum matter charges remain separate open branches.
"""


class UniversalRank3StressPortalFamily:
    family_id = "032U_UNIVERSAL_RANK3_STRESS_MONOPOLE_PORTAL"
    family_version = "1_LINEAR_T_ONLY_NO_MONOPOLE_THEOREM"
    energy_bound_scope = "PARTIAL_REJECTION_ONLY"

    def sample_bounds(self):
        return {
            "log10_range_m": (-6.0, 6.0),
            "log10_positive_kinetic_norm": (-12.0, 12.0),
            "portal_coefficient": (-100.0, 100.0),
        }

    def canonicalize_params(self, params):
        return {
            k: round(float(v), 12)
            for k, v in params.items()
        }

    def analytic_precheck(self, params, config):
        return {
            "passed": False,
            "failure_code": "T_RANK3_STRESS_ONLY_NO_MONOPOLE",
            "derivative_free_rank3_linear_source": False,
            "leading_derivative_source_monopole": 0.0,
            "derivative_multipole_frontier_closed": False,
        }

    def naturalness_precheck(self, params, config):
        return {"passed": True}

    def eft_precheck(self, params, config):
        return {"passed": True}

    def energy_lower_bound(self, params, config):
        return {"energy_lower_bound_j": 0.0}
