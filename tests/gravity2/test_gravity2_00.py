"""GRAVITY2-00 guard tests; no legacy miner imports or writes."""

import json
from pathlib import Path

import pytest

from antigravity_research.gravity2 import engine, policy


def test_presets_are_bounded():
    assert policy.PRESETS["quick"] == (60, 384, 4)
    assert policy.PRESETS["focused"] == (300, 768, 12)
    assert policy.GLOBAL_MIB == 200


def test_legacy_paths_not_output():
    assert "results/gravity2" in str(engine.OUTPUT)
    assert "results/agminer" not in str(engine.OUTPUT)
    assert engine.ROOT == Path(__file__).resolve().parents[2]


def test_null_candidate_only():
    assert (
        policy.ANCHORS["prescribed_mixed_field_capacity_j"]
        == 1.5429162116460216
    )
    assert (
        policy.ANCHORS["historical_loaded_min_acceleration_m_s2"]
        < 0
    )


def test_atomic_no_overwrite(tmp_path):
    p = tmp_path / "science.json"

    engine.atomic_json(p, {"test": True})

    with pytest.raises(FileExistsError):
        engine.atomic_json(p, {"test": False})

    assert json.loads(p.read_text()) == {"test": True}


def test_nonfinite_fails_closed(tmp_path):
    with pytest.raises(ValueError):
        engine.atomic_json(
            tmp_path / "bad.json",
            {"nan": float("nan")},
        )

    assert not (tmp_path / "bad.json").exists()


def test_run_id_traversal_rejected():
    with pytest.raises(ValueError):
        engine.run_id_path(
            "../../agminer/agminer.sqlite3"
        )


def test_scientific_escalation_closed(capsys):
    result = engine.main([
        "run",
        "--level", "L2",
        "--preset", "focused",
        "--minutes", "1",
        "--dry-run",
    ])

    assert result == 2
    assert "implements L0 only" in capsys.readouterr().err


def test_dry_run_no_repo_writes(capsys):
    result = engine.main([
        "run",
        "--dry-run",
        "--minutes", "0.1",
    ])

    assert result == 0
    assert "DRY_RUN_NO_WRITES" in capsys.readouterr().out
