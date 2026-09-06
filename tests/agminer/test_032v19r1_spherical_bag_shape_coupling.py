"""Scientific regressions for 032V19R1 local support and RG structure.

These tests protect:

- the exact local scalar traction decomposition;
- distinction between l=0 and l=2 support;
- the small volume-preserving wall deformation;
- exact reconstruction of the V18 fixed-number mean field;
- the declared loop-cap normalization;
- the theorem-like fixed-order RG obstruction.

Passing these tests does not certify a physical antigravity model.
"""

import math

from antigravity_research.agminer.spherical_bag_shape_coupling import (
    false_vacuum_l0_support,
    f_for_declared_loop_cap,
    fixed_number_meanfield_state,
    fixed_order_rg_structural_gate,
    linear_l2_shape_response,
    local_spherical_traction_multipoles,
    particle_number_from_state,
    sphere_volume_m3,
    spheroid_area_m2,
    spheroid_volume_m3,
)


RADIUS_M = 0.10

FIELD_ENERGY_J = 2545.59319853775

PRESSURE_PERP_J = 836323.1996108652
PRESSURE_Z_J = 836323.1996108663

METRIC_SCALE_EV = 23971.29870009097

FLAVORS = 116
F_PSI_EV = 22.513005017150324
B_AXIAL_EV = 6.19149614689479
M_PSI_EV = 7.193579811578565
MU_EV = 56.5506596329978
CUTOFF_EV = 282.90676468843844

LOOP_PROXY = 0.300000134


def reference_volume():
    return sphere_volume_m3(
        RADIUS_M
    )


def reference_traction():
    return (
        local_spherical_traction_multipoles(
            fermion_pressure_perp_inventory_j=
                PRESSURE_PERP_J,

            fermion_pressure_z_inventory_j=
                PRESSURE_Z_J,

            scalar_field_energy_j=
                FIELD_ENERGY_J,

            sphere_volume_m3_value=
                reference_volume(),
        )
    )


def test_sphere_volume():
    assert math.isclose(
        reference_volume(),
        0.004188790204786391,
        rel_tol=1.0e-14,
    )


def test_scalar_local_traction_identity():
    result = (
        local_spherical_traction_multipoles(
            fermion_pressure_perp_inventory_j=
                0.0,

            fermion_pressure_z_inventory_j=
                0.0,

            scalar_field_energy_j=
                FIELD_ENERGY_J,

            sphere_volume_m3_value=
                reference_volume(),
        )
    )

    assert math.isclose(
        result[
            "scalar_l0_inventory_j"
        ],
        FIELD_ENERGY_J
        / 3.0,
        rel_tol=1.0e-14,
    )

    assert math.isclose(
        result[
            "scalar_l2_inventory_j"
        ],
        2.0
        * FIELD_ENERGY_J
        / 3.0,
        rel_tol=1.0e-14,
    )


def test_v18_local_traction_reference():
    result = reference_traction()

    assert math.isclose(
        result[
            "total_l0_inventory_j"
        ],
        837171.7306770448,
        rel_tol=1.0e-13,
    )

    assert math.isclose(
        result[
            "total_l2_inventory_j"
        ],
        1697.0621323591986,
        rel_tol=1.0e-12,
    )


def test_x075_support_is_positive():
    support = (
        false_vacuum_l0_support(
            radius_m=
                RADIUS_M,

            l0_pressure_pa=
                reference_traction()[
                    "total_l0_pressure_pa"
                ],

            bag_fraction=
                0.75,
        )
    )

    assert (
        support[
            "bag_energy_density_j_m3"
        ]
        >
        0.0
    )

    assert (
        support[
            "wall_tension_j_m2"
        ]
        >
        0.0
    )

    assert (
        0.9e6
        <
        support[
            "sphere_support_energy_j"
        ]
        <
        1.0e6
    )


def test_x075_shape_is_small_and_prolate():
    support = (
        false_vacuum_l0_support(
            radius_m=
                RADIUS_M,

            l0_pressure_pa=
                reference_traction()[
                    "total_l0_pressure_pa"
                ],

            bag_fraction=
                0.75,
        )
    )

    shape = (
        linear_l2_shape_response(
            radius_m=
                RADIUS_M,

            l2_pressure_pa=
                reference_traction()[
                    "total_l2_pressure_pa"
                ],

            wall_tension_j_m2=
                support[
                    "wall_tension_j_m2"
                ],
        )
    )

    assert (
        0.0
        <
        shape[
            "epsilon_l2"
        ]
        <
        0.01
    )

    assert (
        1.0
        <
        shape[
            "pole_to_equator_aspect"
        ]
        <
        1.01
    )

    assert math.isclose(
        shape[
            "volume_ratio_to_reference_sphere"
        ],
        1.0,
        rel_tol=2.0e-14,
    )


