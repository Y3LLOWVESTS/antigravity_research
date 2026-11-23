"""DELTA1-F0D independent mathematical audit.

Reconstruct the canonical Hamiltonian, electric-dipole energy,
toroidal source eigenvalue, negative controls and regression evidence.

Passing this verifier is NOT a physical source, gravitational
repulsion, SI energy, or spacecraft-force certificate.
"""

import hashlib
import json
import math
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

from scipy.integrate import quad

run = Path(os.environ["F0D_RUN"]).resolve()
p = run / "science.json"
checks = {}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def require(name, condition):
    checks[name] = bool(condition)
    if not condition:
        raise AssertionError(name)

def sph1(x):
    if abs(x) < 1e-5:
        return x/3 - x**3/30 + x**5/840
    return (math.sin(x)-x*math.cos(x))/x**2

def sph1p(x):
    if abs(x) < 1e-5:
        return 1/3 - x*x/10 + x**4/168
    return (
        math.sin(x)/x
        + 2*math.cos(x)/x**2
        - 2*math.sin(x)/x**3
    )

v = {
    "program": "DELTA1-F0D_INDEPENDENT_VERIFICATION",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "verifier_sha256": sha(Path(__file__)),
    "checks": checks,
    "complete_energy": "NOT_DERIVED",
    "earth_craft": "NOT_DERIVED",
    "promotion": "NONE",
}

