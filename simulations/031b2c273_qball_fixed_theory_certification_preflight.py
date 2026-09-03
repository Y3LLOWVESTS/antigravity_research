"""
031B2-C273
==========

Fixed-theory certification preflight for the 273-GJ coupled Q-ball source.

This run does NOT optimize the energy downward.

It asks whether the already-promoted 031B2-A best source remains internally
consistent under independent reconstruction and fixed-theory branch tests.

Primary tests:

1. Reconstruct the exact best Q-ball + scalar BVP.
2. Reproduce the stored 273.46-GJ ledger and physical diagnostics.
3. Hold epsilon and chi fixed and continue the SAME THEORY in omega.
4. Test the standard Q-ball branch-slope diagnostic dQ/domega < 0.
5. Independently test the stationary variational identity dE/dQ ~= omega.
6. Compute scalar fluctuation eigenvalues for l=0..8.
7. Reproduce the previously stored l=0 scalar Hessian.
8. Quantify source length scales, field excursions, cross coupling,
   and simple one-loop scalar-mass naturalness diagnostics.
9. Preserve all open claims:
   full coupled nonradial source stability,
   fragmentation,
   activation/off-state,
   UV completion,
   empirical closure,
   full metric backreaction.

This is a certification preflight, not final end-to-end proof.
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

from scipy.integrate import cumulative_trapezoid, quad
from scipy.linalg import eigh_tridiagonal


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
    "031b2c273_qball_fixed_theory_certification_summary.json"
)

OUT_CSV = (
    DATA
    /
    "031b2c273_qball_fixed_theory_continuation.csv"
)


C = 299_792_458.0

MPL_GEV = 2.435e18
HBARC_GEV_M = 1.973269804e-16
J_PER_GEV = 1.602176634e-10

PROVENANCE_REL_TOL = 5.0e-4
VARIATIONAL_REL_TOL = 3.0e-2
HESSIAN_REPRO_REL_TOL = 3.0e-2

LMAX = 8

OMEGA_OFFSETS = (
    -0.060,
    -0.040,
    -0.025,
    -0.015,
    0.000,
    0.015,
    0.025,
    0.040,
    0.060,
)


def require(path: Path) -> None:

    if not path.is_file():

        raise RuntimeError(
            f"Required file missing: {path}"
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

    sys.modules[
        spec.name
    ] = module

    spec.loader.exec_module(
        module
    )

    return module


def relerr(a: float, b: float) -> float:

    return (
        abs(a - b)
        /
        max(
            abs(a),
            abs(b),
            1.0e-300,
        )
    )


def to_builtin(value: Any):

    if isinstance(value, np.generic):

        return value.item()

    if isinstance(value, np.ndarray):

        return value.tolist()

    if isinstance(value, dict):

        return {
            str(key):
            to_builtin(item)
            for key, item
            in value.items()
        }

    if isinstance(value, (list, tuple)):

        return [
            to_builtin(item)
            for item
            in value
        ]

    return value


def branch_integrals(
    qmod,
    solution,
    omega,
    epsilon,
    chi,
):

    x_match = float(
        qmod.X_MATCH
    )

    x = np.linspace(
        1.0e-5,
        x_match,
        9000,
    )

    y, yp, u, up = solution.sol(
        x
    )

    A = np.exp(
        np.clip(
            -0.5
            *
            u**2,
            -700.0,
            0.0,
        )
    )

    potential = qmod.W(
        y
    )

    source_density = (
        0.5
        *
        yp**2
        +
        0.5
        *
        omega**2
        *
        y**2
        +
        A
        *
        potential
    )

    scalar_density = (
        (
            0.5
            *
            up**2
            +
            0.5
            *
            epsilon**2
            *
            u**2
        )
        /
        chi**2
    )

    def integrate(density):

        return float(
            4.0
            *
            math.pi
            *
            np.trapezoid(
                x**2
                *
                density,
                x,
            )
        )

    I_source = integrate(
        source_density
    )

    I_phi_inside = integrate(
        scalar_density
    )

    u_boundary = float(
        solution.sol(
            x_match
        )[
            2
        ]
    )

    def tail_integrand(xx):

        uu = (
            u_boundary
            *
            x_match
            /
            xx
            *
            math.exp(
                -epsilon
                *
                (
                    xx
                    -
                    x_match
                )
            )
        )

        uup = (
            uu
            *
            (
                -epsilon
                -
                1.0
                /
                xx
            )
        )

        return (
            4.0
            *
            math.pi
            *
            xx**2
            *
            (
                0.5
                *
                uup**2
                +
                0.5
                *
                epsilon**2
                *
                uu**2
            )
            /
            chi**2
        )

    I_phi_tail = float(
        quad(
            tail_integrand,
            x_match,
            np.inf,
            epsabs=1.0e-12,
            epsrel=1.0e-8,
            limit=200,
        )[
            0
        ]
    )

    I_E = (
        I_source
        +
        I_phi_inside
        +
        I_phi_tail
    )

    I_Q = float(
        4.0
        *
        math.pi
        *
        omega
        *
        np.trapezoid(
            x**2
            *
            y**2,
            x,
        )
    )

    source_shell = (
        4.0
        *
        math.pi
        *
        x**2
        *
        source_density
    )

    cumulative = np.concatenate(
        (
            [
                0.0
            ],
            cumulative_trapezoid(
                source_shell,
                x,
            ),
        )
    )

    return {
        "x":
        x,

        "y":
        y,

        "u":
        u,

        "I_E":
        I_E,

        "I_Q":
        I_Q,

        "I_source":
        I_source,

        "source_cumulative":
        cumulative,
    }


def scalar_l_eigenvalue(
    qmod,
    solution,
    epsilon,
    chi,
    ell,
):

    x_match = float(
        qmod.X_MATCH
    )

    n = 1400

    x = np.linspace(
        0.0,
        x_match,
        n,
    )

    h = (
        x[
            1
        ]
        -
        x[
            0
        ]
    )

    r = x[
        1:-1
    ]

    state = solution.sol(
        np.maximum(
            r,
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

    potential = (
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

    angular = (
        ell
        *
        (
            ell
            +
            1
        )
        /
        r**2
    )

    diagonal = (
        2.0
        /
        h**2
        +
        potential
        +
        angular
    )

    off = (
        -np.ones(
            len(
                diagonal
            )
            -
            1
        )
        /
        h**2
    )

    eig = eigh_tridiagonal(
        diagonal,
        off,
        select="i",
        select_range=(
            0,
            0,
        ),
        eigvals_only=True,
    )[
        0
    ]

    return float(
        eig
    )


def reconstruct_solution(
    qmod,
    omega,
    epsilon,
    chi,
    previous=None,
):

    seed = qmod.solve_uncoupled_qball(
        omega
    )

    if seed is None:

        return None

    return qmod.solve_coupled(
        seed,
        omega,
        epsilon,
        chi,
        previous=previous,
    )


def main():

    print(
        "=== 031B2-C273 FIXED-THEORY "
        "Q-BALL CERTIFICATION PREFLIGHT ==="
    )

    print(
        "CLAIM_CLASS="
        "MICROSCOPIC_SOURCE_FIXED_THEORY_"
        "STABILITY_AND_VARIATIONAL_AUDIT"
    )

    print(
        "ENERGY_OPTIMIZATION=DISABLED"
    )

    print(
        "PRACTICAL_DEVICE=NO"
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
        "c273_upstream_qball",
        UPSTREAM,
    )

    omega0 = float(
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

    alpha_m = float(
        summary[
            "alpha_m_on_cap"
        ]
    )

    target_energy = float(
        summary[
            "target_energy_J"
        ]
    )

    mediator_range = float(
        summary[
            "mediator_range_m"
        ]
    )

    print(
        f"REFERENCE_E_INVENTORY_J="
        f"{float(best['E_inventory_J']):.15e}"
    )

    print(
        f"OMEGA0="
        f"{omega0:.15e}"
    )

    print(
        f"EPSILON="
        f"{epsilon:.15e}"
    )

    print(
        f"CHI="
        f"{chi:.15e}"
    )

    print(
        "\n=== A — EXACT BEST-CASE RECONSTRUCTION ==="
    )

    solution0 = reconstruct_solution(
        qmod,
        omega0,
        epsilon,
        chi,
        previous=None,
    )

    if solution0 is None:

        raise RuntimeError(
            "Best Q-ball reconstruction failed"
        )

    rebuilt = qmod.evaluate_case(
        solution0,
        omega0,
        epsilon,
        chi,
        target_energy,
        alpha_m,
        mediator_range,
    )

    if not rebuilt.get(
        "success",
        False,
    ):

        raise RuntimeError(
            f"Best Q-ball evaluation failed: {rebuilt}"
        )

    provenance_fields = (
        "E_inventory_J",
        "E_on_J",
        "E_over_QmX",
        "source_leak_fraction",
        "payload_x_overlap_fraction",
        "payload_backreaction_ratio",
        "scalar_fixed_x_hessian",
        "conservation_rel",
    )

    provenance_pass = True

    for key in provenance_fields:

        old = float(
            best[
                key
            ]
        )

        new = float(
            rebuilt[
                key
            ]
        )

        error = relerr(
            new,
            old,
        )

        passed = (
            error
            <=
            PROVENANCE_REL_TOL
        )

        provenance_pass = (
            provenance_pass
            and
            passed
        )

        print(
            f"PROVENANCE "
            f"KEY={key} "
            f"STORED={old:.15e} "
            f"REBUILT={new:.15e} "
            f"RELERR={error:.9e} "
            f"PASS={passed}"
        )

    print(
        f"C273_PROVENANCE_PASS="
        f"{provenance_pass}"
    )

    print(
        "\n=== B — FIXED-THEORY OMEGA CONTINUATION ==="
    )

    requested = sorted(
        set(
            omega0
            +
            np.asarray(
                OMEGA_OFFSETS,
                dtype=float,
            )
        )
    )

    requested = [
        value
        for value
        in requested
        if (
            value
            >
            0.05
            and
            value
            <
            0.98
        )
    ]

    lower = sorted(
        [
            value
            for value
            in requested
            if value
            <
            omega0
        ],
        reverse=True,
    )

    upper = sorted(
        [
            value
            for value
            in requested
            if value
            >
            omega0
        ]
    )

    solved = {
        omega0:
        solution0,
    }

    previous = solution0

    for omega in lower:

        sol = reconstruct_solution(
            qmod,
            omega,
            epsilon,
            chi,
            previous=previous,
        )

        if sol is not None:

            solved[
                omega
            ] = sol

            previous = sol

    previous = solution0

    for omega in upper:

        sol = reconstruct_solution(
            qmod,
            omega,
            epsilon,
            chi,
            previous=previous,
        )

        if sol is not None:

            solved[
                omega
            ] = sol

            previous = sol

    continuation_rows = []

    for omega in sorted(
        solved
    ):

        integ = branch_integrals(
            qmod,
            solved[
                omega
            ],
            omega,
            epsilon,
            chi,
        )

        row = {
            "omega":
            float(
                omega
            ),

            "I_E":
            integ[
                "I_E"
            ],

            "I_Q":
            integ[
                "I_Q"
            ],

            "E_over_Q_dimensionless":
            (
                integ[
                    "I_E"
                ]
                /
                integ[
                    "I_Q"
                ]
            ),
        }

        continuation_rows.append(
            row
        )

        print(
            f"CONTINUATION "
            f"OMEGA={omega:.9e} "
            f"I_E={row['I_E']:.15e} "
            f"I_Q={row['I_Q']:.15e} "
            f"I_E_OVER_I_Q="
            f"{row['E_over_Q_dimensionless']:.15e}"
        )

    if len(
        continuation_rows
    ) < 5:

        raise RuntimeError(
            "Insufficient fixed-theory continuation points"
        )

    local_rows = sorted(
        continuation_rows,
        key=lambda row:
        abs(
            row[
                "omega"
            ]
            -
            omega0
        ),
    )[
        :7
    ]

    local_rows = sorted(
        local_rows,
        key=lambda row:
        row[
            "omega"
        ],
    )

    omega_values = np.asarray(
        [
            row[
                "omega"
            ]
            -
            omega0
            for row
            in local_rows
        ],
        dtype=float,
    )

    q_values = np.asarray(
        [
            row[
                "I_Q"
            ]
            for row
            in local_rows
        ],
        dtype=float,
    )

    e_values = np.asarray(
        [
            row[
                "I_E"
            ]
            for row
            in local_rows
        ],
        dtype=float,
    )

    degree = min(
        3,
        len(
            local_rows
        )
        -
        1,
    )

    q_poly = np.poly1d(
        np.polyfit(
            omega_values,
            q_values,
            degree,
        )
    )

    e_poly = np.poly1d(
        np.polyfit(
            omega_values,
            e_values,
            degree,
        )
    )

    dQ_domega = float(
        q_poly.deriv()(
            0.0
        )
    )

    dE_domega = float(
        e_poly.deriv()(
            0.0
        )
    )

    q0_fit = float(
        q_poly(
            0.0
        )
    )

    slope_indicator = (
        omega0
        /
        q0_fit
        *
        dQ_domega
    )

    slope_pass = bool(
        slope_indicator
        <
        0.0
    )

    dE_dQ = (
        dE_domega
        /
        dQ_domega
    )

    variational_relerr = relerr(
        dE_dQ,
        omega0,
    )

    variational_pass = bool(
        variational_relerr
        <=
        VARIATIONAL_REL_TOL
    )

    print(
        f"DQ_DOMEGA="
        f"{dQ_domega:.15e}"
    )

    print(
        f"OMEGA_OVER_Q_DQ_DOMEGA="
        f"{slope_indicator:.15e}"
    )

    print(
        f"QBALL_SLOPE_STABILITY_PASS="
        f"{slope_pass}"
    )

    print(
        f"DE_DQ_DIMENSIONLESS="
        f"{dE_dQ:.15e}"
    )

    print(
        f"DE_DQ_VS_OMEGA_RELERR="
        f"{variational_relerr:.15e}"
    )

    print(
        f"STATIONARY_VARIATIONAL_IDENTITY_PASS="
        f"{variational_pass}"
    )

    print(
        "\n=== C — SCALAR ANGULAR-MODE HESSIAN ==="
    )

    l_modes = {}

    all_scalar_modes_positive = True

    for ell in range(
        LMAX
        +
        1
    ):

        eig = scalar_l_eigenvalue(
            qmod,
            solution0,
            epsilon,
            chi,
            ell,
        )

        l_modes[
            str(
                ell
            )
        ] = eig

        positive = bool(
            eig
            >
            0.0
        )

        all_scalar_modes_positive = (
            all_scalar_modes_positive
            and
            positive
        )

        print(
            f"SCALAR_MODE "
            f"L={ell} "
            f"EIG={eig:.15e} "
            f"POSITIVE={positive}"
        )

    l0_relerr = relerr(
        l_modes[
            "0"
        ],
        float(
            best[
                "scalar_fixed_x_hessian"
            ]
        ),
    )

    l0_reproduction_pass = bool(
        l0_relerr
        <=
        HESSIAN_REPRO_REL_TOL
    )

    print(
        f"SCALAR_L0_REPRO_RELERR="
        f"{l0_relerr:.15e}"
    )

    print(
        f"SCALAR_L0_REPRO_PASS="
        f"{l0_reproduction_pass}"
    )

    print(
        f"SCALAR_L0_TO_L{LMAX}_ALL_POSITIVE="
        f"{all_scalar_modes_positive}"
    )

    print(
        "\n=== D — LENGTH SCALE / EFT / "
        "RADIATIVE DIAGNOSTICS ==="
    )

    integ0 = branch_integrals(
        qmod,
        solution0,
        omega0,
        epsilon,
        chi,
    )

    x = integ0[
        "x"
    ]

    cumulative = integ0[
        "source_cumulative"
    ]

    source_total = float(
        cumulative[
            -1
        ]
    )

    def radius_fraction(frac):

        target = (
            frac
            *
            source_total
        )

        index = int(
            np.searchsorted(
                cumulative,
                target,
                side="left",
            )
        )

        index = min(
            max(
                index,
                0,
            ),
            len(
                x
            )
            -
            1,
        )

        return float(
            x[
                index
            ]
        )

    mx_gev = float(
        best[
            "m_x_gev"
        ]
    )

    mphi_gev = (
        HBARC_GEV_M
        /
        mediator_range
    )

    physical_length_per_x = (
        HBARC_GEV_M
        /
        mx_gev
    )

    r50_m = (
        radius_fraction(
            0.50
        )
        *
        physical_length_per_x
    )

    r90_m = (
        radius_fraction(
            0.90
        )
        *
        physical_length_per_x
    )

    gradient_scale_r90_gev = (
        HBARC_GEV_M
        /
        r90_m
    )

    F_gev = float(
        best[
            "F_gev"
        ]
    )

    Mc_gev = float(
        best[
            "M_c_gev"
        ]
    )

    Mm_gev = float(
        best[
            "M_m_gev"
        ]
    )

    u_max = float(
        np.max(
            np.abs(
                integ0[
                    "u"
                ]
            )
        )
    )

    y_max = float(
        np.max(
            np.abs(
                integ0[
                    "y"
                ]
            )
        )
    )

    cross_quartic = (
        mx_gev**2
        /
        Mc_gev**2
    )

    loop_16pi2 = (
        16.0
        *
        math.pi**2
    )

    delta_mphi2_cutoff_Mc = (
        cross_quartic
        *
        Mc_gev**2
        /
        loop_16pi2
    )

    delta_mphi2_cutoff_F = (
        cross_quartic
        *
        F_gev**2
        /
        loop_16pi2
    )

    loop_ratio_Mc = (
        delta_mphi2_cutoff_Mc
        /
        mphi_gev**2
    )

    loop_ratio_F = (
        delta_mphi2_cutoff_F
        /
        mphi_gev**2
    )

    gradient_vs_F = (
        gradient_scale_r90_gev
        /
        F_gev
    )

    gradient_vs_Mc = (
        gradient_scale_r90_gev
        /
        Mc_gev
    )

    compactness = (
        2.0
        *
        6.67430e-11
        *
        (
            float(
                best[
                    "E_inventory_J"
                ]
            )
            /
            C**2
        )
        /
        (
            r90_m
            *
            C**2
        )
    )

    print(
        f"SOURCE_R50_M="
        f"{r50_m:.15e}"
    )

    print(
        f"SOURCE_R90_M="
        f"{r90_m:.15e}"
    )

    print(
        f"GRADIENT_SCALE_R90_GEV="
        f"{gradient_scale_r90_gev:.15e}"
    )

    print(
        f"GRADIENT_OVER_F="
        f"{gradient_vs_F:.15e}"
    )

    print(
        f"GRADIENT_OVER_MC="
        f"{gradient_vs_Mc:.15e}"
    )

    print(
        f"MAX_Y_EQUALS_SIGMA_OVER_F="
        f"{y_max:.15e}"
    )

    print(
        f"MAX_U_EQUALS_PHI_OVER_MC="
        f"{u_max:.15e}"
    )

    print(
        f"X_PHI_CROSS_QUARTIC_ESTIMATE="
        f"{cross_quartic:.15e}"
    )

    print(
        f"ONE_LOOP_DMPHI2_OVER_MPHI2_CUTOFF_F="
        f"{loop_ratio_F:.15e}"
    )

    print(
        f"ONE_LOOP_DMPHI2_OVER_MPHI2_CUTOFF_MC="
        f"{loop_ratio_Mc:.15e}"
    )

    print(
        f"COMPACTNESS_2GM_RC2="
        f"{compactness:.15e}"
    )

    amplitude_expansion_safe = bool(
        y_max
        <
        1.0
        and
        u_max
        <
        1.0
    )

    gradient_eft_pass = bool(
        gradient_vs_F
        <
        1.0e-3
        and
        gradient_vs_Mc
        <
        1.0e-3
    )

    print(
        f"SMALL_FIELD_POLYNOMIAL_EXPANSION_SAFE="
        f"{amplitude_expansion_safe}"
    )

    print(
        f"EXACT_NONPOLYNOMIAL_MODEL_REQUIRED="
        f"{not amplitude_expansion_safe}"
    )

    print(
        f"GRADIENT_EFT_SCALE_PASS="
        f"{gradient_eft_pass}"
    )

    print(
        "RADIATIVE_NATURALNESS_CLOSED=NO"
    )

    print(
        "\n=== E — DECISION ==="
    )

    current_physics_pass = bool(
        provenance_pass
        and
        slope_pass
        and
        variational_pass
        and
        l0_reproduction_pass
        and
        all_scalar_modes_positive
        and
        gradient_eft_pass
        and
        bool(
            rebuilt[
                "DEC_pass"
            ]
        )
        and
        bool(
            rebuilt[
                "conservation_pass"
            ]
        )
        and
        bool(
            rebuilt[
                "noether_decay_pass"
            ]
        )
        and
        bool(
            rebuilt[
                "finite_payload_1g_pass"
            ]
        )
    )

    if current_physics_pass:

        classification = (
            "GREEN_273GJ_QBALL_FIXED_THEORY_"
            "RADIAL_AND_SCALAR_MODE_CERTIFICATION_"
            "PREFLIGHT_RADIATIVE_AND_FULL_COUPLED_"
            "NONRADIAL_STABILITY_OPEN"
        )

        next_step = (
            "031B2D273_AXISYMMETRIC_COUPLED_DYNAMIC_"
            "STABILITY_PLUS_031D_ACTIVATION_GATE"
        )

    else:

        classification = (
            "RED_OR_YELLOW_273GJ_CERTIFICATION_"
            "PREFLIGHT_FOUND_NEW_INTERNAL_FAILURE"
        )

        next_step = (
            "DIAGNOSE_273GJ_FIXED_THEORY_FAILURE_"
            "BEFORE_FURTHER_OPTIMIZATION"
        )

    print(
        f"C273_CURRENT_PHYSICS_CHAIN_PASS="
        f"{current_physics_pass}"
    )

    print(
        "C273_FULL_COUPLED_NONRADIAL_STABILITY="
        "NOT_YET"
    )

    print(
        "C273_FRAGMENTATION_STABILITY="
        "NOT_YET"
    )

    print(
        "C273_ACTIVATION_OFFSTATE="
        "NOT_YET"
    )

    print(
        "C273_FULL_METRIC_BACKREACTION="
        "NOT_YET"
    )

    print(
        f"031B2C273_CLASSIFICATION="
        f"{classification}"
    )

    print(
        f"NEXT="
        f"{next_step}"
    )

    OUT_CSV.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUT_CSV.open(
        "w",
        newline="",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=list(
                continuation_rows[
                    0
                ].keys()
            ),
        )

        writer.writeheader()

        writer.writerows(
            continuation_rows
        )

    result = {
        "claim_class":
        "MICROSCOPIC_SOURCE_FIXED_THEORY_"
        "STABILITY_AND_VARIATIONAL_AUDIT",

        "reference_energy_J":
        float(
            best[
                "E_inventory_J"
            ]
        ),

        "provenance_pass":
        provenance_pass,

        "omega0":
        omega0,

        "epsilon":
        epsilon,

        "chi":
        chi,

        "dQ_domega":
        dQ_domega,

        "slope_indicator":
        slope_indicator,

        "qball_slope_stability_pass":
        slope_pass,

        "dE_dQ_dimensionless":
        dE_dQ,

        "variational_relerr":
        variational_relerr,

        "variational_identity_pass":
        variational_pass,

        "scalar_l_modes":
        l_modes,

        "scalar_l0_reproduction_pass":
        l0_reproduction_pass,

        "scalar_modes_all_positive":
        all_scalar_modes_positive,

        "source_r50_m":
        r50_m,

        "source_r90_m":
        r90_m,

        "gradient_scale_r90_gev":
        gradient_scale_r90_gev,

        "gradient_over_F":
        gradient_vs_F,

        "gradient_over_Mc":
        gradient_vs_Mc,

        "max_sigma_over_F":
        y_max,

        "max_phi_over_Mc":
        u_max,

        "cross_quartic_estimate":
        cross_quartic,

        "loop_ratio_cutoff_F":
        loop_ratio_F,

        "loop_ratio_cutoff_Mc":
        loop_ratio_Mc,

        "compactness":
        compactness,

        "small_field_expansion_safe":
        amplitude_expansion_safe,

        "gradient_eft_pass":
        gradient_eft_pass,

        "radiative_naturalness_closed":
        False,

        "current_physics_chain_pass":
        current_physics_pass,

        "classification":
        classification,

        "next":
        next_step,

        "claim_limits": [
            "The standard dQ/domega branch slope is a stability diagnostic, not by itself a complete multidimensional stability theorem.",
            "The scalar l=0..8 Hessian is evaluated at fixed X; fully coupled X-scalar angular modes remain open.",
            "Fragmentation/fission remains open.",
            "The exact logarithmic/exponential interactions are required because the operating field excursions are not assumed small.",
            "The simple one-loop estimates are naturalness diagnostics, not a UV completion.",
            "Activation/off-state and empirical closure remain open.",
            "Full physical metric and payload reaction remain open.",
            "The Q-ball has exponentially small rather than exactly compact source tails.",
        ],
    }

    OUT_JSON.write_text(
        json.dumps(
            to_builtin(
                result
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

    print(
        f"CONTINUATION_CSV="
        f"{OUT_CSV.resolve()}"
    )


if __name__ == "__main__":
    main()
