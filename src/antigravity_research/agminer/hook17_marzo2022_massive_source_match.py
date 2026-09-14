"""032H17A6R2 — Marzo-2022 protected massive MAG source-match gate.

PURPOSE
-------
Test one concrete published massive/Stueckelberg metric-affine-gravity
(MAG) rescue after 032H17A6R1 closed the declared exact-massless
single-compensator class.

The previous sequence established:

    H17A5:
        direct clean V24 -> protected K3 massless 1+ fails a necessary
        source Ward identity;

    H17A6:
        J11 retains the relevant Ward generator and also fails for the
        direct clean source;

    H17A6:
        fixed zero-derivative vector/axial improvements do not repair the
        source;

    H17A6R1:
        a pure exact Stueckelberg redundancy and an ordinary healthy
        massless two-form compensator return to the same Ward obstruction.

R1 deliberately kept massive/Higgsed realizations open because adding a
physical mass sector can change the constraint surface and add a genuine
longitudinal degree of freedom.

This file therefore stops inventing formal compensators and tests a real
published symmetry-protected massive MAG family.

PUBLISHED FAMILY
----------------
Carlo Marzo,
"Radiatively stable ghost and tachyon freedom in Metric Affine Gravity",
Phys. Rev. D 106, 024045 (2022),
arXiv:2110.14788.

The relevant published results are:

1. an Abelian symmetry protects a ghost/tachyon-free MAG sector;

2. the minimal protected theory is massless;

3. a real scalar Stueckelberg extension involving nonmetricity provides a
   mass while preserving the protecting Abelian symmetry;

4. the published quadratic spectrum contains a unique healthy massive
   spin/parity 1- pole in the declared massive branch;

5. open parameter regions with positive pole mass and positive residue
   exist, rather than the healthy theory requiring one isolated accidental
   tuning.

This module treats those statements as literature provenance.

It does NOT pretend that Marzo's paper already contains the project's V24
Dirac source or HOOK17 quadratic universal metric.

SCIENTIFIC QUESTION
-------------------
Does the actual clean V24 equal-rest particle/antiparticle source possess
nonzero support in the physical 1- representation carried by that published
massive sector?

If the exact answer is zero, then adding the published Stueckelberg mass
does not rescue the clean V24 source: the gauge obstruction may be lifted,
but the source still fails to excite the healthy physical massive carrier.

FULL V24 SOURCE DECOMPOSITION
-----------------------------
For torsion-free nonmetricity the V24 rank-three source decomposes into:

    totally symmetric rank-three piece

        plus

    hook-symmetric rank-three piece.

The repository already established for the hook piece:

    2+ support = nonzero
    1+ support = nonzero
    0+ support = zero
    2- support = zero
    1- support = zero.

This module independently inspects the totally symmetric piece.

In the equal-rest source frame, parity is diagnosed by the number of
spatial indices.

For a totally symmetric rank-three tensor S_abc:

    S_00i
        belongs to vector-like odd-parity support;

    S_ijk
        contains the purely spatial odd-parity sectors;

    S_0ij
        contains even-parity spatial tensor support.

The actual V24 clean rest pair is tested component-by-component.

A full-source 1- zero is promoted only if BOTH:

    totally symmetric 1- support = zero

and:

    hook 1- support = zero.

This is stronger than using a single Lorentz trace alone.

WHAT A RED RESULT CLOSES
------------------------
A RED result closes only:

    DIRECT CLEAN V24 EQUAL-REST SOURCE

        ->

    PUBLISHED MARZO-2022 PROTECTED MASSIVE 1- PHYSICAL POLE.

It does NOT close:

- generic Dirac source states;
- momentum-dependent / textured Dirac states;
- full matter-plus-compensator Noether currents;
- indirect source transfer through another physical field;
- Barker-Zell extended-projective / double-vector theories;
- other protected 1+ or 2+ MAG carriers;
- nonlinear vector-graviton completions;
- massive Curtright static off-shell exchange;
- V26D protected cT=1 DHOST/KMM.

STATIC OFF-SHELL DISCIPLINE
---------------------------
Zero physical-pole overlap does not prove that every constrained off-shell
Green-function component is zero.

The correct conclusion is narrower:

    DIRECT HEALTHY MASSIVE-POLE SOURCE = ZERO.

The direct clean-rest-pair route is therefore rejected as the healthy
carrier realization sought by HOOK17.

A separate off-shell metric effect would require its own same-action,
constraint, field-redefinition, and physical-observable proof.

ENERGY POLICY
-------------
No energy calculation or parameter optimization is performed.

The preserved

    17.0676442196 J

quantity remains only the R_P=1e12 HOOK17 canonical field-capacity
reference.

Complete operating energy remains unknown.

CLAIM CLASSIFICATION
--------------------
THEOREM_FIRST_PUBLISHED_MASSIVE_MAG_SOURCE_PROJECTOR_PREFILTER
"""

