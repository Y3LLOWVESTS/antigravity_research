"""032H17A9R2 — projectively completed Dirac matter-action gate.

PURPOSE
-------
Continue HOOK17 after A9R1.

A9:
    established a nonzero exact source numerator on the healthy
    Percacci-Sezgin massive 1+ pole.

A9R1:
    showed that the UNMODIFIED Wheeler Dirac source is not projectively
    compatible as a matter-action identity:

        16 Hermitian source directions tested
        3 projectively compatible
        13 projectively incompatible.

But A9R1 also established:

    clean A9 source remains projectively compatible;

    exact healthy 1+ pole numerator remains 1.44;

    no independent local algebraic obstruction exists in the
    diffeomorphism Ward equation.

A9R2 asks whether a genuinely projectively invariant matter interaction can
preserve the tensor source responsible for the A9 pole.

TWO MATTER CLASSES
------------------

CLASS A
    Conventional Lorentz-spinor projectively invariant Dirac kinetic term.

The standard antisymmetrized spinor covariant derivative is projectively
invariant. At first derivative / mass dimension <=4 its non-Riemannian
fermion couplings reduce to vector irreps:

    axial torsion T_HAT_mu

and the projectively invariant vector combination involving:

    T_mu
    Q_mu
    Q_HAT_mu.

The pure rank-three tensor parts of torsion/nonmetricity are not directly
sourced in that conventional matter class.

For torsion-free P&S gravity the axial torsion channel is absent.

A9R2 proves that the most general torsion-free, projective-trace-free
rank-three source constructed locally and algebraically from ONE vector
current has zero physical massive 1+ pole numerator.

Thus the conventional projectively invariant Lorentz-Dirac vector class
cannot reproduce the A9 tensor pole source.

CLASS B
    Projectively traceless Wheeler/world-spinor distortion coupling.

Let the torsion-free distortion be:

    N_cab = N_bac.

The torsion-free projective gauge image is:

    G(v)_cab
        =
    eta_ab v_c
        +
    eta_ac v_b.

For d dimensions:

    tr[G(v)]_c
        =
    (d+1) v_c,

where

    tr[X]_c = eta^ab X_cab.

Therefore the local projector

    P[X]
        =
    X
        -
    G(tr[X])/(d+1)

has:

    P^2 = P
    P G(v) = 0
    tr(PX) = 0.

With the Lorentz tensor inner product it is also self-adjoint.

Hence the interaction scaffold

    S_int
        =
    integral sqrt(-g)
        H_W^{cab}(psi)
        P[N]_cab

is invariant under the linearized projective shift of the distortion.

Because P is self-adjoint, variation with respect to N produces

    tau_completed
        =
    P[H_W].

This is not state-by-state source surgery.

It is the source obtained from a declared local interaction using only the
projectively invariant part of the distortion.

A9 CLEAN SOURCE
---------------
The clean A9 source already obeys:

    tr(tau_clean) = 0.

Therefore:

    P[tau_clean]
        =
    tau_clean

exactly.

If the exact P&S 1+ numerator remains 1.44 after this projection, then the
projective completion preserves the key A9 positive result.

IMPORTANT CLAIM LIMIT
---------------------
This is still only a LINEARIZED LOCAL MATTER-INTERACTION SCAFFOLD.

A9R2 does NOT establish:

- a nonlinear covariant world-spinor representation;
- the complete curved-space Dirac kinetic action;
- the actual same-action metric stress tensor;
- the full nonlinear Noether identity;
- radiative protection of the matter coupling;
- the V26B1 metric numerator from this same action;
- one universal physical metric;
- finite-payload antigravity;
- complete operating energy;
- a practical device.

The next gate must covariantly lift the surviving scaffold or close it.

ENERGY POLICY
-------------
No energy optimization.

17.0676442196 J remains only the preserved HOOK17 field-capacity reference.

Complete operating energy remains unknown.

H17B remains unauthorized.

CLAIM_CLASSIFICATION
--------------------
PROJECTIVE_MATTER_ACTION_SCAFFOLD_AND_CONVENTIONAL_DIRAC_CLASS_FALSIFICATION
"""

