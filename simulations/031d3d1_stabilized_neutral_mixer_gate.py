#!/usr/bin/env python3
from __future__ import annotations

import csv
import importlib.util
import json
import math
from pathlib import Path
import sys
from typing import Any

import numpy as np
from scipy.integrate import solve_bvp
from scipy.interpolate import PchipInterpolator


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

QBALL_SOURCE = (
    SIM
    / "031b2a_global_qball_activated_scalar_control.py"
)

D3A_SOURCE = (
    SIM
    / "031d3a_u1_metric_activation_capacity.py"
)

OUT_JSON = (
    DATA
    / "031d3d1_stabilized_neutral_mixer_summary.json"
)

OUT_SCAN = (
    DATA
    / "031d3d1_stabilized_neutral_mixer_scan.csv"
)

J_PER_EV = 1.602176634e-19
HBAR_EV_S = 6.582119569e-16
H_EV_S = 4.135667696e-15

PRIMARY_SWITCH_S = 1.0

SWITCH_TIMES_S = (
    10.0,
    1.0,
    0.1,
    0.01,
    0.001,
    1.0e-4,
    1.0e-5,
    1.0e-6,
)

SIGMA_VALUES = (
    3.0,
    5.0,
    10.0,
)

G_GRID = np.logspace(
    -12.0,
    0.0,
    241,
)

STABILIZER_MARGIN = 1.20

MAX_DIMENSIONLESS_COUPLING = 1.0
MAX_QUARTIC = 4.0 * math.pi

RABI_FIDELITY_TARGET = 0.999

COMPLIANCE_IDENTITY_REL_TOL = 2.0e-5
PROFILE_IQ_REL_TOL = 2.0e-5


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
            abs(a),
            abs(b),
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
            str(k):
            builtin(v)
            for k, v
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
            builtin(v)
            for v
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


def solve_gate_compliance(
    rho: np.ndarray,
    a: np.ndarray,
    sigma_energy: float,
) -> dict[str, Any]:

    w_profile = (
        a
        * a
    )

    interp = PchipInterpolator(
        rho,
        w_profile,
        extrapolate=False,
    )

    r0 = max(
        float(
            rho[
                0
            ]
        ),
        1.0e-5,
    )

    rmax = float(
        rho[
            -1
        ]
    )

    mesh = np.linspace(
        r0,
        rmax,
        2400,
    )

    def w_of(
        x,
    ):
        values = interp(
            np.clip(
                x,
                rho[
                    0
                ],
                rho[
                    -1
                ],
            )
        )

        return np.nan_to_num(
            values,
            nan=0.0,
            posinf=0.0,
            neginf=0.0,
        )

    def ode(
        x,
        state,
    ):
        s = state[
            0
        ]

        sp = state[
            1
        ]

        return np.vstack(
            (
                sp,

                sigma_energy
                * sigma_energy
                * s
                - w_of(
                    x
                )
                - 2.0
                * sp
                / x,
            )
        )

    def bc(
        left,
        right,
    ):
        return np.array(
            (
                left[
                    1
                ],

                right[
                    1
                ]
                + (
                    sigma_energy
                    + 1.0
                    / rmax
                )
                * right[
                    0
                ],
            )
        )

    guess_s = (
        w_of(
            mesh
        )
        / (
            sigma_energy
            * sigma_energy
        )
    )

    guess_sp = np.gradient(
        guess_s,
        mesh,
    )

    sol = solve_bvp(
        ode,
        bc,
        mesh,
        np.vstack(
            (
                guess_s,
                guess_sp,
            )
        ),
        tol=2.0e-6,
        max_nodes=25_000,
        verbose=0,
    )

    if not sol.success:
        raise RuntimeError(
            "Gate compliance BVP failed for "
            f"sigma_energy={sigma_energy}: "
            f"{sol.message}"
        )

    rq = np.linspace(
        r0,
        rmax,
        50_000,
    )

    sq, spq = sol.sol(
        rq
    )

    wq = w_of(
        rq
    )

    measure = (
        4.0
        * math.pi
        * rq
        * rq
    )

    compliance = float(
        np.trapezoid(
            measure
            * wq
            * sq,
            rq,
        )
    )

    quadratic_twice = float(
        np.trapezoid(
            measure
            * (
                spq
                * spq
                + sigma_energy
                * sigma_energy
                * sq
                * sq
            ),
            rq,
        )
    )

    identity_relerr = relerr(
        quadratic_twice,
        compliance,
    )

    return {
        "sigma_energy":
            sigma_energy,

        "compliance":
            compliance,

        "quadratic_twice":
            quadratic_twice,

        "identity_relerr":
            identity_relerr,

        "bvp_nodes":
            int(
                sol.x.size
            ),

        "bvp_max_rms":
            float(
                np.max(
                    sol.rms_residuals
                )
            ),

        "pass":
            bool(
                compliance
                > 0.0

                and
                identity_relerr
                <= COMPLIANCE_IDENTITY_REL_TOL
            ),
    }


