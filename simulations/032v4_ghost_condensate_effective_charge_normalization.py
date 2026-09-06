"""
032V4 — ghost-condensate effective-charge normalization closeout.

Purpose:

Determine whether the kappa used by 032N0/N1 is an independent physical
coefficient of the minimal ghost-condensate EFT, or is normalization-
degenerate with the symmetry-breaking scale M.

Canonical literature EFT:

  Sigma = pi_dot - h00/2

  L_eff = L_E +
          M_phys^4 [
              1/2 Sigma^2
              - alpha1/(2 M_phys^2) Kij^2
              - alpha2/(2 M_phys^2) K^2
              + ...
          ]

The covariant formulation permits a field rescaling so the condensate
ground state is X=1. The coefficient of Sigma^2 then defines the physical
symmetry-breaking scale M_phys.

If one instead writes

  Z M0^4 / 2 * Sigma^2,

then

  M_phys = Z^(1/4) M0.

Thus Z is not a second independent enhancement knob in the minimal EFT.

N1 empirically scales as

  E proportional to 1/(kappa^2 M^4).

Therefore its kappa corresponds algebraically to

  Z = kappa^2

and hence

  M_phys = M sqrt(kappa).

This run verifies that degeneracy directly from the stored N1 result.

It does not close nonminimal ghost-condensate EFTs containing a genuinely
independent symmetry-protected operator that changes gravitational charge
per canonical positive-energy norm.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]

OUT = ROOT / "results" / "data" / "032v4_ghost_condensate_effective_charge_normalization_summary.json"
CSV_OUT = ROOT / "results" / "data" / "032v4_ghost_kappa_m_degeneracy.csv"

N1 = ROOT / "results" / "data" / "032n1_ghost_condensate_halfspace_continuum_bound_summary.json"
V3 = ROOT / "results" / "data" / "032v3_physical_action_matcher_summary.json"

TARGET_J = 1.0e7
STRETCH_TARGET_J = 1.0e6
FIELD_TARGET_J = 1.0e5
CANONICAL_M_CAP_GEV = 100.0

for path in (N1, V3):
    if not path.exists():
        raise FileNotFoundError(str(path))

n1 = json.loads(N1.read_text(encoding="utf-8"))
v3 = json.loads(V3.read_text(encoding="utf-8"))

assert v3["promoted_candidate"] == "SHIFT_SYMMETRIC_GHOST_CONDENSATE"
assert v3["ghost_condensate"]["kappa_explicit_eft_mapping_derived"] is False

# ============================================================
# 1. READ AUTHORITATIVE N1 NUMBERS
# ============================================================

E_K1_M100 = float(n1["global_halfspace_floor_kappa1_j"])
E_K10_M100 = float(n1["global_halfspace_floor_kappa10_j"])

KAPPA_N1_MAX = float(n1["kappa_max"])
M_N1_GEV = float(n1["m_gev"])

KAPPA_REQUIRED = float(n1["required_kappa_at_m100gev_for_10mj"])
M_REQUIRED_K10 = float(n1["required_m_gev_at_kappa10_for_10mj"])
M_REQUIRED_K1 = float(n1["required_m_gev_at_kappa1_for_10mj"])

assert abs(M_N1_GEV - 100.0) < 1.0e-12
assert abs(KAPPA_N1_MAX - 10.0) < 1.0e-12

# ============================================================
# 2. SYMBOLIC NORMALIZATION REDUNDANCY
# ============================================================

Z, M0, sigma = sp.symbols("Z M0 sigma", positive=True)
Mphys = sp.symbols("Mphys", positive=True)

L_general = sp.Rational(1,2) * Z * M0**4 * sigma**2

L_canonical = sp.simplify(
    L_general.subs(
        Z,
        (Mphys/M0)**4,
    )
)

expected_canonical = sp.Rational(1,2) * Mphys**4 * sigma**2

normalization_identity = sp.simplify(
    L_canonical - expected_canonical
) == 0

assert normalization_identity

# N1 has energy scaling 1/kappa^2 at fixed M.
# This is exactly reproduced by Z=kappa^2.

kappa = sp.symbols("kappa", positive=True)
M = sp.symbols("M", positive=True)

Mphys_from_kappa = sp.simplify(
    M * (kappa**2)**sp.Rational(1,4)
)

assert sp.simplify(Mphys_from_kappa - M*sp.sqrt(kappa)) == 0

# ============================================================
# 3. NUMERICALLY PROVE N1 DEPENDS ONLY ON M SQRT(KAPPA)
# ============================================================

energy_ratio = E_K1_M100 / E_K10_M100
expected_ratio = KAPPA_N1_MAX**2
energy_scaling_relerr = abs(energy_ratio-expected_ratio)/expected_ratio

assert energy_scaling_relerr < 1.0e-12

MEFF_K1_M100 = M_N1_GEV
MEFF_K10_M100 = M_N1_GEV * math.sqrt(KAPPA_N1_MAX)
MEFF_REQUIRED_FROM_KAPPA = M_N1_GEV * math.sqrt(KAPPA_REQUIRED)
MEFF_REQUIRED_FROM_K10 = M_REQUIRED_K10 * math.sqrt(10.0)
MEFF_REQUIRED_FROM_K1 = M_REQUIRED_K1

required_meff_values = [
    MEFF_REQUIRED_FROM_KAPPA,
    MEFF_REQUIRED_FROM_K10,
    MEFF_REQUIRED_FROM_K1,
]

required_meff_spread = (
    max(required_meff_values)-min(required_meff_values)
) / MEFF_REQUIRED_FROM_K1

assert required_meff_spread < 1.0e-12

# Reconstruct N1 kappa=10 point using only M_eff.

E_FROM_MEFF_K10 = E_K1_M100 * (
    CANONICAL_M_CAP_GEV / MEFF_K10_M100
)**4

k10_reconstruction_relerr = abs(
    E_FROM_MEFF_K10-E_K10_M100
) / E_K10_M100

assert k10_reconstruction_relerr < 1.0e-12

# ============================================================
# 4. APPLY THE LITERATURE CANONICAL M CAP
# ============================================================

# The 2005 nonlinear theory quotes the bound on the physical scale M
# appearing in the canonically normalized low-energy EFT.

PHYSICAL_M_CAP_GEV = CANONICAL_M_CAP_GEV

# If M_phys <= 100 GeV, the best possible N1 energy in this minimal
# normalized branch is simply the kappa=1, M=100 result.

CANONICAL_MINIMAL_FLOOR_J = E_K1_M100
CANONICAL_MINIMAL_FLOOR_GJ = CANONICAL_MINIMAL_FLOOR_J/1.0e9
CANONICAL_FLOOR_OVER_10MJ = CANONICAL_MINIMAL_FLOOR_J/TARGET_J

# Largest kappa that can coexist with bare M=100 while respecting
# M_phys<=100 is exactly one.

KAPPA_MAX_AT_M100_UNDER_PHYSICAL_CAP = (
    PHYSICAL_M_CAP_GEV/M_N1_GEV
)**2

assert abs(KAPPA_MAX_AT_M100_UNDER_PHYSICAL_CAP-1.0) < 1.0e-15

# The old N1 kappa=10, M=100 point corresponds to a canonical physical
# scale above the literature cap.

K10_M100_PHYSICAL_CAP_RATIO = MEFF_K10_M100/PHYSICAL_M_CAP_GEV

REQUIRED_PHYSICAL_SCALE_RATIO = MEFF_REQUIRED_FROM_K1/PHYSICAL_M_CAP_GEV

# ============================================================
# 5. STRETCH-TARGET SCALE REQUIREMENTS
# ============================================================

def required_meff(target_j: float) -> float:
    return PHYSICAL_M_CAP_GEV * (
        CANONICAL_MINIMAL_FLOOR_J/target_j
    )**0.25

MEFF_FOR_10MJ = required_meff(TARGET_J)
MEFF_FOR_1MJ = required_meff(STRETCH_TARGET_J)
MEFF_FOR_100KJ = required_meff(FIELD_TARGET_J)

assert abs(MEFF_FOR_10MJ-MEFF_REQUIRED_FROM_K1)/MEFF_FOR_10MJ < 1.0e-12

# ============================================================
# 6. PARAMETER-DEGENERACY TABLE
# ============================================================

rows = []

for kval in (1.0, 2.0, 5.0, 10.0, KAPPA_REQUIRED, 25.682520968387075):
    meff = M_N1_GEV*math.sqrt(kval)
    energy = E_K1_M100 * (
        CANONICAL_M_CAP_GEV/meff
    )**4

    rows.append({
        "kappa": kval,
        "bare_m_gev": M_N1_GEV,
        "physical_m_eff_gev": meff,
        "physical_cap_ratio": meff/PHYSICAL_M_CAP_GEV,
        "n1_equivalent_energy_j": energy,
        "n1_equivalent_energy_mj": energy/1.0e6,
        "within_minimal_canonical_m_cap": meff <= PHYSICAL_M_CAP_GEV*(1.0+1e-12),
        "independent_eft_lever_certified": False,
    })

CSV_OUT.parent.mkdir(parents=True,exist_ok=True)

with CSV_OUT.open("w",newline="",encoding="utf-8") as handle:
    writer=csv.DictWriter(handle,fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

# ============================================================
# 7. CLAIM DECISION
# ============================================================

kappa_independent_minimal_eft_parameter_certified = False

minimal_canonical_ghost_sub10_closed = (
    CANONICAL_MINIMAL_FLOOR_J >= TARGET_J
    and MEFF_FOR_10MJ > PHYSICAL_M_CAP_GEV
)

full_ghost_condensate_family_closed = False

# What remains open is materially different:
# an explicit nonminimal operator must change charge per canonical norm,
# not merely rename the coefficient of Sigma^2.
nonredundant_charge_operator_frontier_open = True

decision = "RED_MINIMAL_GHOST_KAPPA_LEVER_NORMALIZATION_REDUNDANT"
next_step = "032V5_NONREDUNDANT_PHYSICAL_SUSCEPTIBILITY_ACTION_RERANK"

result = {
    "branch": "032V4_GHOST_CONDENSATE_EFFECTIVE_CHARGE_NORMALIZATION",
    "claim_class": "EFT_NORMALIZATION_AND_PARAMETER_PROVENANCE_CLOSEOUT",
    "strict_target_j": TARGET_J,
    "strict_policy_changed": False,
    "literature_structure": {
        "canonical_sigma_sector": "M_phys^4/2*(pi_dot-h00/2)^2",
        "condensate_field_rescaled_to_X_equals_1": True,
        "physical_scale_m_cap_gev": PHYSICAL_M_CAP_GEV,
        "independent_minimal_kappa_present": False,
    },
    "n1_scaling": {
        "energy_kappa1_m100_j": E_K1_M100,
        "energy_kappa10_m100_j": E_K10_M100,
        "energy_ratio": energy_ratio,
        "expected_kappa_squared_ratio": expected_ratio,
        "relative_error": energy_scaling_relerr,
        "equivalent_physical_scale": "M_eff=M*sqrt(kappa)",
    },
    "physical_scale": {
        "m_eff_kappa1_m100_gev": MEFF_K1_M100,
        "m_eff_kappa10_m100_gev": MEFF_K10_M100,
        "m_eff_required_10mj_from_kappa_gev": MEFF_REQUIRED_FROM_KAPPA,
        "m_eff_required_10mj_from_kappa10_m_gev": MEFF_REQUIRED_FROM_K10,
        "m_eff_required_10mj_from_kappa1_m_gev": MEFF_REQUIRED_FROM_K1,
        "required_meff_spread": required_meff_spread,
        "kappa10_reconstruction_relerr": k10_reconstruction_relerr,
    },
    "canonical_minimal_branch": {
        "physical_m_cap_gev": PHYSICAL_M_CAP_GEV,
        "kappa_max_at_bare_m100_under_cap": KAPPA_MAX_AT_M100_UNDER_PHYSICAL_CAP,
        "minimum_optimistic_floor_j": CANONICAL_MINIMAL_FLOOR_J,
        "minimum_optimistic_floor_gj": CANONICAL_MINIMAL_FLOOR_GJ,
        "floor_over_10mj": CANONICAL_FLOOR_OVER_10MJ,
        "kappa10_m100_physical_cap_ratio": K10_M100_PHYSICAL_CAP_RATIO,
        "required_10mj_physical_scale_ratio": REQUIRED_PHYSICAL_SCALE_RATIO,
        "strict_sub10mj_closed": minimal_canonical_ghost_sub10_closed,
    },
    "stretch_targets": {
        "required_m_eff_10mj_gev": MEFF_FOR_10MJ,
        "required_m_eff_1mj_gev": MEFF_FOR_1MJ,
        "required_m_eff_100kj_gev": MEFF_FOR_100KJ,
    },
    "provenance": {
        "n1_53mj_result_numerically_valid_under_declared_two_knob_parameterization": True,
        "n1_53mj_result_is_trusted_minimal_canonical_eft_near_miss": False,
        "v3_amplitude_identity_algebraically_valid": True,
        "v3_ghost_promotion_as_independent_kappa_physical_match": False,
        "kappa_independent_minimal_eft_parameter_certified": kappa_independent_minimal_eft_parameter_certified,
    },
    "nonredundant_charge_operator_frontier_open": nonredundant_charge_operator_frontier_open,
    "full_ghost_condensate_family_closed": full_ghost_condensate_family_closed,
    "certified_sub10mj_model_found": False,
    "decision": decision,
    "next": next_step,
}

OUT.parent.mkdir(parents=True,exist_ok=True)
OUT.write_text(
    json.dumps(result,indent=2,sort_keys=True)+"\n",
    encoding="utf-8",
)

print("=== 032V4 RESULT ===")
print("N1_E_KAPPA1_M100_GJ=" + format(E_K1_M100/1e9,".12e"))
print("N1_E_KAPPA10_M100_MJ=" + format(E_K10_M100/1e6,".12e"))
print("N1_ENERGY_RATIO_K1_OVER_K10=" + format(energy_ratio,".12e"))
print("EXPECTED_KAPPA_SQUARED_RATIO=" + format(expected_ratio,".12e"))
print("KAPPA_SCALING_RELERR=" + format(energy_scaling_relerr,".12e"))

print("M_EFF_K1_M100_GEV=" + format(MEFF_K1_M100,".12e"))
print("M_EFF_K10_M100_GEV=" + format(MEFF_K10_M100,".12e"))
print("M_EFF_REQUIRED_FROM_KAPPA_GEV=" + format(MEFF_REQUIRED_FROM_KAPPA,".12e"))
print("M_EFF_REQUIRED_FROM_K10_ROUTE_GEV=" + format(MEFF_REQUIRED_FROM_K10,".12e"))
print("M_EFF_REQUIRED_FROM_K1_ROUTE_GEV=" + format(MEFF_REQUIRED_FROM_K1,".12e"))
print("REQUIRED_M_EFF_ROUTE_SPREAD=" + format(required_meff_spread,".12e"))

print("CANONICAL_PHYSICAL_M_CAP_GEV=" + format(PHYSICAL_M_CAP_GEV,".12e"))
print("KAPPA_MAX_AT_BARE_M100_UNDER_CAP=" + format(KAPPA_MAX_AT_M100_UNDER_PHYSICAL_CAP,".12e"))
print("CANONICAL_MINIMAL_OPTIMISTIC_FLOOR_GJ=" + format(CANONICAL_MINIMAL_FLOOR_GJ,".12e"))
print("CANONICAL_FLOOR_OVER_10MJ=" + format(CANONICAL_FLOOR_OVER_10MJ,".12e"))

print("REQUIRED_M_EFF_10MJ_GEV=" + format(MEFF_FOR_10MJ,".12e"))
print("REQUIRED_M_EFF_1MJ_GEV=" + format(MEFF_FOR_1MJ,".12e"))
print("REQUIRED_M_EFF_100KJ_GEV=" + format(MEFF_FOR_100KJ,".12e"))

print("N1_53MJ_NUMERIC_TWO_KNOB_RESULT_VALID=True")
print("N1_53MJ_TRUSTED_MINIMAL_CANONICAL_EFT_NEAR_MISS=False")
print("KAPPA_INDEPENDENT_MINIMAL_EFT_PARAMETER_CERTIFIED=False")
print("MINIMAL_CANONICAL_GHOST_SUB10_CLOSED=" + str(minimal_canonical_ghost_sub10_closed))
print("NONREDUNDANT_GHOST_OPERATOR_FRONTIER_OPEN=" + str(nonredundant_charge_operator_frontier_open))
print("FULL_GHOST_CONDENSATE_FAMILY_CLOSED=False")
print("CERTIFIED_SUB10MJ_MODEL_FOUND=NO")
print("DECISION=" + decision)
print("NEXT=" + next_step)
