"""
031D3C-R2
=========

Independent coupled-linear stability closeout for the promoted D3
X + phi + Y microscopic activation field.

WHY THIS RUN EXISTS
-------------------
031D3C and D3C-R established:

* inherited X+phi stability GREEN;
* activation Q-ball dQ/dOmega < 0;
* new Y cross-Hessian ~1.6e-18;
* l=3..8 rightmost searches complete with no physical growth;
* l=1 apparent growth falls approximately linearly with finite-difference h;
* l=1 growth is domain independent;
* h=.1875 continued the zero-mode trend;
* sparse ARPACK which="LR" nevertheless failed to return any eigenpairs in
  several l=0,1,2 searches.

No physical instability was established.

This run therefore DOES NOT use scipy.sparse.linalg.eigs at all.

Independent method
------------------
Use global Chebyshev-Lobatto radial collocation for the reduced radial fields

    q(r) = r delta-field(r)

so q(0)=q(R)=0.

Construct the complete dense five-field quadratic pencil

    s^2 I + s G + K

for:

    X amplitude
    X phase
    scalar u/chi
    Y amplitude sqrt(rho_Y) a
    Y phase sqrt(rho_Y) phase_Y

and diagonalize the entire first-order companion matrix with scipy.linalg.eig.

This is independent of the finite-difference / sparse-ARPACK route.

The exact symmetries are diagnosed with analytic vectors:

    l=0:
        U(1)_X phase
        U(1)_Y phase

    l=1:
        common spatial translation

No relative translation is removed.

Additionally, reproduce the successful D96 diagnostic:

    translation-orthogonal projected K minimum.

If projected K is positive in l=1, then the relative-displacement sector is
not hiding a negative static stiffness after removal of the exact common
translation.

Only l=0,1,2 are recomputed.

l=3..8 are inherited from D3C because their original rightmost solves
completed at both grids.

Claims
------
GREEN closes only coupled-linear stability through l=8 in the declared
flat-space effective X/phi/Y model.

Still open:
    explicit QY reservoir/transfer/reset
    switching radiation
    nonlinear fragmentation
    Einstein/physical-metric backreaction
    radiative naturalness
    empirical constraints
    practical device
"""

from __future__ import annotations

import csv
import gc
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np

from scipy.linalg import (
    eig,
    eigh,
)


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results" / "data"

QBALL_SOURCE = (
    SIM / "031b2a_global_qball_activated_scalar_control.py"
)

D3A_SOURCE = (
    SIM / "031d3a_u1_metric_activation_capacity.py"
)

D3B_SUMMARY = (
    DATA / "031d3b_full_coupled_activation_summary.json"
)

D3C_SUMMARY = (
    DATA / "031d3c_activation_stability_switching_summary.json"
)

D3CR_SUMMARY = (
    DATA / "031d3cr_surgical_closeout_summary.json"
)

D3AR_SUMMARY = (
    DATA / "031d3ar_metric_eft_payload_summary.json"
)

ROBUST_SUMMARY = (
    DATA / "031c96_operating_margin_robustness_summary.json"
)

OUT_JSON = (
    DATA / "031d3cr2_chebyshev_dense_summary.json"
)

OUT_CSV = (
    DATA / "031d3cr2_chebyshev_dense_spectrum.csv"
)


RMAX = 600.0

# Full dense spectra.
#
# Companion dimensions are:
#   10*(N-1)
#
# N=160 -> 1590 x 1590.
BASE_N_VALUES = (
    112,
    144,
    176,
)

# Extra l=1 refinement.
L1_EXTRA_N = 208

# Domain crosscheck with similar central resolution.
L1_DOMAIN_RMAX = 800.0
L1_DOMAIN_N = 224

PHASE_OVERLAP_MIN = 0.90
TRANSLATION_OVERLAP_MIN = 0.95

# Symmetry classification ALSO requires small |s| so a large mode is never
# hidden merely because it overlaps a symmetry direction.
PHASE_ABS_MAX = 1.0e-2
TRANSLATION_ABS_MAX = 2.0e-2

PHYSICAL_GROWTH_MAX = 1.0e-5

CHEB_GRID_GROWTH_SPREAD_MAX = 5.0e-6

PROJECTED_K_MIN = 1.0e-7

D3CR_L1_REQUIRED = True

X_MATCH = 500.0
X0 = 1.0e-5


def require(path: Path) -> None:
    if not path.is_file():
        raise RuntimeError(
            f"Missing required upstream file: {path}"
        )


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(
        name,
        path,
    )

    if spec is None or spec.loader is None:
        raise RuntimeError(
            f"Cannot import {path}"
        )

    module = importlib.util.module_from_spec(
        spec
    )

    sys.modules[name] = module
    spec.loader.exec_module(module)

    return module


