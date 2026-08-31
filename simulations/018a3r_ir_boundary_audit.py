"""Simulation 018A-3R — global-string infrared boundary audit.

PURPOSE
-------
Determine whether the only failed numerical-control test in Simulation
018A-3 was caused by an artificial finite-domain boundary condition imposed
on the separate nonthermal global-string amplitude.

018A-3 found a strong wall-pull resistance basin:

    kappa_fraction = 0.40, 0.50, 0.60, 0.625

all passed the baseline-shape and relaxed-shape force/barrier tests.

At the selected healthy point

    kappa_fraction = 0.625

the relaxed calculation found approximately

    max(F_bind) / sigma_W = 3.67

with a stable displaced equilibrium and positive escape barrier.

The FFT discretization itself converged extremely strongly.

However, changing the radial BVP domain from R_max=60 to R_max=80 changed the
force ratio by approximately 14.7 percent.

This failed the declared radial-profile convergence requirement and correctly
prevented promotion.

SCIENTIFIC QUESTION
-------------------
Is that radial-domain dependence a physical failure of junction binding, or
is it caused by imposing the incorrect finite-radius boundary condition

    rho(R_max) = F

on a global string whose amplitude reaches vacuum only algebraically?

GLOBAL-STRING ASYMPTOTICS
-------------------------
The radial global-string equation outside the interacting core is

    rho'' + rho'/r
      - rho/r^2
      - lambda_A (rho^2 - F^2) rho
      = 0.

Write

    rho = F(1-u).

For large radius the leading asymptotic behavior is

    u
      ~
      1 / (m_r^2 r^2)

where

    m_r^2
      =
      2 lambda_A F^2.

Therefore

    rho(r)
      =
      F [
          1
          -
          1/(m_r^2 r^2)
          +
          O(r^-4)
        ].

Consequently a finite-domain Dirichlet condition

    rho(R_max)=F

forces the amplitude to vacuum too rapidly and can deform the profile inward
when m_r R_max is only moderately large.

AUDIT STRATEGY
--------------
Do not trust a hand-written asymptotic series as the primary correction.

Instead:

1. solve an isolated global-string radial BVP on a very large reference
   domain;
2. verify that two different very-large domains agree;
3. use the resulting numerical asymptotic profile to supply the correct
   rho(R_max) value to the coupled 017P + wall-string radial BVP;
4. extend rho outside each coupled BVP by the same numerical global-string
   tail rather than setting it abruptly to F;
5. smoothly turn off the isotropic global-string tail near the explicit
   breaking scale 1/m_A, because the true wall makes the far field
   anisotropic there;
6. repeat the wall-pull force and escape-barrier calculation at several
   radial BVP sizes.

This isolates the local junction from the known artificial outer-boundary
condition without pretending that the radial model remains exact through the
full wall region.

REFERENCE GLOBAL STRING
-----------------------
The isolated reference problem uses

    rho(0)=0
    rho(R_ref)=F

with R_ref chosen hundreds of core lengths away.

Two reference domains are used:

    R_ref = 800
    R_ref = 1600.

Agreement at the radii relevant to the composite BVP is required before the
tail is used.

MATCHED COMPOSITE OUTER CONDITION
---------------------------------
For a composite BVP ending at R_max, replace

    rho(R_max)=F

with

    rho(R_max)=rho_global_reference(R_max).

The 017P gauged vortex, superconducting condensate and gauge field retain
their ordinary asymptotic vacuum conditions because their tails are
short-ranged compared with the global-string amplitude tail.

CORRELATION TAIL
----------------
When constructing the displaced-core overlap:

- inside R_max, use the fully relaxed coupled rho profile;
- outside R_max, use the isolated global-string reference profile;
- near the explicit-breaking scale

      r_IR = 1/m_A

  smoothly taper the isotropic amplitude-tail correction to vacuum.

This taper is NOT the actual two-dimensional wall.

It is only an infrared matching prescription for testing whether the local
restoring-force maximum is sensitive to the artificial radial BVP boundary.

Three taper-start fractions are tested:

    0.70 r_IR
    0.80 r_IR
    0.90 r_IR.

A real local core-binding result should not depend strongly on this arbitrary
far-field taper because the restoring-force maximum found in 018A-3 occurs
near d ~ 20-30, well inside r_IR.

SELECTED COUPLING
-----------------
The primary audit point is

    kappa_fraction = 0.625.

018A-2 showed this point to be:

    quartically bounded;
    energetically binding;
    EOS healthy;
    extrinsically stable for m=2,...,40;
    nonmarginal relative to the observed stability boundary near 0.65-0.70.

RADIAL DOMAINS
--------------
The corrected composite problem is solved at

    R_max = 60
    R_max = 80
    R_max = 100.

All remain at or below the explicit-breaking scale

    1/m_A ~ 133.33.

PRIMARY OBSERVABLE
------------------
For each corrected profile compute

    R_force
      =
      max(F_bind) / sigma_W.

Also reconstruct:

    stable displaced equilibrium;
    escape saddle;
    positive barrier.

PROMOTION CONDITION
-------------------
The IR-boundary audit passes only if:

1. the two very-large isolated-global-string references agree;
2. all corrected R_max cases retain force margin > 1.25;
3. all corrected R_max cases retain a stable equilibrium and positive barrier;
4. the relative spread of R_force across R_max=60,80,100 is <= 3 percent;
5. the selected corrected R_max=80 force ratio changes by <=3 percent when the
   far-tail taper start is moved between 0.70, 0.80 and 0.90 r_IR.

If these hold, the original 018A-3 radial-domain failure is classified as
consistent with a finite-box global-string boundary artifact.

If they do not hold, the separate-wall junction remains genuinely
unconverged and must not proceed to the full 2D junction.

BLIND WILDCARD POLICY
---------------------
The user's numbers

    1.6
    1.875
    3.125
    0.625
    5

remain blind auxiliary controls only.

The physically motivated audit is performed first.

For this run the existing 0.625 selected coupling already happens to coincide
with one member of that blind set. No physical significance is assigned to
that coincidence.

UNITS
-----
Natural units and the dimensionless 017P normalization are used.

LIMITATIONS
-----------
A green IR repair does NOT establish:

- the true 2D explicit-breaking string-wall junction;
- the full microscopic junction stress tensor;
- finite-payload gravity after the true junction;
- full field stability;
- nonlinear Einstein-matter consistency;
- practical energy scaling;
- a practical antigravity device.

A green result only restores the translational junction-force preflight and
justifies the real two-dimensional 018A junction calculation.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_018A_GLOBAL_STRING_IR_BOUNDARY_AUDIT
"""

