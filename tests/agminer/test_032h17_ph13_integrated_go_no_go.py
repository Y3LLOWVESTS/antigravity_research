"""PH13-MEGA regression and negative-control tests.

All passes refer only to their explicitly scoped mathematical models.
No physical gravitational lift, stable device or energy is certified.
"""

from dataclasses import replace
from pathlib import Path
import json

import numpy as np
import pytest

from antigravity_research.agminer import (
    hook17_ph13_integrated_go_no_go as ph13
)


@pytest.fixture(scope='module')
def prior():
    file = (
        Path.cwd()
        /ph13.ARCHIVES['ph12_result'][0]
    )
    return json.loads(file.read_text())


@pytest.fixture(scope='module')
def analysis(prior):
    return ph13.run(Path.cwd())


@pytest.fixture(scope='module')
def principal(prior):
    return ph13.exact_portal_principal(prior)


@pytest.fixture(scope='module')
def joint(prior):
    return ph13.exact_joint_scalar_carrier_hessian(prior)


@pytest.fixture(scope='module')
def resolution():
    return {
        n:ph13.trace_induced_second_carrier(n=n)
        for n in (65,97,129)
    }


def test_source_independent_reconstruction(analysis,prior):
    s=analysis['independent_radial_static_fixed_charge']
    v=prior['primary_gauged_equilibrium']
    assert s['bvp_omega']==pytest.approx(v['omega'],abs=5e-8)
    assert s['bvp_Noether_number']==pytest.approx(
        v['Noether_number'],abs=5e-5
    )
    assert s['bvp_rms_max']<2e-9


def test_source_energy_reconstruction(analysis,prior):
    s=analysis['independent_radial_static_fixed_charge']
    assert s['bvp_energy_with_Coulomb_tail']==pytest.approx(
        prior['primary_gauged_equilibrium']['canonical_energy'][
            'scalar_plus_electromagnetic_total_including_Coulomb_tail'
        ],
        rel=1e-5
    )
    assert s['relative_discrete_energy_error']<.001


def test_finite_volume_exact_charge_enforced(analysis):
    v=analysis['independent_radial_static_fixed_charge']['finite_volume']
    assert v['Gauss_flux_relative_error']<1e-8
    assert v['gauss_residual']<1e-9
    assert v['Noether_number']>0


def test_finite_volume_energy_positive_components(analysis):
    v=analysis['independent_radial_static_fixed_charge']['finite_volume']
    assert all(x>0 for x in v['components'].values())
    assert v['energy']==pytest.approx(
        sum(v['components'].values()),rel=1e-12
    )


def test_radial_fixed_charge_subspace_only(analysis):
    s=analysis['independent_radial_static_fixed_charge']
    assert s['finite_modes']==8
    assert s['negative_eigenvalues']==0
    assert s['hessian_min']>0
    assert s['classification']==(
        'RESTRICTED_RADIAL_FIXED_CHARGE_ENERGY_SCREEN_ONLY'
    )
    assert s['full_radial_dynamical_spectrum']=='NOT_CALCULATED'


def test_subspace_hessian_cross_resolution(analysis):
    a=analysis['independent_radial_static_fixed_charge']
    b=analysis['radial_resolution_crosscheck']
    assert b['finite_volume']==640
    assert b['negative_eigenvalues']==0
    assert abs(a['hessian_min']-b['hessian_min'])<.05


def test_branch_slope_not_promoted_to_stability(prior,analysis):
    assert (
        prior['local_branch_stability_slope_control'][
            'dQ_domega_finite_difference'
        ]<0
    )
    assert analysis['gates'][
        'P1_FULL_RADIAL_DYNAMICAL_AND_ANGULAR_STABILITY'
    ]=='NOT_CERTIFIED'


def test_exact_portal_matter_trace(principal):
    assert principal['lambda_at_P0']=='-2*alpha*(K + 2*U)'
    assert principal['same_action_matter_trace_loading']==(
        'REQUIRED_NONCONSTANT_LAMBDA'
    )


def test_exact_carrier_displacements(principal):
    assert principal['same_action_electric_displacements']==(
        'DX=EX+lambda_BY_AND_DY=EY+lambda_BX'
    )
    assert principal['Y_field_source_and_exterior_mixed_P']==(
        'NOT_PRESENT_IN_PH12'
    )


