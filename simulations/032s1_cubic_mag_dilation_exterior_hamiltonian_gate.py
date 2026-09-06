"""
032S1 — cubic metric-affine pure-dilation exterior Hamiltonian gate.

This run reconstructs the charge-dependent vector sector of the exact
RN-like cubic-MAG solution and tests whether stable torsion/nonmetricity
mixing can improve metric charge per positive kinetic joule.

Literature equations used:

  Q_d = 1/2 kappa_d^2
        (2 a6 - 4 a2 - 8 a14 - d1)

and the vector kinetic terms

  16 pi L_kin =
      d1/18 F_T^2
    + (16a2-8a6+32a14+5d1)/8 F_W^2
    - d1/6 F_T F_W
    + terms containing Lambda or axial fields.

Ghost-free conditions include

  d1 <= 0,
  a6 <= -2 a2,
  a14 <= (2a6-4a2-d1)/8.

Parameterize the last inequality as

  a14 = (2a6-4a2-d1)/8 - w,
  w >= 0.

For the pure dilation charge, the exact solution has

  W_t = kappa_d/r
  W_r = -kappa_d/(r Psi)

and the charge-dependent torsion vector satisfies

  T_t = 3 kappa_d/(2r)
  T_r = -3 kappa_d/(2r Psi),

so

  F_T = 3/2 F_W.

The positive electrostatic kinetic form then becomes

  K =
      4 w F_W^2
    + (-d1)/72 (2 F_T - 3 F_W)^2

and therefore

  K >= 4 w F_W^2.

The exact dilation solution saturates the bound.

At the same time

  Q_d = 4 w kappa_d^2.

Defining A_mu = 2 sqrt(w) W_mu therefore gives the canonical
Einstein-Maxwell normalization

  16 pi L = -F_A^2

for the charge-dependent pure-dilation exterior sector, with

  q_A^2 = Q_d.

Thus the positive exterior field inventory is

  E_out(R) = Q_d c^4/(2 G R).

This is an exterior positive-field inventory statement.
Negative gravitational binding or inner cancellations are not allowed
to erase positive operating inventory under the project energy policy.

The result closes only the declared stable pure-dilation RN-like branch.
Spin, shear and genuinely different MAG charge sectors remain separate.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp
import mpmath as mp


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "data" / "032s1_cubic_mag_dilation_exterior_hamiltonian_summary.json"
TAIL_OUT = ROOT / "results" / "data" / "032s1_dilation_positive_tail_energy.csv"
S0 = ROOT / "results" / "data" / "032s0_cubic_mag_dilation_rn_finite_payload_summary.json"

G = 6.67430e-11
C = 299792458.0
ENERGY_TARGET_J = 1.0e7
LIGHT_YEAR_M = 9.4607304725808e15
PARSEC_M = 3.085677581491367e16

if not S0.exists():
    raise FileNotFoundError(str(S0))

s0 = json.loads(S0.read_text(encoding="utf-8"))

Q_NUM = float(s0["required_q_metric_m2"])
R_SOURCE = float(s0["optimized_source_radius_m"])
E_S0_BENCH = float(
    s0["canonical_maxwell_like_benchmark"]["optimized_exterior_energy_j"]
)
TURNOVER_R = float(s0["turnover_to_far_field_attraction_radius_m"])


# ------------------------------------------------------------
# 1. SYMBOLIC STABILITY / METRIC CHARGE REDUCTION
# ------------------------------------------------------------

a2, a6, d1, w, kd = sp.symbols(
    "a2 a6 d1 w kd",
    real=True,
)
FT, FW = sp.symbols("FT FW", real=True)
x = sp.symbols("x", nonnegative=True, real=True)

a14 = (2*a6 - 4*a2 - d1)/8 - w

q_coeff = sp.simplify(
    sp.Rational(1,2)
    * (2*a6 - 4*a2 - 8*a14 - d1)
)
q_metric = sp.simplify(kd**2 * q_coeff)

c_t = d1 / 18
c_w = sp.simplify(
    (16*a2 - 8*a6 + 32*a14 + 5*d1) / 8
)
c_tw = -d1 / 6

# For an electrostatic field F_mu_nu F^mu_nu is negative.
# The positive energy quadratic form is minus the displayed L coefficient.
kinetic_positive = sp.expand(
    -(c_t*FT**2 + c_w*FW**2 + c_tw*FT*FW)
)

kinetic_x = sp.simplify(kinetic_positive.subs(d1, -x))

expected_square = (
    4*w*FW**2
    + x*sp.expand((2*FT - 3*FW)**2)/72
)

square_identity = sp.simplify(kinetic_x - expected_square)

# Exact pure-dilation field-strength relation.
pure_dilation_kinetic = sp.simplify(
    kinetic_positive.subs(FT, sp.Rational(3,2)*FW)
)

# ------------------------------------------------------------
# 2. INDEPENDENT PURE-DILATION TRACE RECONSTRUCTION
# ------------------------------------------------------------

r, psi = sp.symbols("r psi", positive=True, real=True)

# Pure-dilation nonmetricity components from the exact solution.
q1 = kd*psi/r
q2 = -kd/(r*psi)
q3 = sp.Integer(0)
q4 = -r*kd
q5 = -kd/r
q6 = kd/(r*psi**2)
q7 = sp.Integer(0)
q8 = r*kd/psi
q9 = sp.Integer(0)
q10 = sp.Integer(0)

# W_lambda = 1/4 g^{mu nu} Q_lambda mu nu.
W_t = sp.simplify(
    sp.Rational(1,4)
    * (
        q1/psi
        - psi*q2
        - q4/r**2
        - q4/r**2
    )
)

W_r = sp.simplify(
    sp.Rational(1,4)
    * (
        q5/psi
        - psi*q6
        - q8/r**2
        - q8/r**2
    )
)

# Q^nu_{t nu} and Q^nu_{r nu}; equality with W implies Lambda=0.
trace_t = sp.simplify(q1/psi - psi*q7)
trace_r = sp.simplify(q3/psi - psi*q6)

Lambda_t = sp.simplify(sp.Rational(4,9)*(trace_t - W_t))
Lambda_r = sp.simplify(sp.Rational(4,9)*(trace_r - W_r))

# Charge-dependent torsion pieces from t1,t4 and t2=t1 Psi,
# t3=-t4 Psi.
t1_charge = kd/(2*r*psi)
t4_charge = -kd/(2*r*psi)
t2_charge = sp.simplify(t1_charge*psi)
t3_charge = sp.simplify(-t4_charge*psi)

T_t = sp.simplify(t2_charge + 2*t3_charge)
T_r = sp.simplify(-t1_charge + 2*t4_charge)

F_W_tr = sp.simplify(-sp.diff(W_t, r))
F_T_tr = sp.simplify(-sp.diff(T_t, r))
field_ratio = sp.simplify(F_T_tr/F_W_tr)

# ------------------------------------------------------------
# 3. NUMERICAL EXTERIOR POSITIVE-FIELD INVENTORY
# ------------------------------------------------------------

def exterior_energy_j(radius_m):
    return Q_NUM * C**4 / (2.0 * G * radius_m)

E_EXTERIOR = exterior_energy_j(R_SOURCE)
E_OVER_TARGET = E_EXTERIOR / ENERGY_TARGET_J
E_MATCH_RELERR = abs(E_EXTERIOR - E_S0_BENCH) / E_S0_BENCH

# Radius outside which the remaining canonical positive tail finally falls
# below the complete 10-MJ objective.
R_TAIL_10MJ = Q_NUM * C**4 / (2.0 * G * ENERGY_TARGET_J)
R_TAIL_10MJ_LY = R_TAIL_10MJ / LIGHT_YEAR_M
R_TAIL_10MJ_PC = R_TAIL_10MJ / PARSEC_M

E_AT_TURNOVER = exterior_energy_j(TURNOVER_R)

REQUIRED_SURVIVING_FRACTION = ENERGY_TARGET_J / E_EXTERIOR
REQUIRED_ENHANCEMENT = E_OVER_TARGET

# ------------------------------------------------------------
# 4. NUMERIC STRESS TEST OF THE SYMBOLIC SCHUR BOUND
# ------------------------------------------------------------

rng = np.random.default_rng(32051)

# The original float64 Schur audit formed
#
#   4w + x/8 - x/8,
#
# while x/w ranged over as much as 1e36.
# That is intentionally a catastrophic-cancellation problem.
# The symbolic square identity above is exact; this numerical audit now
# evaluates the unreduced Schur expression with 100-decimal precision.

N_STRESS = 20_000
MP_DPS = 100
mp.mp.dps = MP_DPS

logx = rng.uniform(-18.0, 18.0, N_STRESS)
logw = rng.uniform(-18.0, 18.0, N_STRESS)

max_err_mp = mp.mpf("0")
min_ratio_mp = mp.inf
max_ratio_mp = -mp.inf
max_cancellation_ratio_mp = mp.mpf("0")

for lx, lw in zip(logx, logw):
    x_mp = mp.power(10, mp.mpf(repr(float(lx))))
    w_mp = mp.power(10, mp.mpf(repr(float(lw))))

    term_w = 4 * w_mp
    term_x = x_mp / 8

    schur_mp = (
        term_w
        + term_x
        - (x_mp / 12) ** 2 / (x_mp / 18)
    )

    ratio_mp = schur_mp / term_w
    err_mp = abs(ratio_mp - 1)

    max_err_mp = max(max_err_mp, err_mp)
    min_ratio_mp = min(min_ratio_mp, ratio_mp)
    max_ratio_mp = max(max_ratio_mp, ratio_mp)
    max_cancellation_ratio_mp = max(
        max_cancellation_ratio_mp,
        term_x / term_w,
    )

max_schur_relerr = float(max_err_mp)
min_schur_ratio = float(min_ratio_mp)
max_schur_ratio = float(max_ratio_mp)
max_cancellation_ratio = float(max_cancellation_ratio_mp)

numeric_stress_pass = (
    max_schur_relerr < 1.0e-50
    and abs(min_schur_ratio - 1.0) < 1.0e-50
    and abs(max_schur_ratio - 1.0) < 1.0e-50
)


# ------------------------------------------------------------
# 5. POSITIVE TAIL CONVERGENCE TABLE
# ------------------------------------------------------------

radii = np.geomspace(R_SOURCE, 1.0e21, 81)
rows = []

for radius in radii:
    energy = exterior_energy_j(float(radius))
    rows.append(
        {
            "radius_m": float(radius),
            "radius_ly": float(radius/LIGHT_YEAR_M),
            "radius_pc": float(radius/PARSEC_M),
            "positive_tail_energy_j": float(energy),
            "tail_over_10mj": float(energy/ENERGY_TARGET_J),
        }
    )

with TAIL_OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
    writer.writeheader()
    writer.writerows(rows)

# ------------------------------------------------------------
# 6. GATES
# ------------------------------------------------------------

symbolic_metric_pass = sp.simplify(q_coeff - 4*w) == 0
symbolic_square_pass = square_identity == 0
pure_solution_saturates = (
    sp.simplify(pure_dilation_kinetic - 4*w*FW**2) == 0
)
trace_pass = (
    sp.simplify(W_t - kd/r) == 0
    and sp.simplify(W_r + kd/(r*psi)) == 0
    and Lambda_t == 0
    and Lambda_r == 0
)
torsion_ratio_pass = sp.simplify(field_ratio - sp.Rational(3,2)) == 0
# numeric_stress_pass is defined by the multiprecision audit above.
normalization_match_pass = E_MATCH_RELERR < 1.0e-12

positive_exterior_inventory_kills_target = E_EXTERIOR >= ENERGY_TARGET_J

declared_dilation_branch_closed = (
    symbolic_metric_pass
    and symbolic_square_pass
    and pure_solution_saturates
    and trace_pass
    and torsion_ratio_pass
    and numeric_stress_pass
    and normalization_match_pass
    and positive_exterior_inventory_kills_target
)

result = {
    "branch": "032S1_CUBIC_MAG_PURE_DILATION_EXTERIOR_HAMILTONIAN",
    "claim_class": "EXACT_GHOST_FREE_QUADRATIC_EXTERIOR_ENERGY_GATE",
    "literature_equations_reconstructed": {
        "metric_dilation_coefficient_simplifies_to_4w": symbolic_metric_pass,
        "positive_kinetic_square_identity": symbolic_square_pass,
        "pure_dilation_saturates_square_bound": pure_solution_saturates,
        "pure_dilation_weyl_trace_reconstruction": trace_pass,
        "pure_dilation_lambda_zero": bool(Lambda_t == 0 and Lambda_r == 0),
        "torsion_to_weyl_field_strength_ratio_3_over_2": torsion_ratio_pass,
    },
    "symbolic": {
        "q_d": str(q_metric),
        "positive_kinetic_form": str(sp.factor(kinetic_x)),
        "square_form": str(sp.factor(expected_square)),
        "pure_dilation_positive_kinetic": str(sp.factor(pure_dilation_kinetic)),
        "W_t": str(W_t),
        "W_r": str(W_r),
        "Lambda_t": str(Lambda_t),
        "Lambda_r": str(Lambda_r),
        "T_t_charge": str(T_t),
        "T_r_charge": str(T_r),
        "F_T_over_F_W": str(field_ratio),
    },
    "numeric_stress": {
        "samples": N_STRESS,
        "min_schur_ratio_to_4w": min_schur_ratio,
        "max_schur_ratio_to_4w": max_schur_ratio,
        "max_relative_error": max_schur_relerr,
        "multiprecision_decimal_digits": MP_DPS,
        "max_cancellation_ratio": max_cancellation_ratio,
        "pass": numeric_stress_pass,
    },
    "finite_payload_input_from_032S0": {
        "required_q_metric_m2": Q_NUM,
        "source_radius_m": R_SOURCE,
        "turnover_radius_m": TURNOVER_R,
    },
    "positive_exterior_inventory": {
        "formula": "Q*c^4/(2*G*R)",
        "source_surface_energy_j": E_EXTERIOR,
        "source_surface_energy_over_10mj": E_OVER_TARGET,
        "032s0_benchmark_j": E_S0_BENCH,
        "relative_match_to_032s0_benchmark": E_MATCH_RELERR,
        "required_surviving_fraction_for_10mj": REQUIRED_SURVIVING_FRACTION,
        "required_charge_per_joule_enhancement_vs_exact_dilation": REQUIRED_ENHANCEMENT,
        "radius_for_tail_to_fall_to_10mj_m": R_TAIL_10MJ,
        "radius_for_tail_to_fall_to_10mj_ly": R_TAIL_10MJ_LY,
        "radius_for_tail_to_fall_to_10mj_pc": R_TAIL_10MJ_PC,
        "tail_energy_at_turnover_radius_j": E_AT_TURNOVER,
    },
    "negative_binding_allowed_to_game_objective": False,
    "finite_source_matching_needed_to_rescue_energy_gate": False,
    "source_internal_energy_included": False,
    "support_control_energy_included": False,
    "those_omissions_can_only_increase_positive_inventory": True,
    "strict_sub10mj_pure_dilation_branch": False,
    "declared_stable_pure_dilation_branch_closed": declared_dilation_branch_closed,
    "full_cubic_mag_family_closed": False,
    "spin_charge_branch_closed": False,
    "shear_charge_branch_closed": False,
    "decision": (
        "RED_PURE_DILATION_CANONICAL_RN_ENERGY_BURDEN"
        if declared_dilation_branch_closed
        else "UNRESOLVED_REQUIRES_REPAIR"
    ),
    "next": (
        "032S2_CUBIC_MAG_SHEAR_CHARGE_LEVERAGE_PREFLIGHT"
        if declared_dilation_branch_closed
        else "REPAIR_032S1"
    ),
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(
    json.dumps(result, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

print("=== 032S1 RESULT ===")
print("Q_D_COEFFICIENT=" + str(sp.factor(q_coeff)))
print("POSITIVE_KINETIC_SQUARE_IDENTITY=" + str(symbolic_square_pass))
print("PURE_DILATION_SATURATES_BOUND=" + str(pure_solution_saturates))
print("W_T=" + str(W_t))
print("W_R=" + str(W_r))
print("LAMBDA_T=" + str(Lambda_t))
print("LAMBDA_R=" + str(Lambda_r))
print("F_T_OVER_F_W=" + str(field_ratio))
print("NUMERIC_SCHUR_STRESS_SAMPLES=" + str(N_STRESS))
print("NUMERIC_SCHUR_MAX_RELERR=" + format(max_schur_relerr, ".12e"))
print("NUMERIC_SCHUR_MP_DPS=" + str(MP_DPS))
print("NUMERIC_MAX_CANCELLATION_RATIO=" + format(max_cancellation_ratio, ".12e"))
print("Q_REQUIRED_M2=" + format(Q_NUM, ".12e"))
print("SOURCE_RADIUS_M=" + format(R_SOURCE, ".12e"))
print("POSITIVE_EXTERIOR_FIELD_J=" + format(E_EXTERIOR, ".12e"))
print("EXTERIOR_FIELD_OVER_10MJ=" + format(E_OVER_TARGET, ".12e"))
print("MATCH_TO_032S0_BENCH_RELERR=" + format(E_MATCH_RELERR, ".12e"))
print("REQUIRED_SURVIVING_FRACTION=" + format(REQUIRED_SURVIVING_FRACTION, ".12e"))
print("TAIL_10MJ_RADIUS_M=" + format(R_TAIL_10MJ, ".12e"))
print("TAIL_10MJ_RADIUS_LY=" + format(R_TAIL_10MJ_LY, ".12e"))
print("TAIL_10MJ_RADIUS_PC=" + format(R_TAIL_10MJ_PC, ".12e"))
print("TAIL_AT_TURNOVER_J=" + format(E_AT_TURNOVER, ".12e"))
print("NEGATIVE_BINDING_CAN_GAME_OBJECTIVE=NO")
print("SOURCE_INTERNAL_ENERGY_ADDED=NO")
print("SUPPORT_CONTROL_ENERGY_ADDED=NO")
print("STRICT_SUB10MJ_PURE_DILATION=NO")
print("DECLARED_STABLE_PURE_DILATION_BRANCH_CLOSED=" + str(declared_dilation_branch_closed))
print("FULL_CUBIC_MAG_FAMILY_CLOSED=False")
print("DECISION=" + result["decision"])
print("NEXT=" + result["next"])
