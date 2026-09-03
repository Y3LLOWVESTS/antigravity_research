#!/usr/bin/env python3
"""027D — exact self-closing distributed-stress gate.

PURPOSE
-------
Attack the dominant obstruction identified by 027C.

027C established that the corrected genuine-transfer 027B source retains
strong source-level leverage, but a direct axial DEC load path is too costly:

    robust g_path,max beating 006D
        ~= 0.04560965387393934.

The next question is therefore not whether an arbitrary support multiplier
can be reduced.

The correct question is:

    Can an actual distributed positive-energy, DEC-compatible stress tensor
    close the productive source locally while exploiting radial membrane,
    hoop-return, shear, or mixed stress topology so that the complete
    true-stand-off finite-payload source still beats 006D?

027D answers that question using an exact staggered finite-volume equilibrium
problem.

SCIENTIFIC QUESTION
-------------------
Take the strongest corrected 027C zero-cost-export productive source:

    front negative-active scalar cell,
    rear scalar state,
    causal positive-active link,
    positive DEC-saturating compensation.

Embed it as a fixed positive-energy stress sector.

Then allow an additional support sector with:

    positive energy,
    exact type-I DEC,
    arbitrary p_r,
    arbitrary p_z,
    arbitrary p_phi,
    arbitrary T_rz,

and require the COMBINED source to satisfy:

    exact finite-volume local force balance,
    traction-free finite boundary,
    axis regularity,
    global Laue identities,
    exact total DEC.

Does a self-closing support topology exist, and what is its complete
finite-payload coefficient C?

WHY THIS IS STRONGER THAN 027C
------------------------------
027C represented virial export using

    E_path = g_path D_H L/R.

That was deliberately a direct-member proxy.

027D removes g_path from the physics model.

The support tensor chooses its own spatial load path.

Possible solutions can therefore discover:

    radial membrane spreading,
    hoop stress return,
    distributed shear,
    mixed radial/axial closure,
    compact or broad support.

No rod-like architecture is imposed.

PRODUCTIVE SOURCE
-----------------
Read the completed 027C summary.

Use the more conservative of its two best finite-payload zero-cost-export
candidates.

For the selected candidate:

    E_H, S_H
        front productive source;

    E_R = 1 - E_H
    S_R = qbar - S_H
        rear endpoint;

    E_link
    S_link = 2 E_link
        causal link;

    E_comp
    S_comp = 4 E_comp
        positive Laue compensation.

Blob sectors are represented as compact smooth axisymmetric distributions.

For an isotropic sector with source ratio

    q = S/E,

the pressure ratio is

    w = p/rho = (q - 1)/3.

The link is tested in two forms:

    ISOTROPIC_LINK:
        p_r = p_z = p_phi = rho/3.

    AXIAL_LINK:
        p_z = rho,
        p_r = p_phi = 0.

Both have

    S/rho = 2

and satisfy DEC.

SUPPORT SECTOR
--------------
Unknown support variables:

    e_s         cell energy density >= 0
    p_phi,s     cell-centered hoop stress
    p_r,s       radial-face stress
    p_z,s       z-face stress
    T_rz,s      vertex shear.

Cell-centered support stress:

        [p_r    T_rz   0]
        [T_rz   p_z    0]
        [0       0    p_phi].

Exact support DEC is imposed with the spectral second-order-cone condition

    max |lambda_i| <= e_s.

The same exact condition is independently imposed on the total
productive + support stress.

LOCAL CONSERVATION
------------------
The total source obeys the axisymmetric equations

    (1/r) d(r p_r)/dr
      + d(T_rz)/dz
      - p_phi/r
      = 0,

    (1/r) d(r T_rz)/dr
      + d(p_z)/dz
      = 0.

They are imposed as exact integrated annular-cell force balances.

The support boundary is traction free.

GLOBAL LAUE
-----------
Independent necessary checks:

    integral (p_r + p_phi) dV = 0,

    integral p_z dV = 0.

FINITE PAYLOAD
--------------
Payload center:

    z/h = 1.

Payload radii audited:

    R_P/h = 0.25,
    R_P/h = 0.50.

The optimization uses the exact finite-spherical-payload axial cell kernel.

After each promising solution, independently reconstruct the field over:

    payload center,
    17 polar samples on R_P/h = 0.25,
    17 polar samples on R_P/h = 0.50.

The post-audit uses direct three-dimensional annular quadrature.

Promotion requires every sample to remain outward.

COEFFICIENT
-----------
For total positive source energy E and weakest audited outward acceleration A:

    C_robust = E/A.

Benchmarks:

    C_006D
        = 23.591586299249

    C_024D
        = 6.610457607426174.

SEARCH
------
Stage 1:
    low-resolution topology scan over radial support envelopes

        R_max/h =
        1.5,
        2.5,
        3.5,
        5.0

    and both link stress models.

Stage 2:
    refine the strongest architecture.

Stage 3:
    compute a Pareto family by permitting additional support energy and
    maximizing outward finite-payload response.

Physical budget multipliers:

    1.0,
    1.25,
    1.5,
    2.0,
    3.0,
    4.0

relative to the minimum support energy.

Blind wildcard diagnostics:

    0.625,
    1.6,
    1.875,
    3.125,
    5.0.

Wildcard points are explicitly excluded from scientific selection.

PROMOTION
---------
MAJOR_GREEN:

    primary and high resolution both satisfy
        support DEC,
        total DEC,
        exact conservation,
        Laue,
        all-payload outward sign;

    primary/high robust C relative difference <= 0.20;

    conservative C_robust < C_024D.

GREEN:

    same requirements,
    but

        C_robust < C_006D.

YELLOW:

    an exact self-closing DEC source exists and remains outward,
    but does not beat 006D.

RED:

    no finite self-closing DEC support can retain outward payload response
    in the tested envelopes.

SOURCE-SIDE 80% HEURISTIC
-------------------------
Only authorized if MAJOR_GREEN is obtained with resolution convergence.

This is still a source/sign-engine accomplishment, not overall practical
antigravity.

CLAIM LIMITS
------------
027D does NOT establish:

    a microscopic Lagrangian realization;
    the full dynamic shuttle T^{0i};
    formation/collapse/reset reaction momentum;
    radiation lifetime;
    unrestricted stability;
    nonlinear Einstein-matter continuation;
    removal of the 1/G scaling;
    a practical device.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_EXACT_CONSERVATION_DEC_SOURCE_ARCHITECTURE_GATE

NOVEL PHYSICS CLAIM
-------------------
NO.
"""

from __future__ import annotations

from dataclasses import dataclass
import csv
import json
import math
import os
from pathlib import Path
from typing import Any

import cvxpy as cp
import numpy as np
from numpy.polynomial.legendre import leggauss


C_006D = 23.591586299249
C_024D = 6.610457607426174

G_PATH_027C_ROBUST = 0.04560965387393934

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "data"

LINEAGE = DATA / "027c_virial_load_path_gate_summary.json"

OUT_JSON = DATA / "027d_exact_self_closing_stress_summary.json"
OUT_CSV = DATA / "027d_exact_self_closing_stress_cases.csv"
OUT_WILDCARD = DATA / "027d_exact_self_closing_wildcard_audit.csv"
OUT_NPZ = DATA / "027d_exact_self_closing_best_source.npz"

SMOKE = os.environ.get("AG027D_SMOKE", "0") == "1"

PAYLOAD_RADII = (
    0.25,
    0.50,
)

PAYLOAD_MU = np.linspace(
    -1.0,
    1.0,
    17,
)

PHYSICAL_BUDGET_FACTORS = (
    1.0,
    1.25,
    1.5,
    2.0,
    3.0,
    4.0,
)

BLIND_BUDGET_FACTORS = (
    0.625,
    1.6,
    1.875,
    3.125,
    5.0,
)

DEC_TOL = 4.0e-5
CONS_TOL = 4.0e-5
LAUE_TOL = 4.0e-5
CONVERGENCE_TOL = 0.20

GAUSS_ORDER = 6


@dataclass(frozen=True)
class Geometry:
    """One axisymmetric finite-volume support geometry."""

    nr: int
    nz: int
    rmax: float
    zmin: float
    zmax: float
    radial_power: float
    target_z: float
    payload_radius: float

    r_edges: np.ndarray
    z_edges: np.ndarray
    r_centers: np.ndarray
    z_centers: np.ndarray
    volumes: np.ndarray
    kernels: np.ndarray


@dataclass
class ProductiveSource:
    """Fixed 027C-derived productive stress sector on one grid."""

    e_cell: np.ndarray
    pphi_cell: np.ndarray

    pr_face: np.ndarray
    pz_face: np.ndarray

    pr_cell: np.ndarray
    pz_cell: np.ndarray
    trz_cell: np.ndarray

    active_cell: np.ndarray

    energy_components: dict[str, float]
    active_components: dict[str, float]

    product_total_energy: float
    product_total_active: float

    metadata: dict[str, Any]


@dataclass
class Model:
    """One reusable convex closure model."""

    geometry: Geometry
    product: ProductiveSource
    link_model: str

    e_sup: cp.Variable
    pphi_sup: cp.Variable
    pr_face_sup: cp.Variable
    pz_face_sup: cp.Variable
    trz_vertex_sup: cp.Variable

    support_mass: cp.Expression
    total_mass: cp.Expression
    acceleration: cp.Expression

    constraints: list[cp.Constraint]


def require_file(path: Path) -> None:
    """Fail closed if a required artifact is absent."""

    if not path.is_file():
        raise RuntimeError(
            f"Required artifact missing: {path}"
        )


require_file(LINEAGE)

with LINEAGE.open(
    "r",
    encoding="utf-8",
) as f:
    J027C = json.load(f)