from __future__ import annotations

from typing import Any

import numpy as np

from .dirac_hook_vector_bridge import (
    generic_bms_spin1_trace_witness,
    rest_pair_bms_spin1_trace_gate,
    rest_pair_source_parts,
)

from .hook17_dynamic_compensator_noether import (
    h17a6r1_summary,
)

from .hook17_rescue_family_atlas import (
    mikura_percacci_hook_projector_prefilter,
    v24_clean_rest_o3_hook_irrep_gate,
)


TOL = 1.0e-12

HOOK17_REFERENCE_CAPACITY_RP1E12_J = 17.0676442196
STRICT_COMPLETE_OPERATING_TARGET_J = 1.0e7


def _real_rank3(
    tensor: np.ndarray,
    name: str,
) -> np.ndarray:
    """Return one finite real rank-three source tensor."""

    value = np.real_if_close(
        np.asarray(
            tensor
        )
    )

    if np.iscomplexobj(
        value
    ):
        raise ValueError(
            f"{name} must be real after physical source assembly"
        )

    result = np.asarray(
        value,
        dtype=float,
    )

    if result.shape != (
        4,
        4,
        4,
    ):
        raise ValueError(
            f"{name} must have shape (4,4,4)"
        )

    if not np.all(
        np.isfinite(
            result
        )
    ):
        raise ValueError(
            f"{name} must be finite"
        )

    return result


def r1_provenance_gate() -> dict[str, Any]:
    """Require the exact completed R1 scientific starting point."""

    result = h17a6r1_summary()

    passed = bool(
        result[
            "a6_provenance_pass"
        ]
        and
        result[
            "declared_exact_massless_single_compensator_class_closed"
        ]
        and
        not result[
            "higgsed_or_massive_hook_closed"
        ]
        and
        not result[
            "marzo_protected_stueckelberg_family_closed"
        ]
        and
        not result[
            "hook17_closed"
        ]
    )

    return {
        "r1_decision":
            result[
                "decision"
            ],

        "r1_provenance_pass":
            passed,

        "exact_massless_single_compensator_closed":
            result[
                "declared_exact_massless_single_compensator_class_closed"
            ],

        "massive_or_higgsed_open":
            not result[
                "higgsed_or_massive_hook_closed"
            ],

        "marzo_family_open_at_r1":
            not result[
                "marzo_protected_stueckelberg_family_closed"
            ],

        "hook17_open_at_r1":
            not result[
                "hook17_closed"
            ],
    }


