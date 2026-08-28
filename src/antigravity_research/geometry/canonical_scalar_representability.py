"""Canonical-scalar representability and Derrick-stability gate for 006D.

PURPOSE
-------
Determine how far the finite, locally conserved stress-energy distribution
constructed in Simulation 006D can be interpreted as stress-energy produced
by ordinary canonical scalar fields.

SCIENTIFIC QUESTION
-------------------
Can the 006D distributed support collar arise from static canonical scalar
fields, and if its stress tensor is locally representable, can such a field
configuration be stable?

This module deliberately separates:

1. pointwise algebraic representability;
2. symmetry requirements;
3. global Derrick / virial stability.

PHYSICAL MODEL
--------------
Consider N real canonical scalar fields phi_a in flat spacetime with

    L
    =
    -1/2 sum_a partial_mu phi_a partial^mu phi_a
    - V(phi_1, ..., phi_N).

For a static field configuration,

    epsilon
    =
    1/2 sum_a |grad phi_a|^2
    + V

and

    T_ij
    =
    sum_a partial_i phi_a partial_j phi_a
    - epsilon delta_ij.

Therefore

    M_ij
    =
    T_ij + epsilon delta_ij

is the Gram matrix of the spatial field gradients:

    M_ij
    =
    sum_a partial_i phi_a partial_j phi_a.

For a diagonal stress tensor in an orthonormal cylindrical basis,

    M_rr       = epsilon + p_r
    M_phiphi   = epsilon + p_phi
    M_zz       = epsilon + p_z.

A necessary and locally sufficient algebraic condition for arbitrary enough
canonical scalar components is therefore that M be positive semidefinite.

The minimum number of real scalar gradient components required locally is at
least rank(M).

POTENTIAL RECONSTRUCTION
------------------------
For canonical static scalar fields,

    V
    =
    -1/2 (
        epsilon + p_r + p_phi + p_z
    ).

This is a pointwise identity if the stress tensor is exactly reproduced.

STRICT AXISYMMETRY
------------------
If every real scalar field is itself strictly axisymmetric,

    partial_phi phi_a = 0

for every a, and hence

    M_phiphi = 0.

Therefore any region with

    epsilon + p_phi > 0

cannot be reproduced by strictly axisymmetric scalar fields.

An axisymmetric stress tensor may still be produced by fields with angular
phase/winding dependence, for example a complex scalar represented as two real
components.

DERRICK / VIRIAL GATE
---------------------
Define

    E
    =
    integral epsilon dV

and

    P
    =
    integral (
        p_r + p_phi + p_z
    ) dV.

For a canonical static scalar realization,

    K
    =
    1/2 integral sum_i M_ii dV
    =
    (3E + P)/2

is the integrated gradient energy, while

    U
    =
    integral V dV
    =
    -(E + P)/2.

Under the standard three-dimensional Derrick scaling

    phi_lambda(x)
    =
    phi(lambda x),

the energy is

    E(lambda)
    =
    K/lambda
    +
    U/lambda^3.

Therefore

    E'(1)
    =
    P

and

    E''(1)
    =
    -3E - 5P.

A compact static source obeying the Laue condition

    P = 0

is stationary under the dilation but has

    E''(1)
    =
    -3E < 0

whenever E > 0.

Thus the exact 006D stress pattern cannot be a stable minimum of a pure static
canonical multi-scalar theory under the standard Derrick assumptions.

This is a stability result for that field-theory class.  It is not a universal
no-go theorem for:

- gauge fields;
- conserved Noether charge;
- stationary time-dependent fields;
- current-carrying condensates;
- higher-derivative theories;
- nonlinear self-gravity;
- externally constrained systems.

INDEPENDENT 006D PROFILE RECONSTRUCTION
---------------------------------------
This module independently re-implements the radial stress profile documented
by Simulation 006D rather than importing or modifying the simulation.

The dimensionless optimized geometry is

    alpha = 1.437500564637
    beta  = 4.701437405300.

For regularization scale s,

    inner_width = s/4
    outer_width = s.

Define

    q = r p_r

and

    p_phi = dq/dr.

The core, transfer annulus, smooth inner blend, and finite outer collar follow
the documented 006D construction.

Energy density is

    epsilon = max(|p_r|, |p_phi|)

and

    p_z = 0.

The vertical profile used by 006D is positive and common to all nonzero stress
components.  Away from its zero endpoints it multiplies the Gram matrix by a
positive scalar and therefore does not change rank or positive-semidefinite
classification.  Because it is normalized through thickness, the radial
surface integrals used here reproduce the corresponding integrated virial
ratios.

UNITS
-----
The reconstructed 006D profile is dimensionless in the same normalization as
the original simulation.

All representability relations are algebraic and unit-independent as long as
energy density and pressures use the same units.

SIGN CONVENTIONS
----------------
Positive pressure means compression.

Negative pressure means tension.

ASSUMPTIONS
-----------
- static flat-background field theory for the representability gate;
- canonical positive-sign scalar kinetic terms;
- finite localized source;
- standard Derrick scaling is an admissible variation;
- no gauge fields;
- no conserved time-dependent charge;
- no higher-derivative stabilizing terms;
- no nonlinear gravitational stabilization.

VALIDATION
----------
Validation includes:

- known domain-wall stress decomposition;
- known 006B stress-transfer annulus decomposition;
- smooth outer termination;
- dense positive-semidefinite checks;
- independent Laue integral;
- exact virial identities;
- negative Derrick second variation.

LIMITATIONS
-----------
Local Gram representability does not prove that one globally defined set of
fields and one physically motivated potential reproduce the entire source.

The Derrick result does not exclude theories containing additional stabilizing
sectors outside the canonical static scalar assumptions.

RELATED FILES
-------------
simulations/006d_finite_thickness_conserved_source.py
simulations/008b_distributed_field_representability_gate.py
tests/known_solutions/test_canonical_scalar_representability.py

CLAIM CLASSIFICATION
--------------------
ANALYTICAL_FIELD_THEORY_REPRESENTABILITY_AND_STABILITY_GATE
"""

