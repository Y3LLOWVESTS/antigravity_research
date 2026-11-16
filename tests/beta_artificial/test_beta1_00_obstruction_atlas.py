"""BETA1-00 focused mathematical and claim-boundary tests.

15 scoped tests.

Passing does not establish full stability, physical source
realization, Earth/craft reaction, or operating energy.
"""

import sympy as sp

from antigravity_research.beta_artificial.beta1_00_obstruction_atlas import (
    P,
    alpha,
    beta,
    K,
    U,
    E,
    B,
    v,
    portal_quantities,
    local_kinetic_quantities,
    exact_checks,
    gap_atlas,
    scientific_atlas,
)


def test_01_exact_lambda():
    sigma, lm, tr, lam = portal_quantities()

    assert sp.simplify(
        lam - tr * sp.diff(sigma, P)
    ) == 0


def test_02_lambda_P_zero():
    lam = portal_quantities()[3]

    want = (
        -4 * alpha**2 * K
        +4 * beta * K
        -16 * alpha**2 * U
        +8 * beta * U
    )

    assert sp.simplify(
        sp.diff(lam, P).subs(P, 0) - want
    ) == 0


def test_03_weyl_chain():
    assert exact_checks()["Weyl_P_metric_chain"]


def test_04_mixed_epsilon():
    assert exact_checks()["mixed_epsilon_sign"]


def test_05_reciprocal_fields_and_source_variation():
    assert exact_checks()["four_reciprocal_variations"]


def test_06_offshell_phase_ward():
    assert exact_checks()["charged_phase_Ward"]


def test_07_constant_lambda_null():
    atlas = scientific_atlas()

    assert "bulk" in atlas["constant_lambda_null"]


def test_08_aligned_gradient_null():
    atlas = scientific_atlas()

    assert "cross" in atlas["integrability_null"]


def test_09_parity_null():
    assert exact_checks()["parity_and_integrability_nulls"]


def test_10_weak_coupling_order():
    atlas = scientific_atlas()

    assert "O(alpha^2)" in atlas["leading_sigma_order"]
    assert "O(alpha)" in atlas["leading_Y_order"]


def test_11_local_schur_identity():
    assert exact_checks()["reduced_schur"]


def test_12_local_negative_counterexample():
    kin = local_kinetic_quantities()

    assert kin["schur"].subs({
        B: 1,
        v: 1,
        U: 0,
        alpha: 0,
        beta: 1,
    }) == -1


def test_13_healthy_free_limit():
    kin = local_kinetic_quantities()

    assert kin["schur"].subs({
        alpha: 0,
        beta: 0,
    }) == 1

    assert kin["h_vv"] == 1


def test_14_gap_registry_complete():
    rows = gap_atlas()

    assert len(rows) == 7

    assert len({
        row["id"]
        for row in rows
    }) == 7

    assert all(
        row["necessary_condition"]
        and row["falsifier"]
        for row in rows
    )


def test_15_avoid_physical_promotion():
    atlas = scientific_atlas()

    assert atlas["full_constrained_kinetic"] == "NOT_DERIVED"

    assert atlas["physical_earth_craft_force"] == "NOT_DERIVED"

    assert len(exact_checks()) == 8

    assert all(exact_checks().values())
