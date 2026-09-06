"""032P-032R independent frontier rerank."""

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "data" / "032p_032r_frontier_rerank_summary.json"

G = 6.67430e-11
C = 299792458.0
E_TARGET = 1.0e7
L_PLANCK = 1.616255e-35


def pform_threshold(p_rank):
    return (p_rank + 1.0) * math.pi ** 2 / 24.0


def compactness(energy_j, radius_m):
    return G * energy_j / (radius_m * C ** 4)


def beta_required(energy_j, radius_m, p_rank):
    return pform_threshold(p_rank) / compactness(energy_j, radius_m)


def radius_required(energy_j, beta, p_rank):
    return (
        beta
        * G
        * energy_j
        / (pform_threshold(p_rank) * C ** 4)
    )


# 032P sign theorem.
on_static_alpha_nonnegative = True
on_static_repulsion = False

# 032Q locality theorem for minimal EC.
ec_torsion_algebraic = True
ec_external_torsion_for_zero_external_spin = 0.0
ec_true_standoff_via_minimal_torsion = False

# 032R most favorable declared point.
comp_planck = compactness(E_TARGET, L_PLANCK)

pform = {}

for p_rank in (1, 2):
    threshold = pform_threshold(p_rank)
    trigger_beta100 = 100.0 * comp_planck
    beta_planck = beta_required(E_TARGET, L_PLANCK, p_rank)
    beta_nuclear = beta_required(E_TARGET, 1.0e-15, p_rank)
    beta_device = beta_required(E_TARGET, 0.10, p_rank)
    r_beta100 = radius_required(E_TARGET, 100.0, p_rank)

    pform[str(p_rank)] = {
        "threshold_beta_compactness": threshold,
        "compactness_at_10mj_planck_radius": comp_planck,
        "max_trigger_beta100_planck_radius": trigger_beta100,
        "trigger_passes_declared_oracle": trigger_beta100 >= threshold,
        "beta_required_planck_radius": beta_planck,
        "beta_required_1fm_radius": beta_nuclear,
        "beta_required_0p1m_radius": beta_device,
        "radius_required_beta100_m": r_beta100,
        "radius_required_beta100_over_planck": r_beta100 / L_PLANCK,
    }

pform_declared_closed = all(
    not row["trigger_passes_declared_oracle"]
    for row in pform.values()
)

result = {
    "branch": "032P_032R_FRONTIER_RERANK",
    "claim_class": "ANALYTIC_FRONTIER_FALSIFICATION_AND_TRIGGER_PREFLIGHT",
    "energy_target_j": E_TARGET,
    "032P": {
        "theory": "2026_UV_COMPLETE_ON_SCALAR_TENSOR",
        "static_yukawa_alpha_nonnegative": on_static_alpha_nonnegative,
        "static_universal_repulsion": on_static_repulsion,
        "static_branch_closed": True,
        "full_dynamic_class_closed": False,
    },
    "032Q": {
        "theory": "MINIMAL_EINSTEIN_CARTAN",
        "torsion_algebraic_in_spin_density": ec_torsion_algebraic,
        "external_torsion_for_zero_external_spin": ec_external_torsion_for_zero_external_spin,
        "minimal_torsion_true_standoff": ec_true_standoff_via_minimal_torsion,
        "minimal_external_standoff_branch_closed": True,
        "propagating_torsion_extensions_closed": False,
    },
    "032R": {
        "theory": "MATTER_TRIGGERED_PFORM_TENSORIZATION",
        "threshold_model": "OPTIMISTIC_SCALAR_LIKE_FIRST_MODE",
        "source_energy_oracle_j": E_TARGET,
        "minimum_source_radius_oracle_m": L_PLANCK,
        "max_abs_beta_declared": 100.0,
        "p_rank_results": pform,
        "declared_10mj_rge_planck_beta_le100_branch_closed": pform_declared_closed,
        "full_pform_family_closed": False,
    },
    "certified_sub10mj_model_found": False,
    "next": "GLOBAL_RERANK_AFTER_FRONTIER_PACK_V5",
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

print("=== 032P-032R FRONTIER RERANK ===")
print("032P_UV_COMPLETE_ON_STATIC_YUKAWA=ATTRACTIVE_OR_ZERO")
print("032P_STATIC_BRANCH_CLOSED=True")
print("032Q_MINIMAL_EC_EXTERNAL_TORSION=ZERO")
print("032Q_MINIMAL_STANDOFF_BRANCH_CLOSED=True")
print("PFORM_10MJ_PLANCK_COMPACTNESS=" + format(comp_planck, ".12e"))

for p_rank in (1, 2):
    row = pform[str(p_rank)]
    print("PFORM_P=" + str(p_rank))
    print("  THRESHOLD=" + format(row["threshold_beta_compactness"], ".12e"))
    print("  BETA100_TRIGGER=" + format(row["max_trigger_beta100_planck_radius"], ".12e"))
    print("  BETA_REQUIRED_PLANCK=" + format(row["beta_required_planck_radius"], ".12e"))
    print("  BETA_REQUIRED_1FM=" + format(row["beta_required_1fm_radius"], ".12e"))
    print("  BETA_REQUIRED_0P1M=" + format(row["beta_required_0p1m_radius"], ".12e"))
    print("  R_REQUIRED_BETA100_M=" + format(row["radius_required_beta100_m"], ".12e"))
    print("  R_REQUIRED_BETA100_OVER_PLANCK=" + format(row["radius_required_beta100_over_planck"], ".12e"))

print("032R_DECLARED_PFORM_TRIGGER_BRANCH_CLOSED=" + str(pform_declared_closed))
print("032R_FULL_PFORM_FAMILY_CLOSED=False")
print("CERTIFIED_SUB10MJ_MODEL_FOUND=False")
print("NEXT=GLOBAL_RERANK_AFTER_FRONTIER_PACK_V5")
