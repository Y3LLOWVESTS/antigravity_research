"""032H17A12D1R3A — topological F·Fdual same-action rescue theorem gate.

PURPOSE
-------
The A12C reduced-EFT probe result produced the extraordinary finite-payload
reference

    E_field = 2.6568591420597114 J

at

    M = 1 keV

for

    1 kg neutral payload
    1 m true external stand-off
    >= 1 g throughout the sampled payload.

A12D1 established the same-action matter loading of the conformal F^2 portal.

A12D1R1/R2/R2B/R2B1 then showed that ordinary source shaping does not rescue
the few-joule 1-keV F^2 descendant.

R2B1 allowed every axisymmetric azimuthal source-bearing grid cell inside the
original 2 m source support to vary independently and still found a fine-grid
pointwise loaded-capacity floor of approximately 1.93 MJ.

The purpose of R3A is therefore NOT more source shaping.

It is to test a structurally different physical metric portal:

    g_phys_mn = exp(2 sigma_P) g_mn

with

    sigma_P = P / (2 M^4)

and

    P = F_mn *F^(mn).

With mostly-plus convention,

    P = -4 E dot B.

The sign of E relative to B can be chosen so sigma_P has the desired sign.

----------------------------------------------------------------------
1. SAME-ACTION VARIATION
----------------------------------------------------------------------

For the universal conformal physical metric,

    delta S_m
        =
    integral sqrt(-g_phys) T_phys delta sigma.

For

    sigma = P/(2 M^4)

and

    delta P
        =
    2 *F^(mn) delta F_mn
        =
    4 *F^(mn) nabla_m delta A_n,

we obtain

    delta sigma
        =
    (2/M^4) *F^(mn) nabla_m delta A_n.

Therefore the matter contribution to the vector equation is proportional to

    -(2/M^4)
    nabla_m[
        exp(4 sigma) T_phys *F^(mn)
    ].

Using the exact Abelian Bianchi identity

    nabla_m *F^(mn) = 0,

this becomes

    -(2/M^4)
    partial_m[
        exp(4 sigma) T_phys
    ]
    *F^(mn).

Define

    beta(x)
        =
    2 exp(4 sigma) T_phys / M^4.

Then schematically, up to the declared source/sign convention,

    nabla_m F^(mn)
        -
    (partial_m beta) *F^(mn)
        =
    J^n.

This has the standard structural form of axion/theta electrodynamics.

----------------------------------------------------------------------
2. WHY THIS DIFFERS FROM F^2 LOADING
----------------------------------------------------------------------

For A12D1 F^2,

    Z_matter
        =
    1 - 2 exp(4 sigma) T/M^4,

so nonrelativistic matter changes the Maxwell kinetic coefficient throughout
the bulk.

At 1 keV this produced

    Z - 1 ~ O(10^4).

For the linear P portal, if T is spatially constant and sigma is treated to
leading weak-sigma order,

    partial_m beta = 0.

Therefore there is NO leading uniform-bulk matter loading.

The exact conformal factor exp(4 sigma) reintroduces a nonlinear residual:

    partial_m beta
        =
    4 beta partial_m sigma

for constant T.

Because A12C sigma is only O(10^-16), this exact residual can remain tiny even
when |beta| itself is O(10^4).

The finite-payload density-gradient/interface term is NOT tiny:

    partial_m T != 0

near material boundaries or density gradients.

That is the dominant new gate.

----------------------------------------------------------------------
3. AFFINE-PORTAL UNIQUENESS THEOREM
----------------------------------------------------------------------

Consider the broader local conformal family

    sigma = f(P).

At leading weak-sigma order, uniform matter produces a vector variation with
coefficient

    T f'(P) *F.

The Bianchi identity removes the uniform-bulk term only if f'(P) is constant
for arbitrary backgrounds.

Therefore

    f''(P) = 0

and

    f(P) = a + b P.

The constant a is physically irrelevant to the force profile.

Thus:

    linear P

is the unique nontrivial local f(P) portal with exact leading uniform-matter
topological cancellation.

This matters because simple replacements such as

    P^2
    tanh(P)
    rational functions
    saturation functions

generically reintroduce bulk loading.

----------------------------------------------------------------------
4. IDEAL A12C CAPACITY EQUIVALENCE
----------------------------------------------------------------------

The A12C pure magnetic portal is

    sigma_A12C = B_A^2 / M^4

with Maxwell energy density

    u_A12C = B_A^2 / 2.

For the P portal choose locally

    E_new = -B_A / sqrt(2)
    B_new = +B_A / sqrt(2)

with E and B parallel/antiparallel as required by the sign convention.

Then

    P_new
        =
    -4 E_new dot B_new
        =
    +2 B_A^2,

so

    sigma_P
        =
    P_new/(2M^4)
        =
    B_A^2/M^4
        =
    sigma_A12C.

Meanwhile

    u_new
        =
    (E_new^2 + B_new^2)/2
        =
    B_A^2/2
        =
    u_A12C.

Therefore the local invariant-per-canonical-field-energy optimum of the
linear P portal is EXACTLY as good as A12C F^2.

This is an algebraic capacity statement.

It is NOT yet a global Maxwell solution.

The A12C payload lies entirely outside the compact current support, so in the
payload region the magnetostatic B field is curl-free and a local
electrostatic mirror field is integrable.

Inside the current-bearing source region, however, B is not curl-free, so a
global E = -B/sqrt(2) electrostatic realization is not automatically
available.

That is an R3B question.

----------------------------------------------------------------------
5. PARITY / CP
----------------------------------------------------------------------

For an ordinary polar vector gauge field,

    P = F *F = -4 E dot B

is parity odd and CP odd.

Therefore a bare linear P conformal metric explicitly violates P/CP unless its
coefficient carries pseudoscalar transformation character.

There is an important structural conflict:

    parity-even analytic f(P)
        => f(P) even
        => nontrivial f is nonlinear
        => f''(P) != 0 generically
        => leading uniform-bulk topological cancellation is lost.

Thus a single ordinary vector cannot simultaneously have

    nontrivial linear-P cancellation
    +
    exact ordinary parity invariance

without an additional parity-odd structure.

Candidate repairs include:

1. explicit pseudoscalar spurion;
2. dynamical pseudoscalar compensator chi with sigma ~ chi P;
3. cross-topological F_X *F_Y with one vector carrying axial/pseudovector
   parity assignment.

Each has new naturalness, stability, energy and empirical gates.

----------------------------------------------------------------------
6. INTERFACE / DENSITY-GRADIENT PREFLIGHT
----------------------------------------------------------------------

At leading order the matter-induced topological coefficient is

    beta ~= 2 T/M^4.

For nonrelativistic matter,

    T ~= -rho_E.

Hence

    |beta| ~= 2 rho_E/M^4.

This is numerically the same large dimensionless scale that appeared as the
F^2 loading epsilon, but it enters differently:

F^2:
    large coefficient throughout matter bulk.

P portal:
    derivative of the coefficient.

For an abrupt planar beta jump and no independent free surface source, the
theta-like boundary conditions can be represented schematically as

    B_n continuous
    E_t continuous
    D_n = E_n - beta B_n continuous
    H_t = B_t + beta E_t continuous.

For fixed nonzero local E dot B, satisfying both sides of a very large beta
jump can demand substantial field rearrangement.

A local two-side energy-density minimization gives the diagnostic factors

    favorable sign:
        sqrt(2(beta^2 + 2)) - |beta|

    unfavorable sign:
        sqrt(2(beta^2 + 2)) + |beta|.

For |beta| >> 1 the favorable branch scales as

    (sqrt(2)-1)|beta|.

For positive sigma and nonrelativistic T<0, beta*P < 0, selecting the
favorable sign branch automatically.

This abrupt-interface factor is NOT an integrated BVP energy bound.

The project's optimistic payload density is C1 tapered rather than a sharp
step, so a full loaded mixed-E/B solve is required before promotion.

Microscopic atomic density gradients also remain outstanding.

----------------------------------------------------------------------
CLAIM LIMITS
----------------------------------------------------------------------

R3A can establish a structural rescue corridor.

It cannot establish:

- a global E/B field solution;
- a source realization;
- finite-payload loaded BVP success;
- parity completion;
- full hyperbolicity;
- nonlinear stability;
- quantum naturalness;
- empirical consistency;
- complete operating energy;
- a physical antigravity model;
- replacement of 006D;
- a device.

CLAIM CLASSIFICATION
--------------------
PROJECT_THEOREM_FIRST_TOPOLOGICAL_PORTAL_RESCUE_PREFLIGHT
"""

