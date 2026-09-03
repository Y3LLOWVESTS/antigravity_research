"""
031B1-A
=======

B7 fixed-field Z2 scalar-charge tomography and 83-GJ morphology gate.

SCIENTIFIC QUESTION
-------------------
031A-R4S established that a nonlinear Z2 scalarized prescribed source can
produce finite-payload true stand-off at 1 g with

    E_total <= 8.27507820143e10 J

at approximately

    alpha_m(on) = 27.0079
    |alpha_X|   = 1.93027e17
    lambda_phi  = 3.3 m.

The next buildplan gate is microscopic source reuse.

The strongest existing microscopic field is the strict stationary
false-core B=7, eta=0.4, m=8 Skyrmion at N73 and N81.

Before re-equilibrating that field, this run asks whether ONE existing
positive B7 energy sector

    e2
    e4
    V

can carry the required opposite-sign scalar sensitivity.

For a one-sector local dependence,

    J_phi(x)
        proportional to
        -alpha_X * rho_sector(x),

so the scalar-charge morphology is fixed by a genuine B7 invariant rather
than by an arbitrary spatial function.

PHYSICAL EMBEDDING
------------------
This is a fixed-field physical-morphology scout.

The complete interior numerical B7 support, including its voxel corners, is
uniformly scaled to fit inside a sphere of radius

    R_source = 0.95 m.

A spherical finite payload has

    R_payload = 0.10 m

and its nearest surface is separated from the source-support sphere by

    clearance = 1.00 m.

Therefore every source voxel lies strictly outside the payload and the entire
source is on the source side of a true stand-off clearance.

The B7 dimensionless energy distribution is normalized to a variable total
physical B7 energy E_B7. This does NOT yet derive the B7 dimensional
microscopic scale. It is deliberately a fixed-field charge-to-energy
tomography gate.

SCALAR NORMALIZATION
--------------------
Use the established 031 convention

    (nabla^2 - mu^2) psi = -4 pi rho_q

    a_scalar = +2 G alpha_m grad psi.

For negative source scalar charge and positive alpha_m, the force on neutral
ordinary matter is outward.

If sector s carries scalar sensitivity alpha_X,

    dq = -alpha_X dE_s / c^2.

The scalar acceleration is linear in alpha_X E_B7.

The scalar self-field energy is

    E_phi
        = G integral rho_q psi d^3x
        > 0.

For a fixed charge morphology:

    a_scalar = A_s alpha_X E_B7

    E_phi = C_s alpha_X^2 E_B7^2.

Ordinary GR attraction from the complete B7 energy is

    a_GR = B E_B7.

Thus the core energy required for 1 g is

    E_B7
        = g / (A_s alpha_X - B),

provided A_s alpha_X > B.

The total scout ledger is

    E_total
        = E_B7 + E_phi.

At alpha_X -> infinity,

    E_total
        -> C_s g^2 / A_s^2.

That asymptotic value is a morphology-dependent scalar-field-energy floor.

If that floor exceeds 83 GJ, no amount of scalar sensitivity can rescue that
one-sector B7 morphology in this fixed-field approximation.

FINITE PAYLOAD
--------------
The payload sphere is source-free.

Each Cartesian derivative of a Yukawa solution obeys the homogeneous
Helmholtz equation inside the payload.

Therefore its volume average is exactly the center field times

    F_P(mu R_P) = 3 i_1(mu R_P)/(mu R_P).

The Newtonian GR field is harmonic, so its finite-payload average is exactly
its center value.

SELF-ENERGY
-----------
The Yukawa potential is reconstructed by an isolated 3-D FFT convolution.

The within-voxel self term is replaced by the exact uniform-sphere averaged
Yukawa self kernel for an equal-volume sphere.

The convolution implementation is independently checked against an explicit
pair sum on a deterministic small synthetic source before B7 is analyzed.

CLAIM LIMITS
------------
This run does NOT:

- alter or re-equilibrate B7;
- prove a coupled B7-scalar stationary solution;
- derive a microscopic value of the physical B7 length/energy scale;
- establish source/support conservation after scalar dressing;
- establish nonradial stability of the dressed field;
- establish EFT or radiative naturalness;
- establish empirical fifth-force closure;
- supersede mandatory 026C N89 force-convergence work;
- establish a practical device.

A GREEN result authorizes the next coupled-field B7 dressing gate only.

A RED result closes the three simple one-sector B7 dressings and moves to the
independent Q-ball/Q-shell source rather than adding arbitrary B7 operators.

CLAIM_CLASS
-----------
FIXED_MICROSCOPIC_FIELD_SCALAR_CHARGE_TOMOGRAPHY_AND_ENERGY_FLOOR_GATE
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

from scipy.optimize import brentq
from scipy.signal import fftconvolve
from scipy.special import spherical_in


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results/data"

CR3_SOURCE = (
    SIM
    /
    "023cr3_geometric_degree_guarded_unrestricted_relaxation.py"
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

R4S_SUMMARY = (
    DATA
    /
    "031a_r4s_z2_scaling_83gj_recovery_summary.json"
)

OUT_JSON = (
    DATA
    /
    "031b1a_b7_fixed_field_z2_charge_tomography_summary.json"
)

OUT_CSV = (
    DATA
    /
    "031b1a_b7_fixed_field_z2_charge_tomography.csv"
)


G = 6.67430e-11
C = 299_792_458.0
G0 = 9.80665

MPL_GEV = 2.435e18

B = 7
ETA = 0.4
MASS = 8.0

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
MU = 1.0 / MEDIATOR_RANGE_M

N_DIRECTIONS = 320

PAIR_FRACTION_REL_TOL = 3.0e-2
PAIR_KERNEL_CURVE_REL_TOL = 5.0e-2
PAIR_SELF_COEFF_REL_TOL = 1.0e-1

TARGET_REL_TOL = 1.0e-3

SELF_FRACTION_WARN = 0.20

SECTORS = (
    "e2",
    "e4",
    "V",
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


def payload_factor(
    mu: float,
    radius: float,
) -> float:

    x = (
        mu
        *
        radius
    )

    if abs(
        x
    ) < 1.0e-10:

        return 1.0

    return float(
        3.0
        *
        spherical_in(
            1,
            x,
        )
        /
        x
    )


def sphere_self_factor(
    x: float,
) -> float:

    if abs(
        x
    ) < 0.08:

        return (
            6.0
            /
            5.0
            -
            x
            +
            18.0
            *
            x**2
            /
            35.0
            -
            x**3
            /
            5.0
            +
            4.0
            *
            x**4
            /
            63.0
        )

    return (
        3.0
        /
        x**2
        -
        9.0
        *
        (
            1.0
            +
            x
        )
        *
        math.exp(
            -x
        )
        *
        (
            x
            *
            math.cosh(
                x
            )
            -
            math.sinh(
                x
            )
        )
        /
        x**5
    )


def fibonacci_sphere(
    n: int,
) -> np.ndarray:

    k = np.arange(
        n,
        dtype=float,
    )

    golden = (
        math.pi
        *
        (
            3.0
            -
            math.sqrt(
                5.0
            )
        )
    )

    z = (
        1.0
        -
        2.0
        *
        (
            k
            +
            0.5
        )
        /
        n
    )

    rxy = np.sqrt(
        np.maximum(
            0.0,
            1.0
            -
            z**2,
        )
    )

    az = (
        golden
        *
        k
    )

    result = np.column_stack(
        (
            rxy
            *
            np.cos(
                az
            ),
            rxy
            *
            np.sin(
                az
            ),
            z,
        )
    )

    return (
        result
        /
        np.linalg.norm(
            result,
            axis=1,
        )[
            :,
            None
        ]
    )


def load_field(
    path: Path,
    expected_n: int,
):

    with np.load(
        path,
        allow_pickle=False,
    ) as d:

        phi = np.asarray(
            d[
                "phi"
            ],
            dtype=float,
        )

        axis = np.asarray(
            d[
                "axis"
            ],
            dtype=float,
        )

        dx = float(
            d[
                "dx"
            ]
        )

        metadata = {}

        for key in (
            "B",
            "eta",
            "mass",
            "source",
        ):

            if key in d.files:

                raw = d[
                    key
                ]

                try:

                    metadata[
                        key
                    ] = raw.item()

                except Exception:

                    metadata[
                        key
                    ] = str(
                        raw
                    )

    if phi.shape != (
        expected_n,
        expected_n,
        expected_n,
        4,
    ):

        raise RuntimeError(
            f"{path.name}: unexpected field shape {phi.shape}"
        )

    normerr = float(
        np.max(
            np.abs(
                np.linalg.norm(
                    phi,
                    axis=-1,
                )
                -
                1.0
            )
        )
    )

    if normerr > 5.0e-10:

        raise RuntimeError(
            f"{path.name}: S3 norm failure {normerr}"
        )

    if (
        "B"
        in metadata
        and
        int(
            metadata[
                "B"
            ]
        )
        !=
        B
    ):

        raise RuntimeError(
            f"{path.name}: B metadata mismatch"
        )

    if (
        "eta"
        in metadata
        and
        abs(
            float(
                metadata[
                    "eta"
                ]
            )
            -
            ETA
        )
        >
        1.0e-12
    ):

        raise RuntimeError(
            f"{path.name}: eta metadata mismatch"
        )

    if (
        "mass"
        in metadata
        and
        abs(
            float(
                metadata[
                    "mass"
                ]
            )
            -
            MASS
        )
        >
        1.0e-12
    ):

        raise RuntimeError(
            f"{path.name}: mass metadata mismatch"
        )

    return {
        "phi":
        phi,

        "axis":
        axis,

        "dx":
        dx,

        "normerr":
        normerr,

        "metadata":
        metadata,
    }


def reconstruct_b7(
    cr3,
    field,
):

    phi = field[
        "phi"
    ]

    axis = field[
        "axis"
    ]

    dx = field[
        "dx"
    ]

    cr3.B = B
    cr3.ETA = ETA
    cr3.MASS = MASS

    qx, qy, qz = (
        cr3.central4_derivatives(
            phi,
            dx,
        )
    )

    (
        _gxx,
        _gyy,
        _gzz,
        _gxy,
        _gxz,
        _gyz,
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
        center_field[
            ...,
            0
        ]
    )

    rho = (
        e2
        +
        e4
        +
        V
    )

    if (
        float(
            np.min(
                e2
            )
        )
        <
        -1.0e-10
        or
        float(
            np.min(
                e4
            )
        )
        <
        -1.0e-10
        or
        float(
            np.min(
                V
            )
        )
        <
        -1.0e-10
    ):

        raise RuntimeError(
            "Negative B7 energy sector encountered"
        )

    e2 = np.maximum(
        e2,
        0.0,
    )

    e4 = np.maximum(
        e4,
        0.0,
    )

    V = np.maximum(
        V,
        0.0,
    )

    rho = (
        e2
        +
        e4
        +
        V
    )

    volume_dimless = (
        dx**3
    )

    energies = {
        "e2":
        float(
            np.sum(
                e2
            )
            *
            volume_dimless
        ),

        "e4":
        float(
            np.sum(
                e4
            )
            *
            volume_dimless
        ),

        "V":
        float(
            np.sum(
                V
            )
            *
            volume_dimless
        ),
    }

    total_energy = sum(
        energies.values()
    )

    coords = axis[
        2:-2
    ]

    if len(
        coords
    ) != e2.shape[
        0
    ]:

        raise RuntimeError(
            "Coordinate / density shape mismatch"
        )

    X, Y, Z = np.meshgrid(
        coords,
        coords,
        coords,
        indexing="ij",
    )

    max_voxel_radius_dimless = (
        math.sqrt(
            3.0
        )
        *
        (
            float(
                np.max(
                    np.abs(
                        coords
                    )
                )
            )
            +
            0.5
            *
            dx
        )
    )

    physical_scale = (
        SOURCE_RADIUS_M
        /
        max_voxel_radius_dimless
    )

    dx_phys = (
        dx
        *
        physical_scale
    )

    xyz = np.column_stack(
        (
            X.ravel(),
            Y.ravel(),
            Z.ravel(),
        )
    )

    xyz *= physical_scale

    dV_phys = (
        dx_phys**3
    )

    sector_density = {
        "e2":
        e2,

        "e4":
        e4,

        "V":
        V,
    }

    sector_fraction_cells = {}

    for name in SECTORS:

        sector_fraction_cells[
            name
        ] = (
            sector_density[
                name
            ].ravel()
            *
            volume_dimless
            /
            total_energy
        )

    total_fraction_cells = (
        rho.ravel()
        *
        volume_dimless
        /
        total_energy
    )

    if relerr(
        float(
            np.sum(
                total_fraction_cells
            )
        ),
        1.0,
    ) > 1.0e-12:

        raise RuntimeError(
            "B7 normalized energy fractions do not sum to unity"
        )

    return {
        "shape":
        e2.shape,

        "coords_dimless":
        coords,

        "xyz_m":
        xyz,

        "dx_phys_m":
        dx_phys,

        "dV_phys_m3":
        dV_phys,

        "physical_scale_m_per_dimless":
        physical_scale,

        "energies":
        energies,

        "total_energy_dimless":
        total_energy,

        "sector_density":
        sector_density,

        "sector_fraction_cells":
        sector_fraction_cells,

        "total_fraction_cells":
        total_fraction_cells,
    }


def direction_kernel(
    xyz: np.ndarray,
    direction: np.ndarray,
):

    projection = (
        xyz
        @
        direction
    )

    radial_difference = (
        PAYLOAD_CENTER_M
        -
        projection
    )

    payload_position = (
        PAYLOAD_CENTER_M
        *
        direction
    )

    delta = (
        payload_position[
            None,
            :
        ]
        -
        xyz
    )

    distance2 = np.sum(
        delta
        *
        delta,
        axis=1,
    )

    distance = np.sqrt(
        distance2
    )

    if float(
        np.min(
            distance
        )
    ) <= PAYLOAD_RADIUS_M:

        raise RuntimeError(
            "Source intersects finite payload"
        )

    newton_kernel = (
        radial_difference
        /
        (
            distance2
            *
            distance
        )
    )

    yukawa_kernel = (
        np.exp(
            -MU
            *
            distance
        )
        *
        (
            1.0
            +
            MU
            *
            distance
        )
        *
        newton_kernel
    )

    return (
        yukawa_kernel,
        newton_kernel,
    )


def orientation_tomography(
    reconstructed,
    directions,
):

    xyz = reconstructed[
        "xyz_m"
    ]

    total_fraction = reconstructed[
        "total_fraction_cells"
    ]

    sector_fraction = reconstructed[
        "sector_fraction_cells"
    ]

    scalar_leverage = {
        name:
        np.empty(
            len(
                directions
            ),
            dtype=float,
        )
        for name in SECTORS
    }

    gr_leverage = np.empty(
        len(
            directions
        ),
        dtype=float,
    )

    for index, direction in enumerate(
        directions
    ):

        ky, kn = direction_kernel(
            xyz,
            direction,
        )

        gr_leverage[
            index
        ] = float(
            total_fraction
            @
            kn
        )

        for name in SECTORS:

            scalar_leverage[
                name
            ][
                index
            ] = float(
                sector_fraction[
                    name
                ]
                @
                ky
            )

    return {
        "scalar_leverage":
        scalar_leverage,

        "gr_leverage":
        gr_leverage,
    }


def yukawa_kernel_grid(
    n: int,
    dx: float,
    dV: float,
    include_self: bool,
):

    displacement = (
        np.arange(
            -(
                n
                -
                1
            ),
            n,
            dtype=float,
        )
        *
        dx
    )

    r2 = (
        displacement[
            :,
            None,
            None
        ]**2
        +
        displacement[
            None,
            :,
            None
        ]**2
        +
        displacement[
            None,
            None,
            :
        ]**2
    )

    r = np.sqrt(
        r2
    )

    kernel = np.zeros_like(
        r
    )

    nonzero = (
        r
        >
        0.0
    )

    kernel[
        nonzero
    ] = (
        np.exp(
            -MU
            *
            r[
                nonzero
            ]
        )
        /
        r[
            nonzero
        ]
    )

    center = (
        n
        -
        1
    )

    if include_self:

        req = (
            3.0
            *
            dV
            /
            (
                4.0
                *
                math.pi
            )
        )**(
            1.0
            /
            3.0
        )

        kernel[
            center,
            center,
            center
        ] = (
            sphere_self_factor(
                MU
                *
                req
            )
            /
            req
        )

    else:

        kernel[
            center,
            center,
            center
        ] = 0.0

    return kernel


def validate_fft_convolution():

    n = 7
    dx = 0.113
    dV = dx**3

    rho = np.zeros(
        (
            n,
            n,
            n,
        ),
        dtype=float,
    )

    samples = (
        (
            1,
            2,
            3,
            0.8,
        ),
        (
            5,
            4,
            1,
            1.2,
        ),
        (
            3,
            3,
            3,
            0.5,
        ),
        (
            2,
            5,
            4,
            0.3,
        ),
    )

    for i, j, k, value in samples:

        rho[
            i,
            j,
            k
        ] = value

    kernel = yukawa_kernel_grid(
        n,
        dx,
        dV,
        True,
    )

    psi_fft = (
        fftconvolve(
            rho,
            kernel,
            mode="same",
        )
        *
        dV
    )

    req = (
        3.0
        *
        dV
        /
        (
            4.0
            *
            math.pi
        )
    )**(
        1.0
        /
        3.0
    )

    self_kernel = (
        sphere_self_factor(
            MU
            *
            req
        )
        /
        req
    )

    errors = []

    source_points = []

    for i, j, k, value in samples:

        source_points.append(
            (
                np.array(
                    (
                        i,
                        j,
                        k,
                    ),
                    dtype=float,
                )
                *
                dx,
                value,
            )
        )

    for i in range(
        n
    ):

        for j in range(
            n
        ):

            for k in range(
                n
            ):

                x = (
                    np.array(
                        (
                            i,
                            j,
                            k,
                        ),
                        dtype=float,
                    )
                    *
                    dx
                )

                direct = 0.0

                for y, value in source_points:

                    distance = float(
                        np.linalg.norm(
                            x
                            -
                            y
                        )
                    )

                    if distance == 0.0:

                        kval = self_kernel

                    else:

                        kval = (
                            math.exp(
                                -MU
                                *
                                distance
                            )
                            /
                            distance
                        )

                    direct += (
                        value
                        *
                        dV
                        *
                        kval
                    )

                errors.append(
                    abs(
                        direct
                        -
                        float(
                            psi_fft[
                                i,
                                j,
                                k
                            ]
                        )
                    )
                    /
                    max(
                        abs(
                            direct
                        ),
                        abs(
                            float(
                                psi_fft[
                                    i,
                                    j,
                                    k
                                ]
                            )
                        ),
                        1.0e-14,
                    )
                )

    max_error = float(
        max(
            errors
        )
    )

    return {
        "max_relerr":
        max_error,

        "pass":
        bool(
            max_error
            <=
            2.0e-11
        ),
    }


def self_energy_coefficient(
    reconstructed,
    sector_name,
):

    shape = reconstructed[
        "shape"
    ]

    if not (
        shape[
            0
        ]
        ==
        shape[
            1
        ]
        ==
        shape[
            2
        ]
    ):

        raise RuntimeError(
            "Self-energy FFT expects cubic source lattice"
        )

    n = shape[
        0
    ]

    dx = reconstructed[
        "dx_phys_m"
    ]

    dV = reconstructed[
        "dV_phys_m3"
    ]

    fraction_cells = reconstructed[
        "sector_fraction_cells"
    ][
        sector_name
    ].reshape(
        shape
    )

    energy_density_fraction_per_m3 = (
        fraction_cells
        /
        dV
    )

    rho_mass_per_joule_alpha1 = (
        energy_density_fraction_per_m3
        /
        C**2
    )

    kernel = yukawa_kernel_grid(
        n,
        dx,
        dV,
        True,
    )

    psi = (
        fftconvolve(
            rho_mass_per_joule_alpha1,
            kernel,
            mode="same",
        )
        *
        dV
    )

    coeff_total = (
        G
        *
        float(
            np.sum(
                rho_mass_per_joule_alpha1
                *
                psi
            )
            *
            dV
        )
    )

    req = (
        3.0
        *
        dV
        /
        (
            4.0
            *
            math.pi
        )
    )**(
        1.0
        /
        3.0
    )

    self_kernel = (
        sphere_self_factor(
            MU
            *
            req
        )
        /
        req
    )

    q_cell_per_joule_alpha1 = (
        fraction_cells
        /
        C**2
    )

    coeff_self = (
        G
        *
        self_kernel
        *
        float(
            np.sum(
                q_cell_per_joule_alpha1**2
            )
        )
    )

    if coeff_total <= 0.0:

        raise RuntimeError(
            "Nonpositive scalar self-energy coefficient"
        )

    return {
        "coefficient_per_J":
        coeff_total,

        "self_coefficient_per_J":
        coeff_self,

        "self_fraction":
        (
            coeff_self
            /
            coeff_total
        ),
    }


def influence_concentration(
    reconstructed,
    sector_name,
    direction,
):

    ky, _kn = direction_kernel(
        reconstructed[
            "xyz_m"
        ],
        direction,
    )

    weights = reconstructed[
        "sector_fraction_cells"
    ][
        sector_name
    ]

    contribution = (
        weights
        *
        ky
    )

    total_contribution = float(
        np.sum(
            contribution
        )
    )

    total_sector_fraction = float(
        np.sum(
            weights
        )
    )

    order = np.argsort(
        contribution
    )[
        ::-1
    ]

    cumulative_influence = np.cumsum(
        contribution[
            order
        ]
    )

    cumulative_energy = np.cumsum(
        weights[
            order
        ]
    )

    def energy_for_fraction(
        target,
    ):

        index = int(
            np.searchsorted(
                cumulative_influence,
                target
                *
                total_contribution,
                side="left",
            )
        )

        index = min(
            index,
            len(
                cumulative_energy
            )
            -
            1,
        )

        return float(
            cumulative_energy[
                index
            ]
            /
            total_sector_fraction
        )

    xyz = reconstructed[
        "xyz_m"
    ]

    projected = (
        xyz
        @
        direction
    )

    front = float(
        np.sum(
            weights[
                projected
                >=
                0.0
            ]
        )
    )

    rear = float(
        np.sum(
            weights[
                projected
                <
                0.0
            ]
        )
    )

    asymmetry = (
        (
            front
            -
            rear
        )
        /
        max(
            front
            +
            rear,
            1.0e-300,
        )
    )

    dipole_vector = np.sum(
        weights[
            :,
            None
        ]
        *
        xyz,
        axis=0,
    ) / max(
        total_sector_fraction,
        1.0e-300,
    )

    dipole_over_r = float(
        np.linalg.norm(
            dipole_vector
        )
        /
        SOURCE_RADIUS_M
    )

    return {
        "F50_energy_fraction":
        energy_for_fraction(
            0.50
        ),

        "F90_energy_fraction":
        energy_for_fraction(
            0.90
        ),

        "front_fraction":
        (
            front
            /
            max(
                front
                +
                rear,
                1.0e-300,
            )
        ),

        "rear_fraction":
        (
            rear
            /
            max(
                front
                +
                rear,
                1.0e-300,
            )
        ),

        "front_rear_asymmetry":
        asymmetry,

        "dipole_over_source_radius":
        dipole_over_r,

        "productive_charge_participation":
        1.0,
    }


def ledger_at_alpha(
    scalar_A_per_alpha_J,
    gr_B_per_J,
    self_C_per_J,
    alpha_x,
):

    denominator = (
        scalar_A_per_alpha_J
        *
        alpha_x
        -
        gr_B_per_J
    )

    if denominator <= 0.0:

        return {
            "valid":
            False,

            "E_B7_J":
            math.inf,

            "E_scalar_J":
            math.inf,

            "E_total_J":
            math.inf,
        }

    E_B7 = (
        G0
        /
        denominator
    )

    E_scalar = (
        self_C_per_J
        *
        alpha_x**2
        *
        E_B7**2
    )

    return {
        "valid":
        True,

        "E_B7_J":
        E_B7,

        "E_scalar_J":
        E_scalar,

        "E_total_J":
        (
            E_B7
            +
            E_scalar
        ),
    }


def required_alpha_for_target(
    scalar_A_per_alpha_J,
    gr_B_per_J,
    self_C_per_J,
    target_energy,
):

    asymptotic_floor = (
        self_C_per_J
        *
        G0**2
        /
        scalar_A_per_alpha_J**2
    )

    if asymptotic_floor >= target_energy:

        return {
            "reachable":
            False,

            "asymptotic_floor_J":
            asymptotic_floor,

            "alpha_required":
            math.inf,
        }

    alpha_threshold = (
        gr_B_per_J
        /
        scalar_A_per_alpha_J
    )

    lower = max(
        1.0,
        alpha_threshold
        *
        (
            1.0
            +
            1.0e-9
        ),
    )

    def residual(
        alpha,
    ):

        ledger = ledger_at_alpha(
            scalar_A_per_alpha_J,
            gr_B_per_J,
            self_C_per_J,
            alpha,
        )

        return (
            ledger[
                "E_total_J"
            ]
            -
            target_energy
        )

    upper = max(
        lower
        *
        10.0,
        1.0e12,
    )

    while (
        residual(
            upper
        )
        >
        0.0
        and
        upper
        <
        1.0e24
    ):

        upper *= 10.0

    if residual(
        upper
    ) > 0.0:

        return {
            "reachable":
            False,

            "asymptotic_floor_J":
            asymptotic_floor,

            "alpha_required":
            math.inf,
        }

    alpha_required = brentq(
        residual,
        lower,
        upper,
        xtol=1.0e-8,
        rtol=2.0e-12,
        maxiter=300,
    )

    return {
        "reachable":
        True,

        "asymptotic_floor_J":
        asymptotic_floor,

        "alpha_required":
        alpha_required,

        "f_eff_GeV":
        (
            MPL_GEV
            /
            alpha_required
        ),
    }


def normalized_curve_difference(
    a,
    b,
):

    an = (
        a
        /
        np.mean(
            a
        )
    )

    bn = (
        b
        /
        np.mean(
            b
        )
    )

    return float(
        np.linalg.norm(
            an
            -
            bn
        )
        /
        max(
            np.linalg.norm(
                bn
            ),
            1.0e-300,
        )
    )


def main():

    print(
        "=== 031B1-A B7 FIXED-FIELD Z2 "
        "SCALAR-CHARGE TOMOGRAPHY ==="
    )

    print(
        "CLAIM_CLASS="
        "FIXED_MICROSCOPIC_FIELD_SCALAR_CHARGE_"
        "TOMOGRAPHY_AND_ENERGY_FLOOR_GATE"
    )

    print(
        "B7_REEQUILIBRATED=NO"
    )

    print(
        "SCALAR_CHARGE_SPATIAL_FUNCTION_PRESCRIBED=NO"
    )

    print(
        "SCALAR_CHARGE_MAP_FROM_EXISTING_B7_INVARIANT=YES"
    )

    print(
        "FULL_COUPLED_FIELD_SOLUTION=NO"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    for path in (
        CR3_SOURCE,
        N73_FIELD,
        N81_FIELD,
        R4S_SUMMARY,
    ):

        require(
            path
        )

    r4s = json.loads(
        R4S_SUMMARY.read_text()
    )

    if not bool(
        r4s[
            "energy_target_pass"
        ]
    ):

        raise RuntimeError(
            "R4S 83-GJ target is not GREEN"
        )

    TARGET_E_J = float(
        r4s[
            "target_energy_J"
        ]
    )

    ALPHA_M = float(
        r4s[
            "scaling"
        ][
            "alpha_m_cap_required"
        ]
    )

    ALPHA_X_R4S = abs(
        float(
            r4s[
                "scaling"
            ][
                "alpha_x_center_nominal_required"
            ]
        )
    )

    print(
        f"TARGET_E_J="
        f"{TARGET_E_J:.15e}"
    )

    print(
        f"R4S_ALPHA_M_ON="
        f"{ALPHA_M:.15e}"
    )

    print(
        f"R4S_ALPHA_X_MAG="
        f"{ALPHA_X_R4S:.15e}"
    )

    print(
        f"MEDIATOR_RANGE_M="
        f"{MEDIATOR_RANGE_M:.15e}"
    )

    print(
        f"SOURCE_RADIUS_M="
        f"{SOURCE_RADIUS_M:.15e}"
    )

    print(
        f"PAYLOAD_CENTER_M="
        f"{PAYLOAD_CENTER_M:.15e}"
    )

    print(
        f"PAYLOAD_RADIUS_M="
        f"{PAYLOAD_RADIUS_M:.15e}"
    )

    fp = payload_factor(
        MU,
        PAYLOAD_RADIUS_M,
    )

    print(
        f"FINITE_PAYLOAD_HELMHOLTZ_FACTOR="
        f"{fp:.15e}"
    )

    print(
        "\n=== A — FFT YUKAWA "
        "INDEPENDENT VALIDATION ==="
    )

    validation = validate_fft_convolution()

    print(
        f"FFT_YUKAWA_PAIRSUM_MAX_RELERR="
        f"{validation['max_relerr']:.15e}"
    )

    print(
        "FFT_YUKAWA_VALIDATION="
        +
        (
            "PASS"
            if validation[
                "pass"
            ]
            else
            "FAIL"
        )
    )

    if not validation[
        "pass"
    ]:

        raise RuntimeError(
            "FFT Yukawa convolution validation failed"
        )

    cr3 = load_module(
        "b1a_cr3",
        CR3_SOURCE,
    )

    directions = fibonacci_sphere(
        N_DIRECTIONS
    )

    grid_results = {}

    csv_rows = []

    for grid_name, path, n in (
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

        print(
            f"\n=== B — RECONSTRUCT {grid_name} B7 ==="
        )

        field = load_field(
            path,
            n,
        )

        print(
            f"{grid_name}_S3_NORM_MAXERR="
            f"{field['normerr']:.15e}"
        )

        reconstructed = reconstruct_b7(
            cr3,
            field,
        )

        print(
            f"{grid_name}_CONTINUUM_E_TOTAL="
            f"{reconstructed['total_energy_dimless']:.15e}"
        )

        for name in SECTORS:

            energy = reconstructed[
                "energies"
            ][
                name
            ]

            fraction = (
                energy
                /
                reconstructed[
                    "total_energy_dimless"
                ]
            )

            print(
                f"{grid_name}_SECTOR "
                f"NAME={name} "
                f"E={energy:.15e} "
                f"FRACTION={fraction:.15e}"
            )

        print(
            f"{grid_name}_PHYSICAL_SCALE_M_PER_DIMLESS="
            f"{reconstructed['physical_scale_m_per_dimless']:.15e}"
        )

        print(
            f"{grid_name}_PHYSICAL_DX_M="
            f"{reconstructed['dx_phys_m']:.15e}"
        )

        print(
            f"\n=== C — {grid_name} DENSE ORIENTATION TOMOGRAPHY ==="
        )

        orientation = orientation_tomography(
            reconstructed,
            directions,
        )

        gr_B_max = (
            G
            /
            C**2
            *
            float(
                np.max(
                    orientation[
                        "gr_leverage"
                    ]
                )
            )
        )

        sector_results = {}

        for name in SECTORS:

            leverage = orientation[
                "scalar_leverage"
            ][
                name
            ]

            worst_index = int(
                np.argmin(
                    leverage
                )
            )

            worst_direction = directions[
                worst_index
            ]

            min_leverage = float(
                leverage[
                    worst_index
                ]
            )

            mean_leverage = float(
                np.mean(
                    leverage
                )
            )

            max_leverage = float(
                np.max(
                    leverage
                )
            )

            scalar_A = (
                2.0
                *
                G
                *
                ALPHA_M
                *
                fp
                /
                C**2
                *
                min_leverage
            )

            self_energy = self_energy_coefficient(
                reconstructed,
                name,
            )

            ledger_r4s = ledger_at_alpha(
                scalar_A,
                gr_B_max,
                self_energy[
                    "coefficient_per_J"
                ],
                ALPHA_X_R4S,
            )

            target = required_alpha_for_target(
                scalar_A,
                gr_B_max,
                self_energy[
                    "coefficient_per_J"
                ],
                TARGET_E_J,
            )

            morphology = influence_concentration(
                reconstructed,
                name,
                worst_direction,
            )

            sector_fraction = (
                reconstructed[
                    "energies"
                ][
                    name
                ]
                /
                reconstructed[
                    "total_energy_dimless"
                ]
            )

            qabs_r4s = (
                ALPHA_X_R4S
                *
                sector_fraction
                *
                ledger_r4s[
                    "E_B7_J"
                ]
                /
                C**2
                if ledger_r4s[
                    "valid"
                ]
                else
                math.inf
            )

            result = {
                "grid":
                grid_name,

                "sector":
                name,

                "sector_fraction":
                sector_fraction,

                "worst_direction_index":
                worst_index,

                "worst_direction":
                worst_direction,

                "scalar_leverage_min_m2inv":
                min_leverage,

                "scalar_leverage_mean_m2inv":
                mean_leverage,

                "scalar_leverage_max_m2inv":
                max_leverage,

                "gr_acceleration_coeff_max_per_J":
                gr_B_max,

                "scalar_acceleration_coeff_per_alphaX_J":
                scalar_A,

                "self_energy_coeff_per_J":
                self_energy[
                    "coefficient_per_J"
                ],

                "self_energy_self_fraction":
                self_energy[
                    "self_fraction"
                ],

                "R4S_alphaX":
                ALPHA_X_R4S,

                "R4S_E_B7_J":
                ledger_r4s[
                    "E_B7_J"
                ],

                "R4S_E_scalar_J":
                ledger_r4s[
                    "E_scalar_J"
                ],

                "R4S_E_total_J":
                ledger_r4s[
                    "E_total_J"
                ],

                "R4S_83GJ_pass":
                bool(
                    ledger_r4s[
                        "valid"
                    ]
                    and
                    ledger_r4s[
                        "E_total_J"
                    ]
                    <=
                    TARGET_E_J
                    *
                    (
                        1.0
                        +
                        TARGET_REL_TOL
                    )
                ),

                "Qabs_R4S_kg":
                qabs_r4s,

                **target,

                **morphology,
            }

            sector_results[
                name
            ] = {
                **result,

                "_leverage_curve":
                leverage,
            }

            print(
                f"{grid_name}_SCALAR_SECTOR "
                f"NAME={name} "
                f"ENERGY_FRACTION="
                f"{sector_fraction:.9e} "
                f"K_MIN="
                f"{min_leverage:.9e} "
                f"K_MEAN="
                f"{mean_leverage:.9e} "
                f"K_MAX="
                f"{max_leverage:.9e} "
                f"SELF_COEFF="
                f"{self_energy['coefficient_per_J']:.9e} "
                f"SELF_CELL_FRACTION="
                f"{self_energy['self_fraction']:.9e}"
            )

            print(
                f"{grid_name}_83GJ_LEDGER "
                f"NAME={name} "
                f"E_B7_J="
                f"{ledger_r4s['E_B7_J']:.9e} "
                f"E_SCALAR_J="
                f"{ledger_r4s['E_scalar_J']:.9e} "
                f"E_TOTAL_J="
                f"{ledger_r4s['E_total_J']:.9e} "
                f"PASS="
                f"{result['R4S_83GJ_pass']}"
            )

            print(
                f"{grid_name}_ASYMPTOTIC "
                f"NAME={name} "
                f"E_FLOOR_J="
                f"{target['asymptotic_floor_J']:.9e} "
                f"TARGET_REACHABLE="
                f"{target['reachable']} "
                f"ALPHA_X_REQUIRED="
                f"{target.get('alpha_required', math.inf):.9e} "
                f"F_EFF_GEV="
                f"{target.get('f_eff_GeV', 0.0):.9e}"
            )

            print(
                f"{grid_name}_MORPHOLOGY "
                f"NAME={name} "
                f"F50_ENERGY="
                f"{morphology['F50_energy_fraction']:.9e} "
                f"F90_ENERGY="
                f"{morphology['F90_energy_fraction']:.9e} "
                f"FRONT_REAR_ASYM="
                f"{morphology['front_rear_asymmetry']:.9e} "
                f"DIPOLE_OVER_R="
                f"{morphology['dipole_over_source_radius']:.9e}"
            )

            csv_rows.append(
                {
                    key:
                    to_builtin(
                        value
                    )
                    for key, value
                    in result.items()
                    if key
                    !=
                    "worst_direction"
                }
            )

        grid_results[
            grid_name
        ] = {
            "reconstructed":
            reconstructed,

            "orientation":
            orientation,

            "sectors":
            sector_results,
        }

    print(
        "\n=== D — N73 -> N81 "
        "SCALAR-CHARGE CONTINUUM PREFLIGHT ==="
    )

    pair_results = {}

    strong_survivors = []

    weak_survivors = []

    for name in SECTORS:

        a = grid_results[
            "N73"
        ][
            "sectors"
        ][
            name
        ]

        b = grid_results[
            "N81"
        ][
            "sectors"
        ][
            name
        ]

        fraction_rel = relerr(
            a[
                "sector_fraction"
            ],
            b[
                "sector_fraction"
            ],
        )

        kernel_curve_rel = normalized_curve_difference(
            a[
                "_leverage_curve"
            ],
            b[
                "_leverage_curve"
            ],
        )

        self_coeff_rel = relerr(
            a[
                "self_energy_coeff_per_J"
            ],
            b[
                "self_energy_coeff_per_J"
            ],
        )

        floor_rel = relerr(
            a[
                "asymptotic_floor_J"
            ],
            b[
                "asymptotic_floor_J"
            ],
        )

        pair_pass = bool(
            fraction_rel
            <=
            PAIR_FRACTION_REL_TOL
            and
            kernel_curve_rel
            <=
            PAIR_KERNEL_CURVE_REL_TOL
            and
            self_coeff_rel
            <=
            PAIR_SELF_COEFF_REL_TOL
        )

        r4s_strong = bool(
            pair_pass
            and
            a[
                "R4S_83GJ_pass"
            ]
            and
            b[
                "R4S_83GJ_pass"
            ]
        )

        target_reachable_pair = bool(
            pair_pass
            and
            a[
                "reachable"
            ]
            and
            b[
                "reachable"
            ]
        )

        required_alpha_max = (
            max(
                a[
                    "alpha_required"
                ],
                b[
                    "alpha_required"
                ],
            )
            if target_reachable_pair
            else
            math.inf
        )

        within_10x_r4s = bool(
            target_reachable_pair
            and
            required_alpha_max
            <=
            10.0
            *
            ALPHA_X_R4S
        )

        pair = {
            "sector":
            name,

            "sector_fraction_relchange":
            fraction_rel,

            "kernel_curve_relative_difference":
            kernel_curve_rel,

            "self_coefficient_relchange":
            self_coeff_rel,

            "asymptotic_floor_relchange":
            floor_rel,

            "pair_convergence_pass":
            pair_pass,

            "R4S_alphaX_83GJ_pair_pass":
            r4s_strong,

            "target_reachable_pair":
            target_reachable_pair,

            "required_alpha_max":
            required_alpha_max,

            "required_alpha_over_R4S":
            (
                required_alpha_max
                /
                ALPHA_X_R4S
                if math.isfinite(
                    required_alpha_max
                )
                else
                math.inf
            ),

            "within_10x_R4S_alpha":
            within_10x_r4s,

            "N73_floor_J":
            a[
                "asymptotic_floor_J"
            ],

            "N81_floor_J":
            b[
                "asymptotic_floor_J"
            ],

            "N73_F90":
            a[
                "F90_energy_fraction"
            ],

            "N81_F90":
            b[
                "F90_energy_fraction"
            ],
        }

        pair_results[
            name
        ] = pair

        if r4s_strong:

            strong_survivors.append(
                name
            )

        elif (
            target_reachable_pair
            and
            within_10x_r4s
        ):

            weak_survivors.append(
                name
            )

        print(
            f"PAIR_GATE "
            f"NAME={name} "
            f"FRACTION_REL="
            f"{fraction_rel:.9e} "
            f"KERNEL_CURVE_REL="
            f"{kernel_curve_rel:.9e} "
            f"SELF_COEFF_REL="
            f"{self_coeff_rel:.9e} "
            f"FLOOR_REL="
            f"{floor_rel:.9e} "
            f"PAIR_PASS="
            f"{pair_pass} "
            f"R4S_83GJ_PASS="
            f"{r4s_strong} "
            f"ALPHA_REQ_OVER_R4S="
            f"{pair['required_alpha_over_R4S']:.9e}"
        )

    print(
        "\n=== E — PHYSICAL INTERPRETATION ==="
    )

    print(
        "ONE_SECTOR_DRESSINGS_TESTED="
        "e2,e4,V"
    )

    print(
        "ARBITRARY_SPATIAL_COUPLING_USED=NO"
    )

    print(
        "FULL_B7_ENERGY_INCLUDED_IN_GR_ATTRACTION=YES"
    )

    print(
        "SCALAR_FIELD_SELF_ENERGY_INCLUDED=YES"
    )

    print(
        "FINITE_PAYLOAD_INCLUDED=YES"
    )

    print(
        "DENSE_ORIENTATIONS="
        f"{N_DIRECTIONS}"
    )

    max_self_fraction = max(
        grid_results[
            grid
        ][
            "sectors"
        ][
            name
        ][
            "self_energy_self_fraction"
        ]
        for grid in (
            "N73",
            "N81",
        )
        for name in SECTORS
    )

    print(
        f"MAX_CELL_SELF_ENERGY_FRACTION="
        f"{max_self_fraction:.15e}"
    )

    print(
        "CELL_SELF_REGULARIZATION_WARNING="
        +
        (
            "YES"
            if max_self_fraction
            >
            SELF_FRACTION_WARN
            else
            "NO"
        )
    )

    print(
        "\n=== F — DECISION ==="
    )

    if strong_survivors:

        best = min(
            strong_survivors,
            key=lambda name:
            grid_results[
                "N81"
            ][
                "sectors"
            ][
                name
            ][
                "R4S_E_total_J"
            ],
        )

        classification = (
            "GREEN_B7_FIXED_FIELD_ONE_SECTOR_"
            "DRESSING_PRESERVES_83GJ_AT_R4S_"
            "SCALAR_SENSITIVITY"
        )

        next_step = (
            "031B1B_MINIMAL_B7_Z2_COUPLED_FIELD_"
            "REEQUILIBRATION_AND_CONSERVATION_GATE"
        )

    elif weak_survivors:

        best = min(
            weak_survivors,
            key=lambda name:
            pair_results[
                name
            ][
                "required_alpha_over_R4S"
            ],
        )

        classification = (
            "YELLOW_B7_ONE_SECTOR_MORPHOLOGY_HAS_"
            "SUB83GJ_FIELD_FLOOR_BUT_REQUIRES_"
            "STRONGER_SCALAR_SENSITIVITY"
        )

        next_step = (
            "031B2_QBALL_QSHELL_INDEPENDENT_CONTROL_"
            "BEFORE_B7_REEQUILIBRATION"
        )

    else:

        best = "NONE"

        classification = (
            "RED_SIMPLE_B7_E2_E4_V_ONE_SECTOR_"
            "DRESSINGS_FAIL_83GJ_FIXED_FIELD_GATE"
        )

        next_step = (
            "031B2_QBALL_QSHELL_INDEPENDENT_"
            "SCALAR_CHARGE_SOURCE"
        )

    print(
        f"STRONG_83GJ_SECTOR_SURVIVORS="
        f"{','.join(strong_survivors) if strong_survivors else 'NONE'}"
    )

    print(
        f"WEAK_SUB83GJ_FLOOR_SURVIVORS="
        f"{','.join(weak_survivors) if weak_survivors else 'NONE'}"
    )

    print(
        f"BEST_B7_SCALAR_SECTOR="
        f"{best}"
    )

    print(
        f"031B1A_CLASSIFICATION="
        f"{classification}"
    )

    print(
        f"NEXT="
        f"{next_step}"
    )

    print(
        "FULL_COUPLED_B7_SCALAR_FIELD="
        "NOT_YET"
    )

    print(
        "FULL_LOCAL_CONSERVATION="
        "NOT_YET"
    )

    print(
        "EFT_NATURALNESS="
        "NOT_YET"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    summary = {
        "claim_class":
        (
            "FIXED_MICROSCOPIC_FIELD_SCALAR_CHARGE_"
            "TOMOGRAPHY_AND_ENERGY_FLOOR_GATE"
        ),

        "target_energy_J":
        TARGET_E_J,

        "target_acceleration_mps2":
        G0,

        "R4S_alpha_m_on":
        ALPHA_M,

        "R4S_alpha_x_magnitude":
        ALPHA_X_R4S,

        "mediator_range_m":
        MEDIATOR_RANGE_M,

        "source_radius_m":
        SOURCE_RADIUS_M,

        "payload_radius_m":
        PAYLOAD_RADIUS_M,

        "payload_center_m":
        PAYLOAD_CENTER_M,

        "finite_payload_factor":
        fp,

        "fft_validation":
        validation,

        "pair_results":
        pair_results,

        "strong_survivors":
        strong_survivors,

        "weak_survivors":
        weak_survivors,

        "best_sector":
        best,

        "max_cell_self_energy_fraction":
        max_self_fraction,

        "classification":
        classification,

        "next":
        next_step,

        "claim_limits": [
            "B7 is not re-equilibrated after scalar dressing.",
            "The physical B7 dimensional scale is normalized for morphology tomography rather than microscopically derived.",
            "The X/scalar source coupling is a fixed-field derivative attribution only.",
            "Full source/support local conservation after dressing is not established.",
            "Nonradial stability of the coupled system is not established.",
            "EFT and radiative naturalness remain open.",
            "Empirical off-state closure remains open.",
            "026C N89 remains mandatory for the old pure-GR B7 force-convergence credibility branch.",
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

    if csv_rows:

        fieldnames = []

        for row in csv_rows:

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
                csv_rows
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
