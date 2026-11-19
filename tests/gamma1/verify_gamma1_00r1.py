"""Independent verifier; does not import the producing science atlas."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]

EXPECTED = {
    'PH16_R2_source':
        'b5468671f6418fad7b6ed01d916ea65a95a1d59252b84d4411beed9709f86df0',

    'PH16_R2_result':
        'ff700285effc35841fbb8d0e20cffa3c8e4b812e6629b549785a2304b716b2b0',

    'GAMMA1_00_result':
        '480b9228b994f2634fe57ed23b7332e721d9060f43848bdc19e3ace0fb2cc16b',

    'GAMMA1_00_verification':
        '5b34d63219e0bf41af376b9f55064883134c1e75f381166c0c87293d21ccf39d',
}


def digest(path):
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def main():
    if len(sys.argv) != 2:
        raise ValueError(
            'Provide exact GAMMA1-00R1 result path'
        )

    path = Path(sys.argv[1]).resolve()

    assert re.fullmatch(
        r'gamma1_00r1_\d{8}T\d{12}Z\.json',
        path.name
    )

    assert path.parent == ROOT/'results/data'

    side = path.with_name(
        path.name+'.sha256'
    )

    assert side.read_text().strip() == (
        digest(path)+'  '+path.name
    )

    result = json.loads(
        path.read_text()
    )

    assert result['branch'] == 'GAMMA1-00R1'

    assert result['parent_provenance'] == (
        'PASS_EXACT_FOUR_PARENTS'
    )

    assert result['classification'] == (
        'SCOPED_LOCAL_VARIATION_AND_SIGN_ATLAS'
    )

    for name, expected in EXPECTED.items():
        entry = result['provenance'][name]

        assert entry['expected_sha256'] == expected
        assert entry['actual_sha256'] == expected
        assert digest(ROOT/entry['path']) == expected

    for source, sha in result[
        'producing_sources_sha256'
    ].items():
        assert digest(ROOT/source) == sha

    assert len(result['exact_algebra']) >= 12
    assert all(result['exact_algebra'].values())

    trials = result[
        'local_one_action_metric_field_variations'
    ]

    assert set(trials) == {
        'nontrivial_isotropic',
        'nontrivial_anisotropic',
        'coupling_off',
        'both_carriers_off',
        'negative_kinetic_offshell'
    }

    for name, entry in trials.items():
        assert entry['max_relative_error'] < 5.e-7, name

    assert math.isclose(
        trials['negative_kinetic_offshell'][
            'electric_kinetic_min_eigen'
        ],
        -9.23952,
        rel_tol=2.e-12
    )

    assert trials['nontrivial_isotropic'][
        'electric_kinetic_min_eigen'
    ] > 0

    assert trials['nontrivial_isotropic'][
        'local_active_matter_S'
    ] < 0

    assert trials['negative_kinetic_offshell'][
        'local_active_matter_S'
    ] > 0

    dipoles = result['dipole_exterior_trials']

    assert dipoles['aligned']['sign'] == 'OUTWARD'
    assert dipoles['antialigned']['sign'] == 'INWARD'

    for label, d in [
        ('aligned', 1.e-3),
        ('antialigned', -1.e-3)
    ]:
        expected = (
            24*.05*d/2**7
            -192*40*d*d/2**13
        )

        assert math.isclose(
            dipoles[label]['outward_portal_a_over_c2'],
            expected,
            rel_tol=1.e-13
        )

    assert not result['GAMMA1_01_authorized']
    assert not result['006D_replaced']
    assert result['qualified_survivors'] == []

    assert result['theorems'][
        'Earth_down_and_whole_craft_up'
    ] == 'NOT_DERIVED'

    print(
        'GAMMA1_00R1_INDEPENDENT_VERIFICATION=PASS'
    )
    print('RESULT_SHA256='+digest(path))


if __name__ == '__main__':
    main()
