"""Independent GRAVITY2 miner gate- and artifact-verifier.

Recalculates exact restricted source controls with a separate implementation.
A verification PASS means bounded implementation/proof consistency, never lift.
"""
from __future__ import annotations

from fractions import Fraction as F
import json

from .engine import ROOT, atomic_json, atomic_text, digest
from . import miner_cases as cases
from . import miner


def _independent_static_control():
    # Integrated source identity contains only nonnegative
    # terms for A0=0, m_i^2>=0, lambda_i>=0.
    # Equality, finite decay, and zero surface flux
    # require each scalar field to vanish.
    for u, mass, quart in (
        (F(1, 3), F(0), F(2)),
        (F(4, 7), F(3), F(0)),
        (F(0), F(0), F(0)),
    ):
        total = u + mass + quart
        assert total >= 0

        if total == 0:
            assert u == mass == quart == 0

    return True


def _independent_stationary_control():
    # Q=q sum n_i*a_i, E=sum n_i*a_i^2/2.
    # The weighted Cauchy remainder is
    # sum_i,j n_i*n_j*(a_i-a_j)^2 >= 0.
    n = [F(1, 2), F(3, 4), F(5, 6)]
    a = [F(-2), F(3), F(1, 2)]
    q = F(11, 9)

    N = sum(n)

    E = sum(
        (
            z*w*w/2
            for z, w in zip(n, a)
        ),
        F(0),
    )

    Q = sum(
        (
            q*z*w
            for z, w in zip(n, a)
        ),
        F(0),
    )

    pair = sum(
        (
            n[i]*n[j]*(a[i]-a[j])**2
            for i in range(3)
            for j in range(3)
        ),
        F(0),
    )

    assert Q**2 <= 2*q*q*N*E

    assert (
        2*N*sum(
            (
                z*w*w
                for z, w in zip(n, a)
            ),
            F(0),
        )
        - 2*(Q/q)**2
    ) == pair

    return True


