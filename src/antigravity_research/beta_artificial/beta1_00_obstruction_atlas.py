"""BETA1-00: exact source-to-metric obstruction preflight.

SCIENTIFIC QUESTION
-------------------
Which variations and null mechanisms separate PH15-P10's X/source
and first-order Y calculation from a reciprocal physical metric?

MODEL
-----
Metric signature (-,+,+,+).

    P = (1/2) F_X *F_Y
    sigma = alpha*P - beta*P**2
    L_m = -exp(2*sigma)*K - exp(4*sigma)*U

K denotes g^{mu nu}(D_mu psi)* D_nu psi.
U is a scalar potential.

This is a candidate action, not a completed theory.

METHOD
------
Symbolically check portal variations, Weyl metric response, gauge
reciprocity, reduced Ward identities, integrability nulls, and one
restricted local kinetic Schur-complement counterexample.

LIMITATIONS
-----------
No full constrained principal symbol is derived.
No complete X/Y/source/gravity equilibrium is solved.
No Earth reaction or spacecraft force is calculated.
The local kinetic toy is not a stability certificate.
PH15 canonical energies are not SI joules.

CLAIM CLASSIFICATION
--------------------
NECESSARY_CONDITION_DERIVED
"""

import sympy as sp

P, alpha, beta, K, U = sp.symbols(
    "P alpha beta K U", real=True
)

E, B, v = sp.symbols(
    "E B v", real=True
)


def portal_quantities():
    sigma = alpha * P - beta * P**2

    lm = (
        -sp.exp(2 * sigma) * K
        -sp.exp(4 * sigma) * U
    )

    trace_fixed_P = (
        -2 * sp.exp(2 * sigma) * K
        -4 * sp.exp(4 * sigma) * U
    )

    lam = sp.diff(lm, P)

    return sigma, lm, trace_fixed_P, lam


def local_kinetic_quantities():
    """Unconstrained local E,v toy; not full physical mode health."""

    sigma = alpha * (E * B) - beta * (E * B)**2

    lag = (
        E**2 / 2
        + sp.exp(2 * sigma) * v**2 / 2
        - sp.exp(4 * sigma) * U
    )

    h_ee = sp.simplify(
        sp.diff(lag, E, 2).subs(E, 0)
    )

    h_ev = sp.simplify(
        sp.diff(lag, E, v).subs(E, 0)
    )

    h_vv = sp.simplify(
        sp.diff(lag, v, 2).subs(E, 0)
    )

    schur = sp.factor(
        h_ee - h_ev**2 / h_vv
    )

    return {
        "h_EE": h_ee,
        "h_Ev": h_ev,
        "h_vv": h_vv,
        "schur": schur,
    }