from __future__ import annotations

from dataclasses import dataclass
import math

from scipy.integrate import quad


ALPHA_006D = 1.437500564637
BETA_006D = 4.701437405300
FINEST_SCALE_006D = 0.00625


@dataclass(frozen=True)
class ScalarDecomposition:
    """Canonical-scalar decomposition of a diagonal static stress tensor."""

    gram_r: float
    gram_phi: float
    gram_z: float
    potential: float

    def rank(
        self,
        tolerance: float = 1.0e-12,
    ) -> int:
        """Return rank of the diagonal kinetic Gram matrix."""

        return sum(
            value > tolerance
            for value in (
                self.gram_r,
                self.gram_phi,
                self.gram_z,
            )
        )

    def is_positive_semidefinite(
        self,
        tolerance: float = 1.0e-12,
    ) -> bool:
        """Return whether the diagonal kinetic Gram matrix is PSD."""

        return min(
            self.gram_r,
            self.gram_phi,
            self.gram_z,
        ) >= -tolerance


@dataclass(frozen=True)
class SurfaceStress:
    """Dimensionless surface-integrated 006D stress state."""

    epsilon: float
    p_r: float
    p_phi: float
    p_z: float = 0.0

    def scalar_decomposition(
        self,
    ) -> ScalarDecomposition:
        """Return canonical-scalar Gram entries and reconstructed potential."""

        return decompose_diagonal_stress(
            self.epsilon,
            self.p_r,
            self.p_phi,
            self.p_z,
        )


@dataclass(frozen=True)
class DerrickDiagnostics:
    """Integrated canonical-scalar virial and scaling diagnostics."""

    total_energy: float
    pressure_trace_integral: float
    gradient_energy: float
    potential_energy: float
    first_scaling_derivative: float
    second_scaling_derivative: float

    def stationary(
        self,
        relative_tolerance: float = 1.0e-10,
    ) -> bool:
        """Return whether the first scaling derivative is negligible."""

        scale = max(
            abs(self.total_energy),
            1.0,
        )

        return (
            abs(self.first_scaling_derivative)
            <= relative_tolerance * scale
        )

    def stable_against_uniform_scaling(
        self,
    ) -> bool:
        """Return whether the stationary scaling mode has positive curvature."""

        return (
            self.stationary()
            and self.second_scaling_derivative > 0.0
        )


def _finite(
    name: str,
    value: float,
) -> None:
    """Require a finite scalar input."""

    if not math.isfinite(value):
        raise ValueError(
            f"{name} must be finite"
        )


def _positive(
    name: str,
    value: float,
) -> None:
    """Require a finite positive scalar input."""

    _finite(name, value)

    if value <= 0.0:
        raise ValueError(
            f"{name} must be positive"
        )


def smoothstep(
    t: float,
) -> float:
    """Return cubic smoothstep."""

    return t * t * (3.0 - 2.0 * t)


def smoothstep_prime(
    t: float,
) -> float:
    """Return derivative of cubic smoothstep with respect to t."""

    return 6.0 * t * (1.0 - t)


def decompose_diagonal_stress(
    epsilon: float,
    p_r: float,
    p_phi: float,
    p_z: float,
) -> ScalarDecomposition:
    """Return the canonical-scalar kinetic Gram diagonal and potential.

    For static canonical scalar fields,

        M_ii = epsilon + p_i

    and

        V = -(epsilon + p_r + p_phi + p_z)/2.
    """

    for name, value in (
        ("epsilon", epsilon),
        ("p_r", p_r),
        ("p_phi", p_phi),
        ("p_z", p_z),
    ):
        _finite(name, value)

    return ScalarDecomposition(
        gram_r=epsilon + p_r,
        gram_phi=epsilon + p_phi,
        gram_z=epsilon + p_z,
        potential=(
            -0.5
            * (
                epsilon
                + p_r
                + p_phi
                + p_z
            )
        ),
    )


