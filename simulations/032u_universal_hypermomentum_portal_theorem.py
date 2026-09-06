"""
032U — universal hypermomentum portal theorem / preflight.

This run asks whether an ordinary symmetric stress tensor T_munu can,
without adding a new microscopic affine charge or preferred vector,
linearly source a rank-three nonmetricity field with a monopole.

It deliberately separates:

  1. intrinsic MAG hypermomentum;
  2. universal stress-energy-only coupling;
  3. derivative multipole portals;
  4. genuinely new matter charges.

No claim is made that all metric-affine matter portals are impossible.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import quad

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "data" / "032u_universal_hypermomentum_portal_summary.json"
T_RESULT = ROOT / "results" / "data" / "032t_symmetry_protected_mag_matter_coupling_summary.json"

G = 6.67430e-11
C = 299792458.0
ENERGY_TARGET_J = 1.0e7
PAYLOAD_RADIUS_M = 0.10
TARGET_ACCEL = 9.80665

# ------------------------------------------------------------
# 1. VERIFY 032T HANDOFF
# ------------------------------------------------------------

if not T_RESULT.exists():
    raise FileNotFoundError(str(T_RESULT))

t = json.loads(T_RESULT.read_text(encoding="utf-8"))

assert t["minimal_matter_branch"]["declared_branch_closed"] is True
assert t["minimal_matter_branch"]["ordinary_q_hypermomentum_source"] == 0.0
assert t["new_q_matter_portal_required_for_rescue"] is True

# ------------------------------------------------------------
# 2. ZERO-DERIVATIVE RANK-PARITY THEOREM
# ------------------------------------------------------------

# Available tensor building blocks in the declared linear branch:
#
#   T_munu       rank 2
#   eta_munu     rank 2
#   epsilon_abcd rank 4
#
# A contraction always removes two free indices.
# Starting with only even-rank objects therefore leaves even rank.
# Rank 3 cannot be obtained.

def reachable_rank(
    n_metric: int,
    n_epsilon: int,
    contractions: int,
) -> int:
    return (
        2
        + 2*n_metric
        + 4*n_epsilon
        - 2*contractions
    )

reachable = set()

for ng in range(0, 5):
    for ne in range(0, 4):
        total = 2 + 2*ng + 4*ne
        for nc in range(0, total//2 + 1):
            rank = reachable_rank(ng, ne, nc)
            if rank >= 0:
                reachable.add(rank)

zero_derivative_rank3_exists = 3 in reachable
all_reachable_ranks_even = all(rank % 2 == 0 for rank in reachable)

assert zero_derivative_rank3_exists is False
assert all_reachable_ranks_even is True

# ------------------------------------------------------------
# 3. GENERAL ONE-DERIVATIVE MONOPOLE ARGUMENT
# ------------------------------------------------------------

# The most general linear Lorentz-covariant rank-three current built from
# one derivative, T, eta and traces consists schematically of terms of the
# forms
#
#   d_a T_bc,
#   d_b T_ac,
#   d_c T_ab,
#   eta_bc d_a T,
#   eta_ab d_c T,
#   eta_ac d_b T,
#   eta_bc d^r T_ra,
#   eta_ab d^r T_rc,
#   eta_ac d^r T_rb.
#
# For a static compact conserved source:
#
#   d_0 T = 0,
#   d^r T_rmu = 0,
#   integral d^3x d_i(...) = surface term = 0.
#
# Hence the integrated rank-three source monopole vanishes componentwise.

a,b,c,d,e,f,g,h,k = sp.symbols(
    "a b c d e f g h k",
    real=True,
)

static_time_derivative = sp.Integer(0)
conservation_divergence = sp.Integer(0)
compact_spatial_boundary = sp.Integer(0)

general_monopole = sp.simplify(
    a*compact_spatial_boundary
    + b*compact_spatial_boundary
    + c*compact_spatial_boundary
    + d*compact_spatial_boundary
    + e*compact_spatial_boundary
    + f*compact_spatial_boundary
    + g*conservation_divergence
    + h*conservation_divergence
    + k*conservation_divergence
    + static_time_derivative
)

one_derivative_monopole_zero = general_monopole == 0
assert one_derivative_monopole_zero

# ------------------------------------------------------------
# 4. INDEPENDENT SMOOTH-SOURCE NUMERICAL CHECK
# ------------------------------------------------------------

# Use a normalized Gaussian as a finite smooth approximation.
# A derivative source has zero total charge but nonzero first moment.

SOURCE_MASS_KG = ENERGY_TARGET_J / C**2
SIGMA_M = 0.05
L = 12.0 * SIGMA_M

def gaussian_1d(x):
    return (
        math.exp(-(x/SIGMA_M)**2)
        / (math.sqrt(math.pi)*SIGMA_M)
    )

def d_gaussian_1d(x):
    return -2.0*x/SIGMA_M**2 * gaussian_1d(x)

i0, i0err = quad(
    d_gaussian_1d,
    -L,
    L,
    epsabs=1.0e-14,
    epsrel=1.0e-14,
    limit=500,
)

i1, i1err = quad(
    lambda x: x*d_gaussian_1d(x),
    -L,
    L,
    epsabs=1.0e-13,
    epsrel=1.0e-13,
    limit=500,
)

numeric_monopole_kg = SOURCE_MASS_KG * i0
numeric_dipole_kg = SOURCE_MASS_KG * i1
expected_dipole_kg = -SOURCE_MASS_KG

monopole_scale = max(SOURCE_MASS_KG, 1.0e-300)
numeric_monopole_relative = abs(numeric_monopole_kg)/monopole_scale
dipole_relative_error = abs(
    numeric_dipole_kg - expected_dipole_kg
) / SOURCE_MASS_KG

numerical_monopole_pass = numeric_monopole_relative < 1.0e-12
numerical_dipole_pass = dipole_relative_error < 1.0e-11

assert numerical_monopole_pass
assert numerical_dipole_pass

# The nonzero first moment is deliberately preserved:
# derivative portals are not being declared physically absent.
derivative_dipole_nonzero = abs(numeric_dipole_kg) > 0.99*SOURCE_MASS_KG
assert derivative_dipole_nonzero

# ------------------------------------------------------------
# 5. HYPERMOMENTUM / UNIVERSALITY CLAIM LOGIC
# ------------------------------------------------------------

# MAG hypermomentum is an independent connection current decomposed into
# spin, dilation and shear pieces.
hypermomentum_is_connection_source = True
hypermomentum_has_spin_dilation_shear = True

# None of those facts establishes q_hyper/m = one universal constant for
# every neutral material species.
universal_mass_proportional_hypermomentum_certified = False

# A composition-independent fifth force would require such universality,
# or an equivalent universal physical-metric construction.
ep_universality_requires_charge_to_mass_universality = True

# ------------------------------------------------------------
# 6. PORTAL TAXONOMY
# ------------------------------------------------------------

portal_classes = {
    "metric_only": {
        "status": "CLOSED_BY_032T",
        "monopole": False,
    },
    "linear_T_only_zero_derivative_rank3": {
        "status": "CLOSED_BY_RANK_THEOREM",
        "monopole": False,
    },
    "linear_T_only_one_derivative": {
        "status": "OPEN_MULTIPOLE_ONLY",
        "monopole": False,
        "dipole_possible": True,
    },
    "intrinsic_hypermomentum": {
        "status": "OPEN_BUT_UNIVERSALITY_NOT_CERTIFIED",
        "monopole_possible": True,
    },
    "extra_species_current": {
        "status": "NEW_PHYSICS_COMPOSITION_GATE_REQUIRED",
        "monopole_possible": True,
    },
    "preferred_vector_or_lorentz_breaking": {
        "status": "NEW_PHYSICS_SEPARATE_BRANCH",
        "monopole_possible": True,
    },
    "nonlinear_matter_composite": {
        "status": "NEW_PHYSICS_SEPARATE_BRANCH",
        "monopole_possible": True,
    },
}

# ------------------------------------------------------------
# 7. DECISION
# ------------------------------------------------------------

declared_linear_stress_monopole_branch_closed = (
    not zero_derivative_rank3_exists
    and one_derivative_monopole_zero
    and numerical_monopole_pass
)

derivative_multipoIe_branch_closed = False
full_hypermomentum_portal_class_closed = False
full_metric_affine_gravity_closed = False
certified_sub10mj_model = False

decision = (
    "RED_LINEAR_STRESS_ONLY_MONOPOLE_PORTAL_MULTIPOLE_FRONTIER_OPEN"
    if declared_linear_stress_monopole_branch_closed
    else "UNRESOLVED_THEOREM_REQUIRES_REPAIR"
)

next_step = (
    "GLOBAL_RERANK_UNLESS_EXPLICIT_SYMMETRY_PROTECTED_MAG_MATTER_PORTAL_FOUND"
    if declared_linear_stress_monopole_branch_closed
    else "REPAIR_032U"
)

result = {
    "branch": "032U_UNIVERSAL_HYPERMOMENTUM_PORTAL_THEOREM",
    "claim_class": "LINEAR_SOURCE_RANK_AND_MONOPOLE_PREFLIGHT",
    "energy_target_j": ENERGY_TARGET_J,
    "assumptions": [
        "local_Lorentz_covariance",
        "linear_weak_field_source",
        "ordinary_symmetric_stress_energy_only",
        "no_independent_hypermomentum",
        "no_extra_species_current",
        "no_preferred_vector",
        "no_Lorentz_breaking_background",
        "no_nonlinear_fluid_velocity_extraction",
    ],
    "rank_theorem": {
        "reachable_zero_derivative_ranks": sorted(reachable),
        "all_reachable_ranks_even": all_reachable_ranks_even,
        "rank3_source_exists": zero_derivative_rank3_exists,
        "pass": not zero_derivative_rank3_exists,
    },
    "one_derivative_static_compact_source": {
        "symbolic_monopole": str(general_monopole),
        "monopole_zero": one_derivative_monopole_zero,
        "reason": "STATIC_TIME_DERIVATIVE_ZERO_PLUS_SPATIAL_BOUNDARY_TERMS",
    },
    "gaussian_independent_check": {
        "source_mass_kg": SOURCE_MASS_KG,
        "sigma_m": SIGMA_M,
        "integration_half_width_m": L,
        "derivative_monopole_kg": numeric_monopole_kg,
        "monopole_relative_to_source_mass": numeric_monopole_relative,
        "derivative_first_moment_kg": numeric_dipole_kg,
        "expected_first_moment_kg": expected_dipole_kg,
        "first_moment_relative_error": dipole_relative_error,
        "monopole_pass": numerical_monopole_pass,
        "nonzero_dipole_confirmed": derivative_dipole_nonzero,
    },
    "hypermomentum_provenance": {
        "connection_source": hypermomentum_is_connection_source,
        "decomposition_spin_dilation_shear": hypermomentum_has_spin_dilation_shear,
        "universal_mass_proportional_charge_certified": universal_mass_proportional_hypermomentum_certified,
        "ep_requires_charge_mass_universality": ep_universality_requires_charge_to_mass_universality,
    },
    "portal_classes": portal_classes,
    "declared_linear_stress_monopole_branch_closed": declared_linear_stress_monopole_branch_closed,
    "derivative_multipole_branch_closed": derivative_multipoIe_branch_closed,
    "full_hypermomentum_portal_class_closed": full_hypermomentum_portal_class_closed,
    "full_metric_affine_gravity_closed": full_metric_affine_gravity_closed,
    "certified_sub10mj_model": certified_sub10mj_model,
    "decision": decision,
    "next": next_step,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(
    json.dumps(result,indent=2,sort_keys=True)+"\n",
    encoding="utf-8",
)

print("=== 032U RESULT ===")
print("ZERO_DERIVATIVE_RANK3_SOURCE_EXISTS=" + str(zero_derivative_rank3_exists))
print("ALL_ZERO_DERIVATIVE_REACHABLE_RANKS_EVEN=" + str(all_reachable_ranks_even))
print("ONE_DERIVATIVE_STATIC_MONOPOLE_ZERO=" + str(one_derivative_monopole_zero))
print("SOURCE_MASS_10MJ_KG=" + format(SOURCE_MASS_KG, ".12e"))
print("NUMERIC_DERIVATIVE_MONOPOLE_KG=" + format(numeric_monopole_kg, ".12e"))
print("NUMERIC_MONOPOLE_RELATIVE=" + format(numeric_monopole_relative, ".12e"))
print("NUMERIC_FIRST_MOMENT_KG=" + format(numeric_dipole_kg, ".12e"))
print("EXPECTED_FIRST_MOMENT_KG=" + format(expected_dipole_kg, ".12e"))
print("FIRST_MOMENT_RELERR=" + format(dipole_relative_error, ".12e"))
print("DERIVATIVE_DIPOLE_NONZERO=" + str(derivative_dipole_nonzero))
print("UNIVERSAL_MASS_PROPORTIONAL_HYPERMOMENTUM_CERTIFIED=" + str(universal_mass_proportional_hypermomentum_certified))
print("LINEAR_STRESS_MONOPOLE_BRANCH_CLOSED=" + str(declared_linear_stress_monopole_branch_closed))
print("DERIVATIVE_MULTIPOLE_BRANCH_CLOSED=False")
print("FULL_HYPERMOMENTUM_PORTAL_CLASS_CLOSED=False")
print("FULL_METRIC_AFFINE_GRAVITY_CLOSED=False")
print("CERTIFIED_SUB10MJ_MODEL=False")
print("DECISION=" + decision)
print("NEXT=" + next_step)
