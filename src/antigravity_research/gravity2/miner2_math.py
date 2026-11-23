"""GRAVITY2-04 covariant source-frame preflight: scoped exact algebra.

Two source-action families: original Einstein-frame charged matter, and
universally coupled Jordan-frame charged matter. A symmetry-breaking potential
is a separate vacuum operator control. No Einstein solution or sourced lift.
"""
from __future__ import annotations

import hashlib
import json

ACTION_COMMON = {
    "metric_signature": "-+++",
    "carriers": "two canonical U(1) Maxwell kinetic terms in Einstein frame",
    "portal": "gtilde=exp(2sigma(P))*g; sigma=alpha*P-beta*P**2",
    "mixed_invariant":
        "P=(1/4)epsilon^{munurhosigma} FX_munu FY_rhosigma",
    "source_charges": [[1, 0], [0, 1]],
    "source_kinetic":
        "-1/2 sum_i g_source^{mu nu} (Dmu ai Dnu ai + Dmu bi Dnu bi)",
    "Earth_neutral": "unexpanded universal Jordan-metric matter actions",
    "supports": "UNSPECIFIED",
    "R3B_loaded_kernel":
        "NOT_REUSABLE_WITHOUT_NEW_SECOND_VARIATION",
    "units": "CANONICAL_FORMAL_NOT_COMPLETE_SI",
}

# Operator/frame choices, not numerical parameter optimization.
SEEDS = (
    ("A_EINSTEIN_LOCALIZED", "EINSTEIN", "CONVEX", (0, 0)),
    ("B_JORDAN_LOCALIZED", "JORDAN", "CONVEX", (0, 0)),
    ("C_HIGGS_Y_CONTROL", "JORDAN", "BROKEN", (0, 1)),
    ("D_HIGGS_BOTH_CONTROL", "JORDAN", "BROKEN", (1, 1)),
)

HISTORICAL_EXCLUSIONS = (
    "PH12 gauged Q-ball finite source not certified, not rerun",
    "PH13 coupled Schur mode failed, not reopened",
    "PH15 P6-P7 winding stability failed, not reopened",
    "R3B original loaded response -129.67185782242464 m/s^2 not rerun",
)


def registry():
    records = []

    for cid, frame, potential, vev in SEEDS:
        action = {
            **ACTION_COMMON,
            "source_metric":
                "g" if frame == "EINSTEIN" else "gtilde",
            "source_potential": (
                "m2*f2/2+lambda*f2**2/4, m2>=0,lambda>=0"
                if potential == "CONVEX"
                else "sum_i kappa_i*(f2_i-v2_i)**2/4; "
                     "kappa_i>0, v2_i=exterior_source_vevs[i]"
            ),
            "exterior_source_vevs": list(vev),
        }

        payload = json.dumps(
            action,
            sort_keys=True,
            separators=(",", ":"),
        )

        records.append({
            "id": cid,
            "frame": frame,
            "potential": potential,
            "vev": list(vev),
            "action": action,
            "fingerprint":
                hashlib.sha256(payload.encode()).hexdigest(),
            "family":
                "R3B-SRC-A"
                if potential == "CONVEX"
                else "BROKEN_VACUUM_NEGATIVE_CONTROL",
            "qualification": "EXACT_PREFLIGHT_ONLY",
        })

    if len({
        r["fingerprint"] for r in records
    }) != len(records):
        raise ValueError(
            "duplicate generated action fingerprint"
        )

    return records


