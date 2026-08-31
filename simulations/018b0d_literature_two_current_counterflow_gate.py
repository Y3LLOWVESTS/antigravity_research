#!/usr/bin/env python3
"""Simulation 018B-0D — literature-backed two-current counterflow gate.

PURPOSE
-------
Test the highest-priority microscopic repair of the validated 018A-8
counterrotating rim: a genuine two-current superconducting cosmic string rather
than two naively duplicated copies of the 017P condensate on one shared core.

SCIENTIFIC QUESTION
-------------------
Does the published Lilley-Martin-Peter two-current string model admit a
localized two-condensate straight-string solution whose two currents can be
chosen to counterflow exactly, cancel the integrated longitudinal momentum
flux, satisfy closed-loop integer winding compatibility, and remain inside the
published transverse and longitudinal elastic-stability conditions?

LITERATURE MODEL
----------------
Primary source:

    M. Lilley, X. Martin, P. Peter,
    "Coupled currents in cosmic strings",
    Phys. Rev. D 79, 103514 (2009), arXiv:0903.4328.

The microscopic model contains one local U(1) Higgs vortex H and two global
U(1) complex current carriers Phi and Sigma.  In the paper's notation,

    V = 1/2 m_phi^2 |Phi|^2
        + 1/2 m_sigma^2 |Sigma|^2
        + 1/2 (|H|^2-eta^2)
          (f_phi |Phi|^2 + f_sigma |Sigma|^2)
        + 1/4 lambda_phi |Phi|^4
        + 1/4 lambda_sigma |Sigma|^4
        + g/2 |Phi|^2 |Sigma|^2.

The straight-string ansatz is

    H = h(r) exp(i theta),
    Phi = phi(r) exp[i(omega_phi t-k_phi z)],
    Sigma = sigma(r) exp[i(omega_sigma t-k_sigma z)].

The state parameters are

    w_i = k_i^2 - omega_i^2.

The paper's radial field equations (their Eqs. 11-14) are solved directly here.

PUBLISHED BENCHMARK PARAMETERS
------------------------------
Use the representative parameter set from Fig. 1 of arXiv:0903.4328:

    alpha_phi   = 0.018
    alpha_sigma = 0.014
    beta_phi    = 0.010
    beta_sigma  = 0.008
    gamma_phi   = 0.00055
    gamma_sigma = 0.00045
    q_tilde^2   = 0.1

and the paper's weak-coupling case

    g_tilde^2 = 0.05 gamma_phi gamma_sigma.

Set lambda=eta=1 as a harmless choice of the overall dimensionless units and
reconstruct the corresponding unscaled microscopic couplings exactly from the
paper's definitions.

The operating state uses the paper's representative timelike choices

    w_tilde_phi   = -gamma_phi/2
    w_tilde_sigma = -gamma_sigma/2.

These lie strictly inside the confinement ranges quoted in the paper.

COUNTERFLOW CONSTRUCTION
------------------------
For timelike currents write

    omega_i = sqrt(-w_i) cosh(eta_i),
    k_i     = sqrt(-w_i) sinh(eta_i).

The integrated off-diagonal worldsheet stress is proportional to

    C = 2 pi [
        k_phi omega_phi I_phi
        + k_sigma omega_sigma I_sigma
    ],

where

    I_phi   = integral phi^2 r dr,
    I_sigma = integral sigma^2 r dr.

Choose opposite rapidities so C=0 exactly.  Then solve for the member of this
counterflow family satisfying

    |k_phi/k_sigma| = 3/4.

This makes the straight solution exactly compatible with closed-loop integer
windings

    N_phi : N_sigma = +3 : -4

(up to an arbitrary common integer multiple) at one common loop radius.

STABILITY
---------
Transverse stability uses the paper's condition T>0, equivalently the x-limit
from their Eq. 108.

Longitudinal stability is evaluated from their full two-current quartic,
Eqs. 123-130.  The logarithmic derivatives

    L_ij = partial ln(K_i) / partial w_j

are reconstructed numerically from neighboring microscopic BVP solutions and
checked for finite-difference convergence.

VALIDATION
----------
The run requires:

1. published dimensionless parameters reconstruct exactly;
2. both condensates are nonzero and localized;
3. the BVP converges on increasing radial domains;
4. integrated quantities converge with domain size;
5. finite-difference L_ij matrices converge;
6. exact momentum-flux cancellation C=0;
7. exact 3:4 counter-winding compatibility;
8. positive tension and transverse-stability margin;
9. all four roots of the published longitudinal quartic are real;
10. the selected exact 3:-4 counterflow remains stable under all converged
    finite-difference EOS derivative matrices;
11. a deterministic local rapidity neighborhood of +/-25 percent around the
    selected exact counterflow remains stable under all those matrices;
12. a broad diagnostic scan maps, but does not require, remote stability
    regions and instability gaps.

PROMOTION CONDITION
-------------------
GREEN establishes only a literature-backed microscopic two-current RIM
candidate.  It does not yet replace the 018A-8 rim in the gravitational ledger.
The next gate must attach/revalidate the already-developed nonthermal KLS wall
and junction using this new rim EOS, then recompute finite-payload gravity
before launching the global toroidal 018B PDE.

FALSIFIER / STOP RULE
---------------------
If the published two-current BVP cannot retain both condensates, the selected
exact integer-compatible counterflow is outside the transverse or longitudinal
stability domain, its +/-25 percent local neighborhood is not robust under the
converged EOS derivative matrices, or numerical convergence fails, demote this
route and rerank toward spatially separated microscopic cores.

A remote instability elsewhere in rapidity space is NOT a falsifier.  The
published theory predicts a finite elastic domain, not stability at arbitrary
current strength.  Remote instability is mapped as a boundary diagnostic.

Do not tune new couplings after seeing the result.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_REPRODUCTION_AND_COUNTERFLOW_APPLICATION_OF_PUBLISHED_TWO_CURRENT_STRING

WHAT THIS FILE DOES NOT ESTABLISH
---------------------------------
- compatibility with the existing KLS wall/junction;
- finite-payload repulsive gravity for this new rim EOS;
- a global toroidal field solution;
- full vorton/drum composite stability;
- nonlinear Einstein-matter consistency;
- practical energy scaling;
- experimental accessibility;
- a practical antigravity device;
- new physics or novelty.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
from scipy.integrate import simpson, solve_bvp
from scipy.optimize import brentq


# ---------------------------------------------------------------------------
# Published dimensionless parameter set (Lilley-Martin-Peter 2009, Fig. 1).
# ---------------------------------------------------------------------------
ALPHA_PHI = 1.8e-2
ALPHA_SIGMA = 1.4e-2
BETA_PHI = 1.0e-2
BETA_SIGMA = 0.8e-2
GAMMA_PHI = 5.5e-4
GAMMA_SIGMA = 4.5e-4
Q_TILDE_SQ = 1.0e-1

# Weak-coupling benchmark from the paper.
G_TILDE_SQ = 0.05 * GAMMA_PHI * GAMMA_SIGMA

# Overall units.  Setting lambda=eta=1 simply fixes the dimensionless scale.
LAMBDA_H = 1.0
ETA_H = 1.0

# Reconstruct the original microscopic couplings from Eqs. 16-17.
M_PHI_SQ = GAMMA_PHI / ALPHA_PHI
M_SIGMA_SQ = GAMMA_SIGMA / ALPHA_SIGMA
LAMBDA_PHI = M_PHI_SQ / ALPHA_PHI
LAMBDA_SIGMA = M_SIGMA_SQ / ALPHA_SIGMA
F_PHI = BETA_PHI / ALPHA_PHI
F_SIGMA = BETA_SIGMA / ALPHA_SIGMA
Q_SQ = Q_TILDE_SQ
G_TILDE = math.sqrt(G_TILDE_SQ)
G_COUPLING = G_TILDE / (ALPHA_PHI * ALPHA_SIGMA)

# Representative timelike points used in the paper's EOS/stability figures.
W_TILDE_PHI = -0.5 * GAMMA_PHI
W_TILDE_SIGMA = -0.5 * GAMMA_SIGMA
W_PHI = W_TILDE_PHI / ALPHA_PHI
W_SIGMA = W_TILDE_SIGMA / ALPHA_SIGMA

EPS = 1.0e-3
DOMAINS = (40.0, 60.0, 80.0)
N_MESH = 700
BVP_TOL = 3.0e-5
DERIVATIVE_FRACTIONS = (0.005, 0.010, 0.020)


@dataclass
class IntegratedState:
    """Integrated straight-string observables used by the stability test."""

    A: float
    I_phi: float
    I_sigma: float
    K_phi: float
    K_sigma: float
    phi0: float
    sigma0: float
    max_rms_residual: float


def reconstruct_dimensionless_parameters() -> dict[str, float]:
    """Reconstruct the paper's dimensionless inputs from the unscaled ones."""

    alpha_phi = M_PHI_SQ / (LAMBDA_PHI * ETA_H**2)
    alpha_sigma = M_SIGMA_SQ / (LAMBDA_SIGMA * ETA_H**2)
    beta_phi = F_PHI * M_PHI_SQ / (
        LAMBDA_H * LAMBDA_PHI * ETA_H**2
    )
    beta_sigma = F_SIGMA * M_SIGMA_SQ / (
        LAMBDA_H * LAMBDA_SIGMA * ETA_H**2
    )
    gamma_phi = M_PHI_SQ**2 / (
        LAMBDA_H * LAMBDA_PHI * ETA_H**4
    )
    gamma_sigma = M_SIGMA_SQ**2 / (
        LAMBDA_H * LAMBDA_SIGMA * ETA_H**4
    )
    g_tilde = (
        G_COUPLING
        * M_PHI_SQ
        * M_SIGMA_SQ
        / (
            LAMBDA_H
            * LAMBDA_PHI
            * LAMBDA_SIGMA
            * ETA_H**4
        )
    )

    return {
        "alpha_phi": alpha_phi,
        "alpha_sigma": alpha_sigma,
        "beta_phi": beta_phi,
        "beta_sigma": beta_sigma,
        "gamma_phi": gamma_phi,
        "gamma_sigma": gamma_sigma,
        "q_tilde_sq": Q_SQ / LAMBDA_H,
        "g_tilde_sq": g_tilde**2,
    }


