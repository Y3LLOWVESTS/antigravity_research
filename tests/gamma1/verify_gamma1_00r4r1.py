"""Independent R4R1 verifier erratum; does not import R4 science code.

Preserves the original R4 scientific JSON and failing independent verifier.
Never solves PH16 or promotes a gravitational/spacecraft-force claim.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]

RESULT_REL = (
    'results/data/'
    'gamma1_00r4_20261119T011504749138Z.json'
)

PROFILE_REL = (
    'results/data/'
    'gamma1_00r3_20261119T001454764826Z_native_12_L12.npz'
)

RESULT_SHA = (
    'fc33edeec61f3e0e5c4b260b5aa5151328213356d9187eb7fab615f180ee278d'
)

PROFILE_SHA = (
    '94d3763a8d7705ab3dc8774310cf3b8bba96557a0b80d2c34aa110d00b840d54'
)


def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()


def sidecar_matches(path):
    p = Path(path)

    return (
        p.with_name(
            p.name+'.sha256'
        ).read_text().strip()
        ==sha(p)+'  '+p.name
    )


def calculate_signs(profile_path):
    with np.load(
        profile_path,
        allow_pickle=False
    ) as npz:
        R = npz['rho'].reshape(12, 24)
        Z = npz['z'].reshape(12, 24)
        sig = npz['sigma'].reshape(12, 24)
        p = npz['P'].reshape(12, 24)

        joint = npz['joint_gradient']

        fplus = npz[
            'F_plus'
        ].reshape(12, 24)

        fminus = npz[
            'F_minus'
        ].reshape(12, 24)

        weights = npz['weights']
        n = npz['neutral_n']

    assert len(joint) == 4*288
    assert np.linalg.norm(joint) < 1.e-6

    assert np.all(weights > 0)
    assert np.all(n > 0)

    assert np.max(
        abs(sig-(.05*p-40*p*p))
    ) < 2.e-14

    assert np.all(
        np.isfinite(sig)
    )

    radius = np.hypot(R, Z)

    assert np.all(radius > 0)

    # Independent second-order derivative.
    grad_r = np.gradient(
        sig,
        1.,
        axis=0,
        edge_order=1
    )

    grad_z = np.gradient(
        sig,
        1.,
        axis=1,
        edge_order=1
    )

    radial2 = -(
        R*grad_r+Z*grad_z
    )/radius

    outer = radius >= 6.

    # Independent fourth-order stencil.
    # These arrays ALREADY represent NEGATIVE gradients.

    neg_grad_r = -(
        sig[:-4, :]
        -8*sig[1:-3, :]
        +8*sig[3:-1, :]
        -sig[4:, :]
    )/12.

    neg_grad_z = -(
        sig[:, :-4]
        -8*sig[:, 1:-3]
        +8*sig[:, 3:-1]
        -sig[:, 4:]
    )/12.

    R4 = R[2:-2, 2:-2]
    Z4 = Z[2:-2, 2:-2]

    r4 = radius[2:-2, 2:-2]

    fourth_tail = r4 >= 6.

    # CORRECT:
    # Do not negate the already-negated derivatives again.

    corrected4 = (
        R4*neg_grad_r[:, 2:-2]
        +Z4*neg_grad_z[2:-2, :]
    )/r4

    # Reproduce the original verifier's sign error.
    # This is a historical negative control only.

    prior_bug4 = -corrected4

    boundary = np.zeros(
        (12, 24),
        dtype=bool
    )

    boundary[-1, :] = True
    boundary[:, 0] = True
    boundary[:, -1] = True

    return {
        'second_full_outward':
            int((radial2 > 0).sum()),

        'second_full_inward':
            int((radial2 < 0).sum()),

        'second_inner_samples':
            int((~outer).sum()),

        'second_inner_outward':
            int(np.sum(radial2[~outer] > 0)),

        'second_inner_inward':
            int(np.sum(radial2[~outer] < 0)),

        'second_outer_samples':
            int(outer.sum()),

        'second_outer_outward':
            int(np.sum(radial2[outer] > 0)),

        'second_outer_inward':
            int(np.sum(radial2[outer] < 0)),

        'second_full_min':
            float(radial2.min()),

        'second_full_max':
            float(radial2.max()),

        'fourth_tail_samples':
            int(fourth_tail.sum()),

        'fourth_tail_outward':
            int(np.sum(corrected4[fourth_tail] > 0)),

        'fourth_tail_inward':
            int(np.sum(corrected4[fourth_tail] < 0)),

        'fourth_tail_min':
            float(corrected4[fourth_tail].min()),

        'fourth_tail_max':
            float(corrected4[fourth_tail].max()),

        'original_verifier_wrong_sign_outward':
            int(np.sum(prior_bug4[fourth_tail] > 0)),

        'original_verifier_wrong_sign_inward':
            int(np.sum(prior_bug4[fourth_tail] < 0)),

        'original_verifier_old_minus_corrected_max_abs':
            float(
                np.max(
                    np.abs(
                        prior_bug4[fourth_tail]
                        +corrected4[fourth_tail]
                    )
                )
            ),

        'outer_box_cells':
            int(boundary.sum()),

        'outer_box_max_F_amplitude':
            float(
                max(
                    np.max(abs(fplus[boundary])),
                    np.max(abs(fminus[boundary]))
                )
            ),
    }


def validate_result(original_result=ROOT/RESULT_REL):
    result_path = Path(original_result)

    assert result_path.resolve() == (
        ROOT/RESULT_REL
    ).resolve()

    assert sha(result_path) == RESULT_SHA
    assert sidecar_matches(result_path)

    profile = ROOT/PROFILE_REL

    assert sha(profile) == PROFILE_SHA
    assert sidecar_matches(profile)

    doc = json.loads(
        result_path.read_text()
    )

    assert doc['branch'] == 'GAMMA1-00R4'

    assert doc['classification'] == (
        'PASS_SCOPED_ON_BACKGROUND_PORTAL_GRADIENT_AUDIT'
    )

    assert doc['GAMMA1_01_authorized'] is False
    assert doc['006D_replaced'] is False

    assert doc['whole_craft_up'] == (
        'NOT_DERIVED'
    )

    assert doc['complete_energy_lt10MJ'] == (
        'NOT_CERTIFIED'
    )

    assert doc['qualified_physical_survivors'] == []

    # Raw SHA checks explicitly include the original,
    # failed independent verifier. Do not modify it.

    for relative, expected in doc[
        'producer_shas'
    ].items():
        assert sha(ROOT/relative) == expected, relative

    for parent in doc[
        'provenance'
    ].values():
        assert (
            sha(ROOT/parent['path'])
            ==parent['expected_sha256']
            ==parent['actual_sha256']
        )

    assert doc[
        'provenance'
    ]['R3_profile']['actual_sha256'] == PROFILE_SHA

    old_source = (
        ROOT/'tests/gamma1/verify_gamma1_00r4.py'
    ).read_text()

    old_compact = re.sub(
        r'\s+',
        '',
        old_source
    )

    assert (
        'projected4=(-R4*pr4-Z4*pz4)/rr'
        in old_compact
    ), (
        'Old verifier no longer contains expected '
        'double-negation error'
    )

    measured = calculate_signs(profile)

    expected = {
        'second_full_outward': 248,
        'second_full_inward': 40,

        'second_inner_samples': 56,
        'second_inner_outward': 16,
        'second_inner_inward': 40,

        'second_outer_samples': 232,
        'second_outer_outward': 232,
        'second_outer_inward': 0,

        'fourth_tail_samples': 128,
        'fourth_tail_outward': 128,
        'fourth_tail_inward': 0,

        'original_verifier_wrong_sign_outward': 0,
        'original_verifier_wrong_sign_inward': 128,

        'outer_box_cells': 46,
    }

    for key, value in expected.items():
        assert measured[key] == value, (
            key,
            measured[key],
            value
        )

    assert measured['fourth_tail_min'] > 0

    assert measured[
        'outer_box_max_F_amplitude'
    ] > 0

    assert measured[
        'original_verifier_old_minus_corrected_max_abs'
    ] == 0.

    obs = doc['observations']

    counts = obs[
        'portal_radial_projected_a_over_c2'
    ]

    assert counts[
        'full_mesh'
    ]['outward'] == measured['second_full_outward']

    assert counts[
        'full_mesh'
    ]['inward'] == measured['second_full_inward']

    assert counts[
        'r_at_least_6'
    ]['outward'] == measured['second_outer_outward']

    assert counts[
        'r_at_least_6'
    ]['inward'] == measured['second_outer_inward']

    deep = counts[
        'deep_interior_fourth_order_r_at_least_6'
    ]

    assert deep['samples'] == (
        measured['fourth_tail_samples']
    )

    assert deep['outward'] == (
        measured['fourth_tail_outward']
    )

    assert deep['inward'] == (
        measured['fourth_tail_inward']
    )

    assert np.isclose(
        deep['min'],
        measured['fourth_tail_min'],
        rtol=1.e-12,
        atol=1.e-16
    )

    assert np.isclose(
        deep['max'],
        measured['fourth_tail_max'],
        rtol=1.e-12,
        atol=1.e-16
    )

    assert obs[
        'boundary_diagnostics'
    ]['box_is_exterior_solved'] is False

    status = obs[
        'necessary_status'
    ]

    assert status[
        'physical_metric_Einstein_contribution'
    ] == 'NOT_SOLVED'

    assert status[
        'coupled_Lorentzian_mode_health'
    ] == 'NOT_CERTIFIED'

    return measured


def main():
    if len(sys.argv) != 2:
        raise ValueError(
            'Pass exact original immutable R4 JSON path'
        )

    measured = validate_result(
        sys.argv[1]
    )

    print(
        'GAMMA1_00R4R1_INDEPENDENT_VERIFICATION=PASS'
    )

    print(
        'ERRATUM=PRIOR_FOURTH_ORDER_PROJECTION_DOUBLE_NEGATION'
    )

    print(
        'R4_ORIGINAL_RESULT_SHA256='+RESULT_SHA
    )

    print(
        'R3_NATIVE_PROFILE_SHA256='+PROFILE_SHA
    )

    fields = (
        'second_full_outward',
        'second_full_inward',
        'second_outer_outward',
        'second_outer_inward',
        'fourth_tail_outward',
        'fourth_tail_inward',
        'fourth_tail_min',
        'fourth_tail_max',
        'original_verifier_wrong_sign_outward',
        'original_verifier_wrong_sign_inward',
    )

    for key in fields:
        print(
            key.upper()+'='+str(measured[key])
        )


if __name__ == '__main__':
    main()
