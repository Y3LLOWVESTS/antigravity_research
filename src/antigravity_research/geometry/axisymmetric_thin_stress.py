"""Locally conserved axisymmetric thin-stress source models.

PURPOSE
-------
Provide a geometry-aware thin-source model for the first slice of Simulation
006B.  The model generalizes Simulation 005B from a uniform relativistic-
tension disk plus a single support rim to an axisymmetric membrane whose
radial and azimuthal stresses may vary with radius while satisfying local
static stress conservation.

SCIENTIFIC QUESTION
-------------------
How much of the Simulation 005B mass coefficient

    C_005B ~= 79.753148

is caused by its specific support geometry rather than by pointwise dominant
energy condition (DEC) and local conservation requirements?

THEORY / MODEL
--------------
Linearized general relativity in a static, weak-field, axisymmetric setting.
The source is an idealized infinitesimally thin surface at z = 0 plus an
optional idealized outer line support.  Surface stress-energy is represented
in the orthonormal (r, phi, z) basis by

    surface energy density: U(r)
    radial pressure:         p_r(r)
    azimuthal pressure:      p_phi(r)
    normal pressure:         p_z = 0

Positive pressure denotes compression; negative pressure denotes tension.

For a static axisymmetric thin surface with no shear, local flat-background
stress conservation away from line singularities is

    d p_r / dr + (p_r - p_phi) / r = 0

or equivalently

    d(r p_r) / dr = p_phi.

The weak-field active surface-energy density is

    S(r) = U(r) + p_r(r) + p_phi(r).

At an axial target a height h above the surface, positive outward acceleration
is

    a_z = -(2 pi G h / c^2)
          integral r S(r) / (r^2 + h^2)^(3/2) dr

plus any line-source contribution.

CONSERVE-AND-SPREAD CANDIDATE
-----------------------------
A particularly efficient DEC-saturating conserved family has two surface
regions and one outer line support.

Region I, 0 <= r <= a:

    U = U0
    p_r = -U0
    p_phi = -U0

Region II, a < r < R:

    U = U0 a^2 / r^2
    p_r = -U
    p_phi = +U

Outer ring, r = R:

    line energy lambda = U0 a^2 / R
    p_phi,line = +lambda

The inner region is locally repulsive.  The annulus transfers the radial
stress outward while saturating DEC, and the outer ring terminates the radial
tension.  The construction obeys local conservation distributionally within
the ideal thin-source approximation.

INPUTS / OUTPUTS
----------------
The principal public functions are dimensionless.  They use

    alpha = a / h
    beta  = R / h

and return dimensionless field factors or the coefficient C defined by

    M = C a_target h^2 / G.

This normalization makes the geometry result independent of the chosen target
acceleration and stand-off scale as long as the linearized approximation is
valid.

UNITS
-----
Dimensionless functions use radius ratios only.  Physical scaling may be
reconstructed with SI G and c from the existing project constants.

SIGN CONVENTIONS
----------------
Positive axial acceleration means away from the source toward increasing z.
Positive p denotes compression.  Negative p denotes tension.

ASSUMPTIONS
-----------
- linearized general relativity;
- static source;
- axisymmetry;
- infinitesimally thin surface and line distributions;
- no momentum density or shear in this first 006B slice;
- type-I surface stress-energy;
- target lies on the symmetry axis;
- source is entirely at z = 0;
- no stability or material constitutive law is imposed.

ENERGY CONDITIONS
-----------------
The conserve-and-spread family has U >= 0 and saturates the surface DEC:

    |p_r| <= U
    |p_phi| <= U
    p_z = 0.

The outer line support also saturates its one-dimensional DEC at minimum
energy.

NUMERICAL METHOD
----------------
This module contains closed-form dimensionless expressions.  Simulation 006B
performs numerical optimization and an independent radial linear-program
reconstruction.

VALIDATION STRATEGY
-------------------
Validation should include:

1. an independent reconstruction of the Simulation 005B disk-plus-rim
   coefficient without importing finite_tension_disk.py;
2. direct checks of local conservation in each smooth region;
3. exact integrated stress-balance identities;
4. pointwise DEC checks;
5. convergence of an independent discretized radial linear program toward the
   closed-form candidate optimum.

LIMITATIONS
-----------
This model does not establish:

- a fully general 2D (r,z) optimum;
- finite-thickness local conservation;
- an exact nonlinear Einstein solution;
- dynamical or mechanical stability;
- a realizable material or field configuration;
- experimental accessibility;
- a practical antigravity device.

The optimized coefficient from this model is therefore an architecture result
inside a restricted thin-source subclass, not a universal GR lower bound.

RELATED FILES
-------------
Baseline model:
    src/antigravity_research/geometry/finite_tension_disk.py

Baseline simulation:
    simulations/005b_finite_supported_antigravity.py

Abstract lower-bound model:
    src/antigravity_research/geometry/energy_bounds.py

Planned simulation:
    simulations/006b_geometry_aware_dec_optimizer.py

Tests:
    tests/known_solutions/test_axisymmetric_thin_stress.py

CLAIM CLASSIFICATION
--------------------
NUMERICAL_OPTIMIZATION_RESULT once independently reproduced by Simulation 006B.

NOVEL PHYSICS CLAIM
-------------------
NO.  This is a project-derived optimization result inside established
linearized GR assumptions.
"""

