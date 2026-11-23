"""Independent F0F verification: exact wedge and decimal GR bound."""

import hashlib
import json
import math
import os
from decimal import Decimal, getcontext
from fractions import Fraction as Q
from pathlib import Path

OUT = Path(os.environ["F0F_RUN"]).resolve()
checks = {}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check(name, condition):
    checks[name] = bool(condition)
    if not checks[name]:
        raise AssertionError(name)

def fget(F, a, b):
    if a == b:
        return Q(0)
    return F[(a,b)] if a < b else -F[(b,a)]

v = {
    "program": "DELTA1_F0F_INDEPENDENT_CHECK",
    "verifier_source_sha256": sha(Path(__file__)),
    "checks": checks,
    "full_regression": "NOT_RUN",
    "physical_gravity": "NOT_DERIVED",
    "complete_operating_energy": "NOT_CERTIFIED",
    "whole_craft": "NOT_DERIVED",
}

try:
    path = OUT / "science.json"
    s = json.loads(path.read_bytes())

    check(
        "science sha sidecar",
        (OUT / "science.json.sha256").read_text().split()
        == [sha(path), "science.json"],
    )

    check(
        "producer hash",
        s["source_sha256"] == sha(OUT / "f0f.py"),
    )

    check(
        "parents 4 hashes",
        len(s["parents"]) == 4
        and all(
            sha(Path(path)) == expected
            for path, expected in s["parents"].items()
        ),
    )

    parent = Path(os.environ["F0E_PARENT"])

    check(
        "F0E science parent",
        json.loads((parent/"science.json").read_text())["status"]
        == "NECESSARY_GATES_DERIVED_NO_PHYSICAL_PROMOTION",
    )

    check(
        "F0E verifier parent",
        json.loads((parent/"verification.json").read_text())["status"]
        == "PASS_SCOPED_NECESSARY_GATES_ONLY",
    )

    # Independent explicit wedge expansion.
    # This does not reuse APPLY's Levi-Civita permutation code.

    X = {
        (0,1):Q(6,5), (0,2):Q(-3,10),
        (0,3):Q(1,7), (1,2):Q(9,10),
        (1,3):Q(-1,5), (2,3):Q(1,11),
    }

    Y = {
        (0,1):Q(2,3), (0,2):Q(2,5),
        (0,3):Q(9,10), (1,2):Q(-1,2),
        (1,3):Q(1,8), (2,3):Q(4,5),
    }

    wedge = (
        fget(X,0,1)*fget(Y,2,3)
        - fget(X,0,2)*fget(Y,1,3)
        + fget(X,0,3)*fget(Y,1,2)
        + fget(X,2,3)*fget(Y,0,1)
        - fget(X,1,3)*fget(Y,0,2)
        + fget(X,1,2)*fget(Y,0,3)
    )

    portal = s["portal"]

    check(
        "independent exact wedge",
        str(wedge) == portal["wedge_exact"],
    )
    check("nonzero wedge control", wedge != 0)

    check(
        "direct Hilbert null fixed scalar",
        portal["direct_Hilbert_stress_fixed_theta"]
        == "EXACTLY_ZERO",
    )

    check(
        "all metric determinant tests",
        len(portal["metric_tests"]) == 4
        and all(
            x["det_g"] < 0
            and math.isclose(
                x["densitized_portal"],
                float(wedge),
                rel_tol=1e-13,
                abs_tol=1e-13,
            )
            for x in portal["metric_tests"]
        ),
    )

    check(
        "spatial theta current",
        portal["spatially_variable_theta_bulk_current_123_exact"]
        == str(Q(1,5)*fget(Y,2,3)),
    )

    check(
        "constant theta current",
        portal["constant_theta_bulk_current"] == "ZERO",
    )

    check(
        "theta material chain unclosed",
        portal["if_theta_is_metric_dependent"]
        == "ADDITIONAL_CHAIN_RULE_STRESS_UNDERIVED",
    )

    check(
        "noncovariant source unpromoted",
        portal["actual_F0E_covariant_completion"]
        == "NOT_SPECIFIED",
    )

    # Independent high-precision GR energy calculation.

    getcontext().prec = 60

    G = Decimal("6.67430e-11")
    c = Decimal("299792458")
    g = Decimal("9.80665")
    U = Decimal("10000000")
    d = Decimal("1")

    lower = g*c*c*d*d/(Decimal(4)*G)
    upper = Decimal(4)*G*U/(c*c*d*d)
    ratio = lower/U
    length = (Decimal(4)*G*U/(g*c*c)).sqrt()

    bound = s["static_weak_field_GR_conditional_bound"]

    def close(a, b):
        return (
            abs(Decimal(str(b))-a)
            /max(Decimal(1),abs(a))
            < Decimal("2e-14")
        )

    check(
        "independent DEC lower J",
        close(lower,bound["necessary_U_DEC_J"]),
    )

    check(
        "independent max g DEC",
        close(upper,bound["max_acceleration_DEC_m_per_s2"]),
    )

    check(
        "independent shortfall",
        close(ratio,bound["shortfall_factor_at_U10MJ_DEC"]),
    )

    check(
        "independent min stress distance",
        close(
            length,
            bound["necessary_minimum_stress_distance_at_U10MJ_m"],
        ),
    )

    check(
        "Maxwell factor two",
        close(
            g*c*c/(Decimal(2)*G),
            bound["necessary_U_Maxwell_only_J"],
        ),
    )

    check(
        "mass equivalent",
        close(
            lower/(c*c),
            bound["necessary_DEC_source_mass_equivalent_kg"],
        ),
    )

    check(
        "strict 10MJ obstruction under all assumptions",
        lower > U and ratio > Decimal("1e20"),
    )

    stress = bound["stress_examples"]

    check(
        "conservative stress trace bound",
        stress["DEC_max_trace_factor"] == 4
        and stress["Maxwell_trace_factor"] == 2,
    )

    check(
        "DEC violator excluded",
        stress["DEC_violation_counterexample_trace_factor"] > 4,
    )

    check(
        "source matter gap not sufficient",
        bound["if_only_SOURCE_MATTER_is_1m_away"]
        == "BOUND_NOT_APPLICABLE_UNTIL_CARRIER_STRESS_IN_GAP_IS_BOUNDED",
    )

    check(
        "energy budget not total active stress",
        bound["operating_energy_equals_total_gravitating_U"]
        == "NOT_ESTABLISHED",
    )

    check(
        "full source DEC missing",
        bound["DEC_full_F0_source_support"]
        == "NOT_ESTABLISHED",
    )

    check(
        "total stress support missing",
        bound["stand_off_to_total_stress"]
        == "NOT_ESTABLISHED",
    )

    check(
        "no unconditional no go",
        bound["claim_scope"]
        == "CONDITIONAL_NECESSARY_LOWER_BOUND_NOT_DEVICE_NO_GO",
    )

    earth = s["earth_craft_sign_negative_control"]

    check(
        "toy recoil equal opposite",
        earth["earth_force_z_N"] + earth["craft_force_z_N"]
        == 0.0,
    )

    check(
        "ordinary attraction negative control",
        earth["craft_force_z_N"] < 0
        and earth["earth_force_z_N"] > 0
        and earth["earth_down_craft_up"]
        == "NO_FOR_ORDINARY_ATTRACTION",
    )

    check(
        "no actual Earth claim",
        earth["full_actual_action_force"] == "NOT_DERIVED",
    )

    check(
        "no physical promotion",
        s["status"]
        == "PASS_SCOPED_THEOREM_AND_CONDITIONAL_OBSTRUCTION"
        and s["physical_source"] == "NOT_DERIVED"
        and s["whole_craft_external_force"] == "NOT_DERIVED"
        and s["complete_energy_lt_10MJ"] == "NOT_CERTIFIED"
        and s["006D_replaced"] is False,
    )

    check(
        "no full regression claim",
        s["regression"] == "NOT_RUN_F0_ANALYTICAL_PREFLIGHT",
    )

    v["status"] = (
        "PASS_SCOPED_EXACT_PORTAL_AND_CONDITIONAL_DEC_BOUND"
    )

except Exception as exc:
    v["status"] = "HOLD"
    v["error"] = repr(exc)

with (OUT/"verification.json").open("x") as f:
    json.dump(v,f,indent=2,sort_keys=True,allow_nan=False)
    f.write("\n")

(OUT/"verification.json.sha256").write_text(
    sha(OUT/"verification.json")
    + "  verification.json\n"
)

print("F0F_VERIFY =",v["status"])
print(
    "CHECKS =",
    sum(checks.values()),"/",len(checks),
)
print(
    "VERIFICATION_SHA256 =",
    sha(OUT/"verification.json"),
)

if v["status"] == "HOLD":
    raise SystemExit(1)