def initial_guess(r: np.ndarray) -> np.ndarray:
    """Return a smooth vortex plus two-condensate initial BVP guess."""

    y = np.zeros((8, r.size), dtype=float)

    y[0] = np.tanh(r)
    y[1] = 1.0 / np.cosh(r) ** 2

    y[2] = np.exp(-0.5 * r**2)
    y[3] = -r * np.exp(-0.5 * r**2)

    y[4] = 0.38 * np.exp(-r / 3.0)
    y[5] = -(0.38 / 3.0) * np.exp(-r / 3.0)

    y[6] = 0.33 * np.exp(-r / 3.0)
    y[7] = -(0.33 / 3.0) * np.exp(-r / 3.0)

    return y


def solve_state(
    w_phi: float,
    w_sigma: float,
    domain: float,
    seed=None,
    tol: float = BVP_TOL,
):
    """Solve the published four-field radial BVP.

    State ordering:

        h, h', Q, Q', phi, phi', sigma, sigma'.
    """

    r = np.linspace(EPS, domain, N_MESH)

    if seed is None:
        y0 = initial_guess(r)
    else:
        # Continuation from the nearest already-converged BVP is more reliable
        # than restarting all nonlinear solves from an arbitrary profile.
        clipped = np.minimum(r, seed.x[-1])
        y0 = seed.sol(clipped)

        beyond = r > seed.x[-1]
        if np.any(beyond):
            y0[0, beyond] = 1.0
            y0[1, beyond] = 0.0
            y0[2, beyond] = 0.0
            y0[3, beyond] = 0.0
            y0[4, beyond] = 0.0
            y0[5, beyond] = 0.0
            y0[6, beyond] = 0.0
            y0[7, beyond] = 0.0

    def ode(rr, y):
        h, hp, qfun, qp, phi, phip, sigma, sigmap = y

        hpp = (
            -hp / rr
            + (
                qfun**2 / rr**2
                + 0.5 * LAMBDA_H * (h**2 - ETA_H**2)
                + F_PHI * phi**2
                + F_SIGMA * sigma**2
            )
            * h
        )

        qpp = qp / rr + Q_SQ * h**2 * qfun

        phipp = (
            -phip / rr
            + (
                w_phi
                + F_PHI * (h**2 - ETA_H**2)
                + M_PHI_SQ
                + LAMBDA_PHI * phi**2
                + G_COUPLING * sigma**2
            )
            * phi
        )

        sigmapp = (
            -sigmap / rr
            + (
                w_sigma
                + F_SIGMA * (h**2 - ETA_H**2)
                + M_SIGMA_SQ
                + LAMBDA_SIGMA * sigma**2
                + G_COUPLING * phi**2
            )
            * sigma
        )

        return np.vstack(
            [
                hp,
                hpp,
                qp,
                qpp,
                phip,
                phipp,
                sigmap,
                sigmapp,
            ]
        )

    def bc(ya, yb):
        return np.array(
            [
                ya[0],
                ya[2] - 1.0,
                ya[5],
                ya[7],
                yb[0] - ETA_H,
                yb[2],
                yb[4],
                yb[6],
            ]
        )

    return solve_bvp(
        ode,
        bc,
        r,
        y0,
        tol=tol,
        max_nodes=30000,
    )


