"""
031B1-B0
========

Exact nonlinear Z2 e4 self-consistency and B7 virial-burden gate.

PURPOSE
-------
031B1-A found that the existing B7 e4 sector is the unique strong one-sector
fixed-field survivor at the established R4S operating sensitivity:

    target energy ~= 8.2750782e10 J
    alpha_m(on)  ~= 27.0079
    |alpha_X|    ~= 1.93027e17
    lambda_phi   = 3.3 m.

The fixed-field scout attributed scalar charge to e4 but did NOT yet prove
that a local nonlinear coupling can generate that sensitivity.

This run replaces the assigned e4 sensitivity with the explicit minimal Z2
coupling

    c4(phi) = exp[-phi^2/(2 M4^2)]

in the physical B7 e4 energy density.

At fixed B7 field the scalar equation is

    (-nabla^2 + m_phi^2) phi
        =
        epsilon4(x)
        * phi/M4^2
        * exp[-phi^2/(2 M4^2)].

Define

    u = phi/M4

and

    kappa = E_core / M4^2.

Then the nonlinear equation for u is independent of M4 at fixed kappa.

This allows a one-dimensional scalarization scan instead of an arbitrary
two-dimensional coupling campaign.

The scan derives M4 from the physical 1g requirement and then calculates:

    E_core
    E_phi
    E_total_conservative = E_core_off + E_phi

without crediting the reduction of dressed e4 energy as free cancellation.

The source profile is the radial average of the actual N73/N81 e4 density.
031B1-A already found essentially orientation-independent stand-off leverage;
the exact orientation spread is read from its saved CSV and enforced as a
radialization precondition.

The run also calculates the amount by which c4(phi) weakens the B7 Skyrme
term and therefore the Derrick/virial burden that the later full 3-D
re-equilibration must absorb.

THIS RUN DOES NOT
-----------------
- re-equilibrate B7;
- establish full B7+scalar stationarity;
- establish full local conservation;
- establish coupled nonradial stability;
- establish EFT/radiative naturalness;
- establish empirical fifth-force closure;
- supersede 026C N89;
- establish a practical device.

A GREEN result authorizes the expensive 031B1-B1 full 3-D coupled
B7+scalar re-equilibration.

A RED result means the constant-sensitivity B7 result does not survive the
minimal exact local Z2 realization and we should run the independent Q-ball /
Q-shell control before inventing extra B7 operators.
"""

from __future__ import annotations

import csv
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np

from scipy.integrate import solve_bvp
from scipy.interpolate import PchipInterpolator
from scipy.ndimage import gaussian_filter1d
from scipy.optimize import brentq
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results/data"

B1A_SOURCE = (
    SIM
    /
    "031b1a_b7_fixed_field_z2_charge_tomography.py"
)

CR3_SOURCE = (
    SIM
    /
    "023cr3_geometric_degree_guarded_unrestricted_relaxation.py"
)

R4S_SUMMARY = (
    DATA
    /
    "031a_r4s_z2_scaling_83gj_recovery_summary.json"
)

B1A_SUMMARY = (
    DATA
    /
    "031b1a_b7_fixed_field_z2_charge_tomography_summary.json"
)

B1A_CSV = (
    DATA
    /
    "031b1a_b7_fixed_field_z2_charge_tomography.csv"
)

N73_FIELD = (
    DATA
    /
    "026a_true_antigravity_strict_stationary_b7_n73.npz"
)

N81_FIELD = (
    DATA
    /
    "026b_true_antigravity_strict_stationary_b7_n81.npz"
)

OUT_JSON = (
    DATA
    /
    "031b1b0_b7_e4_exact_z2_selfconsistency_summary.json"
)

OUT_CSV = (
    DATA
    /
    "031b1b0_b7_e4_exact_z2_selfconsistency_scan.csv"
)


G = 6.67430e-11
C = 299_792_458.0
G0 = 9.80665

MPL_GEV = 2.435e18

HBARC_GEV_M = 1.973269804e-16

J_PER_GEV = 1.602176634e-10

L_PER_M = 1.0 / HBARC_GEV_M

J_M3_TO_GEV4 = (
    (1.0 / J_PER_GEV)
    *
    HBARC_GEV_M**3
)


SOURCE_RADIUS_M = 0.95

PAYLOAD_RADIUS_M = 0.10

CLEARANCE_M = 1.00

PAYLOAD_CENTER_M = (
    SOURCE_RADIUS_M
    +
    CLEARANCE_M
    +
    PAYLOAD_RADIUS_M
)

MEDIATOR_RANGE_M = 3.30

M_PHI_GEV = (
    HBARC_GEV_M
    /
    MEDIATOR_RANGE_M
)


RADIAL_BINS = 140

BVP_TOL = 3.0e-5

LINEAR_EIG_N = 1000

HESSIAN_EIG_N = 1200


PAIR_REL_TOL = 5.0e-2

RADIALIZATION_MAX_ORIENTATION_SPREAD = 1.0e-4

ENERGY_REL_MARGIN = 2.0e-3

BACKREACTION_LIMIT = 1.0e-2

SCALAR_ENERGY_IDENTITY_REL_TOL = 3.0e-3


KAPPA_GJ_PER_GEV2 = tuple(
    sorted(
        set(
            list(
                np.geomspace(
                    2.5e-3,
                    1.2e-1,
                    18,
                )
            )
            +
            [
                0.00625,
                0.010,
                0.016,
                0.01875,
                0.03125,
                0.050,
            ]
        )
    )
)


def require(
    path: Path,
) -> None:

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
        or
        spec.loader is None
    ):

        raise RuntimeError(
            f"Cannot import {path}"
        )

    module = importlib.util.module_from_spec(
        spec
    )

    sys.modules[
        spec.name
    ] = module

    spec.loader.exec_module(
        module
    )

    return module


def relerr(
    a: float,
    b: float,
) -> float:

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


def to_builtin(
    value: Any,
):

    if isinstance(
        value,
        np.generic,
    ):

        return value.item()

    if isinstance(
        value,
        np.ndarray,
    ):

        return value.tolist()

    if isinstance(
        value,
        dict,
    ):

        return {
            str(
                key
            ):
            to_builtin(
                item
            )
            for key, item
            in value.items()
        }

    if isinstance(
        value,
        (
            list,
            tuple,
        ),
    ):

        return [
            to_builtin(
                item
            )
            for item
            in value
        ]

    return value


