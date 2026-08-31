#!/usr/bin/env python3
"""019A — Wilson-line-sequestered pair-scalar UV-protection gate.

PURPOSE
-------
Test a minimal literature-motivated ultraviolet protection mechanism for the
project's surviving low-energy material-specific two-body scalar operator after
the 018B two-current/KLS general-relativistic realization was demoted by the
confirmed 018C m=2 instability.

ACTIVE SCIENTIFIC QUESTION
--------------------------
Can a technically natural ultralight scalar be realized as a Wilson-line phase
of a local four-dimensional deconstructed gauge theory while simultaneously
producing the required material-pair Wilson coefficient and suppressing the
leading local/same-sector scalar response far below the project's conservative
ordinary-matter leakage allowance?

This is deliberately a UV-PROTECTION WITNESS gate.  It is not yet a Standard
Model material completion, a fifth-force experimental closure, a stellar or
cosmological completion, or a practical antigravity device.

LOW-ENERGY TARGET INHERITED FROM THE PROJECT
---------------------------------------------
The previously verified nonrelativistic pair EFT contains

    H_pair = C_phi * phi * A^dagger B^dagger B A

with

    C_phi = 9.536416387852626e-20 eV^-3.

The selected fifth-force range is 5 km, corresponding to

    m_phi = 3.946539608e-11 eV.

The terrestrial background used by the prior material calculation is

    phi_earth = 1.690631280830914e10 eV.

The conservative target-equivalent leakage allowance is

    f_leak = 5.772961445324848e-7.

DECONSTRUCTED WILSON-LINE MODEL
--------------------------------
Consider a periodic N-site U(1)^N moose with equal link scale mu.  A charged
complex messenger X_j has dimensionless mass-squared matrix

    L_jj = rho^2 + 2,

    L_{j,j+1} = -exp(+i theta/N),
    L_{j+1,j} = -exp(-i theta/N),

where

    theta = phi / f

is the gauge-invariant Wilson phase.  The physical messenger matrix is

    M_X^2 = mu^2 L(theta).

Its exact eigenvalues are

    lambda_n(theta)
      = rho^2 + 2
        - 2 cos[(2 pi n + theta)/N].

The endpoint matter operators can be realized by gauge-charged scalar/fermion
bilinears at distinct moose sites.  Integrating out X produces a nonlocal
cross-sector operator.  We normalize the endpoint sources so that its
coefficient is

    C_AB(theta)
      = - y_A y_B / mu^2 * Re[i G_0d(theta)],

where

    G(theta) = L(theta)^(-1).

The relative factor i is a discrete Z4 phase assignment, not a continuous
cancellation.  Around theta=0,

    d Re[i G_0d] / d theta != 0,

while the local same-site propagator obeys

    G_00(theta) = G_00(-theta)

and therefore

    d G_00 / d theta |_(theta=0) = 0.

The desired pair coefficient is

    C_phi(theta)
      = y_A y_B / (mu^2 f)
        * |d Re[i G_0d] / d theta|.

OPERATING-POINT MATCHING
------------------------
Unlike an expansion only at phi=0, this gate matches C_phi at the actual
terrestrial background

    theta_earth = phi_earth / f.

For each microscopic choice (N, rho, d, y_A y_B), mu and f are solved so that
BOTH

    C_phi(theta_earth) = C_phi,target

and

    m_phi = m_phi,target.

WILSON-LINE NATURALNESS
-----------------------
The one-loop Coleman-Weinberg potential of the messenger is

    V_CW(theta)
      = mu^4/(64 pi^2)
        sum_n lambda_n(theta)^2
        [log lambda_n(theta) - 3/2]

up to theta-independent renormalization terms.  The curvature

    kappa_CW = d^2/dtheta^2 sum_n ... |_(theta=0)

produces

    m_phi^2 = mu^4 kappa_CW / (64 pi^2 f^2).

For N >= 3 the theta-dependent one-loop term is nonlocal in theory space; the
UV divergent local invariants Tr L and Tr L^2 are theta independent.  This is
the finite Wilson-line Coleman-Weinberg mechanism discussed in the classic
5D/deconstruction literature.

LEAKAGE DIAGNOSTIC
------------------
At theta=0 the local linear response vanishes exactly by the Wilson-phase
reflection symmetry.  At the finite terrestrial background it need not vanish.
We therefore compute a deliberately conservative same-sector response proxy

    leakage_proxy
      = |d G_00/dtheta|_earth
        / |d Re[i G_0d]/dtheta|_earth.

This is NOT asserted to be the complete Standard Model one-body scalar charge.
It is a stronger-than-tree-level local Wilson-response diagnostic.  A complete
SM embedding must still calculate operator mixing into electron, nucleon,
quark/gluon, electromagnetic-binding, and generic-atom operators.

INPUTS / UNITS
--------------
All energies are in eV and natural units hbar=c=1 are used internally.

OUTPUTS
-------
The script prints:
- exact matrix/spectral propagator agreement;
- exact local Wilson symmetry at theta=0;
- one-loop UV-local trace-invariant protection;
- Coleman-Weinberg curvature by two independent methods;
- an operating-point solution for a selected moderate-coupling benchmark;
- pair-EFT matching at the terrestrial background;
- messenger/EFT scale separation;
- terrestrial local-response leakage proxy;
- pair-response nonlinearity across the terrestrial background;
- a broad discrete microscopic parameter-basin scan;
- blind wildcard diagnostics that are explicitly not evidence;
- a fail-closed branch decision and next scientific gate.

PROMOTION CONDITION
-------------------
019A may be GREEN only if all of the following hold:
1. exact propagator reconstruction passes;
2. the local linear Wilson response vanishes at the symmetry point;
3. the theta-dependent CW potential is locally UV protected;
4. the same microscopic parameters reproduce C_phi and m_phi;
5. messenger masses remain above the material EFT cutoff;
6. endpoint couplings remain perturbative;
7. the terrestrial Wilson excursion is controlled;
8. the conservative local-response proxy beats the leakage allowance by a
   substantial margin;
9. a nontrivial neighborhood of distinct microscopic points survives;
10. independent numerical reconstructions agree.

A GREEN result promotes only a PROTECTED RELATIVISTIC THEORY-SPACE WITNESS.
It does not establish that the Standard Model or a real material realizes the
required endpoint operators.

FALSIFIERS / STOP RULES
-----------------------
RED if:
- matching requires nonperturbative endpoint couplings;
- the messenger falls below the material EFT cutoff;
- Wilson-line naturalness cannot reproduce the ultralight mass;
- local response exceeds the leakage allowance;
- only an isolated fine-tuned point survives;
- matrix and spectral reconstructions disagree.

If GREEN, the next gate is 019B: explicit anomaly-free Standard Model/material
endpoint embedding plus complete one-body operator-mixing and exact current
5-km fifth-force bound closure.  Stellar/cosmological work remains after that.

LITERATURE ANCHORS
------------------
- C. T. Hill and A. K. Leibovich, "Deconstructing 5-D QED",
  arXiv:hep-ph/0205057.  Finite Wilson-line Coleman-Weinberg potential for
  N >= 3 in deconstructed QED.
- N. Arkani-Hamed, H.-C. Cheng, P. Creminelli, L. Randall,
  "Extranatural Inflation", arXiv:hep-th/0301218.  Nonlocal Wilson-line
  potentials protected by higher-dimensional gauge invariance.
- S. Hor, Y. Nakai, M. Suzuki, J. Xu,
  "Deconstructing the Extra-Dimensional Axion", arXiv:2606.02728.
  Four-dimensional deconstruction of Wilson-line protection and characteristic
  nonlocal suppression.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_019A_WILSON_LINE_SEQUESTERED_PAIR_SCALAR_UV_PROTECTION_GATE
"""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Callable