def integrate_state(sol, domain: float, n: int = 7000) -> IntegratedState:
    """Integrate A and the two condensate norms from the microscopic BVP."""

    r = np.linspace(EPS, domain, n)
    h, hp, qfun, qp, phi, phip, sigma, sigmap = sol.sol(r)

    potential = (
        0.125 * LAMBDA_H * (h**2 - ETA_H**2) ** 2
        + 0.5 * M_PHI_SQ * phi**2
        + 0.5 * M_SIGMA_SQ * sigma**2
        + 0.5
        * (h**2 - ETA_H**2)
        * (F_PHI * phi**2 + F_SIGMA * sigma**2)
        + 0.25 * LAMBDA_PHI * phi**4
        + 0.25 * LAMBDA_SIGMA * sigma**4
        + 0.5 * G_COUPLING * phi**2 * sigma**2
    )

    # Paper Eq. 40.
    a_density = (
        0.5
        * (
            hp**2
            + h**2 * qfun**2 / r**2
            + qp**2 / (Q_SQ * r**2)
            + phip**2
            + sigmap**2
        )
        + potential
    )

    A = 2.0 * math.pi * simpson(a_density * r, x=r)
    i_phi = simpson(phi**2 * r, x=r)
    i_sigma = simpson(sigma**2 * r, x=r)

    return IntegratedState(
        A=float(A),
        I_phi=float(i_phi),
        I_sigma=float(i_sigma),
        K_phi=float(-2.0 * math.pi * i_phi),
        K_sigma=float(-2.0 * math.pi * i_sigma),
        phi0=float(phi[0]),
        sigma0=float(sigma[0]),
        max_rms_residual=float(np.max(sol.rms_residuals)),
    )


