"""GRAVITY2-04 offline source-action compiler tests."""

import ast
from pathlib import Path
from types import SimpleNamespace

import pytest

from antigravity_research.gravity2 import (
    miner2_math as m,
    miner2 as r,
    miner2_check as v,
)


def test_generated_actions_are_distinct():
    c = m.registry()
    assert len(c) == 4
    assert len({
        x["fingerprint"] for x in c
    }) == 4


def test_source_trace_operator():
    identity = m.identities()
    assert identity[
        "Jordan_source_extra_P_variation"
    ] == "NONZERO_GENERAL"
    assert identity[
        "4D_source_Ward_with_variable_conformal_weight"
    ] == "ZERO_OFF_SHELL"
    assert identity[
        "omitted_source_trace_control"
    ] == "NONZERO"


def test_two_action_frames():
    cards = m.registry()
    a,b = (
        m.evaluate(x)
        for x in cards[:2]
    )
    assert not a[
        "changes_portal_source_loading"
    ]
    assert b[
        "changes_portal_source_loading"
    ]
    assert (
        a["source_finite_stable"]
        == b["source_finite_stable"]
        == "NOT_ESTABLISHED"
    )


def test_exterior_higgs_mass_ranks():
    cards = m.registry()
    assert [
        m.evaluate(c)["massless_U1_count"]
        for c in cards
    ] == [2,2,1,0]


def test_negative_physics_controls():
    for c in m.registry():
        x = m.evaluate(c)
        assert not x[
            "qualified_physical_survivor"
        ]
        assert x[
            "R3B_coupled_loaded_solve"
        ] == "NOT_AUTHORIZED"


def test_independent_sympy():
    assert v.independent_math()[
        "jordan_portal_chain"
    ] == "ZERO_RESIDUAL"


def test_l2_rejected():
    a = SimpleNamespace(
        level="L2",
        workers=1,
        preset="focused",
        minutes=1,
        dry_run=True,
    )
    with pytest.raises(ValueError):
        r.run(a)


def test_dry_run(capsys):
    a = SimpleNamespace(
        level="L1",
        workers=1,
        preset="quick",
        minutes=0.5,
        dry_run=True,
    )
    assert r.run(a) == 0
    assert '"writes": "NONE"' in (
        capsys.readouterr().out
    )


def test_no_path_traversal():
    with pytest.raises(ValueError):
        r.run_dir("../agminer")


def test_no_legacy_imports():
    folder = Path(r.__file__).parent

    for name in r.SOURCES:
        t = ast.parse(
            (folder/name).read_text()
        )

        for node in ast.walk(t):
            if isinstance(node,ast.Import):
                assert all(
                    "agminer" not in item.name.lower()
                    for item in node.names
                )

            if (
                isinstance(node,ast.ImportFrom)
                and node.module
            ):
                assert "agminer" not in node.module.lower()
