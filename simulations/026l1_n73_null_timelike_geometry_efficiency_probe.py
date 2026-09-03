#!/usr/bin/env python3
"""026L1 — N73 null-vs-timelike geometry and efficiency probe.

This is a READ-ONLY mechanism diagnostic on the already-green strict N=73
B=7, eta=0.4, m=8 Skyrmion field.

It does not modify the N81 solver, checkpoint or any field.

QUESTION
--------
What does the same physical stress tensor do to:

    1. a slowly moving neutral test body;
    2. a null ray / electromagnetic geometric-optics probe?

For a static source in linearized GR:

    S_slow = rho + Tr(T)

sources h_00 and the slow-particle acceleration.

For a null propagation direction k:

    S_gamma(k) = rho + k_i T_ij k_j

sources the combination h_00 + h_kk entering the local transverse
null-geodesic bending driver.

For a source obeying NEC:

    S_gamma(k) >= 0

for every unit k.

Therefore slow-matter repulsion can coexist with locally focusing null
curvature when sufficiently negative transverse stresses make

    rho + Tr(T) < 0.

EFFICIENCY DIAGNOSTIC
---------------------
Under DEC each principal stress obeys

    -rho <= p_i <= rho.

Hence

    S_slow >= -2 rho.

Define, on negative-active cells,

    Lambda_DEC = -S_slow / (2 rho).

Lambda_DEC=1 is the local maximum negative active source per unit energy
allowed by the type-I DEC cone.

If productive force cells already have Lambda_DEC near unity, further
orders-of-magnitude improvement cannot come primarily from increasing local
negative pressure.  It must come from spatial/kernel leverage, productive
participation, reduced cancellation, or new physics.

OBSERVABLE
----------
Use the exact piecewise-constant rectangular-prism Green-function kernel from
023C2AQR at the previously audited worst-direction payload center.

For the massive source:

    A_slow ~ sum S_slow K_r.

For each photon propagation vector k perpendicular to the payload radial
direction:

    B_gamma(k) ~ sum S_gamma(k) K_r.

Since the payload radial direction is transverse to k, B_gamma is a local
radial null-bending driver.

Only signs and dimensionless source/kernel ratios are interpreted.  This is
NOT an integrated lensing angle and NOT a finite-payload promotion result.

CLAIM LIMITS
------------
This run does not establish nonlinear GR, stability, practical energy scaling,
an experiment or a device.
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

FIELD = (
    ROOT
    / "results/data/"
    "026a_true_antigravity_strict_stationary_b7_n73.npz"
)

SUMMARY73 = (
    ROOT
    / "results/data/"
    "026a_true_antigravity_n73_augmented_minres_summary.json"
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
    "026l1_n73_null_timelike_geometry_efficiency_summary.json"
)

OUT_CSV = (
    ROOT
    / "results/data/"
    "026l1_n73_null_direction_scan.csv"
)

B = 7
ETA = 0.4
MASS = 8.0

PAYLOAD_CENTER = 3.870161274564900e-1

RADIAL = np.array(
    [
        -4.543501844638e-1,
        1.878880658051e-2,
        8.906250000000e-1,
    ],
    dtype=float,
)

RADIAL /= np.linalg.norm(RADIAL)

N_NULL_DIRECTIONS = 24


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)

    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)

    return module


def weighted_quantiles(values, weights, quantiles=(0.1, 0.5, 0.9)):
    values = np.asarray(values, float).ravel()
    weights = np.asarray(weights, float).ravel()

    mask = (
        np.isfinite(values)
        & np.isfinite(weights)
        & (weights > 0.0)
    )

    values = values[mask]
    weights = weights[mask]

    if len(values) == 0:
        return [math.nan for _ in quantiles]

    order = np.argsort(values)
    values = values[order]
    weights = weights[order]

    cumulative = np.cumsum(weights)
    total = float(cumulative[-1])

    return [
        float(
            np.interp(
                q * total,
                cumulative,
                values,
            )
        )
        for q in quantiles
    ]


def prism_radial_kernel(
    aqr,
    xyz,
    dx,
    center,
    radial,
    batch=32768,
):
    half = 0.5 * dx
    out = np.empty(len(xyz), dtype=float)

    for start in range(0, len(xyz), batch):
        stop = min(start + batch, len(xyz))

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


def transverse_basis(radial):
    refs = (
        np.array([0.0, 0.0, 1.0]),
        np.array([0.0, 1.0, 0.0]),
        np.array([1.0, 0.0, 0.0]),
    )

    for ref in refs:
        e1 = np.cross(radial, ref)
        n = np.linalg.norm(e1)

        if n > 1.0e-6:
            e1 /= n
            e2 = np.cross(radial, e1)
            e2 /= np.linalg.norm(e2)
            return e1, e2

    raise RuntimeError(
        "Cannot construct transverse basis"
    )


def main():
    print(
        "=== 026L1 N73 NULL-vs-TIMELIKE GEOMETRY PROBE ===",
        flush=True,
    )

    for path in (
        FIELD,
        SUMMARY73,
        CR3_SOURCE,
        AQR_SOURCE,
    ):
        if not path.is_file():
            raise RuntimeError(
                f"Missing {path}"
            )

    prior = json.loads(
        SUMMARY73.read_text()
    )

    if (
        prior.get("decision")
        !=
        "GREEN_STRICT_N73_CONTINUOUS_OUTWARD_SENTINEL"
    ):
        raise RuntimeError(
            "N73 green lineage audit failed"
        )

    print(
        "N73_GREEN_LINEAGE_AUDIT=PASS",
        flush=True,
    )

    with np.load(
        FIELD,
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

    if phi.shape != (
        73,
        73,
        73,
        4,
    ):
        raise RuntimeError(
            f"Unexpected field shape {phi.shape}"
        )

    if (
        b != B
        or abs(eta - ETA) > 1e-14
        or abs(mass - MASS) > 1e-14
    ):
        raise RuntimeError(
            "Physical metadata mismatch"
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

    print(
        f"S3_NORM_MAXERR={normerr:.15e}",
        flush=True,
    )

    if normerr > 5e-10:
        raise RuntimeError(
            "S3 normalization failure"
        )

    cr3 = load_module(
        "l1_cr3",
        CR3_SOURCE,
    )

    aqr = load_module(
        "l1_aqr",
        AQR_SOURCE,
    )

    # Existing independent analytic-prism validation.
    aqr.validate_analytic_formulae()

    print(
        "ANALYTIC_PRISM_KERNEL_AUDIT=PASS",
        flush=True,
    )

    print(
        "\n=== RECONSTRUCT FULL N73 STRESS TENSOR ===",
        flush=True,
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

    center_field = phi[
        2:-2,
        2:-2,
        2:-2,
    ]

    V = cr3.potential_sigma(
        center_field[..., 0]
    )

    rho = (
        e2
        + e4
        + V
    )

    g = np.empty(
        e2.shape + (3, 3),
        dtype=float,
    )

    g[..., 0, 0] = gxx
    g[..., 1, 1] = gyy
    g[..., 2, 2] = gzz

    g[..., 0, 1] = g[..., 1, 0] = gxy
    g[..., 0, 2] = g[..., 2, 0] = gxz
    g[..., 1, 2] = g[..., 2, 1] = gyz

    g2 = np.einsum(
        "...ik,...kj->...ij",
        g,
        g,
    )

    eye = np.eye(3)

    stress = (
        2.0 * g
        - e2[..., None, None] * eye
        + 2.0
        * (
            e2[..., None, None] * g
            - g2
        )
        - e4[..., None, None] * eye
        - V[..., None, None] * eye
    )

    trace_stress = np.trace(
        stress,
        axis1=-2,
        axis2=-1,
    )

    active_from_stress = (
        rho
        + trace_stress
    )

    active = 2.0 * (
        e4
        - V
    )

    active_identity_rel = float(
        np.max(
            np.abs(
                active_from_stress
                - active
            )
            / (
                rho
                + np.abs(
                    trace_stress
                )
                + np.abs(
                    active
                )
                + 1e-14
            )
        )
    )

    print(
        "ACTIVE_SOURCE_STRESS_IDENTITY_MAXREL="
        f"{active_identity_rel:.15e}",
        flush=True,
    )

    if active_identity_rel > 1e-10:
        raise RuntimeError(
            "Active-source identity failed"
        )

    eig = np.linalg.eigvalsh(
        stress
    )

    lam_min = eig[..., 0]
    lam_mid = eig[..., 1]
    lam_max = eig[..., 2]

    null_min = (
        rho
        + lam_min
    )

    null_max = (
        rho
        + lam_max
    )

    scale = (
        rho
        + np.abs(
            lam_min
        )
        + 1e-14
    )

    null_min_scaled = float(
        np.min(
            null_min
            / scale
        )
    )

    print(
        "MIN_NULL_SOURCE_SCALED="
        f"{null_min_scaled:.15e}",
        flush=True,
    )

    null_source_pass = bool(
        null_min_scaled
        >= -1e-9
    )

    print(
        "ALL_LOCAL_NULL_DIRECTIONS_NONNEGATIVE="
        + (
            "PASS"
            if null_source_pass
            else "FAIL"
        ),
        flush=True,
    )

    if not null_source_pass:
        raise RuntimeError(
            "Unexpected NEC/null-source failure"
        )

    volume = dx**3

    energy_total = float(
        np.sum(
            rho
        )
        * volume
    )

    active_total = float(
        np.sum(
            active
        )
        * volume
    )

    stress_integral = (
        np.sum(
            stress,
            axis=(0, 1, 2),
        )
        * volume
    )

    laue_ratio = float(
        np.linalg.norm(
            stress_integral
        )
        / max(
            energy_total,
            1e-300,
        )
    )

    print(
        f"TOTAL_ENERGY={energy_total:.15e}",
        flush=True,
    )

    print(
        f"TOTAL_ACTIVE_SOURCE={active_total:.15e}",
        flush=True,
    )

    print(
        "INTEGRATED_STRESS_MATRIX="
        + ";".join(
            ",".join(
                f"{x:.8e}"
                for x in row
            )
            for row in stress_integral
        ),
        flush=True,
    )

    print(
        f"LAUE_STRESS_OVER_ENERGY={laue_ratio:.15e}",
        flush=True,
    )

    coords = axis[2:-2]

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
    stress_f = stress.reshape(
        -1,
        3,
        3,
    )

    eig_f = eig.reshape(
        -1,
        3,
    )

    center = (
        PAYLOAD_CENTER
        * RADIAL
    )

    print(
        "\n=== EXACT PRISM KERNEL AT AUDITED PAYLOAD CENTER ===",
        flush=True,
    )

    kernel = prism_radial_kernel(
        aqr,
        xyz,
        dx,
        center,
        RADIAL,
    )

    influence = (
        active_f
        * kernel
    )

    massive_radial = float(
        np.sum(
            influence
        )
    )

    massive_out = float(
        np.sum(
            influence[
                influence > 0.0
            ]
        )
    )

    massive_in = float(
        np.sum(
            influence[
                influence < 0.0
            ]
        )
    )

    massive_l1 = float(
        np.sum(
            np.abs(
                influence
            )
        )
    )

    massive_cancel = (
        massive_l1
        / max(
            abs(
                massive_radial
            ),
            1e-300,
        )
    )

    print(
        "SLOW_MATTER_POINT_RADIAL_DRIVER="
        f"{massive_radial:.15e}",
        flush=True,
    )

    print(
        "SLOW_MATTER_POINT_SIGN="
        + (
            "OUTWARD"
            if massive_radial > 0.0
            else "INWARD"
            if massive_radial < 0.0
            else "ZERO"
        ),
        flush=True,
    )

    print(
        f"SLOW_MATTER_GROSS_OUTWARD={massive_out:.15e}",
        flush=True,
    )

    print(
        f"SLOW_MATTER_GROSS_INWARD={massive_in:.15e}",
        flush=True,
    )

    print(
        f"SLOW_MATTER_CANCELLATION_FACTOR={massive_cancel:.15e}",
        flush=True,
    )

    # --------------------------------------------------------------
    # Local DEC stress-leverage anatomy in the cells that actually
    # contribute outward at this target.
    # --------------------------------------------------------------

    rho_safe = np.maximum(
        rho_f,
        1e-300,
    )

    slow_ratio = (
        active_f
        / rho_safe
    )

    lambda_dec = np.maximum(
        0.0,
        -active_f
        / (
            2.0
            * rho_safe
        ),
    )

    null_min_f = (
        rho_f
        + eig_f[:, 0]
    )

    null_min_ratio = (
        null_min_f
        / rho_safe
    )

    transverse_pair = (
        eig_f[:, 1]
        + eig_f[:, 2]
    )

    transverse_pair_ratio = (
        transverse_pair
        / rho_safe
    )

    productive_w = np.maximum(
        influence,
        0.0,
    )

    (
        dec_p10,
        dec_p50,
        dec_p90,
    ) = weighted_quantiles(
        lambda_dec,
        productive_w,
    )

    (
        slow_p10,
        slow_p50,
        slow_p90,
    ) = weighted_quantiles(
        slow_ratio,
        productive_w,
    )

    (
        null_p10,
        null_p50,
        null_p90,
    ) = weighted_quantiles(
        null_min_ratio,
        productive_w,
    )

    (
        trans_p10,
        trans_p50,
        trans_p90,
    ) = weighted_quantiles(
        transverse_pair_ratio,
        productive_w,
    )

    neg_active = (
        active_f
        < 0.0
    )

    negative_active_energy_fraction = float(
        np.sum(
            rho_f[
                neg_active
            ]
        )
        * volume
        / max(
            energy_total,
            1e-300,
        )
    )

    gross_outward_from_negative_active = float(
        np.sum(
            productive_w[
                neg_active
            ]
        )
        / max(
            np.sum(
                productive_w
            ),
            1e-300,
        )
    )

    near_nec = (
        null_min_ratio
        < 0.10
    )

    gross_outward_near_nec_fraction = float(
        np.sum(
            productive_w[
                near_nec
            ]
        )
        / max(
            np.sum(
                productive_w
            ),
            1e-300,
        )
    )

    order = np.argsort(
        productive_w
    )[::-1]

    cumulative = np.cumsum(
        productive_w[
            order
        ]
    )

    target90 = (
        0.90
        * max(
            float(
                cumulative[-1]
            ),
            1e-300,
        )
    )

    n90 = int(
        np.searchsorted(
            cumulative,
            target90,
        )
        + 1
    )

    productive90 = order[
        :n90
    ]

    f90_energy_fraction = float(
        np.sum(
            rho_f[
                productive90
            ]
        )
        * volume
        / max(
            energy_total,
            1e-300,
        )
    )

    print(
        "\n=== PRODUCTIVE STRESS LEVERAGE ===",
        flush=True,
    )

    print(
        "PRODUCTIVE_DEC_TRACE_LEVERAGE_P10_P50_P90="
        f"{dec_p10:.8e},"
        f"{dec_p50:.8e},"
        f"{dec_p90:.8e}",
        flush=True,
    )

    print(
        "PRODUCTIVE_S_OVER_RHO_P10_P50_P90="
        f"{slow_p10:.8e},"
        f"{slow_p50:.8e},"
        f"{slow_p90:.8e}",
        flush=True,
    )

    print(
        "PRODUCTIVE_MIN_NULL_OVER_RHO_P10_P50_P90="
        f"{null_p10:.8e},"
        f"{null_p50:.8e},"
        f"{null_p90:.8e}",
        flush=True,
    )

    print(
        "PRODUCTIVE_TRANSVERSE_PAIR_OVER_RHO_P10_P50_P90="
        f"{trans_p10:.8e},"
        f"{trans_p50:.8e},"
        f"{trans_p90:.8e}",
        flush=True,
    )

    print(
        "NEGATIVE_ACTIVE_REGION_ENERGY_FRACTION="
        f"{negative_active_energy_fraction:.15e}",
        flush=True,
    )

    print(
        "GROSS_OUTWARD_FROM_NEGATIVE_ACTIVE_FRACTION="
        f"{gross_outward_from_negative_active:.15e}",
        flush=True,
    )

    print(
        "GROSS_OUTWARD_FROM_NEAR_NEC_SATURATION_FRACTION="
        f"{gross_outward_near_nec_fraction:.15e}",
        flush=True,
    )

    print(
        "POINT_FORCE_F90_ENERGY_FRACTION="
        f"{f90_energy_fraction:.15e}",
        flush=True,
    )

    # --------------------------------------------------------------
    # Photon directions in the plane transverse to the same radial
    # line.  This ensures RADIAL is a true transverse bending
    # direction for every tested photon propagation vector.
    # --------------------------------------------------------------

    e1, e2b = transverse_basis(
        RADIAL
    )

    rows = []

    print(
        "\n=== TRANSVERSE NULL-DIRECTION SCAN ===",
        flush=True,
    )

    for j in range(
        N_NULL_DIRECTIONS
    ):
        theta = (
            2.0
            * math.pi
            * j
            / N_NULL_DIRECTIONS
        )

        k = (
            math.cos(theta)
            * e1
            +
            math.sin(theta)
            * e2b
        )

        k /= np.linalg.norm(
            k
        )

        p_k = np.einsum(
            "nij,i,j->n",
            stress_f,
            k,
            k,
        )

        null_source = (
            rho_f
            + p_k
        )

        null_min_here = float(
            np.min(
                null_source
                / (
                    rho_f
                    + np.abs(
                        p_k
                    )
                    + 1e-14
                )
            )
        )

        null_total = float(
            np.sum(
                null_source
            )
            * volume
        )

        null_radial = float(
            np.sum(
                null_source
                * kernel
            )
        )

        null_l1 = float(
            np.sum(
                np.abs(
                    null_source
                    * kernel
                )
            )
        )

        null_cancel = (
            null_l1
            / max(
                abs(
                    null_radial
                ),
                1e-300,
            )
        )

        sign = (
            "OUTWARD"
            if null_radial > 0.0
            else "INWARD"
            if null_radial < 0.0
            else "ZERO"
        )

        rows.append(
            {
                "index":
                    j,
                "theta_rad":
                    theta,
                "kx":
                    float(
                        k[0]
                    ),
                "ky":
                    float(
                        k[1]
                    ),
                "kz":
                    float(
                        k[2]
                    ),
                "min_null_source_scaled":
                    null_min_here,
                "integrated_null_source":
                    null_total,
                "radial_bending_driver":
                    null_radial,
                "sign":
                    sign,
                "cancellation":
                    null_cancel,
            }
        )

        print(
            f"NULL_{j:02d} "
            f"THETA={theta:.8f} "
            f"RADIAL_DRIVER={null_radial:.15e} "
            f"SIGN={sign} "
            f"NULL_TOTAL={null_total:.15e}",
            flush=True,
        )

    null_values = np.array(
        [
            row[
                "radial_bending_driver"
            ]
            for row in rows
        ]
    )

    all_null_inward = bool(
        np.all(
            null_values < 0.0
        )
    )

    all_null_outward = bool(
        np.all(
            null_values > 0.0
        )
    )

    if (
        massive_radial > 0.0
        and all_null_inward
    ):
        split = (
            "PRESENT_SLOW_OUTWARD_NULL_INWARD"
        )

    elif (
        massive_radial > 0.0
        and all_null_outward
    ):
        split = (
            "ABSENT_BOTH_OUTWARD"
        )

    else:
        split = (
            "MIXED_OR_UNRESOLVED"
        )

    print(
        "\n=== 026L1 MECHANISM RESULT ===",
        flush=True,
    )

    print(
        f"TIMELIKE_NULL_SIGN_SPLIT={split}",
        flush=True,
    )

    print(
        "NULL_RADIAL_DRIVER_MIN="
        f"{np.min(null_values):.15e}",
        flush=True,
    )

    print(
        "NULL_RADIAL_DRIVER_MAX="
        f"{np.max(null_values):.15e}",
        flush=True,
    )

    print(
        "NULL_RADIAL_DRIVER_MEAN="
        f"{np.mean(null_values):.15e}",
        flush=True,
    )

    print(
        "LOCAL_DEC_NEGATIVE_ACTIVE_CEILING="
        "S_SLOW_GE_MINUS_2_RHO",
        flush=True,
    )

    # Conservative interpretation only.
    if (
        dec_p50 >= 0.75
    ):
        leverage_class = (
            "PRODUCTIVE_REGION_ALREADY_USES_STRONG_DEC_STRESS_LEVERAGE"
        )

        next_clue = (
            "PRIORITIZE_KERNEL_PARTICIPATION_AND_CANCELLATION_OVER_MORE_LOCAL_STRESS"
        )

    elif (
        dec_p50 <= 0.35
    ):
        leverage_class = (
            "SUBSTANTIAL_LOCAL_DEC_STRESS_HEADROOM_REMAINS"
        )

        next_clue = (
            "CONSTITUTIVE_STRESS_AND_GEOMETRY_BOTH_REMAIN_PLAUSIBLE_IMPROVEMENT_AXES"
        )

    else:
        leverage_class = (
            "INTERMEDIATE_DEC_STRESS_LEVERAGE"
        )

        next_clue = (
            "COMBINE_STRESS_LEVERAGE_WITH_KERNEL_AND_PARTICIPATION_IMPROVEMENT"
        )

    print(
        "PRODUCTIVE_STRESS_LEVERAGE_CLASS="
        f"{leverage_class}",
        flush=True,
    )

    print(
        f"PRACTICALITY_CLUE={next_clue}",
        flush=True,
    )

    result = {
        "simulation":
            "026L1",

        "branch":
            "TRUE_ANTIGRAVITY",

        "field":
            {
                "B":
                    B,
                "N":
                    73,
                "eta":
                    ETA,
                "m":
                    MASS,
            },

        "lineage":
            {
                "n73_green":
                    True,
            },

        "identities":
            {
                "active_source_stress_maxrel":
                    active_identity_rel,
                "min_null_source_scaled":
                    null_min_scaled,
                "all_null_directions_nonnegative":
                    null_source_pass,
                "laue_stress_over_energy":
                    laue_ratio,
            },

        "slow_matter":
            {
                "point_radial_driver":
                    massive_radial,
                "sign":
                    (
                        "OUTWARD"
                        if massive_radial > 0.0
                        else "INWARD"
                    ),
                "gross_outward":
                    massive_out,
                "gross_inward":
                    massive_in,
                "cancellation_factor":
                    massive_cancel,
            },

        "productive_anatomy":
            {
                "dec_trace_leverage_p10_p50_p90":
                    [
                        dec_p10,
                        dec_p50,
                        dec_p90,
                    ],
                "s_over_rho_p10_p50_p90":
                    [
                        slow_p10,
                        slow_p50,
                        slow_p90,
                    ],
                "min_null_over_rho_p10_p50_p90":
                    [
                        null_p10,
                        null_p50,
                        null_p90,
                    ],
                "transverse_pair_over_rho_p10_p50_p90":
                    [
                        trans_p10,
                        trans_p50,
                        trans_p90,
                    ],
                "negative_active_energy_fraction":
                    negative_active_energy_fraction,
                "gross_outward_from_negative_active_fraction":
                    gross_outward_from_negative_active,
                "gross_outward_near_nec_fraction":
                    gross_outward_near_nec_fraction,
                "point_force_f90_energy_fraction":
                    f90_energy_fraction,
                "classification":
                    leverage_class,
            },

        "null_probe":
            {
                "directions":
                    N_NULL_DIRECTIONS,
                "radial_driver_min":
                    float(
                        np.min(
                            null_values
                        )
                    ),
                "radial_driver_max":
                    float(
                        np.max(
                            null_values
                        )
                    ),
                "radial_driver_mean":
                    float(
                        np.mean(
                            null_values
                        )
                    ),
                "all_inward":
                    all_null_inward,
                "all_outward":
                    all_null_outward,
                "timelike_null_sign_split":
                    split,
            },

        "practicality_clue":
            next_clue,

        "claims":
            {
                "integrated_photon_deflection_angle":
                    False,
                "nonlinear_gr":
                    False,
                "stability":
                    False,
                "energy_scaling_improved":
                    False,
                "practical_antigravity_device":
                    False,
            },
    }

    OUT_JSON.write_text(
        json.dumps(
            result,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )

    with OUT_CSV.open(
        "w",
        newline="",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=list(
                rows[0].keys()
            ),
        )
        writer.writeheader()
        writer.writerows(
            rows
        )

    print(
        f"OUT_JSON={OUT_JSON}",
        flush=True,
    )

    print(
        f"OUT_CSV={OUT_CSV}",
        flush=True,
    )

    print(
        "026L1_DECISION=MECHANISM_DIAGNOSTIC_COMPLETE",
        flush=True,
    )

    print(
        "HEURISTIC_INCREASE_AUTHORIZED=NO",
        flush=True,
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO",
        flush=True,
    )


if __name__ == "__main__":
    main()
