"""032H17A10F2 — strict payload floor + source naturalness closeout.

PURPOSE
-------
A10F1 established a converged reduced-EFT finite-source/finite-payload
witness:

    finite compact transverse source
    1 kg neutral toroidal payload
    1.0 m minimum geometric source/payload gap
    1 g outward center-of-mass response
    corrected canonical pair pole coupling = 2
    field/loading energy ~0.215 MJ

Before spending compute on source confinement, nonlinear evolution, or
engineering, this gate addresses two cheaper questions.

1. STRICT FINITE-PAYLOAD FLOOR

A10F1's COM acceleration reaches 1 g, but the least-accelerated payload
element receives only ~3.74 m/s^2.

For the fixed reduced BVP:

    V scales linearly with source amplitude A
    sigma=lambda V^2 scales as A^2
    acceleration scales as A^2
    canonical field energy scales as A^2
    microscopic source number scales as A

Therefore the A10F1 numerical solution can be rescaled exactly so that the
minimum local payload acceleration, not merely COM acceleration, reaches
9.80665 m/s^2.

2. MICROSCOPIC ULTRALIGHT NATURALNESS

The physically normalized carrier has

    m_V = |f| = 1.973269804e-7 eV

for a one-metre range.

A10F1 repaired Wheeler's normalization and established a canonical engineered
pair pole coupling of magnitude

    g_pair = 2.

Because a pair amplitude is a sum of two constituent amplitudes, the triangle
inequality gives the conservative exact lower bound

    max(|g_1|, |g_2|) >= |g_pair|/2 = 1.

The existing Wheeler normalization parameter alpha cancels after canonical
fermion normalization; it is therefore not available as a small physical
coupling knob in the current realization.

PROTECTION AUDIT
----------------
A10C established that the bare engineered connection current does not obey the
required Abelian Ward relation identically; a Stueckelberg scalar completion
was required.

The invariant combination is schematically

    B_mu = A_mu - partial_mu(phi)/f.

Hence the same symmetry permits a local B^2 mass operator.

Therefore the currently demonstrated Stueckelberg symmetry protects the
constraint/ghost structure but does not, by itself, establish a
non-renormalization theorem for an arbitrarily tiny coefficient of B^2 once
the Wheeler matter sector is added.

No exact operator-level conservation theorem for the engineered Wheeler
current has yet been established.

LONGITUDINAL DIAGNOSTIC
-----------------------
For a nonconserved current coupled to B, the longitudinal scalar interaction
contains the characteristic enhancement

    g E / |f|.

For the conservative constituent coupling lower bound g>=1, the electron
threshold gives

    m_e/|f| ~ 2.6e12.

We report the NDA perturbative scale

    Lambda_long ~ 4 pi |f| / g.

This is NOT asserted to be an exact unitarity cutoff of the full unknown UV
completion.

It is a diagnostic showing how much additional current conservation or
Higgs/Noether completion would be needed.

MASS-THRESHOLD NDA
------------------
Because B^2 is symmetry allowed and no exact current-conservation protection
has been demonstrated, use the conservative technical-naturalness estimator

    delta m_V^2
      ~
    c_loop * g^2 * m_f^2 / (16 pi^2).

This is explicitly:

    NOT an exact beta function
    NOT a scheme-independent finite threshold calculation
    NOT a theorem against all protected MAG vector theories.

It is the same type of early technical-naturalness falsifier used previously
in 031F0.

HYPOTHETICAL SMALL-COUPLING ESCAPE
----------------------------------
For diagnostic purposes only, introduce a hypothetical epsilon multiplying the
entire microscopic Wheeler current.

This epsilon DOES NOT EXIST as a free physical coupling in the current
canonical Wheeler action.

If it existed:

    required source number/rest energy scales as 1/epsilon

while

    naturalness and longitudinal control improve with epsilon.

This lets us ask whether a simple weak-coupling rescue would have simultaneous
energy and naturalness headroom even as hypothetical new physics.

CLAIM SCOPE
-----------
A RED result means:

    the CURRENT ordinary-Dirac Wheeler + meter-range Marzo implementation is
    blocked on technical naturalness and should not proceed to expensive
    support/nonlinear simulations without genuinely new protection.

It does NOT erase:

    A10A microscopic source-state escape
    A10C Stueckelberg source completion
    A10D healthy protected pole overlap
    A10E quadratic universal-metric mechanism
    A10F1 finite reduced-EFT payload witness.

It does NOT globally close HOOK17 or every protected massive 1- MAG family.
"""

