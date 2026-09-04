"""
031D2-A — canonical auxiliary-field activation capacity preflight

Previous result
---------------
031D1HR closed the nodeless, same-Noether-charge, gate-free u=0
Q-ball off-state family:

    LOW branch:
        source viable
        scalar tachyonic

    HIGH branch:
        Q-ball source unstable
        energetically unbound

Therefore an auxiliary dynamical activation sector is mandatory.

This run asks the cheapest next question:

    Can a canonical positive-energy auxiliary scalar dynamically supply
    the required off-state phi mass shift without an obvious energy,
    wall-thickness, reciprocity, or elementary naturalness catastrophe?

Gate model
----------
Introduce a real scalar s with

    V_s(s)
        = lambda_s/4 * (s^2 - v_s^2)^2

and reciprocal interaction

    V_int
        = 1/2 * g_s^2 * s^2 * phi^2.

OFF:
    phi ~ 0
    s = v_s

so

    m_phi,off^2
        = m_phi^2 + g_s^2 v_s^2.

ON:
    the device scalar background phi makes

    m_s,eff^2
        = -lambda_s v_s^2 + g_s^2 phi^2.

If positive throughout the required on-state region,
s=0 is locally restored and the added phi mass disappears.

This is a CAPACITY PREFLIGHT ONLY.

It does not yet solve the coupled y/u/s field equations.
It does not certify switching, nucleation, reset, radiation,
full stress-energy, full metric backreaction or empirical closure.
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

LOW_SUMMARY = (
    DATA
    / "031d1r2_lowbranch_offstate_hessian_summary.json"
)

D1HR_SUMMARY = (
    DATA
    / "031d1hr_highbranch_certificate_summary.json"
)

OUT_JSON = (
    DATA
    / "031d2a_auxiliary_gate_capacity_summary.json"
)

OUT_CSV = (
    DATA
    / "031d2a_auxiliary_gate_capacity_scan.csv"
)


HBARC_EV_M = 1.973269804e-7
J_PER_EV = 1.602176634e-19

STABILIZATION_MARGIN = 1.20

ON_CURVATURE_RATIO_REQUIRED = 1.20

G_MAX = math.sqrt(
    4.0 * math.pi
)

LAMBDA_MAX = 4.0 * math.pi

G_VALUES = np.geomspace(
    1.0e-6,
    G_MAX,
    180,
)

WALL_WIDTH_CAPS_M = (
    0.10,
    0.25,
    0.50,
)

GATE_EXTRA_MARGINS_M = (
    0.10,
    0.50,
    1.00,
    1.50,
)

ENERGY_FRACTION_CAP = 0.10

NAIVE_NATURALNESS_LOOP_FACTOR = (
    4.0 * math.pi
)


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
            str(key): builtin(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [
            builtin(item)
            for item in value
        ]

    return value


def evaluate_u_extended(
    solution,
    x: float,
    epsilon: float,
    x_match: float,
) -> float:
    if x <= x_match:
        return float(
            solution.sol(
                max(x, 1.0e-5)
            )[2]
        )

    u_boundary = float(
        solution.sol(
            x_match
        )[2]
    )

    return (
        u_boundary
        * x_match
        / x
        * math.exp(
            -epsilon
            * (
                x - x_match
            )
        )
    )


def gate_energy_floor(
    radius_m: float,
    wall_width_m: float,
    v_ev: float,
    lambda_s: float,
):
    """
    Positive-energy lower ledger.

    Volume term:
        bare V_s(0) = lambda v^4 / 4

    Gradient term:
        Cauchy lower bound for changing s by v over width w,

        integral 1/2 (ds/dx)^2 dx >= v^2/(2w).

    No negative interaction energy is credited.
    Wall-potential energy is omitted, so this remains optimistic.
    """

    volume_m3 = (
        4.0
        / 3.0
        * math.pi
        * radius_m**3
    )

    area_m2 = (
        4.0
        * math.pi
        * radius_m**2
    )

    volume_nat = (
        volume_m3
        / HBARC_EV_M**3
    )

    area_nat = (
        area_m2
        / HBARC_EV_M**2
    )

    width_nat = (
        wall_width_m
        / HBARC_EV_M
    )

    bare_density_ev4 = (
        lambda_s
        * v_ev**4
        / 4.0
    )

    volume_energy_ev = (
        bare_density_ev4
        * volume_nat
    )

    gradient_floor_ev = (
        area_nat
        * v_ev**2
        / (
            2.0
            * width_nat
        )
    )

    return {
        "volume_J":
            volume_energy_ev
            * J_PER_EV,

        "gradient_floor_J":
            gradient_floor_ev
            * J_PER_EV,

        "total_floor_J":
            (
                volume_energy_ev
                + gradient_floor_ev
            )
            * J_PER_EV,
    }


def main() -> None:
    print(
        "=== 031D2-A AUXILIARY GATE CAPACITY PREFLIGHT ==="
    )

    print(
        "CLAIM_CLASS="
        "DYNAMICAL_MEDIATOR_MASS_GATE_CAPACITY_ONLY"
    )

    print(
        "SPATIALLY_PRESCRIBED_MPHI=NO"
    )

    print(
        "RECIPROCAL_PHI_GATE_COUPLING=YES"
    )

    print(
        "FULL_COUPLED_GATE_FIELD_EQUATIONS_SOLVED=NO"
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
            "031C96 robust operating family is not GREEN"
        )

    if not bool(
        low.get(
            "low_branch_robust_tachyon",
            False,
        )
    ):
        raise RuntimeError(
            "031D1-R2 low-branch tachyon not established"
        )

    if not bool(
        d1hr.get(
            "gate_free_same_Q_offstate_route_closed",
            False,
        )
    ):
        raise RuntimeError(
            "031D1HR gate-free closure not established"
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

    omega = float(
        candidate["omega"]
    )

    epsilon = float(
        candidate["epsilon"]
    )

    chi_source = float(
        candidate["chi"]
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

    m_phi_ev = (
        epsilon
        * m_x_ev
    )

    F_gev = float(
        quadrature[
            "F_gev"
        ]
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

    payload_far_surface_from_source_m = (
        payload_center_from_source_m
        + payload_radius_m
    )

    critical_hat = float(
        low[
            "critical_positive_delta_m2_hat"
        ]
    )

    required_hat = (
        STABILIZATION_MARGIN
        * critical_hat
    )

    required_delta_m2_ev2 = (
        required_hat
        * m_x_ev**2
    )

    required_delta_m_ev = math.sqrt(
        required_delta_m2_ev2
    )

    off_total_mass_ev = math.sqrt(
        m_phi_ev**2
        + required_delta_m2_ev2
    )

    off_range_m = (
        HBARC_EV_M
        / off_total_mass_ev
    )

    print(
        f"M_X_EV={m_x_ev:.15e}"
    )

    print(
        f"M_PHI_ON_EV={m_phi_ev:.15e}"
    )

    print(
        f"M_C_GEV={M_c_gev:.15e}"
    )

    print(
        f"CRITICAL_DELTA_M2_HAT="
        f"{critical_hat:.15e}"
    )

    print(
        f"STABILIZATION_MARGIN="
        f"{STABILIZATION_MARGIN:.9f}"
    )

    print(
        f"REQUIRED_DELTA_M2_HAT="
        f"{required_hat:.15e}"
    )

    print(
        f"REQUIRED_DELTA_M_EV="
        f"{required_delta_m_ev:.15e}"
    )

    print(
        f"M_PHI_OFF_EV="
        f"{off_total_mass_ev:.15e}"
    )

    print(
        f"OFF_MEDIATOR_RANGE_M="
        f"{off_range_m:.15e}"
    )

    print(
        f"OFF_YUKAWA_SUPPRESSION_AT_1M="
        f"{math.exp(-1.0 / off_range_m):.15e}"
    )

    print(
        f"OPERATING_ENERGY_GJ="
        f"{operating_energy_j / 1.0e9:.12f}"
    )

    print(
        f"PAYLOAD_CENTER_FROM_SOURCE_M="
        f"{payload_center_from_source_m:.12f}"
    )

    print(
        f"PAYLOAD_FAR_SURFACE_FROM_SOURCE_M="
        f"{payload_far_surface_from_source_m:.12f}"
    )

    qmod = load_module(
        "qball031d2a",
        QBALL_SOURCE,
    )

    original_x_match = float(
        qmod.X_MATCH
    )

    x_match = 80.0
    qmod.X_MATCH = x_match

    try:
        print(
            "\n=== STAGE A: RECONSTRUCT ON-STATE SCALAR PROFILE ==="
        )

        seed = qmod.solve_uncoupled_qball(
            omega
        )

        if seed is None:
            raise RuntimeError(
                "Failed to reconstruct Q-ball seed"
            )

        solution = qmod.solve_coupled(
            seed,
            omega,
            epsilon,
            chi_source,
            previous=None,
        )

        if solution is None:
            raise RuntimeError(
                "Failed to reconstruct coupled on state"
            )

        x_compton_m = (
            HBARC_EV_M
            / m_x_ev
        )

        gate_radii = [
            payload_far_surface_from_source_m
            + margin
            for margin
            in GATE_EXTRA_MARGINS_M
        ]

        phi_boundary = {}

        for radius_m in gate_radii:
            x = (
                radius_m
                / x_compton_m
            )

            u = evaluate_u_extended(
                solution,
                x,
                epsilon,
                x_match,
            )

            phi_ev = abs(
                M_c_ev
                * u
            )

            phi_boundary[
                radius_m
            ] = phi_ev

            print(
                f"ON_PROFILE "
                f"R_GATE_M={radius_m:.9f} "
                f"X={x:.9f} "
                f"U={u:.15e} "
                f"ABS_PHI_EV={phi_ev:.15e}"
            )

        print(
            "\n=== STAGE B: CANONICAL GATE PARAMETER SCAN ==="
        )

        rows = []

        for radius_m in gate_radii:
            phi_min_ev = float(
                phi_boundary[
                    radius_m
                ]
            )

            for wall_cap_m in (
                WALL_WIDTH_CAPS_M
            ):
                for g_s in G_VALUES:
                    v_ev = (
                        required_delta_m_ev
                        / g_s
                    )

                    lambda_width_min = (
                        HBARC_EV_M
                        / (
                            math.sqrt(2.0)
                            * v_ev
                            * wall_cap_m
                        )
                    )**2

                    lambda_on_max = (
                        g_s**2
                        * phi_min_ev**2
                        /
                        (
                            ON_CURVATURE_RATIO_REQUIRED
                            * v_ev**2
                        )
                    )

                    # Add 5% width margin beyond the exact cap.
                    lambda_s = (
                        1.05
                        * lambda_width_min
                    )

                    self_coupling_pass = bool(
                        lambda_s
                        <= LAMBDA_MAX
                    )

                    on_restore_pass = bool(
                        lambda_s
                        <= lambda_on_max
                    )

                    perturbative_g_pass = bool(
                        g_s
                        <= G_MAX
                    )

                    if not (
                        self_coupling_pass
                        and
                        on_restore_pass
                        and
                        perturbative_g_pass
                    ):
                        continue

                    m_s_out_ev = (
                        math.sqrt(
                            2.0
                            * lambda_s
                        )
                        * v_ev
                    )

                    wall_width_actual_m = (
                        HBARC_EV_M
                        / m_s_out_ev
                    )

                    on_curvature_ratio = (
                        g_s**2
                        * phi_min_ev**2
                        /
                        (
                            lambda_s
                            * v_ev**2
                        )
                    )

                    naive_naturalness_cutoff_ev = (
                        NAIVE_NATURALNESS_LOOP_FACTOR
                        * m_s_out_ev
                        / g_s
                    )

                    source_scale_naturalness_pass = bool(
                        naive_naturalness_cutoff_ev
                        >= m_x_ev
                    )

                    energy = gate_energy_floor(
                        radius_m,
                        wall_width_actual_m,
                        v_ev,
                        lambda_s,
                    )

                    energy_fraction = (
                        energy[
                            "total_floor_J"
                        ]
                        / operating_energy_j
                    )

                    energy_pass = bool(
                        energy_fraction
                        <= ENERGY_FRACTION_CAP
                    )

                    candidate_pass = bool(
                        wall_width_actual_m
                        <= wall_cap_m
                        and
                        on_curvature_ratio
                        >= ON_CURVATURE_RATIO_REQUIRED
                        and
                        source_scale_naturalness_pass
                        and
                        energy_pass
                    )

                    rows.append(
                        {
                            "gate_radius_m":
                                radius_m,

                            "wall_cap_m":
                                wall_cap_m,

                            "g_s":
                                float(g_s),

                            "v_s_eV":
                                v_ev,

                            "lambda_s":
                                lambda_s,

                            "lambda_width_min":
                                lambda_width_min,

                            "lambda_on_max":
                                lambda_on_max,

                            "m_s_out_eV":
                                m_s_out_ev,

                            "wall_width_actual_m":
                                wall_width_actual_m,

                            "phi_boundary_eV":
                                phi_min_ev,

                            "on_curvature_ratio":
                                on_curvature_ratio,

                            "required_delta_m2_hat":
                                required_hat,

                            "off_phi_mass_eV":
                                off_total_mass_ev,

                            "off_phi_range_m":
                                off_range_m,

                            "naive_naturalness_cutoff_eV":
                                naive_naturalness_cutoff_ev,

                            "naturalness_cutoff_over_mX":
                                naive_naturalness_cutoff_ev
                                / m_x_ev,

                            "source_scale_naturalness_pass":
                                source_scale_naturalness_pass,

                            "gate_volume_energy_J":
                                energy[
                                    "volume_J"
                                ],

                            "gate_gradient_floor_J":
                                energy[
                                    "gradient_floor_J"
                                ],

                            "gate_total_positive_floor_J":
                                energy[
                                    "total_floor_J"
                                ],

                            "gate_energy_fraction":
                                energy_fraction,

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
            f"TOTAL_GATE_CASES={len(rows)}"
        )

        print(
            f"PASSING_GATE_CASES={len(passing)}"
        )

        if passing:
            best = min(
                passing,
                key=lambda row:
                    float(
                        row[
                            "gate_total_positive_floor_J"
                        ]
                    ),
            )

            print(
                "\n=== STAGE C: BEST CAPACITY SURVIVOR ==="
            )

            for key in (
                "gate_radius_m",
                "wall_cap_m",
                "g_s",
                "v_s_eV",
                "lambda_s",
                "m_s_out_eV",
                "wall_width_actual_m",
                "phi_boundary_eV",
                "on_curvature_ratio",
                "naive_naturalness_cutoff_eV",
                "naturalness_cutoff_over_mX",
                "gate_volume_energy_J",
                "gate_gradient_floor_J",
                "gate_total_positive_floor_J",
                "gate_energy_fraction",
            ):
                print(
                    f"BEST_{key.upper()}="
                    f"{best[key]:.15e}"
                )

            optimistic_total_j = (
                operating_energy_j
                + float(
                    best[
                        "gate_total_positive_floor_J"
                    ]
                )
            )

            print(
                f"OPTIMISTIC_TOTAL_WITH_GATE_FLOOR_GJ="
                f"{optimistic_total_j / 1.0e9:.12f}"
            )

        else:
            best = None

        print(
            "\n=== STAGE D: DECISION ==="
        )

        if passing:
            classification = (
                "GREEN_D2A_CANONICAL_RECIPROCAL_"
                "AUXILIARY_MASS_GATE_HAS_CAPACITY_"
                "NO_OBVIOUS_ENERGY_OR_WIDTH_OBSTRUCTION"
            )

            next_action = (
                "031D2B_SOLVE_FULL_COUPLED_Y_U_S_"
                "ON_OFF_BVP_WALL_ENERGY_SWITCHING_AND_RECIPROCITY"
            )

        elif rows:
            classification = (
                "YELLOW_D2A_CANONICAL_GATE_CAPACITY_"
                "FAILS_DECLARED_COMBINED_PREFLIGHT"
            )

            next_action = (
                "INSPECT_D2A_FAILING_GATE_BEFORE_"
                "CHOOSING_D3_ALTERNATE_ACTIVATION_FIELD"
            )

        else:
            classification = (
                "RED_D2A_CANONICAL_GATE_HAS_NO_"
                "PERTURBATIVE_PARAMETER_WINDOW"
            )

            next_action = (
                "031D3_ALTERNATE_AUXILIARY_ACTIVATION_FIELD"
            )

        print(
            f"031D2A_CLASSIFICATION="
            f"{classification}"
        )

        print(
            f"NEXT={next_action}"
        )

        print(
            "RECIPROCITY_AT_LAGRANGIAN_LEVEL="
            "BUILT_IN"
        )

        print(
            "RECIPROCITY_FULL_FIELD_CLOSED=NO"
        )

        print(
            "FULL_GATE_FIELD_EQUATIONS_CLOSED=NO"
        )

        print(
            "SWITCHING_BARRIER_CLOSED=NO"
        )

        print(
            "FORMATION_RESET_ENERGY_CLOSED=NO"
        )

        print(
            "FULL_METRIC_BACKREACTION_CLOSED=NO"
        )

        print(
            "RADIATIVE_NATURALNESS_CLOSED=NO"
        )

        print(
            "PRACTICAL_DEVICE=NO"
        )

        summary = {
            "classification":
                classification,

            "next":
                next_action,

            "model": {
                "gate_potential":
                    "lambda_s/4*(s^2-v_s^2)^2",

                "interaction":
                    "1/2*g_s^2*s^2*phi^2",

                "reciprocal":
                    True,
            },

            "required_off_stabilization": {
                "critical_delta_m2_hat":
                    critical_hat,

                "margin":
                    STABILIZATION_MARGIN,

                "required_delta_m2_hat":
                    required_hat,

                "required_delta_m_eV":
                    required_delta_m_ev,

                "m_phi_on_eV":
                    m_phi_ev,

                "m_phi_off_eV":
                    off_total_mass_ev,

                "off_range_m":
                    off_range_m,
            },

            "geometry": {
                "payload_center_from_source_m":
                    payload_center_from_source_m,

                "payload_far_surface_from_source_m":
                    payload_far_surface_from_source_m,

                "gate_radii_m":
                    gate_radii,
            },

            "on_profile_phi_boundary_eV":
                {
                    str(key):
                        value
                    for key, value
                    in phi_boundary.items()
                },

            "scan_count":
                len(rows),

            "passing_count":
                len(passing),

            "best":
                best,

            "claim_limits": [
                (
                    "This is only a canonical auxiliary-gate "
                    "capacity preflight."
                ),
                (
                    "No spatially varying mass is prescribed as "
                    "final physics; the proposed mass shift comes "
                    "from the dynamical field s."
                ),
                (
                    "The gate positive-energy ledger is an "
                    "optimistic lower bound, not a solved wall."
                ),
                (
                    "No negative interaction energy is credited."
                ),
                (
                    "The naturalness cutoff is only a naive "
                    "one-loop diagnostic."
                ),
                (
                    "The coupled y/u/s equations, wall profile, "
                    "switching barrier, formation/reset energy and "
                    "radiation remain unsolved."
                ),
                (
                    "Full physical-metric backreaction and "
                    "empirical closure remain open."
                ),
                (
                    "No practical device is established."
                ),
            ],
        }

        OUT_JSON.write_text(
            json.dumps(
                builtin(summary),
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
                    for key in row.keys()
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
        qmod.X_MATCH = original_x_match


if __name__ == "__main__":
    main()