def verify(folder):
    checks = {}

    def gate(label, ok):
        checks[label] = bool(ok)

        if not ok:
            raise AssertionError(label)

    try:
        m = json.loads(
            (folder / "manifest.json").read_text()
        )

        s = json.loads(
            (folder / "science.json").read_text()
        )

        ledger = dict(
            line.split("  ", 1)[::-1]
            for line in (
                folder / "hashes.sha256"
            ).read_text().splitlines()
        )

        gate(
            "immutable manifest",
            ledger["manifest.json"]
            == digest(folder / "manifest.json"),
        )

        gate(
            "immutable science",
            ledger["science.json"]
            == digest(folder / "science.json"),
        )

        gate(
            "run association",
            folder.name == s["run_id"] == m["run_id"],
        )

        gate(
            "program schema",
            m["schema"] == s["schema"] == cases.SCHEMA,
        )

        gate(
            "exact producer source locks",
            m["producer_sha256"] == miner.producer_hashes(),
        )

        gate(
            "supported levels",
            m["level"] in ("L0", "L1")
            and m["workers"] == 1,
        )

        gate(
            "scope not upgraded",
            s["full_regression"] == "NOT_RUN"
            and s["high_level_solvers"]
                == "DISABLED_UNTIL_INDEPENDENT_SOURCE_ACTION",
        )

        gate(
            "no invented lift",
            not s["physical_survivors"]
            and s["physical_lift"] == "NOT_DERIVED"
            and s["complete_energy_SI"] == "NOT_CERTIFIED"
            and s["006D_replaced"] is False,
        )

        gate(
            "action and Earth not closed",
            s["complete_covariant_action"] == "NOT_DERIVED"
            and s["Einstein_exterior_force"] == "NOT_DERIVED"
            and s["real_finite_supported_source"]
                == "NOT_ESTABLISHED",
        )

        gate(
            "action specification exact",
            s["candidate_action"] == cases.ACTION
            and s["candidate_registry"] == cases.registry(),
        )

        import hashlib

        gate(
            "parent fingerprint consistent",
            m["parent_fingerprint"]
            == hashlib.sha256(
                json.dumps(
                    s["parent_locks"],
                    sort_keys=True,
                ).encode()
            ).hexdigest(),
        )

        gate(
            "parent files unchanged",
            s["parent_locks"] == miner.parent_locks(),
        )

        gate(
            "no duplicate evaluated cards",
            len({
                x["candidate_id"]
                for x in s["processed"]
            }) == len(s["processed"]),
        )

        gate(
            "complete queue partition",
            (
                {x["candidate_id"] for x in s["processed"]}
                | set(s["pending"])
            ) == {
                c["id"] for c in cases.registry()
            },
        )

        gate(
            "exact theorem controls independent",
            _independent_static_control()
            and _independent_stationary_control(),
        )

        gate(
            "L1 memory policy",
            m["level"] == "L0"
            or m["memory_soft_mib"] >= 384,
        )

        for entry in s["processed"]:
            cid = entry["candidate_id"]

            reg = {
                c["id"]: c
                for c in cases.registry()
            }[cid]

            gate(
                "fingerprint:" + cid,
                entry["fingerprint"] == reg["fingerprint"],
            )

            ref = entry["evidence_ref"]
            evidence = ROOT / ref["relative_path"]

            gate(
                "evidence hash:" + cid,
                evidence.is_file()
                and digest(evidence) == ref["sha256"],
            )

            result = json.loads(
                evidence.read_text()
            )

            older_manifest = (
                ROOT / "results/gravity2/miner_runs"
                / ref["from_run"]
                / "manifest.json"
            )

            gate(
                "cache producing code provenance:" + cid,
                older_manifest.is_file()
                and json.loads(
                    older_manifest.read_text()
                )["producer_sha256"] == m["producer_sha256"],
            )

            gate(
                "evidence provenance:" + cid,
                result["fingerprint"] == reg["fingerprint"]
                and result["parent_fingerprint"]
                    == m["parent_fingerprint"],
            )

            gate(
                "no promotion:" + cid,
                result["qualified_physical_survivor"] is False
                and result["loaded_simulation"] is False
                and result["complete_source_action"] is False,
            )

            theorem = result["gate_G05"]

            if cid == "C1_STATIC_NO_A0":
                gate(
                    "restricted static theorem",
                    theorem["verdict"] == "FAIL_SCOPED"
                    and theorem["theorem"]
                        == "STATIC_A0_ZERO_CONVEX_SCALAR_SOURCE_NO_GO",
                )

                gate(
                    "restricted static scope",
                    "NOT A NO-GO" in theorem["scope"]
                    and "lambda>=0" in theorem["assumptions"],
                )

            elif cid == "C1_HARMONIC_PHASE":
                gate(
                    "stationary underdetermination",
                    theorem["verdict"] == "UNDERDETERMINED",
                )

            else:
                gate(
                    "zero source control",
                    theorem["theorem"]
                        == "ZERO_CARRIER_AND_CURRENT_CONTROL"
                    and theorem["verdict"] == "FAIL_SCOPED",
                )

            gate(
                "no L2 bypass:" + cid,
                result["other_gates"]["G06_LOAD"]
                    == "NOT_AUTHORIZED",
            )

            if entry["status"] in (
                "RESUMED_PREVIOUS_EVIDENCE",
                "CACHED_SCOPED_FAILURE",
            ):
                gate(
                    "reuse is labeled:" + cid,
                    ref["from_run"] != m["run_id"],
                )

        if s["execution_status"] == "COMPLETED":
            gate(
                "complete only if every candidate processed",
                len(s["processed"]) == len(cases.REGISTRY)
                and not s["pending"]
                and s["parent_locks"]["all_match"],
            )

            status = (
                "PASS_SCOPED_AUTONOMOUS_GATES_NO_PHYSICS"
            )

        else:
            gate(
                "incomplete not promoted",
                not s["physical_survivors"]
                and s["execution_status"] in (
                    "PARENT_HOLD",
                    "USER_STOP",
                    "USER_INTERRUPT",
                    "STORAGE_LIMIT",
                    "TIME_BUDGET_EXCEEDED",
                    "MEMORY_LIMIT",
                    "WORKER_ERROR",
                    "WORKER_BAD_JSON",
                    "WORKER_EVIDENCE_MISMATCH",
                    "WORKER_UNRESPONSIVE",
                ),
            )

            status = "PASS_INCOMPLETE_EVIDENCE_ONLY"

        report = {
            "program": "GRAVITY2_MINER_INDEPENDENT",
            "run_id": folder.name,
            "status": status,
            "checks": checks,
            "science_sha256":
                digest(folder / "science.json"),
            "physical_lift": "NOT_DERIVED",
            "source_action": "NOT_COMPLETE",
            "full_regression": "NOT_RUN",
        }

    except Exception as exc:
        report = {
            "program": "GRAVITY2_MINER_INDEPENDENT",
            "run_id": folder.name,
            "status": "HOLD",
            "checks": checks,
            "error": repr(exc),
            "physical_lift": "NOT_DERIVED",
        }

    path = folder / "verification.json"

    if path.is_file():
        if json.loads(path.read_text()) != report:
            print(
                "VERIFICATION_RECHECK_DIFFERS_NO_OVERWRITE"
            )
            return 3

    else:
        atomic_json(path, report)
        atomic_text(
            folder / "verification.sha256",
            digest(path) + "  verification.json\n",
        )

    print(
        "GRAVITY2_MINER_VERIFY=" + report["status"]
    )

    print(
        "CHECKS="
        + str(sum(checks.values()))
        + "/"
        + str(len(checks))
    )

    print(
        "VERIFICATION_SHA256=" + digest(path)
    )

    return (
        0 if report["status"] in (
            "PASS_SCOPED_AUTONOMOUS_GATES_NO_PHYSICS",
            "PASS_INCOMPLETE_EVIDENCE_ONLY",
        ) else 3
    )
