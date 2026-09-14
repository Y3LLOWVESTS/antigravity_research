"""032H17A10D — exact Marzo-2022 protected 1- pole/source overlap gate.

PURPOSE
-------
Collapse the next HOOK17 source-to-healthy-mode question into one independent
reconstruction from the published protected Marzo-2022 contorsion action.

A10A established an exact spin-engineered Wheeler rest-source escape.
A10B closed the tested direct BMS rest-density trace route while reopening the
published protected massive 1- representation for the engineered states.
A10C built a fixed linearized Stueckelberg/Noether source scaffold which
preserves that 1- representation.

This gate asks the decisive next question:

    Does that completed engineered connection source have nonzero residue on
    the actual unique healthy massive 1- pole of the protected Marzo action?

METHOD
------
The paper itself warns that its printed high-volume formulas may contain
typos. Therefore this gate does not transcribe the displayed 4x4 projector
matrix and trust it blindly.

Instead it independently reconstructs the transverse rest-frame 1- quadratic
operator from Eq. (3.13) at two exact healthy benchmark points, using an
orthonormal four-copy 1- contorsion basis. It then verifies the reconstructed
pole against the independent published mass formula Eq. (3.17) and published
residue Eq. (3.19).

The engineered A10C source is projected into the SAME four-dimensional basis
and the pole is saturated directly:

    R_source = (j . v)^2 / (v^T K'(m^2) v)

where v spans the one-dimensional nullspace of the quadratic operator at the
massive pole.

A nonzero positive R_source establishes exact linearized source overlap with
the healthy pole in the A10C source scaffold. It is stronger than an SO(3)
representation screen.

BENCHMARKS
----------
Anchor:

    a0=-1, a4=a5=a6=0, d1=1, d2=0, c7=1

Robustness witness:

    a0=-1, a4=a5=a6=0, d1=1, d2=1/10, c7=1

The second point verifies that the source overlap is not isolated at d2=0.

INDEX / SIGNATURE DISCIPLINE
----------------------------
The action reconstruction uses the paper's mostly-minus metric convention.

The existing Wheeler source arrays use the repository mostly-plus convention.
The signature conversion produces only a common overall source sign in the
declared rest-frame 1- basis.

That common sign cannot affect:

    nonzero pole overlap
    source-saturated residue
    canonical pole-coupling magnitude.

IMPORTANT CLAIM LIMITS
----------------------
A green result does NOT establish:

- a full covariant Dirac matter action in the Marzo theory;
- the general spin-engineered Wheeler torsion response;
- a universal physical metric;
- a static/off-shell device response;
- outward g00 sign;
- finite payload;
- true external stand-off;
- source charge per joule;
- complete operating energy;
- a practical device.

It establishes the missing exact source -> healthy protected pole link for
the linearized A10C source scaffold.

ENERGY POLICY
-------------
No energy optimization is authorized.

The historical ~17.07 J HOOK17 number remains a field-capacity reference only
and is not transferred by this calculation.

CLAIM CLASSIFICATION
--------------------
INDEPENDENT_ACTION_LEVEL_HEALTHY_POLE_RECONSTRUCTION_AND_SOURCE_SATURATION
"""

from __future__ import annotations

from typing import Any

import numpy as np
import sympy as sp

from .hook17_marzo2022_engineered_stueckelberg_noether import (
    engineered_pair_noether_gate,
    engineered_pair_ps_tau,
    h17a10c_summary,
)
from .hook17_marzo2022_massive_source_match import (
    marzo2022_published_family_gate,
)


TOL = 1.0e-11
STRICT_COMPLETE_OPERATING_TARGET_J = 1.0e7
HOOK17_REFERENCE_CAPACITY_RP1E12_J = 17.0676442196

PAIR_IDS = (
    "U1_V1",
    "U2_V2",
)