def exact_checks():
    sigma, lm, tr, lam = portal_quantities()

    checks = {}

    checks["lambda_identity"] = (
        sp.simplify(
            lam - tr * sp.diff(sigma, P)
        ) == 0
    )

    expected_dlam0 = (
        -4 * alpha**2 * K
        +4 * beta * K
        -16 * alpha**2 * U
        +8 * beta * U
    )

    dlam0 = sp.simplify(
        sp.diff(lam, P).subs(P, 0)
    )

    checks["lambda_P_identity"] = (
        sp.simplify(dlam0 - expected_dlam0) == 0
    )

    # Weyl scaling:
    # g -> exp(2w)g
    # P -> exp(-4w)P
    # K -> exp(-2w)K

    w = sp.symbols("w", real=True)

    p_w = P * sp.exp(-4 * w)

    s_w = alpha * p_w - beta * p_w**2

    density_w = -sp.exp(4 * w) * (
        sp.exp(2 * s_w - 2 * w) * K
        +sp.exp(4 * s_w) * U
    )

    variation = sp.diff(
        density_w, w
    ).subs(w, 0)

    checks["Weyl_P_metric_chain"] = (
        sp.simplify(
            variation - (tr - 4 * P * lam)
        ) == 0
    )

    # Independent mixed epsilon sign check.
    # Choose FX_01=E, FY_23=B.

    fx = sp.zeros(4)
    fy = sp.zeros(4)

    fx[0, 1] = E
    fx[1, 0] = -E

    fy[2, 3] = B
    fy[3, 2] = -B

    mixed = sp.Rational(1, 4) * sum(
        sp.LeviCivita(i, j, k, l)
        *fx[i, j]
        *fy[k, l]
        for i in range(4)
        for j in range(4)
        for k in range(4)
        for l in range(4)
    )

    checks["mixed_epsilon_sign"] = (
        sp.simplify(mixed - E * B) == 0
    )

    # Restricted constitutive reciprocity.
    # The covariant Hodge and boundary obligations
    # remain separate physical research gates.

    fx_symbol, fy_symbol, lam_symbol = sp.symbols(
        "f_x f_y lambda"
    )

    paired_l = (
        -fx_symbol**2 / 2
        -fy_symbol**2 / 2
        +lam_symbol * fx_symbol * fy_symbol
    )

    hx = -sp.diff(paired_l, fx_symbol)
    hy = -sp.diff(paired_l, fy_symbol)

    checks["four_reciprocal_variations"] = (
        sp.simplify(
            hx - (fx_symbol - lam_symbol * fy_symbol)
        ) == 0
        and
        sp.simplify(
            hy - (fy_symbol - lam_symbol * fx_symbol)
        ) == 0
        and
        sp.simplify(
            sp.diff(lm, K) + sp.exp(2 * sigma)
        ) == 0
        and
        sp.simplify(
            sp.diff(lm, U) + sp.exp(4 * sigma)
        ) == 0
    )

    # Reduced off-shell phase Ward identity.
    # Q = dL/d(theta_dot)
    # dL/dA0 = -q Q
    # q E_theta - d(E_A0)/dt = 0

    t = sp.symbols("t")
    q = sp.symbols("q", real=True)

    phase = sp.Function("theta")(t)
    a0 = sp.Function("A0")(t)
    amplitude = sp.Function("f")(t)

    qdot = (
        sp.exp(2 * sigma)
        *amplitude**2
        *(sp.diff(phase, t) - q * a0)
    )

    etheta = -sp.diff(qdot, t)
    ea0 = -q * qdot

    checks["charged_phase_Ward"] = (
        sp.simplify(
            q * etheta - sp.diff(ea0, t)
        ) == 0
    )

    # Static electrostatic integrability controls.

    x, y, z, c = sp.symbols(
        "x y z c", real=True
    )

    a0xyz = x * y + z**2

    electric = -sp.Matrix([
        sp.diff(a0xyz, s)
        for s in (x, y, z)
    ])

    lambda_aligned = a0xyz**2 + 1

    grad_lam = sp.Matrix([
        sp.diff(lambda_aligned, s)
        for s in (x, y, z)
    ])

    aligned = grad_lam.cross(electric)

    constant = sp.Matrix([
        sp.diff(c, s)
        for s in (x, y, z)
    ]).cross(electric)

    transverse = sp.Matrix([
        1, 0, 0
    ]).cross(electric)

    checks["parity_and_integrability_nulls"] = (
        sp.simplify(
            lam.subs({alpha: 0, P: 0})
        ) == 0
        and
        all(
            sp.simplify(term) == 0
            for term in aligned
        )
        and
        all(
            sp.simplify(term) == 0
            for term in constant
        )
        and
        any(
            sp.simplify(term) != 0
            for term in transverse
        )
    )

    kin = local_kinetic_quantities()

    expected_schur = 1 + B**2 * (
        -2 * beta * v**2
        +8 * beta * U
        -2 * alpha**2 * v**2
        -16 * alpha**2 * U
    )

    checks["reduced_schur"] = (
        sp.simplify(
            kin["schur"] - expected_schur
        ) == 0
        and
        kin["schur"].subs({
            B: 1,
            v: 1,
            U: 0,
            alpha: 0,
            beta: 1,
        }) == -1
    )

    return checks


