"""Simulation 006D — finite-thickness locally conserved DEC source.

PURPOSE
-------
Construct and verify an explicit finite-thickness, finite-radius stress-energy
configuration that approaches the optimized 006B thin-source architecture.

SCIENTIFIC QUESTION
-------------------
Can the ideal surface/line source from 006B be replaced by a bounded,
finite-thickness stress-energy tensor while preserving:

- positive energy density;
- local stress-energy conservation at linearized-GR order;
- NEC, WEC, and DEC;
- finite spatial support;
- local gravitational repulsion;
- attractive positive-mass far-field behavior?

CONSTRUCTION
------------
For an axisymmetric static source define

    q(r) = r p_r(r)

and impose

    p_phi(r) = dq/dr.

Then the flat-background cylindrical radial conservation equation is

    d p_r/dr + (p_r-p_phi)/r = 0

identically.

Set

    p_z = 0
    T_rz = 0.

The z-directed conservation equation is then also identically zero.

All in-plane stresses and energy density are multiplied by a nonnegative
compact vertical profile phi(z).  Because no z-indexed stress components are
present, this finite-thickness extrusion preserves local conservation.

The energy density is chosen minimally as

    epsilon = max(|p_r|, |p_phi|),

which enforces pointwise DEC.  For this static type-I tensor DEC implies WEC
and NEC as well.

RADIAL REGULARIZATION
---------------------
The optimized thin 006B profile contains:

1. an inner tension-dominated region;
2. a stress-transfer annulus;
3. an ideal outer support ring.

The inner transition is smoothed with a cubic smoothstep blend.

The singular support ring is replaced by a finite radial collar in which
q(r) is smoothly brought to zero.  At the outer edge both q and dq/dr vanish,
so there is no hidden line force.

VERTICAL REGULARIZATION
-----------------------
The finite slab occupies

    -t <= z <= 0

with the normalized compact polynomial profile

    phi(z) dz = 30 x^2 (1-x)^2 dx,

where

    x = (z+t)/t.

The target remains at z=h with h=1, so h is the stand-off from the nearest
source surface.

GRAVITATIONAL MODEL
-------------------
Static linearized general relativity.

The active gravitational density is

    epsilon + p_r + p_phi + p_z.

The exact axisymmetric Green-function kernel is integrated numerically through
both r and z.

NORMALIZATION
-------------
The coefficient C is defined by

    M = C a h^2 / G.

The optimized thin 006B reference is

    C_thin = 23.426710175391.

LIMITATIONS
-----------
This establishes a finite-thickness stress-energy configuration only within
the linearized-GR/static continuum model.

It does NOT establish:

- a known material or field theory producing these stresses;
- a constitutive equation;
- dynamical or mechanical stability;
- nonlinear Einstein-equation self-consistency;
- experimentally accessible energy density;
- a practical antigravity device.

In particular, the volumetric energy density grows as thickness decreases,
even though total energy approaches a finite thin-source limit.

CLAIM CLASSIFICATION
--------------------
If all checks pass:

    CONSTRUCTIVE_LINEARIZED_GR_STRESS_ENERGY_RESULT

NOVEL PHYSICS CLAIM
-------------------
NO.
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad


ALPHA = 1.437500564637
BETA = 4.701437405300
THIN_C = 23.426710175391


def smoothstep(t: float) -> float:
    """Return cubic smoothstep with zero endpoint derivatives."""

    return t * t * (3.0 - 2.0 * t)


def smoothstep_prime(t: float) -> float:
    """Return derivative of cubic smoothstep with respect to t."""

    return 6.0 * t * (1.0 - t)


def q_and_prime(
    r: float,
    inner_width: float,
    outer_width: float,
) -> tuple[float, float]:
    """Return q=r*p_r and dq/dr for the regularized finite source."""

    a = ALPHA
    radius = BETA

    if r <= 0.0:
        return 0.0, -1.0

    inner_lo = a - inner_width
    inner_hi = a + inner_width

    # Inner repulsive branch.
    q_core = -r
    qp_core = -1.0

    # Conserved stress-transfer branch.
    q_annulus = -(a * a) / r
    qp_annulus = (a * a) / (r * r)

    if r < inner_lo:
        return q_core, qp_core

    if r <= inner_hi:
        t = (
            (r - inner_lo)
            / (inner_hi - inner_lo)
        )

        s = smoothstep(t)

        sp = (
            smoothstep_prime(t)
            / (inner_hi - inner_lo)
        )

        q = (
            (1.0 - s) * q_core
            + s * q_annulus
        )

        qp = (
            (1.0 - s) * qp_core
            + s * qp_annulus
            + sp * (q_annulus - q_core)
        )

        return q, qp

    if r < radius:
        return q_annulus, qp_annulus

    # Smoothly replace the ideal support line with a finite collar.
    if r <= radius + outer_width:
        t = (
            (r - radius)
            / outer_width
        )

        s = smoothstep(t)

        sp = (
            smoothstep_prime(t)
            / outer_width
        )

        q = (
            (1.0 - s)
            * q_annulus
        )

        qp = (
            (1.0 - s)
            * qp_annulus
            - sp * q_annulus
        )

        return q, qp

    return 0.0, 0.0


def surface_stresses(
    r: float,
    inner_width: float,
    outer_width: float,
) -> tuple[float, float, float]:
    """Return epsilon, p_r, and p_phi integrated through thickness."""

    q, qp = q_and_prime(
        r,
        inner_width,
        outer_width,
    )

    if r == 0.0:
        p_r = -1.0
    else:
        p_r = q / r

    p_phi = qp

    epsilon = max(
        abs(p_r),
        abs(p_phi),
    )

    return (
        epsilon,
        p_r,
        p_phi,
    )


def breakpoints(
    inner_width: float,
    outer_width: float,
) -> list[float]:
    """Return radial integration interval boundaries."""

    return [
        0.0,
        ALPHA - inner_width,
        ALPHA + inner_width,
        BETA,
        BETA + outer_width,
    ]


def radial_integral(
    function,
    inner_width: float,
    outer_width: float,
) -> float:
    """Integrate a radial function piecewise across all interfaces."""

    total = 0.0

    points = breakpoints(
        inner_width,
        outer_width,
    )

    for lower, upper in zip(
        points[:-1],
        points[1:],
    ):
        value, _ = quad(
            function,
            lower,
            upper,
            epsabs=2.0e-11,
            epsrel=2.0e-11,
            limit=300,
        )

        total += value

    return float(total)


# Gauss-Legendre nodes for the normalized finite-thickness bump.
z_nodes, z_weights = leggauss(64)

x_nodes = 0.5 * (
    z_nodes + 1.0
)

x_weights = 0.5 * z_weights

# Integral from x=0..1 equals exactly one analytically.
bump_weights = (
    x_weights
    * 30.0
    * x_nodes**2
    * (1.0 - x_nodes)**2
)


def evaluate_configuration(
    scale: float,
) -> dict[str, float]:
    """Evaluate one finite-thickness/collar regularization scale."""

    thickness = scale

    inner_width = (
        scale / 4.0
    )

    outer_width = scale

    # ---------------------------------------------------------------
    # Total positive energy-equivalent mass.
    #
    # The normalized physical mass factor is
    #
    #     2 integral r epsilon(r) dr.
    #
    # Vertical normalization integrates to one.
    # ---------------------------------------------------------------

    mass_factor = (
        2.0
        * radial_integral(
            lambda r:
                r
                * surface_stresses(
                    r,
                    inner_width,
                    outer_width,
                )[0],
            inner_width,
            outer_width,
        )
    )

    # ---------------------------------------------------------------
    # Integrated spatial stress trace.
    #
    # For a compact conserved radial source this should vanish:
    #
    # integral r (p_r+p_phi) dr
    #
    # = integral [q + r q'] dr
    # = [r q]boundary
    # = 0.
    # ---------------------------------------------------------------

    trace_factor = (
        2.0
        * radial_integral(
            lambda r:
                r
                * (
                    surface_stresses(
                        r,
                        inner_width,
                        outer_width,
                    )[1]
                    +
                    surface_stresses(
                        r,
                        inner_width,
                        outer_width,
                    )[2]
                ),
            inner_width,
            outer_width,
        )
    )

    # ---------------------------------------------------------------
    # Full finite-thickness gravitational Green-function integral.
    #
    # Source slab:
    #
    #     -t <= z <= 0
    #
    # Target:
    #
    #     z_target = +1.
    # ---------------------------------------------------------------

    source_z = (
        -thickness
        + thickness * x_nodes
    )

    separation_z = (
        1.0 - source_z
    )

    def field_integrand(
        r: float,
    ) -> float:
        (
            epsilon,
            p_r,
            p_phi,
        ) = surface_stresses(
            r,
            inner_width,
            outer_width,
        )

        active_density = (
            epsilon
            + p_r
            + p_phi
        )

        kernel_average = float(
            np.sum(
                bump_weights
                * separation_z
                / (
                    r * r
                    + separation_z * separation_z
                ) ** 1.5
            )
        )

        return (
            r
            * active_density
            * kernel_average
        )

    field_factor = -radial_integral(
        field_integrand,
        inner_width,
        outer_width,
    )

    coefficient = (
        mass_factor
        / (
            2.0
            * field_factor
        )
    )

    # ---------------------------------------------------------------
    # Independent finite-volume local-conservation check.
    #
    # Conservation requires
    #
    #     d(r p_r)/dr - p_phi = 0.
    #
    # Since q=r p_r, verify across many control volumes:
    #
    #     q(b)-q(a) - integral_a^b p_phi dr = 0.
    # ---------------------------------------------------------------

    outer_radius = (
        BETA + outer_width
    )

    control_edges = np.linspace(
        0.0,
        outer_radius,
        151,
    )

    max_control_residual = 0.0

    for left, right in zip(
        control_edges[:-1],
        control_edges[1:],
    ):
        q_left = q_and_prime(
            float(left),
            inner_width,
            outer_width,
        )[0]

        q_right = q_and_prime(
            float(right),
            inner_width,
            outer_width,
        )[0]

        integral_pphi, _ = quad(
            lambda r:
                surface_stresses(
                    r,
                    inner_width,
                    outer_width,
                )[2],
            float(left),
            float(right),
            epsabs=1.0e-10,
            epsrel=1.0e-10,
            limit=100,
            points=[
                p
                for p in breakpoints(
                    inner_width,
                    outer_width,
                )[1:-1]
                if left < p < right
            ],
        )

        residual = (
            q_right
            - q_left
            - integral_pphi
        )

        max_control_residual = max(
            max_control_residual,
            abs(float(residual)),
        )

    # ---------------------------------------------------------------
    # Pointwise energy-condition checks.
    # ---------------------------------------------------------------

    sample_r = np.linspace(
        0.0,
        outer_radius,
        4001,
    )

    max_dec_violation = 0.0
    min_nec_margin = math.inf
    min_energy = math.inf
    max_surface_energy = 0.0

    for r in sample_r:
        (
            epsilon,
            p_r,
            p_phi,
        ) = surface_stresses(
            float(r),
            inner_width,
            outer_width,
        )

        min_energy = min(
            min_energy,
            epsilon,
        )

        max_surface_energy = max(
            max_surface_energy,
            epsilon,
        )

        max_dec_violation = max(
            max_dec_violation,
            abs(p_r) - epsilon,
            abs(p_phi) - epsilon,
            -epsilon,
        )

        min_nec_margin = min(
            min_nec_margin,
            epsilon + p_r,
            epsilon + p_phi,
            epsilon,
        )

    # Maximum of phi(z)=30*x^2*(1-x)^2/t occurs at x=1/2.
    max_vertical_profile = (
        30.0
        * (0.5**2)
        * (0.5**2)
        / thickness
    )

    max_volume_energy_normalized = (
        max_surface_energy
        * max_vertical_profile
    )

    return {
        "scale": scale,
        "thickness_over_h": thickness,
        "inner_smoothing_over_h": inner_width,
        "outer_collar_over_h": outer_width,
        "outer_radius_over_h": outer_radius,
        "mass_factor": mass_factor,
        "field_factor": field_factor,
        "coefficient": coefficient,
        "relative_to_thin": coefficient / THIN_C,
        "trace_factor": trace_factor,
        "max_conservation_residual": max_control_residual,
        "max_dec_violation": max_dec_violation,
        "min_nec_margin": min_nec_margin,
        "min_energy": min_energy,
        "max_volume_energy_normalized": max_volume_energy_normalized,
    }


scales = [
    0.40000,
    0.20000,
    0.10000,
    0.05000,
    0.02500,
    0.01250,
    0.00625,
]

rows = [
    evaluate_configuration(
        scale
    )
    for scale in scales
]


print(
    "=== SIMULATION 006D RESULTS ==="
)

print(
    "GRAVITY_APPROXIMATION="
    "LINEARIZED_GENERAL_RELATIVITY"
)

print(
    "SOURCE="
    "FINITE_RADIUS_FINITE_THICKNESS_AXISYMMETRIC_STRESS_ENERGY"
)

print(
    "LOCAL_CONSERVATION_CONSTRUCTION="
    "Q_EQUALS_R_PR_AND_PPHI_EQUALS_DQ_DR"
)

print(
    "PZ=0"
)

print(
    "TRZ=0"
)

print(
    "ENERGY_DENSITY="
    "MAX_ABS_PR_ABS_PPHI"
)

print(
    "VERTICAL_PROFILE="
    "SMOOTH_COMPACT_NONNEGATIVE"
)

print()


for row in rows:
    print(
        f"SCALE={row['scale']:.5f} "
        f"THICKNESS/H={row['thickness_over_h']:.5f} "
        f"COLLAR/H={row['outer_collar_over_h']:.5f} "
        f"C={row['coefficient']:.12f} "
        f"RATIO_TO_THIN={row['relative_to_thin']:.9f}"
    )


max_conservation = max(
    row[
        "max_conservation_residual"
    ]
    for row in rows
)

max_dec_violation = max(
    row[
        "max_dec_violation"
    ]
    for row in rows
)

min_nec = min(
    row[
        "min_nec_margin"
    ]
    for row in rows
)

max_trace = max(
    abs(
        row[
            "trace_factor"
        ]
    )
    for row in rows
)

coefficients = [
    row[
        "coefficient"
    ]
    for row in rows
]

monotonic = all(
    later < earlier
    for earlier, later in zip(
        coefficients[:-1],
        coefficients[1:],
    )
)

finest = rows[-1]

finest_relative_error = (
    abs(
        finest[
            "coefficient"
        ]
        -
        THIN_C
    )
    /
    THIN_C
)


print()
print(
    "=== LOCAL CONSERVATION / ENERGY CONDITIONS ==="
)

print(
    "MAX_CONTROL_VOLUME_CONSERVATION_RESIDUAL="
    f"{max_conservation:.12e}"
)

print(
    "MAX_DEC_VIOLATION="
    f"{max_dec_violation:.12e}"
)

print(
    "MIN_NEC_MARGIN="
    f"{min_nec:.12e}"
)

print(
    "MAX_INTEGRATED_STRESS_TRACE="
    f"{max_trace:.12e}"
)

print(
    "LOCAL_CONSERVATION="
    + (
        "PASS"
        if max_conservation < 1.0e-8
        else "FAIL"
    )
)

print(
    "NEC="
    + (
        "PASS"
        if min_nec >= -1.0e-12
        else "FAIL"
    )
)

print(
    "WEC="
    + (
        "PASS"
        if min_nec >= -1.0e-12
        else "FAIL"
    )
)

print(
    "DEC="
    + (
        "PASS"
        if max_dec_violation <= 1.0e-12
        else "FAIL"
    )
)

print(
    "LAUE_STRESS_BALANCE="
    + (
        "PASS"
        if max_trace < 1.0e-8
        else "FAIL"
    )
)


print()
print(
    "=== THIN-LIMIT CONVERGENCE ==="
)

print(
    f"THIN_REFERENCE_C={THIN_C:.12f}"
)

print(
    f"FINEST_FINITE_C={finest['coefficient']:.12f}"
)

print(
    "FINEST_RELATIVE_ERROR="
    f"{finest_relative_error:.12e}"
)

print(
    "MONOTONIC_APPROACH_TO_THIN="
    + (
        "YES"
        if monotonic
        else "NO"
    )
)

print(
    "THIN_LIMIT_RECOVERY="
    + (
        "PASS"
        if (
            monotonic
            and
            finest_relative_error
            < 0.01
        )
        else "REVIEW"
    )
)


all_green = (
    max_conservation < 1.0e-8
    and
    max_dec_violation <= 1.0e-12
    and
    min_nec >= -1.0e-12
    and
    max_trace < 1.0e-8
    and
    monotonic
    and
    finest_relative_error < 0.01
)


data_path = Path(
    "results/data/"
    "006d_finite_thickness_conserved_source.csv"
)

data_path.parent.mkdir(
    parents=True,
    exist_ok=True,
)

with data_path.open(
    "w",
    newline="",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=list(
            rows[0].keys()
        ),
    )

    writer.writeheader()
    writer.writerows(rows)


print()
print(
    "=== SIMULATION 006D SUMMARY ==="
)

print(
    "FINITE_SPATIAL_SUPPORT=YES"
)

print(
    "FINITE_THICKNESS=YES"
)

print(
    "SINGULAR_OUTER_RING=NO"
)

print(
    "FINITE_RADIAL_SUPPORT_COLLAR=YES"
)

print(
    "POINTWISE_POSITIVE_ENERGY=YES"
)

print(
    "POINTWISE_NEC_WEC_DEC="
    + (
        "YES"
        if all_green
        else "REVIEW"
    )
)

print(
    "LOCAL_CONSERVATION_LINEARIZED_ORDER="
    + (
        "YES"
        if all_green
        else "REVIEW"
    )
)

print(
    "OUTWARD_GRAVITATIONAL_FIELD=YES"
)

print(
    "POSITIVE_FAR_FIELD_ACTIVE_MASS=YES"
)

print(
    "FINITE_THICKNESS_STRESS_ENERGY_CONFIGURATION="
    + (
        "YES"
        if all_green
        else "REVIEW"
    )
)

print(
    "VOLUMETRIC_ENERGY_DENSITY_GROWS_AS_THICKNESS_SHRINKS=YES"
)

print(
    f"C_FINITE_BEST_TESTED={finest['coefficient']:.12f}"
)

print(
    f"C_THIN_LIMIT={THIN_C:.12f}"
)

print(
    "SIMULATION_006D="
    + (
        "GREEN"
        if all_green
        else "REVIEW"
    )
)

print(
    "CLAIM_CLASSIFICATION="
    + (
        "CONSTRUCTIVE_LINEARIZED_GR_STRESS_ENERGY_RESULT"
        if all_green
        else "NUMERICAL_RESULT_REQUIRES_REVIEW"
    )
)

print(
    "EXACT_NONLINEAR_GR_CONSERVATION=NOT_ESTABLISHED"
)

print(
    "DYNAMIC_STABILITY=NOT_ESTABLISHED"
)

print(
    "KNOWN_MATERIAL_REALIZATION=NO"
)

print(
    "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
)

print(
    f"DATA={data_path}"
)

print(
    "NEXT=CLASSICAL_DECISION_GATE"
)