def test_spheroid_area_exceeds_equal_volume_sphere():
    support = (
        false_vacuum_l0_support(
            radius_m=
                RADIUS_M,

            l0_pressure_pa=
                reference_traction()[
                    "total_l0_pressure_pa"
                ],

            bag_fraction=
                0.75,
        )
    )

    shape = (
        linear_l2_shape_response(
            radius_m=
                RADIUS_M,

            l2_pressure_pa=
                reference_traction()[
                    "total_l2_pressure_pa"
                ],

            wall_tension_j_m2=
                support[
                    "wall_tension_j_m2"
                ],
        )
    )

    assert (
        spheroid_area_m2(
            shape[
                "a_m"
            ],
            shape[
                "c_m"
            ],
        )
        >
        4.0
        * math.pi
        * RADIUS_M**2
    )

    assert math.isclose(
        spheroid_volume_m3(
            shape[
                "a_m"
            ],
            shape[
                "c_m"
            ],
        ),
        reference_volume(),
        rel_tol=2.0e-14,
    )


def test_fixed_number_reference_reconstructs_v18_state():
    number = (
        particle_number_from_state(
            mass_ev=
                M_PSI_EV,

            axial_b_ev=
                B_AXIAL_EV,

            chemical_potential_ev=
                MU_EV,

            flavors=
                FLAVORS,

            volume_m3=
                reference_volume(),

            order=
                96,
        )
    )

    state = (
        fixed_number_meanfield_state(
            particle_number=
                number,

            volume_m3=
                reference_volume(),

            demag_z=
                1.0
                / 3.0,

            mass_ev=
                M_PSI_EV,

            f_psi_ev=
                F_PSI_EV,

            flavors=
                FLAVORS,

            metric_scale_ev=
                METRIC_SCALE_EV,

            initial_b_ev=
                B_AXIAL_EV,

            initial_mu_ev=
                MU_EV,

            order=
                80,
        )
    )

    assert (
        abs(
            state[
                "axial_b_ev"
            ]
            / B_AXIAL_EV
            - 1.0
        )
        <
        1.0e-8
    )

    assert (
        abs(
            state[
                "chemical_potential_ev"
            ]
            / MU_EV
            - 1.0
        )
        <
        1.0e-8
    )

    assert (
        state[
            "particle_number_relative_error"
        ]
        <
        1.0e-10
    )


def test_loop_cap_reconstructs_fpsi():
    f_value = (
        f_for_declared_loop_cap(
            mass_ev=
                M_PSI_EV,

            flavors=
                FLAVORS,

            loop_proxy=
                LOOP_PROXY,
        )
    )

    assert (
        abs(
            f_value
            / F_PSI_EV
            - 1.0
        )
        <
        1.0e-6
    )


def test_rg_current_delta_is_red():
    result = (
        fixed_order_rg_structural_gate(
            loop_proxy=
                LOOP_PROXY,

            cutoff_ev=
                CUTOFF_EV,

            mass_ev=
                M_PSI_EV,

            hard_scale_ev=
                MU_EV,
        )
    )

    assert (
        result[
            "delta_z_at_declared_cutoff"
        ]
        >
        4.0
    )

    assert (
        result[
            "minimum_delta_z_with_cutoff_at_hard_scale"
        ]
        >
        2.0
    )


def test_no_fixed_order_window_above_hard_scale():
    result = (
        fixed_order_rg_structural_gate(
            loop_proxy=
                LOOP_PROXY,

            cutoff_ev=
                CUTOFF_EV,

            mass_ev=
                M_PSI_EV,

            hard_scale_ev=
                MU_EV,
        )
    )

    assert (
        result[
            "fixed_order_window_exists_above_hard_scale"
        ]
        is False
    )

    assert (
        result[
            "cutoff_ev_for_delta_z_equal_one"
        ]
        <
        MU_EV
    )

    assert (
        result[
            "loop_critical_at_declared_cutoff"
        ]
        <
        0.07
    )
