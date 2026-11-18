"""GAMMA1-00: an L0 algebra/conditional-SI gravity-bridge atlas.

Signature (-+++). P=1/2 F_X *F_Y. Common physical metric
   g_tilde=exp(2 sigma(P)) g,  sigma=alpha*P-beta*P**2.

All source, neutral, Earth, and support actions must share this metric.
Only algebraic implications are checked; their microscopic actions,
Einstein solution, boundary forces and full constrained modes remain open.

M1 bound requires all stress energy, INCLUDING exterior field stress,
to be at least h from a target. Material stand-off alone is insufficient.

No test establishes a real source, true exterior or whole-spacecraft lift.
"""
from __future__ import annotations

import math
import sympy as sp

G = 6.67430e-11
C = 299792458.0
A = 9.80665
H = 1.0
BUDGET = 10_000_000.0
C006D = 23.591586299249


def identities():
    """Algebraic Ward-related controls; NOT complete Ward/Bianchi proofs."""
    p, a, b, u = sp.symbols('p alpha beta u', real=True)
    v, q, tau = sp.symbols('v q tau', nonzero=True)
    z_e, z_c = sp.symbols('z_e z_c', real=True)
    x, y = sp.symbols('x y', real=True)

    sig = a*p-b*p**2
    prime = sp.diff(sig, p)

    # Physical conformal scaling:
    # g_cov -> exp(2u) g_cov
    # sqrt(-g) -> exp(4u) sqrt(-g)
    # P -> exp(-4u) P
    pu = q/(v*sp.exp(4*u))

    check = {
        'hodge_density_invariance': sp.simplify(
            sp.diff(v*sp.exp(4*u)*pu, u)
        ) == 0,

        'P_weyl_weight_minus_four': sp.simplify(
            sp.diff(pu, u).subs(u, 0)+4*q/v
        ) == 0,

        'conformal_trace_chain': sp.simplify(
            sp.diff(
                u+sig.subs(p, p*sp.exp(-4*u)),
                u
            ).subs(u, 0)
            -(1-4*p*prime)
        ) == 0,

        'sigma_derivative': sp.simplify(
            prime-a+2*b*p
        ) == 0,

        'sigma_second_derivative': (
            sp.diff(sig, p, 2) == -2*b
        ),

        'lambda_trace_derivative': sp.simplify(
            tau*prime-tau*(a-2*b*p)
        ) == 0,

        'source_off_sigma': sig.subs(p, 0) == 0,

        'coupling_off_sigma': (
            sig.subs({a: 0, b: 0}) == 0
        ),

        'coupling_off_lambda': (
            (tau*prime).subs({a: 0, b: 0}) == 0
        ),

        'constant_P_no_portal_gradient': (
            sp.diff(
                sig.subs(
                    p, sp.Symbol('p0', real=True)
                ),
                x
            ) == 0
        ),

        'linear_mixed_const_trace_bulk_null': (
            sp.diff(tau*prime, p).subs(b, 0) == 0
        ),

        'mixed_variations_commute': sp.simplify(
            sp.diff(sp.diff(tau*sig, a), b)
            -sp.diff(sp.diff(tau*sig, b), a)
        ) == 0,

        'antisymmetric_commuting_derivatives':
            sp.simplify(
                sp.diff(
                    sp.diff(sp.Function('K')(x, y), x),
                    y
                )
                -sp.diff(
                    sp.diff(sp.Function('K')(x, y), y),
                    x
                )
            ) == 0,
    }

    U = sp.Function('U')(z_e-z_c)

    check['two_coordinate_translation'] = (
        sp.simplify(
            -sp.diff(U, z_e)-sp.diff(U, z_c)
        ) == 0
    )

    V = sp.Function('V')(z_c)

    check['craft_only_false_Earth_force'] = (
        sp.diff(V, z_e) == 0
        and sp.diff(V, z_c) != 0
    )

    return {
        name: bool(ok)
        for name, ok in check.items()
    }


def bounds(a=A, h=H):
    """Scoped static, type-I DEC, linearized-GR necessary budget bound."""
    if not (
        math.isfinite(a)
        and math.isfinite(h)
        and a > 0
        and h > 0
    ):
        raise ValueError(
            'positive finite a and h required'
        )

    scale = a*C*C*h*h/G

    return {
        'a_m_s2': a,
        'all_stress_min_distance_m': h,
        'DEC_general_min_J': scale/4,
        'DEC_sources_below_min_J': scale/2,
        '006D_reference_J': C006D*scale,
        'budget_J': BUDGET,
        'ratio_to_budget': scale/(4*BUDGET),
        'conditional_budget_obstruction':
            scale/4 >= BUDGET,

        'premise': (
            'static type-I DEC in linearized GR; '
            'every source, support AND field stress '
            'element >= h from the target'
        ),

        'not_covered': (
            'a 1m gap free of material can contain '
            'field stress; modified gravity and '
            'quantum matter are not bounded'
        ),
    }


