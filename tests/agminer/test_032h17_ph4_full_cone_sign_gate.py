"""PH4 focused regression: exact 3D cones, source-sign limits, fail-closed gates."""
from dataclasses import replace
from pathlib import Path
import math
import numpy as np
import pytest

from antigravity_research.agminer.hook17_ph4_full_cone_sign_gate import (
    Case,cases,cone_roots,derivatives,directional_audit,evaluate,fields,
    independent_six_by_six_determinant,
    independent_full_lagrangian_second_variation,
    normals,provenance,run,symbolic_and_farfield,
)


def case(label):
    return next(c for c in cases() if c.label==label)


def test_exact_farfield_signs_and_curvature_threshold():
    data=symbolic_and_farfield()
    assert data['analytic_identities']==8
    assert data['negative_even_farfield_signed_coefficient'].startswith('-12')
    assert data['positive_even_farfield_signed_coefficient'].startswith('+12')
    assert data['dipole_at_r_over_r0_2_linear_accel_ratio']==pytest.approx(1/128)
    assert data['dipole_at_r_over_r0_2_even_accel_ratio']==pytest.approx(1/8192)


@pytest.mark.parametrize('law',('linear','even_negative','even_positive'))
def test_portal_derivative_independent_finite_differences(law):
    x=.31;h=1e-5
    sig,sig1,sig2=derivatives(law,.4,x)
    fp=derivatives(law,.4,x+h)[0]
    fm=derivatives(law,.4,x-h)[0]
    assert (fp-fm)/(2*h)==pytest.approx(sig1,abs=1e-9)
    assert (fp+fm-2*sig)/h**2==pytest.approx(sig2,abs=3e-6)


@pytest.mark.parametrize('label,starts',[
    ('linear_mixed','RED_SUPERLUMINAL'),
    ('negative_even_mixed','PASS_SCOPED_ALL_NORMALS_SUBLUMINAL'),
    ('positive_even_mixed','RED_SUPERLUMINAL'),
    ('negative_even_large_P','RED_SUPERLUMINAL'),
    ('negative_even_gradient_failure','RED_GRADIENT'),
    ('negative_even_P_zero_nontrivial_fields','PASS_SCOPED_ALL_NORMALS_SUBLUMINAL'),
    ('linear_no_matter','PASS_SCOPED_LUMINAL'),
    ('linear_no_coupling','PASS_SCOPED_LUMINAL'),
    ('linear_kinetic_failure','RED_KINETIC'),
    ('negative_even_noncollinear','PASS_SCOPED_ALL_NORMALS_SUBLUMINAL'),
    ('linear_noncollinear','RED_SUPERLUMINAL'),
    ('zero_fields','PASS_SCOPED_LUMINAL'),
])
def test_pre_registered_case_verdicts(label,starts):
    rec=evaluate(case(label))
    assert rec['exact_all_normals_verdict'].startswith(starts)
    assert rec['full_matter_and_gravity_characteristics']=='NOT_TESTED'


@pytest.mark.parametrize('label',[
    'negative_even_mixed','negative_even_noncollinear',
    'linear_noncollinear','positive_even_mixed',
])
def test_exact_all_angle_D_min_bound_agrees_with_sampled(label):
    result=directional_audit(case(label),128)
    assert result['directions_tested']==134
    assert result['smallest_sampled_D']>=result['exact_min_D']-2e-14
    assert result['directional_sampling_is_proof'].startswith('NO_')


@pytest.mark.parametrize('label',[
    'negative_even_mixed','negative_even_noncollinear','linear_noncollinear',
])
def test_independent_full_6x6_symbol_factorization(label):
    background=case(label)
    n=np.array([.37,-.52,.77])
    for s in (-1.31,.39,.73,1.27):
        result=independent_six_by_six_determinant(background,n,s)
        assert result['relative_scaled_error']<3e-12


