"""B17-M5V fail-closed integration and numeric validation tests."""
import json
import pytest

from antigravity_research.agminer import (
    hook17_r3b_m5v_unified_exterior_action as m,
)


def test_exact_parent_hashes():
    assert m.verify_provenance() == m.EXPECTED_SHA256


def test_manifest_fixed_and_unique():
    full=m.manifest('full')
    short=m.manifest('preflight')
    assert len(full)==50
    assert len(short)==3
    assert all(x in full for x in short)
    assert len({x['name'] for x in full})==len(full)
    assert len({json.dumps(x['parameters'],sort_keys=True) for x in full})==len(full)
    for job in full:
        assert job['parameters']['cell_q'] in (4,8,12,16)
        assert job['parameters']['source_q'] in (4,6)


def test_missing_full_manifest_cannot_certify_anything():
    result=m.summary(m.manifest('full'),{}, {})
    assert result['decision']=='INCOMPLETE_NO_DECISION'
    assert result['gates']['V0_registered_complete']=='INCOMPLETE'
    assert result['gates']['V7_continuum_limit_and_real_exterior_DtN']=='NOT_CERTIFIED'
    assert result['gates']['V9_whole_spacecraft_external_force']=='NOT_DERIVED'
    assert result['artificial_model_complete'] is False
    assert result['whole_spacecraft_lift'] is False


@pytest.mark.parametrize('source_scale', [0.,.5,1.])
def test_unified_onshell_and_source_response(source_scale):
    result=m.run_case(h=.2,domain='compact',source_scale=source_scale,
                      resolve=(source_scale==1.))
    assert result['stationarity']['weighted_stationarity']<1.e-9
    assert result['stationarity']['weighted_asymmetry']<1.e-10
    assert result['stationarity']['source_neutrality_max_relative']<1.e-10
    assert result['on_shell_identity_abs_j']<1.e-7
    for key in ('earth','craft','common'):
        assert abs(result['fixed_u_minus_analytic_j_m'][key])<2.e-3
    if source_scale==1.:
        for key in ('earth','craft','common'):
            assert abs(result['resolved_minus_analytic_j_m'][key])<2.e-3
    if source_scale==0.:
        assert result['Q_interaction_j']==0.
        assert all(v==0. for v in result['analytic_j_m'].values())
    assert result['whole_spacecraft_lift_certified'] is False
    assert result['boundary_reaction_not_derived'] is True


def test_quadratic_scaling_of_prescribed_source():
    half=m.run_case(h=.2,domain='compact',source_scale=.5)
    full=m.run_case(h=.2,domain='compact',source_scale=1.)
    assert half['Q_interaction_j']==pytest.approx(full['Q_interaction_j']/4.,abs=1.e-8)
    for k in ('earth','craft','common'):
        assert half['analytic_j_m'][k]==pytest.approx(full['analytic_j_m'][k]/4.,abs=1.e-7)


def test_current_reversal_preserves_independent_checks():
    result=m.run_case(h=.2,domain='compact',reverse_current=True)
    for key in ('earth','craft','common'):
        assert abs(result['fixed_u_minus_analytic_j_m'][key])<.002
    assert result['source_derivative_relative_defect']<.001