def test_frozen_carrier_rank_one_hessian_counterexample(principal):
    assert principal['longitudinal_counterexample']<0
    assert principal['longitudinal_small_field_control']>0
    assert principal['full_Dirac_Bergmann_constraint_health']==(
        'NOT_CERTIFIED'
    )


def test_actual_ph12_scalar_center_unloaded(principal):
    p=principal['source_center_conditional_threshold']
    assert p['rank_one_Lpp_at_P0']<0
    assert p['frozen_matter_magnetic_norm_critical']>0
    assert 'HYPOTHETICAL' in p['interpretation']


def test_joint_scalar_and_carrier_frozen_different(joint):
    s=joint['source_center_conditional_joint_hessian']
    assert s['frozen_carrier_threshold_B']>(
        s['joint_scalar_carrier_threshold_B']
    )
    assert s['B2_test_frozen_eigenvalue']>0
    assert s['B2_test_joint_Schur']<0


def test_independent_mixed_derivative_numeric(joint):
    assert joint[
        'independent_mixed_second_derivative_fd'
    ]==pytest.approx(
        joint['independent_mixed_second_derivative_exact'],
        abs=3e-7
    )


def test_joint_counterexample_not_actual_instability(joint,analysis):
    assert joint['classification']==(
        'NECESSARY_LOCAL_PRINCIPAL_MATRIX_NOT_FULL_GAUGE_GRAVITY_PROOF'
    )
    assert analysis['gates'][
        'P2_TWO_CARRIER_ACTUAL_BACKGROUND_AND_SOURCE'
    ]=='NOT_SOLVED'


def test_no_microscopic_y_source_in_linear_response(resolution):
    assert all(
        x['Y_microscopic_current']=='NONE_TO_FIRST_ORDER'
        for x in resolution.values()
    )
    assert all(
        x['Y_induced_source']=='CURL_LAMBDA_EX_EQUIVALENT_ONLY'
        for x in resolution.values()
    )


def test_trace_induced_Y_is_nontrivial(resolution):
    assert all(
        x['Y_B2_integral']>1e-6
        for x in resolution.values()
    )
    assert all(
        x['max_abs_local_P']>1e-6
        for x in resolution.values()
    )


def test_induced_ampere_and_divergence_residuals(resolution):
    assert all(
        x['ampere_residual_spectral']<1e-10
        for x in resolution.values()
    )
    assert all(
        x['divB_over_B_norm_spectral']<1e-10
        for x in resolution.values()
    )


def test_topological_signed_volume_P_zero(resolution):
    for x in resolution.values():
        assert abs(x['signed_integral_P'])<1e-12
        assert x['L1_local_P']>1e-5


def test_induced_Y_spatial_resolution_convergence(resolution):
    a=resolution[97]
    b=resolution[129]
    assert abs(
        a['Y_B2_integral']-b['Y_B2_integral']
    )/b['Y_B2_integral']<.01
    assert abs(
        a['L1_local_P']-b['L1_local_P']
    )/b['L1_local_P']<.01


def test_induction_zero_portal_slope():
    r=ph13.trace_induced_second_carrier(
        n=49,alpha=0.
    )
    assert r['Y_B2_integral']==0
    assert r['max_abs_local_P']==0


def test_induction_coincident_conjugates_cancel():
    r=ph13.trace_induced_second_carrier(
        n=49,same_center=True
    )
    assert r['Y_B2_integral']==0
    assert r['max_abs_local_P']==0


def test_single_spherical_aliasing_vanishes(analysis,resolution):
    x=analysis[
        'PH12_pair_linear_trace_induced_Y'
    ]['single_spherical_aliasing']

    assert x['65']['Y_B2_integral']>(
        x['97']['Y_B2_integral']
    )
    assert x['97']['Y_B2_integral']>(
        x['129']['Y_B2_integral']
    )
    assert (
        x['129']['Y_B2_integral']
        /resolution[129]['Y_B2_integral']
    )<1e-5


def test_source_charge_recomputed_from_bvp(prior,resolution):
    expected=prior[
        'primary_gauged_equilibrium'
    ]['gauge_charge_integrated']

    assert resolution[65][
        'single_isolated_source_gauge_charge'
    ]==pytest.approx(expected,rel=1e-6)


