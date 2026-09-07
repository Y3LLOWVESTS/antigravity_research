"""032V19R5 universal two-scalar quantum-force diagnostics.

PURPOSE
-------
Test an empirical consequence of the CURRENT LOW-ENERGY pure-j=0
kinetic-conformal operator before spending another run on UV completion.

The active branch uses

    A(X)
        =
        1
        -
        C1 X

with

    X
        =
        (partial phi)^2

and

    C1
        =
        1/(2 M^4).

For nonrelativistic matter the same operator produces the matter kinetic
loading already used by the finite-payload solver,

    epsilon
        =
        rho c^2/M^4
        =
        2 C1 rho_nat.

Therefore homogeneous matter has the quadratic scalar action

    L_phi
        ~
        -1/2
        Z
        (partial phi)^2

with

    Z
        =
        1 + epsilon.

The present run studies the OFF-STATE quantum force caused by this quadratic
matter coupling.

No classical source field is required.

WEAK-MATTER TWO-SCALAR FORCE
----------------------------
For a nonrelativistic point mass the worldline coupling has magnitude

    lambda_i
        =
        m_i C1

multiplying

    O
        =
        (partial phi)^2.

For a canonically normalized massless scalar in four Euclidean dimensions,

    G(x)
        =
        1/(4 pi^2 x^2).

The connected correlator is

    <O(x) O(0)>_c
        =
        6/(pi^4 x^8).

Using

    integral d tau
    /(tau^2+r^2)^4
        =
        5 pi/(16 r^7),

one obtains

    V_2phi(r)
        =
        - K
        C1^2
        m1 m2
        /r^7

with

    K
        =
        15/(8 pi^3).

The force is attractive for equal-sign universal matter coupling.

DBI NORMALIZATION CROSS-CHECK
-----------------------------
Bonifacio et al., JHEP 07 (2020) 056, Eq. (6.9), find the leading DBI
two-scalar potential coefficient

    3/(128 pi^3).

The present pure-trace coefficient satisfies

    [15/(8 pi^3)]
    /
    [3/(128 pi^3)]
        =
        80.

The difference follows from the different derivative tensor structure and
vertex normalization.

WEAK HALF-SPACE LIMIT
---------------------
Pairwise integration of the r^-7 potential through two half spaces gives

    |P_Born|
        =
        3/(16 pi^2)
        C1^2
        rho1 rho2
        /d^4.

This is valid only when the matter loading epsilon is small.

For dense matter in the current low-M candidate it is NOT small.

NONPERTURBATIVE MATERIAL RESUMMATION
------------------------------------
For a homogeneous region with constant positive Z, scalar fluctuations obey

    partial_mu
    (
        Z partial^mu phi
    )
        =
        0.

Across a planar interface:

    phi
        continuous,

    Z partial_n phi
        continuous.

Because the bulk wave speed is unchanged, the Euclidean interface reflection
amplitude is

    r
        =
        (Z - 1)/(Z + 1).

For a finite slab of thickness t surrounded by vacuum,

    r_slab(kappa)
        =
        r
        [1-exp(-2 kappa t)]
        /
        [1-r^2 exp(-2 kappa t)].

For two planar bodies separated by d, the zero-temperature scalar Casimir
pressure magnitude is

    |P|
        =
        hbar c
        /(32 pi^2 d^4)
        integral_0^infinity
        dy
        y^3
        R(y) exp(-y)
        /
        [1-R(y) exp(-y)],

where

    kappa
        =
        y/(2d)

and

    R
        =
        r_1 r_2.

For two half spaces this reduces to

    |P|
        =
        3 hbar c
        /(16 pi^2 d^4)
        Li_4(r_1 r_2).

Expanding for small epsilon reproduces the pairwise Born result above.

This gives an important independent reconstruction of the same low-energy
physics.

EMPIRICAL REFERENCE
-------------------
Decca et al. measured effective Casimir pressure using an Au-coated sapphire
sphere above an Au-coated polysilicon plate.

The supplementary experimental description gives approximately

    Au sphere layer
        =
        180 nm

    Au plate layer
        =
        210 nm

    sphere radius
        =
        151.3 micrometers.

At 200 nm separation their tabulated values are

    experimental pressure magnitude
        =
        510.50 mPa

    generalized-plasma theoretical pressure magnitude
        =
        511.26 mPa

    95 percent theory-minus-experiment half-width
        =
        8.40 mPa.

The present finite-film scout deliberately discards all scalar reflection
from the sapphire and polysilicon substrates.

That is a conservative omission for this diagnostic.

CLAIM LIMITS
------------
A red result directly falsifies the CURRENT PURE-j0 low-energy realization
unless additional low-energy physics changes the scalar pair-emission /
material-reflection amplitude.

It does not yet prove that every kinetic-conformal UV completion is
impossible.

Possible remaining loopholes include:

- j=2/disformal companion operators;
- other symmetry-required low-energy companions;
- a genuinely nonlinear material response not represented by the present
  quadratic kinetic coefficient;
- a cancellation mechanism that survives positivity, stability,
  universality, finite payload, and empirical constraints.

Those loopholes must be tested explicitly rather than assumed.

No negative mass is used.
"""

