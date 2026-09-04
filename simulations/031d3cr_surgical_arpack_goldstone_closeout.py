"""
031D3C-R
========

Surgical numerical closeout of the 031D3C coupled-linear stability gate.

Why this exists
---------------

031D3C did NOT establish a physical instability.

It found:

* X+phi inherited stability GREEN;
* Y Q-ball dQ/dOmega < 0;
* new D3 cross-Hessian ~1.6e-18;
* l=0,2,...,8 near-zero spectra essentially oscillatory;
* common l=1 translation Goldstone identified;
* apparent non-symmetry l=1 growth:
      h=.50   -> 4.1630e-5
      h=.375  -> 3.1235e-5
      h=.25   -> 2.0846e-5
  which scales approximately linearly with h;
* Rmax=600 -> 800 at h=.5 leaves the value unchanged;
* certification failed because several expensive which="LR" ARPACK
  requests were incomplete.

The aborted first repair was too expensive and risked overwriting D3C
artifacts.

This version is intentionally narrow:

1. Reuse all completed D3C spectrum results.
2. Rerun ONLY rightmost searches which were incomplete in the
   l=0,1,2 / Rmax=600 / h={.5,.375} closeout region.
3. Request far fewer rightmost eigenvalues.
4. Use a tolerance appropriate to a 1e-4 physical-growth gate.
5. Add ONE new l=1 near-zero solve at h=.1875.
6. Fit the relative-translation growth to h->0.
7. Independently measure analytic translation-vector residuals.
8. Do not repeat the switching ledger or the l=3..8 spectrum.
9. Write ONLY 031d3cr_* artifacts.

A GREEN result is a numerical closeout of coupled-linear stability
within the declared flat-space effective X/phi/Y theory through l=8.

It is not nonlinear, Einstein, EFT, empirical, switching-reservoir,
or practical-device certification.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np

from scipy.sparse import (
    bmat,
    csr_matrix,
    diags,
    identity,
)

from scipy.sparse.linalg import (
    ArpackNoConvergence,
    eigs,
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

D3C_SUMMARY = (
    DATA / "031d3c_activation_stability_switching_summary.json"
)

D3B_SUMMARY = (
    DATA / "031d3b_full_coupled_activation_summary.json"
)

D3AR_SUMMARY = (
    DATA / "031d3ar_metric_eft_payload_summary.json"
)

ROBUST_SUMMARY = (
    DATA / "031c96_operating_margin_robustness_summary.json"
)

OUT_JSON = (
    DATA / "031d3cr_surgical_closeout_summary.json"
)

OUT_CSV = (
    DATA / "031d3cr_rightmost_repair.csv"
)


# ---------------------------------------------------------------------------
# Numerical policy
# ---------------------------------------------------------------------------

RMAX_REPAIR = 600.0

REPAIR_H_VALUES = (
    0.50,
    0.375,
)

NEW_L1_H = 0.1875

L1_INHERITED_H = (
    0.50,
    0.375,
    0.25,
)

RIGHT_TOL = 2.0e-6
RIGHT_MAXITER = 10_000

NEAR_TOL = 2.0e-8
NEAR_MAXITER = 12_000

NEAR_K = 12

# For l=1 we need enough rightmost vectors to see past the common
# translation Goldstone artifact.
RIGHT_K_BY_L = {
    0: 3,
    1: 4,
    2: 2,
}

GROWTH_TOL = 1.0e-4

PHASE_OVERLAP_MIN = 0.95
COMMON_TRANSLATION_OVERLAP_MIN = 0.97

# Continuum behavior expected from the existing D3C sequence.
L1_POWER_MIN = 0.75
L1_POWER_MAX = 1.25

L1_LINEAR_INTERCEPT_MAX = 5.0e-6
L1_QUADRATIC_INTERCEPT_MAX = 5.0e-6

# The new fine-grid magnitude must continue falling.
L1_FINE_MONOTONIC_FACTOR = 0.95

X_SOURCE_MATCH = 500.0
X0 = 1.0e-5


def require(path: Path) -> None:
    if not path.is_file():
        raise RuntimeError(
            f"Missing required file: {path}"
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
    if isinstance(value, np.generic):
        return value.item()

    if isinstance(value, np.ndarray):
        return value.tolist()

    if isinstance(value, complex):
        return {
            "real": float(value.real),
            "imag": float(value.imag),
        }

    if isinstance(value, dict):
        return {
            str(key): builtin(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [
            builtin(item)
            for item in value
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


def f_activation(a):
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


def fp_activation(a):
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


def fpp_activation(a):
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


def overlap(vector, mode) -> float:
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


def deterministic_v0(size: int) -> np.ndarray:
    index = np.arange(
        size,
        dtype=float,
    )

    vector = (
        np.sin(
            0.173
            * index
        )
        +
        0.37
        * np.cos(
            0.071
            * index
        )
    )

    norm = np.linalg.norm(
        vector
    )

    return (
        vector
        / norm
    )


def rightmost_eigs(
    matrix,
    *,
    k: int,
):
    """
    Intentionally modest rightmost solve.

    Complete=False is numerical incompleteness, not instability.
    """

    try:
        values, vectors = eigs(
            matrix,
            k=k,
            which="LR",
            tol=RIGHT_TOL,
            maxiter=RIGHT_MAXITER,
            ncv=max(
                28,
                5 * k + 12,
            ),
            v0=deterministic_v0(
                matrix.shape[0]
            ),
        )

        return (
            np.asarray(
                values
            ),
            np.asarray(
                vectors
            ),
            True,
        )

    except ArpackNoConvergence as exc:
        values = exc.eigenvalues
        vectors = exc.eigenvectors

        if (
            values is None
            or
            vectors is None
        ):
            return (
                np.array(
                    [],
                    dtype=complex,
                ),
                np.empty(
                    (
                        matrix.shape[0],
                        0,
                    ),
                    dtype=complex,
                ),
                False,
            )

        return (
            np.asarray(
                values
            ),
            np.asarray(
                vectors
            ),
            False,
        )


def near_zero_eigs(
    matrix,
    *,
    k: int,
):
    try:
        values, vectors = eigs(
            matrix,
            k=k,
            sigma=1.0e-6,
            which="LM",
            tol=NEAR_TOL,
            maxiter=NEAR_MAXITER,
            ncv=max(
                40,
                3 * k + 8,
            ),
            v0=deterministic_v0(
                matrix.shape[0]
            ),
        )

        return (
            np.asarray(
                values
            ),
            np.asarray(
                vectors
            ),
            True,
        )

    except ArpackNoConvergence as exc:
        values = exc.eigenvalues
        vectors = exc.eigenvectors

        if (
            values is None
            or
            vectors is None
        ):
            return (
                np.array(
                    [],
                    dtype=complex,
                ),
                np.empty(
                    (
                        matrix.shape[0],
                        0,
                    ),
                    dtype=complex,
                ),
                False,
            )

        return (
            np.asarray(
                values
            ),
            np.asarray(
                vectors
            ),
            False,
        )


def main() -> None:
    print(
        "=== 031D3C-R SURGICAL ARPACK/GOLDSTONE CLOSEOUT ===",
        flush=True,
    )

    print(
        "BROAD_L0_TO_L8_RERUN=NO",
        flush=True,
    )

    print(
        "SWITCHING_LEDGER_RERUN=NO",
        flush=True,
    )

    print(
        "ONLY_PREVIOUSLY_INCOMPLETE_RIGHTMOST_CASES=YES",
        flush=True,
    )

    print(
        "NEW_L1_FINE_GRID_H=0.1875",
        flush=True,
    )

    print(
        "ORIGINAL_D3C_ARTIFACTS_OVERWRITTEN=NO",
        flush=True,
    )

    print(
        "PRACTICAL_DEVICE=NO",
        flush=True,
    )

    for path in (
        QBALL_SOURCE,
        D3A_SOURCE,
        D3C_SUMMARY,
        D3B_SUMMARY,
        D3AR_SUMMARY,
        ROBUST_SUMMARY,
    ):
        require(path)

    d3c = json.loads(
        D3C_SUMMARY.read_text()
    )

    d3b = json.loads(
        D3B_SUMMARY.read_text()
    )

    d3ar = json.loads(
        D3AR_SUMMARY.read_text()
    )

    robust = json.loads(
        ROBUST_SUMMARY.read_text()
    )

    if not str(
        d3b.get(
            "classification",
            "",
        )
    ).startswith(
        "GREEN_D3B"
    ):
        raise RuntimeError(
            "D3B microscopic field is not GREEN"
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
            "Activation branch slope failed upstream"
        )

    if not bool(
        d3c[
            "coupling"
        ][
            "background_pass"
        ]
    ):
        raise RuntimeError(
            "D3 background coupling defect failed upstream"
        )

    if not bool(
        d3c[
            "coupling"
        ][
            "cross_preflight_pass"
        ]
    ):
        raise RuntimeError(
            "D3 cross-Hessian preflight failed upstream"
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

    print(
        f"OMEGA_X={omega_x:.15e}",
        flush=True,
    )

    print(
        f"OMEGA_Y={omega_y:.15e}",
        flush=True,
    )

    print(
        f"MU={mu:.15e}",
        flush=True,
    )

    print(
        f"RHO_Y={rho_y:.15e}",
        flush=True,
    )

    qmod = load_module(
        "qball031d3cr",
        QBALL_SOURCE,
    )

    d3a = load_module(
        "d3a031d3cr",
        D3A_SOURCE,
    )

    old_xmatch = float(
        qmod.X_MATCH
    )

    try:
        # ----------------------------------------------------------
        # A — reconstruct backgrounds once.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE A: RECONSTRUCT BACKGROUNDS ===",
            flush=True,
        )

        qmod.X_MATCH = X_SOURCE_MATCH

        source_seed = (
            qmod.solve_uncoupled_qball(
                omega_x
            )
        )

        if source_seed is None:
            raise RuntimeError(
                "Failed long-domain source seed"
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
                "Failed long-domain X+phi reconstruction"
            )

        source_boundary = source.sol(
            X_SOURCE_MATCH
        )

        y500 = float(
            source_boundary[
                0
            ]
        )

        u500 = float(
            source_boundary[
                2
            ]
        )

        kx = math.sqrt(
            1.0
            - omega_x**2
        )

        def source_fields(x):
            x = np.asarray(
                x,
                dtype=float,
            )

            y = np.empty_like(
                x
            )

            yp = np.empty_like(
                x
            )

            u = np.empty_like(
                x
            )

            up = np.empty_like(
                x
            )

            inside = (
                x <= X_SOURCE_MATCH
            )

            if np.any(
                inside
            ):
                state = source.sol(
                    np.maximum(
                        x[
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
                xo = x[
                    outside
                ]

                yo = (
                    y500
                    * X_SOURCE_MATCH
                    / xo
                    * np.exp(
                        -kx
                        * (
                            xo
                            - X_SOURCE_MATCH
                        )
                    )
                )

                uo = (
                    u500
                    * X_SOURCE_MATCH
                    / xo
                    * np.exp(
                        -epsilon
                        * (
                            xo
                            - X_SOURCE_MATCH
                        )
                    )
                )

                y[
                    outside
                ] = yo

                yp[
                    outside
                ] = (
                    -kx
                    -1.0 / xo
                ) * yo

                u[
                    outside
                ] = uo

                up[
                    outside
                ] = (
                    -epsilon
                    -1.0 / xo
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
                "Failed activation background"
            )

        def activation_fields(x):
            rho = (
                mu
                * np.asarray(
                    x,
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
        # Matrix builder.
        # ----------------------------------------------------------

        def build_case(
            rmax: float,
            h_target: float,
            ell: int,
        ):
            cells = int(
                round(
                    rmax
                    / h_target
                )
            )

            h = (
                rmax
                / cells
            )

            r = (
                h
                * np.arange(
                    1,
                    cells,
                    dtype=float,
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

            f = f_activation(
                a
            )

            fp = fp_activation(
                a
            )

            fpp = fpp_activation(
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

            centrifugal = (
                ell
                * (
                    ell
                    + 1.0
                )
                / r**2
            )

            main = (
                2.0
                / h**2
                + centrifugal
            )

            off = (
                -np.ones(
                    n - 1
                )
                / h**2
            )

            T = diags(
                (
                    off,
                    main,
                    off,
                ),
                offsets=(
                    -1,
                    0,
                    1,
                ),
                format="csr",
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

            Z = csr_matrix(
                (
                    n,
                    n,
                )
            )

            I = identity(
                n,
                format="csr",
            )

            Lxa = (
                T
                + diags(
                    v_xamp,
                    format="csr",
                )
            )

            Lxp = (
                T
                + diags(
                    v_xphase,
                    format="csr",
                )
            )

            Lu = (
                T
                + diags(
                    v_u,
                    format="csr",
                )
            )

            Lya = (
                T
                + diags(
                    v_yamp,
                    format="csr",
                )
            )

            Lyp = (
                T
                + diags(
                    v_yphase,
                    format="csr",
                )
            )

            CXU = diags(
                c_xu,
                format="csr",
            )

            CXA = diags(
                c_xa,
                format="csr",
            )

            CUA = diags(
                c_ua,
                format="csr",
            )

            K = bmat(
                (
                    (
                        Lxa,
                        Z,
                        CXU,
                        CXA,
                        Z,
                    ),
                    (
                        Z,
                        Lxp,
                        Z,
                        Z,
                        Z,
                    ),
                    (
                        CXU,
                        Z,
                        Lu,
                        CUA,
                        Z,
                    ),
                    (
                        CXA,
                        Z,
                        CUA,
                        Lya,
                        Z,
                    ),
                    (
                        Z,
                        Z,
                        Z,
                        Z,
                        Lyp,
                    ),
                ),
                format="csr",
            )

            G = bmat(
                (
                    (
                        Z,
                        2.0
                        * omega_x
                        * I,
                        Z,
                        Z,
                        Z,
                    ),
                    (
                        -2.0
                        * omega_x
                        * I,
                        Z,
                        Z,
                        Z,
                        Z,
                    ),
                    (
                        Z,
                        Z,
                        Z,
                        Z,
                        Z,
                    ),
                    (
                        Z,
                        Z,
                        Z,
                        Z,
                        2.0
                        * mu
                        * omega_y
                        * I,
                    ),
                    (
                        Z,
                        Z,
                        Z,
                        -2.0
                        * mu
                        * omega_y
                        * I,
                        Z,
                    ),
                ),
                format="csr",
            )

            nq = (
                5
                * n
            )

            Zq = csr_matrix(
                (
                    nq,
                    nq,
                )
            )

            Iq = identity(
                nq,
                format="csr",
            )

            companion = bmat(
                (
                    (
                        Zq,
                        Iq,
                    ),
                    (
                        -K,
                        -G,
                    ),
                ),
                format="csr",
            )

            phase_x = np.zeros(
                nq,
                dtype=float,
            )

            phase_y = np.zeros(
                nq,
                dtype=float,
            )

            source_translation = np.zeros(
                nq,
                dtype=float,
            )

            activation_translation = np.zeros(
                nq,
                dtype=float,
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

            common_norm2 = float(
                np.dot(
                    common_translation,
                    common_translation,
                )
            )

            if common_norm2 > 0.0:
                projection = (
                    float(
                        np.dot(
                            source_translation,
                            common_translation,
                        )
                    )
                    /
                    common_norm2
                )

                relative_translation = (
                    source_translation
                    - projection
                    * common_translation
                )

            else:
                relative_translation = np.zeros_like(
                    source_translation
                )

            return {
                "rmax":
                    rmax,

                "h":
                    h,

                "cells":
                    cells,

                "ell":
                    ell,

                "n":
                    n,

                "K":
                    K,

                "companion":
                    companion,

                "phase_x":
                    phase_x,

                "phase_y":
                    phase_y,

                "common_translation":
                    common_translation,

                "relative_translation":
                    relative_translation,
            }

        def classify_modes(
            case,
            values,
            vectors,
        ):
            n = case[
                "n"
            ]

            nq = (
                5
                * n
            )

            ell = case[
                "ell"
            ]

            rows = []

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
                    case[
                        "phase_x"
                    ],
                )

                py = overlap(
                    position,
                    case[
                        "phase_y"
                    ],
                )

                ct = overlap(
                    position,
                    case[
                        "common_translation"
                    ],
                )

                rt = overlap(
                    position,
                    case[
                        "relative_translation"
                    ],
                )

                symmetry = False
                symmetry_name = ""

                if (
                    ell == 0
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
                    ct
                    >= COMMON_TRANSLATION_OVERLAP_MIN
                ):
                    symmetry = True
                    symmetry_name = "COMMON_TRANSLATION"

                rows.append(
                    {
                        "real":
                            value.real,

                        "imag":
                            value.imag,

                        "phase_x_overlap":
                            px,

                        "phase_y_overlap":
                            py,

                        "common_translation_overlap":
                            ct,

                        "relative_translation_overlap":
                            rt,

                        "symmetry":
                            symmetry,

                        "symmetry_name":
                            symmetry_name,
                    }
                )

            return rows

        # ----------------------------------------------------------
        # B — identify ONLY incomplete rightmost cases.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE B: IDENTIFY INCOMPLETE RIGHTMOST CASES ===",
            flush=True,
        )

        inherited_spectrum = d3c[
            "spectrum_rows"
        ]

        repair_targets = []

        for row in inherited_spectrum:
            ell = int(
                row[
                    "ell"
                ]
            )

            rmax = float(
                row[
                    "rmax"
                ]
            )

            h_target = float(
                row[
                    "h_target"
                ]
            )

            right_complete = bool(
                row[
                    "right_complete"
                ]
            )

            if (
                ell in (
                    0,
                    1,
                    2,
                )
                and
                abs(
                    rmax
                    - RMAX_REPAIR
                )
                < 1.0e-10
                and
                any(
                    abs(
                        h_target
                        - allowed
                    )
                    < 1.0e-12
                    for allowed
                    in REPAIR_H_VALUES
                )
                and
                not right_complete
            ):
                repair_targets.append(
                    (
                        ell,
                        h_target,
                    )
                )

        repair_targets = sorted(
            set(
                repair_targets
            ),
            key=lambda item:
                (
                    item[
                        1
                    ],
                    item[
                        0
                    ],
                ),
            reverse=True,
        )

        print(
            f"RIGHTMOST_REPAIR_CASE_COUNT="
            f"{len(repair_targets)}",
            flush=True,
        )

        print(
            "RIGHTMOST_REPAIR_CASES="
            + ",".join(
                f"L{ell}@H{h}"
                for ell, h
                in repair_targets
            ),
            flush=True,
        )

        # ----------------------------------------------------------
        # C — rerun only incomplete rightmost requests.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE C: SURGICAL RIGHTMOST ARPACK REPAIR ===",
            flush=True,
        )

        repair_rows = []

        for (
            ell,
            h_target,
        ) in repair_targets:
            print(
                f"START_RIGHTMOST "
                f"L={ell} "
                f"H={h_target:.6f}",
                flush=True,
            )

            case = build_case(
                RMAX_REPAIR,
                h_target,
                ell,
            )

            k = RIGHT_K_BY_L[
                ell
            ]

            values, vectors, complete = (
                rightmost_eigs(
                    case[
                        "companion"
                    ],
                    k=k,
                )
            )

            modes = classify_modes(
                case,
                values,
                vectors,
            )

            physical = [
                mode
                for mode in modes
                if not mode[
                    "symmetry"
                ]
            ]

            if physical:
                max_physical_real = max(
                    mode[
                        "real"
                    ]
                    for mode in physical
                )

            else:
                max_physical_real = (
                    -math.inf
                )

            max_raw_real = max(
                (
                    mode[
                        "real"
                    ]
                    for mode in modes
                ),
                default=math.nan,
            )

            best_common = max(
                (
                    mode[
                        "common_translation_overlap"
                    ]
                    for mode in modes
                ),
                default=0.0,
            )

            row = {
                "ell":
                    ell,

                "h":
                    case[
                        "h"
                    ],

                "rmax":
                    RMAX_REPAIR,

                "matrix_dimension":
                    int(
                        case[
                            "companion"
                        ].shape[
                            0
                        ]
                    ),

                "requested_k":
                    k,

                "returned_count":
                    len(
                        values
                    ),

                "complete":
                    complete,

                "max_raw_real":
                    max_raw_real,

                "max_physical_real":
                    max_physical_real,

                "best_common_translation_overlap":
                    best_common,
            }

            repair_rows.append(
                row
            )

            print(
                f"RIGHTMOST_RESULT "
                f"L={ell} "
                f"H={case['h']:.6f} "
                f"DIM={row['matrix_dimension']} "
                f"RETURNED={row['returned_count']}/{k} "
                f"COMPLETE={complete} "
                f"MAX_RAW_RE={max_raw_real:+.12e} "
                f"MAX_PHYS_RE={max_physical_real:+.12e} "
                f"COMMON_OV={best_common:.9f}",
                flush=True,
            )

            # Explicitly release the large sparse matrices before
            # building the next case.
            del case
            del values
            del vectors

        repaired_complete = bool(
            repair_rows
            and
            all(
                row[
                    "complete"
                ]
                for row in repair_rows
            )
        )

        repaired_worst_physical = max(
            (
                row[
                    "max_physical_real"
                ]
                for row in repair_rows
                if math.isfinite(
                    row[
                        "max_physical_real"
                    ]
                )
            ),
            default=-math.inf,
        )

        repaired_growth_pass = bool(
            repaired_worst_physical
            <= GROWTH_TOL
        )

        print(
            f"RIGHTMOST_ALL_REPAIRS_COMPLETE="
            f"{repaired_complete}",
            flush=True,
        )

        print(
            f"RIGHTMOST_REPAIRED_WORST_PHYSICAL_REAL="
            f"{repaired_worst_physical:.15e}",
            flush=True,
        )

        print(
            f"RIGHTMOST_REPAIRED_GROWTH_PASS="
            f"{repaired_growth_pass}",
            flush=True,
        )

        # ----------------------------------------------------------
        # D — one new fine l=1 near-zero solve.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE D: ONE NEW L1 FINE-GRID SOLVE ===",
            flush=True,
        )

        print(
            f"START_L1_FINE "
            f"RMAX={RMAX_REPAIR:.1f} "
            f"H={NEW_L1_H:.6f}",
            flush=True,
        )

        fine_case = build_case(
            RMAX_REPAIR,
            NEW_L1_H,
            1,
        )

        near_values, near_vectors, near_complete = (
            near_zero_eigs(
                fine_case[
                    "companion"
                ],
                k=NEAR_K,
            )
        )

        near_modes = classify_modes(
            fine_case,
            near_values,
            near_vectors,
        )

        common_mode = max(
            near_modes,
            key=lambda mode:
                mode[
                    "common_translation_overlap"
                ],
            default=None,
        )

        physical_near_modes = [
            mode
            for mode in near_modes
            if not mode[
                "symmetry"
            ]
        ]

        relative_mode = max(
            physical_near_modes,
            key=lambda mode:
                mode[
                    "relative_translation_overlap"
                ],
            default=None,
        )

        if common_mode is None:
            common_overlap = 0.0
            common_real = math.nan

        else:
            common_overlap = float(
                common_mode[
                    "common_translation_overlap"
                ]
            )

            common_real = float(
                common_mode[
                    "real"
                ]
            )

        if relative_mode is None:
            relative_overlap = 0.0
            relative_real = math.nan
            relative_imag = math.nan

        else:
            relative_overlap = float(
                relative_mode[
                    "relative_translation_overlap"
                ]
            )

            relative_real = float(
                relative_mode[
                    "real"
                ]
            )

            relative_imag = float(
                relative_mode[
                    "imag"
                ]
            )

        print(
            f"L1_FINE_RESULT "
            f"H={fine_case['h']:.9f} "
            f"DIM={fine_case['companion'].shape[0]} "
            f"NEAR_COMPLETE={near_complete} "
            f"COMMON_OVERLAP={common_overlap:.12f} "
            f"COMMON_RE={common_real:+.15e} "
            f"RELATIVE_OVERLAP={relative_overlap:.12f} "
            f"RELATIVE_RE={relative_real:+.15e} "
            f"RELATIVE_IM={relative_imag:+.15e}",
            flush=True,
        )

        common_overlap_pass = bool(
            common_overlap
            >= COMMON_TRANSLATION_OVERLAP_MIN
        )

        # ----------------------------------------------------------
        # E — continuum fit using inherited + one new point.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE E: L1 H->0 CONTINUUM FIT ===",
            flush=True,
        )

        inherited_l1 = {}

        for row in inherited_spectrum:
            if (
                int(
                    row[
                        "ell"
                    ]
                )
                == 1
                and
                abs(
                    float(
                        row[
                            "rmax"
                        ]
                    )
                    - RMAX_REPAIR
                )
                < 1.0e-10
            ):
                h = float(
                    row[
                        "h"
                    ]
                )

                if any(
                    abs(
                        h
                        - requested
                    )
                    < 1.0e-10
                    for requested
                    in L1_INHERITED_H
                ):
                    inherited_l1[
                        h
                    ] = {
                        "relative_real":
                            float(
                                row[
                                    "relative_translation_real"
                                ]
                            ),

                        "common_growth":
                            float(
                                row[
                                    "common_translation_growth"
                                ]
                            ),

                        "relative_overlap":
                            float(
                                row[
                                    "relative_translation_overlap"
                                ]
                            ),

                        "common_overlap":
                            float(
                                row[
                                    "common_translation_overlap"
                                ]
                            ),
                    }

        if len(
            inherited_l1
        ) != len(
            L1_INHERITED_H
        ):
            raise RuntimeError(
                "Missing inherited l=1 convergence points"
            )

        h_values = []
        relative_growth_values = []
        common_growth_values = []

        for h in sorted(
            inherited_l1
        ):
            inherited = inherited_l1[
                h
            ]

            h_values.append(
                h
            )

            relative_growth_values.append(
                abs(
                    inherited[
                        "relative_real"
                    ]
                )
            )

            common_growth_values.append(
                abs(
                    inherited[
                        "common_growth"
                    ]
                )
            )

        h_values.append(
            fine_case[
                "h"
            ]
        )

        relative_growth_values.append(
            abs(
                relative_real
            )
        )

        common_growth_values.append(
            abs(
                common_real
            )
        )

        h_arr = np.asarray(
            h_values,
            dtype=float,
        )

        relative_arr = np.asarray(
            relative_growth_values,
            dtype=float,
        )

        common_arr = np.asarray(
            common_growth_values,
            dtype=float,
        )

        order = np.argsort(
            h_arr
        )

        h_arr = h_arr[
            order
        ]

        relative_arr = relative_arr[
            order
        ]

        common_arr = common_arr[
            order
        ]

        positive_mask = (
            relative_arr
            > 0.0
        )

        if np.sum(
            positive_mask
        ) < 3:
            raise RuntimeError(
                "Insufficient positive l1 convergence points"
            )

        relative_power = float(
            np.polyfit(
                np.log(
                    h_arr[
                        positive_mask
                    ]
                ),
                np.log(
                    relative_arr[
                        positive_mask
                    ]
                ),
                1,
            )[
                0
            ]
        )

        linear_fit = np.polyfit(
            h_arr,
            relative_arr,
            1,
        )

        quadratic_fit = np.polyfit(
            h_arr,
            relative_arr,
            2,
        )

        linear_intercept = float(
            linear_fit[
                -1
            ]
        )

        quadratic_intercept = float(
            quadratic_fit[
                -1
            ]
        )

        common_power = float(
            np.polyfit(
                np.log(
                    h_arr
                ),
                np.log(
                    common_arr
                ),
                1,
            )[
                0
            ]
        )

        print(
            "L1_CONTINUUM_POINTS="
            + ",".join(
                f"h={h:.6f}:g={g:.12e}"
                for h, g
                in zip(
                    h_arr,
                    relative_arr,
                    strict=True,
                )
            ),
            flush=True,
        )

        print(
            f"L1_RELATIVE_GROWTH_POWER="
            f"{relative_power:.15e}",
            flush=True,
        )

        print(
            f"L1_LINEAR_H0_INTERCEPT="
            f"{linear_intercept:.15e}",
            flush=True,
        )

        print(
            f"L1_QUADRATIC_H0_INTERCEPT="
            f"{quadratic_intercept:.15e}",
            flush=True,
        )

        print(
            f"COMMON_GOLDSTONE_GROWTH_POWER="
            f"{common_power:.15e}",
            flush=True,
        )

        # For sorted ascending h, the smallest h is index 0.
        fine_monotonic = bool(
            relative_arr[
                0
            ]
            <=
            L1_FINE_MONOTONIC_FACTOR
            * relative_arr[
                1
            ]
        )

        power_pass = bool(
            L1_POWER_MIN
            <= relative_power
            <= L1_POWER_MAX
        )

        intercept_pass = bool(
            abs(
                linear_intercept
            )
            <= L1_LINEAR_INTERCEPT_MAX
            and
            abs(
                quadratic_intercept
            )
            <= L1_QUADRATIC_INTERCEPT_MAX
        )

        print(
            f"L1_FINE_MONOTONIC_PASS="
            f"{fine_monotonic}",
            flush=True,
        )

        print(
            f"L1_H_SCALING_PASS="
            f"{power_pass}",
            flush=True,
        )

        print(
            f"L1_H0_INTERCEPT_PASS="
            f"{intercept_pass}",
            flush=True,
        )

        # ----------------------------------------------------------
        # F — analytic translation residuals.
        # No extra eigensolves.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE F: ANALYTIC TRANSLATION RESIDUAL SCALING ===",
            flush=True,
        )

        residual_rows = []

        for h_target in (
            0.50,
            0.375,
            0.25,
            NEW_L1_H,
        ):
            if (
                abs(
                    h_target
                    - NEW_L1_H
                )
                < 1.0e-12
            ):
                case = fine_case
                owns_case = False

            else:
                case = build_case(
                    RMAX_REPAIR,
                    h_target,
                    1,
                )

                owns_case = True

            K = case[
                "K"
            ]

            common = case[
                "common_translation"
            ]

            relative = case[
                "relative_translation"
            ]

            common_residual = float(
                np.linalg.norm(
                    K
                    @ common
                )
                /
                max(
                    np.linalg.norm(
                        common
                    ),
                    1.0e-300,
                )
            )

            relative_residual = float(
                np.linalg.norm(
                    K
                    @ relative
                )
                /
                max(
                    np.linalg.norm(
                        relative
                    ),
                    1.0e-300,
                )
            )

            residual_rows.append(
                {
                    "h":
                        case[
                            "h"
                        ],

                    "common_residual":
                        common_residual,

                    "relative_residual":
                        relative_residual,
                }
            )

            print(
                f"TRANSLATION_RESIDUAL "
                f"H={case['h']:.6f} "
                f"COMMON={common_residual:.12e} "
                f"RELATIVE={relative_residual:.12e}",
                flush=True,
            )

            if owns_case:
                del case

        residual_rows = sorted(
            residual_rows,
            key=lambda row:
                row[
                    "h"
                ],
        )

        residual_h = np.asarray(
            [
                row[
                    "h"
                ]
                for row in residual_rows
            ],
            dtype=float,
        )

        common_residuals = np.asarray(
            [
                row[
                    "common_residual"
                ]
                for row in residual_rows
            ],
            dtype=float,
        )

        common_residual_power = float(
            np.polyfit(
                np.log(
                    residual_h
                ),
                np.log(
                    common_residuals
                ),
                1,
            )[
                0
            ]
        )

        residual_decreasing = bool(
            common_residuals[
                0
            ]
            <
            common_residuals[
                -1
            ]
        )

        print(
            f"COMMON_TRANSLATION_RESIDUAL_POWER="
            f"{common_residual_power:.15e}",
            flush=True,
        )

        print(
            f"COMMON_TRANSLATION_RESIDUAL_DECREASES="
            f"{residual_decreasing}",
            flush=True,
        )

        # ----------------------------------------------------------
        # G — final decision.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE G: FINAL D3C-R DECISION ===",
            flush=True,
        )

        inherited_non_l1_growth = max(
            float(
                row[
                    "max_physical_growth"
                ]
            )
            for row in inherited_spectrum
            if int(
                row[
                    "ell"
                ]
            )
            != 1
        )

        inherited_non_l1_pass = bool(
            inherited_non_l1_growth
            <= GROWTH_TOL
        )

        inherited_domain_l1 = [
            row
            for row in inherited_spectrum
            if (
                int(
                    row[
                        "ell"
                    ]
                )
                == 1
                and
                abs(
                    float(
                        row[
                            "h"
                        ]
                    )
                    - 0.5
                )
                < 1.0e-12
                and
                float(
                    row[
                        "rmax"
                    ]
                )
                in (
                    600.0,
                    800.0,
                )
            )
        ]

        if len(
            inherited_domain_l1
        ) >= 2:
            domain_values = [
                float(
                    row[
                        "max_physical_growth"
                    ]
                )
                for row in inherited_domain_l1
            ]

            l1_domain_difference = abs(
                max(
                    domain_values
                )
                - min(
                    domain_values
                )
            )

        else:
            l1_domain_difference = math.inf

        l1_domain_pass = bool(
            l1_domain_difference
            <= 1.0e-8
        )

        print(
            f"INHERITED_NON_L1_WORST_REAL="
            f"{inherited_non_l1_growth:.15e}",
            flush=True,
        )

        print(
            f"INHERITED_NON_L1_PASS="
            f"{inherited_non_l1_pass}",
            flush=True,
        )

        print(
            f"L1_R600_R800_FIXED_H_DIFFERENCE="
            f"{l1_domain_difference:.15e}",
            flush=True,
        )

        print(
            f"L1_DOMAIN_INDEPENDENCE_PASS="
            f"{l1_domain_pass}",
            flush=True,
        )

        fine_near_pass = bool(
            near_complete
            and
            common_overlap_pass
        )

        continuum_pass = bool(
            fine_near_pass
            and
            fine_monotonic
            and
            power_pass
            and
            intercept_pass
            and
            l1_domain_pass
        )

        all_physics_pass = bool(
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
            repaired_complete
            and
            repaired_growth_pass
            and
            inherited_non_l1_pass
            and
            continuum_pass
        )

        print(
            f"NEW_FINE_NEAR_SOLVE_PASS="
            f"{fine_near_pass}",
            flush=True,
        )

        print(
            f"L1_CONTINUUM_ZERO_MODE_CLOSEOUT_PASS="
            f"{continuum_pass}",
            flush=True,
        )

        print(
            f"COUPLED_LINEAR_STABILITY_CLOSEOUT_PASS="
            f"{all_physics_pass}",
            flush=True,
        )

        if all_physics_pass:
            classification = (
                "GREEN_D3CR_COUPLED_LINEAR_STABILITY_"
                "THROUGH_L8_L1_CONTINUUM_GOLDSTONE_"
                "ARTIFACT_CLOSED"
            )

            next_action = (
                "031D3D_EXPLICIT_QY_RESERVOIR_TRANSFER_"
                "RESET_AND_RADIATION_GATE"
            )

        elif (
            not repaired_complete
        ):
            classification = (
                "YELLOW_D3CR_RIGHTMOST_ARPACK_"
                "STILL_NUMERICALLY_INCOMPLETE"
            )

            next_action = (
                "STOP_BRUTE_FORCE_ARPACK_AND_USE_"
                "INDEPENDENT_SPECTRAL_METHOD"
            )

        elif (
            not continuum_pass
        ):
            classification = (
                "YELLOW_OR_RED_D3CR_L1_CONTINUUM_"
                "ZERO_MODE_CLOSEOUT_FAILED"
            )

            next_action = (
                "INSPECT_L1_RELATIVE_TRANSLATION_PHYSICS"
            )

        else:
            classification = (
                "RED_D3CR_REPRODUCIBLE_NON_SYMMETRY_"
                "GROWTH_SURVIVES_REPAIR"
            )

            next_action = (
                "D3_ACTIVATION_STABILITY_FAIL"
            )

        print(
            f"031D3CR_CLASSIFICATION="
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
                classification.startswith(
                    "RED_D3CR_REPRODUCIBLE"
                )
            ),
            flush=True,
        )

        print(
            "FULL_031D_ACTIVATION_CERTIFIED=NO",
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

            "inherited_D3C": {
                "classification":
                    d3c[
                        "classification"
                    ],

                "activation_slope_pass":
                    d3c[
                        "activation_branch"
                    ][
                        "slope_pass"
                    ],

                "background_pass":
                    d3c[
                        "coupling"
                    ][
                        "background_pass"
                    ],

                "cross_hessian_pass":
                    d3c[
                        "coupling"
                    ][
                        "cross_preflight_pass"
                    ],

                "new_cross_hessian_max":
                    d3c[
                        "coupling"
                    ][
                        "new_canonical_cross_hessian_max"
                    ],
            },

            "rightmost_repair": {
                "targets":
                    repair_targets,

                "rows":
                    repair_rows,

                "all_complete":
                    repaired_complete,

                "worst_physical_real":
                    repaired_worst_physical,

                "growth_pass":
                    repaired_growth_pass,
            },

            "l1_fine": {
                "h":
                    fine_case[
                        "h"
                    ],

                "near_complete":
                    near_complete,

                "common_overlap":
                    common_overlap,

                "common_real":
                    common_real,

                "relative_overlap":
                    relative_overlap,

                "relative_real":
                    relative_real,

                "relative_imag":
                    relative_imag,
            },

            "l1_continuum": {
                "h":
                    h_arr,

                "relative_growth":
                    relative_arr,

                "common_growth":
                    common_arr,

                "relative_power":
                    relative_power,

                "linear_h0_intercept":
                    linear_intercept,

                "quadratic_h0_intercept":
                    quadratic_intercept,

                "common_growth_power":
                    common_power,

                "fine_monotonic_pass":
                    fine_monotonic,

                "power_pass":
                    power_pass,

                "intercept_pass":
                    intercept_pass,

                "domain_difference":
                    l1_domain_difference,

                "domain_pass":
                    l1_domain_pass,

                "closeout_pass":
                    continuum_pass,
            },

            "translation_residuals":
                residual_rows,

            "decision": {
                "inherited_non_l1_pass":
                    inherited_non_l1_pass,

                "rightmost_complete":
                    repaired_complete,

                "rightmost_growth_pass":
                    repaired_growth_pass,

                "l1_continuum_pass":
                    continuum_pass,

                "coupled_linear_stability_closeout_pass":
                    all_physics_pass,
            },

            "switching_inherited_not_rerun":
                d3c[
                    "switching"
                ],

            "claim_limits": [
                (
                    "GREEN closes the numerical coupled-linear "
                    "stability gate through l=8 in the declared "
                    "flat-space effective X/phi/Y model."
                ),
                (
                    "The original D3C l=3..8 spectra are inherited "
                    "rather than recomputed because those rightmost "
                    "requests completed."
                ),
                (
                    "Only previously incomplete rightmost sectors "
                    "are recomputed."
                ),
                (
                    "The l=1 apparent growth is promoted as a "
                    "discretized zero-mode artifact only if the "
                    "new h=.1875 point continues the h->0 trend."
                ),
                (
                    "The explicit QY reservoir/transfer/reset and "
                    "switching-radiation mechanism remains open."
                ),
                (
                    "Nonlinear fragmentation, Einstein backreaction, "
                    "radiative naturalness and empirical closure "
                    "remain open."
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
                for row in repair_rows
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
                repair_rows
            )

        print(
            f"SUMMARY_JSON={OUT_JSON}",
            flush=True,
        )

        print(
            f"REPAIR_CSV={OUT_CSV}",
            flush=True,
        )

    finally:
        qmod.X_MATCH = old_xmatch


if __name__ == "__main__":
    main()
