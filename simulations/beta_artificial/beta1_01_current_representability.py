"""BETA1-01 scientific runner.

Checks historical SHA-256 fingerprints, compares source-current
representability, and writes immutable JSON and SHA-256 sidecar.

Does not overwrite historical modules or results.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys

from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(
    0, str(ROOT/"src")
)

from antigravity_research.beta_artificial.beta1_01_current_representability import (
    report,
    Target,
)


DEPENDENCIES = {
    "M5I": (
        "src/antigravity_research/agminer/hook17_r3b_m5i_continuum_source.py",
        "ee3ff31e2068e2f6fc5c8bf46ee951e5b11098d24ba36d73e8f0e1f568f44a54",
    ),

    "M5V": (
        "src/antigravity_research/agminer/hook17_r3b_m5v_unified_exterior_action.py",
        "ea193cd163b2fc87e6973878c77e27c761f0625f6c5de3f38594587ef6cdb80f",
    ),

    "P10": (
        "src/antigravity_research/agminer/hook17_ph15_p10_free_space.py",
        "25e564a6dbbd4658f6154781db610738b8ed1114aa0f8fe71bf4ab91092fdddb",
    ),

    "P7": (
        "src/antigravity_research/agminer/hook17_ph15_p7_gauss_phase.py",
        "af2aa57c77232ce1cfd4832bdd859e0fc10a6a75a01fb7d784e221c0ee77da4c",
    ),

    "P1": (
        "src/antigravity_research/agminer/hook17_ph15_p1_theorem.py",
        "9ce430fa8a0e155ef330de27f1a8461c93a970385db4eeb53507c87253c07ca5",
    ),

    "BETA1-00": (
        "src/antigravity_research/beta_artificial/beta1_00_obstruction_atlas.py",
        "7088b754464d57da26b97ea9a42f486770c7eb0c6e6afcf78ab6d156acc119f6",
    ),

    "P10_JSON": (
        "results/data/032h17_ph15_p10_20261116T182301044331Z.json",
        "af59b072dba9a0424c569419af1f673172c3123a371eec8443e52cd81efc73c1",
    ),
}


def digest(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()


def run():
    provenance = {}

    for key, (rel, expected) in DEPENDENCIES.items():
        path = ROOT/rel

        actual = (
            digest(path)
            if path.is_file()
            else None
        )

        provenance[key] = {
            "path": rel,
            "expected_sha256": expected,
            "actual_sha256": actual,
            "status": (
                "MATCH"
                if actual == expected
                else "DRIFT_OR_MISSING"
            ),
        }

    bad = [
        key
        for key, row in provenance.items()
        if row["status"] != "MATCH"
    ]

    if bad:
        raise RuntimeError(
            "Historical fingerprint mismatch; "
            "no silent source substitutions: "
            +str(bad)
        )

    base = sorted(
        (ROOT/"results/data").glob(
            "beta1_00_*.json"
        )
    )

    if not base:
        raise RuntimeError(
            "BETA1-00 immutable baseline missing"
        )

    previous = base[-1]

    side = previous.with_suffix(
        ".json.sha256"
    )

    if (
        not side.is_file()
        or side.read_text().split()[0]
        != digest(previous)
    ):
        raise RuntimeError(
            "BETA1-00 JSON SHA sidecar failed"
        )

    previous_data = json.loads(
        previous.read_text()
    )

    if previous_data.get("primary_verdict") != (
        "YELLOW_EXACT_OBSTRUCTIONS_FULL_KINETIC_AND_EARTH_OPEN"
    ):
        raise RuntimeError(
            "BETA1-00 previous decision not recognized"
        )

    model = report(Target())

    now = datetime.now(timezone.utc)

    stamp = now.strftime(
        "%Y%m%dT%H%M%S%fZ"
    )

    doc = {
        "program": "BETA-1",
        "branch": "BETA1-01",

        "experiment":
            "TWO_CHANNEL_SOURCE_CURRENT_REALIZABILITY_AND_INDUCTION_OBSTRUCTIONS",

        "timestamp_utc":
            now.isoformat(),

        "model_class":
            "NECESSARY_CONDITION_DERIVED",

        "verdict":
            model["verdict"],

        "action_scope":
            "PH15 nonwinding X Maxwell scalar source "
            "and linear Y induction; "
            "no Earth/matter/gravity closure",

        "previous_BETA1_00": {
            "path":
                str(previous.relative_to(ROOT)),
            "sha256":
                digest(previous),
        },

        "parent_source_sha256":
            provenance,

        "source_sha256":
            digest(
                ROOT/
                "src/antigravity_research/beta_artificial/"
                "beta1_01_current_representability.py"
            ),

        "runner_sha256":
            digest(Path(__file__)),

        "independent_verifier_sha256":
            digest(
                ROOT/
                "tests/beta_artificial/"
                "test_beta1_01_current_representability.py"
            ),

        "scientific_results":
            model,

        "source_status":
            "M5I_ARTIFICIAL_NOT_MICROSCOPIC; "
            "PH15_P10_ONSHELL_X_DISCRETE",

        "reciprocity_status":
            "NOT_FULLY_SOLVED",

        "full_constraint_kinetics":
            "NOT_CERTIFIED",

        "Y_induction_matching":
            "CONDITIONAL_NUMERICAL_GEOMETRIC_OBSTRUCTION_FOR_M5I_PAIR_ONLY",

        "physical_P10_Y_channel":
            "PRESERVED",

        "source_energy_SI":
            "NOT_AVAILABLE",

        "earth_craft_force":
            "NOT_DERIVED",

        "whole_craft_reaction":
            "NOT_DERIVED",

        "complete_energy_SI":
            "NOT_AVAILABLE",

        "physical_transfer":
            "NOT_AUTHORIZED",

        "006D_replaced":
            False,

        "ALPHA1_M5V_frozen":
            True,

        "research_completion_heuristic":
            "UNCHANGED_APPROX_35_PERCENT",

        "next_physical_experiments": [
            "PH16: actual P10 source X/Y/scalar fully "
            "reciprocal perturbation and constrained "
            "kinetic characteristic matrix",

            "BETA-1A: evaluate source-current mismatches "
            "on conserved-charge and fixed-spin states, "
            "not arbitrary amplitude fits",

            "BETA1-02: derive passive causal neutral "
            "material response instead of M5V C2",
        ],
    }

    outfile = (
        ROOT/"results/data"/
        f"beta1_01_{stamp}.json"
    )

    encoded = (
        json.dumps(
            doc,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )+"\n"
    ).encode()

    with outfile.open("xb") as f:
        f.write(encoded)
        f.flush()
        os.fsync(f.fileno())

    checksum = hashlib.sha256(
        encoded
    ).hexdigest()

    with outfile.with_suffix(
        ".json.sha256"
    ).open("x") as f:
        f.write(
            f"{checksum}  {outfile.name}\n"
        )
        f.flush()
        os.fsync(f.fileno())

    print(
        "BETA1-01:",
        doc["verdict"]
    )

    print(
        "HISTORICAL_SHA_MATCH:",
        len(provenance),
        "/",
        len(DEPENDENCIES),
    )

    checks = model["exact_symbolic_checks"]

    print(
        "EXACT_ALGEBRA:",
        sum(checks.values()),
        "/",
        len(checks),
    )

    for row in model[
        "potential_interior_extremum_screens"
    ]:
        print(
            "POTENTIAL_SCREEN:",
            row["quadrature_order"],
            "margin=",
            row["interior_minus_boundary"],
            "jphi_at_interior=",
            row["interior_jphi_target"],
            "screen=",
            row["screen_pass"],
        )

    print(
        "M5I_SOURCE_TO_P10_X:",
        model["mechanism_status"][
            "M5I_direct_X_current_in_P10"
        ],
    )

    print(
        "M5I_PRESCRIBED_TO_Y:",
        model["mechanism_status"][
            "M5I_as_Y_from_M5I_RHO"
        ],
    )

    print(
        "PH15_P10_Y_PRESERVED:",
        model["mechanism_status"][
            "P10_original_induced_Y"
        ],
    )

    print(
        "RESULT_JSON:",
        outfile,
    )

    print(
        "SHA256:",
        checksum,
    )

    return outfile


if __name__ == "__main__":
    run()
