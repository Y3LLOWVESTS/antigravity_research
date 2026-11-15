"""PH5 source-independent exact theorem, cone, parity, and force gates."""
import math
import numpy as np
import pytest

from antigravity_research.agminer.hook17_ph5_concavity_escape_audit import (
    Trial, archival, exact_theorems, sigma_derivatives, evaluate,
    independent_six_determinant, finite_difference_radial,
    prescribed_cases, run,
)


def named(name): return next(x for x in prescribed_cases() if x.name==name)


def test_exact_symbolic_conditions():
    assert exact_theorems()['exact_symbolic_identities']==10


@pytest.mark.parametrize('law',('mixed_odd','negative_even','positive_even','linear'))
def test_portal_derivatives_by_difference(law):
    a,b,p=.3,.4,.24
    value,deriv,second=sigma_derivatives(law,a,b,p)
    h=1e-5
    plus=sigma_derivatives(law,a,b,p+h)[0]
    minus=sigma_derivatives(law,a,b,p-h)[0]
    assert (plus-minus)/(2*h)==pytest.approx(deriv,abs=1e-9)
    assert (plus+minus-2*value)/h**2==pytest.approx(second,abs=3e-6)


@pytest.mark.parametrize('name,outward,cone',[('even_concave_inward',False,'PASS_SUBLUMINAL_SCOPED'),
 ('even_convex_outward',True,'RED_SUPERLUMINAL_SCOPED'),
 ('odd_concave_outward',True,'PASS_SUBLUMINAL_SCOPED'),
 ('odd_convex_at_high_P',False,'RED_SUPERLUMINAL_SCOPED'),
 ('linear_outward_unsafe',True,'RED_SUPERLUMINAL_SCOPED'),
 ('odd_background_matter_off',True,'LUMINAL_SCOPED'),
 ('odd_no_carrier_fields',False,'LUMINAL_SCOPED')])
def test_registered_categories(name,outward,cone):
    value=evaluate(named(name))
    assert value['outward_test_matter']==outward
    assert value['cone_gate']==cone
    assert not value['source_and_matter_self_consistent']


def test_mixed_odd_corridor_exists_with_nonzero_fields():
    t=named('odd_concave_outward')
    rec=evaluate(t)
    assert 0<rec['P']<t.a/(2*t.b)
    assert rec['F_double_prime']<0
    assert rec['chi']<0 and rec['K']>0 and rec['Dmin']>0
    assert rec['sigma_prime']>0 and rec['conformal_trace_jacobian']>0


def test_mixed_odd_large_P_loses_corridor():
    t=named('odd_convex_at_high_P')
    rec=evaluate(t)
    assert rec['sigma_prime']<0
    assert rec['chi']>0


@pytest.mark.parametrize('name',('even_concave_inward','even_convex_outward','odd_concave_outward'))
def test_radial_force_independent_finite_difference(name):
    rec=finite_difference_radial(named(name))
    assert rec['absolute_error']<1e-9


@pytest.mark.parametrize('name',('even_concave_inward','odd_concave_outward','odd_convex_at_high_P'))
def test_independent_six_matrix_determinant(name):
    t=named(name)
    for n in (np.array([.3,.4,.5]),np.array([0,0,1.]),np.array([-.31,.4,-.76])):
        for s in (.38,.71,1.28):
            assert independent_six_determinant(t,n,s)<1e-11


@pytest.mark.parametrize('rho,a,b',((-1,.3,.4),(.4,-.3,.4),(.4,.3,-.4),(.4,math.nan,.4)))
def test_invalid_parameters_fails(rho,a,b):
    with pytest.raises(ValueError):
        evaluate(Trial('invalid','mixed_odd',a,b,rho))


def test_bad_fields_fail():
    with pytest.raises(ValueError):
        evaluate(Trial('bad','mixed_odd',.3,.4,.35,ex=(.1,.2)))


def test_no_invented_earth_lift(tmp_path):
    rec=run(tmp_path)
    assert rec['gates']['PH5_P3_EARTH_DOWN_CRAFT_UP']=='NOT_DERIVED'
    assert rec['gates']['PH5_P3_NEUTRAL_1G_AT_1M']=='NOT_CERTIFIED'
    assert rec['gates']['PH5_P0_HISTORY']=='UNRESOLVED'
    assert rec['gates']['PH5_006D_REPLACED']=='NO'


def test_history_fails_on_changed_bytes(tmp_path):
    path=tmp_path/'src/antigravity_research/agminer/hook17_ph4_full_cone_sign_gate.py'
    path.parent.mkdir(parents=True)
    path.write_text('wrong')
    assert archival(tmp_path)['ph4_source']['status']=='MISMATCH'
