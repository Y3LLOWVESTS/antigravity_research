"""
032S2 — cubic metric-affine tensor-sector stability provenance gate.

Purpose:
  Determine whether the shear-charge branch of the 2025 cubic MAG exact
  RN-like solution has actually earned a positive-Hamiltonian stability
  claim before any charge-per-joule optimization is attempted.

Published scope:

  The 2025 stability analysis explicitly studies the vector and axial
  modes of torsion and nonmetricity.

  Its exact RN-like solution additionally contains spin, dilation and
  shear charges and generally massive tensor modes.

  The paper explicitly states that the remaining coupling constants are
  expected to be fixed by a further examination of the tensor sector,
  including its kinetics and interactions with the vector and axial modes.

  Therefore:

    MASSIVE_TENSOR_MODES != POSITIVE_HAMILTONIAN_PROOF
    EXACT_SHEAR_SOLUTION != STABILITY_CERTIFICATION
    VECTOR_AXIAL_STABILITY != TENSOR_STABILITY

The July-2026 gravitational-wave follow-up constructs exact dynamical
torsion/nonmetricity waves in this cubic MAG model, but continues to
characterize the underlying stability result as elimination of ghostly
instabilities from the vector and axial sectors.

This run does not reject the shear family.
It prevents AGMINER from promoting an uncertified tensor sector into an
energy optimization or antigravity candidate.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "data" / "032s2_cubic_mag_tensor_sector_stability_provenance_summary.json"
S0 = ROOT / "results" / "data" / "032s0_cubic_mag_dilation_rn_finite_payload_summary.json"
S1 = ROOT / "results" / "data" / "032s1_cubic_mag_dilation_exterior_hamiltonian_summary.json"

ENERGY_TARGET_J = 1.0e7

if not S0.exists():
    raise FileNotFoundError(str(S0))

if not S1.exists():
    raise FileNotFoundError(str(S1))

s0 = json.loads(S0.read_text(encoding="utf-8"))
s1 = json.loads(S1.read_text(encoding="utf-8"))

# ------------------------------------------------------------
# 1. VERIFY PRIOR CUBIC-MAG STATE
# ------------------------------------------------------------

assert s0["finite_payload_metric_level_green"] is True
assert s0["certified_sub10mj_model"] is False

assert s1["declared_stable_pure_dilation_branch_closed"] is True
assert s1["full_cubic_mag_family_closed"] is False
assert s1["shear_charge_branch_closed"] is False

Q_REQUIRED = float(s0["required_q_metric_m2"])
CANONICAL_REFERENCE_J = float(
    s1["positive_exterior_inventory"]["source_surface_energy_j"]
)
CANONICAL_OVER_TARGET = CANONICAL_REFERENCE_J / ENERGY_TARGET_J

# ------------------------------------------------------------
# 2. PUBLISHED 2025 THEORY PROVENANCE
# ------------------------------------------------------------

# These booleans encode explicit scope statements from
# Bahamonde & Gigante Valcarcel, Phys. Rev. D 111, 084058 (2025).

paper_2025_vector_stability_analyzed = True
paper_2025_axial_stability_analyzed = True
paper_2025_tensor_stability_analyzed = False

paper_2025_exact_shear_charge_exists = True
paper_2025_massive_tensor_modes_exist = True

paper_2025_future_tensor_stability_explicitly_required = True

# Tensor quantities explicitly appearing in the exact-solution parameter
# relations include masses and mixing, but their mere appearance does not
# establish ghost/gradient/tachyon freedom.
published_tensor_quantities = [
    "m_t_squared",
    "m_Omega_squared",
    "m_q_squared",
    "alpha_tOmega",
]

# ------------------------------------------------------------
# 3. 2026 FOLLOW-UP PROVENANCE
# ------------------------------------------------------------

# Bahamonde, Gigante Valcarcel & Senovilla,
# Phys. Rev. D 114, 024027 (2026).

paper_2026_exact_gravitational_waves = True
paper_2026_dynamical_torsion_nonmetricity = True

# The follow-up describes the parent model as having eliminated ghostly
# instabilities in the vector and axial sectors. It does not supply the
# missing complete tensor-sector Hamiltonian stability proof needed here.
paper_2026_complete_shear_tensor_hamiltonian_certification = False

# ------------------------------------------------------------
# 4. CLAIM-LOGIC GATES
# ------------------------------------------------------------

exact_solution_is_not_stability_proof = True
mass_term_is_not_positive_hamiltonian_proof = True
vector_axial_health_does_not_imply_tensor_health = True

tensor_ghost_free_certified = (
    paper_2025_tensor_stability_analyzed
    or paper_2026_complete_shear_tensor_hamiltonian_certification
)

tensor_gradient_stable_certified = False
tensor_tachyon_free_certified = False
tensor_hyperbolic_certified = False
tensor_positive_hamiltonian_certified = False

shear_source_charge_hamiltonian_derived = False
shear_charge_per_joule_bound_derived = False
shear_microscopic_source_realized = False

# The shear metric coefficient from the published exact solution depends
# on a large linear combination of quadratic/cubic couplings and N3.
# Since the tensor stability constraints that should further restrict those
# couplings have not been established, its healthy sign/magnitude domain
# is not certified.
shear_metric_coefficient_exists = True
shear_repulsive_sign_in_healthy_tensor_domain_certified = False

# ------------------------------------------------------------
# 5. AGMINER DECISION
# ------------------------------------------------------------

shear_energy_optimization_authorized = (
    tensor_positive_hamiltonian_certified
    and tensor_gradient_stable_certified
    and tensor_tachyon_free_certified
    and tensor_hyperbolic_certified
)

shear_branch_physically_rejected = False
shear_branch_unresolved = not shear_energy_optimization_authorized

if shear_branch_unresolved:
    decision = "UNRESOLVED_TENSOR_SECTOR_HEALTH_NO_SHEAR_OPTIMIZATION"
    next_step = "032T_GLOBAL_RERANK_OR_FULL_TENSOR_HAMILTONIAN_DERIVATION"
else:
    decision = "GREEN_TO_032S3_SHEAR_CHARGE_PER_JOULE"
    next_step = "032S3_SHEAR_CHARGE_PER_JOULE"

result = {
    "branch": "032S2_CUBIC_MAG_TENSOR_SECTOR_STABILITY_PROVENANCE",
    "claim_class": "THEORY_HEALTH_PROVENANCE_GATE",
    "energy_target_j": ENERGY_TARGET_J,
    "prior_metric_requirement": {
        "required_q_metric_m2": Q_REQUIRED,
        "canonical_dilation_reference_j": CANONICAL_REFERENCE_J,
        "canonical_reference_over_target": CANONICAL_OVER_TARGET,
    },
    "paper_2025": {
        "vector_stability_analyzed": paper_2025_vector_stability_analyzed,
        "axial_stability_analyzed": paper_2025_axial_stability_analyzed,
        "tensor_stability_analyzed": paper_2025_tensor_stability_analyzed,
        "exact_shear_charge_exists": paper_2025_exact_shear_charge_exists,
        "massive_tensor_modes_exist": paper_2025_massive_tensor_modes_exist,
        "future_tensor_stability_explicitly_required": paper_2025_future_tensor_stability_explicitly_required,
        "published_tensor_quantities": published_tensor_quantities,
    },
    "paper_2026_gravitational_wave_followup": {
        "exact_gravitational_waves": paper_2026_exact_gravitational_waves,
        "dynamical_torsion_nonmetricity": paper_2026_dynamical_torsion_nonmetricity,
        "complete_shear_tensor_hamiltonian_certification": paper_2026_complete_shear_tensor_hamiltonian_certification,
    },
    "claim_logic": {
        "exact_solution_is_not_stability_proof": exact_solution_is_not_stability_proof,
        "mass_term_is_not_positive_hamiltonian_proof": mass_term_is_not_positive_hamiltonian_proof,
        "vector_axial_health_does_not_imply_tensor_health": vector_axial_health_does_not_imply_tensor_health,
    },
    "tensor_health": {
        "ghost_free_certified": tensor_ghost_free_certified,
        "gradient_stable_certified": tensor_gradient_stable_certified,
        "tachyon_free_certified": tensor_tachyon_free_certified,
        "hyperbolic_certified": tensor_hyperbolic_certified,
        "positive_hamiltonian_certified": tensor_positive_hamiltonian_certified,
    },
    "shear": {
        "metric_coefficient_exists": shear_metric_coefficient_exists,
        "repulsive_sign_in_healthy_tensor_domain_certified": shear_repulsive_sign_in_healthy_tensor_domain_certified,
        "source_charge_hamiltonian_derived": shear_source_charge_hamiltonian_derived,
        "charge_per_joule_bound_derived": shear_charge_per_joule_bound_derived,
        "microscopic_source_realized": shear_microscopic_source_realized,
        "energy_optimization_authorized": shear_energy_optimization_authorized,
        "physically_rejected": shear_branch_physically_rejected,
        "unresolved": shear_branch_unresolved,
    },
    "strict_sub10mj_shear_model": False,
    "full_cubic_mag_family_closed": False,
    "decision": decision,
    "next": next_step,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

print("=== 032S2 RESULT ===")
print("2025_VECTOR_STABILITY_ANALYZED=" + str(paper_2025_vector_stability_analyzed))
print("2025_AXIAL_STABILITY_ANALYZED=" + str(paper_2025_axial_stability_analyzed))
print("2025_TENSOR_STABILITY_ANALYZED=" + str(paper_2025_tensor_stability_analyzed))
print("2025_EXACT_SHEAR_CHARGE_EXISTS=" + str(paper_2025_exact_shear_charge_exists))
print("2025_MASSIVE_TENSOR_MODES_EXIST=" + str(paper_2025_massive_tensor_modes_exist))
print("2025_FUTURE_TENSOR_STABILITY_REQUIRED=" + str(paper_2025_future_tensor_stability_explicitly_required))
print("2026_EXACT_MAG_GRAVITATIONAL_WAVES=" + str(paper_2026_exact_gravitational_waves))
print("2026_COMPLETE_SHEAR_TENSOR_HAMILTONIAN=" + str(paper_2026_complete_shear_tensor_hamiltonian_certification))
print("TENSOR_GHOST_FREE_CERTIFIED=" + str(tensor_ghost_free_certified))
print("TENSOR_GRADIENT_STABLE_CERTIFIED=" + str(tensor_gradient_stable_certified))
print("TENSOR_TACHYON_FREE_CERTIFIED=" + str(tensor_tachyon_free_certified))
print("TENSOR_HYPERBOLIC_CERTIFIED=" + str(tensor_hyperbolic_certified))
print("TENSOR_POSITIVE_HAMILTONIAN_CERTIFIED=" + str(tensor_positive_hamiltonian_certified))
print("SHEAR_REPULSIVE_SIGN_HEALTHY_DOMAIN_CERTIFIED=" + str(shear_repulsive_sign_in_healthy_tensor_domain_certified))
print("SHEAR_CHARGE_PER_JOULE_BOUND_DERIVED=" + str(shear_charge_per_joule_bound_derived))
print("SHEAR_ENERGY_OPTIMIZATION_AUTHORIZED=" + str(shear_energy_optimization_authorized))
print("SHEAR_PHYSICALLY_REJECTED=" + str(shear_branch_physically_rejected))
print("SHEAR_UNRESOLVED=" + str(shear_branch_unresolved))
print("CERTIFIED_SUB10MJ_SHEAR_MODEL=False")
print("FULL_CUBIC_MAG_FAMILY_CLOSED=False")
print("DECISION=" + decision)
print("NEXT=" + next_step)
