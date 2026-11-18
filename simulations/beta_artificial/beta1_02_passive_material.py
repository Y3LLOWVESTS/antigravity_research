"""BETA1-02 immutable scientific runner with historical SHA protection."""

from __future__ import annotations

import hashlib
import json
import os
import sys

from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT/"src"))

from antigravity_research.beta_artificial.beta1_02_passive_material import (
    summarize,
)


PARENTS = {
    "M5T_MATERIAL_C2": (
        "src/antigravity_research/agminer/"
        "hook17_r3b_m5t_variational_cell_material.py",
        "7b613fc98d3d7247483ea1f0dcb89e492131e46d3f7f549097d73a98cc41ffa5",
    ),

    "M5V_FROZEN_ACTION": (
        "src/antigravity_research/agminer/"
        "hook17_r3b_m5v_unified_exterior_action.py",
        "ea193cd163b2fc87e6973878c77e27c761f0625f6c5de3f38594587ef6cdb80f",
    ),

    "PH11_UNIVERSAL_METRIC": (
        "src/antigravity_research/agminer/"
        "hook17_ph11_universal_metric_support_gate.py",
        "03e2f18b9d382f7503a41735cf3a709930952a37b60d0bb2b13f7aef281280ba",
    ),

    "BETA1_1B1_JSON": (
        "results/data/beta1_1b1_20261117T001913743770Z.json",
        "1468220d56a8555207f3f7e7960880636bc0ccb88bc344ad0d748e5e61a91b11",
    ),

    "BETA1_1B0_JSON": (
        "results/data/beta1_1b0_20261116T235042989026Z.json",
        "e60c13e66bacc77f38a3c97c390073151540132843ff1e22241936884a17fc0b",
    ),

    "PH15_P10_SOURCE": (
        "src/antigravity_research/agminer/"
        "hook17_ph15_p10_free_space.py",
        "25e564a6dbbd4658f6154781db610738b8ed1114aa0f8fe71bf4ab91092fdddb",
    ),

    "BETA1_01_JSON": (
        "results/data/beta1_01_20261116T215749728579Z.json",
        "706856dd6e469911f1845415c48ab30485f9027f238620c69af895b97fbf1579",
    ),
}


def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()