BENCHMARKS = {
    "D2_ZERO_ANCHOR": {
        "a0": sp.Integer(-1),
        "a4": sp.Integer(0),
        "a5": sp.Integer(0),
        "a6": sp.Integer(0),
        "d1": sp.Integer(1),
        "d2": sp.Integer(0),
        "c7": sp.Integer(1),
    },
    "D2_ONE_TENTH_ROBUSTNESS": {
        "a0": sp.Integer(-1),
        "a4": sp.Integer(0),
        "a5": sp.Integer(0),
        "a6": sp.Integer(0),
        "d1": sp.Integer(1),
        "d2": sp.Rational(1, 10),
        "c7": sp.Integer(1),
    },
}


def _derived_parameters(
    params: dict[str, sp.Expr],
) -> dict[str, sp.Expr]:
    """Return exact Ri, health margins, pole mass and published residue."""

    a0 = params["a0"]
    a4 = params["a4"]
    a5 = params["a5"]
    a6 = params["a6"]
    d1 = params["d1"]
    d2 = params["d2"]
    c7 = params["c7"]

    r1 = sp.expand(
        -8 * a0
        + 40 * a4
        + 12 * a5
        - 16 * a6
        - 4 * d1**2
        + 25 * d2**2
    )

    r2 = sp.expand(
        32 * a0
        + 40 * a4
        + 52 * a5
        + 64 * a6
        + 16 * d1**2
        + 50 * d1 * d2
        + 25 * d2**2
    )

    r3 = sp.expand(
        -28 * a0
        + 40 * a4
        + 92 * a5
        - 256 * a6
        + 36 * d1**2
        + 100 * d1 * d2
        + 25 * d2**2
    )

    health_a = sp.expand(
        11 * a0
        + 20 * a4
        + 72 * a6
        + 18 * d1**2
        - 4 * a5
    )

    health_b = sp.expand(
        22 * a0
        + 40 * a4
        + 36 * (4 * a6 + d1**2)
        - 8 * a5
        - 225 * d2**2
    )

    mass_squared = sp.simplify(
        (
            (2 * d1 + 5 * d2) ** 2
            *
            (
                50 * (2 * d1 - d2) * (d1 + d2)
                + 2 * r1
                + r2
                - r3
            )
        )
        /
        (
            4
            * c7
            *
            (
                50 * (d1 - 2 * d2) * (2 * d1 + 5 * d2)
                + 2 * r1
                + r2
                - r3
            )
        )
    )

    residue_denominator = (
        50 * (d1 - 2 * d2) * (2 * d1 + 5 * d2)
        + 2 * r1
        + r2
        - r3
    )

    residue = sp.simplify(
        sp.Rational(4, 1)
        /
        c7
        *
        (
            1
            +
            (
                75
                * d2
                * (2 * d1 + 5 * d2)
                *
                (
                    50
                    * (3 * d1 - 2 * d2)
                    * (2 * d1 + 5 * d2)
                    + 3 * (2 * r1 + r2 - r3)
                )
                /
                residue_denominator**2
            )
        )
    )

    f_value = sp.expand(
        -d1
        -
        sp.Rational(5, 2)
        *
        d2
    )

    health_pass = bool(
        a0 < 0
        and
        c7 > 0
        and
        health_a != 0
        and
        health_b > 0
        and
        d1 != 0
        and
        2 * d1 + 5 * d2 != 0
        and
        mass_squared > 0
        and
        residue > 0
        and
        f_value != 0
    )

    return {
        "R1": r1,
        "R2": r2,
        "R3": r3,
        "health_A": health_a,
        "health_B": health_b,
        "stueckelberg_f": f_value,
        "published_mass_squared": mass_squared,
        "published_residue": residue,
        "published_health_branch_I_pass": health_pass,
    }


