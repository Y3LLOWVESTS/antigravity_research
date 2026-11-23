"""G01-K: local quadratic shell-source response, not gravitational lift.

Hypothesis: a 2+1 worldvolume gauge field a, f=da, j_X=*f,
coupled through A_X wedge f and mixed f/F_Y kinetic terms.

Magnetic drive, complete Lorentzian source/support, gravitational
metric variation and neutral loading are NOT established.
"""
from __future__ import annotations

import hashlib
import json
import os
import secrets
import sys
import tarfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PARENT_ID = "g01jbf_20261121T213657Z_282a797e"
PARENT_REL = (
    Path("results/gravity2/g01j_bf_runs")
    / PARENT_ID / "science.json"
)
PARENT_SHA = (
    "ce57c05c45428548afe80175943cc256fac94212cbc1b0415ff8a73f6dbd6ce3"
)
BASE = ROOT / "results/gravity2/g01k_runs"
CAPACITY = 1.5429162116460216
INWARD = -129.67185782242464


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(obj):
    return (
        json.dumps(
            obj, indent=2, sort_keys=True, allow_nan=False
        ) + "\n"
    ).encode()


def write(path, obj):
    with path.open("xb") as f:
        f.write(encode(obj))
        f.flush()
        os.fsync(f.fileno())


def parent():
    path = ROOT / PARENT_REL

    if (
        not path.is_file()
        or path.is_symlink()
        or sha(path) != PARENT_SHA
    ):
        raise ValueError("G01J_PARENT_HASH_HOLD")

    result = json.loads(path.read_text())
    modes = result["modes"]

    if (
        result["R3B_prescribed_field_capacity_J"] != CAPACITY
        or result["R3B_loaded_inward_minimum_m_s2"] != INWARD
        or result["qualified_physical_survivors"] != 0
        or result["source_radius_m"] != 2.0
        or len(modes) != 12
        or [m["ell"] for m in modes] != list(range(1, 13))
    ):
        raise ValueError("R3B_PARENT_SCIENCE_HOLD")

    return result


def compute(source):
    R = source["source_radius_m"]

    # Canonical length-equivalent coefficients.
    # These are not independently measured material constants.
    K = R
    g = 2 * R
    H = 4.1 * R

    rows = []
    magnetic_energy = 0.0
    stabilizer_energy = 0.0
    combined_energy = 0.0
    max_error = 0.0
    min_determinant = float("inf")

    for mode in source["modes"]:
        ell = mode["ell"]
        b = mode["b_mode"]
        target_q = mode["surface_charge_mode"]
        weight = mode["basis_l2_area_weight"]

        # Harmonic bulk Maxwell Dirichlet-to-Neumann
        # electrostatic and magnetic exterior coefficients.
        A = R / (2 * ell + 1)
        M = R / (ell + 1)

        # Reduced quadratic source action:
        #
        # U = .5*(K+A)*q² + g*q*b
        #     + .5*(H+M)*b² - J*b
        #
        # The q equation gives:
        # q = -g*b/(K+A)
        #
        # The J equation identifies the magnetic
        # drive required to hold the chosen b.
        induced_q = -g * b / (K + A)
        drive = (H + M) * b + g * induced_q

        relative_error = (
            abs(induced_q - target_q)
            / max(1.0, abs(target_q))
        )

        determinant = (K + A) * (H + M) - g * g

        static_threshold = g*g / (K + A) - M

        bare_magnetic = 0.5 * weight * M * b*b
        extra_stabilizer = 0.5 * weight * H * b*b

        reduced_energy = weight * (
            0.5 * (K + A) * induced_q**2
            + g * induced_q * b
            + 0.5 * (H + M) * b*b
        )

        if (
            relative_error > 5e-13
            or determinant <= 0
            or H <= static_threshold
            or drive * b <= 0
        ):
            raise ValueError(
                "SOURCE_RESPONSE_OR_STATIC_HEALTH_FAIL"
            )

        magnetic_energy += bare_magnetic
        stabilizer_energy += extra_stabilizer
        combined_energy += reduced_energy

        max_error = max(max_error, relative_error)
        min_determinant = min(
            min_determinant, determinant
        )

        rows.append({
            "ell": ell,
            "required_q": target_q,
            "induced_q": induced_q,
            "q_relative_error": relative_error,
            "A_electrostatic": A,
            "M_magnetic_exterior": M,
            "required_drive_J_canonical": drive,
            "minimal_static_H": static_threshold,
            "static_H_over_M_threshold":
                static_threshold / M,
            "selected_H_over_M": H / M,
            "constrained_hessian_det": determinant,
            "bare_magnetic_energy_proxy": bare_magnetic,
            "stabilizer_energy_proxy": extra_stabilizer,
        })

    kinetic_determinant = K * H - g*g

    if kinetic_determinant <= 0:
        raise ValueError(
            "WORLDVOLUME_KINETIC_PREFILTER_FAIL"
        )

    return {
        "schema": "gravity2.g01k.local_gauge_shell.v1",
        "status":
            "PASS_SCOPED_LOCAL_STATIC_SOURCE_RESPONSE_NOT_GRAVITY",
        "parent": str(PARENT_REL),
        "parent_sha256": PARENT_SHA,
        "protected_R3B_capacity_J": CAPACITY,
        "historical_loaded_min_m_s2": INWARD,
        "action_scope":
            "HYPOTHETICAL_LOCAL_2PLUS1_WORLDVOLUME_QUADRATIC",
        "proposed_action":
            "S_shell = integral(A_X wedge f "
            "- K/2 f wedge star_h f "
            "- g f wedge star_h F_Y "
            "- H/2 F_Y wedge star_h F_Y); f=da",
        "K": K,
        "g": g,
        "H": H,
        "source_radius_m": R,
        "modes": rows,
        "max_q_relative_error": max_error,
        "min_constrained_static_hessian_det":
            min_determinant,
        "local_mixed_kinetic_det":
            kinetic_determinant,
        "stabilizer_to_bare_magnetic_energy_ratio":
            stabilizer_energy / magnetic_energy,
        "combined_reduced_to_bare_magnetic_energy_ratio":
            combined_energy / magnetic_energy,
        "mandatory_magnetic_drive":
            "DERIVED_REQUIRED_COEFFICIENTS_NOT_PHYSICALLY_SOURCED",
        "metric_variation": "NOT_DERIVED",
        "full_Lorentzian_health": "NOT_ESTABLISHED",
        "microscopic_source": "NOT_ESTABLISHED",
        "loaded_response":
            "HISTORICAL_INWARD_FAILURE_UNRESOLVED",
        "Einstein_gravity": "NOT_DERIVED",
        "Earth_whole_craft_force": "NOT_DERIVED",
        "complete_SI_energy": "NOT_CERTIFIED",
        "physical_survivors": 0,
        "replaced_006D": False,
        "next_gate":
            "SOURCE_Y_CURRENT_LORENTZIAN_HEALTH_MAGNETIC_DRIVE_"
            "LOADED_METRIC_EARTH_CRAFT",
    }


