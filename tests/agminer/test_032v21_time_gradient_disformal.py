"""Scientific regressions for 032V21 time-gradient disformal preflight."""

import math

from antigravity_research.agminer.storage import (
    Storage,
)
from antigravity_research.agminer.time_gradient_disformal import (
    LOOSE_OMEGA_STIFF_CEILING,
    acceleration_for_exponential_s2,
    canonical_background_energy,
    constant_gamma_direct_lapse_gradient,
    critical_energy_density_j_m3,
    disformal_invertibility,
    empirical_k_cap,
    material_kinetic_factors,
    minimum_q2_for_derivative_ratio,
    minimum_q2_for_metric_invertibility,
    persist_v21_failure_rule,
    required_s2_for_exponential_acceleration,
    spherical_exponential_gradient_energy_j,
    stationary_q_integrability,
    anisotropic_finite_slab_pressure_pa,
)


AU_DENSITY = 19300.0

SEPARATION_M = 200.0e-9
SPHERE_AU_M = 180.0e-9
PLATE_AU_M = 210.0e-9

ALLOWED_EXTRA_PA = 0.00764

TARGET_A = 9.80665
H = 0.10

EXPECTED_K_CAP = 4.6371917187e-21


def k_cap():
    return (
        empirical_k_cap(
            gold_density_kg_m3=
                AU_DENSITY,

            separation_m=
                SEPARATION_M,

            sphere_gold_thickness_m=
                SPHERE_AU_M,

            plate_gold_thickness_m=
                PLATE_AU_M,

            allowed_extra_pressure_pa=
                ALLOWED_EXTRA_PA,
        )
    )


def test_stationary_q_cannot_be_smoothly_localized():
    result = (
        stationary_q_integrability(
            spatial_q_gradient_nonzero=
                True
        )
    )

    assert (
        result[
            "stationary_time_independent_spatial_gradient_possible"
        ]
        is False
    )

    assert (
        result[
            "smooth_stationary_q_must_be_spatially_constant"
        ]
        is True
    )


def test_constant_gamma_has_no_direct_static_lapse_gradient():
    assert (
        constant_gamma_direct_lapse_gradient()
        ==
        0.0
    )


def test_anisotropic_gold_response_has_zt_gt_zs():
    state = (
        material_kinetic_factors(
            density_kg_m3=
                AU_DENSITY,

            effective_k_ev_m4=
                EXPECTED_K_CAP,
        )
    )

    assert (
        state[
            "z_t"
        ]
        >
        state[
            "z_s"
        ]
        >
        1.0
    )


def test_empirical_k_cap_reconstructs_reference():
    result = k_cap()

    assert math.isclose(
        result[
            "k_cap_ev_m4"
        ],
        EXPECTED_K_CAP,
        rel_tol=3.0e-10,
    )


def test_empirical_k_cap_gold_factors():
    result = k_cap()

    assert math.isclose(
        result[
            "gold_z_t"
        ],
        2.1572416021,
        rel_tol=3.0e-9,
    )

    assert math.isclose(
        result[
            "gold_z_s"
        ],
        1.19287360035,
        rel_tol=3.0e-9,
    )


def test_half_cap_pressure_is_inside_residual():
    pressure = (
        anisotropic_finite_slab_pressure_pa(
            effective_k_ev_m4=
                0.5
                * EXPECTED_K_CAP,

            density1_kg_m3=
                AU_DENSITY,

            density2_kg_m3=
                AU_DENSITY,

            separation_m=
                SEPARATION_M,

            thickness1_m=
                SPHERE_AU_M,

            thickness2_m=
                PLATE_AU_M,
        )
    )

    assert math.isclose(
        pressure,
        0.002341492649,
        rel_tol=5.0e-9,
    )

    assert (
        pressure
        <
        ALLOWED_EXTRA_PA
    )


def test_required_s2_reconstructs_one_g():
    q2 = 1.0e-12

    s2 = (
        required_s2_for_exponential_acceleration(
            effective_k_ev_m4=
                EXPECTED_K_CAP,

            q2_ev4=
                q2,

            target_acceleration_m_s2=
                TARGET_A,

            gradient_scale_m=
                H,
        )
    )

    acceleration = (
        acceleration_for_exponential_s2(
            effective_k_ev_m4=
                EXPECTED_K_CAP,

            q2_ev4=
                q2,

            s2_ev4=
                s2,

            gradient_scale_m=
                H,
        )
    )

    assert math.isclose(
        acceleration,
        TARGET_A,
        rel_tol=2.0e-14,
    )


