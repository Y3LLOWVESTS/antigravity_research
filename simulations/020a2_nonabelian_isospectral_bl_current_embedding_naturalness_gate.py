#!/usr/bin/env python3
"""020A2 — non-Abelian isospectral B/L current embedding and naturalness gate.

PURPOSE
-------
Test the highest-information continuation of 020A1.

020A1 established four facts:

1. canonical Abelian link masses are Wilson-phase blind;
2. conventional Wilson-dependent vector eigenvalue splitting fails the
   ultralight-mass naturalness gate;
3. an isospectral current-kernel rotation can match the target response;
4. a minimal SU(2) fundamental + adjoint sector realizes an exactly
   isospectral vector representation.

The remaining question is whether that SU(2) isospectral response can be
embedded into the anomaly-free baryon/lepton vector-current endpoint in a
minimal renormalizable way *without* requiring a radiatively unstable
B <-> L degeneracy.

SCIENTIFIC QUESTION
-------------------
Can a minimal renormalizable

    SU(2)_X x U(1)_B x U(1)_L

theory provide a physical, gauge-invariant, isospectral heavy-vector rotation
that:

- produces the required d[M^-2]_{BL}/dphi response;
- keeps all heavy vectors above the preferred 2 x material-EFT scale;
- preserves the ultralight 5-km mode against the first unavoidable
  B/L-exchange-breaking correction;
- does not rely on a tuned equality of unrelated baryon and lepton sectors?

MODEL
-----
Gauge fields:

    X_mu^a  for SU(2)_X
    B_mu    for U(1)_B
    L_mu    for U(1)_L

Scalar sectors:

    H_B : SU(2)_X fundamental, U(1)_B charge +1
    H_L : SU(2)_X fundamental, U(1)_L charge +1
    Phi : real SU(2)_X adjoint, neutral under U(1)_B x U(1)_L

Take equal fundamental VEV magnitudes u in the symmetric limit and choose
orthogonal Bloch directions

    n_B = e_1
    n_L = e_3.

The adjoint has

    <Phi^a> = v n^a(beta),

with

    n(beta) = (sin beta, 0, cos beta).

An exact Phi -> -Phi symmetry forbids the renormalizable orientation-sensitive
cubic H^dagger Phi H.  For SU(2),

    Phi^2 proportional to I,

so H^dagger Phi^2 H is orientation independent.

MASS MATRIX
-----------
For one SU(2) doublet H_i with U(1)_i charge +1,

    M_ii^2 = g_i^2 u^2,

    M_{i,a}^2 = (g_X g_i u^2 / 2) n_i^a,

and each doublet contributes

    g_X^2 u^2 / 4

isotropically to the SU(2) vector block.

With both H_B and H_L present, the exact 5 x 5 mass-squared matrix in the basis

    (B, L, X_1, X_2, X_3)

is

    M^2 =
    [ g_B^2 u^2, 0, c_B, 0, 0
      0, g_L^2 u^2, 0, 0, c_L
      c_B, 0, *, *, *
      0, 0, *, *, *
      0, c_L, *, *, * ],

where

    c_B = g_X g_B u^2 / 2,
    c_L = g_X g_L u^2 / 2,

and the SU(2) block is

    (g_X^2 u^2 / 2) I
    +
    g_X^2 v^2 (I - n n^T).

When

    g_B = g_L = g

and the two fundamental VEVs are equal, changing beta is equivalent to an
orthogonal similarity transformation in the degenerate B/L + X_1/X_3
subspace.  The full heavy-vector spectrum is therefore beta independent while
the fixed-current inverse-propagator element [M^-2]_{BL} changes with beta.

This is a physical relative orientation, not a common gauge rotation, because
the gauge-invariant quantities

    n . n_B
    n . n_L

change with beta while n_B . n_L remains fixed.

LOW-ENERGY RESPONSE
-------------------
The inherited target operator is

    C_phi phi J_B^mu J_{L,mu}

with

    C_phi = 9.536416387852626e-20 eV^-3.

If the protected Wilson angle theta controls beta through the optimistic smooth
response

    beta(theta) = kappa sin(theta),

then

    C_phi
      = (g_B g_L / f)
        |d[M^-2]_{BL}/d beta|
        |d beta/d theta|.

The run solves kappa at the actual terrestrial theta inherited from 019A.

ULTRALIGHT NATURALNESS TEST
---------------------------
Exact B <-> L degeneracy is not a symmetry of ordinary baryon and lepton
matter.  Parameterize the first exchange-breaking deformation as

    g_B = g (1 + epsilon),
    g_L = g (1 - epsilon).

For the tested mass matrix, Tr M^2 and Tr M^4 remain beta independent even
after this deformation.  Consequently the beta-dependent one-loop vector
Coleman-Weinberg curvature is finite and renormalization-scale independent at
this order.

The finite vector contribution is evaluated from

    V_1(beta)
      = 3/(64 pi^2)
        sum_i m_i^4(beta)
        [log(m_i^2/Q^2) - 5/6].

Because d_theta^2 Tr M^4 = 0, the theta curvature is independent of Q.

The induced ultralight mass is

    delta m_phi^2
      = (1/f^2) d^2 V_1 / d theta^2.

The script determines the maximum |epsilon| compatible with

    |delta m_phi^2| <= m_phi^2.

It then compares this required degeneracy with two deliberately conservative
radiative-size diagnostics:

    epsilon_loop_proxy
      = g^2/(16 pi^2)

and an *extra* artificially suppressed comparison

    epsilon_ultraoptimistic
      = 1e-4 * g^2/(16 pi^2).

These are NATURALNESS PROXIES, not claimed exact Standard-Model threshold
predictions.  Their role is to ask whether the required B/L degeneracy is so
extreme that even four additional orders of suppression beyond a generic
one-loop size would still be insufficient.

PARAMETER SEARCH
----------------
The scan varies:

    g_X
    g
    r = v/u

over a compact perturbative grid.

For every point the overall scale u is chosen so that the lightest heavy vector
lies exactly at the preferred boundary

    M_min = 2 Lambda_mat.

The target C_phi is then solved for kappa.  Points requiring kappa > 1 are
discarded.

The broad scan uses a stable dimensionless Coleman-Weinberg shape at
epsilon_ref = 1e-3.  The best point is then reconstructed independently using
high-precision mpmath eigenvalues and automatic second derivatives at a smaller
epsilon.

INPUTS
------
The script reads executed logs from:

    019A
    019B
    019C
    020A1

and refuses to proceed if the required upstream markers are absent.

UNITS
-----
Natural units hbar = c = 1.
Masses and decay constants are in eV.
C_phi is in eV^-3.

VALIDATION
----------
The run checks:

- 020A1 upstream decision;
- exact isospectrality of the full 5 x 5 symmetric mass matrix;
- independent spectral invariants Tr M^2, Tr M^4, Tr M^6;
- physical gauge-invariant relative-angle diagnostics;
- analytic/finite-difference current-kernel response;
- exact target C_phi reconstruction;
- preferred EFT mass margin;
- beta-independent Tr M^2 and Tr M^4 after exchange breaking;
- one-loop Coleman-Weinberg Q independence;
- broad parameter scan;
- high-precision reconstruction of the best scan point;
- linearity of the small-epsilon naturalness response.

FALSIFICATION / STOP RULE
-------------------------
The minimal SU(2) isospectral current embedding is rejected if the complete
tested region requires a B/L degeneracy smaller than the deliberately
ultraoptimistic radiative-size proxy by a substantial factor.

This rejects only the minimal exchange-symmetric SU(2) current embedding tested
here.  It does not prove that every imaginable non-Abelian portal fails.

However, if rescue requires mirror copies or additional sectors whose primary
purpose is to impose a new exact B <-> L symmetry on ordinary matter, the
project buildplan's anti-complexity stop rule is triggered and the branch should
be globally reranked rather than enlarged automatically.

PROMOTION CONDITION
-------------------
A positive result would require:

    RENORMALIZABLE_NONABELIAN_CURRENT_EMBEDDING=YES
    PHYSICAL_ISOSPECTRAL_RESPONSE=YES
    TARGET_C_PHI_MATCH=PASS
    PREFERRED_EFT_MARGIN=PASS
    ULTRALIGHT_MASS_NATURALNESS=PASS
    NO_TUNED_B_L_DEGENERACY=PASS

Even a positive result would still not establish complete operator mixing,
2026 experimental safety, astrophysical safety, a real material, practical
power/energy, or a practical antigravity device.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_020A2_NONABELIAN_ISOSPECTRAL_CURRENT_EMBEDDING_NATURALNESS_GATE
"""

