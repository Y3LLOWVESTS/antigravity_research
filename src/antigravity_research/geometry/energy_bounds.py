"""Energy lower bounds for local gravitational repulsion.

Weak-field static GR uses the active source

    S = epsilon + p_x + p_y + p_z.

For type-I matter satisfying DEC,

    epsilon >= 0
    |p_i| <= epsilon.

Hence pointwise

    -2 epsilon <= S <= 4 epsilon.

The maximally negative value is attained by

    p_x = p_y = p_z = -epsilon.

If all repulsive energy E were placed at minimum distance h from a target,

    a <= 2 G E/(c^2 h^2).

That gives the pointwise DEC bound

    M_equiv >= a h^2/(2G).

For an isolated static source, Laue stress balance requires the integrated
spatial stresses to cancel. Combining this with DEC requires compensating
positive-energy support.

The optimistic static bound becomes

    M_total >= a h^2/G.

This is an optimistic lower bound, not a construction.
"""

from __future__ import annotations

from dataclasses import dataclass

from antigravity_research.geometry.kottler import C, G


@dataclass(frozen=True)
class TypeIDEC:
    satisfied: bool
    active_energy_j: float


def active_energy_j(
    energy_j: float,
    px_j: float,
    py_j: float,
    pz_j: float,
) -> float:
    return (
        energy_j
        + px_j
        + py_j
        + pz_j
    )


def evaluate_integrated_type_i_dec(
    energy_j: float,
    px_j: float,
    py_j: float,
    pz_j: float,
) -> TypeIDEC:

    scale = max(
        abs(energy_j),
        abs(px_j),
        abs(py_j),
        abs(pz_j),
        1.0,
    )

    tol = 1e-12 * scale

    satisfied = (
        energy_j >= -tol
        and abs(px_j) <= energy_j + tol
        and abs(py_j) <= energy_j + tol
        and abs(pz_j) <= energy_j + tol
    )

    return TypeIDEC(
        satisfied=satisfied,
        active_energy_j=active_energy_j(
            energy_j,
            px_j,
            py_j,
            pz_j,
        ),
    )


def pointwise_dec_mass_lower_bound_kg(
    acceleration_m_s2: float,
    minimum_distance_m: float,
) -> float:
    """DEC bound without imposing global static stress balance."""

    if acceleration_m_s2 <= 0:
        raise ValueError("acceleration must be positive")

    if minimum_distance_m <= 0:
        raise ValueError("distance must be positive")

    return (
        acceleration_m_s2
        * minimum_distance_m**2
        / (
            2.0
            * G
        )
    )


def static_laue_dec_mass_lower_bound_kg(
    acceleration_m_s2: float,
    minimum_distance_m: float,
) -> float:
    """Optimistic static isolated DEC bound."""

    if acceleration_m_s2 <= 0:
        raise ValueError("acceleration must be positive")

    if minimum_distance_m <= 0:
        raise ValueError("distance must be positive")

    return (
        acceleration_m_s2
        * minimum_distance_m**2
        / G
    )


def energy_j_from_mass_kg(
    mass_kg: float,
) -> float:
    return mass_kg * C**2
