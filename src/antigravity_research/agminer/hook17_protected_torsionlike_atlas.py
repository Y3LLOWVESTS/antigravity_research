"""032H17A4 protected torsion-like/MAG symmetry atlas for HOOK17.

PURPOSE
-------
Follow 032H17A3 by replacing unprotected codimension-seven single-state
hook-MAG tunings with symmetry-first candidate families.

The central representation fact inherited from V24C is the exact algebraic map

    T_abc = H_abc - H_bac

from the V24 hook H_a(bc) to a pair-antisymmetric rank-three tensor T_[ab]c.
The map uses only index permutations, is parity-even, and is invertible on the
declared hook subspace.

A recent exhaustive symmetry-first classification of linear parity-conserving
pair-antisymmetric rank-three theories on Minkowski space starts from the
general twelve-parameter quadratic action, finds 206 gauge-symmetric
specializations, and identifies 22 ghost/tachyon-free cases. In the torsion
interpretation all unitary cases propagate one or more vector torsion modes,
not scalar or pseudoscalar torsion modes.

This is a scoped literature theorem. It does not classify parity violation,
nonlinear backgrounds, constrained hook-only theories, all metric-affine
actions, or all compensator/Higgs completions.

SCIENTIFIC QUESTION
-------------------
Can the H17A2 healthy source overlap and V26B1 active/off-state mechanism be
moved into a genuinely symmetry-protected carrier family without pretending
that a representation map is already a same-action theory?

This gate therefore:

1. reconstructs the actual V24 hook -> torsion-like map;
2. determines trace, axial, and cyclic properties of the clean source;
3. preserves the exact H17A2 2+ and 1+ source-overlap results;
4. applies the symmetry-first torsion-like catalogue only within its scope;
5. constructs a gauge-invariant Stückelberg-vector quadratic metric witness;
6. reranks protected vector families for the next exact action/projector gate;
7. keeps same-action, H17B, finite-payload, and energy promotion closed.

IMPORTANT SOURCE LESSON
-----------------------
The mapped clean source has zero simple Lorentz vector traces and zero axial
pseudotrace. This does NOT imply zero O(3) vector-mode overlap. H17A2 already
established a nonzero 1+ antisymmetric spatial source. Its three-dimensional
dual vector is explicitly nonzero in the carrier rest frame.

Therefore this run forbids the invalid shortcut

    TRACE_VECTOR_ZERO => ALL_VECTOR_MODES_ZERO.

STUECKELBERG METRIC WITNESS
---------------------------
For a protected vector realization with

    delta V_mu = partial_mu alpha
    delta pi   = m alpha

define

    W_mu = V_mu - partial_mu pi / m.

Then W_mu is gauge invariant. The quadratic physical-metric witness

    g_phys_mn = g_mn + lambda W_m W_n

is likewise gauge invariant, has exact off-state linear silence at W=0, and a
nonzero first variation on an active W background.

This is a kinematic metric witness only. It is not yet the V24 source matched
to a specific protected vector action and it does not establish that the
original 17-J capacity survives the change of carrier.

LITERATURE PROVENANCE
---------------------
Symmetry-first torsion-like catalogue:
    Barker, Marzo, Santoni
    arXiv:2507.05349
    Phys. Rev. D accepted 2026-08-21

Radiatively stable Abelian MAG / Stückelberg extension:
    Marzo
    arXiv:2110.14788
    Phys. Rev. D 106, 024045 (2022)

Extended-projective Dirac-motivated symmetry:
    Barker, Zell
    arXiv:2402.14917

Nonlinear vector-graviton Noether completion:
    Marzo
    arXiv:2603.24008

CLAIM LIMITS
------------
This module does NOT establish:

- a complete same-action HOOK17 theory;
- a protected exact V24-to-vector source projector;
- a completed Noether identity including Dirac matter;
- a unique universal metric derived from a UV-complete action;
- finite-payload outward acceleration or true stand-off;
- source/support/compensator/complete energy;
- quantum, RG, UV, empirical, or nonlinear closure;
- a practical device.

No AGMINER database mutation is performed.
No energy optimization is performed.

CLAIM_CLASSIFICATION=
SYMMETRY_FIRST_REPRESENTATION_ATLAS_AND_GAUGE_INVARIANT_METRIC_PREFLIGHT
"""

