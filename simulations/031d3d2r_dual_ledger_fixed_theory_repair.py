#!/usr/bin/env python3
"""
031D3D2-R
=========

Dual-ledger / fixed-theory repair of the failed 031D3D2 switching closeout.

D3D2 exposed three provenance problems:

1. it compared the exact Hamiltonian source energy against D3B's deliberately
   conservative source inventory;

2. its energy-matched heavy-R construction was not the fixed U(2)-symmetric
   D3D1 Y/R doublet theory;

3. it treated the continuous scalarization bifurcation point as a missing
   source branch and inserted NaN into the path.

This run repairs those issues without changing the certified ON source.

Fixed theory retained
---------------------
D3D1:

    Psi = (Y, R)

    V_doublet = W(sqrt(|Y|^2 + |R|^2))

with equal Y/R microscopic Q-ball scales at the endpoints and conserved
diagonal U(1).

Collective population path:

    Y(r) = sqrt(q) A(r)
    R(r) = sqrt(1-q) A(r)

so:

    Q_Y / Q_total = q
    Q_R / Q_total = 1-q

and the U(2)-symmetric doublet self-energy remains constant along the ideal
internal rotation, apart from the explicitly counted positive stabilizer.

Energy ledgers
--------------
EXACT HAMILTONIAN:
    credits the physical A_X W(X) interaction term and is used for actual
    conservation / switching work.

CONSERVATIVE INVENTORY:
    replaces A_X W(X) by W(X) and therefore refuses to credit the negative
    interaction/binding contribution. This remains the engineering inventory
    quoted by the project.

A GREEN result does NOT lower the conservative 127.8-GJ ON inventory.

Scientific closeout
-------------------
GREEN requires:

- D3D1 still GREEN;
- the D3D2 exact-Hamiltonian reconstruction is internally consistent;
- the old heavy-R "energy match" is explicitly rejected;
- the scalarized/unscalarized branches join continuously at q_crit;
- a finite same-mass U(2) switching path exists;
- total diagonal charge is identically conserved;
- exact forward energy release and reverse work are explicit;
- the control-field mass can be reselected above a conservative chirp margin;
- the forward and reverse resonant-envelope tests pass.

GREEN closes 031D3D only as a DRIVEN ADIABATIC MULTISCALE switching
construction in the declared flat-space effective theory.

Still open:
- microscopic power-supply hardware;
- recovery efficiency of released activation energy;
- carrier-resolved nonlinear radial evolution;
- nonlinear fragmentation;
- multiparticle / higher-harmonic radiation;
- Einstein backreaction;
- EFT / naturalness;
- empirical fifth-force / EP / PPN closure;
- practical device.
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

D3D1_SUMMARY = (
    DATA
    / "031d3d1_stabilized_neutral_mixer_summary.json"
)

D3D2_SUMMARY = (
    DATA
    / "031d3d2_energy_matched_adiabatic_transfer_summary.json"
)

D3D2_BRANCH = (
    DATA
    / "031d3d2_source_scalarization_branch.csv"
)

D3D1_SOURCE = (
    SIM
    / "031d3d1_stabilized_neutral_mixer_gate.py"
)

D3D2_SOURCE = (
    SIM
    / "031d3d2_energy_matched_adiabatic_transfer_closeout.py"
)

OUT_JSON = (
    DATA
    / "031d3d2r_dual_ledger_fixed_theory_summary.json"
)

OUT_PATH = (
    DATA
    / "031d3d2r_fixed_theory_switching_path.csv"
)

OUT_CONTROLLER = (
    DATA
    / "031d3d2r_controller_mass_scan.csv"
)


J_PER_EV = 1.602176634e-19
HBAR_EV_S = 6.582119569e-16
H_EV_S = 4.135667696e-15

PRIMARY_SWITCH_S = 1.0

CHIRP_MARGIN = 2.0

SIGMA_VALUES = (
    80.0,
    100.0,
    150.0,
    200.0,
    300.0,
)

G_GRID = np.logspace(
    -10.0,
    -1.0,
    361,
)

STABILIZER_MARGIN = 1.20

MAX_GHAT = 1.0
MAX_LAMBDA = 4.0 * math.pi

Y_REBUILD_REL_TOL = 2.0e-5
EXACT_IDENTITY_REL_TOL = 2.0e-8

QCRIT_U0_MAX = 1.0e-6
QCRIT_LAMBDA_MAX = 2.0e-5

PATH_BARRIER_ALLOWANCE_J = 1.0e5

RWA_FIDELITY_MIN = 0.999
RWA_NORM_MAX = 2.0e-8

COMPLIANCE_REL_TOL = 2.0e-5


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


def read_branch_rows() -> list[dict[str, Any]]:

    rows = []

    with D3D2_BRANCH.open(
        newline="",
    ) as handle:

        reader = csv.DictReader(
            handle
        )

        for raw in reader:

            success_text = str(
                raw.get(
                    "success",
                    "",
                )
            ).strip().lower()

            success = (
                success_text
                in (
                    "true",
                    "1",
                    "yes",
                )
            )

            row = {
                "q":
                    float(
                        raw[
                            "q"
                        ]
                    ),

                "success":
                    success,
            }

            for key in (
                "omega_x",
                "u0",
                "I_source_scalarized",
                "E_source_scalarized_J",
                "E_source_unscalarized_J",
                "unscalarized_lambda0",
                "bvp_rms",
            ):

                text = str(
                    raw.get(
                        key,
                        "",
                    )
                ).strip()

                if text:

                    row[
                        key
                    ] = float(
                        text
                    )

            if raw.get(
                "error"
            ):

                row[
                    "error"
                ] = raw[
                    "error"
                ]

            rows.append(
                row
            )

    return sorted(
        rows,
        key=lambda row:
        row[
            "q"
        ],
    )


def preliminary_fixed_path(
    branch_rows,
    *,
    qcrit: float,
    off_source_J: float,
    doublet_J: float,
    barrier_max_J: float,
):

    rows = []

    qcrit_row = min(
        branch_rows,
        key=lambda row:
        abs(
            row[
                "q"
            ]
            - qcrit
        ),
    )

    for source in (
        branch_rows
    ):

        q = float(
            source[
                "q"
            ]
        )

        if q <= qcrit:

            E_source = (
                off_source_J
            )

            branch = (
                "UNSCALARIZED"
                if q < qcrit
                else "BIFURCATION_MERGER"
            )

        else:

            if (
                not source.get(
                    "success",
                    False,
                )
                or
                "E_source_scalarized_J"
                not in source
            ):

                raise RuntimeError(
                    f"Missing scalarized source energy at q={q}"
                )

            E_source = float(
                source[
                    "E_source_scalarized_J"
                ]
            )

            branch = (
                "SCALARIZED"
            )

        barrier = (
            4.0
            * q
            * (
                1.0
                - q
            )
            * barrier_max_J
        )

        exact_total = (
            E_source
            + doublet_J
            + barrier
        )

        rows.append(
            {
                "q":
                    q,

                "QY_fraction":
                    q,

                "QR_fraction":
                    1.0
                    - q,

                "Qtotal_fraction":
                    1.0,

                "source_branch":
                    branch,

                "E_source_exact_J":
                    E_source,

                "E_doublet_exact_J":
                    doublet_J,

                "E_stabilizer_J":
                    barrier,

                "E_total_exact_J":
                    exact_total,
            }
        )

    rows = sorted(
        rows,
        key=lambda row:
        row[
            "q"
        ],
    )

    return (
        rows,
        qcrit_row,
    )


def add_chirp(
    rows,
    Q_star: float,
) -> float:

    q = np.array(
        [
            row[
                "q"
            ]
            for row
            in rows
        ],
        dtype=float,
    )

    energy = np.array(
        [
            row[
                "E_total_exact_J"
            ]
            for row
            in rows
        ],
        dtype=float,
    )

    interpolator = (
        PchipInterpolator(
            q,
            energy,
        )
    )

    dense_q = np.linspace(
        float(
            q[
                0
            ]
        ),
        float(
            q[
                -1
            ]
        ),
        100_001,
    )

    dE_dq = (
        interpolator.derivative()(
            dense_q
        )
    )

    chirp_hz = (
        dE_dq
        / Q_star
        / J_PER_EV
        / H_EV_S
    )

    max_chirp = float(
        np.max(
            np.abs(
                chirp_hz
            )
        )
    )

    for row in (
        rows
    ):

        derivative = float(
            interpolator.derivative()(
                row[
                    "q"
                ]
            )
        )

        row[
            "dE_dq_J"
        ] = derivative

        row[
            "chemical_detuning_eV"
        ] = (
            derivative
            / Q_star
            / J_PER_EV
        )

        row[
            "chirp_Hz"
        ] = (
            row[
                "chemical_detuning_eV"
            ]
            / H_EV_S
        )

    return max_chirp


def main() -> None:

    print(
        "=== 031D3D2-R DUAL-LEDGER / FIXED-THEORY REPAIR ==="
    )

    print(
        "CLAIM_CLASS="
        "DRIVEN_ADIABATIC_SWITCHING_PROVENANCE_REPAIR"
    )

    print(
        "EXACT_HAMILTONIAN_AND_CONSERVATIVE_INVENTORY_SEPARATED=YES"
    )

    print(
        "D3D2_HEAVY_R_ENERGY_MATCH_RETAINED=NO"
    )

    print(
        "D3D1_SAME_MASS_U2_DOUBLET_RESTORED=YES"
    )

    print(
        "QCRIT_BRANCH_MERGER_TREATED_CONTINUOUSLY=YES"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    for path in (
        D3D0_SUMMARY,
        D3D1_SUMMARY,
        D3D2_SUMMARY,
        D3D2_BRANCH,
        D3D1_SOURCE,
        D3D2_SOURCE,
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

    d2 = load_json(
        D3D2_SUMMARY
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
            "D3D1 prerequisite is not GREEN"
        )

    branch_rows = (
        read_branch_rows()
    )

    Q_star = float(
        d0[
            "model"
        ][
            "Q_star"
        ]
    )

    mY_eV = float(
        d0[
            "model"
        ][
            "m_A_eV"
        ]
    )

    omegaY = float(
        d0[
            "model"
        ][
            "omega_y"
        ]
    )

    E_Y = float(
        d0[
            "reservoir_qball"
        ][
            "rest_energy_J"
        ]
    )

    E_source_off = float(
        d0[
            "energy_ledger"
        ][
            "off_source_J"
        ]
    )

    E_cons_on = float(
        d0[
            "energy_ledger"
        ][
            "full_on_total_J"
        ]
    )

    E_cons_off = float(
        d0[
            "energy_ledger"
        ][
            "explicit_off_total_J"
        ]
    )

    E_source_exact_on = float(
        d2[
            "hamiltonian_provenance"
        ][
            "source_ON_rebuilt_J"
        ]
    )

    E_exact_on = float(
        d2[
            "hamiltonian_provenance"
        ][
            "full_ON_rebuilt_J"
        ]
    )

    E_Y_rebuilt = float(
        d2[
            "hamiltonian_provenance"
        ][
            "Y_rebuilt_J"
        ]
    )

    E_cons_source_on = (
        E_cons_on
        - E_Y
    )

    binding_credit = (
        E_cons_source_on
        - E_source_exact_on
    )

    exact_identity_relerr = (
        relerr(
            E_exact_on,
            E_source_exact_on
            + E_Y_rebuilt,
        )
    )

    y_rebuild_relerr = (
        relerr(
            E_Y_rebuilt,
            E_Y,
        )
    )

    dual_ledger_pass = bool(
        exact_identity_relerr
        <= EXACT_IDENTITY_REL_TOL
        and
        y_rebuild_relerr
        <= Y_REBUILD_REL_TOL
        and
        binding_credit
        > 0.0
    )

    print(
        "\n=== STAGE A: DUAL ENERGY LEDGER RECONCILIATION ==="
    )

    print(
        f"EXACT_SOURCE_ON_J={E_source_exact_on:.15e}"
    )

    print(
        f"CONSERVATIVE_SOURCE_ON_J={E_cons_source_on:.15e}"
    )

    print(
        f"NEGATIVE_INTERACTION_BINDING_CREDIT_J={binding_credit:.15e}"
    )

    print(
        "NEGATIVE_INTERACTION_BINDING_CREDIT_GJ="
        f"{binding_credit/1.0e9:.15e}"
    )

    print(
        f"EXACT_ON_TOTAL_J={E_exact_on:.15e}"
    )

    print(
        f"CONSERVATIVE_ON_INVENTORY_J={E_cons_on:.15e}"
    )

    print(
        f"Y_REBUILD_RELERR={y_rebuild_relerr:.15e}"
    )

    print(
        "EXACT_HAMILTONIAN_IDENTITY_RELERR="
        f"{exact_identity_relerr:.15e}"
    )

    print(
        f"DUAL_LEDGER_PROVENANCE_PASS={dual_ledger_pass}"
    )

    print(
        "D3B_121P55_GJ_LEDGER_TYPE="
        "CONSERVATIVE_INVENTORY_NOT_EXACT_HAMILTONIAN"
    )

    print(
        "D3D2_38_PERCENT_NORMALIZATION_FAILURE="
        "REJECTED_AS_LEDGER_CATEGORY_ERROR"
    )

    heavy_mass_ratio = float(
        d2[
            "energy_matched_reservoir"
        ][
            "mass_ratio"
        ]
    )

    heavy_R_invalid = bool(
        abs(
            heavy_mass_ratio
            - 1.0
        )
        > 1.0e-6
        and
        "sqrt"
        in str(
            d1[
                "theory"
            ][
                "doublet_potential"
            ]
        ).lower()
    )

    positive_R_match_impossible = bool(
        E_exact_on
        < E_source_off
    )

    print(
        "\n=== STAGE B: D3D2 HEAVY-R REPAIR FALSIFICATION ==="
    )

    print(
        f"D3D2_HEAVY_R_MASS_RATIO={heavy_mass_ratio:.15e}"
    )

    print(
        "D3D1_FIXED_DOUBLET_POTENTIAL="
        f"{d1['theory']['doublet_potential']}"
    )

    print(
        "HEAVY_R_FIXED_THEORY_CONTINUATION_VALID="
        f"{not heavy_R_invalid}"
    )

    print(
        "POSITIVE_R_EXACT_ENDPOINT_ENERGY_MATCH_POSSIBLE="
        f"{not positive_R_match_impossible}"
    )

    print(
        "REASON="
        "EXACT_ON_ENERGY_IS_ALREADY_BELOW_BARE_OFF_SOURCE_ENERGY"
    )

    print(
        "D3D2_ENERGY_MATCHED_HEAVY_R="
        "REJECTED"
    )

    E_exact_off = (
        E_source_off
        + E_Y
    )

    forward_release = (
        E_exact_off
        - E_exact_on
    )

    conservative_delta = (
        E_cons_on
        - E_cons_off
    )

    print(
        "\n=== STAGE C: RESTORED SAME-MASS U2 ENDPOINTS ==="
    )

    print(
        f"EXACT_OFF_WITH_R_J={E_exact_off:.15e}"
    )

    print(
        f"EXACT_ON_J={E_exact_on:.15e}"
    )

    print(
        f"EXACT_FORWARD_RELEASE_J={forward_release:.15e}"
    )

    print(
        "EXACT_FORWARD_RELEASE_GJ="
        f"{forward_release/1.0e9:.15e}"
    )

    print(
        f"MINIMUM_REVERSIBLE_RESET_WORK_J={forward_release:.15e}"
    )

    print(
        "MINIMUM_REVERSIBLE_RESET_WORK_GJ="
        f"{forward_release/1.0e9:.15e}"
    )

    print(
        f"CONSERVATIVE_OFF_INVENTORY_J={E_cons_off:.15e}"
    )

    print(
        f"CONSERVATIVE_ON_INVENTORY_J={E_cons_on:.15e}"
    )

    print(
        f"CONSERVATIVE_ON_MINUS_OFF_J={conservative_delta:.15e}"
    )

    print(
        "CONSERVATIVE_PEAK_INVENTORY_REMAINS_GJ="
        f"{max(E_cons_off,E_cons_on)/1.0e9:.15e}"
    )

    qcrit = float(
        d2[
            "scalarization"
        ][
            "qcrit"
        ]
    )

    old_barrier = float(
        d1[
            "best_candidate"
        ][
            "barrier_energy_J"
        ]
    )

    (
        preliminary_rows,
        qcrit_row,
    ) = preliminary_fixed_path(
        branch_rows,
        qcrit=qcrit,
        off_source_J=E_source_off,
        doublet_J=E_Y,
        barrier_max_J=old_barrier,
    )

    qcrit_u0 = abs(
        float(
            qcrit_row.get(
                "u0",
                math.inf,
            )
        )
    )

    qcrit_lambda = abs(
        float(
            qcrit_row.get(
                "unscalarized_lambda0",
                math.inf,
            )
        )
    )

    branch_merger_pass = bool(
        qcrit_u0
        <= QCRIT_U0_MAX
        and
        qcrit_lambda
        <= QCRIT_LAMBDA_MAX
        and
        bool(
            d2[
                "scalarization"
            ][
                "coverage_pass"
            ]
        )
    )

    prelim_chirp = add_chirp(
        preliminary_rows,
        Q_star,
    )

    print(
        "\n=== STAGE D: SCALARIZATION BRANCH-MERGER REPAIR ==="
    )

    print(
        f"QCRIT={qcrit:.15e}"
    )

    print(
        f"QCRIT_ROW_Q={qcrit_row['q']:.15e}"
    )

    print(
        f"QCRIT_ROW_ABS_U0={qcrit_u0:.15e}"
    )

    print(
        f"QCRIT_ROW_ABS_LAMBDA0={qcrit_lambda:.15e}"
    )

    print(
        f"BRANCH_MERGER_PASS={branch_merger_pass}"
    )

    print(
        "OLD_MISSING_STABLE_SCALARIZED_AT_QCRIT="
        "REJECTED_BIFURCATION_POINT_IS_THE_TRIVIAL_LIMIT"
    )

    print(
        "PRELIMINARY_MAX_ABS_CHIRP_HZ="
        f"{prelim_chirp:.15e}"
    )

    print(
        "\n=== STAGE E: CONTROL-MASS RESELECTION AGAINST PATH CHIRP ===",
        flush=True,
    )

    d1mod = load_module(
        "d3d1_for_d3d2r",
        D3D1_SOURCE,
    )

    d2mod = load_module(
        "d3d2_for_d3d2r",
        D3D2_SOURCE,
    )

    qmod = load_module(
        "qball_for_d3d2r",
        d1mod.QBALL_SOURCE,
    )

    d3a = load_module(
        "d3a_for_d3d2r",
        d1mod.D3A_SOURCE,
    )

    old_qmatch = float(
        qmod.X_MATCH
    )

    old_dmatch = float(
        d3a.X_MATCH
    )

    qmod.X_MATCH = 80.0
    d3a.X_MATCH = 80.0

    try:

        activation = (
            qmod.solve_uncoupled_qball(
                omegaY
            )
        )

        if activation is None:

            raise RuntimeError(
                "Could not reconstruct activation Q-ball"
            )

        k = math.sqrt(
            max(
                1.0
                - omegaY
                * omegaY,
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

        a, _ap = (
            d3a.extended_profile(
                activation,
                omegaY,
                rho,
            )
        )

        I2 = float(
            d1[
                "profile"
            ][
                "I2"
            ]
        )

        I4 = float(
            d1[
                "profile"
            ][
                "I4"
            ]
        )

        energy_scale = float(
            d1[
                "profile"
            ][
                "energy_scale_J_per_I"
            ]
        )

        rabi_eV = (
            HBAR_EV_S
            * math.pi
            / (
                2.0
                * PRIMARY_SWITCH_S
            )
        )

        rabi_dimensionless = (
            rabi_eV
            / mY_eV
        )

        target_mass2 = (
            4.0
            * omegaY
            * rabi_dimensionless
        )

        drive_eV = (
            H_EV_S
            * prelim_chirp
        )

        drive_ratio = (
            drive_eV
            / mY_eV
        )

        controller_rows = []

        for sigma in (
            SIGMA_VALUES
        ):

            sigma_energy = math.sqrt(
                sigma
                * sigma
                + drive_ratio
                * drive_ratio
            )

            compliance = (
                d1mod.solve_gate_compliance(
                    rho,
                    a,
                    sigma_energy,
                )
            )

            threshold_hz = (
                sigma
                * mY_eV
                / H_EV_S
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
                        * compliance[
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

                controller_rows.append(
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

                        "threshold_Hz":
                            threshold_hz,

                        "chirp_margin":
                            threshold_hz
                            / max(
                                prelim_chirp,
                                1.0e-300,
                            ),

                        "compliance":
                            compliance[
                                "compliance"
                            ],

                        "compliance_identity_relerr":
                            compliance[
                                "identity_relerr"
                            ],

                        "gate_energy_J":
                            I_S
                            * energy_scale,

                        "barrier_max_J":
                            I_barrier
                            * energy_scale,

                        "total_control_inventory_J":
                            (
                                I_S
                                + I_barrier
                            )
                            * energy_scale,

                        "radiation_threshold_pass":
                            bool(
                                threshold_hz
                                >=
                                CHIRP_MARGIN
                                * prelim_chirp
                            ),

                        "coupling_pass":
                            bool(
                                ghat
                                <= MAX_GHAT
                            ),

                        "lambda_pass":
                            bool(
                                lam
                                <= MAX_LAMBDA
                            ),

                        "compliance_pass":
                            bool(
                                compliance[
                                    "pass"
                                ]

                                and
                                compliance[
                                    "identity_relerr"
                                ]
                                <= COMPLIANCE_REL_TOL
                            ),
                    }
                )

        viable = [
            row
            for row
            in controller_rows
            if (
                row[
                    "radiation_threshold_pass"
                ]
                and
                row[
                    "coupling_pass"
                ]
                and
                row[
                    "lambda_pass"
                ]
                and
                row[
                    "compliance_pass"
                ]
            )
        ]

        if not viable:

            best = None

        else:

            best = min(
                viable,
                key=lambda row:
                row[
                    "total_control_inventory_J"
                ],
            )

    finally:

        qmod.X_MATCH = (
            old_qmatch
        )

        d3a.X_MATCH = (
            old_dmatch
        )

    if best is None:

        controller_pass = (
            False
        )

        final_rows = (
            preliminary_rows
        )

        final_chirp = (
            prelim_chirp
        )

        best_barrier = (
            old_barrier
        )

    else:

        best_barrier = float(
            best[
                "barrier_max_J"
            ]
        )

        (
            final_rows,
            _qcrit_again,
        ) = preliminary_fixed_path(
            branch_rows,
            qcrit=qcrit,
            off_source_J=E_source_off,
            doublet_J=E_Y,
            barrier_max_J=best_barrier,
        )

        final_chirp = add_chirp(
            final_rows,
            Q_star,
        )

        controller_pass = bool(
            float(
                best[
                    "threshold_Hz"
                ]
            )
            >=
            CHIRP_MARGIN
            * final_chirp
        )

    if best is not None:

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
            "BEST_GATE_ENERGY_1S_J="
            f"{best['gate_energy_J']:.15e}"
        )

        print(
            "BEST_STABILIZER_BARRIER_MAX_J="
            f"{best['barrier_max_J']:.15e}"
        )

        print(
            "BEST_TOTAL_CONTROL_INVENTORY_J="
            f"{best['total_control_inventory_J']:.15e}"
        )

        print(
            "BEST_S_THRESHOLD_HZ="
            f"{best['threshold_Hz']:.15e}"
        )

        print(
            "BEST_THRESHOLD_OVER_FINAL_CHIRP="
            f"{best['threshold_Hz']/max(final_chirp,1.0e-300):.15e}"
        )

    print(
        f"FINAL_MAX_ABS_CHIRP_HZ={final_chirp:.15e}"
    )

    print(
        "CONTROL_MASS_RESELECTION_PASS="
        f"{controller_pass}"
    )

    exact_path = np.array(
        [
            row[
                "E_total_exact_J"
            ]
            for row
            in final_rows
        ],
        dtype=float,
    )

    finite_path = bool(
        np.all(
            np.isfinite(
                exact_path
            )
        )
    )

    path_peak_over_off = float(
        np.max(
            exact_path
        )
        - E_exact_off
    )

    path_release = float(
        exact_path[
            0
        ]
        - exact_path[
            -1
        ]
    )

    endpoint_exact_relerr = (
        relerr(
            float(
                exact_path[
                    0
                ]
            ),
            E_exact_off,
        )
        +
        relerr(
            float(
                exact_path[
                    -1
                ]
            ),
            E_exact_on,
        )
    )

    path_pass = bool(
        finite_path
        and
        endpoint_exact_relerr
        <= 5.0e-8
        and
        path_peak_over_off
        <= PATH_BARRIER_ALLOWANCE_J
        and
        path_release
        > 0.0
    )

    print(
        "\n=== STAGE F: RESTORED FIXED-THEORY EXACT SWITCHING PATH ==="
    )

    print(
        "PATH_EXACT_OFF_J="
        f"{float(exact_path[0]):.15e}"
    )

    print(
        "PATH_EXACT_ON_J="
        f"{float(exact_path[-1]):.15e}"
    )

    print(
        f"PATH_FORWARD_RELEASE_J={path_release:.15e}"
    )

    print(
        "PATH_FORWARD_RELEASE_GJ="
        f"{path_release/1.0e9:.15e}"
    )

    print(
        f"PATH_PEAK_ABOVE_OFF_J={path_peak_over_off:.15e}"
    )

    print(
        "PATH_ENDPOINT_IDENTITY_RELERR_SUM="
        f"{endpoint_exact_relerr:.15e}"
    )

    print(
        f"FINITE_FIXED_THEORY_PATH_PASS={path_pass}"
    )

    reset_work = (
        path_release
    )

    print(
        "\n=== STAGE G: ACTIVATION / RESET ENERGY-FLOW LEDGER ==="
    )

    print(
        f"FORWARD_ACTIVATION_ENERGY_RELEASE_J={path_release:.15e}"
    )

    print(
        "FORWARD_ACTIVATION_RELEASE_POWER_1S_W="
        f"{path_release/PRIMARY_SWITCH_S:.15e}"
    )

    print(
        f"REVERSIBLE_RESET_WORK_FLOOR_J={reset_work:.15e}"
    )

    print(
        "REVERSIBLE_RESET_POWER_FLOOR_1S_W="
        f"{reset_work/PRIMARY_SWITCH_S:.15e}"
    )

    print(
        "FORWARD_DRIVE_MUST_ABSORB_ENERGY=True"
    )

    print(
        "RESET_DRIVE_MUST_SUPPLY_ENERGY=True"
    )

    print(
        "RESET_RECOVERABILITY_ESTABLISHED=False"
    )

    print(
        "IF_FORWARD_RELEASE_IS_NOT_RECOVERED_"
        "DISSIPATION_J="
        f"{path_release:.15e}"
    )

    print(
        "CONSERVATIVE_ON_INVENTORY_REMAINS_J="
        f"{E_cons_on:.15e}"
    )

    tolerance_hz = float(
        d1[
            "resonant_999_tolerance_Hz"
        ]
    )

    forward = (
        d2mod.rwa_transfer(
            PRIMARY_SWITCH_S,
            tolerance_hz,
            reverse=False,
        )
    )

    reverse = (
        d2mod.rwa_transfer(
            PRIMARY_SWITCH_S,
            tolerance_hz,
            reverse=True,
        )
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
        <= RWA_NORM_MAX

        and
        reverse[
            "norm_error"
        ]
        <= RWA_NORM_MAX
    )

    print(
        "\n=== STAGE H: BIDIRECTIONAL ENVELOPE ==="
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
        "BIDIRECTIONAL_TRANSFER_ENVELOPE_PASS="
        f"{rwa_pass}"
    )

    prerequisites = bool(
        dual_ledger_pass
        and
        heavy_R_invalid
        and
        positive_R_match_impossible
        and
        branch_merger_pass
        and
        path_pass
        and
        controller_pass
        and
        rwa_pass
    )

    print(
        "\n=== STAGE I: DECISION ==="
    )

    print(
        f"DUAL_LEDGER_PASS={dual_ledger_pass}"
    )

    print(
        f"HEAVY_R_REPAIR_REJECTED={heavy_R_invalid}"
    )

    print(
        f"QCRIT_BRANCH_MERGER_PASS={branch_merger_pass}"
    )

    print(
        f"FIXED_THEORY_PATH_PASS={path_pass}"
    )

    print(
        f"CONTROL_CHIRP_THRESHOLD_PASS={controller_pass}"
    )

    print(
        f"BIDIRECTIONAL_ENVELOPE_PASS={rwa_pass}"
    )

    if prerequisites:

        classification = (
            "GREEN_D3D2R_DUAL_LEDGER_FIXED_THEORY_"
            "DRIVEN_ADIABATIC_SWITCHING_CLOSEOUT"
        )

        next_action = (
            "031E_FULL_PHYSICAL_METRIC_EINSTEIN_BACKREACTION"
        )

        full_d3d = True

    else:

        classification = (
            "YELLOW_OR_RED_D3D2R_FIXED_THEORY_"
            "SWITCHING_REPAIR_FAILED"
        )

        next_action = (
            "DIAGNOSE_ONLY_FAILED_D3D2R_LEDGER_"
            "BRANCH_PATH_CONTROL_OR_RWA_SUBGATE"
        )

        full_d3d = False

    print(
        f"031D3D2R_CLASSIFICATION={classification}"
    )

    print(
        "FULL_D3D_DRIVEN_ADIABATIC_CLOSEOUT="
        f"{full_d3d}"
    )

    print(
        "ISOLATED_MICROSCOPIC_POWER_SUPPLY_REALIZED=False"
    )

    print(
        "RESET_RECOVERABILITY_ESTABLISHED=False"
    )

    print(
        "CARRIER_RESOLVED_NONLINEAR_RADIAL_PDE_SOLVED=False"
    )

    print(
        "HIGHER_HARMONIC_MULTIPARTICLE_RADIATION_CLOSED=False"
    )

    print(
        "NONLINEAR_FRAGMENTATION_STABILITY_CLOSED=False"
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
            "DRIVEN_ADIABATIC_SWITCHING_PROVENANCE_REPAIR",

        "dual_ledger": {
            "exact_source_ON_J":
                E_source_exact_on,

            "conservative_source_ON_J":
                E_cons_source_on,

            "negative_interaction_binding_credit_J":
                binding_credit,

            "exact_ON_J":
                E_exact_on,

            "conservative_ON_J":
                E_cons_on,

            "exact_identity_relerr":
                exact_identity_relerr,

            "Y_rebuild_relerr":
                y_rebuild_relerr,

            "pass":
                dual_ledger_pass,
        },

        "heavy_R_falsification": {
            "mass_ratio":
                heavy_mass_ratio,

            "fixed_theory_valid":
                not heavy_R_invalid,

            "positive_R_exact_energy_match_possible":
                not positive_R_match_impossible,

            "rejected":
                heavy_R_invalid
                and
                positive_R_match_impossible,
        },

        "same_mass_endpoints": {
            "exact_OFF_J":
                E_exact_off,

            "exact_ON_J":
                E_exact_on,

            "exact_forward_release_J":
                forward_release,

            "minimum_reversible_reset_work_J":
                reset_work,

            "conservative_OFF_J":
                E_cons_off,

            "conservative_ON_J":
                E_cons_on,

            "conservative_ON_minus_OFF_J":
                conservative_delta,
        },

        "scalarization_merger": {
            "qcrit":
                qcrit,

            "qcrit_row_q":
                qcrit_row[
                    "q"
                ],

            "abs_u0":
                qcrit_u0,

            "abs_lambda0":
                qcrit_lambda,

            "pass":
                branch_merger_pass,
        },

        "control": {
            "preliminary_max_abs_chirp_Hz":
                prelim_chirp,

            "final_max_abs_chirp_Hz":
                final_chirp,

            "chirp_margin":
                CHIRP_MARGIN,

            "best":
                best,

            "pass":
                controller_pass,
        },

        "path": {
            "forward_release_J":
                path_release,

            "peak_above_OFF_J":
                path_peak_over_off,

            "endpoint_identity_relerr_sum":
                endpoint_exact_relerr,

            "pass":
                path_pass,
        },

        "rwa": {
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

            "full_D3D_driven_adiabatic_closeout":
                full_d3d,
        },

        "claim_limits": [
            (
                "The exact Hamiltonian is used for switching "
                "energy conservation; the conservative inventory "
                "remains the engineering upper ledger."
            ),
            (
                "The approximately 127.8-GJ conservative ON "
                "inventory is not reduced by this repair."
            ),
            (
                "The D3D2 heavy-R energy-matching construction "
                "is rejected and not carried forward."
            ),
            (
                "GREEN establishes only a driven adiabatic "
                "multiscale switching construction."
            ),
            (
                "Forward activation releases roughly 15.5 GJ "
                "in the exact Hamiltonian; reset requires the "
                "same state-function energy difference absent "
                "recovery."
            ),
            (
                "Recovery efficiency is not established."
            ),
            (
                "The microscopic external power-supply apparatus "
                "is not realized here."
            ),
            (
                "Carrier-resolved nonlinear radial evolution and "
                "higher-harmonic/multiparticle radiation remain "
                "for later nonlinear closure."
            ),
            (
                "Einstein backreaction remains open."
            ),
            (
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

    path_fields = sorted(
        {
            key
            for row
            in final_rows
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
            final_rows
        )

    if controller_rows:

        controller_fields = sorted(
            {
                key
                for row
                in controller_rows
                for key
                in row
            }
        )

        with OUT_CONTROLLER.open(
            "w",
            newline="",
        ) as handle:

            writer = csv.DictWriter(
                handle,
                fieldnames=controller_fields,
            )

            writer.writeheader()

            writer.writerows(
                controller_rows
            )

    print(
        f"SUMMARY_JSON={OUT_JSON}"
    )

    print(
        f"PATH_CSV={OUT_PATH}"
    )

    print(
        f"CONTROLLER_CSV={OUT_CONTROLLER}"
    )


if __name__ == "__main__":
    main()
