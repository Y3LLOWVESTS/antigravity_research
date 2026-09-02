#!/usr/bin/env python3
"""024A3 — isorotation inertia-tomography and teacher-mechanism audit.

Purpose
-------
Test whether the existing healthy Skyrme kinetic structure, activated by a
stationary global SU(2) isorotation, can place high-active-stress energy in a
better finite-payload kernel region than the static B=7 field.

This is a fixed-field prefilter. It does not claim a self-consistent
isospinning solution, stability, hyperbolicity at finite frequency, reaction
momentum closure, nonlinear GR, or a device.

Core identity
-------------
Write phi=(sigma,pi), choose a unit isospin axis a, and at unit angular
frequency let

    u = (0, a x pi).

For the normalized Skyrme Lagrangian L=-H-Q-V used by the 023 branch, with
spatial derivatives q_i and spatial Gram matrix g_ij=q_i.q_j,

    t   = u.u,
    b_i = u.q_i,
    s   = tr(g).

The coefficient of Omega^2 in the energy density is

    k = t(1+s) - sum_i b_i^2 >= 0,

and the coefficient of Omega^2 in the active source S=T00+Tii is

    dS = 2 t(2+s) - 2 sum_i b_i^2 = 2(k+t).

Therefore the isorotational sector satisfies dS/k >= 2 where defined and can
access dS/k>2 without adding a new field or higher-derivative operator.

The dependence on a is quadratic. Define the 3x3 matrices

    T = |pi|^2 I - pi pi^T,
    C = sum_i (pi x q_i^pi)(pi x q_i^pi)^T,
    M_E = (1+s) T - C,
    M_S = 2[(2+s) T - C].

Then

    k  = a^T M_E a,
    dS = a^T M_S a.

For a fixed payload kernel K, integrate

    J_E = integral M_E dV,
    J_A = integral K M_S dV.

The best rigid-isorotation specific leverage is the largest generalized
Rayleigh quotient

    eta_iso = max_a (a^T J_A a)/(a^T J_E a),

found exactly by the 3x3 generalized eigenproblem

    J_A a = eta_iso J_E a.

The run independently verifies that eigen-solution with a Fibonacci isospin-
axis scan.

Teacher-mechanism audit
-----------------------
The Introspective N48 teacher is also decomposed into the four S/K sign
channels. Because its axisymmetric kernel has K>0 on the far side of the
payload, this determines how much raw outward response comes from positive
active source attracting the payload toward far-side stress-energy versus
negative active source repelling it from the near side.

The teacher remains a design diagnostic either way; this audit narrows what
mechanism should be copied by a microscopic successor.

Promotion
---------
No large isospinning field solve is authorized merely from a positive rigid
signal. Promotion requires cubic/quintic continuous-field reconstructions to
agree, quadrature/near-payload errors to be small, the predeclared baseline
axis to remain outward, J_E to be positive definite, and the improvement over
the static baseline to survive a conservative error bound.
"""

from __future__ import annotations

from dataclasses import dataclass
import csv
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
from typing import Any

import numpy as np
from scipy.linalg import eigh

ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results/data"

N65_ARTIFACT = DATA / "023cr4r_strict_stationary_b7_n65.npz"
CR3_SOURCE = SIM / "023cr3_geometric_degree_guarded_unrestricted_relaxation.py"
AQS_SOURCE = SIM / "023c2aqs_continuous_field_active_source_force_integration.py"
AQR_SOURCE = SIM / "023c2aqr_analytic_prism_exact_cap_payload_operator.py"
A2_SUMMARY = DATA / "024a2_explicit_omega_proca_teacher_match_summary.json"
TEACHER_ARCHIVE = DATA / "int14d_capped_thousandfold_final_refinement_N48.npz"

OUT_JSON = DATA / "024a3_isorotation_inertia_tomography_summary.json"
OUT_CSV = DATA / "024a3_isorotation_reconstruction_metrics.csv"
OUT_NPZ = DATA / "024a3_isorotation_inertia_matrices.npz"

B = 7
ETA = 0.4
MASS = 8.0
TEACHER_Q = 2.6496291391878843

GAIN_INTERNAL_TRIGGER = 0.05
REPRESENTATION_REL_TOL = 0.10
AXIS_DOT_MIN = 0.95
FIB_N = 4096
SAFETY_FACTOR = 5.0

MEANINGFUL_GAIN = 1.10
MAJOR_GAIN = 2.0
BREAKTHROUGH_SCALE_GAIN = 10.0

BATCH_POINTS = int(
    os.environ.get(
        "AG_024A3_BATCH_POINTS",
        "120000",
    )
)

FORCE_Q4 = (
    os.environ.get(
        "AG_024A3_FORCE_Q4",
        "AUTO",
    )
    .strip()
    .upper()
)


def require(path: Path) -> None:
    if not path.is_file():
        raise RuntimeError(
            f"Required file missing: {path}"
        )


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(
        name,
        path,
    )

    if (
        spec is None
        or spec.loader is None
    ):
        raise RuntimeError(
            f"Cannot import {path}"
        )

    mod = importlib.util.module_from_spec(
        spec
    )

    sys.modules[name] = mod
    spec.loader.exec_module(mod)

    return mod


def relerr(a: float, b: float) -> float:
    return (
        abs(a - b)
        / max(
            abs(a),
            abs(b),
            1.0e-300,
        )
    )


def sym(a: np.ndarray) -> np.ndarray:
    aa = np.asarray(a, float)
    return 0.5 * (aa + aa.T)


def fibonacci_sphere(n: int) -> np.ndarray:
    k = np.arange(
        n,
        dtype=float,
    )

    z = (
        1.0
        - 2.0
        * (k + 0.5)
        / n
    )

    r = np.sqrt(
        np.maximum(
            0.0,
            1.0 - z * z,
        )
    )

    golden = (
        math.pi
        * (
            3.0
            - math.sqrt(5.0)
        )
    )

    az = golden * k

    out = np.column_stack(
        (
            r * np.cos(az),
            r * np.sin(az),
            z,
        )
    )

    return (
        out
        / np.linalg.norm(
            out,
            axis=1,
        )[:, None]
    )


