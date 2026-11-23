"""Independent four-dimensional GRAVITY2-03A verifier.

Reconstructs the source Ward and metric/Hodge variation
using different symbolic configurations.
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
from .action01_core import read_pinned
from .bridge03a import (
    sha_sources,
    PARENT_SCIENCE,
    PARENT_VERIFY,
)


def verify(directory):
    checks = {}

    def check(label, ok):
        checks[label] = bool(ok)

        if not ok:
            raise AssertionError(label)

    try:
        manifest = json.loads(
            (directory / "manifest.json").read_text()
        )
        science = json.loads(
            (directory / "science.json").read_text()
        )

        recorded = dict(
            line.split("  ", 1)[::-1]
            for line in (
                directory / "hashes.sha256"
            ).read_text().splitlines()
        )

        check(
            "manifest SHA",
            recorded["manifest.json"]
            == digest(directory / "manifest.json"),
        )
        check(
            "science SHA",
            recorded["science.json"]
            == digest(directory / "science.json"),
        )
        check(
            "run association",
            manifest["run_id"]
            == science["run_id"]
            == directory.name,
        )
        check(
            "producer SHA",
            manifest["producer_sha256"] == sha_sources(),
        )
        check(
            "L0 single worker",
            manifest["level"] == "L0"
            and manifest["workers"] == 1,
        )
        check(
            "legacy miner not executed",
            manifest["legacy_AGMINER_access"]
            == "READ_ONLY_SHA_NO_IMPORT",
        )
        check(
            "no physical promotion",
            science["qualified_survivors"] == 0
            and science["complete_action"] == "NOT_DERIVED"
            and science["physical_lift"] == "NOT_DERIVED"
            and science["complete_energy"] == "NOT_CERTIFIED"
            and science["006D_replaced"] is False,
        )
        check(
            "full regression not claimed",
            science["full_regression"] == "NOT_RUN",
        )
        check(
            "resource limit described accurately",
            science["resource"]["monitor_kind"]
            == "SOFT_WATCHDOG",
        )
        check(
            "valid execution state",
            science["execution_status"] in (
                "COMPLETED",
                "TIME_BUDGET_EXCEEDED",
                "WORKER_BAD_JSON",
                "WORKER_ERROR",
                "MEMORY_SOFT_LIMIT",
                "DISK_SOFT_LIMIT",
                "INTERRUPTED",
            ),
        )

        if science["execution_status"] == "COMPLETED":
            evidence = science["evidence"]
            algebra = evidence["derived"]

            check(
                "loaded solver precondition",
                evidence["decision"]
                == "BLOCKED_FOR_LOADED_SOLVER_"
                   "INCOMPLETE_SOURCE_SUPPORT_AND_EARTH_ACTION",
            )
            check(
                "G01 action remains incomplete",
                evidence["gates"]["G01_ACTION"]
                == "ACTION_INCOMPLETE_SUPPORT_EARTH_BOUNDARY",
            )
            check(
                "loaded computation not authorized",
                evidence["loaded_PDE_executed"] is False
                and "NOT_AUTHORIZED"
                in evidence["gates"]["G06_LOAD"],
            )
            check(
                "C1 not a physical survivor",
                evidence["qualified_survivors"] == 0
                and evidence["candidate_status"]
                == "FORMAL_COVARIANT_SECTOR_NOT_REALIZED_SOURCE",
            )
            check(
                "historical negative control",
                evidence[
                    "original_R3B_historical_loaded_min_m_s2"
                ] == -129.67185782242464,
            )
            check(
                "capacity not operating energy",
                evidence["original_R3B_prescribed_capacity_J"]
                == 1.5429162116460216
                and evidence["historical_values"]
                == "REFERENCE_ONLY_NOT_RECOMPUTED",
            )

            for label, parent in evidence["parent_locks"].items():
                path = ROOT / parent["relative_path"]

                check(
                    "parent SHA " + label,
                    path.is_file()
                    and digest(path)
                    == parent["expected_sha256"]
                    and parent["actual_sha256"]
                    == parent["expected_sha256"],
                )

            check(
                "G02 science pinned",
                evidence["parent_locks"]["G02_SCIENCE"][
                    "expected_sha256"
                ] == PARENT_SCIENCE,
            )
            check(
                "G02 verification pinned",
                evidence["parent_locks"]["G02_VERIFICATION"][
                    "expected_sha256"
                ] == PARENT_VERIFY,
            )

            historic, _ = read_pinned(ROOT)

            for label, item in historic.items():
                check(
                    "historical SHA " + label,
                    item["status"] == "MATCH"
                    and evidence["historical_locks"][label][
                        "actual_sha256"
                    ] == item["actual_sha256"],
                )

            # Independent 4D charged-source Ward derivation.
            a, b, q = s.symbols("a b q")

            A = s.symbols("K0:4")
            da = s.symbols("Ua0:4")
            db = s.symbols("Ub0:4")

            a2 = s.symbols("Haa0:4")
            b2 = s.symbols("Hbb0:4")
            dA = s.symbols("dK0:4")

            signs = (-1, 1, 1, 1)

            U = [
                da[k] + q*A[k]*b
                for k in range(4)
            ]

            V = [
                db[k] - q*A[k]*a
                for k in range(4)
            ]

            DU = [
                a2[k] + q*(dA[k]*b+A[k]*db[k])
                for k in range(4)
            ]

            DV = [
                b2[k] - q*(dA[k]*a+A[k]*da[k])
                for k in range(4)
            ]

            Ea = sum(
                signs[k]*(DU[k]+q*A[k]*V[k])
                for k in range(4)
            )

            Eb = sum(
                signs[k]*(DV[k]-q*A[k]*U[k])
                for k in range(4)
            )

            divj = q*sum(
                signs[k]*(
                    db[k]*U[k]
                    + b*DU[k]
                    - da[k]*V[k]
                    - a*DV[k]
                )
                for k in range(4)
            )

            check(
                "independent 4D offshell Ward",
                s.expand(
                    divj-q*(b*Ea-a*Eb)
                ) == 0,
            )
            check(
                "wrong Ward sign rejected",
                s.expand(
                    divj+q*(b*Ea-a*Eb)
                ) != 0,
            )
            check(
                "both U1 sectors reported",
                algebra["source_ward"] == {
                    "X":
                        "ZERO_OFF_SHELL_FULL_4D_SOURCE_JET",
                    "Y":
                        "ZERO_OFF_SHELL_FULL_4D_SOURCE_JET",
                },
            )

            # Independent metric/Hodge variation with
            # different metric perturbation, source stress,
            # alpha and beta from the producer.
            t = s.symbols("t")
            eta = s.diag(-1, 1, 1, 1)

            H = s.Matrix([
                [0, s.Rational(1, 3), 0, 0],
                [s.Rational(1, 3), s.Rational(1, 7), 0, 0],
                [0, 0, s.Rational(1, 13), 0],
                [0, 0, 0, s.Rational(1, 5)],
            ])

            g = eta + t*H
            p0 = s.Integer(2)

            alpha = s.Rational(1, 47)
            beta = s.Rational(1, 131)

            def sigma(p):
                return alpha*p-beta*p*p

            p = p0/s.sqrt(-g.det())

            T = s.diag(
                3,
                s.Rational(2, 5),
                s.Rational(3, 7),
                s.Rational(4, 9),
            )

            T[0, 1] = s.Rational(1, 6)
            T[1, 0] = s.Rational(1, 6)

            dgt = (
                s.exp(2*sigma(p))*g
            ).diff(t).subs(t, 0)

            direct = (
                s.Rational(1, 2)
                * s.exp(4*sigma(p0))
                * sum(
                    T[i, j]*dgt[i, j]
                    for i in range(4)
                    for j in range(4)
                )
            )

            tr = s.exp(2*sigma(p0))*sum(
                eta[i, j]*T[i, j]
                for i in range(4)
                for j in range(4)
            )

            predicted = s.Rational(1, 2)*sum(
                (
                    s.exp(6*sigma(p0))*T[i, j]
                    - s.exp(4*sigma(p0))
                    * p0
                    * (alpha-2*beta*p0)
                    * tr
                    * eta[i, j]
                )*H[i, j]
                for i in range(4)
                for j in range(4)
            )

            wrong = (
                s.Rational(1, 2)
                * s.exp(6*sigma(p0))
                * sum(
                    T[i, j]*H[i, j]
                    for i in range(4)
                    for j in range(4)
                )
            )

            check(
                "independent metric/Hodge variation",
                s.simplify(direct-predicted) == 0,
            )
            check(
                "wrong fixed-P metric rejected",
                s.simplify(direct-wrong) != 0,
            )
            check(
                "reported metric variation residual",
                algebra[
                    "metric_Hodge_chain_variation_residual"
                ] == "0"
                and algebra[
                    "wrong_no_Hodge_negative_control"
                ] == "NONZERO",
            )
            check(
                "no complete Einstein/Bianchi promotion",
                evidence[
                    "Einstein_and_diffeomorphism_Bianchi"
                ] == "NOT_FULLY_DERIVED",
            )

            status = (
                "PASS_SCOPED_4D_IDENTITY_AND_PRECONDITION_BLOCK"
            )

        else:
            check(
                "interrupted run not promoted",
                science["qualified_survivors"] == 0,
            )
            status = "PASS_INCOMPLETE_EVIDENCE_ONLY"

        result = {
            "program": "GRAVITY2-03A-INDEPENDENT",
            "run_id": directory.name,
            "status": status,
            "checks": checks,
            "science_sha256":
                digest(directory / "science.json"),
            "full_action": "NOT_DERIVED",
            "physical_lift": "NOT_DERIVED",
        }

    except Exception as exc:
        result = {
            "program": "GRAVITY2-03A-INDEPENDENT",
            "run_id": directory.name,
            "status": "HOLD",
            "checks": checks,
            "error": repr(exc),
            "full_action": "NOT_DERIVED",
        }

    destination = directory / "verification.json"

    if destination.exists():
        if json.loads(destination.read_text()) != result:
            print(
                "VERIFICATION_RECHECK_DIFFERS_NO_OVERWRITE"
            )
            return 3

    else:
        atomic_json(destination, result)
        atomic_text(
            directory / "verification.sha256",
            digest(destination)
            + "  verification.json\n",
        )

    print("GRAVITY2_03A_VERIFY=" + result["status"])
    print(
        "CHECKS="
        + str(sum(checks.values()))
        + "/"
        + str(len(checks))
    )
    print(
        "VERIFICATION_SHA256="
        + digest(destination)
    )

    return (
        0 if result["status"]
        == "PASS_SCOPED_4D_IDENTITY_AND_PRECONDITION_BLOCK"
        else 3
    )
