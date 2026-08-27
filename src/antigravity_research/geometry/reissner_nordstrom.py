"""Reissner-Nordstrom repulsive-gravity diagnostics.

We investigate an exact Einstein-Maxwell spacetime.

Exterior metric:

    f(r)
      = 1
        - 2GM/(c^2 r)
        + G Q^2/(4*pi*epsilon0*c^4*r^2)

For a static observer, the outward proper acceleration required
to remain fixed is

    a_hold
      = [GM/r^2
         - GQ^2/(4*pi*epsilon0*c^2*r^3)]
        / sqrt(f)

Ordinary attractive gravity:
    a_hold > 0

Repulsive gravitational tendency:
    a_hold < 0

For a neutral freely falling test particle we therefore define

    g_free = -a_hold.

The sign changes at

    r_rep = Q^2/(4*pi*epsilon0*M*c^2).

The exterior Maxwell field has positive energy density with

    p_r = -epsilon
    p_t = +epsilon.

The shell model used here has:

    Minkowski interior
    charged thin shell at R
    Reissner-Nordstrom exterior.

This is an exact GR junction problem, not a Newtonian analogy.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from antigravity_research.geometry.kottler import C, G


EPSILON_0 = 8.8541878128e-12
HBAR = 1.054571817e-34
ELECTRON_MASS_KG = 9.1093837139e-31
ELEMENTARY_CHARGE_C = 1.602176634e-19


@dataclass(frozen=True)
class ShellConditions:
    nec: bool
    wec: bool
    dec: bool


def geometric_mass_m(
    mass_kg: float,
) -> float:
    return (
        G
        * mass_kg
        / C**2
    )


def geometric_charge_squared_m2(
    charge_c: float,
) -> float:
    return (
        G
        * charge_c**2
        / (
            4.0
            * math.pi
            * EPSILON_0
            * C**4
        )
    )


def rn_metric_f(
    radius_m: float,
    mass_kg: float,
    charge_c: float,
) -> float:
    if radius_m <= 0.0:
        raise ValueError(
            "radius_m must be positive"
        )

    m = geometric_mass_m(
        mass_kg
    )

    q2 = geometric_charge_squared_m2(
        charge_c
    )

    return (
        1.0
        - 2.0 * m / radius_m
        + q2 / radius_m**2
    )


def repulsion_radius_m(
    mass_kg: float,
    charge_c: float,
) -> float:
    """Radius where neutral static gravitational tendency changes sign."""

    if mass_kg <= 0.0:
        raise ValueError(
            "mass_kg must be positive"
        )

    return (
        charge_c**2
        / (
            4.0
            * math.pi
            * EPSILON_0
            * mass_kg
            * C**2
        )
    )


def neutral_static_hold_acceleration_m_s2(
    radius_m: float,
    mass_kg: float,
    charge_c: float,
) -> float:
    """Proper acceleration required to hold a neutral observer static.

    Positive:
        must accelerate outward to resist attraction.

    Negative:
        must accelerate inward to resist repulsion.
    """

    f = rn_metric_f(
        radius_m,
        mass_kg,
        charge_c,
    )

    if f <= 0.0:
        raise ValueError(
            "Static observer is not in a static RN region"
        )

    mass_term = (
        G
        * mass_kg
        / radius_m**2
    )

    charge_term = (
        G
        * charge_c**2
        / (
            4.0
            * math.pi
            * EPSILON_0
            * C**2
            * radius_m**3
        )
    )

    return (
        mass_term
        - charge_term
    ) / math.sqrt(f)


def neutral_free_tendency_m_s2(
    radius_m: float,
    mass_kg: float,
    charge_c: float,
) -> float:
    """Outward gravitational tendency relative to static observers."""

    return (
        -neutral_static_hold_acceleration_m_s2(
            radius_m,
            mass_kg,
            charge_c,
        )
    )


def electric_field_v_m(
    radius_m: float,
    charge_c: float,
) -> float:
    return (
        charge_c
        / (
            4.0
            * math.pi
            * EPSILON_0
            * radius_m**2
        )
    )


def maxwell_energy_density_j_m3(
    radius_m: float,
    charge_c: float,
) -> float:
    field = electric_field_v_m(
        radius_m,
        charge_c,
    )

    return (
        0.5
        * EPSILON_0
        * field**2
    )


def electromagnetic_field_energy_mass_outside_kg(
    shell_radius_m: float,
    charge_c: float,
) -> float:
    """Energy-equivalent mass in electric field outside R.

    U_EM = Q^2/(8*pi*epsilon0*R)
    """

    return (
        charge_c**2
        / (
            8.0
            * math.pi
            * EPSILON_0
            * shell_radius_m
            * C**2
        )
    )


def schwinger_critical_field_v_m() -> float:
    return (
        ELECTRON_MASS_KG**2
        * C**3
        / (
            ELEMENTARY_CHARGE_C
            * HBAR
        )
    )


# ============================================================
# PARAMETERIZATION
#
# z = r_rep / R
#
# z > 1 means the repulsive RN region extends outside the shell.
# ============================================================

def solve_source_for_surface_repulsion(
    target_outward_acceleration_m_s2: float,
    shell_radius_m: float,
    z: float,
) -> tuple[float, float]:
    """Solve M and Q for desired neutral gravitational repulsion at R.

    z = r_rep/R must exceed one.

    Define

        u = GM/(c^2 R)

    and

        f(R) = 1 + u(z - 2).

    The exact surface repulsive tendency is

        g = c^2 u(z - 1)/(R sqrt(f)).

    This function analytically solves that equation for u.
    """

    if target_outward_acceleration_m_s2 <= 0.0:
        raise ValueError(
            "target acceleration must be positive"
        )

    if shell_radius_m <= 0.0:
        raise ValueError(
            "shell radius must be positive"
        )

    if z <= 1.0:
        raise ValueError(
            "z must exceed 1 for exterior repulsion"
        )

    a = (
        target_outward_acceleration_m_s2
        * shell_radius_m
        / C**2
    )

    d = z - 1.0
    b = z - 2.0

    discriminant = (
        a**4 * b**2
        + 4.0 * d**2 * a**2
    )

    u = (
        a**2 * b
        + math.sqrt(discriminant)
    ) / (
        2.0 * d**2
    )

    mass_kg = (
        u
        * shell_radius_m
        * C**2
        / G
    )

    charge_c = math.sqrt(
        4.0
        * math.pi
        * EPSILON_0
        * z
        * mass_kg
        * C**2
        * shell_radius_m
    )

    return (
        mass_kg,
        charge_c,
    )


# ============================================================
# ISRAEL SHELL
# ============================================================

def charged_shell_surface_energy_geom_per_m(
    shell_radius_m: float,
    mass_kg: float,
    charge_c: float,
) -> float:
    """Surface energy density in geometrized units [1/m].

    Interior:
        f_- = 1

    Exterior:
        f_+ = RN.

    sigma = (1 - sqrt(f_+))/(4*pi*R)

    A stable algebraic expression is used to avoid cancellation when
    f_+ is extremely close to one.
    """

    r = shell_radius_m

    m = geometric_mass_m(
        mass_kg
    )

    q2 = geometric_charge_squared_m2(
        charge_c
    )

    f = rn_metric_f(
        r,
        mass_kg,
        charge_c,
    )

    if f <= 0.0:
        raise ValueError(
            "Shell is not in a static region"
        )

    sqrt_f = math.sqrt(f)

    one_minus_f = (
        2.0 * m / r
        - q2 / r**2
    )

    stable_difference = (
        one_minus_f
        / (
            1.0
            + sqrt_f
        )
    )

    return (
        stable_difference
        / (
            4.0
            * math.pi
            * r
        )
    )


def charged_shell_surface_pressure_geom_per_m(
    shell_radius_m: float,
    mass_kg: float,
    charge_c: float,
) -> float:
    """Tangential surface pressure in geometrized units [1/m].

    Negative value means surface tension.
    """

    r = shell_radius_m

    m = geometric_mass_m(
        mass_kg
    )

    q2 = geometric_charge_squared_m2(
        charge_c
    )

    f = rn_metric_f(
        r,
        mass_kg,
        charge_c,
    )

    if f <= 0.0:
        raise ValueError(
            "Shell is not in a static region"
        )

    sqrt_f = math.sqrt(f)

    sigma = (
        charged_shell_surface_energy_geom_per_m(
            r,
            mass_kg,
            charge_c,
        )
    )

    derivative = (
        2.0 * m / r**2
        - 2.0 * q2 / r**3
    )

    return (
        -0.5 * sigma
        + derivative
        / (
            16.0
            * math.pi
            * sqrt_f
        )
    )


def charged_shell_surface_energy_j_m2(
    shell_radius_m: float,
    mass_kg: float,
    charge_c: float,
) -> float:
    return (
        C**4
        / G
        * charged_shell_surface_energy_geom_per_m(
            shell_radius_m,
            mass_kg,
            charge_c,
        )
    )


def charged_shell_surface_pressure_n_m(
    shell_radius_m: float,
    mass_kg: float,
    charge_c: float,
) -> float:
    return (
        C**4
        / G
        * charged_shell_surface_pressure_geom_per_m(
            shell_radius_m,
            mass_kg,
            charge_c,
        )
    )


def evaluate_shell_conditions(
    surface_energy_j_m2: float,
    surface_pressure_n_m: float,
) -> ShellConditions:
    """NEC/WEC/DEC for isotropic shell surface stress."""

    scale = max(
        abs(surface_energy_j_m2),
        abs(surface_pressure_n_m),
        1.0,
    )

    tolerance = (
        1.0e-10
        * scale
    )

    nec = (
        surface_energy_j_m2
        + surface_pressure_n_m
        >= -tolerance
    )

    wec = (
        surface_energy_j_m2
        >= -tolerance
        and nec
    )

    dec = (
        surface_energy_j_m2
        >= -tolerance
        and (
            surface_energy_j_m2
            - abs(surface_pressure_n_m)
        )
        >= -tolerance
    )

    return ShellConditions(
        nec=nec,
        wec=wec,
        dec=dec,
    )