def solve_and_integrate(
    w_phi: float,
    w_sigma: float,
    domain: float,
    seed=None,
    tol: float = BVP_TOL,
):
    """Convenience wrapper returning the BVP and integrated state."""

    sol = solve_state(
        w_phi,
        w_sigma,
        domain,
        seed=seed,
        tol=tol,
    )

    if not sol.success:
        raise RuntimeError(sol.message)

    return sol, integrate_state(sol, domain)


def derivative_matrix(nominal_sol, step_fraction: float) -> np.ndarray:
    """Return L_ij = partial ln(-K_i) / partial w_j by centered differences."""

    dw_phi = abs(W_PHI) * step_fraction
    dw_sigma = abs(W_SIGMA) * step_fraction

    states = {}

    for key, wp, ws in (
        ("p_phi", W_PHI + dw_phi, W_SIGMA),
        ("m_phi", W_PHI - dw_phi, W_SIGMA),
        ("p_sigma", W_PHI, W_SIGMA + dw_sigma),
        ("m_sigma", W_PHI, W_SIGMA - dw_sigma),
    ):
        _, integ = solve_and_integrate(
            wp,
            ws,
            60.0,
            seed=nominal_sol,
            tol=4.0e-5,
        )
        states[key] = integ

    l11 = (
        math.log(-states["p_phi"].K_phi)
        - math.log(-states["m_phi"].K_phi)
    ) / (2.0 * dw_phi)

    l21 = (
        math.log(-states["p_phi"].K_sigma)
        - math.log(-states["m_phi"].K_sigma)
    ) / (2.0 * dw_phi)

    l12 = (
        math.log(-states["p_sigma"].K_phi)
        - math.log(-states["m_sigma"].K_phi)
    ) / (2.0 * dw_sigma)

    l22 = (
        math.log(-states["p_sigma"].K_sigma)
        - math.log(-states["m_sigma"].K_sigma)
    ) / (2.0 * dw_sigma)

    return np.array(
        [
            [l11, l12],
            [l21, l22],
        ],
        dtype=float,
    )


def relative_matrix_change(a: np.ndarray, b: np.ndarray) -> float:
    """Maximum entrywise relative difference with a safe denominator."""

    return float(
        np.max(
            np.abs(a - b)
            / np.maximum(np.abs(a), 1.0e-30)
        )
    )


def counterflow_state(
    eta_phi: float,
    integ: IntegratedState,
    lmat: np.ndarray,
):
    """Construct exact C=0 timelike counterflow and evaluate stability."""

    s_phi = -W_PHI
    s_sigma = -W_SIGMA

    target = -(
        integ.I_phi * s_phi
        / (integ.I_sigma * s_sigma)
    ) * math.sinh(2.0 * eta_phi)

    eta_sigma = 0.5 * math.asinh(target)

    omega_phi = math.sqrt(s_phi) * math.cosh(eta_phi)
    k_phi = math.sqrt(s_phi) * math.sinh(eta_phi)

    omega_sigma = math.sqrt(s_sigma) * math.cosh(eta_sigma)
    k_sigma = math.sqrt(s_sigma) * math.sinh(eta_sigma)

    c_flux = 2.0 * math.pi * (
        k_phi * omega_phi * integ.I_phi
        + k_sigma * omega_sigma * integ.I_sigma
    )

    x = k_phi * k_sigma - omega_phi * omega_sigma

    B = math.pi * (
        (k_phi**2 + omega_phi**2) * integ.I_phi
        + (k_sigma**2 + omega_sigma**2) * integ.I_sigma
    )

    root_term = math.sqrt(max(0.0, B**2 - c_flux**2))
    U = integ.A + root_term
    T = integ.A - root_term

    radicand = (
        integ.A**2
        - (
            0.5 * W_PHI * integ.K_phi
            - 0.5 * W_SIGMA * integ.K_sigma
        )
        ** 2
    )

    x_lim = math.sqrt(
        radicand
        / (integ.K_phi * integ.K_sigma)
    )

    l11, l12 = lmat[0]
    l21, l22 = lmat[1]
    determinant_l = l11 * l22 - l12 * l21

    discriminant = x**2 - W_PHI * W_SIGMA

    if discriminant < -1.0e-13:
        raise RuntimeError(
            "Counterflow violates the two-current kinematic discriminant"
        )

    lambda_x = x + math.copysign(
        math.sqrt(max(0.0, discriminant)),
        x,
    )

    # Lilley-Martin-Peter Eqs. 124-130.
    c0 = determinant_l * lambda_x**2 * W_SIGMA**2

    c1 = -2.0 * lambda_x * (
        determinant_l * W_PHI * W_SIGMA**2
        + determinant_l * W_SIGMA * lambda_x**2
        + lambda_x**2 * l11
        + W_SIGMA**2 * l22
    )

    c2 = (
        determinant_l
        * (
            W_PHI**2 * W_SIGMA**2
            + 4.0 * lambda_x**2 * W_PHI * W_SIGMA
            + lambda_x**4
        )
        + 4.0
        * lambda_x**2
        * (1.0 + l11 * W_PHI + l22 * W_SIGMA)
    )

    c3 = -2.0 * lambda_x * (
        determinant_l * W_PHI**2 * W_SIGMA
        + determinant_l * W_PHI * lambda_x**2
        + W_PHI**2 * l11
        + lambda_x**2 * l22
    )

    c4 = determinant_l * lambda_x**2 * W_PHI**2

    roots = np.roots([c4, c3, c2, c1, c0])
    max_root_imag = float(np.max(np.abs(np.imag(roots))))

    return {
        "eta_phi": eta_phi,
        "eta_sigma": eta_sigma,
        "omega_phi": omega_phi,
        "k_phi": k_phi,
        "omega_sigma": omega_sigma,
        "k_sigma": k_sigma,
        "C": float(c_flux),
        "x": float(x),
        "B": float(B),
        "U": float(U),
        "T": float(T),
        "x_lim": float(x_lim),
        "roots": roots,
        "max_root_imag": max_root_imag,
    }


