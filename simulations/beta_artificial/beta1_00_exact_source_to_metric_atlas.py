"""BETA1-00 scientific runner and immutable provenance writer.

Runs the symbolic obstruction preflight, checks available historical
source fingerprints, and writes a new timestamped JSON/SHA-256 pair.

Historical source files and research results are never modified.
"""

import hashlib
import json
import os
import sys

from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT / "src"))

from antigravity_research.beta_artificial.beta1_00_obstruction_atlas import (
    scientific_atlas,
    exact_checks,
    gap_atlas,
)


REFERENCES = {
    "ph15_p10_source": (
        "src/antigravity_research/agminer/"
        "hook17_ph15_p10_free_space.py",
        "25e564a6dbbd4658f6154781db610738b8ed1114aa0f8fe71bf4ab91092fdddb",
    ),
    "ph15_p1_source": (
        "src/antigravity_research/agminer/"
        "hook17_ph15_p1_theorem.py",
        "9ce430fa8a0e155ef330de27f1a8461c93a970385db4eeb53507c87253c07ca5",
    ),
    "ph15_p8_source": (
        "src/antigravity_research/agminer/"
        "hook17_ph15_p8_electric_dipole.py",
        "406aa58db3092d2392adbb78429257538fd51a202f472fd49b3a08862a934fed",
    ),
    "ph11_source": (
        "src/antigravity_research/agminer/"
        "hook17_ph11_universal_metric_support_gate.py",
        "03e2f18b9d382f7503a41735cf3a709930952a37b60d0bb2b13f7aef281280ba",
    ),
    "m5v_frozen_source": (
        "src/antigravity_research/agminer/"
        "hook17_r3b_m5v_unified_exterior_action.py",
        "ea193cd163b2fc87e6973878c77e27c761f0625f6c5de3f38594587ef6cdb80f",
    ),
}


def sha256(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()


def run():
    checks = exact_checks()

    if not all(checks.values()):
        raise RuntimeError(
            f"BETA1-00 exact check failed: {checks}"
        )

    parents = {}

    for key, (relative, expected) in REFERENCES.items():
        path = ROOT / relative

        actual = sha256(path) if path.is_file() else None

        parents[key] = {
            "path": relative,
            "sha256": actual,
            "bundle_expected_sha256": expected,
            "status": (
                "MATCH"
                if actual == expected
                else (
                    "MISSING"
                    if actual is None
                    else "DIFFERENT_FROM_UPLOADED_BUNDLE"
                )
            ),
        }

    relative_json = (
        "results/data/"
        "032h17_ph15_p10_20261116T182301044331Z.json"
    )

    original = ROOT / relative_json

    parents["ph15_p10_reference_json"] = {
        "path": relative_json,
        "sha256": (
            sha256(original)
            if original.is_file()
            else None
        ),
        "status": (
            "PRESENT_NOT_EXTERNALLY_AUTHENTICATED"
            if original.is_file()
            else "NOT_MOUNTED"
        ),
    }

    now = datetime.now(timezone.utc)

    stamp = now.strftime(
        "%Y%m%dT%H%M%S%fZ"
    )

    doc = {
        "program": "BETA-1",
        "branch": "BETA1-00",
        "experiment": "EXACT_SOURCE_TO_METRIC_OBSTRUCTION_ATLAS",
        "timestamp_utc": now.isoformat(),

        "model_class": "NECESSARY_CONDITION_DERIVED",

        "primary_verdict":
            "YELLOW_EXACT_OBSTRUCTIONS_FULL_KINETIC_AND_EARTH_OPEN",

        "action_definition":
            "SEH[g]-1/4 int sqrt(-g)(FX^2+FY^2)"
            "+Ssource[psi,AX,e^(2sigma(P))g]"
            "+Sneutral[e^(2sigma(P))g]+Ssupport; "
            "sigma=alpha*P-beta*P^2, P=FX*dual(FY)/2",

        "sign_conventions":
            "(-,+,+,+); epsilon^(0123)=+1/sqrt(-g); "
            "FX_01=E, FY_23=B gives P=E*B",

        "units": "canonical dimensionless except symbolic c",

        "parent_source_sha256": parents,

        "source_sha256": sha256(
            ROOT /
            "src/antigravity_research/beta_artificial/"
            "beta1_00_obstruction_atlas.py"
        ),

        "runner_sha256": sha256(
            Path(__file__)
        ),

        "independent_verifier_sha256": sha256(
            ROOT /
            "tests/beta_artificial/"
            "test_beta1_00_obstruction_atlas.py"
        ),

        "exact_atlas": scientific_atlas(),

        "missing_physics_atlas": gap_atlas(),

        "source_status":
            "PH15_P10_X_SOURCE_DISCRETE_ONLY",

        "reciprocity_status":
            "EXACT_CONSTITUTIVE_VARIATIONS_NOT_FULL_SOLUTION",

        "constraint_status":
            "FULL_PROJECTED_PRINCIPAL_SYMBOL_NOT_CERTIFIED",

        "stability_status": "NOT_CERTIFIED",

        "exterior_status":
            "PH15_P10_FIRST_ORDER_Y_NOT_FULL_METRIC",

        "earth_craft_force": "NOT_DERIVED",

        "whole_craft_reaction": "NOT_DERIVED",

        "complete_energy_SI": "NOT_AVAILABLE",

        "physical_transfer": "NOT_AUTHORIZED",

        "006D_replaced": False,

        "ALPHA1_M5V_frozen": True,

        "research_completion_heuristic":
            "UNCHANGED_APPROX_35_PERCENT",

        "limitations": [
            "No full nonlinear reciprocal "
            "source-X-Y-neutral-metric-gravity solution",

            "No constrained kinetic spectrum, "
            "continuum certificate or real source/UV",

            "No SI payload, Earth reaction, "
            "complete energy or craft lift",

            "Historical 2,286 regressions are not "
            "reexecuted by this scientific runner",
        ],
    }

    target_dir = ROOT / "results/data"

    target_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    target = target_dir / f"beta1_00_{stamp}.json"

    encoded = (
        json.dumps(
            doc,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        ) + "\n"
    ).encode()

    # Exclusive creation protects historical artifacts.

    with target.open("xb") as f:
        f.write(encoded)
        f.flush()
        os.fsync(f.fileno())

    digest = hashlib.sha256(
        encoded
    ).hexdigest()

    sidecar = target.with_suffix(
        ".json.sha256"
    )

    with sidecar.open("x") as f:
        f.write(
            f"{digest}  {target.name}\n"
        )
        f.flush()
        os.fsync(f.fileno())

    print(
        "BETA1-00:",
        doc["primary_verdict"],
    )

    print(
        "EXACT_CHECKS:",
        f"{sum(checks.values())}/{len(checks)}",
    )

    print(
        "REFERENCE_HASHES:",
        {
            key: value["status"]
            for key, value in parents.items()
        },
    )

    print("RESULT_JSON:", target)
    print("SHA256:", digest)

    return target


if __name__ == "__main__":
    run()