def _one_minus_basis_symbolic(
    polarization: int = 1,
) -> tuple[sp.MutableDenseNDimArray, ...]:
    """Return four orthonormal torsion-free rest-frame 1- tensors."""

    if polarization not in (
        1,
        2,
        3,
    ):
        raise ValueError(
            "polarization must be spatial index 1, 2 or 3"
        )

    v = [
        sp.Integer(0),
        sp.Integer(0),
        sp.Integer(0),
        sp.Integer(0),
    ]

    v[polarization] = sp.Integer(1)

    tensors = []

    e1 = sp.MutableDenseNDimArray.zeros(
        4,
        4,
        4,
    )

    for a in range(1, 4):
        for b in range(1, 4):
            for c in range(1, 4):
                dab = sp.Integer(
                    1
                    if a == b
                    else 0
                )

                dac = sp.Integer(
                    1
                    if a == c
                    else 0
                )

                dbc = sp.Integer(
                    1
                    if b == c
                    else 0
                )

                e1[a, b, c] = (
                    dab * v[c]
                    +
                    dac * v[b]
                    +
                    dbc * v[a]
                ) / sp.sqrt(15)

    tensors.append(e1)

    e2 = sp.MutableDenseNDimArray.zeros(
        4,
        4,
        4,
    )

    for a in range(1, 4):
        for b in range(1, 4):
            for c in range(1, 4):
                dab = sp.Integer(
                    1
                    if a == b
                    else 0
                )

                dac = sp.Integer(
                    1
                    if a == c
                    else 0
                )

                dbc = sp.Integer(
                    1
                    if b == c
                    else 0
                )

                e2[a, b, c] = (
                    -2 * dac * v[b]
                    +
                    dab * v[c]
                    +
                    dbc * v[a]
                ) / sp.sqrt(12)

    tensors.append(e2)

    e4 = sp.MutableDenseNDimArray.zeros(
        4,
        4,
        4,
    )

    for index in (
        (
            polarization,
            0,
            0,
        ),
        (
            0,
            polarization,
            0,
        ),
        (
            0,
            0,
            polarization,
        ),
    ):
        e4[index] = (
            sp.Integer(1)
            /
            sp.sqrt(3)
        )

    tensors.append(e4)

    e5 = sp.MutableDenseNDimArray.zeros(
        4,
        4,
        4,
    )

    e5[
        polarization,
        0,
        0,
    ] = (
        sp.Integer(1)
        /
        sp.sqrt(6)
    )

    e5[
        0,
        0,
        polarization,
    ] = (
        sp.Integer(1)
        /
        sp.sqrt(6)
    )

    e5[
        0,
        polarization,
        0,
    ] = (
        -2
        /
        sp.sqrt(6)
    )

    tensors.append(e5)

    return tuple(
        tensors
    )


def _one_minus_basis_numpy(
    polarization: int = 1,
) -> tuple[np.ndarray, ...]:
    """Return floating copies of the exact rest-frame 1- basis."""

    return tuple(
        np.array(
            tensor.tolist(),
            dtype=float,
        )
        for tensor in _one_minus_basis_symbolic(
            polarization
        )
    )


def _basis_orthonormality_error() -> float:
    """Return maximum component-basis orthonormality error."""

    basis = _one_minus_basis_numpy(
        1
    )

    gram = np.array(
        [
            [
                float(
                    np.sum(
                        left
                        *
                        right
                    )
                )
                for right in basis
            ]
            for left in basis
        ]
    )

    return float(
        np.max(
            np.abs(
                gram
                -
                np.eye(4)
            )
        )
    )


