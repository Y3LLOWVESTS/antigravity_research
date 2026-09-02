#!/usr/bin/env python3
"""024A2 — explicit omega/Proca topological-mediator teacher-match prefilter.

PURPOSE
-------
Test a physically motivated successor to the local B_mu B^mu sextic route:
keep the isoscalar omega/Proca vector field explicit instead of integrating it
out into a local B0^2 operator.

SCIENTIFIC QUESTION
-------------------
Can a finite-range vector field sourced by the B=7 topological baryon density
move positive, near-DEC-saturating stress into a substantially better
finite-payload kernel location than both

1. the current false-core Skyrmion stress organization, and
2. the heavy-vector/local-sextic B0^2 limit tested in 024A1/024A1R?

WHY THIS MODEL
--------------
Introspective found a compact, payload-adjacent, low-cancellation teacher whose
force-weighted median active-source ratio is approximately

    (S/rho)_teacher = 2.649629,

with two principal stresses near +rho and a heterogeneous third stress.

For a healthy static Proca field in metric signature (-,+,+,+), take

    omega_mu = (omega_0, 0, 0, 0)

and define

    e_E = |grad omega_0|^2 / 2,
    e_m = mu^2 omega_0^2 / 2.

Then

    rho_omega = e_E + e_m,

and in the local frame whose first axis is parallel to grad omega_0,

    p_parallel = -e_E + e_m,
    p_perp_1   = +e_E + e_m = rho_omega,
    p_perp_2   = +e_E + e_m = rho_omega.

Therefore

    S_omega = rho + p_parallel + p_perp_1 + p_perp_2
            = 2 e_E + 4 e_m,

and

    S_omega/rho_omega = 2 + 2 f_m,

where

    f_m = e_m/(e_E+e_m).

Matching the Introspective teacher median requires exactly

    f_m = (2.649629 - 2)/2 = 0.3248145,

which gives the normalized principal-stress pattern

    (p_perp_1, p_perp_2, p_parallel)/rho
        = (1, 1, -0.350371).

This is the same constitutive target independently found in 024A for the
near-rank-2 L4+L6 limit, but the explicit vector field adds a crucial new
physical degree of freedom: finite-range spatial spreading.

MODEL
-----
The proposed successor class is a false-core omega-Skyrme model.
Schematically, with the project (-,+,+,+) convention,

    L = L_2 + L_4 - V
        - (1/4) W_{mu nu} W^{mu nu}
        - (1/2) mu_omega^2 omega_mu omega^mu
        + g_omega omega_mu B^mu.

The sign of the last term is conventional here; it is chosen so the static
field equation is

    (-nabla^2 + mu_omega^2) omega_0 = g_omega B_0.

The Wess-Zumino/topological-current interaction is metric independent in the
standard omega-Skyrme formulation and hence does not itself contribute to
T_{mu nu}. The Proca kinetic and mass terms have positive static energy.

The fixed-field specific gravitational leverage of the omega sector is
independent of g_omega because omega_0 is linear in g_omega while both its
stress-energy and energy scale as g_omega^2.

HEAVY-MASS LIMIT / INTERNAL FALSIFIER
-------------------------------------
For mu_omega much larger than the spatial variation scale,

    omega_0 ~= g_omega B_0 / mu_omega^2,

so the mass part of its energy approaches a local B0^2 shape and

    (A_omega/E_omega) ->

    4 integral(B0^2 K_P) dV
    -------------------------
       integral(B0^2) dV.

Thus this run contains its own control: increasing mu_omega must approach the
024A1 local-sextic placement. A genuine finite-range improvement must beat
that heavy/local limit at resolved mu_omega.

LITERATURE ANCHORS
------------------
- Adkins & Nappi, "Stabilization of Chiral Solitons via Vector Mesons" (1984).
- Gudnason & Speight, JHEP 07 (2020) 184, arXiv:2004.12862.
- Harland, Leask & Speight, JHEP 06 (2024) 116, arXiv:2404.11287.

OPERATIONAL OBSERVABLE
----------------------
For a uniform spherical payload centered at c = h n with radius Rp,

    K_P(q) = (n.q) / max(|q|^3, Rp^3),
    q = x - c.

Positive integral means outward acceleration in repository convention.

The fixed-field efficiency is

    eta = A/E.

For an infinitesimal addition of an independently scaled sector,
eta_sector/eta_baseline is the exact first-order gain ratio.

AXIS POLICY
-----------
024A1R established that an everywhere-positive additive active sector cannot
improve all spherical orientations simultaneously. This run therefore uses a
single orientation-locked device axis selected before seeing omega: the N=65
axis with maximum baseline A0 in the saved 024A1 320-direction array.

Because the old midpoint payload operator is not promotion-grade when Rp << dx,
that saved array is used only to select the axis. The baseline force on the
selected axis is then recomputed with repaired finite-payload machinery.

NUMERICAL METHOD
----------------
1. Load the strict-stationary N=65 field.
2. Reconstruct fourth-order B0, rho, e4 and S0.
3. Select the baseline-max 024A1R axis without looking at omega.
4. Re-evaluate the baseline along that axis with:
   a. exact rectangular-prism P0 point kernel plus a separately converged
      finite-payload compact correction;
   b. the existing independent cubic/quintic continuous-field source
      reconstruction when available.
5. Embed B0 in successively padded Cartesian domains and solve

       (-Delta_d + mu^2) omega = B0

   with a DST-I spectral inversion of the positive Dirichlet discrete
   operator.
6. Reconstruct the exact discrete Proca gradient and mass energy ledger.
7. Scan finite vector ranges mu*h.
8. Compare eta_omega against baseline, the local B0^2 heavy-limit comparator,
   and the current L4 sector.
9. For the best resolved candidates, repeat on larger padding and evaluate a
   repaired P0 finite-payload force rather than trusting a midpoint kernel.
10. Compare force-weighted S/rho and spatial concentration with the frozen
    Introspective teacher anatomy.

ENERGY / STRESS CONDITIONS
--------------------------
The isolated Proca sector has

    rho >= 0,
    |p_i| <= rho,
    2 <= S/rho <= 4,

so NEC/WEC/DEC hold pointwise for that sector.

CONSERVATION CAVEAT
-------------------
The fixed Skyrme field plus solved omega field used here is NOT a solution of
the coupled U+omega Euler-Lagrange system. Momentum is exchanged between the
omega sector and its topological source. Separate omega T_{mu nu} need not be
conserved on the frozen U background; only a coupled solution has the full
Noether/conservation statement.

Therefore this run is a model prefilter, not a new microscopic-field
realization.

PROMOTION CONDITION
-------------------
A strong 024A2 promotion requires at least one spatially resolved finite-range
candidate satisfying all of:

- mu*dx <= 0.5;
- positive Proca energy and exact discrete on-shell energy identity;
- analytic/numerical DEC consistency;
- padding convergence of eta_omega <= 5%;
- repaired finite-payload eta_omega/eta_baseline > 1.10;
- repaired eta_omega/eta_local_B0_squared > 1.10;
- force-weighted median S/rho within 0.35 of 2.649629;
- finite-payload result remains outward;
- the selected baseline axis is outward under the repaired P0 operator;
- continuous baseline reconstruction is not robustly contradictory.

A "major" prefilter signal additionally requires

    eta_omega/eta_baseline >= 2.

FALSIFIERS / STOP RULES
-----------------------
- If no resolved finite-range omega candidate beats the baseline, stop the
  direct omega route before a coupled 3D solve.
- If finite range never beats the local B0^2 heavy-limit comparator, the omega
  field has not solved the geometry problem exposed by 024A1.
- If only mu*dx > 0.5 candidates win, classify the result unresolved rather
  than promoting an under-resolved short-range field.
- If the baseline selected axis is not outward under the repaired operator,
  do not use its old midpoint response as evidence.
- Do not increase the project heuristic from this fixed-field prefilter alone.

OUTPUTS
-------
results/data/024a2_explicit_omega_proca_teacher_match_summary.json
results/data/024a2_explicit_omega_proca_mu_scan.csv
results/data/024a2_explicit_omega_proca_selected_field.npz

CLAIM LIMITS
------------
This run does not establish a coupled omega-Skyrme stationary solution,
stability, characteristic hyperbolicity of the full coupled system, continuum
field convergence, nonlinear Einstein-matter consistency, practical energy
scaling, a material, an experiment, or an antigravity device.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_024A2_EXPLICIT_OMEGA_PROCA_TEACHER_MATCH_PREFILTER
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
from typing import Any

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.fft import dstn, idstn


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results/data"

A1_SOURCE = (
    SIM
    / "024a1_sextic_fixed_field_kernel_placement_gate.py"
)
A1_ARRAYS = (
    DATA
    / "024a1_sextic_fixed_field_orientation_arrays.npz"
)
A1_SUMMARY = (
    DATA
    / "024a1_sextic_fixed_field_kernel_placement_summary.json"
)
CR3_SOURCE = (
    SIM
    / "023cr3_geometric_degree_guarded_unrestricted_relaxation.py"
)
N65_ARTIFACT = (
    DATA
    / "023cr4r_strict_stationary_b7_n65.npz"
)
TEACHER_MAPS = (
    DATA
    / "int15_teacher_b7_comparison_maps.npz"
)
AQS_SOURCE = (
    SIM
    / "023c2aqs_continuous_field_active_source_force_integration.py"
)
AQR_SOURCE = (
    SIM
    / "023c2aqr_analytic_prism_exact_cap_payload_operator.py"
)

OUT_JSON = (
    DATA
    / "024a2_explicit_omega_proca_teacher_match_summary.json"
)
OUT_CSV = (
    DATA
    / "024a2_explicit_omega_proca_mu_scan.csv"
)
OUT_NPZ = (
    DATA
    / "024a2_explicit_omega_proca_selected_field.npz"
)

B = 7
ETA = 0.40
MASS = 8.0

TEACHER_Q = 2.6496291391878843
TEACHER_FMASS = 0.5 * (TEACHER_Q - 2.0)
TEACHER_PPAR = 2.0 * TEACHER_FMASS - 1.0

# Main physically motivated range scan in mu*h.
PHYSICAL_MUH = np.array(
    [
        0.25,
        0.35,
        0.50,
        0.70,
        1.00,
        1.40,
        2.00,
        2.80,
        4.00,
        5.60,
        8.00,
        12.0,
        16.0,
        24.0,
    ],
    dtype=float,
)

# Blind wildcard checks are nonprivileged diagnostics only.
WILDCARD_MUH = np.array(
    [
        0.625,
        1.6,
        1.875,
        3.125,
        5.0,
    ],
    dtype=float,
)

MUH_SCAN = np.array(
    sorted(
        set(
            np.concatenate(
                [
                    PHYSICAL_MUH,
                    WILDCARD_MUH,
                ]
            )
        )
    ),
    dtype=float,
)

PAD_SCAN = (97, 129)
PAD_CONFIRM = 161

RESOLVED_MUDX_MAX = 0.50
PAD_REL_TOL = 0.05
Q_MATCH_TOL = 0.35

GAIN_MIN = 1.10
GAIN_MAJOR = 2.00
LOCAL_BEAT_MIN = 1.10

P0_BATCH = int(
    os.environ.get(
        "AG_024A2_P0_BATCH",
        "65536",
    )
)

RUN_CONTINUOUS_BASELINE = (
    os.environ.get(
        "AG_024A2_CONTINUOUS_BASELINE",
        "YES",
    ).strip().upper()
    != "NO"
)


def require(path: Path) -> None:
    if not path.is_file():
        raise RuntimeError(
            f"Required file missing: {path}"
        )


def load_module(
    name: str,
    path: Path,
):
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

    module = (
        importlib.util.module_from_spec(
            spec
        )
    )

    sys.modules[name] = module
    spec.loader.exec_module(module)

    return module


def relerr(
    a: float,
    b: float,
) -> float:
    return (
        abs(a - b)
        / max(
            abs(a),
            abs(b),
            1.0e-300,
        )
    )


def weighted_quantile(
    values: np.ndarray,
    weights: np.ndarray,
    q: float = 0.5,
) -> float:
    v = np.asarray(
        values,
        float,
    ).ravel()

    w = np.asarray(
        weights,
        float,
    ).ravel()

    mask = (
        np.isfinite(v)
        & np.isfinite(w)
        & (w > 0.0)
    )

    if not np.any(mask):
        return float("nan")

    v = v[mask]
    w = w[mask]

    order = np.argsort(v)

    v = v[order]
    w = w[order]

    c = np.cumsum(w)

    idx = min(
        np.searchsorted(
            c,
            q * c[-1],
            side="left",
        ),
        len(v) - 1,
    )

    return float(v[idx])


def build_n65(
    cr3,
) -> dict[str, Any]:
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
                    float(
                        d["B"]
                    )
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

        source = (
            str(
                np.asarray(
                    d["source"]
                ).item()
            )
            if "source" in d.files
            else "UNKNOWN"
        )

    if (
        phi.shape
        != (65, 65, 65, 4)
        or axis.shape
        != (65,)
    ):
        raise RuntimeError(
            "Unexpected N65 artifact "
            f"shape: phi={phi.shape}, "
            f"axis={axis.shape}"
        )

    if (
        b != B
        or abs(eta - ETA)
        > 1.0e-12
        or abs(mass - MASS)
        > 1.0e-12
    ):
        raise RuntimeError(
            "N65 artifact metadata mismatch"
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

    qx, qy, qz = (
        cr3.central4_derivatives(
            phi,
            dx,
        )
    )

    (
        _,
        _,
        _,
        _,
        _,
        _,
        e2,
        e4,
    ) = cr3.metric_terms(
        qx,
        qy,
        qz,
    )

    center = phi[
        2:-2,
        2:-2,
        2:-2,
    ]

    potential = (
        cr3.potential_sigma(
            center[..., 0]
        )
    )

    rho = (
        e2
        + e4
        + potential
    )

    active = (
        2.0
        * (
            e4
            - potential
        )
    )

    mat = np.stack(
        [
            center,
            qx,
            qy,
            qz,
        ],
        axis=-1,
    )

    det = np.linalg.det(mat)

    b0 = (
        -det
        / (
            2.0
            * math.pi**2
        )
    )

    coords = axis[2:-2]

    topology = (
        -float(
            np.sum(det)
            * dx**3
            / (
                2.0
                * math.pi**2
            )
        )
    )

    E0 = float(
        np.sum(rho)
        * dx**3
    )

    E4 = float(
        np.sum(e4)
        * dx**3
    )

    return {
        "phi": phi,
        "axis_full": axis,
        "coords": coords,
        "dx": dx,
        "rho": rho,
        "active": active,
        "e2": e2,
        "e4": e4,
        "potential": potential,
        "b0": b0,
        "topology": topology,
        "E0": E0,
        "E4": E4,
        "normerr": normerr,
        "source": source,
    }


def select_axis():
    require(A1_ARRAYS)

    with np.load(
        A1_ARRAYS,
        allow_pickle=False,
    ) as d:
        directions = np.asarray(
            d["directions"],
            float,
        )

        A_old = np.asarray(
            d["n65_A0"],
            float,
        )

    idx = int(
        np.argmax(A_old)
    )

    n = np.asarray(
        directions[idx],
        float,
    )

    n /= np.linalg.norm(n)

    return (
        n,
        idx,
        float(A_old[idx]),
        float(np.max(A_old)),
    )


def grid_xyz(
    coords: np.ndarray,
) -> np.ndarray:
    X, Y, Z = np.meshgrid(
        coords,
        coords,
        coords,
        indexing="ij",
    )

    return np.column_stack(
        [
            X.ravel(),
            Y.ravel(),
            Z.ravel(),
        ]
    )


def midpoint_force(
    source,
    coords,
    dx,
    center,
    direction,
    Rp,
):
    xyz = grid_xyz(coords)

    q = (
        xyz
        - center[None, :]
    )

    d2 = np.sum(
        q * q,
        axis=1,
    )

    d = np.sqrt(
        np.maximum(
            d2,
            0.0,
        )
    )

    denom = np.where(
        d < Rp,
        Rp**3,
        np.maximum(
            d2 * d,
            1.0e-300,
        ),
    )

    K = (
        q
        @ direction
    ) / denom

    contrib = (
        source.ravel()
        * K
        * dx**3
    )

    return (
        float(
            np.sum(
                contrib
            )
        ),
        float(
            np.sum(
                np.abs(
                    contrib
                )
            )
        ),
        float(
            np.sum(
                np.maximum(
                    contrib,
                    0.0,
                )
            )
        ),
    )


def p0_compact_correction(
    source,
    coords,
    dx,
    center,
    direction,
    Rp,
    nr,
    nmu,
    nphi,
):
    """Integrate finite-payload compact correction.

    The 1/r^3 singularity cancels analytically after including dV.
    Source is piecewise constant on dual voxels centered at coords.
    """

    xr, wr = leggauss(nr)

    r = (
        0.5
        * Rp
        * (
            xr
            + 1.0
        )
    )

    wr = (
        0.5
        * Rp
        * wr
    )

    mu, wmu = leggauss(nmu)

    phi = (
        2.0
        * math.pi
        / nphi
        * (
            np.arange(
                nphi,
                dtype=float,
            )
            + 0.5
        )
    )

    wphi = (
        2.0
        * math.pi
        / nphi
    )

    helper = (
        np.array(
            [
                1.0,
                0.0,
                0.0,
            ]
        )
        if abs(
            direction[0]
        )
        < 0.8
        else np.array(
            [
                0.0,
                1.0,
                0.0,
            ]
        )
    )

    e1 = np.cross(
        direction,
        helper,
    )

    e1 /= np.linalg.norm(e1)

    e2 = np.cross(
        direction,
        e1,
    )

    total = 0.0

    lo = float(
        coords[0]
        - 0.5 * dx
    )

    ngrid = len(coords)

    cp = np.cos(phi)
    sp = np.sin(phi)

    for ir, rr in enumerate(r):
        radial_factor = (
            rr**3
            / Rp**3
            - 1.0
        )

        smu = np.sqrt(
            np.maximum(
                0.0,
                1.0
                - mu * mu,
            )
        )

        dirs = (
            mu[
                :,
                None,
                None,
            ]
            * direction[
                None,
                None,
                :,
            ]
            + smu[
                :,
                None,
                None,
            ]
            * cp[
                None,
                :,
                None,
            ]
            * e1[
                None,
                None,
                :,
            ]
            + smu[
                :,
                None,
                None,
            ]
            * sp[
                None,
                :,
                None,
            ]
            * e2[
                None,
                None,
                :,
            ]
        )

        pts = (
            center[
                None,
                None,
                :,
            ]
            + rr * dirs
        )

        idx = np.floor(
            (
                pts
                - lo
            )
            / dx
        ).astype(int)

        if (
            np.any(
                idx < 0
            )
            or np.any(
                idx
                >= ngrid
            )
        ):
            raise RuntimeError(
                "Payload compact "
                "correction leaves "
                "P0 source domain"
            )

        vals = source[
            idx[..., 0],
            idx[..., 1],
            idx[..., 2],
        ]

        integrand = (
            vals
            * mu[:, None]
            * radial_factor
        )

        total += float(
            wr[ir]
            * wphi
            * np.sum(
                wmu[:, None]
                * integrand
            )
        )

    return total


def p0_force(
    aqr,
    source,
    coords,
    dx,
    center,
    direction,
    Rp,
    label,
):
    """Exact point-prism sum plus converged compact correction."""

    xyz = grid_xyz(coords)

    half = 0.5 * dx

    flat = source.ravel()

    point = 0.0

    for start in range(
        0,
        len(flat),
        P0_BATCH,
    ):
        stop = min(
            start
            + P0_BATCH,
            len(flat),
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

        vec = aqr.prism_field_many(
            lo,
            hi,
        )

        point += float(
            np.sum(
                flat[start:stop]
                * (
                    vec
                    @ direction
                )
            )
        )

    corr_lo = (
        p0_compact_correction(
            source,
            coords,
            dx,
            center,
            direction,
            Rp,
            24,
            24,
            48,
        )
    )

    corr_hi = (
        p0_compact_correction(
            source,
            coords,
            dx,
            center,
            direction,
            Rp,
            40,
            40,
            80,
        )
    )

    corr_err = abs(
        corr_hi
        - corr_lo
    )

    total = (
        point
        + corr_hi
    )

    print(
        f"{label}_P0_POINT_PRISM="
        f"{point:.15e}"
    )

    print(
        f"{label}_P0_COMPACT_CORR_COARSE="
        f"{corr_lo:.15e}"
    )

    print(
        f"{label}_P0_COMPACT_CORR_FINE="
        f"{corr_hi:.15e}"
    )

    print(
        f"{label}_P0_COMPACT_CORR_ABSERR="
        f"{corr_err:.15e}"
    )

    print(
        f"{label}_P0_FORCE="
        f"{total:.15e}"
    )

    return {
        "force": total,
        "point": point,
        "correction": corr_hi,
        "correction_error": corr_err,
    }


def embed_center(
    core,
    n_pad,
):
    n = core.shape[0]

    if (
        core.shape
        != (n, n, n)
        or n_pad < n
        or (
            (n_pad - n)
            & 1
        )
    ):
        raise ValueError(
            "Cannot center core "
            f"{core.shape} "
            f"in pad {n_pad}"
        )

    out = np.zeros(
        (
            n_pad,
            n_pad,
            n_pad,
        ),
        float,
    )

    s = (
        n_pad - n
    ) // 2

    out[
        s:s+n,
        s:s+n,
        s:s+n,
    ] = core

    return out


def solve_omega(
    source,
    dx,
    mu,
):
    """Solve positive Dirichlet screened-Poisson operator."""

    n = source.shape[0]

    shat = dstn(
        source,
        type=1,
        norm="ortho",
    )

    k = np.arange(
        1,
        n + 1,
        dtype=float,
    )

    lam = (
        4.0
        / dx**2
        * np.sin(
            math.pi
            * k
            / (
                2.0
                * (
                    n + 1
                )
            )
        )**2
    )

    denom = (
        lam[:, None, None]
        + lam[None, :, None]
        + lam[None, None, :]
        + mu * mu
    )

    what = (
        shat
        / denom
    )

    return idstn(
        what,
        type=1,
        norm="ortho",
    )


def discrete_proca_ledger(
    omega,
    source,
    dx,
    mu,
):
    """Exact positive energy assignment for the DST operator."""

    egrad = np.zeros_like(
        omega
    )

    for ax in range(3):
        d = (
            np.diff(
                omega,
                axis=ax,
            )
            / dx
        )

        piece = (
            0.25
            * d * d
        )

        sl0 = [
            slice(None)
        ] * 3

        sl1 = [
            slice(None)
        ] * 3

        sl0[ax] = slice(
            0,
            -1,
        )

        sl1[ax] = slice(
            1,
            None,
        )

        egrad[
            tuple(sl0)
        ] += piece

        egrad[
            tuple(sl1)
        ] += piece

        slo = [
            slice(None)
        ] * 3

        shi = [
            slice(None)
        ] * 3

        slo[ax] = 0
        shi[ax] = -1

        egrad[
            tuple(slo)
        ] += (
            0.5
            * (
                omega[
                    tuple(slo)
                ]
                / dx
            )**2
        )

        egrad[
            tuple(shi)
        ] += (
            0.5
            * (
                omega[
                    tuple(shi)
                ]
                / dx
            )**2
        )

    emass = (
        0.5
        * mu
        * mu
        * omega
        * omega
    )

    rho = (
        egrad
        + emass
    )

    active = (
        2.0
        * egrad
        + 4.0
        * emass
    )

    dV = dx**3

    Egrad = float(
        np.sum(egrad)
        * dV
    )

    Emass = float(
        np.sum(emass)
        * dV
    )

    E = (
        Egrad
        + Emass
    )

    Eonshell = (
        0.5
        * float(
            np.sum(
                source
                * omega
            )
            * dV
        )
    )

    identity = relerr(
        E,
        Eonshell,
    )

    q = np.divide(
        active,
        rho,
        out=np.full_like(
            rho,
            np.nan,
        ),
        where=(
            rho
            > 1.0e-300
        ),
    )

    qfinite = q[
        np.isfinite(q)
    ]

    return {
        "egrad": egrad,
        "emass": emass,
        "rho": rho,
        "active": active,
        "q": q,
        "Egrad": Egrad,
        "Emass": Emass,
        "E": E,
        "Eonshell": Eonshell,
        "identity_relerr": identity,
        "q_min": float(
            np.min(
                qfinite
            )
        ),
        "q_max": float(
            np.max(
                qfinite
            )
        ),
        "fmass_global": (
            Emass
            / max(
                E,
                1.0e-300,
            )
        ),
    }


def concentration_metrics(
    rho,
    active,
    qratio,
    coords,
    dx,
    center,
    direction,
    Rp,
):
    xyz = grid_xyz(coords)

    qq = (
        xyz
        - center[None, :]
    )

    d2 = np.sum(
        qq * qq,
        axis=1,
    )

    d = np.sqrt(
        np.maximum(
            d2,
            0.0,
        )
    )

    denom = np.where(
        d < Rp,
        Rp**3,
        np.maximum(
            d2 * d,
            1.0e-300,
        ),
    )

    K = (
        qq
        @ direction
    ) / denom

    cellE = (
        rho.ravel()
        * dx**3
    )

    contrib = (
        active.ravel()
        * K
        * dx**3
    )

    outward = np.maximum(
        contrib,
        0.0,
    )

    A = float(
        np.sum(
            contrib
        )
    )

    gross = float(
        np.sum(
            outward
        )
    )

    cancellation = float(
        np.sum(
            np.abs(
                contrib
            )
        )
        / max(
            abs(A),
            1.0e-300,
        )
    )

    leverage = np.divide(
        outward,
        cellE,
        out=np.zeros_like(
            outward
        ),
        where=(
            cellE
            > 1.0e-300
        ),
    )

    order = np.argsort(
        leverage
    )[::-1]

    co = np.cumsum(
        outward[order]
    )

    ce = np.cumsum(
        cellE[order]
    )

    Etot = float(
        np.sum(
            cellE
        )
    )

    def ef(frac):
        if gross <= 0.0:
            return float("nan")

        i = min(
            int(
                np.searchsorted(
                    co,
                    frac * gross,
                    side="left",
                )
            ),
            len(order) - 1,
        )

        return float(
            ce[i]
            / max(
                Etot,
                1.0e-300,
            )
        )

    qmed = weighted_quantile(
        qratio.ravel(),
        outward,
        0.5,
    )

    return {
        "A_mid": A,
        "gross_outward_mid": gross,
        "cancellation_mid": cancellation,
        "F50_energy_fraction_mid": ef(
            0.5
        ),
        "F90_energy_fraction_mid": ef(
            0.9
        ),
        "outward_weighted_q_median_mid": qmed,
    }


def teacher_overlap(
    rho,
    active,
    coords,
    dx,
    h,
    center,
    direction,
    Rp,
):
    if not TEACHER_MAPS.is_file():
        return {
            "available": False
        }

    with np.load(
        TEACHER_MAPS,
        allow_pickle=False,
    ) as d:
        if not all(
            k in d.files
            for k in (
                "teacher_F90_mask",
                "r_edges",
                "z_edges",
            )
        ):
            return {
                "available": False
            }

        mask = np.asarray(
            d["teacher_F90_mask"],
            bool,
        )

        redges = np.asarray(
            d["r_edges"],
            float,
        )

        zedges = np.asarray(
            d["z_edges"],
            float,
        )

    xyz = grid_xyz(coords)

    z = (
        xyz
        @ direction
    ) / h

    r2 = (
        np.sum(
            xyz * xyz,
            axis=1,
        )
        / h**2
        - z * z
    )

    r = np.sqrt(
        np.maximum(
            r2,
            0.0,
        )
    )

    ir = (
        np.searchsorted(
            redges,
            r,
            side="right",
        )
        - 1
    )

    iz = (
        np.searchsorted(
            zedges,
            z,
            side="right",
        )
        - 1
    )

    valid = (
        (ir >= 0)
        & (
            ir
            < mask.shape[0]
        )
        & (iz >= 0)
        & (
            iz
            < mask.shape[1]
        )
    )

    inmask = np.zeros(
        len(xyz),
        bool,
    )

    inmask[valid] = mask[
        ir[valid],
        iz[valid],
    ]

    qq = (
        xyz
        - center[None, :]
    )

    d2 = np.sum(
        qq * qq,
        axis=1,
    )

    dd = np.sqrt(
        np.maximum(
            d2,
            0.0,
        )
    )

    denom = np.where(
        dd < Rp,
        Rp**3,
        np.maximum(
            d2 * dd,
            1.0e-300,
        ),
    )

    K = (
        qq
        @ direction
    ) / denom

    cellE = (
        rho.ravel()
        * dx**3
    )

    outward = np.maximum(
        active.ravel()
        * K
        * dx**3,
        0.0,
    )

    return {
        "available": True,
        "energy_fraction_in_teacher_F90":
            float(
                np.sum(
                    cellE[inmask]
                )
                / max(
                    np.sum(cellE),
                    1.0e-300,
                )
            ),
        "gross_outward_fraction_in_teacher_F90":
            float(
                np.sum(
                    outward[inmask]
                )
                / max(
                    np.sum(
                        outward
                    ),
                    1.0e-300,
                )
            ),
    }


def continuous_baseline(
    c2aqs,
    aqr,
    field,
    center,
    direction,
    Rp,
):
    if not RUN_CONTINUOUS_BASELINE:
        return {
            "attempted": False,
            "certified": False,
        }

    phi = field["phi"]
    axis = field["axis_full"]
    dx = field["dx"]

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

    near = lowers[
        dmin
        < near_radius
    ]

    far = lowers[
        dmin
        >= near_radius
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

    const = (
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

    methods = {}
    interps = {}

    for method in (
        "cubic",
        "quintic",
    ):
        print(
            "024A2_BUILDING_"
            f"{method.upper()}_"
            "BASELINE_SPLINE=START",
            flush=True,
        )

        interp = (
            c2aqs.build_interpolator(
                axis,
                phi,
                method,
            )
        )

        interps[method] = interp

        c2aqs.nodal_reproduction_check(
            interp,
            phi,
            axis,
            method,
        )

        c2aqs.finite_difference_derivative_check(
            interp,
            axis,
            dx,
            method,
        )

        result = c2aqs.run_method(
            method,
            interp,
            far,
            near,
            offsets,
            center,
            direction,
            Rp,
            use_q4=False,
        )

        methods[method] = result

    spread0 = abs(
        methods["cubic"].best.force
        - methods["quintic"].best.force
    )

    err0 = max(
        methods["cubic"].internal_error,
        methods["quintic"].internal_error,
        spread0,
    )

    margin0 = min(
        abs(
            methods["cubic"].best.force
        ),
        abs(
            methods["quintic"].best.force
        ),
    )

    same0 = (
        np.sign(
            methods["cubic"].best.force
        )
        == np.sign(
            methods["quintic"].best.force
        )
        and methods["cubic"].best.force
        != 0
    )

    cert0 = bool(
        same0
        and margin0
        > c2aqs.SIGN_SAFETY_FACTOR
        * err0
    )

    if not cert0:
        print(
            "024A2_BASELINE_CONTINUOUS_"
            "PRELIM_CERTIFIED=NO; "
            "triggering q4",
            flush=True,
        )

        for method in (
            "cubic",
            "quintic",
        ):
            methods[method] = (
                c2aqs.upgrade_method_q4(
                    methods[method],
                    interps[method],
                    far,
                    offsets,
                    center,
                    direction,
                    Rp,
                )
            )

    spread = abs(
        methods["cubic"].best.force
        - methods["quintic"].best.force
    )

    err = max(
        methods["cubic"].internal_error,
        methods["quintic"].internal_error,
        spread,
    )

    margin = min(
        abs(
            methods["cubic"].best.force
        ),
        abs(
            methods["quintic"].best.force
        ),
    )

    same = (
        np.sign(
            methods["cubic"].best.force
        )
        == np.sign(
            methods["quintic"].best.force
        )
        and methods["cubic"].best.force
        != 0
    )

    certified = bool(
        same
        and margin
        > c2aqs.SIGN_SAFETY_FACTOR
        * err
    )

    mean = 0.5 * (
        methods["cubic"].best.force
        + methods["quintic"].best.force
    )

    return {
        "attempted": True,
        "constant_source_relerr":
            float(const),
        "cubic_force":
            float(
                methods["cubic"].best.force
            ),
        "quintic_force":
            float(
                methods["quintic"].best.force
            ),
        "representation_spread":
            float(spread),
        "error_bound":
            float(err),
        "margin":
            float(margin),
        "certified":
            certified,
        "sign":
            (
                "OUTWARD"
                if (
                    certified
                    and mean > 0
                )
                else (
                    "INWARD"
                    if (
                        certified
                        and mean < 0
                    )
                    else "UNRESOLVED"
                )
            ),
        "mean_force":
            float(mean),
    }


def main() -> None:
    print(
        "=== 024A2 — EXPLICIT "
        "OMEGA/PROCA TEACHER-MATCH "
        "PREFILTER ===",
        flush=True,
    )

    for p in (
        A1_SOURCE,
        A1_ARRAYS,
        A1_SUMMARY,
        CR3_SOURCE,
        N65_ARTIFACT,
        AQR_SOURCE,
    ):
        require(p)

    load_module(
        "ag024a2_a1",
        A1_SOURCE,
    )

    cr3 = load_module(
        "ag024a2_cr3",
        CR3_SOURCE,
    )

    aqr = load_module(
        "ag024a2_aqr",
        AQR_SOURCE,
    )

    c2aqs = (
        load_module(
            "ag024a2_aqs",
            AQS_SOURCE,
        )
        if AQS_SOURCE.is_file()
        else None
    )

    with A1_SUMMARY.open() as f:
        a1sum = json.load(f)

    h = float(
        a1sum[
            "payload"
        ][
            "center_radius"
        ]
    )

    Rp = float(
        a1sum[
            "payload"
        ][
            "payload_radius"
        ]
    )

    field = build_n65(cr3)

    (
        direction,
        axis_index,
        oldA,
        oldAmax,
    ) = select_axis()

    center = (
        h
        * direction
    )

    dx = field["dx"]

    print(
        f"N65_SOURCE="
        f"{field['source']}"
    )

    print(
        f"N65_DX="
        f"{dx:.15e}"
    )

    print(
        f"N65_TOPOLOGY4_REBUILT="
        f"{field['topology']:.15e}"
    )

    print(
        f"N65_E0="
        f"{field['E0']:.15e}"
    )

    print(
        f"PAYLOAD_CENTER_RADIUS="
        f"{h:.15e}"
    )

    print(
        f"PAYLOAD_RADIUS="
        f"{Rp:.15e}"
    )

    print(
        "AXIS_SELECTION="
        "BASELINE_MAX_FROM_024A1_"
        "BEFORE_OMEGA"
    )

    print(
        f"AXIS_INDEX="
        f"{axis_index}"
    )

    print(
        "AXIS_DIRECTION="
        + ",".join(
            f"{x:.15e}"
            for x
            in direction
        )
    )

    print(
        "UPSTREAM_MIDPOINT_A_SELECTED="
        f"{oldA:.15e}"
    )

    print(
        "TEACHER_TARGET_Q="
        f"{TEACHER_Q:.15e}"
    )

    print(
        "TEACHER_TARGET_FMASS="
        f"{TEACHER_FMASS:.15e}"
    )

    print(
        "TEACHER_TARGET_PPAR_OVER_RHO="
        f"{TEACHER_PPAR:.15e}"
    )

    print(
        "PROCA_STATIC_DEC_ANALYTIC=PASS"
    )

    print(
        "WZ_COUPLING_DIRECT_TMUNU="
        "ZERO_IN_STANDARD_"
        "OMEGA_SKYRME_FORMULATION"
    )

    print(
        "FIXED_FIELD_G_OMEGA_CANCELS_"
        "FROM_SPECIFIC_LEVERAGE=YES"
    )

    print(
        "\n=== A — REPAIRED "
        "BASELINE / LOCAL "
        "COMPARATORS ===",
        flush=True,
    )

    base_p0 = p0_force(
        aqr,
        field["active"],
        field["coords"],
        dx,
        center,
        direction,
        Rp,
        "BASELINE",
    )

    if (
        base_p0["force"]
        <= 0.0
    ):
        raise RuntimeError(
            "Baseline-max upstream axis "
            "is not outward under "
            "repaired P0 operator"
        )

    eta0 = (
        base_p0["force"]
        / field["E0"]
    )

    print(
        f"BASELINE_P0_ETA="
        f"{eta0:.15e}"
    )

    local_e = (
        field["b0"]**2
    )

    local_S = (
        4.0
        * local_e
    )

    local_E = float(
        np.sum(local_e)
        * dx**3
    )

    local_p0 = p0_force(
        aqr,
        local_S,
        field["coords"],
        dx,
        center,
        direction,
        Rp,
        "LOCAL_B0SQ",
    )

    eta_local = (
        local_p0["force"]
        / local_E
    )

    print(
        f"LOCAL_B0SQ_E="
        f"{local_E:.15e}"
    )

    print(
        f"LOCAL_B0SQ_ETA="
        f"{eta_local:.15e}"
    )

    print(
        "LOCAL_B0SQ_GAIN_VS_BASELINE="
        f"{eta_local/eta0:.15e}"
    )

    l4_S = (
        2.0
        * field["e4"]
    )

    l4_p0 = p0_force(
        aqr,
        l4_S,
        field["coords"],
        dx,
        center,
        direction,
        Rp,
        "L4",
    )

    eta_l4 = (
        l4_p0["force"]
        / max(
            field["E4"],
            1.0e-300,
        )
    )

    print(
        f"L4_E="
        f"{field['E4']:.15e}"
    )

    print(
        f"L4_ETA="
        f"{eta_l4:.15e}"
    )

    continuous = {
        "attempted": False,
        "certified": False,
    }

    if c2aqs is not None:
        print(
            "\n=== B — INDEPENDENT "
            "CONTINUOUS BASELINE "
            "AXIS CHECK ===",
            flush=True,
        )

        try:
            continuous = (
                continuous_baseline(
                    c2aqs,
                    aqr,
                    field,
                    center,
                    direction,
                    Rp,
                )
            )

        except Exception as exc:
            continuous = {
                "attempted": True,
                "certified": False,
                "error":
                    f"{type(exc).__name__}: "
                    f"{exc}",
            }

            print(
                "BASELINE_CONTINUOUS_ERROR="
                f"{continuous['error']}"
            )

        if continuous.get(
            "attempted"
        ):
            if (
                "cubic_force"
                in continuous
            ):
                print(
                    "BASELINE_CONTINUOUS_CUBIC="
                    f"{continuous['cubic_force']:.15e}"
                )

                print(
                    "BASELINE_CONTINUOUS_QUINTIC="
                    f"{continuous['quintic_force']:.15e}"
                )

                print(
                    "BASELINE_CONTINUOUS_ERROR_BOUND="
                    f"{continuous['error_bound']:.15e}"
                )

                print(
                    "BASELINE_CONTINUOUS_CERTIFIED="
                    + (
                        "YES"
                        if continuous[
                            "certified"
                        ]
                        else "NO"
                    )
                )

                print(
                    "BASELINE_CONTINUOUS_SIGN="
                    f"{continuous['sign']}"
                )

    print(
        "\n=== C — FINITE-RANGE "
        "OMEGA SCAN ===",
        flush=True,
    )

    rows = []

    core = field["b0"]

    for n_pad in PAD_SCAN:
        src = embed_center(
            core,
            n_pad,
        )

        coords = (
            dx
            * (
                np.arange(
                    n_pad,
                    dtype=float,
                )
                - 0.5
                * (
                    n_pad - 1
                )
            )
        )

        for muh in MUH_SCAN:
            mu = float(
                muh / h
            )

            omega = solve_omega(
                src,
                dx,
                mu,
            )

            led = (
                discrete_proca_ledger(
                    omega,
                    src,
                    dx,
                    mu,
                )
            )

            if (
                led[
                    "identity_relerr"
                ]
                > 2.0e-10
            ):
                raise RuntimeError(
                    "Proca discrete energy "
                    "identity failed "
                    f"pad={n_pad} "
                    f"muh={muh}: "
                    f"{led['identity_relerr']}"
                )

            if (
                led["q_min"]
                < 2.0
                - 1.0e-10
                or led["q_max"]
                > 4.0
                + 1.0e-10
            ):
                raise RuntimeError(
                    "Proca q range violated "
                    "analytic [2,4] bound"
                )

            (
                amid,
                l1,
                gross,
            ) = midpoint_force(
                led["active"],
                coords,
                dx,
                center,
                direction,
                Rp,
            )

            eta_mid = (
                amid
                / led["E"]
            )

            metrics = (
                concentration_metrics(
                    led["rho"],
                    led["active"],
                    led["q"],
                    coords,
                    dx,
                    center,
                    direction,
                    Rp,
                )
            )

            overlap = (
                teacher_overlap(
                    led["rho"],
                    led["active"],
                    coords,
                    dx,
                    h,
                    center,
                    direction,
                    Rp,
                )
            )

            row = {
                "pad":
                    n_pad,

                "mu_h":
                    float(muh),

                "mu_dx":
                    float(
                        mu * dx
                    ),

                "resolved_mu_dx":
                    bool(
                        mu * dx
                        <= RESOLVED_MUDX_MAX
                    ),

                "wildcard":
                    bool(
                        np.any(
                            np.isclose(
                                muh,
                                WILDCARD_MUH,
                                rtol=0,
                                atol=1.0e-14,
                            )
                        )
                    ),

                "E":
                    led["E"],

                "Egrad":
                    led["Egrad"],

                "Emass":
                    led["Emass"],

                "fmass_global":
                    led["fmass_global"],

                "energy_identity_relerr":
                    led[
                        "identity_relerr"
                    ],

                "q_min":
                    led["q_min"],

                "q_max":
                    led["q_max"],

                "A_mid":
                    amid,

                "eta_mid":
                    eta_mid,

                "gain_mid_vs_baseline":
                    eta_mid
                    / eta0,

                "gain_mid_vs_local":
                    (
                        eta_mid
                        / eta_local
                        if eta_local
                        != 0
                        else float(
                            "nan"
                        )
                    ),

                "gain_mid_vs_l4":
                    (
                        eta_mid
                        / eta_l4
                        if eta_l4
                        != 0
                        else float(
                            "nan"
                        )
                    ),

                "cancellation_mid":
                    metrics[
                        "cancellation_mid"
                    ],

                "F50_energy_fraction_mid":
                    metrics[
                        "F50_energy_fraction_mid"
                    ],

                "F90_energy_fraction_mid":
                    metrics[
                        "F90_energy_fraction_mid"
                    ],

                "q_outward_weighted_median_mid":
                    metrics[
                        "outward_weighted_q_median_mid"
                    ],

                "q_teacher_absdiff_mid":
                    abs(
                        metrics[
                            "outward_weighted_q_median_mid"
                        ]
                        - TEACHER_Q
                    ),

                "teacher_F90_energy_fraction":
                    overlap.get(
                        "energy_fraction_in_teacher_F90",
                        float("nan"),
                    ),

                "teacher_F90_gross_outward_fraction":
                    overlap.get(
                        "gross_outward_fraction_in_teacher_F90",
                        float("nan"),
                    ),
            }

            rows.append(row)

            print(
                f"OMEGA PAD={n_pad} "
                f"MU_H={muh:.6e} "
                f"MU_DX={mu*dx:.6e} "
                f"RESOLVED="
                f"{'YES' if row['resolved_mu_dx'] else 'NO'} "
                f"E={led['E']:.6e} "
                f"FMASS={led['fmass_global']:.6e} "
                f"QMED="
                f"{row['q_outward_weighted_median_mid']:.6e} "
                f"ETA_MID={eta_mid:.6e} "
                f"G_BASE="
                f"{row['gain_mid_vs_baseline']:.6e} "
                f"G_LOCAL="
                f"{row['gain_mid_vs_local']:.6e} "
                f"F90E="
                f"{row['F90_energy_fraction_mid']:.6e}",
                flush=True,
            )

    by = {
        (
            int(
                r["pad"]
            ),
            float(
                r["mu_h"]
            ),
        ):
            r
        for r in rows
    }

    candidates = []

    for muh in MUH_SCAN:
        r97 = by[
            (
                97,
                float(muh),
            )
        ]

        r129 = by[
            (
                129,
                float(muh),
            )
        ]

        padrel = relerr(
            float(
                r97["eta_mid"]
            ),
            float(
                r129["eta_mid"]
            ),
        )

        r129[
            "pad_eta_mid_relerr_97_129"
        ] = padrel

        r97[
            "pad_eta_mid_relerr_97_129"
        ] = padrel

        if r129[
            "resolved_mu_dx"
        ]:
            score = min(
                float(
                    r129[
                        "gain_mid_vs_baseline"
                    ]
                ),
                float(
                    r129[
                        "gain_mid_vs_local"
                    ]
                ),
            )

            candidates.append(
                (
                    score,
                    -abs(
                        float(
                            r129[
                                "q_outward_weighted_median_mid"
                            ]
                        )
                        - TEACHER_Q
                    ),
                    float(muh),
                )
            )

        print(
            "OMEGA_PAD_CONVERGENCE "
            f"MU_H={muh:.6e} "
            "ETA_RELERR_97_129="
            f"{padrel:.6e}"
        )

    candidates.sort(
        reverse=True
    )

    selected_muh = [
        x[2]
        for x
        in candidates[:3]
    ]

    if not selected_muh:
        raise RuntimeError(
            "No spatially resolved "
            "omega candidate in scan"
        )

    print(
        "SELECTED_MUH_FOR_REPAIRED_FORCE="
        + ",".join(
            f"{x:.12g}"
            for x
            in selected_muh
        )
    )

    print(
        "\n=== D — REPAIRED "
        "FINITE-PAYLOAD OMEGA "
        "CERTIFICATION ===",
        flush=True,
    )

    certified_rows = []

    selected_arrays = None

    for muh in selected_muh:
        results = {}

        pack97_for_save = None

        for n_pad in (
            97,
            129,
        ):
            src = embed_center(
                core,
                n_pad,
            )

            coords = (
                dx
                * (
                    np.arange(
                        n_pad,
                        dtype=float,
                    )
                    - 0.5
                    * (
                        n_pad - 1
                    )
                )
            )

            mu = (
                muh
                / h
            )

            omega = solve_omega(
                src,
                dx,
                mu,
            )

            led = (
                discrete_proca_ledger(
                    omega,
                    src,
                    dx,
                    mu,
                )
            )

            pack = {
                "omega":
                    omega,
                "coords":
                    coords,
                "source":
                    src,
                "ledger":
                    led,
            }

            if n_pad == 97:
                pack97_for_save = (
                    pack
                )

            p0 = p0_force(
                aqr,
                led["active"],
                coords,
                dx,
                center,
                direction,
                Rp,
                (
                    "OMEGA_MUH_"
                    f"{muh:.6g}_"
                    f"PAD{n_pad}"
                ),
            )

            eta = (
                p0["force"]
                / led["E"]
            )

            results[n_pad] = {
                "force":
                    p0["force"],

                "force_error":
                    p0[
                        "correction_error"
                    ],

                "eta":
                    eta,

                "E":
                    led["E"],

                "qmid":
                    by[
                        (
                            n_pad,
                            float(muh),
                        )
                    ][
                        "q_outward_weighted_median_mid"
                    ],
            }

        padrel = relerr(
            results[97]["eta"],
            results[129]["eta"],
        )

        if muh == selected_muh[0]:
            src161 = embed_center(
                core,
                PAD_CONFIRM,
            )

            coords161 = (
                dx
                * (
                    np.arange(
                        PAD_CONFIRM,
                        dtype=float,
                    )
                    - 0.5
                    * (
                        PAD_CONFIRM - 1
                    )
                )
            )

            mu = (
                muh
                / h
            )

            om161 = solve_omega(
                src161,
                dx,
                mu,
            )

            led161 = (
                discrete_proca_ledger(
                    om161,
                    src161,
                    dx,
                    mu,
                )
            )

            p161 = p0_force(
                aqr,
                led161["active"],
                coords161,
                dx,
                center,
                direction,
                Rp,
                (
                    "OMEGA_MUH_"
                    f"{muh:.6g}_"
                    f"PAD{PAD_CONFIRM}"
                ),
            )

            eta161 = (
                p161["force"]
                / led161["E"]
            )

            results[161] = {
                "force":
                    p161["force"],

                "force_error":
                    p161[
                        "correction_error"
                    ],

                "eta":
                    eta161,

                "E":
                    led161["E"],
            }

            padrel = max(
                padrel,
                relerr(
                    results[129]["eta"],
                    eta161,
                ),
            )

        eta_best = results[
            max(results)
        ]["eta"]

        gain_base = (
            eta_best
            / eta0
        )

        gain_local = (
            eta_best
            / eta_local
            if eta_local != 0
            else float("nan")
        )

        gain_l4 = (
            eta_best
            / eta_l4
            if eta_l4 != 0
            else float("nan")
        )

        qmed = float(
            by[
                (
                    129,
                    float(muh),
                )
            ][
                "q_outward_weighted_median_mid"
            ]
        )

        qdiff = abs(
            qmed
            - TEACHER_Q
        )

        resolved = bool(
            (
                muh
                / h
            )
            * dx
            <= RESOLVED_MUDX_MAX
        )

        energy_ok = bool(
            by[
                (
                    129,
                    float(muh),
                )
            ][
                "energy_identity_relerr"
            ]
            <= 2.0e-10
        )

        row = {
            "mu_h":
                float(muh),

            "mu_dx":
                float(
                    (
                        muh
                        / h
                    )
                    * dx
                ),

            "resolved":
                resolved,

            "eta_repaired":
                float(
                    eta_best
                ),

            "gain_vs_baseline_repaired":
                float(
                    gain_base
                ),

            "gain_vs_local_repaired":
                float(
                    gain_local
                ),

            "gain_vs_l4_repaired":
                float(
                    gain_l4
                ),

            "pad_eta_relerr":
                float(
                    padrel
                ),

            "q_outward_weighted_median":
                qmed,

            "q_teacher_absdiff":
                qdiff,

            "energy_identity_pass":
                energy_ok,

            "force_outward":
                bool(
                    results[
                        max(results)
                    ][
                        "force"
                    ]
                    > 0
                ),

            "pads":
                results,
        }

        row[
            "strong_pass"
        ] = bool(
            resolved
            and energy_ok
            and row[
                "force_outward"
            ]
            and padrel
            <= PAD_REL_TOL
            and gain_base
            > GAIN_MIN
            and gain_local
            > LOCAL_BEAT_MIN
            and qdiff
            <= Q_MATCH_TOL
        )

        row[
            "major_pass"
        ] = bool(
            row[
                "strong_pass"
            ]
            and gain_base
            >= GAIN_MAJOR
        )

        certified_rows.append(
            row
        )

        print(
            f"OMEGA_CERT "
            f"MU_H={muh:.6e} "
            f"MU_DX="
            f"{row['mu_dx']:.6e} "
            f"ETA={eta_best:.9e} "
            f"G_BASE="
            f"{gain_base:.9e} "
            f"G_LOCAL="
            f"{gain_local:.9e} "
            f"G_L4="
            f"{gain_l4:.9e} "
            f"PAD_RELERR="
            f"{padrel:.6e} "
            f"QMED="
            f"{qmed:.6e} "
            f"QDIFF="
            f"{qdiff:.6e} "
            f"STRONG="
            f"{'PASS' if row['strong_pass'] else 'FAIL'} "
            f"MAJOR="
            f"{'PASS' if row['major_pass'] else 'FAIL'}",
            flush=True,
        )

        if (
            selected_arrays is None
            or row[
                "gain_vs_baseline_repaired"
            ]
            > selected_arrays[0]
        ):
            if (
                pack97_for_save
                is None
            ):
                raise RuntimeError(
                    "Internal selected "
                    "pad97 pack missing"
                )

            selected_arrays = (
                row[
                    "gain_vs_baseline_repaired"
                ],
                float(muh),
                pack97_for_save,
            )

    print(
        "\n=== E — HEAVY-LIMIT "
        "CONTROL ===",
        flush=True,
    )

    heavy = by[
        (
            129,
            float(
                MUH_SCAN[-1]
            ),
        )
    ]

    print(
        "HEAVY_CONTROL_MU_H="
        f"{float(MUH_SCAN[-1]):.15e}"
    )

    print(
        "HEAVY_CONTROL_MU_DX="
        f"{float(MUH_SCAN[-1]/h*dx):.15e}"
    )

    print(
        "HEAVY_CONTROL_ETA_MID="
        f"{float(heavy['eta_mid']):.15e}"
    )

    print(
        "LOCAL_B0SQ_ETA="
        f"{eta_local:.15e}"
    )

    print(
        "HEAVY_TO_LOCAL_ETA_RELERR_MID="
        f"{relerr(float(heavy['eta_mid']), eta_local):.15e}"
    )

    print(
        "HEAVY_CONTROL_PROMOTION_ELIGIBLE="
        "NO_UNDERRESOLVED_DIAGNOSTIC_ONLY"
    )

    fieldnames = sorted(
        {
            k
            for r in rows
            for k in r.keys()
        }
    )

    with OUT_CSV.open(
        "w",
        newline="",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for r in rows:
            writer.writerow(r)

    if (
        selected_arrays
        is not None
    ):
        (
            _,
            best_muh,
            bestpack,
        ) = selected_arrays

        np.savez_compressed(
            OUT_NPZ,
            omega=np.asarray(
                bestpack[
                    "omega"
                ]
            ),
            rho=np.asarray(
                bestpack[
                    "ledger"
                ][
                    "rho"
                ]
            ),
            active=np.asarray(
                bestpack[
                    "ledger"
                ][
                    "active"
                ]
            ),
            q=np.asarray(
                bestpack[
                    "ledger"
                ][
                    "q"
                ]
            ),
            coords=np.asarray(
                bestpack[
                    "coords"
                ]
            ),
            dx=np.array(dx),
            mu_h=np.array(
                best_muh
            ),
            direction=np.asarray(
                direction
            ),
            payload_center_radius=
                np.array(h),
            payload_radius=
                np.array(Rp),
        )

    major = [
        r
        for r in certified_rows
        if r["major_pass"]
    ]

    strong = [
        r
        for r in certified_rows
        if r["strong_pass"]
    ]

    baseline_continuous_ok = bool(
        not continuous.get(
            "attempted",
            False,
        )
        or (
            continuous.get(
                "certified",
                False,
            )
            and continuous.get(
                "sign"
            )
            == "OUTWARD"
        )
    )

    if (
        major
        and baseline_continuous_ok
    ):
        decision = (
            "GREEN_MAJOR_FINITE_RANGE_"
            "OMEGA_TEACHER_MATCH_PREFILTER"
        )

        next_action = (
            "024B_COUPLED_FALSE_CORE_"
            "OMEGA_SKYRME_REEQUILIBRATION_"
            "WITH_L2L4V_PLUS_OMEGA_AND_"
            "L2V_PLUS_OMEGA_COMPANION"
        )

    elif (
        strong
        and baseline_continuous_ok
    ):
        decision = (
            "GREEN_FINITE_RANGE_"
            "OMEGA_TEACHER_MATCH_PREFILTER"
        )

        next_action = (
            "024B_COUPLED_FALSE_CORE_"
            "OMEGA_SKYRME_REEQUILIBRATION"
        )

    elif (
        (
            major
            or strong
        )
        and not
        baseline_continuous_ok
    ):
        decision = (
            "YELLOW_OMEGA_SIGNAL_"
            "BASELINE_CONTINUOUS_AXIS_"
            "NOT_CERTIFIED"
        )

        next_action = (
            "024A2R_RESOLVE_SELECTED_AXIS_"
            "CONTINUOUS_BASELINE_BEFORE_"
            "COUPLED_FIELD"
        )

    elif any(
        r[
            "gain_vs_baseline_repaired"
        ]
        > 1.0
        and r["resolved"]
        for r
        in certified_rows
    ):
        decision = (
            "YELLOW_FINITE_RANGE_OMEGA_GAIN_"
            "WITHOUT_FULL_TEACHER_OR_"
            "LOCAL_LIMIT_GATE"
        )

        next_action = (
            "024A3_OMEGA_COUPLING_OR_"
            "FALSE_CORE_GEOMETRY_"
            "REDUCED_PREFILTER"
        )

    else:
        decision = (
            "RED_EXPLICIT_OMEGA_FIXED_FIELD_"
            "PREFILTER_NO_RESOLVED_BREAKTHROUGH"
        )

        next_action = (
            "024A3_ALTERNATIVE_GEOMETRY_"
            "REORGANIZING_TOPOLOGICAL_"
            "OPERATOR_PREFILTER"
        )

    best_cert = max(
        certified_rows,
        key=lambda r:
            r[
                "gain_vs_baseline_repaired"
            ],
    )

    summary = {
        "claim_classification":
            "PROJECT_DERIVED_024A2_"
            "EXPLICIT_OMEGA_PROCA_"
            "TEACHER_MATCH_PREFILTER",

        "model":
            "FALSE_CORE_OMEGA_SKYRME_"
            "EXPLICIT_FINITE_RANGE_"
            "TOPOLOGICAL_VECTOR",

        "literature_class":
            "ESTABLISHED_OMEGA_SKYRME_VARIANT",

        "teacher_target": {
            "S_over_rho":
                TEACHER_Q,
            "mass_energy_fraction":
                TEACHER_FMASS,
            "p_parallel_over_rho":
                TEACHER_PPAR,
        },

        "n65": {
            "source":
                field["source"],
            "dx":
                dx,
            "topology4":
                field["topology"],
            "E0":
                field["E0"],
        },

        "payload": {
            "h":
                h,
            "radius":
                Rp,
            "axis_index":
                axis_index,
            "direction":
                direction.tolist(),
            "axis_selection":
                "BASELINE_MAX_FROM_024A1_"
                "BEFORE_OMEGA",
        },

        "comparators": {
            "baseline_p0":
                base_p0,
            "eta_baseline_p0":
                eta0,
            "local_b0sq_p0":
                local_p0,
            "eta_local_b0sq":
                eta_local,
            "l4_p0":
                l4_p0,
            "eta_l4":
                eta_l4,
            "continuous_baseline":
                continuous,
        },

        "certified_candidates":
            certified_rows,

        "best_certified_candidate":
            best_cert,

        "decision":
            decision,

        "next":
            next_action,

        "large_3d_coupled_scan_authorized":
            bool(
                decision.startswith(
                    "GREEN"
                )
            ),

        "claim_limits": {
            "coupled_field_solved":
                False,
            "full_conservation":
                False,
            "stability":
                False,
            "continuum_certified":
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

    with OUT_JSON.open(
        "w"
    ) as f:
        json.dump(
            summary,
            f,
            indent=2,
            allow_nan=True,
        )

        f.write("\n")

    print(
        "\n=== F — 024A2 "
        "DECISION ===",
        flush=True,
    )

    print(
        "024A2_EXPLICIT_OMEGA_PROCA_"
        "TEACHER_MATCH_PREFILTER="
        f"{decision}"
    )

    print(
        f"BEST_MU_H="
        f"{float(best_cert['mu_h']):.15e}"
    )

    print(
        f"BEST_MU_DX="
        f"{float(best_cert['mu_dx']):.15e}"
    )

    print(
        "BEST_GAIN_VS_BASELINE_REPAIRED="
        f"{float(best_cert['gain_vs_baseline_repaired']):.15e}"
    )

    print(
        "BEST_GAIN_VS_LOCAL_B0SQ_REPAIRED="
        f"{float(best_cert['gain_vs_local_repaired']):.15e}"
    )

    print(
        "BEST_GAIN_VS_L4_REPAIRED="
        f"{float(best_cert['gain_vs_l4_repaired']):.15e}"
    )

    print(
        "BEST_Q_OUTWARD_WEIGHTED_MEDIAN="
        f"{float(best_cert['q_outward_weighted_median']):.15e}"
    )

    print(
        "BEST_Q_TEACHER_ABSDIFF="
        f"{float(best_cert['q_teacher_absdiff']):.15e}"
    )

    print(
        "BEST_PAD_ETA_RELERR="
        f"{float(best_cert['pad_eta_relerr']):.15e}"
    )

    print(
        "BASELINE_CONTINUOUS_AXIS_OK="
        + (
            "YES"
            if baseline_continuous_ok
            else "NO"
        )
    )

    print(
        "PROCA_STATIC_DEC="
        "PASS_ANALYTIC"
    )

    print(
        "GENERALIZED_L2_L4_L6_V_"
        "CONSTITUTIVE_PREFLIGHT="
        "RETAINED_AS_HEAVY_LIMIT_CONTEXT"
    )

    print(
        "PURE_BPS_L6_PLUS_V_"
        "STATIC_TEACHER_MATCH="
        "DEMOTED"
    )

    print(
        "LARGE_3D_COUPLED_OMEGA_SKYRME_"
        "SCAN_AUTHORIZED="
        + (
            "YES"
            if summary[
                "large_3d_coupled_scan_authorized"
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
        "PROJECT_DERIVED_024A2_"
        "EXPLICIT_OMEGA_PROCA_"
        "TEACHER_MATCH_PREFILTER"
    )

    print(
        f"SUMMARY_JSON="
        f"{OUT_JSON.relative_to(ROOT)}"
    )

    print(
        f"MU_SCAN_CSV="
        f"{OUT_CSV.relative_to(ROOT)}"
    )

    print(
        f"SELECTED_FIELD_NPZ="
        f"{OUT_NPZ.relative_to(ROOT)}"
    )

    print(
        "024A2_RUN_COMPLETE=YES"
    )


if __name__ == "__main__":
    main()
