"""
031A-R3D
=======

R2R provenance and near-degenerate convex-QP tomography audit.

Scientific question
-------------------
R3 formally failed because the net-neutral reconstruction differed from the
stored R2R field/core decomposition by about 5.5 ppm while reproducing total
energy to about 2.5e-10 relative error.

This audit determines whether that discrepancy represents:

1. a genuine provenance inconsistency, or
2. a nearly flat / near-degenerate direction in the convex R2R optimization
   whose total energy is stable while field/core decomposition changes by ppm.

No physics tolerance is silently relaxed.

For each of the two key R2R cases this run:

- reconstructs the original solution;
- refines the convex minimum with tighter numerical tolerances;
- checks all physical constraints;
- constructs a near-optimal energy shell;
- minimizes and maximizes core energy inside that shell;
- tests whether the stored R2R decomposition lies inside that shell;
- reconstructs scalar-field excursion tomography across the envelope;
- tests whether order-unity source-field excursion is robust to the numerical
  degeneracy.

Promotion condition
-------------------
PROVENANCE_REPAIRED=True requires:

- total objective reconstruction < 1e-7 relative;
- constraints satisfied;
- stored field/core decomposition contained inside the 1e-5 near-optimal
  decomposition envelope;
- order-unity field-excursion conclusion robust across the envelope.

This does not establish a microscopic field or practical device.
"""

from __future__ import annotations

import csv
import importlib.util
import math
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize


ROOT = Path(__file__).resolve().parents[1]

R3_PATH = (
    ROOT
    /
    "simulations"
    /
    "031a_r3_nonlinear_protected_activation_gate.py"
)

R2_CSV = (
    ROOT
    /
    "results"
    /
    "data"
    /
    "031a_r2r_finite_support_scalar_charge_pareto.csv"
)

RESULTS = (
    ROOT
    /
    "results"
    /
    "data"
)

RESULTS.mkdir(
    parents=True,
    exist_ok=True,
)


CASES = (
    (
        "MONO_LE_0P1",
        10.0,
        5.623413251903491e16,
        0.10,
    ),
    (
        "NET_NEUTRAL",
        10.0,
        5.623413251903491e16,
        0.0,
    ),
)

NEAR_OPT_EPS = (
    1.0e-8,
    1.0e-6,
    1.0e-5,
)


def load_module(
    path: Path,
    name: str,
):

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
            f"IMPORT_SPEC_FAILURE={path}"
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


def stored_row(
    alpha_m,
    alpha_x,
    leak,
):

    with R2_CSV.open(
        newline="",
    ) as handle:

        rows = list(
            csv.DictReader(
                handle
            )
        )

    for row in rows:

        if row[
            "family"
        ] != "unrestricted":
            continue

        if row[
            "success"
        ] != "True":
            continue

        if not math.isclose(
            float(
                row[
                    "alpha_m"
                ]
            ),
            alpha_m,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ):
            continue

        if not math.isclose(
            float(
                row[
                    "alpha_x"
                ]
            ),
            alpha_x,
            rel_tol=2.0e-12,
        ):
            continue

        if not math.isclose(
            float(
                row[
                    "leakage_fraction"
                ]
            ),
            leak,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ):
            continue

        return {
            "E_total_J":
            float(
                row[
                    "E_total_J"
                ]
            ),

            "E_field_J":
            float(
                row[
                    "E_field_J"
                ]
            ),

            "E_core_J":
            float(
                row[
                    "E_core_J"
                ]
            ),
        }

    raise RuntimeError(
        "STORED_R2_ROW_NOT_FOUND"
    )


def relerr(
    a,
    b,
):

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