def gap_atlas():
    return [
        {
            "id": "G1_SOURCE_REALIZATION",
            "destination": "PH15/PH16",
            "necessary_condition":
                "full scalar Euler-Lagrange, conserved charges, "
                "finite support and real source stress",
            "falsifier":
                "nonzero loaded source EOM, unstable mode, "
                "or incompatible UV",
        },
        {
            "id": "G2_CARRIER_RECIPROCITY",
            "destination": "PH16",
            "necessary_condition":
                "both H_X=FX-lambda*FY and "
                "H_Y=FY-lambda*FX from one action",
            "falsifier":
                "no healthy reciprocal continuation "
                "or wrong constitutive sign",
        },
        {
            "id": "G3_CONSTRAINED_HEALTH",
            "destination": "PH16",
            "necessary_condition":
                "full gauge-projected positive kinetic "
                "and healthy characteristics",
            "falsifier":
                "negative physical eigenmode "
                "or ill-posed characteristics",
        },
        {
            "id": "G4_PASSIVE_NEUTRAL_MATTER",
            "destination": "BETA1-02/PH16",
            "necessary_condition":
                "neutral/support trace enters portal; "
                "passive, causal material response",
            "falsifier":
                "arbitrarily imposed interface "
                "or nonpassive susceptibility",
        },
        {
            "id": "G5_EARTH_CRAFT_EXTERNAL",
            "destination": "PH17",
            "necessary_condition":
                "on-shell exterior and whole "
                "craft/Earth/field momentum ledger",
            "falsifier":
                "all onboard novel forces cancel "
                "or exterior flux absent",
        },
        {
            "id": "G6_CAUSAL_CYCLES",
            "destination": "B11-M6",
            "necessary_condition":
                "retarded signed impulse including "
                "all phases and recoil without resets",
            "falsifier":
                "negative phases/losses erase "
                "net external cycle impulse",
        },
        {
            "id": "G7_ENERGY_UV",
            "destination": "PH16/PH17",
            "necessary_condition":
                "SI-matched source, support, field, "
                "drive, losses, EFT and empirical checks",
            "falsifier":
                "unavoidable complete operating "
                "cost >= 10,000,000 J",
        },
    ]


def scientific_atlas():
    sigma, lm, tr, lam = portal_quantities()

    kin = local_kinetic_quantities()

    return {
        "lambda_exact": str(lam),

        "lambda_at_P0": str(
            sp.simplify(lam.subs(P, 0))
        ),

        "lambda_P_at_P0": str(
            sp.simplify(
                sp.diff(lam, P).subs(P, 0)
            )
        ),

        "metric_trace_full": str(
            sp.factor(tr - 4 * P * lam)
        ),

        "X_equation":
            "d_mu(FX^mu_nu - lambda *FY^mu_nu) = JX^nu",

        "Y_equation":
            "d_mu(FY^mu_nu - lambda *FX^mu_nu) = 0 "
            "(no microscopic Y charge)",

        "source_scalar_equation":
            "D_mu[exp(2sigma) D^mu psi]"
            "-exp(4sigma) U'(abs(psi)^2) psi=0",

        "source_X_current":
            "JX^nu=-2 sum_i q_i exp(2sigma) "
            "Im(conj(psi_i) D^nu psi_i)",

        "leading_Y_order":
            "O(alpha), conditional regular source-only branch",

        "leading_P_order":
            "O(alpha)",

        "leading_sigma_order":
            "O(alpha^2) for finite fixed beta",

        "leading_X_source_reciprocal_correction":
            "O(alpha^2) source-only; Earth/support "
            "traces may enter Y at O(alpha)",

        "universal_neutral_trace":
            "lambda_total(P=0)=alpha*"
            "(T_source+T_neutral+T_support) "
            "for universally coupled sectors",

        "integrability_null":
            "lambda=F(A0) implies "
            "grad(lambda) cross grad(A0)=0",

        "constant_lambda_null":
            "constant mixed Pontryagin coefficient "
            "has no local bulk source "
            "(smooth Abelian fields)",

        "parity_null":
            "alpha=0 has no linear Y seed at FY=0",

        "conditional_exterior":
            "if EX,BY = O(r^-3), "
            "P=O(r^-6), grad(sigma)=O(r^-7)",

        "local_reduced_kinetic": {
            key: str(value)
            for key, value in kin.items()
        },

        "local_negative_example": str(
            kin["schur"].subs({
                B: 1,
                v: 1,
                U: 0,
                alpha: 0,
                beta: 1,
            })
        ),

        "symbolic_checks": {
            key: "PASS_EXACT" if ok else "FAIL"
            for key, ok in exact_checks().items()
        },

        "full_constrained_kinetic": "NOT_DERIVED",
        "physical_earth_craft_force": "NOT_DERIVED",
    }
