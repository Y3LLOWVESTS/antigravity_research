r"""016H — explicit canonical-field outward-gravity variational gate.

PURPOSE
-------
Test the most important escape identified by Simulation 016G:

    STOP demanding exact reproduction of the engineered 006D stress tensor.

Instead, specify an explicit healthy local relativistic field model, allow the
fields to choose their own stress distribution through fixed-charge energy
minimization, and directly test the physical quantity of interest:

    Does the resulting stress-energy produce an outward gravitational
    acceleration in static linearized general relativity?

This is intended to be the final scientific gate before the current research
slice is documented.

SCIENTIFIC CONTEXT
------------------
The current research chain established:

006D:
    A finite, nonsingular, positive-energy, locally conserved,
    energy-condition-compatible stress tensor produces local outward gravity
    in static linearized GR.

016A:
    Thickening the source drastically reduces peak stresses with only a
    modest gravitational-efficiency penalty.

016B:
    The fixed-charge Derrick capacity and local gauge window survive
    thickening.

016C:
    The simplest global one/two electrostatic realization is obstructed.

016D:
    Smooth noncompact tails remove the exact compact-boundary derivative
    divergence.

016E:
    An exponential tail fails the minimum single gauged-winding finite-energy
    asymptotic requirement, while a C2 power-law tail passes that kinematic
    requirement.

016F:
    Temporal charge and winding can coexist kinematically, with a widened
    transition reducing the required gauge mismatch from approximately 130
    to approximately 9.6.

016G:
    The exact m=2 power-law target is incompatible with the asymptotic
    Euler-Lagrange equation of the minimum asymptotically decoupled canonical
    winding field with a stable vacuum.

Therefore the correct next move is not another exact-T-matching exercise.

016H performs an observable-first field-model test.

MODEL
-----
Use a Friedberg-Lee-Sirlin-inspired local scalar theory containing:

1. one real symmetry-breaking scalar X;

2. two equal complex fields Phi_plus and Phi_minus carrying equal temporal
   frequency and opposite azimuthal winding.

The dimensionless Lagrangian convention underlying the energy functional is

    L
        =
        1/2 d_mu X d^mu X
        +
        sum_a d_mu Phi_a^* d^mu Phi_a
        -
        V.

The potential is

    V
        =
        mu/4 (1-X^2)^2
        +
        X^2 (
            |Phi_plus|^2
            +
            |Phi_minus|^2
        ).

Every term in V is nonnegative.

The vacuum is

    X = +/-1,
    Phi_plus = Phi_minus = 0.

The complex fields become light where X approaches zero, allowing charge and
current to localize in a symmetry-breaking wall region.

This is inspired by the Friedberg-Lee-Sirlin mechanism and by
current-carrying/vorton field constructions, but the counter-winding doubled
ansatz used here is a project-defined preflight model.

COUNTER-WINDING ANSATZ
----------------------
Take

    Phi_plus
        =
        Y(r,z) exp[i(omega t + n phi)]

and

    Phi_minus
        =
        Y(r,z) exp[i(omega t - n phi)].

Their angular momentum densities are equal and opposite.

Therefore

    T_tphi,total = 0.

The total stress-energy is stationary and has no net momentum density from
the counter-winding pair.

TRIAL FIELDS
------------
Allow the real wall-like field and charged winding fields to have independent
radial and vertical widths:

    X
        =
        1
        -
        A exp[
            -1/2 (
                r^2/R_X^2
                +
                z^2/Z_X^2
            )
        ].

The amplitude A is allowed over

    0 <= A <= 2.

A approximately 1 gives a core where X approaches zero.

A approximately 2 gives a transition from the +1 vacuum outside toward the
-1 vacuum in the central region, producing a domain-wall-like shell.

For each counter-winding complex field,

    Y
        =
        B (r/R_Y)^n
        exp[
            -1/2 (
                r^2/R_Y^2
                +
                z^2/Z_Y^2
            )
        ].

The r^n factor makes the winding field regular on the symmetry axis.

Allowing R_X, Z_X, R_Y, and Z_Y to vary independently lets the energy
minimization spatially separate wall tension from charge/current support
instead of forcing them into the same profile.

FIXED CHARGE
------------
For the normalization used here, the total Noether charge of the
counter-winding pair is

    Q
        =
        4 omega
        integral Y^2 dV.

Thus omega is eliminated exactly:

    omega
        =
        Q
        /
        [
            4 integral Y^2 dV
        ].

The variational problem therefore minimizes E at fixed Q.

ENERGY
------
The energy density is

    rho
        =
        1/2 |grad X|^2
        +
        2 [
            omega^2 Y^2
            +
            |grad Y|^2
            +
            n^2 Y^2/r^2
        ]
        +
        V.

All contributions are nonnegative.

The free-particle threshold in the chosen dimensionless units is

    E/Q = 1.

Therefore

    E/Q < 1

is the basic variational binding criterion.

ACTIVE GRAVITATIONAL SOURCE
---------------------------
In static linearized GR with metric signature (-,+,+,+), the Newtonian-like
potential obeys

    nabla^2 Phi
        =
        4 pi G (
            rho
            +
            p_r
            +
            p_phi
            +
            p_z
        )
        / c^2.

Define

    S
        =
        rho
        +
        p_r
        +
        p_phi
        +
        p_z.

For this explicit field model, spatial-gradient terms cancel from the trace
combination, giving the exact identity

    S
        =
        8 omega^2 Y^2
        -
        2 V.

This is extremely important.

The positive scalar potential provides the locally repulsive active-stress
contribution.

Temporal charge provides a positive attractive active contribution.

The calculation therefore tests the actual competition between wall tension
and charge stabilization rather than prescribing the desired answer.

LINEARIZED-GR FORCE
-------------------
For an observation point on the positive symmetry axis at z=h,

    a_z
        proportional to
        -
        integral
            S(r,z)
            (h-z)
            /
            [
                r^2
                +
                (h-z)^2
            ]^(3/2)
            dV.

Repository sign convention:

    a_z > 0
        means outward, away from the source plane;

    a_z < 0
        means inward attraction.

No arbitrary stress target is used in this calculation.

VARIATIONAL STATIONARITY
------------------------
For each:

    mu,
    Q,
    n,

the energy is minimized over

    R_X,
    Z_X,
    R_Y,
    Z_Y,
    B,
    A.

All energy integrals entering the optimizer are evaluated analytically for
the Gaussian family.

The final stress tensor and gravitational field are then recomputed by
independent Gauss-Legendre volume quadrature.

A genuine field solution would have integrated Laue balance

    integral (
        p_r
        +
        p_phi
        +
        p_z
    ) dV
        =
        0.

Equivalently,

    integral S dV
        =
        E.

For a variational stationary configuration, approximate satisfaction of this
identity is a strong internal consistency check.

It is not a substitute for solving the full Euler-Lagrange PDEs.

EXTERIOR DEFINITION
-------------------
The Gaussian fields have infinite mathematical tails.

Define the characteristic vertical width as

    Z_char
        =
        max(
            Z_X,
            Z_Y
        ).

At

    h = 3 Z_char,

the unsquared Gaussian amplitude associated with the widest vertical profile
has fallen to

    exp(-9/2)
        approximately
        0.0111.

The "clean exterior" scan therefore begins at

    h >= 3 Z_char.

A separate near-field scan begins at

    h >= 0.10 Z_char.

This deliberately distinguishes:

    negative active density somewhere;

    local outward acceleration inside/through the field configuration;

    clean-exterior operational repulsion.

Those are not equivalent accomplishments.

OPTIMISTIC NATURE OF THIS GATE
------------------------------
The gauge field is deliberately omitted.

This makes the test optimistic for obtaining gravitational repulsion because
ordinary Maxwell energy contributes positively to the active gravitational
source.

A negative result therefore argues against spending the next research slice
immediately on a much more expensive gauged PDE solve of the same basic
architecture.

However, it is not a theorem against gauged models, because gauge coupling
can alter the equilibrium field profiles.

SCAN
----
Use:

    mu:
        0.1
        0.3
        1.0
        3.0

    total charge Q:
        1000
        3000
        10000
        30000

    winding n:
        1
        2
        3
        4
        5

This gives 80 explicit model/charge/winding cases.

Only localized bound variational states are promoted to the gravitational
decision set.

VALIDATION
----------
For each promoted state:

- verify E/Q < 1;
- compare analytic energy against independent volume quadrature;
- verify the active-source identity pointwise;
- measure integrated pressure-trace residual;
- verify positive total active mass;
- search the near field for outward acceleration;
- search the clean exterior for outward acceleration.

The best exterior candidate is independently recomputed at three quadrature
orders.

INTERPRETATION
--------------
A positive exterior result would be a major change in project status:

    an explicit healthy local canonical field model,
    at variational stationary level,
    naturally produces the same operational sign sought by 006D.

That would justify a full two-dimensional Euler-Lagrange solve next session.

A negative result would also be highly informative.

If bound stationary configurations contain substantial negative active
density but remain gravitationally attractive throughout the tested exterior,
then the problem is not merely generating negative pressure.

It is arranging the positive and negative active source spatially while
maintaining genuine field equilibrium.

That would sharply demote generic FLS/Q-ball realization and favor either:

- a more explicitly separated drum-vorton/domain-wall-plus-rim architecture;
- a different canonical field model;
- or reranking against the surviving non-GR branches.

LIMITATIONS
-----------
016H does NOT establish:

- an exact Euler-Lagrange field solution;
- full dynamic stability;
- a gauged solution;
- nonlinear Einstein-matter equilibrium;
- a material realization;
- experimental accessibility;
- practical energy requirements;
- practical antigravity.

The Gaussian variational family is deliberately more flexible than the
previous fixed stress targets but is still a finite-dimensional ansatz.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_EXPLICIT_CANONICAL_FIELD_VARIATIONAL_GRAVITY_GATE
"""

