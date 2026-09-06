#!/usr/bin/env python3
"""
031F0 — radiative-naturalness / empirical stop-rule gate.

Scientific purpose
------------------
031E is GREEN.

Before spending substantial compute on nonlinear fragmentation and
carrier-resolved radiation, test the cheapest potentially fatal 031F gate:

    Can the activated ultralight scalar remain technically natural
    when the declared universal physical metric couples it to
    ordinary quantum matter?

Declared physical metric:

    A_m(phi,a)
      =
    exp[
        f(a) phi^2 / (2 M_m^2)
    ]

with

    f(a)=1-exp(-a^2/2).

OFF:
    a=0
    f=0
    A_m=1

so the ordinary vacuum has no linear scalar coupling.

ON:
    a >> 1
    f -> 1.

Then Einstein-frame matter masses inherit phi dependence.

For a matter threshold m_i, a conservative Coleman-Weinberg /
naive-dimensional-analysis estimate of the induced scalar curvature is

    |delta m_phi^2|
        ~
    c_loop * m_i^4 / (16 pi^2 M_m^2).

This is NOT claimed as an exact scheme-independent finite correction.

It is a technical-naturalness threshold estimator.

The question is whether the required cancellations are small enough to
be naturally explained by symmetries already present in the declared
031 theory.

Current declared symmetries:
- phi -> -phi Z2
- global U(1) source/activation charges
- diffeomorphism invariance / universal physical metric

These do NOT forbid a phi^2 mass operator.

No shift symmetry, supersymmetric threshold cancellation, conformal
sequestering, or other radiative protection has been constructed in
the current 031 theory.

A RED result means:

    CURRENT 031 EFT IS NOT FULLY CERTIFIED.

It does NOT erase:
- classical microscopic field existence;
- coupled-linear stability;
- activation architecture;
- 031D driven adiabatic switching closeout;
- 031E weak-curvature Einstein/Jordan certificate.

It means a new protection mechanism or UV completion is required before
the architecture can be called technically natural.

If RED here, expensive nonlinear 031F evolution is intentionally skipped
by the project stop rule.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "data"

DATA.mkdir(
    parents=True,
    exist_ok=True,
)

E_SUMMARY = (
    DATA
    / "031e_full_physical_metric_einstein_backreaction_summary.json"
)

D2R_SUMMARY = (
    DATA
    / "031d3d2r_dual_ledger_fixed_theory_summary.json"
)

D3AR2_SUMMARY = (
    DATA
    / "031d3ar2_physical_metric_summary.json"
)

R5_SUMMARY = (
    DATA
    / "031d3cr5_saturation_safe_schur_summary.json"
)

OUT_JSON = (
    DATA
    / "031f0_radiative_naturalness_empirical_summary.json"
)

OUT_CSV = (
    DATA
    / "031f0_matter_threshold_naturalness_scan.csv"
)


PI = math.pi

HBARC_EV_M = 1.973269804e-7

MPL_REDUCED_GEV = 2.435e18

# Deliberately generous alternate coefficient.
#
# If even a 10^-3 fraction of the naive threshold estimate destabilizes
# m_phi, the conclusion is insensitive to order-unity convention choices.

GENEROUS_LOOP_COEFFICIENT = 1.0e-3

# We do not require delta m^2 << m^2.
# Even a factor 10 correction is tolerated for this stop gate.

MAX_NATURAL_MASS2_RATIO = 10.0

# Current 031 theory has no demonstrated symmetry which forbids phi^2.

DECLARED_RADIATIVE_PROTECTION_PRESENT = False


# Representative Standard Model thresholds.
#
# Exact last digits are irrelevant because the hierarchy is enormous.
#
# Each calculation below initially uses ONE effective degree of freedom,
# intentionally understating the full Standard Model contribution.

MATTER_THRESHOLDS_GEV = {
    "electron":
        0.00051099895,

    "muon":
        0.1056583755,

    "tau":
        1.77686,

    "W":
        80.369,

    "Z":
        91.1876,

    "Higgs":
        125.25,

    "top":
        172.76,
}


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

    return value


def matter_delta_m2_gev2(
    mass_gev: float,
    M_m_gev: float,
    coefficient: float,
) -> float:
    """
    Conservative threshold / NDA estimator:

        delta m_phi^2
          ~
        c m_i^4/(16 pi^2 M_m^2).

    One effective degree of freedom only.
    """

    return (
        coefficient
        * mass_gev**4
        / (
            16.0
            * PI
            * PI
            * M_m_gev**2
        )
    )


def naturalness_cutoff_gev(
    m_phi_gev: float,
    M_m_gev: float,
    coefficient: float,
) -> float:
    """
    Solve

        c Lambda^4/(16 pi^2 M_m^2)
          =
        m_phi^2.
    """

    return (
        16.0
        * PI
        * PI
        * M_m_gev**2
        * m_phi_gev**2
        / coefficient
    ) ** 0.25


def source_delta_m2_gev2(
    m_x_gev: float,
    M_c_gev: float,
    cutoff_gev: float,
) -> float:
    """
    Source-side NDA.

    Expansion of A_X around the vacuum produces a parametric quartic

        lambda_Xphi ~ m_X^2/M_c^2.

    Estimate

        delta m_phi^2
          ~
        lambda_Xphi Lambda^2/(16 pi^2).

    Coefficients of order unity are intentionally not overclaimed.
    """

    lam = (
        m_x_gev
        / M_c_gev
    ) ** 2

    return (
        lam
        * cutoff_gev
        * cutoff_gev
        / (
            16.0
            * PI
            * PI
        )
    )


def main() -> None:

    print(
        "=== 031F0 RADIATIVE NATURALNESS / EMPIRICAL STOP-RULE GATE ==="
    )

    print(
        "CLAIM_CLASS="
        "TECHNICAL_NATURALNESS_AND_EMPIRICAL_PREFLIGHT"
    )

    print(
        "031E_GREEN_REQUIRED=YES"
    )

    print(
        "NONLINEAR_EXPENSIVE_EVOLUTION_RUN_FIRST=NO"
    )

    print(
        "CHEAP_FATAL_NATURALNESS_TEST_FIRST=YES"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    for path in (
        E_SUMMARY,
        D2R_SUMMARY,
        D3AR2_SUMMARY,
        R5_SUMMARY,
    ):

        require(
            path
        )

    e = load_json(
        E_SUMMARY
    )

    d2r = load_json(
        D2R_SUMMARY
    )

    d3ar2 = load_json(
        D3AR2_SUMMARY
    )

    r5 = load_json(
        R5_SUMMARY
    )

    e_green = bool(
        str(
            e.get(
                "classification",
                "",
            )
        ).startswith(
            "GREEN_031E"
        )

        and

        e[
            "decision"
        ][
            "promotion_authorized"
        ]
    )

    if not e_green:

        raise RuntimeError(
            "031F0 unauthorized because 031E is not GREEN"
        )

    M_c_gev = float(
        d3ar2[
            "reconstructed"
        ][
            "M_c_GeV"
        ]
    )

    M_m_gev = float(
        d3ar2[
            "reconstructed"
        ][
            "M_m_GeV"
        ]
    )

    alpha_m = float(
        d3ar2[
            "reconstructed"
        ][
            "alpha_m"
        ]
    )

    phi_payload_gev = float(
        d3ar2[
            "reconstructed"
        ][
            "phi_near_payload_GeV"
        ]
    )

    source_cutoff_gev = float(
        d3ar2[
            "EFT"
        ][
            "source_activation_scale_GeV"
        ]
    )

    matter_operator_scale_gev = float(
        d3ar2[
            "EFT"
        ][
            "matter_metric_scale_GeV"
        ]
    )

    m_x_ev = float(
        e[
            "geometry"
        ].get(
            "m_x_eV",
            0.0,
        )
    )

    # 031E summary as originally written does not store m_x explicitly.
    # D3D0 does, but avoid another artifact dependency by reconstructing
    # it from the physical length if necessary.

    if m_x_ev <= 0.0:

        # Source length is exactly 0.033 m in the promoted model.
        x_length_m = 0.033

        m_x_ev = (
            HBARC_EV_M
            / x_length_m
        )

    epsilon = float(
        r5[
            "model"
        ][
            "epsilon"
        ]
    )

    m_phi_ev = (
        epsilon
        * m_x_ev
    )

    m_phi_gev = (
        m_phi_ev
        * 1.0e-9
    )

    lambda_phi_m = (
        HBARC_EV_M
        / m_phi_ev
    )

    alpha_rebuilt = (
        MPL_REDUCED_GEV
        * phi_payload_gev
        / (
            M_m_gev
            * M_m_gev
        )
    )

    alpha_relerr = relerr(
        alpha_rebuilt,
        alpha_m,
    )

    local_two_matter_strength = (
        2.0
        * alpha_m
        * alpha_m
    )

    print(
        "\n=== STAGE A: INHERITED 031E / PHYSICAL-METRIC PROVENANCE ==="
    )

    print(
        f"031E_CLASSIFICATION={e['classification']}"
    )

    print(
        f"M_X_EV={m_x_ev:.15e}"
    )

    print(
        f"EPSILON={epsilon:.15e}"
    )

    print(
        f"M_PHI_EV={m_phi_ev:.15e}"
    )

    print(
        f"PHI_COMPTON_RANGE_M={lambda_phi_m:.15e}"
    )

    print(
        f"M_C_GEV={M_c_gev:.15e}"
    )

    print(
        f"M_M_GEV={M_m_gev:.15e}"
    )

    print(
        f"PHI_PAYLOAD_GEV={phi_payload_gev:.15e}"
    )

    print(
        f"ALPHA_M_CERTIFIED={alpha_m:.15e}"
    )

    print(
        f"ALPHA_M_REBUILT={alpha_rebuilt:.15e}"
    )

    print(
        f"ALPHA_M_REBUILD_RELERR={alpha_relerr:.15e}"
    )

    print(
        "LOCAL_ORDINARY_ORDINARY_SCALAR_STRENGTH_2ALPHA2="
        f"{local_two_matter_strength:.15e}"
    )

    print(
        f"SOURCE_OPERATOR_SCALE_GEV={source_cutoff_gev:.15e}"
    )

    print(
        f"MATTER_OPERATOR_SCALE_GEV={matter_operator_scale_gev:.15e}"
    )

    print(
        "\n=== STAGE B: OFF-VACUUM EMPIRICAL STRUCTURE ==="
    )

    # At Y=0:
    #
    # f=0
    # A_X=1
    # A_m=1
    # d ln A_m/d phi = 0.
    #
    # Therefore the standard scalar-tensor weak-field coupling alpha_0
    # of ordinary vacuum matter is exactly zero in the declared classical
    # OFF theory.

    off_f = 0.0

    off_alpha0 = 0.0

    off_ppn_gamma = 1.0

    off_ppn_beta = 1.0

    off_empirical_structural_pass = bool(
        off_f
        == 0.0

        and
        off_alpha0
        == 0.0

        and
        off_ppn_gamma
        == 1.0

        and
        off_ppn_beta
        == 1.0
    )

    print(
        f"OFF_F_ACTIVATION={off_f:.1f}"
    )

    print(
        "OFF_LINEAR_ORDINARY_MATTER_SCALAR_COUPLING="
        f"{off_alpha0:.1f}"
    )

    print(
        f"OFF_PPN_GAMMA={off_ppn_gamma:.15e}"
    )

    print(
        f"OFF_PPN_BETA={off_ppn_beta:.15e}"
    )

    print(
        "STANDARD_UNACTIVATED_YUKAWA_BOUND_DIRECTLY_APPLICABLE="
        "NO"
    )

    print(
        "MICROSCOPE_WEP_BENCHMARK_1SIGMA_ORDER="
        "3E-15"
    )

    print(
        "UNIVERSAL_JORDAN_METRIC_TREE_LEVEL_COMPOSITION_DEPENDENCE="
        "ZERO"
    )

    print(
        "OFF_EMPIRICAL_STRUCTURAL_PASS="
        f"{off_empirical_structural_pass}"
    )

    leakage_radius_m = float(
        e[
            "far_field"
        ][
            "repulsive_to_attractive_zero_m"
        ]
    )

    far_end_m = float(
        e[
            "far_field"
        ][
            "scan_end_m"
        ]
    )

    far_end_accel = float(
        e[
            "far_field"
        ][
            "scan_end_accel_mps2"
        ]
    )

    print(
        f"ON_REPULSIVE_BASIN_ZERO_M={leakage_radius_m:.15e}"
    )

    print(
        f"ON_FAR_SCAN_END_M={far_end_m:.15e}"
    )

    print(
        f"ON_FAR_SCAN_END_ACCEL_MPS2={far_end_accel:+.15e}"
    )

    print(
        "ON_FIELD_IS_STRONGLY_EMPIRICALLY_TESTED_ALREADY="
        "NO_EXOTIC_XY_SOURCE_NOT_KNOWN_TO_EXIST_IN_EXPERIMENTS"
    )

    print(
        "\n=== STAGE C: MATTER-LOOP TECHNICAL NATURALNESS ==="
    )

    cutoff_nominal_gev = naturalness_cutoff_gev(
        m_phi_gev,
        M_m_gev,
        1.0,
    )

    cutoff_generous_gev = naturalness_cutoff_gev(
        m_phi_gev,
        M_m_gev,
        GENEROUS_LOOP_COEFFICIENT,
    )

    print(
        "NDA_MATTER_NATURALNESS_CUTOFF_GEV="
        f"{cutoff_nominal_gev:.15e}"
    )

    print(
        "NDA_MATTER_NATURALNESS_CUTOFF_MEV="
        f"{cutoff_nominal_gev*1.0e3:.15e}"
    )

    print(
        "GENEROUS_1E_MINUS3_NATURALNESS_CUTOFF_GEV="
        f"{cutoff_generous_gev:.15e}"
    )

    print(
        "GENEROUS_1E_MINUS3_NATURALNESS_CUTOFF_MEV="
        f"{cutoff_generous_gev*1.0e3:.15e}"
    )

    print(
        "MATTER_OPERATOR_OVER_NATURALNESS_CUTOFF="
        f"{matter_operator_scale_gev/cutoff_nominal_gev:.15e}"
    )

    threshold_rows = []

    for name, mass_gev in (
        MATTER_THRESHOLDS_GEV.items()
    ):

        dm2_nominal = matter_delta_m2_gev2(
            mass_gev,
            M_m_gev,
            1.0,
        )

        dm2_generous = matter_delta_m2_gev2(
            mass_gev,
            M_m_gev,
            GENEROUS_LOOP_COEFFICIENT,
        )

        ratio_nominal = (
            dm2_nominal
            / (
                m_phi_gev
                * m_phi_gev
            )
        )

        ratio_generous = (
            dm2_generous
            / (
                m_phi_gev
                * m_phi_gev
            )
        )

        induced_mass_ev = (
            math.sqrt(
                abs(
                    dm2_nominal
                )
            )
            * 1.0e9
        )

        induced_range_m = (
            HBARC_EV_M
            / max(
                induced_mass_ev,
                1.0e-300,
            )
        )

        tuning_nominal = (
            1.0
            / max(
                ratio_nominal,
                1.0
            )
        )

        tuning_generous = (
            1.0
            / max(
                ratio_generous,
                1.0
            )
        )

        row = {
            "particle":
                name,

            "mass_GeV":
                mass_gev,

            "delta_m2_over_mphi2_nominal":
                ratio_nominal,

            "delta_m2_over_mphi2_coeff_1e_minus3":
                ratio_generous,

            "induced_mass_scale_eV_nominal":
                induced_mass_ev,

            "induced_range_m_nominal":
                induced_range_m,

            "required_tuning_nominal":
                tuning_nominal,

            "required_tuning_coeff_1e_minus3":
                tuning_generous,
        }

        threshold_rows.append(
            row
        )

        print(
            "THRESHOLD "
            f"NAME={name} "
            f"M_GEV={mass_gev:.9e} "
            f"RATIO={ratio_nominal:.9e} "
            f"RATIO_C1E3={ratio_generous:.9e} "
            f"DM_EV={induced_mass_ev:.9e} "
            f"RANGE_M={induced_range_m:.9e}"
        )

    muon_row = next(
        row
        for row
        in threshold_rows
        if row[
            "particle"
        ]
        == "muon"
    )

    top_row = next(
        row
        for row
        in threshold_rows
        if row[
            "particle"
        ]
        == "top"
    )

    matter_naturalness_pass = bool(
        muon_row[
            "delta_m2_over_mphi2_coeff_1e_minus3"
        ]
        <= MAX_NATURAL_MASS2_RATIO
    )

    print(
        "MUON_ONE_DOF_NOMINAL_RATIO="
        f"{muon_row['delta_m2_over_mphi2_nominal']:.15e}"
    )

    print(
        "MUON_ONE_DOF_RATIO_WITH_1E_MINUS3_COEFF="
        f"{muon_row['delta_m2_over_mphi2_coeff_1e_minus3']:.15e}"
    )

    print(
        "MUON_REQUIRED_TUNING_NOMINAL="
        f"{muon_row['required_tuning_nominal']:.15e}"
    )

    print(
        "TOP_ONE_DOF_NOMINAL_RATIO="
        f"{top_row['delta_m2_over_mphi2_nominal']:.15e}"
    )

    print(
        "TOP_REQUIRED_TUNING_NOMINAL="
        f"{top_row['required_tuning_nominal']:.15e}"
    )

    print(
        "MATTER_THRESHOLD_NATURALNESS_PASS="
        f"{matter_naturalness_pass}"
    )

    print(
        "\n=== STAGE D: SOURCE-SECTOR LOOP SCALE ==="
    )

    m_x_gev = (
        m_x_ev
        * 1.0e-9
    )

    source_dm2 = source_delta_m2_gev2(
        m_x_gev,
        M_c_gev,
        source_cutoff_gev,
    )

    source_ratio = (
        source_dm2
        / (
            m_phi_gev
            * m_phi_gev
        )
    )

    source_naturalness_cutoff_gev = (
        4.0
        * PI
        * m_phi_gev
        * M_c_gev
        / m_x_gev
    )

    source_naturalness_pass = bool(
        source_ratio
        <= MAX_NATURAL_MASS2_RATIO
    )

    print(
        "SOURCE_LAMBDA_XPHI_NDA="
        f"{(m_x_gev/M_c_gev)**2:.15e}"
    )

    print(
        "SOURCE_10GEV_DELTA_M2_OVER_MPHI2="
        f"{source_ratio:.15e}"
    )

    print(
        "SOURCE_NATURALNESS_CUTOFF_GEV="
        f"{source_naturalness_cutoff_gev:.15e}"
    )

    print(
        "SOURCE_SECTOR_NATURALNESS_PREFLIGHT_PASS="
        f"{source_naturalness_pass}"
    )

    print(
        "\n=== STAGE E: PROTECTION / SYMMETRY AUDIT ==="
    )

    print(
        "PHI_Z2_PRESENT=True"
    )

    print(
        "PHI_Z2_FORBIDS_LINEAR_TERM=True"
    )

    print(
        "PHI_Z2_FORBIDS_MASS_TERM=False"
    )

    print(
        "GLOBAL_U1_PROTECTS_PHI_MASS=False"
    )

    print(
        "SHIFT_SYMMETRY_PRESENT=False"
    )

    print(
        "SUPERSYMMETRIC_THRESHOLD_CANCELLATION_PRESENT=False"
    )

    print(
        "SEQUESTERING_MECHANISM_PRESENT=False"
    )

    print(
        "OTHER_EXPLICIT_RADIATIVE_PROTECTION_PRESENT="
        f"{DECLARED_RADIATIVE_PROTECTION_PRESENT}"
    )

    protection_pass = bool(
        DECLARED_RADIATIVE_PROTECTION_PRESENT
    )

    print(
        f"RADIATIVE_PROTECTION_GATE_PASS={protection_pass}"
    )

    print(
        "\n=== STAGE F: PRACTICAL / SWITCHING LEDGER CARRY-FORWARD ==="
    )

    conservative_on_j = float(
        e[
            "stress_energy"
        ][
            "conservative_inventory_J"
        ]
    )

    activation_release_j = float(
        d2r[
            "same_mass_endpoints"
        ][
            "exact_forward_release_J"
        ]
    )

    reset_work_j = float(
        d2r[
            "same_mass_endpoints"
        ][
            "minimum_reversible_reset_work_J"
        ]
    )

    payload_force_n = float(
        e[
            "payload_backreaction"
        ][
            "interaction_force_N"
        ]
    )

    source_recoil = float(
        e[
            "payload_backreaction"
        ][
            "free_source_recoil_diagnostic_mps2"
        ]
    )

    print(
        "CONSERVATIVE_ON_INVENTORY_GJ="
        f"{conservative_on_j/1.0e9:.15e}"
    )

    print(
        "FORWARD_ACTIVATION_RELEASE_GJ="
        f"{activation_release_j/1.0e9:.15e}"
    )

    print(
        "RESET_REVERSIBLE_WORK_FLOOR_GJ="
        f"{reset_work_j/1.0e9:.15e}"
    )

    print(
        "ONE_SECOND_RESET_POWER_FLOOR_W="
        f"{reset_work_j:.15e}"
    )

    print(
        f"ONE_KG_PAYLOAD_FORCE_N={payload_force_n:.15e}"
    )

    print(
        "FREE_SOURCE_RECOIL_DIAGNOSTIC_MPS2="
        f"{source_recoil:.15e}"
    )

    print(
        "LAB_SUPPORT_HARDWARE_REALIZED=False"
    )

    print(
        "RESET_ENERGY_RECOVERY_REALIZED=False"
    )

    print(
        "\n=== STAGE G: 031F0 DECISION ==="
    )

    radiative_naturalness_green = bool(
        matter_naturalness_pass
        and
        source_naturalness_pass
        and
        protection_pass
    )

    empirical_vacuum_green = bool(
        off_empirical_structural_pass
    )

    print(
        "EMPIRICAL_OFF_VACUUM_STRUCTURE_PASS="
        f"{empirical_vacuum_green}"
    )

    print(
        "SOURCE_SECTOR_NATURALNESS_PASS="
        f"{source_naturalness_pass}"
    )

    print(
        "MATTER_SECTOR_NATURALNESS_PASS="
        f"{matter_naturalness_pass}"
    )

    print(
        "EXPLICIT_PROTECTION_PRESENT="
        f"{protection_pass}"
    )

    print(
        "RADIATIVE_NATURALNESS_FULL_PASS="
        f"{radiative_naturalness_green}"
    )

    if not radiative_naturalness_green:

        classification = (
            "RED_031F0_CURRENT_031_EFT_RADIATIVE_"
            "NATURALNESS_OBSTRUCTION_NO_PROTECTION"
        )

        next_action = (
            "STOP_CURRENT_031_FULL_CERTIFICATION_OR_INTRODUCE_"
            "GENUINE_RADIATIVE_PROTECTION_AND_RESTART_AFFECTED_GATES"
        )

        nonlinear_run_authorized = False

    else:

        classification = (
            "GREEN_031F0_RADIATIVE_NATURALNESS_"
            "EMPIRICAL_PREFLIGHT"
        )

        next_action = (
            "031F1_NONLINEAR_FRAGMENTATION_CARRIER_RADIATION_FINAL_GATE"
        )

        nonlinear_run_authorized = True

    print(
        f"031F0_CLASSIFICATION={classification}"
    )

    print(
        "EXPENSIVE_031F_NONLINEAR_RUN_AUTHORIZED="
        f"{nonlinear_run_authorized}"
    )

    print(
        "CLASSICAL_MICROSCOPIC_FIELD_RESULT_REVOKED=NO"
    )

    print(
        "031D_SWITCHING_RESULT_REVOKED=NO"
    )

    print(
        "031E_EINSTEIN_JORDAN_RESULT_REVOKED=NO"
    )

    print(
        "CURRENT_031_THEORY_FULLY_CERTIFIED="
        f"{radiative_naturalness_green}"
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
            "TECHNICAL_NATURALNESS_AND_EMPIRICAL_PREFLIGHT",

        "inherited": {
            "031E":
                e[
                    "classification"
                ],

            "D3D2R":
                d2r[
                    "classification"
                ],

            "R5":
                r5[
                    "classification"
                ],
        },

        "scales": {
            "m_X_eV":
                m_x_ev,

            "m_phi_eV":
                m_phi_ev,

            "phi_range_m":
                lambda_phi_m,

            "M_c_GeV":
                M_c_gev,

            "M_m_GeV":
                M_m_gev,

            "source_operator_GeV":
                source_cutoff_gev,

            "matter_operator_GeV":
                matter_operator_scale_gev,

            "matter_naturalness_cutoff_GeV":
                cutoff_nominal_gev,

            "matter_naturalness_cutoff_coeff_1e_minus3_GeV":
                cutoff_generous_gev,
        },

        "ordinary_metric": {
            "alpha_m_certified":
                alpha_m,

            "alpha_m_rebuilt":
                alpha_rebuilt,

            "alpha_relerr":
                alpha_relerr,

            "local_2alpha2":
                local_two_matter_strength,

            "OFF_alpha0":
                off_alpha0,

            "OFF_PPN_gamma":
                off_ppn_gamma,

            "OFF_PPN_beta":
                off_ppn_beta,

            "OFF_structural_empirical_pass":
                off_empirical_structural_pass,

            "ON_repulsive_zero_m":
                leakage_radius_m,
        },

        "matter_thresholds":
            threshold_rows,

        "source_naturalness": {
            "delta_m2_over_mphi2_at_declared_cutoff":
                source_ratio,

            "naturalness_cutoff_GeV":
                source_naturalness_cutoff_gev,

            "pass":
                source_naturalness_pass,
        },

        "protection": {
            "phi_Z2":
                True,

            "phi_Z2_protects_mass":
                False,

            "shift_symmetry":
                False,

            "supersymmetry":
                False,

            "sequestering":
                False,

            "other_explicit_protection":
                DECLARED_RADIATIVE_PROTECTION_PRESENT,

            "pass":
                protection_pass,
        },

        "practical": {
            "conservative_ON_inventory_J":
                conservative_on_j,

            "activation_release_J":
                activation_release_j,

            "reset_work_floor_J":
                reset_work_j,

            "payload_force_N":
                payload_force_n,

            "free_source_recoil_mps2":
                source_recoil,

            "support_hardware_realized":
                False,

            "reset_recovery_realized":
                False,
        },

        "decision": {
            "empirical_OFF_vacuum_pass":
                empirical_vacuum_green,

            "matter_naturalness_pass":
                matter_naturalness_pass,

            "source_naturalness_pass":
                source_naturalness_pass,

            "explicit_protection_pass":
                protection_pass,

            "radiative_naturalness_full_pass":
                radiative_naturalness_green,

            "nonlinear_run_authorized":
                nonlinear_run_authorized,
        },

        "claim_limits": [
            (
                "The loop calculation is an NDA/threshold "
                "technical-naturalness estimate, not an exact "
                "scheme-independent one-loop matching result."
            ),
            (
                "The muon and heavier thresholds exceed the "
                "required scalar mass hierarchy by so many orders "
                "that ordinary order-unity scheme factors cannot "
                "restore naturalness."
            ),
            (
                "A demonstrated symmetry or UV mechanism could "
                "change the conclusion, but none is present in the "
                "current declared 031 theory."
            ),
            (
                "OFF-state fifth-force/PPN constraints are not "
                "naively identical to an always-on Yukawa theory "
                "because f(0)=0 exactly."
            ),
            (
                "RED does not revoke the classical field, stability, "
                "switching, or Einstein/Jordan certificates."
            ),
            (
                "RED means the current EFT is not technically "
                "natural and therefore cannot receive full 031 "
                "certification."
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

    fields = list(
        threshold_rows[
            0
        ].keys()
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
            threshold_rows
        )

    print(
        f"SUMMARY_JSON={OUT_JSON}"
    )

    print(
        f"THRESHOLD_CSV={OUT_CSV}"
    )


if __name__ == "__main__":
    main()
