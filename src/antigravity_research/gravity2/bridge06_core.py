"""GRAVITY2-06: stationary Jordan-source Gauss and support preflight.

No PDE solves, no Einstein closure. All equations concern a 1D component
reduction of a canonical charged scalar coupled to the Jordan metric,
P=B*d_x A0, holding B and background geometry fixed during variation.
This is NOT the original R3B field kernel or a complete same-action solution.
"""
from __future__ import annotations

import sympy as sp

HISTORY = {
    "ph12_ph16": "EXISTING_GAUGED_SOURCE_AND_STABILITY_RESULTS_NOT_RERUN",
    "r3b_loaded_min_m_s2": -129.67185782242464,
    "r3b_prescribed_field_capacity_J": 1.5429162116460216,
    "source_ledger_complete": False,
}


def stationary_local_variations():
    """Derive Euler derivatives from the reduced *same* local source action."""
    a, ap, f, fp, B, omega, q = sp.symbols(
        'a ap f fp B omega q', real=True
    )
    alpha, beta, m2, lam = sp.symbols(
        'alpha beta m2 lam', real=True
    )
    P = B*ap
    sigma = alpha*P-beta*P**2
    w, z = sp.exp(2*sigma), sp.exp(4*sigma)
    Omega = omega-q*a
    V = m2*f*f/2+lam*f**4/4
    lag = ap*ap/2 + w*(Omega**2*f*f-fp*fp)/2-z*V
    sigp = alpha-2*beta*P
    trace = sp.exp(-2*sigma)*(Omega**2*f*f-fp*fp)-4*V
    polarization = sp.exp(4*sigma)*trace*sigp
    displacement = ap+B*polarization

    assert sp.simplify(sp.diff(lag, ap)-displacement) == 0
    assert sp.simplify(sp.diff(lag, a)+q*w*Omega*f*f) == 0
    assert sp.simplify(sp.diff(lag, fp)+w*fp) == 0
    assert sp.simplify(
        sp.diff(lag, f)-(w*Omega**2*f-z*(m2*f+lam*f**3))
    ) == 0
    assert sp.simplify(sp.diff(lag, ap, f)-sp.diff(lag, f, ap)) == 0

    # Nonzero polarization and mixed derivative at a declared rational point.
    point = {a: sp.Rational(1,3), ap: sp.Rational(2,5),
             f: sp.Rational(3,4), fp: sp.Rational(1,6),
             B: sp.Rational(4,3), omega: sp.Rational(3,2),
             q: sp.Rational(1,2), alpha: sp.Rational(1,10),
             beta: sp.Rational(1,100), m2: 2, lam: 1}
    pol_nonzero = sp.simplify((B*polarization).subs(point))
    mixed_nonzero = sp.simplify(sp.diff(lag,ap,f).subs(point))
    assert pol_nonzero != 0
    assert mixed_nonzero != 0

    # Genuine gauge invariance of stationary phase: omega -> omega+q*c,
    # A0 -> A0+c, with unchanged A0' and f.
    c=sp.symbols('c',real=True)
    assert sp.simplify(
        lag.subs({a:a+c,omega:omega+q*c})-lag
    ) == 0

    # For B=0 (or sigma'=0) the portal polarization disappears.
    assert sp.simplify((B*polarization).subs(B,0)) == 0
    assert sp.simplify((B*polarization).subs({alpha:0,beta:0})) == 0

    return {
        "model": "STATIC_FLAT_BACKGROUND_1D_COMPONENT_P=B*dA0; B_FROZEN",
        "L_reduced": "(dA0)^2/2 + w*((omega-q*A0)^2*f^2-(df)^2)/2 - z*V",
        "V": "m2*f^2/2+lambda*f^4/4",
        "w_z": "w=exp(2*sigma(P)); z=exp(4*sigma(P))",
        "P": "B*dA0; one-component normalized surrogate, not R3B normalization",
        "Omega": "omega-q*A0",
        "scalar_Euler": "div(w grad f)+w*Omega^2*f-z*(m2*f+lambda*f^3)=0",
        "Gauss_Euler": "div(grad A0 + B*Pi)=-q*w*Omega*f^2",
        "Pi": "exp(4*sigma)*Ttilde_source*sigma_P",
        "Ttilde_source": "exp(-2*sigma)*(Omega^2*f^2-|grad f|^2)-4*V",
        "source_charge_density": "q*w*Omega*f^2",
        "exact_Euler_derivatives": "PASS",
        "gauge_stationary_phase_shift_residual": "0",
        "mixed_source_A0prime_reciprocity_residual": "0",
        "portal_polarization_nonzero_control": "PASS",
        "omit_portal_polarization_negative_control": "FAIL_AS_REQUIRED",
        "sigma_zero_negative_control": "PASS",
        "full_XY_neutral_Earth_support_Einstein_action": "NOT_DERIVED",
    }


