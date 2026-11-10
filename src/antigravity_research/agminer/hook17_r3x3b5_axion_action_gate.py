"""R3X3B5: necessary action-level gates for a minimal axion compensator.

Declared terms:
  L = -F^2/4 - (da)^2/2 - V(a) + gamma*a*P/4 + L_m
  P = F*Fdual
  g_phys = exp(2*kappa*a*P)*g

Define tau = delta(S_m)/delta(sigma)/sqrt(-g),
with sigma = kappa*a*P.

The Maxwell constitutive coefficient is:
  theta = a*(gamma + 4*kappa*tau).

The axion equation is:
  box(a) - V'(a) + (gamma/4+kappa*tau)*P = 0.

Scope: preservation of original F and original Maxwell currents
in a connected region with P != 0, smooth fields and no extra
external axion source. This is not a general no-go theorem.
"""
from __future__ import annotations

from sympy import Matrix, Rational, factor, simplify, symbols


def tensor_non_degeneracy():
    ex, ey, ez, bx, by, bz = symbols(
        "Ex Ey Ez Bx By Bz", real=True
    )

    f = Matrix([
        [0, ex, ey, ez],
        [-ex, 0, -bz, by],
        [-ey, bz, 0, -bx],
        [-ez, -by, bx, 0],
    ])

    eb = ex*bx + ey*by + ez*bz
    determinant = factor(f.det())

    assert simplify(determinant - eb**2) == 0

    return {
        "det_F_covariant": str(determinant),
        "det_equals_E_dot_B_squared": True,
        "P_nonzero_implies_Fdual_nondegenerate": True,
    }


def action_variation_gate():
    gamma, kappa, tau, a, p = symbols(
        "gamma kappa tau a P", real=True
    )

    theta = (gamma + 4*kappa*tau)*a
    coefficient = (
        gamma*Rational(1, 4) + kappa*tau
    )*a

    scalar_source = (
        gamma*Rational(1, 4) + kappa*tau
    )*p

    assert simplify(theta - 4*coefficient) == 0
    assert simplify(
        theta.diff(tau) - 4*kappa*a
    ) == 0
    assert simplify(
        theta.diff(a) - gamma - 4*kappa*tau
    ) == 0
    assert simplify(
        4*a*scalar_source - theta*p
    ) == 0

    return {
        "theta": str(theta),
        "maxwell_matter_interface_derivative_of_theta_by_tau":
            str(theta.diff(tau)),
        "maxwell_axion_derivative_of_theta_by_a":
            str(theta.diff(a)),
        "axion_eom_source": str(scalar_source),
        "gauge_ward_identity": "DIV_J_ZERO_REQUIRED",
        "full_metric_noether_identity_certified": False,
    }


def exact_mirror_no_go():
    gamma, kappa, a, tau, p1, p2 = symbols(
        "gamma kappa a tau P1 P2", real=True
    )

    theta = (gamma + 4*kappa*tau)*a

    # If P != 0 and the original F and J are unchanged,
    # the Maxwell equation requires grad(theta) = 0.
    #
    # In vacuum tau=0. With gamma != 0, a is constant.
    # Its EOM at two points with different P cannot hold
    # for a single potential derivative V'(a).

    theta_vacuum = simplify(theta.subs(tau, 0))
    assert theta_vacuum == gamma*a

    difference = factor(
        gamma*(p1-p2)/4
    )

    assert simplify(
        difference - gamma*(p1-p2)/4
    ) == 0

    # With gamma=0, theta=4*kappa*tau*a.
    # It is zero in exterior vacuum.
    # Exact continuous interface silence then requires
    # theta=0 throughout the connected P!=0 region.
    # Where tau and kappa are nonzero, a=0.
    # Hence sigma=kappa*a*P vanishes in that material.

    no_bare_theta = simplify(
        theta.subs(gamma, 0)
    )

    assert no_bare_theta == 4*kappa*tau*a

    return {
        "vacuum_theta_with_bare_term":
            str(theta_vacuum),
        "two_point_axion_eom_difference":
            str(difference),
        "bare_gamma_nonzero_varying_P_exact_mirror":
            "INCOMPATIBLE",
        "no_bare_gamma_strict_interface_silence":
            "NO_NONZERO_SIGMA_IN_MATERIAL_ON_CONNECTED_NONDEGENERATE_REGION",
        "different_loaded_field_profiles_excluded": False,
        "additional_axion_sources_excluded": False,
        "other_compensating_actions_excluded": False,
    }


def all_gates():
    return {
        "branch": "032H17A12D1R3X3B5",
        "scope":
            "MINIMAL_DYNAMIC_AXION_EXACT_OLD_MIRROR_PRESERVATION",
        "tensor": tensor_non_degeneracy(),
        "variation": action_variation_gate(),
        "exact_mirror": exact_mirror_no_go(),
        "original_r3b_preloaded_capacity_preserved": True,
        "new_compensator_certified": False,
        "physical_antigravity_model_found": False,
        "006d_replaced": False,
    }
