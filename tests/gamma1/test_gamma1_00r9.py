"""R9 on-background Y-axis regularity and falsifying controls."""
from pathlib import Path
import numpy as np
import pytest

from antigravity_research.gamma1.gamma1_00r9_axis_regular import (
    PH16_SHA,P8_SHA,P10_SHA,R3_SHA,R8_ARCHIVE_SHA,
    sha,analyze,continuous_azimuthal_identity,
    regular_azimuthal_fv,reduction,EXTENTS,
)

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope='module')
def report():
    with np.load(
        ROOT/'results/data/gamma1_00r3_20261119T001454764826Z_native_12_L12.npz',
        allow_pickle=False
    ) as f:
        native = {'A_Y':f['A_Y'].copy()}

    with np.load(
        ROOT/'results/data/gamma1_00r8_20261119T043910994414Z_interface_Schur_12_L12.npz',
        allow_pickle=False
    ) as f:
        r8 = {k:f[k].copy() for k in f.files}

    return analyze(native,r8)


@pytest.mark.parametrize('rel,digest',[
    (
        'src/antigravity_research/ph16/ph16_04_joint_stationary.py',
        PH16_SHA
    ),
    (
        'src/antigravity_research/agminer/hook17_ph15_p8_electric_dipole.py',
        P8_SHA
    ),
    (
        'src/antigravity_research/agminer/hook17_ph15_p10_free_space.py',
        P10_SHA
    ),
    (
        'results/data/gamma1_00r3_20261119T001454764826Z_native_12_L12.npz',
        R3_SHA
    ),
    (
        'results/data/gamma1_00r8_20261119T043910994414Z_interface_Schur_12_L12.npz',
        R8_ARCHIVE_SHA
    ),
])
def test_parent_hash(rel,digest):
    assert sha(ROOT/rel)==digest


def test_exact_azimuthal_bulk_identity():
    assert continuous_azimuthal_identity()['bulk_identity']


def test_surface_term_not_silently_dropped():
    assert 'surface_term' in continuous_azimuthal_identity()


@pytest.mark.parametrize('ext',EXTENTS)
def test_regular_operator_symmetric_positive(ext):
    A = regular_azimuthal_fv(ext)
    assert np.max(abs((A-A.T).data),initial=0.) < 3e-11
    assert min(A.diagonal()) > 0


@pytest.mark.parametrize('ext',EXTENTS)
def test_interface_size_46(ext):
    _,rim,_ = reduction(
        regular_azimuthal_fv(ext),ext
    )
    assert len(rim)==46


@pytest.mark.parametrize('ext',EXTENTS)
def test_unfitted_native_improvement(report,ext):
    d = next(
        x for x in report['finite_exterior_sweep']
        if x['outer_extent']==ext
    )
    assert (
        d['axis_regular_Aphi_over_rho_FV'][
            'unfitted_relative_gradient_error'
        ]
        <d['R8_azimuthal_mass_FV'][
            'unfitted_relative_gradient_error'
        ]
    )


def test_outer_60_Y_residual_is_still_large(report):
    d = report['finite_exterior_sweep'][-1][
        'axis_regular_Aphi_over_rho_FV'
    ]

    assert .19<d['unfitted_relative_gradient_error']<.23
    assert d['fitted_relative_gradient_error_DIAGNOSTIC']>.12


def test_axis_two_rows_dominate_original_Y_gradient(report):
    d = report['finite_exterior_sweep'][-1][
        'axis_regular_Aphi_over_rho_FV'
    ]
    assert d['axis_two_rows_original_gradient_fraction']>.98


def test_rim_is_not_dominant(report):
    d = report['finite_exterior_sweep'][-1][
        'axis_regular_Aphi_over_rho_FV'
    ]
    assert d['rim_original_gradient_fraction']<.02


def test_orders_4_8_12_reduce_unfitted_mismatch(report):
    d = report[
        'green_self_cell_order_sensitivity_FIXED_R3_PROFILE'
    ]

    assert (
        d['4']['unfitted_relative_gradient_error']
        >d['8']['unfitted_relative_gradient_error']
        >d['12']['unfitted_relative_gradient_error']
        >.19
    )


def test_order_variation_is_not_new_stationary_solution(report):
    assert report['negative_controls'][
        'quadrature_orders_not_stationary_replays'
    ]=='TRUE'


def test_zero_fields_null_under_regularized_operator():
    A = regular_azimuthal_fv(14)
    zero = np.zeros(A.shape[0])
    assert np.all(A@zero==0)


def test_invalid_extent_rejected():
    with pytest.raises(ValueError):
        regular_azimuthal_fv(12)


def test_archive_shapes(report):
    arrays = report['data_arrays']
    assert arrays['rim_indices'].shape==(46,)
    assert arrays[
        'Y_regular_outer_60_interface_correction'
    ].shape==(46,46)
    assert len(arrays)==5


def test_no_fake_physics(report):
    status = report['physics_status']
    assert status['Einstein_metric_and_force']=='NOT_DERIVED'
    assert status['continuum_Y_operator_equivalence']=='NOT_PROVEN'
    assert status['Earth_down_whole_craft_up']=='NOT_DERIVED'