import mpmath as mp
import numpy as np
from scipy.optimize import brentq


# ---------------------------------------------------------------------------
# Project-inherited low-energy targets.
# ---------------------------------------------------------------------------

TARGET_C_PHI = 9.536416387852626e-20  # eV^-3
TARGET_M_PHI = 3.946539608e-11        # eV
EARTH_PHI = 1.690631280830914e10      # eV
MAX_LEAKAGE_FRACTION = 5.772961445324848e-7
MATERIAL_EFT_CUTOFF = 657.7566        # eV, approximately hbar*c/(3 Angstrom)

# Selected benchmark: moderate endpoint Yukawas rather than the NDA boundary.
SELECTED_N = 9
SELECTED_RHO = 3.0
SELECTED_SEPARATION = 1
SELECTED_Y_PRODUCT = 3.0 * math.pi
SELECTED_Z4_PHASE = 0.5 * math.pi

# Gate thresholds.
MIN_MESSENGER_OVER_EFT = 2.0
MAX_THETA_EARTH = 0.5
MIN_LEAKAGE_MARGIN = 10.0
MAX_PAIR_RESPONSE_NONLINEARITY = 1.0e-3
MAX_ENDPOINT_YUKAWA_SQ_OVER_4PI = 1.0
MAX_MATRIX_SPECTRAL_RELERR = 2.0e-11
MAX_CW_RECONSTRUCTION_RELERR = 2.0e-8
MAX_LOCAL_LINEAR_RATIO_AT_ZERO = 2.0e-11
MAX_LOCAL_TRACE_REL_SHIFT = 2.0e-13
MAX_MATCH_RELERR = 2.0e-10
MIN_BASIN_PASSERS = 40

# High precision is needed because the Wilson-line CW curvature is exponentially
# small in N and is obtained after cancellations among much larger local terms.
mp.mp.dps = 70