def read_b1a_rows():

    rows = []

    with B1A_CSV.open(
        newline="",
    ) as handle:

        reader = csv.DictReader(
            handle
        )

        for row in reader:

            rows.append(
                row
            )

    return rows


def e4_b1a_row(
    rows,
    grid,
):

    for row in rows:

        if (
            row.get(
                "grid"
            )
            ==
            grid
            and
            row.get(
                "sector"
            )
            ==
            "e4"
        ):

            return row

    raise RuntimeError(
        f"Missing e4 row for {grid}"
    )


def make_radial_profile(
    reconstructed,
):

    xyz = reconstructed[
        "xyz_m"
    ]

    radius = np.linalg.norm(
        xyz,
        axis=1,
    )

    e4_weights = reconstructed[
        "sector_fraction_cells"
    ][
        "e4"
    ]

    total_weights = reconstructed[
        "total_fraction_cells"
    ]

    edges = np.linspace(
        0.0,
        SOURCE_RADIUS_M,
        RADIAL_BINS
        +
        1,
    )

    e4_shell, _ = np.histogram(
        radius,
        bins=edges,
        weights=e4_weights,
    )

    total_shell, _ = np.histogram(
        radius,
        bins=edges,
        weights=total_weights,
    )

    centers = (
        0.5
        *
        (
            edges[
                1:
            ]
            +
            edges[
                :-1
            ]
        )
    )

    shell_volume = (
        4.0
        *
        math.pi
        /
        3.0
        *
        (
            edges[
                1:
            ]**3
            -
            edges[
                :-1
            ]**3
        )
    )

    e4_density = (
        e4_shell
        /
        np.maximum(
            shell_volume,
            1.0e-300,
        )
    )

    total_density = (
        total_shell
        /
        np.maximum(
            shell_volume,
            1.0e-300,
        )
    )

    e4_density = gaussian_filter1d(
        e4_density,
        sigma=1.0,
        mode="nearest",
    )

    total_density = gaussian_filter1d(
        total_density,
        sigma=1.0,
        mode="nearest",
    )

    e4_density = np.maximum(
        e4_density,
        0.0,
    )

    total_density = np.maximum(
        total_density,
        0.0,
    )

    x = np.concatenate(
        (
            [
                0.0
            ],
            centers,
            [
                SOURCE_RADIUS_M
            ],
        )
    )

    e4_y = np.concatenate(
        (
            [
                e4_density[
                    0
                ]
            ],
            e4_density,
            [
                0.0
            ],
        )
    )

    total_y = np.concatenate(
        (
            [
                total_density[
                    0
                ]
            ],
            total_density,
            [
                0.0
            ],
        )
    )

    e4_interp_raw = PchipInterpolator(
        x,
        e4_y,
        extrapolate=False,
    )

    total_interp_raw = PchipInterpolator(
        x,
        total_y,
        extrapolate=False,
    )

    fine_r = np.linspace(
        0.0,
        SOURCE_RADIUS_M,
        4000,
    )

    fine_e4 = np.nan_to_num(
        e4_interp_raw(
            fine_r
        ),
        nan=0.0,
    )

    fine_total = np.nan_to_num(
        total_interp_raw(
            fine_r
        ),
        nan=0.0,
    )

    fine_e4 = np.maximum(
        fine_e4,
        0.0,
    )

    fine_total = np.maximum(
        fine_total,
        0.0,
    )

    e4_integral_raw = float(
        np.trapezoid(
            4.0
            *
            math.pi
            *
            fine_r**2
            *
            fine_e4,
            fine_r,
        )
    )

    total_integral_raw = float(
        np.trapezoid(
            4.0
            *
            math.pi
            *
            fine_r**2
            *
            fine_total,
            fine_r,
        )
    )

    exact_e4_fraction = float(
        np.sum(
            e4_weights
        )
    )

    e4_norm = (
        exact_e4_fraction
        /
        max(
            e4_integral_raw,
            1.0e-300,
        )
    )

    total_norm = (
        1.0
        /
        max(
            total_integral_raw,
            1.0e-300,
        )
    )

    def p4(
        r,
    ):

        rr = np.asarray(
            r,
            dtype=float,
        )

        value = np.nan_to_num(
            e4_interp_raw(
                rr
            ),
            nan=0.0,
        )

        value = (
            e4_norm
            *
            np.maximum(
                value,
                0.0,
            )
        )

        value = np.where(
            (
                rr
                >=
                0.0
            )
            &
            (
                rr
                <=
                SOURCE_RADIUS_M
            ),
            value,
            0.0,
        )

        return value

    def ptotal(
        r,
    ):

        rr = np.asarray(
            r,
            dtype=float,
        )

        value = np.nan_to_num(
            total_interp_raw(
                rr
            ),
            nan=0.0,
        )

        value = (
            total_norm
            *
            np.maximum(
                value,
                0.0,
            )
        )

        value = np.where(
            (
                rr
                >=
                0.0
            )
            &
            (
                rr
                <=
                SOURCE_RADIUS_M
            ),
            value,
            0.0,
        )

        return value

    check_e4 = float(
        np.trapezoid(
            4.0
            *
            math.pi
            *
            fine_r**2
            *
            p4(
                fine_r
            ),
            fine_r,
        )
    )

    check_total = float(
        np.trapezoid(
            4.0
            *
            math.pi
            *
            fine_r**2
            *
            ptotal(
                fine_r
            ),
            fine_r,
        )
    )

    centroid = np.sum(
        e4_weights[
            :,
            None
        ]
        *
        xyz,
        axis=0,
    ) / max(
        exact_e4_fraction,
        1.0e-300,
    )

    second = np.einsum(
        "n,ni,nj->ij",
        e4_weights,
        xyz,
        xyz,
    )

    second /= max(
        np.sum(
            e4_weights
        ),
        1.0e-300,
    )

    eig = np.linalg.eigvalsh(
        second
    )

    inertia_anisotropy = float(
        (
            np.max(
                eig
            )
            -
            np.min(
                eig
            )
        )
        /
        max(
            np.mean(
                eig
            ),
            1.0e-300,
        )
    )

    return {
        "p4":
        p4,

        "ptotal":
        ptotal,

        "e4_fraction":
        exact_e4_fraction,

        "e4_integral_check":
        check_e4,

        "total_integral_check":
        check_total,

        "e4_centroid_norm_m":
        float(
            np.linalg.norm(
                centroid
            )
        ),

        "e4_second_moment_anisotropy":
        inertia_anisotropy,
    }


