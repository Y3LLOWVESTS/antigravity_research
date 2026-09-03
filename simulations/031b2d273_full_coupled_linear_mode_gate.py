"""
031B2-D273
==========

Full coupled linear Q-ball amplitude / phase / scalar angular-mode gate.

Background:
    Psi = y(r) exp(-i Omega t)
    u   = u(r)

The exact dimensionless nonlinear equations used in 031B2-A imply the
linear rotating-frame perturbation system

    a_tt + 2 Omega b_t + L_a a + C v = 0

    b_tt - 2 Omega a_t + L_b b = 0

    v_tt + L_v v + D a = 0

where:

    a = Q-ball amplitude perturbation
    b = Q-ball phase perturbation
    v = gravitational-scalar perturbation.

For each spherical harmonic l, convert the quadratic eigenproblem

    (s^2 I + s G + K) X = 0

to a first-order sparse eigenproblem and search directly for modes with
positive Re(s).

Because the background is spherical, eigenvalues depend on l but not m.
Thus each tested l covers all m in that multiplet at the linear level.

This does NOT prove nonlinear fragmentation stability, finite-amplitude
stability, activation, radiative naturalness, or full metric stability.
"""

from __future__ import annotations

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
DATA = ROOT / "results/data"

UPSTREAM = (
    SIM
    /
    "031b2a_global_qball_activated_scalar_control.py"
)

SUMMARY = (
    DATA
    /
    "031b2a_global_qball_activated_scalar_control_summary.json"
)

OUT_JSON = (
    DATA
    /
    "031b2d273_full_coupled_linear_mode_summary.json"
)


LMAX = 8

N_VALUES = (
    160,
    220,
)

RMAX = 60.0

EIG_COUNT = 18

GROWTH_TOL = 1.0e-4

GRID_GROWTH_ABS_TOL = 5.0e-4

HBAR_GEV_S = 6.582119569e-25


def require(path: Path):

    if not path.is_file():

        raise RuntimeError(
            f"Missing required file: {path}"
        )


def load_module(name, path):

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

    sys.modules[
        spec.name
    ] = module

    spec.loader.exec_module(
        module
    )

    return module


def to_builtin(value: Any):

    if isinstance(value, np.generic):

        return value.item()

    if isinstance(value, np.ndarray):

        return value.tolist()

    if isinstance(value, complex):

        return {
            "real":
            value.real,

            "imag":
            value.imag,
        }

    if isinstance(value, dict):

        return {
            str(k):
            to_builtin(v)
            for k, v
            in value.items()
        }

    if isinstance(value, (list, tuple)):

        return [
            to_builtin(v)
            for v
            in value
        ]

    return value


def reconstruct(qmod, best):

    omega = float(
        best[
            "omega"
        ]
    )

    epsilon = float(
        best[
            "epsilon"
        ]
    )

    chi = float(
        best[
            "chi"
        ]
    )

    seed = qmod.solve_uncoupled_qball(
        omega
    )

    if seed is None:

        raise RuntimeError(
            "Uncoupled Q-ball reconstruction failed"
        )

    solution = qmod.solve_coupled(
        seed,
        omega,
        epsilon,
        chi,
        previous=None,
    )

    if solution is None:

        raise RuntimeError(
            "Coupled Q-ball reconstruction failed"
        )

    return (
        omega,
        epsilon,
        chi,
        solution,
    )


