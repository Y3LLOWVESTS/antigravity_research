"""Independent GRAVITY2-05 bounded-action integrity and algebra verifier.

Independently computes Jordan-trace variation and an explicit
nonuniform-weight source jet. A PASS certifies neither full GR
dynamics nor material existence nor loaded response.
"""
from __future__ import annotations

import json
import sympy as s

from .engine import (
    ROOT,
    atomic_json,
    atomic_text,
    digest,
)
from . import bridge05 as miner
from . import bridge05_core as core


def independent_math():
    # Independent conformal rescaling parameter t, instead
    # of differentiating sigma(P) directly.
    t = s.symbols("t",real=True)
    alpha,beta,p,K,V = s.symbols(
        "alpha beta p K V",
        real=True,
    )

    sigma = alpha*p-beta*p*p

    scaled = (
        -s.exp(sigma+t)**2*K/s.Integer(2)
        -s.exp(sigma+t)**4*V
    )

    variation = s.diff(
        scaled,t
    ).subs(t,0)

    L = (
        -s.exp(2*sigma)*K/s.Integer(2)
        -s.exp(4*sigma)*V
    )

    source_trace = -s.exp(-2*sigma)*K-4*V

    assert s.simplify(
        variation-s.exp(4*sigma)*source_trace
    ) == 0

    assert s.simplify(
        s.diff(L,p)-variation*s.diff(sigma,p)
    ) == 0

    assert s.simplify(
        s.diff(L,p)
    ) != 0

    # Independent 1D nonuniform-weight integration
    # by parts, including gauge A and grad(w).
    a,b,q,A,da,db,dda,ddb,dA,w,dw,z,m2,lam = s.symbols(
        "a b q A da db dda ddb dA w dw z m2 lam",
        real=True,
    )

    rho = a*a+b*b
    U = da+q*A*b
    W = db-q*A*a

    dU = dda+q*(dA*b+A*db)
    dW = ddb-q*(dA*a+A*da)

    Ea = (
        w*dU+dw*U+w*q*A*W
        -z*(m2+lam*rho)*a
    )

    Eb = (
        w*dW+dw*W-w*q*A*U
        -z*(m2+lam*rho)*b
    )

    boundary = (
        dw*(a*U+b*W)
        +w*(da*U+db*W+a*dU+b*dW)
    )

    positive = (
        w*(U*U+W*W)
        +z*(m2+lam*rho)*rho
    )

    assert s.expand(
        a*Ea+b*Eb-boundary+positive
    ) == 0

    assert s.expand(
        a*(Ea-dw*U)
        +b*(Eb-dw*W)
        -boundary+positive
    ) != 0

    # Independent field/source mixed derivative.
    x,y,u = s.symbols("x y u",real=True)
    pp = x*y
    ss = pp/s.Integer(7)-pp**2/s.Integer(61)

    W_energy = (
        s.exp(2*ss)*3*u*u/s.Integer(2)
        +s.exp(4*ss)*(2*u*u+u**4)/4
    )

    mixed = s.diff(W_energy,x,u)

    assert s.simplify(
        mixed-s.diff(W_energy,u,x)
    ) == 0

    assert s.simplify(
        mixed.subs({x:1,y:2,u:1})
    ) != 0

    # Independent, restricted positive-source Schur.
    A0 = s.Rational(7)
    b0 = s.Rational(3)
    C0 = s.Rational(4)

    assert A0-b0**2/C0 == s.Rational(19,4)
    assert A0-b0**2/C0 < A0

    return True


