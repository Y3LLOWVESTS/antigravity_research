"""GAMMA1-00R3: single-mesh PH16 profile replay and M0 action gate.

No gravity PDE or source-to-Earth force is claimed.
The historical PH16 producing source is never modified.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import sympy as sp

PH16_SHA = (
    'b5468671f6418fad7b6ed01d916ea65a95a1d59252b84d4411beed9709f86df0'
)


def sha(path):
    path = Path(path)
    return (
        hashlib.sha256(path.read_bytes()).hexdigest()
        if path.is_file() else 'MISSING'
    )


def algebra():
    """Exact restricted variations; not a full covariant E-L proof."""
    a, b, p, q, u, z = sp.symbols(
        'alpha beta P Q U z',
        real=True
    )

    v = sp.symbols('v', positive=True)

    sigma = a*p-b*p**2
    derivative = sp.diff(sigma, p)

    e2 = sp.exp(2*sigma)
    e4 = sp.exp(4*sigma)

    base = e2*q/2+e4*u
    lam = -sp.diff(base, p)

    trace = e2*q-4*(base+lam*p)

    # Four-dimensional conformal transformation:
    # g_cov -> exp(2z) g_cov
    # Q -> exp(-2z) Q
    # sqrt(-g) -> exp(4z) sqrt(-g)
    # P -> exp(-4z) P at fixed covariant F.

    Pz = p*sp.exp(-4*z)
    sigz = a*Pz-b*Pz**2

    lagz = -v*sp.exp(4*z)*(
        sp.exp(2*sigz)*q*sp.exp(-2*z)/2
        +sp.exp(4*sigz)*u
    )

    F, charge = sp.symbols(
        'F charge',
        real=True
    )

    omega, ax = sp.symbols(
        'omega AX',
        real=True
    )

    current = (
        2*e2*(omega-charge*ax)*F**2
    )

    reduced = (
        -e2*(omega-charge*ax)**2*F**2
    )

    n, mass, kappa, C = sp.symbols(
        'n mass kappa C',
        real=True,
        positive=True
    )

    n_hydro = (
        C*sp.exp(-sigma)-mass
    )/kappa

    tests = {
        'sigma_prime':
            sp.simplify(
                derivative-(a-2*b*p)
            ) == 0,

        'portal_lambda':
            sp.simplify(
                lam+(e2*q+4*e4*u)*derivative
            ) == 0,

        'off_shell_metric_trace_scaling':
            sp.simplify(
                sp.diff(lagz, z).subs(z, 0)
                -v*trace
            ) == 0,

        'P_hodge_weight':
            sp.simplify(
                sp.diff(Pz, z).subs(z, 0)
                +4*p
            ) == 0,

        'source_X_current':
            sp.simplify(
                sp.diff(reduced, ax)
                -charge*current
            ) == 0,

        'neutral_hydrostatic_constant_mu':
            sp.simplify(
                (mass+kappa*n_hydro)
                *sp.exp(sigma)-C
            ) == 0,

        'coupling_off':
            sigma.subs({
                a: 0,
                b: 0
            }) == 0,

        'source_off_P_zero':
            sigma.subs(p, 0) == 0,

        'mixed_variations_reciprocal':
            sp.simplify(
                sp.diff(reduced, ax, p)
                -sp.diff(reduced, p, ax)
            ) == 0,
    }

    if not all(tests.values()):
        raise AssertionError(tests)

    return {
        key: bool(value)
        for key, value in tests.items()
    }


def validate_native_profile(
    obj,
    xf,
    recorded,
    solver_meta
):
    """Evaluate an unchanged PH16 solver state against historical data."""
    import numpy as np

    from antigravity_research.ph16.ph16_04_joint_stationary import (
        hydro_profile
    )

    R, grad, d = obj.evaluate(xf, True)

    # Important: evaluate(..., True) returns physical diagnostics.
    # Native root_success and continuation records are returned by
    # solve(), not by evaluate().
    d.update(solver_meta)

    F, AX, AY = obj.unpack(xf)

    m = obj.m
    settings = obj.s
    N = obj.N

    if (
        F.shape != (2, N)
        or AX.shape != (N,)
        or AY.shape != (N,)
    ):
        raise RuntimeError(
            'NATIVE_PROFILE_SHAPE_ERROR'
        )

    arrays_to_check = [
        F,
        AX,
        AY,
        m.w,
        m.rho,
        m.z,
        grad,
    ]

    if any(
        not np.all(np.isfinite(x))
        for x in arrays_to_check
    ):
        raise RuntimeError(
            'NONFINITE_NATIVE_PROFILE'
        )

    residual = float(
        np.linalg.norm(grad)
    )

    if (
        not d['root_success']
        or residual >= 1.e-6
    ):
        raise RuntimeError(
            'PH16_NATIVE_REPLAY_NOT_STATIONARY'
        )

    historical_residual = float(
        recorded['final_residual_L2']
    )

    if abs(
        residual-historical_residual
    ) > 1.e-7:
        raise RuntimeError(
            'REPLAY_RESIDUAL_NOT_MATCHED_TO_HISTORICAL'
        )

    comparison_fields = (
        'Y_norm',
        'Pmax',
        'sigma_max',
        'Routhian_NOT_J',
        'frozen_magnetic_margin_min',
    )

    for key in comparison_fields:
        old = float(recorded[key])
        new = float(d[key])

        if abs(new-old) > max(
            2.e-4,
            2.e-4*abs(old)
        ):
            raise RuntimeError(
                'REPLAY_DIAGNOSTIC_MISMATCH '
                +key+' '+str((old, new))
            )

    for new, old in zip(
        d['N'],
        recorded['N']
    ):
        if abs(float(new)-float(old)) >= 1.e-8:
            raise RuntimeError(
                'REPLAY_NOETHER_MISMATCH'
            )

    if (
        d['frozen_magnetic_margin_min'] <= 0
        or d['frozen_negative_cells'] != 0
    ):
        raise RuntimeError(
            'FROZEN_MAGNETIC_SCREEN_INVALID'
        )

    Er = np.asarray(-obj.Dr@AX)
    Ez = np.asarray(-obj.Dz@AX)

    Br = np.asarray(obj.BR@AY)
    Bz = np.asarray(obj.BZ@AY)

    P = Er*Br+Ez*Bz

    sigma = (
        settings.alpha*P
        -settings.beta*P*P
    )

    n, C = hydro_profile(
        sigma.reshape(m.nr, m.nz),
        m.w.reshape(m.nr, m.nz),
        settings.mass,
        settings.kappa,
        settings.n0
    )

    if not np.isclose(
        np.max(np.abs(P)),
        d['Pmax'],
        rtol=1.e-9,
        atol=1.e-12
    ):
        raise RuntimeError(
            'INDEPENDENT_FIELD_P_MISMATCH'
        )

    if not np.isclose(
        np.min(n),
        d['min_n'],
        rtol=1.e-9,
        atol=1.e-12
    ):
        raise RuntimeError(
            'INDEPENDENT_NEUTRAL_MISMATCH'
        )

    native = {
        'F_plus':
            np.asarray(F[0], dtype='<f8'),

        'F_minus':
            np.asarray(F[1], dtype='<f8'),

        'A_X':
            np.asarray(AX, dtype='<f8'),

        'A_Y':
            np.asarray(AY, dtype='<f8'),

        'rho':
            np.asarray(m.rho, dtype='<f8'),

        'z':
            np.asarray(m.z, dtype='<f8'),

        'weights':
            np.asarray(m.w, dtype='<f8'),

        'E_X_r':
            np.asarray(Er, dtype='<f8'),

        'E_X_z':
            np.asarray(Ez, dtype='<f8'),

        'B_Y_r':
            np.asarray(Br, dtype='<f8'),

        'B_Y_z':
            np.asarray(Bz, dtype='<f8'),

        'P':
            np.asarray(P, dtype='<f8'),

        'sigma':
            np.asarray(sigma, dtype='<f8'),

        'neutral_n':
            np.asarray(n.ravel(), dtype='<f8'),

        'joint_gradient':
            np.asarray(grad, dtype='<f8'),
    }

    diagnostics = {
        'joint_residual_L2':
            residual,

        'recorded_joint_residual_L2':
            historical_residual,

        'root_success':
            bool(d['root_success']),

        'Noether_N': [
            float(value)
            for value in d['N']
        ],

        'frozen_magnetic_margin_min':
            float(
                d['frozen_magnetic_margin_min']
            ),

        'frozen_negative_cells':
            int(
                d['frozen_negative_cells']
            ),

        'Pmax':
            float(np.max(np.abs(P))),

        'Y_norm':
            float(np.linalg.norm(AY)),

        'Routhian_NOT_J':
            float(R),

        'mesh': {
            'nr': int(m.nr),
            'nz': int(m.nz),
            'L': float(settings.L),
            'h': float(m.h),
            'cells': int(N),
        },

        'neutral_mu_constant':
            float(C),
    }

    return {
        'arrays': native,
        'diagnostics': diagnostics,
    }