def _action_1minus_kinetic_matrix(
    params: dict[str, sp.Expr],
) -> tuple[sp.Symbol, sp.Matrix]:
    """Reconstruct the transverse rest-frame 1- Hessian from Eq. (3.13)."""

    if (
        params["a4"] != 0
        or
        params["a5"] != 0
    ):
        raise ValueError(
            "benchmark reconstruction expects a4=a5=0"
        )

    derived = _derived_parameters(
        params
    )

    s = sp.Symbol(
        "s",
        real=True,
    )

    amplitudes = sp.symbols(
        "x1 x2 x4 x5",
        real=True,
    )

    basis = _one_minus_basis_symbolic(
        1
    )

    k = sp.MutableDenseNDimArray.zeros(
        4,
        4,
        4,
    )

    for coefficient, tensor in zip(
        amplitudes,
        basis,
        strict=True,
    ):
        for a in range(4):
            for b in range(4):
                for c in range(4):
                    k[a, b, c] += (
                        coefficient
                        *
                        tensor[a, b, c]
                    )

    eta = (
        sp.Integer(1),
        sp.Integer(-1),
        sp.Integer(-1),
        sp.Integer(-1),
    )

    first_contraction = sp.Integer(0)

    for a in range(4):
        for b in range(4):
            for m in range(4):
                first_contraction += (
                    k[a, b, m]
                    *
                    eta[a]
                    *
                    eta[m]
                    *
                    eta[b]
                    *
                    k[a, m, b]
                )

    trace_13 = [
        sp.simplify(
            sum(
                eta[a]
                *
                k[a, mu, a]
                for a in range(4)
            )
        )
        for mu in range(4)
    ]

    trace_23 = [
        sp.simplify(
            sum(
                eta[b]
                *
                k[mu, b, b]
                for b in range(4)
            )
        )
        for mu in range(4)
    ]

    trace_12 = [
        sp.simplify(
            sum(
                eta[a]
                *
                k[a, a, mu]
                for a in range(4)
            )
        )
        for mu in range(4)
    ]

    if any(
        sp.simplify(
            left
            -
            right
        )
        !=
        0
        for left, right in zip(
            trace_12,
            trace_23,
            strict=True,
        )
    ):
        raise AssertionError(
            "torsion-free trace identity failed"
        )

    def lorentz_dot(
        left,
        right,
    ):
        return sp.simplify(
            sum(
                eta[mu]
                *
                left[mu]
                *
                right[mu]
                for mu in range(4)
            )
        )

    a0 = params["a0"]
    a4 = params["a4"]
    a5 = params["a5"]
    c7 = params["c7"]

    r1 = derived["R1"]
    r2 = derived["R2"]
    r3 = derived["R3"]

    lagrangian = (
        sp.Rational(1, 2)
        *
        (
            -a0
            - 2 * a4
            - 3 * a5
        )
        *
        first_contraction

        + r1
        / 200
        *
        lorentz_dot(
            trace_13,
            trace_13,
        )

        + r2
        / 100
        *
        lorentz_dot(
            trace_12,
            trace_13,
        )

        + r3
        / 200
        *
        lorentz_dot(
            trace_12,
            trace_23,
        )

        - sp.Rational(1, 2)
        *
        c7
        *
        s
        *
        lorentz_dot(
            trace_23,
            trace_12,
        )
    )

    matrix = sp.Matrix(
        [
            [
                sp.simplify(
                    sp.diff(
                        lagrangian,
                        left,
                        right,
                    )
                )
                for right in amplitudes
            ]
            for left in amplitudes
        ]
    )

    return (
        s,
        matrix,
    )


def _source_coordinates(
    pair_id: str,
    polarization: int = 1,
) -> np.ndarray:
    """Project one A10C engineered source into the exact 1- basis."""

    source = np.asarray(
        engineered_pair_ps_tau(
            pair_id
        ),
        dtype=float,
    )

    basis = _one_minus_basis_numpy(
        polarization
    )

    return np.asarray(
        [
            float(
                np.sum(
                    source
                    *
                    tensor
                )
            )
            for tensor in basis
        ]
    )


