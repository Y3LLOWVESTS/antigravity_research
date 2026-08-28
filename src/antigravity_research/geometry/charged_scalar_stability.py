"""Fixed-charge canonical-scalar stability-capacity gate for 006D.

PURPOSE
-------
Determine whether the exact finite 006D stress tensor has enough pointwise
canonical-field kinetic freedom for a conserved-charge / stationary
time-dependent scalar sector to reverse the negative Derrick dilation mode
found in Simulation 008B.

SCIENTIFIC QUESTION
-------------------
Simulation 008B showed two things:

1. the 006D stress tensor is locally compatible with canonical positive-sign
   scalar gradient energy;

2. every purely static canonical multi-scalar realization of the exact
   Laue-balanced stress tensor has a negative uniform Derrick mode.

The cheapest known scalar-field mechanism that can evade the ordinary static
Derrick argument is stationary phase rotation carrying a conserved U(1)-like
charge, as in Q-balls.

This module does NOT construct a Q-ball.  It asks a prior necessary question:

    Does the exact 006D stress tensor even contain enough local stress-energy
    freedom to accommodate the amount of temporal kinetic energy required to
    stabilize the fixed-charge dilation mode?

CANONICAL FIELD DECOMPOSITION
-----------------------------
For canonical real field components with arbitrary time dependence,

    rho
    =
    1/2 D
    +
    1/2 G
    +
    V

where

    D
    =
    sum_a dot(phi_a)^2

and

    G
    =
    sum_a |grad phi_a|^2.

For a diagonal stress tensor,

    rho + p_i
    =
    D + G_i

with

    G_i
    =
    sum_a (partial_i phi_a)^2
    >= 0.

Therefore an exact target stress tensor permits temporal derivative strength
only within

    0 <= D <= min_i(rho + p_i).

The corresponding temporal kinetic energy density is

    t = D/2.

After choosing D, the required spatial kinetic Gram entries are

    G_i
    =
    rho + p_i - D

and the pointwise potential is

    V
    =
    D
    -
    1/2 (
        rho + p_r + p_phi + p_z
    ).

These are pointwise algebraic identities only.  They do not prove global field
integrability.

FIXED-CHARGE DERRICK SCALING
----------------------------
Define integrated quantities

    E = T + K + U

with

    T
        temporal kinetic energy,

    K
        spatial gradient energy,

    U
        potential energy.

Also define

    P
    =
    integral (
        p_r + p_phi + p_z
    ) dV.

For a stationary charged scalar configuration whose conserved charge is held
fixed under the spatial dilation

    phi_lambda(x)
    =
    phi(lambda x),

the temporal kinetic term scales oppositely to the static case because the
phase frequency must change to preserve charge:

    E_Q(lambda)
    =
    lambda^3 T
    +
    K/lambda
    +
    U/lambda^3.

At lambda=1,

    E_Q'(1)
    =
    P.

Thus the Laue condition P=0 again gives dilation stationarity.

The second derivative is

    E_Q''(1)
    =
    24 T
    -
    3 E
    -
    5 P.

For P=0,

    E_Q''(1)
    =
    24T - 3E.

The fixed-charge dilation curvature can therefore become positive only when

    T/E > 1/8.

This is a necessary one-mode stability gate, not a proof of complete
dynamical stability.

006D APPLICATION
----------------
The 006D source uses

    epsilon
    =
    max(
        |p_r|,
        |p_phi|
    )

with

    p_z = 0

and satisfies the pointwise DEC.

Its core and transfer annulus saturate one or more inequalities

    epsilon + p_i = 0

so they have little or no temporal-kinetic capacity while preserving the exact
stress tensor.

The smooth finite outer support collar does not generally saturate all of
those inequalities simultaneously and can therefore contain nonzero temporal
kinetic energy algebraically.

This module integrates that available capacity over the actual independently
reconstructed 006D profile from the 008B source module.

ASSUMPTIONS
-----------
- canonical positive-sign scalar kinetic terms;
- a stationary conserved-charge sector of Q-ball type is permitted in
  principle;
- fixed total charge is used in the Derrick scaling variation;
- exact 006D stress-energy is held fixed pointwise for the algebraic capacity
  calculation;
- normalized 006D vertical profile;
- flat-background matter analysis;
- no gauge-field energy;
- no nonlinear gravity;
- no global scalar-field integrability assumption.

WHAT A GREEN RESULT MEANS
-------------------------
A green result means only:

    The exact 006D stress tensor has sufficient algebraic temporal-kinetic
    capacity for a conserved-charge scalar sector to make the fixed-charge
    uniform dilation curvature positive.

It does NOT mean:

- a global U(1) field configuration exists;
- one potential V(phi) reproduces the profile;
- the equations of motion are satisfied;
- nonaxisymmetric perturbations are stable;
- charge cannot radiate;
- a gauged solution is stable;
- nonlinear GR preserves the configuration;
- a practical antigravity device exists.

LITERATURE CONTEXT
------------------
Q-balls are established non-topological solitons of complex scalar theories
with conserved U(1) charge.  Their stationary phase dependence is a standard
mechanism for evading the purely static Derrick obstruction.

CLAIM CLASSIFICATION
--------------------
ANALYTICAL_KINEMATIC_FIXED_CHARGE_STABILITY_CAPACITY_GATE
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from scipy.integrate import quad

from antigravity_research.geometry.canonical_scalar_representability import (
    ALPHA_006D,
    BETA_006D,
    FINEST_SCALE_006D,
    regularized_006d_breakpoints,
    regularized_006d_surface_stress,
)


@dataclass(frozen=True)
class FixedChargeDerrickDiagnostics:
    """Integrated fixed-charge Derrick quantities."""

    total_energy: float
    pressure_trace: float
    temporal_kinetic: float
    spatial_gradient: float
    potential_energy: float
    first_derivative: float
    second_derivative: float

    @property
    def temporal_fraction(self) -> float:
        """Return T/E."""

        return self.temporal_kinetic / self.total_energy

    @property
    def second_derivative_over_energy(self) -> float:
        """Return E_Q''(1)/E."""

        return self.second_derivative / self.total_energy


def temporal_derivative_capacity(
    epsilon: float,
    p_r: float,
    p_phi: float,
    p_z: float,
) -> float:
    """Return the largest allowed D=sum(dot(phi_a)^2).

    Exact canonical-field reproduction requires

        G_i = epsilon + p_i - D >= 0.

    Therefore

        D_max = min_i(epsilon + p_i).

    Tiny negative roundoff is clipped to zero.
    """

    values = (
        epsilon + p_r,
        epsilon + p_phi,
        epsilon + p_z,
    )

    if not all(
        math.isfinite(value)
        for value in values
    ):
        raise ValueError(
            "stress inputs must be finite"
        )

    return max(
        0.0,
        min(values),
    )


def temporal_kinetic_capacity_density(
    epsilon: float,
    p_r: float,
    p_phi: float,
    p_z: float,
) -> float:
    """Return maximum temporal kinetic energy density D_max/2."""

    return 0.5 * temporal_derivative_capacity(
        epsilon,
        p_r,
        p_phi,
        p_z,
    )


def dynamic_scalar_decomposition(
    epsilon: float,
    p_r: float,
    p_phi: float,
    p_z: float,
    temporal_derivative_squared: float,
) -> tuple[float, float, float, float]:
    """Return spatial Gram entries and potential after allocating D.

    Returns

        (G_r, G_phi, G_z, V).
    """

    capacity = temporal_derivative_capacity(
        epsilon,
        p_r,
        p_phi,
        p_z,
    )

    d = temporal_derivative_squared

    if (
        not math.isfinite(d)
        or d < 0.0
        or d > capacity + 1.0e-12
    ):
        raise ValueError(
            "temporal derivative allocation exceeds local stress capacity"
        )

    g_r = epsilon + p_r - d
    g_phi = epsilon + p_phi - d
    g_z = epsilon + p_z - d

    potential = (
        d
        - 0.5
        * (
            epsilon
            + p_r
            + p_phi
            + p_z
        )
    )

    return (
        g_r,
        g_phi,
        g_z,
        potential,
    )


def fixed_charge_derrick_diagnostics(
    total_energy: float,
    pressure_trace: float,
    temporal_kinetic: float,
) -> FixedChargeDerrickDiagnostics:
    """Return fixed-charge virial decomposition and dilation curvature."""

    if (
        not math.isfinite(total_energy)
        or total_energy <= 0.0
    ):
        raise ValueError(
            "total_energy must be finite and positive"
        )

    if not math.isfinite(pressure_trace):
        raise ValueError(
            "pressure_trace must be finite"
        )

    if (
        not math.isfinite(temporal_kinetic)
        or temporal_kinetic < 0.0
    ):
        raise ValueError(
            "temporal_kinetic must be finite and nonnegative"
        )

    spatial_gradient = (
        0.5
        * (
            pressure_trace
            + 3.0 * total_energy
            - 6.0 * temporal_kinetic
        )
    )

    potential_energy = (
        2.0 * temporal_kinetic
        - 0.5
        * (
            total_energy
            + pressure_trace
        )
    )

    first_derivative = pressure_trace

    second_derivative = (
        24.0 * temporal_kinetic
        - 3.0 * total_energy
        - 5.0 * pressure_trace
    )

    return FixedChargeDerrickDiagnostics(
        total_energy=total_energy,
        pressure_trace=pressure_trace,
        temporal_kinetic=temporal_kinetic,
        spatial_gradient=spatial_gradient,
        potential_energy=potential_energy,
        first_derivative=first_derivative,
        second_derivative=second_derivative,
    )


def critical_temporal_kinetic(
    total_energy: float,
    pressure_trace: float = 0.0,
) -> float:
    """Return T at which the fixed-charge dilation curvature is zero."""

    value = (
        3.0 * total_energy
        + 5.0 * pressure_trace
    ) / 24.0

    return max(
        0.0,
        value,
    )


def _integrate_radial(
    function,
    scale: float,
) -> float:
    """Integrate a normalized 006D surface quantity over area."""

    total = 0.0

    breakpoints = regularized_006d_breakpoints(
        scale
    )

    for lower, upper in zip(
        breakpoints[:-1],
        breakpoints[1:],
    ):
        value, _ = quad(
            lambda radius:
                radius * function(radius),
            lower,
            upper,
            epsabs=2.0e-11,
            epsrel=2.0e-11,
            limit=400,
        )

        total += value

    return (
        2.0
        * math.pi
        * total
    )


def integrated_006d_charge_capacity(
    scale: float = FINEST_SCALE_006D,
) -> tuple[float, float, float]:
    """Return E, pressure trace P, and maximum temporal kinetic T_max."""

    def stress(radius: float):
        return regularized_006d_surface_stress(
            radius,
            scale,
        )

    energy = _integrate_radial(
        lambda radius:
            stress(radius).epsilon,
        scale,
    )

    pressure_trace = _integrate_radial(
        lambda radius:
            (
                stress(radius).p_r
                + stress(radius).p_phi
                + stress(radius).p_z
            ),
        scale,
    )

    temporal_capacity = _integrate_radial(
        lambda radius:
            temporal_kinetic_capacity_density(
                stress(radius).epsilon,
                stress(radius).p_r,
                stress(radius).p_phi,
                stress(radius).p_z,
            ),
        scale,
    )

    return (
        energy,
        pressure_trace,
        temporal_capacity,
    )


def 006d_region_temporal_capacities(
    scale: float = FINEST_SCALE_006D,
) -> dict[str, float]:
    """Return temporal kinetic capacity in the four radial 006D regions."""

    inner_width = scale / 4.0

    regions = {
        "core": (
            0.0,
            ALPHA_006D - inner_width,
        ),
        "inner_transition": (
            ALPHA_006D - inner_width,
            ALPHA_006D + inner_width,
        ),
        "transfer_annulus": (
            ALPHA_006D + inner_width,
            BETA_006D,
        ),
        "outer_collar": (
            BETA_006D,
            BETA_006D + scale,
        ),
    }

    capacities: dict[str, float] = {}

    for name, (lower, upper) in regions.items():
        value, _ = quad(
            lambda radius:
                radius
                * temporal_kinetic_capacity_density(
                    regularized_006d_surface_stress(
                        radius,
                        scale,
                    ).epsilon,
                    regularized_006d_surface_stress(
                        radius,
                        scale,
                    ).p_r,
                    regularized_006d_surface_stress(
                        radius,
                        scale,
                    ).p_phi,
                    regularized_006d_surface_stress(
                        radius,
                        scale,
                    ).p_z,
                ),
            lower,
            upper,
            epsabs=2.0e-11,
            epsrel=2.0e-11,
            limit=400,
        )

        capacities[name] = (
            2.0
            * math.pi
            * value
        )

    return capacities
