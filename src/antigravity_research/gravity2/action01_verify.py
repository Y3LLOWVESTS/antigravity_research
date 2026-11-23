"""Independent GRAVITY2-01 evidence verifier.

Reparses pinned sources; never imports the historical AGMINER.
"""
from __future__ import annotations

import ast
import json
from fractions import Fraction as Q

from . import action01_core as core
from .engine import (
    ROOT, atomic_json, atomic_text, digest,
)
from .action01 import hashes


def verify_run(directory):
    checks = {}

    def check(label, truth):
        checks[label] = bool(truth)
        if not truth:
            raise AssertionError(label)

    try:
        manifest = json.loads(
            (directory/"manifest.json").read_text()
        )

        science = json.loads(
            (directory/"science.json").read_text()
        )

        pairs = [
            line.split("  ", 1)
            for line in (
                directory/"hashes.sha256"
            ).read_text().splitlines()
        ]

        recorded = {
            name: sha for sha, name in pairs
        }

        check(
            "hash manifest",
            recorded["manifest.json"]
            == digest(directory/"manifest.json"),
        )

        check(
            "hash science",
            recorded["science.json"]
            == digest(directory/"science.json"),
        )

        check(
            "run association",
            science["run_id"]
            == manifest["run_id"]
            == directory.name,
        )

        check(
            "new module SHA locks",
            manifest["codes_sha256"] == hashes(),
        )

        check(
            "never modifying legacy miner",
            manifest["legacy_AGMINER_write_or_execution"]
            == "NONE",
        )

        check(
            "old gravity2 code unchanged claim",
            manifest["old_GRAVITY2_00_code_modified"]
            is False,
        )

        check(
            "L0 one worker",
            manifest["level"] == "L0",
        )

        check(
            "no full regression",
            science["full_regression"] == "NOT_RUN",
        )

        check(
            "no lift",
            science["physical_lift"] == "NOT_DERIVED"
            and science["006D_replaced"] is False,
        )

        check(
            "energy uncertified",
            science["complete_energy"]
            == "NOT_CERTIFIED",
        )

        check(
            "no full action promoted",
            science["complete_covariant_action"]
            == "NOT_DERIVED"
            and science["new_source_action_survivors"] == 0,
        )

        check(
            "valid status",
            science["execution_status"] in (
                "COMPLETED",
                "TIME_BUDGET_EXCEEDED",
                "WORKER_ERROR",
                "WORKER_BAD_JSON",
                "MEMORY_SOFT_LIMIT",
                "DISK_SOFT_LIMIT",
                "INTERRUPTED",
            ),
        )

        check(
            "soft limit truthful",
            science["resource"]["limit_class"]
            == "APPLICATION_WATCHDOG_SOFT_LIMITS",
        )

        if science["execution_status"] == "COMPLETED":
            e = science["evidence"]

            for name, (path, expected) in core.PINS.items():
                real = ROOT/path

                check(
                    name + " file SHA",
                    real.is_file()
                    and digest(real) == expected,
                )

                reported = e["parents"][name]

                check(
                    name + " reported SHA",
                    reported["actual_sha256"] == expected
                    and reported["status"] == "MATCH",
                )

                # Reconstruct witness locations independently.
                node = ast.parse(
                    real.read_text(encoding="utf-8")
                )

                live = {
                    x.name: x
                    for x in node.body
                    if isinstance(
                        x,
                        (
                            ast.FunctionDef,
                            ast.AsyncFunctionDef,
                        ),
                    )
                }

                for witness in e["witnesses"][name]:
                    n = live.get(witness["function"])

                    check(
                        name + " witness "
                        + witness["function"],
                        n is not None
                        and n.lineno
                            == witness["start_line"]
                        and n.end_lineno
                            == witness["end_line"],
                    )

            g0dir = (
                ROOT/"results"/"gravity2"
                /"runs"/core.G00_ID
            )

            check(
                "G00 science live SHA",
                digest(g0dir/"science.json")
                == core.G00_SHA,
            )

            check(
                "G00 verifier live SHA",
                digest(
                    g0dir/"independent_verification.json"
                ) == core.G00_VERIFY_SHA,
            )

            check(
                "G00 linked status",
                e["gravity2_00_parent"]["status"]
                == "MATCH",
            )

            check(
                "G01 underdetermined not pass",
                e["gates"]["G01_ACTION"]
                == "UNDERDETERMINED_IN_AUDITED_CODE",
            )

            check(
                "G02 not promoted",
                e["gates"]["G02_VARIATION"]
                == "NOT_RUN_FULL_VARIATION_MISSING",
            )

            check(
                "no complete source action",
                e["qualified_source_actions"] == 0,
            )

            check(
                "historical R3B capacity record",
                e["historical_prescribed_capacity_J"]
                == 1.5429162116460216
                and e["capacity_result"]
                == "RECORDED_NOT_RECOMPUTED",
            )

            check(
                "loaded historical negative preserved",
                e["historical_loaded_min_acceleration_m_s2"]
                == -129.67185782242464
                and e["historical_loaded_result"]
                == "RECORDED_NOT_RERUN",
            )

            check(
                "F2 not R3B loaded",
                e["historical_classification_correction"][
                    "F2_strong_payload_rescue"
                ] == "A12C_F2_SECTOR_NOT_R3B_MIXED_LOADED",
            )

            check(
                "conservation obligations open",
                e["action_terms"][
                    "off_shell_Ward_Noether_Bianchi"
                ] == "NOT_DERIVED_FOR_COMPLETE_ACTION",
            )

            check(
                "Einstein action open",
                e["action_terms"][
                    "einstein_hilbert_and_metric_variation"
                ]
                == "NOT_IDENTIFIED_AS_COMPLETE_COVARIANT_VARIATION",
            )

            # Independent analytic differentiation of
            # the scoped finite-dimensional sign test.
            k = Q(4, 3)
            field_e = Q(3, 5)
            field_a = Q(-2, 7)
            je = Q(1, 4)
            ja = Q(-3, 8)

            check(
                "toy derivative e",
                e["sign_negative_control"]["dQ_de_exact"]
                == str(field_e+k*field_a-je),
            )

            check(
                "toy derivative a",
                e["sign_negative_control"]["dQ_da_exact"]
                == str(-field_a+k*field_e-ja),
            )

            check(
                "toy opposite cross blocks",
                e["sign_negative_control"][
                    "positive_K_cross_blocks_exact"
                ] == [str(k), str(-k)],
            )

            check(
                "toy never full action",
                e["sign_negative_control"][
                    "not_the_full_R3B_action"
                ] is True,
            )

            check(
                "scoped decision",
                e["decision"]
                == "ACTION_COMPLETENESS_ATLAS_NO_PHYSICAL_PROMOTION",
            )

        result = {
            "program":
                "GRAVITY2-01_INDEPENDENT_CODE_AND_CLAIM_VERIFIER",
            "run_id": directory.name,
            "status":
                "PASS_SCOPED_CODE_PROVENANCE_ONLY",
            "science_sha256":
                digest(directory/"science.json"),
            "checks": checks,
            "new_physics": "NONE",
            "complete_action": "NOT_DERIVED",
        }

    except Exception as exc:
        result = {
            "program":
                "GRAVITY2-01_INDEPENDENT_CODE_AND_CLAIM_VERIFIER",
            "run_id": directory.name,
            "status": "HOLD",
            "checks": checks,
            "error": repr(exc),
            "complete_action": "NOT_DERIVED",
        }

    dst = directory/"verification.json"

    if dst.exists():
        if json.loads(dst.read_text()) != result:
            print(
                "VERIFICATION_RECHECK_DIFFERS; "
                "NO_OVERWRITE"
            )
            return 3

    else:
        atomic_json(dst, result)
        atomic_text(
            directory/"verification.sha256",
            digest(dst) + "  verification.json\n",
        )

    print(
        "GRAVITY2_01_VERIFY=" + result["status"]
    )
    print(
        "CHECKS="
        + str(sum(checks.values()))
        + "/"
        + str(len(checks))
    )
    print(
        "VERIFICATION_SHA256=" + digest(dst)
    )

    return (
        0
        if result["status"]
        == "PASS_SCOPED_CODE_PROVENANCE_ONLY"
        else 3
    )
