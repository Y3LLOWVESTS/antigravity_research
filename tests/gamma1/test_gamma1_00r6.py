"""GAMMA1-00R6 focused restricted-trace and Maxwell operator tests."""
from pathlib import Path

import numpy as np
import pytest

from antigravity_research.gamma1.gamma1_00r6_trace_kernel import (
    PH16_SHA,R3_PROFILE_SHA,R5_MULTIPLIER_SHA,
    analyze,best_single_scale,read_lock,sha,
)

ROOT=Path(__file__).resolve().parents[2]
R3=ROOT/'results/data/gamma1_00r3_20261119T001454764826Z_native_12_L12.npz'
R5=ROOT/'results/data/gamma1_00r5_20261119T024922295970Z_lattice_multiplier_12_L12.npz'

@pytest.fixture(scope='module')
def result():
    return analyze(read_lock(R3,R3_PROFILE_SHA),read_lock(R5,R5_MULTIPLIER_SHA))


def test_unmodified_ph16_hash():
    assert sha(ROOT/'src/antigravity_research/ph16/ph16_04_joint_stationary.py')==PH16_SHA


def test_original_R3_profile_hash():
    assert sha(R3)==R3_PROFILE_SHA


def test_original_R5_multiplier_hash():
    assert sha(R5)==R5_MULTIPLIER_SHA


def test_restricted_trace_matches_288_cells(result):
    assert result['numbers']['restricted_matter_trace_lambda_max_abs_error']<3e-12


def test_trace_same_sign_as_previous_lattice(result):
    assert result['numbers']['trace_portal_multiplier_negative_cells']==288
    assert result['numbers']['trace_portal_multiplier_positive_cells']==0


def test_original_stationary_gradient_unchanged(result):
    assert result['numbers']['stationary_gradient_L2']<1e-6


@pytest.mark.parametrize('sector',('X_electric','Y_magnetic'))
def test_nonlocal_green_not_same_nodal_quadrature(result,sector):
    assert result['kernel_comparison'][sector]['whole_grid']['relative_frobenius_mismatch']>.60


@pytest.mark.parametrize('sector',('X_electric','Y_magnetic'))
def test_interior_mismatch_persists(result,sector):
    assert result['kernel_comparison'][sector]['interior_220x220']['relative_frobenius_mismatch']>.60


def test_local_self_positive_control():
    L=np.array([[2.,-1.],[-1.,2.]])
    assert best_single_scale(L,L)['relative_frobenius_mismatch']<1e-14


def test_local_scaled_seven_control():
    L=np.array([[2.,-1.],[-1.,2.]])
    fit=best_single_scale(7*L,L)
    assert fit['best_scale']==pytest.approx(7.)
    assert fit['relative_frobenius_mismatch']<1e-14


def test_degenerate_comparator_fails():
    with pytest.raises(ValueError):
        best_single_scale(np.eye(2),np.zeros((2,2)))


def test_source_off_coupling_off_not_physical_eom(result):
    assert result['controls']['source_off_coupling_off'].startswith('FORMAL_')


def test_no_fake_einstein_claim(result):
    assert result['interpretation']['Einstein_stress_and_metric']=='NOT_DERIVED'
    assert result['interpretation']['exact_full_covariant_reduction']=='NOT_ESTABLISHED'


def test_archive_arrays_finite(result):
    assert len(result['arrays'])==5
    assert all(a.shape==(288,) and np.all(np.isfinite(a)) for a in result['arrays'].values())