def test_induction_not_promoted_as_composite(analysis):
    a=analysis['PH12_pair_linear_trace_induced_Y']
    assert a['composite_on_shell']==(
        'NO_OFFSHELL_TWO_CENTER_SUPERPOSITION'
    )
    assert a['fully_nonperturbative_conformal_Maxwell_matter']==(
        'NOT_SOLVED'
    )
    assert a['net_craft_force']=='NOT_DERIVED'


def test_noether_internal_balance(analysis):
    a=analysis['whole_spacecraft_momentum_theorem']
    assert a['internal_transfers_cancel']==(
        'PASS_EXACT_NOETHER_CONTROL'
    )
    assert abs(a['PH7_total_discrete_momentum_residual'])<1e-8


def test_no_engine_impulse(analysis):
    a=analysis['whole_spacecraft_momentum_theorem']
    assert a['PH12_pure_X_electric_mixed_P']==0
    assert a['whole_craft_external_impulse']=='NOT_DERIVED'
    assert a['B11_M6_complete_signed_cycle']=='NOT_RUN'


def test_free_particle_binding_not_stability_proof(prior,analysis):
    assert prior['primary_gauged_equilibrium'][
        'canonical_energy'
    ]['energy_per_Noether_number']<1
    assert analysis['gates'][
        'P1_FULL_RADIAL_DYNAMICAL_AND_ANGULAR_STABILITY'
    ]=='NOT_CERTIFIED'


def test_uv_completion_not_promoted(analysis):
    assert analysis['gates'][
        'P1_PHI6_UV_NATURALNESS'
    ]=='NOT_CERTIFIED'
    assert analysis['gates'][
        'STRICT_COMPLETE_LT10MJ'
    ]=='NOT_CERTIFIED'


def test_earth_reaction_not_assumed(analysis):
    assert analysis['gates'][
        'P2_EARTH_INTERACTION_AND_EXTERNAL_CRAFT_FORCE'
    ]=='NOT_DERIVED'
    assert analysis['gates'][
        'P3_NEUTRAL_GE1G_GE1M'
    ]=='NOT_CERTIFIED'
    assert analysis['gates']['006D_REPLACED']=='NO'


def test_archive_mismatch_detects_tampering(tmp_path):
    f=tmp_path/ph13.ARCHIVES['ph12_module'][0]
    f.parent.mkdir(parents=True)
    f.write_text('tampered')
    assert ph13.provenance(tmp_path)[
        'ph12_module'
    ]['status']=='HASH_MISMATCH'


def test_missing_archives_detected(tmp_path):
    assert all(
        x['status']=='MISSING'
        for x in ph13.provenance(tmp_path).values()
    )


@pytest.mark.parametrize('changes',[
    {'collocation':20},
    {'finite_volume':20},
    {'f0':0},
    {'R':12},
    {'m':0},
    {'b':-1},
    {'e':-1},
    {'tolerance':-1},
    {'R':float('nan')}
])
def test_invalid_source_parameters(changes):
    with pytest.raises(ValueError):
        ph13.bvp(
            replace(
                ph13.Parameters(),**changes
            )
        )


@pytest.mark.parametrize('args',[
    {'n':32},
    {'n':64},
    {'length':-1},
    {'separation':-1},
    {'alpha':float('nan')}
])
def test_invalid_trace_geometry(args):
    with pytest.raises(ValueError):
        ph13.trace_induced_second_carrier(**args)


def test_bad_source_number_fails_closed():
    with pytest.raises(ValueError):
        ph13.finite_volume_reduced_energy(
            np.ones(480),-3,ph13.Parameters()
        )


def test_bad_amplitude_shape_fails_closed():
    with pytest.raises(ValueError):
        ph13.finite_volume_reduced_energy(
            np.ones(5),2,ph13.Parameters()
        )


def test_previous_branch_must_match(tmp_path):
    f=tmp_path/ph13.ARCHIVES['ph12_result'][0]
    f.parent.mkdir(parents=True)
    f.write_text(
        json.dumps({'branch':'PH11'})
    )
    with pytest.raises(ValueError):
        ph13.run(tmp_path)
