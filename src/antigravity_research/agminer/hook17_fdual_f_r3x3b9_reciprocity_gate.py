"""R3X3B9 — local algebraic-compensator reciprocity preflight.

For a smooth local interaction L(T,P,chi_i), with nondynamical
auxiliaries chi_i satisfying their own algebraic equations:

    L_eff_TP = L_TP - L_Tchi H_chichi^-1 L_chiP

This is a Schur-complement identity.

Exact cancellation of this mixed matter-field response eliminates
the field-dependent matter-force kernel in the SAME local channel.

Not excluded:
- dynamical or derivative compensators;
- independent physical source channels;
- altered fully loaded field profiles;
- nonlocal effective interactions;
- other complete-action structures.

No physical antigravity model is certified.
"""
from __future__ import annotations

from sympy import Matrix, Rational, diff, factor, simplify, symbols


def one_auxiliary_gate() -> dict:
    t, p, x = symbols("T P chi", real=True)
    a, g, h = symbols("a g h", real=True)
    m2 = symbols("m2", positive=True)

    lagrangian = (
        a*t*p
        + (g*p + h*t)*x
        - m2*x**2/2
    )

    solution = (g*p + h*t)/m2

    assert simplify(
        diff(lagrangian, x).subs(x, solution)
    ) == 0

    effective = factor(lagrangian.subs(x, solution))

    matter_mixed = factor(diff(effective, t, p))
    field_mixed = factor(diff(effective, p, t))

    schur = factor(
        diff(lagrangian, t, p)
        - diff(lagrangian, t, x)
        / diff(lagrangian, x, x)
        * diff(lagrangian, x, p)
    )

    expected = a + g*h/m2

    assert simplify(matter_mixed - expected) == 0
    assert simplify(field_mixed - expected) == 0
    assert simplify(schur - expected) == 0

    # Exact cancellation of the mixed coupling.
    tuning = {h: -a*m2/g}
    cancelled = factor(effective.subs(tuning))

    assert simplify(diff(cancelled, t, p)) == 0
    assert simplify(diff(cancelled, p, t)) == 0

    # A P^2 field interaction remains; it has not been
    # proven dynamically stable or phenomenologically allowed.
    assert simplify(
        diff(cancelled, p, p) - g**2/m2
    ) == 0

    return {
        "on_shell_mixed_coefficient": str(field_mixed),
        "schur_complement_verified": True,
        "matter_and_carrier_mixed_derivatives_equal": True,
        "exact_algebraic_cancellation_removes_force_kernel": True,
        "cancelled_example_effective_density": str(cancelled),
        "remaining_p_squared_term": True,
        "remaining_nonlinear_field_stability_certified": False,
    }


def two_auxiliary_gate() -> dict:
    d, u, v, s, r = symbols("d u v s r", real=True)
    m1, m2, k = symbols("m1 m2 k", real=True)

    hessian = Matrix([
        [m1, k],
        [k, m2],
    ])

    matter_mixing = Matrix([[u, v]])
    field_mixing = Matrix([s, r])

    determinant = factor(hessian.det())

    mixed = factor(
        d - (
            matter_mixing
            * hessian.inv()
            * field_mixing
        )[0]
    )

    expected = factor(
        d - (
            u*m2*s - u*k*r
            - v*k*s + v*m1*r
        ) / determinant
    )

    assert simplify(mixed - expected) == 0

    witness = mixed.subs({
        d: 2,
        u: 1,
        v: 2,
        s: 3,
        r: 4,
        m1: 5,
        m2: 6,
        k: 1,
    })

    assert witness == Rational(10, 29)

    return {
        "two_auxiliary_schur_complement_verified": True,
        "hessian_determinant": str(determinant),
        "mixed_kernel": str(mixed),
        "rank_two_rational_witness": str(witness),
        "singular_auxiliary_hessian_excluded_by_scope": True,
    }


def result() -> dict:
    return {
        "branch": "032H17A12D1R3X3B9",
        "scope":
            "LOCAL_SMOOTH_ALGEBRAIC_AUXILIARIES_EXACT_MIXED_RESPONSE_CANCELLATION",
        "single_auxiliary": one_auxiliary_gate(),
        "two_auxiliary": two_auxiliary_gate(),
        "conclusion":
            "EXACT_LOCAL_MIXED_KERNEL_CANCELLATION_REMOVES_SAME_CHANNEL_FIELD_DEPENDENT_MATTER_FORCE",
        "dynamical_derivative_compensators_excluded": False,
        "independent_source_channels_excluded": False,
        "different_loaded_field_profiles_excluded": False,
        "nonlinear_full_action_certified": False,
        "original_r3b_1p542916_j_preloaded_preserved": True,
        "physical_antigravity_model_found": False,
        "006d_replaced": False,
    }
