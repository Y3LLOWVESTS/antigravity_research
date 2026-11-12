"""B15-M1: 3D two-U(1) frozen-matter Lorentzian action identity.

PURPOSE
-------
Verify independent U(1) gauge identities, Bianchi identities,
the corrected Lorentzian constitutive signs, and exact
static-action reciprocity in three spatial dimensions.

ACTION
------
E_i = -grad(phi_i)
B_i = curl(A_i)

L = 0.5*(E_X^2 + E_Y^2 - B_X^2 - B_Y^2)
    + theta*(E_X.B_Y + E_Y.B_X)

For a constant theta, the mixed term is topological and
produces no periodic bulk Euler-Lagrange contribution.

METHOD
------
Use a three-dimensional periodic centered-difference complex
on odd-sized Cartesian grids.

Build the two carrier sectors from the quadratic action,
assembling forward and reverse variation blocks independently.

Check:
- curl(grad) = 0
- div(curl) = 0
- independent U(1) gauge nullspaces
- Lorentzian action Hessian symmetry
- corrected positive-K cross-block skew reciprocity
- constant-theta topological cancellation
- mathematically conserved neutral external currents
- action derivative independent of its assembled Hessian

Odd grids exclude the exact even-grid Nyquist checkerboard
null mode, but do not establish continuum spectral health.

UNITS / ASSUMPTIONS
-------------------
The grid and theta normalization are arbitrary test units.
The theta profile is synthetic and prescribed.

Periodic boundaries are mathematical controls; they are not
R3B physical external-source boundaries.

CLAIM LIMITATIONS
-----------------
This is NOT a loaded 3D torus simulation, a complete
interacting matter action, a microscopic source construction,
a dynamic stability proof, or a complete-energy certificate.

No gravitational repulsion or device is certified.

CLAIM CLASSIFICATION
--------------------
FROZEN_THETA_STATIC_VARIATIONAL_IDENTITY_PREFLIGHT
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy import sparse as sp


BRANCH = "032H17A12D1R3X3B15-M1"


def periodic_derivative(n: int, h: float) -> sp.csr_matrix:
    """Periodic centered derivative; exclude even-grid Nyquist zero."""
    if n < 5 or n % 2 != 1 or h <= 0:
        raise ValueError(
            "Require odd n>=5 and h>0"
        )

    i = np.arange(n)

    return sp.coo_matrix(
        (
            np.r_[
                np.full(n, 0.5 / h),
                np.full(n, -0.5 / h),
            ],
            (
                np.r_[i, i],
                np.r_[(i + 1) % n, (i - 1) % n],
            ),
        ),
        shape=(n, n),
    ).tocsr()


def complex_3d(n: int, h: float):
    """Construct compatible 3D discrete grad and curl."""
    d = periodic_derivative(n, h)
    eye = sp.eye(n, format="csr")

    dx = sp.kron(
        sp.kron(d, eye), eye, format="csr"
    )

    dy = sp.kron(
        sp.kron(eye, d), eye, format="csr"
    )

    dz = sp.kron(
        sp.kron(eye, eye), d, format="csr"
    )

    zero = sp.csr_matrix(dx.shape)

    grad = sp.vstack(
        (dx, dy, dz),
        format="csr",
    )

    curl = sp.bmat(
        (
            (zero, -dz, dy),
            (dz, zero, -dx),
            (-dy, dx, zero),
        ),
        format="csr",
    )

    return grad, curl


def hessians(grad, curl, theta, h):
    """Construct independent Lorentzian action variations."""
    n = grad.shape[1]

    if (
        theta.shape != (n,)
        or not np.isfinite(theta).all()
    ):
        raise ValueError(
            "theta must be finite at every lattice site"
        )

    t3 = sp.block_diag(
        [
            sp.diags(theta, format="csr")
        ] * 3,
        format="csr",
    )

    ke = grad.T @ grad
    kb = curl.T @ curl

    # Separate Maxwell terms for X and Y.
    p = sp.block_diag(
        (ke, ke),
        format="csr",
    )

    b = sp.block_diag(
        (kb, kb),
        format="csr",
    )

    # Independently assemble opposite action variations.
    m = -(grad.T @ t3 @ curl)
    q = -(curl.T @ t3 @ grad)

    z = sp.csr_matrix(m.shape)

    upper = sp.bmat(
        ((z, m), (m, z)),
        format="csr",
    )

    lower = sp.bmat(
        ((z.T, q), (q, z.T)),
        format="csr",
    )

    # Static Lorentzian action Hessian.
    lorentzian = h**3 * sp.bmat(
        (
            (p, upper),
            (lower, -b),
        ),
        format="csr",
    )

    # Flip only the magnetic E-L equations.
    # Correct R3X1 structure has skew cross blocks.
    positive_k = h**3 * sp.bmat(
        (
            (p, upper),
            (-lower, b),
        ),
        format="csr",
    )

    return lorentzian, positive_k, m


def maxabs(matrix):
    if not matrix.nnz:
        return 0.0

    return float(
        np.max(np.abs(matrix.data))
    )


def field_action(x, grad, curl, theta, h):
    """Evaluate the action independently of the Hessian."""
    n = grad.shape[1]
    a = 3 * n

    ex = -(grad @ x[:n])
    ey = -(grad @ x[n:2*n])

    bx = curl @ x[2*n:2*n+a]
    by = curl @ x[2*n+a:2*n+2*a]

    t3 = np.tile(theta, 3)

    return h**3 * (
        0.5 * (
            ex @ ex
            + ey @ ey
            - bx @ bx
            - by @ by
        )
        + (t3 * ex) @ by
        + (t3 * ey) @ bx
    )


def run(n: int = 7, h: float = 1.0) -> dict:
    grad, curl = complex_3d(n, h)
    nsites = n**3

    rng = np.random.default_rng(1501)

    coord = np.arange(n) * 2*np.pi / n

    x, y, z = np.meshgrid(
        coord,
        coord,
        coord,
        indexing="ij",
    )

    # Synthetic nonuniform interface surrogate.
    # NOT the R3B 1 kg payload density or theta.
    theta = (
        0.10
        + 0.04 * np.cos(x)
        + 0.023 * np.sin(y + z)
    ).ravel()

    hessian, positive_k, mixed = hessians(
        grad, curl, theta, h
    )

    _, _, constant_mixed = hessians(
        grad,
        curl,
        np.full(nsites, 0.17),
        h,
    )

    nn = 8 * nsites
    gauge = rng.normal(size=nsites)

    # Two independent U(1) gauge transformations.
    gauge_x = np.r_[
        np.zeros(2*nsites),
        grad @ gauge,
        np.zeros(3*nsites),
    ]

    gauge_y = np.r_[
        np.zeros(5*nsites),
        grad @ gauge,
    ]

    shift_x = np.r_[
        np.ones(nsites),
        np.zeros(nn-nsites),
    ]

    shift_y = np.r_[
        np.zeros(nsites),
        np.ones(nsites),
        np.zeros(nn-2*nsites),
    ]

    # Algebraically conserved mathematical sources.
    # Physical external support is NOT yet constructed.
    conserved = curl @ rng.normal(
        size=3*nsites
    )

    charge = grad.T @ rng.normal(
        size=3*nsites
    )

    test_x = rng.normal(size=nn)
    direction = rng.normal(size=nn)

    eps = 1e-5

    derivative_numeric = (
        field_action(
            test_x + eps*direction,
            grad, curl, theta, h
        )
        - field_action(
            test_x - eps*direction,
            grad, curl, theta, h
        )
    ) / (2*eps)

    derivative_exact = float(
        direction @ (hessian @ test_x)
    )

    edofs = 2 * nsites

    residuals = {
        "curl_grad": maxabs(curl @ grad),
        "div_curl": maxabs(grad.T @ curl),

        "lorentzian_action_reciprocity":
            maxabs(hessian - hessian.T),

        "positive_k_cross_skew":
            maxabs(
                positive_k[:edofs, edofs:]
                + positive_k[edofs:, :edofs].T
            ),

        "constant_theta_topological_null":
            maxabs(constant_mixed),

        "independent_U1_X_gauge":
            float(np.max(np.abs(
                hessian @ gauge_x
            ))),

        "independent_U1_Y_gauge":
            float(np.max(np.abs(
                hessian @ gauge_y
            ))),

        "constant_phi_X_shift":
            float(np.max(np.abs(
                hessian @ shift_x
            ))),

        "constant_phi_Y_shift":
            float(np.max(np.abs(
                hessian @ shift_y
            ))),

        "conserved_source_current_divergence":
            float(np.max(np.abs(
                grad.T @ conserved
            ))),

        "net_source_charge":
            float(abs(np.sum(charge))),

        "independent_action_derivative_relative":
            float(
                abs(
                    derivative_numeric
                    - derivative_exact
                )
                / max(
                    1.0,
                    abs(derivative_exact),
                )
            ),
    }

    scale = max(
        1.0,
        maxabs(hessian),
        maxabs(positive_k),
    )

    identity_error = max(
        value / scale
        for key, value in residuals.items()
        if key
        != "independent_action_derivative_relative"
    )

    passed = (
        identity_error < 1e-10
        and residuals[
            "independent_action_derivative_relative"
        ] < 1e-8
        and maxabs(mixed) > 1e-5
    )

    return {
        "branch": BRANCH,
        "scope":
            "PERIODIC_3D_STATIC_TWO_U1_FROZEN_THETA_ACTION_IDENTITY_ONLY",
        "grid_n": n,
        "grid_step_arbitrary_units": h,
        "frozen_theta_is_synthetic": True,
        "full_r3b_density_or_source_geometry_loaded": False,
        "numerical_residuals": residuals,
        "max_relative_identity_residual": identity_error,
        "nonconstant_theta_mixed_coupling_present":
            bool(maxabs(mixed) > 1e-5),
        "exact_gauge_reciprocity_gate_pass": bool(passed),

        "same_action_full_matter_dynamics_verified": False,
        "dynamic_health_checked": False,
        "source_support_1m_certified": False,
        "physical_current_micro_source_certified": False,
        "loaded_3d_solution": False,
        "loaded_1g": False,
        "field_energy_j": None,
        "complete_operating_energy_certified": False,

        "reference_r3b_preloaded_energy_j_preserved":
            1.5429162116460216,
        "006d_replaced": False,

        "next":
            "BOUNDARY_MIMETIC_3D_TOROIDAL_SOURCE_CALIBRATED_LOADED_AXISYMMETRIC_REPRODUCTION",
    }


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--n",
        type=int,
        default=7,
    )

    parser.add_argument(
        "--h",
        type=float,
        default=1.0,
    )

    args = parser.parse_args()

    result = run(
        args.n,
        args.h,
    )

    output = (
        Path(__file__).resolve().parents[1]
        / "results"
        / "data"
        / f"032h17a12d1r3x3b15_m1_identity_n{args.n}_summary.json"
    )

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output.write_text(
        json.dumps(
            result,
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )

    print(
        "B15_M1_EXACT_GAUGE_RECIPROCITY_PASS=",
        result["exact_gauge_reciprocity_gate_pass"],
    )

    for key, value in result[
        "numerical_residuals"
    ].items():
        print(f"{key}: {value:.4e}")

    print("3D_LOADED_SOLUTION=NO")
    print("RESULT=", output)

    if not result[
        "exact_gauge_reciprocity_gate_pass"
    ]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
