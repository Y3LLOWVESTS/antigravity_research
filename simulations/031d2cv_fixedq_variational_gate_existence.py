"""
031D2C-V — fixed-Q variational existence gate
==============================================

Purpose
-------
Repeated solve_bvp formulations failed before giving a physics result.

This run changes numerical method, not physics.

A static stable configuration must be a stationary local minimum of the
fixed-Noether-charge energy.  Eliminate Omega analytically using

    Q = Omega S[y]

    S[y] = 4 pi integral x^2 y^2 dx

so

    Omega = Q/S[y].

The fixed-Q ON functional is

    I_ON =
        4 pi integral x^2 [
            1/2 y'^2
            + A(u) W(y)
            + (1/2 u'^2 + 1/2 eps^2 u^2)/chi^2
            + rho_s {
                1/2 z'^2
                + a2/4 (z^2-1)^2
                + 1/2 b2 u^2 z^2
              }
        ] dx
        + Q^2/(2 S[y]).

where

    A(u) = exp(-u^2/2)
    W(y) = 1/2 log(1+y^2)
    rho_s = v_s^2/F^2.

Variation gives exactly

    y'' + 2y'/x =
        A y/(1+y^2) - Omega^2 y

    u'' + 2u'/x =
        (eps^2 + delta2 z^2)u
        - chi^2 A W u

    z'' + 2z'/x =
        [a2(z^2-1) + b2 u^2] z

because

    chi^2 rho_s b2 = delta2.

The finite-dimensional functional is minimized directly with analytic
gradients and physical box constraints.

This avoids:
- collocation singular Jacobians;
- direct resolution of exponentially tiny gate amplitudes;
- solving Omega as an extra BVP parameter.

Scientific interpretation
-------------------------
GREEN means:
- an ON local minimum exists at the required conserved Q;
- source, scalar and gate all react;
- positive gate gradient/potential/interaction energy is counted;
- the result survives domain and grid refinement;
- payload-region scalar gradient survives;
- exact OFF branch remains linearly stabilized.

It does NOT establish:
- full coupled perturbative spectrum;
- nonlinear switching/nucleation;
- reset or radiation cost;
- Einstein/full physical-metric closure;
- EFT/naturalness or empirical closure;
- a practical device.

STOP RULE
---------
If all declared ON-biased seeds collapse to the OFF basin, do not continue
BVP repairs of this canonical s^2 phi^2 gate.  Demote the tested gate and
rerank 031D activation mechanisms.
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
from scipy.optimize import minimize


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results" / "data"

QBALL_SOURCE = (
    SIM / "031b2a_global_qball_activated_scalar_control.py"
)

ROBUST_SUMMARY = (
    DATA / "031c96_operating_margin_robustness_summary.json"
)

LOW_SUMMARY = (
    DATA / "031d1r2_lowbranch_offstate_hessian_summary.json"
)

D1HR_SUMMARY = (
    DATA / "031d1hr_highbranch_certificate_summary.json"
)

OUT_JSON = (
    DATA / "031d2cv_fixedq_variational_summary.json"
)

OUT_DOMAIN = (
    DATA / "031d2cv_variational_domain_scan.csv"
)

OUT_SEED = (
    DATA / "031d2cv_multiseed_scan.csv"
)


# ---------------------------------------------------------------------------
# Fixed theory / candidate
# ---------------------------------------------------------------------------

X_MATCH = 80.0
X0_SOURCE = 1.0e-5

G_S = 3.0e-16
M_S_EV = 2.0719332942e-7

STABILIZATION_MARGIN = 1.20

# Domain and grid sequence.
DOMAIN_SPECS = (
    (400.0, 0.30),
    (500.0, 0.30),
    (600.0, 0.30),
    (600.0, 0.20),
)

# Independent ON-biased first-domain seeds.
U_SEED_FACTORS = (
    0.85,
    1.00,
    1.15,
)

Y_MAX = 20.0
U_MAX = 5.0

MAXITER_Z = 1000
MAXITER_UZ = 1400
MAXITER_ALL = 2200

GTOL = 1.0e-7
FTOL = 1.0e-13

PROJECTED_GRADIENT_MAX = 3.0e-4

ON_U0_MIN = 0.20
ON_Z0_MAX = 5.0e-2

Q_REL_TOL = 1.0e-12

DOMAIN_OMEGA_REL_MAX = 8.0e-4
DOMAIN_U0_REL_MAX = 8.0e-3
DOMAIN_ENERGY_REL_MAX = 2.0e-2

GRID_OMEGA_REL_MAX = 5.0e-4
GRID_U0_REL_MAX = 5.0e-3
GRID_ENERGY_REL_MAX = 1.0e-2

PAYLOAD_GRADIENT_RATIO_MIN = 0.90

BASELINE_RECON_REL_MAX = 5.0e-3

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

    module = importlib.util.module_from_spec(spec)
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
            str(key): builtin(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [
            builtin(item)
            for item in value
        ]

    return value


def relerr(a: float, b: float) -> float:
    return abs(a - b) / max(
        abs(a),
        abs(b),
        1.0e-300,
    )


def make_grid(rmax: float, h_target: float):
    intervals = int(
        math.ceil(
            rmax / h_target
        )
    )

    h = rmax / intervals

    r = np.linspace(
        0.0,
        rmax,
        intervals + 1,
    )

    return r, h


def integration_geometry(
    r: np.ndarray,
    h: float,
):
    weights = np.full(
        len(r),
        h,
        dtype=float,
    )

    weights[0] *= 0.5
    weights[-1] *= 0.5

    node = (
        4.0
        * math.pi
        * weights
        * r**2
    )

    rmid = (
        0.5
        * (
            r[:-1]
            + r[1:]
        )
    )

    edge = (
        4.0
        * math.pi
        * rmid**2
        / h
    )

    return node, edge


def add_edge_energy_gradient(
    field: np.ndarray,
    edge: np.ndarray,
    coefficient: float,
    gradient: np.ndarray,
):
    difference = np.diff(
        field
    )

    scaled = (
        coefficient
        * edge
        * difference
    )

    energy = (
        0.5
        * coefficient
        * float(
            np.sum(
                edge
                * difference**2
            )
        )
    )

    gradient[:-1] -= scaled
    gradient[1:] += scaled

    return energy


def full_energy_gradient(
    y: np.ndarray,
    u: np.ndarray,
    z: np.ndarray,
    r: np.ndarray,
    h: float,
    target_q: float,
    epsilon: float,
    chi: float,
    rho_gate: float,
    a2: float,
    b2: float,
):
    node, edge = integration_geometry(
        r,
        h,
    )

    gy = np.zeros_like(y)
    gu = np.zeros_like(u)
    gz = np.zeros_like(z)

    # ---------------------------------------------------------------
    # Gradients
    # ---------------------------------------------------------------

    e_y_grad = add_edge_energy_gradient(
        y,
        edge,
        1.0,
        gy,
    )

    e_u_grad = add_edge_energy_gradient(
        u,
        edge,
        1.0 / chi**2,
        gu,
    )

    e_z_grad = add_edge_energy_gradient(
        z,
        edge,
        rho_gate,
        gz,
    )

    # ---------------------------------------------------------------
    # Q-ball/source potential
    # ---------------------------------------------------------------

    A = np.exp(
        -0.5 * u**2
    )

    W = (
        0.5
        * np.log1p(
            y**2
        )
    )

    source_potential = (
        A * W
    )

    e_source_potential = float(
        np.sum(
            node
            * source_potential
        )
    )

    gy += (
        node
        * A
        * y
        / (
            1.0
            + y**2
        )
    )

    gu += (
        node
        * (
            -u
            * A
            * W
        )
    )

    # ---------------------------------------------------------------
    # Exact fixed-Q kinetic term
    # ---------------------------------------------------------------

    S = float(
        np.sum(
            node
            * y**2
        )
    )

    if (
        not math.isfinite(S)
        or S <= 1.0e-12
    ):
        return (
            1.0e100,
            gy,
            gu,
            gz,
            math.nan,
        )

    omega = (
        target_q
        / S
    )

    e_q = (
        0.5
        * target_q**2
        / S
    )

    gy += (
        -target_q**2
        / S**2
        * node
        * y
    )

    # ---------------------------------------------------------------
    # Scalar potential
    # ---------------------------------------------------------------

    scalar_mass_density = (
        0.5
        * epsilon**2
        * u**2
        / chi**2
    )

    e_scalar_mass = float(
        np.sum(
            node
            * scalar_mass_density
        )
    )

    gu += (
        node
        * epsilon**2
        * u
        / chi**2
    )

    # ---------------------------------------------------------------
    # Gate potential + reciprocal interaction
    # ---------------------------------------------------------------

    gate_potential_density = (
        rho_gate
        * (
            a2
            / 4.0
            * (
                z**2
                - 1.0
            )**2
        )
    )

    interaction_density = (
        rho_gate
        * 0.5
        * b2
        * u**2
        * z**2
    )

    e_gate_potential = float(
        np.sum(
            node
            * gate_potential_density
        )
    )

    e_interaction = float(
        np.sum(
            node
            * interaction_density
        )
    )

    gz += (
        node
        * rho_gate
        * (
            a2
            * (
                z**2
                - 1.0
            )
            * z
            + b2
            * u**2
            * z
        )
    )

    gu += (
        node
        * rho_gate
        * b2
        * u
        * z**2
    )

    total = (
        e_y_grad
        + e_source_potential
        + e_q
        + e_u_grad
        + e_scalar_mass
        + e_z_grad
        + e_gate_potential
        + e_interaction
    )

    return (
        total,
        gy,
        gu,
        gz,
        omega,
    )


def energy_components(
    y: np.ndarray,
    u: np.ndarray,
    z: np.ndarray,
    r: np.ndarray,
    h: float,
    target_q: float,
    epsilon: float,
    chi: float,
    rho_gate: float,
    a2: float,
    b2: float,
):
    node, edge = integration_geometry(
        r,
        h,
    )

    dy = np.diff(y)
    du = np.diff(u)
    dz = np.diff(z)

    i_y_grad = (
        0.5
        * float(
            np.sum(
                edge
                * dy**2
            )
        )
    )

    i_u_grad = (
        0.5
        / chi**2
        * float(
            np.sum(
                edge
                * du**2
            )
        )
    )

    i_z_grad = (
        0.5
        * rho_gate
        * float(
            np.sum(
                edge
                * dz**2
            )
        )
    )

    A = np.exp(
        -0.5
        * u**2
    )

    W = (
        0.5
        * np.log1p(
            y**2
        )
    )

    S = float(
        np.sum(
            node
            * y**2
        )
    )

    omega = (
        target_q
        / S
    )

    i_q = (
        0.5
        * target_q**2
        / S
    )

    i_source_on_potential = float(
        np.sum(
            node
            * A
            * W
        )
    )

    i_source_inventory_potential = float(
        np.sum(
            node
            * W
        )
    )

    i_scalar_mass = float(
        np.sum(
            node
            * (
                0.5
                * epsilon**2
                * u**2
                / chi**2
            )
        )
    )

    i_gate_potential = float(
        np.sum(
            node
            * rho_gate
            * a2
            / 4.0
            * (
                z**2
                - 1.0
            )**2
        )
    )

    i_interaction = float(
        np.sum(
            node
            * rho_gate
            * 0.5
            * b2
            * u**2
            * z**2
        )
    )

    i_gate = (
        i_z_grad
        + i_gate_potential
        + i_interaction
    )

    i_scalar = (
        i_u_grad
        + i_scalar_mass
    )

    i_on = (
        i_y_grad
        + i_source_on_potential
        + i_q
        + i_scalar
        + i_gate
    )

    i_inventory = (
        i_y_grad
        + i_q
        + i_source_inventory_potential
        + i_scalar
        + i_gate
    )

    return {
        "S":
            S,

        "omega":
            omega,

        "I_y_gradient":
            i_y_grad,

        "I_Q_kinetic":
            i_q,

        "I_source_on_potential":
            i_source_on_potential,

        "I_source_inventory_potential":
            i_source_inventory_potential,

        "I_scalar":
            i_scalar,

        "I_gate_gradient":
            i_z_grad,

        "I_gate_potential":
            i_gate_potential,

        "I_gate_interaction":
            i_interaction,

        "I_gate_total":
            i_gate,

        "I_ON":
            i_on,

        "I_INVENTORY":
            i_inventory,

        "E_over_QmX":
            i_on
            / target_q,
    }


def projected_gradient_max(
    values: np.ndarray,
    gradient: np.ndarray,
    bounds,
):
    pg = np.array(
        gradient,
        dtype=float,
        copy=True,
    )

    tolerance = 1.0e-10

    for index, (
        lower,
        upper,
    ) in enumerate(bounds):
        value = values[index]
        grad = pg[index]

        if (
            lower is not None
            and value <= lower + tolerance
            and grad > 0.0
        ):
            pg[index] = 0.0

        elif (
            upper is not None
            and value >= upper - tolerance
            and grad < 0.0
        ):
            pg[index] = 0.0

    return float(
        np.max(
            np.abs(pg)
        )
    )


def main() -> None:
    print(
        "=== 031D2C-V FIXED-Q VARIATIONAL GATE EXISTENCE ==="
    )

    print(
        "COLLOCATION_BVP_USED=NO"
    )

    print(
        "FIXED_Q_ENERGY_MINIMIZATION=YES"
    )

    print(
        "OMEGA_ELIMINATED_ANALYTICALLY=YES"
    )

    print(
        "MULTI_SEED_ON_BASIN_TEST=YES"
    )

    print(
        "POSITIVE_GATE_INTERACTION_INCLUDED=YES"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    for path in (
        QBALL_SOURCE,
        ROBUST_SUMMARY,
        LOW_SUMMARY,
        D1HR_SUMMARY,
    ):
        require(path)

    robust = json.loads(
        ROBUST_SUMMARY.read_text()
    )

    low = json.loads(
        LOW_SUMMARY.read_text()
    )

    d1hr = json.loads(
        D1HR_SUMMARY.read_text()
    )

    if not bool(
        robust.get(
            "family_operating_robustness_green",
            False,
        )
    ):
        raise RuntimeError(
            "031C96 operating family is not GREEN"
        )

    if not bool(
        d1hr.get(
            "gate_free_same_Q_offstate_route_closed",
            False,
        )
    ):
        raise RuntimeError(
            "031D1 gate-free closure missing"
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

    omega_seed = float(
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

    M_c_ev = (
        M_c_gev
        * 1.0e9
    )

    target_q = float(
        low[
            "target_I_Q"
        ]
    )

    operating_energy_j = float(
        operating[
            "energy_J"
        ]
    )

    critical_hat = float(
        low[
            "critical_positive_delta_m2_hat"
        ]
    )

    delta2 = (
        STABILIZATION_MARGIN
        * critical_hat
    )

    required_gv_ev = (
        m_x_ev
        * math.sqrt(
            delta2
        )
    )

    v_s_ev = (
        required_gv_ev
        / G_S
    )

    lambda_s = (
        M_S_EV**2
        /
        (
            2.0
            * v_s_ev**2
        )
    )

    a2 = (
        lambda_s
        * v_s_ev**2
        / m_x_ev**2
    )

    b2 = (
        G_S**2
        * M_c_ev**2
        / m_x_ev**2
    )

    rho_gate = (
        v_s_ev
        / F_ev
    )**2

    identity = (
        chi**2
        * rho_gate
        * b2
    )

    identity_relerr = relerr(
        identity,
        delta2,
    )

    u_transition = math.sqrt(
        a2
        / b2
    )

    off_lambda0 = (
        float(
            low[
                "finest_lambda0"
            ]
        )
        + delta2
    )

    energy_scale_j = (
        F_gev**2
        / m_x_gev
        * J_PER_GEV
    )

    print(
        f"TARGET_I_Q="
        f"{target_q:.15e}"
    )

    print(
        f"G_S="
        f"{G_S:.15e}"
    )

    print(
        f"V_S_EV="
        f"{v_s_ev:.15e}"
    )

    print(
        f"LAMBDA_S="
        f"{lambda_s:.15e}"
    )

    print(
        f"A2_GATE="
        f"{a2:.15e}"
    )

    print(
        f"B2_GATE="
        f"{b2:.15e}"
    )

    print(
        f"DELTA2_GATE="
        f"{delta2:.15e}"
    )

    print(
        f"RHO_GATE="
        f"{rho_gate:.15e}"
    )

    print(
        f"VARIATIONAL_IDENTITY_RELERR="
        f"{identity_relerr:.15e}"
    )

    print(
        f"U_TRANSITION="
        f"{u_transition:.15e}"
    )

    print(
        f"OFF_SCALAR_LAMBDA0_WITH_GATE="
        f"{off_lambda0:+.15e}"
    )

    qmod = load_module(
        "qball031d2cv",
        QBALL_SOURCE,
    )

    old_x_match = float(
        qmod.X_MATCH
    )

    qmod.X_MATCH = X_MATCH

    try:
        print(
            "\n=== STAGE A: RECONSTRUCT UNGATED ON-STATE ==="
        )

        seed = qmod.solve_uncoupled_qball(
            omega_seed
        )

        if seed is None:
            raise RuntimeError(
                "Failed Q-ball seed"
            )

        baseline = qmod.solve_coupled(
            seed,
            omega_seed,
            epsilon,
            chi,
            previous=None,
        )

        if baseline is None:
            raise RuntimeError(
                "Failed baseline scalarized source"
            )

        y80 = float(
            baseline.sol(
                X_MATCH
            )[0]
        )

        u80 = float(
            baseline.sol(
                X_MATCH
            )[2]
        )

        k_y = math.sqrt(
            1.0
            - omega_seed**2
        )

        def baseline_fields(
            r,
            u_factor=1.0,
        ):
            y = np.zeros_like(
                r
            )

            u = np.zeros_like(
                r
            )

            inside = (
                r <= X_MATCH
            )

            positive_r = np.maximum(
                r[
                    inside
                ],
                X0_SOURCE,
            )

            source_state = baseline.sol(
                positive_r
            )

            y[
                inside
            ] = source_state[
                0
            ]

            u[
                inside
            ] = (
                u_factor
                * source_state[
                    2
                ]
            )

            outside = (
                ~inside
            )

            if np.any(
                outside
            ):
                ro = r[
                    outside
                ]

                y[
                    outside
                ] = (
                    y80
                    * X_MATCH
                    / ro
                    * np.exp(
                        -k_y
                        * (
                            ro
                            - X_MATCH
                        )
                    )
                )

                u[
                    outside
                ] = (
                    u_factor
                    * u80
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

            # Dirichlet asymptotic endpoints.
            y[-1] = 0.0
            u[-1] = 0.0

            above = np.where(
                u
                >= u_transition
            )[0]

            if len(
                above
            ) > 0:
                index = int(
                    above[-1]
                )

                if index < len(
                    r
                ) - 1:
                    u_a = u[
                        index
                    ]

                    u_b = u[
                        index + 1
                    ]

                    if (
                        u_a
                        != u_b
                    ):
                        fraction = (
                            u_transition
                            - u_a
                        ) / (
                            u_b
                            - u_a
                        )

                        transition = (
                            r[index]
                            + fraction
                            * (
                                r[
                                    index + 1
                                ]
                                - r[index]
                            )
                        )

                    else:
                        transition = (
                            r[index]
                        )

                else:
                    transition = (
                        r[index]
                    )

            else:
                transition = (
                    0.5
                    * r[-1]
                )

            gate_width = (
                1.0
                / math.sqrt(
                    max(
                        2.0
                        * a2,
                        1.0e-12,
                    )
                )
            )

            argument = np.clip(
                (
                    r
                    - transition
                )
                / gate_width,
                -40.0,
                40.0,
            )

            z = (
                0.5
                * (
                    1.0
                    + np.tanh(
                        argument
                    )
                )
            )

            z[-1] = 1.0

            return (
                y,
                u,
                z,
                transition,
            )

        # -----------------------------------------------------------
        # Independent baseline energy reconstruction
        # -----------------------------------------------------------

        r_check, h_check = make_grid(
            600.0,
            0.20,
        )

        y_check, u_check, _, _ = baseline_fields(
            r_check,
            1.0,
        )

        z_zero = np.zeros_like(
            r_check
        )

        z_zero[-1] = 1.0

        baseline_components = energy_components(
            y_check,
            u_check,
            z_zero,
            r_check,
            h_check,
            target_q,
            epsilon,
            chi,
            0.0,
            a2,
            b2,
        )

        baseline_inventory_j = (
            baseline_components[
                "I_INVENTORY"
            ]
            * energy_scale_j
        )

        baseline_recon_relerr = relerr(
            baseline_inventory_j,
            operating_energy_j,
        )

        print(
            f"BASELINE_VARIATIONAL_INVENTORY_GJ="
            f"{baseline_inventory_j / 1.0e9:.12f}"
        )

        print(
            f"BASELINE_REFERENCE_GJ="
            f"{operating_energy_j / 1.0e9:.12f}"
        )

        print(
            f"BASELINE_RECON_RELERR="
            f"{baseline_recon_relerr:.15e}"
        )

        baseline_recon_pass = bool(
            baseline_recon_relerr
            <= BASELINE_RECON_REL_MAX
        )

        print(
            f"BASELINE_RECON_PASS="
            f"{baseline_recon_pass}"
        )

        if not baseline_recon_pass:
            raise RuntimeError(
                "Variational discretization does not reproduce "
                "the inherited source inventory accurately enough"
            )

        # -----------------------------------------------------------
        # Optimizers
        # -----------------------------------------------------------

        def optimize_fields(
            r,
            h,
            initial,
            staged=True,
        ):
            n = len(
                r
            )

            m = n - 1

            y, u, z = [
                np.array(
                    field,
                    dtype=float,
                    copy=True,
                )
                for field in initial
            ]

            y[-1] = 0.0
            u[-1] = 0.0
            z[-1] = 1.0

            def evaluate(
                yy,
                uu,
                zz,
            ):
                return full_energy_gradient(
                    yy,
                    uu,
                    zz,
                    r,
                    h,
                    target_q,
                    epsilon,
                    chi,
                    rho_gate,
                    a2,
                    b2,
                )

            if staged:
                # ---------------------------------------------------
                # Gate only
                # ---------------------------------------------------

                z_bounds = [
                    (
                        0.0,
                        1.0,
                    )
                    for _ in range(
                        m
                    )
                ]

                def objective_z(
                    values,
                ):
                    zz = np.empty(
                        n
                    )

                    zz[:-1] = values
                    zz[-1] = 1.0

                    energy, _, _, gz, _ = evaluate(
                        y,
                        u,
                        zz,
                    )

                    return (
                        energy,
                        gz[:-1],
                    )

                result_z = minimize(
                    objective_z,
                    z[:-1],
                    method="L-BFGS-B",
                    jac=True,
                    bounds=z_bounds,
                    options={
                        "maxiter":
                            MAXITER_Z,
                        "gtol":
                            GTOL,
                        "ftol":
                            FTOL,
                        "maxls":
                            50,
                    },
                )

                z[:-1] = (
                    result_z.x
                )

                # ---------------------------------------------------
                # u + gate
                # ---------------------------------------------------

                uz0 = np.concatenate(
                    (
                        u[:-1],
                        z[:-1],
                    )
                )

                uz_bounds = (
                    [
                        (
                            0.0,
                            U_MAX,
                        )
                        for _ in range(
                            m
                        )
                    ]
                    +
                    [
                        (
                            0.0,
                            1.0,
                        )
                        for _ in range(
                            m
                        )
                    ]
                )

                def objective_uz(
                    values,
                ):
                    uu = np.empty(
                        n
                    )

                    zz = np.empty(
                        n
                    )

                    uu[:-1] = values[
                        :m
                    ]

                    zz[:-1] = values[
                        m:
                    ]

                    uu[-1] = 0.0
                    zz[-1] = 1.0

                    energy, _, gu, gz, _ = evaluate(
                        y,
                        uu,
                        zz,
                    )

                    return (
                        energy,
                        np.concatenate(
                            (
                                gu[:-1],
                                gz[:-1],
                            )
                        ),
                    )

                result_uz = minimize(
                    objective_uz,
                    uz0,
                    method="L-BFGS-B",
                    jac=True,
                    bounds=uz_bounds,
                    options={
                        "maxiter":
                            MAXITER_UZ,
                        "gtol":
                            GTOL,
                        "ftol":
                            FTOL,
                        "maxls":
                            50,
                    },
                )

                u[:-1] = (
                    result_uz.x[
                        :m
                    ]
                )

                z[:-1] = (
                    result_uz.x[
                        m:
                    ]
                )

            # -------------------------------------------------------
            # Full y/u/z fixed-Q minimization
            # -------------------------------------------------------

            values0 = np.concatenate(
                (
                    y[:-1],
                    u[:-1],
                    z[:-1],
                )
            )

            bounds = (
                [
                    (
                        0.0,
                        Y_MAX,
                    )
                    for _ in range(
                        m
                    )
                ]
                +
                [
                    (
                        0.0,
                        U_MAX,
                    )
                    for _ in range(
                        m
                    )
                ]
                +
                [
                    (
                        0.0,
                        1.0,
                    )
                    for _ in range(
                        m
                    )
                ]
            )

            def objective_all(
                values,
            ):
                yy = np.empty(
                    n
                )

                uu = np.empty(
                    n
                )

                zz = np.empty(
                    n
                )

                yy[:-1] = values[
                    :m
                ]

                uu[:-1] = values[
                    m:
                    2 * m
                ]

                zz[:-1] = values[
                    2 * m:
                ]

                yy[-1] = 0.0
                uu[-1] = 0.0
                zz[-1] = 1.0

                energy, gy, gu, gz, _ = evaluate(
                    yy,
                    uu,
                    zz,
                )

                gradient = np.concatenate(
                    (
                        gy[:-1],
                        gu[:-1],
                        gz[:-1],
                    )
                )

                return (
                    energy,
                    gradient,
                )

            result = minimize(
                objective_all,
                values0,
                method="L-BFGS-B",
                jac=True,
                bounds=bounds,
                options={
                    "maxiter":
                        MAXITER_ALL,
                    "gtol":
                        GTOL,
                    "ftol":
                        FTOL,
                    "maxls":
                        60,
                    "maxcor":
                        30,
                },
            )

            yy = np.empty(
                n
            )

            uu = np.empty(
                n
            )

            zz = np.empty(
                n
            )

            yy[:-1] = result.x[
                :m
            ]

            uu[:-1] = result.x[
                m:
                2 * m
            ]

            zz[:-1] = result.x[
                2 * m:
            ]

            yy[-1] = 0.0
            uu[-1] = 0.0
            zz[-1] = 1.0

            final_energy, gy, gu, gz, omega = evaluate(
                yy,
                uu,
                zz,
            )

            final_gradient = np.concatenate(
                (
                    gy[:-1],
                    gu[:-1],
                    gz[:-1],
                )
            )

            pgrad = projected_gradient_max(
                result.x,
                final_gradient,
                bounds,
            )

            return {
                "y":
                    yy,

                "u":
                    uu,

                "z":
                    zz,

                "energy":
                    final_energy,

                "omega":
                    omega,

                "projected_gradient_max":
                    pgrad,

                "optimizer_success":
                    bool(
                        result.success
                    ),

                "optimizer_status":
                    int(
                        result.status
                    ),

                "optimizer_message":
                    str(
                        result.message
                    ),

                "optimizer_iterations":
                    int(
                        result.nit
                    ),
            }

        # -----------------------------------------------------------
        # STAGE B — first-domain multi-seed ON basin
        # -----------------------------------------------------------

        print(
            "\n=== STAGE B: MULTI-SEED ON-BASIN VARIATIONAL TEST ==="
        )

        first_rmax, first_h_target = DOMAIN_SPECS[
            0
        ]

        first_r, first_h = make_grid(
            first_rmax,
            first_h_target,
        )

        seed_rows = []
        survivors = []

        for u_factor in U_SEED_FACTORS:
            y0, u0, z0, transition = baseline_fields(
                first_r,
                u_factor,
            )

            solved = optimize_fields(
                first_r,
                first_h,
                (
                    y0,
                    u0,
                    z0,
                ),
                staged=True,
            )

            components = energy_components(
                solved[
                    "y"
                ],
                solved[
                    "u"
                ],
                solved[
                    "z"
                ],
                first_r,
                first_h,
                target_q,
                epsilon,
                chi,
                rho_gate,
                a2,
                b2,
            )

            inventory_j = (
                components[
                    "I_INVENTORY"
                ]
                * energy_scale_j
            )

            on_survivor = bool(
                solved[
                    "u"
                ][0]
                >= ON_U0_MIN
                and
                solved[
                    "z"
                ][0]
                <= ON_Z0_MAX
                and
                solved[
                    "projected_gradient_max"
                ]
                <= PROJECTED_GRADIENT_MAX
                and
                0.0
                < components[
                    "omega"
                ]
                < 1.0
            )

            row = {
                "u_seed_factor":
                    u_factor,

                "initial_transition_x":
                    transition,

                "u0_final":
                    float(
                        solved[
                            "u"
                        ][0]
                    ),

                "z0_final":
                    float(
                        solved[
                            "z"
                        ][0]
                    ),

                "omega":
                    components[
                        "omega"
                    ],

                "inventory_J":
                    inventory_j,

                "inventory_GJ":
                    inventory_j
                    / 1.0e9,

                "E_over_QmX":
                    components[
                        "E_over_QmX"
                    ],

                "projected_gradient_max":
                    solved[
                        "projected_gradient_max"
                    ],

                "optimizer_success":
                    solved[
                        "optimizer_success"
                    ],

                "optimizer_iterations":
                    solved[
                        "optimizer_iterations"
                    ],

                "on_survivor":
                    on_survivor,
            }

            seed_rows.append(
                row
            )

            print(
                f"SEED "
                f"U_FACTOR={u_factor:.3f} "
                f"U0={row['u0_final']:.9e} "
                f"Z0={row['z0_final']:.9e} "
                f"OMEGA={row['omega']:.12e} "
                f"E_GJ={row['inventory_GJ']:.9f} "
                f"PGRAD={row['projected_gradient_max']:.6e} "
                f"ON_SURVIVOR={on_survivor}"
            )

            if on_survivor:
                survivors.append(
                    (
                        solved,
                        components,
                        row,
                    )
                )

        if not survivors:
            classification = (
                "RED_D2CV_NO_ON_LOCAL_MINIMUM_FOUND_"
                "IN_DECLARED_MULTI_SEED_FIXEDQ_VARIATIONAL_TEST"
            )

            next_action = (
                "DEMOTE_CANONICAL_S2PHI2_GATE_AND_RERANK_031D"
            )

            print(
                "\n=== STOP RULE ==="
            )

            print(
                "ON_LOCAL_MINIMUM_SURVIVOR_COUNT=0"
            )

            print(
                f"031D2CV_CLASSIFICATION="
                f"{classification}"
            )

            print(
                f"NEXT={next_action}"
            )

            summary = {
                "classification":
                    classification,

                "next":
                    next_action,

                "baseline_reconstruction_relerr":
                    baseline_recon_relerr,

                "seed_rows":
                    seed_rows,

                "claim_limits": [
                    (
                        "This closes only the declared canonical "
                        "s^2 phi^2 gate in the tested fixed theory/"
                        "parameter point and multi-seed variational test."
                    ),
                    (
                        "It does not close all possible auxiliary "
                        "activation fields."
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
                    for row in seed_rows
                    for key in row
                }
            )

            with OUT_SEED.open(
                "w",
                newline="",
            ) as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=fields,
                )

                writer.writeheader()
                writer.writerows(
                    seed_rows
                )

            OUT_DOMAIN.write_text(
                "rmax,h\n"
            )

            return

        # Lowest ON stationary survivor.
        survivors.sort(
            key=lambda item:
                item[1][
                    "I_ON"
                ]
        )

        chosen = survivors[
            0
        ][0]

        print(
            f"ON_LOCAL_MINIMUM_SURVIVOR_COUNT="
            f"{len(survivors)}"
        )

        # -----------------------------------------------------------
        # STAGE C — domain and final grid refinement
        # -----------------------------------------------------------

        print(
            "\n=== STAGE C: DOMAIN / GRID CONTINUATION ==="
        )

        domain_rows = []

        previous_r = first_r
        previous_solution = chosen

        for spec_index, (
            rmax,
            h_target,
        ) in enumerate(
            DOMAIN_SPECS
        ):
            r, h = make_grid(
                rmax,
                h_target,
            )

            if spec_index == 0:
                solved = chosen

            else:
                y_seed = np.interp(
                    r,
                    previous_r,
                    previous_solution[
                        "y"
                    ],
                    left=previous_solution[
                        "y"
                    ][0],
                    right=0.0,
                )

                u_seed = np.interp(
                    r,
                    previous_r,
                    previous_solution[
                        "u"
                    ],
                    left=previous_solution[
                        "u"
                    ][0],
                    right=0.0,
                )

                z_seed = np.interp(
                    r,
                    previous_r,
                    previous_solution[
                        "z"
                    ],
                    left=previous_solution[
                        "z"
                    ][0],
                    right=1.0,
                )

                y_seed[-1] = 0.0
                u_seed[-1] = 0.0
                z_seed[-1] = 1.0

                solved = optimize_fields(
                    r,
                    h,
                    (
                        y_seed,
                        u_seed,
                        z_seed,
                    ),
                    staged=False,
                )

            components = energy_components(
                solved[
                    "y"
                ],
                solved[
                    "u"
                ],
                solved[
                    "z"
                ],
                r,
                h,
                target_q,
                epsilon,
                chi,
                rho_gate,
                a2,
                b2,
            )

            inventory_j = (
                components[
                    "I_INVENTORY"
                ]
                * energy_scale_j
            )

            gate_j = (
                components[
                    "I_gate_total"
                ]
                * energy_scale_j
            )

            gate_interaction_j = (
                components[
                    "I_gate_interaction"
                ]
                * energy_scale_j
            )

            z_array = solved[
                "z"
            ]

            transition_x = float(
                np.interp(
                    0.5,
                    np.maximum.accumulate(
                        np.clip(
                            z_array,
                            0.0,
                            1.0,
                        )
                    ),
                    r,
                )
            )

            row = {
                "rmax":
                    rmax,

                "h":
                    h,

                "omega":
                    components[
                        "omega"
                    ],

                "u0":
                    float(
                        solved[
                            "u"
                        ][0]
                    ),

                "z0":
                    float(
                        solved[
                            "z"
                        ][0]
                    ),

                "transition_x_z50":
                    transition_x,

                "inventory_J":
                    inventory_j,

                "inventory_GJ":
                    inventory_j
                    / 1.0e9,

                "gate_J":
                    gate_j,

                "gate_GJ":
                    gate_j
                    / 1.0e9,

                "interaction_J":
                    gate_interaction_j,

                "E_over_QmX":
                    components[
                        "E_over_QmX"
                    ],

                "projected_gradient_max":
                    solved[
                        "projected_gradient_max"
                    ],

                "optimizer_success":
                    solved[
                        "optimizer_success"
                    ],

                "optimizer_iterations":
                    solved[
                        "optimizer_iterations"
                    ],
            }

            domain_rows.append(
                row
            )

            print(
                f"VARIATIONAL "
                f"RMAX={rmax:.1f} "
                f"H={h:.6f} "
                f"OMEGA={row['omega']:.12e} "
                f"U0={row['u0']:.9e} "
                f"Z0={row['z0']:.9e} "
                f"Z50_X={transition_x:.6f} "
                f"TOTAL_GJ={row['inventory_GJ']:.9f} "
                f"GATE_GJ={row['gate_GJ']:.9f} "
                f"PGRAD={row['projected_gradient_max']:.6e}"
            )

            previous_r = r
            previous_solution = solved

        final_r = previous_r
        final = previous_solution

        final_components = energy_components(
            final[
                "y"
            ],
            final[
                "u"
            ],
            final[
                "z"
            ],
            final_r,
            DOMAIN_SPECS[-1][
                0
            ]
            / (
                len(
                    final_r
                )
                - 1
            ),
            target_q,
            epsilon,
            chi,
            rho_gate,
            a2,
            b2,
        )

        final_inventory_j = (
            final_components[
                "I_INVENTORY"
            ]
            * energy_scale_j
        )

        final_gate_j = (
            final_components[
                "I_gate_total"
            ]
            * energy_scale_j
        )

        # -----------------------------------------------------------
        # Domain convergence: first three h~0.3 cases.
        # -----------------------------------------------------------

        domain_base = domain_rows[
            :3
        ]

        omega_domain = np.array(
            [
                row[
                    "omega"
                ]
                for row in domain_base
            ]
        )

        u0_domain = np.array(
            [
                row[
                    "u0"
                ]
                for row in domain_base
            ]
        )

        energy_domain = np.array(
            [
                row[
                    "inventory_J"
                ]
                for row in domain_base
            ]
        )

        omega_domain_spread = (
            np.max(
                omega_domain
            )
            - np.min(
                omega_domain
            )
        ) / max(
            abs(
                np.mean(
                    omega_domain
                )
            ),
            1.0e-300,
        )

        u0_domain_spread = (
            np.max(
                u0_domain
            )
            - np.min(
                u0_domain
            )
        ) / max(
            abs(
                np.mean(
                    u0_domain
                )
            ),
            1.0e-300,
        )

        energy_domain_spread = (
            np.max(
                energy_domain
            )
            - np.min(
                energy_domain
            )
        ) / max(
            abs(
                np.mean(
                    energy_domain
                )
            ),
            1.0e-300,
        )

        domain_pass = bool(
            omega_domain_spread
            <= DOMAIN_OMEGA_REL_MAX
            and
            u0_domain_spread
            <= DOMAIN_U0_REL_MAX
            and
            energy_domain_spread
            <= DOMAIN_ENERGY_REL_MAX
        )

        # -----------------------------------------------------------
        # Grid refinement: R=600 h~0.3 vs h~0.2.
        # -----------------------------------------------------------

        coarse = domain_rows[
            -2
        ]

        fine = domain_rows[
            -1
        ]

        omega_grid_rel = relerr(
            coarse[
                "omega"
            ],
            fine[
                "omega"
            ],
        )

        u0_grid_rel = relerr(
            coarse[
                "u0"
            ],
            fine[
                "u0"
            ],
        )

        energy_grid_rel = relerr(
            coarse[
                "inventory_J"
            ],
            fine[
                "inventory_J"
            ],
        )

        grid_pass = bool(
            omega_grid_rel
            <= GRID_OMEGA_REL_MAX
            and
            u0_grid_rel
            <= GRID_U0_REL_MAX
            and
            energy_grid_rel
            <= GRID_ENERGY_REL_MAX
        )

        # -----------------------------------------------------------
        # Payload response
        # -----------------------------------------------------------

        print(
            "\n=== STAGE D: FINITE-PAYLOAD RESPONSE ==="
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

        payload_radii_m = (
            (
                "near",
                center_from_source_m
                - payload_radius_m,
            ),
            (
                "center",
                center_from_source_m,
            ),
            (
                "far",
                center_from_source_m
                + payload_radius_m,
            ),
        )

        final_h = (
            final_r[-1]
            / (
                len(
                    final_r
                )
                - 1
            )
        )

        final_up = np.gradient(
            final[
                "u"
            ],
            final_h,
        )

        payload_ratios = []
        payload_signs = []

        for label, radius_m in payload_radii_m:
            xp = (
                radius_m
                / x_length_m
            )

            gated_up = float(
                np.interp(
                    xp,
                    final_r,
                    final_up,
                )
            )

            baseline_up = float(
                baseline.sol(
                    xp
                )[3]
            )

            ratio = (
                abs(
                    gated_up
                )
                / max(
                    abs(
                        baseline_up
                    ),
                    1.0e-300,
                )
            )

            same_sign = bool(
                gated_up
                * baseline_up
                > 0.0
            )

            payload_ratios.append(
                ratio
            )

            payload_signs.append(
                same_sign
            )

            print(
                f"PAYLOAD_{label.upper()} "
                f"R_M={radius_m:.9f} "
                f"BASE_UP={baseline_up:+.12e} "
                f"GATED_UP={gated_up:+.12e} "
                f"ABS_RATIO={ratio:.12e} "
                f"SAME_SIGN={same_sign}"
            )

        payload_pass = bool(
            min(
                payload_ratios
            )
            >= PAYLOAD_GRADIENT_RATIO_MIN
            and
            all(
                payload_signs
            )
        )

        print(
            f"PAYLOAD_GRADIENT_PRESERVED="
            f"{payload_pass}"
        )

        # -----------------------------------------------------------
        # Exact OFF branch quadratic stability
        # -----------------------------------------------------------

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
            off_lambda0
            > 0.0
        )

        off_gate_mass2 = (
            2.0
            * a2
        )

        off_gate_pass = bool(
            off_gate_mass2
            > 0.0
        )

        off_pass = bool(
            off_source_pass
            and
            off_scalar_pass
            and
            off_gate_pass
        )

        final_on_pass = bool(
            final[
                "u"
            ][0]
            >= ON_U0_MIN
            and
            final[
                "z"
            ][0]
            <= ON_Z0_MAX
            and
            final[
                "projected_gradient_max"
            ]
            <= PROJECTED_GRADIENT_MAX
            and
            0.0
            < final_components[
                "omega"
            ]
            < 1.0
        )

        positive_energy_pass = bool(
            math.isfinite(
                final_inventory_j
            )
            and
            final_inventory_j
            > 0.0
            and
            final_gate_j
            >= 0.0
        )

        print(
            "\n=== STAGE E: CONVERGENCE / FINAL DECISION ==="
        )

        print(
            f"OMEGA_DOMAIN_REL_SPREAD="
            f"{omega_domain_spread:.15e}"
        )

        print(
            f"U0_DOMAIN_REL_SPREAD="
            f"{u0_domain_spread:.15e}"
        )

        print(
            f"ENERGY_DOMAIN_REL_SPREAD="
            f"{energy_domain_spread:.15e}"
        )

        print(
            f"DOMAIN_CONVERGENCE_PASS="
            f"{domain_pass}"
        )

        print(
            f"OMEGA_GRID_REL_DIFF="
            f"{omega_grid_rel:.15e}"
        )

        print(
            f"U0_GRID_REL_DIFF="
            f"{u0_grid_rel:.15e}"
        )

        print(
            f"ENERGY_GRID_REL_DIFF="
            f"{energy_grid_rel:.15e}"
        )

        print(
            f"GRID_REFINEMENT_PASS="
            f"{grid_pass}"
        )

        print(
            f"FINAL_PROJECTED_GRADIENT_MAX="
            f"{final['projected_gradient_max']:.15e}"
        )

        print(
            f"FINAL_ON_LOCAL_MINIMUM_PASS="
            f"{final_on_pass}"
        )

        print(
            f"OFF_SCALAR_LAMBDA0_WITH_GATE="
            f"{off_lambda0:+.15e}"
        )

        print(
            f"OFF_GATE_MASS2_HAT="
            f"{off_gate_mass2:.15e}"
        )

        print(
            f"OFF_EXACT_FIXEDQ_BRANCH_PASS="
            f"{off_pass}"
        )

        print(
            f"FINAL_GATE_POSITIVE_ENERGY_GJ="
            f"{final_gate_j / 1.0e9:.12f}"
        )

        print(
            f"FINAL_TOTAL_INVENTORY_GJ="
            f"{final_inventory_j / 1.0e9:.12f}"
        )

        print(
            f"TOTAL_OVER_121P553GJ="
            f"{final_inventory_j / operating_energy_j:.15e}"
        )

        print(
            f"POSITIVE_FINITE_ENERGY_PASS="
            f"{positive_energy_pass}"
        )

        green = bool(
            final_on_pass
            and
            off_pass
            and
            domain_pass
            and
            grid_pass
            and
            payload_pass
            and
            positive_energy_pass
        )

        if green:
            classification = (
                "GREEN_D2CV_FIXEDQ_VARIATIONAL_"
                "MICROSCOPIC_ON_OFF_EXISTENCE"
            )

            next_action = (
                "031D2D_COUPLED_Y_U_GATE_LINEAR_STABILITY_"
                "PLUS_SWITCHING_BARRIER_RESET_RADIATION"
            )

        else:
            classification = (
                "YELLOW_D2CV_ON_VARIATIONAL_BRANCH_FOUND_"
                "BUT_CERTIFICATION_SUBGATE_FAILED"
            )

            next_action = (
                "REFINE_ONLY_FAILED_D2CV_SUBGATE"
            )

        print(
            f"031D2CV_CLASSIFICATION="
            f"{classification}"
        )

        print(
            f"NEXT={next_action}"
        )

        print(
            "COUPLED_Y_U_GATE_SPECTRAL_STABILITY_CLOSED=NO"
        )

        print(
            "SWITCHING_BARRIER_CLOSED=NO"
        )

        print(
            "FORMATION_RESET_ENERGY_CLOSED=NO"
        )

        print(
            "RADIATION_CLOSED=NO"
        )

        print(
            "FULL_METRIC_BACKREACTION_CLOSED=NO"
        )

        print(
            "EFT_NATURALNESS_CLOSED=NO"
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

            "method":
                "FIXED_Q_CONSTRAINED_VARIATIONAL_ENERGY_MINIMIZATION",

            "baseline_reconstruction_relerr":
                baseline_recon_relerr,

            "gate_candidate": {
                "g_s":
                    G_S,

                "v_s_eV":
                    v_s_ev,

                "lambda_s":
                    lambda_s,

                "m_s_eV":
                    M_S_EV,

                "a2":
                    a2,

                "b2":
                    b2,

                "delta2":
                    delta2,

                "rho_gate":
                    rho_gate,

                "variational_identity_relerr":
                    identity_relerr,
            },

            "seed_rows":
                seed_rows,

            "domain_rows":
                domain_rows,

            "convergence": {
                "omega_domain_rel_spread":
                    omega_domain_spread,

                "u0_domain_rel_spread":
                    u0_domain_spread,

                "energy_domain_rel_spread":
                    energy_domain_spread,

                "domain_pass":
                    domain_pass,

                "omega_grid_rel_diff":
                    omega_grid_rel,

                "u0_grid_rel_diff":
                    u0_grid_rel,

                "energy_grid_rel_diff":
                    energy_grid_rel,

                "grid_pass":
                    grid_pass,
            },

            "final": {
                "omega":
                    final_components[
                        "omega"
                    ],

                "u0":
                    float(
                        final[
                            "u"
                        ][0]
                    ),

                "z0":
                    float(
                        final[
                            "z"
                        ][0]
                    ),

                "projected_gradient_max":
                    final[
                        "projected_gradient_max"
                    ],

                "gate_positive_energy_J":
                    final_gate_j,

                "total_inventory_J":
                    final_inventory_j,

                "total_over_previous":
                    final_inventory_j
                    / operating_energy_j,

                "E_over_QmX":
                    final_components[
                        "E_over_QmX"
                    ],
            },

            "payload": {
                "gradient_ratios":
                    payload_ratios,

                "pass":
                    payload_pass,
            },

            "off_state": {
                "source_pass":
                    off_source_pass,

                "scalar_lambda0":
                    off_lambda0,

                "scalar_pass":
                    off_scalar_pass,

                "gate_mass2_hat":
                    off_gate_mass2,

                "gate_pass":
                    off_gate_pass,

                "pass":
                    off_pass,
            },

            "claim_limits": [
                (
                    "This establishes at most a fixed-Q static local "
                    "minimum in the declared canonical gate model."
                ),
                (
                    "The complete coupled perturbative spectrum is "
                    "not yet evaluated."
                ),
                (
                    "Switching/nucleation, formation/reset energy and "
                    "radiation remain open."
                ),
                (
                    "The conservative inventory uses the project's "
                    "source-inventory convention W(y), not negative "
                    "interaction-energy credit."
                ),
                (
                    "Full physical-metric/Einstein backreaction, "
                    "EFT naturalness and empirical fifth-force/EP/PPN "
                    "closure remain open."
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

        seed_fields = sorted(
            {
                key
                for row in seed_rows
                for key in row
            }
        )

        with OUT_SEED.open(
            "w",
            newline="",
        ) as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=seed_fields,
            )

            writer.writeheader()
            writer.writerows(
                seed_rows
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
            f"SEED_CSV={OUT_SEED}"
        )

        print(
            f"DOMAIN_CSV={OUT_DOMAIN}"
        )

    finally:
        qmod.X_MATCH = old_x_match


if __name__ == "__main__":
    main()
