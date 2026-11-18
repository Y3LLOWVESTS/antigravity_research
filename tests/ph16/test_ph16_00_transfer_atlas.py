"""PH16-00 independent test vectors and source-only Y limitation checks."""
from functools import lru_cache
import numpy as np
import pytest

from antigravity_research.ph16.ph16_00_transfer_atlas import (
    report,exact_atlas,current_from_lambda,Control
)

@lru_cache(maxsize=1)
def R():
    return report()

THEOREMS=(
 'sigma_prime',
 'source_lambda_chain',
 'neutral_particle_lambda_chain',
 'total_lambda_is_sum',
 'lambda_at_P0_with_neutral',
 'no_portal_alpha0_first_order',
 'beta_changes_local_linear_Y_stiffness',
 'neutral_trace_changes_Y_drive_at_alpha',
 'positive_rest_mass_conformal_particle',
 'test_particle_conformal_accel',
 'mixed_variation_reciprocal',
 'mixed_lambda_at_FY0',
 'Y0_induction_if_no_matter',
 'Y0_induction_if_alpha0',
 'P_is_even_under_simultaneous_F_reversal',
 'P_is_odd_under_single_F_reversal',
 'neutral_test_mass_must_not_be_negative',
 'conformal_Weyl_trace_source',
 'LeviCivita_P_is_metric_density_sensitive',
 'Pontryagin_density_metric_independent',
)

GATES=(
 'exact_20_action_relations',
 'P10_neutral_X_source_in_all_cases',
 'P10_individual_Noether_conserved',
 'P10_scalar_EOM_small',
 'P10_X_Gauss_small',
 'actual_P10_Y_first_order_nonzero',
 'P10_first_order_Y_current_exact_reproduction',
 'static_Y_magnetic_Bianchi',
 'static_X_electrostatic_Bianchi',
 'neutral_load_changes_first_order_Y_current',
 'not_near_zero_relative_neutral_effect',
 'neutral_variable_trace_distinguishable',
 'constant_trace_bulk_null',
 'aligned_trace_integrability_null',
 'no_X_no_induced_Y',
 'reversal_alpha_antisymmetry',
 'linear_neutral_amplitude_at_fixed_background',
 'positive_first_order_Y_kernel_increment_energy',
 'conformal_particle_effect_not_claimed_SI',
 'positive_sensitivity_P_abs',
 'portal_sigma_reduced_small',
 'finite_source_energy_canonical',
 'mesh_energy_not_converged_certified',
 'source_only_Y_not_universal_loaded',
 'Einstein_metric_not_derived',
 'full_reciprocal_EOM_not_derived',
 'no_neutral_payload_force_claim',
)

@pytest.mark.parametrize('key',THEOREMS)
def test_01_independent_exact_action_check(key):
    assert exact_atlas()['checks'][key]

@pytest.mark.parametrize('key',GATES)
def test_02_scoped_science_gate(key):
    assert R()['gates'][key]

@pytest.mark.parametrize('case',('12_L12','18_L12','12_L16'))
def test_03_P10_fixed_Noether_and_source_EOM(case):
    s=R()['cases'][case]['source']
    assert max(abs(q-400) for q in s['Noether'])<1e-5
    assert abs(s['net_X_charge'])<1e-8
    assert max(s['scalar_EOM_weighted_L2'])<5e-5
    assert s['free_X_Gauss_residual']<1e-9

@pytest.mark.parametrize('case',('12_L12','18_L12','12_L16'))
def test_04_source_Y_reproduces_original_P10(case):
    d=R()['cases'][case]['prescribed_neutral_diagnostic']
    assert d['PH15_P10_first_order_current_reproduction_error']<1e-11

@pytest.mark.parametrize('case',('12_L12','18_L12','12_L16'))
def test_05_prescribed_neutral_trace_changes_induction(case):
    d=R()['cases'][case]['prescribed_neutral_diagnostic']
    assert d['neutral_increment_Y_current_weighted_L2']>1e-5
    assert d['neutral_increment_relative_to_source']>1e-3