def teacher_audit(
    payload_radius_over_h: float,
) -> dict[str, Any]:
    require(TEACHER_ARCHIVE)

    with np.load(
        TEACHER_ARCHIVE,
        allow_pickle=False,
    ) as d:
        needed = (
            "r_edges",
            "z_edges",
            "r_centers",
            "z_centers",
            "volumes",
            "kernels",
            "e",
            "active_density",
        )

        missing = [
            k
            for k in needed
            if k not in d.files
        ]

        if missing:
            raise RuntimeError(
                "Teacher archive missing: "
                + ", ".join(missing)
            )

        r_centers = np.asarray(
            d["r_centers"],
            float,
        )

        z_centers = np.asarray(
            d["z_centers"],
            float,
        )

        volumes = np.asarray(
            d["volumes"],
            float,
        )

        kernels = np.asarray(
            d["kernels"],
            float,
        )

        e = np.asarray(
            d["e"],
            float,
        )

        S = np.asarray(
            d["active_density"],
            float,
        )

    if not (
        volumes.shape
        == kernels.shape
        == e.shape
        == S.shape
    ):
        raise RuntimeError(
            "Teacher array shape mismatch"
        )

    cell_force = S * kernels

    E = float(
        np.sum(
            e * volumes
        )
    )

    A = float(
        np.sum(
            cell_force
        )
    )

    outward = np.maximum(
        cell_force,
        0.0,
    )

    opposing = np.maximum(
        -cell_force,
        0.0,
    )

    gross_out = float(
        np.sum(outward)
    )

    gross_opp = float(
        np.sum(opposing)
    )

    cancellation = (
        gross_out + gross_opp
    ) / max(
        abs(A),
        1.0e-300,
    )

    spp = np.where(
        (S > 0.0)
        & (kernels > 0.0),
        cell_force,
        0.0,
    )

    spn = np.where(
        (S > 0.0)
        & (kernels < 0.0),
        cell_force,
        0.0,
    )

    snp = np.where(
        (S < 0.0)
        & (kernels > 0.0),
        cell_force,
        0.0,
    )

    snn = np.where(
        (S < 0.0)
        & (kernels < 0.0),
        cell_force,
        0.0,
    )

    ledger = {
        "Spos_Kpos":
            float(np.sum(spp)),
        "Spos_Kneg":
            float(np.sum(spn)),
        "Sneg_Kpos":
            float(np.sum(snp)),
        "Sneg_Kneg":
            float(np.sum(snn)),
    }

    ledger_rebuilt = sum(
        ledger.values()
    )

    R, Z = np.meshgrid(
        r_centers,
        z_centers,
        indexing="ij",
    )

    positive_attraction = np.maximum(
        spp,
        0.0,
    )

    negative_repulsion = np.maximum(
        snn,
        0.0,
    )

    positive_attr_total = float(
        np.sum(
            positive_attraction
        )
    )

    negative_rep_total = float(
        np.sum(
            negative_repulsion
        )
    )

    # Teacher coordinates use h=1 and
    # payload center z=1.
    far_center = Z > 1.0

    far_sphere = (
        Z
        >= 1.0
        + float(
            payload_radius_over_h
        )
    )

    near_sphere = (
        Z
        <= 1.0
        - float(
            payload_radius_over_h
        )
    )

    def frac(
        q: np.ndarray,
        mask: np.ndarray,
    ) -> float:
        return float(
            np.sum(
                q[mask]
            )
            / max(
                np.sum(q),
                1.0e-300,
            )
        )

    attr_centroid_r = float(
        np.sum(
            R
            * positive_attraction
        )
        / max(
            positive_attr_total,
            1.0e-300,
        )
    )

    attr_centroid_z = float(
        np.sum(
            Z
            * positive_attraction
        )
        / max(
            positive_attr_total,
            1.0e-300,
        )
    )

    e_ref = e[:, ::-1]
    s_ref = S[:, ::-1]

    e_sym = float(
        np.linalg.norm(
            e - e_ref
        )
        / max(
            np.linalg.norm(e),
            1.0e-300,
        )
    )

    s_sym = float(
        np.linalg.norm(
            S - s_ref
        )
        / max(
            np.linalg.norm(S),
            1.0e-300,
        )
    )

    attr_fraction_of_gross = (
        positive_attr_total
        / max(
            gross_out,
            1.0e-300,
        )
    )

    rep_fraction_of_gross = (
        negative_rep_total
        / max(
            gross_out,
            1.0e-300,
        )
    )

    if (
        attr_fraction_of_gross
        >= 0.90
    ):
        mechanism = (
            "POSITIVE_ACTIVE_FAR_KERNEL_"
            "ATTRACTION_DOMINATED"
        )

    elif (
        rep_fraction_of_gross
        >= 0.50
    ):
        mechanism = (
            "NEGATIVE_ACTIVE_NEAR_KERNEL_"
            "REPULSION_DOMINATED"
        )

    else:
        mechanism = (
            "MIXED_SIGN_MECHANISM"
        )

    return {
        "E":
            E,

        "A":
            A,

        "C":
            E
            / max(
                A,
                1.0e-300,
            ),

        "gross_outward":
            gross_out,

        "gross_opposing":
            gross_opp,

        "cancellation":
            cancellation,

        "ledger":
            ledger,

        "ledger_relerr":
            relerr(
                ledger_rebuilt,
                A,
            ),

        "positive_active_positive_kernel_fraction_of_gross_outward":
            attr_fraction_of_gross,

        "negative_active_negative_kernel_fraction_of_gross_outward":
            rep_fraction_of_gross,

        "positive_active_positive_kernel_far_of_payload_center_fraction":
            frac(
                positive_attraction,
                far_center,
            ),

        "positive_active_positive_kernel_fully_beyond_payload_sphere_fraction":
            frac(
                positive_attraction,
                far_sphere,
            ),

        "negative_active_negative_kernel_fully_near_of_payload_sphere_fraction":
            frac(
                negative_repulsion,
                near_sphere,
            ),

        "positive_channel_centroid_r_over_h":
            attr_centroid_r,

        "positive_channel_centroid_z_over_h":
            attr_centroid_z,

        "energy_reflection_relerr":
            e_sym,

        "active_reflection_relerr":
            s_sym,

        "mechanism_classification":
            mechanism,
    }


