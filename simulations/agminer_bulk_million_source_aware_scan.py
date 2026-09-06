"""
AGMINER bulk Tier-0 source-aware million-point campaign.

Purpose:
  Evaluate 500,000 fresh Sobol points each for repaired 032G and 032H.

Storage policy:
  Do not persist ordinary rejected candidates.
  Persist aggregate counters, resumable Sobol indices, and only the best
  finite-energy points.

Claims:
  A point below the configured energy lower-bound threshold is only
  Tier-0 eligible. It is not a field solution or certified antigravity.
"""

from __future__ import annotations

import json
import math
import signal
import sqlite3
import sys
import time
from pathlib import Path
from typing import Any

from antigravity_research.agminer.candidate import Candidate
from antigravity_research.agminer.policy import current_energy_policy
from antigravity_research.agminer.sampler import SobolSampler
from antigravity_research.agminer.families.family_032g_source_aware_collective_canonical import SourceAwareCollectiveCanonicalFamily
from antigravity_research.agminer.families.family_032h_source_aware_collective_dbi import SourceAwareCollectiveDBIFamily


TARGET_PER_FAMILY = 25_500_000
BATCH_SIZE = 32768
TOP_KEEP = 100
DB_SAFETY_BYTES = 95_000_000

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = Path(sys.argv[1])
CONFIG_PATH = ROOT / "config" / "agminer_032a.json"
SUMMARY_PATH = ROOT / "results" / "agminer" / "bulk_million_source_aware_summary.json"

CONFIG = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
POLICY = current_energy_policy()
POLICY_ID = str(POLICY["policy_id"])
LIMIT_J = float(POLICY["limit_j"])
COMPARISON = str(POLICY["comparison"])

PHYSICAL_MODEL_VERSION = str(
    CONFIG.get("physical_model_version", "032A_INFRASTRUCTURE_ONLY")
)
LEDGER_VERSION = str(
    CONFIG.get("energy_ledger_version", "CONSERVATIVE_COMPLETE_V1")
)

STOP = {"requested": False, "source": None}


def request_stop(signum, frame):
    STOP["requested"] = True
    STOP["source"] = str(signum)
    print("BULK_SIGNAL_STOP_REQUESTED=YES", flush=True)


signal.signal(signal.SIGINT, request_stop)
signal.signal(signal.SIGTERM, request_stop)


def total_db_bytes() -> int:
    total = 0
    for path in (
        DB_PATH,
        Path(str(DB_PATH) + "-wal"),
        Path(str(DB_PATH) + "-shm"),
    ):
        if path.exists():
            total += path.stat().st_size
    return total


def strict_energy_pass(energy_j: float) -> bool:
    if COMPARISON == "LT":
        return energy_j < LIMIT_J
    if COMPARISON == "LE":
        return energy_j <= LIMIT_J
    raise RuntimeError("Unsupported energy comparison: " + COMPARISON)


def gate_pass(result: Any) -> bool | None:
    if result is None:
        return None
    if isinstance(result, bool):
        return result
    if isinstance(result, dict):
        for key in ("passed", "pass", "ok", "valid"):
            if key in result:
                return bool(result[key])
    return None


def extract_energy(result: Any) -> float | None:
    if isinstance(result, (int, float)) and not isinstance(result, bool):
        value = float(result)
        return value if math.isfinite(value) else None
    if isinstance(result, dict):
        for key in (
            "energy_lower_bound_j",
            "lower_bound_j",
            "energy_j",
        ):
            if key in result:
                try:
                    value = float(result[key])
                except (TypeError, ValueError):
                    continue
                if math.isfinite(value):
                    return value
    return None


def compact_params(params: dict[str, float]) -> str:
    return json.dumps(
        params,
        sort_keys=True,
        separators=(",", ":"),
    )