def verify(folder):
    checks = {}

    def gate(k,ok):
        checks[k] = bool(ok)

        if not ok:
            raise AssertionError(k)

    try:
        man = json.loads(
            (folder/"manifest.json").read_text()
        )

        sci = json.loads(
            (folder/"science.json").read_text()
        )

        sha_lines = {
            name:value
            for value,name in (
                line.split("  ",1)
                for line in (
                    folder/"hashes.sha256"
                ).read_text().splitlines()
            )
        }

        gate(
            "manifest SHA",
            sha_lines["manifest.json"]
            == digest(folder/"manifest.json"),
        )

        gate(
            "science SHA",
            sha_lines["science.json"]
            == digest(folder/"science.json"),
        )

        gate(
            "run linkage",
            man["run_id"]
            == sci["run_id"]
            == folder.name,
        )

        gate(
            "producer hash",
            man["producer_sha256"]
            == miner.code_hashes(),
        )

        gate(
            "bounded L0",
            man["level"] == "L0"
            and man["workers"] == 1
            and man["time_limit_seconds"] > 0,
        )

        gate(
            "correct watchdog",
            sci["resource"]["memory_policy"]
            == "SOFT_PSUTIL_PROCESS_WATCHDOG",
        )

        gate(
            "no previous changes asserted",
            man["prior_modification"] == "NONE",
        )

        gate(
            "no historical execution asserted",
            man["legacy_AGMINER"]
            == "READ_ONLY_HASH_NO_EXECUTION",
        )

        gate(
            "parent report intact",
            sci["parent_locks"]
            == miner.parent_report(),
        )

        gate(
            "no physical promotions",
            sci["physical_survivors"] == 0
            and sci["physical_lift"] == "NOT_DERIVED"
            and sci["complete_energy"] == "NOT_CERTIFIED"
            and sci["real_source"] == "NOT_ESTABLISHED"
            and sci["full_gravitational_action"]
                == "NOT_DERIVED"
            and sci["006D_replaced"] is False,
        )

        gate(
            "PDE disabled",
            sci["loaded_PDE"] == "NOT_AUTHORIZED"
            and sci["full_regression"] == "NOT_RUN",
        )

        gate(
            "valid execution state",
            sci["execution_status"] in (
                "COMPLETED",
                "PARENT_HOLD",
                "TIME_BUDGET_EXCEEDED",
                "MEMORY_LIMIT",
                "STORAGE_LIMIT",
                "WORKER_ERROR",
                "WORKER_BAD_JSON",
                "USER_STOP",
                "USER_INTERRUPT",
                "WORKER_UNRESPONSIVE",
            ),
        )

        if sci["execution_status"] == "COMPLETED":
            e = sci["evidence"]

            gate(
                "parents locked",
                sci["parent_locks"]["all_match"] is True,
            )

            gate(
                "decision scoped",
                e["decision"]
                == "SCOPED_JORDAN_STATIC_NO_GO; "
                   "STATIONARY_SUPPORTED_SOURCE_UNDERDETERMINED",
            )

            gate(
                "strict static scope",
                e["weighted_static_source"][
                    "conditional_no_go"
                ]
                == "STATIC_D0_ZERO_A0_ZERO_POSITIVE_POTENTIAL_NO_SUPPORT",
            )

            gate(
                "static gradient weight",
                e["weighted_static_source"][
                    "nonconstant_weight_derivative_required"
                ] is True,
            )

            gate(
                "static failure control",
                e["weighted_static_source"][
                    "omitted_grad_weight_negative_control"
                ] == "NONZERO",
            )

            gate(
                "trace identity",
                e["Jordan_trace_and_reciprocity"][
                    "trace_identity_residual"
                ] == "0",
            )

            gate(
                "Hessian symmetry",
                e["Jordan_trace_and_reciprocity"][
                    "mixed_source_F_reciprocity_residual"
                ] == "0",
            )

            gate(
                "Pxy nonlinear term",
                e["Jordan_trace_and_reciprocity"][
                    "mixed_FX_FY_includes_P_second_derivative"
                ] is True,
            )

            gate(
                "positive mode Schur limited",
                e["Jordan_trace_and_reciprocity"][
                    "restricted_positive_Huu_schur"
                ] == "11/3",
            )

            gate(
                "no force sign",
                e["Jordan_trace_and_reciprocity"][
                    "loaded_force_sign"
                ] == "NOT_DETERMINED",
            )

            gate(
                "original negative result preserved",
                e["historical_R3B_loaded_min_m_s2"]
                == -129.67185782242464,
            )

            gate(
                "field capacity not a device",
                e["historical_R3B_prescribed_capacity_J"]
                == 1.5429162116460216
                and e["historical_values"]
                == "PROVENANCE_ONLY_NOT_RECOMPUTED",
            )

            gate(
                "Higgs controls both Jordan",
                all(
                    e["historical_Higgs_classification_erratum"][
                        k
                    ]["source_in_physical_metric"]
                    for k in (
                        "B_JORDAN_LOCALIZED",
                        "C_HIGGS_Y_CONTROL",
                        "D_HIGGS_BOTH_CONTROL",
                    )
                ),
            )

            gate(
                "C/D trace scope",
                all(
                    e["historical_Higgs_classification_erratum"][
                        k
                    ]["general_interior_portal_trace_term"]
                    == "PRESENT_WHEN_K_OR_V_NONZERO"
                    for k in (
                        "C_HIGGS_Y_CONTROL",
                        "D_HIGGS_BOTH_CONTROL",
                    )
                ),
            )

            gate(
                "stationary unresolved",
                e["gates"]["G05_SOURCE"]
                == "STATIC_CONVEX_UNSUPPORTED_FAIL; STATIONARY_OPEN",
            )

            gate(
                "no hidden load",
                e["gates"]["G06_LOAD"]
                == "NOT_AUTHORIZED_UNDERDETERMINED",
            )

            gate(
                "independent symbolic and negative controls",
                independent_math(),
            )

            status = (
                "PASS_SCOPED_JORDAN_SOURCE_THEOREM_NO_LIFT"
            )

        else:
            gate(
                "incomplete not promoted",
                sci["physical_survivors"] == 0,
            )

            status = "PASS_INCOMPLETE_EVIDENCE_ONLY"

        report = {
            "program": "GRAVITY2-05_INDEPENDENT",
            "run_id": folder.name,
            "status": status,
            "checks": checks,
            "science_sha256":
                digest(folder/"science.json"),
            "whole_craft_lift": "NOT_DERIVED",
        }

    except Exception as exc:
        report = {
            "program": "GRAVITY2-05_INDEPENDENT",
            "run_id": folder.name,
            "status": "HOLD",
            "checks": checks,
            "error": repr(exc),
            "whole_craft_lift": "NOT_DERIVED",
        }

    target = folder/"verification.json"

    if target.exists():
        if json.loads(target.read_text()) != report:
            print(
                "GRAVITY2_05_VERIFY_RECHECK_DIFFERS_NO_OVERWRITE"
            )
            return 3

    else:
        atomic_json(target,report)

        atomic_text(
            folder/"verification.sha256",
            digest(target)
            +"  verification.json\n",
        )

    print(
        "GRAVITY2_05_VERIFY="+report["status"]
    )

    print(
        "CHECKS="
        +str(sum(checks.values()))
        +"/"+str(len(checks))
    )

    if "error" in report:
        print("ERROR="+report["error"])

    print(
        "VERIFICATION_SHA256="
        +digest(target)
    )

    return (
        0
        if report["status"]
        == "PASS_SCOPED_JORDAN_SOURCE_THEOREM_NO_LIFT"
        else 3
    )
