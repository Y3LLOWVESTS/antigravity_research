"""DELTA1-F0D: exact quadratic off-state obstruction; no source promotion.

SCOPE
-----
F0C's canonical frozen-trace quadratic source action, natural
polarization boundary, spherical R=2 support and arbitrary spatial
theta(E.B).

Construct an admissible divergence-free electric displacement and
B=0. The resulting energy is a trial upper bound, not a globally
optimized gravitational field.

All calculated energies are canonical quadratic quantities, NOT
complete operating energy in SI joules.

CLAIM
-----
A strictly negative admissible quadratic direction proves that the
unpolarized off state is not a local minimum within the specified
quadratic model. Nonlinear saturation, realistic material sources,
dynamical stability and gravitational lift are not established.
"""

import hashlib
import json
import math
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
from scipy.special import spherical_jn

OUT = Path(__file__).resolve().parent
PARENT = Path(os.environ["F0C_PARENT"]).resolve()

EXPECTED = {
    "science.json":
        "3c671e54a44a23bd12d2fe2451aed6388bb3c4f6da37408d7abe54c808540f7f",
    "f0c.py":
        "74850d49ec24251990f0fb0d8a5b55a1cd2a1ebe24e826699434fdefb6684ffc",
    "potentials.npz":
        "9e66b39e18f017a39e4f8ba1b9c9708b8a3fb97b1a4377ec81863f1e9805176f",
    "verify_nWI4IF/verification.json":
        "bafc1cf1d415e33a6da251fade2a29b1497d456f8d3aff5316d4b95936bbd9c6",
}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def require(condition, reason):
    if not condition:
        raise RuntimeError(reason)

def create(name, obj):
    raw = (
        json.dumps(obj, sort_keys=True, indent=2, allow_nan=False)
        + "\n"
    ).encode()

    with (OUT / name).open("xb") as stream:
        stream.write(raw)

    with (OUT / (name + ".sha256")).open("x") as stream:
        stream.write(
            digest(OUT / name) + "  " + name + "\n"
        )

started = time.perf_counter()

record = {
    "program":
        "DELTA1-F0D_QUADRATIC_OFFSTATE_STIFFNESS_OBSTRUCTION",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "producer_sha256": digest(Path(__file__)),
    "parents": {
        str(PARENT / k): v for k, v in EXPECTED.items()
    },
    "full_regression": "TO_BE_RUN_SEPARATELY_IN_VERIFY",
    "complete_energy": "UNDETERMINED_NOT_JOULES",
    "earth_craft": "NOT_DERIVED",
    "physical_source_mode": "NOT_SELECTED",
    "physical_payload_minimum": None,
    "exterior_metric_force": "NOT_DERIVED",
    "limitations": [
        "Frozen torus matter trace and prescribed theta profile",
        "Natural polarization boundary; Dirichlet changes trial space",
        "Exact quadratic model only; saturation is not specified",
        "Trial fields need not be the minimizing coupled solution",
        "Exterior electric dipole does not imply metric repulsion",
    ],
}

