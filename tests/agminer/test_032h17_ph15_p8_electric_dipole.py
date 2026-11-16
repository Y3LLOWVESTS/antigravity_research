"""PH15-P8 exact, variational, zero-channel and finite-domain tests."""
import numpy as np
import pytest

from antigravity_research.agminer.hook17_ph15_p8_electric_dipole import (
    Dipole, Spec, theorem_checks, one_charged_soliton_reference
)


@pytest.fixture(scope='module')
def base():
    model=Dipole(Spec(nr=18))
    result,fields=model.solve(400)
    return model,result,fields


def test_fixed_charge_energy_gradient_independently_by_FD():
    model=Dipole(Spec(nr=10,L=10,N=180.))
    x=(model.seed(2.)*np.sqrt(model.w)).ravel()
    E,g=model.energy(x)
    assert np.isfinite(E)
    for i in (7,51,195,301):
        h=2e-5
        xp=x.copy();xm=x.copy()
        xp[i]+=h;xm[i]-=h
        fd=(model.energy(xp)[0]-model.energy(xm)[0])/(2*h)
        assert abs(fd-g[i])<1e-5


def test_neutral_nonspherical_stationary_X_source(base):
    model,r,fd=base
    assert abs(r['net_X_charge'])<1e-10
    assert np.max(abs(np.array(r['individual_Noether'])-model.s.N))<1e-9
    assert r['gauss_L2']<1e-10
    assert max(r['scalar_EOM_weighted_L2'])<1e-4
    assert r['optimizer']['gradient_inf']<1e-5
    assert 3.4<r['source_separation']<3.85
    assert r['charge_density_L2']>1
    assert r['symmetric_parity_max']<1e-5


def test_distinct_seed_converges_to_same_energy_and_separation(base):
    model,r,_=base
    alt=Dipole(Spec(nr=18,seed_separation=.5))
    b,_=alt.solve(400)
    assert abs(b['energy_CANONICAL_NOT_J']-r['energy_CANONICAL_NOT_J'])<1e-5
    assert abs(b['source_separation']-r['source_separation'])<1e-3


def test_first_order_Y_from_on_shell_X_nonzero(base):
    m,r,fd=base
    y=m.y_response(fd)
    assert y['Y_current_L2']>.30
    assert y['Y_magnetic_energy_CANONICAL']>.20
    assert y['Y_magnetic_dipole']>20
    assert y['P_absolute_integral']>1
    assert y['P_outer_shell_max_abs']>1e-6
    assert y['leading_axis_dipole_product_XY']>0
    assert y['Y_reciprocal_loading']=='NOT_SOLVED'


def test_alpha_sign_and_zero_controls(base):
    m,r,fd=base
    p=m.y_response(fd,alpha=1)
    n=m.y_response(fd,alpha=-1)
    z=m.y_response(fd,alpha=0)
    assert z['Y_current_L2']<1e-15
    assert z['Y_magnetic_energy_CANONICAL']<1e-15
    assert z['P_absolute_integral']<1e-15
    assert np.isclose(n['Y_current_L2'],p['Y_current_L2'],rtol=1e-10)
    assert np.isclose(n['Y_magnetic_dipole'],-p['Y_magnetic_dipole'],rtol=1e-10)
    assert np.isclose(n['P_signed_integral'],-p['P_signed_integral'],atol=1e-9)
    assert np.isclose(n['portal_sigma_max_abs_beta0'],p['portal_sigma_max_abs_beta0'],rtol=1e-10)


def test_no_interspecies_repulsion_collapses_dipole():
    m=Dipole(Spec(g=0.))
    r,fd=m.solve(400)
    y=m.y_response(fd)
    assert abs(r['source_separation'])<.005
    assert y['Y_current_L2']<1e-6


def test_stronger_electric_attraction_collapses_dipole():
    m=Dipole(Spec(e=.14))
    r,fd=m.solve(400)
    y=m.y_response(fd)
    assert abs(r['source_separation'])<.005
    assert y['Y_current_L2']<1e-6


def test_restricted_relative_axial_energy_direction_not_full_stability(base):
    m,r,fd=base
    ax=m.axial_trial(fd)
    assert ax['relative']['delta_energy_minus']>0
    assert ax['relative']['delta_energy_plus']>0
    assert ax['common']['symmetric_curvature_proxy']>0


def test_fine_grid_and_larger_box_are_separately_reported():
    m=Dipole(Spec(nr=24,L=16))
    r,fd=m.solve(400)
    y=m.y_response(fd)
    assert r['source_separation']>2.0
    assert r['source_separation']<3.5
    assert r['outer_80percent_spherical_tail_fraction']<.002
    assert y['Y_current_L2']>.25


def test_gradient_sign_control_without_repulsion_needs_new_physics(base):
    m,r,fd=base
    assert m.s.g>.0
    assert abs(r['electric_dipole_X'])>100
    assert abs(r['net_X_charge'])<1e-10
    assert r['domain']=='FINITE_CYLINDRICAL_DIRICHLET'


def test_new_contact_same_action_and_portal_trace():
    t=theorem_checks()
    assert t['source_contact_variation']=='PASS_EXACT_BOTH_SPECIES'
    assert 'dg=' in t['contact_portal_derivative']
    assert t['full_metric_stress']=='NOT_DERIVED'


def test_restricted_angular_gauss_matched_density_positive_only(base):
    m,r,fd=base
    modes=m.angular_gauss_matched_screen(fd)
    assert modes['k1']['minimum_generalized_energy_eigen']>0
    assert modes['k2']['minimum_generalized_energy_eigen']>0
    assert modes['k1']['full_stability']=='NOT_CERTIFIED'


def test_matched_independent_soliton_reference_is_conditional(base):
    m,r,f=base
    ref=one_charged_soliton_reference(m.s)
    assert ref['two_separate_reference_energy_CANONICAL_NOT_J']>r['energy_CANONICAL_NOT_J']
    assert ref['gradient_inf']<1e-5
    assert ref['not_global_binding_proof'] is True