def radial_operator_lowest(
    profile,
    kappa_j_per_gev2,
    nonlinear_solution=None,
):

    rmax = (
        SOURCE_RADIUS_M
        +
        6.0
        *
        MEDIATOR_RANGE_M
    )

    n = (
        HESSIAN_EIG_N
        if nonlinear_solution
        is not None
        else
        LINEAR_EIG_N
    )

    r = np.linspace(
        0.0,
        rmax,
        n,
    )

    h = (
        r[
            1
        ]
        -
        r[
            0
        ]
    )

    ri = r[
        1:-1
    ]

    source_coeff = (
        kappa_j_per_gev2
        *
        J_M3_TO_GEV4
        *
        profile[
            "p4"
        ](
            ri
        )
    )

    if nonlinear_solution is None:

        curvature_gev2 = (
            M_PHI_GEV**2
            -
            source_coeff
        )

    else:

        u = nonlinear_solution.sol(
            np.maximum(
                ri,
                1.0e-8,
            )
        )[
            0
        ]

        c4 = np.exp(
            np.clip(
                -0.5
                *
                u**2,
                -700.0,
                0.0,
            )
        )

        curvature_gev2 = (
            M_PHI_GEV**2
            +
            source_coeff
            *
            c4
            *
            (
                u**2
                -
                1.0
            )
        )

    potential_m2inv = (
        L_PER_M**2
        *
        curvature_gev2
    )

    diagonal = (
        2.0
        /
        h**2
        +
        potential_m2inv
    )

    off = (
        -np.ones(
            len(
                ri
            )
            -
            1
        )
        /
        h**2
    )

    op = diags(
        (
            off,
            diagonal,
            off,
        ),
        (
            -1,
            0,
            1,
        ),
        format="csr",
    )

    eig = eigsh(
        op,
        k=1,
        which="SA",
        return_eigenvectors=False,
        tol=1.0e-8,
    )[
        0
    ]

    return float(
        eig
    )


def solve_u_branch(
    profile,
    kappa_j_per_gev2,
):

    linear_eig = radial_operator_lowest(
        profile,
        kappa_j_per_gev2,
        None,
    )

    if linear_eig >= 0.0:

        return {
            "success":
            False,

            "reason":
            "TRIVIAL_BRANCH_LINEarly_STABLE",

            "linear_eigenvalue_m2inv":
            linear_eig,
        }

    rmax = (
        SOURCE_RADIUS_M
        +
        8.0
        *
        MEDIATOR_RANGE_M
    )

    r = np.unique(
        np.concatenate(
            (
                np.linspace(
                    1.0e-6,
                    SOURCE_RADIUS_M,
                    280,
                ),
                np.linspace(
                    SOURCE_RADIUS_M,
                    rmax,
                    360,
                ),
            )
        )
    )

    source_coeff_scale = (
        kappa_j_per_gev2
        *
        J_M3_TO_GEV4
    )

    def equations(
        rr,
        y,
    ):

        u = y[
            0
        ]

        c4 = np.exp(
            np.clip(
                -0.5
                *
                u**2,
                -700.0,
                0.0,
            )
        )

        rhs = (
            M_PHI_GEV**2
            *
            u
            -
            source_coeff_scale
            *
            profile[
                "p4"
            ](
                rr
            )
            *
            u
            *
            c4
        )

        return np.vstack(
            (
                y[
                    1
                ],
                L_PER_M**2
                *
                rhs
                -
                2.0
                *
                y[
                    1
                ]
                /
                rr,
            )
        )

    def bc(
        left,
        right,
    ):

        return np.array(
            (
                left[
                    1
                ],
                right[
                    0
                ],
            )
        )

    candidates = []

    for amplitude in (
        0.35,
        0.75,
        1.25,
        2.0,
        3.0,
        4.0,
    ):

        inside = np.exp(
            -(
                r
                /
                max(
                    SOURCE_RADIUS_M,
                    1.0e-6,
                )
            )**4
        )

        tail = np.exp(
            -np.maximum(
                r
                -
                SOURCE_RADIUS_M,
                0.0,
            )
            /
            MEDIATOR_RANGE_M
        )

        guess_u = (
            amplitude
            *
            inside
            *
            tail
        )

        guess_du = np.gradient(
            guess_u,
            r,
        )

        solution = solve_bvp(
            equations,
            bc,
            r,
            np.vstack(
                (
                    guess_u,
                    guess_du,
                )
            ),
            tol=BVP_TOL,
            max_nodes=25_000,
            verbose=0,
        )

        if not solution.success:

            continue

        u0 = abs(
            float(
                solution.sol(
                    1.0e-6
                )[
                    0
                ]
            )
        )

        if u0 < 1.0e-4:

            continue

        scalar_eig = radial_operator_lowest(
            profile,
            kappa_j_per_gev2,
            solution,
        )

        candidates.append(
            (
                scalar_eig,
                u0,
                solution,
            )
        )

    if not candidates:

        return {
            "success":
            False,

            "reason":
            "NONTRIVIAL_BRANCH_NOT_FOUND",

            "linear_eigenvalue_m2inv":
            linear_eig,
        }

    stable = [
        item
        for item
        in candidates
        if item[
            0
        ]
        >
        0.0
    ]

    if stable:

        chosen = min(
            stable,
            key=lambda item:
            abs(
                item[
                    1
                ]
            ),
        )

    else:

        chosen = max(
            candidates,
            key=lambda item:
            item[
                0
            ],
        )

    scalar_eig, u0, solution = chosen

    return {
        "success":
        True,

        "solution":
        solution,

        "linear_eigenvalue_m2inv":
        linear_eig,

        "scalar_hessian_eigenvalue_m2inv":
        scalar_eig,

        "scalar_radial_stability":
        bool(
            scalar_eig
            >
            0.0
        ),

        "u_center":
        u0,
    }


