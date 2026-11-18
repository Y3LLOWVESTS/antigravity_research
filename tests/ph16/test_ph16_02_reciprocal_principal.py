"""PH16-02: 100 exact, gauge, variational and scope tests."""

from functools import lru_cache

import numpy as np
import pytest

from antigravity_research.ph16.ph16_02_reciprocal_principal import (
    exact_identities,
    report,
    full_constitutive,
    transverse_symbol,
    finite_B_dispersion,
    derivative_matrix,
)


@lru_cache(maxsize=1)
def R():
    return report()


@lru_cache(maxsize=1)
def EXACT():
    return exact_identities()


EXACT_NAMES = tuple(EXACT()['checks'])

GATE_NAMES = (
    'exact_one_action_consistency',
    'P10_three_source_reconstructions',
    'P10_net_charge_neutral',
    'P10_scalar_EOM_small',
    'P10_X_Gauss_kernel_residual_small',
    'Y_first_order_nonzero',
    'fluid_number_preserved_all_cases',
    'fluid_mu_hydrostatic_all_cases',
    'Y_Bianchi_all_cases',
    'Y_full_lambda_current_defect_nonzero',
    'X_Gauss_increment_nonzero',
    'local_finite_P_fd_Hessian',
    'positive_beta40_frozen_P0',
    'negative_beta60_frozen_P0',
    'positive_beta40_finite_P',
    'negative_beta60_finite_P',
    'negative_beta80_finite_P',
    'negative_cells_nonzero_at_beta60',
    'two_gauge_transverse_negative_eigen_at_beta60',
    'two_gauge_transverse_positive_all_beta40',
    'three_unmodified_modes_canonical',
    'finite_B_active_kinetic_positive_in_test',
    'finite_B_beta60_negative_speed2',
    'finite_B_beta40_positive_speed2',
    'beta40_stationary_Y_fullcell_projected',
    'beta40_Y_Hessian_positive_restricted',
    'beta40_Y_gradient_FD',
    'beta40_Y_Hessian_FD',
    'source_Noether_constraint_not_reclosed',
    'small_oneway_portal',
    'not_full_on_shell',
    'not_complete_stability_certificate',
)

CASES = ('12_L12','18_L12','12_L16')


@pytest.mark.parametrize('name',EXACT_NAMES)
def test_01_exact_same_action(name):
    assert EXACT()['checks'][name]


@pytest.mark.parametrize('name',GATE_NAMES)
def test_02_scoped_gates(name):
    assert R()['gates'][name]


@pytest.mark.parametrize('case',CASES)
def test_03_protected_P10_EOM(case):
    p = R()['cases'][case]['P10_background']
    assert abs(p['neutral_X_charge'])<1e-8
    assert p['P10_scalar_EOM_weighted_L2_max']<5e-5


@pytest.mark.parametrize('case',CASES)
def test_04_fluid_number_and_redshifted_mu(case):
    for v in R()['cases'][case]['beta_sweep'].values():
        assert v['fluid_number_error']<1e-8
        assert v['fluid_redshifted_mu_error']<1e-10


@pytest.mark.parametrize('case',CASES)
def test_05_Y_Gauss_Bianchi(case):
    for v in R()['cases'][case]['beta_sweep'].values():
        assert v['Y_magnetic_Bianchi_inf']<1e-10


@pytest.mark.parametrize('case',CASES)
def test_06_nonlinear_Y_current_mismatch(case):
    a = R()['cases'][case]['beta_sweep']
    assert (
        a['40']['first_order_Y_current_reciprocity_defect_L2']
        >1e-3
    )


@pytest.mark.parametrize('case',CASES)
def test_07_X_Gauss_portal_increment(case):
    a = R()['cases'][case]['beta_sweep']
    assert a['40']['X_Gauss_portal_increment_L2']>1e-9


@pytest.mark.parametrize('case',CASES)
def test_08_finite_P_two_U1_beta40_positive(case):
    a = R()['cases'][case]['beta_sweep']['40']
    assert (
        a['local_finite_B_dispersion']
        ['squared_phase_speeds'][0]>0
    )


@pytest.mark.parametrize('case',CASES)
def test_09_finite_P_two_U1_beta60_negative(case):
    a = R()['cases'][case]['beta_sweep']['60']
    assert (
        a['local_finite_B_dispersion']
        ['squared_phase_speeds'][0]<0
    )
    assert not (
        a['local_finite_B_dispersion']
        ['cutoff_and_wavelength_certified']
    )


@pytest.mark.parametrize('case',CASES)
def test_10_variational_fullcell_Y40_residual(case):
    y = R()['cases'][case][
        'finite_box_discrete_variational_Y_beta40'
    ]
    assert y['Y_stationary_fullcell_residual_L2']<1e-9


