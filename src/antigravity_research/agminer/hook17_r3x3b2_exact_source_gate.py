"""R3X3B2 — exact unbroken-U(1) massive-Dirac source-protection gate.

QUESTION
--------
Can a parity-odd vector/axial source completion furnish an exactly
massless carrier when its static microscopic source is massive Dirac matter?

SCOPE
-----
Local U(1)^n gauge theories; exact unbroken generators; hard Dirac masses
or one-VEV Yukawa masses; nonsingular gauge kinetic normalization.

For a Yukawa term conjugate(psi_L) Phi psi_R, gauge invariance requires

    q_L - q_R = q_Phi.

A surviving massless generator v must obey

    q_Phi . v = 0.

Therefore

    (q_L - q_R) . v = 0.

The axial charge on the surviving generator vanishes. A hard mass gives
q_L = q_R directly.

LIMITATIONS
-----------
This does not exclude composite or nonminimal currents, new geometric
sources, massless matter, or a genuinely independent compensator.

Classical gauge invariance and anomaly cancellation are separate gates.
This module does not prove physical source realization or energy viability.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product


def fr_vec(values):
    return tuple(Fraction(v) for v in values)


def dot(a, b):
    return sum(
        (x * y for x, y in zip(a, b)),
        Fraction(0),
    )


def nullspace(rows, n):
    """Exact rational nullspace of the scalar-VEV charge matrix."""
    a = [list(fr_vec(row)) for row in rows]

    if any(len(row) != n for row in a):
        raise ValueError("VEV charge dimensions differ")

    pivots = []
    r = 0

    for c in range(n):
        p = next(
            (j for j in range(r, len(a)) if a[j][c]),
            None,
        )

        if p is None:
            continue

        a[r], a[p] = a[p], a[r]
        d = a[r][c]
        a[r] = [v / d for v in a[r]]

        for j in range(len(a)):
            if j != r and a[j][c]:
                m = a[j][c]
                a[j] = [
                    x - m * y
                    for x, y in zip(a[j], a[r])
                ]

        pivots.append(c)
        r += 1

    free = [c for c in range(n) if c not in pivots]
    vectors = []

    for f in free:
        v = [Fraction(0)] * n
        v[f] = Fraction(1)

        for i, p in enumerate(pivots):
            v[p] = -a[i][f]

        vectors.append(tuple(v))

    assert all(
        dot(row, vec) == 0
        for row in a
        for vec in vectors
    )

    return tuple(vectors)


def massive_dirac_gate(
    q_l,
    q_r,
    vevs,
    mass_higgs_charge=None,
):
    """Check Dirac mass gauge invariance and surviving axial charges."""
    l = fr_vec(q_l)
    r = fr_vec(q_r)

    if len(l) != len(r) or not l:
        raise ValueError("left/right charge dimensions differ")

    n = len(l)

    h = (
        fr_vec(mass_higgs_charge)
        if mass_higgs_charge is not None
        else (Fraction(0),) * n
    )

    if len(h) != n:
        raise ValueError("Higgs charge dimension mismatch")

    unbroken = nullspace(vevs, n)

    invariant_mass = all(
        l[i] - r[i] == h[i]
        for i in range(n)
    )

    # This implementation accepts a hard mass or a Yukawa mass
    # from one of the explicitly declared condensing scalar VEVs.
    condenses = (
        not any(h)
        or h in tuple(fr_vec(v) for v in vevs)
    )

    invariant_mass = invariant_mass and condenses

    axial = tuple(
        dot(
            tuple(r[i] - l[i] for i in range(n)),
            v,
        ) / 2
        for v in unbroken
    )

    return {
        "number_of_unbroken_u1": len(unbroken),
        "mass_term_gauge_invariant_and_vev_realized":
            invariant_mass,
        "unbroken_basis": [
            [str(x) for x in v]
            for v in unbroken
        ],
        "axial_charges_on_unbroken_basis": [
            str(x) for x in axial
        ],
        "massive_dirac_axial_source_on_unbroken_u1_allowed":
            bool(invariant_mass and any(axial)),
        "unbroken_massive_dirac_vectorlike":
            bool(
                invariant_mass
                and all(x == 0 for x in axial)
            ),
    }


def anomaly_polynomials(chiral_pairs):
    """Exact Abelian cubic and mixed-gravitational anomaly numerators.

    Input: Dirac pairs (q_L vector, q_R vector).

    This is an Abelian anomaly screen only. Mixed anomalies involving
    additional gauge groups require separate tests.
    """
    if not chiral_pairs:
        raise ValueError("must provide fermions")

    pairs = [
        (fr_vec(l), fr_vec(r))
        for l, r in chiral_pairs
    ]

    n = len(pairs[0][0])

    if any(
        len(l) != n or len(r) != n
        for l, r in pairs
    ):
        raise ValueError("charge vector dimensions differ")

    gravitational = tuple(
        sum(
            (l[i] - r[i] for l, r in pairs),
            Fraction(0),
        )
        for i in range(n)
    )

    cubic = {
        ",".join(map(str, inds)): str(
            sum(
                (
                    l[inds[0]] * l[inds[1]] * l[inds[2]]
                    - r[inds[0]] * r[inds[1]] * r[inds[2]]
                    for l, r in pairs
                ),
                Fraction(0),
            )
        )
        for inds in product(range(n), repeat=3)
    }

    return {
        "mixed_gravitational_numerators": [
            str(x) for x in gravitational
        ],
        "abelian_cubic_numerators": cubic,
        "these_abelian_anomalies_cancel":
            all(x == 0 for x in gravitational)
            and all(
                Fraction(x) == 0
                for x in cubic.values()
            ),
        "full_microscopic_anomaly_completion_certified":
            False,
    }


def declared_source_atlas():
    one_axial = massive_dirac_gate(
        [1], [-1], [],
    )

    with_higgs = massive_dirac_gate(
        [1], [-1], [[2]], [2],
    )

    mixed = massive_dirac_gate(
        [1, 0], [0, 1],
        [[1, -1]], [1, -1],
    )

    vector = massive_dirac_gate(
        [2], [2], [],
    )

    assert not one_axial[
        "mass_term_gauge_invariant_and_vev_realized"
    ]

    assert with_higgs["number_of_unbroken_u1"] == 0
    assert mixed["number_of_unbroken_u1"] == 1
    assert mixed["unbroken_massive_dirac_vectorlike"]
    assert vector["unbroken_massive_dirac_vectorlike"]

    return {
        "single_u1_hard_mass_pure_axial": one_axial,
        "single_u1_higgs_generated_pure_axial": with_higgs,
        "two_u1_chiral_higgs_mass_unbroken_vectorlike":
            mixed,
        "vectorlike_massless_source": vector,
        "single_axial_dirac_anomaly":
            anomaly_polynomials([([1], [-1])]),
        "paired_opposite_axial_anomaly":
            anomaly_polynomials([
                ([1], [-1]),
                ([-1], [1]),
            ]),
        "parity_even_cross_topological_algebra":
            "R3X0_ALREADY_CHECKED",
        "cross_topological_micro_source":
            "NOT_CERTIFIED",
        "new_composite_pseudovector_source":
            "OPEN_UNTESTED",
        "new_action_derived_interface_compensator":
            "OPEN_UNTESTED",
        "original_r3b_1p542916_j_preloaded_preserved":
            True,
        "006d_replaced": False,
        "physical_antigravity_model_found": False,
    }
