"""BETA1-02 exact, numerical, passivity and provenance regression tests."""

import ast
import math

from functools import lru_cache
from pathlib import Path

import numpy as np

from antigravity_research.beta_artificial.beta1_02_passive_material import (
    Spec,
    c2_fraction,
    exact_theorems,
    material_system,
    retarded_kernel,
    summarize,
)


@lru_cache(maxsize=1)
def result():
    return summarize()


@lru_cache(maxsize=1)
def material():
    return material_system()


def test_01_twelve_exact_identities():
    checks = exact_theorems()["checks"]
    assert len(checks) == 12
    assert all(checks.values())


def test_02_kink_analytic_eom():
    assert exact_theorems()["checks"][
        "phi4_kink_Euler_Lagrange"
    ]


def test_03_metric_stress_noether_ward():
    assert exact_theorems()["checks"][
        "material_stress_Ward_offshell"
    ]


def test_04_C2_endpoints():
    assert exact_theorems()["checks"][
        "C2_endpoints_exact"
    ]


def test_05_C2_first_second_derivatives():
    assert exact_theorems()["checks"][
        "C2_first_second_derivatives_endpoints_zero"
    ]


def test_06_C2_third_derivative_jump():
    assert exact_theorems()["checks"][
        "C2_third_derivative_endpoint_nonzero"
    ]


def test_07_phi4_kink_exponential_tails():
    assert result()["gates"][
        "noncompact_analytic_kink"
    ]


def test_08_C2_has_nonzero_stationary_residual():
    assert result()["gates"][
        "C2_profile_not_exact_on_shell"
    ]


def test_09_width_from_kappa_not_fitted():
    assert result()["gates"][
        "width_responds_to_physical_kappa"
    ]


def test_10_positive_surface_tension():
    assert result()["gates"][
        "surface_tension_positive"
    ]


def test_11_discrete_stationary_EOM():
    assert result()["gates"][
        "discrete_kink_stationarity"
    ]


def test_12_refined_discrete_EOM():
    assert result()["gates"][
        "mesh_refined_kink_stationarity"
    ]


def test_13_energy_error_decreases_with_mesh():
    assert result()["gates"][
        "interface_energy_convergence"
    ]


def test_14_surface_energy_matches_continuum():
    assert result()["gates"][
        "interface_energy_approaches_tension"
    ]


def test_15_C2_profile_mismatch_is_nonzero():
    assert result()["kink_profiles"]["1.0"][
        "matched_profile_max_abs_difference"
    ] > .03


def test_16_mass_kinetic_is_positive():
    assert result()["gates"]["kinetic_positive"]


def test_17_material_hessian_supported_positive():
    assert result()["gates"][
        "supported_material_positive_modes"
    ]


def test_18_material_hessian_refined_positive():
    assert result()["gates"][
        "refined_supported_material_positive_modes"
    ]


def test_19_material_wave_speed_below_light_canonical():
    speed = result()["stationary"][
        "material_wave_speed_canonical"
    ]
    assert 0 < speed < 1


def test_20_exact_action_cross_FD():
    assert result()["gates"][
        "cross_variation_same_action"
    ]


def test_21_static_response_reciprocity():
    assert result()["gates"]["static_reciprocity"]


def test_22_static_response_psd():
    assert result()["gates"]["static_passivity"]


def test_23_four_frequency_reciprocity():
    assert result()["gates"]["dynamic_reciprocity"]

    assert len(result()[
        "passive_reciprocal_susceptibility"
    ]["frequencies"]) == 4


def test_24_retarded_imaginary_spectral_measure_positive():
    assert result()["gates"][
        "retarded_spectral_passivity"
    ]


def test_25_retarded_kernel_zero_before_impulse():
    assert result()["gates"][
        "retarded_kernel_zero_before_drive"
    ]

    np.testing.assert_array_equal(
        retarded_kernel(
            material(),
            -1.0,
        ),
        np.zeros((3, 3)),
    )


def test_26_retarded_kernel_is_reciprocal():
    assert result()["gates"][
        "retarded_kernel_reciprocity"
    ]