from __future__ import annotations

import hashlib
import math
from pathlib import Path
import re

import mpmath as mp
import numpy as np
from scipy.optimize import brentq


ROOT = Path(__file__).resolve().parents[1]

A_LOG = ROOT / "results/logs/019a_wilson_line_sequestered_pair_scalar_uv_protection_gate.log"
B_LOG = ROOT / "results/logs/019b_anomaly_free_sm_material_endpoint_and_one_body_mixing_gate.log"
C_LOG = ROOT / "results/logs/019c_vector_wilson_portal_minimal_uv_construction_gate.log"
D_LOG = ROOT / "results/logs/020a1_collective_isospectral_vector_rotation_representation_gate.log"

D_SOURCE = ROOT / "simulations/020a1_collective_isospectral_vector_rotation_representation_gate.py"

TARGET_C_PHI = 9.536416387852626e-20
TARGET_M_PHI = 3.946539608e-11
MATERIAL_EFT_CUTOFF = 657.7566
PREFERRED_MARGIN = 2.0
PERTURBATIVE_G_MAX = math.sqrt(4.0 * math.pi)

MAX_SPECTRAL_DRIFT = 1.0e-11
MAX_MATCH_RELERR = 1.0e-8
MAX_KERNEL_DERIV_RELERR = 1.0e-7
MAX_KAPPA = 1.0
EPS_SCAN = 1.0e-3
EPS_HP = 1.0e-4

GX_GRID = np.geomspace(0.30, 3.50, 8)
G_GRID = np.geomspace(0.20, 3.50, 9)
R_GRID = np.geomspace(0.30, 3.50, 8)

# Blind wildcard values are diagnostics only, never evidence.
BLIND_WILDCARD_RATIOS = (1.6, 1.875, 3.125, 0.625, 5.0)


def require_marker(path: Path, marker: str) -> None:
    """Require an exact upstream scientific marker."""

    if not path.exists():
        raise RuntimeError(f"Missing upstream log: {path}")
    text = path.read_text()
    if marker not in text:
        raise RuntimeError(f"Missing required marker in {path.name}: {marker}")


def exact_scalar(path: Path, prefix: str) -> float:
    """Read one scientific scalar from an executed log."""

    if not path.exists():
        raise RuntimeError(f"Missing log: {path}")
    pattern = re.compile(rf"^{re.escape(prefix)}([+\-0-9.eE]+)$", re.MULTILINE)
    match = pattern.search(path.read_text())
    if match is None:
        raise RuntimeError(f"Could not find {prefix} in {path.name}")
    return float(match.group(1))


def sha256(path: Path) -> str:
    """Return SHA-256 for an upstream source file."""

    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_error(a: float, b: float) -> float:
    """Return robust relative error."""

    return abs(a - b) / max(abs(a), abs(b), 1.0e-300)


