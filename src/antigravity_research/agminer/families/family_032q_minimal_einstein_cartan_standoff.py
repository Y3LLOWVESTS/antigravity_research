"""
032Q — minimal Einstein-Cartan separated neutral-payload stand-off branch.

In standard Einstein-Cartan gravity the connection/torsion equation is
algebraic: torsion is proportional to the local intrinsic spin density.

Consequently, outside a compact source region whose spin density vanishes,
the torsion also vanishes. Spin-torsion contact effects can modify dense
matter internally, but there is no propagating exterior torsion field in
the minimal theory that can provide a separated stand-off force.

The ordinary exterior metric gravitational field remains a separate GR
question and does not turn this contact torsion into long-range antigravity.

This gate does NOT close theories with explicit propagating torsion terms.
"""


class MinimalEinsteinCartanStandOffFamily:
    family_id = "032Q_MINIMAL_EINSTEIN_CARTAN_STANDOFF"
    family_version = "1_ALGEBRAIC_TORSION_BRANCH"
    energy_bound_scope = "PARTIAL_REJECTION_ONLY"

    def sample_bounds(self):
        return {
            "spin_fraction": (0.0, 1.0),
            "source_radius_m": (1.0e-6, 10.0),
        }

    def canonicalize_params(self, params):
        return {k: round(float(v), 12) for k, v in params.items()}

    def analytic_precheck(self, params, config):
        return {
            "passed": False,
            "failure_code": "T_EC_TORSION_NO_EXTERNAL_STANDOFF",
        }

    def naturalness_precheck(self, params, config):
        return {"passed": True}

    def eft_precheck(self, params, config):
        return {"passed": True}

    def energy_lower_bound(self, params, config):
        return {"energy_lower_bound_j": 0.0}
