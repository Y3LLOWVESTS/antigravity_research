"""Independent F0E necessary-condition verification."""

import hashlib
import json
import math
import os
import sys
from pathlib import Path

from scipy.integrate import quad

run = Path(os.environ["F0E_RUN"]).resolve()
s = json.loads((run/"science.json").read_bytes())
checks = {}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check(name, ok):
    checks[name] = bool(ok)
    if not ok:
        raise AssertionError(name)

def j1(x):
    return math.sin(x)/x**2-math.cos(x)/x

def j1prime(x):
    return (
        math.sin(x)/x
        +2*math.cos(x)/x**2
        -2*math.sin(x)/x**3
    )

def potential(c2,c4,c6,x):
    return c2*x/2+c4*x*x/4+c6*x*x*x/6

v = {
    "program": "F0E_INDEPENDENT_VERIFICATION",
    "checks": checks,
    "verifier_sha256": sha(Path(__file__)),
    "full_regression": "NOT_RUN",
    "physical_source": "NOT_CERTIFIED",
    "earth_craft": "NOT_DERIVED",
    "complete_energy": "NOT_DERIVED",
}

try:
    check(
        "science sidecar",
        (run/"science.json.sha256").read_text().split()
        == [sha(run/"science.json"),"science.json"],
    )

    check(
        "producer source hash",
        s["producer_sha256"]==sha(run/"f0e.py"),
    )

    check(
        "parents immutable",
        all(
            sha(Path(path))==h
            for path,h in s["parents"].items()
        ),
    )

    check(
        "original F0D scope",
        s["status"]
        == "NECESSARY_GATES_DERIVED_NO_PHYSICAL_PROMOTION",
    )

    a=s["parameters"]["a"]
    R=s["parameters"]["R_m"]
    uniform=s["uniform_trial"]
    toroidal=s["toroidal_trial"]

    # Reconstruct uniform dipole from electrostatic energy.
    V=4*math.pi*R**3/3
    inside=V/18

    angular=quad(
        lambda u: 1+3*u*u,-1,1
    )[0]

    outside=(
        math.pi*R**6/9
        *quad(lambda r:r**(-4),R,math.inf)[0]
        *angular
    )

    base=a+2*(inside+outside)/V

    check(
        "independent dipole curvature",
        abs(base+1/60)<1e-12,
    )

    gamma=-base/3

    check(
        "independent surface threshold",
        abs(gamma-uniform["minimum_gamma_over_R"])
        <1e-12,
    )

    check(
        "stiffness alone cannot remove uniform direction",
        base<0 and
        s["uniform_trial"]["stiffness_alone_suffices"]
        is False,
    )

    # Independent root via direct trigonometric bisection.
    lo,hi=2.0,2.2
    for _ in range(75):
        mid=(lo+hi)/2
        if j1prime(mid)>0:
            lo=mid
        else:
            hi=mid
    root=(lo+hi)/2

    check(
        "independent toroidal root",
        abs(root-toroidal["root"])<1e-12,
    )

    # Numerical radial integral, independent of the
    # closed Bessel normalization identity in APPLY.
    radial=quad(
        lambda u:u*u*j1(root*u)**2,
        0,1,
        epsabs=1e-13,
    )[0]

    surface=j1(root)**2/radial

    check(
        "independent surface Rayleigh ratio",
        abs(surface-toroidal["surface_ratio"])<1e-11,
    )

    kappa=(-a-surface*gamma)/(root*root)

    check(
        "independent silent threshold",
        abs(
            kappa-
            toroidal[
                "minimum_kappa_over_R2_at_uniform_gamma_threshold"
            ]
        )<1e-11,
    )

    check(
        "zero stiffness surface threshold",
        abs(
            -a/surface-
            toroidal["minimum_gamma_over_R_at_zero_kappa"]
        )<1e-11,
    )

    # Recheck each Rayleigh trial without reading stored signs.
    for i,row in enumerate(s["trial_cases"]):
        g=row["gamma_over_R"]
        k=row["kappa_over_R2"]

        lu=base+3*g
        lt=a+root*root*k+surface*g

        check(
            "trial_%d_uniform"%i,
            abs(lu-row["uniform_curvature_upper"])<1e-11,
        )
        check(
            "trial_%d_toroidal"%i,
            abs(lt-row["toroidal_curvature_upper"])<1e-11,
        )

    # Verify illustrative Landau stationary roots directly.
    for i,row in enumerate(s["landau_examples"]):
        c2,c4,c6=row["c2"],row["c4"],row["c6"]
        delta=c4*c4-4*c2*c6

        check(
            "landau_%d_discriminant"%i,
            abs(delta-row["discriminant"])<1e-12,
        )

        if "x_stable_on" in row:
            x=row["x_stable_on"]
            xu=row["x_unstable"]

            check(
                "landau_%d_stationarity"%i,
                abs(c2+c4*x+c6*x*x)<1e-12,
            )
            check(
                "landau_%d_positive_on_curvature"%i,
                c2+3*c4*x+5*c6*x*x>0,
            )
            check(
                "landau_%d_barrier"%i,
                potential(c2,c4,c6,xu)>0,
            )
            check(
                "landau_%d_energy"%i,
                abs(
                    potential(c2,c4,c6,x)
                    -row["on_energy_relative_off"]
                )<1e-12,
            )

    check(
        "no automatic exterior promotion",
        s["metric_observability"]["actual_stationary_loaded_mode"]
        =="NOT_DERIVED",
    )

    check(
        "no gravitational force or energy promotion",
        s["physical_source"]=="NOT_SPECIFIED"
        and s["complete_energy_j"] is None
        and s["earth_craft_force"]=="NOT_DERIVED",
    )

    check(
        "no full regression claim",
        s["full_regression"]
        =="NOT_RUN_SCOPED_ANALYTICAL_PREFLIGHT",
    )

    v["status"]="PASS_SCOPED_NECESSARY_GATES_ONLY"

except Exception as exc:
    v["status"]="HOLD"
    v["error"]=repr(exc)

raw=(json.dumps(v,indent=2,sort_keys=True)+"\n").encode()

with (run/"verification.json").open("xb") as f:
    f.write(raw)

with (run/"verification.json.sha256").open("x") as f:
    f.write(
        sha(run/"verification.json")
        +"  verification.json\n"
    )

print("F0E_VERIFICATION =",v["status"])
print(
    "FOCUSED_CHECKS =",
    sum(checks.values()),"/",len(checks),
)
print(
    "VERIFICATION_SHA256 =",
    sha(run/"verification.json"),
)

if v["status"]!="PASS_SCOPED_NECESSARY_GATES_ONLY":
    sys.exit(1)
