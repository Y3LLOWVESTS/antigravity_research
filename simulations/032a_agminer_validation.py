"""
032A AGMINER infrastructure validation.

Purpose
-------
Validate the miner itself before any real 032 theory is introduced.

This run checks:

- deterministic candidate identities through the unit-test stack;
- exact 10 GJ boundary behavior;
- historical >10-GJ objective controls;
- early naturalness rejection;
- persistent terminal failure memory;
- duplicate skip behavior;
- compact SQLite storage;
- live summary reconstruction.

This is not a new antigravity physics result.
"""

from __future__ import annotations

from pathlib import Path

from antigravity_research.agminer.candidate import Candidate
from antigravity_research.agminer.config import (
    config_fingerprint,
    load_config,
)
from antigravity_research.agminer.energy import (
    hard_energy_gate,
)
from antigravity_research.agminer.families.family_031_control import (
    historical_energy_controls,
)
from antigravity_research.agminer.families.family_mock_validation import (
    unprotected_sub10_control,
)
from antigravity_research.agminer.naturalness import (
    naturalness_gate,
)
from antigravity_research.agminer.reporting import (
    configure_logging,
    rebuild_summaries,
)
from antigravity_research.agminer.storage import Storage


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "agminer_032a.json"

config = load_config(CONFIG_PATH)

database_path = ROOT / str(
    config["database_path"]
)

log_path = ROOT / str(
    config["log_path"]
)

output_dir = ROOT / "results" / "agminer"

logger = configure_logging(
    log_path,
    max_mb=int(
        config["logging_limit_mb"]
    ),
    backup_count=int(
        config["logging_backup_count"]
    ),
)

storage = Storage(database_path)

run_id = "032A_INFRASTRUCTURE_VALIDATION_V1"

storage.start_run(
    run_id=run_id,
    family="032A_INFRASTRUCTURE",
    family_version="1",
    config_fingerprint=config_fingerprint(
        config
    ),
    sampler_seed=int(
        config["sampler_seed"]
    ),
)

storage.clear_stop()

print(
    "=== 032A AGMINER INFRASTRUCTURE VALIDATION ==="
)
print(
    "REAL_032_PHYSICS_SEARCH=NOT_AUTHORIZED"
)

logger.info(
    "032A infrastructure validation started"
)

boundary_values_mj = [
    9.999999,
    10.000000000,
    10.000001,
]

boundary_expected = [
    True,
    False,
    False,
]

boundary_observed: list[bool] = []

for value_mj in boundary_values_mj:
    decision = hard_energy_gate(
        value_mj * 1.0e6
    )

    boundary_observed.append(
        decision.passed
    )

    print(
        f"BOUNDARY_{value_mj:.9f}_MJ="
        f"{'PASS' if decision.passed else 'REJECT'}"
    )

boundary_pass = (
    boundary_observed
    == boundary_expected
)

historical_evaluated = 0
historical_skipped = 0

for control in historical_energy_controls():
    candidate = Candidate(
        family_id="031_HISTORICAL_ENERGY_CONTROL",
        family_version="1",
        params={
            "name": control.name,
            "energy_j": control.energy_j,
        },
        physical_model_version=(
            "031_HISTORICAL_CONTROL_IMPORT_V1"
        ),
        energy_ledger_version=(
            "CONSERVATIVE_COMPLETE_V1"
        ),
    )

    if storage.is_terminal(
        candidate.candidate_id
    ):
        historical_skipped += 1
        continue

    storage.record_candidate(
        candidate,
        state="TIER0_RUNNING",
        run_id=run_id,
    )

    decision = hard_energy_gate(
        control.energy_j
    )

    if decision.passed:
        raise RuntimeError(
            "Historical >10-GJ control "
            "unexpectedly passed energy gate"
        )

    storage.reject(
        candidate.candidate_id,
        state=str(decision.state),
        failure_code=str(
            decision.failure_code
        ),
        gate="historical_energy_control",
        energy_j=control.energy_j,
        run_id=run_id,
    )

    historical_evaluated += 1

naturalness_candidate = (
    unprotected_sub10_control()
)

naturalness_evaluated = 0
naturalness_skipped = 0

if storage.is_terminal(
    naturalness_candidate.candidate_id
):
    naturalness_skipped = 1
