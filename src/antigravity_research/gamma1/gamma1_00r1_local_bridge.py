"""GAMMA1-00R1: scoped local one-action stress/constitutive and sign preflight.

This is a four-dimensional diagonal-metric local evaluation of hypothetical
canonical scalar participants, Maxwell X/Y, and a universal physical metric.
No participant profile is an on-shell finite source, Earth model or spacecraft.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
import math
import sympy as sp


@dataclass(frozen=True)
class Sector:
    name: str
    k: tuple[float, float, float, float]
    potential: float


@dataclass(frozen=True)
class Trial:
    metric: tuple[float, float, float, float]
    fields: tuple[float, float, float, float]
    alpha: float
    beta: float
    sectors: tuple[Sector, ...]


def trials() -> dict[str, Trial]:
    basic = (
        Sector('source', (.31, .12, .06, 0.), .13),
        Sector('neutral', (0., .08, 0., .02), .10),
        Sector('Earth', (0., 0., .15, 0.), .18),
        Sector('supports', (0., .06, 0., .04), .09),
    )
    return {
        'nontrivial_isotropic': Trial(
            (1., 1., 1., 1.),
            (.14, .2, -.04, .08), .05, 40., basic
        ),
        'nontrivial_anisotropic': Trial(
            (1.2, .9, 1.1, .8),
            (.04, -.06, .08, .05), .1, .5, basic
        ),
        'coupling_off': Trial(
            (1.2, .9, 1.1, .8),
            (.04, -.06, .08, .05), 0., 0., basic
        ),
        'both_carriers_off': Trial(
            (1., 1., 1., 1.),
            (0., 0., 0., 0.), .05, 40., basic
        ),
        'negative_kinetic_offshell': Trial(
            (1., 1., 1., 1.),
            (0., .2, 0., 0.), .05, 40.,
            (
                Sector('source', (2., 0., 0., 0.), .2),
                Sector('neutral', (0., 0., 0., 0.), 0.),
                Sector('Earth', (0., 0., 0., 0.), 0.),
                Sector('supports', (0., 0., 0., 0.), 0.),
            )
        ),
    }


def evaluate(trial: Trial) -> dict:
    t, a, b, c = trial.metric
    ex, bx, ey, by = trial.fields

    if min(trial.metric) <= 0 or not all(
        map(
            math.isfinite,
            trial.metric + trial.fields
            + (trial.alpha, trial.beta)
        )
    ):
        raise ValueError(
            'finite Lorentzian diagonal metric and fields required'
        )

    required = {'source', 'neutral', 'Earth', 'supports'}
    names = {s.name for s in trial.sectors}

    if len(names) != 4 or names != required:
        raise ValueError(
            'the four required participants must be distinct'
        )

    if any(
        s.potential < 0
        or not math.isfinite(s.potential)
        or len(s.k) != 4
        or not all(map(math.isfinite, s.k))
        for s in trial.sectors
    ):
        raise ValueError(
            'invalid scalar trial participant'
        )

    v = math.sqrt(t*a*b*c)
    inv = (-1/t, 1/a, 1/b, 1/c)
    cov = (-t, a, b, c)

    p = (ex*by + bx*ey)/v

    sigma = trial.alpha*p - trial.beta*p*p
    sp1 = trial.alpha - 2*trial.beta*p
    sp2 = -2*trial.beta

    e2 = math.exp(2*sigma)
    e4 = e2*e2

    grad2 = [
        sum(s.k[i]**2 for s in trial.sectors)
        for i in range(4)
    ]

    q = sum(
        inv[i]*grad2[i]
        for i in range(4)
    )

    u = sum(
        s.potential for s in trial.sectors
    )

    lam = -(e2*q + 4*e4*u)*sp1

    chi = (
        -(2*e2*q + 16*e4*u)*sp1**2
        -(e2*q + 4*e4*u)*sp2
    )

    matter_base = .5*e2*q + e4*u
    matter_density = -v*matter_base

    em_density = .5*v*(
        (ex*ex + ey*ey)/(t*a)
        -(bx*bx + by*by)/(b*c)
    )

    # Einstein-frame matter stress:
    # metric variation at fixed F and fixed scalar gradients.
    matter_stress = tuple(
        e2*grad2[i]
        -cov[i]*(matter_base + lam*p)
        for i in range(4)
    )

    # Magnetic fields held fixed.
    # This is a local electric kinetic sub-block,
    # NOT the complete constrained dynamical Hessian.
    base = v/(t*a)
    shift = chi/v

    h00 = base + shift*by*by
    h11 = base + shift*bx*bx
    h01 = shift*bx*by

    discriminant = math.sqrt(
        (h00-h11)**2 + 4*h01*h01
    )

    eigmin = .5*(h00+h11-discriminant)
    eigmax = .5*(h00+h11+discriminant)

    return {
        'volume': v,
        'P': p,
        'sigma': sigma,
        'lambda': lam,
        'chi_dlambda_dP': chi,
        'Q_scalar': q,
        'potential_sum': u,
        'matter_density': matter_density,
        'maxwell_density': em_density,
        'total_density': matter_density+em_density,
        'T_matter_diag': matter_stress,
        'local_active_matter_S': sum(matter_stress),

        'field_density_derivatives': (
            v*ex/(t*a)+lam*by,
            -v*bx/(b*c)+lam*ey,
            v*ey/(t*a)+lam*bx,
            -v*by/(b*c)+lam*ex,
        ),

        'electric_kinetic_H': (
            (h00, h01),
            (h01, h11)
        ),

        'electric_kinetic_min_eigen': eigmin,
        'electric_kinetic_max_eigen': eigmax,
    }


def _change_metric(
    trial: Trial,
    i: int,
    value: float
) -> Trial:
    m = list(trial.metric)
    m[i] = value
    return replace(trial, metric=tuple(m))


def _change_field(
    trial: Trial,
    i: int,
    value: float
) -> Trial:
    f = list(trial.fields)
    f[i] = value
    return replace(trial, fields=tuple(f))


def _fd(fn, x: float, h: float) -> float:
    return (fn(x+h)-fn(x-h))/(2*h)


def derivative_audit(
    trial: Trial,
    step: float = 1.e-5
) -> dict:
    """Finite differences of the action density."""
    e = evaluate(trial)
    m = trial.metric
    errors = {}

    for i in range(4):
        h = step*max(1., abs(m[i]))

        # dg^00/dt=+1/t^2
        # dg^ii/dm_i=-1/m_i^2
        sign = 1 if i == 0 else -1

        derivative = _fd(
            lambda value: evaluate(
                _change_metric(trial, i, value)
            )['matter_density'],
            m[i], h
        )

        predicted_stress = (
            -2*sign*m[i]**2
            /e['volume']*derivative
        )

        expected = e['T_matter_diag'][i]

        errors[f'metric_{i}'] = (
            abs(expected-predicted_stress)
            /max(1., abs(expected))
        )

    for i in range(4):
        x = trial.fields[i]
        h = step*max(1., abs(x))

        derivative = _fd(
            lambda value: evaluate(
                _change_field(trial, i, value)
            )['total_density'],
            x, h
        )

        expected = e['field_density_derivatives'][i]

        errors[f'field_{i}'] = (
            abs(expected-derivative)
            /max(1., abs(expected))
        )

    return {
        'relative_errors': errors,
        'max_relative_error': max(errors.values())
    }


def exact_identities() -> dict[str, bool]:
    p, alpha, beta, v, j, u = sp.symbols(
        'p alpha beta v j u',
        real=True,
        nonzero=True
    )
    bx, by, chi, base = sp.symbols(
        'bx by chi base', real=True
    )
    x, y = sp.symbols('x y', real=True)

    sig = alpha*p-beta*p**2
    sigp = sp.diff(sig, p)
    w = (j/v)*sp.exp(-4*u)

    c0 = base+chi*by**2/v
    c1 = base+chi*bx**2/v
    c01 = chi*bx*by/v

    determinant = sp.expand(
        c0*c1-c01**2
    )

    expected = base*(
        base+chi*(bx*bx+by*by)/v
    )

    S = sp.Function('S')(x)

    checks = {
        'sqrtg_P_metric_independent':
            sp.simplify(
                sp.diff(
                    v*sp.exp(4*u)*w, u
                )
            ) == 0,

        'P_conformal_weight_negative_four':
            sp.simplify(
                sp.diff(w, u)+4*w
            ) == 0,

        'P_metric_inverse_trace_variation':
            sp.simplify(
                sp.diff(w, u)-(-4*w)
            ) == 0,

        'mixed_sigma_second_derivative':
            sp.diff(sig, p, 2) == -2*beta,

        'lambda_chain':
            sp.simplify(
                sigp-alpha+2*beta*p
            ) == 0,

        'rank_one_electric_determinant':
            sp.simplify(
                determinant-expected
            ) == 0,

        'constant_lambda_induction_zero':
            sp.diff(
                sp.Symbol('lambda0'), x
            ) == 0,

        'opposite_dipole_orientation_flips_P':
            sp.simplify(
                sig.subs(p, -p)
                -sig.subs(p, p)
                +2*alpha*p
            ) == 0,

        'four_dim_trace_stress_chain':
            sp.simplify(
                (1-4*p*sigp)
                -(1-4*alpha*p+8*beta*p*p)
            ) == 0,

        'source_off_zero_sigma':
            sig.subs(p, 0) == 0,

        'coupling_off_zero_sigma':
            sig.subs({
                alpha: 0,
                beta: 0
            }) == 0,

        'off_shell_scalar_translation':
            sp.diff(S, x)-sp.diff(S, x) == 0,
    }

    return {
        k: bool(val)
        for k, val in checks.items()
    }


def farfield(
    alpha=.05,
    beta=40.,
    d=1.e-3,
    r=2.
) -> dict:
    """Prescribed axial dipoles; not a coupled Maxwell source."""
    if (
        not all(map(math.isfinite, (alpha, beta, d, r)))
        or r <= 0
    ):
        raise ValueError(
            'invalid dipole assumptions'
        )

    P = 4*d/r**6
    sigma = alpha*P-beta*P*P

    acceleration = (
        24*alpha*d/r**7
        -192*beta*d*d/r**13
    )

    sign = (
        'OUTWARD' if acceleration > 0
        else 'INWARD' if acceleration < 0
        else 'ZERO'
    )

    return {
        'P': P,
        'sigma': sigma,
        'outward_portal_a_over_c2': acceleration,
        'scale': 'arbitrary dipole units, not m/s^2',
        'sign': sign,
    }


def atlas() -> dict:
    checks = exact_identities()

    if not all(checks.values()):
        raise AssertionError(checks)

    audit = {}

    for name, trial in trials().items():
        computed = evaluate(trial)
        numerical = derivative_audit(trial)

        if numerical['max_relative_error'] >= 5.e-7:
            raise AssertionError(
                (name, numerical)
            )

        audit[name] = {
            'max_relative_error':
                numerical['max_relative_error'],

            'T_matter_diag':
                computed['T_matter_diag'],

            'local_active_matter_S':
                computed['local_active_matter_S'],

            'electric_kinetic_min_eigen':
                computed['electric_kinetic_min_eigen'],

            'P': computed['P'],
        }

    if audit['negative_kinetic_offshell'][
        'electric_kinetic_min_eigen'
    ] >= 0:
        raise AssertionError(
            'negative off-shell trial disappeared'
        )

    if audit['nontrivial_isotropic'][
        'electric_kinetic_min_eigen'
    ] <= 0:
        raise AssertionError(
            'positive off-shell control disappeared'
        )

    plus = farfield(d=1.e-3)
    minus = farfield(d=-1.e-3)

    if (
        plus['sign'] != 'OUTWARD'
        or minus['sign'] != 'INWARD'
    ):
        raise AssertionError(
            'conditional dipole polarity control failed'
        )

    return {
        'experiment':
            'GAMMA1-00R1_OFFSHELL_LOCAL_METRIC_BRIDGE_PREFLIGHT',

        'fidelity':
            'L0_EXACT_IDENTITIES_L1_LOCAL_FD_NO_PDE',

        'exact_algebra': checks,

        'local_one_action_metric_field_variations':
            audit,

        'dipole_exterior_trials': {
            'aligned': plus,
            'antialigned': minus,
        },

        'theorems': {
            'metric_hodge_density':
                'METRIC_INDEPENDENT_AT_FIXED_F',

            'universal_participant_stress':
                'DERIVED_FOR_LOCAL_CANONICAL_SCALAR_TRIALS',

            'constitutive':
                'DERIVED_FOR_SAME_TRIAL_ACTION',

            'local_electric_rank_one_hessian':
                'DERIVED_AT_FIXED_SCALARS_MAGNETIC_METRIC',

            'beta40_health':
                'NOT_UNIFORMLY_POSITIVE_ON_OFFSHELL_TRIALS',

            'beta40_PH16_actual_mode_health':
                'NOT_DETERMINED',

            'dipole_sign':
                'NOT_SOURCE_INDEPENDENT',

            'dipole_multipole_assumption':
                'P~r^-6, a_sigma~r^-7 only if both fields dipolar',

            'full_offshell_Ward_Noether':
                'OPEN_REQUIRES_REAL_SOURCE_EOM',

            'full_gravitational_boundary':
                'OPEN',

            'Einstein_metric_solution':
                'NOT_SOLVED',

            'Earth_down_and_whole_craft_up':
                'NOT_DERIVED',

            'physical_1kg_1g_1m':
                'NOT_CERTIFIED',

            'complete_SI_energy':
                'NOT_CERTIFIED',

            'M2_full_health':
                'NOT_TESTED',
        },

        'M0_go': 'NOT_QUALIFIED',

        'M1_go':
            'CONDITIONAL_STATIC_DEC_BUDGET_OBSTRUCTION_RETAINED',

        'M2_go':
            'UNQUALIFIED_PENDING_INDEPENDENT_OPERATOR_THEORY',

        'M3_go': 'RESERVED',

        'qualified_survivors': [],
        'GAMMA1_01_authorized': False,
        'PH16_05_authorized': False,
        'PH17_authorized': False,
        '006D_replaced': False,

        'classification':
            'SCOPED_LOCAL_VARIATION_AND_SIGN_ATLAS',

        'decision':
            'STOP_NUMERICAL_ESCALATION_REQUIRES_PHYSICAL_DERIVATION',
    }
