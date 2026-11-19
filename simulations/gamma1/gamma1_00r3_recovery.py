"""GAMMA1-00R3: one-mesh unchanged PH16 solver replay.

A new replay is not the historical exact state, even if stationary
diagnostics agree. Earlier results and producing sources are immutable.
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
sys.path.insert(0, str(ROOT/'src'))

from antigravity_research.gamma1.gamma1_00r3_action_recovery import (
    algebra,
    sha,
    validate_native_profile,
    PH16_SHA,
)

PARENTS = {
    'PH16_SOURCE': (
        'src/antigravity_research/ph16/ph16_04_joint_stationary.py',
        PH16_SHA
    ),

    'PH16_R2_JSON': (
        'results/data/ph16_04_20261118T164454314313Z.json',
        'ff700285effc35841fbb8d0e20cffa3c8e4b812e6629b549785a2304b716b2b0'
    ),

    'GAMMA_00_JSON': (
        'results/data/gamma1_00_20261118T202714278070Z.json',
        '480b9228b994f2634fe57ed23b7332e721d9060f43848bdc19e3ace0fb2cc16b'
    ),

    'GAMMA_00_VERIFY': (
        'results/data/gamma1_00_verification_20261118T204048204526Z.json',
        '5b34d63219e0bf41af376b9f55064883134c1e75f381166c0c87293d21ccf39d'
    ),

    'GAMMA_R1_JSON': (
        'results/data/gamma1_00r1_20261118T211802035544Z.json',
        'b543157cddb1e1e97c5260bf1de0ef39b329e7b0ea3b96fb12ed33df20d81e08'
    ),

    'GAMMA_R1_VERIFY': (
        'results/data/gamma1_00r1_verification_20261118T213059468632Z.json',
        'e92a73b0a6101e0a980fcab208c9140d55cb25382fb9fe83035763749fd05b63'
    ),

    'GAMMA_R2_JSON': (
        'results/data/gamma1_00r2_20261118T214917926733Z.json',
        '62a0fce503016a97d30e8330a9ca600080c17a06ae38f320373ccc2c912fb10f'
    ),

    'GAMMA_R2_VERIFY': (
        'results/data/gamma1_00r2_verification_20261118T220330544123Z.json',
        '024b16ee47c9452d3b74838a81948dbf3341087819dbaa619e9bafe0488d1eab'
    ),
}

SOURCES = [
    'src/antigravity_research/gamma1/gamma1_00r3_action_recovery.py',
    'simulations/gamma1/gamma1_00r3_recovery.py',
    'tests/gamma1/test_gamma1_00r3.py',
    'tests/gamma1/verify_gamma1_00r3.py',
    'theory/gamma1/GAMMA1_00R3_ACTION_AND_NATIVE_PROFILE_LEDGER.md',
]


def checked_provenance():
    found = {}

    for key, (rel, expected) in PARENTS.items():
        actual = sha(ROOT/rel)

        found[key] = {
            'path': rel,
            'expected': expected,
            'actual': actual,
        }

        if actual != expected:
            raise RuntimeError(
                'PARENT_RAW_SHA_DRIFT: '+key
            )

        if rel.endswith('.json'):
            sidecar = ROOT/(rel+'.sha256')

            if (
                not sidecar.is_file()
                or sidecar.read_text().strip()
                != expected+'  '+Path(rel).name
            ):
                raise RuntimeError(
                    'PARENT_SIDECAR_DRIFT: '+key
                )

    r2 = json.loads(
        (
            ROOT/PARENTS['GAMMA_R2_JSON'][0]
        ).read_text()
    )

    v2 = json.loads(
        (
            ROOT/PARENTS['GAMMA_R2_VERIFY'][0]
        ).read_text()
    )

    if (
        r2.get('classification')
        != 'PASS_SCOPED_NONUNIQUENESS_AND_EVIDENCE_SUFFICIENCY'

        or r2.get('parent_provenance')
        != 'PASS_EXACT_SIX_PARENTS_AND_SOURCES'

        or v2.get('full_regression_passed')
        != 3013

        or v2.get('result_sha256')
        != PARENTS['GAMMA_R2_JSON'][1]
    ):
        raise RuntimeError(
            'R2_VERIFICATION_CHAIN_DRIFT'
        )

    return found


def main():
    import numpy as np

    now = dt.datetime.now(
        dt.timezone.utc
    )

    stamp = now.strftime(
        '%Y%m%dT%H%M%S%fZ'
    )

    base = 'gamma1_00r3_'+stamp

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

    output = data/(base+'.json')
    sidecar = data/(base+'.json.sha256')
    logfile = logs/(base+'.log')

    result = {
        'branch': 'GAMMA1-00R3',
        'timestamp_utc': now.isoformat(),
        'classification': 'FAILED_OR_INCOMPLETE',

        'parents': {
            name: {
                'path': path,
                'expected': digest,
                'actual': sha(ROOT/path),
            }
            for name, (path, digest) in PARENTS.items()
        },

        'producer_shas': {
            rel: sha(ROOT/rel)
            for rel in SOURCES
        },

        '006D_replaced': False,
        'GAMMA1_01_authorized': False,
        'Earth_down': 'NOT_DERIVED',
        'whole_craft_up': 'NOT_DERIVED',
        'complete_energy_lt10MJ': 'NOT_CERTIFIED',
    }

    rc = 2

    try:
        checked_provenance()

        if 'MISSING' in result[
            'producer_shas'
        ].values():
            raise RuntimeError(
                'R3_PRODUCER_MISSING'
            )

        original = json.loads(
            (
                ROOT/PARENTS['PH16_R2_JSON'][0]
            ).read_text()
        )

        reference = original[
            'scoped_results'
        ]['cases']['12_L12']['Y_preconditioned_joint']

        from antigravity_research.ph16.ph16_04_joint_stationary import (
            Settings,
            JointAction,
            CoulombSource,
            Spec,
        )

        settings = Settings(
            nr=12,
            L=12.0
        )

        if (
            settings.alpha,
            settings.beta,
            settings.n0,
            settings.mass,
            settings.kappa
        ) != (
            .05,
            40.,
            .15,
            1.,
            .5
        ):
            raise RuntimeError(
                'PH16_REPLAY_PARAMETERS_DRIFT'
            )

        # Exactly the historical PH16 producing classes.
        # No edits to PH16, equations, or thresholds.

        mesh = CoulombSource(
            Spec(
                nr=settings.nr,
                L=settings.L
            ),
            self_order=8
        )

        p10, source = mesh.solve(350)

        obj = JointAction(
            mesh,
            settings
        )

        initial = obj.initialize(
            p10,
            source
        )

        pre_seed, pre_meta = obj.precondition_Y(
            initial
        )

        xf, solver_meta = obj.solve(
            pre_seed,
            maxiter=450
        )

        record = validate_native_profile(
            obj,
            xf,
            reference,
            solver_meta
        )

        arrays = record.pop('arrays')

        npz = data/(
            base+'_native_12_L12.npz'
        )

        with npz.open('xb') as handle:
            np.savez_compressed(
                handle,
                **arrays
            )
            handle.flush()
            os.fsync(handle.fileno())

        profile_sha = sha(npz)

        npz_sidecar = npz.with_name(
            npz.name+'.sha256'
        )

        with npz_sidecar.open('x') as handle:
            handle.write(
                profile_sha+'  '+npz.name+'\n'
            )
            handle.flush()
            os.fsync(handle.fileno())

        result.update({
            'classification':
                'PASS_SINGLE_MESH_REPLAY_MATCHED_SCOPED_ACTION_CONTRACT',

            'action_checks':
                algebra(),

            'native_profile_archive': {
                'path': str(
                    npz.relative_to(ROOT)
                ),
                'sha256': profile_sha,
                'array_keys': sorted(arrays),
                'dimensionless_canonical': True,
                'not_historical_exact_state': True,
            },

            'replayed_mesh':
                record['diagnostics'],

            'precondition_Y_metadata':
                pre_meta,

            'replay_method':
                'Original CoulombSource.solve(350), initialize, precondition_Y, JointAction.solve(pre_seed,maxiter=450); no modified equation or threshold',

            'claim':
                'NEW_STATIONARY_REPLAY_MATCHES_ARCHIVED_SCALAR_DIAGNOSTICS_NOT_ORIGINAL_EXACT_ARRAYS',

            'covariant_action_status':
                'OPERATOR_DEFINED_BUT_EARTH_SUPPORT_CONSTITUTIVE_AND_ONSHELL_MATCH_OPEN',

            'full_Lorentzian_mode_health':
                'NOT_CERTIFIED',

            'Einstein_metric':
                'NOT_SOLVED',

            'true_exterior':
                'NOT_CERTIFIED',

            'qualified_survivors': [],

            'decision':
                'USE_NATIVE_PROFILE_FOR_INDEPENDENT_COVARIANT_CONSTRAINT_AND_EINSTEIN_GATE',
        })

        rc = 0

    except Exception as exc:
        result['error'] = str(exc)
        result['traceback'] = traceback.format_exc()
        result['decision'] = (
            'STOP_PRESERVE_FAILURE_NO_PROMOTION'
        )

    raw = (
        json.dumps(
            result,
            indent=2,
            sort_keys=True,
            allow_nan=False
        )+'\n'
    ).encode()

    with output.open('xb') as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())

    result_sha = hashlib.sha256(
        raw
    ).hexdigest()

    with sidecar.open('x') as handle:
        handle.write(
            result_sha+'  '+output.name+'\n'
        )
        handle.flush()
        os.fsync(handle.fileno())

    statements = [
        'RESULT_JSON='+str(output),
        'RESULT_SHA256='+result_sha,

        'CLASSIFICATION='
        +result['classification'],

        'PROFILE_ARCHIVE='
        +result.get(
            'native_profile_archive', {}
        ).get('path', 'NONE'),

        'PROFILE_SHA256='
        +result.get(
            'native_profile_archive', {}
        ).get('sha256', 'NONE'),

        'FULL_LORENTZIAN_HEALTH=NOT_CERTIFIED',
        'EARTH_DOWN_WHOLE_CRAFT_UP=NOT_DERIVED',
        'GAMMA1_01_AUTOMATIC_AUTHORIZATION=NO',
        '006D_REPLACED=NO',
        'RETURN_CODE='+str(rc),
    ]

    with logfile.open('x') as handle:
        handle.write(
            '\n'.join(statements)+'\n'
        )
        handle.flush()
        os.fsync(handle.fileno())

    print(
        '\n'.join(statements),
        flush=True
    )

    return rc


if __name__ == '__main__':
    raise SystemExit(main())