from __future__ import annotations

import json
import math
from functools import lru_cache
from pathlib import Path
from typing import Any


BRANCH = "032H17A12D1R3A"

PORTAL_SCALE_EV = 1000.0

C_LIGHT_M_S = 299792458.0

A12C_REFERENCE_FIELD_ENERGY_J = 2.6568591420597114

A12C_REFERENCE_SIGMA_MAX = 1.3615723178022103e-16

A12C_REFERENCE_MIN_ACCEL_M_S2 = 9.80665

A12C_REFERENCE_STANDOFF_M = 1.0

A12C_SOURCE_RADIUS_M = 2.0

NONLINEAR_BULK_PROXY_PASS_MAX = 1.0e-8

INTERFACE_LARGE_BETA_THRESHOLD = 100.0


def _repo_root() -> Path:
    return (
        Path(__file__)
        .resolve()
        .parents[3]
    )


def _load_json(
    filename: str,
) -> dict[str, Any]:
    path = (
        _repo_root()
        /
        "results"
        /
        "data"
        /
        filename
    )

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


@lru_cache(maxsize=1)
def a12c_artifact() -> dict[str, Any]:
    return _load_json(
        "032h17a12c_hook17_concurrent_u1_fieldstrength_metric_summary.json"
    )


@lru_cache(maxsize=1)
def a12d1_artifact() -> dict[str, Any]:
    return _load_json(
        "032h17a12d1_hook17_pauli_f2_same_action_loading_summary.json"
    )


