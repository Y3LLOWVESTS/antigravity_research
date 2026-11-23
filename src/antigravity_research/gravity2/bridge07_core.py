"""GRAVITY2-07: two-dimensional Hodge/Bianchi-consistent nonlinear Y solver.

Geometry:
  A_X = a(x,z) dt
  A_Y = b(x,z) dy
  P = a_x*b_z-a_z*b_x = E_X dot B_Y

The periodic (x,z) domain is a mathematical field-response test, NOT a
finite exterior spacecraft or source. Scalar f and X potential a remain
prescribed. Only Y potential b is solved from its own reduced action.
"""
from __future__ import annotations

import numpy as np

GRIDS = (9, 15, 23, 31)
ALPHA, BETA = .08, .005
Q, OMEGA, M2, LAMBDA = .4, 1.25, .8, .4
TOL = 1e-10


def dx(v, h):
    return (
        np.roll(v, -1, axis=0)
        - np.roll(v, 1, axis=0)
    ) / (2*h)


def dz(v, h):
    return (
        np.roll(v, -1, axis=1)
        - np.roll(v, 1, axis=1)
    ) / (2*h)


def lap(v, h):
    return dx(dx(v, h), h) + dz(dz(v, h), h)


def prescribed_background(n):
    # Odd N avoids spurious checkerboard null directions
    # of the periodic central-difference Laplacian.
    if n < 7 or n % 2 != 1:
        raise ValueError("odd N >= 7 required")

    h = 2*np.pi/n
    x = np.arange(n, dtype=float)*h
    X, Z = np.meshgrid(x, x, indexing="ij")

    a = .22 * (
        np.cos(X)
        + .31*np.cos(X+2*Z)
        + .12*np.sin(2*X-Z)
    )

    f = (
        .9
        + .2*np.cos(Z+.3*np.sin(X))
        + .09*np.sin(2*X+Z)
    )

    assert f.min() > 0

    return h, a, f


def source_parts(
    b, a, f, h,
    alpha=ALPHA,
    beta=BETA,
):
    ax, az = dx(a, h), dz(a, h)
    bx, bz = dx(b, h), dz(b, h)

    P = ax*bz-az*bx
    sigma = alpha*P-beta*P*P

    w = np.exp(2*sigma)
    z = np.exp(4*sigma)

    K = (
        (OMEGA-Q*a)**2*f*f
        - dx(f, h)**2
        - dz(f, h)**2
    )

    V = .5*M2*f*f+.25*LAMBDA*f**4

    Pi = (
        w*K-4*z*V
    ) * (alpha-2*beta*P)

    return P, Pi, K, V


def portal_force(
    b, a, f, h,
    alpha=ALPHA,
    beta=BETA,
):
    _, Pi, _, _ = source_parts(
        b, a, f, h, alpha, beta
    )

    return (
        dx(Pi*dz(a, h), h)
        - dz(Pi*dx(a, h), h)
    )


def magnetic_laplacian_inverse(source, h):
    n = source.shape[0]

    if source.shape != (n, n) or n % 2 != 1:
        raise ValueError("odd square grid required")

    k = np.fft.fftfreq(n)*n
    eig = (
        np.sin(2*np.pi*k/n)/h
    )**2

    denominator = eig[:, None]+eig[None, :]

    value = np.fft.fft2(source)
    value[0, 0] = 0

    result = np.zeros_like(value)

    np.divide(
        value,
        denominator,
        out=result,
        where=denominator > 1e-14,
    )

    return np.fft.ifft2(result).real


def action(
    b, a, f, h,
    alpha=ALPHA,
    beta=BETA,
):
    P, _, K, V = source_parts(
        b, a, f, h, alpha, beta
    )

    sigma = alpha*P-beta*P*P

    magnetic = -.5 * (
        dx(b, h)**2
        + dz(b, h)**2
    )

    jordan_source = (
        .5*np.exp(2*sigma)*K
        - np.exp(4*sigma)*V
    )

    return float(
        h*h*np.sum(magnetic+jordan_source)
    )


def residual(
    b, a, f, h,
    alpha=ALPHA,
    beta=BETA,
):
    return (
        -lap(b, h)
        -portal_force(b, a, f, h, alpha, beta)
    )


