"""032H17A12D1R3D0 — polarization-node Maxwell-integrability preflight.

PURPOSE
-------
Determine whether the R3C1-validated interface-loading obstruction can be
structurally suppressed by a static, axisymmetric, single-U(1) mixed-E/B
field whose payload-region fields obey source-free Maxwell equations.

This is intentionally a cheap theorem-first preflight. It is NOT the fully
loaded same-action BVP.

SCIENTIFIC QUESTION
-------------------
Can globally Maxwell-integrable exterior fields approach

    E_t -> 0
    B_n -> 0

through the finite toroidal payload density-gradient layer while preserving

    grad(E dot B)

with the correct whole-payload outward sign?

If yes, authorize a node-centered loaded R3D1 BVP.

If no, do not spend additional runs sculpting the same single-field static
axisymmetric node. Move to the preferred cross-topological F_X dual F_Y
construction.

CLOSED-SURFACE INTEGRABILITY ISSUE
----------------------------------
For static electrostatics in a source-free payload interior,

    E = -grad(phi)
    Laplacian(phi) = 0.

If E_t = 0 on the entire closed payload interface, phi is constant on that
boundary. Harmonic uniqueness then makes phi constant in the bounded payload
interior, so E vanishes there.

For the static axisymmetric poloidal magnetic sector,

    B = -grad(psi_m)
    Laplacian(psi_m) = 0

locally in the source-free payload material. Exact B_n = 0 on the entire
closed interface gives homogeneous Neumann data, leaving no nontrivial
poloidal field in the bounded payload volume.

A solid torus does admit a topological toroidal harmonic magnetic field, but
an axisymmetric electrostatic E is poloidal, so a purely toroidal B has

    E dot B = 0

identically and does not by itself generate the required topological metric
gradient.

Therefore the exact nontrivial single-field closed node is obstructed under
this declared static axisymmetric source-free ansatz.

The scientifically relevant remaining question is whether an APPROXIMATE
node can suppress the interface driver sufficiently while preserving useful
E dot B structure.

METHOD
------
1. Use exact exterior Laplace multipoles l=1...lmax.

2. Construct density-gradient weighted interface trace matrices for

       E_t
       B_n.

3. Solve generalized eigenvalue problems

       T_E v = lambda_E F v
       N_B v = lambda_B F v

   to obtain the Maxwell-integrable fields with the smallest possible
   tangential-electric and normal-magnetic contamination in the declared
   multipole space.

4. Build a deterministic low-dimensional shape library from those trace
   eigenmodes.

5. Pair electric and magnetic shapes and require the resulting

       grad(E dot B)

   acceleration to have one outward sign everywhere in the finite payload.

6. Analytically choose the E/B amplitude ratio that minimizes the dangerous
   interface-driver norm for the required 1-g field product.

7. Compare that driver to the R3B simple mirror at the same 1-g normalization.

8. Repeat across lmax and across two grids resolving the 0.1 m density taper
   with four and five cells.

R3C1 TARGET
-----------
R3C1 directly found first sign loss at approximately

    h=0.040 m:
    lambda_crit = 1.0396081544458862e-5.

This is NOT continuum certified.

R3D0 therefore does not treat it as an engineering tolerance.

For authorization of an expensive loaded single-field BVP, require the
candidate interface driver to be no larger than

    1e-4

of the R3B simple-mirror driver on both validation grids.

That is still only a preflight threshold. The loaded R3D1 BVP remains the
actual test.

ENERGY POLICY
-------------
Do not optimize an already tiny field number.

R3D0 merely rejects pathological node constructions whose EXTERIOR canonical
field capacity exceeds 100 J after exact 1-g normalization.

This exterior field term is NOT complete operating energy.

CLAIM LIMITS
------------
A green R3D0 does not establish:

- a fully loaded solution;
- a microscopic source;
- parity/CP completion;
- source/support energy;
- interacting hyperbolicity;
- nonlinear stability;
- quantum naturalness;
- empirical viability;
- complete energy below 10 MJ;
- replacement of 006D;
- a practical device.

CLAIM CLASSIFICATION
--------------------
PROJECT_MAXWELL_INTEGRABILITY_AND_NODE_FEASIBILITY_PREFLIGHT
"""

from __future__ import annotations

import json
import math
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np

from scipy.linalg import eigh
from scipy.special import eval_legendre