@lru_cache(maxsize=1)
def r2b1_artifact() -> dict[str, Any]:
    return _load_json(
        "032h17a12d1r2b1_hook17_f2_1kev_grid_complete_source_bound_summary.json"
    )


def provenance_gate() -> dict[str, Any]:
    a12c = (
        a12c_artifact()
    )

    a12d1 = (
        a12d1_artifact()
    )

    r2b1 = (
        r2b1_artifact()
    )

    production = (
        a12c[
            "massless_f2_finite_payload_bvp"
        ][
            "production"
        ]
    )

    passed = bool(
        math.isclose(
            float(
                production[
                    "field_energy_j"
                ]
            ),
            A12C_REFERENCE_FIELD_ENERGY_J,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        )

        and

        math.isclose(
            float(
                production[
                    "payload_sigma_max"
                ]
            ),
            A12C_REFERENCE_SIGMA_MAX,
            rel_tol=1.0e-12,
            abs_tol=0.0,
        )

        and

        a12d1[
            "same_action_variation"
        ][
            "finite_matter_quadratic_loading_present"
        ]
        is True

        and

        r2b1[
            "a12c_2p656859j_ruled_out_on_both_grids"
        ]
        is True

        and

        r2b1[
            "continuous_source_space_exhausted"
        ]
        is False

        and

        r2b1[
            "a12b_exact_massless_carrier_closed"
        ]
        is False

        and

        r2b1[
            "a12c_f2_metric_mechanism_closed"
        ]
        is False
    )

    return {
        "pass":
            passed,

        "a12c_field_energy_j":
            production[
                "field_energy_j"
            ],

        "a12c_sigma_max":
            production[
                "payload_sigma_max"
            ],

        "a12c_standoff_m":
            production[
                "geometric_external_standoff_m"
            ],

        "a12c_loaded_matter_included":
            production[
                "loaded_matter_backreaction_included"
            ],

        "a12d1_f2_loading_present":
            a12d1[
                "same_action_variation"
            ][
                "finite_matter_quadratic_loading_present"
            ],

        "r2b1_few_joule_source_shaping_ruled_out":
            r2b1[
                "a12c_2p656859j_ruled_out_on_both_grids"
            ],

        "r2b1_fine_grid_capacity_floor_j":
            r2b1[
                "fine_grid_certified_loaded_capacity_floor_j"
            ],

        "r2b1_a12c_response_gap_factor":
            r2b1[
                "a12c_reference_response_gap_factor_on_fine_grid"
            ],

        "a12b_carrier_preserved":
            not r2b1[
                "a12b_exact_massless_carrier_closed"
            ],

        "a12c_mechanism_preserved":
            not r2b1[
                "a12c_f2_metric_mechanism_closed"
            ],
    }


