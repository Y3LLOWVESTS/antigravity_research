"""GRAVITY2-02 bounded R3B source-action atlas.

Source-action templates are hypotheses, not certified mechanisms.
No historical AGMINER module is imported or executed.
"""
from __future__ import annotations

import sympy as sp
from pathlib import Path

from .action01_core import read_pinned
from .engine import digest

G01_ID = "g201_20261121T041450Z_f4c901cc"
G01_SCIENCE_SHA = (
    "e1d3012279be440b8b021cc9cf52505e90c317263dc42a43c64133a4baa2720f"
)
G01_VERIFY_SHA = (
    "4ae76fd26c41278519ceebb38a86585e45a4a4149a45b8edf2362019cb15d74f"
)

CANDIDATES = (
    {
        "id": "C0_SOURCE_FREE_CONTROL",
        "family": "TWO_U1_NO_CHARGED_SOURCE",
        "definition": (
            "Einstein-Hilbert + canonical Maxwell X/Y + "
            "universal conformal neutral-matter portal"
        ),
        "assumptions": (
            "Static regular all-space source-free fields; "
            "finite energy; no external boundary flux"
        ),
        "classification": "NEGATIVE_CONTROL_NO_FINITE_SOURCE",
        "sourceability": "NOT_ESTABLISHED",
    },
    {
        "id": "C1_TWO_CHARGED_SCALARS",
        "family": "LOCAL_U1X_U1Y_SCALAR_SOURCE",
        "definition": (
            "Einstein-Hilbert + two canonical Maxwell sectors "
            "+ two independently charged complex scalars "
            "+ universal conformal neutral-matter portal "
            "+ dynamical-support and Earth action slots"
        ),
        "assumptions": (
            "Canonical scalar kinetic terms; real charges; "
            "nonnegative mass and quartic parameters; "
            "support and Earth actions still unspecified"
        ),
        "classification":
            "FORMAL_COVARIANT_SOURCE_TEMPLATE_UNDERDETERMINED",
        "sourceability":
            "FINITE_STABLE_EQUILIBRIUM_NOT_DERIVED",
    },
    {
        "id": "C2_POINT_CHARGE_CONTROL",
        "family": "UNREGULARIZED_MAXWELL_POINT_SOURCE",
        "definition": (
            "Static 3D Maxwell point charges with zero "
            "core radius, no finite material regularization"
        ),
        "assumptions": (
            "Ordinary positive Maxwell energy; "
            "nonzero charge; zero core radius"
        ),
        "classification":
            "REJECT_INFINITE_SELF_ENERGY_UNDER_ASSUMPTIONS",
        "sourceability":
            "SINGULAR_ZERO_RADIUS_SOURCE",
    },
)


