"""BETA1-1B1 independent kinetic, gauge, gradient and provenance tests."""

import json

from functools import lru_cache
from pathlib import Path

from antigravity_research.beta_artificial.beta1_1b1_constrained_y_dynamics import (
    exact_branch_theorems,
    run_cases,
)


@lru_cache(maxsize=1)
def report():
    root = Path(__file__).resolve().parents[2]

    prior = root/(
        "results/data/"
        "beta1_1b0_20261116T235042989026Z.json"
    )

    assert prior.is_file(), (
        "Frozen verified BETA1-1B0 JSON required"
    )

    data = json.loads(
        prior.read_text()
    )

    return run_cases(
        data["scoped_results"]["cases"]
    )


def test_01_action_checks_are_exact():
    checks = exact_branch_theorems()["checks"]

    assert len(checks) == 10
    assert all(checks.values())


def test_02_zero_y_stationarity():
    assert report()["symbolic"]["checks"][
        "zero_Y_stationary_alpha0"
    ]


def test_03_positive_electric_kinetic():
    assert report()["symbolic"]["checks"][
        "positive_electric_Y_kinetic"
    ]


def test_04_no_velocity_cross_at_alpha0():
    assert report()["symbolic"]["checks"][
        "electric_magnetic_velocity_cross_null"
    ]


def test_05_constitutive_lambda_exact():
    assert report()["symbolic"]["checks"][
        "lambda_linear_response"
    ]


def test_06_wave_parallel_E_is_maxwell():
    assert report()["symbolic"]["checks"][
        "wave_parallel_E_characteristic"
    ]


def test_07_wave_perpendicular_E_characteristic():
    assert report()["symbolic"]["checks"][
        "wave_perp_E_characteristic"
    ]


def test_08_source_EOM_and_charge():
    assert report()["gates"][
        "source_gauss_eom_all"
    ]


def test_09_first_order_Y_zero_at_alpha0():
    assert report()["gates"][
        "zero_alpha_Y_null"
    ]


def test_10_Kappa_nonnegative_sampled():
    assert report()["gates"][
        "Kappa_nonnegative_sampled"
    ]


def test_11_local_beta0_positive():
    assert report()["gates"][
        "beta0_local_positive"
    ]


def test_12_local_beta50_positive():
    assert report()["gates"][
        "beta50_local_positive"
    ]


def test_13_local_beta100_negative():
    assert report()["gates"][
        "beta100_local_negative"
    ]


def test_14_negative_inside_source():
    assert report()["gates"][
        "beta100_interior_negative"
    ]


def test_15_positive_kinetic_mass_all():
    assert report()["gates"][
        "alpha0_electric_kinetic_positive"
    ]


def test_16_beta0_positive_omega_squared():
    assert report()["gates"][
        "beta0_dynamic_positive"
    ]


def test_17_beta50_positive_omega_squared():
    assert report()["gates"][
        "beta50_dynamic_positive"
    ]


def test_18_beta75_negative_omega_squared():
    assert report()["gates"][
        "beta75_dynamic_negative"
    ]


def test_19_beta100_negative_omega_squared():
    assert report()["gates"][
        "beta100_dynamic_negative"
    ]


def test_20_both_basis_families_negative():
    assert report()["gates"][
        "both_bases_negative"
    ]


def test_21_Bianchi_and_Gauss():
    assert report()["gates"][
        "constraints_and_Bianchi"
    ]


def test_22_generalized_eigen_residual():
    assert report()["gates"][
        "eigen_residual_small"
    ]


def test_23_time_growth_matches_cosh():
    assert report()["gates"][
        "time_domain_growth_reproduced"
    ]


def test_24_signed_energy_ledger():
    assert report()["gates"][
        "time_domain_energy_ledger"
    ]


def test_25_parent_Ritz_threshold():
    assert report()["gates"][
        "parent_static_Ritz_threshold_consistent"
    ]


def test_26_fixed_h_domain_convergence():
    assert report()["gates"][
        "fixed_h_domain_growth_convergence"
    ]


def test_27_mesh_refinement_consistency():
    assert report()["gates"][
        "mesh_refinement_growth_consistency"
    ]


def test_28_all_21_gates_and_5_cases():
    result = report()

    assert len(result["gates"]) == 21
    assert len(result["cases"]) == 5
    assert all(result["gates"].values())


def test_29_boundary_taper_retains_negative_mode():
    assert all(
        c["basis"]["dirichlet"]["spectrum"]["100"][
            "negative_mode_count"
        ] >= 1
        for c in report()["cases"].values()
    )


def test_30_not_a_Y_ghost_claim():
    assert (
        "POSITIVE_MAXWELL_Y_TIME_KINETIC"
        in report()["gauge_conclusion"]
    )


def test_31_alpha_nonzero_still_open():
    result = report()

    assert "ALPHA_NONZERO" in result["stationarity"]

    assert result["physical_transfer"] == (
        "NOT_AUTHORIZED"
    )


def test_32_not_a_force_or_energy_result():
    result = report()

    limitations = "; ".join(
        result["limitations"]
    )

    assert (
        "No sourced neutral 1kg payload"
        in limitations
    )

    assert result["verdict"].startswith(
        "YELLOW_"
    )