def solve(
    n,
    alpha=ALPHA,
    beta=BETA,
):
    h, a, f = prescribed_background(n)

    b = np.zeros_like(a)

    for iteration in range(201):
        source = portal_force(
            b, a, f, h, alpha, beta
        )

        err = float(
            np.linalg.norm(
                residual(
                    b, a, f, h, alpha, beta
                )
            )
            / max(
                float(np.linalg.norm(source)),
                1.0,
            )
        )

        if not np.isfinite(err):
            raise RuntimeError(
                "nonfinite nonlinear residual"
            )

        if err < TOL:
            break

        if iteration >= 200:
            raise RuntimeError(
                "bounded nonlinear Y solver failed"
            )

        proposal = magnetic_laplacian_inverse(
            source, h
        )

        b = .5*b+.5*proposal
        b -= b.mean()

    # B_Y=(-partial_z b,0,partial_x b).
    # The magnetic Bianchi divergence must vanish.
    bianchi = (
        dx(-dz(b, h), h)
        +dz(dx(b, h), h)
    )

    energy_density = .5*float(
        np.mean(
            dx(b, h)**2
            +dz(b, h)**2
        )
    )

    report = {
        "n": n,
        "h_canonical": float(h),
        "iterations": iteration,
        "equation_residual_relative": err,
        "bianchi_max_abs":
            float(np.max(abs(bianchi))),
        "y_field_max_abs":
            float(np.max(abs(b))),
        "magnetic_gradient_energy_density_canonical":
            energy_density,
        "mean_b": float(np.mean(b)),
        "off_shell_action_canonical":
            action(
                b, a, f, h, alpha, beta
            ),
        "status":
            "PASS_SCOPED_2D_Y_EULER_ONLY",
    }

    assert err < 1e-10
    assert report["bianchi_max_abs"] < 1e-12

    return report, {
        "a": a,
        "f": f,
        "b": b,
    }


def scientific_run():
    rows = []
    archive = {}

    for n in GRIDS:
        report, fields = solve(n)

        rows.append(report)

        archive.update({
            f"{key}_{n}": value
            for key, value in fields.items()
        })

    # Portal-off control must give no induced Y field.
    off, _ = solve(
        15,
        alpha=0,
        beta=0,
    )

    assert off["y_field_max_abs"] == 0

    assert all(
        row["y_field_max_abs"] > 1e-5
        for row in rows
    )

    h, a, f = prescribed_background(15)

    # Collinear one-dimensional fields cannot support
    # the tested transverse portal source.
    a_col = np.broadcast_to(
        a[:, 0, None], a.shape
    ).copy()

    f_col = np.broadcast_to(
        f[:, 0, None], f.shape
    ).copy()

    zero = portal_force(
        np.zeros_like(a),
        a_col,
        f_col,
        h,
    )

    assert np.max(abs(zero)) < 1e-12

    # A constant coefficient of F_X wedge F_Y
    # is a boundary/topological contribution.
    Pi_const = np.full_like(a, .7)

    topological = (
        dx(Pi_const*dz(a, h), h)
        -dz(Pi_const*dx(a, h), h)
    )

    assert np.max(abs(topological)) < 1e-12

    return {
        "decision":
            "2D_HODGE_VALID_NONLINEAR_Y_RESPONSE; "
            "FROZEN_SOURCE_AND_X_NOT_PHYSICALIZED",
        "geometry":
            "2D_PERIODIC_FLAT_XZ_PATCH_NOT_FINITE_EXTERIOR",
        "potentials":
            "A_X=a(x,z)dt; A_Y=b(x,z)dy",
        "P":
            "a_x*b_z-a_z*b_x = E_X dot B_Y "
            "with chosen orientation",
        "source":
            "f(x,z) and a(x,z) PRESCRIBED; NOT ON SHELL",
        "L":
            "1/2|grad a|^2-1/2|grad b|^2"
            "+1/2 exp(2sigma)K-exp(4sigma)V",
        "Y_euler":
            "Delta b+Dx(Pi*Dz a)-Dz(Pi*Dx a)=0",
        "Pi":
            "(exp(2sigma)*K-4*exp(4sigma)*V)*sigma_P",
        "n_y_solved": True,
        "x_and_source_solved": False,
        "full_mode_stability": "NOT_DERIVED",
        "convergence":
            "FOUR_RESOLUTION_SENSITIVITY_ONLY_"
            "NOT_CONTINUUM_PROOF",
        "rows": rows,
        "controls": {
            "no_portal_zero_Y_max":
                off["y_field_max_abs"],
            "collinear_1D_zero_source_max":
                float(np.max(abs(zero))),
            "constant_Pi_topological_source_max":
                float(np.max(abs(topological))),
        },
        "parent_history": {
            "R3B_prescribed_capacity_J":
                1.5429162116460216,
            "R3B_loaded_min_m_s2":
                -129.67185782242464,
            "R3B_history_recomputed": False,
        },
        "physical_survivors": 0,
        "real_finite_supported_source":
            "NOT_ESTABLISHED",
        "loaded_neutral_force": "NOT_COMPUTED",
        "complete_Einstein_action": "NOT_DERIVED",
        "whole_craft_lift": "NOT_DERIVED",
        "SI_complete_energy": "NOT_CERTIFIED",
        "L2_authorized": False,
    }, archive
