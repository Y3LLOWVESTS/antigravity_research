"""PH8 independently checking finite 3D scalar sources and fail-closed physics."""
from dataclasses import replace
from pathlib import Path
import math
import numpy as np
import pytest
from antigravity_research.agminer import hook17_ph8_finite_scalar_source_gate as ph8

@pytest.fixture(scope='module')
def primary(): return ph8.fourier_fields(ph8.Spec())

@pytest.fixture(scope='module')
def main_results(): return ph8.run(Path('.'))

def test_exact_compact_kg_and_ward_theorems():
    t=ph8.theorem_controls()
    assert t['compact_linear_KG_bounded_trap']=='FAIL_FOR_THIS_PROFILE'
    assert t['charged_scalar_N0_phase_current']=='PASS_EXACT'
    assert t['gauge_Ward_local_off_shell_identity']=='PASS_EXACT_1D_PHASE_WITH_GAUGE_POTENTIAL'
    assert t['Weyl_weight_of_P']==-4

def test_bounded_quadratic_trap_fails_for_compact_scalar():
    import sympy as sp
    r,R,k=sp.symbols('r R k',positive=True)
    f=(1-r*r/R**2)**k
    lap=sp.diff(f,r,2)+2*sp.diff(f,r)/r
    ratio=sp.simplify(lap/f)
    pole=sp.limit(ratio*(1-r*r/R**2)**2,r,R,dir='-')
    assert sp.simplify(pole-4*k*(k-1)/R**2)==0
    assert pole.subs({R:1,k:4})>0

def test_source_species_global_charge_neutrality():
    src=ph8.signed_sources(ph8.Spec())
    vol=src['vol']
    assert vol*np.sum(src['rho_x_plus'])==pytest.approx(1,abs=1e-14)
    assert vol*np.sum(src['rho_x_minus'])==pytest.approx(-1,abs=1e-14)
    assert np.max(abs(src['rho_y']))==0
    assert abs(vol*np.sum(src['rho_x']))<1e-13

def test_compact_source_true_support_geometry():
    s=ph8.Spec();src=ph8.signed_sources(s)
    x,y,z=src['x'],src['y'],src['z']
    outside_x=((x*x+y*y+(z-s.electric_offset)**2>s.electric_radius**2)
               & (x*x+y*y+(z+s.electric_offset)**2>s.electric_radius**2))
    outside_y=(x*x+y*y+z*z>s.magnetic_radius**2)
    assert np.max(abs(src['rho_x'][outside_x]))==0
    assert np.max(abs(src['j_y'][:,outside_y]))==0
    assert src['support_extent']==pytest.approx(1.55)
    assert s.probe_z-src['support_extent']>=1.0

def test_azimuthal_current_is_analytic_solenoidal():
    # For J=C f(r)(-y,x,0), div J = C(-y f_x + x f_y)=0.
    import sympy as sp
    x,y,z,R,k,C=sp.symbols('x y z R k C',real=True)
    profile=(1-(x*x+y*y+z*z)/R**2)**(2*k)
    divergence=sp.diff(-C*y*profile,x)+sp.diff(C*x*profile,y)
    assert sp.simplify(divergence)==0

def test_canonical_finite_static_fields(primary):
    assert primary['electric_energy_canonical']>0
    assert primary['magnetic_energy_canonical']>0
    assert primary['unloaded_scalar_time_plus_rest_energy_canonical']>primary['field_energy_canonical']
    assert math.isfinite(primary['field_energy_canonical'])

def test_static_maxwell_gauss_and_bianchi_screen(primary):
    assert primary['max_abs_Gauss_X_residual']<1e-4
    assert primary['max_abs_divergence_BY_residual']<1e-10
    assert primary['max_abs_divergence_JY_sampled']<5e-4

def test_nyquist_and_source_current_resolution_improves(primary):
    coarse=ph8.fourier_fields(replace(ph8.Spec(),n=64))
    assert primary['max_abs_Gauss_X_residual']<.1*coarse['max_abs_Gauss_X_residual']
    assert primary['max_abs_divergence_JY_sampled']<.2*coarse['max_abs_divergence_JY_sampled']

def test_topological_mixed_P_signed_integral_zero(primary):
    assert abs(primary['volume_integral_P'])<1e-10
    assert primary['volume_integral_abs_P']>1e-5
    assert primary['P_at_probe']>0

