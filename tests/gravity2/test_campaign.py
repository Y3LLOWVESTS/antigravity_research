"""GRAVITY2 campaign release: safety, evidence and science gate tests."""
from types import SimpleNamespace
import json
import pytest
from antigravity_research.gravity2 import campaign as r
from antigravity_research.gravity2 import campaign_science as m
from antigravity_research.gravity2 import campaign_check as v


def test_seed_distinct_and_bounded():
    t=m.default_tasks()
    assert len(t)==2
    assert len({j['candidate'] for j in t})==1
    assert [j['gate'] for j in t]==['ACTION_COMPLETENESS','CHARGE_BALANCE_CONTROL']
    assert all(r.validate_job(j) for j in t)


def test_local_action_compilation():
    assert m.symbolic_local_control()=='EXACT_OPPOSITE_CHARGE_VARIATION_AND_GAUGE_SHIFT'


def test_gauss_screen_from_parent():
    ev=m.charge_screen(r.ROOT,m.default_tasks()[0]['action'])
    assert len(ev['rows'])==4
    assert ev['status']=='SCOPED_CONTROL_ONLY'
    assert all(row['single_charge']>16 for row in ev['rows'])
    assert all(abs(row['zero_mode_adjusted_charge'])<1e-11 for row in ev['rows'])
    assert all(row['scalar_and_X_stationary']=='NOT_TESTED' for row in ev['rows'])
    assert all(v.independent_check(m.default_tasks()[1],ev,{}) .values())


def test_completeness_blocks():
    j=m.default_tasks()[0]
    ev=m.completeness(j['action'])
    assert ev['status']=='BLOCKED_ACTION_INCOMPLETE'
    assert 'Earth_action' in ev['missing_action_terms']
    assert all(v.independent_check(j,ev,{}).values())


def test_fidelity_lock():
    with pytest.raises(ValueError):
        r.execute(SimpleNamespace(level='L2',workers=1,preset='quick',minutes=.5,
                   resume=None,dry_run=True,fresh=False))


def test_missing_action_not_promotion():
    for task in m.default_tasks():
        assert task['action']['source_support_action'] is None
        assert task['action']['metric_Hodge_variation_complete'] is False


def test_dry_run_has_no_writes(capsys):
    assert r.execute(SimpleNamespace(level='L1',workers=1,preset='quick',minutes=.5,
                   resume=None,dry_run=True,fresh=False))==0
    assert 'NONE' in capsys.readouterr().out


def test_provider_guard():
    j=m.default_tasks()[0]
    with pytest.raises(ValueError):r.validate_job({**j,'module':'evil'})
    with pytest.raises(ValueError):r.validate_job({**j,'independent':'campaign_science'})
    with pytest.raises(ValueError):r.validate_job({**j,'id':'../wrong'})


def test_order_dep_priority():
    a=dict(m.default_tasks()[0])
    b=dict(m.default_tasks()[1]);b['requires']=['JPAIR_ACTION_INVENTORY']
    b['priority']=100; a['priority']=90
    result=r.dispatch_order([b,a]);assert [x['id'] for x in result]==[
        'JPAIR_ACTION_INVENTORY','JPAIR_CHARGE_CONTROL']


def test_root_and_parent_pins():
    assert set(r.PARENTS)=={'G08_SCIENCE','G08_VERIFICATION','G07_ARCHIVE'}
    assert r.parent_locks()['G07_ARCHIVE']['match'] is True


def test_run_id_path():
    with pytest.raises(ValueError):r.locate('../escape')


def test_no_legacy_import_code():
    import ast
    for n in r.CORE_FILES:
        tree=ast.parse((r.PKG/n).read_text())
        for node in ast.walk(tree):
            if isinstance(node,ast.Import):
                assert all('agminer' not in a.name.lower() for a in node.names)
            if isinstance(node,ast.ImportFrom) and node.module:
                assert 'agminer' not in node.module.lower()
