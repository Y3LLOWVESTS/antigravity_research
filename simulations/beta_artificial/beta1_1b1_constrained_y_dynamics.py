"""BETA1-1B1 immutable scientific runner with SHA-256 parent protection."""

from __future__ import annotations

import hashlib
import json
import os
import sys

from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/"src"))

from antigravity_research.beta_artificial.beta1_1b1_constrained_y_dynamics import (
    run_cases,
)

PARENTS = {
    "PH15_P10_SOURCE": (
        "src/antigravity_research/agminer/"
        "hook17_ph15_p10_free_space.py",
        "25e564a6dbbd4658f6154781db610738b8ed1114aa0f8fe71bf4ab91092fdddb",
    ),

    "PH15_P8_SOURCE": (
        "src/antigravity_research/agminer/"
        "hook17_ph15_p8_electric_dipole.py",
        "406aa58db3092d2392adbb78429257538fd51a202f472fd49b3a08862a934fed",
    ),

    "BETA1_1B0_SOURCE": (
        "src/antigravity_research/beta_artificial/"
        "beta1_1b0_p10_local_response.py",
        "a137d99b297891c7c1c901c0ebaafa96aa52df94fcd5b44dfb69d683f82a37c5",
    ),

    "BETA1_1B0_JSON": (
        "results/data/"
        "beta1_1b0_20261116T235042989026Z.json",
        "e60c13e66bacc77f38a3c97c390073151540132843ff1e22241936884a17fc0b",
    ),

    "BETA1_01_JSON": (
        "results/data/"
        "beta1_01_20261116T215749728579Z.json",
        "706856dd6e469911f1845415c48ab30485f9027f238620c69af895b97fbf1579",
    ),

    "PH15_P10_JSON": (
        "results/data/"
        "032h17_ph15_p10_20261116T182301044331Z.json",
        "af59b072dba9a0424c569419af1f673172c3123a371eec8443e52cd81efc73c1",
    ),
}


def sha256(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()


def main():
    parents = {}

    for name, (relative, expected) in PARENTS.items():
        path = ROOT/relative

        actual = (
            sha256(path)
            if path.is_file()
            else None
        )

        if actual != expected:
            raise RuntimeError(
                f"FAIL-CLOSED {name} fingerprint mismatch: "
                f"{actual}; expected {expected}"
            )

        if name.endswith("_JSON") and name.startswith("BETA1_"):
            sidecar = path.with_suffix(
                ".json.sha256"
            )

            if (
                not sidecar.is_file()
                or sidecar.read_text().split()[0] != actual
            ):
                raise RuntimeError(
                    "FAIL-CLOSED historical sidecar: "+name
                )

        parents[name] = {
            "path": relative,
            "sha256": actual,
            "status": "MATCH",
        }

    previous = json.loads(
        (ROOT/PARENTS["BETA1_1B0_JSON"][0]).read_text()
    )

    if previous.get("verdict") != (
        "YELLOW_ALPHA0_BETA100_DISCRETE_NEGATIVE_"
        "MAGNETIC_MODE_FULL_PH16_OPEN"
    ):
        raise RuntimeError(
            "Previous scientific verdict drift"
        )

    result = run_cases(
        previous["scoped_results"]["cases"]
    )

    if not all(result["gates"].values()):
        raise RuntimeError(
            "Scientific gate failure: "
            +str(result["gates"])
        )

    ts = datetime.now(timezone.utc)

    stamp = ts.strftime(
        "%Y%m%dT%H%M%S%fZ"
    )

    model = ROOT/(
        "src/antigravity_research/beta_artificial/"
        "beta1_1b1_constrained_y_dynamics.py"
    )

    tests = ROOT/(
        "tests/beta_artificial/"
        "test_beta1_1b1_constrained_y_dynamics.py"
    )

    doc = {
        "program": "BETA-1",
        "branch": "BETA1-1B1",

        "experiment":
            "ACTUAL_P10_ALPHA0_CONSTRAINED_Y_"
            "DYNAMIC_GRADIENT_OBSTRUCTION",

        "timestamp_utc": ts.isoformat(),

        "classification": result["classification"],
        "verdict": result["verdict"],

        "parent_source_sha256": parents,

        "source_sha256": sha256(model),
        "runner_sha256": sha256(__file__),

        "independent_verifier_sha256":
            sha256(tests),

        "scoped_results": result,

        "physical_alpha_nonzero_reciprocal_stability":
            "NOT_DERIVED",

        "source_full_reciprocity":
            "NOT_SOLVED",

        "physical_metric_neutral_Earth":
            "NOT_SOLVED",

        "whole_craft_reaction":
            "NOT_DERIVED",

        "earth_craft_force":
            "NOT_DERIVED",

        "neutral_payload_1kg_1g_1m":
            "NOT_CERTIFIED",

        "complete_energy_SI":
            "NOT_AVAILABLE",

        "physical_transfer":
            "NOT_AUTHORIZED",

        "006D_replaced": False,
        "ALPHA1_M5V_frozen": True,

        "research_completion_heuristic":
            "UNCHANGED_APPROX_35_PERCENT",
    }

    encoded = (
        json.dumps(
            doc,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )+"\n"
    ).encode()

    out = (
        ROOT/"results/data"/
        f"beta1_1b1_{stamp}.json"
    )

    out.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with out.open("xb") as stream:
        stream.write(encoded)
        stream.flush()
        os.fsync(stream.fileno())

    digest = hashlib.sha256(
        encoded
    ).hexdigest()

    sidecar = out.with_suffix(
        ".json.sha256"
    )

    with sidecar.open("x") as stream:
        stream.write(
            f"{digest}  {out.name}\n"
        )
        stream.flush()
        os.fsync(stream.fileno())

    print(
        "BETA1-1B1:",
        result["verdict"],
    )

    print(
        "PROVENANCE:",
        len(parents),
        "/",
        len(PARENTS),
        "MATCH",
    )

    checks = result["symbolic"]["checks"]

    print(
        "EXACT CHECKS:",
        sum(checks.values()),
        "/",
        len(checks),
    )

    print(
        "SCIENTIFIC GATES:",
        sum(result["gates"].values()),
        "/",
        len(result["gates"]),
    )

    for name, case in result["cases"].items():
        a = case["basis"]["legacy"]
        b = case["basis"]["dirichlet"]

        print(
            "CASE", name,

            "local_beta=",
            round(
                case["local_threshold_beta_alpha0"], 6
            ),

            "legacy_beta=",
            round(a["critical_beta"], 6),

            "dirichlet_beta=",
            round(b["critical_beta"], 6),

            "omega2_taper_beta100=",
            round(
                b["spectrum"]["100"][
                    "omega_squared_min"
                ], 6
            ),

            "gamma_taper=",
            round(
                b["spectrum"]["100"][
                    "max_growth_rate_canonical_inverse_time"
                ], 6
            ),

            flush=True,
        )

    print("GHOST_IN_TESTED_Y_CHANNEL: NO")
    print("RESTRICTED_GRADIENT_INSTABILITY_ALPHA0_BETA100: YES")
    print("ALPHA_NONZERO_ONSHELL_HEALTH: OPEN")
    print("EARTH_FORCE: NOT_DERIVED")
    print("RESULT_JSON:", out)
    print("SHA256:", digest)


if __name__ == "__main__":
    main()