def strictly_axisymmetric_scalars_sufficient(
    decomposition: ScalarDecomposition,
    tolerance: float = 1.0e-12,
) -> bool:
    """Return whether fields with zero azimuthal derivative could suffice.

    Strictly axisymmetric real scalar fields have zero phi-gradient and
    therefore require M_phiphi = 0.
    """

    return (
        abs(decomposition.gram_phi)
        <= tolerance
    )


def regularized_006d_q_and_prime(
    radius: float,
    scale: float = FINEST_SCALE_006D,
) -> tuple[float, float]:
    """Independently reconstruct q=r*p_r and dq/dr from Simulation 006D."""

    _finite("radius", radius)
    _positive("scale", scale)

    if radius < 0.0:
        raise ValueError(
            "radius must be nonnegative"
        )

    alpha = ALPHA_006D
    beta = BETA_006D

    inner_width = scale / 4.0
    outer_width = scale

    if inner_width >= alpha:
        raise ValueError(
            "scale is too large for the documented 006D inner geometry"
        )

    if radius <= 0.0:
        return 0.0, -1.0

    inner_lo = alpha - inner_width
    inner_hi = alpha + inner_width

    q_core = -radius
    qp_core = -1.0

    q_annulus = (
        -(alpha * alpha)
        / radius
    )

    qp_annulus = (
        alpha * alpha
        / (radius * radius)
    )

    if radius < inner_lo:
        return q_core, qp_core

    if radius <= inner_hi:
        t = (
            (radius - inner_lo)
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

    if radius < beta:
        return q_annulus, qp_annulus

    if radius <= beta + outer_width:
        t = (
            (radius - beta)
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


def regularized_006d_surface_stress(
    radius: float,
    scale: float = FINEST_SCALE_006D,
) -> SurfaceStress:
    """Return independently reconstructed 006D surface stress."""

    q, qp = regularized_006d_q_and_prime(
        radius,
        scale,
    )

    if radius == 0.0:
        p_r = -1.0
    else:
        p_r = q / radius

    p_phi = qp

    epsilon = max(
        abs(p_r),
        abs(p_phi),
    )

    return SurfaceStress(
        epsilon=epsilon,
        p_r=p_r,
        p_phi=p_phi,
        p_z=0.0,
    )


def regularized_006d_breakpoints(
    scale: float = FINEST_SCALE_006D,
) -> tuple[float, ...]:
    """Return radial integration boundaries for the reconstructed profile."""

    _positive("scale", scale)

    inner_width = scale / 4.0

    return (
        0.0,
        ALPHA_006D - inner_width,
        ALPHA_006D + inner_width,
        BETA_006D,
        BETA_006D + scale,
    )


def _piecewise_radial_integral(
    function,
    scale: float,
) -> float:
    """Integrate across every profile interface independently."""

    total = 0.0

    points = regularized_006d_breakpoints(
        scale
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


def integrated_006d_energy_and_pressure_trace(
    scale: float = FINEST_SCALE_006D,
) -> tuple[float, float]:
    """Return dimensionless E and integrated spatial pressure trace.

    The normalized vertical profile used by 006D integrates to one, so the
    surface-integrated radial stress quantities give the same total ratios.

    The overall factor 2*pi is retained.
    """

    energy = (
        2.0
        * math.pi
        * _piecewise_radial_integral(
            lambda radius:
                radius
                * regularized_006d_surface_stress(
                    radius,
                    scale,
                ).epsilon,
            scale,
        )
    )

    pressure_trace = (
        2.0
        * math.pi
        * _piecewise_radial_integral(
            lambda radius:
                radius
                * (
                    regularized_006d_surface_stress(
                        radius,
                        scale,
                    ).p_r
                    +
                    regularized_006d_surface_stress(
                        radius,
                        scale,
                    ).p_phi
                ),
            scale,
        )
    )

    return (
        energy,
        pressure_trace,
    )


def canonical_scalar_derrick_diagnostics(
    total_energy: float,
    pressure_trace_integral: float,
) -> DerrickDiagnostics:
    """Return canonical-scalar kinetic, potential, and scaling diagnostics.

    For a static canonical scalar representation,

        K = (3E + P)/2
        U = -(E + P)/2

    where

        P = integral sum_i p_i dV.

    Under

        phi_lambda(x) = phi(lambda x),

        E(lambda) = K/lambda + U/lambda^3.

    Therefore

        E'(1)  = P
        E''(1) = -3E - 5P.
    """

    _positive(
        "total_energy",
        total_energy,
    )

    _finite(
        "pressure_trace_integral",
        pressure_trace_integral,
    )

    gradient_energy = (
        0.5
        * (
            3.0 * total_energy
            + pressure_trace_integral
        )
    )

    potential_energy = (
        -0.5
        * (
            total_energy
            + pressure_trace_integral
        )
    )

    first_derivative = (
        pressure_trace_integral
    )

    second_derivative = (
        -3.0 * total_energy
        - 5.0 * pressure_trace_integral
    )

    return DerrickDiagnostics(
        total_energy=total_energy,
        pressure_trace_integral=pressure_trace_integral,
        gradient_energy=gradient_energy,
        potential_energy=potential_energy,
        first_scaling_derivative=first_derivative,
        second_scaling_derivative=second_derivative,
    )
