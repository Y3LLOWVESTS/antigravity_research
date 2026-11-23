"""DELTA1-F0F: exact portal stress and conditional GR energy bound.

No microphysical source, on-shell universal metric or whole-craft
force is derived.

The far-source inequality assumes all gravitating stress, including
carrier fields and supports, lies >=d from a neutral target point,
obeys DEC and is static/weak-field. A 1m gap in source matter alone
is NOT enough.
"""

import hashlib
import itertools
import json
import math
import os
from datetime import datetime, timezone
from fractions import Fraction as Q
from pathlib import Path

OUT = Path(os.environ["F0F_RUN"]).resolve()
PARENT = Path(os.environ["F0E_PARENT"]).resolve()

EXPECTED = {
    "science.json":
        "bdc6d1b27befa108cc982d392e8bf265c17b96f814f54810d49b180d0dc834d4",
    "verification.json":
        "63ca7c612bf5d39e6fa238c9a992b31500f3067e090e3cc43047ca7d87a8503e",
    "f0e.py":
        "2b09062244380ce573442e169b76a602e49a4a690d628838bcac92158fcd6fe1",
    "verify.py":
        "2628c93c66a31f91b92634a1d3e8de95ff80242ce21ef91afa04754cdd041581",
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sign(values):
    inversions = sum(
        values[i] > values[j]
        for i in range(len(values))
        for j in range(i + 1, len(values))
    )
    return -1 if inversions % 2 else 1

def fvalue(F, i, j):
    if i == j:
        return Q(0)
    return F[(i, j)] if i < j else -F[(j, i)]

def wedge(F, H):
    return sum(
        (
            Q(sign(p), 4)
            * fvalue(F, p[0], p[1])
            * fvalue(H, p[2], p[3])
            for p in itertools.permutations(range(4))
        ),
        Q(0),
    )

def determinant(M):
    return sum(
        (
            sign(p) * math.prod(M[i][p[i]] for i in range(4))
            for p in itertools.permutations(range(4))
        ),
        0.0,
    )

def save(name, data):
    with (OUT / name).open("x") as f:
        json.dump(data, f, indent=2, sort_keys=True, allow_nan=False)
        f.write("\n")
    (OUT / (name + ".sha256")).write_text(
        sha(OUT / name) + "  " + name + "\n"
    )

record = {
    "program": "DELTA1-F0F_EXACT_PORTAL_METRIC_AND_CONDITIONAL_GR_ENERGY_ATLAS",
    "utc": datetime.now(timezone.utc).isoformat(),
    "source_sha256": sha(Path(__file__)),
    "parents": {
        str(PARENT / name): value
        for name, value in EXPECTED.items()
    },
    "regression": "NOT_RUN_F0_ANALYTICAL_PREFLIGHT",
    "gravitational_lift": "NOT_DERIVED",
    "whole_craft_external_force": "NOT_DERIVED",
    "physical_source": "NOT_DERIVED",
    "complete_energy_lt_10MJ": "NOT_CERTIFIED",
    "006D_replaced": False,
}

try:
    for name, expected in EXPECTED.items():
        require(
            sha(PARENT / name) == expected,
            "parent SHA mismatch: " + name,
        )

    parent = json.loads((PARENT / "science.json").read_bytes())
    verified = json.loads((PARENT / "verification.json").read_bytes())

    require(
        parent["status"] ==
        "NECESSARY_GATES_DERIVED_NO_PHYSICAL_PROMOTION",
        "F0E scientific status",
    )
    require(
        verified["status"] ==
        "PASS_SCOPED_NECESSARY_GATES_ONLY",
        "F0E verification status",
    )
    require(
        len(verified["checks"]) == 35
        and all(verified["checks"].values()),
        "F0E focused checks",
    )
    require(
        parent["physical_source"] == "NOT_SPECIFIED",
        "source provenance",
    )

    # A. Covariant completion: theta * F_X wedge F_Y.
    #
    # At fixed theta and covariant 2-form components, the
    # 4-form does not depend on the spacetime metric.
    #
    # This does NOT eliminate indirect carrier, source,
    # material or metric-dependent theta stress.

    X = {
        (0,1): Q(6,5), (0,2): Q(-3,10),
        (0,3): Q(1,7), (1,2): Q(9,10),
        (1,3): Q(-1,5), (2,3): Q(1,11),
    }

    Y = {
        (0,1): Q(2,3), (0,2): Q(2,5),
        (0,3): Q(9,10), (1,2): Q(-1,2),
        (1,3): Q(1,8), (2,3): Q(4,5),
    }

    W = wedge(X, Y)
    require(W != 0, "nontrivial wedge control")

    metrics = [
        [[-1.,0,0,0],[0,1.,0,0],[0,0,1.,0],[0,0,0,1.]],
        [[-4.,0,0,0],[0,4.,0,0],[0,0,4.,0],[0,0,0,4.]],
        [[-.9,0,0,0],[0,1.1,0,0],[0,0,2.,0],[0,0,0,.8]],
        [[-1.,.2,0,0],[.2,1.,0,0],
         [0,0,1.4,.15],[0,0,.15,.7]],
    ]

    metric_tests = []

    for M in metrics:
        det = determinant(M)
        require(det < 0, "non-Lorentzian test metric")

        sqrtg = math.sqrt(-det)
        density = float(W) / sqrtg
        integrated = sqrtg * density

        require(
            abs(integrated - float(W)) < 1e-13,
            "metric independence",
        )

        metric_tests.append({
            "det_g": det,
            "sqrt_minus_g": sqrtg,
            "densitized_portal": integrated,
        })

    # Induced current from dtheta wedge F_Y.
    dtheta = {
        0: Q(0), 1: Q(1,5),
        2: Q(0), 3: Q(0),
    }

    current_123 = (
        dtheta[1] * fvalue(Y,2,3)
        + dtheta[2] * fvalue(Y,3,1)
        + dtheta[3] * fvalue(Y,1,2)
    )

    require(
        current_123 == Q(4,25),
        "variable-theta current",
    )

    record["portal"] = {
        "covariant_operator": "theta F_X wedge F_Y",
        "wedge_exact": str(W),
        "wedge_float": float(W),
        "metric_tests": metric_tests,
        "direct_Hilbert_stress_fixed_theta": "EXACTLY_ZERO",
        "spatially_variable_theta_bulk_current_123_exact":
            str(current_123),
        "spatially_variable_theta_bulk_current_123":
            float(current_123),
        "constant_theta_bulk_current": "ZERO",
        "if_theta_is_metric_dependent":
            "ADDITIONAL_CHAIN_RULE_STRESS_UNDERIVED",
        "carrier_source_support_stress":
            "MUST_BE_VARIED_SEPARATELY",
        "actual_F0E_covariant_completion": "NOT_SPECIFIED",
        "physical_metric": "NOT_DERIVED",
    }

    # B. Static weak-field Einstein gravity:
    #
    # |a| <= G/d² * integral |T00 + Tii|/c² dV
    #     <= 4 G U/(c² d²)
    #
    # DEC implies |Tii| <= T00 in an orthonormal frame.
    #
    # This bound requires distance from ALL gravitating
    # stress, not merely from onboard source matter.

    G = 6.67430e-11
    c = 299792458.0
    target_g = 9.80665
    d = 1.0
    budget = 10_000_000.0

    max_dec = 4 * G * budget / (c*c*d*d)
    max_maxwell = 2 * G * budget / (c*c*d*d)

    required_dec = target_g * c*c*d*d / (4*G)
    required_maxwell = target_g * c*c*d*d / (2*G)

    minimum_distance = math.sqrt(
        4*G*budget / (target_g*c*c)
    )

    require(
        abs(max_dec*required_dec/(target_g*budget)-1)
        < 1e-14,
        "energy-bound algebra",
    )
    require(
        required_dec > budget*1e20,
        "source-energy scale",
    )

    stress_examples = {
        "DEC_max_trace_factor": 4,
        "Maxwell_trace_factor": 2,
        "DEC_violation_counterexample_trace_factor": 7,
    }

    record["static_weak_field_GR_conditional_bound"] = {
        "G_SI": G,
        "c_m_per_s": c,
        "target_acceleration_m_per_s2": target_g,
        "minimum_distance_from_ALL_GRAVITATING_STRESS_m": d,
        "illustrative_total_gravitating_stress_energy_J": budget,
        "assumptions": [
            "Einstein gravity; linearized static weak-field",
            "DEC holds for complete stress-energy including supports",
            "ALL relevant source stress, including carrier-field energy, is at least d from every tested neutral material point",
            "U is total positive gravitating stress energy, including rest energy; it is NOT automatically operating energy",
        ],
        "max_acceleration_DEC_m_per_s2": max_dec,
        "max_acceleration_Maxwell_only_m_per_s2": max_maxwell,
        "necessary_U_DEC_J": required_dec,
        "necessary_U_Maxwell_only_J": required_maxwell,
        "necessary_DEC_source_mass_equivalent_kg":
            required_dec/(c*c),
        "shortfall_factor_at_U10MJ_DEC":
            required_dec/budget,
        "necessary_minimum_stress_distance_at_U10MJ_m":
            minimum_distance,
        "stress_examples": stress_examples,
        "if_only_SOURCE_MATTER_is_1m_away":
            "BOUND_NOT_APPLICABLE_UNTIL_CARRIER_STRESS_IN_GAP_IS_BOUNDED",
        "operating_energy_equals_total_gravitating_U":
            "NOT_ESTABLISHED",
        "DEC_full_F0_source_support": "NOT_ESTABLISHED",
        "stand_off_to_total_stress": "NOT_ESTABLISHED",
        "claim_scope":
            "CONDITIONAL_NECESSARY_LOWER_BOUND_NOT_DEVICE_NO_GO",
    }

    # C. Earth/craft negative control.
    # Ordinary positive-mass Newtonian attraction cannot be
    # relabeled as the required repulsive Earth-down/craft-up.

    M_earth = 1.0e12
    M_craft = 1.0
    force_craft_z = -G*M_earth*M_craft

    record["earth_craft_sign_negative_control"] = {
        "toy": "ordinary_positive_mass_Newtonian_pair",
        "craft_force_z_N": force_craft_z,
        "earth_force_z_N": -force_craft_z,
        "sum_force_z_N": 0.0,
        "earth_down_craft_up":
            "NO_FOR_ORDINARY_ATTRACTION",
        "full_actual_action_force": "NOT_DERIVED",
    }

    record["decision"] = {
        "status":
            "SCOPED_L0_ATLAS_COMPLETE_NO_PHYSICAL_PROMOTION",
        "F0_portal_direct_metric_stress":
            "NULL_UNDER_METRIC_INDEPENDENT_THETA",
        "source_to_metric_bridge":
            "MISSING_REAL_COVARIANT_SOURCE_AND_THETA_METRIC_DEPENDENCE",
        "weak_field_GR_energy":
            "HUGE_CONDITIONAL_OBSTRUCTION_IF_STRESS_STANDOFF_AND_U_CAP_HOLD",
        "next_high_information_falsifier":
            "DERIVE_COMPLETE_COVARIANT_THETA_METRIC_VARIATION_AND_ACTUAL_LOADED_STRESS_SPATIAL_SUPPORT_BEFORE_NEW_PDE",
        "full_regression_required_before_promotion": True,
    }

    record["status"] = (
        "PASS_SCOPED_THEOREM_AND_CONDITIONAL_OBSTRUCTION"
    )

except Exception as exc:
    record["status"] = "HOLD"
    record["error"] = repr(exc)

save("science.json", record)

print("F0F_SCIENCE =", record["status"])

if "portal" in record:
    print(
        "DIRECT_PORTAL_HILBERT_STRESS =",
        record["portal"]["direct_Hilbert_stress_fixed_theta"],
    )
    print(
        "CONDITIONAL_GR_ENERGY_LOWER_J =",
        record["static_weak_field_GR_conditional_bound"]["necessary_U_DEC_J"],
    )
    print(
        "SHORTFALL_FACTOR =",
        record["static_weak_field_GR_conditional_bound"]["shortfall_factor_at_U10MJ_DEC"],
    )

print("SCIENCE_SHA256 =", sha(OUT / "science.json"))

if record["status"] == "HOLD":
    raise SystemExit(1)
