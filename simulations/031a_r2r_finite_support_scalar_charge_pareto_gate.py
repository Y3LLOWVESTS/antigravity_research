"""
031A-R2R — Finite-Support One-Sided Scalar-Charge Pareto Gate

True-antigravity scalar-metric preflight.

This is NOT a microscopic source or device.

The source is represented by non-overlapping uniform spherical charge/energy
blobs arranged into axisymmetric rings entirely behind the true-stand-off
plane.

Massless on-state advantages:

- each blob has an exact exterior 1/r scalar field;
- each positive source-core mass has an exact exterior Newtonian field;
- scalar self-energy of a uniform sphere is analytic;
- cross-energy of non-overlapping spherical blobs is analytic;
- finite spherical payload averaging is exact by the harmonic mean-value
  property because all source support lies outside the payload.

Normalization inherited from certified 031A:

    nabla^2 psi = -4*pi*rho_q

    a_phi = 2*G*alpha_m*grad(psi)

    E_phi = (G/4*pi) integral |grad psi|^2 dV

Scalar charge q is expressed as an equivalent mass charge.

For a microscopic source sensitivity alpha_X, impose the optimistic local bound

    |q| <= alpha_X * M_core

therefore

    E_core >= c^2 * |q| / alpha_X

The corresponding ordinary GR attraction of E_core/c^2 is included.

NOT included:

- microscopic source realization;
- stabilization energy;
- activation/gate energy;
- support/control energy;
- radiative corrections in the primary ledger;
- off-state fifth-force engineering.

Therefore the reported energy is an optimistic lower bound.

A radiative-naturalness diagnostic is printed separately and is NOT used as
a hard theorem because a protected UV completion could alter it.
"""

from __future__ import annotations

import csv
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.optimize import linprog, minimize


G = 6.67430e-11
C = 299_792_458.0
G0 = 9.80665

HBARC_EVM = 1.973269804e-7
MPL_REDUCED_GEV = 2.435e18

PAYLOAD_RADIUS = 0.10
CLEARANCE = 1.00

D = PAYLOAD_RADIUS + CLEARANCE

BLOB_RADIUS = 0.055

TARGET_1TJ = 1.0e12
TARGET_1E11 = 1.0e11

ALPHA_M_VALUES = (
    1.0,
    2.0,
    3.0,
    3.125,
    5.0,
    10.0,
)

ALPHA_X_GRID = np.logspace(
    14.0,
    18.0,
    17,
)

LEAK_CASES = (
    1.0,
    0.10,
    0.01,
    0.0,
)

CERTIFIED_R1_RANGE = {
    10.0: (
        1.001133253996320,
        1.004692531345657,
    ),
    3.0: (
        1.030963959542184,
        1.046613207930021,
    ),
    1.0: (
        1.475370862074284,
        1.358018253777487,
    ),
    0.5: (
        4.172194646883209,
        2.454893761210717,
    ),
    0.3: (
        2.581197207834287e1,
        6.409783798047898,
    ),
    0.2: (
        3.465146325507072e2,
        2.423117401291679e1,
    ),
    0.1: (
        1.864406074762075e6,
        1.845328572777107e3,
    ),
}


RESULTS = Path("results/data")

RESULTS.mkdir(
    parents=True,
    exist_ok=True,
)


@dataclass
class GeometrySpec:
    name: str
    radial: tuple[float, ...]
    depth: tuple[float, ...]


COARSE = GeometrySpec(
    "coarse",
    (
        0.00,
        0.30,
        0.60,
        0.90,
    ),
    (
        0.00,
        0.40,
        0.90,
    ),
)

MEDIUM = GeometrySpec(
    "medium",
    (
        0.00,
        0.20,
        0.40,
        0.60,
        0.80,
        1.00,
    ),
    (
        0.00,
        0.25,
        0.55,
        0.95,
    ),
)

FINE = GeometrySpec(
    "fine",
    (
        0.00,
        0.16,
        0.32,
        0.48,
        0.64,
        0.80,
        0.96,
    ),
    (
        0.00,
        0.20,
        0.40,
        0.70,
        1.00,
    ),
)


def ring_count(
    radius: float,
) -> int:

    if radius == 0.0:
        return 1

    target_spacing = (
        2.45
        *
        BLOB_RADIUS
    )

    return max(
        6,
        int(
            math.floor(
                2.0
                *
                math.pi
                *
                radius
                /
                target_spacing
            )
        ),
    )


