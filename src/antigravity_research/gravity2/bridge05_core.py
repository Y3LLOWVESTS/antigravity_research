"""GRAVITY2-05: Jordan-source existence and reciprocal-loading preflight.

The only candidate is the existing B_JORDAN_LOCALIZED action template.
No fully specified 4D material/support/Earth action, Einstein solution, or
source-produced R3B loaded response is inferred from this restricted algebra.

Conventions: g=(-,+,+,+), gtilde=e^(2sigma(P))g,
sigma=alpha*P-beta*P**2, real charged scalar D=partial-i*q*A.
"""
from __future__ import annotations

import sympy as s


PARENT_ID = "g2v2_20261121T045908Z_7c71a597"
PARENT_SCIENCE_SHA = "be8fa79e2d58f30a36fa50d7c23d8e087647eb1d05f1ab2c1b2121394f5cddb0"
PARENT_VERIFY_SHA = "d5daae1f97c5d253334b833cd84e72767efeed25092bfb28d913670cc13ff593"


def weighted_static_identity() -> dict:
    """Exact pointwise Euler/boundary identity with spatially varying w,z.

    Source Euler E_a/b = D_i(w D_i a/b) - z dV/da/b, with
    w=e^(2sigma(P(x)))>0, z=e^(4sigma(P(x)))>0,
    V=m2*(a*a+b*b)/2 + lam*(a*a+b*b)**2/4.

    For E_a=E_b=0, integrate against a,b over R^3. If the
    boundary flux vanishes, then integral(w |D_i phi|^2 +
    z (m2+lam*|phi|^2)|phi|^2)=0. Nonnegative m2,lam force
    a=b=0 for finite, decaying scalar.

    Restricted to STRICT static D0phi=0, A0=0, no-support
    flat/static-lapse sector. Nontrivial lapse, phase/charge
    and material boundaries are NOT covered.
    """
    a,b,q,m2,lam,w,z = s.symbols(
        "a b q m2 lam w z",real=True
    )

    aa = s.symbols("A0:3",real=True)
    da = s.symbols("da0:3",real=True)
    db = s.symbols("db0:3",real=True)
    dda = s.symbols("dda0:3",real=True)
    ddb = s.symbols("ddb0:3",real=True)
    dA = s.symbols("dA0:3",real=True)
    dw = s.symbols("dw0:3",real=True)

    u = [
        da[i]+q*aa[i]*b
        for i in range(3)
    ]
    v = [
        db[i]-q*aa[i]*a
        for i in range(3)
    ]

    du = [
        dda[i]+q*(dA[i]*b+aa[i]*db[i])
        for i in range(3)
    ]
    dv = [
        ddb[i]-q*(dA[i]*a+aa[i]*da[i])
        for i in range(3)
    ]

    rho = a*a+b*b
    Va = (m2+lam*rho)*a
    Vb = (m2+lam*rho)*b

    ea = sum(
        (
            w*du[i]+dw[i]*u[i]+w*q*aa[i]*v[i]
            for i in range(3)
        ),
        s.Integer(0),
    ) - z*Va

    eb = sum(
        (
            w*dv[i]+dw[i]*v[i]-w*q*aa[i]*u[i]
            for i in range(3)
        ),
        s.Integer(0),
    ) - z*Vb

    divergence = sum(
        (
            dw[i]*(a*u[i]+b*v[i])
            +w*(
                da[i]*u[i]+db[i]*v[i]
                +a*du[i]+b*dv[i]
            )
            for i in range(3)
        ),
        s.Integer(0),
    )

    positive = (
        w*sum(
            (
                u[i]**2+v[i]**2
                for i in range(3)
            ),
            s.Integer(0),
        )
        +z*(m2+lam*rho)*rho
    )

    assert s.expand(
        a*ea+b*eb-divergence+positive
    ) == 0

    wrong_ea = ea-sum(
        (dw[i]*u[i] for i in range(3)),
        s.Integer(0),
    )
    wrong_eb = eb-sum(
        (dw[i]*v[i] for i in range(3)),
        s.Integer(0),
    )

    assert s.expand(
        a*wrong_ea+b*wrong_eb-divergence+positive
    ) != 0

    return {
        "test":
            "EXACT_3D_JORDAN_WEIGHTED_STATIC_EULER",
        "identity":
            "a*E_a+b*E_b=div_i[w*(a*U_i+b*V_i)]"
            "-w*sum_i(U_i**2+V_i**2)"
            "-z*(m2+lam*rho)*rho",
        "residual": "0",
        "nonconstant_weight_derivative_required": True,
        "omitted_grad_weight_negative_control": "NONZERO",
        "conditional_no_go":
            "STATIC_D0_ZERO_A0_ZERO_POSITIVE_POTENTIAL_NO_SUPPORT",
        "result":
            "TRIVIAL_SCALAR_AND_ZERO_MINIMAL_CURRENT_WITH_ZERO_SURFACE_FLUX",
        "scope":
            "R3_STATIC_FLAT_SLICE_NO_MATERIAL_BOUNDARIES; "
            "DOES_NOT_EXCLUDE_HARMONIC_PHASE_A0_OR_SUPPORTS",
    }