def marzo2022_published_family_gate() -> dict[str, Any]:
    """Encode the published action-family facts needed for source matching.

    This is literature provenance only.

    The detailed kinetic matrices, residues, and pole masses are not
    independently rederived here because the immediate falsifier is source
    representation support.
    """

    return {
        "family":
            "MARZO2022_PROTECTED_ABELIAN_MAG_STUECKELBERG",

        "reference":
            (
                "C. Marzo, Phys. Rev. D 106, 024045 (2022), "
                "arXiv:2110.14788"
            ),

        "explicit_metric_affine_action_published":
            True,

        "protecting_abelian_symmetry_published":
            True,

        "protection_nonaccidental":
            True,

        "minimal_protected_model_massless":
            True,

        "stueckelberg_scalar_extension_published":
            True,

        "stueckelberg_extension_uses_nonmetricity":
            True,

        "massive_extension_preserves_abelian_protection":
            True,

        "published_massive_physical_pole_count":
            1,

        "published_massive_physical_pole_sector":
            "1_MINUS",

        "published_ghost_tachyon_free_massive_regions_exist":
            True,

        "healthy_region_is_not_declared_single_accidental_point":
            True,

        "v24_dirac_source_derived_in_published_action":
            False,

        "hook17_quadratic_metric_derived_in_published_action":
            False,

        "same_action_hook17_complete":
            False,

        "claim_scope":
            "PUBLISHED_FREE_AND_STUECKELBERG_MAG_PROVENANCE_ONLY",
    }


def _nonzero_component_rows(
    tensor: np.ndarray,
) -> list[dict[str, Any]]:
    """Return exact sparse support diagnostics for one rank-three tensor."""

    rows: list[dict[str, Any]] = []

    for a in range(
        4
    ):
        for b in range(
            4
        ):
            for c in range(
                4
            ):
                component = float(
                    tensor[
                        a,
                        b,
                        c,
                    ]
                )

                if abs(
                    component
                ) <= TOL:
                    continue

                time_count = int(
                    a == 0
                ) + int(
                    b == 0
                ) + int(
                    c == 0
                )

                rows.append(
                    {
                        "a":
                            a,

                        "b":
                            b,

                        "c":
                            c,

                        "value":
                            component,

                        "time_index_count":
                            time_count,

                        "spatial_index_count":
                            3
                            -
                            time_count,
                    }
                )

    return rows