from __future__ import annotations

import math

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.optimize import minimize


PI_3_OVER_2 = math.pi ** 1.5

MU_VALUES = (
    0.1,
    0.3,
    1.0,
    3.0,
)

CHARGES = (
    1000.0,
    3000.0,
    10000.0,
    30000.0,
)

WINDINGS = (
    1,
    2,
    3,
    4,
    5,
)

FREE_PARTICLE_THRESHOLD = 1.0

BOUND_E_OVER_Q_MAX = 0.999

PROFILE_AMPLITUDE_MIN = 0.05

SOURCE_TAIL_AMPLITUDE_AT_3Z = math.exp(
    -4.5
)


def overlap_y_with_x_gaussian(
    winding: int,
    amplitude_y: float,
    radius_y: float,
    height_y: float,
    radius_x: float,
    height_x: float,
    x_gaussian_power: int,
) -> float:
    """Return integral of Y^2 times a power of the X Gaussian envelope.

    The complex-field amplitude is

        Y
            =
            B (r/R_Y)^n
            exp[
                -1/2 (
                    r^2/R_Y^2
                    +
                    z^2/Z_Y^2
                )
            ].

    The real-field Gaussian envelope is

        e_X
            =
            exp[
                -1/2 (
                    r^2/R_X^2
                    +
                    z^2/Z_X^2
                )
            ].

    This function analytically evaluates

        integral Y^2 e_X^k dV.
    """

    radial_coefficient = (
        1.0
        / (
            radius_y
            * radius_y
        )
        +
        x_gaussian_power
        / (
            2.0
            * radius_x
            * radius_x
        )
    )

    vertical_coefficient = (
        1.0
        / (
            height_y
            * height_y
        )
        +
        x_gaussian_power
        / (
            2.0
            * height_x
            * height_x
        )
    )

    return (
        amplitude_y
        * amplitude_y
        * PI_3_OVER_2
        * math.factorial(
            winding
        )
        / (
            radius_y
            ** (
                2
                * winding
            )
            * radial_coefficient
            ** (
                winding
                +
                1
            )
            * math.sqrt(
                vertical_coefficient
            )
        )
    )