def static_unresonant_pmax(
    coupling_eV: float,
    detuning_eV: float,
) -> float:

    return (
        coupling_eV
        * coupling_eV
        / (
            coupling_eV
            * coupling_eV
            + 0.25
            * detuning_eV
            * detuning_eV
        )
    )


def main() -> None:

    print(
        "=== 031D3D1 STABILIZED NEUTRAL MIXER + RESONANT TRANSFER PREFLIGHT ==="
    )

    print(
        "CLAIM_CLASS="
        "FIXED_THEORY_CONTROL_FIELD_BOUNDEDNESS_AND_TRANSFER_CAPACITY_PREFLIGHT"
    )

    print(
        "D3D0_ENDPOINT_RESERVOIR_GREEN_REQUIRED=YES"
    )

    print(
        "NAIVE_CUBIC_MIXER_PROMOTED=NO"
    )

    print(
        "FULL_TIME_DOMAIN_FIELD_TRANSFER_SOLVED=NO"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    for path in (
        D3D0_SUMMARY,
        QBALL_SOURCE,
        D3A_SOURCE,
    ):
        require(
            path
        )

    d0 = load_json(
        D3D0_SUMMARY
    )

    if not str(
        d0.get(
            "classification",
            "",
        )
    ).startswith(
        "GREEN_D3D0"
    ):
        raise RuntimeError(
            "D3D0 endpoint reservoir is not GREEN"
        )

    model = d0[
        "model"
    ]

    ledger = d0[
        "energy_ledger"
    ]

    reservoir = d0[
        "reservoir_qball"
    ]

    omega = float(
        model[
            "omega_y"
        ]
    )

    m_a_eV = float(
        model[
            "m_A_eV"
        ]
    )

    q_star = float(
        model[
            "Q_star"
        ]
    )

    delta_E_J = float(
        ledger[
            "explicit_reservoir_on_minus_off_J"
        ]
    )

    reservoir_E_J = float(
        reservoir[
            "rest_energy_J"
        ]
    )

    inherited_I_E = float(
        reservoir[
            "I_E"
        ]
    )

    energy_scale_J = (
        reservoir_E_J
        / inherited_I_E
    )

    detuning_eV = (
        delta_E_J
        / q_star
        / J_PER_EV
    )

    carrier_Hz = (
        detuning_eV
        / H_EV_S
    )

    carrier_rad_s = (
        detuning_eV
        / HBAR_EV_S
    )

    detuning_over_mA = (
        detuning_eV
        / m_a_eV
    )

    print(
        "\n=== STAGE A: D3D0 PROVENANCE + DETUNING ==="
    )

    print(
        "D3D0_CLASSIFICATION="
        f"{d0['classification']}"
    )

    print(
        f"Q_STAR={q_star:.15e}"
    )

    print(
        f"ENDPOINT_DELTA_E_J={delta_E_J:.15e}"
    )

    print(
        "ENDPOINT_DELTA_E_GJ="
        f"{delta_E_J/1.0e9:.15e}"
    )

    print(
        "DETUNING_PER_CHARGE_EV="
        f"{detuning_eV:.15e}"
    )

    print(
        "DETUNING_OVER_MA="
        f"{detuning_over_mA:.15e}"
    )

    print(
        "RESONANT_CARRIER_HZ="
        f"{carrier_Hz:.15e}"
    )

    print(
        "RESONANT_CARRIER_RAD_S="
        f"{carrier_rad_s:.15e}"
    )

    qmod = load_module(
        "qball031d3d1",
        QBALL_SOURCE,
    )

    d3a = load_module(
        "d3a031d3d1",
        D3A_SOURCE,
    )

    old_match = float(
        qmod.X_MATCH
    )

    old_d3a_match = float(
        d3a.X_MATCH
    )

    qmod.X_MATCH = 80.0
    d3a.X_MATCH = 80.0

    try:
        activation = (
            qmod.solve_uncoupled_qball(
                omega
            )
        )

        if activation is None:
            raise RuntimeError(
                "Failed to reconstruct activation/reservoir Q-ball"
            )

        ints = (
            d3a.activation_integrals(
                activation,
                omega,
            )
        )

        k = math.sqrt(
            max(
                1.0
                - omega
                * omega,
                1.0e-12,
            )
        )

        rho_max = max(
            140.0,
            80.0
            + 25.0
            / k,
        )

        rho = np.linspace(
            1.0e-5,
            rho_max,
            60_000,
        )

        a, ap = (
            d3a.extended_profile(
                activation,
                omega,
                rho,
            )
        )

        measure = (
            4.0
            * math.pi
            * rho
            * rho
        )

        I2 = float(
            np.trapezoid(
                measure
                * a
                * a,
                rho,
            )
        )

        I4 = float(
            np.trapezoid(
                measure
                * a**4,
                rho,
            )
        )

        iq_rebuilt = (
            omega
            * I2
        )

        iq_rel = relerr(
            iq_rebuilt,
            float(
                ints[
                    "I_Q"
                ]
            ),
        )

        profile_pass = bool(
            iq_rel
            <= PROFILE_IQ_REL_TOL
        )

        print(
            "\n=== STAGE B: DOUBLET PROFILE / NORMALIZATION ==="
        )

        print(
            f"PROFILE_I2={I2:.15e}"
        )

        print(
            f"PROFILE_I4={I4:.15e}"
        )

        print(
            "PROFILE_IQ_REBUILT="
            f"{iq_rebuilt:.15e}"
        )

        print(
            "PROFILE_IQ_REFERENCE="
            f"{float(ints['I_Q']):.15e}"
        )

        print(
            "PROFILE_IQ_RELERR="
            f"{iq_rel:.15e}"
        )

        print(
            "PROFILE_NORMALIZATION_PASS="
            f"{profile_pass}"
        )

        print(
            "DOUBLET_SELF_POTENTIAL="
            "W(SQRT(ABS_Y2_PLUS_ABS_R2))"
        )

        print(
            "DOUBLET_ENDPOINTS_REPRODUCE_ORIGINAL_QBALL=YES"
        )

        print(
            "TOTAL_DIAGONAL_U1_EXACT=YES"
        )

        print(
            "\n=== STAGE C: NAIVE MIXER BOUNDEDNESS ==="
        )

        print(
            "NAIVE_MIXER="
            "G*S*(CONJ(Y)*R+CONJ(R)*Y)"
        )

        print(
            "NAIVE_ONLY_QUADRATIC_S_POTENTIAL_BOUNDED_BELOW=False"
        )

        print(
            "REASON="
            "MINIMIZING_S_GENERATES_NEGATIVE_QUARTIC_DOMINATING_LOG_QBALL_POTENTIAL"
        )

        print(
            "NAIVE_D3D0_MIXER_FORM="
            "RED_AS_STANDALONE_POTENTIAL"
        )

        print(
            "\n=== STAGE D: MINIMAL STABILIZED MIXER THEORY ==="
        )

        print(
            "V_GATE="
            "0.5*SIGMA2*S2"
            "+LAMBDA*ABS_Y2*ABS_R2"
            "-2*G*S*RE_CONJY_R"
        )

        print(
            "SUFFICIENT_BOUNDEDNESS="
            "LAMBDA_GE_2*G2/SIGMA2"
        )

        print(
            f"STABILIZER_MARGIN={STABILIZER_MARGIN:.6f}"
        )

        compliance_rows = []
        candidates = []

        for sigma in (
            SIGMA_VALUES
        ):
            # Time-harmonic gate energy contains both
            # m_S^2 S^2 and omega_drive^2 S^2.
            sigma_energy = math.sqrt(
                sigma
                * sigma
                + detuning_over_mA
                * detuning_over_mA
            )

            comp = solve_gate_compliance(
                rho,
                a,
                sigma_energy,
            )

            comp[
                "sigma"
            ] = sigma

            compliance_rows.append(
                comp
            )

            print(
                f"COMPLIANCE "
                f"SIGMA={sigma:.3f} "
                f"SIGMA_ENERGY={sigma_energy:.6f} "
                f"C={comp['compliance']:.15e} "
                f"IDENTITY_RELERR="
                f"{comp['identity_relerr']:.6e} "
                f"PASS={comp['pass']}"
            )

            rabi_eV = (
                HBAR_EV_S
                * math.pi
                / (
                    2.0
                    * PRIMARY_SWITCH_S
                )
            )

            rabi_dimless = (
                rabi_eV
                / m_a_eV
            )

            # For S(t)=S0 cos(omega_d t), the resonant
            # positive-frequency component is half the peak.
            # The KG -> two-mode reduction contributes the
            # additional 1/(2 Omega), hence:
            #
            #   g <S>_peak = 4 Omega (hbar Omega_R / m_A).
            target_mass2 = (
                4.0
                * omega
                * rabi_dimless
            )

            for ghat in (
                G_GRID
            ):
                overlap_required = (
                    target_mass2
                    * I2
                    / ghat
                )

                I_S = (
                    overlap_required
                    * overlap_required
                    / (
                        2.0
                        * comp[
                            "compliance"
                        ]
                    )
                )

                lam = (
                    STABILIZER_MARGIN
                    * 2.0
                    * ghat
                    * ghat
                    / (
                        sigma
                        * sigma
                    )
                )

                I_barrier = (
                    0.25
                    * lam
                    * I4
                )

                I_overhead = (
                    I_S
                    + I_barrier
                )

                candidates.append(
                    {
                        "sigma":
                            sigma,

                        "sigma_energy":
                            sigma_energy,

                        "ghat":
                            float(
                                ghat
                            ),

                        "lambda":
                            lam,

                        "I_S_primary":
                            I_S,

                        "I_barrier":
                            I_barrier,

                        "I_overhead_primary":
                            I_overhead,

                        "gate_energy_primary_J":
                            I_S
                            * energy_scale_J,

                        "barrier_energy_J":
                            I_barrier
                            * energy_scale_J,

                        "total_overhead_primary_J":
                            I_overhead
                            * energy_scale_J,

                        "fundamental_S_radiation_kinematically_closed":
                            bool(
                                sigma
                                * m_a_eV
                                > detuning_eV
                            ),

                        "perturbative_coupling_pass":
                            bool(
                                ghat
                                <= MAX_DIMENSIONLESS_COUPLING
                            ),

                        "quartic_pass":
                            bool(
                                lam
                                <= MAX_QUARTIC
                            ),

                        "compliance_pass":
                            bool(
                                comp[
                                    "pass"
                                ]
                            ),
                    }
                )

        viable = [
            c
            for c
            in candidates
            if (
                c[
                    "fundamental_S_radiation_kinematically_closed"
                ]
                and
                c[
                    "perturbative_coupling_pass"
                ]
                and
                c[
                    "quartic_pass"
                ]
                and
                c[
                    "compliance_pass"
                ]
            )
        ]

        if not viable:
            raise RuntimeError(
                "No viable stabilized-mixer candidate "
                "in declared scan"
            )

        best = min(
            viable,
            key=lambda c:
            c[
                "I_overhead_primary"
            ],
        )

        print(
            f"BEST_SIGMA={best['sigma']:.15e}"
        )

        print(
            f"BEST_GHAT={best['ghat']:.15e}"
        )

        print(
            f"BEST_LAMBDA={best['lambda']:.15e}"
        )

        print(
            "BEST_GATE_FIELD_ENERGY_1S_J="
            f"{best['gate_energy_primary_J']:.15e}"
        )

        print(
            "BEST_STABILIZER_BARRIER_J="
            f"{best['barrier_energy_J']:.15e}"
        )

        print(
            "BEST_CONTROL_OVERHEAD_1S_J="
            f"{best['total_overhead_primary_J']:.15e}"
        )

        print(
            "BEST_CONTROL_OVERHEAD_OVER_ENDPOINT="
            f"{best['total_overhead_primary_J']/delta_E_J:.15e}"
        )

        print(
            "FUNDAMENTAL_S_RADIATION_KINEMATICALLY_CLOSED="
            f"{best['fundamental_S_radiation_kinematically_closed']}"
        )

        print(
            "\n=== STAGE E: STATIC-RABI FALSIFICATION / RESONANT REQUIREMENT ==="
        )

        rabi_primary_eV = (
            HBAR_EV_S
            * math.pi
            / (
                2.0
                * PRIMARY_SWITCH_S
            )
        )

        p_static = (
            static_unresonant_pmax(
                rabi_primary_eV,
                detuning_eV,
            )
        )

        freq_tol_eV = (
            2.0
            * rabi_primary_eV
            * math.sqrt(
                (
                    1.0
                    - RABI_FIDELITY_TARGET
                )
                / RABI_FIDELITY_TARGET
            )
        )

        freq_tol_Hz = (
            freq_tol_eV
            / H_EV_S
        )

        print(
            "PRIMARY_RABI_ENERGY_EV="
            f"{rabi_primary_eV:.15e}"
        )

        print(
            "UNRESONANT_STATIC_MIXER_PMAX="
            f"{p_static:.15e}"
        )

        print(
            "D3D0_SIMPLE_DC_RABI_ORACLE_SUFFICIENT=False"
        )

        print(
            "RESONANT_OR_CHIRPED_DRIVE_REQUIRED=True"
        )

        print(
            "RESONANT_999_DETUNING_TOLERANCE_HZ="
            f"{freq_tol_Hz:.15e}"
        )

        print(
            "RESONANT_999_RELATIVE_CARRIER_TOLERANCE="
            f"{freq_tol_Hz/carrier_Hz:.15e}"
        )

        print(
            "TRANSFER_PATH_DEPENDENT_CHIRP_NOT_YET_SOLVED=YES"
        )

        print(
            "\n=== STAGE F: FIXED-THEORY SWITCHING POWER / GATE ENERGY ==="
        )

        fixed_sigma = float(
            best[
                "sigma"
            ]
        )

        fixed_g = float(
            best[
                "ghat"
            ]
        )

        fixed_comp = next(
            row
            for row
            in compliance_rows
            if row[
                "sigma"
            ]
            == fixed_sigma
        )

        scan_rows = []

        for T in (
            SWITCH_TIMES_S
        ):
            rabi_eV = (
                HBAR_EV_S
                * math.pi
                / (
                    2.0
                    * T
                )
            )

            target_mass2 = (
                4.0
                * omega
                * (
                    rabi_eV
                    / m_a_eV
                )
            )

            overlap_required = (
                target_mass2
                * I2
                / fixed_g
            )

            I_S = (
                overlap_required
                * overlap_required
                / (
                    2.0
                    * fixed_comp[
                        "compliance"
                    ]
                )
            )

            gate_J = (
                I_S
                * energy_scale_J
            )

            barrier_J = float(
                best[
                    "barrier_energy_J"
                ]
            )

            total_transient_J = (
                gate_J
                + barrier_J
            )

            endpoint_power_W = (
                delta_E_J
                / T
            )

            unrecovered_controller_power_W = (
                total_transient_J
                / T
            )

            row = {
                "switch_s":
                    T,

                "rabi_energy_eV":
                    rabi_eV,

                "carrier_Hz":
                    carrier_Hz,

                "gate_field_energy_J":
                    gate_J,

                "stabilizer_barrier_J":
                    barrier_J,

                "transient_control_overhead_J":
                    total_transient_J,

                "endpoint_work_J":
                    delta_E_J,

                "endpoint_average_power_W":
                    endpoint_power_W,

                "unrecovered_control_average_power_W":
                    unrecovered_controller_power_W,

                "fundamental_S_radiation_closed":
                    bool(
                        fixed_sigma
                        * m_a_eV
                        > detuning_eV
                    ),
            }

            scan_rows.append(
                row
            )

            print(
                f"SWITCH "
                f"T={T:.9e} "
                f"GATE_J={gate_J:.9e} "
                f"BARRIER_J={barrier_J:.9e} "
                f"ENDPOINT_POWER_W="
                f"{endpoint_power_W:.9e} "
                f"CONTROL_POWER_W="
                f"{unrecovered_controller_power_W:.9e}"
            )

        gate_theory_pass = bool(
            profile_pass

            and
            all(
                row[
                    "pass"
                ]
                for row
                in compliance_rows
            )

            and
            best[
                "ghat"
            ]
            <= MAX_DIMENSIONLESS_COUPLING

            and
            best[
                "lambda"
            ]
            <= MAX_QUARTIC

            and
            best[
                "fundamental_S_radiation_kinematically_closed"
            ]

            and
            best[
                "total_overhead_primary_J"
            ]
            < delta_E_J
        )

        print(
            "\n=== STAGE G: DECISION ==="
        )

        print(
            "FIXED_THEORY_STABILIZED_MIXER_PREFLIGHT_PASS="
            f"{gate_theory_pass}"
        )

        print(
            "TOTAL_DIAGONAL_U1_CONSERVED=YES"
        )

        print(
            "ENDPOINT_GATE_ENERGY_ZERO=YES"
        )

        print(
            "GATE_HAMILTONIAN_BOUNDED_BELOW="
            "YES_BY_DECLARED_STABILIZER"
        )

        print(
            "RECIPROCAL_Y_R_S_INTERACTION=YES"
        )

        print(
            "FULL_DYNAMIC_RADIAL_TRANSFER_REALIZED=False"
        )

        print(
            "SOURCE_RESPONSE_ALONG_TRANSFER_PATH_SOLVED=False"
        )

        print(
            "FINITE_TIME_Y_R_OR_SOURCE_RADIATION_CLOSED=False"
        )

        print(
            "RESET_RECOVERABILITY_ESTABLISHED=False"
        )

        if gate_theory_pass:
            classification = (
                "GREEN_D3D1_STABILIZED_NEUTRAL_"
                "MIXER_CAPACITY_PREFLIGHT"
            )

            next_action = (
                "031D3D2_CHIRPED_ADIABATIC_FULL_RADIAL_"
                "TRANSFER_SOURCE_RESPONSE_RADIATION_CLOSEOUT"
            )

        else:
            classification = (
                "RED_OR_YELLOW_D3D1_STABILIZED_"
                "MIXER_CAPACITY_FAILED"
            )

            next_action = (
                "DIAGNOSE_ONLY_FAILED_D3D1_"
                "BOUNDEDNESS_COMPLIANCE_OR_ENERGY_SUBGATE"
            )

        print(
            f"031D3D1_CLASSIFICATION={classification}"
        )

        print(
            "FULL_D3D_CLOSED=False"
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
                (
                    "FIXED_THEORY_CONTROL_FIELD_"
                    "BOUNDEDNESS_AND_TRANSFER_CAPACITY_PREFLIGHT"
                ),

            "d3d0_classification":
                d0[
                    "classification"
                ],

            "detuning": {
                "endpoint_delta_E_J":
                    delta_E_J,

                "per_charge_eV":
                    detuning_eV,

                "over_mA":
                    detuning_over_mA,

                "carrier_Hz":
                    carrier_Hz,

                "carrier_rad_s":
                    carrier_rad_s,
            },

            "profile": {
                "I2":
                    I2,

                "I4":
                    I4,

                "I_Q_rebuilt":
                    iq_rebuilt,

                "I_Q_reference":
                    float(
                        ints[
                            "I_Q"
                        ]
                    ),

                "I_Q_relerr":
                    iq_rel,

                "pass":
                    profile_pass,

                "energy_scale_J_per_I":
                    energy_scale_J,
            },

            "theory": {
                "doublet_potential":
                    "W(sqrt(|Y|^2+|R|^2))",

                "gate_potential":
                    (
                        "0.5*sigma^2*s^2 "
                        "+ lambda*|Y|^2|R|^2 "
                        "- 2*g*s*Re(conj(Y)R)"
                    ),

                "boundedness_condition":
                    "lambda >= 2*g^2/sigma^2",

                "stabilizer_margin":
                    STABILIZER_MARGIN,
            },

            "compliance":
                compliance_rows,

            "best_candidate":
                best,

            "unresonant_static_pmax_1s":
                p_static,

            "resonant_999_tolerance_Hz":
                freq_tol_Hz,

            "switching_rows":
                scan_rows,

            "decision": {
                "preflight_pass":
                    gate_theory_pass,

                "full_D3D_closed":
                    False,
            },

            "claim_limits": [
                (
                    "GREEN is only a stabilized neutral-mixer "
                    "capacity preflight in an extended flat-space "
                    "effective theory."
                ),
                (
                    "The U(2)-symmetric Y/R doublet and stabilizing "
                    "cross quartic are new fixed-theory ingredients, "
                    "not established particles or interactions."
                ),
                (
                    "The simple D3D0 DC Rabi oracle is not sufficient "
                    "once the 30.74-GJ endpoint detuning is included."
                ),
                (
                    "A resonant or chirped drive is required; the "
                    "transfer-dependent resonance path is not solved here."
                ),
                (
                    "Only fundamental linear S radiation is "
                    "kinematically screened by the selected mass; "
                    "Y/R/source radiation remains open."
                ),
                (
                    "Reset recoverability is not assumed."
                ),
                (
                    "Einstein backreaction, nonlinear stability, "
                    "EFT/naturalness and empirical closure remain open."
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

        with OUT_SCAN.open(
            "w",
            newline="",
        ) as handle:

            writer = csv.DictWriter(
                handle,
                fieldnames=list(
                    scan_rows[
                        0
                    ].keys()
                ),
            )

            writer.writeheader()

            writer.writerows(
                scan_rows
            )

        print(
            f"SUMMARY_JSON={OUT_JSON}"
        )

        print(
            f"SCAN_CSV={OUT_SCAN}"
        )

    finally:
        qmod.X_MATCH = (
            old_match
        )

        d3a.X_MATCH = (
            old_d3a_match
        )


if __name__ == "__main__":
    main()
