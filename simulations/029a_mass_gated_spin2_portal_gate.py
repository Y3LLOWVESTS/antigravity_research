#!/usr/bin/env python3
"""029A — mass-gated massive-spin-2 portal gate.

PURPOSE
-------
Test a genuinely different practicality mechanism after 028A--028C closed the
tested local scalar gain classes.

Instead of making

    M_Pl,
    F(chi),
    or a kinetic eigenvalue

critical, 029A asks whether an additional healthy massive spin-2 mode can be:

    light inside the activated device region,
    heavy outside,
    universally coupled through the gravitational metric sector.

This is a spectral / mass-gap gain mechanism.

SCIENTIFIC QUESTIONS
--------------------
A. What source does a massive Fierz-Pauli spin-2 field see?

For exchange between conserved sources, the massless graviton trace coefficient
is 1/2 while the massive Fierz-Pauli trace coefficient is 1/3.

For a slow payload, the corresponding source combinations are therefore

    S_GR = rho + p1 + p2 + p3

and

    S_FP = 2 rho + p1 + p2 + p3.

For the B=7 Skyrme field used by the project,

    rho  = e2 + e4 + V

    S_GR = 2(e4 - V),

therefore

    S_FP = rho + S_GR
         = e2 + 3 e4 - V.

A massive spin-2 mode with relative matter coupling alpha contributes the
usual vDVZ 4/3 enhancement for dust. In the project's GR kernel
normalization this means

    a_FP
      =
    (2/3) alpha^2
    times the same spatial kernel applied to S_FP.

B. Can 006D simply be amplified?

No.

006D has

    p_z = 0

and satisfies DEC,

    p_r >= -rho,
    p_phi >= -rho.

Therefore pointwise

    S_FP
      =
    2 rho + p_r + p_phi
      >=
    0.

A one-sided Fierz-Pauli mode is therefore attractive or zero on 006D.

029A records this as an analytic control and DOES NOT pretend that the new
mode simply multiplies C_006D.

C. Does the ACTUAL B7 field possess an external massive-spin-2 repulsive
channel?

Use the authoritative strict stationary fields

    N=73
    N=81

and reconstruct independently

    e2,
    e4,
    V,
    rho,
    S_GR,
    S_FP.

The field is audited through

    integral S_GR / E ~= 1
    integral S_FP / E ~= 2,

the expected static virial/Laue result.

The scan then evaluates finite-payload force outside an energy-enclosing
source radius.

D. If B7 is the wrong microscopic field, does an independently conserved
positive-energy DEC source exist for the Fierz-Pauli kernel?

A second-order-cone axisymmetric finite-volume optimizer searches directly
over

    epsilon >= 0,
    p_r,
    p_z,
    p_phi,
    T_rz,

with:

    exact discrete local force balance,
    traction-free boundaries,
    axis regularity,
    exact type-I DEC,
    global Laue balance.

The objective is a finite true-stand-off Fierz-Pauli field, not GR.

E. If a source survives, can mass-gating attack the 1/G practicality scale?

For a selected source, solve for the relative massive-mode coupling alpha
required to meet:

PRIMARY TARGET
    1 g
    1 m
    total energy <= 1 TJ

SECONDARY TARGET
    0.1 g
    1 cm
    total energy <= 1 PJ.

The source is allocated 90% of total budget.
10% is reserved for the gain/control sector.

MASSIVE-SPIN-2 EFT GATES
------------------------
Inside mediator mass:

    m_in h = mu_h.

The absolute maximum healthy gravitational massive-spin-2 strong-coupling
scale is

    Lambda_3 = (m_in^2 M_Pl)^(1/3).

A stricter coupling-aware diagnostic is also reported using

    M_eff = M_Pl / max(alpha,1).

Require the coupling-aware Lambda_3 to exceed the inverse device scale by
at least 100x for route-level promotion.

Vainshtein diagnostic:

    r_V ~ (alpha r_s / m_in^2)^(1/3).

Require

    r_V / h < 0.1

so that the payload is not inside a strongly nonlinear screened region.

EXTERIOR MASS GATING
--------------------
A globally light strongly coupled massive spin-2 mode is observationally
unacceptable.

029A therefore does NOT allow the interior mode to remain light outside.

It asks for an exterior mass m_out such that the Yukawa force attenuation
through a transition layer obeys

    alpha_Y (1+x) exp(-x)
        <=
    1e-4,

where

    alpha_Y = (4/3) alpha^2,
    x = m_out ell.

The 1e-4 value is an explicit conservative engineering proxy, not a
replacement for a wavelength-by-wavelength published fifth-force analysis.

CONTROL-WALL LOWER BOUND
------------------------
Mass-varying massive-gravity models can use a scalar to set the graviton
mass.

For a deliberately favorable canonical scalar relation

    m_g = g chi

with

    g <= 4 pi,

029A computes the minimum gradient-energy floor required to change from
m_in to m_out across the wall.

This is ONLY a lower bound.

It omits:

    scalar potential energy,
    full bimetric interaction-potential energy,
    backreaction,
    junction-condition energy,
    global cosmological consistency.

Thus a RED result is strong.

A GREEN result is only authorization for a full covariant localized
bimetric/mass-varying solve.

FINITE PAYLOAD
--------------
For the B7 branch the payload sphere has

    R_payload = 0.10 h_numerical.

Seven deterministic points are checked:

    center,
    near axial surface,
    far axial surface,
    +/- transverse basis 1,
    +/- transverse basis 2.

All must accelerate outward along the intended thrust axis.

TRUE-STANDOFF / TAIL CONTROL
----------------------------
The numerical Skyrmion has an exponentially decaying continuum tail but is
represented in a finite vacuum box.

Define R_999999 as the radius enclosing 99.9999% of continuum energy.

All payload samples must lie outside R_999999.

The residual energy outside the near payload surface is explicitly recorded.

This is called

    TAIL_CONTROLLED_EXTERNAL_STANDOFF

rather than a mathematical compact-support theorem.

B7 RESOLUTION GATE
------------------
Candidate selection uses N73 only.

The exact same:

    orientation,
    stand-off factor,
    mu_h

is then tested on N81.

Promotion requires:

    all seven FP payload samples outward on N73 and N81,
    N73->N81 C_FP relative change <= 0.25,
    maximum cancellation factor <= 100,
    virial/source identities green,
    tail fraction <= 2e-6.

A weaker sign survivor is retained as YELLOW but cannot earn the 80 marker.

RELAXED SOURCE GATE
-------------------
The independent DEC finite-volume optimizer is allowed to promote source-level
headroom, but NEVER the route-level 80 marker by itself because it is not a
microscopic matter realization.

80-PERCENT RULE
---------------
The project's percentage is a heuristic of accumulated research
knowledge/accomplishment, NOT probability of success.

ROUTE_LEVEL_80_HEURISTIC_AUTHORIZED may become YES only if:

1. the ACTUAL B7 microscopic field has tail-controlled external FP repulsion;
2. N73 and N81 agree under the strict gate above;
3. the 1 g / 1 m / 1 TJ portal meets:
       coupling-aware Lambda3 margin >= 100,
       r_V/h < 0.1,
       exterior attenuation gate,
       canonical wall lower bound <= 10% budget;
4. no negative interaction/control energy is credited;
5. 94-test baseline is green.

Even then:

    PRACTICAL_ANTIGRAVITY_DEVICE = NO

because a localized nonlinear ghost-free bimetric solution is not yet solved.

CLAIM LIMITS
------------
This run does NOT establish:

- full nonlinear Hassan-Rosen / dRGT field equations for the device;
- a spatially localized mass-varying solution;
- full scalar control-sector stress-energy;
- cosmological viability;
- all laboratory fifth-force bounds;
- N89 B7 convergence;
- full B7 Hessian/fission stability;
- reactionless propulsion;
- a practical antigravity device;
- discovery of new physics.

REFERENCES
----------
Fierz-Pauli / vDVZ massive spin-2 exchange.
Ghost-free Hassan-Rosen bimetric gravity.
Mass-varying massive gravity.
Universal Lambda_3 massive-spin-2 strong-coupling bound.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_TRUE_ANTIGRAVITY_MASS_GATED_SPIN2_PORTAL_PREFLIGHT
"""

from __future__ import annotations

import csv
import json
import math
import os
from pathlib import Path
from typing import Any

import cvxpy as cp
import numpy as np
from numpy.polynomial.legendre import leggauss


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "data"

FIELD_PATHS = {
    73: DATA / "026a_true_antigravity_strict_stationary_b7_n73.npz",
    81: DATA / "026b_true_antigravity_strict_stationary_b7_n81.npz",
}

LINEAGE_028C = DATA / "028c_onshell_cubic_braiding_closure_summary.json"

OUT_JSON = DATA / "029a_mass_gated_spin2_portal_summary.json"
OUT_B7 = DATA / "029a_b7_fp_standoff_scan.csv"
OUT_RELAXED = DATA / "029a_relaxed_fp_dec_source_scan.csv"
OUT_PORTAL = DATA / "029a_spin2_portal_scaling.csv"

SMOKE = os.environ.get("AG029A_SMOKE", "0") == "1"

B = 7
ETA = 0.4
MASS = 8.0

C_LIGHT = 299_792_458.0
G_NEWTON = 6.67430e-11
G0 = 9.80665