def build_geometry(
    spec: GeometrySpec,
):

    coordinates = []

    basis_indices = []

    metadata = []

    basis = 0

    for depth in spec.depth:

        z = -(
            D
            +
            BLOB_RADIUS
            +
            depth
        )

        for rho in spec.radial:

            count = ring_count(
                rho,
            )

            metadata.append(
                {
                    "rho": rho,
                    "depth": depth,
                    "z": z,
                    "nphi": count,
                }
            )

            if count == 1:

                coordinates.append(
                    (
                        0.0,
                        0.0,
                        z,
                    )
                )

                basis_indices.append(
                    basis
                )

            else:

                for k in range(
                    count
                ):

                    phi = (
                        2.0
                        *
                        math.pi
                        *
                        k
                        /
                        count
                    )

                    coordinates.append(
                        (
                            rho
                            *
                            math.cos(phi),
                            rho
                            *
                            math.sin(phi),
                            z,
                        )
                    )

                    basis_indices.append(
                        basis
                    )

            basis += 1

    xyz = np.asarray(
        coordinates,
        dtype=float,
    )

    basis_indices = np.asarray(
        basis_indices,
        dtype=int,
    )

    number_basis = len(
        metadata
    )

    counts = np.bincount(
        basis_indices,
        minlength=number_basis,
    ).astype(float)

    differences = (
        xyz[:, None, :]
        -
        xyz[None, :, :]
    )

    distances = np.linalg.norm(
        differences,
        axis=2,
    )

    off_diagonal = ~np.eye(
        len(xyz),
        dtype=bool,
    )

    minimum_separation = float(
        np.min(
            distances[
                off_diagonal
            ]
        )
    )

    maximum_surface_z = float(
        np.max(
            xyz[:, 2]
            +
            BLOB_RADIUS
        )
    )

    if (
        minimum_separation
        <=
        2.0
        *
        BLOB_RADIUS
        *
        (
            1.0
            -
            1.0e-12
        )
    ):
        raise RuntimeError(
            "SOURCE_BLOBS_OVERLAP"
        )

    if (
        maximum_surface_z
        >
        -D
        +
        1.0e-12
    ):
        raise RuntimeError(
            "TRUE_STANDOFF_PLANE_VIOLATION"
        )

    physical_kernel = np.empty_like(
        distances
    )

    physical_kernel[
        off_diagonal
    ] = (
        1.0
        /
        distances[
            off_diagonal
        ]
    )

    np.fill_diagonal(
        physical_kernel,
        6.0
        /
        (
            5.0
            *
            BLOB_RADIUS
        ),
    )

    mapping = np.zeros(
        (
            len(xyz),
            number_basis,
        ),
        dtype=float,
    )

    for physical_index, basis_index in enumerate(
        basis_indices
    ):

        mapping[
            physical_index,
            basis_index,
        ] = (
            1.0
            /
            counts[
                basis_index
            ]
        )

    field_kernel = (
        mapping.T
        @
        physical_kernel
        @
        mapping
    )

    field_kernel = (
        field_kernel
        +
        field_kernel.T
    ) / 2.0

    minimum_eigenvalue = float(
        np.min(
            np.linalg.eigvalsh(
                field_kernel
            )
        )
    )

    if minimum_eigenvalue <= 0.0:
        raise RuntimeError(
            "FIELD_ENERGY_MATRIX_NOT_POSITIVE"
        )

    z = np.array(
        [
            item["z"]
            for item in metadata
        ],
        dtype=float,
    )

    rho = np.array(
        [
            item["rho"]
            for item in metadata
        ],
        dtype=float,
    )

    distance_to_payload = np.sqrt(
        z * z
        +
        rho * rho
    )

    acceleration_geometry = (
        z
        /
        distance_to_payload**3
    )

    return {
        "spec": spec,
        "xyz": xyz,
        "metadata": metadata,
        "field_kernel": field_kernel,
        "acceleration_geometry": acceleration_geometry,
        "z": z,
        "minimum_eigenvalue": minimum_eigenvalue,
        "minimum_separation": minimum_separation,
        "maximum_surface_z": maximum_surface_z,
    }


def halfspace_floor(
    scalar_acceleration: float,
    alpha_m: float,
) -> float:

    return (
        scalar_acceleration**2
        *
        D**3
        /
        (
            2.0
            *
            G
            *
            alpha_m**2
        )
    )