from __future__ import annotations

from dataclasses import dataclass
import importlib.util
import math
from pathlib import Path
import sys

import numpy as np
from scipy.integrate import solve_bvp
from scipy.interpolate import CubicSpline
from scipy.signal import fftconvolve


ROOT = Path(__file__).resolve().parents[1]

CORE_PATH = (
    ROOT
    / "simulations"
    / "018a2_nonthermal_core_binding_preflight.py"
)

GATE3_PATH = (
    ROOT
    / "simulations"
    / "018a3_wall_pull_vs_binding_force_gate.py"
)


def load_module(
    name: str,
    path: Path,
):
    """Load one Python file safely under Python 3.13."""

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


core = load_module(
    "ag018a2_ir_audit",
    CORE_PATH,
)

gate3 = load_module(
    "ag018a3_ir_audit",
    GATE3_PATH,
)


SELECTED_KF = 0.625

GLOBAL_REFERENCE_DOMAINS = (
    800.0,
    1600.0,
)

COMPOSITE_RMAX_VALUES = (
    60.0,
    80.0,
    100.0,
)

PRIMARY_TAPER_START = 0.80

TAPER_START_VALUES = (
    0.70,
    0.80,
    0.90,
)

FFT_BOX_HALF = 280.0
FFT_REQUESTED_DX = 0.70

DISPLACEMENT_MAX = 110.0

REFERENCE_TOL = 2.0e-5
FORCE_RATIO_SPREAD_MAX = 0.03
TAPER_FORCE_SPREAD_MAX = 0.03
FORCE_RATIO_MIN = 1.25

GLOBAL_BVP_TOL = 5.0e-8
COMPOSITE_BVP_TOL = 2.0e-6

MAX_NODES = 40000


@dataclass
class TailReference:
    """One isolated global-string radial solution."""

    rmax: float
    solution: object


def global_mass_sq() -> float:
    """Return the radial Higgs mass squared in the core approximation."""

    return (
        2.0
        *
        core.LAMBDA_A
        *
        core.F_PHASE
        *
        core.F_PHASE
    )


def isolated_global_guess(
    r: np.ndarray,
) -> np.ndarray:
    """Smooth guess for the isolated global-string magnitude."""

    rho = (
        core.F_PHASE
        *
        np.tanh(
            core.M_R
            *
            r
        )
    )

    rho_p = (
        core.F_PHASE
        *
        core.M_R
        /
        np.cosh(
            np.minimum(
                core.M_R
                *
                r,
                50.0,
            )
        ) ** 2
    )

    return np.vstack(
        [
            rho,
            rho_p,
        ]
    )


