"""B17-M5T: same-functional cell-material tests."""

import numpy as np
import pytest

from antigravity_research.agminer import (
    hook17_r3b_m5t_variational_cell_material as m,
)


def test_legacy_codebundle_provenance():
    assert (
        m.validate_legacy_provenance()
        == m.EXPECTED_PARENT_SHA256
    )


@pytest.mark.parametrize("profile", ["c1", "c2"])
@pytest.mark.parametrize(
    "x",
    [-.3, -.17, -.01, .07, .21, .3],
)
def test_smoothstep_edge_derivative(profile, x):
    delta = 1.e-6

    fraction, predicted = m.f_and_dedge(
        np.array([x]),
        0.0,
        .25,
        profile,
    )

    plus = m.f_and_dedge(
        np.array([x]),
        delta,
        .25,
        profile,
    )[0]

    minus = m.f_and_dedge(
        np.array([x]),
        -delta,
        .25,
        profile,
    )[0]

    assert 0.0 <= fraction.item() <= 1.0

    assert predicted.item() == pytest.approx(
        ((plus-minus)/(2.0*delta)).item(),
        abs=3.e-9,
    )


@pytest.mark.parametrize("profile", ["c1", "c2"])
def test_density_coordinate_variations(profile):
    r = np.array([
        [1.9, 2.3],
        [1.6, 2.7],
    ])

    z = np.array([
        [-3.15, -2.9],
        [-2.1, -1.0],
    ])

    geometry = m.MaterialGeometry()
    delta = 1.e-5

    _, earth_derivative, craft_derivative = (
        m.geometry_at(
            r, z, 0.0, 0.0,
            profile, .5, geometry, True,
        )
    )

    earth_plus = m.geometry_at(
        r, z, delta, 0.0,
        profile, .5, geometry, True,
    )[0]

    earth_minus = m.geometry_at(
        r, z, -delta, 0.0,
        profile, .5, geometry, True,
    )[0]

    craft_plus = m.geometry_at(
        r, z, 0.0, delta,
        profile, .5, geometry, True,
    )[0]

    craft_minus = m.geometry_at(
        r, z, 0.0, -delta,
        profile, .5, geometry, True,
    )[0]

    assert np.max(np.abs(
        (earth_plus-earth_minus)/(2.0*delta)
        - earth_derivative
    )) < 1.e-5

    assert np.max(np.abs(
        (craft_plus-craft_minus)/(2.0*delta)
        - craft_derivative
    )) < 1.e-5

    _, noearth_derivative, _ = m.geometry_at(
        r, z, 0.0, 0.0,
        profile, .5, geometry, False,
    )

    assert not np.any(noearth_derivative)


def test_cylindrical_cell_material_derivative():
    base = m.assemble_original_aligned_source(.25)

    for profile, width in (
        ("c1", .25),
        ("c2", .5),
    ):
        _, analytic_earth, analytic_craft = (
            m.dual_cell_beta(
                base,
                profile=profile,
                width=width,
                order=8,
            )
        )

        delta = 1.e-4

        earth_plus = m.dual_cell_beta(
            base,
            earth=delta,
            profile=profile,
            width=width,
            order=8,
        )[0]

        earth_minus = m.dual_cell_beta(
            base,
            earth=-delta,
            profile=profile,
            width=width,
            order=8,
        )[0]

        craft_plus = m.dual_cell_beta(
            base,
            craft=delta,
            profile=profile,
            width=width,
            order=8,
        )[0]

        craft_minus = m.dual_cell_beta(
            base,
            craft=-delta,
            profile=profile,
            width=width,
            order=8,
        )[0]

        assert np.max(np.abs(
            (earth_plus-earth_minus)/(2.0*delta)
            - analytic_earth
        )) < 2.e-5

        assert np.max(np.abs(
            (craft_plus-craft_minus)/(2.0*delta)
            - analytic_craft
        )) < 2.e-5

        _, noearth, _ = m.dual_cell_beta(
            base,
            profile=profile,
            width=width,
            order=8,
            earth_present=False,
        )

        assert np.array_equal(
            noearth,
            np.zeros_like(noearth),
        )


def test_separately_resolved_action_derivatives():
    result = m.evaluate(
        h=.25,
        profile="c2",
        width=.5,
        order=8,
        step=1.e-4,
    )

    assert result[
        "maximum_abs_disagreement_j_m"
    ] < .002

    assert result["numerical_residuals"][
        "stationarity"
    ] < 1.e-8

    assert result["numerical_residuals"][
        "weighted_asymmetry"
    ] < 1.e-10

    for term in ("earth", "craft", "common"):
        assert abs(result[
            "finite_minus_analytic_j_m"
        ][term]) < .002

    assert not result[
        "M5P_exterior_boundary_reproduced"
    ]

    assert not result[
        "whole_spacecraft_force_derived"
    ]


def test_zero_source_control():
    result = m.evaluate(
        h=.25,
        profile="c2",
        width=.5,
        order=8,
        step=1.e-4,
        zero_source=True,
    )

    assert result["interaction_action_j"] == 0.0

    for term in ("earth", "craft", "common"):
        assert result[
            "same_functional_analytic_j_m"
        ][term] == 0.0

        assert result[
            "finite_difference_j_m"
        ][term] == 0.0


def test_manifest_and_registration():
    quick = m.manifest("quick")
    full = m.manifest("full")

    assert len(quick) == 3
    assert len(full) == 21

    assert all(
        item in full for item in quick
    )

    assert len({
        str(item) for item in full
    }) == 21
