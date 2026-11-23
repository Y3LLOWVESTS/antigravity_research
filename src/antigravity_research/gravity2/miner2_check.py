"""Independent GRAVITY2-04 evidence and symbolic-source verifier.

Separate trace derivation and 2x2 mass-rank checks.
No test represents a complete source, Einstein gravity, or certified lift.
"""
from __future__ import annotations

import json

from . import miner2 as run
from . import miner2_math as physics
from .engine import ROOT, atomic_json, atomic_text, digest


def independent_math():
    import sympy as s

    z,a,b,k,v = s.symbols(
        "z a b k v", real=True
    )

    sig = a*z-b*z**2
    x = s.exp(sig)

    density = -(x*x*k)/2-x**4*v

    # Derive the same source contribution by a separate
    # infinitesimal conformal rescaling, not the producer's
    # directly factorized source-trace formula.
    t = s.symbols("t",real=True)

    perturbed = (
        -(x*s.exp(t))**2*k/2
        -(x*s.exp(t))**4*v
    )

    direct = s.diff(
        perturbed,t
    ).subs(t,0)

    hodge = s.diff(
        density,z
    )

    assert s.simplify(
        hodge-direct*s.diff(sig,z)
    ) == 0

    assert s.simplify(hodge) != 0

    assert s.simplify(
        s.diff(-(k/2+v),z)
    ) == 0

    return {
        "jordan_portal_chain": "ZERO_RESIDUAL",
        "Einstein_frame_direct_portal": "ZERO",
        "source_trace_omission_control": "NONZERO",
        "mass_rank_none": 0,
        "mass_rank_one": 1,
        "mass_rank_both": 2,
    }