HBARC_EV_M = 1.973269804e-7
EV_J = 1.602176634e-19
MPL_REDUCED_EV = 2.435e27

ENERGY_ENCLOSED = 0.999999
TAIL_MAX = 2.0e-6

PAYLOAD_RADIUS_RATIO = 0.10

MAX_B7_C_RELCHANGE = 0.25
MAX_B7_CANCELLATION = 100.0

SOURCE_BUDGET_FRACTION = 0.90
CONTROL_BUDGET_FRACTION = 0.10

ALPHA_Y_OUT_MAX = 1.0e-4
PRIMARY_WALL_FRACTION = 0.25
PRIMARY_LAMBDA3_MARGIN = 100.0
PRIMARY_VAINSHtein_RATIO = 0.10

DEC_TOL = 2.0e-5
CONS_TOL = 2.0e-5
LAUE_TOL = 2.0e-5

KNOWN_RADIAL = np.array(
    [
        -4.543501844637980e-1,
        1.878880658050992e-2,
        8.906249999999961e-1,
    ],
    dtype=float,
)
KNOWN_RADIAL /= np.linalg.norm(KNOWN_RADIAL)

if SMOKE:
    STANDOFF_FACTORS = (1.25,)
    MU_H_VALUES = (0.25,)
    FIBONACCI_COUNT = 0

    RELAXED_GEOMETRIES = (
        (6, 8, 2.0, 1.25),
    )
    RELAXED_MU = (0.25,)

else:
    STANDOFF_FACTORS = (
        1.12,
        1.25,
        1.50,
        2.00,
    )

    MU_H_VALUES = (
        0.03,
        0.10,
        0.25,
        0.50,
        1.00,
        2.00,
    )

    FIBONACCI_COUNT = 24

    RELAXED_GEOMETRIES = (
        (10, 14, 1.5, 1.00),
        (10, 14, 2.5, 1.50),
        (10, 14, 4.0, 2.00),
    )

    RELAXED_MU = (
        0.03,
        0.10,
        0.25,
        0.50,
        1.00,
    )


TARGETS = (
    (
        "MACRO_1G_1M_1TJ",
        G0,
        1.0,
        1.0e12,
    ),
    (
        "SUBSCALE_0P1G_1CM_1PJ",
        0.1 * G0,
        0.01,
        1.0e15,
    ),
)


def jfloat(x: Any) -> Any:
    """Convert NumPy/scalar values into JSON-safe finite Python values."""

    if isinstance(x, np.generic):
        x = x.item()

    if isinstance(x, float):
        if not math.isfinite(x):
            return None

    return x


def jsonable(obj: Any) -> Any:
    """Recursively make a scientific result JSON-safe."""

    if isinstance(obj, dict):
        return {
            str(k): jsonable(v)
            for k, v in obj.items()
            if not str(k).startswith("_")
        }

    if isinstance(obj, (list, tuple)):
        return [
            jsonable(v)
            for v in obj
        ]

    if isinstance(obj, np.ndarray):
        return obj.tolist()

    return jfloat(obj)


def require(path: Path) -> None:
    """Fail closed on absent lineage or field artifacts."""

    if not path.is_file():
        raise RuntimeError(
            f"Required file missing: {path}"
        )


for path in (
    *FIELD_PATHS.values(),
    LINEAGE_028C,
):
    require(path)


J028C = json.loads(
    LINEAGE_028C.read_text(
        encoding="utf-8",
    )
)

if not str(
    J028C.get(
        "decision",
        "",
    )
).startswith(
    "DECISIVE_RED_"
):
    raise RuntimeError(
        "029A expects the completed decisive-RED 028C lineage"
    )