from .hook17_concurrent_u1_fieldstrength_metric import (
    C_LIGHT_M_S,
    EV_J,
    HBAR_C_EV_M,
    PAYLOAD_MAJOR_RADIUS_M,
    PAYLOAD_MINOR_RADIUS_M,
    REFERENCE_PORTAL_SCALE_EV,
    SOURCE_RADIUS_M,
    TARGET_ACCELERATION_M_S2,
    _payload_mask,
    payload_center_z_m,
)

from .hook17_f2_strong_payload_loading_rescue import (
    PRIMARY_DENSITY_MODEL,
    payload_density_profile_kg_m3,
)

from .hook17_fdual_f_global_mirror_prefight import (
    PRIMARY_FIT_RADIUS_M,
    fit_exterior_multipoles,
    reconstruct_a12c_field,
)


BRANCH = "032H17A12D1R3D0"

# These grids resolve the 0.1 m finite density-gradient layer with four
# and five cells respectively.
GRID_SPACINGS_M = (
    0.025,
    0.020,
)

# Deliberately increase harmonic freedom progressively. This is not a random
# geometry search.
LMAX_VALUES = (
    4,
    8,
    12,
    16,
    20,
)

LOW_MODE_COUNT = 6

LOCAL_PADDING_M = 0.15

# Finest directly resolved R3C1 first-sign-loss value.
# Diagnostic only; not continuum certified.
R3C1_FINE_CRITICAL_LOADING = (
    1.0396081544458862e-5
)

# A candidate within one order of magnitude of the provisional R3C1
# suppression requirement is worth the expensive fully loaded BVP.
BVP_AUTHORIZATION_DRIVER_RATIO = (
    1.0e-4
)

FIELD_CAPACITY_GUARDRAIL_J = (
    100.0
)

GROSS_NODE_REORIENTATION_DEG = (
    45.15505016895276
)

NODE_TAPER_ROTATION_DEG = (
    4.591569781127255
)


def _repo_root() -> Path:
    return (
        Path(__file__)
        .resolve()
        .parents[3]
    )


@lru_cache(maxsize=1)
def r3c1_artifact() -> dict[str, Any]:
    path = (
        _repo_root()
        /
        "results"
        /
        "data"
        /
        "032h17a12d1r3c1_hook17_fdual_f_exact_reciprocity_ultrasmall_summary.json"
    )

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def provenance_gate() -> dict[str, Any]:
    data = (
        r3c1_artifact()
    )

    passed = bool(
        data.get(
            "authorize_r3d0_node_integrability_prefight"
        )
        is True

        and

        data.get(
            "full_variational_certificate_pass_all_grids"
        )
        is True

        and

        data.get(
            "direct_vs_woodbury_pass_original_grids"
        )
        is True

        and

        data.get(
            "physical_antigravity_model_found"
        )
        is False

        and

        data.get(
            "006d_replaced"
        )
        is False
    )

    return {
        "pass":
            passed,

        "r3c1_decision":
            data.get(
                "decision"
            ),

        "r3c1_finest_direct_threshold":
            float(
                data[
                    "refined_first_loss_lambdas"
                ][
                    "0.04"
                ]
            ),

        "physical_antigravity_model_found":
            False,

        "006d_replaced":
            False,
    }


def closed_surface_integrability_gate() -> dict[str, Any]:
    return {
        "scope":
            "STATIC_SOURCE_FREE_PAYLOAD_INTERIOR_"
            "AXISYMMETRIC_POLARIZATION_NODE",

        "electric_statement":
            (
                "Et=0 on the entire closed payload interface makes "
                "electrostatic phi constant on that boundary; Laplace "
                "uniqueness then makes E=0 in the source-free payload "
                "interior."
            ),

        "poloidal_magnetic_statement":
            (
                "Bn=0 on the entire closed interface gives homogeneous "
                "Neumann data for the single-valued harmonic magnetic "
                "scalar potential in the axisymmetric poloidal sector; "
                "the poloidal B field is then trivial inside the payload."
            ),

        "toroidal_loophole":
            (
                "A nontrivial toroidal harmonic B field is topologically "
                "allowed in a solid-torus region, but an axisymmetric "
                "electrostatic E is poloidal, so that purely toroidal "
                "loophole has E dot B = 0 identically."
            ),

        "exact_nontrivial_single_field_closed_node":
            False,

        "approximate_node_still_open":
            True,

        "cross_topological_fallback_preserved":
            True,
    }


