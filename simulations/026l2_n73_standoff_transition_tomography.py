#!/usr/bin/env python3
"""026L2 — N73 stand-off transition and signed-kernel tomography.

PURPOSE
-------
Perform a quick, read-only mechanism diagnostic on the already-green strict
N=73 B=7, eta=0.4, m=8 Skyrmion.

026L1 found:

    slow-matter radial driver > 0

at the audited payload location while the source/payload geometry exhibited
extreme cancellation.

The present run asks the more important geometry question:

    Does outward gravity survive as the payload is moved OUTSIDE the
    microscopic source?

This distinguishes:

CLASS B — embedded/two-sided outward gravity:
    S+ K+ can pull the payload outward toward positive active source lying
    beyond it.

from

CLASS A-LIKE — one-sided repulsive geometry:
    source is overwhelmingly behind the payload and the useful channel is

        S- K- > 0.

This is a diagnostic only.  A noncompact Skyrmion tail prevents us from calling
an energy-percentile criterion strict compact-support stand-off.

SIGNED LEDGER
-------------
For active source

    S = rho + Tr(T),

and signed radial Green-function kernel K,

the force contribution is

    I = S K.

Four channels are reconstructed separately:

    S+ K+ : outward far-side attraction
    S+ K- : inward near-side attraction
    S- K+ : inward far-side negative-active response
    S- K- : outward true-repulsive channel

The sum of all four must reconstruct the total driver.

SOURCE-EXCLUSION TOMOGRAPHY
---------------------------
For source coordinate projected onto the payload radial unit vector n,

    q = x dot n,

and payload center

    c = d n,

cells with

    q > d

lie beyond the payload plane.

We calculate the fractions of total energy and |S| beyond that plane.

The scan explicitly includes locations at which only approximately

    10%, 5%, 1%, 0.1%, 0.01%

of source energy remains beyond the payload.

An outward response at the 0.1% or 0.01% level would be evidence for an
effective one-sided outward point field in the actual B7 realization.

It would NOT yet establish:
- strict compact-support stand-off;
- finite-payload stand-off;
- continuum force convergence;
- stability;
- nonlinear GR;
- practical antigravity.

DEC-CONDITIONED REPULSIVE LEVERAGE
----------------------------------
026L1's aggregate productive DEC statistic mixed ordinary far-side attraction
with true negative-active repulsion.

Here the DEC leverage

    Lambda_DEC = -S / (2 rho)

is evaluated ONLY in cells satisfying

    S < 0
    K < 0

so that

    S K > 0.

This directly measures how strongly the genuine repulsive channel uses the
local type-I DEC limit

    S >= -2 rho.

NULL COMPANION
--------------
Eight photon propagation directions perpendicular to the payload radial
direction are also evaluated using

    S_gamma(k) = rho + k_i T_ij k_j.

This remains a weak-field null-kernel diagnostic, not a complete integrated
lensing angle.

VALIDATION
----------
- green N73 lineage required;
- S^3 normalization checked;
- active-source identity checked;
- exact analytic prism formula independently validated;
- original d=0.387016... point force must reproduce the 026L1 result;
- signed ledger must reconstruct total force to floating-point precision;
- positive total active source gives inward far-field limiting behavior.

OUTPUT
------
results/data/026l2_n73_standoff_transition_summary.json
results/data/026l2_n73_standoff_transition_scan.csv
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
    "026l2_n73_standoff_transition_summary.json"
)

OUT_CSV = (
    ROOT
    / "results/data/"
    "026l2_n73_standoff_transition_scan.csv"
)

B = 7
ETA = 0.4
MASS = 8.0

AUDITED_D = 3.870161274564900e-1

# Same worst-direction radial orientation used by 026L1.
RADIAL = np.array(
    [
        -4.543501844638e-1,
        1.878880658051e-2,
        8.906250000000e-1,
    ],
    dtype=float,
)

RADIAL /= np.linalg.norm(
    RADIAL
)

EXPECTED_L1_DRIVER = (
    1.325019144674116e-1
)

N_NULL = 8


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

    target = (
        float(q)
        * total
    )

    return float(
        np.interp(
            target,
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


def transverse_basis(
    radial,
):
    refs = (
        np.array(
            [0.0, 0.0, 1.0]
        ),
        np.array(
            [0.0, 1.0, 0.0]
        ),
        np.array(
            [1.0, 0.0, 0.0]
        ),
    )

    for ref in refs:

        e1 = np.cross(
            radial,
            ref,
        )

        n = np.linalg.norm(
            e1
        )

        if n > 1.0e-8:

            e1 /= n

            e2 = np.cross(
                radial,
                e1,
            )

            e2 /= np.linalg.norm(
                e2
            )

            return (
                e1,
                e2,
            )

    raise RuntimeError(
        "Could not construct transverse basis"
    )


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

        field = (
            aqr.prism_field_many(
                lo,
                hi,
            )
        )

        out[start:stop] = (
            field
            @ radial
        )

    return out


def unique_sorted(
    values,
    tol=1.0e-8,
):
    values = sorted(
        float(x)
        for x in values
        if math.isfinite(
            float(x)
        )
        and float(x) > 0.0
    )

    out = []

    for x in values:

        if (
            not out
            or abs(
                x - out[-1]
            )
            >
            tol
            * max(
                1.0,
                abs(x),
                abs(out[-1]),
            )
        ):
            out.append(
                x
            )

    return out


def main():
    print(
        "=== 026L2 N73 STAND-OFF TRANSITION TOMOGRAPHY ===",
        flush=True,
    )

    prior = json.loads(
        SUMMARY73.read_text()
    )

    if (
        prior.get(
            "decision"
        )
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
        "S3_NORM_MAXERR="
        f"{normerr:.15e}",
        flush=True,
    )

    if normerr > 5.0e-10:
        raise RuntimeError(
            "S3 normalization failure"
        )

    cr3 = load_module(
        "l2_cr3",
        CR3_SOURCE,
    )

    aqr = load_module(
        "l2_aqr",
        AQR_SOURCE,
    )

    aqr.validate_analytic_formulae()

    print(
        "ANALYTIC_PRISM_KERNEL_AUDIT=PASS",
        flush=True,
    )

    print(
        "\n=== RECONSTRUCT N73 SOURCE ===",
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

    g = np.empty(
        e2.shape
        + (
            3,
            3,
        ),
        dtype=float,
    )

    g[..., 0, 0] = gxx
    g[..., 1, 1] = gyy
    g[..., 2, 2] = gzz

    g[..., 0, 1] = (
        g[..., 1, 0]
    ) = gxy

    g[..., 0, 2] = (
        g[..., 2, 0]
    ) = gxz

    g[..., 1, 2] = (
        g[..., 2, 1]
    ) = gyz

    g2 = np.einsum(
        "...ik,...kj->...ij",
        g,
        g,
    )

    eye = np.eye(
        3
    )

    stress = (
        2.0 * g
        - e2[..., None, None]
        * eye
        + 2.0
        * (
            e2[..., None, None]
            * g
            - g2
        )
        - e4[..., None, None]
        * eye
        - V[..., None, None]
        * eye
    )

    active_check = (
        rho
        + np.trace(
            stress,
            axis1=-2,
            axis2=-1,
        )
    )

    active_relerr = float(
        np.max(
            np.abs(
                active_check
                - active
            )
            / (
                rho
                + np.abs(
                    active
                )
                + np.abs(
                    active_check
                )
                + 1.0e-14
            )
        )
    )

    print(
        "ACTIVE_IDENTITY_MAXREL="
        f"{active_relerr:.15e}",
        flush=True,
    )

    if active_relerr > 1.0e-10:
        raise RuntimeError(
            "Active source identity failure"
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
        (
            X.ravel(),
            Y.ravel(),
            Z.ravel(),
        )
    )

    rho_f = rho.ravel()

    active_f = active.ravel()

    stress_f = stress.reshape(
        -1,
        3,
        3,
    )

    volume = (
        dx**3
    )

    energy_total = float(
        np.sum(
            rho_f
        )
        * volume
    )

    active_total = float(
        np.sum(
            active_f
        )
        * volume
    )

    abs_active_total = float(
        np.sum(
            np.abs(
                active_f
            )
        )
        * volume
    )

    print(
        f"TOTAL_ENERGY={energy_total:.15e}",
        flush=True,
    )

    print(
        f"TOTAL_ACTIVE={active_total:.15e}",
        flush=True,
    )

    if active_total <= 0.0:
        raise RuntimeError(
            "Expected positive far-field active mass"
        )

    # --------------------------------------------------------------
    # Source support relative to the chosen radial direction.
    # --------------------------------------------------------------

    projection = (
        xyz
        @ RADIAL
    )

    radius = np.linalg.norm(
        xyz,
        axis=1,
    )

    q90 = weighted_quantile(
        projection,
        rho_f,
        0.90,
    )

    q95 = weighted_quantile(
        projection,
        rho_f,
        0.95,
    )

    q99 = weighted_quantile(
        projection,
        rho_f,
        0.99,
    )

    q999 = weighted_quantile(
        projection,
        rho_f,
        0.999,
    )

    q9999 = weighted_quantile(
        projection,
        rho_f,
        0.9999,
    )

    r50 = weighted_quantile(
        radius,
        rho_f,
        0.50,
    )

    r90 = weighted_quantile(
        radius,
        rho_f,
        0.90,
    )

    r99 = weighted_quantile(
        radius,
        rho_f,
        0.99,
    )

    print(
        "\n=== SOURCE SUPPORT TOMOGRAPHY ===",
        flush=True,
    )

    print(
        "PROJECTED_ENERGY_Q90="
        f"{q90:.15e}",
        flush=True,
    )

    print(
        "PROJECTED_ENERGY_Q95="
        f"{q95:.15e}",
        flush=True,
    )

    print(
        "PROJECTED_ENERGY_Q99="
        f"{q99:.15e}",
        flush=True,
    )

    print(
        "PROJECTED_ENERGY_Q999="
        f"{q999:.15e}",
        flush=True,
    )

    print(
        "PROJECTED_ENERGY_Q9999="
        f"{q9999:.15e}",
        flush=True,
    )

    print(
        "RADIAL_ENERGY_R50="
        f"{r50:.15e}",
        flush=True,
    )

    print(
        "RADIAL_ENERGY_R90="
        f"{r90:.15e}",
        flush=True,
    )

    print(
        "RADIAL_ENERGY_R99="
        f"{r99:.15e}",
        flush=True,
    )

    # --------------------------------------------------------------
    # Precompute transverse null sources.
    # --------------------------------------------------------------

    e1, e2b = transverse_basis(
        RADIAL
    )

    null_sources = []

    for j in range(
        N_NULL
    ):

        theta = (
            2.0
            * math.pi
            * j
            / N_NULL
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

        null_sources.append(
            rho_f
            + p_k
        )

    null_sources = np.asarray(
        null_sources,
        dtype=float,
    )

    min_null = float(
        np.min(
            null_sources
        )
    )

    print(
        "MIN_SAMPLED_NULL_SOURCE="
        f"{min_null:.15e}",
        flush=True,
    )

    # --------------------------------------------------------------
    # Scan points:
    #
    # - original embedded payload;
    # - dense transition interval;
    # - projected 90...99.99% source-exclusion locations;
    # - radial support locations;
    # - explicit far-field sentinel.
    # --------------------------------------------------------------

    transition_end = max(
        q9999,
        AUDITED_D
        + 0.50,
    )

    scan_d = list(
        np.linspace(
            AUDITED_D,
            transition_end,
            10,
        )
    )

    scan_d.extend(
        [
            AUDITED_D,
            q90,
            q95,
            q99,
            q999,
            q9999,
            r90,
            r99,
            1.10 * q9999,
            1.25 * q9999,
            1.50 * q9999,
            2.00 * r99,
        ]
    )

    scan_d = unique_sorted(
        scan_d
    )

    print(
        "SCAN_POINT_COUNT="
        f"{len(scan_d)}",
        flush=True,
    )

    rows = []

    print(
        "\n=== EXACT SIGNED-KERNEL STAND-OFF SWEEP ===",
        flush=True,
    )

    for index, d in enumerate(
        scan_d
    ):

        center = (
            d
            * RADIAL
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

        net = float(
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

        l1 = float(
            np.sum(
                np.abs(
                    influence
                )
            )
        )

        cancellation = (
            l1
            / max(
                abs(net),
                1.0e-300,
            )
        )

        s_pos = (
            active_f >= 0.0
        )

        s_neg = ~s_pos

        k_pos = (
            kernel >= 0.0
        )

        k_neg = ~k_pos

        m_pp = (
            s_pos
            & k_pos
        )

        m_pm = (
            s_pos
            & k_neg
        )

        m_np = (
            s_neg
            & k_pos
        )

        m_nm = (
            s_neg
            & k_neg
        )

        spp = float(
            np.sum(
                influence[
                    m_pp
                ]
            )
        )

        spm = float(
            np.sum(
                influence[
                    m_pm
                ]
            )
        )

        snp = float(
            np.sum(
                influence[
                    m_np
                ]
            )
        )

        snm = float(
            np.sum(
                influence[
                    m_nm
                ]
            )
        )

        ledger_sum = (
            spp
            + spm
            + snp
            + snm
        )

        ledger_relerr = (
            abs(
                ledger_sum
                - net
            )
            / max(
                abs(net),
                l1,
                1.0e-300,
            )
        )

        if ledger_relerr > 1.0e-12:
            raise RuntimeError(
                "Signed ledger reconstruction failure"
            )

        embedded_positive_out = max(
            spp,
            0.0,
        )

        true_repulsive_out = max(
            snm,
            0.0,
        )

        embedded_fraction = (
            embedded_positive_out
            / max(
                gross_out,
                1.0e-300,
            )
        )

        true_repulsive_fraction = (
            true_repulsive_out
            / max(
                gross_out,
                1.0e-300,
            )
        )

        ahead = (
            projection > d
        )

        ahead_energy = float(
            np.sum(
                rho_f[
                    ahead
                ]
            )
            * volume
            / max(
                energy_total,
                1.0e-300,
            )
        )

        ahead_abs_active = float(
            np.sum(
                np.abs(
                    active_f[
                        ahead
                    ]
                )
            )
            * volume
            / max(
                abs_active_total,
                1.0e-300,
            )
        )

        # Genuine repulsive-channel DEC leverage:
        #
        # S<0 and K<0 only.
        repulsive_mask = (
            m_nm
            & (
                influence > 0.0
            )
            & (
                rho_f > 0.0
            )
        )

        lambda_dec = np.zeros_like(
            rho_f
        )

        lambda_dec[
            repulsive_mask
        ] = (
            -active_f[
                repulsive_mask
            ]
            / (
                2.0
                * rho_f[
                    repulsive_mask
                ]
            )
        )

        if np.any(
            repulsive_mask
        ):

            repulsive_weights = np.where(
                repulsive_mask,
                influence,
                0.0,
            )

            (
                dec10,
                dec50,
                dec90,
            ) = weighted_quantiles(
                lambda_dec,
                repulsive_weights,
            )

        else:

            dec10 = math.nan
            dec50 = math.nan
            dec90 = math.nan

        null_driver = (
            null_sources
            @ kernel
        )

        null_min_driver = float(
            np.min(
                null_driver
            )
        )

        null_max_driver = float(
            np.max(
                null_driver
            )
        )

        null_mean_driver = float(
            np.mean(
                null_driver
            )
        )

        null_class = (
            "ALL_INWARD"
            if null_max_driver < 0.0
            else
            "ALL_OUTWARD"
            if null_min_driver > 0.0
            else
            "MIXED"
        )

        sign = (
            "OUTWARD"
            if net > 0.0
            else
            "INWARD"
            if net < 0.0
            else
            "ZERO"
        )

        if ahead_energy <= 1.0e-4:
            geometry = (
                "EFFECTIVE_99P99_ENERGY_BEHIND"
            )

        elif ahead_energy <= 1.0e-3:
            geometry = (
                "EFFECTIVE_99P9_ENERGY_BEHIND"
            )

        elif ahead_energy <= 1.0e-2:
            geometry = (
                "EFFECTIVE_99_ENERGY_BEHIND"
            )

        else:
            geometry = (
                "EMBEDDED_OR_TWO_SIDED"
            )

        row = {
            "index":
                index,
            "d":
                d,
            "d_over_r99":
                d
                / r99,
            "slow_driver":
                net,
            "sign":
                sign,
            "gross_outward":
                gross_out,
            "gross_inward":
                gross_in,
            "cancellation":
                cancellation,
            "Splus_Kplus":
                spp,
            "Splus_Kminus":
                spm,
            "Sminus_Kplus":
                snp,
            "Sminus_Kminus":
                snm,
            "embedded_positive_fraction_gross_out":
                embedded_fraction,
            "true_repulsive_fraction_gross_out":
                true_repulsive_fraction,
            "energy_ahead_fraction":
                ahead_energy,
            "abs_active_ahead_fraction":
                ahead_abs_active,
            "repulsive_DEC_p10":
                dec10,
            "repulsive_DEC_p50":
                dec50,
            "repulsive_DEC_p90":
                dec90,
            "null_driver_min":
                null_min_driver,
            "null_driver_mean":
                null_mean_driver,
            "null_driver_max":
                null_max_driver,
            "null_class":
                null_class,
            "geometry_class":
                geometry,
        }

        rows.append(
            row
        )

        print(
            "SCAN "
            f"I={index:02d} "
            f"D={d:.9e} "
            f"D_R99={d/r99:.6f} "
            f"F={net:+.12e} "
            f"SIGN={sign} "
            f"E_AHEAD={ahead_energy:.6e} "
            f"S+K+={spp:+.8e} "
            f"S-K-={snm:+.8e} "
            f"EMBED_OUT_FRAC={embedded_fraction:.6f} "
            f"TRUE_REP_OUT_FRAC={true_repulsive_fraction:.6f} "
            f"DEC50={dec50:.6f} "
            f"NULL={null_class} "
            f"GEOM={geometry}",
            flush=True,
        )

    # --------------------------------------------------------------
    # Reproduce 026L1 audited d=0.387016...
    # --------------------------------------------------------------

    nearest = min(
        rows,
        key=lambda r: abs(
            r["d"]
            - AUDITED_D
        ),
    )

    if abs(
        nearest["d"]
        - AUDITED_D
    ) > 1.0e-10:
        raise RuntimeError(
            "Audited point missing from scan"
        )

    l1_relerr = (
        abs(
            nearest[
                "slow_driver"
            ]
            - EXPECTED_L1_DRIVER
        )
        / max(
            abs(
                EXPECTED_L1_DRIVER
            ),
            1.0e-300,
        )
    )

    print(
        "\n=== 026L1 REPRODUCTION ===",
        flush=True,
    )

    print(
        "L1_DRIVER_REPRO_RELERR="
        f"{l1_relerr:.15e}",
        flush=True,
    )

    if l1_relerr > 1.0e-10:
        raise RuntimeError(
            "026L1 point-driver reproduction failed"
        )

    print(
        "L1_DRIVER_REPRO=PASS",
        flush=True,
    )

    # --------------------------------------------------------------
    # Locate sign changes in the sampled radial field.
    # --------------------------------------------------------------

    crossings = []

    for a, b_row in zip(
        rows[:-1],
        rows[1:],
    ):

        fa = float(
            a["slow_driver"]
        )

        fb = float(
            b_row[
                "slow_driver"
            ]
        )

        if (
            fa == 0.0
            or fb == 0.0
            or fa * fb < 0.0
        ):

            da = float(
                a["d"]
            )

            db = float(
                b_row[
                    "d"
                ]
            )

            # Linear interpolation scout only.
            if fb != fa:

                root = (
                    da
                    - fa
                    * (
                        db - da
                    )
                    / (
                        fb - fa
                    )
                )

            else:
                root = (
                    0.5
                    * (
                        da + db
                    )
                )

            crossings.append(
                {
                    "d_left":
                        da,
                    "d_right":
                        db,
                    "f_left":
                        fa,
                    "f_right":
                        fb,
                    "linear_root":
                        float(
                            root
                        ),
                }
            )

    effective_99 = [
        r
        for r in rows
        if (
            r[
                "energy_ahead_fraction"
            ]
            <= 1.0e-2
        )
    ]

    effective_999 = [
        r
        for r in rows
        if (
            r[
                "energy_ahead_fraction"
            ]
            <= 1.0e-3
        )
    ]

    effective_9999 = [
        r
        for r in rows
        if (
            r[
                "energy_ahead_fraction"
            ]
            <= 1.0e-4
        )
    ]

    outward_99 = [
        r
        for r in effective_99
        if r[
            "slow_driver"
        ]
        > 0.0
    ]

    outward_999 = [
        r
        for r in effective_999
        if r[
            "slow_driver"
        ]
        > 0.0
    ]

    outward_9999 = [
        r
        for r in effective_9999
        if r[
            "slow_driver"
        ]
        > 0.0
    ]

    # Far-field sentinel is the largest d.
    far = rows[-1]

    farfield_expected = bool(
        far[
            "slow_driver"
        ]
        < 0.0
    )

    print(
        "\n=== STAND-OFF TRANSITION RESULT ===",
        flush=True,
    )

    print(
        "SIGN_CROSSING_COUNT="
        f"{len(crossings)}",
        flush=True,
    )

    for i, cross in enumerate(
        crossings
    ):
        print(
            f"SIGN_CROSSING_{i}_BRACKET="
            f"{cross['d_left']:.9e},"
            f"{cross['d_right']:.9e} "
            f"LINEAR_ROOT="
            f"{cross['linear_root']:.9e}",
            flush=True,
        )

    print(
        "OUTWARD_WITH_99_PERCENT_ENERGY_BEHIND="
        + (
            "YES"
            if outward_99
            else "NO"
        ),
        flush=True,
    )

    print(
        "OUTWARD_WITH_99P9_PERCENT_ENERGY_BEHIND="
        + (
            "YES"
            if outward_999
            else "NO"
        ),
        flush=True,
    )

    print(
        "OUTWARD_WITH_99P99_PERCENT_ENERGY_BEHIND="
        + (
            "YES"
            if outward_9999
            else "NO"
        ),
        flush=True,
    )

    print(
        "FAR_FIELD_DRIVER="
        f"{far['slow_driver']:+.15e}",
        flush=True,
    )

    print(
        "POSITIVE_ACTIVE_MASS_FAR_FIELD_LIMIT_CHECK="
        + (
            "PASS"
            if farfield_expected
            else "FAIL"
        ),
        flush=True,
    )

    if not farfield_expected:
        raise RuntimeError(
            "Far-field limiting-case sign did not become inward"
        )

    # --------------------------------------------------------------
    # Identify the best genuinely repulsive sampled location.
    # --------------------------------------------------------------

    repulsive_candidates = [
        r
        for r in rows
        if (
            r[
                "slow_driver"
            ]
            > 0.0
            and
            r[
                "true_repulsive_fraction_gross_out"
            ]
            > 0.50
        )
    ]

    if repulsive_candidates:

        best_repulsive = max(
            repulsive_candidates,
            key=lambda r: r[
                "slow_driver"
            ],
        )

        best_repulsive_present = True

        print(
            "TRUE_REPULSIVE_DOMINANT_OUTWARD_POINT=PRESENT",
            flush=True,
        )

        print(
            "BEST_TRUE_REPULSIVE_D="
            f"{best_repulsive['d']:.15e}",
            flush=True,
        )

        print(
            "BEST_TRUE_REPULSIVE_DRIVER="
            f"{best_repulsive['slow_driver']:.15e}",
            flush=True,
        )

        print(
            "BEST_TRUE_REPULSIVE_ENERGY_AHEAD="
            f"{best_repulsive['energy_ahead_fraction']:.15e}",
            flush=True,
        )

        print(
            "BEST_TRUE_REPULSIVE_DEC50="
            f"{best_repulsive['repulsive_DEC_p50']:.15e}",
            flush=True,
        )

    else:

        best_repulsive = None

        best_repulsive_present = False

        print(
            "TRUE_REPULSIVE_DOMINANT_OUTWARD_POINT=NOT_FOUND",
            flush=True,
        )

    # --------------------------------------------------------------
    # Mechanism classification.
    # --------------------------------------------------------------

    if outward_9999:

        mechanism = (
            "EFFECTIVE_NEAR_ONE_SIDED_OUTWARD_POINT_FIELD_SURVIVES_99P99"
        )

        clue = (
            "MICROSCOPIC_FIELD_CONTAINS_STANDOFF_LIKE_REPULSIVE_HEADROOM"
        )

    elif outward_999:

        mechanism = (
            "EFFECTIVE_NEAR_ONE_SIDED_OUTWARD_POINT_FIELD_SURVIVES_99P9"
        )

        clue = (
            "PURSUE_NEGATIVE_ACTIVE_KERNEL_SEGREGATION_IN_ACTUAL_FIELD"
        )

    elif outward_99:

        mechanism = (
            "OUTWARD_RESPONSE_SURVIVES_TO_99_PERCENT_SOURCE_EXCLUSION"
        )

        clue = (
            "B7_HAS_PARTIAL_STANDOFF_LIKE_STRUCTURE_BUT_TAIL_OR_FARSIDE_SUPPORT_STILL_MATTERS"
        )

    else:

        mechanism = (
            "OUTWARD_RESPONSE_IS_PREDOMINANTLY_EMBEDDED_OR_TWO_SIDED"
        )

        clue = (
            "REORGANIZE_NEGATIVE_ACTIVE_CORE_AND_POSITIVE_SCAFFOLDING_BEFORE_MORE_LOCAL_STRESS"
        )

    print(
        "026L2_MECHANISM_CLASS="
        f"{mechanism}",
        flush=True,
    )

    print(
        "026L2_PRACTICALITY_CLUE="
        f"{clue}",
        flush=True,
    )

    # --------------------------------------------------------------
    # Persist.
    # --------------------------------------------------------------

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

    summary = {
        "simulation":
            "026L2",

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

        "support":
            {
                "projected_q90":
                    q90,
                "projected_q95":
                    q95,
                "projected_q99":
                    q99,
                "projected_q999":
                    q999,
                "projected_q9999":
                    q9999,
                "radial_r50":
                    r50,
                "radial_r90":
                    r90,
                "radial_r99":
                    r99,
            },

        "audit":
            {
                "active_identity_maxrel":
                    active_relerr,
                "l1_driver_reproduction_relerr":
                    l1_relerr,
                "positive_active_farfield_check":
                    farfield_expected,
            },

        "transition":
            {
                "crossings":
                    crossings,
                "outward_with_99_percent_energy_behind":
                    bool(
                        outward_99
                    ),
                "outward_with_99p9_percent_energy_behind":
                    bool(
                        outward_999
                    ),
                "outward_with_99p99_percent_energy_behind":
                    bool(
                        outward_9999
                    ),
                "true_repulsive_dominant_outward_point":
                    best_repulsive_present,
                "best_true_repulsive":
                    best_repulsive,
                "mechanism_class":
                    mechanism,
            },

        "practicality_clue":
            clue,

        "claims":
            {
                "strict_compact_support_standoff":
                    False,
                "finite_payload_standoff":
                    False,
                "continuum_force_convergence":
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
            summary,
            indent=2,
            sort_keys=True,
        )
        + "\n"
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
        "026L2_DECISION=STANDOFF_TRANSITION_DIAGNOSTIC_COMPLETE",
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