def x_gaussian_integral(
    radius_x: float,
    height_x: float,
    power: int,
) -> float:
    """Return integral of exp[-power*q/2] over three-space."""

    return (
        (
            2.0
            * math.pi
            / power
        )
        ** 1.5
        * radius_x
        * radius_x
        * height_x
    )


def unpack(
    parameters: np.ndarray,
) -> tuple[
    float,
    float,
    float,
    float,
    float,
    float,
]:
    """Convert optimizer coordinates to physical variational parameters."""

    (
        log_radius_x,
        log_height_x,
        log_radius_y,
        log_height_y,
        log_amplitude_y,
        amplitude_x,
    ) = parameters

    return (
        math.exp(
            log_radius_x
        ),
        math.exp(
            log_height_x
        ),
        math.exp(
            log_radius_y
        ),
        math.exp(
            log_height_y
        ),
        math.exp(
            log_amplitude_y
        ),
        amplitude_x,
    )


def analytic_energy(
    parameters: np.ndarray,
    charge: float,
    winding: int,
    mu: float,
) -> float:
    """Return exact variational energy in the Gaussian ansatz."""

    (
        radius_x,
        height_x,
        radius_y,
        height_y,
        amplitude_y,
        amplitude_x,
    ) = unpack(
        parameters
    )

    y2 = overlap_y_with_x_gaussian(
        winding,
        amplitude_y,
        radius_y,
        height_y,
        radius_x,
        height_x,
        0,
    )

    if (
        y2
        <= 0.0
        or not math.isfinite(
            y2
        )
    ):
        return 1.0e100

    temporal_energy = (
        charge
        * charge
        / (
            8.0
            * y2
        )
    )

    x_gradient_energy = (
        0.5
        * amplitude_x
        * amplitude_x
        * PI_3_OVER_2
        * (
            height_x
            +
            0.5
            * radius_x
            * radius_x
            / height_x
        )
    )

    complex_normalization = (
        PI_3_OVER_2
        * math.factorial(
            winding
        )
    )

    y_spatial_energy = (
        2.0
        * complex_normalization
        * amplitude_y
        * amplitude_y
        * (
            (
                winding
                +
                1.0
            )
            * height_y
            +
            0.5
            * radius_y
            * radius_y
            / height_y
        )
    )

    j2 = x_gaussian_integral(
        radius_x,
        height_x,
        2,
    )

    j3 = x_gaussian_integral(
        radius_x,
        height_x,
        3,
    )

    j4 = x_gaussian_integral(
        radius_x,
        height_x,
        4,
    )

    x_potential_energy = (
        mu
        / 4.0
        * (
            4.0
            * amplitude_x
            * amplitude_x
            * j2
            -
            4.0
            * amplitude_x
            ** 3
            * j3
            +
            amplitude_x
            ** 4
            * j4
        )
    )

    y2_x1 = overlap_y_with_x_gaussian(
        winding,
        amplitude_y,
        radius_y,
        height_y,
        radius_x,
        height_x,
        1,
    )

    y2_x2 = overlap_y_with_x_gaussian(
        winding,
        amplitude_y,
        radius_y,
        height_y,
        radius_x,
        height_x,
        2,
    )

    coupling_energy = (
        2.0
        * (
            y2
            -
            2.0
            * amplitude_x
            * y2_x1
            +
            amplitude_x
            * amplitude_x
            * y2_x2
        )
    )

    return float(
        temporal_energy
        +
        x_gradient_energy
        +
        y_spatial_energy
        +
        x_potential_energy
        +
        coupling_energy
    )