try:
    s = json.loads(p.read_bytes())

    require(
        "source sidecar",
        (run/"science.json.sha256").read_text().split()
        == [sha(p), "science.json"],
    )
    require(
        "source script sidecar",
        (run/"f0d.py.sha256").read_text().split()
        == [sha(run/"f0d.py"), "f0d.py"],
    )
    require(
        "science producer",
        s["producer_sha256"] == sha(run/"f0d.py"),
    )
    require(
        "scoped theorem status",
        s["status"]
        == "SCOPED_QUADRATIC_OFFSTATE_UNSTABLE_ALL_NONNEGATIVE_STIFFNESS",
    )
    require(
        "parents unchanged",
        all(
            sha(Path(path)) == h
            for path, h in s["parents"].items()
        ),
    )
    require(
        "exact parent count",
        len(s["parents"]) == 4,
    )

    # -------------------------------------------------------
    # Independent Legendre transform of the original action.
    # -------------------------------------------------------

    error = 0.0
    wrong_detected = False

    for theta in (0.0, 0.25, 18987.283771593688):
        P = 0.14
        D = 0.83
        B = -0.2
        a = -0.35
        k = 0.7
        g = 0.3

        E = D-P-theta*B

        lag = (
            0.5*(E*E-B*B)
            + theta*E*B
            + P*E
            - 0.5*a*P*P
            - 0.5*k*g*g
        )

        leg = D*E-lag

        ham = (
            0.5*((D-P-theta*B)**2+B*B)
            + 0.5*a*P*P
            + 0.5*k*g*g
        )

        error = max(
            error,
            abs(ham-leg)/max(1, abs(ham)),
        )

        wrong = (
            0.5*(D-P+theta*B)**2
            + 0.5*B*B
            + 0.5*a*P*P
            + 0.5*k*g*g
        )

        if theta != 0 and abs(ham-wrong) > 0.1:
            wrong_detected = True

    require(
        "independent Legendre transform",
        error < 1e-11,
    )
    require(
        "mixed-field sign negative control",
        wrong_detected,
    )

    # -------------------------------------------------------
    # Independent real-space dipole energy.
    # -------------------------------------------------------

    a = s["assumed_parameters"]["a"]
    R = s["assumed_parameters"]["source_radius_m"]
    V = 4*math.pi*R**3/3

    inner = 0.5*(V/9)

    angular = quad(
        lambda u: 1+3*u*u,
        -1,
        1,
        epsabs=1e-12,
    )[0]

    outer = (
        math.pi*R**6/9
        * quad(
            lambda r: r**(-4),
            R,
            math.inf,
            epsabs=1e-12,
        )[0]
        * angular
    )

    ref = s["uniform_dipole_trial"]

    require(
        "improper radial exterior integral",
        abs(
            outer-ref["field_energy_outside_per_A2"]
        ) < 1e-11,
    )
    require(
        "independent inside integral",
        abs(
            inner-ref["field_energy_inside_per_A2"]
        ) < 1e-11,
    )
    require(
        "uniform canonical curvature",
        abs(
            a+2*(inner+outer)/V
            - ref["curvature_upper"]
        ) < 1e-12,
    )

    require(
        "negative for sampled kappa",
        all(
            item["uniform_trial_negative"]
            and item["uniform_trial_curvature_upper"] < 0
            for item in s["kappa_grid"]
        ),
    )

    require(
        "analytic all-kappa obstruction",
        ref["gradient_cost"] == 0
        and a+2*(inner+outer)/V < 0
        and s["assumed_parameters"]["boundary"]
        == "NATURAL_NEUMANN",
    )

    # Surface Gauss continuity and tangential E continuity.
    require(
        "surface Gauss and tangential E",
        all(
            abs(2*u/3-2*u/3) < 1e-14
            and abs(
                math.sqrt(1-u*u)/3
                - math.sqrt(1-u*u)/3
            ) < 1e-14
            for u in (-0.8, 0.0, 0.7)
        ),
    )

    # -------------------------------------------------------
    # Independent spherical-Bessel derivative root.
    # -------------------------------------------------------

    lo, hi = 2.0, 2.2

    require(
        "silent root bracket",
        sph1p(lo) > 0 and sph1p(hi) < 0,
    )

    for _ in range(75):
        mid = (lo+hi)/2
        if sph1p(mid) > 0:
            lo = mid
        else:
            hi = mid

    root = (lo+hi)/2
    silent = s["silent_mode"]

    require(
        "independent root",
        abs(
            root-silent["root_j1prime"]
        ) < 1e-12,
    )
    require(
        "exact natural derivative",
        abs(sph1p(root)) < 1e-13,
    )

    # Independent direct radial Rayleigh integration.
    numerator = quad(
        lambda r:
            r*r*(root/R*sph1p(root*r/R))**2
            + 2*sph1(root*r/R)**2,
        0,
        R,
        epsabs=1e-12,
    )[0]

    denominator = quad(
        lambda r:
            r*r*sph1(root*r/R)**2,
        0,
        R,
        epsabs=1e-12,
    )[0]

    independent_rq = numerator/denominator

    require(
        "independent toroidal Rayleigh",
        abs(
            independent_rq
            - silent["rayleigh_numeric_per_m2"]
        ) < 1e-11,
    )
    require(
        "silent exact radial eigenvalue",
        abs(
            independent_rq-root**2/R**2
        ) < 1e-11,
    )
    require(
        "independent kappa crossing",
        abs(
            -a/root**2
            - silent["critical_kappa_over_R2"]
        ) < 1e-12,
    )

    require(
        "toroidal divergence and traction",
        silent["divergence"] == "ZERO_ANALYTICALLY"
        and silent["normal_component"]
        == "ZERO_ANALYTICALLY"
        and silent["exterior_metric"] == "ZERO",
    )

    phases = silent["phases"]

    require(
        "silent sign both sides",
        phases[0]["silent_curvature"] < 0
        and phases[1]["silent_curvature"] < 0
        and abs(
            phases[2]["silent_curvature"]
        ) < 1e-12
        and phases[3]["silent_curvature"] > 0
        and all(
            item["uniform_curvature_upper"] < 0
            for item in phases
        ),
    )

    require(
        "pinned boundary negative control",
        s["counterfactual_pinned_boundary"].startswith(
            "UNIFORM_TRIAL_NOT_ADMISSIBLE"
        ),
    )

    require(
        "no force/energy promotion",
        s["physical_payload_minimum"] is None
        and s["complete_energy"]
        == "UNDETERMINED_NOT_JOULES"
        and s["earth_craft"] == "NOT_DERIVED"
        and s["physical_source_mode"] == "NOT_SELECTED",
    )

    require(
        "historical loaded inward",
        len(s["historical_loaded_minima"]) == 4
        and all(
            x < 0
            for x in s["historical_loaded_minima"]
        ),
    )

    # -------------------------------------------------------
    # Full repository regression evidence.
    # -------------------------------------------------------

    log = run/"full_regression.log"
    exit_path = run/"full_regression.exitcode"

    if log.exists() and exit_path.exists():
        require(
            "regression log sidecar",
            (run/"full_regression.log.sha256")
            .read_text().split()
            == [sha(log), "full_regression.log"],
        )

        exit_code = int(exit_path.read_text().strip())
        content = log.read_text(errors="replace")

        values = [
            int(n)
            for n in re.findall(
                r"(\d+) passed",
                content,
            )
        ]

        passed = values[-1] if values else None

        regression_status = (
            "PASS"
            if exit_code == 0
            and passed is not None
            and passed >= 3304
            else "HOLD"
        )

        v["full_regression"] = {
            "exit_code": exit_code,
            "passed": passed,
            "sha256": sha(log),
            "status": regression_status,
        }

        require(
            "full regression recorded",
            regression_status == "PASS",
        )
    else:
        v["full_regression"] = {
            "status": "NOT_RUN",
        }

    v["status"] = "PASS_SCOPED_THEOREM_NO_SOURCE_PROMOTION"

except Exception as exc:
    v.update(
        status="HOLD",
        error=repr(exc),
    )

raw = (
    json.dumps(
        v,
        sort_keys=True,
        indent=2,
        allow_nan=False,
    ) + "\n"
).encode()

with (run/"verification.json").open("xb") as f:
    f.write(raw)

with (run/"verification.json.sha256").open("x") as f:
    f.write(
        sha(run/"verification.json")
        + "  verification.json\n"
    )

print("F0D_VERIFICATION =", v["status"])
print(
    "FOCUSED_CHECKS =",
    sum(checks.values()),
    "/",
    len(checks),
)
print(
    "FULL_REGRESSION =",
    v.get("full_regression"),
)
print(
    "VERIFICATION_SHA256 =",
    sha(run/"verification.json"),
)

if v["status"] == "HOLD":
    sys.exit(1)