from __future__ import annotations

import math

from scipy.integrate import quad


EV_J = 1.602176634e-19
HBARC_EV_M = 1.973269804e-7
C_LIGHT = 299792458.0

PI = math.pi

TRACE_PAIR_COEFFICIENT = (
    15.0
    /
    (
        8.0
        * PI**3
    )
)

DBI_REFERENCE_COEFFICIENT = (
    3.0
    /
    (
        128.0
        * PI**3
    )
)


def metric_scale_from_c1_ev(
    c1_ev_m4: float,
) -> float:
    """Return M from C1=1/(2 M^4)."""

    c1 = float(
        c1_ev_m4
    )

    if c1 <= 0.0:
        raise ValueError(
            "positive C1 required"
        )

    return (
        1.0
        /
        (
            2.0
            * c1
        )
    )**0.25


def density_kg_m3_to_ev4(
    density_kg_m3: float,
) -> float:
    """Convert rest-mass density to natural-unit eV^4."""

    density = float(
        density_kg_m3
    )

    if density <= 0.0:
        raise ValueError(
            "density must be positive"
        )

    density_j_m3 = (
        density
        * C_LIGHT**2
    )

    return (
        density_j_m3
        * HBARC_EV_M**3
        / EV_J
    )


def matter_loading_from_c1(
    *,
    c1_ev_m4: float,
    density_kg_m3: float,
) -> dict[str, float]:
    """Return epsilon and Z for homogeneous nonrelativistic matter."""

    c1 = float(
        c1_ev_m4
    )

    rho = (
        density_kg_m3_to_ev4(
            density_kg_m3
        )
    )

    if c1 <= 0.0:
        raise ValueError(
            "positive C1 required"
        )

    epsilon = (
        2.0
        * c1
        * rho
    )

    z_factor = (
        1.0
        + epsilon
    )

    reflection = (
        (
            z_factor
            - 1.0
        )
        /
        (
            z_factor
            + 1.0
        )
    )

    return {
        "rho_ev4":
            rho,

        "epsilon":
            epsilon,

        "z_factor":
            z_factor,

        "interface_reflection":
            reflection,

        "born_material_limit":
            (
                epsilon
                < 0.1
            ),
    }


def trace_pair_force_coefficient() -> float:
    """Return 15/(8 pi^3)."""

    return (
        TRACE_PAIR_COEFFICIENT
    )


def dbi_reference_force_coefficient() -> float:
    """Return the published leading DBI coefficient 3/(128 pi^3)."""

    return (
        DBI_REFERENCE_COEFFICIENT
    )


def integrated_pairwise_pressure_coefficient() -> float:
    """Return the half-space coefficient after integrating r^-7.

    For

        V(r)
            =
            -K C1^2 m1 m2/r^7,

    integration over two half spaces gives

        |P|
            =
            (pi/10)
            K
            C1^2 rho1 rho2/d^4.

    With

        K=15/(8 pi^3)

    this is

        3/(16 pi^2).
    """

    return (
        PI
        / 10.0
        * TRACE_PAIR_COEFFICIENT
    )