def optimize_case(
    charge: float,
    winding: int,
    mu: float,
):
    """Minimize energy at fixed charge from multiple independent starts."""

    bounds = (
        (
            math.log(
                0.10
            ),
            math.log(
                150.0
            ),
        ),
        (
            math.log(
                0.10
            ),
            math.log(
                150.0
            ),
        ),
        (
            math.log(
                0.10
            ),
            math.log(
                150.0
            ),
        ),
        (
            math.log(
                0.10
            ),
            math.log(
                150.0
            ),
        ),
        (
            math.log(
                0.005
            ),
            math.log(
                50.0
            ),
        ),
        (
            0.0,
            2.0,
        ),
    )

    starting_points = (
        (
            3.0,
            1.0,
            3.0,
            1.0,
            1.0,
            1.0,
        ),
        (
            4.0,
            1.5,
            6.0,
            1.5,
            1.0,
            2.0,
        ),
        (
            6.0,
            2.0,
            9.0,
            2.0,
            0.5,
            2.0,
        ),
        (
            4.0,
            3.0,
            6.0,
            3.0,
            1.5,
            1.5,
        ),
        (
            10.0,
            3.0,
            12.0,
            2.0,
            0.3,
            2.0,
        ),
    )

    best = None

    for (
        radius_x,
        height_x,
        radius_y,
        height_y,
        amplitude_y,
        amplitude_x,
    ) in starting_points:
        initial = np.array(
            [
                math.log(
                    radius_x
                ),
                math.log(
                    height_x
                ),
                math.log(
                    radius_y
                ),
                math.log(
                    height_y
                ),
                math.log(
                    amplitude_y
                ),
                amplitude_x,
            ],
            dtype=float,
        )

        result = minimize(
            analytic_energy,
            initial,
            args=(
                charge,
                winding,
                mu,
            ),
            method="L-BFGS-B",
            bounds=bounds,
            options={
                "maxiter":
                    1500,
                "ftol":
                    1.0e-13,
                "gtol":
                    1.0e-9,
                "maxls":
                    40,
            },
        )

        if (
            best is None
            or result.fun
            <
            best.fun
        ):
            best = result

    return best


def quadrature_grid(
    radius_limit: float,
    height_limit: float,
    order: int,
) -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
]:
    """Return cylindrical Gauss-Legendre volume grid."""

    nodes_r, weights_r = leggauss(
        order
    )

    nodes_z, weights_z = leggauss(
        order
    )

    radius = (
        0.5
        * radius_limit
        * (
            nodes_r
            +
            1.0
        )
    )

    radial_weights = (
        0.5
        * radius_limit
        * weights_r
    )

    z_value = (
        height_limit
        * nodes_z
    )

    vertical_weights = (
        height_limit
        * weights_z
    )

    rr, zz = np.meshgrid(
        radius,
        z_value,
        indexing="ij",
    )

    volume_weights = (
        2.0
        * math.pi
        * rr
        * radial_weights[
            :,
            None
        ]
        * vertical_weights[
            None,
            :
        ]
    )

    return (
        rr,
        zz,
        volume_weights,
    )


