"""
031A-R4
=======

Z2 induced-scalarization finite-source BVP.

This run replaces prescribed scalar charge with an actual nonlinear scalar
field equation.

Einstein-frame scalar scaffold:

    V(phi) = 1/2 m_phi^2 phi^2

Exotic source coupling:

    A_X(phi) = exp[-phi^2/(2 M_X^2)]

Ordinary neutral-matter coupling:

    A_m(phi) = exp[+phi^2/(2 M_m^2)]

A finite X source therefore has

    V_eff(phi)
      = 1/2 m_phi^2 phi^2
        + rho_X A_X(phi)

and

    V_eff''(0)
      = m_phi^2 - rho_X/M_X^2.

For sufficiently large rho_X the phi=0 source state becomes tachyonically
unstable and a scalarized branch can emerge.

Ordinary neutral matter follows the physical metric

    g_tilde = A_m(phi)^2 g

and therefore, in the weak-field static limit,

    a_phi
      = -c^2 grad ln A_m
      = -(c^2/M_m^2) phi grad(phi).

A single-sign scalarized lump can consequently repel ordinary neutral matter
while the asymptotic vacuum phi=0 has zero linear ordinary-matter coupling.

IMPORTANT CLAIM LIMITS

- Prescribed X matter density profile is still external.
- X support dynamics are not solved.
- Full local conservation of source + supports is therefore NOT established.
- Nonradial stability is not established.
- EFT/radiative naturalness is not established.
- Earth/environment reciprocity is only diagnosed perturbatively.
- This is NOT a practical device.

The energy ledger reports:

    E_on =
        dressed X energy
      + scalar gradient energy
      + scalar potential energy

    E_off =
        unscreened X source inventory at phi=0

and conservatively uses

    E_inventory = max(E_on, E_off).

No negative transition-energy credit is used.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np

from numpy.polynomial.legendre import leggauss

from scipy.integrate import solve_bvp
from scipy.optimize import brentq
from scipy.sparse import diags
from scipy.sparse.linalg import eigsh


G = 6.67430e-11
C = 299_792_458.0
G0 = 9.80665

MPL_GEV = 2.435e18

HBARC_GEV_M = 1.973269804e-16

L_PER_M = 1.0 / HBARC_GEV_M

J_PER_GEV = 1.602176634e-10

J_M3_TO_GEV4 = (
    (1.0 / J_PER_GEV)
    *
    HBARC_GEV_M**3
)


PAYLOAD_RADIUS_M = 0.10

CLEARANCE_M = 1.00


TARGET_1TJ_J = 1.0e12

TARGET_1E11_J = 1.0e11


MEDIATOR_RANGE_M = 3.30

M_PHI_GEV = (
    HBARC_GEV_M
    /
    MEDIATOR_RANGE_M
)


# Least-deformed classical R3 Z2 scaffold.
M_X_GEV = 8.365645334354521e1

M_M_R3_SEED_GEV = 6.273348993561532e9


# Maintain the previous physically motivated ordinary-matter coupling scale:
# require |alpha_m| <= 10 everywhere in the finite payload.
ALPHA_M_PAYLOAD_CAP = 10.0


SOURCE_RADII_M = (
    0.70,
    0.80,
    0.90,
    0.95,
    1.00,
    1.10,
    1.25,
    1.50,
    2.00,
)


# Includes the user's blind wildcard values where scientifically harmless.
ETA_OVER_CRIT = (
    0.625,
    1.05,
    1.25,
    1.60,
    1.875,
    3.125,
    5.0,
    7.5,
    9.0,
    10.0,
    12.0,
    15.0,
)


EDGE_WIDTHS_M = (
    0.025,
    0.050,
    0.075,
    0.100,
)


RESULTS = Path(
    "results/data"
)

RESULTS.mkdir(
    parents=True,
    exist_ok=True,
)


def source_profile(
    r,
    radius,
    edge_width,
):

    r = np.asarray(
        r,
        dtype=float,
    )

    result = np.zeros_like(
        r
    )

    inner = max(
        0.0,
        radius
        -
        edge_width,
    )

    result[
        r
        <=
        inner
    ] = 1.0

    mask = (
        (r > inner)
        &
        (r < radius)
    )

    if np.any(
        mask
    ):

        t = (
            radius
            -
            r[
                mask
            ]
        ) / edge_width

        # C1 compact smoothstep.
        result[
            mask
        ] = (
            3.0
            *
            t**2
            -
            2.0
            *
            t**3
        )

    return result


def sharp_sphere_eta_critical(
    radius,
):

    """
    Exact l=0 zero-mode threshold for a sharp uniform sphere.

    Inside at onset:

        phi ~ sin(k r)/r

    Outside:

        phi ~ exp(-m r)/r

    Matching gives

        k cot(k R) = -m

    with the first root in (pi/2, pi).

    eta = rho_X/(m^2 M_X^2)

    and

        k = m sqrt(eta - 1).
    """

    mR = (
        radius
        /
        MEDIATOR_RANGE_M
    )

    root = brentq(
        lambda x:
        (
            x
            /
            math.tan(
                x
            )
            +
            mR
        ),
        math.pi
        /
        2.0
        +
        1.0e-10,
        math.pi
        -
        1.0e-10,
    )

    eta = (
        1.0
        +
        (
            root
            /
            mR
        )**2
    )

    return eta


def solve_scalar_bvp(
    radius,
    eta,
    tolerance=1.0e-4,
    edge_width=None,
):

    if edge_width is None:

        edge_width = min(
            0.050,
            radius
            /
            10.0,
        )

    edge_width = min(
        edge_width,
        radius
        /
        4.0,
    )

    rho_critical = (
        M_PHI_GEV**2
        *
        M_X_GEV**2
    )

    rho_bare = (
        eta
        *
        rho_critical
    )

    phi_bulk_guess = (
        M_X_GEV
        *
        math.sqrt(
            max(
                0.0,
                2.0
                *
                math.log(
                    max(
                        eta,
                        1.0
                        +
                        1.0e-15,
                    )
                ),
            )
        )
    )

    r_max = (
        radius
        +
        8.0
        *
        MEDIATOR_RANGE_M
    )

    transition_start = max(
        1.0e-5,
        radius
        -
        edge_width,
    )

    r = np.unique(
        np.concatenate(
            (
                np.linspace(
                    1.0e-5,
                    transition_start,
                    150,
                ),
                np.linspace(
                    transition_start,
                    radius,
                    80,
                ),
                np.linspace(
                    radius,
                    r_max,
                    300,
                ),
            )
        )
    )

    phi_guess = np.where(
        r <= radius,
        phi_bulk_guess,
        phi_bulk_guess
        *
        radius
        /
        r
        *
        np.exp(
            -(
                r
                -
                radius
            )
            /
            MEDIATOR_RANGE_M
        ),
    )

    dphi_guess = np.gradient(
        phi_guess,
        r,
    )

    def equations(
        rr,
        y,
    ):

        phi = y[
            0
        ]

        profile = source_profile(
            rr,
            radius,
            edge_width,
        )

        A_X = np.exp(
            np.clip(
                -phi**2
                /
                (
                    2.0
                    *
                    M_X_GEV**2
                ),
                -700.0,
                0.0,
            )
        )

        source_term = (
            rho_bare
            *
            profile
            *
            phi
            /
            M_X_GEV**2
            *
            A_X
        )

        rhs_natural = (
            M_PHI_GEV**2
            *
            phi
            -
            source_term
        )

        return np.vstack(
            (
                y[
                    1
                ],
                L_PER_M**2
                *
                rhs_natural
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

    def boundary_conditions(
        y_left,
        y_right,
    ):

        return np.array(
            (
                y_left[
                    1
                ],
                y_right[
                    0
                ],
            )
        )

    guess = np.vstack(
        (
            phi_guess,
            dphi_guess,
        )
    )

    solution = solve_bvp(
        equations,
        boundary_conditions,
        r,
        guess,
        tol=tolerance,
        max_nodes=30_000,
        verbose=0,
    )

    # The trivial phi=0 solution always exists. If the first solve falls back
    # onto it, retry with a larger scalarized seed.
    if solution.success:

        phi_center = abs(
            float(
                solution.sol(
                    1.0e-5
                )[
                    0
                ]
            )
        )

        if (
            phi_bulk_guess
            >
            0.0
            and
            phi_center
            <
            1.0e-5
            *
            max(
                1.0,
                phi_bulk_guess,
            )
        ):

            solution = solve_bvp(
                equations,
                boundary_conditions,
                r,
                1.6
                *
                guess,
                tol=tolerance,
                max_nodes=30_000,
                verbose=0,
            )

    return {
        "solution":
        solution,

        "rho_bare_gev4":
        rho_bare,

        "rho_critical_gev4":
        rho_critical,

        "phi_bulk_guess_gev":
        phi_bulk_guess,

        "edge_width_m":
        edge_width,

        "radius_m":
        radius,

        "eta":
        eta,
    }


def energy_ledger(
    solved,
    samples=7000,
):

    solution = solved[
        "solution"
    ]

    radius = solved[
        "radius_m"
    ]

    edge_width = solved[
        "edge_width_m"
    ]

    rho_bare = solved[
        "rho_bare_gev4"
    ]

    r = np.linspace(
        1.0e-5,
        solution.x[
            -1
        ],
        samples,
    )

    phi, dphi_dr_m = solution.sol(
        r
    )

    profile = source_profile(
        r,
        radius,
        edge_width,
    )

    A_X = np.exp(
        np.clip(
            -phi**2
            /
            (
                2.0
                *
                M_X_GEV**2
            ),
            -700.0,
            0.0,
        )
    )

    gradient_density_gev4 = (
        0.5
        *
        (
            dphi_dr_m
            /
            L_PER_M
        )**2
    )

    potential_density_gev4 = (
        0.5
        *
        M_PHI_GEV**2
        *
        phi**2
    )

    dressed_source_density_gev4 = (
        rho_bare
        *
        profile
        *
        A_X
    )

    off_source_density_gev4 = (
        rho_bare
        *
        profile
    )

    volume_factor = (
        4.0
        *
        math.pi
        *
        r**2
    )

    def integrate_density(
        density,
    ):

        return float(
            np.trapezoid(
                density
                /
                J_M3_TO_GEV4
                *
                volume_factor,
                r,
            )
        )

    E_gradient = integrate_density(
        gradient_density_gev4
    )

    E_potential = integrate_density(
        potential_density_gev4
    )

    E_source_on = integrate_density(
        dressed_source_density_gev4
    )

    E_source_off = integrate_density(
        off_source_density_gev4
    )

    E_on = (
        E_gradient
        +
        E_potential
        +
        E_source_on
    )

    E_inventory = max(
        E_on,
        E_source_off,
    )

    return {
        "E_gradient_J":
        E_gradient,

        "E_potential_J":
        E_potential,

        "E_source_on_J":
        E_source_on,

        "E_source_off_J":
        E_source_off,

        "E_on_J":
        E_on,

        "E_inventory_J":
        E_inventory,

        "off_over_on":
        (
            E_source_off
            /
            E_source_on
            if E_source_on
            >
            0.0
            else math.inf
        ),
    }


def physical_scalar_acceleration(
    solution,
    radius_from_source,
    M_m_gev,
):

    phi, dphi = solution.sol(
        radius_from_source
    )

    return float(
        -C**2
        *
        phi
        *
        dphi
        /
        M_m_gev**2
    )


def conservative_gr_acceleration(
    E_on,
    radius_from_source,
):

    return (
        G
        *
        (
            E_on
            /
            C**2
        )
        /
        radius_from_source**2
    )


def finite_payload_response(
    solved,
    ledger,
    M_m_gev,
):

    solution = solved[
        "solution"
    ]

    source_radius = solved[
        "radius_m"
    ]

    payload_center = (
        source_radius
        +
        CLEARANCE_M
        +
        PAYLOAD_RADIUS_M
    )

    def radial_net_acceleration(
        r,
    ):

        return (
            physical_scalar_acceleration(
                solution,
                r,
                M_m_gev,
            )
            -
            conservative_gr_acceleration(
                ledger[
                    "E_on_J"
                ],
                r,
            )
        )

    surface_radii = (
        payload_center
        -
        PAYLOAD_RADIUS_M,
        payload_center,
        payload_center
        +
        PAYLOAD_RADIUS_M,
    )

    surface_values = [
        radial_net_acceleration(
            r
        )
        for r
        in surface_radii
    ]

    radial_nodes, radial_weights = leggauss(
        18
    )

    angular_nodes, angular_weights = leggauss(
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

    payload_radial_weights = (
        0.5
        *
        PAYLOAD_RADIUS_M
        *
        radial_weights
    )

    volume = (
        4.0
        *
        math.pi
        *
        PAYLOAD_RADIUS_M**3
        /
        3.0
    )

    integral = 0.0

    for s, ws in zip(
        payload_radii,
        payload_radial_weights,
    ):

        for mu, wmu in zip(
            angular_nodes,
            angular_weights,
        ):

            r = math.sqrt(
                payload_center**2
                +
                s**2
                +
                2.0
                *
                payload_center
                *
                s
                *
                mu
            )

            projection = (
                payload_center
                +
                s
                *
                mu
            ) / r

            integral += (
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
                radial_net_acceleration(
                    r
                )
                *
                projection
            )

    a_cm = (
        integral
        /
        volume
    )

    return {
        "payload_center_m":
        payload_center,

        "a_cm_mps2":
        a_cm,

        "a_near_surface_mps2":
        surface_values[
            0
        ],

        "a_center_sample_mps2":
        surface_values[
            1
        ],

        "a_far_surface_mps2":
        surface_values[
            2
        ],

        "a_adverse_surface_mps2":
        min(
            surface_values
        ),
    }


def payload_matter_mass_shift_ratio(
    M_m_gev,
    density_kg_m3,
):

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

    return (
        rho_energy_gev4
        /
        (
            M_m_gev**2
            *
            M_PHI_GEV**2
        )
    )


def radial_hessian_lowest_mode(
    solved,
):

    solution = solved[
        "solution"
    ]

    radius = solved[
        "radius_m"
    ]

    edge_width = solved[
        "edge_width_m"
    ]

    rho_bare = solved[
        "rho_bare_gev4"
    ]

    n = 1500

    r = np.linspace(
        0.0,
        solution.x[
            -1
        ],
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

    interior_r = r[
        1:-1
    ]

    phi = solution.sol(
        np.maximum(
            interior_r,
            1.0e-6,
        )
    )[
        0
    ]

    profile = source_profile(
        interior_r,
        radius,
        edge_width,
    )

    A_X = np.exp(
        np.clip(
            -phi**2
            /
            (
                2.0
                *
                M_X_GEV**2
            ),
            -700.0,
            0.0,
        )
    )

    A_X_second = (
        A_X
        *
        (
            phi**2
            /
            M_X_GEV**4
            -
            1.0
            /
            M_X_GEV**2
        )
    )

    effective_curvature = (
        M_PHI_GEV**2
        +
        rho_bare
        *
        profile
        *
        A_X_second
    )

    U_per_m2 = (
        L_PER_M**2
        *
        effective_curvature
    )

    diagonal = (
        2.0
        /
        h**2
        +
        U_per_m2
    )

    off_diagonal = (
        -np.ones(
            len(
                interior_r
            )
            -
            1
        )
        /
        h**2
    )

    operator = diags(
        (
            off_diagonal,
            diagonal,
            off_diagonal,
        ),
        (
            -1,
            0,
            1,
        ),
        format="csr",
    )

    eigenvalue = eigsh(
        operator,
        k=1,
        which="SA",
        return_eigenvectors=False,
        tol=1.0e-8,
    )[
        0
    ]

    return float(
        eigenvalue
    )


def evaluate_case(
    radius,
    factor,
    tolerance=1.0e-4,
    edge_width=None,
):

    eta_critical = sharp_sphere_eta_critical(
        radius
    )

    eta = (
        factor
        *
        eta_critical
    )

    solved = solve_scalar_bvp(
        radius,
        eta,
        tolerance=tolerance,
        edge_width=edge_width,
    )

    solution = solved[
        "solution"
    ]

    if not solution.success:

        return {
            "success":
            False,

            "radius_m":
            radius,

            "factor":
            factor,

            "eta_critical":
            eta_critical,

            "eta":
            eta,

            "message":
            solution.message,
        }

    phi_center = abs(
        float(
            solution.sol(
                1.0e-5
            )[
                0
            ]
        )
    )

    if phi_center < 1.0e-3:

        return {
            "success":
            False,

            "trivial_branch":
            True,

            "radius_m":
            radius,

            "factor":
            factor,

            "eta_critical":
            eta_critical,

            "eta":
            eta,

            "message":
            "TRIVIAL_PHI_ZERO_BRANCH",
        }

    ledger = energy_ledger(
        solved
    )

    payload_center = (
        radius
        +
        CLEARANCE_M
        +
        PAYLOAD_RADIUS_M
    )

    near_payload_radius = (
        payload_center
        -
        PAYLOAD_RADIUS_M
    )

    phi_near = abs(
        float(
            solution.sol(
                near_payload_radius
            )[
                0
            ]
        )
    )

    if phi_near <= 0.0:

        return {
            "success":
            False,

            "radius_m":
            radius,

            "factor":
            factor,

            "message":
            "ZERO_PAYLOAD_FIELD",
        }

    # Choose the strongest ordinary-matter coupling allowed by the declared
    # alpha_m cap at the nearest payload surface.
    M_m_required = math.sqrt(
        MPL_GEV
        *
        phi_near
        /
        ALPHA_M_PAYLOAD_CAP
    )

    response = finite_payload_response(
        solved,
        ledger,
        M_m_required,
    )

    payload_screening_8000 = (
        payload_matter_mass_shift_ratio(
            M_m_required,
            8000.0,
        )
    )

    alpha_x_center = (
        -MPL_GEV
        *
        phi_center
        /
        M_X_GEV**2
    )

    compactness = (
        2.0
        *
        G
        *
        ledger[
            "E_on_J"
        ]
        /
        (
            C**4
            *
            radius
        )
    )

    result = {
        "success":
        True,

        "radius_m":
        radius,

        "edge_width_m":
        solved[
            "edge_width_m"
        ],

        "factor":
        factor,

        "eta_critical":
        eta_critical,

        "eta":
        eta,

        "phi_center_gev":
        phi_center,

        "phi_near_payload_gev":
        phi_near,

        "alpha_x_center":
        alpha_x_center,

        "M_m_required_gev":
        M_m_required,

        "alpha_m_near_payload":
        ALPHA_M_PAYLOAD_CAP,

        "payload_mass_shift_ratio_rho8000":
        payload_screening_8000,

        "compactness":
        compactness,

        **ledger,

        **response,
    }

    result[
        "_solved"
    ] = solved

    return result


def public_row(
    result,
):

    return {
        key:
        value
        for key, value
        in result.items()
        if not key.startswith(
            "_"
        )
    }


def main():

    print(
        "=== 031A-R4 Z2 INDUCED-SCALARIZATION "
        "FINITE-SOURCE BVP ==="
    )

    print(
        "CLAIM_CLASS="
        "NONLINEAR_SCALAR_FIELD_EXISTENCE_PREFLIGHT"
    )

    print(
        "TRUE_ANTIGRAVITY_TARGET="
        "YES_NEUTRAL_MATTER_PHYSICAL_METRIC"
    )

    print(
        "SCALAR_CHARGE_PRESCRIBED="
        "NO"
    )

    print(
        "X_DENSITY_PROFILE_DYNAMICAL="
        "NO_NOT_YET"
    )

    print(
        "FULL_LOCAL_CONSERVATION="
        "NO_NOT_YET"
    )

    print(
        "PRACTICAL_DEVICE="
        "NO"
    )

    print(
        f"MEDIATOR_RANGE_M="
        f"{MEDIATOR_RANGE_M:.15e}"
    )

    print(
        f"M_X_GEV="
        f"{M_X_GEV:.15e}"
    )

    print(
        f"M_M_R3_SEED_GEV="
        f"{M_M_R3_SEED_GEV:.15e}"
    )

    print(
        f"ALPHA_M_PAYLOAD_CAP="
        f"{ALPHA_M_PAYLOAD_CAP:.15e}"
    )

    print(
        "OFF_STATE_LINEAR_MATTER_COUPLING="
        "ZERO_BY_Z2_SYMMETRY"
    )

    print(
        "\n=== A — EXACT FINITE-SIZE "
        "SCALARIZATION THRESHOLDS ==="
    )

    for radius in SOURCE_RADII_M:

        eta_critical = sharp_sphere_eta_critical(
            radius
        )

        print(
            f"SCALARIZATION_THRESHOLD "
            f"R_M={radius:.9e} "
            f"ETA_CRIT_SHARP="
            f"{eta_critical:.9e}"
        )

    print(
        "\n=== B — NONLINEAR BVP SCAN ==="
    )

    rows = []

    candidates = []

    for radius in SOURCE_RADII_M:

        for factor in ETA_OVER_CRIT:

            result = evaluate_case(
                radius,
                factor,
            )

            rows.append(
                public_row(
                    result
                )
            )

            if not result.get(
                "success",
                False,
            ):

                print(
                    f"BVP_CASE "
                    f"R_M={radius:g} "
                    f"FACTOR={factor:g} "
                    f"SUCCESS=False "
                    f"REASON="
                    f"{result.get('message', 'UNKNOWN')}"
                )

                continue

            print(
                f"BVP_CASE "
                f"R_M={radius:g} "
                f"FACTOR={factor:g} "
                f"ETA={result['eta']:.9e} "
                f"PHI0_GEV="
                f"{result['phi_center_gev']:.9e} "
                f"MM_GEV="
                f"{result['M_m_required_gev']:.9e} "
                f"E_ON_J="
                f"{result['E_on_J']:.9e} "
                f"E_OFF_J="
                f"{result['E_source_off_J']:.9e} "
                f"E_INV_J="
                f"{result['E_inventory_J']:.9e} "
                f"A_CM="
                f"{result['a_cm_mps2']:.9e} "
                f"A_ADVERSE="
                f"{result['a_adverse_surface_mps2']:.9e} "
                f"PAYLOAD_BACKREACTION_RATIO="
                f"{result['payload_mass_shift_ratio_rho8000']:.9e}"
            )

            if (
                result[
                    "a_adverse_surface_mps2"
                ]
                >=
                G0
                and
                result[
                    "E_inventory_J"
                ]
                <=
                TARGET_1TJ_J
                and
                result[
                    "payload_mass_shift_ratio_rho8000"
                ]
                <=
                1.0e-2
            ):

                candidates.append(
                    result
                )

    print(
        f"NOMINAL_1G_1TJ_CANDIDATES="
        f"{len(candidates)}"
    )

    candidates.sort(
        key=lambda item:
        item[
            "E_inventory_J"
        ]
    )

    shortlist = candidates[
        :8
    ]

    print(
        "\n=== C — EDGE-REGULARIZATION "
        "ROBUSTNESS ==="
    )

    robust_candidates = []

    for nominal in shortlist:

        edge_records = []

        all_success = True

        for width in EDGE_WIDTHS_M:

            width_use = min(
                width,
                nominal[
                    "radius_m"
                ]
                /
                4.0,
            )

            test = evaluate_case(
                nominal[
                    "radius_m"
                ],
                nominal[
                    "factor"
                ],
                tolerance=1.0e-4,
                edge_width=width_use,
            )

            if not test.get(
                "success",
                False,
            ):

                all_success = False

                print(
                    f"EDGE_TEST "
                    f"R_M={nominal['radius_m']:g} "
                    f"FACTOR={nominal['factor']:g} "
                    f"EDGE_M={width_use:g} "
                    f"SUCCESS=False"
                )

                continue

            edge_records.append(
                test
            )

            print(
                f"EDGE_TEST "
                f"R_M={nominal['radius_m']:g} "
                f"FACTOR={nominal['factor']:g} "
                f"EDGE_M={width_use:g} "
                f"E_INV_J="
                f"{test['E_inventory_J']:.9e} "
                f"A_ADVERSE="
                f"{test['a_adverse_surface_mps2']:.9e} "
                f"BACKREACTION="
                f"{test['payload_mass_shift_ratio_rho8000']:.9e}"
            )

        if (
            not all_success
            or
            len(
                edge_records
            )
            ==
            0
        ):

            continue

        maximum_energy = max(
            item[
                "E_inventory_J"
            ]
            for item
            in edge_records
        )

        minimum_adverse = min(
            item[
                "a_adverse_surface_mps2"
            ]
            for item
            in edge_records
        )

        maximum_backreaction = max(
            item[
                "payload_mass_shift_ratio_rho8000"
            ]
            for item
            in edge_records
        )

        energies = np.asarray(
            [
                item[
                    "E_inventory_J"
                ]
                for item
                in edge_records
            ],
            dtype=float,
        )

        energy_spread = (
            (
                np.max(
                    energies
                )
                -
                np.min(
                    energies
                )
            )
            /
            np.mean(
                energies
            )
        )

        robust = (
            maximum_energy
            <=
            TARGET_1TJ_J
            and
            minimum_adverse
            >=
            G0
            and
            maximum_backreaction
            <=
            1.0e-2
            and
            energy_spread
            <=
            0.25
        )

        print(
            f"EDGE_ROBUSTNESS "
            f"R_M={nominal['radius_m']:g} "
            f"FACTOR={nominal['factor']:g} "
            f"MAX_E_INV_J="
            f"{maximum_energy:.9e} "
            f"MIN_A_ADVERSE="
            f"{minimum_adverse:.9e} "
            f"ENERGY_SPREAD="
            f"{energy_spread:.9e} "
            f"PASS={robust}"
        )

        if robust:

            nominal[
                "_edge_max_energy"
            ] = maximum_energy

            nominal[
                "_edge_min_adverse"
            ] = minimum_adverse

            nominal[
                "_edge_energy_spread"
            ] = energy_spread

            robust_candidates.append(
                nominal
            )

    robust_candidates.sort(
        key=lambda item:
        item[
            "_edge_max_energy"
        ]
    )

    best = (
        robust_candidates[
            0
        ]
        if robust_candidates
        else None
    )

    print(
        f"EDGE_ROBUST_1G_1TJ_CANDIDATES="
        f"{len(robust_candidates)}"
    )

    radial_stability_pass = False

    convergence_pass = False

    strong_target = False

    if best is not None:

        print(
            "\n=== D — BEST ROBUST CANDIDATE ==="
        )

        solved = best[
            "_solved"
        ]

        lowest_radial_eigenvalue = (
            radial_hessian_lowest_mode(
                solved
            )
        )

        radial_stability_pass = (
            lowest_radial_eigenvalue
            >
            0.0
        )

        strong_target = (
            best[
                "_edge_max_energy"
            ]
            <=
            TARGET_1E11_J
        )

        print(
            f"BEST_R_M="
            f"{best['radius_m']:.15e}"
        )

        print(
            f"BEST_FACTOR_OVER_CRIT="
            f"{best['factor']:.15e}"
        )

        print(
            f"BEST_ETA="
            f"{best['eta']:.15e}"
        )

        print(
            f"BEST_PHI_CENTER_GEV="
            f"{best['phi_center_gev']:.15e}"
        )

        print(
            f"BEST_ALPHA_X_CENTER="
            f"{best['alpha_x_center']:.15e}"
        )

        print(
            f"BEST_M_M_GEV="
            f"{best['M_m_required_gev']:.15e}"
        )

        print(
            f"BEST_E_ON_J="
            f"{best['E_on_J']:.15e}"
        )

        print(
            f"BEST_E_OFF_J="
            f"{best['E_source_off_J']:.15e}"
        )

        print(
            f"BEST_EDGE_MAX_INVENTORY_J="
            f"{best['_edge_max_energy']:.15e}"
        )

        print(
            f"BEST_A_CM_MPS2="
            f"{best['a_cm_mps2']:.15e}"
        )

        print(
            f"BEST_EDGE_MIN_ADVERSE_MPS2="
            f"{best['_edge_min_adverse']:.15e}"
        )

        print(
            f"BEST_PAYLOAD_BACKREACTION_RATIO="
            f"{best['payload_mass_shift_ratio_rho8000']:.15e}"
        )

        print(
            f"BEST_COMPACTNESS="
            f"{best['compactness']:.15e}"
        )

        print(
            f"RADIAL_HESSIAN_LOWEST_EIGENVALUE_M2INV="
            f"{lowest_radial_eigenvalue:.15e}"
        )

        print(
            f"RADIAL_STABILITY_PASS="
            f"{radial_stability_pass}"
        )

        print(
            "\n=== E — SOLVER CONVERGENCE ==="
        )

        convergence_records = []

        for tolerance in (
            1.0e-3,
            3.0e-4,
            1.0e-4,
            3.0e-5,
        ):

            test = evaluate_case(
                best[
                    "radius_m"
                ],
                best[
                    "factor"
                ],
                tolerance=tolerance,
                edge_width=min(
                    0.050,
                    best[
                        "radius_m"
                    ]
                    /
                    10.0,
                ),
            )

            if not test.get(
                "success",
                False,
            ):

                continue

            convergence_records.append(
                test
            )

            print(
                f"CONVERGENCE "
                f"TOL={tolerance:.1e} "
                f"E_INV_J="
                f"{test['E_inventory_J']:.15e} "
                f"A_CM="
                f"{test['a_cm_mps2']:.15e} "
                f"A_ADVERSE="
                f"{test['a_adverse_surface_mps2']:.15e}"
            )

        if len(
            convergence_records
        ) >= 3:

            energies = np.asarray(
                [
                    row[
                        "E_inventory_J"
                    ]
                    for row
                    in convergence_records[
                        -3:
                    ]
                ]
            )

            accelerations = np.asarray(
                [
                    row[
                        "a_adverse_surface_mps2"
                    ]
                    for row
                    in convergence_records[
                        -3:
                    ]
                ]
            )

            E_rel = (
                np.max(
                    energies
                )
                -
                np.min(
                    energies
                )
            ) / np.mean(
                energies
            )

            A_rel = (
                np.max(
                    accelerations
                )
                -
                np.min(
                    accelerations
                )
            ) / np.mean(
                accelerations
            )

            convergence_pass = (
                E_rel
                <=
                5.0e-3
                and
                A_rel
                <=
                5.0e-3
            )

            print(
                f"CONVERGENCE_E_REL_SPREAD="
                f"{E_rel:.15e}"
            )

            print(
                f"CONVERGENCE_A_REL_SPREAD="
                f"{A_rel:.15e}"
            )

        print(
            f"CONVERGENCE_PASS="
            f"{convergence_pass}"
        )

    print(
        "\n=== F — DECISION ==="
    )

    if best is None:

        classification = (
            "RED_NO_EDGE_ROBUST_1G_1TJ_"
            "SINGLE_SIGN_Z2_BVP"
        )

        next_step = (
            "DIAGNOSE_Z2_PARAMETER_SCALING_"
            "BEFORE_MICROSCOPIC_SOURCE_WORK"
        )

    elif not radial_stability_pass:

        classification = (
            "RED_Z2_BVP_RADIAL_INSTABILITY"
        )

        next_step = (
            "DIAGNOSE_RADIAL_MODE"
        )

    elif not convergence_pass:

        classification = (
            "YELLOW_Z2_BVP_NOT_NUMERICALLY_CONVERGED"
        )

        next_step = (
            "031A_R4R_CONVERGENCE_AND_EDGE_REFINEMENT"
        )

    elif strong_target:

        classification = (
            "GREEN_Z2_FIELD_EQUATION_"
            "SURVIVES_1E11_STRONG_TARGET"
        )

        next_step = (
            "031B1_B7_SCALAR_CHARGE_DRESSING_"
            "PLUS_031B2_QBALL_CONTROL"
        )

    else:

        classification = (
            "GREEN_Z2_FIELD_EQUATION_"
            "SURVIVES_1TJ_TARGET_"
            "STRONG_1E11_MARGIN_LOST"
        )

        next_step = (
            "031B1_B7_SCALAR_CHARGE_DRESSING_"
            "PLUS_031B2_QBALL_CONTROL"
        )

    print(
        f"R4_SCALAR_FIELD_EXISTS="
        f"{best is not None}"
    )

    print(
        f"R4_TRUE_STANDOFF="
        f"{best is not None}"
    )

    print(
        f"R4_FINITE_PAYLOAD_1G_ALL_SURFACE="
        f"{best is not None}"
    )

    print(
        f"R4_RADIAL_STABILITY="
        f"{radial_stability_pass}"
    )

    print(
        f"R4_CONVERGENCE="
        f"{convergence_pass}"
    )

    print(
        f"R4_1TJ_TARGET="
        f"{best is not None}"
    )

    print(
        f"R4_1E11_TARGET="
        f"{strong_target}"
    )

    print(
        "R4_FULL_SOURCE_REALIZATION="
        "NO"
    )

    print(
        "R4_FULL_LOCAL_CONSERVATION="
        "NO"
    )

    print(
        "R4_NONAXISYMMETRIC_STABILITY="
        "NOT_TESTED"
    )

    print(
        "R4_EFT_NATURALNESS="
        "NOT_CLOSED"
    )

    print(
        f"031A_R4_CLASSIFICATION="
        f"{classification}"
    )

    print(
        f"NEXT="
        f"{next_step}"
    )

    csv_path = (
        RESULTS
        /
        "031a_r4_z2_induced_scalarization_scan.csv"
    )

    public_rows = [
        row
        for row
        in rows
        if row
    ]

    if public_rows:

        keys = []

        for row in public_rows:

            for key in row:

                if key not in keys:

                    keys.append(
                        key
                    )

        with csv_path.open(
            "w",
            newline="",
        ) as handle:

            writer = csv.DictWriter(
                handle,
                fieldnames=keys,
                extrasaction="ignore",
            )

            writer.writeheader()

            writer.writerows(
                public_rows
            )

    summary = {
        "claim_class":
        "NONLINEAR_SCALAR_FIELD_EXISTENCE_PREFLIGHT",

        "practical_device":
        False,

        "scalar_charge_prescribed":
        False,

        "external_X_density_profile":
        True,

        "full_local_conservation":
        False,

        "mediator_range_m":
        MEDIATOR_RANGE_M,

        "M_X_gev":
        M_X_GEV,

        "alpha_m_payload_cap":
        ALPHA_M_PAYLOAD_CAP,

        "nominal_candidates":
        len(
            candidates
        ),

        "edge_robust_candidates":
        len(
            robust_candidates
        ),

        "best":
        (
            None
            if best is None
            else public_row(
                best
            )
        ),

        "radial_stability_pass":
        radial_stability_pass,

        "convergence_pass":
        convergence_pass,

        "strong_1e11_target":
        strong_target,

        "classification":
        classification,

        "next":
        next_step,
    }

    summary_path = (
        RESULTS
        /
        "031a_r4_z2_induced_scalarization_summary.json"
    )

    summary_path.write_text(
        json.dumps(
            summary,
            indent=2,
        )
        +
        "\n"
    )

    print(
        f"SUMMARY_JSON="
        f"{summary_path.resolve()}"
    )

    print(
        f"SCAN_CSV="
        f"{csv_path.resolve()}"
    )


if __name__ == "__main__":
    main()
