"""032H17A12D1R1 — strongly loaded low-capacity F^2 payload rescue.

PURPOSE
-------
A12C established a remarkable probe-limit result:

    finite neutral 1 kg payload
    true 1 m external stand-off
    whole sampled payload >= 1 g outward
    canonical field energy = 2.6568591420597114 J
    reference metric scale = 1 keV.

A12D1 then established that the same universal matter action modifies the
vector kinetic operator inside finite matter:

    Z_matter
        =
    1 + 2 rho_E / M_X^4

at leading order in the extraordinarily small operating sigma.

At 1 keV, even the average-density lower bound gives Z-1 >> 1, so exact
perturbative reuse of the unloaded A12C field is invalid.

Crucially, A12D1 did NOT prove that the strongly loaded solution fails.

This branch therefore performs the missing calculation.

STATIC SAME-ACTION EQUATION
---------------------------
For

    g_phys = exp(2 sigma) g

and

    sigma = F_X^2 / (2 M_X^4),

the nonrelativistic finite-matter quadratic action is

    L_quad
        =
    -(1/4)
    Z(x)
    F_X^2

with

    Z(x)
        =
    1 + 2 rho_E(x)/M_X^4.

For the axisymmetric magnetostatic field

    A = A_phi(rho,z) e_phi,

    B_rho = -partial_z A_phi,

    B_z = (1/rho) partial_rho(rho A_phi),

the variational equation is

    curl[ Z(x) B ] = J.

This run discretizes the positive quadratic functional directly:

    E_quad
        =
    (1/2)
    int Z B^2 dV,

rather than inserting an ad-hoc pointwise correction into the old PDE.

That gives a symmetric positive-definite static operator whenever Z>0.

PAYLOAD MODEL
-------------
A true microscopic payload density was absent from A12C because the payload
was only a probe region.

R1 therefore introduces an explicitly finite neutral-matter density.

The primary rescue profile is intentionally optimistic:

    OPTIMISTIC_FLAT_C1

It has a flat central density and a C1 taper to zero across the outer half of
the 0.2 m torus minor radius.

Its cross-sectional mean profile is exactly 23/40, so its peak density is
only 40/23 times the volume-average density.

This gives the few-joule mechanism a substantially better chance than a
strongly peaked payload.

A second smoother profile,

    POLYNOMIAL_C1

uses

    p(s) = (1-s^2)^2

and has peak density three times the average.

It is used as a robustness diagnostic only.

Both profiles:

- contain exactly 1 kg analytically;
- occupy the original A12C toroidal support;
- preserve the 1 m geometric source/payload stand-off;
- are nonnegative;
- vanish continuously at the payload boundary.

ENERGY ACCOUNTING
-----------------
The run separates:

1. canonical field energy

       E_field = (1/2) int B^2 dV;

2. leading payload interaction energy

       E_payload = (1/2) int (Z-1) B^2 dV;

3. loaded quadratic capacity

       E_loaded = E_field + E_payload;

4. source work

       E_source_work = (1/2) int J A dV.

For the variational solution,

    E_source_work = E_loaded

up to numerical solve precision.

The payload interaction term is independently reconstructed from

    int rho c^2 [exp(sigma)-1] dV.

Because sigma required for meter-scale 1 g response is extremely small,
the exact exponential correction should be tiny.  That statement is checked
rather than assumed.

IMPORTANT CLAIM LIMIT
---------------------
This is PAYLOAD-loaded, not fully source-loaded.

The microscopic source completion is still unresolved.

Therefore even an excellent R1 result does NOT establish:

- complete same-action source matter;
- a microscopic source;
- source/support energy;
- UV completion;
- empirical consistency;
- stability of every interacting mode;
- complete operating energy;
- a physical antigravity model;
- a device.

R1 answers a narrower but decisive question:

    Does the low-capacity A12C F^2 mechanism survive the finite payload's
    own same-action backreaction?

LOW-CAPACITY RESCUE LOGIC
-------------------------
The exact 1 keV point is retested at multiple resolutions.

A targeted portal scan is then allowed because A12D1 introduced a NEW
physical failure mode.  This is not optimization performed merely to lower
an already-small field number.

If the exact 1 keV branch loses the outward whole-payload sign but a nearby
low-energy strongly-loaded branch survives, the mechanism remains open and
a loading-aware source-shape rescue is promoted.

If no strongly-loaded branch remains below 10 MJ, the next structural escape
is the mixed-E/B topological F*F portal already left open by A12D0.

CLAIM CLASSIFICATION
--------------------
PROJECT_STRONGLY_LOADED_PAYLOAD_PREFLIGHT
"""

from __future__ import annotations

import json
import math
from functools import lru_cache
from pathlib import Path
from typing import Any

import numpy as np
from scipy.interpolate import RegularGridInterpolator
from scipy.sparse import coo_matrix, diags
from scipy.sparse.linalg import spsolve

from .hook17_concurrent_u1_fieldstrength_metric import (
    C_LIGHT_M_S,
    EV_J,
    HBAR_C_EV_M,
    PAYLOAD_MAJOR_RADIUS_M,
    PAYLOAD_MASS_KG,
    PAYLOAD_MINOR_RADIUS_M,
    PAYLOAD_STANDOFF_M,
    REFERENCE_PORTAL_SCALE_EV,
    SOURCE_RADIUS_M,
    STRICT_COMPLETE_OPERATING_TARGET_J,
    TARGET_ACCELERATION_M_S2,
)
from .hook17_pauli_f2_same_action_loading import (
    h17a12d1_summary,
)


