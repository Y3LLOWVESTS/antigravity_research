"""Independent GAMMA1-00R2 SHA/provenance and rational witness verification.

Do not import source science module; no re-solve of PH16.
"""
from __future__ import annotations

from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
PARENT_DIGESTS = {
    'PH16_R2_source': 'b5468671f6418fad7b6ed01d916ea65a95a1d59252b84d4411beed9709f86df0',
    'PH16_R2_result': 'ff700285effc35841fbb8d0e20cffa3c8e4b812e6629b549785a2304b716b2b0',
    'GAMMA1_00_result': '480b9228b994f2634fe57ed23b7332e721d9060f43848bdc19e3ace0fb2cc16b',
    'GAMMA1_00_verification': '5b34d63219e0bf41af376b9f55064883134c1e75f381166c0c87293d21ccf39d',
    'GAMMA1_00R1_result': 'b543157cddb1e1e97c5260bf1de0ef39b329e7b0ea3b96fb12ed33df20d81e08',
    'GAMMA1_00R1_verification': 'e92a73b0a6101e0a980fcab208c9140d55cb25382fb9fe83035763749fd05b63',
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if len(sys.argv) != 2:
        raise ValueError('Supply exact GAMMA1-00R2 immutable result JSON')
    path = Path(sys.argv[1]).resolve()
    assert path.parent == ROOT/'results/data'
    assert re.fullmatch(r'gamma1_00r2_\d{8}T\d{12}Z\.json', path.name)
    side = path.with_name(path.name+'.sha256')
    assert side.read_text().strip() == digest(path)+'  '+path.name
    doc = json.loads(path.read_text())
    assert doc['branch'] == 'GAMMA1-00R2'
    assert doc['classification'] == 'PASS_SCOPED_NONUNIQUENESS_AND_EVIDENCE_SUFFICIENCY'
    assert doc['parent_provenance'] == 'PASS_EXACT_SIX_PARENTS_AND_SOURCES'
    for name, value in PARENT_DIGESTS.items():
        p = doc['provenance'][name]
        assert p['expected_sha256'] == value
        assert p['actual_sha256'] == value
        assert digest(ROOT/p['path']) == value
    for relpath, expected in doc['producing_sources_sha256'].items():
        assert digest(ROOT/relpath) == expected
    ph16 = json.loads((ROOT/doc['provenance']['PH16_R2_result']['path']).read_text())
    cases = ph16['scoped_results']['cases']
    audit = doc['PH16_R2_saved_data']
    assert set(cases) == {'12_L12', '18_L12', '12_L16'}
    for key, case in cases.items():
        joint = case['Y_preconditioned_joint']
        assert set(audit['missing_final_arrays_per_mesh'][key]) == {'F','A','Y'}
        assert not {'F','A','Y'} <= joint.keys()
        assert math.isclose(joint['final_residual_L2'], audit['cases'][key]['joint_residual_L2'], rel_tol=1e-13)
    assert audit['can_evaluate_actual_background_local_kinetic_matrix'] is False
    checks = doc['covariant_completion_nonuniqueness']['exact_checks']
    assert len(checks) >= 10 and all(checks.values())
    assert 'NOT_PROPOSED_NEW_PHYSICS' in doc['covariant_completion_nonuniqueness']['role']
    h = Fraction(1, 1024)
    for eta in (-2, 0, 2):
        def lag(E):
            return Fraction(1+eta, 2)*E*E
        hessian = (lag(h)+lag(-h)-2*lag(Fraction(0)))/(h*h)
        assert int(hessian) == doc['independent_fraction_electric_hessian'][str(eta)]
    assert doc['qualified_physical_survivors'] == []
    assert doc['GAMMA1_01_authorized'] is False
    assert doc['006D_replaced'] is False
    assert doc['Earth_down'] == 'NOT_DERIVED'
    assert doc['whole_craft_up'] == 'NOT_DERIVED'
    assert doc['complete_SI_energy_lt10MJ'] == 'NOT_CERTIFIED'
    print('GAMMA1_00R2_INDEPENDENT_VERIFICATION=PASS')
    print('RESULT_SHA256='+digest(path))


if __name__ == '__main__':
    main()