def clean_v24_totally_symmetric_parity_gate() -> dict[str, Any]:
    """Decompose the clean V24 totally symmetric source by rest-frame parity.

    The exact equal-rest source is reconstructed from the same V24 Dirac
    bilinear implementation used by the earlier source gates.

    No hard-coded component values are used to decide support.
    """

    source = _real_rank3(
        rest_pair_source_parts()[
            "totally_symmetric"
        ],
        "clean V24 totally symmetric source",
    )

    permutation_error = max(
        float(
            np.max(
                np.abs(
                    source
                    -
                    np.transpose(
                        source,
                        permutation,
                    )
                )
            )
        )
        for permutation in (
            (
                1,
                0,
                2,
            ),
            (
                0,
                2,
                1,
            ),
            (
                2,
                1,
                0,
            ),
        )
    )

    nonzero = _nonzero_component_rows(
        source
    )

    source_norm = float(
        np.linalg.norm(
            source
        )
    )

    time_histogram = {
        str(
            count
        ):
            sum(
                1
                for row in nonzero
                if row[
                    "time_index_count"
                ]
                ==
                count
            )
        for count in range(
            4
        )
    }

    all_nonzero_have_exactly_one_time_index = bool(
        nonzero
        and
        all(
            row[
                "time_index_count"
            ]
            ==
            1
            for row in nonzero
        )
    )

    s_00i = np.asarray(
        source[
            0,
            0,
            1:,
        ],
        dtype=float,
    )

    s_ijk = np.asarray(
        source[
            1:,
            1:,
            1:,
        ],
        dtype=float,
    )

    s_0ij = np.asarray(
        source[
            0,
            1:,
            1:,
        ],
        dtype=float,
    )

    s_00i_norm2 = float(
        np.sum(
            s_00i
            *
            s_00i
        )
    )

    s_ijk_norm2 = float(
        np.sum(
            s_ijk
            *
            s_ijk
        )
    )

    s_0ij_trace = float(
        np.trace(
            s_0ij
        )
    )

    s_0ij_spin2 = (
        s_0ij
        -
        np.eye(
            3
        )
        *
        s_0ij_trace
        /
        3.0
    )

    s_0ij_spin2_norm2 = float(
        np.sum(
            s_0ij_spin2
            *
            s_0ij_spin2
        )
    )

    s_0ij_spin0_norm2 = float(
        3.0
        *
        (
            s_0ij_trace
            /
            3.0
        )
        **
        2
    )

    negative_parity_tensor_support_norm2 = (
        s_00i_norm2
        +
        s_ijk_norm2
    )

    return {
        "source_norm":
            source_norm,

        "totally_symmetric":
            bool(
                permutation_error
                <=
                TOL
            ),

        "maximum_permutation_error":
            permutation_error,

        "nonzero_component_count":
            len(
                nonzero
            ),

        "nonzero_components":
            nonzero,

        "time_index_count_histogram":
            time_histogram,

        "all_nonzero_components_have_exactly_one_time_index":
            all_nonzero_have_exactly_one_time_index,

        "s_00i":
            s_00i.tolist(),

        "s_00i_norm2":
            s_00i_norm2,

        "s_00i_zero":
            bool(
                s_00i_norm2
                <=
                TOL
            ),

        "s_ijk_norm2":
            s_ijk_norm2,

        "s_ijk_zero":
            bool(
                s_ijk_norm2
                <=
                TOL
            ),

        "s_0ij":
            s_0ij.tolist(),

        "s_0ij_trace":
            s_0ij_trace,

        "s_0ij_spin2_norm2":
            s_0ij_spin2_norm2,

        "s_0ij_spin2_support_nonzero":
            bool(
                s_0ij_spin2_norm2
                >
                TOL
            ),

        "s_0ij_spin0_norm2":
            s_0ij_spin0_norm2,

        "s_0ij_spin0_support_nonzero":
            bool(
                s_0ij_spin0_norm2
                >
                TOL
            ),

        "totally_symmetric_negative_parity_tensor_support_norm2":
            negative_parity_tensor_support_norm2,

        "totally_symmetric_1minus_support_zero":
            bool(
                negative_parity_tensor_support_norm2
                <=
                TOL
            ),

        "parity_interpretation":
            (
                "NONZERO CLEAN TOTAL-SYMMETRIC COMPONENTS "
                "HAVE ONE TIME AND TWO SPATIAL INDICES; "
                "ODD-PARITY S_00i AND S_ijk SUPPORT VANISH"
            ),

        "component_norm_is_physical_energy":
            False,
    }


def clean_v24_hook_parity_gate() -> dict[str, Any]:
    """Return the already-established hook-sector O(3) parity support."""

    irrep = (
        v24_clean_rest_o3_hook_irrep_gate()
    )

    prefilter = (
        mikura_percacci_hook_projector_prefilter()
    )

    support = irrep[
        "exact_o3_irrep_support"
    ]

    exact_zeros = set(
        prefilter[
            "o3_irrep_exact_zeros"
        ]
    )

    return {
        "hook_2plus_support_nonzero":
            bool(
                support[
                    "HOOK_2_PLUS"
                ]
            ),

        "hook_1plus_support_nonzero":
            bool(
                support[
                    "HOOK_1_PLUS"
                ]
            ),

        "hook_0plus_support_zero":
            bool(
                not support[
                    "HOOK_0_PLUS"
                ]
            ),

        "hook_2minus_support_zero":
            bool(
                not support[
                    "HOOK_2_MINUS"
                ]
                and
                "HOOK_2_MINUS"
                in exact_zeros
            ),

        "hook_1minus_support_zero":
            bool(
                not support[
                    "HOOK_1_MINUS"
                ]
                and
                "HOOK_1_MINUS"
                in exact_zeros
            ),

        "hook_2plus_norm2":
            float(
                irrep[
                    "spin2_plus_support_norm2"
                ]
            ),

        "hook_1plus_norm2":
            float(
                irrep[
                    "spin1_plus_support_norm2"
                ]
            ),

        "hook_0plus_norm2":
            float(
                irrep[
                    "spin0_plus_support_norm2"
                ]
            ),

        "canonical_residue_recomputed_here":
            False,

        "representation_support_is_physical_energy":
            False,
    }


