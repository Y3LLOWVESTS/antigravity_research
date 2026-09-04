"""
031D3A-R2
=========

Correct the source-coupling versus ordinary-matter physical-metric
normalization before the full D3B coupled solve.

Established 031 microscopic source theory
-----------------------------------------

The exotic X Q-ball scalarizes through

    A_X(u) = exp(-u^2/2)

with

    u = phi/M_c.

Ordinary neutral matter instead follows

    A_m(phi) = exp(+phi^2/(2 M_m^2)).

The positive exponent is essential:

    a_phi = -c^2 grad ln A_m

and a localized phi profile with d(phi^2)/dr < 0 therefore produces
outward radial acceleration.

Correct D3 activation
---------------------

Use one activation fraction

    f(a) = 1 - exp(-a^2/2).

Then the coherent activated theory is

    A_X(u,a)
      = exp[- f(a) u^2 / 2]

for the exotic source sector, while ordinary neutral matter follows

    A_m(phi,a)
      = exp[+ f(a) phi^2/(2 M_m^2)].

OFF:
    a=0
    f=0
    A_X=1
    A_m=1

so:
- the exotic source no longer scalarizes;
- ordinary matter has no scalar metric coupling;
- phi=0 has positive bare scalar mass;
- there is no quadratic phi-a mixing.

ON:
    a >> 1
    f -> 1

so both inherited couplings are recovered.

Scientific repair
-----------------

031D3A-R correctly used M_c for the SOURCE reaction and for the source
activation operator scale.

But its payload-reaction diagnostic also used u=phi/M_c.

That is conservative but is not the established ordinary-matter metric.
Payload reaction must instead use M_m.

This run:

1. reconstructs the promoted source;
2. reconstructs M_m from the actual operating alpha_m;
3. uses the correct positive physical metric;
4. recomputes the whole radial interval occupied by the finite payload;
5. recomputes the activation-field reaction caused by a 1-kg payload;
6. separately reports source-activation and matter-metric EFT scales;
7. preserves the D3A-R 10-GeV source-operator floor and energy ledger.

This does NOT solve the coupled X + phi + Y equations.
"""

from __future__ import annotations

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

D3A_SOURCE = (
    SIM / "031d3a_u1_metric_activation_capacity.py"
)

ROBUST_SUMMARY = (
    DATA / "031c96_operating_margin_robustness_summary.json"
)

D1_LOW_SUMMARY = (
    DATA / "031d1r2_lowbranch_offstate_hessian_summary.json"
)

D3AR_SUMMARY = (
    DATA / "031d3ar_metric_eft_payload_summary.json"
)

OUT_JSON = (
    DATA / "031d3ar2_physical_metric_summary.json"
)


X_MATCH = 80.0

MPL_REDUCED_GEV = 2.435e18

PAYLOAD_MASS_KG = 1.0

PAYLOAD_SAMPLE_N = 5001

MIN_F = 0.999

MAX_METRIC_GRADIENT_RELERR = 5.0e-3

MAX_PAYLOAD_REACTION_RATIO = 0.10

MIN_SOURCE_OPERATOR_CUTOFF_GEV = 10.0

HBARC_EV_M = 1.973269804e-7
J_PER_EV = 1.602176634e-19
C_LIGHT = 299_792_458.0


def require(path: Path):
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