def symbolic_gate() -> dict:
    """Exact restricted algebra, not full Einstein field equations."""
    p, alpha, beta, trace = sp.symbols(
        "p alpha beta trace", real=True
    )
    sigma = alpha*p - beta*p*p
    sigma_p = sp.diff(sigma, p)
    coupling = sp.exp(4*sigma)*trace*sigma_p

    # P = Q/sqrt(-g) as a four-form density divided by volume.
    # A conformal variation g_ab -> (1+t) g_ab (4 dimensions)
    # gives P(t)=P/(1+t)^2 at fixed F_X,F_Y.
    t = sp.symbols("t", real=True)
    p_t = p/(1+t)**2
    scale = (1+t)*sp.exp(
        2*(sigma.subs(p,p_t)-sigma)
    )
    metric_trace = sp.simplify(
        sp.diff(scale,t).subs(t,0)
    )
    expected_metric = 1-4*p*sigma_p
    assert sp.simplify(
        metric_trace-expected_metric
    ) == 0

    # Mixed portal reciprocity:
    # grad(lambda) x grad(P) =
    # exp(4 sigma) sigma_P grad(T) x grad(P).
    gp = sp.Matrix(sp.symbols("gp0:3"))
    gt = sp.Matrix(sp.symbols("gt0:3"))
    grad_lambda = (
        sp.diff(coupling,p)*gp
        +sp.diff(coupling,trace)*gt
    )
    curl_residual = (
        grad_lambda.cross(gp)
        -sp.exp(4*sigma)*sigma_p*gt.cross(gp)
    )
    assert all(
        sp.simplify(v) == 0 for v in curl_residual
    )

    # Local U(1) charged-scalar gauge and Noether identity,
    # exactly in a one-coordinate restriction.
    a,b,da,db,A,q,m,quartic = sp.symbols(
        "a b da db A q m quartic", real=True
    )
    d2a,d2b,dA,theta,dtheta = sp.symbols(
        "d2a d2b dA theta dtheta", real=True
    )

    u = da + q*A*b
    v = db - q*A*a
    amplitude = a*a+b*b
    lagrangian = (
        -(u*u+v*v)/2
        -m*m*amplitude
        -quartic*amplitude*amplitude/2
    )

    # D=partial-iqA; infinitesimal:
    # delta psi=iq theta psi, delta A=partial theta.
    delta_u = (
        -q*(dtheta*b+theta*db)
        +q*dtheta*b
        +q*A*q*theta*a
    )
    delta_v = (
        q*(dtheta*a+theta*da)
        -q*dtheta*a
        +q*q*A*theta*b
    )
    gauge_kinetic = sp.simplify(
        2*u*delta_u+2*v*delta_v
    )
    gauge_potential = sp.simplify(
        2*a*(-q*theta*b)+2*b*(q*theta*a)
    )
    assert gauge_kinetic == 0
    assert gauge_potential == 0

    Du = d2a+q*(dA*b+A*db)
    Dv = d2b-q*(dA*a+A*da)

    # One-coordinate Euler derivatives. Other directions are
    # not inferred from this test.
    Ea = sp.diff(lagrangian,a)+Du
    Eb = sp.diff(lagrangian,b)+Dv
    current = -sp.diff(lagrangian,A)

    def total_derivative(z):
        return sp.expand(
            sp.diff(z,a)*da
            +sp.diff(z,b)*db
            +sp.diff(z,da)*d2a
            +sp.diff(z,db)*d2b
            +sp.diff(z,A)*dA
        )

    ward = sp.simplify(
        total_derivative(current)
        -q*(b*Ea-a*Eb)
    )
    assert ward == 0

    # Bare theta F_X wedge F_Y has no direct Hilbert
    # stress when theta is an independent fixed scalar.
    topological = sp.symbols("kappa theta Q")
    kappa, theta_symbol, Q = topological
    bare_variation = sp.diff(
        kappa*theta_symbol*Q,t
    )
    assert bare_variation == 0

    # Point-charge Maxwell energy is proportional to
    # integral_epsilon^R dr / r^2.
    eps,R = sp.symbols(
        "eps R", positive=True
    )
    point_integral = sp.integrate(
        1/sp.Symbol("r",positive=True)**2,
        (sp.Symbol("r",positive=True),eps,R)
    )
    assert sp.limit(
        point_integral,eps,0,dir="+"
    ) == sp.oo

    return {
        "portal_sigma": "alpha*p-beta*p**2",
        "portal_lambda":
            "exp(4*sigma)*trace*diff(sigma,p)",
        "metric_trace_factor":
            sp.sstr(metric_trace),
        "metric_variation_residual": "0",
        "transverse_reciprocity_residual": "0",
        "charged_scalar_gauge_variation": "0",
        "charged_scalar_one_coordinate_Ward_residual": "0",
        "bare_fixed_theta_direct_Hilbert_residual": "0",
        "point_charge_self_energy_limit": "POSITIVE_INFINITY",
        "scope": (
            "EXACT_SYMBOLIC_LOCAL_IDENTITY_CHECKS_ONLY; "
            "NO_FULL_GRAVITATIONAL_OR_CONSTRAINED_MODE_CLOSURE"
        ),
    }