def build_problem(
    r2,
    geometry,
    alpha_m,
    alpha_x,
    leakage_fraction,
):

    K = geometry[
        "field_kernel"
    ]

    acceleration_geometry = geometry[
        "acceleration_geometry"
    ]

    n = len(
        acceleration_geometry
    )

    qref = (
        r2.G0
        *
        r2.D**2
        /
        (
            2.0
            *
            r2.G
            *
            alpha_m
        )
    )

    field_scale = (
        r2.G
        *
        qref**2
        /
        r2.TARGET_1TJ
    )

    core_scale = (
        r2.C**2
        *
        qref
        /
        alpha_x
        /
        r2.TARGET_1TJ
    )

    scalar_kernel = (
        r2.D**2
        *
        acceleration_geometry
    )

    gr_kernel = (
        r2.D**2
        *
        acceleration_geometry
        /
        (
            2.0
            *
            alpha_m
            *
            alpha_x
        )
    )

    acceleration_row = np.concatenate(
        (
            scalar_kernel
            +
            gr_kernel,
            -scalar_kernel
            +
            gr_kernel,
        )
    )

    ones = np.ones(
        n
    )

    net_row = np.concatenate(
        (
            ones,
            -ones,
        )
    )

    abs_row = np.concatenate(
        (
            ones,
            ones,
        )
    )

    def signed(
        x,
    ):

        return (
            x[
                :n
            ]
            -
            x[
                n:
            ]
        )

    def absolute(
        x,
    ):

        return (
            x[
                :n
            ]
            +
            x[
                n:
            ]
        )

    def field_dimless(
        x,
    ):

        s = signed(
            x
        )

        return (
            field_scale
            *
            float(
                s
                @
                K
                @
                s
            )
        )

    def core_dimless(
        x,
    ):

        return (
            core_scale
            *
            float(
                np.sum(
                    absolute(
                        x
                    )
                )
            )
        )

    def total_dimless(
        x,
    ):

        return (
            field_dimless(
                x
            )
            +
            core_dimless(
                x
            )
        )

    def total_gradient(
        x,
    ):

        s = signed(
            x
        )

        gs = (
            2.0
            *
            field_scale
            *
            (
                K
                @
                s
            )
        )

        return np.concatenate(
            (
                gs
                +
                core_scale,
                -gs
                +
                core_scale,
            )
        )

    core_gradient = (
        core_scale
        *
        np.ones(
            2
            *
            n
        )
    )

    constraints = [
        {
            "type":
            "ineq",

            "fun":
            (
                lambda x:
                float(
                    acceleration_row
                    @
                    x
                    -
                    1.0
                )
            ),

            "jac":
            (
                lambda x:
                acceleration_row
            ),
        }
    ]

    if leakage_fraction == 0.0:

        constraints.append(
            {
                "type":
                "eq",

                "fun":
                (
                    lambda x:
                    float(
                        net_row
                        @
                        x
                    )
                ),

                "jac":
                (
                    lambda x:
                    net_row
                ),
            }
        )

    elif leakage_fraction < 1.0:

        constraints.extend(
            [
                {
                    "type":
                    "ineq",

                    "fun":
                    (
                        lambda x:
                        float(
                            leakage_fraction
                            *
                            (
                                abs_row
                                @
                                x
                            )
                            -
                            (
                                net_row
                                @
                                x
                            )
                        )
                    ),

                    "jac":
                    (
                        lambda x:
                        (
                            leakage_fraction
                            *
                            abs_row
                            -
                            net_row
                        )
                    ),
                },
                {
                    "type":
                    "ineq",

                    "fun":
                    (
                        lambda x:
                        float(
                            leakage_fraction
                            *
                            (
                                abs_row
                                @
                                x
                            )
                            +
                            (
                                net_row
                                @
                                x
                            )
                        )
                    ),

                    "jac":
                    (
                        lambda x:
                        (
                            leakage_fraction
                            *
                            abs_row
                            +
                            net_row
                        )
                    ),
                },
            ]
        )

    bounds = [
        (
            0.0,
            None,
        )
    ] * (
        2
        *
        n
    )

    return {
        "K":
        K,

        "n":
        n,

        "qref":
        qref,

        "field_scale":
        field_scale,

        "core_scale":
        core_scale,

        "acceleration_row":
        acceleration_row,

        "net_row":
        net_row,

        "abs_row":
        abs_row,

        "signed":
        signed,

        "absolute":
        absolute,

        "field":
        field_dimless,

        "core":
        core_dimless,

        "total":
        total_dimless,

        "gradient":
        total_gradient,

        "core_gradient":
        core_gradient,

        "constraints":
        constraints,

        "bounds":
        bounds,
    }


def constraint_diagnostics(
    problem,
    x,
    leak,
):

    acceleration_margin = float(
        problem[
            "acceleration_row"
        ]
        @
        x
        -
        1.0
    )

    net = float(
        problem[
            "net_row"
        ]
        @
        x
    )

    absolute = float(
        problem[
            "abs_row"
        ]
        @
        x
    )

    if leak == 0.0:

        leakage_margin = (
            -abs(
                net
            )
        )

        leakage_violation = abs(
            net
        )

    else:

        leakage_margin = (
            leak
            *
            absolute
            -
            abs(
                net
            )
        )

        leakage_violation = max(
            0.0,
            -leakage_margin,
        )

    nonnegative_violation = max(
        0.0,
        -float(
            np.min(
                x
            )
        ),
    )

    return {
        "acceleration_margin":
        acceleration_margin,

        "leakage_margin":
        leakage_margin,

        "leakage_violation":
        leakage_violation,

        "nonnegative_violation":
        nonnegative_violation,
    }