PRIMARY_DENSITY_MODEL = "OPTIMISTIC_FLAT_C1"
ROBUSTNESS_DENSITY_MODEL = "POLYNOMIAL_C1"

FLAT_CORE_FRACTION = 0.5

# For the declared C1 flat-core profile this is exact:
#
#   2 int_0^1 s p(s) ds = 23/40.
FLAT_C1_CROSS_SECTION_MEAN = 23.0 / 40.0

POLYNOMIAL_C1_CROSS_SECTION_MEAN = 1.0 / 3.0

# Fixed payload sampling independent of PDE grid.
PAYLOAD_SAMPLE_RADIAL_COUNT = 31
PAYLOAD_SAMPLE_ANGULAR_COUNT = 96
PAYLOAD_SAMPLE_MAX_RADIUS_FRACTION = 0.995

# Broad rescue scan.  This is deliberately narrow relative to the full
# possible theory space and centered on preservation of the A12C mechanism.
BROAD_PORTAL_SCALES_EV = (
    250.0,
    500.0,
    1000.0,
    2000.0,
    5000.0,
    10000.0,
    12000.0,
    14000.0,
    16000.0,
    18000.0,
    20000.0,
    24000.0,
    32000.0,
    40000.0,
)

BROAD_SCAN_GRID_M = 0.100
INTERMEDIATE_GRID_M = 0.075
PRODUCTION_GRID_M = 0.050

PRODUCTION_RHO_MAX_M = 12.0
PRODUCTION_Z_MIN_M = -10.0
PRODUCTION_Z_MAX_M = 13.0

LARGER_RHO_MAX_M = 14.0
LARGER_Z_MIN_M = -12.0
LARGER_Z_MAX_M = 15.0

UNLOADED_RECONSTRUCTION_ENERGY_TOL = 0.06
UNLOADED_RECONSTRUCTION_SOURCE_TOL = 0.06

# Loaded branch is more difficult numerically.  These are preflight gates,
# not final promotion tolerances.
LOADED_GRID_CAPACITY_RELERR_MAX = 0.15
LOADED_GRID_SOURCE_RELERR_MAX = 0.15
LOADED_DOMAIN_CAPACITY_RELERR_MAX = 0.10

LOW_CAPACITY_J = 100.0
LOW_KJ_CAPACITY_J = 10000.0
SUB_MJ_CAPACITY_J = 1.0e6


def _repo_root() -> Path:
    """Return repository root from src/antigravity_research/agminer."""

    return (
        Path(__file__)
        .resolve()
        .parents[3]
    )


@lru_cache(maxsize=1)
def a12c_artifact() -> dict[str, Any]:
    """Load frozen A12C result artifact."""

    path = (
        _repo_root()
        /
        "results"
        /
        "data"
        /
        "032h17a12c_hook17_concurrent_u1_fieldstrength_metric_summary.json"
    )

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


@lru_cache(maxsize=1)
def a12d1_artifact() -> dict[str, Any]:
    """Load completed A12D1 result artifact."""

    path = (
        _repo_root()
        /
        "results"
        /
        "data"
        /
        "032h17a12d1_hook17_pauli_f2_same_action_loading_summary.json"
    )

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def payload_center_z_m() -> float:
    """Return original A12C torus center."""

    centerline_radius = (
        SOURCE_RADIUS_M
        +
        PAYLOAD_STANDOFF_M
        +
        PAYLOAD_MINOR_RADIUS_M
    )

    return math.sqrt(
        centerline_radius**2
        -
        PAYLOAD_MAJOR_RADIUS_M**2
    )


def geometric_standoff_m() -> float:
    """Return exact source-surface to payload-support gap."""

    centerline_distance = math.sqrt(
        PAYLOAD_MAJOR_RADIUS_M**2
        +
        payload_center_z_m()**2
    )

    return (
        centerline_distance
        -
        PAYLOAD_MINOR_RADIUS_M
        -
        SOURCE_RADIUS_M
    )


def payload_torus_volume_m3() -> float:
    """Return geometric A12C torus volume."""

    return (
        2.0
        *
        math.pi**2
        *
        PAYLOAD_MAJOR_RADIUS_M
        *
        PAYLOAD_MINOR_RADIUS_M**2
    )


def average_payload_mass_density_kg_m3() -> float:
    """Return 1 kg divided by geometric torus volume."""

    return (
        PAYLOAD_MASS_KG
        /
        payload_torus_volume_m3()
    )


def one_ev4_j_m3() -> float:
    """Return SI energy density corresponding to one eV^4."""

    return (
        EV_J
        /
        HBAR_C_EV_M**3
    )


def _flat_c1_profile(
    s: np.ndarray,
) -> np.ndarray:
    """Return flat-core C1 radial profile on dimensionless cross radius."""

    profile = np.zeros_like(
        s,
        dtype=float,
    )

    core = (
        s
        <=
        FLAT_CORE_FRACTION
    )

    transition = (
        (
            s
            >
            FLAT_CORE_FRACTION
        )
        &
        (
            s
            <
            1.0
        )
    )

    profile[
        core
    ] = 1.0

    t = (
        (
            1.0
            -
            s[
                transition
            ]
        )
        /
        (
            1.0
            -
            FLAT_CORE_FRACTION
        )
    )

    profile[
        transition
    ] = (
        t**2
        *
        (
            3.0
            -
            2.0
            *
            t
        )
    )

    return profile