def unit_vector(beta: float) -> np.ndarray:
    """Return adjoint orientation n(beta)."""

    return np.array([math.sin(beta), 0.0, math.cos(beta)], dtype=float)


def dimensionless_mass2(
    beta: float,
    g_x: float,
    g: float,
    r: float,
    epsilon: float = 0.0,
) -> np.ndarray:
    """Return M^2/u^2 for the minimal SU(2)_X x U(1)_B x U(1)_L model.

    Basis:
        (B, L, X1, X2, X3)

    The physical adjoint VEV is v = r*u.
    """

    g_b = g * (1.0 + epsilon)
    g_l = g * (1.0 - epsilon)

    n = unit_vector(beta)

    matrix = np.zeros((5, 5), dtype=float)

    matrix[0, 0] = g_b * g_b
    matrix[1, 1] = g_l * g_l

    # Two equal SU(2) fundamentals contribute g_X^2 u^2 / 2 * I.
    su2 = (g_x * g_x / 2.0) * np.eye(3)

    # Real adjoint contribution g_X^2 v^2 (I - n n^T).
    su2 += g_x * g_x * r * r * (np.eye(3) - np.outer(n, n))
    matrix[2:, 2:] = su2

    c_b = g_x * g_b / 2.0
    c_l = g_x * g_l / 2.0

    # H_B Bloch direction e1; H_L Bloch direction e3.
    matrix[0, 2] = c_b
    matrix[2, 0] = c_b

    matrix[1, 4] = c_l
    matrix[4, 1] = c_l

    return matrix


def physical_mass2(
    beta: float,
    g_x: float,
    g: float,
    u: float,
    r: float,
    epsilon: float = 0.0,
) -> np.ndarray:
    """Return physical M^2 in eV^2."""

    return u * u * dimensionless_mass2(beta, g_x, g, r, epsilon)


def scale_u_to_margin(g_x: float, g: float, r: float) -> float | None:
    """Choose u so the lightest vector is exactly at 2 Lambda_mat."""

    eig = np.linalg.eigvalsh(dimensionless_mass2(0.0, g_x, g, r, 0.0))
    smallest = float(np.min(eig))
    if smallest <= 1.0e-14:
        return None

    target_mass = PREFERRED_MARGIN * MATERIAL_EFT_CUTOFF
    return target_mass / math.sqrt(smallest)


def cross_kernel(
    beta: float,
    g_x: float,
    g: float,
    u: float,
    r: float,
    epsilon: float = 0.0,
) -> float:
    """Return [M^-2]_{BL} in eV^-2."""

    inverse = np.linalg.inv(physical_mass2(beta, g_x, g, u, r, epsilon))
    return float(inverse[0, 1])


def cross_kernel_derivative_beta_fd(
    beta: float,
    g_x: float,
    g: float,
    u: float,
    r: float,
    step: float = 1.0e-5,
) -> float:
    """Independent finite-difference derivative d[M^-2]BL/d beta."""

    plus = cross_kernel(beta + step, g_x, g, u, r)
    minus = cross_kernel(beta - step, g_x, g, u, r)
    return (plus - minus) / (2.0 * step)


def cross_kernel_derivative_beta_matrix(
    beta: float,
    g_x: float,
    g: float,
    u: float,
    r: float,
) -> float:
    """Matrix-identity derivative -[M^-2 M_beta^2 M^-2]_{BL}."""

    step = 1.0e-6
    m_plus = physical_mass2(beta + step, g_x, g, u, r)
    m_minus = physical_mass2(beta - step, g_x, g, u, r)
    dm = (m_plus - m_minus) / (2.0 * step)

    inverse = np.linalg.inv(physical_mass2(beta, g_x, g, u, r))
    return float(-(inverse @ dm @ inverse)[0, 1])


def c_phi_for_kappa(
    kappa: float,
    theta_earth: float,
    f: float,
    g_x: float,
    g: float,
    u: float,
    r: float,
) -> float:
    """Return C_phi for beta(theta)=kappa sin(theta)."""

    beta = kappa * math.sin(theta_earth)
    dkernel_dbeta = cross_kernel_derivative_beta_matrix(
        beta,
        g_x,
        g,
        u,
        r,
    )
    beta_theta = kappa * math.cos(theta_earth)

    return (g * g / f) * abs(dkernel_dbeta * beta_theta)


def solve_kappa(
    theta_earth: float,
    f: float,
    g_x: float,
    g: float,
    u: float,
    r: float,
) -> float | None:
    """Solve the first small positive kappa matching the target."""

    grid = np.logspace(-5, 0, 180)
    values = [
        c_phi_for_kappa(k, theta_earth, f, g_x, g, u, r) - TARGET_C_PHI
        for k in grid
    ]

    for left, right, f_left, f_right in zip(
        grid[:-1],
        grid[1:],
        values[:-1],
        values[1:],
        strict=True,
    ):
        if f_left <= 0.0 <= f_right:
            return float(
                brentq(
                    lambda x: c_phi_for_kappa(
                        x,
                        theta_earth,
                        f,
                        g_x,
                        g,
                        u,
                        r,
                    )
                    - TARGET_C_PHI,
                    left,
                    right,
                    xtol=1.0e-14,
                    rtol=1.0e-12,
                )
            )

    return None


def spectral_invariants(matrix: np.ndarray) -> tuple[float, float, float]:
    """Return Tr M^2, Tr M^4, Tr M^6 for a mass-squared matrix."""

    m2 = matrix
    m4 = m2 @ m2
    m6 = m4 @ m2
    return (
        float(np.trace(m2)),
        float(np.trace(m4)),
        float(np.trace(m6)),
    )