def energy_coefficients(
    profile,
    solution,
    kappa_j_per_gev2,
):

    r = np.linspace(
        1.0e-6,
        solution.x[
            -1
        ],
        7000,
    )

    u, du = solution.sol(
        r
    )

    c4 = np.exp(
        np.clip(
            -0.5
            *
            u**2,
            -700.0,
            0.0,
        )
    )

    p4 = profile[
        "p4"
    ](
        r
    )

    volume = (
        4.0
        *
        math.pi
        *
        r**2
    )

    e4_on_fraction = float(
        np.trapezoid(
            p4
            *
            c4
            *
            volume,
            r,
        )
    )

    u2c4_integral = float(
        np.trapezoid(
            p4
            *
            u**2
            *
            c4
            *
            volume,
            r,
        )
    )

    E_phi_identity_coeff = (
        0.5
        *
        kappa_j_per_gev2
        *
        u2c4_integral
    )

    gradient_density_gev4 = (
        0.5
        *
        (
            du
            /
            L_PER_M
        )**2
    )

    mass_density_gev4 = (
        0.5
        *
        M_PHI_GEV**2
        *
        u**2
    )

    E_phi_direct_coeff = float(
        np.trapezoid(
            (
                gradient_density_gev4
                +
                mass_density_gev4
            )
            /
            J_M3_TO_GEV4
            *
            volume,
            r,
        )
    )

    identity_relerr = relerr(
        E_phi_identity_coeff,
        E_phi_direct_coeff,
    )

    f4 = profile[
        "e4_fraction"
    ]

    non_e4_coeff = (
        kappa_j_per_gev2
        *
        (
            1.0
            -
            f4
        )
    )

    e4_on_coeff = (
        kappa_j_per_gev2
        *
        e4_on_fraction
    )

    E_on_coeff = (
        non_e4_coeff
        +
        e4_on_coeff
        +
        E_phi_direct_coeff
    )

    E_conservative_coeff = (
        kappa_j_per_gev2
        +
        E_phi_direct_coeff
    )

    e4_c4_mean = (
        e4_on_fraction
        /
        max(
            f4,
            1.0e-300,
        )
    )

    return {
        "E_phi_identity_coeff_J_per_GeV2":
        E_phi_identity_coeff,

        "E_phi_direct_coeff_J_per_GeV2":
        E_phi_direct_coeff,

        "scalar_energy_identity_relerr":
        identity_relerr,

        "e4_on_fraction_total_core":
        e4_on_fraction,

        "e4_c4_weighted_mean":
        e4_c4_mean,

        "E_on_coeff_J_per_GeV2":
        E_on_coeff,

        "E_conservative_coeff_J_per_GeV2":
        E_conservative_coeff,
    }


def scalar_unit_response(
    solution,
    E_on_coeff,
    alpha_m_cap,
):

    near_radius = (
        PAYLOAD_CENTER_M
        -
        PAYLOAD_RADIUS_M
    )

    u_near = abs(
        float(
            solution.sol(
                near_radius
            )[
                0
            ]
        )
    )

    if u_near <= 1.0e-14:

        return {
            "success":
            False,

            "reason":
            "VANISHING_PAYLOAD_FIELD",
        }

    def a_scalar_unit(
        radius,
    ):

        u, du = solution.sol(
            radius
        )

        return float(
            -C**2
            *
            alpha_m_cap
            *
            u
            *
            du
            /
            (
                MPL_GEV
                *
                u_near
            )
        )

    def a_gr_coeff(
        radius,
    ):

        return (
            G
            *
            (
                E_on_coeff
                /
                C**2
            )
            /
            radius**2
        )

    surface_radii = (
        PAYLOAD_CENTER_M
        -
        PAYLOAD_RADIUS_M,
        PAYLOAD_CENTER_M,
        PAYLOAD_CENTER_M
        +
        PAYLOAD_RADIUS_M,
    )

    scalar_surface_unit = [
        a_scalar_unit(
            radius
        )
        for radius
        in surface_radii
    ]

    gr_surface_coeff = [
        a_gr_coeff(
            radius
        )
        for radius
        in surface_radii
    ]

    radial_nodes, radial_weights = np.polynomial.legendre.leggauss(
        18
    )

    angular_nodes, angular_weights = np.polynomial.legendre.leggauss(
        22
    )

    payload_radii = (
        0.5
        *
        PAYLOAD_RADIUS_M
        *
        (
            radial_nodes
            +
            1.0
        )
    )

    payload_weights = (
        0.5
        *
        PAYLOAD_RADIUS_M
        *
        radial_weights
    )

    volume_payload = (
        4.0
        *
        math.pi
        *
        PAYLOAD_RADIUS_M**3
        /
        3.0
    )

    scalar_integral = 0.0

    for s, ws in zip(
        payload_radii,
        payload_weights,
    ):

        for mu, wmu in zip(
            angular_nodes,
            angular_weights,
        ):

            radius = math.sqrt(
                PAYLOAD_CENTER_M**2
                +
                s**2
                +
                2.0
                *
                PAYLOAD_CENTER_M
                *
                s
                *
                mu
            )

            projection = (
                PAYLOAD_CENTER_M
                +
                s
                *
                mu
            ) / radius

            scalar_integral += (
                2.0
                *
                math.pi
                *
                s**2
                *
                ws
                *
                wmu
                *
                a_scalar_unit(
                    radius
                )
                *
                projection
            )

    scalar_cm_unit = (
        scalar_integral
        /
        volume_payload
    )

    gr_cm_coeff = (
        G
        *
        (
            E_on_coeff
            /
            C**2
        )
        /
        PAYLOAD_CENTER_M**2
    )

    return {
        "success":
        True,

        "u_near_payload":
        u_near,

        "scalar_surface_unit_per_GeV":
        scalar_surface_unit,

        "gr_surface_coeff_per_GeV2":
        gr_surface_coeff,

        "scalar_cm_unit_per_GeV":
        scalar_cm_unit,

        "gr_cm_coeff_per_GeV2":
        gr_cm_coeff,
    }


def solve_required_m4(
    response,
):

    scalar = response[
        "scalar_surface_unit_per_GeV"
    ]

    gr = response[
        "gr_surface_coeff_per_GeV2"
    ]

    def adverse_net(
        m4,
    ):

        return min(
            scalar[
                index
            ]
            *
            m4
            -
            gr[
                index
            ]
            *
            m4**2
            for index
            in range(
                len(
                    scalar
                )
            )
        )

    lower = 1.0e-4

    upper = 1.0

    while (
        adverse_net(
            upper
        )
        <
        G0
        and
        upper
        <
        1.0e5
    ):

        upper *= 1.5

    if adverse_net(
        upper
    ) < G0:

        return {
            "success":
            False,

            "reason":
            "NO_1G_ROOT",
        }

    root = brentq(
        lambda m4:
        adverse_net(
            m4
        )
        -
        G0,
        lower,
        upper,
        xtol=1.0e-11,
        rtol=1.0e-12,
        maxiter=300,
    )

    net_surface = [
        scalar[
            index
        ]
        *
        root
        -
        gr[
            index
        ]
        *
        root**2
        for index
        in range(
            len(
                scalar
            )
        )
    ]

    net_cm = (
        response[
            "scalar_cm_unit_per_GeV"
        ]
        *
        root
        -
        response[
            "gr_cm_coeff_per_GeV2"
        ]
        *
        root**2
    )

    return {
        "success":
        True,

        "M4_GeV":
        root,

        "a_surface_mps2":
        net_surface,

        "a_adverse_mps2":
        min(
            net_surface
        ),

        "a_cm_mps2":
        net_cm,
    }


