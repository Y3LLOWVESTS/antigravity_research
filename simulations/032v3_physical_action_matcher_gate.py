"""
032V3 — physical-action matcher for the 032V2 response target.

This run does not create a new theory.

It asks which already-explicit physical action is structurally closest
to the response target learned in 032V2, while respecting project closure
and provenance.

Primary literature provenance:

Ghost condensate:
  Arkani-Hamed, Cheng, Luty, Mukohyama,
  hep-th/0312099.
  The low-energy EFT admits a distinction between particle-physics energy
  and gravitational energy and can contain gravitating and antigravitating
  excitations.

Ghost nonlinear dynamics:
  Arkani-Hamed et al., hep-ph/0507120.
  Nonlinear dynamics allows the symmetry-breaking scale M up to roughly
  100 GeV in the minimal theory.

Asymmetron:
  Aqeel, Burrage, Gould, Saffin,
  Phys. Rev. D 113, 056022 (2026), arXiv:2510.25499.
  Universal conformal matter coupling is retained while the bare scalar
  potential receives explicit symmetry breaking.

Project provenance:
  014A already tested the ordinary symmetron image-force approximation
  with a full nonlinear backreacted PDE and found attraction throughout
  the tested domain.

  032S2 leaves cubic-MAG shear unresolved behind tensor stability.

  032T/032U close the simple metric-only and linear-stress-monopole
  nonmetricity matter portals.

The purpose of this run is prioritization, not certification.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]

OUT = ROOT / "results" / "data" / "032v3_physical_action_matcher_summary.json"
CSV_OUT = ROOT / "results" / "data" / "032v3_physical_action_matcher_matrix.csv"

V2 = ROOT / "results" / "data" / "032v2_feasibility_first_action_response_summary.json"
N1 = ROOT / "results" / "data" / "032n1_ghost_condensate_halfspace_continuum_bound_summary.json"
S2 = ROOT / "results" / "data" / "032s2_cubic_mag_tensor_sector_stability_provenance_summary.json"
T = ROOT / "results" / "data" / "032t_symmetry_protected_mag_matter_coupling_summary.json"
U = ROOT / "results" / "data" / "032u_universal_hypermomentum_portal_summary.json"

TARGET_J = 1.0e7
C = 299792458.0
G = 6.67430e-11
PLANCK_LENGTH_M = 1.616255e-35


for path in (V2, N1, S2, T, U):
    if not path.exists():
        raise FileNotFoundError(str(path))

v2 = json.loads(V2.read_text(encoding="utf-8"))
n1 = json.loads(N1.read_text(encoding="utf-8"))
s2 = json.loads(S2.read_text(encoding="utf-8"))
t = json.loads(T.read_text(encoding="utf-8"))
u = json.loads(U.read_text(encoding="utf-8"))


# ============================================================
# 1. RECONSTRUCT THE V2 TARGET
# ============================================================

assert v2["decision"] == "GREEN_ROBUST_SUB10MJ_ACTION_RESPONSE_TARGETS_EXIST"
assert v2["certified_sub10mj_model_found"] is False

least = v2["least_deformed_target"]

V2_EQUIV_J = float(least["reference_equivalent_energy_j"])
V2_LAMBDA = float(least["susceptibility_gain"])
V2_AMP = float(least["amplitude_response_gain"])
V2_TAX = float(least["total_tax"])
V2_EIGMIN = float(least["kinetic_min_eigenvalue"])
V2_COND = float(least["kinetic_condition_number"])

assert V2_EQUIV_J < TARGET_J
assert V2_EIGMIN >= 0.40
assert V2_COND <= 5.0

NO_TAX_AMP_REQUIRED = float(
    v2["exact_requirements"][0]["required_amplitude_response_gain"]
)


# ============================================================
# 2. GHOST-CONDENSATE MATCH
# ============================================================

N1_E_J = float(n1["global_halfspace_floor_kappa10_j"])
N1_KAPPA = float(n1["kappa_max"])
N1_REQUIRED_KAPPA = float(n1["required_kappa_at_m100gev_for_10mj"])
N1_REQUIRED_M_GEV = float(n1["required_m_gev_at_kappa10_for_10mj"])
N1_M_GEV = float(n1["m_gev"])

GHOST_REQUIRED_AMP = N1_REQUIRED_KAPPA / N1_KAPPA
GHOST_REQUIRED_SUSCEPTIBILITY = GHOST_REQUIRED_AMP**2

# Because the N1 optimistic energy scales as 1/kappa^2, the V2 least
# target can be translated into an equivalent kappa only as a design
# target. This is NOT yet an action-level identification of kappa.
GHOST_V2_EQUIV_KAPPA = N1_KAPPA * V2_AMP

ghost_n1_identity_relerr = abs(
    GHOST_REQUIRED_AMP - NO_TAX_AMP_REQUIRED
) / NO_TAX_AMP_REQUIRED

assert ghost_n1_identity_relerr < 1.0e-12
assert n1["full_ghost_condensate_family_closed"] is False
assert n1["field_solution"] is False
assert n1["complete_operating_ledger"] is False

# Published minimal-theory nonlinear analysis motivates M less than or
# roughly equal to 100 GeV. The project therefore does not use the
# 151.9-GeV M-only route as the preferred escape.
ghost_m_only_escape_within_minimal_cap = N1_REQUIRED_M_GEV <= N1_M_GEV

# The unresolved question is much sharper:
# Does the project kappa correspond to a real symmetry-protected EFT
# coefficient that can reach roughly 23-26 without instability,
# strong coupling, or hidden positive energy?
ghost_kappa_explicit_eft_mapping_derived = False
ghost_kappa_23_stability_certified = False
ghost_kappa_23_naturalness_certified = False
ghost_kappa_23_complete_field_certified = False


# ============================================================
# 3. ASYMMETRON MINIMAL SCREENED-BODY SIGN
# ============================================================

# The 2026 asymmetron modifies the bare potential but deliberately retains
# the symmetron Weyl factor to preserve screening:
#
#     A(phi) = 1 + phi^2/(2 M^2) + ...
#
# For a static screened dense body, |phi| grows from approximately zero
# near the body toward the selected vacuum outside.
#
# Therefore phi*dphi/dz > 0 when z points away from the body, and
#
#     F5_z = -d ln A/dz < 0,
#
# meaning the minimal screened-body fifth force points back toward it.

phi, phip, M = sp.symbols("phi phip M", real=True)
M_positive = sp.symbols("M_positive", positive=True)

A = 1 + phi**2/(2*M_positive**2)
dlnA_dz = sp.factor(sp.diff(sp.log(A), phi) * phip)

expected = sp.factor(
    phi*phip / (
        M_positive**2 * A
    )
)

assert sp.simplify(dlnA_dz - expected) == 0

asymmetron_minimal_screened_body_outward = False
asymmetron_minimal_screened_body_direction = "INWARD"

# Explicit symmetry breaking and matter-seeded bubble/domain-wall
# configurations are genuinely newer than 014A and are not closed here.
asymmetron_bubble_branch_closed = False
asymmetron_bubble_finite_payload_repulsion_established = False
asymmetron_bubble_complete_energy_established = False

# Authoritative project result from 014A.
project_014a_standard_symmetron_full_nonlinear_repulsion_found = False
project_014a_tested_cases = 20


# ============================================================
# 4. METRIC-AFFINE MATCHERS
# ============================================================

assert s2["shear"]["unresolved"] is True
assert s2["shear"]["energy_optimization_authorized"] is False

assert t["minimal_matter_branch"]["declared_branch_closed"] is True
assert t["new_q_matter_portal_required_for_rescue"] is True

assert u["declared_linear_stress_monopole_branch_closed"] is True
assert u["full_hypermomentum_portal_class_closed"] is False


# ============================================================
# 5. STRONG-FIELD SCALARIZATION TRIGGER SCALE
# ============================================================

# This is only a scale discriminator, not a no-go theorem.
# Scalarization literature concerns strongly self-gravitating bodies.

mass_10mj_kg = TARGET_J / C**2
compactness_10mj_10cm = G*mass_10mj_kg/(0.10*C**2)
compactness_10mj_planck = G*mass_10mj_kg/(PLANCK_LENGTH_M*C**2)


# ============================================================
# 6. MATCHER MATRIX
# ============================================================

rows = [
    {
        "priority": 1,
        "candidate": "SHIFT_SYMMETRIC_GHOST_CONDENSATE",
        "explicit_action": "YES",
        "healthy_sector": "CONDITIONAL_EFT_BACKGROUND",
        "universal_neutral_metric_response": "YES_GRAVITATIONAL",
        "repulsive_or_antigravitating_mechanism": "YES_IN_LITERATURE_AND_PROJECT_PREFIELD",
        "energy_proximity": "53.2404669_MJ_OPTIMISTIC_N1_CONTROL",
        "v2_amplitude_gap": GHOST_REQUIRED_AMP,
        "hard_blocker": "KAPPA_NOT_YET_MAPPED_TO_EXPLICIT_STABLE_EFT_COEFFICIENT",
        "status": "OPEN_HIGHEST_PRIORITY",
        "next_test": "DERIVE_KAPPA_FROM_EXPLICIT_GHOST_EFT_AND_TEST_KAPPA_23_TO_26",
    },
    {
        "priority": 2,
        "candidate": "2026_ASYMMETRON_BUBBLE_BRANCH",
        "explicit_action": "YES",
        "healthy_sector": "CANONICAL_SCALAR_METASTABLE_VACUA",
        "universal_neutral_metric_response": "YES_JORDAN_METRIC",
        "repulsive_or_antigravitating_mechanism": "NOT_ESTABLISHED_FOR_BUBBLE_PAYLOAD",
        "energy_proximity": "NOT_DERIVED",
        "v2_amplitude_gap": "",
        "hard_blocker": "MINIMAL_SCREENED_BODY_FORCE_INWARD_BUBBLE_STANDOFF_UNRESOLVED",
        "status": "SECONDARY_OPEN_NEW_BRANCH",
        "next_test": "ONLY_AFTER_GHOST_PROVENANCE_OR_IF_BUBBLE_HAS_NEW_OUTWARD_METRIC_SIGN",
    },
    {
        "priority": 3,
        "candidate": "CUBIC_MAG_SHEAR_CHARGE",
        "explicit_action": "YES",
        "healthy_sector": "TENSOR_SECTOR_UNRESOLVED",
        "universal_neutral_metric_response": "YES_IF_EXACT_METRIC_BRANCH_HEALTHY",
        "repulsive_or_antigravitating_mechanism": "METRIC_COEFFICIENT_EXISTS",
        "energy_proximity": "NOT_AUTHORIZED",
        "v2_amplitude_gap": "",
        "hard_blocker": "POSITIVE_TENSOR_HAMILTONIAN_NOT_CERTIFIED",
        "status": "BLOCKED_UNRESOLVED",
        "next_test": "FULL_TENSOR_HAMILTONIAN_ONLY_IF_RERANK_JUSTIFIES_COST",
    },
    {
        "priority": 4,
        "candidate": "HEALTHY_SYMMETRIC_MAG_SPIN3",
        "explicit_action": "YES",
        "healthy_sector": "YES_LINEARIZED",
        "universal_neutral_metric_response": "NO_PORTAL_ESTABLISHED",
        "repulsive_or_antigravitating_mechanism": "NO_MINIMAL_METRIC_ONLY_RESPONSE",
        "energy_proximity": "NOT_AUTHORIZED",
        "v2_amplitude_gap": "",
        "hard_blocker": "ORDINARY_MATTER_SOURCE_PORTAL_ABSENT",
        "status": "BLOCKED_BY_032T_032U",
        "next_test": "WAIT_FOR_EXPLICIT_SYMMETRY_PROTECTED_UNIVERSAL_PORTAL",
    },
    {
        "priority": 5,
        "candidate": "STRONG_FIELD_SCALARIZATION_CLASS",
        "explicit_action": "YES_MULTIPLE_THEORIES",
        "healthy_sector": "THEORY_DEPENDENT",
        "universal_neutral_metric_response": "YES_IN_SCALAR_TENSOR_REALIZATIONS",
        "repulsive_or_antigravitating_mechanism": "NOT_ESTABLISHED_AT_LAB_COMPACTNESS",
        "energy_proximity": "NO_LAB_TRIGGER_ESTABLISHED",
        "v2_amplitude_gap": "",
        "hard_blocker": "KNOWN_SCALARIZATION_IS_STRONG_GRAVITY_TRIGGERED",
        "status": "LOW_PRIORITY_NOT_CLOSED",
        "next_test": "ONLY_PROMOTE_IF_NEW_LOW_COMPACTNESS_ACTIVATION_MECHANISM_FOUND",
    },
]


# ============================================================
# 7. DECISION
# ============================================================

promoted = rows[0]

decision = "GREEN_PHYSICAL_MATCHER_GHOST_CONDENSATE_COEFFICIENT_PROVENANCE_TOP"
next_step = "032V4_GHOST_CONDENSATE_EFFECTIVE_CHARGE_COEFFICIENT_PROVENANCE"

result = {
    "branch": "032V3_PHYSICAL_ACTION_MATCHER",
    "claim_class": "LITERATURE_AND_PROJECT_PROVENANCE_RERANK_NOT_MODEL_CERTIFICATION",
    "strict_target_j": TARGET_J,
    "strict_policy_changed": False,
    "v2_target": {
        "equivalent_energy_j": V2_EQUIV_J,
        "susceptibility_gain": V2_LAMBDA,
        "amplitude_gain": V2_AMP,
        "total_tax": V2_TAX,
        "kinetic_min_eigenvalue": V2_EIGMIN,
        "kinetic_condition_number": V2_COND,
    },
    "ghost_condensate": {
        "n1_energy_j_at_kappa10": N1_E_J,
        "n1_kappa": N1_KAPPA,
        "required_kappa_for_10mj": N1_REQUIRED_KAPPA,
        "required_amplitude_gain": GHOST_REQUIRED_AMP,
        "required_susceptibility_gain": GHOST_REQUIRED_SUSCEPTIBILITY,
        "v2_no_tax_amplitude_identity_relerr": ghost_n1_identity_relerr,
        "v2_least_target_equivalent_kappa": GHOST_V2_EQUIV_KAPPA,
        "required_m_gev_at_kappa10": N1_REQUIRED_M_GEV,
        "minimal_project_m_cap_gev": N1_M_GEV,
        "m_only_escape_within_minimal_cap": ghost_m_only_escape_within_minimal_cap,
        "kappa_explicit_eft_mapping_derived": ghost_kappa_explicit_eft_mapping_derived,
        "kappa_23_stability_certified": ghost_kappa_23_stability_certified,
        "kappa_23_naturalness_certified": ghost_kappa_23_naturalness_certified,
        "kappa_23_complete_field_certified": ghost_kappa_23_complete_field_certified,
        "full_family_closed": n1["full_ghost_condensate_family_closed"],
    },
    "asymmetron": {
        "weyl_factor": "A=1+phi^2/(2M^2)+...",
        "dlnA_dz": str(dlnA_dz),
        "minimal_screened_body_direction": asymmetron_minimal_screened_body_direction,
        "minimal_screened_body_outward": asymmetron_minimal_screened_body_outward,
        "bubble_branch_closed": asymmetron_bubble_branch_closed,
        "bubble_finite_payload_repulsion_established": asymmetron_bubble_finite_payload_repulsion_established,
        "bubble_complete_energy_established": asymmetron_bubble_complete_energy_established,
        "014a_standard_symmetron_tested_cases": project_014a_tested_cases,
        "014a_full_nonlinear_repulsion_found": project_014a_standard_symmetron_full_nonlinear_repulsion_found,
    },
    "strong_field_scale": {
        "10mj_mass_kg": mass_10mj_kg,
        "compactness_at_10cm": compactness_10mj_10cm,
        "compactness_at_planck_length": compactness_10mj_planck,
        "used_as_no_go_theorem": False,
    },
    "matcher_matrix": rows,
    "promoted_candidate": promoted["candidate"],
    "promoted_status": promoted["status"],
    "templates_are_physical_models": False,
    "new_physical_model_certified": False,
    "certified_sub10mj_model_found": False,
    "decision": decision,
    "next": next_step,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

print("=== 032V3 RESULT ===")
print("V2_EQUIV_MJ=" + format(V2_EQUIV_J/1e6, ".12e"))
print("V2_LAMBDA=" + format(V2_LAMBDA, ".12e"))
print("V2_AMPLITUDE_GAIN=" + format(V2_AMP, ".12e"))
print("V2_TOTAL_TAX=" + format(V2_TAX, ".12e"))

print("N1_KAPPA10_MJ=" + format(N1_E_J/1e6, ".12e"))
print("N1_REQUIRED_KAPPA_10MJ=" + format(N1_REQUIRED_KAPPA, ".12e"))
print("N1_REQUIRED_AMP_GAIN=" + format(GHOST_REQUIRED_AMP, ".12e"))
print("N1_REQUIRED_SUSCEPTIBILITY=" + format(GHOST_REQUIRED_SUSCEPTIBILITY, ".12e"))
print("N1_V2_NO_TAX_AMP_IDENTITY_RELERR=" + format(ghost_n1_identity_relerr, ".12e"))
print("V2_LEAST_TARGET_EQUIV_GHOST_KAPPA=" + format(GHOST_V2_EQUIV_KAPPA, ".12e"))
print("N1_REQUIRED_M_GEV_KAPPA10=" + format(N1_REQUIRED_M_GEV, ".12e"))
print("N1_MINIMAL_M_CAP_GEV=" + format(N1_M_GEV, ".12e"))
print("M_ONLY_ESCAPE_WITHIN_MINIMAL_CAP=" + str(ghost_m_only_escape_within_minimal_cap))
print("GHOST_KAPPA_EXPLICIT_EFT_MAPPING=" + str(ghost_kappa_explicit_eft_mapping_derived))

print("ASYMMETRON_MINIMAL_SCREENED_BODY_DIRECTION=" + asymmetron_minimal_screened_body_direction)
print("ASYMMETRON_MINIMAL_SCREENED_BODY_OUTWARD=" + str(asymmetron_minimal_screened_body_outward))
print("ASYMMETRON_BUBBLE_BRANCH_CLOSED=" + str(asymmetron_bubble_branch_closed))
print("PROJECT_014A_FULL_NONLINEAR_REPULSION_FOUND=" + str(project_014a_standard_symmetron_full_nonlinear_repulsion_found))

print("MAG_SHEAR_UNRESOLVED=" + str(s2["shear"]["unresolved"]))
print("MAG_MINIMAL_METRIC_BRANCH_CLOSED=" + str(t["minimal_matter_branch"]["declared_branch_closed"]))
print("MAG_STRESS_MONOPOLE_PORTAL_CLOSED=" + str(u["declared_linear_stress_monopole_branch_closed"]))

print("10MJ_COMPACTNESS_10CM=" + format(compactness_10mj_10cm, ".12e"))
print("10MJ_COMPACTNESS_PLANCK_RADIUS=" + format(compactness_10mj_planck, ".12e"))

print("PROMOTED_CANDIDATE=" + promoted["candidate"])
print("PROMOTED_STATUS=" + promoted["status"])
print("NEW_PHYSICAL_MODEL_CERTIFIED=False")
print("CERTIFIED_SUB10MJ_MODEL_FOUND=NO")
print("DECISION=" + decision)
print("NEXT=" + next_step)