def load_n65():
    require(N65_ARTIFACT)

    with np.load(
        N65_ARTIFACT,
        allow_pickle=False,
    ) as d:
        phi = np.asarray(
            d["phi"],
            float,
        )

        axis = np.asarray(
            d["axis"],
            float,
        )

        dx = float(
            d["dx"]
        )

        b = (
            int(
                round(
                    float(d["B"])
                )
            )
            if "B" in d.files
            else B
        )

        eta = (
            float(d["eta"])
            if "eta" in d.files
            else ETA
        )

        mass = (
            float(d["mass"])
            if "mass" in d.files
            else MASS
        )

    if (
        phi.shape
        != (65, 65, 65, 4)
        or axis.shape
        != (65,)
    ):
        raise RuntimeError(
            "Unexpected N65 shape: "
            f"{phi.shape}, {axis.shape}"
        )

    if (
        b != B
        or abs(eta - ETA)
        > 1.0e-12
        or abs(mass - MASS)
        > 1.0e-12
    ):
        raise RuntimeError(
            "N65 metadata mismatch"
        )

    normerr = float(
        np.max(
            np.abs(
                np.sum(
                    phi * phi,
                    axis=-1,
                )
                - 1.0
            )
        )
    )

    if normerr > 5.0e-10:
        raise RuntimeError(
            "N65 S3 norm failure: "
            f"{normerr}"
        )

    return phi, axis, dx


def validate_local_formula(
    cr3,
    phi: np.ndarray,
    dx: float,
):
    qx, qy, qz = (
        cr3.central4_derivatives(
            phi,
            dx,
        )
    )

    center = phi[
        2:-2,
        2:-2,
        2:-2,
    ]

    qs = (
        qx,
        qy,
        qz,
    )

    g = np.empty(
        center.shape[:-1]
        + (3, 3),
        float,
    )

    for i, qi in enumerate(qs):
        for j, qj in enumerate(qs):
            g[..., i, j] = np.sum(
                qi * qj,
                axis=-1,
            )

    s = np.trace(
        g,
        axis1=-2,
        axis2=-1,
    )

    pi = center[..., 1:]

    pi2 = np.sum(
        pi * pi,
        axis=-1,
    )

    I3 = np.eye(3)

    T = (
        pi2[
            ...,
            None,
            None,
        ]
        * I3
        - pi[
            ...,
            :,
            None,
        ]
        * pi[
            ...,
            None,
            :,
        ]
    )

    C = np.zeros_like(T)

    for qi in qs:
        c = np.cross(
            pi,
            qi[..., 1:],
        )

        C += (
            c[
                ...,
                :,
                None,
            ]
            * c[
                ...,
                None,
                :,
            ]
        )

    ME = (
        (1.0 + s)[
            ...,
            None,
            None,
        ]
        * T
        - C
    )

    MS = (
        2.0
        * (
            (2.0 + s)[
                ...,
                None,
                None,
            ]
            * T
            - C
        )
    )

    flat = ME.reshape(
        -1,
        3,
        3,
    )

    stride = max(
        1,
        len(flat) // 25000,
    )

    evals = np.linalg.eigvalsh(
        flat[::stride]
    )

    min_me = float(
        np.min(evals)
    )

    ident = (
        MS
        - 2.0 * ME
        - 2.0 * T
    )

    ident_scale = max(
        float(
            np.max(
                np.abs(MS)
            )
        ),
        1.0,
    )

    ident_rel = float(
        np.max(
            np.abs(ident)
        )
        / ident_scale
    )

    return {
        "min_sampled_ME_eigenvalue":
            min_me,

        "MS_minus_2ME_minus_2T_scaled":
            ident_rel,

        "local_energy_PSD_pass":
            bool(
                min_me
                >= -2.0e-10
            ),

        "constitutive_identity_pass":
            bool(
                ident_rel
                <= 2.0e-12
            ),
    }


@dataclass
class MatIntegral:
    JE: np.ndarray
    JA: np.ndarray
    E0: float
    A0: float


def zero_integral():
    return MatIntegral(
        np.zeros((3, 3)),
        np.zeros((3, 3)),
        0.0,
        0.0,
    )


def add_integrals(
    a: MatIntegral,
    b: MatIntegral,
):
    return MatIntegral(
        a.JE + b.JE,
        a.JA + b.JA,
        a.E0 + b.E0,
        a.A0 + b.A0,
    )


def matrix_density_from_interp(
    interp,
    points: np.ndarray,
):
    u = np.asarray(
        interp(points),
        float,
    )

    ux = np.asarray(
        interp(
            points,
            nu=(1, 0, 0),
        ),
        float,
    )

    uy = np.asarray(
        interp(
            points,
            nu=(0, 1, 0),
        ),
        float,
    )

    uz = np.asarray(
        interp(
            points,
            nu=(0, 0, 1),
        ),
        float,
    )

    norm = np.linalg.norm(
        u,
        axis=1,
    )

    if float(
        np.min(norm)
    ) < 0.25:
        raise RuntimeError(
            "Spline field approaches "
            "zero norm"
        )

    ph = (
        u
        / norm[:, None]
    )

    def project(du):
        return (
            du
            - ph
            * np.sum(
                ph * du,
                axis=1,
            )[:, None]
        ) / norm[:, None]

    q = [
        project(ux),
        project(uy),
        project(uz),
    ]

    G = np.empty(
        (
            len(points),
            3,
            3,
        ),
        float,
    )

    for i in range(3):
        for j in range(3):
            G[:, i, j] = np.sum(
                q[i] * q[j],
                axis=1,
            )

    s = np.trace(
        G,
        axis1=1,
        axis2=2,
    )

    trG2 = np.sum(
        G * G,
        axis=(1, 2),
    )

    e4 = (
        0.5
        * (
            s * s
            - trG2
        )
    )

    sigma = ph[:, 0]

    V = (
        MASS
        * MASS
        * (1.0 - sigma)
        * (1.0 + ETA * sigma)
    )

    rho0 = (
        s
        + e4
        + V
    )

    active0 = (
        2.0
        * (
            e4
            - V
        )
    )

    pi = ph[:, 1:]

    pi2 = np.sum(
        pi * pi,
        axis=1,
    )

    T = (
        pi2[:, None, None]
        * np.eye(3)[
            None,
            :,
            :,
        ]
        - pi[:, :, None]
        * pi[:, None, :]
    )

    C = np.zeros_like(T)

    for qi in q:
        c = np.cross(
            pi,
            qi[:, 1:],
        )

        C += (
            c[:, :, None]
            * c[:, None, :]
        )

    ME = (
        (1.0 + s)[
            :,
            None,
            None,
        ]
        * T
        - C
    )

    MS = (
        2.0
        * (
            (2.0 + s)[
                :,
                None,
                None,
            ]
            * T
            - C
        )
    )

    return (
        ME,
        MS,
        rho0,
        active0,
    )


