"""
031B2-B0
========

83-GJ recovery gate using only rigid translation of existing real Q-balls
and previously declared ordinary-matter coupling headroom.

NO NEW SOURCE OPERATOR.

An isolated spherical Q-ball can be translated without changing its intrinsic
field equations, energy, Noether charge, or isolated stability.

This run:

- reconstructs promising 031B2-A solutions;
- reproduces their centered energy before using them;
- moves the solved source toward the payload;
- computes exact angular X-source containment inside the declared 0.95-m
  source region;
- computes X-source overlap with the finite payload;
- recomputes scalar and ordinary-GR acceleration over the complete payload
  surface and volume;
- first uses the promoted alpha_m=27.0079;
- then raises alpha_m only until the already declared 1% payload-backreaction
  diagnostic;
- asks whether E_inventory <= 8.27507820143e10 J.

The Q-ball source has exponentially small tails, not mathematical compact
support. Tail fractions are therefore explicitly reported rather than hidden.
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

from scipy.integrate import cumulative_trapezoid, quad
from scipy.optimize import brentq


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results/data"

QBALL_SOURCE = (
    SIM
    /
    "031b2a_global_qball_activated_scalar_control.py"
)

QBALL_SUMMARY = (
    DATA
    /
    "031b2a_global_qball_activated_scalar_control_summary.json"
)

QBALL_CSV = (
    DATA
    /
    "031b2a_global_qball_activated_scalar_control_scan.csv"
)

OUT_JSON = (
    DATA
    /
    "031b2b0_qball_payload_adjacent_translation_summary.json"
)

OUT_CSV = (
    DATA
    /
    "031b2b0_qball_payload_adjacent_translation_scan.csv"
)


G = 6.67430e-11
C = 299_792_458.0
G0 = 9.80665

MPL_GEV = 2.435e18
HBARC_GEV_M = 1.973269804e-16
J_PER_GEV = 1.602176634e-10

J_M3_TO_GEV4 = (
    (1.0 / J_PER_GEV)
    *
    HBARC_GEV_M**3
)

SOURCE_RADIUS_M = 0.95
PAYLOAD_RADIUS_M = 0.10
PAYLOAD_CENTER_M = 2.05

SOURCE_LEAK_LIMIT = 1.0e-4
STRICT_SOURCE_LEAK_DIAGNOSTIC = 1.0e-6
PAYLOAD_OVERLAP_LIMIT = 1.0e-10
BACKREACTION_LIMIT = 1.0e-2

PROVENANCE_REL_TOL = 7.0e-4
TARGET_REL_TOL = 2.0e-3

ALPHA_SEARCH_MAX = 100.0

SURFACE_MU_POINTS = 181
CM_RADIAL_POINTS = 16
CM_ANGULAR_POINTS = 20


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

    if spec is None or spec.loader is None:

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


def relerr(a, b):

    return (
        abs(a - b)
        /
        max(
            abs(a),
            abs(b),
            1.0e-300,
        )
    )


def to_builtin(value: Any):

    if isinstance(value, np.generic):

        return value.item()

    if isinstance(value, np.ndarray):

        return value.tolist()

    if isinstance(value, dict):

        return {
            str(key):
            to_builtin(item)
            for key, item
            in value.items()
        }

    if isinstance(value, (list, tuple)):

        return [
            to_builtin(item)
            for item
            in value
        ]

    return value


def as_bool(value):

    return (
        str(value).strip().lower()
        in
        (
            "true",
            "1",
            "yes",
        )
    )


def read_prefilter_rows():

    rows = []

    with QBALL_CSV.open(
        newline="",
    ) as handle:

        reader = csv.DictReader(
            handle
        )

        for raw in reader:

            if not as_bool(
                raw.get(
                    "success",
                    False,
                )
            ):

                continue

            if not as_bool(
                raw.get(
                    "prefilter_pass",
                    False,
                )
            ):

                continue

            rows.append(
                {
                    "omega":
                    float(
                        raw[
                            "omega"
                        ]
                    ),

                    "epsilon":
                    float(
                        raw[
                            "epsilon"
                        ]
                    ),

                    "chi":
                    float(
                        raw[
                            "chi"
                        ]
                    ),

                    "chi_factor":
                    float(
                        raw[
                            "chi_factor"
                        ]
                    ),

                    "E_inventory_J":
                    float(
                        raw[
                            "E_inventory_J"
                        ]
                    ),
                }
            )

    return rows


def select_rows(rows):

    chosen = {}

    for epsilon in sorted(
        set(
            row[
                "epsilon"
            ]
            for row
            in rows
        )
    ):

        group = sorted(
            [
                row
                for row
                in rows
                if math.isclose(
                    row[
                        "epsilon"
                    ],
                    epsilon,
                    rel_tol=0.0,
                    abs_tol=1.0e-12,
                )
            ],
            key=lambda row:
            row[
                "E_inventory_J"
            ],
        )

        for row in group[
            :4
        ]:

            chosen[
                (
                    row[
                        "omega"
                    ],
                    row[
                        "epsilon"
                    ],
                    row[
                        "chi_factor"
                    ],
                )
            ] = row

    for row in sorted(
        rows,
        key=lambda row:
        row[
            "E_inventory_J"
        ],
    )[
        :8
    ]:

        chosen[
            (
                row[
                    "omega"
                ],
                row[
                    "epsilon"
                ],
                row[
                    "chi_factor"
                ],
            )
        ] = row

    return list(
        chosen.values()
    )


def fraction_inside_origin_sphere(
    shell_radius,
    shift,
):

    r = np.asarray(
        shell_radius,
        dtype=float,
    )

    if shift <= 1.0e-15:

        return (
            r
            <=
            SOURCE_RADIUS_M
        ).astype(float)

    denom = (
        2.0
        *
        r
        *
        shift
    )

    c = np.divide(
        SOURCE_RADIUS_M**2
        -
        r**2
        -
        shift**2,
        denom,
        out=np.full_like(
            r,
            np.inf,
        ),
        where=denom
        !=
        0.0,
    )

    fraction = np.clip(
        0.5
        *
        (
            c
            +
            1.0
        ),
        0.0,
        1.0,
    )

    zero = (
        r
        <=
        1.0e-15
    )

    fraction[
        zero
    ] = (
        1.0
        if shift
        <=
        SOURCE_RADIUS_M
        else
        0.0
    )

    return fraction


def fraction_inside_payload(
    shell_radius,
    payload_distance,
):

    r = np.asarray(
        shell_radius,
        dtype=float,
    )

    denom = (
        2.0
        *
        r
        *
        payload_distance
    )

    c = np.divide(
        r**2
        +
        payload_distance**2
        -
        PAYLOAD_RADIUS_M**2,
        denom,
        out=np.full_like(
            r,
            np.inf,
        ),
        where=denom
        !=
        0.0,
    )

    fraction = np.clip(
        0.5
        *
        (
            1.0
            -
            c
        ),
        0.0,
        1.0,
    )

    zero = (
        r
        <=
        1.0e-15
    )

    fraction[
        zero
    ] = (
        1.0
        if payload_distance
        <=
        PAYLOAD_RADIUS_M
        else
        0.0
    )

    return fraction


def reconstruct(
    qmod,
    row,
    mediator_range,
):

    omega = row[
        "omega"
    ]

    epsilon = row[
        "epsilon"
    ]

    chi = row[
        "chi"
    ]

    seed = qmod.solve_uncoupled_qball(
        omega
    )

    if seed is None:

        return None

    solution = qmod.solve_coupled(
        seed,
        omega,
        epsilon,
        chi,
        previous=None,
    )

    if solution is None:

        return None

    x_match = float(
        qmod.X_MATCH
    )

    x = np.linspace(
        1.0e-5,
        x_match,
        12_000,
    )

    y, yp, u, up = solution.sol(
        x
    )

    A = np.exp(
        np.clip(
            -0.5
            *
            u**2,
            -700.0,
            0.0,
        )
    )

    potential = qmod.W(
        y
    )

    source_on_density = (
        0.5
        *
        yp**2
        +
        0.5
        *
        omega**2
        *
        y**2
        +
        A
        *
        potential
    )

    source_off_density = (
        0.5
        *
        yp**2
        +
        0.5
        *
        omega**2
        *
        y**2
        +
        potential
    )

    scalar_density = (
        (
            0.5
            *
            up**2
            +
            0.5
            *
            epsilon**2
            *
            u**2
        )
        /
        chi**2
    )

    total_on_density = (
        source_on_density
        +
        scalar_density
    )

    def integrate(density):

        return float(
            4.0
            *
            math.pi
            *
            np.trapezoid(
                x**2
                *
                density,
                x,
            )
        )

    I_X_ON = integrate(
        source_on_density
    )

    I_X_OFF = integrate(
        source_off_density
    )

    I_PHI_IN = integrate(
        scalar_density
    )

    u_boundary = float(
        solution.sol(
            x_match
        )[
            2
        ]
    )

    def tail_integrand(xx):

        uu = (
            u_boundary
            *
            x_match
            /
            xx
            *
            math.exp(
                -epsilon
                *
                (
                    xx
                    -
                    x_match
                )
            )
        )

        uup = (
            uu
            *
            (
                -epsilon
                -
                1.0
                /
                xx
            )
        )

        return (
            4.0
            *
            math.pi
            *
            xx**2
            *
            (
                0.5
                *
                uup**2
                +
                0.5
                *
                epsilon**2
                *
                uu**2
            )
            /
            chi**2
        )

    I_PHI_TAIL = float(
        quad(
            tail_integrand,
            x_match,
            np.inf,
            epsabs=1.0e-12,
            epsrel=1.0e-8,
            limit=200,
        )[
            0
        ]
    )

    I_INVENTORY = (
        I_X_OFF
        +
        I_PHI_IN
        +
        I_PHI_TAIL
    )

    mphi_gev = (
        HBARC_GEV_M
        /
        mediator_range
    )

    mx_gev = (
        mphi_gev
        /
        epsilon
    )

    length_m = (
        HBARC_GEV_M
        /
        mx_gev
    )

    physical_radius = (
        x
        *
        length_m
    )

    source_shell = (
        4.0
        *
        math.pi
        *
        x**2
        *
        source_on_density
    )

    cumulative_on = np.concatenate(
        (
            [
                0.0
            ],
            cumulative_trapezoid(
                4.0
                *
                math.pi
                *
                x**2
                *
                total_on_density,
                x,
            ),
        )
    )

    def enclosed(xx):

        return float(
            np.interp(
                xx,
                x,
                cumulative_on,
                left=0.0,
                right=cumulative_on[
                    -1
                ],
            )
        )

    return {
        "row":
        row,

        "solution":
        solution,

        "x":
        x,

        "source_shell":
        source_shell,

        "physical_radius":
        physical_radius,

        "I_X_ON":
        I_X_ON,

        "inventory_coeff":
        (
            I_INVENTORY
            /
            mx_gev
            *
            J_PER_GEV
        ),

        "mphi_gev":
        mphi_gev,

        "mx_gev":
        mx_gev,

        "length_m":
        length_m,

        "chi":
        chi,

        "enclosed":
        enclosed,
    }


def containment(
    case,
    shift,
):

    inside_source_region = (
        fraction_inside_origin_sphere(
            case[
                "physical_radius"
            ],
            shift,
        )
    )

    source_leak = (
        np.trapezoid(
            case[
                "source_shell"
            ]
            *
            (
                1.0
                -
                inside_source_region
            ),
            case[
                "x"
            ],
        )
        /
        case[
            "I_X_ON"
        ]
    )

    payload_distance = (
        PAYLOAD_CENTER_M
        -
        shift
    )

    payload_fraction = fraction_inside_payload(
        case[
            "physical_radius"
        ],
        payload_distance,
    )

    payload_overlap = (
        np.trapezoid(
            case[
                "source_shell"
            ]
            *
            payload_fraction,
            case[
                "x"
            ],
        )
        /
        case[
            "I_X_ON"
        ]
    )

    return (
        float(
            source_leak
        ),
        float(
            payload_overlap
        ),
    )


def force_solution(
    qmod,
    case,
    shift,
    alpha_m,
):

    solution = case[
        "solution"
    ]

    chi = case[
        "chi"
    ]

    length_m = case[
        "length_m"
    ]

    mx_gev = case[
        "mx_gev"
    ]

    payload_distance = (
        PAYLOAD_CENTER_M
        -
        shift
    )

    near_distance = (
        payload_distance
        -
        PAYLOAD_RADIUS_M
    )

    if near_distance <= 0.0:

        return None

    x_near = (
        near_distance
        /
        length_m
    )

    if x_near >= float(
        qmod.X_MATCH
    ):

        return None

    u_near = abs(
        float(
            solution.sol(
                x_near
            )[
                2
            ]
        )
    )

    if u_near <= 1.0e-15:

        return None

    def scalar_per_alpha_F(radius):

        xx = (
            radius
            /
            length_m
        )

        state = solution.sol(
            xx
        )

        u = float(
            state[
                2
            ]
        )

        up = float(
            state[
                3
            ]
        )

        return (
            -C**2
            *
            (
                mx_gev
                /
                (
                    chi
                    *
                    HBARC_GEV_M
                    *
                    MPL_GEV
                )
            )
            *
            (
                u
                *
                up
                /
                u_near
            )
        )

    def gr_per_F2(radius):

        xx = (
            radius
            /
            length_m
        )

        energy_coeff = (
            case[
                "enclosed"
            ](
                xx
            )
            /
            mx_gev
            *
            J_PER_GEV
        )

        return (
            G
            *
            (
                energy_coeff
                /
                C**2
            )
            /
            radius**2
        )

    mus = np.linspace(
        -1.0,
        1.0,
        SURFACE_MU_POINTS,
    )

    scalar_surface = []
    gr_surface = []

    for mu in mus:

        dz = (
            payload_distance
            +
            PAYLOAD_RADIUS_M
            *
            mu
        )

        transverse = (
            PAYLOAD_RADIUS_M
            *
            math.sqrt(
                max(
                    0.0,
                    1.0
                    -
                    mu**2,
                )
            )
        )

        radius = math.sqrt(
            dz**2
            +
            transverse**2
        )

        projection = (
            dz
            /
            radius
        )

        scalar_surface.append(
            alpha_m
            *
            scalar_per_alpha_F(
                radius
            )
            *
            projection
        )

        gr_surface.append(
            gr_per_F2(
                radius
            )
            *
            projection
        )

    scalar_surface = np.asarray(
        scalar_surface,
        dtype=float,
    )

    gr_surface = np.asarray(
        gr_surface,
        dtype=float,
    )

    radial_nodes, radial_weights = (
        np.polynomial.legendre.leggauss(
            CM_RADIAL_POINTS
        )
    )

    angular_nodes, angular_weights = (
        np.polynomial.legendre.leggauss(
            CM_ANGULAR_POINTS
        )
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

    payload_volume = (
        4.0
        *
        math.pi
        *
        PAYLOAD_RADIUS_M**3
        /
        3.0
    )

    scalar_cm = 0.0
    gr_cm = 0.0

    for s, ws in zip(
        payload_radii,
        payload_weights,
    ):

        for mu, wmu in zip(
            angular_nodes,
            angular_weights,
        ):

            dz = (
                payload_distance
                +
                s
                *
                mu
            )

            transverse = (
                s
                *
                math.sqrt(
                    max(
                        0.0,
                        1.0
                        -
                        mu**2,
                    )
                )
            )

            radius = math.sqrt(
                dz**2
                +
                transverse**2
            )

            projection = (
                dz
                /
                radius
            )

            common = (
                2.0
                *
                math.pi
                *
                s**2
                *
                ws
                *
                wmu
            )

            scalar_cm += (
                common
                *
                alpha_m
                *
                scalar_per_alpha_F(
                    radius
                )
                *
                projection
            )

            gr_cm += (
                common
                *
                gr_per_F2(
                    radius
                )
                *
                projection
            )

    scalar_cm /= payload_volume
    gr_cm /= payload_volume

    scalar_min = float(
        np.min(
            scalar_surface
        )
    )

    if scalar_min <= 0.0:

        return None

    guess = (
        G0
        /
        scalar_min
    )

    F_scan = np.geomspace(
        max(
            guess
            *
            1.0e-3,
            1.0e-12,
        ),
        guess
        *
        100.0,
        600,
    )

    def adverse(F):

        return float(
            np.min(
                scalar_surface
                *
                F
                -
                gr_surface
                *
                F**2
            )
        )

    residual = np.asarray(
        [
            adverse(F)
            -
            G0
            for F
            in F_scan
        ]
    )

    crossings = np.where(
        (
            residual[
                :-1
            ]
            <=
            0.0
        )
        &
        (
            residual[
                1:
            ]
            >=
            0.0
        )
    )[
        0
    ]

    if len(
        crossings
    ) == 0:

        return None

    index = int(
        crossings[
            0
        ]
    )

    F_required = float(
        brentq(
            lambda F:
            adverse(
                F
            )
            -
            G0,
            F_scan[
                index
            ],
            F_scan[
                index
                +
                1
            ],
            xtol=1.0e-12,
            rtol=1.0e-12,
            maxiter=300,
        )
    )

    surface_net = (
        scalar_surface
        *
        F_required
        -
        gr_surface
        *
        F_required**2
    )

    a_cm = (
        scalar_cm
        *
        F_required
        -
        gr_cm
        *
        F_required**2
    )

    E_inventory = (
        case[
            "inventory_coeff"
        ]
        *
        F_required**2
    )

    Mc_gev = (
        F_required
        /
        chi
    )

    phi_near = (
        Mc_gev
        *
        u_near
    )

    Mm2 = (
        MPL_GEV
        *
        phi_near
        /
        alpha_m
    )

    payload_density_gev4 = (
        8000.0
        *
        C**2
        *
        J_M3_TO_GEV4
    )

    backreaction = (
        payload_density_gev4
        /
        (
            Mm2
            *
            case[
                "mphi_gev"
            ]**2
        )
    )

    return {
        "alpha_m":
        float(
            alpha_m
        ),

        "F_gev":
        F_required,

        "E_inventory_J":
        E_inventory,

        "surface_min_mps2":
        float(
            np.min(
                surface_net
            )
        ),

        "surface_max_mps2":
        float(
            np.max(
                surface_net
            )
        ),

        "a_cm_mps2":
        float(
            a_cm
        ),

        "backreaction":
        float(
            backreaction
        ),

        "M_m_gev":
        math.sqrt(
            Mm2
        ),
    }


def maximum_shift(
    case,
    leak_limit,
):

    shifts = np.linspace(
        0.0,
        0.94,
        189,
    )

    allowed = []

    for shift in shifts:

        leak, overlap = containment(
            case,
            float(
                shift
            ),
        )

        if (
            leak
            <=
            leak_limit
            and
            overlap
            <=
            PAYLOAD_OVERLAP_LIMIT
        ):

            allowed.append(
                float(
                    shift
                )
            )

    if not allowed:

        return 0.0

    lower = max(
        allowed
    )

    larger = [
        float(
            shift
        )
        for shift
        in shifts
        if shift
        >
        lower
    ]

    if not larger:

        return lower

    upper = min(
        larger
    )

    leak_low, overlap_low = containment(
        case,
        lower,
    )

    leak_high, overlap_high = containment(
        case,
        upper,
    )

    if (
        overlap_high
        <=
        PAYLOAD_OVERLAP_LIMIT
        and
        leak_low
        <=
        leak_limit
        and
        leak_high
        >
        leak_limit
    ):

        return float(
            brentq(
                lambda shift:
                containment(
                    case,
                    shift,
                )[
                    0
                ]
                -
                leak_limit,
                lower,
                upper,
                xtol=1.0e-9,
                rtol=1.0e-10,
                maxiter=100,
            )
        )

    return lower


def alpha_ceiling_solution(
    qmod,
    case,
    shift,
    alpha_start,
):

    start = force_solution(
        qmod,
        case,
        shift,
        alpha_start,
    )

    if start is None:

        return None

    if start[
        "backreaction"
    ] > BACKREACTION_LIMIT:

        return None

    low = alpha_start

    high = (
        alpha_start
        *
        1.10
    )

    high_result = force_solution(
        qmod,
        case,
        shift,
        high,
    )

    while (
        high_result is not None
        and
        high_result[
            "backreaction"
        ]
        <
        BACKREACTION_LIMIT
        and
        high
        <
        ALPHA_SEARCH_MAX
    ):

        low = high

        high = min(
            high
            *
            1.15,
            ALPHA_SEARCH_MAX,
        )

        high_result = force_solution(
            qmod,
            case,
            shift,
            high,
        )

        if math.isclose(
            high,
            ALPHA_SEARCH_MAX,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ):

            break

    if high_result is None:

        return None

    if high_result[
        "backreaction"
    ] <= BACKREACTION_LIMIT:

        return high_result

    alpha = float(
        brentq(
            lambda value:
            force_solution(
                qmod,
                case,
                shift,
                value,
            )[
                "backreaction"
            ]
            -
            BACKREACTION_LIMIT,
            low,
            high,
            xtol=1.0e-8,
            rtol=1.0e-10,
            maxiter=120,
        )
    )

    return force_solution(
        qmod,
        case,
        shift,
        alpha,
    )


def main():

    print(
        "=== 031B2-B0 83-GJ "
        "PAYLOAD-ADJACENT Q-BALL TRANSLATION ==="
    )

    print(
        "CLAIM_CLASS="
        "EXISTING_MICROSCOPIC_SOURCE_"
        "MORPHOLOGY_AND_COUPLING_HEADROOM_GATE"
    )

    print(
        "NEW_SOURCE_OPERATOR=NO"
    )

    print(
        "SOURCE_INTRINSIC_SOLUTION_CHANGED=NO"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    require(
        QBALL_SOURCE
    )

    require(
        QBALL_SUMMARY
    )

    require(
        QBALL_CSV
    )

    summary = json.loads(
        QBALL_SUMMARY.read_text()
    )

    target = float(
        summary[
            "target_energy_J"
        ]
    )

    alpha_promoted = float(
        summary[
            "alpha_m_on_cap"
        ]
    )

    mediator_range = float(
        summary[
            "mediator_range_m"
        ]
    )

    prior_best = float(
        summary[
            "best"
        ][
            "E_inventory_J"
        ]
    )

    energy_gap = (
        prior_best
        /
        target
    )

    required_leverage = math.sqrt(
        energy_gap
    )

    muR = (
        SOURCE_RADIUS_M
        /
        mediator_range
    )

    centered_thin_shell_gain = (
        math.sinh(
            muR
        )
        /
        muR
    )

    print(
        f"TARGET_ENERGY_J="
        f"{target:.15e}"
    )

    print(
        f"PRIOR_REAL_QBALL_ENERGY_J="
        f"{prior_best:.15e}"
    )

    print(
        f"ENERGY_GAP_FACTOR="
        f"{energy_gap:.15e}"
    )

    print(
        f"REQUIRED_AMPLITUDE_LEVERAGE="
        f"{required_leverage:.15e}"
    )

    print(
        f"CENTERED_THIN_SPHERICAL_SHELL_YUKAWA_GAIN="
        f"{centered_thin_shell_gain:.15e}"
    )

    print(
        f"CENTERED_SHELL_GEOMETRY_ALONE_SUFFICIENT="
        f"{centered_thin_shell_gain >= required_leverage}"
    )

    qmod = load_module(
        "b2b0_upstream_qball",
        QBALL_SOURCE,
    )

    rows = select_rows(
        read_prefilter_rows()
    )

    print(
        f"SELECTED_BRANCHES="
        f"{len(rows)}"
    )

    output_rows = []

    provenance_all_pass = True

    for index, row in enumerate(
        rows
    ):

        case = reconstruct(
            qmod,
            row,
            mediator_range,
        )

        if case is None:

            continue

        centered = force_solution(
            qmod,
            case,
            0.0,
            alpha_promoted,
        )

        if centered is None:

            continue

        provenance_error = relerr(
            centered[
                "E_inventory_J"
            ],
            row[
                "E_inventory_J"
            ],
        )

        provenance_pass = bool(
            provenance_error
            <=
            PROVENANCE_REL_TOL
        )

        provenance_all_pass = (
            provenance_all_pass
            and
            provenance_pass
        )

        print(
            f"CENTERED_PROVENANCE "
            f"OMEGA={row['omega']:.9e} "
            f"EPS={row['epsilon']:.9e} "
            f"CHI_FACTOR={row['chi_factor']:.9e} "
            f"RELERR={provenance_error:.9e} "
            f"PASS={provenance_pass}"
        )

        if not provenance_pass:

            continue

        max_shift = maximum_shift(
            case,
            SOURCE_LEAK_LIMIT,
        )

        strict_shift = maximum_shift(
            case,
            STRICT_SOURCE_LEAK_DIAGNOSTIC,
        )

        shifts = sorted(
            set(
                [
                    0.0,
                    0.25
                    *
                    max_shift,
                    0.50
                    *
                    max_shift,
                    0.75
                    *
                    max_shift,
                    max_shift,
                ]
            )
        )

        branch_rows = []

        for shift in shifts:

            leak, overlap = containment(
                case,
                shift,
            )

            promoted = force_solution(
                qmod,
                case,
                shift,
                alpha_promoted,
            )

            ceiling = alpha_ceiling_solution(
                qmod,
                case,
                shift,
                alpha_promoted,
            )

            if (
                promoted is None
                or
                ceiling is None
            ):

                continue

            result = {
                "omega":
                row[
                    "omega"
                ],

                "epsilon":
                row[
                    "epsilon"
                ],

                "chi":
                row[
                    "chi"
                ],

                "chi_factor":
                row[
                    "chi_factor"
                ],

                "shift_m":
                shift,

                "max_shift_1e4_m":
                max_shift,

                "max_shift_1e6_m":
                strict_shift,

                "source_leak":
                leak,

                "payload_overlap":
                overlap,

                "promoted_alpha":
                alpha_promoted,

                "promoted_energy_J":
                promoted[
                    "E_inventory_J"
                ],

                "promoted_backreaction":
                promoted[
                    "backreaction"
                ],

                "ceiling_alpha":
                ceiling[
                    "alpha_m"
                ],

                "ceiling_energy_J":
                ceiling[
                    "E_inventory_J"
                ],

                "ceiling_backreaction":
                ceiling[
                    "backreaction"
                ],

                "ceiling_surface_min_mps2":
                ceiling[
                    "surface_min_mps2"
                ],

                "ceiling_a_cm_mps2":
                ceiling[
                    "a_cm_mps2"
                ],
            }

            branch_rows.append(
                result
            )

            output_rows.append(
                result
            )

            print(
                f"TRANSLATION_CASE "
                f"OMEGA={row['omega']:.9e} "
                f"EPS={row['epsilon']:.9e} "
                f"CHI_FACTOR={row['chi_factor']:.9e} "
                f"SHIFT_M={shift:.9e} "
                f"LEAK={leak:.9e} "
                f"OVERLAP={overlap:.9e} "
                f"E_ALPHA27_J="
                f"{promoted['E_inventory_J']:.9e} "
                f"ALPHA_CEIL="
                f"{ceiling['alpha_m']:.9e} "
                f"E_CEIL_J="
                f"{ceiling['E_inventory_J']:.9e} "
                f"BACK_CEIL="
                f"{ceiling['backreaction']:.9e}"
            )

        if branch_rows:

            best_branch = min(
                branch_rows,
                key=lambda item:
                item[
                    "ceiling_energy_J"
                ],
            )

            print(
                f"BRANCH_BEST "
                f"OMEGA={row['omega']:.9e} "
                f"EPS={row['epsilon']:.9e} "
                f"CHI_FACTOR={row['chi_factor']:.9e} "
                f"MAX_SHIFT_1E4_M="
                f"{max_shift:.9e} "
                f"MAX_SHIFT_1E6_M="
                f"{strict_shift:.9e} "
                f"BEST_SHIFT_M="
                f"{best_branch['shift_m']:.9e} "
                f"BEST_ALPHA="
                f"{best_branch['ceiling_alpha']:.9e} "
                f"BEST_E_J="
                f"{best_branch['ceiling_energy_J']:.9e}"
            )

    if not output_rows:

        raise RuntimeError(
            "No translated cases survived provenance"
        )

    best = min(
        output_rows,
        key=lambda item:
        item[
            "ceiling_energy_J"
        ],
    )

    promoted_survivors = [
        row
        for row
        in output_rows
        if (
            row[
                "promoted_energy_J"
            ]
            <=
            target
            *
            (
                1.0
                +
                TARGET_REL_TOL
            )
            and
            row[
                "source_leak"
            ]
            <=
            SOURCE_LEAK_LIMIT
            and
            row[
                "payload_overlap"
            ]
            <=
            PAYLOAD_OVERLAP_LIMIT
        )
    ]

    ceiling_survivors = [
        row
        for row
        in output_rows
        if (
            row[
                "ceiling_energy_J"
            ]
            <=
            target
            *
            (
                1.0
                +
                TARGET_REL_TOL
            )
            and
            row[
                "ceiling_backreaction"
            ]
            <=
            BACKREACTION_LIMIT
            *
            (
                1.0
                +
                1.0e-6
            )
            and
            row[
                "source_leak"
            ]
            <=
            SOURCE_LEAK_LIMIT
            and
            row[
                "payload_overlap"
            ]
            <=
            PAYLOAD_OVERLAP_LIMIT
        )
    ]

    print(
        "\n=== 83-GJ DECISION ==="
    )

    print(
        f"CENTERED_PROVENANCE_ALL_PASS="
        f"{provenance_all_pass}"
    )

    print(
        f"BEST_TRANSLATED_ENERGY_J="
        f"{best['ceiling_energy_J']:.15e}"
    )

    print(
        f"BEST_TRANSLATED_ENERGY_OVER_83GJ_TARGET="
        f"{best['ceiling_energy_J'] / target:.15e}"
    )

    print(
        f"BEST_TRANSLATED_SHIFT_M="
        f"{best['shift_m']:.15e}"
    )

    print(
        f"BEST_TRANSLATED_ALPHA_M="
        f"{best['ceiling_alpha']:.15e}"
    )

    print(
        f"BEST_TRANSLATED_BACKREACTION="
        f"{best['ceiling_backreaction']:.15e}"
    )

    print(
        f"BEST_TRANSLATED_SOURCE_LEAK="
        f"{best['source_leak']:.15e}"
    )

    print(
        f"BEST_TRANSLATED_PAYLOAD_OVERLAP="
        f"{best['payload_overlap']:.15e}"
    )

    print(
        f"BEST_TRANSLATED_OMEGA="
        f"{best['omega']:.15e}"
    )

    print(
        f"BEST_TRANSLATED_EPSILON="
        f"{best['epsilon']:.15e}"
    )

    print(
        f"BEST_TRANSLATED_CHI_FACTOR="
        f"{best['chi_factor']:.15e}"
    )

    print(
        f"PROMOTED_ALPHA_83GJ_SURVIVORS="
        f"{len(promoted_survivors)}"
    )

    print(
        f"BACKREACTION_CEILING_83GJ_SURVIVORS="
        f"{len(ceiling_survivors)}"
    )

    if promoted_survivors:

        classification = (
            "GREEN_REAL_QBALL_RECOVERS_83GJ_"
            "BY_TRANSLATION_AT_EXISTING_ALPHA"
        )

        next_step = (
            "031B2C83_TRANSLATED_QBALL_FULL_"
            "STABILITY_AND_ACTIVATION_GATE"
        )

    elif ceiling_survivors:

        classification = (
            "GREEN_REAL_QBALL_RECOVERS_83GJ_"
            "BY_TRANSLATION_WITHIN_PREDECLARED_"
            "1PCT_BACKREACTION_HEADROOM"
        )

        next_step = (
            "031B2C83_TRANSLATED_QBALL_FULL_"
            "STABILITY_AND_ACTIVATION_GATE"
        )

    else:

        classification = (
            "RED_TRANSLATION_PLUS_ALLOWED_"
            "COUPLING_HEADROOM_CANNOT_RECOVER_83GJ"
        )

        next_step = (
            "031C_QSHELL_OR_MULTICOMPONENT_"
            "PAYLOAD_ADJACENT_SOURCE_GATE"
        )

    print(
        f"031B2B0_CLASSIFICATION="
        f"{classification}"
    )

    print(
        f"NEXT="
        f"{next_step}"
    )

    print(
        "STRICT_COMPACT_SOURCE_SUPPORT="
        "NO_QBALL_HAS_EXPONENTIAL_TAILS"
    )

    print(
        "FULL_SOURCE_PAYLOAD_REACTION="
        "NOT_YET"
    )

    print(
        "FULL_NONRADIAL_STABILITY="
        "NOT_YET"
    )

    print(
        "ACTIVATION_OFFSTATE="
        "NOT_YET"
    )

    print(
        "PRACTICAL_DEVICE=NO"
    )

    OUT_CSV.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUT_CSV.open(
        "w",
        newline="",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=list(
                output_rows[
                    0
                ].keys()
            ),
        )

        writer.writeheader()

        writer.writerows(
            output_rows
        )

    result = {
        "claim_class":
        "EXISTING_MICROSCOPIC_SOURCE_"
        "MORPHOLOGY_AND_COUPLING_HEADROOM_GATE",

        "target_energy_J":
        target,

        "prior_best_energy_J":
        prior_best,

        "energy_gap_factor":
        energy_gap,

        "required_amplitude_leverage":
        required_leverage,

        "centered_thin_shell_yukawa_gain":
        centered_thin_shell_gain,

        "centered_shell_geometry_alone_sufficient":
        centered_thin_shell_gain
        >=
        required_leverage,

        "centered_provenance_all_pass":
        provenance_all_pass,

        "promoted_alpha_survivors":
        len(
            promoted_survivors
        ),

        "backreaction_ceiling_survivors":
        len(
            ceiling_survivors
        ),

        "best":
        best,

        "classification":
        classification,

        "next":
        next_step,

        "claim_limits": [
            "No new microscopic interaction is introduced.",
            "The existing isolated Q-ball is translated rigidly.",
            "Payload reaction on the source fields remains perturbative.",
            "Q-ball X support is exponentially small but not exactly compact.",
            "The declared 1e-4 source containment and 1e-10 payload-overlap thresholds are explicit operational thresholds, not exact mathematical compact support.",
            "Alpha_m is allowed to rise only to the previously declared 1% payload-backreaction diagnostic.",
            "Full coupled nonradial stability remains open.",
            "Activation/off-state and empirical closure remain open.",
            "No practical device is established.",
        ],
    }

    OUT_JSON.write_text(
        json.dumps(
            to_builtin(
                result
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
