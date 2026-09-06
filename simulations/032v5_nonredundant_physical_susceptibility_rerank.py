"""
032V5 — canonical re-anchor and nonredundant susceptibility theorem.

V4 established that the old N1 kappa lever was normalization-redundant.

Therefore the trusted physical optimistic reference is no longer
53.2404669 MJ. It is the canonical minimal ghost floor:

    E_ref = 5.324046687 GJ.

This run asks what a genuinely nonredundant healthy action must do in
order to lower that physical scale into:

    <10 MJ      strict project objective
    <1 MJ       stretch objective
    <100 kJ     field-level headroom objective.

For a positive quadratic response sector:

    E = 1/2 x^T H x
    A = k^T x

the optimum susceptibility is:

    Lambda = k^T H^-1 k.

For positive H:

    Lambda <= ||k||^2 / lambda_min(H).

This creates a model-independent tradeoff between:

    canonical coupling strength,
    kinetic softness,
    and number of coherently participating channels.

The result is a design theorem, not a physical antigravity model.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

OUT = ROOT / "results" / "data" / "032v5_nonredundant_physical_susceptibility_summary.json"
CSV_OUT = ROOT / "results" / "data" / "032v5_nonredundant_leverage_requirements.csv"

V2 = ROOT / "results" / "data" / "032v2_feasibility_first_action_response_summary.json"
V4 = ROOT / "results" / "data" / "032v4_ghost_condensate_effective_charge_normalization_summary.json"

STRICT_TARGET_J = 1.0e7
STRETCH_TARGET_J = 1.0e6
HEADROOM_TARGET_J = 1.0e5


for path in (V2, V4):
    if not path.exists():
        raise FileNotFoundError(str(path))

v2 = json.loads(V2.read_text(encoding="utf-8"))
v4 = json.loads(V4.read_text(encoding="utf-8"))


# ============================================================
# 1. PROVENANCE HANDOFF
# ============================================================

assert v4["decision"] == "RED_MINIMAL_GHOST_KAPPA_LEVER_NORMALIZATION_REDUNDANT"
assert v4["canonical_minimal_branch"]["strict_sub10mj_closed"] is True
assert v4["provenance"]["n1_53mj_result_is_trusted_minimal_canonical_eft_near_miss"] is False

CANONICAL_REF_J = float(
    v4["canonical_minimal_branch"]["minimum_optimistic_floor_j"]
)

OLD_V2_REF_J = float(
    v2["reference_control"]["energy_j"]
)

REANCHOR_FACTOR = CANONICAL_REF_J / OLD_V2_REF_J

assert abs(REANCHOR_FACTOR - 100.0) < 1.0e-10

# V2 mathematical response ratios remain valid.
# Its absolute energy labels must be multiplied by the physical re-anchor.

V2_LEAST_OLD_J = float(
    v2["least_deformed_target"]["reference_equivalent_energy_j"]
)

V2_LEAST_REANCHORED_J = V2_LEAST_OLD_J * REANCHOR_FACTOR


# ============================================================
# 2. EXACT PHYSICAL RESPONSE REQUIREMENTS
# ============================================================

target_specs = [
    ("STRICT_10MJ", STRICT_TARGET_J),
    ("STRETCH_1MJ", STRETCH_TARGET_J),
    ("HEADROOM_100KJ", HEADROOM_TARGET_J),
]

requirements = []

for name, target_j in target_specs:
    lam = CANONICAL_REF_J / target_j
    amp = math.sqrt(lam)

    requirements.append({
        "target": name,
        "target_j": target_j,
        "required_susceptibility": lam,
        "required_amplitude_gain": amp,
    })


# ============================================================
# 3. RECONSTRUCT THE DECLARED V2 ROBUST BOX
# ============================================================

search = v2["search"]
box = search["parameter_box"]

GMAX = float(box["g1_g2"][1])
EIGMIN_FLOOR = float(search["kinetic_min_eigenvalue_requirement"])
COND_MAX = float(search["kinetic_condition_number_max"])
N_V2 = 2

PARTICIPATION_MAX = float(box["productive_participation"][1])
CANCELLATION_MIN = float(box["cancellation_tax"][0])
SCAFFOLD_MIN = float(box["scaffold_tax"][0])

TAX_MIN = (
    CANCELLATION_MIN
    * SCAFFOLD_MIN
    / PARTICIPATION_MAX
)

assert abs(GMAX - 3.0) < 1.0e-12
assert abs(EIGMIN_FLOOR - 0.4) < 1.0e-12
assert abs(TAX_MIN - 1.0) < 1.0e-12

# Rayleigh bound:
# Lambda <= ||k||^2 / lambda_min.

K_NORM2_MAX = N_V2 * GMAX**2
V2_LAMBDA_MAX_BOUND = K_NORM2_MAX / EIGMIN_FLOOR

# This bound is actually attained within the original V2 parameter box.
# Choose:
#
# H = [[0.8,-0.4],[-0.4,0.8]]
# k = [3,3].
#
# Eigenvalues are 0.4 and 1.2, condition number 3.

H = np.array([
    [0.8, -0.4],
    [-0.4, 0.8],
], dtype=float)

k = np.array([3.0, 3.0], dtype=float)

eigs = np.linalg.eigvalsh(H)
WITNESS_EIGMIN = float(eigs[0])
WITNESS_EIGMAX = float(eigs[-1])
WITNESS_COND = WITNESS_EIGMAX / WITNESS_EIGMIN

WITNESS_LAMBDA = float(k @ np.linalg.solve(H, k))

assert abs(WITNESS_EIGMIN - 0.4) < 1.0e-12
assert WITNESS_COND <= COND_MAX
assert abs(WITNESS_LAMBDA - V2_LAMBDA_MAX_BOUND) < 1.0e-12

V2_CANONICAL_MIN_J = (
    CANONICAL_REF_J
    * TAX_MIN
    / V2_LAMBDA_MAX_BOUND
)

V2_CANONICAL_MIN_MJ = V2_CANONICAL_MIN_J / 1.0e6

V2_REANCHORED_SUB10_POSSIBLE = V2_CANONICAL_MIN_J < STRICT_TARGET_J
V2_REANCHORED_NEAR100_POSSIBLE = V2_CANONICAL_MIN_J < 1.0e8
V2_REANCHORED_MECHANISM1GJ_POSSIBLE = V2_CANONICAL_MIN_J <= 1.0e9

assert V2_REANCHORED_SUB10_POSSIBLE is False
assert V2_REANCHORED_NEAR100_POSSIBLE is False
assert V2_REANCHORED_MECHANISM1GJ_POSSIBLE is True


# ============================================================
# 4. THREE NONREDUNDANT ROUTES
# ============================================================

# Route A:
# Keep two channels and the robust eigenvalue floor.
# How large must equal per-channel canonical couplings become?

# Lambda <= (2 g^2)/eigmin.

# Route B:
# Keep the old maximum coupling norm.
# How soft must the kinetic eigenmode become?

# Route C:
# Keep O(1) per-channel coupling and robust eigmin.
# How many fully coherent channels are mathematically necessary?

route_rows = []

for spec in requirements:
    lam = float(spec["required_susceptibility"])

    equal_g_required = math.sqrt(
        lam * EIGMIN_FLOOR / N_V2
    )

    eigmin_required_at_old_k = K_NORM2_MAX / lam

    # Original V2 diagonal entries were >=0.5, so any such 2x2 matrix
    # has lambda_max(H)>=0.5. This gives an optimistic condition-number
    # lower bound if the soft-mode route is used.
    condition_lower_bound = 0.5 / eigmin_required_at_old_k

    min_coherent_channels = math.ceil(
        lam * EIGMIN_FLOOR / (GMAX**2)
    )

    route_rows.append({
        "target": spec["target"],
        "target_j": spec["target_j"],
        "required_susceptibility": lam,
        "required_amplitude_gain": spec["required_amplitude_gain"],
        "two_channel_equal_g_required": equal_g_required,
        "g_required_over_old_gmax": equal_g_required/GMAX,
        "eigmin_required_at_old_k_norm": eigmin_required_at_old_k,
        "soft_mode_condition_number_lower_bound": condition_lower_bound,
        "minimum_coherent_channels_g3_eigmin0p4": min_coherent_channels,
    })


# ============================================================
# 5. PHYSICAL INTERPRETATION / RERANK
# ============================================================

# These are mechanism classes, not physical models.

lever_rerank = [
    {
        "priority": 1,
        "lever": "SYMMETRY_PROTECTED_COHERENT_MULTI_CHANNEL",
        "mathematical_status": "CAN_REACH_REQUIRED_LAMBDA_WITHOUT_SOFT_KINETIC_MODE",
        "physical_status": "NEW_ACTION_AND_COMPLETE_SOURCE_SCALING_REQUIRED",
        "project_warning": "DO_NOT_REOPEN_032E_032G_032H_SOURCE_LEDGER_FAILURES",
        "key_test": "DOES_USEFUL_RESPONSE_SCALE_FASTER_THAN_COMPLETE_SOURCE_PLUS_SCAFFOLD_ENERGY",
    },
    {
        "priority": 2,
        "lever": "EXPLICIT_NONREDUNDANT_HIGHER_DERIVATIVE_OR_KINETIC_OPERATOR",
        "mathematical_status": "POSSIBLE_NEW_SUSCEPTIBILITY_STRUCTURE",
        "physical_status": "STATIC_OPPOSITE_SIGN_CHARGE_PER_JOULE_NOT_YET_DERIVED",
        "project_warning": "NORMALIZATION_OR_FIELD_REDEFINITION_REDUNDANCY_MUST_BE_TESTED_FIRST",
        "key_test": "CANONICAL_HAMILTONIAN_SCHUR_COMPLEMENT_AND_STATIC_METRIC_RESPONSE",
    },
    {
        "priority": 3,
        "lever": "LARGE_CANONICAL_COUPLING_NORM",
        "mathematical_status": "SUFFICIENT_IF_GENUINELY_INDEPENDENT",
        "physical_status": "EMPIRICAL_AND_RADIATIVE_RISK",
        "project_warning": "UNIVERSAL_FIFTH_FORCE_EP_AND_LOOP_CONSTRAINTS",
        "key_test": "CAN_LARGE_COUPLING_BE_SYMMETRY_PROTECTED_AND_METRIC_UNIVERSAL",
    },
    {
        "priority": 4,
        "lever": "SOFT_NEAR_CRITICAL_KINETIC_MODE",
        "mathematical_status": "CAN_ENHANCE_SUSCEPTIBILITY",
        "physical_status": "HIGH_STRONG_COUPLING_AND_STABILITY_RISK",
        "project_warning": "BOUNDARY_OPTIMA_AND_SMALL_EIGENVALUES_ARE_HIGH_RISK",
        "key_test": "CUTOFF_STAYS_ABOVE_OPERATING_MOMENTA_AND_NONLINEAR_STABILITY_SURVIVES",
    },
    {
        "priority": 5,
        "lever": "GEOMETRY_OR_MORPHOLOGY_ONLY",
        "mathematical_status": "INSUFFICIENT_IN_DECLARED_GHOST_BRANCH",
        "physical_status": "CLOSED_BY_032N1_FOR_DECLARED_LINEAR_BRANCH",
        "project_warning": "DO_NOT_REOPEN_WITH_MORE_RANDOM_GEOMETRY",
        "key_test": "NONE_UNLESS_THE_ACTION_CHANGES",
    },
]


# ============================================================
# 6. WRITE CSV
# ============================================================

CSV_OUT.parent.mkdir(parents=True, exist_ok=True)

with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=list(route_rows[0].keys()),
    )
    writer.writeheader()
    writer.writerows(route_rows)


# ============================================================
# 7. DECISION
# ============================================================

decision = "RED_OLD_O1_TWO_CHANNEL_SUB10_AFTER_CANONICAL_REANCHOR"
next_step = "032V6_EXPLICIT_NONREDUNDANT_ACTION_FAMILY_PREFLIGHT"

result = {
    "branch": "032V5_NONREDUNDANT_PHYSICAL_SUSCEPTIBILITY_RERANK",
    "claim_class": "CANONICAL_RESPONSE_BOUND_AND_MECHANISM_RERANK",
    "strict_target_j": STRICT_TARGET_J,
    "stretch_target_j": STRETCH_TARGET_J,
    "headroom_target_j": HEADROOM_TARGET_J,
    "strict_policy_changed": False,
    "provenance": {
        "canonical_reference_j": CANONICAL_REF_J,
        "old_v2_reference_j": OLD_V2_REF_J,
        "reanchor_factor": REANCHOR_FACTOR,
        "v2_response_geometry_still_mathematically_valid": True,
        "v2_old_absolute_sub10_energy_labels_physically_current": False,
        "v2_least_old_j": V2_LEAST_OLD_J,
        "v2_least_reanchored_j": V2_LEAST_REANCHORED_J,
    },
    "required_nonredundant_leverage": requirements,
    "old_v2_robust_box": {
        "channels": N_V2,
        "gmax": GMAX,
        "kinetic_eigmin_floor": EIGMIN_FLOOR,
        "condition_number_max": COND_MAX,
        "minimum_total_tax": TAX_MIN,
        "max_k_norm_squared": K_NORM2_MAX,
        "exact_max_susceptibility": V2_LAMBDA_MAX_BOUND,
        "witness_h": H.tolist(),
        "witness_k": k.tolist(),
        "witness_eigmin": WITNESS_EIGMIN,
        "witness_condition_number": WITNESS_COND,
        "witness_susceptibility": WITNESS_LAMBDA,
        "canonical_minimum_energy_j": V2_CANONICAL_MIN_J,
        "canonical_minimum_energy_mj": V2_CANONICAL_MIN_MJ,
        "sub10_possible": V2_REANCHORED_SUB10_POSSIBLE,
        "10_to_100mj_possible": V2_REANCHORED_NEAR100_POSSIBLE,
        "100mj_to_1gj_possible": V2_REANCHORED_MECHANISM1GJ_POSSIBLE,
    },
    "lever_routes": route_rows,
    "mechanism_rerank": lever_rerank,
    "claim_discipline": {
        "physical_model_found": False,
        "sub10_model_found": False,
        "one_mj_model_found": False,
        "multi_channel_bound_is_complete_source_ledger": False,
        "soft_mode_is_automatically_healthy": False,
        "large_coupling_is_automatically_empirically_allowed": False,
        "old_closed_multiscalar_families_reopened": False,
    },
    "certified_sub10mj_model_found": False,
    "decision": decision,
    "next": next_step,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

print("=== 032V5 RESULT ===")
print("CANONICAL_REFERENCE_GJ=" + format(CANONICAL_REF_J/1e9, ".12e"))
print("OLD_V2_REFERENCE_MJ=" + format(OLD_V2_REF_J/1e6, ".12e"))
print("REANCHOR_FACTOR=" + format(REANCHOR_FACTOR, ".12e"))
print("V2_LEAST_OLD_MJ=" + format(V2_LEAST_OLD_J/1e6, ".12e"))
print("V2_LEAST_REANCHORED_MJ=" + format(V2_LEAST_REANCHORED_J/1e6, ".12e"))

for row in requirements:
    print(
        row["target"]
        + "_LAMBDA_REQUIRED="
        + format(row["required_susceptibility"], ".12e")
    )
    print(
        row["target"]
        + "_AMPLITUDE_REQUIRED="
        + format(row["required_amplitude_gain"], ".12e")
    )

print("V2_BOX_EXACT_LAMBDA_MAX=" + format(V2_LAMBDA_MAX_BOUND, ".12e"))
print("V2_BOX_WITNESS_EIGMIN=" + format(WITNESS_EIGMIN, ".12e"))
print("V2_BOX_WITNESS_CONDITION=" + format(WITNESS_COND, ".12e"))
print("V2_BOX_CANONICAL_MIN_MJ=" + format(V2_CANONICAL_MIN_MJ, ".12e"))
print("V2_BOX_SUB10_POSSIBLE=" + str(V2_REANCHORED_SUB10_POSSIBLE))
print("V2_BOX_10_TO_100MJ_POSSIBLE=" + str(V2_REANCHORED_NEAR100_POSSIBLE))
print("V2_BOX_100MJ_TO_1GJ_POSSIBLE=" + str(V2_REANCHORED_MECHANISM1GJ_POSSIBLE))

for row in route_rows:
    prefix = row["target"]
    print(prefix + "_TWO_CHANNEL_EQUAL_G_REQUIRED=" + format(row["two_channel_equal_g_required"], ".12e"))
    print(prefix + "_SOFT_EIGMIN_REQUIRED=" + format(row["eigmin_required_at_old_k_norm"], ".12e"))
    print(prefix + "_SOFT_CONDITION_LOWER_BOUND=" + format(row["soft_mode_condition_number_lower_bound"], ".12e"))
    print(prefix + "_MIN_COHERENT_CHANNELS=" + str(row["minimum_coherent_channels_g3_eigmin0p4"]))

print("OLD_V2_SUB10_ENERGY_LABELS=CLOSED_BY_CANONICAL_REANCHOR")
print("PHYSICAL_MODEL_FOUND=NO")
print("CERTIFIED_SUB10MJ_MODEL_FOUND=NO")
print("DECISION=" + decision)
print("NEXT=" + next_step)