from __future__ import annotations

from typing import Any

import numpy as np

from .hook17_percacci_sezgin_1plus_projector import (
    percacci_sezgin_case_i_gate,
    torsion_free_ps_source,
)

from .hook17_ps_wheeler_same_action_noether import (
    h17a9r1_summary,
    hermitian_spinor_probe_set,
    projective_traces,
    ps_torsion_free_source_for_spinor,
)


ETA = np.diag(
    [
        -1.0,
        1.0,
        1.0,
        1.0,
    ]
)

DIMENSION = 4

TOL = 1.0e-12

HOOK17_REFERENCE_CAPACITY_RP1E12_J = 17.0676442196
STRICT_COMPLETE_OPERATING_TARGET_J = 1.0e7


def a9r1_provenance_gate() -> dict[str, Any]:
    """Require exact A9R1 starting state."""

    result = h17a9r1_summary()

    passed = bool(
        result[
            "a9_provenance_pass"
        ]
        and
        result[
            "direct_unmodified_wheeler_ps_same_action_closed"
        ]
        and
        result[
            "a9_exact_1plus_pole_overlap_preserved"
        ]
        and
        result[
            "local_symmetric_sigma_completion_exists"
        ]
        and
        not result[
            "projectively_completed_wheeler_matter_action_closed"
        ]
        and
        not result[
            "hook17_closed"
        ]
    )

    return {
        "a9r1_decision":
            result[
                "decision"
            ],

        "a9r1_provenance_pass":
            passed,

        "unmodified_wheeler_closed":
            result[
                "direct_unmodified_wheeler_ps_same_action_closed"
            ],

        "clean_pole_preserved":
            result[
                "a9_exact_1plus_pole_overlap_preserved"
            ],

        "clean_pole_numerator":
            result[
                "a9_exact_1plus_pole_numerator"
            ],

        "local_sigma_completion_exists":
            result[
                "local_symmetric_sigma_completion_exists"
            ],

        "projective_completion_open":
            not result[
                "projectively_completed_wheeler_matter_action_closed"
            ],

        "hook17_open":
            not result[
                "hook17_closed"
            ],
    }


def conventional_projective_dirac_literature_gate() -> dict[str, Any]:
    """Encode the relevant standard projectively invariant Dirac class."""

    return {
        "family":
            "STANDARD_PROJECTIVELY_INVARIANT_LORENTZ_DIRAC",

        "spinor_covariant_derivative_uses_gamma_commutator":
            True,

        "projectively_invariant":
            True,

        "first_derivative":
            True,

        "mass_dimension_at_most_four":
            True,

        "direct_axial_torsion_source":
            True,

        "direct_torsion_trace_vector_source":
            True,

        "direct_nonmetricity_q_vector_source":
            True,

        "direct_nonmetricity_qhat_vector_source":
            True,

        "direct_pure_tensor_nonmetricity_source":
            False,

        "direct_pure_tensor_torsion_source":
            False,

        "torsion_free_ps_axial_torsion_available":
            False,

        "remaining_torsion_free_source_class":
            "PROJECTIVELY_INVARIANT_VECTOR_TRACE_SECTOR",

        "same_as_wheeler_world_spinor_tensor_source":
            False,

        "claim_scope":
            (
                "LOCAL FIRST-DERIVATIVE STANDARD LORENTZ-SPINOR "
                "PROJECTIVELY INVARIANT MATTER CLASS"
            ),
    }


def _require_tf_rank3(
    tensor: np.ndarray,
) -> np.ndarray:
    """Return finite first-third symmetric rank-three tensor."""

    value = np.asarray(
        tensor,
        dtype=float,
    )

    if value.shape != (
        4,
        4,
        4,
    ):
        raise ValueError(
            "tensor must have shape (4,4,4)"
        )

    if not np.all(
        np.isfinite(
            value
        )
    ):
        raise ValueError(
            "tensor must be finite"
        )

    return value


