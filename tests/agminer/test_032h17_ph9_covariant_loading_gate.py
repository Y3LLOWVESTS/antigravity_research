"""PH9 exact gauge and frozen-amplitude Maxwell closure, fail-closed tests."""
from dataclasses import replace
from pathlib import Path
import numpy as np
import pytest
from antigravity_research.agminer import hook17_ph8_finite_scalar_source_gate as ph8
from antigravity_research.agminer import hook17_ph9_covariant_loading_gate as ph9

@pytest.fixture(scope='module')
def data(tmp_path_factory):
    return ph9.run(tmp_path_factory.mktemp('ph9_no_archive'))


def test_action_derived_charge_current_signs():
    t=ph9.exact_minimal_coupling_controls()
    assert t['electric_current_from_action']=='PASS_EXACT'
    assert t['azimuthal_current_from_action']=='PASS_EXACT'


def test_explicit_y_current_matches_ph8_shape():
    s=ph8.Spec(n=48)
    a=ph8.signed_sources(s)
    x,y,z=a['x'],a['y'],a['z']
    ring=np.maximum(1-(x*x+y*y+z*z)/s.magnetic_radius**2,0.)**(2*s.envelope_power)
    amp=a['vortex_amplitude_squared']
    # Two scalar species have |q|=|n|=1, opposite charges and winding.
    j=np.array([-4*amp*y*ring/s.magnetic_radius**2,
                 4*amp*x*ring/s.magnetic_radius**2,np.zeros_like(x)])
    assert np.max(abs(j-a['j_y']))<1e-12


def test_canonical_current_normalization_is_matter_density_not_coupling():
    s=ph8.Spec(n=48)
    a=ph8.signed_sources(s)
    xp,xm,yp,ym=ph9.scalar_amplitudes(a,s)
    vol=a['vol']
    assert np.sum(2*s.omega*xp)*vol==pytest.approx(s.charge)
    assert np.sum(2*s.omega*xm)*vol==pytest.approx(s.charge)
    assert np.sum(2*s.omega*abs(yp)**2)*vol==pytest.approx(s.magnetic_species_charge)
    assert np.sum(2*s.omega*abs(ym)**2)*vol==pytest.approx(s.magnetic_species_charge)


def test_loaded_maxwell_gauss_and_ampere(data):
    p=data['primary']
    assert p['max_gauss_error']<1e-4
    assert p['relative_ampere_error']<5e-5
    assert p['relative_current_divergence']<5e-4
    assert p['relative_vector_potential_divergence']<2e-6


def test_charge_conservation_and_chirality(data):
    p=data['primary']
    assert abs(p['source_total_charge_loaded'])<1e-10
    assert p['loaded_metric_accel_shape']>0
    assert p['earthward_axis_accel_z_shape']<0
    assert data['chirality_reversal_control']['metric_accel_shape']<0


def test_ph8_first_iteration_exact_reproduction(data):
    reference=ph8.fourier_fields(ph8.Spec(n=96))
    p=data['primary']
    assert p['first_iteration_P_probe']==pytest.approx(reference['P_at_probe'],abs=1e-12)
    assert p['first_iteration_metric_accel_shape']==pytest.approx(
        reference['neutral_acceleration_over_c_squared_shape'],abs=1e-12)


def test_source_self_loading_is_not_silently_ignored(data):
    p=data['primary']
    assert p['relative_gauge_rho_self_loading']>.1
    assert p['relative_gauge_J_self_loading']>.02
    assert 0<p['ratio_loaded_to_first_iteration_P']<1


def test_complete_scalar_gradient_energy_is_explicit(data):
    e=data['primary']['canonical_energy']
    assert e['matter_spatial']>e['matter_rest']
    assert e['matter_time']>0
    assert e['field_EB']>0
    assert e['electric_E']+e['magnetic_B']==pytest.approx(e['field_EB'])
    assert e['field_plus_matter_excluding_support']==pytest.approx(
        sum(e[k] for k in ('matter_spatial','matter_time','matter_rest','field_EB')))


def test_scalar_EOM_remains_off_shell(data):
    assert data['primary']['electric_scalar_KG_EOM_residual_L2_per_field_L2']>1
    assert data['gates']['P1_CHARGED_SCALAR_ON_SHELL']=='RED_NONZERO_KG_EOM_RESIDUAL'
    assert data['gates']['P1_COMPLETE_SOURCE_SUPPORT']=='NOT_DERIVED'


def test_domain_screen_at_common_dx(data):
    a=data['primary'];b=data['larger_domain_same_dx']
    assert a['spec']['length']/a['spec']['n']==pytest.approx(
        b['spec']['length']/b['spec']['n'])
    ratio=abs(a['loaded_metric_accel_shape']-b['loaded_metric_accel_shape'])/abs(b['loaded_metric_accel_shape'])
    assert ratio < .1


def test_coarse_grid_residual_demoted(data):
    assert data['primary']['max_gauss_error']<.1*data['coarse_grid_error_control']['max_gauss_error']


def test_off_control_and_no_craft_promotion(data):
    assert data['portal_off_control']['metric_accel_shape']==0
    assert data['gates']['P3_EARTH_DOWN_FULL_CRAFT_UP']=='NOT_DERIVED'
    assert data['gates']['006D_REPLACED']=='NO'


def test_missing_history_unresolved(data):
    assert data['gates']['P0_PROVENANCE']=='UNRESOLVED'


def test_history_mismatch_blocks_promotion(tmp_path):
    f=tmp_path/'src/antigravity_research/agminer/hook17_ph8_finite_scalar_source_gate.py'
    f.parent.mkdir(parents=True)
    f.write_text('wrong')
    assert ph9.archival(tmp_path)['ph8_source']['status']=='HASH_MISMATCH'


def test_solver_rejects_invalid_screen():
    with pytest.raises(ValueError):
        ph9.screened_poisson(np.ones((2,2,2)),np.zeros((2,2,2)),np.ones((2,2,2)))


def test_chirality_validates_input():
    with pytest.raises(ValueError):
        ph9.solve(ph8.Spec(n=48),orientation=0)
