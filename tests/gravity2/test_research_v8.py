"""Patch 6/7: bounded toy response, tamper, and planner controls."""
import json
import pytest
from antigravity_research.gravity2 import response_v7 as response
from antigravity_research.gravity2 import response_check_v7 as check
from antigravity_research.gravity2 import planner_v8 as planner
from antigravity_research.gravity2 import research_v8 as run


def test_reciprocity_with_independent_inverse():
    s=response.example(); r=response.compute(s)
    assert len(check.review(s,r))>=12
    assert r['complete_SI_energy']=='NOT_CERTIFIED'
    assert r['whole_craft_lift']=='NOT_DERIVED'
    assert abs(r['earth_coordinate_force_toy']+r['craft_coordinate_force_toy'])<1e-12


def test_source_relaxation_changes_response():
    r=response.compute(response.example())
    assert abs(r['loaded_field_response_toy'][0]-r['frozen_field_response_toy'][0])>1e-5


def test_nonsymmetric_action_rejected():
    s=response.example();s['A'][0][1]=1.
    with pytest.raises(ValueError,match='NO_COMMON'):
        response.compute(s)


def test_unhealthy_source_rejected():
    s=response.example();s['A'][0][0]=-1
    with pytest.raises(ValueError,match='UNHEALTHY'):
        response.compute(s)


def test_physical_claim_rejected():
    s=response.example();s['source_kind']='PHYSICAL_SOURCE'
    with pytest.raises(ValueError,match='NOT_DERIVED'):
        response.compute(s)


def test_fake_earth_reaction_rejected():
    s=response.example();r=response.compute(s)
    r['earth_coordinate_force_toy']=0
    with pytest.raises(ValueError,match='INDEPENDENT_TOY_REVIEW_HOLD'):
        check.review(s,r)


def test_planner_no_sourced_physics():
    s=response.example();r=response.compute(s);c=check.review(s,r)
    p=planner.select(r,c)
    assert p['next_gate']=='G01_ACTION'
    assert p['physically_authorized_runs']==0


def test_closed_failure_no_new_mechanism():
    s=response.example();r=response.compute(s);c=check.review(s,r)
    p=planner.select(r,c,[{'id':'X','family':'M2','new_action_term':'','historical_obstruction_changed':'R3A','cheap_falsifier':'Ward'}])
    assert p['rejected_ideas'][0]['reason']=='NO_NEW_MECHANISM'


def test_novel_candidate_stays_unverified():
    s=response.example();r=response.compute(s);c=check.review(s,r)
    p=planner.select(r,c,[{'id':'X','family':'M2','new_action_term':'hypothetical covariant operator','historical_obstruction_changed':'R3A','cheap_falsifier':'Ward'}])
    assert p['unverified_ideas'][0]['status']=='UNVERIFIED_IDEA_ONLY'
    assert p['physically_authorized_runs']==0


def test_excess_candidates_rejected():
    s=response.example();r=response.compute(s);c=check.review(s,r)
    with pytest.raises(ValueError,match='MAX_TWO'):
        planner.select(r,c,[{},{},{}])


def test_dry_and_integrity_run(monkeypatch,tmp_path):
    monkeypatch.setattr(run,'BASE',tmp_path/'runs')
    monkeypatch.setattr(run,'source_locks',lambda:{'code':'pinned'})
    monkeypatch.setattr(run,'parent_locks',lambda:{'parents':'pinned'})
    assert run.run(dry=True)==0 and not run.BASE.exists()
    assert run.run()==0
    folder=next(run.BASE.iterdir())
    assert run.verify(folder)==0
    sci=json.loads((folder/'science.json').read_text())
    sci['whole_craft_lift']='DERIVED'
    (folder/'science.json').write_text(json.dumps(sci))
    assert run.verify(folder)==3


def test_source_provenance_drift(monkeypatch,tmp_path):
    monkeypatch.setattr(run,'BASE',tmp_path/'runs')
    monkeypatch.setattr(run,'source_locks',lambda:{'code':'pinned'})
    monkeypatch.setattr(run,'parent_locks',lambda:{'parents':'pinned'})
    assert run.run()==0
    folder=next(run.BASE.iterdir())
    monkeypatch.setattr(run,'source_locks',lambda:{'code':'tampered'})
    assert run.verify(folder)==3