def tomography(
    r3,
    r2,
    geometry,
    problem,
    x,
    alpha_x,
):

    n = problem[
        "n"
    ]

    signed = problem[
        "signed"
    ](
        x
    )

    absolute = problem[
        "absolute"
    ](
        x
    )

    q_signed = (
        problem[
            "qref"
        ]
        *
        signed
    )

    q_abs = (
        problem[
            "qref"
        ]
        *
        absolute
    )

    psi = (
        geometry[
            "field_kernel"
        ]
        @
        q_signed
    )

    signs = np.sign(
        signed
    )

    w = (
        signs
        *
        (
            -2.0
            *
            r2.G
            *
            alpha_x
            *
            psi
            /
            r2.C**2
        )
    )

    weights = q_abs

    active = (
        weights
        >
        0.0
    )

    if not np.any(
        active
    ):

        return {
            "w50":
            math.nan,

            "w90":
            math.nan,

            "wmax":
            math.nan,

            "mean_signed_w":
            math.nan,
        }

    w50 = r3.weighted_quantile(
        np.abs(
            w
        ),
        weights,
        0.50,
    )

    w90 = r3.weighted_quantile(
        np.abs(
            w
        ),
        weights,
        0.90,
    )

    mean_signed_w = float(
        np.sum(
            weights
            *
            w
        )
        /
        np.sum(
            weights
        )
    )

    return {
        "w50":
        w50,

        "w90":
        w90,

        "wmax":
        float(
            np.max(
                np.abs(
                    w[
                        active
                    ]
                )
            )
        ),

        "mean_signed_w":
        mean_signed_w,
    }


def refine_minimum(
    problem,
    x0,
):

    return minimize(
        problem[
            "total"
        ],
        x0,
        jac=problem[
            "gradient"
        ],
        method="SLSQP",
        bounds=problem[
            "bounds"
        ],
        constraints=problem[
            "constraints"
        ],
        options={
            "ftol":
            1.0e-13,

            "maxiter":
            5000,

            "disp":
            False,
        },
    )


def envelope_solution(
    problem,
    x0,
    best_total,
    eps,
    direction,
):

    constraints = list(
        problem[
            "constraints"
        ]
    )

    budget = (
        best_total
        *
        (
            1.0
            +
            eps
        )
    )

    constraints.append(
        {
            "type":
            "ineq",

            "fun":
            (
                lambda x:
                float(
                    budget
                    -
                    problem[
                        "total"
                    ](
                        x
                    )
                )
            ),

            "jac":
            (
                lambda x:
                -problem[
                    "gradient"
                ](
                    x
                )
            ),
        }
    )

    if direction == "MIN_CORE":

        fun = problem[
            "core"
        ]

        jac = (
            lambda x:
            problem[
                "core_gradient"
            ]
        )

    elif direction == "MAX_CORE":

        fun = (
            lambda x:
            -problem[
                "core"
            ](
                x
            )
        )

        jac = (
            lambda x:
            -problem[
                "core_gradient"
            ]
        )

    else:

        raise ValueError(
            direction
        )

    return minimize(
        fun,
        x0,
        jac=jac,
        method="SLSQP",
        bounds=problem[
            "bounds"
        ],
        constraints=constraints,
        options={
            "ftol":
            1.0e-12,

            "maxiter":
            5000,

            "disp":
            False,
        },
    )


