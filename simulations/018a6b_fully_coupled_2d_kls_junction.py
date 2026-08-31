#!/usr/bin/env python3
"""Simulation 018A-6B — fully coupled two-dimensional KLS junction gate.

PURPOSE
-------
Release all microscopic matter/gauge degrees of freedom that were held fixed
in 018A-6A and determine whether the preferred nonthermal KLS-style wall
actually survives as a solution of the coupled field equations.

The active model combines:

    - the literature-backed 017P superconducting gauged string;
    - the charge-2 reinterpretation of the 017P vortex field Phi;
    - one charge-1 complex wall field A;
    - the same fundamental U(1)_X gauge field;
    - the current-carrying sigma condensate;
    - the gauge-invariant phase-locking interaction.

PRIOR RESULTS
-------------
018A-4:

    same-gauge U(1) -> Z2 -> 1 topology = PASS
    mandatory global-string logarithmic tail = ABSENT
    selected +/-10 percent robustness = 125/125

018A-5:

    relaxed microscopic planar wall = PASS
    sigma_W = 5.623876169625573e-4
    active wall source = -sigma_W
    transverse complex-A mode = stable
    selected robustness = 125/125

018A-6A:

    true 2D complex A field = solved
    one-sided wall termination = PASS
    domain convergence = PASS
    resolution convergence = PASS
    finite localized junction energy = PASS
    gauge-invariance check = PASS

018A-6B0:

    Phi backreaction source = small
    gauge-current backreaction = small
    junction active-source perturbation = small
    fixed-background EOS = healthy
    m=2..40 extrinsic stability = PASS
    one- and two-junction stationarity = PASS.

ACTIVE SCIENTIFIC QUESTION
--------------------------
When Phi, sigma, A, and the transverse gauge field are allowed to relax
simultaneously, does there exist a finite-energy, numerically converged,
topologically correct wall-ending-on-vortex solution whose localized junction
energy and stress remain compatible with the healthy 017P EOS and radial
stationarity?

APPROXIMATION LEVEL
-------------------
This is a genuine coupled two-dimensional transverse string-wall junction
calculation.

The string is locally straight along the y direction.

The Phi topological phase is fixed to unit vortex winding

    Phi = f(x,z) exp(i theta)

while its amplitude f(x,z) is fully relaxed.

Fixing the topological phase pins the vortex position and fixes gauge freedom;
it does not freeze its amplitude or gauge-flux profile.

The current-carrying condensate is

    sigma =
      s(x,z) exp[i(omega t + k y)].

Its transverse amplitude s(x,z) is fully relaxed.

The charge-1 field

    A(x,z)

is fully complex and fully relaxed.

The transverse U(1)_X gauge links are fully relaxed in the fixed-vortex-phase
gauge.

This is therefore substantially stronger than 018A-6A, but it is still a
local straight-junction calculation rather than the curved finite-radius drum.

FIELD THEORY
------------
The original 017P reduced transverse potential at fixed

    chi = omega^2-k^2

is

    V_017P =
      lambda_Phi/4 (|Phi|^2-eta_Phi^2)^2
      + lambda_sigma/4 (s^2-eta_sigma^2)^2
      + beta |Phi|^2 s^2
      - lambda_sigma eta_sigma^4/4
      - chi s^2.

The KLS extension is

    V_KLS =
      lambda_A/4 (|A|^2-F^2)^2

      - h [
          Phi^* A^2
          +
          Phi (A^*)^2
        ]

      + c_Phi (|Phi|^2-eta_Phi^2)

      + c_A (|A|^2-F^2)

      + C

with

    c_Phi = h F^2 / eta_Phi
    c_A   = 2 h eta_Phi
    C     = 2 h eta_Phi F^2.

SELECTED PARAMETERS
-------------------
017P Set-G selected point:

    lambda_Phi   = 1
    lambda_sigma = 900
    eta_Phi      = 1
    eta_sigma    = 0.1825
    beta         = 20
    g_017P       = 0.1414213562373095
    chi          = 0.00475.

Same-gauge KLS sector:

    q_Phi = 2
    q_A   = 1

    g_X =
      g_017P / 2

    F =
      0.075

    h =
      0.010

    lambda_A =
      1.

GAUGE-COVARIANT LATTICE
------------------------
Use noncompact fundamental link angles

    alpha_x =
      g_X integral X_x dx

    alpha_z =
      g_X integral X_z dz.

The charge-1 parallel transporter is

    U =
      exp(i alpha).

The charge-2 Phi transporter is

    U^2 =
      exp(2 i alpha).

The discrete scalar gradient energies are therefore

    |A_q-U A_p|^2

and

    |Phi_q-U^2 Phi_p|^2.

The plaquette flux is

    P =
      alpha_x(i,j)
      + alpha_z(i+1,j)
      - alpha_x(i,j+1)
      - alpha_z(i,j).

Since

    P =
      g_X B dx^2,

the magnetic energy is

    E_B =
      1/(2 g_X^2 dx^2)
      sum P^2.

This reproduces the continuum normalization

    integral B^2/2 d^2x.

FULLY COUPLED VARIABLES
-----------------------
The optimizer releases simultaneously:

    f(x,z)
    s(x,z)
    Re A(x,z)
    Im A(x,z)
    alpha_x(x,z)
    alpha_z(x,z).

The outer boundary remains fixed to the independently reconstructed 017P
background plus the converged 018A-6A one-sided wall boundary.

The vortex center value

    f(0,0)=0

is fixed to preserve unit winding and prevent translation of the topological
core out of the box.

No phenomenological core-binding interaction is used.

INITIAL CONDITION
-----------------
For every coupled solve:

1. reconstruct the appropriate 017P radial background;
2. solve the already verified 018A-6A fixed-background A problem;
3. use that field configuration as the starting A field;
4. use the radial f, s, and gauge profiles as the starting remaining fields;
5. release every interior variable simultaneously.

Because 018A-6B0 measured very small forcing in the frozen sectors, this is a
continuation from an already nearby stationary configuration rather than a
blind nonlinear search.

JUNCTION ENERGY
---------------
Directly comparing raw lattice total energies across resolutions can obscure a
small junction energy beneath discretization error in the much larger 017P
string energy.

Therefore use a same-grid subtraction.

For each grid define

    E_reference =
      E_017P,background,lattice
      +
      E_KLS,018A6A,lattice.

Let

    Delta E_relax =
      E_full_coupled
      -
      E_reference.

The already converged 018A-6A junction excess on that same grid is

    mu_6A =
      E_KLS,018A6A
      -
      sigma_W L.

The fully coupled junction excess is reconstructed as

    mu_full =
      mu_6A
      +
      Delta E_relax.

This same-grid difference strongly cancels unrelated lattice error in the
large base-string energy.

SIGMA2
------
The current condensate integral is reconstructed with the same strategy.

Let

    Delta Sigma2 =
      integral [
        s_full^2
        -
        s_background^2
      ] d^2x.

Then

    Sigma2_full =
      Sigma2_radial
      +
      Delta Sigma2.

This suppresses square-grid quadrature bias in the exponentially localized
string condensate.

ACTIVE GRAVITATIONAL SOURCE
---------------------------
For the physical stationary fields, while the reduced transverse potential
contains

    -chi s^2,

the physical scalar potential does not.

Using

    chi =
      omega^2-k^2,

the complete active density of the scalar plus transverse magnetic sector may
be written in terms of the reduced potential as

    S =
      2(omega^2+k^2)s^2
      - 2 V_reduced
      + B^2.

Transverse scalar gradients cancel from

    T_tt+T_xx+T_yy+T_zz.

The magnetic contribution is

    +B^2.

For the fixed-background reference the corresponding expression is evaluated
on the exact same grid.

The difference therefore measures the mandatory active-source change generated
by coupled relaxation without confusing it with the much larger pre-existing
017P line source.

The one-sided wall active contribution is separately

    -sigma_W L.

FULL LINE-STRESS BOOKKEEPING
----------------------------
For the localized endpoint define

    Delta Sigma2 =
      Sigma2_full-Sigma2_017P.

The reduced junction energy is

    mu_full.

Its longitudinal physical energy/stress contributions from the changed
current condensate are

    Delta U_J =
      mu_full
      +
      2 omega^2 Delta Sigma2

    Delta T_yy,J =
      -mu_full
      +
      2 k^2 Delta Sigma2.

The directly reconstructed active endpoint contribution is also reported.

The remaining transverse integrated stress sum is inferred from

    T_perp,J =
      Lambda_active,J
      -
      Delta U_J
      -
      Delta T_yy,J.

This is bookkeeping, not an assumption that the endpoint is an isolated
free string. The attached wall can supply nonzero transverse force.

EOS CONTINUATION
----------------
Three fully coupled common-grid solutions are computed at

    chi =
      0.00425
      0.00450
      0.00475.

For each calculate

    A_eff =
      A_string
      +
      mu_full

and

    Sigma2_full.

The fully coupled variational identity is tested:

    dA_eff/dchi
      =
      -Sigma2_full.

Then

    c_T^2 =
      1 /
      [
        1
        +
        2 chi Sigma2_full/A_eff
      ]

and

    c_L^2 =
      1 /
      [
        1
        +
        2 chi
        (dSigma2_full/dchi)
        /
        Sigma2_full
      ].

The published 017P m=2..40 thin-string cubic is rerun on those fully coupled
effective quantities.

CONVERGENCE
-----------
Fixed-dx domain sequence:

    N=61,  L=75
    N=81,  L=100
    N=101, L=125.

Fixed-L resolution sequence:

    N=81,  L=100
    N=101, L=100
    N=121, L=100.

The selected high-information stress/EOS point is the finest

    N=121, L=100

solution.

The common-grid chi continuation uses

    N=81, L=100.

MORPHOLOGY
----------
The fully coupled solution must retain:

    one wall on the negative-x side;
    vacuum recovery on positive x;
    locked gauge-invariant relative phase away from the defect;
    a localized vortex core.

PASS CONDITIONS
---------------
The gate is green only if:

    FULL_COUPLED_ANALYTIC_GRADIENT=PASS

    FULL_COUPLED_DOMAIN_CONVERGENCE=PASS

    FULL_COUPLED_DOMAIN_WALL_SLOPE=PASS

    FULL_COUPLED_RESOLUTION_CONVERGENCE=PASS

    FULL_COUPLED_WALL_TERMINATION=PASS

    FULL_COUPLED_RELATIVE_PHASE_LOCKING=PASS

    FULL_COUPLED_VARIATIONAL_IDENTITY=PASS

    FULL_COUPLED_EOS_HEALTH=PASS

    FULL_COUPLED_M2_TO_M40_STABILITY=PASS

    FULL_COUPLED_ACTIVE_SOURCE_BUDGET=PASS

    FULL_COUPLED_ONE_JUNCTION_STATIONARITY=PASS

    FULL_COUPLED_TWO_JUNCTION_STATIONARITY=PASS.

PROMOTION
---------
A green result establishes:

    FULLY_COUPLED_LOCAL_2D_KLS_JUNCTION=SUPPORTED

at the straight-string level.

It does NOT by itself make full 018A green.

The next mandatory gate would be:

    018A7_COMPLETE_MICROSCOPIC_GRAVITY_CLOSEOUT

using the measured wall and junction stress-energy to retest:

    positive total active mass;
    point acceleration;
    finite-payload CM acceleration;
    kernel leverage;
    complete stationarity;
    robust neighborhood.

Only a green gravity closeout may promote 018A and authorize 018B.

FALSIFICATION
-------------
Stop or rerank if full coupling:

    destroys the wall endpoint;
    produces growing/nonlocalized junction energy;
    drives large uncontrolled changes in Sigma2;
    breaks the variational identity;
    exits the healthy EOS/stability basin;
    consumes the line-energy budget;
    generates an active source large enough to overturn the desired gravity.

UNITS
-----
Natural units and the existing dimensionless 017P normalization.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_018A_FULLY_COUPLED_LOCAL_2D_KLS_JUNCTION

PRACTICAL CLAIM
---------------
This run cannot establish a practical antigravity device.
"""

