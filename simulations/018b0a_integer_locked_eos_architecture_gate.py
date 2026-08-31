#!/usr/bin/env python3
"""018B-0A — integer-locked vorton EOS architecture gate.

PURPOSE
-------
Close the remaining quantization/EOS consistency question created by the
018B-0 single-stationary-vorton architecture campaign before any microscopic
reparameterization or global toroidal PDE solve.

018B-0 found a deep robust source-level candidate near:

    F = 0.0384

with projected:

    C_eff ~ 8.77e5

and approximately a factor-two source-level energy improvement relative to the
validated two-copy 018A-8 source.

However, the vorton winding N is an integer.

The quantities:

    chi
    q = Q/N
    ell = L/Q
    k
    omega
    Sigma2
    A_string
    radial stress
    radius R
    winding N

are not independent.

A legitimate stationary circular vorton must satisfy:

    k L = 2 pi N

with:

    L = 2 pi R

so:

    k R = N.

Thus rounding the continuous N estimate while holding the old selected chi
fixed is not the correct operation.

The EOS and equilibrium radius must move together until:

    k(chi) R(chi,F) = integer.

SCIENTIFIC QUESTION
-------------------
Does the source-level single-vorton candidate discovered by 018B-0 possess
integer-winding-locked equilibria inside the already verified healthy 017P
EOS interval, and if so what exact F, chi, N, R and payload height should be
sent into the next microscopic wall/junction revalidation?

VERIFIED 017P BRANCH
--------------------
The preferred phase-ratio 0.99 branch was explicitly scanned at:

    0.0015 <= chi <= 0.00475.

At each journaled point the project recorded:

    q = Q/N
    ell = L/Q
    w_stat.

The same branch was verified against the superconducting-string BVP and the
published thin-string stability criterion.

The tabulated values are used as the discrete external EOS data for the
architecture lock.

PCHIP interpolation is used only between already-computed branch points.

No extrapolation outside the verified interval is permitted.

EOS IDENTITIES
--------------
For a stationary loop:

    k
      =
      2 pi / (q ell).

Because:

    chi
      =
      omega^2 - k^2,

we have:

    omega
      =
      sqrt(k^2 + chi).

The fixed-charge straight-string relation also gives:

    omega/k
      =
      q/(2 pi Sigma2),

hence:

    Sigma2
      =
      q k / (2 pi omega).

For one string copy:

    P_parallel
      =
      2 k^2 Sigma2
      -
      A_string.

The previously promoted pair-load relation independently gives:

    P_parallel
      =
      w_stat ell / (4 pi).

Therefore:

    A_string
      =
      2 k^2 Sigma2
      -
      P_parallel.

The one-copy active line is:

    Lambda_active
      =
      2 Sigma2
      (
        omega^2 + k^2
      ).

The physical energy line is:

    U
      =
      Lambda_active
      -
      P_parallel.

At the selected 017P endpoint these identities must reconstruct the directly
solved BVP values before the scan is allowed to proceed.

SINGLE-VORTON RADIAL EQUILIBRIUM
--------------------------------
At source-preflight level the selected one-vorton architecture has radial
support:

    P_eff
      =
      P_parallel
      -
      mu_J,

where mu_J is the measured reduced KLS junction excess.

For microscopic wall tension sigma_W(F),

    R
      =
      P_eff / sigma_W.

Integer locking requires:

    k(chi) R(chi,F)
      =
      N

for integer N.

This equation is solved directly with Brent root finding.

No nearest-integer approximation is used for promoted candidates.

WALL CONTINUATION
-----------------
The already verified Ising-wall tension law is retained:

    sigma_W(F)
      proportional to
      F^3.

Its normalization is calibrated against the fully solved F=0.075 wall.

The wall inverse scale is:

    k_W
      =
      F sqrt(lambda_A)/2.

The next microscopic run must explicitly re-solve the wall at the selected F.

Therefore this file remains a source-level EOS/quantization gate.

FINITE-PAYLOAD GRAVITY
----------------------
The exact finite-thickness spherical-payload overlap kernel from 018A-8 is
retained.

For each integer-locked candidate the payload height ratio x=h/R is optimized
only after chi and N are locked.

Required simultaneously:

    positive total active mass;
    positive point acceleration;
    positive finite-payload acceleration;
    kernel leverage > 1;
    clear wall/core scale separation;
    healthy topology preflight;
    integer winding exactly satisfied.

WORLD-SHEET STABILITY
---------------------
The locked chi must stay inside:

    0.0015 <= chi <= 0.00475.

Characteristic speeds are reconstructed from the EOS interpolation:

    c_T^2
      =
      1 /
      (
        1
        +
        2 chi Sigma2/A_string
      )

and:

    c_L^2
      =
      1 /
      (
        1
        +
        2 chi
        dSigma2/dchi
        /
        Sigma2
      ).

The existing m=2..40 extrinsic stability polynomial test is then rerun.

FULL INTEGER MAP
----------------
At F=0.0384 every integer root in the verified stable chi interval is mapped.

This explicitly checks whether the highest-chi locked state is also the
minimum-C state instead of assuming it.

DENSE F SEARCH
--------------
Scan:

    0.0340 <= F <= 0.0405

in increments of:

    0.00005.

At each F solve the five highest-chi integer states and select the lowest-C
locked state.

The scan therefore contains thousands of separately quantized candidates.

ROBUSTNESS
----------
Serious finalists undergo a 3^8 = 6561 deterministic family-level stress.

Dimensions:

    F                       +/-10 percent
    junction energy         x0.5, x1, x2
    radial support          +/-10 percent
    base active line        +/-10 percent
    junction active source  x0.5, x1, x2
    q interpolation scale   +/-0.1 percent
    ell interpolation scale +/-0.1 percent
    payload height          +/-10 percent

Each perturbed model is re-locked to an integer winding inside the verified
EOS band.

This tests whether integer compatibility survives across a physical model
family.

FIXED-N CONTINUITY
------------------
A second stricter local test keeps the selected integer N fixed.

Small perturbations are applied to:

    F              +/-0.5 percent
    junction mu    +/-10 percent
    radial support +/-1 percent
    q              +/-0.1 percent
    ell            +/-0.1 percent.

The same N must retain an EOS root inside the verified stability band.

This tests whether the selected topological sector itself has a local basin.

RANDOM STRESS
-------------
After deterministic selection, 20,000 continuous random source-level
perturbations are re-locked to integer winding.

DIRECT BVP VERIFICATION
-----------------------
For the selected candidate, the underlying 017P straight-string radial BVP is
solved directly again.

The BVP-reconstructed:

    Sigma2
    A_string
    P_parallel

are compared against the tabulated-EOS reconstruction.

Then the integer-lock root itself is re-solved with direct BVP stresses.

This is the independent verification path.

PROMOTION CONDITION
-------------------
A green result requires:

    EOS_ENDPOINT_RECONSTRUCTION=PASS

    SELECTED_F_FULL_INTEGER_MAP=PASS

    INTEGER_LOCKED_FEASIBLE_REGION=YES

    LOCKED_WORLD_SHEET_STABILITY=PASS

    INTEGER_RELOCKED_DETERMINISTIC_STRESS=PASS

    FIXED_N_LOCAL_CONTINUITY=PASS

    INTEGER_RELOCKED_RANDOM_STRESS=PASS

    DIRECT_BVP_INTEGER_LOCK=PASS

    HIGH_PRECISION_LOCKED_GRAVITY=PASS.

If green:

    NEXT =
      018B0B_MICROSCOPIC_REVALIDATION_AT_INTEGER_LOCKED_F_CHI.

Only after 018B0B may the lower source-level energy coefficient replace the
validated 018A-8 coefficient.

STOP RULE
---------
If no robust integer-locked single-vorton region exists inside the established
healthy EOS interval, reject the single-vorton simplification and return to
the current validated two-copy architecture.

Do not expand the stable chi interval merely to save the new architecture.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_018B0A_INTEGER_LOCKED_EOS_ARCHITECTURE_GATE

LIMITATIONS
-----------
This is not:

    a new microscopic wall solve;
    a new fully coupled junction solve;
    a global toroidal field solution;
    a full composite stability proof;
    nonlinear Einstein-matter;
    practical antigravity.

The current source-level energy improvement remains projected until 018B0B.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import importlib.util
import itertools
import math
from pathlib import Path
import sys

import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq, minimize_scalar


ROOT = Path(__file__).resolve().parents[1]

SOURCE = (
    ROOT
    / "simulations"
    / "018b0_exhaustive_architecture_pareto_campaign.py"
)


def load_module(
    name: str,
    path: Path,
):
    """Import a verified project simulation without invoking main()."""

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


b0 = load_module(
    "ag018b0_integer_lock",
    SOURCE,
)

g8 = b0.g8
fc = b0.fc
m = b0.m


# ============================================================================
# Verified 017P phase-ratio 0.99 EOS branch.
# ============================================================================

CHI_TABLE = np.array(
    [
        0.00150,
        0.00175,
        0.00200,
        0.00225,
        0.00250,
        0.00275,
        0.00300,
        0.00325,
        0.00350,
        0.00375,
        0.00400,
        0.00425,
        0.00450,
        0.00475,
    ],
    dtype=float,
)

Q_OVER_N_TABLE = np.array(
    [
        6.610153175742,
        6.611540595143,
        6.612928538126,
        6.614317005017,
        6.615705996143,
        6.617095511828,
        6.618485552399,
        6.619876118183,
        6.621267209507,
        6.622658826698,
        6.624050970083,
        6.625443639991,
        6.626836836750,
        6.628230560688,
    ],
    dtype=float,
)

ELL_TABLE = np.array(
    [
        0.4267787088735,
        0.4266999025968,
        0.4266210964221,
        0.4265422903479,
        0.4264634843719,
        0.4263846784915,
        0.4263058727048,
        0.4262270670093,
        0.4261482614029,
        0.4260694558834,
        0.4259906504485,
        0.4259118450959,
        0.4258330398233,
        0.4257542346286,
    ],
    dtype=float,
)

W_STAT_TABLE = np.array(
    [
        11.99620573870,
        12.04743600628,
        12.09870180481,
        12.15000316360,
        12.20134011304,
        12.25271268399,
        12.30412090627,
        12.35556481063,
        12.40704442711,
        12.45855978637,
        12.51011091880,
        12.56169785486,
        12.61332062541,
        12.66497926067,
    ],
    dtype=float,
)

CHI_MIN = float(
    CHI_TABLE[
        0
    ]
)

CHI_MAX = float(
    CHI_TABLE[
        -1
    ]
)

Q_SPLINE = PchipInterpolator(
    CHI_TABLE,
    Q_OVER_N_TABLE,
    extrapolate=False,
)

ELL_SPLINE = PchipInterpolator(
    CHI_TABLE,
    ELL_TABLE,
    extrapolate=False,
)

W_SPLINE = PchipInterpolator(
    CHI_TABLE,
    W_STAT_TABLE,
    extrapolate=False,
)


# ============================================================================
# Campaign policy.
# ============================================================================

F_REFERENCE = 0.0384

F_SCAN = np.arange(
    0.0340,
    0.0405001,
    0.00005,
)

FINALIST_F = (
    0.0404,
    0.0394,
    0.0384,
    0.0376,
    0.0370,
    0.0360,
    0.0348,
)

PAYLOAD_RADIUS_OVER_H = 0.25

X_MIN = 0.003
X_MAX = 0.040

MIN_SCALE = 10.0
MIN_DEEP_SCALE = 15.0

MIN_DEEP_PAYLOAD = 0.05
MIN_DEEP_LEVERAGE = 1.02

INTEGER_RESIDUAL_TOL = 2.0e-7

RANDOM_CASES = 20000
RANDOM_SEED = 1801801

CURRENT_VALIDATED_C = (
    1.774169582609975e6
)

CURRENT_VALIDATED_ENERGY_J = (
    2.342887778715687e34
)

B0_PROJECTED_C = (
    8.768254563224691e5
)

B0_PROJECTED_ENERGY_J = (
    1.157895877497030e34
)

G_SI = 6.67430e-11
C_SI = 299792458.0
G0_SI = 9.80665


@dataclass(
    frozen=True
)
class BranchState:
    """One reconstructed point on the verified straight-vorton EOS."""

    chi: float

    q: float
    ell: float
    w_stat: float

    k: float
    omega: float

    sigma2: float
    p_parallel: float
    a_string: float

    energy_line: float
    active_line: float


@dataclass(
    frozen=True
)
class LockedState:
    """One exact integer-winding equilibrium."""

    f_value: float
    n_integer: int

    branch: BranchState

    sigma_wall: float
    k_wall: float

    radius: float

    integer_residual: float


def reconstruct_branch(
    chi: float,
    *,
    q_factor: float = 1.0,
    ell_factor: float = 1.0,
    support_factor: float = 1.0,
) -> BranchState:
    """Reconstruct one EOS point from the verified q, ell and load tables."""

    if not (
        CHI_MIN
        <=
        chi
        <=
        CHI_MAX
    ):
        raise ValueError(
            "chi outside verified 017P stable interpolation interval"
        )

    q = float(
        Q_SPLINE(
            chi
        )
    ) * q_factor

    ell = float(
        ELL_SPLINE(
            chi
        )
    ) * ell_factor

    w_stat = float(
        W_SPLINE(
            chi
        )
    )

    k = (
        2.0
        *
        math.pi
        /
        (
            q
            *
            ell
        )
    )

    omega = math.sqrt(
        k
        *
        k
        +
        chi
    )

    sigma2 = (
        q
        *
        k
        /
        (
            2.0
            *
            math.pi
            *
            omega
        )
    )

    p_parallel = (
        w_stat
        *
        ell
        /
        (
            4.0
            *
            math.pi
        )
        *
        support_factor
    )

    a_string = (
        2.0
        *
        k
        *
        k
        *
        sigma2

        -
        p_parallel
    )

    active_line = (
        2.0
        *
        sigma2
        *
        (
            omega
            *
            omega

            +
            k
            *
            k
        )
    )

    energy_line = (
        active_line
        -
        p_parallel
    )

    return BranchState(
        chi=float(
            chi
        ),

        q=float(
            q
        ),

        ell=float(
            ell
        ),

        w_stat=float(
            w_stat
        ),

        k=float(
            k
        ),

        omega=float(
            omega
        ),

        sigma2=float(
            sigma2
        ),

        p_parallel=float(
            p_parallel
        ),

        a_string=float(
            a_string
        ),

        energy_line=float(
            energy_line
        ),

        active_line=float(
            active_line
        ),
    )


def wall_tension(
    anchors,
    f_value: float,
) -> float:
    """Use the calibrated microscopic F^3 Ising-wall tension law."""

    return float(
        b0.wall_tension(
            anchors,
            f_value,
        )
    )


def wall_inverse_width(
    anchors,
    f_value: float,
) -> float:
    """Return the selected KLS wall inverse profile scale."""

    return float(
        b0.wall_k(
            anchors,
            f_value,
        )
    )


def winding_continuous(
    anchors,
    f_value: float,
    chi: float,
    *,
    mu_factor: float = 1.0,
    q_factor: float = 1.0,
    ell_factor: float = 1.0,
    support_factor: float = 1.0,
) -> tuple[float, float, BranchState]:
    """Return kR and R before imposing integer quantization."""

    branch = reconstruct_branch(
        chi,
        q_factor=q_factor,
        ell_factor=ell_factor,
        support_factor=support_factor,
    )

    mu_j = (
        anchors.mu_j
        *
        mu_factor
    )

    support = (
        branch.p_parallel
        -
        mu_j
    )

    if support <= 0.0:
        return (
            math.nan,
            math.nan,
            branch,
        )

    sigma_wall = (
        wall_tension(
            anchors,
            f_value,
        )
    )

    radius = (
        support
        /
        sigma_wall
    )

    return (
        float(
            branch.k
            *
            radius
        ),

        float(
            radius
        ),

        branch,
    )


def solve_fixed_integer(
    anchors,
    f_value: float,
    n_integer: int,
    *,
    mu_factor: float = 1.0,
    q_factor: float = 1.0,
    ell_factor: float = 1.0,
    support_factor: float = 1.0,
) -> LockedState | None:
    """Solve k(chi) R(chi,F)=N on the verified EOS interval."""

    def residual(
        chi: float,
    ) -> float:

        winding, _, _ = (
            winding_continuous(
                anchors,
                f_value,
                chi,
                mu_factor=mu_factor,
                q_factor=q_factor,
                ell_factor=ell_factor,
                support_factor=support_factor,
            )
        )

        return (
            winding
            -
            n_integer
        )

    grid = np.linspace(
        CHI_MIN,
        CHI_MAX,
        129,
    )

    values = [
        residual(
            float(
                chi
            )
        )
        for chi in grid
    ]

    brackets = []

    for (
        left,
        right,
        f_left,
        f_right,
    ) in zip(
        grid[
            :-1
        ],
        grid[
            1:
        ],
        values[
            :-1
        ],
        values[
            1:
        ],
    ):

        if not (
            math.isfinite(
                f_left
            )
            and
            math.isfinite(
                f_right
            )
        ):
            continue

        if f_left == 0.0:

            brackets.append(
                (
                    float(
                        left
                    ),
                    float(
                        left
                    ),
                )
            )

        elif (
            f_left
            *
            f_right
            <
            0.0
        ):

            brackets.append(
                (
                    float(
                        left
                    ),
                    float(
                        right
                    ),
                )
            )

    if values[
        -1
    ] == 0.0:

        brackets.append(
            (
                CHI_MAX,
                CHI_MAX,
            )
        )

    if not brackets:
        return None

    # If a non-monotonic branch ever produced multiple roots for one N,
    # prefer the highest-chi root because it stays closest to the promoted
    # high-chi 017P operating point. All roots are still exposed in the
    # full-map audit below.
    roots = []

    for (
        left,
        right,
    ) in brackets:

        if left == right:

            root = left

        else:

            root = brentq(
                residual,
                left,
                right,
                xtol=2.0e-13,
                rtol=2.0e-13,
                maxiter=200,
            )

        roots.append(
            float(
                root
            )
        )

    chi = max(
        roots
    )

    winding, radius, branch = (
        winding_continuous(
            anchors,
            f_value,
            chi,
            mu_factor=mu_factor,
            q_factor=q_factor,
            ell_factor=ell_factor,
            support_factor=support_factor,
        )
    )

    return LockedState(
        f_value=float(
            f_value
        ),

        n_integer=int(
            n_integer
        ),

        branch=branch,

        sigma_wall=wall_tension(
            anchors,
            f_value,
        ),

        k_wall=wall_inverse_width(
            anchors,
            f_value,
        ),

        radius=float(
            radius
        ),

        integer_residual=float(
            winding
            -
            n_integer
        ),
    )


def highest_chi_lock(
    anchors,
    f_value: float,
    *,
    mu_factor: float = 1.0,
    q_factor: float = 1.0,
    ell_factor: float = 1.0,
    support_factor: float = 1.0,
    integer_backoff: int = 0,
) -> LockedState | None:
    """Return one of the highest-chi integer roots in the verified band."""

    winding_max, _, _ = (
        winding_continuous(
            anchors,
            f_value,
            CHI_MAX,
            mu_factor=mu_factor,
            q_factor=q_factor,
            ell_factor=ell_factor,
            support_factor=support_factor,
        )
    )

    winding_min, _, _ = (
        winding_continuous(
            anchors,
            f_value,
            CHI_MIN,
            mu_factor=mu_factor,
            q_factor=q_factor,
            ell_factor=ell_factor,
            support_factor=support_factor,
        )
    )

    if not (
        math.isfinite(
            winding_max
        )
        and
        math.isfinite(
            winding_min
        )
    ):
        return None

    upper = int(
        math.floor(
            max(
                winding_min,
                winding_max,
            )
        )
    )

    lower = int(
        math.ceil(
            min(
                winding_min,
                winding_max,
            )
        )
    )

    target = (
        upper
        -
        integer_backoff
    )

    if target < lower:
        return None

    return solve_fixed_integer(
        anchors,
        f_value,
        target,
        mu_factor=mu_factor,
        q_factor=q_factor,
        ell_factor=ell_factor,
        support_factor=support_factor,
    )


def sigma2_derivative(
    chi: float,
) -> float:
    """Centered derivative of the reconstructed EOS condensate integral."""

    step = 2.0e-6

    if chi - step < CHI_MIN:
        left = chi
        right = chi + step
    elif chi + step > CHI_MAX:
        left = chi - step
        right = chi
    else:
        left = chi - step
        right = chi + step

    return (
        reconstruct_branch(
            right
        ).sigma2
        -
        reconstruct_branch(
            left
        ).sigma2
    ) / (
        right
        -
        left
    )


def stability_metrics(
    locked: LockedState,
):
    """Run EOS characteristic speeds and the existing m=2..40 test."""

    branch = (
        locked.branch
    )

    d_sigma = (
        sigma2_derivative(
            branch.chi
        )
    )

    ct2 = (
        1.0
        /
        (
            1.0
            +
            2.0
            *
            branch.chi
            *
            branch.sigma2
            /
            branch.a_string
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
            branch.chi
            *
            d_sigma
            /
            branch.sigma2
        )
    )

    (
        stable,
        min_disc,
        max_imag,
        worst_mode,
    ) = (
        fc.extrinsic_stability(
            ct2,
            cl2,
        )
    )

    passed = (
        CHI_MIN
        <=
        branch.chi
        <=
        CHI_MAX

        and
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

        and
        stable
    )

    return {
        "ct2":
            float(
                ct2
            ),

        "cl2":
            float(
                cl2
            ),

        "min_disc":
            float(
                min_disc
            ),

        "max_imag":
            float(
                max_imag
            ),

        "worst_mode":
            int(
                worst_mode
            ),

        "pass":
            bool(
                passed
            ),
    }


def evaluate_locked(
    anchors,
    locked: LockedState,
    x: float,
    *,
    base_active_factor: float = 1.0,
    endpoint_active_factor: float = 1.0,
    high_precision: bool = False,
):
    """Evaluate gravity and energy for one exact integer-locked state."""

    branch = (
        locked.branch
    )

    topology = (
        b0.topology_metrics(
            anchors,
            locked.f_value,
        )
    )

    active_line = (
        branch.active_line
        *
        base_active_factor

        +
        anchors.endpoint_active
        *
        endpoint_active_factor
    )

    junction_physical_energy = (
        anchors.mu_j

        +
        2.0
        *
        branch.omega
        *
        branch.omega
        *
        anchors.delta_sigma2
    )

    energy_line = (
        branch.energy_line
        +
        junction_physical_energy
    )

    (
        wall_point,
        wall_payload,
    ) = (
        b0.wall_kernel_factors(
            locked.sigma_wall,
            locked.k_wall,
            locked.radius,
            x,
            high_precision=high_precision,
        )
    )

    rim_inward = (
        2.0
        *
        math.pi
        *
        active_line
        *
        x
        /
        (
            1.0
            +
            x
            *
            x
        ) ** 1.5
    )

    point_outward = (
        wall_point
        -
        rim_inward
    )

    payload_outward = (
        wall_payload
        -
        rim_inward
    )

    positive_active_per_r = (
        2.0
        *
        math.pi
        *
        active_line
    )

    negative_active_per_r = (
        math.pi
        *
        locked.sigma_wall
        *
        locked.radius
    )

    active_mass_per_r = (
        positive_active_per_r
        -
        negative_active_per_r
    )

    if (
        positive_active_per_r
        >
        0.0
        and
        negative_active_per_r
        >
        0.0
        and
        rim_inward
        >
        0.0
    ):

        kappa_positive = (
            rim_inward
            /
            positive_active_per_r
        )

        kappa_negative = (
            wall_payload
            /
            negative_active_per_r
        )

        active_ratio = (
            positive_active_per_r
            /
            negative_active_per_r
        )

        leverage_margin = (
            (
                kappa_negative
                /
                kappa_positive
            )
            /
            active_ratio
        )

    else:

        leverage_margin = (
            -math.inf
        )

    wall_width90 = (
        2.0
        *
        math.atanh(
            0.9
        )
        /
        locked.k_wall
    )

    r_over_wall = (
        locked.radius
        /
        wall_width90
    )

    r_over_core = (
        locked.radius
        /
        anchors.rim_core_width
    )

    min_scale = min(
        r_over_wall,
        r_over_core,
    )

    energy_per_r = (
        2.0
        *
        math.pi
        *
        energy_line

        +
        math.pi
        *
        locked.sigma_wall
        *
        locked.radius
    )

    if payload_outward > 0.0:

        c_eff = (
            energy_per_r
            /
            (
                payload_outward
                *
                x
                *
                x
            )
        )

    else:

        c_eff = (
            math.inf
        )

    integer_pass = (
        abs(
            locked.integer_residual
        )
        <
        INTEGER_RESIDUAL_TOL
    )

    passed = (
        bool(
            topology[
                "pass"
            ]
        )

        and
        integer_pass

        and
        point_outward
        >
        0.0

        and
        payload_outward
        >
        0.0

        and
        active_mass_per_r
        >
        0.0

        and
        leverage_margin
        >
        1.0

        and
        min_scale
        >
        MIN_SCALE
    )

    return {
        "pass":
            bool(
                passed
            ),

        "x":
            float(
                x
            ),

        "point_outward":
            float(
                point_outward
            ),

        "payload_outward":
            float(
                payload_outward
            ),

        "active_mass_per_r":
            float(
                active_mass_per_r
            ),

        "leverage_margin":
            float(
                leverage_margin
            ),

        "r_over_wall":
            float(
                r_over_wall
            ),

        "r_over_core":
            float(
                r_over_core
            ),

        "min_scale":
            float(
                min_scale
            ),

        "energy_per_r":
            float(
                energy_per_r
            ),

        "c_eff":
            float(
                c_eff
            ),

        "active_line":
            float(
                active_line
            ),

        "energy_line":
            float(
                energy_line
            ),
    }


def optimize_height(
    anchors,
    locked: LockedState,
):
    """Optimize h/R only after EOS and integer winding are fixed."""

    grid = np.linspace(
        X_MIN,
        X_MAX,
        72,
    )

    records = [
        evaluate_locked(
            anchors,
            locked,
            float(
                x
            ),
        )
        for x in grid
    ]

    feasible = [
        (
            index,
            record,
        )
        for (
            index,
            record,
        )
        in enumerate(
            records
        )
        if
        record[
            "pass"
        ]
        and
        math.isfinite(
            record[
                "c_eff"
            ]
        )
    ]

    if not feasible:
        return None

    best_index, best_record = min(
        feasible,
        key=lambda item:
            item[
                1
            ][
                "c_eff"
            ],
    )

    left = float(
        grid[
            max(
                0,
                best_index
                -
                1,
            )
        ]
    )

    right = float(
        grid[
            min(
                len(
                    grid
                )
                -
                1,
                best_index
                +
                1,
            )
        ]
    )

    if right <= left:
        return best_record

    def objective(
        x: float,
    ) -> float:

        record = evaluate_locked(
            anchors,
            locked,
            float(
                x
            ),
        )

        if not record[
            "pass"
        ]:
            return 1.0e100

        return float(
            record[
                "c_eff"
            ]
        )

    result = minimize_scalar(
        objective,
        bounds=(
            left,
            right,
        ),
        method="bounded",
        options={
            "xatol":
                1.0e-10,

            "maxiter":
                200,
        },
    )

    refined = evaluate_locked(
        anchors,
        locked,
        float(
            result.x
        ),
    )

    if not refined[
        "pass"
    ]:
        return best_record

    return refined


def print_locked(
    prefix: str,
    locked: LockedState,
    gravity,
) -> None:
    """Print one candidate compactly."""

    print(
        f"{prefix} "
        f"F={locked.f_value:.9f} "
        f"CHI={locked.branch.chi:.15e} "
        f"N={locked.n_integer} "
        f"INTEGER_RESIDUAL={locked.integer_residual:+.15e} "
        f"Q_OVER_N={locked.branch.q:.15e} "
        f"ELL={locked.branch.ell:.15e} "
        f"K={locked.branch.k:.15e} "
        f"OMEGA={locked.branch.omega:.15e} "
        f"SIGMA2={locked.branch.sigma2:.15e} "
        f"A_STRING={locked.branch.a_string:.15e} "
        f"P_PARALLEL={locked.branch.p_parallel:.15e} "
        f"R={locked.radius:.15e} "
        f"X={gravity['x']:.15e} "
        f"PAYLOAD={gravity['payload_outward']:+.15e} "
        f"POINT={gravity['point_outward']:+.15e} "
        f"LEVERAGE={gravity['leverage_margin']:.15e} "
        f"R_OVER_WALL={gravity['r_over_wall']:.12f} "
        f"R_OVER_CORE={gravity['r_over_core']:.12f} "
        f"C={gravity['c_eff']:.15e}"
    )


def all_integer_locks(
    anchors,
    f_value: float,
):
    """Enumerate every integer root across the complete verified chi band."""

    n_left, _, _ = (
        winding_continuous(
            anchors,
            f_value,
            CHI_MIN,
        )
    )

    n_right, _, _ = (
        winding_continuous(
            anchors,
            f_value,
            CHI_MAX,
        )
    )

    n_min = int(
        math.ceil(
            min(
                n_left,
                n_right,
            )
        )
    )

    n_max = int(
        math.floor(
            max(
                n_left,
                n_right,
            )
        )
    )

    roots = []

    for n_integer in range(
        n_min,
        n_max
        +
        1,
    ):

        locked = solve_fixed_integer(
            anchors,
            f_value,
            n_integer,
        )

        if locked is not None:
            roots.append(
                locked
            )

    return roots


def candidate_at_f(
    anchors,
    f_value: float,
):
    """Evaluate the five highest-chi integer roots and retain lowest C."""

    candidates = []

    for backoff in range(
        5
    ):

        locked = highest_chi_lock(
            anchors,
            f_value,
            integer_backoff=backoff,
        )

        if locked is None:
            continue

        gravity = optimize_height(
            anchors,
            locked,
        )

        if gravity is None:
            continue

        stability = stability_metrics(
            locked
        )

        if not stability[
            "pass"
        ]:
            continue

        candidates.append(
            (
                locked,
                gravity,
                stability,
            )
        )

    if not candidates:
        return None

    return min(
        candidates,
        key=lambda item:
            item[
                1
            ][
                "c_eff"
            ],
    )


def relock_family_case(
    anchors,
    nominal_locked: LockedState,
    nominal_gravity,
    *,
    f_factor: float,
    mu_factor: float,
    support_factor: float,
    base_active_factor: float,
    endpoint_active_factor: float,
    q_factor: float,
    ell_factor: float,
    x_factor: float,
):
    """Relock a perturbed model family to its highest healthy integer state."""

    f_value = (
        nominal_locked.f_value
        *
        f_factor
    )

    locked = highest_chi_lock(
        anchors,
        f_value,
        mu_factor=mu_factor,
        q_factor=q_factor,
        ell_factor=ell_factor,
        support_factor=support_factor,
    )

    if locked is None:

        return {
            "pass":
                False,

            "payload":
                -math.inf,

            "point":
                -math.inf,

            "leverage":
                -math.inf,

            "scale":
                0.0,

            "c_eff":
                math.inf,
        }

    x = (
        nominal_gravity[
            "x"
        ]
        *
        x_factor
    )

    gravity = evaluate_locked(
        anchors,
        locked,
        x,
        base_active_factor=base_active_factor,
        endpoint_active_factor=endpoint_active_factor,
    )

    return {
        "pass":
            bool(
                gravity[
                    "pass"
                ]
            ),

        "payload":
            float(
                gravity[
                    "payload_outward"
                ]
            ),

        "point":
            float(
                gravity[
                    "point_outward"
                ]
            ),

        "leverage":
            float(
                gravity[
                    "leverage_margin"
                ]
            ),

        "scale":
            float(
                gravity[
                    "min_scale"
                ]
            ),

        "c_eff":
            float(
                gravity[
                    "c_eff"
                ]
            ),

        "chi":
            float(
                locked.branch.chi
            ),

        "n":
            int(
                locked.n_integer
            ),
    }


def deterministic_relocked_stress(
    anchors,
    locked,
    gravity,
):
    """Run 3^8=6561 integer-relocked family stress cases."""

    ordinary = (
        0.90,
        1.00,
        1.10,
    )

    junction = (
        0.50,
        1.00,
        2.00,
    )

    interpolation = (
        0.999,
        1.000,
        1.001,
    )

    total = 0
    passed = 0

    min_payload = math.inf
    min_point = math.inf
    min_leverage = math.inf
    min_scale = math.inf

    min_chi = math.inf
    max_chi = -math.inf

    max_c = 0.0

    worst = None

    for (
        f_factor,
        mu_factor,
        support_factor,
        base_active_factor,
        endpoint_active_factor,
        q_factor,
        ell_factor,
        x_factor,
    ) in itertools.product(
        ordinary,
        junction,
        ordinary,
        ordinary,
        junction,
        interpolation,
        interpolation,
        ordinary,
    ):

        total += 1

        result = relock_family_case(
            anchors,
            locked,
            gravity,
            f_factor=f_factor,
            mu_factor=mu_factor,
            support_factor=support_factor,
            base_active_factor=base_active_factor,
            endpoint_active_factor=endpoint_active_factor,
            q_factor=q_factor,
            ell_factor=ell_factor,
            x_factor=x_factor,
        )

        if result[
            "pass"
        ]:
            passed += 1

        if result[
            "payload"
        ] < min_payload:

            min_payload = (
                result[
                    "payload"
                ]
            )

            worst = {
                "F_FACTOR":
                    f_factor,

                "MU_FACTOR":
                    mu_factor,

                "SUPPORT_FACTOR":
                    support_factor,

                "BASE_ACTIVE_FACTOR":
                    base_active_factor,

                "ENDPOINT_ACTIVE_FACTOR":
                    endpoint_active_factor,

                "Q_FACTOR":
                    q_factor,

                "ELL_FACTOR":
                    ell_factor,

                "X_FACTOR":
                    x_factor,

                "LOCKED_CHI":
                    result.get(
                        "chi"
                    ),

                "LOCKED_N":
                    result.get(
                        "n"
                    ),
            }

        min_point = min(
            min_point,
            result[
                "point"
            ],
        )

        min_leverage = min(
            min_leverage,
            result[
                "leverage"
            ],
        )

        min_scale = min(
            min_scale,
            result[
                "scale"
            ],
        )

        if "chi" in result:

            min_chi = min(
                min_chi,
                result[
                    "chi"
                ],
            )

            max_chi = max(
                max_chi,
                result[
                    "chi"
                ],
            )

        if math.isfinite(
            result[
                "c_eff"
            ]
        ):

            max_c = max(
                max_c,
                result[
                    "c_eff"
                ],
            )

        else:

            max_c = math.inf

    all_pass = (
        passed
        ==
        total
    )

    deep_pass = (
        all_pass

        and
        min_payload
        >
        MIN_DEEP_PAYLOAD

        and
        min_leverage
        >
        MIN_DEEP_LEVERAGE

        and
        min_scale
        >
        MIN_DEEP_SCALE
    )

    return {
        "total":
            total,

        "passed":
            passed,

        "all_pass":
            all_pass,

        "deep_pass":
            deep_pass,

        "min_payload":
            min_payload,

        "min_point":
            min_point,

        "min_leverage":
            min_leverage,

        "min_scale":
            min_scale,

        "min_chi":
            min_chi,

        "max_chi":
            max_chi,

        "max_c":
            max_c,

        "worst":
            worst,
    }


def solve_same_n_perturbed(
    anchors,
    nominal_locked,
    *,
    f_factor: float,
    mu_factor: float,
    support_factor: float,
    q_factor: float,
    ell_factor: float,
):
    """Keep the exact selected winding and ask whether a local EOS root survives."""

    return solve_fixed_integer(
        anchors,
        nominal_locked.f_value
        *
        f_factor,
        nominal_locked.n_integer,
        mu_factor=mu_factor,
        q_factor=q_factor,
        ell_factor=ell_factor,
        support_factor=support_factor,
    )


def fixed_n_continuity(
    anchors,
    locked,
    gravity,
):
    """Test a local basin while holding the topological integer N fixed."""

    f_levels = (
        0.995,
        1.000,
        1.005,
    )

    mu_levels = (
        0.90,
        1.00,
        1.10,
    )

    support_levels = (
        0.99,
        1.00,
        1.01,
    )

    interpolation_levels = (
        0.999,
        1.000,
        1.001,
    )

    total = 0
    passed = 0

    min_payload = math.inf
    min_chi = math.inf
    max_chi = -math.inf

    for (
        f_factor,
        mu_factor,
        support_factor,
        q_factor,
        ell_factor,
    ) in itertools.product(
        f_levels,
        mu_levels,
        support_levels,
        interpolation_levels,
        interpolation_levels,
    ):

        total += 1

        perturbed = solve_same_n_perturbed(
            anchors,
            locked,
            f_factor=f_factor,
            mu_factor=mu_factor,
            support_factor=support_factor,
            q_factor=q_factor,
            ell_factor=ell_factor,
        )

        if perturbed is None:
            continue

        result = evaluate_locked(
            anchors,
            perturbed,
            gravity[
                "x"
            ],
        )

        if result[
            "pass"
        ]:
            passed += 1

        min_payload = min(
            min_payload,
            result[
                "payload_outward"
            ],
        )

        min_chi = min(
            min_chi,
            perturbed.branch.chi,
        )

        max_chi = max(
            max_chi,
            perturbed.branch.chi,
        )

    return {
        "total":
            total,

        "passed":
            passed,

        "pass":
            passed
            ==
            total,

        "min_payload":
            min_payload,

        "min_chi":
            min_chi,

        "max_chi":
            max_chi,
    }


def randomized_relocked_stress(
    anchors,
    locked,
    gravity,
):
    """Run 20k continuous integer-relocked family perturbations."""

    rng = np.random.default_rng(
        RANDOM_SEED
    )

    passed = 0

    min_payload = math.inf
    min_leverage = math.inf
    min_scale = math.inf

    for _ in range(
        RANDOM_CASES
    ):

        f_factor = rng.uniform(
            0.90,
            1.10,
        )

        mu_factor = math.exp(
            rng.uniform(
                math.log(
                    0.50
                ),
                math.log(
                    2.00
                ),
            )
        )

        support_factor = rng.uniform(
            0.90,
            1.10,
        )

        base_active_factor = rng.uniform(
            0.90,
            1.10,
        )

        endpoint_active_factor = math.exp(
            rng.uniform(
                math.log(
                    0.50
                ),
                math.log(
                    2.00
                ),
            )
        )

        q_factor = rng.uniform(
            0.999,
            1.001,
        )

        ell_factor = rng.uniform(
            0.999,
            1.001,
        )

        x_factor = rng.uniform(
            0.90,
            1.10,
        )

        result = relock_family_case(
            anchors,
            locked,
            gravity,
            f_factor=f_factor,
            mu_factor=mu_factor,
            support_factor=support_factor,
            base_active_factor=base_active_factor,
            endpoint_active_factor=endpoint_active_factor,
            q_factor=q_factor,
            ell_factor=ell_factor,
            x_factor=x_factor,
        )

        if result[
            "pass"
        ]:
            passed += 1

        min_payload = min(
            min_payload,
            result[
                "payload"
            ],
        )

        min_leverage = min(
            min_leverage,
            result[
                "leverage"
            ],
        )

        min_scale = min(
            min_scale,
            result[
                "scale"
            ],
        )

    return {
        "total":
            RANDOM_CASES,

        "passed":
            passed,

        "pass":
            passed
            ==
            RANDOM_CASES,

        "min_payload":
            min_payload,

        "min_leverage":
            min_leverage,

        "min_scale":
            min_scale,
    }


# ============================================================================
# Direct 017P radial BVP reconstruction.
# ============================================================================

DIRECT_CACHE = {}


def direct_bvp_state(
    chi: float,
):
    """Re-solve the actual 017P straight radial fields at arbitrary chi."""

    key = round(
        float(
            chi
        ),
        12,
    )

    if key in DIRECT_CACHE:
        return DIRECT_CACHE[
            key
        ]

    original_chi = float(
        m.CHI_SELECTED
    )

    try:

        m.CHI_SELECTED = float(
            chi
        )

        radial = (
            m.solve_017p_background()
        )

        diag = (
            m.diagnose_017p(
                radial
            )
        )

    finally:

        m.CHI_SELECTED = (
            original_chi
        )

    q = float(
        Q_SPLINE(
            chi
        )
    )

    ell = float(
        ELL_SPLINE(
            chi
        )
    )

    k = (
        2.0
        *
        math.pi
        /
        (
            q
            *
            ell
        )
    )

    omega = math.sqrt(
        k
        *
        k
        +
        chi
    )

    sigma2 = float(
        diag.sigma2
    )

    a_string = float(
        diag.a_string
    )

    p_parallel = (
        2.0
        *
        k
        *
        k
        *
        sigma2

        -
        a_string
    )

    active_line = (
        2.0
        *
        sigma2
        *
        (
            omega
            *
            omega

            +
            k
            *
            k
        )
    )

    energy_line = (
        2.0
        *
        omega
        *
        omega
        *
        sigma2

        +
        a_string
    )

    state = {
        "chi":
            float(
                chi
            ),

        "q":
            q,

        "ell":
            ell,

        "k":
            k,

        "omega":
            omega,

        "sigma2":
            sigma2,

        "a_string":
            a_string,

        "p_parallel":
            p_parallel,

        "active_line":
            active_line,

        "energy_line":
            energy_line,
    }

    DIRECT_CACHE[
        key
    ] = state

    return state


def direct_integer_lock(
    anchors,
    nominal_locked,
):
    """Independently solve the selected fixed-N root using direct BVP stresses."""

    n_integer = (
        nominal_locked.n_integer
    )

    f_value = (
        nominal_locked.f_value
    )

    sigma_wall = (
        wall_tension(
            anchors,
            f_value,
        )
    )

    def residual(
        chi: float,
    ) -> float:

        state = (
            direct_bvp_state(
                chi
            )
        )

        support = (
            state[
                "p_parallel"
            ]
            -
            anchors.mu_j
        )

        radius = (
            support
            /
            sigma_wall
        )

        return (
            state[
                "k"
            ]
            *
            radius

            -
            n_integer
        )

    center = (
        nominal_locked.branch.chi
    )

    half_width = 2.0e-5

    root = None

    for _ in range(
        6
    ):

        left = max(
            CHI_MIN,
            center
            -
            half_width,
        )

        right = min(
            CHI_MAX,
            center
            +
            half_width,
        )

        f_left = residual(
            left
        )

        f_right = residual(
            right
        )

        if f_left == 0.0:

            root = left
            break

        if f_right == 0.0:

            root = right
            break

        if (
            f_left
            *
            f_right
            <
            0.0
        ):

            root = brentq(
                residual,
                left,
                right,
                xtol=5.0e-12,
                rtol=5.0e-12,
                maxiter=80,
            )

            break

        half_width *= 2.0

    if root is None:
        return None

    state = (
        direct_bvp_state(
            float(
                root
            )
        )
    )

    support = (
        state[
            "p_parallel"
        ]
        -
        anchors.mu_j
    )

    radius = (
        support
        /
        sigma_wall
    )

    residual_final = (
        state[
            "k"
        ]
        *
        radius
        -
        n_integer
    )

    return {
        "chi":
            float(
                root
            ),

        "n":
            int(
                n_integer
            ),

        "state":
            state,

        "radius":
            float(
                radius
            ),

        "residual":
            float(
                residual_final
            ),
    }


def direct_locked_gravity(
    anchors,
    direct_lock,
    f_value: float,
):
    """Recompute high-precision gravity and energy from direct BVP stresses."""

    state = (
        direct_lock[
            "state"
        ]
    )

    radius = float(
        direct_lock[
            "radius"
        ]
    )

    sigma_wall = (
        wall_tension(
            anchors,
            f_value,
        )
    )

    k_wall = (
        wall_inverse_width(
            anchors,
            f_value,
        )
    )

    junction_energy = (
        anchors.mu_j

        +
        2.0
        *
        state[
            "omega"
        ] ** 2
        *
        anchors.delta_sigma2
    )

    active_line = (
        state[
            "active_line"
        ]
        +
        anchors.endpoint_active
    )

    energy_line = (
        state[
            "energy_line"
        ]
        +
        junction_energy
    )

    def evaluate_x(
        x: float,
        *,
        high_precision: bool,
    ):

        (
            wall_point,
            wall_payload,
        ) = (
            b0.wall_kernel_factors(
                sigma_wall,
                k_wall,
                radius,
                x,
                high_precision=high_precision,
            )
        )

        rim = (
            2.0
            *
            math.pi
            *
            active_line
            *
            x
            /
            (
                1.0
                +
                x
                *
                x
            ) ** 1.5
        )

        payload = (
            wall_payload
            -
            rim
        )

        point = (
            wall_point
            -
            rim
        )

        energy_per_r = (
            2.0
            *
            math.pi
            *
            energy_line

            +
            math.pi
            *
            sigma_wall
            *
            radius
        )

        if payload <= 0.0:

            c_eff = (
                math.inf
            )

        else:

            c_eff = (
                energy_per_r
                /
                (
                    payload
                    *
                    x
                    *
                    x
                )
            )

        return {
            "x":
                float(
                    x
                ),

            "wall_point":
                float(
                    wall_point
                ),

            "wall_payload":
                float(
                    wall_payload
                ),

            "rim":
                float(
                    rim
                ),

            "point":
                float(
                    point
                ),

            "payload":
                float(
                    payload
                ),

            "energy_per_r":
                float(
                    energy_per_r
                ),

            "c_eff":
                float(
                    c_eff
                ),
        }

    coarse_x = np.linspace(
        X_MIN,
        X_MAX,
        80,
    )

    coarse = [
        evaluate_x(
            float(
                x
            ),
            high_precision=False,
        )
        for x in coarse_x
    ]

    finite = [
        (
            i,
            record,
        )
        for (
            i,
            record,
        )
        in enumerate(
            coarse
        )
        if math.isfinite(
            record[
                "c_eff"
            ]
        )
    ]

    if not finite:
        return None

    best_index, _ = min(
        finite,
        key=lambda item:
            item[
                1
            ][
                "c_eff"
            ],
    )

    left = float(
        coarse_x[
            max(
                0,
                best_index
                -
                1,
            )
        ]
    )

    right = float(
        coarse_x[
            min(
                len(
                    coarse_x
                )
                -
                1,
                best_index
                +
                1,
            )
        ]
    )

    optimization = minimize_scalar(
        lambda x:
            evaluate_x(
                float(
                    x
                ),
                high_precision=False,
            )[
                "c_eff"
            ],
        bounds=(
            left,
            right,
        ),
        method="bounded",
        options={
            "xatol":
                1.0e-10,
        },
    )

    selected_x = float(
        optimization.x
    )

    scout = evaluate_x(
        selected_x,
        high_precision=True,
    )

    h = (
        selected_x
        *
        radius
    )

    payload_radius = (
        PAYLOAD_RADIUS_OVER_H
        *
        h
    )

    adaptive_wall = (
        g8.wall_gravity_factors(
            sigma_wall,
            k_wall,
            radius,
            h,
            payload_radius,
        )
    )

    (
        rim_values,
        rim_worst,
    ) = (
        g8.rim_envelope(
            active_line,
            radius,
            h,
            payload_radius,
            anchors.rim_core_width,
            high_precision=True,
        )
    )

    payload_hp = (
        adaptive_wall[
            "payload"
        ]
        -
        rim_worst
    )

    point_hp = (
        adaptive_wall[
            "point"
        ]
        -
        rim_worst
    )

    c_hp = (
        scout[
            "energy_per_r"
        ]
        /
        (
            payload_hp
            *
            selected_x
            *
            selected_x
        )
    )

    return {
        "x":
            selected_x,

        "point":
            float(
                point_hp
            ),

        "payload":
            float(
                payload_hp
            ),

        "c_eff":
            float(
                c_hp
            ),

        "rim_values":
            rim_values,

        "rim_worst":
            float(
                rim_worst
            ),

        "scout_wall_point_relerr":
            abs(
                scout[
                    "wall_point"
                ]
                -
                adaptive_wall[
                    "point"
                ]
            )
            /
            abs(
                adaptive_wall[
                    "point"
                ]
            ),

        "scout_wall_payload_relerr":
            abs(
                scout[
                    "wall_payload"
                ]
                -
                adaptive_wall[
                    "payload"
                ]
            )
            /
            abs(
                adaptive_wall[
                    "payload"
                ]
            ),
    }


def energy_scaling(
    c_eff: float,
):
    """Return 1g / 1m mass and energy equivalents."""

    mass = (
        c_eff
        *
        G0_SI
        /
        G_SI
    )

    energy = (
        mass
        *
        C_SI
        *
        C_SI
    )

    return (
        float(
            mass
        ),

        float(
            energy
        ),
    )


def main() -> None:
    """Execute the complete integer-winding/EOS lock campaign."""

    anchors = (
        b0.reconstruct_anchors()
    )

    print(
        "=== ANTIGRAVITY_RESEARCH 018B-0A ==="
    )

    print(
        "QUESTION="
        "DOES_THE_SINGLE_VORTON_ARCHITECTURE_SURVIVE_EXACT_INTEGER_WINDING_LOCKING_TO_THE_VERIFIED_017P_EOS"
    )

    # ========================================================================
    # EOS endpoint reconstruction.
    # ========================================================================

    print(
        "\n=== VERIFIED EOS ENDPOINT RECONSTRUCTION ==="
    )

    endpoint = (
        reconstruct_branch(
            CHI_MAX
        )
    )

    sigma2_expected = (
        1.054410621125
    )

    a_expected = (
        10.02499735504
    )

    k_expected = (
        2.226503003591
    )

    omega_expected = (
        2.227569443362
    )

    sigma2_relerr = (
        abs(
            endpoint.sigma2
            -
            sigma2_expected
        )
        /
        sigma2_expected
    )

    a_relerr = (
        abs(
            endpoint.a_string
            -
            a_expected
        )
        /
        a_expected
    )

    k_relerr = (
        abs(
            endpoint.k
            -
            k_expected
        )
        /
        k_expected
    )

    omega_relerr = (
        abs(
            endpoint.omega
            -
            omega_expected
        )
        /
        omega_expected
    )

    endpoint_pass = (
        sigma2_relerr
        <
        2.0e-10

        and
        a_relerr
        <
        2.0e-10

        and
        k_relerr
        <
        2.0e-10

        and
        omega_relerr
        <
        2.0e-10
    )

    print(
        "EOS_TABLE_POINTS="
        f"{len(CHI_TABLE)}"
    )

    print(
        "EOS_STABLE_CHI_MIN="
        f"{CHI_MIN:.8f}"
    )

    print(
        "EOS_STABLE_CHI_MAX="
        f"{CHI_MAX:.8f}"
    )

    print(
        "ENDPOINT_SIGMA2="
        f"{endpoint.sigma2:.15e}"
    )

    print(
        "ENDPOINT_SIGMA2_RELERR="
        f"{sigma2_relerr:.15e}"
    )

    print(
        "ENDPOINT_A_STRING="
        f"{endpoint.a_string:.15e}"
    )

    print(
        "ENDPOINT_A_STRING_RELERR="
        f"{a_relerr:.15e}"
    )

    print(
        "ENDPOINT_K="
        f"{endpoint.k:.15e}"
    )

    print(
        "ENDPOINT_K_RELERR="
        f"{k_relerr:.15e}"
    )

    print(
        "ENDPOINT_OMEGA="
        f"{endpoint.omega:.15e}"
    )

    print(
        "ENDPOINT_OMEGA_RELERR="
        f"{omega_relerr:.15e}"
    )

    print(
        "EOS_ENDPOINT_RECONSTRUCTION="
        f"{'PASS' if endpoint_pass else 'FAIL'}"
    )

    if not endpoint_pass:

        print(
            "018B0A_INTEGER_LOCKED_EOS_GATE=RED"
        )

        print(
            "NEXT=REPAIR_EOS_RECONSTRUCTION_BEFORE_ANY_PARAMETER_SCAN"
        )

        return

    # ========================================================================
    # Show why naive rounding was insufficient.
    # ========================================================================

    print(
        "\n=== NAIVE ROUNDING DIAGNOSTIC ==="
    )

    previous_r = (
        5.638035286988926e3
    )

    previous_n = (
        12553
    )

    naive_k = (
        previous_n
        /
        previous_r
    )

    naive_chi = (
        omega_expected
        *
        omega_expected

        -
        naive_k
        *
        naive_k
    )

    print(
        "B0_CONTINUOUS_R="
        f"{previous_r:.15e}"
    )

    print(
        f"B0_ROUNDED_N={previous_n}"
    )

    print(
        "NAIVE_FIXED_R_FIXED_OMEGA_CHI="
        f"{naive_chi:.15e}"
    )

    print(
        "NAIVE_CHI_INSIDE_VERIFIED_BAND="
        f"{'YES' if CHI_MIN <= naive_chi <= CHI_MAX else 'NO'}"
    )

    # ========================================================================
    # Full integer map at F=0.0384.
    # ========================================================================

    print(
        "\n=== FULL INTEGER MAP AT F=0.0384 ==="
    )

    all_locks = (
        all_integer_locks(
            anchors,
            F_REFERENCE,
        )
    )

    print(
        "REFERENCE_F_INTEGER_ROOT_COUNT="
        f"{len(all_locks)}"
    )

    mapped = []

    for index, locked in enumerate(
        all_locks
    ):

        gravity = optimize_height(
            anchors,
            locked,
        )

        if gravity is None:
            continue

        stability = stability_metrics(
            locked
        )

        if not stability[
            "pass"
        ]:
            continue

        mapped.append(
            (
                locked,
                gravity,
                stability,
            )
        )

        if (
            index
            <
            3

            or
            index
            >=
            len(
                all_locks
            )
            -
            3
        ):

            print_locked(
                "REFERENCE_INTEGER_EDGE",
                locked,
                gravity,
            )

    if not mapped:

        print(
            "SELECTED_F_FULL_INTEGER_MAP=FAIL"
        )

        print(
            "018B0A_INTEGER_LOCKED_EOS_GATE=RED"
        )

        return

    best_reference = min(
        mapped,
        key=lambda item:
            item[
                1
            ][
                "c_eff"
            ],
    )

    highest_reference = max(
        mapped,
        key=lambda item:
            item[
                0
            ].branch.chi,
    )

    print_locked(
        "REFERENCE_F_BEST_INTEGER",
        best_reference[
            0
        ],
        best_reference[
            1
        ],
    )

    print_locked(
        "REFERENCE_F_HIGHEST_CHI_INTEGER",
        highest_reference[
            0
        ],
        highest_reference[
            1
        ],
    )

    high_is_best = (
        best_reference[
            0
        ].n_integer
        ==
        highest_reference[
            0
        ].n_integer
    )

    print(
        "HIGHEST_CHI_INTEGER_IS_MINIMUM_C_AT_REFERENCE_F="
        f"{'YES' if high_is_best else 'NO'}"
    )

    print(
        "SELECTED_F_FULL_INTEGER_MAP=PASS"
    )

    # ========================================================================
    # Dense F scan.
    # ========================================================================

    print(
        "\n=== DENSE INTEGER-LOCKED F SEARCH ==="
    )

    f_results = []

    for f_value in F_SCAN:

        result = candidate_at_f(
            anchors,
            float(
                f_value
            ),
        )

        if result is None:
            continue

        f_results.append(
            result
        )

    print(
        "DENSE_F_TOTAL="
        f"{len(F_SCAN)}"
    )

    print(
        "DENSE_F_INTEGER_LOCKED_PASSING="
        f"{len(f_results)}"
    )

    if not f_results:

        print(
            "INTEGER_LOCKED_FEASIBLE_REGION=NO"
        )

        print(
            "018B0A_INTEGER_LOCKED_EOS_GATE=RED"
        )

        return

    print(
        "INTEGER_LOCKED_FEASIBLE_REGION=YES"
    )

    lowest_c = min(
        f_results,
        key=lambda item:
            item[
                1
            ][
                "c_eff"
            ],
    )

    max_f = max(
        f_results,
        key=lambda item:
            item[
                0
            ].f_value,
    )

    print_locked(
        "LOCKED_SCAN_LOWEST_C",
        lowest_c[
            0
        ],
        lowest_c[
            1
        ],
    )

    print_locked(
        "LOCKED_SCAN_MAX_F",
        max_f[
            0
        ],
        max_f[
            1
        ],
    )

    # ========================================================================
    # Finalist integer-lock stress.
    # ========================================================================

    print(
        "\n=== 6561-CASE INTEGER-RELOCKED FINALIST STRESS ==="
    )

    finalist_records = []

    for f_value in FINALIST_F:

        nominal = candidate_at_f(
            anchors,
            f_value,
        )

        if nominal is None:

            print(
                "LOCKED_FINALIST "
                f"F={f_value:.9f} "
                "FOUND=NO"
            )

            continue

        locked, gravity, stability = (
            nominal
        )

        stress = (
            deterministic_relocked_stress(
                anchors,
                locked,
                gravity,
            )
        )

        finalist_records.append(
            (
                locked,
                gravity,
                stability,
                stress,
            )
        )

        print_locked(
            "LOCKED_FINALIST_NOMINAL",
            locked,
            gravity,
        )

        print(
            "LOCKED_FINALIST_STRESS "
            f"F={locked.f_value:.9f} "
            f"TOTAL={stress['total']} "
            f"PASSING={stress['passed']} "
            f"ALL_PASS={'YES' if stress['all_pass'] else 'NO'} "
            f"DEEP_PASS={'YES' if stress['deep_pass'] else 'NO'} "
            f"MIN_PAYLOAD={stress['min_payload']:+.15e} "
            f"MIN_POINT={stress['min_point']:+.15e} "
            f"MIN_LEVERAGE={stress['min_leverage']:.15e} "
            f"MIN_SCALE={stress['min_scale']:.15e} "
            f"MIN_LOCKED_CHI={stress['min_chi']:.15e} "
            f"MAX_LOCKED_CHI={stress['max_chi']:.15e} "
            f"MAX_C={stress['max_c']:.15e}"
        )

        print(
            "LOCKED_FINALIST_WORST_CASE="
            f"{stress['worst']}"
        )

    deep = [
        record
        for record
        in finalist_records
        if record[
            3
        ][
            "deep_pass"
        ]
    ]

    if not deep:

        print(
            "DEEP_ROBUST_INTEGER_LOCKED_SINGLE_VORTON=NO"
        )

        print(
            "018B0A_INTEGER_LOCKED_EOS_GATE=RED"
        )

        print(
            "NEXT=RETURN_TO_VALIDATED_TWO_COPY_ARCHITECTURE"
        )

        return

    # Robustness first: use largest F among deep survivors, matching 018B-0.
    selected_record = max(
        deep,
        key=lambda item:
            item[
                0
            ].f_value,
    )

    (
        selected_locked,
        selected_gravity,
        selected_stability,
        selected_stress,
    ) = selected_record

    print(
        "\n=== SELECTED INTEGER-LOCKED ARCHITECTURE ==="
    )

    print_locked(
        "SELECTED_INTEGER_LOCKED",
        selected_locked,
        selected_gravity,
    )

    print(
        "LOCKED_CT2="
        f"{selected_stability['ct2']:.15e}"
    )

    print(
        "LOCKED_CL2="
        f"{selected_stability['cl2']:.15e}"
    )

    print(
        "LOCKED_MIN_M2_TO_M40_DISCRIMINANT="
        f"{selected_stability['min_disc']:+.15e}"
    )

    print(
        "LOCKED_WORST_MODE="
        f"{selected_stability['worst_mode']}"
    )

    print(
        "LOCKED_MAX_ROOT_IMAG="
        f"{selected_stability['max_imag']:.15e}"
    )

    print(
        "LOCKED_WORLD_SHEET_STABILITY="
        f"{'PASS' if selected_stability['pass'] else 'FAIL'}"
    )

    # ========================================================================
    # Fixed-N local continuity.
    # ========================================================================

    print(
        "\n=== FIXED-N LOCAL CONTINUITY ==="
    )

    fixed_n = (
        fixed_n_continuity(
            anchors,
            selected_locked,
            selected_gravity,
        )
    )

    print(
        "FIXED_N="
        f"{selected_locked.n_integer}"
    )

    print(
        "FIXED_N_CONTINUITY_TOTAL="
        f"{fixed_n['total']}"
    )

    print(
        "FIXED_N_CONTINUITY_PASSING="
        f"{fixed_n['passed']}"
    )

    print(
        "FIXED_N_CONTINUITY_MIN_PAYLOAD="
        f"{fixed_n['min_payload']:+.15e}"
    )

    print(
        "FIXED_N_CONTINUITY_MIN_CHI="
        f"{fixed_n['min_chi']:.15e}"
    )

    print(
        "FIXED_N_CONTINUITY_MAX_CHI="
        f"{fixed_n['max_chi']:.15e}"
    )

    print(
        "FIXED_N_LOCAL_CONTINUITY="
        f"{'PASS' if fixed_n['pass'] else 'FAIL'}"
    )

    # ========================================================================
    # Random re-lock stress.
    # ========================================================================

    print(
        "\n=== 20,000-CASE RANDOM INTEGER-RELOCKED STRESS ==="
    )

    random = (
        randomized_relocked_stress(
            anchors,
            selected_locked,
            selected_gravity,
        )
    )

    print(
        "INTEGER_RELOCKED_RANDOM_TOTAL="
        f"{random['total']}"
    )

    print(
        "INTEGER_RELOCKED_RANDOM_PASSING="
        f"{random['passed']}"
    )

    print(
        "INTEGER_RELOCKED_RANDOM_PASS_FRACTION="
        f"{random['passed'] / random['total']:.15f}"
    )

    print(
        "INTEGER_RELOCKED_RANDOM_MIN_PAYLOAD="
        f"{random['min_payload']:+.15e}"
    )

    print(
        "INTEGER_RELOCKED_RANDOM_MIN_LEVERAGE="
        f"{random['min_leverage']:.15e}"
    )

    print(
        "INTEGER_RELOCKED_RANDOM_MIN_SCALE="
        f"{random['min_scale']:.15e}"
    )

    print(
        "INTEGER_RELOCKED_RANDOM_STRESS="
        f"{'PASS' if random['pass'] else 'FAIL'}"
    )

    # ========================================================================
    # Direct BVP verification.
    # ========================================================================

    print(
        "\n=== DIRECT 017P BVP INTEGER-LOCK VERIFICATION ==="
    )

    interpolation_at_selected = (
        reconstruct_branch(
            selected_locked.branch.chi
        )
    )

    direct_at_interp_root = (
        direct_bvp_state(
            selected_locked.branch.chi
        )
    )

    sigma2_bvp_relerr = (
        abs(
            direct_at_interp_root[
                "sigma2"
            ]
            -
            interpolation_at_selected.sigma2
        )
        /
        direct_at_interp_root[
            "sigma2"
        ]
    )

    a_bvp_relerr = (
        abs(
            direct_at_interp_root[
                "a_string"
            ]
            -
            interpolation_at_selected.a_string
        )
        /
        direct_at_interp_root[
            "a_string"
        ]
    )

    p_bvp_relerr = (
        abs(
            direct_at_interp_root[
                "p_parallel"
            ]
            -
            interpolation_at_selected.p_parallel
        )
        /
        abs(
            direct_at_interp_root[
                "p_parallel"
            ]
        )
    )

    print(
        "BVP_AT_INTERPOLATED_LOCK_SIGMA2_RELERR="
        f"{sigma2_bvp_relerr:.15e}"
    )

    print(
        "BVP_AT_INTERPOLATED_LOCK_A_STRING_RELERR="
        f"{a_bvp_relerr:.15e}"
    )

    print(
        "BVP_AT_INTERPOLATED_LOCK_P_PARALLEL_RELERR="
        f"{p_bvp_relerr:.15e}"
    )

    direct_lock = (
        direct_integer_lock(
            anchors,
            selected_locked,
        )
    )

    if direct_lock is None:

        print(
            "DIRECT_BVP_INTEGER_LOCK=FAIL"
        )

        print(
            "018B0A_INTEGER_LOCKED_EOS_GATE=RED"
        )

        return

    print(
        "DIRECT_BVP_LOCKED_CHI="
        f"{direct_lock['chi']:.15e}"
    )

    print(
        "DIRECT_BVP_LOCKED_N="
        f"{direct_lock['n']}"
    )

    print(
        "DIRECT_BVP_LOCKED_R="
        f"{direct_lock['radius']:.15e}"
    )

    print(
        "DIRECT_BVP_INTEGER_RESIDUAL="
        f"{direct_lock['residual']:+.15e}"
    )

    chi_shift = (
        direct_lock[
            "chi"
        ]
        -
        selected_locked.branch.chi
    )

    print(
        "DIRECT_BVP_VS_INTERPOLATED_LOCK_CHI_SHIFT="
        f"{chi_shift:+.15e}"
    )

    direct_lock_pass = (
        CHI_MIN
        <=
        direct_lock[
            "chi"
        ]
        <=
        CHI_MAX

        and
        abs(
            direct_lock[
                "residual"
            ]
        )
        <
        INTEGER_RESIDUAL_TOL

        and
        sigma2_bvp_relerr
        <
        2.0e-4

        and
        a_bvp_relerr
        <
        2.0e-4

        and
        p_bvp_relerr
        <
        2.0e-4
    )

    print(
        "DIRECT_BVP_INTEGER_LOCK="
        f"{'PASS' if direct_lock_pass else 'FAIL'}"
    )

    # ========================================================================
    # Direct-BVP variational/EOS verification.
    # ========================================================================

    print(
        "\n=== DIRECT BVP LOCAL EOS CHECK ==="
    )

    derivative_step = (
        2.0e-5
    )

    left_chi = max(
        CHI_MIN,
        direct_lock[
            "chi"
        ]
        -
        derivative_step,
    )

    right_chi = min(
        CHI_MAX,
        direct_lock[
            "chi"
        ]
        +
        derivative_step,
    )

    left_state = (
        direct_bvp_state(
            left_chi
        )
    )

    right_state = (
        direct_bvp_state(
            right_chi
        )
    )

    center_state = (
        direct_lock[
            "state"
        ]
    )

    d_a = (
        right_state[
            "a_string"
        ]
        -
        left_state[
            "a_string"
        ]
    ) / (
        right_chi
        -
        left_chi
    )

    d_sigma = (
        right_state[
            "sigma2"
        ]
        -
        left_state[
            "sigma2"
        ]
    ) / (
        right_chi
        -
        left_chi
    )

    variational_relerr = (
        abs(
            d_a
            +
            center_state[
                "sigma2"
            ]
        )
        /
        center_state[
            "sigma2"
        ]
    )

    ct2_direct = (
        1.0
        /
        (
            1.0
            +
            2.0
            *
            direct_lock[
                "chi"
            ]
            *
            center_state[
                "sigma2"
            ]
            /
            center_state[
                "a_string"
            ]
        )
    )

    cl2_direct = (
        1.0
        /
        (
            1.0
            +
            2.0
            *
            direct_lock[
                "chi"
            ]
            *
            d_sigma
            /
            center_state[
                "sigma2"
            ]
        )
    )

    (
        direct_stability,
        direct_min_disc,
        direct_max_imag,
        direct_worst_mode,
    ) = (
        fc.extrinsic_stability(
            ct2_direct,
            cl2_direct,
        )
    )

    direct_eos_pass = (
        variational_relerr
        <
        2.0e-3

        and
        0.0
        <
        ct2_direct
        <=
        1.0

        and
        0.0
        <
        cl2_direct
        <=
        1.0

        and
        direct_stability
    )

    print(
        "DIRECT_BVP_VARIATIONAL_RELERR="
        f"{variational_relerr:.15e}"
    )

    print(
        "DIRECT_BVP_CT2="
        f"{ct2_direct:.15e}"
    )

    print(
        "DIRECT_BVP_CL2="
        f"{cl2_direct:.15e}"
    )

    print(
        "DIRECT_BVP_MIN_M2_TO_M40_DISCRIMINANT="
        f"{direct_min_disc:+.15e}"
    )

    print(
        "DIRECT_BVP_WORST_MODE="
        f"{direct_worst_mode}"
    )

    print(
        "DIRECT_BVP_MAX_ROOT_IMAG="
        f"{direct_max_imag:.15e}"
    )

    print(
        "DIRECT_BVP_EOS_STABILITY="
        f"{'PASS' if direct_eos_pass else 'FAIL'}"
    )

    # ========================================================================
    # High precision direct-BVP gravity.
    # ========================================================================

    print(
        "\n=== HIGH-PRECISION INTEGER-LOCKED GRAVITY ==="
    )

    direct_gravity = (
        direct_locked_gravity(
            anchors,
            direct_lock,
            selected_locked.f_value,
        )
    )

    if direct_gravity is None:

        print(
            "HIGH_PRECISION_LOCKED_GRAVITY=FAIL"
        )

        print(
            "018B0A_INTEGER_LOCKED_EOS_GATE=RED"
        )

        return

    print(
        "DIRECT_LOCK_OPTIMAL_X="
        f"{direct_gravity['x']:.15e}"
    )

    print(
        "DIRECT_LOCK_POINT_OUTWARD="
        f"{direct_gravity['point']:+.15e}"
    )

    print(
        "DIRECT_LOCK_PAYLOAD_OUTWARD="
        f"{direct_gravity['payload']:+.15e}"
    )

    for (
        width,
        inward,
    ) in direct_gravity[
        "rim_values"
    ]:

        print(
            "DIRECT_LOCK_RIM_CORE "
            f"WIDTH={float(width):.15e} "
            f"INWARD={float(inward):.15e}"
        )

    print(
        "DIRECT_LOCK_SCOUT_VS_ADAPTIVE_WALL_POINT_RELERR="
        f"{direct_gravity['scout_wall_point_relerr']:.15e}"
    )

    print(
        "DIRECT_LOCK_SCOUT_VS_ADAPTIVE_WALL_PAYLOAD_RELERR="
        f"{direct_gravity['scout_wall_payload_relerr']:.15e}"
    )

    print(
        "DIRECT_LOCK_C="
        f"{direct_gravity['c_eff']:.15e}"
    )

    high_precision_pass = (
        direct_gravity[
            "point"
        ]
        >
        0.0

        and
        direct_gravity[
            "payload"
        ]
        >
        0.0

        and
        direct_gravity[
            "scout_wall_point_relerr"
        ]
        <
        5.0e-6

        and
        direct_gravity[
            "scout_wall_payload_relerr"
        ]
        <
        5.0e-6
    )

    print(
        "HIGH_PRECISION_LOCKED_GRAVITY="
        f"{'PASS' if high_precision_pass else 'FAIL'}"
    )

    # ========================================================================
    # 1g / 1m energy bookkeeping.
    # ========================================================================

    print(
        "\n=== 1g / 1m ENERGY REQUIREMENT ==="
    )

    (
        projected_mass,
        projected_energy,
    ) = (
        energy_scaling(
            direct_gravity[
                "c_eff"
            ]
        )
    )

    print(
        "VALIDATED_018A8_C="
        f"{CURRENT_VALIDATED_C:.15e}"
    )

    print(
        "VALIDATED_018A8_ONE_G_ONE_M_ENERGY_J="
        f"{CURRENT_VALIDATED_ENERGY_J:.15e}"
    )

    print(
        "018B0_SOURCE_PROJECTED_C="
        f"{B0_PROJECTED_C:.15e}"
    )

    print(
        "018B0_SOURCE_PROJECTED_ONE_G_ONE_M_ENERGY_J="
        f"{B0_PROJECTED_ENERGY_J:.15e}"
    )

    print(
        "INTEGER_LOCKED_PROJECTED_C="
        f"{direct_gravity['c_eff']:.15e}"
    )

    print(
        "INTEGER_LOCKED_PROJECTED_ONE_G_ONE_M_MASS_KG="
        f"{projected_mass:.15e}"
    )

    print(
        "INTEGER_LOCKED_PROJECTED_ONE_G_ONE_M_ENERGY_J="
        f"{projected_energy:.15e}"
    )

    print(
        "INTEGER_LOCK_ENERGY_CHANGE_VS_018B0_FACTOR="
        f"{projected_energy / B0_PROJECTED_ENERGY_J:.15e}"
    )

    print(
        "PROJECTED_IMPROVEMENT_VS_VALIDATED_018A8="
        f"{CURRENT_VALIDATED_ENERGY_J / projected_energy:.15e}"
    )

    print(
        "ENERGY_MODEL_STATUS="
        "PROJECTED_UNTIL_SELECTED_F_CHI_MICROSCOPIC_WALL_AND_JUNCTION_ARE_RESOLVED"
    )

    print(
        "LATEST_VALIDATED_ONE_G_ONE_M_ENERGY_J="
        f"{CURRENT_VALIDATED_ENERGY_J:.15e}"
    )

    # ========================================================================
    # Final decision.
    # ========================================================================

    deterministic_pass = (
        selected_stress[
            "all_pass"
        ]
        and
        selected_stress[
            "deep_pass"
        ]
    )

    overall = (
        endpoint_pass

        and
        len(
            mapped
        )
        >
        0

        and
        selected_stability[
            "pass"
        ]

        and
        deterministic_pass

        and
        fixed_n[
            "pass"
        ]

        and
        random[
            "pass"
        ]

        and
        direct_lock_pass

        and
        direct_eos_pass

        and
        high_precision_pass
    )

    print(
        "\n=== 018B-0A DECISION ==="
    )

    print(
        "EOS_ENDPOINT_RECONSTRUCTION="
        f"{'PASS' if endpoint_pass else 'FAIL'}"
    )

    print(
        "SELECTED_F_FULL_INTEGER_MAP=PASS"
    )

    print(
        "INTEGER_LOCKED_FEASIBLE_REGION=YES"
    )

    print(
        "LOCKED_WORLD_SHEET_STABILITY="
        f"{'PASS' if selected_stability['pass'] else 'FAIL'}"
    )

    print(
        "INTEGER_RELOCKED_DETERMINISTIC_STRESS="
        f"{'PASS' if deterministic_pass else 'FAIL'}"
    )

    print(
        "FIXED_N_LOCAL_CONTINUITY="
        f"{'PASS' if fixed_n['pass'] else 'FAIL'}"
    )

    print(
        "INTEGER_RELOCKED_RANDOM_STRESS="
        f"{'PASS' if random['pass'] else 'FAIL'}"
    )

    print(
        "DIRECT_BVP_INTEGER_LOCK="
        f"{'PASS' if direct_lock_pass else 'FAIL'}"
    )

    print(
        "DIRECT_BVP_EOS_STABILITY="
        f"{'PASS' if direct_eos_pass else 'FAIL'}"
    )

    print(
        "HIGH_PRECISION_LOCKED_GRAVITY="
        f"{'PASS' if high_precision_pass else 'FAIL'}"
    )

    print(
        "018B0A_INTEGER_LOCKED_EOS_ARCHITECTURE_GATE="
        f"{'GREEN' if overall else 'RED'}"
    )

    if overall:

        print(
            "INTEGER_LOCKED_018B_TARGET_F="
            f"{selected_locked.f_value:.12f}"
        )

        print(
            "INTEGER_LOCKED_018B_TARGET_CHI="
            f"{direct_lock['chi']:.15e}"
        )

        print(
            "INTEGER_LOCKED_018B_TARGET_N="
            f"{direct_lock['n']}"
        )

        print(
            "INTEGER_LOCKED_018B_TARGET_R="
            f"{direct_lock['radius']:.15e}"
        )

        print(
            "INTEGER_LOCKED_018B_TARGET_X="
            f"{direct_gravity['x']:.15e}"
        )

        print(
            "018B_TARGET_ARCHITECTURE="
            "SINGLE_STATIONARY_GAUGED_VORTON_PLUS_ONE_KLS_WALL"
        )

        print(
            "NEXT="
            "018B0B_MICROSCOPIC_REVALIDATION_AT_INTEGER_LOCKED_F_CHI"
        )

    else:

        print(
            "018B_TARGET_ARCHITECTURE="
            "DO_NOT_PROMOTE_NEW_SINGLE_VORTON_POINT"
        )

        print(
            "NEXT="
            "IDENTIFY_INTEGER_LOCK_OR_DIRECT_BVP_FAILURE_CHANNEL"
        )

    print(
        "FULL_018A_GATE="
        "GREEN_INHERITED_FOR_VALIDATED_TWO_COPY_SOURCE"
    )

    print(
        "NEW_SINGLE_VORTON_MICROSCOPIC_REVALIDATION="
        "NOT_YET_COMPLETE"
    )

    print(
        "TRUE_018B_GLOBAL_TOROIDAL_FIELD_SOLUTION="
        "NOT_YET_RUN"
    )

    print(
        "CURRENT_HEURISTIC="
        "APPROXIMATELY_66_PERCENT_NOT_A_PROBABILITY"
    )

    print(
        "HEURISTIC_INCREASE_FROM_THIS_GATE="
        "NO_EOS_QUANTIZATION_CONSISTENCY_ALONE_DOES_NOT_EARN_018B_PROMOTION"
    )

    print(
        "PRACTICAL_ENERGY_SCALING="
        "STILL_CATASTROPHIC"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )

    print(
        "NEW_PHYSICS_DISCOVERY=NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_018B0A_INTEGER_LOCKED_EOS_ARCHITECTURE_GATE"
    )


if __name__ == "__main__":
    main()