def integrate_cells_matrix(
    c2aqs,
    interp,
    lowers,
    offsets,
    weights,
    center,
    direction,
    radius,
    label,
):
    if lowers.size == 0:
        return zero_integral()

    n_q = offsets.shape[0]

    cells_per_batch = max(
        1,
        BATCH_POINTS
        // max(
            n_q,
            1,
        ),
    )

    out = zero_integral()

    n_cells = len(lowers)
    last = -1

    for start in range(
        0,
        n_cells,
        cells_per_batch,
    ):
        stop = min(
            start
            + cells_per_batch,
            n_cells,
        )

        lo = lowers[
            start:stop
        ]

        pts = (
            lo[:, None, :]
            + offsets[
                None,
                :,
                :,
            ]
        ).reshape(
            -1,
            3,
        )

        w = np.broadcast_to(
            weights[None, :],
            (
                len(lo),
                n_q,
            ),
        ).reshape(-1)

        (
            ME,
            MS,
            rho0,
            active0,
        ) = (
            matrix_density_from_interp(
                interp,
                pts,
            )
        )

        K = c2aqs.kernel_radial(
            pts,
            center,
            direction,
            radius,
        )

        JE = np.einsum(
            "n,nij->ij",
            w,
            ME,
            optimize=True,
        )

        JA = np.einsum(
            "n,nij->ij",
            w * K,
            MS,
            optimize=True,
        )

        E0 = float(
            np.sum(
                w * rho0
            )
        )

        A0 = float(
            np.sum(
                w
                * active0
                * K
            )
        )

        out = add_integrals(
            out,
            MatIntegral(
                JE,
                JA,
                E0,
                A0,
            ),
        )

        pct = int(
            100
            * stop
            / n_cells
        )

        if (
            pct // 20
            != last // 20
        ):
            print(
                f"{label}_PROGRESS="
                f"{stop}/{n_cells} "
                f"PERCENT={pct}",
                flush=True,
            )

            last = pct

    out.JE[:] = sym(
        out.JE
    )

    out.JA[:] = sym(
        out.JA
    )

    return out


def solve_generalized(
    m: MatIntegral,
):
    JE = sym(m.JE)
    JA = sym(m.JA)

    eval_E = np.linalg.eigvalsh(
        JE
    )

    if (
        float(
            np.min(eval_E)
        )
        <= 1.0e-12
        * max(
            float(
                np.max(eval_E)
            ),
            1.0,
        )
    ):
        raise RuntimeError(
            "Integrated isoinertia "
            "matrix not positive "
            f"definite: {eval_E}"
        )

    vals, vecs = eigh(
        JA,
        JE,
    )

    idx = int(
        np.argmax(vals)
    )

    a = np.asarray(
        vecs[:, idx],
        float,
    )

    a /= np.linalg.norm(a)

    eta = float(
        vals[idx]
    )

    eta0 = float(
        m.A0
        / m.E0
    )

    gain = (
        eta / eta0
        if eta0 != 0.0
        else float("nan")
    )

    return {
        "JE_eigenvalues":
            eval_E.tolist(),

        "generalized_eigenvalues":
            vals.tolist(),

        "axis":
            a.tolist(),

        "eta_iso":
            eta,

        "E0":
            float(m.E0),

        "A0":
            float(m.A0),

        "eta0":
            eta0,

        "gain":
            gain,
    }


def fibonacci_verify(
    m: MatIntegral,
    solved,
):
    axes = fibonacci_sphere(
        FIB_N
    )

    num = np.einsum(
        "ni,ij,nj->n",
        axes,
        m.JA,
        axes,
    )

    den = np.einsum(
        "ni,ij,nj->n",
        axes,
        m.JE,
        axes,
    )

    eta = num / den

    idx = int(
        np.argmax(eta)
    )

    best = float(
        eta[idx]
    )

    a_scan = axes[idx]
    a_eig = np.asarray(
        solved["axis"],
        float,
    )

    dot = float(
        abs(
            np.dot(
                a_scan,
                a_eig,
            )
        )
    )

    return {
        "scan_eta_max":
            best,

        "eigen_eta":
            float(
                solved[
                    "eta_iso"
                ]
            ),

        "relative_gap":
            relerr(
                best,
                float(
                    solved[
                        "eta_iso"
                    ]
                ),
            ),

        "nearest_best_axis_absdot":
            dot,
    }