def same_action_variation_gate() -> dict[str, Any]:
    return {
        "physical_metric":
            "g_phys_mn=exp(2*sigma_P)*g_mn",

        "portal_invariant":
            "P=F_mn*F^(mn)=-4 E dot B",

        "sigma":
            "sigma_P=P/(2*M^4)",

        "matter_metric_variation":
            "deltaS_m=int[sqrt(-g_phys)*T_phys*delta_sigma]",

        "delta_P":
            "deltaP=2*Fdual^(mn)*deltaF_mn=4*Fdual^(mn)*nabla_m(deltaA_n)",

        "delta_sigma":
            "delta_sigma=(2/M^4)*Fdual^(mn)*nabla_m(deltaA_n)",

        "matter_vector_variation":
            "-(2/M^4)*nabla_m[exp(4*sigma)*T_phys*Fdual^(mn)]",

        "bianchi_identity":
            "nabla_m Fdual^(mn)=0",

        "reduced_matter_term":
            "-(2/M^4)*partial_m[exp(4*sigma)*T_phys]*Fdual^(mn)",

        "beta_definition":
            "beta=2*exp(4*sigma)*T_phys/M^4",

        "schematic_same_action_equation":
            "nabla_m F^(mn)-(partial_m beta)*Fdual^(mn)=J^n",

        "leading_constant_trace_bulk_loading_zero":
            True,

        "exact_constant_trace_bulk_loading_zero":
            False,

        "exact_residual_origin":
            "partial_m exp(4*sigma)=4*exp(4*sigma)*partial_m sigma",

        "gauge_invariant":
            True,

        "off_state_linear_source":
            False,

        "equations_at_most_second_order_in_A":
            True,
    }


def affine_bulk_cancellation_theorem() -> dict[str, Any]:
    return {
        "family":
            "sigma=f(P)",

        "leading_uniform_matter_coefficient":
            "T*f_prime(P)",

        "uniform_bulk_derivative":
            "T*f_double_prime(P)*partial_m(P)",

        "cancellation_for_arbitrary_background_requires":
            "f_double_prime(P)=0",

        "general_solution":
            "f(P)=a+b*P",

        "constant_a_force_irrelevant":
            True,

        "linear_P_unique_nontrivial_local_fP_bulk_cancellation":
            True,

        "P_squared_preserves_bulk_cancellation":
            False,

        "generic_saturating_function_preserves_bulk_cancellation":
            False,

        "generic_rational_function_preserves_bulk_cancellation":
            False,

        "nontrivial_analytic_parity_even_fP_can_be_affine":
            False,
    }


def ideal_capacity_equivalence_gate() -> dict[str, Any]:
    a12c = (
        a12c_artifact()
    )

    production = (
        a12c[
            "massless_f2_finite_payload_bvp"
        ][
            "production"
        ]
    )

    field_energy = float(
        production[
            "field_energy_j"
        ]
    )

    sigma_max = float(
        production[
            "payload_sigma_max"
        ]
    )

    mirror_amplitude_ratio = (
        1.0
        /
        math.sqrt(
            2.0
        )
    )

    p_over_ba2 = 2.0

    sigma_ratio = (
        p_over_ba2
        /
        2.0
    )

    energy_ratio = (
        mirror_amplitude_ratio**2
        +
        mirror_amplitude_ratio**2
    )

    ideal_mixed_energy = (
        field_energy
        *
        energy_ratio
    )

    payload_rest_shift_upper_j = (
        C_LIGHT_M_S**2
        *
        sigma_max
    )

    return {
        "a12c_reference_field_energy_j":
            field_energy,

        "a12c_reference_sigma_max":
            sigma_max,

        "mirror_E_over_BA":
            -mirror_amplitude_ratio,

        "mirror_B_over_BA":
            mirror_amplitude_ratio,

        "mirror_P_over_BA_squared":
            p_over_ba2,

        "mirror_sigma_over_a12c_sigma":
            sigma_ratio,

        "mirror_canonical_energy_over_a12c_energy":
            energy_ratio,

        "ideal_mixed_EB_field_energy_j":
            ideal_mixed_energy,

        "ideal_capacity_exactly_equal_to_a12c":
            math.isclose(
                ideal_mixed_energy,
                field_energy,
                rel_tol=0.0,
                abs_tol=1.0e-14,
            ),

        "local_bound":
            "u=(E^2+B^2)/2 >= |P|/4",

        "bound_saturated_when":
            "|E|=|B| and E parallel_or_antiparallel B",

        "payload_rest_energy_conformal_shift_upper_j":
            payload_rest_shift_upper_j,

        "payload_entirely_outside_current_support":
            bool(
                float(
                    production[
                        "geometric_external_standoff_m"
                    ]
                )
                >
                0.0
            ),

        "payload_region_magnetic_field_curl_free_in_source_free_limit":
            True,

        "local_electrostatic_mirror_integrable_in_payload_region":
            True,

        "global_electrostatic_mirror_integrable_through_current_source":
            False,

        "global_mirror_field_solution_established":
            False,

        "new_global_BVP_required":
            True,
    }