def ensure_tables(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS bulk_scan_state (
            family TEXT NOT NULL,
            family_version TEXT NOT NULL,
            policy_id TEXT NOT NULL,
            next_index INTEGER NOT NULL,
            target_index INTEGER NOT NULL,
            tested INTEGER NOT NULL,
            analytic_fail INTEGER NOT NULL,
            naturalness_fail INTEGER NOT NULL,
            eft_fail INTEGER NOT NULL,
            energy_fail INTEGER NOT NULL,
            unresolved INTEGER NOT NULL,
            eligible INTEGER NOT NULL,
            best_energy_j REAL,
            best_candidate_id TEXT,
            updated_at REAL NOT NULL,
            PRIMARY KEY (
                family,
                family_version,
                policy_id
            )
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS bulk_best_candidates (
            candidate_id TEXT PRIMARY KEY,
            family TEXT NOT NULL,
            family_version TEXT NOT NULL,
            policy_id TEXT NOT NULL,
            sample_index INTEGER NOT NULL,
            energy_j REAL NOT NULL,
            energy_state TEXT NOT NULL,
            params_json_compact TEXT NOT NULL,
            updated_at REAL NOT NULL
        )
        """
    )
    connection.commit()


def initial_state(
    connection: sqlite3.Connection,
    family: str,
    version: str,
) -> dict[str, Any]:
    row = connection.execute(
        """
        SELECT * FROM bulk_scan_state
        WHERE family=? AND family_version=? AND policy_id=?
        """,
        (family, version, POLICY_ID),
    ).fetchone()

    if row is not None:
        return dict(row)

    state = {
        "family": family,
        "family_version": version,
        "policy_id": POLICY_ID,
        "next_index": 0,
        "target_index": TARGET_PER_FAMILY,
        "tested": 0,
        "analytic_fail": 0,
        "naturalness_fail": 0,
        "eft_fail": 0,
        "energy_fail": 0,
        "unresolved": 0,
        "eligible": 0,
        "best_energy_j": None,
        "best_candidate_id": None,
        "updated_at": time.time(),
    }

    connection.execute(
        """
        INSERT INTO bulk_scan_state (
            family,family_version,policy_id,next_index,target_index,
            tested,analytic_fail,naturalness_fail,eft_fail,energy_fail,
            unresolved,eligible,best_energy_j,best_candidate_id,updated_at
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            state["family"],
            state["family_version"],
            state["policy_id"],
            state["next_index"],
            state["target_index"],
            state["tested"],
            state["analytic_fail"],
            state["naturalness_fail"],
            state["eft_fail"],
            state["energy_fail"],
            state["unresolved"],
            state["eligible"],
            state["best_energy_j"],
            state["best_candidate_id"],
            state["updated_at"],
        ),
    )
    connection.commit()
    return state


def load_top(
    connection: sqlite3.Connection,
    family: str,
    version: str,
) -> list[dict[str, Any]]:
    rows = connection.execute(
        """
        SELECT candidate_id,sample_index,energy_j,energy_state,
               params_json_compact
        FROM bulk_best_candidates
        WHERE family=? AND family_version=? AND policy_id=?
        ORDER BY energy_j ASC,candidate_id ASC
        LIMIT ?
        """,
        (family, version, POLICY_ID, TOP_KEEP),
    ).fetchall()
    return [dict(row) for row in rows]


def persist_top(
    connection: sqlite3.Connection,
    family: str,
    version: str,
    top: list[dict[str, Any]],
) -> None:
    connection.execute(
        """
        DELETE FROM bulk_best_candidates
        WHERE family=? AND family_version=? AND policy_id=?
        """,
        (family, version, POLICY_ID),
    )

    now = time.time()
    for row in top[:TOP_KEEP]:
        connection.execute(
            """
            INSERT OR REPLACE INTO bulk_best_candidates (
                candidate_id,family,family_version,policy_id,
                sample_index,energy_j,energy_state,
                params_json_compact,updated_at
            ) VALUES (?,?,?,?,?,?,?,?,?)
            """,
            (
                row["candidate_id"],
                family,
                version,
                POLICY_ID,
                int(row["sample_index"]),
                float(row["energy_j"]),
                str(row["energy_state"]),
                str(row["params_json_compact"]),
                now,
            ),
        )

def persist_state(
    connection: sqlite3.Connection,
    state: dict[str, Any],
) -> None:
    state["updated_at"] = time.time()
    connection.execute(
        """
        UPDATE bulk_scan_state
        SET next_index=?,target_index=?,tested=?,
            analytic_fail=?,naturalness_fail=?,eft_fail=?,
            energy_fail=?,unresolved=?,eligible=?,
            best_energy_j=?,best_candidate_id=?,updated_at=?
        WHERE family=? AND family_version=? AND policy_id=?
        """,
        (
            state["next_index"],
            state["target_index"],
            state["tested"],
            state["analytic_fail"],
            state["naturalness_fail"],
            state["eft_fail"],
            state["energy_fail"],
            state["unresolved"],
            state["eligible"],
            state["best_energy_j"],
            state["best_candidate_id"],
            state["updated_at"],
            state["family"],
            state["family_version"],
            state["policy_id"],
        ),
    )
    connection.commit()


def consider_top(
    top: list[dict[str, Any]],
    plugin: Any,
    params: dict[str, float],
    sample_index: int,
    energy_j: float,
    energy_state: str,
) -> None:
    if len(top) >= TOP_KEEP and energy_j >= float(top[-1]["energy_j"]):
        return

    candidate = Candidate(
        family_id=str(plugin.family_id),
        family_version=str(plugin.family_version),
        params=params,
        physical_model_version=PHYSICAL_MODEL_VERSION,
        energy_ledger_version=LEDGER_VERSION,
    )

    top.append(
        {
            "candidate_id": candidate.candidate_id,
            "sample_index": sample_index,
            "energy_j": energy_j,
            "energy_state": energy_state,
            "params_json_compact": compact_params(params),
        }
    )
    top.sort(
        key=lambda item: (
            float(item["energy_j"]),
            str(item["candidate_id"]),
        )
    )
    del top[TOP_KEEP:]


def evaluate_family(
    connection: sqlite3.Connection,
    plugin: Any,
) -> dict[str, Any]:
    family = str(plugin.family_id)
    version = str(plugin.family_version)

    if str(getattr(plugin, "energy_bound_scope", "")) != "COMPLETE_OPERATING_LOWER_BOUND":
        raise RuntimeError(
            family + " is not eligible for source-aware bulk scan"
        )

    state = initial_state(connection, family, version)
    top = load_top(connection, family, version)
    bounds = plugin.sample_bounds()

    print("")
    print("=== BULK_FAMILY_START ===")
    print("FAMILY=" + family)
    print("VERSION=" + version)
    print("START_INDEX=" + str(state["next_index"]))
    print("TARGET_INDEX=" + str(state["target_index"]))

    last_report = int(state["tested"])

    while (
        int(state["next_index"]) < int(state["target_index"])
        and not STOP["requested"]
    ):
        if total_db_bytes() >= DB_SAFETY_BYTES:
            STOP["requested"] = True
            STOP["source"] = "DB_BUDGET"
            print("DB_BUDGET_STOP=YES", flush=True)
            break

        remaining = (
            int(state["target_index"])
            - int(state["next_index"])
        )
        batch_count = min(BATCH_SIZE, remaining)
        batch_start = int(state["next_index"])

        sampler = SobolSampler(bounds, index=batch_start)
        samples = sampler.sample(batch_count)

        for offset, raw in enumerate(samples):
            if STOP["requested"]:
                break

            sample_index = batch_start + offset
            params = {
                str(key): float(value)
                for key, value in raw.items()
            }

            canonicalizer = getattr(plugin, "canonicalize_params", None)
            if callable(canonicalizer):
                params = canonicalizer(params)

            state["tested"] += 1

            try:
                analytic = gate_pass(
                    plugin.analytic_precheck(params, CONFIG)
                )
            except Exception:
                analytic = None

            if analytic is False:
                state["analytic_fail"] += 1
                state["next_index"] = sample_index + 1
                continue
            if analytic is None:
                state["unresolved"] += 1
                state["next_index"] = sample_index + 1
                continue

            try:
                naturalness = gate_pass(
                    plugin.naturalness_precheck(params, CONFIG)
                )
            except Exception:
                naturalness = None

            if naturalness is False:
                state["naturalness_fail"] += 1
                state["next_index"] = sample_index + 1
                continue
            if naturalness is None:
                state["unresolved"] += 1
                state["next_index"] = sample_index + 1
                continue

            try:
                eft = gate_pass(
                    plugin.eft_precheck(params, CONFIG)
                )
            except Exception:
                eft = None

            if eft is False:
                state["eft_fail"] += 1
                state["next_index"] = sample_index + 1
                continue
            if eft is None:
                state["unresolved"] += 1
                state["next_index"] = sample_index + 1
                continue

            try:
                energy_j = extract_energy(
                    plugin.energy_lower_bound(params, CONFIG)
                )
            except Exception:
                energy_j = None

            if energy_j is None or energy_j < 0.0:
                state["unresolved"] += 1
                state["next_index"] = sample_index + 1
                continue

            passed = strict_energy_pass(energy_j)

            if passed:
                state["eligible"] += 1
                energy_state = "TIER0_ELIGIBLE_LOWER_BOUND"
            else:
                state["energy_fail"] += 1
                energy_state = "REJECTED_ENERGY_OBJECTIVE"

            consider_top(
                top,
                plugin,
                params,
                sample_index,
                energy_j,
                energy_state,
            )

            if (
                state["best_energy_j"] is None
                or energy_j < float(state["best_energy_j"])
            ):
                state["best_energy_j"] = energy_j
                if top:
                    state["best_candidate_id"] = top[0]["candidate_id"]

            state["next_index"] = sample_index + 1

        persist_top(connection, family, version, top)
        persist_state(connection, state)

        if int(state["tested"]) - last_report >= 1_000_000:
            last_report = int(state["tested"])
            print(
                "BULK_PROGRESS"
                + " family=" + family
                + " tested=" + str(state["tested"])
                + " naturalness_fail=" + str(state["naturalness_fail"])
                + " eft_fail=" + str(state["eft_fail"])
                + " energy_fail=" + str(state["energy_fail"])
                + " eligible=" + str(state["eligible"])
                + " best_j="
                + (
                    "NONE"
                    if state["best_energy_j"] is None
                    else format(float(state["best_energy_j"]), ".12e")
                )
                + " db_bytes=" + str(total_db_bytes()),
                flush=True,
            )

    persist_top(connection, family, version, top)
    persist_state(connection, state)

    print("=== BULK_FAMILY_DONE ===")
    print("FAMILY=" + family)
    print("TESTED=" + str(state["tested"]))
    print("NEXT_INDEX=" + str(state["next_index"]))
    print("NATURALNESS_FAIL=" + str(state["naturalness_fail"]))
    print("EFT_FAIL=" + str(state["eft_fail"]))
    print("ENERGY_FAIL=" + str(state["energy_fail"]))
    print("UNRESOLVED=" + str(state["unresolved"]))
    print("ELIGIBLE=" + str(state["eligible"]))
    print(
        "BEST_ENERGY_J="
        + (
            "NONE"
            if state["best_energy_j"] is None
            else format(float(state["best_energy_j"]), ".12e")
        )
    )

    return {
        "family": family,
        "family_version": version,
        "next_index": int(state["next_index"]),
        "target_index": int(state["target_index"]),
        "tested": int(state["tested"]),
        "analytic_fail": int(state["analytic_fail"]),
        "naturalness_fail": int(state["naturalness_fail"]),
        "eft_fail": int(state["eft_fail"]),
        "energy_fail": int(state["energy_fail"]),
        "unresolved": int(state["unresolved"]),
        "eligible": int(state["eligible"]),
        "best_energy_j": state["best_energy_j"],
        "best_candidate_id": state["best_candidate_id"],
        "top": top[:25],
    }


connection = sqlite3.connect(DB_PATH)
connection.row_factory = sqlite3.Row
connection.execute("PRAGMA journal_mode=WAL")
connection.execute("PRAGMA synchronous=NORMAL")
ensure_tables(connection)

plugins = [
    SourceAwareCollectiveCanonicalFamily(),
    SourceAwareCollectiveDBIFamily(),
]

print("=== AGMINER BULK MILLION PRECHECK ===")
print("POLICY_ID=" + POLICY_ID)
print("COMPARISON=" + COMPARISON)
print("ENERGY_LIMIT_J=" + format(LIMIT_J, ".12e"))
print("TARGET_PER_FAMILY=" + str(TARGET_PER_FAMILY))
print("TOTAL_TARGET=" + str(TARGET_PER_FAMILY * len(plugins)))
print("DB_BYTES_START=" + str(total_db_bytes()))

summaries = []

for plugin in plugins:
    if STOP["requested"]:
        break
    summaries.append(evaluate_family(connection, plugin))

connection.execute("PRAGMA wal_checkpoint(PASSIVE)")
connection.commit()
connection.close()

total_tested = sum(row["tested"] for row in summaries)
total_eligible = sum(row["eligible"] for row in summaries)
total_unresolved = sum(row["unresolved"] for row in summaries)

all_top = []
for row in summaries:
    for item in row["top"]:
        all_top.append(
            {
                "family": row["family"],
                "family_version": row["family_version"],
                **item,
            }
        )

all_top.sort(
    key=lambda item: (
        float(item["energy_j"]),
        str(item["candidate_id"]),
    )
)

summary = {
    "claim_class": "BULK_TIER0_LOWER_BOUND_SCREENING_ONLY",
    "policy_id": POLICY_ID,
    "comparison": COMPARISON,
    "energy_limit_j": LIMIT_J,
    "target_per_family": TARGET_PER_FAMILY,
    "total_target": TARGET_PER_FAMILY * len(plugins),
    "total_tested_reported": total_tested,
    "total_eligible": total_eligible,
    "total_unresolved": total_unresolved,
    "stop_requested": STOP["requested"],
    "stop_source": STOP["source"],
    "db_bytes_end": total_db_bytes(),
    "families": summaries,
    "best_overall": all_top[:25],
    "certified_antigravity_model_found": False,
}

SUMMARY_PATH.parent.mkdir(parents=True, exist_ok=True)
SUMMARY_PATH.write_text(
    json.dumps(summary, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)

print("")
print("=== AGMINER BULK MILLION SUMMARY ===")
print("TOTAL_TESTED_REPORTED=" + str(total_tested))
print("TOTAL_ELIGIBLE=" + str(total_eligible))
print("TOTAL_UNRESOLVED=" + str(total_unresolved))
print("STOP_REQUESTED=" + str(STOP["requested"]))
print("STOP_SOURCE=" + str(STOP["source"]))
print("DB_BYTES_END=" + str(total_db_bytes()))

if all_top:
    best = all_top[0]
    print("BEST_FAMILY=" + str(best["family"]))
    print("BEST_CANDIDATE=" + str(best["candidate_id"]))
    print("BEST_LOWER_BOUND_J=" + format(float(best["energy_j"]), ".12e"))
    print("BEST_ENERGY_STATE=" + str(best["energy_state"]))
else:
    print("BEST_CANDIDATE=NONE")

print("CERTIFIED_ANTIGRAVITY_MODEL_FOUND=NO")
