"""EPSILON1-01: source demand and near-critical-mode gate.

One-mode mathematical model, not a physical solution.

E_bare = E_f*((1+delta)*x*x+y*y-2*s*x*y)
E_drive = -2*E_f*(r*x+j*y)

EOM:
  (1+delta)*x-s*y=r
  y-s*x=j

The recorded U3B projections are NOT continuum-converged.
An independent physical source producing j is NOT supplied.
"""

import argparse
import datetime
import hashlib
import json
import math

from pathlib import Path

PARENT_SHA = (
    "2840555051406416bcf4bfc9a8bc17f736d61a97e623"
    "f5019aa8dcbe39e23f16"
)

CAP_J = 10_000_000.0
S_VALUES = (0.7, 0.8, 0.9, 0.99)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def solve(D, s, r, j):
    det = D-s*s

    if det <= 0:
        raise ValueError("NONPOSITIVE_STATIC_HESSIAN")

    x = (r+s*j)/det
    y = (s*r+D*j)/det

    return x, y


def controls():
    assert solve(1, 0, 1, 0) == (1, 0)

    assert solve(
        1, 0.5, -.1, 0
    )[0] < 0

    assert abs(
        solve(
            1, math.sqrt(.9), .1, 0
        )[0]-1
    ) < 1e-13

    assert solve(1, .9, 0, 0)[0] == 0

    assert solve(1, .9, 0, .25)[0] > 0

    for D in (1.0, 1.00000149):
        for s in S_VALUES:
            r = .07
            gamma = D-r
            j = gamma/s-s

            x, y = solve(D, s, r, j)

            assert abs(x-1) < 3e-13
            assert abs(y-gamma/s) < 3e-13
            assert abs(D*x-s*y-r) < 3e-13
            assert abs(y-s*x-j) < 3e-13

    return 6


def evaluate(parent):
    if parent.get("experiment") != (
        "EPSILON1-00-HEALTHY-SCHUR-SOURCE-CONTROL-ATLAS"
    ):
        raise ValueError("PARENT_EXPERIMENT_DRIFT")

    if (
        parent.get("physical_survivors") != 0
        or parent.get("full_regression") != "NOT_RUN"
    ):
        raise ValueError("PARENT_CLAIM_DRIFT")

    if parent.get("parent_sha256") != (
        "5e29b2d389fee45ff4a3098b29f1ac3c8bd436cb678d9"
        "c8df2c24535e14450f5"
    ):
        raise ValueError("U4A_PARENT_DRIFT")

    ef = float(parent["ephi_u1_fixed_profile_j"])
    em = float(parent["reference_em_illustrative_j"])

    if not (0 < ef < CAP_J and em > 0):
        raise ValueError("ENERGY_REFERENCE_DRIFT")

    results = []

    for case in parent["cases"]:
        if case.get(
            "u4a_parent_maxwell_converged"
        ) is not False:
            raise ValueError("CONVERGENCE_SCOPE_DRIFT")

        r = float(case["source_projection_observed"])
        D = float(case["source_projection_required"])

        gamma = float(
            case["dimensionless_required_deficit_gamma"]
        )

        if not (
            D >= 1
            and gamma > 0
            and abs(gamma-(D-r)) < 2e-12
        ):
            raise ValueError("PARENT_RATIO_DRIFT")

        tuned_s2 = D-r

        tuned_s = (
            math.sqrt(tuned_s2)
            if 0 < tuned_s2 < 1
            else None
        )

        scans = []

        for s in S_VALUES:
            no_x, no_y = solve(D, s, r, 0)

            demanded_y = gamma/s
            demanded_j = demanded_y-s

            yes_x, yes_y = solve(
                D, s, r, demanded_j
            )

            if not (
                abs(yes_x-1) < 1e-11
                and abs(yes_y-demanded_y) < 1e-11
            ):
                raise ValueError("SOURCE_DEMAND_EOM_FAILURE")

            q = (
                demanded_j/r
                if abs(r) > 1e-14
                else None
            )

            quad = ef*(
                D+demanded_y**2
                -2*s*demanded_y
            )

            parent_quad = ef*(
                1+gamma**2/s**2-2*gamma
            )

            if not math.isclose(
                quad-parent_quad,
                ef*(D-1),
                rel_tol=1e-7,
                abs_tol=1e-7,
            ):
                raise ValueError("LOADING_ENERGY_DRIFT")

            disc = math.sqrt(
                (D-1)**2+4*s*s
            )

            lam_min = .5*(D+1-disc)
            lam_max = .5*(D+1+disc)

            scans.append({
                "s": s,
                "static_hessian_eigen_min": lam_min,
                "static_hessian_eigen_max": lam_max,
                "condition_number_mass_matrix":
                    lam_max/lam_min,
                "no_independent_source_x": no_x,
                "no_independent_source_y": no_y,
                "required_independent_source_j_over_2Ef":
                    demanded_j,
                "required_shared_invariant_q_j_over_r":
                    q,
                "auxiliary_y_for_x_equals_one":
                    demanded_y,
                "quadratic_energy_loaded_j": quad,
                "quadratic_plus_reference_EM_j":
                    quad+em,
                "optimistic_budget_headroom_j":
                    CAP_J-quad-em,
                "positive_static_modes": lam_min > 0,
            })

        tuned_condition = None

        if tuned_s is not None:
            disc = math.sqrt(
                (D-1)**2+4*tuned_s2
            )

            tuned_condition = (
                (D+1+disc)/(D+1-disc)
            )

        results.append({
            "box_m": case["box_m"],
            "h_m": case["grid_h_m"],
            "ell_max": case["ell_max"],
            "r_loaded_observed_unconverged": r,
            "D_required": D,
            "delta_loading": D-1,
            "gamma_deficit": gamma,
            "no_independent_source_tuned_s":
                tuned_s,
            "no_independent_source_tuned_health_margin_1_minus_s2":
                (1-tuned_s2)
                if tuned_s is not None
                else None,
            "no_independent_source_tuned_condition_number":
                tuned_condition,
            "s_scan": scans,
        })

    rsigns = [
        row["r_loaded_observed_unconverged"]
        for row in results
    ]

    mixed_signs = (
        any(r > 0 for r in rsigns)
        and any(r < 0 for r in rsigns)
    )

    return {
        "experiment":
            "EPSILON1-01-SOURCE-RANK-AND-NEAR-CRITICAL-GATE",
        "model":
            "one-mode canonical quadratic two-scalar toy",
        "derivation":
            "(1+delta)x-s*y=r; y-s*x=j",
        "fixed_co_source_cannot_match_sign_mixed_parent_trials":
            mixed_signs,
        "parent_maxwell_continuum":
            "NOT_CONVERGED",
        "independent_source_action":
            "NOT_SUPPLIED",
        "physical_source_provenance":
            "NOT_SUPPLIED",
        "Einstein_metric_earthcraft":
            "NOT_SOLVED",
        "complete_operating_energy":
            "NOT_ESTABLISHED",
        "parent_ephi_j": ef,
        "parent_reference_em_j": em,
        "physical_survivors": 0,
        "full_regression": "NOT_RUN",
        "controls_passed": controls(),
        "cases": results,
    }


