"""PH11: independent action variation, radial traction, fail-closed gates."""

import copy
import json
from pathlib import Path

import pytest
import sympy as sp

from antigravity_research.agminer import (
    hook17_ph11_universal_metric_support_gate as ph11
)

DATA = (
    Path(__file__).resolve().parents[2]
    / 'results/data/032h17_ph10_bounded_well_20261115T044314781842Z.json'
)


@pytest.fixture(scope='module')
def ph10():
    return json.loads(DATA.read_text())


@pytest.fixture(scope='module')
def inspected(ph10, tmp_path_factory):
    return ph11.run(
        tmp_path_factory.mktemp('no_archive'), ph10
    )


def test_symbolic_action_variations():
    x = ph11.exact_variations()

    assert x['universal_scalar_metric_chain_rule'] == 'PASS_EXACT'
    assert x['matter_trace_portal_loading'] == 'PASS_EXACT'
    assert x['metric_variation_Weyl_cross_check'] == 'PASS_EXACT'
    assert x['metric_variation_anisotropic_zz_cross_check'] == 'PASS_EXACT'
    assert x['Maxwell_four_dimensional_Weyl_invariance'] == 'PASS_EXACT'


def test_portal_trace_nonzero_for_massive_matter():
    p, a, b, K, U = sp.symbols(
        'p a b K U', real=True
    )
    sig = a*p-b*p**2
    om = sp.exp(sig)
    lam = sp.diff(-om**2*K-om**4*U, p)

    assert sp.simplify(
        lam.subs({K: 0, U: 1, p: 0, b: 0})+4*a
    ) == 0


def test_vacuum_and_zero_slope_portal_lam_vanish():
    p, a, b, K, U = sp.symbols(
        'p a b K U', real=True
    )
    om = sp.exp(a*p-b*p*p)
    lam = sp.diff(-om**2*K-om**4*U, p)

    assert sp.simplify(lam.subs({K: 0, U: 0})) == 0
    assert sp.simplify(lam.subs({a: 0, b: 0})) == 0


def test_density_variable_lambda_has_new_bulk_term():
    z = sp.symbols('z')
    c = sp.Function('c')(z)
    b = sp.Function('b')(z)

    assert sp.simplify(
        sp.diff(c*b, z)-c*sp.diff(b, z)
    ) == b*sp.diff(c, z)


def test_ward_gauge_variation_is_not_just_charge_neutrality():
    t = ph11.exact_variations()

    assert (
        t['source_phase_gauge_Noether_identity']
        == 'PASS_EXACT_OFF_SHELL_IDENTITY'
    )
    assert t['all_species_universal_metric_EOM'] == 'NOT_DERIVED'


@pytest.mark.parametrize('idx', [0, 1])
def test_shell_pressure_exact_positive(ph10, idx):
    r = ph11.wall_load(ph10)['modes'][idx]

    assert r['integrated_radial_traction_single_species'] > 0
    assert (
        r['integrated_radial_traction_pair']
        == 2*r['integrated_radial_traction_single_species']
    )
    assert r['radial_net_vector_force_for_isolated_spherical_well'] == 0


@pytest.mark.parametrize('idx', [0, 1])
def test_radial_traction_matches_independent_energy_difference(ph10, idx):
    r = ph11.wall_load(ph10)['modes'][idx]

    assert r[
        'integrated_radial_traction_single_species'
    ] == pytest.approx(
        -r['independent_energy_radius_derivative_single_species'],
        rel=5e-8
    )
    assert r['relative_derivative_disagreement'] < 5e-8


def test_radial_pair_total_reproduces(ph10):
    w = ph11.wall_load(ph10)

    assert w[
        'total_integrated_radial_traction_magnitude'
    ] == pytest.approx(4.7692969236461344, abs=1e-10)

    assert (
        w['finite_onboard_trap_hardware_energy']
        == 'NOT_IN_PH10_LEDGER'
    )
    assert w['net_external_propulsive_force'] == 'NOT_DERIVED'


def test_wall_derivative_step_refinement(ph10):
    a = ph11.wall_load(ph10, relative_step=1.e-4)
    b = ph11.wall_load(ph10, relative_step=1.e-5)

    assert (
        a['total_integrated_radial_traction_magnitude']
        == b['total_integrated_radial_traction_magnitude']
    )
    assert max(
        v['relative_derivative_disagreement']
        for v in a['modes']
    ) < 1e-7


