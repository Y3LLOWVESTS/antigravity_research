"""PH10 focused exact mode, loading, exterior and fail-closed tests."""
from dataclasses import replace
from pathlib import Path
import numpy as np
import pytest
from antigravity_research.agminer import hook17_ph10_bounded_well_source_gate as p

@pytest.fixture(scope='module')
def data(tmp_path_factory):
    return p.run(tmp_path_factory.mktemp('ph10_archive_absent'))

@pytest.mark.parametrize('l',[0,1])
def test_finite_bound_mode_positive_quadratic_mass(l):
    m=p.radial_mode(l,1.,5.,4.)
    assert m['depth']>0
    assert m['minimum_quadratic_mass_squared']>0
    assert abs(m['boundary_slope_jump'])<1e-10
    assert abs(m['match_residual'])<1e-10

@pytest.mark.parametrize('l',[0,1])
def test_radial_ODE_in_both_regions(l):
    m=p.radial_mode(l,1.,5.,4.)
    residual=p.mode_radial_residual(m,np.array([.22,.55,.82,1.27,1.7]))
    assert np.max(abs(residual))<2e-6

def test_independent_continuum_weak_variational_identity(data):
    for mode in data['primary']['independent_continuum_radial_virial']:
        assert mode['relative_variational_residual']<1e-10
        assert 0<mode['fraction_outside_well']<1
        assert mode['fraction_beyond_probe_from_its_center']>0

def test_on_shell_zero_gauge_vs_loaded_source_EOM(data):
    p0=data['primary']
    assert p0['scalar_KG_residual_from_loaded_X']>.01
    assert p0['scalar_KG_residual_from_loaded_Y_exact_gauge_correction']>.01
    assert data['gates']['P1_GAUGE_LOADED_CHARGED_SCALAR_EOM']=='RED_RESIDUAL_NONZERO'

def test_exact_N0_source_neutrality_and_independent_current():
    src=p.normalized_fields(p.Spec())
    assert abs(src['charge_x'])<1e-10
    assert src['charge_y']==0
    assert np.any(src['j0'][0]!=0)
    assert np.any(src['j0'][1]!=0)

def test_gauss_and_current_residual_are_not_hidden(data):
    a=data['primary']
    assert 0<a['max_gauss_residual']<.001
    assert 0<a['relative_current_divergence']<.1
    assert a['CG_phi']['relative_equation_residual']<1e-8
    assert all(s['relative_equation_residual']<1e-8 for s in a['CG_vector'])

def test_sign_controls_and_portal_off(data):
    assert data['primary']['upper_probe']['acceleration_shape']>0
    assert data['primary']['lower_probe']['acceleration_shape']<0
    assert data['portal_off']['upper_probe']['acceleration_shape']==0
    assert data['chirality_reversal']['upper_probe']['P']==pytest.approx(-data['primary']['upper_probe']['P'],abs=1e-13)

def test_domain_screen_and_no_true_source_vacuum(data):
    assert data['domain_P_relative_difference']<.15
    assert data['primary']['probe_geometric_clearance']>=1
    assert data['gates']['P2_REAL_3D_SOURCE_COMPACT']=='NO_EXPONENTIAL_TAILS'

def test_canonical_energy_scope(data):
    v=data['primary']['partial_energy']
    assert all(np.isfinite(z) for z in v.values())
    assert v['field']>0 and v['matter_gradient']>0
    assert v['sum_excluding_trap_hardware']==pytest.approx(sum(
        v[k] for k in ('field','matter_gradient','matter_time','matter_rest_plus_prescribed_trap')))
    assert data['gates']['STRICT_FULL_ENERGY_LT10MJ']=='NOT_CERTIFIED'

def test_no_engine_promotion(data):
    g=data['gates']
    assert g['P3_EARTH_DOWN_CRAFT_UP']=='NOT_DERIVED'
    assert g['P3_UNIVERSAL_METRIC_AND_GRAVITY']=='NOT_DERIVED'
    assert g['006D_REPLACED']=='NO'
    assert g['P1_BOUNDED_TRAP_STRESS_ENERGY']=='NOT_DERIVED'

def test_invalid_masses_and_probe():
    with pytest.raises(ValueError):p.normalized_fields(replace(p.Spec(),omega=5.))
    with pytest.raises(ValueError):p.normalized_fields(replace(p.Spec(),n=53))
    with pytest.raises(ValueError):p.normalized_fields(replace(p.Spec(),probe_z=2.))
    with pytest.raises(ValueError):p.radial_mode(2,1.,5.,4.)

def test_chirality_rejected():
    with pytest.raises(ValueError):p.solve(p.Spec(),orientation=0)

def test_missing_archive_blocks_provenance(data):
    assert data['gates']['P0_PROVENANCE']=='UNRESOLVED'

def test_altered_archive_fails_closed(tmp_path):
    f=tmp_path/'src/antigravity_research/agminer/hook17_ph9_covariant_loading_gate.py'
    f.parent.mkdir(parents=True)
    f.write_text('altered PH9')
    assert p.provenance(tmp_path)['ph9_source']['status']=='HASH_MISMATCH'