def projective_trace_vector(
    tensor: np.ndarray,
) -> np.ndarray:
    """Return t_c = eta^ab X_cab."""

    value = _require_tf_rank3(
        tensor
    )

    return np.einsum(
        "ab,cab->c",
        ETA,
        value,
    )


def projective_gauge_image(
    vector: np.ndarray,
) -> np.ndarray:
    """Return torsion-free projective gauge image G(v)_cab."""

    v = np.asarray(
        vector,
        dtype=float,
    )

    if v.shape != (
        4,
    ):
        raise ValueError(
            "vector must have shape (4,)"
        )

    result = np.zeros(
        (
            4,
            4,
            4,
        ),
        dtype=float,
    )

    for c in range(
        4
    ):
        for a in range(
            4
        ):
            for b in range(
                4
            ):
                result[
                    c,
                    a,
                    b,
                ] = (
                    ETA[
                        a,
                        b
                    ]
                    *
                    v[
                        c
                    ]
                    +
                    ETA[
                        a,
                        c
                    ]
                    *
                    v[
                        b
                    ]
                )

    return result


def projective_traceless_projection(
    tensor: np.ndarray,
) -> np.ndarray:
    """Return P[X] = X-G(tr X)/(d+1)."""

    value = _require_tf_rank3(
        tensor
    )

    trace = projective_trace_vector(
        value
    )

    return (
        value
        -
        projective_gauge_image(
            trace
        )
        /
        float(
            DIMENSION
            +
            1
        )
    )


def raise_rank3(
    tensor: np.ndarray,
) -> np.ndarray:
    """Raise all three indices with eta."""

    value = _require_tf_rank3(
        tensor
    )

    return np.einsum(
        "ci,aj,bk,ijk->cab",
        ETA,
        ETA,
        ETA,
        value,
    )


def lorentz_rank3_inner(
    left: np.ndarray,
    right: np.ndarray,
) -> float:
    """Return Lorentz tensor inner product."""

    return float(
        np.einsum(
            "cab,cab->",
            _require_tf_rank3(
                left
            ),
            raise_rank3(
                right
            ),
        )
    )


