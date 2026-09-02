#!/usr/bin/env python3
"""024C — teacher-guided planar stress-lens source discovery.

PURPOSE
-------
Construct and test a genuinely new static conserved-DEC stress architecture
whose design is guided by the completed Introspective mechanism-discovery
program rather than by modifying the 006D radial membrane profile.

The proposed architecture is called the:

    TEACHER-GUIDED PLANAR STRESS LENS

Its intended source organization is:

1. Place a compact, strongly tensile, near-DEC productive source region near
   the payload-facing side of a finite source.

2. Use the full axisymmetric static stress tensor

       p_r,
       p_z,
       p_phi,
       T_rz

   so compensating support stress can be routed both radially outward and
   vertically downward.

3. Place the compulsory positive active/support contribution farther from the
   payload, where the gravitational kernel is weaker.

4. Optimize not merely one axial point but a finite circular working plane.

5. Demand a relatively flat outward axial response across that plane and small
   transverse acceleration.

This is deliberately NOT the 006D ansatz.

006D remains the conservative reference coefficient:

    C_006D = 23.591586299249.

SCIENTIFIC QUESTION
-------------------
Can a fresh static, positive-energy, locally conserved, DEC-compatible
stress-energy architecture exploit the Introspective lessons

    compact productive stress,
    near-DEC operation,
    low cancellation,
    spatial kernel leverage,
    stress-dominated useful response,
    low-kernel placement of structural overhead

to beat 006D while producing a finite approximately planar outward-gravity
working region?

WHY THIS IS NOT "006D VERSION 2"
--------------------------------
006D uses a highly structured thin radial membrane architecture based on

    q(r) = r p_r(r)

with the support load transferred primarily in the radial direction and
terminated in a finite outer collar.

024C does not prescribe any 006D radial profile.

Instead it solves over a finite two-dimensional cylindrical slab with
independent stress degrees of freedom:

    energy density:
        e(r,z)

    azimuthal pressure:
        p_phi(r,z)

    radial face pressure:
        p_r(r,z)

    vertical face pressure:
        p_z(r,z)

    meridional shear:
        T_rz(r,z).

The source optimizer is therefore free to discover a qualitatively different
three-dimensional stress-routing architecture.

INTROSPECTIVE LESSONS USED
--------------------------
The completed Introspective branch established as durable design information:

- useful source influence can be extremely concentrated;
- productive source placement near a high-leverage payload kernel matters
  enormously;
- approximately 59 percent of the teacher's net response came from spatial
  stress rather than energy density alone;
- the teacher operated close to the DEC stress boundary;
- useful response need not result from extreme positive/negative cancellation;
- structural/scaffolding energy should preferentially occupy low-kernel
  regions;
- the old raw ~17230x teacher is a design diagnostic, not a certified
  continuum source or microscopic field.

For a strict one-sided stand-off source with all matter below the target plane,
the sign must be adapted.

The point-target kernel below the target is negative:

    K_z < 0.

Therefore useful outward acceleration requires locally negative weighted active
source:

    S
      =
    e + p_r + p_z + p_phi
      <
    0

in the high-leverage region.

For type-I DEC:

    -e <= lambda_i <= e

and consequently:

    -2e <= S <= 4e.

Thus the ideal productive tensile limit for the stand-off geometry is

    S/e -> -2,

not the positive S/e~2.65 anatomy of the old source-centered teacher.

The transferable lesson is therefore:

    NEAR-DEC STRESS LEVERAGE

rather than:

    COPY THE OLD TEACHER SIGN.

PLANAR WORKING-REGION OBSERVABLE
--------------------------------
The source occupies

    0 <= r <= R,
    -D <= z <= 0.

The nominal working plane is

    z = h = 1.

Instead of optimizing acceleration at one axial point, define a circular
working aperture

    0 <= s <= A,

where s is transverse distance from the symmetry axis.

The primary objective uses the area-average axial acceleration across the
disk:

    <a_z>_disk
      =
    (2/A^2)
    integral_0^A s a_z(s,h) ds.

The optimization normalizes

    <a_z>_disk >= 1.

The source coefficient is then

    C_planar
      =
    E / <a_z>_disk

in the same h=1 weak-field normalization used by the project's source-level
comparators.

Because the optimizer enforces approximately unit disk-average response, the
reported energy is directly the effective coefficient.

PLANARITY / DIRECTIONALITY METRICS
----------------------------------
After optimization, independently reconstruct the vector acceleration at
multiple target radii across the working plane.

Require and report:

    MIN_AXIAL_ACCELERATION

    MAX_AXIAL_ACCELERATION

    PLANAR_FLATNESS
        =
    (max a_z - min a_z) / mean a_z

    EDGE_TO_CENTER_AXIAL_RATIO

    MAX_TRANSVERSE_FRACTION
        =
    max |a_r| / |a_z|.

A good planar source should have:

    every sentinel a_z > 0,

    PLANAR_FLATNESS <= 0.15,

    MAX_TRANSVERSE_FRACTION <= 0.15.

These thresholds are deliberately demanding but are only source-design gates.

STATIC GR CANNOT FORM A PERFECT GRAVITY BEAM
--------------------------------------------
The source-free gravitational potential obeys Laplace's equation.

Therefore a static finite source cannot create a field that is exactly
nonzero only on one plane or exactly confined like a collimated material beam.

024C tests a finite working-plane plateau and directionality, not perfect
field confinement.

FINITE-PAYLOAD INTERPRETATION
-----------------------------
Every target sentinel lies in a source-free region.

For a sufficiently small uniform spherical payload centered at any sentinel,
the acceleration components are harmonic inside the payload ball.

The mean-value theorem then gives

    a_CM
      =
    a(center).

Thus these sentinel accelerations also describe finite spherical payload
center-of-mass acceleration whenever the payload ball remains source-free.

LOCAL CONSERVATION
------------------
Use the already audited staggered finite-volume static equations:

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

Vacuum boundaries have zero traction.

ENERGY CONDITIONS
-----------------
The cell-centered spatial stress tensor is

    [[p_r, T_rz, 0],
     [T_rz, p_z, 0],
     [0, 0, p_phi]].

Its principal stresses lambda_i must obey

    |lambda_i| <= e.

This is the type-I dominant energy condition.

The inherited solver also independently checks local conservation, Laue
balance, total active mass, and DEC after optimization.

POSITIVE FAR-FIELD ACTIVE MASS
------------------------------
For a compact static locally conserved source, the Laue integral gives

    integral T_ii dV = 0.

Therefore

    integral S dV
      =
    integral e dV
      >
    0.

A green source therefore retains positive total far-field active mass.

NEW MECHANISM HYPOTHESIS
------------------------
The hypothesis being tested is:

    BURIED THREE-DIMENSIONAL STRESS RETURN.

A near-top productive tensile region may create the useful outward effect.

The stresses necessary to conserve it may then be routed:

    radially outward

and

    vertically downward

into a lower-kernel region.

This provides a new degree of geometric leverage unavailable to a strictly
thin radial stress-transfer architecture.

The run explicitly compares different source depths to determine whether this
vertical separation produces a measurable efficiency advantage.

SOURCE GEOMETRY SEARCH
----------------------
Primary physically motivated one-sided slabs:

    R/h:
        approximately 2.5 to 5

    depth/h:
        approximately 0.25 to 1.25.

The geometry scan is intentionally small.

Its purpose is to determine whether the new mechanism exists, not to perform
another enormous relaxed-source coefficient search.

The selected geometry is refined at two higher resolutions.

BLIND WILDCARD CHECK
--------------------
The values

    0.625
    1.6
    1.875
    3.125
    5

are also included in explicitly labeled diagnostic geometries.

They are:

    NOT physics priors,
    NOT optimization targets,
    NOT promotion evidence.

They are kept separate from the physically motivated selection.

VALIDATION
----------
Before new science:

1. The repository's 94 known-solution tests must pass.

2. The inherited full finite-volume solver must independently reproduce the
   known 006B finite-volume positive control.

For the selected 024C solution:

3. Rebuild the entire disk-averaged force with a separate higher-order
   off-axis kernel quadrature.

4. Independently evaluate multiple off-axis vector-force sentinels.

5. Check coefficient convergence between the two refinement levels.

6. Check physical participation widths against grid spacing.

7. If SCS is installed, independently re-solve the medium-resolution selected
   case and compare its coefficient with CLARABEL.

TEACHER-ANATOMY DIAGNOSTICS
---------------------------
For the selected source report:

    A_rho

    A_stress

    stress fraction of net useful response

    force-weighted median S/e

    DEC saturation

    cancellation factor

    F90 energy fraction

    F90 weighted mean r/h

    F90 weighted mean z/h.

This tests whether the optimizer independently converges toward the durable
Introspective design principles.

PROMOTION CONDITIONS
--------------------
024C is a high-priority new source-record candidate only if:

- medium and high refinements are green;
- independent disk-force reconstruction passes;
- coefficient relative difference <= 15 percent;
- minimum high-resolution participation width >= 3 cells;
- every working-plane sentinel accelerates outward;
- planar flatness <= 15 percent;
- maximum transverse acceleration fraction <= 15 percent;
- conservative coefficient beats finite 006D;
- independent SCS check passes if SCS is available.

Even then the correct classification is:

    NEW CONSERVED-DEC PLANAR SOURCE CANDIDATE

not:

    MICROSCOPIC FIELD,
    EXPERIMENT,
    DEVICE,
    NEW PHYSICS.

FALSIFIERS
----------
The mechanism is demoted if:

- depth does not improve the result relative to shallower source geometries;
- good coefficients require grid-scale concentration;
- working-plane response becomes highly nonuniform;
- transverse force is comparable to axial force;
- coefficient does not beat 006D after refinement;
- conservation or DEC fails;
- independent force reconstruction disagrees;
- independent solver materially disagrees.

STOP RULE
---------
If no physically motivated geometry provides a converged improvement over
006D, do not launch a large source scan.

Conclude:

    BURIED_STRESS_RETURN_DID_NOT_BEAT_006D_IN_TESTED_CLASS.

If a robust improvement is found, the next step is NOT more coefficient
polishing.

The next step is:

    identify the simplest microscopic field theory capable of producing the
    discovered stress anatomy.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_TEACHER_GUIDED_PLANAR_CONSERVED_DEC_SOURCE_DISCOVERY_SCOUT

DOES NOT ESTABLISH
------------------
- microscopic realizability;
- field stability;
- nonlinear Einstein-matter continuation;
- perfect gravitational collimation;
- practical energy scaling;
- experimental antigravity;
- a practical device.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
from pathlib import Path
import sys
from typing import Any

import numpy as np
from numpy.polynomial.legendre import leggauss


ROOT = Path(__file__).resolve().parents[1]

SIM_DIR = ROOT / "simulations"
DATA_DIR = ROOT / "results/data"

INT14A_SUMMARY = (
    DATA_DIR
    / "int14a_conservation_aware_constructive_headroom_summary.json"
)

INT15_SUMMARY = (
    DATA_DIR
    / "int15_static_pulse_successor_blueprint_summary.json"
)

INT14B_SOURCE = (
    SIM_DIR
    / "int14b_support_constrained_structural_overhead_bridge.py"
)

INT14C_SOURCE = (
    SIM_DIR
    / "int14c_thousandfold_uv_regular_source_verification.py"
)

OUT_SUMMARY = (
    DATA_DIR
    / "024c_teacher_guided_planar_stress_lens_summary.json"
)

OUT_CASES = (
    DATA_DIR
    / "024c_teacher_guided_planar_stress_lens_cases.csv"
)

OUT_NPZ = (
    DATA_DIR
    / "024c_teacher_guided_planar_stress_lens_selected.npz"
)


C006D = 23.591586299249
C006B_THIN = 23.426710175391
C006B_FINITE20 = 32.95475466694425

TARGET_Z = 1.0
PRIMARY_APERTURE = 0.50

COARSE_NR = 10
COARSE_NZ = 6

MEDIUM_NR = 14
MEDIUM_NZ = 8

HIGH_NR = 18
HIGH_NZ = 10

C_CONVERGENCE_TOL = 0.15
MIN_WIDTH_CELLS = 3.0

MAX_PLANAR_FLATNESS = 0.15
MAX_TRANSVERSE_FRACTION = 0.15

INDEPENDENT_FORCE_REL_TOL = 5.0e-4
SCS_C_REL_TOL = 0.05

OPT_CELL_ORDER = 4
OPT_NPHI = 16
OPT_TARGET_ORDER = 5

HI_CELL_ORDER = 7
HI_NPHI = 48
HI_TARGET_ORDER = 9

SENTINEL_COUNT = 9


def require(path: Path) -> None:
    """Require one upstream artifact."""

    if not path.is_file():
        raise RuntimeError(
            f"Required file missing: {path}"
        )


def load_module(
    name: str,
    path: Path,
):
    """Import a repository simulation module without invoking main()."""

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


def relative_error(
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


def first_finite(
    *values: Any,
) -> float:
    """Return first finite float-like value."""

    for value in values:

        try:
            x = float(
                value
            )
        except Exception:
            continue

        if math.isfinite(
            x
        ):
            return x

    raise RuntimeError(
        "No finite candidate value."
    )


def weighted_median(
    values: np.ndarray,
    weights: np.ndarray,
) -> float:
    """Weighted median of finite positive-weight samples."""

    v = np.asarray(
        values,
        dtype=float,
    ).ravel()

    w = np.asarray(
        weights,
        dtype=float,
    ).ravel()

    good = (
        np.isfinite(v)
        &
        np.isfinite(w)
        &
        (
            w
            > 0.0
        )
    )

    if not np.any(
        good
    ):
        return float(
            "nan"
        )

    v = v[
        good
    ]

    w = w[
        good
    ]

    order = np.argsort(
        v
    )

    v = v[
        order
    ]

    w = w[
        order
    ]

    cumulative = np.cumsum(
        w
    )

    index = int(
        np.searchsorted(
            cumulative,
            0.5
            * cumulative[
                -1
            ],
            side="left",
        )
    )

    index = min(
        index,
        len(v) - 1,
    )

    return float(
        v[
            index
        ]
    )


def vector_cell_kernel(
    r0: float,
    r1: float,
    z0: float,
    z1: float,
    target_r: float,
    target_z: float,
    *,
    order: int,
    nphi: int,
) -> tuple[
    float,
    float,
]:
    """Integrate radial and axial Newtonian kernel over one axisymmetric cell.

    The target is placed at azimuth phi=0 without loss of generality.

    Returned components use the same dimensionless sign convention as the
    existing repository finite-volume axial kernel:

        source below target -> K_z < 0.

    Multiplying K by the active source density therefore gives the signed
    acceleration functional used by the source optimizer.
    """

    gx, gw = leggauss(
        order
    )

    r_mid = (
        0.5
        * (
            r0
            + r1
        )
    )

    r_half = (
        0.5
        * (
            r1
            - r0
        )
    )

    z_mid = (
        0.5
        * (
            z0
            + z1
        )
    )

    z_half = (
        0.5
        * (
            z1
            - z0
        )
    )

    rr = (
        r_mid
        + r_half
        * gx
    )

    rw = (
        r_half
        * gw
    )

    zz = (
        z_mid
        + z_half
        * gx
    )

    zw = (
        z_half
        * gw
    )

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

    sinphi = np.sin(
        phi
    )

    phi_weight = (
        2.0
        * math.pi
        / nphi
    )

    kr = 0.0
    kz = 0.0

    for r, wr in zip(
        rr,
        rw,
    ):

        x_source = (
            r
            * cosphi
        )

        y_source = (
            r
            * sinphi
        )

        dx = (
            x_source
            - target_r
        )

        dy = y_source

        for z, wz in zip(
            zz,
            zw,
        ):

            dz = (
                z
                - target_z
            )

            d2 = (
                dx
                * dx
                + dy
                * dy
                + dz
                * dz
            )

            inv_d3 = (
                d2
                ** -1.5
            )

            common = (
                float(
                    wr
                )
                * float(
                    wz
                )
                * float(
                    r
                )
                * phi_weight
            )

            kr += (
                common
                * float(
                    np.sum(
                        dx
                        * inv_d3
                    )
                )
            )

            kz += (
                common
                * float(
                    np.sum(
                        dz
                        * inv_d3
                    )
                )
            )

    return (
        kr,
        kz,
    )


def disk_target_nodes(
    aperture: float,
    order: int,
) -> tuple[
    np.ndarray,
    np.ndarray,
]:
    """Area-uniform radial quadrature nodes for a circular target disk.

    Uniform disk area corresponds to uniform u=s^2/A^2 on [0,1].
    """

    if aperture <= 0.0:
        return (
            np.array(
                [0.0],
                dtype=float,
            ),
            np.array(
                [1.0],
                dtype=float,
            ),
        )

    gx, gw = leggauss(
        order
    )

    u = (
        0.5
        * (
            gx
            + 1.0
        )
    )

    weights = (
        0.5
        * gw
    )

    radii = (
        aperture
        * np.sqrt(
            u
        )
    )

    return (
        radii,
        weights,
    )


def cell_disk_average_axial_kernel(
    r0: float,
    r1: float,
    z0: float,
    z1: float,
    *,
    aperture: float,
    target_z: float,
    cell_order: int,
    nphi: int,
    target_order: int,
) -> float:
    """Disk-area-averaged axial kernel for one source cell."""

    radii, weights = (
        disk_target_nodes(
            aperture,
            target_order,
        )
    )

    total = 0.0

    for target_r, weight in zip(
        radii,
        weights,
    ):

        _kr, kz = vector_cell_kernel(
            r0,
            r1,
            z0,
            z1,
            float(
                target_r
            ),
            target_z,
            order=cell_order,
            nphi=nphi,
        )

        total += (
            float(
                weight
            )
            * kz
        )

    return float(
        total
    )


def build_planar_geometry(
    case,
    *,
    aperture: float,
    cell_order: int,
    nphi: int,
    target_order: int,
):
    """Build one rectangular one-sided stress-lens finite-volume geometry."""

    r_edges = np.linspace(
        0.0,
        case.radius,
        case.nr + 1,
    )

    z_edges = np.linspace(
        case.zmin,
        case.zmax,
        case.nz + 1,
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

    volumes = np.zeros(
        (
            case.nr,
            case.nz,
        ),
        dtype=float,
    )

    kernels = np.zeros_like(
        volumes
    )

    for i in range(
        case.nr
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
            case.nz
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

            kernels[
                i,
                j,
            ] = (
                cell_disk_average_axial_kernel(
                    r0,
                    r1,
                    z0,
                    z1,
                    aperture=aperture,
                    target_z=case.target_z,
                    cell_order=cell_order,
                    nphi=nphi,
                    target_order=target_order,
                )
            )

    active_mask = np.ones(
        (
            case.nr,
            case.nz,
        ),
        dtype=bool,
    )

    return (
        r_edges,
        z_edges,
        r_centers,
        z_centers,
        volumes,
        kernels,
        active_mask,
    )


def solve_planar_case(
    int14b,
    int14c,
    case,
    *,
    aperture: float,
    solver_override: str | None = None,
) -> dict[str, Any]:
    """Solve with a temporary disk-average kernel geometry."""

    original = (
        int14b.build_geometry
    )

    def custom_geometry(
        supplied_case,
    ):
        return build_planar_geometry(
            supplied_case,
            aperture=aperture,
            cell_order=OPT_CELL_ORDER,
            nphi=OPT_NPHI,
            target_order=OPT_TARGET_ORDER,
        )

    int14b.build_geometry = (
        custom_geometry
    )

    try:
        row = (
            int14c.solve_diagnostic_case(
                int14b,
                case,
                solver_override=solver_override,
            )
        )
    finally:
        int14b.build_geometry = (
            original
        )

    return row


def make_case(
    int14b,
    name: str,
    *,
    nr: int,
    nz: int,
    radius: float,
    depth: float,
    payload_radius: float,
    category: str,
):
    """Construct a one-sided rectangular stress-lens source."""

    return int14b.SupportCase(
        name=name,
        nr=nr,
        nz=nz,
        radius=radius,
        zmin=-depth,
        zmax=0.0,
        target_z=TARGET_Z,
        payload_radius=payload_radius,
        spherical_mask=False,
        reflection_symmetry=False,
        category=category,
    )


def high_order_kernel_arrays(
    arrays: dict[str, np.ndarray],
    *,
    target_r: float,
    target_z: float,
) -> tuple[
    np.ndarray,
    np.ndarray,
]:
    """Independent high-order vector kernel arrays for one target point."""

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

    shape = np.asarray(
        arrays[
            "active_density"
        ]
    ).shape

    kr = np.zeros(
        shape,
        dtype=float,
    )

    kz = np.zeros(
        shape,
        dtype=float,
    )

    for i in range(
        shape[
            0
        ]
    ):

        for j in range(
            shape[
                1
            ]
        ):

            kr[
                i,
                j,
            ], kz[
                i,
                j,
            ] = vector_cell_kernel(
                float(
                    r_edges[
                        i
                    ]
                ),
                float(
                    r_edges[
                        i + 1
                    ]
                ),
                float(
                    z_edges[
                        j
                    ]
                ),
                float(
                    z_edges[
                        j + 1
                    ]
                ),
                target_r,
                target_z,
                order=HI_CELL_ORDER,
                nphi=HI_NPHI,
            )

    return (
        kr,
        kz,
    )


def high_order_disk_average_kernel(
    arrays: dict[str, np.ndarray],
    *,
    aperture: float,
    target_z: float,
) -> np.ndarray:
    """Independent high-order disk-average axial kernel array."""

    radii, weights = (
        disk_target_nodes(
            aperture,
            HI_TARGET_ORDER,
        )
    )

    active_shape = np.asarray(
        arrays[
            "active_density"
        ]
    ).shape

    total = np.zeros(
        active_shape,
        dtype=float,
    )

    for target_r, weight in zip(
        radii,
        weights,
    ):

        _kr, kz = (
            high_order_kernel_arrays(
                arrays,
                target_r=float(
                    target_r
                ),
                target_z=target_z,
            )
        )

        total += (
            float(
                weight
            )
            * kz
        )

    return total


def planar_diagnostics(
    row: dict[str, Any],
    *,
    aperture: float,
) -> dict[str, Any]:
    """Independent vector-force and teacher-anatomy reconstruction."""

    arrays = row.get(
        "_arrays"
    )

    if arrays is None:
        raise RuntimeError(
            "Selected source row has no arrays."
        )

    active_density = np.asarray(
        arrays[
            "active_density"
        ],
        dtype=float,
    )

    e = np.asarray(
        arrays[
            "e"
        ],
        dtype=float,
    )

    pr = np.asarray(
        arrays[
            "pr"
        ],
        dtype=float,
    )

    pz = np.asarray(
        arrays[
            "pz"
        ],
        dtype=float,
    )

    pphi = np.asarray(
        arrays[
            "pphi"
        ],
        dtype=float,
    )

    volumes = np.asarray(
        arrays[
            "volumes"
        ],
        dtype=float,
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

    sentinel_radii = np.linspace(
        0.0,
        aperture,
        SENTINEL_COUNT,
    )

    axial = []
    radial = []

    for target_r in sentinel_radii:

        kr, kz = (
            high_order_kernel_arrays(
                arrays,
                target_r=float(
                    target_r
                ),
                target_z=TARGET_Z,
            )
        )

        radial.append(
            float(
                np.sum(
                    kr
                    * active_density
                )
            )
        )

        axial.append(
            float(
                np.sum(
                    kz
                    * active_density
                )
            )
        )

    axial_a = np.asarray(
        axial,
        dtype=float,
    )

    radial_a = np.asarray(
        radial,
        dtype=float,
    )

    mean_axial = float(
        np.mean(
            axial_a
        )
    )

    min_axial = float(
        np.min(
            axial_a
        )
    )

    max_axial = float(
        np.max(
            axial_a
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
                mean_axial
            ),
            1.0e-300,
        )
    )

    transverse_fraction = float(
        np.max(
            np.abs(
                radial_a
            )
            /
            np.maximum(
                np.abs(
                    axial_a
                ),
                1.0e-300,
            )
        )
    )

    edge_to_center = (
        float(
            axial_a[
                -1
            ]
            /
            axial_a[
                0
            ]
        )
        if abs(
            axial_a[
                0
            ]
        )
        > 1.0e-300
        else float(
            "nan"
        )
    )

    # Completely independent disk-average force.
    kernels_hi = (
        high_order_disk_average_kernel(
            arrays,
            aperture=aperture,
            target_z=TARGET_Z,
        )
    )

    acceleration_hi = float(
        np.sum(
            kernels_hi
            * active_density
        )
    )

    acceleration_base = float(
        row[
            "acceleration"
        ]
    )

    force_relerr = relative_error(
        acceleration_hi,
        acceleration_base,
    )

    force_pass = bool(
        acceleration_hi
        > 0.0
        and force_relerr
        <= INDEPENDENT_FORCE_REL_TOL
    )

    # Backside directional leakage diagnostic.
    backside_z = (
        float(
            z_edges[
                0
            ]
        )
        - TARGET_Z
    )

    kernels_back = (
        high_order_disk_average_kernel(
            arrays,
            aperture=aperture,
            target_z=backside_z,
        )
    )

    backside_axial = float(
        np.sum(
            kernels_back
            * active_density
        )
    )

    front_to_back_abs_ratio = (
        abs(
            acceleration_hi
        )
        /
        max(
            abs(
                backside_axial
            ),
            1.0e-300,
        )
    )

    # Axial persistence one-half h beyond the nominal plane.
    kernels_far = (
        high_order_disk_average_kernel(
            arrays,
            aperture=aperture,
            target_z=1.5,
        )
    )

    far_axial = float(
        np.sum(
            kernels_far
            * active_density
        )
    )

    far_over_working = (
        far_axial
        /
        acceleration_hi
        if abs(
            acceleration_hi
        )
        > 1.0e-300
        else float(
            "nan"
        )
    )

    # Teacher-style anatomy on the high-order working-plane kernel.
    cell_energy = (
        e
        * volumes
    )

    cell_force = (
        active_density
        * kernels_hi
    )

    outward = np.maximum(
        cell_force,
        0.0,
    )

    opposing = np.maximum(
        -cell_force,
        0.0,
    )

    gross_outward = float(
        np.sum(
            outward
        )
    )

    gross_opposing = float(
        np.sum(
            opposing
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
                acceleration_hi
            ),
            1.0e-300,
        )
    )

    a_rho = float(
        np.sum(
            e
            * kernels_hi
        )
    )

    stress_trace = (
        pr
        + pz
        + pphi
    )

    a_stress = float(
        np.sum(
            stress_trace
            * kernels_hi
        )
    )

    stress_fraction = (
        a_stress
        /
        acceleration_hi
        if abs(
            acceleration_hi
        )
        > 1.0e-300
        else float(
            "nan"
        )
    )

    s_over_e = np.full_like(
        e,
        np.nan,
        dtype=float,
    )

    nonzero = (
        e
        > max(
            float(
                np.max(
                    e
                )
            ),
            1.0,
        )
        * 1.0e-15
    )

    s_over_e[
        nonzero
    ] = (
        active_density[
            nonzero
        ]
        /
        e[
            nonzero
        ]
    )

    force_weighted_median_s_over_e = (
        weighted_median(
            s_over_e,
            outward,
        )
    )

    # F90 productive skeleton by leverage.
    energy_flat = np.maximum(
        cell_energy.ravel(),
        0.0,
    )

    outward_flat = np.maximum(
        outward.ravel(),
        0.0,
    )

    leverage = np.zeros_like(
        energy_flat
    )

    good = (
        energy_flat
        > max(
            float(
                np.max(
                    energy_flat
                )
            ),
            1.0,
        )
        * 1.0e-15
    )

    leverage[
        good
    ] = (
        outward_flat[
            good
        ]
        /
        energy_flat[
            good
        ]
    )

    order = np.argsort(
        leverage
    )[::-1]

    cumulative = np.cumsum(
        outward_flat[
            order
        ]
    )

    total_outward = float(
        cumulative[
            -1
        ]
    )

    if total_outward > 0.0:

        cut = int(
            np.searchsorted(
                cumulative,
                0.90
                * total_outward,
                side="left",
            )
        )

        cut = min(
            cut,
            len(order) - 1,
        )

        chosen = order[
            : cut + 1
        ]

        f90_energy_fraction = (
            float(
                np.sum(
                    energy_flat[
                        chosen
                    ]
                )
            )
            /
            max(
                float(
                    np.sum(
                        energy_flat
                    )
                ),
                1.0e-300,
            )
        )

        selected_weight = (
            outward_flat[
                chosen
            ]
        )

        r_flat = R.ravel()
        z_flat = Z.ravel()

        f90_r_mean = (
            float(
                np.sum(
                    r_flat[
                        chosen
                    ]
                    * selected_weight
                )
            )
            /
            max(
                float(
                    np.sum(
                        selected_weight
                    )
                ),
                1.0e-300,
            )
        )

        f90_z_mean = (
            float(
                np.sum(
                    z_flat[
                        chosen
                    ]
                    * selected_weight
                )
            )
            /
            max(
                float(
                    np.sum(
                        selected_weight
                    )
                ),
                1.0e-300,
            )
        )

    else:

        f90_energy_fraction = float(
            "nan"
        )

        f90_r_mean = float(
            "nan"
        )

        f90_z_mean = float(
            "nan"
        )

    dec_ratio = np.asarray(
        arrays.get(
            "dec_ratio",
            np.full_like(
                e,
                np.nan,
            ),
        ),
        dtype=float,
    )

    max_dec_saturation = float(
        np.nanmax(
            dec_ratio
        )
    )

    all_outward = bool(
        min_axial
        > 0.0
    )

    planar_pass = bool(
        all_outward
        and flatness
        <= MAX_PLANAR_FLATNESS
        and transverse_fraction
        <= MAX_TRANSVERSE_FRACTION
    )

    return {
        "sentinel_radii":
            sentinel_radii,

        "sentinel_axial":
            axial_a,

        "sentinel_radial":
            radial_a,

        "independent_disk_kernel":
            kernels_hi,

        "independent_disk_acceleration":
            acceleration_hi,

        "base_disk_acceleration":
            acceleration_base,

        "independent_force_relative_error":
            force_relerr,

        "independent_force_pass":
            force_pass,

        "minimum_axial":
            min_axial,

        "maximum_axial":
            max_axial,

        "mean_sentinel_axial":
            mean_axial,

        "planar_flatness":
            flatness,

        "edge_to_center_axial_ratio":
            edge_to_center,

        "max_transverse_fraction":
            transverse_fraction,

        "all_sentinels_outward":
            all_outward,

        "planar_pass":
            planar_pass,

        "backside_target_z":
            backside_z,

        "backside_disk_axial":
            backside_axial,

        "front_to_back_abs_ratio":
            front_to_back_abs_ratio,

        "far_plane_z":
            1.5,

        "far_plane_disk_axial":
            far_axial,

        "far_over_working":
            far_over_working,

        "A_rho":
            a_rho,

        "A_stress":
            a_stress,

        "stress_fraction":
            stress_fraction,

        "gross_outward":
            gross_outward,

        "gross_opposing":
            gross_opposing,

        "cancellation":
            cancellation,

        "force_weighted_median_S_over_e":
            force_weighted_median_s_over_e,

        "max_DEC_saturation":
            max_dec_saturation,

        "F90_energy_fraction":
            f90_energy_fraction,

        "F90_r_mean":
            f90_r_mean,

        "F90_z_mean":
            f90_z_mean,
    }


def public_row(
    row: dict[str, Any],
    *,
    radius: float,
    depth: float,
    aperture: float,
    category: str,
    resolution: str,
) -> dict[str, Any]:
    """Strip private arrays and attach geometry metadata."""

    clean = {
        key: value
        for key, value
        in row.items()
        if key != "_arrays"
    }

    clean.update({
        "radius_over_h":
            radius,

        "depth_over_h":
            depth,

        "aperture_over_h":
            aperture,

        "category":
            category,

        "resolution_label":
            resolution,
    })

    return clean


def print_case(
    label: str,
    row: dict[str, Any],
) -> None:
    """Print one compact solver result."""

    print(
        f"024C_CASE={label} "
        f"C={float(row.get('coefficient', float('nan'))):.12e} "
        f"A={float(row.get('acceleration', float('nan'))):+.12e} "
        f"GREEN={'YES' if bool(row.get('green', False)) else 'NO'} "
        f"DEC={float(row.get('max_dec_violation', float('nan'))):.3e} "
        f"CONS={float(row.get('max_conservation_residual', float('nan'))):.3e} "
        f"CANCEL={float(row.get('cancellation', float('nan'))):.6e}",
        flush=True,
    )


def main() -> None:
    """Execute 024C."""

    print(
        "=== 024C TEACHER-GUIDED PLANAR STRESS LENS ===",
        flush=True,
    )

    for path in (
        INT14A_SUMMARY,
        INT14B_SOURCE,
        INT14C_SOURCE,
    ):
        require(
            path
        )

    prior = json.loads(
        INT14A_SUMMARY.read_text(
            encoding="utf-8"
        )
    )

    if INT15_SUMMARY.is_file():
        teacher = json.loads(
            INT15_SUMMARY.read_text(
                encoding="utf-8"
            )
        )
    else:
        teacher = {}

    payload_radius = first_finite(
        prior.get(
            "finite_payload_match",
            {},
        ).get(
            "payload_radius_over_h"
        ),
        prior.get(
            "current_exact_map",
            {},
        ).get(
            "payload_radius_over_h"
        ),
    )

    current_b7_c = first_finite(
        prior[
            "current_exact_map"
        ][
            "C"
        ]
    )

    int14b = load_module(
        "ag024c_int14b",
        INT14B_SOURCE,
    )

    int14c = load_module(
        "ag024c_int14c",
        INT14C_SOURCE,
    )

    print(
        "\n=== A — FIXED ANCHORS ==="
    )

    print(
        f"C_006D="
        f"{C006D:.15f}"
    )

    print(
        f"C_006B_THIN="
        f"{C006B_THIN:.15f}"
    )

    print(
        f"B7_C="
        f"{current_b7_c:.15f}"
    )

    print(
        f"PAYLOAD_RADIUS_OVER_H="
        f"{payload_radius:.15f}"
    )

    print(
        f"PRIMARY_WORKING_APERTURE_OVER_H="
        f"{PRIMARY_APERTURE:.15f}"
    )

    if teacher:

        try:
            teacher_c = float(
                teacher[
                    "teacher"
                ][
                    "coefficient"
                ]
            )

            print(
                f"RAW_TEACHER_C_DIAGNOSTIC="
                f"{teacher_c:.15e}"
            )

        except Exception:
            pass

    print(
        "RAW_TEACHER_USED_AS_CERTIFIED_SOURCE=NO"
    )

    print(
        "SOURCE_STRICTLY_Z_LE_ZERO=YES"
    )

    print(
        "PLANAR_PERFECT_STATIC_CONFINEMENT_CLAIM=NO"
    )

    # ------------------------------------------------------------
    # B. Recover inherited finite-volume solver against known 006B.
    # ------------------------------------------------------------

    print(
        "\n=== B — INHERITED SOLVER POSITIVE CONTROL ===",
        flush=True,
    )

    recovery_case = (
        int14b.SupportCase(
            name=(
                "024C_RECOVERY_006B_KNOWN_THIN20"
            ),
            nr=20,
            nz=2,
            radius=5.0,
            zmin=-0.125,
            zmax=0.0,
            target_z=1.0,
            payload_radius=payload_radius,
            spherical_mask=False,
            reflection_symmetry=False,
            category="VALIDATION",
        )
    )

    recovery = (
        int14c.solve_diagnostic_case(
            int14b,
            recovery_case,
        )
    )

    recovery_c = float(
        recovery.get(
            "coefficient",
            float(
                "nan"
            ),
        )
    )

    recovery_rel = relative_error(
        recovery_c,
        C006B_FINITE20,
    )

    recovery_pass = bool(
        recovery.get(
            "green",
            False,
        )
        and recovery_rel
        <= 3.0e-3
    )

    print(
        f"RECOVERY_006B_C="
        f"{recovery_c:.15e}"
    )

    print(
        f"RECOVERY_006B_EXPECTED="
        f"{C006B_FINITE20:.15e}"
    )

    print(
        f"RECOVERY_006B_RELERR="
        f"{recovery_rel:.15e}"
    )

    print(
        "RECOVERY_006B="
        + (
            "PASS"
            if recovery_pass
            else "FAIL"
        )
    )

    if not recovery_pass:
        raise RuntimeError(
            "Inherited finite-volume solver failed 006B positive control."
        )

    # ------------------------------------------------------------
    # C. Small physically motivated geometry matrix.
    # ------------------------------------------------------------

    print(
        "\n=== C — PHYSICAL PLANAR-STRESS-LENS GEOMETRY SCOUT ===",
        flush=True,
    )

    physical_specs = [
        (
            2.50,
            0.25,
        ),
        (
            2.50,
            0.625,
        ),
        (
            3.125,
            0.25,
        ),
        (
            3.125,
            0.625,
        ),
        (
            3.125,
            1.00,
        ),
        (
            4.00,
            0.25,
        ),
        (
            4.00,
            0.625,
        ),
        (
            4.00,
            1.00,
        ),
        (
            4.00,
            1.25,
        ),
        (
            5.00,
            0.625,
        ),
        (
            5.00,
            1.25,
        ),
    ]

    wildcard_specs = [
        (
            1.875,
            0.625,
        ),
        (
            3.125,
            1.6,
        ),
        (
            5.0,
            0.625,
        ),
    ]

    rows_public: list[
        dict[str, Any]
    ] = []

    physical_solutions: list[
        tuple[
            float,
            float,
            Any,
            dict[str, Any],
        ]
    ] = []

    wildcard_solutions: list[
        tuple[
            float,
            float,
            Any,
            dict[str, Any],
        ]
    ] = []

    for index, (
        radius,
        depth,
    ) in enumerate(
        physical_specs
    ):

        name = (
            f"024C_PHYSICAL_{index:02d}_"
            f"R{radius:.3f}_D{depth:.3f}"
        ).replace(
            ".",
            "P",
        )

        case = make_case(
            int14b,
            name,
            nr=COARSE_NR,
            nz=COARSE_NZ,
            radius=radius,
            depth=depth,
            payload_radius=payload_radius,
            category=(
                "PHYSICALLY_MOTIVATED_GEOMETRY"
            ),
        )

        print(
            f"024C_SOLVE_BEGIN={name} "
            f"GRID={COARSE_NR}x{COARSE_NZ} "
            f"R={radius:.6f} "
            f"D={depth:.6f}",
            flush=True,
        )

        row = solve_planar_case(
            int14b,
            int14c,
            case,
            aperture=PRIMARY_APERTURE,
        )

        print_case(
            name,
            row,
        )

        rows_public.append(
            public_row(
                row,
                radius=radius,
                depth=depth,
                aperture=PRIMARY_APERTURE,
                category=(
                    "PHYSICALLY_MOTIVATED_GEOMETRY"
                ),
                resolution="COARSE",
            )
        )

        physical_solutions.append(
            (
                radius,
                depth,
                case,
                row,
            )
        )

    print(
        "\n=== D — BLIND WILDCARD DIAGNOSTICS ===",
        flush=True,
    )

    for index, (
        radius,
        depth,
    ) in enumerate(
        wildcard_specs
    ):

        name = (
            f"024C_WILDCARD_{index:02d}_"
            f"R{radius:.3f}_D{depth:.3f}"
        ).replace(
            ".",
            "P",
        )

        case = make_case(
            int14b,
            name,
            nr=COARSE_NR,
            nz=COARSE_NZ,
            radius=radius,
            depth=depth,
            payload_radius=payload_radius,
            category=(
                "BLIND_WILDCARD_NOT_PHYSICS_PRIOR"
            ),
        )

        print(
            f"024C_WILDCARD_BEGIN={name} "
            f"R={radius:.6f} "
            f"D={depth:.6f}",
            flush=True,
        )

        row = solve_planar_case(
            int14b,
            int14c,
            case,
            aperture=PRIMARY_APERTURE,
        )

        print_case(
            name,
            row,
        )

        rows_public.append(
            public_row(
                row,
                radius=radius,
                depth=depth,
                aperture=PRIMARY_APERTURE,
                category=(
                    "BLIND_WILDCARD_NOT_PHYSICS_PRIOR"
                ),
                resolution="COARSE",
            )
        )

        wildcard_solutions.append(
            (
                radius,
                depth,
                case,
                row,
            )
        )

    print(
        "WILDCARDS_ARE_PHYSICS_PRIORS=NO"
    )

    # ------------------------------------------------------------
    # E. Select ONLY from physically motivated cases.
    # ------------------------------------------------------------

    green_physical = [
        item
        for item
        in physical_solutions
        if bool(
            item[
                3
            ].get(
                "green",
                False,
            )
        )
        and math.isfinite(
            float(
                item[
                    3
                ].get(
                    "coefficient",
                    float(
                        "nan"
                    ),
                )
            )
        )
    ]

    if not green_physical:
        raise RuntimeError(
            "No green physically motivated 024C geometry."
        )

    selected = min(
        green_physical,
        key=lambda item: float(
            item[
                3
            ][
                "coefficient"
            ]
        ),
    )

    (
        selected_r,
        selected_d,
        _selected_case_coarse,
        selected_row_coarse,
    ) = selected

    print(
        "\n=== E — SELECTED PHYSICAL GEOMETRY ==="
    )

    print(
        f"SELECTED_R_OVER_H="
        f"{selected_r:.15f}"
    )

    print(
        f"SELECTED_DEPTH_OVER_H="
        f"{selected_d:.15f}"
    )

    print(
        f"SELECTED_COARSE_C="
        f"{float(selected_row_coarse['coefficient']):.15e}"
    )

    if wildcard_solutions:

        wildcard_green = [
            item
            for item
            in wildcard_solutions
            if bool(
                item[
                    3
                ].get(
                    "green",
                    False,
                )
            )
        ]

        if wildcard_green:

            best_wildcard = min(
                wildcard_green,
                key=lambda item: float(
                    item[
                        3
                    ][
                        "coefficient"
                    ]
                ),
            )

            print(
                f"BEST_WILDCARD_C_DIAGNOSTIC="
                f"{float(best_wildcard[3]['coefficient']):.15e}"
            )

            print(
                "BEST_WILDCARD_USED_FOR_PROMOTION=NO"
            )

    # ------------------------------------------------------------
    # F. Refine selected geometry.
    # ------------------------------------------------------------

    print(
        "\n=== F — SELECTED GEOMETRY REFINEMENT ===",
        flush=True,
    )

    refined = {}

    for (
        label,
        nr,
        nz,
    ) in (
        (
            "MEDIUM",
            MEDIUM_NR,
            MEDIUM_NZ,
        ),
        (
            "HIGH",
            HIGH_NR,
            HIGH_NZ,
        ),
    ):

        name = (
            f"024C_SELECTED_{label}_"
            f"R{selected_r:.3f}_D{selected_d:.3f}"
        ).replace(
            ".",
            "P",
        )

        case = make_case(
            int14b,
            name,
            nr=nr,
            nz=nz,
            radius=selected_r,
            depth=selected_d,
            payload_radius=payload_radius,
            category="SELECTED_REFINEMENT",
        )

        print(
            f"024C_REFINEMENT_BEGIN={label} "
            f"GRID={nr}x{nz}",
            flush=True,
        )

        row = solve_planar_case(
            int14b,
            int14c,
            case,
            aperture=PRIMARY_APERTURE,
        )

        print_case(
            label,
            row,
        )

        refined[
            label
        ] = (
            case,
            row,
        )

        rows_public.append(
            public_row(
                row,
                radius=selected_r,
                depth=selected_d,
                aperture=PRIMARY_APERTURE,
                category="SELECTED_REFINEMENT",
                resolution=label,
            )
        )

    medium_case, medium_row = (
        refined[
            "MEDIUM"
        ]
    )

    high_case, high_row = (
        refined[
            "HIGH"
        ]
    )

    if not (
        bool(
            medium_row.get(
                "green",
                False,
            )
        )
        and bool(
            high_row.get(
                "green",
                False,
            )
        )
    ):
        raise RuntimeError(
            "Selected source did not remain green under refinement."
        )

    c_medium = float(
        medium_row[
            "coefficient"
        ]
    )

    c_high = float(
        high_row[
            "coefficient"
        ]
    )

    c_conservative = max(
        c_medium,
        c_high,
    )

    c_rel = relative_error(
        c_medium,
        c_high,
    )

    improvement_vs_006d = (
        C006D
        / c_conservative
    )

    improvement_vs_b7 = (
        current_b7_c
        / c_conservative
    )

    high_width = min(
        float(
            high_row.get(
                "energy_width_cells",
                float(
                    "nan"
                ),
            )
        ),
        float(
            high_row.get(
                "force_width_cells",
                float(
                    "nan"
                ),
            )
        ),
    )

    print(
        f"REFINEMENT_C_MEDIUM="
        f"{c_medium:.15e}"
    )

    print(
        f"REFINEMENT_C_HIGH="
        f"{c_high:.15e}"
    )

    print(
        f"REFINEMENT_C_CONSERVATIVE="
        f"{c_conservative:.15e}"
    )

    print(
        f"REFINEMENT_C_REL_DIFF="
        f"{c_rel:.15e}"
    )

    print(
        f"HIGH_MIN_PARTICIPATION_WIDTH_CELLS="
        f"{high_width:.15e}"
    )

    print(
        f"IMPROVEMENT_VS_006D="
        f"{improvement_vs_006d:.15e}"
    )

    print(
        f"HEADROOM_VS_B7="
        f"{improvement_vs_b7:.15e}"
    )

    # ------------------------------------------------------------
    # G. Independent force, planarity and anatomy.
    # ------------------------------------------------------------

    print(
        "\n=== G — INDEPENDENT PLANAR VECTOR-FORCE AUDIT ===",
        flush=True,
    )

    diagnostics = (
        planar_diagnostics(
            high_row,
            aperture=PRIMARY_APERTURE,
        )
    )

    print(
        f"INDEPENDENT_DISK_ACCELERATION="
        f"{diagnostics['independent_disk_acceleration']:+.15e}"
    )

    print(
        f"BASE_DISK_ACCELERATION="
        f"{diagnostics['base_disk_acceleration']:+.15e}"
    )

    print(
        f"INDEPENDENT_FORCE_RELERR="
        f"{diagnostics['independent_force_relative_error']:.15e}"
    )

    print(
        "INDEPENDENT_FORCE_RECONSTRUCTION="
        + (
            "PASS"
            if diagnostics[
                "independent_force_pass"
            ]
            else "FAIL"
        )
    )

    for radius, az, ar in zip(
        diagnostics[
            "sentinel_radii"
        ],
        diagnostics[
            "sentinel_axial"
        ],
        diagnostics[
            "sentinel_radial"
        ],
    ):

        print(
            f"PLANAR_SENTINEL_R={float(radius):.6f} "
            f"AZ={float(az):+.12e} "
            f"AR={float(ar):+.12e}"
        )

    print(
        f"PLANAR_MIN_AXIAL="
        f"{diagnostics['minimum_axial']:+.15e}"
    )

    print(
        f"PLANAR_MAX_AXIAL="
        f"{diagnostics['maximum_axial']:+.15e}"
    )

    print(
        f"PLANAR_FLATNESS="
        f"{diagnostics['planar_flatness']:.15e}"
    )

    print(
        f"PLANAR_EDGE_TO_CENTER="
        f"{diagnostics['edge_to_center_axial_ratio']:.15e}"
    )

    print(
        f"PLANAR_MAX_TRANSVERSE_FRACTION="
        f"{diagnostics['max_transverse_fraction']:.15e}"
    )

    print(
        "PLANAR_ALL_SENTINELS_OUTWARD="
        + (
            "YES"
            if diagnostics[
                "all_sentinels_outward"
            ]
            else "NO"
        )
    )

    print(
        "PLANAR_WORKING_REGION_GATE="
        + (
            "PASS"
            if diagnostics[
                "planar_pass"
            ]
            else "FAIL"
        )
    )

    print(
        f"FRONT_TO_BACK_ABS_RESPONSE_RATIO="
        f"{diagnostics['front_to_back_abs_ratio']:.15e}"
    )

    print(
        f"AXIAL_RESPONSE_AT_Z1P5_OVER_WORKING="
        f"{diagnostics['far_over_working']:.15e}"
    )

    # ------------------------------------------------------------
    # H. Teacher-inspired anatomy.
    # ------------------------------------------------------------

    print(
        "\n=== H — DISCOVERED STRESS ANATOMY ==="
    )

    print(
        f"ANATOMY_A_RHO="
        f"{diagnostics['A_rho']:+.15e}"
    )

    print(
        f"ANATOMY_A_STRESS="
        f"{diagnostics['A_stress']:+.15e}"
    )

    print(
        f"ANATOMY_STRESS_FRACTION="
        f"{diagnostics['stress_fraction']:+.15e}"
    )

    print(
        f"ANATOMY_CANCELLATION="
        f"{diagnostics['cancellation']:.15e}"
    )

    print(
        f"ANATOMY_FORCE_WEIGHTED_MEDIAN_S_OVER_E="
        f"{diagnostics['force_weighted_median_S_over_e']:+.15e}"
    )

    print(
        f"ANATOMY_MAX_DEC_SATURATION="
        f"{diagnostics['max_DEC_saturation']:.15e}"
    )

    print(
        f"ANATOMY_F90_ENERGY_FRACTION="
        f"{diagnostics['F90_energy_fraction']:.15e}"
    )

    print(
        f"ANATOMY_F90_R_MEAN_OVER_H="
        f"{diagnostics['F90_r_mean']:.15e}"
    )

    print(
        f"ANATOMY_F90_Z_MEAN_OVER_H="
        f"{diagnostics['F90_z_mean']:.15e}"
    )

    # ------------------------------------------------------------
    # I. Vertical-routing mechanism audit.
    # ------------------------------------------------------------

    print(
        "\n=== I — BURIED STRESS-RETURN MECHANISM AUDIT ==="
    )

    same_radius_physical = [
        item
        for item
        in physical_solutions
        if abs(
            item[
                0
            ]
            - selected_r
        )
        < 1.0e-12
        and bool(
            item[
                3
            ].get(
                "green",
                False,
            )
        )
    ]

    shallow_reference = None

    if same_radius_physical:

        shallow_reference = min(
            same_radius_physical,
            key=lambda item: item[
                1
            ],
        )

    if (
        shallow_reference is not None
        and shallow_reference[
            1
        ]
        < selected_d
    ):

        shallow_c = float(
            shallow_reference[
                3
            ][
                "coefficient"
            ]
        )

        vertical_routing_gain = (
            shallow_c
            /
            float(
                selected_row_coarse[
                    "coefficient"
                ]
            )
        )

        print(
            f"SAME_R_SHALLOW_DEPTH="
            f"{shallow_reference[1]:.15e}"
        )

        print(
            f"SAME_R_SHALLOW_C="
            f"{shallow_c:.15e}"
        )

        print(
            f"VERTICAL_ROUTING_GAIN_COARSE="
            f"{vertical_routing_gain:.15e}"
        )

        print(
            "BURIED_STRESS_RETURN_HELPED_COARSE="
            + (
                "YES"
                if vertical_routing_gain
                > 1.05
                else "NO"
            )
        )

    else:

        vertical_routing_gain = float(
            "nan"
        )

        print(
            "VERTICAL_ROUTING_GAIN_COARSE=UNRESOLVED_NO_SHALLOW_SAME_R_CONTROL"
        )

    # ------------------------------------------------------------
    # J. Aperture sensitivity on fixed high-resolution source.
    # ------------------------------------------------------------

    print(
        "\n=== J — WORKING-PLANE APERTURE SENSITIVITY ==="
    )

    aperture_sensitivity = {}

    for aperture in (
        0.25,
        0.50,
        0.75,
    ):

        diag = planar_diagnostics(
            high_row,
            aperture=aperture,
        )

        aperture_sensitivity[
            str(
                aperture
            )
        ] = {
            key: value
            for key, value
            in diag.items()
            if key not in (
                "sentinel_radii",
                "sentinel_axial",
                "sentinel_radial",
                "independent_disk_kernel",
            )
        }

        print(
            f"APERTURE={aperture:.2f} "
            f"A={diag['independent_disk_acceleration']:+.12e} "
            f"FLATNESS={diag['planar_flatness']:.9e} "
            f"TRANSVERSE={diag['max_transverse_fraction']:.9e} "
            f"ALL_OUTWARD={'YES' if diag['all_sentinels_outward'] else 'NO'}"
        )

    # ------------------------------------------------------------
    # K. Independent SCS selected-case check when available.
    # ------------------------------------------------------------

    print(
        "\n=== K — INDEPENDENT SOLVER CHECK ===",
        flush=True,
    )

    installed = (
        int14c.cp.installed_solvers()
    )

    scs_available = (
        "SCS"
        in installed
    )

    scs_pass = True
    scs_rel = float(
        "nan"
    )
    scs_c = float(
        "nan"
    )

    if scs_available:

        scs_row = solve_planar_case(
            int14b,
            int14c,
            medium_case,
            aperture=PRIMARY_APERTURE,
            solver_override="SCS",
        )

        scs_c = float(
            scs_row.get(
                "coefficient",
                float(
                    "nan"
                ),
            )
        )

        scs_rel = relative_error(
            scs_c,
            c_medium,
        )

        scs_pass = bool(
            scs_row.get(
                "green",
                False,
            )
            and scs_rel
            <= SCS_C_REL_TOL
        )

        print(
            f"SCS_MEDIUM_C="
            f"{scs_c:.15e}"
        )

        print(
            f"SCS_CLARABEL_C_REL_DIFF="
            f"{scs_rel:.15e}"
        )

        print(
            "INDEPENDENT_SCS_CHECK="
            + (
                "PASS"
                if scs_pass
                else "FAIL"
            )
        )

    else:

        print(
            "INDEPENDENT_SCS_CHECK=UNAVAILABLE"
        )

    # ------------------------------------------------------------
    # L. Final gates.
    # ------------------------------------------------------------

    convergence_pass = bool(
        c_rel
        <= C_CONVERGENCE_TOL
    )

    width_pass = bool(
        math.isfinite(
            high_width
        )
        and high_width
        >= MIN_WIDTH_CELLS
    )

    beats_006d = bool(
        c_conservative
        < C006D
    )

    teacher_like_stress = bool(
        diagnostics[
            "max_DEC_saturation"
        ]
        >= 0.90
        and diagnostics[
            "cancellation"
        ]
        <= 2.0
    )

    major_candidate = bool(
        convergence_pass
        and width_pass
        and diagnostics[
            "independent_force_pass"
        ]
        and diagnostics[
            "planar_pass"
        ]
        and beats_006d
        and scs_pass
    )

    if major_candidate:

        decision = (
            "YELLOW_HIGH_PRIORITY_NEW_PLANAR_"
            "CONSERVED_DEC_SOURCE_RECORD_CANDIDATE"
        )

        next_action = (
            "024C1R_INDEPENDENT_RECONSTRUCTION_HIGHER_RESOLUTION_"
            "FINITE_PAYLOAD_AND_SOURCE_ANATOMY_CONFIRMATION"
        )

    elif (
        diagnostics[
            "planar_pass"
        ]
        and convergence_pass
        and width_pass
    ):

        decision = (
            "YELLOW_PLANAR_CONSERVED_DEC_MORPHOLOGY_"
            "NO_006D_EFFICIENCY_RECORD"
        )

        next_action = (
            "COMPARE_DISCOVERED_STRESS_ANATOMY_WITH_FIELD_THEORY_"
            "ACCESSIBILITY_BEFORE_ANY_MORE_SOURCE_OPTIMIZATION"
        )

    elif beats_006d:

        decision = (
            "YELLOW_RAW_SOURCE_EFFICIENCY_IMPROVEMENT_"
            "PLANAR_OR_REGULARITY_GATE_FAILED"
        )

        next_action = (
            "ONE_TARGETED_024C_REPAIR_ONLY_IF_FAILURE_IS_NUMERICAL_"
            "NOT_PHYSICAL"
        )

    else:

        decision = (
            "RED_BURIED_PLANAR_STRESS_LENS_"
            "DID_NOT_BEAT_006D_IN_TESTED_CLASS"
        )

        next_action = (
            "STOP_024C_SOURCE_SEARCH_AND_RETURN_TO_"
            "MICROSCOPIC_STATIC_OR_ANALOGUE_RERANK"
        )

    print(
        "\n=== L — 024C DECISION ==="
    )

    print(
        "NEW_ARCHITECTURE_IS_006D_PROFILE="
        "NO"
    )

    print(
        "FULL_RZ_STRESS_ROUTING_USED=YES"
    )

    print(
        "STRICT_TRUE_STANDOFF_ZLE0=YES"
    )

    print(
        "POSITIVE_FAR_FIELD_ACTIVE_MASS="
        "PASS_IF_GREEN_LAUE"
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
            if diagnostics[
                "planar_pass"
            ]
            else "FAIL"
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
        "TEACHER_LIKE_NEAR_DEC_LOW_CANCELLATION="
        + (
            "YES"
            if teacher_like_stress
            else "NO"
        )
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
        f"024C_DECISION="
        f"{decision}"
    )

    print(
        f"NEXT="
        f"{next_action}"
    )

    print(
        "CURRENT_KNOWLEDGE_HEURISTIC="
        "70_TO_71_PERCENT_RETAIN_UNLESS_RESULT_EARNS_PROMOTION"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )

    # ------------------------------------------------------------
    # Persist cases.
    # ------------------------------------------------------------

    fields = sorted({
        key
        for row in rows_public
        for key in row.keys()
    })

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
            rows_public
        )

    arrays = high_row[
        "_arrays"
    ]

    np.savez_compressed(
        OUT_NPZ,
        **{
            key: np.asarray(
                value
            )
            for key, value
            in arrays.items()
        },
        independent_disk_kernel=np.asarray(
            diagnostics[
                "independent_disk_kernel"
            ]
        ),
        sentinel_radii=np.asarray(
            diagnostics[
                "sentinel_radii"
            ]
        ),
        sentinel_axial=np.asarray(
            diagnostics[
                "sentinel_axial"
            ]
        ),
        sentinel_radial=np.asarray(
            diagnostics[
                "sentinel_radial"
            ]
        ),
    )

    summary = {
        "claim_classification":
            (
                "PROJECT_DERIVED_TEACHER_GUIDED_PLANAR_"
                "CONSERVED_DEC_SOURCE_DISCOVERY_SCOUT"
            ),

        "anchors": {
            "C_006D":
                C006D,

            "C_006B_thin":
                C006B_THIN,

            "C_B7":
                current_b7_c,

            "payload_radius_over_h":
                payload_radius,
        },

        "design": {
            "name":
                "TEACHER_GUIDED_PLANAR_STRESS_LENS",

            "is_006D_profile":
                False,

            "strict_z_le_0":
                True,

            "working_plane_z_over_h":
                TARGET_Z,

            "primary_aperture_over_h":
                PRIMARY_APERTURE,

            "full_rz_stress_routing":
                True,

            "perfect_static_beam_claim":
                False,
        },

        "selected_geometry": {
            "radius_over_h":
                selected_r,

            "depth_over_h":
                selected_d,
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

            "minimum_high_width_cells":
                high_width,

            "improvement_vs_006D":
                improvement_vs_006d,

            "headroom_vs_B7":
                improvement_vs_b7,
        },

        "planar_diagnostics": {
            key: (
                value.tolist()
                if isinstance(
                    value,
                    np.ndarray,
                )
                else value
            )
            for key, value
            in diagnostics.items()
            if key
            !=
            "independent_disk_kernel"
        },

        "aperture_sensitivity":
            aperture_sensitivity,

        "vertical_routing_gain_coarse":
            vertical_routing_gain,

        "independent_solver": {
            "SCS_available":
                scs_available,

            "SCS_C":
                scs_c,

            "SCS_relative_difference":
                scs_rel,

            "pass":
                scs_pass,
        },

        "gates": {
            "coefficient_convergence":
                convergence_pass,

            "physical_width":
                width_pass,

            "independent_force":
                bool(
                    diagnostics[
                        "independent_force_pass"
                    ]
                ),

            "planar_working_region":
                bool(
                    diagnostics[
                        "planar_pass"
                    ]
                ),

            "beats_006D":
                beats_006d,

            "teacher_like_near_DEC_low_cancellation":
                teacher_like_stress,

            "major_candidate":
                major_candidate,
        },

        "decision":
            decision,

        "next":
            next_action,

        "claim_limits": [
            "NO_MICROSCOPIC_FIELD_REALIZATION",
            "NO_FULL_STABILITY",
            "NO_NONLINEAR_GR",
            "NO_PERFECT_GRAVITY_BEAM",
            "NO_PRACTICAL_ENERGY_SCALING",
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

    print(
        f"SELECTED_NPZ="
        f"{OUT_NPZ.relative_to(ROOT)}"
    )

    print(
        "024C_RUN_COMPLETE=YES"
    )


if __name__ == "__main__":
    main()