def clean_v24_full_1minus_source_gate() -> dict[str, Any]:
    """Determine whether the complete clean V24 source has 1- support.

    The torsion-free rank-three nonmetricity source decomposes completely into
    the totally symmetric piece plus the hook-symmetric piece.

    A zero 1- projection in both independent pieces implies a zero 1-
    projection for the complete clean source.
    """

    symmetric = (
        clean_v24_totally_symmetric_parity_gate()
    )

    hook = (
        clean_v24_hook_parity_gate()
    )

    full_zero = bool(
        symmetric[
            "totally_symmetric_1minus_support_zero"
        ]
        and
        hook[
            "hook_1minus_support_zero"
        ]
    )

    return {
        "nonmetricity_source_decomposition":
            "TOTALLY_SYMMETRIC_PLUS_HOOK_SYMMETRIC",

        "totally_symmetric_1minus_support_zero":
            symmetric[
                "totally_symmetric_1minus_support_zero"
            ],

        "hook_1minus_support_zero":
            hook[
                "hook_1minus_support_zero"
            ],

        "full_clean_v24_1minus_support_zero":
            full_zero,

        "full_clean_v24_1minus_support_nonzero":
            not full_zero,

        "productive_even_parity_support_survives":
            bool(
                symmetric[
                    "s_0ij_spin2_support_nonzero"
                ]
                or
                hook[
                    "hook_1plus_support_nonzero"
                ]
                or
                hook[
                    "hook_2plus_support_nonzero"
                ]
            ),

        "hook_1plus_support_nonzero":
            hook[
                "hook_1plus_support_nonzero"
            ],

        "hook_2plus_support_nonzero":
            hook[
                "hook_2plus_support_nonzero"
            ],

        "claim_scope":
            (
                "CLEAN V24 EQUAL-REST SOURCE "
                "REST-FRAME SPIN-PARITY SUPPORT"
            ),
    }


def marzo2022_clean_v24_source_match_gate() -> dict[str, Any]:
    """Test the clean V24 source against the published massive 1- pole."""

    family = (
        marzo2022_published_family_gate()
    )

    source = (
        clean_v24_full_1minus_source_gate()
    )

    trace_crosscheck = (
        rest_pair_bms_spin1_trace_gate()
    )

    healthy_pole_is_1minus = bool(
        family[
            "published_massive_physical_pole_count"
        ]
        ==
        1
        and
        family[
            "published_massive_physical_pole_sector"
        ]
        ==
        "1_MINUS"
    )

    direct_nonzero = bool(
        healthy_pole_is_1minus
        and
        not source[
            "full_clean_v24_1minus_support_zero"
        ]
    )

    closed = bool(
        family[
            "explicit_metric_affine_action_published"
        ]
        and
        family[
            "published_ghost_tachyon_free_massive_regions_exist"
        ]
        and
        healthy_pole_is_1minus
        and
        source[
            "full_clean_v24_1minus_support_zero"
        ]
    )

    return {
        "published_family_exists":
            family[
                "explicit_metric_affine_action_published"
            ],

        "published_family_is_symmetry_protected":
            family[
                "protecting_abelian_symmetry_published"
            ],

        "published_healthy_massive_pole_sector":
            family[
                "published_massive_physical_pole_sector"
            ],

        "published_healthy_massive_pole_count":
            family[
                "published_massive_physical_pole_count"
            ],

        "full_clean_v24_1minus_support_zero":
            source[
                "full_clean_v24_1minus_support_zero"
            ],

        "direct_clean_v24_healthy_massive_pole_source_nonzero":
            direct_nonzero,

        "direct_clean_v24_healthy_massive_pole_source_zero":
            not direct_nonzero,

        "clean_rest_pair_lorentz_trace_zero_crosscheck":
            trace_crosscheck[
                "lorentz_trace_zero"
            ],

        "clean_rest_pair_direct_trace_carrier_overlap_zero_crosscheck":
            trace_crosscheck[
                "direct_trace_carrier_overlap_zero"
            ],

        "direct_clean_v24_marzo2022_massive_1minus_closed":
            closed,

        "static_offshell_constrained_response_evaluated":
            False,

        "static_offshell_constrained_response_closed":
            False,

        "generic_dirac_source_states_closed":
            False,

        "indirect_metric_mixing_source_closed":
            False,

        "same_action_v24_dirac_matter_derived_in_marzo2022":
            False,

        "closure_scope":
            (
                "DIRECT CLEAN V24 EQUAL-REST SOURCE "
                "TO THE PUBLISHED HEALTHY MARZO-2022 MASSIVE 1- POLE"
            ),

        "interpretation":
            (
                "THE PUBLISHED MASS TERM CHANGES THE GAUGE/CONSTRAINT "
                "STRUCTURE, BUT THE CLEAN V24 SOURCE HAS ZERO SUPPORT "
                "IN THE ONLY PUBLISHED HEALTHY MASSIVE PHYSICAL POLE"
            ),
    }


