"""Independent SHA/native-array verifier.

Does not import the producing R3 science module or rerun PH16.
"""
import hashlib
import json
from pathlib import Path
import re
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]


def sha(path):
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def main():
    assert len(sys.argv) == 2, (
        'Supply exact immutable R3 result'
    )

    path = Path(
        sys.argv[1]
    ).resolve()

    assert path.parent == ROOT/'results/data'

    assert re.fullmatch(
        r'gamma1_00r3_\d{8}T\d{12}Z\.json',
        path.name
    )

    sidecar = path.with_name(
        path.name+'.sha256'
    )

    assert sidecar.read_text().strip() == (
        sha(path)+'  '+path.name
    )

    doc = json.loads(
        path.read_text()
    )

    assert doc['classification'] == (
        'PASS_SINGLE_MESH_REPLAY_MATCHED_SCOPED_ACTION_CONTRACT'
    )

    assert doc['branch'] == 'GAMMA1-00R3'
    assert len(doc['parents']) == 8

    for parent in doc['parents'].values():
        assert (
            parent['actual']
            == parent['expected']
            == sha(ROOT/parent['path'])
        )

    for relative, expected in doc[
        'producer_shas'
    ].items():
        assert sha(ROOT/relative) == expected

    assert len(doc['action_checks']) >= 9
    assert all(doc['action_checks'].values())

    record = doc['native_profile_archive']
    file_path = ROOT/record['path']

    assert record['sha256'] == sha(file_path)

    npz_sidecar = file_path.with_name(
        file_path.name+'.sha256'
    )

    assert npz_sidecar.read_text().strip() == (
        sha(file_path)+'  '+file_path.name
    )

    with np.load(
        file_path,
        allow_pickle=False
    ) as arrays:
        assert set(arrays.files) == set(
            record['array_keys']
        )

        mesh = doc['replayed_mesh']['mesh']
        n = mesh['nr']*mesh['nz']

        for key in arrays.files:
            # All cellwise arrays contain N entries.
            # The complete F+/F-/X/Y gradient contains 4N.
            expected_shape = (
                (4*n,)
                if key == 'joint_gradient'
                else (n,)
            )

            assert arrays[key].shape == (
                expected_shape
            ), key

            assert np.isfinite(
                arrays[key]
            ).all(), key

        P = (
            arrays['E_X_r']*arrays['B_Y_r']
            +arrays['E_X_z']*arrays['B_Y_z']
        )

        sigma = .05*P-40*P*P

        assert np.allclose(
            P,
            arrays['P'],
            rtol=1.e-10,
            atol=1.e-12
        )

        assert np.allclose(
            sigma,
            arrays['sigma'],
            rtol=1.e-10,
            atol=1.e-12
        )

        assert np.linalg.norm(
            arrays['joint_gradient']
        ) < 1.e-6

        assert np.all(
            arrays['weights'] > 0
        )

        assert np.all(
            arrays['neutral_n'] > 0
        )

        assert np.isclose(
            np.max(np.abs(P)),
            doc['replayed_mesh']['Pmax'],
            rtol=1.e-10
        )

        assert np.isclose(
            np.linalg.norm(arrays['A_Y']),
            doc['replayed_mesh']['Y_norm'],
            rtol=1.e-10
        )

    replay = doc['replayed_mesh']

    assert replay['root_success'] is True

    assert (
        replay['frozen_magnetic_margin_min']
        > 0
    )

    assert (
        replay['frozen_negative_cells']
        == 0
    )

    assert len(replay['Noether_N']) == 2

    assert all(
        abs(value-400) < 1.e-8
        for value in replay['Noether_N']
    )

    assert doc['claim'] == (
        'NEW_STATIONARY_REPLAY_MATCHES_ARCHIVED_SCALAR_DIAGNOSTICS_NOT_ORIGINAL_EXACT_ARRAYS'
    )

    assert doc[
        'full_Lorentzian_mode_health'
    ] == 'NOT_CERTIFIED'

    assert doc[
        'whole_craft_up'
    ] == 'NOT_DERIVED'

    assert doc[
        'complete_energy_lt10MJ'
    ] == 'NOT_CERTIFIED'

    assert doc['qualified_survivors'] == []

    assert doc[
        'GAMMA1_01_authorized'
    ] is False

    assert doc[
        '006D_replaced'
    ] is False

    print(
        'GAMMA1_00R3_INDEPENDENT_VERIFICATION=PASS'
    )

    print(
        'RESULT_SHA256='+sha(path)
    )

    print(
        'PROFILE_SHA256='+sha(file_path)
    )


if __name__ == '__main__':
    main()
