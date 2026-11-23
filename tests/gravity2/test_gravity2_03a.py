"""GRAVITY2-03A focused scientific and isolation tests."""

import ast
from pathlib import Path
from types import SimpleNamespace

import pytest

from antigravity_research.gravity2 import bridge03a as g


def test_mixed_4d_invariant():
    result = g.exact_4d()
    assert result["P_minkowski_control"] == "2"
    assert result["dP_metric_variation_residual"] == "0"


def test_metric_hodge_variation():
    result = g.exact_4d()
    assert result[
        "metric_Hodge_chain_variation_residual"
    ] == "0"
    assert result[
        "wrong_no_Hodge_negative_control"
    ] == "NONZERO"


def test_two_4d_ward_identities():
    result = g.exact_4d()
    assert set(result["source_ward"]) == {"X", "Y"}
    assert all(
        status == "ZERO_OFF_SHELL_FULL_4D_SOURCE_JET"
        for status in result["source_ward"].values()
    )


def test_authoritative_parent_hashes():
    result = g.audit()
    assert result["decision"].startswith(
        "BLOCKED_FOR_LOADED_SOLVER"
    )
    assert all(
        p["expected_sha256"] == p["actual_sha256"]
        for p in result["parent_locks"].values()
    )


def test_no_loaded_solver_promotion():
    result = g.audit()
    assert result["loaded_PDE_executed"] is False
    assert result["qualified_survivors"] == 0
    assert result["complete_covariant_action"] == "NOT_DERIVED"
    assert "NOT_AUTHORIZED" in result["gates"]["G06_LOAD"]


def test_historical_negative_control_preserved():
    result = g.audit()
    assert (
        result["original_R3B_historical_loaded_min_m_s2"]
        == -129.67185782242464
    )
    assert (
        result["original_R3B_prescribed_capacity_J"]
        == 1.5429162116460216
    )


def test_dry_run(capsys):
    args = SimpleNamespace(
        level="L0",
        workers=1,
        preset="quick",
        minutes=0.5,
        dry_run=True,
    )

    assert g.run(args) == 0
    assert "DISABLED" in capsys.readouterr().out


def test_l1_denied():
    args = SimpleNamespace(
        level="L1",
        workers=1,
        preset="short",
        minutes=1,
        dry_run=True,
    )

    with pytest.raises(ValueError):
        g.run(args)


def test_no_legacy_miner_import():
    folder = Path(g.__file__).parent

    for name in g.SOURCES:
        tree = ast.parse(
            (folder/name).read_text()
        )

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                assert all(
                    "agminer" not in item.name.lower()
                    for item in node.names
                )

            if (
                isinstance(node, ast.ImportFrom)
                and node.module
            ):
                assert (
                    "agminer" not in node.module.lower()
                )