from __future__ import annotations

from dataclasses import dataclass
import importlib.util
import math
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import minimize


ROOT = Path(__file__).resolve().parents[1]

SOURCE = (
    ROOT
    / "simulations"
    / "018a6a_fixed_background_2d_kls_junction.py"
)


def load_module(
    name: str,
    path: Path,
):
    """Load the already locally verified 018A-6A implementation."""

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

    sys.modules[name] = module

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


m = load_module(
    "ag018a6a_fullcoupled",
    SOURCE,
)


# ============================================================================
# Physical anchors.
# ============================================================================

CHI_SELECTED = 0.00475

CHI_VALUES = (
    0.00425,
    0.00450,
    0.00475,
)

OMEGA_SELECTED = 2.227569443362
K_SELECTED = 2.226503003591

Q_OVER_N = 6.628230560688
ELL = 0.4257542346286
W_STAT = 12.66497926067

WALL_WIDTH90 = 78.534118560778


# ============================================================================
# Numerical sequence.
# ============================================================================

DOMAIN_CASES = (
    (61, 75.0),
    (81, 100.0),
    (101, 125.0),
)

RESOLUTION_CASES = (
    (81, 100.0),
    (101, 100.0),
    (121, 100.0),
)

CHI_CASE = (
    81,
    100.0,
)

GRADIENT_CHECK_CASE = (
    31,
    50.0,
)


# ============================================================================
# Numerical tolerances / stop rules.
# ============================================================================

OPT_MAXITER = 1400
OPT_FTOL = 2.0e-12
OPT_GTOL = 2.0e-7

MAX_GRAD_RMS = 3.0e-6
MAX_GRAD_ABS = 3.0e-5

MAX_GRADIENT_CHECK_RELERR = 2.0e-6

MAX_DOMAIN_MU_REL_SPREAD = 0.03
MAX_DOMAIN_SLOPE_RELERR = 0.02

MAX_RESOLUTION_MU_REL_SPREAD = 0.05

MAX_NEGATIVE_WALL_A_OVER_F = 0.03
MIN_POSITIVE_RECOVERY_A_OVER_F = 0.94
MAX_PHASE_LOCK_RMS = 2.0e-3

MAX_VARIATIONAL_RELERR = 0.015

MAX_ACTIVE_PAIR_PERTURBATION = 0.01

MIN_SCALE_SEPARATION = 10.0
MAX_INTEGER_MISMATCH = 1.0e-3


@dataclass
class FullProblem:
    """All data required for one fully coupled lattice minimization."""

    chi: float

    n: int
    box_half: float
    dx: float

    fixed_result: object
    radial_solution: object
    radial_diag: object

    weights: np.ndarray

    theta: np.ndarray
    phi_phase: np.ndarray

    f0: np.ndarray
    s0: np.ndarray
    a0: np.ndarray

    ax0: np.ndarray
    az0: np.ndarray

    f_free: np.ndarray
    s_free: np.ndarray
    a_free: np.ndarray

    ax_free: np.ndarray
    az_free: np.ndarray

    nf: int
    ns: int
    na: int
    nax: int
    naz: int


@dataclass
class FullResult:
    """Diagnostics from one fully coupled junction minimization."""

    chi: float

    n: int
    box_half: float
    dx: float

    success: bool
    optimizer_message: str
    iterations: int

    energy_reference: float
    energy_full: float
    relaxation_delta_energy: float

    mu_fixed: float
    mu_full: float

    sigma2_background: float
    sigma2_full: float
    delta_sigma2: float

    grad_rms: float
    grad_max: float

    f: np.ndarray
    s: np.ndarray
    a: np.ndarray

    ax: np.ndarray
    az: np.ndarray

    problem: FullProblem


# ============================================================================
# Problem construction.
# ============================================================================


