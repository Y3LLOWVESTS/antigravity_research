"""GRAVITY2-01 targeted scientific-scope guards."""

import ast
from pathlib import Path

import pytest

from antigravity_research.gravity2 import (
    action01_core as core,
)
from antigravity_research.gravity2 import (
    action01 as cli,
)


def test_scoped_negative_control():
    v = core.static_action_sign()
    assert v["status"] == "PASS_EXACT_SCOPED_STATIC_QUADRATIC"
    assert v["positive_K_cross_blocks_exact"] == [
        "4/3", "-4/3"
    ]
    assert v["not_the_full_R3B_action"] is True


def test_exact_witnesses_in_project_sources():
    p, trees = core.read_pinned(cli.ROOT)

    assert all(
        x["status"] == "MATCH"
        for x in p.values()
    )

    for name in core.PINS:
        assert all(
            x["status"] == "FOUND"
            for x in core.function_inventory(
                trees[name],
                core.WITNESSES[name],
            )
        )


def test_real_R3B_loaded_not_A12C_F2():
    assert "fdual_f_loaded_payload_homotopy" in (
        core.PINS["R3B_MIXED_LOADED"][0]
    )
    assert "f2_strong_payload_loading_rescue" in (
        core.PINS["A12C_F2_LOAD_NOT_R3B"][0]
    )
    assert (
        core.PINS["R3B_MIXED_LOADED"][1]
        != core.PINS["A12C_F2_LOAD_NOT_R3B"][1]
    )


def test_action_undertermination_explicit():
    a = core.audit(cli.ROOT)

    assert a["qualified_source_actions"] == 0
    assert a["physical_lift"] == "NOT_DERIVED"
    assert a["action_terms"][
        "finite_real_source_matter_action_and_JX_JY"
    ].startswith("NOT_")
    assert a["historical_loaded_result"] == "RECORDED_NOT_RERUN"


def test_l1_denied_without_changes():
    class A:
        level = "L1"
        workers = 1
        preset = "short"
        minutes = 1
        dry_run = True

    with pytest.raises(ValueError, match="L0 only"):
        cli.run(A())


def test_dry_run(capsys):
    class A:
        level = "L0"
        workers = 1
        preset = "quick"
        minutes = 0.5
        dry_run = True

    assert cli.run(A()) == 0
    assert "no_legacy_imports" in capsys.readouterr().out


def test_path_escape_rejected():
    with pytest.raises(ValueError):
        cli.checked_id("../agminer.sqlite3")


def test_never_import_legacy_agminer():
    here = Path(cli.__file__).parent

    for name in cli.SOURCES:
        t = ast.parse(
            (here/name).read_text()
        )

        imports = []

        for n in ast.walk(t):
            if isinstance(n, ast.Import):
                imports += [
                    x.name for x in n.names
                ]

            if isinstance(n, ast.ImportFrom) and n.module:
                imports.append(n.module)

        assert not any(
            "agminer" in v.lower()
            for v in imports
        )
