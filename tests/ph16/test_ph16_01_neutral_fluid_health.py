"""PH16-01: 105 independent exact, numerical, and fail-closed scope tests."""
from functools import lru_cache
import numpy as np
import pytest
from antigravity_research.ph16.ph16_01_neutral_fluid_health import (
    exact_atlas, report, hydro_profile, principal_coefficients,
    finite_difference_principal, trace,
)

@lru_cache(maxsize=1)
def R():return report()

EXACT=tuple(exact_atlas()['checks'])
GATES=(
 'symbolic_all_exact','real_P10_3_reconstructions','source_P10_charge_neutral',
 'source_fixed_noether_each_species','source_base_EOM_converged',
 'source_base_X_gauss_converged','fluid_density_positive','fluid_number_preservation',
 'fluid_hydrostatic_mu_first_integral','fluid_hydrostatic_Euler_local',
 'fluid_WEC_positive','fluid_DEC_positive','fluid_sound_speed_sub_luminal',
 'fluid_sigma_weak_oneway','fluid_density_readjusts','hydrostatic_density_induction_nonzero',
 'arbitrary_Gaussian_same_number','arbitrary_Gaussian_is_not_hydrostatic',
 'hydrostatic_source_smaller_than_imposed_profile','constant_trace_no_local_Y_drive',
 'constant_trace_still_modifies_Y_stiffness','beta0_frozen_magnetic_positive',
 'beta40_frozen_magnetic_positive','beta60_frozen_magnetic_negative',
 'beta80_frozen_magnetic_negative','critical_beta_between_40_and60',
 'beta40_second_variation_independent_FD','some_negative_cells_at_beta60',
 'Y_electric_frozen_kinetic_positive','full_coupled_modes_not_claimed_healthy',
 'fluid_not_claimed_real_Earth','missing_source_recognition','missing_Einstein_recognition',
 'missing_support_boundaries','missing_full_craft_reaction','missing_SI_and_complete_energy',
)
CASES=('12_L12','18_L12','12_L16')

@pytest.mark.parametrize('name',EXACT)
def test_01_symbolic_exact_variation(name):assert exact_atlas()['checks'][name]

@pytest.mark.parametrize('name',GATES)
def test_02_scoped_scientific_gate(name):assert R()['gates'][name]

@pytest.mark.parametrize('case',CASES)
def test_03_protected_P10_source(case):
    s=R()['cases'][case]['source']
    assert abs(s['net_X_charge'])<1e-8
    assert max(abs(x-400) for x in s['Noether'])<1e-5
    assert s['base_free_X_Gauss_residual']<1e-9

@pytest.mark.parametrize('case',CASES)
def test_04_hydrostatic_number_and_positivity(case):
    f=R()['cases'][case]['neutral_hydrostatic_ONE_WAY']
    assert f['number_preservation_abs_error']<1e-8
    assert f['positive_min_density']>0

@pytest.mark.parametrize('case',CASES)
def test_05_redshifted_mu_Euler_balance(case):
    f=R()['cases'][case]['neutral_hydrostatic_ONE_WAY']
    assert f['redshifted_mu_max_residual']<1e-11
    assert f['static_Euler_finite_difference_inf']<1e-8

@pytest.mark.parametrize('case',CASES)
def test_06_fluid_sound_mode_DEC(case):
    f=R()['cases'][case]['neutral_hydrostatic_ONE_WAY']
    assert 0<f['minimum_sound_speed_squared']<=f['maximum_sound_speed_squared']<1
    assert f['minimum_energy_minus_abs_pressure']>0

@pytest.mark.parametrize('case',CASES)
def test_07_gaussian_same_number_but_off_hydrostatic(case):
    f=R()['cases'][case]['neutral_hydrostatic_ONE_WAY']
    assert f['gaussian_number_error']<1e-8
    assert f['arbitrary_Gaussian_redshifted_mu_range']>.001

@pytest.mark.parametrize('case',CASES)
def test_08_hydro_does_not_falsely_claim_zero_loading(case):
    f=R()['cases'][case]['neutral_hydrostatic_ONE_WAY']
    assert f['density_response_Y_current_L2']>1e-9
    assert f['ratio_hydro_over_arbitrary']<.01
    assert f['constant_fluid_trace_changes_Y_stiffness']

@pytest.mark.parametrize('case',CASES)
def test_09_beta40_positive_frozen_margin(case):
    h=R()['cases'][case]['principal_Y_frozen_background']
    assert h['scans']['40']['minimum_frozen_magnetic_margin']>0
    assert h['scans']['40']['kinetic_Y_electric_frozen']==1

@pytest.mark.parametrize('case',CASES)
def test_10_beta60_negative_local_principal(case):
    h=R()['cases'][case]['principal_Y_frozen_background']
    assert h['scans']['60']['minimum_frozen_magnetic_margin']<0
    assert h['scans']['60']['negative_cells']>0

@pytest.mark.parametrize('case',CASES)
def test_11_beta80_negative_local_principal(case):
    h=R()['cases'][case]['principal_Y_frozen_background']
    assert h['scans']['80']['minimum_frozen_magnetic_margin']<0
    assert h['scans']['80']['negative_cells']>0

@pytest.mark.parametrize('case',CASES)
def test_12_finite_difference_magnetic_second_variation(case):
    h=R()['cases'][case]['principal_Y_frozen_background']
    assert abs(h['beta40_local_second_B_derivative_FD']-h['beta40_local_second_B_derivative_exact'])<3e-5

@pytest.mark.parametrize('case',CASES)
def test_13_unresolved_whole_craft_and_Einstein(case):
    c=R()['cases'][case]
    assert c['missing']['full_X_Y_source_EOM']=='NOT_SOLVED'
    assert c['missing']['Einstein_EOM']=='NOT_SOLVED'
    assert c['missing']['physical_Earth_down_craft_up']=='NOT_DERIVED'
    assert c['principal_Y_frozen_background']['complete_X_Y_fluid_solid_kinetic_matrix']=='NOT_SOLVED'

@pytest.mark.parametrize('case',CASES)
def test_14_canonical_and_eft_not_physical_promotion(case):
    c=R()['cases'][case]
    assert c['missing']['complete_SI_energy_lt10MJ']=='NOT_CERTIFIED'
    assert c['source']['Y_approximation'].startswith('SOURCE_ONLY_')
    assert c['neutral_hydrostatic_ONE_WAY']['status'].startswith('ONE_WAY_')


def test_15_independent_flat_sigma_hydro_uniform():
    sigma=np.zeros((7,8));w=np.ones((7,8))
    n,C=hydro_profile(sigma,w,1.,.5,.15)
    np.testing.assert_allclose(n,.15,atol=1e-12)
    assert abs(C-1.075)<1e-12


def test_16_independent_chi_sign_and_anti_fake_health():
    K=np.array([[2.,1.]]);U=np.array([[.1,.2]]);E2=np.array([[.1,.2]])
    chi,mag,_,_=principal_coefficients(K,U,E2,.15,1.,.5,.05,80.)
    assert np.allclose(mag,1-chi*E2)
    assert len(R()['symbolic']['checks'])==31 and len(R()['gates'])==36
    assert R()['physical_transfer']=='SCOPED_FLUID_IDENTITY_AND_NECESSARY_PRINCIPAL_HEALTH_ONLY'

# 31 + 36 + 12*3 + 2 = 105 focused tests.