def main():

    print(
        "=== 031A-R3D R2R PROVENANCE / "
        "NEAR-DEGENERATE QP AUDIT ==="
    )

    print(
        "CLAIM_CLASS="
        "NUMERICAL_PROVENANCE_AND_TOMOGRAPHY_AUDIT"
    )

    print(
        "MICROSCOPIC_FIELD=NO"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    r3 = load_module(
        R3_PATH,
        "r3audit",
    )

    r2 = r3.load_r2_module()

    geometry = r2.build_geometry(
        r2.MEDIUM
    )

    overall_provenance = True

    overall_tomography = True

    case_summaries = []

    for (
        label,
        alpha_m,
        alpha_x,
        leak,
    ) in CASES:

        print()
        print(
            f"=== CASE {label} ==="
        )

        expected = stored_row(
            alpha_m,
            alpha_x,
            leak,
        )

        baseline = r3.solve_vector(
            r2,
            geometry,
            alpha_m,
            alpha_x,
            leak,
        )

        x0 = baseline[
            "vector"
        ]

        problem = build_problem(
            r2,
            geometry,
            alpha_m,
            alpha_x,
            leak,
        )

        refined = refine_minimum(
            problem,
            x0,
        )

        xbest = (
            refined.x
            if refined.success
            else x0
        )

        best_total = problem[
            "total"
        ](
            xbest
        )

        best_field = problem[
            "field"
        ](
            xbest
        )

        best_core = problem[
            "core"
        ](
            xbest
        )

        total_j = (
            best_total
            *
            r2.TARGET_1TJ
        )

        field_j = (
            best_field
            *
            r2.TARGET_1TJ
        )

        core_j = (
            best_core
            *
            r2.TARGET_1TJ
        )

        total_rel = relerr(
            total_j,
            expected[
                "E_total_J"
            ],
        )

        field_rel = relerr(
            field_j,
            expected[
                "E_field_J"
            ],
        )

        core_rel = relerr(
            core_j,
            expected[
                "E_core_J"
            ],
        )

        diagnostics = constraint_diagnostics(
            problem,
            xbest,
            leak,
        )

        print(
            f"REFINED_MINIMUM "
            f"CASE={label} "
            f"SUCCESS={refined.success} "
            f"E_TOTAL_J={total_j:.15e} "
            f"E_FIELD_J={field_j:.15e} "
            f"E_CORE_J={core_j:.15e} "
            f"TOTAL_RELERR={total_rel:.9e} "
            f"FIELD_RELERR={field_rel:.9e} "
            f"CORE_RELERR={core_rel:.9e}"
        )

        print(
            f"CONSTRAINT_AUDIT "
            f"CASE={label} "
            f"ACC_MARGIN="
            f"{diagnostics['acceleration_margin']:.9e} "
            f"LEAK_MARGIN="
            f"{diagnostics['leakage_margin']:.9e} "
            f"LEAK_VIOL="
            f"{diagnostics['leakage_violation']:.9e} "
            f"NONNEG_VIOL="
            f"{diagnostics['nonnegative_violation']:.9e}"
        )

        expected_core_dimless = (
            expected[
                "E_core_J"
            ]
            /
            r2.TARGET_1TJ
        )

        envelope_records = []

        stored_inside_1e5 = False

        robust_w50 = []

        robust_w90 = []

        for eps in NEAR_OPT_EPS:

            low = envelope_solution(
                problem,
                xbest,
                best_total,
                eps,
                "MIN_CORE",
            )

            high = envelope_solution(
                problem,
                xbest,
                best_total,
                eps,
                "MAX_CORE",
            )

            if (
                not low.success
                or
                not high.success
            ):

                print(
                    f"ENVELOPE "
                    f"CASE={label} "
                    f"EPS={eps:.1e} "
                    f"PASS=False "
                    f"LOW_SUCCESS={low.success} "
                    f"HIGH_SUCCESS={high.success}"
                )

                overall_provenance = False

                continue

            core_low = problem[
                "core"
            ](
                low.x
            )

            core_high = problem[
                "core"
            ](
                high.x
            )

            if core_low > core_high:

                core_low, core_high = (
                    core_high,
                    core_low,
                )

                low, high = (
                    high,
                    low,
                )

            inside = (
                expected_core_dimless
                >=
                core_low
                -
                1.0e-12
                and
                expected_core_dimless
                <=
                core_high
                +
                1.0e-12
            )

            if math.isclose(
                eps,
                1.0e-5,
                rel_tol=0.0,
                abs_tol=1.0e-15,
            ):

                stored_inside_1e5 = inside

            tomo_low = tomography(
                r3,
                r2,
                geometry,
                problem,
                low.x,
                alpha_x,
            )

            tomo_high = tomography(
                r3,
                r2,
                geometry,
                problem,
                high.x,
                alpha_x,
            )

            robust_w50.extend(
                [
                    tomo_low[
                        "w50"
                    ],
                    tomo_high[
                        "w50"
                    ],
                ]
            )

            robust_w90.extend(
                [
                    tomo_low[
                        "w90"
                    ],
                    tomo_high[
                        "w90"
                    ],
                ]
            )

            print(
                f"ENVELOPE "
                f"CASE={label} "
                f"EPS={eps:.1e} "
                f"PASS=True "
                f"CORE_MIN_J="
                f"{core_low*r2.TARGET_1TJ:.15e} "
                f"CORE_MAX_J="
                f"{core_high*r2.TARGET_1TJ:.15e} "
                f"STORED_CORE_INSIDE={inside} "
                f"W50_MINCORE="
                f"{tomo_low['w50']:.9e} "
                f"W90_MINCORE="
                f"{tomo_low['w90']:.9e} "
                f"W50_MAXCORE="
                f"{tomo_high['w50']:.9e} "
                f"W90_MAXCORE="
                f"{tomo_high['w90']:.9e}"
            )

            envelope_records.append(
                (
                    eps,
                    core_low,
                    core_high,
                    inside,
                    tomo_low,
                    tomo_high,
                )
            )

        finite_w50 = [
            value
            for value
            in robust_w50
            if math.isfinite(
                value
            )
        ]

        finite_w90 = [
            value
            for value
            in robust_w90
            if math.isfinite(
                value
            )
        ]

        min_w50 = (
            min(
                finite_w50
            )
            if finite_w50
            else math.nan
        )

        min_w90 = (
            min(
                finite_w90
            )
            if finite_w90
            else math.nan
        )

        tomography_robust = (
            math.isfinite(
                min_w50
            )
            and
            math.isfinite(
                min_w90
            )
            and
            min_w50
            >
            0.50
            and
            min_w90
            >
            1.0
        )

        provenance_repaired_case = (
            refined.success
            and
            total_rel
            <
            1.0e-7
            and
            diagnostics[
                "acceleration_margin"
            ]
            >
            -1.0e-8
            and
            diagnostics[
                "leakage_violation"
            ]
            <
            1.0e-8
            and
            diagnostics[
                "nonnegative_violation"
            ]
            <
            1.0e-10
            and
            stored_inside_1e5
        )

        overall_provenance = (
            overall_provenance
            and
            provenance_repaired_case
        )

        overall_tomography = (
            overall_tomography
            and
            tomography_robust
        )

        print(
            f"CASE_DECISION "
            f"CASE={label} "
            f"STORED_INSIDE_1E5_ENVELOPE="
            f"{stored_inside_1e5} "
            f"MIN_ENVELOPE_W50="
            f"{min_w50:.9e} "
            f"MIN_ENVELOPE_W90="
            f"{min_w90:.9e} "
            f"TOMOGRAPHY_ROBUST="
            f"{tomography_robust} "
            f"PROVENANCE_REPAIRED_CASE="
            f"{provenance_repaired_case}"
        )

        case_summaries.append(
            {
                "label":
                label,

                "total_relerr":
                total_rel,

                "field_relerr":
                field_rel,

                "core_relerr":
                core_rel,

                "stored_inside_1e5":
                stored_inside_1e5,

                "min_w50":
                min_w50,

                "min_w90":
                min_w90,

                "tomography_robust":
                tomography_robust,

                "provenance_repaired":
                provenance_repaired_case,
            }
        )

    print()
    print(
        "=== R3D DECISION ==="
    )

    print(
        f"PROVENANCE_REPAIRED="
        f"{overall_provenance}"
    )

    print(
        f"ORDER_UNITY_TOMOGRAPHY_ROBUST="
        f"{overall_tomography}"
    )

    if (
        overall_provenance
        and
        overall_tomography
    ):

        classification = (
            "GREEN_R2R_PROVENANCE_REPAIRED_"
            "ORDER_UNITY_SELF_FIELD_ROBUST"
        )

        next_step = (
            "031A_R4_Z2_INDUCED_SCALARIZATION_"
            "FINITE_SOURCE_BVP"
        )

    elif overall_provenance:

        classification = (
            "YELLOW_PROVENANCE_REPAIRED_"
            "TOMOGRAPHY_NOT_ROBUST"
        )

        next_step = (
            "REOPTIMIZE_NONLINEAR_SOURCE_"
            "BEFORE_Z2_BVP"
        )

    else:

        classification = (
            "RED_R2R_PROVENANCE_NOT_REPAIRED"
        )

        next_step = (
            "DIAGNOSE_R2R_OPTIMIZER_OR_"
            "STORED_ARTIFACTS"
        )

    print(
        f"031A_R3D_CLASSIFICATION="
        f"{classification}"
    )

    print(
        f"NEXT="
        f"{next_step}"
    )

    import json

    summary = {
        "claim_class":
        "NUMERICAL_PROVENANCE_AND_TOMOGRAPHY_AUDIT",

        "practical_device":
        False,

        "microscopic_field":
        False,

        "provenance_repaired":
        overall_provenance,

        "order_unity_tomography_robust":
        overall_tomography,

        "cases":
        case_summaries,

        "near_opt_eps":
        list(
            NEAR_OPT_EPS
        ),

        "classification":
        classification,

        "next":
        next_step,
    }

    output = (
        RESULTS
        /
        "031a_r3d_r2r_provenance_degeneracy_summary.json"
    )

    output.write_text(
        json.dumps(
            summary,
            indent=2,
        )
        +
        "\n"
    )

    print(
        f"SUMMARY_JSON="
        f"{output.resolve()}"
    )


if __name__ == "__main__":
    main()
