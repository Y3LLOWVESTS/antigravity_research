"""Independent integrity audit for v5 checkpoints and resumed evidence.

Revalidates each scientific result through its v4 independent reviewer.
Neither completion nor recovery establishes gravitational lift.
"""
from __future__ import annotations

import json

from .engine import atomic_json, atomic_text, digest
from . import campaign_v5 as run


def verify(folder, *, require_complete=True):
    checks = {}

    def gate(name, condition):
        checks[name] = bool(condition)
        if not condition:
            raise ValueError(name)

    try:
        manifest, latest, head = run.inspect(
            folder,
            require_complete=require_complete,
        )

        science = json.loads(
            (folder / 'science.json').read_text()
        )

        ledger = dict(
            row.split('  ', 1)[::-1]
            for row in (
                folder / 'hashes.sha256'
            ).read_text().splitlines()
        )

        for name in ('manifest.json', 'science.json'):
            gate(
                'file SHA ' + name,
                ledger.get(name) == digest(folder / name),
            )

        gate(
            'run linkage',
            science['run_id'] == manifest['run_id'] == folder.name,
        )

        gate(
            'checkpoint anchor',
            science['last_checkpoint_sha256'] == head,
        )

        gate(
            'completed entries identical',
            science['jobs'] == latest['done'],
        )

        gate(
            'skipped entries identical',
            science['skipped'] == latest['skipped'],
        )

        remaining = [
            task['id']
            for task in manifest['tasks']
            if task['id'] not in {
                x['id']
                for x in latest['done'] + latest['skipped']
            }
        ]

        gate(
            'remaining tasks honest',
            science['remaining'] == remaining,
        )

        gate(
            'no gravitational promotion',
            science['qualified_physical_survivors'] == 0
            and science['whole_craft_lift'] == 'NOT_DERIVED'
            and science['energy_J'] == 'NOT_CERTIFIED'
            and science['006D_replaced'] is False,
        )

        gate(
            'no unsupported full regression claim',
            science['full_repository_regression'] == 'NOT_RUN',
        )

        complete = (
            len(latest['done']) + len(latest['skipped'])
            == len(manifest['tasks'])
        )

        gate(
            'completion and state consistency',
            science['state'] != 'COMPLETED' or complete,
        )

        if science['state'] == 'COMPLETED' and complete:
            status = 'PASS_SCOPED_CAMPAIGN_NO_LIFT'
        elif not require_complete:
            status = 'PASS_INCOMPLETE_EVIDENCE_ONLY'
        else:
            raise ValueError('INCOMPLETE_OR_FAILED_CAMPAIGN')

        result = {
            'program': 'GRAVITY2_V5_INDEPENDENT',
            'run_id': folder.name,
            'status': status,
            'checks': checks,
            'science_sha256': digest(folder / 'science.json'),
            'checkpoint_sha256': head,
            'physical_success': False,
        }

    except Exception as exc:
        result = {
            'program': 'GRAVITY2_V5_INDEPENDENT',
            'run_id': folder.name,
            'status': 'HOLD',
            'checks': checks,
            'error': repr(exc),
            'physical_success': False,
        }

    destination = folder / 'verification.json'

    if destination.exists():
        if json.loads(destination.read_text()) != result:
            print('GRAVITY2_V5_REVERIFY_DIFFERED_NO_OVERWRITE')
            return 3
    else:
        atomic_json(destination, result)
        atomic_text(
            folder / 'verification.sha256',
            digest(destination) + '  verification.json\n',
        )

    print('GRAVITY2_V5_VERIFY=' + result['status'])
    print(
        'CHECKS='
        + str(sum(checks.values()))
        + '/'
        + str(len(checks))
    )

    if 'error' in result:
        print('ERROR=' + result['error'])

    print('VERIFICATION_SHA256=' + digest(destination))

    return (
        0
        if result['status'] == 'PASS_SCOPED_CAMPAIGN_NO_LIFT'
        else 3
    )