def solve_isolated_global(
    rmax: float,
    previous=None,
) -> TailReference:
    """Solve the isolated global-string amplitude to a very large radius."""

    r = np.geomspace(
        core.R0,
        rmax,
        1400,
    )

    if previous is None:
        guess = isolated_global_guess(
            r
        )
    else:
        old_rmax = float(
            previous.rmax
        )

        clipped = np.clip(
            r,
            core.R0,
            old_rmax,
        )

        guess = previous.solution.sol(
            clipped
        )

        beyond = (
            r
            >
            old_rmax
        )

        if np.any(
            beyond
        ):
            guess[
                0,
                beyond,
            ] = (
                core.F_PHASE
            )

            guess[
                1,
                beyond,
            ] = 0.0

    def ode(
        rr: np.ndarray,
        y: np.ndarray,
    ) -> np.ndarray:
        rho = y[0]
        rho_p = y[1]

        rr_safe = np.maximum(
            rr,
            1.0e-12,
        )

        rho_pp = (
            -rho_p
            /
            rr_safe
            +
            rho
            /
            (
                rr_safe
                *
                rr_safe
            )
            +
            core.LAMBDA_A
            *
            (
                rho
                *
                rho
                -
                core.F_PHASE
                *
                core.F_PHASE
            )
            *
            rho
        )

        return np.vstack(
            [
                rho_p,
                rho_pp,
            ]
        )

    def bc(
        ya: np.ndarray,
        yb: np.ndarray,
    ) -> np.ndarray:
        return np.array(
            [
                ya[0],
                yb[0]
                -
                core.F_PHASE,
            ]
        )

    solution = solve_bvp(
        ode,
        bc,
        r,
        guess,
        tol=GLOBAL_BVP_TOL,
        max_nodes=MAX_NODES,
    )

    if solution.status != 0:
        raise RuntimeError(
            "isolated global-string BVP failed: "
            f"{solution.message}"
        )

    return TailReference(
        rmax=rmax,
        solution=solution,
    )


def rho_reference(
    reference: TailReference,
    radius: np.ndarray | float,
) -> np.ndarray:
    """Evaluate the large-domain isolated global-string amplitude."""

    arr = np.asarray(
        radius,
        dtype=float,
    )

    clipped = np.clip(
        arr,
        core.R0,
        reference.rmax,
    )

    values = reference.solution.sol(
        clipped
    )[0]

    values = np.asarray(
        values,
        dtype=float,
    )

    values = np.where(
        arr
        <
        core.R0,
        0.0,
        values,
    )

    values = np.where(
        arr
        >
        reference.rmax,
        core.F_PHASE,
        values,
    )

    return values


def solve_matched_composite(
    *,
    chi: float,
    fraction: float,
    rmax: float,
    tail_reference: TailReference,
    previous=None,
):
    """Solve the coupled composite with a matched global-string outer value."""

    if not (
        0.0
        <=
        fraction
        <
        1.0
    ):
        raise ValueError(
            "fraction must satisfy 0 <= fraction < 1"
        )

    kappa = (
        core.kappa_from_fraction(
            fraction
        )
    )

    rho_outer = float(
        rho_reference(
            tail_reference,
            rmax,
        )
    )

    r = np.geomspace(
        core.R0,
        rmax,
        core.BASE_GRID_POINTS,
    )

    if previous is None:
        guess = core.initial_guess(
            r
        )
    else:
        previous_rmax = float(
            previous.x[-1]
        )

        clipped = np.clip(
            r,
            core.R0,
            previous_rmax,
        )

        guess = previous.sol(
            clipped
        )

        beyond = (
            r
            >
            previous_rmax
        )

        if np.any(
            beyond
        ):
            guess[
                0,
                beyond,
            ] = core.ETA_PHI

            guess[
                2,
                beyond,
            ] = 0.0

            guess[
                4,
                beyond,
            ] = (
                core.VORTEX_WINDING
                /
                core.GAUGE_G
            )

            guess[
                6,
                beyond,
            ] = rho_reference(
                tail_reference,
                r[
                    beyond
                ],
            )

            guess[
                1,
                beyond,
            ] = 0.0

            guess[
                3,
                beyond,
            ] = 0.0

            guess[
                5,
                beyond,
            ] = 0.0

            guess[
                7,
                beyond,
            ] = np.gradient(
                guess[
                    6,
                    beyond,
                ],
                r[
                    beyond
                ],
            )

    def ode(
        rr: np.ndarray,
        y: np.ndarray,
    ) -> np.ndarray:
        (
            f,
            fp,
            s,
            sp,
            gauge,
            gauge_p,
            rho,
            rho_p,
        ) = y

        rr_safe = np.maximum(
            rr,
            1.0e-12,
        )

        angular = (
            (
                core.VORTEX_WINDING
                -
                core.GAUGE_G
                *
                gauge
            )
            /
            rr_safe
        ) ** 2

        f_pp = (
            -fp
            /
            rr_safe
            +
            (
                0.5
                *
                core.LAMBDA_PHI
                *
                (
                    f
                    *
                    f
                    -
                    core.ETA_PHI
                    *
                    core.ETA_PHI
                )
                +
                core.BETA
                *
                s
                *
                s
                +
                angular
                -
                0.25
                *
                kappa
                *
                (
                    rho
                    *
                    rho
                    -
                    core.F_PHASE
                    *
                    core.F_PHASE
                )
            )
            *
            f
        )

        s_pp = (
            -sp
            /
            rr_safe
            +
            (
                0.5
                *
                core.LAMBDA_SIGMA
                *
                (
                    s
                    *
                    s
                    -
                    core.ETA_SIGMA
                    *
                    core.ETA_SIGMA
                )
                +
                core.BETA
                *
                f
                *
                f
                -
                chi
            )
            *
            s
        )

        gauge_pp = (
            gauge_p
            /
            rr_safe
            -
            2.0
            *
            core.GAUGE_G
            *
            f
            *
            f
            *
            (
                core.VORTEX_WINDING
                -
                core.GAUGE_G
                *
                gauge
            )
        )

        rho_pp = (
            -rho_p
            /
            rr_safe
            +
            rho
            /
            (
                rr_safe
                *
                rr_safe
            )
            +
            (
                core.LAMBDA_A
                *
                (
                    rho
                    *
                    rho
                    -
                    core.F_PHASE
                    *
                    core.F_PHASE
                )
                -
                0.5
                *
                kappa
                *
                (
                    f
                    *
                    f
                    -
                    core.ETA_PHI
                    *
                    core.ETA_PHI
                )
            )
            *
            rho
        )

        return np.vstack(
            [
                fp,
                f_pp,
                sp,
                s_pp,
                gauge_p,
                gauge_pp,
                rho_p,
                rho_pp,
            ]
        )

    def bc(
        ya: np.ndarray,
        yb: np.ndarray,
    ) -> np.ndarray:
        return np.array(
            [
                ya[0],
                ya[3],
                ya[4],
                ya[6],

                yb[0]
                -
                core.ETA_PHI,

                yb[2],

                yb[4]
                -
                core.VORTEX_WINDING
                /
                core.GAUGE_G,

                yb[6]
                -
                rho_outer,
            ]
        )

    solution = solve_bvp(
        ode,
        bc,
        r,
        guess,
        tol=COMPOSITE_BVP_TOL,
        max_nodes=MAX_NODES,
    )

    if solution.status != 0:
        raise RuntimeError(
            "matched composite BVP failed: "
            f"{solution.message}"
        )

    return solution


