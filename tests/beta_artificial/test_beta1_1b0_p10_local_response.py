"""BETA1-1B0: 22 scoped symbolic and numerical research tests."""

from functools import lru_cache

from antigravity_research.beta_artificial.beta1_1b0_p10_local_response import (
    exact_variation,
    run_cases,
)


@lru_cache(maxsize=1)
def report():
    return run_cases()


def test_01_symbolic_double_variation():
    assert exact_variation()[
        "canonical_2phase_Schur_equals_H_BB"
    ]


def test_02_positive_potential_identity():
    assert exact_variation()[
        "U_polynomial_nonnegative_for_s>=0_gcontact>=0"
    ]


def test_03_beta0_structural_sign():
    assert exact_variation()[
        "beta0_alpha_any_nonnegative_source_curvature"
    ]


def test_04_source_eom_and_noether():
    assert report()["gates"]["source_eom_neutrality"]


def test_05_induced_Y_linear_alpha():
    assert report()["gates"]["PH15_first_order_Y_alpha_scaling"]


def test_06_beta0_maxwell_alpha0():
    assert report()["gates"]["alpha0_beta0_free_maxwell"]


def test_07_beta0_alpha1_phase_response():
    assert report()["gates"]["positive_beta0_all_grids"]


def test_08_beta100_local_negative():
    assert report()["gates"]["beta100_local_sign_change_all_grids"]


def test_09_alpha0_beta100_negative_ritz():
    assert report()["gates"]["alpha0_beta100_negative_ritz_all_grids"]


def test_10_alpha0_beta75_negative_refined():
    assert report()["gates"]["alpha0_beta75_negative_ritz_refined"]


def test_11_ritz_root_fixed_h_domain():
    assert report()["gates"][
        "alpha0_critical_Ritz_beta_fixed_h_domain_agreement"
    ]


def test_12_ritz_root_mesh_refinement():
    assert report()["gates"][
        "alpha0_critical_Ritz_beta_L16_grid_agreement"
    ]


def test_13_local_threshold_fixed_h_domain():
    assert report()["gates"][
        "fixed_h_domain_beta_threshold_rel_below_2pct"
    ]


def test_14_full_exponential_energy_fd():
    assert report()["gates"][
        "alpha0_beta100_finite_amplitude_H_matches"
    ]


def test_15_azimuthal_bianchi():
    assert report()["gates"]["alpha0_beta100_Bianchi"]


def test_16_phase_finite_difference():
    assert report()["gates"]["phase_fd_cross_check"]


def test_17_alpha0_beta100_odd_null():
    assert all(
        row["alpha0_beta100_full_exponential_H_fd"][
            "odd_energy_error"
        ] < 1e-8
        for row in report()["cases"].values()
    )


def test_18_critical_beta_positive_finite():
    assert all(
        50 < row[
            "alpha0_Ritz_beta_critical_fixed_basis"
        ] < 100
        for row in report()["cases"].values()
    )


def test_19_local_and_ritz_threshold_distinct():
    assert all(
        row["alpha0_Ritz_beta_critical_fixed_basis"]
        > row["beta_thresholds_local"]["0.0"]["value"]
        for row in report()["cases"].values()
    )


def test_20_on_source_K_U_control():
    assert all(
        row["K_plus_2U_min"] > 0
        and row["min_U"] >= 0
        for row in report()["cases"].values()
    )


def test_21_physical_claims_remain_open():
    result = report()

    assert result["physical_claim"] == (
        "NO_FULL_PH16_STABILITY_OR_EARTH_FORCE"
    )

    assert result["classification"] == (
        "NECESSARY_CONDITION_DERIVED"
    )


def test_22_modes_not_full_stability_proof():
    result = report()

    assert len(result["cases"]) == 5
    assert len(result["gates"]) == 13

    assert "global Noether" in " ".join(
        result["limitations"]
    )