def audit(root: Path) -> dict:
    g01 = (
        root/"results"/"gravity2"/"action01_runs"
        /G01_ID
    )
    parents = {
        "GRAVITY2_01_SCIENCE": {
            "path": str(
                (g01/"science.json").relative_to(root)
            ),
            "expected_sha256": G01_SCIENCE_SHA,
            "actual_sha256": (
                digest(g01/"science.json")
                if (g01/"science.json").is_file()
                else None
            ),
        },
        "GRAVITY2_01_VERIFICATION": {
            "path": str(
                (g01/"verification.json").relative_to(root)
            ),
            "expected_sha256": G01_VERIFY_SHA,
            "actual_sha256": (
                digest(g01/"verification.json")
                if (g01/"verification.json").is_file()
                else None
            ),
        },
    }

    pinned, _ = read_pinned(root)
    all_match = (
        all(
            p["actual_sha256"] == p["expected_sha256"]
            for p in parents.values()
        )
        and all(
            p["status"] == "MATCH"
            for p in pinned.values()
        )
    )

    if not all_match:
        return {
            "decision": "PARENT_HOLD",
            "parents": parents,
            "historical_files": pinned,
            "candidates": [],
            "gates": {"G00_PARENT":"HOLD"},
            "qualified_survivors": 0,
            "complete_action": "NOT_DERIVED",
        }

    algebra = symbolic_gate()

    return {
        "decision": "SCOPED_ACTION_TEMPLATE_ATLAS_NO_PROMOTION",
        "parents": parents,
        "historical_files": pinned,
        "candidates": list(CANDIDATES),
        "gates": {
            "G00_PARENT": "PASS_SCOPED",
            "G01_ACTION":
                "TEMPLATES_ONLY_NOT_COMPLETE_SOURCE_ACTION",
            "G02_VARIATION":
                "PARTIAL_EXACT_PORTAL_AND_SOURCE_VARIATION",
            "G03_WARD":
                "SCOPED_ONE_COORDINATE_U1_NOETHER_IDENTITY",
            "G04_HEALTH": "NOT_DERIVED_FULL_MODES",
            "G05_SOURCE": "FINITE_SOURCE_NOT_DERIVED",
            "G06_LOAD": "NOT_RUN",
            "G07_METRIC": "NOT_SOLVED",
            "G08_ENERGY": "COMPLETE_SI_NOT_CERTIFIED",
            "G09_EXTERIOR": "NOT_RUN",
            "G10_REACTION": "NOT_DERIVED",
            "G11_REALISM": "NOT_CERTIFIED",
        },
        "symbolic_identities": algebra,
        "source_action_template": {
            "Einstein":
                "S_EH[g]=M_Pl^2/2 integral sqrt(-g) R",
            "carriers":
                "integral sqrt(-g)*(-F_X^2/4-F_Y^2/4)",
            "charged_sources":
                "sum_i integral sqrt(-g)*(-|D_i Psi_i|^2"
                "-m_i^2|Psi_i|^2-lambda_i|Psi_i|^4/2)",
            "D_i": "nabla-i*q_i*A_i",
            "portal":
                "g_tilde=exp(2*sigma(P))*g; "
                "P=epsilon(F_X,F_Y)/(4*sqrt(-g))",
            "neutral_matter":
                "S_neutral[g_tilde,psi_n] UNEXPANDED",
            "Earth_matter":
                "S_Earth[g_tilde,psi_E] UNEXPANDED",
            "supports":
                "S_support[g,chi,Psi_X,Psi_Y] UNEXPANDED",
        },
        "unresolved": [
            "Exact reproduction of the original R3B field kernel",
            "Physically stable, compact current-carrying source",
            "Explicit source/support/Earth material actions",
            "All off-shell 4D metric and source variations",
            "Gauge constraints and full Lorentzian mode spectrum",
            "Reciprocal strong neutral-matter loading",
            "Finite continuum and exterior metric solution",
            "Earth-down and total spacecraft-up reaction",
            "Complete SI operating energy strictly below 10 MJ",
            "Empirical, quantum and UV consistency",
        ],
        "historical_R3B_capacity_J":
            1.5429162116460216,
        "historical_loaded_min_m_s2":
            -129.67185782242464,
        "historical_values":
            "PROVENANCE_ANCHORS_NOT_RECOMPUTED",
        "qualified_survivors": 0,
        "complete_action": "NOT_DERIVED",
        "physical_lift": "NOT_DERIVED",
        "complete_energy": "NOT_CERTIFIED",
        "full_regression": "NOT_RUN",
    }