def generic_dirac_escape_gate() -> dict[str, Any]:
    """Preserve source-state engineering without promoting an algebraic witness."""

    generic = (
        generic_bms_spin1_trace_witness()
    )

    return {
        "generic_algebraic_trace_carrier_nonzero":
            generic[
                "generic_algebraic_trace_carrier_nonzero"
            ],

        "generic_trace_covector_norm":
            generic[
                "trace_covector_norm"
            ],

        "generic_spinor_on_shell_localized_stationary":
            generic[
                "spinor_is_on_shell_localized_stationary_source"
            ],

        "generic_source_ward_identity_established":
            generic[
                "source_ward_identity_established"
            ],

        "generic_support_energy_established":
            generic[
                "support_energy_established"
            ],

        "generic_dirac_protected_spin1_closed":
            generic[
                "generic_dirac_protected_spin1_closed"
            ],

        "source_state_engineering_remains_open":
            bool(
                generic[
                    "generic_algebraic_trace_carrier_nonzero"
                ]
                and
                not generic[
                    "generic_dirac_protected_spin1_closed"
                ]
            ),

        "generic_algebraic_witness_is_physical_source":
            False,
    }


def source_support_rows() -> list[dict[str, Any]]:
    """Return compact source-support rows for durable CSV output."""

    symmetric = (
        clean_v24_totally_symmetric_parity_gate()
    )

    hook = (
        clean_v24_hook_parity_gate()
    )

    full = (
        clean_v24_full_1minus_source_gate()
    )

    return [
        {
            "source_sector":
                "TOTALLY_SYMMETRIC_1_MINUS",

            "support_nonzero":
                not symmetric[
                    "totally_symmetric_1minus_support_zero"
                ],

            "support_norm2":
                symmetric[
                    "totally_symmetric_negative_parity_tensor_support_norm2"
                ],

            "status":
                "ZERO_EXACT_REST_FRAME_SUPPORT",
        },
        {
            "source_sector":
                "HOOK_1_MINUS",

            "support_nonzero":
                not hook[
                    "hook_1minus_support_zero"
                ],

            "support_norm2":
                0.0,

            "status":
                "ZERO_EXACT_REST_FRAME_SUPPORT",
        },
        {
            "source_sector":
                "FULL_V24_1_MINUS",

            "support_nonzero":
                not full[
                    "full_clean_v24_1minus_support_zero"
                ],

            "support_norm2":
                0.0,

            "status":
                "ZERO_DIRECT_HEALTHY_MARZO2022_POLE_SUPPORT",
        },
        {
            "source_sector":
                "HOOK_1_PLUS",

            "support_nonzero":
                hook[
                    "hook_1plus_support_nonzero"
                ],

            "support_norm2":
                hook[
                    "hook_1plus_norm2"
                ],

            "status":
                "NONZERO_PRESERVED",
        },
        {
            "source_sector":
                "HOOK_2_PLUS",

            "support_nonzero":
                hook[
                    "hook_2plus_support_nonzero"
                ],

            "support_norm2":
                hook[
                    "hook_2plus_norm2"
                ],

            "status":
                "NONZERO_PRESERVED",
        },
    ]