def field_arrays(
    parameters: np.ndarray,
    charge: float,
    winding: int,
    mu: float,
    order: int,
) -> dict[str, object]:
    """Reconstruct stress-energy independently by volume quadrature."""

    (
        radius_x,
        height_x,
        radius_y,
        height_y,
        amplitude_y,
        amplitude_x,
    ) = unpack(
        parameters
    )

    radius_limit = (
        8.0
        * max(
            radius_x,
            radius_y,
        )
    )

    height_limit = (
        8.0
        * max(
            height_x,
            height_y,
        )
    )

    (
        rr,
        zz,
        volume_weights,
    ) = quadrature_grid(
        radius_limit,
        height_limit,
        order,
    )

    x_envelope = np.exp(
        -0.5
        * (
            (
                rr
                / radius_x
            )
            ** 2
            +
            (
                zz
                / height_x
            )
            ** 2
        )
    )

    field_x = (
        1.0
        -
        amplitude_x
        * x_envelope
    )

    y_envelope = np.exp(
        -0.5
        * (
            (
                rr
                / radius_y
            )
            ** 2
            +
            (
                zz
                / height_y
            )
            ** 2
        )
    )

    field_y = (
        amplitude_y
        * (
            rr
            / radius_y
        )
        ** winding
        * y_envelope
    )

    y2_analytic = overlap_y_with_x_gaussian(
        winding,
        amplitude_y,
        radius_y,
        height_y,
        radius_x,
        height_x,
        0,
    )

    omega = (
        charge
        / (
            4.0
            * y2_analytic
        )
    )

    x_r = (
        amplitude_x
        * x_envelope
        * rr
        / (
            radius_x
            * radius_x
        )
    )

    x_z = (
        amplitude_x
        * x_envelope
        * zz
        / (
            height_x
            * height_x
        )
    )

    safe_radius = np.maximum(
        rr,
        1.0e-300,
    )

    y_r = (
        field_y
        * (
            winding
            / safe_radius
            -
            rr
            / (
                radius_y
                * radius_y
            )
        )
    )

    y_z = (
        -field_y
        * zz
        / (
            height_y
            * height_y
        )
    )

    angular_gradient = (
        winding
        * winding
        * field_y
        * field_y
        / (
            safe_radius
            * safe_radius
        )
    )

    potential = (
        mu
        / 4.0
        * (
            1.0
            -
            field_x
            * field_x
        )
        ** 2
        +
        2.0
        * field_x
        * field_x
        * field_y
        * field_y
    )

    energy_density = (
        0.5
        * (
            x_r
            * x_r
            +
            x_z
            * x_z
        )
        +
        2.0
        * (
            omega
            * omega
            * field_y
            * field_y
            +
            y_r
            * y_r
            +
            y_z
            * y_z
            +
            angular_gradient
        )
        +
        potential
    )

    pressure_r = (
        0.5
        * (
            x_r
            * x_r
            -
            x_z
            * x_z
        )
        +
        2.0
        * (
            omega
            * omega
            * field_y
            * field_y
            +
            y_r
            * y_r
            -
            y_z
            * y_z
            -
            angular_gradient
        )
        -
        potential
    )

    pressure_z = (
        0.5
        * (
            -x_r
            * x_r
            +
            x_z
            * x_z
        )
        +
        2.0
        * (
            omega
            * omega
            * field_y
            * field_y
            -
            y_r
            * y_r
            +
            y_z
            * y_z
            -
            angular_gradient
        )
        -
        potential
    )

    pressure_phi = (
        -0.5
        * (
            x_r
            * x_r
            +
            x_z
            * x_z
        )
        +
        2.0
        * (
            omega
            * omega
            * field_y
            * field_y
            -
            y_r
            * y_r
            -
            y_z
            * y_z
            +
            angular_gradient
        )
        -
        potential
    )

    active_direct = (
        energy_density
        +
        pressure_r
        +
        pressure_z
        +
        pressure_phi
    )

    active_closed = (
        8.0
        * omega
        * omega
        * field_y
        * field_y
        -
        2.0
        * potential
    )

    active_scale = max(
        1.0,
        float(
            np.max(
                np.abs(
                    active_direct
                )
            )
        ),
    )

    active_identity_error = float(
        np.max(
            np.abs(
                active_direct
                -
                active_closed
            )
        )
        / active_scale
    )

    energy = float(
        np.sum(
            volume_weights
            * energy_density
        )
    )

    active_mass = float(
        np.sum(
            volume_weights
            * active_direct
        )
    )

    pressure_trace = float(
        np.sum(
            volume_weights
            * (
                pressure_r
                +
                pressure_z
                +
                pressure_phi
            )
        )
    )

    negative_active = float(
        np.sum(
            volume_weights
            * np.maximum(
                -active_direct,
                0.0,
            )
        )
    )

    z_characteristic = max(
        height_x,
        height_y,
    )

    near_heights = np.linspace(
        0.10
        * z_characteristic,
        3.0
        * z_characteristic,
        121,
    )

    exterior_upper = max(
        6.0
        * z_characteristic,
        1.5
        * max(
            radius_x,
            radius_y,
        ),
    )

    exterior_heights = np.linspace(
        3.0
        * z_characteristic,
        exterior_upper,
        121,
    )

    def acceleration_scan(
        heights: np.ndarray,
    ) -> np.ndarray:
        values = []

        for height in heights:
            separation = (
                height
                -
                zz
            )

            denominator = (
                rr
                * rr
                +
                separation
                * separation
            ) ** 1.5

            kernel_integral = float(
                np.sum(
                    volume_weights
                    * active_direct
                    * separation
                    / denominator
                )
            )

            values.append(
                -kernel_integral
            )

        return np.asarray(
            values,
            dtype=float,
        )

    near_acceleration = acceleration_scan(
        near_heights
    )

    exterior_acceleration = acceleration_scan(
        exterior_heights
    )

    near_index = int(
        np.argmax(
            near_acceleration
        )
    )

    exterior_index = int(
        np.argmax(
            exterior_acceleration
        )
    )

    acceleration_at_3z = float(
        exterior_acceleration[
            0
        ]
    )

    return {
        "energy":
            energy,
        "active_mass":
            active_mass,
        "pressure_trace":
            pressure_trace,
        "negative_active":
            negative_active,
        "active_identity_error":
            active_identity_error,
        "near_max":
            float(
                near_acceleration[
                    near_index
                ]
            ),
        "near_height":
            float(
                near_heights[
                    near_index
                ]
            ),
        "exterior_max":
            float(
                exterior_acceleration[
                    exterior_index
                ]
            ),
        "exterior_height":
            float(
                exterior_heights[
                    exterior_index
                ]
            ),
        "acceleration_at_3z":
            acceleration_at_3z,
        "omega":
            omega,
        "radius_x":
            radius_x,
        "height_x":
            height_x,
        "radius_y":
            radius_y,
        "height_y":
            height_y,
        "amplitude_y":
            amplitude_y,
        "amplitude_x":
            amplitude_x,
    }


