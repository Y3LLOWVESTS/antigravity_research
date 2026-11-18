"""Independent raw-SHA and SI verifier.

Does not import the GAMMA1-00 atlas implementation.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[2]

PARENTS = {
    'PH16_R2_source':
        'b5468671f6418fad7b6ed01d916ea65a95a1d59252b84d4411beed9709f86df0',
    'PH16_R2_result':
        'ff700285effc35841fbb8d0e20cffa3c8e4b812e6629b549785a2304b716b2b0',
}


def sha(path):
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def main():
    if len(sys.argv) != 2:
        raise ValueError(
            'Supply the exact GAMMA result JSON path'
        )

    output = Path(sys.argv[1]).resolve()

    assert re.fullmatch(
        r'gamma1_00_\d{8}T\d{12}Z\.json',
        output.name
    ), output

    assert output.parent == ROOT/'results/data'

    side = output.with_name(
        output.name+'.sha256'
    )

    assert side.read_text().strip() == (
        sha(output)+'  '+output.name
    )

    r = json.loads(output.read_text())

    assert r['branch'] == 'GAMMA1-00'

    for key, expected in PARENTS.items():
        p = r['provenance'][key]

        assert p['expected_sha256'] == expected
        assert p['actual_sha256'] == expected
        assert sha(ROOT/p['path']) == expected

    for file, claimed in r['gamma_source_shas'].items():
        assert sha(ROOT/file) == claimed

    assert (
        r['classification']
        == 'ATLAS_COMPLETE_SCOPED'
    ), r.get('error')

    assert all(
        r['exact_checked_algebra'].values()
    )

    assert len(r['exact_checked_algebra']) >= 14

    expected = (
        9.80665*299792458**2
        /(4*6.67430e-11)
    )

    assert math.isclose(
        r['SI_conditional_bounds']['DEC_general_min_J'],
        expected,
        rel_tol=2e-15
    )

    assert r['qualified_survivors'] == []
    assert r['GAMMA1_01_authorized'] is False
    assert r['006D_replaced'] is False

    assert (
        r['complete_energy_lt10MJ']
        == 'NOT_CERTIFIED'
    )

    assert (
        r['force_ledger']['whole_craft_up']
        == 'NOT_DERIVED'
    )

    print(
        'GAMMA1_00_INDEPENDENT_VERIFICATION=PASS'
    )
    print('RESULT_SHA256='+sha(output))


if __name__ == '__main__':
    main()