def loading_structure_gate() -> dict[str, Any]:
    a12d1 = (
        a12d1_artifact()
    )

    r2b1 = (
        r2b1_artifact()
    )

    rho_average_ev4 = float(
        a12d1[
            "payload_average_density"
        ][
            "average_payload_rest_energy_density_ev4"
        ]
    )

    epsilon_average = (
        2.0
        *
        rho_average_ev4
        /
        PORTAL_SCALE_EV**4
    )

    fine_grid = min(
        r2b1[
            "grid_results"
        ],
        key=lambda row:
            float(
                row[
                    "grid_spacing_m"
                ]
            ),
    )

    f2_peak_z = float(
        fine_grid[
            "z_max"
        ]
    )

    epsilon_peak = (
        f2_peak_z
        -
        1.0
    )

    sigma_max = (
        A12C_REFERENCE_SIGMA_MAX
    )

    exp_4sigma = math.exp(
        4.0
        *
        sigma_max
    )

    beta_average = (
        epsilon_average
        *
        exp_4sigma
    )

    beta_peak = (
        epsilon_peak
        *
        exp_4sigma
    )

    nonlinear_bulk_principal_proxy_average = (
        4.0
        *
        beta_average
        *
        sigma_max
    )

    nonlinear_bulk_principal_proxy_peak = (
        4.0
        *
        beta_peak
        *
        sigma_max
    )

    suppression_factor = (
        epsilon_peak
        /
        nonlinear_bulk_principal_proxy_peak
    )

    return {
        "portal_scale_ev":
            PORTAL_SCALE_EV,

        "average_rest_energy_density_ev4":
            rho_average_ev4,

        "f2_average_bulk_loading_epsilon":
            epsilon_average,

        "f2_peak_bulk_loading_epsilon":
            epsilon_peak,

        "topological_beta_average_magnitude":
            beta_average,

        "topological_beta_peak_magnitude":
            beta_peak,

        "leading_uniform_bulk_loading_exactly_zero":
            True,

        "exact_uniform_bulk_nonlinear_principal_proxy_average":
            nonlinear_bulk_principal_proxy_average,

        "exact_uniform_bulk_nonlinear_principal_proxy_peak":
            nonlinear_bulk_principal_proxy_peak,

        "nonlinear_bulk_proxy_pass":
            nonlinear_bulk_principal_proxy_peak
            <
            NONLINEAR_BULK_PROXY_PASS_MAX,

        "f2_bulk_vs_topological_residual_suppression_factor":
            suppression_factor,

        "density_gradient_coefficient_remains_large":
            beta_peak
            >
            INTERFACE_LARGE_BETA_THRESHOLD,

        "dominant_loaded_problem_changes_from_bulk_to_interface":
            True,
    }


def planar_interface_penalty(
    beta: float,
) -> dict[str, float]:
    magnitude = abs(
        float(
            beta
        )
    )

    root = math.sqrt(
        2.0
        *
        (
            magnitude**2
            +
            2.0
        )
    )

    return {
        "favorable_energy_density_factor":
            root
            -
            magnitude,

        "unfavorable_energy_density_factor":
            root
            +
            magnitude,
    }


