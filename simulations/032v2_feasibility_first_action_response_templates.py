"""
032V2 — feasibility-first action-response templates.

This is NOT an arbitrary law-of-physics generator.

It asks a narrower mathematical question:

    Given a healthy positive quadratic response sector,
    how much finite-payload susceptibility is required to move a
    verified 53.24-MJ learning control into the <10-MJ region?

Reduced template:

    E_field = 1/2 x^T H x
    A_useful = k^T x

with H positive definite.

For a required response A0, minimization gives

    E_min = A0^2 / (2 k^T H^-1 k).

Therefore the useful susceptibility is

    Lambda = k^T H^-1 k.

We normalize Lambda=1 to the verified 032N1 learning control.

Additional physically conservative taxes are represented separately:

    scaffold >= 1
    cancellation >= 1
    productive_participation <= 1.

The translated learning energy is

    E_equiv = E_032N1
              * scaffold
              * cancellation
              / (participation * Lambda).

IMPORTANT:

    E_equiv is a design-target translation, NOT a complete operating
    energy prediction for a new theory.

Every surviving template must later be matched to an explicit local
action, symmetry protection, microscopic source, physical metric,
naturalness calculation and EFT before becoming an AGMINER family.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy.stats import qmc


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "data" / "032v2_feasibility_first_action_response_summary.json"
CSV_OUT = ROOT / "results" / "data" / "032v2_action_response_template_targets.csv"
N1 = ROOT / "results" / "data" / "032n1_ghost_condensate_halfspace_continuum_bound_summary.json"
V1 = ROOT / "results" / "data" / "032v1_trusted_learning_corridor_summary.json"

TARGET_J = 1.0e7
NEAR_CEILING_J = 1.0e8
MECHANISM_CEILING_J = 1.0e9
SAMPLES = 2**20
SEED = 32052


if not N1.exists():
    raise FileNotFoundError(str(N1))

if not V1.exists():
    raise FileNotFoundError(str(V1))

n1 = json.loads(N1.read_text(encoding="utf-8"))
v1 = json.loads(V1.read_text(encoding="utf-8"))

assert v1["database_corridor"]["trusted_active_rows"] == 0
assert v1["certified_sub10mj_model_found"] is False

REF_J = float(n1["global_halfspace_floor_kappa10_j"])
REF_FACTOR = REF_J / TARGET_J

assert 5.32 < REF_FACTOR < 5.33


# ------------------------------------------------------------
# 1. Exact one-channel design requirements.
# ------------------------------------------------------------

tax_cases = [1.0, 2.0, 5.0, 10.0]
requirements = []

for tax in tax_cases:
    lambda_needed = REF_FACTOR * tax
    amplitude_gain = math.sqrt(lambda_needed)

    requirements.append(
        {
            "total_tax": tax,
            "required_susceptibility_gain": lambda_needed,
            "required_amplitude_response_gain": amplitude_gain,
        }
    )


# ------------------------------------------------------------
# 2. Sobol search over a healthy two-channel reduced sector.
# ------------------------------------------------------------

# H = [[z1,b],[b,z2]], with b=rho*sqrt(z1*z2).
# Positive definiteness is explicit.
# k=(g1,g2) is the reduced finite-payload response vector.

sampler = qmc.Sobol(d=8, scramble=True, seed=SEED)
u = sampler.random_base2(m=20)

# O(1) parameter box only.
z1 = 10.0 ** (
    math.log10(0.5)
    + u[:,0] * (math.log10(2.0)-math.log10(0.5))
)
z2 = 10.0 ** (
    math.log10(0.5)
    + u[:,1] * (math.log10(2.0)-math.log10(0.5))
)

g1 = 0.5 + 2.5*u[:,2]
g2 = 0.5 + 2.5*u[:,3]

rho = -0.5 + u[:,4]

participation = 0.5 + 0.5*u[:,5]
cancellation = 1.0 + u[:,6]
scaffold = 10.0 ** (math.log10(1.0) + u[:,7]*math.log10(5.0))

b = rho*np.sqrt(z1*z2)
det = z1*z2 - b*b

disc = np.sqrt((z1-z2)**2 + 4.0*b*b)
eig_min = 0.5*(z1+z2-disc)
eig_max = 0.5*(z1+z2+disc)
condition = eig_max/eig_min

Lambda = (
    g1*g1*z2
    - 2.0*g1*g2*b
    + g2*g2*z1
) / det

tax = scaffold*cancellation/participation

E_equiv = REF_J * tax/Lambda

# Robustness gate deliberately stays away from a singular kinetic matrix.
robust = (
    (det > 0.0)
    & (eig_min >= 0.40)
    & (condition <= 5.0)
    & (Lambda > 0.0)
)

target = robust & (E_equiv < TARGET_J)
near = robust & (E_equiv >= TARGET_J) & (E_equiv < NEAR_CEILING_J)
mechanism = robust & (E_equiv >= NEAR_CEILING_J) & (E_equiv <= MECHANISM_CEILING_J)

# A distance-from-baseline measure. Lower means less deformation from
# z1=z2=g1=g2=1, rho=0, participation=1, cancellation=scaffold=1.
complexity = (
    np.log(z1)**2
    + np.log(z2)**2
    + np.log(g1)**2
    + np.log(g2)**2
    + rho*rho
    + np.log(1.0/participation)**2
    + np.log(cancellation)**2
    + np.log(scaffold)**2
)


def count(mask):
    return int(np.count_nonzero(mask))


def row_at(i):
    if E_equiv[i] < TARGET_J:
        band = "TARGET_LT_10MJ"
    elif E_equiv[i] < NEAR_CEILING_J:
        band = "NEAR_MISS_10_TO_100MJ"
    elif E_equiv[i] <= MECHANISM_CEILING_J:
        band = "MECHANISM_100MJ_TO_1GJ"
    else:
        band = "ARCHIVE_GT_1GJ"

    return {
        "index": int(i),
        "reference_equivalent_energy_j": float(E_equiv[i]),
        "reference_equivalent_energy_mj": float(E_equiv[i]/1.0e6),
        "band": band,
        "susceptibility_gain": float(Lambda[i]),
        "amplitude_response_gain": float(math.sqrt(Lambda[i])),
        "z1": float(z1[i]),
        "z2": float(z2[i]),
        "g1": float(g1[i]),
        "g2": float(g2[i]),
        "rho": float(rho[i]),
        "productive_participation": float(participation[i]),
        "cancellation_tax": float(cancellation[i]),
        "scaffold_tax": float(scaffold[i]),
        "total_tax": float(tax[i]),
        "kinetic_min_eigenvalue": float(eig_min[i]),
        "kinetic_condition_number": float(condition[i]),
        "distance_from_unit_template": float(complexity[i]),
        "positive_hamiltonian": True,
        "physical_model": False,
        "complete_energy_prediction": False,
        "certification_eligible": False,
    }


# ------------------------------------------------------------
# 3. Extract robust target templates.
# ------------------------------------------------------------

target_idx = np.flatnonzero(target)
near_idx = np.flatnonzero(near)
mechanism_idx = np.flatnonzero(mechanism)

# Least-deformed sub-10 design target.
if target_idx.size:
    least_target_idx = int(
        target_idx[np.argmin(complexity[target_idx])]
    )
    best_energy_idx = int(
        target_idx[np.argmin(E_equiv[target_idx])]
    )
else:
    least_target_idx = None
    best_energy_idx = None

# Keep a diverse compact target packet:
# 100 least-deformed target templates,
# 50 lowest-energy target templates,
# 50 closest near misses.
selected = []

if target_idx.size:
    a = target_idx[np.argsort(complexity[target_idx])[:100]]
    bidx = target_idx[np.argsort(E_equiv[target_idx])[:50]]
    selected.extend(int(x) for x in a)
    selected.extend(int(x) for x in bidx)

if near_idx.size:
    cidx = near_idx[np.argsort(E_equiv[near_idx])[:50]]
    selected.extend(int(x) for x in cidx)

selected = list(dict.fromkeys(selected))
selected_rows = [row_at(i) for i in selected]

CSV_OUT.parent.mkdir(parents=True, exist_ok=True)

if selected_rows:
    with CSV_OUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(selected_rows[0].keys()),
        )
        writer.writeheader()
        writer.writerows(selected_rows)
else:
    CSV_OUT.write_text("index\n", encoding="utf-8")

# ------------------------------------------------------------
# 4. Interpretation.
# ------------------------------------------------------------

least_target = (
    row_at(least_target_idx)
    if least_target_idx is not None
    else None
)

best_energy = (
    row_at(best_energy_idx)
    if best_energy_idx is not None
    else None
)

# Project mechanism knowledge is preserved only as comparison.
# We do not multiply unrelated historical headrooms together.
conserved_dec_headroom_low = 12.8
conserved_dec_headroom_high = 17.9
raw_teacher_headroom = 17230.0
productive_participation_gap = 9.7

if target_idx.size:
    decision = "GREEN_ROBUST_SUB10MJ_ACTION_RESPONSE_TARGETS_EXIST"
    next_step = "032V3_MATCH_ROBUST_TARGETS_TO_EXPLICIT_SYMMETRY_PROTECTED_PHYSICAL_ACTIONS"
else:
    decision = "RED_NO_ROBUST_SUB10MJ_TARGET_IN_DECLARED_O1_TEMPLATE_BOX"
    next_step = "032V3_EXPAND_MECHANISM_BASIS_NOT_PARAMETER_MAGNITUDES"

result = {
    "branch": "032V2_FEASIBILITY_FIRST_ACTION_RESPONSE_TEMPLATES",
    "claim_class": "MATHEMATICAL_DESIGN_TARGET_GENERATOR_NOT_PHYSICAL_MODEL_SEARCH",
    "strict_target_j": TARGET_J,
    "strict_policy_changed": False,
    "reference_control": {
        "name": "032N1_GHOST_CONDENSATE_CONTINUUM_FLOOR",
        "energy_j": REF_J,
        "target_factor": REF_FACTOR,
        "declared_branch_reopened": False,
    },
    "exact_requirements": requirements,
    "template_action": {
        "energy": "E=1/2*x^T*H*x",
        "useful_response": "A=k^T*x",
        "minimum_energy_scaling": "E_min proportional to 1/(k^T H^-1 k)",
        "hamiltonian_positive_definite_required": True,
    },
    "search": {
        "samples": SAMPLES,
        "robust_count": count(robust),
        "target_lt10mj_count": count(target),
        "near_10_to_100mj_count": count(near),
        "mechanism_100mj_to_1gj_count": count(mechanism),
        "kinetic_min_eigenvalue_requirement": 0.40,
        "kinetic_condition_number_max": 5.0,
        "parameter_box": {
            "z1_z2": [0.5,2.0],
            "g1_g2": [0.5,3.0],
            "rho": [-0.5,0.5],
            "productive_participation": [0.5,1.0],
            "cancellation_tax": [1.0,2.0],
            "scaffold_tax": [1.0,5.0],
        },
    },
    "least_deformed_target": least_target,
    "lowest_reference_equivalent_energy_target": best_energy,
    "historical_comparison_only": {
        "conserved_dec_headroom_range": [
            conserved_dec_headroom_low,
            conserved_dec_headroom_high,
        ],
        "raw_teacher_headroom": raw_teacher_headroom,
        "productive_participation_gap": productive_participation_gap,
        "cross_theory_headrooms_multiplied": False,
    },
    "claim_discipline": {
        "templates_are_physical_models": False,
        "reference_equivalent_energy_is_complete_operating_energy": False,
        "templates_inserted_into_agminer_database": False,
        "sub10_template_is_certified_antigravity": False,
        "explicit_physical_action_match_required_next": True,
        "microscopic_source_required_next": True,
        "naturalness_required_next": True,
        "eft_required_next": True,
        "universal_physical_metric_required_next": True,
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

print("=== 032V2 RESULT ===")
print("REFERENCE_032N1_J=" + format(REF_J, ".12e"))
print("REFERENCE_OVER_TARGET=" + format(REF_FACTOR, ".12e"))

for r in requirements:
    print(
        "TAX_" + format(r["total_tax"], ".0f")
        + "_REQUIRED_SUSCEPTIBILITY="
        + format(r["required_susceptibility_gain"], ".12e")
    )
    print(
        "TAX_" + format(r["total_tax"], ".0f")
        + "_REQUIRED_AMPLITUDE_GAIN="
        + format(r["required_amplitude_response_gain"], ".12e")
    )

print("SAMPLES=" + str(SAMPLES))
print("ROBUST_POSITIVE_HAMILTONIAN_COUNT=" + str(count(robust)))
print("ROBUST_SUB10_TARGET_COUNT=" + str(count(target)))
print("ROBUST_10_TO_100MJ_COUNT=" + str(count(near)))
print("ROBUST_100MJ_TO_1GJ_COUNT=" + str(count(mechanism)))

if least_target is not None:
    print("LEAST_DEFORMED_TARGET_EQUIV_MJ=" + format(least_target["reference_equivalent_energy_mj"], ".12e"))
    print("LEAST_DEFORMED_TARGET_LAMBDA=" + format(least_target["susceptibility_gain"], ".12e"))
    print("LEAST_DEFORMED_TARGET_AMPLITUDE_GAIN=" + format(least_target["amplitude_response_gain"], ".12e"))
    print("LEAST_DEFORMED_TARGET_TOTAL_TAX=" + format(least_target["total_tax"], ".12e"))
    print("LEAST_DEFORMED_TARGET_EIGMIN=" + format(least_target["kinetic_min_eigenvalue"], ".12e"))
    print("LEAST_DEFORMED_TARGET_CONDITION=" + format(least_target["kinetic_condition_number"], ".12e"))
else:
    print("LEAST_DEFORMED_TARGET=NONE")

print("TEMPLATES_ARE_PHYSICAL_MODELS=False")
print("AGMINER_DB_INSERTIONS=0")
print("CROSS_THEORY_HEADROOM_MULTIPLICATION=NO")
print("CERTIFIED_SUB10MJ_MODEL_FOUND=NO")
print("DECISION=" + decision)
print("NEXT=" + next_step)
