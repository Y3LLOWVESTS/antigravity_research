"""032V26B1 same-action compatibility and nonlinear hook-metric preflight.

PURPOSE
-------
Test whether the surviving V24 intrinsic Dirac hook source possesses a new
algebraic universal-metric numerator worth carrying into an explicit nonlinear
metric-affine action.

This run deliberately separates two questions:

1. Does the V24 hook source admit a useful nonlinear rank-two metric
   descendant at the algebraic level?

2. Does a currently identified published action already contain, in one
   symmetry-compatible theory,

       microscopic Dirac source
       +
       healthy propagating hook carrier
       +
       nonremovable universal physical-metric response?

The first question may have a positive answer while the second remains NO.

That distinction is mandatory.

SCIENTIFIC CONTEXT
------------------
V24 established an explicit intrinsic Dirac nonmetricity/hypermomentum source.
For the tested equal-amplitude rest particle/antiparticle pair:

- the desired nonmetricity-like source adds;
- the torsion-like contribution can cancel in the tested projection;
- the Weyl/dilation trace vanishes;
- a nonzero hook representation survives;
- an exact hook-to-torsion-like representation map exists.

V24D then closed the tested LINEAR vector-to-metric bridge. The apparent
quadratic vector/graviton mixing diagonalizes after the appropriate
Stueckelberg field redefinition and source Ward reconstruction.

V26A subsequently closed near-singular generic cross mixing as a free gain
engine.

Therefore V26B must seek a genuinely nonlinear active-state NUMERATOR.

RANK-PARITY PREFLIGHT
---------------------
Let

    H_{a(bc)}

be the rank-three hook/nonmetricity carrier.

Using only zero-derivative Lorentz tensors of even rank,

    g_{ab}

and

    epsilon_{abcd},

an algebraic expression LINEAR in H has an odd number of tensor indices before
pairwise contractions. Every contraction changes the number of free indices
by an even amount.

Therefore a zero-derivative covariant symmetric rank-two metric descendant
cannot be built linearly from one H unless an additional odd-rank background
object is supplied.

Symbolically,

    H
      -/-> linear algebraic rank-two metric tensor

under the stated assumptions.

This is only a zero-derivative statement.

For example,

    nabla^a H_{a(mu nu)}

is rank two and is NOT excluded by this theorem.

QUADRATIC METRIC DESCENDANTS
----------------------------
At quadratic order the index-parity obstruction disappears.

Three simple covariant rank-two witnesses are

    A_{mu nu}
        =
    H_{mu a b} H_nu^{ a b}

    B_{mu nu}
        =
    H_{a mu b} H^a_{ nu }{}^b

and

    C_{mu nu}
        =
    g_{mu nu}
    H_{a b c} H^{a b c}.

A universal physical-metric design scaffold could therefore have the form

    g_phys_{mu nu}
        =
    g_{mu nu}
      +
    1 / M_H^2
    [
        c_A A_{mu nu}
        +
        c_B B_{mu nu}
        +
        c_C C_{mu nu}
    ]
      +
    ...

if such a descendant is compatible with the actual protected MAG symmetry,
constraint algebra, radiative structure, and microscopic source.

That compatibility is NOT assumed here.

ACTIVE/OFF-STATE STRUCTURE
--------------------------
For any quadratic descendant Q(H),

    Q(H_bar + delta H)
        =
    Q(H_bar)
      +
    dQ[H_bar; delta H]
      +
    Q(delta H).

Because Q is quadratic,

    dQ[H_bar; delta H]
        =
    Q(H_bar + delta H)
      -
    Q(H_bar)
      -
    Q(delta H).

Hence

    H_bar = 0
        =>
    dQ = 0

while

    H_bar != 0
        =>
    dQ may be nonzero.

This provides an algebraic active-background numerator.

It does NOT by itself prove:

- a protected action;
- a healthy pole;
- radiative protection;
- a Ward-compatible source;
- an empirical loophole;
- antigravity;
- finite-payload response;
- low energy.

SAME-ACTION REQUIREMENT
-----------------------
The project explicitly forbids constructing a model by stitching together

    Wheeler Dirac source
    +
    unrelated healthy MAG propagator
    +
    unrelated matter metric.

The published-action compatibility atlas in this module therefore asks whether
all required arrows are already established in one action.

Current literature ingredients include:

Wheeler 2026, arXiv:2601.09013
    Explicit GL(4)-Dirac torsion/nonmetricity sources.

Barker & Zell 2024, arXiv:2402.14917
    Extended-projective symmetry, Dirac-motivated matter coupling, naturally
    healthy protected metric-affine sectors.

Barker, Marzo & Santoni 2025, arXiv:2505.23894
    Symmetry-first healthy totally symmetric distortion sectors.

Barker, Marzo & Santoni 2025, arXiv:2507.05349
    Symmetry-first pair-antisymmetric rank-three theories with healthy vector
    sectors.

Percacci & Sezgin 2025, arXiv:2508.14211
    Healthy spin-three propagation in symmetric metric-affine gravity at
    linear level.

Marzo 2026, arXiv:2603.24008
    Healthy massless-spin-two / massive-spin-one quadratic structure with
    consistent nonlinear deformation through quartic order.

These are ingredients and comparison theories.

They are NOT silently merged into one theory.

WEAK-FIELD PAYLOAD SCALE
------------------------
For

    g_00 = -(1 + 2 Phi/c^2)

the weak-field acceleration is

    a_i
        =
    (c^2 / 2) partial_i delta g_00.

A 1g change over 0.1 m therefore requires only a lapse variation of order

    |Delta g_00|
        ~
    2 g L / c^2
        ~
    2.18e-17.

This shows that metric invertibility is not automatically the difficult part
for an algebraic active-state descendant.

It says nothing about how much source energy is required to create H.

CLAIM LIMITS
------------
This module does NOT establish:

- an explicit healthy V26 MAG action;
- a microscopic on-shell V26 field;
- canonical source charge per joule;
- Ward compatibility of a proposed nonlinear metric;
- radiative protection;
- empirical consistency;
- finite-payload antigravity;
- support;
- stability;
- complete operating energy;
- a practical device.

No AGMINER model, rejection, action oracle, survivor, mechanism metric, or
region rule is created.

CLAIM_CLASSIFICATION=
PROJECT_DERIVED_ALGEBRAIC_NUMERATOR_AND_SAME_ACTION_PREFLIGHT
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np

from .dirac_hook_vector_bridge import (
    hook_torsionlike_map_diagnostics,
    rest_pair_source_parts,
)


ETA = np.diag(
    [
        -1.0,
        1.0,
        1.0,
        1.0,
    ]
)

C_LIGHT_M_S = 299792458.0
STANDARD_GRAVITY_M_S2 = 9.80665
REFERENCE_PAYLOAD_LENGTH_M = 0.10


def _finite_scalar(
    value: float,
    name: str,
) -> float:
    """Return a finite scalar or raise ValueError."""
    result = float(
        value
    )

    if not math.isfinite(
        result
    ):
        raise ValueError(
            f"{name} must be finite"
        )

    return result


def _validate_hook(
    hook: np.ndarray,
) -> np.ndarray:
    """Return a validated real H_a(bc) hook tensor."""
    h = np.asarray(
        hook,
        dtype=float,
    )

    if h.shape != (
        4,
        4,
        4,
    ):
        raise ValueError(
            "hook must have shape (4,4,4)"
        )

    if not np.all(
        np.isfinite(
            h
        )
    ):
        raise ValueError(
            "hook components must be finite"
        )

    if not np.allclose(
        h,
        np.swapaxes(
            h,
            1,
            2,
        ),
        atol=1.0e-12,
        rtol=0.0,
    ):
        raise ValueError(
            "hook must be symmetric in its last two indices"
        )

    return h


def zero_derivative_linear_metric_descendant_gate() -> dict[str, Any]:
    """Return the rank-parity theorem for an algebraic linear H -> metric map."""
    return {
        "source_rank":
            3,

        "target_rank":
            2,

        "allowed_background_invariant_tensor_ranks":
            [
                2,
                4,
            ],

        "allowed_background_invariants":
            [
                "g_mu_nu",
                "epsilon_mu_nu_rho_sigma",
            ],

        "additional_odd_rank_background_tensor":
            False,

        "zero_derivative_linear_rank2_descendant_exists":
            False,

        "reason":
            (
                "FREE_INDEX_PARITY: A TERM LINEAR_IN_RANK3_HOOK "
                "PLUS_ONLY_EVEN_RANK_INVARIANTS RETAINS_ODD_FREE_INDEX_PARITY "
                "AFTER_PAIRWISE_CONTRACTIONS"
            ),

        "derivative_linear_rank2_descendants_closed":
            False,

        "example_derivative_linear_operator":
            "nabla^a H_a(mu nu)",

        "nonlinear_descendants_closed":
            False,
    }


def rest_pair_hook() -> np.ndarray:
    """Return the actual V24 clean-rest-pair hook source tensor."""
    return np.asarray(
        rest_pair_source_parts()[
            "hook"
        ],
        dtype=float,
    )


def raise_last_two_indices(
    hook: np.ndarray,
) -> np.ndarray:
    """Return H_nu^{ab} from H_nu cd."""
    h = _validate_hook(
        hook
    )

    return np.einsum(
        "ac,bd,ncd->nab",
        ETA,
        ETA,
        h,
    )


def raise_first_and_third_indices(
    hook: np.ndarray,
) -> np.ndarray:
    """Return H^a_nu{}^b from H_c nu d."""
    h = _validate_hook(
        hook
    )

    return np.einsum(
        "ac,bd,cnd->anb",
        ETA,
        ETA,
        h,
    )


def raise_all_indices(
    hook: np.ndarray,
) -> np.ndarray:
    """Return H^{abc} from H_def."""
    h = _validate_hook(
        hook
    )

    return np.einsum(
        "ad,be,cf,def->abc",
        ETA,
        ETA,
        ETA,
        h,
    )


def hook_quadratic_metric_basis(
    hook: np.ndarray,
) -> dict[str, Any]:
    """Return three simple symmetric rank-two H^2 metric descendants."""
    h = _validate_hook(
        hook
    )

    raised_last = (
        raise_last_two_indices(
            h
        )
    )

    raised_first_third = (
        raise_first_and_third_indices(
            h
        )
    )

    raised_all = (
        raise_all_indices(
            h
        )
    )

    tensor_a = np.einsum(
        "mab,nab->mn",
        h,
        raised_last,
    )

    tensor_b = np.einsum(
        "amb,anb->mn",
        h,
        raised_first_third,
    )

    scalar_h2 = float(
        np.einsum(
            "abc,abc->",
            h,
            raised_all,
        )
    )

    tensor_c = (
        ETA
        *
        scalar_h2
    )

    symmetry_errors = {
        "A":
            float(
                np.max(
                    np.abs(
                        tensor_a
                        -
                        tensor_a.T
                    )
                )
            ),

        "B":
            float(
                np.max(
                    np.abs(
                        tensor_b
                        -
                        tensor_b.T
                    )
                )
            ),

        "C":
            float(
                np.max(
                    np.abs(
                        tensor_c
                        -
                        tensor_c.T
                    )
                )
            ),
    }

    return {
        "A":
            tensor_a,

        "B":
            tensor_b,

        "C":
            tensor_c,

        "H2_scalar":
            scalar_h2,

        "symmetry_errors":
            symmetry_errors,

        "all_rank2_descendants_symmetric":
            bool(
                max(
                    symmetry_errors.values()
                )
                <
                1.0e-12
            ),
    }


def quadratic_metric_descendant(
    hook: np.ndarray,
    *,
    coefficient_a: float = 0.0,
    coefficient_b: float = 1.0,
    coefficient_c: float = 0.0,
) -> np.ndarray:
    """Return c_A A + c_B B + c_C C for the declared hook."""
    c_a = _finite_scalar(
        coefficient_a,
        "coefficient_a",
    )

    c_b = _finite_scalar(
        coefficient_b,
        "coefficient_b",
    )

    c_c = _finite_scalar(
        coefficient_c,
        "coefficient_c",
    )

    basis = (
        hook_quadratic_metric_basis(
            hook
        )
    )

    return (
        c_a
        *
        basis[
            "A"
        ]
        +
        c_b
        *
        basis[
            "B"
        ]
        +
        c_c
        *
        basis[
            "C"
        ]
    )


def quadratic_active_background_derivative(
    background_hook: np.ndarray,
    perturbation_hook: np.ndarray,
    *,
    coefficient_a: float = 0.0,
    coefficient_b: float = 1.0,
    coefficient_c: float = 0.0,
) -> np.ndarray:
    """Return the exact first variation of the quadratic metric descendant.

    For quadratic Q,

        dQ[H; dH]
            =
        Q(H+dH) - Q(H) - Q(dH).

    No finite-difference step is needed.
    """
    h_background = _validate_hook(
        background_hook
    )

    h_perturbation = _validate_hook(
        perturbation_hook
    )

    q_total = (
        quadratic_metric_descendant(
            h_background
            +
            h_perturbation,

            coefficient_a=
                coefficient_a,

            coefficient_b=
                coefficient_b,

            coefficient_c=
                coefficient_c,
        )
    )

    q_background = (
        quadratic_metric_descendant(
            h_background,

            coefficient_a=
                coefficient_a,

            coefficient_b=
                coefficient_b,

            coefficient_c=
                coefficient_c,
        )
    )

    q_perturbation = (
        quadratic_metric_descendant(
            h_perturbation,

            coefficient_a=
                coefficient_a,

            coefficient_b=
                coefficient_b,

            coefficient_c=
                coefficient_c,
        )
    )

    return (
        q_total
        -
        q_background
        -
        q_perturbation
    )


def rest_pair_hook_metric_atlas() -> dict[str, Any]:
    """Return nonlinear rank-two witnesses for the actual V24 rest-pair hook."""
    hook = (
        rest_pair_hook()
    )

    basis = (
        hook_quadratic_metric_basis(
            hook
        )
    )

    map_gate = (
        hook_torsionlike_map_diagnostics()
    )

    rows = {}

    for name in (
        "A",
        "B",
        "C",
    ):
        tensor = np.asarray(
            basis[
                name
            ],
            dtype=float,
        )

        rows[
            name
        ] = {
            "tensor":
                tensor.tolist(),

            "tensor_norm":
                float(
                    np.linalg.norm(
                        tensor
                    )
                ),

            "g00_numerator":
                float(
                    tensor[
                        0,
                        0
                    ]
                ),

            "g00_numerator_nonzero":
                bool(
                    abs(
                        float(
                            tensor[
                                0,
                                0
                            ]
                        )
                    )
                    >
                    1.0e-12
                ),

            "maximum_offdiagonal_component":
                float(
                    np.max(
                        np.abs(
                            tensor
                            -
                            np.diag(
                                np.diag(
                                    tensor
                                )
                            )
                        )
                    )
                ),
        }

    return {
        "rest_pair_hook_nonzero":
            bool(
                np.linalg.norm(
                    hook
                )
                >
                1.0e-14
            ),

        "rest_pair_hook_component_norm":
            float(
                np.linalg.norm(
                    hook
                )
            ),

        "hook_last_pair_symmetric":
            bool(
                np.allclose(
                    hook,
                    np.swapaxes(
                        hook,
                        1,
                        2,
                    ),
                    atol=1.0e-12,
                    rtol=0.0,
                )
            ),

        "representation_map_invertible":
            map_gate[
                "representation_map_invertible_on_declared_hook_space"
            ],

        "pair_torsionlike_equals_two_single":
            map_gate[
                "pair_torsionlike_equals_two_single"
            ],

        "H2_scalar":
            float(
                basis[
                    "H2_scalar"
                ]
            ),

        "basis":
            rows,

        "at_least_one_quadratic_g00_numerator_nonzero":
            bool(
                any(
                    row[
                        "g00_numerator_nonzero"
                    ]
                    for row
                    in rows.values()
                )
            ),

        "all_basis_tensors_symmetric":
            basis[
                "all_rank2_descendants_symmetric"
            ],

        "component_norm_is_energy":
            False,

        "quadratic_metric_witness_is_action_oracle":
            False,
    }


def active_offstate_numerator_gate() -> dict[str, Any]:
    """Return exact active/off-state linearization diagnostics."""
    hook = (
        rest_pair_hook()
    )

    zero_hook = np.zeros_like(
        hook
    )

    selected = (
        quadratic_metric_descendant(
            hook,
            coefficient_b=
                1.0,
        )
    )

    active_derivative = (
        quadratic_active_background_derivative(
            hook,
            hook,
            coefficient_b=
                1.0,
        )
    )

    offstate_derivative = (
        quadratic_active_background_derivative(
            zero_hook,
            hook,
            coefficient_b=
                1.0,
        )
    )

    active_expected = (
        2.0
        *
        selected
    )

    active_relative_error = float(
        np.linalg.norm(
            active_derivative
            -
            active_expected
        )
        /
        max(
            np.linalg.norm(
                active_expected
            ),
            1.0,
        )
    )

    offstate_norm = float(
        np.linalg.norm(
            offstate_derivative
        )
    )

    return {
        "selected_basis":
            "B",

        "offstate_background_hook_zero":
            True,

        "offstate_linear_metric_response_norm":
            offstate_norm,

        "offstate_linear_metric_response_zero":
            bool(
                offstate_norm
                <
                1.0e-12
            ),

        "active_background_hook_nonzero":
            True,

        "active_linear_metric_response_norm":
            float(
                np.linalg.norm(
                    active_derivative
                )
            ),

        "active_linear_metric_response_nonzero":
            bool(
                np.linalg.norm(
                    active_derivative
                )
                >
                1.0e-12
            ),

        "quadratic_homogeneity_derivative_relative_error":
            active_relative_error,

        "quadratic_homogeneity_identity_pass":
            bool(
                active_relative_error
                <
                1.0e-12
            ),

        "active_background_numerator_present":
            bool(
                offstate_norm
                <
                1.0e-12
                and
                np.linalg.norm(
                    active_derivative
                )
                >
                1.0e-12
            ),

        "small_principal_eigenvalue_required_by_this_algebra":
            False,

        "protected_symmetry_compatibility_established":
            False,

        "radiative_active_only_protection_established":
            False,
    }


def weak_field_lapse_variation(
    *,
    acceleration_m_s2: float = STANDARD_GRAVITY_M_S2,
    length_m: float = REFERENCE_PAYLOAD_LENGTH_M,
) -> dict[str, float]:
    """Return |Delta g00| ~ 2 a L / c^2."""
    acceleration = _finite_scalar(
        acceleration_m_s2,
        "acceleration_m_s2",
    )

    length = _finite_scalar(
        length_m,
        "length_m",
    )

    if acceleration <= 0.0:
        raise ValueError(
            "acceleration_m_s2 must be positive"
        )

    if length <= 0.0:
        raise ValueError(
            "length_m must be positive"
        )

    lapse = (
        2.0
        *
        acceleration
        *
        length
        /
        C_LIGHT_M_S**2
    )

    return {
        "acceleration_m_s2":
            acceleration,

        "length_m":
            length,

        "absolute_delta_g00":
            lapse,
    }


def normalized_metric_signature(
    tensor: np.ndarray,
    *,
    delta_g00: float,
) -> dict[str, Any]:
    """Apply a normalized tensor load and report metric inertia.

    The tensor is rescaled so its 00 component produces the requested
    delta_g00. This is a metric-invertibility diagnostic only.
    """
    t = np.asarray(
        tensor,
        dtype=float,
    )

    if t.shape != (
        4,
        4,
    ):
        raise ValueError(
            "tensor must have shape (4,4)"
        )

    if not np.all(
        np.isfinite(
            t
        )
    ):
        raise ValueError(
            "tensor components must be finite"
        )

    if not np.allclose(
        t,
        t.T,
        atol=1.0e-12,
        rtol=0.0,
    ):
        raise ValueError(
            "tensor must be symmetric"
        )

    load = _finite_scalar(
        delta_g00,
        "delta_g00",
    )

    t00 = float(
        t[
            0,
            0
        ]
    )

    if abs(
        t00
    ) <= 1.0e-15:
        raise ValueError(
            "tensor 00 component must be nonzero"
        )

    normalized_delta = (
        load
        *
        t
        /
        t00
    )

    metric = (
        ETA
        +
        normalized_delta
    )

    eigenvalues = np.linalg.eigvalsh(
        metric
    )

    negative_count = int(
        np.count_nonzero(
            eigenvalues
            <
            0.0
        )
    )

    positive_count = int(
        np.count_nonzero(
            eigenvalues
            >
            0.0
        )
    )

    determinant = float(
        np.linalg.det(
            metric
        )
    )

    return {
        "requested_delta_g00":
            load,

        "normalization_tensor_g00":
            t00,

        "metric":
            metric.tolist(),

        "eigenvalues":
            eigenvalues.tolist(),

        "negative_eigenvalue_count":
            negative_count,

        "positive_eigenvalue_count":
            positive_count,

        "determinant":
            determinant,

        "lorentzian_signature":
            bool(
                negative_count
                ==
                1
                and
                positive_count
                ==
                3
            ),

        "invertible":
            bool(
                abs(
                    determinant
                )
                >
                1.0e-14
            ),

        "this_is_an_energy_test":
            False,
    }


def same_action_compatibility_atlas() -> list[dict[str, Any]]:
    """Return conservative published-action compatibility rows.

    'NOT_ESTABLISHED' does not mean impossible. It means the required arrow
    has not been established by the cited theory plus the completed project
    reconstruction.
    """
    return [
        {
            "family":
                "WHEELER_2026_GL4_DIRAC_SOURCE",

            "reference":
                "arXiv:2601.09013",

            "explicit_dirac_affine_source":
                "YES",

            "healthy_propagating_hook_mode_same_action":
                "NOT_ESTABLISHED",

            "universal_physical_metric_hook_bridge_same_action":
                "NOT_ESTABLISHED",

            "nonlinear_active_background_bridge_same_action":
                "NOT_ESTABLISHED",

            "current_same_action_survivor":
                False,

            "reason":
                (
                    "SOURCE_SIDE_RESULT_EXISTS_BUT_REQUIRED_HEALTHY_"
                    "PROPAGATING_AND_UNIVERSAL_METRIC_CHAIN_NOT_ESTABLISHED"
                ),
        },
        {
            "family":
                "BARKER_ZELL_2024_EXTENDED_PROJECTIVE",

            "reference":
                "arXiv:2402.14917",

            "explicit_dirac_affine_source":
                "DIRAC_MOTIVATED_COUPLING_PRESENT",

            "healthy_propagating_hook_mode_same_action":
                "NO_MATCH_ESTABLISHED_TO_V24_HOOK",

            "universal_physical_metric_hook_bridge_same_action":
                "NOT_ESTABLISHED",

            "nonlinear_active_background_bridge_same_action":
                "NOT_ESTABLISHED",

            "current_same_action_survivor":
                False,

            "reason":
                (
                    "HEALTHY_SYMMETRY_PROTECTED_ACTION_EXISTS_BUT_"
                    "V24_HOOK_TO_UNIVERSAL_METRIC_CHAIN_NOT_ESTABLISHED"
                ),
        },
        {
            "family":
                "BARKER_MARZO_SANTONI_2025_TORSIONLIKE",

            "reference":
                "arXiv:2507.05349",

            "explicit_dirac_affine_source":
                "NOT_WHEELER_SOURCE_IN_SAME_ACTION",

            "healthy_propagating_hook_mode_same_action":
                "HEALTHY_PAIR_ANTISYMMETRIC_VECTOR_MODES_EXIST",

            "universal_physical_metric_hook_bridge_same_action":
                "NO_DIRECT_DYNAMICAL_METRIC_BRIDGE_IN_DECLARED_UNIVERSAL_IR",

            "nonlinear_active_background_bridge_same_action":
                "OPEN_NOT_ESTABLISHED",

            "current_same_action_survivor":
                False,

            "reason":
                (
                    "V24_REPRESENTATION_MAP_IS_NOT_AN_ACTION_MATCH"
                ),
        },
        {
            "family":
                "PERCACCI_SEZGIN_2025_SYMMETRIC_MAG_SPIN3",

            "reference":
                "arXiv:2508.14211",

            "explicit_dirac_affine_source":
                "NOT_WHEELER_SOURCE_IN_SAME_ACTION",

            "healthy_propagating_hook_mode_same_action":
                "HEALTHY_SPIN3_SECTOR_EXISTS",

            "universal_physical_metric_hook_bridge_same_action":
                "NOT_ESTABLISHED",

            "nonlinear_active_background_bridge_same_action":
                "NOT_ESTABLISHED",

            "current_same_action_survivor":
                False,

            "reason":
                (
                    "V24B_CLEAN_DIRECT_SPIN3_SHORTCUT_CLOSED_IN_TESTED_FORM"
                ),
        },
        {
            "family":
                "MARZO_2026_VECTOR_GRAVITON",

            "reference":
                "arXiv:2603.24008",

            "explicit_dirac_affine_source":
                "NO_V24_DIRAC_HOOK_IDENTIFICATION",

            "healthy_propagating_hook_mode_same_action":
                "HEALTHY_MASSIVE_VECTOR_BUT_HOOK_IDENTIFICATION_NOT_ESTABLISHED",

            "universal_physical_metric_hook_bridge_same_action":
                "LINEAR_ROUTE_CLOSED_BY_PROJECT_V24D",

            "nonlinear_active_background_bridge_same_action":
                "OPEN_NOT_ESTABLISHED",

            "current_same_action_survivor":
                False,

            "reason":
                (
                    "NONLINEAR_COMPLETION_REMAINS_OPEN_BUT_NO_CURRENT_"
                    "SAME_ACTION_DIRAC_HOOK_TO_METRIC_CHAIN"
                ),
        },
    ]


def proposed_same_action_scaffold() -> dict[str, Any]:
    """Return the explicit V26 design scaffold without promoting it to an action.

    This merely states the mathematical object that a future exact action would
    need to justify.
    """
    return {
        "schematic_action":
            (
                "S = Integral sqrt(-g) ["
                "(Mpl^2/2) R(g,Gamma) "
                "+ L_protected_MAG(g,Gamma) "
                "+ L_Dirac(g,Gamma,Psi)"
                "] + S_matter[g_phys(g,H(Gamma,g)), chi]"
            ),

        "hook_definition":
            (
                "H_a(bc) = protected hook projection of post-Riemannian "
                "distortion/nonmetricity"
            ),

        "universal_metric_scaffold":
            (
                "g_phys_mn = g_mn + M_H^-2 "
                "[cA H_mab H_n^ab + "
                "cB H_amb H^a_n^b + "
                "cC g_mn H_abc H^abc] + ..."
            ),

        "riemannian_offstate_exact":
            True,

        "offstate_condition":
            "H_a(bc)=0 => g_phys_mn=g_mn",

        "all_ordinary_matter_uses_one_metric":
            True,

        "same_action_dirac_source_proven":
            False,

        "protected_mag_symmetry_compatible_with_metric_scaffold":
            False,

        "constraint_health_proven":
            False,

        "ward_compatibility_proven":
            False,

        "radiative_protection_proven":
            False,

        "empirical_viability_proven":
            False,

        "status":
            "DESIGN_SCAFFOLD_NOT_ACTION_ORACLE",
    }


def v26b1_gate() -> dict[str, Any]:
    """Return the complete conservative V26B1 promotion state."""
    parity = (
        zero_derivative_linear_metric_descendant_gate()
    )

    atlas = (
        rest_pair_hook_metric_atlas()
    )

    active = (
        active_offstate_numerator_gate()
    )

    compatibility = (
        same_action_compatibility_atlas()
    )

    same_action_survivors = [
        row
        for row
        in compatibility
        if row[
            "current_same_action_survivor"
        ]
    ]

    algebraic_witness = bool(
        parity[
            "zero_derivative_linear_rank2_descendant_exists"
        ]
        is False
        and
        atlas[
            "at_least_one_quadratic_g00_numerator_nonzero"
        ]
        and
        active[
            "active_background_numerator_present"
        ]
    )

    return {
        "phase":
            "032V26B1",

        "claim_classification":
            (
                "PROJECT_DERIVED_ALGEBRAIC_NUMERATOR_"
                "AND_SAME_ACTION_PREFLIGHT"
            ),

        "intrinsic_dirac_hook_source_preserved":
            atlas[
                "rest_pair_hook_nonzero"
            ],

        "hook_zero_derivative_linear_metric_descendant":
            parity[
                "zero_derivative_linear_rank2_descendant_exists"
            ],

        "hook_derivative_linear_metric_descendants_closed":
            parity[
                "derivative_linear_rank2_descendants_closed"
            ],

        "hook_quadratic_rank2_metric_descendant_exists":
            atlas[
                "at_least_one_quadratic_g00_numerator_nonzero"
            ],

        "hook_quadratic_active_background_g00_numerator":
            active[
                "active_background_numerator_present"
            ],

        "offstate_linear_hook_metric_response_zero":
            active[
                "offstate_linear_metric_response_zero"
            ],

        "numerator_requires_principal_margin_collapse_at_algebraic_level":
            active[
                "small_principal_eigenvalue_required_by_this_algebra"
            ],

        "published_same_action_survivor_count":
            len(
                same_action_survivors
            ),

        "published_same_action_v26b1_survivor":
            bool(
                same_action_survivors
            ),

        "algebraic_design_witness":
            algebraic_witness,

        "full_symmetry_protected_action_established":
            False,

        "healthy_mode_projection_authorized":
            False,

        "action_oracle_authorized":
            False,

        "energy_optimization_authorized":
            False,

        "agminer_database_mutation_authorized":
            False,

        "finite_payload_claim_authorized":
            False,

        "practical_model_claim_authorized":
            False,

        "next_primary":
            (
                "032V26C_EXPLICIT_SYMMETRY_COMPATIBLE_"
                "HOOK_METRIC_ACTION_CONSTRUCTION"
            ),

        "fallback_if_same_action_cannot_be_constructed":
            (
                "RERANK_TO_PROTECTED_ACTIVE_ONLY_CT1_DHOST_KMM"
            ),
    }
