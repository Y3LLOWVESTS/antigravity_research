"""
031D3-A — independent U(1) metric-activation field capacity gate

Scientific motivation
---------------------
031D1 closed the gate-free same-Q off state.

The tested canonical D2 mediator-mass gate has now failed to produce a
certified stationary reciprocal realization under several independent
numerical formulations. It is strongly demoted under the project stop
rule, without claiming mathematical impossibility.

D3 changes mechanism rather than repairing D2.

Introduce an independent complex activation field Y with a positive
Hamiltonian and global U(1) charge. Ordinary neutral matter responds
through one physical metric

    g_tilde = A(phi,Y)^2 g

with

    log A = -1/2 f(a) u^2

    a = |Y|/V
    u = phi/M_c

and

    f(a) = 1 - exp(-a^2/2).

OFF:
    Y = 0
    f = 0
    A = 1.

Thus the scalar-metric coupling vanishes exactly in the ordinary vacuum.

ON:
    a >> 1
    f -> 1

and the existing scalarized source/metric coupling is recovered.

Activation field
----------------
Use the same positive-Hamiltonian logarithmic global-U(1) Q-ball class
already validated for the microscopic source:

    W_A(a) = 1/2 log(1+a^2)

    Y = V a(r) exp(-i omega_A t)/sqrt(2).

The activation Q-ball is independent; its physical scale is set by
m_A and V.

This run is a capacity/reaction/energy preflight only.

It does NOT yet solve the fully coupled X + phi + Y field equations.

Tests
-----
1. finite positive activation energy;
2. E_A/(Q_A m_A) < 1;
3. activation f >= declared value over productive source and payload;
4. tiny on-state leakage at 10 m;
5. source coupling remains near the certified f=1 source;
6. activation-source reaction can be made perturbatively small;
7. activation energy/control inventory remains useful;
8. basic self-coupling and metric-operator EFT scales exceed source
   gradients.

The complete Y stress-energy is represented by the canonical Q-ball
inventory. Formation/reset, charge transport, radiation and coupled
stability remain open.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np


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
    DATA / "031d3a_u1_metric_activation_summary.json"
)

OUT_CSV = (
    DATA / "031d3a_u1_metric_activation_scan.csv"
)


X_MATCH = 80.0

OMEGA_A_VALUES = (
    0.20,
    0.25,
    0.30,
    0.35,
    0.40,
    0.45,
    0.50,
    0.55,
    0.60,
    0.65,
)

MU_VALUES = np.geomspace(
    0.015,
    0.30,
    100,
)

F_ACT_MIN = 0.999

F_LEAK_10M_MAX = 1.0e-8

SOURCE_A_RELERR_MAX = 5.0e-3

SOURCE_REACTION_RATIO_MAX = 0.10

SOURCE_MASK_FRACTION = 1.0e-4

EFT_MARGIN_OVER_MX = 10.0

ENERGY_GREEN_FRACTION = 0.10
ENERGY_YELLOW_FRACTION = 1.00

SELF_COUPLING_MAX = 4.0 * math.pi

HBARC_EV_M = 1.973269804e-7
J_PER_EV = 1.602176634e-19


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


def builtin(value):
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


def activation_fraction_derivative(a):
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


def W(a):
    return (
        0.5
        * np.log1p(
            a**2
        )
    )


def count_nodes(solution) -> int:
    rho = np.linspace(
        1.0e-5,
        X_MATCH,
        8000,
    )

    a = np.asarray(
        solution.sol(rho)[0],
        dtype=float,
    )

    scale = max(
        float(
            np.max(
                np.abs(a)
            )
        ),
        1.0e-300,
    )

    significant = a[
        np.abs(a)
        > 1.0e-7 * scale
    ]

    if len(significant) < 2:
        return 0

    return int(
        np.sum(
            np.sign(
                significant[1:]
            )
            * np.sign(
                significant[:-1]
            )
            < 0.0
        )
    )


def extended_profile(
    solution,
    omega,
    rho,
):
    rho = np.asarray(
        rho,
        dtype=float,
    )

    a = np.empty_like(
        rho
    )

    ap = np.empty_like(
        rho
    )

    inside = (
        rho <= X_MATCH
    )

    if np.any(
        inside
    ):
        state = solution.sol(
            np.maximum(
                rho[
                    inside
                ],
                1.0e-5,
            )
        )

        a[
            inside
        ] = state[
            0
        ]

        ap[
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
        k = math.sqrt(
            max(
                1.0
                - omega**2,
                1.0e-12,
            )
        )

        boundary = solution.sol(
            X_MATCH
        )

        a80 = float(
            boundary[0]
        )

        ro = rho[
            outside
        ]

        ao = (
            a80
            * X_MATCH
            / ro
            * np.exp(
                -k
                * (
                    ro
                    - X_MATCH
                )
            )
        )

        apo = (
            -k
            -1.0 / ro
        ) * ao

        a[
            outside
        ] = ao

        ap[
            outside
        ] = apo

    return (
        a,
        ap,
    )


def activation_integrals(
    solution,
    omega,
):
    k = math.sqrt(
        max(
            1.0
            - omega**2,
            1.0e-12,
        )
    )

    rho_max = max(
        140.0,
        X_MATCH
        + 25.0 / k,
    )

    rho = np.linspace(
        1.0e-5,
        rho_max,
        60_000,
    )

    a, ap = extended_profile(
        solution,
        omega,
        rho,
    )

    density = (
        0.5
        * ap**2
        + 0.5
        * omega**2
        * a**2
        + W(a)
    )

    I_E = float(
        4.0
        * math.pi
        * np.trapezoid(
            rho**2
            * density,
            rho,
        )
    )

    I_Q = float(
        4.0
        * math.pi
        * omega
        * np.trapezoid(
            rho**2
            * a**2,
            rho,
        )
    )

    return {
        "I_E":
            I_E,

        "I_Q":
            I_Q,

        "E_over_Qm":
            I_E / I_Q,
    }


def main() -> None:
    print(
        "=== 031D3-A U1 METRIC-ACTIVATION CAPACITY GATE ==="
    )

    print(
        "D2_CANONICAL_MEDIATOR_MASS_GATE="
        "STRONGLY_DEMOTED_NOT_PROVEN_IMPOSSIBLE"
    )

    print(
        "D3_MECHANISM="
        "A_PHI_ACTIVATION_BY_INDEPENDENT_GLOBAL_U1_FIELD"
    )

    print(
        "PHYSICAL_METRIC="
        "LOG_A=-0.5*F_ACTIVATION*U^2"
    )

    print(
        "F_ACTIVATION=1-EXP(-A_FIELD^2/2)"
    )

    print(
        "OFF_STATE_Y_ZERO_IMPLIES_A_EQUAL_ONE=YES"
    )

    print(
        "OFF_STATE_BILINEAR_PHI_Y_MIXING=NO"
    )

    print(
        "FULL_X_PHI_Y_COUPLED_FIELD_SOLVE=NO"
    )

    print(
        "FORMATION_RESET_CHARGE_TRANSPORT_CLOSED=NO"
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

    omega_source = float(
        candidate[
            "omega"
        ]
    )

    epsilon = float(
        candidate[
            "epsilon"
        ]
    )

    chi_source = float(
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
        / chi_source
    )

    M_c_ev = (
        M_c_gev
        * 1.0e9
    )

    operating_energy_j = float(
        operating[
            "energy_J"
        ]
    )

    x_length_m = (
        HBARC_EV_M
        / m_x_ev
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

    payload_center_from_source_m = abs(
        payload_center_m
        - source_shift_m
    )

    payload_x = np.array(
        (
            (
                payload_center_from_source_m
                - payload_radius_m
            )
            / x_length_m,

            payload_center_from_source_m
            / x_length_m,

            (
                payload_center_from_source_m
                + payload_radius_m
            )
            / x_length_m,
        ),
        dtype=float,
    )

    x_leak_10m = (
        10.0
        / x_length_m
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

    print(
        f"M_X_EV={m_x_ev:.15e}"
    )

    print(
        f"F_SOURCE_GEV={F_gev:.15e}"
    )

    print(
        f"M_C_GEV={M_c_gev:.15e}"
    )

    print(
        f"PAYLOAD_X_NEAR={payload_x[0]:.12f}"
    )

    print(
        f"PAYLOAD_X_CENTER={payload_x[1]:.12f}"
    )

    print(
        f"PAYLOAD_X_FAR={payload_x[2]:.12f}"
    )

    print(
        f"LEAKAGE_TEST_X_10M={x_leak_10m:.12f}"
    )

    print(
        f"OFF_SOURCE_QBALL_PASS={off_source_pass}"
    )

    print(
        f"OFF_SCALAR_QUADRATIC_MASS2_HAT="
        f"{epsilon**2:.15e}"
    )

    print(
        "OFF_SCALAR_QUADRATIC_STABLE=True"
    )

    qmod = load_module(
        "qball031d3a",
        QBALL_SOURCE,
    )

    old_xmatch = float(
        qmod.X_MATCH
    )

    qmod.X_MATCH = X_MATCH

    try:
        print(
            "\n=== STAGE A: RECONSTRUCT CERTIFIED ON SOURCE ==="
        )

        source_seed = qmod.solve_uncoupled_qball(
            omega_source
        )

        if source_seed is None:
            raise RuntimeError(
                "Failed source Q-ball seed"
            )

        source = qmod.solve_coupled(
            source_seed,
            omega_source,
            epsilon,
            chi_source,
            previous=None,
        )

        if source is None:
            raise RuntimeError(
                "Failed certified source reconstruction"
            )

        x_source = np.linspace(
            1.0e-5,
            X_MATCH,
            5000,
        )

        source_state = source.sol(
            x_source
        )

        y_source = np.asarray(
            source_state[
                0
            ],
            dtype=float,
        )

        u_source = np.asarray(
            source_state[
                2
            ],
            dtype=float,
        )

        W_source = W(
            y_source
        )

        source_mask = (
            W_source
            >= SOURCE_MASK_FRACTION
            * np.max(
                W_source
            )
        )

        A_baseline = np.exp(
            -0.5
            * u_source**2
        )

        print(
            f"SOURCE_PRODUCTIVE_MASK_POINTS="
            f"{int(np.sum(source_mask))}"
        )

        print(
            f"SOURCE_U0="
            f"{float(u_source[0]):.15e}"
        )

        print(
            "\n=== STAGE B: ACTIVATION-QBALL PROFILE LIBRARY ==="
        )

        profile_library = []

        for omega_a in OMEGA_A_VALUES:
            try:
                activation_solution = (
                    qmod.solve_uncoupled_qball(
                        omega_a
                    )
                )
            except Exception as exc:
                print(
                    f"ACTIVATION_PROFILE "
                    f"OMEGA={omega_a:.6f} "
                    f"SUCCESS=False "
                    f"ERROR={exc}"
                )

                continue

            if activation_solution is None:
                print(
                    f"ACTIVATION_PROFILE "
                    f"OMEGA={omega_a:.6f} "
                    "SUCCESS=False"
                )

                continue

            nodes = count_nodes(
                activation_solution
            )

            if nodes != 0:
                print(
                    f"ACTIVATION_PROFILE "
                    f"OMEGA={omega_a:.6f} "
                    f"SUCCESS=False "
                    f"NODES={nodes}"
                )

                continue

            integrals = activation_integrals(
                activation_solution,
                omega_a,
            )

            a0 = float(
                activation_solution.sol(
                    1.0e-5
                )[0]
            )

            profile_library.append(
                (
                    omega_a,
                    activation_solution,
                    integrals,
                )
            )

            print(
                f"ACTIVATION_PROFILE "
                f"OMEGA={omega_a:.6f} "
                f"A0={a0:.9e} "
                f"I_E={integrals['I_E']:.9e} "
                f"I_Q={integrals['I_Q']:.9e} "
                f"E_OVER_QM="
                f"{integrals['E_over_Qm']:.9e}"
            )

        if not profile_library:
            raise RuntimeError(
                "No nodeless activation Q-ball profiles"
            )

        print(
            "\n=== STAGE C: GEOMETRY / REACTION / ENERGY SCAN ==="
        )

        rows = []

        for (
            omega_a,
            activation_solution,
            integrals,
        ) in profile_library:

            bound_pass = bool(
                integrals[
                    "E_over_Qm"
                ] < 1.0
            )

            for mu in MU_VALUES:
                m_a_ev = (
                    mu
                    * m_x_ev
                )

                rho_source = (
                    mu
                    * x_source
                )

                a_source, _ = extended_profile(
                    activation_solution,
                    omega_a,
                    rho_source,
                )

                f_source = activation_fraction(
                    a_source
                )

                fp_source = (
                    activation_fraction_derivative(
                        a_source
                    )
                )

                f_source_min = float(
                    np.min(
                        f_source[
                            source_mask
                        ]
                    )
                )

                A_activated = np.exp(
                    -0.5
                    * f_source
                    * u_source**2
                )

                source_A_relerr = float(
                    np.max(
                        np.abs(
                            A_activated[
                                source_mask
                            ]
                            /
                            A_baseline[
                                source_mask
                            ]
                            - 1.0
                        )
                    )
                )

                a_payload, _ = extended_profile(
                    activation_solution,
                    omega_a,
                    mu
                    * payload_x,
                )

                f_payload = activation_fraction(
                    a_payload
                )

                payload_f_min = float(
                    np.min(
                        f_payload
                    )
                )

                a_leak, _ = extended_profile(
                    activation_solution,
                    omega_a,
                    np.array(
                        [
                            mu
                            * x_leak_10m
                        ]
                    ),
                )

                f_leak_10m = float(
                    activation_fraction(
                        a_leak
                    )[0]
                )

                geometry_pass = bool(
                    f_source_min
                    >= F_ACT_MIN
                    and
                    payload_f_min
                    >= F_ACT_MIN
                    and
                    f_leak_10m
                    <= F_LEAK_10M_MAX
                    and
                    source_A_relerr
                    <= SOURCE_A_RELERR_MAX
                )

                if not geometry_pass:
                    continue

                # --------------------------------------------------
                # Source reaction estimate.
                #
                # Full activation EOM in x has schematic source term
                #
                #   -(F/V)^2 * 1/2 u^2 A W f'(a).
                #
                # Compare it with the absolute intrinsic Q-ball
                # force scale
                #
                #   mu^2 [ |a/(1+a^2)| + Omega_A^2 |a| ].
                #
                # This avoids relying on cancellations in the
                # stationary activation equation.
                # --------------------------------------------------

                source_force_shape = (
                    0.5
                    * u_source**2
                    * A_activated
                    * W_source
                    * np.abs(
                        fp_source
                    )
                )

                intrinsic_scale = (
                    mu**2
                    * (
                        np.abs(
                            a_source
                            /
                            (
                                1.0
                                + a_source**2
                            )
                        )
                        + omega_a**2
                        * np.abs(
                            a_source
                        )
                        + 1.0e-14
                    )
                )

                reaction_shape = float(
                    np.max(
                        (
                            source_force_shape[
                                source_mask
                            ]
                            /
                            intrinsic_scale[
                                source_mask
                            ]
                        )
                    )
                )

                V_reaction_ev = (
                    F_ev
                    * math.sqrt(
                        max(
                            reaction_shape,
                            0.0,
                        )
                        /
                        SOURCE_REACTION_RATIO_MAX
                    )
                )

                # Metric-operator scale:
                #
                # T phi^2 |Y|^2 /(V^2 M_c^2)
                #
                # corresponds schematically to
                #
                # Lambda_A ~ sqrt(V M_c).
                #
                # Require Lambda_A > margin * m_X.
                V_eft_ev = (
                    (
                        EFT_MARGIN_OVER_MX
                        * m_x_ev
                    )**2
                    /
                    M_c_ev
                )

                # Small-field logarithmic potential quartic is order
                # m_A^2/V^2. Keep it perturbative.
                V_self_ev = (
                    m_a_ev
                    / math.sqrt(
                        SELF_COUPLING_MAX
                    )
                )

                V_required_ev = max(
                    V_reaction_ev,
                    V_eft_ev,
                    V_self_ev,
                )

                reaction_ratio = (
                    (
                        F_ev
                        / V_required_ev
                    )**2
                    * reaction_shape
                )

                metric_operator_scale_ev = math.sqrt(
                    V_required_ev
                    * M_c_ev
                )

                self_coupling_est = (
                    m_a_ev**2
                    / V_required_ev**2
                )

                activation_energy_ev = (
                    integrals[
                        "I_E"
                    ]
                    * V_required_ev**2
                    / m_a_ev
                )

                activation_energy_j = (
                    activation_energy_ev
                    * J_PER_EV
                )

                activation_energy_fraction = (
                    activation_energy_j
                    / operating_energy_j
                )

                activation_charge = (
                    integrals[
                        "I_Q"
                    ]
                    * V_required_ev**2
                    / m_a_ev**2
                )

                reaction_pass = bool(
                    reaction_ratio
                    <= SOURCE_REACTION_RATIO_MAX
                    * (
                        1.0
                        + 1.0e-10
                    )
                )

                eft_pass = bool(
                    metric_operator_scale_ev
                    >=
                    EFT_MARGIN_OVER_MX
                    * m_x_ev
                    and
                    self_coupling_est
                    <= SELF_COUPLING_MAX
                )

                candidate_pass = bool(
                    geometry_pass
                    and
                    bound_pass
                    and
                    reaction_pass
                    and
                    eft_pass
                )

                rows.append(
                    {
                        "omega_activation":
                            omega_a,

                        "mu_mA_over_mX":
                            float(mu),

                        "m_A_eV":
                            m_a_ev,

                        "I_E_activation":
                            integrals[
                                "I_E"
                            ],

                        "I_Q_activation":
                            integrals[
                                "I_Q"
                            ],

                        "E_over_Qm":
                            integrals[
                                "E_over_Qm"
                            ],

                        "source_f_min":
                            f_source_min,

                        "payload_f_min":
                            payload_f_min,

                        "f_leak_10m":
                            f_leak_10m,

                        "source_A_relerr":
                            source_A_relerr,

                        "reaction_shape":
                            reaction_shape,

                        "V_reaction_eV":
                            V_reaction_ev,

                        "V_eft_eV":
                            V_eft_ev,

                        "V_self_eV":
                            V_self_ev,

                        "V_required_eV":
                            V_required_ev,

                        "reaction_ratio":
                            reaction_ratio,

                        "metric_operator_scale_eV":
                            metric_operator_scale_ev,

                        "self_coupling_est":
                            self_coupling_est,

                        "activation_energy_J":
                            activation_energy_j,

                        "activation_energy_GJ":
                            activation_energy_j
                            / 1.0e9,

                        "activation_energy_fraction":
                            activation_energy_fraction,

                        "activation_charge":
                            activation_charge,

                        "geometry_pass":
                            geometry_pass,

                        "bound_pass":
                            bound_pass,

                        "reaction_pass":
                            reaction_pass,

                        "eft_pass":
                            eft_pass,

                        "candidate_pass":
                            candidate_pass,
                    }
                )

        passing = [
            row
            for row in rows
            if bool(
                row[
                    "candidate_pass"
                ]
            )
        ]

        print(
            f"CAPACITY_CASES={len(rows)}"
        )

        print(
            f"PASSING_CASES={len(passing)}"
        )

        if passing:
            best = min(
                passing,
                key=lambda row:
                    float(
                        row[
                            "activation_energy_J"
                        ]
                    ),
            )

            print(
                "\n=== STAGE D: BEST D3 CAPACITY SURVIVOR ==="
            )

            for key in (
                "omega_activation",
                "mu_mA_over_mX",
                "m_A_eV",
                "E_over_Qm",
                "source_f_min",
                "payload_f_min",
                "f_leak_10m",
                "source_A_relerr",
                "V_required_eV",
                "reaction_ratio",
                "metric_operator_scale_eV",
                "self_coupling_est",
                "activation_energy_GJ",
                "activation_energy_fraction",
                "activation_charge",
            ):
                print(
                    f"BEST_{key.upper()}="
                    f"{best[key]:.15e}"
                )

            optimistic_total_j = (
                operating_energy_j
                + best[
                    "activation_energy_J"
                ]
            )

            print(
                f"OPTIMISTIC_TOTAL_ON_INVENTORY_GJ="
                f"{optimistic_total_j / 1.0e9:.12f}"
            )

            if (
                best[
                    "activation_energy_fraction"
                ]
                <= ENERGY_GREEN_FRACTION
            ):
                classification = (
                    "GREEN_D3A_U1_METRIC_ACTIVATION_HAS_"
                    "LOW_ENERGY_GEOMETRIC_REACTION_CAPACITY"
                )

                next_action = (
                    "031D3B_FULL_FIXED_QX_QY_COUPLED_"
                    "X_PHI_Y_METRIC_ACTIVATION_SOLVE"
                )

            elif (
                best[
                    "activation_energy_fraction"
                ]
                <= ENERGY_YELLOW_FRACTION
            ):
                classification = (
                    "YELLOW_D3A_U1_METRIC_ACTIVATION_"
                    "CAPACITY_SURVIVES_BUT_ENERGY_NOT_SMALL"
                )

                next_action = (
                    "031D3B_COUPLED_EXISTENCE_BEFORE_OPTIMIZATION"
                )

            else:
                classification = (
                    "RED_D3A_U1_METRIC_ACTIVATION_"
                    "CAPACITY_COST_EXCEEDS_SOURCE_INVENTORY"
                )

                next_action = (
                    "RERANK_031D_AFTER_D1_D2_D3_NEGATIVE_LEDGER"
                )

        else:
            best = None

            classification = (
                "RED_D3A_NO_TESTED_U1_ACTIVATION_PROFILE_"
                "MEETS_GEOMETRY_REACTION_EFT_GATES"
            )

            next_action = (
                "RERANK_031D_AUXILIARY_ACTIVATION_CLASS"
            )

        print(
            "\n=== STAGE E: DECISION ==="
        )

        print(
            f"031D3A_CLASSIFICATION="
            f"{classification}"
        )

        print(
            f"NEXT={next_action}"
        )

        print(
            "OFF_STATE_LINEAR_SCALAR_STABLE=True"
        )

        print(
            "OFF_STATE_ACTIVATION_VACUUM_STABLE=True"
        )

        print(
            "FULL_X_PHI_Y_FIELD_EQUATIONS_SOLVED=NO"
        )

        print(
            "ACTIVATION_QBALL_COUPLED_STABILITY_CLOSED=NO"
        )

        print(
            "FORMATION_ENERGY_LOWER_BOUND_INCLUDED="
            f"{best is not None}"
        )

        print(
            "CHARGE_INJECTION_RESET_CLOSED=NO"
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
            "EMPIRICAL_FIFTH_FORCE_EPPPN_CLOSED=NO"
        )

        print(
            "PRACTICAL_DEVICE=NO"
        )

        summary = {
            "classification":
                classification,

            "next":
                next_action,

            "mechanism": {
                "activation_field":
                    "independent complex global-U1 Q-ball",

                "metric":
                    (
                        "log A = -0.5 * "
                        "(1-exp(-a^2/2)) * u^2"
                    ),

                "off_state":
                    "Y=0 => f=0 => A=1",

                "quadratic_phi_Y_mixing_off":
                    False,
            },

            "off_state": {
                "source_qball_pass":
                    off_source_pass,

                "scalar_mass2_hat":
                    epsilon**2,

                "scalar_quadratic_stable":
                    True,

                "activation_vacuum_stable":
                    True,
            },

            "scan_count":
                len(rows),

            "passing_count":
                len(passing),

            "best":
                best,

            "claim_limits": [
                (
                    "This is a fixed-field capacity and reaction "
                    "preflight, not a coupled X/phi/Y solution."
                ),
                (
                    "The activation field has positive canonical "
                    "Q-ball energy and conserved U(1) charge."
                ),
                (
                    "Switching requires injection/removal of activation "
                    "charge or an explicit reservoir."
                ),
                (
                    "The reaction bound is deliberately perturbative; "
                    "a full coupled field may shift the optimum."
                ),
                (
                    "The metric-operator scale is only a dimensional "
                    "EFT diagnostic, not radiative closure."
                ),
                (
                    "Formation/reset, radiation, full metric "
                    "backreaction and empirical constraints remain open."
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

        if rows:
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

        else:
            OUT_CSV.write_text(
                "candidate_pass\n"
            )

        print(
            f"SUMMARY_JSON={OUT_JSON}"
        )

        print(
            f"SCAN_CSV={OUT_CSV}"
        )

    finally:
        qmod.X_MATCH = old_xmatch


if __name__ == "__main__":
    main()