def portal_source_hessian() -> dict:
    """Exact local Jordan source stress/portal cross variation.

    The two-form component reduction P=X*Y is a local model
    for disjoint F_X,F_Y components. NOT a globally solved
    Maxwell or gravitational system.

    The local amplitude u is a scalar and k*u**2 is a
    chosen positive derivative-contraction model.
    Everything here is algebraic and OFF SHELL.
    """
    p,alpha,beta,k,rho,m2,lam = s.symbols(
        "p alpha beta k rho m2 lam",
        real=True,
    )

    sigma = alpha*p-beta*p*p
    sigp = s.diff(sigma,p)
    V = m2*rho/s.Integer(2)+lam*rho*rho/s.Integer(4)

    L_j = (
        -s.exp(2*sigma)*k/s.Integer(2)
        -s.exp(4*sigma)*V
    )

    L_e = -k/s.Integer(2)-V
    trace = -s.exp(-2*sigma)*k-4*V

    assert s.simplify(
        s.diff(L_j,p)-s.exp(4*sigma)*trace*sigp
    ) == 0

    assert s.diff(L_e,p) == 0

    x,y,u = s.symbols("x y u",real=True)
    P = x*y
    ss = alpha*P-beta*P*P

    K = k*u*u
    V_u = m2*u*u/s.Integer(2)+lam*u**4/s.Integer(4)

    L = (
        -s.exp(2*ss)*K/s.Integer(2)
        -s.exp(4*ss)*V_u
    )

    cross = s.diff(L,x,u)

    assert s.simplify(
        cross-s.diff(L,u,x)
    ) == 0

    # Second derivative of P=X*Y contributes to
    # the X/Y field Hessian even at fixed scalar amplitude.
    d2xy = s.diff(L,x,y)
    P_only = s.symbols("Ponly",real=True)

    Lp = (
        -s.exp(
            2*(alpha*P_only-beta*P_only**2)
        )*K/s.Integer(2)
        -s.exp(
            4*(alpha*P_only-beta*P_only**2)
        )*V_u
    )

    chain = (
        s.diff(Lp,P_only,2).subs(P_only,P)*x*y
        +s.diff(Lp,P_only).subs(P_only,P)
    )

    assert s.simplify(d2xy-chain) == 0

    omitted_chain = s.diff(
        Lp,P_only
    ).subs(P_only,P)

    assert s.simplify(
        d2xy
        -s.diff(Lp,P_only,2).subs(P_only,P)*x*y
        -omitted_chain
    ) == 0

    numbers = {
        alpha:s.Rational(1,11),
        beta:s.Rational(1,113),
        k:2,
        m2:3,
        lam:1,
        x:1,
        y:2,
        u:1,
    }

    assert s.simplify(
        cross.subs(numbers)
    ) != 0

    assert s.simplify(
        d2xy.subs(numbers)
    ) != 0

    assert s.simplify(
        omitted_chain.subs(numbers)
    ) != 0

    # A restricted positive unconstrained source mode.
    # This is NOT the constrained R3B Hessian.
    Hff = s.Rational(5)
    Hfu = s.Rational(2)
    Huu = s.Rational(3)
    reduced = Hff-Hfu**2/Huu

    assert reduced == s.Rational(11,3)
    assert reduced < Hff

    return {
        "source_frame":
            "JORDAN_UNIVERSAL_SOURCE",
        "sigma":
            "alpha*P-beta*P**2",
        "source_trace":
            "Ttilde_source=-exp(-2sigma)*K-4V",
        "dL_source_dP":
            "exp(4sigma)*Ttilde_source*sigma_P",
        "Einstein_source_dL_dP":
            "0_AT_FIXED_CANONICAL_FIELDS",
        "trace_identity_residual": "0",
        "mixed_F_source_second_derivative":
            "NONZERO_AT_DECLARED_OFFSHELL_TEST_POINT",
        "mixed_source_F_reciprocity_residual": "0",
        "mixed_FX_FY_includes_P_second_derivative": True,
        "omitted_Pxy_chain_negative_control": "NONZERO",
        "restricted_positive_Huu_schur": str(reduced),
        "unrelaxed_Hff": str(Hff),
        "Schur_scope":
            "ONE_UNCONSTRAINED_POSITIVE_SOURCE_MODE; "
            "NOT_GAUGE_PROJECTED_REAL_FIELD_HESSIAN",
        "loaded_force_sign":
            "NOT_DETERMINED",
    }


