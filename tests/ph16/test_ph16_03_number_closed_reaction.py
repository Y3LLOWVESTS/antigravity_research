"""PH16-03 reduced Routhian, Noether, neutral number, FD and anti-promotion tests."""
from functools import lru_cache
import numpy as np
import pytest
from antigravity_research.ph16.ph16_03_number_closed_reaction import (
    report,exact_atlas,NumberClosedY,Settings,
)
from antigravity_research.agminer.hook17_ph15_p10_free_space import CoulombSource,Spec

@lru_cache(maxsize=1)
def R():return report()

EXACT=(
 'sigma_prime','source_Noether_stationarity','source_X_current_conjugate',
 'matter_portal_lambda','matter_portal_chi','neutral_pullback_number_weight',
 'hydrostatic_mu','fluid_trace','schur_frequency_stiffening',
 'no_portal_alpha_beta_zero',
)
GATES=(
 'three_P10_sources','P10_source_initial_on_shell',
 'Y_omega_stationary','Y_omega_reduced_Hessian_positive',
 'source_individual_Noether_reclosed','old_P10_omega_fails_Noether',
 'Routhian_gradient_independent_FD','Routhian_Hessian_independent_FD',
 'neutral_material_number_preserved','neutral_chemical_hydrostatic',
 'fluid_positive','outer_neutral_converged',
 'frozen_source_EOM_defect_reported','X_mixed_grid_defect_reported',
 'frozen_gauge_beta40_positive','no_false_full_source_solve',
 'no_false_metric_solve','no_false_earth_force',
)
CASES=('12_L12','18_L12','12_L16')

@pytest.mark.parametrize('name',EXACT)
def test_01_action_exact(name):assert exact_atlas()[name]

@pytest.mark.parametrize('name',GATES)
def test_02_scoped_research_gate(name):assert R()['gates'][name]

@pytest.mark.parametrize('case',CASES)
def test_03_noether_both_charged_species(case):
    c=R()['cases'][case]
    assert len(c['inner']['Noether'])==2
    np.testing.assert_allclose(c['inner']['Noether'],[400.,400.],atol=1e-9)
    assert c['source_N_residual_max']<1e-9
    assert c['frozen_P10_omega_Noether_defect_abs']>1e-4

@pytest.mark.parametrize('case',CASES)
def test_04_neutral_material_number(case):
    c=R()['cases'][case]
    assert c['neutral_number_residual']<1e-8
    assert c['neutral_labels_positive']

@pytest.mark.parametrize('case',CASES)
def test_05_neutral_equilibrium_and_outer_iteration(case):
    c=R()['cases'][case]
    assert c['neutral_mu_redshift_range']<1e-9
    assert c['neutral_outer_updates'][-1]<1e-9

@pytest.mark.parametrize('case',CASES)
def test_06_reduced_Y_stationarity(case):
    c=R()['cases'][case]
    assert c['inner']['residual_L2']<1e-8
    assert c['inner']['Hessian_min']>0

@pytest.mark.parametrize('case',CASES)
def test_07_independent_Routhian_FD(case):
    c=R()['cases'][case]
    assert c['Routhian_directional_gradient_fd_abs']<2e-6
    assert c['Routhian_Hessian_vector_fd_L2']<2e-6

@pytest.mark.parametrize('case',CASES)
def test_08_offshell_F_X_are_reported(case):
    c=R()['cases'][case]
    assert max(c['source_frozen_EOM_diagnostic_weighted_L2'])>1e-7
    assert c['X_mixed_discretization_kernel_defect_inf']>1e-8
    assert c['full_source_X_EOM']=='NOT_SOLVED'

@pytest.mark.parametrize('case',CASES)
def test_09_portal_gauge_margin_not_full_stability(case):
    c=R()['cases'][case]
    assert c['magnetic_margin_beta40_min']>0
    assert c['magnetic_negative_cell_count']==0
    assert c['metric_Einstein_EOM']=='NOT_SOLVED'

@pytest.mark.parametrize('case',CASES)
def test_10_canonical_not_physical(case):
    c=R()['cases'][case]
    assert c['real_Earth_and_full_craft']=='NOT_DERIVED'
    assert c['SI_complete_energy']=='NOT_CERTIFIED'


def test_11_no_portal_zero_Y_stationarity():
    m=CoulombSource(Spec(nr=12,L=12.),self_order=8)
    _,f=m.solve(350)
    o=NumberClosedY(m,f,Settings(alpha=0.,beta=0.),np.full(m.cells,.15))
    g,H,R,N=o.evaluate(np.zeros(m.cells))
    assert np.max(abs(g))<1e-12
    np.testing.assert_allclose(N,[400.,400.],atol=1e-10)


def test_12_all_counts():
    assert len(EXACT)==10 and len(GATES)==18
    assert len(R()['cases'])==3
    assert all(R()['exact'].values()) and all(R()['gates'].values())
    assert R()['full_joint_on_shell']=='NOT_SOLVED'

# 10 exact + 18 scoped + 8 x 3 cases + 2 controls = 54 focused tests.