else:
    storage.record_candidate(
        naturalness_candidate,
        state="TIER0_RUNNING",
        run_id=run_id,
    )

    naturalness = naturalness_gate(
        protection_specified=False,
        margin=0.0,
        threshold=float(
            config[
                "naturalness_threshold"
            ]
        ),
    )

    if naturalness.passed:
        raise RuntimeError(
            "Synthetic unprotected control "
            "unexpectedly passed naturalness"
        )

    storage.reject(
        naturalness_candidate.candidate_id,
        state=str(naturalness.state),
        failure_code=str(
            naturalness.failure_code
        ),
        gate="naturalness",
        energy_j=8.0e6,
        run_id=run_id,
    )

    naturalness_evaluated = 1

terminal_candidates = []

for control in historical_energy_controls():
    terminal_candidates.append(
        Candidate(
            family_id=(
                "031_HISTORICAL_ENERGY_CONTROL"
            ),
            family_version="1",
            params={
                "name": control.name,
                "energy_j": control.energy_j,
            },
            physical_model_version=(
                "031_HISTORICAL_CONTROL_IMPORT_V1"
            ),
            energy_ledger_version=(
                "CONSERVATIVE_COMPLETE_V1"
            ),
        )
    )

terminal_candidates.append(
    naturalness_candidate
)

second_pass_skips = sum(
    storage.is_terminal(
        candidate.candidate_id
    )
    for candidate in terminal_candidates
)

duplicate_memory_pass = (
    second_pass_skips
    == len(terminal_candidates)
)

summary = rebuild_summaries(
    storage,
    output_dir,
)

storage.checkpoint_wal()

database_bytes = (
    database_path.stat().st_size
    if database_path.exists()
    else 0
)

storage.finish_run(
    run_id,
    status=(
        "COMPLETED_GREEN"
        if (
            boundary_pass
            and duplicate_memory_pass
            and storage.region_rule_count()
            == 0
        )
        else "COMPLETED_RED"
    ),
)

logger.info(
    "032A infrastructure validation finished"
)

print()
print(
    f"HISTORICAL_ENERGY_CONTROLS="
    f"{len(historical_energy_controls())}"
)
print(
    f"HISTORICAL_FIRST_PASS_EVALUATED="
    f"{historical_evaluated}"
)
print(
    f"HISTORICAL_ALREADY_KNOWN="
    f"{historical_skipped}"
)
print(
    "SYNTHETIC_NATURALNESS_FIRST_PASS_EVALUATED="
    f"{naturalness_evaluated}"
)
print(
    "SYNTHETIC_NATURALNESS_ALREADY_KNOWN="
    f"{naturalness_skipped}"
)
print(
    f"SECOND_PASS_TERMINAL_SKIPS="
    f"{second_pass_skips}"
)
print(
    f"EXPECTED_SECOND_PASS_SKIPS="
    f"{len(terminal_candidates)}"
)
print(
    f"EXACT_REJECTION_REGION_RULES="
    f"{storage.region_rule_count()}"
)
print(
    f"MODEL_COUNT={summary['model_count']}"
)
print(
    f"REJECTION_COUNT="
    f"{summary['rejection_count']}"
)
print(
    f"DATABASE_BYTES={database_bytes}"
)
print(
    f"BOUNDARY_GATE="
    f"{'GREEN' if boundary_pass else 'RED'}"
)
print(
    f"FAILURE_MEMORY_GATE="
    f"{'GREEN' if duplicate_memory_pass else 'RED'}"
)
print(
    "NATURALNESS_EARLY_GATE="
    "GREEN"
)

validation_green = (
    boundary_pass
    and duplicate_memory_pass
    and storage.region_rule_count() == 0
)

print()
print(
    "032A_INFRASTRUCTURE_VALIDATION="
    f"{'GREEN' if validation_green else 'RED'}"
)

if validation_green:
    print(
        "NEXT="
        "STOP_RESUME_CRASH_AND_PARETO_"
        "INTEGRATION_VALIDATION"
    )
else:
    print(
        "NEXT="
        "REPAIR_AGMINER_CORE_BEFORE_"
        "ANY_NEW_PHYSICS"
    )

storage.close()