def interface_gate() -> dict[str, Any]:
    loading = (
        loading_structure_gate()
    )

    beta_average = float(
        loading[
            "topological_beta_average_magnitude"
        ]
    )

    beta_peak = float(
        loading[
            "topological_beta_peak_magnitude"
        ]
    )

    average_penalty = (
        planar_interface_penalty(
            beta_average
        )
    )

    peak_penalty = (
        planar_interface_penalty(
            beta_peak
        )
    )

    heuristic_average_energy_j = (
        A12C_REFERENCE_FIELD_ENERGY_J
        *
        average_penalty[
            "favorable_energy_density_factor"
        ]
    )

    heuristic_peak_energy_j = (
        A12C_REFERENCE_FIELD_ENERGY_J
        *
        peak_penalty[
            "favorable_energy_density_factor"
        ]
    )

    return {
        "boundary_conditions":
            {
                "B_normal":
                    "continuous",

                "E_tangential":
                    "continuous",

                "D_normal":
                    "E_n-beta*B_n continuous",

                "H_tangential":
                    "B_t+beta*E_t continuous",
            },

        "positive_sigma_and_nonrelativistic_T_select_favorable_sign":
            True,

        "reason":
            "beta*P=4*T*sigma<0 for T<0 and sigma>0 at leading order",

        "average_beta_magnitude":
            beta_average,

        "peak_beta_magnitude":
            beta_peak,

        "average_favorable_local_energy_density_factor":
            average_penalty[
                "favorable_energy_density_factor"
            ],

        "peak_favorable_local_energy_density_factor":
            peak_penalty[
                "favorable_energy_density_factor"
            ],

        "average_unfavorable_local_energy_density_factor":
            average_penalty[
                "unfavorable_energy_density_factor"
            ],

        "peak_unfavorable_local_energy_density_factor":
            peak_penalty[
                "unfavorable_energy_density_factor"
            ],

        "naive_if_favorable_factor_applied_to_entire_a12c_field_average_j":
            heuristic_average_energy_j,

        "naive_if_favorable_factor_applied_to_entire_a12c_field_peak_j":
            heuristic_peak_energy_j,

        "heuristic_global_energy_is_rigorous_bound":
            False,

        "abrupt_step_is_actual_payload_density_model":
            False,

        "actual_optimistic_payload_density_is_C1_tapered":
            True,

        "smooth_taper_may_reduce_abrupt_interface_penalty":
            True,

        "P_node_or_polarization_rotation_in_density_gradient_layer_is_open":
            True,

        "microscopic_atomic_density_gradient_homogenization_completed":
            False,

        "full_interface_loaded_BVP_required":
            True,
    }


def parity_gate() -> dict[str, Any]:
    return {
        "ordinary_vector_P_is_parity_odd":
            True,

        "ordinary_vector_P_is_C_even":
            True,

        "ordinary_vector_P_is_CP_odd":
            True,

        "bare_linear_P_metric_preserves_parity":
            False,

        "bare_linear_P_metric_preserves_CP":
            False,

        "analytic_parity_even_single_vector_fP_must_be_even_in_P":
            True,

        "nontrivial_even_fP_is_affine":
            False,

        "parity_even_single_vector_and_exact_leading_topological_cancellation_compatible_without_extra_structure":
            False,

        "repair_requires_additional_parity_odd_structure":
            True,

        "repair_options":
            [
                "EXPLICIT_PSEUDOSCALAR_SPURION",
                "DYNAMICAL_PSEUDOSCALAR_COMPENSATOR_CHI_TIMES_P",
                "VECTOR_AXIAL_CROSS_TOPOLOGICAL_FX_DUAL_FY",
            ],

        "parity_problem_is_mathematical_inconsistency":
            False,

        "parity_problem_is_model_building_and_empirical_gate":
            True,
    }