from __future__ import annotations

from typing import Any

import itertools
import numpy as np

from .dirac_hook_vector_bridge import (
    hook_to_torsionlike,
    marzo_2026_vector_graviton_bridge_template,
    torsionlike_to_hook,
)
from .hook17_healthy_mag_projector import (
    h17a2_summary,
    timelike_rest_pole_projector_gate,
)
from .nonlinear_hook_metric_bridge import rest_pair_hook


ETA = np.diag(
    [
        -1.0,
        1.0,
        1.0,
        1.0,
    ]
)

TOL = 1.0e-12

HOOK17_REFERENCE_CAPACITY_RP1E12_J = 17.0676442196
STRICT_COMPLETE_OPERATING_TARGET_J = 1.0e7


def _levi_civita_4() -> np.ndarray:
    """Return epsilon^{abcd} as a numerical alternating symbol."""
    eps = np.zeros(
        (
            4,
            4,
            4,
            4,
        ),
        dtype=float,
    )

    for permutation in itertools.permutations(
        range(
            4
        )
    ):
        inversions = sum(
            1
            for i in range(
                4
            )
            for j in range(
                i + 1,
                4,
            )
            if permutation[
                i
            ]
            >
            permutation[
                j
            ]
        )

        eps[
            permutation
        ] = (
            -1.0
            if inversions % 2
            else 1.0
        )

    return eps


def mapped_v24_torsionlike_source_gate() -> dict[
    str,
    Any,
]:
    """Return exact representation and irreducible-source diagnostics."""
    hook = np.asarray(
        rest_pair_hook(),
        dtype=float,
    )

    torsionlike = np.asarray(
        hook_to_torsionlike(
            hook
        ),
        dtype=float,
    )

    reconstructed = np.asarray(
        torsionlike_to_hook(
            torsionlike
        ),
        dtype=float,
    )

    antisymmetry_error = float(
        np.linalg.norm(
            torsionlike
            +
            np.swapaxes(
                torsionlike,
                0,
                1,
            )
        )
    )

    cyclic = (
        torsionlike
        +
        np.transpose(
            torsionlike,
            (
                1,
                2,
                0,
            ),
        )
        +
        np.transpose(
            torsionlike,
            (
                2,
                0,
                1,
            ),
        )
    )

    trace_a = np.einsum(
        "bc,abc->a",
        ETA,
        torsionlike,
    )

    trace_b = np.einsum(
        "ac,abc->b",
        ETA,
        torsionlike,
    )

    epsilon = (
        _levi_civita_4()
    )

    axial = np.einsum(
        "dabc,abc->d",
        epsilon,
        torsionlike,
    )

    hook_norm = float(
        np.linalg.norm(
            hook
        )
    )

    torsion_norm = float(
        np.linalg.norm(
            torsionlike
        )
    )

    roundtrip_error = float(
        np.linalg.norm(
            reconstructed
            -
            hook
        )
        /
        max(
            hook_norm,
            1.0,
        )
    )

    return {
        "hook_source_nonzero":
            bool(
                hook_norm
                >
                TOL
            ),

        "hook_norm":
            hook_norm,

        "torsionlike_source_nonzero":
            bool(
                torsion_norm
                >
                TOL
            ),

        "torsionlike_norm":
            torsion_norm,

        "first_pair_antisymmetric":
            bool(
                antisymmetry_error
                <=
                TOL
            ),

        "first_pair_antisymmetry_error":
            antisymmetry_error,

        "hook_roundtrip_relative_error":
            roundtrip_error,

        "map_invertible_on_declared_hook_source":
            bool(
                roundtrip_error
                <=
                TOL
            ),

        "map_uses_levi_civita":
            False,

        "map_parity_even":
            True,

        "cyclic_sum_norm":
            float(
                np.linalg.norm(
                    cyclic
                )
            ),

        "cyclic_identity_zero":
            bool(
                np.linalg.norm(
                    cyclic
                )
                <=
                TOL
            ),

        "lorentz_trace_a":
            trace_a.tolist(),

        "lorentz_trace_a_norm":
            float(
                np.linalg.norm(
                    trace_a
                )
            ),

        "lorentz_trace_a_zero":
            bool(
                np.linalg.norm(
                    trace_a
                )
                <=
                TOL
            ),

        "lorentz_trace_b":
            trace_b.tolist(),

        "lorentz_trace_b_norm":
            float(
                np.linalg.norm(
                    trace_b
                )
            ),

        "lorentz_trace_b_zero":
            bool(
                np.linalg.norm(
                    trace_b
                )
                <=
                TOL
            ),

        "axial_pseudotrace":
            axial.tolist(),

        "axial_pseudotrace_norm":
            float(
                np.linalg.norm(
                    axial
                )
            ),

        "axial_pseudotrace_zero":
            bool(
                np.linalg.norm(
                    axial
                )
                <=
                TOL
            ),

        "trace_zero_closes_all_vector_modes":
            False,
    }


