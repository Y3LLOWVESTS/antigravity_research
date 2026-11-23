"""GRAVITY2-00 independent report verifier.

This verifies evidence integrity, reproducibility and claim boundaries.
It is NOT a physical source-to-gravity theorem verifier. That comes
with the later GRAVITY2-01 mathematical-action implementation.
"""

import json
from pathlib import Path

from .engine import (
    digest,
    atomic_json,
    atomic_text,
    ROOT,
    source_hashes,
)

from .policy import (
    ANCHORS,
    GATES,
    PARENTS,
    PROGRAM,
    SCHEMA,
)


def verify_run(run_dir: Path) -> int:
    checks = {}

    def record(label, ok):
        checks[label] = bool(ok)
        if not ok:
            raise AssertionError(label)

    try:
        manifest_path = run_dir / "manifest.json"
        science_path = run_dir / "science.json"

        manifest = json.loads(
            manifest_path.read_text()
        )
        science = json.loads(
            science_path.read_text()
        )

        hashes = dict(
            line.split("  ", 1)[::-1]
            for line in
            (run_dir / "hashes.sha256").read_text().splitlines()
        )

        record(
            "manifest hash",
            hashes["manifest.json"] == digest(manifest_path),
        )

        record(
            "science hash",
            hashes["science.json"] == digest(science_path),
        )

        record(
            "same run id",
            manifest["run_id"]
            == science["run_id"]
            == run_dir.name,
        )

        record(
            "schema and program",
            manifest["schema"]
            == science["schema"]
            == SCHEMA
            and manifest["program"]
            == science["program"]
            == PROGRAM,
        )

        record(
            "unmodified producing modules",
            manifest["producer_sources_sha256"]
            == source_hashes(),
        )

        record(
            "legacy access read-only",
            manifest["legacy_miner_access"]
            == "READ_ONLY_SOURCE_SHA_NO_EXECUTION_OR_WRITES",
        )

        record(
            "no scientific promotion",
            science["physical_success"] is False
            and science["Einstein_source_to_metric_bridge"]
            == "NOT_DERIVED"
            and science["whole_craft_force"]
            == "NOT_DERIVED"
            and science["certified_complete_energy_j"] is None
            and science["physical_research_percentage_promotion"]
            == "NONE",
        )

        record(
            "no implied full regression",
            science["full_regression"] == "NOT_RUN",
        )

        record(
            "historical R3B value is protected, not rederived",
            science["historical_anchors"][
                "prescribed_mixed_field_capacity_j"
            ] == 1.5429162116460216
            and science["historical_anchors_provenance"]
            == "RECORDED_ONLY_NOT_RECOMPUTED",
        )

        record(
            "prescribed loaded force negative control",
            science["historical_anchors"][
                "historical_loaded_min_acceleration_m_s2"
            ] == -129.67185782242464
            and ANCHORS[
                "historical_preloaded_min_acceleration_m_s2"
            ] > 0,
        )

        record(
            "gate inventory complete",
            set(science["gates"]) == set(GATES),
        )

        record(
            "G02 through G11 did not run",
            all(
                science["gates"][x] == "NOT_RUN"
                for x in GATES[2:]
            ),
        )

        record(
            "bounded output recorded",
            manifest["disk_soft_limit_mib"] > 0
            and science["resource"]["disk_soft_policy"]
            == "APPLICATION_WATCHDOG_NOT_KERNEL_QUOTA",
        )

        record(
            "valid execution classification",
            science["execution_status"] in (
                "COMPLETED",
                "TIME_BUDGET_EXCEEDED",
                "MEMORY_LIMIT",
                "STORAGE_LIMIT",
                "USER_STOP",
                "USER_INTERRUPT",
                "SOFTWARE_ERROR",
            ),
        )

        if science["execution_status"] == "COMPLETED":

            for key, (path, expected) in PARENTS.items():
                p = science["parents"][key]

                record(
                    "parent expectation " + key,
                    p["sha256_expected"] == expected
                    and p["path_relative_to_repo"] == path
                    and p["mandatory"] is True,
                )

                original = ROOT / path

                actual = (
                    digest(original)
                    if original.is_file()
                    else None
                )

                record(
                    "parent live provenance " + key,
                    actual == p["sha256_actual"],
                )

                record(
                    "parent accurate classification " + key,
                    p["status"] == (
                        "MATCH"
                        if actual == expected
                        else "MISSING"
                        if actual is None
                        else "DRIFT"
                    ),
                )

            locked = all(
                science["parents"][key]["status"] == "MATCH"
                for key in PARENTS
            )

            record(
                "gate G00 truthful",
                science["gates"]["G00_PARENT"]
                == (
                    "PASS_SCOPED"
                    if locked
                    else "UNDERDETERMINED"
                ),
            )

            record(
                "gate G01 truthful",
                science["gates"]["G01_ACTION"]
                == (
                    "UNDERDETERMINED"
                    if locked
                    else "NOT_RUN"
                ),
            )

            record(
                "R3B-NULL never survivor",
                science["candidate"]["id"] == "R3B-NULL"
                and science["candidate"]["outcome"]
                == "NEVER_A_PHYSICAL_SURVIVOR",
            )

        else:
            record(
                "uncompleted run not promoted",
                all(
                    x == "NOT_RUN"
                    for x in science["gates"].values()
                ),
            )

        result = {
            "schema": SCHEMA,
            "program":
                "GRAVITY2-00-INDEPENDENT-EVIDENCE-VERIFIER",
            "run_id": run_dir.name,
            "verification": "PASS_EVIDENCE_INTEGRITY_ONLY",
            "checks": checks,
            "physical_model": "NOT_VERIFIED",
            "source_action": "NOT_DERIVED",
            "full_regression": "NOT_RUN",
            "science_sha256": digest(science_path),
            "producer_source_sha256":
                manifest["producer_sources_sha256"],
            "parent_status": science["parent_audit_status"],
        }

    except Exception as exc:
        result = {
            "schema": SCHEMA,
            "program":
                "GRAVITY2-00-INDEPENDENT-EVIDENCE-VERIFIER",
            "run_id": run_dir.name,
            "verification": "HOLD",
            "checks": checks,
            "error": repr(exc),
            "physical_model": "NOT_VERIFIED",
        }

    p = run_dir / "independent_verification.json"

    if p.exists():
        earlier = json.loads(p.read_text())

        if earlier != result:
            print(
                "VERIFIER_RECHECK_DIFFERS; "
                "original evidence preserved"
            )
            return 3

        print("VERIFIER_EXISTING_IMMUTABLE_RESULT")

    else:
        atomic_json(p, result)

        atomic_text(
            run_dir / "independent_verification.sha256",
            digest(p) + "  independent_verification.json\n",
        )

    print(
        "GRAVITY2_VERIFY=",
        result["verification"],
    )
    print(
        "CHECKS=",
        sum(checks.values()),
        "/",
        len(checks),
    )
    print(
        "VERIFICATION_SHA256=",
        digest(p),
    )
    print(
        "RUN_DIR=",
        run_dir,
    )

    return (
        0
        if result["verification"]
        == "PASS_EVIDENCE_INTEGRITY_ONLY"
        else 3
    )