def projector_algebra_gate() -> dict[str, Any]:
    """Verify projector locality, idempotence and gauge annihilation."""

    raw_x = np.arange(
        64,
        dtype=float,
    ).reshape(
        (
            4,
            4,
            4,
        )
    )

    raw_y = np.cos(
        np.arange(
            64,
            dtype=float,
        )
    ).reshape(
        (
            4,
            4,
            4,
        )
    )

    x = (
        0.5
        *
        (
            raw_x
            +
            np.swapaxes(
                raw_x,
                0,
                2,
            )
        )
        /
        17.0
    )

    y = (
        0.5
        *
        (
            raw_y
            +
            np.swapaxes(
                raw_y,
                0,
                2,
            )
        )
    )

    px = projective_traceless_projection(
        x
    )

    ppx = projective_traceless_projection(
        px
    )

    py = projective_traceless_projection(
        y
    )

    vector = np.array(
        [
            0.7,
            -0.2,
            0.4,
            0.9,
        ]
    )

    gauge = projective_gauge_image(
        vector
    )

    projected_gauge = projective_traceless_projection(
        gauge
    )

    trace_px = projective_trace_vector(
        px
    )

    symmetry_error = float(
        np.max(
            np.abs(
                px
                -
                np.swapaxes(
                    px,
                    0,
                    2,
                )
            )
        )
    )

    idempotence_error = float(
        np.linalg.norm(
            ppx
            -
            px
        )
    )

    gauge_error = float(
        np.linalg.norm(
            projected_gauge
        )
    )

    trace_error = float(
        np.linalg.norm(
            trace_px
        )
    )

    self_adjoint_error = abs(
        lorentz_rank3_inner(
            x,
            py,
        )
        -
        lorentz_rank3_inner(
            px,
            y,
        )
    )

    gauge_trace = projective_trace_vector(
        gauge
    )

    expected_gauge_trace = (
        float(
            DIMENSION
            +
            1
        )
        *
        vector
    )

    gauge_trace_error = float(
        np.linalg.norm(
            gauge_trace
            -
            expected_gauge_trace
        )
    )

    return {
        "dimension":
            DIMENSION,

        "projector_is_local_algebraic":
            True,

        "inverse_derivative_used":
            False,

        "inverse_momentum_used":
            False,

        "gauge_trace_reconstruction_error":
            gauge_trace_error,

        "projector_idempotence_error":
            idempotence_error,

        "projector_gauge_annihilation_error":
            gauge_error,

        "projector_output_trace_norm":
            trace_error,

        "projector_preserves_torsion_free_symmetry_error":
            symmetry_error,

        "projector_self_adjoint_error":
            self_adjoint_error,

        "projector_idempotent":
            bool(
                idempotence_error
                <=
                TOL
            ),

        "projector_annihilates_projective_gauge_image":
            bool(
                gauge_error
                <=
                TOL
            ),

        "projector_output_projective_trace_zero":
            bool(
                trace_error
                <=
                TOL
            ),

        "projector_preserves_first_third_symmetry":
            bool(
                symmetry_error
                <=
                TOL
            ),

        "projector_self_adjoint":
            bool(
                self_adjoint_error
                <=
                TOL
            ),
    }


def projected_wheeler_probe_rows() -> list[dict[str, Any]]:
    """Project every A9R1 Hermitian Wheeler source into projective subspace."""

    rows: list[dict[str, Any]] = []

    for probe in hermitian_spinor_probe_set():
        raw = ps_torsion_free_source_for_spinor(
            probe[
                "spinor"
            ]
        )

        projected = projective_traceless_projection(
            raw
        )

        trace_12, trace_23 = projective_traces(
            projected
        )

        norm_12 = float(
            np.linalg.norm(
                trace_12
            )
        )

        norm_23 = float(
            np.linalg.norm(
                trace_23
            )
        )

        rows.append(
            {
                "name":
                    probe[
                        "name"
                    ],

                "kind":
                    probe[
                        "kind"
                    ],

                "raw_source_norm":
                    float(
                        np.linalg.norm(
                            raw
                        )
                    ),

                "projected_source_norm":
                    float(
                        np.linalg.norm(
                            projected
                        )
                    ),

                "projected_trace_12":
                    trace_12.tolist(),

                "projected_trace_23":
                    trace_23.tolist(),

                "projected_trace_12_norm":
                    norm_12,

                "projected_trace_23_norm":
                    norm_23,

                "projective_compatible_after_action_projection":
                    bool(
                        norm_12
                        <=
                        1.0e-11
                        and
                        norm_23
                        <=
                        1.0e-11
                    ),
            }
        )

    return rows


def all_probe_projective_completion_gate() -> dict[str, Any]:
    """Test projective source identity over complete Wheeler probe basis."""

    rows = projected_wheeler_probe_rows()

    all_pass = all(
        row[
            "projective_compatible_after_action_projection"
        ]
        for row in rows
    )

    maximum_trace = max(
        max(
            row[
                "projected_trace_12_norm"
            ],
            row[
                "projected_trace_23_norm"
            ],
        )
        for row in rows
    )

    return {
        "probe_count":
            len(
                rows
            ),

        "all_16_projected_wheeler_probes_projective_compatible":
            bool(
                len(
                    rows
                )
                ==
                16
                and
                all_pass
            ),

        "maximum_projected_trace_norm":
            maximum_trace,

        "state_by_state_parameter_fitting_used":
            False,

        "single_fixed_projector_used_for_all_sources":
            True,

        "rows":
            rows,
    }