def corrected_higgs_scope() -> dict:
    """Correct C/D source-trace classification, preserve prior files."""
    from .miner2_math import registry

    cases = {
        x["id"]:x
        for x in registry()
    }

    out = {}

    for name in (
        "B_JORDAN_LOCALIZED",
        "C_HIGGS_Y_CONTROL",
        "D_HIGGS_BOTH_CONTROL",
    ):
        card = cases[name]
        assert card["frame"] == "JORDAN"

        out[name] = {
            "source_in_physical_metric": True,
            "general_interior_portal_trace_term":
                "PRESENT_WHEN_K_OR_V_NONZERO",
            "exterior_constant_broken_vacuum":
                "TRACE_ZERO_IF_K_ZERO_AND_V_AT_MINIMUM_ZERO",
            "historical_prior_flag_not_overwritten": True,
            "massless_U1_count_from_previous_scope":
                2-sum(card["vev"]),
        }

    return out


def scientific_evidence() -> dict:
    return {
        "weighted_static_source":
            weighted_static_identity(),
        "Jordan_trace_and_reciprocity":
            portal_source_hessian(),
        "historical_Higgs_classification_erratum":
            corrected_higgs_scope(),
        "historical_R3B_loaded_min_m_s2":
            -129.67185782242464,
        "historical_R3B_prescribed_capacity_J":
            1.5429162116460216,
        "historical_values":
            "PROVENANCE_ONLY_NOT_RECOMPUTED",
        "decision":
            "SCOPED_JORDAN_STATIC_NO_GO; "
            "STATIONARY_SUPPORTED_SOURCE_UNDERDETERMINED",
        "gates": {
            "G01_ACTION":
                "INCOMPLETE_EARTH_NEUTRAL_SUPPORTS",
            "G02_VARIATION":
                "PASS_SCOPED_JORDAN_WEIGHTED_EULER_AND_PORTAL_CHAIN",
            "G03_WARD":
                "INHERITED_SCOPED_03A_NOT_REDERIVED_FULL_DIFEOMORPHISM",
            "G04_HEALTH":
                "NOT_DERIVED_FULL_CONSTRAINED_MODES",
            "G05_SOURCE":
                "STATIC_CONVEX_UNSUPPORTED_FAIL; STATIONARY_OPEN",
            "G06_LOAD":
                "NOT_AUTHORIZED_UNDERDETERMINED",
            "G07_METRIC":
                "NOT_SOLVED_EINSTEIN",
            "G08_ENERGY":
                "NOT_CERTIFIED_COMPLETE_SI",
            "G09_EXTERIOR": "NOT_RUN",
            "G10_REACTION": "NOT_DERIVED",
            "G11_REALISM": "NOT_CERTIFIED",
        },
        "source_equations_scope":
            "STATIC_ONLY_WITH_NONUNIFORM_CONFORMAL_WEIGHT; "
            "FULL_JORDAN_4D_SUPPORT_FLUID_NOT_DERIVED",
        "survivors": 0,
        "physical_lift": "NOT_DERIVED",
        "complete_energy": "NOT_CERTIFIED",
        "full_regression": "NOT_RUN",
    }
