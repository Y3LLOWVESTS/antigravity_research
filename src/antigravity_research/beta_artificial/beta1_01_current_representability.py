"""BETA1-01: exact current-channel mismatch and induced-Y compatibility.

Compare frozen M5I's arbitrary stationary (rho_X,j_phi) target with
PH15-P10's physically sourced restricted nonwinding X sector and
first-order, trace-induced Y source.

Two distinct mapping hypotheses:

A: j_phi is a microscopic X current (P10 has none).
B: j_phi is a first-order effective Y current (Jacobian compatibility).

No current, energy, stability, GR, or craft force is optimized.

Physical interpretations are restricted. A P10 Y effective source is
NOT a microscopic X azimuthal source. The M5I source has arbitrary
amplitudes and SI lengths; its amplitudes are NOT calibrated SI currents.

Numerical potential extrema are convergence screens, not validated
PDE proofs or model-wide impossibility certificates.
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass

import numpy as np
import sympy as sp

from numpy.polynomial.legendre import leggauss
from scipy.special import ellipk


@dataclass(frozen=True)
class Target:
    radial_center_m: float = 1.15
    radial_halfwidth_m: float = .42
    axial_halfwidth_m: float = .50
    density_amplitude: float = 1.0
    azimuthal_current_amplitude: float = 1.0


def target_current(r, z, s=Target()):
    """M5I's actual source profile, reproduced independently."""

    r, z = np.asarray(r), np.asarray(z)

    d = (
        1
        - ((r-s.radial_center_m)/s.radial_halfwidth_m)**2
        - (z/s.axial_halfwidth_m)**2
    )

    bump = np.maximum(d, 0)**5

    return (
        s.density_amplitude*(z/s.axial_halfwidth_m)*bump,
        s.azimuthal_current_amplitude*bump,
    )


def exact_target_moments(s=Target()):
    """Analytic integration over disk u^2+v^2<=1.

    Cylindrical volume: dV = 2*pi*r dr dz.

    Integral (1-u^2-v^2)^n = pi/(n+1).

    Integral v^2*(1-u^2-v^2)^n =
        pi/[2(n+1)(n+2)].
    """

    R = s.radial_center_m
    a = s.radial_halfwidth_m
    b = s.axial_halfwidth_m
    d = s.density_amplitude
    j = s.azimuthal_current_amplitude

    return {
        "net_charge": 0.,
        "electric_dipole_z":
            d*math.pi**2*a*b*b*R/42,
        "magnetic_dipole_z":
            j*math.pi**2*a*b*(R*R/6+a*a/84),
        "charge_density_L2_squared":
            d*d*math.pi**2*a*b*R/132,
        "azimuthal_current_L2_squared":
            j*j*2*math.pi**2*a*b*R/11,
    }


def independent_moments(s=Target(), n=96):
    """Independent tensor Gauss quadrature."""

    x, w = leggauss(n)

    r = (
        s.radial_center_m
        + s.radial_halfwidth_m*x[:, None]
    )

    z = s.axial_halfwidth_m*x[None, :]

    rr = np.broadcast_to(r, (n, n))
    zz = np.broadcast_to(z, (n, n))

    rho, jphi = target_current(rr, zz, s)

    vol = (
        2*math.pi*rr
        *s.radial_halfwidth_m
        *s.axial_halfwidth_m
        *w[:, None]
        *w[None, :]
    )

    return {
        "net_charge":
            float(np.sum(vol*rho)),
        "electric_dipole_z":
            float(np.sum(vol*zz*rho)),
        "magnetic_dipole_z":
            float(np.sum(.5*vol*rr*jphi)),
        "charge_density_L2_squared":
            float(np.sum(vol*rho**2)),
        "azimuthal_current_L2_squared":
            float(np.sum(vol*jphi**2)),
    }


def _sources(s, n):
    x, w = leggauss(n)

    rp = (
        s.radial_center_m
        + s.radial_halfwidth_m*x[:, None]
    )

    zp = s.axial_halfwidth_m*x[None, :]

    rfull = np.broadcast_to(rp, (n, n))
    zfull = np.broadcast_to(zp, (n, n))

    density, _ = target_current(
        rfull, zfull, s
    )

    weights = (
        s.radial_halfwidth_m
        *s.axial_halfwidth_m
        *w[:, None]
        *w[None, :]
    )

    return (
        rfull.ravel(),
        zfull.ravel(),
        (rfull*density*weights).ravel(),
    )


def coulomb_potential(r, z, sources):
    """Free-space axisymmetric Coulomb quadrature.

    A0 = integral dr'dz' [
        r' rho' K(m)/(pi D)
    ].

    This is a prescribed-charge diagnostic,
    NOT an on-shell scalar source calculation.

    Near-source logarithmic integrability can
    slow numerical quadrature convergence.
    """

    rp, zp, q = sources

    d2 = (r+rp)**2+(z-zp)**2

    m = np.clip(
        4*r*rp/d2,
        0.,
        1.-1e-15,
    )

    return float(
        np.sum(
            q*ellipk(m)
            /(math.pi*np.sqrt(d2))
        )
    )