def _local_grid(
    h: float,
) -> dict[str, Any]:
    center = (
        payload_center_z_m()
    )

    half = (
        PAYLOAD_MINOR_RADIUS_M
        +
        LOCAL_PADDING_M
    )

    rhos = np.arange(
        PAYLOAD_MAJOR_RADIUS_M
        -
        half,
        PAYLOAD_MAJOR_RADIUS_M
        +
        half
        +
        0.5
        *
        h,
        h,
    )

    zs = np.arange(
        center
        -
        half,
        center
        +
        half
        +
        0.5
        *
        h,
        h,
    )

    rho, z = np.meshgrid(
        rhos,
        zs,
    )

    if (
        float(
            np.min(
                np.sqrt(
                    rho**2
                    +
                    z**2
                )
            )
        )
        <=
        SOURCE_RADIUS_M
    ):
        raise RuntimeError(
            "R3D0 local grid entered the source sphere"
        )

    return {
        "h":
            float(
                h
            ),

        "rhos":
            rhos,

        "zs":
            zs,

        "rho":
            rho,

        "z":
            z,
    }


def _legendre_derivative(
    ell: int,
    x: np.ndarray,
) -> np.ndarray:
    if ell == 0:
        return np.zeros_like(
            x
        )

    p = eval_legendre(
        ell,
        x,
    )

    pm1 = eval_legendre(
        ell
        -
        1,
        x,
    )

    return (
        ell
        *
        (
            pm1
            -
            x
            *
            p
        )
        /
        (
            1.0
            -
            x**2
        )
    )


def exterior_multipole_basis(
    grid: dict[str, Any],
    lmax: int,
) -> dict[str, np.ndarray]:
    """Return unit-amplitude source-free exterior multipole fields.

    For each ell >= 1 use

        psi_l
            =
        (R_s/r)^(ell+1) P_ell(cos theta)

    and return

        F_l = -grad psi_l.

    These are exactly curl-free and divergence-free in the source-free
    payload region.

    No ell=0 mode is included, so no electric or magnetic monopole is used.
    """

    rho = np.asarray(
        grid[
            "rho"
        ],
        dtype=float,
    )

    z = np.asarray(
        grid[
            "z"
        ],
        dtype=float,
    )

    radius = np.sqrt(
        rho**2
        +
        z**2
    )

    x = (
        z
        /
        radius
    )

    sin_theta = (
        rho
        /
        radius
    )

    frho = []
    fz = []

    for ell in range(
        1,
        int(
            lmax
        )
        +
        1,
    ):
        p = eval_legendre(
            ell,
            x,
        )

        dp = (
            _legendre_derivative(
                ell,
                x,
            )
        )

        common = (
            SOURCE_RADIUS_M ** (
                ell
                +
                1
            )
            /
            radius ** (
                ell
                +
                2
            )
        )

        f_r = (
            (
                ell
                +
                1.0
            )
            *
            common
            *
            p
        )

        f_theta = (
            common
            *
            sin_theta
            *
            dp
        )

        frho.append(
            f_r
            *
            sin_theta
            +
            f_theta
            *
            x
        )

        fz.append(
            f_r
            *
            x
            -
            f_theta
            *
            sin_theta
        )

    return {
        "rho":
            np.asarray(
                frho
            ),

        "z":
            np.asarray(
                fz
            ),
    }


def interface_geometry(
    grid: dict[str, Any],
) -> dict[str, Any]:
    rho = np.asarray(
        grid[
            "rho"
        ]
    )

    z = np.asarray(
        grid[
            "z"
        ]
    )

    h = float(
        grid[
            "h"
        ]
    )

    density = (
        payload_density_profile_kg_m3(
            rho,
            z,
            PRIMARY_DENSITY_MODEL,
        )
    )

    d_density_dz, d_density_drho = (
        np.gradient(
            density,
            h,
            h,
            edge_order=2,
        )
    )

    grad = np.sqrt(
        d_density_drho**2
        +
        d_density_dz**2
    )

    layer = (
        grad
        >
        1.0e-8
        *
        float(
            np.max(
                grad
            )
        )
    )

    n_rho = np.zeros_like(
        grad
    )

    n_z = np.zeros_like(
        grad
    )

    np.divide(
        d_density_drho,
        grad,
        out=n_rho,
        where=layer,
    )

    np.divide(
        d_density_dz,
        grad,
        out=n_z,
        where=layer,
    )

    volume = (
        2.0
        *
        math.pi
        *
        rho
        *
        h**2
    )

    # Strongest density-gradient cells receive strongest weight.
    weight = (
        grad
        *
        volume
        *
        layer
    )

    payload = (
        _payload_mask(
            rho,
            z,
        )
    )

    return {
        "density":
            density,

        "grad":
            grad,

        "layer":
            layer,

        "n_rho":
            n_rho,

        "n_z":
            n_z,

        "weight":
            weight,

        "payload":
            payload,
    }


