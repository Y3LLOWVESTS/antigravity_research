"""
031D3B
======

Full microscopic ON-state realization for the independent global-U(1)
metric-activation architecture.

This is the first run that solves simultaneously:

    X Q-ball source       y(x)
    scalar-metric field   u(x)=phi/M_c
    activation Q-ball     a(x)=|Y|/V

while fixing BOTH conserved charges Q_X and Q_Y.

Correct D3 theory
-----------------

    f(a) = 1 - exp(-a^2/2)

    A_X(u,a) = exp[-f(a) u^2/2]

The exotic X source therefore obeys

    y'' + 2y'/x
      = A_X y/(1+y^2) - Omega_X^2 y

    u'' + 2u'/x
      = epsilon^2 u
        - chi^2 f A_X W_X(y) u.

The independent activation Q-ball obeys

    a'' + 2a'/x
      = mu^2 [
            a/(1+a^2)
            - Omega_Y^2 a
        ]
        - (1/(2 rho_Y))
          u^2 A_X W_X(y) f'(a),

where

    mu     = m_A/m_X
    rho_Y  = (V/F)^2.

The second term is the exact reciprocal source reaction implied by
A_X(u,a).

Charges
-------

    I_QX
      = 4 pi Omega_X integral x^2 y^2 dx

and, with rho=m_A r=mu x,

    I_QY
      = 4 pi Omega_Y mu^3 integral x^2 a^2 dx.

Omega_X and Omega_Y are BVP parameters fixed by the declared charges.

Ordinary matter is NOT used to generate the source solution because the
correct D3A-R2 calculation found its reaction on Y to be ~3.4e-16.

Its physical metric is evaluated afterward as

    A_m =
      exp[+ f(a) phi^2/(2 M_m^2)].

Numerical continuation
----------------------

At t=0 use

    f_t = 1

in the X/phi equations and remove the reciprocal X->Y source term.

This is exactly the independently reconstructed scalarized source plus the
independent activation Q-ball.

Continue through

    f_t = 1 - t(1-f)

and multiply the reciprocal Y source by t.

Only t=1 is the physical D3 theory.

Claims possible from GREEN
--------------------------
- full microscopic coupled ON field exists;
- both U(1) charges are conserved;
- source/activation reciprocity is included;
- positive activation Hamiltonian is counted;
- finite-payload physical metric remains outward;
- domain convergence and dense residual checks pass.

Still open:
- complete coupled perturbative spectrum;
- nonlinear stability/fission;
- activation charge injection/removal;
- switching barrier/reset/power/radiation;
- Einstein/full physical-metric backreaction;
- final radiative naturalness and empirical closure.

OFF state is in the Q_Y=0 charge sector, not the same Q_Y sector.
No practical-device claim.
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

from scipy.integrate import cumulative_trapezoid, solve_bvp


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results" / "data"

QBALL_SOURCE = (
    SIM / "031b2a_global_qball_activated_scalar_control.py"
)

D3A_SOURCE = (
    SIM / "031d3a_u1_metric_activation_capacity.py"
)

ROBUST_SUMMARY = (
    DATA / "031c96_operating_margin_robustness_summary.json"
)

LOW_SUMMARY = (
    DATA / "031d1r2_lowbranch_offstate_hessian_summary.json"
)

D3AR_SUMMARY = (
    DATA / "031d3ar_metric_eft_payload_summary.json"
)

D3AR2_SUMMARY = (
    DATA / "031d3ar2_physical_metric_summary.json"
)

OUT_JSON = (
    DATA / "031d3b_full_coupled_activation_summary.json"
)

OUT_HOMOTOPY = (
    DATA / "031d3b_homotopy_scan.csv"
)

OUT_DOMAIN = (
    DATA / "031d3b_domain_scan.csv"
)


X_SOURCE_MATCH = 80.0

X0 = 1.0e-5

HOMOTOPY_VALUES = (
    0.0,
    0.10,
    0.25,
    0.50,
    0.75,
    1.00,
)

DOMAIN_VALUES = (
    500.0,
    700.0,
    900.0,
)

BVP_TOL_HOMOTOPY = 2.0e-5
BVP_TOL_FINAL = 6.0e-6
MAX_NODES = 65_000

Q_REL_MAX = 3.0e-6

MAX_BVP_RMS = 3.0e-5
MAX_DENSE_NORMALIZED_RESIDUAL = 3.0e-4

DOMAIN_OMEGA_REL_MAX = 1.0e-3
DOMAIN_CENTER_REL_MAX = 5.0e-3
DOMAIN_ENERGY_REL_MAX = 1.0e-2

MIN_SOURCE_ACTIVATION_F = 0.999

MIN_PAYLOAD_ACCELERATION_RATIO = 0.98
MAX_PAYLOAD_ACCELERATION_RATIO = 1.02

MAX_ACTIVATION_ENERGY_FRACTION = 0.10

MAX_SOURCE_INVENTORY_REL_SHIFT = 0.03

HBARC_EV_M = 1.973269804e-7
J_PER_GEV = 1.602176634e-10


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


def relerr(a: float, b: float) -> float:
    return abs(a - b) / max(
        abs(a),
        abs(b),
        1.0e-300,
    )


def W(field):
    return (
        0.5
        * np.log1p(
            np.asarray(
                field,
                dtype=float,
            )**2
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


def activation_fraction_prime(a):
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


def make_grid(xmax: float):
    pieces = [
        np.linspace(
            X0,
            min(
                100.0,
                xmax,
            ),
            1400,
        )
    ]

    if xmax > 100.0:
        pieces.append(
            np.linspace(
                100.0,
                min(
                    300.0,
                    xmax,
                ),
                1200,
            )
        )

    if xmax > 300.0:
        pieces.append(
            np.linspace(
                300.0,
                xmax,
                max(
                    800,
                    int(
                        (xmax - 300.0)
                        * 2.0
                    ),
                ),
            )
        )

    return np.unique(
        np.concatenate(
            pieces
        )
    )


def tail_charge_x(
    amplitude: float,
    omega: float,
    k: float,
    xmax: float,
):
    return (
        4.0
        * math.pi
        * omega
        * amplitude**2
        * xmax**2
        / (
            2.0
            * k
        )
    )


def tail_charge_y(
    amplitude: float,
    omega: float,
    mu: float,
    k: float,
    xmax: float,
):
    return (
        4.0
        * math.pi
        * omega
        * mu**3
        * amplitude**2
        * xmax**2
        / (
            2.0
            * k
        )
    )


def main() -> None:
    print(
        "=== 031D3B FULL FIXED-QX,QY MICROSCOPIC ACTIVATION ==="
    )

    print(
        "FULL_X_PHI_Y_COUPLED_ON_FIELD=YES"
    )

    print(
        "FIXED_QX=YES"
    )

    print(
        "FIXED_QY=YES"
    )

    print(
        "SOURCE_ACTIVATION_RECIPROCITY_INCLUDED=YES"
    )

    print(
        "ORDINARY_PAYLOAD_REACTION_IN_SOURCE_BVP=NO"
    )

    print(
        "REASON_PAYLOAD_REACTION_PREVIOUSLY_BOUNDED="
        "3P44E_MINUS16"
    )

    print(
        "OFF_STATE_SAME_QY=NO"
    )

    print(
        "OFF_STATE_REQUIRES_QY_ZERO_OR_RESERVOIR=YES"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    for path in (
        QBALL_SOURCE,
        D3A_SOURCE,
        ROBUST_SUMMARY,
        LOW_SUMMARY,
        D3AR_SUMMARY,
        D3AR2_SUMMARY,
    ):
        require(path)

    robust = json.loads(
        ROBUST_SUMMARY.read_text()
    )

    low = json.loads(
        LOW_SUMMARY.read_text()
    )

    d3ar = json.loads(
        D3AR_SUMMARY.read_text()
    )

    d3ar2 = json.loads(
        D3AR2_SUMMARY.read_text()
    )

    if not str(
        d3ar2.get(
            "classification",
            "",
        )
    ).startswith(
        "GREEN_D3AR2"
    ):
        raise RuntimeError(
            "031D3A-R2 is not GREEN"
        )

    primary = d3ar.get(
        "primary"
    )

    if primary is None:
        raise RuntimeError(
            "Missing D3A-R primary candidate"
        )

    candidate = robust[
        "candidate"
    ]

    operating = robust[
        "interior_20pct_margin_point"
    ]

    quadrature = robust[
        "quadrature"
    ][
        "high_order_result"
    ]

    nominal_geometry = next(
        row
        for row in robust[
            "geometry_scan"
        ]
        if row[
            "label"
        ] == "nominal"
    )

    omega_x_seed = float(
        candidate[
            "omega"
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

    m_x_gev = float(
        candidate[
            "m_x_gev_derived"
        ]
    )

    m_x_ev = (
        m_x_gev
        * 1.0e9
    )

    F_gev = float(
        quadrature[
            "F_gev"
        ]
    )

    F_ev = (
        F_gev
        * 1.0e9
    )

    M_c_gev = (
        F_gev
        / chi
    )

    M_m_gev = float(
        d3ar2[
            "reconstructed"
        ][
            "M_m_GeV"
        ]
    )

    gamma_m = (
        M_c_gev
        / M_m_gev
    )**2

    operating_energy_j = float(
        operating[
            "energy_J"
        ]
    )

    target_qx = float(
        low[
            "target_I_Q"
        ]
    )

    omega_y_seed = float(
        primary[
            "omega_activation"
        ]
    )

    mu = float(
        primary[
            "mu_mA_over_mX"
        ]
    )

    m_a_ev = float(
        primary[
            "m_A_eV"
        ]
    )

    V_ev = float(
        primary[
            "V_required_eV"
        ]
    )

    V_gev = (
        V_ev
        / 1.0e9
    )

    rho_y = (
        V_ev
        / F_ev
    )**2

    pre_activation_energy_j = (
        float(
            primary[
                "activation_energy_J"
            ]
        )
    )

    pre_total_j = (
        operating_energy_j
        + pre_activation_energy_j
    )

    qmod = load_module(
        "qball031d3b",
        QBALL_SOURCE,
    )

    d3a = load_module(
        "d3a031d3b",
        D3A_SOURCE,
    )

    old_xmatch = float(
        qmod.X_MATCH
    )

    qmod.X_MATCH = X_SOURCE_MATCH

    try:
        print(
            "\n=== STAGE A: INDEPENDENT FIELD RECONSTRUCTION ==="
        )

        source_seed = (
            qmod.solve_uncoupled_qball(
                omega_x_seed
            )
        )

        if source_seed is None:
            raise RuntimeError(
                "Failed source Q-ball seed"
            )

        source = qmod.solve_coupled(
            source_seed,
            omega_x_seed,
            epsilon,
            chi,
            previous=None,
        )

        if source is None:
            raise RuntimeError(
                "Failed scalarized source reconstruction"
            )

        activation = (
            qmod.solve_uncoupled_qball(
                omega_y_seed
            )
        )

        if activation is None:
            raise RuntimeError(
                "Failed activation Q-ball reconstruction"
            )

        activation_integrals = (
            d3a.activation_integrals(
                activation,
                omega_y_seed,
            )
        )

        target_qy = float(
            activation_integrals[
                "I_Q"
            ]
        )

        inherited_activation_ratio = float(
            activation_integrals[
                "E_over_Qm"
            ]
        )

        inherited_physical_qy = (
            target_qy
            * V_ev**2
            / m_a_ev**2
        )

        declared_physical_qy = float(
            primary[
                "activation_charge"
            ]
        )

        physical_qy_relerr = relerr(
            inherited_physical_qy,
            declared_physical_qy,
        )

        print(
            f"TARGET_I_QX="
            f"{target_qx:.15e}"
        )

        print(
            f"TARGET_I_QY="
            f"{target_qy:.15e}"
        )

        print(
            f"TARGET_PHYSICAL_QY="
            f"{inherited_physical_qy:.15e}"
        )

        print(
            f"D3AR_PHYSICAL_QY="
            f"{declared_physical_qy:.15e}"
        )

        print(
            f"PHYSICAL_QY_PROVENANCE_RELERR="
            f"{physical_qy_relerr:.15e}"
        )

        print(
            f"OMEGA_X_SEED="
            f"{omega_x_seed:.15e}"
        )

        print(
            f"OMEGA_Y_SEED="
            f"{omega_y_seed:.15e}"
        )

        print(
            f"MU_MA_OVER_MX="
            f"{mu:.15e}"
        )

        print(
            f"RHO_Y_V2_OVER_F2="
            f"{rho_y:.15e}"
        )

        print(
            f"INHERITED_ACTIVATION_E_OVER_QM="
            f"{inherited_activation_ratio:.15e}"
        )

        # ----------------------------------------------------------
        # Initial field extensions.
        # ----------------------------------------------------------

        source_boundary = source.sol(
            X_SOURCE_MATCH
        )

        y80 = float(
            source_boundary[
                0
            ]
        )

        u80 = float(
            source_boundary[
                2
            ]
        )

        ky_seed = math.sqrt(
            1.0
            - omega_x_seed**2
        )

        def independent_source_fields(x):
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
                    y80
                    * X_SOURCE_MATCH
                    / xo
                    * np.exp(
                        -ky_seed
                        * (
                            xo
                            - X_SOURCE_MATCH
                        )
                    )
                )

                uo = (
                    u80
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
                    -ky_seed
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

        def independent_activation_fields(x):
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
                    omega_y_seed,
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

        # ----------------------------------------------------------
        # Coupled BVP.
        # ----------------------------------------------------------

        def equations_factory(
            t_value,
        ):
            def equations(
                x,
                state,
                parameters,
            ):
                omega_x = float(
                    parameters[
                        0
                    ]
                )

                omega_y = float(
                    parameters[
                        1
                    ]
                )

                y = state[
                    0
                ]

                u = state[
                    2
                ]

                a = state[
                    4
                ]

                f = activation_fraction(
                    a
                )

                fp = activation_fraction_prime(
                    a
                )

                # Numerical homotopy:
                #
                # t=0 -> inherited scalarized source, independent Y.
                # t=1 -> physical D3 theory.
                f_t = (
                    1.0
                    - t_value
                    * (
                        1.0
                        - f
                    )
                )

                A_x = np.exp(
                    -0.5
                    * f_t
                    * u**2
                )

                W_x = W(
                    y
                )

                reciprocal_y_source = (
                    - t_value
                    * 0.5
                    / rho_y
                    * u**2
                    * A_x
                    * W_x
                    * fp
                )

                return np.vstack(
                    (
                        state[
                            1
                        ],

                        A_x
                        * y
                        / (
                            1.0
                            + y**2
                        )
                        - omega_x**2
                        * y
                        - 2.0
                        * state[
                            1
                        ]
                        / x,

                        state[
                            3
                        ],

                        epsilon**2
                        * u
                        - chi**2
                        * f_t
                        * A_x
                        * W_x
                        * u
                        - 2.0
                        * state[
                            3
                        ]
                        / x,

                        state[
                            5
                        ],

                        mu**2
                        * (
                            a
                            / (
                                1.0
                                + a**2
                            )
                            - omega_y**2
                            * a
                        )
                        + reciprocal_y_source
                        - 2.0
                        * state[
                            5
                        ]
                        / x,

                        4.0
                        * math.pi
                        * omega_x
                        * x**2
                        * y**2,

                        4.0
                        * math.pi
                        * omega_y
                        * mu**3
                        * x**2
                        * a**2,
                    )
                )

            return equations

        def boundary_factory(
            xmax,
        ):
            def boundary(
                left,
                right,
                parameters,
            ):
                omega_x = float(
                    parameters[
                        0
                    ]
                )

                omega_y = float(
                    parameters[
                        1
                    ]
                )

                kx = math.sqrt(
                    max(
                        1.0
                        - omega_x**2,
                        1.0e-10,
                    )
                )

                ky = (
                    mu
                    * math.sqrt(
                        max(
                            1.0
                            - omega_y**2,
                            1.0e-10,
                        )
                    )
                )

                qx_tail = tail_charge_x(
                    float(
                        right[
                            0
                        ]
                    ),
                    omega_x,
                    kx,
                    xmax,
                )

                qy_tail = tail_charge_y(
                    float(
                        right[
                            4
                        ]
                    ),
                    omega_y,
                    mu,
                    ky,
                    xmax,
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
                            5
                        ],

                        left[
                            6
                        ],

                        left[
                            7
                        ],

                        right[
                            1
                        ]
                        + (
                            kx
                            + 1.0
                            / xmax
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
                            / xmax
                        )
                        * right[
                            2
                        ],

                        right[
                            5
                        ]
                        + (
                            ky
                            + 1.0
                            / xmax
                        )
                        * right[
                            4
                        ],

                        right[
                            6
                        ]
                        + qx_tail
                        - target_qx,

                        right[
                            7
                        ]
                        + qy_tail
                        - target_qy,
                    ),
                    dtype=float,
                )

            return boundary

        def first_guess(
            x,
        ):
            y, yp, u, up = (
                independent_source_fields(
                    x
                )
            )

            a, ap = (
                independent_activation_fields(
                    x
                )
            )

            qx_prime = (
                4.0
                * math.pi
                * omega_x_seed
                * x**2
                * y**2
            )

            qy_prime = (
                4.0
                * math.pi
                * omega_y_seed
                * mu**3
                * x**2
                * a**2
            )

            qx = np.concatenate(
                (
                    np.array(
                        [
                            0.0
                        ]
                    ),
                    cumulative_trapezoid(
                        qx_prime,
                        x,
                    ),
                )
            )

            qy = np.concatenate(
                (
                    np.array(
                        [
                            0.0
                        ]
                    ),
                    cumulative_trapezoid(
                        qy_prime,
                        x,
                    ),
                )
            )

            return np.vstack(
                (
                    y,
                    yp,
                    u,
                    up,
                    a,
                    ap,
                    qx,
                    qy,
                )
            )

        def solve_bvp_stage(
            x,
            guess,
            params,
            t_value,
            tolerance,
        ):
            return solve_bvp(
                equations_factory(
                    t_value
                ),
                boundary_factory(
                    float(
                        x[
                            -1
                        ]
                    )
                ),
                x,
                guess,
                p=np.asarray(
                    params,
                    dtype=float,
                ),
                tol=tolerance,
                max_nodes=MAX_NODES,
                verbose=0,
            )

        print(
            "\n=== STAGE B: COUPLING HOMOTOPY ==="
        )

        x = make_grid(
            DOMAIN_VALUES[
                0
            ]
        )

        guess = first_guess(
            x
        )

        params = np.array(
            (
                omega_x_seed,
                omega_y_seed,
            ),
            dtype=float,
        )

        homotopy_rows = []

        solution = None

        for t_value in HOMOTOPY_VALUES:
            solution = solve_bvp_stage(
                x,
                guess,
                params,
                t_value,
                BVP_TOL_HOMOTOPY,
            )

            if not solution.success:
                raise RuntimeError(
                    "D3B homotopy failed at "
                    f"t={t_value}: "
                    f"{solution.message}"
                )

            params = np.array(
                solution.p,
                dtype=float,
            )

            x = solution.x
            guess = solution.y

            center = solution.sol(
                X0
            )

            outer = solution.sol(
                x[
                    -1
                ]
            )

            omega_x = float(
                params[
                    0
                ]
            )

            omega_y = float(
                params[
                    1
                ]
            )

            kx = math.sqrt(
                max(
                    1.0
                    - omega_x**2,
                    1.0e-10,
                )
            )

            ky = (
                mu
                * math.sqrt(
                    max(
                        1.0
                        - omega_y**2,
                        1.0e-10,
                    )
                )
            )

            qx_total = (
                float(
                    outer[
                        6
                    ]
                )
                + tail_charge_x(
                    float(
                        outer[
                            0
                        ]
                    ),
                    omega_x,
                    kx,
                    float(
                        x[
                            -1
                        ]
                    ),
                )
            )

            qy_total = (
                float(
                    outer[
                        7
                    ]
                )
                + tail_charge_y(
                    float(
                        outer[
                            4
                        ]
                    ),
                    omega_y,
                    mu,
                    ky,
                    float(
                        x[
                            -1
                        ]
                    ),
                )
            )

            row = {
                "t":
                    float(
                        t_value
                    ),

                "omega_x":
                    omega_x,

                "omega_y":
                    omega_y,

                "y0":
                    float(
                        center[
                            0
                        ]
                    ),

                "u0":
                    float(
                        center[
                            2
                        ]
                    ),

                "a0":
                    float(
                        center[
                            4
                        ]
                    ),

                "f0":
                    float(
                        activation_fraction(
                            center[
                                4
                            ]
                        )
                    ),

                "QX_relerr":
                    relerr(
                        qx_total,
                        target_qx,
                    ),

                "QY_relerr":
                    relerr(
                        qy_total,
                        target_qy,
                    ),

                "nodes":
                    int(
                        solution.x.size
                    ),

                "max_bvp_rms":
                    float(
                        np.max(
                            solution.rms_residuals
                        )
                    ),
            }

            homotopy_rows.append(
                row
            )

            print(
                f"HOMOTOPY "
                f"T={t_value:.2f} "
                f"OMEGA_X={omega_x:.12e} "
                f"OMEGA_Y={omega_y:.12e} "
                f"U0={row['u0']:.12e} "
                f"A0={row['a0']:.12e} "
                f"F0={row['f0']:.12e} "
                f"QX_REL={row['QX_relerr']:.6e} "
                f"QY_REL={row['QY_relerr']:.6e} "
                f"NODES={row['nodes']} "
                f"RMS={row['max_bvp_rms']:.6e}"
            )

        # ----------------------------------------------------------
        # Physical t=1 domain continuation.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE C: PHYSICAL T=1 DOMAIN CONVERGENCE ==="
        )

        def extend_solution(
            previous,
            new_x,
        ):
            old_xmax = float(
                previous.x[
                    -1
                ]
            )

            old_params = np.asarray(
                previous.p,
                dtype=float,
            )

            omega_x = float(
                old_params[
                    0
                ]
            )

            omega_y = float(
                old_params[
                    1
                ]
            )

            kx = math.sqrt(
                max(
                    1.0
                    - omega_x**2,
                    1.0e-10,
                )
            )

            ky = (
                mu
                * math.sqrt(
                    max(
                        1.0
                        - omega_y**2,
                        1.0e-10,
                    )
                )
            )

            state = np.zeros(
                (
                    8,
                    len(
                        new_x
                    ),
                ),
                dtype=float,
            )

            inside = (
                new_x
                <= old_xmax
            )

            state[
                :,
                inside
            ] = previous.sol(
                new_x[
                    inside
                ]
            )

            outside = (
                ~inside
            )

            if np.any(
                outside
            ):
                xo = new_x[
                    outside
                ]

                boundary = previous.sol(
                    old_xmax
                )

                yb = float(
                    boundary[
                        0
                    ]
                )

                ub = float(
                    boundary[
                        2
                    ]
                )

                ab = float(
                    boundary[
                        4
                    ]
                )

                qxb = float(
                    boundary[
                        6
                    ]
                )

                qyb = float(
                    boundary[
                        7
                    ]
                )

                yout = (
                    yb
                    * old_xmax
                    / xo
                    * np.exp(
                        -kx
                        * (
                            xo
                            - old_xmax
                        )
                    )
                )

                uout = (
                    ub
                    * old_xmax
                    / xo
                    * np.exp(
                        -epsilon
                        * (
                            xo
                            - old_xmax
                        )
                    )
                )

                aout = (
                    ab
                    * old_xmax
                    / xo
                    * np.exp(
                        -ky
                        * (
                            xo
                            - old_xmax
                        )
                    )
                )

                state[
                    0,
                    outside
                ] = yout

                state[
                    1,
                    outside
                ] = (
                    -kx
                    -1.0 / xo
                ) * yout

                state[
                    2,
                    outside
                ] = uout

                state[
                    3,
                    outside
                ] = (
                    -epsilon
                    -1.0 / xo
                ) * uout

                state[
                    4,
                    outside
                ] = aout

                state[
                    5,
                    outside
                ] = (
                    -ky
                    -1.0 / xo
                ) * aout

                state[
                    6,
                    outside
                ] = (
                    qxb
                    + 4.0
                    * math.pi
                    * omega_x
                    * yb**2
                    * old_xmax**2
                    * (
                        1.0
                        - np.exp(
                            -2.0
                            * kx
                            * (
                                xo
                                - old_xmax
                            )
                        )
                    )
                    / (
                        2.0
                        * kx
                    )
                )

                state[
                    7,
                    outside
                ] = (
                    qyb
                    + 4.0
                    * math.pi
                    * omega_y
                    * mu**3
                    * ab**2
                    * old_xmax**2
                    * (
                        1.0
                        - np.exp(
                            -2.0
                            * ky
                            * (
                                xo
                                - old_xmax
                            )
                        )
                    )
                    / (
                        2.0
                        * ky
                    )
                )

            return state

        def energy_ledger(
            sol,
        ):
            xmax = float(
                sol.x[
                    -1
                ]
            )

            sample = np.linspace(
                X0,
                xmax,
                80_000,
            )

            state = sol.sol(
                sample
            )

            y = np.asarray(
                state[
                    0
                ],
                dtype=float,
            )

            yp = np.asarray(
                state[
                    1
                ],
                dtype=float,
            )

            u = np.asarray(
                state[
                    2
                ],
                dtype=float,
            )

            up = np.asarray(
                state[
                    3
                ],
                dtype=float,
            )

            a = np.asarray(
                state[
                    4
                ],
                dtype=float,
            )

            ap = np.asarray(
                state[
                    5
                ],
                dtype=float,
            )

            omega_x = float(
                sol.p[
                    0
                ]
            )

            omega_y = float(
                sol.p[
                    1
                ]
            )

            f = activation_fraction(
                a
            )

            A_x = np.exp(
                -0.5
                * f
                * u**2
            )

            W_x = W(
                y
            )

            W_y = W(
                a
            )

            source_exact_density = (
                0.5
                * yp**2
                + 0.5
                * omega_x**2
                * y**2
                + A_x
                * W_x
            )

            source_inventory_density = (
                0.5
                * yp**2
                + 0.5
                * omega_x**2
                * y**2
                + W_x
            )

            scalar_density = (
                (
                    0.5
                    * up**2
                    + 0.5
                    * epsilon**2
                    * u**2
                )
                / chi**2
            )

            activation_density = (
                rho_y
                * (
                    0.5
                    * ap**2
                    + mu**2
                    * (
                        0.5
                        * omega_y**2
                        * a**2
                        + W_y
                    )
                )
            )

            measure = (
                4.0
                * math.pi
                * sample**2
            )

            I_source_exact = float(
                np.trapezoid(
                    measure
                    * source_exact_density,
                    sample,
                )
            )

            I_source_inventory = float(
                np.trapezoid(
                    measure
                    * source_inventory_density,
                    sample,
                )
            )

            I_scalar = float(
                np.trapezoid(
                    measure
                    * scalar_density,
                    sample,
                )
            )

            I_activation = float(
                np.trapezoid(
                    measure
                    * activation_density,
                    sample,
                )
            )

            energy_scale_j = (
                F_gev**2
                / m_x_gev
                * J_PER_GEV
            )

            source_scalar_exact_j = (
                (
                    I_source_exact
                    + I_scalar
                )
                * energy_scale_j
            )

            source_scalar_inventory_j = (
                (
                    I_source_inventory
                    + I_scalar
                )
                * energy_scale_j
            )

            activation_j = (
                I_activation
                * energy_scale_j
            )

            exact_total_j = (
                source_scalar_exact_j
                + activation_j
            )

            conservative_total_j = (
                source_scalar_inventory_j
                + activation_j
            )

            return {
                "source_scalar_exact_J":
                    source_scalar_exact_j,

                "source_scalar_inventory_J":
                    source_scalar_inventory_j,

                "activation_J":
                    activation_j,

                "exact_total_J":
                    exact_total_j,

                "conservative_total_J":
                    conservative_total_j,
            }

        domain_rows = []

        physical = solution

        for index, xmax in enumerate(
            DOMAIN_VALUES
        ):
            new_x = make_grid(
                xmax
            )

            if (
                abs(
                    physical.x[
                        -1
                    ]
                    - xmax
                )
                < 1.0e-10
            ):
                new_guess = physical.sol(
                    new_x
                )

            else:
                new_guess = extend_solution(
                    physical,
                    new_x,
                )

            physical = solve_bvp_stage(
                new_x,
                new_guess,
                physical.p,
                1.0,
                BVP_TOL_FINAL,
            )

            if not physical.success:
                raise RuntimeError(
                    "D3B physical-domain solve failed "
                    f"at XMAX={xmax}: "
                    f"{physical.message}"
                )

            center = physical.sol(
                X0
            )

            outer = physical.sol(
                xmax
            )

            omega_x = float(
                physical.p[
                    0
                ]
            )

            omega_y = float(
                physical.p[
                    1
                ]
            )

            kx = math.sqrt(
                1.0
                - omega_x**2
            )

            ky = (
                mu
                * math.sqrt(
                    1.0
                    - omega_y**2
                )
            )

            qx_total = (
                float(
                    outer[
                        6
                    ]
                )
                + tail_charge_x(
                    float(
                        outer[
                            0
                        ]
                    ),
                    omega_x,
                    kx,
                    xmax,
                )
            )

            qy_total = (
                float(
                    outer[
                        7
                    ]
                )
                + tail_charge_y(
                    float(
                        outer[
                            4
                        ]
                    ),
                    omega_y,
                    mu,
                    ky,
                    xmax,
                )
            )

            ledger = energy_ledger(
                physical
            )

            row = {
                "xmax":
                    xmax,

                "omega_x":
                    omega_x,

                "omega_y":
                    omega_y,

                "y0":
                    float(
                        center[
                            0
                        ]
                    ),

                "u0":
                    float(
                        center[
                            2
                        ]
                    ),

                "a0":
                    float(
                        center[
                            4
                        ]
                    ),

                "f0":
                    float(
                        activation_fraction(
                            center[
                                4
                            ]
                        )
                    ),

                "QX_relerr":
                    relerr(
                        qx_total,
                        target_qx,
                    ),

                "QY_relerr":
                    relerr(
                        qy_total,
                        target_qy,
                    ),

                "activation_GJ":
                    ledger[
                        "activation_J"
                    ]
                    / 1.0e9,

                "conservative_total_GJ":
                    ledger[
                        "conservative_total_J"
                    ]
                    / 1.0e9,

                "nodes":
                    int(
                        physical.x.size
                    ),

                "max_bvp_rms":
                    float(
                        np.max(
                            physical.rms_residuals
                        )
                    ),
            }

            domain_rows.append(
                row
            )

            print(
                f"DOMAIN "
                f"XMAX={xmax:.1f} "
                f"OMEGA_X={omega_x:.12e} "
                f"OMEGA_Y={omega_y:.12e} "
                f"U0={row['u0']:.12e} "
                f"A0={row['a0']:.12e} "
                f"QX_REL={row['QX_relerr']:.6e} "
                f"QY_REL={row['QY_relerr']:.6e} "
                f"ACT_GJ={row['activation_GJ']:.9f} "
                f"TOTAL_GJ="
                f"{row['conservative_total_GJ']:.9f} "
                f"RMS={row['max_bvp_rms']:.6e}"
            )

        # ----------------------------------------------------------
        # Dense independent residual reconstruction.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE D: DENSE EQUATION RESIDUAL RECONSTRUCTION ==="
        )

        xmax = float(
            physical.x[
                -1
            ]
        )

        dense_x = np.linspace(
            X0,
            xmax,
            30_000,
        )

        dense_state = physical.sol(
            dense_x
        )

        dense_derivative = physical.sol(
            dense_x,
            1,
        )

        dense_rhs = equations_factory(
            1.0
        )(
            dense_x,
            dense_state,
            physical.p,
        )

        normalized_residual = (
            np.abs(
                dense_derivative
                - dense_rhs
            )
            /
            (
                1.0
                + np.abs(
                    dense_rhs
                )
            )
        )

        dense_residual_max = float(
            np.max(
                normalized_residual
            )
        )

        print(
            f"DENSE_NORMALIZED_RESIDUAL_MAX="
            f"{dense_residual_max:.15e}"
        )

        print(
            f"BVP_RMS_RESIDUAL_MAX="
            f"{float(np.max(physical.rms_residuals)):.15e}"
        )

        # ----------------------------------------------------------
        # Source activation coverage.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE E: SOURCE / PAYLOAD PHYSICAL RESPONSE ==="
        )

        productive_x = np.linspace(
            X0,
            X_SOURCE_MATCH,
            5000,
        )

        productive_state = physical.sol(
            productive_x
        )

        productive_y = np.asarray(
            productive_state[
                0
            ],
            dtype=float,
        )

        productive_a = np.asarray(
            productive_state[
                4
            ],
            dtype=float,
        )

        source_mask = (
            W(
                productive_y
            )
            >= 1.0e-4
            * np.max(
                W(
                    productive_y
                )
            )
        )

        source_f_min = float(
            np.min(
                activation_fraction(
                    productive_a[
                        source_mask
                    ]
                )
            )
        )

        print(
            f"SOURCE_PRODUCTIVE_F_MIN="
            f"{source_f_min:.15e}"
        )

        source_shift_m = float(
            operating[
                "shift_m"
            ]
        )

        payload_center_m = float(
            nominal_geometry[
                "payload_center_m"
            ]
        )

        payload_radius_m = float(
            nominal_geometry[
                "payload_radius_m"
            ]
        )

        center_from_source_m = abs(
            payload_center_m
            - source_shift_m
        )

        x_length_m = (
            HBARC_EV_M
            / m_x_ev
        )

        x_near = (
            (
                center_from_source_m
                - payload_radius_m
            )
            / x_length_m
        )

        x_far = (
            (
                center_from_source_m
                + payload_radius_m
            )
            / x_length_m
        )

        x_payload = np.linspace(
            x_near,
            x_far,
            2001,
        )

        coupled_payload = physical.sol(
            x_payload
        )

        baseline_payload = source.sol(
            x_payload
        )

        u = np.asarray(
            coupled_payload[
                2
            ],
            dtype=float,
        )

        up = np.asarray(
            coupled_payload[
                3
            ],
            dtype=float,
        )

        a = np.asarray(
            coupled_payload[
                4
            ],
            dtype=float,
        )

        ap = np.asarray(
            coupled_payload[
                5
            ],
            dtype=float,
        )

        ub = np.asarray(
            baseline_payload[
                2
            ],
            dtype=float,
        )

        upb = np.asarray(
            baseline_payload[
                3
            ],
            dtype=float,
        )

        f = activation_fraction(
            a
        )

        fp = activation_fraction_prime(
            a
        )

        df_dx = (
            fp
            * ap
        )

        dlogA_final = (
            gamma_m
            * (
                f
                * u
                * up
                + 0.5
                * u**2
                * df_dx
            )
        )

        dlogA_baseline = (
            gamma_m
            * ub
            * upb
        )

        acceleration_ratio = (
            np.abs(
                dlogA_final
            )
            /
            np.maximum(
                np.abs(
                    dlogA_baseline
                ),
                1.0e-300,
            )
        )

        payload_ratio_min = float(
            np.min(
                acceleration_ratio
            )
        )

        payload_ratio_max = float(
            np.max(
                acceleration_ratio
            )
        )

        payload_f_min = float(
            np.min(
                f
            )
        )

        outward_sign_pass = bool(
            np.all(
                dlogA_final
                < 0.0
            )
        )

        print(
            f"PAYLOAD_F_MIN="
            f"{payload_f_min:.15e}"
        )

        print(
            f"PAYLOAD_ACCELERATION_RATIO_MIN="
            f"{payload_ratio_min:.15e}"
        )

        print(
            f"PAYLOAD_ACCELERATION_RATIO_MAX="
            f"{payload_ratio_max:.15e}"
        )

        print(
            f"PAYLOAD_OUTWARD_SIGN_PASS="
            f"{outward_sign_pass}"
        )

        # ----------------------------------------------------------
        # Final energy and convergence.
        # ----------------------------------------------------------

        final_ledger = energy_ledger(
            physical
        )

        activation_fraction_of_source = (
            final_ledger[
                "activation_J"
            ]
            / operating_energy_j
        )

        source_inventory_rel_shift = relerr(
            final_ledger[
                "source_scalar_inventory_J"
            ],
            operating_energy_j,
        )

        conservative_total_gj = (
            final_ledger[
                "conservative_total_J"
            ]
            / 1.0e9
        )

        omega_x_values = np.array(
            [
                row[
                    "omega_x"
                ]
                for row in domain_rows
            ]
        )

        omega_y_values = np.array(
            [
                row[
                    "omega_y"
                ]
                for row in domain_rows
            ]
        )

        u0_values = np.array(
            [
                row[
                    "u0"
                ]
                for row in domain_rows
            ]
        )

        a0_values = np.array(
            [
                row[
                    "a0"
                ]
                for row in domain_rows
            ]
        )

        energy_values = np.array(
            [
                row[
                    "conservative_total_GJ"
                ]
                for row in domain_rows
            ]
        )

        def relative_spread(values):
            return (
                float(
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

        omega_x_spread = relative_spread(
            omega_x_values
        )

        omega_y_spread = relative_spread(
            omega_y_values
        )

        u0_spread = relative_spread(
            u0_values
        )

        a0_spread = relative_spread(
            a0_values
        )

        energy_spread = relative_spread(
            energy_values
        )

        domain_pass = bool(
            omega_x_spread
            <= DOMAIN_OMEGA_REL_MAX
            and
            omega_y_spread
            <= DOMAIN_OMEGA_REL_MAX
            and
            u0_spread
            <= DOMAIN_CENTER_REL_MAX
            and
            a0_spread
            <= DOMAIN_CENTER_REL_MAX
            and
            energy_spread
            <= DOMAIN_ENERGY_REL_MAX
        )

        final_domain = domain_rows[
            -1
        ]

        charge_pass = bool(
            final_domain[
                "QX_relerr"
            ]
            <= Q_REL_MAX
            and
            final_domain[
                "QY_relerr"
            ]
            <= Q_REL_MAX
        )

        residual_pass = bool(
            final_domain[
                "max_bvp_rms"
            ]
            <= MAX_BVP_RMS
            and
            dense_residual_max
            <= MAX_DENSE_NORMALIZED_RESIDUAL
        )

        source_activation_pass = bool(
            source_f_min
            >= MIN_SOURCE_ACTIVATION_F
        )

        payload_pass = bool(
            payload_f_min
            >= MIN_SOURCE_ACTIVATION_F
            and
            payload_ratio_min
            >= MIN_PAYLOAD_ACCELERATION_RATIO
            and
            payload_ratio_max
            <= MAX_PAYLOAD_ACCELERATION_RATIO
            and
            outward_sign_pass
        )

        energy_pass = bool(
            activation_fraction_of_source
            <= MAX_ACTIVATION_ENERGY_FRACTION
            and
            source_inventory_rel_shift
            <= MAX_SOURCE_INVENTORY_REL_SHIFT
            and
            final_ledger[
                "conservative_total_J"
            ]
            > 0.0
        )

        frequency_pass = bool(
            0.0
            < float(
                physical.p[
                    0
                ]
            )
            < 1.0
            and
            0.0
            < float(
                physical.p[
                    1
                ]
            )
            < 1.0
        )

        off_source_pass = bool(
            low[
                "source_slope_stable"
            ]
            and
            low[
                "qball_bound_pass"
            ]
        )

        off_scalar_pass = bool(
            epsilon**2
            > 0.0
        )

        off_qy0_structure_pass = bool(
            off_source_pass
            and
            off_scalar_pass
        )

        print(
            "\n=== STAGE F: FINAL MICROSCOPIC EXISTENCE DECISION ==="
        )

        print(
            f"OMEGA_X_DOMAIN_REL_SPREAD="
            f"{omega_x_spread:.15e}"
        )

        print(
            f"OMEGA_Y_DOMAIN_REL_SPREAD="
            f"{omega_y_spread:.15e}"
        )

        print(
            f"U0_DOMAIN_REL_SPREAD="
            f"{u0_spread:.15e}"
        )

        print(
            f"A0_DOMAIN_REL_SPREAD="
            f"{a0_spread:.15e}"
        )

        print(
            f"ENERGY_DOMAIN_REL_SPREAD="
            f"{energy_spread:.15e}"
        )

        print(
            f"DOMAIN_CONVERGENCE_PASS="
            f"{domain_pass}"
        )

        print(
            f"FIXED_QX_QY_PASS="
            f"{charge_pass}"
        )

        print(
            f"DENSE_RESIDUAL_PASS="
            f"{residual_pass}"
        )

        print(
            f"SOURCE_ACTIVATION_PASS="
            f"{source_activation_pass}"
        )

        print(
            f"FINITE_PAYLOAD_RESPONSE_PASS="
            f"{payload_pass}"
        )

        print(
            f"ACTIVATION_ENERGY_GJ="
            f"{final_ledger['activation_J']/1.0e9:.12f}"
        )

        print(
            f"SOURCE_SCALAR_CONSERVATIVE_GJ="
            f"{final_ledger['source_scalar_inventory_J']/1.0e9:.12f}"
        )

        print(
            f"FULL_CONSERVATIVE_ON_INVENTORY_GJ="
            f"{conservative_total_gj:.12f}"
        )

        print(
            f"PRECOUPLING_REFERENCE_TOTAL_GJ="
            f"{pre_total_j/1.0e9:.12f}"
        )

        print(
            f"SOURCE_INVENTORY_REL_SHIFT="
            f"{source_inventory_rel_shift:.15e}"
        )

        print(
            f"ACTIVATION_ENERGY_FRACTION_OF_SOURCE="
            f"{activation_fraction_of_source:.15e}"
        )

        print(
            f"ENERGY_GATE_PASS="
            f"{energy_pass}"
        )

        print(
            f"FREQUENCY_BOUND_PASS="
            f"{frequency_pass}"
        )

        print(
            f"OFF_QY_ZERO_STRUCTURE_PASS="
            f"{off_qy0_structure_pass}"
        )

        print(
            "OFF_STATE_SAME_QY=False"
        )

        green = bool(
            domain_pass
            and
            charge_pass
            and
            residual_pass
            and
            source_activation_pass
            and
            payload_pass
            and
            energy_pass
            and
            frequency_pass
            and
            off_qy0_structure_pass
        )

        if green:
            classification = (
                "GREEN_D3B_FULL_FIXED_QX_QY_"
                "COUPLED_MICROSCOPIC_ON_FIELD_EXISTS"
            )

            next_action = (
                "031D3C_COUPLED_LINEAR_STABILITY_"
                "PLUS_QY_SWITCHING_RESERVOIR_RESET_GATE"
            )

        else:
            classification = (
                "YELLOW_OR_RED_D3B_FULL_COUPLED_"
                "MICROSCOPIC_EXISTENCE_NOT_CERTIFIED"
            )

            next_action = (
                "DIAGNOSE_ONLY_FAILED_D3B_SUBGATE"
            )

        print(
            f"031D3B_CLASSIFICATION="
            f"{classification}"
        )

        print(
            f"NEXT={next_action}"
        )

        print(
            "COUPLED_LINEAR_STABILITY_CLOSED=NO"
        )

        print(
            "QY_CHARGE_INJECTION_REMOVAL_CLOSED=NO"
        )

        print(
            "SWITCHING_RESET_POWER_CLOSED=NO"
        )

        print(
            "RADIATION_CLOSED=NO"
        )

        print(
            "FULL_METRIC_BACKREACTION_CLOSED=NO"
        )

        print(
            "RADIATIVE_NATURALNESS_CLOSED=NO"
        )

        print(
            "EMPIRICAL_CLOSURE=NO"
        )

        print(
            "PRACTICAL_DEVICE=NO"
        )

        summary = {
            "classification":
                classification,

            "next":
                next_action,

            "theory": {
                "f":
                    "1-exp(-a^2/2)",

                "source_metric_factor":
                    "A_X=exp[-f(a)u^2/2]",

                "matter_metric":
                    (
                        "A_m=exp[+f(a)phi^2/"
                        "(2 M_m^2)]"
                    ),

                "off_same_QY":
                    False,
            },

            "charges": {
                "target_I_QX":
                    target_qx,

                "target_I_QY":
                    target_qy,

                "physical_QY":
                    inherited_physical_qy,

                "physical_QY_provenance_relerr":
                    physical_qy_relerr,
            },

            "homotopy_rows":
                homotopy_rows,

            "domain_rows":
                domain_rows,

            "convergence": {
                "omega_x_rel_spread":
                    omega_x_spread,

                "omega_y_rel_spread":
                    omega_y_spread,

                "u0_rel_spread":
                    u0_spread,

                "a0_rel_spread":
                    a0_spread,

                "energy_rel_spread":
                    energy_spread,

                "dense_normalized_residual_max":
                    dense_residual_max,

                "pass":
                    domain_pass
                    and residual_pass,
            },

            "payload": {
                "source_f_min":
                    source_f_min,

                "payload_f_min":
                    payload_f_min,

                "acceleration_ratio_min":
                    payload_ratio_min,

                "acceleration_ratio_max":
                    payload_ratio_max,

                "outward_sign_pass":
                    outward_sign_pass,

                "pass":
                    payload_pass,
            },

            "energy": {
                "activation_J":
                    final_ledger[
                        "activation_J"
                    ],

                "source_scalar_conservative_J":
                    final_ledger[
                        "source_scalar_inventory_J"
                    ],

                "full_conservative_on_J":
                    final_ledger[
                        "conservative_total_J"
                    ],

                "precoupling_reference_J":
                    pre_total_j,

                "activation_fraction_of_source":
                    activation_fraction_of_source,

                "source_inventory_rel_shift":
                    source_inventory_rel_shift,
            },

            "off_state": {
                "QY":
                    0.0,

                "same_QY_as_ON":
                    False,

                "source_qball_pass":
                    off_source_pass,

                "bare_scalar_mass2_hat":
                    epsilon**2,

                "structure_pass":
                    off_qy0_structure_pass,
            },

            "claim_limits": [
                (
                    "GREEN establishes a static microscopic coupled "
                    "ON field at fixed Q_X and fixed Q_Y."
                ),
                (
                    "The OFF vacuum lies in the Q_Y=0 sector, so "
                    "activation requires charge injection/removal or "
                    "a reservoir."
                ),
                (
                    "Ordinary-payload reaction is not included in the "
                    "BVP because D3A-R2 bounded it at ~3.4e-16."
                ),
                (
                    "Complete coupled perturbative and nonlinear "
                    "stability remain open."
                ),
                (
                    "Switching/reset/power/radiation remain open."
                ),
                (
                    "Full Einstein/physical-metric backreaction, "
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

        homotopy_fields = sorted(
            {
                key
                for row in homotopy_rows
                for key in row
            }
        )

        with OUT_HOMOTOPY.open(
            "w",
            newline="",
        ) as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=homotopy_fields,
            )

            writer.writeheader()
            writer.writerows(
                homotopy_rows
            )

        domain_fields = sorted(
            {
                key
                for row in domain_rows
                for key in row
            }
        )

        with OUT_DOMAIN.open(
            "w",
            newline="",
        ) as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=domain_fields,
            )

            writer.writeheader()
            writer.writerows(
                domain_rows
            )

        print(
            f"SUMMARY_JSON={OUT_JSON}"
        )

        print(
            f"HOMOTOPY_CSV={OUT_HOMOTOPY}"
        )

        print(
            f"DOMAIN_CSV={OUT_DOMAIN}"
        )

    finally:
        qmod.X_MATCH = old_xmatch


if __name__ == "__main__":
    main()