def builtin(value: Any):
    if isinstance(
        value,
        (
            complex,
            np.complexfloating,
        ),
    ):
        return {
            "real":
                float(
                    np.real(
                        value
                    )
                ),

            "imag":
                float(
                    np.imag(
                        value
                    )
                ),
        }

    if isinstance(value, np.generic):
        return value.item()

    if isinstance(value, np.ndarray):
        return value.tolist()

    if isinstance(value, dict):
        return {
            str(k): builtin(v)
            for k, v in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [
            builtin(v)
            for v in value
        ]

    return value


def W(q):
    q = np.asarray(
        q,
        dtype=float,
    )

    return (
        0.5
        * np.log1p(
            q**2
        )
    )


def activation_fraction(a):
    a = np.asarray(
        a,
        dtype=float,
    )

    return (
        1.0
        - np.exp(
            -0.5
            * a**2
        )
    )


def activation_fp(a):
    a = np.asarray(
        a,
        dtype=float,
    )

    return (
        a
        * np.exp(
            -0.5
            * a**2
        )
    )


def activation_fpp(a):
    a = np.asarray(
        a,
        dtype=float,
    )

    return (
        (
            1.0
            - a**2
        )
        * np.exp(
            -0.5
            * a**2
        )
    )


def overlap(
    vector,
    mode,
) -> float:
    vector = np.asarray(
        vector,
        dtype=complex,
    )

    mode = np.asarray(
        mode,
        dtype=complex,
    )

    nv = np.linalg.norm(
        vector
    )

    nm = np.linalg.norm(
        mode
    )

    if (
        nv <= 1.0e-300
        or
        nm <= 1.0e-300
    ):
        return 0.0

    return float(
        abs(
            np.vdot(
                mode,
                vector,
            )
        )
        /
        (
            nv
            * nm
        )
    )


def chebyshev_radial(
    N: int,
    rmax: float,
):
    """
    Chebyshev-Lobatto differentiation on [0,rmax].

    x_j = cos(pi j/N)
    r   = rmax(1-x)/2

    The reduced radial perturbations obey Dirichlet conditions at both
    endpoints, so only interior nodes are retained.
    """

    j = np.arange(
        N + 1,
        dtype=float,
    )

    x = np.cos(
        math.pi
        * j
        / N
    )

    c = np.ones(
        N + 1,
        dtype=float,
    )

    c[
        0
    ] = 2.0

    c[
        -1
    ] = 2.0

    c *= (
        -1.0
    )**np.arange(
        N + 1
    )

    X = np.tile(
        x,
        (
            N + 1,
            1,
        ),
    ).T

    dX = (
        X
        - X.T
    )

    D = (
        np.outer(
            c,
            1.0 / c,
        )
        /
        (
            dX
            + np.eye(
                N + 1
            )
        )
    )

    D -= np.diag(
        np.sum(
            D,
            axis=1,
        )
    )

    # r = R(1-x)/2.
    Dr = (
        -2.0
        / rmax
        * D
    )

    D2r = (
        Dr
        @ Dr
    )

    r = (
        0.5
        * rmax
        * (
            1.0
            - x
        )
    )

    interior = np.arange(
        1,
        N,
        dtype=int,
    )

    return (
        r[
            interior
        ],
        Dr[
            np.ix_(
                interior,
                interior,
            )
        ],
        D2r[
            np.ix_(
                interior,
                interior,
            )
        ],
    )


def relative_spread(
    values,
):
    values = np.asarray(
        values,
        dtype=float,
    )

    return float(
        (
            np.max(
                values
            )
            - np.min(
                values
            )
        )
        /
        max(
            abs(
                float(
                    np.mean(
                        values
                    )
                )
            ),
            1.0e-300,
        )
    )


def main() -> None:
    print(
        "=== 031D3C-R2 INDEPENDENT CHEBYSHEV DENSE SPECTRUM ===",
        flush=True,
    )

    print(
        "SPARSE_ARPACK_USED=NO",
        flush=True,
    )

    print(
        "RADIAL_DISCRETIZATION=CHEBYSHEV_LOBATTO",
        flush=True,
    )

    print(
        "EIGENSOLVER=DENSE_SCIPY_LINALG_EIG",
        flush=True,
    )

    print(
        "RECOMPUTED_L=0,1,2",
        flush=True,
    )

    print(
        "INHERITED_L=3_TO_8",
        flush=True,
    )

    print(
        "D96_STYLE_TRANSLATION_ORTHOGONAL_STIFFNESS=YES",
        flush=True,
    )

    print(
        "PRACTICAL_DEVICE=NO",
        flush=True,
    )

    for path in (
        QBALL_SOURCE,
        D3A_SOURCE,
        D3B_SUMMARY,
        D3C_SUMMARY,
        D3CR_SUMMARY,
        D3AR_SUMMARY,
        ROBUST_SUMMARY,
    ):
        require(path)

    d3b = json.loads(
        D3B_SUMMARY.read_text()
    )

    d3c = json.loads(
        D3C_SUMMARY.read_text()
    )

    d3cr = json.loads(
        D3CR_SUMMARY.read_text()
    )

    d3ar = json.loads(
        D3AR_SUMMARY.read_text()
    )

    robust = json.loads(
        ROBUST_SUMMARY.read_text()
    )

    if not str(
        d3b[
            "classification"
        ]
    ).startswith(
        "GREEN_D3B"
    ):
        raise RuntimeError(
            "D3B is not GREEN"
        )

    if not bool(
        d3c[
            "source_stability"
        ][
            "inherited_green"
        ]
    ):
        raise RuntimeError(
            "Inherited X+phi stability is not GREEN"
        )

    if not bool(
        d3c[
            "activation_branch"
        ][
            "slope_pass"
        ]
    ):
        raise RuntimeError(
            "Activation branch slope failed"
        )

    if D3CR_L1_REQUIRED and not bool(
        d3cr[
            "decision"
        ][
            "l1_continuum_pass"
        ]
    ):
        raise RuntimeError(
            "D3C-R finite-difference l1 continuum gate did not pass"
        )

    candidate = robust[
        "candidate"
    ]

    quadrature = robust[
        "quadrature"
    ][
        "high_order_result"
    ]

    primary = d3ar[
        "primary"
    ]

    omega_x = float(
        d3b[
            "domain_rows"
        ][
            -1
        ][
            "omega_x"
        ]
    )

    omega_y = float(
        d3b[
            "domain_rows"
        ][
            -1
        ][
            "omega_y"
        ]
    )

    epsilon = float(
        candidate[
            "epsilon"
        ]
    )

    chi = float(
        candidate[
            "chi"
        ]
    )

    F_gev = float(
        quadrature[
            "F_gev"
        ]
    )

    mu = float(
        primary[
            "mu_mA_over_mX"
        ]
    )

    rho_y = (
        float(
            primary[
                "V_required_eV"
            ]
        )
        /
        (
            F_gev
            * 1.0e9
        )
    )**2

    sqrt_rho = math.sqrt(
        rho_y
    )

    qmod = load_module(
        "qball031d3cr2",
        QBALL_SOURCE,
    )

    d3a = load_module(
        "d3a031d3cr2",
        D3A_SOURCE,
    )

    old_xmatch = float(
        qmod.X_MATCH
    )

    try:
        # ----------------------------------------------------------
        # Reconstruct the essentially exact saturated-product background.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE A: BACKGROUND RECONSTRUCTION ===",
            flush=True,
        )

        qmod.X_MATCH = X_MATCH

        source_seed = (
            qmod.solve_uncoupled_qball(
                omega_x
            )
        )

        if source_seed is None:
            raise RuntimeError(
                "Failed X seed"
            )

        source = qmod.solve_coupled(
            source_seed,
            omega_x,
            epsilon,
            chi,
            previous=None,
        )

        if source is None:
            raise RuntimeError(
                "Failed X+phi source"
            )

        boundary = source.sol(
            X_MATCH
        )

        y_boundary = float(
            boundary[
                0
            ]
        )

        u_boundary = float(
            boundary[
                2
            ]
        )

        kx_tail = math.sqrt(
            1.0
            - omega_x**2
        )

        def source_fields(r):
            r = np.asarray(
                r,
                dtype=float,
            )

            y = np.empty_like(
                r
            )

            yp = np.empty_like(
                r
            )

            u = np.empty_like(
                r
            )

            up = np.empty_like(
                r
            )

            inside = (
                r <= X_MATCH
            )

            if np.any(
                inside
            ):
                state = source.sol(
                    np.maximum(
                        r[
                            inside
                        ],
                        X0,
                    )
                )

                y[
                    inside
                ] = state[
                    0
                ]

                yp[
                    inside
                ] = state[
                    1
                ]

                u[
                    inside
                ] = state[
                    2
                ]

                up[
                    inside
                ] = state[
                    3
                ]

            outside = (
                ~inside
            )

            if np.any(
                outside
            ):
                ro = r[
                    outside
                ]

                yo = (
                    y_boundary
                    * X_MATCH
                    / ro
                    * np.exp(
                        -kx_tail
                        * (
                            ro
                            - X_MATCH
                        )
                    )
                )

                uo = (
                    u_boundary
                    * X_MATCH
                    / ro
                    * np.exp(
                        -epsilon
                        * (
                            ro
                            - X_MATCH
                        )
                    )
                )

                y[
                    outside
                ] = yo

                yp[
                    outside
                ] = (
                    -kx_tail
                    -1.0 / ro
                ) * yo

                u[
                    outside
                ] = uo

                up[
                    outside
                ] = (
                    -epsilon
                    -1.0 / ro
                ) * uo

            return (
                y,
                yp,
                u,
                up,
            )

        qmod.X_MATCH = 80.0

        activation = (
            qmod.solve_uncoupled_qball(
                omega_y
            )
        )

        if activation is None:
            raise RuntimeError(
                "Failed activation Q-ball"
            )

        def activation_fields(r):
            rho = (
                mu
                * np.asarray(
                    r,
                    dtype=float,
                )
            )

            a, ap_rho = (
                d3a.extended_profile(
                    activation,
                    omega_y,
                    rho,
                )
            )

            return (
                np.asarray(
                    a,
                    dtype=float,
                ),

                mu
                * np.asarray(
                    ap_rho,
                    dtype=float,
                ),
            )

        print(
            f"SOURCE_U0="
            f"{float(source.sol(X0)[2]):.15e}",
            flush=True,
        )

        print(
            f"ACTIVATION_A0="
            f"{float(activation.sol(X0)[0]):.15e}",
            flush=True,
        )

        # ----------------------------------------------------------
        # Build one Chebyshev quadratic problem.
        # ----------------------------------------------------------

        def build_problem(
            ell: int,
            N: int,
            rmax: float,
        ):
            r, Dr, D2r = (
                chebyshev_radial(
                    N,
                    rmax,
                )
            )

            n = len(
                r
            )

            y, yp, u, up = (
                source_fields(
                    r
                )
            )

            a, ap = (
                activation_fields(
                    r
                )
            )

            f = activation_fraction(
                a
            )

            fp = activation_fp(
                a
            )

            fpp = activation_fpp(
                a
            )

            A = np.exp(
                -0.5
                * f
                * u**2
            )

            wx = W(
                y
            )

            T = (
                -D2r
                + np.diag(
                    ell
                    * (
                        ell
                        + 1.0
                    )
                    / r**2
                )
            )

            v_xamp = (
                A
                * (
                    1.0
                    - y**2
                )
                / (
                    1.0
                    + y**2
                )**2
                - omega_x**2
            )

            v_xphase = (
                A
                / (
                    1.0
                    + y**2
                )
                - omega_x**2
            )

            v_u = (
                epsilon**2
                + chi**2
                * A
                * wx
                * (
                    f**2
                    * u**2
                    - f
                )
            )

            v_yamp = (
                mu**2
                * (
                    (
                        1.0
                        - a**2
                    )
                    / (
                        1.0
                        + a**2
                    )**2
                    - omega_y**2
                )
                -
                0.5
                / rho_y
                * u**2
                * A
                * wx
                * (
                    fpp
                    -0.5
                    * u**2
                    * fp**2
                )
            )

            v_yphase = (
                mu**2
                * (
                    1.0
                    / (
                        1.0
                        + a**2
                    )
                    - omega_y**2
                )
                -
                0.5
                / rho_y
                * u**2
                * A
                * wx
                * np.exp(
                    -0.5
                    * a**2
                )
            )

            c_xu = (
                -chi
                * f
                * u
                * A
                * y
                / (
                    1.0
                    + y**2
                )
            )

            c_xa = (
                -0.5
                / sqrt_rho
                * u**2
                * fp
                * A
                * y
                / (
                    1.0
                    + y**2
                )
            )

            c_ua = (
                -chi
                / sqrt_rho
                * u
                * A
                * wx
                * fp
                * (
                    1.0
                    -0.5
                    * f
                    * u**2
                )
            )

            Z = np.zeros(
                (
                    n,
                    n,
                ),
                dtype=float,
            )

            I = np.eye(
                n
            )

            Lxa = (
                T
                + np.diag(
                    v_xamp
                )
            )

            Lxp = (
                T
                + np.diag(
                    v_xphase
                )
            )

            Lu = (
                T
                + np.diag(
                    v_u
                )
            )

            Lya = (
                T
                + np.diag(
                    v_yamp
                )
            )

            Lyp = (
                T
                + np.diag(
                    v_yphase
                )
            )

            CXU = np.diag(
                c_xu
            )

            CXA = np.diag(
                c_xa
            )

            CUA = np.diag(
                c_ua
            )

            K = np.block(
                [
                    [
                        Lxa,
                        Z,
                        CXU,
                        CXA,
                        Z,
                    ],
                    [
                        Z,
                        Lxp,
                        Z,
                        Z,
                        Z,
                    ],
                    [
                        CXU,
                        Z,
                        Lu,
                        CUA,
                        Z,
                    ],
                    [
                        CXA,
                        Z,
                        CUA,
                        Lya,
                        Z,
                    ],
                    [
                        Z,
                        Z,
                        Z,
                        Z,
                        Lyp,
                    ],
                ]
            )

            G = np.block(
                [
                    [
                        Z,
                        2.0
                        * omega_x
                        * I,
                        Z,
                        Z,
                        Z,
                    ],
                    [
                        -2.0
                        * omega_x
                        * I,
                        Z,
                        Z,
                        Z,
                        Z,
                    ],
                    [
                        Z,
                        Z,
                        Z,
                        Z,
                        Z,
                    ],
                    [
                        Z,
                        Z,
                        Z,
                        Z,
                        2.0
                        * mu
                        * omega_y
                        * I,
                    ],
                    [
                        Z,
                        Z,
                        Z,
                        -2.0
                        * mu
                        * omega_y
                        * I,
                        Z,
                    ],
                ]
            )

            nq = (
                5
                * n
            )

            companion = np.block(
                [
                    [
                        np.zeros(
                            (
                                nq,
                                nq,
                            )
                        ),
                        np.eye(
                            nq
                        ),
                    ],
                    [
                        -K,
                        -G,
                    ],
                ]
            )

            phase_x = np.zeros(
                nq
            )

            phase_y = np.zeros(
                nq
            )

            source_translation = np.zeros(
                nq
            )

            activation_translation = np.zeros(
                nq
            )

            phase_x[
                n:
                2 * n
            ] = (
                r
                * y
            )

            phase_y[
                4 * n:
                5 * n
            ] = (
                r
                * sqrt_rho
                * a
            )

            source_translation[
                0:n
            ] = (
                r
                * yp
            )

            source_translation[
                2 * n:
                3 * n
            ] = (
                r
                * up
                / chi
            )

            activation_translation[
                3 * n:
                4 * n
            ] = (
                r
                * sqrt_rho
                * ap
            )

            common_translation = (
                source_translation
                + activation_translation
            )

            return {
                "r":
                    r,

                "n":
                    n,

                "K":
                    K,

                "G":
                    G,

                "companion":
                    companion,

                "phase_x":
                    phase_x,

                "phase_y":
                    phase_y,

                "common_translation":
                    common_translation,
            }

        def dense_case(
            ell: int,
            N: int,
            rmax: float,
        ):
            print(
                f"START_DENSE "
                f"L={ell} "
                f"N={N} "
                f"RMAX={rmax:.1f}",
                flush=True,
            )

            problem = build_problem(
                ell,
                N,
                rmax,
            )

            companion = problem[
                "companion"
            ]

            nq = (
                5
                * problem[
                    "n"
                ]
            )

            # Complete spectrum + right eigenvectors.
            values, vectors = eig(
                companion,
                left=False,
                right=True,
                overwrite_a=True,
                check_finite=False,
            )

            modes = []

            for index in range(
                len(
                    values
                )
            ):
                value = complex(
                    values[
                        index
                    ]
                )

                position = vectors[
                    :nq,
                    index
                ]

                px = overlap(
                    position,
                    problem[
                        "phase_x"
                    ],
                )

                py = overlap(
                    position,
                    problem[
                        "phase_y"
                    ],
                )

                ct = overlap(
                    position,
                    problem[
                        "common_translation"
                    ],
                )

                symmetry = False
                symmetry_name = ""

                if (
                    ell == 0
                    and
                    abs(
                        value
                    )
                    <= PHASE_ABS_MAX
                    and
                    max(
                        px,
                        py,
                    )
                    >= PHASE_OVERLAP_MIN
                ):
                    symmetry = True
                    symmetry_name = "U1_PHASE"

                if (
                    ell == 1
                    and
                    abs(
                        value
                    )
                    <= TRANSLATION_ABS_MAX
                    and
                    ct
                    >= TRANSLATION_OVERLAP_MIN
                ):
                    symmetry = True
                    symmetry_name = "COMMON_TRANSLATION"

                modes.append(
                    {
                        "real":
                            value.real,

                        "imag":
                            value.imag,

                        "abs":
                            abs(
                                value
                            ),

                        "phase_x_overlap":
                            px,

                        "phase_y_overlap":
                            py,

                        "translation_overlap":
                            ct,

                        "symmetry":
                            symmetry,

                        "symmetry_name":
                            symmetry_name,
                    }
                )

            physical = [
                mode
                for mode in modes
                if not mode[
                    "symmetry"
                ]
            ]

            max_physical_real = max(
                mode[
                    "real"
                ]
                for mode in physical
            )

            # Highest real part among modes with little translation overlap.
            low_translation_modes = [
                mode
                for mode in modes
                if mode[
                    "translation_overlap"
                ] < 0.80
            ]

            low_overlap_max_real = max(
                (
                    mode[
                        "real"
                    ]
                    for mode
                    in low_translation_modes
                ),
                default=math.nan,
            )

            if ell == 1:
                translation_mode = max(
                    modes,
                    key=lambda mode:
                        mode[
                            "translation_overlap"
                        ],
                )

                translation_overlap = float(
                    translation_mode[
                        "translation_overlap"
                    ]
                )

                translation_real = float(
                    translation_mode[
                        "real"
                    ]
                )

                translation_imag = float(
                    translation_mode[
                        "imag"
                    ]
                )

                # D96-style translation-orthogonal projected stiffness.
                t = np.asarray(
                    problem[
                        "common_translation"
                    ],
                    dtype=float,
                )

                t /= max(
                    np.linalg.norm(
                        t
                    ),
                    1.0e-300,
                )

                K = np.asarray(
                    problem[
                        "K"
                    ],
                    dtype=float,
                )

                P = (
                    np.eye(
                        nq
                    )
                    - np.outer(
                        t,
                        t,
                    )
                )

                # P K P contains an exact projected null vector t.
                # Lift only that one removed symmetry direction.
                stiffness_scale = max(
                    1.0,
                    float(
                        np.max(
                            np.abs(
                                np.diag(
                                    K
                                )
                            )
                        )
                    ),
                )

                Kproj = (
                    P
                    @ K
                    @ P
                    + stiffness_scale
                    * np.outer(
                        t,
                        t,
                    )
                )

                projected_eigs = eigh(
                    Kproj,
                    eigvals_only=True,
                    subset_by_index=(
                        0,
                        3,
                    ),
                    check_finite=False,
                )

                projected_k0 = float(
                    projected_eigs[
                        0
                    ]
                )

                translation_K_residual = float(
                    np.linalg.norm(
                        K
                        @ t
                    )
                    /
                    max(
                        np.linalg.norm(
                            K
                        )
                        * np.linalg.norm(
                            t
                        ),
                        1.0e-300,
                    )
                )

                del P
                del Kproj

            else:
                translation_overlap = math.nan
                translation_real = math.nan
                translation_imag = math.nan
                projected_k0 = math.nan
                translation_K_residual = math.nan

            row = {
                "ell":
                    ell,

                "N":
                    N,

                "rmax":
                    rmax,

                "interior_nodes":
                    problem[
                        "n"
                    ],

                "companion_dimension":
                    int(
                        companion.shape[
                            0
                        ]
                    ),

                "max_physical_real":
                    float(
                        max_physical_real
                    ),

                "low_translation_overlap_max_real":
                    float(
                        low_overlap_max_real
                    ),

                "translation_real":
                    translation_real,

                "translation_imag":
                    translation_imag,

                "translation_overlap":
                    translation_overlap,

                "projected_k0":
                    projected_k0,

                "translation_K_residual":
                    translation_K_residual,
            }

            print(
                f"DENSE_RESULT "
                f"L={ell} "
                f"N={N} "
                f"RMAX={rmax:.1f} "
                f"DIM={row['companion_dimension']} "
                f"MAX_PHYS_RE="
                f"{row['max_physical_real']:+.12e} "
                f"LOWOV_MAX_RE="
                f"{row['low_translation_overlap_max_real']:+.12e} "
                f"TRANS_RE="
                f"{row['translation_real']:+.12e} "
                f"TRANS_OV="
                f"{row['translation_overlap']:.9f} "
                f"KPROJ0="
                f"{row['projected_k0']:+.12e}",
                flush=True,
            )

            del values
            del vectors
            del companion
            del problem

            gc.collect()

            return row

        # ----------------------------------------------------------
        # Dense independent scans.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE B: CHEBYSHEV DENSE l=0,1,2 ===",
            flush=True,
        )

        rows = []

        for N in BASE_N_VALUES:
            for ell in (
                0,
                1,
                2,
            ):
                rows.append(
                    dense_case(
                        ell,
                        N,
                        RMAX,
                    )
                )

        print(
            "\n=== STAGE C: EXTRA l=1 RESOLUTION / DOMAIN ===",
            flush=True,
        )

        rows.append(
            dense_case(
                1,
                L1_EXTRA_N,
                RMAX,
            )
        )

        rows.append(
            dense_case(
                1,
                L1_DOMAIN_N,
                L1_DOMAIN_RMAX,
            )
        )

        # ----------------------------------------------------------
        # Independent decision.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE D: CROSS-DISCRETIZATION DECISION ===",
            flush=True,
        )

        main_rows = [
            row
            for row in rows
            if row[
                "rmax"
            ] == RMAX
        ]

        decisions = {}

        for ell in (
            0,
            1,
            2,
        ):
            ell_rows = [
                row
                for row in main_rows
                if row[
                    "ell"
                ] == ell
            ]

            growth = np.asarray(
                [
                    max(
                        row[
                            "max_physical_real"
                        ],
                        0.0,
                    )
                    for row
                    in ell_rows
                ],
                dtype=float,
            )

            worst = float(
                np.max(
                    growth
                )
            )

            spread = float(
                np.max(
                    growth
                )
                - np.min(
                    growth
                )
            )

            passed = bool(
                worst
                <= PHYSICAL_GROWTH_MAX
                and
                spread
                <= CHEB_GRID_GROWTH_SPREAD_MAX
            )

            decisions[
                ell
            ] = {
                "worst_real_growth":
                    worst,

                "growth_spread":
                    spread,

                "pass":
                    passed,
            }

            print(
                f"CHEB_L{ell}_WORST_REAL="
                f"{worst:.15e}",
                flush=True,
            )

            print(
                f"CHEB_L{ell}_GROWTH_SPREAD="
                f"{spread:.15e}",
                flush=True,
            )

            print(
                f"CHEB_L{ell}_PASS="
                f"{passed}",
                flush=True,
            )

        l1_rows = [
            row
            for row in main_rows
            if row[
                "ell"
            ] == 1
        ]

        minimum_translation_overlap = min(
            row[
                "translation_overlap"
            ]
            for row in l1_rows
        )

        minimum_projected_k = min(
            row[
                "projected_k0"
            ]
            for row in l1_rows
        )

        maximum_low_overlap_real = max(
            row[
                "low_translation_overlap_max_real"
            ]
            for row in l1_rows
        )

        domain_row = next(
            row
            for row in rows
            if (
                row[
                    "ell"
                ] == 1
                and
                row[
                    "rmax"
                ]
                == L1_DOMAIN_RMAX
            )
        )

        finest_main = next(
            row
            for row in rows
            if (
                row[
                    "ell"
                ] == 1
                and
                row[
                    "rmax"
                ]
                == RMAX
                and
                row[
                    "N"
                ]
                == L1_EXTRA_N
            )
        )

        domain_growth_difference = abs(
            max(
                domain_row[
                    "max_physical_real"
                ],
                0.0,
            )
            -
            max(
                finest_main[
                    "max_physical_real"
                ],
                0.0,
            )
        )

        projected_k_pass = bool(
            minimum_projected_k
            >= PROJECTED_K_MIN
        )

        translation_overlap_pass = bool(
            minimum_translation_overlap
            >= TRANSLATION_OVERLAP_MIN
        )

        low_overlap_pass = bool(
            maximum_low_overlap_real
            <= PHYSICAL_GROWTH_MAX
        )

        domain_pass = bool(
            domain_growth_difference
            <= CHEB_GRID_GROWTH_SPREAD_MAX
        )

        print(
            f"CHEB_L1_MIN_TRANSLATION_OVERLAP="
            f"{minimum_translation_overlap:.15e}",
            flush=True,
        )

        print(
            f"CHEB_L1_MIN_PROJECTED_K="
            f"{minimum_projected_k:.15e}",
            flush=True,
        )

        print(
            f"CHEB_L1_MAX_LOW_OVERLAP_REAL="
            f"{maximum_low_overlap_real:.15e}",
            flush=True,
        )

        print(
            f"CHEB_L1_DOMAIN_GROWTH_DIFFERENCE="
            f"{domain_growth_difference:.15e}",
            flush=True,
        )

        print(
            f"CHEB_TRANSLATION_OVERLAP_PASS="
            f"{translation_overlap_pass}",
            flush=True,
        )

        print(
            f"CHEB_TRANSLATION_PROJECTED_STIFFNESS_PASS="
            f"{projected_k_pass}",
            flush=True,
        )

        print(
            f"CHEB_LOW_OVERLAP_MODES_PASS="
            f"{low_overlap_pass}",
            flush=True,
        )

        print(
            f"CHEB_DOMAIN_PASS="
            f"{domain_pass}",
            flush=True,
        )

        inherited_l3_to_l8_rows = [
            row
            for row in d3c[
                "spectrum_rows"
            ]
            if int(
                row[
                    "ell"
                ]
            )
            >= 3
        ]

        inherited_l3_to_l8_complete = bool(
            inherited_l3_to_l8_rows
            and
            all(
                bool(
                    row[
                        "right_complete"
                    ]
                )
                for row
                in inherited_l3_to_l8_rows
            )
        )

        inherited_l3_to_l8_worst = max(
            float(
                row[
                    "max_physical_growth"
                ]
            )
            for row
            in inherited_l3_to_l8_rows
        )

        inherited_l3_to_l8_pass = bool(
            inherited_l3_to_l8_complete
            and
            inherited_l3_to_l8_worst
            <= PHYSICAL_GROWTH_MAX
        )

        print(
            f"INHERITED_L3_TO_L8_RIGHTMOST_COMPLETE="
            f"{inherited_l3_to_l8_complete}",
            flush=True,
        )

        print(
            f"INHERITED_L3_TO_L8_WORST_REAL="
            f"{inherited_l3_to_l8_worst:.15e}",
            flush=True,
        )

        print(
            f"INHERITED_L3_TO_L8_PASS="
            f"{inherited_l3_to_l8_pass}",
            flush=True,
        )

        finite_difference_l1_pass = bool(
            d3cr[
                "decision"
            ][
                "l1_continuum_pass"
            ]
        )

        independent_cheb_pass = bool(
            decisions[
                0
            ][
                "pass"
            ]
            and
            decisions[
                1
            ][
                "pass"
            ]
            and
            decisions[
                2
            ][
                "pass"
            ]
            and
            translation_overlap_pass
            and
            projected_k_pass
            and
            low_overlap_pass
            and
            domain_pass
        )

        full_linear_pass = bool(
            bool(
                d3c[
                    "source_stability"
                ][
                    "inherited_green"
                ]
            )
            and
            bool(
                d3c[
                    "activation_branch"
                ][
                    "slope_pass"
                ]
            )
            and
            bool(
                d3c[
                    "coupling"
                ][
                    "background_pass"
                ]
            )
            and
            bool(
                d3c[
                    "coupling"
                ][
                    "cross_preflight_pass"
                ]
            )
            and
            finite_difference_l1_pass
            and
            independent_cheb_pass
            and
            inherited_l3_to_l8_pass
        )

        print(
            f"FINITE_DIFFERENCE_L1_CONTINUUM_PASS="
            f"{finite_difference_l1_pass}",
            flush=True,
        )

        print(
            f"INDEPENDENT_CHEBYSHEV_L012_PASS="
            f"{independent_cheb_pass}",
            flush=True,
        )

        print(
            f"COUPLED_LINEAR_STABILITY_FINAL_PASS="
            f"{full_linear_pass}",
            flush=True,
        )

        # ----------------------------------------------------------
        # Final classification.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE E: FINAL 031D3C-R2 CLASSIFICATION ===",
            flush=True,
        )

        if full_linear_pass:
            classification = (
                "GREEN_D3CR2_COUPLED_LINEAR_STABILITY_"
                "THROUGH_L8_INDEPENDENT_CHEBYSHEV_DENSE_"
                "AND_TRANSLATION_PROJECTED_STIFFNESS_PASS"
            )

            next_action = (
                "031D3D_EXPLICIT_QY_RESERVOIR_TRANSFER_"
                "RESET_AND_RADIATION_GATE"
            )

        else:
            classification = (
                "YELLOW_OR_RED_D3CR2_INDEPENDENT_"
                "SPECTRAL_CLOSEOUT_FAILED"
            )

            next_action = (
                "DIAGNOSE_ONLY_FAILED_CHEBYSHEV_SUBGATE"
            )

        print(
            f"031D3CR2_CLASSIFICATION="
            f"{classification}",
            flush=True,
        )

        print(
            f"NEXT={next_action}",
            flush=True,
        )

        print(
            "TRUE_D3_INSTABILITY_ESTABLISHED="
            + str(
                (
                    not full_linear_pass
                )
                and
                any(
                    decisions[
                        ell
                    ][
                        "worst_real_growth"
                    ]
                    > PHYSICAL_GROWTH_MAX
                    for ell
                    in (
                        0,
                        1,
                        2,
                    )
                )
            ),
            flush=True,
        )

        print(
            "RIGHTMOST_ARPACK_REQUIRED_FOR_CLAIM=NO",
            flush=True,
        )

        print(
            "EXPLICIT_QY_TRANSFER_RESERVOIR_CLOSED=NO",
            flush=True,
        )

        print(
            "RESET_RADIATION_CLOSED=NO",
            flush=True,
        )

        print(
            "NONLINEAR_FRAGMENTATION_CLOSED=NO",
            flush=True,
        )

        print(
            "FULL_EINSTEIN_BACKREACTION_CLOSED=NO",
            flush=True,
        )

        print(
            "RADIATIVE_NATURALNESS_CLOSED=NO",
            flush=True,
        )

        print(
            "EMPIRICAL_CLOSURE=NO",
            flush=True,
        )

        print(
            "PRACTICAL_DEVICE=NO",
            flush=True,
        )

        summary = {
            "classification":
                classification,

            "next":
                next_action,

            "method": {
                "radial_discretization":
                    "Chebyshev-Lobatto",

                "eigensolver":
                    "complete dense scipy.linalg.eig",

                "sparse_ARPACK":
                    False,

                "recomputed_l":
                    [
                        0,
                        1,
                        2,
                    ],

                "inherited_l":
                    [
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                    ],
            },

            "rows":
                rows,

            "chebyshev_decisions":
                decisions,

            "l1": {
                "minimum_translation_overlap":
                    minimum_translation_overlap,

                "minimum_projected_k":
                    minimum_projected_k,

                "maximum_low_overlap_real":
                    maximum_low_overlap_real,

                "domain_growth_difference":
                    domain_growth_difference,

                "translation_overlap_pass":
                    translation_overlap_pass,

                "projected_stiffness_pass":
                    projected_k_pass,

                "low_overlap_pass":
                    low_overlap_pass,

                "domain_pass":
                    domain_pass,
            },

            "inherited": {
                "finite_difference_l1_continuum_pass":
                    finite_difference_l1_pass,

                "l3_to_l8_rightmost_complete":
                    inherited_l3_to_l8_complete,

                "l3_to_l8_worst_real":
                    inherited_l3_to_l8_worst,

                "l3_to_l8_pass":
                    inherited_l3_to_l8_pass,
            },

            "decision": {
                "independent_chebyshev_l012_pass":
                    independent_cheb_pass,

                "full_coupled_linear_stability_pass":
                    full_linear_pass,
            },

            "claim_limits": [
                (
                    "GREEN establishes coupled-linear stability "
                    "through l=8 only in the declared flat-space "
                    "effective X/phi/Y theory."
                ),
                (
                    "l=0,1,2 are independently reconstructed using "
                    "Chebyshev collocation and complete dense "
                    "diagonalization rather than finite differences "
                    "and sparse ARPACK."
                ),
                (
                    "l=3..8 are inherited from D3C because their "
                    "rightmost searches completed at both declared grids."
                ),
                (
                    "The exact common l=1 translation is removed only "
                    "for the projected-stiffness diagnostic; relative "
                    "translation remains physical."
                ),
                (
                    "The explicit QY reservoir/transfer/reset mechanism "
                    "and switching radiation remain open."
                ),
                (
                    "Nonlinear fragmentation, Einstein backreaction, "
                    "radiative naturalness and empirical closure remain open."
                ),
                (
                    "No practical device is established."
                ),
            ],
        }

        OUT_JSON.write_text(
            json.dumps(
                builtin(
                    summary
                ),
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )

        fields = sorted(
            {
                key
                for row in rows
                for key in row
            }
        )

        with OUT_CSV.open(
            "w",
            newline="",
        ) as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=fields,
            )

            writer.writeheader()
            writer.writerows(
                rows
            )

        print(
            f"SUMMARY_JSON={OUT_JSON}",
            flush=True,
        )

        print(
            f"SPECTRUM_CSV={OUT_CSV}",
            flush=True,
        )

    finally:
        qmod.X_MATCH = old_xmatch


if __name__ == "__main__":
    main()
