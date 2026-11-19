"""Immutable GAMMA1-00R4 on-background sign audit.

No PH16 stationary replay; no Einstein field solve.
Every failure produces an immutable failure JSON/SHA/log.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sys
import traceback

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(
    0,
    str(ROOT/'src')
)

from antigravity_research.gamma1.gamma1_00r4_background_sign import (
    sha,
    checked_profile,
    inspect,
    EXPECTED_R3_SHA,
    EXPECTED_PROFILE_SHA,
    EXPECTED_R3_VERIFY_SHA,
    EXPECTED_PH16_SOURCE_SHA,
)

PARENTS = {
    'PH16_R2_source': (
        'src/antigravity_research/ph16/ph16_04_joint_stationary.py',
        EXPECTED_PH16_SOURCE_SHA
    ),

    'R3_result': (
        'results/data/gamma1_00r3_20261119T001454764826Z.json',
        EXPECTED_R3_SHA
    ),

    'R3_verification': (
        'results/data/gamma1_00r3_verification_20261119T002902463013Z.json',
        EXPECTED_R3_VERIFY_SHA
    ),

    'R3_profile': (
        'results/data/gamma1_00r3_20261119T001454764826Z_native_12_L12.npz',
        EXPECTED_PROFILE_SHA
    ),
}

SOURCES = [
    'src/antigravity_research/gamma1/gamma1_00r4_background_sign.py',
    'simulations/gamma1/gamma1_00r4_background_audit.py',
    'tests/gamma1/test_gamma1_00r4.py',
    'tests/gamma1/verify_gamma1_00r4.py',
    'theory/gamma1/GAMMA1_00R4_ON_BACKGROUND_PORTAL_SIGN_LEDGER.md',
]


def read_ancestor_chain():
    r3 = json.loads(
        (
            ROOT/PARENTS['R3_result'][0]
        ).read_text()
    )

    v3 = json.loads(
        (
            ROOT/PARENTS['R3_verification'][0]
        ).read_text()
    )

    if (
        r3.get('classification')
        != 'PASS_SINGLE_MESH_REPLAY_MATCHED_SCOPED_ACTION_CONTRACT'

        or v3.get('classification')
        != 'SINGLE_NATIVE_REPLAY_AND_FULL_REGRESSION_VERIFIED'

        or v3.get('full_regression_passed')
        != 3033

        or v3.get('result_sha256')
        != EXPECTED_R3_SHA

        or v3.get('native_profile_sha256')
        != EXPECTED_PROFILE_SHA

        or r3['native_profile_archive']['sha256']
        != EXPECTED_PROFILE_SHA

        or r3.get('GAMMA1_01_authorized')
        is not False
    ):
        raise ValueError(
            'R3 verified parent contract drift'
        )

    if len(r3['parents']) != 8:
        raise ValueError(
            'R3 predecessor parent count drift'
        )

    for label, entry in r3['parents'].items():
        relative = entry['path']
        expected = entry['expected']

        if (
            sha(ROOT/relative) != expected
            or entry['actual'] != expected
        ):
            raise ValueError(
                'R3 ancestor drift '+label
            )

    for relative, expected in r3[
        'producer_shas'
    ].items():
        if sha(ROOT/relative) != expected:
            raise ValueError(
                'R3 original producing file changed: '
                +relative
            )

    return {
        'historical_R3_ancestors':
            len(r3['parents']),

        'historical_R3_producing_files':
            len(r3['producer_shas']),
    }


def main():
    now = dt.datetime.now(
        dt.timezone.utc
    )

    tag = now.strftime(
        '%Y%m%dT%H%M%S%fZ'
    )

    basename = 'gamma1_00r4_'+tag

    data = ROOT/'results/data'
    logs = ROOT/'results/logs'

    data.mkdir(
        parents=True,
        exist_ok=True
    )

    logs.mkdir(
        parents=True,
        exist_ok=True
    )

    output = data/(basename+'.json')
    sidecar = data/(basename+'.json.sha256')
    logfile = logs/(basename+'.log')

    provenance = {
        label: {
            'path': relative,
            'expected_sha256': expected,
            'actual_sha256': sha(ROOT/relative),
        }
        for label, (relative, expected)
        in PARENTS.items()
    }

    result = {
        'branch': 'GAMMA1-00R4',
        'timestamp_utc': now.isoformat(),
        'classification': 'FAILED_OR_INCOMPLETE',
        'provenance': provenance,

        'producer_shas': {
            relative: sha(ROOT/relative)
            for relative in SOURCES
        },

        '006D_replaced': False,
        'GAMMA1_01_authorized': False,
        'Earth_down': 'NOT_DERIVED',
        'whole_craft_up': 'NOT_DERIVED',
        'complete_energy_lt10MJ': 'NOT_CERTIFIED',
    }

    status = 2

    try:
        for label, entry in provenance.items():
            if (
                entry['expected_sha256']
                != entry['actual_sha256']
            ):
                raise ValueError(
                    'Parent hash failed: '+label
                )

            if label != 'PH16_R2_source':
                parent = ROOT/entry['path']
                parent_sidecar = parent.with_name(
                    parent.name+'.sha256'
                )

                if (
                    not parent_sidecar.is_file()
                    or parent_sidecar.read_text().strip()
                    != entry['expected_sha256']
                    +'  '+parent.name
                ):
                    raise ValueError(
                        'Parent sidecar failed: '+label
                    )

        if 'MISSING' in result[
            'producer_shas'
        ].values():
            raise ValueError(
                'R4 producing file missing'
            )

        result['ancestor_validation'] = (
            read_ancestor_chain()
        )

        native = checked_profile(
            ROOT/PARENTS['R3_profile'][0]
        )

        result['observations'] = (
            inspect(native)
        )

        result.update({
            'classification':
                'PASS_SCOPED_ON_BACKGROUND_PORTAL_GRADIENT_AUDIT',

            'decision':
                'STOP_NO_GRAVITATIONAL_PROMOTION_COMPLETE_COVARIANT_ACTION_NEXT',

            'qualified_physical_survivors': [],

            'physical_1kg_torus_1g_at_1m':
                'NOT_CERTIFIED',

            'PH16_replay':
                'NOT_RUN',

            'Einstein_equations':
                'NOT_SOLVED',

            'Lorentzian_modes':
                'NOT_CERTIFIED',

            'continuum_exterior':
                'NOT_CERTIFIED',
        })

        status = 0

    except Exception as exc:
        result['error'] = str(exc)
        result['traceback'] = (
            traceback.format_exc()
        )

        result['decision'] = (
            'PRESERVE_FAILURE_NO_PROMOTION'
        )

    raw = (
        json.dumps(
            result,
            sort_keys=True,
            indent=2,
            allow_nan=False
        )+'\n'
    ).encode()

    with output.open('xb') as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())

    digest = hashlib.sha256(
        raw
    ).hexdigest()

    with sidecar.open('x') as handle:
        handle.write(
            digest+'  '+output.name+'\n'
        )
        handle.flush()
        os.fsync(handle.fileno())

    statements = [
        'RESULT_JSON='+str(output),
        'RESULT_SHA256='+digest,

        'CLASSIFICATION='
        +result['classification'],

        'PH16_REPLAY=NOT_RUN',
        'WHOLE_CRAFT_UP=NOT_DERIVED',
        'GAMMA1_01_AUTOMATIC_AUTHORIZATION=NO',
        '006D_REPLACED=NO',
        'RETURN_CODE='+str(status),
    ]

    with logfile.open('x') as handle:
        handle.write(
            '\n'.join(statements)+'\n'
        )

    print(
        '\n'.join(statements),
        flush=True
    )

    return status


if __name__ == '__main__':
    raise SystemExit(main())