def h17a2_oneplus_spatial_dual_vector_gate() -> dict[
    str,
    Any,
]:
    """Dualize the exact H17A2 1+ spatial antisymmetric source to a vector."""
    pole = (
        timelike_rest_pole_projector_gate()
    )

    matrix = np.asarray(
        pole[
            "hook_1plus_spatial_source_matrix"
        ],
        dtype=float,
    )

    dual = np.array(
        [
            matrix[
                1,
                2,
            ],
            matrix[
                2,
                0,
            ],
            matrix[
                0,
                1,
            ],
        ],
        dtype=float,
    )

    matrix_norm2 = float(
        np.sum(
            matrix
            *
            matrix
        )
    )

    dual_norm2 = float(
        np.sum(
            dual
            *
            dual
        )
    )

    return {
        "oneplus_antisymmetric_matrix":
            matrix.tolist(),

        "oneplus_matrix_norm2":
            matrix_norm2,

        "spatial_dual_vector":
            dual.tolist(),

        "spatial_dual_vector_norm2":
            dual_norm2,

        "spatial_dual_vector_nonzero":
            bool(
                dual_norm2
                >
                TOL
            ),

        "dual_norm_identity_pass":
            bool(
                np.isclose(
                    matrix_norm2,
                    2.0
                    *
                    dual_norm2,
                    rtol=0.0,
                    atol=TOL,
                )
            ),

        "lorentz_covariant_action_projector_established":
            False,

        "same_action_vector_source_identification_established":
            False,
    }


def torsionlike_catalogue_theorem_gate() -> dict[
    str,
    Any,
]:
    """Encode the scoped 2025/2026 symmetry-first torsion-like theorem."""
    mapped = (
        mapped_v24_torsionlike_source_gate()
    )

    h17a2 = (
        h17a2_summary()
    )

    return {
        "literature_family":
            "BARKER_MARZO_SANTONI_2507_05349",

        "background":
            "MINKOWSKI",

        "linear":
            True,

        "parity_conserving":
            True,

        "field_representation":
            "PAIR_ANTISYMMETRIC_RANK3",

        "general_quadratic_parameter_count":
            12,

        "gauge_symmetric_specializations":
            206,

        "ghost_tachyon_free_specializations":
            22,

        "unitary_torsion_modes_vector_only":
            True,

        "unitary_scalar_torsion_present":
            False,

        "unitary_pseudoscalar_torsion_present":
            False,

        "v24_hook_maps_into_pair_antisymmetric_representation":
            bool(
                mapped[
                    "first_pair_antisymmetric"
                ]
                and
                mapped[
                    "map_invertible_on_declared_hook_source"
                ]
            ),

        "h17a2_2plus_source_overlap_exists_in_unprotected_hook_action":
            bool(
                h17a2[
                    "hook_2plus_exact_pole_source_nonzero"
                ]
            ),

        "h17a2_1plus_source_overlap_exists_in_unprotected_hook_action":
            bool(
                h17a2[
                    "hook_1plus_exact_pole_source_nonzero"
                ]
            ),

        "catalogue_supplies_protected_spin2_carrier":
            False,

        "catalogue_supplies_protected_vector_carriers":
            True,

        "catalogue_rescues_h17_2plus_directly":
            False,

        "catalogue_keeps_h17_1plus_representation_target_open":
            True,

        "catalogue_closes_all_protected_hook_2plus_theories":
            False,

        "scope_exclusions":
            [
                "PARITY_VIOLATING",
                "NONLINEAR_BACKGROUND",
                "CURVED_BACKGROUND",
                "HOOK_ONLY_CONSTRAINED_ACTIONS_OUTSIDE_CATALOGUE",
                "OTHER_MAG_REPRESENTATIONS",
                "COMPENSATOR_OR_HIGGS_COMPLETIONS_OUTSIDE_CATALOGUE",
            ],
    }


