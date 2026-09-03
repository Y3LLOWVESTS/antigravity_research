"""
031A-R3
=======

Nonlinear source-sensitivity, protected activation, and self-screening theorem
gate for Activated Scalar-Metric Charge Antigravity.

Purpose
-------
031A-R2R found finite-support one-sided scalar-charge configurations with
optimistic total energy below 1e11 J for:

    alpha_m = 10
    |alpha_X| = 5.623413251903491e16

including low-monopole and exactly net-neutral cases.

R2R nevertheless treated source scalar charge through the local algebraic bound

    |q_X| <= |alpha_X| E_X/c^2

without resolving the nonlinear dependence of E_X on the scalar field that
produces alpha_X.

This gate asks whether the successful R2R configuration already samples an
order-unity field excursion in the microscopic sensitivity scale, and whether
simple known protection/activation mechanisms survive cheap analytical tests.

This file is still a preflight.

It does NOT establish:

- a microscopic source;
- a B7 scalar dressing;
- a Q-ball/Q-shell source;
- a complete activation field;
- radiative stability;
- empirical viability;
- a practical antigravity device.

Scientific slices
-----------------

A. Reconstruct the R2R strong candidate including its actual optimized charge
   vector.

B. Reconstruct the scalar potential at every source basis element.

C. Test the exact charge-weighted field-excursion identity

       |<Delta phi / f_X>_Q| = 2 E_phi / E_X

   when the finite-sensitivity bound is saturated.

D. Quantify local exponential-source susceptibility / self-screening.

E. Test cheap source-dependence controls:

       exponential
       positive affine
       single-harmonic pNGB-like

F. Show that ordinary gravitational spontaneous scalarization is not a
   laboratory trigger at the R2R source compactness.

G. Test a standard density-driven symmetron activation geometry against the
   already-certified R1 Yukawa range penalties.

H. Translate the R2R target into a Z2 quadratic protected scaffold:

       A_m(phi) ~ exp(+phi^2 / 2 M_m^2)
       E_X(phi) ~ E_X0 exp(-phi^2 / 2 M_X^2)

   so that, for phi > 0,

       alpha_m = +Mpl phi / M_m^2
       alpha_X = -Mpl phi / M_X^2

   and therefore

       M_m^2 / M_X^2 = |alpha_X| / alpha_m.

   This is only a scaffold.  The next stage must solve its actual nonlinear
   finite-source field equation if this preflight survives.

Important convention
--------------------
The project uses

    phi / Mpl = -2 G psi / c^2

with psi in kg/m and

    f_X = Mpl / |alpha_X|.

Thus

    phi / f_X = -2 G |alpha_X| psi / c^2.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import linprog, minimize
from scipy.special import spherical_in


ROOT = Path(__file__).resolve().parents[1]

R2_PATH = (
    ROOT
    /
    "simulations"
    /
    "031a_r2r_finite_support_scalar_charge_pareto_gate.py"
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


G = 6.67430e-11
C = 299_792_458.0
G0 = 9.80665

MPL_REDUCED_GEV = 2.435e18

HBARC_EVM = 1.973269804e-7

EV_PER_J = 1.0 / 1.602176634e-19

J_M3_TO_EV4 = (
    EV_PER_J
    *
    HBARC_EVM**3
)

PRIMARY_ALPHA_M = 10.0

PRIMARY_ALPHA_X = 5.623413251903491e16

PRIMARY_LEAK = 0.10

NET_NEUTRAL_LEAK = 0.0

PREFERRED_RANGE_M = 3.30

TARGET_1TJ = 1.0e12

TARGET_1E11 = 1.0e11

PAYLOAD_DENSITIES_KG_M3 = (
    100.0,
    1000.0,
    8000.0,
)

COUPLING_VARIATION_TARGETS = (
    1.0,
    0.30,
    0.10,
    0.03,
)

ACTIVATION_RADII_M = (
    1.10,
    2.20,
    3.30,
    5.00,
    10.0,
    15.0,
)


def load_r2_module():

    if not R2_PATH.exists():

        raise RuntimeError(
            f"MISSING_R2_SOURCE={R2_PATH}"
        )

    spec = importlib.util.spec_from_file_location(
        "r2",
        R2_PATH,
    )

    if (
        spec is None
        or
        spec.loader is None
    ):

        raise RuntimeError(
            "R2_IMPORT_SPEC_FAILURE"
        )

    module = importlib.util.module_from_spec(
        spec
    )

    # Python 3.13 dataclasses resolves type metadata through the defining
    # module in sys.modules.  Dynamically loaded modules must therefore be
    # registered before exec_module().
    import sys
    sys.modules[spec.name] = module

    spec.loader.exec_module(
        module
    )

    return module


def read_expected_row(
    alpha_m: float,
    alpha_x: float,
    leak: float,
):

    with R2_CSV.open(
        newline="",
    ) as handle:

        rows = list(
            csv.DictReader(
                handle
            )
        )

    best = None

    for row in rows:

        if row["family"] != "unrestricted":
            continue

        if row["success"] != "True":
            continue

        if not math.isclose(
            float(
                row["alpha_m"]
            ),
            alpha_m,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ):
            continue

        if not math.isclose(
            float(
                row["alpha_x"]
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

        best = row

        break

    if best is None:

        raise RuntimeError(
            "EXPECTED_R2_ROW_NOT_FOUND"
        )

    return {
        key: (
            value
            if key
            in {
                "message",
                "family",
            }
            else (
                value
                ==
                "True"
                if key
                ==
                "success"
                else float(
                    value
                )
            )
        )
        for key, value
        in best.items()
    }


def weighted_quantile(
    values,
    weights,
    quantile,
):

    values = np.asarray(
        values,
        dtype=float,
    )

    weights = np.asarray(
        weights,
        dtype=float,
    )

    mask = (
        np.isfinite(
            values
        )
        &
        np.isfinite(
            weights
        )
        &
        (
            weights
            >
            0.0
        )
    )

    values = values[
        mask
    ]

    weights = weights[
        mask
    ]

    if len(
        values
    ) == 0:

        return math.nan

    order = np.argsort(
        values
    )

    values = values[
        order
    ]

    weights = weights[
        order
    ]

    cumulative = np.cumsum(
        weights
    )

    target = (
        quantile
        *
        cumulative[
            -1
        ]
    )

    index = int(
        np.searchsorted(
            cumulative,
            target,
            side="left",
        )
    )

    index = min(
        index,
        len(
            values
        )
        -
        1,
    )

    return float(
        values[
            index
        ]
    )


def solve_vector(
    r2,
    geometry,
    alpha_m,
    alpha_x,
    leakage_fraction,
):

    field_kernel = geometry[
        "field_kernel"
    ]

    acceleration_geometry = geometry[
        "acceleration_geometry"
    ]

    number_basis = len(
        acceleration_geometry
    )

    charge_reference = (
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

    field_energy_scale = (
        r2.G
        *
        charge_reference**2
        /
        r2.TARGET_1TJ
    )

    core_energy_scale = (
        r2.C**2
        *
        charge_reference
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

    total_acceleration_row = np.concatenate(
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
        number_basis
    )

    net_charge_row = np.concatenate(
        (
            ones,
            -ones,
        )
    )

    absolute_charge_row = np.concatenate(
        (
            ones,
            ones,
        )
    )

    linear_ub = [
        -total_acceleration_row
    ]

    linear_ub_rhs = [
        -1.0
    ]

    linear_eq = None

    linear_eq_rhs = None

    if leakage_fraction == 0.0:

        linear_eq = [
            net_charge_row
        ]

        linear_eq_rhs = [
            0.0
        ]

    elif leakage_fraction < 1.0:

        linear_ub.extend(
            [
                (
                    net_charge_row
                    -
                    leakage_fraction
                    *
                    absolute_charge_row
                ),
                (
                    -net_charge_row
                    -
                    leakage_fraction
                    *
                    absolute_charge_row
                ),
            ]
        )

        linear_ub_rhs.extend(
            [
                0.0,
                0.0,
            ]
        )

    feasibility = linprog(
        absolute_charge_row,
        A_ub=np.asarray(
            linear_ub
        ),
        b_ub=np.asarray(
            linear_ub_rhs
        ),
        A_eq=(
            None
            if linear_eq is None
            else np.asarray(
                linear_eq
            )
        ),
        b_eq=(
            None
            if linear_eq_rhs is None
            else np.asarray(
                linear_eq_rhs
            )
        ),
        bounds=[
            (
                0.0,
                None,
            )
        ]
        *
        (
            2
            *
            number_basis
        ),
        method="highs",
    )

    if not feasibility.success:

        raise RuntimeError(
            "R3_LINEAR_FEASIBILITY_FAILURE"
        )

    def objective(
        vector,
    ):

        positive = vector[
            :number_basis
        ]

        negative = vector[
            number_basis:
        ]

        signed = (
            positive
            -
            negative
        )

        absolute = (
            positive
            +
            negative
        )

        return (
            field_energy_scale
            *
            float(
                signed
                @
                field_kernel
                @
                signed
            )
            +
            core_energy_scale
            *
            float(
                np.sum(
                    absolute
                )
            )
        )

    def gradient(
        vector,
    ):

        positive = vector[
            :number_basis
        ]

        negative = vector[
            number_basis:
        ]

        signed = (
            positive
            -
            negative
        )

        field_gradient = (
            2.0
            *
            field_energy_scale
            *
            (
                field_kernel
                @
                signed
            )
        )

        return np.concatenate(
            (
                field_gradient
                +
                core_energy_scale,
                -field_gradient
                +
                core_energy_scale,
            )
        )

    constraints = [
        {
            "type":
            "ineq",

            "fun":
            (
                lambda vector,
                row=total_acceleration_row:
                float(
                    row
                    @
                    vector
                    -
                    1.0
                )
            ),

            "jac":
            (
                lambda vector,
                row=total_acceleration_row:
                row
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
                    lambda vector,
                    row=net_charge_row:
                    float(
                        row
                        @
                        vector
                    )
                ),

                "jac":
                (
                    lambda vector,
                    row=net_charge_row:
                    row
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
                        lambda vector,
                        qrow=net_charge_row,
                        arow=absolute_charge_row,
                        fraction=leakage_fraction:
                        float(
                            fraction
                            *
                            (
                                arow
                                @
                                vector
                            )
                            -
                            (
                                qrow
                                @
                                vector
                            )
                        )
                    ),

                    "jac":
                    (
                        lambda vector,
                        qrow=net_charge_row,
                        arow=absolute_charge_row,
                        fraction=leakage_fraction:
                        (
                            fraction
                            *
                            arow
                            -
                            qrow
                        )
                    ),
                },
                {
                    "type":
                    "ineq",

                    "fun":
                    (
                        lambda vector,
                        qrow=net_charge_row,
                        arow=absolute_charge_row,
                        fraction=leakage_fraction:
                        float(
                            fraction
                            *
                            (
                                arow
                                @
                                vector
                            )
                            +
                            (
                                qrow
                                @
                                vector
                            )
                        )
                    ),

                    "jac":
                    (
                        lambda vector,
                        qrow=net_charge_row,
                        arow=absolute_charge_row,
                        fraction=leakage_fraction:
                        (
                            fraction
                            *
                            arow
                            +
                            qrow
                        )
                    ),
                },
            ]
        )

    optimized = minimize(
        objective,
        feasibility.x,
        jac=gradient,
        method="SLSQP",
        bounds=[
            (
                0.0,
                None,
            )
        ]
        *
        (
            2
            *
            number_basis
        ),
        constraints=constraints,
        options={
            "ftol":
            1.0e-11,

            "maxiter":
            1800,

            "disp":
            False,
        },
    )

    if not optimized.success:

        raise RuntimeError(
            "R3_VECTOR_OPTIMIZATION_FAILURE: "
            +
            str(
                optimized.message
            )
        )

    vector = optimized.x

    positive = vector[
        :number_basis
    ]

    negative = vector[
        number_basis:
    ]

    signed = (
        positive
        -
        negative
    )

    absolute = (
        positive
        +
        negative
    )

    q_signed = (
        charge_reference
        *
        signed
    )

    q_absolute = (
        charge_reference
        *
        absolute
    )

    psi = (
        field_kernel
        @
        q_signed
    )

    e_field = (
        r2.G
        *
        float(
            q_signed
            @
            field_kernel
            @
            q_signed
        )
    )

    q_abs_total = float(
        np.sum(
            q_absolute
        )
    )

    e_core = (
        r2.C**2
        *
        q_abs_total
        /
        alpha_x
    )

    e_total = (
        e_field
        +
        e_core
    )

    q_net = float(
        np.sum(
            q_signed
        )
    )

    return {
        "vector":
        vector,

        "positive":
        positive,

        "negative":
        negative,

        "signed":
        signed,

        "absolute":
        absolute,

        "q_signed":
        q_signed,

        "q_absolute":
        q_absolute,

        "psi":
        psi,

        "charge_reference":
        charge_reference,

        "E_field_J":
        e_field,

        "E_core_J":
        e_core,

        "E_total_J":
        e_total,

        "Qabs_kg":
        q_abs_total,

        "Qnet_kg":
        q_net,

        "monopole_fraction":
        (
            abs(
                q_net
            )
            /
            q_abs_total
        ),
    }


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


def payload_factor(
    mu,
    payload_radius,
):

    x = (
        mu
        *
        payload_radius
    )

    if abs(
        x
    ) < 1.0e-8:

        return 1.0

    return float(
        3.0
        *
        spherical_in(
            1,
            x,
        )
        /
        x
    )


def r1_range_penalties(
    lambda_over_d,
    d,
    payload_radius,
):

    lambda_m = (
        lambda_over_d
        *
        d
    )

    mu = (
        1.0
        /
        lambda_m
    )

    x = (
        mu
        *
        d
    )

    fp = payload_factor(
        mu,
        payload_radius,
    )

    energy_ratio = (
        math.exp(
            2.0
            *
            x
        )
        /
        (
            2.0
            *
            x**2
            +
            2.0
            *
            x
            +
            1.0
        )
        /
        fp**2
    )

    charge_ratio = (
        math.exp(
            x
        )
        /
        (
            (
                1.0
                +
                x
            )
            *
            fp
        )
    )

    return (
        energy_ratio,
        charge_ratio,
    )


def symmetron_sphere_screening(
    x,
):

    if abs(
        x
    ) < 1.0e-5:

        return (
            1.0
            -
            0.4
            *
            x**2
        )

    return (
        3.0
        *
        (
            1.0
            -
            math.tanh(
                x
            )
            /
            x
        )
        /
        x**2
    )


def analyze_candidate(
    r2,
    geometry,
    leak,
    label,
):

    expected = read_expected_row(
        PRIMARY_ALPHA_M,
        PRIMARY_ALPHA_X,
        leak,
    )

    solved = solve_vector(
        r2,
        geometry,
        PRIMARY_ALPHA_M,
        PRIMARY_ALPHA_X,
        leak,
    )

    energy_relerr = relerr(
        solved[
            "E_total_J"
        ],
        expected[
            "E_total_J"
        ],
    )

    field_relerr = relerr(
        solved[
            "E_field_J"
        ],
        expected[
            "E_field_J"
        ],
    )

    core_relerr = relerr(
        solved[
            "E_core_J"
        ],
        expected[
            "E_core_J"
        ],
    )

    provenance_pass = (
        energy_relerr
        <
        5.0e-6
        and
        field_relerr
        <
        5.0e-6
        and
        core_relerr
        <
        5.0e-6
    )

    print(
        f"R2_VECTOR_RECONSTRUCTION "
        f"CASE={label} "
        f"E_RELERR={energy_relerr:.9e} "
        f"FIELD_RELERR={field_relerr:.9e} "
        f"CORE_RELERR={core_relerr:.9e} "
        f"PASS={provenance_pass}"
    )

    f_x_gev = (
        MPL_REDUCED_GEV
        /
        PRIMARY_ALPHA_X
    )

    psi = solved[
        "psi"
    ]

    signed = solved[
        "signed"
    ]

    q_absolute = solved[
        "q_absolute"
    ]

    sign = np.sign(
        signed
    )

    z = (
        -2.0
        *
        G
        *
        PRIMARY_ALPHA_X
        *
        psi
        /
        C**2
    )

    w = (
        sign
        *
        z
    )

    weight = (
        q_absolute
    )

    active = (
        weight
        >
        0.0
    )

    weighted_mean_w = float(
        np.sum(
            weight
            *
            w
        )
        /
        np.sum(
            weight
        )
    )

    identity_rhs = (
        -2.0
        *
        solved[
            "E_field_J"
        ]
        /
        solved[
            "E_core_J"
        ]
    )

    identity_relerr = relerr(
        weighted_mean_w,
        identity_rhs,
    )

    abs_w = np.abs(
        w
    )

    w50 = weighted_quantile(
        abs_w,
        weight,
        0.50,
    )

    w90 = weighted_quantile(
        abs_w,
        weight,
        0.90,
    )

    w99 = weighted_quantile(
        abs_w,
        weight,
        0.99,
    )

    wmax = float(
        np.max(
            abs_w[
                active
            ]
        )
    )

    frac_gt_03 = float(
        np.sum(
            weight[
                abs_w
                >
                0.30
            ]
        )
        /
        np.sum(
            weight
        )
    )

    frac_gt_1 = float(
        np.sum(
            weight[
                abs_w
                >
                1.0
            ]
        )
        /
        np.sum(
            weight
        )
    )

    frac_gt_pi2 = float(
        np.sum(
            weight[
                abs_w
                >
                (
                    math.pi
                    /
                    2.0
                )
            ]
        )
        /
        np.sum(
            weight
        )
    )

    print(
        f"FIELD_EXCURSION "
        f"CASE={label} "
        f"MEAN_SIGNED_W={weighted_mean_w:.9e} "
        f"IDENTITY_RHS={identity_rhs:.9e} "
        f"IDENTITY_RELERR={identity_relerr:.9e} "
        f"ABS_W50={w50:.9e} "
        f"ABS_W90={w90:.9e} "
        f"ABS_W99={w99:.9e} "
        f"ABS_WMAX={wmax:.9e} "
        f"QFRAC_GT_0P3={frac_gt_03:.9e} "
        f"QFRAC_GT_1={frac_gt_1:.9e} "
        f"QFRAC_GT_PI_OVER_2={frac_gt_pi2:.9e}"
    )

    blob_volume = (
        4.0
        *
        math.pi
        *
        r2.BLOB_RADIUS**3
        /
        3.0
    )

    basis_volumes = np.asarray(
        [
            item[
                "nphi"
            ]
            *
            blob_volume
            for item
            in geometry[
                "metadata"
            ]
        ],
        dtype=float,
    )

    core_energy_basis = (
        C**2
        *
        q_absolute
        /
        PRIMARY_ALPHA_X
    )

    core_density = np.zeros_like(
        core_energy_basis
    )

    core_density[
        active
    ] = (
        core_energy_basis[
            active
        ]
        /
        basis_volumes[
            active
        ]
    )

    ell_exp = np.full_like(
        core_density,
        np.inf,
    )

    ell_exp[
        active
    ] = (
        C**2
        /
        np.sqrt(
            8.0
            *
            math.pi
            *
            G
            *
            PRIMARY_ALPHA_X**2
            *
            core_density[
                active
            ]
        )
    )

    ell50 = weighted_quantile(
        ell_exp,
        weight,
        0.50,
    )

    ell10 = weighted_quantile(
        ell_exp,
        weight,
        0.10,
    )

    ell90 = weighted_quantile(
        ell_exp,
        weight,
        0.90,
    )

    print(
        f"EXPONENTIAL_SUSCEPTIBILITY "
        f"CASE={label} "
        f"ELL10_M={ell10:.9e} "
        f"ELL50_M={ell50:.9e} "
        f"ELL90_M={ell90:.9e} "
        f"BLOB_RADIUS_M={r2.BLOB_RADIUS:.9e} "
        f"ELL50_OVER_BLOB="
        f"{ell50/r2.BLOB_RADIUS:.9e}"
    )

    affine_bad_fraction = float(
        np.sum(
            weight[
                (
                    1.0
                    +
                    w
                )
                <=
                0.0
            ]
        )
        /
        np.sum(
            weight
        )
    )

    pngb_bad_fraction = float(
        np.sum(
            weight[
                w
                <=
                -math.pi
                /
                2.0
            ]
        )
        /
        np.sum(
            weight
        )
    )

    print(
        f"SIMPLE_PROTECTION_CONTROLS "
        f"CASE={label} "
        f"AFFINE_NONPOSITIVE_QFRAC="
        f"{affine_bad_fraction:.9e} "
        f"PNGB_SINGLE_HARMONIC_ZERO_CROSS_QFRAC="
        f"{pngb_bad_fraction:.9e} "
        f"EXPONENTIAL_CONSTANT_SENSITIVITY=YES "
        f"EXPONENTIAL_CURVATURE_SCREENING=YES"
    )

    return {
        "label":
        label,

        "expected":
        expected,

        "solved":
        solved,

        "provenance_pass":
        provenance_pass,

        "f_x_gev":
        f_x_gev,

        "weighted_mean_w":
        weighted_mean_w,

        "identity_rhs":
        identity_rhs,

        "identity_relerr":
        identity_relerr,

        "w50":
        w50,

        "w90":
        w90,

        "w99":
        w99,

        "wmax":
        wmax,

        "frac_gt_03":
        frac_gt_03,

        "frac_gt_1":
        frac_gt_1,

        "frac_gt_pi2":
        frac_gt_pi2,

        "ell10":
        ell10,

        "ell50":
        ell50,

        "ell90":
        ell90,

        "affine_bad_fraction":
        affine_bad_fraction,

        "pngb_bad_fraction":
        pngb_bad_fraction,

        "basis_volumes":
        basis_volumes,

        "core_density":
        core_density,
    }


def main():

    print(
        "=== 031A-R3 NONLINEAR SOURCE-SENSITIVITY "
        "+ PROTECTED ACTIVATION GATE ==="
    )

    print(
        "CLAIM_CLASS="
        "THEOREM_AND_PROTECTION_PREFLIGHT"
    )

    print(
        "MICROSCOPIC_FIELD="
        "NO"
    )

    print(
        "PRACTICAL_DEVICE="
        "NO"
    )

    r2 = load_r2_module()

    geometry = r2.build_geometry(
        r2.MEDIUM
    )

    print(
        "\n=== A — R2R PROVENANCE + "
        "LOCAL FIELD TOMOGRAPHY ==="
    )

    strong = analyze_candidate(
        r2,
        geometry,
        PRIMARY_LEAK,
        "MONO_LE_0P1",
    )

    neutral = analyze_candidate(
        r2,
        geometry,
        NET_NEUTRAL_LEAK,
        "NET_NEUTRAL",
    )

    provenance_pass = (
        strong[
            "provenance_pass"
        ]
        and
        neutral[
            "provenance_pass"
        ]
        and
        strong[
            "identity_relerr"
        ]
        <
        1.0e-8
        and
        neutral[
            "identity_relerr"
        ]
        <
        1.0e-8
    )

    print(
        f"R3_PROVENANCE_PASS="
        f"{provenance_pass}"
    )

    print(
        "\n=== B — LARGE-SENSITIVITY "
        "MICROSCOPIC SCALE ==="
    )

    f_x_gev = (
        MPL_REDUCED_GEV
        /
        PRIMARY_ALPHA_X
    )

    m_phi_ev = (
        HBARC_EVM
        /
        PREFERRED_RANGE_M
    )

    cw_low_ev = math.sqrt(
        2.0
        *
        math.pi
        *
        m_phi_ev
        *
        f_x_gev
        *
        1.0e9
    )

    cw_high_ev = math.sqrt(
        4.0
        *
        math.pi
        *
        m_phi_ev
        *
        f_x_gev
        *
        1.0e9
    )

    print(
        f"FX_GEV="
        f"{f_x_gev:.15e}"
    )

    print(
        f"TARGET_MEDIATOR_MASS_EV="
        f"{m_phi_ev:.15e}"
    )

    print(
        f"UNPROTECTED_CW_CARRIER_MAX_LOW_EV="
        f"{cw_low_ev:.15e}"
    )

    print(
        f"UNPROTECTED_CW_CARRIER_MAX_HIGH_EV="
        f"{cw_high_ev:.15e}"
    )

    print(
        "UNPROTECTED_HEAVY_DIRECT_SOURCE="
        "RED_WITHOUT_ADDITIONAL_PROTECTION"
    )

    print(
        "\n=== C — GRAVITY-INDUCED "
        "SPONTANEOUS SCALARIZATION CONTROL ==="
    )

    source_mass_kg = (
        strong[
            "solved"
        ][
            "E_core_J"
        ]
        /
        C**2
    )

    source_compactness = (
        G
        *
        source_mass_kg
        /
        (
            r2.D
            *
            C**2
        )
    )

    reference_compactness = (
        0.10
    )

    compactness_gap = (
        reference_compactness
        /
        source_compactness
    )

    print(
        f"R2_SOURCE_MASS_EQUIV_KG="
        f"{source_mass_kg:.15e}"
    )

    print(
        f"R2_SOURCE_COMPACTNESS="
        f"{source_compactness:.15e}"
    )

    print(
        f"REFERENCE_STRONG_FIELD_COMPACTNESS="
        f"{reference_compactness:.15e}"
    )

    print(
        f"COMPACTNESS_GAP_TO_STRONG_FIELD="
        f"{compactness_gap:.15e}"
    )

    print(
        "STANDARD_GRAVITY_INDUCED_SCALARIZATION="
        "RED_AS_LAB_TRIGGER"
    )

    print(
        "\n=== D — STANDARD DENSITY-DRIVEN "
        "SYMMETRON CAVITY TEST ==="
    )

    strong_e_field = (
        strong[
            "solved"
        ][
            "E_field_J"
        ]
    )

    strong_e_core = (
        strong[
            "solved"
        ][
            "E_core_J"
        ]
    )

    first_1tj_radius = None

    first_1e11_radius = None

    for radius in ACTIVATION_RADII_M:

        lambda_max = (
            radius
            /
            (
                math.pi
                *
                math.sqrt(
                    2.0
                )
            )
        )

        lambda_over_d = (
            lambda_max
            /
            r2.D
        )

        (
            energy_penalty,
            charge_penalty,
        ) = r1_range_penalties(
            lambda_over_d,
            r2.D,
            r2.PAYLOAD_RADIUS,
        )

        optimistic_total = (
            strong_e_field
            *
            energy_penalty
            +
            strong_e_core
            *
            charge_penalty
        )

        if (
            first_1tj_radius
            is None
            and
            optimistic_total
            <=
            TARGET_1TJ
        ):

            first_1tj_radius = radius

        if (
            first_1e11_radius
            is None
            and
            optimistic_total
            <=
            TARGET_1E11
        ):

            first_1e11_radius = radius

        print(
            f"SYMMETRON_CAVITY "
            f"R_ACT_M={radius:.9e} "
            f"LAMBDA_MAX_M={lambda_max:.9e} "
            f"LAMBDA_OVER_D={lambda_over_d:.9e} "
            f"E_PENALTY={energy_penalty:.9e} "
            f"Q_PENALTY={charge_penalty:.9e} "
            f"OPTIMISTIC_TOTAL_J="
            f"{optimistic_total:.9e}"
        )

    print(
        f"SYMMETRON_FIRST_DECLARED_RADIUS_LE_1TJ_M="
        f"{first_1tj_radius}"
    )

    print(
        f"SYMMETRON_FIRST_DECLARED_RADIUS_LE_1E11_M="
        f"{first_1e11_radius}"
    )

    long_range_critical_radius = (
        math.pi
        *
        math.sqrt(
            2.0
        )
        *
        PREFERRED_RANGE_M
    )

    print(
        f"SYMMETRON_RCRIT_FOR_3P3M_RANGE_M="
        f"{long_range_critical_radius:.15e}"
    )

    print(
        "\n=== E — Z2 QUADRATIC "
        "OPPOSITE-CHARGE SCAFFOLD ==="
    )

    ratio = (
        PRIMARY_ALPHA_X
        /
        PRIMARY_ALPHA_M
    )

    total_support_volume = float(
        np.sum(
            strong[
                "basis_volumes"
            ]
        )
    )

    delta_phi_90_gev = (
        strong[
            "w90"
        ]
        *
        f_x_gev
    )

    print(
        f"ALPHA_X_OVER_ALPHA_M="
        f"{ratio:.15e}"
    )

    print(
        f"R2_QWEIGHTED_DELTA_PHI90_GEV="
        f"{delta_phi_90_gev:.15e}"
    )

    z2_rows = []

    for allowed_fraction in COUPLING_VARIATION_TARGETS:

        phi0_gev = (
            delta_phi_90_gev
            /
            allowed_fraction
        )

        m_x_gev = math.sqrt(
            phi0_gev
            *
            MPL_REDUCED_GEV
            /
            PRIMARY_ALPHA_X
        )

        m_m_gev = math.sqrt(
            phi0_gev
            *
            MPL_REDUCED_GEV
            /
            PRIMARY_ALPHA_M
        )

        ratio_reconstruction = (
            m_m_gev**2
            /
            m_x_gev**2
        )

        active_density = strong[
            "core_density"
        ]

        positive_density = active_density[
            active_density
            >
            0.0
        ]

        weights_density = strong[
            "solved"
        ][
            "q_absolute"
        ][
            active_density
            >
            0.0
        ]

        local_ell = (
            HBARC_EVM
            *
            m_x_gev
            *
            1.0e9
            /
            np.sqrt(
                positive_density
                *
                J_M3_TO_EV4
            )
        )

        ell10 = weighted_quantile(
            local_ell,
            weights_density,
            0.10,
        )

        ell50 = weighted_quantile(
            local_ell,
            weights_density,
            0.50,
        )

        ell90 = weighted_quantile(
            local_ell,
            weights_density,
            0.90,
        )

        phi0_ev = (
            phi0_gev
            *
            1.0e9
        )

        positive_mass_term_ev4 = (
            0.5
            *
            m_phi_ev**2
            *
            phi0_ev**2
        )

        positive_mass_term_j_m3 = (
            positive_mass_term_ev4
            /
            J_M3_TO_EV4
        )

        e_mass_support = (
            positive_mass_term_j_m3
            *
            total_support_volume
        )

        activation_ball_volume = (
            4.0
            *
            math.pi
            *
            r2.D**3
            /
            3.0
        )

        e_mass_d_ball = (
            positive_mass_term_j_m3
            *
            activation_ball_volume
        )

        m_x_ev = (
            m_x_gev
            *
            1.0e9
        )

        cw_quad_low = math.sqrt(
            2.0
            *
            math.pi
            *
            m_phi_ev
            *
            m_x_ev
        )

        cw_quad_high = math.sqrt(
            4.0
            *
            math.pi
            *
            m_phi_ev
            *
            m_x_ev
        )

        payload_screening = {}

        for density_kg_m3 in PAYLOAD_DENSITIES_KG_M3:

            density_energy_ev4 = (
                density_kg_m3
                *
                C**2
                *
                J_M3_TO_EV4
            )

            payload_radius_evinv = (
                r2.PAYLOAD_RADIUS
                /
                HBARC_EVM
            )

            x_payload = (
                payload_radius_evinv
                *
                math.sqrt(
                    density_energy_ev4
                )
                /
                (
                    m_m_gev
                    *
                    1.0e9
                )
            )

            screen = symmetron_sphere_screening(
                x_payload
            )

            payload_screening[
                density_kg_m3
            ] = screen

        classical_window = (
            ell50
            >
            r2.BLOB_RADIUS
            and
            e_mass_support
            <
            TARGET_1E11
            and
            min(
                payload_screening.values()
            )
            >
            0.90
        )

        row = {
            "allowed_fraction":
            allowed_fraction,

            "phi0_gev":
            phi0_gev,

            "M_X_gev":
            m_x_gev,

            "M_m_gev":
            m_m_gev,

            "ratio_reconstruction":
            ratio_reconstruction,

            "ell10_m":
            ell10,

            "ell50_m":
            ell50,

            "ell90_m":
            ell90,

            "positive_mass_term_j_m3":
            positive_mass_term_j_m3,

            "positive_mass_term_support_j":
            e_mass_support,

            "positive_mass_term_d_ball_j":
            e_mass_d_ball,

            "cw_quad_low_ev":
            cw_quad_low,

            "cw_quad_high_ev":
            cw_quad_high,

            "payload_screening":
            payload_screening,

            "classical_window":
            classical_window,
        }

        z2_rows.append(
            row
        )

        print(
            f"Z2_SCAFFOLD "
            f"MAX_FRAC_VARIATION="
            f"{allowed_fraction:.9e} "
            f"PHI0_GEV={phi0_gev:.9e} "
            f"M_X_GEV={m_x_gev:.9e} "
            f"M_M_GEV={m_m_gev:.9e} "
            f"RATIO_RECON="
            f"{ratio_reconstruction:.9e} "
            f"ELL10_M={ell10:.9e} "
            f"ELL50_M={ell50:.9e} "
            f"ELL90_M={ell90:.9e} "
            f"E_MASS_SUPPORT_J="
            f"{e_mass_support:.9e} "
            f"E_MASS_DBALL_J="
            f"{e_mass_d_ball:.9e} "
            f"CW_CARRIER_LOW_EV="
            f"{cw_quad_low:.9e} "
            f"CW_CARRIER_HIGH_EV="
            f"{cw_quad_high:.9e} "
            f"SCREEN_RHO100="
            f"{payload_screening[100.0]:.9e} "
            f"SCREEN_RHO1000="
            f"{payload_screening[1000.0]:.9e} "
            f"SCREEN_RHO8000="
            f"{payload_screening[8000.0]:.9e} "
            f"CLASSICAL_WINDOW="
            f"{classical_window}"
        )

    z2_classical_survivor = any(
        row[
            "classical_window"
        ]
        for row
        in z2_rows
    )

    print(
        f"Z2_CLASSICAL_PREFLIGHT_SURVIVOR="
        f"{z2_classical_survivor}"
    )

    print(
        "\n=== F — DECISION ==="
    )

    nonlinear_required = (
        strong[
            "w90"
        ]
        >
        0.30
    )

    order_unity_excursion = (
        strong[
            "w50"
        ]
        >
        0.50
        or
        abs(
            strong[
                "weighted_mean_w"
            ]
        )
        >
        1.0
    )

    print(
        f"NONLINEAR_SOURCE_DEPENDENCE_REQUIRED="
        f"{nonlinear_required}"
    )

    print(
        f"ORDER_UNITY_SOURCE_FIELD_EXCURSION="
        f"{order_unity_excursion}"
    )

    print(
        "DERIVATIVE_ONLY_SHIFT_SYMMETRY_STATIC_CHARGE="
        "ZERO_WITHOUT_SHIFT_BREAKING"
    )

    print(
        "SINGLE_HARMONIC_PNGB_PROTECTION="
        "DIAGNOSTIC_ONLY_NOT_PROMOTED"
    )

    print(
        "STANDARD_GRAVITY_SCALARIZATION="
        "DEMOTED_FOR_LAB_SOURCE"
    )

    if not provenance_pass:

        classification = (
            "RED_R2_PROVENANCE_RECONSTRUCTION_FAILURE"
        )

        next_step = (
            "DIAGNOSE_R2R_BEFORE_NEW_PHYSICS"
        )

    elif not nonlinear_required:

        classification = (
            "GREEN_LINEAR_SENSITIVITY_APPROXIMATION_SURVIVES"
        )

        next_step = (
            "031B1_FIXED_FIELD_B7_SCALAR_CHARGE_TOMOGRAPHY"
        )

    elif z2_classical_survivor:

        classification = (
            "YELLOW_Z2_PROTECTED_INDUCED_SCALARIZATION_"
            "SURVIVES_CLASSICAL_PREFLIGHT_"
            "QUANTUM_PROTECTION_UNRESOLVED"
        )

        next_step = (
            "031A_R4_Z2_INDUCED_SCALARIZATION_"
            "FINITE_SOURCE_BVP"
        )

    else:

        classification = (
            "RED_SIMPLE_PROTECTED_ACTIVATION_SCAFFOLDS"
        )

        next_step = (
            "031_GLOBAL_RERANK_BEFORE_MICROSCOPIC_PDE"
        )

    print(
        f"031A_R3_CLASSIFICATION="
        f"{classification}"
    )

    print(
        f"NEXT="
        f"{next_step}"
    )

    summary = {
        "claim_class":
        "THEOREM_AND_PROTECTION_PREFLIGHT",

        "practical_device":
        False,

        "microscopic_field":
        False,

        "r2_provenance_pass":
        provenance_pass,

        "strong_candidate": {
            "E_total_J":
            strong[
                "solved"
            ][
                "E_total_J"
            ],

            "E_field_J":
            strong[
                "solved"
            ][
                "E_field_J"
            ],

            "E_core_J":
            strong[
                "solved"
            ][
                "E_core_J"
            ],

            "monopole_fraction":
            strong[
                "solved"
            ][
                "monopole_fraction"
            ],

            "w50":
            strong[
                "w50"
            ],

            "w90":
            strong[
                "w90"
            ],

            "w99":
            strong[
                "w99"
            ],

            "wmax":
            strong[
                "wmax"
            ],

            "weighted_mean_w":
            strong[
                "weighted_mean_w"
            ],

            "ell50_exponential_m":
            strong[
                "ell50"
            ],
        },

        "f_x_gev":
        f_x_gev,

        "unprotected_cw_carrier_low_ev":
        cw_low_ev,

        "unprotected_cw_carrier_high_ev":
        cw_high_ev,

        "source_compactness":
        source_compactness,

        "strong_field_compactness_reference":
        reference_compactness,

        "symmetron_rcrit_3p3m_m":
        long_range_critical_radius,

        "z2_classical_survivor":
        z2_classical_survivor,

        "z2_rows":
        z2_rows,

        "classification":
        classification,

        "next":
        next_step,

        "claim_limits": [
            "No microscopic source solved.",
            "No activation PDE solved.",
            "No radiative protection established.",
            "No empirical fifth-force closure established.",
            "Negative interaction energy is not credited as a practical energy saving.",
            "Z2 scaffold results are only classical parameter translations.",
        ],
    }

    summary_path = (
        RESULTS
        /
        "031a_r3_nonlinear_protected_activation_summary.json"
    )

    summary_path.write_text(
        json.dumps(
            summary,
            indent=2,
        )
        +
        "\n"
    )

    print(
        f"SUMMARY_JSON="
        f"{summary_path.resolve()}"
    )


if __name__ == "__main__":
    main()