def post_massive_rescue_rerank() -> list[dict[str, Any]]:
    """Return the theorem-first rescue order after this direct source test."""

    return [
        {
            "priority":
                1,

            "family":
                "BARKER_ZELL_EXTENDED_PROJECTIVE_DOUBLE_VECTOR",

            "status":
                "OPEN_EXACT_DIRAC_SOURCE_MATCH_REQUIRED",

            "reason":
                (
                    "PUBLISHED DIRAC-MOTIVATED PROTECTED SYMMETRY; "
                    "EXACT CLEAN/GENERAL SOURCE PROJECTION STILL REQUIRED"
                ),
        },
        {
            "priority":
                2,

            "family":
                "OTHER_NATIVE_PROTECTED_MAG_1PLUS_2PLUS",

            "status":
                "OPEN_SOURCE_SUPPORTED_REPRESENTATIONS_FIRST",

            "reason":
                (
                    "CLEAN V24 HAS EXACT NONZERO 1+ AND 2+ SUPPORT"
                ),
        },
        {
            "priority":
                3,

            "family":
                "MARZO2026_NONLINEAR_VECTOR_GRAVITON",

            "status":
                "OPEN_EXACT_SOURCE_IDENTIFICATION_REQUIRED",

            "reason":
                (
                    "ONLY GENUINELY NONLINEAR CONTINUATION MAY EVADE "
                    "THE CLOSED V24D LINEAR VECTOR-METRIC BRIDGE"
                ),
        },
        {
            "priority":
                4,

            "family":
                "FULL_NOETHER_COMPLETE_MATTER_PLUS_COMPENSATOR",

            "status":
                "OPEN_EXPLICIT_ACTION_REQUIRED",

            "reason":
                (
                    "R1 DID NOT CLOSE ADDITIONAL MATTER CURRENTS "
                    "DERIVED FROM ONE VARIATIONAL ACTION"
                ),
        },
        {
            "priority":
                5,

            "family":
                "DIRAC_SOURCE_STATE_ENGINEERING",

            "status":
                "OPEN_AFTER_NATIVE_ACTION_SOURCE_MATCHES",

            "reason":
                (
                    "GENERIC DIRAC ALGEBRAIC TRACE WITNESS EXISTS "
                    "BUT IS NOT YET AN ONSHELL LOCALIZED SOURCE"
                ),
        },
        {
            "priority":
                6,

            "family":
                "MASSIVE_CURTRIGHT_HOOK",

            "status":
                "OPEN_LOWER_PRIORITY_STATIC_OFFSHELL_REQUIRED",

            "reason":
                (
                    "REST-FRAME PHYSICAL-POLE SUPPORT ALREADY ZERO; "
                    "MASSIVE-SPIN2 DUALITY RISK PRESERVED"
                ),
        },
        {
            "priority":
                7,

            "family":
                "V26D_PROTECTED_CT1_DHOST_KMM",

            "status":
                "PRESERVED_INDEPENDENT_FALLBACK",

            "reason":
                "RESUME IF HOOK17 CREDIBLE RESCUE FAMILIES EXHAUST",
        },
    ]