def method_run(
    c2aqs,
    interp,
    far,
    near,
    offsets,
    center,
    direction,
    radius,
    method,
):
    tag = method.upper()

    far2 = integrate_cells_matrix(
        c2aqs,
        interp,
        far,
        *offsets["far2"],
        center,
        direction,
        radius,
        f"{tag}_ISO_FAR_Q2",
    )

    far3 = integrate_cells_matrix(
        c2aqs,
        interp,
        far,
        *offsets["far3"],
        center,
        direction,
        radius,
        f"{tag}_ISO_FAR_Q3",
    )

    nc = integrate_cells_matrix(
        c2aqs,
        interp,
        near,
        *offsets["near_coarse"],
        center,
        direction,
        radius,
        f"{tag}_ISO_NEAR_COARSE",
    )

    nf = integrate_cells_matrix(
        c2aqs,
        interp,
        near,
        *offsets["near_fine"],
        center,
        direction,
        radius,
        f"{tag}_ISO_NEAR_FINE",
    )

    q2 = add_integrals(
        far2,
        nf,
    )

    q3 = add_integrals(
        far3,
        nf,
    )

    near_test = add_integrals(
        far3,
        nc,
    )

    s2 = solve_generalized(q2)
    s3 = solve_generalized(q3)
    sn = solve_generalized(
        near_test
    )

    internal = max(
        abs(
            s3["gain"]
            - s2["gain"]
        ),
        abs(
            s3["gain"]
            - sn["gain"]
        ),
    )

    use_q4 = (
        FORCE_Q4 == "YES"
        or (
            FORCE_Q4 == "AUTO"
            and internal
            > GAIN_INTERNAL_TRIGGER
        )
    )

    if FORCE_Q4 == "NO":
        use_q4 = False

    best_int = q3
    best = s3
    s4 = None

    if use_q4:
        far4 = integrate_cells_matrix(
            c2aqs,
            interp,
            far,
            *offsets["far4"],
            center,
            direction,
            radius,
            f"{tag}_ISO_FAR_Q4",
        )

        q4 = add_integrals(
            far4,
            nf,
        )

        s4 = solve_generalized(
            q4
        )

        internal = max(
            internal,
            abs(
                s4["gain"]
                - s3["gain"]
            ),
        )

        best_int = q4
        best = s4

    fib = fibonacci_verify(
        best_int,
        best,
    )

    return {
        "method":
            method,

        "q2":
            s2,

        "q3":
            s3,

        "near_coarse":
            sn,

        "q4":
            s4,

        "q4_used":
            bool(use_q4),

        "best":
            best,

        "best_integral":
            best_int,

        "internal_gain_abs_error":
            float(internal),

        "fibonacci":
            fib,
    }


def clean_method(result):
    return {
        k: v
        for k, v
        in result.items()
        if k
        != "best_integral"
    }