def main() -> None:
    """Run the literature BVP reproduction and exact counterflow gate."""

    print(
        "=== 018B-0D — LITERATURE-BACKED TWO-CURRENT COUNTERFLOW GATE ==="
    )

    print("\n=== LITERATURE PARAMETER RECONSTRUCTION ===")

    reconstructed = reconstruct_dimensionless_parameters()

    expected = {
        "alpha_phi": ALPHA_PHI,
        "alpha_sigma": ALPHA_SIGMA,
        "beta_phi": BETA_PHI,
        "beta_sigma": BETA_SIGMA,
        "gamma_phi": GAMMA_PHI,
        "gamma_sigma": GAMMA_SIGMA,
        "q_tilde_sq": Q_TILDE_SQ,
        "g_tilde_sq": G_TILDE_SQ,
    }

    max_parameter_relerr = 0.0

    for key in expected:
        relerr = abs(reconstructed[key] - expected[key]) / max(
            abs(expected[key]),
            1.0e-30,
        )
        max_parameter_relerr = max(max_parameter_relerr, relerr)
        print(
            f"{key.upper()}_RECONSTRUCTED={reconstructed[key]:.15e} "
            f"EXPECTED={expected[key]:.15e} "
            f"RELERR={relerr:.3e}"
        )

    parameter_pass = max_parameter_relerr < 1.0e-12

    print(
        "PUBLISHED_PARAMETER_RECONSTRUCTION="
        + ("PASS" if parameter_pass else "FAIL")
    )

    quartic_condition = (
        LAMBDA_PHI * LAMBDA_SIGMA
        > G_COUPLING**2
    )

    confinement_phi = (
        -M_PHI_SQ
        < W_PHI
        < F_PHI * ETA_H**2 - M_PHI_SQ
    )

    confinement_sigma = (
        -M_SIGMA_SQ
        < W_SIGMA
        < F_SIGMA * ETA_H**2 - M_SIGMA_SQ
    )

    print(f"LAMBDA_PHI={LAMBDA_PHI:.15e}")
    print(f"LAMBDA_SIGMA={LAMBDA_SIGMA:.15e}")
    print(f"G_COUPLING={G_COUPLING:.15e}")
    print(
        "PUBLISHED_WEAK_MODERATE_QUARTIC_CONDITION="
        + ("PASS" if quartic_condition else "FAIL")
    )
    print(
        "PHI_CURRENT_CONFINEMENT="
        + ("PASS" if confinement_phi else "FAIL")
    )
    print(
        "SIGMA_CURRENT_CONFINEMENT="
        + ("PASS" if confinement_sigma else "FAIL")
    )

    print("\n=== RADIAL BVP DOMAIN CONVERGENCE ===")

    domain_states = {}
    seed = None

    for domain in DOMAINS:
        sol, integ = solve_and_integrate(
            W_PHI,
            W_SIGMA,
            domain,
            seed=seed,
        )
        domain_states[domain] = (sol, integ)
        seed = sol

        print(
            f"DOMAIN={domain:.0f} "
            f"A={integ.A:.15e} "
            f"I_PHI={integ.I_phi:.15e} "
            f"I_SIGMA={integ.I_sigma:.15e} "
            f"PHI0={integ.phi0:.15e} "
            f"SIGMA0={integ.sigma0:.15e} "
            f"MAX_RMS_RESIDUAL={integ.max_rms_residual:.3e}"
        )

    integ60 = domain_states[60.0][1]
    integ80 = domain_states[80.0][1]

    domain_changes = {
        "A": abs(integ80.A - integ60.A) / abs(integ80.A),
        "I_phi": abs(integ80.I_phi - integ60.I_phi) / abs(integ80.I_phi),
        "I_sigma": abs(integ80.I_sigma - integ60.I_sigma) / abs(integ80.I_sigma),
    }

    max_domain_change = max(domain_changes.values())

    for key, value in domain_changes.items():
        print(f"DOMAIN_60_TO_80_{key.upper()}_REL_CHANGE={value:.15e}")

    domain_pass = max_domain_change < 5.0e-4

    both_condensates = (
        integ80.phi0 > 1.0e-3
        and integ80.sigma0 > 1.0e-3
    )

    residual_pass = max(
        domain_states[d][1].max_rms_residual
        for d in DOMAINS
    ) < 5.0e-5

    print(
        "TWO_CONDENSATES_LOCALIZED="
        + ("PASS" if both_condensates else "FAIL")
    )
    print(
        "BVP_DOMAIN_CONVERGENCE="
        + ("PASS" if domain_pass else "FAIL")
    )
    print(
        "BVP_RESIDUAL_GATE="
        + ("PASS" if residual_pass else "FAIL")
    )

    print("\n=== EOS DERIVATIVE / LONGITUDINAL-STABILITY PREFLIGHT ===")

    nominal_sol = domain_states[60.0][0]
    derivative_matrices = {}

    for step_fraction in DERIVATIVE_FRACTIONS:
        matrix = derivative_matrix(nominal_sol, step_fraction)
        derivative_matrices[step_fraction] = matrix

        print(
            f"DERIVATIVE_STEP_FRACTION={step_fraction:.6f} "
            f"L11={matrix[0,0]:+.15e} "
            f"L12={matrix[0,1]:+.15e} "
            f"L21={matrix[1,0]:+.15e} "
            f"L22={matrix[1,1]:+.15e}"
        )

    change_small_mid = relative_matrix_change(
        derivative_matrices[0.005],
        derivative_matrices[0.010],
    )
    change_mid_large = relative_matrix_change(
        derivative_matrices[0.010],
        derivative_matrices[0.020],
    )

    derivative_pass = max(
        change_small_mid,
        change_mid_large,
    ) < 5.0e-4

    print(
        "L_MATRIX_0P5_TO_1P0_PERCENT_MAX_REL_CHANGE="
        f"{change_small_mid:.15e}"
    )
    print(
        "L_MATRIX_1P0_TO_2P0_PERCENT_MAX_REL_CHANGE="
        f"{change_mid_large:.15e}"
    )
    print(
        "EOS_DERIVATIVE_CONVERGENCE="
        + ("PASS" if derivative_pass else "FAIL")
    )

    print("\n=== EXACT 3:-4 INTEGER-COMPATIBLE COUNTERFLOW ===")

    lmat = derivative_matrices[0.010]
    integ = integ60

    def winding_ratio_residual(eta_phi):
        state = counterflow_state(eta_phi, integ, lmat)
        return abs(state["k_phi"] / state["k_sigma"]) - 0.75

    eta_phi = brentq(
        winding_ratio_residual,
        0.10,
        0.80,
        xtol=1.0e-13,
        rtol=1.0e-13,
    )

    counter = counterflow_state(
        eta_phi,
        integ,
        lmat,
    )

    ratio = abs(counter["k_phi"] / counter["k_sigma"])
    flux_scale = max(
        2.0
        * math.pi
        * (
            abs(counter["k_phi"] * counter["omega_phi"] * integ.I_phi)
            + abs(counter["k_sigma"] * counter["omega_sigma"] * integ.I_sigma)
        ),
        1.0e-30,
    )
    flux_rel = abs(counter["C"]) / flux_scale

    loop_radius_3 = 3.0 / counter["k_phi"]
    loop_radius_4 = 4.0 / abs(counter["k_sigma"])
    loop_radius_relerr = abs(loop_radius_3 - loop_radius_4) / loop_radius_3

    transverse_margin = (
        counter["x_lim"] - abs(counter["x"])
    ) / counter["x_lim"]

    roots = counter["roots"]

    print(f"ETA_PHI={counter['eta_phi']:.15e}")
    print(f"ETA_SIGMA={counter['eta_sigma']:.15e}")
    print(f"OMEGA_PHI={counter['omega_phi']:.15e}")
    print(f"K_PHI={counter['k_phi']:+.15e}")
    print(f"OMEGA_SIGMA={counter['omega_sigma']:.15e}")
    print(f"K_SIGMA={counter['k_sigma']:+.15e}")
    print(f"ABS_K_RATIO={ratio:.15e}")
    print(f"COUNTERFLOW_C={counter['C']:+.15e}")
    print(f"COUNTERFLOW_C_RELATIVE={flux_rel:.15e}")
    print(f"X_STATE_PARAMETER={counter['x']:+.15e}")
    print(f"X_TRANSVERSE_LIMIT={counter['x_lim']:.15e}")
    print(f"TRANSVERSE_MARGIN_FRACTION={transverse_margin:.15e}")
    print(f"ENERGY_PER_LENGTH_U={counter['U']:.15e}")
    print(f"TENSION_T={counter['T']:.15e}")
    print(f"CT2=T_OVER_U={counter['T']/counter['U']:.15e}")
    print(f"LOOP_RADIUS_FROM_NPHI_3={loop_radius_3:.15e}")
    print(f"LOOP_RADIUS_FROM_NSIGMA_4={loop_radius_4:.15e}")
    print(f"LOOP_RADIUS_INTEGER_MATCH_RELERR={loop_radius_relerr:.15e}")
    print(
        "LONGITUDINAL_QUARTIC_ROOTS="
        + ",".join(
            f"{z.real:+.12e}{z.imag:+.3e}j"
            for z in roots
        )
    )
    print(
        "LONGITUDINAL_MAX_ROOT_IMAG="
        f"{counter['max_root_imag']:.15e}"
    )

    exact_counterflow_pass = (
        flux_rel < 1.0e-11
        and abs(ratio - 0.75) < 1.0e-11
        and loop_radius_relerr < 1.0e-11
    )

    transverse_pass = (
        counter["T"] > 0.0
        and abs(counter["x"]) < counter["x_lim"]
    )

    longitudinal_pass = counter["max_root_imag"] < 1.0e-8

    print(
        "EXACT_COUNTERFLOW_MOMENTUM_CANCELLATION="
        + ("PASS" if exact_counterflow_pass else "FAIL")
    )
    print(
        "INTEGER_WINDING_3_TO_MINUS4_COMPATIBILITY="
        + ("PASS" if loop_radius_relerr < 1.0e-11 else "FAIL")
    )
    print(
        "TRANSVERSE_TWO_CURRENT_STABILITY="
        + ("PASS" if transverse_pass else "FAIL")
    )
    print(
        "LONGITUDINAL_TWO_CURRENT_STABILITY="
        + ("PASS" if longitudinal_pass else "FAIL")
    )

    print("\n=== SELECTED-POINT NUMERICAL STABILITY ROBUSTNESS ===")

    selected_matrix_passes = []
    selected_max_imag = 0.0

    for step_fraction in DERIVATIVE_FRACTIONS:
        state = counterflow_state(
            eta_phi,
            integ,
            derivative_matrices[step_fraction],
        )
        margin = (
            state["x_lim"] - abs(state["x"])
        ) / state["x_lim"]
        passed = (
            state["T"] > 0.0
            and margin > 0.0
            and state["max_root_imag"] < 1.0e-8
        )
        selected_matrix_passes.append(passed)
        selected_max_imag = max(
            selected_max_imag,
            state["max_root_imag"],
        )
        print(
            f"SELECTED_DERIVATIVE_STEP={step_fraction:.6f} "
            f"TENSION={state['T']:+.15e} "
            f"TRANSVERSE_MARGIN={margin:+.15e} "
            f"MAX_LONGITUDINAL_ROOT_IMAG={state['max_root_imag']:.15e} "
            f"STABLE={'YES' if passed else 'NO'}"
        )

    selected_matrix_robust = all(selected_matrix_passes)

    print(
        "SELECTED_COUNTERFLOW_STABLE_ALL_DERIVATIVE_MATRICES="
        + ("PASS" if selected_matrix_robust else "FAIL")
    )

    print("\n=== LOCAL +/-25 PERCENT COUNTERFLOW ROBUSTNESS ===")

    local_eta_grid = np.linspace(
        0.75 * eta_phi,
        1.25 * eta_phi,
        101,
    )

    local_total = 0
    local_passed = 0
    local_min_tension = math.inf
    local_min_transverse_margin = math.inf
    local_max_root_imag = 0.0

    for eta in local_eta_grid:
        for step_fraction in DERIVATIVE_FRACTIONS:
            state = counterflow_state(
                float(eta),
                integ,
                derivative_matrices[step_fraction],
            )
            margin = (
                state["x_lim"] - abs(state["x"])
            ) / state["x_lim"]
            passed = (
                state["T"] > 0.0
                and margin > 0.0
                and state["max_root_imag"] < 1.0e-8
            )
            local_total += 1
            local_passed += int(passed)
            local_min_tension = min(
                local_min_tension,
                state["T"],
            )
            local_min_transverse_margin = min(
                local_min_transverse_margin,
                margin,
            )
            local_max_root_imag = max(
                local_max_root_imag,
                state["max_root_imag"],
            )

    local_basin_pass = local_passed == local_total

    print(
        f"LOCAL_COUNTERFLOW_ROBUSTNESS_PASS={local_passed}/{local_total}"
    )
    print(
        "LOCAL_COUNTERFLOW_MIN_TENSION="
        f"{local_min_tension:+.15e}"
    )
    print(
        "LOCAL_COUNTERFLOW_MIN_TRANSVERSE_MARGIN="
        f"{local_min_transverse_margin:+.15e}"
    )
    print(
        "LOCAL_COUNTERFLOW_MAX_LONGITUDINAL_ROOT_IMAG="
        f"{local_max_root_imag:.15e}"
    )
    print(
        "LOCAL_COUNTERFLOW_STABILITY_BASIN="
        + ("PASS" if local_basin_pass else "FAIL")
    )

    print("\n=== BROAD COUNTERFLOW ELASTIC-DOMAIN MAP ===")

    # This broad scan is diagnostic only.  A finite current-carrying string
    # is not expected to remain elastically stable at arbitrary current.
    # We map connected stable intervals and instability gaps so that the
    # selected 3:-4 point can be located relative to the nearest boundary.
    broad_eta_grid = np.linspace(0.001, 2.5, 2500)
    broad_stable = []
    broad_min_tension = math.inf
    broad_min_transverse_margin = math.inf
    broad_max_root_imag = 0.0

    for eta in broad_eta_grid:
        state = counterflow_state(float(eta), integ, lmat)
        margin = (
            state["x_lim"] - abs(state["x"])
        ) / state["x_lim"]
        passed = (
            state["T"] > 0.0
            and margin > 0.0
            and state["max_root_imag"] < 1.0e-8
        )
        broad_stable.append(passed)
        broad_min_tension = min(broad_min_tension, state["T"])
        broad_min_transverse_margin = min(
            broad_min_transverse_margin,
            margin,
        )
        broad_max_root_imag = max(
            broad_max_root_imag,
            state["max_root_imag"],
        )

    intervals = []
    start = None
    for index, (eta, passed) in enumerate(
        zip(broad_eta_grid, broad_stable)
    ):
        if passed and start is None:
            start = float(eta)
        if start is not None and (
            not passed or index == len(broad_eta_grid) - 1
        ):
            if passed:
                end = float(eta)
            else:
                end = float(broad_eta_grid[index - 1])
            intervals.append((start, end))
            start = None

    containing_interval = None
    for lo, hi in intervals:
        if lo <= eta_phi <= hi:
            containing_interval = (lo, hi)
            break

    if containing_interval is None:
        distance_to_boundary = 0.0
    else:
        distance_to_boundary = min(
            eta_phi - containing_interval[0],
            containing_interval[1] - eta_phi,
        )

    print(
        "BROAD_COUNTERFLOW_STABLE_INTERVALS="
        + ";".join(
            f"[{lo:.6f},{hi:.6f}]"
            for lo, hi in intervals
        )
    )
    print(
        "SELECTED_COUNTERFLOW_CONTAINING_INTERVAL="
        + (
            f"[{containing_interval[0]:.6f},{containing_interval[1]:.6f}]"
            if containing_interval is not None
            else "NONE"
        )
    )
    print(
        "SELECTED_COUNTERFLOW_DISTANCE_TO_NEAREST_MAPPED_BOUNDARY="
        f"{distance_to_boundary:.15e}"
    )
    print(
        "BROAD_COUNTERFLOW_MAX_LONGITUDINAL_ROOT_IMAG="
        f"{broad_max_root_imag:.15e}"
    )
    print(
        "REMOTE_INSTABILITY_IS_EXPECTED_FINITE_ELASTIC_DOMAIN_DIAGNOSTIC=YES"
    )

    print("\n=== DECISION ===")

    green = all(
        [
            parameter_pass,
            quartic_condition,
            confinement_phi,
            confinement_sigma,
            both_condensates,
            domain_pass,
            residual_pass,
            derivative_pass,
            exact_counterflow_pass,
            transverse_pass,
            longitudinal_pass,
            selected_matrix_robust,
            local_basin_pass,
        ]
    )

    if green:
        print("018B0D_TWO_CURRENT_COUNTERFLOW_GATE=GREEN")
        print("LITERATURE_BACKED_TWO_CURRENT_MICROSCOPIC_RIM_CANDIDATE=YES")
        print("EXACT_INTEGRATED_T_TZ_CANCELLATION=YES")
        print("CLOSED_LOOP_INTEGER_COUNTERWINDING_COMPATIBILITY=YES")
        print("PUBLISHED_TWO_CURRENT_ELASTIC_STABILITY=PASS_AT_SELECTED_STATE")
        print("VALIDATED_018A8_GRAVITY_LEDGER=UNCHANGED_PENDING_REVALIDATION")
        print(
            "NEXT=018B0E_KLS_WALL_JUNCTION_AND_FINITE_PAYLOAD_"
            "REVALIDATION_WITH_TWO_CURRENT_RIM_EOS"
        )
    else:
        print("018B0D_TWO_CURRENT_COUNTERFLOW_GATE=RED")
        print("LITERATURE_BACKED_TWO_CURRENT_MICROSCOPIC_RIM_CANDIDATE=NO")
        print(
            "NEXT=RERANK_SPATIALLY_SEPARATED_MICROSCOPIC_CORES_"
            "BEFORE_TRUE_018B"
        )

    print("CURRENT_HEURISTIC=APPROXIMATELY_66_PERCENT_NOT_A_PROBABILITY")
    print("HEURISTIC_INCREASE_FROM_THIS_GATE=NO_RIM_SELECTION_ONLY")
    print("TRUE_018B_GREEN_TARGET=APPROXIMATELY_68_PERCENT")
    print("018C_GREEN_TARGET=APPROXIMATELY_71_TO_72_PERCENT")
    print("018D_GREEN_TARGET=APPROXIMATELY_72_TO_74_PERCENT")
    print("018E_GREEN_TARGET=APPROXIMATELY_78_TO_80_PERCENT")
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
    print("NEW_PHYSICS_DISCOVERY=NO")
    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_REPRODUCTION_AND_COUNTERFLOW_APPLICATION_"
        "OF_PUBLISHED_TWO_CURRENT_STRING"
    )


if __name__ == "__main__":
    main()
