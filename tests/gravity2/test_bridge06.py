"""GRAVITY2-06 negative-control, correct-scope and operational safety tests."""
import ast
from pathlib import Path
from types import SimpleNamespace
import pytest
from antigravity_research.gravity2 import bridge06_core as core
from antigravity_research.gravity2 import bridge06 as runner
from antigravity_research.gravity2 import bridge06_check as verifier


def test_local_euler():
    a=core.stationary_local_variations()
    assert a['exact_Euler_derivatives']=='PASS'
    assert 'B*Pi' in a['Gauss_Euler']


def test_polarization_nonzero():
    a=core.stationary_local_variations()
    assert a['portal_polarization_nonzero_control']=='PASS'
    assert a['omit_portal_polarization_negative_control']=='FAIL_AS_REQUIRED'


def test_stationary_gauge():
    assert core.stationary_local_variations()['gauge_stationary_phase_shift_residual']=='0'


def test_wall_reduced_only():
    a=core.stationary_integral_and_wall()
    assert a['natural_Robin']=='w*n.grad(f)+kappa*f=0'
    assert a['material_wall_dynamical_traction']=='NOT_DERIVED'


def test_frozen_bound_not_exported():
    assert 'invalidates' in core.stationary_integral_and_wall()['full_portal_Gauss_difference']


def test_independent_algebra():
    assert verifier.independent_algebra().startswith('PASS_')


def test_decision_no_survivors():
    a=core.evidence()
    assert a['qualified_survivors']==0 and a['lift']=='NOT_DERIVED'
    assert 'SOURCE_UNDERDETERMINED' in a['decision']


def test_wrong_level_rejected():
    with pytest.raises(ValueError):
        runner.run(SimpleNamespace(level='L1',workers=1,preset='quick',minutes=.5,dry_run=True))


def test_dry_run(capsys):
    assert runner.run(SimpleNamespace(level='L0',workers=1,preset='quick',minutes=.5,dry_run=True))==0
    assert 'DISABLED' in capsys.readouterr().out


def test_no_path_escape():
    with pytest.raises(ValueError):
        runner.location('../agminer')


def test_no_legacy_import():
    pkg=Path(runner.__file__).parent
    for name in runner.SOURCES:
        tree=ast.parse((pkg/name).read_text())
        for node in ast.walk(tree):
            if isinstance(node,ast.Import):
                assert all('agminer' not in alias.name.lower() for alias in node.names)
            if isinstance(node,ast.ImportFrom) and node.module:
                assert 'agminer' not in node.module.lower()