from __future__ import annotations

import math


def _validate_positive_ratio(name: str, value: float) -> None:
    if not math.isfinite(value) or value <= 0.0:
        raise ValueError(f"{name} must be finite and positive")


def radial_kernel_primitive(x: float) -> float:
    """Return a primitive of 1/[x (1+x^2)^(3/2)].

    Parameters
    ----------
    x:
        Positive dimensionless radius r/h.

    Returns
    -------
    float
        F(x) satisfying

            dF/dx = 1 / (x * (1 + x^2)^(3/2)).

    Notes
    -----
    The stable form is

        F(x) = log[x / (sqrt(1+x^2) + 1)] + 1/sqrt(1+x^2).
    """

    _validate_positive_ratio("x", x)

    root = math.sqrt(1.0 + x * x)

    return math.log(x / (root + 1.0)) + 1.0 / root


def uniform_disk_ring_field_factor(radius_over_h: float) -> float:
    """Return the independent q=1 disk-plus-rim axial field factor.

    The physical outward acceleration is

        a_z = 2*pi*G*U/c^2 * factor

    for a uniform q=1 membrane of radius R and its minimum-energy DEC ring,
    with ``radius_over_h = R/h``.

    This expression is intentionally written independently of the production
    formula in ``finite_tension_disk.py`` so it can serve as a cross-check.
    """

    x = radius_over_h
    _validate_positive_ratio("radius_over_h", x)

    root = math.sqrt(1.0 + x * x)

    membrane = 1.0 - 1.0 / root
    ring = -2.0 * x * x / (1.0 + x * x) ** 1.5

    return membrane + ring


def uniform_disk_ring_mass_coefficient(radius_over_h: float) -> float:
    """Return C for the q=1 uniform disk plus minimum-DEC rim.

    ``C`` is defined by

        M = C * a_target * h^2 / G.

    ``math.inf`` is returned when the target point is not in the repulsive
    region of the model.
    """

    x = radius_over_h
    factor = uniform_disk_ring_field_factor(x)

    if factor <= 0.0:
        return math.inf

    # Total positive mass-energy of the q=1 disk-plus-rim architecture is
    # 3*pi*U*R^2/c^2.  Divide by
    # a_z = 2*pi*G*U*factor/c^2 and by h^2/G.
    return 3.0 * x * x / (2.0 * factor)