def families():
    """One registered new operator; no qualified survivors."""
    return [
        {
            'id': 'M0',
            'operator': 'sigma(P)=alpha P-beta P^2',
            'physical_response':
                'a=-grad(Phi_E+c^2 sigma) at leading static order',
            'sign': 'NOT_DERIVED_ON_PH16_SOURCE',
            'health': 'OPEN',
            'source': 'PH16_FINITE_LATTICE_ONLY',
            'SI_energy': 'UNKNOWN',
            'cheap_falsifier':
                'same-action full metric/source stress and exterior SI',
        },
        {
            'id': 'M1',
            'operator':
                'Einstein GR + finite type-I DEC stress',
            'physical_response':
                '006D: outward locally, positive far active mass',
            'sign': 'LOCAL_REFERENCE_ONLY',
            'health': 'MATERIAL_OPEN',
            'source': '006D_CONSERVED_LINEARIZED_STRESS',
            'SI_energy':
                'CONDITIONAL_BOUND_FAILS_10MJ',
            'cheap_falsifier':
                'test all-stress distance premise or derive field-aware bound',
        },
        {
            'id': 'M2',
            'operator': (
                'vector-Horndeski double-dual Riemann '
                'L^{munurhosigma} F_Xmunu F_Xrhosigma'
            ),
            'physical_response': 'UNKNOWN',
            'sign': 'UNKNOWN',
            'health': 'OPEN',
            'source': 'UNKNOWN',
            'SI_energy': 'UNKNOWN',
            'cheap_falsifier':
                'metric/boundary variation, constraint and cutoff',
        },
        {
            'id': 'M3',
            'operator':
                'renormalized semiclassical stress (reserve)',
            'physical_response': 'NOT_SPECIFIED',
            'sign': 'UNKNOWN',
            'health': 'OPEN',
            'source': 'NOT_SPECIFIED',
            'SI_energy': 'UNKNOWN',
            'cheap_falsifier':
                'define physical quantum state and backreaction',
        },
    ]


def atlas():
    checks = identities()

    assert len(checks) >= 14 and all(
        checks.values()
    ), checks

    bound = bounds()

    assert bound['conditional_budget_obstruction']

    return {
        'experiment':
            'GAMMA1-00_EXACT_SOURCE_TO_GRAVITY_BRIDGE_FORK',
        'scope':
            'L0_SYMBOLIC_AND_CONDITIONAL_SI_NO_PDE',
        'signature': '-+++',
        'P': '0.5 FX_munu (*FY)^munu',

        'same_action': (
            'Einstein-Hilbert+GHY+Maxwell X/Y+'
            'source+neutral+Earth+supports; '
            'all matter uses g_tilde'
        ),

        'M0_formal_variations': {
            'metric':
                'T_E = exp(2sigma) T_tilde - lambda P g',
            'lambda':
                'exp(4sigma) trace(T_tilde) sigma_prime',
            'X':
                'nabla(F_X-lambda *F_Y)=J_X',
            'Y':
                'nabla(F_Y-lambda *F_X)=J_Y (zero in baseline)',
            'Ward':
                'nabla J=0 only with matter Euler-Lagrange equations',
            'Bianchi':
                'dF_X=dF_Y=0; total stress conserved on shell',
            'neutral':
                'geodesic in g_tilde; sources/support/Earth E-L OPEN',
            'weak_field':
                'a=-grad(Phi_E)-c^2 grad(sigma)',
            'gravitational_boundary_stress': 'OPEN',
            'off_shell_diffeomorphism_identity':
                'NOT_FULLY_DERIVED',
        },

        'exact_checked_algebra': checks,
        'SI_conditional_bounds': bound,
        'families': families(),

        'negative_controls': {
            'source_off':
                'sigma(0)=0; Y variation can still be nonzero',
            'coupling_off':
                'sigma=lambda=0',
            'Earth_off':
                'no Earth E-L and no Earth force observable',
            'constant_P':
                'no local portal gradient',
            'craft_only':
                'no genuine Earth action/reaction',
            'fake_Earth_charge':
                'reject nonuniversal prescribed susceptibility',
            'M2_flat_curvature':
                'operator zero on exactly Minkowski',
            'field_capacity_only':
                'not complete operating energy',
        },

        'convergence': {
            'symbolic': 'EXACT',
            'new_PDE': 'NOT_RUN',
            'continuum_exterior': 'NOT_CERTIFIED',
        },

        'force_ledger': {
            'Earth_down': 'NOT_DERIVED',
            'whole_craft_up': 'NOT_DERIVED',
            'supports_recoil': 'NOT_DERIVED',
            'field_boundary_momentum': 'NOT_DERIVED',
        },

        'energy_ledger': {
            'source': 'UNKNOWN',
            'supports': 'UNKNOWN',
            'fields': 'NOT_SI_NORMALIZED',
            'activation': 'UNKNOWN',
            'off_state': 'UNKNOWN',
            'UV': 'UNKNOWN',
            'complete_J': 'NOT_CERTIFIED',
        },

        'qualified_survivors': [],
        'M3_run_authorized': False,
        'GAMMA1_01_authorized': False,
        'PH16_05_transfer_authorized': False,
        'PH17_transfer_authorized': False,
        '006D_replaced': False,

        'torus_1kg_1g_1m': 'NOT_CERTIFIED',
        'full_mode_health': 'NOT_CERTIFIED',
        'complete_energy_lt10MJ': 'NOT_CERTIFIED',

        'decision':
            'INSUFFICIENT_THEORY_NEEDS_DERIVATION',

        'claim_classification':
            'SCOPED_THEOREM_ATLAS_NOT_GRAVITY_LIFT',
    }
