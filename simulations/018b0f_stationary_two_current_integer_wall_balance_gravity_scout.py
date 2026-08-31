#!/usr/bin/env python3
"""Simulation 018B-0F — stationary two-current integer wall-balance gravity scout.

PURPOSE
-------
Test whether the literature-backed two-current straight-string state selected
in 018B-0D has a stationary, angular-momentum-carrying loop frame that can
support the new 018B-0F0 KLS wall while preserving outward finite-payload
linearized-GR gravity.

SCIENTIFIC QUESTION
-------------------
Can one Lorentz-related state of the already-solved two-current string satisfy,
at the same time,

    exact integer winding for both currents;
    positive laboratory-frame longitudinal pressure;
    near-exact wall balance;
    R / wall_width90 >= 10;
    positive total active mass;
    outward finite-payload gravity;
    a conservative wall/rim finite-size stress test?

This is deliberately a source-level scout before the new two-current 2D
string-wall junction is solved. It may authorize that junction calculation;
it may not promote a new microscopic realization or energy coefficient.

WORLDSHEET KINEMATICS
---------------------
The 018B-0D zero-momentum eigenframe has

    T^{ab} = diag(U, -T).

For a boost v along the string,

    E = gamma^2 (U - v^2 T)
    P = gamma^2 (v^2 U - T)
    J = -gamma^2 v (U-T)

and the gravitoelectric active line source is

    Lambda_active = E + P.

The phase gradients transform as

    omega_i' = gamma (omega_i - v k_i)
    k_i'     = gamma (k_i - v omega_i).

Positive wall-supporting compression requires

    P > 0

or equivalently

    v^2 > T/U.

INTEGER CLOSURE
---------------
For a circular loop,

    k_phi' R   = N_phi
    k_sigma' R = N_sigma

with integers N_phi and N_sigma. For every coprime base integer pair the
required boost is solved algebraically, then a common integer multiplier is
chosen to approach wall balance.

MECHANICAL BALANCE
------------------
Before the not-yet-rederived junction is included, use

    P = sigma_W R.

Require fractional mismatch <= 1e-4.

GRAVITY
-------
Use the measured 018B-0F0 quantities separately:

    wall mechanical tension = sigma_W
    wall integrated active source = S_W < 0.

For a thin wall disk at z=z_W and an axis payload center h,

    F_W = 2 pi |S_W| R
          [1 - (h-z_W)/sqrt(R^2+(h-z_W)^2)].

For the positive active rim,

    Q_rim = 2 pi R Lambda_active.

The payload is a uniform sphere with radius a=0.25 h. The scout requires its
lower surface to lie at least five measured wall widths above the wall center.
For the thin source planes/rim used here the payload is therefore source-free,
so the spherical mean-value identity makes its center-of-mass acceleration
identical to the center acceleration.

FINITE-SIZE STRESS TEST
-----------------------
The nominal thin result is not accepted alone. Recompute the gravitational
sign after deliberately:

    moving the entire negative wall source two wall-width90 measures farther
    from the payload;

    and placing the complete positive rim active source at the most attractive
    of a 3x3 cross-section envelope with

        Delta r = 0, +/-2 core_width
        Delta z = 0, +/-2 core_width.

This is a deliberately adverse scout envelope, not a replacement for the
actual finite-thickness 018B field solution.

SEARCH POLICIES
---------------
The following are robustness policies rather than physical theorems:

    |v| <= 0.99
    R / wall_width90 >= 10
    payload bottom / wall_width90 >= 5

The first prevents promotion from relying on the v -> 1 boundary.

ENERGY LEDGER
-------------
At scout level,

    E_total/R = pi sigma_W R + 2 pi E.

The project coefficient is

    C_eff = (E_total/R) / [F_payload (h/R)^2].

The new two-current 2D junction is absent, so any C reported here is

    PROJECTED_PREFLIGHT_NOT_VALIDATED.

FALSIFIER / STOP RULE
---------------------
If no exact-integer deep-interior candidate survives balance and gravity, do
not launch the 2D junction merely because ultra-relativistic v -> 1 states can
formally generate large pressure.

If GREEN, next is

    018B0G_NEW_TWO_CURRENT_2D_STRING_WALL_JUNCTION_REVALIDATION.

CLAIM LIMITS
------------
This scout does not establish:

- a curved microscopic toroidal field solution;
- the new two-current 2D string-wall junction;
- full circular-loop stability;
- complete T_munu of the curved field configuration;
- frame-dragging consistency;
- nonlinear Einstein-matter consistency;
- payload backreaction;
- a validated new energy coefficient;
- practical antigravity.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_018B0F_STATIONARY_TWO_CURRENT_INTEGER_WALL_BALANCE_GRAVITY_SCOUT
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
import re

from scipy.optimize import minimize_scalar


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


# ---------------------------------------------------------------------------
# Search / robustness policy.
# ---------------------------------------------------------------------------

BASE_WINDING_MAX = 500

# Deliberately leave at least 1 percent subluminal headroom.
MAX_ABS_V = 0.99

BALANCE_REL_TOL = 1.0e-4

MIN_R_OVER_WALL90 = 10.0

MIN_PAYLOAD_BOTTOM_OVER_WALL90 = 5.0

PAYLOAD_RADIUS_OVER_H = 0.25

X_MIN = 0.01
X_MAX = 0.45

CORE_ENVELOPE_MULTIPLIER = 2.0

WALL_ADVERSE_SHIFT_WIDTHS = 2.0


# ---------------------------------------------------------------------------
# Current validated energy ledger.
#
# A value found in this scout MUST NOT replace these numbers until the new
# microscopic junction and subsequent complete source revalidation are GREEN.
# ---------------------------------------------------------------------------

VALIDATED_C = 1.774169582609975e6

VALIDATED_MASS_1G_1M = (
    2.606814218315347e17
)

VALIDATED_ENERGY_1G_1M = (
    2.342887778715687e34
)


# Blind wildcard diagnostic only.
#
# These values are deliberately carried as a nonprivileged check requested by
# the project workflow. They are not optimization targets or evidence.
WILDCARD_X_FACTORS = (
    0.625,
    1.6,
    1.875,
    3.125,
    5.0,
)


@dataclass(
    frozen=True,
)
class State:
    """018B-0D straight-string zero-momentum worldsheet state."""

    U: float
    T: float

    omega_phi: float
    k_phi: float

    omega_sigma: float
    k_sigma: float


@dataclass(
    frozen=True,
)
class Wall:
    """018B-0F0 microscopic wall quantities used by the scout."""

    tension: float

    active: float

    width90: float

    core_width: float


@dataclass
class Candidate:
    """One exact dual-integer stationary-loop candidate."""

    base_phi: int
    base_sigma: int

    mult: int

    n_phi: int
    n_sigma: int

    v: float
    gamma: float

    radius: float

    balance_rel: float

    energy_line: float
    pressure_line: float
    momentum_line: float
    active_line: float

    omega_phi_lab: float
    k_phi_lab: float

    omega_sigma_lab: float
    k_sigma_lab: float

    x: float = math.nan

    c_worst: float = math.inf

    f_nominal: float = -math.inf

    f_worst: float = -math.inf

    active_mass_per_r: float = -math.inf

    clearance: float = -math.inf


def scalar(
    path: Path,
    label: str,
) -> float:
    """Read a finite floating-point result immediately after an exact label."""

    text = path.read_text(
        errors="replace",
    )

    number = (
        r"([+-]?"
        r"(?:\d+(?:\.\d*)?|\.\d+)"
        r"(?:[eE][+-]?\d+)?)"
    )

    match = re.search(
        re.escape(
            label,
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
            1,
        )
    )

    if not math.isfinite(
        value,
    ):
        raise RuntimeError(
            f"Nonfinite {label!r} in {path}"
        )

    return value


def require(
    path: Path,
    marker: str,
) -> None:
    """Require an upstream GREEN marker before inheriting its output."""

    if not path.exists():
        raise RuntimeError(
            f"Missing upstream log: {path}"
        )

    text = path.read_text(
        errors="replace",
    )

    if marker not in text:
        raise RuntimeError(
            f"Missing upstream marker {marker!r} in {path}"
        )


def load_inputs() -> tuple[
    State,
    Wall,
]:
    """Load only quantities explicitly promoted by 018B-0D and 018B-0F0."""

    require(
        D_LOG,
        "018B0D_TWO_CURRENT_COUNTERFLOW_GATE=GREEN",
    )

    require(
        F0_LOG,
        "018B0F0_LILLEY_KLS_NORMALIZATION_WALL_BRIDGE=GREEN",
    )

    state = State(
        U=scalar(
            D_LOG,
            "ENERGY_PER_LENGTH_U=",
        ),

        T=scalar(
            D_LOG,
            "TENSION_T=",
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

    wall = Wall(
        tension=scalar(
            F0_LOG,
            "NEW_WALL_TENSION=",
        ),

        active=scalar(
            F0_LOG,
            "NEW_WALL_ACTIVE_SOURCE=",
        ),

        width90=scalar(
            F0_LOG,
            "NEW_WALL_WIDTH90=",
        ),

        core_width=scalar(
            F0_LOG,
            "NEW_STRING_GAUGE_CORE_INVERSE_MASS_PROXY=",
        ),
    )

    return (
        state,
        wall,
    )


def boost(
    state: State,
    v: float,
):
    """Lorentz-transform phase gradients and the worldsheet stress tensor.

    The zero-momentum eigenframe stress is

        T^{ab}
        =
        diag(
            U,
            -T,
        ).

    In the stationary loop frame this gives

        E
        =
        gamma^2
        (
            U
            -
            v^2 T
        )

        P
        =
        gamma^2
        (
            v^2 U
            -
            T
        )

        J
        =
        -gamma^2 v
        (
            U-T
        ).

    Here P>0 is the compressive longitudinal stress required by the membrane.
    """

    gamma = (
        1.0
        /
        math.sqrt(
            1.0
            -
            v
            *
            v
        )
    )

    gamma2 = (
        gamma
        *
        gamma
    )

    omega_phi_lab = (
        gamma
        *
        (
            state.omega_phi
            -
            v
            *
            state.k_phi
        )
    )

    k_phi_lab = (
        gamma
        *
        (
            state.k_phi
            -
            v
            *
            state.omega_phi
        )
    )

    omega_sigma_lab = (
        gamma
        *
        (
            state.omega_sigma
            -
            v
            *
            state.k_sigma
        )
    )

    k_sigma_lab = (
        gamma
        *
        (
            state.k_sigma
            -
            v
            *
            state.omega_sigma
        )
    )

    energy = (
        gamma2
        *
        (
            state.U
            -
            v
            *
            v
            *
            state.T
        )
    )

    pressure = (
        gamma2
        *
        (
            v
            *
            v
            *
            state.U
            -
            state.T
        )
    )

    momentum = (
        -gamma2
        *
        v
        *
        (
            state.U
            -
            state.T
        )
    )

    active = (
        energy
        +
        pressure
    )

    return (
        gamma,

        omega_phi_lab,
        k_phi_lab,

        omega_sigma_lab,
        k_sigma_lab,

        energy,
        pressure,
        momentum,
        active,
    )


def exact_v(
    state: State,
    n_phi: int,
    n_sigma: int,
):
    """Solve analytically for the boost giving one exact winding ratio.

    Exact closure requires

        N_phi / k_phi'
        =
        N_sigma / k_sigma'.

    Eliminating gamma gives

        v
        =
        (
            k_phi N_sigma
            -
            k_sigma N_phi
        )
        /
        (
            omega_phi N_sigma
            -
            omega_sigma N_phi
        ).
    """

    denominator = (
        state.omega_phi
        *
        n_sigma

        -

        state.omega_sigma
        *
        n_phi
    )

    if abs(
        denominator
    ) < 1.0e-15:
        return None

    return (
        state.k_phi
        *
        n_sigma

        -

        state.k_sigma
        *
        n_phi
    ) / denominator


def ring_kernel(
    radius: float,
    z_source: float,
    h_payload: float,
) -> float:
    """Return the positive-magnitude axial kernel of a circular source ring."""

    vertical = (
        h_payload
        -
        z_source
    )

    distance = math.hypot(
        radius,
        vertical,
    )

    return (
        vertical
        /
        distance**3
    )


def gravity_and_c(
    wall: Wall,
    candidate: Candidate,
    x: float,
    adverse: bool,
):
    """Evaluate source-level gravity and projected coefficient.

    The negative-active wall disk gives an outward contribution.

    The positive-active stationary rim gives an inward contribution.

    For the adverse envelope:

    - displace the entire negative wall two measured wall widths farther from
      the payload;
    - choose the most attractive rim location in a 3x3 +/-2-core-width
      cross-sectional location envelope.

    This is intentionally conservative but remains only a scout.
    """

    radius = (
        candidate.radius
    )

    h_payload = (
        x
        *
        radius
    )

    if adverse:

        wall_z = (
            -WALL_ADVERSE_SHIFT_WIDTHS
            *
            wall.width90
        )

        core = (
            CORE_ENVELOPE_MULTIPLIER
            *
            wall.core_width
        )

    else:

        wall_z = 0.0

        core = 0.0

    vertical_wall = (
        h_payload
        -
        wall_z
    )

    wall_kernel = (
        1.0

        -

        vertical_wall
        /
        math.sqrt(
            radius
            *
            radius

            +

            vertical_wall
            *
            vertical_wall
        )
    )

    # wall.active is negative.
    wall_outward = (
        2.0
        *
        math.pi
        *
        (
            -wall.active
        )
        *
        radius
        *
        wall_kernel
    )

    q_rim = (
        2.0
        *
        math.pi
        *
        radius
        *
        candidate.active_line
    )

    if adverse:

        inward_kernel = max(
            ring_kernel(
                radius
                +
                dr,

                dz,

                h_payload,
            )

            for dr in (
                -core,
                0.0,
                core,
            )

            for dz in (
                -core,
                0.0,
                core,
            )

            if (
                radius
                +
                dr
                >
                0.0
            )
        )

    else:

        inward_kernel = (
            ring_kernel(
                radius,
                0.0,
                h_payload,
            )
        )

    rim_inward = (
        radius
        *
        q_rim
        *
        inward_kernel
    )

    net_outward = (
        wall_outward
        -
        rim_inward
    )

    # Energy per source radius.
    #
    # Disk:
    #     E_wall/R = pi sigma R.
    #
    # Ring:
    #     E_rim/R = 2 pi E_line.
    energy_per_r = (
        math.pi
        *
        wall.tension
        *
        radius

        +

        2.0
        *
        math.pi
        *
        candidate.energy_line
    )

    # Total active source divided by R.
    active_mass_per_r = (
        2.0
        *
        math.pi
        *
        candidate.active_line

        +

        math.pi
        *
        wall.active
        *
        radius
    )

    payload_bottom = (
        (
            1.0
            -
            PAYLOAD_RADIUS_OVER_H
        )
        *
        h_payload
    )

    clearance = (
        payload_bottom
        /
        wall.width90
    )

    if net_outward <= 0.0:

        c_eff = math.inf

    else:

        c_eff = (
            energy_per_r
            /
            (
                net_outward
                *
                x
                *
                x
            )
        )

    return (
        net_outward,
        c_eff,
        active_mass_per_r,
        clearance,
        wall_outward,
        rim_inward,
    )


def invariant_errors(
    state: State,
    candidate: Candidate,
):
    """Independently verify Lorentz and dual-integer invariants."""

    phi_before = (
        state.omega_phi**2
        -
        state.k_phi**2
    )

    phi_after = (
        candidate.omega_phi_lab**2
        -
        candidate.k_phi_lab**2
    )

    sigma_before = (
        state.omega_sigma**2
        -
        state.k_sigma**2
    )

    sigma_after = (
        candidate.omega_sigma_lab**2
        -
        candidate.k_sigma_lab**2
    )

    phi_rel = (
        abs(
            phi_after
            -
            phi_before
        )
        /
        max(
            abs(
                phi_before
            ),
            1.0e-30,
        )
    )

    sigma_rel = (
        abs(
            sigma_after
            -
            sigma_before
        )
        /
        max(
            abs(
                sigma_before
            ),
            1.0e-30,
        )
    )

    # For the 1+1 stress matrix under the conventions used above:
    #
    # trace(T^a_b)
    # =
    # U + T
    # =
    # E - P.
    trace_before = (
        state.U
        +
        state.T
    )

    trace_after = (
        candidate.energy_line
        -
        candidate.pressure_line
    )

    trace_rel = (
        abs(
            trace_after
            -
            trace_before
        )
        /
        max(
            abs(
                trace_before
            ),
            1.0e-30,
        )
    )

    determinant_before = (
        -state.U
        *
        state.T
    )

    determinant_after = (
        candidate.energy_line
        *
        candidate.pressure_line

        -

        candidate.momentum_line**2
    )

    determinant_rel = (
        abs(
            determinant_after
            -
            determinant_before
        )
        /
        max(
            abs(
                determinant_before
            ),
            1.0e-30,
        )
    )

    radius_phi = (
        candidate.n_phi
        /
        candidate.k_phi_lab
    )

    radius_sigma = (
        candidate.n_sigma
        /
        candidate.k_sigma_lab
    )

    radius_rel = (
        abs(
            radius_phi
            -
            radius_sigma
        )
        /
        max(
            abs(
                radius_phi
            ),
            abs(
                radius_sigma
            ),
            1.0e-30,
        )
    )

    return (
        phi_rel,
        sigma_rel,
        trace_rel,
        determinant_rel,
        radius_rel,
    )


def enumerate_candidates(
    state: State,
    wall: Wall,
):
    """Enumerate exact integer stationary loops satisfying the scout gates."""

    ct2 = (
        state.T
        /
        state.U
    )

    found = {}

    for base_phi in range(
        -BASE_WINDING_MAX,
        BASE_WINDING_MAX
        +
        1,
    ):

        if base_phi == 0:
            continue

        for base_sigma in range(
            -BASE_WINDING_MAX,
            BASE_WINDING_MAX
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

            v = exact_v(
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
                MAX_ABS_V
            ):
                continue

            # Positive longitudinal pressure requires v^2 > T/U.
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
            ) = boost(
                state,
                v,
            )

            if (
                pressure <= 0.0
                or
                active <= 0.0
                or
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

            radius_phi_unit = (
                base_phi
                /
                k_phi_lab
            )

            radius_sigma_unit = (
                base_sigma
                /
                k_sigma_lab
            )

            if (
                radius_phi_unit <= 0.0
                or
                radius_sigma_unit <= 0.0
            ):
                continue

            if (
                abs(
                    radius_phi_unit
                    -
                    radius_sigma_unit
                )
                /
                max(
                    radius_phi_unit,
                    radius_sigma_unit,
                )
                >
                2.0e-12
            ):
                continue

            radius_unit = (
                0.5
                *
                (
                    radius_phi_unit
                    +
                    radius_sigma_unit
                )
            )

            # Mechanical balance seeks
            #
            #     pressure = sigma_W R
            #
            # and R is an integer multiple of radius_unit.
            multiplier_target = (
                pressure
                /
                (
                    wall.tension
                    *
                    radius_unit
                )
            )

            multiplier_center = int(
                round(
                    multiplier_target
                )
            )

            for multiplier in range(
                max(
                    1,
                    multiplier_center
                    -
                    2,
                ),
                max(
                    1,
                    multiplier_center
                    +
                    2,
                )
                +
                1,
            ):

                radius = (
                    multiplier
                    *
                    radius_unit
                )

                if (
                    radius
                    /
                    wall.width90
                    <
                    MIN_R_OVER_WALL90
                ):
                    continue

                wall_load = (
                    wall.tension
                    *
                    radius
                )

                balance_rel = (
                    abs(
                        pressure
                        -
                        wall_load
                    )
                    /
                    max(
                        abs(
                            pressure
                        ),
                        abs(
                            wall_load
                        ),
                        1.0e-30,
                    )
                )

                if (
                    balance_rel
                    >
                    BALANCE_REL_TOL
                ):
                    continue

                candidate = Candidate(
                    base_phi=base_phi,

                    base_sigma=base_sigma,

                    mult=multiplier,

                    n_phi=(
                        base_phi
                        *
                        multiplier
                    ),

                    n_sigma=(
                        base_sigma
                        *
                        multiplier
                    ),

                    v=v,

                    gamma=gamma,

                    radius=radius,

                    balance_rel=balance_rel,

                    energy_line=energy,

                    pressure_line=pressure,

                    momentum_line=momentum,

                    active_line=active,

                    omega_phi_lab=omega_phi_lab,

                    k_phi_lab=k_phi_lab,

                    omega_sigma_lab=omega_sigma_lab,

                    k_sigma_lab=k_sigma_lab,
                )

                # The finite spherical payload must have its entire lower
                # surface at least five measured wall widths above z=0.
                x_floor = (
                    MIN_PAYLOAD_BOTTOM_OVER_WALL90
                    *
                    wall.width90
                    /
                    (
                        (
                            1.0
                            -
                            PAYLOAD_RADIUS_OVER_H
                        )
                        *
                        radius
                    )
                )

                x_low = max(
                    X_MIN,
                    x_floor,
                )

                if x_low >= X_MAX:
                    continue

                def objective(
                    x,
                ):
                    value = gravity_and_c(
                        wall,
                        candidate,
                        float(
                            x
                        ),
                        True,
                    )[
                        1
                    ]

                    if math.isfinite(
                        value
                    ):
                        return value

                    return 1.0e300

                result = minimize_scalar(
                    objective,

                    bounds=(
                        x_low,
                        X_MAX,
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

                candidate.f_nominal = (
                    gravity_and_c(
                        wall,
                        candidate,
                        candidate.x,
                        False,
                    )[
                        0
                    ]
                )

                (
                    candidate.f_worst,
                    _c_worst,

                    candidate.active_mass_per_r,

                    candidate.clearance,

                    _wall_outward,
                    _rim_inward,
                ) = gravity_and_c(
                    wall,
                    candidate,
                    candidate.x,
                    True,
                )

                if (
                    candidate.f_worst <= 0.0
                    or
                    candidate.active_mass_per_r <= 0.0
                ):
                    continue

                key = (
                    candidate.n_phi,
                    candidate.n_sigma,
                )

                previous = found.get(
                    key
                )

                if (
                    previous is None
                    or
                    candidate.c_worst
                    <
                    previous.c_worst
                ):
                    found[
                        key
                    ] = candidate

    return list(
        found.values()
    )


def continuous_floor(
    state: State,
    wall: Wall,
    vmax: float,
):
    """Diagnostic continuous-v lower bound with no integer restriction.

    This is not promotion evidence.

    It answers whether the broad source-level mechanism is already impossible
    before integer quantization is applied.
    """

    transverse_speed = math.sqrt(
        state.T
        /
        state.U
    )

    best = (
        math.inf,
        math.nan,
        math.nan,
    )

    if vmax <= transverse_speed:
        return best

    for index in range(
        700
    ):

        v = (
            transverse_speed

            +

            (
                vmax
                -
                transverse_speed
            )
            *
            (
                index
                +
                1
            )
            /
            700.0
        )

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
        ) = boost(
            state,
            v,
        )

        if pressure <= 0.0:
            continue

        radius = (
            pressure
            /
            wall.tension
        )

        if (
            radius
            /
            wall.width90
            <
            MIN_R_OVER_WALL90
        ):
            continue

        fake = Candidate(
            base_phi=0,
            base_sigma=0,

            mult=0,

            n_phi=0,
            n_sigma=0,

            v=v,
            gamma=gamma,

            radius=radius,

            balance_rel=0.0,

            energy_line=energy,

            pressure_line=pressure,

            momentum_line=momentum,

            active_line=active,

            omega_phi_lab=omega_phi_lab,

            k_phi_lab=k_phi_lab,

            omega_sigma_lab=omega_sigma_lab,

            k_sigma_lab=k_sigma_lab,
        )

        x_floor = (
            MIN_PAYLOAD_BOTTOM_OVER_WALL90
            *
            wall.width90
            /
            (
                (
                    1.0
                    -
                    PAYLOAD_RADIUS_OVER_H
                )
                *
                radius
            )
        )

        x_low = max(
            X_MIN,
            x_floor,
        )

        if x_low >= X_MAX:
            continue

        def objective(
            x,
        ):
            value = gravity_and_c(
                wall,
                fake,
                float(
                    x
                ),
                True,
            )[
                1
            ]

            if math.isfinite(
                value
            ):
                return value

            return 1.0e300

        result = minimize_scalar(
            objective,

            bounds=(
                x_low,
                X_MAX,
            ),

            method="bounded",
        )

        if (
            result.success
            and
            float(
                result.fun
            )
            <
            1.0e299
            and
            float(
                result.fun
            )
            <
            best[
                0
            ]
        ):
            best = (
                float(
                    result.fun
                ),

                float(
                    v
                ),

                float(
                    result.x
                ),
            )

    return best


def main() -> None:
    """Run the stationary integer-wall-balance and gravity scout."""

    print(
        "=== 018B-0F — STATIONARY TWO-CURRENT INTEGER "
        "WALL-BALANCE + GRAVITY SCOUT ==="
    )

    state, wall = (
        load_inputs()
    )

    ct2 = (
        state.T
        /
        state.U
    )

    print(
        "\n=== INPUT / SIGN PREFLIGHT ==="
    )

    print(
        f"U={state.U:+.15e}"
    )

    print(
        f"T={state.T:+.15e}"
    )

    print(
        "CT2=T_OVER_U="
        f"{ct2:+.15e}"
    )

    print(
        "CT="
        f"{math.sqrt(ct2):+.15e}"
    )

    print(
        "WALL_TENSION="
        f"{wall.tension:+.15e}"
    )

    print(
        "WALL_ACTIVE_SOURCE="
        f"{wall.active:+.15e}"
    )

    print(
        "WALL_WIDTH90="
        f"{wall.width90:+.15e}"
    )

    print(
        "RIM_CORE_WIDTH_PROXY="
        f"{wall.core_width:+.15e}"
    )

    print(
        "POSITIVE_PRESSURE_REQUIRES_V2_GT_T_OVER_U=YES"
    )

    # ------------------------------------------------------------------
    # First ask the continuous problem. This reveals whether the broad
    # stationary support/gravity mechanism exists before integer closure.
    # ------------------------------------------------------------------

    print(
        "\n=== CONTINUOUS BOUND — DIAGNOSTIC ONLY ==="
    )

    for vmax in (
        0.98,
        0.99,
        0.995,
        0.999,
    ):

        (
            c_min,
            v_min,
            x_min,
        ) = continuous_floor(
            state,
            wall,
            vmax,
        )

        print(
            f"BOOST_CEILING={vmax:.6f} "
            f"ADVERSE_ENVELOPE_PROJECTED_C_MIN="
            f"{c_min:.12e} "
            f"V_AT_MIN="
            f"{v_min:+.12e} "
            f"X_AT_MIN="
            f"{x_min:.12e}"
        )

    print(
        "CONTINUOUS_BOUND_PROMOTION_EVIDENCE=NO"
    )

    # ------------------------------------------------------------------
    # Exact two-current integer loop.
    # ------------------------------------------------------------------

    print(
        "\n=== EXACT INTEGER SEARCH ==="
    )

    candidates = enumerate_candidates(
        state,
        wall,
    )

    print(
        f"BASE_WINDING_MAX="
        f"{BASE_WINDING_MAX}"
    )

    print(
        f"MAX_ABS_V="
        f"{MAX_ABS_V:.6f}"
    )

    print(
        f"BALANCE_REL_TOL="
        f"{BALANCE_REL_TOL:.3e}"
    )

    print(
        "EXACT_INTEGER_DEEP_INTERIOR_PASSERS="
        f"{len(candidates)}"
    )

    if not candidates:

        print(
            "018B0F_STATIONARY_INTEGER_WALL_BALANCE_GRAVITY_SCOUT="
            "RED"
        )

        print(
            "NEXT="
            "CLASSIFY_FAILURE_BEFORE_2D_JUNCTION"
        )

        print(
            "CURRENT_HEURISTIC="
            "APPROXIMATELY_66_PERCENT_NOT_A_PROBABILITY"
        )

        print(
            "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
        )

        return

    # Robustness-first policies were already applied.
    # Among states passing those hard gates, select the lowest adverse C.
    selected = min(
        candidates,
        key=lambda item:
            item.c_worst,
    )

    (
        phi_rel,
        sigma_rel,
        trace_rel,
        determinant_rel,
        radius_rel,
    ) = invariant_errors(
        state,
        selected,
    )

    print(
        "\n=== SELECTED CANDIDATE ==="
    )

    print(
        f"BASE_N_PHI="
        f"{selected.base_phi}"
    )

    print(
        f"BASE_N_SIGMA="
        f"{selected.base_sigma}"
    )

    print(
        f"COMMON_MULTIPLIER="
        f"{selected.mult}"
    )

    print(
        f"N_PHI="
        f"{selected.n_phi}"
    )

    print(
        f"N_SIGMA="
        f"{selected.n_sigma}"
    )

    print(
        f"BOOST_V="
        f"{selected.v:+.15e}"
    )

    print(
        f"BOOST_GAMMA="
        f"{selected.gamma:.15e}"
    )

    print(
        "LIGHTCONE_MARGIN_1_MINUS_ABS_V="
        f"{1.0 - abs(selected.v):.15e}"
    )

    print(
        f"RADIUS="
        f"{selected.radius:.15e}"
    )

    print(
        "R_OVER_WALL90="
        f"{selected.radius / wall.width90:.15e}"
    )

    print(
        "LAB_ENERGY_LINE="
        f"{selected.energy_line:+.15e}"
    )

    print(
        "LAB_P_PARALLEL="
        f"{selected.pressure_line:+.15e}"
    )

    print(
        "LAB_MOMENTUM_LINE="
        f"{selected.momentum_line:+.15e}"
    )

    print(
        "LAB_ACTIVE_LINE="
        f"{selected.active_line:+.15e}"
    )

    print(
        "WALL_LOAD_SIGMA_R="
        f"{wall.tension * selected.radius:+.15e}"
    )

    print(
        "WALL_BALANCE_RELERR="
        f"{selected.balance_rel:.15e}"
    )

    print(
        "SELECTED_H_OVER_R="
        f"{selected.x:.15e}"
    )

    print(
        "PAYLOAD_BOTTOM_OVER_WALL90="
        f"{selected.clearance:.15e}"
    )

    # ------------------------------------------------------------------
    # Independent algebraic reconstruction.
    # ------------------------------------------------------------------

    print(
        "\n=== EXACTNESS / LORENTZ CHECKS ==="
    )

    print(
        "PHI_PHASE_INVARIANT_RELERR="
        f"{phi_rel:.15e}"
    )

    print(
        "SIGMA_PHASE_INVARIANT_RELERR="
        f"{sigma_rel:.15e}"
    )

    print(
        "STRESS_TRACE_INVARIANT_RELERR="
        f"{trace_rel:.15e}"
    )

    print(
        "STRESS_DETERMINANT_INVARIANT_RELERR="
        f"{determinant_rel:.15e}"
    )

    print(
        "DUAL_INTEGER_RADIUS_RELERR="
        f"{radius_rel:.15e}"
    )

    invariants_pass = (
        max(
            phi_rel,
            sigma_rel,
            trace_rel,
            determinant_rel,
            radius_rel,
        )
        <
        2.0e-12
    )

    print(
        "BOOST_AND_INTEGER_INVARIANTS="
        +
        (
            "PASS"
            if invariants_pass
            else "FAIL"
        )
    )

    nominal = gravity_and_c(
        wall,
        selected,
        selected.x,
        False,
    )

    adverse = gravity_and_c(
        wall,
        selected,
        selected.x,
        True,
    )

    print(
        "\n=== GRAVITY ==="
    )

    print(
        "NOMINAL_FINITE_PAYLOAD_OUTWARD_FACTOR="
        f"{nominal[0]:+.15e}"
    )

    print(
        "ADVERSE_FINITE_PAYLOAD_OUTWARD_FACTOR="
        f"{adverse[0]:+.15e}"
    )

    print(
        "ADVERSE_TOTAL_ACTIVE_MASS_PER_R="
        f"{adverse[2]:+.15e}"
    )

    print(
        "ADVERSE_WALL_OUTWARD_FACTOR="
        f"{adverse[4]:+.15e}"
    )

    print(
        "ADVERSE_RIM_INWARD_FACTOR="
        f"{adverse[5]:+.15e}"
    )

    print(
        "PROJECTED_C_EFF_ADVERSE="
        f"{adverse[1]:.15e}"
    )

    print(
        "FINITE_PAYLOAD_OUTWARD="
        +
        (
            "PASS"
            if adverse[0] > 0.0
            else "FAIL"
        )
    )

    print(
        "POSITIVE_TOTAL_ACTIVE_MASS="
        +
        (
            "PASS"
            if adverse[2] > 0.0
            else "FAIL"
        )
    )

    print(
        "ADVERSE_FINITE_SIZE_GRAVITY_STRESS_TEST="
        +
        (
            "PASS"
            if adverse[0] > 0.0
            else "FAIL"
        )
    )

    # ------------------------------------------------------------------
    # User-requested blind wildcard diagnostic.
    #
    # These values do not contribute to selection or promotion.
    # ------------------------------------------------------------------

    print(
        "\n=== BLIND WILDCARD HEIGHT DIAGNOSTIC — NOT EVIDENCE ==="
    )

    for factor in WILDCARD_X_FACTORS:

        x_value = (
            selected.x
            *
            factor
        )

        if (
            x_value <= 0.0
            or
            x_value >= 1.0
        ):

            print(
                f"WILDCARD_X_FACTOR={factor:.6f} "
                "STATUS=OUTSIDE_DOMAIN"
            )

            continue

        diagnostic = gravity_and_c(
            wall,
            selected,
            x_value,
            True,
        )

        print(
            f"WILDCARD_X_FACTOR="
            f"{factor:.6f} "

            f"X="
            f"{x_value:.9e} "

            f"F_OUT="
            f"{diagnostic[0]:+.9e} "

            f"OUTWARD="
            f"{'YES' if diagnostic[0] > 0.0 else 'NO'}"
        )

    print(
        "WILDCARD_VALUES_USED_AS_EVIDENCE=NO"
    )

    # ------------------------------------------------------------------
    # Scaling diagnostic.
    #
    # This is projected only because the new 2D junction and curved
    # microscopic ring are absent.
    # ------------------------------------------------------------------

    improvement = (
        VALIDATED_C
        /
        adverse[
            1
        ]
    )

    projected_mass = (
        VALIDATED_MASS_1G_1M
        /
        improvement
    )

    projected_energy = (
        VALIDATED_ENERGY_1G_1M
        /
        improvement
    )

    print(
        "\n=== ENERGY LEDGER ==="
    )

    print(
        "ENERGY_MODEL_STATUS="
        "PROJECTED_PREFLIGHT_NOT_VALIDATED"
    )

    print(
        "CURRENT_VALIDATED_C="
        f"{VALIDATED_C:.15e}"
    )

    print(
        "PROJECTED_SCOUT_C="
        f"{adverse[1]:.15e}"
    )

    print(
        "PROJECTED_IMPROVEMENT_FACTOR="
        f"{improvement:.15e}"
    )

    print(
        "PROJECTED_ONE_G_ONE_M_MASS_KG="
        f"{projected_mass:.15e}"
    )

    print(
        "PROJECTED_ONE_G_ONE_M_ENERGY_J="
        f"{projected_energy:.15e}"
    )

    print(
        "NEW_TWO_CURRENT_2D_JUNCTION_INCLUDED=NO"
    )

    print(
        "CURVED_MICROSCOPIC_RING_INCLUDED=NO"
    )

    print(
        "FULL_LOOP_STABILITY_INCLUDED=NO"
    )

    print(
        "FRAME_DRAGGING_INCLUDED=NO"
    )

    # ------------------------------------------------------------------
    # Decision.
    # ------------------------------------------------------------------

    green = (
        invariants_pass

        and
        selected.balance_rel
        <=
        BALANCE_REL_TOL

        and
        abs(
            selected.v
        )
        <=
        MAX_ABS_V

        and
        selected.radius
        /
        wall.width90
        >=
        MIN_R_OVER_WALL90

        and
        selected.clearance
        >=
        MIN_PAYLOAD_BOTTOM_OVER_WALL90

        and
        adverse[
            0
        ]
        >
        0.0

        and
        adverse[
            2
        ]
        >
        0.0

        and
        math.isfinite(
            adverse[
                1
            ]
        )
    )

    print(
        "\n=== DECISION ==="
    )

    if green:

        print(
            "018B0F_STATIONARY_INTEGER_WALL_BALANCE_GRAVITY_SCOUT="
            "GREEN"
        )

        print(
            "STATIONARY_TWO_CURRENT_POSITIVE_PPAR_RIM_CANDIDATE="
            "YES"
        )

        print(
            "EXACT_DUAL_INTEGER_LOOP_CLOSURE="
            "PASS"
        )

        print(
            "NEAR_EXACT_WALL_BALANCE="
            "PASS"
        )

        print(
            "SOURCE_LEVEL_FINITE_PAYLOAD_REPULSION="
            "PASS"
        )

        print(
            "PROJECTED_SCALING_IMPROVEMENT="
            "YES_BUT_NOT_VALIDATED"
        )

        print(
            "NEXT="
            "018B0G_NEW_TWO_CURRENT_2D_STRING_WALL_"
            "JUNCTION_REVALIDATION"
        )

        print(
            "NEXT_AFTER_018B0G_GREEN="
            "018B0H_COMPLETE_SOURCE_GRAVITY_REVALIDATION_"
            "THEN_TRUE_018B_GLOBAL_TOROIDAL_SOLVE"
        )

    else:

        print(
            "018B0F_STATIONARY_INTEGER_WALL_BALANCE_GRAVITY_SCOUT="
            "RED"
        )

        print(
            "NEXT="
            "CLASSIFY_FAILED_GATE_BEFORE_2D_JUNCTION"
        )

    print(
        "CURRENT_HEURISTIC="
        "APPROXIMATELY_66_PERCENT_NOT_A_PROBABILITY"
    )

    print(
        "HEURISTIC_INCREASE_FROM_THIS_GATE="
        "NO_SOURCE_LEVEL_SCOUT_ONLY"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )

    print(
        "NEW_PHYSICS_DISCOVERY=NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_018B0F_STATIONARY_TWO_CURRENT_"
        "INTEGER_WALL_BALANCE_GRAVITY_SCOUT"
    )


if __name__ == "__main__":
    main()
