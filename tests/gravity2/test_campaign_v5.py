"""GRAVITY2 v5 checkpoint/recovery adversarial regression."""
import json
from types import SimpleNamespace

import pytest

from antigravity_research.gravity2 import campaign_v5 as v5
from antigravity_research.gravity2 import campaign_check_v5 as checker


@pytest.fixture
def environment(tmp_path, monkeypatch):
    base = tmp_path / 'results/gravity2/campaign_v5_runs'
    base.mkdir(parents=True)

    source = tmp_path / 'fake_provider.py'
    source.write_text('SCIENCE = 1\n')

    jobs = [
        {
            'id': 'TASK_A',
            'requires': [],
            'level': 'L0',
            'gate': 'ACTION_COMPLETENESS',
            'module': 'fake_provider',
            'independent': 'fake_reviewer',
            'candidate': 'TEST',
            'action': {'source': 'toy'},
            'priority': 20,
            'schema': 'gravity2.campaign.task.v1',
        },
        {
            'id': 'TASK_B',
            'requires': ['TASK_A'],
            'level': 'L0',
            'gate': 'ACTION_COMPLETENESS',
            'module': 'fake_provider',
            'independent': 'fake_reviewer',
            'candidate': 'TEST',
            'action': {'source': 'toy'},
            'priority': 10,
            'schema': 'gravity2.campaign.task.v1',
        },
    ]

    monkeypatch.setattr(v5, 'ROOT', tmp_path)
    monkeypatch.setattr(v5, 'BASE', base)
    monkeypatch.setattr(
        v5, 'code_hashes', lambda: {'test': 'locked'}
    )
    monkeypatch.setattr(v5.v4, 'jobs', lambda: jobs)
    monkeypatch.setattr(
        v5.v4, 'core_hashes', lambda: {'test': 'v4'}
    )
    monkeypatch.setattr(
        v5.v4, 'provider_file', lambda *_: source
    )
    monkeypatch.setattr(
        v5.v4, 'parent_locks',
        lambda: {'parent': {'match': True}},
    )
    monkeypatch.setattr(
        v5.inputs, 'manifest', lambda *args: {'test': 'inputs'}
    )
    monkeypatch.setattr(
        v5.v4, 'reviewed_checks',
        lambda job, evidence: {'independent': True},
    )
    monkeypatch.setattr(
        v5.v4, 'validate_job', lambda job: job
    )
    monkeypatch.setattr(v5, '_rss_available', lambda: True)
    monkeypatch.setattr(v5, 'bytes_under', lambda *_: 0)

    return tmp_path, base, jobs


def create_interrupted(environment):
    root, base, jobs = environment
    rid = 'g2camp5_20261121T120000Z_abcdef12'
    folder = base / rid
    folder.mkdir()
    (folder / 'checkpoints').mkdir()

    manifest = {
        'schema': 'gravity2.campaign.v5',
        'run_id': rid,
        'code_sha256': {'test': 'locked'},
        'parents': {'parent': {'match': True}},
        'tasks': jobs,
        'tasks_sha256': v5.science.signature(jobs),
        'level': 'L0',
        'resume_from': None,
        'resume_checkpoint_sha256': None,
    }

    v5.atomic_json(folder / 'manifest.json', manifest)
    head = v5.commit(folder, [], [], '0' * 64)

    job = jobs[0]
    evidence = {'status': 'PASS_SCOPED'}
    target = folder / 'TASK_A.json'
    v5.atomic_json(target, evidence)

    entry = {
        'id': 'TASK_A',
        'scientific_verdict': 'PASS_SCOPED',
        'verification_status': 'VERIFIED',
        'execution_origin': 'FRESH',
        'review_checks': {'independent': True},
        'fingerprint': v5.science_fp(job, manifest),
        'scientific_input_manifest': {'test': 'inputs'},
        'evidence_sha256': v5.digest(target),
        'worker_peak_rss_mib': None,
    }

    head = v5.commit(folder, [entry], [], head)
    return folder, head