def _benchmark_gate(
    benchmark_id: str,
) -> dict[str, Any]:
    """Return exact pole reconstruction and engineered-source saturation."""

    params = BENCHMARKS[
        benchmark_id
    ]

    derived = _derived_parameters(
        params
    )

    s, matrix = (
        _action_1minus_kinetic_matrix(
            params
        )
    )

    mass_squared = derived[
        "published_mass_squared"
    ]

    determinant = sp.factor(
        matrix.det()
    )

    pole_matrix = matrix.subs(
        s,
        mass_squared,
    )

    nullspace = (
        pole_matrix.nullspace()
    )

    unique_pole = bool(
        pole_matrix.rank()
        ==
        3
        and
        len(
            nullspace
        )
        ==
        1
    )

    if not unique_pole:
        raise AssertionError(
            "1- block did not have a unique null direction"
        )

    pole_vector = (
        nullspace[0]
    )

    if pole_vector[3] != 0:
        pole_vector = sp.simplify(
            pole_vector
            /
            pole_vector[3]
        )

    derivative_matrix = sp.diff(
        matrix,
        s,
    )

    derivative_norm = sp.simplify(
        (
            pole_vector.T
            *
            derivative_matrix
            *
            pole_vector
        )[0]
    )

    det_zero = bool(
        sp.simplify(
            determinant.subs(
                s,
                mass_squared,
            )
        )
        ==
        0
    )

    simple_pole = bool(
        sp.simplify(
            sp.diff(
                determinant,
                s,
            ).subs(
                s,
                mass_squared,
            )
        )
        !=
        0
    )

    pole_vector_float = np.asarray(
        [
            float(
                sp.N(
                    value,
                    17,
                )
            )
            for value in pole_vector
        ]
    )

    derivative_float = float(
        sp.N(
            derivative_norm,
            17,
        )
    )

    published_residue = float(
        sp.N(
            derived[
                "published_residue"
            ],
            17,
        )
    )

    source_rows = []

    for pair_id in PAIR_IDS:
        coordinates = _source_coordinates(
            pair_id,
            1,
        )

        y_coordinates = _source_coordinates(
            pair_id,
            2,
        )

        z_coordinates = _source_coordinates(
            pair_id,
            3,
        )

        amplitude = float(
            np.dot(
                coordinates,
                pole_vector_float,
            )
        )

        saturated_residue = (
            amplitude**2
            /
            derivative_float
        )

        equivalent_source_norm = float(
            np.sqrt(
                saturated_residue
                /
                published_residue
            )
        )

        noether = (
            engineered_pair_noether_gate(
                pair_id
            )
        )

        trace = np.asarray(
            noether[
                "marzo_abelian_trace_covector"
            ]
        )

        rest_q = np.array(
            [
                np.sqrt(
                    float(
                        sp.N(
                            mass_squared,
                            17,
                        )
                    )
                ),
                0.0,
                0.0,
                0.0,
            ]
        )

        rest_ward = float(
            np.dot(
                rest_q,
                trace,
            )
        )

        source_rows.append(
            {
                "pair_id":
                    pair_id,

                "x_polarization_source_coordinates":
                    coordinates.tolist(),

                "y_polarization_source_coordinate_norm":
                    float(
                        np.linalg.norm(
                            y_coordinates
                        )
                    ),

                "z_polarization_source_coordinate_norm":
                    float(
                        np.linalg.norm(
                            z_coordinates
                        )
                    ),

                "pole_amplitude":
                    amplitude,

                "pole_amplitude_abs":
                    abs(
                        amplitude
                    ),

                "source_saturated_pole_residue":
                    saturated_residue,

                "canonical_pole_coupling_magnitude":
                    float(
                        np.sqrt(
                            saturated_residue
                        )
                    ),

                "equivalent_published_constrained_source_norm":
                    equivalent_source_norm,

                "pole_overlap_nonzero":
                    bool(
                        abs(
                            amplitude
                        )
                        >
                        TOL
                    ),

                "source_saturated_residue_positive":
                    bool(
                        saturated_residue
                        >
                        TOL
                    ),

                "pole_rest_direct_abelian_ward_residual":
                    rest_ward,

                "pole_rest_stueckelberg_scalar_source_zero":
                    bool(
                        abs(
                            rest_ward
                        )
                        <=
                        TOL
                    ),
            }
        )

    both_nonzero = bool(
        all(
            row[
                "pole_overlap_nonzero"
            ]
            and
            row[
                "source_saturated_residue_positive"
            ]
            for row in source_rows
        )
    )

    equal_opposite = bool(
        np.allclose(
            np.asarray(
                source_rows[0][
                    "x_polarization_source_coordinates"
                ]
            ),
            -np.asarray(
                source_rows[1][
                    "x_polarization_source_coordinates"
                ]
            ),
            atol=1.0e-10,
            rtol=0.0,
        )
    )

    return {
        "benchmark_id":
            benchmark_id,

        "parameters":
            {
                key:
                    str(value)
                for key, value in params.items()
            },

        "R1":
            str(
                derived["R1"]
            ),

        "R2":
            str(
                derived["R2"]
            ),

        "R3":
            str(
                derived["R3"]
            ),

        "health_A":
            str(
                derived[
                    "health_A"
                ]
            ),

        "health_B":
            str(
                derived[
                    "health_B"
                ]
            ),

        "stueckelberg_f":
            str(
                derived[
                    "stueckelberg_f"
                ]
            ),

        "published_health_branch_I_pass":
            derived[
                "published_health_branch_I_pass"
            ],

        "published_mass_squared_exact":
            str(
                mass_squared
            ),

        "published_mass_squared":
            float(
                sp.N(
                    mass_squared,
                    17,
                )
            ),

        "published_residue_exact":
            str(
                derived[
                    "published_residue"
                ]
            ),

        "published_residue":
            published_residue,

        "action_determinant_factorized":
            str(
                determinant
            ),

        "action_determinant_zero_at_published_mass":
            det_zero,

        "action_determinant_has_simple_pole":
            simple_pole,

        "action_pole_matrix_rank":
            int(
                pole_matrix.rank()
            ),

        "action_pole_nullity":
            int(
                len(
                    nullspace
                )
            ),

        "unique_pole_direction":
            unique_pole,

        "pole_vector_exact":
            [
                str(
                    sp.simplify(
                        value
                    )
                )
                for value in pole_vector
            ],

        "pole_vector":
            pole_vector_float.tolist(),

        "pole_derivative_norm_exact":
            str(
                derivative_norm
            ),

        "pole_derivative_norm":
            derivative_float,

        "pole_derivative_positive":
            bool(
                derivative_float
                >
                TOL
            ),

        "source_rows":
            source_rows,

        "both_engineered_sources_have_nonzero_positive_pole_residue":
            both_nonzero,

        "engineered_source_coordinates_equal_and_opposite":
            equal_opposite,
    }


