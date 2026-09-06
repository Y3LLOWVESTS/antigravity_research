#!/usr/bin/env python3
"""
031D3D2 — energy-matched adiabatic activation-transfer closeout.

This run is deliberately intended to be the last 031D switching gate if it
passes.

D3D0 established an exact endpoint charge reservoir using a spectator
complex field R sharing the diagonal global U(1).

D3D1 established a bounded reciprocal neutral mixer capacity, but retained
an approximately 30.74-GJ OFF-to-ON endpoint energy mismatch.

A closed evolution cannot hide that energy.

D3D2 therefore gives R one globally fixed mass scale such that its OFF
Q-ball carries the source/scalarization energy that appears in ON.

The run then:

1. independently reconstructs the common Hamiltonian normalization;
2. reconstructs microscopic OFF and ON fields;
3. verifies the energy-matched R Q-ball at identical conserved charge;
4. locates the unscalarized-source tachyonic threshold;
5. follows the scalarized source branch backward through that threshold;
6. constructs an explicit finite-energy Y<->R population path;
7. preserves Q_Y+Q_R exactly along that path;
8. includes source/scalar reaction self-consistently at every sampled q;
9. remaps the inherited bounded controller for unequal Y/R morphology;
10. derives the path-dependent chemical detuning/chirp;
11. checks leading single-particle radiation thresholds;
12. checks forward and reverse resonant-envelope transfer.

GREEN closes D3D only at the adiabatic multiscale flat-space
effective-theory level.

It does NOT establish:
- a carrier-resolved nonlinear radial PDE trajectory;
- nonlinear fragmentation stability;
- multiparticle/higher-harmonic radiation closure;
- Einstein backreaction;
- EFT/naturalness;
- empirical fifth-force/EP/PPN closure;
- a practical device.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
from pathlib import Path
import sys
from typing import Any

import numpy as np

from scipy.integrate import (
    cumulative_trapezoid,
    solve_bvp,
    solve_ivp,
)

from scipy.optimize import brentq

from scipy.sparse import diags
from scipy.sparse.linalg import eigsh


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results" / "data"

DATA.mkdir(
    parents=True,
    exist_ok=True,
)

D3D0_SUMMARY = (
    DATA
    / "031d3d0_exact_conserved_charge_reservoir_summary.json"
)

D3D1_SUMMARY = (
    DATA
    / "031d3d1_stabilized_neutral_mixer_summary.json"
)

R5_SUMMARY = (
    DATA
    / "031d3cr5_saturation_safe_schur_summary.json"
)

D3C_SUMMARY = (
    DATA
    / "031d3c_activation_stability_switching_summary.json"
)

R4_SOURCE = (
    SIM
    / "031d3cr4_relative_translation_ward_closeout.py"
)

OUT_JSON = (
    DATA
    / "031d3d2_energy_matched_adiabatic_transfer_summary.json"
)

OUT_PATH = (
    DATA
    / "031d3d2_energy_matched_transfer_path.csv"
)

OUT_BRANCH = (
    DATA
    / "031d3d2_source_scalarization_branch.csv"
)


J_PER_EV = 1.602176634e-19
H_EV_S = 4.135667696e-15

X0 = 1.0e-5

SOURCE_RMAX = 500.0
ENERGY_RMAX = 1200.0
SOURCE_MATCH = 80.0

BVP_TOL = 8.0e-6
BVP_MAX_NODES = 40_000

ENERGY_NORMALIZATION_REL_TOL = 1.5e-2
ENDPOINT_EQUALITY_REL_TOL = 1.5e-2
RESERVOIR_SCALING_REL_TOL = 8.0e-3
SOURCE_ENDPOINT_REL_TOL = 1.5e-2

SCALAR_BRANCH_Q_GAP_MAX = 0.035

RWA_FIDELITY_MIN = 0.999
RWA_NORM_ERR_MAX = 2.0e-8

PRIMARY_SWITCH_S = 1.0

Q_SCAN_COARSE = np.linspace(
    0.0,
    1.0,
    21,
)


def require(
    path: Path,
) -> None:

    if not path.is_file():

        raise RuntimeError(
            f"Missing required artifact: {path}"
        )


def load_json(
    path: Path,
) -> dict[str, Any]:

    return json.loads(
        path.read_text()
    )


def load_module(
    name: str,
    path: Path,
):

    spec = (
        importlib.util.spec_from_file_location(
            name,
            path,
        )
    )

    if (
        spec is None
        or spec.loader is None
    ):

        raise RuntimeError(
            f"Cannot import {path}"
        )

    module = (
        importlib.util.module_from_spec(
            spec
        )
    )

    sys.modules[
        name
    ] = module

    try:

        spec.loader.exec_module(
            module
        )

    except Exception:

        sys.modules.pop(
            name,
            None,
        )

        raise

    return module


def relerr(
    a: float,
    b: float,
    floor: float = 1.0e-300,
) -> float:

    return (
        abs(
            a - b
        )
        / max(
            abs(
                a
            ),
            abs(
                b
            ),
            floor,
        )
    )


def builtin(
    value: Any,
) -> Any:

    if isinstance(
        value,
        dict,
    ):

        return {
            str(
                key
            ):
            builtin(
                child
            )
            for key, child
            in value.items()
        }

    if isinstance(
        value,
        (
            list,
            tuple,
        ),
    ):

        return [
            builtin(
                child
            )
            for child
            in value
        ]

    if isinstance(
        value,
        np.ndarray,
    ):

        return value.tolist()

    if isinstance(
        value,
        (
            np.floating,
            np.integer,
            np.bool_,
        ),
    ):

        return value.item()

    return value


def W(
    z,
):

    z = np.asarray(
        z,
        dtype=float,
    )

    return (
        0.5
        * np.log1p(
            z * z
        )
    )


def activation_fraction(
    a,
):

    a = np.asarray(
        a,
        dtype=float,
    )

    return -np.expm1(
        -0.5
        * a
        * a
    )


def make_mesh() -> np.ndarray:

    return np.unique(
        np.concatenate(
            (
                np.linspace(
                    X0,
                    20.0,
                    700,
                ),

                np.linspace(
                    20.0,
                    100.0,
                    500,
                ),

                np.linspace(
                    100.0,
                    SOURCE_RMAX,
                    600,
                ),
            )
        )
    )


def make_energy_grid() -> np.ndarray:

    return np.unique(
        np.concatenate(
            (
                np.linspace(
                    X0,
                    20.0,
                    8000,
                ),

                np.linspace(
                    20.0,
                    120.0,
                    7000,
                ),

                np.linspace(
                    120.0,
                    500.0,
                    7000,
                ),

                np.linspace(
                    500.0,
                    ENERGY_RMAX,
                    5000,
                ),
            )
        )
    )


def uncoupled_source_eval(
    source,
    omega: float,
    x,
):

    x = np.asarray(
        x,
        dtype=float,
    )

    out_y = np.empty_like(
        x
    )

    out_yp = np.empty_like(
        x
    )

    inside = (
        x <= SOURCE_MATCH
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

        out_y[
            inside
        ] = state[
            0
        ]

        out_yp[
            inside
        ] = state[
            1
        ]

    outside = (
        ~inside
    )

    if np.any(
        outside
    ):

        xx = x[
            outside
        ]

        boundary = source.sol(
            SOURCE_MATCH
        )

        yb = float(
            boundary[
                0
            ]
        )

        k = math.sqrt(
            max(
                1.0
                - omega
                * omega,
                1.0e-14,
            )
        )

        yy = (
            yb
            * SOURCE_MATCH
            / xx
            * np.exp(
                -k
                * (
                    xx
                    - SOURCE_MATCH
                )
            )
        )

        out_y[
            outside
        ] = yy

        out_yp[
            outside
        ] = (
            -k
            - 1.0
            / xx
        ) * yy

    return (
        out_y,
        out_yp,
    )


def bvp_source_eval(
    solution,
    epsilon: float,
    x,
):

    x = np.asarray(
        x,
        dtype=float,
    )

    state = np.empty(
        (
            4,
            x.size,
        ),
        dtype=float,
    )

    inside = (
        x <= SOURCE_RMAX
    )

    if np.any(
        inside
    ):

        state[
            :,
            inside,
        ] = (
            solution.sol(
                np.maximum(
                    x[
                        inside
                    ],
                    X0,
                )
            )[
                :4
            ]
        )

    outside = (
        ~inside
    )

    if np.any(
        outside
    ):

        xx = x[
            outside
        ]

        boundary = solution.sol(
            SOURCE_RMAX
        )

        omega = float(
            solution.p[
                0
            ]
        )

        ky = math.sqrt(
            max(
                1.0
                - omega
                * omega,
                1.0e-14,
            )
        )

        y = (
            float(
                boundary[
                    0
                ]
            )
            * SOURCE_RMAX
            / xx
            * np.exp(
                -ky
                * (
                    xx
                    - SOURCE_RMAX
                )
            )
        )

        u = (
            float(
                boundary[
                    2
                ]
            )
            * SOURCE_RMAX
            / xx
            * np.exp(
                -epsilon
                * (
                    xx
                    - SOURCE_RMAX
                )
            )
        )

        state[
            0,
            outside,
        ] = y

        state[
            1,
            outside,
        ] = (
            -ky
            - 1.0
            / xx
        ) * y

        state[
            2,
            outside,
        ] = u

        state[
            3,
            outside,
        ] = (
            -epsilon
            - 1.0
            / xx
        ) * u

    return tuple(
        state[
            index
        ]
        for index
        in range(
            4
        )
    )


def solve_source_branch(
    q: float,
    a1_func,
    target_qx: float,
    epsilon: float,
    chi: float,
    *,
    previous=None,
    seed_arrays=None,
    omega_seed: float,
):

    mesh = make_mesh()

    def ode(
        x,
        state,
        params,
    ):

        omega = float(
            params[
                0
            ]
        )

        y = state[
            0
        ]

        yp = state[
            1
        ]

        u = state[
            2
        ]

        up = state[
            3
        ]

        a1 = a1_func(
            x
        )

        f = activation_fraction(
            math.sqrt(
                max(
                    q,
                    0.0,
                )
            )
            * a1
        )

        A = np.exp(
            -0.5
            * f
            * u
            * u
        )

        return np.vstack(
            (
                yp,

                A
                * y
                / (
                    1.0
                    + y
                    * y
                )
                - omega
                * omega
                * y
                - 2.0
                * yp
                / x,

                up,

                epsilon
                * epsilon
                * u
                - chi
                * chi
                * f
                * A
                * W(
                    y
                )
                * u
                - 2.0
                * up
                / x,

                4.0
                * math.pi
                * omega
                * x
                * x
                * y
                * y,
            )
        )

    def bc(
        left,
        right,
        params,
    ):

        omega = float(
            params[
                0
            ]
        )

        k = math.sqrt(
            max(
                1.0
                - omega
                * omega,
                1.0e-14,
            )
        )

        return np.array(
            (
                left[
                    1
                ],

                left[
                    3
                ],

                left[
                    4
                ],

                right[
                    1
                ]
                + (
                    k
                    + 1.0
                    / SOURCE_RMAX
                )
                * right[
                    0
                ],

                right[
                    3
                ]
                + (
                    epsilon
                    + 1.0
                    / SOURCE_RMAX
                )
                * right[
                    2
                ],

                right[
                    4
                ]
                - target_qx,
            ),
            dtype=float,
        )

    if previous is not None:

        guess4 = (
            previous.sol(
                mesh
            )[
                :4
            ]
        )

        omega_guess = float(
            previous.p[
                0
            ]
        )

    elif seed_arrays is not None:

        guess4 = np.vstack(
            [
                np.asarray(
                    value,
                    dtype=float,
                )
                for value
                in seed_arrays(
                    mesh
                )
            ]
        )

        omega_guess = float(
            omega_seed
        )

    else:

        raise RuntimeError(
            "Need previous solution or seed arrays"
        )

    qprime = (
        4.0
        * math.pi
        * omega_guess
        * mesh
        * mesh
        * guess4[
            0
        ]
        * guess4[
            0
        ]
    )

    qint = np.concatenate(
        (
            np.array(
                [
                    0.0
                ]
            ),

            cumulative_trapezoid(
                qprime,
                mesh,
            ),
        )
    )

    guess = np.vstack(
        (
            guess4,
            qint,
        )
    )

    solution = solve_bvp(
        ode,
        bc,
        mesh,
        guess,
        p=np.array(
            [
                omega_guess
            ],
            dtype=float,
        ),
        tol=BVP_TOL,
        max_nodes=BVP_MAX_NODES,
        verbose=0,
    )

    if not solution.success:

        raise RuntimeError(
            "Source BVP failed at "
            f"q={q:.9f}: "
            f"{solution.message}"
        )

    return solution


def source_energy_I(
    y,
    yp,
    u,
    up,
    omega: float,
    f,
    chi: float,
    epsilon: float,
    x,
) -> float:

    A = np.exp(
        -0.5
        * f
        * u
        * u
    )

    density = (
        0.5
        * yp
        * yp

        + 0.5
        * omega
        * omega
        * y
        * y

        + A
        * W(
            y
        )

        + 0.5
        * (
            up
            * up
            + epsilon
            * epsilon
            * u
            * u
        )
        / (
            chi
            * chi
        )
    )

    return float(
        4.0
        * math.pi
        * np.trapezoid(
            x
            * x
            * density,
            x,
        )
    )


def component_energy_I(
    a,
    apx,
    rho: float,
    mu: float,
    omega: float,
    x,
) -> float:

    density = (
        rho
        * (
            0.5
            * apx
            * apx

            + 0.5
            * mu
            * mu
            * omega
            * omega
            * a
            * a

            + mu
            * mu
            * W(
                a
            )
        )
    )

    return float(
        4.0
        * math.pi
        * np.trapezoid(
            x
            * x
            * density,
            x,
        )
    )


def lowest_unscalarized_scalar_mode(
    q: float,
    a1_func,
    yoff_func,
    epsilon: float,
    chi: float,
) -> float:

    rmax = SOURCE_RMAX

    n = 1800

    h = (
        rmax
        / n
    )

    r = (
        h
        * np.arange(
            1,
            n,
            dtype=float,
        )
    )

    a = a1_func(
        r
    )

    y = yoff_func(
        r
    )

    f = activation_fraction(
        math.sqrt(
            max(
                q,
                0.0,
            )
        )
        * a
    )

    potential = (
        epsilon
        * epsilon
        - chi
        * chi
        * f
        * W(
            y
        )
    )

    diagonal = (
        2.0
        / (
            h
            * h
        )
        + potential
    )

    off = (
        -np.ones(
            n
            - 2
        )
        / (
            h
            * h
        )
    )

    operator = diags(
        (
            off,
            diagonal,
            off,
        ),
        offsets=(
            -1,
            0,
            1,
        ),
        format="csr",
    )

    return float(
        eigsh(
            operator,
            k=1,
            which="SA",
            return_eigenvectors=False,
            tol=2.0e-10,
        )[
            0
        ]
    )


def rwa_transfer(
    duration: float,
    detuning_hz: float,
    reverse: bool = False,
) -> dict[str, float]:

    delta = (
        2.0
        * math.pi
        * detuning_hz
    )

    def rhs(
        t,
        psi,
    ):

        omega_r = (
            2.0
            * math.pi
            / duration
            * math.sin(
                math.pi
                * t
                / duration
            ) ** 2
        )

        H00 = (
            0.5
            * delta
        )

        H11 = (
            -0.5
            * delta
        )

        H01 = (
            0.5
            * omega_r
        )

        return (
            -1j
            * np.array(
                (
                    H00
                    * psi[
                        0
                    ]
                    + H01
                    * psi[
                        1
                    ],

                    H01
                    * psi[
                        0
                    ]
                    + H11
                    * psi[
                        1
                    ],
                ),
                dtype=complex,
            )
        )

    if reverse:

        initial = np.array(
            (
                1.0,
                0.0,
            ),
            dtype=complex,
        )

    else:

        initial = np.array(
            (
                0.0,
                1.0,
            ),
            dtype=complex,
        )

    solution = solve_ivp(
        rhs,
        (
            0.0,
            duration,
        ),
        initial,
        rtol=2.0e-11,
        atol=2.0e-13,
        method="DOP853",
    )

    final = solution.y[
        :,
        -1
    ]

    target_index = (
        1
        if reverse
        else 0
    )

    fidelity = float(
        abs(
            final[
                target_index
            ]
        ) ** 2
    )

    norm_error = abs(
        float(
            np.vdot(
                final,
                final,
            ).real
        )
        - 1.0
    )

    return {
        "fidelity":
            fidelity,

        "norm_error":
            norm_error,

        "steps":
            int(
                solution.t.size
            ),
    }


def main() -> None:

    print(
        "=== 031D3D2 ENERGY-MATCHED ADIABATIC TRANSFER / "
        "SOURCE-RESPONSE CLOSEOUT ==="
    )

    print(
        "CLAIM_CLASS="
        "ADIABATIC_MULTISCALE_FIXED_CHARGE_TRANSFER_CLOSEOUT"
    )

    print(
        "D3D1_GREEN_REQUIRED=YES"
    )

    print(
        "ENERGY_MATCHED_SPECTATOR_R="
        "YES_FIXED_GLOBAL_THEORY_PARAMETER"
    )

    print(
        "SOURCE_RESPONSE_SOLVED_SELF_CONSISTENTLY_ALONG_TRANSFER=YES"
    )

    print(
        "FULL_CARRIER_RESOLVED_TIME_DOMAIN_PDE=NO"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    for path in (
        D3D0_SUMMARY,
        D3D1_SUMMARY,
        R5_SUMMARY,
        D3C_SUMMARY,
        R4_SOURCE,
    ):

        require(
            path
        )

    d0 = load_json(
        D3D0_SUMMARY
    )

    d1 = load_json(
        D3D1_SUMMARY
    )

    r5 = load_json(
        R5_SUMMARY
    )

    d3c = load_json(
        D3C_SUMMARY
    )

    if not str(
        d1.get(
            "classification",
            "",
        )
    ).startswith(
        "GREEN_D3D1"
    ):

        raise RuntimeError(
            "D3D1 preflight is not GREEN"
        )

    model = r5[
        "model"
    ]

    epsilon = float(
        model[
            "epsilon"
        ]
    )

    chi = float(
        model[
            "chi"
        ]
    )

    omega_x_on = float(
        model[
            "omega_x"
        ]
    )

    omega_y = float(
        model[
            "omega_y"
        ]
    )

    mu_y = float(
        model[
            "mu"
        ]
    )

    rho_y = float(
        model[
            "rho_y"
        ]
    )

    target_qx = float(
        model[
            "target_I_QX"
        ]
    )

    target_qy = float(
        model[
            "target_I_QY"
        ]
    )

    switching = d3c[
        "switching"
    ]

    omega_x_off = float(
        switching[
            "off_omega_x"
        ]
    )

    E_off_source_J = float(
        switching[
            "off_source_energy_J"
        ]
    )

    E_on_total_J = float(
        switching[
            "full_on_conservative_J"
        ]
    )

    E_y_cert_J = float(
        switching[
            "on_activation_inventory_J"
        ]
    )

    Q_star = float(
        d0[
            "model"
        ][
            "Q_star"
        ]
    )

    m_y_eV = float(
        d0[
            "model"
        ][
            "m_A_eV"
        ]
    )

    eqm = float(
        d0[
            "reservoir_qball"
        ][
            "E_over_Qm_model"
        ]
    )

    target_R_J = (
        E_on_total_J
        - E_off_source_J
    )

    m_R_eV = (
        target_R_J
        / (
            Q_star
            * J_PER_EV
            * eqm
        )
    )

    mass_ratio = (
        m_R_eV
        / m_y_eV
    )

    mu_R = (
        mu_y
        * mass_ratio
    )

    rho_R = (
        rho_y
        * mass_ratio
        * mass_ratio
    )

    print(
        "\n=== STAGE A: ENERGY-MATCHED RESERVOIR THEORY ==="
    )

    print(
        f"TARGET_R_ENERGY_J={target_R_J:.15e}"
    )

    print(
        f"M_Y_EV={m_y_eV:.15e}"
    )

    print(
        f"M_R_EV={m_R_eV:.15e}"
    )

    print(
        f"M_R_OVER_M_Y={mass_ratio:.15e}"
    )

    print(
        f"MU_R={mu_R:.15e}"
    )

    print(
        f"RHO_R={rho_R:.15e}"
    )

    print(
        f"R_E_OVER_QMR={eqm:.15e}"
    )

    print(
        "FIXED_THEORY_SPATIAL_PARAMETER_PROGRAMMING=NO"
    )

    r4 = load_module(
        "r4_for_d3d2",
        R4_SOURCE,
    )

    d3b = load_module(
        "d3b_for_d3d2",
        r4.D3B_SOURCE,
    )

    qmod = load_module(
        "qball_for_d3d2",
        r4.QBALL_SOURCE,
    )

    d3a = load_module(
        "d3a_for_d3d2",
        r4.D3A_SOURCE,
    )

    old_xmatch = float(
        qmod.X_MATCH
    )

    old_d3a_match = float(
        d3a.X_MATCH
    )

    try:

        print(
            "\n=== STAGE B: FULL ON + OFF MICROSCOPIC RECONSTRUCTION ===",
            flush=True,
        )

        (
            product80,
            source80,
            activation80,
        ) = (
            r4.build_product_background(
                qmod,
                d3a,
                omega_x_on,
                omega_y,
                epsilon,
                chi,
                mu_y,
                r4.X_SOURCE_MATCH,
            )
        )

        (
            _coarse,
            _fine,
            tight,
            _homotopy,
            _diag_c,
            _diag_f,
            diag_t,
        ) = (
            r4.reconstruct_full_background(
                d3b,
                qmod,
                d3a,
                product80,
                source80,
                activation80,
                omega_x_seed=omega_x_on,
                omega_y_seed=omega_y,
                epsilon=epsilon,
                chi=chi,
                mu=mu_y,
                rho_y=rho_y,
                target_qx=target_qx,
                target_qy=target_qy,
            )
        )

        on_eval = (
            r4.full_solution_evaluator(
                tight,
                epsilon,
                mu_y,
            )
        )

        omega_x_on_tight = float(
            tight.p[
                0
            ]
        )

        omega_y_tight = float(
            tight.p[
                1
            ]
        )

        qmod.X_MATCH = (
            SOURCE_MATCH
        )

        source_off = (
            qmod.solve_uncoupled_qball(
                omega_x_off
            )
        )

        if source_off is None:

            raise RuntimeError(
                "Could not reconstruct OFF source Q-ball"
            )

        activation_unc = (
            qmod.solve_uncoupled_qball(
                omega_y
            )
        )

        if activation_unc is None:

            raise RuntimeError(
                "Could not reconstruct spectator Q-ball branch"
            )

        print(
            f"OFF_OMEGA_X={omega_x_off:.15e}"
        )

        print(
            f"ON_OMEGA_X_REBUILT={omega_x_on_tight:.15e}"
        )

        print(
            f"ON_OMEGA_Y_REBUILT={omega_y_tight:.15e}"
        )

        print(
            "ON_BVP_RMS="
            f"{diag_t['max_rms_residual']:.15e}"
        )

        def off_seed_arrays(
            x,
        ):

            y, yp = (
                uncoupled_source_eval(
                    source_off,
                    omega_x_off,
                    x,
                )
            )

            zero = np.zeros_like(
                y
            )

            return (
                y,
                yp,
                zero,
                zero,
            )

        def yoff_func(
            x,
        ):

            return uncoupled_source_eval(
                source_off,
                omega_x_off,
                x,
            )[
                0
            ]

        def a1_func(
            x,
        ):

            return np.asarray(
                on_eval(
                    np.asarray(
                        x,
                        dtype=float,
                    )
                )[
                    4
                ],
                dtype=float,
            )

        def ap1_func(
            x,
        ):

            return np.asarray(
                on_eval(
                    np.asarray(
                        x,
                        dtype=float,
                    )
                )[
                    5
                ],
                dtype=float,
            )

        xE = make_energy_grid()

        y0, yp0 = (
            uncoupled_source_eval(
                source_off,
                omega_x_off,
                xE,
            )
        )

        zero = np.zeros_like(
            y0
        )

        I_source_off = (
            source_energy_I(
                y0,
                yp0,
                zero,
                zero,
                omega_x_off,
                np.zeros_like(
                    y0
                ),
                chi,
                epsilon,
                xE,
            )
        )

        E_scale_J = (
            E_off_source_J
            / I_source_off
        )

        (
            yon,
            ypon,
            uon,
            upon,
            aon,
            apon,
        ) = on_eval(
            xE
        )

        f_on = (
            activation_fraction(
                aon
            )
        )

        I_source_on = (
            source_energy_I(
                yon,
                ypon,
                uon,
                upon,
                omega_x_on_tight,
                f_on,
                chi,
                epsilon,
                xE,
            )
        )

        I_y_on = (
            component_energy_I(
                aon,
                apon,
                rho_y,
                mu_y,
                omega_y_tight,
                xE,
            )
        )

        E_y_rebuilt_J = (
            E_scale_J
            * I_y_on
        )

        E_source_on_rebuilt_J = (
            E_scale_J
            * I_source_on
        )

        E_on_rebuilt_J = (
            E_scale_J
            * (
                I_source_on
                + I_y_on
            )
        )

        y_norm_rel = relerr(
            E_y_rebuilt_J,
            E_y_cert_J,
        )

        on_total_rel = relerr(
            E_on_rebuilt_J,
            E_on_total_J,
        )

        source_on_target_J = (
            E_on_total_J
            - E_y_cert_J
        )

        source_on_rel = relerr(
            E_source_on_rebuilt_J,
            source_on_target_J,
        )

        energy_norm_pass = bool(
            y_norm_rel
            <= ENERGY_NORMALIZATION_REL_TOL

            and
            on_total_rel
            <= ENERGY_NORMALIZATION_REL_TOL

            and
            source_on_rel
            <= SOURCE_ENDPOINT_REL_TOL
        )

        print(
            "\n=== STAGE C: INDEPENDENT COMMON HAMILTONIAN NORMALIZATION ==="
        )

        print(
            f"I_SOURCE_OFF={I_source_off:.15e}"
        )

        print(
            f"COMMON_ENERGY_SCALE_J={E_scale_J:.15e}"
        )

        print(
            f"I_SOURCE_ON={I_source_on:.15e}"
        )

        print(
            f"I_Y_ON={I_y_on:.15e}"
        )

        print(
            f"E_Y_REBUILT_J={E_y_rebuilt_J:.15e}"
        )

        print(
            f"E_Y_CERTIFIED_J={E_y_cert_J:.15e}"
        )

        print(
            f"E_Y_RELERR={y_norm_rel:.15e}"
        )

        print(
            "E_SOURCE_ON_REBUILT_J="
            f"{E_source_on_rebuilt_J:.15e}"
        )

        print(
            f"E_SOURCE_ON_TARGET_J={source_on_target_J:.15e}"
        )

        print(
            f"E_SOURCE_ON_RELERR={source_on_rel:.15e}"
        )

        print(
            f"E_ON_REBUILT_J={E_on_rebuilt_J:.15e}"
        )

        print(
            f"E_ON_CERTIFIED_J={E_on_total_J:.15e}"
        )

        print(
            f"E_ON_RELERR={on_total_rel:.15e}"
        )

        print(
            "COMMON_HAMILTONIAN_NORMALIZATION_PASS="
            f"{energy_norm_pass}"
        )

        def r_profile(
            x,
        ):

            rho = (
                mu_R
                * np.asarray(
                    x,
                    dtype=float,
                )
            )

            ar, aprho = (
                d3a.extended_profile(
                    activation_unc,
                    omega_y,
                    rho,
                )
            )

            return (
                np.asarray(
                    ar,
                    dtype=float,
                ),

                mu_R
                * np.asarray(
                    aprho,
                    dtype=float,
                ),
            )

        ar1, arp1 = (
            r_profile(
                xE
            )
        )

        I_R_on = (
            component_energy_I(
                ar1,
                arp1,
                rho_R,
                mu_R,
                omega_y,
                xE,
            )
        )

        E_R_rebuilt_J = (
            E_scale_J
            * I_R_on
        )

        R_scaling_rel = relerr(
            E_R_rebuilt_J,
            target_R_J,
        )

        R_stability = bool(
            eqm
            < 1.0
        )

        reservoir_scaling_pass = bool(
            R_scaling_rel
            <= RESERVOIR_SCALING_REL_TOL

            and
            R_stability
        )

        print(
            "\n=== STAGE D: SPECTATOR-R MICROSCOPIC SCALING AUDIT ==="
        )

        print(
            f"I_R_FULL={I_R_on:.15e}"
        )

        print(
            f"E_R_REBUILT_J={E_R_rebuilt_J:.15e}"
        )

        print(
            f"E_R_TARGET_J={target_R_J:.15e}"
        )

        print(
            f"E_R_SCALING_RELERR={R_scaling_rel:.15e}"
        )

        print(
            f"E_R_OVER_QMR={eqm:.15e}"
        )

        print(
            f"R_BOUND_QBALL_PASS={R_stability}"
        )

        print(
            "ENERGY_MATCHED_RESERVOIR_SCALING_PASS="
            f"{reservoir_scaling_pass}"
        )

        print(
            "\n=== STAGE E: UNSCALARIZED-BRANCH TACHYONIC THRESHOLD ===",
            flush=True,
        )

        scalar_modes = []

        for q in (
            Q_SCAN_COARSE
        ):

            lam = (
                lowest_unscalarized_scalar_mode(
                    float(
                        q
                    ),
                    a1_func,
                    yoff_func,
                    epsilon,
                    chi,
                )
            )

            scalar_modes.append(
                (
                    float(
                        q
                    ),
                    lam,
                )
            )

            print(
                f"UNSCALARIZED "
                f"q={q:.6f} "
                f"LAMBDA0={lam:+.15e}",
                flush=True,
            )

        qcrit = None

        for (
            qa,
            la,
        ), (
            qb,
            lb,
        ) in zip(
            scalar_modes[
                :-1
            ],
            scalar_modes[
                1:
            ],
        ):

            if la == 0.0:

                qcrit = (
                    qa
                )

                break

            if (
                la
                * lb
                < 0.0
            ):

                qcrit = brentq(
                    lambda qq:
                    lowest_unscalarized_scalar_mode(
                        float(
                            qq
                        ),
                        a1_func,
                        yoff_func,
                        epsilon,
                        chi,
                    ),
                    qa,
                    qb,
                    xtol=2.0e-5,
                    rtol=2.0e-5,
                )

                break

        if qcrit is None:

            raise RuntimeError(
                "No scalarization threshold found on q in [0,1]"
            )

        lambda_qcrit = (
            lowest_unscalarized_scalar_mode(
                qcrit,
                a1_func,
                yoff_func,
                epsilon,
                chi,
            )
        )

        print(
            f"SCALARIZATION_QCRIT={qcrit:.15e}"
        )

        print(
            "SCALARIZATION_QCRIT_LAMBDA="
            f"{lambda_qcrit:+.15e}"
        )

        special = [
            1.0,
            0.99,
            0.97,
            0.93,
            0.85,
            0.70,
            0.50,
            0.30,
            0.15,
            0.07,
            0.03,
            0.01,
            0.0,

            max(
                0.0,
                qcrit
                - 0.05,
            ),

            max(
                0.0,
                qcrit
                - 0.02,
            ),

            max(
                0.0,
                qcrit
                - 0.01,
            ),

            max(
                0.0,
                qcrit
                - 0.005,
            ),

            qcrit,

            min(
                1.0,
                qcrit
                + 0.005,
            ),

            min(
                1.0,
                qcrit
                + 0.01,
            ),

            min(
                1.0,
                qcrit
                + 0.02,
            ),

            min(
                1.0,
                qcrit
                + 0.05,
            ),
        ]

        q_branch = sorted(
            {
                round(
                    float(
                        value
                    ),
                    8,
                )
                for value
                in special
            },
            reverse=True,
        )

        print(
            "\n=== STAGE F: BACKWARD SCALARIZED SOURCE CONTINUATION ===",
            flush=True,
        )

        def on_seed_arrays(
            x,
        ):

            state = on_eval(
                np.asarray(
                    x,
                    dtype=float,
                )
            )

            return (
                state[
                    0
                ],
                state[
                    1
                ],
                state[
                    2
                ],
                state[
                    3
                ],
            )

        previous = None

        branch_rows = []

        for index, q in enumerate(
            q_branch
        ):

            try:

                solution = solve_source_branch(
                    q,
                    a1_func,
                    target_qx,
                    epsilon,
                    chi,
                    previous=previous,
                    seed_arrays=(
                        on_seed_arrays
                        if index == 0
                        else None
                    ),
                    omega_seed=(
                        omega_x_on_tight
                        if index == 0
                        else float(
                            previous.p[
                                0
                            ]
                        )
                    ),
                )

                previous = (
                    solution
                )

                (
                    ys,
                    yps,
                    us,
                    ups,
                ) = bvp_source_eval(
                    solution,
                    epsilon,
                    xE,
                )

                fs = activation_fraction(
                    math.sqrt(
                        max(
                            q,
                            0.0,
                        )
                    )
                    * a1_func(
                        xE
                    )
                )

                Is = source_energy_I(
                    ys,
                    yps,
                    us,
                    ups,
                    float(
                        solution.p[
                            0
                        ]
                    ),
                    fs,
                    chi,
                    epsilon,
                    xE,
                )

                u0 = float(
                    solution.sol(
                        X0
                    )[
                        2
                    ]
                )

                lam_un = (
                    lowest_unscalarized_scalar_mode(
                        q,
                        a1_func,
                        yoff_func,
                        epsilon,
                        chi,
                    )
                )

                row = {
                    "q":
                        q,

                    "success":
                        True,

                    "omega_x":
                        float(
                            solution.p[
                                0
                            ]
                        ),

                    "u0":
                        u0,

                    "I_source_scalarized":
                        Is,

                    "E_source_scalarized_J":
                        E_scale_J
                        * Is,

                    "E_source_unscalarized_J":
                        E_off_source_J,

                    "unscalarized_lambda0":
                        lam_un,

                    "bvp_rms":
                        float(
                            np.max(
                                solution.rms_residuals
                            )
                        ),

                    "nodes":
                        int(
                            solution.x.size
                        ),
                }

                print(
                    f"SCALARIZED "
                    f"q={q:.8f} "
                    f"OMEGA={row['omega_x']:.12e} "
                    f"U0={u0:+.12e} "
                    f"E_J={row['E_source_scalarized_J']:.12e} "
                    f"UN_LAMBDA={lam_un:+.6e} "
                    f"RMS={row['bvp_rms']:.3e}",
                    flush=True,
                )

            except Exception as exc:

                row = {
                    "q":
                        q,

                    "success":
                        False,

                    "error":
                        str(
                            exc
                        ),
                }

                print(
                    f"SCALARIZED "
                    f"q={q:.8f} "
                    f"FAILED={exc}",
                    flush=True,
                )

                previous = None

            branch_rows.append(
                row
            )

        branch_by_q = {
            round(
                float(
                    row[
                        "q"
                    ]
                ),
                8,
            ):
            row
            for row
            in branch_rows
            if row.get(
                "success"
            )
        }

        nontrivial = [
            row
            for row
            in branch_rows
            if (
                row.get(
                    "success"
                )

                and
                abs(
                    float(
                        row.get(
                            "u0",
                            0.0,
                        )
                    )
                )
                > 1.0e-3
            )
        ]

        q_scalar_min = min(
            (
                float(
                    row[
                        "q"
                    ]
                )
                for row
                in nontrivial
            ),
            default=float(
                "nan"
            ),
        )

        if math.isfinite(
            q_scalar_min
        ):

            branch_gap = max(
                q_scalar_min
                - qcrit,
                0.0,
            )

        else:

            branch_gap = float(
                "inf"
            )

        unstable_coverage = bool(
            math.isfinite(
                q_scalar_min
            )

            and
            q_scalar_min
            <= qcrit
            + SCALAR_BRANCH_Q_GAP_MAX
        )

        print(
            f"SCALARIZED_BRANCH_MIN_Q={q_scalar_min:.15e}"
        )

        print(
            f"SCALARIZED_TO_TACHYON_GAP={branch_gap:.15e}"
        )

        print(
            "UNSTABLE_REGION_SCALARIZED_COVERAGE_PASS="
            f"{unstable_coverage}"
        )

        print(
            "\n=== STAGE G: COMPLETE ENERGY-MATCHED ADIABATIC PATH ===",
            flush=True,
        )

        aY_full = (
            a1_func(
                xE
            )
        )

        apY_full = (
            ap1_func(
                xE
            )
        )

        (
            ar_full,
            apr_full,
        ) = r_profile(
            xE
        )

        Jyy = float(
            4.0
            * math.pi
            * np.trapezoid(
                xE
                * xE
                * aY_full
                * aY_full,
                xE,
            )
        )

        Jyr = float(
            4.0
            * math.pi
            * np.trapezoid(
                xE
                * xE
                * aY_full
                * ar_full,
                xE,
            )
        )

        Jy4 = float(
            4.0
            * math.pi
            * np.trapezoid(
                xE
                * xE
                * aY_full**4,
                xE,
            )
        )

        Jy2r2 = float(
            4.0
            * math.pi
            * np.trapezoid(
                xE
                * xE
                * aY_full**2
                * ar_full**2,
                xE,
            )
        )

        overlap_gain = (
            mass_ratio
            * Jyr
            / max(
                Jyy,
                1.0e-300,
            )
        )

        old_gate_J = float(
            d1[
                "best_candidate"
            ][
                "gate_energy_primary_J"
            ]
        )

        old_barrier_J = float(
            d1[
                "best_candidate"
            ][
                "barrier_energy_J"
            ]
        )

        mapped_gate_J = (
            old_gate_J
            / max(
                overlap_gain
                * overlap_gain,
                1.0e-300,
            )
        )

        mapped_barrier_half_J = (
            old_barrier_J
            * mass_ratio
            * mass_ratio
            * Jy2r2
            / max(
                Jy4,
                1.0e-300,
            )
        )

        print(
            f"Y_R_MODE_OVERLAP_GAIN={overlap_gain:.15e}"
        )

        print(
            f"MAPPED_GATE_ENERGY_1S_J={mapped_gate_J:.15e}"
        )

        print(
            "MAPPED_STABILIZER_BARRIER_HALF_J="
            f"{mapped_barrier_half_J:.15e}"
        )

        path_rows = []

        path_q_values = sorted(
            {
                float(
                    row[
                        "q"
                    ]
                )
                for row
                in branch_rows
            }
        )

        for q in (
            path_q_values
        ):

            lam_un = (
                lowest_unscalarized_scalar_mode(
                    q,
                    a1_func,
                    yoff_func,
                    epsilon,
                    chi,
                )
            )

            scalar_row = branch_by_q.get(
                round(
                    q,
                    8,
                )
            )

            scalar_E = None
            scalar_u0 = 0.0

            if scalar_row is not None:

                scalar_E = float(
                    scalar_row[
                        "E_source_scalarized_J"
                    ]
                )

                scalar_u0 = abs(
                    float(
                        scalar_row[
                            "u0"
                        ]
                    )
                )

            if (
                scalar_E is not None
                and
                scalar_u0
                > 1.0e-3
            ):

                choose_scalar = bool(
                    lam_un
                    < 0.0

                    or
                    scalar_E
                    < E_off_source_J
                )

            else:

                choose_scalar = False

            if (
                lam_un
                < 0.0
                and
                not choose_scalar
            ):

                source_path_valid = (
                    False
                )

                E_source = float(
                    "nan"
                )

                branch_name = (
                    "MISSING_STABLE_SCALARIZED"
                )

            else:

                source_path_valid = (
                    True
                )

                E_source = (
                    scalar_E
                    if choose_scalar
                    else E_off_source_J
                )

                branch_name = (
                    "SCALARIZED"
                    if choose_scalar
                    else "UNSCALARIZED"
                )

            aq = (
                math.sqrt(
                    max(
                        q,
                        0.0,
                    )
                )
                * aY_full
            )

            aqp = (
                math.sqrt(
                    max(
                        q,
                        0.0,
                    )
                )
                * apY_full
            )

            pr = max(
                1.0
                - q,
                0.0,
            )

            arq = (
                math.sqrt(
                    pr
                )
                * ar_full
            )

            arqp = (
                math.sqrt(
                    pr
                )
                * apr_full
            )

            IYq = component_energy_I(
                aq,
                aqp,
                rho_y,
                mu_y,
                omega_y_tight,
                xE,
            )

            IRq = component_energy_I(
                arq,
                arqp,
                rho_R,
                mu_R,
                omega_y,
                xE,
            )

            EYq = (
                E_scale_J
                * IYq
            )

            ERq = (
                E_scale_J
                * IRq
            )

            barrier_q = (
                mapped_barrier_half_J
                * 4.0
                * q
                * (
                    1.0
                    - q
                )
            )

            if source_path_valid:

                total = (
                    E_source
                    + EYq
                    + ERq
                    + barrier_q
                )

            else:

                total = float(
                    "nan"
                )

            row = {
                "q":
                    q,

                "QY_fraction":
                    q,

                "QR_fraction":
                    1.0
                    - q,

                "Qtotal_fraction":
                    1.0,

                "unscalarized_lambda0":
                    lam_un,

                "source_branch":
                    branch_name,

                "source_path_valid":
                    source_path_valid,

                "E_source_J":
                    E_source,

                "E_Y_J":
                    EYq,

                "E_R_J":
                    ERq,

                "E_stabilizer_J":
                    barrier_q,

                "E_total_path_J":
                    total,
            }

            path_rows.append(
                row
            )

            print(
                f"PATH "
                f"q={q:.8f} "
                f"BRANCH={branch_name} "
                f"E_SOURCE={E_source:.12e} "
                f"E_Y={EYq:.12e} "
                f"E_R={ERq:.12e} "
                f"E_BAR={barrier_q:.6e} "
                f"E_TOTAL={total:.12e}",
                flush=True,
            )

        path_rows = sorted(
            path_rows,
            key=lambda row:
            row[
                "q"
            ],
        )

        all_path_valid = all(
            bool(
                row[
                    "source_path_valid"
                ]
            )
            for row
            in path_rows
        )

        qvals = np.array(
            [
                row[
                    "q"
                ]
                for row
                in path_rows
            ],
            dtype=float,
        )

        evals = np.array(
            [
                row[
                    "E_total_path_J"
                ]
                for row
                in path_rows
            ],
            dtype=float,
        )

        if (
            not all_path_valid
            or
            not np.all(
                np.isfinite(
                    evals
                )
            )
        ):

            path_barrier_J = float(
                "nan"
            )

            endpoint_rel = float(
                "inf"
            )

            max_chirp_hz = float(
                "inf"
            )

        else:

            endpoint_rel = relerr(
                evals[
                    0
                ],
                evals[
                    -1
                ],
            )

            path_barrier_J = float(
                np.max(
                    evals
                )
                - max(
                    evals[
                        0
                    ],
                    evals[
                        -1
                    ],
                )
            )

            dEdq = np.gradient(
                evals,
                qvals,
                edge_order=2,
            )

            chirp_eV = (
                dEdq
                / Q_star
                / J_PER_EV
            )

            chirp_hz = (
                chirp_eV
                / H_EV_S
            )

            max_chirp_hz = float(
                np.max(
                    np.abs(
                        chirp_hz
                    )
                )
            )

            for (
                row,
                de,
                ce,
                ch,
            ) in zip(
                path_rows,
                dEdq,
                chirp_eV,
                chirp_hz,
                strict=True,
            ):

                row[
                    "dE_dq_J"
                ] = float(
                    de
                )

                row[
                    "chemical_detuning_eV"
                ] = float(
                    ce
                )

                row[
                    "chirp_Hz"
                ] = float(
                    ch
                )

        endpoint_equality_pass = bool(
            endpoint_rel
            <= ENDPOINT_EQUALITY_REL_TOL
        )

        finite_path_pass = bool(
            all_path_valid

            and
            math.isfinite(
                path_barrier_J
            )

            and
            path_barrier_J
            >= -1.0e6
        )

        print(
            f"PATH_ENDPOINT_RELERR={endpoint_rel:.15e}"
        )

        print(
            f"REVERSIBLE_PATH_BARRIER_J={path_barrier_J:.15e}"
        )

        print(
            f"MAX_ABS_PATH_CHIRP_HZ={max_chirp_hz:.15e}"
        )

        print(
            f"ENDPOINT_ENERGY_MATCH_PASS={endpoint_equality_pass}"
        )

        print(
            f"FINITE_ADIABATIC_PATH_PASS={finite_path_pass}"
        )

        sigma = float(
            d1[
                "best_candidate"
            ][
                "sigma"
            ]
        )

        mS_eV = (
            sigma
            * m_y_eV
        )

        mS_hz = (
            mS_eV
            / H_EV_S
        )

        mX_eV = float(
            d0[
                "model"
            ][
                "m_x_eV"
            ]
        )

        mphi_eV = (
            epsilon
            * mX_eV
        )

        mphi_hz = (
            mphi_eV
            / H_EV_S
        )

        envelope_hz = (
            1.0
            / PRIMARY_SWITCH_S
        )

        S_radiation_closed = bool(
            max_chirp_hz
            < mS_hz
        )

        source_scalar_envelope_closed = bool(
            envelope_hz
            < mphi_hz
        )

        print(
            "\n=== STAGE H: MULTISCALE SWITCHING / RADIATION GATE ==="
        )

        print(
            f"M_S_EV={mS_eV:.15e}"
        )

        print(
            f"M_S_THRESHOLD_HZ={mS_hz:.15e}"
        )

        print(
            f"M_PHI_EV={mphi_eV:.15e}"
        )

        print(
            f"M_PHI_THRESHOLD_HZ={mphi_hz:.15e}"
        )

        print(
            f"SOURCE_ENVELOPE_HZ={envelope_hz:.15e}"
        )

        print(
            "FUNDAMENTAL_S_RADIATION_CLOSED="
            f"{S_radiation_closed}"
        )

        print(
            "SCALAR_ENVELOPE_RADIATION_CLOSED="
            f"{source_scalar_envelope_closed}"
        )

        tol_hz = float(
            d1[
                "resonant_999_tolerance_Hz"
            ]
        )

        forward = rwa_transfer(
            PRIMARY_SWITCH_S,
            tol_hz,
            reverse=False,
        )

        reverse = rwa_transfer(
            PRIMARY_SWITCH_S,
            tol_hz,
            reverse=True,
        )

        rwa_pass = bool(
            forward[
                "fidelity"
            ]
            >= RWA_FIDELITY_MIN

            and
            reverse[
                "fidelity"
            ]
            >= RWA_FIDELITY_MIN

            and
            forward[
                "norm_error"
            ]
            <= RWA_NORM_ERR_MAX

            and
            reverse[
                "norm_error"
            ]
            <= RWA_NORM_ERR_MAX
        )

        print(
            "RWA_FORWARD_FIDELITY="
            f"{forward['fidelity']:.15e}"
        )

        print(
            "RWA_REVERSE_FIDELITY="
            f"{reverse['fidelity']:.15e}"
        )

        print(
            "RWA_FORWARD_NORM_ERROR="
            f"{forward['norm_error']:.15e}"
        )

        print(
            "RWA_REVERSE_NORM_ERROR="
            f"{reverse['norm_error']:.15e}"
        )

        print(
            "BIDIRECTIONAL_CHARGE_TRANSFER_ENVELOPE_PASS="
            f"{rwa_pass}"
        )

        print(
            "ENDPOINT_NET_SPATIAL_MOMENTUM_CHANGE="
            "0_BY_SPHERICAL_COLOCATION"
        )

        print(
            "HIGHER_HARMONIC_AND_NONLINEAR_RADIATION_"
            "DEFERRED_TO_031F=YES"
        )

        branch_pass = bool(
            unstable_coverage

            and
            math.isfinite(
                qcrit
            )

            and
            0.0
            < qcrit
            < 1.0
        )

        inherited_bounded_mixer = bool(
            d1[
                "decision"
            ][
                "preflight_pass"
            ]

            and
            float(
                d1[
                    "best_candidate"
                ][
                    "lambda"
                ]
            )
            > 0.0
        )

        prerequisites = bool(
            energy_norm_pass

            and
            reservoir_scaling_pass

            and
            branch_pass

            and
            endpoint_equality_pass

            and
            finite_path_pass

            and
            inherited_bounded_mixer

            and
            math.isfinite(
                mapped_gate_J
            )

            and
            math.isfinite(
                mapped_barrier_half_J
            )

            and
            S_radiation_closed

            and
            source_scalar_envelope_closed

            and
            rwa_pass
        )

        print(
            "\n=== STAGE I: DECISION ==="
        )

        print(
            f"ENERGY_PROVENANCE_PASS={energy_norm_pass}"
        )

        print(
            f"ENERGY_MATCHED_R_PASS={reservoir_scaling_pass}"
        )

        print(
            f"SCALARIZATION_BRANCH_PASS={branch_pass}"
        )

        print(
            f"ENDPOINT_EQUALITY_PASS={endpoint_equality_pass}"
        )

        print(
            f"ADIABATIC_PATH_PASS={finite_path_pass}"
        )

        print(
            "INHERITED_BOUNDED_MIXER_PASS="
            f"{inherited_bounded_mixer}"
        )

        print(
            "MULTISCALE_RADIATION_PREFLIGHT_PASS="
            f"{S_radiation_closed and source_scalar_envelope_closed}"
        )

        print(
            f"BIDIRECTIONAL_TRANSFER_PASS={rwa_pass}"
        )

        if prerequisites:

            classification = (
                "GREEN_D3D2_ENERGY_MATCHED_ADIABATIC_"
                "MULTISCALE_TRANSFER_SOURCE_RESPONSE_CLOSEOUT"
            )

            next_action = (
                "031E_FULL_PHYSICAL_METRIC_EINSTEIN_BACKREACTION"
            )

            full_d3d = (
                True
            )

        else:

            classification = (
                "YELLOW_OR_RED_D3D2_ENERGY_MATCHED_"
                "TRANSFER_CLOSEOUT_FAILED"
            )

            next_action = (
                "DIAGNOSE_ONLY_FAILED_D3D2_ENERGY_"
                "BRANCH_PATH_OR_RADIATION_SUBGATE"
            )

            full_d3d = (
                False
            )

        print(
            f"031D3D2_CLASSIFICATION={classification}"
        )

        print(
            "FULL_D3D_ADIABATIC_MULTISCALE_CLOSED="
            f"{full_d3d}"
        )

        print(
            "FULL_CARRIER_RESOLVED_RADIAL_PDE_SOLVED=False"
        )

        print(
            "NONLINEAR_SWITCHING_STABILITY_CLOSED=False"
        )

        print(
            "FULL_EINSTEIN_BACKREACTION_CLOSED=False"
        )

        print(
            "EFT_NATURALNESS_EMPIRICAL_CLOSURE=False"
        )

        print(
            "PRACTICAL_DEVICE=NO"
        )

        print(
            f"NEXT={next_action}"
        )

        summary = {
            "classification":
                classification,

            "next":
                next_action,

            "claim_class":
                "ADIABATIC_MULTISCALE_FIXED_CHARGE_TRANSFER_CLOSEOUT",

            "energy_matched_reservoir": {
                "m_Y_eV":
                    m_y_eV,

                "m_R_eV":
                    m_R_eV,

                "mass_ratio":
                    mass_ratio,

                "mu_R":
                    mu_R,

                "rho_R":
                    rho_R,

                "target_R_energy_J":
                    target_R_J,

                "rebuilt_R_energy_J":
                    E_R_rebuilt_J,

                "relative_error":
                    R_scaling_rel,

                "E_over_Qm":
                    eqm,

                "pass":
                    reservoir_scaling_pass,
            },

            "hamiltonian_provenance": {
                "common_energy_scale_J":
                    E_scale_J,

                "Y_rebuilt_J":
                    E_y_rebuilt_J,

                "Y_certified_J":
                    E_y_cert_J,

                "Y_relerr":
                    y_norm_rel,

                "source_ON_rebuilt_J":
                    E_source_on_rebuilt_J,

                "source_ON_target_J":
                    source_on_target_J,

                "source_ON_relerr":
                    source_on_rel,

                "full_ON_rebuilt_J":
                    E_on_rebuilt_J,

                "full_ON_certified_J":
                    E_on_total_J,

                "full_ON_relerr":
                    on_total_rel,

                "pass":
                    energy_norm_pass,
            },

            "scalarization": {
                "qcrit":
                    qcrit,

                "lambda_at_qcrit":
                    lambda_qcrit,

                "scalarized_min_q":
                    q_scalar_min,

                "branch_gap":
                    branch_gap,

                "coverage_pass":
                    unstable_coverage,
            },

            "controller_remap": {
                "mode_overlap_gain":
                    overlap_gain,

                "mapped_gate_energy_1s_J":
                    mapped_gate_J,

                "mapped_stabilizer_barrier_half_J":
                    mapped_barrier_half_J,

                "inherited_boundedness_pass":
                    inherited_bounded_mixer,
            },

            "path": {
                "endpoint_relerr":
                    endpoint_rel,

                "reversible_barrier_J":
                    path_barrier_J,

                "max_abs_chirp_Hz":
                    max_chirp_hz,

                "endpoint_match_pass":
                    endpoint_equality_pass,

                "finite_path_pass":
                    finite_path_pass,
            },

            "radiation": {
                "mS_eV":
                    mS_eV,

                "mS_threshold_Hz":
                    mS_hz,

                "mphi_eV":
                    mphi_eV,

                "mphi_threshold_Hz":
                    mphi_hz,

                "source_envelope_Hz":
                    envelope_hz,

                "fundamental_S_closed":
                    S_radiation_closed,

                "scalar_envelope_closed":
                    source_scalar_envelope_closed,

                "higher_harmonics_deferred_031F":
                    True,
            },

            "rwa": {
                "test_detuning_Hz":
                    tol_hz,

                "forward":
                    forward,

                "reverse":
                    reverse,

                "pass":
                    rwa_pass,
            },

            "decision": {
                "prerequisites":
                    prerequisites,

                "full_D3D_adiabatic_multiscale_closed":
                    full_d3d,

                "full_carrier_resolved_radial_PDE_solved":
                    False,
            },

            "claim_limits": [
                (
                    "GREEN closes D3D only at the adiabatic "
                    "multiscale flat-space effective-theory level."
                ),
                (
                    "The spectator R mass is one globally fixed "
                    "parameter, not a spatially prescribed coupling."
                ),
                (
                    "The X+phi source response is solved "
                    "self-consistently along the prescribed conserved-"
                    "charge population path."
                ),
                (
                    "The Y/R population path is an explicit finite-"
                    "energy collective path, not a carrier-resolved "
                    "nonlinear PDE trajectory."
                ),
                (
                    "Only leading single-particle radiation thresholds "
                    "and the slow scalar envelope are closed here."
                ),
                (
                    "Higher-harmonic, nonlinear fragmentation and "
                    "multiparticle radiation remain for 031F."
                ),
                (
                    "Einstein backreaction remains for 031E."
                ),
                (
                    "EFT/naturalness and empirical fifth-force/EP/PPN "
                    "closure remain for 031F."
                ),
                (
                    "No practical antigravity device is established."
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

        branch_fields = sorted(
            {
                key
                for row
                in branch_rows
                for key
                in row
            }
        )

        with OUT_BRANCH.open(
            "w",
            newline="",
        ) as handle:

            writer = csv.DictWriter(
                handle,
                fieldnames=branch_fields,
            )

            writer.writeheader()

            writer.writerows(
                branch_rows
            )

        path_fields = sorted(
            {
                key
                for row
                in path_rows
                for key
                in row
            }
        )

        with OUT_PATH.open(
            "w",
            newline="",
        ) as handle:

            writer = csv.DictWriter(
                handle,
                fieldnames=path_fields,
            )

            writer.writeheader()

            writer.writerows(
                path_rows
            )

        print(
            f"SUMMARY_JSON={OUT_JSON}"
        )

        print(
            f"PATH_CSV={OUT_PATH}"
        )

        print(
            f"BRANCH_CSV={OUT_BRANCH}"
        )

    finally:

        qmod.X_MATCH = (
            old_xmatch
        )

        d3a.X_MATCH = (
            old_d3a_match
        )


if __name__ == "__main__":
    main()