def health_and_ward_gate() -> dict[str, Any]:
    return {
        "portal_is_gauge_invariant":
            True,

        "matter_induced_current":
            "Jmatter^n=(2/M^4)*nabla_m[exp(4*sigma)*T*Fdual^(mn)] up to source-sign convention",

        "matter_induced_current_identically_conserved":
            True,

        "conservation_reason":
            "double divergence of antisymmetric rank-2 tensor vanishes",

        "off_state_F_zero_implies_portal_source_zero":
            True,

        "field_equations_second_order":
            True,

        "higher_time_derivative_ostrogradsky_from_portal":
            False,

        "free_Maxwell_sector_positive_energy":
            True,

        "constant_beta_topological_term_changes_local_Maxwell_bulk_equations":
            False,

        "variable_beta_changes_field_equations":
            True,

        "full_interacting_hyperbolicity_certified":
            False,

        "finite_interface_characteristics_certified":
            False,

        "Einstein_metric_stress_backreaction_certified":
            False,

        "quantum_naturalness_certified":
            False,

        "radiative_lower_dimension_mixing_certified":
            False,

        "empirical_constraints_certified":
            False,

        "complete_energy_certified":
            False,
    }


def rescue_portal_atlas() -> list[dict[str, Any]]:
    return [
        {
            "priority":
                1,

            "portal":
                "SINGLE_VECTOR_LINEAR_P_MECHANISM_DIAGNOSTIC",

            "schematic":
                "sigma=P/(2*M^4)",

            "ideal_a12c_capacity_preserved":
                True,

            "leading_uniform_bulk_cancellation":
                True,

            "ordinary_parity_preserved":
                False,

            "extra_field_required":
                False,

            "status":
                "STRUCTURALLY_OPEN_PARITY_AND_INTERFACE_GATES",

            "next_falsifier":
                "GLOBAL_MIRROR_FIELD_PLUS_FINITE_DENSITY_GRADIENT_TRANSFER",
        },
        {
            "priority":
                2,

            "portal":
                "PSEUDOSCALAR_COMPENSATED_LINEAR_P",

            "schematic":
                "sigma=(chi/f)*P/(2*M^4)",

            "ideal_a12c_capacity_preserved":
                True,

            "leading_uniform_bulk_cancellation":
                True,

            "ordinary_parity_preserved":
                True,

            "extra_field_required":
                True,

            "status":
                "OPEN_IF_CHI_APPROX_CONSTANT_AND_HEALTHY",

            "next_falsifier":
                "CHI_VEV_ENERGY_STABILITY_DOMAIN_WALL_AND_GRADIENT_COST",
        },
        {
            "priority":
                3,

            "portal":
                "VECTOR_AXIAL_CROSS_TOPOLOGICAL",

            "schematic":
                "sigma=F_X*F_Y/(2*M^4)",

            "ideal_a12c_capacity_preserved":
                "CONDITIONAL",

            "leading_uniform_bulk_cancellation":
                True,

            "ordinary_parity_preserved":
                "POSSIBLE_WITH_VECTOR_AXIAL_ASSIGNMENT",

            "extra_field_required":
                True,

            "status":
                "OPEN_NEW_CARRIER_ACTION_REQUIRED",

            "next_falsifier":
                "EXACT_PROTECTED_AXIAL_OR_PSEUDOVECTOR_CARRIER_AND_CROSS_SOURCE",
        },
        {
            "priority":
                4,

            "portal":
                "PARITY_EVEN_P_SQUARED",

            "schematic":
                "sigma~P^2/Lambda^8",

            "ideal_a12c_capacity_preserved":
                False,

            "leading_uniform_bulk_cancellation":
                False,

            "ordinary_parity_preserved":
                True,

            "extra_field_required":
                False,

            "status":
                "DEPRIORITIZED_BULK_LOADING_RETURNS",

            "next_falsifier":
                "ONLY_REVISIT_WITH_GENUINELY_NEW_PROTECTION",
        },
        {
            "priority":
                5,

            "portal":
                "RETURN_TO_1KEV_F2_SOURCE_SHAPING",

            "schematic":
                "sigma=F^2/(2*M^4)",

            "ideal_a12c_capacity_preserved":
                True,

            "leading_uniform_bulk_cancellation":
                False,

            "ordinary_parity_preserved":
                True,

            "extra_field_required":
                False,

            "status":
                "CLOSED_SCOPED_BY_R2B1_FOR_AXISYMMETRIC_ORIGINAL_SUPPORT_GRID_SPACE",

            "next_falsifier":
                "NONE_WITHOUT_GENUINELY_NEW_PHYSICS",
        },
    ]


