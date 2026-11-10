"""R3X3B9 — algebraic-compensator reciprocity gate.

Carries forward R3X3B8 without interpreting the spherical
benchmark as a solution or no-go theorem for the toroidal payload.
"""
from __future__ import annotations

import json
from pathlib import Path

from antigravity_research.agminer.hook17_f2_strong_payload_loading_rescue import (
    primary_peak_loading_gate,
)
from antigravity_research.agminer.hook17_fdual_f_r3x3b9_reciprocity_gate import (
    result,
)


def prior_spherical_audit(path: Path) -> dict:
    if not path.is_file():
        return {
            "available": False,
            "scope": "NO_PRIOR_SPHERICAL_ARTIFACT",
        }

    prior = json.loads(path.read_text(encoding="utf-8"))

    if prior.get("branch") != "032H17A12D1R3X3B8":
        raise ValueError("R3X3B8 artifact branch mismatch")

    if prior.get("r3b_torus_no_go_proved") is not False:
        raise ValueError("Sphere/torus distinction not preserved")

    rows = [
        r for r in prior["modes"]
        if r["theta"] == 1e4
        and r["ell"] in (1, 10)
    ]

    if len(rows) != 2:
        raise ValueError("Missing R3X3B8 reference modes")

    return {
        "available": True,
        "theta_reference": 10000.0,
        "reference_transmission_norms": {
            str(r["ell"]): float(r["transfer_norm_max"])
            for r in rows
        },
        "torus_no_go_proved": False,
    }


def run(root: Path = Path(".")) -> dict:
    root = Path(root)
    summary = result()

    loading = primary_peak_loading_gate()
    theta_peak = float(loading["peak_epsilon_load"])

    summary["comparison_to_r3b"] = {
        "one_keV_peak_dimensionless_beta_magnitude": theta_peak,
        "sphere_uniform_amplitude_bound_at_matched_theta":
            3.0/(theta_peak - 3.0),
        "spherical_bound_applies_to_r3b_torus": False,
    }

    summary["r3x3b8_prior"] = prior_spherical_audit(
        root / "results/data/"
        "032h17a12d1r3x3b8_spherical_interface_screening_summary.json"
    )

    target = (
        root / "results/data/"
        "032h17a12d1r3x3b9_reciprocity_preflight_summary.json"
    )

    target.parent.mkdir(parents=True, exist_ok=True)

    target.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(
        "R3X3B9_ALGEBRAIC_RECIPROCITY_PASS=",
        summary["single_auxiliary"]["schur_complement_verified"],
    )
    print(
        "R3X3B9_TWO_AUXILIARY_PASS=",
        summary["two_auxiliary"][
            "two_auxiliary_schur_complement_verified"
        ],
    )
    print(
        "MIXED_FORCE_IF_EXACTLY_CANCELLED=",
        "ZERO_IN_SAME_LOCAL_CHANNEL",
    )
    print("R3B_PEAK_BETA_MAGNITUDE=", theta_peak)
    print("SPHERICAL_TORUS_NO_GO=", False)
    print(
        "R3X3B8_PROVENANCE_FOUND=",
        summary["r3x3b8_prior"]["available"],
    )
    print("R3X3B9_RESULT_PATH=", target)

    return summary


if __name__ == "__main__":
    run()