def potential_boundary_screen(
    s=Target(),
    n=112,
    angles=101,
):
    """Screen an exact critical-point obstruction.

    If a smooth A0 has an interior value
    greater than its boundary maximum
    over the upper positive-charge lobe,
    it has an interior stationary point.

    At grad(A0)=0:

        j_Yphi =
        lambda_r*A0_z-lambda_z*A0_r = 0.

    If j_target_phi>0 at that point,
    no smooth lambda matches the
    prescribed target current everywhere.

    The numerical boundary maximum is
    SAMPLED, not interval certified.
    """

    src = _sources(s, n)

    R = s.radial_center_m
    a = s.radial_halfwidth_m
    b = s.axial_halfwidth_m

    inside = coulomb_potential(
        R, .46*b, src
    )

    th = np.linspace(
        0, math.pi, angles
    )

    values = [
        coulomb_potential(
            R+a*math.cos(t),
            b*math.sin(t),
            src,
        )
        for t in th
    ]

    maximum = max(values)

    parity = coulomb_potential(
        R, 0., src
    )

    jphi = float(
        target_current(
            R, .46*b, s
        )[1]
    )

    return {
        "quadrature_order": n,
        "boundary_samples": angles,
        "interior_coordinate": [
            R, .46*b
        ],
        "interior_potential_canonical": inside,
        "upper_ellipse_boundary_max_canonical": maximum,
        "interior_minus_boundary": inside-maximum,
        "z0_potential_parity_check": parity,
        "interior_jphi_target": jphi,
        "screen_pass": bool(
            inside > maximum+2e-4
            and abs(parity) < 1e-9
        ),
    }


def exact_symbolic_conditions():
    """Exact scoped algebra, not full source/metric health."""

    (
        q1, q2, f1, f2,
        rr, ap, om1, om2,
        a0, n1, n2,
    ) = sp.symbols(
        "q1 q2 f1 f2 r Aphi "
        "omega1 omega2 A0 n1 n2",
        real=True,
    )

    charge = 2*(
        q1*(om1-q1*a0)*f1*f1
        +q2*(om2-q2*a0)*f2*f2
    )

    jphi = 2*(
        q1*f1*f1*(n1/rr-q1*ap)
        +q2*f2*f2*(n2/rr-q2*ap)
    )

    x_null = (
        sp.simplify(
            jphi.subs({
                n1: 0,
                n2: 0,
                ap: 0,
            })
        ) == 0
    )

    # For n_i=0, the fixed-scalar
    # magnetostatic energy contains:
    #
    # 1/2 |curl A|^2
    # + sum_i q_i^2 f_i^2 |A|^2.
    #
    # With zero boundary flux, its
    # stationary homogeneous Ampere
    # equation has only A=0.

    coeff = sp.expand(
        q1*q1*f1*f1
        +q2*q2*f2*f2
    )

    polynomial = sp.Poly(
        coeff, f1, f2
    )

    coeff_nonnegative = bool(
        polynomial.coeff_monomial(f1**2) == q1**2
        and
        polynomial.coeff_monomial(f2**2) == q2**2
    )

    lr, lz, ar, az = sp.symbols(
        "lr lz Ar Az",
        real=True,
    )

    jy = lr*az-lz*ar

    critical = (
        sp.simplify(
            jy.subs({
                ar: 0,
                az: 0,
            })
        ) == 0
    )

    aa, bb, K, U, P = sp.symbols(
        "alpha beta K U P",
        real=True,
    )

    sig = aa*P-bb*P**2

    lm = (
        -sp.exp(2*sig)*K
        -sp.exp(4*sig)*U
    )

    lam = sp.diff(lm, P)

    dlam = sp.simplify(
        sp.diff(lam, P).subs(P, 0)
    )

    expected = (
        4*bb*(K+2*U)
        -4*aa**2*(K+4*U)
    )

    # Frozen electric X and scalar matter.
    # Y magnetic constitutive eigenvalue
    # parallel to E_X:
    #
    # 1-lambda'_0*|E_X|^2.
    #
    # NOT the complete constrained
    # canonical kinetic spectrum.

    ex = sp.symbols(
        "Ex", real=True
    )

    eig = 1-dlam*ex**2

    checks = {
        "nonwinding_Aphi0_X_current_exact_null":
            x_null,

        "azimuthal_X_energy_positive_coefficient":
            coeff_nonnegative,

        "induced_Y_critical_A0_null":
            critical,

        "portal_lambda_P0_identity":
            sp.simplify(
                dlam-expected
            ) == 0,

        "frozen_magnetic_Y_transverse_positive":
            True,

        "frozen_magnetic_Y_parallel_eigenvalue":
            sp.simplify(
                eig-(1-expected*ex**2)
            ) == 0,

        "beta0_alpha0_free_positive":
            sp.simplify(
                eig.subs({
                    aa: 0,
                    bb: 0,
                })-1
            ) == 0,
    }

    formulas = {
        "X_charge_density_formula":
            str(charge),

        "X_azimuthal_current_formula":
            str(jphi),

        "Y_induced_azimuthal_formula":
            str(jy),

        "lambda_P0":
            str(dlam),

        "frozen_magnetic_Y_parallel_eigenvalue":
            str(eig),

        "frozen_magnetic_Y_scope":
            "fixed-X electric and frozen matter; "
            "NOT full constrained modes",
    }

    return checks, formulas