@dataclass(frozen=True)
class MicroscopicPoint:
    """One solved microscopic Wilson-line witness point."""

    N: int
    rho: float
    separation: int
    y_product: float
    kappa_cw: float
    d_cross_zero: float
    mu: float
    f: float
    theta_earth: float
    d_cross_earth: float
    d_self_earth: float
    leakage_proxy: float
    leakage_margin: float
    pair_response_nonlinearity: float
    messenger_min_mass: float
    messenger_over_eft: float
    y_endpoint: float
    yukawa_sq_over_4pi: float
    c_match_relerr: float
    m_match_relerr: float


# ---------------------------------------------------------------------------
# Exact deconstructed messenger matrix and derivatives.
# ---------------------------------------------------------------------------


def lattice_matrix(N: int, rho: float, theta: float) -> np.ndarray:
    """Return the exact dimensionless periodic messenger mass-squared matrix."""

    matrix = np.zeros((N, N), dtype=complex)
    np.fill_diagonal(matrix, rho * rho + 2.0)

    link = np.exp(1j * theta / N)

    for j in range(N):
        k = (j + 1) % N
        matrix[j, k] += -link
        matrix[k, j] += -np.conj(link)

    return matrix


def lattice_matrix_prime(N: int, rho: float, theta: float) -> np.ndarray:
    """Return dL/dtheta analytically."""

    del rho

    prime = np.zeros((N, N), dtype=complex)
    link = np.exp(1j * theta / N)

    for j in range(N):
        k = (j + 1) % N
        prime[j, k] += -(1j / N) * link
        prime[k, j] += +(1j / N) * np.conj(link)

    return prime


