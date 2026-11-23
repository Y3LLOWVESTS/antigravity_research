"""Scoped GRAVITY2-02 guards."""
import ast
from pathlib import Path

import pytest

from antigravity_research.gravity2 import (
    action02_core as core,
    action02 as cli,
)


def test_exact_symbolic_identities():
    x=core.symbolic_gate()
    assert x["metric_variation_residual"]=="0"
    assert x["transverse_reciprocity_residual"]=="0"
    assert x["charged_scalar_one_coordinate_Ward_residual"]=="0"


def test_point_charge_control():
    x=core.symbolic_gate()
    assert x["point_charge_self_energy_limit"]=="POSITIVE_INFINITY"


def test_distinct_action_cases():
    assert len(core.CANDIDATES)==3
    assert len({c["family"] for c in core.CANDIDATES})==3


def test_no_certified_action():
    a=core.audit(cli.ROOT)
    assert a["decision"]=="SCOPED_ACTION_TEMPLATE_ATLAS_NO_PROMOTION"
    assert a["qualified_survivors"]==0
    assert a["complete_action"]=="NOT_DERIVED"


def test_parent_sources_locked():
    a=core.audit(cli.ROOT)
    assert all(
        p["status"]=="MATCH"
        for p in a["historical_files"].values()
    )


def test_l1_rejected():
    class Args:
        level="L1"
        workers=1
        preset="quick"
        minutes=0.5
        dry_run=True
    with pytest.raises(ValueError):
        cli.execute(Args())


def test_dry_run_no_output(capsys):
    class Args:
        level="L0"
        workers=1
        preset="quick"
        minutes=0.5
        dry_run=True
    assert cli.execute(Args())==0
    assert "DRY_RUN_NO_WRITES" in capsys.readouterr().out


def test_no_legacy_imports_or_execution():
    root=Path(cli.__file__).resolve().parent
    for name in cli.FILES:
        tree=ast.parse((root/name).read_text())
        for node in ast.walk(tree):
            if isinstance(node,ast.Import):
                assert all(
                    "agminer" not in n.name.lower()
                    for n in node.names
                )
            if isinstance(node,ast.ImportFrom) and node.module:
                assert "agminer" not in node.module.lower()
