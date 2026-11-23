"""GRAVITY2-08: periodic Gauss zero-mode and action-provenance audit."""
import ast
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from antigravity_research.gravity2 import bridge08_core as core
from antigravity_research.gravity2 import bridge08 as runner
from antigravity_research.gravity2 import bridge08_check as check

PARENT=runner.ROOT/runner.PARENT_DIR/'fields.npz'


def fields(n=15):
    with np.load(PARENT,allow_pickle=False) as ar:
        return tuple(ar[f'{k}_{n}'].copy() for k in 'afb')


def test_periodic_gauss_zero_mode():
    a,f,b=fields()
    r=core.one_row(a,f,b,15)
    assert r['charge_integral_canonical']>16
    assert r['periodic_divergence_integral']<1e-10
    assert abs(r['Gauss_integral_residual']+r['charge_integral_canonical'])<1e-10


def test_all_grids_same_charge_sign():
    with np.load(PARENT,allow_pickle=False) as ar:
        rows=core.scientific_evidence(ar)['rows']
    assert len(rows)==4
    assert all(r['rho_min']>.17 and r['charge_integral_canonical']>16 for r in rows)


def test_Y_only_and_source_offshell():
    a,f,b=fields()
    e=core.euler(a,f,b,2*np.pi/15)
    rms=lambda v:np.sqrt(np.mean(v*v))
    assert rms(e['b'])<1e-9
    assert rms(e['a'])>.4 and rms(e['f'])>.4


def test_x_maxwell_action_erratum():
    a,f,b=fields()
    h=2*np.pi/15
    old=core.action(a,f,b,h,include_x=False)
    new=core.action(a,f,b,h,include_x=True)
    assert new-old>.6


def test_uniform_background_not_physical_solution():
    a,f,b=fields()
    r=core.one_row(a,f,b,15)
    assert r['after_uniform_compensator_X_rms']>.1
    assert r['uniform_compensator_required_density']<-.3


def test_portal_off_still_charged():
    a,f,b=fields()
    p=core.pieces(a,f,b,2*np.pi/15,alpha=0,beta=0)
    assert np.min(p['rho'])>0


def test_q_zero_control_not_same_charge_source():
    a,f,b=fields()
    p=core.pieces(a,f,b,2*np.pi/15,q=0)
    assert np.max(np.abs(p['rho']))==0


def test_independent_symbolic():
    assert check.independent_symbolic()


def test_independent_FD():
    a,f,b=fields()
    err,signal=check.finite_differences(a,f,b,2*np.pi/15)
    assert all(err[z]<5e-7 and signal[z]>1e-6 for z in 'afb')


def test_level_lock():
    with pytest.raises(ValueError):
        runner.run(SimpleNamespace(
            level='L2',
            workers=1,
            preset='quick',
            minutes=.5,
            dry_run=True,
        ))


def test_dry_run(capsys):
    assert runner.run(SimpleNamespace(
        level='L0',
        workers=1,
        preset='quick',
        minutes=.5,
        dry_run=True,
    ))==0
    assert 'SEALED_G07_FIELDS_READ_ONLY' in capsys.readouterr().out


def test_path_escape():
    with pytest.raises(ValueError):
        runner.owned('../agminer')


def test_no_import_from_legacy():
    for filename in runner.SOURCE_NAMES[:3]:
        tree=ast.parse((runner.ROOT/filename).read_text())
        for node in ast.walk(tree):
            if isinstance(node,ast.Import):
                assert all(
                    'agminer' not in x.name.lower()
                    for x in node.names
                )
            if isinstance(node,ast.ImportFrom) and node.module:
                assert 'agminer' not in node.module.lower()
