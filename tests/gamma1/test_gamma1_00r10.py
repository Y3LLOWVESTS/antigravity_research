"""Focused R10 exact static reduction, off-shell stress control, restricted kinetics."""
from pathlib import Path
import numpy as np
import pytest

from antigravity_research.gamma1.gamma1_00r10_lorentzian_preflight import (
    PH16_SHA,R3_SHA,R5_SHA,R9_RESULT_SHA,R9_VERIFY_SHA,R9_ARCHIVE_SHA,
    sha,exact_lorentzian_necessary_identities,numerical_evidence,
)

ROOT=Path(__file__).resolve().parents[2]


@pytest.fixture(scope='module')
def observation():
    with np.load(
        ROOT/'results/data/gamma1_00r3_20261119T001454764826Z_native_12_L12.npz',
        allow_pickle=False
    ) as native, np.load(
        ROOT/'results/data/gamma1_00r5_20261119T024922295970Z_lattice_multiplier_12_L12.npz',
        allow_pickle=False
    ) as r5:

        return numerical_evidence(
            {k:native[k].copy() for k in native.files},
            {k:r5[k].copy() for k in r5.files}
        )


@pytest.mark.parametrize('rel,expected',[
 ('src/antigravity_research/ph16/ph16_04_joint_stationary.py',PH16_SHA),
 ('results/data/gamma1_00r3_20261119T001454764826Z_native_12_L12.npz',R3_SHA),
 ('results/data/gamma1_00r5_20261119T024922295970Z_lattice_multiplier_12_L12.npz',R5_SHA),
 ('results/data/gamma1_00r9_20261119T050922694396Z.json',R9_RESULT_SHA),
 ('results/data/gamma1_00r9_verification_20261119T052236433890Z.json',R9_VERIFY_SHA),
 ('results/data/gamma1_00r9_20261119T050922694396Z_Y_axis_regular_12_L12.npz',R9_ARCHIVE_SHA),
])
def test_parent_raw_hash(rel,expected):
    assert sha(ROOT/rel)==expected


def test_exact_13_restricted_identities():
    d=exact_lorentzian_necessary_identities()
    assert len(d)==13 and all(d.values())


def test_stationary_noether_400_400(observation):
    assert np.allclose(
        observation['beta40']['charge_numbers'],
        [400.,400.],
        rtol=0,
        atol=1e-9
    )


def test_X_total_charge_neutral(observation):
    assert abs(
        observation['beta40']['net_X_gauge_charge']
    )<1e-9


def test_lambda_recovered_from_original_action(observation):
    lo,hi=observation['beta40']['lambda_range']
    assert lo < hi < 0
    assert observation['beta40']['lambda_finite_difference_max_abs']<1e-3


def test_chi_second_variation(observation):
    lo,hi=observation['beta40']['chi_range']
    assert 0<lo<hi
    assert observation['beta40']['chi_finite_difference_max_abs']<2e-2


def test_fixed_background_electric_positive(observation):
    d=observation['beta40']
    assert d['electric_rank_one_min']>1
    assert d['negative_electric_cells']==0


def test_fixed_background_magnetic_positive(observation):
    d=observation['beta40']
    assert d['magnetic_rank_one_min']>.2
    assert d['negative_magnetic_cells']==0


def test_beta60_offshell_warning(observation):
    d=observation['beta60_OFFSHELL_FROZEN_PROFILE_CONTROL']
    assert d['negative_magnetic_cells']==4
    assert d['magnetic_rank_one_min']<0


def test_beta60_is_not_stationary(observation):
    assert observation[
        'beta60_OFFSHELL_FROZEN_PROFILE_CONTROL'
    ]['original_PH16_stationarity_beta60']=='NOT_CLAIMED'


def test_fluid_redshifted_chemical_equilibrium(observation):
    assert observation[
        'beta40'
    ]['redshifted_fluid_mu_spread']<1e-12


def test_monopole_only_energy_bound(observation):
    d=observation['single_monopole_SI_CONTROL_ONLY']
    assert d['rest_energy_J']>1e28
    assert d['scope'].startswith('POINT_MONOPOLE_')


def test_missing_full_gravity_explicit(observation):
    d=observation['obstructions']
    assert d['Earth_down_whole_craft_up']=='NOT_DERIVED'
    assert d['full_constrained_Lorentzian_symbol']=='NOT_COMPUTED'
    assert d['complete_energy_lt10MJ']=='NOT_CERTIFIED'


def test_no_sourced_lift_from_static_blocks(observation):
    assert observation[
        'obstructions'
    ]['actual_source_off_and_Earth_present']=='NOT_SOLVED'