def solve_case(
    geometry,
    alpha_m: float,
    alpha_x: float,
    leakage_fraction: float,
    family: str = "unrestricted",
):

    field_kernel = geometry[
        "field_kernel"
    ]

    acceleration_geometry = geometry[
        "acceleration_geometry"
    ]

    metadata = geometry[
        "metadata"
    ]

    number_basis = len(
        acceleration_geometry
    )

    charge_reference = (
        G0
        *
        D**2
        /
        (
            2.0
            *
            G
            *
            alpha_m
        )
    )

    field_energy_scale = (
        G
        *
        charge_reference**2
        /
        TARGET_1TJ
    )

    core_energy_scale = (
        C**2
        *
        charge_reference
        /
        alpha_x
        /
        TARGET_1TJ
    )

    scalar_kernel = (
        D**2
        *
        acceleration_geometry
    )

    gr_kernel = (
        D**2
        *
        acceleration_geometry
        /
        (
            2.0
            *
            alpha_m
            *
            alpha_x
        )
    )

    total_acceleration_row = np.concatenate(
        (
            scalar_kernel
            +
            gr_kernel,
            -scalar_kernel
            +
            gr_kernel,
        )
    )

    bounds = []

    for block in (
        "positive",
        "negative",
    ):

        for item in metadata:

            upper = None

            if family == "front_rear":

                if (
                    block
                    ==
                    "positive"
                    and
                    item["depth"]
                    <
                    0.50
                ):
                    upper = 0.0

                if (
                    block
                    ==
                    "negative"
                    and
                    item["depth"]
                    >
                    0.55
                ):
                    upper = 0.0

            bounds.append(
                (
                    0.0,
                    upper,
                )
            )

    ones = np.ones(
        number_basis
    )

    net_charge_row = np.concatenate(
        (
            ones,
            -ones,
        )
    )

    absolute_charge_row = np.concatenate(
        (
            ones,
            ones,
        )
    )

    linear_ub = [
        -total_acceleration_row
    ]

    linear_ub_rhs = [
        -1.0
    ]

    linear_eq = None

    linear_eq_rhs = None

    if leakage_fraction == 0.0:

        linear_eq = [
            net_charge_row
        ]

        linear_eq_rhs = [
            0.0
        ]

    elif leakage_fraction < 1.0:

        linear_ub.extend(
            [
                (
                    net_charge_row
                    -
                    leakage_fraction
                    *
                    absolute_charge_row
                ),
                (
                    -net_charge_row
                    -
                    leakage_fraction
                    *
                    absolute_charge_row
                ),
            ]
        )

        linear_ub_rhs.extend(
            [
                0.0,
                0.0,
            ]
        )

    feasibility = linprog(
        absolute_charge_row,
        A_ub=np.asarray(
            linear_ub
        ),
        b_ub=np.asarray(
            linear_ub_rhs
        ),
        A_eq=(
            None
            if linear_eq is None
            else np.asarray(
                linear_eq
            )
        ),
        b_eq=(
            None
            if linear_eq_rhs is None
            else np.asarray(
                linear_eq_rhs
            )
        ),
        bounds=bounds,
        method="highs",
    )

    if not feasibility.success:
        return None

    def objective(
        vector,
    ):

        positive = vector[
            :number_basis
        ]

        negative = vector[
            number_basis:
        ]

        signed = (
            positive
            -
            negative
        )

        absolute = (
            positive
            +
            negative
        )

        return (
            field_energy_scale
            *
            float(
                signed
                @
                field_kernel
                @
                signed
            )
            +
            core_energy_scale
            *
            float(
                np.sum(
                    absolute
                )
            )
        )

    def objective_gradient(
        vector,
    ):

        positive = vector[
            :number_basis
        ]

        negative = vector[
            number_basis:
        ]

        signed = (
            positive
            -
            negative
        )

        signed_gradient = (
            2.0
            *
            field_energy_scale
            *
            (
                field_kernel
                @
                signed
            )
        )

        return np.concatenate(
            (
                signed_gradient
                +
                core_energy_scale,
                -signed_gradient
                +
                core_energy_scale,
            )
        )

    constraints = [
        {
            "type": "ineq",
            "fun": (
                lambda vector,
                row=total_acceleration_row:
                float(
                    row
                    @
                    vector
                    -
                    1.0
                )
            ),
            "jac": (
                lambda vector,
                row=total_acceleration_row:
                row
            ),
        }
    ]

    if leakage_fraction == 0.0:

        constraints.append(
            {
                "type": "eq",
                "fun": (
                    lambda vector,
                    row=net_charge_row:
                    float(
                        row
                        @
                        vector
                    )
                ),
                "jac": (
                    lambda vector,
                    row=net_charge_row:
                    row
                ),
            }
        )

    elif leakage_fraction < 1.0:

        constraints.extend(
            [
                {
                    "type": "ineq",
                    "fun": (
                        lambda vector,
                        qrow=net_charge_row,
                        arow=absolute_charge_row,
                        fraction=leakage_fraction:
                        float(
                            fraction
                            *
                            (
                                arow
                                @
                                vector
                            )
                            -
                            (
                                qrow
                                @
                                vector
                            )
                        )
                    ),
                    "jac": (
                        lambda vector,
                        qrow=net_charge_row,
                        arow=absolute_charge_row,
                        fraction=leakage_fraction:
                        (
                            fraction
                            *
                            arow
                            -
                            qrow
                        )
                    ),
                },
                {
                    "type": "ineq",
                    "fun": (
                        lambda vector,
                        qrow=net_charge_row,
                        arow=absolute_charge_row,
                        fraction=leakage_fraction:
                        float(
                            fraction
                            *
                            (
                                arow
                                @
                                vector
                            )
                            +
                            (
                                qrow
                                @
                                vector
                            )
                        )
                    ),
                    "jac": (
                        lambda vector,
                        qrow=net_charge_row,
                        arow=absolute_charge_row,
                        fraction=leakage_fraction:
                        (
                            fraction
                            *
                            arow
                            +
                            qrow
                        )
                    ),
                },
            ]
        )

    optimized = minimize(
        objective,
        feasibility.x,
        jac=objective_gradient,
        method="SLSQP",
        bounds=bounds,
        constraints=constraints,
        options={
            "ftol": 1.0e-10,
            "maxiter": 1200,
            "disp": False,
        },
    )

    vector = optimized.x

    positive = vector[
        :number_basis
    ]

    negative = vector[
        number_basis:
    ]

    signed_dimensionless = (
        positive
        -
        negative
    )

    absolute_dimensionless = (
        positive
        +
        negative
    )

    physical_charge = (
        charge_reference
        *
        signed_dimensionless
    )

    scalar_terms = (
        G0
        *
        scalar_kernel
        *
        signed_dimensionless
    )

    gr_terms = (
        G0
        *
        gr_kernel
        *
        absolute_dimensionless
    )

    scalar_acceleration = float(
        np.sum(
            scalar_terms
        )
    )

    gr_acceleration = float(
        np.sum(
            gr_terms
        )
    )

    total_acceleration = (
        scalar_acceleration
        +
        gr_acceleration
    )

    field_energy = (
        G
        *
        float(
            physical_charge
            @
            field_kernel
            @
            physical_charge
        )
    )

    absolute_charge = (
        charge_reference
        *
        float(
            np.sum(
                absolute_dimensionless
            )
        )
    )

    net_charge = (
        charge_reference
        *
        float(
            np.sum(
                signed_dimensionless
            )
        )
    )

    core_energy = (
        C**2
        *
        absolute_charge
        /
        alpha_x
    )

    total_energy = (
        field_energy
        +
        core_energy
    )

    gross_outward = float(
        np.sum(
            np.clip(
                scalar_terms,
                0.0,
                None,
            )
        )
    )

    gross_opposing = float(
        -np.sum(
            np.clip(
                scalar_terms,
                None,
                0.0,
            )
        )
    )

    if scalar_acceleration != 0.0:

        cancellation = (
            gross_outward
            +
            gross_opposing
        ) / abs(
            scalar_acceleration
        )

    else:

        cancellation = math.inf

    productive_mask = (
        scalar_terms
        >
        0.0
    )

    if (
        np.sum(
            absolute_dimensionless
        )
        >
        0.0
    ):

        productive_participation = float(
            np.sum(
                absolute_dimensionless[
                    productive_mask
                ]
            )
            /
            np.sum(
                absolute_dimensionless
            )
        )

    else:

        productive_participation = 0.0

    f50 = math.nan

    f90 = math.nan

    if (
        gross_outward
        >
        0.0
        and
        np.sum(
            absolute_dimensionless
        )
        >
        0.0
    ):

        indices = np.where(
            productive_mask
        )[0]

        indices = indices[
            np.argsort(
                scalar_terms[
                    indices
                ]
            )[::-1]
        ]

        cumulative_acceleration = 0.0

        cumulative_charge = 0.0

        total_absolute_dimensionless = float(
            np.sum(
                absolute_dimensionless
            )
        )

        for index in indices:

            cumulative_acceleration += (
                scalar_terms[
                    index
                ]
            )

            cumulative_charge += (
                absolute_dimensionless[
                    index
                ]
            )

            influence_fraction = (
                cumulative_acceleration
                /
                gross_outward
            )

            charge_fraction = (
                cumulative_charge
                /
                total_absolute_dimensionless
            )

            if (
                math.isnan(
                    f50
                )
                and
                influence_fraction
                >=
                0.50
            ):
                f50 = charge_fraction

            if (
                math.isnan(
                    f90
                )
                and
                influence_fraction
                >=
                0.90
            ):
                f90 = charge_fraction

                break

    dipole_z = (
        charge_reference
        *
        float(
            np.sum(
                signed_dimensionless
                *
                geometry["z"]
            )
        )
    )

    if absolute_charge > 0.0:

        monopole_fraction = (
            abs(
                net_charge
            )
            /
            absolute_charge
        )

        dipole_normalized = (
            abs(
                dipole_z
            )
            /
            (
                absolute_charge
                *
                D
            )
        )

    else:

        monopole_fraction = 0.0

        dipole_normalized = 0.0

    theorem_floor = halfspace_floor(
        scalar_acceleration,
        alpha_m,
    )

    if theorem_floor > 0.0:

        field_over_floor = (
            field_energy
            /
            theorem_floor
        )

    else:

        field_over_floor = math.inf

    return {
        "success": bool(
            optimized.success
        ),
        "message": str(
            optimized.message
        ),
        "alpha_m": alpha_m,
        "alpha_x": alpha_x,
        "leakage_fraction": leakage_fraction,
        "family": family,
        "E_field_J": field_energy,
        "E_core_J": core_energy,
        "E_total_J": total_energy,
        "a_scalar_mps2": scalar_acceleration,
        "a_gr_mps2": gr_acceleration,
        "a_total_mps2": total_acceleration,
        "Qabs_kg": absolute_charge,
        "Qnet_kg": net_charge,
        "monopole_fraction": monopole_fraction,
        "dipole_normalized": dipole_normalized,
        "cancellation": cancellation,
        "productive_participation": productive_participation,
        "F50_core_fraction": f50,
        "F90_core_fraction": f90,
        "halfspace_floor_J": theorem_floor,
        "field_over_halfspace_floor": field_over_floor,
        "iterations": int(
            getattr(
                optimized,
                "nit",
                -1,
            )
        ),
    }


