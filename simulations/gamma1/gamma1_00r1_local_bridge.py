"""GAMMA1-00R1 immutable local-algebraic runner.

Requires unchanged historical parent records.
No Einstein PDE, real Earth force, craft lift or SI operating energy.
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

from antigravity_research.gamma1.gamma1_00r1_local_bridge import atlas

PARENTS = {
    'PH16_R2_source': (
        'src/antigravity_research/ph16/ph16_04_joint_stationary.py',
        'b5468671f6418fad7b6ed01d916ea65a95a1d59252b84d4411beed9709f86df0'
    ),

    'PH16_R2_result': (
        'results/data/ph16_04_20261118T164454314313Z.json',
        'ff700285effc35841fbb8d0e20cffa3c8e4b812e6629b549785a2304b716b2b0'
    ),

    'GAMMA1_00_result': (
        'results/data/gamma1_00_20261118T202714278070Z.json',
        '480b9228b994f2634fe57ed23b7332e721d9060f43848bdc19e3ace0fb2cc16b'
    ),

    'GAMMA1_00_verification': (
        'results/data/gamma1_00_verification_20261118T204048204526Z.json',
        '5b34d63219e0bf41af376b9f55064883134c1e75f381166c0c87293d21ccf39d'
    ),
}

SOURCES = [
    'src/antigravity_research/gamma1/gamma1_00r1_local_bridge.py',
    'simulations/gamma1/gamma1_00r1_local_bridge.py',
    'tests/gamma1/test_gamma1_00r1.py',
    'tests/gamma1/verify_gamma1_00r1.py',
    'theory/gamma1/GAMMA1_00R1_LOCAL_METRIC_VARIATION_LEDGER.md',
]


def sha(path: Path) -> str:
    if not path.is_file():
        return 'MISSING'

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def main() -> int:
    now = dt.datetime.now(dt.timezone.utc)
    stamp = now.strftime('%Y%m%dT%H%M%S%fZ')
    name = 'gamma1_00r1_'+stamp

    data = ROOT/'results/data'
    logs = ROOT/'results/logs'

    data.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)

    output = data/(name+'.json')
    sidecar = data/(name+'.json.sha256')
    logfile = logs/(name+'.log')

    provenance = {
        key: {
            'path': path,
            'expected_sha256': expected,
            'actual_sha256': sha(ROOT/path),
        }
        for key, (path, expected) in PARENTS.items()
    }

    result = {
        'branch': 'GAMMA1-00R1',
        'timestamp_utc': now.isoformat(),
        'classification': 'FAILED_OR_INCOMPLETE',
        'provenance': provenance,

        'producing_sources_sha256': {
            path: sha(ROOT/path)
            for path in SOURCES
        },

        'GAMMA1_01_authorized': False,
        '006D_replaced': False,
    }

    status = 2

    try:
        for name_p, entry in provenance.items():
            if (
                entry['actual_sha256']
                != entry['expected_sha256']
            ):
                raise RuntimeError(
                    name_p
                    +' original parent SHA mismatch: '
                    +str(entry)
                )

        if 'MISSING' in result[
            'producing_sources_sha256'
        ].values():
            raise RuntimeError(
                'Missing GAMMA1-00R1 producing source or ledger'
            )

        previous = json.loads(
            (ROOT/PARENTS['GAMMA1_00_result'][0]).read_text()
        )

        verified = json.loads(
            (ROOT/PARENTS['GAMMA1_00_verification'][0]).read_text()
        )

        if (
            previous['classification']
            != 'ATLAS_COMPLETE_SCOPED'

            or previous['parent_provenance']
            != 'PASS_EXACT_RAW_SHA'

            or previous['GAMMA1_01_authorized'] is not False

            or verified['classification']
            != 'SCOPED_ATLAS_AND_FULL_SUITE_VERIFIED'

            or verified['full_suite_passed'] != 2959

            or verified['atlas_result_sha256']
            != PARENTS['GAMMA1_00_result'][1]
        ):
            raise RuntimeError(
                'Recorded verified GAMMA1-00 parent contract failed'
            )

        for path, expected in previous[
            'gamma_source_shas'
        ].items():
            if sha(ROOT/path) != expected:
                raise RuntimeError(
                    'Original GAMMA1-00 producing source changed: '
                    +path
                )

        result.update(atlas())

        result['classification'] = (
            'SCOPED_LOCAL_VARIATION_AND_SIGN_ATLAS'
        )
        result['parent_provenance'] = (
            'PASS_EXACT_FOUR_PARENTS'
        )

        status = 0

    except Exception as exc:
        result['error'] = str(exc)
        result['traceback'] = traceback.format_exc()
        result['parent_provenance'] = 'NOT_PASS'
        result['decision'] = 'STOP_INVALID_OR_INCOMPLETE'

    raw = (
        json.dumps(
            result,
            sort_keys=True,
            indent=2,
            allow_nan=False
        )+'\n'
    ).encode()

    with output.open('xb') as f:
        f.write(raw)

    digest = hashlib.sha256(raw).hexdigest()

    with sidecar.open('x') as f:
        f.write(
            digest+'  '+output.name+'\n'
        )

    report = [
        'RESULT_JSON='+str(output),
        'RESULT_SHA256='+digest,
        'ATLAS_CLASSIFICATION='+result['classification'],
        'PARENT_PROVENANCE='+result['parent_provenance'],
        'M0_BETA40_ONSHELL_HEALTH=NOT_DETERMINED',
        'EARTH_DOWN_WHOLE_CRAFT_UP=NOT_DERIVED',
        'GAMMA1_01_AUTOMATIC_AUTHORIZATION=NO',
        '006D_REPLACED=NO',
        'RETURN_CODE='+str(status),
    ]

    with logfile.open('x') as f:
        f.write('\n'.join(report)+'\n')

    print('\n'.join(report), flush=True)

    return status


if __name__ == '__main__':
    raise SystemExit(main())