@pytest.mark.parametrize('case',('12_L12','18_L12','12_L16'))
def test_06_null_controls_not_physical_Earth(case):
    d=R()['cases'][case]['prescribed_neutral_diagnostic']
    assert d['constant_neutral_trace_null_error']<1e-11
    assert d['A0_aligned_trace_null_error']<1e-11
    assert d['source_off_A0_zero_current']==0

@pytest.mark.parametrize('case',('12_L12','18_L12','12_L16'))
def test_07_alpha_reversal_and_density_doubling(case):
    d=R()['cases'][case]['prescribed_neutral_diagnostic']
    assert d['alpha_sign_reversal_error']<1e-11
    assert d['density_amplitude_double_error']<1e-11

@pytest.mark.parametrize('case',('12_L12','18_L12','12_L16'))
def test_08_independent_gauge_Bianchi(case):
    d=R()['cases'][case]['prescribed_neutral_diagnostic']
    assert d['Y_magnetic_Bianchi_inf']<1e-11
    assert d['X_electrostatic_Bianchi_inf']<1e-11

@pytest.mark.parametrize('case',('12_L12','18_L12','12_L16'))
def test_09_no_full_Earth_or_metric_promotions(case):
    d=R()['cases'][case]['prescribed_neutral_diagnostic']
    assert d['physical_Earth_density_EOM']=='NOT_SOLVED'
    assert d['physical_metric_Einstein_EOM']=='NOT_SOLVED'
    assert d['source_X_Y_reciprocal_EOM']=='NOT_SOLVED'
    assert d['physical_force_and_1kg_benchmark']=='NOT_DERIVED'

@pytest.mark.parametrize('case',('12_L12','18_L12','12_L16'))
def test_10_canonical_not_joules(case):
    d=R()['cases'][case]['prescribed_neutral_diagnostic']
    assert d['prescribed_sigma_max_abs']<1
    assert d['first_order_P_abs_integral_canonical']>0
    assert d['fixed_g_test_accel_z_max_abs_CANONICAL_NOT_SI']>0

def test_11_constant_analytic_lambda_null():
    r,z=np.meshgrid(
        np.linspace(.5,4.,9),
        np.linspace(-2,2,9),
        indexing='ij'
    )
    A=np.sin(r)+z*z
    j=current_from_lambda(A,np.full_like(A,3.),.5)
    np.testing.assert_allclose(j,0,atol=1e-14)

def test_12_exact_parallel_gradient_integrability():
    r,z=np.meshgrid(
        np.linspace(.5,4.5,9),
        np.linspace(-2,2,9),
        indexing='ij'
    )
    A=2*r-3*z
    j=current_from_lambda(A,.8*A+1.2,.5)
    np.testing.assert_allclose(j,0,atol=1e-12)

def test_13_transverse_gradient_nonzero():
    r,z=np.meshgrid(
        np.linspace(.5,4.5,9),
        np.linspace(-2,2,9),
        indexing='ij'
    )
    A=2*r-3*z
    lam=5*r+7*z
    j=current_from_lambda(A,lam,.5)
    np.testing.assert_allclose(
        j,-29*np.ones_like(j),atol=1e-12
    )

def test_14_no_false_physical_transfer():
    r=R()
    assert r['transfer_classification']==(
        'REQUIREMENTS_TRANSFER_ONLY_NOT_PHYSICAL_MECHANISM'
    )
    assert r['physical_Earth_down_craft_up']=='NOT_DERIVED'
    assert r['physical_units_and_UV']=='NOT_CERTIFIED'
    assert r['complete_healthy_modes']=='NOT_SOLVED'

def test_15_scientific_gate_and_identity_counts():
    r=R()
    assert len(r['exact']['checks'])==len(THEOREMS)==20
    assert len(r['gates'])==len(GATES)==27
    assert all(r['exact']['checks'].values())
    assert all(r['gates'].values())

# Total = 20 + 27 + 3*8 + 5 = 76 tests.
