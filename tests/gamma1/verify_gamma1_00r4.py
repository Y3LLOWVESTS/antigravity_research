"""Independent R4 verifier.

Recomputes gradients directly from the R3 archive using NumPy.
Does not import R4 producing-science code or rerun PH16.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[2]

EXPECTED_PROFILE = (
    '94d3763a8d7705ab3dc8774310cf3b8bba96557a0b80d2c34aa110d00b840d54'
)


def digest(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()


def main():
    if len(sys.argv) != 2:
        raise ValueError(
            'Supply exact immutable R4 result JSON'
        )

    path = Path(
        sys.argv[1]
    ).resolve()

    assert path.parent == ROOT/'results/data'

    assert re.fullmatch(
        r'gamma1_00r4_\d{8}T\d{12}Z\.json',
        path.name
    )

    sidecar = path.with_name(
        path.name+'.sha256'
    )

    assert sidecar.read_text().strip() == (
        digest(path)+'  '+path.name
    )

    record = json.loads(
        path.read_text()
    )

    assert record['classification'] == (
        'PASS_SCOPED_ON_BACKGROUND_PORTAL_GRADIENT_AUDIT'
    )

    assert record['branch'] == 'GAMMA1-00R4'

    assert record[
        'ancestor_validation'
    ]['historical_R3_ancestors'] == 8

    for entry in record[
        'provenance'
    ].values():
        assert (
            entry['actual_sha256']
            ==entry['expected_sha256']
            ==digest(ROOT/entry['path'])
        )

    for relative, expected in record[
        'producer_shas'
    ].items():
        assert digest(ROOT/relative) == expected

    profile = (
        ROOT/record[
            'provenance'
        ]['R3_profile']['path']
    )

    assert digest(profile) == EXPECTED_PROFILE

    with np.load(
        profile,
        allow_pickle=False
    ) as arrays:
        assert len(arrays.files) == 15

        R = arrays['rho'].reshape(12, 24)
        Z = arrays['z'].reshape(12, 24)

        sigma = arrays[
            'sigma'
        ].reshape(12, 24)

        P = arrays['P']

        assert np.max(
            abs(
                sigma.ravel()
                -(.05*P-40*P**2)
            )
        ) < 2.e-14

        assert np.linalg.norm(
            arrays['joint_gradient']
        ) < 1.e-6

        assert np.all(
            arrays['neutral_n'] > 0
        )

        # Independent derivative implementation.
        derivative_r = np.gradient(
            sigma,
            1.,
            axis=0,
            edge_order=1
        )

        derivative_z = np.gradient(
            sigma,
            1.,
            axis=1,
            edge_order=1
        )

        radii = np.hypot(
            R,
            Z
        )

        projected = (
            -(
                R*derivative_r
                +Z*derivative_z
            )/radii
        ).ravel()

        inner = radii.ravel() < 6
        outer = ~inner

        counts = record['observations'][
            'portal_radial_projected_a_over_c2'
        ]

        assert (
            (projected > 0).sum(),
            (projected < 0).sum()
        ) == (248, 40)

        assert (
            outer.sum(),
            np.sum(projected[outer] > 0)
        ) == (232, 232)

        assert (
            inner.sum(),
            np.sum(projected[inner] < 0)
        ) == (56, 40)

        assert np.isclose(
            projected.min(),
            counts['full_mesh']['min'],
            rtol=1.e-12
        )

        assert np.isclose(
            projected.max(),
            counts['full_mesh']['max'],
            rtol=1.e-12
        )

        # Independent 4th-order stencil away from edges.
        pr4 = -(
            sigma[:-4, :]
            -8*sigma[1:-3, :]
            +8*sigma[3:-1, :]
            -sigma[4:, :]
        )/12

        pz4 = -(
            sigma[:, :-4]
            -8*sigma[:, 1:-3]
            +8*sigma[:, 3:-1]
            -sigma[:, 4:]
        )/12

        pr4 = pr4[:, 2:-2]
        pz4 = pz4[2:-2, :]

        R4 = R[2:-2, 2:-2]
        Z4 = Z[2:-2, 2:-2]

        rr = np.hypot(R4, Z4)

        projected4 = (
            -R4*pr4-Z4*pz4
        )/rr

        tail = rr >= 6

        assert tail.sum() == 128

        assert np.all(
            projected4[tail] > 0
        )

        assert np.isclose(
            projected4[tail].min(),
            counts[
                'deep_interior_fourth_order_r_at_least_6'
            ]['min'],
            rtol=1.e-12
        )

        # The computational-box edge is not an exterior proof.
        boundary = np.zeros(
            (12, 24),
            dtype=bool
        )

        boundary[-1, :] = True
        boundary[:, 0] = True
        boundary[:, -1] = True

        assert boundary.sum() == 46

        assert np.isclose(
            max(abs(sigma[boundary])),
            record['observations'][
                'boundary_diagnostics'
            ]['outer_box_max_abs_sigma']
        )

    assert record[
        'qualified_physical_survivors'
    ] == []

    assert record[
        'GAMMA1_01_authorized'
    ] is False

    assert record[
        '006D_replaced'
    ] is False

    status = record[
        'observations'
    ]['necessary_status']

    assert status[
        'physical_metric_Einstein_contribution'
    ] == 'NOT_SOLVED'

    assert status[
        'complete_energy_lt10MJ'
    ] == 'NOT_CERTIFIED'

    assert record[
        'whole_craft_up'
    ] == 'NOT_DERIVED'

    print(
        'GAMMA1_00R4_INDEPENDENT_VERIFICATION=PASS'
    )

    print(
        'RESULT_SHA256='+digest(path)
    )

    print(
        'R3_PROFILE_SHA256='+digest(profile)
    )


if __name__ == '__main__':
    main()