def build_full_problem(
    chi: float,
    n: int,
    box_half: float,
) -> FullProblem:
    """Construct one fully coupled continuation from the verified 018A-6A state."""

    m.CHI_SELECTED = float(
        chi
    )

    radial_solution = (
        m.solve_017p_background()
    )

    radial_diag = (
        m.diagnose_017p(
            radial_solution
        )
    )

    fixed_result = (
        m.run_case(
            radial_solution,
            n=n,
            box_half=box_half,
        )
    )

    if not fixed_result.optimizer_success:
        raise RuntimeError(
            "018A-6A starting solution failed for "
            f"chi={chi}, N={n}, L={box_half}"
        )

    background = (
        fixed_result.problem
    )

    theta = np.arctan2(
        background.Z,
        background.X,
    )

    phi_phase = np.exp(
        1j
        *
        theta
    )

    f0 = np.array(
        background.f_background,
        copy=True,
    )

    s0 = (
        m.evaluate_radial_component(
            radial_solution,
            background.radius,
            2,
            0.0,
        )
    )

    a0 = np.array(
        fixed_result.field,
        copy=True,
    )

    ax0 = np.angle(
        background.ux
    )

    az0 = np.angle(
        background.uz
    )

    node_interior = np.array(
        ~background.fixed_mask,
        copy=True,
    )

    f_free = np.array(
        node_interior,
        copy=True,
    )

    # Pin the vortex center and therefore its topological position.
    center = (
        n
        //
        2
    )

    f_free[
        center,
        center,
    ] = False

    s_free = np.array(
        node_interior,
        copy=True,
    )

    a_free = np.array(
        node_interior,
        copy=True,
    )

    # A gauge link is released only when both endpoints lie inside the outer
    # fixed boundary. This keeps the asymptotic flux boundary exactly fixed.
    ax_free = np.zeros(
        ax0.shape,
        dtype=bool,
    )

    ax_free[
        1:-1,
        1:-1,
    ] = True

    az_free = np.zeros(
        az0.shape,
        dtype=bool,
    )

    az_free[
        1:-1,
        1:-1,
    ] = True

    return FullProblem(
        chi=float(
            chi
        ),

        n=n,
        box_half=box_half,
        dx=background.dx,

        fixed_result=fixed_result,
        radial_solution=radial_solution,
        radial_diag=radial_diag,

        weights=np.array(
            background.weights,
            copy=True,
        ),

        theta=theta,
        phi_phase=phi_phase,

        f0=f0,
        s0=s0,
        a0=a0,

        ax0=ax0,
        az0=az0,

        f_free=f_free,
        s_free=s_free,
        a_free=a_free,

        ax_free=ax_free,
        az_free=az_free,

        nf=int(
            np.count_nonzero(
                f_free
            )
        ),

        ns=int(
            np.count_nonzero(
                s_free
            )
        ),

        na=int(
            np.count_nonzero(
                a_free
            )
        ),

        nax=int(
            np.count_nonzero(
                ax_free
            )
        ),

        naz=int(
            np.count_nonzero(
                az_free
            )
        ),
    )


# ============================================================================
# Pack / unpack.
# ============================================================================


def pack_initial(
    problem: FullProblem,
) -> np.ndarray:
    """Pack the fixed-background continuation state."""

    a_values = (
        problem.a0[
            problem.a_free
        ]
    )

    return np.concatenate(
        [
            problem.f0[
                problem.f_free
            ],

            problem.s0[
                problem.s_free
            ],

            a_values.real,
            a_values.imag,

            problem.ax0[
                problem.ax_free
            ],

            problem.az0[
                problem.az_free
            ],
        ]
    )


def unpack(
    problem: FullProblem,
    variables: np.ndarray,
) -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
]:
    """Restore the optimizer vector to all coupled fields."""

    f = np.array(
        problem.f0,
        copy=True,
    )

    s = np.array(
        problem.s0,
        copy=True,
    )

    a = np.array(
        problem.a0,
        copy=True,
    )

    ax = np.array(
        problem.ax0,
        copy=True,
    )

    az = np.array(
        problem.az0,
        copy=True,
    )

    offset = 0

    f[
        problem.f_free
    ] = variables[
        offset:
        offset
        +
        problem.nf
    ]

    offset += problem.nf

    s[
        problem.s_free
    ] = variables[
        offset:
        offset
        +
        problem.ns
    ]

    offset += problem.ns

    a_real = variables[
        offset:
        offset
        +
        problem.na
    ]

    offset += problem.na

    a_imag = variables[
        offset:
        offset
        +
        problem.na
    ]

    offset += problem.na

    a[
        problem.a_free
    ] = (
        a_real
        +
        1j
        *
        a_imag
    )

    ax[
        problem.ax_free
    ] = variables[
        offset:
        offset
        +
        problem.nax
    ]

    offset += problem.nax

    az[
        problem.az_free
    ] = variables[
        offset:
        offset
        +
        problem.naz
    ]

    offset += problem.naz

    if offset != variables.size:
        raise RuntimeError(
            "Pack/unpack variable-count mismatch"
        )

    center = (
        problem.n
        //
        2
    )

    f[
        center,
        center,
    ] = 0.0

    return (
        f,
        s,
        a,
        ax,
        az,
    )


def optimizer_bounds(
    problem: FullProblem,
):
    """Return conservative amplitude bounds without constraining phases/flux."""

    return (
        [
            (
                0.0,
                1.5,
            )
        ]
        *
        problem.nf

        +
        [
            (
                0.0,
                1.0,
            )
        ]
        *
        problem.ns

        +
        [
            (
                None,
                None,
            )
        ]
        *
        (
            2
            *
            problem.na

            +
            problem.nax

            +
            problem.naz
        )
    )


# ============================================================================
# Potentials and plaquettes.
# ============================================================================


def fields_from_amplitudes(
    problem: FullProblem,
    f: np.ndarray,
) -> np.ndarray:
    """Return the fixed-unit-winding complex Phi field."""

    return (
        f
        *
        problem.phi_phase
    )


def base_potential(
    problem: FullProblem,
    f: np.ndarray,
    s: np.ndarray,
) -> np.ndarray:
    """Return the 017P reduced transverse potential density."""

    return (
        m.LAMBDA_PHI
        /
        4.0
        *
        (
            f
            *
            f
            -
            m.ETA_PHI
            *
            m.ETA_PHI
        ) ** 2

        +
        m.LAMBDA_SIGMA
        /
        4.0
        *
        (
            s
            *
            s
            -
            m.ETA_SIGMA
            *
            m.ETA_SIGMA
        ) ** 2

        +
        m.BETA
        *
        f
        *
        f
        *
        s
        *
        s

        -
        m.LAMBDA_SIGMA
        /
        4.0
        *
        m.ETA_SIGMA**4

        -
        problem.chi
        *
        s
        *
        s
    )


def extension_potential(
    problem: FullProblem,
    phi: np.ndarray,
    a: np.ndarray,
) -> np.ndarray:
    """Return the complete same-gauge KLS extension potential."""

    amplitude_sq = (
        np.abs(
            a
        ) ** 2
    )

    trilinear = (
        problem.fixed_result.problem.h_lock
        *
        (
            np.conj(
                phi
            )
            *
            a
            *
            a

            +
            phi
            *
            np.conj(
                a
            )
            *
            np.conj(
                a
            )
        )
    ).real

    p = (
        problem.fixed_result.problem
    )

    return (
        m.LAMBDA_A
        /
        4.0
        *
        (
            amplitude_sq
            -
            m.F_A
            *
            m.F_A
        ) ** 2

        -
        trilinear

        +
        p.c_phi
        *
        (
            np.abs(
                phi
            ) ** 2
            -
            m.ETA_PHI
            *
            m.ETA_PHI
        )

        +
        p.c_a
        *
        (
            amplitude_sq
            -
            m.F_A
            *
            m.F_A
        )

        +
        p.constant
    )


def plaquette(
    ax: np.ndarray,
    az: np.ndarray,
) -> np.ndarray:
    """Return the fundamental noncompact lattice flux angle."""

    return (
        ax[
            :,
            :-1
        ]

        +
        az[
            1:,
            :
        ]

        -
        ax[
            :,
            1:
        ]

        -
        az[
            :-1,
            :
        ]
    )


# ============================================================================
# Full energy and analytic gradient.
# ============================================================================


