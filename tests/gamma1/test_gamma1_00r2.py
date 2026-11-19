"""Focused GAMMA1-00R2 tests of evidence sufficiency and nonuniqueness.

Historical experiments are not repeated or modified.
"""
from __future__ import annotations

from fractions import Fraction
from pathlib import Path

import pytest
import sympy as sp

from antigravity_research.gamma1.gamma1_00r2_completion_gate import (
    EXPECTED_CASES, PH16_SOURCE_SHA,
    exact_completion_witness, independent_fraction_check,
    result_atlas, result_sufficiency, source_structure,
)

ROOT = Path(__file__).resolve().parents[2]
PH16 = ROOT/'src/antigravity_research/ph16/ph16_04_joint_stationary.py'


def fixture():
    cases = {}
    for key, (nr, L) in EXPECTED_CASES.items():
        cases[key] = {
            'mesh': {'nr': nr, 'L': L, 'h': .2},
            'Y_preconditioned_joint': {
                'final_residual_L2': 6.5e-8,
                'root_success': True,
                'N': [400.0, 400.0],
                'frozen_magnetic_margin_min': .25,
                'frozen_negative_cells': 0,
                'Y_norm': .1,
                'Pmax': .01,
            },
            'direct_weak_seed': {'final_residual_L2': .018 if key == '18_L12' else 5e-8},
        }
    return {
        'source_sha256': PH16_SOURCE_SHA,
        'scoped_gates_pass': True,
        '006D_replaced': False,
        'whole_craft_Earth_down_craft_up': 'NOT_DERIVED',
        'scoped_results': {'cases': cases},
    }


def test_actual_source_structure():
    s = source_structure(PH16)
    assert s['stationary_state_local_only']
    assert s['final_summary_variable'] == 'pre_solved'
    assert not s['final_state_arrays_returned']
    assert s['PH16_source_sha256'] == PH16_SOURCE_SHA


def test_exact_completion_witness():
    checks = exact_completion_witness()['exact_checks']
    assert len(checks) >= 10 and all(checks.values())


@pytest.mark.parametrize('eta,expected', [(-2, -1), (0, 1), (2, 3)])
def test_frozen_fluid_transverse_electric_hessian(eta, expected):
    e = sp.Symbol('E', real=True)
    L = sp.Rational(1+eta, 2)*e**2
    assert sp.diff(L, e, 2) == expected


@pytest.mark.parametrize('eta', [-2, 0, 2])
def test_static_zero_for_every_eta(eta):
    E = sp.Symbol('E')
    delta = sp.Rational(eta, 2)*E*E
    assert delta.subs(E, 0) == 0
    assert sp.diff(delta, E).subs(E, 0) == 0


@pytest.mark.parametrize('eta', [-2, 0, 2])
def test_exact_fraction_finite_difference(eta):
    h = Fraction(1, 1024)
    fun = lambda E: Fraction(1+eta, 2)*E*E
    fd = (fun(h)-2*fun(Fraction(0))+fun(-h))/(h*h)
    assert fd == 1+eta
    assert independent_fraction_check()[str(eta)] == fd


def test_dispersion_sign_differs():
    k = sp.symbols('k', positive=True)
    assert k**2/Fraction(-1) < 0
    assert sp.simplify(k**2/(1+2)) == k**2/3


def test_gauge_invariant_fieldstrength_identity():
    x, y = sp.symbols('x y')
    gauge = sp.Function('gauge')(x, y)
    assert sp.diff(gauge, x, y)-sp.diff(gauge, y, x) == 0


def test_source_saved_no_full_fields():
    out = result_sufficiency(fixture())
    assert not out['all_three_complete_saved_profiles']
    assert not out['can_evaluate_full_Lorentzian_constrained_spectrum']
    assert all(set(fields) == {'F', 'A', 'Y'} for fields in out['missing_final_arrays_per_mesh'].values())


def test_weak_seed_failure_preserved():
    data = result_sufficiency(fixture())
    assert data['cases']['18_L12']['weak_seed_residual_L2'] == .018


@pytest.mark.parametrize('key', list(EXPECTED_CASES))
def test_noether_retained_per_case(key):
    out = result_sufficiency(fixture())
    assert out['cases'][key]['Noether_N'] == [400, 400]
    assert out['cases'][key]['stationary_root_success']


def test_reject_claim_drift():
    f = fixture()
    f['006D_replaced'] = True
    with pytest.raises(ValueError):
        result_sufficiency(f)


def test_reject_stationarity_drift():
    f = fixture()
    f['scoped_results']['cases']['12_L12']['Y_preconditioned_joint']['final_residual_L2'] = 1.e-4
    with pytest.raises(ValueError):
        result_sufficiency(f)


def test_reject_source_sha_drift():
    f = fixture()
    f['source_sha256'] = 'bad'
    with pytest.raises(ValueError):
        result_sufficiency(f)


def test_reject_missing_case():
    f = fixture()
    f['scoped_results']['cases'].pop('18_L12')
    with pytest.raises(ValueError):
        result_sufficiency(f)


def test_reject_injected_complete_final_profiles():
    f = fixture()
    for record in f['scoped_results']['cases'].values():
        record['Y_preconditioned_joint'].update({'F': [1], 'A': [1], 'Y': [1]})
    with pytest.raises(ValueError):
        result_sufficiency(f)


def test_full_scoped_atlas_never_promotes():
    a = result_atlas(fixture(), PH16)
    assert a['qualified_physical_survivors'] == []
    assert not a['GAMMA1_01_authorized']
    assert not a['PH17_authorized']
    assert not a['006D_replaced']
    assert a['Einstein_metric'] == 'NOT_SOLVED'
    assert a['Earth_down'] == 'NOT_DERIVED'
    assert a['whole_craft_up'] == 'NOT_DERIVED'
    assert a['complete_SI_energy_lt10MJ'] == 'NOT_CERTIFIED'


def test_no_prior_run_recomputed():
    a = result_atlas(fixture(), PH16)
    assert a['PH16_source_structure']['recomputation_performed'] is False
    assert a['PH16_R2_saved_data']['rerun_of_PH16_performed'] is False


def test_only_diagnostic_new_operator():
    a = result_atlas(fixture(), PH16)
    assert a['covariant_completion_nonuniqueness']['role'] == (
        'NONUNIQUENESS_COUNTEREXAMPLE_NOT_PROPOSED_NEW_PHYSICS'
    )


def test_prevents_stability_certification():
    a = result_atlas(fixture(), PH16)
    assert a['M0_actual_stationary_background_ghost'] == 'NOT_ESTABLISHED'
    assert a['M0_full_modes_from_archived_R2'] == 'NOT_DETERMINABLE'