def stueckelberg_vector_metric_gate() -> dict[
    str,
    Any,
]:
    """Verify a gauge-invariant quadratic vector physical-metric witness."""
    mass = 2.3

    vector = np.array(
        [
            0.4,
            -0.2,
            0.7,
            0.1,
        ],
        dtype=float,
    )

    grad_pi = np.array(
        [
            0.3,
            0.5,
            -0.4,
            0.2,
        ],
        dtype=float,
    )

    grad_alpha = np.array(
        [
            -0.6,
            0.9,
            0.25,
            -0.35,
        ],
        dtype=float,
    )

    invariant = (
        vector
        -
        grad_pi
        /
        mass
    )

    transformed_vector = (
        vector
        +
        grad_alpha
    )

    transformed_grad_pi = (
        grad_pi
        +
        mass
        *
        grad_alpha
    )

    transformed_invariant = (
        transformed_vector
        -
        transformed_grad_pi
        /
        mass
    )

    gauge_error = float(
        np.linalg.norm(
            transformed_invariant
            -
            invariant
        )
    )

    metric = np.outer(
        invariant,
        invariant,
    )

    transformed_metric = np.outer(
        transformed_invariant,
        transformed_invariant,
    )

    metric_gauge_error = float(
        np.linalg.norm(
            transformed_metric
            -
            metric
        )
    )

    perturbation = np.array(
        [
            0.11,
            -0.07,
            0.05,
            0.13,
        ],
        dtype=float,
    )

    active_first_variation = (
        np.outer(
            invariant,
            perturbation,
        )
        +
        np.outer(
            perturbation,
            invariant,
        )
    )

    zero = np.zeros(
        4,
        dtype=float,
    )

    offstate_first_variation = (
        np.outer(
            zero,
            perturbation,
        )
        +
        np.outer(
            perturbation,
            zero,
        )
    )

    return {
        "gauge_transformation":
            "delta_V=partial_alpha; delta_pi=m_alpha",

        "gauge_invariant_vector":
            "W=V-partial_pi/m",

        "gauge_invariant_vector_error":
            gauge_error,

        "gauge_invariant_vector_pass":
            bool(
                gauge_error
                <=
                TOL
            ),

        "physical_metric_witness":
            "g_phys=g+lambda W_mu W_nu",

        "metric_gauge_invariance_error":
            metric_gauge_error,

        "metric_gauge_invariance_pass":
            bool(
                metric_gauge_error
                <=
                TOL
            ),

        "offstate_first_variation_norm":
            float(
                np.linalg.norm(
                    offstate_first_variation
                )
            ),

        "offstate_linear_silence":
            bool(
                np.linalg.norm(
                    offstate_first_variation
                )
                <=
                TOL
            ),

        "active_first_variation_norm":
            float(
                np.linalg.norm(
                    active_first_variation
                )
            ),

        "active_linear_response_nonzero":
            bool(
                np.linalg.norm(
                    active_first_variation
                )
                >
                TOL
            ),

        "one_universal_symmetric_rank2_metric_witness":
            bool(
                np.allclose(
                    metric,
                    metric.T,
                    atol=TOL,
                    rtol=0.0,
                )
            ),

        "exact_v24_source_matched_to_W":
            False,

        "same_action_dirac_source_ward_complete":
            False,

        "hook17_17j_capacity_preserved_under_vector_completion":
            False,
    }