def main():
    print(
        "=== 031D3A-R2 CORRECT PHYSICAL-METRIC NORMALIZATION ==="
    )

    print(
        "SOURCE_COUPLING="
        "A_X=EXP[-F_ACTIVATION*U^2/2]"
    )

    print(
        "ORDINARY_MATTER_METRIC="
        "A_M=EXP[+F_ACTIVATION*PHI^2/(2*M_M^2)]"
    )

    print(
        "SOURCE_AND_MATTER_COUPLINGS_DISTINGUISHED=YES"
    )

    print(
        "D3AR_10GEV_SOURCE_OPERATOR_FLOOR_PRESERVED=YES"
    )

    print(
        "FULL_X_PHI_Y_COUPLED_SOLVE=NO"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    for path in (
        QBALL_SOURCE,
        D3A_SOURCE,
        ROBUST_SUMMARY,
        D1_LOW_SUMMARY,
        D3AR_SUMMARY,
    ):
        require(path)

    robust = json.loads(
        ROBUST_SUMMARY.read_text()
    )

    low = json.loads(
        D1_LOW_SUMMARY.read_text()
    )

    d3ar = json.loads(
        D3AR_SUMMARY.read_text()
    )

    if not str(
        d3ar.get(
            "classification",
            "",
        )
    ).startswith(
        "GREEN_D3AR"
    ):
        raise RuntimeError(
            "031D3A-R is not GREEN"
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
        if row["label"] == "nominal"
    )

    omega_x = float(
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
        1.0e9
        * m_x_gev
    )

    F_gev = float(
        quadrature[
            "F_gev"
        ]
    )

    M_c_gev = (
        F_gev
        / chi
    )

    M_c_ev = (
        1.0e9
        * M_c_gev
    )

    alpha_m = float(
        operating[
            "alpha_m"
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

    center_from_source_m = abs(
        payload_center_m
        - source_shift_m
    )

    near_m = (
        center_from_source_m
        - payload_radius_m
    )

    far_m = (
        center_from_source_m
        + payload_radius_m
    )

    x_length_m = (
        HBARC_EV_M
        / m_x_ev
    )

    x_near = (
        near_m
        / x_length_m
    )

    x_far = (
        far_m
        / x_length_m
    )

    qmod = load_module(
        "qball031d3ar2",
        QBALL_SOURCE,
    )

    d3a = load_module(
        "d3a031d3ar2",
        D3A_SOURCE,
    )

    old_xmatch = float(
        qmod.X_MATCH
    )

    qmod.X_MATCH = X_MATCH

    try:
        print(
            "\n=== STAGE A: RECONSTRUCT PROMOTED SOURCE ==="
        )

        seed = qmod.solve_uncoupled_qball(
            omega_x
        )

        if seed is None:
            raise RuntimeError(
                "Failed source Q-ball seed"
            )

        source = qmod.solve_coupled(
            seed,
            omega_x,
            epsilon,
            chi,
            previous=None,
        )

        if source is None:
            raise RuntimeError(
                "Failed promoted source reconstruction"
            )

        near_state = source.sol(
            x_near
        )

        u_near = abs(
            float(
                near_state[
                    2
                ]
            )
        )

        phi_near_gev = (
            M_c_gev
            * u_near
        )

        if (
            phi_near_gev <= 0.0
            or alpha_m <= 0.0
        ):
            raise RuntimeError(
                "Invalid near-payload scalar/matter sensitivity"
            )

        M_m_gev = math.sqrt(
            MPL_REDUCED_GEV
            * phi_near_gev
            / alpha_m
        )

        M_m_ev = (
            1.0e9
            * M_m_gev
        )

        print(
            f"ALPHA_M_OPERATING="
            f"{alpha_m:.15e}"
        )

        print(
            f"U_NEAR_PAYLOAD="
            f"{u_near:.15e}"
        )

        print(
            f"PHI_NEAR_PAYLOAD_GEV="
            f"{phi_near_gev:.15e}"
        )

        print(
            f"RECONSTRUCTED_M_M_GEV="
            f"{M_m_gev:.15e}"
        )

        print(
            f"M_M_OVER_M_C="
            f"{M_m_gev/M_c_gev:.15e}"
        )

        # ----------------------------------------------------------
        # Activation candidate.
        # ----------------------------------------------------------

        omega_a = float(
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

        activation = (
            qmod.solve_uncoupled_qball(
                omega_a
            )
        )

        if activation is None:
            raise RuntimeError(
                "Failed activation Q-ball reconstruction"
            )

        print(
            "\n=== STAGE B: CORRECT FINITE-PAYLOAD METRIC ==="
        )

        x_payload = np.linspace(
            x_near,
            x_far,
            PAYLOAD_SAMPLE_N,
        )

        state = source.sol(
            x_payload
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

        rho_a = (
            mu
            * x_payload
        )

        a, ap_rho = (
            d3a.extended_profile(
                activation,
                omega_a,
                rho_a,
            )
        )

        a = np.asarray(
            a,
            dtype=float,
        )

        ap_rho = np.asarray(
            ap_rho,
            dtype=float,
        )

        f = np.asarray(
            d3a.activation_fraction(
                a
            ),
            dtype=float,
        )

        fp = np.asarray(
            d3a.activation_fraction_derivative(
                a
            ),
            dtype=float,
        )

        da_dx = (
            mu
            * ap_rho
        )

        df_dx = (
            fp
            * da_dx
        )

        gamma_m = (
            M_c_gev
            / M_m_gev
        )**2

        # Correct positive-exponent ordinary-matter metric:
        #
        # ln A_m = +gamma_m f u^2 / 2.
        dlogA_baseline_dx = (
            gamma_m
            * u
            * up
        )

        dlogA_activated_dx = (
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

        metric_gradient_relerr = (
            np.abs(
                dlogA_activated_dx
                - dlogA_baseline_dx
            )
            /
            np.maximum(
                np.abs(
                    dlogA_baseline_dx
                ),
                1.0e-300,
            )
        )

        max_metric_gradient_relerr = float(
            np.max(
                metric_gradient_relerr
            )
        )

        f_min = float(
            np.min(
                f
            )
        )

        # Outward scalar acceleration requires
        #
        # a_r = - c^2 d_r ln A_m > 0
        #
        # therefore d_r ln A_m < 0.
        outward_sign_pass = bool(
            np.all(
                dlogA_activated_dx
                < 0.0
            )
        )

        print(
            f"CORRECT_PAYLOAD_F_MIN="
            f"{f_min:.15e}"
        )

        print(
            f"CORRECT_METRIC_GRADIENT_RELERR_MAX="
            f"{max_metric_gradient_relerr:.15e}"
        )

        print(
            f"CORRECT_OUTWARD_METRIC_SIGN_PASS="
            f"{outward_sign_pass}"
        )

        # ----------------------------------------------------------
        # Correct payload reaction on Y.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE C: CORRECT PAYLOAD-TO-Y REACTION ==="
        )

        payload_volume_m3 = (
            4.0
            * math.pi
            * payload_radius_m**3
            / 3.0
        )

        payload_density_kg_m3 = (
            PAYLOAD_MASS_KG
            / payload_volume_m3
        )

        payload_trace_j_m3 = (
            payload_density_kg_m3
            * C_LIGHT**2
        )

        payload_trace_ev4 = (
            payload_trace_j_m3
            / J_PER_EV
            * HBARC_EV_M**3
        )

        phi_ev = (
            M_c_ev
            * u
        )

        intrinsic_shape = (
            np.abs(
                a
                /
                (
                    1.0
                    + a**2
                )
            )
            +
            omega_a**2
            * np.abs(
                a
            )
            +
            1.0e-300
        )

        # Ordinary matter:
        #
        # ln A_m =
        #   + f(a) phi^2/(2 M_m^2)
        #
        # d ln A_m / d sigma_Y =
        #   phi^2 f'(a)/(2 M_m^2 V).
        #
        # Compare T*dlnA/dsigma against
        # m_A^2 V * intrinsic_shape.
        payload_reaction_ratio_array = (
            payload_trace_ev4
            * phi_ev**2
            * np.abs(
                fp
            )
            /
            (
                2.0
                * M_m_ev**2
                * m_a_ev**2
                * V_ev**2
                * intrinsic_shape
            )
        )

        correct_payload_reaction_ratio = float(
            np.max(
                payload_reaction_ratio_array
            )
        )

        old_payload_reaction_ratio = float(
            primary[
                "payload_reaction_ratio"
            ]
        )

        expected_suppression = (
            M_c_gev
            / M_m_gev
        )**2

        observed_suppression = (
            correct_payload_reaction_ratio
            /
            max(
                old_payload_reaction_ratio,
                1.0e-300,
            )
        )

        print(
            f"D3AR_OLD_PAYLOAD_REACTION_RATIO="
            f"{old_payload_reaction_ratio:.15e}"
        )

        print(
            f"CORRECT_PAYLOAD_REACTION_RATIO="
            f"{correct_payload_reaction_ratio:.15e}"
        )

        print(
            f"EXPECTED_MC2_OVER_MM2="
            f"{expected_suppression:.15e}"
        )

        print(
            f"OBSERVED_REACTION_SUPPRESSION="
            f"{observed_suppression:.15e}"
        )

        # ----------------------------------------------------------
        # Distinct EFT operator scales.
        # ----------------------------------------------------------

        print(
            "\n=== STAGE D: SOURCE VS MATTER OPERATOR SCALES ==="
        )

        source_activation_scale_gev = math.sqrt(
            V_gev
            * M_c_gev
        )

        matter_metric_scale_gev = math.sqrt(
            V_gev
            * M_m_gev
        )

        print(
            f"SOURCE_ACTIVATION_OPERATOR_SCALE_GEV="
            f"{source_activation_scale_gev:.15e}"
        )

        print(
            f"MATTER_METRIC_OPERATOR_SCALE_GEV="
            f"{matter_metric_scale_gev:.15e}"
        )

        print(
            f"MATTER_OVER_SOURCE_OPERATOR_SCALE="
            f"{matter_metric_scale_gev/source_activation_scale_gev:.15e}"
        )

        source_reaction_ratio = float(
            primary[
                "source_reaction_ratio"
            ]
        )

        activation_energy_gj = float(
            primary[
                "activation_energy_GJ"
            ]
        )

        operating_energy_gj = (
            float(
                operating[
                    "energy_J"
                ]
            )
            / 1.0e9
        )

        total_gj = (
            operating_energy_gj
            + activation_energy_gj
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

        # With f(a)=0 in the OFF vacuum the source scalarization term
        # is absent at quadratic order, leaving bare +epsilon^2.
        off_scalar_mass2_hat = (
            epsilon**2
        )

        off_scalar_pass = bool(
            off_scalar_mass2_hat
            > 0.0
        )

        print(
            "\n=== STAGE E: DECISION ==="
        )

        print(
            f"SOURCE_REACTION_RATIO="
            f"{source_reaction_ratio:.15e}"
        )

        print(
            f"OFF_SOURCE_QBALL_PASS="
            f"{off_source_pass}"
        )

        print(
            f"OFF_SCALAR_MASS2_HAT="
            f"{off_scalar_mass2_hat:.15e}"
        )

        print(
            f"OFF_SCALAR_STABLE="
            f"{off_scalar_pass}"
        )

        print(
            f"ACTIVATION_ENERGY_GJ="
            f"{activation_energy_gj:.12f}"
        )

        print(
            f"CORRECTED_OPTIMISTIC_TOTAL_GJ="
            f"{total_gj:.12f}"
        )

        metric_pass = bool(
            f_min
            >= MIN_F
            and
            max_metric_gradient_relerr
            <= MAX_METRIC_GRADIENT_RELERR
            and
            outward_sign_pass
        )

        payload_reaction_pass = bool(
            correct_payload_reaction_ratio
            <= MAX_PAYLOAD_REACTION_RATIO
        )

        source_operator_pass = bool(
            source_activation_scale_gev
            >= MIN_SOURCE_OPERATOR_CUTOFF_GEV
            * (
                1.0
                - 1.0e-12
            )
        )

        matter_operator_pass = bool(
            matter_metric_scale_gev
            >= MIN_SOURCE_OPERATOR_CUTOFF_GEV
        )

        off_pass = bool(
            off_source_pass
            and
            off_scalar_pass
        )

        print(
            f"CORRECT_PHYSICAL_METRIC_PASS="
            f"{metric_pass}"
        )

        print(
            f"CORRECT_PAYLOAD_REACTION_PASS="
            f"{payload_reaction_pass}"
        )

        print(
            f"SOURCE_OPERATOR_10GEV_PASS="
            f"{source_operator_pass}"
        )

        print(
            f"MATTER_OPERATOR_10GEV_PASS="
            f"{matter_operator_pass}"
        )

        print(
            f"OFF_STATE_STRUCTURE_PASS="
            f"{off_pass}"
        )

        green = bool(
            metric_pass
            and
            payload_reaction_pass
            and
            source_operator_pass
            and
            matter_operator_pass
            and
            off_pass
        )

        if green:
            classification = (
                "GREEN_D3AR2_CORRECT_SOURCE_AND_"
                "PHYSICAL_METRIC_NORMALIZATION_PASS"
            )

            next_action = (
                "031D3B_FULL_FIXED_QX_QY_COUPLED_"
                "X_PHI_Y_ACTIVATION_SOLVE"
            )

        else:
            classification = (
                "RED_OR_YELLOW_D3AR2_PHYSICAL_"
                "METRIC_NORMALIZATION_REPAIR_FAILED"
            )

            next_action = (
                "DIAGNOSE_FAILED_D3AR2_SUBGATE"
            )

        print(
            f"031D3AR2_CLASSIFICATION="
            f"{classification}"
        )

        print(
            f"NEXT={next_action}"
        )

        print(
            "D3_PHYSICAL_METRIC_SIGN_CORRECTED=YES"
        )

        print(
            "D3_SOURCE_COUPLING_AND_MATTER_METRIC_SEPARATED=YES"
        )

        print(
            "FULL_X_PHI_Y_COUPLED_FIELD_SOLVE=NO"
        )

        print(
            "COUPLED_STABILITY_CLOSED=NO"
        )

        print(
            "CHARGE_INJECTION_RESET_CLOSED=NO"
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

            "couplings": {
                "source":
                    "A_X=exp[-f(a)u^2/2]",

                "ordinary_matter":
                    "A_m=exp[+f(a)phi^2/(2 M_m^2)]",
            },

            "reconstructed": {
                "M_c_GeV":
                    M_c_gev,

                "M_m_GeV":
                    M_m_gev,

                "alpha_m":
                    alpha_m,

                "phi_near_payload_GeV":
                    phi_near_gev,
            },

            "payload": {
                "f_min":
                    f_min,

                "metric_gradient_relerr_max":
                    max_metric_gradient_relerr,

                "outward_sign_pass":
                    outward_sign_pass,

                "old_D3AR_reaction_ratio":
                    old_payload_reaction_ratio,

                "correct_reaction_ratio":
                    correct_payload_reaction_ratio,

                "expected_Mc2_over_Mm2":
                    expected_suppression,

                "observed_suppression":
                    observed_suppression,
            },

            "EFT": {
                "V_GeV":
                    V_gev,

                "source_activation_scale_GeV":
                    source_activation_scale_gev,

                "matter_metric_scale_GeV":
                    matter_metric_scale_gev,
            },

            "energy": {
                "source_operating_GJ":
                    operating_energy_gj,

                "activation_GJ":
                    activation_energy_gj,

                "optimistic_total_GJ":
                    total_gj,
            },

            "off_state": {
                "source_qball_pass":
                    off_source_pass,

                "scalar_mass2_hat":
                    off_scalar_mass2_hat,

                "scalar_stable":
                    off_scalar_pass,
            },

            "claim_limits": [
                (
                    "This is a normalization/provenance repair, "
                    "not the full coupled D3 solution."
                ),
                (
                    "The D3A-R source-reaction and 10-GeV source "
                    "operator tests remain applicable."
                ),
                (
                    "Ordinary-matter reaction must use M_m rather "
                    "than M_c."
                ),
                (
                    "Switching requires activation-charge transport "
                    "or a reservoir and remains unclosed."
                ),
                (
                    "Full coupled stability, metric backreaction, "
                    "radiative naturalness and empirical closure "
                    "remain mandatory."
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

        print(
            f"SUMMARY_JSON={OUT_JSON}"
        )

    finally:
        qmod.X_MATCH = old_xmatch


if __name__ == "__main__":
    main()