def objective_and_gradient(
    problem: FullProblem,
    variables: np.ndarray,
) -> tuple[
    float,
    np.ndarray,
]:
    """Return the complete coupled reduced energy and exact gradient."""

    (
        f,
        s,
        a,
        ax,
        az,
    ) = unpack(
        problem,
        variables,
    )

    phi = fields_from_amplitudes(
        problem,
        f,
    )

    ux = np.exp(
        1j
        *
        ax
    )

    uz = np.exp(
        1j
        *
        az
    )

    ux2 = (
        ux
        *
        ux
    )

    uz2 = (
        uz
        *
        uz
    )

    # -----------------------------------------------------------------------
    # Gauge-covariant scalar links.
    # -----------------------------------------------------------------------

    rphi_x = (
        phi[
            1:,
            :
        ]

        -
        ux2
        *
        phi[
            :-1,
            :
        ]
    )

    rphi_z = (
        phi[
            :,
            1:
        ]

        -
        uz2
        *
        phi[
            :,
            :-1
        ]
    )

    ra_x = (
        a[
            1:,
            :
        ]

        -
        ux
        *
        a[
            :-1,
            :
        ]
    )

    ra_z = (
        a[
            :,
            1:
        ]

        -
        uz
        *
        a[
            :,
            :-1
        ]
    )

    rs_x = (
        s[
            1:,
            :
        ]

        -
        s[
            :-1,
            :
        ]
    )

    rs_z = (
        s[
            :,
            1:
        ]

        -
        s[
            :,
            :-1
        ]
    )

    scalar_gradient_energy = float(
        np.sum(
            np.abs(
                rphi_x
            ) ** 2
        )

        +
        np.sum(
            np.abs(
                rphi_z
            ) ** 2
        )

        +
        np.sum(
            np.abs(
                ra_x
            ) ** 2
        )

        +
        np.sum(
            np.abs(
                ra_z
            ) ** 2
        )

        +
        np.sum(
            rs_x
            *
            rs_x
        )

        +
        np.sum(
            rs_z
            *
            rs_z
        )
    )

    flux = plaquette(
        ax,
        az,
    )

    gauge_energy = float(
        0.5
        /
        (
            m.G_X
            *
            m.G_X
            *
            problem.dx
            *
            problem.dx
        )
        *
        np.sum(
            flux
            *
            flux
        )
    )

    v_base = base_potential(
        problem,
        f,
        s,
    )

    v_extension = extension_potential(
        problem,
        phi,
        a,
    )

    potential_energy = float(
        problem.dx
        *
        problem.dx
        *
        np.sum(
            problem.weights
            *
            (
                v_base
                +
                v_extension
            )
        )
    )

    total_energy = (
        scalar_gradient_energy
        +
        gauge_energy
        +
        potential_energy
    )

    # -----------------------------------------------------------------------
    # Complex Phi link gradient dE/dPhi*.
    # -----------------------------------------------------------------------

    g_phi = np.zeros_like(
        phi,
        dtype=complex,
    )

    g_phi[
        1:,
        :
    ] += rphi_x

    g_phi[
        :-1,
        :
    ] += (
        -np.conj(
            ux2
        )
        *
        rphi_x
    )

    g_phi[
        :,
        1:
    ] += rphi_z

    g_phi[
        :,
        :-1
    ] += (
        -np.conj(
            uz2
        )
        *
        rphi_z
    )

    # Project complex Phi variation onto the fixed topological phase.
    g_f = (
        2.0
        *
        np.real(
            np.conj(
                problem.phi_phase
            )
            *
            g_phi
        )
    )

    # -----------------------------------------------------------------------
    # Real sigma link gradient.
    # -----------------------------------------------------------------------

    g_s = np.zeros_like(
        s,
        dtype=float,
    )

    g_s[
        1:,
        :
    ] += (
        2.0
        *
        rs_x
    )

    g_s[
        :-1,
        :
    ] -= (
        2.0
        *
        rs_x
    )

    g_s[
        :,
        1:
    ] += (
        2.0
        *
        rs_z
    )

    g_s[
        :,
        :-1
    ] -= (
        2.0
        *
        rs_z
    )

    # -----------------------------------------------------------------------
    # Complex A link gradient dE/dA*.
    # -----------------------------------------------------------------------

    g_a = np.zeros_like(
        a,
        dtype=complex,
    )

    g_a[
        1:,
        :
    ] += ra_x

    g_a[
        :-1,
        :
    ] += (
        -np.conj(
            ux
        )
        *
        ra_x
    )

    g_a[
        :,
        1:
    ] += ra_z

    g_a[
        :,
        :-1
    ] += (
        -np.conj(
            uz
        )
        *
        ra_z
    )

    # -----------------------------------------------------------------------
    # Potential derivatives.
    # -----------------------------------------------------------------------

    p = (
        problem.fixed_result.problem
    )

    phase_projection = np.real(
        np.conj(
            problem.phi_phase
        )
        *
        a
        *
        a
    )

    dv_df = (
        m.LAMBDA_PHI
        *
        f
        *
        (
            f
            *
            f
            -
            m.ETA_PHI
            *
            m.ETA_PHI
        )

        +
        2.0
        *
        m.BETA
        *
        f
        *
        s
        *
        s

        +
        2.0
        *
        p.c_phi
        *
        f

        -
        2.0
        *
        p.h_lock
        *
        phase_projection
    )

    dv_ds = (
        m.LAMBDA_SIGMA
        *
        s
        *
        (
            s
            *
            s
            -
            m.ETA_SIGMA
            *
            m.ETA_SIGMA
        )

        +
        2.0
        *
        m.BETA
        *
        f
        *
        f
        *
        s

        -
        2.0
        *
        problem.chi
        *
        s
    )

    g_a_potential = (
        m.LAMBDA_A
        /
        2.0
        *
        (
            np.abs(
                a
            ) ** 2
            -
            m.F_A
            *
            m.F_A
        )
        *
        a

        +
        p.c_a
        *
        a

        -
        2.0
        *
        p.h_lock
        *
        phi
        *
        np.conj(
            a
        )
    )

    weight_factor = (
        problem.weights
        *
        problem.dx
        *
        problem.dx
    )

    g_f += (
        weight_factor
        *
        dv_df
    )

    g_s += (
        weight_factor
        *
        dv_ds
    )

    g_a += (
        weight_factor
        *
        g_a_potential
    )

    # -----------------------------------------------------------------------
    # Link-angle gradient.
    #
    # d/da |q-exp(i qcharge a)p|^2
    #
    #   =
    #
    # 2 qcharge Im[q^* exp(i qcharge a) p].
    # -----------------------------------------------------------------------

    g_ax = (
        2.0
        *
        np.imag(
            np.conj(
                a[
                    1:,
                    :
                ]
            )
            *
            ux
            *
            a[
                :-1,
                :
            ]
        )

        +
        4.0
        *
        np.imag(
            np.conj(
                phi[
                    1:,
                    :
                ]
            )
            *
            ux2
            *
            phi[
                :-1,
                :
            ]
        )
    )

    g_az = (
        2.0
        *
        np.imag(
            np.conj(
                a[
                    :,
                    1:
                ]
            )
            *
            uz
            *
            a[
                :,
                :-1
            ]
        )

        +
        4.0
        *
        np.imag(
            np.conj(
                phi[
                    :,
                    1:
                ]
            )
            *
            uz2
            *
            phi[
                :,
                :-1
            ]
        )
    )

    gauge_coefficient = (
        1.0
        /
        (
            m.G_X
            *
            m.G_X
            *
            problem.dx
            *
            problem.dx
        )
    )

    gauge_flux_gradient = (
        gauge_coefficient
        *
        flux
    )

    g_ax[
        :,
        :-1
    ] += gauge_flux_gradient

    g_az[
        1:,
        :
    ] += gauge_flux_gradient

    g_ax[
        :,
        1:
    ] -= gauge_flux_gradient

    g_az[
        :-1,
        :
    ] -= gauge_flux_gradient

    # -----------------------------------------------------------------------
    # Pack gradient in exactly the optimizer-variable ordering.
    # -----------------------------------------------------------------------

    ga_values = (
        g_a[
            problem.a_free
        ]
    )

    gradient = np.concatenate(
        [
            g_f[
                problem.f_free
            ],

            g_s[
                problem.s_free
            ],

            2.0
            *
            ga_values.real,

            2.0
            *
            ga_values.imag,

            g_ax[
                problem.ax_free
            ],

            g_az[
                problem.az_free
            ],
        ]
    )

    return (
        float(
            total_energy
        ),
        gradient,
    )


# ============================================================================
# Validation and solve.
# ============================================================================


def directional_gradient_check(
    problem: FullProblem,
) -> float:
    """Verify the complete coupled analytic gradient by directional differencing."""

    variables = pack_initial(
        problem
    )

    _, gradient = objective_and_gradient(
        problem,
        variables,
    )

    rng = np.random.default_rng(
        20260830
    )

    direction = rng.normal(
        size=variables.size
    )

    direction /= np.linalg.norm(
        direction
    )

    epsilon = 5.0e-7

    e_plus, _ = objective_and_gradient(
        problem,
        variables
        +
        epsilon
        *
        direction,
    )

    e_minus, _ = objective_and_gradient(
        problem,
        variables
        -
        epsilon
        *
        direction,
    )

    finite_difference = (
        e_plus
        -
        e_minus
    ) / (
        2.0
        *
        epsilon
    )

    analytic = float(
        np.dot(
            gradient,
            direction,
        )
    )

    return (
        abs(
            finite_difference
            -
            analytic
        )
        /
        max(
            abs(
                finite_difference
            ),
            abs(
                analytic
            ),
            1.0e-14,
        )
    )


