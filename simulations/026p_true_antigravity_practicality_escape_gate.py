#!/usr/bin/env python3
"""026P — TRUE-ANTIGRAVITY PRACTICALITY ESCAPE GATE.

PURPOSE
=======
This is a final-session decision experiment.

It is NOT another unconstrained source optimization and NOT an analogue-force
study.

It uses the project's two strongest strict microscopic true-antigravity field
realizations:

    N=73
    N=81

for the false-core

    B=7
    eta=0.4
    m=8

Skyrmion.

The central question is:

    Given the actual microscopic energy density and active-stress budget now
    demonstrated by the B7 field, what is the largest true stand-off outward
    gravitational response that could be obtained through ideal spatial
    organization and DEC-compatible stress organization?

Then:

    Is that improvement remotely sufficient to overcome the absolute 1/G
    energy scale required for practical macroscopic gravity?

This separates two bottlenecks:

    A. SOURCE-ORGANIZATION GAP

    B. FUNDAMENTAL ABSOLUTE-SCALING GAP

The run is intended to identify the highest-information path for future
TRUE ANTIGRAVITY work.

It does NOT claim to build a practical device.


BACKGROUND
==========

For a static weak-field source, the slow neutral-matter active density is

    S = rho + Tr(T).

For a type-I stress tensor satisfying DEC,

    -rho <= p_i <= rho,

so

    -2 rho <= S <= 4 rho.

For an isolated exactly stationary conserved source, the Laue condition gives

    integral T_ij dV = 0,

and therefore ideally

    integral S dV = integral rho dV.

This is crucial.

Negative active density cannot fill the whole source.  It has to be balanced by
positive-active support.

For an outside payload all source cells lie behind the payload, so the radial
Newton/linearized-GR kernel is negative.

Outward gravity therefore comes from

    S < 0
    K < 0
    S K > 0.

Ordinary positive active mass gives

    S > 0
    K < 0
    S K < 0.

The ideal static DEC source therefore wants:

    strong negative S where |K| is large;
    compensating positive S where |K| is small.


THREE SOURCE-ORGANIZATION LEVELS
================================

LEVEL 0 — ACTUAL MICROSCOPIC FIELD

Use the exact reconstructed B7

    rho(x)
    S(x)

without modification.

LEVEL 1 — PACKET-RELOCATION UPPER BOUND

Keep the complete multiset of actual microscopic active-density packets S_i,
but permit them to be spatially rearranged arbitrarily inside the existing
99.9%-energy support.

This preserves the amount of negative and positive active source already
present in the actual field.

It deliberately ignores microscopic field compatibility and therefore is an
UPPER BOUND on what geometry alone could achieve.

By the rearrangement inequality, the maximum of

    sum_i S_i K_i

is obtained by similarly sorting S and K.

LEVEL 2 — FIXED-rho DEC + LAUE UPPER BOUND

Freeze the ACTUAL microscopic energy density rho_i at every position.

Permit the local active source to range over the full DEC interval

    -2 rho_i <= S_i <= 4 rho_i

while imposing either:

    integral S = integral rho

for the ideal static Laue target, or

    integral S = current active mass

as a sensitivity control.

This is solved exactly as a bounded linear program.

Because the objective is linear, the solution is bang-bang:

    S = -2 rho

in the largest-|K| productive region, and

    S = +4 rho

where the kernel penalty is smallest, with at most one partially filled
transition cell.

This is deliberately optimistic.

It is NOT automatically a locally conserved realizable field.

Its purpose is to measure the maximum remaining microscopic stress-organization
headroom associated with the ACTUAL B7 energy density.


TRUE STAND-OFF SUPPORT
======================

The source is truncated only for this extremal bound to the radius containing
99.9% of the microscopic energy:

    R999.

Payload centers are placed at

    1.10 R999
    1.25 R999
    1.50 R999
    2.00 R999.

Thus the optimization cannot obtain fake outward gravity by putting ordinary
positive active source beyond the payload.

The exact rectangular-prism Green-function kernel previously validated by the
project is used.


PRACTICALITY SCALING
====================

The project linearized-GR scaling is

    E = C a c^2 h^2 / G.

This run does NOT assume C=1 is a fundamental lower bound.

Instead it asks:

    What value of C would actually be required to achieve selected acceleration,
    length and total-energy budgets?

That is

    C_required = E_budget G / (a c^2 h^2).

It compares those values with:

    B7 historical coefficient      ~422.222
    006D stand-off coefficient      ~23.5916

and with optimistic hypothetical coefficients down to

    1e-12.

If practical operation requires coefficients many orders below every
demonstrated source-level headroom, then coefficient polishing is not the
dominant route.

A genuinely new TRUE-GRAVITY mechanism would need to alter the parametric
scaling or introduce a device-local universal gravitational coupling/effective
scale.

An ordinary nongravitational fifth force is outside the scope of this run.


NONLINEAR-GR SCOUT
==================

For a target acceleration a acting over length h,

    epsilon_target ~ a h / c^2.

If epsilon_target << 1, ordinary metric nonlinearities at that same field
strength are parametrically small.

Conversely a source of characteristic size h with strong compactness epsilon
requires roughly

    E_compact ~ epsilon c^4 h / G.

This does not constitute a nonlinear-GR no-go theorem.

It simply quantifies the energy scale associated with entering genuinely
strong-curvature gravity.


PROMOTION / FALSIFICATION
=========================

A. If the actual microscopic S histogram can be rearranged into an outward
   true-stand-off field at both N73 and N81:

       GEOMETRY_HEADROOM = PRESENT.

B. If geometry alone fails but the fixed-rho DEC+Laue optimum succeeds:

       CONSTITUTIVE_PLUS_GEOMETRIC_HEADROOM = PRESENT.

C. If even the DEC+Laue fixed-rho optimum fails:

       CURRENT_B7_ENERGY_DENSITY_ARCHITECTURE = INSUFFICIENT
       for the tested stand-off geometry.

D. Regardless of A-C, the absolute scaling ledger reports how many orders
   separate pure-GR coefficients from practical energy targets.

This run does NOT authorize:

    practical antigravity;
    new physics discovery;
    nonlinear Einstein-Skyrme validation;
    stability;
    continuum force magnitude convergence;
    a 90% heuristic claim.

It is a PATHFINDING / FALSIFICATION experiment.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

FIELD_PATHS = {
    73:
        ROOT
        / "results/data/"
        "026a_true_antigravity_strict_stationary_b7_n73.npz",

    81:
        ROOT
        / "results/data/"
        "026b_true_antigravity_strict_stationary_b7_n81.npz",
}

SUMMARY73 = (
    ROOT
    / "results/data/"
    "026a_true_antigravity_n73_augmented_minres_summary.json"
)

SUMMARY81 = (
    ROOT
    / "results/data/"
    "026b_true_antigravity_n81_force_convergence_summary.json"
)

CR3_SOURCE = (
    ROOT
    / "simulations/"
    "023cr3_geometric_degree_guarded_unrestricted_relaxation.py"
)

AQR_SOURCE = (
    ROOT
    / "simulations/"
    "023c2aqr_analytic_prism_exact_cap_payload_operator.py"
)

OUT_JSON = (
    ROOT
    / "results/data/"
    "026p_true_antigravity_practicality_escape_summary.json"
)

OUT_SCAN = (
    ROOT
    / "results/data/"
    "026p_true_antigravity_standoff_bounds.csv"
)

OUT_SCALE = (
    ROOT
    / "results/data/"
    "026p_true_antigravity_absolute_scaling.csv"
)


B = 7
ETA = 0.4
MASS = 8.0

C_B7 = 422.2220709083088
C_006D = 23.591586299249

C_LIGHT = 299_792_458.0
G_NEWTON = 6.67430e-11
G0 = 9.80665

RADIAL = np.array(
    [
        -4.543501844637980e-1,
        1.878880658050992e-2,
        8.906249999999961e-1,
    ],
    dtype=float,
)

RADIAL /= np.linalg.norm(
    RADIAL
)

STANDOFF_FACTORS = (
    1.10,
    1.25,
    1.50,
    2.00,
)

SCALING_ACCEL_G = (
    0.1,
    1.0,
)

SCALING_LENGTH_M = (
    1.0e-3,
    1.0e-2,
    1.0e-1,
    1.0,
)

ENERGY_BUDGETS_J = (
    1.0e6,
    1.0e9,
    1.0e12,
    1.0e15,
)

REFERENCE_COEFFICIENTS = {
    "B7_422":
        C_B7,

    "006D_23P59":
        C_006D,

    "C_1":
        1.0,

    "C_1E_MINUS_3":
        1.0e-3,

    "C_1E_MINUS_6":
        1.0e-6,

    "C_1E_MINUS_9":
        1.0e-9,

    "C_1E_MINUS_12":
        1.0e-12,
}


def load_module(
    name: str,
    path: Path,
):
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

    spec.loader.exec_module(
        module
    )

    return module


def weighted_quantile(
    values,
    weights,
    q,
):
    values = np.asarray(
        values,
        dtype=float,
    ).ravel()

    weights = np.asarray(
        weights,
        dtype=float,
    ).ravel()

    mask = (
        np.isfinite(values)
        & np.isfinite(weights)
        & (weights > 0.0)
    )

    v = values[mask]
    w = weights[mask]

    order = np.argsort(
        v
    )

    v = v[order]
    w = w[order]

    cumulative = np.cumsum(
        w
    )

    total = float(
        cumulative[-1]
    )

    return float(
        np.interp(
            q * total,
            cumulative,
            v,
        )
    )


def weighted_quantiles(
    values,
    weights,
    qs=(0.1, 0.5, 0.9),
):
    return [
        weighted_quantile(
            values,
            weights,
            q,
        )
        for q in qs
    ]


def prism_radial_kernel(
    aqr,
    xyz,
    dx,
    center,
    radial,
    batch=32768,
):
    half = (
        0.5
        * dx
    )

    out = np.empty(
        len(xyz),
        dtype=float,
    )

    for start in range(
        0,
        len(xyz),
        batch,
    ):
        stop = min(
            start + batch,
            len(xyz),
        )

        lo = (
            xyz[start:stop]
            - half
            - center[None, :]
        )

        hi = (
            xyz[start:stop]
            + half
            - center[None, :]
        )

        field = aqr.prism_field_many(
            lo,
            hi,
        )

        out[start:stop] = (
            field
            @ radial
        )

    return out


def dec_laue_optimum(
    rho,
    kernel,
    target_active_sum,
):
    """Exact bounded LP for fixed rho.

    Maximize

        sum s_i K_i

    subject to

        -2 rho_i <= s_i <= 4 rho_i
        sum s_i = target_active_sum.

    Starting at all lower bounds, added active density should be allocated
    to the LARGEST kernel values first.

    For a one-sided outside payload all K<0, so this places positive
    compensation where it is least harmful.
    """

    rho = np.asarray(
        rho,
        dtype=float,
    )

    kernel = np.asarray(
        kernel,
        dtype=float,
    )

    lower = (
        -2.0
        * rho
    )

    upper = (
        4.0
        * rho
    )

    capacity = (
        upper
        - lower
    )

    lower_sum = float(
        np.sum(
            lower
        )
    )

    upper_sum = float(
        np.sum(
            upper
        )
    )

    target = float(
        target_active_sum
    )

    tol = (
        1.0e-11
        * max(
            1.0,
            abs(lower_sum),
            abs(upper_sum),
            abs(target),
        )
    )

    if (
        target
        <
        lower_sum - tol
        or
        target
        >
        upper_sum + tol
    ):
        raise RuntimeError(
            "DEC LP target outside feasible interval"
        )

    need = (
        target
        - lower_sum
    )

    order = np.argsort(
        kernel
    )[::-1]

    cap_order = (
        capacity[
            order
        ]
    )

    cumulative = np.cumsum(
        cap_order
    )

    s = lower.copy()

    if need > 0.0:

        j = int(
            np.searchsorted(
                cumulative,
                need,
                side="left",
            )
        )

        if j > 0:
            full = order[
                :j
            ]

            s[
                full
            ] = upper[
                full
            ]

            used = float(
                cumulative[
                    j - 1
                ]
            )

        else:
            used = 0.0

        if j < len(order):

            idx = int(
                order[
                    j
                ]
            )

            partial = (
                need
                - used
            )

            partial = max(
                0.0,
                min(
                    float(
                        capacity[
                            idx
                        ]
                    ),
                    float(
                        partial
                    ),
                ),
            )

            s[
                idx
            ] = (
                lower[
                    idx
                ]
                + partial
            )

    constraint_relerr = float(
        abs(
            np.sum(
                s
            )
            - target
        )
        / max(
            abs(target),
            np.sum(
                rho
            ),
            1.0e-300,
        )
    )

    if constraint_relerr > 1.0e-10:
        raise RuntimeError(
            "DEC LP equality constraint reconstruction failed"
        )

    if np.any(
        s
        <
        lower
        - 1.0e-10
        * (
            rho + 1.0
        )
    ):
        raise RuntimeError(
            "DEC LP lower bound violation"
        )

    if np.any(
        s
        >
        upper
        + 1.0e-10
        * (
            rho + 1.0
        )
    ):
        raise RuntimeError(
            "DEC LP upper bound violation"
        )

    objective = float(
        np.dot(
            s,
            kernel,
        )
    )

    total_energy_weight = max(
        float(
            np.sum(
                rho
            )
        ),
        1.0e-300,
    )

    negative_energy_fraction = float(
        np.sum(
            rho[
                s < 0.0
            ]
        )
        / total_energy_weight
    )

    lower_mask = np.isclose(
        s,
        lower,
        rtol=1.0e-10,
        atol=1.0e-12,
    )

    upper_mask = np.isclose(
        s,
        upper,
        rtol=1.0e-10,
        atol=1.0e-12,
    )

    lower_energy_fraction = float(
        np.sum(
            rho[
                lower_mask
            ]
        )
        / total_energy_weight
    )

    upper_energy_fraction = float(
        np.sum(
            rho[
                upper_mask
            ]
        )
        / total_energy_weight
    )

    return {
        "source":
            s,

        "objective":
            objective,

        "constraint_relerr":
            constraint_relerr,

        "negative_energy_fraction":
            negative_energy_fraction,

        "lower_saturated_energy_fraction":
            lower_energy_fraction,

        "upper_saturated_energy_fraction":
            upper_energy_fraction,
    }


def packet_relocation_bound(
    active,
    rho,
    kernel,
    projection,
):
    """Rearrangement-inequality upper bound using actual packets.

    A packet carries its rho and S together.

    We assign the most negative-S packet to the most negative kernel location,
    and the most positive packet to the least negative kernel location.

    This preserves the exact microscopic stress histogram but ignores field
    compatibility and transport cost.
    """

    active = np.asarray(
        active,
        dtype=float,
    )

    rho = np.asarray(
        rho,
        dtype=float,
    )

    kernel = np.asarray(
        kernel,
        dtype=float,
    )

    projection = np.asarray(
        projection,
        dtype=float,
    )

    packet_order = np.argsort(
        active
    )

    position_order = np.argsort(
        kernel
    )

    assigned_active = np.empty_like(
        active
    )

    assigned_rho = np.empty_like(
        rho
    )

    assigned_active[
        position_order
    ] = active[
        packet_order
    ]

    assigned_rho[
        position_order
    ] = rho[
        packet_order
    ]

    objective = float(
        np.dot(
            assigned_active,
            kernel,
        )
    )

    neg = (
        assigned_active
        < 0.0
    )

    pos = (
        assigned_active
        >= 0.0
    )

    if np.any(
        neg
    ):
        neg_centroid = float(
            np.sum(
                projection[
                    neg
                ]
                * assigned_rho[
                    neg
                ]
            )
            / max(
                np.sum(
                    assigned_rho[
                        neg
                    ]
                ),
                1.0e-300,
            )
        )

    else:
        neg_centroid = math.nan

    if np.any(
        pos
    ):
        pos_centroid = float(
            np.sum(
                projection[
                    pos
                ]
                * assigned_rho[
                    pos
                ]
            )
            / max(
                np.sum(
                    assigned_rho[
                        pos
                    ]
                ),
                1.0e-300,
            )
        )

    else:
        pos_centroid = math.nan

    return {
        "objective":
            objective,

        "negative_packet_centroid":
            neg_centroid,

        "positive_packet_centroid":
            pos_centroid,

        "assigned_active":
            assigned_active,

        "assigned_rho":
            assigned_rho,
    }


def reconstruct_field(
    N,
    cr3,
):
    path = FIELD_PATHS[
        N
    ]

    with np.load(
        path,
        allow_pickle=False,
    ) as d:

        phi = np.asarray(
            d["phi"],
            dtype=float,
        )

        axis = np.asarray(
            d["axis"],
            dtype=float,
        )

        dx = float(
            d["dx"]
        )

        b = int(
            d["B"]
        )

        eta = float(
            d["eta"]
        )

        mass = float(
            d["mass"]
        )

    expected_shape = (
        N,
        N,
        N,
        4,
    )

    if phi.shape != expected_shape:
        raise RuntimeError(
            f"N{N} unexpected shape {phi.shape}"
        )

    if (
        b != B
        or abs(
            eta - ETA
        )
        > 1.0e-14
        or abs(
            mass - MASS
        )
        > 1.0e-14
    ):
        raise RuntimeError(
            f"N{N} physical metadata mismatch"
        )

    normerr = float(
        np.max(
            np.abs(
                np.linalg.norm(
                    phi,
                    axis=-1,
                )
                - 1.0
            )
        )
    )

    if normerr > 5.0e-10:
        raise RuntimeError(
            f"N{N} S3 normalization failure"
        )

    qx, qy, qz = (
        cr3.central4_derivatives(
            phi,
            dx,
        )
    )

    (
        gxx,
        gyy,
        gzz,
        gxy,
        gxz,
        gyz,
        e2,
        e4,
    ) = cr3.metric_terms(
        qx,
        qy,
        qz,
    )

    center_field = (
        phi[
            2:-2,
            2:-2,
            2:-2,
        ]
    )

    V = cr3.potential_sigma(
        center_field[..., 0]
    )

    rho = (
        e2
        + e4
        + V
    )

    active = (
        2.0
        * (
            e4 - V
        )
    )

    coords = axis[
        2:-2
    ]

    X, Y, Z = np.meshgrid(
        coords,
        coords,
        coords,
        indexing="ij",
    )

    xyz = np.column_stack(
        [
            X.ravel(),
            Y.ravel(),
            Z.ravel(),
        ]
    )

    rho_f = rho.ravel()
    active_f = active.ravel()

    radius = np.linalg.norm(
        xyz,
        axis=1,
    )

    projection = (
        xyz
        @ RADIAL
    )

    volume = (
        dx**3
    )

    total_energy = float(
        np.sum(
            rho_f
        )
        * volume
    )

    total_active = float(
        np.sum(
            active_f
        )
        * volume
    )

    r99 = weighted_quantile(
        radius,
        rho_f,
        0.99,
    )

    r999 = weighted_quantile(
        radius,
        rho_f,
        0.999,
    )

    support = (
        radius
        <=
        r999
        + 1.0e-12
    )

    rho_s = rho_f[
        support
    ]

    active_s = active_f[
        support
    ]

    xyz_s = xyz[
        support
    ]

    proj_s = projection[
        support
    ]

    support_energy = float(
        np.sum(
            rho_s
        )
        * volume
    )

    support_active = float(
        np.sum(
            active_s
        )
        * volume
    )

    support_fraction = (
        support_energy
        / total_energy
    )

    negative_active = (
        active_s
        < 0.0
    )

    negative_energy_fraction = float(
        np.sum(
            rho_s[
                negative_active
            ]
        )
        / max(
            np.sum(
                rho_s
            ),
            1.0e-300,
        )
    )

    if np.any(
        negative_active
    ):
        current_neg_centroid = float(
            np.sum(
                proj_s[
                    negative_active
                ]
                * rho_s[
                    negative_active
                ]
            )
            / np.sum(
                rho_s[
                    negative_active
                ]
            )
        )

    else:
        current_neg_centroid = math.nan

    current_positive = (
        active_s
        >= 0.0
    )

    current_pos_centroid = float(
        np.sum(
            proj_s[
                current_positive
            ]
            * rho_s[
                current_positive
            ]
        )
        / max(
            np.sum(
                rho_s[
                    current_positive
                ]
            ),
            1.0e-300,
        )
    )

    return {
        "N":
            N,

        "phi_norm_maxerr":
            normerr,

        "dx":
            dx,

        "rho":
            rho_s,

        "active":
            active_s,

        "xyz":
            xyz_s,

        "projection":
            proj_s,

        "volume":
            volume,

        "total_energy":
            total_energy,

        "total_active":
            total_active,

        "r99":
            r99,

        "r999":
            r999,

        "support_energy":
            support_energy,

        "support_active":
            support_active,

        "support_energy_fraction":
            support_fraction,

        "negative_active_energy_fraction":
            negative_energy_fraction,

        "current_negative_centroid":
            current_neg_centroid,

        "current_positive_centroid":
            current_pos_centroid,
    }


def source_analysis(
    field,
    factor,
    aqr,
):
    N = int(
        field[
            "N"
        ]
    )

    rho = field[
        "rho"
    ]

    active = field[
        "active"
    ]

    xyz = field[
        "xyz"
    ]

    projection = field[
        "projection"
    ]

    r999 = float(
        field[
            "r999"
        ]
    )

    volume = float(
        field[
            "volume"
        ]
    )

    d = (
        factor
        * r999
    )

    center = (
        d
        * RADIAL
    )

    kernel = prism_radial_kernel(
        aqr,
        xyz,
        field[
            "dx"
        ],
        center,
        RADIAL,
    )

    kmin = float(
        np.min(
            kernel
        )
    )

    kmax = float(
        np.max(
            kernel
        )
    )

    all_behind = bool(
        kmax < 0.0
    )

    if not all_behind:
        raise RuntimeError(
            f"N{N} factor={factor}: support is not fully behind payload"
        )

    influence = (
        active
        * kernel
    )

    actual_driver = float(
        np.sum(
            influence
        )
    )

    gross_out = float(
        np.sum(
            influence[
                influence > 0.0
            ]
        )
    )

    gross_in = float(
        np.sum(
            influence[
                influence < 0.0
            ]
        )
    )

    cancellation = float(
        np.sum(
            np.abs(
                influence
            )
        )
        / max(
            abs(
                actual_driver
            ),
            1.0e-300,
        )
    )

    if actual_driver < 0.0:

        scaffold_suppression_to_flip = float(
            max(
                0.0,
                1.0
                - gross_out
                / max(
                    abs(
                        gross_in
                    ),
                    1.0e-300,
                )
            )
        )

    else:
        scaffold_suppression_to_flip = 0.0

    repulsive = (
        (active < 0.0)
        & (kernel < 0.0)
        & (influence > 0.0)
        & (rho > 0.0)
    )

    if np.any(
        repulsive
    ):

        lambda_dec = np.zeros_like(
            rho
        )

        lambda_dec[
            repulsive
        ] = (
            -active[
                repulsive
            ]
            / (
                2.0
                * rho[
                    repulsive
                ]
            )
        )

        weights = np.where(
            repulsive,
            influence,
            0.0,
        )

        (
            dec10,
            dec50,
            dec90,
        ) = weighted_quantiles(
            lambda_dec,
            weights,
        )

    else:
        dec10 = math.nan
        dec50 = math.nan
        dec90 = math.nan

    packet = packet_relocation_bound(
        active,
        rho,
        kernel,
        projection,
    )

    sum_rho = float(
        np.sum(
            rho
        )
    )

    sum_active = float(
        np.sum(
            active
        )
    )

    ideal_laue = dec_laue_optimum(
        rho,
        kernel,
        target_active_sum=sum_rho,
    )

    current_mass = dec_laue_optimum(
        rho,
        kernel,
        target_active_sum=sum_active,
    )

    support_energy = float(
        field[
            "support_energy"
        ]
    )

    # Dimensionless normalized source efficiency proxy.
    #
    # raw driver / energy scales as 1/L^2, so multiply by R999^2.
    def normalized_efficiency(
        force,
    ):
        return float(
            force
            * r999**2
            / max(
                support_energy,
                1.0e-300,
            )
        )

    actual_eta = normalized_efficiency(
        actual_driver
    )

    packet_eta = normalized_efficiency(
        packet[
            "objective"
        ]
    )

    laue_eta = normalized_efficiency(
        ideal_laue[
            "objective"
        ]
    )

    current_mass_eta = normalized_efficiency(
        current_mass[
            "objective"
        ]
    )

    result = {
        "N":
            N,

        "factor":
            float(
                factor
            ),

        "d":
            d,

        "r999":
            r999,

        "support_energy_fraction":
            float(
                field[
                    "support_energy_fraction"
                ]
            ),

        "kernel_min":
            kmin,

        "kernel_max":
            kmax,

        "support_strictly_behind_payload":
            all_behind,

        "actual_driver":
            actual_driver,

        "actual_sign":
            (
                "OUTWARD"
                if actual_driver > 0.0
                else "INWARD"
                if actual_driver < 0.0
                else "ZERO"
            ),

        "gross_outward":
            gross_out,

        "gross_inward":
            gross_in,

        "cancellation":
            cancellation,

        "scaffold_suppression_to_flip":
            scaffold_suppression_to_flip,

        "actual_negative_energy_fraction":
            float(
                field[
                    "negative_active_energy_fraction"
                ]
            ),

        "repulsive_DEC_p10":
            dec10,

        "repulsive_DEC_p50":
            dec50,

        "repulsive_DEC_p90":
            dec90,

        "packet_relocation_bound":
            float(
                packet[
                    "objective"
                ]
            ),

        "packet_relocation_sign":
            (
                "OUTWARD"
                if packet[
                    "objective"
                ] > 0.0
                else "INWARD"
            ),

        "packet_negative_centroid":
            float(
                packet[
                    "negative_packet_centroid"
                ]
            ),

        "packet_positive_centroid":
            float(
                packet[
                    "positive_packet_centroid"
                ]
            ),

        "current_negative_centroid":
            float(
                field[
                    "current_negative_centroid"
                ]
            ),

        "current_positive_centroid":
            float(
                field[
                    "current_positive_centroid"
                ]
            ),

        "ideal_DEC_Laue_bound":
            float(
                ideal_laue[
                    "objective"
                ]
            ),

        "ideal_DEC_Laue_sign":
            (
                "OUTWARD"
                if ideal_laue[
                    "objective"
                ] > 0.0
                else "INWARD"
            ),

        "ideal_negative_energy_fraction":
            float(
                ideal_laue[
                    "negative_energy_fraction"
                ]
            ),

        "ideal_lower_saturated_energy_fraction":
            float(
                ideal_laue[
                    "lower_saturated_energy_fraction"
                ]
            ),

        "ideal_upper_saturated_energy_fraction":
            float(
                ideal_laue[
                    "upper_saturated_energy_fraction"
                ]
            ),

        "current_mass_DEC_bound":
            float(
                current_mass[
                    "objective"
                ]
            ),

        "current_mass_DEC_sign":
            (
                "OUTWARD"
                if current_mass[
                    "objective"
                ] > 0.0
                else "INWARD"
            ),

        "actual_eta_norm":
            actual_eta,

        "packet_eta_norm":
            packet_eta,

        "ideal_Laue_eta_norm":
            laue_eta,

        "current_mass_eta_norm":
            current_mass_eta,
    }

    print(
        "BOUND "
        f"N={N} "
        f"FACTOR={factor:.2f} "
        f"D={d:.8e} "
        f"R999={r999:.8e} "
        f"ACTUAL={actual_driver:+.8e} "
        f"PACKET={packet['objective']:+.8e} "
        f"DEC_LAUE={ideal_laue['objective']:+.8e} "
        f"DEC_CURRENT_MASS={current_mass['objective']:+.8e} "
        f"NEG_E_ACTUAL={field['negative_active_energy_fraction']:.6f} "
        f"NEG_E_IDEAL={ideal_laue['negative_energy_fraction']:.6f} "
        f"DEC50={dec50:.6f} "
        f"SCAFFOLD_SUPPRESS={scaffold_suppression_to_flip:.6f}",
        flush=True,
    )

    return result


def relative_change(
    a,
    b,
):
    return float(
        abs(
            b - a
        )
        / max(
            abs(a),
            abs(b),
            1.0e-300,
        )
    )


def scaling_analysis():
    rows = []

    for accel_g in SCALING_ACCEL_G:

        a = (
            accel_g
            * G0
        )

        for h in SCALING_LENGTH_M:

            coeff_one_energy = (
                a
                * C_LIGHT**2
                * h**2
                / G_NEWTON
            )

            weakness = (
                a
                * h
                / C_LIGHT**2
            )

            compact_1e3 = (
                1.0e-3
                * C_LIGHT**4
                * h
                / G_NEWTON
            )

            compact_0p1 = (
                1.0e-1
                * C_LIGHT**4
                * h
                / G_NEWTON
            )

            for budget in ENERGY_BUDGETS_J:

                c_required = (
                    budget
                    * G_NEWTON
                    / (
                        a
                        * C_LIGHT**2
                        * h**2
                    )
                )

                b7_gap = (
                    C_B7
                    / c_required
                )

                d6_gap = (
                    C_006D
                    / c_required
                )

                row = {
                    "accel_g":
                        accel_g,

                    "length_m":
                        h,

                    "energy_budget_J":
                        budget,

                    "coefficient_one_energy_J":
                        coeff_one_energy,

                    "C_required":
                        c_required,

                    "B7_improvement_factor_required":
                        b7_gap,

                    "006D_improvement_factor_required":
                        d6_gap,

                    "B7_orders_required":
                        math.log10(
                            b7_gap
                        ),

                    "006D_orders_required":
                        math.log10(
                            d6_gap
                        ),

                    "effective_G_over_G_if_C1":
                        1.0
                        / c_required,

                    "target_metric_weakness_ah_over_c2":
                        weakness,

                    "energy_for_compactness_1e_minus_3_J":
                        compact_1e3,

                    "energy_for_compactness_0p1_J":
                        compact_0p1,
                }

                rows.append(
                    row
                )

    return rows


def main():
    print(
        "=== 026P TRUE-ANTIGRAVITY PRACTICALITY ESCAPE GATE ===",
        flush=True,
    )

    for path in (
        FIELD_PATHS[73],
        FIELD_PATHS[81],
        SUMMARY73,
        SUMMARY81,
        CR3_SOURCE,
        AQR_SOURCE,
    ):
        if not path.is_file():
            raise RuntimeError(
                f"Missing {path}"
            )

    summary73 = json.loads(
        SUMMARY73.read_text()
    )

    summary81 = json.loads(
        SUMMARY81.read_text()
    )

    if (
        summary73.get(
            "decision"
        )
        !=
        "GREEN_STRICT_N73_CONTINUOUS_OUTWARD_SENTINEL"
    ):
        raise RuntimeError(
            "N73 green lineage audit failed"
        )

    if not bool(
        summary81.get(
            "n81",
            {},
        ).get(
            "stationary",
            False,
        )
    ):
        raise RuntimeError(
            "N81 strict-stationarity lineage audit failed"
        )

    if not bool(
        summary81.get(
            "n81",
            {},
        ).get(
            "physical_gate",
            False,
        )
    ):
        raise RuntimeError(
            "N81 physical-gate lineage audit failed"
        )

    n81_force = summary81.get(
        "n81_force"
    )

    if (
        not isinstance(
            n81_force,
            dict,
        )
        or not bool(
            n81_force.get(
                "certified",
                False,
            )
        )
        or n81_force.get(
            "sign"
        )
        != "OUTWARD"
    ):
        raise RuntimeError(
            "N81 outward-force lineage audit failed"
        )

    print(
        "026P_N73_STRICT_GREEN_LINEAGE=PASS",
        flush=True,
    )

    print(
        "026P_N81_STRICT_PHYSICAL_OUTWARD_LINEAGE=PASS",
        flush=True,
    )

    print(
        "026P_N81_FORCE_CONVERGENCE_STATUS="
        + str(
            summary81.get(
                "decision"
            )
        ),
        flush=True,
    )

    cr3 = load_module(
        "p_cr3",
        CR3_SOURCE,
    )

    aqr = load_module(
        "p_aqr",
        AQR_SOURCE,
    )

    aqr.validate_analytic_formulae()

    print(
        "026P_ANALYTIC_PRISM_KERNEL_AUDIT=PASS",
        flush=True,
    )

    fields = {}

    print(
        "\n=== MICROSCOPIC SOURCE RECONSTRUCTION ===",
        flush=True,
    )

    for N in (
        73,
        81,
    ):
        field = reconstruct_field(
            N,
            cr3,
        )

        fields[
            N
        ] = field

        print(
            "FIELD "
            f"N={N} "
            f"DX={field['dx']:.12e} "
            f"ENERGY={field['total_energy']:.12e} "
            f"ACTIVE={field['total_active']:.12e} "
            f"R99={field['r99']:.12e} "
            f"R999={field['r999']:.12e} "
            f"SUPPORT_E_FRAC={field['support_energy_fraction']:.12e} "
            f"NEG_ACTIVE_E_FRAC={field['negative_active_energy_fraction']:.12e} "
            f"NORMERR={field['phi_norm_maxerr']:.3e}",
            flush=True,
        )

    r999_relchange = relative_change(
        fields[73][
            "r999"
        ],
        fields[81][
            "r999"
        ],
    )

    negative_fraction_relchange = relative_change(
        fields[73][
            "negative_active_energy_fraction"
        ],
        fields[81][
            "negative_active_energy_fraction"
        ],
    )

    print(
        "N73_N81_R999_RELCHANGE="
        f"{r999_relchange:.15e}",
        flush=True,
    )

    print(
        "N73_N81_NEGATIVE_ACTIVE_ENERGY_FRACTION_RELCHANGE="
        f"{negative_fraction_relchange:.15e}",
        flush=True,
    )

    print(
        "\n=== TRUE STAND-OFF EXTREMAL BOUNDS ===",
        flush=True,
    )

    bound_rows = []

    by_key = {}

    for N in (
        73,
        81,
    ):

        for factor in STANDOFF_FACTORS:

            row = source_analysis(
                fields[
                    N
                ],
                factor,
                aqr,
            )

            bound_rows.append(
                row
            )

            by_key[
                (
                    N,
                    factor,
                )
            ] = row

    print(
        "\n=== N73 -> N81 BOUND CONVERGENCE ===",
        flush=True,
    )

    convergence_rows = []

    for factor in STANDOFF_FACTORS:

        a = by_key[
            (
                73,
                factor,
            )
        ]

        b = by_key[
            (
                81,
                factor,
            )
        ]

        packet_rel = relative_change(
            a[
                "packet_eta_norm"
            ],
            b[
                "packet_eta_norm"
            ],
        )

        laue_rel = relative_change(
            a[
                "ideal_Laue_eta_norm"
            ],
            b[
                "ideal_Laue_eta_norm"
            ],
        )

        current_mass_rel = relative_change(
            a[
                "current_mass_eta_norm"
            ],
            b[
                "current_mass_eta_norm"
            ],
        )

        convergence_rows.append(
            {
                "factor":
                    factor,

                "packet_eta_relchange":
                    packet_rel,

                "ideal_Laue_eta_relchange":
                    laue_rel,

                "current_mass_eta_relchange":
                    current_mass_rel,
            }
        )

        print(
            "BOUND_CONVERGENCE "
            f"FACTOR={factor:.2f} "
            f"PACKET_REL={packet_rel:.8e} "
            f"DEC_LAUE_REL={laue_rel:.8e} "
            f"DEC_CURRENT_MASS_REL={current_mass_rel:.8e}",
            flush=True,
        )

    primary = by_key[
        (
            81,
            1.25,
        )
    ]

    packet_standoff = bool(
        primary[
            "packet_relocation_bound"
        ]
        > 0.0
    )

    dec_standoff = bool(
        primary[
            "ideal_DEC_Laue_bound"
        ]
        > 0.0
    )

    current_standoff = bool(
        primary[
            "actual_driver"
        ]
        > 0.0
    )

    participation_gap = float(
        primary[
            "ideal_negative_energy_fraction"
        ]
        / max(
            primary[
                "actual_negative_energy_fraction"
            ],
            1.0e-300,
        )
    )

    if packet_standoff:

        architecture_path = (
            "ACTUAL_STRESS_HISTOGRAM_HAS_STANDOFF_HEADROOM_"
            "SPATIAL_SEGREGATION_AND_PARTICIPATION_ARE_PRIMARY"
        )

    elif dec_standoff:

        architecture_path = (
            "GEOMETRY_ALONE_INSUFFICIENT_"
            "CONSTITUTIVE_STRESS_PLUS_SPATIAL_SEGREGATION_REQUIRED"
        )

    else:

        architecture_path = (
            "CURRENT_B7_RHO_ARCHITECTURE_INSUFFICIENT_"
            "NEW_MICROSCOPIC_FIELD_FAMILY_REQUIRED"
        )

    print(
        "\n=== MICROSCOPIC ARCHITECTURE DECISION ===",
        flush=True,
    )

    print(
        "026P_CURRENT_N81_1P25R999_STANDOFF="
        + (
            "OUTWARD"
            if current_standoff
            else "INWARD"
        ),
        flush=True,
    )

    print(
        "026P_ACTUAL_PACKET_RELOCATION_STANDOFF="
        + (
            "POSSIBLE_IN_RELAXED_BOUND"
            if packet_standoff
            else "NOT_POSSIBLE_IN_RELAXED_BOUND"
        ),
        flush=True,
    )

    print(
        "026P_DEC_LAUE_STANDOFF="
        + (
            "POSSIBLE_IN_RELAXED_BOUND"
            if dec_standoff
            else "NOT_POSSIBLE_IN_RELAXED_BOUND"
        ),
        flush=True,
    )

    print(
        "026P_ACTUAL_NEGATIVE_ACTIVE_ENERGY_FRACTION="
        f"{primary['actual_negative_energy_fraction']:.15e}",
        flush=True,
    )

    print(
        "026P_IDEAL_DEC_LAUE_NEGATIVE_ENERGY_FRACTION="
        f"{primary['ideal_negative_energy_fraction']:.15e}",
        flush=True,
    )

    print(
        "026P_PRODUCTIVE_PARTICIPATION_GAP_FACTOR="
        f"{participation_gap:.15e}",
        flush=True,
    )

    print(
        "026P_CURRENT_REPULSIVE_DEC50="
        f"{primary['repulsive_DEC_p50']:.15e}",
        flush=True,
    )

    print(
        "026P_CURRENT_SCAFFOLD_SUPPRESSION_TO_FLIP="
        f"{primary['scaffold_suppression_to_flip']:.15e}",
        flush=True,
    )

    print(
        "026P_ARCHITECTURE_PATH="
        f"{architecture_path}",
        flush=True,
    )

    print(
        "\n=== ABSOLUTE PURE-GR SCALING LEDGER ===",
        flush=True,
    )

    scaling_rows = scaling_analysis()

    for accel_g in SCALING_ACCEL_G:

        for h in SCALING_LENGTH_M:

            subset = [
                r
                for r in scaling_rows
                if (
                    r[
                        "accel_g"
                    ]
                    == accel_g
                    and
                    r[
                        "length_m"
                    ]
                    == h
                    and
                    r[
                        "energy_budget_J"
                    ]
                    == 1.0e9
                )
            ]

            row = subset[
                0
            ]

            print(
                "SCALING "
                f"A_G={accel_g:.1f} "
                f"H_M={h:.3e} "
                f"E_C1={row['coefficient_one_energy_J']:.8e} "
                f"C_REQ_AT_1GJ={row['C_required']:.8e} "
                f"006D_ORDERS_TO_1GJ={row['006D_orders_required']:.6f} "
                f"GEFF_OVER_G_C1={row['effective_G_over_G_if_C1']:.8e} "
                f"AH_OVER_C2={row['target_metric_weakness_ah_over_c2']:.8e}",
                flush=True,
            )

    headline = [
        r
        for r in scaling_rows
        if (
            r[
                "accel_g"
            ]
            == 1.0
            and
            r[
                "length_m"
            ]
            == 1.0
            and
            r[
                "energy_budget_J"
            ]
            == 1.0e12
        )
    ][0]

    generous_small = [
        r
        for r in scaling_rows
        if (
            r[
                "accel_g"
            ]
            == 0.1
            and
            r[
                "length_m"
            ]
            == 1.0e-2
            and
            r[
                "energy_budget_J"
            ]
            == 1.0e15
        )
    ][0]

    print(
        "\n=== PRACTICALITY ESCAPE REQUIREMENT ===",
        flush=True,
    )

    print(
        "ONE_G_ONE_METER_ONE_TJ_C_REQUIRED="
        f"{headline['C_required']:.15e}",
        flush=True,
    )

    print(
        "ONE_G_ONE_METER_ONE_TJ_006D_ORDERS_GAP="
        f"{headline['006D_orders_required']:.15e}",
        flush=True,
    )

    print(
        "ONE_G_ONE_METER_ONE_TJ_B7_ORDERS_GAP="
        f"{headline['B7_orders_required']:.15e}",
        flush=True,
    )

    print(
        "POINT_ONE_G_ONE_CM_ONE_PJ_C_REQUIRED="
        f"{generous_small['C_required']:.15e}",
        flush=True,
    )

    print(
        "POINT_ONE_G_ONE_CM_ONE_PJ_006D_ORDERS_GAP="
        f"{generous_small['006D_orders_required']:.15e}",
        flush=True,
    )

    print(
        "POINT_ONE_G_ONE_CM_ONE_PJ_B7_ORDERS_GAP="
        f"{generous_small['B7_orders_required']:.15e}",
        flush=True,
    )

    nonlinear_1m = headline[
        "target_metric_weakness_ah_over_c2"
    ]

    strong_energy_1m = headline[
        "energy_for_compactness_0p1_J"
    ]

    print(
        "ONE_G_ONE_METER_TARGET_METRIC_WEAKNESS="
        f"{nonlinear_1m:.15e}",
        flush=True,
    )

    print(
        "ONE_METER_ENERGY_FOR_COMPACTNESS_0P1="
        f"{strong_energy_1m:.15e}",
        flush=True,
    )

    # Interpretation:
    #
    # If practical C requirements are many orders smaller than the best
    # demonstrated source coefficients and beyond any verified source-level
    # headroom, another order-unity coefficient improvement is not the dominant
    # route.
    #
    # We deliberately do not declare an absolute theorem that no unknown GR
    # construction could ever reach such a coefficient.
    #
    # Instead we mark the parametric scaling problem as the dominant unresolved
    # practicality requirement.

    if (
        headline[
            "006D_orders_required"
        ]
        > 10.0
    ):

        scaling_path = (
            "NEW_PARAMETRIC_TRUE_GRAVITY_SCALE_OR_"
            "DEVICE_LOCAL_UNIVERSAL_METRIC_COUPLING_REQUIRED"
        )

    else:

        scaling_path = (
            "SOURCE_COEFFICIENT_IMPROVEMENT_MAY_REMAIN_COMPETITIVE"
        )

    print(
        "026P_SCALING_PATH="
        f"{scaling_path}",
        flush=True,
    )

    print(
        "\n=== FINAL TRUE-ANTIGRAVITY PATH ===",
        flush=True,
    )

    print(
        "026P_STAGE_1="
        f"{architecture_path}",
        flush=True,
    )

    print(
        "026P_STAGE_2="
        f"{scaling_path}",
        flush=True,
    )

    print(
        "026P_STAGE_3="
        "CONSERVATION_COMPATIBILITY_STABILITY_"
        "NONLINEAR_GR_AND_EMPIRICAL_VALIDATION",
        flush=True,
    )

    print(
        "026P_N89_STILL_REQUIRED_FOR_B7_FORCE_CONTINUUM=YES",
        flush=True,
    )

    print(
        "026P_N89_IS_A_PRACTICALITY_SCALING_ESCAPE=NO",
        flush=True,
    )

    print(
        "026P_TRUE_ANTIGRAVITY_NOT_ANALOGUE=YES",
        flush=True,
    )

    # Write outputs.
    with OUT_SCAN.open(
        "w",
        newline="",
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=list(
                bound_rows[
                    0
                ].keys()
            ),
        )

        writer.writeheader()

        writer.writerows(
            bound_rows
        )

    with OUT_SCALE.open(
        "w",
        newline="",
    ) as f:

        writer = csv.DictWriter(
            f,
            fieldnames=list(
                scaling_rows[
                    0
                ].keys()
            ),
        )

        writer.writeheader()

        writer.writerows(
            scaling_rows
        )

    summary = {
        "simulation":
            "026P",

        "branch":
            "TRUE_ANTIGRAVITY",

        "question":
            (
                "What microscopic source reorganization and what additional "
                "parametric gravitational scaling improvement are required "
                "to move from the strict B7 field toward practical true "
                "antigravity?"
            ),

        "lineage":
            {
                "N73_strict_green":
                    True,

                "N81_strict_stationary":
                    True,

                "N81_physical":
                    True,

                "N81_force_sign_certified_outward":
                    True,

                "N81_force_magnitude_converged":
                    False,
            },

        "field_comparison":
            {
                "N73":
                    {
                        "r999":
                            fields[73][
                                "r999"
                            ],

                        "negative_active_energy_fraction":
                            fields[73][
                                "negative_active_energy_fraction"
                            ],

                        "energy":
                            fields[73][
                                "total_energy"
                            ],
                    },

                "N81":
                    {
                        "r999":
                            fields[81][
                                "r999"
                            ],

                        "negative_active_energy_fraction":
                            fields[81][
                                "negative_active_energy_fraction"
                            ],

                        "energy":
                            fields[81][
                                "total_energy"
                            ],
                    },

                "r999_relchange":
                    r999_relchange,

                "negative_active_fraction_relchange":
                    negative_fraction_relchange,
            },

        "primary_N81_1p25R999":
            primary,

        "cross_resolution_bounds":
            convergence_rows,

        "architecture":
            {
                "actual_standoff":
                    current_standoff,

                "packet_relocation_standoff":
                    packet_standoff,

                "DEC_Laue_standoff":
                    dec_standoff,

                "participation_gap_factor":
                    participation_gap,

                "path":
                    architecture_path,
            },

        "scaling":
            {
                "one_g_one_meter_one_TJ":
                    headline,

                "point_one_g_one_cm_one_PJ":
                    generous_small,

                "path":
                    scaling_path,
            },

        "final_path":
            {
                "stage_1_microscopic_architecture":
                    architecture_path,

                "stage_2_practical_scaling":
                    scaling_path,

                "stage_3_validation":
                    (
                        "CONSERVATION_COMPATIBILITY_STABILITY_"
                        "NONLINEAR_GR_AND_EMPIRICAL_VALIDATION"
                    ),
            },

        "claims":
            {
                "new_physics_discovery":
                    False,

                "practical_antigravity_device":
                    False,

                "90_percent_heuristic_authorized":
                    False,

                "continuum_force_magnitude":
                    False,

                "full_stability":
                    False,

                "nonlinear_GR":
                    False,
            },
    }

    OUT_JSON.write_text(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )

    print(
        "\n=== OUTPUTS ===",
        flush=True,
    )

    print(
        f"OUT_JSON={OUT_JSON}",
        flush=True,
    )

    print(
        f"OUT_STANDOFF_CSV={OUT_SCAN}",
        flush=True,
    )

    print(
        f"OUT_SCALING_CSV={OUT_SCALE}",
        flush=True,
    )

    print(
        "\n=== 026P DECISION ===",
        flush=True,
    )

    print(
        "026P_DECISION=TRUE_ANTIGRAVITY_PRACTICALITY_PATH_QUANTIFIED",
        flush=True,
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO",
        flush=True,
    )

    print(
        "NEW_PHYSICS_DISCOVERY=NO",
        flush=True,
    )

    print(
        "HEURISTIC_90_PERCENT_AUTHORIZED=NO",
        flush=True,
    )


if __name__ == "__main__":
    main()
