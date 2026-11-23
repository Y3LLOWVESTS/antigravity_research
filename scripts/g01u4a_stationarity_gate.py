"""G01-U4A: fixed-profile scalar stationarity gate.

ACTION / EQUATIONS
------------------
Inherited from G01-U1:

 (-Delta + mu^2 + delta_m2) f = P_loaded
 (-Delta + mu^2) f = P_reference

 delta_m2 = 8*pi*G*beta*rho_neutral/c^2

For the identical fixed scalar f at full amplitude:

 <f,P_loaded>/<f,P_reference>
     = 1 + <delta_m2*f^2>/<f,P_reference>

The baseline overlap must be positive.

MODEL LIMITS
------------
This is a necessary weak-form stationarity test.
It is not a local full scalar solve.

U3B Maxwell solutions have unresolved continuum
convergence. The surface source currents remain
prescribed. No Einstein/whole-craft solution exists.

The weak-feedback energy estimate assumes fixed
scalar profile, fixed shell field shapes, and
simultaneous rescaling of both Maxwell fields.

The canonical operator scale is dimensional and
convention-dependent, not a certified EFT cutoff.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math

from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from numpy.polynomial.legendre import leggauss
from scipy.integrate import trapezoid
from scipy.interpolate import PchipInterpolator

G = 6.67430e-11
C = 299792458.0
HBAR = 1.054571817e-34
EV = 1.602176634e-19

R = 2.0
R_MAJOR = 1.0
R_MINOR = 0.2
CENTER = 3.2
ENERGY_CAP = 10_000_000.0

PINS = {
    "u1": (
        "0f5b138a22d9da0088cdb9d6c2bfdcfbb046603845447"
        "d250878809c454616c3"
    ),
    "radial": (
        "cfe54027edcd6a33532faa5eec138455bc35a89193f9b3"
        "af1d4cd4f5bf727999"
    ),
    "u3b": (
        "44f14ce4ba14e46d3fd4816d9fad2395fd1fef133a358"
        "94e884ad8ace9335126"
    ),
    "producer_u3b": (
        "103416a4b816af2b4b6a586f135eb0dafc945e1a1c3734"
        "315afa6b3352c535ff"
    ),
}


def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()


def baseline_overlap(rgrid, f0, f2, limit):
    """Independent analytic P0/P2 source overlap."""

    def segment(a, b):
        middle = rgrid[
            (rgrid > a) & (rgrid < b)
        ]
        return np.r_[a, middle, b]

    inside = segment(float(rgrid[0]), R)
    outside = segment(R, limit)

    inner = trapezoid(
        inside**2*f0(inside)/(R*R),
        inside,
    )

    outer = trapezoid(
        -R**4/outside**4
        *(f0(outside)+f2(outside)/5),
        outside,
    )

    return float(4*math.pi*(inner+outer))


def torus_overlap(f0, f2, beta, nq=80, na=256):
    """Evaluate positive scalar loading on a smooth 1kg torus."""

    nodes, weights = leggauss(nq)

    q = (nodes+1)/2
    wq = weights/2

    angular = (
        2*math.pi*np.arange(na)/na
    )

    qq = q[:, None]
    aa = angular[None, :]

    rho = (
        R_MAJOR
        +R_MINOR*qq*np.cos(aa)
    )

    z = (
        math.sqrt(
            CENTER**2-R_MAJOR**2
        )
        +R_MINOR*qq*np.sin(aa)
    )

    radius = np.hypot(rho, z)
    mu = z/radius

    p2 = (3*mu*mu-1)/2

    scalar = (
        f0(radius)+f2(radius)*p2
    )

    shape = (
        (1-qq)**2*(1+2*qq)
    )

    volume = (
        3*math.pi**2
        *R_MAJOR*R_MINOR**2/5
    )

    weights3d = (
        2*math.pi*rho
        *R_MINOR**2
        *qq*shape
        *wq[:, None]
        *(2*math.pi/na)
        /volume
    )

    mass = float(np.sum(weights3d))

    if abs(mass-1) >= 1e-11:
        raise RuntimeError(
            "TORUS_MASS_NORMALIZATION_FAILED"
        )

    mean_f2 = float(
        np.sum(weights3d*scalar**2)
    )

    overlap = (
        8*math.pi*G*beta
        *mean_f2/(C*C)
    )

    return {
        "torus_mass_kg": mass,
        "smooth_shape_volume_m3": volume,
        "mass_averaged_f_squared": mean_f2,
        "matter_overlap_m": overlap,
        "nq": nq,
        "na": na,
    }


def evaluate(u1, radial_path, u3b):
    selected = u1["selected_conditional_law"]

    beta = float(
        selected["beta_dimensionless"]
    )

    amplitude = float(
        selected["source_axion_amplitude_A"]
    )

    kappa = float(
        selected[
            "source_kappa_m_per_J_assuming_illustrative_dipole_calibration"
        ]
    )

    scalar_energy = float(
        selected[
            "scalar_kinetic_and_mass_energy_j"
        ]
    )

    gradient_driver = float(
        selected[
            "Maxwell_reciprocal_loading_prefilter"
        ]["R_times_max_gradient_theta"]
    )

    if not (
        beta > 0
        and amplitude > 0
        and kappa > 0
        and gradient_driver > 0
        and 0 < scalar_energy < ENERGY_CAP
    ):
        raise RuntimeError(
            "PARENT_PHYSICAL_ASSUMPTIONS_CHANGED"
        )

    if (
        u1["physical_survivors"] != 0
        or u3b["physical_survivors"] != 0
    ):
        raise RuntimeError(
            "PARENT_CLAIM_DRIFT"
        )

    if (
        u3b["producer_sha256"]
        != PINS["producer_u3b"]
        or u3b["parent_u1_sha256"]
        != PINS["u1"]
        or u3b["parent_radial_sha256"]
        != PINS["radial"]
    ):
        raise RuntimeError(
            "U3B_PROVENANCE_DRIFT"
        )

    with np.load(
        radial_path,
        allow_pickle=False,
    ) as archive:
        r = np.asarray(
            archive["r"], float
        )
        f0_data = np.asarray(
            archive["f0"], float
        )
        f2_data = np.asarray(
            archive["f2"], float
        )
        mediator = float(
            archive["mu"]
        )

    if not (
        mediator == 1.0
        and r[0] < R
        and r[-1] > 80
        and np.all(np.diff(r) > 0)
    ):
        raise RuntimeError(
            "RADIAL_PARENT_GRID_CHANGED"
        )

    f0 = PchipInterpolator(r, f0_data)
    f2 = PchipInterpolator(r, f2_data)

    matter = torus_overlap(
        f0, f2, beta
    )

    second = torus_overlap(
        f0, f2, beta,
        nq=40,
        na=128,
    )

    relative_error = abs(
        matter["matter_overlap_m"]
        -second["matter_overlap_m"]
    )/max(
        matter["matter_overlap_m"],
        1e-30,
    )

    if relative_error > 5e-5:
        raise RuntimeError(
            "TORUS_QUADRATURE_NOT_CONVERGED"
        )

    results = []

    for case in u3b["results"]:
        full = case["full"]

        if (
            full["t"] != 1
            or full["constant_theta_null"]
        ):
            raise RuntimeError(
                "NOT_FULL_U3B_AMPLITUDE"
            )

        box = float(case["L"])

        reference = baseline_overlap(
            r, f0, f2, box
        )

        if reference <= 0:
            raise RuntimeError(
                "REFERENCE_OVERLAP_NOT_POSITIVE"
            )

        measured = float(
            full[
                "scalar_source_projection_ratio"
            ]
        )

        required = (
            1
            +matter["matter_overlap_m"]
            /reference
        )

        gap = required-measured

        results.append({
            "box_m": box,
            "h_m": case["h"],
            "ells": case["ells"],
            "reference_overlap_m": reference,
            "matter_overlap_m":
                matter["matter_overlap_m"],
            "measured_source_ratio": measured,
            "required_frozen_profile_ratio":
                required,
            "projected_stationarity_gap": gap,
            "stationarity": (
                "FAIL_IN_RECORDED_TRIAL"
                if abs(gap) > 0.01
                else "INCONCLUSIVE"
            ),
            "parent_maxwell_residual":
                full[
                    "static_maxwell_relative_residual"
                ],
            "maxwell_continuum":
                "NOT_CONVERGED",
        })

    if len(results) != 4:
        raise RuntimeError(
            "U3B_RESULT_COUNT_CHANGED"
        )

    # Fixed scalar and fixed shell shapes:
    # Maxwell energy scales as s.
    # E.B scales as s.
    # Maintaining phi requires kappa -> kappa/s.
    # Therefore |grad theta| scales as 1/s.

    em_reference = (
        6*math.pi*amplitude/kappa
    )

    weak_em = (
        em_reference*gradient_driver
    )

    conditional_total = (
        scalar_energy+weak_em
    )

    # Canonical dimensional normalization.
    # This is not a loop or UV-completion test.

    scalar_coefficient = (
        C**4/(8*math.pi*G)
    )

    theta_per_phi = (
        scalar_coefficient*kappa
    )

    operator_energy_scale_ev = (
        math.sqrt(
            scalar_coefficient*HBAR*C
        )
        /theta_per_phi/EV
    )

    return {
        "scalar_equation":
            "(-Delta+mu^2+8piG beta rho/c^2)f=P_loaded",
        "scope":
            "FROZEN_U1_F0_F2_SCALAR_PROFILE",
        "finite_torus": matter,
        "torus_relative_quadrature_error":
            relative_error,
        "cases": results,
        "weak_feedback_energy": {
            "illustrative_em_reference_j":
                em_reference,
            "scalar_energy_j":
                scalar_energy,
            "R_gradient_theta":
                gradient_driver,
            "em_for_Rgradienttheta_le_1_j":
                weak_em,
            "conditional_scalar_plus_em_j":
                conditional_total,
            "exceeds_10MJ": bool(
                conditional_total >= ENERGY_CAP
            ),
            "general_no_go": False,
        },
        "canonical_dimensional_estimate": {
            "scalar_coefficient_J_per_m":
                scalar_coefficient,
            "theta_per_dimensionless_phi":
                theta_per_phi,
            "operator_scale_eV":
                operator_energy_scale_ev,
            "UV_certified": False,
        },
    }


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--u1", type=Path, required=True
    )
    parser.add_argument(
        "--radial", type=Path, required=True
    )
    parser.add_argument(
        "--u3b", type=Path, required=True
    )
    parser.add_argument(
        "--out", type=Path, required=True
    )

    args = parser.parse_args()

    for label, path in (
        ("u1", args.u1),
        ("radial", args.radial),
        ("u3b", args.u3b),
    ):
        if sha(path) != PINS[label]:
            raise RuntimeError(
                label.upper()+"_SHA_LOCK_FAILED"
            )

    result = evaluate(
        json.loads(args.u1.read_text()),
        args.radial,
        json.loads(args.u3b.read_text()),
    )

    data = {
        "experiment":
            "G01-U4A-SCALAR-STATIONARITY-ENERGY-GATE",
        "created_utc":
            datetime.now(timezone.utc).isoformat(),
        "producer_sha256":
            sha(Path(__file__)),
        "parents_sha256": {
            k: PINS[k]
            for k in ("u1", "radial", "u3b")
        },
        "science": result,
        "physical_survivors": 0,
        "full_local_scalar_EOM":
            "NOT_SOLVED",
        "physical_source_current":
            "NOT_SOLVED",
        "Einstein_earthcraft":
            "NOT_SOLVED",
        "Maxwell_convergence":
            "HOLD_NONCONVERGED_PARENT",
        "claim":
            "FROZEN_U1_PROFILE_INCONSISTENT_WITH_RECORDED_U3B_TRIALS",
        "full_regression":
            "NOT_RUN",
    }

    out = args.out

    out.mkdir(
        parents=True,
        exist_ok=False,
    )

    raw = (
        json.dumps(
            data,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )+"\n"
    ).encode()

    with (out/"science.json").open("xb") as f:
        f.write(raw)

    digest = hashlib.sha256(raw).hexdigest()

    (out/"science.json.sha256").write_text(
        digest+"  science.json\n"
    )

    print("G01U4A_PARENT_HASHES=PASS")
    print("G01U4A_FINITE_TORUS_MASS=PASS")
    print("G01U4A_TORUS_QUADRATURE=PASS")

    for row in result["cases"]:
        print(
            "BOX", row["box_m"],
            "H", row["h_m"],
            "ELL_MAX", max(row["ells"]),
            "MEASURED", row["measured_source_ratio"],
            "REQUIRED",
                row["required_frozen_profile_ratio"],
            "GAP",
                row["projected_stationarity_gap"],
            "VERDICT", row["stationarity"],
            flush=True,
        )

    energy = result["weak_feedback_energy"]

    print(
        "CONDITIONAL_WEAK_FEEDBACK_TOTAL_J",
        energy["conditional_scalar_plus_em_j"]
    )

    print(
        "CANONICAL_OPERATOR_SCALE_EV",
        result[
            "canonical_dimensional_estimate"
        ]["operator_scale_eV"]
    )

    print("G01U4A_PHYSICAL_SURVIVORS=0")
    print("G01U4A_FULL_REGRESSION=NOT_RUN")
    print("SCIENCE_SHA256="+digest)


if __name__ == "__main__":
    main()