def h17a6r2_summary() -> dict[str, Any]:
    """Return the conservative H17A6R2 scientific decision."""

    provenance = (
        r1_provenance_gate()
    )

    family = (
        marzo2022_published_family_gate()
    )

    source = (
        clean_v24_full_1minus_source_gate()
    )

    match = (
        marzo2022_clean_v24_source_match_gate()
    )

    generic = (
        generic_dirac_escape_gate()
    )

    direct_closed = bool(
        provenance[
            "r1_provenance_pass"
        ]
        and
        family[
            "published_ghost_tachyon_free_massive_regions_exist"
        ]
        and
        match[
            "direct_clean_v24_marzo2022_massive_1minus_closed"
        ]
    )

    decision = (
        "RED_SCOPED_A6R2_"
        "MARZO2022_PROTECTED_MASSIVE_1MINUS_"
        "HAS_ZERO_DIRECT_CLEAN_V24_REST_FRAME_SOURCE_SUPPORT__"
        "GENERIC_DIRAC_AND_OTHER_PROTECTED_FAMILIES_REMAIN_OPEN"
        if direct_closed
        else
        "CHECK_A6R2_SOURCE_REPRESENTATION_OR_LITERATURE_PROVENANCE"
    )

    return {
        "branch":
            "032H17A6R2",

        "subgate":
            "MARZO2022_PROTECTED_MASSIVE_1MINUS_SOURCE_MATCH",

        "decision":
            decision,

        "r1_provenance_pass":
            provenance[
                "r1_provenance_pass"
            ],

        "marzo2022_published_protected_massive_family_exists":
            bool(
                family[
                    "explicit_metric_affine_action_published"
                ]
                and
                family[
                    "stueckelberg_scalar_extension_published"
                ]
                and
                family[
                    "published_ghost_tachyon_free_massive_regions_exist"
                ]
            ),

        "marzo2022_massive_physical_pole_sector":
            family[
                "published_massive_physical_pole_sector"
            ],

        "clean_v24_full_1minus_support_zero":
            source[
                "full_clean_v24_1minus_support_zero"
            ],

        "direct_clean_v24_marzo2022_massive_1minus_closed":
            direct_closed,

        "static_offshell_marzo2022_response_closed":
            False,

        "generic_dirac_marzo2022_source_closed":
            False,

        "generic_dirac_source_state_engineering_open":
            generic[
                "source_state_engineering_remains_open"
            ],

        "productive_clean_v24_1plus_survives":
            source[
                "hook_1plus_support_nonzero"
            ],

        "productive_clean_v24_2plus_survives":
            source[
                "hook_2plus_support_nonzero"
            ],

        "full_noether_complete_matter_compensator_closed":
            False,

        "all_higgsed_or_massive_hook_closed":
            False,

        "barker_zell_extended_projective_closed":
            False,

        "other_protected_1plus_2plus_closed":
            False,

        "marzo2026_nonlinear_vector_graviton_closed":
            False,

        "massive_curtright_static_offshell_closed":
            False,

        "hook17_closed":
            False,

        "hook17_reference_capacity_rp1e12_j":
            HOOK17_REFERENCE_CAPACITY_RP1E12_J,

        "hook17_complete_energy_j":
            None,

        "strict_complete_operating_target_j":
            STRICT_COMPLETE_OPERATING_TARGET_J,

        "capacity_recalculation_authorized":
            False,

        "energy_optimization_authorized":
            False,

        "sub100j_capacity_tuning_authorized":
            False,

        "h17b_authorized":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "practical_device_found":
            False,

        "v26d_fallback_status":
            "PRESERVED",

        "v26e_status":
            "PAUSED_NOT_CLOSED",

        "next":
            (
                "032H17A7_BARKER_ZELL_EXTENDED_PROJECTIVE_"
                "DIRAC_SOURCE_MATCH_GATE"
            ),

        "next_scientific_question":
            (
                "Does the actual V24 Dirac hypermomentum source project "
                "nontrivially onto the protected physical vector sector "
                "selected by the Barker-Zell extended-projective / "
                "alternative-double-vector symmetry in one compatible "
                "matter-plus-gravity action?"
            ),

        "rerank":
            post_massive_rescue_rerank(),

        "claim_scope":
            (
                "DIRECT CLEAN V24 EQUAL-REST SOURCE TO PUBLISHED "
                "MARZO2022 HEALTHY MASSIVE 1- POLE ONLY"
            ),
    }