def payload_density_profile_kg_m3(
    rho: np.ndarray,
    z: np.ndarray,
    density_model: str = PRIMARY_DENSITY_MODEL,
) -> np.ndarray:
    """Return analytically normalized finite payload mass density."""

    s = (
        np.sqrt(
            (
                rho
                -
                PAYLOAD_MAJOR_RADIUS_M
            ) ** 2
            +
            (
                z
                -
                payload_center_z_m()
            ) ** 2
        )
        /
        PAYLOAD_MINOR_RADIUS_M
    )

    average_density = (
        average_payload_mass_density_kg_m3()
    )

    if (
        density_model
        ==
        PRIMARY_DENSITY_MODEL
    ):
        profile = (
            _flat_c1_profile(
                s
            )
        )

        peak_density = (
            average_density
            /
            FLAT_C1_CROSS_SECTION_MEAN
        )

    elif (
        density_model
        ==
        ROBUSTNESS_DENSITY_MODEL
    ):
        profile = np.zeros_like(
            s,
            dtype=float,
        )

        inside = (
            s
            <
            1.0
        )

        profile[
            inside
        ] = (
            1.0
            -
            s[
                inside
            ] ** 2
        ) ** 2

        peak_density = (
            average_density
            /
            POLYNOMIAL_C1_CROSS_SECTION_MEAN
        )

    else:
        raise ValueError(
            "unknown density_model"
        )

    return (
        peak_density
        *
        profile
    )


def payload_density_model_gate() -> dict[str, Any]:
    """Return exact analytic payload-density normalization."""

    average_density = (
        average_payload_mass_density_kg_m3()
    )

    primary_peak = (
        average_density
        /
        FLAT_C1_CROSS_SECTION_MEAN
    )

    robustness_peak = (
        average_density
        /
        POLYNOMIAL_C1_CROSS_SECTION_MEAN
    )

    return {
        "payload_mass_kg":
            PAYLOAD_MASS_KG,

        "torus_volume_m3":
            payload_torus_volume_m3(),

        "average_density_kg_m3":
            average_density,

        "primary_density_model":
            PRIMARY_DENSITY_MODEL,

        "primary_cross_section_mean":
            FLAT_C1_CROSS_SECTION_MEAN,

        "primary_peak_density_kg_m3":
            primary_peak,

        "primary_peak_over_average":
            (
                primary_peak
                /
                average_density
            ),

        "robustness_density_model":
            ROBUSTNESS_DENSITY_MODEL,

        "robustness_cross_section_mean":
            POLYNOMIAL_C1_CROSS_SECTION_MEAN,

        "robustness_peak_density_kg_m3":
            robustness_peak,

        "robustness_peak_over_average":
            (
                robustness_peak
                /
                average_density
            ),

        "density_nonnegative":
            True,

        "compact_support":
            True,

        "same_geometric_standoff_as_a12c":
            math.isclose(
                geometric_standoff_m(),
                1.0,
                rel_tol=0.0,
                abs_tol=1.0e-12,
            ),

        "primary_profile_is_deliberately_optimistic":
            True,
    }


def loading_coefficient_z(
    density_kg_m3: np.ndarray,
    portal_scale_ev: float,
) -> np.ndarray:
    """Return leading same-action finite-matter kinetic factor Z."""

    portal_scale_ev = float(
        portal_scale_ev
    )

    if portal_scale_ev <= 0.0:
        raise ValueError(
            "portal_scale_ev must be positive"
        )

    rho_energy_j_m3 = (
        density_kg_m3
        *
        C_LIGHT_M_S**2
    )

    rho_energy_ev4 = (
        rho_energy_j_m3
        /
        one_ev4_j_m3()
    )

    return (
        1.0
        +
        2.0
        *
        rho_energy_ev4
        /
        portal_scale_ev**4
    )


def primary_peak_loading_gate(
    portal_scale_ev: float = REFERENCE_PORTAL_SCALE_EV,
) -> dict[str, float]:
    """Return exact peak loading implied by primary analytic density profile."""

    density_gate = (
        payload_density_model_gate()
    )

    peak_density = float(
        density_gate[
            "primary_peak_density_kg_m3"
        ]
    )

    peak_rho_ev4 = (
        peak_density
        *
        C_LIGHT_M_S**2
        /
        one_ev4_j_m3()
    )

    epsilon_peak = (
        2.0
        *
        peak_rho_ev4
        /
        float(
            portal_scale_ev
        ) ** 4
    )

    return {
        "portal_scale_ev":
            float(
                portal_scale_ev
            ),

        "peak_epsilon_load":
            epsilon_peak,

        "peak_z":
            1.0
            +
            epsilon_peak,
    }


def _source_profile(
    rho: np.ndarray,
    z: np.ndarray,
) -> np.ndarray:
    """Return frozen compact A12C azimuthal source morphology."""

    radius_squared = (
        rho**2
        +
        z**2
    )

    inside = (
        radius_squared
        <
        SOURCE_RADIUS_M**2
    )

    profile = np.zeros_like(
        rho,
        dtype=float,
    )

    x = (
        radius_squared[
            inside
        ]
        /
        SOURCE_RADIUS_M**2
    )

    profile[
        inside
    ] = (
        (
            rho[
                inside
            ]
            /
            SOURCE_RADIUS_M
        )
        *
        (
            1.0
            -
            x
        ) ** 2
    )

    return profile


