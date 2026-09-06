"""Read-only SQLite inspection utilities for AGMINER.

These functions never create schemas, update metadata, or alter the
campaign database.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


def connect_readonly(path: str | Path) -> sqlite3.Connection:
    database = Path(path).resolve()

    if not database.exists():
        raise FileNotFoundError(database)

    uri = database.as_uri() + "?mode=ro"

    connection = sqlite3.connect(
        uri,
        uri=True,
        timeout=5.0,
    )

    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA query_only=ON")

    return connection


def status_snapshot(path: str | Path) -> dict[str, Any]:
    connection = connect_readonly(path)

    try:
        model_count = int(
            connection.execute(
                "SELECT COUNT(*) FROM models"
            ).fetchone()[0]
        )

        rejection_count = int(
            connection.execute(
                "SELECT COUNT(*) FROM rejections"
            ).fetchone()[0]
        )

        region_rule_count = int(
            connection.execute(
                "SELECT COUNT(*) FROM region_rules"
            ).fetchone()[0]
        )

        survivor_count = int(
            connection.execute(
                "SELECT COUNT(*) FROM survivors"
            ).fetchone()[0]
        )

        stop_row = connection.execute(
            "SELECT value FROM metadata WHERE key=?" ,
            ("stop_requested",),
        ).fetchone()

        stop_requested = (
            stop_row is not None
            and str(stop_row[0]) == "1"
        )

        return {
            "models": model_count,
            "rejections": rejection_count,
            "region_rules": region_rule_count,
            "survivors": survivor_count,
            "stop_requested": stop_requested,
        }
    finally:
        connection.close()


def failure_counts(path: str | Path) -> list[dict[str, Any]]:
    connection = connect_readonly(path)

    try:
        rows = connection.execute(
            """
            SELECT
                failure_code,
                gate,
                COUNT(*) AS count
            FROM rejections
            GROUP BY failure_code, gate
            ORDER BY count DESC, failure_code
            """
        ).fetchall()

        return [dict(row) for row in rows]
    finally:
        connection.close()


def top_rows(
    path: str | Path,
    limit: int = 10,
) -> list[dict[str, Any]]:
    connection = connect_readonly(path)

    try:
        rows = connection.execute(
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
                "TIER1_SURVIVOR",
                "TIER2_SURVIVOR",
                "CERTIFICATION_READY",
                "CERTIFICATION_IN_PROGRESS",
                "CERTIFIED"
            )
            ORDER BY energy_j ASC, candidate_id ASC
            LIMIT ?
            """,
            (int(limit),),
        ).fetchall()

        return [dict(row) for row in rows]
    finally:
        connection.close()


def survivor_rows(path: str | Path) -> list[dict[str, Any]]:
    connection = connect_readonly(path)

    try:
        rows = connection.execute(
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
                "TIER1_SURVIVOR",
                "TIER2_SURVIVOR",
                "CERTIFICATION_READY",
                "CERTIFICATION_IN_PROGRESS",
                "CERTIFIED"
            )
            ORDER BY energy_j ASC, candidate_id ASC
            """
        ).fetchall()

        return [dict(row) for row in rows]
    finally:
        connection.close()


def readonly_write_probe(path: str | Path) -> bool:
    connection = connect_readonly(path)

    try:
        try:
            connection.execute(
                "CREATE TABLE agminer_should_never_exist(x INTEGER)"
            )
        except sqlite3.OperationalError:
            return True

        return False
    finally:
        connection.close()
