"""
031D1 — Q-ball self-activation / fixed-charge off-state gate
============================================================

PURPOSE
-------
Test the cheapest decisive activation/off-state question for the current
031 Q-ball architecture:

    Can the SAME conserved-U(1)-charge microscopic source possess a stable
    unscalarized u=0 state?

The current source equations are

    y'' + 2 y'/x
        = exp(-u^2/2) dW/dy - Omega^2 y

    u'' + 2 u'/x
        = [epsilon^2 - chi^2 exp(-u^2/2) W(y)] u

with

    W(y) = 0.5 log(1+y^2).

Therefore u=0 is always an exact Z2-symmetric solution branch.

At u=0, the linear scalar perturbation operator is

    L_off =
        -d^2/dx^2
        -2/x d/dx
        + epsilon^2
        -chi^2 W(y).

For reduced radial perturbation q=x*delta_u in l=0,

    K_off =
        -d^2/dx^2
        +epsilon^2
        -chi^2 W(y).

Because the source coupling is even in u, the y equation has no term linear
in delta_u around u=0. Likewise the U(1) charge changes only at higher order
under a pure delta_u perturbation. A robust negative scalar eigenvalue is
therefore a genuine coupled linear instability even at fixed Noether charge.

SCIENTIFIC QUESTION
-------------------
Does a stable u=0 Q-ball branch exist at the same conserved Noether charge as
the current GREEN scalarized source?

CHEAPEST DECISIVE TEST
----------------------
1. Reconstruct the scalarized Omega=0.34 source.
2. Independently compute its dimensionless Noether charge I_Q.
3. Scan the exact uncoupled u=0 Q-ball family.
4. Find every Omega_off satisfying I_Q_off = I_Q_on.
5. Check E/(Q m_X), dQ/dOmega, and the scalar off-state Hessian.
6. Converge the scalar Hessian in grid spacing and domain.

PROMOTION
---------
The current self-activation mechanism survives D1 only if at least one
same-charge unscalarized Q-ball branch is source-stable and has no negative
off-state scalar mode.

FALSIFIER
---------
A same-Q physical Q-ball off branch with a converged negative scalar Hessian
is a tachyonic off state: the device cannot remain unactivated without an
additional gating sector.

STOP RULE
---------
If all viable same-Q u=0 branches are tachyonic, close the gate-free
self-activation/off-state route and move directly to 031D2/D3:

    minimum auxiliary positive mass shift
    + explicit gate field
    + gate/control energy
    + reciprocity
    + switching/reset accounting.

CLAIM LIMITS
------------
This run does NOT:
- establish an auxiliary gate field;
- price gate/control energy;
- close finite-amplitude fragmentation;
- solve the full physical metric;
- establish radiative naturalness;
- establish empirical fifth-force/EP/PPN consistency;
- establish a practical device.
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

from scipy.integrate import quad
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import brentq


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results" / "data"

QBALL_SOURCE = (
    SIM
    / "031b2a_global_qball_activated_scalar_control.py"
)

ROBUST_SUMMARY = (
    DATA
    / "031c96_operating_margin_robustness_summary.json"
)

D96_SUMMARY = (
    DATA
    / "031b2d96_combined_coupled_linear_goldstone_summary.json"
)

OUT_JSON = (
    DATA
    / "031d1_qball_offstate_fixed_charge_summary.json"
)

OUT_CHARGE_CSV = (
    DATA
    / "031d1_offstate_charge_match_scan.csv"
)

OUT_HESSIAN_CSV = (
    DATA
    / "031d1_offstate_hessian_convergence.csv"
)


X_MATCH_SOURCE = 80.0

OMEGA_SCAN = np.linspace(
    0.18,
    0.95,
    40,
)

ROOT_XTOL = 2.0e-9
ROOT_RTOL = 2.0e-9

Q_MATCH_REL_TOL = 2.0e-6

E_OVER_QMX_BOUND = 1.0

DQ_DOMEGA_STEP = 2.0e-3

DOMAIN_EPS_R_VALUES = (
    1.2,
    3.0,
    5.0,
)

H_TARGETS = (
    0.50,
    0.25,
)

NEGATIVE_EIGENVALUE_TOL = 1.0e-6

HESSIAN_GRID_REL_TOL = 5.0e-2
HESSIAN_DOMAIN_REL_TOL = 5.0e-2

ON_E_OVER_Q_REL_TOL = 3.0e-3
INVENTORY_REPRO_REL_TOL = 3.0e-3

HBAR_GEV_S = 6.582119569e-25
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


def relerr(a: float, b: float) -> float:
    return abs(a - b) / max(
        abs(a),
        abs(b),
        1.0e-300,
    )


def to_builtin(value: Any):
    if isinstance(value, np.generic):
        return value.item()

    if isinstance(value, np.ndarray):
        return value.tolist()

    if isinstance(value, dict):
        return {
            str(k): to_builtin(v)
            for k, v in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [
            to_builtin(v)
            for v in value
        ]

    return value


def W(y):
    return 0.5 * np.log1p(y * y)


def integrate_spherical(
    x: np.ndarray,
    density: np.ndarray,
) -> float:
    return float(
        4.0
        * math.pi
        * np.trapezoid(
            x * x * density,
            x,
        )
    )


def scalar_tail_integral(
    u_boundary: float,
    epsilon: float,
    chi: float,
    x_boundary: float,
) -> float:
    """
    Exact asymptotic Yukawa tail ansatz:

        u(x) =
            u_R R/x exp[-epsilon(x-R)].
    """

    def integrand(xx: float) -> float:
        u = (
            u_boundary
            * x_boundary
            / xx
            * math.exp(
                -epsilon
                * (xx - x_boundary)
            )
        )

        up = (
            -epsilon
            -1.0 / xx
        ) * u

        density = (
            0.5 * up * up
            +0.5 * epsilon * epsilon * u * u
        ) / (chi * chi)

        return (
            4.0
            * math.pi
            * xx * xx
            * density
        )

    return float(
        quad(
            integrand,
            x_boundary,
            np.inf,
            epsabs=1.0e-12,
            epsrel=1.0e-9,
            limit=300,
        )[0]
    )


def coupled_integrals(
    solution,
    omega: float,
    epsilon: float,
    chi: float,
) -> dict[str, float]:
    """
    Independent reconstruction of the exact dimensionless energy/charge
    integrals used by the upstream Q-ball implementation.
    """

    x = np.linspace(
        1.0e-5,
        X_MATCH_SOURCE,
        20_000,
    )

    state = solution.sol(x)

    y = np.asarray(
        state[0],
        dtype=float,
    )

    yp = np.asarray(
        state[1],
        dtype=float,
    )

    u = np.asarray(
        state[2],
        dtype=float,
    )

    up = np.asarray(
        state[3],
        dtype=float,
    )

    A = np.exp(
        np.clip(
            -0.5 * u * u,
            -700.0,
            0.0,
        )
    )

    potential = W(y)

    source_on_density = (
        0.5 * yp * yp
        +0.5 * omega * omega * y * y
        +A * potential
    )

    source_off_inventory_density = (
        0.5 * yp * yp
        +0.5 * omega * omega * y * y
        +potential
    )

    scalar_density = (
        0.5 * up * up
        +0.5 * epsilon * epsilon * u * u
    ) / (chi * chi)

    I_X_ON = integrate_spherical(
        x,
        source_on_density,
    )

    I_X_OFF_INVENTORY = integrate_spherical(
        x,
        source_off_inventory_density,
    )

    I_PHI_INSIDE = integrate_spherical(
        x,
        scalar_density,
    )

    u_boundary = float(
        solution.sol(
            X_MATCH_SOURCE
        )[2]
    )

    I_PHI_TAIL = scalar_tail_integral(
        u_boundary,
        epsilon,
        chi,
        X_MATCH_SOURCE,
    )

    I_PHI = (
        I_PHI_INSIDE
        +I_PHI_TAIL
    )

    I_ON = (
        I_X_ON
        +I_PHI
    )

    I_INVENTORY = (
        I_X_OFF_INVENTORY
        +I_PHI
    )

    I_Q = float(
        4.0
        * math.pi
        * omega
        * np.trapezoid(
            x * x * y * y,
            x,
        )
    )

    return {
        "I_X_ON": I_X_ON,
        "I_X_OFF_INVENTORY":
            I_X_OFF_INVENTORY,
        "I_PHI_INSIDE":
            I_PHI_INSIDE,
        "I_PHI_TAIL":
            I_PHI_TAIL,
        "I_PHI":
            I_PHI,
        "I_ON":
            I_ON,
        "I_INVENTORY":
            I_INVENTORY,
        "I_Q":
            I_Q,
        "E_over_QmX":
            I_ON / I_Q,
    }


def uncoupled_integrals(
    solution,
    omega: float,
) -> dict[str, float]:

    x = np.linspace(
        1.0e-5,
        X_MATCH_SOURCE,
        16_000,
    )

    state = solution.sol(x)

    y = np.asarray(
        state[0],
        dtype=float,
    )

    yp = np.asarray(
        state[1],
        dtype=float,
    )

    density = (
        0.5 * yp * yp
        +0.5 * omega * omega * y * y
        +W(y)
    )

    I_E = integrate_spherical(
        x,
        density,
    )

    I_Q = float(
        4.0
        * math.pi
        * omega
        * np.trapezoid(
            x * x * y * y,
            x,
        )
    )

    return {
        "I_E": I_E,
        "I_Q": I_Q,
        "E_over_QmX": (
            I_E / I_Q
            if I_Q > 0.0
            else math.inf
        ),
    }


def profile_y_extended(
    solution,
    omega: float,
    r: np.ndarray,
) -> np.ndarray:
    """
    Evaluate y inside the solved Q-ball domain and continue its tiny
    asymptotic tail analytically outside X_MATCH_SOURCE.
    """

    r = np.asarray(
        r,
        dtype=float,
    )

    clipped = np.minimum(
        r,
        X_MATCH_SOURCE,
    )

    y = np.asarray(
        solution.sol(
            np.maximum(
                clipped,
                1.0e-5,
            )
        )[0],
        dtype=float,
    )

    outside = (
        r
        > X_MATCH_SOURCE
    )

    if np.any(outside):
        y_R = float(
            solution.sol(
                X_MATCH_SOURCE
            )[0]
        )

        decay = math.sqrt(
            max(
                1.0 - omega * omega,
                1.0e-12,
            )
        )

        rr = r[outside]

        y[outside] = (
            y_R
            * X_MATCH_SOURCE
            / rr
            * np.exp(
                -decay
                * (
                    rr
                    - X_MATCH_SOURCE
                )
            )
        )

    return y


def off_hessian_row(
    solution,
    omega: float,
    epsilon: float,
    chi: float,
    epsilon_rmax: float,
    h_target: float,
) -> dict[str, float]:
    """
    Conservative Dirichlet reduced-radial Hessian.

    Dirichlet at the outer boundary restricts the variational space and
    therefore raises the lowest eigenvalue. Thus a robust negative result
    here is sufficient to prove an infinite-domain negative direction.
    """

    rmax = (
        epsilon_rmax
        / epsilon
    )

    intervals = max(
        int(round(
            rmax / h_target
        )),
        40,
    )

    h = (
        rmax
        / intervals
    )

    r = (
        np.arange(
            1,
            intervals,
            dtype=float,
        )
        * h
    )

    y = profile_y_extended(
        solution,
        omega,
        r,
    )

    potential = (
        epsilon * epsilon
        -chi * chi * W(y)
    )

    diagonal = (
        2.0 / (h * h)
        +potential
    )

    off = (
        -np.ones(
            len(diagonal) - 1,
            dtype=float,
        )
        / (h * h)
    )

    eigs = eigh_tridiagonal(
        diagonal,
        off,
        select="i",
        select_range=(0, 2),
        eigvals_only=True,
        check_finite=True,
    )

    lambda0 = float(eigs[0])

    growth = (
        math.sqrt(-lambda0)
        if lambda0 < 0.0
        else 0.0
    )

    return {
        "epsilon_rmax":
            float(epsilon_rmax),
        "rmax":
            float(rmax),
        "h_target":
            float(h_target),
        "h":
            float(h),
        "intervals":
            int(intervals),
        "lambda0":
            lambda0,
        "lambda1":
            float(eigs[1]),
        "lambda2":
            float(eigs[2]),
        "growth_dimensionless":
            growth,
        "potential_min":
            float(np.min(potential)),
        "potential_center_proxy":
            float(potential[0]),
    }


def main() -> None:
    print(
        "=== 031D1 Q-BALL FIXED-CHARGE OFF-STATE GATE ==="
    )

    print(
        "CLAIM_CLASS="
        "SELF_ACTIVATION_OFFSTATE_FIXED_NOETHER_CHARGE_PREFLIGHT"
    )

    print(
        "AUXILIARY_GATE_FIELD_INCLUDED=NO"
    )

    print(
        "CONTROL_ENERGY_INCLUDED=NO"
    )

    print(
        "OFF_STATE_LINEAR_MATTER_COUPLING="
        "ZERO_BY_EVEN_Z2_AT_U0"
    )

    print(
        "FIXED_CHARGE_SCALAR_MODE_DECOUPLES_AT_LINEAR_ORDER=YES"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    for path in (
        QBALL_SOURCE,
        ROBUST_SUMMARY,
        D96_SUMMARY,
    ):
        require(path)

    robust = json.loads(
        ROBUST_SUMMARY.read_text()
    )

    d96 = json.loads(
        D96_SUMMARY.read_text()
    )

    if not bool(
        robust.get(
            "family_operating_robustness_green",
            False,
        )
    ):
        raise RuntimeError(
            "031C96 robust operating family is not GREEN"
        )

    if not str(
        d96.get(
            "classification",
            "",
        )
    ).startswith(
        "GREEN_96GJ_INTRINSIC_QBALL"
    ):
        raise RuntimeError(
            "D96 intrinsic source stability is not GREEN"
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

    omega_on = float(
        candidate["omega"]
    )

    epsilon = float(
        candidate["epsilon"]
    )

    chi = float(
        candidate["chi"]
    )

    m_x_gev = float(
        candidate["m_x_gev_derived"]
    )

    F_gev = float(
        quadrature["F_gev"]
    )

    robust_inventory_j = float(
        operating["energy_J"]
    )

    stored_e_over_q = float(
        candidate["E_over_QmX"]
    )

    print(
        f"OMEGA_ON={omega_on:.15e}"
    )

    print(
        f"EPSILON={epsilon:.15e}"
    )

    print(
        f"CHI={chi:.15e}"
    )

    print(
        f"M_X_GEV={m_x_gev:.15e}"
    )

    print(
        f"F_GEV_ROBUST_POINT={F_gev:.15e}"
    )

    print(
        f"ROBUST_20PCT_INVENTORY_J="
        f"{robust_inventory_j:.15e}"
    )

    qmod = load_module(
        "qball031d1",
        QBALL_SOURCE,
    )

    original_x_match = float(
        qmod.X_MATCH
    )

    qmod.X_MATCH = X_MATCH_SOURCE

    try:
        print(
            "\n=== STAGE A: RECONSTRUCT GREEN ON STATE ==="
        )

        seed_on = qmod.solve_uncoupled_qball(
            omega_on
        )

        if seed_on is None:
            raise RuntimeError(
                "Failed to reconstruct uncoupled seed at Omega_on"
            )

        on_solution = qmod.solve_coupled(
            seed_on,
            omega_on,
            epsilon,
            chi,
            previous=None,
        )

        if on_solution is None:
            raise RuntimeError(
                "Failed to reconstruct scalarized on state"
            )

        on = coupled_integrals(
            on_solution,
            omega_on,
            epsilon,
            chi,
        )

        e_over_q_relerr = relerr(
            on["E_over_QmX"],
            stored_e_over_q,
        )

        energy_prefactor = (
            F_gev * F_gev
            / m_x_gev
            * J_PER_GEV
        )

        on_dynamic_j = (
            on["I_ON"]
            * energy_prefactor
        )

        on_inventory_j = (
            on["I_INVENTORY"]
            * energy_prefactor
        )

        inventory_relerr = relerr(
            on_inventory_j,
            robust_inventory_j,
        )

        q_absolute = (
            on["I_Q"]
            * F_gev * F_gev
            / (m_x_gev * m_x_gev)
        )

        on_reconstruction_pass = bool(
            e_over_q_relerr
            <= ON_E_OVER_Q_REL_TOL
            and
            inventory_relerr
            <= INVENTORY_REPRO_REL_TOL
        )

        print(
            f"ON_I_Q={on['I_Q']:.15e}"
        )

        print(
            f"ON_I_ON={on['I_ON']:.15e}"
        )

        print(
            f"ON_I_INVENTORY="
            f"{on['I_INVENTORY']:.15e}"
        )

        print(
            f"ON_E_OVER_QMX="
            f"{on['E_over_QmX']:.15e}"
        )

        print(
            f"STORED_E_OVER_QMX="
            f"{stored_e_over_q:.15e}"
        )

        print(
            f"ON_E_OVER_QMX_RELERR="
            f"{e_over_q_relerr:.15e}"
        )

        print(
            f"ON_DYNAMIC_ENERGY_GJ="
            f"{on_dynamic_j / 1.0e9:.12f}"
        )

        print(
            f"ON_INVENTORY_RECONSTRUCTED_GJ="
            f"{on_inventory_j / 1.0e9:.12f}"
        )

        print(
            f"ON_INVENTORY_RELERR="
            f"{inventory_relerr:.15e}"
        )

        print(
            f"NOETHER_CHARGE_ABSOLUTE="
            f"{q_absolute:.15e}"
        )

        print(
            "ON_RECONSTRUCTION_PASS="
            f"{on_reconstruction_pass}"
        )

        print(
            "\n=== STAGE B: UNACTIVATED u=0 Q-BALL FAMILY ==="
        )

        cache: dict[
            float,
            tuple[
                object | None,
                dict[str, float] | None,
            ]
        ] = {}

        scan_rows: list[
            dict[str, Any]
        ] = []

        def solve_off(
            omega: float,
        ):
            key = round(
                float(omega),
                12,
            )

            if key in cache:
                return cache[key]

            solution = (
                qmod.solve_uncoupled_qball(
                    float(omega)
                )
            )

            if solution is None:
                cache[key] = (
                    None,
                    None,
                )

                return cache[key]

            metrics = uncoupled_integrals(
                solution,
                float(omega),
            )

            cache[key] = (
                solution,
                metrics,
            )

            return cache[key]

        target_q = float(
            on["I_Q"]
        )

        valid_scan = []

        for omega in OMEGA_SCAN:
            solution, metrics = solve_off(
                float(omega)
            )

            if solution is None:
                row = {
                    "scan_type":
                        "omega_scan",
                    "omega":
                        float(omega),
                    "success":
                        False,
                }

                scan_rows.append(row)

                print(
                    f"OFF_SCAN OMEGA={omega:.9f} "
                    "SUCCESS=False"
                )

                continue

            residual = (
                float(metrics["I_Q"])
                -target_q
            )

            row = {
                "scan_type":
                    "omega_scan",
                "omega":
                    float(omega),
                "success":
                    True,
                "I_Q":
                    float(metrics["I_Q"]),
                "I_E":
                    float(metrics["I_E"]),
                "E_over_QmX":
                    float(
                        metrics[
                            "E_over_QmX"
                        ]
                    ),
                "Q_residual":
                    residual,
                "Q_rel_residual":
                    abs(residual)
                    / max(
                        abs(target_q),
                        1.0e-300,
                    ),
            }

            scan_rows.append(row)
            valid_scan.append(row)

            print(
                f"OFF_SCAN OMEGA={omega:.9f} "
                f"I_Q={metrics['I_Q']:.9e} "
                f"Q_RES={residual:+.9e} "
                f"E_OVER_QMX="
                f"{metrics['E_over_QmX']:.9e}"
            )

        valid_scan.sort(
            key=lambda row:
            float(row["omega"])
        )

        brackets = []

        for left, right in zip(
            valid_scan[:-1],
            valid_scan[1:],
            strict=True,
        ):
            f_left = float(
                left["Q_residual"]
            )

            f_right = float(
                right["Q_residual"]
            )

            if f_left == 0.0:
                brackets.append(
                    (
                        float(left["omega"]),
                        float(left["omega"]),
                    )
                )

            elif (
                f_left * f_right
                < 0.0
            ):
                brackets.append(
                    (
                        float(left["omega"]),
                        float(right["omega"]),
                    )
                )

        roots = []

        def q_residual(
            omega: float,
        ) -> float:
            solution, metrics = solve_off(
                omega
            )

            if (
                solution is None
                or metrics is None
            ):
                raise RuntimeError(
                    "Off-family solve failed inside Q root"
                )

            return (
                float(metrics["I_Q"])
                -target_q
            )

        for left, right in brackets:
            if left == right:
                root = left
            else:
                root = float(
                    brentq(
                        q_residual,
                        left,
                        right,
                        xtol=ROOT_XTOL,
                        rtol=ROOT_RTOL,
                        maxiter=100,
                    )
                )

            if not any(
                abs(root - old)
                < 2.0e-6
                for old in roots
            ):
                roots.append(root)

        roots.sort()

        print(
            f"SAME_Q_OFF_ROOT_COUNT={len(roots)}"
        )

        print(
            "\n=== STAGE C: SAME-Q OFF BRANCH DIAGNOSTICS ==="
        )

        root_records = []
        hessian_rows = []

        for root_id, omega_off in enumerate(
            roots
        ):
            solution, metrics = solve_off(
                omega_off
            )

            if (
                solution is None
                or metrics is None
            ):
                continue

            q_rel = relerr(
                float(metrics["I_Q"]),
                target_q,
            )

            d = DQ_DOMEGA_STEP

            minus_solution, minus_metrics = (
                solve_off(
                    omega_off - d
                )
            )

            plus_solution, plus_metrics = (
                solve_off(
                    omega_off + d
                )
            )

            if (
                minus_metrics is not None
                and
                plus_metrics is not None
            ):
                dq_domega = (
                    float(
                        plus_metrics[
                            "I_Q"
                        ]
                    )
                    -
                    float(
                        minus_metrics[
                            "I_Q"
                        ]
                    )
                ) / (2.0 * d)
            else:
                dq_domega = math.nan

            qball_bound = bool(
                float(
                    metrics[
                        "E_over_QmX"
                    ]
                )
                < E_OVER_QMX_BOUND
            )

            slope_stable = bool(
                math.isfinite(
                    dq_domega
                )
                and
                dq_domega < 0.0
            )

            source_viable = bool(
                q_rel <= Q_MATCH_REL_TOL
                and
                qball_bound
                and
                slope_stable
            )

            chi_critical = (
                qmod.scalarization_critical_chi(
                    solution,
                    epsilon,
                )
            )

            chi_over_critical = (
                chi / chi_critical
                if (
                    chi_critical is not None
                    and
                    chi_critical > 0.0
                )
                else math.nan
            )

            off_energy_j = (
                float(
                    metrics["I_E"]
                )
                * energy_prefactor
            )

            delta_off_minus_on_j = (
                off_energy_j
                -on_dynamic_j
            )

            print(
                f"OFF_ROOT={root_id} "
                f"OMEGA={omega_off:.12e} "
                f"Q_RELERR={q_rel:.6e} "
                f"E_OVER_QMX="
                f"{metrics['E_over_QmX']:.9e} "
                f"DQ_DOMEGA="
                f"{dq_domega:+.9e} "
                f"SOURCE_VIABLE="
                f"{source_viable} "
                f"CHI_CRIT="
                f"{chi_critical if chi_critical is not None else math.nan:.9e} "
                f"CHI_OVER_CRIT="
                f"{chi_over_critical:.9e} "
                f"E_OFF_GJ="
                f"{off_energy_j / 1.0e9:.9f}"
            )

            local_rows = []

            for epsilon_rmax in (
                DOMAIN_EPS_R_VALUES
            ):
                for h_target in H_TARGETS:
                    row = off_hessian_row(
                        solution,
                        omega_off,
                        epsilon,
                        chi,
                        epsilon_rmax,
                        h_target,
                    )

                    row.update(
                        {
                            "root_id":
                                root_id,
                            "omega_off":
                                omega_off,
                        }
                    )

                    local_rows.append(row)
                    hessian_rows.append(row)

                    print(
                        f"OFF_HESSIAN ROOT={root_id} "
                        f"EPS_R={epsilon_rmax:.3f} "
                        f"H={row['h']:.9f} "
                        f"LAMBDA0="
                        f"{row['lambda0']:+.12e} "
                        f"GROWTH="
                        f"{row['growth_dimensionless']:.12e} "
                        f"VMIN="
                        f"{row['potential_min']:+.12e}"
                    )

            def get_row(
                eps_r: float,
                h_target: float,
            ):
                candidates = [
                    row
                    for row in local_rows
                    if abs(
                        float(
                            row[
                                "epsilon_rmax"
                            ]
                        )
                        -eps_r
                    ) < 1.0e-12
                    and
                    abs(
                        float(
                            row[
                                "h_target"
                            ]
                        )
                        -h_target
                    ) < 1.0e-12
                ]

                if len(candidates) != 1:
                    raise RuntimeError(
                        "Missing Hessian convergence row"
                    )

                return candidates[0]

            fine5 = get_row(
                5.0,
                0.25,
            )

            coarse5 = get_row(
                5.0,
                0.50,
            )

            fine3 = get_row(
                3.0,
                0.25,
            )

            lambda_fine = float(
                fine5["lambda0"]
            )

            grid_rel = relerr(
                lambda_fine,
                float(
                    coarse5[
                        "lambda0"
                    ]
                ),
            )

            domain_rel = relerr(
                lambda_fine,
                float(
                    fine3[
                        "lambda0"
                    ]
                ),
            )

            negative_all = all(
                float(row["lambda0"])
                < -NEGATIVE_EIGENVALUE_TOL
                for row in local_rows
            )

            robust_tachyon = bool(
                negative_all
                and
                grid_rel
                <= HESSIAN_GRID_REL_TOL
                and
                domain_rel
                <= HESSIAN_DOMAIN_REL_TOL
            )

            growth_dimless = (
                math.sqrt(
                    -lambda_fine
                )
                if lambda_fine < 0.0
                else 0.0
            )

            growth_rate_s = (
                growth_dimless
                * m_x_gev
                / HBAR_GEV_S
            )

            e_fold_s = (
                1.0 / growth_rate_s
                if growth_rate_s > 0.0
                else math.inf
            )

            delta_m2_hat_critical = max(
                0.0,
                -lambda_fine,
            )

            delta_m2_over_mphi2 = (
                delta_m2_hat_critical
                / (epsilon * epsilon)
            )

            m_eff_over_mphi = math.sqrt(
                1.0
                +delta_m2_over_mphi2
            )

            m_x_ev = (
                m_x_gev
                * 1.0e9
            )

            delta_m2_ev2 = (
                delta_m2_hat_critical
                * m_x_ev * m_x_ev
            )

            record = {
                "root_id":
                    root_id,
                "omega_off":
                    omega_off,
                "I_Q":
                    float(metrics["I_Q"]),
                "Q_match_relerr":
                    q_rel,
                "I_E":
                    float(metrics["I_E"]),
                "E_over_QmX":
                    float(
                        metrics[
                            "E_over_QmX"
                        ]
                    ),
                "dq_domega":
                    dq_domega,
                "qball_bound":
                    qball_bound,
                "slope_stable":
                    slope_stable,
                "source_viable":
                    source_viable,
                "chi_critical":
                    chi_critical,
                "chi_over_critical":
                    chi_over_critical,
                "off_energy_J":
                    off_energy_j,
                "off_minus_on_dynamic_J":
                    delta_off_minus_on_j,
                "lambda0_fine":
                    lambda_fine,
                "hessian_grid_rel_difference":
                    grid_rel,
                "hessian_domain_rel_difference":
                    domain_rel,
                "robust_tachyon":
                    robust_tachyon,
                "growth_dimensionless":
                    growth_dimless,
                "growth_rate_s_inverse":
                    growth_rate_s,
                "e_fold_time_s":
                    e_fold_s,
                "critical_positive_delta_m2_hat":
                    delta_m2_hat_critical,
                "critical_delta_m2_over_mphi2":
                    delta_m2_over_mphi2,
                "critical_m_eff_over_mphi":
                    m_eff_over_mphi,
                "critical_delta_m2_eV2":
                    delta_m2_ev2,
            }

            root_records.append(
                record
            )

            scan_rows.append(
                {
                    "scan_type":
                        "same_q_root",
                    **record,
                }
            )

            print(
                f"OFF_ROOT_DECISION={root_id} "
                f"LAMBDA_FINE="
                f"{lambda_fine:+.12e} "
                f"GRID_REL="
                f"{grid_rel:.6e} "
                f"DOMAIN_REL="
                f"{domain_rel:.6e} "
                f"ROBUST_TACHYON="
                f"{robust_tachyon} "
                f"EFOLD_S="
                f"{e_fold_s:.9e} "
                f"DELTA_M2_OVER_MPHI2="
                f"{delta_m2_over_mphi2:.9e}"
            )

        print(
            "\n=== STAGE D: FIXED-CHARGE OFF-STATE DECISION ==="
        )

        viable = [
            row
            for row in root_records
            if bool(
                row["source_viable"]
            )
        ]

        viable_non_tachyonic = [
            row
            for row in viable
            if not bool(
                row[
                    "robust_tachyon"
                ]
            )
        ]

        all_viable_tachyonic = bool(
            viable
            and
            all(
                bool(
                    row[
                        "robust_tachyon"
                    ]
                )
                for row in viable
            )
        )

        if not on_reconstruction_pass:
            classification = (
                "YELLOW_D1_ON_STATE_"
                "INDEPENDENT_RECONSTRUCTION_FAILED"
            )

            next_action = (
                "DEBUG_D1_PROVENANCE_BEFORE_PHYSICS"
            )

        elif len(roots) == 0:
            classification = (
                "RED_D1_NO_UNSCALARIZED_"
                "SAME_CHARGE_QBALL_BRANCH_FOUND"
            )

            next_action = (
                "031D2D3_AUXILIARY_GATE_OR_"
                "CHARGE_EXPORT_ARCHITECTURE"
            )

        elif len(viable) == 0:
            classification = (
                "RED_D1_NO_SOURCE_STABLE_"
                "UNSCALARIZED_SAME_CHARGE_QBALL_OFF_BRANCH"
            )

            next_action = (
                "031D2D3_AUXILIARY_GATE_OR_"
                "ALTERNATE_OFF_SOURCE_STATE"
            )

        elif all_viable_tachyonic:
            classification = (
                "RED_D1_GATE_FREE_Z2_OFFSTATE_"
                "TACHYONIC_AT_FIXED_NOETHER_CHARGE"
            )

            next_action = (
                "031D2D3_MINIMUM_AUXILIARY_GATE_"
                "MASS_SHIFT_CONTROL_ENERGY_AND_RECIPROCITY"
            )

        else:
            classification = (
                "YELLOW_D1_SAME_CHARGE_OFFSTATE_"
                "NOT_FALSIFIED_REQUIRES_ROBIN_BARRIER_"
                "AND_FULL_GATE_DYNAMICS"
            )

            next_action = (
                "031D1R_ROBIN_OFFSTATE_AND_"
                "SWITCHING_BARRIER_GATE"
            )

        auxiliary_gate_required = bool(
            classification.startswith(
                "RED_D1"
            )
        )

        if viable:
            best_gate_target = max(
                viable,
                key=lambda row:
                float(
                    row[
                        "lambda0_fine"
                    ]
                ),
            )
        else:
            best_gate_target = None

        print(
            f"ON_RECONSTRUCTION_PASS="
            f"{on_reconstruction_pass}"
        )

        print(
            f"SAME_Q_ROOT_COUNT="
            f"{len(roots)}"
        )

        print(
            f"VIABLE_SAME_Q_OFF_BRANCH_COUNT="
            f"{len(viable)}"
        )

        print(
            f"ALL_VIABLE_OFF_BRANCHES_TACHYONIC="
            f"{all_viable_tachyonic}"
        )

        print(
            f"AUXILIARY_GATE_REQUIRED="
            f"{auxiliary_gate_required}"
        )

        if best_gate_target is not None:
            print(
                "BEST_OFF_BRANCH_CRITICAL_"
                "DELTA_M2_OVER_MPHI2="
                f"{best_gate_target['critical_delta_m2_over_mphi2']:.15e}"
            )

            print(
                "BEST_OFF_BRANCH_CRITICAL_"
                "M_EFF_OVER_MPHI="
                f"{best_gate_target['critical_m_eff_over_mphi']:.15e}"
            )

            print(
                "BEST_OFF_BRANCH_"
                "EFOLD_TIME_S="
                f"{best_gate_target['e_fold_time_s']:.15e}"
            )

        print(
            "031D1_CLASSIFICATION="
            f"{classification}"
        )

        print(
            "NEXT="
            f"{next_action}"
        )

        print(
            "ACTIVATION_OFFSTATE_CLOSED="
            +(
                "NO_GATE_FREE_ROUTE_FALSIFIED"
                if auxiliary_gate_required
                else "NO"
            )
        )

        print(
            "GATE_CONTROL_ENERGY_CLOSED=NO"
        )

        print(
            "RECIPROCITY_CLOSED=NO"
        )

        print(
            "FINITE_AMPLITUDE_FRAGMENTATION_CLOSED=NO"
        )

        print(
            "FULL_METRIC_BACKREACTION_CLOSED=NO"
        )

        print(
            "RADIATIVE_NATURALNESS_CLOSED=NO"
        )

        print(
            "EMPIRICAL_FIFTH_FORCE_CLOSURE=NO"
        )

        print(
            "PRACTICAL_DEVICE=NO"
        )

        summary = {
            "classification":
                classification,
            "next":
                next_action,
            "question":
                (
                    "Can the current Q-ball remain "
                    "unscalarized at the same conserved "
                    "Noether charge?"
                ),
            "model": {
                "omega_on":
                    omega_on,
                "epsilon":
                    epsilon,
                "chi":
                    chi,
                "m_x_gev":
                    m_x_gev,
                "F_gev_robust_point":
                    F_gev,
                "off_state_linear_matter_coupling":
                    0.0,
                "fixed_charge_scalar_decoupling_linear":
                    True,
            },
            "on_state": {
                **on,
                "stored_E_over_QmX":
                    stored_e_over_q,
                "E_over_QmX_relerr":
                    e_over_q_relerr,
                "dynamic_energy_J":
                    on_dynamic_j,
                "inventory_reconstructed_J":
                    on_inventory_j,
                "robust_inventory_reference_J":
                    robust_inventory_j,
                "inventory_relerr":
                    inventory_relerr,
                "absolute_noether_charge":
                    q_absolute,
                "reconstruction_pass":
                    on_reconstruction_pass,
            },
            "same_q_roots":
                root_records,
            "same_q_root_count":
                len(roots),
            "viable_same_q_off_branch_count":
                len(viable),
            "all_viable_off_branches_tachyonic":
                all_viable_tachyonic,
            "auxiliary_gate_required":
                auxiliary_gate_required,
            "best_gate_target":
                best_gate_target,
            "claim_limits": [
                (
                    "This tests only the gate-free u=0 "
                    "off state of the current single-field "
                    "Z2 Q-ball model."
                ),
                (
                    "A RED result does not close all "
                    "activation architectures."
                ),
                (
                    "The outer Dirichlet Hessian is "
                    "conservative for proving a negative mode."
                ),
                (
                    "Auxiliary gate stress-energy and "
                    "control energy are not included."
                ),
                (
                    "Finite-amplitude fragmentation/fission "
                    "remains open."
                ),
                (
                    "Full physical-metric backreaction "
                    "remains open."
                ),
                (
                    "Radiative naturalness and empirical "
                    "closure remain open."
                ),
                (
                    "No practical device is established."
                ),
            ],
        }

        OUT_JSON.write_text(
            json.dumps(
                to_builtin(summary),
                indent=2,
                sort_keys=True,
            )
            + "\n"
        )

        charge_fields = sorted(
            {
                key
                for row in scan_rows
                for key in row.keys()
            }
        )

        with OUT_CHARGE_CSV.open(
            "w",
            newline="",
        ) as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=charge_fields,
            )

            writer.writeheader()
            writer.writerows(
                scan_rows
            )

        if hessian_rows:
            hessian_fields = sorted(
                {
                    key
                    for row in hessian_rows
                    for key in row.keys()
                }
            )

            with OUT_HESSIAN_CSV.open(
                "w",
                newline="",
            ) as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=hessian_fields,
                )

                writer.writeheader()
                writer.writerows(
                    hessian_rows
                )

        else:
            OUT_HESSIAN_CSV.write_text(
                "root_id,omega_off\n"
            )

        print(
            f"SUMMARY_JSON={OUT_JSON}"
        )

        print(
            f"CHARGE_SCAN_CSV={OUT_CHARGE_CSV}"
        )

        print(
            f"HESSIAN_SCAN_CSV={OUT_HESSIAN_CSV}"
        )

    finally:
        qmod.X_MATCH = original_x_match


if __name__ == "__main__":
    main()
