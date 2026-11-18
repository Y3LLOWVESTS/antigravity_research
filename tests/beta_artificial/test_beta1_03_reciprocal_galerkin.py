"""BETA1-03 exact signs, real P10 source, reciprocal source/X/Y L1 witnesses."""
from functools import lru_cache
import pytest
import math
from antigravity_research.beta_artificial.beta1_03_reciprocal_galerkin import report,exact_identities,CASES

@lru_cache(maxsize=1)
def R():return report()

# 10 independent exact-action identity assertions.
@pytest.mark.parametrize('name',[
 'same_action_Y_drive','same_action_Y_curvature_fixed_phase',
 'Y0_stationary_alpha0','Y0_not_stationary_alpha_nonzero_generic',
 'beta_enters_linear_Y_response','beta_critical_coefficient',
 'induced_P_order_alpha','Y_source_sign_matches_PH15',
 'independent_alpha0_beta0_maxwell','linear_drive_independent_beta'])
def test_01_exact_action_identities(name):assert exact_identities()['checks'][name]

# 28 scoped scientific gates are independently asserted and fail closed.
@pytest.mark.parametrize('gate',[
 'symbolic_10','P10_source_reused_all','same_action_baseline_energy',
 'baseline_reduced_stationarity','Gauss_source_exact_baseline',
 'Gauss_relaxed_scalar_modes_positive_baseline','nonzero_alpha_induces_Y',
 'reduced_stationarity_for_beta_upto60','fixed_individual_Noether',
 'neutral_net_X_charge','alpha_linear_Y_scaling_small',
 'source_alpha_squared_scaling','beta_changes_leading_alpha_response',
 'beta60_amplification_over_beta0','beta80_Y_stiffness_negative_control',
 'beta80_not_claimed_healthy','nonzero_unprojected_equation_remainder',
 'small_beta40_portal_sigma','positive_y_fixed_source_at_beta0',
 'no_full_PDE_or_Earth_promotion','positive_reduced_schur_beta_le60',
 'independent_cross_variation_reciprocal','independent_fourpoint_variation',
 'Y_magnetic_Bianchi','Y_static_Gauss','fixedN_neutral_local_gauge_Ward',
 'grid_sensitivity_not_falsely_converged','domain_sensitivity_not_falsely_converged'])
def test_02_scientific_gates(gate):assert R()['gates'][gate]

# 3-source explicit checks: 3*4=12 tests, total 10+28+12=50 focused tests.
@pytest.mark.parametrize('key',[c[0] for c in CASES])
def test_03_per_source_20_modes(key):
    b=R()['cases'][key]['basis']
    assert b['scalar_modes']==6 and b['X_Gauss_response_modes']==6 and b['Y_axisymmetric_modes']==8
    assert b['full_Y_PDE']=='NOT_SOLVED'

@pytest.mark.parametrize('key',[c[0] for c in CASES])
def test_04_per_source_true_noether(key):
    c=R()['cases'][key]
    for beta in ('0','20','40','60'):
        for x in c['fixed_beta_scans'][beta]:
            assert x['fixed_N_error_inf']<1e-8
            assert abs(x['net_X_charge'])<1e-8

@pytest.mark.parametrize('key',[c[0] for c in CASES])
def test_05_per_source_healthy_small_beta(key):
    c=R()['cases'][key]
    for beta in ('0','20','40','60'):
        assert c['fixed_beta_scans'][beta][1]['Y_Schur_static_min']>0

@pytest.mark.parametrize('key',[c[0] for c in CASES])
def test_06_per_source_open_unprojected_equations(key):
    c=R()['cases'][key]
    assert c['omitted_equation_probe']['unprojected_joint_L2']>1e-6
    assert c['fixed_beta_scans']['40'][1]['reduced_stationarity']<1e-6
    assert c['independent_Ward_mixed_variation']['cross_derivative_fourpoint_error']<1e-5


def test_07_no_force_or_006D_promotion():
    r=R()
    assert r['physical_transfer']=='NOT_AUTHORIZED'
    assert r['verdict'].startswith('YELLOW_')
    assert 'No Earth-down craft-up' in '; '.join(r['limits'])


def test_08_correct_test_count():
    r=R()
    assert len(r['cases'])==3 and len(r['gates'])==28 and len(r['symbolic']['checks'])==10
    assert all(r['gates'].values())

# Total tests: 10 + 28 + 12 + 2 = 52.