def inverse_and_prime(
    N: int,
    rho: float,
    theta: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Return G=L^-1 and G'=-G L' G."""

    matrix = lattice_matrix(N, rho, theta)
    inverse = np.linalg.inv(matrix)
    prime = lattice_matrix_prime(N, rho, theta)
    inverse_prime = -inverse @ prime @ inverse
    return inverse, inverse_prime


def spectral_inverse_element(
    N: int,
    rho: float,
    theta: float,
    separation: int,
) -> complex:
    """Independently reconstruct G_0d from the exact Fourier spectrum."""

    total = 0.0j

    for n in range(N):
        k = 2.0 * math.pi * n / N
        lam = rho * rho + 2.0 - 2.0 * math.cos(k + theta / N)
        total += np.exp(-1j * k * separation) / lam

    return total / N


def spectral_inverse_prime_element(
    N: int,
    rho: float,
    theta: float,
    separation: int,
) -> complex:
    """Independently reconstruct dG_0d/dtheta from the Fourier spectrum."""

    total = 0.0j

    for n in range(N):
        k = 2.0 * math.pi * n / N
        angle = k + theta / N
        lam = rho * rho + 2.0 - 2.0 * math.cos(angle)
        lam_prime = (2.0 / N) * math.sin(angle)
        total += (
            -np.exp(-1j * k * separation)
            * lam_prime
            / (lam * lam)
        )

    return total / N


def cross_derivative(
    N: int,
    rho: float,
    theta: float,
    separation: int,
) -> float:
    """Return d Re[i G_0d]/dtheta from the matrix identity."""

    _, inverse_prime = inverse_and_prime(N, rho, theta)
    return float(np.real(1j * inverse_prime[0, separation]))


def self_derivative(N: int, rho: float, theta: float) -> float:
    """Return d Re[G_00]/dtheta."""

    _, inverse_prime = inverse_and_prime(N, rho, theta)
    return float(np.real(inverse_prime[0, 0]))


# ---------------------------------------------------------------------------
# High-precision one-loop Wilson-line curvature.
# ---------------------------------------------------------------------------


def cw_spectral_sum_mp(N: int, rho: float, theta: mp.mpf) -> mp.mpf:
    """Return the dimensionless theta-dependent Coleman-Weinberg spectral sum."""

    rho_mp = mp.mpf(str(rho))
    total = mp.mpf("0")

    for n in range(N):
        angle = (2 * mp.pi * n + theta) / N
        lam = rho_mp * rho_mp + 2 - 2 * mp.cos(angle)
        total += lam * lam * (mp.log(lam) - mp.mpf("1.5"))

    return total


def cw_curvature_analytic_mp(N: int, rho: float) -> mp.mpf:
    """Return d^2 S_CW/dtheta^2 at theta=0 analytically at high precision."""

    rho_mp = mp.mpf(str(rho))
    total = mp.mpf("0")

    for n in range(N):
        angle = 2 * mp.pi * n / N
        lam = rho_mp * rho_mp + 2 - 2 * mp.cos(angle)
        lam_prime = (mp.mpf(2) / N) * mp.sin(angle)
        lam_second = (mp.mpf(2) / (N * N)) * mp.cos(angle)

        # For f(lam)=lam^2(log lam - 3/2):
        # f' = 2 lam (log lam - 1), f'' = 2 log lam.
        total += (
            2 * mp.log(lam) * lam_prime * lam_prime
            + 2 * lam * (mp.log(lam) - 1) * lam_second
        )

    return total


def cw_curvature_independent_mp(N: int, rho: float) -> mp.mpf:
    """Independently evaluate the same curvature by arbitrary-precision differentiation."""

    return mp.diff(
        lambda theta: cw_spectral_sum_mp(N, rho, theta),
        mp.mpf("0"),
        2,
    )


# ---------------------------------------------------------------------------
# Simultaneous operating-point matching.
# ---------------------------------------------------------------------------


def solve_operating_point(
    N: int,
    rho: float,
    separation: int,
    y_product: float,
) -> MicroscopicPoint | None:
    """Solve mu and f so C_phi is matched at Earth and m_phi is matched at theta=0."""

    kappa_mp = cw_curvature_analytic_mp(N, rho)

    if kappa_mp <= 0:
        return None

    kappa = float(kappa_mp)
    sqrt_kappa = math.sqrt(kappa)

    def f_from_mu(mu: float) -> float:
        # m_phi = mu^2 sqrt(kappa)/(8 pi f)
        return mu * mu * sqrt_kappa / (8.0 * math.pi * TARGET_M_PHI)

    def log_match(log_mu: float) -> float:
        mu = math.exp(log_mu)
        f = f_from_mu(mu)
        theta_earth = EARTH_PHI / f
        d_cross = abs(cross_derivative(N, rho, theta_earth, separation))

        if d_cross <= 0.0:
            return -1.0e100

        c_value = y_product * d_cross / (mu * mu * f)
        return math.log(c_value / TARGET_C_PHI)

    # Search a very broad microscopic scale interval.  Multiple roots are not
    # expected for the selected controlled-theta branch, but we detect them.
    grid = np.linspace(math.log(50.0), math.log(1.0e7), 180)
    values = [log_match(float(x)) for x in grid]
    roots: list[float] = []

    for left, right, f_left, f_right in zip(
        grid[:-1],
        grid[1:],
        values[:-1],
        values[1:],
    ):
        if not (math.isfinite(f_left) and math.isfinite(f_right)):
            continue

        if f_left == 0.0:
            roots.append(math.exp(float(left)))
        elif f_left * f_right < 0.0:
            root = brentq(log_match, float(left), float(right), xtol=1.0e-13)
            roots.append(math.exp(root))

    # Keep the root with the smallest controlled Wilson excursion.
    if not roots:
        return None

    candidates = []

    for mu in roots:
        f = f_from_mu(mu)
        theta_earth = EARTH_PHI / f
        d_cross_zero = abs(cross_derivative(N, rho, 0.0, separation))
        d_cross_earth = abs(cross_derivative(N, rho, theta_earth, separation))
        d_self_earth = abs(self_derivative(N, rho, theta_earth))

        c_reconstructed = y_product * d_cross_earth / (mu * mu * f)
        m_reconstructed = mu * mu * sqrt_kappa / (8.0 * math.pi * f)

        leakage_proxy = d_self_earth / max(d_cross_earth, 1.0e-300)
        leakage_margin = MAX_LEAKAGE_FRACTION / max(leakage_proxy, 1.0e-300)

        pair_response_nonlinearity = abs(
            d_cross_earth / max(d_cross_zero, 1.0e-300) - 1.0
        )

        messenger_min_mass = mu * rho
        messenger_over_eft = messenger_min_mass / MATERIAL_EFT_CUTOFF
        y_endpoint = math.sqrt(y_product)
        yukawa_sq_over_4pi = y_endpoint * y_endpoint / (4.0 * math.pi)

        candidates.append(
            MicroscopicPoint(
                N=N,
                rho=rho,
                separation=separation,
                y_product=y_product,
                kappa_cw=kappa,
                d_cross_zero=d_cross_zero,
                mu=mu,
                f=f,
                theta_earth=theta_earth,
                d_cross_earth=d_cross_earth,
                d_self_earth=d_self_earth,
                leakage_proxy=leakage_proxy,
                leakage_margin=leakage_margin,
                pair_response_nonlinearity=pair_response_nonlinearity,
                messenger_min_mass=messenger_min_mass,
                messenger_over_eft=messenger_over_eft,
                y_endpoint=y_endpoint,
                yukawa_sq_over_4pi=yukawa_sq_over_4pi,
                c_match_relerr=abs(c_reconstructed / TARGET_C_PHI - 1.0),
                m_match_relerr=abs(m_reconstructed / TARGET_M_PHI - 1.0),
            )
        )

    return min(candidates, key=lambda point: abs(point.theta_earth))


def point_passes(point: MicroscopicPoint) -> bool:
    """Apply the declared 019A microscopic witness gates."""

    return bool(
        point.messenger_over_eft >= MIN_MESSENGER_OVER_EFT
        and abs(point.theta_earth) <= MAX_THETA_EARTH
        and point.leakage_margin >= MIN_LEAKAGE_MARGIN
        and point.pair_response_nonlinearity <= MAX_PAIR_RESPONSE_NONLINEARITY
        and point.yukawa_sq_over_4pi <= MAX_ENDPOINT_YUKAWA_SQ_OVER_4PI
        and point.c_match_relerr <= MAX_MATCH_RELERR
        and point.m_match_relerr <= MAX_MATCH_RELERR
    )


# ---------------------------------------------------------------------------
# Independent audits.
# ---------------------------------------------------------------------------


def relative_error(a: complex | float, b: complex | float) -> float:
    """Return a scale-safe relative error."""

    return float(abs(a - b) / max(abs(a), abs(b), 1.0e-300))


def finite_difference_first(
    function: Callable[[float], float],
    x: float,
    h: float,
) -> float:
    """Five-point first derivative used only as an independent audit."""

    return float(
        (
            function(x - 2.0 * h)
            - 8.0 * function(x - h)
            + 8.0 * function(x + h)
            - function(x + 2.0 * h)
        )
        / (12.0 * h)
    )


def print_point(prefix: str, point: MicroscopicPoint) -> None:
    """Print one solved microscopic point in stable machine-readable form."""

    print(f"{prefix}_N={point.N}")
    print(f"{prefix}_RHO={point.rho:.15e}")
    print(f"{prefix}_SEPARATION={point.separation}")
    print(f"{prefix}_Y_PRODUCT={point.y_product:.15e}")
    print(f"{prefix}_Y_ENDPOINT={point.y_endpoint:.15e}")
    print(f"{prefix}_YUKAWA_SQ_OVER_4PI={point.yukawa_sq_over_4pi:.15e}")
    print(f"{prefix}_KAPPA_CW={point.kappa_cw:.15e}")
    print(f"{prefix}_MU_EV={point.mu:.15e}")
    print(f"{prefix}_F_EV={point.f:.15e}")
    print(f"{prefix}_F_GEV={point.f / 1.0e9:.15e}")
    print(f"{prefix}_THETA_EARTH={point.theta_earth:.15e}")
    print(f"{prefix}_MESSENGER_MIN_MASS_EV={point.messenger_min_mass:.15e}")
    print(f"{prefix}_MESSENGER_OVER_MATERIAL_EFT={point.messenger_over_eft:.15e}")
    print(f"{prefix}_D_CROSS_ZERO={point.d_cross_zero:.15e}")
    print(f"{prefix}_D_CROSS_EARTH={point.d_cross_earth:.15e}")
    print(f"{prefix}_D_SELF_EARTH={point.d_self_earth:.15e}")
    print(f"{prefix}_LOCAL_RESPONSE_LEAKAGE_PROXY={point.leakage_proxy:.15e}")
    print(f"{prefix}_LEAKAGE_MARGIN={point.leakage_margin:.15e}")
    print(f"{prefix}_PAIR_RESPONSE_NONLINEARITY={point.pair_response_nonlinearity:.15e}")
    print(f"{prefix}_C_PHI_MATCH_RELERR={point.c_match_relerr:.15e}")
    print(f"{prefix}_M_PHI_MATCH_RELERR={point.m_match_relerr:.15e}")


# ---------------------------------------------------------------------------
# Main gate.
# ---------------------------------------------------------------------------


def main() -> None:
    """Execute the complete 019A Wilson-line UV-protection witness gate."""

    print("=== 019A — WILSON-LINE SEQUESTERED PAIR-SCALAR UV PROTECTION GATE ===")

    print("\n=== INHERITED LOW-ENERGY TARGET ===")
    print(f"TARGET_C_PHI_EV_MINUS3={TARGET_C_PHI:.15e}")
    print(f"TARGET_M_PHI_EV={TARGET_M_PHI:.15e}")
    print(f"TARGET_RANGE_M=5.000000000000000e+03")
    print(f"EARTH_PHI_EV={EARTH_PHI:.15e}")
    print(f"MAXIMUM_PORTAL_LEAKAGE_FRACTION={MAX_LEAKAGE_FRACTION:.15e}")
    print(f"MATERIAL_EFT_CUTOFF_EV={MATERIAL_EFT_CUTOFF:.15e}")

    # ------------------------------------------------------------------
    # Exact propagator and symmetry audit for the selected witness.
    # ------------------------------------------------------------------

    print("\n=== EXACT MATRIX / SPECTRAL PROPAGATOR AUDIT ===")

    theta_checks = (0.0, 0.173, -0.287, 0.411)
    max_g_relerr = 0.0
    max_gp_relerr = 0.0

    for theta in theta_checks:
        inverse, inverse_prime = inverse_and_prime(
            SELECTED_N,
            SELECTED_RHO,
            theta,
        )
        matrix_value = inverse[0, SELECTED_SEPARATION]
        spectral_value = spectral_inverse_element(
            SELECTED_N,
            SELECTED_RHO,
            theta,
            SELECTED_SEPARATION,
        )
        matrix_prime = inverse_prime[0, SELECTED_SEPARATION]
        spectral_prime = spectral_inverse_prime_element(
            SELECTED_N,
            SELECTED_RHO,
            theta,
            SELECTED_SEPARATION,
        )

        g_relerr = relative_error(matrix_value, spectral_value)
        gp_relerr = relative_error(matrix_prime, spectral_prime)
        max_g_relerr = max(max_g_relerr, g_relerr)
        max_gp_relerr = max(max_gp_relerr, gp_relerr)

        print(
            f"PROPAGATOR_THETA={theta:+.6f} "
            f"G_RELERR={g_relerr:.3e} "
            f"GP_RELERR={gp_relerr:.3e}"
        )

    propagator_pass = (
        max_g_relerr <= MAX_MATRIX_SPECTRAL_RELERR
        and max_gp_relerr <= MAX_MATRIX_SPECTRAL_RELERR
    )

    print(f"MAX_G_MATRIX_SPECTRAL_RELERR={max_g_relerr:.15e}")
    print(f"MAX_GP_MATRIX_SPECTRAL_RELERR={max_gp_relerr:.15e}")
    print(f"EXACT_PROPAGATOR_RECONSTRUCTION={'PASS' if propagator_pass else 'FAIL'}")

    print("\n=== WILSON SYMMETRY / LOCAL UV PROTECTION ===")

    d_cross_zero = abs(
        cross_derivative(
            SELECTED_N,
            SELECTED_RHO,
            0.0,
            SELECTED_SEPARATION,
        )
    )
    d_self_zero = abs(self_derivative(SELECTED_N, SELECTED_RHO, 0.0))
    local_linear_ratio = d_self_zero / max(d_cross_zero, 1.0e-300)

    # Independent finite-difference confirmation of the local evenness.
    def g00_real(theta: float) -> float:
        inverse = np.linalg.inv(lattice_matrix(SELECTED_N, SELECTED_RHO, theta))
        return float(np.real(inverse[0, 0]))

    d_self_fd = abs(finite_difference_first(g00_real, 0.0, 1.0e-4))
    d_self_fd_ratio = d_self_fd / max(d_cross_zero, 1.0e-300)

    local_linear_pass = (
        local_linear_ratio <= MAX_LOCAL_LINEAR_RATIO_AT_ZERO
        and d_self_fd_ratio <= 5.0e-8
        and d_cross_zero > 0.0
    )

    print(f"TREE_CROSS_LINEAR_RESPONSE={d_cross_zero:.15e}")
    print(f"TREE_LOCAL_LINEAR_RESPONSE_ANALYTIC={d_self_zero:.15e}")
    print(f"TREE_LOCAL_LINEAR_RESPONSE_FD={d_self_fd:.15e}")
    print(f"LOCAL_TO_CROSS_LINEAR_RATIO_AT_ZERO={local_linear_ratio:.15e}")
    print(f"Z4_RELATIVE_ENDPOINT_PHASE={SELECTED_Z4_PHASE / math.pi:.6f}_PI")
    print("PROTECTION_MECHANISM=LOCAL_WILSON_EVENNESS_PLUS_DISCRETE_Z4_CROSS_PHASE")
    print(f"TREE_ONE_BODY_LINEAR_WILSON_RESPONSE={'FORBIDDEN_AT_SYMMETRY_POINT' if local_linear_pass else 'NOT_PROTECTED'}")

    # Verify that the one-loop divergent local invariants are theta independent.
    reference_L = lattice_matrix(SELECTED_N, SELECTED_RHO, 0.0)
    reference_tr1 = np.trace(reference_L)
    reference_tr2 = np.trace(reference_L @ reference_L)
    trace_shift = 0.0

    for theta in (0.37, 1.1, -2.2):
        matrix = lattice_matrix(SELECTED_N, SELECTED_RHO, theta)
        tr1 = np.trace(matrix)
        tr2 = np.trace(matrix @ matrix)
        trace_shift = max(
            trace_shift,
            relative_error(tr1, reference_tr1),
            relative_error(tr2, reference_tr2),
        )

    local_uv_pass = trace_shift <= MAX_LOCAL_TRACE_REL_SHIFT

    print(f"MAX_LOCAL_TRACE_INVARIANT_REL_SHIFT={trace_shift:.15e}")
    print(f"THETA_DEPENDENT_ONE_LOOP_LOCAL_DIVERGENCE={'ABSENT_IN_THIS_MESSENGER_SECTOR' if local_uv_pass else 'DETECTED'}")

    # ------------------------------------------------------------------
    # Coleman-Weinberg naturalness audit.
    # ------------------------------------------------------------------

    print("\n=== COLEMAN-WEINBERG NATURALNESS RECONSTRUCTION ===")

    kappa_analytic_mp = cw_curvature_analytic_mp(SELECTED_N, SELECTED_RHO)
    kappa_independent_mp = cw_curvature_independent_mp(SELECTED_N, SELECTED_RHO)
    kappa_analytic = float(kappa_analytic_mp)
    kappa_independent = float(kappa_independent_mp)
    cw_relerr = relative_error(kappa_analytic, kappa_independent)
    cw_pass = kappa_analytic > 0.0 and cw_relerr <= MAX_CW_RECONSTRUCTION_RELERR

    print(f"CW_KAPPA_ANALYTIC={kappa_analytic:.15e}")
    print(f"CW_KAPPA_INDEPENDENT={kappa_independent:.15e}")
    print(f"CW_KAPPA_RECONSTRUCTION_RELERR={cw_relerr:.15e}")
    print(f"WILSON_LINE_ONE_LOOP_MASS_CURVATURE={'POSITIVE' if kappa_analytic > 0.0 else 'NONPOSITIVE'}")
    print(f"ULTRALIGHT_WILSON_NATURALNESS_PREFLIGHT={'PASS' if cw_pass and local_uv_pass else 'FAIL'}")

    # ------------------------------------------------------------------
    # Selected operating point.
    # ------------------------------------------------------------------

    print("\n=== SELECTED OPERATING-POINT SOLUTION ===")

    selected = solve_operating_point(
        SELECTED_N,
        SELECTED_RHO,
        SELECTED_SEPARATION,
        SELECTED_Y_PRODUCT,
    )

    if selected is None:
        raise RuntimeError("Selected Wilson-line operating point has no simultaneous C_phi/m_phi solution")

    print_point("SELECTED", selected)

    selected_pass = point_passes(selected)

    print(f"PAIR_NR_MATCH_AT_EARTH={'PASS' if selected.c_match_relerr <= MAX_MATCH_RELERR else 'FAIL'}")
    print(f"ULTRALIGHT_MASS_MATCH={'PASS' if selected.m_match_relerr <= MAX_MATCH_RELERR else 'FAIL'}")
    print(f"MESSENGER_ABOVE_MATERIAL_EFT={'PASS' if selected.messenger_over_eft >= MIN_MESSENGER_OVER_EFT else 'FAIL'}")
    print(f"PERTURBATIVE_ENDPOINT_YUKAWAS={'PASS' if selected.yukawa_sq_over_4pi <= MAX_ENDPOINT_YUKAWA_SQ_OVER_4PI else 'FAIL'}")
    print(f"EARTH_WILSON_EXCURSION={'CONTROLLED' if abs(selected.theta_earth) <= MAX_THETA_EARTH else 'TOO_LARGE'}")
    print(f"EARTH_LOCAL_RESPONSE_PROXY={'PASS' if selected.leakage_margin >= MIN_LEAKAGE_MARGIN else 'FAIL'}")
    print(f"EARTH_PAIR_RESPONSE_LINEARITY={'PASS' if selected.pair_response_nonlinearity <= MAX_PAIR_RESPONSE_NONLINEARITY else 'FAIL'}")

    # ------------------------------------------------------------------
    # Broad discrete microscopic-basin scan.
    # ------------------------------------------------------------------

    print("\n=== MICROSCOPIC PARAMETER-BASIN SCAN ===")

    N_values = range(7, 17)
    rho_values = (1.50, 1.75, 2.00, 2.25, 2.50, 2.75, 3.00)
    y_products = (math.pi, 2.0 * math.pi, 3.0 * math.pi, 4.0 * math.pi)

    total_points = 0
    solved_points = 0
    passing_points: list[MicroscopicPoint] = []

    for N in N_values:
        max_sep = min(3, N // 2)

        for rho in rho_values:
            for separation in range(1, max_sep + 1):
                for y_product in y_products:
                    total_points += 1
                    point = solve_operating_point(N, rho, separation, y_product)

                    if point is None:
                        continue

                    solved_points += 1

                    if point_passes(point):
                        passing_points.append(point)

    basin_pass = len(passing_points) >= MIN_BASIN_PASSERS

    print(f"MICROSCOPIC_SCAN_TOTAL={total_points}")
    print(f"MICROSCOPIC_SCAN_SOLVED={solved_points}")
    print(f"MICROSCOPIC_SCAN_PASS={len(passing_points)}")
    print(f"MICROSCOPIC_SCAN_PASS_FRACTION={len(passing_points) / max(total_points, 1):.15e}")

    if passing_points:
        best_leakage = max(passing_points, key=lambda point: point.leakage_margin)
        lowest_coupling = min(passing_points, key=lambda point: point.yukawa_sq_over_4pi)
        largest_scale_margin = max(passing_points, key=lambda point: point.messenger_over_eft)
        print_point("BEST_LEAKAGE_MARGIN", best_leakage)
        print_point("LOWEST_COUPLING_PASSER", lowest_coupling)
        print_point("LARGEST_EFT_MARGIN_PASSER", largest_scale_margin)

    print(f"PERTURBATIVE_PARAMETER_BASIN={'PASS' if basin_pass else 'FAIL'}")

    # ------------------------------------------------------------------
    # Selected-point local robustness without reoptimizing toward wildcards.
    # ------------------------------------------------------------------

    print("\n=== SELECTED LOCAL ROBUSTNESS ===")

    local_pass = 0
    local_total = 0

    for rho_factor in (0.90, 1.00, 1.10):
        for y_factor in (0.75, 1.00, 1.25):
            local_total += 1
            point = solve_operating_point(
                SELECTED_N,
                SELECTED_RHO * rho_factor,
                SELECTED_SEPARATION,
                SELECTED_Y_PRODUCT * y_factor,
            )
            passed = point is not None and point_passes(point)
            local_pass += int(passed)
            print(
                f"LOCAL_ROBUST_RHO_FACTOR={rho_factor:.3f} "
                f"Y_FACTOR={y_factor:.3f} "
                f"PASS={'YES' if passed else 'NO'}"
            )

    local_robust_pass = local_pass >= 7
    print(f"SELECTED_LOCAL_ROBUSTNESS_PASS={local_pass}/{local_total}")
    print(f"SELECTED_LOCAL_ROBUSTNESS={'PASS' if local_robust_pass else 'FAIL'}")

    # Blind wildcard check required by project workflow.  These values are not
    # evidence and are not used to choose or optimize the selected point.
    print("\n=== BLIND WILDCARD RHO DIAGNOSTIC — NOT EVIDENCE ===")

    for factor in (0.625, 1.6, 1.875, 3.125, 5.0):
        rho = SELECTED_RHO * factor
        point = solve_operating_point(
            SELECTED_N,
            rho,
            SELECTED_SEPARATION,
            SELECTED_Y_PRODUCT,
        )
        passed = point is not None and point_passes(point)
        print(
            f"WILDCARD_RHO_FACTOR={factor:.6f} "
            f"RHO={rho:.9e} "
            f"PASS={'YES' if passed else 'NO'}"
        )

    print("WILDCARD_VALUES_USED_AS_EVIDENCE=NO")

    # ------------------------------------------------------------------
    # Decision.
    # ------------------------------------------------------------------

    print("\n=== 019A DECISION ===")

    overall = bool(
        propagator_pass
        and local_linear_pass
        and local_uv_pass
        and cw_pass
        and selected_pass
        and basin_pass
        and local_robust_pass
    )

    if overall:
        print("019A_WILSON_LINE_SEQUESTERED_PAIR_SCALAR_UV_PROTECTION_GATE=GREEN")
        print("RELATIVISTIC_THEORY_SPACE_OPERATOR_WITNESS=SUPPORTED")
        print("NONLOCAL_WILSON_PROTECTION=PASS")
        print("PAIR_NR_MATCH=PASS")
        print("TREE_LINEAR_LOCAL_RESPONSE=SYMMETRY_FORBIDDEN_AT_THETA_ZERO")
        print("EARTH_BACKGROUND_LOCAL_RESPONSE_PROXY=PASS")
        print("ULTRALIGHT_MASS_NATURALNESS=PASS_WITHIN_DECONSTRUCTED_MESSENGER_SECTOR")
        print("PERTURBATIVE_PARAMETER_BASIN=YES")
        print("INDEPENDENT_RECONSTRUCTION=PASS")
        print("PROTECTED_SCALAR_BRANCH=RETAIN_AND_ESCALATE")
        print("NEXT=019B_ANOMALY_FREE_SM_MATERIAL_ENDPOINT_AND_ONE_BODY_OPERATOR_MIXING_GATE")
        print("NEXT_AFTER_019B_GREEN=019C_EXACT_5KM_EXPERIMENTAL_BOUND_THEN_STELLAR_COSMOLOGY")
    else:
        print("019A_WILSON_LINE_SEQUESTERED_PAIR_SCALAR_UV_PROTECTION_GATE=RED")
        print("PROTECTED_SCALAR_BRANCH=DO_NOT_PROMOTE_FROM_THIS_WITNESS")
        print("NEXT=CLASSIFY_019A_FAILURE_AND_GLOBAL_RERANK_IF_FUNDAMENTAL")

    # Explicit claim boundaries regardless of GREEN/RED.
    print("STANDARD_MODEL_MATERIAL_ENDPOINT_EMBEDDING=NOT_ESTABLISHED")
    print("COMPLETE_ONE_BODY_OPERATOR_MIXING=NOT_YET_019B")
    print("EXACT_2026_5KM_FIFTH_FORCE_BOUND=NOT_YET_019C")
    print("STELLAR_COSMOLOGICAL_COMPLETION=NOT_ESTABLISHED")
    print("REAL_ANTIGRAVITY_MATERIAL=NO")
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
    print("NEW_PHYSICS_DISCOVERY=NO")
    print("018B_FIELD_EXISTENCE_RESULT=RETAINED")
    print("018C_M2_STABILITY_FALSIFICATION=RETAINED")
    print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_68_PERCENT_NOT_A_PROBABILITY")
    print("HEURISTIC_INCREASE_FROM_019A=NO_UNLESS_019B_CLOSES_REAL_MATERIAL_ONE_BODY_MIXING")
    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_019A_WILSON_LINE_SEQUESTERED_PAIR_SCALAR_UV_PROTECTION_GATE"
    )


if __name__ == "__main__":
    main()
