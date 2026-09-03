"""
031A-R4S
=======

Z2 scaling theorem and 83-GJ recovery gate.

PURPOSE
-------
031A-R4 solved an actual nonlinear Z2 scalarization boundary-value problem and
found robust true-stand-off finite-payload 1g solutions below 1 TJ.

Its best edge-robust conservative inventory was approximately

    6.051458764e11 J

rather than the preferred R2R target

    8.275078201430060e10 J.

R4, however, fixed the activated ordinary-matter scalar coupling to

    alpha_m <= 10.

The R4 field equation has an exact fixed-shape scaling symmetry.

For

    A_X(phi) = exp[-phi^2/(2 M_X^2)]

define

    u = phi/M_X

and

    eta = rho_X/(m_phi^2 M_X^2).

At fixed eta, source geometry, edge profile, and mediator range, the
dimensionless equation for u is independent of M_X.

Therefore

    M_X   -> s M_X
    phi   -> s phi
    rho_X -> s^2 rho_X

preserves the dimensionless scalarized solution.

All R4 source and scalar energy terms then scale as

    E -> s^2 E.

For ordinary matter,

    A_m(phi) = exp[phi^2/(2 M_m^2)]

and

    alpha_m = M_Pl phi/M_m^2.

At fixed dimensionless scalar profile,

    a_phi ~ alpha_m M_X.

Hence a target acceleration can be retained under

    s * alpha_m = constant.

This implies the useful classical scaling

    E ~ alpha_m^(-2)

until a separate physical condition such as payload backreaction, EFT
breakdown, radiative instability, empirical leakage, or source realizability
intervenes.

SCIENTIFIC QUESTION
-------------------
Can the exact R4 nonlinear scalarized branch be rescaled back to the
8.275078201430060e10-J target while:

- retaining 1g at the adverse edge of every declared R4 edge profile;
- reproducing the scaling through fresh nonlinear BVP solves rather than
  trusting algebra alone;
- preserving radial stability;
- preserving numerical convergence;
- keeping payload scalar backreaction below 1%;
- keeping the Z2 off-state linear ordinary-matter coupling exactly zero?

This is NOT a microscopic source realization.

The X density profile is still externally prescribed.

This run does NOT establish:

- full source/support conservation;
- B7 realization;
- Q-ball realization;
- nonradial stability;
- EFT/radiative naturalness;
- experimental viability;
- a practical antigravity device.

The purpose is to decide whether the 83-GJ target is already excluded by the
R4 nonlinear field equation, or whether the R4 600-GJ result was largely a
consequence of the provisional alpha_m=10 operating cap.

CLAIM_CLASSIFICATION
--------------------
ANALYTIC_SCALING_THEOREM_PLUS_DIRECT_BVP_VALIDATION
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

R4_PATH = (
    ROOT
    /
    "simulations"
    /
    "031a_r4_z2_induced_scalarization_finite_source_bvp.py"
)

OUT_JSON = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "031a_r4s_z2_scaling_83gj_recovery_summary.json"
)

OUT_CSV = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "031a_r4s_z2_scaling_83gj_scan.csv"
)


G0 = 9.80665

TARGET_E_J = 8.275078201430060e10

BACKREACTION_LIMIT = 1.0e-2


RADIUS_M = 0.95

FACTOR = 9.0


BASE_MX_GEV = 8.365645334354521e1

BASE_ALPHA_M_CAP = 10.0

BASE_RADIAL_EIG = 1.056660623703529e-1


EDGE_BASE = {
    0.025: {
        "E_inventory_J":
        6.051458764238419e11,

        "a_adverse_mps2":
        1.049817721e1,

        "backreaction":
        7.793983546e-4,
    },

    0.050: {
        "E_inventory_J":
        5.814503803077527e11,

        "a_adverse_mps2":
        1.026588288e1,

        "backreaction":
        7.970344234057992e-4,
    },

    0.075: {
        "E_inventory_J":
        5.585192381e11,

        "a_adverse_mps2":
        1.003960851e1,

        "backreaction":
        8.149981179e-4,
    },

    0.100: {
        "E_inventory_J":
        5.363280681e11,

        "a_adverse_mps2":
        9.819147594149598,

        "backreaction":
        8.332965730e-4,
    },
}


BASE_ENERGY_MAX = max(
    value[
        "E_inventory_J"
    ]
    for value
    in EDGE_BASE.values()
)

BASE_ADVERSE_MIN = min(
    value[
        "a_adverse_mps2"
    ]
    for value
    in EDGE_BASE.values()
)

BASE_BACKREACTION_MAX = max(
    value[
        "backreaction"
    ]
    for value
    in EDGE_BASE.values()
)


BASE_PROVENANCE_E_REL_TOL = 5.0e-6

BASE_PROVENANCE_A_REL_TOL = 5.0e-6

BASE_PROVENANCE_BACK_REL_TOL = 5.0e-6


SCALING_REL_TOL = 2.0e-4

FORCE_REL_TOL = 2.0e-4

TARGET_ENERGY_REL_TOL = 3.0e-3

TARGET_FORCE_REL_TOL = 3.0e-3

STABILITY_REL_TOL = 5.0e-3

CONVERGENCE_REL_TOL = 5.0e-3


PHYSICAL_ALPHA_SCAN = [
    10.0,
    15.0,
    20.0,
    25.0,
    27.0,
    30.0,
    35.0,
    40.0,
]


BLIND_WILDCARD_ALPHA_SCAN = [
    6.25,
    16.0,
    18.75,
    31.25,
    50.0,
]


def load_module(
    name: str,
    path: Path,
):

    if not path.is_file():

        raise RuntimeError(
            f"Required source missing: {path}"
        )

    spec = importlib.util.spec_from_file_location(
        name,
        path,
    )

    if (
        spec is None
        or
        spec.loader is None
    ):

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


def relerr(
    a: float,
    b: float,
) -> float:

    return (
        abs(
            a
            -
            b
        )
        /
        max(
            abs(
                a
            ),
            abs(
                b
            ),
            1.0e-300,
        )
    )


def to_builtin(
    value: Any,
):

    if isinstance(
        value,
        np.generic,
    ):

        return value.item()

    if isinstance(
        value,
        np.ndarray,
    ):

        return value.tolist()

    if isinstance(
        value,
        dict,
    ):

        return {
            str(
                key
            ):
            to_builtin(
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
            to_builtin(
                item
            )
            for item
            in value
        ]

    return value


def set_model(
    r4,
    mx_gev: float,
    alpha_m_cap: float,
) -> None:

    r4.M_X_GEV = float(
        mx_gev
    )

    r4.ALPHA_M_PAYLOAD_CAP = float(
        alpha_m_cap
    )


def direct_edge_family(
    r4,
    mx_gev: float,
    alpha_m_cap: float,
    tolerance: float = 1.0e-4,
):

    set_model(
        r4,
        mx_gev,
        alpha_m_cap,
    )

    rows = []

    for edge in sorted(
        EDGE_BASE
    ):

        result = r4.evaluate_case(
            RADIUS_M,
            FACTOR,
            tolerance=tolerance,
            edge_width=edge,
        )

        if not result.get(
            "success",
            False,
        ):

            raise RuntimeError(
                "Direct BVP failed for "
                f"M_X={mx_gev}, "
                f"alpha_m={alpha_m_cap}, "
                f"edge={edge}"
            )

        rows.append(
            {
                "edge_m":
                float(
                    edge
                ),

                "E_inventory_J":
                float(
                    result[
                        "E_inventory_J"
                    ]
                ),

                "E_on_J":
                float(
                    result[
                        "E_on_J"
                    ]
                ),

                "E_off_J":
                float(
                    result[
                        "E_source_off_J"
                    ]
                ),

                "a_cm_mps2":
                float(
                    result[
                        "a_cm_mps2"
                    ]
                ),

                "a_adverse_mps2":
                float(
                    result[
                        "a_adverse_surface_mps2"
                    ]
                ),

                "backreaction":
                float(
                    result[
                        "payload_mass_shift_ratio_rho8000"
                    ]
                ),

                "phi_center_gev":
                float(
                    result[
                        "phi_center_gev"
                    ]
                ),

                "phi_near_gev":
                float(
                    result[
                        "phi_near_payload_gev"
                    ]
                ),

                "M_m_gev":
                float(
                    result[
                        "M_m_required_gev"
                    ]
                ),

                "alpha_x_center":
                float(
                    result[
                        "alpha_x_center"
                    ]
                ),

                "_solved":
                result[
                    "_solved"
                ],
            }
        )

    return rows


def family_extrema(
    rows,
):

    return {
        "energy_max_J":
        max(
            row[
                "E_inventory_J"
            ]
            for row
            in rows
        ),

        "energy_min_J":
        min(
            row[
                "E_inventory_J"
            ]
            for row
            in rows
        ),

        "adverse_min_mps2":
        min(
            row[
                "a_adverse_mps2"
            ]
            for row
            in rows
        ),

        "adverse_max_mps2":
        max(
            row[
                "a_adverse_mps2"
            ]
            for row
            in rows
        ),

        "backreaction_max":
        max(
            row[
                "backreaction"
            ]
            for row
            in rows
        ),
    }


def scaling_prediction(
    alpha_m_cap: float,
    force_factor: float,
):

    s = (
        force_factor
        *
        BASE_ALPHA_M_CAP
        /
        alpha_m_cap
    )

    energy = (
        BASE_ENERGY_MAX
        *
        s
        *
        s
    )

    backreaction = (
        BASE_BACKREACTION_MAX
        *
        alpha_m_cap
        /
        (
            s
            *
            BASE_ALPHA_M_CAP
        )
    )

    return {
        "alpha_m_cap":
        float(
            alpha_m_cap
        ),

        "mx_scale":
        float(
            s
        ),

        "M_X_gev":
        float(
            BASE_MX_GEV
            *
            s
        ),

        "energy_max_J":
        float(
            energy
        ),

        "backreaction_max":
        float(
            backreaction
        ),

        "predicted_adverse_min_mps2":
        float(
            BASE_ADVERSE_MIN
            *
            force_factor
        ),

        "energy_target_pass":
        bool(
            energy
            <=
            TARGET_E_J
        ),

        "backreaction_pass":
        bool(
            backreaction
            <=
            BACKREACTION_LIMIT
        ),

        "joint_pass":
        bool(
            energy
            <=
            TARGET_E_J
            and
            backreaction
            <=
            BACKREACTION_LIMIT
        ),
    }


def main():

    print(
        "=== 031A-R4S Z2 SCALING / "
        "83-GJ RECOVERY GATE ==="
    )

    print(
        "CLAIM_CLASS="
        "ANALYTIC_SCALING_THEOREM_PLUS_"
        "DIRECT_BVP_VALIDATION"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    print(
        "FULL_SOURCE_REALIZATION=NO"
    )

    print(
        "FULL_LOCAL_CONSERVATION=NO"
    )

    print(
        "EFT_NATURALNESS=CARRIED_OPEN"
    )

    r4 = load_module(
        "r4s_upstream_r4",
        R4_PATH,
    )

    print(
        "\n=== A — R4 EXECUTED-CANDIDATE "
        "PROVENANCE RECONSTRUCTION ==="
    )

    base_rows = direct_edge_family(
        r4,
        BASE_MX_GEV,
        BASE_ALPHA_M_CAP,
        tolerance=1.0e-4,
    )

    base_pass = True

    for row in base_rows:

        edge = row[
            "edge_m"
        ]

        reference = EDGE_BASE[
            edge
        ]

        e_rel = relerr(
            row[
                "E_inventory_J"
            ],
            reference[
                "E_inventory_J"
            ],
        )

        a_rel = relerr(
            row[
                "a_adverse_mps2"
            ],
            reference[
                "a_adverse_mps2"
            ],
        )

        b_rel = relerr(
            row[
                "backreaction"
            ],
            reference[
                "backreaction"
            ],
        )

        passed = (
            e_rel
            <=
            BASE_PROVENANCE_E_REL_TOL
            and
            a_rel
            <=
            BASE_PROVENANCE_A_REL_TOL
            and
            b_rel
            <=
            BASE_PROVENANCE_BACK_REL_TOL
        )

        base_pass = (
            base_pass
            and
            passed
        )

        print(
            f"BASE_RECON "
            f"EDGE_M={edge:.3f} "
            f"E_RELERR={e_rel:.9e} "
            f"A_RELERR={a_rel:.9e} "
            f"BACK_RELERR={b_rel:.9e} "
            f"PASS={passed}"
        )

    base_extrema = family_extrema(
        base_rows
    )

    print(
        f"BASE_PROVENANCE_PASS="
        f"{base_pass}"
    )

    print(
        f"BASE_EDGE_MAX_ENERGY_J="
        f"{base_extrema['energy_max_J']:.15e}"
    )

    print(
        f"BASE_EDGE_MIN_ADVERSE_MPS2="
        f"{base_extrema['adverse_min_mps2']:.15e}"
    )

    print(
        f"BASE_EDGE_MAX_BACKREACTION="
        f"{base_extrema['backreaction_max']:.15e}"
    )

    print(
        "\n=== B — EXACT FIXED-SHAPE "
        "SCALING THEOREM ==="
    )

    force_factor = (
        G0
        /
        base_extrema[
            "adverse_min_mps2"
        ]
    )

    s_energy = math.sqrt(
        TARGET_E_J
        /
        base_extrema[
            "energy_max_J"
        ]
    )

    alpha_required = (
        BASE_ALPHA_M_CAP
        *
        force_factor
        /
        s_energy
    )

    mx_required = (
        BASE_MX_GEV
        *
        s_energy
    )

    base_nominal = next(
        row
        for row
        in base_rows
        if math.isclose(
            row[
                "edge_m"
            ],
            0.050,
        )
    )

    mm_scale_sq = (
        s_energy
        *
        BASE_ALPHA_M_CAP
        /
        alpha_required
    )

    mm_scale = math.sqrt(
        mm_scale_sq
    )

    mm_required = (
        base_nominal[
            "M_m_gev"
        ]
        *
        mm_scale
    )

    phi_center_required = (
        base_nominal[
            "phi_center_gev"
        ]
        *
        s_energy
    )

    alpha_x_required = (
        base_nominal[
            "alpha_x_center"
        ]
        /
        s_energy
    )

    predicted_backreaction = (
        base_extrema[
            "backreaction_max"
        ]
        *
        alpha_required
        /
        (
            s_energy
            *
            BASE_ALPHA_M_CAP
        )
    )

    alpha_max_backreaction = (
        BASE_ALPHA_M_CAP
        *
        math.sqrt(
            BACKREACTION_LIMIT
            *
            force_factor
            /
            base_extrema[
                "backreaction_max"
            ]
        )
    )

    s_at_backreaction_limit = (
        force_factor
        *
        BASE_ALPHA_M_CAP
        /
        alpha_max_backreaction
    )

    energy_floor_backreaction = (
        base_extrema[
            "energy_max_J"
        ]
        *
        s_at_backreaction_limit**2
    )

    print(
        f"TARGET_ENERGY_J="
        f"{TARGET_E_J:.15e}"
    )

    print(
        f"FORCE_MATCH_FACTOR="
        f"{force_factor:.15e}"
    )

    print(
        f"ENERGY_SCALE_REQUIRED="
        f"{s_energy:.15e}"
    )

    print(
        f"ALPHA_M_CAP_REQUIRED_FOR_83GJ="
        f"{alpha_required:.15e}"
    )

    print(
        f"M_X_REQUIRED_GEV="
        f"{mx_required:.15e}"
    )

    print(
        f"M_M_NOMINAL_REQUIRED_GEV="
        f"{mm_required:.15e}"
    )

    print(
        f"PHI_CENTER_NOMINAL_REQUIRED_GEV="
        f"{phi_center_required:.15e}"
    )

    print(
        f"ALPHA_X_CENTER_NOMINAL_REQUIRED="
        f"{alpha_x_required:.15e}"
    )

    print(
        f"PREDICTED_MAX_PAYLOAD_BACKREACTION="
        f"{predicted_backreaction:.15e}"
    )

    print(
        f"ALPHA_M_CAP_MAX_AT_1PCT_BACKREACTION="
        f"{alpha_max_backreaction:.15e}"
    )

    print(
        f"ENERGY_FLOOR_AT_1PCT_BACKREACTION_J="
        f"{energy_floor_backreaction:.15e}"
    )

    source_ratio_base = (
        base_nominal[
            "phi_center_gev"
        ]
        /
        BASE_MX_GEV
    )

    source_ratio_scaled = (
        phi_center_required
        /
        mx_required
    )

    lnA_near_base = (
        base_nominal[
            "phi_near_gev"
        ]**2
        /
        (
            2.0
            *
            base_nominal[
                "M_m_gev"
            ]**2
        )
    )

    phi_near_required = (
        base_nominal[
            "phi_near_gev"
        ]
        *
        s_energy
    )

    lnA_near_scaled = (
        phi_near_required**2
        /
        (
            2.0
            *
            mm_required**2
        )
    )

    print(
        f"PHI_CENTER_OVER_MX_BASE="
        f"{source_ratio_base:.15e}"
    )

    print(
        f"PHI_CENTER_OVER_MX_SCALED="
        f"{source_ratio_scaled:.15e}"
    )

    print(
        f"LN_A_M_NEAR_BASE="
        f"{lnA_near_base:.15e}"
    )

    print(
        f"LN_A_M_NEAR_SCALED="
        f"{lnA_near_scaled:.15e}"
    )

    print(
        "\n=== C — ALPHA_M / ENERGY / "
        "BACKREACTION PARETO ==="
    )

    scan_rows = []

    all_alpha = sorted(
        set(
            PHYSICAL_ALPHA_SCAN
            +
            BLIND_WILDCARD_ALPHA_SCAN
            +
            [
                alpha_required,
                alpha_max_backreaction,
            ]
        )
    )

    for alpha in all_alpha:

        row = scaling_prediction(
            alpha,
            force_factor,
        )

        row[
            "blind_wildcard"
        ] = bool(
            alpha
            in
            BLIND_WILDCARD_ALPHA_SCAN
        )

        scan_rows.append(
            row
        )

        print(
            f"SCALING_SCAN "
            f"ALPHA_M_CAP={alpha:.9e} "
            f"BLIND_WILDCARD="
            f"{row['blind_wildcard']} "
            f"M_X_GEV="
            f"{row['M_X_gev']:.9e} "
            f"E_MAX_J="
            f"{row['energy_max_J']:.9e} "
            f"BACK_MAX="
            f"{row['backreaction_max']:.9e} "
            f"ENERGY_PASS="
            f"{row['energy_target_pass']} "
            f"BACK_PASS="
            f"{row['backreaction_pass']} "
            f"JOINT_PASS="
            f"{row['joint_pass']}"
        )

    print(
        "\n=== D — DIRECT BVP VALIDATION "
        "AT 83-GJ SCALING POINT ==="
    )

    target_rows = direct_edge_family(
        r4,
        mx_required,
        alpha_required,
        tolerance=1.0e-4,
    )

    target_extrema = family_extrema(
        target_rows
    )

    direct_scaling_pass = True

    for base, scaled in zip(
        base_rows,
        target_rows,
    ):

        e_predicted = (
            base[
                "E_inventory_J"
            ]
            *
            s_energy**2
        )

        a_predicted = (
            base[
                "a_adverse_mps2"
            ]
            *
            s_energy
            *
            alpha_required
            /
            BASE_ALPHA_M_CAP
        )

        back_predicted = (
            base[
                "backreaction"
            ]
            *
            alpha_required
            /
            (
                s_energy
                *
                BASE_ALPHA_M_CAP
            )
        )

        phi_predicted = (
            base[
                "phi_center_gev"
            ]
            *
            s_energy
        )

        e_rel = relerr(
            scaled[
                "E_inventory_J"
            ],
            e_predicted,
        )

        a_rel = relerr(
            scaled[
                "a_adverse_mps2"
            ],
            a_predicted,
        )

        back_rel = relerr(
            scaled[
                "backreaction"
            ],
            back_predicted,
        )

        phi_rel = relerr(
            scaled[
                "phi_center_gev"
            ],
            phi_predicted,
        )

        passed = (
            e_rel
            <=
            SCALING_REL_TOL
            and
            a_rel
            <=
            FORCE_REL_TOL
            and
            back_rel
            <=
            SCALING_REL_TOL
            and
            phi_rel
            <=
            SCALING_REL_TOL
        )

        direct_scaling_pass = (
            direct_scaling_pass
            and
            passed
        )

        print(
            f"DIRECT_SCALE "
            f"EDGE_M="
            f"{scaled['edge_m']:.3f} "
            f"E_J="
            f"{scaled['E_inventory_J']:.15e} "
            f"A_ADVERSE="
            f"{scaled['a_adverse_mps2']:.15e} "
            f"BACK="
            f"{scaled['backreaction']:.15e} "
            f"E_RELERR="
            f"{e_rel:.9e} "
            f"A_RELERR="
            f"{a_rel:.9e} "
            f"BACK_RELERR="
            f"{back_rel:.9e} "
            f"PHI_RELERR="
            f"{phi_rel:.9e} "
            f"PASS="
            f"{passed}"
        )

    energy_target_pass = (
        target_extrema[
            "energy_max_J"
        ]
        <=
        TARGET_E_J
        *
        (
            1.0
            +
            TARGET_ENERGY_REL_TOL
        )
    )

    force_target_pass = (
        target_extrema[
            "adverse_min_mps2"
        ]
        >=
        G0
        *
        (
            1.0
            -
            TARGET_FORCE_REL_TOL
        )
    )

    backreaction_target_pass = (
        target_extrema[
            "backreaction_max"
        ]
        <=
        BACKREACTION_LIMIT
    )

    print(
        f"DIRECT_SCALING_THEOREM_PASS="
        f"{direct_scaling_pass}"
    )

    print(
        f"DIRECT_EDGE_MAX_ENERGY_J="
        f"{target_extrema['energy_max_J']:.15e}"
    )

    print(
        f"DIRECT_EDGE_MIN_ADVERSE_MPS2="
        f"{target_extrema['adverse_min_mps2']:.15e}"
    )

    print(
        f"DIRECT_EDGE_MAX_BACKREACTION="
        f"{target_extrema['backreaction_max']:.15e}"
    )

    print(
        f"DIRECT_83GJ_ENERGY_PASS="
        f"{energy_target_pass}"
    )

    print(
        f"DIRECT_1G_ALL_EDGE_PASS="
        f"{force_target_pass}"
    )

    print(
        f"DIRECT_BACKREACTION_PASS="
        f"{backreaction_target_pass}"
    )

    print(
        "\n=== E — STABILITY / CONVERGENCE / "
        "EFT-SCALE DIAGNOSTICS ==="
    )

    target_nominal = next(
        row
        for row
        in target_rows
        if math.isclose(
            row[
                "edge_m"
            ],
            0.050,
        )
    )

    radial_eigenvalue = float(
        r4.radial_hessian_lowest_mode(
            target_nominal[
                "_solved"
            ]
        )
    )

    eigenvalue_relerr = relerr(
        radial_eigenvalue,
        BASE_RADIAL_EIG,
    )

    radial_stability_pass = bool(
        radial_eigenvalue
        >
        0.0
        and
        eigenvalue_relerr
        <=
        STABILITY_REL_TOL
    )

    set_model(
        r4,
        mx_required,
        alpha_required,
    )

    convergence_high = r4.evaluate_case(
        RADIUS_M,
        FACTOR,
        tolerance=3.0e-5,
        edge_width=0.050,
    )

    if not convergence_high.get(
        "success",
        False,
    ):

        raise RuntimeError(
            "High-accuracy target BVP failed"
        )

    convergence_energy_relerr = relerr(
        float(
            convergence_high[
                "E_inventory_J"
            ]
        ),
        target_nominal[
            "E_inventory_J"
        ],
    )

    convergence_force_relerr = relerr(
        float(
            convergence_high[
                "a_adverse_surface_mps2"
            ]
        ),
        target_nominal[
            "a_adverse_mps2"
        ],
    )

    convergence_pass = bool(
        convergence_energy_relerr
        <=
        CONVERGENCE_REL_TOL
        and
        convergence_force_relerr
        <=
        CONVERGENCE_REL_TOL
    )

    minimum_edge_m = min(
        EDGE_BASE
    )

    gradient_momentum_gev = (
        r4.HBARC_GEV_M
        /
        minimum_edge_m
    )

    gradient_to_mx = (
        gradient_momentum_gev
        /
        mx_required
    )

    field_to_mx = (
        target_nominal[
            "phi_center_gev"
        ]
        /
        mx_required
    )

    lnA_near_direct = (
        target_nominal[
            "phi_near_gev"
        ]**2
        /
        (
            2.0
            *
            target_nominal[
                "M_m_gev"
            ]**2
        )
    )

    print(
        f"RADIAL_HESSIAN_TARGET_M2INV="
        f"{radial_eigenvalue:.15e}"
    )

    print(
        f"RADIAL_HESSIAN_RELERR_VS_BASE="
        f"{eigenvalue_relerr:.15e}"
    )

    print(
        f"RADIAL_STABILITY_SCALING_PASS="
        f"{radial_stability_pass}"
    )

    print(
        f"CONVERGENCE_E_RELERR="
        f"{convergence_energy_relerr:.15e}"
    )

    print(
        f"CONVERGENCE_A_RELERR="
        f"{convergence_force_relerr:.15e}"
    )

    print(
        f"CONVERGENCE_PASS="
        f"{convergence_pass}"
    )

    print(
        f"MIN_EDGE_GRADIENT_MOMENTUM_GEV="
        f"{gradient_momentum_gev:.15e}"
    )

    print(
        f"GRADIENT_MOMENTUM_OVER_MX="
        f"{gradient_to_mx:.15e}"
    )

    print(
        f"FIELD_AMPLITUDE_OVER_MX="
        f"{field_to_mx:.15e}"
    )

    print(
        f"LN_A_M_NEAR_DIRECT="
        f"{lnA_near_direct:.15e}"
    )

    print(
        "OFF_STATE_LINEAR_MATTER_COUPLING="
        "ZERO_BY_Z2_SYMMETRY"
    )

    print(
        "FIELD_AMPLITUDE_OVER_MX_GT1="
        "NONPOLYNOMIAL_COUPLING_MUST_BE_"
        "TREATED_AS_EXACT_OR_UV_COMPLETED"
    )

    print(
        "RADIATIVE_NATURALNESS="
        "NOT_CLOSED"
    )

    print(
        "\n=== F — DECISION ==="
    )

    target_classical_pass = bool(
        base_pass
        and
        direct_scaling_pass
        and
        energy_target_pass
        and
        force_target_pass
        and
        backreaction_target_pass
        and
        radial_stability_pass
        and
        convergence_pass
        and
        alpha_required
        <
        alpha_max_backreaction
    )

    print(
        f"R4S_BASE_PROVENANCE_PASS="
        f"{base_pass}"
    )

    print(
        f"R4S_SCALING_THEOREM_DIRECTLY_VALIDATED="
        f"{direct_scaling_pass}"
    )

    print(
        f"R4S_83GJ_CLASSICAL_RECOVERY="
        f"{target_classical_pass}"
    )

    print(
        f"R4S_REQUIRED_ALPHA_BELOW_"
        f"BACKREACTION_CEILING="
        f"{alpha_required < alpha_max_backreaction}"
    )

    if target_classical_pass:

        classification = (
            "GREEN_Z2_SCALING_RECOVERS_83GJ_"
            "CLASSICAL_TARGET_WITH_ONSTATE_"
            "ALPHA_M_APPROX27_SOURCE_REALIZATION_"
            "AND_EFT_OPEN"
        )

        next_step = (
            "031B1_B7_FIXED_FIELD_Z2_CHARGE_"
            "TOMOGRAPHY_PLUS_031B2_QBALL_"
            "SCALING_PREFLIGHT"
        )

    else:

        classification = (
            "RED_OR_YELLOW_Z2_83GJ_SCALING_"
            "RECOVERY_NOT_CERTIFIED"
        )

        next_step = (
            "DIAGNOSE_SCALING_OR_BACKREACTION_"
            "BEFORE_MICROSCOPIC_SOURCE"
        )

    print(
        f"031A_R4S_CLASSIFICATION="
        f"{classification}"
    )

    print(
        f"NEXT="
        f"{next_step}"
    )

    for row in scan_rows:

        row[
            "classification"
        ] = (
            "JOINT_PASS"
            if row[
                "joint_pass"
            ]
            else
            "FAIL_ONE_OR_MORE"
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
                scan_rows[
                    0
                ].keys()
            ),
        )

        writer.writeheader()

        writer.writerows(
            scan_rows
        )

    summary = {
        "claim_class":
        "ANALYTIC_SCALING_THEOREM_PLUS_"
        "DIRECT_BVP_VALIDATION",

        "practical_device":
        False,

        "full_source_realization":
        False,

        "full_local_conservation":
        False,

        "target_energy_J":
        TARGET_E_J,

        "target_acceleration_mps2":
        G0,

        "base_provenance_pass":
        base_pass,

        "base_extrema":
        base_extrema,

        "scaling": {
            "force_factor":
            force_factor,

            "mx_scale_required":
            s_energy,

            "alpha_m_cap_required":
            alpha_required,

            "M_X_required_gev":
            mx_required,

            "M_m_nominal_required_gev":
            mm_required,

            "phi_center_nominal_required_gev":
            phi_center_required,

            "alpha_x_center_nominal_required":
            alpha_x_required,

            "predicted_max_backreaction":
            predicted_backreaction,

            "alpha_m_cap_max_1pct_backreaction":
            alpha_max_backreaction,

            "energy_floor_1pct_backreaction_J":
            energy_floor_backreaction,
        },

        "direct_target_extrema":
        target_extrema,

        "direct_scaling_pass":
        direct_scaling_pass,

        "energy_target_pass":
        energy_target_pass,

        "force_target_pass":
        force_target_pass,

        "backreaction_target_pass":
        backreaction_target_pass,

        "radial_hessian_target_m2inv":
        radial_eigenvalue,

        "radial_stability_scaling_pass":
        radial_stability_pass,

        "convergence_pass":
        convergence_pass,

        "field_amplitude_over_MX":
        field_to_mx,

        "gradient_momentum_over_MX":
        gradient_to_mx,

        "ln_A_m_near":
        lnA_near_direct,

        "radiative_naturalness_closed":
        False,

        "classification":
        classification,

        "next":
        next_step,

        "claim_limits": [
            "X density profile remains prescribed.",
            "Full source/support conservation is not established.",
            "Nonradial stability is not established.",
            "EFT/radiative naturalness is not established.",
            "The alpha_m value is an activated on-state coupling.",
            "Empirical off-state closure remains to be demonstrated beyond the exact Z2 linear null.",
            "The 83-GJ recovery uses a scaling symmetry of the R4 prescribed-source model and must survive microscopic source realization.",
        ],
    }

    OUT_JSON.write_text(
        json.dumps(
            to_builtin(
                summary
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
        f"SCAN_CSV="
        f"{OUT_CSV.resolve()}"
    )


if __name__ == "__main__":
    main()
