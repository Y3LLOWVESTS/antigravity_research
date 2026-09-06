"""
032B2 — finite-payload canonical kinetic-energy lower bound.

Scope
-----
Universal-metric canonical quadratic-twin pNGB family 032B.

Purpose
-------
Use the finite-payload center-of-mass requirement plus the 032B1
naturalness bound on the universal scalar coupling to derive an
unavoidable positive canonical scalar kinetic-energy floor inside
the payload volume itself.

No field equation is solved.
No source model is assumed.
No potential-energy credit is used.
No negative binding credit is used.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

from antigravity_research.agminer.policy import current_energy_policy


ROOT = Path(__file__).resolve().parents[1]

B1_PATH = (
    ROOT
    / "results"
    / "data"
    / "032b1_metric_twin_naturalness_charge_summary.json"
)

CONFIG_PATH = (
    ROOT
    / "config"
    / "agminer_032a.json"
)

OUTPUT_PATH = (
    ROOT
    / "results"
    / "data"
    / "032b2_finite_payload_kinetic_energy_bound_summary.json"
)

MPL_REDUCED_GEV = 2.435e18
HBARC_GEV_M = 1.973269804e-16
GEV_TO_J = 1.602176634e-10
C_LIGHT = 299792458.0


if not B1_PATH.exists():
    raise RuntimeError("032B1 result is required")

if not CONFIG_PATH.exists():
    raise RuntimeError("AGMINER config is required")

b1 = json.loads(B1_PATH.read_text(encoding="utf-8"))
config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
policy = current_energy_policy()

alpha_declared = float(
    b1["alpha_visible_naturalness_max"]
)

declared_cutoff_gev = float(
    b1["cutoff_gev"]
)

top_mass_gev = float(
    b1["top_mass_gev"]
)

payload_radius_m = float(
    config["payload_radius_m"]
)

target_cm_accel_mps2 = float(
    config["target_cm_accel_mps2"]
)

energy_limit_j = float(
    policy["limit_j"]
)

payload_volume_m3 = (
    4.0
    * math.pi
    * payload_radius_m ** 3
    / 3.0
)

# ------------------------------------------------------------
# Bound derivation.
#
# For one universal conformal metric:
#
#   a = -(c^2 alpha / Mpl) grad(phi).
#
# The homogeneous benchmark payload has:
#
#   a_CM = volume_average(a).
#
# If |alpha| <= alpha_max everywhere, Cauchy-Schwarz gives:
#
#   |a_CM|
#   <= c^2 alpha_max / Mpl
#      * sqrt(volume_average(|grad phi|^2)).
#
# Therefore:
#
#   integral_payload |grad phi|^2 dV
#   >= V [Mpl a_CM/(c^2 alpha_max)]^2.
#
# For a canonical scalar:
#
#   E_kin = 1/2 integral |grad phi|^2 dV.
#
# This is a lower bound on only one positive component of the
# complete energy ledger.
# ------------------------------------------------------------


def kinetic_floor_j(alpha_max: float) -> float:
    if alpha_max <= 0.0:
        raise ValueError("alpha_max must be positive")

    acceleration_gradient_m_inv = (
        target_cm_accel_mps2
        / C_LIGHT ** 2
    )

    grad_phi_gev2 = (
        MPL_REDUCED_GEV
        / alpha_max
        * acceleration_gradient_m_inv
        * HBARC_GEV_M
    )

    volume_gev_minus3 = (
        payload_volume_m3
        / HBARC_GEV_M ** 3
    )

    energy_gev = (
        0.5
        * volume_gev_minus3
        * grad_phi_gev2 ** 2
    )

    return energy_gev * GEV_TO_J



def kinetic_floor_j_direct(alpha_max: float) -> float:
    return (
        0.5
        * payload_volume_m3
        * (MPL_REDUCED_GEV / alpha_max) ** 2
        * (target_cm_accel_mps2 / C_LIGHT ** 2) ** 2
        * GEV_TO_J
        / HBARC_GEV_M
    )



declared_floor_j = kinetic_floor_j(
    alpha_declared
)

declared_floor_direct_j = kinetic_floor_j_direct(
    alpha_declared
)

independent_relerr = abs(
    declared_floor_j
    - declared_floor_direct_j
) / declared_floor_j

# ------------------------------------------------------------
# Extremely generous rescue test.
#
# B1 has alpha_max proportional to 1/Lambda.
# Lower Lambda from the declared 10 TeV all the way to the
# top-quark threshold. This is much more permissive than the
# declared family benchmark.
# ------------------------------------------------------------

alpha_top_threshold = (
    alpha_declared
    * declared_cutoff_gev
    / top_mass_gev
)

top_threshold_floor_j = kinetic_floor_j(
    alpha_top_threshold
)

# Coupling needed for the payload kinetic floor alone to equal
# the configured energy objective.

alpha_required = (
    alpha_declared
    * math.sqrt(
        declared_floor_j
        / energy_limit_j
    )
)

# Since alpha_max scales as 1/Lambda in the B1 loop formula,
# infer the cutoff that would be needed to reach this alpha.

required_cutoff_gev = (
    declared_cutoff_gev
    * alpha_declared
    / alpha_required
)

declared_energy_gap = (
    declared_floor_j
    / energy_limit_j
)

top_threshold_energy_gap = (
    top_threshold_floor_j
    / energy_limit_j
)

alpha_gap_declared = (
    alpha_required
    / alpha_declared
)

alpha_gap_top_threshold = (
    alpha_required
    / alpha_top_threshold
)

required_cutoff_below_top = (
    required_cutoff_gev
    < top_mass_gev
)

# Derivative-expansion diagnostic at the declared coupling.

grad_phi_declared_gev2 = (
    MPL_REDUCED_GEV
    / alpha_declared
    * (target_cm_accel_mps2 / C_LIGHT ** 2)
    * HBARC_GEV_M
)

gradient_energy_scale_gev = math.sqrt(
    grad_phi_declared_gev2
)

# 10 TeV is the most optimistic minimal pNGB scale used for this
# declared family comparison.

declared_f_gev = declared_cutoff_gev

derivative_expansion_ratio = (
    grad_phi_declared_gev2
    / declared_f_gev ** 2
)

declared_fails = (
    declared_floor_j
    >= energy_limit_j
)

top_threshold_fails = (
    top_threshold_floor_j
    >= energy_limit_j
)

canonical_family_closed = (
    declared_fails
    and top_threshold_fails
    and required_cutoff_below_top
    and independent_relerr < 1.0e-12
)

result = {
    "branch": "032B2",
    "claim_class": "ANALYTIC_FINITE_PAYLOAD_ENERGY_LOWER_BOUND",
    "scope": (
        "CANONICAL_UNIVERSAL_METRIC_QUADRATIC_TWIN_PNGB_032B"
    ),
    "energy_policy_id": str(policy["policy_id"]),
    "energy_limit_j": energy_limit_j,
    "energy_comparison": str(policy["comparison"]),
    "payload_radius_m": payload_radius_m,
    "payload_volume_m3": payload_volume_m3,
    "target_cm_accel_mps2": target_cm_accel_mps2,
    "alpha_declared_10tev": alpha_declared,
    "declared_cutoff_gev": declared_cutoff_gev,
    "top_mass_gev": top_mass_gev,
    "alpha_top_threshold_generous": alpha_top_threshold,
    "alpha_required_for_energy_target": alpha_required,
    "alpha_gap_declared": alpha_gap_declared,
    "alpha_gap_top_threshold": alpha_gap_top_threshold,
    "declared_payload_kinetic_floor_j": declared_floor_j,
    "independent_payload_kinetic_floor_j": declared_floor_direct_j,
    "independent_reconstruction_relerr": independent_relerr,
    "declared_energy_gap_x": declared_energy_gap,
    "top_threshold_payload_kinetic_floor_j": top_threshold_floor_j,
    "top_threshold_energy_gap_x": top_threshold_energy_gap,
    "required_cutoff_gev_to_hit_energy_target": required_cutoff_gev,
    "required_cutoff_below_top_threshold": required_cutoff_below_top,
    "gradient_energy_scale_gev": gradient_energy_scale_gev,
    "derivative_expansion_ratio_gradphi_over_f2": derivative_expansion_ratio,
    "potential_energy_included": False,
    "source_energy_included": False,
    "twin_energy_included": False,
    "activation_energy_included": False,
    "support_control_energy_included": False,
    "negative_binding_credit_used": False,
    "surface_acceleration_gate_used": False,
    "cm_gate_alone_sufficient_for_bound": True,
    "field_solver_used": False,
    "canonical_032b_family_closed": canonical_family_closed,
    "noncanonical_protected_families_closed": False,
}

if canonical_family_closed:
    classification = (
        "RED_CANONICAL_032B_FINITE_PAYLOAD_KINETIC_ENERGY_NO_GO"
    )
    next_step = (
        "032C_RERANK_GENUINELY_NONCANONICAL_OR_DIFFERENT_PROTECTED_FAMILIES"
    )
else:
    classification = (
        "UNRESOLVED_CANONICAL_032B"
    )
    next_step = (
        "REPAIR_OR_TIGHTEN_032B2_BOUND"
    )

result["classification"] = classification
result["next"] = next_step

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

print("=== 032B2 FINITE-PAYLOAD KINETIC ENERGY BOUND ===")
print("CLAIM_CLASS=ANALYTIC_FINITE_PAYLOAD_ENERGY_LOWER_BOUND")
print("FIELD_SOLVER_USED=NO")
print("PAYLOAD_RADIUS_M=" + format(payload_radius_m, ".12e"))
print("PAYLOAD_VOLUME_M3=" + format(payload_volume_m3, ".12e"))
print("TARGET_CM_ACCEL_MPS2=" + format(target_cm_accel_mps2, ".12e"))
print("ENERGY_LIMIT_J=" + format(energy_limit_j, ".12e"))
print("ALPHA_DECLARED_10TEV=" + format(alpha_declared, ".12e"))
print("DECLARED_PAYLOAD_KINETIC_FLOOR_J=" + format(declared_floor_j, ".12e"))
print("DECLARED_ENERGY_GAP_X=" + format(declared_energy_gap, ".12e"))
print("INDEPENDENT_RECONSTRUCTION_RELERR=" + format(independent_relerr, ".12e"))
print("ALPHA_TOP_THRESHOLD_GENEROUS=" + format(alpha_top_threshold, ".12e"))
print("TOP_THRESHOLD_KINETIC_FLOOR_J=" + format(top_threshold_floor_j, ".12e"))
print("TOP_THRESHOLD_ENERGY_GAP_X=" + format(top_threshold_energy_gap, ".12e"))
print("ALPHA_REQUIRED_FOR_10MJ=" + format(alpha_required, ".12e"))
print("ALPHA_GAP_DECLARED_X=" + format(alpha_gap_declared, ".12e"))
print("ALPHA_GAP_TOP_THRESHOLD_X=" + format(alpha_gap_top_threshold, ".12e"))
print("REQUIRED_CUTOFF_GEV=" + format(required_cutoff_gev, ".12e"))
print("REQUIRED_CUTOFF_BELOW_TOP_THRESHOLD=" + str(required_cutoff_below_top))
print("GRADIENT_ENERGY_SCALE_GEV=" + format(gradient_energy_scale_gev, ".12e"))
print("DERIVATIVE_EXPANSION_RATIO=" + format(derivative_expansion_ratio, ".12e"))
print("SOURCE_ENERGY_COUNTED=NO")
print("POTENTIAL_ENERGY_COUNTED=NO")
print("TWIN_ENERGY_COUNTED=NO")
print("CM_GATE_ALONE_SUFFICIENT=YES")
print("CLASSIFICATION=" + classification)
print("CANONICAL_032B_FAMILY_CLOSED=" + str(canonical_family_closed))
print("NONCANONICAL_PROTECTED_FAMILIES_CLOSED=False")
print("NEXT=" + next_step)
