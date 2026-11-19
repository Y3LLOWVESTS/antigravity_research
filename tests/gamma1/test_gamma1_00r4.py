"""Focused on-background checks of immutable GAMMA1-00R3 data."""
from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import pytest

from antigravity_research.gamma1.gamma1_00r4_background_sign import (
    EXPECTED_PROFILE_SHA,
    checked_profile,
    grid_d1,
    inspect,
    sha,
)

ROOT = Path(__file__).resolve().parents[2]

PROFILE = (
    ROOT
    /'results/data'
    /'gamma1_00r3_20261119T001454764826Z_native_12_L12.npz'
)


@pytest.fixture(scope='module')
def evidence():
    return inspect(
        checked_profile(PROFILE)
    )


def test_raw_hash():
    assert sha(PROFILE) == EXPECTED_PROFILE_SHA


def test_archive_shapes():
    native = checked_profile(PROFILE)

    assert len(native) == 15
    assert native['F_plus'].shape == (288,)
    assert native['joint_gradient'].shape == (1152,)


@pytest.mark.parametrize(
    'n',
    [5, 12, 24]
)
def test_D1_of_constant_zero(n):
    assert np.max(
        abs(grid_d1(n, 1.)@np.ones(n))
    ) < 1.e-14


@pytest.mark.parametrize(
    'n',
    [5, 12, 24]
)
def test_D1_of_linear_one(n):
    x = np.arange(
        n,
        dtype=float
    )

    assert np.allclose(
        grid_d1(n, 1.)@x,
        1.,
        atol=1.e-14
    )


def test_no_fake_SI(evidence):
    status = evidence['necessary_status']

    assert status[
        'physical_metric_Einstein_contribution'
    ] == 'NOT_SOLVED'

    assert status[
        'complete_energy_lt10MJ'
    ] == 'NOT_CERTIFIED'


def test_P_reconstruction(evidence):
    assert max(
        evidence[
            'native_reconstruction_max_abs_error'
        ].values()
    ) < 2.e-12


def test_neutral_EOS(evidence):
    assert evidence[
        'neutral_hydrostatic_max_abs_error'
    ] < 2.e-12


def test_source_is_stationary(evidence):
    assert evidence[
        'native_grad_L2'
    ] < 1.e-6


def test_recorded_signs_all(evidence):
    counts = evidence[
        'portal_radial_projected_a_over_c2'
    ]['full_mesh']

    assert (
        counts['outward'],
        counts['inward'],
        counts['zero']
    ) == (248, 40, 0)


def test_inner_sign_mixed(evidence):
    counts = evidence[
        'portal_radial_projected_a_over_c2'
    ]['r_less_6']

    assert (
        counts['samples'],
        counts['outward'],
        counts['inward']
    ) == (56, 16, 40)


def test_outer_sign_on_native_stencil(evidence):
    counts = evidence[
        'portal_radial_projected_a_over_c2'
    ]['r_at_least_6']

    assert counts['samples'] == 232
    assert counts['outward'] == 232
    assert counts['inward'] == 0
    assert counts['min'] > 0


def test_interior_not_only_boundary(evidence):
    counts = evidence[
        'portal_radial_projected_a_over_c2'
    ]['interior_r_at_least_6']

    assert counts['samples'] == 176
    assert counts['outward'] == 176
    assert counts['min'] > 0


def test_fourth_order_independent_stencil(evidence):
    counts = evidence[
        'portal_radial_projected_a_over_c2'
    ]['deep_interior_fourth_order_r_at_least_6']

    assert counts['samples'] == 128
    assert counts['outward'] == 128
    assert counts['min'] > 0


@pytest.mark.parametrize(
    'bin_name',
    [
        '0_to_2',
        '2_to_4',
        '4_to_6',
        '6_to_8',
        '8_to_10',
        '10_to_12',
        '12_and_above',
    ]
)
def test_radial_bins_partition_nonempty(
    evidence,
    bin_name
):
    counts = evidence[
        'portal_radial_projected_a_over_c2'
    ]['radial_bins'][bin_name]

    assert counts['samples'] > 0

    assert counts['samples'] == (
        counts['outward']
        +counts['inward']
        +counts['zero']
    )


def test_all_radial_bins_recombine(evidence):
    bins = evidence[
        'portal_radial_projected_a_over_c2'
    ]['radial_bins']

    assert sum(
        counts['samples']
        for counts in bins.values()
    ) == 288

    assert sum(
        counts['outward']
        for counts in bins.values()
    ) == 248


def test_outer_box_distinguished_from_inner_axis(evidence):
    info = evidence[
        'boundary_diagnostics'
    ]

    assert info[
        'outer_box_cell_count'
    ] == 46

    assert info[
        'inner_axis_cell_count'
    ] == 24

    assert info[
        'outer_box_max_abs_sigma'
    ] > 0

    assert info[
        'box_is_exterior_solved'
    ] is False


def test_all_nulls_are_explicit(evidence):
    info = evidence[
        'negative_controls'
    ]

    assert info[
        'alpha_beta_both_off_sigma_and_gradient'
    ] == 'ZERO_EXACT'

    assert info[
        'both_X_Y_fields_off_sigma_and_gradient'
    ] == 'ZERO_EXACT'

    assert info[
        'Earth_off'
    ] == 'NO_EARTH_VARIABLE_IN_PH16'


def test_not_automatically_portal_lift(evidence):
    status = evidence[
        'necessary_status'
    ]

    assert status[
        'full_test_torus_outward_throughout'
    ] == 'NOT_TESTED'

    assert status[
        'recoil_Earth_down_whole_craft_up'
    ] == 'NOT_DERIVED'


def test_wrong_profile_sha_rejected():
    with pytest.raises(ValueError):
        checked_profile(
            PROFILE,
            '0'*64
        )


def test_corrupt_file_rejected(tmp_path):
    fake = tmp_path/'fake.npz'

    fake.write_bytes(
        b'not an npz'
    )

    expected = hashlib.sha256(
        fake.read_bytes()
    ).hexdigest()

    with pytest.raises(Exception):
        checked_profile(
            fake,
            expected
        )


def test_runner_is_read_only_with_no_replay():
    source = (
        ROOT
        /'simulations/gamma1/gamma1_00r4_background_audit.py'
    ).read_text()

    assert 'checked_profile(' in source
    assert 'JointAction(' not in source

    assert (
        "'GAMMA1_01_authorized': False"
        in source
    )