def _gram(
    rows: np.ndarray,
    weight: np.ndarray,
) -> np.ndarray:
    return np.einsum(
        "in,n,jn->ij",
        rows,
        weight,
        rows,
        optimize=True,
    )


def trace_grams(
    basis: dict[str, np.ndarray],
    geom: dict[str, Any],
) -> dict[str, np.ndarray]:
    layer = np.asarray(
        geom[
            "layer"
        ]
    )

    weight = np.asarray(
        geom[
            "weight"
        ]
    )[
        layer
    ]

    n_rho = np.asarray(
        geom[
            "n_rho"
        ]
    )[
        layer
    ]

    n_z = np.asarray(
        geom[
            "n_z"
        ]
    )[
        layer
    ]

    f_rho = np.asarray(
        basis[
            "rho"
        ]
    )[
        :,
        layer
    ]

    f_z = np.asarray(
        basis[
            "z"
        ]
    )[
        :,
        layer
    ]

    tangent = (
        -f_rho
        *
        n_z[
            None,
            :
        ]
        +
        f_z
        *
        n_rho[
            None,
            :
        ]
    )

    normal = (
        f_rho
        *
        n_rho[
            None,
            :
        ]
        +
        f_z
        *
        n_z[
            None,
            :
        ]
    )

    total = (
        _gram(
            f_rho,
            weight,
        )
        +
        _gram(
            f_z,
            weight,
        )
    )

    return {
        "total":
            total,

        "tangent":
            _gram(
                tangent,
                weight,
            ),

        "normal":
            _gram(
                normal,
                weight,
            ),
    }


def generalized_trace_modes(
    bad: np.ndarray,
    total: np.ndarray,
) -> dict[str, np.ndarray]:
    """Find the least-bad Maxwell-integrable interface trace modes."""

    scale = max(
        float(
            np.trace(
                total
            )
        )
        /
        max(
            total.shape[
                0
            ],
            1,
        ),
        1.0,
    )

    total_regularized = (
        0.5
        *
        (
            total
            +
            total.T
        )
        +
        1.0e-12
        *
        scale
        *
        np.eye(
            total.shape[
                0
            ]
        )
    )

    bad_symmetric = (
        0.5
        *
        (
            bad
            +
            bad.T
        )
    )

    values, vectors = eigh(
        bad_symmetric,
        total_regularized,
    )

    order = np.argsort(
        values
    )

    return {
        "fractions_squared":
            np.clip(
                values[
                    order
                ],
                0.0,
                None,
            ),

        "vectors":
            vectors[
                :,
                order
            ],

        "total_regularized":
            total_regularized,
    }


def _normalize(
    coefficient: np.ndarray,
    metric: np.ndarray,
) -> np.ndarray:
    norm_squared = float(
        coefficient
        @
        metric
        @
        coefficient
    )

    if norm_squared <= 0.0:
        raise RuntimeError(
            "nonpositive candidate norm"
        )

    return (
        coefficient
        /
        math.sqrt(
            norm_squared
        )
    )


def shape_library(
    modes: dict[str, np.ndarray],
    count: int = LOW_MODE_COUNT,
) -> list[dict[str, Any]]:
    """Build deterministic combinations of the lowest trace modes."""

    vectors = np.asarray(
        modes[
            "vectors"
        ]
    )

    metric = np.asarray(
        modes[
            "total_regularized"
        ]
    )

    k = min(
        int(
            count
        ),
        vectors.shape[
            1
        ],
    )

    output: list[
        dict[str, Any]
    ] = []

    for i in range(
        k
    ):
        output.append(
            {
                "id":
                    f"m{i}",

                "coeff":
                    _normalize(
                        vectors[
                            :,
                            i
                        ],
                        metric,
                    ),
            }
        )

    # All pairwise sums and differences among the low trace modes.
    for i in range(
        k
    ):
        for j in range(
            i
            +
            1,
            k,
        ):
            for sign in (
                -1.0,
                1.0,
            ):
                coefficient = (
                    vectors[
                        :,
                        i
                    ]
                    +
                    sign
                    *
                    vectors[
                        :,
                        j
                    ]
                )

                output.append(
                    {
                        "id":
                            (
                                f"m{i}"
                                +
                                (
                                    "p"
                                    if sign
                                    >
                                    0.0
                                    else
                                    "m"
                                )
                                +
                                f"m{j}"
                            ),

                        "coeff":
                            _normalize(
                                coefficient,
                                metric,
                            ),
                    }
                )

    # A few three-mode interference directions.
    if k >= 3:
        for s1, s2 in (
            (
                1.0,
                1.0,
            ),
            (
                1.0,
                -1.0,
            ),
            (
                -1.0,
                1.0,
            ),
            (
                -1.0,
                -1.0,
            ),
        ):
            coefficient = (
                vectors[
                    :,
                    0
                ]
                +
                s1
                *
                vectors[
                    :,
                    1
                ]
                +
                s2
                *
                vectors[
                    :,
                    2
                ]
            )

            output.append(
                {
                    "id":
                        (
                            "m0_"
                            +
                            str(
                                int(
                                    s1
                                )
                            )
                            +
                            "m1_"
                            +
                            str(
                                int(
                                    s2
                                )
                            )
                            +
                            "m2"
                        ),

                    "coeff":
                        _normalize(
                            coefficient,
                            metric,
                        ),
                }
            )

    return output