def solve_full_case(
    chi: float,
    n: int,
    box_half: float,
) -> FullResult:
    """Run one simultaneous Phi/sigma/A/gauge relaxation."""

    problem = build_full_problem(
        chi,
        n,
        box_half,
    )

    variables0 = pack_initial(
        problem
    )

    energy_reference, _ = (
        objective_and_gradient(
            problem,
            variables0,
        )
    )

    result = minimize(
        lambda vector: objective_and_gradient(
            problem,
            vector,
        ),
        variables0,
        method="L-BFGS-B",
        jac=True,
        bounds=optimizer_bounds(
            problem
        ),
        options={
            "maxiter":
                OPT_MAXITER,

            "ftol":
                OPT_FTOL,

            "gtol":
                OPT_GTOL,

            "maxls":
                50,

            "maxcor":
                20,
        },
    )

    (
        f,
        s,
        a,
        ax,
        az,
    ) = unpack(
        problem,
        result.x,
    )

    energy_full, gradient = (
        objective_and_gradient(
            problem,
            result.x,
        )
    )

    grad_rms = float(
        np.linalg.norm(
            gradient
        )
        /
        math.sqrt(
            gradient.size
        )
    )

    grad_max = float(
        np.max(
            np.abs(
                gradient
            )
        )
    )

    relaxation_delta_energy = (
        energy_full
        -
        energy_reference
    )

    mu_fixed = float(
        problem.fixed_result.junction_excess_energy
    )

    mu_full = (
        mu_fixed
        +
        relaxation_delta_energy
    )

    delta_sigma2_grid = float(
        problem.dx
        *
        problem.dx
        *
        np.sum(
            problem.weights
            *
            (
                s
                *
                s

                -
                problem.s0
                *
                problem.s0
            )
        )
    )

    sigma2_full = (
        float(
            problem.radial_diag.sigma2
        )
        +
        delta_sigma2_grid
    )

    success = (
        bool(
            result.success
        )

        and
        problem.fixed_result.optimizer_success

        and
        grad_rms
        <
        MAX_GRAD_RMS

        and
        grad_max
        <
        MAX_GRAD_ABS
    )

    return FullResult(
        chi=float(
            chi
        ),

        n=n,
        box_half=box_half,
        dx=problem.dx,

        success=success,
        optimizer_message=str(
            result.message
        ),
        iterations=int(
            result.nit
        ),

        energy_reference=float(
            energy_reference
        ),
        energy_full=float(
            energy_full
        ),
        relaxation_delta_energy=float(
            relaxation_delta_energy
        ),

        mu_fixed=mu_fixed,
        mu_full=float(
            mu_full
        ),

        sigma2_background=float(
            problem.radial_diag.sigma2
        ),
        sigma2_full=float(
            sigma2_full
        ),
        delta_sigma2=float(
            delta_sigma2_grid
        ),

        grad_rms=grad_rms,
        grad_max=grad_max,

        f=f,
        s=s,
        a=a,

        ax=ax,
        az=az,

        problem=problem,
    )


# ============================================================================
# Physical diagnostics.
# ============================================================================


def morphology(
    result: FullResult,
) -> dict[str, float]:
    """Measure wall termination and phase locking after full coupling."""

    p = result.problem

    x = p.fixed_result.problem.x
    X = p.fixed_result.problem.X
    Z = p.fixed_result.problem.Z
    radius = p.fixed_result.problem.radius

    L = p.box_half

    center = int(
        np.argmin(
            np.abs(
                x
            )
        )
    )

    negative = (
        (
            x
            >
            -0.75
            *
            L
        )
        &
        (
            x
            <
            -0.45
            *
            L
        )
    )

    positive = (
        (
            x
            >
            0.45
            *
            L
        )
        &
        (
            x
            <
            0.75
            *
            L
        )
    )

    negative_wall_max = float(
        np.max(
            np.abs(
                result.a[
                    negative,
                    center,
                ]
            )
        )
        /
        m.F_A
    )

    positive_recovery_min = float(
        np.min(
            np.abs(
                result.a[
                    positive,
                    center,
                ]
            )
        )
        /
        m.F_A
    )

    phi = fields_from_amplitudes(
        p,
        result.f,
    )

    a_amp = np.abs(
        result.a
    )

    lock_cosine = (
        np.real(
            np.conj(
                phi
            )
            *
            result.a
            *
            result.a
        )
        /
        np.maximum(
            result.f
            *
            a_amp
            *
            a_amp,
            1.0e-30,
        )
    )

    lock_mask = (
        (
            radius
            >
            30.0
        )

        &
        (
            result.f
            >
            0.90
        )

        &
        (
            a_amp
            >
            0.5
            *
            m.F_A
        )
    )

    phase_lock_rms = float(
        np.sqrt(
            np.mean(
                (
                    1.0
                    -
                    lock_cosine[
                        lock_mask
                    ]
                ) ** 2
            )
        )
    )

    f_change = float(
        np.max(
            np.abs(
                result.f
                -
                p.f0
            )
        )
    )

    sigma_change_rms = float(
        np.sqrt(
            np.mean(
                (
                    result.s
                    -
                    p.s0
                ) ** 2
            )
        )
    )

    a_change_rms_over_f = float(
        np.sqrt(
            np.mean(
                np.abs(
                    result.a
                    -
                    p.a0
                ) ** 2
            )
        )
        /
        m.F_A
    )

    gauge_change_rms = float(
        math.sqrt(
            (
                np.mean(
                    (
                        result.ax
                        -
                        p.ax0
                    ) ** 2
                )

                +
                np.mean(
                    (
                        result.az
                        -
                        p.az0
                    ) ** 2
                )
            )
            /
            2.0
        )
    )

    return {
        "negative_wall_max":
            negative_wall_max,

        "positive_recovery_min":
            positive_recovery_min,

        "phase_lock_rms":
            phase_lock_rms,

        "f_change_max":
            f_change,

        "sigma_change_rms":
            sigma_change_rms,

        "a_change_rms_over_f":
            a_change_rms_over_f,

        "gauge_change_rms":
            gauge_change_rms,

        "core_f":
            float(
                result.f[
                    center,
                    center,
                ]
            ),

        "core_a_over_f":
            float(
                np.abs(
                    result.a[
                        center,
                        center,
                    ]
                )
                /
                m.F_A
            ),
    }


def active_source_diagnostics(
    result: FullResult,
) -> dict[str, float]:
    """Compute same-grid corrected fully coupled junction active source."""

    p = result.problem

    phi_full = fields_from_amplitudes(
        p,
        result.f,
    )

    phi_background = fields_from_amplitudes(
        p,
        p.f0,
    )

    v_base_full = base_potential(
        p,
        result.f,
        result.s,
    )

    v_base_background = base_potential(
        p,
        p.f0,
        p.s0,
    )

    v_ext_full = extension_potential(
        p,
        phi_full,
        result.a,
    )

    v_ext_fixed = extension_potential(
        p,
        phi_background,
        p.a0,
    )

    measure = (
        p.weights
        *
        p.dx
        *
        p.dx
    )

    vint_base_full = float(
        np.sum(
            measure
            *
            v_base_full
        )
    )

    vint_base_background = float(
        np.sum(
            measure
            *
            v_base_background
        )
    )

    vint_ext_full = float(
        np.sum(
            measure
            *
            v_ext_full
        )
    )

    vint_ext_fixed = float(
        np.sum(
            measure
            *
            v_ext_fixed
        )
    )

    sigma2_grid_full = float(
        np.sum(
            measure
            *
            result.s
            *
            result.s
        )
    )

    sigma2_grid_background = float(
        np.sum(
            measure
            *
            p.s0
            *
            p.s0
        )
    )

    flux_full = plaquette(
        result.ax,
        result.az,
    )

    flux_background = plaquette(
        p.ax0,
        p.az0,
    )

    b2_full_integral = float(
        1.0
        /
        (
            m.G_X
            *
            m.G_X
            *
            p.dx
            *
            p.dx
        )
        *
        np.sum(
            flux_full
            *
            flux_full
        )
    )

    b2_background_integral = float(
        1.0
        /
        (
            m.G_X
            *
            m.G_X
            *
            p.dx
            *
            p.dx
        )
        *
        np.sum(
            flux_background
            *
            flux_background
        )
    )

    active_base_background = (
        2.0
        *
        (
            OMEGA_SELECTED**2
            +
            K_SELECTED**2
        )
        *
        sigma2_grid_background

        -
        2.0
        *
        vint_base_background

        +
        b2_background_integral
    )

    active_ext_fixed = (
        -2.0
        *
        vint_ext_fixed
    )

    active_reference = (
        active_base_background
        +
        active_ext_fixed
    )

    active_full = (
        2.0
        *
        (
            OMEGA_SELECTED**2
            +
            K_SELECTED**2
        )
        *
        sigma2_grid_full

        -
        2.0
        *
        (
            vint_base_full
            +
            vint_ext_full
        )

        +
        b2_full_integral
    )

    active_relaxation_delta = (
        active_full
        -
        active_reference
    )

    wall_active = (
        -m.SIGMA_W_RELAXED_018A5
        *
        p.box_half
    )

    fixed_junction_active = (
        active_ext_fixed
        -
        wall_active
    )

    junction_active = (
        fixed_junction_active
        +
        active_relaxation_delta
    )

    delta_u = (
        result.mu_full

        +
        2.0
        *
        OMEGA_SELECTED**2
        *
        result.delta_sigma2
    )

    delta_tyy = (
        -result.mu_full

        +
        2.0
        *
        K_SELECTED**2
        *
        result.delta_sigma2
    )

    transverse_stress_sum = (
        junction_active
        -
        delta_u
        -
        delta_tyy
    )

    active_line_017p_pair = (
        4.0
        *
        result.sigma2_background
        *
        (
            OMEGA_SELECTED**2
            +
            K_SELECTED**2
        )
    )

    pair_perturbation_fraction = (
        2.0
        *
        abs(
            junction_active
        )
        /
        active_line_017p_pair
    )

    return {
        "active_full":
            active_full,

        "active_reference":
            active_reference,

        "active_relaxation_delta":
            active_relaxation_delta,

        "fixed_junction_active":
            fixed_junction_active,

        "junction_active":
            junction_active,

        "delta_u":
            delta_u,

        "delta_tyy":
            delta_tyy,

        "transverse_stress_sum":
            transverse_stress_sum,

        "active_line_017p_pair":
            active_line_017p_pair,

        "pair_perturbation_fraction":
            pair_perturbation_fraction,
    }