def test_27_noninstantaneous_high_frequency_decay():
    assert result()["gates"][
        "high_frequency_response_decays"
    ]


def test_28_time_cycle_passivity():
    assert result()["gates"][
        "time_cycle_drive_energy_passive"
    ]


def test_29_full_including_bath_energy_ledger():
    assert result()["gates"][
        "time_cycle_full_bath_work_ledger"
    ]


def test_30_temporal_refinement():
    assert result()["gates"][
        "time_step_convergence"
    ]


def test_31_explicit_conservative_bath():
    assert result()["stationary"][
        "supported_bath_modes"
    ] > 0

    assert result()["time_cycle"][
        "material_dissipated_heat"
    ] == 0


def test_32_post_pulse_energy_not_reset():
    assert result()["gates"]["post_pulse_no_reset"]


def test_33_zero_metric_drive_control():
    assert result()["gates"]["source_off_zero"]


def test_34_homogeneous_phi4_scalar_control():
    assert result()["gates"][
        "homogeneous_scalar_control_zero_energy"
    ]

    assert result()[
        "homogeneous_order_parameter"
    ]["dust_trace"] == "NOT_INCLUDED"


def test_35_boundary_traction_reciprocity():
    assert result()["gates"][
        "boundary_traction_symmetric"
    ]


def test_36_M5T_frozen_C2_function_reproduction():
    # Extract and execute only the historical pure C2 function,
    # not the old artificial field optimizer.

    root = Path(__file__).resolve().parents[2]

    path = root/(
        "src/antigravity_research/agminer/"
        "hook17_r3b_m5t_variational_cell_material.py"
    )

    tree = ast.parse(
        path.read_text()
    )

    function = next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "f_and_dedge"
    )

    scope = {"np": np}

    exec(
        compile(
            ast.Module(
                body=[function],
                type_ignores=[],
            ),
            str(path),
            "exec",
        ),
        scope,
    )

    x = np.linspace(
        -1,
        1,
        61,
    )

    for halfwidth in (.25, .5, .75):
        actual, _ = scope["f_and_dedge"](
            x,
            0.0,
            halfwidth,
            "c2",
        )

        np.testing.assert_allclose(
            actual,
            c2_fraction(
                x,
                halfwidth,
            ),
            atol=1e-14,
            rtol=0,
        )


def test_37_no_fictional_M5V_source_certification():
    assert result()["material_obstructions"][
        "C2_0p25_to_0p75m_material_width"
    ] == "NOT_DERIVED_FROM_M5V"


def test_38_P10_alpha_nonzero_still_open():
    assert result()["material_obstructions"][
        "source_X_Y_reciprocity"
    ] == "NOT_SOLVED"


def test_39_PH11_support_history_protected():
    assert result()["material_obstructions"][
        "R3A_suppression"
    ] == "HISTORICAL_CONTROL_NOT_RETESTED"


def test_40_no_dust_trace_or_Earth_force():
    status = result()["material_obstructions"]

    assert status[
        "full_neutral_dust_mass_trace"
    ] == "MISSING"

    assert status[
        "Earth_hull_external_reaction"
    ] == "NOT_DERIVED"


def test_41_no_SI_or_gravitational_promotion():
    r = result()

    assert r["physical_transfer"] == (
        "NOT_AUTHORIZED"
    )

    assert "not joules" in " ".join(
        r["limits"]
    )


def test_42_scope_of_the_C2_obstruction():
    r = result()["material_obstructions"]

    assert r[
        "C2_compact_smoothstep_as_exact_analytic_phi4_interface"
    ] == "CLOSED_IN_TESTED_LOCAL_ACTION_CLASS"

    assert r[
        "C2_as_general_coarse_grained_profile"
    ] == "NOT_EXCLUDED"


def test_43_all_scientific_gates():
    gates = result()["gates"]

    assert len(gates) == 28
    assert all(gates.values())


def test_44_energy_finite_and_no_10MJ_claim():
    assert math.isfinite(
        result()["time_cycle"]["external_work"]
    )

    assert result()["time_cycle"][
        "full_source_field_support_ledger"
    ] == "NOT_CLOSED"