def test_exterior_signed_matter_force_both_sides(primary):
    assert primary['probe_clearance']>1
    assert primary['neutral_acceleration_over_c_squared_shape']>0
    assert primary['a_earthward_z_shape']<0
    assert primary['P_at_earthward_axis_probe']==pytest.approx(primary['P_at_probe'],rel=1e-8)

def test_finite_difference_independent_metric_force(primary):
    assert primary['neutral_acceleration_over_c_squared_shape']==pytest.approx(
        primary['a_over_c2_independent_sigma_difference'],abs=1e-9)

def test_no_portal_zero_metric_response():
    s=replace(ph8.Spec(),alpha=0.,beta=0.)
    p=ph8.fourier_fields(s)
    assert p['neutral_acceleration_over_c_squared_shape']==0
    assert p['field_energy_canonical']>0

def test_even_negative_quadratic_local_sign_reversed():
    s=replace(ph8.Spec(),alpha=0.,beta=.4)
    p=ph8.fourier_fields(s)
    assert p['neutral_acceleration_over_c_squared_shape']<0

def test_chirality_flip_reverses_mixed_invariant():
    pos=ph8.fourier_fields(ph8.Spec(),chirality=1)
    neg=ph8.fourier_fields(ph8.Spec(),chirality=-1)
    assert neg['P_at_probe']==-pos['P_at_probe']
    assert neg['dP_dz_at_probe']==-pos['dP_dz_at_probe']
    assert neg['neutral_acceleration_over_c_squared_shape']<0
    assert neg['field_energy_canonical']==pytest.approx(pos['field_energy_canonical'])

def test_finite_domain_box_screen(main_results):
    assert main_results['domain_relative_P_difference']<.05
    assert main_results['domain_relative_force_difference']<.05

def test_source_eom_not_promoted_despite_current_conservation(primary):
    assert primary['charged_scalar_covariant_rho_loading_relative_L2']>.01
    assert primary['charged_scalar_covariant_J_loading_relative_L2']>.01
    assert primary['full_charged_scalar_EOM']=='NOT_SOLVED'
    assert primary['full_portal_backreaction']=='NOT_SOLVED'

def test_support_stresses_fail_closed(primary):
    assert primary['X_positive_cloud_internal_support_Fz']<0
    assert primary['Y_magnetic_local_hoop_stress_L1']>0
    assert primary['X_positive_cloud_internal_support_Fz'] !=0

def test_two_U1_momentum_not_cross_poynting(primary):
    assert primary['two_carrier_maxwell_field_momentum']==0

def test_reaction_not_whole_craft_force(main_results):
    r=main_results['reaction_diagnostic']
    assert r['earthward_probe_force_z_shape']<0
    assert r['craftward_reaction_z_if_earth_is_external']>0
    assert r['earth_source_metric_response']=='NOT_DERIVED'
    assert r['whole_craft_force_for_both_onboard_in_static_reduced_potential']==0

def test_missing_history_fails_closed(tmp_path):
    x=ph8.run(tmp_path)
    assert x['gates']['P0_PROVENANCE']=='UNRESOLVED'
    assert x['gates']['P1_CHARGED_SCALAR_ON_SHELL']=='RED_NOT_SATISFIED'
    assert x['gates']['P3_EARTH_DOWN_WHOLE_CRAFT_UP']=='NOT_DERIVED'
    assert x['gates']['STRICT_COMPLETE_LT10MJ']=='NOT_CERTIFIED'
    assert x['gates']['006D_REPLACED']=='NO'

def test_bad_history_hash_fails_closed(tmp_path):
    f=tmp_path/'results/data/032h17_ph7_noether_spectral_health_20261115T023628445509Z.json'
    f.parent.mkdir(parents=True)
    f.write_text('not PH7')
    assert ph8.provenance(tmp_path)['ph7_result']['status']=='HASH_MISMATCH'

@pytest.mark.parametrize('changes',[
    {'n':47},{'envelope_power':2},{'charge':-1},
    {'probe_z':2.0},{'probe_z':8.0},{'length':0.},
    {'alpha':-1},{'omega':float('nan')},
])
def test_bad_geometries_rejected(changes):
    with pytest.raises(ValueError):ph8.signed_sources(replace(ph8.Spec(),**changes))

@pytest.mark.parametrize('chirality',[0,2,-2])
def test_only_physical_chirality_controls(chirality):
    with pytest.raises(ValueError):ph8.fourier_fields(ph8.Spec(),chirality=chirality)