def select_027c_candidate() -> dict[str, Any]:
    """Select the conservative completed zero-cost-export 027C candidate."""

    candidates = []

    for seed in J027C.get(
        "seeds",
        [],
    ):
        row = seed.get(
            "best_dense_global_control"
        )

        if row is not None:
            candidates.append(
                row
            )

    if not candidates:
        raise RuntimeError(
            "027C contains no finite-payload global-control candidate"
        )

    return max(
        candidates,
        key=lambda row: float(
            row[
                "C_payload"
            ]
        ),
    )


SOURCE_ROW = select_027c_candidate()
SOURCE_META = SOURCE_ROW["meta"]


def component_ledger() -> dict[str, float]:
    """Recover the normalized productive source ledger."""

    e_high = float(
        SOURCE_META[
            "E_high"
        ]
    )

    s_high = float(
        SOURCE_META[
            "S_high"
        ]
    )

    qbar = float(
        SOURCE_META[
            "qbar"
        ]
    )

    e_rear = (
        1.0
        - e_high
    )

    s_rear = (
        qbar
        - s_high
    )

    e_link = float(
        SOURCE_META[
            "E_link"
        ]
    )

    s_link = (
        2.0
        * e_link
    )

    e_comp = float(
        SOURCE_ROW[
            "E_comp"
        ]
    )

    s_comp = (
        4.0
        * e_comp
    )

    return {
        "E_HIGH": e_high,
        "S_HIGH": s_high,
        "E_REAR": e_rear,
        "S_REAR": s_rear,
        "E_LINK": e_link,
        "S_LINK": s_link,
        "E_COMP": e_comp,
        "S_COMP": s_comp,
    }


LEDGER = component_ledger()


def isotropic_w(
    energy: float,
    active: float,
) -> float:
    """Return p/rho for an isotropic component with active ratio S/rho."""

    if energy <= 0.0:
        raise RuntimeError(
            "Nonpositive productive component energy"
        )

    q = (
        active
        / energy
    )

    w = (
        q
        - 1.0
    ) / 3.0

    if abs(w) > 1.0 + 1.0e-10:
        raise RuntimeError(
            f"Productive isotropic component violates DEC: w={w}"
        )

    return float(w)


W_HIGH = isotropic_w(
    LEDGER["E_HIGH"],
    LEDGER["S_HIGH"],
)

W_REAR = isotropic_w(
    LEDGER["E_REAR"],
    LEDGER["S_REAR"],
)

W_COMP = isotropic_w(
    LEDGER["E_COMP"],
    LEDGER["S_COMP"],
)