from __future__ import annotations

import math
from functools import lru_cache
from typing import Any

from .hook17_marzo2022_engineered_stueckelberg_noether import (
    h17a10c_summary,
)
from .hook17_marzo_finite_transverse_payload_bvp import (
    h17a10f1_summary,
)


TARGET_ACCELERATION_M_S2 = 9.80665
STRICT_COMPLETE_OPERATING_TARGET_J = 1.0e7

ELECTRON_MASS_EV = 510998.95
HBAR_C_EV_M = 1.973269804e-7

LOOP_COEFFICIENTS = (
    1.0,
    1.0e-3,
    1.0e-6,
    1.0e-9,
    1.0e-12,
)


@lru_cache(maxsize=1)
def strict_payload_floor_rescale() -> dict[str, Any]:
    """Rescale A10F1 so every sampled payload point reaches >=1 g."""

    previous = h17a10f1_summary()

    bvp = previous[
        "primary_torus_payload_bvp"
    ]

    source_energy = previous[
        "source_rest_energy"
    ]

    old_min = float(
        bvp[
            "payload_local_outward_acceleration_min_m_s2"
        ]
    )

    if old_min <= 0.0:
        raise ValueError(
            "A10F1 minimum payload acceleration must be positive"
        )

    acceleration_scale = (
        TARGET_ACCELERATION_M_S2
        /
        old_min
    )

    amplitude_scale = math.sqrt(
        acceleration_scale
    )

    scaled_min = (
        old_min
        *
        acceleration_scale
    )

    scaled_max = (
        float(
            bvp[
                "payload_local_outward_acceleration_max_m_s2"
            ]
        )
        *
        acceleration_scale
    )

    scaled_com = (
        float(
            bvp[
                "payload_com_outward_acceleration_m_s2"
            ]
        )
        *
        acceleration_scale
    )

    field_energy = (
        float(
            bvp[
                "field_loading_energy_j"
            ]
        )
        *
        acceleration_scale
    )

    source_work_energy = (
        float(
            bvp[
                "source_work_energy_j"
            ]
        )
        *
        acceleration_scale
    )

    pair_count = (
        float(
            bvp[
                "source_pair_count"
            ]
        )
        *
        amplitude_scale
    )

    peak_pair_density = (
        float(
            bvp[
                "peak_pair_density_m3"
            ]
        )
        *
        amplitude_scale
    )

    average_pair_density = (
        float(
            bvp[
                "average_pair_density_m3"
            ]
        )
        *
        amplitude_scale
    )

    electron_rest = (
        float(
            source_energy[
                "electron_positron_rest_energy_floor_j"
            ]
        )
        *
        amplitude_scale
    )

    proton_rest = (
        float(
            source_energy[
                "proton_antiproton_rest_energy_comparator_j"
            ]
        )
        *
        amplitude_scale
    )

    field_plus_electron = (
        field_energy
        +
        electron_rest
    )

    field_plus_proton = (
        field_energy
        +
        proton_rest
    )

    return {
        "original_local_min_acceleration_m_s2":
            old_min,

        "required_acceleration_energy_scale":
            acceleration_scale,

        "required_field_source_amplitude_scale":
            amplitude_scale,

        "strict_local_min_acceleration_m_s2":
            scaled_min,

        "strict_payload_com_acceleration_m_s2":
            scaled_com,

        "strict_local_max_acceleration_m_s2":
            scaled_max,

        "strict_minimum_local_payload_floor_pass":
            bool(
                scaled_min
                >=
                TARGET_ACCELERATION_M_S2
                *
                (
                    1.0
                    -
                    1.0e-12
                )
            ),

        "geometric_external_standoff_m":
            float(
                bvp[
                    "geometric_external_standoff_m"
                ]
            ),

        "reduced_eft_1g_1m_strict_payload_performance_pass":
            bool(
                scaled_min
                >=
                TARGET_ACCELERATION_M_S2
                *
                (
                    1.0
                    -
                    1.0e-12
                )
                and
                float(
                    bvp[
                        "geometric_external_standoff_m"
                    ]
                )
                >=
                1.0
                -
                1.0e-12
            ),

        "strict_field_loading_energy_j":
            field_energy,

        "strict_source_work_energy_j":
            source_work_energy,

        "strict_source_pair_count":
            pair_count,

        "strict_peak_pair_density_m3":
            peak_pair_density,

        "strict_average_pair_density_m3":
            average_pair_density,

        "strict_electron_positron_rest_floor_j":
            electron_rest,

        "strict_proton_antiproton_rest_comparator_j":
            proton_rest,

        "strict_field_plus_electron_rest_partial_j":
            field_plus_electron,

        "strict_field_plus_proton_rest_partial_j":
            field_plus_proton,

        "electron_partial_below_10mj":
            bool(
                field_plus_electron
                <
                STRICT_COMPLETE_OPERATING_TARGET_J
            ),

        "proton_mass_comparator_partial_below_10mj":
            bool(
                field_plus_proton
                <
                STRICT_COMPLETE_OPERATING_TARGET_J
            ),

        "partial_energy_is_complete_energy":
            False,
    }


