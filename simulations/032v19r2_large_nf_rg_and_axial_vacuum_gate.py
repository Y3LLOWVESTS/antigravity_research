"""032V19R2 — large-Nf axial determinant, RG, and bulk-vacuum gate.

PURPOSE
-------
Determine whether the R1 fixed-order wavefunction failure is evidence of
fatal strong coupling or instead an order-one many-flavor two-point
renormalization that admits a controlled large-Nf organization.

The run also evaluates the exact constant-spacelike-b fermion determinant in
a symmetry-restored cutoff scout and separates:

    wavefunction renormalization

from

    nonlinear b^4-and-higher vacuum structure.

This run deliberately does not optimize source energy.

PRIMARY QUESTIONS
-----------------
1. Is each individual hidden-fermion loop weak?
2. Is the collective O(1) correction compatible with large-Nf counting?
3. Does the exact determinant reproduce the expected logarithmic Z term?
4. Is there an unavoidable multi-MJ nonlinear bulk Dirac-sea contribution?
5. Does canonical field rescaling preserve C1 f^2?
6. Can the published Jiang positive-C1 spin-2 matching be adopted directly?
7. What remains before actual UV certification?

IMPORTANT
---------
A positive R2 result does not constitute a UV completion.

The exact source wall is inhomogeneous, so boundary/Casimir vacuum corrections
remain open.

Full beta functions and UV matching for C1, f_psi, m_psi and companion
operators also remain open.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

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
    symmetry_restored_axial_vacuum_density_ev4,
    quadratic_wavefunction_density_ev4,
)
from antigravity_research.agminer.c1_payload_matching import (
    c1_from_metric_scale_ev,
)
from antigravity_research.agminer.policy import (
    current_energy_policy,
)


ROOT = Path(
    __file__
).resolve().parents[1]

R1_PATH = (
    ROOT
    / "results"
    / "data"
    / "032v19r1_local_traction_shape_payload_rg_summary.json"
)

V18_PATH = (
    ROOT
    / "results"
    / "data"
    / "032v18_universal_metric_rg_support_ready_summary.json"
)

OUT = (
    ROOT
    / "results"
    / "data"
    / "032v19r2_large_nf_rg_axial_vacuum_summary.json"
)

VACUUM_SCAN_OUT = (
    ROOT
    / "results"
    / "data"
    / "032v19r2_axial_vacuum_cutoff_scan.csv"
)

RUNNING_OUT = (
    ROOT
    / "results"
    / "data"
    / "032v19r2_large_nf_rescaling_scan.csv"
)


TARGET_J = 1.0e7


policy = current_energy_policy()

assert math.isclose(
    float(
        policy[
            "limit_j"
        ]
    ),
    TARGET_J,
    rel_tol=0.0,
    abs_tol=0.0,
)

assert (
    str(
        policy[
            "comparison"
        ]
    )
    ==
    "LT"
)


r1 = json.loads(
    R1_PATH.read_text(
        encoding="utf-8"
    )
)

v18 = json.loads(
    V18_PATH.read_text(
        encoding="utf-8"
    )
)


assert (
    r1[
        "decision"
    ]
    ==
    "GREEN_LOCAL_TRACTION_AND_NEARBY_SUPPORTED_1G_RETUNE_LT4MJ_RED_STRUCTURAL_FIXED_ORDER_RG_UV_MATCHING_MANDATORY"
)


selected = r1[
    "selected_retuned_reference"
]

rg = r1[
    "rg_retuned_reference"
]

sphere = v18[
    "sphere_exact_payload_optimum"
]

physical = v18[
    "sphere_physical_source"
]

meanfield = v18[
    "sphere_meanfield"
]


nf = int(
    selected[
        "flavors"
    ]
)

f_psi_ev = float(
    selected[
        "f_psi_ev"
    ]
)

b_ev = float(
    selected[
        "axial_b_ev"
    ]
)

mu_ev = float(
    selected[
        "chemical_potential_ev"
    ]
)

mass_ev = float(
    physical[
        "m_psi_ev"
    ]
)

metric_scale_ev = float(
    sphere[
        "metric_scale_ev"
    ]
)

source_radius_m = float(
    meanfield[
        "source_radius_m"
    ]
)

source_volume_m3 = (
    4.0
    * math.pi
    * source_radius_m**3
    / 3.0
)

declared_cutoff_ev = (
    4.0
    * math.pi
    * f_psi_ev
)

hard_scale_ev = max(
    mass_ev,
    b_ev,
    mu_ev,
)

static_preflight_j = float(
    selected[
        "static_preflight_j"
    ]
)

delta_z_hard = float(
    rg[
        "minimum_delta_z_with_cutoff_at_hard_scale"
    ]
)

delta_z_declared = float(
    rg[
        "delta_z_at_declared_cutoff"
    ]
)


# ============================================================
# 1. LARGE-NF POWER COUNTING
# ============================================================

large_nf = (
    large_nf_power_counting(
        flavors=
            nf,

        mass_ev=
            mass_ev,

        f_psi_ev=
            f_psi_ev,
    )
)


assert math.isclose(
    large_nf[
        "collective_loop"
    ],
    float(
        selected[
            "loop_proxy"
        ]
    ),
    rel_tol=2.0e-12,
)


# ============================================================
# 2. CANONICAL FIELD-RESCALING SCOUT
# ============================================================

c1 = (
    c1_from_metric_scale_ev(
        metric_scale_ev
    )
)

rescaled_hard = (
    field_rescaling_scout(
        f_psi_ev=
            f_psi_ev,

        c1_ev_m4=
            c1,

        collective_loop=
            large_nf[
                "collective_loop"
            ],

        delta_z=
            delta_z_hard,
    )
)

rescaled_declared = (
    field_rescaling_scout(
        f_psi_ev=
            f_psi_ev,

        c1_ev_m4=
            c1,

        collective_loop=
            large_nf[
                "collective_loop"
            ],

        delta_z=
            delta_z_declared,
    )
)


assert (
    rescaled_hard[
        "positive_kinetic_factor"
    ]
)

assert (
    rescaled_declared[
        "positive_kinetic_factor"
    ]
)

assert (
    rescaled_hard[
        "invariant_relative_error"
    ]
    <
    1.0e-13
)

assert (
    rescaled_declared[
        "invariant_relative_error"
    ]
    <
    1.0e-13
)


# ============================================================
# 3. EXACT CONSTANT-b VACUUM SCOUT
# ============================================================

cutoff_ratios = (
    1.0,
    1.5,
    2.0,
    3.0,
    5.0,
    8.0,
)

vacuum_rows = []

for ratio in cutoff_ratios:
    cutoff = (
        ratio
        * hard_scale_ev
    )

    full_density = (
        symmetry_restored_axial_vacuum_density_ev4(
            mass_ev=
                mass_ev,

            axial_b_ev=
                b_ev,

            flavors=
                nf,

            cutoff_ev=
                cutoff,

            p_order=
                160,

            u_order=
                120,
        )
    )

    quadratic_density = (
        quadratic_wavefunction_density_ev4(
            mass_ev=
                mass_ev,

            axial_b_ev=
                b_ev,

            flavors=
                nf,

            cutoff_ev=
                cutoff,

            order=
                256,
        )
    )

    nonlinear_density = (
        full_density
        - quadratic_density
    )

    nonlinear_energy_j = (
        nonlinear_density
        * ev4_energy_density_j_m3(
            1.0
        )
        * source_volume_m3
    )

    vacuum_rows.append(
        {
            "cutoff_over_hard":
                ratio,

            "cutoff_ev":
                cutoff,

            "full_symmetry_restored_density_ev4":
                full_density,

            "quadratic_wavefunction_density_ev4":
                quadratic_density,

            "nonlinear_remainder_ev4":
                nonlinear_density,

            "nonlinear_remainder_j":
                nonlinear_energy_j,

            "physical_vacuum_energy_claim":
                False,
        }
    )


declared_full_density = (
    symmetry_restored_axial_vacuum_density_ev4(
        mass_ev=
            mass_ev,

        axial_b_ev=
            b_ev,

        flavors=
            nf,

        cutoff_ev=
            declared_cutoff_ev,

        p_order=
            180,

        u_order=
            140,
    )
)

declared_quadratic_density = (
    quadratic_wavefunction_density_ev4(
        mass_ev=
            mass_ev,

        axial_b_ev=
            b_ev,

        flavors=
            nf,

        cutoff_ev=
            declared_cutoff_ev,

        order=
            320,
    )
)

declared_nonlinear_density = (
    declared_full_density
    - declared_quadratic_density
)

declared_nonlinear_energy_j = (
    declared_nonlinear_density
    * ev4_energy_density_j_m3(
        1.0
    )
    * source_volume_m3
)


remainder_8hard = (
    nonlinear_vacuum_remainder_ev4(
        mass_ev=
            mass_ev,

        axial_b_ev=
            b_ev,

        flavors=
            nf,

        cutoff_ev=
            8.0
            * hard_scale_ev,

        p_order=
            180,

        u_order=
            140,
    )
)

nonlinear_convergence_fraction = (
    abs(
        remainder_8hard
        - declared_nonlinear_density
    )
    /
    abs(
        remainder_8hard
    )
)


# ============================================================
# 4. UNIVERSAL LOG COEFFICIENT
# ============================================================

asymptotic_slope = (
    asymptotic_quadratic_log_slope_ev4(
        mass_ev=
            mass_ev,

        axial_b_ev=
            b_ev,

        flavors=
            nf,
    )
)

finite_slope = (
    finite_cutoff_quadratic_log_slope_ev4(
        mass_ev=
            mass_ev,

        axial_b_ev=
            b_ev,

        flavors=
            nf,

        cutoff_ev=
            declared_cutoff_ev,
    )
)

slope_ratio = (
    finite_slope
    / asymptotic_slope
)


assert (
    slope_ratio
    >
    0.999
)

assert (
    nonlinear_convergence_fraction
    <
    2.0e-3
)


# ============================================================
# 5. NATURAL NONLINEAR LOOP SCALE
# ============================================================

natural_b4_density = (
    natural_b4_loop_scale_ev4(
        axial_b_ev=
            b_ev,

        flavors=
            nf,
    )
)

natural_b4_energy_j = (
    natural_b4_density
    * ev4_energy_density_j_m3(
        1.0
    )
    * source_volume_m3
)


assert (
    abs(
        declared_nonlinear_energy_j
    )
    <
    1.0e3
)

assert (
    natural_b4_energy_j
    <
    1.0e3
)


# ============================================================
# 6. BULK DERIVATIVE-EXPANSION SCALE
# ============================================================

bulk_scale = (
    bulk_derivative_expansion_scout(
        mass_ev=
            mass_ev,

        source_radius_m=
            source_radius_m,
    )
)


# ============================================================
# 7. UV TEMPLATE AUDIT
# ============================================================

jiang_template = (
    jiang_positive_c1_spin2_template()
)

assert (
    jiang_template[
        "pure_j0_completion"
    ]
    is False
)


# ============================================================
# 8. RUNNING / RESCALING TABLE
# ============================================================

running_rows = [
    {
        "location":
            "LOW_ENERGY_REFERENCE",

        "delta_z":
            0.0,

        "z_factor":
            1.0,

        "f_rescaled_ev":
            f_psi_ev,

        "c1_rescaled_ev_m4":
            c1,

        "collective_loop_rescaled":
            large_nf[
                "collective_loop"
            ],

        "full_rge_completed":
            False,
    },
    {
        "location":
            "OCCUPIED_HARD_SCALE_SCOUT",

        "delta_z":
            delta_z_hard,

        **rescaled_hard,
    },
    {
        "location":
            "DECLARED_NDA_CUTOFF_SCOUT",

        "delta_z":
            delta_z_declared,

        **rescaled_declared,
    },
]


# ============================================================
# 9. SCIENTIFIC CLASSIFICATION
# ============================================================

large_nf_reorganization_available = bool(
    large_nf[
        "large_nf_power_counting_scout"
    ]
    and
    rescaled_hard[
        "positive_kinetic_factor"
    ]
    and
    rescaled_declared[
        "positive_kinetic_factor"
    ]
)

bulk_nonlinear_not_catastrophic_scout = bool(
    abs(
        declared_nonlinear_energy_j
    )
    <
    1.0e4
    and
    nonlinear_convergence_fraction
    <
    2.0e-3
)


decision = (
    "GREEN_LARGE_NF_AXIAL_REORGANIZATION_AVAILABLE_"
    "GREEN_NONCATASTROPHIC_BULK_VACUUM_SCOUT_"
    "RED_DIRECT_JIANG_SPIN2_TEMPLATE_FOR_PURE_J0_"
    "OUTWARD_SIGN_UV_COMPLETION_BOUNDARY_VACUUM_AND_FULL_RGE_OPEN"
)

next_step = (
    "032V19R3_OUTWARD_SIGN_UV_COMPLETION_"
    "AND_COMPANION_OPERATOR_FALSIFICATION_GATE"
)


summary = {
    "branch":
        "032V19R2_LARGE_NF_AXIAL_DETERMINANT_RG_AND_VACUUM_GATE",

    "claim_class":
        "LARGE_NF_AND_CONSTANT_BACKGROUND_QUANTUM_PREFLIGHT",

    "energy_policy_id":
        str(
            policy[
                "policy_id"
            ]
        ),

    "r1_input_decision":
        r1[
            "decision"
        ],

    "source": {
        "flavors":
            nf,

        "f_psi_ev":
            f_psi_ev,

        "m_psi_ev":
            mass_ev,

        "axial_b_ev":
            b_ev,

        "chemical_potential_ev":
            mu_ev,

        "hard_scale_ev":
            hard_scale_ev,

        "declared_cutoff_ev":
            declared_cutoff_ev,

        "metric_scale_ev":
            metric_scale_ev,

        "static_preflight_j":
            static_preflight_j,
    },

    "large_nf": {
        **large_nf,

        "exact_fermion_determinant_is_leading_nf_object":
            True,

        "higher_scalar_loop_suppression_fully_proved":
            False,
    },

    "field_rescaling": {
        "hard_scale":
            rescaled_hard,

        "declared_cutoff":
            rescaled_declared,

        "c1_f2_invariant_preserved":
            True,

        "this_is_full_rge":
            False,
    },

    "vacuum": {
        "regulator":
            "ROTATIONAL_3MOMENTUM_CUTOFF_WITH_MASSLESS_SUBTRACTION",

        "massless_decoupling_condition":
            "GAUGE_SINGLET_HIDDEN_FERMION_REQUIRED",

        "gauge_quantum_numbers_fully_uv_specified":
            False,

        "declared_full_symmetry_restored_density_ev4":
            declared_full_density,

        "declared_quadratic_wavefunction_density_ev4":
            declared_quadratic_density,

        "declared_nonlinear_remainder_ev4":
            declared_nonlinear_density,

        "declared_nonlinear_remainder_j":
            declared_nonlinear_energy_j,

        "remainder_8hard_ev4":
            remainder_8hard,

        "nonlinear_convergence_fraction":
            nonlinear_convergence_fraction,

        "natural_b4_loop_density_ev4":
            natural_b4_density,

        "natural_b4_loop_energy_j":
            natural_b4_energy_j,

        "quadratic_log_slope_ratio_to_asymptotic":
            slope_ratio,

        "bulk_nonlinear_not_catastrophic_scout":
            bulk_nonlinear_not_catastrophic_scout,

        "nonlinear_remainder_is_unique_physical_energy":
            False,

        "quadratic_term_is_additive_device_energy":
            False,

        "boundary_casimir_included":
            False,

        "complete_renormalized_vacuum":
            False,
    },

    "bulk_derivative_expansion":
        bulk_scale,

    "uv_template_audit": {
        "jiang_positive_c1_spin2":
            jiang_template,

        "jiang_template_directly_usable":
            False,

        "outward_sign_pure_j0_uv_completion_proved":
            False,

        "companion_operator_matching_complete":
            False,
    },

    "gate_status": {
        "r1_supported_1g_state":
            "PRESERVED",

        "fixed_order_rg":
            "RED_STRUCTURAL_PRESERVED",

        "fixed_order_cutoff_tuning_escape":
            "CLOSED_PRESERVED",

        "large_nf_power_counting":
            (
                "GREEN_SCOUT"
                if large_nf_reorganization_available
                else "RED"
            ),

        "exact_constant_b_fermion_determinant":
            "GREEN_NUMERICAL_SCOUT",

        "universal_log_coefficient":
            "GREEN_RECONSTRUCTED",

        "bulk_nonlinear_axial_vacuum":
            (
                "GREEN_NONCATASTROPHIC_SCOUT"
                if bulk_nonlinear_not_catastrophic_scout
                else "RED"
            ),

        "complete_renormalized_axial_vacuum":
            "YELLOW_OPEN",

        "boundary_axial_vacuum":
            "OPEN",

        "full_c1_f_mass_rge":
            "OPEN",

        "jiang_spin2_direct_adoption":
            "RED",

        "outward_sign_universal_uv_completion":
            "OPEN_RED_BLOCKER",

        "companion_wilson_coefficients":
            "OPEN",

        "empirical_closure":
            "OPEN",

        "full_coupled_chi_psi_phi_modes":
            "OPEN",

        "complete_operating_energy":
            "NOT_ESTABLISHED",
    },

    "physical_antigravity_model_found":
        False,

    "certified_sub10mj_model_found":
        False,

    "decision":
        decision,

    "next":
        next_step,
}


OUT.write_text(
    json.dumps(
        summary,
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
)


with VACUUM_SCAN_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=
            list(
                vacuum_rows[
                    0
                ].keys()
            ),
    )

    writer.writeheader()

    writer.writerows(
        vacuum_rows
    )


with RUNNING_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    fieldnames = [
        "location",
        "delta_z",
        "z_factor",
        "f_rescaled_ev",
        "c1_rescaled_ev_m4",
        "collective_loop_rescaled",
        "full_rge_completed",
    ]

    writer = csv.DictWriter(
        handle,
        fieldnames=
            fieldnames,
        extrasaction=
            "ignore",
    )

    writer.writeheader()

    writer.writerows(
        running_rows
    )


print(
    "BRANCH="
    + summary[
        "branch"
    ]
)

print(
    "G_P_EQUIVALENT="
    f"{large_nf['g_p_equivalent']:.12e}"
)

print(
    "SINGLE_FLAVOR_LOOP="
    f"{large_nf['single_flavor_loop']:.12e}"
)

print(
    "COLLECTIVE_LOOP="
    f"{large_nf['collective_loop']:.12e}"
)

print(
    "ONE_OVER_NF="
    f"{large_nf['one_over_nf']:.12e}"
)

print(
    "INDUCED_FOUR_POINT_SCALING="
    f"{large_nf['induced_four_point_scaling']:.12e}"
)

print(
    "Z_HARD_SCOUT="
    f"{rescaled_hard['z_factor']:.12e}"
)

print(
    "Z_DECLARED_CUTOFF_SCOUT="
    f"{rescaled_declared['z_factor']:.12e}"
)

print(
    "RESCALED_LOOP_AT_HARD="
    f"{rescaled_hard['collective_loop_rescaled']:.12e}"
)

print(
    "RESCALED_LOOP_AT_DECLARED_CUTOFF="
    f"{rescaled_declared['collective_loop_rescaled']:.12e}"
)

print(
    "C1_F2_INVARIANT_RELERR="
    f"{rescaled_declared['invariant_relative_error']:.12e}"
)

print(
    "VACUUM_LOG_SLOPE_RATIO="
    f"{slope_ratio:.12e}"
)

print(
    "VACUUM_NONLINEAR_REMAINDER_EV4="
    f"{declared_nonlinear_density:.12e}"
)

print(
    "VACUUM_NONLINEAR_REMAINDER_J="
    f"{declared_nonlinear_energy_j:.12e}"
)

print(
    "VACUUM_REMAINDER_CONVERGENCE="
    f"{nonlinear_convergence_fraction:.12e}"
)

print(
    "NATURAL_B4_LOOP_ENERGY_J="
    f"{natural_b4_energy_j:.12e}"
)

print(
    "SOURCE_RADIUS_OVER_FERMION_COMPTON="
    f"{bulk_scale['source_radius_over_compton']:.12e}"
)

print(
    "JIANG_SPIN2_TEMPLATE_PURE_J0="
    + str(
        jiang_template[
            "pure_j0_completion"
        ]
    )
)

print(
    "FIXED_ORDER_RG_RED_PRESERVED=True"
)

print(
    "LARGE_NF_REORGANIZATION_AVAILABLE="
    + str(
        large_nf_reorganization_available
    )
)

print(
    "BULK_NONLINEAR_VACUUM_CATASTROPHIC="
    + str(
        not bulk_nonlinear_not_catastrophic_scout
    )
)

print(
    "COMPLETE_RENORMALIZED_VACUUM=False"
)

print(
    "OUTWARD_SIGN_UV_COMPLETION_PROVED=False"
)

print(
    "PHYSICAL_ANTIGRAVITY_MODEL_FOUND=False"
)

print(
    "CERTIFIED_SUB10MJ_MODEL_FOUND=False"
)

print(
    "DECISION="
    + decision
)

print(
    "NEXT="
    + next_step
)
