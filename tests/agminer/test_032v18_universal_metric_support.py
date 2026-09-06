import math

from antigravity_research.agminer.axial_dirac_meanfield import (
    meanfield_scaling_metrics,
)
from antigravity_research.agminer.c1_payload_matching import (
    required_q2_for_payload_surface,
)
from antigravity_research.agminer.universal_metric_support import (
    canonical_rescaling,
    isotropic_bag_shape_compatible,
    polarized_sphere_incident_coefficients,
    scalar_sphere_integrated_stresses_j,
    spherical_anisotropic_dec_support_floor_j,
)


G = 9.80665

SOURCE_RADIUS_M = 0.10
PAYLOAD_RADIUS_M = 0.10
CENTER_SEPARATION_M = 0.30


def test_canonical_rescaling_preserves_c1_f_squared():
    result = canonical_rescaling(
        c1_bare_ev_m4=
            1.5e-18,

        f_bare_ev=
            10.0,

        kinetic_z=
            4.25,
    )

    assert (
        result[
            "invariant_relative_error"
        ]
        < 1.0e-15
    )


def test_minimal_isotropic_bag_prefers_sphere():
    assert (
        isotropic_bag_shape_compatible(
            a_m=
                0.10,

            c_m=
                0.10,
        )
        is True
    )

    assert (
        isotropic_bag_shape_compatible(
            a_m=
                0.2574,

            c_m=
                0.09659,
        )
        is False
    )


def test_spherical_scalar_stress_trace_is_minus_field_energy():
    energy = 1234.5

    stress = (
        scalar_sphere_integrated_stresses_j(
            energy
        )
    )

    assert math.isclose(
        stress[
            "trace_j"
        ],
        -energy,
        rel_tol=1.0e-15,
    )


def test_anisotropic_dec_support_floor_uses_largest_principal_stress():
    result = (
        spherical_anisotropic_dec_support_floor_j(
            fermion_pressure_perp_inventory_j=
                100.0,

            fermion_pressure_z_inventory_j=
                100.0,

            scalar_field_energy_j=
                10.0,
        )
    )

    assert math.isclose(
        result[
            "support_energy_floor_j"
        ],
        102.0,
        rel_tol=1.0e-15,
    )


def test_l32_spherical_expansion_reconstructs_v14_vacuum_q():
    coefficients = (
        polarized_sphere_incident_coefficients(
            source_radius_m=
                SOURCE_RADIUS_M,

            center_separation_m=
                CENTER_SEPARATION_M,

            lmax=
                32,
        )
    )

    result = required_q2_for_payload_surface(
        coefficients=
            coefficients,

        epsilon_trace_load=
            0.0,

        payload_radius_m=
            PAYLOAD_RADIUS_M,

        target_acceleration_m_s2=
            G,

        surface_count=
            801,
    )

    assert math.isclose(
        math.sqrt(
            result[
                "q2"
            ]
        ),
        3.6616787206413e-7,
        rel_tol=2.0e-10,
    )


def test_l28_l32_spherical_payload_convergence():
    low = (
        polarized_sphere_incident_coefficients(
            source_radius_m=
                SOURCE_RADIUS_M,

            center_separation_m=
                CENTER_SEPARATION_M,

            lmax=
                28,
        )
    )

    high = (
        polarized_sphere_incident_coefficients(
            source_radius_m=
                SOURCE_RADIUS_M,

            center_separation_m=
                CENTER_SEPARATION_M,

            lmax=
                32,
        )
    )

    low_result = (
        required_q2_for_payload_surface(
            coefficients=
                low,

            epsilon_trace_load=
                3.0,

            payload_radius_m=
                PAYLOAD_RADIUS_M,

            target_acceleration_m_s2=
                G,

            surface_count=
                801,
        )
    )

    high_result = (
        required_q2_for_payload_surface(
            coefficients=
                high,

            epsilon_trace_load=
                3.0,

            payload_radius_m=
                PAYLOAD_RADIUS_M,

            target_acceleration_m_s2=
                G,

            surface_count=
                801,
        )
    )

    relative_error = (
        abs(
            low_result[
                "q2"
            ]
            - high_result[
                "q2"
            ]
        )
        /
        high_result[
            "q2"
        ]
    )

    assert (
        relative_error
        < 2.0e-8
    )


def test_payload_epsilon_three_requires_about_3p8x_spherical_q2():
    coefficients = (
        polarized_sphere_incident_coefficients(
            source_radius_m=
                SOURCE_RADIUS_M,

            center_separation_m=
                CENTER_SEPARATION_M,

            lmax=
                32,
        )
    )

    vacuum = (
        required_q2_for_payload_surface(
            coefficients=
                coefficients,

            epsilon_trace_load=
                0.0,

            payload_radius_m=
                PAYLOAD_RADIUS_M,

            target_acceleration_m_s2=
                G,

            surface_count=
                801,
        )
    )

    loaded = (
        required_q2_for_payload_surface(
            coefficients=
                coefficients,

            epsilon_trace_load=
                3.0,

            payload_radius_m=
                PAYLOAD_RADIUS_M,

            target_acceleration_m_s2=
                G,

            surface_count=
                801,
        )
    )

    factor = (
        loaded[
            "q2"
        ]
        /
        vacuum[
            "q2"
        ]
    )

    assert (
        3.79
        < factor
        < 3.82
    )


def test_oblate_loop030_state_cannot_be_transplanted_to_sphere():
    volume = (
        4.0
        * math.pi
        * SOURCE_RADIUS_M**3
        / 3.0
    )

    metrics = meanfield_scaling_metrics(
        q=
            3.6616787206413e-7,

        metric_scale_ev=
            1.0e5,

        volume_m3=
            volume,

        demag_z=
            1.0 / 3.0,

        r_mass_over_b=
            1.2286138490752774,

        u_mu_over_b=
            3.27821298270277,

        order=
            80,
    )

    assert (
        0.54
        < metrics[
            "loop_proxy"
        ]
        < 0.55
    )