def born_halfspace_pressure_pa(
    *,
    c1_ev_m4: float,
    density1_kg_m3: float,
    density2_kg_m3: float,
    separation_m: float,
) -> float:
    """Return weak-material pairwise half-space pressure magnitude."""

    c1 = float(
        c1_ev_m4
    )

    separation = float(
        separation_m
    )

    if (
        c1 <= 0.0
        or separation <= 0.0
    ):
        raise ValueError(
            "positive C1 and separation required"
        )

    rho1 = (
        density_kg_m3_to_ev4(
            density1_kg_m3
        )
    )

    rho2 = (
        density_kg_m3_to_ev4(
            density2_kg_m3
        )
    )

    d_nat = (
        separation
        / HBARC_EV_M
    )

    pressure_ev4 = (
        integrated_pairwise_pressure_coefficient()
        * c1**2
        * rho1
        * rho2
        / d_nat**4
    )

    return (
        pressure_ev4
        * EV_J
        / HBARC_EV_M**3
    )


def _slab_reflection(
    *,
    z_factor: float,
    kappa_m1: float,
    thickness_m: float | None,
) -> float:
    """Return Euclidean scalar reflection amplitude."""

    z_value = float(
        z_factor
    )

    kappa = float(
        kappa_m1
    )

    if z_value <= 0.0:
        raise ValueError(
            "positive kinetic factor required"
        )

    if kappa < 0.0:
        raise ValueError(
            "kappa cannot be negative"
        )

    interface = (
        (
            z_value
            - 1.0
        )
        /
        (
            z_value
            + 1.0
        )
    )

    if thickness_m is None:
        return interface

    thickness = float(
        thickness_m
    )

    if thickness <= 0.0:
        raise ValueError(
            "slab thickness must be positive"
        )

    attenuation = math.exp(
        -2.0
        * kappa
        * thickness
    )

    denominator = (
        1.0
        -
        interface**2
        * attenuation
    )

    return (
        interface
        * (
            1.0
            -
            attenuation
        )
        / denominator
    )


def scalar_casimir_pressure_pa(
    *,
    c1_ev_m4: float,
    density1_kg_m3: float,
    density2_kg_m3: float,
    separation_m: float,
    thickness1_m: float | None = None,
    thickness2_m: float | None = None,
) -> dict[str, float | bool]:
    """Return exact quadratic-material scalar Casimir pressure magnitude.

    Substrates behind finite slabs are deliberately omitted.
    """

    separation = float(
        separation_m
    )

    if separation <= 0.0:
        raise ValueError(
            "separation must be positive"
        )

    load1 = (
        matter_loading_from_c1(
            c1_ev_m4=
                c1_ev_m4,

            density_kg_m3=
                density1_kg_m3,
        )
    )

    load2 = (
        matter_loading_from_c1(
            c1_ev_m4=
                c1_ev_m4,

            density_kg_m3=
                density2_kg_m3,
        )
    )

    def integrand(
        y_value: float,
    ) -> float:
        y = float(
            y_value
        )

        if y <= 0.0:
            return 0.0

        kappa = (
            y
            /
            (
                2.0
                * separation
            )
        )

        r1 = (
            _slab_reflection(
                z_factor=
                    float(
                        load1[
                            "z_factor"
                        ]
                    ),

                kappa_m1=
                    kappa,

                thickness_m=
                    thickness1_m,
            )
        )

        r2 = (
            _slab_reflection(
                z_factor=
                    float(
                        load2[
                            "z_factor"
                        ]
                    ),

                kappa_m1=
                    kappa,

                thickness_m=
                    thickness2_m,
            )
        )

        product = (
            r1
            * r2
        )

        exponential = math.exp(
            -y
        )

        denominator = (
            1.0
            -
            product
            * exponential
        )

        return (
            y**3
            * product
            * exponential
            / denominator
        )

    integral, integration_error = quad(
        integrand,
        0.0,
        80.0,
        epsabs=
            1.0e-11,
        epsrel=
            1.0e-10,
        limit=
            300,
    )

    hbar_c_j_m = (
        HBARC_EV_M
        * EV_J
    )

    pressure = (
        hbar_c_j_m
        /
        (
            32.0
            * PI**2
            * separation**4
        )
        * integral
    )

    return {
        "pressure_magnitude_pa":
            pressure,

        "force_sign":
            "ATTRACTIVE",

        "dimensionless_integral":
            integral,

        "integration_error":
            integration_error,

        "epsilon1":
            float(
                load1[
                    "epsilon"
                ]
            ),

        "epsilon2":
            float(
                load2[
                    "epsilon"
                ]
            ),

        "z1":
            float(
                load1[
                    "z_factor"
                ]
            ),

        "z2":
            float(
                load2[
                    "z_factor"
                ]
            ),

        "interface_r1":
            float(
                load1[
                    "interface_reflection"
                ]
            ),

        "interface_r2":
            float(
                load2[
                    "interface_reflection"
                ]
            ),

        "finite_slab1":
            (
                thickness1_m
                is not None
            ),

        "finite_slab2":
            (
                thickness2_m
                is not None
            ),

        "substrate_scalar_reflection_included":
            False,
    }