def central4_derivatives(
    phi: np.ndarray,
    dx: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Fourth-order centered spatial derivatives on the 2-cell interior."""

    qx = (
        phi[:-4, 2:-2, 2:-2]
        - 8.0 * phi[1:-3, 2:-2, 2:-2]
        + 8.0 * phi[3:-1, 2:-2, 2:-2]
        - phi[4:, 2:-2, 2:-2]
    ) / (
        12.0 * dx
    )

    qy = (
        phi[2:-2, :-4, 2:-2]
        - 8.0 * phi[2:-2, 1:-3, 2:-2]
        + 8.0 * phi[2:-2, 3:-1, 2:-2]
        - phi[2:-2, 4:, 2:-2]
    ) / (
        12.0 * dx
    )

    qz = (
        phi[2:-2, 2:-2, :-4]
        - 8.0 * phi[2:-2, 2:-2, 1:-3]
        + 8.0 * phi[2:-2, 2:-2, 3:-1]
        - phi[2:-2, 2:-2, 4:]
    ) / (
        12.0 * dx
    )

    return qx, qy, qz


def reconstruct_b7(
    n: int,
) -> dict[str, Any]:
    """Reconstruct the B7 continuum stress sources independently."""

    path = FIELD_PATHS[n]

    with np.load(
        path,
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

        stored_active = (
            float(
                d["active_total"]
            )
            if "active_total" in d.files
            else None
        )

        grad_rms = (
            float(
                d["grad_rms"]
            )
            if "grad_rms" in d.files
            else None
        )

        grad_max = (
            float(
                d["grad_max"]
            )
            if "grad_max" in d.files
            else None
        )

    if phi.shape != (
        n,
        n,
        n,
        4,
    ):
        raise RuntimeError(
            f"N{n} unexpected field shape {phi.shape}"
        )

    if axis.shape != (
        n,
    ):
        raise RuntimeError(
            f"N{n} unexpected axis shape {axis.shape}"
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
            f"N{n} physical metadata mismatch"
        )

    norm_error = float(
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

    if norm_error > 5.0e-10:
        raise RuntimeError(
            f"N{n} S3 norm error {norm_error}"
        )

    qx, qy, qz = central4_derivatives(
        phi,
        dx,
    )

    gxx = np.sum(
        qx * qx,
        axis=-1,
    )
    gyy = np.sum(
        qy * qy,
        axis=-1,
    )
    gzz = np.sum(
        qz * qz,
        axis=-1,
    )

    gxy = np.sum(
        qx * qy,
        axis=-1,
    )
    gxz = np.sum(
        qx * qz,
        axis=-1,
    )
    gyz = np.sum(
        qy * qz,
        axis=-1,
    )

    e2 = (
        gxx
        + gyy
        + gzz
    )

    e4 = (
        gxx * gyy
        - gxy * gxy
        + gxx * gzz
        - gxz * gxz
        + gyy * gzz
        - gyz * gyz
    )

    sigma = phi[
        2:-2,
        2:-2,
        2:-2,
        0,
    ]

    potential = (
        MASS
        ** 2
        * (
            1.0
            - sigma
        )
        * (
            1.0
            + ETA
            * sigma
        )
    )

    rho = (
        e2
        + e4
        + potential
    )

    sgr = (
        2.0
        * (
            e4
            - potential
        )
    )

    sfp = (
        e2
        + 3.0
        * e4
        - potential
    )

    identity_error = float(
        np.max(
            np.abs(
                sfp
                - (
                    rho
                    + sgr
                )
            )
        )
    )

    coords_axis = axis[
        2:-2
    ]

    X, Y, Z = np.meshgrid(
        coords_axis,
        coords_axis,
        coords_axis,
        indexing="ij",
    )

    volume = (
        dx
        ** 3
    )

    energy = float(
        np.sum(
            rho
        )
        * volume
    )

    sgr_total = float(
        np.sum(
            sgr
        )
        * volume
    )

    sfp_total = float(
        np.sum(
            sfp
        )
        * volume
    )

    weights = (
        rho
        * volume
    )

    centroid = np.array(
        [
            float(
                np.sum(
                    weights
                    * X
                )
                / energy
            ),
            float(
                np.sum(
                    weights
                    * Y
                )
                / energy
            ),
            float(
                np.sum(
                    weights
                    * Z
                )
                / energy
            ),
        ],
        dtype=float,
    )

    coords = np.column_stack(
        [
            X.ravel(),
            Y.ravel(),
            Z.ravel(),
        ]
    )

    coords -= centroid[
        None,
        :
    ]

    rho_flat = rho.ravel()
    sgr_flat = sgr.ravel()
    sfp_flat = sfp.ravel()

    radii = np.linalg.norm(
        coords,
        axis=1,
    )

    order = np.argsort(
        radii
    )

    cumulative = np.cumsum(
        rho_flat[
            order
        ]
        * volume
    )

    target = (
        ENERGY_ENCLOSED
        * energy
    )

    index = int(
        np.searchsorted(
            cumulative,
            target,
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

    support_radius = float(
        radii[
            order[
                index
            ]
        ]
    )

    negative_fp_energy = float(
        np.sum(
            rho_flat[
                sfp_flat
                < 0.0
            ]
        )
        * volume
    )

    negative_gr_energy = float(
        np.sum(
            rho_flat[
                sgr_flat
                < 0.0
            ]
        )
        * volume
    )

    active_reconstruction_relerr = (
        abs(
            sgr_total
            - stored_active
        )
        / max(
            abs(
                stored_active
            ),
            1.0e-300,
        )
        if stored_active is not None
        else None
    )

    virial_gr_ratio = (
        sgr_total
        / energy
    )

    virial_fp_ratio = (
        sfp_total
        / energy
    )

    virial_green = bool(
        abs(
            virial_gr_ratio
            - 1.0
        )
        <= 0.03
        and abs(
            virial_fp_ratio
            - 2.0
        )
        <= 0.03
    )

    if (
        active_reconstruction_relerr
        is not None
        and active_reconstruction_relerr
        > 5.0e-8
    ):
        raise RuntimeError(
            (
                f"N{n} active-source reconstruction mismatch "
                f"{active_reconstruction_relerr}"
            )
        )

    return {
        "n":
            n,

        "dx":
            dx,

        "phi_norm_maxerr":
            norm_error,

        "grad_rms":
            grad_rms,

        "grad_max":
            grad_max,

        "energy":
            energy,

        "sgr_total":
            sgr_total,

        "sfp_total":
            sfp_total,

        "virial_gr_ratio":
            virial_gr_ratio,

        "virial_fp_ratio":
            virial_fp_ratio,

        "virial_green":
            virial_green,

        "stored_active_total":
            stored_active,

        "active_reconstruction_relerr":
            active_reconstruction_relerr,

        "sfp_identity_maxerr":
            identity_error,

        "energy_centroid":
            centroid,

        "support_radius":
            support_radius,

        "negative_fp_energy_fraction":
            negative_fp_energy
            / energy,

        "negative_gr_energy_fraction":
            negative_gr_energy
            / energy,

        "_coords":
            coords,

        "_radii":
            radii,

        "_rho":
            rho_flat,

        "_sgr":
            sgr_flat,

        "_sfp":
            sfp_flat,

        "_volume":
            volume,
    }


def fibonacci_sphere(
    count: int,
) -> list[np.ndarray]:
    """Deterministic unit vectors."""

    if count <= 0:
        return []

    k = np.arange(
        count,
        dtype=float,
    )

    golden = (
        math.pi
        * (
            3.0
            - math.sqrt(
                5.0
            )
        )
    )

    z = (
        1.0
        - 2.0
        * (
            k
            + 0.5
        )
        / count
    )

    rxy = np.sqrt(
        np.maximum(
            0.0,
            1.0
            - z * z,
        )
    )

    az = (
        golden
        * k
    )

    vec = np.column_stack(
        [
            rxy
            * np.cos(
                az
            ),
            rxy
            * np.sin(
                az
            ),
            z,
        ]
    )

    return [
        row
        / np.linalg.norm(
            row
        )
        for row in vec
    ]


def direction_table() -> list[tuple[str, np.ndarray]]:
    """Predetermined orientation set; no post-hoc random search."""

    rows: list[
        tuple[
            str,
            np.ndarray,
        ]
    ] = [
        (
            "KNOWN_026P",
            KNOWN_RADIAL.copy(),
        ),
        (
            "KNOWN_026P_ANTIPODE",
            -KNOWN_RADIAL.copy(),
        ),
        (
            "X_PLUS",
            np.array(
                [
                    1.0,
                    0.0,
                    0.0,
                ]
            ),
        ),
        (
            "X_MINUS",
            np.array(
                [
                    -1.0,
                    0.0,
                    0.0,
                ]
            ),
        ),
        (
            "Y_PLUS",
            np.array(
                [
                    0.0,
                    1.0,
                    0.0,
                ]
            ),
        ),
        (
            "Y_MINUS",
            np.array(
                [
                    0.0,
                    -1.0,
                    0.0,
                ]
            ),
        ),
        (
            "Z_PLUS",
            np.array(
                [
                    0.0,
                    0.0,
                    1.0,
                ]
            ),
        ),
        (
            "Z_MINUS",
            np.array(
                [
                    0.0,
                    0.0,
                    -1.0,
                ]
            ),
        ),
    ]

    for index, vec in enumerate(
        fibonacci_sphere(
            FIBONACCI_COUNT
        )
    ):
        rows.append(
            (
                f"FIB_{index:02d}",
                vec,
            )
        )

    return rows


DIRECTIONS = direction_table()


def yukawa_factor(
    distance: np.ndarray,
    mu: float,
) -> np.ndarray:
    """Radial-force Yukawa multiplier."""

    x = (
        mu
        * distance
    )

    return (
        (
            1.0
            + x
        )
        * np.exp(
            -x
        )
    )


def force_driver(
    field: dict[str, Any],
    point: np.ndarray,
    direction: np.ndarray,
    source_key: str,
    mu: float,
) -> dict[str, float]:
    """Return the dimensionless outward projected source functional."""

    coords = field[
        "_coords"
    ]

    source = field[
        source_key
    ]

    delta = (
        coords
        - point[
            None,
            :
        ]
    )

    distance = np.linalg.norm(
        delta,
        axis=1,
    )

    if float(
        np.min(
            distance
        )
    ) <= 0.0:
        raise RuntimeError(
            "Payload point collided with source cell"
        )

    projection = (
        delta
        @ direction
    )

    kernel = (
        projection
        / (
            distance
            ** 3
        )
    )

    if mu > 0.0:
        kernel *= yukawa_factor(
            distance,
            mu,
        )

    contribution = (
        source
        * kernel
        * field[
            "_volume"
        ]
    )

    net = float(
        np.sum(
            contribution
        )
    )

    gross_out = float(
        np.sum(
            contribution[
                contribution
                > 0.0
            ]
        )
    )

    gross_in = float(
        -np.sum(
            contribution[
                contribution
                < 0.0
            ]
        )
    )

    cancellation = (
        (
            gross_out
            + gross_in
        )
        / abs(
            net
        )
        if abs(
            net
        )
        > 1.0e-300
        else math.inf
    )

    return {
        "net":
            net,

        "gross_out":
            gross_out,

        "gross_in":
            gross_in,

        "cancellation":
            cancellation,
    }


def center_scan(
    field: dict[str, Any],
) -> list[dict[str, Any]]:
    """N73 selection scan using predetermined orientations only."""

    rows = []

    energy = float(
        field[
            "energy"
        ]
    )

    support_radius = float(
        field[
            "support_radius"
        ]
    )

    for direction_name, direction in DIRECTIONS:

        for factor in STANDOFF_FACTORS:

            d = (
                factor
                * support_radius
            )

            payload_radius = (
                PAYLOAD_RADIUS_RATIO
                * d
            )

            near_radius = (
                d
                - payload_radius
            )

            tail_fraction = float(
                np.sum(
                    field[
                        "_rho"
                    ][
                        field[
                            "_radii"
                        ]
                        > near_radius
                    ]
                )
                * field[
                    "_volume"
                ]
                / energy
            )

            center = (
                direction
                * d
            )

            gr = force_driver(
                field,
                center,
                direction,
                "_sgr",
                0.0,
            )

            delta = (
                field[
                    "_coords"
                ]
                - center[
                    None,
                    :
                ]
            )

            distance = np.linalg.norm(
                delta,
                axis=1,
            )

            projection = (
                delta
                @ direction
            )

            base_kernel = (
                projection
                / (
                    distance
                    ** 3
                )
            )

            for mu_h in MU_H_VALUES:

                mu = (
                    mu_h
                    / d
                )

                contribution = (
                    field[
                        "_sfp"
                    ]
                    * base_kernel
                    * yukawa_factor(
                        distance,
                        mu,
                    )
                    * field[
                        "_volume"
                    ]
                )

                fp_net = float(
                    np.sum(
                        contribution
                    )
                )

                gross_out = float(
                    np.sum(
                        contribution[
                            contribution
                            > 0.0
                        ]
                    )
                )

                gross_in = float(
                    -np.sum(
                        contribution[
                            contribution
                            < 0.0
                        ]
                    )
                )

                cancellation = (
                    (
                        gross_out
                        + gross_in
                    )
                    / abs(
                        fp_net
                    )
                    if abs(
                        fp_net
                    )
                    > 1.0e-300
                    else math.inf
                )

                c_fp_center = (
                    1.5
                    * energy
                    / (
                        fp_net
                        * d
                        * d
                    )
                    if fp_net
                    > 0.0
                    else math.inf
                )

                rows.append(
                    {
                        "N":
                            field[
                                "n"
                            ],

                        "direction":
                            direction_name,

                        "direction_x":
                            float(
                                direction[
                                    0
                                ]
                            ),

                        "direction_y":
                            float(
                                direction[
                                    1
                                ]
                            ),

                        "direction_z":
                            float(
                                direction[
                                    2
                                ]
                            ),

                        "standoff_factor":
                            factor,

                        "d":
                            d,

                        "payload_radius":
                            payload_radius,

                        "mu_h":
                            mu_h,

                        "fp_center":
                            fp_net,

                        "gr_center":
                            gr[
                                "net"
                            ],

                        "fp_cancellation":
                            cancellation,

                        "C_FP_center_alpha1":
                            c_fp_center,

                        "tail_energy_fraction":
                            tail_fraction,

                        "_direction":
                            direction.copy(),
                    }
                )

    return rows


def perpendicular_basis(
    direction: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Stable orthonormal transverse basis."""

    axis = np.eye(
        3
    )[
        int(
            np.argmin(
                np.abs(
                    direction
                )
            )
        )
    ]

    e1 = np.cross(
        direction,
        axis,
    )

    e1 /= np.linalg.norm(
        e1
    )

    e2 = np.cross(
        direction,
        e1,
    )

    e2 /= np.linalg.norm(
        e2
    )

    return e1, e2


def payload_audit(
    field: dict[str, Any],
    direction: np.ndarray,
    factor: float,
    mu_h: float,
) -> dict[str, Any]:
    """Seven-point external finite-payload audit."""

    d = (
        factor
        * float(
            field[
                "support_radius"
            ]
        )
    )

    radius = (
        PAYLOAD_RADIUS_RATIO
        * d
    )

    center = (
        direction
        * d
    )

    e1, e2 = perpendicular_basis(
        direction
    )

    points = [
        (
            "CENTER",
            center,
        ),
        (
            "NEAR_AXIAL",
            center
            - radius
            * direction,
        ),
        (
            "FAR_AXIAL",
            center
            + radius
            * direction,
        ),
        (
            "TRANSVERSE_1_PLUS",
            center
            + radius
            * e1,
        ),
        (
            "TRANSVERSE_1_MINUS",
            center
            - radius
            * e1,
        ),
        (
            "TRANSVERSE_2_PLUS",
            center
            + radius
            * e2,
        ),
        (
            "TRANSVERSE_2_MINUS",
            center
            - radius
            * e2,
        ),
    ]

    mu = (
        mu_h
        / d
    )

    samples = []

    for label, point in points:

        fp = force_driver(
            field,
            point,
            direction,
            "_sfp",
            mu,
        )

        gr = force_driver(
            field,
            point,
            direction,
            "_sgr",
            0.0,
        )

        samples.append(
            {
                "label":
                    label,

                "fp":
                    fp[
                        "net"
                    ],

                "gr":
                    gr[
                        "net"
                    ],

                "fp_cancellation":
                    fp[
                        "cancellation"
                    ],
            }
        )

    min_fp = min(
        row[
            "fp"
        ]
        for row in samples
    )

    max_cancellation = max(
        row[
            "fp_cancellation"
        ]
        for row in samples
    )

    near_radius = (
        d
        - radius
    )

    tail_fraction = float(
        np.sum(
            field[
                "_rho"
            ][
                field[
                    "_radii"
                ]
                > near_radius
            ]
        )
        * field[
            "_volume"
        ]
        / field[
            "energy"
        ]
    )

    c_robust = (
        1.5
        * field[
            "energy"
        ]
        / (
            min_fp
            * d
            * d
        )
        if min_fp
        > 0.0
        else math.inf
    )

    return {
        "N":
            field[
                "n"
            ],

        "d":
            d,

        "payload_radius":
            radius,

        "mu_h":
            mu_h,

        "all_fp_outward":
            all(
                row[
                    "fp"
                ]
                > 0.0
                for row in samples
            ),

        "min_fp":
            min_fp,

        "max_fp_cancellation":
            max_cancellation,

        "C_FP_robust_alpha1":
            c_robust,

        "tail_energy_fraction":
            tail_fraction,

        "samples":
            samples,
    }


def select_n73_candidate(
    field73: dict[str, Any],
    rows: list[dict[str, Any]],
) -> dict[str, Any] | None:
    """Train on N73 only; N81 remains an independent validation field."""

    ranked = sorted(
        (
            row
            for row in rows
            if (
                row[
                    "fp_center"
                ]
                > 0.0
                and row[
                    "tail_energy_fraction"
                ]
                <= TAIL_MAX
                and math.isfinite(
                    row[
                        "C_FP_center_alpha1"
                    ]
                )
            )
        ),
        key=lambda row: (
            row[
                "C_FP_center_alpha1"
            ],
            row[
                "fp_cancellation"
            ],
        ),
    )

    for row in ranked[
        :16
    ]:

        audit = payload_audit(
            field73,
            row[
                "_direction"
            ],
            float(
                row[
                    "standoff_factor"
                ]
            ),
            float(
                row[
                    "mu_h"
                ]
            ),
        )

        if (
            audit[
                "all_fp_outward"
            ]
            and audit[
                "tail_energy_fraction"
            ]
            <= TAIL_MAX
        ):
            return {
                **row,
                "payload":
                    audit,
            }

    return None


def validate_on_n81(
    field81: dict[str, Any],
    candidate73: dict[str, Any],
) -> dict[str, Any]:
    """Blind companion-resolution validation of the selected N73 geometry."""

    direction = np.array(
        [
            candidate73[
                "direction_x"
            ],
            candidate73[
                "direction_y"
            ],
            candidate73[
                "direction_z"
            ],
        ],
        dtype=float,
    )

    audit81 = payload_audit(
        field81,
        direction,
        float(
            candidate73[
                "standoff_factor"
            ]
        ),
        float(
            candidate73[
                "mu_h"
            ]
        ),
    )

    c73 = float(
        candidate73[
            "payload"
        ][
            "C_FP_robust_alpha1"
        ]
    )

    c81 = float(
        audit81[
            "C_FP_robust_alpha1"
        ]
    )

    c_relchange = (
        abs(
            c81
            - c73
        )
        / max(
            abs(
                c81
            ),
            abs(
                c73
            ),
            1.0e-300,
        )
        if (
            math.isfinite(
                c73
            )
            and math.isfinite(
                c81
            )
        )
        else math.inf
    )

    max_cancel = max(
        float(
            candidate73[
                "payload"
            ][
                "max_fp_cancellation"
            ]
        ),
        float(
            audit81[
                "max_fp_cancellation"
            ]
        ),
    )

    strong = bool(
        candidate73[
            "payload"
        ][
            "all_fp_outward"
        ]
        and audit81[
            "all_fp_outward"
        ]
        and c_relchange
        <= MAX_B7_C_RELCHANGE
        and max_cancel
        <= MAX_B7_CANCELLATION
        and field81[
            "virial_green"
        ]
        and audit81[
            "tail_energy_fraction"
        ]
        <= TAIL_MAX
    )

    sign_survives = bool(
        candidate73[
            "payload"
        ][
            "all_fp_outward"
        ]
        and audit81[
            "all_fp_outward"
        ]
    )

    return {
        "N73_C_FP":
            c73,

        "N81_C_FP":
            c81,

        "C_relative_change":
            c_relchange,

        "max_cancellation":
            max_cancel,

        "sign_survives_N73_N81":
            sign_survives,

        "strong_resolution_gate":
            strong,

        "N81_payload":
            audit81,
    }


def gl_nodes(
    a: float,
    b: float,
    order: int = 4,
) -> tuple[np.ndarray, np.ndarray]:
    """Gauss-Legendre interval rule."""

    x, w = leggauss(
        order
    )

    return (
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
        * x,

        0.5
        * (
            b
            - a
        )
        * w,
    )


def annular_kernel(
    r0: float,
    r1: float,
    z0: float,
    z1: float,
    target_z: float,
    mu: float,
) -> float:
    """Exact quadrature of the axial Yukawa force kernel over one cell."""

    rr, wr = gl_nodes(
        r0,
        r1,
    )

    zz, wz = gl_nodes(
        z0,
        z1,
    )

    R, Z = np.meshgrid(
        rr,
        zz,
        indexing="ij",
    )

    WR, WZ = np.meshgrid(
        wr,
        wz,
        indexing="ij",
    )

    dz = (
        Z
        - target_z
    )

    distance = np.sqrt(
        R * R
        + dz * dz
    )

    integrand = (
        2.0
        * math.pi
        * R
        * dz
        / (
            distance
            ** 3
        )
    )

    if mu > 0.0:
        integrand *= yukawa_factor(
            distance,
            mu,
        )

    return float(
        np.sum(
            WR
            * WZ
            * integrand
        )
    )


def soc_dec(
    constraints: list[cp.Constraint],
    energy,
    pr,
    pz,
    trz,
    pphi,
) -> None:
    """Exact type-I DEC for the axisymmetric 3x3 spatial stress tensor."""

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

    radius = cp.norm(
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
            radius
            <= energy
            - mean,

            radius
            <= energy
            + mean,

            pphi
            <= energy,

            -pphi
            <= energy,
        ]
    )