# ============================================================================
# EOS / stability.
# ============================================================================


def cubic_discriminant(
    a0: float,
    a1: float,
    a2: float,
    a3: float,
) -> float:
    """Return cubic discriminant."""

    return (
        a1
        *
        a1
        *
        a2
        *
        a2

        -
        4.0
        *
        a1**3
        *
        a3

        -
        4.0
        *
        a0
        *
        a2**3

        -
        27.0
        *
        a0
        *
        a0
        *
        a3
        *
        a3

        +
        18.0
        *
        a0
        *
        a1
        *
        a2
        *
        a3
    )


def extrinsic_stability(
    ct2: float,
    cl2: float,
) -> tuple[
    bool,
    float,
    float,
    int,
]:
    """Apply the journaled 017P m=2..40 cubic stability criterion."""

    passed = True

    min_disc = math.inf
    max_imag = 0.0
    worst_mode = -1

    for mode in range(
        2,
        41,
    ):

        mode2 = float(
            mode
            *
            mode
        )

        a0 = (
            2.0
            *
            (
                cl2
                -
                ct2
            )
            *
            (
                mode2
                -
                1.0
            )
            *
            mode
        )

        a1 = (
            4.0
            *
            ct2
            *
            (
                1.0
                -
                cl2
            )
            *
            (
                mode2
                -
                1.0
            )

            -
            (
                1.0
                +
                ct2
            )
            *
            (
                cl2
                -
                ct2
            )
            *
            (
                mode2
                +
                1.0
            )
        )

        a2 = (
            2.0
            *
            ct2
            *
            (
                cl2
                -
                ct2

                -
                2.0
                *
                (
                    1.0
                    -
                    cl2
                    *
                    ct2
                )
            )
            *
            mode
        )

        a3 = (
            ct2
            *
            (
                1.0
                +
                ct2
            )
            *
            (
                1.0
                -
                cl2
                *
                ct2
            )
        )

        disc = cubic_discriminant(
            a0,
            a1,
            a2,
            a3,
        )

        roots = np.roots(
            [
                a3,
                a2,
                a1,
                a0,
            ]
        )

        root_imag = float(
            np.max(
                np.abs(
                    np.imag(
                        roots
                    )
                )
            )
        )

        if disc < min_disc:
            min_disc = disc
            worst_mode = mode

        max_imag = max(
            max_imag,
            root_imag,
        )

        if (
            disc
            <=
            0.0

            or
            root_imag
            >
            1.0e-8
        ):
            passed = False

    return (
        passed,
        min_disc,
        max_imag,
        worst_mode,
    )


def stationarity(
    mu_junction: float,
    junction_count: int,
) -> dict[str, float | bool]:
    """Apply measured fully coupled junction line energy to wall stationarity."""

    w_eff = (
        W_STAT

        -
        2.0
        *
        math.pi
        *
        junction_count
        *
        mu_junction
        /
        ELL
    )

    if w_eff <= 0.0:
        return {
            "passed":
                False,

            "w_eff":
                w_eff,
        }

    q_req = (
        w_eff
        /
        m.SIGMA_W_RELAXED_018A5
    )

    n_req = (
        q_req
        /
        Q_OVER_N
    )

    n_integer = max(
        1,
        int(
            round(
                n_req
            )
        ),
    )

    q_integer = (
        n_integer
        *
        Q_OVER_N
    )

    radius = (
        q_req
        *
        ELL
        /
        (
            2.0
            *
            math.pi
        )
    )

    mismatch = (
        abs(
            m.SIGMA_W_RELAXED_018A5
            *
            q_integer
            -
            w_eff
        )
        /
        w_eff
    )

    radius_over_wall = (
        radius
        /
        WALL_WIDTH90
    )

    radius_over_core = (
        radius
        /
        m.A_CORE_WIDTH
    )

    passed = (
        radius_over_wall
        >=
        MIN_SCALE_SEPARATION

        and
        radius_over_core
        >=
        MIN_SCALE_SEPARATION

        and
        mismatch
        <=
        MAX_INTEGER_MISMATCH
    )

    return {
        "passed":
            passed,

        "w_eff":
            w_eff,

        "q_req":
            q_req,

        "n_req":
            n_req,

        "n_integer":
            float(
                n_integer
            ),

        "radius":
            radius,

        "mismatch":
            mismatch,

        "radius_over_wall":
            radius_over_wall,

        "radius_over_core":
            radius_over_core,
    }


# ============================================================================
# Cache because domain / resolution / chi sequences overlap.
# ============================================================================

CASE_CACHE: dict[
    tuple[
        float,
        int,
        float,
    ],
    FullResult,
] = {}


def cached_case(
    chi: float,
    n: int,
    box_half: float,
) -> FullResult:
    """Solve or return one already completed coupled case."""

    key = (
        round(
            float(
                chi
            ),
            9,
        ),
        int(
            n
        ),
        float(
            box_half
        ),
    )

    if key not in CASE_CACHE:
        CASE_CACHE[
            key
        ] = solve_full_case(
            chi,
            n,
            box_half,
        )

    return CASE_CACHE[
        key
    ]


# ============================================================================
# Main.
# ============================================================================


def print_case(
    prefix: str,
    result: FullResult,
) -> None:
    """Print one compact fully coupled result."""

    print(
        f"{prefix} "
        f"CHI={result.chi:.9f} "
        f"N={result.n} "
        f"L={result.box_half:.3f} "
        f"DX={result.dx:.12f} "
        f"ITER={result.iterations} "
        f"OPT={'PASS' if result.success else 'FAIL'} "
        f"DELTA_RELAX={result.relaxation_delta_energy:+.15e} "
        f"MU_FIXED={result.mu_fixed:+.15e} "
        f"MU_FULL={result.mu_full:+.15e} "
        f"SIGMA2_FULL={result.sigma2_full:.15e} "
        f"DELTA_SIGMA2={result.delta_sigma2:+.15e} "
        f"GRAD_RMS={result.grad_rms:.6e} "
        f"GRAD_MAX={result.grad_max:.6e}"
    )


