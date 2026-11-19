"""Focused R8 original-action finite exterior Schur gates; no PH16 replay."""
from pathlib import Path

import numpy as np
import pytest

from antigravity_research.gamma1.gamma1_00r8_boundary_schur import (
    sha,analyze,exterior_schur,extended_indices,EXTENTS,
    PH16_SHA,P8_SHA,P10_SHA,R3_SHA,
)

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope='module')
def report():
    p = (
        ROOT/
        'results/data/gamma1_00r3_20261119T001454764826Z_native_12_L12.npz'
    )

    with np.load(p,allow_pickle=False) as f:
        native = {
            k:f[k].copy()
            for k in ('A_X','A_Y')
        }

    return analyze(native)


def test_original_PH16_hash():
    assert sha(
        ROOT/'src/antigravity_research/ph16/ph16_04_joint_stationary.py'
    ) == PH16_SHA


def test_original_P8_hash():
    assert sha(
        ROOT/'src/antigravity_research/agminer/hook17_ph15_p8_electric_dipole.py'
    ) == P8_SHA


def test_original_P10_hash():
    assert sha(
        ROOT/'src/antigravity_research/agminer/hook17_ph15_p10_free_space.py'
    ) == P10_SHA


def test_native_sha():
    assert sha(
        ROOT/'results/data/gamma1_00r3_20261119T001454764826Z_native_12_L12.npz'
    ) == R3_SHA


def test_index_count_and_uniqueness():
    for ext in EXTENTS:
        ids = extended_indices(ext)
        assert ids.shape == (288,)
        assert len(np.unique(ids)) == 288


def test_reject_invalid_outer():
    with pytest.raises(ValueError):
        extended_indices(12)


@pytest.mark.parametrize('ext',EXTENTS)
def test_every_interface_is_46_cells(ext):
    s = exterior_schur(ext)
    assert len(s['X']['rim']) == len(s['Y']['rim']) == 46
    assert np.array_equal(
        s['X']['rim'],
        s['Y']['rim']
    )


@pytest.mark.parametrize('sector',('X','Y'))
def test_corrected_matrix_is_reciprocal_positive(report,sector):
    a = exterior_schur(60)[sector]['operator']
    assert np.max(abs(a-a.T)) < 4e-10
    assert np.min(np.linalg.eigvalsh(a)) > 0


@pytest.mark.parametrize('sector',('X','Y'))
def test_boundary_only_correction(report,sector):
    assert all(
        m['carriers'][sector]['correction_only_on_box_rim']
        for m in report['finite_exterior_schur_sweep']
    )


def test_X_native_gradient_improves_more_than_tenfold(report):
    old = report[
        'reference_local_dirichlet_native'
    ]['X']['native_gradient_relative_best_scaled_DIAGNOSTIC_ONLY']

    new = report[
        'finite_exterior_schur_sweep'
    ][-1]['carriers']['X'][
        'native_gradient_relative_best_scaled_DIAGNOSTIC_ONLY'
    ]

    assert old > 10*new


def test_Y_residual_nonzero(report):
    d = report[
        'finite_exterior_schur_sweep'
    ][-1]['carriers']['Y']

    assert (
        .15
        <d['native_gradient_relative_best_scaled_DIAGNOSTIC_ONLY']
        <.25
    )


def test_no_scaling_used_in_construction(report):
    d = report[
        'finite_exterior_schur_sweep'
    ][-1]['carriers']['X']

    assert d['native_gradient_relative_unscaled'] > .05
    assert d['native_gradient_best_scale_DIAGNOSTIC_ONLY'] != 1


def test_no_infinite_domain_claim(report):
    assert report['scope']['asymptotic_infinite_DtN'] == 'NOT_CERTIFIED'
    assert report['scope']['on_shell_convergence_across_meshes'] == 'NOT_TESTED'


def test_no_earth_or_Einstein_claim(report):
    assert report['scope']['Einstein_metric'] == 'NOT_SOLVED'
    assert report['scope']['Earth_down_whole_craft_up'] == 'NOT_DERIVED'
    assert report['scope']['complete_energy_lt10MJ'] == 'NOT_CERTIFIED'


def test_archive_content(report):
    archive = report['archive']
    assert len(archive) == 11
    assert archive['rim_indices'].shape == (46,)
    assert archive['Y_outer_60_rim_correction'].shape == (46,46)


def test_negative_zero_fields(report):
    a = exterior_schur(24)

    for key in ('X','Y'):
        zero = np.zeros(288)
        assert np.dot(zero,a[key]['operator']@zero) == 0.
        assert np.all(a[key]['operator']@zero == 0)