def smooth_tail_weight(
    radius: np.ndarray,
    start_fraction: float,
) -> np.ndarray:
    """Smoothly suppress isotropic tail near the explicit-breaking scale."""

    r_ir = (
        1.0
        /
        core.M_A
    )

    start = (
        start_fraction
        *
        r_ir
    )

    weight = np.ones_like(
        radius,
        dtype=float,
    )

    outer = (
        radius
        >=
        r_ir
    )

    transition = (
        (radius > start)
        &
        (radius < r_ir)
    )

    weight[
        outer
    ] = 0.0

    u = (
        radius[
            transition
        ]
        -
        start
    ) / (
        r_ir
        -
        start
    )

    weight[
        transition
    ] = (
        0.5
        *
        (
            1.0
            +
            np.cos(
                math.pi
                *
                u
            )
        )
    )

    return weight


def odd_grid_count(
    box_half: float,
    requested_dx: float,
) -> int:
    """Return an odd Cartesian grid count."""

    n = int(
        round(
            2.0
            *
            box_half
            /
            requested_dx
        )
    ) + 1

    if n % 2 == 0:
        n += 1

    return max(
        n,
        101,
    )


def matched_correlation(
    solution,
    *,
    profile_rmax: float,
    tail_reference: TailReference,
    taper_start_fraction: float,
) -> tuple[
    np.ndarray,
    np.ndarray,
    float,
    int,
]:
    """Build the displaced interaction correlation with matched IR tail."""

    n = odd_grid_count(
        FFT_BOX_HALF,
        FFT_REQUESTED_DX,
    )

    x = np.linspace(
        -FFT_BOX_HALF,
        FFT_BOX_HALF,
        n,
    )

    dx = float(
        x[1]
        -
        x[0]
    )

    X, Y = np.meshgrid(
        x,
        x,
        indexing="ij",
    )

    radius = np.sqrt(
        X
        *
        X
        +
        Y
        *
        Y
    )

    flat = radius.ravel()

    inside = (
        flat
        <=
        profile_rmax
    )

    clipped = np.clip(
        flat,
        core.R0,
        profile_rmax,
    )

    values = solution.sol(
        clipped
    )

    f = values[0].reshape(
        radius.shape
    )

    rho = values[6].reshape(
        radius.shape
    )

    inside_2d = inside.reshape(
        radius.shape
    )

    f = np.array(
        f,
        copy=True,
    )

    rho = np.array(
        rho,
        copy=True,
    )

    f[
        ~inside_2d
    ] = core.ETA_PHI

    rho_reference_full = (
        rho_reference(
            tail_reference,
            radius,
        )
    )

    tail_weight = (
        smooth_tail_weight(
            radius,
            taper_start_fraction,
        )
    )

    rho_matched_tail = (
        core.F_PHASE
        +
        tail_weight
        *
        (
            rho_reference_full
            -
            core.F_PHASE
        )
    )

    rho[
        ~inside_2d
    ] = (
        rho_matched_tail[
            ~inside_2d
        ]
    )

    axis = (
        radius
        <
        core.R0
    )

    f[
        axis
    ] = 0.0

    rho[
        axis
    ] = 0.0

    f_deficit = (
        f
        *
        f
        -
        core.ETA_PHI
        *
        core.ETA_PHI
    )

    rho_deficit = (
        rho
        *
        rho
        -
        core.F_PHASE
        *
        core.F_PHASE
    )

    correlation = (
        fftconvolve(
            f_deficit,
            rho_deficit,
            mode="same",
        )
        *
        dx
        *
        dx
    )

    center = (
        n
        //
        2
    )

    displacement = (
        x[
            center:
        ]
        -
        x[
            center
        ]
    )

    line = correlation[
        center:,
        center,
    ]

    keep = (
        displacement
        <=
        DISPLACEMENT_MAX
    )

    return (
        displacement[
            keep
        ],
        line[
            keep
        ],
        dx,
        n,
    )