def spectral_shape(
    theta: float,
    epsilon: float,
    kappa: float,
    g_x: float,
    g: float,
    r: float,
) -> float:
    """Dimensionless theta-dependent one-loop shape sum lambda^2 log lambda.

    Overall u^4 is restored outside this function.

    Tr M^4 is theta independent in this model, so all terms proportional to
    log(Q^2) or the vector-scheme constant drop out of the theta curvature.
    """

    beta = kappa * math.sin(theta)
    eig = np.linalg.eigvalsh(dimensionless_mass2(beta, g_x, g, r, epsilon))
    if np.any(eig <= 0.0):
        raise RuntimeError("Non-positive vector mass eigenvalue")
    return float(np.sum(eig * eig * np.log(eig)))


def second_derivative_five_point(function, x: float = 0.0, h: float = 1.0e-3) -> float:
    """Five-point second derivative."""

    return (
        -function(x + 2.0 * h)
        + 16.0 * function(x + h)
        - 30.0 * function(x)
        + 16.0 * function(x - h)
        - function(x - 2.0 * h)
    ) / (12.0 * h * h)


def naturalness_ratio_double(
    epsilon: float,
    kappa: float,
    g_x: float,
    g: float,
    u: float,
    r: float,
    f: float,
) -> float:
    """Return |delta m_phi^2|/m_phi^2 from finite vector CW curvature."""

    d2_shape = second_derivative_five_point(
        lambda theta: spectral_shape(
            theta,
            epsilon,
            kappa,
            g_x,
            g,
            r,
        )
    )

    d2_v = 3.0 * u**4 / (64.0 * math.pi**2) * d2_shape
    delta_m2 = abs(d2_v) / (f * f)

    return delta_m2 / (TARGET_M_PHI * TARGET_M_PHI)


def mp_mass2(
    beta: mp.mpf,
    epsilon: mp.mpf,
    g_x: mp.mpf,
    g: mp.mpf,
    u: mp.mpf,
    r: mp.mpf,
) -> mp.matrix:
    """High-precision physical mass-squared matrix."""

    g_b = g * (1 + epsilon)
    g_l = g * (1 - epsilon)

    n = (mp.sin(beta), mp.mpf("0"), mp.cos(beta))
    v = r * u

    matrix = mp.matrix(5, 5)

    matrix[0, 0] = g_b**2 * u**2
    matrix[1, 1] = g_l**2 * u**2

    for i in range(3):
        for j in range(3):
            identity = mp.mpf("1") if i == j else mp.mpf("0")
            matrix[2 + i, 2 + j] = (
                g_x**2 * u**2 / 2 * identity
                + g_x**2 * v**2 * (identity - n[i] * n[j])
            )

    c_b = g_x * g_b * u**2 / 2
    c_l = g_x * g_l * u**2 / 2

    matrix[0, 2] = c_b
    matrix[2, 0] = c_b
    matrix[1, 4] = c_l
    matrix[4, 1] = c_l

    return matrix


def naturalness_ratio_high_precision(
    epsilon: float,
    kappa: float,
    g_x: float,
    g: float,
    u: float,
    r: float,
    f: float,
) -> float:
    """Independent high-precision CW curvature using mp.eigsy + mp.diff."""

    mp.mp.dps = 60

    eps_mp = mp.mpf(str(epsilon))
    kap_mp = mp.mpf(str(kappa))
    gx_mp = mp.mpf(str(g_x))
    g_mp = mp.mpf(str(g))
    u_mp = mp.mpf(str(u))
    r_mp = mp.mpf(str(r))
    f_mp = mp.mpf(str(f))
    mphi_mp = mp.mpf(str(TARGET_M_PHI))

    def potential(theta: mp.mpf) -> mp.mpf:
        beta = kap_mp * mp.sin(theta)
        eig, _ = mp.eigsy(
            mp_mass2(
                beta,
                eps_mp,
                gx_mp,
                g_mp,
                u_mp,
                r_mp,
            )
        )

        total = mp.fsum(
            mass2**2 * (mp.log(mass2) - mp.mpf(5) / 6)
            for mass2 in eig
        )
        return 3 * total / (64 * mp.pi**2)

    d2 = mp.diff(potential, mp.mpf("0"), 2)
    ratio = abs(d2) / (f_mp**2 * mphi_mp**2)
    return float(ratio)