def main():
    parents = {}

    for name, (relative, expected) in PARENTS.items():
        path = ROOT/relative

        actual = (
            sha(path)
            if path.is_file()
            else None
        )

        if actual != expected:
            raise RuntimeError(
                "FAIL_CLOSED historical parent SHA mismatch: "
                +name+" "+str(actual)
            )

        if name.startswith("BETA1_"):
            sidecar = path.with_suffix(
                ".json.sha256"
            )

            if (
                not sidecar.is_file()
                or sidecar.read_text().split()[0] != actual
            ):
                raise RuntimeError(
                    "FAIL_CLOSED historical sidecar: "
                    +name
                )

        parents[name] = {
            "path": relative,
            "expected_sha256": expected,
            "actual_sha256": actual,
            "status": "MATCH",
        }

    predecessor = json.loads(
        (
            ROOT/PARENTS["BETA1_1B1_JSON"][0]
        ).read_text()
    )

    assert predecessor["verdict"] == (
        "YELLOW_ALPHA0_CONSTRAINED_Y_GRADIENT_"
        "INSTABILITY_BETA100_NONZERO_ALPHA_OPEN"
    )

    result = summarize()

    if not all(result["gates"].values()):
        raise RuntimeError(
            "FAIL_CLOSED BETA1-02 gates: "
            +str({
                k: v
                for k, v in result["gates"].items()
                if not v
            })
        )

    now = datetime.now(timezone.utc)

    stamp = now.strftime(
        "%Y%m%dT%H%M%S%fZ"
    )

    module = ROOT/(
        "src/antigravity_research/beta_artificial/"
        "beta1_02_passive_material.py"
    )

    verifier = ROOT/(
        "tests/beta_artificial/"
        "test_beta1_02_passive_material.py"
    )

    doc = {
        "program": "BETA-1",
        "branch": "BETA1-02",

        "experiment":
            "PASSIVE_CAUSAL_ACTION_DERIVED_"
            "NEUTRAL_INTERFACE_VS_M5V_C2",

        "timestamp_utc":
            now.isoformat(),

        "classification":
            "EXACT_CONDITIONAL_INTERFACE_THEOREM_"
            "AND_FINITE_PASSIVE_TOY_WITNESS",

        "primary_verdict":
            result["primary_verdict"],

        "source_sha256":
            sha(module),

        "runner_sha256":
            sha(__file__),

        "independent_verifier_sha256":
            sha(verifier),

        "parent_source_sha256":
            parents,

        "scoped_results":
            result,

        "neutral_material_action":
            "TOY_ORDER_PARAMETER_WITH_EXPLICIT_"
            "PINNING_AND_FINITE_BATH",

        "Earth_material_number_density":
            "NOT_DERIVED",

        "M5V_C2_as_exact_stationary_interface":
            "OBSTRUCTED_ONLY_IN_TESTED_PHI4_ACTION_CLASS",

        "M5V_C2_as_coarse_grained_response":
            "NOT_EXCLUDED",

        "full_universal_metric_matter":
            "NOT_SOLVED",

        "complete_source_X_Y_metric_reciprocity":
            "NOT_SOLVED",

        "source_support_hull_earth_reaction":
            "NOT_DERIVED",

        "neutral_torus_1kg_1g_1m":
            "NOT_CERTIFIED",

        "whole_craft_force":
            "NOT_DERIVED",

        "complete_energy_SI":
            "NOT_AVAILABLE",

        "physical_transfer":
            "NOT_AUTHORIZED",

        "ALPHA1_M5V_frozen":
            True,

        "006D_replaced":
            False,

        "research_completion_heuristic":
            "UNCHANGED_APPROX_35_PERCENT",

        "recommended_next":
            "BETA1-03 on-shell nonzero-alpha reciprocal "
            "source/X/Y; BETA1-04 exterior force "
            "and support Ward preflight",
    }

    encoded = (
        json.dumps(
            doc,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )+"\n"
    ).encode()

    outfile = (
        ROOT/"results/data"/
        f"beta1_02_{stamp}.json"
    )

    outfile.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with outfile.open("xb") as f:
        f.write(encoded)
        f.flush()
        os.fsync(f.fileno())

    digest = hashlib.sha256(
        encoded
    ).hexdigest()

    sidecar = outfile.with_suffix(
        ".json.sha256"
    )

    with sidecar.open("x") as f:
        f.write(
            f"{digest}  {outfile.name}\n"
        )
        f.flush()
        os.fsync(f.fileno())

    print(
        "BETA1-02:",
        doc["primary_verdict"],
    )

    print(
        "PARENTS:",
        len(parents),
        "/",
        len(PARENTS),
        "MATCH",
    )

    checks = result["theorems"]["checks"]
    gates = result["gates"]

    print(
        "SYMBOLIC:",
        sum(checks.values()),
        "/",
        len(checks),
    )

    print(
        "SCIENTIFIC GATES:",
        sum(gates.values()),
        "/",
        len(gates),
    )

    for key, row in result["kink_profiles"].items():
        print(
            "INTERFACE",
            "kappa="+key,
            "derived_ell=",
            round(row["ell_action"], 7),
            "C2_halfwidth=",
            round(
                row["slope_matched_C2_halfwidth"],
                7,
            ),
            "C2_EOM_residual=",
            round(
                row["C2_Euler_Lagrange_residual_L2"],
                7,
            ),
            "tail=",
            round(
                row["kink_tail_fraction_at_C2_edge"],
                8,
            ),
        )

    print(
        "CROSS_VARIATION_ERROR:",
        result["same_action_cross_variation"][
            "abs_error"
        ],
    )

    print(
        "CYCLE_WORK:",
        result["time_cycle"]["external_work"],
    )

    print(
        "CYCLE_STORED_ENERGY:",
        result["time_cycle"]["final_energy"],
    )

    print("PASSIVE_TOY_WITNESS: YES")
    print("EARTH_CRAFT_FORCE: NOT_DERIVED")
    print("006D_REPLACED: NO")
    print("RESULT_JSON:", outfile)
    print("SHA256:", digest)


if __name__ == "__main__":
    main()