def main() -> None:
    print(
        "=== 024A3 — ISOROTATION "
        "INERTIA TOMOGRAPHY + "
        "TEACHER MECHANISM AUDIT ===",
        flush=True,
    )

    for p in (
        N65_ARTIFACT,
        CR3_SOURCE,
        AQS_SOURCE,
        AQR_SOURCE,
        A2_SUMMARY,
        TEACHER_ARCHIVE,
    ):
        require(p)

    cr3 = load_module(
        "ag024a3_cr3",
        CR3_SOURCE,
    )

    c2aqs = load_module(
        "ag024a3_aqs",
        AQS_SOURCE,
    )

    aqr = load_module(
        "ag024a3_aqr",
        AQR_SOURCE,
    )

    aqr.validate_analytic_formulae()

    with A2_SUMMARY.open() as f:
        a2 = json.load(f)

    h = float(
        a2["payload"]["h"]
    )

    Rp = float(
        a2["payload"]["radius"]
    )

    direction = np.asarray(
        a2["payload"]["direction"],
        float,
    )

    direction /= np.linalg.norm(
        direction
    )

    center = (
        h
        * direction
    )

    expected_cubic = float(
        a2[
            "comparators"
        ][
            "continuous_baseline"
        ][
            "cubic_force"
        ]
    )

    expected_quintic = float(
        a2[
            "comparators"
        ][
            "continuous_baseline"
        ][
            "quintic_force"
        ]
    )

    print(
        "\n=== A — INTROSPECTIVE "
        "TEACHER MECHANISM AUDIT ===",
        flush=True,
    )

    ta = teacher_audit(
        Rp / h
    )

    for key in (
        "E",
        "A",
        "C",
        "gross_outward",
        "gross_opposing",
        "cancellation",
        "ledger_relerr",
        "positive_active_positive_kernel_fraction_of_gross_outward",
        "negative_active_negative_kernel_fraction_of_gross_outward",
        "positive_active_positive_kernel_far_of_payload_center_fraction",
        "positive_active_positive_kernel_fully_beyond_payload_sphere_fraction",
        "positive_channel_centroid_r_over_h",
        "positive_channel_centroid_z_over_h",
        "energy_reflection_relerr",
        "active_reflection_relerr",
    ):
        print(
            f"TEACHER_{key.upper()}="
            f"{float(ta[key]):.15e}"
        )

    for key, val in (
        ta["ledger"].items()
    ):
        print(
            "TEACHER_LEDGER_"
            f"{key.upper()}="
            f"{float(val):.15e}"
        )

    print(
        "TEACHER_OPERATIONAL_MECHANISM="
        f"{ta['mechanism_classification']}"
    )

    print(
        "TEACHER_RAW_17230X_STATUS="
        "DESIGN_DIAGNOSTIC_NOT_"
        "CONTINUUM_CERTIFIED"
    )

    print(
        "\n=== B — N65 / LOCAL "
        "ISOROTATION IDENTITIES ===",
        flush=True,
    )

    phi, axis, dx = load_n65()

    local = validate_local_formula(
        cr3,
        phi,
        dx,
    )

    print(
        f"N65_DX={dx:.15e}"
    )

    print(
        "PAYLOAD_AXIS_SELECTION="
        "BASELINE_MAX_FROM_024A1_"
        "BEFORE_ISOROTATION"
    )

    print(
        "PAYLOAD_DIRECTION="
        + ",".join(
            f"{x:.15e}"
            for x in direction
        )
    )

    print(
        f"PAYLOAD_H={h:.15e}"
    )

    print(
        f"PAYLOAD_RADIUS={Rp:.15e}"
    )

    print(
        "ISOROTATION_LOCAL_ME_"
        "MIN_EIG_SAMPLED="
        f"{local['min_sampled_ME_eigenvalue']:.15e}"
    )

    print(
        "ISOROTATION_CONSTITUTIVE_"
        "IDENTITY_SCALED_ERR="
        f"{local['MS_minus_2ME_minus_2T_scaled']:.15e}"
    )

    print(
        "ISOROTATION_LOCAL_ENERGY_PSD="
        + (
            "PASS"
            if local[
                "local_energy_PSD_pass"
            ]
            else "FAIL"
        )
    )

    print(
        "ISOROTATION_DS_MINUS_2K_"
        "EQUALS_2T="
        + (
            "PASS"
            if local[
                "constitutive_identity_pass"
            ]
            else "FAIL"
        )
    )

    print(
        "STANDARD_SKYRME_DEC_"
        "LITERATURE_THEOREM="
        "RETAINED_WITH_DYNAMIC_"
        "HYPERBOLICITY_CAVEAT"
    )

    print(
        "\n=== C — CONTINUOUS "
        "FINITE-PAYLOAD MATRIX "
        "CUBATURE SETUP ===",
        flush=True,
    )

    lowers = c2aqs.cell_lowers(
        axis
    )

    dmin = (
        c2aqs.min_distance_to_cells(
            lowers,
            dx,
            center,
        )
    )

    near_radius = (
        c2aqs.NEAR_RADIUS_DX
        * dx
    )

    near_mask = (
        dmin < near_radius
    )

    near = lowers[
        near_mask
    ]

    far = lowers[
        ~near_mask
    ]

    offsets = {
        "far2":
            c2aqs.composite_gauss_offsets(
                dx,
                2,
                1,
            ),

        "far3":
            c2aqs.composite_gauss_offsets(
                dx,
                3,
                1,
            ),

        "far4":
            c2aqs.composite_gauss_offsets(
                dx,
                4,
                1,
            ),

        "near_coarse":
            c2aqs.composite_gauss_offsets(
                dx,
                c2aqs.NEAR_GAUSS_ORDER,
                c2aqs.NEAR_COARSE_SUBDIV,
            ),

        "near_fine":
            c2aqs.composite_gauss_offsets(
                dx,
                c2aqs.NEAR_GAUSS_ORDER,
                c2aqs.NEAR_FINE_SUBDIV,
            ),
    }

    const_err = (
        c2aqs.constant_source_validation(
            aqr,
            axis,
            dx,
            far,
            near,
            center,
            direction,
            Rp,
            *offsets["far3"],
            *offsets["near_fine"],
        )
    )

    print(
        "CONSTANT_SOURCE_KERNEL_"
        "VALIDATION_RELERR="
        f"{const_err:.15e}"
    )

    if (
        const_err
        > c2aqs.FORCE_CONST_VALIDATION_REL_TOL
    ):
        raise RuntimeError(
            "Constant-source "
            "finite-payload "
            "validation failed"
        )

    results = {}

    for method in (
        "cubic",
        "quintic",
    ):
        print(
            f"\n=== D — {method.upper()} "
            "CONTINUOUS ISOROTATION "
            "TOMOGRAPHY ===",
            flush=True,
        )

        interp = (
            c2aqs.build_interpolator(
                axis,
                phi,
                method,
            )
        )

        nodal = (
            c2aqs.nodal_reproduction_check(
                interp,
                phi,
                axis,
                method,
            )
        )

        deriv = (
            c2aqs.finite_difference_derivative_check(
                interp,
                axis,
                dx,
                method,
            )
        )

        if (
            nodal
            > c2aqs.NODAL_REPRO_ABS_TOL
            or deriv
            > c2aqs.DERIVATIVE_REL_TOL
        ):
            raise RuntimeError(
                f"{method} spline "
                "validation failed"
            )

        r = method_run(
            c2aqs,
            interp,
            far,
            near,
            offsets,
            center,
            direction,
            Rp,
            method,
        )

        results[method] = r

        b = r["best"]
        fib = r["fibonacci"]

        print(
            f"{method.upper()}_BASELINE_E="
            f"{b['E0']:.15e}"
        )

        print(
            f"{method.upper()}_BASELINE_A="
            f"{b['A0']:.15e}"
        )

        print(
            f"{method.upper()}_BASELINE_ETA="
            f"{b['eta0']:.15e}"
        )

        print(
            f"{method.upper()}_ISO_ETA_OPT="
            f"{b['eta_iso']:.15e}"
        )

        print(
            f"{method.upper()}_ISO_GAIN_OPT="
            f"{b['gain']:.15e}"
        )

        print(
            f"{method.upper()}_ISO_AXIS="
            + ",".join(
                f"{x:.15e}"
                for x in b["axis"]
            )
        )

        print(
            f"{method.upper()}_INTERNAL_"
            "GAIN_ABSERR="
            f"{r['internal_gain_abs_error']:.15e}"
        )

        print(
            f"{method.upper()}_FIBONACCI_"
            "REL_GAP="
            f"{fib['relative_gap']:.15e}"
        )

        print(
            f"{method.upper()}_FIBONACCI_"
            "AXIS_ABSDOT="
            f"{fib['nearest_best_axis_absdot']:.15e}"
        )

        print(
            f"{method.upper()}_Q4_USED="
            + (
                "YES"
                if r["q4_used"]
                else "NO"
            )
        )

    c = results["cubic"]
    q = results["quintic"]

    cb = c["best"]
    qb = q["best"]

    gain_spread = abs(
        float(cb["gain"])
        - float(qb["gain"])
    )

    gain_scale = max(
        abs(
            float(
                cb["gain"]
            )
        ),
        abs(
            float(
                qb["gain"]
            )
        ),
        1.0,
    )

    gain_spread_rel = (
        gain_spread
        / gain_scale
    )

    axis_dot = float(
        abs(
            np.dot(
                np.asarray(
                    cb["axis"]
                ),
                np.asarray(
                    qb["axis"]
                ),
            )
        )
    )

    error_bound = max(
        c[
            "internal_gain_abs_error"
        ],
        q[
            "internal_gain_abs_error"
        ],
        gain_spread,
    )

    gain_floor_raw = min(
        float(
            cb["gain"]
        ),
        float(
            qb["gain"]
        ),
    )

    gain_floor_conservative = (
        gain_floor_raw
        - SAFETY_FACTOR
        * error_bound
    )

    cubic_base_rel = relerr(
        float(
            cb["A0"]
        ),
        expected_cubic,
    )

    quintic_base_rel = relerr(
        float(
            qb["A0"]
        ),
        expected_quintic,
    )

    baseline_reproduction = bool(
        cubic_base_rel
        <= 5.0e-3
        and quintic_base_rel
        <= 5.0e-3
    )

    fib_ok = bool(
        c["fibonacci"][
            "relative_gap"
        ]
        <= 3.0e-3
        and q["fibonacci"][
            "relative_gap"
        ]
        <= 3.0e-3
        and c["fibonacci"][
            "nearest_best_axis_absdot"
        ]
        >= 0.995
        and q["fibonacci"][
            "nearest_best_axis_absdot"
        ]
        >= 0.995
    )

    representation_ok = bool(
        gain_spread_rel
        <= REPRESENTATION_REL_TOL
        and axis_dot
        >= AXIS_DOT_MIN
    )

    baseline_outward = bool(
        float(
            cb["A0"]
        ) > 0.0
        and float(
            qb["A0"]
        ) > 0.0
    )

    local_ok = bool(
        local[
            "local_energy_PSD_pass"
        ]
        and local[
            "constitutive_identity_pass"
        ]
    )

    print(
        "\n=== E — CROSS-"
        "REPRESENTATION CERTIFICATE ===",
        flush=True,
    )

    print(
        "CUBIC_BASELINE_FORCE_RELERR_"
        "VS_024A2="
        f"{cubic_base_rel:.15e}"
    )

    print(
        "QUINTIC_BASELINE_FORCE_RELERR_"
        "VS_024A2="
        f"{quintic_base_rel:.15e}"
    )

    print(
        "BASELINE_024A2_REPRODUCTION="
        + (
            "PASS"
            if baseline_reproduction
            else "FAIL"
        )
    )

    print(
        "CUBIC_QUINTIC_GAIN_ABS_SPREAD="
        f"{gain_spread:.15e}"
    )

    print(
        "CUBIC_QUINTIC_GAIN_REL_SPREAD="
        f"{gain_spread_rel:.15e}"
    )

    print(
        "CUBIC_QUINTIC_AXIS_ABSDOT="
        f"{axis_dot:.15e}"
    )

    print(
        "GAIN_ERROR_BOUND_ABS="
        f"{error_bound:.15e}"
    )

    print(
        "GAIN_FLOOR_RAW="
        f"{gain_floor_raw:.15e}"
    )

    print(
        "GAIN_FLOOR_CONSERVATIVE_"
        "5SIGMA_STYLE="
        f"{gain_floor_conservative:.15e}"
    )

    print(
        "FIBONACCI_EIGEN_CROSSCHECK="
        + (
            "PASS"
            if fib_ok
            else "FAIL"
        )
    )

    print(
        "CUBIC_QUINTIC_REPRESENTATION="
        + (
            "PASS"
            if representation_ok
            else "FAIL"
        )
    )

    print(
        "\n=== F — FROZEN RIGID "
        "TOTAL-EFFICIENCY "
        "DIAGNOSTICS ===",
        flush=True,
    )

    energy_fraction_rows = []

    for x in (
        0.01,
        0.05,
        0.10,
        0.25,
        0.50,
        1.0,
    ):
        ratio = (
            1.0
            + gain_floor_conservative
            * x
        ) / (
            1.0 + x
        )

        energy_fraction_rows.append(
            {
                "Erot_over_Estatic":
                    x,

                "conservative_total_efficiency_ratio":
                    ratio,
            }
        )

        print(
            "FROZEN_EROT_OVER_E0="
            f"{x:.6e} "
            "CONSERVATIVE_TOTAL_ETA_RATIO="
            f"{ratio:.15e}"
        )

    print(
        "FROZEN_RIGID_DIAGNOSTIC_IS_NOT_"
        "FREQUENCY_OR_STATIONARITY_"
        "CERTIFICATE=YES"
    )

    all_health = bool(
        local_ok
        and baseline_reproduction
        and baseline_outward
        and fib_ok
        and representation_ok
    )

    if (
        all_health
        and gain_floor_conservative
        >= BREAKTHROUGH_SCALE_GAIN
    ):
        decision = (
            "GREEN_BREAKTHROUGH_SCALE_"
            "ISOROTATION_LEVERAGE_PREFILTER"
        )

        next_action = (
            "024B_COUPLED_B7_ISOSPINNING_"
            "ROUTHIAN_REEQUILIBRATION_WITH_"
            "T0I_HYPERBOLICITY_AND_"
            "FISSION_GATES"
        )

    elif (
        all_health
        and gain_floor_conservative
        >= MAJOR_GAIN
    ):
        decision = (
            "GREEN_MAJOR_ISOROTATION_"
            "LEVERAGE_PREFILTER"
        )

        next_action = (
            "024B_COUPLED_B7_ISOSPINNING_"
            "ROUTHIAN_REEQUILIBRATION_WITH_"
            "T0I_HYPERBOLICITY_AND_"
            "FISSION_GATES"
        )

    elif (
        all_health
        and gain_floor_conservative
        >= MEANINGFUL_GAIN
    ):
        decision = (
            "GREEN_MEANINGFUL_ISOROTATION_"
            "LEVERAGE_PREFILTER"
        )

        next_action = (
            "024B_REDUCED_ISOSPINNING_B7_"
            "ROUTHIAN_SCOUT_BEFORE_FULL_3D"
        )

    elif (
        gain_floor_raw > 1.0
        and not all_health
    ):
        decision = (
            "YELLOW_ISOROTATION_SIGNAL_"
            "NOT_NUMERICALLY_CERTIFIED"
        )

        next_action = (
            "024A3R_ISOROTATION_"
            "CONTINUUM_OR_AXIS_REPAIR"
        )

    else:
        decision = (
            "RED_RIGID_ISOROTATION_"
            "NO_CERTIFIED_EFFICIENCY_"
            "ADVANTAGE"
        )

        next_action = (
            "024A4_ALTERNATIVE_DYNAMIC_"
            "OR_GEOMETRY_REORGANIZING_"
            "FIELD_PREFILTER"
        )

    summary = {
        "claim_classification":
            "PROJECT_DERIVED_024A3_"
            "ISOROTATION_INERTIA_"
            "TOMOGRAPHY_PREFILTER",

        "teacher_audit":
            ta,

        "local_isorotation":
            local,

        "payload": {
            "h":
                h,

            "radius":
                Rp,

            "direction":
                direction.tolist(),

            "selection":
                "BASELINE_MAX_FROM_024A1_"
                "BEFORE_ISOROTATION",
        },

        "methods": {
            "cubic":
                clean_method(c),

            "quintic":
                clean_method(q),
        },

        "cross_representation": {
            "gain_abs_spread":
                gain_spread,

            "gain_rel_spread":
                gain_spread_rel,

            "axis_absdot":
                axis_dot,

            "error_bound_abs":
                error_bound,

            "gain_floor_raw":
                gain_floor_raw,

            "gain_floor_conservative":
                gain_floor_conservative,

            "baseline_reproduction":
                baseline_reproduction,

            "fibonacci_crosscheck":
                fib_ok,

            "representation_pass":
                representation_ok,

            "all_health":
                all_health,
        },

        "frozen_energy_fraction_diagnostics":
            energy_fraction_rows,

        "decision":
            decision,

        "next":
            next_action,

        "large_coupled_isospinning_solve_authorized":
            bool(
                decision.startswith(
                    "GREEN"
                )
            ),

        "claim_limits": {
            "rigid_fixed_field_only":
                True,

            "coupled_isospinning_stationary_solution":
                False,

            "full_conservation_on_reequilibrated_solution":
                False,

            "finite_frequency_hyperbolicity":
                False,

            "T0i_reaction_momentum_completion":
                False,

            "fission_stability":
                False,

            "nonlinear_einstein_matter":
                False,

            "practical_device":
                False,
        },

        "current_knowledge_heuristic":
            "APPROXIMATELY_70_TO_71_PERCENT_"
            "NOT_A_PROBABILITY",
    }

    OUT_JSON.write_text(
        json.dumps(
            summary,
            indent=2,
            allow_nan=True,
        )
        + "\n"
    )

    rows = []

    for method, r in (
        results.items()
    ):
        for level in (
            "q2",
            "q3",
            "q4",
            "near_coarse",
        ):
            ss = r.get(level)

            if ss is None:
                continue

            rows.append(
                {
                    "method":
                        method,

                    "level":
                        level,

                    "baseline_E":
                        ss["E0"],

                    "baseline_A":
                        ss["A0"],

                    "baseline_eta":
                        ss["eta0"],

                    "iso_eta":
                        ss["eta_iso"],

                    "iso_gain":
                        ss["gain"],

                    "axis_x":
                        ss["axis"][0],

                    "axis_y":
                        ss["axis"][1],

                    "axis_z":
                        ss["axis"][2],
                }
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
        writer.writerows(rows)

    np.savez_compressed(
        OUT_NPZ,

        cubic_JE=np.asarray(
            c[
                "best_integral"
            ].JE
        ),

        cubic_JA=np.asarray(
            c[
                "best_integral"
            ].JA
        ),

        quintic_JE=np.asarray(
            q[
                "best_integral"
            ].JE
        ),

        quintic_JA=np.asarray(
            q[
                "best_integral"
            ].JA
        ),

        cubic_axis=np.asarray(
            cb["axis"]
        ),

        quintic_axis=np.asarray(
            qb["axis"]
        ),

        payload_direction=
            direction,

        payload_h=np.array(h),

        payload_radius=
            np.array(Rp),
    )

    print(
        "\n=== G — 024A3 "
        "DECISION ===",
        flush=True,
    )

    print(
        "024A3_ISOROTATION_INERTIA_"
        "TOMOGRAPHY="
        f"{decision}"
    )

    print(
        "TEACHER_OPERATIONAL_MECHANISM="
        f"{ta['mechanism_classification']}"
    )

    print(
        "TEACHER_POSITIVE_ACTIVE_"
        "POSITIVE_KERNEL_GROSS_FRACTION="
        f"{ta['positive_active_positive_kernel_fraction_of_gross_outward']:.15e}"
    )

    print(
        "TEACHER_NEGATIVE_ACTIVE_"
        "NEGATIVE_KERNEL_GROSS_FRACTION="
        f"{ta['negative_active_negative_kernel_fraction_of_gross_outward']:.15e}"
    )

    print(
        f"CUBIC_ISO_GAIN="
        f"{float(cb['gain']):.15e}"
    )

    print(
        f"QUINTIC_ISO_GAIN="
        f"{float(qb['gain']):.15e}"
    )

    print(
        "CERTIFIED_CONSERVATIVE_"
        "GAIN_FLOOR="
        f"{gain_floor_conservative:.15e}"
    )

    print(
        "OPTIMAL_AXIS_CUBIC="
        + ",".join(
            f"{x:.15e}"
            for x
            in cb["axis"]
        )
    )

    print(
        "OPTIMAL_AXIS_QUINTIC="
        + ",".join(
            f"{x:.15e}"
            for x
            in qb["axis"]
        )
    )

    print(
        f"OPTIMAL_AXIS_ABSDOT="
        f"{axis_dot:.15e}"
    )

    print(
        "STANDARD_SKYRME_DEC="
        "SUPPORTED_BY_ESTABLISHED_THEOREM"
    )

    print(
        "FINITE_FREQUENCY_HYPERBOLICITY="
        "UNRESOLVED_REQUIRES_024B"
    )

    print(
        "T0I_AND_REACTION_MOMENTUM="
        "MANDATORY_IN_024B"
    )

    print(
        "RIGID_ISOROTATION_IS_NOT_"
        "COUPLED_STATIONARY_SOLUTION=YES"
    )

    print(
        "LARGE_COUPLED_ISOSPINNING_"
        "SOLVE_AUTHORIZED="
        + (
            "YES"
            if summary[
                "large_coupled_isospinning_solve_authorized"
            ]
            else "NO"
        )
    )

    print(
        f"NEXT={next_action}"
    )

    print(
        "CURRENT_KNOWLEDGE_HEURISTIC="
        "APPROXIMATELY_70_TO_71_PERCENT_"
        "NOT_A_PROBABILITY"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )

    print(
        "NEW_PHYSICS_DISCOVERY=NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_024A3_"
        "ISOROTATION_INERTIA_"
        "TOMOGRAPHY_PREFILTER"
    )

    print(
        "SUMMARY_JSON="
        f"{OUT_JSON.relative_to(ROOT)}"
    )

    print(
        "METRICS_CSV="
        f"{OUT_CSV.relative_to(ROOT)}"
    )

    print(
        "MATRICES_NPZ="
        f"{OUT_NPZ.relative_to(ROOT)}"
    )

    print(
        "024A3_RUN_COMPLETE=YES"
    )


if __name__ == "__main__":
    main()