def test_required_s2_at_best_k_is_about_9412_ev4():
    q2 = 1.0e-12

    s2 = (
        required_s2_for_exponential_acceleration(
            effective_k_ev_m4=
                EXPECTED_K_CAP,

            q2_ev4=
                q2,

            target_acceleration_m_s2=
                TARGET_A,

            gradient_scale_m=
                H,
        )
    )

    assert (
        9411.0
        <
        s2
        <
        9413.0
    )


def test_canonical_q_background_is_stiff():
    result = (
        canonical_background_energy(
            q2_ev4=
                1.0e-12
        )
    )

    assert (
        result[
            "equation_of_state_w"
        ]
        ==
        1.0
    )


def test_reference_critical_energy_density():
    critical = (
        critical_energy_density_j_m3()
    )

    assert math.isclose(
        critical,
        7.6689477678e-10,
        rel_tol=3.0e-10,
    )


def test_loose_cosmological_ceiling_is_noninvertible_at_one_g():
    critical = (
        critical_energy_density_j_m3()
    )

    rho_q = (
        LOOSE_OMEGA_STIFF_CEILING
        * critical
    )

    q2 = (
        2.0
        * rho_q
        /
        20.852156864043042
    )

    s2 = (
        required_s2_for_exponential_acceleration(
            effective_k_ev_m4=
                EXPECTED_K_CAP,

            q2_ev4=
                q2,

            target_acceleration_m_s2=
                TARGET_A,

            gradient_scale_m=
                H,
        )
    )

    state = (
        disformal_invertibility(
            effective_k_ev_m4=
                EXPECTED_K_CAP,

            q2_ev4=
                q2,

            s2_ev4=
                s2,
        )
    )

    assert (
        state[
            "metric_signature_margin"
        ]
        <
        0.0
    )

    assert (
        state[
            "lorentzian_invertible_branch"
        ]
        is False
    )


def test_minimum_invertible_background_exceeds_loose_stiff_ceiling():
    q2 = (
        minimum_q2_for_metric_invertibility(
            effective_k_ev_m4=
                EXPECTED_K_CAP,

            target_acceleration_m_s2=
                TARGET_A,

            gradient_scale_m=
                H,
        )
    )

    background = (
        canonical_background_energy(
            q2_ev4=
                q2
        )
    )

    assert (
        background[
            "omega"
        ]
        >
        2.7e-3
    )

    assert (
        background[
            "omega"
        ]
        >
        LOOSE_OMEGA_STIFF_CEILING
    )


def test_chi_le_one_requires_even_more_background():
    q2 = (
        minimum_q2_for_derivative_ratio(
            effective_k_ev_m4=
                EXPECTED_K_CAP,

            target_acceleration_m_s2=
                TARGET_A,

            gradient_scale_m=
                H,

            maximum_ratio=
                1.0,
        )
    )

    background = (
        canonical_background_energy(
            q2_ev4=
                q2
        )
    )

    assert (
        background[
            "omega"
        ]
        >
        5.5e-3
    )


def test_local_gradient_energy_itself_is_not_mj_scale():
    reference_k = (
        0.5
        * EXPECTED_K_CAP
    )

    q2 = (
        minimum_q2_for_derivative_ratio(
            effective_k_ev_m4=
                reference_k,

            target_acceleration_m_s2=
                TARGET_A,

            gradient_scale_m=
                H,

            maximum_ratio=
                1.0,
        )
    )

    s2 = (
        required_s2_for_exponential_acceleration(
            effective_k_ev_m4=
                reference_k,

            q2_ev4=
                q2,

            target_acceleration_m_s2=
                TARGET_A,

            gradient_scale_m=
                H,
        )
    )

    energy = (
        spherical_exponential_gradient_energy_j(
            s2_at_radius_ev4=
                s2,

            radius_m=
                0.10,

            decay_scale_m=
                H,
        )
    )

    assert (
        1.2e4
        <
        energy
        <
        1.3e4
    )


def test_failure_memory_is_idempotent(tmp_path):
    storage = Storage(
        tmp_path
        / "agminer.sqlite3"
    )

    try:
        first = (
            persist_v21_failure_rule(
                storage,

                k_cap_ev_m4=
                    EXPECTED_K_CAP,

                omega_min_invertible=
                    2.8e-3,

                omega_loose_ceiling=
                    LOOSE_OMEGA_STIFF_CEILING,
            )
        )

        second = (
            persist_v21_failure_rule(
                storage,

                k_cap_ev_m4=
                    EXPECTED_K_CAP,

                omega_min_invertible=
                    2.8e-3,

                omega_loose_ceiling=
                    LOOSE_OMEGA_STIFF_CEILING,
            )
        )

        assert first == 1
        assert second == 0

    finally:
        storage.close()