def _field_from_coeff(
    basis: dict[str, np.ndarray],
    coefficient: np.ndarray,
) -> tuple[
    np.ndarray,
    np.ndarray,
]:
    return (
        np.tensordot(
            coefficient,
            basis[
                "rho"
            ],
            axes=(
                0,
                0,
            ),
        ),
        np.tensordot(
            coefficient,
            basis[
                "z"
            ],
            axes=(
                0,
                0,
            ),
        ),
    )


def _acceleration(
    e_rho: np.ndarray,
    e_z: np.ndarray,
    b_rho: np.ndarray,
    b_z: np.ndarray,
    h: float,
) -> np.ndarray:
    dot_eb = (
        e_rho
        *
        b_rho
        +
        e_z
        *
        b_z
    )

    sigma = (
        -2.0
        *
        HBAR_C_EV_M**2
        *
        dot_eb
        /
        REFERENCE_PORTAL_SCALE_EV**4
    )

    d_sigma_dz, _ = (
        np.gradient(
            sigma,
            h,
            h,
            edge_order=2,
        )
    )

    return (
        -C_LIGHT_M_S**2
        *
        d_sigma_dz
    )


def _bad_integral(
    f_rho: np.ndarray,
    f_z: np.ndarray,
    geom: dict[str, Any],
    kind: str,
) -> float:
    n_rho = np.asarray(
        geom[
            "n_rho"
        ]
    )

    n_z = np.asarray(
        geom[
            "n_z"
        ]
    )

    if kind == "tangent":
        component = (
            -f_rho
            *
            n_z
            +
            f_z
            *
            n_rho
        )

    elif kind == "normal":
        component = (
            f_rho
            *
            n_rho
            +
            f_z
            *
            n_z
        )

    else:
        raise ValueError(
            kind
        )

    return float(
        np.sum(
            np.asarray(
                geom[
                    "weight"
                ]
            )
            *
            component**2
        )
    )


def _driver_norm(
    e_rho: np.ndarray,
    e_z: np.ndarray,
    b_rho: np.ndarray,
    b_z: np.ndarray,
    geom: dict[str, Any],
) -> float:
    return math.sqrt(
        _bad_integral(
            e_rho,
            e_z,
            geom,
            "tangent",
        )
        +
        _bad_integral(
            b_rho,
            b_z,
            geom,
            "normal",
        )
    )


def exterior_energy_j(
    coefficient: np.ndarray,
) -> float:
    """Exterior canonical energy for one harmonic scalar field."""

    ells = np.arange(
        1,
        len(
            coefficient
        )
        +
        1,
        dtype=float,
    )

    energy_coefficients = (
        2.0
        *
        math.pi
        *
        SOURCE_RADIUS_M
        *
        (
            ells
            +
            1.0
        )
        /
        (
            2.0
            *
            ells
            +
            1.0
        )
        *
        (
            EV_J
            /
            HBAR_C_EV_M
        )
    )

    return float(
        np.sum(
            energy_coefficients
            *
            np.asarray(
                coefficient
            ) ** 2
        )
    )