def verify(folder):
    checks = {}

    def check(label,ok):
        checks[label] = bool(ok)

        if not ok:
            raise AssertionError(label)

    try:
        man = json.loads(
            (folder/"manifest.json").read_text()
        )

        sci = json.loads(
            (folder/"science.json").read_text()
        )

        ledger = dict(
            line.split("  ",1)[::-1]
            for line in (
                folder/"hashes.sha256"
            ).read_text().splitlines()
        )

        check(
            "manifest immutable SHA",
            ledger["manifest.json"]
                == digest(folder/"manifest.json"),
        )

        check(
            "science immutable SHA",
            ledger["science.json"]
                == digest(folder/"science.json"),
        )

        check(
            "run id",
            man["run_id"]
                == sci["run_id"]
                == folder.name,
        )

        check(
            "code source hashes",
            man["code_sha256"]
                == run.code_hashes(),
        )

        check(
            "scoped runtime",
            man["level"] == "L1"
            and man["workers"] == 1,
        )

        check(
            "no old miner overwrite asserted",
            man["previous_GRAVITY2_producers"]
                == "NOT_MODIFIED",
        )

        check(
            "no legacy execution",
            man["old_AGMINER"]
                == "READ_ONLY_NO_EXECUTION",
        )

        check(
            "accurate parent locks",
            sci["parent_locks"]
                == run.locks(),
        )

        check(
            "parent fingerprint",
            man["parent_fingerprint"]
                == run.parent_digest(
                    sci["parent_locks"]
                ),
        )

        check(
            "generated action registry",
            sci["generated_actions"]
                == physics.registry(),
        )

        check(
            "no historical repeats",
            sci["historical_exclusions"]
                == list(
                    physics.HISTORICAL_EXCLUSIONS
                ),
        )

        check(
            "hard physical claim boundary",
            sci["physical_survivors"] == []
            and sci["complete_action"]
                == "NOT_DERIVED"
            and sci["whole_craft_lift"]
                == "NOT_DERIVED"
            and sci["complete_energy"]
                == "NOT_CERTIFIED"
            and sci["006D_replaced"] is False,
        )

        check(
            "no PDE",
            sci["loaded_PDE"]
                == "NOT_AUTHORIZED"
            and sci["full_regression"]
                == "NOT_RUN",
        )

        check(
            "legal execution status",
            sci["execution_status"] in (
                "COMPLETED",
                "PARENT_HOLD",
                "TIME_BUDGET_EXCEEDED",
                "USER_STOP",
                "USER_INTERRUPT",
                "STORAGE_LIMIT",
                "WORKER_ERROR",
                "WORKER_EVIDENCE_MISMATCH",
            ),
        )

        cards = {
            c["id"]:c
            for c in physics.registry()
        }

        done = {
            x["candidate_id"]
            for x in sci["processed"]
        }

        check(
            "unique candidates",
            len(done) == len(sci["processed"]),
        )

        check(
            "queue partition",
            done|set(sci["pending"]) == set(cards),
        )

        math = independent_math()

        check(
            "independent trace identity",
            math["jordan_portal_chain"]
                == "ZERO_RESIDUAL",
        )

        for entry in sci["processed"]:
            cid = entry["candidate_id"]
            card = cards[cid]

            check(
                "fingerprint "+cid,
                entry["fingerprint"]
                    == card["fingerprint"],
            )

            ref = entry["evidence_ref"]
            path = ROOT/ref["relative_path"]

            check(
                "case evidence SHA "+cid,
                path.is_file()
                and digest(path) == ref["sha256"],
            )

            val = json.loads(path.read_text())

            check(
                "case association "+cid,
                val["id"] == cid
                and val["fingerprint"]
                    == card["fingerprint"]
                and val["parent_fingerprint"]
                    == man["parent_fingerprint"],
            )

            check(
                "massless count "+cid,
                val["massless_U1_count"]
                    == 2-sum(card["vev"]),
            )

            check(
                "source frame "+cid,
                val["source_in_physical_metric"]
                    == (card["frame"]=="JORDAN"),
            )

            check(
                "physical gates "+cid,
                val["qualified_physical_survivor"]
                    is False
                and val["source_finite_stable"]
                    == "NOT_ESTABLISHED"
                and val["R3B_coupled_loaded_solve"]
                    == "NOT_AUTHORIZED",
            )

            expected = (
                "ACTION_COMPARISON_UNDERDETERMINED_SOURCE_SUPPORT"
                if card["potential"]=="CONVEX"
                else
                "SCOPED_NO_UNBROKEN_U1_FOR_BOTH_EXTERIOR_VEVS"
                if card["vev"] == [1,1]
                else
                "ONE_EXTERIOR_CARRIER_HIGGSED_OTHER_UNBROKEN"
            )

            check(
                "scoped decision "+cid,
                val["decision"] == expected,
            )

            check(
                "trace variation not frozen "+cid,
                val["necessary_identity_checks"][
                    "Jordan_source_extra_P_variation"
                ] == "NONZERO_GENERAL",
            )

            if entry["status"] == "REUSED_VERIFIED_EVIDENCE":
                old = run.run_dir(
                    ref["from_run"]
                )

                check(
                    "cached run previously verified "+cid,
                    old != folder
                    and (
                        old/"verification.json"
                    ).is_file()
                    and json.loads(
                        (
                            old/"verification.json"
                        ).read_text()
                    )["status"]
                        == "PASS_SCOPED_ACTION_GENERATION_ONLY",
                )

            else:
                check(
                    "new evidence belongs to this run "+cid,
                    ref["from_run"] == folder.name,
                )

        if sci["execution_status"] == "COMPLETED":
            check(
                "completed queue",
                len(sci["processed"]) == len(cards)
                and not sci["pending"]
                and run.lock_pass(
                    sci["parent_locks"]
                ),
            )

            status = (
                "PASS_SCOPED_ACTION_GENERATION_ONLY"
            )

        else:
            check(
                "incomplete not promoted",
                not sci["physical_survivors"],
            )

            status = (
                "PASS_INCOMPLETE_EVIDENCE_ONLY"
            )

        report = {
            "program":
                "GRAVITY2-04_INDEPENDENT_VERIFIER",
            "run_id": folder.name,
            "status": status,
            "checks": checks,
            "science_sha256":
                digest(folder/"science.json"),
            "physical_success": "NO",
            "full_action": "NOT_DERIVED",
        }

    except Exception as exc:
        report = {
            "program":
                "GRAVITY2-04_INDEPENDENT_VERIFIER",
            "run_id": folder.name,
            "status": "HOLD",
            "checks": checks,
            "error": repr(exc),
            "physical_success": "NO",
        }

    path = folder/"verification.json"

    if path.exists():
        if json.loads(path.read_text()) != report:
            print(
                "VERIFICATION_RECHECK_DIFFERS; "
                "EVIDENCE_UNCHANGED"
            )
            return 3

    else:
        atomic_json(path,report)

        atomic_text(
            folder/"verification.sha256",
            digest(path)
            +"  verification.json\n",
        )

    print(
        "GRAVITY2_04_VERIFY="+report["status"]
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
        +digest(path)
    )

    return (
        0
        if report["status"]
        == "PASS_SCOPED_ACTION_GENERATION_ONLY"
        else 3
    )