def print_case(
    charge: float,
    winding: int,
    mu: float,
    result,
    metrics: dict[str, object],
) -> None:
    """Print one promoted variational case."""

    analytic = float(
        result.fun
    )

    numerical = float(
        metrics[
            "energy"
        ]
    )

    energy_relative_error = abs(
        numerical
        -
        analytic
    ) / analytic

    active_over_energy = (
        float(
            metrics[
                "active_mass"
            ]
        )
        / numerical
    )

    trace_over_energy = (
        float(
            metrics[
                "pressure_trace"
            ]
        )
        / numerical
    )

    negative_active_fraction = (
        float(
            metrics[
                "negative_active"
            ]
        )
        / numerical
    )

    if result.jac is None:
        gradient_over_energy = math.nan
    else:
        gradient_over_energy = float(
            np.max(
                np.abs(
                    result.jac
                )
            )
            / analytic
        )

    print(
        "BOUND_CASE "
        f"MU={mu:.8f} "
        f"Q={charge:.1f} "
        f"N={winding:d} "
        f"E_OVER_Q={analytic/charge:.12f} "
        f"RX={metrics['radius_x']:.9f} "
        f"ZX={metrics['height_x']:.9f} "
        f"RY={metrics['radius_y']:.9f} "
        f"ZY={metrics['height_y']:.9f} "
        f"B={metrics['amplitude_y']:.9f} "
        f"A={metrics['amplitude_x']:.9f} "
        f"OMEGA={metrics['omega']:.12f} "
        f"ENERGY_QUADRATURE_REL_ERROR="
        f"{energy_relative_error:.3e} "
        f"ACTIVE_IDENTITY_ERROR="
        f"{metrics['active_identity_error']:.3e} "
        f"ACTIVE_MASS_OVER_E="
        f"{active_over_energy:.12f} "
        f"PRESSURE_TRACE_OVER_E="
        f"{trace_over_energy:+.3e} "
        f"NEGATIVE_ACTIVE_FRACTION_OVER_E="
        f"{negative_active_fraction:.12f} "
        f"OPT_GRADIENT_OVER_E="
        f"{gradient_over_energy:.3e} "
        f"NEAR_MAX_A_KERNEL="
        f"{metrics['near_max']:.12e} "
        f"NEAR_MAX_H="
        f"{metrics['near_height']:.9f} "
        f"A_AT_3Z_KERNEL="
        f"{metrics['acceleration_at_3z']:.12e} "
        f"EXTERIOR_MAX_A_KERNEL="
        f"{metrics['exterior_max']:.12e} "
        f"EXTERIOR_MAX_H="
        f"{metrics['exterior_height']:.9f}"
    )