def main() -> None:
    """Execute the complete fully coupled local-junction promotion gate."""

    original_chi = float(
        m.CHI_SELECTED
    )

    print(
        "=== ANTIGRAVITY_RESEARCH 018A-6B ==="
    )

    print(
        "QUESTION="
        "DOES_THE_KLS_WALL_END_ON_THE_017P_VORTEX_AFTER_SIMULTANEOUS_PHI_A_SIGMA_GAUGE_RELAXATION"
    )

    print(
        "FULLY_COUPLED_TRANSVERSE_FIELDS="
        "PHI_AMPLITUDE_PLUS_A_COMPLEX_PLUS_SIGMA_AMPLITUDE_PLUS_GAUGE_LINKS"
    )

    print(
        "VORTEX_TOPOLOGICAL_PHASE="
        "UNIT_WINDING_FIXED_GAUGE"
    )

    # ========================================================================
    # Full analytic gradient.
    # ========================================================================

    print(
        "\n=== FULL-COUPLED ANALYTIC GRADIENT CHECK ==="
    )

    gradient_problem = build_full_problem(
        CHI_SELECTED,
        GRADIENT_CHECK_CASE[
            0
        ],
        GRADIENT_CHECK_CASE[
            1
        ],
    )

    gradient_relerr = (
        directional_gradient_check(
            gradient_problem
        )
    )

    gradient_pass = (
        gradient_relerr
        <
        MAX_GRADIENT_CHECK_RELERR
    )

    print(
        "FULL_COUPLED_GRADIENT_DIRECTIONAL_RELERR="
        f"{gradient_relerr:.15e}"
    )

    print(
        "FULL_COUPLED_ANALYTIC_GRADIENT="
        f"{'PASS' if gradient_pass else 'FAIL'}"
    )

    if not gradient_pass:
        print(
            "018A6B_FULLY_COUPLED_2D_KLS_JUNCTION="
            "RED"
        )

        print(
            "NEXT="
            "AUDIT_ANALYTIC_FULL_COUPLED_GRADIENT_BEFORE_SCIENTIFIC_INTERPRETATION"
        )

        m.CHI_SELECTED = original_chi
        return

    # ========================================================================
    # Domain convergence.
    # ========================================================================

    print(
        "\n=== FULL-COUPLED FIXED-DX DOMAIN CONVERGENCE ==="
    )

    domain_results = []

    for (
        n,
        box_half,
    ) in DOMAIN_CASES:

        result = cached_case(
            CHI_SELECTED,
            n,
            box_half,
        )

        domain_results.append(
            result
        )

        print_case(
            "DOMAIN",
            result,
        )

    domain_mu = np.array(
        [
            result.mu_full
            for result
            in domain_results
        ],
        dtype=float,
    )

    domain_mu_spread = (
        float(
            np.max(
                domain_mu
            )
            -
            np.min(
                domain_mu
            )
        )
        /
        max(
            abs(
                float(
                    np.mean(
                        domain_mu
                    )
                )
            ),
            1.0e-30,
        )
    )

    domain_optimizer_pass = all(
        result.success
        for result
        in domain_results
    )

    domain_pass = (
        domain_optimizer_pass
        and
        domain_mu_spread
        <
        MAX_DOMAIN_MU_REL_SPREAD
    )

    print(
        "FULL_COUPLED_DOMAIN_MU_REL_SPREAD="
        f"{domain_mu_spread:.15e}"
    )

    print(
        "FULL_COUPLED_DOMAIN_CONVERGENCE="
        f"{'PASS' if domain_pass else 'FAIL'}"
    )

    domain_model_totals = np.array(
        [
            result.problem.radial_diag.a_string

            +
            m.SIGMA_W_RELAXED_018A5
            *
            result.box_half

            +
            result.mu_full

            for result
            in domain_results
        ],
        dtype=float,
    )

    slope_pass = True

    for index in range(
        len(
            domain_results
        )
        -
        1
    ):

        left = domain_results[
            index
        ]

        right = domain_results[
            index
            +
            1
        ]

        slope = (
            domain_model_totals[
                index
                +
                1
            ]
            -
            domain_model_totals[
                index
            ]
        ) / (
            right.box_half
            -
            left.box_half
        )

        ratio = (
            slope
            /
            m.SIGMA_W_RELAXED_018A5
        )

        print(
            "FULL_DOMAIN_SLOPE "
            f"L1={left.box_half:.3f} "
            f"L2={right.box_half:.3f} "
            f"DE_DL={slope:.15e} "
            f"OVER_SIGMA={ratio:.12f}"
        )

        if (
            abs(
                ratio
                -
                1.0
            )
            >=
            MAX_DOMAIN_SLOPE_RELERR
        ):
            slope_pass = False

    print(
        "FULL_COUPLED_DOMAIN_WALL_SLOPE="
        f"{'PASS' if slope_pass else 'FAIL'}"
    )

    # ========================================================================
    # Resolution convergence.
    # ========================================================================

    print(
        "\n=== FULL-COUPLED FIXED-DOMAIN RESOLUTION CONVERGENCE ==="
    )

    resolution_results = []

    for (
        n,
        box_half,
    ) in RESOLUTION_CASES:

        result = cached_case(
            CHI_SELECTED,
            n,
            box_half,
        )

        resolution_results.append(
            result
        )

        print_case(
            "RESOLUTION",
            result,
        )

    resolution_mu = np.array(
        [
            result.mu_full
            for result
            in resolution_results
        ],
        dtype=float,
    )

    resolution_mu_spread = (
        float(
            np.max(
                resolution_mu
            )
            -
            np.min(
                resolution_mu
            )
        )
        /
        max(
            abs(
                float(
                    np.mean(
                        resolution_mu
                    )
                )
            ),
            1.0e-30,
        )
    )

    resolution_optimizer_pass = all(
        result.success
        for result
        in resolution_results
    )

    resolution_pass = (
        resolution_optimizer_pass
        and
        resolution_mu_spread
        <
        MAX_RESOLUTION_MU_REL_SPREAD
    )

    print(
        "FULL_COUPLED_RESOLUTION_MU_REL_SPREAD="
        f"{resolution_mu_spread:.15e}"
    )

    print(
        "FULL_COUPLED_RESOLUTION_CONVERGENCE="
        f"{'PASS' if resolution_pass else 'FAIL'}"
    )

    selected = resolution_results[
        -1
    ]

    # ========================================================================
    # Fully coupled morphology.
    # ========================================================================

    print(
        "\n=== FULL-COUPLED SELECTED MORPHOLOGY / BACKREACTION ==="
    )

    morph = morphology(
        selected
    )

    for key in (
        "negative_wall_max",
        "positive_recovery_min",
        "phase_lock_rms",
        "f_change_max",
        "sigma_change_rms",
        "a_change_rms_over_f",
        "gauge_change_rms",
        "core_f",
        "core_a_over_f",
    ):
        print(
            f"{key.upper()}="
            f"{float(morph[key]):.15e}"
        )

    termination_pass = (
        morph[
            "negative_wall_max"
        ]
        <
        MAX_NEGATIVE_WALL_A_OVER_F

        and
        morph[
            "positive_recovery_min"
        ]
        >
        MIN_POSITIVE_RECOVERY_A_OVER_F
    )

    phase_lock_pass = (
        morph[
            "phase_lock_rms"
        ]
        <
        MAX_PHASE_LOCK_RMS
    )

    print(
        "FULL_COUPLED_WALL_TERMINATION="
        f"{'PASS' if termination_pass else 'FAIL'}"
    )

    print(
        "FULL_COUPLED_RELATIVE_PHASE_LOCKING="
        f"{'PASS' if phase_lock_pass else 'FAIL'}"
    )

    # ========================================================================
    # Active source and line-stress bookkeeping.
    # ========================================================================

    print(
        "\n=== COMPLETE SELECTED LOCAL LINE-STRESS BOOKKEEPING ==="
    )

    active = active_source_diagnostics(
        selected
    )

    for key in (
        "active_full",
        "active_reference",
        "active_relaxation_delta",
        "fixed_junction_active",
        "junction_active",
        "delta_u",
        "delta_tyy",
        "transverse_stress_sum",
        "active_line_017p_pair",
        "pair_perturbation_fraction",
    ):
        print(
            f"{key.upper()}="
            f"{float(active[key]):+.15e}"
        )

    active_pass = (
        active[
            "pair_perturbation_fraction"
        ]
        <
        MAX_ACTIVE_PAIR_PERTURBATION
    )

    print(
        "FULL_COUPLED_ACTIVE_SOURCE_BUDGET="
        f"{'PASS' if active_pass else 'FAIL'}"
    )

    # ========================================================================
    # Fully coupled chi continuation.
    # ========================================================================

    print(
        "\n=== FULL-COUPLED COMMON-GRID CHI CONTINUATION ==="
    )

    chi_records = []

    for chi in CHI_VALUES:

        result = cached_case(
            chi,
            CHI_CASE[
                0
            ],
            CHI_CASE[
                1
            ],
        )

        a_eff = (
            result.problem.radial_diag.a_string
            +
            result.mu_full
        )

        chi_records.append(
            (
                float(
                    chi
                ),
                float(
                    result.sigma2_full
                ),
                float(
                    a_eff
                ),
                result,
            )
        )

        print(
            "FULL_CHI "
            f"CHI={chi:.9f} "
            f"SIGMA2_FULL={result.sigma2_full:.15e} "
            f"A_STRING={result.problem.radial_diag.a_string:.15e} "
            f"MU_FULL={result.mu_full:+.15e} "
            f"A_EFF={a_eff:.15e} "
            f"OPT={'PASS' if result.success else 'FAIL'}"
        )

    chi_array = np.array(
        [
            record[
                0
            ]
            for record
            in chi_records
        ],
        dtype=float,
    )

    sigma_array = np.array(
        [
            record[
                1
            ]
            for record
            in chi_records
        ],
        dtype=float,
    )

    a_eff_array = np.array(
        [
            record[
                2
            ]
            for record
            in chi_records
        ],
        dtype=float,
    )

    sigma_poly = np.polyfit(
        chi_array,
        sigma_array,
        2,
    )

    a_poly = np.polyfit(
        chi_array,
        a_eff_array,
        2,
    )

    d_sigma = float(
        np.polyval(
            np.polyder(
                sigma_poly
            ),
            CHI_SELECTED,
        )
    )

    d_a_eff = float(
        np.polyval(
            np.polyder(
                a_poly
            ),
            CHI_SELECTED,
        )
    )

    sigma_selected_common = float(
        sigma_array[
            -1
        ]
    )

    a_eff_selected_common = float(
        a_eff_array[
            -1
        ]
    )

    variational_relerr = (
        abs(
            d_a_eff
            +
            sigma_selected_common
        )
        /
        sigma_selected_common
    )

    variational_pass = (
        variational_relerr
        <
        MAX_VARIATIONAL_RELERR
    )

    print(
        "FULL_COUPLED_DA_EFF_DCHI="
        f"{d_a_eff:+.15e}"
    )

    print(
        "FULL_COUPLED_DSIGMA2_DCHI="
        f"{d_sigma:+.15e}"
    )

    print(
        "FULL_COUPLED_VARIATIONAL_RELERR="
        f"{variational_relerr:.15e}"
    )

    print(
        "FULL_COUPLED_VARIATIONAL_IDENTITY="
        f"{'PASS' if variational_pass else 'FAIL'}"
    )

    ct2 = (
        1.0
        /
        (
            1.0
            +
            2.0
            *
            CHI_SELECTED
            *
            sigma_selected_common
            /
            a_eff_selected_common
        )
    )

    cl2 = (
        1.0
        /
        (
            1.0
            +
            2.0
            *
            CHI_SELECTED
            *
            d_sigma
            /
            sigma_selected_common
        )
    )

    eos_pass = (
        0.0
        <
        ct2
        <=
        1.0

        and
        0.0
        <
        cl2
        <=
        1.0
    )

    print(
        "FULL_COUPLED_CT2="
        f"{ct2:.15e}"
    )

    print(
        "FULL_COUPLED_CL2="
        f"{cl2:.15e}"
    )

    print(
        "FULL_COUPLED_EOS_HEALTH="
        f"{'PASS' if eos_pass else 'FAIL'}"
    )

    (
        stability_pass,
        min_disc,
        max_imag,
        worst_mode,
    ) = extrinsic_stability(
        ct2,
        cl2,
    )

    print(
        "FULL_COUPLED_MIN_M2_TO_M40_DISCRIMINANT="
        f"{min_disc:+.15e}"
    )

    print(
        f"FULL_COUPLED_WORST_MODE={worst_mode}"
    )

    print(
        "FULL_COUPLED_MAX_ROOT_IMAG="
        f"{max_imag:.15e}"
    )

    print(
        "FULL_COUPLED_M2_TO_M40_STABILITY="
        f"{'PASS' if stability_pass else 'FAIL'}"
    )

    # ========================================================================
    # Mandatory stationarity.
    # ========================================================================

    print(
        "\n=== FULL-COUPLED MANDATORY JUNCTION STATIONARITY ==="
    )

    stationarity_results = {}

    for count in (
        1,
        2,
    ):

        case = stationarity(
            selected.mu_full,
            count,
        )

        stationarity_results[
            count
        ] = case

        print(
            "FULL_STATIONARITY "
            f"JUNCTION_COUNT={count} "
            f"W_EFF={float(case['w_eff']):.15e} "
            f"Q_REQ={float(case.get('q_req', math.nan)):.15e} "
            f"N_REQ={float(case.get('n_req', math.nan)):.15e} "
            f"N_INT={int(case.get('n_integer', 0.0))} "
            f"R_REQ={float(case.get('radius', math.nan)):.15e} "
            f"R_OVER_WALL90={float(case.get('radius_over_wall', math.nan)):.12f} "
            f"R_OVER_A_CORE={float(case.get('radius_over_core', math.nan)):.12f} "
            f"INTEGER_MISMATCH={float(case.get('mismatch', math.nan)):.15e} "
            f"PASS={'YES' if case['passed'] else 'NO'}"
        )

    one_stationarity = bool(
        stationarity_results[
            1
        ][
            "passed"
        ]
    )

    two_stationarity = bool(
        stationarity_results[
            2
        ][
            "passed"
        ]
    )

    print(
        "FULL_COUPLED_ONE_JUNCTION_STATIONARITY="
        f"{'PASS' if one_stationarity else 'FAIL'}"
    )

    print(
        "FULL_COUPLED_TWO_JUNCTION_STATIONARITY="
        f"{'PASS' if two_stationarity else 'FAIL'}"
    )

    # ========================================================================
    # Decision.
    # ========================================================================

    chi_optimizer_pass = all(
        record[
            3
        ].success
        for record
        in chi_records
    )

    overall_green = (
        gradient_pass

        and
        domain_pass

        and
        slope_pass

        and
        resolution_pass

        and
        termination_pass

        and
        phase_lock_pass

        and
        chi_optimizer_pass

        and
        variational_pass

        and
        eos_pass

        and
        stability_pass

        and
        active_pass

        and
        one_stationarity

        and
        two_stationarity
    )

    print(
        "\n=== 018A-6B DECISION ==="
    )

    print(
        "FULL_COUPLED_ANALYTIC_GRADIENT="
        f"{'PASS' if gradient_pass else 'FAIL'}"
    )

    print(
        "FULL_COUPLED_DOMAIN_CONVERGENCE="
        f"{'PASS' if domain_pass else 'FAIL'}"
    )

    print(
        "FULL_COUPLED_DOMAIN_WALL_SLOPE="
        f"{'PASS' if slope_pass else 'FAIL'}"
    )

    print(
        "FULL_COUPLED_RESOLUTION_CONVERGENCE="
        f"{'PASS' if resolution_pass else 'FAIL'}"
    )

    print(
        "FULL_COUPLED_WALL_TERMINATION="
        f"{'PASS' if termination_pass else 'FAIL'}"
    )

    print(
        "FULL_COUPLED_RELATIVE_PHASE_LOCKING="
        f"{'PASS' if phase_lock_pass else 'FAIL'}"
    )

    print(
        "FULL_COUPLED_CHI_CONTINUATION="
        f"{'PASS' if chi_optimizer_pass else 'FAIL'}"
    )

    print(
        "FULL_COUPLED_VARIATIONAL_IDENTITY="
        f"{'PASS' if variational_pass else 'FAIL'}"
    )

    print(
        "FULL_COUPLED_EOS_HEALTH="
        f"{'PASS' if eos_pass else 'FAIL'}"
    )

    print(
        "FULL_COUPLED_M2_TO_M40_STABILITY="
        f"{'PASS' if stability_pass else 'FAIL'}"
    )

    print(
        "FULL_COUPLED_ACTIVE_SOURCE_BUDGET="
        f"{'PASS' if active_pass else 'FAIL'}"
    )

    print(
        "FULL_COUPLED_ONE_JUNCTION_STATIONARITY="
        f"{'PASS' if one_stationarity else 'FAIL'}"
    )

    print(
        "FULL_COUPLED_TWO_JUNCTION_STATIONARITY="
        f"{'PASS' if two_stationarity else 'FAIL'}"
    )

    print(
        "018A6B_FULLY_COUPLED_2D_KLS_JUNCTION="
        f"{'GREEN' if overall_green else 'RED'}"
    )

    if overall_green:
        print(
            "FULLY_COUPLED_LOCAL_2D_KLS_JUNCTION="
            "SUPPORTED"
        )

        print(
            "NEXT="
            "018A7_COMPLETE_MICROSCOPIC_GRAVITY_CLOSEOUT_WITH_MEASURED_WALL_AND_JUNCTION_STRESS"
        )
    else:
        print(
            "FULLY_COUPLED_LOCAL_2D_KLS_JUNCTION="
            "NOT_ESTABLISHED"
        )

        print(
            "NEXT="
            "IDENTIFY_FAILED_FULL_COUPLED_CHANNEL_BEFORE_ANY_018A_GRAVITY_PROMOTION"
        )

    print(
        "FINITE_PAYLOAD_GRAVITY_WITH_COMPLETE_NEW_SECTOR="
        "NOT_YET_TESTED"
    )

    print(
        "POSITIVE_TOTAL_ACTIVE_MASS_WITH_COMPLETE_NEW_SECTOR="
        "NOT_YET_TESTED"
    )

    print(
        "FULL_018A_GATE="
        "NOT_YET_GREEN"
    )

    print(
        "018B_FULL_FINITE_THICKNESS_DRUM="
        "NOT_YET_AUTHORIZED"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE="
        "NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_018A_FULLY_COUPLED_LOCAL_2D_KLS_JUNCTION"
    )

    m.CHI_SELECTED = original_chi


if __name__ == "__main__":
    main()