def interaction_energy(
    displacement: np.ndarray,
    correlation: np.ndarray,
    fraction: float,
) -> np.ndarray:
    """Convert correlation to local junction interaction energy."""

    del displacement

    kappa = (
        core.kappa_from_fraction(
            fraction
        )
    )

    energy = (
        -0.25
        *
        kappa
        *
        correlation
    )

    return (
        energy
        -
        float(
            energy[-1]
        )
    )


@dataclass
class Metrics:
    """Force and metastability observables."""

    force_ratio: float
    stable_d: float
    unstable_d: float
    barrier: float
    stable_curvature: float
    unstable_curvature: float
    passed: bool


def interpolate_root(
    x0: float,
    x1: float,
    y0: float,
    y1: float,
) -> float:
    """Linearly interpolate one sign-changing root."""

    if y1 == y0:
        return (
            0.5
            *
            (
                x0
                +
                x1
            )
        )

    return (
        x0
        -
        y0
        *
        (
            x1
            -
            x0
        )
        /
        (
            y1
            -
            y0
        )
    )


def calculate_metrics(
    displacement: np.ndarray,
    energy: np.ndarray,
    *,
    eta_relax: float,
    sigma_wall: float,
) -> Metrics:
    """Calculate force ratio and metastable barrier."""

    eta = float(
        np.clip(
            eta_relax,
            0.0,
            1.0,
        )
    )

    spline = CubicSpline(
        displacement,
        energy,
        bc_type="natural",
    )

    dense = np.linspace(
        float(
            displacement[0]
        ),
        float(
            displacement[-1]
        ),
        16001,
    )

    force = (
        eta
        *
        spline(
            dense,
            1,
        )
    )

    force_ratio = (
        float(
            np.max(
                force
            )
        )
        /
        sigma_wall
    )

    balance = (
        force
        -
        sigma_wall
    )

    upward = np.where(
        (
            balance[:-1]
            <
            0.0
        )
        &
        (
            balance[1:]
            >=
            0.0
        )
    )[0]

    if len(
        upward
    ) == 0:
        return Metrics(
            force_ratio=force_ratio,
            stable_d=math.nan,
            unstable_d=math.nan,
            barrier=math.nan,
            stable_curvature=math.nan,
            unstable_curvature=math.nan,
            passed=False,
        )

    i_stable = int(
        upward[0]
    )

    stable_d = (
        interpolate_root(
            dense[
                i_stable
            ],
            dense[
                i_stable
                +
                1
            ],
            balance[
                i_stable
            ],
            balance[
                i_stable
                +
                1
            ],
        )
    )

    downward = np.where(
        (
            np.arange(
                len(
                    balance
                )
                -
                1
            )
            >
            i_stable
        )
        &
        (
            balance[:-1]
            >=
            0.0
        )
        &
        (
            balance[1:]
            <
            0.0
        )
    )[0]

    if len(
        downward
    ) == 0:
        return Metrics(
            force_ratio=force_ratio,
            stable_d=stable_d,
            unstable_d=math.nan,
            barrier=math.nan,
            stable_curvature=float(
                eta
                *
                spline(
                    stable_d,
                    2,
                )
            ),
            unstable_curvature=math.nan,
            passed=False,
        )

    i_unstable = int(
        downward[0]
    )

    unstable_d = (
        interpolate_root(
            dense[
                i_unstable
            ],
            dense[
                i_unstable
                +
                1
            ],
            balance[
                i_unstable
            ],
            balance[
                i_unstable
                +
                1
            ],
        )
    )

    stable_curvature = float(
        eta
        *
        spline(
            stable_d,
            2,
        )
    )

    unstable_curvature = float(
        eta
        *
        spline(
            unstable_d,
            2,
        )
    )

    def effective_energy(
        d: float,
    ) -> float:
        return float(
            eta
            *
            (
                spline(d)
                -
                spline(0.0)
            )
            -
            sigma_wall
            *
            d
        )

    barrier = (
        effective_energy(
            unstable_d
        )
        -
        effective_energy(
            stable_d
        )
    )

    passed = (
        force_ratio
        >
        FORCE_RATIO_MIN
        and
        stable_curvature
        >
        0.0
        and
        unstable_curvature
        <
        0.0
        and
        barrier
        >
        0.0
    )

    return Metrics(
        force_ratio=force_ratio,
        stable_d=stable_d,
        unstable_d=unstable_d,
        barrier=barrier,
        stable_curvature=stable_curvature,
        unstable_curvature=unstable_curvature,
        passed=passed,
    )


