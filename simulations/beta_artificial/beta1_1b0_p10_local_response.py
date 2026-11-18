"""BETA1-1B0 immutable scientific runner with parent SHA protection."""

from __future__ import annotations

import hashlib
import json
import os
import sys

from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT/"src"))

from antigravity_research.beta_artificial.beta1_1b0_p10_local_response import (
    run_cases,
)


PARENTS = {
    "P10_source": (
        "src/antigravity_research/agminer/"
        "hook17_ph15_p10_free_space.py",
        "25e564a6dbbd4658f6154781db610738b8ed1114aa0f8fe71bf4ab91092fdddb",
    ),

    "P8_source": (
        "src/antigravity_research/agminer/"
        "hook17_ph15_p8_electric_dipole.py",
        "406aa58db3092d2392adbb78429257538fd51a202f472fd49b3a08862a934fed",
    ),

    "P10_JSON": (
        "results/data/"
        "032h17_ph15_p10_20261116T182301044331Z.json",
        "af59b072dba9a0424c569419af1f673172c3123a371eec8443e52cd81efc73c1",
    ),

    "BETA1_00_JSON": (
        "results/data/"
        "beta1_00_20261116T200742656266Z.json",
        "866a305e4d7618d174ff63e864a3d7054ffc9133284e0e5c3637dec89145f708",
    ),

    "BETA1_01_JSON": (
        "results/data/"
        "beta1_01_20261116T215749728579Z.json",
        "706856dd6e469911f1845415c48ab30485f9027f238620c69af895b97fbf1579",
    ),
}


def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()


def main():
    provenance = {}

    for label, (relative, expected) in PARENTS.items():
        path = ROOT/relative

        actual = (
            sha(path)
            if path.is_file()
            else None
        )

        if actual != expected:
            raise RuntimeError(
                f"{label} missing or SHA-256 drift: "
                f"{actual} expected {expected}"
            )

        provenance[label] = {
            "path": relative,
            "sha256": actual,
            "status": "MATCH",
        }

        if label.startswith("BETA1_"):
            sidecar = path.with_suffix(
                ".json.sha256"
            )

            if (
                not sidecar.is_file()
                or sidecar.read_text().split()[0] != actual
            ):
                raise RuntimeError(
                    "Prior BETA JSON sidecar mismatch: "+label
                )

    result = run_cases()

    if not all(result["gates"].values()):
        raise RuntimeError(
            "Scientific gate failure: "
            +str(result["gates"])
        )

    now = datetime.now(timezone.utc)

    stamp = now.strftime(
        "%Y%m%dT%H%M%S%fZ"
    )

    model = ROOT/(
        "src/antigravity_research/beta_artificial/"
        "beta1_1b0_p10_local_response.py"
    )

    tests = ROOT/(
        "tests/beta_artificial/"
        "test_beta1_1b0_p10_local_response.py"
    )

    doc = {
        "program": "BETA-1",
        "branch": "BETA1-1B0",

        "experiment":
            "P10_ACTUAL_SOURCE_MAGNETIC_Y_RITZ_"
            "AND_LOCAL_PHASE_SCHUR",

        "timestamp_utc": now.isoformat(),

        "classification": result["classification"],
        "verdict": result["verdict"],

        "parent_source_sha256": provenance,
        "source_sha256": sha(model),
        "runner_sha256": sha(__file__),
        "independent_verifier_sha256": sha(tests),

        "scoped_results": result,

        "gauge_constraint_scope":
            "B_Y=curl(A_Y_phi) divergence-free; "
            "alpha=0 implies lambda0=0, so X Gauss "
            "has no first-order magnetic-Y perturbation; "
            "full constraints not solved",

        "constrained_dynamic_stability": "NOT_CERTIFIED",
        "source_full_reciprocity": "NOT_SOLVED",
        "neutral_matter_earth_metric": "NOT_SOLVED",

        "earth_craft_force": "NOT_DERIVED",
        "whole_craft_reaction": "NOT_DERIVED",

        "source_energy_SI": "NOT_AVAILABLE",
        "complete_energy_SI": "NOT_AVAILABLE",

        "physical_transfer": "NOT_AUTHORIZED",

        "research_completion_heuristic":
            "UNCHANGED_APPROX_35_PERCENT",

        "006D_replaced": False,
        "ALPHA1_M5V_frozen": True,

        "next":
            "BETA1-1B1 complete dynamic gauge/phase "
            "constrained operator, then BETA1-02 passive "
            "neutral matter versus M5V C2",
    }

    destination = (
        ROOT/"results/data"/
        f"beta1_1b0_{stamp}.json"
    )

    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    encoded = (
        json.dumps(
            doc,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )+"\n"
    ).encode()

    with destination.open("xb") as stream:
        stream.write(encoded)
        stream.flush()
        os.fsync(stream.fileno())

    digest = hashlib.sha256(
        encoded
    ).hexdigest()

    sidecar = destination.with_suffix(
        ".json.sha256"
    )

    with sidecar.open("x") as stream:
        stream.write(
            f"{digest}  {destination.name}\n"
        )
        stream.flush()
        os.fsync(stream.fileno())

    print("BETA1-1B0:", doc["verdict"])
    print(
        "PARENT_SHA256:",
        len(provenance),
        "/",
        len(PARENTS),
        "MATCH",
    )
    print(
        "SCIENTIFIC_GATES:",
        sum(result["gates"].values()),
        "/",
        len(result["gates"]),
    )

    for name, case in result["cases"].items():
        print(
            "CASE", name,
            "beta_local_alpha0=",
            round(
                case["beta_thresholds_local"]["0.0"]["value"],
                6,
            ),
            "beta_Ritz_alpha0=",
            round(
                case["alpha0_Ritz_beta_critical_fixed_basis"],
                6,
            ),
            "Ritz_alpha0_beta100=",
            round(
                case["rayleigh_alpha0_beta100"]["minimum"],
                7,
            ),
            "Y_first_order=",
            round(
                case["Y_current_first_order_alpha1"],
                7,
            ),
            flush=True,
        )

    print("PH15_P10_SOURCE_PRESERVED: YES; RE-SOLVED")
    print("FULL_CONSTRAINED_PH16: OPEN")
    print("EARTH_FORCE: NOT_DERIVED")
    print("RESULT_JSON:", destination)
    print("SHA256:", digest)


if __name__ == "__main__":
    main()