@lru_cache(maxsize=1)
def microscopic_coupling_lower_bound() -> dict[str, Any]:
    """Extract an exact conservative constituent coupling lower bound."""

    previous = h17a10f1_summary()

    normalization = previous[
        "source_normalization"
    ]

    pair_coupling = abs(
        float(
            previous[
                "corrected_canonical_pair_pole_coupling"
            ]
        )
    )

    constituent_lower_bound = (
        pair_coupling
        /
        2.0
    )

    return {
        "canonical_engineered_pair_pole_coupling":
            pair_coupling,

        "constituent_coupling_lower_bound":
            constituent_lower_bound,

        "lower_bound_reason":
            (
                "TRIANGLE_INEQUALITY_FOR_TWO_CONSTITUENT_"
                "AMPLITUDES"
            ),

        "at_least_one_constituent_order_unity":
            bool(
                constituent_lower_bound
                >=
                1.0
            ),

        "wheeler_alpha_cancels_after_canonicalization":
            bool(
                normalization[
                    "alpha_cancels_from_canonical_bare_current"
                ]
            ),

        "current_action_has_free_small_source_coupling":
            False,

        "source_overlap_survived_normalization_repair":
            bool(
                normalization[
                    "a10d_nonzero_pole_overlap_survives_normalization_repair"
                ]
            ),
    }


@lru_cache(maxsize=1)
def stueckelberg_protection_audit() -> dict[str, Any]:
    """Audit what the currently demonstrated symmetry does and does not protect."""

    a10c = h17a10c_summary()

    previous = h17a10f1_summary()

    f_ev = abs(
        float(
            previous[
                "physical_family"
            ][
                "stueckelberg_f_ev"
            ]
        )
    )

    direct_not_conserved = bool(
        a10c[
            "both_engineered_direct_pure_connection_ward_fail_generic"
        ]
    )

    completed = bool(
        a10c[
            "both_engineered_stueckelberg_completed_ward_pass"
        ]
    )

    return {
        "stueckelberg_f_abs_ev":
            f_ev,

        "one_metre_carrier_mass_ev":
            f_ev,

        "bare_engineered_connection_current_ward_identity":
            not direct_not_conserved,

        "stueckelberg_completion_required":
            direct_not_conserved,

        "stueckelberg_completed_ward_pass":
            completed,

        "invariant_field_combination":
            "B=A-dphi/f",

        "B_squared_mass_operator_stueckelberg_invariant":
            True,

        "tiny_B_squared_coefficient_forbidden_by_current_symmetry":
            False,

        "operator_level_exact_engineered_current_conservation_established":
            False,

        "matter_loop_nonrenormalization_theorem_established":
            False,

        "higgs_radial_completion_established":
            False,

        "additional_chiral_or_noether_mass_protection_established":
            False,

        "ghost_tachyon_structural_protection_is_same_as_ultralight_mass_naturalness":
            False,

        "quantitative_ultralight_mass_naturalness_certified":
            False,
    }