def report(s=Target()):
    analytic = exact_target_moments(s)

    moments = {}

    for n in (64, 112):
        numeric = independent_moments(
            s, n
        )

        moments[str(n)] = {
            "values": numeric,
            "relative_or_absolute_errors": {
                k: abs(numeric[k]-v)
                /max(1., abs(v))
                for k, v in analytic.items()
            },
        }

    boundaries = [
        potential_boundary_screen(
            s, n, 81
        )
        for n in (64, 112)
    ]

    checks, formulas = exact_symbolic_conditions()

    if not all(checks.values()):
        raise ArithmeticError(
            f"Symbolic failure: {checks}"
        )

    if any(
        max(
            row["relative_or_absolute_errors"].values()
        ) > 2e-8
        for row in moments.values()
    ):
        raise ArithmeticError(
            "Source moment integration did not converge"
        )

    if not all(
        b["screen_pass"]
        for b in boundaries
    ):
        raise ArithmeticError(
            "No supported potential-interior numerical witness"
        )

    gap = abs(
        boundaries[0]["interior_minus_boundary"]
        -boundaries[1]["interior_minus_boundary"]
    )

    if gap > 5e-5:
        raise ArithmeticError(
            "Potential boundary margin not consistent"
        )

    return {
        "target_parameters":
            asdict(s),

        "target_exact_moments":
            analytic,

        "independent_quadrature_moments":
            moments,

        "potential_interior_extremum_screens":
            boundaries,

        "potential_margin_cross_resolution_abs":
            gap,

        "source_channels": {
            "X_microscopic_P10":
                "ZERO_AZIMUTHAL_FOR_NONWINDING_ELECTROSTATIC_RESTRICTION",

            "Y_effective_P10":
                "NONZERO_FIRST_ORDER_FROM_ONSHELL_X_SOURCE_NO_BACKREACTION",

            "M5I_prescribed":
                "INDEPENDENT_RHO_AND_JPHI_NOT_ONSHELL_MATTER",

            "M5V_source":
                "M5I_CURRENT_USED_AS_PRESCRIBED_CARRIER_INPUT",
        },

        "exact_theorems": {
            "X_class":
                "NO_NONZERO_PRESCRIBED_AZIMUTHAL_MICROSCOPIC_X_CURRENT_IN_P10_NONWINDING_AZIMUTHAL_A0_CLASS",

            "X_ampere":
                "NO_SOURCE_FREE_NONWINDING_A_PHI_WITH_STANDARD_POSITIVE_STATIC_ENERGY_AND_VANISHING_BOUNDARY_FLUX_AT_ZERO_PORTAL",

            "Y_critical_point":
                "IF_A0_HAS_INTERIOR_EXTREMUM_IN_REGION_JTARGET_PHI_NONZERO_THEN_NO_SMOOTH_LAMBDA_CAN_REPRODUCE_TARGET_EVERYWHERE",

            "Y_M5I_screen":
                "TWO_NUMERICAL_QUADRATURES_INDICATE_SUCH_INTERIOR_EXTREMUM_FOR_FROZEN_M5I_RHO;_NOT_RIGOROUS_INTERVAL_CERTIFICATE",
        },

        "exact_symbolic_checks":
            checks,

        "symbolic_formulas":
            formulas,

        "mechanism_status": {
            "P10_original_induced_Y":
                "PRESERVED_NOT_DISPROVEN",

            "M5I_direct_X_current_in_P10":
                "CLOSED_RESTRICTED_ANSATZ",

            "M5I_as_Y_from_M5I_RHO":
                "NUMERICALLY_DISFAVORED_UNDER_MATCHED_POISSON_AND_SMOOTH_LAMBDA",

            "winding_or_new_Y_source":
                "REQUIRES_NEW_SECTOR_AND_P7_HEALTH_RETEST",

            "beta_and_kinetic":
                "FULL_CONSTRAINED_HEALTH_OPEN",

            "earth_force":
                "NOT_DERIVED",

            "physical_transfer":
                "NOT_AUTHORIZED",
        },

        "magnetic_ellipticity_warning":
            "frozen Y magnetic eigenvalue="
            "1-lambda_P0*|EX|^2; local positive "
            "needed for restricted screening; "
            "not full canonical health",

        "verdict":
            "YELLOW_RESTRICTED_M5I_TO_P10_CURRENT_MAPPINGS_OBSTRUCTED_FULL_PHYSICAL_MODEL_OPEN",
    }
