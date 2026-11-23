"""EPSILON1-02: auxiliary-source symmetry and spectral-mixing gate.

Scoped candidate action extension, not a complete gravity action:

L = -1/2 (df)^2 -1/2 m_f^2 f^2
    -1/2 (dchi)^2 -1/2 m_chi^2 chi^2
    +nu^2 f chi
    +g_chi chi (|Fplus|^2+|Fminus|^2)

Both f and chi are treated as pseudoscalars.
The density coupling explicitly violates parity.
It preserves separate Fplus/Fminus phase symmetries.

The model has canonicalized field normalizations.
No source coupling magnitude or source energy is derived.
The EPSILON1 global threshold is only a conditional
modewise screening benchmark, not a local no-go.
"""

import argparse
import cmath
import datetime
import hashlib
import json
import math
from pathlib import Path

PIN = (
    "adfa83e0171ba8102d82d275e4749ffa5ab951ab0b088"
    "686333055ebeb9ebd70"
)

CAP = 10_000_000.0
MF = 1.0

K_LIST = (0.0, 0.5, 1.0, 2.0, 5.0)
MCHI_LIST = (0.5, 1.0, 2.0, 4.0, 10.0, 100.0)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def controls():
    a = 1 + 2j
    b = 0.8 - 0.4j
    alpha = 0.23
    beta = 0.71

    ap = a * cmath.exp(1j * alpha)
    bp = b * cmath.exp(1j * beta)

    def rho(u, v):
        return abs(u)**2 + abs(v)**2

    assert math.isclose(
        rho(a, b), rho(ap, bp),
        rel_tol=1e-14
    )

    # The cross bilinear breaks the independent
    # phase symmetries, despite gauge neutrality.

    assert abs(ap * bp - a * b) > 0.1

    ag = a * cmath.exp(1j * alpha)
    bg = b * cmath.exp(-1j * alpha)

    assert abs(ag * bg - a * b) < 1e-14

    # Positive kinetic and mass mixing spectral bound.
    for m in MCHI_LIST:
        for k in K_LIST:
            s = MF*m / math.sqrt(
                (k*k+MF*MF)*(k*k+m*m)
            )
            bound = MF / math.hypot(k, MF)

            assert 0 < s <= 1+1e-12
            assert s <= bound+1e-13

    # Pseudoscalar chi times scalar density is
    # parity odd. This is a flagged physical cost,
    # not a reason to call the model a ghost.

    assert (-1)*(+1) == -1

    return {
        "separate_phase_density": "PASS",
        "cross_bilinear_noether_break": "PASS",
        "opposite_gauge_phase": "PASS",
        "spectral_upper_bounds": "PASS",
        "parity_violation_density_source": "PASS",
    }