def exact_ps_1plus_numerator_for_source(
    source: np.ndarray,
) -> dict[str, Any]:
    """Evaluate P&S Case-I massive 1+ pole numerator for arbitrary tau."""

    tau = _require_tf_rank3(
        source
    )

    case = percacci_sezgin_case_i_gate()

    mass2 = float(
        case[
            "m_plus_squared"
        ]
    )

    mass = float(
        np.sqrt(
            mass2
        )
    )

    q_up = np.array(
        [
            mass,
            0.0,
            0.0,
            0.0,
        ]
    )

    q_cov = (
        ETA
        @
        q_up
    )

    div1 = np.einsum(
        "c,cab->ab",
        q_up,
        tau,
    )

    current = (
        0.5
        *
        (
            div1
            -
            div1.T
        )
    )

    transverse = (
        ETA
        +
        np.outer(
            q_up,
            q_up,
        )
        /
        mass2
    )

    projected_current = np.einsum(
        "ac,bd,cd->ab",
        transverse,
        transverse,
        current,
    )

    numerator = float(
        np.einsum(
            "ab,ab->",
            current,
            projected_current,
        )
    )

    return {
        "m_plus_squared":
            mass2,

        "q_up":
            q_up.tolist(),

        "q_cov":
            q_cov.tolist(),

        "antisymmetric_div1_norm":
            float(
                np.linalg.norm(
                    current
                )
            ),

        "double_transverse_current_norm":
            float(
                np.linalg.norm(
                    projected_current
                )
            ),

        "pole_numerator":
            numerator,

        "pole_numerator_nonzero":
            bool(
                abs(
                    numerator
                )
                >
                TOL
            ),
    }


def clean_projected_source_gate() -> dict[str, Any]:
    """Verify projective action projection leaves clean A9 source unchanged."""

    clean = np.asarray(
        torsion_free_ps_source(),
        dtype=float,
    )

    projected = projective_traceless_projection(
        clean
    )

    difference = float(
        np.linalg.norm(
            projected
            -
            clean
        )
    )

    trace = projective_trace_vector(
        clean
    )

    nonzero_indices = np.argwhere(
        np.abs(
            clean
        )
        >
        TOL
    )

    all_distinct = bool(
        len(
            nonzero_indices
        )
        >
        0
        and
        all(
            len(
                set(
                    map(
                        int,
                        row,
                    )
                )
            )
            ==
            3
            for row in nonzero_indices
        )
    )

    raw_pole = exact_ps_1plus_numerator_for_source(
        clean
    )

    projected_pole = exact_ps_1plus_numerator_for_source(
        projected
    )

    return {
        "clean_source_norm":
            float(
                np.linalg.norm(
                    clean
                )
            ),

        "clean_projective_trace_norm":
            float(
                np.linalg.norm(
                    trace
                )
            ),

        "clean_source_already_projective_traceless":
            bool(
                np.linalg.norm(
                    trace
                )
                <=
                TOL
            ),

        "clean_nonzero_components_have_all_distinct_indices":
            all_distinct,

        "projected_minus_clean_norm":
            difference,

        "projective_completion_leaves_clean_source_unchanged":
            bool(
                difference
                <=
                TOL
            ),

        "raw_clean_1plus_pole_numerator":
            raw_pole[
                "pole_numerator"
            ],

        "projected_clean_1plus_pole_numerator":
            projected_pole[
                "pole_numerator"
            ],

        "projected_clean_1plus_pole_numerator_nonzero":
            projected_pole[
                "pole_numerator_nonzero"
            ],

        "a9_numerator_preserved_exactly":
            bool(
                abs(
                    raw_pole[
                        "pole_numerator"
                    ]
                    -
                    projected_pole[
                        "pole_numerator"
                    ]
                )
                <=
                TOL
                and
                abs(
                    projected_pole[
                        "pole_numerator"
                    ]
                    -
                    1.44
                )
                <=
                1.0e-11
            ),
    }