@pytest.mark.parametrize('label',[
    'negative_even_mixed','negative_even_noncollinear','linear_noncollinear',
])
def test_independent_full_action_second_variation(label):
    result=independent_full_lagrangian_second_variation(
        case(label),np.array([.37,-.52,.77]))
    assert result['abs_error']<3e-6


def test_all_angle_negative_even_extraordinary_cone_within_light():
    for label in ('negative_even_mixed','negative_even_noncollinear'):
        background=case(label)
        for n in normals(80):
            roots=cone_roots(background,n)['extraordinary_phase_roots']
            assert roots is not None
            assert max(abs(x) for x in roots)<=1+2e-12


def test_all_angle_linear_superluminal_counterexample():
    background=case('linear_mixed')
    speeds=[cone_roots(background,n)['extraordinary_phase_roots']
            for n in normals(40)]
    assert any(max(abs(x) for x in roots)>1.05 for roots in speeds if roots)


def test_high_field_parity_even_causes_curvature_sign_reversal():
    weak=evaluate(case('negative_even_mixed'))
    high=evaluate(case('negative_even_large_P'))
    assert weak['chi']<0<high['chi']
    assert high['A_kinetic']>0 and high['D_min_all_normals']>0
    assert high['exact_all_normals_verdict'].startswith('RED_SUPERLUMINAL')


def test_negative_even_no_linear_force_at_P_zero():
    bg=evaluate(case('negative_even_P_zero_nontrivial_fields'))
    assert bg['P']==0.0
    assert bg['sigma_prime']==0.0
    assert bg['chi']<0


def test_negative_even_conformal_map_invertible_at_finite_P():
    for p in (-100.,-3.,-.2,0.,.2,3.,100.):
        sig,first,_=derivatives('even_negative',.4,p)
        assert 1-4*p*first>=1


@pytest.mark.parametrize('invalid',[(-1, .4),(.3,-1),(.3,float('nan'))])
def test_matter_coupling_input_rejected(invalid):
    bg=replace(case('negative_even_mixed'),rho=invalid[0],coupling=invalid[1])
    with pytest.raises(ValueError):evaluate(bg)


def test_bad_field_shapes_rejected():
    with pytest.raises(ValueError):evaluate(replace(case('negative_even_mixed'),ex=(1.,2.)))
    with pytest.raises(ValueError):evaluate(replace(case('negative_even_mixed'),ex=(1.,2.,math.inf)))
    with pytest.raises(ValueError):derivatives('not_law',.4,.1)


def test_degenerate_direction_rejected():
    with pytest.raises(ValueError):cone_roots(case('negative_even_mixed'),np.zeros(3))
    with pytest.raises(ValueError):cone_roots(case('negative_even_mixed'),np.array([np.nan,0.,1.]))


@pytest.mark.parametrize('bad_s',[0.,1.,-1.,math.nan])
def test_bad_trial_frequency_rejected(bad_s):
    with pytest.raises(ValueError):independent_six_by_six_determinant(
        case('negative_even_mixed'),np.array([1.,0.,0.]),bad_s)


def test_missing_history_fails_closed(tmp_path):
    result=run(tmp_path)
    assert result['gates']['PH4_P0_PROVENANCE']=='UNRESOLVED'
    assert result['gates']['PH4_P3_EARTH_DOWN_FULL_CRAFT_UP']=='NOT_DERIVED'
    assert result['gates']['PH4_B11_M6_FULL_CAUSAL_LOADED_IMPULSE']=='NOT_RUN'
    assert result['gates']['PH4_STRICT_COMPLETE_LT10MJ']=='NOT_CERTIFIED'
    assert result['gates']['PH4_006D_REPLACED']=='NO'


def test_history_hash_mismatch_fails_closed(tmp_path):
    folder=tmp_path/'src/antigravity_research/agminer'
    folder.mkdir(parents=True)
    (folder/'hook17_ph3_causal_portal_gate.py').write_text('not frozen code')
    assert provenance(tmp_path)['ph3_source']['status']=='HASH_MISMATCH'
