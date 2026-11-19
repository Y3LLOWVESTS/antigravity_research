"""GAMMA1-00R1 scoped local action/FD and exterior controls."""
import math
import pytest

from antigravity_research.gamma1.gamma1_00r1_local_bridge import (
    Trial,
    Sector,
    trials,
    evaluate,
    derivative_audit,
    exact_identities,
    farfield,
    atlas,
)


def test_exact_identities():
    checks = exact_identities()
    assert len(checks) >= 12
    assert all(checks.values()), checks


@pytest.mark.parametrize('name', list(trials()))
@pytest.mark.parametrize('step', [1.e-5, 5.e-6])
def test_independent_metric_and_field_variations(name, step):
    audit = derivative_audit(
        trials()[name], step
    )

    assert len(audit['relative_errors']) == 8
    assert audit['max_relative_error'] < 5.e-7


def test_ph16_beta_40_offshell_kinetic_not_uniform():
    witness = evaluate(
        trials()['negative_kinetic_offshell']
    )

    assert witness['electric_kinetic_min_eigen'] < -9
    assert math.isclose(
        witness['electric_kinetic_min_eigen'],
        -9.23952
    )
    assert witness['P'] == 0


def test_good_offshell_control():
    assert evaluate(
        trials()['nontrivial_isotropic']
    )['electric_kinetic_min_eigen'] > 0


def test_metric_active_source_both_signs_offshell():
    assert evaluate(
        trials()['nontrivial_isotropic']
    )['local_active_matter_S'] < 0

    assert evaluate(
        trials()['negative_kinetic_offshell']
    )['local_active_matter_S'] > 0


def test_source_and_earth_participants():
    assert [
        s.name
        for s in trials()['nontrivial_isotropic'].sectors
    ] == [
        'source', 'neutral', 'Earth', 'supports'
    ]


def test_source_off_portal():
    out = evaluate(
        trials()['both_carriers_off']
    )

    assert out['P'] == 0
    assert out['sigma'] == 0
    assert out['electric_kinetic_min_eigen'] > 0


def test_coupling_off():
    out = evaluate(
        trials()['coupling_off']
    )

    assert out['sigma'] == 0
    assert out['lambda'] == 0
    assert out['chi_dlambda_dP'] == 0


def test_nonzero_Y_first_variation_even_if_Y_off():
    witness = evaluate(
        trials()['negative_kinetic_offshell']
    )

    # Local Y-electric derivative.
    # Not by itself a nonzero bulk Euler-Lagrange source.
    assert witness[
        'field_density_derivatives'
    ][2] != 0


def test_rank_one_determinant():
    for trial in trials().values():
        e = evaluate(trial)
        H = e['electric_kinetic_H']

        observed = (
            H[0][0]*H[1][1]
            -H[0][1]**2
        )

        baseline = (
            e['volume']
            /(trial.metric[0]*trial.metric[1])
        )

        bx = trial.fields[1]
        by = trial.fields[3]

        expected = baseline*(
            baseline
            +e['chi_dlambda_dP']
            *(bx**2+by**2)/e['volume']
        )

        assert math.isclose(
            observed,
            expected,
            rel_tol=1.e-12,
            abs_tol=1.e-12
        )


def test_dipole_sign_flips():
    assert farfield(
        d=1.e-3
    )['sign'] == 'OUTWARD'

    assert farfield(
        d=-1.e-3
    )['sign'] == 'INWARD'


def test_dipole_farfield_scaling():
    a1 = farfield(
        alpha=.1, beta=0, d=.2, r=2
    )['outward_portal_a_over_c2']

    a2 = farfield(
        alpha=.1, beta=0, d=.2, r=4
    )['outward_portal_a_over_c2']

    assert math.isclose(a1/a2, 128.)


@pytest.mark.parametrize(
    'r', [0, -1, float('nan'), float('inf')]
)
def test_reject_invalid_dipole_radius(r):
    with pytest.raises(ValueError):
        farfield(r=r)


def test_bad_metric_fail_closed():
    trial = trials()['nontrivial_isotropic']

    invalid = Trial(
        (-1, 1, 1, 1),
        trial.fields,
        trial.alpha,
        trial.beta,
        trial.sectors
    )

    with pytest.raises(ValueError):
        evaluate(invalid)


def test_no_craft_force_or_claim_promotion():
    result = atlas()

    assert result['qualified_survivors'] == []
    assert not result['GAMMA1_01_authorized']
    assert not result['006D_replaced']

    assert result['theorems'][
        'Earth_down_and_whole_craft_up'
    ] == 'NOT_DERIVED'

    assert result['theorems'][
        'beta40_PH16_actual_mode_health'
    ] == 'NOT_DETERMINED'

    assert result['theorems'][
        'complete_SI_energy'
    ] == 'NOT_CERTIFIED'