def main():
    ap = argparse.ArgumentParser()

    ap.add_argument(
        "--parent", type=Path, required=True
    )

    ap.add_argument(
        "--out", type=Path, required=True
    )

    args = ap.parse_args()
    parent_raw = args.parent.read_bytes()

    if sha(parent_raw) != PARENT_SHA:
        raise ValueError(
            "IMMUTABLE_EPSILON1_00_PARENT_MISMATCH"
        )

    data = evaluate(json.loads(parent_raw))

    data["parent_sha256"] = PARENT_SHA
    data["producer_sha256"] = sha(
        Path(__file__).read_bytes()
    )

    data["created_utc"] = (
        datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat()
    )

    args.out.mkdir(
        parents=True,
        exist_ok=False,
    )

    raw = (
        json.dumps(
            data,
            sort_keys=True,
            indent=2,
            allow_nan=False,
        )+"\n"
    ).encode()

    with (args.out/"science.json").open("xb") as f:
        f.write(raw)

    (args.out/"science.json.sha256").write_text(
        sha(raw)+"  science.json\n"
    )

    print("EPSILON1_01_PARENT_SHA=PASS")
    print("EPSILON1_01_2X2_EOM_CONTROLS=PASS")

    print(
        "EPSILON1_01_SHARED_SOURCE_SIGN_GATE",
        data[
            "fixed_co_source_cannot_match_sign_mixed_parent_trials"
        ]
    )

    for row in data["cases"]:
        entry = next(
            x for x in row["s_scan"]
            if x["s"] == .8
        )

        print(
            "CASE",
            row["box_m"],
            row["h_m"],
            row["ell_max"],
            "R",
            row["r_loaded_observed_unconverged"],
            "S_NO_SOURCE",
            row["no_independent_source_tuned_s"],
            "J_AT_S0.8",
            entry[
                "required_independent_source_j_over_2Ef"
            ],
            "Q_SHARED_AT_S0.8",
            entry[
                "required_shared_invariant_q_j_over_r"
            ],
            "BUDGET_HEADROOM_J",
            entry["optimistic_budget_headroom_j"],
        )

    print("EPSILON1_01_PHYSICAL_SURVIVORS=0")
    print("FULL_REGRESSION=NOT_RUN")
    print("SCIENCE_SHA256="+sha(raw))


if __name__ == "__main__":
    main()