@lru_cache(maxsize=1)
def _r3b_reference_amplitudes() -> tuple[float, ...]:
    """Fit the R3B reference only once for the entire R3D0 run."""

    reference = (
        reconstruct_a12c_field(
            0.050
        )
    )

    fit = (
        fit_exterior_multipoles(
            reference,
            PRIMARY_FIT_RADIUS_M,
            12,
        )
    )

    return tuple(
        float(
            value
        )
        for value in fit[
            "boundary_amplitudes"
        ]
    )


def baseline_driver(
    grid: dict[str, Any],
    geom: dict[str, Any],
) -> dict[str, float]:
    """Return same-grid 1-g R3B simple-mirror interface-driver norm."""

    amplitudes = np.asarray(
        _r3b_reference_amplitudes(),
        dtype=float,
    )

    basis = (
        exterior_multipole_basis(
            grid,
            len(
                amplitudes
            ),
        )
    )

    f_rho, f_z = (
        _field_from_coeff(
            basis,
            amplitudes,
        )
    )

    # R3B exterior mirror:
    #
    #     B = +F / sqrt(2)
    #     E = -F / sqrt(2)
    #
    # giving negative E.B and positive sigma.
    e_rho = (
        -f_rho
        /
        math.sqrt(
            2.0
        )
    )

    e_z = (
        -f_z
        /
        math.sqrt(
            2.0
        )
    )

    b_rho = (
        f_rho
        /
        math.sqrt(
            2.0
        )
    )

    b_z = (
        f_z
        /
        math.sqrt(
            2.0
        )
    )

    acceleration = (
        _acceleration(
            e_rho,
            e_z,
            b_rho,
            b_z,
            float(
                grid[
                    "h"
                ]
            ),
        )
    )

    payload = np.asarray(
        geom[
            "payload"
        ]
    )

    minimum = float(
        np.min(
            acceleration[
                payload
            ]
        )
    )

    if minimum <= 0.0:
        raise RuntimeError(
            "R3D0 multipole baseline lost whole-payload outward sign"
        )

    scale = math.sqrt(
        TARGET_ACCELERATION_M_S2
        /
        minimum
    )

    driver = (
        _driver_norm(
            scale
            *
            e_rho,
            scale
            *
            e_z,
            scale
            *
            b_rho,
            scale
            *
            b_z,
            geom,
        )
    )

    return {
        "driver_norm":
            driver,

        "scale":
            scale,

        "minimum_acceleration_m_s2_before_normalization":
            minimum,
    }