def conserved_annular_field_factor(
    inner_radius_over_h: float,
    outer_radius_over_h: float,
) -> float:
    """Return the axial field factor of the conserved annular architecture.

    Parameters
    ----------
    inner_radius_over_h:
        ``alpha = a/h`` for the outer edge of the repulsive inner disk.

    outer_radius_over_h:
        ``beta = R/h`` for the outer support ring.  Must exceed ``alpha``.

    Returns
    -------
    float
        Dimensionless ``f`` in

            a_z = 2*pi*G*U0/c^2 * f.

        Positive values correspond to outward acceleration.
    """

    alpha = inner_radius_over_h
    beta = outer_radius_over_h

    _validate_positive_ratio("inner_radius_over_h", alpha)
    _validate_positive_ratio("outer_radius_over_h", beta)

    if beta <= alpha:
        raise ValueError("outer radius must exceed inner radius")

    inner = 1.0 - 1.0 / math.sqrt(1.0 + alpha * alpha)

    annular_integral = (
        radial_kernel_primitive(beta)
        - radial_kernel_primitive(alpha)
    )

    annulus = -alpha * alpha * annular_integral

    ring = (
        -2.0
        * alpha
        * alpha
        / (1.0 + beta * beta) ** 1.5
    )

    return inner + annulus + ring


def conserved_annular_mass_factor(
    inner_radius_over_h: float,
    outer_radius_over_h: float,
) -> float:
    """Return the dimensionless positive-energy factor before field division.

    The total mass-energy is

        M = pi * U0 * a^2 / c^2 * [3 + 2 log(R/a)].

    In units proportional to ``pi*U0*h^2/c^2``, this function returns

        alpha^2 * [3 + 2 log(beta/alpha)].
    """

    alpha = inner_radius_over_h
    beta = outer_radius_over_h

    _validate_positive_ratio("inner_radius_over_h", alpha)
    _validate_positive_ratio("outer_radius_over_h", beta)

    if beta <= alpha:
        raise ValueError("outer radius must exceed inner radius")

    return (
        alpha
        * alpha
        * (3.0 + 2.0 * math.log(beta / alpha))
    )


def conserved_annular_mass_coefficient(
    inner_radius_over_h: float,
    outer_radius_over_h: float,
) -> float:
    """Return C for the locally conserved DEC annular architecture.

    ``C`` is defined by

        M = C * a_target * h^2 / G.

    The result combines the complete positive energy of the repulsive inner
    disk, the stress-transfer annulus, and the minimum-energy outer line
    support.  ``math.inf`` is returned if the chosen geometry is not repulsive
    at the target.
    """

    factor = conserved_annular_field_factor(
        inner_radius_over_h,
        outer_radius_over_h,
    )

    if factor <= 0.0:
        return math.inf

    mass_factor = conserved_annular_mass_factor(
        inner_radius_over_h,
        outer_radius_over_h,
    )

    # Physical mass has a factor pi, while acceleration has 2*pi, leaving 1/2.
    return mass_factor / (2.0 * factor)


def conserved_annular_integrated_stress_trace_factor(
    inner_radius_over_h: float,
    outer_radius_over_h: float,
) -> float:
    """Return the normalized integrated spatial-stress trace.

    The normalization is ``pi*U0*h^2``.  For the complete inner disk,
    annulus, and outer ring, exact local conservation implies a zero result.

    This explicit identity is kept as a regression target rather than simply
    returning zero by definition.
    """

    alpha = inner_radius_over_h
    beta = outer_radius_over_h

    _validate_positive_ratio("inner_radius_over_h", alpha)
    _validate_positive_ratio("outer_radius_over_h", beta)

    if beta <= alpha:
        raise ValueError("outer radius must exceed inner radius")

    # Inner disk: p_r + p_phi = -2 U0.
    inner_trace = -2.0 * alpha * alpha

    # Annulus: p_r + p_phi = 0 pointwise.
    annulus_trace = 0.0

    # Outer line: p_phi,line = lambda = U0*a^2/R.  Integrating around the
    # circumference gives +2*pi*U0*a^2, or +2*alpha^2 in this normalization.
    ring_trace = 2.0 * alpha * alpha

    return inner_trace + annulus_trace + ring_trace
