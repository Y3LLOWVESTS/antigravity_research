#!/usr/bin/env python3
"""024C1 — intuitive guarded stress-sandwich source gate.

PURPOSE
-------
Test a deliberately understandable static source architecture rather than
allowing a general 2-D optimizer to invent an opaque stress field.

The architecture contains three physically interpretable connected pieces:

    1. PAYLOAD-FACING WORKING FACE

       A finite upper disk close to the payload.

       Intended role:
           concentrated tensile / negative-active source producing useful
           outward gravity.

    2. OUTER GUARD / RETURN WALL

       A cylindrical annulus joining the front face to a deeper backplane.

       Intended role:
           transmit the stresses required by local conservation away from the
           highest gravitational kernel.

    3. BURIED BACKPLANE

       A broader lower disk.

       Intended role:
           carry compensating structural stress at larger payload distance.

This is the static gravitational analogue of a mechanically guarded sandwich.

It is NOT a material proposal.

It is NOT a microscopic field theory.

It is a constrained stress-energy architecture designed to determine whether
the durable Introspective mechanism lessons can be expressed in a simple,
recognizable geometry.

SCIENTIFIC QUESTION
-------------------
Can a source made from an intuitive front-face / side-return / buried-backplane
geometry:

    - remain positive-energy;
    - satisfy type-I DEC;
    - satisfy local static conservation;
    - have positive total far-field active mass;
    - generate outward gravity throughout a finite working plane;
    - suppress transverse acceleration;
    - reduce cancellation relative to 024C;
    - and beat 006D in acceleration per total source energy?

WHY THIS FOLLOWS 024C
---------------------
024C established several useful facts.

1. Full r-z stress routing is viable.

2. Burying compensating stress improved the coarse coefficient by about 8%.

3. Roughly 90% of useful gross response was concentrated in about 21.6% of
   the energy.

4. The productive region remained close to the payload-facing surface.

5. The architecture nevertheless had cancellation approximately 3.43.

6. The r=0.5h working plane had axial flatness approximately 12%, but
   transverse acceleration reached approximately 57% of axial acceleration.

7. Its conservative coefficient was approximately 38.32, worse than

       C_006D = 23.591586299249.

The next experiment therefore constrains the *architecture*, not merely the
objective.

INTUITIVE MECHANISM
-------------------
The intended stress flow is:

    TOP WORKING FACE
            |
            v
       OUTER GUARD
            |
            v
     BURIED BACKPLANE.

The hypothesis is that the high-leverage source can do useful work near z=0
while the mandatory stress return is exported both:

    radially outward

and

    vertically downward.

The general conservation law in cylindrical coordinates is retained:

    (1/r) d(r p_r)/dr
    +
    d(T_rz)/dz
    -
    p_phi/r
    =
    0,

and

    (1/r) d(r T_rz)/dr
    +
    d(p_z)/dz
    =
    0.

STRESS-ENERGY MODEL
-------------------
Variables are the same audited staggered finite-volume quantities used in the
Introspective conserved-source program:

    e(r,z)          >= 0
    p_phi(r,z)
    p_r             on radial faces
    p_z             on vertical faces
    T_rz            on vertices.

The active gravitoelectric source is:

    S
      =
    e + p_r + p_z + p_phi.

TYPE-I DOMINANT ENERGY CONDITION
--------------------------------
At every cell, the principal stresses of:

    [[p_r, T_rz, 0],
     [T_rz, p_z, 0],
     [0, 0, p_phi]]

must satisfy:

    |lambda_i| <= e.

The r-z eigenvalue bound is imposed as an exact second-order-cone constraint.

LOCAL CONSERVATION
------------------
Every active finite-volume cell obeys exact integrated radial and vertical
force balance.

The outer boundary of the full three-piece source is traction-free.

No external mechanical support is omitted.

VON LAUE / GLOBAL BALANCE
-------------------------
The static compact source additionally enforces:

    integral (p_r+p_phi) dV = 0

and

    integral p_z dV = 0.

Therefore:

    integral tr(T) dV = 0

and consequently:

    integral S dV
      =
    integral e dV
      >
    0.

The far field remains attractive / positive-active-mass even when the local
near field points outward.

WORKING-PLANE TARGET
--------------------
Use:

    payload plane:
        z/h = 1

    aperture:
        0 <= r/h <= 0.5.

Five explicit radial sentinels are optimized simultaneously:

    r/h =
        0
        0.125
        0.25
        0.375
        0.5.

Two optimization modes are solved for each physical architecture.

POINT MODE
----------
Require only:

    a_z(r=0) >= 1.

This measures the intrinsic source efficiency without requiring a broad field.

PLANAR MODE
-----------
Require at every sentinel:

    1.0 <= a_z <= 1.10

and:

    |a_r| <= 0.15.

Because a_z >= 1, this guarantees approximately:

    |a_r/a_z| <= 15%.

This is a substantially stronger planarity requirement than merely checking
the result after optimization.

The ratio:

    C_planar / C_point

is the explicit energetic price of gravitational field shaping.

A perfect finite static gravitational beam is not claimed.

The source-free potential remains harmonic.

GUIDED ROLE CHECK
-----------------
After selecting the best physical geometry, solve one additional version that
encodes the intuitive role assignment at the integrated level.

Require:

    top active source
        <=
    -0.25 * top energy,

and:

    backplane active source >= 0.

This asks whether the intended:

    productive tensile front
        +
    positive deeper compensation

can actually coexist with conservation and DEC.

This guided result is diagnostic.

It does not supersede the unrestricted optimum unless it independently passes
all gates.

GEOMETRY
--------
The active source mask is the union of:

TOP:
    z >= -t_top
    r <= R_top

SIDE GUARD:
    |r-R_top| <= w_guard/2
    -D <= z <= 0

BACKPLANE:
    z <= -D+t_back
    r <= R_outer.

This produces one connected finite source.

The primary geometry scout varies only:

    top radius,
    total outer radius,
    depth.

The thicknesses remain deliberately simple.

This is not a brute-force morphology search.

PRIMARY PHYSICAL GEOMETRIES
---------------------------
Test four deliberately interpretable designs.

A:
    R_top=1.5
    R_outer=4.0
    D=1.25

B:
    R_top=2.0
    R_outer=4.0
    D=1.50

C:
    R_top=2.5
    R_outer=4.5
    D=1.50

D:
    R_top=2.5
    R_outer=5.0
    D=2.00

Common approximate dimensions:

    top thickness = 0.25 h
    guard width   = 0.50 h
    back thickness= 0.40 h.

BLIND WILDCARD DIAGNOSTICS
--------------------------
The user-requested blind values:

    0.625
    1.6
    1.875
    3.125
    5

are also tested as top-radius values in a fixed diagnostic geometry.

They are explicitly:

    BLIND_WILDCARD_NOT_PHYSICS_PRIOR.

They are not used to select the physical candidate and cannot earn promotion.

NUMERICAL STRATEGY
------------------
Scout grid:

    16 x 12.

Selected planar geometry:

    MEDIUM:
        20 x 16

    HIGH:
        24 x 20.

The highest-resolution selected solution receives an independent, higher-order
vector-kernel reconstruction.

INDEPENDENT SOLVER
------------------
The selected medium PLANAR problem is also solved with SCS.

Two results are reported separately:

    SCS_OBJECTIVE_MATCH

and

    SCS_FULL_POSTCHECK.

This prevents a bookkeeping issue in one residual from being confused with
objective disagreement.

DEC DIAGNOSTIC REPAIR
---------------------
024C reported a maximum DEC ratio above one even though its absolute DEC
violation was tiny.

That ratio was contaminated by divisions in numerically near-vacuum cells.

024C1 therefore reports:

    MAX_DEC_VIOLATION_ABSOLUTE

using all active cells, which remains the actual physics gate,

and:

    MAX_DEC_RATIO_MATERIALLY_OCCUPIED

only where:

    e >= 1e-6 * max(e).

This diagnostic ratio is not substituted for the absolute DEC test.

PROMOTION CONDITIONS
--------------------
A new source-record candidate requires:

    known-solution regression PASS

    medium/high source GREEN

    C convergence <= 15%

    minimum participation width >= 3 cells

    independent vector-force reconstruction PASS

    all planar sentinels satisfy the declared bounds

    conservative C < C_006D

    SCS objective/full check acceptable.

A weaker morphology result is still scientifically useful if:

    planar gate passes

but:

    C >= C_006D.

Then the architecture teaches us how much energy must be paid for a directed
working plane.

FALSIFIERS
----------
The intuitive stress sandwich is demoted if:

    no planar geometry is feasible;

or:

    the planar penalty is severe;

or:

    the selected planar coefficient is worse than 024C;

or:

    cancellation does not improve;

or:

    useful force is not actually concentrated in the top working face;

or:

    refinement / width / independent reconstruction fails.

STOP RULE
---------
If the intuitive source fails to improve materially on 024C and 006D:

    do not perform another free-form source optimization.

Return priority to:

    006D microscopic realization,

    the 023C field fallback,

    and Analogue Antigravity.

If it beats 006D robustly:

    stop coefficient polishing;

    identify a minimal microscopic field / material stress system capable of
    reproducing the discovered three-piece stress flow.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_INTUITIVE_GUARDED_STRESS_SANDWICH_SOURCE_PREFILTER

DOES NOT ESTABLISH
------------------
- a microscopic field realization;
- a known material;
- full dynamical stability;
- nonlinear Einstein-matter continuation;
- perfect gravitational collimation;
- favorable practical 1/G scaling;
- an experiment;
- a practical antigravity device.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
import importlib.util
import json
import math
from pathlib import Path
import sys
from typing import Any

import cvxpy as cp
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SIM_DIR = ROOT / "simulations"
DATA_DIR = ROOT / "results/data"

PRIOR_SUMMARY = (
    DATA_DIR
    / "024c_teacher_guided_planar_stress_lens_summary.json"
)

INT14B_SOURCE = (
    SIM_DIR
    / "int14b_support_constrained_structural_overhead_bridge.py"
)

C024_SOURCE = (
    SIM_DIR
    / "024c_teacher_guided_planar_stress_lens.py"
)

OUT_SUMMARY = (
    DATA_DIR
    / "024c1_intuitive_guarded_stress_sandwich_summary.json"
)

OUT_CASES = (
    DATA_DIR
    / "024c1_intuitive_guarded_stress_sandwich_cases.csv"
)

OUT_NPZ = (
    DATA_DIR
    / "024c1_intuitive_guarded_stress_sandwich_selected.npz"
)


C006D = 23.591586299249

PRIOR_024C_C = 38.32239108713473
PRIOR_024C_TRANSVERSE = 0.5740376772322424
PRIOR_024C_CANCELLATION = 3.4300573206758806

TARGET_Z = 1.0

SENTINEL_RADII = np.asarray(
    (
        0.0,
        0.125,
        0.25,
        0.375,
        0.5,
    ),
    dtype=float,
)

AXIAL_MIN = 1.0
AXIAL_MAX = 1.10
RADIAL_ABS_MAX = 0.15

DEC_TOL = 3.0e-6
CONS_TOL = 3.0e-6
TRACE_TOL = 3.0e-6
ACTIVE_TOTAL_TOL = 3.0e-6

CONSTRAINT_POST_TOL = 2.0e-4

C_CONVERGENCE_TOL = 0.15
MIN_WIDTH_CELLS = 3.0

INDEPENDENT_VECTOR_TOL = 5.0e-4
SCS_OBJECTIVE_TOL = 0.05

SCOUT_NR = 16
SCOUT_NZ = 12

MEDIUM_NR = 20
MEDIUM_NZ = 16

HIGH_NR = 24
HIGH_NZ = 20

SCOUT_KERNEL_ORDER = 4
SCOUT_NPHI = 24

INDEPENDENT_KERNEL_ORDER = 7
INDEPENDENT_NPHI = 64

BLIND_WILDCARD_VALUES = (
    0.625,
    1.6,
    1.875,
    3.125,
    5.0,
)


@dataclass(frozen=True)
class SandwichSpec:
    """One intuitive connected three-piece source geometry."""

    name: str

    top_radius: float

    outer_radius: float

    depth: float

    top_thickness: float = 0.25

    guard_width: float = 0.50

    back_thickness: float = 0.40

    category: str = "PHYSICAL"


def require(
    path: Path,
) -> None:
    """Require one upstream file."""

    if not path.is_file():
        raise RuntimeError(
            f"Required file missing: {path}"
        )


def load_module(
    name: str,
    path: Path,
):
    """Import a repository simulation without running main()."""

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

    module = importlib.util.module_from_spec(
        spec
    )

    sys.modules[
        name
    ] = module

    try:
        spec.loader.exec_module(
            module
        )
    except Exception:
        sys.modules.pop(
            name,
            None,
        )
        raise

    return module


def relerr(
    a: float,
    b: float,
) -> float:
    """Stable relative error."""

    return (
        abs(
            a - b
        )
        /
        max(
            abs(a),
            abs(b),
            1.0e-300,
        )
    )


def effective_volume(
    integrated_quantity: np.ndarray,
    volumes: np.ndarray,
) -> float:
    """Effective support volume for a nonnegative integrated quantity."""

    q = np.maximum(
        np.asarray(
            integrated_quantity,
            dtype=float,
        ),
        0.0,
    )

    v = np.asarray(
        volumes,
        dtype=float,
    )

    numerator = float(
        np.sum(
            q
        )
    ) ** 2

    denominator = float(
        np.sum(
            q
            * q
            / np.maximum(
                v,
                1.0e-300,
            )
        )
    )

    if denominator <= 0.0:
        return 0.0

    return (
        numerator
        / denominator
    )


def force_energy_fraction(
    cell_energy: np.ndarray,
    outward_force: np.ndarray,
    fraction: float,
) -> float:
    """Energy fraction needed to account for a chosen outward-force fraction."""

    e = np.maximum(
        np.asarray(
            cell_energy,
            dtype=float,
        ).ravel(),
        0.0,
    )

    f = np.maximum(
        np.asarray(
            outward_force,
            dtype=float,
        ).ravel(),
        0.0,
    )

    total_e = float(
        np.sum(
            e
        )
    )

    total_f = float(
        np.sum(
            f
        )
    )

    if (
        total_e <= 0.0
        or total_f <= 0.0
    ):
        return float(
            "nan"
        )

    leverage = np.zeros_like(
        e
    )

    good = (
        e
        >
        max(
            float(
                np.max(
                    e
                )
            ),
            1.0,
        )
        * 1.0e-15
    )

    leverage[
        good
    ] = (
        f[
            good
        ]
        /
        e[
            good
        ]
    )

    order = np.argsort(
        leverage
    )[::-1]

    cumulative = np.cumsum(
        f[
            order
        ]
    )

    index = int(
        np.searchsorted(
            cumulative,
            fraction
            * total_f,
            side="left",
        )
    )

    index = min(
        index,
        len(
            order
        )
        - 1,
    )

    chosen = order[
        : index + 1
    ]

    return float(
        np.sum(
            e[
                chosen
            ]
        )
        / total_e
    )


def make_case(
    int14b,
    spec: SandwichSpec,
    nr: int,
    nz: int,
):
    """Build the metadata object required by inherited boundary routines."""

    return int14b.SupportCase(
        name=spec.name,
        nr=nr,
        nz=nz,
        radius=spec.outer_radius,
        zmin=-spec.depth,
        zmax=0.0,
        target_z=TARGET_Z,
        payload_radius=0.043298860805059215,
        spherical_mask=False,
        reflection_symmetry=False,
        category=spec.category,
    )


def build_geometry(
    c024,
    spec: SandwichSpec,
    nr: int,
    nz: int,
    *,
    kernel_order: int,
    nphi: int,
) -> dict[str, np.ndarray]:
    """Build connected top-face / guard / backplane geometry and kernels."""

    if not (
        0.0
        <
        spec.top_radius
        <=
        spec.outer_radius
    ):
        raise RuntimeError(
            "Invalid top/outer radius."
        )

    if not (
        0.0
        <
        spec.top_thickness
        <
        spec.depth
    ):
        raise RuntimeError(
            "Invalid top thickness."
        )

    if not (
        0.0
        <
        spec.back_thickness
        <
        spec.depth
    ):
        raise RuntimeError(
            "Invalid back thickness."
        )

    if spec.guard_width <= 0.0:
        raise RuntimeError(
            "Invalid guard width."
        )

    r_edges = np.linspace(
        0.0,
        spec.outer_radius,
        nr + 1,
    )

    z_edges = np.linspace(
        -spec.depth,
        0.0,
        nz + 1,
    )

    r_centers = (
        0.5
        * (
            r_edges[
                :-1
            ]
            + r_edges[
                1:
            ]
        )
    )

    z_centers = (
        0.5
        * (
            z_edges[
                :-1
            ]
            + z_edges[
                1:
            ]
        )
    )

    R, Z = np.meshgrid(
        r_centers,
        z_centers,
        indexing="ij",
    )

    top_mask = (
        (
            R
            <=
            spec.top_radius
        )
        &
        (
            Z
            >=
            -spec.top_thickness
        )
    )

    guard_lo = max(
        0.0,
        spec.top_radius
        - 0.5
        * spec.guard_width,
    )

    guard_hi = min(
        spec.outer_radius,
        spec.top_radius
        + 0.5
        * spec.guard_width,
    )

    guard_mask = (
        (
            R
            >=
            guard_lo
        )
        &
        (
            R
            <=
            guard_hi
        )
    )

    back_mask = (
        (
            R
            <=
            spec.outer_radius
        )
        &
        (
            Z
            <=
            -spec.depth
            + spec.back_thickness
        )
    )

    active_mask = (
        top_mask
        |
        guard_mask
        |
        back_mask
    )

    # Disjoint role masks used only for diagnostics.
    role_top = (
        top_mask
        &
        active_mask
    )

    role_back = (
        back_mask
        &
        ~role_top
        &
        active_mask
    )

    role_guard = (
        active_mask
        &
        ~role_top
        &
        ~role_back
    )

    volumes = np.zeros(
        (
            nr,
            nz,
        ),
        dtype=float,
    )

    kr = np.zeros(
        (
            len(
                SENTINEL_RADII
            ),
            nr,
            nz,
        ),
        dtype=float,
    )

    kz = np.zeros_like(
        kr
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

        annulus_area = (
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
                annulus_area
                * (
                    z1
                    - z0
                )
            )

            if not active_mask[
                i,
                j
            ]:
                continue

            for k, target_r in enumerate(
                SENTINEL_RADII
            ):

                (
                    kr[
                        k,
                        i,
                        j,
                    ],
                    kz[
                        k,
                        i,
                        j,
                    ],
                ) = (
                    c024.vector_cell_kernel(
                        r0,
                        r1,
                        z0,
                        z1,
                        float(
                            target_r
                        ),
                        TARGET_Z,
                        order=kernel_order,
                        nphi=nphi,
                    )
                )

    return {
        "r_edges":
            r_edges,

        "z_edges":
            z_edges,

        "r_centers":
            r_centers,

        "z_centers":
            z_centers,

        "volumes":
            volumes,

        "active_mask":
            active_mask,

        "role_top":
            role_top,

        "role_guard":
            role_guard,

        "role_back":
            role_back,

        "kr":
            kr,

        "kz":
            kz,
    }


def solve_case(
    int14b,
    c024,
    spec: SandwichSpec,
    nr: int,
    nz: int,
    *,
    mode: str,
    guided: bool = False,
    solver_override: str | None = None,
) -> dict[str, Any]:
    """Solve one point or planar guarded-sandwich source."""

    if mode not in (
        "POINT",
        "PLANAR",
    ):
        raise RuntimeError(
            f"Unknown mode: {mode}"
        )

    case = make_case(
        int14b,
        spec,
        nr,
        nz,
    )

    geometry = build_geometry(
        c024,
        spec,
        nr,
        nz,
        kernel_order=SCOUT_KERNEL_ORDER,
        nphi=SCOUT_NPHI,
    )

    r_edges = geometry[
        "r_edges"
    ]

    z_edges = geometry[
        "z_edges"
    ]

    volumes = geometry[
        "volumes"
    ]

    active_mask = geometry[
        "active_mask"
    ]

    role_top = geometry[
        "role_top"
    ]

    role_guard = geometry[
        "role_guard"
    ]

    role_back = geometry[
        "role_back"
    ]

    kr = geometry[
        "kr"
    ]

    kz = geometry[
        "kz"
    ]

    e = cp.Variable(
        (
            nr,
            nz,
        ),
        nonneg=True,
        name=(
            f"e_{spec.name}_"
            f"{mode}_"
            f"{nr}x{nz}"
        ),
    )

    pphi = cp.Variable(
        (
            nr,
            nz,
        ),
        name=(
            f"pphi_{spec.name}_"
            f"{mode}_"
            f"{nr}x{nz}"
        ),
    )

    pr_face = cp.Variable(
        (
            nr + 1,
            nz,
        ),
        name=(
            f"pr_{spec.name}_"
            f"{mode}_"
            f"{nr}x{nz}"
        ),
    )

    pz_face = cp.Variable(
        (
            nr,
            nz + 1,
        ),
        name=(
            f"pz_{spec.name}_"
            f"{mode}_"
            f"{nr}x{nz}"
        ),
    )

    trz_vertex = cp.Variable(
        (
            nr + 1,
            nz + 1,
        ),
        name=(
            f"trz_{spec.name}_"
            f"{mode}_"
            f"{nr}x{nz}"
        ),
    )

    constraints: list[
        cp.Constraint
    ] = []

    int14b.add_mask_boundary_constraints(
        constraints,
        case,
        active_mask,
        e,
        pphi,
        pr_face,
        pz_face,
        trz_vertex,
    )

    pr_cell: list[
        list[
            cp.Expression
        ]
    ] = [
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

    pz_cell: list[
        list[
            cp.Expression
        ]
    ] = [
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

    trz_cell: list[
        list[
            cp.Expression
        ]
    ] = [
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

    # ------------------------------------------------------------
    # Exact type-I DEC in each cell.
    # ------------------------------------------------------------

    for i in range(
        nr
    ):

        for j in range(
            nz
        ):

            prc = (
                0.5
                * (
                    pr_face[
                        i,
                        j
                    ]
                    + pr_face[
                        i + 1,
                        j
                    ]
                )
            )

            pzc = (
                0.5
                * (
                    pz_face[
                        i,
                        j
                    ]
                    + pz_face[
                        i,
                        j + 1
                    ]
                )
            )

            trzc = (
                0.25
                * (
                    trz_vertex[
                        i,
                        j
                    ]
                    + trz_vertex[
                        i + 1,
                        j
                    ]
                    + trz_vertex[
                        i,
                        j + 1
                    ]
                    + trz_vertex[
                        i + 1,
                        j + 1
                    ]
                )
            )

            pr_cell[
                i
            ][
                j
            ] = prc

            pz_cell[
                i
            ][
                j
            ] = pzc

            trz_cell[
                i
            ][
                j
            ] = trzc

            mean = (
                0.5
                * (
                    prc
                    + pzc
                )
            )

            half_difference = (
                0.5
                * (
                    prc
                    - pzc
                )
            )

            spectral_radius = cp.norm(
                cp.hstack(
                    [
                        half_difference,
                        trzc,
                    ]
                ),
                2,
            )

            constraints.extend(
                [
                    spectral_radius
                    <=
                    e[
                        i,
                        j
                    ]
                    - mean,

                    spectral_radius
                    <=
                    e[
                        i,
                        j
                    ]
                    + mean,

                    pphi[
                        i,
                        j
                    ]
                    <=
                    e[
                        i,
                        j
                    ],

                    -pphi[
                        i,
                        j
                    ]
                    <=
                    e[
                        i,
                        j
                    ],
                ]
            )

    # ------------------------------------------------------------
    # Exact integrated finite-volume conservation.
    # ------------------------------------------------------------

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

            dz = float(
                z_edges[
                    j + 1
                ]
                - z_edges[
                    j
                ]
            )

            trz_south = (
                0.5
                * (
                    trz_vertex[
                        i,
                        j
                    ]
                    + trz_vertex[
                        i + 1,
                        j
                    ]
                )
            )

            trz_north = (
                0.5
                * (
                    trz_vertex[
                        i,
                        j + 1
                    ]
                    + trz_vertex[
                        i + 1,
                        j + 1
                    ]
                )
            )

            trz_west = (
                0.5
                * (
                    trz_vertex[
                        i,
                        j
                    ]
                    + trz_vertex[
                        i,
                        j + 1
                    ]
                )
            )

            trz_east = (
                0.5
                * (
                    trz_vertex[
                        i + 1,
                        j
                    ]
                    + trz_vertex[
                        i + 1,
                        j + 1
                    ]
                )
            )

            radial_balance = (
                dz
                * (
                    r1
                    * pr_face[
                        i + 1,
                        j
                    ]
                    - r0
                    * pr_face[
                        i,
                        j
                    ]
                )
                + annular_radial_factor
                * (
                    trz_north
                    - trz_south
                )
                - dr
                * dz
                * pphi[
                    i,
                    j
                ]
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
                    pz_face[
                        i,
                        j + 1
                    ]
                    - pz_face[
                        i,
                        j
                    ]
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

    pr_matrix = cp.vstack(
        [
            cp.hstack(
                [
                    pr_cell[
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

    pz_matrix = cp.vstack(
        [
            cp.hstack(
                [
                    pz_cell[
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

    volume_constant = cp.Constant(
        volumes
    )

    # Integrated static Laue constraints.
    constraints.extend(
        [
            cp.sum(
                cp.multiply(
                    volume_constant,
                    pr_matrix
                    + pphi,
                )
            )
            == 0.0,

            cp.sum(
                cp.multiply(
                    volume_constant,
                    pz_matrix,
                )
            )
            == 0.0,
        ]
    )

    active_density = (
        e
        + pr_matrix
        + pz_matrix
        + pphi
    )

    total_energy = cp.sum(
        cp.multiply(
            volume_constant,
            e,
        )
    )

    axial_expr = []

    radial_expr = []

    for k in range(
        len(
            SENTINEL_RADII
        )
    ):

        axial_expr.append(
            cp.sum(
                cp.multiply(
                    cp.Constant(
                        kz[
                            k
                        ]
                    ),
                    active_density,
                )
            )
        )

        radial_expr.append(
            cp.sum(
                cp.multiply(
                    cp.Constant(
                        kr[
                            k
                        ]
                    ),
                    active_density,
                )
            )
        )

    if mode == "POINT":

        constraints.append(
            axial_expr[
                0
            ]
            >= AXIAL_MIN
        )

    else:

        for az, ar in zip(
            axial_expr,
            radial_expr,
        ):

            constraints.extend(
                [
                    az
                    >= AXIAL_MIN,

                    az
                    <= AXIAL_MAX,

                    cp.abs(
                        ar
                    )
                    <= RADIAL_ABS_MAX,
                ]
            )

    # ------------------------------------------------------------
    # Optional intuitive role assignment.
    # ------------------------------------------------------------

    if guided:

        top_weight = (
            volumes
            * role_top.astype(
                float
            )
        )

        back_weight = (
            volumes
            * role_back.astype(
                float
            )
        )

        top_energy = cp.sum(
            cp.multiply(
                cp.Constant(
                    top_weight
                ),
                e,
            )
        )

        top_active = cp.sum(
            cp.multiply(
                cp.Constant(
                    top_weight
                ),
                active_density,
            )
        )

        back_active = cp.sum(
            cp.multiply(
                cp.Constant(
                    back_weight
                ),
                active_density,
            )
        )

        constraints.extend(
            [
                top_active
                <=
                -0.25
                * top_energy,

                back_active
                >= 0.0,
            ]
        )

    problem = cp.Problem(
        cp.Minimize(
            total_energy
        ),
        constraints,
    )

    installed = cp.installed_solvers()

    if solver_override is not None:

        if solver_override not in installed:

            return {
                "name":
                    spec.name,

                "mode":
                    mode,

                "guided":
                    guided,

                "solver":
                    solver_override,

                "status":
                    "SOLVER_NOT_INSTALLED",

                "green":
                    False,

                "coefficient":
                    float(
                        "nan"
                    ),
            }

        solver = solver_override

    else:

        solver = (
            "CLARABEL"
            if "CLARABEL" in installed
            else "SCS"
        )

    if solver == "SCS":

        problem.solve(
            solver="SCS",
            verbose=False,
            eps=2.0e-7,
            max_iters=400000,
        )

    else:

        problem.solve(
            solver=solver,
            verbose=False,
        )

    base = {
        "name":
            spec.name,

        "category":
            spec.category,

        "mode":
            mode,

        "guided":
            guided,

        "solver":
            solver,

        "status":
            str(
                problem.status
            ),

        "nr":
            nr,

        "nz":
            nz,

        "top_radius":
            spec.top_radius,

        "outer_radius":
            spec.outer_radius,

        "depth":
            spec.depth,

        "top_thickness":
            spec.top_thickness,

        "guard_width":
            spec.guard_width,

        "back_thickness":
            spec.back_thickness,
    }

    if problem.status not in (
        cp.OPTIMAL,
        cp.OPTIMAL_INACCURATE,
    ):

        return {
            **base,

            "green":
                False,

            "coefficient":
                float(
                    "nan"
                ),
        }

    e_v = np.asarray(
        e.value,
        dtype=float,
    )

    pphi_v = np.asarray(
        pphi.value,
        dtype=float,
    )

    prf_v = np.asarray(
        pr_face.value,
        dtype=float,
    )

    pzf_v = np.asarray(
        pz_face.value,
        dtype=float,
    )

    trzv_v = np.asarray(
        trz_vertex.value,
        dtype=float,
    )

    pr_v = (
        0.5
        * (
            prf_v[
                :-1,
                :
            ]
            + prf_v[
                1:,
                :
            ]
        )
    )

    pz_v = (
        0.5
        * (
            pzf_v[
                :,
                :-1
            ]
            + pzf_v[
                :,
                1:
            ]
        )
    )

    trz_v = (
        0.25
        * (
            trzv_v[
                :-1,
                :-1
            ]
            + trzv_v[
                1:,
                :-1
            ]
            + trzv_v[
                :-1,
                1:
            ]
            + trzv_v[
                1:,
                1:
            ]
        )
    )

    active_v = (
        e_v
        + pr_v
        + pz_v
        + pphi_v
    )

    energy_v = float(
        np.sum(
            volumes
            * e_v
        )
    )

    axial_v = np.asarray(
        [
            float(
                np.sum(
                    kz[
                        k
                    ]
                    * active_v
                )
            )
            for k in range(
                len(
                    SENTINEL_RADII
                )
            )
        ],
        dtype=float,
    )

    radial_v = np.asarray(
        [
            float(
                np.sum(
                    kr[
                        k
                    ]
                    * active_v
                )
            )
            for k in range(
                len(
                    SENTINEL_RADII
                )
            )
        ],
        dtype=float,
    )

    # ------------------------------------------------------------
    # Independent DEC postcheck.
    # ------------------------------------------------------------

    max_dec_violation = 0.0

    dec_ratio = np.zeros_like(
        e_v
    )

    max_e = max(
        float(
            np.max(
                e_v
            )
        ),
        1.0e-300,
    )

    materially_occupied = (
        active_mask
        &
        (
            e_v
            >=
            1.0e-6
            * max_e
        )
    )

    for i in range(
        nr
    ):

        for j in range(
            nz
        ):

            stress = np.asarray(
                [
                    [
                        pr_v[
                            i,
                            j
                        ],
                        trz_v[
                            i,
                            j
                        ],
                        0.0,
                    ],
                    [
                        trz_v[
                            i,
                            j
                        ],
                        pz_v[
                            i,
                            j
                        ],
                        0.0,
                    ],
                    [
                        0.0,
                        0.0,
                        pphi_v[
                            i,
                            j
                        ],
                    ],
                ],
                dtype=float,
            )

            largest = float(
                np.max(
                    np.abs(
                        np.linalg.eigvalsh(
                            stress
                        )
                    )
                )
            )

            max_dec_violation = max(
                max_dec_violation,
                largest
                - e_v[
                    i,
                    j
                ],
            )

            if materially_occupied[
                i,
                j
            ]:

                dec_ratio[
                    i,
                    j
                ] = (
                    largest
                    /
                    max(
                        e_v[
                            i,
                            j
                        ],
                        1.0e-300,
                    )
                )

    occupied_ratios = dec_ratio[
        materially_occupied
    ]

    if occupied_ratios.size:

        max_dec_ratio_occupied = float(
            np.max(
                occupied_ratios
            )
        )

    else:

        max_dec_ratio_occupied = float(
            "nan"
        )

    # ------------------------------------------------------------
    # Conservation postcheck.
    # ------------------------------------------------------------

    max_cons = 0.0

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

            dz = float(
                z_edges[
                    j + 1
                ]
                - z_edges[
                    j
                ]
            )

            trz_south = (
                0.5
                * (
                    trzv_v[
                        i,
                        j
                    ]
                    + trzv_v[
                        i + 1,
                        j
                    ]
                )
            )

            trz_north = (
                0.5
                * (
                    trzv_v[
                        i,
                        j + 1
                    ]
                    + trzv_v[
                        i + 1,
                        j + 1
                    ]
                )
            )

            trz_west = (
                0.5
                * (
                    trzv_v[
                        i,
                        j
                    ]
                    + trzv_v[
                        i,
                        j + 1
                    ]
                )
            )

            trz_east = (
                0.5
                * (
                    trzv_v[
                        i + 1,
                        j
                    ]
                    + trzv_v[
                        i + 1,
                        j + 1
                    ]
                )
            )

            rr = (
                dz
                * (
                    r1
                    * prf_v[
                        i + 1,
                        j
                    ]
                    - r0
                    * prf_v[
                        i,
                        j
                    ]
                )
                + annular_radial_factor
                * (
                    trz_north
                    - trz_south
                )
                - dr
                * dz
                * pphi_v[
                    i,
                    j
                ]
            )

            zz = (
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
                    pzf_v[
                        i,
                        j + 1
                    ]
                    - pzf_v[
                        i,
                        j
                    ]
                )
            )

            max_cons = max(
                max_cons,
                abs(
                    float(
                        rr
                    )
                ),
                abs(
                    float(
                        zz
                    )
                ),
            )

    radial_laue = float(
        np.sum(
            volumes
            * (
                pr_v
                + pphi_v
            )
        )
    )

    vertical_laue = float(
        np.sum(
            volumes
            * pz_v
        )
    )

    trace_integral = (
        radial_laue
        + vertical_laue
    )

    active_total = float(
        np.sum(
            volumes
            * active_v
        )
    )

    active_total_relerr = (
        abs(
            active_total
            - energy_v
        )
        /
        max(
            abs(
                energy_v
            ),
            1.0e-300,
        )
    )

    # ------------------------------------------------------------
    # Force anatomy.
    # ------------------------------------------------------------

    center_force = (
        kz[
            0
        ]
        * active_v
    )

    gross_outward = float(
        np.sum(
            np.maximum(
                center_force,
                0.0,
            )
        )
    )

    gross_opposing = float(
        np.sum(
            np.maximum(
                -center_force,
                0.0,
            )
        )
    )

    cancellation = (
        (
            gross_outward
            + gross_opposing
        )
        /
        max(
            abs(
                axial_v[
                    0
                ]
            ),
            1.0e-300,
        )
    )

    cell_energy = (
        volumes
        * e_v
    )

    outward_cell = np.maximum(
        center_force,
        0.0,
    )

    f90 = force_energy_fraction(
        cell_energy,
        outward_cell,
        0.90,
    )

    energy_veff = effective_volume(
        cell_energy,
        volumes,
    )

    force_veff = effective_volume(
        outward_cell,
        volumes,
    )

    energy_length = (
        energy_veff
        ** (
            1.0
            / 3.0
        )
        if energy_veff
        > 0.0
        else 0.0
    )

    force_length = (
        force_veff
        ** (
            1.0
            / 3.0
        )
        if force_veff
        > 0.0
        else 0.0
    )

    grid_scale = max(
        float(
            spec.outer_radius
            / nr
        ),
        float(
            spec.depth
            / nz
        ),
    )

    width_cells = (
        min(
            energy_length,
            force_length,
        )
        /
        max(
            grid_scale,
            1.0e-300,
        )
    )

    role_metrics = {}

    for role_name, mask in (
        (
            "top",
            role_top,
        ),
        (
            "guard",
            role_guard,
        ),
        (
            "back",
            role_back,
        ),
    ):

        role_energy = float(
            np.sum(
                volumes[
                    mask
                ]
                * e_v[
                    mask
                ]
            )
        )

        role_center_force = float(
            np.sum(
                center_force[
                    mask
                ]
            )
        )

        role_active = float(
            np.sum(
                volumes[
                    mask
                ]
                * active_v[
                    mask
                ]
            )
        )

        role_metrics[
            role_name
        ] = {
            "energy":
                role_energy,

            "energy_fraction":
                role_energy
                / max(
                    energy_v,
                    1.0e-300,
                ),

            "center_force":
                role_center_force,

            "active_integral":
                role_active,

            "outward_share":
                max(
                    role_center_force,
                    0.0,
                )
                / max(
                    gross_outward,
                    1.0e-300,
                ),
        }

    min_axial = float(
        np.min(
            axial_v
        )
    )

    max_axial = float(
        np.max(
            axial_v
        )
    )

    max_abs_radial = float(
        np.max(
            np.abs(
                radial_v
            )
        )
    )

    max_transverse_fraction = float(
        np.max(
            np.abs(
                radial_v
            )
            /
            np.maximum(
                np.abs(
                    axial_v
                ),
                1.0e-300,
            )
        )
    )

    flatness = (
        (
            max_axial
            - min_axial
        )
        /
        max(
            abs(
                float(
                    np.mean(
                        axial_v
                    )
                )
            ),
            1.0e-300,
        )
    )

    if mode == "POINT":

        target_postcheck = bool(
            axial_v[
                0
            ]
            >=
            AXIAL_MIN
            - CONSTRAINT_POST_TOL
        )

    else:

        target_postcheck = bool(
            min_axial
            >=
            AXIAL_MIN
            - CONSTRAINT_POST_TOL

            and
            max_axial
            <=
            AXIAL_MAX
            + CONSTRAINT_POST_TOL

            and
            max_abs_radial
            <=
            RADIAL_ABS_MAX
            + CONSTRAINT_POST_TOL
        )

    physics_green = bool(
        math.isfinite(
            energy_v
        )
        and energy_v
        > 0.0

        and max_dec_violation
        <= DEC_TOL

        and max_cons
        <= CONS_TOL

        and abs(
            trace_integral
        )
        <= TRACE_TOL

        and active_total_relerr
        <= ACTIVE_TOTAL_TOL

        and target_postcheck
    )

    return {
        **base,

        "green":
            physics_green,

        "coefficient":
            energy_v,

        "energy":
            energy_v,

        "axial":
            axial_v,

        "radial":
            radial_v,

        "min_axial":
            min_axial,

        "max_axial":
            max_axial,

        "max_abs_radial":
            max_abs_radial,

        "max_transverse_fraction":
            max_transverse_fraction,

        "planar_flatness":
            flatness,

        "max_dec_violation":
            max_dec_violation,

        "max_dec_ratio_occupied":
            max_dec_ratio_occupied,

        "max_conservation_residual":
            max_cons,

        "radial_laue":
            radial_laue,

        "vertical_laue":
            vertical_laue,

        "trace_integral":
            trace_integral,

        "active_total":
            active_total,

        "active_total_relerr":
            active_total_relerr,

        "gross_outward":
            gross_outward,

        "gross_opposing":
            gross_opposing,

        "cancellation":
            cancellation,

        "F90_energy_fraction":
            f90,

        "energy_effective_length":
            energy_length,

        "force_effective_length":
            force_length,

        "min_width_cells":
            width_cells,

        "role_metrics":
            role_metrics,

        "_arrays": {
            "r_edges":
                r_edges,

            "z_edges":
                z_edges,

            "volumes":
                volumes,

            "active_mask":
                active_mask,

            "role_top":
                role_top,

            "role_guard":
                role_guard,

            "role_back":
                role_back,

            "e":
                e_v,

            "pr":
                pr_v,

            "pz":
                pz_v,

            "pphi":
                pphi_v,

            "trz":
                trz_v,

            "active_density":
                active_v,

            "kr":
                kr,

            "kz":
                kz,
        },
    }


def public_row(
    row: dict[str, Any],
) -> dict[str, Any]:
    """Flatten one result for CSV output."""

    out = {
        key: value
        for key, value
        in row.items()
        if (
            key
            not in (
                "_arrays",
                "role_metrics",
                "axial",
                "radial",
            )
        )
    }

    axial = row.get(
        "axial"
    )

    radial = row.get(
        "radial"
    )

    if axial is not None:

        for index, value in enumerate(
            np.asarray(
                axial,
                dtype=float,
            )
        ):

            out[
                f"axial_{index}"
            ] = float(
                value
            )

    if radial is not None:

        for index, value in enumerate(
            np.asarray(
                radial,
                dtype=float,
            )
        ):

            out[
                f"radial_{index}"
            ] = float(
                value
            )

    roles = row.get(
        "role_metrics",
        {}
    )

    for role_name, metrics in roles.items():

        for key, value in metrics.items():

            out[
                f"{role_name}_{key}"
            ] = value

    return out


def print_case(
    label: str,
    row: dict[str, Any],
) -> None:
    """Compact decision line."""

    coefficient = float(
        row.get(
            "coefficient",
            float(
                "nan"
            ),
        )
    )

    print(
        f"024C1_CASE={label} "
        f"MODE={row.get('mode')} "
        f"GUIDED={'YES' if row.get('guided') else 'NO'} "
        f"C={coefficient:.12e} "
        f"GREEN={'YES' if bool(row.get('green', False)) else 'NO'} "
        f"MIN_AZ={float(row.get('min_axial', float('nan'))):+.6e} "
        f"MAX_AR={float(row.get('max_abs_radial', float('nan'))):.6e} "
        f"TRANS={float(row.get('max_transverse_fraction', float('nan'))):.6e} "
        f"CANCEL={float(row.get('cancellation', float('nan'))):.6e} "
        f"DEC={float(row.get('max_dec_violation', float('nan'))):.3e} "
        f"CONS={float(row.get('max_conservation_residual', float('nan'))):.3e}",
        flush=True,
    )


def independent_vector_reconstruction(
    c024,
    row: dict[str, Any],
) -> dict[str, Any]:
    """Higher-order vector-force reconstruction of selected high solution."""

    arrays = row[
        "_arrays"
    ]

    active = np.asarray(
        arrays[
            "active_density"
        ],
        dtype=float,
    )

    active_mask = np.asarray(
        arrays[
            "active_mask"
        ],
        dtype=bool,
    )

    r_edges = np.asarray(
        arrays[
            "r_edges"
        ],
        dtype=float,
    )

    z_edges = np.asarray(
        arrays[
            "z_edges"
        ],
        dtype=float,
    )

    nr, nz = active.shape

    axial_hi = np.zeros(
        len(
            SENTINEL_RADII
        ),
        dtype=float,
    )

    radial_hi = np.zeros_like(
        axial_hi
    )

    for i in range(
        nr
    ):

        for j in range(
            nz
        ):

            if not active_mask[
                i,
                j
            ]:
                continue

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

            for k, target_r in enumerate(
                SENTINEL_RADII
            ):

                kr_hi, kz_hi = (
                    c024.vector_cell_kernel(
                        r0,
                        r1,
                        z0,
                        z1,
                        float(
                            target_r
                        ),
                        TARGET_Z,
                        order=INDEPENDENT_KERNEL_ORDER,
                        nphi=INDEPENDENT_NPHI,
                    )
                )

                radial_hi[
                    k
                ] += (
                    kr_hi
                    * active[
                        i,
                        j
                    ]
                )

                axial_hi[
                    k
                ] += (
                    kz_hi
                    * active[
                        i,
                        j
                    ]
                )

    axial_base = np.asarray(
        row[
            "axial"
        ],
        dtype=float,
    )

    radial_base = np.asarray(
        row[
            "radial"
        ],
        dtype=float,
    )

    max_abs_diff = float(
        max(
            np.max(
                np.abs(
                    axial_hi
                    - axial_base
                )
            ),
            np.max(
                np.abs(
                    radial_hi
                    - radial_base
                )
            ),
        )
    )

    scale = max(
        float(
            np.max(
                np.abs(
                    axial_hi
                )
            )
        ),
        float(
            np.max(
                np.abs(
                    radial_hi
                )
            )
        ),
        1.0,
    )

    normalized_error = (
        max_abs_diff
        / scale
    )

    passed = bool(
        normalized_error
        <=
        INDEPENDENT_VECTOR_TOL
    )

    return {
        "axial_hi":
            axial_hi,

        "radial_hi":
            radial_hi,

        "max_abs_difference":
            max_abs_diff,

        "normalized_error":
            normalized_error,

        "pass":
            passed,
    }


def main() -> None:
    """Execute the complete 024C1 gate."""

    print(
        "=== 024C1 INTUITIVE GUARDED STRESS SANDWICH ===",
        flush=True,
    )

    for path in (
        PRIOR_SUMMARY,
        INT14B_SOURCE,
        C024_SOURCE,
    ):
        require(
            path
        )

    prior = json.loads(
        PRIOR_SUMMARY.read_text(
            encoding="utf-8"
        )
    )

    if prior.get(
        "decision"
    ) != (
        "RED_BURIED_PLANAR_STRESS_LENS_"
        "DID_NOT_BEAT_006D_IN_TESTED_CLASS"
    ):
        raise RuntimeError(
            "Unexpected 024C predecessor decision."
        )

    int14b = load_module(
        "ag024c1_int14b",
        INT14B_SOURCE,
    )

    c024 = load_module(
        "ag024c1_024c",
        C024_SOURCE,
    )

    print(
        "\n=== A — ANCHORS AND DESIGN TARGETS ==="
    )

    print(
        f"C_006D="
        f"{C006D:.15f}"
    )

    print(
        f"C_024C_CONSERVATIVE="
        f"{PRIOR_024C_C:.15f}"
    )

    print(
        f"024C_TRANSVERSE_FRACTION="
        f"{PRIOR_024C_TRANSVERSE:.15f}"
    )

    print(
        f"024C_CANCELLATION="
        f"{PRIOR_024C_CANCELLATION:.15f}"
    )

    print(
        "ARCHITECTURE="
        "TOP_FACE_PLUS_GUARD_PLUS_BURIED_BACKPLANE"
    )

    print(
        "PLANAR_SENTINEL_RADII="
        + ",".join(
            f"{x:.3f}"
            for x in SENTINEL_RADII
        )
    )

    print(
        f"PLANAR_AXIAL_RANGE="
        f"{AXIAL_MIN:.3f}_TO_{AXIAL_MAX:.3f}"
    )

    print(
        f"PLANAR_RADIAL_ABS_MAX="
        f"{RADIAL_ABS_MAX:.3f}"
    )

    # ------------------------------------------------------------
    # B. Physical scout.
    # ------------------------------------------------------------

    physical_specs = [
        SandwichSpec(
            "024C1_PHYSICAL_A",
            top_radius=1.50,
            outer_radius=4.00,
            depth=1.25,
        ),
        SandwichSpec(
            "024C1_PHYSICAL_B",
            top_radius=2.00,
            outer_radius=4.00,
            depth=1.50,
        ),
        SandwichSpec(
            "024C1_PHYSICAL_C",
            top_radius=2.50,
            outer_radius=4.50,
            depth=1.50,
        ),
        SandwichSpec(
            "024C1_PHYSICAL_D",
            top_radius=2.50,
            outer_radius=5.00,
            depth=2.00,
        ),
    ]

    all_rows: list[
        dict[str, Any]
    ] = []

    physical_rows = []

    print(
        "\n=== B — PHYSICAL GEOMETRY SCOUT ===",
        flush=True,
    )

    for spec in physical_specs:

        point = solve_case(
            int14b,
            c024,
            spec,
            SCOUT_NR,
            SCOUT_NZ,
            mode="POINT",
        )

        print_case(
            spec.name
            + "_POINT",
            point,
        )

        all_rows.append(
            point
        )

        planar = solve_case(
            int14b,
            c024,
            spec,
            SCOUT_NR,
            SCOUT_NZ,
            mode="PLANAR",
        )

        print_case(
            spec.name
            + "_PLANAR",
            planar,
        )

        all_rows.append(
            planar
        )

        physical_rows.append(
            (
                spec,
                point,
                planar,
            )
        )

    # ------------------------------------------------------------
    # C. Blind wildcard diagnostics.
    # ------------------------------------------------------------

    print(
        "\n=== C — BLIND WILDCARD DIAGNOSTICS ==="
    )

    print(
        "BLIND_WILDCARD_NOT_PHYSICS_PRIOR_VALUES="
        + ",".join(
            str(
                value
            )
            for value in BLIND_WILDCARD_VALUES
        )
    )

    for value in BLIND_WILDCARD_VALUES:

        wildcard_spec = SandwichSpec(
            name=(
                "024C1_WILDCARD_TOPR_"
                + str(
                    value
                ).replace(
                    ".",
                    "P",
                )
            ),
            top_radius=min(
                value,
                5.0,
            ),
            outer_radius=5.0,
            depth=1.6,
            category=(
                "BLIND_WILDCARD_NOT_PHYSICS_PRIOR"
            ),
        )

        row = solve_case(
            int14b,
            c024,
            wildcard_spec,
            12,
            10,
            mode="POINT",
        )

        print_case(
            wildcard_spec.name,
            row,
        )

        all_rows.append(
            row
        )

    print(
        "WILDCARDS_USED_FOR_SELECTION=NO"
    )

    # ------------------------------------------------------------
    # D. Select only from physical PLANAR cases.
    # ------------------------------------------------------------

    planar_green = [
        item
        for item in physical_rows
        if bool(
            item[
                2
            ].get(
                "green",
                False,
            )
        )
        and math.isfinite(
            float(
                item[
                    2
                ].get(
                    "coefficient",
                    float(
                        "nan"
                    ),
                )
            )
        )
    ]

    if not planar_green:

        print(
            "\n=== D — NO PLANAR FEASIBLE PHYSICAL SCOUT ==="
        )

        print(
            "PHYSICAL_PLANAR_FEASIBLE_CASES=0"
        )

        decision = (
            "RED_INTUITIVE_SANDWICH_NO_PLANAR_FEASIBLE_SCOUT"
        )

        summary = {
            "claim_classification":
                (
                    "PROJECT_DERIVED_INTUITIVE_GUARDED_"
                    "STRESS_SANDWICH_SOURCE_PREFILTER"
                ),

            "decision":
                decision,

            "gates": {
                "planar_feasible":
                    False,

                "beats_024C":
                    False,

                "beats_006D":
                    False,
            },

            "next":
                (
                    "STOP_024C1_AND_RERANK_006D_MICROSCOPIC_"
                    "REALIZATION_VS_ANALOGUE_ANTIGRAVITY"
                ),

            "practical_antigravity_device":
                False,
        }

        public = [
            public_row(
                row
            )
            for row in all_rows
        ]

        fields = sorted(
            {
                key
                for row in public
                for key in row
            }
        )

        with OUT_CASES.open(
            "w",
            encoding="utf-8",
            newline="",
        ) as handle:

            writer = csv.DictWriter(
                handle,
                fieldnames=fields,
            )

            writer.writeheader()

            writer.writerows(
                public
            )

        OUT_SUMMARY.write_text(
            json.dumps(
                summary,
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

        print(
            f"024C1_DECISION="
            f"{decision}"
        )

        print(
            "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
        )

        print(
            f"SUMMARY_JSON="
            f"{OUT_SUMMARY.relative_to(ROOT)}"
        )

        print(
            f"CASES_CSV="
            f"{OUT_CASES.relative_to(ROOT)}"
        )

        print(
            "024C1_RUN_COMPLETE=YES"
        )

        return

    selected_spec, scout_point, scout_planar = min(
        planar_green,
        key=lambda item: float(
            item[
                2
            ][
                "coefficient"
            ]
        ),
    )

    print(
        "\n=== D — SELECTED INTUITIVE GEOMETRY ==="
    )

    print(
        f"SELECTED_NAME="
        f"{selected_spec.name}"
    )

    print(
        f"SELECTED_TOP_RADIUS="
        f"{selected_spec.top_radius:.15f}"
    )

    print(
        f"SELECTED_OUTER_RADIUS="
        f"{selected_spec.outer_radius:.15f}"
    )

    print(
        f"SELECTED_DEPTH="
        f"{selected_spec.depth:.15f}"
    )

    print(
        f"SELECTED_SCOUT_POINT_C="
        f"{float(scout_point['coefficient']):.15e}"
    )

    print(
        f"SELECTED_SCOUT_PLANAR_C="
        f"{float(scout_planar['coefficient']):.15e}"
    )

    print(
        f"SELECTED_SCOUT_PLANAR_PREMIUM="
        f"{float(scout_planar['coefficient']) / float(scout_point['coefficient']):.15e}"
    )

    # ------------------------------------------------------------
    # E. Refinement.
    # ------------------------------------------------------------

    print(
        "\n=== E — SELECTED PLANAR REFINEMENT ===",
        flush=True,
    )

    medium = solve_case(
        int14b,
        c024,
        SandwichSpec(
            **{
                **selected_spec.__dict__,
                "name":
                    selected_spec.name
                    + "_MEDIUM",
            }
        ),
        MEDIUM_NR,
        MEDIUM_NZ,
        mode="PLANAR",
    )

    print_case(
        "SELECTED_MEDIUM_PLANAR",
        medium,
    )

    all_rows.append(
        medium
    )

    high = solve_case(
        int14b,
        c024,
        SandwichSpec(
            **{
                **selected_spec.__dict__,
                "name":
                    selected_spec.name
                    + "_HIGH",
            }
        ),
        HIGH_NR,
        HIGH_NZ,
        mode="PLANAR",
    )

    print_case(
        "SELECTED_HIGH_PLANAR",
        high,
    )

    all_rows.append(
        high
    )

    high_point = solve_case(
        int14b,
        c024,
        SandwichSpec(
            **{
                **selected_spec.__dict__,
                "name":
                    selected_spec.name
                    + "_HIGH_POINT",
            }
        ),
        HIGH_NR,
        HIGH_NZ,
        mode="POINT",
    )

    print_case(
        "SELECTED_HIGH_POINT",
        high_point,
    )

    all_rows.append(
        high_point
    )

    # Guided intuitive-role test.
    guided_high = solve_case(
        int14b,
        c024,
        SandwichSpec(
            **{
                **selected_spec.__dict__,
                "name":
                    selected_spec.name
                    + "_HIGH_GUIDED",
            }
        ),
        HIGH_NR,
        HIGH_NZ,
        mode="PLANAR",
        guided=True,
    )

    print_case(
        "SELECTED_HIGH_PLANAR_GUIDED",
        guided_high,
    )

    all_rows.append(
        guided_high
    )

    # ------------------------------------------------------------
    # F. Refinement metrics.
    # ------------------------------------------------------------

    print(
        "\n=== F — REFINEMENT AND PLANARITY PREMIUM ==="
    )

    if not (
        bool(
            medium.get(
                "green",
                False,
            )
        )
        and bool(
            high.get(
                "green",
                False,
            )
        )
    ):

        convergence_green = False
        c_medium = float(
            medium.get(
                "coefficient",
                float(
                    "nan"
                ),
            )
        )
        c_high = float(
            high.get(
                "coefficient",
                float(
                    "nan"
                ),
            )
        )
        c_conservative = float(
            "nan"
        )
        c_rel = float(
            "nan"
        )

    else:

        convergence_green = True

        c_medium = float(
            medium[
                "coefficient"
            ]
        )

        c_high = float(
            high[
                "coefficient"
            ]
        )

        c_conservative = max(
            c_medium,
            c_high,
        )

        c_rel = relerr(
            c_medium,
            c_high,
        )

    print(
        f"PLANAR_C_MEDIUM="
        f"{c_medium:.15e}"
    )

    print(
        f"PLANAR_C_HIGH="
        f"{c_high:.15e}"
    )

    print(
        f"PLANAR_C_CONSERVATIVE="
        f"{c_conservative:.15e}"
    )

    print(
        f"PLANAR_C_REL_DIFF="
        f"{c_rel:.15e}"
    )

    if bool(
        high_point.get(
            "green",
            False,
        )
    ):

        point_high_c = float(
            high_point[
                "coefficient"
            ]
        )

        planarity_premium = (
            c_high
            / point_high_c
            if math.isfinite(
                c_high
            )
            else float(
                "nan"
            )
        )

    else:

        point_high_c = float(
            "nan"
        )

        planarity_premium = float(
            "nan"
        )

    print(
        f"POINT_C_HIGH="
        f"{point_high_c:.15e}"
    )

    print(
        f"PLANARITY_ENERGY_PREMIUM="
        f"{planarity_premium:.15e}"
    )

    width_high = float(
        high.get(
            "min_width_cells",
            float(
                "nan"
            ),
        )
    )

    print(
        f"HIGH_MIN_PARTICIPATION_WIDTH_CELLS="
        f"{width_high:.15e}"
    )

    # ------------------------------------------------------------
    # G. Independent high-order force reconstruction.
    # ------------------------------------------------------------

    print(
        "\n=== G — INDEPENDENT HIGH-ORDER VECTOR FORCE ===",
        flush=True,
    )

    if bool(
        high.get(
            "green",
            False,
        )
    ):

        independent = (
            independent_vector_reconstruction(
                c024,
                high,
            )
        )

        print(
            f"INDEPENDENT_VECTOR_MAX_ABS_DIFF="
            f"{float(independent['max_abs_difference']):.15e}"
        )

        print(
            f"INDEPENDENT_VECTOR_NORMALIZED_ERROR="
            f"{float(independent['normalized_error']):.15e}"
        )

        print(
            "INDEPENDENT_VECTOR_FORCE="
            + (
                "PASS"
                if bool(
                    independent[
                        "pass"
                    ]
                )
                else "FAIL"
            )
        )

        for radius, az, ar in zip(
            SENTINEL_RADII,
            independent[
                "axial_hi"
            ],
            independent[
                "radial_hi"
            ],
        ):

            print(
                f"INDEPENDENT_SENTINEL_R="
                f"{float(radius):.6f} "
                f"AZ={float(az):+.12e} "
                f"AR={float(ar):+.12e}"
            )

    else:

        independent = {
            "pass":
                False,

            "reason":
                "HIGH_NOT_GREEN",
        }

        print(
            "INDEPENDENT_VECTOR_FORCE=NOT_RUN_HIGH_NOT_GREEN"
        )

    # ------------------------------------------------------------
    # H. Corrected DEC / anatomy diagnostics.
    # ------------------------------------------------------------

    print(
        "\n=== H — INTUITIVE STRESS ANATOMY ==="
    )

    print(
        f"MAX_DEC_VIOLATION_ABSOLUTE="
        f"{float(high.get('max_dec_violation', float('nan'))):.15e}"
    )

    print(
        f"MAX_DEC_RATIO_MATERIALLY_OCCUPIED="
        f"{float(high.get('max_dec_ratio_occupied', float('nan'))):.15e}"
    )

    print(
        f"SELECTED_CANCELLATION="
        f"{float(high.get('cancellation', float('nan'))):.15e}"
    )

    print(
        f"SELECTED_F90_ENERGY_FRACTION="
        f"{float(high.get('F90_energy_fraction', float('nan'))):.15e}"
    )

    print(
        f"SELECTED_MAX_TRANSVERSE_FRACTION="
        f"{float(high.get('max_transverse_fraction', float('nan'))):.15e}"
    )

    print(
        f"SELECTED_PLANAR_FLATNESS="
        f"{float(high.get('planar_flatness', float('nan'))):.15e}"
    )

    roles = high.get(
        "role_metrics",
        {}
    )

    for role_name in (
        "top",
        "guard",
        "back",
    ):

        role = roles.get(
            role_name,
            {}
        )

        print(
            f"ROLE_{role_name.upper()}_ENERGY_FRACTION="
            f"{float(role.get('energy_fraction', float('nan'))):.15e}"
        )

        print(
            f"ROLE_{role_name.upper()}_CENTER_FORCE="
            f"{float(role.get('center_force', float('nan'))):+.15e}"
        )

        print(
            f"ROLE_{role_name.upper()}_ACTIVE_INTEGRAL="
            f"{float(role.get('active_integral', float('nan'))):+.15e}"
        )

        print(
            f"ROLE_{role_name.upper()}_OUTWARD_SHARE="
            f"{float(role.get('outward_share', float('nan'))):.15e}"
        )

    guided_green = bool(
        guided_high.get(
            "green",
            False,
        )
    )

    print(
        "GUIDED_ROLE_ASSIGNMENT="
        + (
            "FEASIBLE_GREEN"
            if guided_green
            else "NOT_GREEN"
        )
    )

    if guided_green:

        print(
            f"GUIDED_PLANAR_C="
            f"{float(guided_high['coefficient']):.15e}"
        )

        print(
            f"GUIDED_PENALTY_VS_FREE_PLANAR="
            f"{float(guided_high['coefficient']) / c_high:.15e}"
        )

    # ------------------------------------------------------------
    # I. Independent SCS.
    # ------------------------------------------------------------

    print(
        "\n=== I — INDEPENDENT SCS CHECK ===",
        flush=True,
    )

    installed = cp.installed_solvers()

    scs_available = (
        "SCS"
        in installed
    )

    scs_objective_match = False
    scs_full_postcheck = False
    scs_rel = float(
        "nan"
    )
    scs_c = float(
        "nan"
    )

    if scs_available:

        scs = solve_case(
            int14b,
            c024,
            SandwichSpec(
                **{
                    **selected_spec.__dict__,
                    "name":
                        selected_spec.name
                        + "_MEDIUM_SCS",
                }
            ),
            MEDIUM_NR,
            MEDIUM_NZ,
            mode="PLANAR",
            solver_override="SCS",
        )

        all_rows.append(
            scs
        )

        scs_c = float(
            scs.get(
                "coefficient",
                float(
                    "nan"
                ),
            )
        )

        if (
            math.isfinite(
                scs_c
            )
            and math.isfinite(
                c_medium
            )
        ):

            scs_rel = relerr(
                scs_c,
                c_medium,
            )

        scs_objective_match = bool(
            math.isfinite(
                scs_rel
            )
            and scs_rel
            <= SCS_OBJECTIVE_TOL
        )

        scs_full_postcheck = bool(
            scs.get(
                "green",
                False,
            )
        )

        print(
            f"SCS_MEDIUM_C="
            f"{scs_c:.15e}"
        )

        print(
            f"SCS_CLARABEL_OBJECTIVE_REL_DIFF="
            f"{scs_rel:.15e}"
        )

        print(
            "SCS_OBJECTIVE_MATCH="
            + (
                "PASS"
                if scs_objective_match
                else "FAIL"
            )
        )

        print(
            "SCS_FULL_POSTCHECK="
            + (
                "PASS"
                if scs_full_postcheck
                else "FAIL"
            )
        )

        print(
            f"SCS_MAX_DEC_VIOLATION="
            f"{float(scs.get('max_dec_violation', float('nan'))):.15e}"
        )

        print(
            f"SCS_MAX_CONSERVATION_RESIDUAL="
            f"{float(scs.get('max_conservation_residual', float('nan'))):.15e}"
        )

    else:

        print(
            "SCS_OBJECTIVE_MATCH=UNAVAILABLE"
        )

        print(
            "SCS_FULL_POSTCHECK=UNAVAILABLE"
        )

    # ------------------------------------------------------------
    # J. Compare against predecessor and 006D.
    # ------------------------------------------------------------

    print(
        "\n=== J — COMPARATIVE RESULT ==="
    )

    convergence_pass = bool(
        convergence_green
        and math.isfinite(
            c_rel
        )
        and c_rel
        <= C_CONVERGENCE_TOL
    )

    width_pass = bool(
        math.isfinite(
            width_high
        )
        and width_high
        >= MIN_WIDTH_CELLS
    )

    independent_pass = bool(
        independent.get(
            "pass",
            False,
        )
    )

    high_planar_pass = bool(
        high.get(
            "green",
            False,
        )
    )

    beats_024c = bool(
        math.isfinite(
            c_conservative
        )
        and c_conservative
        < PRIOR_024C_C
    )

    beats_006d = bool(
        math.isfinite(
            c_conservative
        )
        and c_conservative
        < C006D
    )

    cancellation_improved = bool(
        math.isfinite(
            float(
                high.get(
                    "cancellation",
                    float(
                        "nan"
                    ),
                )
            )
        )
        and float(
            high[
                "cancellation"
            ]
        )
        < PRIOR_024C_CANCELLATION
    )

    transverse_improved = bool(
        math.isfinite(
            float(
                high.get(
                    "max_transverse_fraction",
                    float(
                        "nan"
                    ),
                )
            )
        )
        and float(
            high[
                "max_transverse_fraction"
            ]
        )
        < PRIOR_024C_TRANSVERSE
    )

    print(
        f"IMPROVEMENT_FACTOR_VS_024C="
        f"{PRIOR_024C_C / c_conservative:.15e}"
        if math.isfinite(
            c_conservative
        )
        else
        "IMPROVEMENT_FACTOR_VS_024C=nan"
    )

    print(
        f"IMPROVEMENT_FACTOR_VS_006D="
        f"{C006D / c_conservative:.15e}"
        if math.isfinite(
            c_conservative
        )
        else
        "IMPROVEMENT_FACTOR_VS_006D=nan"
    )

    print(
        "CANCELLATION_IMPROVED_VS_024C="
        + (
            "YES"
            if cancellation_improved
            else "NO"
        )
    )

    print(
        "TRANSVERSE_IMPROVED_VS_024C="
        + (
            "YES"
            if transverse_improved
            else "NO"
        )
    )

    print(
        "BEATS_024C="
        + (
            "YES"
            if beats_024c
            else "NO"
        )
    )

    print(
        "BEATS_006D="
        + (
            "YES"
            if beats_006d
            else "NO"
        )
    )

    print(
        "C_CONVERGENCE_GATE="
        + (
            "PASS"
            if convergence_pass
            else "FAIL"
        )
    )

    print(
        "WIDTH_GATE="
        + (
            "PASS"
            if width_pass
            else "FAIL"
        )
    )

    print(
        "PLANAR_GATE="
        + (
            "PASS"
            if high_planar_pass
            else "FAIL"
        )
    )

    print(
        "INDEPENDENT_FORCE_GATE="
        + (
            "PASS"
            if independent_pass
            else "FAIL"
        )
    )

    # ------------------------------------------------------------
    # K. Decision.
    # ------------------------------------------------------------

    independent_solver_good = bool(
        (
            not scs_available
        )
        or (
            scs_objective_match
            and scs_full_postcheck
        )
    )

    record_candidate = bool(
        beats_006d
        and convergence_pass
        and width_pass
        and high_planar_pass
        and independent_pass
        and independent_solver_good
    )

    if record_candidate:

        decision = (
            "YELLOW_HIGH_PRIORITY_INTUITIVE_PLANAR_"
            "SOURCE_RECORD_CANDIDATE"
        )

        next_action = (
            "024C2_INDEPENDENT_HIGHER_RESOLUTION_AND_"
            "FINITE_PAYLOAD_CONFIRMATION_THEN_MICROSCOPIC_FIELD_MAPPING"
        )

    elif (
        beats_024c
        and convergence_pass
        and width_pass
        and high_planar_pass
        and independent_pass
    ):

        decision = (
            "YELLOW_INTUITIVE_PLANAR_ARCHITECTURE_"
            "IMPROVES_024C_BUT_NOT_006D"
        )

        next_action = (
            "ANALYZE_THREE_PIECE_STRESS_FLOW_AND_TEST_ONE_"
            "MINIMAL_MICROSCOPIC_REALIZABILITY_PREFILTER"
        )

    elif (
        high_planar_pass
        and convergence_pass
        and width_pass
        and independent_pass
    ):

        decision = (
            "YELLOW_DIRECTIONAL_PLANAR_MORPHOLOGY_ONLY_"
            "NO_EFFICIENCY_RECORD"
        )

        next_action = (
            "STOP_STATIC_SOURCE_COEFFICIENT_SEARCH_AND_RERANK_"
            "006D_MICROSCOPIC_REALIZATION_VS_ANALOGUE_ANTIGRAVITY"
        )

    else:

        decision = (
            "RED_INTUITIVE_GUARDED_STRESS_SANDWICH_"
            "DID_NOT_SURVIVE_PROMOTION_GATES"
        )

        next_action = (
            "STOP_024C_STATIC_SOURCE_SEARCH_AND_RERANK_"
            "006D_MICROSCOPIC_REALIZATION_VS_ANALOGUE_ANTIGRAVITY"
        )

    print(
        "\n=== K — 024C1 DECISION ==="
    )

    print(
        f"024C1_DECISION="
        f"{decision}"
    )

    print(
        f"NEXT="
        f"{next_action}"
    )

    print(
        "MICROSCOPIC_FIELD_REALIZATION=NO"
    )

    print(
        "NONLINEAR_GR=NO"
    )

    print(
        "PERFECT_PLANAR_GRAVITY_BEAM=NO"
    )

    print(
        "CURRENT_KNOWLEDGE_HEURISTIC="
        "70_TO_71_PERCENT_RETAIN_UNLESS_NEW_RECORD_EARNS_PROMOTION"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )

    # ------------------------------------------------------------
    # Persist.
    # ------------------------------------------------------------

    public = [
        public_row(
            row
        )
        for row in all_rows
    ]

    fields = sorted(
        {
            key
            for row in public
            for key in row.keys()
        }
    )

    with OUT_CASES.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
        )

        writer.writeheader()

        writer.writerows(
            public
        )

    if "_arrays" in high:

        arrays = high[
            "_arrays"
        ]

        payload = {
            key: np.asarray(
                value
            )
            for key, value in arrays.items()
        }

        if (
            "axial_hi"
            in independent
        ):

            payload[
                "independent_axial_hi"
            ] = np.asarray(
                independent[
                    "axial_hi"
                ]
            )

            payload[
                "independent_radial_hi"
            ] = np.asarray(
                independent[
                    "radial_hi"
                ]
            )

        payload[
            "sentinel_radii"
        ] = SENTINEL_RADII

        np.savez_compressed(
            OUT_NPZ,
            **payload,
        )

    summary = {
        "claim_classification":
            (
                "PROJECT_DERIVED_INTUITIVE_GUARDED_"
                "STRESS_SANDWICH_SOURCE_PREFILTER"
            ),

        "anchors": {
            "C_006D":
                C006D,

            "C_024C_conservative":
                PRIOR_024C_C,

            "024C_transverse_fraction":
                PRIOR_024C_TRANSVERSE,

            "024C_cancellation":
                PRIOR_024C_CANCELLATION,
        },

        "architecture": {
            "name":
                "GUARDED_STRESS_SANDWICH",

            "pieces": [
                "PAYLOAD_FACING_WORKING_FACE",
                "OUTER_GUARD_STRESS_RETURN",
                "BURIED_BACKPLANE",
            ],

            "strict_true_standoff":
                True,

            "local_conservation":
                True,

            "type_I_DEC":
                True,

            "external_support_omitted":
                False,
        },

        "selected_geometry": {
            "name":
                selected_spec.name,

            "top_radius":
                selected_spec.top_radius,

            "outer_radius":
                selected_spec.outer_radius,

            "depth":
                selected_spec.depth,

            "top_thickness":
                selected_spec.top_thickness,

            "guard_width":
                selected_spec.guard_width,

            "back_thickness":
                selected_spec.back_thickness,
        },

        "refinement": {
            "C_medium":
                c_medium,

            "C_high":
                c_high,

            "C_conservative":
                c_conservative,

            "C_relative_difference":
                c_rel,

            "point_C_high":
                point_high_c,

            "planarity_energy_premium":
                planarity_premium,

            "minimum_width_cells_high":
                width_high,
        },

        "high_planar": {
            key: value
            for key, value in public_row(
                high
            ).items()
        },

        "guided_high": {
            key: value
            for key, value in public_row(
                guided_high
            ).items()
        },

        "independent_vector": {
            key: (
                value.tolist()
                if isinstance(
                    value,
                    np.ndarray,
                )
                else value
            )
            for key, value in independent.items()
        },

        "independent_solver": {
            "SCS_available":
                scs_available,

            "SCS_C":
                scs_c,

            "objective_relative_difference":
                scs_rel,

            "objective_match":
                scs_objective_match,

            "full_postcheck":
                scs_full_postcheck,
        },

        "gates": {
            "coefficient_convergence":
                convergence_pass,

            "physical_width":
                width_pass,

            "planar":
                high_planar_pass,

            "independent_force":
                independent_pass,

            "cancellation_improved_vs_024C":
                cancellation_improved,

            "transverse_improved_vs_024C":
                transverse_improved,

            "beats_024C":
                beats_024c,

            "beats_006D":
                beats_006d,

            "record_candidate":
                record_candidate,
        },

        "decision":
            decision,

        "next":
            next_action,

        "claim_limits": [
            "NO_MICROSCOPIC_FIELD",
            "NO_FULL_DYNAMIC_STABILITY",
            "NO_NONLINEAR_GR",
            "NO_PERFECT_STATIC_GRAVITY_BEAM",
            "NO_1_OVER_G_SCALING_ESCAPE",
            "NO_EXPERIMENT",
            "NO_PRACTICAL_DEVICE",
        ],
    }

    OUT_SUMMARY.write_text(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
            allow_nan=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        f"SUMMARY_JSON="
        f"{OUT_SUMMARY.relative_to(ROOT)}"
    )

    print(
        f"CASES_CSV="
        f"{OUT_CASES.relative_to(ROOT)}"
    )

    if OUT_NPZ.is_file():

        print(
            f"SELECTED_NPZ="
            f"{OUT_NPZ.relative_to(ROOT)}"
        )

    print(
        "024C1_RUN_COMPLETE=YES"
    )


if __name__ == "__main__":
    main()