def main() -> None:
    """Run the repaired infrared-boundary convergence audit."""

    print(
        "=== ANTIGRAVITY_RESEARCH 018A-3R ==="
    )

    print(
        "QUESTION="
        "IS_018A3_RADIAL_NONCONVERGENCE_A_FINITE_BOX_GLOBAL_STRING_ARTIFACT"
    )

    print(
        "\n=== GLOBAL STRING ASYMPTOTIC SCALE ==="
    )

    m2 = (
        global_mass_sq()
    )

    m = math.sqrt(
        m2
    )

    print(
        f"M_RADIAL_SQ={m2:.15e}"
    )

    print(
        f"M_RADIAL={m:.15e}"
    )

    print(
        f"ONE_OVER_M_RADIAL={1.0 / m:.15e}"
    )

    print(
        f"ONE_OVER_M_A={1.0 / core.M_A:.15e}"
    )

    print(
        "\n=== VERY-LARGE GLOBAL-STRING REFERENCES ==="
    )

    references = []

    previous = None

    for rmax in GLOBAL_REFERENCE_DOMAINS:
        reference = (
            solve_isolated_global(
                rmax,
                previous=previous,
            )
        )

        references.append(
            reference
        )

        previous = reference

        print(
            "GLOBAL_REFERENCE "
            f"RMAX={rmax:.1f} "
            f"NODES={reference.solution.x.size} "
            f"MAX_RMS_RESIDUAL="
            f"{float(np.max(reference.solution.rms_residuals)):.15e}"
        )

    reference_a = (
        references[0]
    )

    reference_b = (
        references[1]
    )

    check_radii = np.array(
        COMPOSITE_RMAX_VALUES,
        dtype=float,
    )

    rho_a = (
        rho_reference(
            reference_a,
            check_radii,
        )
    )

    rho_b = (
        rho_reference(
            reference_b,
            check_radii,
        )
    )

    reference_relerr = (
        np.max(
            np.abs(
                rho_a
                -
                rho_b
            )
            /
            core.F_PHASE
        )
    )

    for (
        radius,
        value_a,
        value_b,
    ) in zip(
        check_radii,
        rho_a,
        rho_b,
    ):
        leading_deficit = (
            1.0
            /
            (
                m2
                *
                radius
                *
                radius
            )
        )

        print(
            "TAIL_CHECK "
            f"R={radius:.1f} "
            f"RHO_REF800_OVER_F={value_a / core.F_PHASE:.12f} "
            f"RHO_REF1600_OVER_F={value_b / core.F_PHASE:.12f} "
            f"LEADING_ASYMPTOTIC_DEFICIT={leading_deficit:.12e}"
        )

    print(
        f"GLOBAL_REFERENCE_MAX_REL_DIFF={reference_relerr:.15e}"
    )

    reference_pass = (
        reference_relerr
        <=
        REFERENCE_TOL
    )

    print(
        "GLOBAL_REFERENCE_CONVERGENCE="
        f"{'PASS' if reference_pass else 'FAIL'}"
    )

    tail_reference = (
        reference_b
    )

    print(
        "\n=== MICROSCOPIC WALL FORCE ==="
    )

    wall = (
        gate3.wall_mod.solve_planar_wall(
            gate3.wall_mod.F_PHASE,
            gate3.wall_mod.MASS_HIERARCHY,
            12.0,
        )
    )

    sigma_wall = float(
        wall[
            "tension"
        ]
    )

    print(
        f"SIGMA_W={sigma_wall:.15e}"
    )

    print(
        f"ACTIVE_OVER_SIGMA={wall['active_over_tension']:+.15e}"
    )

    assert (
        abs(
            wall[
                "active_over_tension"
            ]
            +
            1.0
        )
        <
        1.0e-5
    )

    print(
        "MICROSCOPIC_WALL_RECONSTRUCTION=PASS"
    )

    print(
        "\n=== MATCHED-TAIL COMPOSITE DOMAIN AUDIT ==="
    )

    domain_records = []

    previous_base = None
    previous_selected = None

    for rmax in COMPOSITE_RMAX_VALUES:

        base_solution = (
            solve_matched_composite(
                chi=core.CHI_SELECTED,
                fraction=0.0,
                rmax=rmax,
                tail_reference=tail_reference,
                previous=previous_base,
            )
        )

        selected_solution = (
            solve_matched_composite(
                chi=core.CHI_SELECTED,
                fraction=SELECTED_KF,
                rmax=rmax,
                tail_reference=tail_reference,
                previous=previous_selected,
            )
        )

        previous_base = (
            base_solution
        )

        previous_selected = (
            selected_solution
        )

        base_diag = (
            core.diagnose(
                base_solution,
                chi=core.CHI_SELECTED,
                kappa_fraction=0.0,
                rmax=rmax,
            )
        )

        selected_diag = (
            core.diagnose(
                selected_solution,
                chi=core.CHI_SELECTED,
                kappa_fraction=SELECTED_KF,
                rmax=rmax,
            )
        )

        delta_total = (
            selected_diag.a_total_ir
            -
            base_diag.a_total_ir
        )

        eta = (
            abs(
                delta_total
            )
            /
            abs(
                selected_diag.a_cross
            )
        )

        eta = float(
            np.clip(
                eta,
                0.0,
                1.0,
            )
        )

        (
            displacement,
            correlation,
            dx,
            n,
        ) = (
            matched_correlation(
                selected_solution,
                profile_rmax=rmax,
                tail_reference=tail_reference,
                taper_start_fraction=PRIMARY_TAPER_START,
            )
        )

        energy = (
            interaction_energy(
                displacement,
                correlation,
                SELECTED_KF,
            )
        )

        metrics = (
            calculate_metrics(
                displacement,
                energy,
                eta_relax=eta,
                sigma_wall=sigma_wall,
            )
        )

        domain_records.append(
            (
                rmax,
                eta,
                metrics,
            )
        )

        rho_outer = float(
            rho_reference(
                tail_reference,
                rmax,
            )
        )

        print(
            "MATCHED_DOMAIN "
            f"RMAX={rmax:.1f} "
            f"M_R_TIMES_R={m * rmax:.9f} "
            f"RHO_OUTER_OVER_F={rho_outer / core.F_PHASE:.12f} "
            f"ETA={eta:.12f} "
            f"FFT_N={n} "
            f"FFT_DX={dx:.12e} "
            f"FORCE_RATIO={metrics.force_ratio:.12f} "
            f"STABLE_D={metrics.stable_d:.9f} "
            f"UNSTABLE_D={metrics.unstable_d:.9f} "
            f"BARRIER={metrics.barrier:.15e} "
            f"STABLE_CURV={metrics.stable_curvature:+.15e} "
            f"UNSTABLE_CURV={metrics.unstable_curvature:+.15e} "
            f"PASS={'YES' if metrics.passed else 'NO'}"
        )

    force_ratios = np.array(
        [
            row[2].force_ratio
            for row
            in domain_records
        ],
        dtype=float,
    )

    domain_force_spread = (
        float(
            np.max(
                force_ratios
            )
            -
            np.min(
                force_ratios
            )
        )
        /
        float(
            np.mean(
                force_ratios
            )
        )
    )

    all_domains_pass = all(
        row[2].passed
        for row
        in domain_records
    )

    print(
        f"MATCHED_DOMAIN_FORCE_REL_SPREAD={domain_force_spread:.15e}"
    )

    print(
        "MATCHED_DOMAIN_ALL_PHYSICS_PASS="
        f"{'YES' if all_domains_pass else 'NO'}"
    )

    matched_domain_convergence = (
        all_domains_pass
        and
        domain_force_spread
        <=
        FORCE_RATIO_SPREAD_MAX
    )

    print(
        "MATCHED_RADIAL_PROFILE_CONVERGENCE="
        f"{'PASS' if matched_domain_convergence else 'FAIL'}"
    )

    print(
        "\n=== EXPLICIT-BREAKING IR TAPER SENSITIVITY ==="
    )

    selected_rmax = 80.0

    base80 = (
        solve_matched_composite(
            chi=core.CHI_SELECTED,
            fraction=0.0,
            rmax=selected_rmax,
            tail_reference=tail_reference,
        )
    )

    selected80 = (
        solve_matched_composite(
            chi=core.CHI_SELECTED,
            fraction=SELECTED_KF,
            rmax=selected_rmax,
            tail_reference=tail_reference,
            previous=base80,
        )
    )

    base80_diag = (
        core.diagnose(
            base80,
            chi=core.CHI_SELECTED,
            kappa_fraction=0.0,
            rmax=selected_rmax,
        )
    )

    selected80_diag = (
        core.diagnose(
            selected80,
            chi=core.CHI_SELECTED,
            kappa_fraction=SELECTED_KF,
            rmax=selected_rmax,
        )
    )

    eta80 = (
        abs(
            selected80_diag.a_total_ir
            -
            base80_diag.a_total_ir
        )
        /
        abs(
            selected80_diag.a_cross
        )
    )

    eta80 = float(
        np.clip(
            eta80,
            0.0,
            1.0,
        )
    )

    taper_records = []

    for taper_start in TAPER_START_VALUES:

        (
            displacement,
            correlation,
            dx,
            n,
        ) = (
            matched_correlation(
                selected80,
                profile_rmax=selected_rmax,
                tail_reference=tail_reference,
                taper_start_fraction=taper_start,
            )
        )

        energy = (
            interaction_energy(
                displacement,
                correlation,
                SELECTED_KF,
            )
        )

        metrics = (
            calculate_metrics(
                displacement,
                energy,
                eta_relax=eta80,
                sigma_wall=sigma_wall,
            )
        )

        taper_records.append(
            (
                taper_start,
                metrics,
            )
        )

        print(
            "TAPER "
            f"START_FRACTION={taper_start:.3f} "
            f"FORCE_RATIO={metrics.force_ratio:.12f} "
            f"STABLE_D={metrics.stable_d:.9f} "
            f"UNSTABLE_D={metrics.unstable_d:.9f} "
            f"BARRIER={metrics.barrier:.15e} "
            f"PASS={'YES' if metrics.passed else 'NO'}"
        )

    taper_force_ratios = np.array(
        [
            record[1].force_ratio
            for record
            in taper_records
        ],
        dtype=float,
    )

    taper_spread = (
        float(
            np.max(
                taper_force_ratios
            )
            -
            np.min(
                taper_force_ratios
            )
        )
        /
        float(
            np.mean(
                taper_force_ratios
            )
        )
    )

    taper_all_pass = all(
        record[1].passed
        for record
        in taper_records
    )

    print(
        f"TAPER_FORCE_RATIO_REL_SPREAD={taper_spread:.15e}"
    )

    taper_pass = (
        taper_all_pass
        and
        taper_spread
        <=
        TAPER_FORCE_SPREAD_MAX
    )

    print(
        "IR_TAPER_SENSITIVITY="
        f"{'PASS' if taper_pass else 'FAIL'}"
    )

    print(
        "\n=== BLIND WILDCARD NOTE ==="
    )

    print(
        "WILDCARD_VALUES="
        "1.6,1.875,3.125,0.625,5"
    )

    print(
        "WILDCARD_SELECTED_POINT_OVERLAP="
        "0.625"
    )

    print(
        "WILDCARD_INTERPRETATION="
        "BLIND_CONTROL_ONLY_NOT_PHYSICS_PRIOR"
    )

    print(
        "\n=== 018A-3R DECISION ==="
    )

    overall_green = (
        reference_pass
        and
        matched_domain_convergence
        and
        taper_pass
    )

    print(
        "GLOBAL_REFERENCE_CONVERGENCE="
        f"{'PASS' if reference_pass else 'FAIL'}"
    )

    print(
        "MATCHED_RADIAL_PROFILE_CONVERGENCE="
        f"{'PASS' if matched_domain_convergence else 'FAIL'}"
    )

    print(
        "IR_TAPER_SENSITIVITY="
        f"{'PASS' if taper_pass else 'FAIL'}"
    )

    print(
        "018A3R_IR_BOUNDARY_AUDIT="
        f"{'GREEN' if overall_green else 'RED'}"
    )

    if overall_green:
        print(
            "ORIGINAL_018A3_RADIAL_FAILURE="
            "CONSISTENT_WITH_FINITE_BOX_GLOBAL_STRING_BOUNDARY_ARTIFACT"
        )

        print(
            "018A3_TRANSLATIONAL_FORCE_PREFLIGHT_AFTER_IR_REPAIR="
            "GREEN"
        )
    else:
        print(
            "ORIGINAL_018A3_RADIAL_FAILURE="
            "NOT_RESOLVED"
        )

        print(
            "018A3_TRANSLATIONAL_FORCE_PREFLIGHT_AFTER_IR_REPAIR="
            "NOT_GREEN"
        )

    print(
        "TRUE_2D_STRING_WALL_JUNCTION="
        "NOT_YET_SOLVED"
    )

    print(
        "COMPLETE_JUNCTION_STRESS_ENERGY="
        "NOT_YET_SOLVED"
    )

    print(
        "FINITE_PAYLOAD_GRAVITY_AFTER_TRUE_JUNCTION="
        "NOT_YET_TESTED"
    )

    print(
        "FULL_018A_GATE="
        "NOT_YET_GREEN"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE="
        "NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_018A_GLOBAL_STRING_IR_BOUNDARY_AUDIT"
    )

    if overall_green:
        print(
            "NEXT="
            "018A4_TRUE_2D_EXPLICIT_BREAKING_STRING_WALL_JUNCTION"
        )
    else:
        print(
            "NEXT="
            "DETERMINE_WHETHER_REMAINING_PROFILE_DRIFT_IS_PHYSICAL_BEFORE_ANY_2D_ESCALATION"
        )


if __name__ == "__main__":
    main()
