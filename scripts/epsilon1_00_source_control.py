"""EPSILON1-00: healthy auxiliary-field source-control atlas.

SCIENTIFIC QUESTION
-------------------
Can a hypothetical independent pseudoscalar source
compensate G01-U4A's missing scalar-source projection
while preserving a positive coupled static Hessian?

ACTION
------
E[f,chi] =
  0.5 <f,A f> + 0.5 <chi,B chi>
  - <f,K chi> - <J_f,f> - <J_chi,chi>

A and B are positive self-adjoint operators.

Define:
  s = || A^(-1/2) K B^(-1/2) || < 1

For S=<f,A f> and D=<f,K chi>=gamma*S:

  <chi,B chi> >= gamma^2*S/s^2

With E_f=C*S/2:

  E_chi,bare >= gamma^2*E_f/s^2

Including the negative mixing contribution:

  E_quadratic >= E_f*(1+gamma^2/s^2-2*gamma)

ASSUMPTIONS
-----------
- Frozen U1 scalar reference.
- U4A projected source deficit.
- Positive quadratic Hessian, static only.
- Hypothetical additional dynamical pseudoscalar.
- No freely certified source current.
- No full local field equations.
- No Lorentzian mode certification.
- No Einstein or Earth/craft gravitational solution.
- No complete operating-energy certification.

The quadratic-energy bound is model-conditional.
It is not a general gravitational no-go.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math

from datetime import datetime, timezone
from pathlib import Path

U4A_SHA = (
    "5e29b2d389fee45ff4a3098b29f1ac3c8bd436cb678d9"
    "c8df2c24535e14450f5"
)

CAP_J = 10_000_000.0

S_GRID = (
    0.25,
    0.50,
    0.65,
    0.70,
    0.80,
    0.90,
    0.99,
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def evaluate(parent: dict) -> dict:
    assert parent["experiment"] == (
        "G01-U4A-SCALAR-STATIONARITY-ENERGY-GATE"
    )

    assert parent["physical_survivors"] == 0

    assert parent["Maxwell_convergence"] == (
        "HOLD_NONCONVERGED_PARENT"
    )

    science = parent["science"]

    energy = science["weak_feedback_energy"]

    ef = float(energy["scalar_energy_j"])

    em = float(
        energy["illustrative_em_reference_j"]
    )

    assert 0 < ef < CAP_J
    assert em > 0

    results = []

    for case in science["cases"]:
        p0 = float(
            case["reference_overlap_m"]
        )

        observed = float(
            case["measured_source_ratio"]
        )

        required = float(
            case["required_frozen_profile_ratio"]
        )

        gamma = required-observed

        assert p0 > 0
        assert gamma > 0

        assert math.isclose(
            gamma,
            case["projected_stationarity_gap"],
            abs_tol=1e-12,
        )

        deficit = gamma*p0

        denominator = (
            (CAP_J-em)/ef
            -1
            +2*gamma
        )

        minimum_s = (
            gamma/math.sqrt(denominator)
            if denominator > 0
            else None
        )

        scans = []

        for s in S_GRID:
            bare = ef*(gamma/s)**2

            interaction = -2*gamma*ef

            total = (
                ef+bare+interaction
            )

            if total < -1e-6:
                raise RuntimeError(
                    "POSITIVE_SCHUR_BOUND_VIOLATED"
                )

            scans.append({
                "schur_s": s,
                "health_margin_1_minus_s2":
                    1-s*s,
                "auxiliary_bare_energy_bound_j":
                    bare,
                "negative_interaction_energy_at_target_j":
                    interaction,
                "quadratic_coupled_energy_lower_bound_j":
                    total,
                "plus_reference_em_j":
                    total+em,
                "under_10MJ_optimistic_only":
                    total+em < CAP_J,
            })

        results.append({
            "box_m": case["box_m"],
            "grid_h_m": case["h_m"],
            "ell_max": max(case["ells"]),
            "u4a_parent_maxwell_converged":
                False,
            "source_projection_observed":
                observed,
            "source_projection_required":
                required,
            "dimensionless_required_deficit_gamma":
                gamma,
            "source_overlap_deficit_m":
                deficit,
            "unrestricted_auxiliary_bare_energy_infimum_j":
                ef*gamma*gamma,
            "minimum_s_to_fit_optimistic_10MJ_quadratic_plus_em":
                minimum_s,
            "scans": scans,
        })

    return {
        "experiment":
            "EPSILON1-00-HEALTHY-SCHUR-SOURCE-CONTROL-ATLAS",
        "ephi_u1_fixed_profile_j": ef,
        "reference_em_illustrative_j": em,
        "energy_cap_complete_j": CAP_J,
        "theorem":
            "For positive Hessian, "
            "s=||A^-1/2 K B^-1/2||<1 and "
            "|<f,K chi>|<=s sqrt(<f,Af><chi,Bchi>)",
        "assumptions": [
            "Same canonical scalar normalization as U1",
            "Frozen U1 scalar reference",
            "U4A projected deficit, not local EOM",
            "Positive static scalar Hessian",
            "Hypothetical dynamical pseudoscalar chi",
            "No source-material microphysics",
            "Illustrative reference Maxwell energy",
            "No full nonlinear or Einstein solution",
        ],
        "interpretation":
            "Necessary healthy quadratic control bounds "
            "only; negative interaction included; "
            "no complete energy certification",
        "physical_survivors": 0,
        "full_regression": "NOT_RUN",
        "cases": results,
    }


def main():
    ap = argparse.ArgumentParser()

    ap.add_argument(
        "--u4a", type=Path, required=True
    )

    ap.add_argument(
        "--out", type=Path, required=True
    )

    args = ap.parse_args()

    raw = args.u4a.read_bytes()

    if sha(raw) != U4A_SHA:
        raise RuntimeError(
            "IMMUTABLE_U4A_PARENT_SHA_MISMATCH"
        )

    report = evaluate(json.loads(raw))

    report["parent_sha256"] = U4A_SHA

    report["producer_sha256"] = sha(
        Path(__file__).read_bytes()
    )

    report["created_utc"] = (
        datetime.now(timezone.utc).isoformat()
    )

    args.out.mkdir(
        parents=True,
        exist_ok=False,
    )

    result = (
        json.dumps(
            report,
            sort_keys=True,
            indent=2,
            allow_nan=False,
        )+"\n"
    ).encode()

    with (
        args.out/"science.json"
    ).open("xb") as f:
        f.write(result)

    (
        args.out/"science.json.sha256"
    ).write_text(
        sha(result)+"  science.json\n"
    )

    print("EPSILON1_00_PARENT_SHA=PASS")

    for case in report["cases"]:
        print(
            "CASE",
            case["box_m"],
            case["grid_h_m"],
            case["ell_max"],
            "SOURCE_DEFICIT_GAMMA",
            case[
                "dimensionless_required_deficit_gamma"
            ],
            "MINIMUM_S_FOR_OPTIMISTIC_10MJ",
            case[
                "minimum_s_to_fit_optimistic_10MJ_quadratic_plus_em"
            ],
        )

    print("EPSILON1_00_PHYSICAL_SURVIVORS=0")
    print("FULL_REGRESSION=NOT_RUN")
    print("SCIENCE_SHA256="+sha(result))


if __name__ == "__main__":
    main()