def longitudinal_stueckelberg_diagnostic() -> dict[str, Any]:
    """Return the microscopic E/f longitudinal-enhancement diagnostic."""

    protection = (
        stueckelberg_protection_audit()
    )

    coupling = (
        microscopic_coupling_lower_bound()
    )

    f_ev = float(
        protection[
            "stueckelberg_f_abs_ev"
        ]
    )

    g_lower = float(
        coupling[
            "constituent_coupling_lower_bound"
        ]
    )

    electron_over_f = (
        ELECTRON_MASS_EV
        /
        f_ev
    )

    longitudinal_at_electron = (
        g_lower
        *
        electron_over_f
    )

    nominal_scale_ev = (
        4.0
        *
        math.pi
        *
        f_ev
        /
        g_lower
    )

    nominal_length_m = (
        HBAR_C_EV_M
        /
        nominal_scale_ev
    )

    electron_over_nominal_scale = (
        ELECTRON_MASS_EV
        /
        nominal_scale_ev
    )

    previous = h17a10f1_summary()

    source_q_over_f = float(
        previous[
            "source_characteristic_q_over_abs_f"
        ]
    )

    return {
        "constituent_coupling_lower_bound":
            g_lower,

        "stueckelberg_f_abs_ev":
            f_ev,

        "electron_mass_ev":
            ELECTRON_MASS_EV,

        "electron_energy_over_f":
            electron_over_f,

        "longitudinal_enhancement_gE_over_f_at_electron_threshold":
            longitudinal_at_electron,

        "nominal_4pi_f_over_g_scale_ev":
            nominal_scale_ev,

        "nominal_4pi_f_over_g_length_m":
            nominal_length_m,

        "electron_mass_over_nominal_perturbative_scale":
            electron_over_nominal_scale,

        "macroscopic_device_source_q_over_f":
            source_q_over_f,

        "macroscopic_device_source_gradient_is_the_uv_test":
            False,

        "exact_unitarity_cutoff_computed":
            False,

        "full_uv_completion_computed":
            False,

        "additional_exact_current_protection_required":
            True,
    }


def fermion_threshold_mass_nda(
    *,
    fermion_mass_ev: float = ELECTRON_MASS_EV,
    loop_coefficient: float = 1.0,
) -> dict[str, Any]:
    """Return conservative mass-threshold technical-naturalness NDA."""

    mass_f = float(
        fermion_mass_ev
    )

    coefficient = float(
        loop_coefficient
    )

    if (
        mass_f <= 0.0
        or
        coefficient <= 0.0
    ):
        raise ValueError(
            "fermion mass and loop coefficient must be positive"
        )

    protection = (
        stueckelberg_protection_audit()
    )

    coupling = (
        microscopic_coupling_lower_bound()
    )

    mass_vector = float(
        protection[
            "one_metre_carrier_mass_ev"
        ]
    )

    g_lower = float(
        coupling[
            "constituent_coupling_lower_bound"
        ]
    )

    intended_mass_squared = (
        mass_vector**2
    )

    nda_delta_mass_squared = (
        coefficient
        *
        g_lower**2
        *
        mass_f**2
        /
        (
            16.0
            *
            math.pi**2
        )
    )

    ratio = (
        nda_delta_mass_squared
        /
        intended_mass_squared
    )

    induced_mass_ev = math.sqrt(
        nda_delta_mass_squared
    )

    induced_range_m = (
        HBAR_C_EV_M
        /
        induced_mass_ev
    )

    return {
        "fermion_mass_ev":
            mass_f,

        "loop_coefficient":
            coefficient,

        "constituent_coupling_lower_bound":
            g_lower,

        "intended_vector_mass_ev":
            mass_vector,

        "intended_vector_mass_squared_ev2":
            intended_mass_squared,

        "nda_delta_mass_squared_ev2":
            nda_delta_mass_squared,

        "nda_delta_mass_squared_over_target":
            ratio,

        "induced_mass_scale_ev":
            induced_mass_ev,

        "induced_range_m":
            induced_range_m,

        "technical_naturalness_pass":
            bool(
                ratio
                <=
                1.0
            ),

        "exact_beta_function":
            False,

        "exact_finite_matching":
            False,
    }


def naturalness_suppression_requirement() -> dict[str, Any]:
    """Return how small the unknown loop coefficient must be."""

    protection = (
        stueckelberg_protection_audit()
    )

    coupling = (
        microscopic_coupling_lower_bound()
    )

    mass_vector = float(
        protection[
            "one_metre_carrier_mass_ev"
        ]
    )

    g_lower = float(
        coupling[
            "constituent_coupling_lower_bound"
        ]
    )

    required_loop_coefficient = (
        16.0
        *
        math.pi**2
        *
        mass_vector**2
        /
        (
            g_lower**2
            *
            ELECTRON_MASS_EV**2
        )
    )

    rows = [
        fermion_threshold_mass_nda(
            loop_coefficient=
                value
        )
        for value
        in LOOP_COEFFICIENTS
    ]

    return {
        "rows":
            rows,

        "loop_coefficient_required_for_delta_m2_at_most_target":
            required_loop_coefficient,

        "required_suppression_below_1e_minus_20":
            bool(
                required_loop_coefficient
                <
                1.0e-20
            ),

        "all_tested_loop_coefficients_fail":
            bool(
                all(
                    not row[
                        "technical_naturalness_pass"
                    ]
                    for row
                    in rows
                )
            ),

        "smallest_tested_loop_coefficient":
            min(
                LOOP_COEFFICIENTS
            ),

        "smallest_tested_ratio":
            min(
                row[
                    "nda_delta_mass_squared_over_target"
                ]
                for row
                in rows
            ),
    }


