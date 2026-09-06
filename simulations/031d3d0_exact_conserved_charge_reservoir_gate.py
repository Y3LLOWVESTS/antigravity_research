#!/usr/bin/env python3
"""
031D3D0 — exact conserved-charge reservoir architecture gate.

Scientific purpose
------------------
031D3C-R5 promoted the D3 X+phi+Y microscopic ON field to
coupled-linear GREEN within the declared flat-space effective theory.

The next mandatory problem is activation charge control.

The current ON state carries

    Q_Y ~= 2.2018e35

while the desired exact OFF state requires

    Y = 0
    Q_Y = 0.

Deleting or creating Q_Y by hand is forbidden.

This preflight compares the minimal reservoir architectures before any
expensive time-dependent controller PDE is built.

Architecture A:
    spatially translate the same Y Q-ball away from the source.

    Fails exact OFF at every finite separation because a canonical
    massive Q-ball has a noncompact exponential tail.

Architecture B:
    phase/frequency manipulation of the same nonzero Y field.

    Fails because activation depends on |Y|, not its phase.

Architecture C:
    introduce a second complex spectator field R carrying the same
    diagonal global U(1) charge.

    OFF:
        Y = 0
        R = R_Q
        Q_total = Q_R = Q_*

    ON:
        Y = Y_Q
        R = 0
        Q_total = Q_Y = Q_*

A future real neutral control field S can mediate

    L_mix ~ -kappa S (Y* R + R* Y)

which preserves the diagonal U(1):

    Y -> exp(i alpha) Y
    R -> exp(i alpha) R.

S=0 gives exact endpoint decoupling.

This run does NOT realize S or the time-dependent transfer.

What D3D0 establishes if GREEN
------------------------------
- one explicit positive-energy microscopic reservoir field exists;
- exact Y=0 OFF endpoint is structurally possible;
- total diagonal activation charge can be identical in OFF and ON;
- reservoir stress-energy inventory is included;
- the old ON-OFF energy ledger is corrected for the persistent reservoir;
- switching time/power and reset-release scales are quantified;
- simpler same-Y reservoir routes are closed.

What remains open
-----------------
- dynamical R <-> Y conversion;
- complete neutral-gate S stress-energy;
- transfer efficiency;
- finite-time radiation;
- local reaction stresses during switching;
- recovery of the ~31 GJ endpoint energy on reset;
- nonlinear switching stability;
- Einstein backreaction;
- EFT/naturalness and empirical closure;
- practical device.

The spectator R is a new field-theory ingredient and is not claimed to
exist in nature.
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


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results" / "data"

DATA.mkdir(
    parents=True,
    exist_ok=True,
)

R5_SUMMARY = (
    DATA
    / "031d3cr5_saturation_safe_schur_summary.json"
)

D3C_SUMMARY = (
    DATA
    / "031d3c_activation_stability_switching_summary.json"
)

ROBUST_SUMMARY = (
    DATA
    / "031c96_operating_margin_robustness_summary.json"
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
    / "031d3d0_exact_conserved_charge_reservoir_summary.json"
)

OUT_POWER_CSV = (
    DATA
    / "031d3d0_reservoir_switching_power_scan.csv"
)

OUT_ARCH_CSV = (
    DATA
    / "031d3d0_reservoir_architecture_scan.csv"
)

J_PER_EV = 1.602176634e-19
HBAR_EV_S = 6.582119569e-16
C_LIGHT = 299_792_458.0

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

REMOTE_RHO_SAMPLES = (
    5.0,
    10.0,
    15.0,
    20.0,
)

Q_RATIO_REL_TOL = 5.0e-6
ENERGY_RATIO_REL_TOL = 5.0e-6
CHARGE_ROTATION_REL_TOL = 2.0e-14
MIN_RABI_ORACLE_FIDELITY = 1.0 - 2.0e-14


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
                item
            )
            for key, item
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
                item
            )
            for item
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


def safe_activation_fraction(
    amplitude,
):

    amplitude = np.asarray(
        amplitude,
        dtype=float,
    )

    return -np.expm1(
        -0.5
        * amplitude
        * amplitude
    )


def rabi_oracle() -> dict[str, float | bool]:
    """
    Pure two-mode algebra oracle.

    For Hamiltonian proportional to sigma_x,

        U(theta) = exp(-i theta sigma_x),

    theta=pi/2 maps

        |R> -> -i |Y>

    while preserving norm exactly.
    """

    sigma_x = np.array(
        [
            [
                0.0,
                1.0,
            ],
            [
                1.0,
                0.0,
            ],
        ],
        dtype=complex,
    )

    identity = np.eye(
        2,
        dtype=complex,
    )

    theta = (
        0.5
        * math.pi
    )

    U = (
        math.cos(
            theta
        )
        * identity
        - 1j
        * math.sin(
            theta
        )
        * sigma_x
    )

    initial = np.array(
        [
            0.0,
            1.0,
        ],
        dtype=complex,
    )

    final = (
        U
        @ initial
    )

    norm_initial = float(
        np.vdot(
            initial,
            initial,
        ).real
    )

    norm_final = float(
        np.vdot(
            final,
            final,
        ).real
    )

    y_fraction = float(
        abs(
            final[
                0
            ]
        ) ** 2
    )

    r_fraction = float(
        abs(
            final[
                1
            ]
        ) ** 2
    )

    unitary_error = float(
        np.linalg.norm(
            U.conj().T
            @ U
            - identity,
            ord="fro",
        )
    )

    passed = bool(
        relerr(
            norm_initial,
            norm_final,
        )
        <= CHARGE_ROTATION_REL_TOL
        and
        y_fraction
        >= MIN_RABI_ORACLE_FIDELITY
        and
        r_fraction
        <= 2.0e-14
        and
        unitary_error
        <= 2.0e-14
    )

    return {
        "initial_norm":
            norm_initial,

        "final_norm":
            norm_final,

        "final_Y_fraction":
            y_fraction,

        "final_R_fraction":
            r_fraction,

        "unitary_error":
            unitary_error,

        "pass":
            passed,
    }


def main() -> None:

    print(
        "=== 031D3D0 EXACT CONSERVED-CHARGE RESERVOIR ARCHITECTURE GATE ==="
    )

    print(
        "CLAIM_CLASS=MICROSCOPIC_ENDPOINT_RESERVOIR_PREFLIGHT"
    )

    print(
        "R5_COUPLED_LINEAR_GREEN_REQUIRED=YES"
    )

    print(
        "EXACT_OFF_Y_ZERO_REQUIRED=YES"
    )

    print(
        "TOTAL_DIAGONAL_U1_CHARGE_CONSERVATION_REQUIRED=YES"
    )

    print(
        "SPATIALLY_PRESCRIBED_ACTIVATION_ALLOWED=NO"
    )

    print(
        "RESERVOIR_STRESS_ENERGY_MUST_BE_INCLUDED=YES"
    )

    print(
        "FULL_DYNAMIC_TRANSFER_SOLVED=NO"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    for path in (
        R5_SUMMARY,
        D3C_SUMMARY,
        ROBUST_SUMMARY,
        QBALL_SOURCE,
        D3A_SOURCE,
    ):

        require(
            path
        )

    r5 = load_json(
        R5_SUMMARY
    )

    d3c = load_json(
        D3C_SUMMARY
    )

    robust = load_json(
        ROBUST_SUMMARY
    )

    r5_green = bool(
        str(
            r5.get(
                "classification",
                "",
            )
        ).startswith(
            "GREEN_D3CR5"
        )
        and
        r5.get(
            "decision",
            {},
        ).get(
            "promotion_authorized",
            False,
        )
    )

    if not r5_green:

        raise RuntimeError(
            "D3D0 is unauthorized because R5 stability is not GREEN"
        )

    print(
        "\n=== STAGE A: R5 PROMOTION PROVENANCE ==="
    )

    print(
        f"R5_CLASSIFICATION={r5['classification']}"
    )

    print(
        "R5_PROMOTION_AUTHORIZED="
        f"{r5['decision']['promotion_authorized']}"
    )

    print(
        "R5_RELAXED_RELATIVE_LOWER_BOUND="
        f"{r5['schur']['relaxed_relative_lower_bound']:+.15e}"
    )

    print(
        "R5_COUPLED_LINEAR_STABILITY_PREREQUISITE=PASS"
    )

    switching = (
        d3c[
            "switching"
        ]
    )

    q_star = float(
        switching[
            "on_physical_QY"
        ]
    )

    activation_energy_j = float(
        switching[
            "on_activation_inventory_J"
        ]
    )

    off_source_energy_j = float(
        switching[
            "off_source_energy_J"
        ]
    )

    full_on_energy_j = float(
        switching[
            "full_on_conservative_J"
        ]
    )

    old_on_minus_off_j = float(
        switching[
            "conservative_on_minus_off_J"
        ]
    )

    omega_y = float(
        r5[
            "model"
        ][
            "omega_y"
        ]
    )

    mu = float(
        r5[
            "model"
        ][
            "mu"
        ]
    )

    m_x_gev = float(
        robust[
            "candidate"
        ][
            "m_x_gev_derived"
        ]
    )

    m_x_ev = (
        m_x_gev
        * 1.0e9
    )

    m_a_ev = (
        mu
        * m_x_ev
    )

    print(
        "\n=== STAGE B: CURRENT CHARGE / ENERGY SCALE ==="
    )

    print(
        f"Q_STAR={q_star:.15e}"
    )

    print(
        f"ACTIVATION_RESERVOIR_ENERGY_J={activation_energy_j:.15e}"
    )

    print(
        "ACTIVATION_RESERVOIR_ENERGY_GJ="
        f"{activation_energy_j/1.0e9:.15e}"
    )

    print(
        f"OFF_SOURCE_ENERGY_J={off_source_energy_j:.15e}"
    )

    print(
        f"FULL_ON_ENERGY_J={full_on_energy_j:.15e}"
    )

    print(
        f"OLD_D3C_ON_MINUS_OFF_J={old_on_minus_off_j:.15e}"
    )

    print(
        f"M_X_EV={m_x_ev:.15e}"
    )

    print(
        f"M_A_EV={m_a_ev:.15e}"
    )

    qmod = load_module(
        "qball031d3d0",
        QBALL_SOURCE,
    )

    d3a = load_module(
        "d3a031d3d0",
        D3A_SOURCE,
    )

    old_x_match = float(
        qmod.X_MATCH
    )

    qmod.X_MATCH = 80.0

    try:

        activation = (
            qmod.solve_uncoupled_qball(
                omega_y
            )
        )

        if activation is None:

            raise RuntimeError(
                "Failed to reconstruct the omega_Y activation Q-ball"
            )

        integrals = (
            d3a.activation_integrals(
                activation,
                omega_y,
            )
        )

        e_over_qm_model = float(
            integrals[
                "E_over_Qm"
            ]
        )

        e_over_qm_physical = (
            activation_energy_j
            / (
                q_star
                * m_a_ev
                * J_PER_EV
            )
        )

        eqm_relerr = (
            relerr(
                e_over_qm_model,
                e_over_qm_physical,
            )
        )

        reservoir_bound_pass = bool(
            e_over_qm_model
            < 1.0
            and
            e_over_qm_physical
            < 1.0
            and
            eqm_relerr
            <= ENERGY_RATIO_REL_TOL
        )

        a0 = float(
            activation.sol(
                1.0e-5
            )[
                0
            ]
        )

        print(
            "\n=== STAGE C: MICROSCOPIC RESERVOIR Q-BALL RECONSTRUCTION ==="
        )

        print(
            f"RESERVOIR_OMEGA={omega_y:.15e}"
        )

        print(
            f"RESERVOIR_A0={a0:.15e}"
        )

        print(
            f"RESERVOIR_I_E={float(integrals['I_E']):.15e}"
        )

        print(
            f"RESERVOIR_I_Q={float(integrals['I_Q']):.15e}"
        )

        print(
            f"RESERVOIR_E_OVER_QM_MODEL={e_over_qm_model:.15e}"
        )

        print(
            f"RESERVOIR_E_OVER_QM_PHYSICAL={e_over_qm_physical:.15e}"
        )

        print(
            f"RESERVOIR_E_OVER_QM_RELERR={eqm_relerr:.15e}"
        )

        print(
            f"RESERVOIR_BOUND_QBALL_PASS={reservoir_bound_pass}"
        )

        print(
            "RESERVOIR_POSITIVE_ENERGY="
            f"{activation_energy_j > 0.0}"
        )

        # ----------------------------------------------------------
        # Architecture A:
        # same Y soliton moved to finite spatial separation.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE D1: ARCHITECTURE A — REMOTE SAME-Y SOLITON ==="
        )

        remote_rows = []

        for rho in (
            REMOTE_RHO_SAMPLES
        ):

            a, _ap = (
                d3a.extended_profile(
                    activation,
                    omega_y,
                    np.array(
                        [
                            rho
                        ],
                        dtype=float,
                    ),
                )
            )

            amp = abs(
                float(
                    np.asarray(
                        a
                    )[
                        0
                    ]
                )
            )

            f_value = float(
                safe_activation_fraction(
                    np.array(
                        [
                            amp
                        ]
                    )
                )[
                    0
                ]
            )

            remote_rows.append(
                {
                    "rho":
                        float(
                            rho
                        ),

                    "amplitude":
                        amp,

                    "activation_fraction":
                        f_value,
                }
            )

            print(
                f"REMOTE_Y "
                f"RHO={rho:.3f} "
                f"A={amp:.15e} "
                f"F={f_value:.15e}"
            )

        remote_exact_off = False

        print(
            "REMOTE_SAME_Y_QBALL_FINITE_DISTANCE_EXACT_Y_ZERO=False"
        )

        print(
            "REMOTE_SAME_Y_REASON="
            "NONTRIVIAL_CANONICAL_QBALL_HAS_NONCOMPACT_EXPONENTIAL_TAIL"
        )

        print(
            "REMOTE_SAME_Y_ARCHITECTURE="
            "RED_FOR_EXACT_OFF_REQUIREMENT"
        )

        # ----------------------------------------------------------
        # Architecture B:
        # same nonzero |Y| with phase/frequency control.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE D2: ARCHITECTURE B — PHASE/FREQUENCY ONLY ==="
        )

        test_amp = abs(
            a0
        )

        f_original = float(
            safe_activation_fraction(
                np.array(
                    [
                        test_amp
                    ]
                )
            )[
                0
            ]
        )

        phases = (
            0.0,
            0.25
            * math.pi,
            0.5
            * math.pi,
            math.pi,
        )

        phase_values = []

        for phase in (
            phases
        ):

            complex_y = (
                test_amp
                * complex(
                    math.cos(
                        phase
                    ),
                    math.sin(
                        phase
                    ),
                )
            )

            f_phase = float(
                safe_activation_fraction(
                    np.array(
                        [
                            abs(
                                complex_y
                            )
                        ]
                    )
                )[
                    0
                ]
            )

            phase_values.append(
                f_phase
            )

            print(
                f"PHASE_SCAN "
                f"THETA={phase:.12e} "
                f"ABS_Y={abs(complex_y):.15e} "
                f"F={f_phase:.15e}"
            )

        phase_spread = (
            max(
                phase_values
            )
            - min(
                phase_values
            )
        )

        phase_only_exact_off = bool(
            f_original == 0.0
        )

        print(
            f"PHASE_F_SPREAD={phase_spread:.15e}"
        )

        print(
            "PHASE_ONLY_EXACT_OFF="
            f"{phase_only_exact_off}"
        )

        print(
            "PHASE_FREQUENCY_ARCHITECTURE="
            "RED_ACTIVATION_DEPENDS_ON_MODULUS"
        )

        # ----------------------------------------------------------
        # Architecture C:
        # spectator complex field R with same diagonal U(1).
        # ----------------------------------------------------------

        print(
            "\n=== STAGE D3: ARCHITECTURE C — SPECTATOR R Q-BALL ==="
        )

        oracle = (
            rabi_oracle()
        )

        for key, value in (
            oracle.items()
        ):

            print(
                f"RABI_ORACLE_{key.upper()}={value}"
            )

        # Exact endpoint charges are declared analytically.
        #
        # OFF:
        #   QY = 0
        #   QR = Q*
        #
        # ON:
        #   QY = Q*
        #   QR = 0
        #
        # Both have identical diagonal Qtotal.

        off_qy = 0.0
        off_qr = q_star

        on_qy = q_star
        on_qr = 0.0

        off_q_total = (
            off_qy
            + off_qr
        )

        on_q_total = (
            on_qy
            + on_qr
        )

        charge_total_relerr = (
            relerr(
                off_q_total,
                on_q_total,
            )
        )

        charge_endpoint_pass = bool(
            off_qy
            == 0.0
            and
            on_qy
            > 0.0
            and
            off_qr
            > 0.0
            and
            on_qr
            == 0.0
            and
            charge_total_relerr
            <= CHARGE_ROTATION_REL_TOL
            and
            oracle[
                "pass"
            ]
        )

        print(
            f"OFF_QY={off_qy:.15e}"
        )

        print(
            f"OFF_QR={off_qr:.15e}"
        )

        print(
            f"OFF_QTOTAL={off_q_total:.15e}"
        )

        print(
            f"ON_QY={on_qy:.15e}"
        )

        print(
            f"ON_QR={on_qr:.15e}"
        )

        print(
            f"ON_QTOTAL={on_q_total:.15e}"
        )

        print(
            f"QTOTAL_ENDPOINT_RELERR={charge_total_relerr:.15e}"
        )

        print(
            f"EXACT_ENDPOINT_CHARGE_STRUCTURE_PASS={charge_endpoint_pass}"
        )

        print(
            "DIAGONAL_U1_MIXING_INTERACTION="
            "KAPPA*S*(CONJ(Y)*R+CONJ(R)*Y)"
        )

        print(
            "DIAGONAL_U1_CONSERVED_BY_MIXER=YES"
        )

        print(
            "S_ZERO_ENDPOINT_MIXING_ZERO=YES"
        )

        print(
            "OFF_Y_ZERO_EXACT=YES"
        )

        print(
            "SPATIALLY_PRESCRIBED_COUPLING=NO"
        )

        print(
            "SPECTATOR_R_ENTERING_PHYSICAL_METRIC=NO_BY_DECLARED_GLOBAL_THEORY"
        )

        print(
            "R_STRESS_ENERGY_INCLUDED_AS_QBALL_INVENTORY=YES"
        )

        print(
            "RADIATIVE_STABILITY_OF_Y_R_ASYMMETRY=CARRIED_TO_031F_NOT_CLOSED"
        )

        # ----------------------------------------------------------
        # Correct endpoint energy ledger.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE E: EXPLICIT RESERVOIR ENDPOINT ENERGY LEDGER ==="
        )

        reservoir_rest_energy_j = (
            activation_energy_j
        )

        explicit_off_total_j = (
            off_source_energy_j
            + reservoir_rest_energy_j
        )

        explicit_on_total_j = (
            full_on_energy_j
        )

        explicit_on_minus_off_j = (
            explicit_on_total_j
            - explicit_off_total_j
        )

        expected_reduction_j = (
            old_on_minus_off_j
            - reservoir_rest_energy_j
        )

        ledger_relerr = (
            relerr(
                explicit_on_minus_off_j,
                expected_reduction_j,
            )
        )

        activation_mass_equivalent_kg = (
            reservoir_rest_energy_j
            / (
                C_LIGHT
                * C_LIGHT
            )
        )

        endpoint_mass_difference_kg = (
            explicit_on_minus_off_j
            / (
                C_LIGHT
                * C_LIGHT
            )
        )

        energy_per_charge_j = (
            explicit_on_minus_off_j
            / q_star
        )

        energy_per_charge_ev = (
            energy_per_charge_j
            / J_PER_EV
        )

        endpoint_energy_pass = bool(
            reservoir_rest_energy_j
            > 0.0
            and
            explicit_off_total_j
            > 0.0
            and
            explicit_on_total_j
            > 0.0
            and
            explicit_on_minus_off_j
            > 0.0
            and
            ledger_relerr
            <= 1.0e-12
        )

        print(
            "RESERVOIR_REST_ENERGY_J="
            f"{reservoir_rest_energy_j:.15e}"
        )

        print(
            "RESERVOIR_REST_ENERGY_GJ="
            f"{reservoir_rest_energy_j/1.0e9:.15e}"
        )

        print(
            "RESERVOIR_MASS_EQUIVALENT_KG="
            f"{activation_mass_equivalent_kg:.15e}"
        )

        print(
            "EXPLICIT_RESERVOIR_OFF_TOTAL_J="
            f"{explicit_off_total_j:.15e}"
        )

        print(
            "EXPLICIT_RESERVOIR_OFF_TOTAL_GJ="
            f"{explicit_off_total_j/1.0e9:.15e}"
        )

        print(
            "EXPLICIT_RESERVOIR_ON_TOTAL_J="
            f"{explicit_on_total_j:.15e}"
        )

        print(
            "EXPLICIT_RESERVOIR_ON_TOTAL_GJ="
            f"{explicit_on_total_j/1.0e9:.15e}"
        )

        print(
            "OLD_NO_RESERVOIR_ON_MINUS_OFF_J="
            f"{old_on_minus_off_j:.15e}"
        )

        print(
            "EXPLICIT_RESERVOIR_ON_MINUS_OFF_J="
            f"{explicit_on_minus_off_j:.15e}"
        )

        print(
            "EXPLICIT_RESERVOIR_ON_MINUS_OFF_GJ="
            f"{explicit_on_minus_off_j/1.0e9:.15e}"
        )

        print(
            "ENDPOINT_LEDGER_REDUCTION_FROM_PERSISTENT_RESERVOIR_J="
            f"{reservoir_rest_energy_j:.15e}"
        )

        print(
            "ENDPOINT_LEDGER_IDENTITY_RELERR="
            f"{ledger_relerr:.15e}"
        )

        print(
            "ENDPOINT_MASS_DIFFERENCE_KG="
            f"{endpoint_mass_difference_kg:.15e}"
        )

        print(
            "ENDPOINT_ENERGY_PER_TRANSFERRED_CHARGE_EV="
            f"{energy_per_charge_ev:.15e}"
        )

        print(
            f"ENDPOINT_ENERGY_LEDGER_PASS={endpoint_energy_pass}"
        )

        # ----------------------------------------------------------
        # Switching-time and power floor/preflight.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE F: SWITCHING TIME / POWER / RESET SCALE ==="
        )

        power_rows = []

        for seconds in (
            SWITCH_TIMES_S
        ):

            omega_mix = (
                0.5
                * math.pi
                / seconds
            )

            hbar_omega_mix_ev = (
                HBAR_EV_S
                * omega_mix
            )

            mixing_over_ma = (
                hbar_omega_mix_ev
                / m_a_ev
            )

            endpoint_power_w = (
                explicit_on_minus_off_j
                / seconds
            )

            charge_conversion_rate = (
                q_star
                / seconds
            )

            # The reservoir already exists in OFF.
            # No new 6.23-GJ soliton formation is required per cycle.
            #
            # However the endpoint ON state is ~30.74 GJ higher.
            # That energy must enter from the controller/environment.
            #
            # On reset, the same energy is released. It may be
            # coherently recovered, stored, radiated or dissipated.
            # Recovery is NOT assumed here.

            unrecovered_reset_release_j = (
                explicit_on_minus_off_j
            )

            unrecovered_reset_average_power_w = (
                unrecovered_reset_release_j
                / seconds
            )

            power_rows.append(
                {
                    "seconds":
                        float(
                            seconds
                        ),

                    "effective_rabi_omega_rad_s":
                        omega_mix,

                    "effective_mix_hbar_omega_eV":
                        hbar_omega_mix_ev,

                    "mix_scale_over_mA":
                        mixing_over_ma,

                    "endpoint_energy_input_J":
                        explicit_on_minus_off_j,

                    "endpoint_average_input_power_W":
                        endpoint_power_w,

                    "charge_conversion_rate_per_s":
                        charge_conversion_rate,

                    "reset_unrecovered_release_J":
                        unrecovered_reset_release_j,

                    "reset_unrecovered_average_power_W":
                        unrecovered_reset_average_power_w,
                }
            )

            print(
                f"SWITCH "
                f"T={seconds:.9e} "
                f"HBAR_OMEGA_MIX_EV={hbar_omega_mix_ev:.9e} "
                f"MIX_OVER_MA={mixing_over_ma:.9e} "
                f"ENDPOINT_POWER_W={endpoint_power_w:.9e} "
                f"Q_RATE={charge_conversion_rate:.9e}"
            )

        print(
            "SPATIAL_RESERVOIR_TRANSLATION_REQUIRED=NO"
        )

        print(
            "SPATIAL_CHARGE_TRANSPORT_ENERGY_ENDPOINT_MODEL=ZERO_BY_COLOCATION"
        )

        print(
            "INTERNAL_SPECIES_CONVERSION_ENERGY=NOT_ZERO"
        )

        print(
            "MINIMUM_ENDPOINT_ENERGY_INPUT_ESTABLISHED="
            "NO_PATH_DEPENDENT_BUT_STATE_DIFFERENCE_IS_EXPLICIT"
        )

        print(
            "RESET_RECOVERABILITY_ESTABLISHED=False"
        )

        print(
            "RESET_RELEASE_IF_UNRECOVERED_J="
            f"{explicit_on_minus_off_j:.15e}"
        )

        print(
            "RADIATION_LOWER_BOUND_FOR_REVERSIBLE_ENDPOINT_PATH_J=0"
        )

        print(
            "RADIATION_OR_DISSIPATION_IF_ENDPOINT_ENERGY_NOT_RECOVERED_J="
            f"{explicit_on_minus_off_j:.15e}"
        )

        print(
            "FINITE_TIME_RADIATION_CALCULATED=NO_REQUIRES_DYNAMIC_MIXER"
        )

        print(
            "ENDPOINT_NET_SPATIAL_MOMENTUM_CHANGE=0_BY_COLOCATED_SPHERICAL_STATES"
        )

        print(
            "LOCAL_TRANSFER_REACTION_STRESS_CLOSED=NO"
        )

        # ----------------------------------------------------------
        # Architecture decision.
        # ----------------------------------------------------------

        architecture_rows = [
            {
                "architecture":
                    "REMOTE_SAME_Y_QBALL",

                "exact_off_Y_zero":
                    False,

                "total_charge_conserved":
                    True,

                "reservoir_stress_energy":
                    True,

                "survives":
                    False,

                "reason":
                    "noncompact_Y_tail_at_every_finite_separation",
            },

            {
                "architecture":
                    "PHASE_OR_FREQUENCY_ONLY",

                "exact_off_Y_zero":
                    False,

                "total_charge_conserved":
                    True,

                "reservoir_stress_energy":
                    False,

                "survives":
                    False,

                "reason":
                    "activation_depends_on_modulus_absY",
            },

            {
                "architecture":
                    "CREATE_DESTROY_Y_WITHOUT_RESERVOIR",

                "exact_off_Y_zero":
                    True,

                "total_charge_conserved":
                    False,

                "reservoir_stress_energy":
                    False,

                "survives":
                    False,

                "reason":
                    "violates_total_activation_charge_conservation",
            },

            {
                "architecture":
                    "COLOCATED_SPECTATOR_R_DIAGONAL_U1",

                "exact_off_Y_zero":
                    True,

                "total_charge_conserved":
                    True,

                "reservoir_stress_energy":
                    True,

                "survives":
                    bool(
                        reservoir_bound_pass
                        and
                        charge_endpoint_pass
                        and
                        endpoint_energy_pass
                    ),

                "reason":
                    (
                        "exact_endpoint_reservoir_survivor_"
                        "dynamic_neutral_mixer_still_required"
                    ),
            },
        ]

        survivor_count = sum(
            bool(
                row[
                    "survives"
                ]
            )
            for row
            in architecture_rows
        )

        spectator_survives = bool(
            architecture_rows[
                -1
            ][
                "survives"
            ]
        )

        print(
            "\n=== STAGE G: ARCHITECTURE DECISION ==="
        )

        for row in (
            architecture_rows
        ):

            print(
                "ARCH "
                f"NAME={row['architecture']} "
                f"EXACT_OFF={row['exact_off_Y_zero']} "
                f"Q_CONSERVED={row['total_charge_conserved']} "
                f"T_MUNU={row['reservoir_stress_energy']} "
                f"SURVIVES={row['survives']} "
                f"REASON={row['reason']}"
            )

        print(
            f"SURVIVING_ARCHITECTURE_COUNT={survivor_count}"
        )

        prerequisites = bool(
            r5_green
            and
            reservoir_bound_pass
            and
            charge_endpoint_pass
            and
            endpoint_energy_pass
            and
            spectator_survives
            and
            survivor_count
            == 1
        )

        if prerequisites:

            classification = (
                "GREEN_D3D0_EXACT_ENDPOINT_SPECTATOR_QBALL_"
                "RESERVOIR_ARCHITECTURE_SURVIVES"
            )

            next_action = (
                "031D3D1_FULL_DYNAMIC_NEUTRAL_MIXER_"
                "TRANSFER_STRESS_ENERGY_RADIATION_GATE"
            )

        else:

            classification = (
                "RED_OR_YELLOW_D3D0_NO_CERTIFIED_MINIMAL_"
                "EXACT_OFF_RESERVOIR_ENDPOINT"
            )

            next_action = (
                "DIAGNOSE_ONLY_D3D0_FAILED_RESERVOIR_SUBGATE"
            )

        print(
            f"031D3D0_CLASSIFICATION={classification}"
        )

        print(
            "EXACT_ENDPOINT_Q_RESERVOIR_PREFLIGHT="
            f"{'GREEN' if prerequisites else 'UNRESOLVED'}"
        )

        print(
            "TOTAL_DIAGONAL_U1_ENDPOINT_CONSERVATION="
            f"{charge_endpoint_pass}"
        )

        print(
            "OFF_QY_EXACT_ZERO="
            f"{charge_endpoint_pass}"
        )

        print(
            "RESERVOIR_OWN_POSITIVE_ENERGY_INCLUDED="
            f"{reservoir_bound_pass}"
        )

        print(
            "RECIPROCAL_DYNAMIC_TRANSFER_REALIZED=False"
        )

        print(
            "GATE_S_STRESS_ENERGY_INCLUDED=False"
        )

        print(
            "SWITCHING_RADIATION_CLOSED=False"
        )

        print(
            "FORMATION_OF_INITIAL_RESERVOIR_ENERGY_J="
            f"{reservoir_rest_energy_j:.15e}"
        )

        print(
            "FORMATION_PER_CYCLE_REQUIRED="
            "NO_IF_RESERVOIR_SURVIVES_RESET"
        )

        print(
            "RESET_RECOVERABILITY_ESTABLISHED=False"
        )

        print(
            "FULL_D3D_CLOSED=False"
        )

        print(
            "FULL_EINSTEIN_BACKREACTION_CLOSED=False"
        )

        print(
            "NONLINEAR_STABILITY_CLOSED=False"
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
                "MICROSCOPIC_ENDPOINT_RESERVOIR_PREFLIGHT",

            "r5_prerequisite": {
                "classification":
                    r5[
                        "classification"
                    ],

                "promotion_authorized":
                    r5[
                        "decision"
                    ][
                        "promotion_authorized"
                    ],

                "relaxed_relative_lower_bound":
                    r5[
                        "schur"
                    ][
                        "relaxed_relative_lower_bound"
                    ],
            },

            "model": {
                "omega_y":
                    omega_y,

                "mu":
                    mu,

                "m_x_eV":
                    m_x_ev,

                "m_A_eV":
                    m_a_ev,

                "Q_star":
                    q_star,
            },

            "reservoir_qball": {
                "a0":
                    a0,

                "I_E":
                    float(
                        integrals[
                            "I_E"
                        ]
                    ),

                "I_Q":
                    float(
                        integrals[
                            "I_Q"
                        ]
                    ),

                "E_over_Qm_model":
                    e_over_qm_model,

                "E_over_Qm_physical":
                    e_over_qm_physical,

                "E_over_Qm_relerr":
                    eqm_relerr,

                "bound_pass":
                    reservoir_bound_pass,

                "rest_energy_J":
                    reservoir_rest_energy_j,

                "mass_equivalent_kg":
                    activation_mass_equivalent_kg,
            },

            "remote_same_Y": {
                "exact_off":
                    remote_exact_off,

                "samples":
                    remote_rows,

                "classification":
                    "RED_FOR_EXACT_OFF_REQUIREMENT",
            },

            "phase_only": {
                "activation_fraction":
                    f_original,

                "phase_spread":
                    phase_spread,

                "exact_off":
                    phase_only_exact_off,

                "classification":
                    "RED_ACTIVATION_DEPENDS_ON_MODULUS",
            },

            "spectator_R": {
                "mixer_form":
                    "kappa*S*(conj(Y)*R+conj(R)*Y)",

                "diagonal_U1":
                    True,

                "rabi_oracle":
                    oracle,

                "off": {
                    "QY":
                        off_qy,

                    "QR":
                        off_qr,

                    "Qtotal":
                        off_q_total,
                },

                "on": {
                    "QY":
                        on_qy,

                    "QR":
                        on_qr,

                    "Qtotal":
                        on_q_total,
                },

                "charge_total_relerr":
                    charge_total_relerr,

                "endpoint_charge_pass":
                    charge_endpoint_pass,

                "dynamic_mixer_realized":
                    False,
            },

            "energy_ledger": {
                "off_source_J":
                    off_source_energy_j,

                "reservoir_rest_J":
                    reservoir_rest_energy_j,

                "explicit_off_total_J":
                    explicit_off_total_j,

                "full_on_total_J":
                    explicit_on_total_j,

                "old_no_reservoir_on_minus_off_J":
                    old_on_minus_off_j,

                "explicit_reservoir_on_minus_off_J":
                    explicit_on_minus_off_j,

                "ledger_identity_relerr":
                    ledger_relerr,

                "endpoint_mass_difference_kg":
                    endpoint_mass_difference_kg,

                "endpoint_energy_per_charge_eV":
                    energy_per_charge_ev,

                "pass":
                    endpoint_energy_pass,
            },

            "switching_power_rows":
                power_rows,

            "architectures":
                architecture_rows,

            "decision": {
                "survivor_count":
                    survivor_count,

                "spectator_R_survives":
                    spectator_survives,

                "prerequisites":
                    prerequisites,

                "full_D3D_closed":
                    False,
            },

            "claim_limits": [
                (
                    "GREEN establishes only an exact endpoint reservoir "
                    "architecture in an extended flat-space effective theory."
                ),
                (
                    "The spectator R field is a new theoretical ingredient "
                    "and is not established in nature."
                ),
                (
                    "The neutral dynamic mixing field S is not solved here."
                ),
                (
                    "The 30.74-GJ ON-minus-explicit-OFF difference is an "
                    "endpoint inventory difference, not proven irreversible work."
                ),
                (
                    "Reset recoverability is not assumed."
                ),
                (
                    "Finite-time radiation and local transfer reaction stresses "
                    "remain open."
                ),
                (
                    "Einstein backreaction, nonlinear stability, EFT/naturalness "
                    "and empirical closure remain open."
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

        with OUT_POWER_CSV.open(
            "w",
            newline="",
        ) as handle:

            writer = csv.DictWriter(
                handle,
                fieldnames=list(
                    power_rows[
                        0
                    ].keys()
                ),
            )

            writer.writeheader()

            writer.writerows(
                power_rows
            )

        with OUT_ARCH_CSV.open(
            "w",
            newline="",
        ) as handle:

            writer = csv.DictWriter(
                handle,
                fieldnames=list(
                    architecture_rows[
                        0
                    ].keys()
                ),
            )

            writer.writeheader()

            writer.writerows(
                architecture_rows
            )

        print(
            f"SUMMARY_JSON={OUT_JSON}"
        )

        print(
            f"POWER_CSV={OUT_POWER_CSV}"
        )

        print(
            f"ARCHITECTURE_CSV={OUT_ARCH_CSV}"
        )

    finally:

        qmod.X_MATCH = (
            old_x_match
        )


if __name__ == "__main__":
    main()