def evaluate_pair(
    e_shape: dict[str, Any],
    b_shape: dict[str, Any],
    basis: dict[str, np.ndarray],
    grams: dict[str, np.ndarray],
    grid: dict[str, Any],
    geom: dict[str, Any],
    baseline_driver_norm: float,
) -> dict[str, Any]:
    """Evaluate one E/B shape pair and optimize only its amplitude ratio."""

    c_e = np.asarray(
        e_shape[
            "coeff"
        ]
    )

    c_b = np.asarray(
        b_shape[
            "coeff"
        ]
    )

    e_rho, e_z = (
        _field_from_coeff(
            basis,
            c_e,
        )
    )

    b_rho, b_z = (
        _field_from_coeff(
            basis,
            c_b,
        )
    )

    acceleration = (
        _acceleration(
            e_rho,
            e_z,
            b_rho,
            b_z,
            float(
                grid[
                    "h"
                ]
            ),
        )
    )

    payload = np.asarray(
        geom[
            "payload"
        ]
    )

    minimum_positive_sign = float(
        np.min(
            acceleration[
                payload
            ]
        )
    )

    maximum_positive_sign = float(
        np.max(
            acceleration[
                payload
            ]
        )
    )

    # Reversing one field reverses E.B and the entire metric acceleration.
    minimum_negative_sign = (
        -maximum_positive_sign
    )

    if (
        minimum_negative_sign
        >
        minimum_positive_sign
    ):
        b_rho = (
            -b_rho
        )

        b_z = (
            -b_z
        )

        c_b = (
            -c_b
        )

        acceleration = (
            -acceleration
        )

        minimum = (
            minimum_negative_sign
        )

    else:
        minimum = (
            minimum_positive_sign
        )

    # If neither overall sign produces positive acceleration everywhere,
    # amplitude rescaling cannot repair morphology.
    if minimum <= 0.0:
        return {
            "e_id":
                e_shape[
                    "id"
                ],

            "b_id":
                b_shape[
                    "id"
                ],

            "whole_payload_sign":
                False,

            "minimum_acceleration_m_s2":
                minimum,
        }

    # Acceleration scales as alpha * beta.
    product_scale = (
        TARGET_ACCELERATION_M_S2
        /
        minimum
    )

    e_bad = max(
        float(
            c_e
            @
            grams[
                "tangent"
            ]
            @
            c_e
        ),
        1.0e-300,
    )

    b_bad = max(
        float(
            c_b
            @
            grams[
                "normal"
            ]
            @
            c_b
        ),
        1.0e-300,
    )

    # Minimize
    #
    #     alpha^2 E_t^2 + beta^2 B_n^2
    #
    # subject to alpha beta = product_scale.
    #
    # The exact optimum is
    #
    #     alpha / beta = sqrt(B_bad/E_bad).
    optimized_e_over_b = math.sqrt(
        b_bad
        /
        e_bad
    )

    alpha = math.sqrt(
        product_scale
        *
        optimized_e_over_b
    )

    beta = math.sqrt(
        product_scale
        /
        optimized_e_over_b
    )

    driver = math.sqrt(
        alpha**2
        *
        e_bad
        +
        beta**2
        *
        b_bad
    )

    exterior_energy = (
        alpha**2
        *
        exterior_energy_j(
            c_e
        )
        +
        beta**2
        *
        exterior_energy_j(
            c_b
        )
    )

    total_e = float(
        c_e
        @
        grams[
            "total"
        ]
        @
        c_e
    )

    total_b = float(
        c_b
        @
        grams[
            "total"
        ]
        @
        c_b
    )

    return {
        "e_id":
            e_shape[
                "id"
            ],

        "b_id":
            b_shape[
                "id"
            ],

        "whole_payload_sign":
            True,

        "minimum_acceleration_m_s2":
            TARGET_ACCELERATION_M_S2,

        "maximum_acceleration_m_s2":
            float(
                np.max(
                    acceleration[
                        payload
                    ]
                )
            )
            *
            product_scale,

        "electric_amplitude":
            alpha,

        "magnetic_amplitude":
            beta,

        "optimized_E_over_B_amplitude":
            alpha
            /
            beta,

        "electric_tangent_amplitude_fraction":
            math.sqrt(
                e_bad
                /
                max(
                    total_e,
                    1.0e-300,
                )
            ),

        "magnetic_normal_amplitude_fraction":
            math.sqrt(
                b_bad
                /
                max(
                    total_b,
                    1.0e-300,
                )
            ),

        "driver_norm":
            driver,

        "driver_ratio_vs_r3b":
            driver
            /
            baseline_driver_norm,

        "interface_suppression_factor_vs_r3b":
            baseline_driver_norm
            /
            driver,

        "exterior_canonical_energy_j":
            exterior_energy,

        "sub100j_exterior_capacity":
            bool(
                exterior_energy
                <
                FIELD_CAPACITY_GUARDRAIL_J
            ),
    }


def run_grid_lmax(
    h: float,
    lmax: int,
) -> dict[str, Any]:
    grid = (
        _local_grid(
            float(
                h
            )
        )
    )

    geom = (
        interface_geometry(
            grid
        )
    )

    basis = (
        exterior_multipole_basis(
            grid,
            int(
                lmax
            ),
        )
    )

    grams = (
        trace_grams(
            basis,
            geom,
        )
    )

    # Electric field wants E_t -> 0.
    e_modes = (
        generalized_trace_modes(
            grams[
                "tangent"
            ],
            grams[
                "total"
            ],
        )
    )

    # Magnetic field wants B_n -> 0.
    b_modes = (
        generalized_trace_modes(
            grams[
                "normal"
            ],
            grams[
                "total"
            ],
        )
    )

    e_library = (
        shape_library(
            e_modes
        )
    )

    b_library = (
        shape_library(
            b_modes
        )
    )

    baseline = (
        baseline_driver(
            grid,
            geom,
        )
    )

    rows = []

    for e_shape in e_library:
        for b_shape in b_library:
            rows.append(
                evaluate_pair(
                    e_shape,
                    b_shape,
                    basis,
                    grams,
                    grid,
                    geom,
                    baseline[
                        "driver_norm"
                    ],
                )
            )

    positive = [
        row
        for row in rows
        if row.get(
            "whole_payload_sign"
        )
        is True
    ]

    positive.sort(
        key=lambda row:
        (
            row[
                "driver_ratio_vs_r3b"
            ],
            row[
                "exterior_canonical_energy_j"
            ],
        )
    )

    best = (
        positive[
            0
        ]
        if positive
        else
        None
    )

    return {
        "grid_spacing_m":
            float(
                h
            ),

        "lmax":
            int(
                lmax
            ),

        "interface_cells_across_taper":
            0.1
            /
            float(
                h
            ),

        "electric_exact_trace_floor_amplitude":
            math.sqrt(
                float(
                    e_modes[
                        "fractions_squared"
                    ][
                        0
                    ]
                )
            ),

        "magnetic_exact_trace_floor_amplitude":
            math.sqrt(
                float(
                    b_modes[
                        "fractions_squared"
                    ][
                        0
                    ]
                )
            ),

        "electric_first_four_trace_fractions_squared":
            [
                float(
                    value
                )
                for value in e_modes[
                    "fractions_squared"
                ][
                    :4
                ]
            ],

        "magnetic_first_four_trace_fractions_squared":
            [
                float(
                    value
                )
                for value in b_modes[
                    "fractions_squared"
                ][
                    :4
                ]
            ],

        "electric_shape_count":
            len(
                e_library
            ),

        "magnetic_shape_count":
            len(
                b_library
            ),

        "whole_payload_positive_pair_count":
            len(
                positive
            ),

        "baseline_driver_norm":
            float(
                baseline[
                    "driver_norm"
                ]
            ),

        "best":
            best,
    }