@lru_cache(maxsize=1)
def hypothetical_weak_current_escape() -> dict[str, Any]:
    """Test energy/naturalness overlap for a hypothetical new epsilon coupling."""

    strict = (
        strict_payload_floor_rescale()
    )

    protection = (
        stueckelberg_protection_audit()
    )

    field_energy = float(
        strict[
            "strict_field_loading_energy_j"
        ]
    )

    electron_rest_at_epsilon_one = float(
        strict[
            "strict_electron_positron_rest_floor_j"
        ]
    )

    available_rest_budget = (
        STRICT_COMPLETE_OPERATING_TARGET_J
        -
        field_energy
    )

    if available_rest_budget <= 0.0:
        epsilon_energy_min = math.inf
    else:
        epsilon_energy_min = (
            electron_rest_at_epsilon_one
            /
            available_rest_budget
        )

    mass_vector = float(
        protection[
            "one_metre_carrier_mass_ev"
        ]
    )

    epsilon_naturalness_max_c1 = (
        4.0
        *
        math.pi
        *
        mass_vector
        /
        ELECTRON_MASS_EV
    )

    rows = []

    for coefficient in LOOP_COEFFICIENTS:
        epsilon_max = (
            epsilon_naturalness_max_c1
            /
            math.sqrt(
                coefficient
            )
        )

        source_rest_energy = (
            electron_rest_at_epsilon_one
            /
            epsilon_max
        )

        partial_total = (
            field_energy
            +
            source_rest_energy
        )

        rows.append(
            {
                "loop_coefficient":
                    coefficient,

                "epsilon_naturalness_max":
                    epsilon_max,

                "epsilon_energy_min":
                    epsilon_energy_min,

                "naturalness_energy_overlap":
                    bool(
                        epsilon_max
                        >=
                        epsilon_energy_min
                    ),

                "source_rest_energy_at_naturalness_epsilon_j":
                    source_rest_energy,

                "field_plus_source_rest_at_naturalness_epsilon_j":
                    partial_total,
            }
        )

    loop_coefficient_needed_for_overlap = (
        (
            epsilon_naturalness_max_c1
            /
            epsilon_energy_min
        ) ** 2
    )

    return {
        "hypothetical_epsilon_exists_in_current_action":
            False,

        "diagnostic_only":
            True,

        "field_energy_independent_of_epsilon_for_fixed_target_field":
            True,

        "source_number_scales_as_one_over_epsilon":
            True,

        "source_rest_energy_scales_as_one_over_epsilon":
            True,

        "epsilon_energy_min_for_electron_partial_below_10mj":
            epsilon_energy_min,

        "epsilon_naturalness_max_for_c_loop_1":
            epsilon_naturalness_max_c1,

        "rows":
            rows,

        "all_tested_coefficients_have_no_energy_naturalness_overlap":
            bool(
                all(
                    not row[
                        "naturalness_energy_overlap"
                    ]
                    for row
                    in rows
                )
            ),

        "loop_coefficient_needed_before_simple_epsilon_overlap":
            loop_coefficient_needed_for_overlap,

        "requires_loop_suppression_below_1e_minus_15":
            bool(
                loop_coefficient_needed_for_overlap
                <
                1.0e-15
            ),
    }


