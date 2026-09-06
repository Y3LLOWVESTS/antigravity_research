"""
032T — independent symmetric-MAG source and radiative-provenance gate.

This run distinguishes three accomplishments:

  A. linear ghost/tachyon-free nonmetricity propagation,
  B. radiatively protected nonlinear/EFT foundation,
  C. a universal ordinary-matter source and payload coupling.

They are not interchangeable.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "data" / "032t_symmetry_protected_mag_matter_coupling_summary.json"
S2 = ROOT / "results" / "data" / "032s2_cubic_mag_tensor_sector_stability_provenance_summary.json"

G = 6.67430e-11
C = 299792458.0
ENERGY_TARGET_J = 1.0e7
TARGET_ACCEL = 9.80665
PAYLOAD_RADIUS_M = 0.10
FAR_DISTANCE_M = 2.0 * PAYLOAD_RADIUS_M

# ------------------------------------------------------------
# 1. PRIOR FRONTIER PROVENANCE
# ------------------------------------------------------------

if S2.exists():
    s2 = json.loads(S2.read_text(encoding="utf-8"))
    assert s2["shear"]["unresolved"] is True
    assert s2["shear"]["energy_optimization_authorized"] is False

# ------------------------------------------------------------
# 2. 2025 SIMPLE SYMMETRIC-MAG STRUCTURE
# ------------------------------------------------------------

simple_2025_linear_ghost_tachyon_free_examples_exist = True
simple_2025_graviton_propagator_standard_gr = True

# For the healthy one-extra-state branches used in the classification,
# curvature-nonmetricity mixing is removed.
simple_2025_b_rq4 = 0.0
simple_2025_b_rq6 = 0.0

# The free propagator analysis introduces an independent source for Q.
simple_2025_q_has_independent_rank3_source = True
simple_2025_matter_interactions_classified = False

# ------------------------------------------------------------
# 3. MINIMAL UNIVERSAL-MATTER ASSUMPTION
# ------------------------------------------------------------

# Ordinary neutral source and payload couple only to g_mu_nu.
# No Q-dependent matter operator is inserted by hand.
minimal_matter_metric_only = True
ordinary_q_hypermomentum_source = 0.0

# Abstract linear inverse-propagator demonstration.
Kq, Kh, mix, T = sp.symbols(
    "Kq Kh mix T",
    nonzero=True,
)

K = sp.Matrix([
    [Kq, mix],
    [mix, Kh],
])

J_metric_only = sp.Matrix([0, T])

response_general = sp.simplify(K.inv() * J_metric_only)
response_decoupled = sp.simplify(
    response_general.subs(mix, 0)
)

q_response = sp.simplify(response_decoupled[0])
h_response = sp.simplify(response_decoupled[1])

assert q_response == 0
assert sp.simplify(h_response - T/Kh) == 0

# ------------------------------------------------------------
# 4. STRICT 10-MJ ORDINARY-GR BENCHMARK
# ------------------------------------------------------------

source_mass_kg = ENERGY_TARGET_J / C**2
gr_accel = G * source_mass_kg / FAR_DISTANCE_M**2
gr_shortfall = TARGET_ACCEL / gr_accel

# Direction is inward.
gr_outward_accel = -gr_accel

# No Q response exists in this declared branch.
q_outward_accel = 0.0
total_outward_accel = gr_outward_accel + q_outward_accel

finite_payload_true_standoff = False

# ------------------------------------------------------------
# 5. RADIATIVE / EFT PROVENANCE RERANK
# ------------------------------------------------------------

# 2025 symmetry-first result for parity-preserving totally symmetric
# distortion: symmetry-protected foundations reduce to massless spin-1
# and spin-3 possibilities in addition to the graviton; scalar-generated
# gauge symmetries yield no viable model.
symmetry_first_2025_only_massless_spin1_spin3 = True
symmetry_first_2025_scalar_gauge_viable = False

# Generic tuned linear ghost freedom is not treated as radiatively
# certified under the symmetry-first EFT criterion.
tuned_linear_health_equals_radiative_certification = False

# ------------------------------------------------------------
# 6. 2026 MASSIVE SPIN-3 FRONTIER PROVENANCE
# ------------------------------------------------------------

spin3_2026_linear_healthy_propagation_exists = True
spin3_2026_rank3_nonmetricity_field = True

# What has NOT yet been supplied for our antigravity claim stack:
spin3_2026_universal_neutral_matter_portal_certified = False
spin3_2026_finite_payload_repulsion_certified = False
spin3_2026_charge_per_joule_bound_derived = False
spin3_2026_complete_nonlinear_device_field_certified = False

spin3_energy_optimization_authorized = (
    spin3_2026_universal_neutral_matter_portal_certified
    and spin3_2026_finite_payload_repulsion_certified
)

# ------------------------------------------------------------
# 7. DECISIONS
# ------------------------------------------------------------

minimal_metric_only_branch_closed = (
    simple_2025_graviton_propagator_standard_gr
    and simple_2025_b_rq4 == 0.0
    and simple_2025_b_rq6 == 0.0
    and ordinary_q_hypermomentum_source == 0.0
    and q_response == 0
    and total_outward_accel < 0.0
)

new_portal_required = minimal_metric_only_branch_closed

certified_sub10mj = False

result = {
    "branch": "032T_SYMMETRY_PROTECTED_MAG_MATTER_COUPLING_GATE",
    "claim_class": "TREE_LEVEL_SOURCE_AND_RADIATIVE_PROVENANCE_GATE",
    "energy_target_j": ENERGY_TARGET_J,
    "simple_symmetric_mag_2025": {
        "linear_ghost_tachyon_free_examples_exist": simple_2025_linear_ghost_tachyon_free_examples_exist,
        "standard_graviton_propagator": simple_2025_graviton_propagator_standard_gr,
        "b_rq4": simple_2025_b_rq4,
        "b_rq6": simple_2025_b_rq6,
        "q_has_independent_rank3_source": simple_2025_q_has_independent_rank3_source,
        "matter_interactions_classified": simple_2025_matter_interactions_classified,
    },
    "minimal_matter_branch": {
        "metric_only": minimal_matter_metric_only,
        "ordinary_q_hypermomentum_source": ordinary_q_hypermomentum_source,
        "symbolic_q_response": str(q_response),
        "symbolic_metric_response": str(h_response),
        "source_mass_from_10mj_kg": source_mass_kg,
        "gr_accel_mps2_at_20cm": gr_accel,
        "gr_accel_direction": "INWARD",
        "target_over_gr_accel": gr_shortfall,
        "q_outward_accel_mps2": q_outward_accel,
        "finite_payload_true_standoff": finite_payload_true_standoff,
        "declared_branch_closed": minimal_metric_only_branch_closed,
    },
    "symmetry_first_2025": {
        "only_massless_spin1_spin3_found_for_declared_class": symmetry_first_2025_only_massless_spin1_spin3,
        "scalar_generated_gauge_viable": symmetry_first_2025_scalar_gauge_viable,
        "tuned_linear_health_is_radiative_certification": tuned_linear_health_equals_radiative_certification,
    },
    "massive_spin3_2026": {
        "linear_healthy_propagation_exists": spin3_2026_linear_healthy_propagation_exists,
        "rank3_nonmetricity_field": spin3_2026_rank3_nonmetricity_field,
        "universal_neutral_matter_portal_certified": spin3_2026_universal_neutral_matter_portal_certified,
        "finite_payload_repulsion_certified": spin3_2026_finite_payload_repulsion_certified,
        "charge_per_joule_bound_derived": spin3_2026_charge_per_joule_bound_derived,
        "complete_nonlinear_device_field_certified": spin3_2026_complete_nonlinear_device_field_certified,
        "energy_optimization_authorized": spin3_energy_optimization_authorized,
        "status": "UNRESOLVED_PORTAL_AND_DEVICE_COUPLING",
    },
    "new_q_matter_portal_required_for_rescue": new_portal_required,
    "portal_requirements_if_introduced": [
        "universal_neutral_matter_response",
        "equivalence_principle_consistency",
        "radiative_naturalness",
        "positive_hamiltonian",
        "reciprocity_and_reaction",
        "finite_payload_outward_sign",
        "complete_source_and_control_energy",
    ],
    "certified_sub10mj_model": certified_sub10mj,
    "full_metric_affine_gravity_closed": False,
    "decision": "RED_MINIMAL_METRIC_ONLY_MAG_BRANCH_PORTAL_FRONTIER_OPEN",
    "next": "032U_UNIVERSAL_HYPERMOMENTUM_PORTAL_OR_GLOBAL_RERANK",
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(
    json.dumps(result,indent=2,sort_keys=True)+"\n",
    encoding="utf-8",
)

print("=== 032T RESULT ===")
print("STANDARD_GRAVITON_PROPAGATOR=" + str(simple_2025_graviton_propagator_standard_gr))
print("B_RQ4=" + format(simple_2025_b_rq4, ".1f"))
print("B_RQ6=" + format(simple_2025_b_rq6, ".1f"))
print("MINIMAL_Q_SOURCE=" + format(ordinary_q_hypermomentum_source, ".1f"))
print("SYMBOLIC_Q_RESPONSE=" + str(q_response))
print("SYMBOLIC_METRIC_RESPONSE=" + str(h_response))
print("SOURCE_MASS_10MJ_KG=" + format(source_mass_kg, ".12e"))
print("GR_ACCEL_20CM_MPS2=" + format(gr_accel, ".12e"))
print("TARGET_OVER_GR_ACCEL=" + format(gr_shortfall, ".12e"))
print("GR_DIRECTION=INWARD")
print("NONMETRICITY_OUTWARD_RESPONSE=0")
print("MINIMAL_METRIC_ONLY_MAG_BRANCH_CLOSED=" + str(minimal_metric_only_branch_closed))
print("NEW_Q_MATTER_PORTAL_REQUIRED=" + str(new_portal_required))
print("SYMMETRY_FIRST_ONLY_MASSLESS_SPIN1_SPIN3=" + str(symmetry_first_2025_only_massless_spin1_spin3))
print("MASSIVE_SPIN3_2026_LINEAR_HEALTHY=" + str(spin3_2026_linear_healthy_propagation_exists))
print("MASSIVE_SPIN3_UNIVERSAL_PORTAL_CERTIFIED=" + str(spin3_2026_universal_neutral_matter_portal_certified))
print("MASSIVE_SPIN3_ENERGY_OPTIMIZATION_AUTHORIZED=" + str(spin3_energy_optimization_authorized))
print("CERTIFIED_SUB10MJ_MODEL=False")
print("FULL_MAG_CLOSED=False")
print("DECISION=" + result["decision"])
print("NEXT=" + result["next"])