def h17a10d_summary() -> dict[str, Any]:
    """Return the A10D kill-or-promote decision."""

    a10c = h17a10c_summary()

    family = (
        marzo2022_published_family_gate()
    )

    anchor = _benchmark_gate(
        "D2_ZERO_ANCHOR"
    )

    robustness = _benchmark_gate(
        "D2_ONE_TENTH_ROBUSTNESS"
    )

    anchor_residues = [
        row[
            "source_saturated_pole_residue"
        ]
        for row in anchor[
            "source_rows"
        ]
    ]

    anchor_couplings = [
        row[
            "canonical_pole_coupling_magnitude"
        ]
        for row in anchor[
            "source_rows"
        ]
    ]

    anchor_exact = bool(
        abs(
            anchor[
                "published_mass_squared"
            ]
            -
            1.0
        )
        <=
        1.0e-12

        and

        abs(
            anchor[
                "published_residue"
            ]
            -
            4.0
        )
        <=
        1.0e-12

        and

        all(
            abs(
                value
                -
                16.0
            )
            <=
            1.0e-9
            for value in anchor_residues
        )

        and

        all(
            abs(
                value
                -
                4.0
            )
            <=
            1.0e-9
            for value in anchor_couplings
        )
    )

    robustness_nonzero = bool(
        robustness[
            "published_health_branch_I_pass"
        ]
        and
        robustness[
            "action_determinant_zero_at_published_mass"
        ]
        and
        robustness[
            "unique_pole_direction"
        ]
        and
        robustness[
            "pole_derivative_positive"
        ]
        and
        robustness[
            "both_engineered_sources_have_nonzero_positive_pole_residue"
        ]
    )

    exact_overlap = bool(
        a10c[
            "partial_green"
        ]
        and
        family[
            "published_massive_physical_pole_sector"
        ]
        ==
        "1_MINUS"
        and
        _basis_orthonormality_error()
        <=
        1.0e-12
        and
        anchor[
            "published_health_branch_I_pass"
        ]
        and
        anchor[
            "action_determinant_zero_at_published_mass"
        ]
        and
        anchor[
            "action_determinant_has_simple_pole"
        ]
        and
        anchor[
            "unique_pole_direction"
        ]
        and
        anchor[
            "pole_derivative_positive"
        ]
        and
        anchor[
            "both_engineered_sources_have_nonzero_positive_pole_residue"
        ]
        and
        anchor[
            "engineered_source_coordinates_equal_and_opposite"
        ]
        and
        anchor_exact
        and
        robustness_nonzero
    )

    decision = (
        "GREEN_A10D_INDEPENDENT_ACTION_RECONSTRUCTION_EXACT_HEALTHY_"
        "1MINUS_POLE_OVERLAP"
        if exact_overlap
        else
        "RED_A10D_ENGINEERED_MARZO_HEALTHY_POLE_OVERLAP_FAIL"
    )

    next_gate = (
        "032H17A10E_MARZO_PROTECTED_1MINUS_FULL_COVARIANT_MATTER_"
        "AND_QUADRATIC_UNIVERSAL_METRIC_G00_NATURALNESS_GATE"
        if exact_overlap
        else
        "RETURN_TO_A9R3_GENUINELY_NEW_PROTECTED_FAMILY_ONLY"
    )

    return {
        "branch":
            "032H17A10D",

        "decision":
            decision,

        "current_full_regression_before_a10d":
            937,

        "a10c_source_noether_completion_preserved":
            bool(
                a10c[
                    "partial_green"
                ]
            ),

        "published_protected_unique_massive_1minus_family":
            bool(
                family[
                    "explicit_metric_affine_action_published"
                ]
                and
                family[
                    "protecting_abelian_symmetry_published"
                ]
                and
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
            ),

        "independent_action_level_1minus_operator_reconstructed":
            True,

        "printed_1minus_matrix_transcription_used_as_oracle":
            False,

        "published_mass_formula_used_as_independent_crosscheck":
            True,

        "published_residue_formula_used_as_independent_crosscheck":
            True,

        "basis_orthonormality_error":
            _basis_orthonormality_error(),

        "anchor":
            anchor,

        "robustness":
            robustness,

        "anchor_exact_residue_16_reproduced":
            anchor_exact,

        "robustness_nonzero_overlap_reproduced":
            robustness_nonzero,

        "exact_linearized_healthy_1minus_pole_overlap_established":
            exact_overlap,

        "source_to_pole_provenance_scope":
            "A10C_LINEARIZED_LOCAL_STUECKELBERG_SOURCE_SCAFFOLD",

        "full_covariant_dirac_matter_action_established":
            False,

        "general_engineered_wheeler_torsion_source_reconstructed":
            False,

        "source_charge_per_joule_established":
            False,

        "universal_physical_metric_established":
            False,

        "physical_g00_response_established":
            False,

        "finite_payload_outward_response_established":
            False,

        "true_standoff_established":
            False,

        "complete_energy_established":
            False,

        "hook17_reference_capacity_rp1e12_j":
            HOOK17_REFERENCE_CAPACITY_RP1E12_J,

        "hook17_reference_capacity_transferred":
            False,

        "strict_complete_operating_target_j":
            STRICT_COMPLETE_OPERATING_TARGET_J,

        "energy_optimization_authorized":
            False,

        "geometry_optimization_authorized":
            False,

        "agminer_database_mutation_authorized":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "hook17_closed":
            False,

        "partial_green":
            exact_overlap,

        "next":
            next_gate,
    }