def vector_tracefree_source(
    vector: np.ndarray,
    amplitude: float = 1.0,
) -> np.ndarray:
    """Most general parity-even TF projective-tracefree source from one vector.

    With first-third symmetry the parity-even metric/vector basis is

        eta_ab V_c + eta_ac V_b
        eta_cb V_a.

    Projective trace freedom fixes their relative coefficient:

        tau_cab
          =
        A (
            eta_ab V_c
            +
            eta_ac V_b
            -
            (d+1) eta_cb V_a
        ).

    In d=4 the last coefficient is -5.
    """

    vector = np.asarray(
        vector,
        dtype=float,
    )

    if vector.shape != (
        4,
    ):
        raise ValueError(
            "vector must have shape (4,)"
        )

    result = np.zeros(
        (
            4,
            4,
            4,
        ),
        dtype=float,
    )

    factor = float(
        DIMENSION
        +
        1
    )

    for c in range(
        4
    ):
        for a in range(
            4
        ):
            for b in range(
                4
            ):
                result[
                    c,
                    a,
                    b,
                ] = (
                    amplitude
                    *
                    (
                        ETA[
                            a,
                            b
                        ]
                        *
                        vector[
                            c
                        ]
                        +
                        ETA[
                            a,
                            c
                        ]
                        *
                        vector[
                            b
                        ]
                        -
                        factor
                        *
                        ETA[
                            c,
                            b
                        ]
                        *
                        vector[
                            a
                        ]
                    )
                )

    return result


def conventional_vector_1plus_no_go_gate() -> dict[str, Any]:
    """Prove standard projective vector source has zero P&S massive 1+ pole.

    It is enough to evaluate a basis of four vector currents.

    If the double-transverse physical current is zero for every basis vector,
    linearity makes it zero for every vector current.
    """

    basis = np.eye(
        4,
        dtype=float,
    )

    rows: list[dict[str, Any]] = []

    for index in range(
        4
    ):
        source = vector_tracefree_source(
            basis[
                index
            ]
        )

        trace_12, trace_23 = projective_traces(
            source
        )

        pole = exact_ps_1plus_numerator_for_source(
            source
        )

        rows.append(
            {
                "basis_vector":
                    index,

                "trace_12_norm":
                    float(
                        np.linalg.norm(
                            trace_12
                        )
                    ),

                "trace_23_norm":
                    float(
                        np.linalg.norm(
                            trace_23
                        )
                    ),

                "antisymmetric_div1_norm":
                    pole[
                        "antisymmetric_div1_norm"
                    ],

                "double_transverse_current_norm":
                    pole[
                        "double_transverse_current_norm"
                    ],

                "pole_numerator":
                    pole[
                        "pole_numerator"
                    ],

                "physical_1plus_current_zero":
                    bool(
                        pole[
                            "double_transverse_current_norm"
                        ]
                        <=
                        TOL
                    ),
            }
        )

    all_zero = all(
        row[
            "physical_1plus_current_zero"
        ]
        for row in rows
    )

    maximum_numerator = max(
        abs(
            row[
                "pole_numerator"
            ]
        )
        for row in rows
    )

    return {
        "vector_basis_count":
            len(
                rows
            ),

        "most_general_parity_even_tf_projective_vector_source_tested":
            True,

        "parity_odd_axial_rank3_source_survives_tf_symmetrization":
            False,

        "all_vector_basis_physical_1plus_currents_zero":
            all_zero,

        "maximum_vector_basis_1plus_numerator":
            maximum_numerator,

        "standard_projective_lorentz_dirac_vector_class_1plus_closed":
            bool(
                all_zero
                and
                maximum_numerator
                <=
                TOL
            ),

        "clean_a9_tensor_source_closed":
            False,

        "rows":
            rows,

        "interpretation":
            (
                "VECTOR TRACE SOURCES PRODUCE q-WEDGE-V CURRENTS "
                "THAT ARE REMOVED BY THE DOUBLE-TRANSVERSE MASSIVE "
                "1+ PROJECTOR; THE A9 ALL-DISTINCT TENSOR SOURCE IS "
                "REPRESENTATIONALLY DIFFERENT"
            ),
    }


