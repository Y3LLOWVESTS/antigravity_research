"""Scientific regressions for the 032V19 physical spherical bag preflight.

These tests protect:

- the V18 integrated stress reconstruction;
- false-vacuum plus wall pressure balance;
- the finite quartic-wall mapping;
- the hidden-fermion Yukawa confinement barrier;
- support-sector loop-size diagnostics;
- support trace-loading diagnostics;
- the spacelike-axial spectral gap;
- conditional radial and l=2 stability scouts.

Passing these tests does not certify a coupled physical antigravity model.
"""

import math

import numpy as np

from antigravity_research.agminer.physical_spherical_bag import (
    axial_spacelike_gap,
    fermion_cw_magnitude_proxy_j,
    friedberg_lee_bag_support,
    l2_wall_stiffness_scout_j,
    pressure_decomposition_j,
    quartic_wall_parameters,
    radial_gamma_threshold,
    sphere_volume_m3,
    support_loop_naturalness,
    tilted_wall_potential_ev4,
    trace_load_epsilon,
    yukawa_mass_barrier,
)


RADIUS_M = 0.10

FIELD_ENERGY_J = 2545.59319853775

FERMION_PRESSURE_PERP_J = 836323.1996108652
FERMION_PRESSURE_Z_J = 836323.1996108663

TOTAL_PRESSURE_PERP_J = (
    FERMION_PRESSURE_PERP_J
    - 3.0
    * FIELD_ENERGY_J
    / 5.0
)

TOTAL_PRESSURE_Z_J = (
    FERMION_PRESSURE_Z_J
    + FIELD_ENERGY_J
    / 5.0
)

BAG_FRACTION = 0.95
M_CHI_EV = 100.0

M_PSI_EV = 7.193579811578565
MU_EV = 56.5506596329978
B_AXIAL_EV = 6.19149614689479

FLAVORS = 116
AXIAL_CUTOFF_EV = 282.90676468843844
METRIC_SCALE_EV = 23971.29870009097

BAND_ENERGY_J = 2579779.581097457


def reference_support():
    return friedberg_lee_bag_support(
        radius_m=
            RADIUS_M,

        pressure_perp_j=
            TOTAL_PRESSURE_PERP_J,

        pressure_z_j=
            TOTAL_PRESSURE_Z_J,

        bag_fraction=
            BAG_FRACTION,
    )


def reference_wall():
    support = reference_support()

    return quartic_wall_parameters(
        wall_tension_j_m2=
            support[
                "wall_tension_j_m2"
            ],

        mediator_mass_ev=
            M_CHI_EV,
    )


def test_v18_total_pressure_decomposition():
    result = pressure_decomposition_j(
        pressure_perp_j=
            TOTAL_PRESSURE_PERP_J,

        pressure_z_j=
            TOTAL_PRESSURE_Z_J,
    )

    assert math.isclose(
        result[
            "mean_pressure_inventory_j"
        ],
        835474.6685446863,
        rel_tol=2.0e-14,
    )

    assert math.isclose(
        result[
            "anisotropy_reserve_floor_j"
        ],
        1357.6497058875393,
        rel_tol=2.0e-14,
    )


def test_reference_false_vacuum_bag_stays_close_to_v18_support_floor():
    result = reference_support()

    assert math.isclose(
        result[
            "support_preflight_j"
        ],
        857719.184964191,
        rel_tol=2.0e-13,
    )

    assert (
        0.84e6
        <
        result[
            "support_preflight_j"
        ]
        <
        0.87e6
    )

    assert (
        result[
            "equatorial_required_tension_j_m2"
        ]
        >
        0.0
    )

    assert (
        result[
            "polar_required_tension_j_m2"
        ]
        >
        0.0
    )

    assert (
        result[
            "tension_anisotropy_ratio"
        ]
        <
        1.06
    )


def test_reference_wall_is_finite_and_below_axial_cutoff():
    wall = reference_wall()

    assert math.isclose(
        wall[
            "vev_ev"
        ],
        42635.29240329986,
        rel_tol=2.0e-13,
    )

    assert math.isclose(
        wall[
            "lambda"
        ],
        2.750625802927001e-6,
        rel_tol=2.0e-13,
    )

    assert (
        wall[
            "wall_thickness_m"
        ]
        <
        1.0e-8
    )

    assert (
        M_CHI_EV
        <
        AXIAL_CUTOFF_EV
    )


