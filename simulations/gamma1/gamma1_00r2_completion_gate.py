"""Immutable GAMMA1-00R2 runner: original PH16/GAMMA provenance mandatory.

No reruns of PH16; no modification of previous JSON/source or thresholds.
Failure itself creates an immutable JSON/SHA/log with nonzero exit status.
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

from antigravity_research.gamma1.gamma1_00r2_completion_gate import (
    hash_file, result_atlas,
)

PARENTS = {
    'PH16_R2_source': (
        'src/antigravity_research/ph16/ph16_04_joint_stationary.py',
        'b5468671f6418fad7b6ed01d916ea65a95a1d59252b84d4411beed9709f86df0'),
    'PH16_R2_result': (
        'results/data/ph16_04_20261118T164454314313Z.json',
        'ff700285effc35841fbb8d0e20cffa3c8e4b812e6629b549785a2304b716b2b0'),
    'GAMMA1_00_result': (
        'results/data/gamma1_00_20261118T202714278070Z.json',
        '480b9228b994f2634fe57ed23b7332e721d9060f43848bdc19e3ace0fb2cc16b'),
    'GAMMA1_00_verification': (
        'results/data/gamma1_00_verification_20261118T204048204526Z.json',
        '5b34d63219e0bf41af376b9f55064883134c1e75f381166c0c87293d21ccf39d'),
    'GAMMA1_00R1_result': (
        'results/data/gamma1_00r1_20261118T211802035544Z.json',
        'b543157cddb1e1e97c5260bf1de0ef39b329e7b0ea3b96fb12ed33df20d81e08'),
    'GAMMA1_00R1_verification': (
        'results/data/gamma1_00r1_verification_20261118T213059468632Z.json',
        'e92a73b0a6101e0a980fcab208c9140d55cb25382fb9fe83035763749fd05b63'),
}

SOURCES = [
    'src/antigravity_research/gamma1/gamma1_00r2_completion_gate.py',
    'simulations/gamma1/gamma1_00r2_completion_gate.py',
    'tests/gamma1/test_gamma1_00r2.py',
    'tests/gamma1/verify_gamma1_00r2.py',
    'theory/gamma1/GAMMA1_00R2_STATIONARY_COMPLETION_LEDGER.md',
]


def check_parent_chain(root: Path, provenance: dict) -> None:
    for key, entry in provenance.items():
        if entry['actual_sha256'] != entry['expected_sha256']:
            raise RuntimeError(f'PARENT_{key}_MISSING_OR_HASH_MISMATCH')
        parent = root/entry['path']
        if parent.suffix == '.json':
            sidecar = parent.with_name(parent.name+'.sha256')
            if not sidecar.is_file() or sidecar.read_text().strip() != (
                entry['actual_sha256']+'  '+parent.name
            ):
                raise RuntimeError(f'PARENT_{key}_SIDECAR_MISMATCH')

    old = json.loads((root/PARENTS['GAMMA1_00_result'][0]).read_text())
    r1 = json.loads((root/PARENTS['GAMMA1_00R1_result'][0]).read_text())
    v0 = json.loads((root/PARENTS['GAMMA1_00_verification'][0]).read_text())
    v1 = json.loads((root/PARENTS['GAMMA1_00R1_verification'][0]).read_text())
    if old.get('classification') != 'ATLAS_COMPLETE_SCOPED':
        raise RuntimeError('GAMMA1_00_parent classification drift')
    if r1.get('classification') != 'SCOPED_LOCAL_VARIATION_AND_SIGN_ATLAS':
        raise RuntimeError('GAMMA1_00R1_parent classification drift')
    if v0.get('full_suite_passed') != 2959 or v1.get('full_regression_passed') != 2986:
        raise RuntimeError('Previous immutable regression count drift')
    if v0.get('atlas_result_sha256') != PARENTS['GAMMA1_00_result'][1]:
        raise RuntimeError('GAMMA1_00 manifest link mismatch')
    if v1.get('atlas_result_sha256') != PARENTS['GAMMA1_00R1_result'][1]:
        raise RuntimeError('GAMMA1_00R1 manifest link mismatch')
    if old.get('GAMMA1_01_authorized') is not False or r1.get('GAMMA1_01_authorized') is not False:
        raise RuntimeError('Prior next-run authorization changed')
    for data, key in ((old, 'gamma_source_shas'), (r1, 'producing_sources_sha256')):
        for relpath, expected in data[key].items():
            if hash_file(root/relpath) != expected:
                raise RuntimeError('PARENT_SOURCE_HASH_DRIFT '+relpath)


def main() -> int:
    now = dt.datetime.now(dt.timezone.utc)
    tag = now.strftime('%Y%m%dT%H%M%S%fZ')
    basename = 'gamma1_00r2_'+tag
    data = ROOT/'results/data'
    logs = ROOT/'results/logs'
    data.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)
    output = data/(basename+'.json')
    sidecar = data/(basename+'.json.sha256')
    logfile = logs/(basename+'.log')
    provenance = {
        key: {'path': path, 'expected_sha256': expected,
              'actual_sha256': hash_file(ROOT/path)}
        for key, (path, expected) in PARENTS.items()
    }
    result = {
        'branch': 'GAMMA1-00R2',
        'timestamp_utc': now.isoformat(),
        'classification': 'FAILED_OR_INCOMPLETE',
        'provenance': provenance,
        'producing_sources_sha256': {path: hash_file(ROOT/path) for path in SOURCES},
        'GAMMA1_01_authorized': False,
        '006D_replaced': False,
        'Earth_down': 'NOT_DERIVED',
        'whole_craft_up': 'NOT_DERIVED',
    }
    status = 2
    try:
        check_parent_chain(ROOT, provenance)
        if any(x == 'MISSING' for x in result['producing_sources_sha256'].values()):
            raise RuntimeError('Producing source missing')
        document = json.loads((ROOT/PARENTS['PH16_R2_result'][0]).read_text())
        result.update(result_atlas(document, ROOT/PARENTS['PH16_R2_source'][0]))
        result['classification'] = 'PASS_SCOPED_NONUNIQUENESS_AND_EVIDENCE_SUFFICIENCY'
        result['parent_provenance'] = 'PASS_EXACT_SIX_PARENTS_AND_SOURCES'
        status = 0
    except Exception as exc:
        result['parent_provenance'] = 'NOT_PASS'
        result['error'] = str(exc)
        result['traceback'] = traceback.format_exc()
        result['decision'] = 'STOP_WITHOUT_PROMOTION'

    raw = (json.dumps(result, sort_keys=True, indent=2, allow_nan=False)+'\n').encode()
    with output.open('xb') as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    sha = hashlib.sha256(raw).hexdigest()
    with sidecar.open('x') as handle:
        handle.write(sha+'  '+output.name+'\n')
        handle.flush()
        os.fsync(handle.fileno())
    statements = [
        'RESULT_JSON='+str(output),
        'RESULT_SHA256='+sha,
        'CLASSIFICATION='+result['classification'],
        'PARENT_PROVENANCE='+result['parent_provenance'],
        'PH16_R2_FINAL_PROFILE_AVAILABLE=NO_OR_NOT_VERIFIED',
        'ACTUAL_PH16_LORENTZIAN_MODE_HEALTH=NOT_DETERMINED',
        'EARTH_DOWN_WHOLE_CRAFT_UP=NOT_DERIVED',
        'GAMMA1_01_AUTOMATIC_AUTHORIZATION=NO',
        '006D_REPLACED=NO',
        'RETURN_CODE='+str(status),
    ]
    with logfile.open('x') as handle:
        handle.write('\n'.join(statements)+'\n')
        handle.flush()
        os.fsync(handle.fileno())
    print('\n'.join(statements), flush=True)
    return status


if __name__ == '__main__':
    raise SystemExit(main())