def empirical_pressure_gate(
    *,
    extra_pressure_pa: float,
    measured_pressure_pa: float,
    standard_theory_pressure_pa: float,
    confidence_halfwidth_pa: float,
) -> dict[str, float | bool]:
    """Compare an additional attractive pressure with Casimir data."""

    extra = float(
        extra_pressure_pa
    )

    measured = float(
        measured_pressure_pa
    )

    theory = float(
        standard_theory_pressure_pa
    )

    halfwidth = float(
        confidence_halfwidth_pa
    )

    if (
        extra < 0.0
        or measured <= 0.0
        or theory <= 0.0
        or halfwidth <= 0.0
    ):
        raise ValueError(
            "invalid empirical pressure input"
        )

    predicted_total = (
        theory
        + extra
    )

    mismatch = abs(
        predicted_total
        - measured
    )

    return {
        "predicted_total_pressure_pa":
            predicted_total,

        "absolute_theory_experiment_mismatch_pa":
            mismatch,

        "mismatch_over_95pct_halfwidth":
            (
                mismatch
                / halfwidth
            ),

        "extra_over_95pct_halfwidth":
            (
                extra
                / halfwidth
            ),

        "extra_over_measured_pressure":
            (
                extra
                / measured
            ),

        "excluded_at_declared_95pct_interval":
            (
                mismatch
                >
                halfwidth
            ),
    }


def soft_mass_range_scout(
    *,
    required_range_m: float,
    laboratory_separation_m: float,
) -> dict[str, float | bool]:
    """Check whether a soft mass compatible with device range matters in lab."""

    device_range = float(
        required_range_m
    )

    separation = float(
        laboratory_separation_m
    )

    if (
        device_range <= 0.0
        or separation <= 0.0
    ):
        raise ValueError(
            "positive lengths required"
        )

    maximum_mass_ev = (
        HBARC_EV_M
        / device_range
    )

    md_dimensionless = (
        maximum_mass_ev
        * separation
        / HBARC_EV_M
    )

    return {
        "maximum_mass_ev_for_required_range":
            maximum_mass_ev,

        "m_times_d_over_hbarc":
            md_dimensionless,

        "massless_laboratory_limit":
            (
                md_dimensionless
                <
                1.0e-3
            ),
    }


def laboratory_momentum_scout(
    *,
    separation_m: float,
    source_hard_scale_ev: float,
    metric_scale_ev: float,
) -> dict[str, float | bool]:
    """Compare q~hbar c/d with source and metric scales."""

    separation = float(
        separation_m
    )

    hard = float(
        source_hard_scale_ev
    )

    metric = float(
        metric_scale_ev
    )

    if (
        separation <= 0.0
        or hard <= 0.0
        or metric <= 0.0
    ):
        raise ValueError(
            "positive scales required"
        )

    q_ev = (
        HBARC_EV_M
        / separation
    )

    return {
        "q_ev":
            q_ev,

        "q_over_source_hard":
            (
                q_ev
                / hard
            ),

        "q_over_metric_scale":
            (
                q_ev
                / metric
            ),

        "below_source_hard_scale":
            (
                q_ev
                <
                hard
            ),

        "below_metric_scale":
            (
                q_ev
                <
                metric
            ),
    }