def main() -> None:
    """Execute the complete 020A2 gate."""

    print("=== 020A2 — NON-ABELIAN ISOSPECTRAL B/L CURRENT EMBEDDING + NATURALNESS GATE ===")

    require_marker(
        A_LOG,
        "019A_WILSON_LINE_SEQUESTERED_PAIR_SCALAR_UV_PROTECTION_GATE=GREEN",
    )
    require_marker(
        B_LOG,
        "VECTOR_CURRENT_ONE_BODY_MIXING_PREFLIGHT=PASS",
    )
    require_marker(
        C_LOG,
        "019C_MINIMAL_ABELIAN_VECTOR_WILSON_UV_CONSTRUCTION_GATE=GREEN_NEGATIVE_RESULT",
    )
    require_marker(
        D_LOG,
        "020A1_COLLECTIVE_ISOSPECTRAL_VECTOR_REPRESENTATION_GATE=GREEN_NEGATIVE_RESULT",
    )
    require_marker(
        D_LOG,
        "SU2_RENORMALIZABLE_ISOSPECTRAL_REPRESENTATION=PASS",
    )

    selected_f = exact_scalar(A_LOG, "SELECTED_F_EV=")
    theta_earth = exact_scalar(A_LOG, "SELECTED_THETA_EARTH=")

    print("\n=== UPSTREAM AUDIT ===")
    print(f"020A1_SOURCE_SHA256={sha256(D_SOURCE)}")
    print(f"SELECTED_F_EV={selected_f:.15e}")
    print(f"SELECTED_THETA_EARTH={theta_earth:.15e}")
    print("019A_WILSON_PROTECTION=RETAINED")
    print("019B_ANOMALY_FREE_B_L_CURRENT_ENDPOINT=RETAINED")
    print("019C_VECTOR_HIGGS_MEDIATOR_ALGEBRA=RETAINED")
    print("020A1_SU2_ISOSPECTRAL_REPRESENTATION=RETAINED")

    # ------------------------------------------------------------------
    # A. Exact symmetric 5x5 renormalizable witness.
    # ------------------------------------------------------------------
    print("\n=== A — FULL RENORMALIZABLE 5x5 ISOSPECTRAL MASS MATRIX ===")

    bench_gx = 1.0
    bench_g = 1.0
    bench_r = 1.0
    bench_u = scale_u_to_margin(bench_gx, bench_g, bench_r)
    if bench_u is None:
        raise RuntimeError("Benchmark scaling failed")

    beta_grid = np.linspace(-math.pi, math.pi, 121)
    ref_matrix = physical_mass2(
        beta_grid[0],
        bench_gx,
        bench_g,
        bench_u,
        bench_r,
    )
    ref_eig = np.linalg.eigvalsh(ref_matrix)
    ref_inv = spectral_invariants(ref_matrix)

    max_eig_drift = 0.0
    max_tr2_drift = 0.0
    max_tr4_drift = 0.0
    max_tr6_drift = 0.0

    for beta in beta_grid[1:]:
        matrix = physical_mass2(
            beta,
            bench_gx,
            bench_g,
            bench_u,
            bench_r,
        )
        eig = np.linalg.eigvalsh(matrix)
        inv = spectral_invariants(matrix)

        max_eig_drift = max(
            max_eig_drift,
            float(
                np.max(
                    np.abs(eig - ref_eig)
                    / np.maximum(np.abs(ref_eig), 1.0e-300)
                )
            ),
        )

        max_tr2_drift = max(
            max_tr2_drift,
            relative_error(inv[0], ref_inv[0]),
        )
        max_tr4_drift = max(
            max_tr4_drift,
            relative_error(inv[1], ref_inv[1]),
        )
        max_tr6_drift = max(
            max_tr6_drift,
            relative_error(inv[2], ref_inv[2]),
        )

    symmetric_iso_pass = (
        max_eig_drift <= MAX_SPECTRAL_DRIFT
        and max_tr2_drift <= MAX_SPECTRAL_DRIFT
        and max_tr4_drift <= MAX_SPECTRAL_DRIFT
        and max_tr6_drift <= MAX_SPECTRAL_DRIFT
    )

    masses = np.sqrt(ref_eig)

    print(f"BENCH_U_EV={bench_u:.15e}")
    print(f"BENCH_V_EV={bench_u * bench_r:.15e}")
    print(
        "BENCH_VECTOR_MASSES_EV="
        + ",".join(f"{mass:.12e}" for mass in masses)
    )
    print(f"BENCH_MIN_VECTOR_OVER_EFT={masses[0] / MATERIAL_EFT_CUTOFF:.15e}")
    print(f"FULL5X5_MAX_EIGENVALUE_REL_DRIFT={max_eig_drift:.15e}")
    print(f"FULL5X5_MAX_TR_M2_REL_DRIFT={max_tr2_drift:.15e}")
    print(f"FULL5X5_MAX_TR_M4_REL_DRIFT={max_tr4_drift:.15e}")
    print(f"FULL5X5_MAX_TR_M6_REL_DRIFT={max_tr6_drift:.15e}")
    print(
        "RENORMALIZABLE_FULL5X5_ISOSPECTRAL_VECTOR_WITNESS="
        + ("PASS" if symmetric_iso_pass else "FAIL")
    )

    # ------------------------------------------------------------------
    # B. Physical gauge-invariant relative orientation.
    # ------------------------------------------------------------------
    print("\n=== B — PHYSICAL RELATIVE-ANGLE / GAUGE-INVARIANT AUDIT ===")

    n_b = np.array([1.0, 0.0, 0.0])
    n_l = np.array([0.0, 0.0, 1.0])

    beta_a = 0.173
    beta_b = 0.411

    n_a = unit_vector(beta_a)
    n_betab = unit_vector(beta_b)

    inv_b_l = float(np.dot(n_b, n_l))
    inv_phi_b_a = float(np.dot(n_a, n_b))
    inv_phi_l_a = float(np.dot(n_a, n_l))
    inv_phi_b_b = float(np.dot(n_betab, n_b))
    inv_phi_l_b = float(np.dot(n_betab, n_l))

    physical_relative_angle = (
        abs(inv_phi_b_a - inv_phi_b_b) > 1.0e-6
        and abs(inv_phi_l_a - inv_phi_l_b) > 1.0e-6
        and abs(inv_b_l) <= 1.0e-14
    )

    print(f"N_B_DOT_N_L={inv_b_l:.15e}")
    print(f"BETA_A_NPHI_DOT_NB={inv_phi_b_a:.15e}")
    print(f"BETA_A_NPHI_DOT_NL={inv_phi_l_a:.15e}")
    print(f"BETA_B_NPHI_DOT_NB={inv_phi_b_b:.15e}")
    print(f"BETA_B_NPHI_DOT_NL={inv_phi_l_b:.15e}")
    print(
        "SU2_ISOSPECTRAL_ROTATION_IS_PHYSICAL_RELATIVE_ORIENTATION="
        + ("PASS" if physical_relative_angle else "FAIL")
    )

    # ------------------------------------------------------------------
    # C. Target response at the real terrestrial Wilson angle.
    # ------------------------------------------------------------------
    print("\n=== C — TARGET C_PHI MATCH ===")

    bench_kappa = solve_kappa(
        theta_earth,
        selected_f,
        bench_gx,
        bench_g,
        bench_u,
        bench_r,
    )
    if bench_kappa is None:
        raise RuntimeError("Benchmark cannot match target C_phi")

    bench_beta_earth = bench_kappa * math.sin(theta_earth)

    derivative_matrix = cross_kernel_derivative_beta_matrix(
        bench_beta_earth,
        bench_gx,
        bench_g,
        bench_u,
        bench_r,
    )
    derivative_fd = cross_kernel_derivative_beta_fd(
        bench_beta_earth,
        bench_gx,
        bench_g,
        bench_u,
        bench_r,
    )

    derivative_relerr = relative_error(derivative_matrix, derivative_fd)

    bench_c = c_phi_for_kappa(
        bench_kappa,
        theta_earth,
        selected_f,
        bench_gx,
        bench_g,
        bench_u,
        bench_r,
    )
    c_relerr = relative_error(bench_c, TARGET_C_PHI)

    match_pass = (
        bench_kappa <= MAX_KAPPA
        and derivative_relerr <= MAX_KERNEL_DERIV_RELERR
        and c_relerr <= MAX_MATCH_RELERR
    )

    print(f"BENCH_KAPPA={bench_kappa:.15e}")
    print(f"BENCH_BETA_EARTH={bench_beta_earth:.15e}")
    print(f"BENCH_DMINV_BL_DBETA_MATRIX={derivative_matrix:.15e}")
    print(f"BENCH_DMINV_BL_DBETA_FD={derivative_fd:.15e}")
    print(f"BENCH_KERNEL_DERIVATIVE_RELERR={derivative_relerr:.15e}")
    print(f"BENCH_C_PHI_RECONSTRUCTED={bench_c:.15e}")
    print(f"BENCH_C_PHI_MATCH_RELERR={c_relerr:.15e}")
    print("TARGET_C_PHI_MATCH=" + ("PASS" if match_pass else "FAIL"))

    # ------------------------------------------------------------------
    # D. Exchange-breaking finite-CW structure.
    # ------------------------------------------------------------------
    print("\n=== D — B/L EXCHANGE-BREAKING FINITE CW STRUCTURE ===")

    eps_check = 0.01
    ref_eps_inv = None
    max_eps_tr2 = 0.0
    max_eps_tr4 = 0.0
    max_eps_tr6 = 0.0
    max_eps_eig = 0.0

    for index, beta in enumerate(np.linspace(-1.0, 1.0, 81)):
        matrix = physical_mass2(
            beta,
            bench_gx,
            bench_g,
            bench_u,
            bench_r,
            eps_check,
        )
        eig = np.linalg.eigvalsh(matrix)
        inv = spectral_invariants(matrix)

        if index == 0:
            ref_eps_inv = inv
            ref_eps_eig = eig
            continue

        assert ref_eps_inv is not None
        max_eps_tr2 = max(
            max_eps_tr2,
            relative_error(inv[0], ref_eps_inv[0]),
        )
        max_eps_tr4 = max(
            max_eps_tr4,
            relative_error(inv[1], ref_eps_inv[1]),
        )
        max_eps_tr6 = max(
            max_eps_tr6,
            relative_error(inv[2], ref_eps_inv[2]),
        )
        max_eps_eig = max(
            max_eps_eig,
            float(
                np.max(
                    np.abs(eig - ref_eps_eig)
                    / np.maximum(np.abs(ref_eps_eig), 1.0e-300)
                )
            ),
        )

    finite_cw_structure = (
        max_eps_tr2 <= 1.0e-11
        and max_eps_tr4 <= 1.0e-11
        and max_eps_eig > 1.0e-8
    )

    print(f"EXCHANGE_BREAK_EPSILON_CHECK={eps_check:.15e}")
    print(f"EXCHANGE_BREAK_MAX_EIGENVALUE_REL_DRIFT={max_eps_eig:.15e}")
    print(f"EXCHANGE_BREAK_MAX_TR_M2_REL_DRIFT={max_eps_tr2:.15e}")
    print(f"EXCHANGE_BREAK_MAX_TR_M4_REL_DRIFT={max_eps_tr4:.15e}")
    print(f"EXCHANGE_BREAK_MAX_TR_M6_REL_DRIFT={max_eps_tr6:.15e}")
    print(
        "EXCHANGE_BREAK_THETA_CW_IS_FINITE_AT_ONE_LOOP="
        + ("PASS" if finite_cw_structure else "FAIL")
    )
    print(
        "REASON="
        "TR_M2_AND_TR_M4_THETA_INDEPENDENT_WHILE_FULL_SPECTRUM_CHANGES"
    )

    # Q-independence audit: because Tr M^4 has no theta curvature, changing Q
    # changes only a theta-independent term.
    def cw_curvature_with_q(q_ev: float) -> float:
        def potential(theta: float) -> float:
            beta = bench_kappa * math.sin(theta)
            eig = np.linalg.eigvalsh(
                physical_mass2(
                    beta,
                    bench_gx,
                    bench_g,
                    bench_u,
                    bench_r,
                    eps_check,
                )
            )
            return float(
                3.0
                / (64.0 * math.pi**2)
                * np.sum(
                    eig
                    * eig
                    * (np.log(eig / (q_ev * q_ev)) - 5.0 / 6.0)
                )
            )

        return second_derivative_five_point(potential, h=1.0e-3)

    q1 = MATERIAL_EFT_CUTOFF
    q2 = 10.0 * MATERIAL_EFT_CUTOFF
    curv_q1 = cw_curvature_with_q(q1)
    curv_q2 = cw_curvature_with_q(q2)
    q_relerr = relative_error(curv_q1, curv_q2)

    print(f"CW_CURVATURE_Q1={curv_q1:.15e}")
    print(f"CW_CURVATURE_Q2={curv_q2:.15e}")
    print(f"CW_CURVATURE_Q_RELERR={q_relerr:.15e}")

    # ------------------------------------------------------------------
    # E. Robust perturbative region scan.
    # ------------------------------------------------------------------
    print("\n=== E — ROBUST PARAMETER REGION NATURALNESS SCAN ===")

    candidates: list[dict[str, float]] = []

    for g_x in GX_GRID:
        for g in G_GRID:
            if g_x > PERTURBATIVE_G_MAX or g > PERTURBATIVE_G_MAX:
                continue

            for r in R_GRID:
                u = scale_u_to_margin(float(g_x), float(g), float(r))
                if u is None:
                    continue

                kappa = solve_kappa(
                    theta_earth,
                    selected_f,
                    float(g_x),
                    float(g),
                    u,
                    float(r),
                )
                if kappa is None or kappa > MAX_KAPPA:
                    continue

                ratio = naturalness_ratio_double(
                    EPS_SCAN,
                    kappa,
                    float(g_x),
                    float(g),
                    u,
                    float(r),
                    selected_f,
                )

                if not math.isfinite(ratio) or ratio <= 0.0:
                    continue

                epsilon_allowed = EPS_SCAN / ratio
                loop_proxy = float(g) ** 2 / (16.0 * math.pi**2)
                ultra_proxy = 1.0e-4 * loop_proxy

                masses_here = np.sqrt(
                    np.linalg.eigvalsh(
                        physical_mass2(
                            0.0,
                            float(g_x),
                            float(g),
                            u,
                            float(r),
                        )
                    )
                )

                candidates.append(
                    {
                        "g_x": float(g_x),
                        "g": float(g),
                        "r": float(r),
                        "u": u,
                        "v": u * float(r),
                        "kappa": kappa,
                        "epsilon_allowed_est": epsilon_allowed,
                        "loop_proxy": loop_proxy,
                        "ultra_proxy": ultra_proxy,
                        "generic_deficit": loop_proxy / epsilon_allowed,
                        "ultra_deficit": ultra_proxy / epsilon_allowed,
                        "min_mass": float(masses_here[0]),
                        "max_mass": float(masses_here[-1]),
                    }
                )

    if not candidates:
        raise RuntimeError("No perturbative target-matching scan points survived")

    candidates.sort(key=lambda item: item["generic_deficit"])
    best = candidates[0]

    print(f"SCAN_SURVIVING_TARGET_MATCH_POINTS={len(candidates)}")
    print(f"SCAN_BEST_GX={best['g_x']:.15e}")
    print(f"SCAN_BEST_G={best['g']:.15e}")
    print(f"SCAN_BEST_V_OVER_U={best['r']:.15e}")
    print(f"SCAN_BEST_U_EV={best['u']:.15e}")
    print(f"SCAN_BEST_V_EV={best['v']:.15e}")
    print(f"SCAN_BEST_KAPPA={best['kappa']:.15e}")
    print(f"SCAN_BEST_MIN_VECTOR_EV={best['min_mass']:.15e}")
    print(f"SCAN_BEST_MAX_VECTOR_EV={best['max_mass']:.15e}")
    print(f"SCAN_BEST_EPSILON_ALLOWED_EST={best['epsilon_allowed_est']:.15e}")
    print(f"SCAN_BEST_GENERIC_LOOP_PROXY={best['loop_proxy']:.15e}")
    print(f"SCAN_BEST_ULTRAOPTIMISTIC_PROXY={best['ultra_proxy']:.15e}")
    print(f"SCAN_BEST_GENERIC_NATURALNESS_DEFICIT={best['generic_deficit']:.15e}")
    print(f"SCAN_BEST_ULTRAOPTIMISTIC_DEFICIT={best['ultra_deficit']:.15e}")

    # ------------------------------------------------------------------
    # F. High-precision independent reconstruction of best point.
    # ------------------------------------------------------------------
    print("\n=== F — HIGH-PRECISION BEST-POINT RECONSTRUCTION ===")

    hp_ratio = naturalness_ratio_high_precision(
        EPS_HP,
        best["kappa"],
        best["g_x"],
        best["g"],
        best["u"],
        best["r"],
        selected_f,
    )

    hp_epsilon_allowed = EPS_HP / hp_ratio
    hp_generic_deficit = best["loop_proxy"] / hp_epsilon_allowed
    hp_ultra_deficit = best["ultra_proxy"] / hp_epsilon_allowed

    # Local linearity validation around the high-precision epsilon.
    hp_ratio_half = naturalness_ratio_high_precision(
        EPS_HP / 2.0,
        best["kappa"],
        best["g_x"],
        best["g"],
        best["u"],
        best["r"],
        selected_f,
    )
    hp_ratio_double = naturalness_ratio_high_precision(
        EPS_HP * 2.0,
        best["kappa"],
        best["g_x"],
        best["g"],
        best["u"],
        best["r"],
        selected_f,
    )

    slope_center = hp_ratio / EPS_HP
    slope_half = hp_ratio_half / (EPS_HP / 2.0)
    slope_double = hp_ratio_double / (EPS_HP * 2.0)

    linearity_relspread = (
        max(slope_half, slope_center, slope_double)
        - min(slope_half, slope_center, slope_double)
    ) / max(slope_center, 1.0e-300)

    print(f"HP_EPSILON={EPS_HP:.15e}")
    print(f"HP_DM2_OVER_MPHI2={hp_ratio:.15e}")
    print(f"HP_EPSILON_ALLOWED={hp_epsilon_allowed:.15e}")
    print(f"HP_GENERIC_LOOP_PROXY={best['loop_proxy']:.15e}")
    print(f"HP_ULTRAOPTIMISTIC_PROXY={best['ultra_proxy']:.15e}")
    print(f"HP_GENERIC_NATURALNESS_DEFICIT={hp_generic_deficit:.15e}")
    print(f"HP_ULTRAOPTIMISTIC_DEFICIT={hp_ultra_deficit:.15e}")
    print(f"HP_SMALL_EPSILON_LINEARITY_RELSPREAD={linearity_relspread:.15e}")

    # ------------------------------------------------------------------
    # Blind wildcard diagnostics.
    # ------------------------------------------------------------------
    print("\n=== BLIND WILDCARD RATIO DIAGNOSTICS — NOT EVIDENCE ===")

    for ratio in BLIND_WILDCARD_RATIOS:
        u = scale_u_to_margin(bench_gx, bench_g, ratio)
        if u is None:
            print(f"WILDCARD_RATIO={ratio:.6f} STATUS=NO_POSITIVE_MASS")
            continue

        kappa = solve_kappa(
            theta_earth,
            selected_f,
            bench_gx,
            bench_g,
            u,
            ratio,
        )
        if kappa is None:
            print(f"WILDCARD_RATIO={ratio:.6f} STATUS=NO_TARGET_MATCH")
            continue

        print(
            f"WILDCARD_RATIO={ratio:.6f} "
            f"KAPPA={kappa:.15e} "
            f"U_EV={u:.15e} "
            f"V_EV={u * ratio:.15e}"
        )

    print("BLIND_WILDCARD_VALUES_USED_AS_EVIDENCE=NO")

    # ------------------------------------------------------------------
    # Decision.
    # ------------------------------------------------------------------
    print("\n=== 020A2 DECISION ===")

    all_core_witnesses = (
        symmetric_iso_pass
        and physical_relative_angle
        and match_pass
        and finite_cw_structure
        and q_relerr <= 1.0e-3
    )

    robust_naturalness_fail = hp_ultra_deficit > 1.0

    if not all_core_witnesses:
        print("020A2_NONABELIAN_ISOSPECTRAL_CURRENT_EMBEDDING_GATE=RED")
        print("REASON=INTERNAL_RECONSTRUCTION_OR_REQUIRED_WITNESS_FAILED")
        print("NEXT=DEBUG_BEFORE_SCIENTIFIC_INTERPRETATION")
    elif robust_naturalness_fail:
        print(
            "020A2_NONABELIAN_ISOSPECTRAL_CURRENT_EMBEDDING_GATE="
            "GREEN_NEGATIVE_RESULT"
        )
        print("RENORMALIZABLE_FULL5X5_ISOSPECTRAL_CURRENT_RESPONSE=SUPPORTED")
        print("PHYSICAL_RELATIVE_ORIENTATION=SUPPORTED")
        print("TARGET_PAIR_RESPONSE=SUPPORTED")
        print("PURE_VECTOR_SYMMETRIC_CW_THETA_DEPENDENCE=ZERO_BY_ISOSPECTRALITY")
        print("B_L_EXCHANGE_BREAKING_CW=FINITE_BUT_FATAL")
        print("MINIMAL_B_L_EXCHANGE_SYMMETRIC_SU2_PORTAL=REJECTED_BY_NATURALNESS")
        print(
            "EXACT_B_L_MATTER_EXCHANGE_SYMMETRY_REQUIRED_FOR_RESCUE="
            "YES"
        )
        print(
            "ADDING_MIRROR_MATTER_SOLELY_TO_ENFORCE_EXCHANGE_SYMMETRY="
            "BLOCKED_BY_ANTI_COMPLEXITY_STOP_RULE"
        )
        print("COMPLETE_MICROSCOPIC_VECTOR_WILSON_UV_WITNESS=NO")
        print("020A_MINIMAL_COLLECTIVE_TREE_CLASS=STRUCTURALLY_EXHAUSTED")
        print("020A2_SMALL_SU2_NONABELIAN_GATE=FAILS_MINIMAL_NATURALNESS")
        print("GLOBAL_RERANK=REQUIRED")
        print(
            "NEXT="
            "GLOBAL_RERANK_WITH_PRIORITY_ON_NEW_STRUCTURAL_SCALING_NOT_LARGER_QUIVER"
        )
    else:
        print("020A2_NONABELIAN_ISOSPECTRAL_CURRENT_EMBEDDING_GATE=GREEN")
        print("RENORMALIZABLE_FULL5X5_ISOSPECTRAL_CURRENT_RESPONSE=SUPPORTED")
        print("ULTRALIGHT_MASS_NATURALNESS=PASS")
        print("NEXT=COMPLETE_TRANSFER_SPURION_AND_ONE_BODY_OPERATOR_GATE")

    print("019A_WILSON_LINE_UV_PROTECTION_WITNESS=RETAINED")
    print("019B_ANOMALY_FREE_VECTOR_CURRENT_ENDPOINT=RETAINED")
    print("019C_VECTOR_HIGGS_MEDIATOR_ALGEBRA=RETAINED")
    print("020A1_ISOSPECTRAL_REPRESENTATION_RESULT=RETAINED")
    print("018B_FIELD_EXISTENCE_RESULT=RETAINED")
    print("018C_M2_STABILITY_FALSIFICATION=RETAINED")
    print("CURRENT_KNOWLEDGE_HEURISTIC=APPROXIMATELY_68_PERCENT_NOT_A_PROBABILITY")
    print("HEURISTIC_CHANGE=NONE_UNLESS_COMPLETE_PORTAL_SURVIVES")
    print("EXACT_2026_5KM_EXPERIMENTAL_BOUND=DEFER_UNTIL_COMPLETE_PORTAL_EXISTS")
    print("REAL_ANTIGRAVITY_MATERIAL=NO")
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
    print("NEW_PHYSICS_DISCOVERY=NO")
    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_020A2_NONABELIAN_ISOSPECTRAL_CURRENT_EMBEDDING_NATURALNESS_GATE"
    )


if __name__ == "__main__":
    main()