def projected_wheeler_action_scaffold_gate() -> dict[str, Any]:
    """Classify the explicit local projective distortion interaction."""

    algebra = projector_algebra_gate()
    probes = all_probe_projective_completion_gate()
    clean = clean_projected_source_gate()

    scaffold = bool(
        algebra[
            "projector_idempotent"
        ]
        and
        algebra[
            "projector_annihilates_projective_gauge_image"
        ]
        and
        algebra[
            "projector_output_projective_trace_zero"
        ]
        and
        algebra[
            "projector_preserves_first_third_symmetry"
        ]
        and
        algebra[
            "projector_self_adjoint"
        ]
        and
        probes[
            "all_16_projected_wheeler_probes_projective_compatible"
        ]
        and
        clean[
            "projective_completion_leaves_clean_source_unchanged"
        ]
        and
        clean[
            "a9_numerator_preserved_exactly"
        ]
    )

    return {
        "declared_interaction":
            (
                "S_INT=INTEGRAL SQRT(-g) "
                "H_W^{cab}(psi) P[N]_{cab}"
            ),

        "distortion_n":
            "N=A-GAMMA_LEVI_CIVITA",

        "projective_projector":
            "P[X]=X-G(TR[X])/5",

        "projector_local":
            algebra[
                "projector_is_local_algebraic"
            ],

        "projector_idempotent":
            algebra[
                "projector_idempotent"
            ],

        "projector_self_adjoint":
            algebra[
                "projector_self_adjoint"
            ],

        "projector_annihilates_gauge_image":
            algebra[
                "projector_annihilates_projective_gauge_image"
            ],

        "variation_source":
            "TAU_COMPLETED=P[H_W]",

        "all_wheeler_probe_sources_projective_after_variation":
            probes[
                "all_16_projected_wheeler_probes_projective_compatible"
            ],

        "clean_source_unchanged":
            clean[
                "projective_completion_leaves_clean_source_unchanged"
            ],

        "clean_1plus_numerator_preserved":
            clean[
                "a9_numerator_preserved_exactly"
            ],

        "linearized_local_projective_matter_action_scaffold_exists":
            scaffold,

        "nonlinear_covariant_world_spinor_lift_established":
            False,

        "actual_same_action_metric_stress_derived":
            False,

        "full_nonlinear_noether_identity_established":
            False,

        "radiative_protection_of_matter_interaction_established":
            False,

        "v26b1_metric_numerator_same_action_derived":
            False,

        "same_action_hook17_complete":
            False,
    }