def threshold_case(
    rows,
    alpha_m,
    leakage_fraction,
    family,
    target_energy,
):

    candidates = [
        row
        for row in rows
        if (
            row["alpha_m"]
            ==
            alpha_m
            and
            row["leakage_fraction"]
            ==
            leakage_fraction
            and
            row["family"]
            ==
            family
            and
            row["success"]
            and
            row["E_total_J"]
            <=
            target_energy
        )
    ]

    if not candidates:
        return None

    return min(
        candidates,
        key=(
            lambda row:
            row["alpha_x"]
        ),
    )


def print_threshold(
    row,
    alpha_m,
    label,
    target_name,
):

    if row is None:

        print(
            f"THRESHOLD "
            f"ALPHA_M={alpha_m:g} "
            f"CASE={label} "
            f"TARGET={target_name} "
            f"NONE"
        )

        return

    print(
        f"THRESHOLD "
        f"ALPHA_M={alpha_m:g} "
        f"CASE={label} "
        f"TARGET={target_name} "
        f"ALPHA_X={row['alpha_x']:.9e} "
        f"E_TOTAL_J={row['E_total_J']:.9e} "
        f"E_FIELD_J={row['E_field_J']:.9e} "
        f"E_CORE_J={row['E_core_J']:.9e} "
        f"MONOPOLE={row['monopole_fraction']:.6e} "
        f"DIPOLE={row['dipole_normalized']:.6e} "
        f"CANCELLATION={row['cancellation']:.6e} "
        f"PRODUCTIVE={row['productive_participation']:.6e} "
        f"F90={row['F90_core_fraction']:.6e} "
        f"FIELD_OVER_FLOOR={row['field_over_halfspace_floor']:.6e}"
    )