def main() -> None:
    """Execute the explicit canonical-field gravitational sign gate."""

    print(
        "=== 016H — EXPLICIT CANONICAL FIELD MODEL "
        "OUTWARD-GRAVITY GATE ==="
    )

    print()

    print(
        "MODEL="
        "FLS_INSPIRED_REAL_SCALAR_PLUS_EQUAL_COUNTERWINDING_COMPLEX_PAIR"
    )

    print(
        "GAUGE_FIELD_INCLUDED="
        "NO_OPTIMISTIC_SIGN_PREFLIGHT"
    )

    print(
        "NET_T_TPHI_FROM_COMPLEX_PAIR="
        "ZERO_BY_EQUAL_OPPOSITE_WINDING"
    )

    print(
        "POTENTIAL_NONNEGATIVE="
        "YES"
    )

    print(
        "FREE_PARTICLE_THRESHOLD_E_OVER_Q="
        f"{FREE_PARTICLE_THRESHOLD:.12f}"
    )

    print(
        "CLEAN_EXTERIOR_START="
        "H_GE_3_TIMES_MAX_Z_WIDTH"
    )

    print(
        "GAUSSIAN_AMPLITUDE_AT_3Z="
        f"{SOURCE_TAIL_AMPLITUDE_AT_3Z:.12e}"
    )

    records = []

    for mu in MU_VALUES:
        for charge in CHARGES:
            for winding in WINDINGS:
                result = optimize_case(
                    charge,
                    winding,
                    mu,
                )

                (
                    radius_x,
                    height_x,
                    radius_y,
                    height_y,
                    amplitude_y,
                    amplitude_x,
                ) = unpack(
                    result.x
                )

                e_over_q = (
                    float(
                        result.fun
                    )
                    / charge
                )

                localized = bool(
                    amplitude_x
                    >
                    PROFILE_AMPLITUDE_MIN
                    and amplitude_y
                    >
                    0.0051
                    and radius_x
                    <
                    149.0
                    and height_x
                    <
                    149.0
                    and radius_y
                    <
                    149.0
                    and height_y
                    <
                    149.0
                )

                bound = bool(
                    e_over_q
                    <
                    BOUND_E_OVER_Q_MAX
                )

                if not (
                    localized
                    and bound
                ):
                    print(
                        "NONPROMOTED_CASE "
                        f"MU={mu:.8f} "
                        f"Q={charge:.1f} "
                        f"N={winding:d} "
                        f"E_OVER_Q={e_over_q:.12f} "
                        f"LOCALIZED={localized} "
                        f"BOUND={bound}"
                    )

                    continue

                metrics = field_arrays(
                    result.x,
                    charge,
                    winding,
                    mu,
                    order=64,
                )

                analytic_energy_value = float(
                    result.fun
                )

                numerical_energy_value = float(
                    metrics[
                        "energy"
                    ]
                )

                energy_relative_error = abs(
                    numerical_energy_value
                    -
                    analytic_energy_value
                ) / analytic_energy_value

                active_ratio = (
                    float(
                        metrics[
                            "active_mass"
                        ]
                    )
                    / numerical_energy_value
                )

                trace_ratio = (
                    float(
                        metrics[
                            "pressure_trace"
                        ]
                    )
                    / numerical_energy_value
                )

                internal_consistency = bool(
                    energy_relative_error
                    <
                    3.0e-3
                    and float(
                        metrics[
                            "active_identity_error"
                        ]
                    )
                    <
                    1.0e-11
                    and abs(
                        active_ratio
                        -
                        1.0
                    )
                    <
                    1.0e-2
                    and abs(
                        trace_ratio
                    )
                    <
                    1.0e-2
                )

                record = {
                    "mu":
                        mu,
                    "charge":
                        charge,
                    "winding":
                        winding,
                    "result":
                        result,
                    "metrics":
                        metrics,
                    "consistent":
                        internal_consistency,
                    "e_over_q":
                        e_over_q,
                }

                records.append(
                    record
                )

                print_case(
                    charge,
                    winding,
                    mu,
                    result,
                    metrics,
                )

                print(
                    "CASE_INTERNAL_CONSISTENCY="
                    f"{internal_consistency}"
                )

    print()
    print(
        "=== 016H GLOBAL SCAN SUMMARY ==="
    )

    consistent_records = [
        record
        for record
        in records
        if record[
            "consistent"
        ]
    ]

    print(
        "PROMOTED_BOUND_CASES="
        f"{len(records)}"
    )

    print(
        "INTERNALLY_CONSISTENT_BOUND_CASES="
        f"{len(consistent_records)}"
    )

    if not consistent_records:
        print(
            "016H_DECISION="
            "NO_TRUSTWORTHY_VARIATIONAL_STATES"
        )

        print(
            "NEXT_AFTER_DOCUMENTATION="
            "AUDIT_VARIATIONAL_IMPLEMENTATION"
        )

        print(
            "PRACTICAL_ANTIGRAVITY_DEVICE="
            "NO"
        )

        return

    any_negative_active = any(
        float(
            record[
                "metrics"
            ][
                "negative_active"
            ]
        )
        >
        0.0
        for record
        in consistent_records
    )

    any_near_outward = any(
        float(
            record[
                "metrics"
            ][
                "near_max"
            ]
        )
        >
        0.0
        for record
        in consistent_records
    )

    any_exterior_outward = any(
        float(
            record[
                "metrics"
            ][
                "exterior_max"
            ]
        )
        >
        0.0
        for record
        in consistent_records
    )

    best_exterior = max(
        consistent_records,
        key=lambda record:
            float(
                record[
                    "metrics"
                ][
                    "exterior_max"
                ]
            ),
    )

    best_negative_fraction = max(
        consistent_records,
        key=lambda record:
            float(
                record[
                    "metrics"
                ][
                    "negative_active"
                ]
            )
            / float(
                record[
                    "metrics"
                ][
                    "energy"
                ]
            ),
    )

    print(
        "NEGATIVE_ACTIVE_DENSITY_EXISTS="
        f"{any_negative_active}"
    )

    print(
        "ANY_NEAR_FIELD_OUTWARD_ACCELERATION="
        f"{any_near_outward}"
    )

    print(
        "ANY_CLEAN_EXTERIOR_OUTWARD_ACCELERATION="
        f"{any_exterior_outward}"
    )

    print(
        "BEST_EXTERIOR_CASE "
        f"MU={best_exterior['mu']:.8f} "
        f"Q={best_exterior['charge']:.1f} "
        f"N={best_exterior['winding']:d} "
        f"E_OVER_Q={best_exterior['e_over_q']:.12f} "
        f"A_KERNEL="
        f"{best_exterior['metrics']['exterior_max']:.12e} "
        f"H="
        f"{best_exterior['metrics']['exterior_height']:.9f}"
    )

    best_negative_ratio = (
        float(
            best_negative_fraction[
                "metrics"
            ][
                "negative_active"
            ]
        )
        /
        float(
            best_negative_fraction[
                "metrics"
            ][
                "energy"
            ]
        )
    )

    print(
        "LARGEST_NEGATIVE_ACTIVE_FRACTION_CASE "
        f"MU={best_negative_fraction['mu']:.8f} "
        f"Q={best_negative_fraction['charge']:.1f} "
        f"N={best_negative_fraction['winding']:d} "
        f"NEGATIVE_ACTIVE_FRACTION_OVER_E="
        f"{best_negative_ratio:.12f}"
    )

    print()
    print(
        "=== INDEPENDENT FORCE-RESOLUTION CHECK ==="
    )

    validation_orders = (
        64,
        96,
        128,
    )

    validation_values = []

    for order in validation_orders:
        validation = field_arrays(
            best_exterior[
                "result"
            ].x,
            best_exterior[
                "charge"
            ],
            best_exterior[
                "winding"
            ],
            best_exterior[
                "mu"
            ],
            order=order,
        )

        validation_values.append(
            float(
                validation[
                    "exterior_max"
                ]
            )
        )

        print(
            "VALIDATION "
            f"ORDER={order:d} "
            f"ENERGY="
            f"{validation['energy']:.15e} "
            f"ACTIVE_MASS_OVER_E="
            f"{validation['active_mass']/validation['energy']:.15e} "
            f"PRESSURE_TRACE_OVER_E="
            f"{validation['pressure_trace']/validation['energy']:+.3e} "
            f"ACTIVE_IDENTITY_ERROR="
            f"{validation['active_identity_error']:.3e} "
            f"A_AT_3Z="
            f"{validation['acceleration_at_3z']:.15e} "
            f"EXTERIOR_MAX_A="
            f"{validation['exterior_max']:.15e} "
            f"EXTERIOR_MAX_H="
            f"{validation['exterior_height']:.12f}"
        )

    force_sign_stable = all(
        value
        >
        0.0
        for value
        in validation_values
    ) or all(
        value
        <
        0.0
        for value
        in validation_values
    )

    print(
        "EXTERIOR_FORCE_SIGN_RESOLUTION_STABLE="
        f"{force_sign_stable}"
    )

    print()
    print(
        "=== 016H FINAL DECISION ==="
    )

    if (
        any_exterior_outward
        and force_sign_stable
        and validation_values[
            -1
        ]
        >
        0.0
    ):
        print(
            "EXPLICIT_CANONICAL_FIELD_VARIATIONAL_"
            "EXTERIOR_REPULSION="
            "FOUND"
        )

        print(
            "OBSERVABLE_FIRST_REALIZATION_ESCAPE="
            "GREEN_AT_VARIATIONAL_LEVEL"
        )

        print(
            "MAJOR_RESULT="
            "EXPLICIT_LOCAL_RELATIVISTIC_FIELD_MODEL_"
            "NATURALLY_GENERATES_OUTWARD_LINEARIZED_GR_FIELD_"
            "WITHOUT_EXACT_006D_STRESS_MATCHING"
        )

        print(
            "NEXT_AFTER_DOCUMENTATION="
            "FULL_2D_COUNTERWINDING_FLS_EULER_LAGRANGE_"
            "BOUNDARY_VALUE_SOLVE"
        )

    elif (
        any_near_outward
        and not any_exterior_outward
    ):
        print(
            "EXPLICIT_CANONICAL_FIELD_VARIATIONAL_"
            "LOCAL_REPULSIVE_ZONE="
            "YES"
        )

        print(
            "EXPLICIT_CANONICAL_FIELD_VARIATIONAL_"
            "CLEAN_EXTERIOR_REPULSION="
            "NO_IN_TESTED_SCAN"
        )

        print(
            "INTERPRETATION="
            "LOCAL_NEGATIVE_ACTIVE_STRESS_DOES_NOT_LIFT_TO_"
            "OPERATIONAL_EXTERIOR_REPULSION"
        )

        print(
            "NEXT_AFTER_DOCUMENTATION="
            "REQUIRE_STRONGER_SPATIAL_SEGREGATION_OR_RERANK_"
            "AGAINST_NON_GR_BRANCHES"
        )

    else:
        print(
            "EXPLICIT_CANONICAL_FIELD_VARIATIONAL_"
            "EXTERIOR_REPULSION="
            "NOT_FOUND_IN_TESTED_SCAN"
        )

        print(
            "EXPLICIT_CANONICAL_FIELD_VARIATIONAL_"
            "NEAR_FIELD_REPULSION="
            "NOT_FOUND_IN_TESTED_SCAN"
        )

        print(
            "NEGATIVE_ACTIVE_DENSITY_WITHOUT_REPULSIVE_FIELD="
            f"{any_negative_active}"
        )

        print(
            "INTERPRETATION="
            "GENERIC_COUNTERWINDING_FLS_LIKE_EQUILIBRIA_"
            "DO_NOT_AUTOMATICALLY_INHERIT_006D_REPULSION"
        )

        print(
            "NEXT_AFTER_DOCUMENTATION="
            "DEPRIORITIZE_GENERIC_FLS_QBALL_REALIZATION_AND_"
            "RERANK_SPATIALLY_SEPARATED_DRUM_VORTON_006D_"
            "VERSUS_014D_DISFORMAL_AND_SURVIVING_FIFTH_FORCE_BRANCHES"
        )

    print(
        "006D_GRAVITATIONAL_CONSTRUCTION_INVALIDATED="
        "NO"
    )

    print(
        "016G_ASYMPTOTIC_NO_GO_INVALIDATED="
        "NO"
    )

    print(
        "FULL_EULER_LAGRANGE_FIELD_SOLUTION="
        "NOT_ESTABLISHED"
    )

    print(
        "FULL_DYNAMIC_STABILITY="
        "NOT_ESTABLISHED"
    )

    print(
        "NONLINEAR_GR_REALIZATION="
        "NOT_ESTABLISHED"
    )

    print(
        "MACROSCOPIC_AH2_OVER_G_ENERGY_SCALING="
        "UNCHANGED"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE="
        "NO"
    )

    print(
        "PAUSE_AND_UPDATE_DOCUMENTATION_AFTER_016H="
        "YES"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_EXPLICIT_CANONICAL_FIELD_"
        "VARIATIONAL_GRAVITY_GATE"
    )


if __name__ == "__main__":
    main()