def test_reference_tilted_potential_is_nonnegative_on_wide_field_scan():
    support = reference_support()
    wall = reference_wall()

    chi = np.linspace(
        -3.0
        * wall[
            "vev_ev"
        ],
        3.0
        * wall[
            "vev_ev"
        ],
        120001,
    )

    potential = (
        tilted_wall_potential_ev4(
            chi,
            vev_ev=
                wall[
                    "vev_ev"
                ],
            lambda_=
                wall[
                    "lambda"
                ],
            bag_density_j_m3=
                support[
                    "bag_energy_density_j_m3"
                ],
        )
    )

    assert (
        float(
            np.min(
                potential
            )
        )
        >
        -1.0e-8
        * wall[
            "degenerate_barrier_ev4"
        ]
    )


def test_five_percent_mass_barrier_confines_on_nanometer_scale():
    wall = reference_wall()

    barrier = yukawa_mass_barrier(
        inside_mass_ev=
            M_PSI_EV,

        chemical_potential_ev=
            MU_EV,

        vev_ev=
            wall[
                "vev_ev"
            ],

        outside_mass_factor=
            1.05,
    )

    assert (
        barrier[
            "outside_mass_ev"
        ]
        >
        MU_EV
    )

    assert (
        barrier[
            "decay_length_m"
        ]
        <
        2.0e-8
    )

    assert (
        barrier[
            "yukawa"
        ]
        <
        1.0e-3
    )


def test_support_scalar_loop_proxies_are_small_at_reference_point():
    wall = reference_wall()

    barrier = yukawa_mass_barrier(
        inside_mass_ev=
            M_PSI_EV,

        chemical_potential_ev=
            MU_EV,

        vev_ev=
            wall[
                "vev_ev"
            ],

        outside_mass_factor=
            1.05,
    )

    result = support_loop_naturalness(
        flavors=
            FLAVORS,

        yukawa=
            barrier[
                "yukawa"
            ],

        lambda_=
            wall[
                "lambda"
            ],

        cutoff_ev=
            AXIAL_CUTOFF_EV,

        mediator_mass_ev=
            M_CHI_EV,
    )

    assert (
        result[
            "delta_lambda_over_lambda"
        ]
        <
        1.0e-6
    )

    assert (
        result[
            "delta_m2_over_m2"
        ]
        <
        1.0e-4
    )


def test_support_trace_loading_is_weak():
    support = reference_support()
    wall = reference_wall()

    bag_epsilon = trace_load_epsilon(
        energy_density_j_m3=
            support[
                "bag_energy_density_j_m3"
            ],

        metric_scale_ev=
            METRIC_SCALE_EV,
    )

    wall_density = (
        support[
            "wall_tension_j_m2"
        ]
        /
        wall[
            "wall_thickness_m"
        ]
    )

    wall_epsilon = trace_load_epsilon(
        energy_density_j_m3=
            wall_density,

        metric_scale_ev=
            METRIC_SCALE_EV,
    )

    assert (
        bag_epsilon
        <
        1.0e-9
    )

    assert (
        wall_epsilon
        <
        1.0e-3
    )


def test_v18_axial_background_is_on_gapped_spacelike_branch():
    result = axial_spacelike_gap(
        b_ev=
            B_AXIAL_EV,

        mass_ev=
            M_PSI_EV,
    )

    assert (
        result[
            "strict_b_below_m"
        ]
        is True
    )

    assert (
        result[
            "gap_ev"
        ]
        >
        1.0
    )


def test_reference_stability_scout_has_large_geometric_margin():
    support = reference_support()

    assert math.isclose(
        radial_gamma_threshold(
            BAG_FRACTION
        ),
        0.05,
        rel_tol=1.0e-14,
    )

    l2_stiffness = (
        l2_wall_stiffness_scout_j(
            support[
                "wall_energy_j"
            ]
        )
    )

    assert (
        l2_stiffness
        /
        support[
            "anisotropy_reserve_floor_j"
        ]
        >
        30.0
    )


def test_reference_static_subtotal_is_below_four_mj_but_not_complete():
    support = reference_support()

    subtotal = (
        BAND_ENERGY_J
        +
        FIELD_ENERGY_J
        +
        support[
            "support_preflight_j"
        ]
    )

    assert (
        subtotal
        <
        4.0e6
    )

    wall = reference_wall()

    barrier = yukawa_mass_barrier(
        inside_mass_ev=
            M_PSI_EV,

        chemical_potential_ev=
            MU_EV,

        vev_ev=
            wall[
                "vev_ev"
            ],

        outside_mass_factor=
            1.05,
    )

    cw_proxy = fermion_cw_magnitude_proxy_j(
        flavors=
            FLAVORS,

        inside_mass_ev=
            M_PSI_EV,

        outside_mass_ev=
            barrier[
                "outside_mass_ev"
            ],

        volume_m3=
            sphere_volume_m3(
                RADIUS_M
            ),
    )

    assert (
        subtotal
        + cw_proxy
        <
        1.0e7
    )