@pytest.mark.parametrize('case',CASES)
def test_11_variational_fullcell_Y40_hessian(case):
    y = R()['cases'][case][
        'finite_box_discrete_variational_Y_beta40'
    ]
    assert y['Y_discrete_Hessian_min_eigenvalue']>0


@pytest.mark.parametrize('case',CASES)
def test_12_independent_action_FD_directional(case):
    y = R()['cases'][case][
        'finite_box_discrete_variational_Y_beta40'
    ]
    assert y['action_gradient_directional_FD_error']<2e-7
    assert y['action_Hessian_directional_FD_error']<2e-7


@pytest.mark.parametrize('case',CASES)
def test_13_source_Noether_not_reclosed(case):
    y = R()['cases'][case][
        'finite_box_discrete_variational_Y_beta40'
    ]
    assert max(
        y['source_Noether_reaction_unresolved_abs_shift']
    )>1e-4

    assert y['joint_source_X_residual']==(
        'NOT_SOLVED_NOT_CLAIMED'
    )


@pytest.mark.parametrize('case',CASES)
def test_13b_beta60_finite_grid_does_not_certify_uv(case):
    y = R()['cases'][case][
        'finite_box_discrete_variational_Y_beta40'
    ]
    expected_negative = case!='12_L16'
    assert (
        (y['beta60_initial_fullcell_Hessian_min_eigenvalue']<0)
        ==expected_negative
    )
    assert (
        R()['cases'][case]['beta_sweep']['60']
        ['actual_first_order_P_margin_min']<0
    )


@pytest.mark.parametrize(
    'pair',
    (
        (1.,2.,.15,0.),
        (1.5,.3,.17,1e-4),
        (-1.,.4,.15,-2e-4),
    ),
)
def test_14_constitutive_finite_difference(pair):
    K,U,n,P = pair
    alpha = .05
    beta = 40.
    mass = 1.
    kappa = .5

    def L(z):
        sig = alpha*z-beta*z*z
        return (
            -K*np.exp(2*sig)
            -U*np.exp(4*sig)
            -mass*n*np.exp(sig)
            -kappa*n*n*np.exp(-2*sig)/2
        )

    lam,chi = full_constitutive(
        K,U,n,alpha,beta,mass,kappa,P
    )
    h = 1e-5

    assert abs(
        (L(P+h)-L(P-h))/(2*h)-lam
    )<1e-5

    assert abs(
        (L(P+h)-2*L(P)+L(P-h))/h**2-chi
    )<2e-4


@pytest.mark.parametrize(
    'khat',
    (
        (1.,0.,0.),
        (0.,1.,0.),
        (0.,0.,1.),
    ),
)
def test_15_transverse_gauge_symbol(khat):
    E = np.array([.1,.2,.3])

    eig,mat,basis,w = transverse_symbol(
        E,50.,khat
    )

    assert np.allclose(mat,mat.T)
    assert (
        np.max(abs(np.array(basis)@np.array(khat)))
        <1e-12
    )
    assert np.sum(abs(eig-1)<1e-12)>=3
    assert np.all(np.isfinite(eig))


def test_16_beta_positive_and_negative_finiteB():
    positive = finite_B_dispersion(
        (.1,0.,0.),(.01,0.,0.),
        40.,(0.,1.,0.)
    )
    negative = finite_B_dispersion(
        (.1,0.,0.),(.01,0.,0.),
        200.,(0.,1.,0.)
    )

    assert positive['squared_phase_speeds'][0]>0
    assert negative['squared_phase_speeds'][0]<0
    assert negative['kinetic_active']>0
    assert not negative['cutoff_and_wavelength_certified']


def test_17_matrix_gradient_linear():
    D = derivative_matrix(15,.3)
    np.testing.assert_allclose(
        D@(np.arange(15)*.3),
        1.,
        atol=1e-12,
    )


def test_18_research_claims_fail_closed():
    r = R()

    assert r['physical_promotion']=='DENIED'
    assert r['full_source_X_Y_fluid_solid_metric_on_shell']==(
        'NOT_SOLVED'
    )
    assert r['3D_Earth_and_whole_craft']=='NOT_DERIVED'
    assert r['1kg_1g_1m_and_lt10MJ']=='NOT_CERTIFIED'


def test_19_counts_and_immutability_expectations():
    assert len(EXACT_NAMES)==22
    assert len(GATE_NAMES)==32
    assert len(R()['cases'])==3
    assert all(R()['gates'].values())


# 22 exact + 32 gates + 12*3 case tests + 10 controls = 100.