try:
    # Immutable F0C provenance.
    for name, value in EXPECTED.items():
        require(
            digest(PARENT / name) == value,
            "parent SHA mismatch: " + name,
        )

    parent = json.loads(
        (PARENT / "science.json").read_bytes()
    )
    verified = json.loads(
        (PARENT / "verify_nWI4IF/verification.json").read_bytes()
    )

    require(
        parent["status"]
        == "LOADED_AXIAL_TRIAL_COMPLETE_PHYSICAL_MODE_UNDERDETERMINED",
        "F0C scientific state",
    )
    require(
        verified["status"]
        == "PASS_SCOPED_TRIAL_AND_MODE_OBSTRUCTION",
        "F0C verification",
    )
    require(
        len(verified["checks"]) == 25
        and all(verified["checks"].values()),
        "F0C focused checks",
    )
    require(
        parent["energy"] == "ENERGY_UNDETERMINED",
        "energy claim",
    )
    require(
        parent["earth_craft"] == "NOT_DERIVED",
        "external force claim",
    )

    a = -0.35
    R = 2.0
    eta = 0.25

    require(
        math.isclose(
            parent["loaded_uniform_curvature_upper"],
            a + 1 / 3,
            abs_tol=1e-13,
        ),
        "F0C curvature baseline",
    )

    # ----------------------------------------------------------
    # A. Uniform axial polarization trial
    # ----------------------------------------------------------
    # P = A zhat inside the sphere.
    #
    # E_inside = -A zhat / 3.
    # E_outside is the ordinary exterior electric dipole.
    #
    # D = P + E, B = 0.
    #
    # div D = 0 and the normal component of D is continuous.
    # This field configuration is admissible for any theta(r,z).
    #
    # Canonical H:
    #
    # H = |D-P-theta*B|^2/2 + |B|^2/2
    #     + a|P|^2/2 + kappa|grad P|^2/2.
    #
    # The natural polarization boundary admits uniform P.
    # Its interior gradient stiffness cost vanishes.

    x, weight_x = np.polynomial.legendre.leggauss(32)
    u, weight_u = np.polynomial.legendre.leggauss(32)

    radial = (x + 1) / 2
    wr = weight_x / 2

    volume = 4 * math.pi * R**3 / 3

    inside = (
        math.pi * R**3 / 9
        * float(np.dot(wr, radial**2))
        * float(weight_u.sum())
    )

    outside = (
        math.pi * R**3 / 9
        * float(np.dot(wr, radial**2))
        * float(np.dot(weight_u, 1 + 3*u*u))
    )

    field = inside + outside
    curvature = a + 2 * field / volume

    require(
        abs(inside - volume/18) < 1e-12,
        "interior dipole quadrature",
    )
    require(
        abs(outside - volume/9) < 1e-12,
        "exterior dipole quadrature",
    )
    require(
        abs(curvature + 1/60) < 1e-12,
        "uniform negative-curvature direction",
    )

    kappa_grid = [
        0.0, 0.01, 0.1, 1.0, 10.0, 1e6,
    ]

    scan = [
        {
            "kappa_over_R2": k,
            "uniform_trial_curvature_upper": curvature,
            "uniform_trial_negative": curvature < 0,
        }
        for k in kappa_grid
    ]

    # ----------------------------------------------------------
    # B. Exterior-silent toroidal mode
    # ----------------------------------------------------------
    # P = j1(x1*r/R) * (zhat cross rhat)
    #
    # div P = 0
    # P.normal = 0
    # E = B = 0
    # D = P
    #
    # Natural boundary requires j1'(x1) = 0.
    # This mode has zero exterior carrier and metric response.

    root = brentq(
        lambda t: spherical_jn(1, t, derivative=True),
        2.0,
        2.2,
        xtol=1e-14,
    )

    f = spherical_jn(1, root*radial)
    df = (
        (root/R)
        * spherical_jn(1, root*radial, derivative=True)
    )

    mass = float(
        np.dot(
            wr,
            R**3 * radial**2 * f*f,
        )
    )

    grad = float(
        np.dot(
            wr,
            R * (
                R**2 * radial**2 * df*df
                + 2*f*f
            ),
        )
    )

    rayleigh = grad / mass
    spectral = (root/R)**2

    require(
        abs(rayleigh - spectral) < 1e-11,
        "toroidal Rayleigh integral",
    )
    require(
        abs(spherical_jn(1, root, derivative=True)) < 1e-13,
        "natural polarization boundary",
    )

    critical = -a / root**2

    phases = [
        {
            "kappa_over_R2": s * critical,
            "silent_curvature": a + s*critical*root**2,
            "uniform_curvature_upper": curvature,
            "silent_sign": (
                "NEGATIVE" if s < 1
                else "ZERO" if s == 1
                else "POSITIVE"
            ),
        }
        for s in (0, 0.5, 1, 2)
    ]

    # ----------------------------------------------------------
    # C. Claim-bounded decision
    # ----------------------------------------------------------

    record.update({
        "status":
            "SCOPED_QUADRATIC_OFFSTATE_UNSTABLE_ALL_NONNEGATIVE_STIFFNESS",

        "source_action": parent["action"],

        "assumed_parameters": {
            "a": a,
            "source_radius_m": R,
            "eta": eta,
            "boundary": "NATURAL_NEUMANN",
            "trace": "FROZEN",
        },

        "canonical_hamiltonian":
            "H=0.5*|D-P-theta*B|^2+0.5*|B|^2"
            "+0.5*a*|P|^2+0.5*kappa*|grad P|^2",

        "uniform_dipole_trial": {
            "field_energy_inside_per_A2": inside,
            "field_energy_outside_per_A2": outside,
            "field_energy_total_per_A2": field,
            "volume_m3": volume,
            "source_bare_energy_per_A2": a*volume/2,
            "total_trial_energy_per_A2":
                field + a*volume/2,
            "curvature_upper": curvature,
            "gradient_cost": 0,
            "admissibility":
                "div D=0; normal D continuous; "
                "B=0; natural source boundary",
            "metric_observable":
                "NOT_DETERMINED_BY_ELECTRIC_DIPOLE",
        },

        "kappa_grid": scan,

        "silent_mode": {
            "formula":
                "P=j1(x1*r/R)*(z_hat cross r_hat)",
            "divergence": "ZERO_ANALYTICALLY",
            "normal_component": "ZERO_ANALYTICALLY",
            "source_fields": "E=B=0, D=P",
            "exterior_metric": "ZERO",
            "root_j1prime": root,
            "rayleigh_numeric_per_m2": rayleigh,
            "rayleigh_exact_per_m2": spectral,
            "critical_kappa_over_R2": critical,
            "phases": phases,
        },

        "counterfactual_pinned_boundary":
            "UNIFORM_TRIAL_NOT_ADMISSIBLE; "
            "NO_GENERAL_STABILITY_CLAIM",

        "decision":
            "DO_NOT_SOLVE_NONLINEAR_PDE_UNTIL_"
            "SATURATING_SOURCE_ACTION_AND_BOUNDARY_SPECIFIED",

        "historical_loaded_minima": [
            float(row["minimum"])
            for row in parent["rows"]
            if row["case"] == "loaded"
        ],

        "theorem_scope":
            "NEGATIVE_RAYLEIGH_QUOTIENT_AT_P=0; "
            "NOT_NONLINEAR_OR_LORENTZIAN_STABILITY",
    })

except Exception as exc:
    record.update(
        status="HOLD",
        error=repr(exc),
    )

record["wall_s"] = time.perf_counter() - started

create("science.json", record)

print("F0D_STATUS =", record["status"])
print(
    "UNIFORM_CURVATURE_UPPER =",
    record.get("uniform_dipole_trial", {}).get(
        "curvature_upper"
    ),
)
print(
    "SILENT_KAPPA_CRIT/R2 =",
    record.get("silent_mode", {}).get(
        "critical_kappa_over_R2"
    ),
)
print(
    "SCIENCE_SHA256 =",
    digest(OUT / "science.json"),
)

if record["status"] == "HOLD":
    raise SystemExit(1)
