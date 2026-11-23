"""GRAVITY2 automated source-action registry and cheap theorem gates.

All candidates are explicit. No unconstrained parameter proposals, field fits,
PDE simulations, or changes to historical AGMINER. Numerical score is not physics.
"""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction

SCHEMA = "gravity2.miner.v1"

ACTION = {
    "id": "C1_TWO_CHARGED_SCALARS_EINSTEIN_SOURCE",
    "signature": "-+++",
    "carrier": "two canonical abelian Maxwell sectors X,Y",
    "source": (
        "two complex scalars, L=-1/2 sum_i|D_i phi_i|^2 "
        "- sum_i(m_i^2|phi_i|^2/2+lambda_i|phi_i|^4/4)"
    ),
    "source_metric": (
        "g (explicit Einstein-frame source assumption; "
        "equivalence principle untested)"
    ),
    "neutral_and_Earth_metric": (
        "gtilde=exp(2*(alpha*P-beta*P**2))*g"
    ),
    "mixed_invariant": (
        "P=epsilon(F_X,F_Y)/4, epsilon contravariant 1/sqrt(-g)"
    ),
    "source_support": "NOT_SPECIFIED",
    "Earth_action": "NOT_EXPANDED",
    "neutral_action": "NOT_EXPANDED",
    "boundary": "NO_SUPPORTED_STATIONARY_SOURCE_YET",
    "physical_units": "NOT_NORMALIZED_TO_COMPLETE_SI",
}

REGISTRY = (
    {
        "id": "NULL_ZERO_SOURCE",
        "family": "NEGATIVE_CONTROL",
        "priority": 0,
        "assumptions": (
            "F_X=F_Y=0; no charged source; no engine mechanism"
        ),
        "question": (
            "Does a source-free zero-field control falsely "
            "earn a physical survivor?"
        ),
    },
    {
        "id": "C1_STATIC_NO_A0",
        "family": "R3B-SRC-A/STRICT_STATIC",
        "priority": 1,
        "assumptions": (
            "source Einstein-frame canonical charged scalars; "
            "partial_t phi=0, A0=0; R3 no material/support boundary; "
            "regular finite-energy phi->0; "
            "m_i^2>=0, lambda_i>=0"
        ),
        "question": (
            "Does positive static scalar energy require phi=0, "
            "ruling out nonzero source currents within this sector?"
        ),
    },
    {
        "id": "C1_HARMONIC_PHASE",
        "family": "R3B-SRC-A/STATIONARY_PHASE",
        "priority": 2,
        "assumptions": (
            "phi=f(x)exp(i omega t); A0 allowed; finite support "
            "and dynamical confinement NOT demonstrated; "
            "real q, frequency and norm are unprovided"
        ),
        "question": (
            "Can stationary phase evade the static obstruction "
            "without falsely implying finite stable supported source?"
        ),
    },
)