def decision_from_atlas(
    atlas: list[dict[str, Any]],
) -> dict[str, Any]:
    finest_h = min(
        GRID_SPACINGS_M
    )

    companion_h = max(
        GRID_SPACINGS_M
    )

    maximum_lmax = max(
        LMAX_VALUES
    )

    finest = [
        row
        for row in atlas
        if (
            math.isclose(
                row[
                    "grid_spacing_m"
                ],
                finest_h,
            )
            and
            row[
                "lmax"
            ]
            ==
            maximum_lmax
        )
    ][
        0
    ]

    companion = [
        row
        for row in atlas
        if (
            math.isclose(
                row[
                    "grid_spacing_m"
                ],
                companion_h,
            )
            and
            row[
                "lmax"
            ]
            ==
            maximum_lmax
        )
    ][
        0
    ]

    best_finest = (
        finest.get(
            "best"
        )
    )

    best_companion = (
        companion.get(
            "best"
        )
    )

    promote = bool(
        best_finest
        is not None

        and

        best_companion
        is not None

        and

        best_finest[
            "driver_ratio_vs_r3b"
        ]
        <=
        BVP_AUTHORIZATION_DRIVER_RATIO

        and

        best_companion[
            "driver_ratio_vs_r3b"
        ]
        <=
        BVP_AUTHORIZATION_DRIVER_RATIO

        and

        best_finest[
            "sub100j_exterior_capacity"
        ]
        is True

        and

        best_companion[
            "sub100j_exterior_capacity"
        ]
        is True
    )

    if promote:
        decision = (
            "GREEN_R3D0_APPROXIMATE_SINGLE_FIELD_NODE_MAXWELL_INTEGRABLE__"
            "DRIVER_SUPPRESSION_NEAR_R3C1_REQUIREMENT__"
            "AUTHORIZE_FULL_LOADED_R3D1_BVP"
        )

        next_branch = (
            "032H17A12D1R3D1_"
            "NODE_CENTERED_FULL_LOADED_SAME_ACTION_BVP"
        )

    else:
        decision = (
            "RED_SCOPED_R3D0_STATIC_AXISYMMETRIC_SINGLE_FIELD_NODE_"
            "NOT_PROMOTED__EXACT_CLOSED_NODE_OBSTRUCTED_AND_"
            "APPROXIMATE_MULTIPOLE_NODE_MISSES_PREFLIGHT_TARGET__"
            "PIVOT_CROSS_TOPOLOGICAL"
        )

        next_branch = (
            "032H17A12D1R3X0_"
            "CROSS_TOPOLOGICAL_FX_FDUALY_NODE_PREFLIGHT"
        )

    return {
        "decision":
            decision,

        "next":
            next_branch,

        "authorize_single_field_loaded_r3d1":
            promote,

        "authorize_cross_topological_r3x0":
            not promote,

        "provisional_r3c1_interface_ratio_target":
            R3C1_FINE_CRITICAL_LOADING,

        "r3d0_bvp_authorization_driver_ratio":
            BVP_AUTHORIZATION_DRIVER_RATIO,

        "finest_best":
            best_finest,

        "companion_best":
            best_companion,

        "exact_closed_node_nontrivial":
            False,

        "threshold_is_continuum_certified":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "complete_energy_established":
            False,

        "006d_replaced":
            False,
    }