@lru_cache(maxsize=1)
def h17a10f2_summary() -> dict[str, Any]:
    """Return scoped A10F2 naturalness closeout."""

    strict = (
        strict_payload_floor_rescale()
    )

    coupling = (
        microscopic_coupling_lower_bound()
    )

    protection = (
        stueckelberg_protection_audit()
    )

    longitudinal = (
        longitudinal_stueckelberg_diagnostic()
    )

    naturalness = (
        naturalness_suppression_requirement()
    )

    epsilon = (
        hypothetical_weak_current_escape()
    )

    reduced_eft_performance_survives = bool(
        strict[
            "reduced_eft_1g_1m_strict_payload_performance_pass"
        ]
        and
        strict[
            "strict_field_loading_energy_j"
        ]
        <
        STRICT_COMPLETE_OPERATING_TARGET_J
    )

    technical_naturalness_block = bool(
        coupling[
            "at_least_one_constituent_order_unity"
        ]
        and
        not coupling[
            "current_action_has_free_small_source_coupling"
        ]
        and
        protection[
            "B_squared_mass_operator_stueckelberg_invariant"
        ]
        and
        not protection[
            "operator_level_exact_engineered_current_conservation_established"
        ]
        and
        not protection[
            "matter_loop_nonrenormalization_theorem_established"
        ]
        and
        naturalness[
            "all_tested_loop_coefficients_fail"
        ]
        and
        naturalness[
            "required_suppression_below_1e_minus_20"
        ]
        and
        longitudinal[
            "longitudinal_enhancement_gE_over_f_at_electron_threshold"
        ]
        >
        1.0e10
    )

    decision = (
        "RED_A10F2_CURRENT_WHEELER_MARZO_ORDINARY_DIRAC_"
        "REALIZATION_BLOCKED_ON_ULTRALIGHT_SOURCE_NATURALNESS__"
        "STRICT_REDUCED_EFT_1G_1M_PAYLOAD_SURVIVES"
        if (
            reduced_eft_performance_survives
            and
            technical_naturalness_block
        )
        else
        "YELLOW_A10F2_REQUIRES_REVIEW"
    )

    return {
        "branch":
            "032H17A10F2",

        "decision":
            decision,

        "current_full_regression_before_a10f2":
            983,

        "strict_payload_floor":
            strict,

        "microscopic_coupling":
            coupling,

        "stueckelberg_protection":
            protection,

        "longitudinal_diagnostic":
            longitudinal,

        "electron_threshold_naturalness":
            naturalness,

        "hypothetical_weak_current_escape":
            epsilon,

        "strict_reduced_eft_1g_1m_payload_performance_survives":
            reduced_eft_performance_survives,

        "current_ordinary_dirac_source_technical_naturalness_certified":
            False,

        "current_ordinary_dirac_wheeler_marzo_realization_blocked":
            technical_naturalness_block,

        "current_realization_full_certification_stops_here":
            technical_naturalness_block,

        "expensive_source_support_simulation_authorized":
            False,

        "expensive_full_nonlinear_bvp_authorized":
            False,

        "complete_energy_optimization_authorized":
            False,

        "a10a_source_state_escape_preserved":
            True,

        "a10c_source_noether_completion_preserved":
            True,

        "a10d_healthy_pole_overlap_preserved":
            True,

        "a10e_quadratic_metric_mechanism_preserved":
            True,

        "a10f1_finite_reduced_eft_payload_witness_preserved":
            True,

        "marzo_protected_1minus_family_globally_closed":
            False,

        "all_higgsed_noether_completions_closed":
            False,

        "all_exact_conserved_current_completions_closed":
            False,

        "hook17_closed":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "complete_energy_established":
            False,

        "project_true_standoff_certified":
            False,

        "strict_complete_operating_target_j":
            STRICT_COMPLETE_OPERATING_TARGET_J,

        "next":
            (
                "RETURN_TO_A9R3_WITH_GENUINELY_NEW_PROTECTED_SOURCE_FAMILY__"
                "PRIORITIZE_EXACT_CURRENT_CONSERVATION_OR_FULL_HIGGSED_"
                "NOETHER_COMPLETION_BEFORE_ANY_NEW_FINITE_PAYLOAD_RUN"
                if technical_naturalness_block
                else
                "032H17A10F3_FULL_MICROSCOPIC_SOURCE_AND_COMPLETE_LEDGER"
            ),

        "claim_scope":
            (
                "TECHNICAL_NATURALNESS_NDA_AND_LONGITUDINAL_"
                "POWER_COUNTING_CLOSEOUT_OF_CURRENT_ORDINARY_DIRAC_"
                "WHEELER_MARZO_REALIZATION;_NOT_AN_EXACT_LOOP_NO_GO_"
                "FOR_ALL_PROTECTED_MAG"
            ),
    }
