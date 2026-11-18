"""BETA1-04 independent force, stress and momentum ledger regression."""
from __future__ import annotations
from dataclasses import replace
from functools import lru_cache
import numpy as np
import pytest
from antigravity_research.beta_artificial.beta1_04_external_ledger import (
    Settings,CoupledToy,exact_theorems,static_on_shell_total,action_gradient_audit,report
)

@lru_cache(maxsize=1)
def R():return report()

@pytest.mark.parametrize('check',[
    'earth_craft_action_reciprocity','internal_support_force_pair','translation_invariance_U',
    'source_shape_singlebody_translation_invariant','static_stress_matter_exchange',
    'Noether_momentum_partition','on_shell_Hellmann_Feynman','source_off_interaction',
    'earth_absent_interaction','equal_opposite_charge_repulsion_condition',
    'double_charge_quadratic_force','static_field_off_complete',
])
def test_01_symbolic_conservation(check):
    assert exact_theorems()[check]

@pytest.mark.parametrize('gate',[
    'exact_Noether_stress_theorems','repulsive_opposite_scalar_charge_toy',
    'closed_static_body_reaction','analytic_kernel_matches_density_force',
    'stress_flux_matches_region_force','stress_flux_matches_Earth_body_force',
    'local_stress_divergence_Ward','same_action_coordinate_derivative',
    'action_earth_craft_force_pair','source_only_translates_not_whole_craft_offset',
    'offset_source_hull_support_reaction','offset_whole_craft_force_exterior_only',
    'common_translation_invariant','static_common_force_zero',
    'Earth_absent_zero_interaction','source_off_zero_interaction',
    'same_sign_attractive_control','double_q_scaling_fourfold',
    'grid_static_convergence','periodic_box_sensitivity_control',
    'grid_traction_all','local_stress_Ward_refines','box64_stress_Ward_resolved',
    'dynamic_left_region_stress_flux_Ward','field_kinetic_and_mass_positive',
    'dynamic_energy_law','dynamic_momentum_law',
    'dynamic_earth_impulse_equals_deltaP','dynamic_craft_impulse_equals_deltaP',
    'dynamic_field_carries_difference','dynamic_spring_internal_cancellation',
    'dynamic_signed_impulse_accounted','dynamic_temporal_refinement_energy',
    'dynamic_temporal_refinement_impulse','dynamic_source_off_no_craft_force',
    'dynamic_earth_absent_no_unforced_craft_force',
    'internal_excitation_no_ex_nihilo_momentum','internal_excitation_no_energy_reset',
    'finite_box_not_called_true_exterior',
    'toy_scalar_charges_not_called_neutral_metric_matter',
    'M5V_residual_not_called_reaction_certification',
    'full_P10_PDE_and_Earth_force_not_certified','no_SI_energy_certification',
])
def test_02_all_scoped_gates(gate):assert R()['gates'][gate]

@pytest.mark.parametrize('name',('earth_absent','source_off'))
def test_03_independent_zero_cross_energy(name):
    m=CoupledToy(replace(Settings(),q_earth=0.) if name=='earth_absent' else replace(Settings(),q_source=0.))
    assert abs(m.derivative_source_energy(m.X0))<1e-14
    np.testing.assert_allclose(m.statics()['force'],[0,0],atol=1e-9)

@pytest.mark.parametrize('shift',(-4.,-1.,0.,1.,5.))
def test_04_full_translation_not_force(shift):
    m=CoupledToy()
    np.testing.assert_allclose(static_on_shell_total(m,m.X0+shift),static_on_shell_total(m,m.X0),atol=1e-10)

@pytest.mark.parametrize('n',(128,256,512))
def test_05_grid_force_vs_exact_pair(n):
    m=CoupledToy(replace(Settings(),n=n))
    s=m.statics()
    np.testing.assert_allclose(s['force'],s['analytic_force'],atol=1e-8)
    assert abs(s['force'].sum())<1e-10

@pytest.mark.parametrize('offset',(0.,.2,.4))
def test_06_hull_source_support_cancellation(offset):
    m=CoupledToy();X=m.X0.copy();X[2]-=offset
    a=action_gradient_audit(m,X)
    assert abs(a['earth_craft_force_sum'])<1e-8
    assert abs(a['hull_force']-m.s.spring*offset)<1e-7
    assert abs(a['whole_craft_force']-m.statics(X)['force'][1])<1e-7

def test_07_field_momentum_not_ignored():
    d=R()['dynamics']['earth_present']
    assert d['field_momentum_change']>.01
    assert abs(d['craft_momentum_change']+d['earth_momentum_change'])>.01
    assert abs(d['craft_momentum_change']+d['earth_momentum_change']+d['field_momentum_change'])<1e-8

def test_08_no_free_craft_impulse_without_Earth_and_actuation():
    d=R()['dynamics']['earth_absent']
    assert abs(d['craft_momentum_change'])<1e-8
    assert abs(d['field_momentum_change'])<1e-8

def test_09_internal_spring_momentum_to_field_not_thrust():
    d=R()['dynamics']['earth_absent_internal_spring_excitation']
    assert abs(d['craft_momentum_change'])>.02
    assert abs(d['craft_momentum_change']+d['field_momentum_change'])<1e-8
    assert d['time_history_not_reset']

def test_10_guardrails_preserve_missing_real_physics():
    r=R()
    assert r['promotion']=='NOT_AUTHORIZED'
    assert r['status'].startswith('YELLOW_')
    assert 'ordinary neutral universal-metric gravity not established' in '; '.join(r['limits'])
    assert 'PERIODIC domain' in '; '.join(r['limits'])
    assert 'not SI force/energy' in '; '.join(r['limits'])

def test_11_count_and_ledger():
    r=R()
    assert len(r['symbolic'])==12 and len(r['gates'])==43
    assert all(r['symbolic'].values()) and all(r['gates'].values())
    assert len(r['dynamics'])==5

# Total = 12 + 43 + 2 + 5 + 3 + 3 + 5 = 73 tests