def main():
    if sys.flags.optimize:
        raise RuntimeError("PYTHON_OPTIMIZATION_NOT_ALLOWED")

    if BASE.is_symlink():
        raise RuntimeError("UNSAFE_RESULTS_BASE")

    BASE.mkdir(parents=True, exist_ok=True)

    rid = (
        datetime.now(timezone.utc).strftime(
            "g01k_%Y%m%dT%H%M%SZ_"
        ) + secrets.token_hex(4)
    )

    folder = BASE / rid
    folder.mkdir(mode=0o700)

    manifest = {
        "schema": "gravity2.g01k.manifest.v1",
        "run_id": rid,
        "parent_path": str(PARENT_REL),
        "parent_sha256": PARENT_SHA,
        "source_sha256": {
            name: sha(ROOT / "scripts" / name)
            for name in (
                "g01k_source_v1.py",
                "g01k_check_v1.py",
            )
        },
        "full_repository_regression": "SKIPPED",
    }

    write(folder / "manifest.json", manifest)

    status = "HOLD"
    science = None

    try:
        import g01k_check_v1 as checker

        original = parent()
        science = compute(original)

        write(folder / "science.json", science)

        verification = checker.review(
            science, original
        )

        verification["science_sha256"] = sha(
            folder / "science.json"
        )

        write(
            folder / "verification.json",
            verification
        )

        status = "PASS_SCOPED"

    except Exception as exc:
        write(
            folder / "hold.json",
            {"status": "HOLD", "error": repr(exc)}
        )
        print(
            "G01K_HOLD=" + repr(exc),
            file=sys.stderr,
        )

    names = sorted(
        p.name for p in folder.glob("*.json")
    )

    ledger = "".join(
        sha(folder / name) + "  " + name + "\n"
        for name in names
    )

    with (folder / "SHA256SUMS.txt").open("xb") as f:
        f.write(ledger.encode())

    archive = folder / (
        rid + "_UPLOAD.tar.gz"
    )

    with tarfile.open(
        archive, "x:gz"
    ) as bundle:
        for name in names + ["SHA256SUMS.txt"]:
            bundle.add(
                folder / name,
                arcname=rid + "/" + name,
            )

    print("G01K_RUN=" + rid)
    print("G01K_STATUS=" + status)

    if science is not None:
        print(
            "MAX_MODE_RECONSTRUCTION_ERROR="
            + str(science["max_q_relative_error"])
        )
        print(
            "MIN_STATIC_DETERMINANT="
            + str(science[
                "min_constrained_static_hessian_det"
            ])
        )
        print(
            "LOCAL_KINETIC_DETERMINANT="
            + str(science["local_mixed_kinetic_det"])
        )
        print(
            "Y_STABILIZER_MAGNETIC_ENERGY_RATIO="
            + str(science[
                "stabilizer_to_bare_magnetic_energy_ratio"
            ])
        )

    print("GRAVITATIONAL_LIFT=NOT_DERIVED")
    print("UPLOAD_ARCHIVE=" + str(archive))
    print("UPLOAD_SHA256=" + sha(archive))

    return 0 if status == "PASS_SCOPED" else 3


if __name__ == "__main__":
    raise SystemExit(main())