def _payload_sample_points() -> np.ndarray:
    """Return fixed axisymmetric torus cross-section samples."""

    radial_fractions = np.linspace(
        0.0,
        PAYLOAD_SAMPLE_MAX_RADIUS_FRACTION,
        PAYLOAD_SAMPLE_RADIAL_COUNT,
    )

    angles = np.linspace(
        0.0,
        2.0
        *
        math.pi,
        PAYLOAD_SAMPLE_ANGULAR_COUNT,
        endpoint=False,
    )

    points = []

    for fraction in radial_fractions:
        radius = (
            PAYLOAD_MINOR_RADIUS_M
            *
            fraction
        )

        for angle in angles:
            rho = (
                PAYLOAD_MAJOR_RADIUS_M
                +
                radius
                *
                math.cos(
                    angle
                )
            )

            z = (
                payload_center_z_m()
                +
                radius
                *
                math.sin(
                    angle
                )
            )

            points.append(
                [
                    z,
                    rho,
                ]
            )

    return np.asarray(
        points,
        dtype=float,
    )


def _grid(
    h: float,
    rho_max_m: float,
    z_min_m: float,
    z_max_m: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Return full cylindrical grid."""

    rhos = np.arange(
        0.0,
        rho_max_m
        +
        0.5
        *
        h,
        h,
    )

    zs = np.arange(
        z_min_m,
        z_max_m
        +
        0.5
        *
        h,
        h,
    )

    rho_grid, z_grid = np.meshgrid(
        rhos,
        zs,
    )

    return (
        rhos,
        zs,
        rho_grid,
        z_grid,
    )


def _assemble_weighted_operator(
    rhos: np.ndarray,
    zs: np.ndarray,
    z_coefficient: np.ndarray,
    source_profile: np.ndarray,
    h: float,
) -> tuple[Any, np.ndarray]:
    """Assemble symmetric finite-volume operator from magnetic energy.

    The discrete quadratic form approximates

        int rho Z [
            (partial_z A)^2
            +
            ((1/rho) partial_rho(rho A))^2
        ] d rho d z.

    Dirichlet A_phi=0 is imposed on the outer rectangular boundary and at the
    symmetry axis.
    """

    n_rho_full = len(
        rhos
    )

    n_z_full = len(
        zs
    )

    nr = (
        n_rho_full
        -
        2
    )

    nz = (
        n_z_full
        -
        2
    )

    n = (
        nr
        *
        nz
    )

    diagonal = np.zeros(
        n,
        dtype=float,
    )

    row_blocks = []
    col_blocks = []
    data_blocks = []

    def index(
        j: np.ndarray,
        i: np.ndarray,
    ) -> np.ndarray:
        return (
            (
                j
                -
                1
            )
            *
            nr
            +
            (
                i
                -
                1
            )
        )

    # Interior z edges.
    interior_i = np.arange(
        1,
        n_rho_full
        -
        1,
    )

    interior_j_edge = np.arange(
        1,
        n_z_full
        -
        2,
    )

    jj, ii = np.meshgrid(
        interior_j_edge,
        interior_i,
        indexing="ij",
    )

    k1 = index(
        jj,
        ii,
    ).ravel()

    k2 = index(
        jj
        +
        1,
        ii,
    ).ravel()

    coefficient = (
        rhos[
            ii
        ]
        *
        0.5
        *
        (
            z_coefficient[
                jj,
                ii
            ]
            +
            z_coefficient[
                jj
                +
                1,
                ii
            ]
        )
    ).ravel()

    np.add.at(
        diagonal,
        k1,
        coefficient,
    )

    np.add.at(
        diagonal,
        k2,
        coefficient,
    )

    row_blocks.extend(
        [
            k1,
            k2,
        ]
    )

    col_blocks.extend(
        [
            k2,
            k1,
        ]
    )

    data_blocks.extend(
        [
            -coefficient,
            -coefficient,
        ]
    )

    # Lower and upper z Dirichlet edges.
    interior_i = np.arange(
        1,
        n_rho_full
        -
        1,
    )

    for j_inside, j_boundary in (
        (
            1,
            0,
        ),
        (
            n_z_full
            -
            2,
            n_z_full
            -
            1,
        ),
    ):
        jj_boundary = np.full_like(
            interior_i,
            j_inside,
        )

        k = index(
            jj_boundary,
            interior_i,
        )

        coefficient = (
            rhos[
                interior_i
            ]
            *
            0.5
            *
            (
                z_coefficient[
                    j_inside,
                    interior_i
                ]
                +
                z_coefficient[
                    j_boundary,
                    interior_i
                ]
            )
        )

        np.add.at(
            diagonal,
            k,
            coefficient,
        )

    # Interior radial edges.
    interior_j = np.arange(
        1,
        n_z_full
        -
        1,
    )

    interior_i_edge = np.arange(
        1,
        n_rho_full
        -
        2,
    )

    jj, ii = np.meshgrid(
        interior_j,
        interior_i_edge,
        indexing="ij",
    )

    k1 = index(
        jj,
        ii,
    ).ravel()

    k2 = index(
        jj,
        ii
        +
        1,
    ).ravel()

    rho_edge = (
        0.5
        *
        (
            rhos[
                ii
            ]
            +
            rhos[
                ii
                +
                1
            ]
        )
    )

    z_edge = (
        0.5
        *
        (
            z_coefficient[
                jj,
                ii
            ]
            +
            z_coefficient[
                jj,
                ii
                +
                1
            ]
        )
    )

    base_coefficient = (
        z_edge
        /
        rho_edge
    ).ravel()

    rho_1 = (
        rhos[
            ii
        ]
    ).ravel()

    rho_2 = (
        rhos[
            ii
            +
            1
        ]
    ).ravel()

    np.add.at(
        diagonal,
        k1,
        base_coefficient
        *
        rho_1**2,
    )

    np.add.at(
        diagonal,
        k2,
        base_coefficient
        *
        rho_2**2,
    )

    off_diagonal = (
        -base_coefficient
        *
        rho_1
        *
        rho_2
    )

    row_blocks.extend(
        [
            k1,
            k2,
        ]
    )

    col_blocks.extend(
        [
            k2,
            k1,
        ]
    )

    data_blocks.extend(
        [
            off_diagonal,
            off_diagonal,
        ]
    )

    # Axis Dirichlet edge.
    interior_j = np.arange(
        1,
        n_z_full
        -
        1,
    )

    i_inside = 1
    i_boundary = 0

    k = index(
        interior_j,
        np.full_like(
            interior_j,
            i_inside,
        ),
    )

    rho_edge = (
        0.5
        *
        (
            rhos[
                i_inside
            ]
            +
            rhos[
                i_boundary
            ]
        )
    )

    z_edge = (
        0.5
        *
        (
            z_coefficient[
                interior_j,
                i_inside
            ]
            +
            z_coefficient[
                interior_j,
                i_boundary
            ]
        )
    )

    np.add.at(
        diagonal,
        k,
        (
            z_edge
            /
            rho_edge
            *
            rhos[
                i_inside
            ] ** 2
        ),
    )

    # Outer radial Dirichlet edge.
    i_inside = (
        n_rho_full
        -
        2
    )

    i_boundary = (
        n_rho_full
        -
        1
    )

    k = index(
        interior_j,
        np.full_like(
            interior_j,
            i_inside,
        ),
    )

    rho_edge = (
        0.5
        *
        (
            rhos[
                i_inside
            ]
            +
            rhos[
                i_boundary
            ]
        )
    )

    z_edge = (
        0.5
        *
        (
            z_coefficient[
                interior_j,
                i_inside
            ]
            +
            z_coefficient[
                interior_j,
                i_boundary
            ]
        )
    )

    np.add.at(
        diagonal,
        k,
        (
            z_edge
            /
            rho_edge
            *
            rhos[
                i_inside
            ] ** 2
        ),
    )

    rows = np.concatenate(
        [
            *[
                np.asarray(
                    block
                ).ravel()
                for block in row_blocks
            ],
            np.arange(
                n
            ),
        ]
    )

    cols = np.concatenate(
        [
            *[
                np.asarray(
                    block
                ).ravel()
                for block in col_blocks
            ],
            np.arange(
                n
            ),
        ]
    )

    data = np.concatenate(
        [
            *[
                np.asarray(
                    block
                ).ravel()
                for block in data_blocks
            ],
            diagonal,
        ]
    )

    operator = coo_matrix(
        (
            data,
            (
                rows,
                cols,
            ),
        ),
        shape=(
            n,
            n,
        ),
    ).tocsr()

    rho_i, _ = np.meshgrid(
        rhos[
            1:-1
        ],
        zs[
            1:-1
        ],
    )

    rhs = (
        h**2
        *
        rho_i
        *
        source_profile
    ).ravel()

    return (
        operator,
        rhs,
    )


def operator_structure_gate() -> dict[str, Any]:
    """Check symmetry and positivity on a deterministic small grid."""

    h = 0.5

    rhos, zs, rho_grid, z_grid = (
        _grid(
            h,
            4.0,
            -4.0,
            5.0,
        )
    )

    density = (
        payload_density_profile_kg_m3(
            rho_grid,
            z_grid,
            PRIMARY_DENSITY_MODEL,
        )
    )

    z_coefficient = (
        loading_coefficient_z(
            density,
            1000.0,
        )
    )

    rho_i, z_i = np.meshgrid(
        rhos[
            1:-1
        ],
        zs[
            1:-1
        ],
    )

    source = (
        _source_profile(
            rho_i,
            z_i,
        )
    )

    operator, rhs = (
        _assemble_weighted_operator(
            rhos,
            zs,
            z_coefficient,
            source,
            h,
        )
    )

    asymmetry = (
        operator
        -
        operator.T
    )

    if asymmetry.nnz:
        symmetry_residual = float(
            np.max(
                np.abs(
                    asymmetry.data
                )
            )
        )
    else:
        symmetry_residual = 0.0

    diagonal = (
        operator.diagonal()
    )

    return {
        "symmetric":
            symmetry_residual
            <
            1.0e-12,

        "symmetry_residual":
            symmetry_residual,

        "all_diagonal_positive":
            bool(
                np.all(
                    diagonal
                    >
                    0.0
                )
            ),

        "rhs_finite":
            bool(
                np.all(
                    np.isfinite(
                        rhs
                    )
                )
            ),

        "z_positive":
            bool(
                np.min(
                    z_coefficient
                )
                >
                0.0
            ),
    }


def _edge_energy_integral(
    field: np.ndarray,
    rhos: np.ndarray,
    z_coefficient: np.ndarray,
) -> float:
    """Return discrete integral of rho Z B^2 over dr dz without 2pi."""

    rho_grid = np.broadcast_to(
        rhos[
            None,
            :
        ],
        field.shape,
    )

    z_difference = (
        field[
            1:,
            :
        ]
        -
        field[
            :-1,
            :
        ]
    )

    z_edge_coefficient = (
        0.5
        *
        (
            z_coefficient[
                1:,
                :
            ]
            +
            z_coefficient[
                :-1,
                :
            ]
        )
    )

    integral_z = float(
        np.sum(
            rho_grid[
                :-1,
                :
            ]
            *
            z_edge_coefficient
            *
            z_difference**2
        )
    )

    q = (
        rho_grid
        *
        field
    )

    q_difference = (
        q[
            :,
            1:
        ]
        -
        q[
            :,
            :-1
        ]
    )

    rho_edge = (
        0.5
        *
        (
            rhos[
                1:
            ]
            +
            rhos[
                :-1
            ]
        )
    )

    radial_edge_coefficient = (
        0.5
        *
        (
            z_coefficient[
                :,
                1:
            ]
            +
            z_coefficient[
                :,
                :-1
            ]
        )
    )

    integral_r = float(
        np.sum(
            radial_edge_coefficient
            /
            rho_edge[
                None,
                :
            ]
            *
            q_difference**2
        )
    )

    return (
        integral_z
        +
        integral_r
    )


def _sample_payload_acceleration(
    acceleration: np.ndarray,
    rhos: np.ndarray,
    zs: np.ndarray,
) -> np.ndarray:
    """Interpolate acceleration to fixed payload sample points."""

    interpolator = RegularGridInterpolator(
        (
            zs,
            rhos,
        ),
        acceleration,
        bounds_error=True,
    )

    return np.asarray(
        interpolator(
            _payload_sample_points()
        ),
        dtype=float,
    )


def solve_strong_payload_loading(
    h: float,
    portal_scale_ev: float,
    rho_max_m: float = PRODUCTION_RHO_MAX_M,
    z_min_m: float = PRODUCTION_Z_MIN_M,
    z_max_m: float = PRODUCTION_Z_MAX_M,
    density_model: str = PRIMARY_DENSITY_MODEL,
    include_payload_loading: bool = True,
) -> dict[str, Any]:
    """Solve one static payload-loaded A12 F^2 BVP."""

    h = float(
        h
    )

    portal_scale_ev = float(
        portal_scale_ev
    )

    rhos, zs, rho_grid, z_grid = (
        _grid(
            h,
            rho_max_m,
            z_min_m,
            z_max_m,
        )
    )

    density = (
        payload_density_profile_kg_m3(
            rho_grid,
            z_grid,
            density_model,
        )
    )

    if include_payload_loading:
        z_coefficient = (
            loading_coefficient_z(
                density,
                portal_scale_ev,
            )
        )
    else:
        z_coefficient = np.ones_like(
            density,
            dtype=float,
        )

    rho_i, z_i = np.meshgrid(
        rhos[
            1:-1
        ],
        zs[
            1:-1
        ],
    )

    source_i = (
        _source_profile(
            rho_i,
            z_i,
        )
    )

    operator, rhs = (
        _assemble_weighted_operator(
            rhos,
            zs,
            z_coefficient,
            source_i,
            h,
        )
    )

    solution = spsolve(
        operator,
        rhs,
    )

    if not np.all(
        np.isfinite(
            solution
        )
    ):
        raise RuntimeError(
            "nonfinite loaded field solution"
        )

    field = np.zeros_like(
        rho_grid,
        dtype=float,
    )

    field[
        1:-1,
        1:-1,
    ] = solution.reshape(
        (
            len(
                zs
            )
            -
            2,
            len(
                rhos
            )
            -
            2,
        )
    )

    source = np.zeros_like(
        field
    )

    source[
        1:-1,
        1:-1,
    ] = source_i

    d_a_dz, d_a_drho = np.gradient(
        field,
        h,
        h,
        edge_order=2,
    )

    b_rho = (
        -d_a_dz
    )

    a_over_rho = np.zeros_like(
        field
    )

    np.divide(
        field,
        rho_grid,
        out=a_over_rho,
        where=
            rho_grid
            >
            0.0,
    )

    b_z = (
        d_a_drho
        +
        a_over_rho
    )

    b_squared = (
        b_rho**2
        +
        b_z**2
    )

    sigma_unit = (
        HBAR_C_EV_M**2
        *
        b_squared
        /
        portal_scale_ev**4
    )

    d_sigma_dz, _ = np.gradient(
        sigma_unit,
        h,
        h,
        edge_order=2,
    )

    acceleration_unit = (
        -C_LIGHT_M_S**2
        *
        d_sigma_dz
    )

    sampled_unit = (
        _sample_payload_acceleration(
            acceleration_unit,
            rhos,
            zs,
        )
    )

    minimum_unit = float(
        np.min(
            sampled_unit
        )
    )

    maximum_unit = float(
        np.max(
            sampled_unit
        )
    )

    base = {
        "grid_spacing_m":
            h,

        "rho_max_m":
            rho_max_m,

        "z_min_m":
            z_min_m,

        "z_max_m":
            z_max_m,

        "grid_n_rho":
            len(
                rhos
            ),

        "grid_n_z":
            len(
                zs
            ),

        "portal_scale_ev":
            portal_scale_ev,

        "density_model":
            density_model,

        "payload_loading_included":
            include_payload_loading,

        "geometric_external_standoff_m":
            geometric_standoff_m(),

        "z_min":
            float(
                np.min(
                    z_coefficient
                )
            ),

        "z_max":
            float(
                np.max(
                    z_coefficient
                )
            ),

        "unit_source_payload_acceleration_min_m_s2":
            minimum_unit,

        "unit_source_payload_acceleration_max_m_s2":
            maximum_unit,

        "unit_source_whole_payload_outward_sign":
            minimum_unit
            >
            0.0,

        "normalizable_to_whole_payload_1g":
            minimum_unit
            >
            0.0,

        "complete_energy_established":
            False,
    }

    if minimum_unit <= 0.0:
        return base

    source_scale = math.sqrt(
        TARGET_ACCELERATION_M_S2
        /
        minimum_unit
    )

    field_scaled = (
        source_scale
        *
        field
    )

    source_scaled = (
        source_scale
        *
        source
    )

    b_squared_scaled = (
        source_scale**2
        *
        b_squared
    )

    sigma = (
        source_scale**2
        *
        sigma_unit
    )

    acceleration = (
        source_scale**2
        *
        acceleration_unit
    )

    sampled_acceleration = (
        source_scale**2
        *
        sampled_unit
    )

    canonical_integral = (
        _edge_energy_integral(
            field_scaled,
            rhos,
            np.ones_like(
                z_coefficient
            ),
        )
    )

    loaded_integral = (
        _edge_energy_integral(
            field_scaled,
            rhos,
            z_coefficient,
        )
    )

    energy_conversion = (
        0.5
        *
        2.0
        *
        math.pi
        /
        HBAR_C_EV_M
        *
        EV_J
    )

    canonical_field_energy_j = (
        energy_conversion
        *
        canonical_integral
    )

    loaded_quadratic_capacity_j = (
        energy_conversion
        *
        loaded_integral
    )

    payload_interaction_energy_j = (
        loaded_quadratic_capacity_j
        -
        canonical_field_energy_j
    )

    source_work_j = (
        0.5
        *
        2.0
        *
        math.pi
        *
        float(
            np.sum(
                rho_grid
                *
                source_scaled
                *
                field_scaled
            )
        )
        *
        h**2
        /
        HBAR_C_EV_M
        *
        EV_J
    )

    source_work_relative_error = (
        abs(
            source_work_j
            -
            loaded_quadratic_capacity_j
        )
        /
        loaded_quadratic_capacity_j
    )

    integrated_source_ev_m = (
        2.0
        *
        math.pi
        *
        float(
            np.sum(
                rho_grid
                *
                source_scaled
            )
        )
        *
        h**2
    )

    cylindrical_volume_weights = (
        2.0
        *
        math.pi
        *
        rho_grid
        *
        h**2
    )

    discrete_payload_mass_kg = float(
        np.sum(
            density
            *
            cylindrical_volume_weights
        )
    )

    mass_weight = (
        density
        *
        cylindrical_volume_weights
    )

    mass_weight_sum = float(
        np.sum(
            mass_weight
        )
    )

    payload_com_acceleration = float(
        np.sum(
            mass_weight
            *
            acceleration
        )
        /
        mass_weight_sum
    )

    exact_payload_conformal_shift_j = float(
        np.sum(
            density
            *
            C_LIGHT_M_S**2
            *
            np.expm1(
                sigma
            )
            *
            cylindrical_volume_weights
        )
    )

    payload_mask = (
        density
        >
        0.0
    )

    sigma_max = float(
        np.max(
            sigma[
                payload_mask
            ]
        )
    )

    sigma_min = float(
        np.min(
            sigma[
                payload_mask
            ]
        )
    )

    exact_z_exponential_fractional_correction_max = float(
        abs(
            math.expm1(
                4.0
                *
                sigma_max
            )
        )
    )

    a12c = (
        a12c_artifact()
    )

    a12c_production = (
        a12c[
            "massless_f2_finite_payload_bvp"
        ][
            "production"
        ]
    )

    a12c_source = float(
        a12c_production[
            "integrated_canonical_source_ev_m"
        ]
    )

    a12c_field_energy = float(
        a12c_production[
            "field_energy_j"
        ]
    )

    return {
        **base,

        "source_amplitude_e_v_per_m2":
            source_scale,

        "payload_local_acceleration_min_m_s2":
            float(
                np.min(
                    sampled_acceleration
                )
            ),

        "payload_local_acceleration_max_m_s2":
            float(
                np.max(
                    sampled_acceleration
                )
            ),

        "payload_com_acceleration_m_s2":
            payload_com_acceleration,

        "strict_whole_payload_1g_pass":
            bool(
                np.min(
                    sampled_acceleration
                )
                >=
                TARGET_ACCELERATION_M_S2
                *
                (
                    1.0
                    -
                    1.0e-11
                )
            ),

        "canonical_field_energy_j":
            canonical_field_energy_j,

        "payload_interaction_energy_j":
            payload_interaction_energy_j,

        "loaded_quadratic_capacity_j":
            loaded_quadratic_capacity_j,

        "source_work_j":
            source_work_j,

        "source_work_relative_error":
            source_work_relative_error,

        "exact_payload_conformal_shift_j":
            exact_payload_conformal_shift_j,

        "payload_interaction_vs_exact_shift_relative_error":
            (
                abs(
                    payload_interaction_energy_j
                    -
                    exact_payload_conformal_shift_j
                )
                /
                max(
                    abs(
                        exact_payload_conformal_shift_j
                    ),
                    1.0e-300,
                )
            ),

        "integrated_canonical_source_ev_m":
            integrated_source_ev_m,

        "integrated_source_ratio_vs_a12c":
            (
                integrated_source_ev_m
                /
                a12c_source
            ),

        "loaded_capacity_ratio_vs_a12c_field_reference":
            (
                loaded_quadratic_capacity_j
                /
                a12c_field_energy
            ),

        "discrete_payload_mass_kg":
            discrete_payload_mass_kg,

        "payload_sigma_min":
            sigma_min,

        "payload_sigma_max":
            sigma_max,

        "exact_z_exponential_fractional_correction_max":
            exact_z_exponential_fractional_correction_max,

        "small_sigma_expansion_self_consistent":
            exact_z_exponential_fractional_correction_max
            <
            1.0e-10,

        "loaded_capacity_strictly_below_10mj":
            loaded_quadratic_capacity_j
            <
            STRICT_COMPLETE_OPERATING_TARGET_J,

        "loaded_capacity_below_1mj":
            loaded_quadratic_capacity_j
            <
            SUB_MJ_CAPACITY_J,

        "loaded_capacity_below_10kj":
            loaded_quadratic_capacity_j
            <
            LOW_KJ_CAPACITY_J,

        "loaded_capacity_below_100j":
            loaded_quadratic_capacity_j
            <
            LOW_CAPACITY_J,

        "complete_energy_established":
            False,
    }


def unloaded_reconstruction_gate() -> dict[str, Any]:
    """Independently reconstruct A12C using the new variational solver."""

    result = (
        solve_strong_payload_loading(
            h=BROAD_SCAN_GRID_M,
            portal_scale_ev=REFERENCE_PORTAL_SCALE_EV,
            density_model=PRIMARY_DENSITY_MODEL,
            include_payload_loading=False,
        )
    )

    a12c = (
        a12c_artifact()
    )

    production = (
        a12c[
            "massless_f2_finite_payload_bvp"
        ][
            "production"
        ]
    )

    reference_energy = float(
        production[
            "field_energy_j"
        ]
    )

    reference_source = float(
        production[
            "integrated_canonical_source_ev_m"
        ]
    )

    energy_relerr = (
        abs(
            result[
                "canonical_field_energy_j"
            ]
            -
            reference_energy
        )
        /
        reference_energy
    )

    source_relerr = (
        abs(
            result[
                "integrated_canonical_source_ev_m"
            ]
            -
            reference_source
        )
        /
        reference_source
    )

    passed = bool(
        result[
            "strict_whole_payload_1g_pass"
        ]
        and
        energy_relerr
        <
        UNLOADED_RECONSTRUCTION_ENERGY_TOL
        and
        source_relerr
        <
        UNLOADED_RECONSTRUCTION_SOURCE_TOL
        and
        result[
            "source_work_relative_error"
        ]
        <
        1.0e-10
    )

    return {
        "pass":
            passed,

        "new_solver_result":
            result,

        "a12c_reference_field_energy_j":
            reference_energy,

        "a12c_reference_integrated_source_ev_m":
            reference_source,

        "field_energy_relative_error":
            energy_relerr,

        "integrated_source_relative_error":
            source_relerr,
    }


def provenance_gate() -> dict[str, Any]:
    """Require A12C low-capacity mechanism and completed A12D1 loading theorem."""

    a12c = (
        a12c_artifact()
    )

    a12d1_disk = (
        a12d1_artifact()
    )

    a12d1_live = (
        h17a12d1_summary()
    )

    passed = bool(
        a12c[
            "branch"
        ]
        ==
        "032H17A12C"

        and

        a12c[
            "gauge_invariant_massless_f2_reduced_eft_1g_1m_witness"
        ]
        is True

        and

        a12c[
            "a12b_exact_massless_carrier_closed"
        ]
        is False

        and

        a12d1_disk[
            "branch"
        ]
        ==
        "032H17A12D1"

        and

        a12d1_disk[
            "minimal_electron_pauli_perturbative_kernel_reuse_closed"
        ]
        is True

        and

        a12d1_disk[
            "a12c_gauge_invariant_f2_metric_mechanism_closed"
        ]
        is False

        and

        a12d1_live[
            "minimal_electron_pauli_perturbative_kernel_reuse_closed"
        ]
        is True

        and

        a12d1_live[
            "a12c_gauge_invariant_f2_metric_mechanism_closed"
        ]
        is False
    )

    return {
        "pass":
            passed,

        "a12c_branch":
            a12c[
                "branch"
            ],

        "a12d1_branch":
            a12d1_disk[
                "branch"
            ],

        "a12c_low_capacity_mechanism_preserved":
            not a12d1_disk[
                "a12c_gauge_invariant_f2_metric_mechanism_closed"
            ],

        "a12d1_closed_only_perturbative_pauli_kernel_reuse":
            a12d1_disk[
                "minimal_electron_pauli_perturbative_kernel_reuse_closed"
            ],

        "strongly_loaded_solution_was_closed_by_a12d1":
            a12d1_disk[
                "strongly_loaded_pauli_rescue_closed"
            ],
    }


def claim_policy_gate() -> dict[str, Any]:
    """Permanent claim limits for this rescue branch."""

    return {
        "a12b_carrier_modified":
            False,

        "a12c_metric_function_modified":
            False,

        "a12c_source_geometry_modified":
            False,

        "a12c_payload_support_geometry_modified":
            False,

        "new_physics_inserted_to_force_success":
            False,

        "payload_backreaction_added":
            True,

        "microscopic_source_backreaction_added":
            False,

        "source_physicalization_established":
            False,

        "complete_energy_established":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "006d_replaced":
            False,

        "practical_device_found":
            False,
    }