def r3a_summary() -> dict[str, Any]:
    provenance = (
        provenance_gate()
    )

    variation = (
        same_action_variation_gate()
    )

    theorem = (
        affine_bulk_cancellation_theorem()
    )

    capacity = (
        ideal_capacity_equivalence_gate()
    )

    loading = (
        loading_structure_gate()
    )

    interface = (
        interface_gate()
    )

    parity = (
        parity_gate()
    )

    health = (
        health_and_ward_gate()
    )

    atlas = (
        rescue_portal_atlas()
    )

    structural_rescue_survives = bool(
        provenance[
            "pass"
        ]

        and

        variation[
            "leading_constant_trace_bulk_loading_zero"
        ]

        and

        theorem[
            "linear_P_unique_nontrivial_local_fP_bulk_cancellation"
        ]

        and

        capacity[
            "ideal_capacity_exactly_equal_to_a12c"
        ]

        and

        loading[
            "nonlinear_bulk_proxy_pass"
        ]

        and

        health[
            "portal_is_gauge_invariant"
        ]

        and

        health[
            "matter_induced_current_identically_conserved"
        ]

        and

        health[
            "field_equations_second_order"
        ]
    )

    dominant_remaining_gate = (
        "FINITE_DENSITY_GRADIENT_INTERFACE_MIXING_PLUS_GLOBAL_EB_REALIZATION"
        if structural_rescue_survives
        else
        "R3A_THEOREM_OR_HEALTH_FAILURE"
    )

    if (
        structural_rescue_survives
        and
        loading[
            "density_gradient_coefficient_remains_large"
        ]
        and
        parity[
            "repair_requires_additional_parity_odd_structure"
        ]
    ):
        decision = (
            "YELLOW_GREEN_SCOPED_R3A_LINEAR_FDUALF_PRESERVES_"
            "THE_IDEAL_A12C_2P656859J_INVARIANT_PER_FIELD_ENERGY_"
            "AND_REMOVES_THE_FATAL_LEADING_UNIFORM_BULK_LOADING__"
            "EXACT_NONLINEAR_BULK_RESIDUAL_IS_TINY__"
            "FINITE_DENSITY_GRADIENT_INTERFACE_MIXING_AND_PARITY_CP_"
            "COMPLETION_ARE_NOW_THE_DOMINANT_GATES__AUTHORIZE_R3B"
        )

        next_branch = (
            "032H17A12D1R3B_GLOBAL_MIRROR_FIELD_"
            "INTEGRABILITY_AND_DENSITY_GRADIENT_TRANSFER_PREFLIGHT"
        )

    elif structural_rescue_survives:
        decision = (
            "YELLOW_SCOPED_R3A_TOPOLOGICAL_RESCUE_SURVIVES_"
            "THEOREM_GATE_BUT_REQUIRES_REVIEW"
        )

        next_branch = (
            "REVIEW_R3A_INTERFACE_AND_PARITY_STRUCTURE"
        )

    else:
        decision = (
            "RED_SCOPED_R3A_LINEAR_FDUALF_DOES_NOT_SURVIVE_"
            "CHEAP_SAME_ACTION_THEOREM_GATE"
        )

        next_branch = (
            "BUILD_CARRYOVER_NOTES_AND_RERANK_OTHER_A12D0_PORTALS"
        )

    return {
        "branch":
            BRANCH,

        "decision":
            decision,

        "provenance":
            provenance,

        "same_action_variation":
            variation,

        "affine_bulk_cancellation_theorem":
            theorem,

        "ideal_a12c_capacity_equivalence":
            capacity,

        "loading_structure":
            loading,

        "interface_prefight":
            interface,

        "parity_cp":
            parity,

        "health_and_ward":
            health,

        "rescue_portal_atlas":
            atlas,

        "structural_rescue_survives_cheap_gate":
            structural_rescue_survives,

        "dominant_remaining_gate":
            dominant_remaining_gate,

        "r3b_authorized":
            structural_rescue_survives,

        "full_loaded_EB_BVP_authorized_immediately":
            False,

        "a12b_exact_massless_carrier_closed":
            False,

        "a12c_low_capacity_clue_discarded":
            False,

        "a12c_f2_metric_mechanism_globally_closed":
            False,

        "mixed_eb_topological_portal_closed":
            not structural_rescue_survives,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "006d_replaced":
            False,

        "practical_device_found":
            False,

        "hook17_closed":
            False,

        "next":
            next_branch,
    }