def test_recoverable_without_final_science(environment):
    folder, head = create_interrupted(environment)
    assert not (folder / 'science.json').exists()

    _, checkpoint, digest = v5.inspect(folder)
    assert digest == head
    assert len(checkpoint['done']) == 1


def test_checkpoint_chain_corruption_rejected(environment):
    folder, _ = create_interrupted(environment)
    path = folder / 'checkpoints/000001.json'
    event = json.loads(path.read_text())
    event['previous_sha256'] = 'f' * 64
    path.write_text(json.dumps(event))

    with pytest.raises(ValueError, match='CHAIN_BROKEN'):
        v5.inspect(folder)


def test_scientific_evidence_tampering_rejected(environment):
    folder, _ = create_interrupted(environment)
    (folder / 'TASK_A.json').write_text(
        '{"status":"FAIL_SCOPED"}'
    )

    with pytest.raises(ValueError, match='EVIDENCE_INTEGRITY'):
        v5.inspect(folder)


def test_source_provenance_drift_rejected(
    environment, monkeypatch
):
    folder, _ = create_interrupted(environment)

    monkeypatch.setattr(
        v5, 'code_hashes', lambda: {'test': 'changed'}
    )

    with pytest.raises(ValueError, match='CODE_PROVENANCE'):
        v5.inspect(folder)


def test_completed_gate_restored_with_explicit_label(
    environment, monkeypatch
):
    root, base, jobs = environment
    old, _ = create_interrupted(environment)

    new_id = 'g2camp5_20261121T130000Z_abcdef34'
    monkeypatch.setattr(v5, '_new_run_id', lambda: new_id)

    def fake_supervise(process, folder, deadline, ram, disk):
        v5.atomic_json(
            folder / '_worker.json',
            {'status': 'PASS_SCOPED'},
        )
        return ('COMPLETED', 0, 12.0, '', False)

    monkeypatch.setattr(v5, 'supervise', fake_supervise)
    monkeypatch.setattr(
        v5.subprocess, 'Popen', lambda *a, **k: object()
    )
    monkeypatch.setattr(
        v5, 'PRESETS', {'short': (1000, 512, 10)}
    )

    args = SimpleNamespace(
        workers=1,
        level='L0',
        preset='short',
        minutes=2,
        dry_run=False,
        resume=old.name,
    )

    assert v5.execute(args) == 0

    new = base / new_id
    _, checkpoint, _ = v5.inspect(
        new, require_complete=True
    )

    assert len(checkpoint['done']) == 2
    assert checkpoint['done'][0]['execution_origin'] == (
        'RECOVERED_CHECKPOINT'
    )
    assert checkpoint['done'][1]['execution_origin'] == 'FRESH'
    assert checkpoint['done'][0]['recovered_from']['run_id'] == (
        old.name
    )

    assert checker.verify(
        new, require_complete=True
    ) == 0


def test_duplicate_resume_claim_rejected(
    environment, monkeypatch
):
    folder, _ = create_interrupted(environment)
    (folder / 'resume.claim').write_text('another-run\n')

    monkeypatch.setattr(
        v5, 'PRESETS', {'short': (1000, 512, 10)}
    )

    args = SimpleNamespace(
        workers=1,
        level='L0',
        preset='short',
        minutes=2,
        dry_run=False,
        resume=folder.name,
    )

    with pytest.raises(
        ValueError, match='RESUME_ALREADY_CLAIMED'
    ):
        v5.execute(args)

    assert len(v5.inspect(folder)[1]['done']) == 1


def test_unexpected_checkpoint_file_rejected(environment):
    folder, _ = create_interrupted(environment)
    (folder / 'checkpoints/garbage.json').write_text('{}')

    with pytest.raises(
        ValueError, match='CHECKPOINT_GAP_OR_ORPHAN'
    ):
        v5.inspect(folder)