def protected_family_atlas() -> list[
    dict[
        str,
        Any,
    ]
]:
    """Return the symmetry-first H17A4 family ranking."""
    catalogue = (
        torsionlike_catalogue_theorem_gate()
    )

    marzo = (
        marzo_2026_vector_graviton_bridge_template()
    )

    return [
        {
            "priority":
                1,

            "family":
                "BMS2026_TORSIONLIKE_UNITARY_VECTOR_CATALOGUE",

            "protection":
                "EXPLICIT_GAUGE_SYMMETRY_CLASSIFICATION",

            "healthy_open_region_or_models":
                True,

            "v24_representation_match":
                catalogue[
                    "v24_hook_maps_into_pair_antisymmetric_representation"
                ],

            "v24_exact_action_projector":
                False,

            "gauge_invariant_metric_witness":
                True,

            "status":
                "OPEN_HIGHEST_PRIORITY_EXACT_1PLUS_PROJECTOR_REQUIRED",
        },
        {
            "priority":
                2,

            "family":
                "MARZO2022_ABELIAN_NONMETRICITY_VECTOR_STUECKELBERG",

            "protection":
                (
                    "ABELIAN_GAUGE_SYMMETRY_WITH_"
                    "STUECKELBERG_MASS_EXTENSION"
                ),

            "healthy_open_region_or_models":
                True,

            "v24_representation_match":
                False,

            "v24_exact_action_projector":
                False,

            "gauge_invariant_metric_witness":
                True,

            "status":
                "OPEN_SOURCE_MATCH_REQUIRED",
        },
        {
            "priority":
                3,

            "family":
                "BARKER_ZELL2024_EXTENDED_PROJECTIVE_ALT_DOUBLE_VECTOR",

            "protection":
                (
                    "EXTENDED_PROJECTIVE_OR_"
                    "ALTERNATIVE_DOUBLE_VECTOR_SYMMETRY"
                ),

            "healthy_open_region_or_models":
                True,

            "v24_representation_match":
                False,

            "v24_exact_action_projector":
                False,

            "gauge_invariant_metric_witness":
                False,

            "status":
                (
                    "OPEN_DIRAC_MOTIVATED_VECTOR_FAMILY_"
                    "SOURCE_MATCH_REQUIRED"
                ),
        },
        {
            "priority":
                4,

            "family":
                "MARZO2026_NONLINEAR_VECTOR_GRAVITON_NOETHER_COMPLETION",

            "protection":
                (
                    "GAUGE_INVARIANT_VECTOR_MASS_"
                    "AND_NOETHER_COMPLETION"
                ),

            "healthy_open_region_or_models":
                bool(
                    marzo[
                        "unitary_open_region_reported"
                    ]
                ),

            "v24_representation_match":
                False,

            "v24_exact_action_projector":
                False,

            "gauge_invariant_metric_witness":
                bool(
                    marzo[
                        "quadratic_vector_graviton_mixing"
                    ]
                ),

            "status":
                "OPEN_STRONGEST_BRIDGE_SIDE_NONLINEAR_TEMPLATE",
        },
        {
            "priority":
                5,

            "family":
                "MASSIVE_CURTRIGHT_STUECKELBERG_HOOK",

            "protection":
                "MIXED_SYMMETRY_STUECKELBERG_COMPLETION",

            "healthy_open_region_or_models":
                True,

            "v24_representation_match":
                True,

            "v24_exact_action_projector":
                False,

            "gauge_invariant_metric_witness":
                False,

            "status":
                (
                    "OPEN_LOWER_PRIORITY_"
                    "MASSIVE_SPIN2_DUALITY_AUDIT_REQUIRED"
                ),
        },
    ]