def main():

    print(
        "=== 031A-R2R FINITE-SUPPORT "
        "ONE-SIDED SCALAR-CHARGE PARETO GATE ==="
    )

    print(
        "CLAIM_CLASS="
        "FINITE_SUPPORT_ORACLE_AND_"
        "FINITE_SENSITIVITY_PREFLIGHT"
    )

    print(
        "TRUE_ANTIGRAVITY_TARGET="
        "YES_ONE_PHYSICAL_METRIC"
    )

    print(
        "MICROSCOPIC_SOURCE=NO"
    )

    print(
        "ACTIVATION_MECHANISM=NO"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    print(
        f"PAYLOAD_RADIUS_M="
        f"{PAYLOAD_RADIUS:.15e}"
    )

    print(
        f"CLEARANCE_M="
        f"{CLEARANCE:.15e}"
    )

    print(
        f"CENTER_TO_SOURCE_SUPPORT_D_M="
        f"{D:.15e}"
    )

    print(
        f"BLOB_RADIUS_M="
        f"{BLOB_RADIUS:.15e}"
    )

    geometries = {
        spec.name: build_geometry(
            spec
        )
        for spec in (
            COARSE,
            MEDIUM,
            FINE,
        )
    }

    medium = geometries[
        "medium"
    ]

    print(
        "\n=== A — GEOMETRY / "
        "ENERGY-MATRIX VALIDATION ==="
    )

    geometry_pass = True

    for name, geometry in geometries.items():

        valid = (
            geometry[
                "maximum_surface_z"
            ]
            <=
            -D
            +
            1.0e-12
            and
            geometry[
                "minimum_separation"
            ]
            >
            2.0
            *
            BLOB_RADIUS
            *
            (
                1.0
                -
                1.0e-12
            )
            and
            geometry[
                "minimum_eigenvalue"
            ]
            >
            0.0
        )

        geometry_pass = (
            geometry_pass
            and
            valid
        )

        print(
            f"GEOMETRY={name} "
            f"NBASIS="
            f"{len(geometry['metadata'])} "
            f"NPHYSICAL="
            f"{len(geometry['xyz'])} "
            f"MIN_BLOB_SEP="
            f"{geometry['minimum_separation']:.9e} "
            f"MAX_SOURCE_SURFACE_Z="
            f"{geometry['maximum_surface_z']:.9e} "
            f"K_MIN_EIG="
            f"{geometry['minimum_eigenvalue']:.9e} "
            f"PASS={valid}"
        )

    print(
        f"R2R_GEOMETRY_PASS="
        f"{geometry_pass}"
    )

    print(
        "\n=== B — MEDIUM-BASIS "
        "PARETO SCAN ==="
    )

    rows = []

    for alpha_m in ALPHA_M_VALUES:

        for leakage_fraction in LEAK_CASES:

            for family in (
                "unrestricted",
                "front_rear",
            ):

                if (
                    family
                    ==
                    "front_rear"
                    and
                    leakage_fraction
                    ==
                    1.0
                ):
                    continue

                for alpha_x in ALPHA_X_GRID:

                    result = solve_case(
                        medium,
                        alpha_m,
                        float(
                            alpha_x
                        ),
                        leakage_fraction,
                        family,
                    )

                    if result is not None:
                        rows.append(
                            result
                        )

    theorem_failures = [
        row
        for row in rows
        if (
            row["success"]
            and
            row[
                "field_over_halfspace_floor"
            ]
            <
            1.0
            -
            2.0e-6
        )
    ]

    halfspace_pass = (
        len(
            theorem_failures
        )
        ==
        0
    )

    print(
        f"R2R_HALFSPACE_BOUND_PASS="
        f"{halfspace_pass}"
    )

    if theorem_failures:

        worst = min(
            theorem_failures,
            key=(
                lambda row:
                row[
                    "field_over_halfspace_floor"
                ]
            ),
        )

        print(
            "R2R_HALFSPACE_BOUND_WORST="
            f"{worst['field_over_halfspace_floor']:.9e}"
        )

    labels = (
        (
            1.0,
            "ANY",
        ),
        (
            0.10,
            "MONO_LE_0P1",
        ),
        (
            0.01,
            "MONO_LE_0P01",
        ),
        (
            0.0,
            "NET_NEUTRAL",
        ),
    )

    for alpha_m in ALPHA_M_VALUES:

        for leakage_fraction, label in labels:

            row_1tj = threshold_case(
                rows,
                alpha_m,
                leakage_fraction,
                "unrestricted",
                TARGET_1TJ,
            )

            row_1e11 = threshold_case(
                rows,
                alpha_m,
                leakage_fraction,
                "unrestricted",
                TARGET_1E11,
            )

            print_threshold(
                row_1tj,
                alpha_m,
                label,
                "1TJ",
            )

            print_threshold(
                row_1e11,
                alpha_m,
                label,
                "1E11",
            )

    print(
        "\n=== C — BEST PARETO MEMBERS ==="
    )

    for leakage_fraction, label in labels:

        candidates = [
            row
            for row in rows
            if (
                row[
                    "leakage_fraction"
                ]
                ==
                leakage_fraction
                and
                row[
                    "family"
                ]
                ==
                "unrestricted"
                and
                row[
                    "success"
                ]
            )
        ]

        if not candidates:
            continue

        best = min(
            candidates,
            key=(
                lambda row:
                row[
                    "E_total_J"
                ]
            ),
        )

        print(
            f"BEST_{label} "
            f"ALPHA_M="
            f"{best['alpha_m']:g} "
            f"ALPHA_X="
            f"{best['alpha_x']:.9e} "
            f"E_TOTAL_J="
            f"{best['E_total_J']:.9e} "
            f"E_FIELD_J="
            f"{best['E_field_J']:.9e} "
            f"E_CORE_J="
            f"{best['E_core_J']:.9e} "
            f"MONOPOLE="
            f"{best['monopole_fraction']:.9e} "
            f"DIPOLE="
            f"{best['dipole_normalized']:.9e} "
            f"CANCELLATION="
            f"{best['cancellation']:.9e} "
            f"PRODUCTIVE="
            f"{best['productive_participation']:.9e} "
            f"F50="
            f"{best['F50_core_fraction']:.9e} "
            f"F90="
            f"{best['F90_core_fraction']:.9e} "
            f"FIELD_OVER_FLOOR="
            f"{best['field_over_halfspace_floor']:.9e}"
        )

    print(
        "\n=== D — FRONT / REAR "
        "MORPHOLOGY CONTROL ==="
    )

    for alpha_m in (
        3.125,
        5.0,
        10.0,
    ):

        for leakage_fraction in (
            0.10,
            0.0,
        ):

            unrestricted = threshold_case(
                rows,
                alpha_m,
                leakage_fraction,
                "unrestricted",
                TARGET_1TJ,
            )

            front_rear = threshold_case(
                rows,
                alpha_m,
                leakage_fraction,
                "front_rear",
                TARGET_1TJ,
            )

            unrestricted_energy = (
                math.inf
                if unrestricted is None
                else unrestricted[
                    "E_total_J"
                ]
            )

            front_rear_energy = (
                math.inf
                if front_rear is None
                else front_rear[
                    "E_total_J"
                ]
            )

            ratio = (
                front_rear_energy
                /
                unrestricted_energy
                if (
                    math.isfinite(
                        front_rear_energy
                    )
                    and
                    math.isfinite(
                        unrestricted_energy
                    )
                )
                else math.inf
            )

            print(
                f"FRONT_REAR_CONTROL "
                f"ALPHA_M={alpha_m:g} "
                f"LEAK={leakage_fraction:g} "
                f"UNRESTRICTED_E_J="
                f"{unrestricted_energy:.9e} "
                f"FRONT_REAR_E_J="
                f"{front_rear_energy:.9e} "
                f"RATIO="
                f"{ratio:.9e}"
            )

    print(
        "\n=== E — BASIS CONVERGENCE ==="
    )

    convergence_cases = (
        (
            5.0,
            1.0e17,
            0.10,
        ),
        (
            10.0,
            3.162277660168379e16,
            0.10,
        ),
        (
            10.0,
            1.0e17,
            0.0,
        ),
    )

    basis_convergence_pass = True

    convergence_rows = []

    for (
        alpha_m,
        alpha_x,
        leakage_fraction,
    ) in convergence_cases:

        energies = []

        for geometry_name in (
            "coarse",
            "medium",
            "fine",
        ):

            result = solve_case(
                geometries[
                    geometry_name
                ],
                alpha_m,
                alpha_x,
                leakage_fraction,
                "unrestricted",
            )

            if (
                result is None
                or
                not result[
                    "success"
                ]
            ):

                energies.append(
                    math.nan
                )

            else:

                energies.append(
                    result[
                        "E_total_J"
                    ]
                )

                convergence_rows.append(
                    {
                        "geometry":
                        geometry_name,
                        **result,
                    }
                )

        if all(
            math.isfinite(
                value
            )
            for value in energies
        ):

            relative_coarse_medium = (
                abs(
                    energies[1]
                    -
                    energies[0]
                )
                /
                energies[1]
            )

            relative_medium_fine = (
                abs(
                    energies[2]
                    -
                    energies[1]
                )
                /
                energies[2]
            )

            shrinking = (
                relative_medium_fine
                <
                relative_coarse_medium
            )

            passed = (
                shrinking
                and
                relative_medium_fine
                <
                0.15
            )

            basis_convergence_pass = (
                basis_convergence_pass
                and
                passed
            )

            print(
                f"BASIS_CONVERGENCE "
                f"ALPHA_M={alpha_m:g} "
                f"ALPHA_X={alpha_x:.9e} "
                f"LEAK={leakage_fraction:g} "
                f"E_COARSE="
                f"{energies[0]:.9e} "
                f"E_MEDIUM="
                f"{energies[1]:.9e} "
                f"E_FINE="
                f"{energies[2]:.9e} "
                f"REL_CM="
                f"{relative_coarse_medium:.9e} "
                f"REL_MF="
                f"{relative_medium_fine:.9e} "
                f"SHRINKING={shrinking} "
                f"PASS={passed}"
            )

        else:

            basis_convergence_pass = False

            print(
                f"BASIS_CONVERGENCE "
                f"ALPHA_M={alpha_m:g} "
                f"ALPHA_X={alpha_x:.9e} "
                f"LEAK={leakage_fraction:g} "
                f"PASS=False "
                f"REASON=SOLVE_FAILURE"
            )

    print(
        f"BASIS_CONVERGENCE_PASS="
        f"{basis_convergence_pass}"
    )

    print(
        "\n=== F — RANGE CONTROL "
        "FROM CERTIFIED 031A-R1 ==="
    )

    for (
        lambda_over_d,
        (
            energy_ratio,
            charge_ratio,
        ),
    ) in CERTIFIED_R1_RANGE.items():

        print(
            f"RANGE_CONTROL "
            f"LAMBDA_OVER_D="
            f"{lambda_over_d:g} "
            f"E_OVER_MASSLESS="
            f"{energy_ratio:.15e} "
            f"QABS_OVER_MASSLESS="
            f"{charge_ratio:.15e}"
        )

    print(
        "\n=== G — PRACTICALITY MARKERS ==="
    )

    one_tj_candidate = threshold_case(
        rows,
        5.0,
        0.10,
        "unrestricted",
        TARGET_1TJ,
    )

    strong_candidate = threshold_case(
        rows,
        10.0,
        0.10,
        "unrestricted",
        TARGET_1E11,
    )

    neutral_candidate = threshold_case(
        rows,
        5.0,
        0.0,
        "unrestricted",
        TARGET_1TJ,
    )

    print(
        "ONE_TJ_OPTIMISTIC_CANDIDATE="
        f"{one_tj_candidate is not None}"
    )

    print(
        "STRONG_1E11_MONO_LE_0P1_CANDIDATE="
        f"{strong_candidate is not None}"
    )

    print(
        "NET_NEUTRAL_1TJ_ALPHA_M5_CANDIDATE="
        f"{neutral_candidate is not None}"
    )

    if strong_candidate is not None:

        f_x_gev = (
            MPL_REDUCED_GEV
            /
            strong_candidate[
                "alpha_x"
            ]
        )

        print(
            "STRONG_CANDIDATE_ALPHA_M="
            f"{strong_candidate['alpha_m']:.15e}"
        )

        print(
            "STRONG_CANDIDATE_ALPHA_X="
            f"{strong_candidate['alpha_x']:.15e}"
        )

        print(
            "STRONG_CANDIDATE_FX_GEV="
            f"{f_x_gev:.15e}"
        )

        print(
            "STRONG_CANDIDATE_E_TOTAL_J="
            f"{strong_candidate['E_total_J']:.15e}"
        )

        print(
            "STRONG_CANDIDATE_E_FIELD_J="
            f"{strong_candidate['E_field_J']:.15e}"
        )

        print(
            "STRONG_CANDIDATE_E_CORE_J="
            f"{strong_candidate['E_core_J']:.15e}"
        )

        print(
            "STRONG_CANDIDATE_MONOPOLE_FRAC="
            f"{strong_candidate['monopole_fraction']:.15e}"
        )

        print(
            "STRONG_CANDIDATE_DIPOLE_NORM="
            f"{strong_candidate['dipole_normalized']:.15e}"
        )

        print(
            "STRONG_CANDIDATE_CANCELLATION="
            f"{strong_candidate['cancellation']:.15e}"
        )

        print(
            "STRONG_CANDIDATE_PRODUCTIVE="
            f"{strong_candidate['productive_participation']:.15e}"
        )

        print(
            "\n=== H — UNPROTECTED "
            "COLEMAN-WEINBERG NATURALNESS DIAGNOSTIC ==="
        )

        preferred_range = (
            3.0
            *
            D
        )

        scalar_mass_ev = (
            HBARC_EVM
            /
            preferred_range
        )

        f_x_ev = (
            f_x_gev
            *
            1.0e9
        )

        base_mass = math.sqrt(
            scalar_mass_ev
            *
            f_x_ev
        )

        coefficient_high = (
            1.0
            /
            (
                4.0
                *
                math.pi**2
            )
        )

        coefficient_low = (
            1.0
            /
            (
                16.0
                *
                math.pi**2
            )
        )

        mx_low_ev = (
            base_mass
            *
            coefficient_high**(
                -0.25
            )
        )

        mx_high_ev = (
            base_mass
            *
            coefficient_low**(
                -0.25
            )
        )

        print(
            "CW_DIAGNOSTIC_ONLY="
            "YES_NOT_A_NO_GO_THEOREM"
        )

        print(
            "CW_ASSUMPTION="
            "UNPROTECTED_MASS_DEPENDENCE_"
            "M_X_PHI_PROPORTIONAL_EXP_PHI_OVER_FX"
        )

        print(
            "CW_PREFERRED_ON_RANGE_M="
            f"{preferred_range:.15e}"
        )

        print(
            "CW_TARGET_SCALAR_MASS_EV="
            f"{scalar_mass_ev:.15e}"
        )

        print(
            "CW_FX_EV="
            f"{f_x_ev:.15e}"
        )

        print(
            "CW_NATURAL_MX_MAX_LOW_EV="
            f"{mx_low_ev:.15e}"
        )

        print(
            "CW_NATURAL_MX_MAX_HIGH_EV="
            f"{mx_high_ev:.15e}"
        )

        print(
            "CW_INTERPRETATION="
            "NAIVE_HEAVY_UNPROTECTED_SOURCE_SECTOR_"
            "LIKELY_REQUIRES_PROTECTION_OR_TUNING"
        )

    if (
        not geometry_pass
        or
        not halfspace_pass
    ):

        classification = (
            "RED_NUMERICAL_OR_THEOREM_"
            "INTEGRITY_FAILURE"
        )

        next_step = (
            "DIAGNOSE_R2R_GEOMETRY_OR_"
            "FIELD_ENERGY_RECONSTRUCTION"
        )

    elif not basis_convergence_pass:

        classification = (
            "YELLOW_BASIS_NOT_CONVERGED"
        )

        next_step = (
            "031A_R2R2_BASIS_AND_"
            "COMPACT_SUPPORT_REFINEMENT"
        )

    elif one_tj_candidate is None:

        classification = (
            "RED_FINITE_SUPPORT_MORPHOLOGY_"
            "RESTORES_GT_1TJ_AT_ALPHA_M5"
        )

        next_step = (
            "031A_GLOBAL_RERANK_OR_"
            "030B_THEOREM_BACKSTOP"
        )

    elif strong_candidate is not None:

        classification = (
            "GREEN_FINITE_SUPPORT_PARETO_"
            "SURVIVES_OPTIMISTIC_1E11_GATE"
        )

        next_step = (
            "031A_R3_PROTECTED_CHARGE_"
            "ACTIVATION_EFT_NATURALNESS_GATE"
        )

    else:

        classification = (
            "GREEN_1TJ_ONLY_FINITE_SUPPORT_"
            "PARETO_SURVIVES"
        )

        next_step = (
            "031A_R3_PROTECTED_CHARGE_"
            "ACTIVATION_EFT_NATURALNESS_GATE"
        )

    print(
        f"031A_R2R_CLASSIFICATION="
        f"{classification}"
    )

    print(
        f"NEXT="
        f"{next_step}"
    )

    csv_path = (
        RESULTS
        /
        "031a_r2r_finite_support_scalar_charge_pareto.csv"
    )

    if rows:

        with csv_path.open(
            "w",
            newline="",
        ) as handle:

            writer = csv.DictWriter(
                handle,
                fieldnames=list(
                    rows[0].keys()
                ),
            )

            writer.writeheader()

            writer.writerows(
                rows
            )

    summary = {
        "claim_class":
        "FINITE_SUPPORT_ORACLE_AND_FINITE_SENSITIVITY_PREFLIGHT",

        "true_antigravity_target":
        True,

        "microscopic_source":
        False,

        "practical_device":
        False,

        "geometry_pass":
        geometry_pass,

        "halfspace_bound_pass":
        halfspace_pass,

        "basis_convergence_pass":
        basis_convergence_pass,

        "one_tj_candidate_alpha_m5_mono_le_0p1":
        one_tj_candidate
        is not None,

        "strong_1e11_candidate_alpha_m10_mono_le_0p1":
        strong_candidate
        is not None,

        "net_neutral_1tj_candidate_alpha_m5":
        neutral_candidate
        is not None,

        "classification":
        classification,

        "next":
        next_step,

        "payload_radius_m":
        PAYLOAD_RADIUS,

        "clearance_m":
        CLEARANCE,

        "center_to_source_support_m":
        D,

        "blob_radius_m":
        BLOB_RADIUS,

        "alpha_m_values":
        list(
            ALPHA_M_VALUES
        ),

        "alpha_x_grid":
        [
            float(
                value
            )
            for value in ALPHA_X_GRID
        ],

        "leakage_cases":
        list(
            LEAK_CASES
        ),

        "omitted_costs":
        [
            "microscopic realization",
            "stabilization",
            "activation gate field",
            "support control",
            "full radiative corrections",
            "off-state empirical leakage",
        ],
    }

    json_path = (
        RESULTS
        /
        "031a_r2r_finite_support_scalar_charge_summary.json"
    )

    json_path.write_text(
        json.dumps(
            summary,
            indent=2,
        )
        +
        "\n"
    )

    print(
        f"SUMMARY_JSON="
        f"{json_path.resolve()}"
    )

    print(
        f"PARETO_CSV="
        f"{csv_path.resolve()}"
    )


if __name__ == "__main__":
    main()