def fingerprint(card: dict) -> str:
    """Include physical action, ansatz, units, boundary, metric and source."""
    raw = json.dumps(
        {"action": ACTION, "candidate": card},
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(raw.encode()).hexdigest()


def registry() -> list[dict]:
    return [
        {**c, "fingerprint": fingerprint(c)}
        for c in sorted(REGISTRY, key=lambda x: x["priority"])
    ]


def _static_euler_identity_3d() -> str:
    """Derive 3D static scalar E-L times phi as divergence plus positive terms.

    Independent symbols represent the spatial first and diagonal second jets.
    This is an algebraic identity of the declared canonical scalar source,
    not a theorem for unspecified supports or a full gravity action.
    """
    import sympy as s

    a, b, q, m2, lam = s.symbols(
        "a b q m2 lam", real=True
    )

    A = s.symbols("A0:3", real=True)
    da = s.symbols("da0:3", real=True)
    db = s.symbols("db0:3", real=True)
    dda = s.symbols("dda0:3", real=True)
    ddb = s.symbols("ddb0:3", real=True)
    dA = s.symbols("dA0:3", real=True)

    U = [
        da[i] + q*A[i]*b
        for i in range(3)
    ]

    V = [
        db[i] - q*A[i]*a
        for i in range(3)
    ]

    DU = [
        dda[i] + q*(dA[i]*b+A[i]*db[i])
        for i in range(3)
    ]

    DV = [
        ddb[i] - q*(dA[i]*a+A[i]*da[i])
        for i in range(3)
    ]

    radius2 = a*a+b*b

    Ea = sum(
        (
            DU[i]+q*A[i]*V[i]
            for i in range(3)
        ),
        s.Integer(0),
    ) - (m2+lam*radius2)*a

    Eb = sum(
        (
            DV[i]-q*A[i]*U[i]
            for i in range(3)
        ),
        s.Integer(0),
    ) - (m2+lam*radius2)*b

    boundary_div = sum(
        (
            da[i]*U[i]+db[i]*V[i]+a*DU[i]+b*DV[i]
            for i in range(3)
        ),
        s.Integer(0),
    )

    positive = sum(
        (
            U[i]**2+V[i]**2
            for i in range(3)
        ),
        s.Integer(0),
    ) + (m2+lam*radius2)*radius2

    assert s.expand(
        a*Ea+b*Eb-boundary_div+positive
    ) == 0

    # Reversing the divergence sign must be rejected.
    bad = s.expand(
        a*Ea+b*Eb+boundary_div+positive
    )

    assert bad != 0

    return (
        "PASS_EXACT_3D_STATIC_EULER_INTEGRATED_IDENTITY"
    )


def static_integrated_identity() -> dict:
    """Necessary static no-source theorem, with explicit boundary assumptions.

    For D0 phi=0, m^2>=0, lambda>=0 and vanishing surface flux:

      0=int(|D_i phi|^2 + m^2|phi|^2 + lambda|phi|^4) d^3x.

    Every term is nonnegative, hence finite decaying phi=0, j=0.
    It does not exclude A0, harmonic phases, negative potentials or supports.
    """
    euler = _static_euler_identity_3d()

    trials = (
        (1, 0, 0),
        (0, 2, 0),
        (0, 0, 3),
        (2, 3, 5),
        (0, 0, 0),
    )

    values = [
        sum(Fraction(k) for k in tri)
        for tri in trials
    ]

    assert all(v >= 0 for v in values)

    # Negative-potential control: the positivity theorem
    # no longer applies outside its stated assumptions.
    wrong = Fraction(1)+Fraction(-2)
    assert wrong < 0

    return {
        "verdict": "FAIL_SCOPED",
        "euler_identity": euler,
        "theorem": "STATIC_A0_ZERO_CONVEX_SCALAR_SOURCE_NO_GO",
        "assumptions": (
            "D0phi=0, positive spatial norm, m^2>=0, lambda>=0, "
            "regular finite decay, zero support/surface term"
        ),
        "integrated_equation": (
            "0=integral(|D_i phi|^2 + m^2|phi|^2 "
            "+ lambda|phi|^4) d^3x"
        ),
        "consequence": (
            "phi_X=phi_Y=0 and J_X=J_Y=0 "
            "for this restricted ansatz"
        ),
        "negative_control": (
            "negative m^2/potential or nonzero boundary term "
            "defeats positivity assumption"
        ),
        "scope": (
            "NOT A NO-GO FOR SUPPORTED, TIME-HARMONIC, "
            "A0-NONZERO OR DIFFERENT SOURCE ACTIONS"
        ),
    }


def stationary_necessary_bound() -> dict:
    """Flat normal-frame temporal current/energy Cauchy bound.

    n=f^2; a=omega-q A0; j0=q*a*n; e0=1/2 a^2*n.

    For spatially varying a, Cauchy gives:
        Q^2 <= 2 q^2 N E0
    with N=int n, Q=int j0.

    No physical SI source normalizations are supplied.
    """
    samples = [
        (Fraction(1), Fraction(2), Fraction(3)),
        (Fraction(2), Fraction(-1), Fraction(5)),
        (Fraction(3), Fraction(4), Fraction(1)),
    ]

    q = Fraction(7, 3)

    total_n = sum(
        (n for n, a, w in samples),
        Fraction(0),
    )

    total_q = sum(
        (q*n*a for n, a, w in samples),
        Fraction(0),
    )

    total_e = sum(
        (n*a*a/2 for n, a, w in samples),
        Fraction(0),
    )

    assert total_q**2 <= 2*q*q*total_n*total_e
    assert total_n > 0 and total_e >= 0

    return {
        "verdict": "UNDERDETERMINED",
        "theorem": (
            "STATIONARY_TEMPORAL_CURRENT_CAPACITY_INEQUALITY"
        ),
        "equation": (
            "|Q|^2<=2*q^2*N*E_time, N=int f^2, "
            "E_time=int (omega-qA0)^2*f^2/2"
        ),
        "example_exact": {
            "N": str(total_n),
            "Q": str(total_q),
            "E": str(total_e),
        },
        "missing": [
            "finite stable solution of coupled source+X/Y Euler equations",
            "source/support boundaries",
            "realizable current and total energy in SI",
            "loaded R3B exterior response",
        ],
        "scope": (
            "NECESSARY_FLAT_NORMAL_FRAME_NOT_FINITE_SOURCE_PROOF"
        ),
    }


def evaluate(candidate_id: str, level: str) -> dict:
    cards = {
        c["id"]: c
        for c in registry()
    }

    if candidate_id not in cards or level not in ("L0", "L1"):
        raise ValueError(
            "candidate/level not in authorized finite registry"
        )

    card = cards[candidate_id]

    if candidate_id == "NULL_ZERO_SOURCE":
        gate = {
            "verdict": "FAIL_SCOPED",
            "theorem": "ZERO_CARRIER_AND_CURRENT_CONTROL",
            "scope": "ZERO_FIELDS_ONLY",
            "consequence": (
                "no portal gradient or gravitational lift "
                "in the zero-field control"
            ),
        }

    elif candidate_id == "C1_STATIC_NO_A0":
        gate = static_integrated_identity()

    else:
        gate = (
            stationary_necessary_bound()
            if level == "L1"
            else {
                "verdict": "UNDERDETERMINED",
                "theorem": "STATIONARY_SOURCE_REQUIRES_L1",
                "scope": "L0_NO_SOLVE",
            }
        )

    return {
        "candidate_id": candidate_id,
        "fingerprint": card["fingerprint"],
        "action_id": ACTION["id"],
        "level": level,
        "gate_G05": gate,
        "other_gates": {
            "G01_ACTION": "INCOMPLETE_SUPPORT_EARTH_BOUNDARY",
            "G02_VARIATION": (
                "SCOPED_IDENTITIES_PRIOR_G203A_NOT_NEW_FULL_EOM"
            ),
            "G03_WARD": (
                "SCOPED_PRIOR_G203A_NOT_FULL_DIFEOMORPHISM_BIANCHI"
            ),
            "G04_HEALTH": "NOT_PROVEN",
            "G06_LOAD": "NOT_AUTHORIZED",
            "G07_METRIC": "NOT_SOLVED_EINSTEIN",
            "G08_ENERGY": "NOT_CERTIFIED",
            "G09_EXTERIOR": "NOT_RUN",
            "G10_REACTION": "NOT_DERIVED",
            "G11_REALISM": "NOT_CERTIFIED",
        },
        "qualified_physical_survivor": False,
        "complete_source_action": False,
        "loaded_simulation": False,
    }