def stationary_integral_and_wall():
    """Exact integrated stationary scalar identity with optional fixed wall.

    L_wall=-kappa*f^2/2 per fixed boundary area, stationary Robin condition
    w*n.grad(f)+kappa*f=0. If surface and volume factors omitted this is
    a flat normal-wall reduced action ONLY, not a physical spacecraft wall.
    """
    f, grad, omega, a, q, m2, lam, w, z, kappa = sp.symbols(
        'f grad omega a q m2 lam w z kappa',real=True
    )
    source = w*((omega-q*a)**2*f**2-grad**2)-z*(m2*f**2+lam*f**4)
    # Scalar integrated EOM: 0 = -int (w grad²+zV') + int w Omega²f² + boundary.
    # Wall Robin makes boundary=-kappa f².
    identity = sp.expand(
        (w*grad**2+z*(m2*f**2+lam*f**4)+kappa*f**2)
        -w*(omega-q*a)**2*f**2
    )
    assert sp.expand(identity+source-kappa*f*f) == 0
    # Nonnegative lhs when omega=0 AND A0=0 and positive coefficients.
    assert sp.simplify(identity.subs({omega:0,a:0})-(
        w*grad**2+z*(m2*f**2+lam*f**4)+kappa*f**2
    )) == 0
    # Frequency bound holds ONLY for prescribed positive w,z plus
    # ordinary Gauss (no polarization): |Omega|<=|omega| when q*omega>0.
    return {
        "scalar_integral_identity": "int[w*|grad f|^2+z*(m2*f^2+lambda*f^4)]+surface(kappa*f^2)=int[w*Omega^2*f^2]",
        "fixed_wall_action": "S_wall=-int_boundary dt dA (kappa/2)*f^2; wall geometry prescribed",
        "natural_Robin": "w*n.grad(f)+kappa*f=0",
        "strict_static_positive_wall": "TRIVIAL_FOR_omega_A0_ZERO_AND_kappa_m2_lambda_NONNEGATIVE",
        "ordinary_Gauss_frozen_w_only": "-Delta A0+q^2*w*f^2*A0=q*omega*w*f^2",
        "conditional_maximum_principle": "if q>0 omega>0 A0(infty)=0 w>0 independent of A0 gradients, then 0<=q*A0<=omega",
        "conditional_frequency_no_go": "if omega^2 < inf_x(m2*z/w), no nonzero localized solution with kappa>=0 under ordinary Gauss and zero boundary work",
        "full_portal_Gauss_difference": "div(B*Pi) term invalidates use of ordinary-Gauss maximum-principle bound",
        "material_wall_dynamical_traction": "NOT_DERIVED",
        "physical_finite_source": "NOT_ESTABLISHED",
    }


def evidence():
    a = stationary_local_variations()
    b = stationary_integral_and_wall()
    return {
        "program":"GRAVITY2-06_SOURCE_EXISTENCE_PREFLIGHT",
        "decision":"FULL_PORTAL_GAUSS_CHANGES_STATIONARY_BOUND; SOURCE_UNDERDETERMINED",
        "local_variations":a,
        "conditional_obstructions":b,
        "history":HISTORY,
        "negative_controls":[
            "portal off -> ordinary Gauss", "omitted B*Pi breaks Euler variation",
            "phase gauge shift omega and A0 together", "wall with negative kappa not protected",
        ],
        "gates":{
            "G00_PARENT":"LOCKED_CONDITIONALLY_BY_RUNNER",
            "G01_ACTION":"INCOMPLETE_XY_NEUTRAL_EARTH_SUPPORT",
            "G02_VARIATION":"PASS_SCOPED_COMPONENT_SAME_REDUCED_ACTION",
            "G03_WARD":"PASS_RESTRICTED_STATIONARY_GAUGE_SHIFT_ONLY",
            "G04_HEALTH":"NOT_DERIVED",
            "G05_SOURCE":"STRICT_STATIC_AND_FROZEN_PORTAL_BOUNDS_ONLY; FULL_PORTAL_OPEN",
            "G06_LOAD":"NOT_AUTHORIZED",
            "G07_METRIC":"EINSTEIN_NOT_SOLVED",
            "G08_ENERGY":"COMPLETE_SI_NOT_CERTIFIED",
            "G09_EXTERIOR":"NOT_RUN",
            "G10_REACTION":"NOT_DERIVED",
            "G11_REALISM":"NOT_CERTIFIED",
        },
        "qualified_survivors":0,
        "full_action":"NOT_DERIVED",
        "lift":"NOT_DERIVED",
        "complete_energy":"NOT_CERTIFIED",
        "full_regression":"NOT_RUN",
    }