def evaluate(parent):
    assert parent["experiment"] == (
        "EPSILON1-01-SOURCE-RANK-AND-NEAR-CRITICAL-GATE"
    )

    assert parent["parent_sha256"] == (
        "2840555051406416bcf4bfc9a8bc17f736d61a97e623"
        "f5019aa8dcbe39e23f16"
    )

    assert parent["physical_survivors"] == 0

    assert parent["parent_maxwell_continuum"] == (
        "NOT_CONVERGED"
    )

    ef = float(parent["parent_ephi_j"])
    em = float(parent["parent_reference_em_j"])

    results = []

    for case in parent["cases"]:
        gamma = float(case["gamma_deficit"])
        D = float(case["D_required"])

        denominator = (
            (CAP-em)/ef-D+2*gamma
        )

        assert denominator > 0

        threshold = (
            gamma/math.sqrt(denominator)
        )

        assert 0 < threshold < 1

        # Equal scalar mass and arbitrary auxiliary mass
        # limiting modewise cutoff estimates.

        k_equal = MF*math.sqrt(
            1/threshold-1
        )

        k_any_mass = MF*math.sqrt(
            1/(threshold*threshold)-1
        )

        scans = []

        for k in K_LIST:
            upper = MF/math.hypot(k, MF)

            mass_cases = []

            for mchi in MCHI_LIST:
                ceiling = MF*mchi/math.sqrt(
                    (k*k+MF*MF)
                    *(k*k+mchi*mchi)
                )

                mass_cases.append({
                    "mchi_inverse_range_per_m": mchi,
                    "modewise_mixing_strict_upper":
                        ceiling,
                    "can_exceed_global_optimistic_threshold_in_this_mode":
                        ceiling > threshold,
                })

            scans.append({
                "k_inverse_m": k,
                "absolute_modewise_healthy_upper":
                    upper,
                "cannot_reach_threshold_even_with_unbounded_mchi":
                    upper <= threshold,
                "mass_cases": mass_cases,
            })

        s08 = next(
            row for row in case["s_scan"]
            if row["s"] == 0.8
        )

        results.append({
            "box_m": case["box_m"],
            "h_m": case["h_m"],
            "ell_max": case["ell_max"],
            "unconverged_projection_r":
                case[
                    "r_loaded_observed_unconverged"
                ],
            "independent_drive_j_required_at_s_0p8":
                s08[
                    "required_independent_source_j_over_2Ef"
                ],
            "global_optimistic_quadratic_energy_threshold_s":
                threshold,
            "equal_masses_modewise_cutoff_k_inverse_m":
                k_equal,
            "any_aux_mass_modewise_cutoff_k_inverse_m":
                k_any_mass,
            "k_scan": scans,
        })

    return {
        "experiment":
            "EPSILON1-02-COVARIANT-SOURCE-SYMMETRY-AND-SPECTRAL-MIXING-GATE",
        "candidate_covariant_extension":
            "L=-1/2(df)^2-m_f^2*f^2/2"
            "-1/2(dchi)^2-m_chi^2*chi^2/2"
            "+nu^2*f*chi"
            "+g_chi*chi*(abs(Fplus)^2+abs(Fminus)^2)",
        "canonicalized_mf_inverse_range_per_m": MF,
        "healthy_quadratic_condition":
            "abs(nu_squared)<m_f*m_chi"
            " with positive kinetic terms",
        "exact_modewise_s_k":
            "abs(nu_squared)/sqrt("
            "(k^2+m_f^2)*(k^2+m_chi^2))",
        "source_operators": [
            {
                "name": "charged_scalar_density",
                "operator":
                    "chi*(abs(Fplus)^2+abs(Fminus)^2)",
                "separate_noether":
                    "PRESERVED_AT_OPERATOR_LEVEL",
                "X_gauge":
                    "PRESERVED_AT_OPERATOR_LEVEL",
                "parity":
                    "VIOLATED_IF_CHI_PSEUDOSCALAR",
                "physical_source":
                    "CONDITIONAL_NEEDS_FULL_SOURCE_EOM_AND_COUPLING",
            },
            {
                "name": "dirac_pseudoscalar",
                "operator":
                    "chi*(i*bar(Psi)*gamma5*Psi)",
                "fermion_number":
                    "PRESERVED_AT_OPERATOR_LEVEL",
                "parity": "PRESERVED",
                "physical_source":
                    "CONDITIONAL_NEEDS_POLARIZED_SOURCE_AND_ENERGY",
            },
            {
                "name": "same_maxwell_pseudoscalar",
                "operator": "chi*(F_X wedge F_Y)",
                "X_Y_gauge":
                    "PRESERVED_AT_OPERATOR_LEVEL",
                "independent_source":
                    "NOT_ESTABLISHED_SHARED_EXISTING_CARRIER",
            },
            {
                "name": "cross_bilinear_scalar",
                "operator": "chi*Im(Fplus*Fminus)",
                "X_gauge":
                    "PRESERVED_FOR_OPPOSITE_X_CHARGES",
                "separate_noether":
                    "BROKEN_UNLESS_ADDITIONAL_SYMMETRY_COMPENSATORS",
            },
        ],
        "interpretation":
            "The EPSILON1-00 mixing threshold is GLOBAL. "
            "Modewise comparison is a CONDITIONAL screen, "
            "not a no-go without the actual Fourier spectrum.",
        "actual_mismatch_spectrum": "NOT_AVAILABLE",
        "source_coupling_magnitude": "NOT_DERIVED",
        "source_charges_and_backreaction": "NOT_DERIVED",
        "full_action_including_original_X_Y_matter_metric_Earth_support":
            "NOT_DERIVED",
        "physical_source_survivors": 0,
        "gravitational_survivors": 0,
        "full_regression": "NOT_RUN",
        "controls": controls(),
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

    if digest(parent_raw) != PIN:
        raise RuntimeError(
            "IMMUTABLE_PARENT_SHA_MISMATCH"
        )

    report = evaluate(
        json.loads(parent_raw)
    )

    report["parent_sha256"] = PIN
    report["producer_sha256"] = digest(
        Path(__file__).read_bytes()
    )
    report["created_utc"] = (
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
            report,
            sort_keys=True,
            indent=2,
            allow_nan=False,
        )+"\n"
    ).encode()

    with (args.out/"science.json").open("xb") as f:
        f.write(raw)

    (args.out/"science.json.sha256").write_text(
        digest(raw)+"  science.json\n"
    )

    print("EPSILON1_02_PARENT_SHA=PASS")

    for name, value in report["controls"].items():
        print("CONTROL", name, value)

    for row in report["cases"]:
        print(
            "CASE",
            row["box_m"],
            row["h_m"],
            row["ell_max"],
            "THRESHOLD_GLOBAL",
            row[
                "global_optimistic_quadratic_energy_threshold_s"
            ],
            "K_CUTOFF_EQUAL",
            row[
                "equal_masses_modewise_cutoff_k_inverse_m"
            ],
            "K_CUTOFF_ANY_MCHI",
            row[
                "any_aux_mass_modewise_cutoff_k_inverse_m"
            ],
            "J_AT_S0.8",
            row[
                "independent_drive_j_required_at_s_0p8"
            ],
        )

    print("EPSILON1_02_PHYSICAL_SURVIVORS=0")
    print("EPSILON1_02_CERTIFICATION=NOT_ESTABLISHED")
    print("FULL_REGRESSION=NOT_RUN")
    print("SCIENCE_SHA256="+digest(raw))


if __name__ == "__main__":
    main()
