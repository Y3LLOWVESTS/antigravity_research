"""
Compact AGMINER logging and summary views.
"""

from __future__ import annotations

import csv
import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

from .pareto import mechanism_pareto_frontier, pareto_frontier
from .storage import Storage


def configure_logging(
    path: str | Path,
    *,
    max_mb: int = 2,
    backup_count: int = 2,
) -> logging.Logger:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("antigravity_research.agminer")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if not logger.handlers:
        handler = RotatingFileHandler(
            destination,
            maxBytes=max_mb * 1024 * 1024,
            backupCount=backup_count,
            encoding="utf-8",
        )

        formatter = logging.Formatter(
            "%(asctime)s %(levelname)s %(message)s"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def _write_csv(
    path: Path,
    rows: list[dict[str, Any]],
    fieldnames: list[str],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
        )

        writer.writeheader()

        for row in rows:
            writer.writerow(row)


def rebuild_summaries(
    storage: Storage,
    output_dir: str | Path,
) -> dict[str, Any]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    top_rows = storage.top_rows(25)
    survivor_rows = storage.survivor_rows()
    pareto_rows = pareto_frontier(survivor_rows)
    mechanism_rows = storage.mechanism_rows()
    mechanism_pareto_rows = mechanism_pareto_frontier(mechanism_rows)
    oracle_rows = storage.oracle_rows()
    scaling_rows = storage.collective_scaling_rows()

    failure_rows = [
        dict(row)
        for row in storage.failure_counts()
    ]

    _write_csv(
        output / "top_candidates.csv",
        top_rows,
        [
            "candidate_id",
            "family",
            "energy_j",
            "payload_surface_min",
            "naturalness_margin",
            "stability_margin",
            "leakage",
            "backreaction",
            "state",
        ],
    )

    _write_csv(
        output / "pareto_frontier.csv",
        pareto_rows,
        [
            "candidate_id",
            "family",
            "family_version",
            "energy_j",
            "payload_cm",
            "payload_surface_min",
            "naturalness_margin",
            "stability_margin",
            "leakage",
            "backreaction",
            "state",
            "tier",
        ],
    )

    _write_csv(
        output / "mechanism_frontier.csv",
        mechanism_pareto_rows,
        [
            "candidate_id",
            "family",
            "family_version",
            "energy_j",
            "oracle_energy_j",
            "realization_gap",
            "response_per_complete_joule",
            "productive_participation",
            "kernel_relative",
            "cancellation_ratio",
            "scaffolding_fraction",
            "organization_headroom",
            "state",
        ],
    )

    _write_csv(
        output / "oracle_learning.csv",
        oracle_rows,
        [
            "candidate_id",
            "family",
            "family_version",
            "energy_j",
            "canonical_invariant_id",
            "proven_lower_bound_j",
            "relaxed_complete_energy_j",
            "realized_complete_energy_j",
            "ledger_scope",
            "normalization_invariant",
            "naturalness_screened",
            "universal_metric_screened",
            "trusted_for_reachability",
            "priority",
            "realization_gap",
            "proof_reference",
        ],
    )

    _write_csv(
        output / "collective_scaling.csv",
        scaling_rows,
        [
            "family",
            "family_version",
            "probe_id",
            "sample_count",
            "response_exponent",
            "energy_exponent",
            "efficiency_exponent",
            "scaffold_exponent",
            "beneficial_collective_scaling",
            "proof_reference",
        ],
    )

    _write_csv(
        output / "failure_counts.csv",
        failure_rows,
        [
            "failure_code",
            "gate",
            "count",
        ],
    )

    summary = {
        "model_count": storage.model_count(),
        "rejection_count": storage.rejection_count(),
        "survivor_count": len(survivor_rows),
        "pareto_count": len(pareto_rows),
        "mechanism_metric_count": len(mechanism_rows),
        "mechanism_pareto_count": len(mechanism_pareto_rows),
        "action_oracle_count": len(oracle_rows),
        "collective_scaling_count": len(scaling_rows),
        "database_bytes": (
            storage.path.stat().st_size
            if storage.path.exists()
            else 0
        ),
        "stop_requested": storage.stop_requested(),
    }

    with (
        output / "run_summary.json"
    ).open(
        "w",
        encoding="utf-8",
    ) as handle:
        json.dump(
            summary,
            handle,
            indent=2,
            sort_keys=True,
        )
        handle.write("\n")

    return summary
