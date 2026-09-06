"""
SQLite persistence for AGMINER.

SQLite is authoritative for routine candidate metadata and rejection memory.
Ordinary rejected candidates retain no field arrays.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .candidate import Candidate
from .mechanism import MechanismMetrics
from .oracle import ActionOracle, CollectiveScalingAssessment, assess_oracle
from .policy import current_energy_policy


TERMINAL_STATES = {
    "REJECTED_TIER0",
    "REJECTED_NUMERICAL",
    "REJECTED_PAYLOAD",
    "REJECTED_CONSERVATION",
    "REJECTED_NATURALNESS",
    "REJECTED_EFT",
    "REJECTED_STABILITY",
    "REJECTED_LEAKAGE",
    "REJECTED_BACKREACTION",
    "CERTIFIED",
    "INVALIDATED_BY_LATER_GATE",
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Storage:
    """
    Transactional AGMINER database wrapper.

    Candidate evaluations should be committed promptly so completed work
    survives interruption.
    """

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(
            str(self.path),
            timeout=30.0,
        )

        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.execute("PRAGMA synchronous=NORMAL")
        self.connection.execute("PRAGMA foreign_keys=ON")

        self._create_schema()

    def close(self) -> None:
        self.connection.commit()
        self.connection.close()

    def _create_schema(self) -> None:
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS runs (
                run_id TEXT PRIMARY KEY,
                started_at TEXT NOT NULL,
                ended_at TEXT,
                status TEXT NOT NULL,
                family TEXT,
                family_version TEXT,
                config_fingerprint TEXT,
                sampler_seed INTEGER,
                tested_count INTEGER NOT NULL DEFAULT 0,
                known_skip_count INTEGER NOT NULL DEFAULT 0,
                best_energy_j REAL
            );

            CREATE TABLE IF NOT EXISTS models (
                candidate_id TEXT PRIMARY KEY,
                family TEXT NOT NULL,
                family_version TEXT NOT NULL,
                physical_model_version TEXT NOT NULL,
                energy_ledger_version TEXT NOT NULL,
                params_json TEXT NOT NULL,
                state TEXT NOT NULL,
                tier INTEGER NOT NULL DEFAULT 0,
                energy_j REAL,
                payload_cm REAL,
                payload_surface_min REAL,
                naturalness_margin REAL,
                stability_margin REAL,
                leakage REAL,
                backreaction REAL,
                runtime_s REAL,
                run_id TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS rejections (
                candidate_id TEXT PRIMARY KEY,
                failure_code TEXT NOT NULL,
                gate TEXT NOT NULL,
                energy_j REAL,
                run_id TEXT,
                rejected_at TEXT NOT NULL,
                FOREIGN KEY(candidate_id)
                    REFERENCES models(candidate_id)
            );

            CREATE TABLE IF NOT EXISTS survivors (
                candidate_id TEXT PRIMARY KEY,
                energy_rank INTEGER,
                pareto_flag INTEGER NOT NULL DEFAULT 0,
                checkpoint_path TEXT,
                certification_priority REAL,
                pinned INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY(candidate_id)
                    REFERENCES models(candidate_id)
            );

            CREATE TABLE IF NOT EXISTS region_rules (
                rule_id INTEGER PRIMARY KEY AUTOINCREMENT,
                family TEXT NOT NULL,
                family_version TEXT NOT NULL,
                rule_type TEXT NOT NULL,
                rule_json TEXT NOT NULL,
                proof_reference TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS mechanism_metrics (
                candidate_id TEXT PRIMARY KEY,
                net_response REAL NOT NULL,
                gross_response REAL NOT NULL,
                productive_charge_abs REAL NOT NULL,
                productive_energy_j REAL NOT NULL,
                complete_energy_j REAL NOT NULL,
                charge_per_productive_joule REAL NOT NULL,
                productive_participation REAL NOT NULL,
                scaffolding_fraction REAL NOT NULL,
                cancellation_ratio REAL NOT NULL,
                kernel_effective REAL NOT NULL,
                kernel_geometric_max REAL,
                kernel_relative REAL,
                response_per_complete_joule REAL NOT NULL,
                factorized_response_per_joule REAL NOT NULL,
                identity_relative_error REAL NOT NULL,
                organization_headroom REAL,
                charge_units TEXT NOT NULL,
                decomposition_version TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(candidate_id)
                    REFERENCES models(candidate_id)
            );

            CREATE TABLE IF NOT EXISTS action_oracles (
                candidate_id TEXT PRIMARY KEY,
                canonical_invariant_id TEXT NOT NULL,
                proven_lower_bound_j REAL,
                relaxed_complete_energy_j REAL,
                realized_complete_energy_j REAL,
                ledger_scope TEXT NOT NULL,
                normalization_invariant INTEGER NOT NULL,
                naturalness_screened INTEGER NOT NULL,
                universal_metric_screened INTEGER NOT NULL,
                trusted_for_reachability INTEGER NOT NULL,
                priority TEXT NOT NULL,
                realization_gap REAL,
                proof_reference TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY(candidate_id)
                    REFERENCES models(candidate_id)
            );

            CREATE TABLE IF NOT EXISTS collective_scaling (
                family TEXT NOT NULL,
                family_version TEXT NOT NULL,
                probe_id TEXT NOT NULL,
                sample_count INTEGER NOT NULL,
                response_exponent REAL NOT NULL,
                energy_exponent REAL NOT NULL,
                efficiency_exponent REAL NOT NULL,
                scaffold_exponent REAL,
                beneficial_collective_scaling INTEGER NOT NULL,
                proof_reference TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                PRIMARY KEY(family, family_version, probe_id)
            );

            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );
            """
        )

        self.connection.commit()

    def start_run(
        self,
        *,
        run_id: str,
        family: str,
        family_version: str,
        config_fingerprint: str,
        sampler_seed: int,
    ) -> None:
        now = _utc_now()

        self.connection.execute(
            """
            INSERT INTO runs (
                run_id,
                started_at,
                status,
                family,
                family_version,
                config_fingerprint,
                sampler_seed
            )
            VALUES (?, ?, 'RUNNING', ?, ?, ?, ?)
            ON CONFLICT(run_id) DO UPDATE SET
                status='RUNNING',
                family=excluded.family,
                family_version=excluded.family_version,
                config_fingerprint=excluded.config_fingerprint,
                sampler_seed=excluded.sampler_seed
            """,
            (
                run_id,
                now,
                family,
                family_version,
                config_fingerprint,
                sampler_seed,
            ),
        )

        self.connection.commit()

    def finish_run(
        self,
        run_id: str,
        *,
        status: str = "COMPLETED",
    ) -> None:
        self.connection.execute(
            """
            UPDATE runs
            SET ended_at=?, status=?
            WHERE run_id=?
            """,
            (
                _utc_now(),
                status,
                run_id,
            ),
        )

        self.connection.commit()

    def record_candidate(
        self,
        candidate: Candidate,
        *,
        state: str = "NEW",
        tier: int = 0,
        run_id: str | None = None,
    ) -> None:
        now = _utc_now()

        params_json = json.dumps(
            candidate.params,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )

        self.connection.execute(
            """
            INSERT OR IGNORE INTO models (
                candidate_id,
                family,
                family_version,
                physical_model_version,
                energy_ledger_version,
                params_json,
                state,
                tier,
                run_id,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                candidate.candidate_id,
                candidate.family_id,
                candidate.family_version,
                candidate.physical_model_version,
                candidate.energy_ledger_version,
                params_json,
                state,
                tier,
                run_id,
                now,
                now,
            ),
        )

        self.connection.commit()

    def candidate_state(
        self,
        candidate_id: str,
    ) -> str | None:
        row = self.connection.execute(
            """
            SELECT state
            FROM models
            WHERE candidate_id=?
            """,
            (candidate_id,),
        ).fetchone()

        if row is None:
            return None

        return str(row["state"])

    def is_terminal(
        self,
        candidate_id: str,
    ) -> bool:
        state = self.candidate_state(candidate_id)

        if state is None:
            return False

        prefix = "REJECTED_ENERGY_OBJECTIVE:"

        if state.startswith(prefix):
            current_id = str(current_energy_policy()["policy_id"])
            return state == prefix + current_id

        return state in TERMINAL_STATES

    def set_state(
        self,
        candidate_id: str,
        state: str,
        *,
        tier: int | None = None,
    ) -> None:
        if tier is None:
            self.connection.execute(
                """
                UPDATE models
                SET state=?, updated_at=?
                WHERE candidate_id=?
                """,
                (
                    state,
                    _utc_now(),
                    candidate_id,
                ),
            )
        else:
            self.connection.execute(
                """
                UPDATE models
                SET state=?, tier=?, updated_at=?
                WHERE candidate_id=?
                """,
                (
                    state,
                    tier,
                    _utc_now(),
                    candidate_id,
                ),
            )

        self.connection.commit()

    def reject(
        self,
        candidate_id: str,
        *,
        state: str,
        failure_code: str,
        gate: str,
        energy_j: float | None,
        run_id: str | None,
    ) -> None:
        now = _utc_now()

        with self.connection:
            self.connection.execute(
                """
                UPDATE models
                SET state=?,
                    energy_j=COALESCE(?, energy_j),
                    updated_at=?
                WHERE candidate_id=?
                """,
                (
                    state,
                    energy_j,
                    now,
                    candidate_id,
                ),
            )

            self.connection.execute(
                """
                INSERT INTO rejections (
                    candidate_id,
                    failure_code,
                    gate,
                    energy_j,
                    run_id,
                    rejected_at
                )
                VALUES (?, ?, ?, ?, ?, ?)
                ON CONFLICT(candidate_id) DO UPDATE SET
                    failure_code=excluded.failure_code,
                    gate=excluded.gate,
                    energy_j=excluded.energy_j,
                    run_id=excluded.run_id,
                    rejected_at=excluded.rejected_at
                """,
                (
                    candidate_id,
                    failure_code,
                    gate,
                    energy_j,
                    run_id,
                    now,
                ),
            )

    def record_survivor(
        self,
        candidate_id: str,
        *,
        state: str,
        tier: int,
        energy_j: float,
        payload_cm: float,
        payload_surface_min: float,
        naturalness_margin: float,
        stability_margin: float,
        leakage: float,
        backreaction: float,
    ) -> None:
        now = _utc_now()

        with self.connection:
            self.connection.execute(
                """
                UPDATE models
                SET state=?,
                    tier=?,
                    energy_j=?,
                    payload_cm=?,
                    payload_surface_min=?,
                    naturalness_margin=?,
                    stability_margin=?,
                    leakage=?,
                    backreaction=?,
                    updated_at=?
                WHERE candidate_id=?
                """,
                (
                    state,
                    tier,
                    energy_j,
                    payload_cm,
                    payload_surface_min,
                    naturalness_margin,
                    stability_margin,
                    leakage,
                    backreaction,
                    now,
                    candidate_id,
                ),
            )

            self.connection.execute(
                """
                INSERT INTO survivors (
                    candidate_id,
                    pareto_flag
                )
                VALUES (?, 0)
                ON CONFLICT(candidate_id) DO NOTHING
                """,
                (candidate_id,),
            )

    def record_mechanism_metrics(
        self,
        candidate_id: str,
        metrics: MechanismMetrics,
    ) -> None:
        record = metrics.to_record()

        if record["identity_relative_error"] > 1.0e-10:
            raise ValueError("mechanism factorization identity failed")

        self.connection.execute(
            """
            INSERT INTO mechanism_metrics (
                candidate_id,
                net_response,
                gross_response,
                productive_charge_abs,
                productive_energy_j,
                complete_energy_j,
                charge_per_productive_joule,
                productive_participation,
                scaffolding_fraction,
                cancellation_ratio,
                kernel_effective,
                kernel_geometric_max,
                kernel_relative,
                response_per_complete_joule,
                factorized_response_per_joule,
                identity_relative_error,
                organization_headroom,
                charge_units,
                decomposition_version,
                updated_at
            )
            VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            ON CONFLICT(candidate_id) DO UPDATE SET
                net_response=excluded.net_response,
                gross_response=excluded.gross_response,
                productive_charge_abs=excluded.productive_charge_abs,
                productive_energy_j=excluded.productive_energy_j,
                complete_energy_j=excluded.complete_energy_j,
                charge_per_productive_joule=excluded.charge_per_productive_joule,
                productive_participation=excluded.productive_participation,
                scaffolding_fraction=excluded.scaffolding_fraction,
                cancellation_ratio=excluded.cancellation_ratio,
                kernel_effective=excluded.kernel_effective,
                kernel_geometric_max=excluded.kernel_geometric_max,
                kernel_relative=excluded.kernel_relative,
                response_per_complete_joule=excluded.response_per_complete_joule,
                factorized_response_per_joule=excluded.factorized_response_per_joule,
                identity_relative_error=excluded.identity_relative_error,
                organization_headroom=excluded.organization_headroom,
                charge_units=excluded.charge_units,
                decomposition_version=excluded.decomposition_version,
                updated_at=excluded.updated_at
            """,
            (
                candidate_id,
                record["net_response"],
                record["gross_response"],
                record["productive_charge_abs"],
                record["productive_energy_j"],
                record["complete_energy_j"],
                record["charge_per_productive_joule"],
                record["productive_participation"],
                record["scaffolding_fraction"],
                record["cancellation_ratio"],
                record["kernel_effective"],
                record["kernel_geometric_max"],
                record["kernel_relative"],
                record["response_per_complete_joule"],
                record["factorized_response_per_joule"],
                record["identity_relative_error"],
                record["organization_headroom"],
                record["charge_units"],
                record["decomposition_version"],
                _utc_now(),
            ),
        )
        self.connection.commit()

    def record_action_oracle(
        self,
        candidate_id: str,
        oracle: ActionOracle,
    ) -> None:
        assessment = assess_oracle(oracle)

        self.connection.execute(
            """
            INSERT INTO action_oracles (
                candidate_id,
                canonical_invariant_id,
                proven_lower_bound_j,
                relaxed_complete_energy_j,
                realized_complete_energy_j,
                ledger_scope,
                normalization_invariant,
                naturalness_screened,
                universal_metric_screened,
                trusted_for_reachability,
                priority,
                realization_gap,
                proof_reference,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(candidate_id) DO UPDATE SET
                canonical_invariant_id=excluded.canonical_invariant_id,
                proven_lower_bound_j=excluded.proven_lower_bound_j,
                relaxed_complete_energy_j=excluded.relaxed_complete_energy_j,
                realized_complete_energy_j=excluded.realized_complete_energy_j,
                ledger_scope=excluded.ledger_scope,
                normalization_invariant=excluded.normalization_invariant,
                naturalness_screened=excluded.naturalness_screened,
                universal_metric_screened=excluded.universal_metric_screened,
                trusted_for_reachability=excluded.trusted_for_reachability,
                priority=excluded.priority,
                realization_gap=excluded.realization_gap,
                proof_reference=excluded.proof_reference,
                updated_at=excluded.updated_at
            """,
            (
                candidate_id,
                oracle.canonical_invariant_id,
                oracle.proven_lower_bound_j,
                oracle.relaxed_complete_energy_j,
                oracle.realized_complete_energy_j,
                oracle.ledger_scope,
                int(oracle.normalization_invariant),
                int(oracle.naturalness_screened),
                int(oracle.universal_metric_screened),
                int(oracle.trusted_for_reachability),
                assessment.priority,
                assessment.realization_gap,
                oracle.proof_reference,
                _utc_now(),
            ),
        )
        self.connection.commit()

    def record_collective_scaling(
        self,
        *,
        family: str,
        family_version: str,
        probe_id: str,
        assessment: CollectiveScalingAssessment,
        proof_reference: str,
    ) -> None:
        if not proof_reference:
            raise ValueError("proof_reference is required")

        self.connection.execute(
            """
            INSERT INTO collective_scaling (
                family,
                family_version,
                probe_id,
                sample_count,
                response_exponent,
                energy_exponent,
                efficiency_exponent,
                scaffold_exponent,
                beneficial_collective_scaling,
                proof_reference,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(family, family_version, probe_id) DO UPDATE SET
                sample_count=excluded.sample_count,
                response_exponent=excluded.response_exponent,
                energy_exponent=excluded.energy_exponent,
                efficiency_exponent=excluded.efficiency_exponent,
                scaffold_exponent=excluded.scaffold_exponent,
                beneficial_collective_scaling=excluded.beneficial_collective_scaling,
                proof_reference=excluded.proof_reference,
                updated_at=excluded.updated_at
            """,
            (
                family,
                family_version,
                probe_id,
                assessment.sample_count,
                assessment.response_exponent,
                assessment.energy_exponent,
                assessment.efficiency_exponent,
                assessment.scaffold_exponent,
                int(assessment.beneficial_collective_scaling),
                proof_reference,
                _utc_now(),
            ),
        )
        self.connection.commit()

    def mechanism_rows(self) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            """
            SELECT
                m.candidate_id,
                m.family,
                m.family_version,
                m.energy_j,
                m.payload_surface_min,
                m.naturalness_margin,
                m.stability_margin,
                m.leakage,
                m.backreaction,
                m.state,
                mm.response_per_complete_joule,
                mm.productive_participation,
                mm.scaffolding_fraction,
                mm.cancellation_ratio,
                mm.kernel_relative,
                mm.organization_headroom,
                ao.relaxed_complete_energy_j AS oracle_energy_j,
                ao.realization_gap
            FROM models AS m
            JOIN mechanism_metrics AS mm
                ON mm.candidate_id=m.candidate_id
            LEFT JOIN action_oracles AS ao
                ON ao.candidate_id=m.candidate_id
            WHERE m.energy_j IS NOT NULL
            ORDER BY m.energy_j, m.candidate_id
            """
        ).fetchall()
        return [dict(row) for row in rows]

    def oracle_rows(self) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            """
            SELECT
                m.candidate_id,
                m.family,
                m.family_version,
                m.energy_j,
                ao.canonical_invariant_id,
                ao.proven_lower_bound_j,
                ao.relaxed_complete_energy_j,
                ao.realized_complete_energy_j,
                ao.ledger_scope,
                ao.normalization_invariant,
                ao.naturalness_screened,
                ao.universal_metric_screened,
                ao.trusted_for_reachability,
                ao.priority,
                ao.realization_gap,
                ao.proof_reference
            FROM action_oracles AS ao
            JOIN models AS m
                ON m.candidate_id=ao.candidate_id
            ORDER BY
                COALESCE(
                    ao.relaxed_complete_energy_j,
                    ao.realized_complete_energy_j,
                    m.energy_j
                ),
                m.candidate_id
            """
        ).fetchall()
        return [dict(row) for row in rows]

    def collective_scaling_rows(self) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            """
            SELECT
                family,
                family_version,
                probe_id,
                sample_count,
                response_exponent,
                energy_exponent,
                efficiency_exponent,
                scaffold_exponent,
                beneficial_collective_scaling,
                proof_reference
            FROM collective_scaling
            ORDER BY
                efficiency_exponent DESC,
                family,
                probe_id
            """
        ).fetchall()
        return [dict(row) for row in rows]

    def recover_interrupted_candidates(self) -> int:
        now = _utc_now()
        cursor = self.connection.execute(
            """
            UPDATE models
            SET state="REJECTED_NUMERICAL",
                updated_at=?
            WHERE state IN (
                "TIER0_RUNNING",
                "TIER1_RUNNING",
                "TIER2_RUNNING"
            )
            """,
            (now,),
        )

        recovered = int(cursor.rowcount)

        self.connection.commit()

        return recovered

    def failure_counts(self) -> list[sqlite3.Row]:
        return list(
            self.connection.execute(
                """
                SELECT
                    failure_code,
                    gate,
                    COUNT(*) AS count
                FROM rejections
                GROUP BY failure_code, gate
                ORDER BY count DESC, failure_code
                """
            )
        )

    def survivor_rows(self) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            """
            SELECT
                candidate_id,
                family,
                family_version,
                energy_j,
                payload_cm,
                payload_surface_min,
                naturalness_margin,
                stability_margin,
                leakage,
                backreaction,
                state,
                tier
            FROM models
            WHERE state IN (
                'TIER1_SURVIVOR',
                'TIER2_SURVIVOR',
                'CERTIFICATION_READY',
                'CERTIFICATION_IN_PROGRESS',
                'CERTIFIED'
            )
            ORDER BY energy_j, candidate_id
            """
        ).fetchall()

        return [dict(row) for row in rows]

    def top_rows(
        self,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        rows = self.connection.execute(
            """
            SELECT
                candidate_id,
                family,
                energy_j,
                payload_surface_min,
                naturalness_margin,
                stability_margin,
                leakage,
                backreaction,
                state
            FROM models
            WHERE state IN (
                'TIER1_SURVIVOR',
                'TIER2_SURVIVOR',
                'CERTIFICATION_READY',
                'CERTIFICATION_IN_PROGRESS',
                'CERTIFIED'
            )
            ORDER BY energy_j ASC, candidate_id ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

        return [dict(row) for row in rows]

    def model_count(self) -> int:
        row = self.connection.execute(
            "SELECT COUNT(*) AS count FROM models"
        ).fetchone()

        return int(row["count"])

    def rejection_count(self) -> int:
        row = self.connection.execute(
            "SELECT COUNT(*) AS count FROM rejections"
        ).fetchone()

        return int(row["count"])

    def region_rule_count(self) -> int:
        row = self.connection.execute(
            "SELECT COUNT(*) AS count FROM region_rules"
        ).fetchone()

        return int(row["count"])

    def add_region_rule(
        self,
        *,
        family: str,
        family_version: str,
        rule_type: str,
        rule: dict[str, Any],
        proof_reference: str,
    ) -> None:
        self.connection.execute(
            """
            INSERT INTO region_rules (
                family,
                family_version,
                rule_type,
                rule_json,
                proof_reference,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                family,
                family_version,
                rule_type,
                json.dumps(
                    rule,
                    sort_keys=True,
                    separators=(",", ":"),
                ),
                proof_reference,
                _utc_now(),
            ),
        )

        self.connection.commit()

    def set_metadata(
        self,
        key: str,
        value: str,
    ) -> None:
        self.connection.execute(
            """
            INSERT INTO metadata (
                key,
                value,
                updated_at
            )
            VALUES (?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET
                value=excluded.value,
                updated_at=excluded.updated_at
            """,
            (
                key,
                value,
                _utc_now(),
            ),
        )

        self.connection.commit()

    def get_metadata(
        self,
        key: str,
        default: str | None = None,
    ) -> str | None:
        row = self.connection.execute(
            """
            SELECT value
            FROM metadata
            WHERE key=?
            """,
            (key,),
        ).fetchone()

        if row is None:
            return default

        return str(row["value"])

    def request_stop(self) -> None:
        self.set_metadata("stop_requested", "1")

    def clear_stop(self) -> None:
        self.set_metadata("stop_requested", "0")

    def stop_requested(self) -> bool:
        return self.get_metadata(
            "stop_requested",
            "0",
        ) == "1"

    def checkpoint_wal(self) -> None:
        self.connection.commit()
        self.connection.execute("PRAGMA wal_checkpoint(PASSIVE)")
