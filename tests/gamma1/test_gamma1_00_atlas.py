"""Focused GAMMA1-00 algebraic, SI and rejection controls.

Passing these tests does not certify a physical gravitational engine.
"""
import math
import pytest

from antigravity_research.gamma1.gamma1_00_atlas import (
    identities,
    bounds,
    atlas,
    families,
    A,
    C,
    G,
    BUDGET,
    C006D,
)


def test_symbolic():
    checks = identities()
    assert len(checks) >= 14
    assert all(checks.values()), checks


def test_independent_SI():
    b = bounds()

    expected = (
        9.80665*299792458**2
        /(4*6.67430e-11)
    )

    assert math.isclose(
        b['DEC_general_min_J'],
        expected,
        rel_tol=1e-14
    )

    assert b['DEC_general_min_J'] > 1e27


def test_below_source():
    b = bounds()

    assert math.isclose(
        b['DEC_sources_below_min_J'],
        2*b['DEC_general_min_J']
    )


def test_006d_reference():
    assert math.isclose(
        bounds()['006D_reference_J'],
        C006D*A*C*C/G
    )


def test_strict_ceiling():
    assert BUDGET == 1e7
    assert bounds()['conditional_budget_obstruction']


def test_scaling():
    assert math.isclose(
        bounds(a=2*A, h=3)['DEC_general_min_J'],
        18*bounds()['DEC_general_min_J']
    )


@pytest.mark.parametrize(
    'a,h',
    [
        (0, 1),
        (-1, 1),
        (1, 0),
        (1, -1),
        (float('nan'), 1),
        (1, float('inf')),
    ]
)
def test_bad_units(a, h):
    with pytest.raises(ValueError):
        bounds(a, h)


def test_families():
    assert [
        p['id'] for p in families()
    ] == ['M0', 'M1', 'M2', 'M3']

    assert sum(
        'Horndeski' in p['operator']
        for p in families()
    ) == 1


def test_controls():
    r = atlas()

    assert r['negative_controls']['Earth_off'].startswith(
        'no Earth'
    )

    assert r['exact_checked_algebra'][
        'craft_only_false_Earth_force'
    ]


def test_no_claim_upgrade():
    r = atlas()

    assert not r['006D_replaced']
    assert not r['qualified_survivors']
    assert not r['GAMMA1_01_authorized']

    assert (
        r['force_ledger']['whole_craft_up']
        == 'NOT_DERIVED'
    )

    assert (
        r['complete_energy_lt10MJ']
        == 'NOT_CERTIFIED'
    )


def test_gap_assumption_explicit():
    assert 'field stress' in bounds()['not_covered']
    assert 'field stress' in bounds()['premise']