def h17a9r2_summary() -> dict[str, Any]:
    """Return conservative A9R2 result."""

    provenance = a9r1_provenance_gate()
    literature = conventional_projective_dirac_literature_gate()
    conventional = conventional_vector_1plus_no_go_gate()
    scaffold = projected_wheeler_action_scaffold_gate()
    clean = clean_projected_source_gate()
    probes = all_probe_projective_completion_gate()

    partial_green = bool(
        provenance[
            "a9r1_provenance_pass"
        ]
        and
        conventional[
            "standard_projective_lorentz_dirac_vector_class_1plus_closed"
        ]
        and
        scaffold[
            "linearized_local_projective_matter_action_scaffold_exists"
        ]
        and
        scaffold[
            "clean_1plus_numerator_preserved"
        ]
    )

    return {
        "branch":
            "032H17A9R2",

        "subgate":
            "PROJECTIVELY_COMPLETED_DIRAC_MATTER_ACTION_GATE",

        "decision":
            (
                "GREEN_PARTIAL_A9R2_LOCAL_PROJECTIVE_TRACELESS_"
                "DISTORTION_MATTER_SCAFFOLD_PRESERVES_A9_1PLUS_POLE__"
                "STANDARD_PROJECTIVE_LORENTZ_DIRAC_VECTOR_CLASS_CLOSED__"
                "FULL_COVARIANT_WORLD_SPINOR_LIFT_REMAINS_OPEN"
            )
            if partial_green
            else
            "CHECK_A9R2_PROJECTOR_OR_POLE_PRESERVATION",

        "a9r1_provenance_pass":
            provenance[
                "a9r1_provenance_pass"
            ],

        "unmodified_wheeler_ps_same_action_closed":
            provenance[
                "unmodified_wheeler_closed"
            ],

        "standard_projective_lorentz_dirac_action_exists":
            literature[
                "projectively_invariant"
            ],

        "standard_projective_lorentz_dirac_pure_tensor_source":
            literature[
                "direct_pure_tensor_nonmetricity_source"
            ],

        "standard_projective_lorentz_dirac_vector_class_1plus_closed":
            conventional[
                "standard_projective_lorentz_dirac_vector_class_1plus_closed"
            ],

        "projective_projector_local":
            scaffold[
                "projector_local"
            ],

        "projective_projector_idempotent":
            scaffold[
                "projector_idempotent"
            ],

        "projective_projector_self_adjoint":
            scaffold[
                "projector_self_adjoint"
            ],

        "projective_projector_annihilates_gauge_image":
            scaffold[
                "projector_annihilates_gauge_image"
            ],

        "all_16_projected_wheeler_probes_projective_compatible":
            probes[
                "all_16_projected_wheeler_probes_projective_compatible"
            ],

        "maximum_projected_wheeler_trace_norm":
            probes[
                "maximum_projected_trace_norm"
            ],

        "clean_a9_source_unchanged_by_projective_completion":
            clean[
                "projective_completion_leaves_clean_source_unchanged"
            ],

        "clean_a9_projected_1plus_pole_numerator":
            clean[
                "projected_clean_1plus_pole_numerator"
            ],

        "clean_a9_1plus_pole_numerator_preserved":
            clean[
                "a9_numerator_preserved_exactly"
            ],

        "linearized_local_projective_matter_action_scaffold_exists":
            scaffold[
                "linearized_local_projective_matter_action_scaffold_exists"
            ],

        "nonlinear_covariant_world_spinor_lift_established":
            scaffold[
                "nonlinear_covariant_world_spinor_lift_established"
            ],

        "actual_same_action_metric_stress_derived":
            scaffold[
                "actual_same_action_metric_stress_derived"
            ],

        "full_nonlinear_matter_noether_identity_established":
            scaffold[
                "full_nonlinear_noether_identity_established"
            ],

        "radiative_protection_of_matter_interaction_established":
            scaffold[
                "radiative_protection_of_matter_interaction_established"
            ],

        "v26b1_metric_numerator_same_action_derived":
            False,

        "same_action_hook17_complete":
            False,

        "universal_physical_metric_established":
            False,

        "finite_payload_antigravity_established":
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

        "partial_green":
            partial_green,

        "next":
            (
                "032H17A9R3_COVARIANT_PROJECTIVE_WORLD_SPINOR_"
                "ACTION_AND_METRIC_STRESS_GATE"
            ),

        "next_scientific_question":
            (
                "Can the local projectively traceless Wheeler distortion "
                "interaction be lifted to a fully covariant world-spinor "
                "matter action whose connection source remains the A9R2 "
                "projected hypermomentum and whose metric variation supplies "
                "the required sigma_ab from the same action?"
            ),

        "claim_scope":
            (
                "LINEARIZED LOCAL PROJECTIVELY TRACELESS DISTORTION "
                "MATTER-INTERACTION SCAFFOLD; NOT A COMPLETE COVARIANT "
                "HOOK17 ACTION"
            ),
    }