def identities():
    import sympy as s

    p, alpha, beta, k, v = s.symbols(
        "p alpha beta k v", real=True
    )

    sig = alpha*p-beta*p*p
    dsig = s.diff(sig, p)

    # Source density divided by sqrt(-g), at fixed g and Dpsi.
    lj = -s.exp(2*sig)*k/s.Integer(2) - s.exp(4*sig)*v
    le = -k/s.Integer(2)-v

    jordan_trace = -s.exp(-2*sig)*k-4*v
    extra = s.exp(4*sig)*jordan_trace*dsig

    assert s.simplify(s.diff(lj, p)-extra) == 0
    assert s.diff(le, p) == 0
    assert s.simplify(extra) != 0

    # Omitting the Jordan source trace changes the equations.
    assert s.simplify(
        s.diff(lj, p)-s.diff(le, p)
    ) != 0

    # Four-coordinate off-shell charged scalar identity.
    # w(x) accounts for an arbitrary conformal kinetic weight.
    a,b,q,w,z,m2,lam = s.symbols(
        "a b q w z m2 lam", real=True
    )

    A = s.symbols("A0:4")
    da = s.symbols("da0:4")
    db = s.symbols("db0:4")
    d2a = s.symbols("d2a0:4")
    d2b = s.symbols("d2b0:4")
    dA = s.symbols("dA0:4")
    dw = s.symbols("dw0:4")

    sign = (-1,1,1,1)

    U = [da[i]+q*A[i]*b for i in range(4)]
    V = [db[i]-q*A[i]*a for i in range(4)]

    DU = [
        d2a[i]+q*(dA[i]*b+A[i]*db[i])
        for i in range(4)
    ]

    DV = [
        d2b[i]-q*(dA[i]*a+A[i]*da[i])
        for i in range(4)
    ]

    potential = z*(
        m2*(a*a+b*b)/2
        +lam*(a*a+b*b)**2/4
    )

    ea = sum(
        sign[i]*(
            w*DU[i]+dw[i]*U[i]+w*q*A[i]*V[i]
        )
        for i in range(4)
    )-s.diff(potential,a)

    eb = sum(
        sign[i]*(
            w*DV[i]+dw[i]*V[i]-w*q*A[i]*U[i]
        )
        for i in range(4)
    )-s.diff(potential,b)

    divj = q*sum(
        sign[i]*(
            dw[i]*(b*U[i]-a*V[i])
            +w*(
                db[i]*U[i]+b*DU[i]
                -da[i]*V[i]-a*DV[i]
            )
        )
        for i in range(4)
    )

    assert s.expand(
        divj-q*(b*ea-a*eb)
    ) == 0

    # Wrong-sign Ward equation must fail.
    assert s.expand(
        divj+q*(b*ea-a*eb)
    ) != 0

    return {
        "source_trace_P_variation":
            "dL_J/dP=e^(4sigma)*Ttilde_source*sigma_P",
        "source_trace":
            "Ttilde_source=-e^(-2sigma)*K-4V",
        "Einstein_source_direct_P_variation": "ZERO",
        "Jordan_source_extra_P_variation": "NONZERO_GENERAL",
        "4D_source_Ward_with_variable_conformal_weight":
            "ZERO_OFF_SHELL",
        "reversed_Ward_sign_control": "NONZERO",
        "omitted_source_trace_control": "NONZERO",
        "scope":
            "EXACT_FORMAL_SOURCE_SECTOR; NOT_FULL_EINSTEIN_ACTION",
    }


def evaluate(card):
    import sympy as s

    if card not in registry():
        raise ValueError(
            "candidate not generated by pinned grammar"
        )

    q = s.Matrix(ACTION_COMMON["source_charges"])
    vevs = card["vev"]

    # At exterior P=0 and a constant scalar vacuum,
    # Higgs mass matrix is proportional to Q^T diag(v_i^2) Q.
    mass = q.T*s.diag(*vevs)*q
    rank = mass.rank()

    assert rank in (0,1,2)
    assert all(e >= 0 for e in mass.eigenvals())

    if card["potential"] == "CONVEX":
        assert vevs == [0,0]
        decision = (
            "ACTION_COMPARISON_UNDERDETERMINED_SOURCE_SUPPORT"
        )
        novel = card["frame"] == "JORDAN"

    elif rank == 2:
        decision = (
            "SCOPED_NO_UNBROKEN_U1_FOR_BOTH_EXTERIOR_VEVS"
        )
        novel = False

    else:
        decision = (
            "ONE_EXTERIOR_CARRIER_HIGGSED_OTHER_UNBROKEN"
        )
        novel = False

    return {
        "id": card["id"],
        "fingerprint": card["fingerprint"],
        "decision": decision,
        "charge_matrix": [
            [int(q[i,j]) for j in range(2)]
            for i in range(2)
        ],
        "exterior_gauge_mass_matrix": [
            [str(mass[i,j]) for j in range(2)]
            for i in range(2)
        ],
        "exterior_mass_rank": rank,
        "massless_U1_count": 2-rank,
        "source_in_physical_metric":
            card["frame"] == "JORDAN",
        "changes_portal_source_loading": novel,
        "necessary_identity_checks": identities(),
        "exterior_higgs_scope":
            "EXTERIOR_CONSTANT_VEV_ONLY; "
            "INTERIOR_CONDENSATE_NOT_EXCLUDED",
        "qualified_physical_survivor": False,
        "source_finite_stable": "NOT_ESTABLISHED",
        "supports_Earth_neutral_EOM": "NOT_DERIVED",
        "R3B_coupled_loaded_solve": "NOT_AUTHORIZED",
        "GR_energy": "NOT_CERTIFIED",
        "Einstein_gravity": "NOT_SOLVED",
        "physical_lift": "NOT_DERIVED",
    }
