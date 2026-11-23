"""F0E: Necessary source-stability, boundary and switching gates.

MODEL
-----
F0D quadratic canonical polarization Hamiltonian, supplemented
conditionally by a nonnegative surface penalty gamma |P|²/2.

Two admissible perturbations are examined:
  1. Uniform axial polarization with an electrostatic dipole trial.
  2. Divergence-free toroidal polarization with zero carrier fields.

These are Rayleigh trial bounds, not the complete coupled spectrum.
A hypothetical Landau potential is examined algebraically, without
claiming a microscopic realization.

No SI operating energy, Einstein closure, or lift is inferred.
"""

import hashlib
import json
import math
import os
from datetime import datetime, timezone
from pathlib import Path

from scipy.optimize import brentq
from scipy.special import spherical_jn

OUT = Path(os.environ["F0E_RUN"]).resolve()
PARENT = Path(os.environ["F0D_PARENT"]).resolve()

EXPECTED = {
    "science.json":
        "2db67eea46adf84327c14c0177c1863148893217a377ac67a1f3a39ec9cb6465",
    "f0d.py":
        "4936c50e7819d3cd115740e416255782c174b14c96415514faf80e895fdc240c",
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def write_json(name, data):
    raw = (
        json.dumps(data, sort_keys=True, indent=2, allow_nan=False)
        + "\n"
    ).encode()
    with (OUT/name).open("xb") as f:
        f.write(raw)
    with (OUT/(name+".sha256")).open("x") as f:
        f.write(sha(OUT/name)+"  "+name+"\n")

def landau(c2, c4, c6):
    """Stationary amplitudes of V=c2*A²/2+c4*A⁴/4+c6*A⁶/6."""
    discriminant = c4*c4-4*c2*c6
    result = {
        "c2": c2, "c4": c4, "c6": c6,
        "discriminant": discriminant,
        "off_strict_local_minimum": c2 > 0,
    }
    if c6 <= 0 or c4 >= 0 or discriminant <= 0:
        result["classification"] = "NO_DOUBLE_WELL_BRANCH"
        return result

    x_minus = (-c4-math.sqrt(discriminant))/(2*c6)
    x_plus = (-c4+math.sqrt(discriminant))/(2*c6)

    if x_minus <= 0 or x_plus <= 0:
        result["classification"] = "NO_POSITIVE_DOUBLE_WELL"
        return result

    def potential(x):
        return c2*x/2+c4*x*x/4+c6*x*x*x/6

    on_energy = potential(x_plus)
    barrier = potential(x_minus)

    result.update({
        "x_unstable": x_minus,
        "x_stable_on": x_plus,
        "barrier_above_off": barrier,
        "on_energy_relative_off": on_energy,
        "on_second_derivative":
            c2+3*c4*x_plus+5*c6*x_plus*x_plus,
        "classification": (
            "BISTABLE_ON_GLOBALLY_FAVORED"
            if on_energy < 0 else
            "BISTABLE_OFF_GLOBALLY_FAVORED"
        ),
    })
    return result

result = {
    "program": "DELTA1_F0E_SOURCE_COMPLETION_NECESSARY_GATES",
    "utc": datetime.now(timezone.utc).isoformat(),
    "producer_sha256": sha(Path(__file__)),
    "parents": {
        str(PARENT/name): value
        for name, value in EXPECTED.items()
    },
    "full_regression": "NOT_RUN_SCOPED_ANALYTICAL_PREFLIGHT",
    "physical_source": "NOT_SPECIFIED",
    "complete_energy_j": None,
    "einstein_gravity": "NOT_DERIVED",
    "earth_craft_force": "NOT_DERIVED",
    "metric_lift": "NOT_CERTIFIED",
    "next": "CONDITIONAL_MICROPHYSICAL_SOURCE_ACTION_REQUIRED",
}

try:
    for name, expected in EXPECTED.items():
        require(
            sha(PARENT/name) == expected,
            "parent provenance mismatch: "+name,
        )

    parent = json.loads(
        (PARENT/"science.json").read_bytes()
    )

    require(
        parent["status"] ==
        "SCOPED_QUADRATIC_OFFSTATE_UNSTABLE_ALL_NONNEGATIVE_STIFFNESS",
        "F0D status mismatch",
    )

    a = float(parent["assumed_parameters"]["a"])
    R = float(parent["assumed_parameters"]["source_radius_m"])
    base = a+1/3

    require(abs(a+0.35) < 1e-13, "source a")
    require(abs(R-2) < 1e-13, "source R")
    require(
        abs(base-parent["uniform_dipole_trial"]["curvature_upper"])
        < 1e-12,
        "uniform field energy",
    )

    # gamma is a proposed surface cost, NOT an existing source
    # coefficient. g = gamma/R, k = kappa/R².
    #
    # Uniform trial:
    # lambda_u = a + 1/3 + 3*g.
    #
    # Toroidal trial:
    # lambda_t = a + x1²*k + Csurface*g.

    x1 = brentq(
        lambda x: spherical_jn(1,x,derivative=True),
        2, 2.2, xtol=1e-14,
    )

    j0 = spherical_jn(0,x1)
    j1 = spherical_jn(1,x1)
    j2 = spherical_jn(2,x1)

    radial_integral = (j1*j1-j0*j2)/2
    surface_ratio = j1*j1/radial_integral

    require(
        radial_integral > 0,
        "radial norm",
    )

    # Exact Bessel identity for this Neumann trial.
    require(
        abs(surface_ratio-2*x1*x1/(x1*x1-2))
        < 1e-11,
        "Bessel boundary identity",
    )

    gamma_min = -base/3
    kappa_silent_at_gamma_min = (
        -a-surface_ratio*gamma_min
    )/(x1*x1)

    gamma_silent_at_kappa_zero = -a/surface_ratio

    def trial(g,k):
        lu = base+3*g
        lt = a+x1*x1*k+surface_ratio*g
        return {
            "gamma_over_R": g,
            "kappa_over_R2": k,
            "uniform_curvature_upper": lu,
            "toroidal_curvature_upper": lt,
            "known_negative_trial": bool(lu < -1e-12 or lt < -1e-12),
            "other_modes": "NOT_TESTED",
        }

    cases = [
        trial(0,0),
        trial(0,1),
        trial(gamma_min,0),
        trial(gamma_min,kappa_silent_at_gamma_min),
        trial(0.10,0),
    ]

    require(
        all(x["known_negative_trial"] for x in cases[:3]),
        "negative controls",
    )
    require(
        not cases[3]["known_negative_trial"],
        "two-trial marginal point",
    )

    # Switching conditions.
    #
    # Positive quartic alone:
    # c2<0 -> unstable off state.
    # c2>0, c4>=0 -> no nonzero stable on state.
    #
    # A positive quadratic, negative quartic, positive sextic
    # can produce a bistable effective potential, but its
    # coefficients are not yet derived from source microphysics.

    examples = [
        landau(0.10,-1,1),
        landau(0.20,-1,1),
        landau(0.30,-1,1),
    ]

    require(
        examples[0]["classification"]
        == "BISTABLE_ON_GLOBALLY_FAVORED",
        "first-order example 1",
    )
    require(
        examples[1]["classification"]
        == "BISTABLE_OFF_GLOBALLY_FAVORED",
        "first-order example 2",
    )
    require(
        examples[2]["classification"]
        == "NO_DOUBLE_WELL_BRANCH",
        "no-on-state control",
    )

    result.update({
        "status": "NECESSARY_GATES_DERIVED_NO_PHYSICAL_PROMOTION",
        "scope": (
            "F0D quadratic trials plus hypothetical surface "
            "penalty and conditional polynomial switching models"
        ),
        "parameters": {
            "a": a,
            "R_m": R,
            "gamma": "UNSPECIFIED_SOURCE_PARAMETER",
            "kappa": "UNSPECIFIED_SOURCE_PARAMETER",
            "quartic": "UNSPECIFIED_SOURCE_PARAMETER",
            "sextic": "UNSPECIFIED_SOURCE_PARAMETER",
        },
        "uniform_trial": {
            "expression": "a+1/3+3*gamma/R",
            "minimum_gamma_over_R": gamma_min,
            "surface_required_to_remove_known_negative_direction":
                True,
            "stiffness_alone_suffices": False,
        },
        "toroidal_trial": {
            "root": x1,
            "surface_ratio": surface_ratio,
            "expression":
                "a+x1²*kappa/R²+Csurface*gamma/R",
            "minimum_kappa_over_R2_at_uniform_gamma_threshold":
                kappa_silent_at_gamma_min,
            "minimum_gamma_over_R_at_zero_kappa":
                gamma_silent_at_kappa_zero,
            "trial_only_for_nonzero_gamma": True,
        },
        "trial_cases": cases,
        "landau_examples": examples,
        "switching_theorems": {
            "positive_quartic_only":
                "CANNOT_PRODUCE_STRICTLY_STABLE_OFF_AND_NONZERO_ON",
            "negative_quartic_positive_sextic":
                "CONDITIONALLY_BISTABLE_IF_c2_POSITIVE_"
                "AND_c4_NEGATIVE_AND_c6_POSITIVE_"
                "AND_c4_SQUARED_GREATER_THAN_4_c2_c6",
            "microscopic_coefficients":
                "NOT_DERIVED",
        },
        "metric_observability": {
            "uniform_B_zero_trial": "E_DOT_B_ZERO",
            "toroidal_zero_field_trial": "E_DOT_B_ZERO",
            "actual_stationary_loaded_mode": "NOT_DERIVED",
            "warning":
                "Zero trial E.B does not prove that "
                "field-relaxed eigenmodes have zero E.B",
        },
        "scientific_decision":
            "NO_FURTHER_FIELD_AMPLITUDE_OPTIMIZATION_WITHOUT_"
            "PHYSICAL_BOUNDARY_AND_SATURATION_ACTION",
    })

except Exception as exc:
    result["status"] = "HOLD"
    result["error"] = repr(exc)

write_json("science.json",result)

print("F0E_STATUS =",result["status"])
if result["status"] != "HOLD":
    print(
        "UNIFORM_GAMMA_OVER_R_THRESHOLD =",
        gamma_min,
    )
    print(
        "TOROIDAL_KAPPA_OVER_R2_AT_THRESHOLD =",
        kappa_silent_at_gamma_min,
    )
    print(
        "TOROIDAL_GAMMA_OVER_R_AT_KAPPA_ZERO =",
        gamma_silent_at_kappa_zero,
    )
    print(
        "PHYSICAL_SOURCE =",
        result["physical_source"],
    )

print("SCIENCE_SHA256 =",sha(OUT/"science.json"))

if result["status"] == "HOLD":
    raise SystemExit(1)