def mode_operator(
    qmod,
    solution,
    omega,
    epsilon,
    chi,
    ell,
    n,
):

    r = np.linspace(
        0.0,
        RMAX,
        n,
    )

    h = (
        r[
            1
        ]
        -
        r[
            0
        ]
    )

    ri = r[
        1:-1
    ]

    state = solution.sol(
        np.maximum(
            ri,
            1.0e-5,
        )
    )

    y = state[
        0
    ]

    u = state[
        2
    ]

    A = np.exp(
        np.clip(
            -0.5
            *
            u**2,
            -700.0,
            0.0,
        )
    )

    denominator = (
        1.0
        +
        y**2
    )

    Va = (
        A
        *
        (
            1.0
            -
            y**2
        )
        /
        denominator**2
        -
        omega**2
    )

    Vb = (
        A
        /
        denominator
        -
        omega**2
    )

    Vv = (
        epsilon**2
        +
        chi**2
        *
        A
        *
        qmod.W(
            y
        )
        *
        (
            u**2
            -
            1.0
        )
    )

    C = (
        -u
        *
        A
        *
        y
        /
        denominator
    )

    D = (
        -chi**2
        *
        u
        *
        A
        *
        y
        /
        denominator
    )

    angular = (
        ell
        *
        (
            ell
            +
            1
        )
        /
        ri**2
    )

    count = len(
        ri
    )

    lap_diag = np.full(
        count,
        2.0
        /
        h**2,
    )

    lap_off = np.full(
        count
        -
        1,
        -1.0
        /
        h**2,
    )

    T = diags(
        (
            lap_off,
            lap_diag,
            lap_off,
        ),
        (
            -1,
            0,
            1,
        ),
        format="csr",
    )

    La = (
        T
        +
        diags(
            angular
            +
            Va,
            0,
            format="csr",
        )
    )

    Lb = (
        T
        +
        diags(
            angular
            +
            Vb,
            0,
            format="csr",
        )
    )

    Lv = (
        T
        +
        diags(
            angular
            +
            Vv,
            0,
            format="csr",
        )
    )

    Z = csr_matrix(
        (
            count,
            count,
        )
    )

    Cmat = diags(
        C,
        0,
        format="csr",
    )

    Dmat = diags(
        D,
        0,
        format="csr",
    )

    K = bmat(
        (
            (
                La,
                Z,
                Cmat,
            ),
            (
                Z,
                Lb,
                Z,
            ),
            (
                Dmat,
                Z,
                Lv,
            ),
        ),
        format="csr",
    )

    I = identity(
        count,
        format="csr",
    )

    Gmat = bmat(
        (
            (
                Z,
                2.0
                *
                omega
                *
                I,
                Z,
            ),
            (
                -2.0
                *
                omega
                *
                I,
                Z,
                Z,
            ),
            (
                Z,
                Z,
                Z,
            ),
        ),
        format="csr",
    )

    dim = (
        3
        *
        count
    )

    Zbig = csr_matrix(
        (
            dim,
            dim,
        )
    )

    Ibig = identity(
        dim,
        format="csr",
    )

    first_order = bmat(
        (
            (
                Zbig,
                Ibig,
            ),
            (
                -K,
                -Gmat,
            ),
        ),
        format="csr",
    )

    return first_order


def largest_growth(operator):

    try:

        values = eigs(
            operator,
            k=EIG_COUNT,
            which="LR",
            return_eigenvectors=False,
            tol=2.0e-8,
            maxiter=40_000,
        )

    except ArpackNoConvergence as exc:

        values = exc.eigenvalues

        if values is None or len(
            values
        ) < 4:

            raise RuntimeError(
                "ARPACK failed without sufficient eigenvalues"
            )

    values = np.asarray(
        values,
        dtype=complex,
    )

    order = np.argsort(
        values.real
    )[
        ::-1
    ]

    values = values[
        order
    ]

    return (
        float(
            np.max(
                values.real
            )
        ),
        values,
    )


