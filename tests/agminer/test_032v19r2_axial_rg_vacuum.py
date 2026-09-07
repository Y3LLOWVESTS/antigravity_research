"""Scientific regressions for 032V19R2 axial RG and vacuum diagnostics.

These tests protect:

- the equivalent pseudoscalar coupling convention;
- collective versus per-flavor loop accounting;
- large-Nf power counting;
- canonical C1 f^2 invariance;
- massless-decoupling subtraction;
- the universal logarithmic vacuum coefficient;
- convergence and scale of the nonlinear constant-background remainder;
- bulk derivative-expansion hierarchy;
- rejection of the Jiang positive-C1 spin-2 template as a pure j=0
  completion.

Passing these tests does not establish a UV completion or practical device.
"""

import math

from antigravity_research.agminer.axial_rg_vacuum import (
    asymptotic_quadratic_log_slope_ev4,
    bulk_derivative_expansion_scout,
    ev4_energy_density_j_m3,
    field_rescaling_scout,
    finite_cutoff_quadratic_log_slope_ev4,
    jiang_positive_c1_spin2_template,
    large_nf_power_counting,
    natural_b4_loop_scale_ev4,
    nonlinear_vacuum_remainder_ev4,
    pseudoscalar_equivalent_coupling,
    symmetry_restored_axial_vacuum_density_ev4,
)


NF = 118

M_PSI_EV = 7.193579811578565
F_PSI_EV = 22.70625323988203
B_EV = 6.123454611098919

HARD_EV = 56.92491792612398
CUTOFF_EV = 285.337620114

METRIC_SCALE_EV = 23971.29870009097
C1 = 1.0 / (
    2.0
    * METRIC_SCALE_EV**4
)

DELTA_Z_HARD = 2.482254192298938
DELTA_Z_CUTOFF = 4.416572781507421

RADIUS_M = 0.10

VOLUME_M3 = (
    4.0
    * math.pi
    * RADIUS_M**3
    / 3.0
)


def test_equivalent_pseudoscalar_coupling():
    g_p = (
        pseudoscalar_equivalent_coupling(
            mass_ev=
                M_PSI_EV,

            f_psi_ev=
                F_PSI_EV,
        )
    )

    assert math.isclose(
        g_p,
        0.6336210325482954,
        rel_tol=2.0e-14,
    )


def test_collective_loop_reconstructs_r1():
    result = (
        large_nf_power_counting(
            flavors=
                NF,

            mass_ev=
                M_PSI_EV,

            f_psi_ev=
                F_PSI_EV,
        )
    )

    assert math.isclose(
        result[
            "collective_loop"
        ],
        0.30000013422209776,
        rel_tol=2.0e-14,
    )


def test_single_flavor_loop_is_small():
    result = (
        large_nf_power_counting(
            flavors=
                NF,

            mass_ev=
                M_PSI_EV,

            f_psi_ev=
                F_PSI_EV,
        )
    )

    assert (
        result[
            "single_flavor_loop"
        ]
        <
        3.0e-3
    )


def test_large_nf_power_counting_scout():
    result = (
        large_nf_power_counting(
            flavors=
                NF,

            mass_ev=
                M_PSI_EV,

            f_psi_ev=
                F_PSI_EV,
        )
    )

    assert (
        result[
            "one_over_nf"
        ]
        <
        0.009
    )

    assert (
        result[
            "induced_four_point_scaling"
        ]
        <
        8.0e-4
    )

    assert (
        result[
            "large_nf_power_counting_scout"
        ]
        is True
    )


def test_canonical_rescaling_preserves_c1_f2():
    loop = (
        large_nf_power_counting(
            flavors=
                NF,

            mass_ev=
                M_PSI_EV,

            f_psi_ev=
                F_PSI_EV,
        )[
            "collective_loop"
        ]
    )

    result = (
        field_rescaling_scout(
            f_psi_ev=
                F_PSI_EV,

            c1_ev_m4=
                C1,

            collective_loop=
                loop,

            delta_z=
                DELTA_Z_HARD,
        )
    )

    assert (
        result[
            "invariant_relative_error"
        ]
        <
        1.0e-14
    )

    assert (
        result[
            "positive_kinetic_factor"
        ]
        is True
    )


