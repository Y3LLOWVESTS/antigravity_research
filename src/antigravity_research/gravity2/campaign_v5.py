"""GRAVITY2 v5 durable per-gate checkpoints and crash recovery.

Uses the independently reviewed v4 science controls unchanged.
Recovered gates are copied, rechecked, and explicitly labeled.
Incomplete or corrupted checkpoints are not accepted.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys
import time

from . import campaign_v4 as v4
from . import campaign_science as science
from . import scientific_inputs_v3 as inputs
from .engine import atomic_json, atomic_text, digest, bytes_under
from .miner import _rss_available, supervise
from .policy import PRESETS, GLOBAL_MIB

ROOT = v4.ROOT
BASE = ROOT / 'results/gravity2/campaign_v5_runs'
RUN_RE = re.compile(r'g2camp5_\d{8}T\d{6}Z_[a-f0-9]{8}\Z')
MIB = 1024 * 1024
SCHEMA = 'gravity2.checkpoint.v5'


def locate(run_id):
    if not isinstance(run_id, str) or not RUN_RE.fullmatch(run_id):
        raise ValueError('UNSAFE_RUN_ID')
    return BASE / run_id


def sha_json(obj):
    return hashlib.sha256(
        science.canonical(obj).encode('utf-8')
    ).hexdigest()


def code_hashes():
    result = dict(v4.core_hashes())

    package = Path(__file__).resolve().parent
    for name in ('campaign_v5.py', 'campaign_check_v5.py'):
        result[name] = digest(package / name)

    result['tests/gravity2/test_campaign_v5.py'] = digest(
        ROOT / 'tests/gravity2/test_campaign_v5.py'
    )
    return result


def science_fp(job, manifest):
    return sha_json({
        'job': job,
        'code': manifest['code_sha256'],
        'parents': manifest['parents'],
        'source_inputs': inputs.manifest(ROOT, job),
        'producer': digest(v4.provider_file(job['module'])),
        'independent': digest(
            v4.provider_file(job['independent'])
        ),
    })


def chain(folder):
    """Validate a contiguous, SHA-linked checkpoint sequence."""
    if folder.is_symlink():
        raise ValueError('SYMLINK_RUN_DIR')

    manifest_file = folder / 'manifest.json'
    if manifest_file.is_symlink():
        raise ValueError('SYMLINK_MANIFEST')

    manifest = json.loads(manifest_file.read_text())

    if (
        manifest['run_id'] != folder.name
        or manifest['schema'] != 'gravity2.campaign.v5'
    ):
        raise ValueError('MANIFEST_RUN_MISMATCH')

    if manifest['code_sha256'] != code_hashes():
        raise ValueError('CODE_PROVENANCE_DRIFT')

    if manifest['parents'] != v4.parent_locks():
        raise ValueError('SOURCE_PARENT_DRIFT')

    tasks = manifest['tasks']

    if science.signature(tasks) != manifest['tasks_sha256']:
        raise ValueError('TASK_SIGNATURE_DRIFT')

    expected = v4.dispatch_order([
        job for job in v4.jobs()
        if int(job['level'][1:]) <= int(manifest['level'][1:])
    ])

    if tasks != expected:
        raise ValueError('TASK_GRAPH_DRIFT')

    directory = folder / 'checkpoints'

    if not directory.is_dir() or directory.is_symlink():
        raise ValueError('CHECKPOINT_DIR_MISSING')

    entries = sorted(directory.iterdir())

    if not entries:
        raise ValueError('NO_DURABLE_CHECKPOINT')

    if any(
        path.is_symlink() or not path.is_file()
        for path in entries
    ):
        raise ValueError('CHECKPOINT_FILE_UNSAFE')

    if len(entries) > len(tasks) + 1:
        raise ValueError('CHECKPOINT_COUNT_OUT_OF_BOUNDS')

    previous = '0' * 64
    previous_processed = -1
    previous_done = []
    previous_skipped = []
    latest = None

    for sequence, path in enumerate(entries):
        if path.name != f'{sequence:06d}.json':
            raise ValueError('CHECKPOINT_GAP_OR_ORPHAN')

        event = json.loads(path.read_text())

        if (
            event.get('schema') != SCHEMA
            or event.get('sequence') != sequence
            or event.get('previous_sha256') != previous
            or event.get('manifest_sha256') != digest(manifest_file)
        ):
            raise ValueError('CHECKPOINT_CHAIN_BROKEN')

        done = event.get('done')
        skipped = event.get('skipped')

        if not isinstance(done, list) or not isinstance(skipped, list):
            raise ValueError('CHECKPOINT_ENTRIES_INVALID')

        processed = len(done) + len(skipped)

        if processed != sequence:
            raise ValueError('CHECKPOINT_SEQUENCE_INVALID')

        if processed <= previous_processed:
            raise ValueError('CHECKPOINT_NON_MONOTONIC')

        if (
            done[:len(previous_done)] != previous_done
            or skipped[:len(previous_skipped)] != previous_skipped
            or sorted(x['id'] for x in done + skipped)
            != sorted(job['id'] for job in tasks[:processed])
        ):
            raise ValueError('CHECKPOINT_PREFIX_OR_MUTATION')

        previous_done = done
        previous_skipped = skipped
        previous_processed = processed
        previous = digest(path)
        latest = event

    assert latest is not None

    if len(latest['done']) + len(latest['skipped']) > len(tasks):
        raise ValueError('CHECKPOINT_TOO_MANY_JOBS')

    return manifest, latest, previous


def commit(folder, done, skipped, previous):
    sequence = len(done) + len(skipped)
    path = folder / 'checkpoints' / f'{sequence:06d}.json'

    if path.exists() or path.is_symlink():
        raise ValueError('CHECKPOINT_ALREADY_EXISTS')

    event = {
        'schema': SCHEMA,
        'sequence': sequence,
        'previous_sha256': previous,
        'manifest_sha256': digest(folder / 'manifest.json'),
        'done': done,
        'skipped': skipped,
    }

    atomic_json(path, event)
    return digest(path)


def inspect(folder, *, require_complete=False, _depth=0):
    if _depth > 8:
        raise ValueError('RECOVERY_DEPTH_EXCEEDED')

    manifest, checkpoint, head_sha = chain(folder)
    tasks = manifest['tasks']
    processed = checkpoint['done'] + checkpoint['skipped']
    by_id = {job['id']: job for job in tasks}
    seen = set()
    completed = {}

    for item in processed:
        ident = item['id']

        if ident not in by_id or ident in seen:
            raise ValueError('DUPLICATE_OR_UNKNOWN_JOB')

        seen.add(ident)
        job = by_id[ident]

        if item.get('skipped'):
            if item.get('reason') != 'PREREQUISITES_NOT_PROVED':
                raise ValueError('BAD_SKIP_REASON')

            if all(
                v4.parent_ready(list(completed.values()), dep)
                for dep in job['requires']
            ):
                raise ValueError('UNJUSTIFIED_SKIP')
            continue

        if not all(
            v4.parent_ready(list(completed.values()), dep)
            for dep in job['requires']
        ):
            raise ValueError('UNAUTHORIZED_CHILD')

        if item.get('fingerprint') != science_fp(job, manifest):
            raise ValueError('SCIENTIFIC_FINGERPRINT_DRIFT')

        if item.get('scientific_input_manifest') != (
            inputs.manifest(ROOT, job)
        ):
            raise ValueError('SCIENTIFIC_INPUT_DRIFT')

        evidence_path = folder / (ident + '.json')

        if (
            evidence_path.is_symlink()
            or not evidence_path.is_file()
            or item.get('evidence_sha256') != digest(evidence_path)
        ):
            raise ValueError('EVIDENCE_INTEGRITY_FAILURE')

        evidence = json.loads(evidence_path.read_text())
        checks = v4.reviewed_checks(job, evidence)

        if (
            item.get('scientific_verdict') != evidence['status']
            or item.get('review_checks') != checks
            or item.get('verification_status') != 'VERIFIED'
            or item.get('execution_origin') not in (
                'FRESH', 'RECOVERED_CHECKPOINT'
            )
        ):
            raise ValueError('INDEPENDENT_REVIEW_DRIFT')

        if item['execution_origin'] == 'RECOVERED_CHECKPOINT':
            source = item.get('recovered_from')

            if (
                not isinstance(source, dict)
                or source.get('run_id') != manifest.get('resume_from')
                or source.get('checkpoint_sha256')
                != manifest.get('resume_checkpoint_sha256')
            ):
                raise ValueError('RECOVERY_LINEAGE_MISSING')

            old = locate(source['run_id'])

            if old.resolve() == folder.resolve():
                raise ValueError('RECOVERY_SELF_REFERENCE')

            oldman, oldevent, oldhash = inspect(
                old, _depth=_depth + 1
            )

            if (
                oldhash != source['checkpoint_sha256']
                or oldman['code_sha256'] != manifest['code_sha256']
                or oldman['tasks_sha256'] != manifest['tasks_sha256']
            ):
                raise ValueError('RECOVERY_SOURCE_DRIFT')

            prior = next(
                (
                    entry for entry in oldevent['done']
                    if entry['id'] == ident
                ),
                None,
            )

            if (
                prior is None
                or prior['evidence_sha256']
                != source.get('prior_evidence_sha256')
                or prior['evidence_sha256']
                != item['evidence_sha256']
            ):
                raise ValueError('RECOVERY_SOURCE_NOT_CERTIFIED')

        completed[ident] = item

    if {x['id'] for x in processed} != {
        job['id'] for job in tasks[:len(processed)]
    }:
        raise ValueError('OUT_OF_ORDER_CHECKPOINT')

    if require_complete and len(processed) != len(tasks):
        raise ValueError('INCOMPLETE_CAMPAIGN')

    return manifest, checkpoint, head_sha


def _new_run_id():
    return datetime.now(timezone.utc).strftime(
        'g2camp5_%Y%m%dT%H%M%SZ_'
    ) + secrets.token_hex(4)


def _lock(folder):
    handle = (folder / 'execution.lock').open('a+b')

    try:
        fcntl.flock(
            handle.fileno(),
            fcntl.LOCK_EX | fcntl.LOCK_NB,
        )
    except BlockingIOError:
        handle.close()
        raise ValueError('RUN_STILL_ACTIVE')

    return handle


def _worker(input_file, output_file):
    source = Path(input_file)
    target = Path(output_file)

    if (
        target.name != '_worker.json'
        or not RUN_RE.fullmatch(target.parent.name)
        or target.parent.parent.resolve() != BASE.resolve()
        or source != target.parent / '_input.json'
        or source.is_symlink()
        or target.is_symlink()
    ):
        raise ValueError('WORKER_OUTPUT_NOT_OWNED')

    job = json.loads(source.read_text())
    v4.validate_job(job)
    before = inputs.manifest(ROOT, job)

    module = __import__(
        'antigravity_research.gravity2.' + job['module'],
        fromlist=['run_gate'],
    )

    evidence = module.run_gate(job, {'root': str(ROOT)})

    if before != inputs.manifest(ROOT, job):
        raise ValueError('SCIENTIFIC_INPUT_DRIFT_DURING_WORKER')

    if (
        not isinstance(evidence, dict)
        or evidence.get('status') not in (
            'BLOCKED_ACTION_INCOMPLETE',
            'SCOPED_CONTROL_ONLY',
            'UNDERDETERMINED',
            'FAIL_SCOPED',
            'PASS_SCOPED',
        )
        or len(science.canonical(evidence)) > 262144
    ):
        raise ValueError('WORKER_EVIDENCE_INVALID')

    atomic_json(target, evidence)


def execute(args):
    fault_pause = getattr(args, 'test_pause_seconds', 0.0)

    if (
        not isinstance(fault_pause, (int, float))
        or not math.isfinite(fault_pause)
        or not 0 <= fault_pause <= 30
        or (args.resume and fault_pause)
    ):
        raise ValueError('INVALID_FAULT_INJECTION')

    if args.workers != 1 or args.level not in ('L0', 'L1'):
        raise ValueError('ONLY_L0_L1_ONE_WORKER')

    cap, ram, disk = PRESETS[args.preset]
    seconds = 60 * args.minutes

    if not math.isfinite(seconds) or not 0 < seconds <= cap:
        raise ValueError('INVALID_TIME_BUDGET')

    tasks = v4.dispatch_order([
        job for job in v4.jobs()
        if int(job['level'][1:]) <= int(args.level[1:])
    ])

    if args.dry_run:
        print(json.dumps({
            'program': 'GRAVITY2_CHECKPOINT_V5',
            'tasks': [
                {'id': job['id'], 'gate': job['gate']}
                for job in tasks
            ],
            'writes': 'NONE',
            'L2_L4': 'LOCKED',
        }, indent=2))
        return 0

    if (
        not _rss_available()
        or bytes_under(ROOT / 'results/gravity2')
        > (GLOBAL_MIB - disk) * MIB
    ):
        raise ValueError('RESOURCE_PREFLIGHT_HOLD')

    parents = v4.parent_locks()

    if not all(row['match'] for row in parents.values()):
        raise ValueError('SOURCE_PARENT_HOLD')

    old = None
    recovered = None
    old_lock = None

    if args.resume:
        old = locate(args.resume)
        old_lock = _lock(old)

        try:
            oldman, oldcheckpoint, head = inspect(old)

            if (
                oldman['level'] != args.level
                or oldman['tasks'] != tasks
                or oldman['code_sha256'] != code_hashes()
            ):
                raise ValueError('RESUME_PROVENANCE_MISMATCH')

            if (old / 'science.json').exists():
                oldscience = json.loads(
                    (old / 'science.json').read_text()
                )

                if oldscience.get('state') == 'COMPLETED':
                    raise ValueError('CANNOT_RESUME_COMPLETED')

            if (old / 'resume.claim').exists():
                raise ValueError('RESUME_ALREADY_CLAIMED')

            recovered = (oldcheckpoint, head)

        except BaseException:
            old_lock.close()
            raise

    rid = _new_run_id()
    folder = locate(rid)
    folder.mkdir(parents=True, exist_ok=False, mode=0o700)
    lock = _lock(folder)

    start = time.monotonic()
    deadline = start + seconds
    finished = []
    skipped = []
    state = 'COMPLETED'

    manifest = {
        'schema': 'gravity2.campaign.v5',
        'run_id': rid,
        'level': args.level,
        'preset': args.preset,
        'workers': 1,
        'wall_seconds': seconds,
        'ram_soft_mib': ram,
        'disk_soft_mib': disk,
        'code_sha256': code_hashes(),
        'parents': parents,
        'tasks': tasks,
        'tasks_sha256': science.signature(tasks),
        'resume_from': args.resume,
        'resume_checkpoint_sha256':
            recovered[1] if recovered else None,
        'test_fault_pause_after_first_checkpoint_s': fault_pause,
        'physical_scope': 'SCOPED_L0_L1_NO_LIFT',
    }

    atomic_json(folder / 'manifest.json', manifest)
    (folder / 'checkpoints').mkdir(mode=0o700)
    head = commit(folder, finished, skipped, '0' * 64)

    print('GRAVITY2_CHECKPOINT_V5_RUN=' + rid, flush=True)

    try:
        if recovered is not None:
            source_claim = old / 'resume.claim'

            with source_claim.open('x') as handle:
                handle.write(rid + '\n')

            copied = recovered[0]
            source_done = {
                item['id']: item for item in copied['done']
            }
            source_skipped = {
                item['id']: item for item in copied['skipped']
            }

            count = len(source_done) + len(source_skipped)

            for task in tasks[:count]:
                ident = task['id']

                if ident in source_skipped:
                    skipped.append(source_skipped[ident])
                else:
                    prior = source_done[ident]
                    raw = (old / (ident + '.json')).read_bytes()
                    target = folder / (ident + '.json')

                    with target.open('xb') as handle:
                        handle.write(raw)

                    item = dict(prior)
                    item['execution_origin'] = 'RECOVERED_CHECKPOINT'
                    item['recovered_from'] = {
                        'run_id': old.name,
                        'checkpoint_sha256': recovered[1],
                        'prior_evidence_sha256':
                            prior['evidence_sha256'],
                    }
                    item['evidence_sha256'] = digest(target)
                    finished.append(item)

                head = commit(folder, finished, skipped, head)

            inspect(old)

            print(
                'RECOVERED_JOBS=' + str(len(finished)),
                flush=True,
            )

        for job in tasks[len(finished) + len(skipped):]:
            ident = job['id']

            if (folder / 'stop.request').exists():
                state = 'USER_STOP'
                break

            if time.monotonic() >= deadline:
                state = 'TIME_BUDGET_EXCEEDED'
                break

            if bytes_under(
                ROOT / 'results/gravity2'
            ) > (GLOBAL_MIB - disk) * MIB:
                state = 'STORAGE_LIMIT'
                break

            if not all(
                v4.parent_ready(finished, dep)
                for dep in job['requires']
            ):
                skipped.append({
                    'id': ident,
                    'skipped': True,
                    'reason': 'PREREQUISITES_NOT_PROVED',
                })
                head = commit(folder, finished, skipped, head)
                continue

            before = inputs.manifest(ROOT, job)
            fingerprint = science_fp(job, manifest)

            worker_input = folder / '_input.json'
            worker_output = folder / '_worker.json'

            atomic_json(worker_input, job)

            env = dict(os.environ)
            env.update({
                'PYTHONPATH': str(ROOT / 'src'),
                'PYTHONDONTWRITEBYTECODE': '1',
                'OPENBLAS_NUM_THREADS': '1',
                'OMP_NUM_THREADS': '1',
                'MKL_NUM_THREADS': '1',
                'VECLIB_MAXIMUM_THREADS': '1',
            })

            process = subprocess.Popen(
                [
                    sys.executable,
                    '-m',
                    'antigravity_research.gravity2.campaign_v5',
                    '_worker',
                    '--input',
                    str(worker_input),
                    '--output',
                    str(worker_output),
                ],
                cwd=ROOT,
                env=env,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                start_new_session=True,
            )

            outcome, rc, peak, stdout, truncated = supervise(
                process, folder, deadline, ram, disk
            )

            worker_input.unlink(missing_ok=True)

            if (
                outcome != 'COMPLETED'
                or rc != 0
                or not worker_output.is_file()
            ):
                state = (
                    outcome
                    if outcome != 'COMPLETED'
                    else 'WORKER_ERROR'
                )
                atomic_text(
                    folder / 'worker_failure.log',
                    str(stdout)[-2048:],
                )
                break

            evidence = json.loads(worker_output.read_text())
            worker_output.unlink(missing_ok=True)

            if before != inputs.manifest(ROOT, job):
                state = 'SCIENTIFIC_INPUT_DRIFT'
                break

            try:
                checks = v4.reviewed_checks(job, evidence)
            except Exception as exc:
                state = 'INDEPENDENT_REVIEW_HOLD'
                atomic_text(
                    folder / 'review_failure.log',
                    repr(exc)[:2048],
                )
                break

            target = folder / (ident + '.json')

            if target.exists():
                raise ValueError('EVIDENCE_TARGET_ALREADY_EXISTS')

            atomic_json(target, evidence)

            finished.append({
                'id': ident,
                'scientific_verdict': evidence['status'],
                'verification_status': 'VERIFIED',
                'execution_origin': 'FRESH',
                'review_checks': checks,
                'fingerprint': fingerprint,
                'scientific_input_manifest': before,
                'evidence_sha256': digest(target),
                'worker_peak_rss_mib': peak,
            })

            head = commit(folder, finished, skipped, head)

            print(
                'CHECKPOINTED_GATE=' + ident + ' ' + evidence['status'],
                flush=True,
            )

            if len(finished) + len(skipped) == 1 and fault_pause:
                print(
                    'FAULT_INJECTION_PAUSE_READY=' + rid,
                    flush=True,
                )
                time.sleep(fault_pause)

    except KeyboardInterrupt:
        state = 'USER_INTERRUPT'

    except Exception as exc:
        state = 'EXECUTION_ERROR'
        atomic_text(
            folder / 'execution_failure.log',
            repr(exc)[:2048] + '\n',
        )

    finally:
        remaining = [
            job['id'] for job in tasks
            if job['id'] not in {
                item['id']
                for item in finished + skipped
            }
        ]

        science_output = {
            'program': 'GRAVITY2_V5_CRASH_SAFE_CAMPAIGN',
            'run_id': rid,
            'state': state,
            'jobs': finished,
            'skipped': skipped,
            'remaining': remaining,
            'last_checkpoint_sha256': head,
            'qualified_physical_survivors': 0,
            '006D_replaced': False,
            'whole_craft_lift': 'NOT_DERIVED',
            'energy_J': 'NOT_CERTIFIED',
            'full_repository_regression': 'NOT_RUN',
        }

        atomic_json(folder / 'science.json', science_output)

        atomic_text(
            folder / 'hashes.sha256',
            ''.join(
                digest(folder / name) + '  ' + name + '\n'
                for name in ('manifest.json', 'science.json')
            ),
        )

        lock.close()

        if old_lock is not None:
            old_lock.close()

    from .campaign_check_v5 import verify

    result = verify(
        folder,
        require_complete=(state == 'COMPLETED'),
    )
    return result if state == 'COMPLETED' else 3


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog='gravity2.campaign_v5'
    )
    sub = parser.add_subparsers(dest='cmd', required=True)

    for name in ('run', 'resume'):
        cmd = sub.add_parser(name)
        cmd.add_argument('--level', default='L1', choices=('L0', 'L1'))
        cmd.add_argument('--preset', default='short', choices=tuple(PRESETS))
        cmd.add_argument('--minutes', default=2.0, type=float)
        cmd.add_argument('--workers', default=1, type=int)
        cmd.add_argument('--dry-run', action='store_true')
        cmd.add_argument(
            '--test-pause-after-first-checkpoint',
            dest='test_pause_seconds',
            default=0.0,
            type=float,
        )
        if name == 'resume':
            cmd.add_argument('--run-id', required=True)

    command = sub.add_parser('verify')
    command.add_argument('--run-id', required=True)

    worker = sub.add_parser('_worker')
    worker.add_argument('--input', required=True)
    worker.add_argument('--output', required=True)

    args = parser.parse_args(argv)

    try:
        if args.cmd in ('run', 'resume'):
            args.resume = (
                args.run_id if args.cmd == 'resume' else None
            )
            return execute(args)

        if args.cmd == 'verify':
            from .campaign_check_v5 import verify
            return verify(
                locate(args.run_id),
                require_complete=True,
            )

        if args.cmd == '_worker':
            _worker(args.input, args.output)
            return 0

    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(
            'GRAVITY2_V5_HOLD=' + repr(exc),
            file=sys.stderr,
        )
        return 3

    return 3


if __name__ == '__main__':
    raise SystemExit(main())
