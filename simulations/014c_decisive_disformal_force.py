"""014C — decisive non-static disformal antiparallel-force gate.

PURPOSE
-------
Independently reproduce the directional repulsive fifth-force mechanism
reported for non-static disformally coupled quintessence, then immediately
test its weak-field scaling and whether it reverses the total acceleration.

SCIENTIFIC QUESTION
-------------------
014B independently reproduced the healthy background windows in which the
published coefficient xi_0 crosses zero. The reference paper reports that
its fully nonlinear 3D simulations develop fifth-force regions antiparallel
to Newtonian gravity near those crossings.

This gate asks four progressively stronger questions:

1. Can the project reproduce antiparallel fifth-force regions by evolving the
   full non-static beta=0 Klein-Gordon equation on an explicitly asymmetric
   density field rather than using the algebraic phi ~ xi_0 Psi ansatz?

2. Does the sign survive grid refinement and a genuine 3D control?

3. Does the matter-frame invertibility/stability condition g_phi > 0 remain
   satisfied in those regions?

4. Is the repulsive fifth force large enough to reverse the total force, or
   does it vanish parametrically in the weak-field limit near xi_0 = 0?

REFERENCE THEORY
----------------
Llinares, Hagala & Mota,
"Non-linear Phenomenology of Disformally Coupled Quintessence",
MNRAS 491, 1868-1886,
arXiv:1902.02125.

The matter-frame metric is

    gtilde_ab
        =
        g_ab
        + B(phi) phi_,a phi_,b.

The paper's Velocity-Flipping (VF) beta=0 model has

    v0 = 10,
    nu = 1,
    b0 = 0.1,
    beta = 0.

We use units

    H0 = M_Pl = c = 1,

so

    V0 = 10,
    B0 = 0.1.

For constant B, the weak-field scalar equation used by the reference paper is

    phi_ddot
        =
        [
            a^-2 Laplacian(phi)
            - 3 H phi_dot
            - V_,phi
        ]
        /
        [
            1 + gamma^2 rho
        ],

    gamma^2
        =
        B / g_phi,

    g_phi
        =
        1
        - B phi_dot^2
        + B a^-2 |grad phi|^2.

For

    V(phi)
        =
        V0 exp(-nu phi),

we have

    -V_,phi
        =
        nu V0 exp(-nu phi).

The force definitions are

    F_Psi
        =
        -grad(Psi)/a^2,

    F_phi
        =
        -(1/2)
        (xi/g_phi)
        grad(phi),

in these units, with beta=0

    xi
        =
        2 B phi_ddot.

Positive

    F_phi . F_Psi < 0

means the fifth force is locally antiparallel to gravity.

IMPORTANT PERTURBATIVE OBSERVATION
----------------------------------
At a homogeneous xi_0 = 0 crossing, introduce a regular spatial perturbation
parameter epsilon:

    phi
        =
        phi_0
        + epsilon phi_1
        + O(epsilon^2),

    Psi
        =
        epsilon Psi_1
        + O(epsilon^2),

    xi
        =
        epsilon xi_1
        + O(epsilon^2),

    g_phi
        =
        g_0
        + O(epsilon).

Then

    F_phi
        ~
        xi grad(phi)
        =
        O(epsilon^2),

while

    F_Psi
        =
        O(epsilon).

Therefore, in a smooth weak-field perturbative regime at the xi_0 crossing,

    |F_phi| / |F_Psi|
        =
        O(epsilon).

This does NOT forbid:

- nonperturbative enhancement;
- a singular limit;
- a screened extension;
- another disformal theory;
- an experimentally motivated new coupling structure.

It does mean that the same zero of xi_0 which permits local direction flips
can also suppress the force amplitude.

CONTROLLED DENSITY GEOMETRY
---------------------------
The reference publication used fully self-consistent cosmological N-body
simulations. Reproducing that entire code is beyond a single terminal gate.

Instead this calculation uses an imposed but physically admissible
Einstein-de Sitter growing-mode density field:

    delta(x,t)
        proportional to
        a(t).

Since

    rho_0
        proportional to
        a^-3,

Poisson's equation

    Laplacian(Psi)
        =
        a^2 delta_rho / 2

then gives a time-independent Psi.

This cleanly isolates the non-static scalar response from density-remeshing
artifacts.

The density pattern is:

- deterministic;
- positive in total density;
- strongly non-spherical;
- multi-mode;
- non-Gaussian.

The scalar initial perturbation is initialized using the published
first-order relation

    phi
        =
        phi_0
        + xi_0 Psi,

with its corresponding time derivative.

This avoids the zero-perturbation warm-up artifact discussed in the reference
simulations.

NUMERICAL METHOD
----------------
- Einstein-de Sitter background.
- High-accuracy DOP853 homogeneous background integration.
- Exact root finding for the physical beta=0 background phi_ddot=0 crossing.
- Periodic FFT Poisson solve for Psi.
- Second-order centered periodic finite differences.
- SSPRK3 explicit method-of-lines hyperbolic scalar evolution.
- 2D refinement:
      48^2,
      72^2,
      96^2,
      128^2.
- Independent 3D controls:
      24^3,
      32^3,
      40^3.
- Direct evaluation of the published F_Psi and F_phi expressions.
- Exact-root perturbation-amplitude scaling audit.

The 2D calculation is not advertised as a reproduction of the publication's
full 3D N-body simulation.

The 3D controls strengthen the force-sign result but still use imposed rather
than dynamically evolved matter.

VALIDATION / STOP RULES
-----------------------
A repulsion candidate is accepted only if:

- g_phi stays positive;
- |Psi| << 1;
- total matter density remains positive;
- a substantial antiparallel region exists at xi_0=0;
- the sign survives 2D refinement;
- the sign independently survives 3D refinement;
- the homogeneous scalar mean stays close to the independently integrated
  background;
- weak-amplitude scaling approaches

      F_phi ~ epsilon^2,

      F_Psi ~ epsilon.

A local antiparallel fifth force is NOT yet antigravity of an ordinary
payload.

Net force reversal requires

    |F_phi|
        >
        |F_Psi|

where the two forces are antiparallel.

ORDINARY-MATTER LIMITATION
--------------------------
The concrete reference model deliberately couples the disformal metric to
dark matter rather than ordinary baryons because it does not contain a
screening mechanism.

Thus a positive force-sign result here is a modified-gravity theoretical
result.

It is not yet a baryonic antigravity device.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_REDUCED_NONSTATIC_DISFORMAL_FORCE_REPRODUCTION_AND_SCALING_GATE
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import brentq


# ===========================================================================
# 0. Published VF model in H0 = M_Pl = c = 1 units
# ===========================================================================

B0 = 0.1
V0 = 10.0
NU = 1.0

T_START = 0.84
T_END = 1.20
BOX_L = 0.32


def scale_factor(time: float) -> float:
    """Return Einstein-de Sitter scale factor with H0=1."""

    return (1.5 * time) ** (2.0 / 3.0)


def hubble(time: float) -> float:
    """Return Einstein-de Sitter Hubble parameter with H0=1."""

    return 2.0 / (3.0 * time)


def background_density(time: float) -> float:
    """Return pressureless EdS density for M_Pl=H0=1."""

    return 3.0 / scale_factor(time) ** 3


print("=== VF MODEL AND EXACT FORCE DEFINITIONS ===")

print("VF_V0=1.0000000000000000e+01")
print("VF_NU=1.0000000000000000e+00")
print("VF_B0=1.0000000000000001e-01")
print("VF_BETA=0")

print(
    "UNITS="
    "H0_EQUALS_MPL_EQUALS_C_EQUALS_1"
)

print(
    "F_PSI="
    "MINUS_GRAD_PSI_OVER_A2"
)

print(
    "F_PHI="
    "MINUS_ONE_HALF_XI_OVER_GPHI_TIMES_GRAD_PHI"
)

print(
    "BETA0_XI="
    "2_B_PHI_DDOT"
)


# ===========================================================================
# 1. Exact weak-perturbation power counting at xi_0=0
# ===========================================================================

print()
print("=== XI0-ZERO PERTURBATIVE ORDER THEOREM ===")

epsilon = sp.symbols(
    "epsilon",
    positive=True,
    real=True,
)

g0, xi1, grad_phi1, grad_psi1 = sp.symbols(
    "g0 xi1 grad_phi1 grad_psi1",
    nonzero=True,
    finite=True,
    real=True,
)

f_phi_order = sp.simplify(
    (
        epsilon
        * xi1
    )
    * (
        epsilon
        * grad_phi1
    )
    / g0
)

f_psi_order = sp.simplify(
    epsilon
    * grad_psi1
)

ratio_order = sp.simplify(
    f_phi_order
    / f_psi_order
)

print(
    "F_PHI_LEADING_ORDER="
    f"{sp.sstr(f_phi_order)}"
)

print(
    "F_PSI_LEADING_ORDER="
    f"{sp.sstr(f_psi_order)}"
)

print(
    "FORCE_RATIO_LEADING_ORDER="
    f"{sp.sstr(ratio_order)}"
)

assert sp.degree(
    sp.Poly(
        sp.expand(
            f_phi_order
        ),
        epsilon,
    )
) == 2

assert sp.degree(
    sp.Poly(
        sp.expand(
            f_psi_order
        ),
        epsilon,
    )
) == 1

assert sp.degree(
    sp.Poly(
        sp.expand(
            ratio_order
        ),
        epsilon,
    )
) == 1

print(
    "XI0_ZERO_F_PHI_PERTURBATIVE_ORDER="
    "EPSILON_SQUARED"
)

print(
    "XI0_ZERO_F_PSI_PERTURBATIVE_ORDER="
    "EPSILON"
)

print(
    "XI0_ZERO_FORCE_RATIO_PERTURBATIVE_ORDER="
    "EPSILON"
)


# ===========================================================================
# 2. Exact homogeneous beta=0 background and xi_0 root
# ===========================================================================

print()
print("=== EXACT HOMOGENEOUS VF BACKGROUND ===")


def background_rhs(
    time: float,
    state: np.ndarray,
) -> np.ndarray:
    """Return (phi_dot, phi_ddot) from the beta=0 reference equation."""

    phi_value = float(
        state[0]
    )

    phi_dot = float(
        state[1]
    )

    H = hubble(
        time
    )

    rho0 = background_density(
        time
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

    phi_ddot = (
        -3.0
        * H
        * phi_dot
        + NU
        * V0
        * math.exp(
            -NU
            * phi_value
        )
    ) / (
        1.0
        + gamma_squared
        * rho0
    )

    return np.array(
        [
            phi_dot,
            phi_ddot,
        ],
        dtype=float,
    )


background_solution = solve_ivp(
    background_rhs,
    (
        1.0e-5,
        1.35,
    ),
    (
        0.0,
        0.0,
    ),
    method="DOP853",
    rtol=2.0e-12,
    atol=2.0e-14,
    max_step=0.002,
    dense_output=True,
)

assert background_solution.success


def background_acceleration(
    time: float,
) -> float:
    """Return homogeneous phi_ddot."""

    return float(
        background_rhs(
            time,
            background_solution.sol(
                time
            ),
        )[1]
    )


root_search_grid = np.linspace(
    0.2,
    1.3,
    4000,
)

root_search_values = np.array(
    [
        background_acceleration(
            time
        )
        for time in root_search_grid
    ]
)

crossings = np.where(
    root_search_values[:-1]
    * root_search_values[1:]
    < 0.0
)[0]

assert len(
    crossings
) >= 1

root_index = int(
    crossings[0]
)

T_XI_ZERO = brentq(
    background_acceleration,
    float(
        root_search_grid[
            root_index
        ]
    ),
    float(
        root_search_grid[
            root_index + 1
        ]
    ),
    xtol=1.0e-14,
    rtol=1.0e-14,
)

phi_root_background = float(
    background_solution.sol(
        T_XI_ZERO
    )[0]
)

phi_dot_root_background = float(
    background_solution.sol(
        T_XI_ZERO
    )[1]
)

background_g_phi_root = (
    1.0
    - B0
    * phi_dot_root_background**2
)

print(
    "T_XI0_ZERO_H0_UNITS="
    f"{T_XI_ZERO:.16e}"
)

print(
    "PHI_BACKGROUND_AT_XI0_ZERO="
    f"{phi_root_background:.16e}"
)

print(
    "PHI_DOT_BACKGROUND_AT_XI0_ZERO="
    f"{phi_dot_root_background:.16e}"
)

print(
    "BACKGROUND_G_PHI_AT_XI0_ZERO="
    f"{background_g_phi_root:.16e}"
)

print(
    "BACKGROUND_PHI_DDOT_AT_ROOT="
    f"{background_acceleration(T_XI_ZERO):+.16e}"
)

assert (
    background_g_phi_root
    > 0.0
)

assert abs(
    background_acceleration(
        T_XI_ZERO
    )
) < 1.0e-12

print(
    "HEALTHY_BACKGROUND_XI0_ZERO="
    "YES"
)


# ===========================================================================
# 3. Numerical utilities
# ===========================================================================


def background_xi_dot(
    time: float,
) -> float:
    """Return d(xi_0)/dt for matched initial perturbations."""

    dt = 2.0e-5

    d_acceleration_dt = (
        background_acceleration(
            time + dt
        )
        - background_acceleration(
            time - dt
        )
    ) / (
        2.0
        * dt
    )

    return (
        2.0
        * B0
        * d_acceleration_dt
    )


def derivatives_nd(
    field: np.ndarray,
    spacing: float,
) -> tuple[
    list[np.ndarray],
    np.ndarray,
]:
    """Return centered periodic gradient components and Laplacian."""

    gradients: list[
        np.ndarray
    ] = []

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
    delta_at_root: np.ndarray,
    box_length: float,
) -> np.ndarray:
    """Solve the periodic Poisson equation at the xi_0 crossing."""

    shape = (
        delta_at_root.shape
    )

    dimension = (
        delta_at_root.ndim
    )

    points = (
        shape[0]
    )

    a = scale_factor(
        T_XI_ZERO
    )

    rho0 = background_density(
        T_XI_ZERO
    )

    source = (
        a**2
        * rho0
        * delta_at_root
        / 2.0
    )

    source_hat = np.fft.fftn(
        source
    )

    frequency = (
        2.0
        * math.pi
        * np.fft.fftfreq(
            points,
            d=box_length
            / points,
        )
    )

    meshes = np.meshgrid(
        *(
            [
                frequency
            ]
            * dimension
        ),
        indexing="ij",
    )

    k_squared = np.zeros(
        shape,
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
# 4. Deterministic asymmetric density fields
# ===========================================================================


def density_shape_2d(
    points: int,
    box_length: float,
) -> np.ndarray:
    """Return deterministic positive-density 2D asymmetric contrast."""

    coordinate = (
        np.arange(
            points,
            dtype=float,
        )
        * box_length
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
        / box_length
    )

    v = (
        2.0
        * math.pi
        * y
        / box_length
    )

    raw = (
        0.95
        * np.cos(
            u + 0.17
        )
        + 0.70
        * np.sin(
            v - 0.41
        )
        + 0.55
        * np.cos(
            u
            + 2.0
            * v
            + 0.73
        )
        + 0.42
        * np.sin(
            2.0
            * u
            - v
            + 1.31
        )
        + 0.33
        * np.cos(
            3.0
            * u
            + v
            - 0.62
        )
        + 0.27
        * np.sin(
            u
            - 3.0
            * v
            + 0.28
        )
        + 0.20
        * np.cos(
            2.0
            * u
            + 3.0
            * v
            + 2.0
        )
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
    box_length: float,
) -> np.ndarray:
    """Return deterministic positive-density 3D asymmetric contrast."""

    coordinate = (
        np.arange(
            points,
            dtype=float,
        )
        * box_length
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
        / box_length
    )

    v = (
        2.0
        * math.pi
        * y
        / box_length
    )

    w = (
        2.0
        * math.pi
        * z
        / box_length
    )

    raw = (
        0.80
        * np.cos(
            u + 0.17
        )
        + 0.65
        * np.sin(
            v - 0.41
        )
        + 0.55
        * np.cos(
            w + 0.90
        )
        + 0.45
        * np.cos(
            u
            + 2.0
            * v
            - w
            + 0.73
        )
        + 0.35
        * np.sin(
            2.0
            * u
            - v
            + 2.0
            * w
            + 1.31
        )
        + 0.28
        * np.cos(
            3.0
            * u
            + v
            + w
            - 0.62
        )
        + 0.22
        * np.sin(
            u
            - 3.0
            * v
            + 2.0
            * w
            + 0.28
        )
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
# 5. Full non-static scalar solver
# ===========================================================================


@dataclass
class ForceMetrics:
    """Diagnostics for one spatial field snapshot."""

    time: float
    minimum_g_phi: float
    maximum_abs_psi: float
    repulsive_fraction: float
    strongly_antiparallel_fraction: float
    minimum_force_cosine: float
    maximum_repulsive_force_ratio: float
    rms_force_ratio: float
    local_total_force_reversal: bool
    background_mean_relative_error: float


@dataclass
class SpatialRun:
    """Output required for convergence and root-scaling audits."""

    dimension: int
    points: int
    root_metrics: ForceMetrics
    peak_repulsive_metrics: ForceMetrics
    root_phi: np.ndarray
    root_phi_dot: np.ndarray
    density_contrast_root: np.ndarray
    psi: np.ndarray
    spacing: float


def run_spatial_case(
    *,
    dimension: int,
    points: int,
    box_length: float = BOX_L,
) -> SpatialRun:
    """Evolve the exact beta=0 KG equation in 2D or 3D geometry."""

    if dimension == 2:
        density_contrast_root = density_shape_2d(
            points,
            box_length,
        )

    elif dimension == 3:
        density_contrast_root = density_shape_3d(
            points,
            box_length,
        )

    else:
        raise ValueError(
            "dimension must be 2 or 3"
        )

    spacing = (
        box_length
        / points
    )

    psi = poisson_periodic(
        density_contrast_root,
        box_length,
    )

    (
        psi_gradients,
        _,
    ) = derivatives_nd(
        psi,
        spacing,
    )

    initial_background = (
        background_solution.sol(
            T_START
        )
    )

    initial_phi_background = float(
        initial_background[0]
    )

    initial_phi_dot_background = float(
        initial_background[1]
    )

    initial_xi = (
        2.0
        * B0
        * background_acceleration(
            T_START
        )
    )

    initial_xi_dot = (
        background_xi_dot(
            T_START
        )
    )

    phi = (
        np.full(
            density_contrast_root.shape,
            initial_phi_background,
            dtype=float,
        )
        + initial_xi
        * psi
    )

    phi_dot = (
        np.full(
            density_contrast_root.shape,
            initial_phi_dot_background,
            dtype=float,
        )
        + initial_xi_dot
        * psi
    )

    a_root = scale_factor(
        T_XI_ZERO
    )

    def rhs(
        time: float,
        current_phi: np.ndarray,
        current_phi_dot: np.ndarray,
    ):
        """Return exact beta=0 non-static scalar evolution."""

        a = scale_factor(
            time
        )

        H = hubble(
            time
        )

        rho0 = background_density(
            time
        )

        contrast = (
            density_contrast_root
            * a
            / a_root
        )

        density = (
            rho0
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
        ) / (
            1.0
            + gamma_squared
            * density
        )

        return (
            current_phi_dot,
            phi_ddot,
            g_phi,
            gradients,
        )

    def force_metrics(
        time: float,
        current_phi: np.ndarray,
        current_phi_dot: np.ndarray,
    ) -> ForceMetrics:
        """Evaluate the published Newtonian and disformal force fields."""

        a = scale_factor(
            time
        )

        (
            _,
            phi_ddot,
            g_phi,
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

        fifth_force_components = []
        gravity_components = []

        for (
            phi_gradient,
            psi_gradient,
        ) in zip(
            gradients,
            psi_gradients,
        ):
            fifth_force_components.append(
                -0.5
                * (
                    xi
                    / g_phi
                )
                * phi_gradient
            )

            gravity_components.append(
                -psi_gradient
                / a**2
            )

        fifth_force_squared = np.zeros_like(
            current_phi
        )

        gravity_squared = np.zeros_like(
            current_phi
        )

        force_dot = np.zeros_like(
            current_phi
        )

        for (
            fifth_component,
            gravity_component,
        ) in zip(
            fifth_force_components,
            gravity_components,
        ):
            fifth_force_squared += (
                fifth_component**2
            )

            gravity_squared += (
                gravity_component**2
            )

            force_dot += (
                fifth_component
                * gravity_component
            )

        fifth_magnitude = np.sqrt(
            fifth_force_squared
        )

        gravity_magnitude = np.sqrt(
            gravity_squared
        )

        gravity_mask = (
            gravity_magnitude
            > 0.05
            * float(
                np.max(
                    gravity_magnitude
                )
            )
        )

        direction_mask = (
            gravity_mask
            & (
                fifth_magnitude
                > 1.0e-18
            )
        )

        cosine = np.zeros_like(
            current_phi
        )

        cosine[
            direction_mask
        ] = (
            force_dot[
                direction_mask
            ]
            / (
                fifth_magnitude[
                    direction_mask
                ]
                * gravity_magnitude[
                    direction_mask
                ]
            )
        )

        repulsive_mask = (
            direction_mask
            & (
                force_dot
                < 0.0
            )
        )

        strongly_antiparallel_mask = (
            direction_mask
            & (
                cosine
                < -0.5
            )
        )

        force_ratio = np.zeros_like(
            current_phi
        )

        force_ratio[
            gravity_mask
        ] = (
            fifth_magnitude[
                gravity_mask
            ]
            / gravity_magnitude[
                gravity_mask
            ]
        )

        rms_force_ratio = (
            math.sqrt(
                float(
                    np.mean(
                        fifth_force_squared[
                            gravity_mask
                        ]
                    )
                )
            )
            / math.sqrt(
                float(
                    np.mean(
                        gravity_squared[
                            gravity_mask
                        ]
                    )
                )
            )
        )

        homogeneous_phi = float(
            background_solution.sol(
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
                - homogeneous_phi
            )
            / max(
                abs(
                    homogeneous_phi
                ),
                1.0e-12,
            )
        )

        return ForceMetrics(
            time=time,
            minimum_g_phi=float(
                np.min(
                    g_phi
                )
            ),
            maximum_abs_psi=float(
                np.max(
                    np.abs(
                        psi
                    )
                )
            ),
            repulsive_fraction=float(
                np.sum(
                    repulsive_mask
                )
                / np.sum(
                    gravity_mask
                )
            ),
            strongly_antiparallel_fraction=float(
                np.sum(
                    strongly_antiparallel_mask
                )
                / np.sum(
                    gravity_mask
                )
            ),
            minimum_force_cosine=float(
                np.min(
                    cosine[
                        direction_mask
                    ]
                )
            ),
            maximum_repulsive_force_ratio=(
                float(
                    np.max(
                        force_ratio[
                            repulsive_mask
                        ]
                    )
                )
                if np.any(
                    repulsive_mask
                )
                else 0.0
            ),
            rms_force_ratio=(
                rms_force_ratio
            ),
            local_total_force_reversal=bool(
                np.any(
                    repulsive_mask
                    & (
                        force_ratio
                        > 1.0
                    )
                )
            ),
            background_mean_relative_error=(
                background_mean_relative_error
            ),
        )

    records = [
        force_metrics(
            T_START,
            phi,
            phi_dot,
        )
    ]

    def evolve_segment(
        start_time: float,
        end_time: float,
        current_phi: np.ndarray,
        current_phi_dot: np.ndarray,
    ):
        """Advance one interval with SSPRK3 and land exactly on endpoint."""

        duration = (
            end_time
            - start_time
        )

        maximum_dt = (
            0.18
            * spacing
            * scale_factor(
                start_time
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
            // 120,
        )

        for step in range(
            number_of_steps
        ):
            time = (
                start_time
                + step
                * dt
            )

            (
                k_phi,
                k_p,
                _,
                _,
            ) = rhs(
                time,
                current_phi,
                current_phi_dot,
            )

            phi_stage_1 = (
                current_phi
                + dt
                * k_phi
            )

            p_stage_1 = (
                current_phi_dot
                + dt
                * k_p
            )

            (
                l_phi,
                l_p,
                _,
                _,
            ) = rhs(
                time + dt,
                phi_stage_1,
                p_stage_1,
            )

            phi_stage_2 = (
                0.75
                * current_phi
                + 0.25
                * (
                    phi_stage_1
                    + dt
                    * l_phi
                )
            )

            p_stage_2 = (
                0.75
                * current_phi_dot
                + 0.25
                * (
                    p_stage_1
                    + dt
                    * l_p
                )
            )

            (
                m_phi,
                m_p,
                _,
                _,
            ) = rhs(
                time
                + 0.5
                * dt,
                phi_stage_2,
                p_stage_2,
            )

            current_phi = (
                current_phi
                / 3.0
                + 2.0
                / 3.0
                * (
                    phi_stage_2
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
                    p_stage_2
                    + dt
                    * m_p
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
                records.append(
                    force_metrics(
                        time + dt,
                        current_phi,
                        current_phi_dot,
                    )
                )

        return (
            current_phi,
            current_phi_dot,
        )

    # Land exactly on the xi_0 zero.
    phi, phi_dot = evolve_segment(
        T_START,
        T_XI_ZERO,
        phi,
        phi_dot,
    )

    root_phi = np.array(
        phi,
        copy=True,
    )

    root_phi_dot = np.array(
        phi_dot,
        copy=True,
    )

    root_metrics = force_metrics(
        T_XI_ZERO,
        phi,
        phi_dot,
    )

    records.append(
        root_metrics
    )

    phi, phi_dot = evolve_segment(
        T_XI_ZERO,
        T_END,
        phi,
        phi_dot,
    )

    peak_repulsive_metrics = max(
        records,
        key=lambda result:
            result.maximum_repulsive_force_ratio,
    )

    return SpatialRun(
        dimension=dimension,
        points=points,
        root_metrics=root_metrics,
        peak_repulsive_metrics=(
            peak_repulsive_metrics
        ),
        root_phi=root_phi,
        root_phi_dot=root_phi_dot,
        density_contrast_root=(
            density_contrast_root
        ),
        psi=psi,
        spacing=spacing,
    )


# ===========================================================================
# 6. 2D refinement sequence
# ===========================================================================

print()
print("=== 2D NONSTATIC ASYMMETRIC REFINEMENT ===")

runs_2d = [
    run_spatial_case(
        dimension=2,
        points=points,
    )
    for points in [
        48,
        72,
        96,
        128,
    ]
]

for result in runs_2d:
    root = (
        result.root_metrics
    )

    peak = (
        result.peak_repulsive_metrics
    )

    print(
        "GRID="
        f"{result.points}x{result.points} "
        "ROOT_MIN_GPHI="
        f"{root.minimum_g_phi:.16e} "
        "ROOT_MAX_ABS_PSI="
        f"{root.maximum_abs_psi:.16e} "
        "ROOT_REPULSIVE_FRACTION="
        f"{root.repulsive_fraction:.16e} "
        "ROOT_STRONG_ANTIPARALLEL_FRACTION="
        f"{root.strongly_antiparallel_fraction:.16e} "
        "ROOT_MIN_COS="
        f"{root.minimum_force_cosine:+.16e} "
        "ROOT_MAX_REPULSIVE_RATIO="
        f"{root.maximum_repulsive_force_ratio:.16e} "
        "ROOT_RMS_FORCE_RATIO="
        f"{root.rms_force_ratio:.16e} "
        "ROOT_NET_REVERSAL="
        + (
            "YES"
            if root.local_total_force_reversal
            else "NO"
        )
    )

    print(
        "GRID="
        f"{result.points}x{result.points} "
        "PEAK_TIME="
        f"{peak.time:.16e} "
        "PEAK_REPULSIVE_F5_OVER_FN="
        f"{peak.maximum_repulsive_force_ratio:.16e} "
        "PEAK_MIN_COS="
        f"{peak.minimum_force_cosine:+.16e}"
    )

for result in runs_2d:
    root = (
        result.root_metrics
    )

    assert (
        root.minimum_g_phi
        > 0.0
    )

    assert (
        root.maximum_abs_psi
        < 0.05
    )

    assert (
        root.repulsive_fraction
        > 0.30
    )

    assert (
        root.strongly_antiparallel_fraction
        > 0.25
    )

    assert (
        root.minimum_force_cosine
        < -0.95
    )

    assert not (
        root.local_total_force_reversal
    )

    assert (
        root.background_mean_relative_error
        < 1.0e-3
    )

last_2d = (
    runs_2d[-1]
    .root_metrics
)

previous_2d = (
    runs_2d[-2]
    .root_metrics
)

rms_ratio_refinement_change_2d = (
    abs(
        last_2d.rms_force_ratio
        - previous_2d.rms_force_ratio
    )
    / last_2d.rms_force_ratio
)

print(
    "2D_HIGH_GRID_ROOT_RMS_RATIO_REL_CHANGE="
    f"{rms_ratio_refinement_change_2d:.16e}"
)

assert (
    rms_ratio_refinement_change_2d
    < 0.05
)

print(
    "2D_ANTIPARALLEL_SIGN_REFINEMENT_STABLE="
    "YES"
)


# ===========================================================================
# 7. Independent 3D control
# ===========================================================================

print()
print("=== 3D NONSTATIC ASYMMETRIC CONTROL ===")

runs_3d = [
    run_spatial_case(
        dimension=3,
        points=points,
    )
    for points in [
        24,
        32,
        40,
    ]
]

for result in runs_3d:
    root = (
        result.root_metrics
    )

    print(
        "GRID="
        f"{result.points}x"
        f"{result.points}x"
        f"{result.points} "
        "ROOT_MIN_GPHI="
        f"{root.minimum_g_phi:.16e} "
        "ROOT_MAX_ABS_PSI="
        f"{root.maximum_abs_psi:.16e} "
        "ROOT_REPULSIVE_FRACTION="
        f"{root.repulsive_fraction:.16e} "
        "ROOT_STRONG_ANTIPARALLEL_FRACTION="
        f"{root.strongly_antiparallel_fraction:.16e} "
        "ROOT_MIN_COS="
        f"{root.minimum_force_cosine:+.16e} "
        "ROOT_MAX_REPULSIVE_RATIO="
        f"{root.maximum_repulsive_force_ratio:.16e} "
        "ROOT_RMS_FORCE_RATIO="
        f"{root.rms_force_ratio:.16e} "
        "ROOT_NET_REVERSAL="
        + (
            "YES"
            if root.local_total_force_reversal
            else "NO"
        )
    )

for result in runs_3d:
    root = (
        result.root_metrics
    )

    assert (
        root.minimum_g_phi
        > 0.0
    )

    assert (
        root.maximum_abs_psi
        < 0.05
    )

    assert (
        root.repulsive_fraction
        > 0.30
    )

    assert (
        root.strongly_antiparallel_fraction
        > 0.25
    )

    assert (
        root.minimum_force_cosine
        < -0.95
    )

    assert not (
        root.local_total_force_reversal
    )

    assert (
        root.background_mean_relative_error
        < 2.0e-3
    )

last_3d = (
    runs_3d[-1]
    .root_metrics
)

previous_3d = (
    runs_3d[-2]
    .root_metrics
)

rms_ratio_refinement_change_3d = (
    abs(
        last_3d.rms_force_ratio
        - previous_3d.rms_force_ratio
    )
    / last_3d.rms_force_ratio
)

print(
    "3D_HIGH_GRID_ROOT_RMS_RATIO_REL_CHANGE="
    f"{rms_ratio_refinement_change_3d:.16e}"
)

assert (
    rms_ratio_refinement_change_3d
    < 0.10
)

print(
    "3D_ANTIPARALLEL_SIGN_REFINEMENT_STABLE="
    "YES"
)


# ===========================================================================
# 8. Source positivity and weak-field checks
# ===========================================================================

print()
print("=== SOURCE AND WEAK-FIELD VALIDATION ===")

reference_2d = (
    runs_2d[2]
)

minimum_delta_root = float(
    np.min(
        reference_2d
        .density_contrast_root
    )
)

maximum_delta_root = float(
    np.max(
        reference_2d
        .density_contrast_root
    )
)

minimum_total_density_factor_end = (
    1.0
    + minimum_delta_root
    * scale_factor(
        T_END
    )
    / scale_factor(
        T_XI_ZERO
    )
)

print(
    "ROOT_MIN_DELTA="
    f"{minimum_delta_root:.16e}"
)

print(
    "ROOT_MAX_DELTA="
    f"{maximum_delta_root:.16e}"
)

print(
    "END_MIN_RHO_OVER_BACKGROUND="
    f"{minimum_total_density_factor_end:.16e}"
)

print(
    "REFERENCE_2D_MAX_ABS_PSI="
    f"{reference_2d.root_metrics.maximum_abs_psi:.16e}"
)

assert (
    minimum_total_density_factor_end
    > 0.0
)

assert (
    reference_2d
    .root_metrics
    .maximum_abs_psi
    < 0.05
)

print(
    "TOTAL_MATTER_DENSITY_POSITIVE="
    "YES"
)

print(
    "NEWTONIAN_WEAK_FIELD_CONDITION="
    "PASS"
)

print(
    "INITIAL_PERTURBATION_MATCHED_TO_PUBLISHED_LINEAR_RELATION="
    "YES"
)


# ===========================================================================
# 9. Exact-root amplitude scaling audit
# ===========================================================================

print()
print("=== XI0-ZERO NUMERICAL AMPLITUDE SCALING ===")

root_phi = (
    reference_2d.root_phi
)

root_phi_dot = (
    reference_2d.root_phi_dot
)

density_contrast_root = (
    reference_2d
    .density_contrast_root
)

psi = (
    reference_2d.psi
)

spacing = (
    reference_2d.spacing
)

(
    psi_gradients,
    _,
) = derivatives_nd(
    psi,
    spacing,
)

a_root = scale_factor(
    T_XI_ZERO
)

H_root = hubble(
    T_XI_ZERO
)

rho0_root = background_density(
    T_XI_ZERO
)

phi0_root = float(
    background_solution.sol(
        T_XI_ZERO
    )[0]
)

phi_dot0_root = float(
    background_solution.sol(
        T_XI_ZERO
    )[1]
)

scaling_epsilons = [
    1.0,
    0.5,
    0.25,
    0.125,
    0.0625,
    0.03125,
    0.015625,
    0.0078125,
    0.00390625,
]

scaling_fifth_rms = []
scaling_gravity_rms = []

for scaling_epsilon in scaling_epsilons:
    scaled_phi = (
        phi0_root
        + scaling_epsilon
        * (
            root_phi
            - phi0_root
        )
    )

    scaled_phi_dot = (
        phi_dot0_root
        + scaling_epsilon
        * (
            root_phi_dot
            - phi_dot0_root
        )
    )

    scaled_density = (
        rho0_root
        * (
            1.0
            + scaling_epsilon
            * density_contrast_root
        )
    )

    (
        gradients,
        laplacian,
    ) = derivatives_nd(
        scaled_phi,
        spacing,
    )

    gradient_squared = np.zeros_like(
        scaled_phi
    )

    for component in gradients:
        gradient_squared += (
            component**2
        )

    g_phi = (
        1.0
        + B0
        * (
            -scaled_phi_dot**2
            + gradient_squared
            / a_root**2
        )
    )

    gamma_squared = (
        B0
        / g_phi
    )

    phi_ddot = (
        laplacian
        / a_root**2
        - 3.0
        * H_root
        * scaled_phi_dot
        + NU
        * V0
        * np.exp(
            -NU
            * scaled_phi
        )
    ) / (
        1.0
        + gamma_squared
        * scaled_density
    )

    xi = (
        2.0
        * B0
        * phi_ddot
    )

    fifth_force_squared = np.zeros_like(
        scaled_phi
    )

    gravity_squared = np.zeros_like(
        scaled_phi
    )

    for (
        phi_gradient,
        psi_gradient,
    ) in zip(
        gradients,
        psi_gradients,
    ):
        fifth_component = (
            -0.5
            * (
                xi
                / g_phi
            )
            * phi_gradient
        )

        gravity_component = (
            -scaling_epsilon
            * psi_gradient
            / a_root**2
        )

        fifth_force_squared += (
            fifth_component**2
        )

        gravity_squared += (
            gravity_component**2
        )

    fifth_rms = math.sqrt(
        float(
            np.mean(
                fifth_force_squared
            )
        )
    )

    gravity_rms = math.sqrt(
        float(
            np.mean(
                gravity_squared
            )
        )
    )

    scaling_fifth_rms.append(
        fifth_rms
    )

    scaling_gravity_rms.append(
        gravity_rms
    )

    print(
        "EPSILON="
        f"{scaling_epsilon:.9f} "
        "RMS_F_PHI="
        f"{fifth_rms:.16e} "
        "RMS_F_PSI="
        f"{gravity_rms:.16e} "
        "RMS_RATIO="
        f"{fifth_rms/gravity_rms:.16e} "
        "MIN_GPHI="
        f"{float(np.min(g_phi)):.16e}"
    )

fit_count = 5

fit_epsilon = np.array(
    scaling_epsilons[
        -fit_count:
    ],
    dtype=float,
)

fit_fifth = np.array(
    scaling_fifth_rms[
        -fit_count:
    ],
    dtype=float,
)

fit_gravity = np.array(
    scaling_gravity_rms[
        -fit_count:
    ],
    dtype=float,
)

fifth_force_power = float(
    np.polyfit(
        np.log(
            fit_epsilon
        ),
        np.log(
            fit_fifth
        ),
        1,
    )[0]
)

gravity_force_power = float(
    np.polyfit(
        np.log(
            fit_epsilon
        ),
        np.log(
            fit_gravity
        ),
        1,
    )[0]
)

ratio_power = float(
    np.polyfit(
        np.log(
            fit_epsilon
        ),
        np.log(
            fit_fifth
            / fit_gravity
        ),
        1,
    )[0]
)

print(
    "ASYMPTOTIC_F_PHI_POWER="
    f"{fifth_force_power:.16e}"
)

print(
    "ASYMPTOTIC_F_PSI_POWER="
    f"{gravity_force_power:.16e}"
)

print(
    "ASYMPTOTIC_FORCE_RATIO_POWER="
    f"{ratio_power:.16e}"
)

assert (
    1.95
    < fifth_force_power
    < 2.05
)

assert (
    0.99
    < gravity_force_power
    < 1.01
)

assert (
    0.95
    < ratio_power
    < 1.05
)

print(
    "XI0_ZERO_SECOND_ORDER_FIFTH_FORCE_NUMERICALLY_CONFIRMED="
    "YES"
)

print(
    "XI0_ZERO_FIRST_ORDER_NEWTONIAN_FORCE_NUMERICALLY_CONFIRMED="
    "YES"
)

print(
    "XI0_ZERO_REPULSION_TO_GRAVITY_RATIO_VANISHES_IN_WEAK_LIMIT="
    "YES"
)


# ===========================================================================
# 10. Practical force-sign interpretation
# ===========================================================================

print()
print("=== PRACTICAL FORCE-SIGN INTERPRETATION ===")

all_runs = (
    runs_2d
    + runs_3d
)

minimum_g_phi_all = min(
    result
    .root_metrics
    .minimum_g_phi
    for result in all_runs
)

maximum_root_rms_ratio = max(
    result
    .root_metrics
    .rms_force_ratio
    for result in all_runs
)

maximum_repulsive_ratio_any_time = max(
    result
    .peak_repulsive_metrics
    .maximum_repulsive_force_ratio
    for result in all_runs
)

any_total_reversal = any(
    result
    .root_metrics
    .local_total_force_reversal
    or result
    .peak_repulsive_metrics
    .local_total_force_reversal
    for result in all_runs
)

print(
    "MIN_GPHI_ALL_REFINEMENT_RUNS="
    f"{minimum_g_phi_all:.16e}"
)

print(
    "MAX_ROOT_RMS_F5_OVER_FN="
    f"{maximum_root_rms_ratio:.16e}"
)

print(
    "MAX_REPULSIVE_F5_OVER_FN_ANY_TESTED_MEANINGFUL_POINT="
    f"{maximum_repulsive_ratio_any_time:.16e}"
)

print(
    "TOTAL_FORCE_REVERSAL_FOUND="
    + (
        "YES"
        if any_total_reversal
        else "NO"
    )
)

assert (
    minimum_g_phi_all
    > 0.0
)

assert not (
    any_total_reversal
)

print(
    "HEALTHY_GPHI_ANTIPARALLEL_FIFTH_FORCE="
    "YES"
)

print(
    "NET_GRAVITY_PLUS_FIFTH_FORCE_REVERSAL_IN_TESTED_VF_CONFIGURATION="
    "NO"
)


# ===========================================================================
# 11. Final scientific classification
# ===========================================================================

print()
print("=== 014C FINAL GATE ===")

print(
    "PUBLISHED_NONSTATIC_BETA0_KG_EQUATION="
    "USED_WITHOUT_QUASISTATIC_APPROXIMATION"
)

print(
    "PUBLISHED_FIFTH_FORCE_DEFINITION="
    "USED"
)

print(
    "ZERO_PERTURBATION_WARMUP_INITIALIZATION="
    "AVOIDED"
)

print(
    "NONSYMMETRIC_2D_ANTIPARALLEL_FIFTH_FORCE="
    "REPRODUCED"
)

print(
    "NONSYMMETRIC_3D_ANTIPARALLEL_FIFTH_FORCE="
    "REPRODUCED"
)

print(
    "ANTIPARALLEL_SIGN_SURVIVES_REFINEMENT="
    "YES"
)

print(
    "DISFORMAL_METRIC_INVERTIBILITY_GPHI_POSITIVE="
    "YES"
)

print(
    "XI0_ZERO_REPULSIVE_CHANNEL_IS_SECOND_ORDER_IN_WEAK_PERTURBATIONS="
    "YES"
)

print(
    "NEWTONIAN_GRAVITY_REMAINS_FIRST_ORDER="
    "YES"
)

print(
    "TESTED_REFERENCE_MODEL_TOTAL_FORCE_SIGN_REVERSAL="
    "NO"
)

print(
    "REFERENCE_MODEL_COUPLES_ORDINARY_BARYONS="
    "NO"
)

print(
    "REFERENCE_MODEL_COUPLES_DARK_MATTER="
    "YES"
)

print(
    "SCREENED_BARYONIC_EXTENSION_REQUIRED_FOR_ORDINARY_PAYLOAD="
    "YES"
)

print(
    "PRACTICAL_BARYONIC_ANTIGRAVITY_DEVICE="
    "NO"
)

print(
    "UNKNOWN_NONPERTURBATIVE_DISFORMAL_ENHANCEMENT_GENERAL_NO_GO="
    "NO"
)

print(
    "PROJECT_REPRODUCED_DISFORMAL_REPULSIVE_FIFTH_FORCE_MECHANISM="
    "YES_IN_CONTROLLED_REDUCED_MODEL"
)

print(
    "CLAIM_CLASSIFICATION="
    "PROJECT_DERIVED_REDUCED_NONSTATIC_DISFORMAL_FORCE_REPRODUCTION_AND_SCALING_GATE"
)

print(
    "NEXT_IF_RESEARCH_CONTINUES="
    "SCREENED_BARYONIC_NONPERTURBATIVE_DISFORMAL_EXTENSION_MUST_BE_SPECIFIED_BEFORE_MORE_NUMERICS"
)

print(
    "014C_DECISIVE_DISFORMAL_FORCE_GATE="
    "GREEN"
)
