#!/usr/bin/env python3
"""Simulation 018B-0G — two-current fixed-background 2D junction + conservative corrected scout.

PURPOSE
-------
Rebuild the KLS string-wall junction on the literature-backed two-current
Lilley-Martin-Peter microscopic string selected by 018B-0D and connected to
the KLS wall by 018B-0F0.

This is the last fixed-background/backreaction preflight before releasing all
new two-current junction fields simultaneously.

ACTIVE SCIENTIFIC QUESTION
--------------------------
Does the new two-current string admit a finite localized charge-1 KLS wall
termination in its own charge-2 Higgs/gauge background, with numerically
controlled junction energy/active source and sufficiently small frozen-field
backreaction that a fully coupled 2D solve is justified?

A second conservative question is asked immediately: if the measured junction
penalties are deliberately inflated, does at least one exact dual-integer
stationary loop still satisfy wall balance, positive total active mass, and
finite-payload outward gravity?

MODEL
-----
The underlying two-current string is the published Abelian model reproduced in
018B-0D. Its transverse profiles depend on the Lorentz scalars

    w_Phi   = k_Phi^2   - omega_Phi^2
    w_Sigma = k_Sigma^2 - omega_Sigma^2.

The 018B-0F stationary state is a boost of this same worldsheet state, so these
invariants and therefore the local transverse BVP are unchanged by the large
laboratory-frame current momentum.

The KLS bridge from 018B-0F0 uses

    Q_H = 2,
    Q_A = 1,
    g_X = q / 2,

and the gauge-invariant phase-lock interaction

    -h (H^* A^2 + H A^{*2}).

The full added potential density is

    V_ext = lambda_A/4 (|A|^2-F^2)^2
            - h (H^* A^2 + H A^{*2})
            + c_H (|H|^2-1)
            + c_A (|A|^2-F^2)
            + V_0,

with

    c_H = h F^2,
    c_A = 2 h,
    V_0 = 2 h F^2.

At the intended vacuum H=1, A=F the potential is exactly zero.

NUMERICAL METHOD
----------------
1. Independently reconstruct the two-current radial BVP on domains 40, 60,
   and 80 and compare the domain-80 condensate integrals/core amplitudes with
   the already executed 018B-0D log.

2. Freeze that converged H/gauge background and solve the complex A field on a
   Cartesian lattice using compact U(1) link transport. Boundary data enforce
   the half-winding phase A ~ F exp(i theta/2) and a smooth branch-wall zero on
   the negative x axis.

3. Use several resolutions at fixed domain and several domains at fixed dx.
   The long planar wall contribution is subtracted, leaving a finite junction
   excess. Linear/quadratic/cubic dx->0 extrapolations are compared instead
   of promoting one grid value.

4. Audit the frozen-field H source and A-induced gauge-link current relative
   to the original charged-Higgs current.

5. Inflate the measured junction energy and positive active source before
   re-running the exact-integer stationary scout. A pass under this adverse
   bound authorizes, but does not replace, the fully coupled junction solve.

SIGN / STRESS CONVENTIONS
-------------------------
For the static transverse A extension, the added line energy mu_J contributes
longitudinal pressure approximately -mu_J. It therefore reduces the rim's
available positive compression. The integrated gravitoelectric active source
is computed directly from the fixed-background scalar extension as

    Lambda_J = -2 integral V_ext d^2x - Lambda_wall * L.

The conservative corrected stationary scout uses

    P_available = P_rim - mu_J,bound,
    E_line      = E_rim + mu_J,bound,
    A_line      = A_rim + Lambda_J,bound.

APPROXIMATION LEVEL
-------------------
This is NOT the final junction. H, Phi, Sigma, and the gauge field are frozen
in the 2D junction solve. Their induced sources are measured explicitly.
A GREEN result only authorizes the fully coupled matched-lattice continuation.

VALIDATION / FALSIFICATION
--------------------------
Require:
- upstream 018B-0D, 018B-0F0, and 018B-0F GREEN markers;
- independent two-current radial BVP reconstruction;
- finite localized 2D junction;
- controlled dx extrapolation and domain trend;
- one-sided wall termination and gauge-invariant phase locking;
- small H and gauge backreaction diagnostics;
- a conservative junction-penalized exact-integer stationary candidate;
- positive far active mass and adverse finite-payload outward gravity.

If any of these fail, do not proceed blindly to a global toroidal solve.

CLAIM LIMITS
------------
A GREEN result does not establish a fully coupled two-current junction, a
curved microscopic ring, complete loop stability, frame dragging, a global
Euler-Lagrange torus, nonlinear Einstein-matter consistency, practical energy
scaling, or a practical antigravity device.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_018B0G_TWO_CURRENT_FIXED_BACKGROUND_JUNCTION_AND_BACKREACTION_PREFLIGHT
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import importlib.util
import math
from pathlib import Path
import re
import sys

import numpy as np
from scipy.integrate import simpson, solve_bvp
from scipy.optimize import minimize, minimize_scalar


ROOT = Path(__file__).resolve().parents[1]

D_LOG = (
    ROOT
    / "results/logs"
    / "018b0d_literature_two_current_counterflow_gate.log"
)

F0_LOG = (
    ROOT
    / "results/logs"
    / "018b0f0_lilley_kls_same_gauge_normalization_wall_bridge.log"
)

F_LOG = (
    ROOT
    / "results/logs"
    / "018b0f_stationary_two_current_integer_wall_balance_gravity_scout.log"
)

F_SOURCE = (
    ROOT
    / "simulations"
    / "018b0f_stationary_two_current_integer_wall_balance_gravity_scout.py"
)


F_A = 0.075
H_LOCK = 0.010
LAMBDA_A = 1.0

C_H = H_LOCK * F_A * F_A
C_A = 2.0 * H_LOCK
V0 = 2.0 * H_LOCK * F_A * F_A

PLANAR_FIXED_SIGMA = (
    4.0
    /
    3.0
    *
    F_A**3
    *
    math.sqrt(
        LAMBDA_A
    )
)

WALL_INV_LENGTH = (
    F_A
    *
    math.sqrt(
        LAMBDA_A
    )
    /
    2.0
)

WALL_LENGTH = (
    1.0
    /
    WALL_INV_LENGTH
)


RADIAL_DOMAINS = (
    40.0,
    60.0,
    80.0,
)

RESOLUTION_CASES = (
    (81, 60.0),
    (121, 60.0),
    (161, 60.0),
    (201, 60.0),
)

DOMAIN_CASES = (
    (101, 50.0),
    (121, 60.0),
    (161, 80.0),
)


MAX_BVP_RMS = 5.0e-5
MAX_RADIAL_REFERENCE_RELERR = 5.0e-4

MAX_A_GRAD_RMS = 5.0e-6
MAX_A_GRAD_MAX = 5.0e-5

MAX_EXTRAPOLATION_SPREAD_FRACTION = 2.0e-2
MAX_DOMAIN_SHIFT_FRACTION = 1.0e-2

MAX_H_SOURCE = 1.0e-3
MAX_GAUGE_CURRENT_RATIO = 5.0e-2

MAX_NEGATIVE_TO_POSITIVE_AXIS_RATIO = 2.0e-2
MIN_PHASE_LOCK_COS = 0.995


# Deliberately adverse inflation before the corrected source-level scout.
JUNCTION_ENERGY_INFLATION = 1.25
JUNCTION_ACTIVE_INFLATION = 1.50


@dataclass
class Parameters:
    """Published two-current microscopic parameters in the chosen units."""

    q: float

    lambda_phi: float
    lambda_sigma: float

    g: float

    m_phi_sq: float
    m_sigma_sq: float

    f_phi: float
    f_sigma: float

    omega_phi: float
    k_phi: float

    omega_sigma: float
    k_sigma: float


@dataclass
class LatticeProblem:
    """One fixed-background compact-link complex-A junction problem."""

    n: int
    box_half: float
    dx: float

    x: np.ndarray

    X: np.ndarray
    Z: np.ndarray

    radius: np.ndarray
    theta: np.ndarray

    H: np.ndarray
    Q: np.ndarray

    ux: np.ndarray
    uz: np.ndarray

    weights: np.ndarray

    fixed: np.ndarray
    interior: tuple[np.ndarray, np.ndarray]

    boundary: np.ndarray
    initial: np.ndarray


def load_module(
    name: str,
    path: Path,
):
    """Import a local simulation module without invoking main()."""

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


def require_marker(
    path: Path,
    marker: str,
) -> None:
    """Require one upstream scientific GREEN marker."""

    if not path.exists():

        raise RuntimeError(
            f"Missing upstream log: {path}"
        )

    if marker not in path.read_text(
        errors="replace"
    ):

        raise RuntimeError(
            f"Missing upstream marker {marker!r} in {path}"
        )


def scalar(
    path: Path,
    label: str,
) -> float:
    """Read one finite scalar after an exact label."""

    text = path.read_text(
        errors="replace"
    )

    number = (
        r"([+-]?"
        r"(?:\d+(?:\.\d*)?|\.\d+)"
        r"(?:[eE][+-]?\d+)?)"
    )

    match = re.search(
        re.escape(
            label
        )
        +
        number,
        text,
    )

    if match is None:

        raise RuntimeError(
            f"Missing {label!r} in {path}"
        )

    value = float(
        match.group(
            1
        )
    )

    if not math.isfinite(
        value
    ):

        raise RuntimeError(
            f"Nonfinite {label!r} in {path}"
        )

    return value


def domain80_reference(
    path: Path,
) -> dict[str, float]:
    """Read the DOMAIN=80 reconstruction diagnostics from 018B-0D."""

    text = path.read_text(
        errors="replace"
    )

    match = re.search(
        r"DOMAIN=80\s+"
        r"A=([^\s]+)\s+"
        r"I_PHI=([^\s]+)\s+"
        r"I_SIGMA=([^\s]+)\s+"
        r"PHI0=([^\s]+)\s+"
        r"SIGMA0=([^\s]+)\s+"
        r"MAX_RMS_RESIDUAL=([^\s]+)",
        text,
    )

    if match is None:

        raise RuntimeError(
            "Could not reconstruct 018B-0D DOMAIN=80 reference"
        )

    keys = (
        "A",
        "I_PHI",
        "I_SIGMA",
        "PHI0",
        "SIGMA0",
        "RMS",
    )

    return {
        key:
            float(
                value
            )

        for key, value
        in zip(
            keys,
            match.groups(),
        )
    }


def load_parameters() -> Parameters:
    """Load the already reconstructed physical parameters from current logs."""

    return Parameters(

        q=math.sqrt(
            scalar(
                F0_LOG,
                "QTILDE_SQ=",
            )
        ),

        lambda_phi=scalar(
            F0_LOG,
            "LAMBDA_PHI=",
        ),

        lambda_sigma=scalar(
            F0_LOG,
            "LAMBDA_SIGMA=",
        ),

        g=scalar(
            F0_LOG,
            "G=",
        ),

        m_phi_sq=scalar(
            F0_LOG,
            "M_PHI_SQ=",
        ),

        m_sigma_sq=scalar(
            F0_LOG,
            "M_SIGMA_SQ=",
        ),

        f_phi=scalar(
            F0_LOG,
            "F_PHI=",
        ),

        f_sigma=scalar(
            F0_LOG,
            "F_SIGMA=",
        ),

        omega_phi=scalar(
            D_LOG,
            "OMEGA_PHI=",
        ),

        k_phi=scalar(
            D_LOG,
            "K_PHI=",
        ),

        omega_sigma=scalar(
            D_LOG,
            "OMEGA_SIGMA=",
        ),

        k_sigma=scalar(
            D_LOG,
            "K_SIGMA=",
        ),
    )


def solve_radial(
    parameters: Parameters,
    domain: float,
):
    """Independently solve the published two-current straight-string BVP."""

    eps = 1.0e-4

    r = np.linspace(
        eps,
        domain,
        max(
            500,
            int(
                domain
                *
                10
            ),
        ),
    )

    h0 = np.tanh(
        r
        /
        2.0
    )

    hp0 = (
        0.5
        /
        np.cosh(
            r
            /
            2.0
        ) ** 2
    )

    Q0 = np.exp(
        -0.5
        *
        (
            parameters.q
            *
            r
        ) ** 2
    )

    Qp0 = (
        -parameters.q**2
        *
        r
        *
        Q0
    )

    phi0 = (
        0.38356708
        *
        np.exp(
            -r
            /
            8.0
        )
    )

    phip0 = (
        -phi0
        /
        8.0
    )

    sigma0 = (
        0.32597385
        *
        np.exp(
            -r
            /
            8.0
        )
    )

    sigmap0 = (
        -sigma0
        /
        8.0
    )

    guess = np.vstack(
        (
            h0,
            hp0,
            Q0,
            Qp0,
            phi0,
            phip0,
            sigma0,
            sigmap0,
        )
    )

    w_phi = (
        parameters.k_phi**2
        -
        parameters.omega_phi**2
    )

    w_sigma = (
        parameters.k_sigma**2
        -
        parameters.omega_sigma**2
    )

    def ode(
        rr,
        y,
    ):

        (
            H,
            Hp,
            Q,
            Qp,
            Phi,
            Phip,
            Sigma,
            Sigmap,
        ) = y

        return np.vstack(
            (
                Hp,

                -Hp
                /
                rr
                +
                (
                    Q**2
                    /
                    rr**2

                    +

                    0.5
                    *
                    (
                        H**2
                        -
                        1.0
                    )

                    +

                    parameters.f_phi
                    *
                    Phi**2

                    +

                    parameters.f_sigma
                    *
                    Sigma**2
                )
                *
                H,

                Qp,

                Qp
                /
                rr

                +

                parameters.q**2
                *
                H**2
                *
                Q,

                Phip,

                -Phip
                /
                rr

                +

                (
                    w_phi

                    +

                    parameters.f_phi
                    *
                    (
                        H**2
                        -
                        1.0
                    )

                    +

                    parameters.m_phi_sq

                    +

                    parameters.lambda_phi
                    *
                    Phi**2

                    +

                    parameters.g
                    *
                    Sigma**2
                )
                *
                Phi,

                Sigmap,

                -Sigmap
                /
                rr

                +

                (
                    w_sigma

                    +

                    parameters.f_sigma
                    *
                    (
                        H**2
                        -
                        1.0
                    )

                    +

                    parameters.m_sigma_sq

                    +

                    parameters.lambda_sigma
                    *
                    Sigma**2

                    +

                    parameters.g
                    *
                    Phi**2
                )
                *
                Sigma,
            )
        )

    def bc(
        ya,
        yb,
    ):

        return np.array(
            [
                ya[
                    0
                ],

                ya[
                    2
                ]
                -
                1.0,

                ya[
                    5
                ],

                ya[
                    7
                ],

                yb[
                    0
                ]
                -
                1.0,

                yb[
                    2
                ],

                yb[
                    4
                ],

                yb[
                    6
                ],
            ],
            dtype=float,
        )

    solution = solve_bvp(
        ode,
        bc,
        r,
        guess,
        tol=1.0e-5,
        max_nodes=30000,
    )

    if solution.status != 0:

        raise RuntimeError(
            f"Radial BVP failed on domain {domain}: "
            f"{solution.message}"
        )

    dense = np.linspace(
        eps,
        domain,
        8001,
    )

    (
        H,
        _,
        _,
        _,
        Phi,
        _,
        Sigma,
        _,
    ) = solution.sol(
        dense
    )

    del H

    # Match the 018B-0D convention: these radial condensate integrals do not
    # include the later 2*pi angular factor.
    i_phi = float(
        simpson(
            dense
            *
            Phi**2,
            x=dense,
        )
    )

    i_sigma = float(
        simpson(
            dense
            *
            Sigma**2,
            x=dense,
        )
    )

    return {
        "solution":
            solution,

        "max_rms":
            float(
                np.max(
                    solution.rms_residuals
                )
            ),

        "i_phi":
            i_phi,

        "i_sigma":
            i_sigma,

        "phi0":
            float(
                solution.sol(
                    eps
                )[
                    4
                ]
            ),

        "sigma0":
            float(
                solution.sol(
                    eps
                )[
                    6
                ]
            ),

        "w_phi":
            w_phi,

        "w_sigma":
            w_sigma,
    }


def boundary_field(
    X: np.ndarray,
    Z: np.ndarray,
) -> np.ndarray:
    """Construct a smooth asymptotic half-winding field with one branch wall."""

    theta = np.arctan2(
        Z,
        X,
    )

    suppression = np.ones_like(
        X,
        dtype=float,
    )

    negative = (
        X
        <
        0.0
    )

    suppression[
        negative
    ] = np.tanh(
        np.abs(
            Z[
                negative
            ]
        )
        /
        WALL_LENGTH
    )

    result = (
        F_A
        *
        np.exp(
            0.5j
            *
            theta
        )
        *
        suppression
    )

    result[
        np.hypot(
            X,
            Z,
        )
        <
        1.0e-14
    ] = 0.0

    return result


def build_problem(
    radial_solution,
    n: int,
    box_half: float,
) -> LatticeProblem:
    """Build one fixed-background complex-A junction lattice."""

    x = np.linspace(
        -box_half,
        box_half,
        n,
    )

    dx = float(
        x[
            1
        ]
        -
        x[
            0
        ]
    )

    X, Z = np.meshgrid(
        x,
        x,
        indexing="ij",
    )

    radius = np.hypot(
        X,
        Z,
    )

    theta = np.arctan2(
        Z,
        X,
    )

    rr = np.maximum(
        radius,
        radial_solution.x[
            0
        ],
    )

    clipped = np.minimum(
        rr,
        radial_solution.x[
            -1
        ],
    )

    radial = radial_solution.sol(
        clipped
    )

    H_amp = np.array(
        radial[
            0
        ],
        copy=True,
    )

    Q = np.array(
        radial[
            2
        ],
        copy=True,
    )

    outside = (
        radius
        >
        radial_solution.x[
            -1
        ]
    )

    H_amp[
        outside
    ] = 1.0

    Q[
        outside
    ] = 0.0

    H = (
        H_amp
        *
        np.exp(
            1j
            *
            theta
        )
    )

    # q_A / q_H = 1/2.
    dtheta_x = np.angle(
        np.exp(
            1j
            *
            (
                theta[
                    1:,
                    :
                ]
                -
                theta[
                    :-1,
                    :
                ]
            )
        )
    )

    qmid_x = (
        0.5
        *
        (
            Q[
                1:,
                :
            ]
            +
            Q[
                :-1,
                :
            ]
        )
    )

    ux = np.exp(
        0.5j
        *
        (
            qmid_x
            -
            1.0
        )
        *
        dtheta_x
    )

    dtheta_z = np.angle(
        np.exp(
            1j
            *
            (
                theta[
                    :,
                    1:
                ]
                -
                theta[
                    :,
                    :-1
                ]
            )
        )
    )

    qmid_z = (
        0.5
        *
        (
            Q[
                :,
                1:
            ]
            +
            Q[
                :,
                :-1
            ]
        )
    )

    uz = np.exp(
        0.5j
        *
        (
            qmid_z
            -
            1.0
        )
        *
        dtheta_z
    )

    boundary = boundary_field(
        X,
        Z,
    )

    gate = (
        0.5
        *
        (
            1.0
            -
            np.tanh(
                X
                /
                2.0
            )
        )
    )

    suppression = (
        1.0

        -

        gate
        *
        (
            1.0

            -

            np.tanh(
                np.abs(
                    Z
                )
                /
                WALL_LENGTH
            )
        )
    )

    initial = (
        F_A
        *
        np.exp(
            0.5j
            *
            theta
        )
        *
        suppression
    )

    initial[
        radius
        <
        0.5
        *
        dx
    ] = 0.0

    fixed = np.zeros(
        (
            n,
            n,
        ),
        dtype=bool,
    )

    fixed[
        [
            0,
            -1,
        ],
        :
    ] = True

    fixed[
        :,
        [
            0,
            -1,
        ]
    ] = True

    initial[
        fixed
    ] = boundary[
        fixed
    ]

    weights = np.ones(
        (
            n,
            n,
        ),
        dtype=float,
    )

    weights[
        [
            0,
            -1,
        ],
        :
    ] *= 0.5

    weights[
        :,
        [
            0,
            -1,
        ]
    ] *= 0.5

    return LatticeProblem(
        n=n,
        box_half=box_half,
        dx=dx,

        x=x,

        X=X,
        Z=Z,

        radius=radius,
        theta=theta,

        H=H,
        Q=Q,

        ux=ux,
        uz=uz,

        weights=weights,

        fixed=fixed,
        interior=np.where(
            ~fixed
        ),

        boundary=boundary,
        initial=initial,
    )


def pack(
    problem: LatticeProblem,
    field: np.ndarray,
) -> np.ndarray:
    """Pack free complex A sites into one real optimizer vector."""

    values = field[
        problem.interior
    ]

    return np.concatenate(
        (
            values.real,
            values.imag,
        )
    )


def unpack(
    problem: LatticeProblem,
    variables: np.ndarray,
) -> np.ndarray:
    """Restore one real optimizer vector to the full complex lattice."""

    field = np.array(
        problem.boundary,
        copy=True,
    )

    count = (
        problem.interior[
            0
        ].size
    )

    field[
        problem.interior
    ] = (
        variables[
            :count
        ]

        +

        1j
        *
        variables[
            count:
        ]
    )

    return field


def extension_potential(
    problem: LatticeProblem,
    field: np.ndarray,
) -> np.ndarray:
    """Return the complete added KLS potential density."""

    amplitude_sq = (
        np.abs(
            field
        ) ** 2
    )

    phase_lock = (
        np.conj(
            problem.H
        )
        *
        field**2

        +

        problem.H
        *
        np.conj(
            field
        ) ** 2
    ).real

    return (
        0.25
        *
        LAMBDA_A
        *
        (
            amplitude_sq
            -
            F_A**2
        ) ** 2

        -

        H_LOCK
        *
        phase_lock

        +

        C_H
        *
        (
            np.abs(
                problem.H
            ) ** 2
            -
            1.0
        )

        +

        C_A
        *
        (
            amplitude_sq
            -
            F_A**2
        )

        +

        V0
    )


def objective_and_gradient(
    problem: LatticeProblem,
    variables: np.ndarray,
):
    """Return lattice energy and exact analytic gradient for complex A."""

    field = unpack(
        problem,
        variables,
    )

    gradient_complex = np.zeros_like(
        field,
        dtype=complex,
    )

    dx_link = (
        problem.ux
        *
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

    dz_link = (
        problem.uz
        *
        field[
            :,
            1:
        ]

        -

        field[
            :,
            :-1
        ]
    )

    kinetic = float(
        np.sum(
            np.abs(
                dx_link
            ) ** 2
        )

        +

        np.sum(
            np.abs(
                dz_link
            ) ** 2
        )
    )

    gradient_complex[
        :-1,
        :
    ] += (
        -dx_link
    )

    gradient_complex[
        1:,
        :
    ] += (
        np.conj(
            problem.ux
        )
        *
        dx_link
    )

    gradient_complex[
        :,
        :-1
    ] += (
        -dz_link
    )

    gradient_complex[
        :,
        1:
    ] += (
        np.conj(
            problem.uz
        )
        *
        dz_link
    )

    amplitude_sq = (
        np.abs(
            field
        ) ** 2
    )

    potential = extension_potential(
        problem,
        field,
    )

    potential_energy = float(
        problem.dx**2
        *
        np.sum(
            problem.weights
            *
            potential
        )
    )

    potential_gradient = (
        0.5
        *
        LAMBDA_A
        *
        (
            amplitude_sq
            -
            F_A**2
        )
        *
        field

        -

        2.0
        *
        H_LOCK
        *
        problem.H
        *
        np.conj(
            field
        )

        +

        C_A
        *
        field
    )

    gradient_complex += (
        problem.dx**2
        *
        problem.weights
        *
        potential_gradient
    )

    local = gradient_complex[
        problem.interior
    ]

    gradient = np.concatenate(
        (
            2.0
            *
            local.real,

            2.0
            *
            local.imag,
        )
    )

    return (
        kinetic
        +
        potential_energy,
        gradient,
    )


def solve_lattice(
    radial_solution,
    n: int,
    box_half: float,
):
    """Relax one A-only fixed-background junction lattice."""

    problem = build_problem(
        radial_solution,
        n,
        box_half,
    )

    variables = pack(
        problem,
        problem.initial,
    )

    result = minimize(
        lambda values:
            objective_and_gradient(
                problem,
                values,
            ),

        variables,

        jac=True,

        method="L-BFGS-B",

        options={
            "maxiter":
                1200,

            "ftol":
                1.0e-12,

            "gtol":
                1.0e-8,

            "maxls":
                40,
        },
    )

    energy, gradient = (
        objective_and_gradient(
            problem,
            result.x,
        )
    )

    field = unpack(
        problem,
        result.x,
    )

    potential = extension_potential(
        problem,
        field,
    )

    gradient_rms = float(
        math.sqrt(
            np.mean(
                gradient**2
            )
        )
    )

    gradient_max = float(
        np.max(
            np.abs(
                gradient
            )
        )
    )

    junction_energy = float(
        energy

        -

        PLANAR_FIXED_SIGMA
        *
        box_half
    )

    active_total = float(
        -2.0
        *
        problem.dx**2
        *
        np.sum(
            problem.weights
            *
            potential
        )
    )

    junction_active = float(
        active_total

        +

        PLANAR_FIXED_SIGMA
        *
        box_half
    )

    iz0 = int(
        np.argmin(
            np.abs(
                problem.x
            )
        )
    )

    ix_negative = int(
        np.argmin(
            np.abs(
                problem.x
                +
                0.5
                *
                box_half
            )
        )
    )

    ix_positive = int(
        np.argmin(
            np.abs(
                problem.x
                -
                0.5
                *
                box_half
            )
        )
    )

    negative_axis = float(
        abs(
            field[
                ix_negative,
                iz0
            ]
        )
    )

    positive_axis = float(
        abs(
            field[
                ix_positive,
                iz0
            ]
        )
    )

    axis_ratio = (
        negative_axis
        /
        max(
            positive_axis,
            1.0e-30,
        )
    )

    phase = (
        2.0
        *
        np.angle(
            field
        )

        -

        np.angle(
            problem.H
        )
    )

    phase_cos = np.cos(
        phase
    )

    lock_mask = (
        (
            problem.radius
            >
            10.0
        )

        &

        ~(
            (
                problem.X
                <
                0.0
            )

            &

            (
                np.abs(
                    problem.Z
                )
                <
                15.0
            )
        )
    )

    phase_lock_p01 = float(
        np.percentile(
            phase_cos[
                lock_mask
            ],
            1.0,
        )
    )

    # Frozen-field H source from dV_ext / dH*.
    h_source = (
        -H_LOCK
        *
        field**2

        +

        C_H
        *
        problem.H
    )

    h_source_max = float(
        np.max(
            np.abs(
                h_source
            )
        )
    )

    h_source_rms = float(
        math.sqrt(
            np.mean(
                np.abs(
                    h_source
                ) ** 2
            )
        )
    )

    # Compare A-induced and original-H link currents with respect to the same
    # fundamental gauge-link phase.
    da_x = (
        problem.ux
        *
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

    da_z = (
        problem.uz
        *
        field[
            :,
            1:
        ]

        -

        field[
            :,
            :-1
        ]
    )

    j_a_x = (
        0.5
        *
        2.0
        *
        np.real(
            np.conj(
                da_x
            )
            *
            (
                1j
                *
                problem.ux
                *
                field[
                    1:,
                    :
                ]
            )
        )
    )

    j_a_z = (
        0.5
        *
        2.0
        *
        np.real(
            np.conj(
                da_z
            )
            *
            (
                1j
                *
                problem.uz
                *
                field[
                    :,
                    1:
                ]
            )
        )
    )

    uh_x = (
        problem.ux**2
    )

    uh_z = (
        problem.uz**2
    )

    d_h_x = (
        uh_x
        *
        problem.H[
            1:,
            :
        ]

        -

        problem.H[
            :-1,
            :
        ]
    )

    d_h_z = (
        uh_z
        *
        problem.H[
            :,
            1:
        ]

        -

        problem.H[
            :,
            :-1
        ]
    )

    j_h_x = np.real(
        np.conj(
            d_h_x
        )
        *
        (
            1j
            *
            uh_x
            *
            problem.H[
                1:,
                :
            ]
        )
    )

    j_h_z = np.real(
        np.conj(
            d_h_z
        )
        *
        (
            1j
            *
            uh_z
            *
            problem.H[
                :,
                1:
            ]
        )
    )

    a_current_l2 = float(
        math.sqrt(
            np.sum(
                j_a_x**2
            )

            +

            np.sum(
                j_a_z**2
            )
        )
    )

    h_current_l2 = float(
        math.sqrt(
            np.sum(
                j_h_x**2
            )

            +

            np.sum(
                j_h_z**2
            )
        )
    )

    current_ratio = (
        a_current_l2
        /
        max(
            h_current_l2,
            1.0e-30,
        )
    )

    passed = (
        gradient_rms
        <=
        MAX_A_GRAD_RMS

        and

        gradient_max
        <=
        MAX_A_GRAD_MAX

        and

        junction_energy
        >
        0.0

        and

        axis_ratio
        <=
        MAX_NEGATIVE_TO_POSITIVE_AXIS_RATIO

        and

        phase_lock_p01
        >=
        MIN_PHASE_LOCK_COS
    )

    return {
        "passed":
            passed,

        "optimizer_success":
            bool(
                result.success
            ),

        "n":
            n,

        "box_half":
            box_half,

        "dx":
            problem.dx,

        "energy":
            float(
                energy
            ),

        "junction_energy":
            junction_energy,

        "junction_active":
            junction_active,

        "gradient_rms":
            gradient_rms,

        "gradient_max":
            gradient_max,

        "axis_ratio":
            axis_ratio,

        "phase_lock_p01":
            phase_lock_p01,

        "h_source_max":
            h_source_max,

        "h_source_rms":
            h_source_rms,

        "a_current_l2":
            a_current_l2,

        "h_current_l2":
            h_current_l2,

        "current_ratio":
            current_ratio,

        "iterations":
            int(
                result.nit
            ),
    }


def extrapolated_estimate(
    results: list[dict],
    key: str,
):
    """Compare linear/quadratic/cubic dx -> 0 extrapolations."""

    ordered = sorted(
        results,
        key=lambda row:
            row[
                "dx"
            ],
        reverse=True,
    )

    x = np.array(
        [
            row[
                "dx"
            ]
            for row
            in ordered
        ],
        dtype=float,
    )

    y = np.array(
        [
            row[
                key
            ]
            for row
            in ordered
        ],
        dtype=float,
    )

    estimates = []

    for degree in (
        1,
        2,
        3,
    ):

        fit = np.polyfit(
            x,
            y,
            degree,
        )

        estimates.append(
            float(
                np.polyval(
                    fit,
                    0.0,
                )
            )
        )

    central = float(
        np.median(
            estimates
        )
    )

    spread = float(
        max(
            estimates
        )
        -
        min(
            estimates
        )
    )

    spread_fraction = (
        spread
        /
        max(
            abs(
                central
            ),
            1.0e-30,
        )
    )

    return (
        central,
        spread_fraction,
        tuple(
            estimates
        ),
    )


def corrected_integer_search(
    scout,
    state,
    wall,
    mu_bound: float,
    active_bound: float,
):
    """Repeat 018B-0F with conservative localized junction penalties."""

    found = []

    ct2 = (
        state.T
        /
        state.U
    )

    for base_phi in range(
        -scout.BASE_WINDING_MAX,
        scout.BASE_WINDING_MAX
        +
        1,
    ):

        if base_phi == 0:
            continue

        for base_sigma in range(
            -scout.BASE_WINDING_MAX,
            scout.BASE_WINDING_MAX
            +
            1,
        ):

            if (
                base_sigma == 0

                or

                math.gcd(
                    abs(
                        base_phi
                    ),
                    abs(
                        base_sigma
                    ),
                )
                !=
                1
            ):
                continue

            v = scout.exact_v(
                state,
                base_phi,
                base_sigma,
            )

            if (
                v is None

                or

                not math.isfinite(
                    v
                )

                or

                abs(
                    v
                )
                >=
                scout.MAX_ABS_V
            ):
                continue

            if (
                v
                *
                v
                <=
                ct2
            ):
                continue

            (
                gamma,

                omega_phi_lab,
                k_phi_lab,

                omega_sigma_lab,
                k_sigma_lab,

                energy,
                pressure,
                momentum,
                active,
            ) = scout.boost(
                state,
                v,
            )

            pressure_available = (
                pressure
                -
                mu_bound
            )

            if (
                pressure_available
                <=
                0.0

                or

                active
                <=
                0.0
            ):
                continue

            if (
                abs(
                    k_phi_lab
                )
                <
                1.0e-15

                or

                abs(
                    k_sigma_lab
                )
                <
                1.0e-15
            ):
                continue

            r_phi_unit = (
                base_phi
                /
                k_phi_lab
            )

            r_sigma_unit = (
                base_sigma
                /
                k_sigma_lab
            )

            if (
                r_phi_unit
                <=
                0.0

                or

                r_sigma_unit
                <=
                0.0
            ):
                continue

            if (
                abs(
                    r_phi_unit
                    -
                    r_sigma_unit
                )
                /
                max(
                    r_phi_unit,
                    r_sigma_unit,
                )
                >
                2.0e-12
            ):
                continue

            radius_unit = (
                0.5
                *
                (
                    r_phi_unit
                    +
                    r_sigma_unit
                )
            )

            target_mult = (
                pressure_available
                /
                (
                    wall.tension
                    *
                    radius_unit
                )
            )

            center_mult = int(
                round(
                    target_mult
                )
            )

            for mult in range(
                max(
                    1,
                    center_mult
                    -
                    2,
                ),

                max(
                    1,
                    center_mult
                    +
                    2,
                )
                +
                1,
            ):

                radius = (
                    mult
                    *
                    radius_unit
                )

                if (
                    radius
                    /
                    wall.width90
                    <
                    scout.MIN_R_OVER_WALL90
                ):
                    continue

                load = (
                    wall.tension
                    *
                    radius
                )

                balance_rel = (
                    abs(
                        pressure_available
                        -
                        load
                    )
                    /
                    max(
                        abs(
                            pressure_available
                        ),
                        abs(
                            load
                        ),
                        1.0e-30,
                    )
                )

                if (
                    balance_rel
                    >
                    scout.BALANCE_REL_TOL
                ):
                    continue

                candidate = scout.Candidate(

                    base_phi=base_phi,

                    base_sigma=base_sigma,

                    mult=mult,

                    n_phi=(
                        base_phi
                        *
                        mult
                    ),

                    n_sigma=(
                        base_sigma
                        *
                        mult
                    ),

                    v=v,

                    gamma=gamma,

                    radius=radius,

                    balance_rel=balance_rel,

                    energy_line=(
                        energy
                        +
                        mu_bound
                    ),

                    pressure_line=pressure_available,

                    momentum_line=momentum,

                    active_line=(
                        active
                        +
                        active_bound
                    ),

                    omega_phi_lab=omega_phi_lab,

                    k_phi_lab=k_phi_lab,

                    omega_sigma_lab=omega_sigma_lab,

                    k_sigma_lab=k_sigma_lab,
                )

                x_floor = (
                    scout.MIN_PAYLOAD_BOTTOM_OVER_WALL90
                    *
                    wall.width90

                    /

                    (
                        (
                            1.0
                            -
                            scout.PAYLOAD_RADIUS_OVER_H
                        )
                        *
                        radius
                    )
                )

                x_low = max(
                    scout.X_MIN,
                    x_floor,
                )

                if (
                    x_low
                    >=
                    scout.X_MAX
                ):
                    continue

                def objective(
                    x,
                ):

                    value = scout.gravity_and_c(
                        wall,
                        candidate,
                        float(
                            x
                        ),
                        True,
                    )[
                        1
                    ]

                    return (
                        value
                        if math.isfinite(
                            value
                        )
                        else 1.0e300
                    )

                result = minimize_scalar(
                    objective,

                    bounds=(
                        x_low,
                        scout.X_MAX,
                    ),

                    method="bounded",

                    options={
                        "xatol":
                            1.0e-10,
                    },
                )

                if (
                    not result.success

                    or

                    not math.isfinite(
                        float(
                            result.fun
                        )
                    )

                    or

                    float(
                        result.fun
                    )
                    >=
                    1.0e299
                ):
                    continue

                candidate.x = float(
                    result.x
                )

                candidate.c_worst = float(
                    result.fun
                )

                adverse = scout.gravity_and_c(
                    wall,
                    candidate,
                    candidate.x,
                    True,
                )

                nominal = scout.gravity_and_c(
                    wall,
                    candidate,
                    candidate.x,
                    False,
                )

                candidate.f_worst = float(
                    adverse[
                        0
                    ]
                )

                candidate.f_nominal = float(
                    nominal[
                        0
                    ]
                )

                candidate.active_mass_per_r = float(
                    adverse[
                        2
                    ]
                )

                candidate.clearance = float(
                    adverse[
                        3
                    ]
                )

                if (
                    candidate.f_worst
                    <=
                    0.0

                    or

                    candidate.active_mass_per_r
                    <=
                    0.0
                ):
                    continue

                found.append(
                    (
                        candidate,
                        adverse,
                        nominal,
                    )
                )

    if not found:
        return []

    best_by_pair = {}

    for record in found:

        candidate = record[
            0
        ]

        key = (
            candidate.n_phi,
            candidate.n_sigma,
        )

        previous = best_by_pair.get(
            key
        )

        if (
            previous is None

            or

            candidate.c_worst
            <
            previous[
                0
            ].c_worst
        ):

            best_by_pair[
                key
            ] = record

    return sorted(
        best_by_pair.values(),
        key=lambda record:
            record[
                0
            ].c_worst,
    )


def main() -> None:
    """Run the new two-current fixed-background junction and corrected scout."""

    print(
        "=== 018B-0G — TWO-CURRENT 2D JUNCTION "
        "+ BACKREACTION PREFLIGHT ==="
    )

    require_marker(
        D_LOG,
        "018B0D_TWO_CURRENT_COUNTERFLOW_GATE=GREEN",
    )

    require_marker(
        F0_LOG,
        "018B0F0_LILLEY_KLS_NORMALIZATION_WALL_BRIDGE=GREEN",
    )

    require_marker(
        F_LOG,
        "018B0F_STATIONARY_INTEGER_WALL_BALANCE_GRAVITY_SCOUT=GREEN",
    )

    if not F_SOURCE.exists():

        raise RuntimeError(
            f"Missing 018B-0F source: {F_SOURCE}"
        )

    source_hash = hashlib.sha256(
        F_SOURCE.read_bytes()
    ).hexdigest()

    print(
        "UPSTREAM_018B0F_SOURCE_SHA256="
        f"{source_hash}"
    )

    print(
        "UPSTREAM_018B0F_HASH_ENFORCED="
        "NO_EXECUTED_LOCAL_SOURCE_IS_AUTHORITY"
    )

    scout = load_module(
        "ag018b0g_scout",
        F_SOURCE,
    )

    state, wall = scout.load_inputs()

    parameters = load_parameters()

    print(
        "\n=== LORENTZ-INVARIANT MICROSTATE CHECK ==="
    )

    w_phi = (
        parameters.k_phi**2
        -
        parameters.omega_phi**2
    )

    w_sigma = (
        parameters.k_sigma**2
        -
        parameters.omega_sigma**2
    )

    print(
        f"W_PHI="
        f"{w_phi:+.15e}"
    )

    print(
        f"W_SIGMA="
        f"{w_sigma:+.15e}"
    )

    print(
        "STATIONARY_BOOST_CHANGES_TRANSVERSE_BVP="
        "NO_BY_LORENTZ_INVARIANCE"
    )

    print(
        "\n=== INDEPENDENT TWO-CURRENT RADIAL BVP RECONSTRUCTION ==="
    )

    radial_results = {}

    for domain in RADIAL_DOMAINS:

        result = solve_radial(
            parameters,
            domain,
        )

        radial_results[
            domain
        ] = result

        print(
            f"RADIAL_DOMAIN="
            f"{domain:.0f} "

            f"I_PHI="
            f"{result['i_phi']:.15e} "

            f"I_SIGMA="
            f"{result['i_sigma']:.15e} "

            f"PHI0="
            f"{result['phi0']:.15e} "

            f"SIGMA0="
            f"{result['sigma0']:.15e} "

            f"MAX_RMS="
            f"{result['max_rms']:.3e}"
        )

    reference = domain80_reference(
        D_LOG
    )

    r80 = radial_results[
        80.0
    ]

    radial_errors = [
        abs(
            r80[
                "i_phi"
            ]
            -
            reference[
                "I_PHI"
            ]
        )
        /
        abs(
            reference[
                "I_PHI"
            ]
        ),

        abs(
            r80[
                "i_sigma"
            ]
            -
            reference[
                "I_SIGMA"
            ]
        )
        /
        abs(
            reference[
                "I_SIGMA"
            ]
        ),

        abs(
            r80[
                "phi0"
            ]
            -
            reference[
                "PHI0"
            ]
        )
        /
        abs(
            reference[
                "PHI0"
            ]
        ),

        abs(
            r80[
                "sigma0"
            ]
            -
            reference[
                "SIGMA0"
            ]
        )
        /
        abs(
            reference[
                "SIGMA0"
            ]
        ),
    ]

    radial_reference_max = max(
        radial_errors
    )

    radial_pass = (
        max(
            row[
                "max_rms"
            ]
            for row
            in radial_results.values()
        )
        <=
        MAX_BVP_RMS

        and

        radial_reference_max
        <=
        MAX_RADIAL_REFERENCE_RELERR
    )

    print(
        "RADIAL_DOMAIN80_REFERENCE_MAX_RELERR="
        f"{radial_reference_max:.15e}"
    )

    print(
        "INDEPENDENT_TWO_CURRENT_RADIAL_RECONSTRUCTION="
        f"{'PASS' if radial_pass else 'FAIL'}"
    )

    radial_solution = r80[
        "solution"
    ]

    print(
        "\n=== FIXED-BACKGROUND 2D JUNCTION — "
        "RESOLUTION SEQUENCE ==="
    )

    resolution_results = []

    cache = {}

    for (
        n,
        box_half,
    ) in RESOLUTION_CASES:

        key = (
            n,
            box_half,
        )

        result = solve_lattice(
            radial_solution,
            n,
            box_half,
        )

        resolution_results.append(
            result
        )

        cache[
            key
        ] = result

        print(
            f"JUNCTION_N={n} "
            f"L={box_half:.1f} "
            f"DX={result['dx']:.9f} "

            f"PASS="
            f"{'YES' if result['passed'] else 'NO'} "

            f"MU="
            f"{result['junction_energy']:+.15e} "

            f"ACTIVE="
            f"{result['junction_active']:+.15e} "

            f"GRAD_RMS="
            f"{result['gradient_rms']:.3e} "

            f"GRAD_MAX="
            f"{result['gradient_max']:.3e} "

            f"AXIS_RATIO="
            f"{result['axis_ratio']:.3e} "

            f"PHASE_LOCK_P01="
            f"{result['phase_lock_p01']:.9f}"
        )

    print(
        "\n=== FIXED-BACKGROUND 2D JUNCTION — "
        "DOMAIN SEQUENCE ==="
    )

    domain_results = []

    for (
        n,
        box_half,
    ) in DOMAIN_CASES:

        key = (
            n,
            box_half,
        )

        if key in cache:

            result = cache[
                key
            ]

        else:

            result = solve_lattice(
                radial_solution,
                n,
                box_half,
            )

            cache[
                key
            ] = result

        domain_results.append(
            result
        )

        print(
            f"JUNCTION_DOMAIN_L="
            f"{box_half:.1f} "

            f"N={n} "

            f"DX="
            f"{result['dx']:.9f} "

            f"PASS="
            f"{'YES' if result['passed'] else 'NO'} "

            f"MU="
            f"{result['junction_energy']:+.15e} "

            f"ACTIVE="
            f"{result['junction_active']:+.15e}"
        )

    (
        mu_cont,
        mu_spread,
        mu_estimates,
    ) = extrapolated_estimate(
        resolution_results,
        "junction_energy",
    )

    (
        active_cont,
        active_spread,
        active_estimates,
    ) = extrapolated_estimate(
        resolution_results,
        "junction_active",
    )

    by_l = {
        row[
            "box_half"
        ]:
            row

        for row
        in domain_results
    }

    mu_domain_shift = abs(
        by_l[
            80.0
        ][
            "junction_energy"
        ]
        -
        by_l[
            60.0
        ][
            "junction_energy"
        ]
    )

    mu_domain_fraction = (
        mu_domain_shift
        /
        max(
            abs(
                by_l[
                    80.0
                ][
                    "junction_energy"
                ]
            ),
            1.0e-30,
        )
    )

    mu_estimate = (
        mu_cont

        +

        (
            by_l[
                80.0
            ][
                "junction_energy"
            ]

            -

            by_l[
                60.0
            ][
                "junction_energy"
            ]
        )
    )

    max_mu_observed = max(
        row[
            "junction_energy"
        ]
        for row
        in cache.values()
    )

    max_active_observed = max(
        abs(
            row[
                "junction_active"
            ]
        )
        for row
        in cache.values()
    )

    mu_bound = (
        JUNCTION_ENERGY_INFLATION
        *
        max(
            max_mu_observed,
            abs(
                mu_estimate
            ),
        )
    )

    active_bound = (
        JUNCTION_ACTIVE_INFLATION
        *
        max(
            max_active_observed,
            abs(
                active_cont
            ),
        )
    )

    convergence_pass = (
        all(
            row[
                "passed"
            ]
            for row
            in cache.values()
        )

        and

        mu_spread
        <=
        MAX_EXTRAPOLATION_SPREAD_FRACTION

        and

        active_spread
        <=
        MAX_EXTRAPOLATION_SPREAD_FRACTION

        and

        mu_domain_fraction
        <=
        MAX_DOMAIN_SHIFT_FRACTION
    )

    print(
        "\n=== JUNCTION CONTINUUM / DOMAIN AUDIT ==="
    )

    print(
        "MU_DX0_LINEAR_QUADRATIC_CUBIC="
        +
        ",".join(
            f"{value:.15e}"
            for value
            in mu_estimates
        )
    )

    print(
        "MU_DX0_EXTRAPOLATION_SPREAD_FRACTION="
        f"{mu_spread:.15e}"
    )

    print(
        "ACTIVE_DX0_LINEAR_QUADRATIC_CUBIC="
        +
        ",".join(
            f"{value:.15e}"
            for value
            in active_estimates
        )
    )

    print(
        "ACTIVE_DX0_EXTRAPOLATION_SPREAD_FRACTION="
        f"{active_spread:.15e}"
    )

    print(
        "MU_L60_TO_L80_REL_SHIFT_AT_DX1="
        f"{mu_domain_fraction:.15e}"
    )

    print(
        "JUNCTION_MU_ESTIMATE_PREFLIGHT="
        f"{mu_estimate:.15e}"
    )

    print(
        "JUNCTION_MU_CONSERVATIVE_BOUND="
        f"{mu_bound:.15e}"
    )

    print(
        "JUNCTION_ACTIVE_CONSERVATIVE_BOUND="
        f"{active_bound:.15e}"
    )

    print(
        "FIXED_BACKGROUND_JUNCTION_CONVERGENCE="
        f"{'PASS' if convergence_pass else 'FAIL'}"
    )

    selected_grid = cache[
        (
            161,
            80.0,
        )
    ]

    backreaction_pass = (
        selected_grid[
            "h_source_max"
        ]
        <=
        MAX_H_SOURCE

        and

        selected_grid[
            "current_ratio"
        ]
        <=
        MAX_GAUGE_CURRENT_RATIO
    )

    print(
        "\n=== FROZEN-FIELD BACKREACTION AUDIT ==="
    )

    print(
        "H_EXTENSION_SOURCE_MAX="
        f"{selected_grid['h_source_max']:.15e}"
    )

    print(
        "H_EXTENSION_SOURCE_RMS="
        f"{selected_grid['h_source_rms']:.15e}"
    )

    print(
        "A_GAUGE_CURRENT_L2="
        f"{selected_grid['a_current_l2']:.15e}"
    )

    print(
        "H_GAUGE_CURRENT_L2="
        f"{selected_grid['h_current_l2']:.15e}"
    )

    print(
        "A_TO_H_GAUGE_CURRENT_L2_RATIO="
        f"{selected_grid['current_ratio']:.15e}"
    )

    print(
        "PHI_DIRECT_KLS_SOURCE=0"
    )

    print(
        "SIGMA_DIRECT_KLS_SOURCE=0"
    )

    print(
        "FIXED_BACKGROUND_BACKREACTION_PREFLIGHT="
        f"{'PASS' if backreaction_pass else 'FAIL'}"
    )

    print(
        "\n=== CONSERVATIVE JUNCTION-PENALIZED "
        "STATIONARY SCOUT ==="
    )

    print(
        "JUNCTION_ENERGY_INFLATION="
        f"{JUNCTION_ENERGY_INFLATION:.6f}"
    )

    print(
        "JUNCTION_ACTIVE_INFLATION="
        f"{JUNCTION_ACTIVE_INFLATION:.6f}"
    )

    print(
        "INFLATED_VALUES_ARE_PHYSICAL_FIT_PARAMETERS=NO"
    )

    corrected = corrected_integer_search(
        scout,
        state,
        wall,
        mu_bound,
        active_bound,
    )

    print(
        "CORRECTED_EXACT_INTEGER_PASSERS="
        f"{len(corrected)}"
    )

    corrected_green = bool(
        corrected
    )

    if corrected:

        candidate, adverse, nominal = (
            corrected[
                0
            ]
        )

        print(
            "CORRECTED_BASE_N_PHI="
            f"{candidate.base_phi}"
        )

        print(
            "CORRECTED_BASE_N_SIGMA="
            f"{candidate.base_sigma}"
        )

        print(
            "CORRECTED_COMMON_MULTIPLIER="
            f"{candidate.mult}"
        )

        print(
            "CORRECTED_N_PHI="
            f"{candidate.n_phi}"
        )

        print(
            "CORRECTED_N_SIGMA="
            f"{candidate.n_sigma}"
        )

        print(
            "CORRECTED_BOOST_V="
            f"{candidate.v:+.15e}"
        )

        print(
            "CORRECTED_LIGHTCONE_MARGIN="
            f"{1.0 - abs(candidate.v):.15e}"
        )

        print(
            "CORRECTED_RADIUS="
            f"{candidate.radius:.15e}"
        )

        print(
            "CORRECTED_R_OVER_WALL90="
            f"{candidate.radius / wall.width90:.15e}"
        )

        print(
            "CORRECTED_P_AVAILABLE="
            f"{candidate.pressure_line:+.15e}"
        )

        print(
            "CORRECTED_WALL_LOAD="
            f"{wall.tension * candidate.radius:+.15e}"
        )

        print(
            "CORRECTED_WALL_BALANCE_RELERR="
            f"{candidate.balance_rel:.15e}"
        )

        print(
            "CORRECTED_H_OVER_R="
            f"{candidate.x:.15e}"
        )

        print(
            "CORRECTED_NOMINAL_PAYLOAD_OUTWARD="
            f"{nominal[0]:+.15e}"
        )

        print(
            "CORRECTED_ADVERSE_PAYLOAD_OUTWARD="
            f"{adverse[0]:+.15e}"
        )

        print(
            "CORRECTED_ACTIVE_MASS_PER_R="
            f"{adverse[2]:+.15e}"
        )

        print(
            "CORRECTED_PROJECTED_C="
            f"{adverse[1]:.15e}"
        )

        print(
            "CORRECTED_PROJECTED_C_STATUS="
            "PREFLIGHT_ONLY_NOT_VALIDATED"
        )

    overall = (
        radial_pass

        and

        convergence_pass

        and

        backreaction_pass

        and

        corrected_green
    )

    print(
        "\n=== DECISION ==="
    )

    if overall:

        print(
            "018B0G_TWO_CURRENT_FIXED_BACKGROUND_2D_JUNCTION_GATE="
            "GREEN"
        )

        print(
            "NEW_TWO_CURRENT_FIXED_BACKGROUND_JUNCTION="
            "SUPPORTED"
        )

        print(
            "NEW_TWO_CURRENT_JUNCTION_BACKREACTION_EXPECTATION="
            "PERTURBATIVE_AT_PREFLIGHT_LEVEL"
        )

        print(
            "JUNCTION_PENALIZED_STATIONARY_GRAVITY_SCOUT="
            "PASS"
        )

        print(
            "FULLY_COUPLED_TWO_CURRENT_2D_JUNCTION="
            "AUTHORIZED"
        )

        print(
            "NEXT="
            "018B0G2_FULLY_COUPLED_TWO_CURRENT_MATCHED_2D_JUNCTION"
        )

        print(
            "NEXT_AFTER_018B0G2_GREEN="
            "018B0H_COMPLETE_SOURCE_GRAVITY_REVALIDATION"
        )

    else:

        print(
            "018B0G_TWO_CURRENT_FIXED_BACKGROUND_2D_JUNCTION_GATE="
            "RED"
        )

        print(
            "FULLY_COUPLED_TWO_CURRENT_2D_JUNCTION="
            "NOT_AUTHORIZED"
        )

        print(
            "NEXT="
            "CLASSIFY_018B0G_FAILURE_BEFORE_ESCALATION"
        )

    print(
        "CURRENT_HEURISTIC="
        "APPROXIMATELY_66_PERCENT_NOT_A_PROBABILITY"
    )

    print(
        "HEURISTIC_INCREASE_FROM_THIS_GATE="
        "NO_FIXED_BACKGROUND_PREFLIGHT_ONLY"
    )

    print(
        "TRUE_018B_GLOBAL_FIELD_SOLUTION="
        "NOT_YET_RUN"
    )

    print(
        "FULL_COMPOSITE_STABILITY="
        "NOT_ESTABLISHED"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )

    print(
        "NEW_PHYSICS_DISCOVERY=NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_018B0G_TWO_CURRENT_FIXED_BACKGROUND_"
        "JUNCTION_AND_BACKREACTION_PREFLIGHT"
    )


if __name__ == "__main__":
    main()