def payload_backreaction(
    M4_GeV,
    u_near,
    alpha_m_cap,
    density_kg_m3=8000.0,
):

    Mm2 = (
        MPL_GEV
        *
        M4_GeV
        *
        u_near
        /
        alpha_m_cap
    )

    rho_energy_j_m3 = (
        density_kg_m3
        *
        C**2
    )

    rho_energy_gev4 = (
        rho_energy_j_m3
        *
        J_M3_TO_GEV4
    )

    ratio = (
        rho_energy_gev4
        /
        (
            Mm2
            *
            M_PHI_GEV**2
        )
    )

    return {
        "M_m_GeV":
        math.sqrt(
            Mm2
        ),

        "payload_backreaction_ratio":
        ratio,
    }


def derrick_diagnostics(
    reconstructed,
    e4_c4_mean,
):

    E2 = float(
        reconstructed[
            "energies"
        ][
            "e2"
        ]
    )

    E4 = float(
        reconstructed[
            "energies"
        ][
            "e4"
        ]
    )

    V = float(
        reconstructed[
            "energies"
        ][
            "V"
        ]
    )

    dressed_E4 = (
        e4_c4_mean
        *
        E4
    )

    residual = (
        E2
        -
        dressed_E4
        +
        3.0
        *
        V
    )

    dressed_energy = (
        E2
        +
        dressed_E4
        +
        V
    )

    relative = (
        abs(
            residual
        )
        /
        max(
            dressed_energy,
            1.0e-300,
        )
    )

    disc = (
        E2**2
        +
        12.0
        *
        V
        *
        dressed_E4
    )

    x = (
        -E2
        +
        math.sqrt(
            max(
                disc,
                0.0,
            )
        )
    ) / max(
        6.0
        *
        V,
        1.0e-300,
    )

    lambda_est = math.sqrt(
        max(
            x,
            0.0,
        )
    )

    if relative < 0.10:

        burden = "MILD"

    elif relative < 0.40:

        burden = "SUBSTANTIAL"

    else:

        burden = "SEVERE"

    return {
        "derrick_residual":
        residual,

        "derrick_relative_burden":
        relative,

        "uniform_scale_estimate":
        lambda_est,

        "reequilibration_burden":
        burden,
    }


def evaluate_kappa(
    profile,
    reconstructed,
    kappa_gj_per_gev2,
    alpha_m_cap,
):

    kappa = (
        kappa_gj_per_gev2
        *
        1.0e9
    )

    branch = solve_u_branch(
        profile,
        kappa,
    )

    if not branch.get(
        "success",
        False,
    ):

        return {
            "success":
            False,

            "kappa_GJ_per_GeV2":
            kappa_gj_per_gev2,

            **{
                key:
                value
                for key, value
                in branch.items()
                if key
                !=
                "solution"
            },
        }

    solution = branch[
        "solution"
    ]

    energy = energy_coefficients(
        profile,
        solution,
        kappa,
    )

    response = scalar_unit_response(
        solution,
        energy[
            "E_on_coeff_J_per_GeV2"
        ],
        alpha_m_cap,
    )

    if not response.get(
        "success",
        False,
    ):

        return {
            "success":
            False,

            "kappa_GJ_per_GeV2":
            kappa_gj_per_gev2,

            "reason":
            response.get(
                "reason",
                "RESPONSE_FAILURE",
            ),
        }

    m4solve = solve_required_m4(
        response
    )

    if not m4solve.get(
        "success",
        False,
    ):

        return {
            "success":
            False,

            "kappa_GJ_per_GeV2":
            kappa_gj_per_gev2,

            "reason":
            m4solve.get(
                "reason",
                "M4_FAILURE",
            ),
        }

    M4 = m4solve[
        "M4_GeV"
    ]

    E_core = (
        kappa
        *
        M4**2
    )

    E_phi = (
        energy[
            "E_phi_direct_coeff_J_per_GeV2"
        ]
        *
        M4**2
    )

    E_on = (
        energy[
            "E_on_coeff_J_per_GeV2"
        ]
        *
        M4**2
    )

    E_conservative = (
        E_core
        +
        E_phi
    )

    u_near = response[
        "u_near_payload"
    ]

    back = payload_backreaction(
        M4,
        u_near,
        alpha_m_cap,
    )

    u_center = branch[
        "u_center"
    ]

    alpha_x_center = (
        -MPL_GEV
        *
        u_center
        /
        M4
    )

    f_center = (
        M4
        /
        max(
            abs(
                u_center
            ),
            1.0e-300,
        )
    )

    derrick = derrick_diagnostics(
        reconstructed,
        energy[
            "e4_c4_weighted_mean"
        ],
    )

    scalar_energy_pass = (
        energy[
            "scalar_energy_identity_relerr"
        ]
        <=
        SCALAR_ENERGY_IDENTITY_REL_TOL
    )

    result = {
        "success":
        True,

        "kappa_GJ_per_GeV2":
        kappa_gj_per_gev2,

        "linear_eigenvalue_m2inv":
        branch[
            "linear_eigenvalue_m2inv"
        ],

        "scalar_hessian_eigenvalue_m2inv":
        branch[
            "scalar_hessian_eigenvalue_m2inv"
        ],

        "scalar_radial_stability":
        branch[
            "scalar_radial_stability"
        ],

        "u_center":
        u_center,

        "u_near_payload":
        u_near,

        "M4_GeV":
        M4,

        "M_m_GeV":
        back[
            "M_m_GeV"
        ],

        "alpha_x_center":
        alpha_x_center,

        "f_center_GeV":
        f_center,

        "E_core_J":
        E_core,

        "E_phi_J":
        E_phi,

        "E_on_J":
        E_on,

        "E_total_conservative_J":
        E_conservative,

        "a_cm_mps2":
        m4solve[
            "a_cm_mps2"
        ],

        "a_adverse_mps2":
        m4solve[
            "a_adverse_mps2"
        ],

        "payload_backreaction_ratio":
        back[
            "payload_backreaction_ratio"
        ],

        "e4_c4_weighted_mean":
        energy[
            "e4_c4_weighted_mean"
        ],

        "scalar_energy_identity_relerr":
        energy[
            "scalar_energy_identity_relerr"
        ],

        "scalar_energy_identity_pass":
        scalar_energy_pass,

        "target_energy_pass":
        False,

        "backreaction_pass":
        bool(
            back[
                "payload_backreaction_ratio"
            ]
            <=
            BACKREACTION_LIMIT
        ),

        **derrick,
    }

    return result