def h17a4_summary() -> dict[
    str,
    Any,
]:
    """Return conservative H17A4 promotion logic."""
    mapped = (
        mapped_v24_torsionlike_source_gate()
    )

    oneplus = (
        h17a2_oneplus_spatial_dual_vector_gate()
    )

    catalogue = (
        torsionlike_catalogue_theorem_gate()
    )

    metric = (
        stueckelberg_vector_metric_gate()
    )

    atlas = (
        protected_family_atlas()
    )

    representation_green = bool(
        mapped[
            "map_invertible_on_declared_hook_source"
        ]
        and
        mapped[
            "first_pair_antisymmetric"
        ]
        and
        catalogue[
            "catalogue_supplies_protected_vector_carriers"
        ]
        and
        oneplus[
            "spatial_dual_vector_nonzero"
        ]
    )

    metric_green = bool(
        metric[
            "gauge_invariant_vector_pass"
        ]
        and
        metric[
            "metric_gauge_invariance_pass"
        ]
        and
        metric[
            "offstate_linear_silence"
        ]
        and
        metric[
            "active_linear_response_nonzero"
        ]
    )

    exact_same_action_survivors = sum(
        1
        for row in atlas
        if row[
            "v24_exact_action_projector"
        ]
        and
        row[
            "gauge_invariant_metric_witness"
        ]
    )

    if (
        representation_green
        and
        metric_green
        and
        exact_same_action_survivors
        ==
        0
    ):
        decision = (
            "YELLOW_H17A4_"
            "SYMMETRY_FIRST_TORSIONLIKE_VECTOR_FAMILIES_SURVIVE_"
            "AND_GAUGE_INVARIANT_STUECKELBERG_METRIC_WITNESS_EXISTS__"
            "PROTECTED_EXACT_V24_1PLUS_ACTION_PROJECTOR_STILL_REQUIRED"
        )

        next_step = (
            "032H17A5_"
            "EXACT_PROTECTED_TORSIONLIKE_1PLUS_ACTION_PROJECTOR_"
            "DIRAC_SOURCE_WARD_AND_VECTOR_GRAVITON_IDENTIFICATION_GATE"
        )

    else:
        decision = (
            "RED_H17A4_"
            "NO_PROTECTED_VECTOR_RESCUE_FAMILY_SURVIVES_PREFLIGHT"
        )

        next_step = (
            "RERANK_H17_F3_F4_F5_AND_V26D_FALLBACK"
        )

    return {
        "decision":
            decision,

        "next":
            next_step,

        "v24_hook_to_torsionlike_map_green":
            representation_green,

        "mapped_source_simple_vector_trace_zero":
            bool(
                mapped[
                    "lorentz_trace_a_zero"
                ]
                and
                mapped[
                    "lorentz_trace_b_zero"
                ]
            ),

        "mapped_source_axial_pseudotrace_zero":
            mapped[
                "axial_pseudotrace_zero"
            ],

        "mapped_source_cyclic_identity_zero":
            mapped[
                "cyclic_identity_zero"
            ],

        "trace_zero_closes_all_vector_modes":
            False,

        "h17a2_1plus_spatial_dual_vector_nonzero":
            oneplus[
                "spatial_dual_vector_nonzero"
            ],

        "h17a2_1plus_spatial_dual_vector_norm2":
            oneplus[
                "spatial_dual_vector_norm2"
            ],

        "torsionlike_catalogue_gauge_symmetric_specializations":
            catalogue[
                "gauge_symmetric_specializations"
            ],

        "torsionlike_catalogue_unitary_specializations":
            catalogue[
                "ghost_tachyon_free_specializations"
            ],

        "torsionlike_catalogue_vector_only_unitary_modes":
            catalogue[
                "unitary_torsion_modes_vector_only"
            ],

        "catalogue_directly_rescues_2plus":
            catalogue[
                "catalogue_rescues_h17_2plus_directly"
            ],

        "catalogue_keeps_1plus_target_open":
            catalogue[
                "catalogue_keeps_h17_1plus_representation_target_open"
            ],

        "catalogue_closes_all_protected_2plus":
            catalogue[
                "catalogue_closes_all_protected_hook_2plus_theories"
            ],

        "stueckelberg_metric_gauge_invariant":
            metric[
                "metric_gauge_invariance_pass"
            ],

        "stueckelberg_metric_offstate_silent":
            metric[
                "offstate_linear_silence"
            ],

        "stueckelberg_metric_active_response_nonzero":
            metric[
                "active_linear_response_nonzero"
            ],

        "protected_exact_same_action_survivors":
            exact_same_action_survivors,

        "same_action_provenance_complete":
            False,

        "full_noether_completion":
            False,

        "h17b_authorized":
            False,

        "energy_optimization_authorized":
            False,

        "sub100j_efficiency_tuning_authorized":
            False,

        "agminer_database_mutation_authorized":
            False,

        "hook17_reference_capacity_rp1e12_j":
            HOOK17_REFERENCE_CAPACITY_RP1E12_J,

        "hook17_complete_energy_j":
            None,

        "strict_complete_operating_target_j":
            STRICT_COMPLETE_OPERATING_TARGET_J,

        "exactly_target_passes":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "practical_device_found":
            False,

        "v26d_fallback_status":
            "PRESERVED_PAUSED_V26E_NOT_ACTIVATED",
    }
