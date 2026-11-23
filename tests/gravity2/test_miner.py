"""GRAVITY2 autonomous framework tests (no old miner execution)."""

import ast
from pathlib import Path
from types import SimpleNamespace

import pytest

from antigravity_research.gravity2 import (
    miner,
    miner_cases as c,
    miner_verify as v,
)


def test_registry_dedup():
    r = c.registry()
    assert len(r) == 3
    assert len({x["fingerprint"] for x in r}) == 3
    assert len([
        x for x in r
        if x["family"] != "NEGATIVE_CONTROL"
    ]) <= 2


def test_static_obstruction_scope():
    r = c.static_integrated_identity()
    assert r["verdict"] == "FAIL_SCOPED"
    assert "NOT A NO-GO" in r["scope"]


def test_stationary_not_promoted():
    r = c.evaluate("C1_HARMONIC_PHASE", "L1")
    assert r["gate_G05"]["verdict"] == "UNDERDETERMINED"
    assert not r["loaded_simulation"]


def test_zero_source_negative_control():
    r = c.evaluate("NULL_ZERO_SOURCE", "L0")
    assert r["gate_G05"]["verdict"] == "FAIL_SCOPED"


def test_source_standalone_checks():
    assert v._independent_static_control()
    assert v._independent_stationary_control()


def test_l2_not_authorized():
    a = SimpleNamespace(
        level="L2",
        workers=1,
        preset="focused",
        minutes=1,
        dry_run=True,
    )
    with pytest.raises(ValueError):
        miner.run(a)


def test_dry_run_writes_nothing(capsys):
    a = SimpleNamespace(
        level="L1",
        workers=1,
        preset="quick",
        minutes=1,
        dry_run=True,
    )
    assert miner.run(a) == 0
    assert '"writes": "NONE"' in capsys.readouterr().out


def test_traversal_refused():
    with pytest.raises(ValueError):
        miner.run_dir("../agminer")


def test_no_agminer_imports():
    base = Path(miner.__file__).parent

    for name in miner.SOURCE_FILES:
        tree = ast.parse((base/name).read_text())

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                assert all(
                    "agminer" not in alias.name
                    for alias in node.names
                )

            if (
                isinstance(node, ast.ImportFrom)
                and node.module
            ):
                assert "agminer" not in node.module
