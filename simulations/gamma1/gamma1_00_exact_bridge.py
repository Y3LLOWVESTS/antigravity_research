"""GAMMA1-00 immutable L0 runner with PH16-04R2 raw-byte provenance.

Writes a JSON, SHA sidecar, and log on success OR failure.
Never overwrites prior artifacts or silently uses a different
parent source/result.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
import sys
import traceback

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'src'))

from antigravity_research.gamma1.gamma1_00_atlas import atlas

PARENTS = {
    'PH16_R2_source': (
        'src/antigravity_research/ph16/ph16_04_joint_stationary.py',
        'b5468671f6418fad7b6ed01d916ea65a95a1d59252b84d4411beed9709f86df0'
    ),
    'PH16_R2_result': (
        'results/data/ph16_04_20261118T164454314313Z.json',
        'ff700285effc35841fbb8d0e20cffa3c8e4b812e6629b549785a2304b716b2b0'
    ),
}

SOURCES = [
    'src/antigravity_research/gamma1/gamma1_00_atlas.py',
    'simulations/gamma1/gamma1_00_exact_bridge.py',
    'tests/gamma1/test_gamma1_00_atlas.py',
    'tests/gamma1/verify_gamma1_00.py',
    'theory/gamma1/GAMMA1_00_THEOREM_LEDGER.md',
]


def sha(path):
    if not path.is_file():
        return 'MISSING'

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def run():
    now = dt.datetime.now(dt.timezone.utc)
    tag = now.strftime('%Y%m%dT%H%M%S%fZ')
    base = 'gamma1_00_' + tag

    data = ROOT/'results/data'
    logs = ROOT/'results/logs'

    data.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)

    out = data/(base+'.json')
    side = data/(base+'.json.sha256')
    logfile = logs/(base+'.log')

    provenance = {
        k: {
            'path': p,
            'expected_sha256': expected,
            'actual_sha256': sha(ROOT/p),
        }
        for k, (p, expected) in PARENTS.items()
    }

    result = {
        'branch': 'GAMMA1-00',
        'timestamp_utc': now.isoformat(),
        'provenance': provenance,

        'gamma_source_shas': {
            p: sha(ROOT/p)
            for p in SOURCES
        },

        'classification': 'FAILED_OR_INCOMPLETE',
        'GAMMA1_01_authorized': False,
        '006D_replaced': False,
    }

    status = 2

    try:
        for name, entry in provenance.items():
            if (
                entry['actual_sha256']
                != entry['expected_sha256']
            ):
                raise RuntimeError(
                    name+' MISSING/WRONG SHA: '+str(entry)
                )

        if any(
            x == 'MISSING'
            for x in result['gamma_source_shas'].values()
        ):
            raise RuntimeError(
                'GAMMA code/test/document missing'
            )

        result.update(atlas())

        result['classification'] = 'ATLAS_COMPLETE_SCOPED'
        result['parent_provenance'] = 'PASS_EXACT_RAW_SHA'
        status = 0

    except Exception as exc:
        result['error'] = str(exc)
        result['traceback'] = traceback.format_exc()
        result['parent_provenance'] = 'NOT_PASS'
        result['decision'] = (
            'NO_NEXT_RUN_UNTIL_CAUSE_RESOLVED'
        )

    raw = (
        json.dumps(
            result,
            sort_keys=True,
            indent=2,
            allow_nan=False
        )+'\n'
    ).encode()

    with out.open('xb') as f:
        f.write(raw)

    checksum = hashlib.sha256(raw).hexdigest()

    with side.open('x') as f:
        f.write(checksum+'  '+out.name+'\n')

    lines = [
        f'RESULT_JSON={out}',
        f'RESULT_SHA256={checksum}',
        f'ATLAS_CLASSIFICATION={result["classification"]}',
        f'PH16_SOURCE_SHA={provenance["PH16_R2_source"]["actual_sha256"]}',
        f'PH16_RESULT_SHA={provenance["PH16_R2_result"]["actual_sha256"]}',
        '006D_REPLACED=NO',
        'GAMMA1_01_AUTOMATIC_AUTHORIZATION=NO',
        f'RETURN_CODE={status}',
    ]

    with logfile.open('x') as f:
        f.write('\n'.join(lines)+'\n')

    print('\n'.join(lines), flush=True)

    return status


if __name__ == '__main__':
    raise SystemExit(run())