def test_massless_subtraction_exactly_decouples():
    result = (
        symmetry_restored_axial_vacuum_density_ev4(
            mass_ev=
                0.0,

            axial_b_ev=
                B_EV,

            flavors=
                NF,

            cutoff_ev=
                5.0
                * HARD_EV,

            p_order=
                64,

            u_order=
                48,
        )
    )

    assert (
        abs(
            result
        )
        <
        1.0e-10
    )


def test_quadratic_log_slope_matches_asymptotic_coefficient():
    finite = (
        finite_cutoff_quadratic_log_slope_ev4(
            mass_ev=
                M_PSI_EV,

            axial_b_ev=
                B_EV,

            flavors=
                NF,

            cutoff_ev=
                CUTOFF_EV,
        )
    )

    asymptotic = (
        asymptotic_quadratic_log_slope_ev4(
            mass_ev=
                M_PSI_EV,

            axial_b_ev=
                B_EV,

            flavors=
                NF,
        )
    )

    assert (
        finite
        / asymptotic
        >
        0.999
    )


def test_nonlinear_remainder_is_about_expected_scale():
    remainder = (
        nonlinear_vacuum_remainder_ev4(
            mass_ev=
                M_PSI_EV,

            axial_b_ev=
                B_EV,

            flavors=
                NF,

            cutoff_ev=
                CUTOFF_EV,

            p_order=
                120,

            u_order=
                96,
        )
    )

    assert (
        -1420.0
        <
        remainder
        <
        -1380.0
    )


def test_nonlinear_remainder_converges_with_cutoff():
    remainder_5 = (
        nonlinear_vacuum_remainder_ev4(
            mass_ev=
                M_PSI_EV,

            axial_b_ev=
                B_EV,

            flavors=
                NF,

            cutoff_ev=
                5.0
                * HARD_EV,

            p_order=
                120,

            u_order=
                96,
        )
    )

    remainder_8 = (
        nonlinear_vacuum_remainder_ev4(
            mass_ev=
                M_PSI_EV,

            axial_b_ev=
                B_EV,

            flavors=
                NF,

            cutoff_ev=
                8.0
                * HARD_EV,

            p_order=
                120,

            u_order=
                96,
        )
    )

    relative_change = (
        abs(
            remainder_8
            - remainder_5
        )
        /
        abs(
            remainder_8
        )
    )

    assert (
        relative_change
        <
        2.0e-3
    )


def test_nonlinear_remainder_energy_is_not_mj_scale():
    remainder = (
        nonlinear_vacuum_remainder_ev4(
            mass_ev=
                M_PSI_EV,

            axial_b_ev=
                B_EV,

            flavors=
                NF,

            cutoff_ev=
                CUTOFF_EV,

            p_order=
                120,

            u_order=
                96,
        )
    )

    energy_j = (
        remainder
        * ev4_energy_density_j_m3(
            1.0
        )
        * VOLUME_M3
    )

    assert (
        abs(
            energy_j
        )
        <
        1.0e3
    )


def test_natural_b4_loop_scale_is_small_in_energy_units():
    density = (
        natural_b4_loop_scale_ev4(
            axial_b_ev=
                B_EV,

            flavors=
                NF,
        )
    )

    energy_j = (
        density
        * ev4_energy_density_j_m3(
            1.0
        )
        * VOLUME_M3
    )

    assert (
        energy_j
        <
        1.0e3
    )


def test_bulk_derivative_expansion_has_large_scale_separation():
    result = (
        bulk_derivative_expansion_scout(
            mass_ev=
                M_PSI_EV,

            source_radius_m=
                RADIUS_M,
        )
    )

    assert (
        result[
            "source_radius_over_compton"
        ]
        >
        1.0e6
    )

    assert (
        result[
            "bulk_slow_variation_scout"
        ]
        is True
    )


def test_jiang_spin2_template_is_not_pure_j0():
    result = (
        jiang_positive_c1_spin2_template()
    )

    assert math.isclose(
        result[
            "c2_over_c1"
        ],
        12.0,
        rel_tol=0.0,
        abs_tol=0.0,
    )

    assert math.isclose(
        result[
            "c4_over_c1"
        ],
        -12.0,
        rel_tol=0.0,
        abs_tol=0.0,
    )

    assert (
        result[
            "pure_j0_completion"
        ]
        is False
    )

    assert (
        result[
            "directly_adopted"
        ]
        is False
    )