def solve_relaxed_fp(
    nr: int,
    nz: int,
    rmax: float,
    depth: float,
    mu_h: float,
) -> dict[str, Any]:
    """Independent conserved-DEC Fierz-Pauli true-stand-off optimizer."""

    r_edges = np.linspace(
        0.0,
        rmax,
        nr + 1,
    )

    z_edges = np.linspace(
        -depth,
        0.0,
        nz + 1,
    )

    volumes = np.zeros(
        (
            nr,
            nz,
        ),
        dtype=float,
    )

    targets = (
        0.90,
        1.00,
        1.10,
    )

    fp_kernel = {
        target:
            np.zeros(
                (
                    nr,
                    nz,
                ),
                dtype=float,
            )
        for target in targets
    }

    gr_kernel = np.zeros(
        (
            nr,
            nz,
        ),
        dtype=float,
    )

    for i in range(
        nr
    ):
        for j in range(
            nz
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
                math.pi
                * (
                    r1 * r1
                    - r0 * r0
                )
                * (
                    z1
                    - z0
                )
            )

            for target in targets:

                fp_kernel[
                    target
                ][
                    i,
                    j
                ] = annular_kernel(
                    r0,
                    r1,
                    z0,
                    z1,
                    target,
                    mu_h,
                )

            gr_kernel[
                i,
                j
            ] = annular_kernel(
                r0,
                r1,
                z0,
                z1,
                1.0,
                0.0,
            )

    e = cp.Variable(
        (
            nr,
            nz,
        ),
        nonneg=True,
    )

    pphi = cp.Variable(
        (
            nr,
            nz,
        )
    )

    prf = cp.Variable(
        (
            nr + 1,
            nz,
        )
    )

    pzf = cp.Variable(
        (
            nr,
            nz + 1,
        )
    )

    trzv = cp.Variable(
        (
            nr + 1,
            nz + 1,
        )
    )

    constraints: list[
        cp.Constraint
    ] = [
        prf[
            nr,
            :
        ]
        == 0.0,

        pzf[
            :,
            0
        ]
        == 0.0,

        pzf[
            :,
            nz
        ]
        == 0.0,

        trzv[
            0,
            :
        ]
        == 0.0,

        trzv[
            nr,
            :
        ]
        == 0.0,

        trzv[
            :,
            0
        ]
        == 0.0,

        trzv[
            :,
            nz
        ]
        == 0.0,
    ]

    pr_cells = []
    pz_cells = []
    trz_cells = []

    for i in range(
        nr
    ):

        row_pr = []
        row_pz = []
        row_trz = []

        for j in range(
            nz
        ):

            pr = (
                0.5
                * (
                    prf[
                        i,
                        j
                    ]
                    + prf[
                        i + 1,
                        j
                    ]
                )
            )

            pz = (
                0.5
                * (
                    pzf[
                        i,
                        j
                    ]
                    + pzf[
                        i,
                        j + 1
                    ]
                )
            )

            trz = (
                0.25
                * (
                    trzv[
                        i,
                        j
                    ]
                    + trzv[
                        i + 1,
                        j
                    ]
                    + trzv[
                        i,
                        j + 1
                    ]
                    + trzv[
                        i + 1,
                        j + 1
                    ]
                )
            )

            row_pr.append(
                pr
            )

            row_pz.append(
                pz
            )

            row_trz.append(
                trz
            )

            soc_dec(
                constraints,
                e[
                    i,
                    j
                ],
                pr,
                pz,
                trz,
                pphi[
                    i,
                    j
                ],
            )

        pr_cells.append(
            row_pr
        )

        pz_cells.append(
            row_pz
        )

        trz_cells.append(
            row_trz
        )

    for j in range(
        nz
    ):
        constraints.append(
            prf[
                0,
                j
            ]
            ==
            pphi[
                0,
                j
            ]
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

        dr = (
            r1
            - r0
        )

        arf = (
            0.5
            * (
                r1 * r1
                - r0 * r0
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

            dz = (
                z1
                - z0
            )

            trz_s = (
                0.5
                * (
                    trzv[
                        i,
                        j
                    ]
                    + trzv[
                        i + 1,
                        j
                    ]
                )
            )

            trz_n = (
                0.5
                * (
                    trzv[
                        i,
                        j + 1
                    ]
                    + trzv[
                        i + 1,
                        j + 1
                    ]
                )
            )

            trz_w = (
                0.5
                * (
                    trzv[
                        i,
                        j
                    ]
                    + trzv[
                        i,
                        j + 1
                    ]
                )
            )

            trz_e = (
                0.5
                * (
                    trzv[
                        i + 1,
                        j
                    ]
                    + trzv[
                        i + 1,
                        j + 1
                    ]
                )
            )

            radial = (
                dz
                * (
                    r1
                    * prf[
                        i + 1,
                        j
                    ]
                    - r0
                    * prf[
                        i,
                        j
                    ]
                )
                + arf
                * (
                    trz_n
                    - trz_s
                )
                - dr
                * dz
                * pphi[
                    i,
                    j
                ]
            )

            vertical = (
                2.0
                * dz
                * (
                    r1
                    * trz_e
                    - r0
                    * trz_w
                )
                + (
                    r1 * r1
                    - r0 * r0
                )
                * (
                    pzf[
                        i,
                        j + 1
                    ]
                    - pzf[
                        i,
                        j
                    ]
                )
            )

            constraints.extend(
                [
                    radial
                    == 0.0,

                    vertical
                    == 0.0,
                ]
            )

    prc = cp.vstack(
        [
            cp.hstack(
                row
            )
            for row in pr_cells
        ]
    )

    pzc = cp.vstack(
        [
            cp.hstack(
                row
            )
            for row in pz_cells
        ]
    )

    trzc = cp.vstack(
        [
            cp.hstack(
                row
            )
            for row in trz_cells
        ]
    )

    V = cp.Constant(
        volumes
    )

    constraints.extend(
        [
            cp.sum(
                cp.multiply(
                    V,
                    prc
                    + pphi,
                )
            )
            == 0.0,

            cp.sum(
                cp.multiply(
                    V,
                    pzc,
                )
            )
            == 0.0,
        ]
    )

    sfp = (
        2.0
        * e
        + prc
        + pzc
        + pphi
    )

    sgr = (
        e
        + prc
        + pzc
        + pphi
    )

    fp_accel = {}

    for target in targets:

        fp_accel[
            target
        ] = cp.sum(
            cp.multiply(
                cp.Constant(
                    fp_kernel[
                        target
                    ]
                ),
                sfp,
            )
        )

        constraints.append(
            fp_accel[
                target
            ]
            >= 1.0
        )

    energy_expr = cp.sum(
        cp.multiply(
            V,
            e,
        )
    )

    problem = cp.Problem(
        cp.Minimize(
            energy_expr
        ),
        constraints,
    )

    installed = cp.installed_solvers()

    solver = (
        "CLARABEL"
        if "CLARABEL" in installed
        else "SCS"
    )

    if solver == "CLARABEL":
        problem.solve(
            solver=solver,
            verbose=False,
        )
    else:
        problem.solve(
            solver=solver,
            verbose=False,
            eps=1.0e-5,
            max_iters=200000,
        )

    status = str(
        problem.status
    )

    if status not in {
        "optimal",
        "optimal_inaccurate",
    }:
        return {
            "feasible":
                False,

            "status":
                status,

            "solver":
                solver,

            "nr":
                nr,

            "nz":
                nz,

            "rmax":
                rmax,

            "depth":
                depth,

            "mu_h":
                mu_h,
        }

    ea = np.asarray(
        e.value,
        dtype=float,
    )

    ppa = np.asarray(
        pphi.value,
        dtype=float,
    )

    prfa = np.asarray(
        prf.value,
        dtype=float,
    )

    pzfa = np.asarray(
        pzf.value,
        dtype=float,
    )

    trzva = np.asarray(
        trzv.value,
        dtype=float,
    )

    pra = (
        0.5
        * (
            prfa[:-1]
            + prfa[1:]
        )
    )

    pza = (
        0.5
        * (
            pzfa[:, :-1]
            + pzfa[:, 1:]
        )
    )

    trza = (
        0.25
        * (
            trzva[:-1, :-1]
            + trzva[1:, :-1]
            + trzva[:-1, 1:]
            + trzva[1:, 1:]
        )
    )

    sfpa = (
        2.0
        * ea
        + pra
        + pza
        + ppa
    )

    sgra = (
        ea
        + pra
        + pza
        + ppa
    )

    energy = float(
        np.sum(
            volumes
            * ea
        )
    )

    fp_values = [
        float(
            np.sum(
                fp_kernel[
                    target
                ]
                * sfpa
            )
        )
        for target in targets
    ]

    gr_center = float(
        np.sum(
            gr_kernel
            * sgra
        )
    )

    min_fp = min(
        fp_values
    )

    c_fp = (
        1.5
        * energy
        / min_fp
    )

    dec_violation = 0.0

    for index in np.ndindex(
        ea.shape
    ):

        i, j = index

        matrix = np.array(
            [
                [
                    pra[
                        i,
                        j
                    ],
                    trza[
                        i,
                        j
                    ],
                    0.0,
                ],
                [
                    trza[
                        i,
                        j
                    ],
                    pza[
                        i,
                        j
                    ],
                    0.0,
                ],
                [
                    0.0,
                    0.0,
                    ppa[
                        i,
                        j
                    ],
                ],
            ]
        )

        eig = np.linalg.eigvalsh(
            matrix
        )

        dec_violation = max(
            dec_violation,
            float(
                np.max(
                    np.abs(
                        eig
                    )
                )
                - ea[
                    i,
                    j
                ]
            ),
        )

    laue1 = float(
        np.sum(
            volumes
            * (
                pra
                + ppa
            )
        )
    )

    laue2 = float(
        np.sum(
            volumes
            * pza
        )
    )

    laue_rel = max(
        abs(
            laue1
        ),
        abs(
            laue2
        ),
    ) / max(
        energy,
        1.0e-300,
    )

    fp_total = float(
        np.sum(
            volumes
            * sfpa
        )
    )

    negative_participation = float(
        np.sum(
            volumes[
                sfpa
                < 0.0
            ]
            * ea[
                sfpa
                < 0.0
            ]
        )
        / energy
    )

    numerical_green = bool(
        dec_violation
        <= DEC_TOL
        and laue_rel
        <= LAUE_TOL
        and min_fp
        >= 1.0
        - 5.0e-5
    )

    return {
        "feasible":
            True,

        "status":
            status,

        "solver":
            solver,

        "nr":
            nr,

        "nz":
            nz,

        "rmax":
            rmax,

        "depth":
            depth,

        "mu_h":
            mu_h,

        "energy":
            energy,

        "fp_near":
            fp_values[
                0
            ],

        "fp_center":
            fp_values[
                1
            ],

        "fp_far":
            fp_values[
                2
            ],

        "fp_min":
            min_fp,

        "gr_center":
            gr_center,

        "C_FP_alpha1":
            c_fp,

        "DEC_violation":
            dec_violation,

        "Laue_relative_residual":
            laue_rel,

        "FP_total_over_E":
            fp_total
            / energy,

        "negative_FP_energy_participation":
            negative_participation,

        "numerical_green":
            numerical_green,

        "_e":
            ea,

        "_sfp":
            sfpa,

        "_sgr":
            sgra,

        "_volumes":
            volumes,

        "_fp_values":
            fp_values,
    }


def relaxed_campaign() -> dict[str, Any]:
    """Low-grid tournament followed by one independent refinement."""

    rows = []

    for nr, nz, rmax, depth in RELAXED_GEOMETRIES:

        for mu_h in RELAXED_MU:

            print(
                (
                    "029A_RELAXED_BEGIN "
                    f"GRID={nr}x{nz} "
                    f"RMAX={rmax} "
                    f"DEPTH={depth} "
                    f"MU_H={mu_h}"
                ),
                flush=True,
            )

            row = solve_relaxed_fp(
                nr,
                nz,
                rmax,
                depth,
                mu_h,
            )

            rows.append(
                row
            )

            print(
                (
                    "029A_RELAXED_RESULT "
                    f"FEASIBLE={row.get('feasible')} "
                    f"C={row.get('C_FP_alpha1')} "
                    f"GREEN={row.get('numerical_green')}"
                ),
                flush=True,
            )

    valid = [
        row
        for row in rows
        if (
            row.get(
                "feasible",
                False,
            )
            and row.get(
                "numerical_green",
                False,
            )
            and math.isfinite(
                float(
                    row[
                        "C_FP_alpha1"
                    ]
                )
            )
        )
    ]

    if not valid:
        return {
            "rows":
                rows,

            "coarse_best":
                None,

            "refined":
                None,

            "converged":
                False,
        }

    coarse = min(
        valid,
        key=lambda row: row[
            "C_FP_alpha1"
        ],
    )

    if SMOKE:
        return {
            "rows":
                rows,

            "coarse_best":
                coarse,

            "refined":
                None,

            "converged":
                False,
        }

    refined = solve_relaxed_fp(
        14,
        20,
        float(
            coarse[
                "rmax"
            ]
        ),
        float(
            coarse[
                "depth"
            ]
        ),
        float(
            coarse[
                "mu_h"
            ]
        ),
    )

    relchange = (
        abs(
            refined[
                "C_FP_alpha1"
            ]
            - coarse[
                "C_FP_alpha1"
            ]
        )
        / max(
            abs(
                refined[
                    "C_FP_alpha1"
                ]
            ),
            abs(
                coarse[
                    "C_FP_alpha1"
                ]
            ),
            1.0e-300,
        )
        if (
            refined.get(
                "feasible",
                False,
            )
            and refined.get(
                "numerical_green",
                False,
            )
        )
        else math.inf
    )

    converged = bool(
        refined.get(
            "feasible",
            False,
        )
        and refined.get(
            "numerical_green",
            False,
        )
        and relchange
        <= 0.25
    )

    return {
        "rows":
            rows,

        "coarse_best":
            coarse,

        "refined":
            refined,

        "C_relative_change":
            relchange,

        "converged":
            converged,
    }


def required_yukawa_x(
    ratio: float,
) -> float:
    """Solve (1+x) exp(-x) <= 1/ratio."""

    if ratio <= 1.0:
        return 0.0

    target = (
        1.0
        / ratio
    )

    low = 0.0
    high = 1.0

    def f(x: float) -> float:
        return (
            (
                1.0
                + x
            )
            * math.exp(
                -x
            )
        )

    while f(
        high
    ) > target:
        high *= 2.0

        if high > 1.0e6:
            raise RuntimeError(
                "Yukawa attenuation solve failed"
            )

    for _ in range(
        100
    ):

        mid = (
            0.5
            * (
                low
                + high
            )
        )

        if f(
            mid
        ) > target:
            low = mid
        else:
            high = mid

    return high


def wall_lower_bound(
    h_m: float,
    m_in_eV: float,
    m_out_eV: float,
    wall_fraction: float,
) -> float:
    """Favorable canonical scalar mass-control gradient lower bound."""

    ell_m = (
        wall_fraction
        * h_m
    )

    radius_m = h_m

    coupling = (
        4.0
        * math.pi
    )

    delta_chi_eV = (
        max(
            0.0,
            m_out_eV
            - m_in_eV,
        )
        / coupling
    )

    radius_evinv = (
        radius_m
        / HBARC_EV_M
    )

    ell_evinv = (
        ell_m
        / HBARC_EV_M
    )

    energy_eV = (
        0.5
        * 4.0
        * math.pi
        * radius_evinv
        ** 2
        / ell_evinv
        * delta_chi_eV
        ** 2
    )

    return (
        energy_eV
        * EV_J
    )


def portal_from_b7(
    field: dict[str, Any],
    candidate73: dict[str, Any],
    validation: dict[str, Any],
) -> list[dict[str, Any]]:
    """Practicality preflight using the N81 actual-field validation data."""

    if not validation[
        "sign_survives_N73_N81"
    ]:
        return []

    direction = np.array(
        [
            candidate73[
                "direction_x"
            ],
            candidate73[
                "direction_y"
            ],
            candidate73[
                "direction_z"
            ],
        ],
        dtype=float,
    )

    factor = float(
        candidate73[
            "standoff_factor"
        ]
    )

    mu_h = float(
        candidate73[
            "mu_h"
        ]
    )

    audit = payload_audit(
        field,
        direction,
        factor,
        mu_h,
    )

    d_num = float(
        audit[
            "d"
        ]
    )

    rows = []

    for target_name, acceleration, h_m, budget in TARGETS:

        source_budget = (
            SOURCE_BUDGET_FRACTION
            * budget
        )

        control_budget = (
            CONTROL_BUDGET_FRACTION
            * budget
        )

        required_driver = (
            field[
                "energy"
            ]
            * acceleration
            * C_LIGHT
            ** 2
            * h_m
            ** 2
            / (
                G_NEWTON
                * source_budget
                * d_num
                ** 2
            )
        )

        alpha2_required = 0.0
        impossible = False

        sample_requirements = []

        for sample in audit[
            "samples"
        ]:

            afp = float(
                sample[
                    "fp"
                ]
            )

            agr = float(
                sample[
                    "gr"
                ]
            )

            if afp <= 0.0:
                impossible = True
                alpha2 = math.inf

            else:
                alpha2 = max(
                    0.0,
                    1.5
                    * (
                        required_driver
                        - agr
                    )
                    / afp,
                )

            alpha2_required = max(
                alpha2_required,
                alpha2,
            )

            sample_requirements.append(
                {
                    "label":
                        sample[
                            "label"
                        ],

                    "alpha2_required":
                        alpha2,
                }
            )

        if impossible or not math.isfinite(
            alpha2_required
        ):

            rows.append(
                {
                    "target":
                        target_name,

                    "possible":
                        False,

                    "reason":
                        "NONPOSITIVE_FP_PAYLOAD_SAMPLE",
                }
            )

            continue

        alpha = math.sqrt(
            alpha2_required
        )

        alpha_y = (
            4.0
            / 3.0
            * alpha2_required
        )

        m_in_eV = (
            mu_h
            * HBARC_EV_M
            / h_m
        )

        probe_eV = (
            HBARC_EV_M
            / h_m
        )

        lambda3_max_eV = (
            m_in_eV
            ** 2
            * MPL_REDUCED_EV
        ) ** (
            1.0
            / 3.0
        )

        effective_planck = (
            MPL_REDUCED_EV
            / max(
                alpha,
                1.0,
            )
        )

        lambda3_coupling_eV = (
            m_in_eV
            ** 2
            * effective_planck
        ) ** (
            1.0
            / 3.0
        )

        lambda3_margin = (
            lambda3_coupling_eV
            / probe_eV
        )

        matter_coupling_scale_eV = (
            MPL_REDUCED_EV
            / max(
                alpha,
                1.0e-300,
            )
        )

        source_schwarzschild_radius = (
            2.0
            * G_NEWTON
            * source_budget
            / (
                C_LIGHT
                ** 4
            )
        )

        m_inverse_m = (
            mu_h
            / h_m
        )

        vainshtein_radius = (
            (
                max(
                    alpha,
                    1.0
                )
                * source_schwarzschild_radius
                / (
                    m_inverse_m
                    ** 2
                )
            )
            ** (
                1.0
                / 3.0
            )
            if m_inverse_m
            > 0.0
            else math.inf
        )

        vainshtein_ratio = (
            vainshtein_radius
            / h_m
        )

        wall_rows = []

        for wall_fraction in (
            0.10,
            0.25,
            0.50,
        ):

            attenuation_ratio = max(
                1.0,
                alpha_y
                / ALPHA_Y_OUT_MAX,
            )

            x_required = required_yukawa_x(
                attenuation_ratio
            )

            ell_m = (
                wall_fraction
                * h_m
            )

            m_out_eV = (
                x_required
                * HBARC_EV_M
                / ell_m
            )

            m_out_eV = max(
                m_out_eV,
                m_in_eV,
            )

            wall_j = wall_lower_bound(
                h_m,
                m_in_eV,
                m_out_eV,
                wall_fraction,
            )

            range_out_m = (
                HBARC_EV_M
                / m_out_eV
                if m_out_eV
                > 0.0
                else math.inf
            )

            wall_rows.append(
                {
                    "wall_fraction":
                        wall_fraction,

                    "attenuation_x":
                        x_required,

                    "m_out_eV":
                        m_out_eV,

                    "mass_ratio_out_in":
                        (
                            m_out_eV
                            / m_in_eV
                            if m_in_eV
                            > 0.0
                            else math.inf
                        ),

                    "exterior_range_m":
                        range_out_m,

                    "canonical_wall_lower_bound_J":
                        wall_j,

                    "wall_budget_ratio":
                        wall_j
                        / control_budget,
                }
            )

        primary_wall = next(
            row
            for row in wall_rows
            if abs(
                row[
                    "wall_fraction"
                ]
                - PRIMARY_WALL_FRACTION
            )
            < 1.0e-12
        )

        portal_health = bool(
            lambda3_margin
            >= PRIMARY_LAMBDA3_MARGIN
            and vainshtein_ratio
            < PRIMARY_VAINSHtein_RATIO
            and primary_wall[
                "canonical_wall_lower_bound_J"
            ]
            <= control_budget
        )

        rows.append(
            {
                "target":
                    target_name,

                "possible":
                    True,

                "acceleration_m_s2":
                    acceleration,

                "h_m":
                    h_m,

                "budget_J":
                    budget,

                "source_budget_J":
                    source_budget,

                "control_budget_J":
                    control_budget,

                "required_dimensionless_driver":
                    required_driver,

                "alpha2_required":
                    alpha2_required,

                "alpha_required":
                    alpha,

                "alpha_Y_equivalent":
                    alpha_y,

                "mu_h":
                    mu_h,

                "m_in_eV":
                    m_in_eV,

                "probe_eV":
                    probe_eV,

                "Lambda3_max_eV":
                    lambda3_max_eV,

                "Lambda3_coupling_aware_eV":
                    lambda3_coupling_eV,

                "Lambda3_coupling_aware_margin":
                    lambda3_margin,

                "matter_coupling_scale_eV":
                    matter_coupling_scale_eV,

                "Vainshtein_radius_m":
                    vainshtein_radius,

                "Vainshtein_over_h":
                    vainshtein_ratio,

                "wall_cases":
                    wall_rows,

                "primary_wall":
                    primary_wall,

                "portal_health_preflight":
                    portal_health,

                "sample_requirements":
                    sample_requirements,
            }
        )

    return rows


print(
    "=== 029A LINEAGE ===",
    flush=True,
)

print(
    "028C_DECISION="
    + str(
        J028C.get(
            "decision"
        )
    ),
    flush=True,
)

print(
    "006D_FP_POINTWISE_REPULSION_POSSIBLE=NO",
    flush=True,
)

print(
    (
        "006D_FP_ANALYTIC_REASON="
        "2RHO_PLUS_PR_PLUS_PPHI_GE_ZERO_FROM_PZ_ZERO_AND_DEC"
    ),
    flush=True,
)

print(
    "FP_LOCAL_DEC_MIN_SOURCE_RATIO=-1",
    flush=True,
)

print(
    "FP_STATIC_LAUE_TOTAL_SOURCE_RATIO=2",
    flush=True,
)


print(
    "\n=== 029A B7 FIELD RECONSTRUCTION ===",
    flush=True,
)

field73 = reconstruct_b7(
    73
)

field81 = reconstruct_b7(
    81
)

for field in (
    field73,
    field81,
):

    print(
        (
            f"N{field['n']}_ENERGY={field['energy']:.15e} "
            f"SGR_OVER_E={field['virial_gr_ratio']:.15e} "
            f"SFP_OVER_E={field['virial_fp_ratio']:.15e} "
            f"NEG_FP_ENERGY_FRAC={field['negative_fp_energy_fraction']:.15e} "
            f"R999999={field['support_radius']:.15e} "
            f"VIRIAL_GREEN={field['virial_green']}"
        ),
        flush=True,
    )


print(
    "\n=== 029A N73 B7 FP STANDOFF SELECTION ===",
    flush=True,
)

b7_scan = center_scan(
    field73
)

candidate73 = select_n73_candidate(
    field73,
    b7_scan,
)

if candidate73 is None:

    print(
        "B7_N73_FP_EXTERNAL_CANDIDATE=NONE",
        flush=True,
    )

    validation = None

else:

    print(
        (
            "B7_N73_FP_EXTERNAL_CANDIDATE=FOUND "
            f"DIRECTION={candidate73['direction']} "
            f"FACTOR={candidate73['standoff_factor']} "
            f"MU_H={candidate73['mu_h']} "
            f"C_FP={candidate73['payload']['C_FP_robust_alpha1']:.15e} "
            f"CANCEL={candidate73['payload']['max_fp_cancellation']:.15e}"
        ),
        flush=True,
    )

    validation = validate_on_n81(
        field81,
        candidate73,
    )

    print(
        (
            "B7_N81_VALIDATION "
            f"SIGN={validation['sign_survives_N73_N81']} "
            f"STRONG={validation['strong_resolution_gate']} "
            f"C73={validation['N73_C_FP']:.15e} "
            f"C81={validation['N81_C_FP']:.15e} "
            f"RELCHANGE={validation['C_relative_change']:.15e} "
            f"CANCEL={validation['max_cancellation']:.15e}"
        ),
        flush=True,
    )


print(
    "\n=== 029A INDEPENDENT RELAXED FP-DEC SOURCE SEARCH ===",
    flush=True,
)

relaxed = relaxed_campaign()

relaxed_best = (
    relaxed.get(
        "refined"
    )
    if relaxed.get(
        "converged"
    )
    else relaxed.get(
        "coarse_best"
    )
)

if relaxed_best is None:

    print(
        "RELAXED_FP_DEC_SOURCE=NONE",
        flush=True,
    )

else:

    print(
        (
            "RELAXED_FP_DEC_SOURCE "
            f"C={relaxed_best['C_FP_alpha1']:.15e} "
            f"MU_H={relaxed_best['mu_h']:.15e} "
            f"NEG_PART={relaxed_best['negative_FP_energy_participation']:.15e} "
            f"CONVERGED={relaxed.get('converged')}"
        ),
        flush=True,
    )


portal_rows = []

if (
    candidate73 is not None
    and validation is not None
    and validation[
        "sign_survives_N73_N81"
    ]
):

    print(
        "\n=== 029A MASS-GATED SPIN-2 PORTAL SCALING ===",
        flush=True,
    )

    portal_rows = portal_from_b7(
        field81,
        candidate73,
        validation,
    )

    for row in portal_rows:

        if not row.get(
            "possible",
            False,
        ):

            print(
                (
                    "029A_PORTAL "
                    f"TARGET={row['target']} "
                    "POSSIBLE=NO"
                ),
                flush=True,
            )

            continue

        print(
            (
                "029A_PORTAL "
                f"TARGET={row['target']} "
                f"ALPHA={row['alpha_required']:.15e} "
                f"ALPHA_Y={row['alpha_Y_equivalent']:.15e} "
                f"M_IN_EV={row['m_in_eV']:.15e} "
                f"LAMBDA3_MARGIN={row['Lambda3_coupling_aware_margin']:.15e} "
                f"RV_OVER_H={row['Vainshtein_over_h']:.15e} "
                f"M_OUT_EV={row['primary_wall']['m_out_eV']:.15e} "
                f"WALL_J={row['primary_wall']['canonical_wall_lower_bound_J']:.15e} "
                f"HEALTH={row['portal_health_preflight']}"
            ),
            flush=True,
        )


macro = next(
    (
        row
        for row in portal_rows
        if row.get(
            "target"
        )
        == "MACRO_1G_1M_1TJ"
    ),
    None,
)

b7_strong = bool(
    validation is not None
    and validation.get(
        "strong_resolution_gate",
        False,
    )
)

macro_portal_green = bool(
    macro is not None
    and macro.get(
        "possible",
        False,
    )
    and macro.get(
        "portal_health_preflight",
        False,
    )
)

relaxed_green = bool(
    relaxed.get(
        "converged",
        False,
    )
)

route_80 = bool(
    b7_strong
    and macro_portal_green
    and not SMOKE
)


if SMOKE:

    decision = (
        "SMOKE_ONLY"
    )

    next_step = (
        "RUN_FULL_029A"
    )

elif route_80:

    decision = (
        "MAJOR_GREEN_ACTUAL_B7_MASS_GATED_SPIN2_PORTAL_PREFLIGHT"
    )

    next_step = (
        "BUILD_FULL_LOCALIZED_GHOST_FREE_BIMETRIC_MASS_WALL_"
        "WITH_COMPLETE_CONTROL_TMUNU_AND_N89_COMPANION"
    )

elif (
    validation is not None
    and validation.get(
        "sign_survives_N73_N81",
        False,
    )
):

    decision = (
        "YELLOW_ACTUAL_B7_FP_EXTERNAL_SIGN_SURVIVES_"
        "BUT_STRICT_PORTAL_GATE_NOT_COMPLETE"
    )

    next_step = (
        "DIAGNOSE_FP_FORCE_CONVERGENCE_OR_PORTAL_HEALTH_LIMITER"
    )

elif relaxed_green:

    decision = (
        "YELLOW_RELAXED_CONSERVED_DEC_FP_SOURCE_SURVIVES_"
        "BUT_NO_MICROSCOPIC_FIELD"
    )

    next_step = (
        "FIELD_REALIZATION_REQUIRED_BEFORE_SPIN2_PORTAL_PROMOTION"
    )

else:

    decision = (
        "RED_NO_PROMOTION_GRADE_MASS_GATED_SPIN2_ROUTE_IN_029A"
    )

    next_step = (
        "PRESERVE_006D_AND_CLOSE_CURRENT_SIGN_PLUS_LOCAL_GAIN_PROGRAM"
    )


b7_csv_fields = [
    "N",
    "direction",
    "direction_x",
    "direction_y",
    "direction_z",
    "standoff_factor",
    "d",
    "payload_radius",
    "mu_h",
    "fp_center",
    "gr_center",
    "fp_cancellation",
    "C_FP_center_alpha1",
    "tail_energy_fraction",
]

with OUT_B7.open(
    "w",
    newline="",
    encoding="utf-8",
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=b7_csv_fields,
    )

    writer.writeheader()

    for row in b7_scan:

        writer.writerow(
            {
                key:
                    row.get(
                        key
                    )
                for key in b7_csv_fields
            }
        )


relaxed_rows_for_csv = list(
    relaxed[
        "rows"
    ]
)

if relaxed.get(
    "refined"
) is not None:
    relaxed_rows_for_csv.append(
        relaxed[
            "refined"
        ]
    )

relaxed_fields = [
    "feasible",
    "status",
    "solver",
    "nr",
    "nz",
    "rmax",
    "depth",
    "mu_h",
    "energy",
    "fp_near",
    "fp_center",
    "fp_far",
    "fp_min",
    "gr_center",
    "C_FP_alpha1",
    "DEC_violation",
    "Laue_relative_residual",
    "FP_total_over_E",
    "negative_FP_energy_participation",
    "numerical_green",
]

with OUT_RELAXED.open(
    "w",
    newline="",
    encoding="utf-8",
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=relaxed_fields,
    )

    writer.writeheader()

    for row in relaxed_rows_for_csv:

        writer.writerow(
            {
                key:
                    row.get(
                        key
                    )
                for key in relaxed_fields
            }
        )


portal_fields = [
    "target",
    "possible",
    "acceleration_m_s2",
    "h_m",
    "budget_J",
    "source_budget_J",
    "control_budget_J",
    "alpha2_required",
    "alpha_required",
    "alpha_Y_equivalent",
    "mu_h",
    "m_in_eV",
    "Lambda3_max_eV",
    "Lambda3_coupling_aware_eV",
    "Lambda3_coupling_aware_margin",
    "matter_coupling_scale_eV",
    "Vainshtein_radius_m",
    "Vainshtein_over_h",
    "portal_health_preflight",
]

with OUT_PORTAL.open(
    "w",
    newline="",
    encoding="utf-8",
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=portal_fields,
    )

    writer.writeheader()

    for row in portal_rows:

        writer.writerow(
            {
                key:
                    row.get(
                        key
                    )
                for key in portal_fields
            }
        )


summary = {
    "branch":
        "TRUE_ANTIGRAVITY",

    "simulation":
        "029A",

    "lineage_028C":
        J028C.get(
            "decision"
        ),

    "physics": {
        "GR_source":
            "rho + trace(T)",

        "FP_source":
            "2 rho + trace(T)",

        "B7_FP_identity":
            "S_FP = e2 + 3 e4 - V",

        "massive_mode_normalization":
            "a_FP = (2/3) alpha^2 K[S_FP]",

        "006D_direct_FP_amplification":
            False,

        "006D_reason":
            "p_z=0 plus DEC implies 2rho+p_r+p_phi >= 0",
    },

    "B7_fields": {
        "N73":
            jsonable(
                field73
            ),

        "N81":
            jsonable(
                field81
            ),
    },

    "B7_selected_N73":
        jsonable(
            candidate73
        ),

    "B7_N81_validation":
        jsonable(
            validation
        ),

    "relaxed_FP_DEC_source": {
        "coarse_best":
            jsonable(
                relaxed.get(
                    "coarse_best"
                )
            ),

        "refined":
            jsonable(
                relaxed.get(
                    "refined"
                )
            ),

        "C_relative_change":
            jfloat(
                relaxed.get(
                    "C_relative_change"
                )
            ),

        "converged":
            bool(
                relaxed.get(
                    "converged",
                    False,
                )
            ),
    },

    "portal_scaling":
        jsonable(
            portal_rows
        ),

    "decision":
        decision,

    "next":
        next_step,

    "route_level_80_heuristic_authorized":
        route_80,

    "overall_practical_antigravity_device":
        False,

    "overall_practical_antigravity_proven":
        False,

    "mandatory_parallel_credibility_branch":
        "026C_N89_FORCE_CONVERGENCE",

    "claims": {
        "actual_B7_field_used":
            True,

        "N73_N81_FP_standoff_sign_tested":
            True,

        "relaxed_conserved_DEC_FP_source_tested":
            True,

        "full_bimetric_field_equations_solved":
            False,

        "mass_wall_full_Tmunu_included":
            False,

        "published_fifth_force_curve_fully_applied":
            False,

        "nonlinear_portal_stability_proven":
            False,

        "practical_antigravity_device":
            False,
    },
}


OUT_JSON.write_text(
    json.dumps(
        jsonable(
            summary
        ),
        indent=2,
        sort_keys=True,
    ),
    encoding="utf-8",
)


print(
    "\n=== 029A FINAL RESULT ===",
    flush=True,
)

print(
    (
        "B7_FP_NEGATIVE_ENERGY_PARTICIPATION_N73="
        f"{field73['negative_fp_energy_fraction']:.15e}"
    ),
    flush=True,
)

print(
    (
        "B7_FP_NEGATIVE_ENERGY_PARTICIPATION_N81="
        f"{field81['negative_fp_energy_fraction']:.15e}"
    ),
    flush=True,
)

if validation is None:

    print(
        "B7_FP_N73_N81_EXTERNAL_SIGN=NO_VALIDATED_CANDIDATE",
        flush=True,
    )

else:

    print(
        (
            "B7_FP_N73_N81_EXTERNAL_SIGN="
            + (
                "YES"
                if validation[
                    "sign_survives_N73_N81"
                ]
                else "NO"
            )
        ),
        flush=True,
    )

    print(
        (
            "B7_FP_STRONG_RESOLUTION_GATE="
            + (
                "YES"
                if validation[
                    "strong_resolution_gate"
                ]
                else "NO"
            )
        ),
        flush=True,
    )

    print(
        (
            "B7_FP_C_RELCHANGE="
            f"{validation['C_relative_change']:.15e}"
        ),
        flush=True,
    )


print(
    (
        "RELAXED_FP_DEC_SOURCE_CONVERGED="
        + (
            "YES"
            if relaxed.get(
                "converged",
                False,
            )
            else "NO"
        )
    ),
    flush=True,
)

if relaxed_best is not None:

    print(
        (
            "RELAXED_FP_DEC_SOURCE_C="
            f"{relaxed_best['C_FP_alpha1']:.15e}"
        ),
        flush=True,
    )


if macro is not None and macro.get(
    "possible",
    False,
):

    print(
        (
            "MACRO_ALPHA_REQUIRED="
            f"{macro['alpha_required']:.15e}"
        ),
        flush=True,
    )

    print(
        (
            "MACRO_LAMBDA3_MARGIN="
            f"{macro['Lambda3_coupling_aware_margin']:.15e}"
        ),
        flush=True,
    )

    print(
        (
            "MACRO_VAINshtein_OVER_H="
            f"{macro['Vainshtein_over_h']:.15e}"
        ),
        flush=True,
    )

    print(
        (
            "MACRO_M_OUT_EV="
            f"{macro['primary_wall']['m_out_eV']:.15e}"
        ),
        flush=True,
    )

    print(
        (
            "MACRO_WALL_LOWER_BOUND_J="
            f"{macro['primary_wall']['canonical_wall_lower_bound_J']:.15e}"
        ),
        flush=True,
    )

    print(
        (
            "MACRO_PORTAL_HEALTH_PREFLIGHT="
            + (
                "YES"
                if macro[
                    "portal_health_preflight"
                ]
                else "NO"
            )
        ),
        flush=True,
    )


print(
    f"029A_DECISION={decision}",
    flush=True,
)

print(
    f"NEXT={next_step}",
    flush=True,
)

print(
    (
        "ROUTE_LEVEL_80_HEURISTIC_AUTHORIZED="
        + (
            "YES"
            if route_80
            else "NO"
        )
    ),
    flush=True,
)

print(
    "HEURISTIC_IS_PROBABILITY=NO",
    flush=True,
)

print(
    "FULL_LOCALIZED_BIMETRIC_SOLUTION=NO",
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
    f"B7_SCAN_CSV={OUT_B7}",
    flush=True,
)

print(
    f"RELAXED_SCAN_CSV={OUT_RELAXED}",
    flush=True,
)

print(
    f"PORTAL_CSV={OUT_PORTAL}",
    flush=True,
)

print(
    "029A_RUN_COMPLETE=YES",
    flush=True,
)
