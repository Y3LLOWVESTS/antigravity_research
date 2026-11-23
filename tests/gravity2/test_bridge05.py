"""GRAVITY2-05 exact theorem, scope and isolation tests."""
from types import SimpleNamespace
from pathlib import Path
import ast

import pytest

from antigravity_research.gravity2 import (
    bridge05_core as c,
    bridge05 as r,
    bridge05_check as v,
)


def test_weighted_static_exact():
    a = c.weighted_static_identity()
    assert a["residual"] == "0"
    assert a["nonconstant_weight_derivative_required"]
    assert a["omitted_grad_weight_negative_control"] == "NONZERO"


def test_static_scope_no_harmonic_no_go():
    a = c.weighted_static_identity()
    assert "D0_ZERO" in a["conditional_no_go"]
    assert "DOES_NOT_EXCLUDE_HARMONIC" in a["scope"]


def test_jordan_trace_hessian():
    a = c.portal_source_hessian()
    assert a["trace_identity_residual"] == "0"
    assert a["mixed_source_F_reciprocity_residual"] == "0"
    assert a["mixed_FX_FY_includes_P_second_derivative"]


def test_schur_scoped_not_gravity():
    a = c.portal_source_hessian()
    assert a["restricted_positive_Huu_schur"] == "11/3"
    assert a["loaded_force_sign"] == "NOT_DETERMINED"


def test_prior_higgs_erratum():
    a = c.corrected_higgs_scope()

    assert [
        a[n]["massless_U1_count_from_previous_scope"]
        for n in a
    ] == [2,1,0]

    assert all(
        x["source_in_physical_metric"]
        for x in a.values()
    )


def test_independent_algebra():
    assert v.independent_math()


def test_l2_rejected():
    with pytest.raises(ValueError):
        r.run(SimpleNamespace(
            level="L2",
            workers=1,
            preset="quick",
            minutes=.5,
            dry_run=True,
        ))


def test_dry_run(capsys):
    assert r.run(SimpleNamespace(
        level="L0",
        workers=1,
        preset="quick",
        minutes=.5,
        dry_run=True,
    )) == 0

    assert "NOT_AUTHORIZED" in capsys.readouterr().out


def test_path_rejected():
    with pytest.raises(ValueError):
        r.directory("../old_agminer")


def test_no_legacy_imports():
    pkg = Path(r.__file__).parent

    for name in r.SOURCES:
        tree = ast.parse(
            (pkg/name).read_text()
        )

        for n in ast.walk(tree):
            if isinstance(n,ast.Import):
                assert all(
                    "agminer" not in x.name.lower()
                    for x in n.names
                )

            if isinstance(n,ast.ImportFrom) and n.module:
                assert "agminer" not in n.module.lower()