def main():

    print(
        "=== 031B1-B0 EXACT Z2 e4 "
        "SELF-CONSISTENCY GATE ==="
    )

    print(
        "CLAIM_CLASS="
        "NONLINEAR_LOCAL_Z2_MICROSCOPIC_SECTOR_"
        "SELFCONSISTENCY_PREFLIGHT"
    )

    print(
        "B7_REEQUILIBRATED=NO"
    )

    print(
        "LOCAL_Z2_COUPLING_EXPLICIT=YES"
    )

    print(
        "SCALAR_SENSITIVITY_ASSIGNED_BY_HAND=NO"
    )

    print(
        "FULL_LOCAL_CONSERVATION=NO_NOT_YET"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    for path in (
        B1A_SOURCE,
        CR3_SOURCE,
        R4S_SUMMARY,
        B1A_SUMMARY,
        B1A_CSV,
        N73_FIELD,
        N81_FIELD,
    ):

        require(
            path
        )

    b1a = load_module(
        "b1b0_b1a",
        B1A_SOURCE,
    )

    cr3 = load_module(
        "b1b0_cr3",
        CR3_SOURCE,
    )

    r4s = json.loads(
        R4S_SUMMARY.read_text()
    )

    b1a_summary = json.loads(
        B1A_SUMMARY.read_text()
    )

    if (
        b1a_summary.get(
            "best_sector"
        )
        !=
        "e4"
    ):

        raise RuntimeError(
            "031B1-A did not promote e4"
        )

    TARGET_E_J = float(
        r4s[
            "target_energy_J"
        ]
    )

    ALPHA_M_CAP = float(
        r4s[
            "scaling"
        ][
            "alpha_m_cap_required"
        ]
    )

    print(
        f"TARGET_E_J="
        f"{TARGET_E_J:.15e}"
    )

    print(
        f"ALPHA_M_ON_CAP="
        f"{ALPHA_M_CAP:.15e}"
    )

    print(
        f"MEDIATOR_RANGE_M="
        f"{MEDIATOR_RANGE_M:.15e}"
    )

    print(
        "\n=== A — RECONSTRUCT B7 e4 RADIAL PROFILES ==="
    )

    b1a_rows = read_b1a_rows()

    grids = {}

    for label, path, n in (
        (
            "N73",
            N73_FIELD,
            73,
        ),
        (
            "N81",
            N81_FIELD,
            81,
        ),
    ):

        field = b1a.load_field(
            path,
            n,
        )

        reconstructed = b1a.reconstruct_b7(
            cr3,
            field,
        )

        profile = make_radial_profile(
            reconstructed
        )

        prior = e4_b1a_row(
            b1a_rows,
            label,
        )

        kmin = float(
            prior[
                "scalar_leverage_min_m2inv"
            ]
        )

        kmean = float(
            prior[
                "scalar_leverage_mean_m2inv"
            ]
        )

        kmax = float(
            prior[
                "scalar_leverage_max_m2inv"
            ]
        )

        orientation_spread = (
            (
                kmax
                -
                kmin
            )
            /
            max(
                kmean,
                1.0e-300,
            )
        )

        radialization_pass = bool(
            orientation_spread
            <=
            RADIALIZATION_MAX_ORIENTATION_SPREAD
            and
            relerr(
                profile[
                    "e4_integral_check"
                ],
                profile[
                    "e4_fraction"
                ],
            )
            <=
            3.0e-3
            and
            abs(
                profile[
                    "total_integral_check"
                ]
                -
                1.0
            )
            <=
            3.0e-3
        )

        print(
            f"RADIAL_PROFILE "
            f"GRID={label} "
            f"E4_FRACTION="
            f"{profile['e4_fraction']:.9e} "
            f"E4_INT="
            f"{profile['e4_integral_check']:.9e} "
            f"TOTAL_INT="
            f"{profile['total_integral_check']:.9e} "
            f"ORIENTATION_SPREAD="
            f"{orientation_spread:.9e} "
            f"CENTROID_M="
            f"{profile['e4_centroid_norm_m']:.9e} "
            f"SECOND_MOMENT_ANIS="
            f"{profile['e4_second_moment_anisotropy']:.9e} "
            f"PASS={radialization_pass}"
        )

        if not radialization_pass:

            raise RuntimeError(
                f"{label} radialization precondition failed"
            )

        grids[
            label
        ] = {
            "reconstructed":
            reconstructed,

            "profile":
            profile,

            "orientation_spread":
            orientation_spread,
        }

    print(
        "\n=== B — EXACT NONLINEAR Z2 KAPPA SCAN ==="
    )

    scan_rows = []

    per_grid = {
        "N73":
        {},
        "N81":
        {},
    }

    for kappa_gj in KAPPA_GJ_PER_GEV2:

        for label in (
            "N73",
            "N81",
        ):

            result = evaluate_kappa(
                grids[
                    label
                ][
                    "profile"
                ],
                grids[
                    label
                ][
                    "reconstructed"
                ],
                float(
                    kappa_gj
                ),
                ALPHA_M_CAP,
            )

            if result.get(
                "success",
                False,
            ):

                result[
                    "target_energy_pass"
                ] = bool(
                    result[
                        "E_total_conservative_J"
                    ]
                    <=
                    TARGET_E_J
                    *
                    (
                        1.0
                        +
                        ENERGY_REL_MARGIN
                    )
                )

            result[
                "grid"
            ] = label

            per_grid[
                label
            ][
                float(
                    kappa_gj
                )
            ] = result

            scan_rows.append(
                {
                    key:
                    to_builtin(
                        value
                    )
                    for key, value
                    in result.items()
                }
            )

            if not result.get(
                "success",
                False,
            ):

                print(
                    f"Z2_CASE "
                    f"GRID={label} "
                    f"KAPPA_GJ_PER_GEV2="
                    f"{float(kappa_gj):.9e} "
                    f"SUCCESS=False "
                    f"REASON="
                    f"{result.get('reason', 'UNKNOWN')}"
                )

                continue

            print(
                f"Z2_CASE "
                f"GRID={label} "
                f"KAPPA_GJ_PER_GEV2="
                f"{float(kappa_gj):.9e} "
                f"U0="
                f"{result['u_center']:.9e} "
                f"M4_GEV="
                f"{result['M4_GeV']:.9e} "
                f"ALPHA_X_CENTER="
                f"{result['alpha_x_center']:.9e} "
                f"E_CORE_J="
                f"{result['E_core_J']:.9e} "
                f"E_PHI_J="
                f"{result['E_phi_J']:.9e} "
                f"E_TOTAL_J="
                f"{result['E_total_conservative_J']:.9e} "
                f"A_ADVERSE="
                f"{result['a_adverse_mps2']:.9e} "
                f"BACK="
                f"{result['payload_backreaction_ratio']:.9e} "
                f"C4_MEAN="
                f"{result['e4_c4_weighted_mean']:.9e} "
                f"DERRICK_REL="
                f"{result['derrick_relative_burden']:.9e} "
                f"SCALAR_STABLE="
                f"{result['scalar_radial_stability']} "
                f"E_PASS="
                f"{result['target_energy_pass']} "
                f"BACK_PASS="
                f"{result['backreaction_pass']}"
            )

    print(
        "\n=== C — N73 / N81 PAIR GATE ==="
    )

    pair_rows = []

    joint_candidates = []

    for kappa_gj in KAPPA_GJ_PER_GEV2:

        kappa = float(
            kappa_gj
        )

        a = per_grid[
            "N73"
        ][
            kappa
        ]

        b = per_grid[
            "N81"
        ][
            kappa
        ]

        if not (
            a.get(
                "success",
                False,
            )
            and
            b.get(
                "success",
                False,
            )
        ):

            continue

        m4_rel = relerr(
            a[
                "M4_GeV"
            ],
            b[
                "M4_GeV"
            ],
        )

        energy_rel = relerr(
            a[
                "E_total_conservative_J"
            ],
            b[
                "E_total_conservative_J"
            ],
        )

        c4_rel = relerr(
            a[
                "e4_c4_weighted_mean"
            ],
            b[
                "e4_c4_weighted_mean"
            ],
        )

        u0_rel = relerr(
            a[
                "u_center"
            ],
            b[
                "u_center"
            ],
        )

        pair_converged = bool(
            m4_rel
            <=
            PAIR_REL_TOL
            and
            energy_rel
            <=
            PAIR_REL_TOL
            and
            c4_rel
            <=
            PAIR_REL_TOL
            and
            u0_rel
            <=
            PAIR_REL_TOL
        )

        physics_pass = bool(
            pair_converged
            and
            a[
                "target_energy_pass"
            ]
            and
            b[
                "target_energy_pass"
            ]
            and
            a[
                "backreaction_pass"
            ]
            and
            b[
                "backreaction_pass"
            ]
            and
            a[
                "scalar_radial_stability"
            ]
            and
            b[
                "scalar_radial_stability"
            ]
            and
            a[
                "scalar_energy_identity_pass"
            ]
            and
            b[
                "scalar_energy_identity_pass"
            ]
        )

        worst_energy = max(
            a[
                "E_total_conservative_J"
            ],
            b[
                "E_total_conservative_J"
            ],
        )

        worst_derrick = max(
            a[
                "derrick_relative_burden"
            ],
            b[
                "derrick_relative_burden"
            ],
        )

        minimum_c4 = min(
            a[
                "e4_c4_weighted_mean"
            ],
            b[
                "e4_c4_weighted_mean"
            ],
        )

        pair = {
            "kappa_GJ_per_GeV2":
            kappa,

            "M4_relchange":
            m4_rel,

            "energy_relchange":
            energy_rel,

            "c4_relchange":
            c4_rel,

            "u0_relchange":
            u0_rel,

            "pair_converged":
            pair_converged,

            "physics_pass":
            physics_pass,

            "worst_energy_J":
            worst_energy,

            "worst_derrick_relative":
            worst_derrick,

            "minimum_e4_c4_mean":
            minimum_c4,
        }

        pair_rows.append(
            pair
        )

        if physics_pass:

            joint_candidates.append(
                (
                    pair,
                    a,
                    b,
                )
            )

        print(
            f"PAIR_GATE "
            f"KAPPA_GJ_PER_GEV2="
            f"{kappa:.9e} "
            f"M4_REL="
            f"{m4_rel:.9e} "
            f"ENERGY_REL="
            f"{energy_rel:.9e} "
            f"C4_REL="
            f"{c4_rel:.9e} "
            f"U0_REL="
            f"{u0_rel:.9e} "
            f"WORST_E_J="
            f"{worst_energy:.9e} "
            f"WORST_DERRICK_REL="
            f"{worst_derrick:.9e} "
            f"PAIR_PASS="
            f"{pair_converged} "
            f"PHYSICS_PASS="
            f"{physics_pass}"
        )

    print(
        "\n=== D — LEAST-DISRUPTIVE 83-GJ SURVIVOR ==="
    )

    best = None

    if joint_candidates:

        best = max(
            joint_candidates,
            key=lambda item:
            (
                item[
                    0
                ][
                    "minimum_e4_c4_mean"
                ],
                -item[
                    0
                ][
                    "worst_energy_J"
                ],
            ),
        )

        pair, n73, n81 = best

        print(
            f"BEST_KAPPA_GJ_PER_GEV2="
            f"{pair['kappa_GJ_per_GeV2']:.15e}"
        )

        print(
            f"BEST_WORST_ENERGY_J="
            f"{pair['worst_energy_J']:.15e}"
        )

        print(
            f"BEST_MIN_E4_C4_MEAN="
            f"{pair['minimum_e4_c4_mean']:.15e}"
        )

        print(
            f"BEST_WORST_DERRICK_REL="
            f"{pair['worst_derrick_relative']:.15e}"
        )

        print(
            f"BEST_N73_M4_GEV="
            f"{n73['M4_GeV']:.15e}"
        )

        print(
            f"BEST_N81_M4_GEV="
            f"{n81['M4_GeV']:.15e}"
        )

        print(
            f"BEST_N73_ALPHA_X_CENTER="
            f"{n73['alpha_x_center']:.15e}"
        )

        print(
            f"BEST_N81_ALPHA_X_CENTER="
            f"{n81['alpha_x_center']:.15e}"
        )

        print(
            f"BEST_N73_E_CORE_J="
            f"{n73['E_core_J']:.15e}"
        )

        print(
            f"BEST_N81_E_CORE_J="
            f"{n81['E_core_J']:.15e}"
        )

        print(
            f"BEST_N73_E_PHI_J="
            f"{n73['E_phi_J']:.15e}"
        )

        print(
            f"BEST_N81_E_PHI_J="
            f"{n81['E_phi_J']:.15e}"
        )

        print(
            f"BEST_N73_REEQUILIBRATION_BURDEN="
            f"{n73['reequilibration_burden']}"
        )

        print(
            f"BEST_N81_REEQUILIBRATION_BURDEN="
            f"{n81['reequilibration_burden']}"
        )

        print(
            f"BEST_N73_UNIFORM_SCALE_ESTIMATE="
            f"{n73['uniform_scale_estimate']:.15e}"
        )

        print(
            f"BEST_N81_UNIFORM_SCALE_ESTIMATE="
            f"{n81['uniform_scale_estimate']:.15e}"
        )

    print(
        "\n=== E — DECISION ==="
    )

    if best is None:

        classification = (
            "RED_MINIMAL_LOCAL_Z2_E4_DRESSING_"
            "DOES_NOT_PRESERVE_83GJ_AFTER_"
            "NONLINEAR_SELFCONSISTENCY"
        )

        next_step = (
            "031B2_QBALL_QSHELL_INDEPENDENT_"
            "SCALAR_CHARGE_CONTROL"
        )

    else:

        pair, n73, n81 = best

        severe = bool(
            n73[
                "reequilibration_burden"
            ]
            ==
            "SEVERE"
            or
            n81[
                "reequilibration_burden"
            ]
            ==
            "SEVERE"
        )

        if severe:

            classification = (
                "YELLOW_83GJ_SURVIVES_EXACT_Z2_"
                "BUT_B7_VIRIAL_REEQUILIBRATION_"
                "BURDEN_IS_SEVERE"
            )

        else:

            classification = (
                "GREEN_83GJ_SURVIVES_EXACT_LOCAL_Z2_"
                "E4_SELFCONSISTENCY_B7_FULL_3D_"
                "REEQUILIBRATION_AUTHORIZED"
            )

        next_step = (
            "031B1B1_FULL_3D_B7_PLUS_SCALAR_"
            "REEQUILIBRATION_CONSERVATION_GATE"
        )

    print(
        f"B1B0_JOINT_83GJ_SURVIVORS="
        f"{len(joint_candidates)}"
    )

    print(
        f"B1B0_EXACT_LOCAL_Z2_83GJ_SURVIVES="
        f"{best is not None}"
    )

    print(
        "B1B0_FULL_B7_REEQUILIBRATION="
        "NOT_YET"
    )

    print(
        "B1B0_FULL_LOCAL_CONSERVATION="
        "NOT_YET"
    )

    print(
        "B1B0_COUPLED_NONRADIAL_STABILITY="
        "NOT_YET"
    )

    print(
        "B1B0_EFT_NATURALNESS="
        "NOT_CLOSED"
    )

    print(
        f"031B1B0_CLASSIFICATION="
        f"{classification}"
    )

    print(
        f"NEXT="
        f"{next_step}"
    )

    OUT_CSV.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if scan_rows:

        fieldnames = []

        for row in scan_rows:

            for key in row:

                if key not in fieldnames:

                    fieldnames.append(
                        key
                    )

        with OUT_CSV.open(
            "w",
            newline="",
        ) as handle:

            writer = csv.DictWriter(
                handle,
                fieldnames=fieldnames,
                extrasaction="ignore",
            )

            writer.writeheader()

            writer.writerows(
                scan_rows
            )

    summary = {
        "claim_class":
        "NONLINEAR_LOCAL_Z2_MICROSCOPIC_SECTOR_"
        "SELFCONSISTENCY_PREFLIGHT",

        "target_energy_J":
        TARGET_E_J,

        "alpha_m_on_cap":
        ALPHA_M_CAP,

        "mediator_range_m":
        MEDIATOR_RANGE_M,

        "joint_83gj_survivors":
        len(
            joint_candidates
        ),

        "exact_local_z2_83gj_survives":
        best is not None,

        "best":
        (
            None
            if best is None
            else {
                "pair":
                best[
                    0
                ],

                "N73":
                {
                    key:
                    value
                    for key, value
                    in best[
                        1
                    ].items()
                    if key
                    !=
                    "solution"
                },

                "N81":
                {
                    key:
                    value
                    for key, value
                    in best[
                        2
                    ].items()
                    if key
                    !=
                    "solution"
                },
            }
        ),

        "pair_rows":
        pair_rows,

        "classification":
        classification,

        "next":
        next_step,

        "claim_limits": [
            "B7 itself is not re-equilibrated in this run.",
            "The e4 density is radialized after validating the tiny fixed-field orientation spread.",
            "The local Z2 scalar equation is solved nonlinearly rather than assigning alpha_X.",
            "Scalar gradient and mass energy are positive and independently reconstructed.",
            "The conservative ledger does not credit e4 suppression as free negative energy.",
            "The Derrick diagnostic estimates, but does not replace, full B7 re-equilibration.",
            "Full B7+scalar local conservation is not yet established.",
            "Coupled nonradial stability is not yet established.",
            "EFT/radiative naturalness and empirical closure remain open.",
            "026C N89 remains mandatory in parallel.",
            "No practical device is established.",
        ],
    }

    OUT_JSON.write_text(
        json.dumps(
            to_builtin(
                summary
            ),
            indent=2,
            sort_keys=True,
        )
        +
        "\n"
    )

    print(
        f"SUMMARY_JSON="
        f"{OUT_JSON.resolve()}"
    )

    print(
        f"SCAN_CSV="
        f"{OUT_CSV.resolve()}"
    )


if __name__ == "__main__":
    main()
