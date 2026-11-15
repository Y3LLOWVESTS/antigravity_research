"""PH14: independent neutral on-shell scalar-Maxwell source and fail-closed gates."""
from dataclasses import replace
from pathlib import Path
import math
import numpy as np
import pytest
from antigravity_research.agminer import hook17_ph14_neutral_composite as p


@pytest.fixture(scope='module')
def report(tmp_path_factory):
    return p.run(tmp_path_factory.mktemp('ph14_no_archives'))


@pytest.fixture(scope='module')
def source(report):
    return report['on_shell_neutral_source']


def test_shared_two_species_source_action_current_exact(report):
    assert report['exact_action']['canonical_two_scalar_current']=='PASS_EXACT'


def test_two_species_radial_onshell_equations_exact(report):
    assert report['exact_action']['two_radial_Euler_Lagrange']=='PASS_EXACT'


def test_phase_gauge_covariance_exact(report):
    assert report['exact_action']['local_gauge_covariance']=='PASS_EXACT'


def test_positive_bounded_phi6_potential(report):
    assert report['exact_action']['positive_phi6_potential']=='PASS_EXACT'


def test_nonlinear_stationary_two_species_BVP(source):
    assert source['BVP_status']=='SOLVED'
    assert source['BVP_collocation_rms']<2.e-8
    assert 0<source['omega_plus']<1
    assert 0<source['omega_minus']<1.08


def test_both_scalar_amplitudes_solved(source):
    assert source['f_plus_center']==pytest.approx(.7,abs=1e-10)
    assert .65<source['f_minus_center']<.70
    assert source['f_minus_center']!=pytest.approx(.7,abs=1e-3)


def test_both_scalar_tails_decay(source):
    assert 0<source['tail_plus_relative']<1e-7
    assert 0<source['tail_minus_relative']<1e-7


def test_individual_noether_numbers_positive(source):
    assert source['Noether_plus']>70
    assert source['Noether_minus']>70


def test_net_charge_close_zero_and_gauss_flux(source):
    assert abs(source['integrated_net_gauge_charge'])<1e-9
    assert source['relative_charge_neutrality']<1e-9
    assert source['absolute_charge_vs_flux_error']<1e-9
    assert abs(source['boundary_Gauss_flux'])<1e-12


def test_local_X_electric_is_not_trivial(source):
    assert source['max_abs_radial_E']>5e-4
    assert source['electric_field_energy']>1e-6


def test_energy_ledger_is_positive(source):
    terms=source['canonical_energy_terms']
    assert terms['matter_time']>0
    assert terms['matter_gradient']>0
    assert terms['positive_scalar_potential']>0
    assert terms['electric_inside']>0
    assert source['total_field_plus_matter_energy']==pytest.approx(sum(terms.values()))


def test_energy_below_free_species_threshold(source):
    assert source['binding_below_free_quanta']>.5
    assert source['energy_over_free_mass']<1.


def test_independent_local_stress_conservation(source):
    assert source['local_radial_stress_divergence_max']<1e-10


def test_independent_integrated_stress_virial(source):
    assert source['stress_virial_relative_residual']<1e-9


def test_both_isolated_reference_lumps_are_fully_solved(report):
    isolated=report['separated_lumps_same_N_comparison']['isolated_by_species']
    assert 0<isolated['plus']['omega']<1.
    assert 0<isolated['minus']['omega']<1.08
    assert isolated['plus']['rms']<2e-8
    assert isolated['minus']['rms']<2e-8


def test_equal_individual_noether_numbers_in_separated_reference(report,source):
    isolated=report['separated_lumps_same_N_comparison']['isolated_by_species']
    assert isolated['plus']['N']==pytest.approx(source['Noether_plus'],abs=1e-7)
    assert isolated['minus']['N']==pytest.approx(source['Noether_minus'],abs=1e-7)


def test_joint_composite_below_separated_charged_Qballs(report):
    x=report['separated_lumps_same_N_comparison']
    assert x['joint_lower_than_separated']
    assert .3 < x['binding_vs_two_isolated'] < .5
    assert x['scope'].startswith('CLASSICAL_FIXED_INDIVIDUAL')


def test_mesh_refinement_energy_stable(report,source):
    assert report['high_resolution']['n']==880
    assert abs(report['high_resolution']['energy']-source['total_field_plus_matter_energy'])<1e-4


def test_domain_refinement_energy_stable(report,source):
    assert report['larger_radius']['R']==48
    assert abs(report['larger_radius']['energy']-source['total_field_plus_matter_energy'])<1e-4