def test_loaded_trace_from_energy_ledger(ph10):
    s = ph11.summarize_ph10(ph10)

    assert s[
        'loaded_stress_trace_integral_at_Omega_1'
    ] == pytest.approx(-7.626236863823186)
    assert s[
        'trace_includes_prescribed_trap_but_not_its_hardware'
    ]


def test_current_divergence_is_not_promoted(ph10):
    a = ph11.summarize_ph10(ph10)

    assert a['source_current_relative_divergence'] > .03
    assert a['loaded_scalar_EOM_X'] > .3
    assert a['loaded_scalar_EOM_Y'] > .04


def test_local_pair_reaction_only_not_earth_body(ph10):
    a = ph11.summarize_ph10(ph10)

    assert a['earthward_point_probe_force_shape'] < 0
    assert (
        a['equal_opposite_reaction_for_finite_pair_POTENTIAL_ONLY']
        > 0
    )
    assert a['earth_body_integral_and_GR_stress'] == 'NOT_DERIVED'


def test_ph10_loaded_probe_not_si_acceleration(ph10):
    a = ph11.summarize_ph10(ph10)

    assert 0 < a['neutral_probe_force_shape'] < 1.e-4
    assert a['metric_portal_canonical_mode_health'] == 'NOT_CERTIFIED'


def test_prior_invalid_model_does_not_promote(inspected):
    g = inspected['gates']

    assert g['P1_LOADED_SOURCE_MATTER_EOM'] == 'RED_PH10_OFF_SHELL'
    assert g['P2_FULL_TRACE_LOADED_CARRIER_FIELDS'] == 'MISSING_FROM_PH10'
    assert g['P3_EARTH_DOWN_CRAFT_UP'] == 'NOT_DERIVED'
    assert g['STRICT_FULL_ENERGY_LT10MJ'] == 'NOT_CERTIFIED'
    assert g['006D_REPLACED'] == 'NO'


def test_missing_archive_reports_unresolved(inspected):
    assert inspected['gates']['P0_PROVENANCE'] == 'UNRESOLVED'
    assert all(
        v['status'] == 'MISSING'
        for v in inspected['archival_provenance'].values()
    )


def test_altered_archive_blocks_promotion(ph10, tmp_path):
    r = (
        tmp_path
        / 'results/data/032h17_ph10_bounded_well_20261115T044314781842Z.json'
    )
    r.parent.mkdir(parents=True)
    r.write_text('unrelated')

    assert ph11.provenance(tmp_path)[
        'ph10_result'
    ]['status'] == 'HASH_MISMATCH'

    assert ph11.run(
        tmp_path, ph10
    )['gates']['P0_PROVENANCE'] == 'UNRESOLVED'


def test_wrong_branch_rejected(ph10, tmp_path):
    a = copy.deepcopy(ph10)
    a['branch'] = 'PH9'

    with pytest.raises(ValueError):
        ph11.run(tmp_path, a)


def test_invalid_zero_frequency_fails_closed(ph10):
    a = copy.deepcopy(ph10)
    a['primary']['spec']['omega'] = 0.

    with pytest.raises(ValueError):
        ph11.wall_load(a)


def test_missing_mode_fails_closed(ph10):
    a = copy.deepcopy(ph10)
    a['primary']['eigenstates'].pop()

    with pytest.raises(ValueError):
        ph11.wall_load(a)


def test_variational_stress_not_si_certified(ph10):
    w = ph11.wall_load(ph10)

    assert w['SI_calibration'] == 'NONE'
    assert w['scope'] == 'FIXED_STATES_SQUARE_WELL_INTERFACE_ONLY'


def test_full_EH_eom_not_fake_pass(inspected):
    v = inspected['exact_variations']

    assert v['einstein_source_on_shell'] == 'NOT_DERIVED'
    assert v['full_U1_constraints_and_mode_health'] == 'NOT_CERTIFIED'
    assert inspected['gates']['B11_M6_FULL_SIGNED_CYCLE'] == 'NOT_RUN'