def gauss_interval(
    a: float,
    b: float,
    order: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Return Gauss-Legendre nodes and weights on one interval."""

    x0, w0 = leggauss(
        order
    )

    x = (
        0.5
        * (
            a
            + b
        )
        + 0.5
        * (
            b
            - a
        )
        * x0
    )

    w = (
        0.5
        * (
            b
            - a
        )
        * w0
    )

    return x, w


def finite_payload_cell_kernel(
    r0: float,
    r1: float,
    z0: float,
    z1: float,
    target_z: float,
    payload_radius: float,
) -> float:
    """Exact annular-cell kernel for a uniform spherical payload average."""

    rr, rw = gauss_interval(
        r0,
        r1,
        GAUSS_ORDER,
    )

    zz, zw = gauss_interval(
        z0,
        z1,
        GAUSS_ORDER,
    )

    R, Z = np.meshgrid(
        rr,
        zz,
        indexing="ij",
    )

    WR, WZ = np.meshgrid(
        rw,
        zw,
        indexing="ij",
    )

    dzp = (
        Z
        - target_z
    )

    d2 = (
        R
        * R
        + dzp
        * dzp
    )

    d = np.sqrt(
        d2
    )

    denominator = np.maximum(
        d2
        * d,
        payload_radius
        ** 3,
    )

    integrand = (
        2.0
        * math.pi
        * R
        * dzp
        / denominator
    )

    return float(
        np.sum(
            WR
            * WZ
            * integrand
        )
    )


def build_geometry(
    nr: int,
    nz: int,
    rmax: float,
    zmin: float,
    *,
    radial_power: float = 1.55,
    target_z: float = 1.0,
    payload_radius: float = 0.50,
) -> Geometry:
    """Construct a nonuniform-r / uniform-z staggered support grid."""

    u = np.linspace(
        0.0,
        1.0,
        nr + 1,
    )

    r_edges = (
        rmax
        * u
        ** radial_power
    )

    z_edges = np.linspace(
        zmin,
        0.0,
        nz + 1,
    )

    r_centers = (
        0.5
        * (
            r_edges[:-1]
            + r_edges[1:]
        )
    )

    z_centers = (
        0.5
        * (
            z_edges[:-1]
            + z_edges[1:]
        )
    )

    volumes = np.zeros(
        (
            nr,
            nz,
        ),
        dtype=float,
    )

    kernels = np.zeros_like(
        volumes
    )

    for i in range(
        nr
    ):
        r0 = float(
            r_edges[
                i
            ]
        )

        r1 = float(
            r_edges[
                i + 1
            ]
        )

        annulus = (
            math.pi
            * (
                r1
                * r1
                - r0
                * r0
            )
        )

        for j in range(
            nz
        ):
            z0 = float(
                z_edges[
                    j
                ]
            )

            z1 = float(
                z_edges[
                    j + 1
                ]
            )

            volumes[
                i,
                j,
            ] = (
                annulus
                * (
                    z1
                    - z0
                )
            )

            kernels[
                i,
                j,
            ] = finite_payload_cell_kernel(
                r0,
                r1,
                z0,
                z1,
                target_z,
                payload_radius,
            )

    return Geometry(
        nr=nr,
        nz=nz,
        rmax=rmax,
        zmin=zmin,
        zmax=0.0,
        radial_power=radial_power,
        target_z=target_z,
        payload_radius=payload_radius,
        r_edges=r_edges,
        z_edges=z_edges,
        r_centers=r_centers,
        z_centers=z_centers,
        volumes=volumes,
        kernels=kernels,
    )


def compact_blob_shape(
    r,
    z,
    z_center: float,
    radius: float,
):
    """Smooth compact C1-ish spherical bump."""

    d2 = (
        np.asarray(
            r
        )
        ** 2
        + (
            np.asarray(
                z
            )
            - z_center
        )
        ** 2
    )

    x2 = (
        d2
        / (
            radius
            * radius
        )
    )

    return np.where(
        x2 < 1.0,
        (
            1.0
            - x2
        )
        ** 2,
        0.0,
    )


def tube_shape(
    r,
    z,
    z_front: float,
    z_rear: float,
    radius: float,
):
    """Compact axial tube with smooth endpoint taper."""

    r = np.asarray(
        r
    )

    z = np.asarray(
        z
    )

    radial_x2 = (
        r
        * r
        / (
            radius
            * radius
        )
    )

    radial = np.where(
        radial_x2 < 1.0,
        (
            1.0
            - radial_x2
        )
        ** 2,
        0.0,
    )

    upper = max(
        z_front,
        z_rear,
    )

    lower = min(
        z_front,
        z_rear,
    )

    length = (
        upper
        - lower
    )

    t = (
        z
        - lower
    ) / length

    axial = np.where(
        (
            t > 0.0
        )
        & (
            t < 1.0
        ),
        np.sin(
            math.pi
            * t
        )
        ** 2,
        0.0,
    )

    return (
        radial
        * axial
    )


def normalized_component(
    geometry: Geometry,
    shape_cell: np.ndarray,
    energy: float,
) -> float:
    """Return density normalization for an exact requested grid energy."""

    raw = float(
        np.sum(
            geometry.volumes
            * shape_cell
        )
    )

    if raw <= 0.0:
        raise RuntimeError(
            "Productive component disappeared on grid"
        )

    return (
        energy
        / raw
    )


def build_productive_source(
    geometry: Geometry,
    link_model: str,
) -> ProductiveSource:
    """Discretize the corrected 027C productive source on one grid."""

    if link_model not in (
        "ISOTROPIC_LINK",
        "AXIAL_LINK",
    ):
        raise ValueError(
            link_model
        )

    target_z = 1.0

    d_high = float(
        SOURCE_META[
            "d_high"
        ]
    )

    d_low = float(
        SOURCE_META[
            "d_low"
        ]
    )

    d_comp = float(
        SOURCE_META[
            "d_comp"
        ]
    )

    z_high = (
        target_z
        - d_high
    )

    z_rear = (
        target_z
        - d_low
    )

    z_comp = (
        target_z
        - d_comp
    )

    nominal_radius = float(
        SOURCE_META[
            "radius"
        ]
    )

    front_radius = min(
        max(
            0.19,
            nominal_radius,
        ),
        0.94
        * abs(
            z_high
        ),
    )

    rear_radius = max(
        0.24,
        nominal_radius,
    )

    comp_radius = max(
        0.28,
        1.15
        * nominal_radius,
    )

    link_radius = max(
        0.12,
        0.60
        * front_radius,
    )

    RC, ZC = np.meshgrid(
        geometry.r_centers,
        geometry.z_centers,
        indexing="ij",
    )

    RR_FACE, ZR_FACE = np.meshgrid(
        geometry.r_edges,
        geometry.z_centers,
        indexing="ij",
    )

    RZ_FACE, ZZ_FACE = np.meshgrid(
        geometry.r_centers,
        geometry.z_edges,
        indexing="ij",
    )

    components = [
        {
            "name": "HIGH",
            "kind": "BLOB",
            "energy": LEDGER[
                "E_HIGH"
            ],
            "active": LEDGER[
                "S_HIGH"
            ],
            "w": W_HIGH,
            "z": z_high,
            "radius": front_radius,
        },
        {
            "name": "REAR",
            "kind": "BLOB",
            "energy": LEDGER[
                "E_REAR"
            ],
            "active": LEDGER[
                "S_REAR"
            ],
            "w": W_REAR,
            "z": z_rear,
            "radius": rear_radius,
        },
        {
            "name": "COMP",
            "kind": "BLOB",
            "energy": LEDGER[
                "E_COMP"
            ],
            "active": LEDGER[
                "S_COMP"
            ],
            "w": W_COMP,
            "z": z_comp,
            "radius": comp_radius,
        },
    ]

    e_cell = np.zeros(
        (
            geometry.nr,
            geometry.nz,
        ),
        dtype=float,
    )

    pphi_cell = np.zeros_like(
        e_cell
    )

    pr_face = np.zeros(
        (
            geometry.nr + 1,
            geometry.nz,
        ),
        dtype=float,
    )

    pz_face = np.zeros(
        (
            geometry.nr,
            geometry.nz + 1,
        ),
        dtype=float,
    )

    energy_components: dict[str, float] = {}
    active_components: dict[str, float] = {}

    for c in components:
        shape_c = compact_blob_shape(
            RC,
            ZC,
            c[
                "z"
            ],
            c[
                "radius"
            ],
        )

        norm = normalized_component(
            geometry,
            shape_c,
            float(
                c[
                    "energy"
                ]
            ),
        )

        rho_c = (
            norm
            * shape_c
        )

        shape_r = compact_blob_shape(
            RR_FACE,
            ZR_FACE,
            c[
                "z"
            ],
            c[
                "radius"
            ],
        )

        shape_z = compact_blob_shape(
            RZ_FACE,
            ZZ_FACE,
            c[
                "z"
            ],
            c[
                "radius"
            ],
        )

        rho_r = (
            norm
            * shape_r
        )

        rho_z = (
            norm
            * shape_z
        )

        w = float(
            c[
                "w"
            ]
        )

        e_cell += rho_c
        pphi_cell += (
            w
            * rho_c
        )
        pr_face += (
            w
            * rho_r
        )
        pz_face += (
            w
            * rho_z
        )

        energy_components[
            c[
                "name"
            ]
        ] = float(
            np.sum(
                geometry.volumes
                * rho_c
            )
        )

        active_components[
            c[
                "name"
            ]
        ] = (
            (
                1.0
                + 3.0
                * w
            )
            * energy_components[
                c[
                    "name"
                ]
            ]
        )

    link_cell_shape = tube_shape(
        RC,
        ZC,
        z_high,
        z_rear,
        link_radius,
    )

    link_norm = normalized_component(
        geometry,
        link_cell_shape,
        LEDGER[
            "E_LINK"
        ],
    )

    rho_link_cell = (
        link_norm
        * link_cell_shape
    )

    rho_link_r = (
        link_norm
        * tube_shape(
            RR_FACE,
            ZR_FACE,
            z_high,
            z_rear,
            link_radius,
        )
    )

    rho_link_z = (
        link_norm
        * tube_shape(
            RZ_FACE,
            ZZ_FACE,
            z_high,
            z_rear,
            link_radius,
        )
    )

    e_cell += rho_link_cell

    if (
        link_model
        == "ISOTROPIC_LINK"
    ):
        pphi_cell += (
            rho_link_cell
            / 3.0
        )

        pr_face += (
            rho_link_r
            / 3.0
        )

        pz_face += (
            rho_link_z
            / 3.0
        )

    else:
        pz_face += (
            rho_link_z
        )

    energy_components[
        "LINK"
    ] = float(
        np.sum(
            geometry.volumes
            * rho_link_cell
        )
    )

    active_components[
        "LINK"
    ] = (
        2.0
        * energy_components[
            "LINK"
        ]
    )

    pr_cell = (
        0.5
        * (
            pr_face[:-1, :]
            + pr_face[1:, :]
        )
    )

    pz_cell = (
        0.5
        * (
            pz_face[:, :-1]
            + pz_face[:, 1:]
        )
    )

    trz_cell = np.zeros_like(
        e_cell
    )

    active_cell = (
        e_cell
        + pr_cell
        + pz_cell
        + pphi_cell
    )

    product_total_energy = float(
        np.sum(
            geometry.volumes
            * e_cell
        )
    )

    product_total_active = float(
        np.sum(
            geometry.volumes
            * active_cell
        )
    )

    metadata = {
        "link_model": link_model,
        "z_high": z_high,
        "z_rear": z_rear,
        "z_comp": z_comp,
        "front_radius": front_radius,
        "rear_radius": rear_radius,
        "comp_radius": comp_radius,
        "link_radius": link_radius,
        "source_meta": SOURCE_META,
        "source_row_C_payload": SOURCE_ROW[
            "C_payload"
        ],
    }

    return ProductiveSource(
        e_cell=e_cell,
        pphi_cell=pphi_cell,
        pr_face=pr_face,
        pz_face=pz_face,
        pr_cell=pr_cell,
        pz_cell=pz_cell,
        trz_cell=trz_cell,
        active_cell=active_cell,
        energy_components=energy_components,
        active_components=active_components,
        product_total_energy=product_total_energy,
        product_total_active=product_total_active,
        metadata=metadata,
    )


def soc_dec_constraints(
    constraints: list[cp.Constraint],
    energy,
    pr,
    pz,
    trz,
    pphi,
) -> None:
    """Append exact type-I DEC SOC constraints for one cell."""

    mean = (
        0.5
        * (
            pr
            + pz
        )
    )

    half_difference = (
        0.5
        * (
            pr
            - pz
        )
    )

    spectral_radius = cp.norm(
        cp.hstack(
            [
                half_difference,
                trz,
            ]
        ),
        2,
    )

    constraints.extend(
        [
            spectral_radius
            <= energy
            - mean,

            spectral_radius
            <= energy
            + mean,

            pphi
            <= energy,

            -pphi
            <= energy,
        ]
    )


def build_model(
    geometry: Geometry,
    link_model: str,
) -> Model:
    """Build one exact combined productive+support convex closure problem."""

    product = build_productive_source(
        geometry,
        link_model,
    )

    nr = geometry.nr
    nz = geometry.nz

    e_sup = cp.Variable(
        (
            nr,
            nz,
        ),
        nonneg=True,
        name=(
            "027d_es_"
            + link_model
        ),
    )

    pphi_sup = cp.Variable(
        (
            nr,
            nz,
        ),
        name=(
            "027d_pphi_"
            + link_model
        ),
    )

    pr_face_sup = cp.Variable(
        (
            nr + 1,
            nz,
        ),
        name=(
            "027d_pr_"
            + link_model
        ),
    )

    pz_face_sup = cp.Variable(
        (
            nr,
            nz + 1,
        ),
        name=(
            "027d_pz_"
            + link_model
        ),
    )

    trz_vertex_sup = cp.Variable(
        (
            nr + 1,
            nz + 1,
        ),
        name=(
            "027d_trz_"
            + link_model
        ),
    )

    constraints: list[cp.Constraint] = []

    constraints.extend(
        [
            pr_face_sup[
                nr,
                :,
            ]
            == 0.0,

            pz_face_sup[
                :,
                0,
            ]
            == 0.0,

            pz_face_sup[
                :,
                nz,
            ]
            == 0.0,

            trz_vertex_sup[
                0,
                :,
            ]
            == 0.0,

            trz_vertex_sup[
                nr,
                :,
            ]
            == 0.0,

            trz_vertex_sup[
                :,
                0,
            ]
            == 0.0,

            trz_vertex_sup[
                :,
                nz,
            ]
            == 0.0,
        ]
    )

    pr_sup_cell: list[list[cp.Expression]] = [
        [
            None
            for _ in range(
                nz
            )
        ]
        for _ in range(
            nr
        )
    ]  # type: ignore[list-item]

    pz_sup_cell: list[list[cp.Expression]] = [
        [
            None
            for _ in range(
                nz
            )
        ]
        for _ in range(
            nr
        )
    ]  # type: ignore[list-item]

    trz_sup_cell: list[list[cp.Expression]] = [
        [
            None
            for _ in range(
                nz
            )
        ]
        for _ in range(
            nr
        )
    ]  # type: ignore[list-item]

    for j in range(
        nz
    ):
        constraints.append(
            (
                pr_face_sup[
                    0,
                    j,
                ]
                + product.pr_face[
                    0,
                    j,
                ]
            )
            ==
            (
                pphi_sup[
                    0,
                    j,
                ]
                + product.pphi_cell[
                    0,
                    j,
                ]
            )
        )

    for i in range(
        nr
    ):
        for j in range(
            nz
        ):
            pr_s = (
                0.5
                * (
                    pr_face_sup[
                        i,
                        j,
                    ]
                    + pr_face_sup[
                        i + 1,
                        j,
                    ]
                )
            )

            pz_s = (
                0.5
                * (
                    pz_face_sup[
                        i,
                        j,
                    ]
                    + pz_face_sup[
                        i,
                        j + 1,
                    ]
                )
            )

            trz_s = (
                0.25
                * (
                    trz_vertex_sup[
                        i,
                        j,
                    ]
                    + trz_vertex_sup[
                        i + 1,
                        j,
                    ]
                    + trz_vertex_sup[
                        i,
                        j + 1,
                    ]
                    + trz_vertex_sup[
                        i + 1,
                        j + 1,
                    ]
                )
            )

            pr_sup_cell[
                i
            ][
                j
            ] = pr_s

            pz_sup_cell[
                i
            ][
                j
            ] = pz_s

            trz_sup_cell[
                i
            ][
                j
            ] = trz_s

            soc_dec_constraints(
                constraints,
                e_sup[
                    i,
                    j,
                ],
                pr_s,
                pz_s,
                trz_s,
                pphi_sup[
                    i,
                    j,
                ],
            )

            total_e = (
                e_sup[
                    i,
                    j,
                ]
                + product.e_cell[
                    i,
                    j,
                ]
            )

            total_pr = (
                pr_s
                + product.pr_cell[
                    i,
                    j,
                ]
            )

            total_pz = (
                pz_s
                + product.pz_cell[
                    i,
                    j,
                ]
            )

            total_trz = trz_s

            total_pphi = (
                pphi_sup[
                    i,
                    j,
                ]
                + product.pphi_cell[
                    i,
                    j,
                ]
            )

            soc_dec_constraints(
                constraints,
                total_e,
                total_pr,
                total_pz,
                total_trz,
                total_pphi,
            )

    for i in range(
        nr
    ):
        r0 = float(
            geometry.r_edges[
                i
            ]
        )

        r1 = float(
            geometry.r_edges[
                i + 1
            ]
        )

        dr = (
            r1
            - r0
        )

        annular_radial_factor = (
            0.5
            * (
                r1
                * r1
                - r0
                * r0
            )
        )

        for j in range(
            nz
        ):
            z0 = float(
                geometry.z_edges[
                    j
                ]
            )

            z1 = float(
                geometry.z_edges[
                    j + 1
                ]
            )

            dz = (
                z1
                - z0
            )

            pr_w = (
                pr_face_sup[
                    i,
                    j,
                ]
                + product.pr_face[
                    i,
                    j,
                ]
            )

            pr_e = (
                pr_face_sup[
                    i + 1,
                    j,
                ]
                + product.pr_face[
                    i + 1,
                    j,
                ]
            )

            pz_south = (
                pz_face_sup[
                    i,
                    j,
                ]
                + product.pz_face[
                    i,
                    j,
                ]
            )

            pz_north = (
                pz_face_sup[
                    i,
                    j + 1,
                ]
                + product.pz_face[
                    i,
                    j + 1,
                ]
            )

            pphi_total = (
                pphi_sup[
                    i,
                    j,
                ]
                + product.pphi_cell[
                    i,
                    j,
                ]
            )

            trz_south = (
                0.5
                * (
                    trz_vertex_sup[
                        i,
                        j,
                    ]
                    + trz_vertex_sup[
                        i + 1,
                        j,
                    ]
                )
            )

            trz_north = (
                0.5
                * (
                    trz_vertex_sup[
                        i,
                        j + 1,
                    ]
                    + trz_vertex_sup[
                        i + 1,
                        j + 1,
                    ]
                )
            )

            trz_west = (
                0.5
                * (
                    trz_vertex_sup[
                        i,
                        j,
                    ]
                    + trz_vertex_sup[
                        i,
                        j + 1,
                    ]
                )
            )

            trz_east = (
                0.5
                * (
                    trz_vertex_sup[
                        i + 1,
                        j,
                    ]
                    + trz_vertex_sup[
                        i + 1,
                        j + 1,
                    ]
                )
            )

            radial_balance = (
                dz
                * (
                    r1
                    * pr_e
                    - r0
                    * pr_w
                )
                + annular_radial_factor
                * (
                    trz_north
                    - trz_south
                )
                - dr
                * dz
                * pphi_total
            )

            vertical_balance = (
                2.0
                * dz
                * (
                    r1
                    * trz_east
                    - r0
                    * trz_west
                )
                + (
                    r1
                    * r1
                    - r0
                    * r0
                )
                * (
                    pz_north
                    - pz_south
                )
            )

            constraints.extend(
                [
                    radial_balance
                    == 0.0,

                    vertical_balance
                    == 0.0,
                ]
            )

    pr_sup_matrix = cp.vstack(
        [
            cp.hstack(
                [
                    pr_sup_cell[
                        i
                    ][
                        j
                    ]
                    for j in range(
                        nz
                    )
                ]
            )
            for i in range(
                nr
            )
        ]
    )

    pz_sup_matrix = cp.vstack(
        [
            cp.hstack(
                [
                    pz_sup_cell[
                        i
                    ][
                        j
                    ]
                    for j in range(
                        nz
                    )
                ]
            )
            for i in range(
                nr
            )
        ]
    )

    trz_sup_matrix = cp.vstack(
        [
            cp.hstack(
                [
                    trz_sup_cell[
                        i
                    ][
                        j
                    ]
                    for j in range(
                        nz
                    )
                ]
            )
            for i in range(
                nr
            )
        ]
    )

    total_pr_matrix = (
        pr_sup_matrix
        + cp.Constant(
            product.pr_cell
        )
    )

    total_pz_matrix = (
        pz_sup_matrix
        + cp.Constant(
            product.pz_cell
        )
    )

    total_pphi_matrix = (
        pphi_sup
        + cp.Constant(
            product.pphi_cell
        )
    )

    volume_constant = cp.Constant(
        geometry.volumes
    )

    constraints.extend(
        [
            cp.sum(
                cp.multiply(
                    volume_constant,
                    total_pr_matrix
                    + total_pphi_matrix,
                )
            )
            == 0.0,

            cp.sum(
                cp.multiply(
                    volume_constant,
                    total_pz_matrix,
                )
            )
            == 0.0,
        ]
    )

    support_active = (
        e_sup
        + pr_sup_matrix
        + pz_sup_matrix
        + pphi_sup
    )

    total_active = (
        cp.Constant(
            product.active_cell
        )
        + support_active
    )

    support_mass = cp.sum(
        cp.multiply(
            volume_constant,
            e_sup,
        )
    )

    total_mass = (
        product.product_total_energy
        + support_mass
    )

    acceleration = cp.sum(
        cp.multiply(
            cp.Constant(
                geometry.kernels
            ),
            total_active,
        )
    )

    return Model(
        geometry=geometry,
        product=product,
        link_model=link_model,
        e_sup=e_sup,
        pphi_sup=pphi_sup,
        pr_face_sup=pr_face_sup,
        pz_face_sup=pz_face_sup,
        trz_vertex_sup=trz_vertex_sup,
        support_mass=support_mass,
        total_mass=total_mass,
        acceleration=acceleration,
        constraints=constraints,
    )


def solve_problem(
    problem: cp.Problem,
) -> tuple[str, str]:
    """Solve with Clarabel and fail over to SCS."""

    installed = cp.installed_solvers()

    solver = (
        "CLARABEL"
        if "CLARABEL"
        in installed
        else "SCS"
    )

    try:
        if (
            solver
            == "CLARABEL"
        ):
            problem.solve(
                solver=solver,
                verbose=False,
            )

        else:
            problem.solve(
                solver=solver,
                verbose=False,
                eps=2.0e-5,
                max_iters=200000,
            )

    except Exception:
        if (
            solver
            != "SCS"
            and "SCS"
            in installed
        ):
            solver = "SCS"

            problem.solve(
                solver=solver,
                verbose=False,
                eps=2.0e-5,
                max_iters=200000,
            )

        else:
            raise

    return (
        str(
            problem.status
        ),
        solver,
    )


def extract_arrays(
    model: Model,
) -> dict[str, np.ndarray]:
    """Extract solved support and total source arrays."""

    e_sup = np.asarray(
        model.e_sup.value,
        dtype=float,
    )

    pphi_sup = np.asarray(
        model.pphi_sup.value,
        dtype=float,
    )

    prf_sup = np.asarray(
        model.pr_face_sup.value,
        dtype=float,
    )

    pzf_sup = np.asarray(
        model.pz_face_sup.value,
        dtype=float,
    )

    trzv_sup = np.asarray(
        model.trz_vertex_sup.value,
        dtype=float,
    )

    pr_sup = (
        0.5
        * (
            prf_sup[:-1, :]
            + prf_sup[1:, :]
        )
    )

    pz_sup = (
        0.5
        * (
            pzf_sup[:, :-1]
            + pzf_sup[:, 1:]
        )
    )

    trz_sup = (
        0.25
        * (
            trzv_sup[:-1, :-1]
            + trzv_sup[1:, :-1]
            + trzv_sup[:-1, 1:]
            + trzv_sup[1:, 1:]
        )
    )

    e_total = (
        model.product.e_cell
        + e_sup
    )

    pr_total = (
        model.product.pr_cell
        + pr_sup
    )

    pz_total = (
        model.product.pz_cell
        + pz_sup
    )

    pphi_total = (
        model.product.pphi_cell
        + pphi_sup
    )

    active_total = (
        e_total
        + pr_total
        + pz_total
        + pphi_total
    )

    return {
        "e_sup": e_sup,
        "pphi_sup": pphi_sup,
        "prf_sup": prf_sup,
        "pzf_sup": pzf_sup,
        "trzv_sup": trzv_sup,
        "pr_sup": pr_sup,
        "pz_sup": pz_sup,
        "trz_sup": trz_sup,
        "e_total": e_total,
        "pr_total": pr_total,
        "pz_total": pz_total,
        "pphi_total": pphi_total,
        "active_total": active_total,
    }


def dec_violation(
    e: np.ndarray,
    pr: np.ndarray,
    pz: np.ndarray,
    trz: np.ndarray,
    pphi: np.ndarray,
) -> float:
    """Return maximum eigenvalue-minus-energy DEC violation."""

    worst = 0.0

    for index in np.ndindex(
        e.shape
    ):
        i, j = index

        matrix = np.array(
            [
                [
                    pr[
                        i,
                        j,
                    ],
                    trz[
                        i,
                        j,
                    ],
                    0.0,
                ],
                [
                    trz[
                        i,
                        j,
                    ],
                    pz[
                        i,
                        j,
                    ],
                    0.0,
                ],
                [
                    0.0,
                    0.0,
                    pphi[
                        i,
                        j,
                    ],
                ],
            ],
            dtype=float,
        )

        largest = float(
            np.max(
                np.abs(
                    np.linalg.eigvalsh(
                        matrix
                    )
                )
            )
        )

        worst = max(
            worst,
            largest
            - e[
                i,
                j,
            ],
        )

    return worst


def conservation_relative_residual(
    model: Model,
    arrays: dict[str, np.ndarray],
) -> float:
    """Reconstruct normalized integrated total cell-force residual."""

    g = model.geometry
    p = model.product

    prf = (
        arrays[
            "prf_sup"
        ]
        + p.pr_face
    )

    pzf = (
        arrays[
            "pzf_sup"
        ]
        + p.pz_face
    )

    trzv = arrays[
        "trzv_sup"
    ]

    pphi = arrays[
        "pphi_total"
    ]

    worst = 0.0

    for i in range(
        g.nr
    ):
        r0 = float(
            g.r_edges[
                i
            ]
        )

        r1 = float(
            g.r_edges[
                i + 1
            ]
        )

        dr = (
            r1
            - r0
        )

        arf = (
            0.5
            * (
                r1
                * r1
                - r0
                * r0
            )
        )

        for j in range(
            g.nz
        ):
            z0 = float(
                g.z_edges[
                    j
                ]
            )

            z1 = float(
                g.z_edges[
                    j + 1
                ]
            )

            dz = (
                z1
                - z0
            )

            ts = (
                0.5
                * (
                    trzv[
                        i,
                        j,
                    ]
                    + trzv[
                        i + 1,
                        j,
                    ]
                )
            )

            tn = (
                0.5
                * (
                    trzv[
                        i,
                        j + 1,
                    ]
                    + trzv[
                        i + 1,
                        j + 1,
                    ]
                )
            )

            tw = (
                0.5
                * (
                    trzv[
                        i,
                        j,
                    ]
                    + trzv[
                        i,
                        j + 1,
                    ]
                )
            )

            te = (
                0.5
                * (
                    trzv[
                        i + 1,
                        j,
                    ]
                    + trzv[
                        i + 1,
                        j + 1,
                    ]
                )
            )

            radial_terms = np.array(
                [
                    dz
                    * r1
                    * prf[
                        i + 1,
                        j,
                    ],

                    -dz
                    * r0
                    * prf[
                        i,
                        j,
                    ],

                    arf
                    * tn,

                    -arf
                    * ts,

                    -dr
                    * dz
                    * pphi[
                        i,
                        j,
                    ],
                ]
            )

            vertical_terms = np.array(
                [
                    2.0
                    * dz
                    * r1
                    * te,

                    -2.0
                    * dz
                    * r0
                    * tw,

                    (
                        r1
                        * r1
                        - r0
                        * r0
                    )
                    * pzf[
                        i,
                        j + 1,
                    ],

                    -(
                        r1
                        * r1
                        - r0
                        * r0
                    )
                    * pzf[
                        i,
                        j,
                    ],
                ]
            )

            for terms in (
                radial_terms,
                vertical_terms,
            ):
                numerator = abs(
                    float(
                        np.sum(
                            terms
                        )
                    )
                )

                denominator = max(
                    float(
                        np.sum(
                            np.abs(
                                terms
                            )
                        )
                    ),
                    1.0e-12,
                )

                worst = max(
                    worst,
                    numerator
                    / denominator,
                )

    return worst


def laue_relative_residual(
    model: Model,
    arrays: dict[str, np.ndarray],
) -> float:
    """Return maximum normalized Laue residual."""

    v = model.geometry.volumes

    e_total = float(
        np.sum(
            v
            * arrays[
                "e_total"
            ]
        )
    )

    radial = float(
        np.sum(
            v
            * (
                arrays[
                    "pr_total"
                ]
                + arrays[
                    "pphi_total"
                ]
            )
        )
    )

    axial = float(
        np.sum(
            v
            * arrays[
                "pz_total"
            ]
        )
    )

    return max(
        abs(
            radial
        ),
        abs(
            axial
        ),
    ) / max(
        e_total,
        1.0e-12,
    )


def point_field_from_cells(
    geometry: Geometry,
    active: np.ndarray,
    target_r: float,
    target_z: float,
    *,
    subdivision: int = 2,
    nphi: int = 72,
) -> float:
    """Direct 3D midpoint annular reconstruction of one axial field value."""

    phi = (
        2.0
        * math.pi
        * (
            np.arange(
                nphi,
                dtype=float,
            )
            + 0.5
        )
        / nphi
    )

    cosphi = np.cos(
        phi
    )

    total = 0.0

    scale = max(
        float(
            np.max(
                np.abs(
                    active
                )
            )
        ),
        1.0,
    )

    threshold = (
        scale
        * 1.0e-13
    )

    for i in range(
        geometry.nr
    ):
        r0_cell = float(
            geometry.r_edges[
                i
            ]
        )

        r1_cell = float(
            geometry.r_edges[
                i + 1
            ]
        )

        for j in range(
            geometry.nz
        ):
            s = float(
                active[
                    i,
                    j,
                ]
            )

            if abs(
                s
            ) < threshold:
                continue

            z0_cell = float(
                geometry.z_edges[
                    j
                ]
            )

            z1_cell = float(
                geometry.z_edges[
                    j + 1
                ]
            )

            r_breaks = np.linspace(
                r0_cell,
                r1_cell,
                subdivision + 1,
            )

            z_breaks = np.linspace(
                z0_cell,
                z1_cell,
                subdivision + 1,
            )

            for ir in range(
                subdivision
            ):
                ra = float(
                    r_breaks[
                        ir
                    ]
                )

                rb = float(
                    r_breaks[
                        ir + 1
                    ]
                )

                rs = (
                    0.5
                    * (
                        ra
                        + rb
                    )
                )

                annulus_area = (
                    math.pi
                    * (
                        rb
                        * rb
                        - ra
                        * ra
                    )
                )

                for iz in range(
                    subdivision
                ):
                    za = float(
                        z_breaks[
                            iz
                        ]
                    )

                    zb = float(
                        z_breaks[
                            iz + 1
                        ]
                    )

                    zs = (
                        0.5
                        * (
                            za
                            + zb
                        )
                    )

                    volume = (
                        annulus_area
                        * (
                            zb
                            - za
                        )
                    )

                    dz = (
                        zs
                        - target_z
                    )

                    d2 = (
                        rs
                        * rs
                        + target_r
                        * target_r
                        - 2.0
                        * rs
                        * target_r
                        * cosphi
                        + dz
                        * dz
                    )

                    kernel = float(
                        np.mean(
                            dz
                            / (
                                d2
                                ** 1.5
                            )
                        )
                    )

                    total += (
                        s
                        * volume
                        * kernel
                    )

    return total


def payload_surface_audit(
    model: Model,
    arrays: dict[str, np.ndarray],
) -> dict[str, Any]:
    """Independent center and finite-payload surface sign audit."""

    active = arrays[
        "active_total"
    ]

    samples = []

    center = point_field_from_cells(
        model.geometry,
        active,
        0.0,
        1.0,
    )

    samples.append(
        {
            "label": "CENTER_DIRECT",
            "acceleration": center,
        }
    )

    for radius in PAYLOAD_RADII:
        for mu in PAYLOAD_MU:
            r_target = (
                radius
                * math.sqrt(
                    max(
                        0.0,
                        1.0
                        - float(
                            mu
                        )
                        ** 2,
                    )
                )
            )

            z_target = (
                1.0
                + radius
                * float(
                    mu
                )
            )

            value = point_field_from_cells(
                model.geometry,
                active,
                r_target,
                z_target,
            )

            samples.append(
                {
                    "label": (
                        f"R{radius:.2f}"
                        f"_MU{mu:+.4f}"
                    ),
                    "acceleration": value,
                }
            )

    weakest = min(
        samples,
        key=lambda row: row[
            "acceleration"
        ],
    )

    return {
        "all_outward": all(
            row[
                "acceleration"
            ]
            > 0.0
            for row in samples
        ),
        "minimum_acceleration": float(
            weakest[
                "acceleration"
            ]
        ),
        "minimum_location": weakest[
            "label"
        ],
        "center_direct": float(
            center
        ),
        "samples": samples,
    }


def product_dec_violation(
    product: ProductiveSource,
) -> float:
    """Audit the fixed productive source DEC."""

    return dec_violation(
        product.e_cell,
        product.pr_cell,
        product.pz_cell,
        product.trz_cell,
        product.pphi_cell,
    )


def topology_anatomy(
    model: Model,
    arrays: dict[str, np.ndarray],
) -> dict[str, float]:
    """Summarize support load-path anatomy."""

    v = model.geometry.volumes

    e_sup = arrays[
        "e_sup"
    ]

    sup_mass = float(
        np.sum(
            v
            * e_sup
        )
    )

    support_active = (
        arrays[
            "e_sup"
        ]
        + arrays[
            "pr_sup"
        ]
        + arrays[
            "pz_sup"
        ]
        + arrays[
            "pphi_sup"
        ]
    )

    support_force = float(
        np.sum(
            model.geometry.kernels
            * support_active
        )
    )

    total_active = arrays[
        "active_total"
    ]

    negative_energy = float(
        np.sum(
            v[
                total_active
                < 0.0
            ]
            * arrays[
                "e_total"
            ][
                total_active
                < 0.0
            ]
        )
    )

    total_energy = float(
        np.sum(
            v
            * arrays[
                "e_total"
            ]
        )
    )

    R, _Z = np.meshgrid(
        model.geometry.r_centers,
        model.geometry.z_centers,
        indexing="ij",
    )

    radial_threshold = (
        2.0
        * float(
            model.product.metadata[
                "front_radius"
            ]
        )
    )

    broad_energy = float(
        np.sum(
            v[
                R
                >= radial_threshold
            ]
            * e_sup[
                R
                >= radial_threshold
            ]
        )
    )

    load_reference = (
        float(
            SOURCE_META[
                "D_high"
            ]
        )
        * float(
            SOURCE_META[
                "separation"
            ]
        )
        / float(
            SOURCE_META[
                "radius"
            ]
        )
    )

    g_eff = (
        sup_mass
        / load_reference
        if load_reference
        > 0.0
        else math.nan
    )

    return {
        "support_energy": sup_mass,
        "support_active_force": support_force,
        "negative_active_energy_fraction": (
            negative_energy
            / total_energy
        ),
        "support_broad_radial_energy_fraction": (
            broad_energy
            / sup_mass
            if sup_mass
            > 0.0
            else 0.0
        ),
        "integrated_abs_pr_over_Esup": (
            float(
                np.sum(
                    v
                    * np.abs(
                        arrays[
                            "pr_sup"
                        ]
                    )
                )
            )
            / max(
                sup_mass,
                1.0e-12,
            )
        ),
        "integrated_abs_pz_over_Esup": (
            float(
                np.sum(
                    v
                    * np.abs(
                        arrays[
                            "pz_sup"
                        ]
                    )
                )
            )
            / max(
                sup_mass,
                1.0e-12,
            )
        ),
        "integrated_abs_pphi_over_Esup": (
            float(
                np.sum(
                    v
                    * np.abs(
                        arrays[
                            "pphi_sup"
                        ]
                    )
                )
            )
            / max(
                sup_mass,
                1.0e-12,
            )
        ),
        "integrated_abs_trz_over_Esup": (
            float(
                np.sum(
                    v
                    * np.abs(
                        arrays[
                            "trz_sup"
                        ]
                    )
                )
            )
            / max(
                sup_mass,
                1.0e-12,
            )
        ),
        "g_eff_energy_proxy": g_eff,
    }


def evaluate_solution(
    model: Model,
    status: str,
    solver: str,
    *,
    mode: str,
    budget_factor: float | None,
    selection_role: str,
) -> dict[str, Any]:
    """Post-check one solved convex source."""

    base = {
        "mode": mode,
        "budget_factor": budget_factor,
        "selection_role": selection_role,
        "status": status,
        "solver": solver,
        "nr": model.geometry.nr,
        "nz": model.geometry.nz,
        "rmax": model.geometry.rmax,
        "zmin": model.geometry.zmin,
        "link_model": model.link_model,
    }

    if status not in (
        cp.OPTIMAL,
        cp.OPTIMAL_INACCURATE,
        "optimal",
        "optimal_inaccurate",
    ):
        return {
            **base,
            "feasible": False,
            "green_numerics": False,
            "C_center": math.nan,
            "C_robust": math.nan,
        }

    arrays = extract_arrays(
        model
    )

    g = model.geometry
    p = model.product

    support_mass = float(
        np.sum(
            g.volumes
            * arrays[
                "e_sup"
            ]
        )
    )

    total_mass = (
        p.product_total_energy
        + support_mass
    )

    acceleration_center = float(
        np.sum(
            g.kernels
            * arrays[
                "active_total"
            ]
        )
    )

    product_accel = float(
        np.sum(
            g.kernels
            * p.active_cell
        )
    )

    product_c = (
        p.product_total_energy
        / product_accel
        if product_accel
        > 0.0
        else math.inf
    )

    support_dec = dec_violation(
        arrays[
            "e_sup"
        ],
        arrays[
            "pr_sup"
        ],
        arrays[
            "pz_sup"
        ],
        arrays[
            "trz_sup"
        ],
        arrays[
            "pphi_sup"
        ],
    )

    total_dec = dec_violation(
        arrays[
            "e_total"
        ],
        arrays[
            "pr_total"
        ],
        arrays[
            "pz_total"
        ],
        arrays[
            "trz_sup"
        ],
        arrays[
            "pphi_total"
        ],
    )

    cons = conservation_relative_residual(
        model,
        arrays,
    )

    laue = laue_relative_residual(
        model,
        arrays,
    )

    surface = payload_surface_audit(
        model,
        arrays,
    )

    weakest = float(
        surface[
            "minimum_acceleration"
        ]
    )

    c_center = (
        total_mass
        / acceleration_center
        if acceleration_center
        > 0.0
        else math.inf
    )

    c_robust = (
        total_mass
        / weakest
        if weakest
        > 0.0
        else math.inf
    )

    anatomy = topology_anatomy(
        model,
        arrays,
    )

    numerical_green = bool(
        support_dec
        <= DEC_TOL
        and total_dec
        <= DEC_TOL
        and cons
        <= CONS_TOL
        and laue
        <= LAUE_TOL
    )

    result = {
        **base,
        "feasible": True,
        "green_numerics": numerical_green,
        "product_total_energy": p.product_total_energy,
        "product_total_active": p.product_total_active,
        "product_DEC_violation": product_dec_violation(
            p
        ),
        "product_only_acceleration": product_accel,
        "product_only_C": product_c,
        "support_energy": support_mass,
        "total_energy": total_mass,
        "acceleration_center_COM": acceleration_center,
        "surface_center_direct": surface[
            "center_direct"
        ],
        "surface_minimum_acceleration": weakest,
        "surface_minimum_location": surface[
            "minimum_location"
        ],
        "all_payload_samples_outward": surface[
            "all_outward"
        ],
        "C_center": c_center,
        "C_robust": c_robust,
        "support_DEC_violation": support_dec,
        "total_DEC_violation": total_dec,
        "conservation_relative_residual": cons,
        "laue_relative_residual": laue,
        "anatomy": anatomy,
        "arrays": arrays,
        "surface_samples": surface[
            "samples"
        ],
        "product_metadata": p.metadata,
    }

    return result


def minimum_support_solution(
    model: Model,
    *,
    selection_role: str,
) -> dict[str, Any]:
    """Find the least-positive-energy DEC support needed for closure."""

    problem = cp.Problem(
        cp.Minimize(
            model.support_mass
        ),
        model.constraints,
    )

    status, solver = solve_problem(
        problem
    )

    return evaluate_solution(
        model,
        status,
        solver,
        mode="MIN_SUPPORT",
        budget_factor=None,
        selection_role=selection_role,
    )


def maximum_force_solution(
    model: Model,
    support_budget: float,
    *,
    budget_factor: float,
    selection_role: str,
) -> dict[str, Any]:
    """Maximize outward payload response at a fixed support energy budget."""

    constraints = list(
        model.constraints
    )

    constraints.append(
        model.support_mass
        <= support_budget
        * (
            1.0
            + 2.0e-7
        )
    )

    problem = cp.Problem(
        cp.Maximize(
            model.acceleration
        ),
        constraints,
    )

    status, solver = solve_problem(
        problem
    )

    return evaluate_solution(
        model,
        status,
        solver,
        mode="MAX_FORCE_AT_SUPPORT_BUDGET",
        budget_factor=budget_factor,
        selection_role=selection_role,
    )


def clean_result(
    row: dict[str, Any] | None,
) -> dict[str, Any] | None:
    """Remove large arrays from a result before JSON serialization."""

    if row is None:
        return None

    out = {}

    for key, value in row.items():
        if key in (
            "arrays",
            "surface_samples",
        ):
            continue

        out[
            key
        ] = value

    return out


def quality_score(
    row: dict[str, Any],
) -> tuple[int, float, float]:
    """Rank low-resolution architecture candidates."""

    if not row.get(
        "feasible",
        False,
    ):
        return (
            3,
            math.inf,
            math.inf,
        )

    if (
        row.get(
            "green_numerics",
            False,
        )
        and row.get(
            "all_payload_samples_outward",
            False,
        )
        and math.isfinite(
            float(
                row.get(
                    "C_robust",
                    math.inf,
                )
            )
        )
    ):
        return (
            0,
            float(
                row[
                    "C_robust"
                ]
            ),
            float(
                row[
                    "support_energy"
                ]
            ),
        )

    if row.get(
        "green_numerics",
        False,
    ):
        return (
            1,
            float(
                row.get(
                    "support_energy",
                    math.inf,
                )
            ),
            math.inf,
        )

    return (
        2,
        float(
            row.get(
                "support_energy",
                math.inf,
            )
        ),
        math.inf,
    )


def print_row(
    prefix: str,
    row: dict[str, Any] | None,
) -> None:
    """Print the compact scientific state of one row."""

    if row is None:
        print(
            f"{prefix}=NONE",
            flush=True,
        )
        return

    if not row.get(
        "feasible",
        False,
    ):
        print(
            (
                f"{prefix}=INFEASIBLE "
                f"STATUS={row.get('status')}"
            ),
            flush=True,
        )
        return

    print(
        (
            f"{prefix} "
            f"C_ROBUST={row['C_robust']:.12e} "
            f"C_CENTER={row['C_center']:.12e} "
            f"E_SUPPORT={row['support_energy']:.12e} "
            f"E_TOTAL={row['total_energy']:.12e} "
            f"A_MIN={row['surface_minimum_acceleration']:.12e} "
            f"OUTWARD={row['all_payload_samples_outward']} "
            f"DEC_TOTAL={row['total_DEC_violation']:.3e} "
            f"CONS={row['conservation_relative_residual']:.3e} "
            f"LAUE={row['laue_relative_residual']:.3e} "
            f"G_EFF={row['anatomy']['g_eff_energy_proxy']:.6e} "
            f"LINK={row['link_model']} "
            f"RMAX={row['rmax']:.6f} "
            f"GRID={row['nr']}x{row['nz']}"
        ),
        flush=True,
    )


z_comp_center = (
    1.0
    - float(
        SOURCE_META[
            "d_comp"
        ]
    )
)

zmin_full = min(
    -4.5,
    z_comp_center
    - 0.75,
)


if SMOKE:
    radial_envelopes = (
        2.5,
    )

    low_nr = 8
    low_nz = 18

else:
    radial_envelopes = (
        1.5,
        2.5,
        3.5,
        5.0,
    )

    low_nr = 10
    low_nz = 26


print(
    "=== 027D PRODUCTIVE SOURCE LEDGER ===",
    flush=True,
)

for key in sorted(
    LEDGER
):
    print(
        f"{key}={LEDGER[key]:.15e}",
        flush=True,
    )

print(
    f"W_HIGH={W_HIGH:.15e}",
    flush=True,
)

print(
    f"W_REAR={W_REAR:.15e}",
    flush=True,
)

print(
    f"W_COMP={W_COMP:.15e}",
    flush=True,
)

print(
    (
        "027C_CONSERVATIVE_ZERO_COST_REFERENCE_C="
        f"{float(SOURCE_ROW['C_payload']):.15e}"
    ),
    flush=True,
)

print(
    (
        "027C_REQUIRED_G_PATH_BEATING_006D="
        f"{G_PATH_027C_ROBUST:.15e}"
    ),
    flush=True,
)


low_rows: list[dict[str, Any]] = []


print(
    "\n=== 027D STAGE 1 — LOW-RESOLUTION TOPOLOGY SCAN ===",
    flush=True,
)


for rmax in radial_envelopes:
    for link_model in (
        "ISOTROPIC_LINK",
        "AXIAL_LINK",
    ):
        print(
            (
                "027D_LOW_BEGIN "
                f"RMAX={rmax:.6f} "
                f"LINK={link_model}"
            ),
            flush=True,
        )

        geometry = build_geometry(
            low_nr,
            low_nz,
            rmax,
            zmin_full,
        )

        model = build_model(
            geometry,
            link_model,
        )

        row = minimum_support_solution(
            model,
            selection_role=(
                "PHYSICAL_PREFILTER"
            ),
        )

        low_rows.append(
            row
        )

        print_row(
            "027D_LOW_RESULT",
            row,
        )


low_ranked = sorted(
    low_rows,
    key=quality_score,
)


if not low_ranked:
    raise RuntimeError(
        "027D produced no topology rows"
    )


selected_low = low_ranked[
    0
]


print(
    "\n=== 027D LOW-RESOLUTION WINNER ===",
    flush=True,
)

print_row(
    "027D_SELECTED_LOW",
    selected_low,
)


if SMOKE:
    summary = {
        "simulation": "027D",
        "branch": "TRUE_ANTIGRAVITY",
        "smoke_only": True,
        "selected_low": clean_result(
            selected_low
        ),
        "decision": "SMOKE_ONLY",
        "claims": {
            "practical_antigravity_device": False,
        },
    }

    with OUT_JSON.open(
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            summary,
            f,
            indent=2,
            sort_keys=True,
        )

    print(
        "027D_SMOKE_ONLY=YES",
        flush=True,
    )

    print(
        "027D_RUN_COMPLETE=YES",
        flush=True,
    )

    raise SystemExit(
        0
    )


selected_rmax = float(
    selected_low[
        "rmax"
    ]
)

selected_link = str(
    selected_low[
        "link_model"
    ]
)


print(
    "\n=== 027D STAGE 2 — PRIMARY GRID ===",
    flush=True,
)


primary_geometry = build_geometry(
    14,
    34,
    selected_rmax,
    zmin_full,
)

primary_model = build_model(
    primary_geometry,
    selected_link,
)

primary_min = minimum_support_solution(
    primary_model,
    selection_role="PHYSICAL_MINIMUM_CLOSURE",
)

print_row(
    "027D_PRIMARY_MIN",
    primary_min,
)


physical_rows: list[dict[str, Any]] = []
wildcard_rows: list[dict[str, Any]] = []


if primary_min.get(
    "feasible",
    False,
):
    minimum_energy = float(
        primary_min[
            "support_energy"
        ]
    )

    for factor in PHYSICAL_BUDGET_FACTORS:
        print(
            (
                "027D_PRIMARY_BUDGET_BEGIN "
                f"FACTOR={factor:.6f}"
            ),
            flush=True,
        )

        budget = (
            minimum_energy
            * factor
        )

        row = maximum_force_solution(
            primary_model,
            budget,
            budget_factor=factor,
            selection_role="PHYSICAL_BUDGET_SCAN",
        )

        physical_rows.append(
            row
        )

        print_row(
            "027D_PRIMARY_BUDGET_RESULT",
            row,
        )

    for factor in BLIND_BUDGET_FACTORS:
        print(
            (
                "027D_BLIND_WILDCARD_BEGIN "
                f"FACTOR={factor:.6f}"
            ),
            flush=True,
        )

        budget = (
            minimum_energy
            * factor
        )

        row = maximum_force_solution(
            primary_model,
            budget,
            budget_factor=factor,
            selection_role=(
                "BLIND_NON_EVIDENTIARY_EXCLUDED"
            ),
        )

        wildcard_rows.append(
            row
        )

        print_row(
            "027D_BLIND_WILDCARD_RESULT",
            row,
        )


physical_valid = [
    row
    for row in physical_rows
    if (
        row.get(
            "feasible",
            False,
        )
        and row.get(
            "green_numerics",
            False,
        )
        and row.get(
            "all_payload_samples_outward",
            False,
        )
        and math.isfinite(
            float(
                row.get(
                    "C_robust",
                    math.inf,
                )
            )
        )
    )
]


if physical_valid:
    primary_best = min(
        physical_valid,
        key=lambda row: float(
            row[
                "C_robust"
            ]
        ),
    )

elif (
    primary_min.get(
        "feasible",
        False,
    )
    and primary_min.get(
        "green_numerics",
        False,
    )
):
    primary_best = primary_min

else:
    primary_best = None


print(
    "\n=== 027D PRIMARY BEST ===",
    flush=True,
)

print_row(
    "027D_PRIMARY_BEST",
    primary_best,
)


print(
    "\n=== 027D STAGE 3 — HIGH-RESOLUTION INDEPENDENT REFINEMENT ===",
    flush=True,
)


high_geometry = build_geometry(
    18,
    44,
    selected_rmax,
    zmin_full,
)

high_model = build_model(
    high_geometry,
    selected_link,
)

high_min = minimum_support_solution(
    high_model,
    selection_role="PHYSICAL_HIGH_MINIMUM_CLOSURE",
)

print_row(
    "027D_HIGH_MIN",
    high_min,
)


high_best = None
selected_factor = None


if (
    primary_best is not None
    and primary_best.get(
        "budget_factor"
    )
    is not None
    and high_min.get(
        "feasible",
        False,
    )
):
    selected_factor = float(
        primary_best[
            "budget_factor"
        ]
    )

    high_budget = (
        float(
            high_min[
                "support_energy"
            ]
        )
        * selected_factor
    )

    high_best = maximum_force_solution(
        high_model,
        high_budget,
        budget_factor=selected_factor,
        selection_role="PHYSICAL_HIGH_RECONSTRUCTION",
    )

    print_row(
        "027D_HIGH_MATCHED_BUDGET",
        high_best,
    )

elif (
    high_min.get(
        "feasible",
        False,
    )
):
    high_best = high_min


c_rel_diff = math.inf


if (
    primary_best is not None
    and high_best is not None
    and primary_best.get(
        "feasible",
        False,
    )
    and high_best.get(
        "feasible",
        False,
    )
    and math.isfinite(
        float(
            primary_best.get(
                "C_robust",
                math.inf,
            )
        )
    )
    and math.isfinite(
        float(
            high_best.get(
                "C_robust",
                math.inf,
            )
        )
    )
):
    cpv = float(
        primary_best[
            "C_robust"
        ]
    )

    chv = float(
        high_best[
            "C_robust"
        ]
    )

    c_rel_diff = (
        abs(
            cpv
            - chv
        )
        / max(
            abs(
                cpv
            ),
            abs(
                chv
            ),
            1.0e-12,
        )
    )


high_green = bool(
    high_best is not None
    and high_best.get(
        "feasible",
        False,
    )
    and high_best.get(
        "green_numerics",
        False,
    )
    and high_best.get(
        "all_payload_samples_outward",
        False,
    )
)


primary_green = bool(
    primary_best is not None
    and primary_best.get(
        "feasible",
        False,
    )
    and primary_best.get(
        "green_numerics",
        False,
    )
    and primary_best.get(
        "all_payload_samples_outward",
        False,
    )
)


converged = bool(
    primary_green
    and high_green
    and c_rel_diff
    <= CONVERGENCE_TOL
)


conservative_c = math.inf


if converged:
    conservative_c = max(
        float(
            primary_best[
                "C_robust"
            ]
        ),
        float(
            high_best[
                "C_robust"
            ]
        ),
    )


if (
    converged
    and conservative_c
    < C_024D
):
    decision = (
        "MAJOR_GREEN_EXACT_SELF_CLOSING_DEC_STRESS_"
        "BEATS_024D"
    )

    next_step = (
        "AUTHORIZE_MICROSCOPIC_FIELD_REALIZATION_"
        "OF_027D_STRESS_ANATOMY"
    )

    source_80 = True

elif (
    converged
    and conservative_c
    < C_006D
):
    decision = (
        "GREEN_EXACT_SELF_CLOSING_DEC_STRESS_"
        "BEATS_006D"
    )

    next_step = (
        "EXTRACT_STRESS_FUNCTION_AND_BUILD_"
        "MINIMAL_MICROSCOPIC_FIELD_REALIZATION"
    )

    source_80 = False

elif (
    high_green
    or primary_green
):
    decision = (
        "YELLOW_EXACT_SELF_CLOSING_SOURCE_EXISTS_"
        "BUT_DOES_NOT_BEAT_006D"
    )

    next_step = (
        "DIAGNOSE_PRODUCTIVE_SUPPORT_KERNEL_ANATOMY_"
        "BEFORE_FIELD_REALIZATION"
    )

    source_80 = False

else:
    decision = (
        "RED_NO_OUTWARD_EXACT_SELF_CLOSING_DEC_SOURCE_"
        "IN_TESTED_ENVELOPES"
    )

    next_step = (
        "CLOSE_027B_027C_SHUTTLE_CLOSURE_CLASS_"
        "AND_RERANK_SOURCE_ENGINE"
    )

    source_80 = False


best_arrays_row = None


if high_best is not None and high_best.get(
    "feasible",
    False,
):
    best_arrays_row = high_best

elif primary_best is not None and primary_best.get(
    "feasible",
    False,
):
    best_arrays_row = primary_best

elif primary_min.get(
    "feasible",
    False,
):
    best_arrays_row = primary_min


if best_arrays_row is not None:
    arrays = best_arrays_row[
        "arrays"
    ]

    geometry = (
        high_model.geometry
        if best_arrays_row is high_best
        else primary_model.geometry
    )

    product = (
        high_model.product
        if best_arrays_row is high_best
        else primary_model.product
    )

    np.savez_compressed(
        OUT_NPZ,
        r_edges=geometry.r_edges,
        z_edges=geometry.z_edges,
        r_centers=geometry.r_centers,
        z_centers=geometry.z_centers,
        volumes=geometry.volumes,
        kernels=geometry.kernels,
        e_product=product.e_cell,
        pr_product=product.pr_cell,
        pz_product=product.pz_cell,
        pphi_product=product.pphi_cell,
        active_product=product.active_cell,
        e_support=arrays[
            "e_sup"
        ],
        pr_support=arrays[
            "pr_sup"
        ],
        pz_support=arrays[
            "pz_sup"
        ],
        pphi_support=arrays[
            "pphi_sup"
        ],
        trz_support=arrays[
            "trz_sup"
        ],
        e_total=arrays[
            "e_total"
        ],
        pr_total=arrays[
            "pr_total"
        ],
        pz_total=arrays[
            "pz_total"
        ],
        pphi_total=arrays[
            "pphi_total"
        ],
        active_total=arrays[
            "active_total"
        ],
    )


rows_for_csv = (
    low_rows
    + [
        primary_min
    ]
    + physical_rows
    + wildcard_rows
    + [
        high_min
    ]
)

if high_best is not None:
    rows_for_csv.append(
        high_best
    )


csv_fields = [
    "selection_role",
    "mode",
    "budget_factor",
    "status",
    "solver",
    "nr",
    "nz",
    "rmax",
    "zmin",
    "link_model",
    "feasible",
    "green_numerics",
    "product_only_C",
    "support_energy",
    "total_energy",
    "acceleration_center_COM",
    "surface_minimum_acceleration",
    "surface_minimum_location",
    "all_payload_samples_outward",
    "C_center",
    "C_robust",
    "support_DEC_violation",
    "total_DEC_violation",
    "conservation_relative_residual",
    "laue_relative_residual",
    "g_eff_energy_proxy",
]


with OUT_CSV.open(
    "w",
    newline="",
    encoding="utf-8",
) as f:
    writer = csv.DictWriter(
        f,
        fieldnames=csv_fields,
    )

    writer.writeheader()

    for row in rows_for_csv:
        if row is None:
            continue

        anatomy = row.get(
            "anatomy",
            {},
        )

        writer.writerow(
            {
                "selection_role": row.get(
                    "selection_role"
                ),
                "mode": row.get(
                    "mode"
                ),
                "budget_factor": row.get(
                    "budget_factor"
                ),
                "status": row.get(
                    "status"
                ),
                "solver": row.get(
                    "solver"
                ),
                "nr": row.get(
                    "nr"
                ),
                "nz": row.get(
                    "nz"
                ),
                "rmax": row.get(
                    "rmax"
                ),
                "zmin": row.get(
                    "zmin"
                ),
                "link_model": row.get(
                    "link_model"
                ),
                "feasible": row.get(
                    "feasible"
                ),
                "green_numerics": row.get(
                    "green_numerics"
                ),
                "product_only_C": row.get(
                    "product_only_C"
                ),
                "support_energy": row.get(
                    "support_energy"
                ),
                "total_energy": row.get(
                    "total_energy"
                ),
                "acceleration_center_COM": row.get(
                    "acceleration_center_COM"
                ),
                "surface_minimum_acceleration": row.get(
                    "surface_minimum_acceleration"
                ),
                "surface_minimum_location": row.get(
                    "surface_minimum_location"
                ),
                "all_payload_samples_outward": row.get(
                    "all_payload_samples_outward"
                ),
                "C_center": row.get(
                    "C_center"
                ),
                "C_robust": row.get(
                    "C_robust"
                ),
                "support_DEC_violation": row.get(
                    "support_DEC_violation"
                ),
                "total_DEC_violation": row.get(
                    "total_DEC_violation"
                ),
                "conservation_relative_residual": row.get(
                    "conservation_relative_residual"
                ),
                "laue_relative_residual": row.get(
                    "laue_relative_residual"
                ),
                "g_eff_energy_proxy": anatomy.get(
                    "g_eff_energy_proxy"
                ),
            }
        )


with OUT_WILDCARD.open(
    "w",
    newline="",
    encoding="utf-8",
) as f:
    fields = [
        "budget_factor",
        "feasible",
        "C_robust",
        "all_payload_samples_outward",
        "selection_role",
    ]

    writer = csv.DictWriter(
        f,
        fieldnames=fields,
    )

    writer.writeheader()

    for row in wildcard_rows:
        writer.writerow(
            {
                "budget_factor": row.get(
                    "budget_factor"
                ),
                "feasible": row.get(
                    "feasible"
                ),
                "C_robust": row.get(
                    "C_robust"
                ),
                "all_payload_samples_outward": row.get(
                    "all_payload_samples_outward"
                ),
                "selection_role": (
                    "BLIND_NON_EVIDENTIARY_EXCLUDED"
                ),
            }
        )


summary = {
    "branch": "TRUE_ANTIGRAVITY",
    "simulation": "027D",
    "question": (
        "Can an exact finite-volume positive-energy DEC support tensor "
        "self-close the corrected 027C productive source while retaining "
        "true-stand-off outward finite-payload gravity?"
    ),
    "lineage": {
        "027c_decision": J027C.get(
            "decision"
        ),
        "027c_robust_g_path_max_006D": (
            G_PATH_027C_ROBUST
        ),
        "027c_selected_zero_cost_C": float(
            SOURCE_ROW[
                "C_payload"
            ]
        ),
        "C_006D": C_006D,
        "C_024D": C_024D,
    },
    "productive_ledger": LEDGER,
    "productive_pressure_ratios": {
        "W_HIGH": W_HIGH,
        "W_REAR": W_REAR,
        "W_COMP": W_COMP,
    },
    "selected_architecture": {
        "rmax": selected_rmax,
        "link_model": selected_link,
        "zmin": zmin_full,
    },
    "low_scan": [
        clean_result(
            row
        )
        for row in low_rows
    ],
    "primary_minimum": clean_result(
        primary_min
    ),
    "primary_physical_budget_scan": [
        clean_result(
            row
        )
        for row in physical_rows
    ],
    "primary_best": clean_result(
        primary_best
    ),
    "high_minimum": clean_result(
        high_min
    ),
    "high_best": clean_result(
        high_best
    ),
    "convergence": {
        "primary_high_C_robust_relative_difference": (
            c_rel_diff
            if math.isfinite(
                c_rel_diff
            )
            else None
        ),
        "criterion": CONVERGENCE_TOL,
        "pass": converged,
        "conservative_C_robust": (
            conservative_c
            if math.isfinite(
                conservative_c
            )
            else None
        ),
    },
    "decision": decision,
    "next": next_step,
    "source_engine_80_heuristic_authorized": source_80,
    "overall_practical_antigravity_80_heuristic_authorized": False,
    "mandatory_parallel_credibility_branch": (
        "026C_N89_FORCE_CONVERGENCE"
    ),
    "claims": {
        "exact_discrete_local_spatial_conservation": (
            bool(
                primary_green
                or high_green
            )
        ),
        "positive_energy_support": True,
        "support_DEC_imposed": True,
        "total_DEC_imposed": True,
        "microscopic_field_realization": False,
        "full_dynamic_Tmunu_conservation": False,
        "reaction_momentum_closed": False,
        "radiation_lifetime_closed": False,
        "full_stability": False,
        "nonlinear_GR": False,
        "removes_1_over_G_scaling": False,
        "practical_antigravity_device": False,
    },
}


with OUT_JSON.open(
    "w",
    encoding="utf-8",
) as f:
    json.dump(
        summary,
        f,
        indent=2,
        sort_keys=True,
    )


print(
    "\n=== 027D FINAL RESULT ===",
    flush=True,
)

print(
    f"SELECTED_RMAX={selected_rmax:.15e}",
    flush=True,
)

print(
    f"SELECTED_LINK_MODEL={selected_link}",
    flush=True,
)

print_row(
    "PRIMARY_BEST",
    primary_best,
)

print_row(
    "HIGH_BEST",
    high_best,
)

print(
    (
        "PRIMARY_HIGH_C_ROBUST_REL_DIFF="
        + (
            f"{c_rel_diff:.15e}"
            if math.isfinite(
                c_rel_diff
            )
            else "NONE"
        )
    ),
    flush=True,
)

print(
    (
        "CONSERVATIVE_C_ROBUST="
        + (
            f"{conservative_c:.15e}"
            if math.isfinite(
                conservative_c
            )
            else "NONE"
        )
    ),
    flush=True,
)

print(
    f"027D_DECISION={decision}",
    flush=True,
)

print(
    f"NEXT={next_step}",
    flush=True,
)

print(
    (
        "SOURCE_ENGINE_80_HEURISTIC_AUTHORIZED="
        + (
            "YES"
            if source_80
            else "NO"
        )
    ),
    flush=True,
)

print(
    "OVERALL_PRACTICAL_ANTIGRAVITY_80_HEURISTIC_AUTHORIZED=NO",
    flush=True,
)

print(
    "MICROSCOPIC_FIELD_REALIZATION=NO",
    flush=True,
)

print(
    "FULL_DYNAMIC_TMUNU_CONSERVATION=NO",
    flush=True,
)

print(
    "REMOVES_1_OVER_G_SCALING=NO",
    flush=True,
)

print(
    "PRACTICAL_ANTIGRAVITY_DEVICE=NO",
    flush=True,
)

print(
    "026C_N89_STILL_REQUIRED=YES",
    flush=True,
)

print(
    f"SUMMARY_JSON={OUT_JSON}",
    flush=True,
)

print(
    f"CASES_CSV={OUT_CSV}",
    flush=True,
)

print(
    f"WILDCARD_CSV={OUT_WILDCARD}",
    flush=True,
)

if OUT_NPZ.exists():
    print(
        f"BEST_SOURCE_NPZ={OUT_NPZ}",
        flush=True,
    )

print(
    "027D_RUN_COMPLETE=YES",
    flush=True,
)
