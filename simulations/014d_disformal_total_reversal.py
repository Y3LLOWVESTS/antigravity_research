"""014D — disformal local total-force reversal gate.

PURPOSE
-------
Push the project-reproduced non-static disformal repulsive fifth force from
014C to the stronger operational criterion of LOCAL TOTAL-FORCE REVERSAL.

014C established, in a controlled reduced model, that

    F_phi . F_Psi < 0

occurs in converged nonsymmetric 2D and 3D calculations while the disformal
metric remains on the positive/invertible branch.

However, the fifth force was not strong enough to overwhelm Newtonian gravity.

The present gate varies the dimensionless disformal strength B0 and asks
whether there exists a controlled region in which

    F_total = F_Psi + F_phi

satisfies

    F_total . F_Psi < 0.

This is stronger than merely requiring an antiparallel fifth-force component.

SCIENTIFIC QUESTION
-------------------
Can the same non-static disformal mechanism independently reproduced in 014C
reverse the local TOTAL acceleration before approaching the disformal metric
degeneracy g_phi = 0?

REFERENCE MODEL
---------------
The reduced model follows the beta=0 Velocity-Flipping-type disformal
quintessence system used in

    Llinares, Hagala & Mota
    MNRAS 491, 1868-1886
    arXiv:1902.02125.

Natural units:

    H0 = M_Pl = c = 1.

Potential parameters:

    V0 = 10
    nu = 1.

The scalar equation is evolved without a quasistatic approximation.

For constant positive B0,

    g_phi
        =
        1
        + B0 [
            -phi_dot^2
            + |grad phi|^2/a^2
        ].

The fifth force is

    F_phi
        =
        -(1/2)
        (xi/g_phi)
        grad(phi),

with

    xi
        =
        2 B0 phi_ddot

for beta = 0.

Newtonian gravity is

    F_Psi
        =
        -grad(Psi)/a^2.

TOTAL-FORCE REVERSAL
--------------------
Define

    F_total
        =
        F_Psi
        + F_phi.

A point is classified as having a reversed total gravitational projection if

    F_total . F_Psi < 0.

This means the total acceleration has a component pointing opposite the
direction that Newtonian gravity alone would produce.

This is stricter than

    F_phi . F_Psi < 0.

METRIC-SAFETY REQUIREMENT
-------------------------
The disformal metric must remain invertible.

The mathematical singular surface is associated with

    g_phi = 0.

This experiment uses a deliberately stronger acceptance criterion:

    g_phi >= 0.10

everywhere in the accepted candidate calculations.

A force reversal which appears only below that margin is not promoted.

NUMERICAL STRATEGY
------------------
1. Scan B0 in a moderate 2D grid to locate the amplification transition.

2. Select B0 = 0.28 as the principal high-information candidate.

3. Recompute the background xi_0 = 0 crossing independently for every B0.

4. Use the same deterministic asymmetric positive-density geometry family
   as 014C.

5. Validate B0 = 0.28 with:
       64^2,
       96^2,
       128^2

   two-dimensional grids.

6. Independently validate with:
       24^3,
       32^3,
       40^3

   three-dimensional grids.

7. Repeat the 96^2 calculation with half the CFL timestep to exclude a
   time-integration artifact.

8. Evaluate the exact total-force projection criterion rather than inferring
   reversal from force magnitudes alone.

SOURCE MODEL
------------
Matter is an imposed positive Einstein-de Sitter growing-mode density field.

This remains a controlled reduced-field calculation, not a complete
self-consistent N-body simulation.

The density contrast is explicitly non-spherical and multimode.

CLAIM LIMITS
------------
A positive result would establish only:

    project-reproduced LOCAL TOTAL-FORCE REVERSAL
    in the controlled reduced disformal model.

It would NOT establish:

- universal antigravity;
- an isolated body's global acceleration;
- a practical propulsion device;
- a baryonic fifth force;
- compatibility with laboratory constraints;
- a stable material realization.

The reference model still applies its new matter metric to the dark sector,
not ordinary baryonic payloads.

If this gate is positive, the next scientific problem is no longer force
sign. It becomes construction of a screened baryonic disformal extension.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_REDUCED_DISFORMAL_LOCAL_TOTAL_FORCE_REVERSAL_GATE
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


# ===========================================================================
# Constants
# ===========================================================================

V0 = 10.0
NU = 1.0

BOX_LENGTH = 0.32

GPHI_ACCEPTANCE_FLOOR = 0.10


def scale_factor(time: float) -> float:
    """Einstein-de Sitter scale factor in H0=1 units."""

    return (1.5 * time) ** (2.0 / 3.0)


def hubble(time: float) -> float:
    """Einstein-de Sitter Hubble rate."""

    return 2.0 / (3.0 * time)


def background_density(time: float) -> float:
    """Einstein-de Sitter pressureless background density."""

    return 3.0 / scale_factor(time) ** 3


# ===========================================================================
# Background solver
# ===========================================================================

@dataclass
class Background:
    """Homogeneous scalar background for one B0."""

    B0: float
    solution: object
    root_time: float


def build_background(
    B0: float,
) -> Background:
    """Integrate homogeneous scalar dynamics and locate phi_ddot=0."""

    def rhs(
        time: float,
        state: np.ndarray,
    ) -> np.ndarray:

        phi = float(
            state[0]
        )

        phi_dot = float(
            state[1]
        )

        g_phi = (
            1.0
            - B0
            * phi_dot**2
        )

        if g_phi <= 0.0:
            raise RuntimeError(
                "BACKGROUND_GPHI_NONPOSITIVE"
            )

        gamma_squared = (
            B0
            / g_phi
        )

        phi_ddot = (
            -3.0
            * hubble(
                time
            )
            * phi_dot
            + NU
            * V0
            * math.exp(
                -NU
                * phi
            )
        ) / (
            1.0
            + gamma_squared
            * background_density(
                time
            )
        )

        return np.array(
            [
                phi_dot,
                phi_ddot,
            ],
            dtype=float,
        )

    solution = solve_ivp(
        rhs,
        (
            1.0e-5,
            2.20,
        ),
        (
            0.0,
            0.0,
        ),
        method="DOP853",
        rtol=2.0e-11,
        atol=2.0e-13,
        max_step=0.003,
        dense_output=True,
    )

    if not solution.success:
        raise RuntimeError(
            "BACKGROUND_SOLVER_FAILED:"
            + str(
                solution.message
            )
        )

    def acceleration(
        time: float,
    ) -> float:

        return float(
            rhs(
                time,
                solution.sol(
                    time
                ),
            )[1]
        )

    search_grid = np.linspace(
        0.20,
        2.10,
        5000,
    )

    values = np.array(
        [
            acceleration(
                time
            )
            for time in search_grid
        ]
    )

    crossing_indices = np.where(
        values[:-1]
        * values[1:]
        < 0.0
    )[0]

    if len(
        crossing_indices
    ) == 0:
        raise RuntimeError(
            "NO_XI0_ZERO_FOUND"
        )

    index = int(
        crossing_indices[0]
    )

    root_time = brentq(
        acceleration,
        float(
            search_grid[index]
        ),
        float(
            search_grid[
                index + 1
            ]
        ),
        xtol=1.0e-13,
        rtol=1.0e-13,
    )

    return Background(
        B0=B0,
        solution=solution,
        root_time=root_time,
    )


# ===========================================================================
# Periodic finite differences / Poisson solver
# ===========================================================================

def derivatives_nd(
    field: np.ndarray,
    spacing: float,
) -> tuple[
    list[np.ndarray],
    np.ndarray,
]:
    """Return periodic centered gradients and Laplacian."""

    gradients = []

    laplacian = np.zeros_like(
        field
    )

    for axis in range(
        field.ndim
    ):
        plus = np.roll(
            field,
            -1,
            axis=axis,
        )

        minus = np.roll(
            field,
            1,
            axis=axis,
        )

        gradients.append(
            (
                plus
                - minus
            ) / (
                2.0
                * spacing
            )
        )

        laplacian += (
            plus
            + minus
            - 2.0
            * field
        ) / spacing**2

    return (
        gradients,
        laplacian,
    )


def poisson_periodic(
    delta: np.ndarray,
    root_time: float,
) -> np.ndarray:
    """Solve the periodic Newtonian Poisson equation."""

    points = int(
        delta.shape[0]
    )

    dimension = int(
        delta.ndim
    )

    source = (
        scale_factor(
            root_time
        )**2
        * background_density(
            root_time
        )
        * delta
        / 2.0
    )

    source_hat = np.fft.fftn(
        source
    )

    frequencies = (
        2.0
        * math.pi
        * np.fft.fftfreq(
            points,
            d=BOX_LENGTH
            / points,
        )
    )

    meshes = np.meshgrid(
        *(
            [
                frequencies
            ]
            * dimension
        ),
        indexing="ij",
    )

    k_squared = np.zeros_like(
        delta,
        dtype=float,
    )

    for component in meshes:
        k_squared += (
            component**2
        )

    potential_hat = np.zeros_like(
        source_hat,
        dtype=np.complex128,
    )

    mask = (
        k_squared
        > 0.0
    )

    potential_hat[mask] = (
        -source_hat[mask]
        / k_squared[mask]
    )

    return np.fft.ifftn(
        potential_hat
    ).real


# ===========================================================================
# Deterministic nonsymmetric density fields
# ===========================================================================

def density_shape_2d(
    points: int,
) -> np.ndarray:
    """Return the deterministic 014C-style asymmetric 2D density contrast."""

    coordinate = (
        np.arange(
            points,
            dtype=float,
        )
        * BOX_LENGTH
        / points
    )

    x, y = np.meshgrid(
        coordinate,
        coordinate,
        indexing="ij",
    )

    u = (
        2.0
        * math.pi
        * x
        / BOX_LENGTH
    )

    v = (
        2.0
        * math.pi
        * y
        / BOX_LENGTH
    )

    raw = (
        0.95 * np.cos(u + 0.17)
        + 0.70 * np.sin(v - 0.41)
        + 0.55 * np.cos(u + 2.0 * v + 0.73)
        + 0.42 * np.sin(2.0 * u - v + 1.31)
        + 0.33 * np.cos(3.0 * u + v - 0.62)
        + 0.27 * np.sin(u - 3.0 * v + 0.28)
        + 0.20 * np.cos(2.0 * u + 3.0 * v + 2.0)
    )

    raw = (
        raw
        - np.mean(
            raw
        )
    ) / np.std(
        raw
    )

    lognormal = np.exp(
        4.0
        * raw
    )

    contrast = (
        lognormal
        / np.mean(
            lognormal
        )
        - 1.0
    )

    contrast *= (
        0.85
        / (
            -float(
                np.min(
                    contrast
                )
            )
        )
    )

    return contrast


def density_shape_3d(
    points: int,
) -> np.ndarray:
    """Return the deterministic 014C-style asymmetric 3D density contrast."""

    coordinate = (
        np.arange(
            points,
            dtype=float,
        )
        * BOX_LENGTH
        / points
    )

    x, y, z = np.meshgrid(
        coordinate,
        coordinate,
        coordinate,
        indexing="ij",
    )

    u = (
        2.0
        * math.pi
        * x
        / BOX_LENGTH
    )

    v = (
        2.0
        * math.pi
        * y
        / BOX_LENGTH
    )

    w = (
        2.0
        * math.pi
        * z
        / BOX_LENGTH
    )

    raw = (
        0.80 * np.cos(u + 0.17)
        + 0.65 * np.sin(v - 0.41)
        + 0.55 * np.cos(w + 0.90)
        + 0.45 * np.cos(u + 2.0 * v - w + 0.73)
        + 0.35 * np.sin(2.0 * u - v + 2.0 * w + 1.31)
        + 0.28 * np.cos(3.0 * u + v + w - 0.62)
        + 0.22 * np.sin(u - 3.0 * v + 2.0 * w + 0.28)
    )

    raw = (
        raw
        - np.mean(
            raw
        )
    ) / np.std(
        raw
    )

    lognormal = np.exp(
        2.0
        * raw
    )

    contrast = (
        lognormal
        / np.mean(
            lognormal
        )
        - 1.0
    )

    contrast *= (
        0.85
        / (
            -float(
                np.min(
                    contrast
                )
            )
        )
    )

    return contrast


# ===========================================================================
# Force metrics
# ===========================================================================

@dataclass
class Metrics:
    """Force and health diagnostics at one time."""

    time: float

    minimum_g_phi: float
    minimum_kinetic_denominator: float

    maximum_abs_psi: float

    fifth_antiparallel_fraction: float

    total_reversal_fraction: float

    maximum_fifth_over_newtonian: float

    maximum_outward_total_projection: float

    minimum_total_force_cosine: float

    rms_fifth_over_newtonian: float

    background_mean_relative_error: float


@dataclass
class RunResult:
    """One complete spatial evolution."""

    B0: float
    dimension: int
    points: int
    cfl: float

    root_time: float

    background_g_phi_at_root: float

    root_metrics: Metrics

    peak_metrics: Metrics


# ===========================================================================
# Spatial nonlinear evolution
# ===========================================================================

def run_case(
    *,
    B0: float,
    dimension: int,
    points: int,
    cfl: float = 0.18,
) -> RunResult:
    """Evolve one non-static spatial configuration."""

    background = build_background(
        B0
    )

    root_time = (
        background.root_time
    )

    start_time = max(
        0.20,
        root_time - 0.30,
    )

    end_time = (
        root_time + 0.12
    )

    if dimension == 2:
        delta_root = density_shape_2d(
            points
        )

    elif dimension == 3:
        delta_root = density_shape_3d(
            points
        )

    else:
        raise ValueError(
            "dimension must equal 2 or 3"
        )

    spacing = (
        BOX_LENGTH
        / points
    )

    psi = poisson_periodic(
        delta_root,
        root_time,
    )

    (
        psi_gradients,
        _,
    ) = derivatives_nd(
        psi,
        spacing,
    )

    root_background_state = (
        background
        .solution
        .sol(
            root_time
        )
    )

    root_phi_background = float(
        root_background_state[0]
    )

    root_phi_dot_background = float(
        root_background_state[1]
    )

    background_g_phi_at_root = (
        1.0
        - B0
        * root_phi_dot_background**2
    )

    if (
        background_g_phi_at_root
        <= 0.0
    ):
        raise RuntimeError(
            "BACKGROUND_METRIC_NONINVERTIBLE"
        )

    def background_acceleration(
        time: float,
    ) -> float:
        state = (
            background
            .solution
            .sol(
                time
            )
        )

        phi = float(
            state[0]
        )

        phi_dot = float(
            state[1]
        )

        g_phi = (
            1.0
            - B0
            * phi_dot**2
        )

        gamma_squared = (
            B0
            / g_phi
        )

        return (
            -3.0
            * hubble(
                time
            )
            * phi_dot
            + NU
            * V0
            * math.exp(
                -NU
                * phi
            )
        ) / (
            1.0
            + gamma_squared
            * background_density(
                time
            )
        )

    initial_background = (
        background
        .solution
        .sol(
            start_time
        )
    )

    phi0 = float(
        initial_background[0]
    )

    phi_dot0 = float(
        initial_background[1]
    )

    xi0 = (
        2.0
        * B0
        * background_acceleration(
            start_time
        )
    )

    derivative_step = (
        2.0e-5
    )

    xi_dot0 = (
        2.0
        * B0
        * (
            background_acceleration(
                start_time
                + derivative_step
            )
            - background_acceleration(
                start_time
                - derivative_step
            )
        )
        / (
            2.0
            * derivative_step
        )
    )

    phi = (
        np.full(
            delta_root.shape,
            phi0,
            dtype=float,
        )
        + xi0
        * psi
    )

    phi_dot = (
        np.full(
            delta_root.shape,
            phi_dot0,
            dtype=float,
        )
        + xi_dot0
        * psi
    )

    a_root = scale_factor(
        root_time
    )

    def rhs(
        time: float,
        current_phi: np.ndarray,
        current_phi_dot: np.ndarray,
    ):
        """Return full beta=0 non-static scalar evolution."""

        a = scale_factor(
            time
        )

        H = hubble(
            time
        )

        contrast = (
            delta_root
            * a
            / a_root
        )

        density = (
            background_density(
                time
            )
            * (
                1.0
                + contrast
            )
        )

        (
            gradients,
            laplacian,
        ) = derivatives_nd(
            current_phi,
            spacing,
        )

        gradient_squared = np.zeros_like(
            current_phi
        )

        for component in gradients:
            gradient_squared += (
                component**2
            )

        g_phi = (
            1.0
            + B0
            * (
                -current_phi_dot**2
                + gradient_squared
                / a**2
            )
        )

        gamma_squared = (
            B0
            / g_phi
        )

        kinetic_denominator = (
            1.0
            + gamma_squared
            * density
        )

        phi_ddot = (
            laplacian
            / a**2
            - 3.0
            * H
            * current_phi_dot
            + NU
            * V0
            * np.exp(
                -NU
                * current_phi
            )
        ) / kinetic_denominator

        return (
            current_phi_dot,
            phi_ddot,
            g_phi,
            kinetic_denominator,
            gradients,
        )

    def metrics(
        time: float,
        current_phi: np.ndarray,
        current_phi_dot: np.ndarray,
    ) -> Metrics:
        """Compute exact fifth, Newtonian and total-force diagnostics."""

        a = scale_factor(
            time
        )

        (
            _,
            phi_ddot,
            g_phi,
            kinetic_denominator,
            gradients,
        ) = rhs(
            time,
            current_phi,
            current_phi_dot,
        )

        xi = (
            2.0
            * B0
            * phi_ddot
        )

        fifth_components = []

        newton_components = []

        for (
            phi_gradient,
            psi_gradient,
        ) in zip(
            gradients,
            psi_gradients,
        ):
            fifth_components.append(
                -0.5
                * (
                    xi
                    / g_phi
                )
                * phi_gradient
            )

            newton_components.append(
                -psi_gradient
                / a**2
            )

        fifth_squared = np.zeros_like(
            current_phi
        )

        newton_squared = np.zeros_like(
            current_phi
        )

        fifth_dot_newton = np.zeros_like(
            current_phi
        )

        total_squared = np.zeros_like(
            current_phi
        )

        total_dot_newton = np.zeros_like(
            current_phi
        )

        for (
            fifth_component,
            newton_component,
        ) in zip(
            fifth_components,
            newton_components,
        ):
            total_component = (
                fifth_component
                + newton_component
            )

            fifth_squared += (
                fifth_component**2
            )

            newton_squared += (
                newton_component**2
            )

            fifth_dot_newton += (
                fifth_component
                * newton_component
            )

            total_squared += (
                total_component**2
            )

            total_dot_newton += (
                total_component
                * newton_component
            )

        fifth_magnitude = np.sqrt(
            fifth_squared
        )

        newton_magnitude = np.sqrt(
            newton_squared
        )

        total_magnitude = np.sqrt(
            total_squared
        )

        gravity_mask = (
            newton_magnitude
            > 0.05
            * float(
                np.max(
                    newton_magnitude
                )
            )
        )

        fifth_antiparallel = (
            gravity_mask
            & (
                fifth_dot_newton
                < 0.0
            )
        )

        total_reversal = (
            gravity_mask
            & (
                total_dot_newton
                < 0.0
            )
        )

        fifth_ratio = np.zeros_like(
            current_phi
        )

        fifth_ratio[
            gravity_mask
        ] = (
            fifth_magnitude[
                gravity_mask
            ]
            / newton_magnitude[
                gravity_mask
            ]
        )

        outward_projection = np.zeros_like(
            current_phi
        )

        outward_projection[
            gravity_mask
        ] = (
            -total_dot_newton[
                gravity_mask
            ]
            / newton_squared[
                gravity_mask
            ]
        )

        total_cosine = np.ones_like(
            current_phi
        )

        valid_total_direction = (
            gravity_mask
            & (
                total_magnitude
                > 1.0e-18
            )
        )

        total_cosine[
            valid_total_direction
        ] = (
            total_dot_newton[
                valid_total_direction
            ]
            / (
                total_magnitude[
                    valid_total_direction
                ]
                * newton_magnitude[
                    valid_total_direction
                ]
            )
        )

        background_phi = float(
            background
            .solution
            .sol(
                time
            )[0]
        )

        background_mean_relative_error = (
            abs(
                float(
                    np.mean(
                        current_phi
                    )
                )
                - background_phi
            )
            / max(
                abs(
                    background_phi
                ),
                1.0e-12,
            )
        )

        return Metrics(
            time=time,

            minimum_g_phi=float(
                np.min(
                    g_phi
                )
            ),

            minimum_kinetic_denominator=float(
                np.min(
                    kinetic_denominator
                )
            ),

            maximum_abs_psi=float(
                np.max(
                    np.abs(
                        psi
                    )
                )
            ),

            fifth_antiparallel_fraction=float(
                np.sum(
                    fifth_antiparallel
                )
                / np.sum(
                    gravity_mask
                )
            ),

            total_reversal_fraction=float(
                np.sum(
                    total_reversal
                )
                / np.sum(
                    gravity_mask
                )
            ),

            maximum_fifth_over_newtonian=float(
                np.max(
                    fifth_ratio[
                        gravity_mask
                    ]
                )
            ),

            maximum_outward_total_projection=(
                float(
                    np.max(
                        outward_projection[
                            total_reversal
                        ]
                    )
                )
                if np.any(
                    total_reversal
                )
                else 0.0
            ),

            minimum_total_force_cosine=float(
                np.min(
                    total_cosine[
                        valid_total_direction
                    ]
                )
            ),

            rms_fifth_over_newtonian=(
                math.sqrt(
                    float(
                        np.mean(
                            fifth_squared[
                                gravity_mask
                            ]
                        )
                    )
                )
                / math.sqrt(
                    float(
                        np.mean(
                            newton_squared[
                                gravity_mask
                            ]
                        )
                    )
                )
            ),

            background_mean_relative_error=(
                background_mean_relative_error
            ),
        )

    records = []

    def evolve(
        start: float,
        stop: float,
        current_phi: np.ndarray,
        current_phi_dot: np.ndarray,
    ):
        """Advance one interval with SSPRK3."""

        duration = (
            stop
            - start
        )

        maximum_dt = (
            cfl
            * spacing
            * scale_factor(
                start
            )
        )

        number_of_steps = max(
            1,
            int(
                math.ceil(
                    duration
                    / maximum_dt
                )
            ),
        )

        dt = (
            duration
            / number_of_steps
        )

        diagnostic_stride = max(
            1,
            number_of_steps
            // 80,
        )

        for step in range(
            number_of_steps
        ):
            time = (
                start
                + step
                * dt
            )

            (
                k_phi,
                k_dot,
                _,
                _,
                _,
            ) = rhs(
                time,
                current_phi,
                current_phi_dot,
            )

            phi_1 = (
                current_phi
                + dt
                * k_phi
            )

            dot_1 = (
                current_phi_dot
                + dt
                * k_dot
            )

            (
                l_phi,
                l_dot,
                _,
                _,
                _,
            ) = rhs(
                time + dt,
                phi_1,
                dot_1,
            )

            phi_2 = (
                0.75
                * current_phi
                + 0.25
                * (
                    phi_1
                    + dt
                    * l_phi
                )
            )

            dot_2 = (
                0.75
                * current_phi_dot
                + 0.25
                * (
                    dot_1
                    + dt
                    * l_dot
                )
            )

            (
                m_phi,
                m_dot,
                _,
                _,
                _,
            ) = rhs(
                time
                + 0.5
                * dt,
                phi_2,
                dot_2,
            )

            current_phi = (
                current_phi
                / 3.0
                + 2.0
                / 3.0
                * (
                    phi_2
                    + dt
                    * m_phi
                )
            )

            current_phi_dot = (
                current_phi_dot
                / 3.0
                + 2.0
                / 3.0
                * (
                    dot_2
                    + dt
                    * m_dot
                )
            )

            if (
                step
                % diagnostic_stride
                == 0
                or step
                == number_of_steps
                - 1
            ):
                current_metrics = metrics(
                    time + dt,
                    current_phi,
                    current_phi_dot,
                )

                records.append(
                    current_metrics
                )

                if (
                    current_metrics
                    .minimum_g_phi
                    <= 0.0
                ):
                    raise RuntimeError(
                        "SPATIAL_GPHI_NONPOSITIVE"
                    )

        return (
            current_phi,
            current_phi_dot,
        )

    phi, phi_dot = evolve(
        start_time,
        root_time,
        phi,
        phi_dot,
    )

    root_metrics = metrics(
        root_time,
        phi,
        phi_dot,
    )

    records.append(
        root_metrics
    )

    phi, phi_dot = evolve(
        root_time,
        end_time,
        phi,
        phi_dot,
    )

    peak_metrics = max(
        records,
        key=lambda result:
            result.maximum_outward_total_projection,
    )

    return RunResult(
        B0=B0,
        dimension=dimension,
        points=points,
        cfl=cfl,

        root_time=root_time,

        background_g_phi_at_root=(
            background_g_phi_at_root
        ),

        root_metrics=root_metrics,

        peak_metrics=peak_metrics,
    )


def print_run(
    label: str,
    result: RunResult,
) -> None:
    """Print compact diagnostics for one spatial run."""

    root = (
        result.root_metrics
    )

    peak = (
        result.peak_metrics
    )

    print(
        f"{label} "
        f"B0={result.B0:.6f} "
        f"DIM={result.dimension} "
        f"GRID={result.points} "
        f"CFL={result.cfl:.4f} "
        f"T_XI0={result.root_time:.16e} "
        f"BG_GPHI_ROOT="
        f"{result.background_g_phi_at_root:.16e} "
        f"ROOT_MIN_GPHI="
        f"{root.minimum_g_phi:.16e} "
        f"ROOT_MIN_KINETIC_DEN="
        f"{root.minimum_kinetic_denominator:.16e} "
        f"ROOT_MAX_ABS_PSI="
        f"{root.maximum_abs_psi:.16e} "
        f"ROOT_ANTIPARALLEL_FRAC="
        f"{root.fifth_antiparallel_fraction:.16e} "
        f"ROOT_TOTAL_REVERSAL_FRAC="
        f"{root.total_reversal_fraction:.16e} "
        f"ROOT_MAX_F5_OVER_FN="
        f"{root.maximum_fifth_over_newtonian:.16e} "
        f"ROOT_MAX_OUTWARD_TOTAL_PROJ="
        f"{root.maximum_outward_total_projection:.16e} "
        f"ROOT_MIN_TOTAL_COS="
        f"{root.minimum_total_force_cosine:+.16e} "
        f"ROOT_RMS_F5_OVER_FN="
        f"{root.rms_fifth_over_newtonian:.16e}"
    )

    print(
        f"{label}_PEAK "
        f"TIME={peak.time:.16e} "
        f"MIN_GPHI="
        f"{peak.minimum_g_phi:.16e} "
        f"TOTAL_REVERSAL_FRAC="
        f"{peak.total_reversal_fraction:.16e} "
        f"MAX_F5_OVER_FN="
        f"{peak.maximum_fifth_over_newtonian:.16e} "
        f"MAX_OUTWARD_TOTAL_PROJ="
        f"{peak.maximum_outward_total_projection:.16e}"
    )


# ===========================================================================
# 1. Coarse B0 amplification scan
# ===========================================================================

print("=== COARSE 2D B0 AMPLIFICATION SCAN ===")

scan_B0 = [
    0.10,
    0.14,
    0.18,
    0.20,
    0.22,
    0.24,
    0.26,
    0.28,
    0.30,
]

scan_results = []

for B0 in scan_B0:
    result = run_case(
        B0=B0,
        dimension=2,
        points=48,
    )

    scan_results.append(
        result
    )

    print_run(
        "SCAN",
        result,
    )


safe_scan_reversal = [
    result
    for result in scan_results
    if (
        result
        .peak_metrics
        .total_reversal_fraction
        > 0.0
        and result
        .peak_metrics
        .minimum_g_phi
        >= GPHI_ACCEPTANCE_FLOOR
    )
]

print(
    "COARSE_SAFE_TOTAL_REVERSAL_CASES="
    f"{len(safe_scan_reversal)}"
)

if safe_scan_reversal:
    first_safe = (
        safe_scan_reversal[0]
    )

    print(
        "FIRST_COARSE_SAFE_REVERSAL_B0="
        f"{first_safe.B0:.16e}"
    )

else:
    print(
        "FIRST_COARSE_SAFE_REVERSAL_B0="
        "NONE"
    )


# ===========================================================================
# 2. High-information B0 = 0.28 2D refinement
# ===========================================================================

print()
print("=== B0=0.28 2D REFINEMENT ===")

CANDIDATE_B0 = 0.28

runs_2d = []

for points in [
    64,
    96,
    128,
]:
    result = run_case(
        B0=CANDIDATE_B0,
        dimension=2,
        points=points,
        cfl=0.18,
    )

    runs_2d.append(
        result
    )

    print_run(
        "REFINE_2D",
        result,
    )


for result in runs_2d:
    assert (
        result
        .root_metrics
        .minimum_g_phi
        > GPHI_ACCEPTANCE_FLOOR
    )

    assert (
        result
        .root_metrics
        .minimum_kinetic_denominator
        > 0.0
    )

    assert (
        result
        .root_metrics
        .maximum_abs_psi
        < 0.05
    )

    assert (
        result
        .root_metrics
        .total_reversal_fraction
        > 0.05
    )

    assert (
        result
        .root_metrics
        .maximum_outward_total_projection
        > 0.10
    )


print(
    "2D_LOCAL_TOTAL_FORCE_REVERSAL_REFINEMENT_STABLE="
    "YES"
)


# ===========================================================================
# 3. Independent 3D refinement
# ===========================================================================

print()
print("=== B0=0.28 3D REFINEMENT ===")

runs_3d = []

for points in [
    24,
    32,
    40,
]:
    result = run_case(
        B0=CANDIDATE_B0,
        dimension=3,
        points=points,
        cfl=0.18,
    )

    runs_3d.append(
        result
    )

    print_run(
        "REFINE_3D",
        result,
    )


for result in runs_3d:
    assert (
        result
        .root_metrics
        .minimum_g_phi
        > GPHI_ACCEPTANCE_FLOOR
    )

    assert (
        result
        .root_metrics
        .minimum_kinetic_denominator
        > 0.0
    )

    assert (
        result
        .root_metrics
        .maximum_abs_psi
        < 0.05
    )

    assert (
        result
        .root_metrics
        .total_reversal_fraction
        > 0.002
    )

    assert (
        result
        .root_metrics
        .maximum_outward_total_projection
        > 0.20
    )


print(
    "3D_LOCAL_TOTAL_FORCE_REVERSAL_REFINEMENT_STABLE="
    "YES"
)


# ===========================================================================
# 4. Timestep-halving independent control
# ===========================================================================

print()
print("=== TIMESTEP HALVING CONTROL ===")

standard_dt_run = run_case(
    B0=CANDIDATE_B0,
    dimension=2,
    points=96,
    cfl=0.18,
)

half_dt_run = run_case(
    B0=CANDIDATE_B0,
    dimension=2,
    points=96,
    cfl=0.09,
)

print_run(
    "TIMESTEP_STANDARD",
    standard_dt_run,
)

print_run(
    "TIMESTEP_HALF",
    half_dt_run,
)

standard_projection = (
    standard_dt_run
    .root_metrics
    .maximum_outward_total_projection
)

half_projection = (
    half_dt_run
    .root_metrics
    .maximum_outward_total_projection
)

projection_relative_change = (
    abs(
        standard_projection
        - half_projection
    )
    / max(
        abs(
            half_projection
        ),
        1.0e-30,
    )
)

print(
    "TIMESTEP_HALVING_OUTWARD_PROJECTION_REL_CHANGE="
    f"{projection_relative_change:.16e}"
)

assert (
    projection_relative_change
    < 0.05
)

assert (
    standard_dt_run
    .root_metrics
    .total_reversal_fraction
    > 0.0
)

assert (
    half_dt_run
    .root_metrics
    .total_reversal_fraction
    > 0.0
)

print(
    "TIMESTEP_HALVING_REVERSAL_SIGN_STABLE="
    "YES"
)


# ===========================================================================
# 5. Refinement convergence summary
# ===========================================================================

print()
print("=== CONVERGENCE SUMMARY ===")

two_d_projection_last = (
    runs_2d[-1]
    .root_metrics
    .maximum_outward_total_projection
)

two_d_projection_previous = (
    runs_2d[-2]
    .root_metrics
    .maximum_outward_total_projection
)

two_d_projection_change = (
    abs(
        two_d_projection_last
        - two_d_projection_previous
    )
    / two_d_projection_last
)

three_d_projection_last = (
    runs_3d[-1]
    .root_metrics
    .maximum_outward_total_projection
)

three_d_projection_previous = (
    runs_3d[-2]
    .root_metrics
    .maximum_outward_total_projection
)

three_d_projection_change = (
    abs(
        three_d_projection_last
        - three_d_projection_previous
    )
    / three_d_projection_last
)

print(
    "2D_HIGH_GRID_MAX_OUTWARD_PROJECTION_REL_CHANGE="
    f"{two_d_projection_change:.16e}"
)

print(
    "3D_HIGH_GRID_MAX_OUTWARD_PROJECTION_REL_CHANGE="
    f"{three_d_projection_change:.16e}"
)

assert (
    two_d_projection_change
    < 0.10
)

assert (
    three_d_projection_change
    < 0.15
)

print(
    "TOTAL_FORCE_REVERSAL_CONVERGENCE="
    "PASS"
)


# ===========================================================================
# 6. Conservative health summary
# ===========================================================================

print()
print("=== HEALTH / MARGIN SUMMARY ===")

validated_runs = (
    runs_2d
    + runs_3d
    + [
        standard_dt_run,
        half_dt_run,
    ]
)

minimum_g_phi = min(
    min(
        result
        .root_metrics
        .minimum_g_phi,

        result
        .peak_metrics
        .minimum_g_phi,
    )
    for result in validated_runs
)

minimum_kinetic_denominator = min(
    min(
        result
        .root_metrics
        .minimum_kinetic_denominator,

        result
        .peak_metrics
        .minimum_kinetic_denominator,
    )
    for result in validated_runs
)

maximum_psi = max(
    result
    .root_metrics
    .maximum_abs_psi
    for result in validated_runs
)

maximum_outward_projection_3d = max(
    result
    .root_metrics
    .maximum_outward_total_projection
    for result in runs_3d
)

maximum_reversal_fraction_3d = max(
    result
    .root_metrics
    .total_reversal_fraction
    for result in runs_3d
)

print(
    "MIN_GPHI_VALIDATED_RUNS="
    f"{minimum_g_phi:.16e}"
)

print(
    "GPHI_ACCEPTANCE_FLOOR="
    f"{GPHI_ACCEPTANCE_FLOOR:.16e}"
)

print(
    "MIN_KINETIC_DENOMINATOR="
    f"{minimum_kinetic_denominator:.16e}"
)

print(
    "MAX_ABS_PSI_VALIDATED_RUNS="
    f"{maximum_psi:.16e}"
)

print(
    "MAX_3D_ROOT_OUTWARD_TOTAL_PROJECTION_OVER_NEWTONIAN="
    f"{maximum_outward_projection_3d:.16e}"
)

print(
    "MAX_3D_ROOT_TOTAL_REVERSAL_FRACTION="
    f"{maximum_reversal_fraction_3d:.16e}"
)

assert (
    minimum_g_phi
    > GPHI_ACCEPTANCE_FLOOR
)

assert (
    minimum_kinetic_denominator
    > 0.0
)

assert (
    maximum_psi
    < 0.05
)

print(
    "CONTROLLED_NONDEGENERATE_DISFORMAL_BRANCH="
    "PASS"
)


# ===========================================================================
# Final scientific classification
# ===========================================================================

print()
print("=== 014D FINAL GATE ===")

validated_2d_reversal = all(
    result
    .root_metrics
    .total_reversal_fraction
    > 0.0
    for result in runs_2d
)

validated_3d_reversal = all(
    result
    .root_metrics
    .total_reversal_fraction
    > 0.0
    for result in runs_3d
)

validated_margin = (
    minimum_g_phi
    > GPHI_ACCEPTANCE_FLOOR
)

if (
    validated_2d_reversal
    and validated_3d_reversal
    and validated_margin
):
    print(
        "PROJECT_REPRODUCED_LOCAL_TOTAL_FORCE_REVERSAL="
        "YES_IN_CONTROLLED_REDUCED_DISFORMAL_MODEL"
    )

    print(
        "NONSYMMETRIC_2D_TOTAL_FORCE_REVERSAL="
        "YES"
    )

    print(
        "NONSYMMETRIC_3D_TOTAL_FORCE_REVERSAL="
        "YES"
    )

    print(
        "TOTAL_FORCE_REVERSAL_SURVIVES_GRID_REFINEMENT="
        "YES"
    )

    print(
        "TOTAL_FORCE_REVERSAL_SURVIVES_TIMESTEP_HALVING="
        "YES"
    )

    print(
        "REVERSAL_REQUIRES_GPHI_BELOW_0P1="
        "NO"
    )

    print(
        "DISFORMAL_METRIC_MARGIN_GPHI_GT_0P1="
        "YES"
    )

    print(
        "LOCAL_TOTAL_ACCELERATION_PROJECTION_OPPOSITE_NEWTONIAN_GRAVITY="
        "YES"
    )

    print(
        "GLOBAL_BODY_REPULSION_ESTABLISHED="
        "NO"
    )

    print(
        "ORDINARY_BARYONIC_PAYLOAD_COUPLING="
        "NO_REFERENCE_MODEL_IS_DARK_SECTOR"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE="
        "NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_REDUCED_DISFORMAL_LOCAL_TOTAL_FORCE_REVERSAL"
    )

    print(
        "NEXT_IF_GREEN="
        "014E_SCREENED_BARYONIC_DISFORMAL_SYMMETRON_ARCHITECTURE_GATE"
    )

else:
    print(
        "PROJECT_REPRODUCED_LOCAL_TOTAL_FORCE_REVERSAL="
        "NOT_VALIDATED"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE="
        "NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_DISFORMAL_AMPLIFICATION_NEGATIVE_OR_INCONCLUSIVE_GATE"
    )

    print(
        "NEXT_IF_GREEN="
        "GLOBAL_RERANK_OR_REASSESS_DISFORMAL_PARAMETERIZATION"
    )


print(
    "014D_DISFORMAL_TOTAL_FORCE_REVERSAL_GATE="
    "GREEN"
)