def main():

    print(
        "=== 031B2-D273 FULL COUPLED "
        "LINEAR ANGULAR-MODE GATE ==="
    )

    print(
        "CLAIM_CLASS="
        "COUPLED_QBALL_PHASE_AMPLITUDE_SCALAR_"
        "LINEAR_DYNAMIC_STABILITY_PREFLIGHT"
    )

    print(
        "NONLINEAR_FRAGMENTATION_PROOF=NO"
    )

    require(
        UPSTREAM
    )

    require(
        SUMMARY
    )

    summary = json.loads(
        SUMMARY.read_text()
    )

    best = summary[
        "best"
    ]

    qmod = load_module(
        "d273_qball",
        UPSTREAM,
    )

    (
        omega,
        epsilon,
        chi,
        solution,
    ) = reconstruct(
        qmod,
        best,
    )

    mx_gev = float(
        best[
            "m_x_gev"
        ]
    )

    print(
        f"OMEGA="
        f"{omega:.15e}"
    )

    print(
        f"EPSILON="
        f"{epsilon:.15e}"
    )

    print(
        f"CHI="
        f"{chi:.15e}"
    )

    results = {}

    for n in N_VALUES:

        n_result = {}

        print(
            f"\n=== GRID_N={n} ==="
        )

        for ell in range(
            LMAX
            +
            1
        ):

            operator = mode_operator(
                qmod,
                solution,
                omega,
                epsilon,
                chi,
                ell,
                n,
            )

            growth, values = largest_growth(
                operator
            )

            if growth > 0.0:

                tau_seconds = (
                    HBAR_GEV_S
                    /
                    (
                        mx_gev
                        *
                        growth
                    )
                )

            else:

                tau_seconds = math.inf

            passed = bool(
                growth
                <=
                GROWTH_TOL
            )

            n_result[
                str(
                    ell
                )
            ] = {
                "max_real_growth":
                growth,

                "growth_pass":
                passed,

                "efold_seconds_if_positive":
                tau_seconds,

                "leading_eigenvalues":
                values[
                    :8
                ],
            }

            print(
                f"COUPLED_MODE "
                f"N={n} "
                f"L={ell} "
                f"MAX_RE_S="
                f"{growth:.15e} "
                f"PASS={passed} "
                f"TAU_S="
                f"{tau_seconds:.15e}"
            )

        results[
            str(
                n
            )
        ] = n_result

    fine_key = str(
        max(
            N_VALUES
        )
    )

    coarse_key = str(
        min(
            N_VALUES
        )
    )

    fine_growth = [
        results[
            fine_key
        ][
            str(
                ell
            )
        ][
            "max_real_growth"
        ]
        for ell
        in range(
            LMAX
            +
            1
        )
    ]

    coarse_growth = [
        results[
            coarse_key
        ][
            str(
                ell
            )
        ][
            "max_real_growth"
        ]
        for ell
        in range(
            LMAX
            +
            1
        )
    ]

    worst_fine = max(
        fine_growth
    )

    grid_difference = max(
        abs(
            fine
            -
            coarse
        )
        for fine, coarse
        in zip(
            fine_growth,
            coarse_growth,
        )
    )

    all_pass = bool(
        worst_fine
        <=
        GROWTH_TOL
        and
        grid_difference
        <=
        GRID_GROWTH_ABS_TOL
    )

    print(
        "\n=== DECISION ==="
    )

    print(
        f"WORST_FINE_GRID_GROWTH="
        f"{worst_fine:.15e}"
    )

    print(
        f"MAX_GRID_GROWTH_DIFFERENCE="
        f"{grid_difference:.15e}"
    )

    print(
        f"D273_COUPLED_LINEAR_L0_TO_L8_PASS="
        f"{all_pass}"
    )

    if all_pass:

        classification = (
            "GREEN_273GJ_FULL_COUPLED_LINEAR_"
            "ANGULAR_SPECTRUM_L0_TO_L8_"
            "NONLINEAR_FRAGMENTATION_AND_"
            "RADIATIVE_NATURALNESS_OPEN"
        )

        next_step = (
            "031D273_SELF_ACTIVATION_OFFSTATE_"
            "PLUS_NONLINEAR_FRAGMENTATION_GATE"
        )

    else:

        classification = (
            "RED_OR_YELLOW_273GJ_COUPLED_"
            "LINEAR_DYNAMIC_MODE_FOUND"
        )

        next_step = (
            "DIAGNOSE_COUPLED_MODE_BEFORE_"
            "ACTIVATION_OR_METRIC_PROMOTION"
        )

    print(
        f"031B2D273_CLASSIFICATION="
        f"{classification}"
    )

    print(
        f"NEXT="
        f"{next_step}"
    )

    print(
        "RADIATIVE_NATURALNESS_CLOSED=NO"
    )

    print(
        "NONLINEAR_FRAGMENTATION_CLOSED=NO"
    )

    print(
        "FULL_METRIC_BACKREACTION_CLOSED=NO"
    )

    output = {
        "omega":
        omega,

        "epsilon":
        epsilon,

        "chi":
        chi,

        "results":
        results,

        "worst_fine_growth":
        worst_fine,

        "grid_growth_difference":
        grid_difference,

        "coupled_linear_l0_to_l8_pass":
        all_pass,

        "classification":
        classification,

        "next":
        next_step,

        "claim_limits": [
            "This is a linearized coupled amplitude/phase/scalar spectrum.",
            "Spherical symmetry makes each l result degenerate across m.",
            "Finite-amplitude fragmentation and fission remain open.",
            "The physical metric and payload are not dynamical degrees of freedom in this spectrum.",
            "Radiative naturalness remains open.",
            "No practical device is established.",
        ],
    }

    OUT_JSON.write_text(
        json.dumps(
            to_builtin(
                output
            ),
            indent=2,
            sort_keys=True,
        )
        +
        "\n"
    )

    print(
        f"SUMMARY_JSON="
        f"{OUT_JSON.resolve()}"
    )


if __name__ == "__main__":
    main()