def test_equal_species_analytic_null_controls(report):
    assert report['symmetric_mass_null']['max_abs_E']<1e-7
    assert report['asymmetric_control']['max_abs_E']>1e-6


def test_frozen_translation_positive_curvature_not_stability_proof(report):
    x=report['frozen_translation_only']
    assert x['small_relative_translation_curvature']>0
    assert 'NOT_FULL_SPECTRAL' in x['classification']


def test_trial_rigid_translation_energy_increases(report):
    values=report['frozen_translation_only']['frozen_pair_Coulomb_interaction']
    assert values['0.0']<values['0.25']<values['0.5']<values['1.0']<values['2.0']


def test_two_individual_noether_numbers_fixed_in_gauss_reload(report,source):
    r=report['restricted_fixed_two_charge_radial']['background_fv']
    assert r['Gauss_relative_residual']<1e-8
    assert r['Noether_plus']==pytest.approx(source['Noether_plus'],abs=1e-7)
    assert r['Noether_minus']==pytest.approx(source['Noether_minus'],abs=1e-7)


def test_restricted_hessian_is_explicitly_not_full_stability(report):
    x=report['restricted_fixed_two_charge_radial']
    assert x['modes']==12
    assert x['negative_eigenvalues']==0
    assert x['lowest_eigenvalue']>0
    assert x['classification'].endswith('NOT_DYNAMICAL_STABILITY')


def test_restricted_hessian_cross_grid(report):
    a=report['restricted_fixed_two_charge_radial']
    b=report['restricted_radial_resolution']
    assert b['n']==660
    assert b['negative_eigenvalues']==0
    assert abs(a['lowest_eigenvalue']-b['lowest_eigenvalue'])<.02


def test_on_shell_spherical_mixed_portal_is_zero(report):
    assert report['exact_action']['spherical_trace_induced_Y']=='ZERO_BY_ROTATIONAL_SYMMETRY'
    assert report['gates']['P2_ONSHELL_SPHERICAL_TRACE_INDUCED_Y']=='EXACT_ZERO_BY_SYMMETRY'


def test_no_false_carrier_or_craft_promotion(report):
    gates=report['gates']
    assert gates['P2_NONSYMMETRIC_FULL_ONSHELL_Y']=='NOT_DERIVED'
    assert gates['P3_EARTH_DOWN_CRAFT_UP']=='NOT_DERIVED'
    assert gates['006D_REPLACED']=='NO'


def test_no_SI_and_UV_promotion(report):
    assert report['on_shell_neutral_source']['SI_mass_energy']=='NOT_CALIBRATED'
    assert report['gates']['P1_REAL_PARTICLES_AND_QUANTUM_UV']=='NOT_CERTIFIED'
    assert report['gates']['STRICT_COMPLETE_LT10MJ']=='NOT_CERTIFIED'


def test_no_1g_1m_or_complete_cycle_promotion(report):
    assert report['gates']['P3_NEUTRAL_1G_1M']=='NOT_CERTIFIED'
    assert report['gates']['B11_M6_COMPLETE_CAUSAL_IMPULSE']=='NOT_RUN'


def test_history_absence_is_fail_closed(report):
    assert report['gates']['P0_PROVENANCE']=='UNRESOLVED'


def test_archive_tampering_detected(tmp_path):
    f=tmp_path/p.ARCHIVES['ph13_module'][0]
    f.parent.mkdir(parents=True)
    f.write_text('not the archived source')
    assert p.provenance(tmp_path)['ph13_module']['status']=='HASH_MISMATCH'


@pytest.mark.parametrize('change',[
    {'m_plus':0.0},{'m_minus':0.0},{'quartic':-1.},
    {'sextic':0.},{'e':-1.},{'plus_center':0.},
    {'radius':10.},{'n':47},{'n':181},{'tolerance':-1.},
    {'m_minus':float('nan')},{'quartic':8.},
])
def test_invalid_source_data_rejected(change):
    with pytest.raises(ValueError):p.solve_composite(replace(p.Spec(),**change))


def test_fixed_charge_invalid_Noether_target():
    s=p.Spec()
    with pytest.raises(ValueError):
        p.reduced_energy_fixed_numbers(s,np.ones(200),np.ones(200),-1,1)


def test_fixed_charge_invalid_amplitude_shape():
    s=p.Spec()
    with pytest.raises(ValueError):
        p.reduced_energy_fixed_numbers(s,np.ones(200),np.ones(10),1,1)


def test_invalid_hessian_grid():
    with pytest.raises(ValueError):p.fixed_charge_radial_subspace(n=12)


def test_invalid_hessian_step():
    with pytest.raises(ValueError):p.fixed_charge_radial_subspace(step=0.)
