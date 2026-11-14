"""B17-M2: source-relaxed variational and planar consistency tests."""

import math

import numpy as np
import pytest

from antigravity_research.agminer.hook17_r3b_layer_variational_gate import (
    Layer,
    axial_slab_variational,
    physical_r3b_axial_b,
    stationary_nosource_planar_localization_gate,
    CANONICAL_K_J_PER_M3_PER_FIELD2,
)


def test_equal_theta_ordinary_carrier_energy():
    layers = [
        Layer("a", 0.01, 1.2),
        Layer("b", 0.02, 1.2),
    ]

    result = axial_slab_variational(layers, 5.0, 1000.0)

    expected = (
        0.5
        * CANONICAL_K_J_PER_M3_PER_FIELD2
        * 25.0
        * 0.03
    )

    assert math.isclose(
        result["optimal"]["carrier_energy_j_per_m2"],
        expected,
        rel_tol=1e-12,
    )

    assert all(
        abs(e) < 1e-8
        for e in result["optimal"]["e_normal_per_layer"]
    )


def test_exact_two_layer_variational_minimum():
    layers = [
        Layer("vac", 0.02, 0),
        Layer("matter", 0.01, 1.2),
    ]

    result = axial_slab_variational(
        layers, 13.0, 1000.0,
        fixed_source_e_normal=13.0,
    )

    assert (
        result["optimal"]["carrier_energy_j_per_m2"]
        <
        result["fixed_source"]["carrier_energy_j_per_m2"]
    )

    assert (
        result["optimal"]["absolute_d_continuity_residual"]
        < 1e-9
    )

    assert math.isclose(
        result["analytic_optimum_j_per_m2"],
        result["optimal"]["carrier_energy_j_per_m2"],
        rel_tol=1e-12,
    )


def test_variational_minimum_random_source_displacements():
    layers = [
        Layer("a", 0.012, 0),
        Layer("b", 0.03, 0.00012),
        Layer("c", 0.015, 1.2),
    ]

    result = axial_slab_variational(
        layers, 17.0, 1000.0
    )

    from antigravity_research.agminer.hook17_r3b_earth_interface import (
        theta_for_density,
    )

    theta = np.array([
        theta_for_density(x.density_kg_m3)
        for x in layers
    ])

    lengths = np.array([
        x.thickness_m for x in layers
    ])

    optimum_d = result["optimal"]["source_displacement"]
    optimum_u = result["optimal"]["carrier_energy_j_per_m2"]

    for d in np.linspace(
        optimum_d-3e5,
        optimum_d+3e5,
        41,
    ):
        trial_u = (
            0.5
            * CANONICAL_K_J_PER_M3_PER_FIELD2
            * np.dot(
                lengths,
                (d-theta*17.0)**2 + 17.0**2,
            )
        )

        assert trial_u >= optimum_u-1e-9


def test_layer_permutation_and_field_sign():
    layers = [
        Layer("air", 0.01, 1.2),
        Layer("ground", 0.01, 2000),
    ]

    first = axial_slab_variational(
        layers, 3.0, 1000.0
    )

    second = axial_slab_variational(
        layers[::-1], -3.0, 1000.0
    )

    assert math.isclose(
        first["optimal"]["carrier_energy_j_per_m2"],
        second["optimal"]["carrier_energy_j_per_m2"],
        rel_tol=1e-12,
    )


def test_zero_field_and_source_free_planar_theorem():
    layers = [
        Layer("vac", 0.01, 0),
        Layer("ground", 0.01, 2000),
    ]

    zero = axial_slab_variational(
        layers, 0.0, 1000.0
    )

    assert zero["optimal"]["carrier_energy_j_per_m2"] == 0

    theorem = stationary_nosource_planar_localization_gate(
        True, True
    )

    assert theorem[
        "source_free_planar_fullline_field_zero_proven"
    ]

    assert not theorem[
        "finite_3d_onboard_source_ruled_out"
    ]

    assert not stationary_nosource_planar_localization_gate(
        False, False
    )["source_free_planar_fullline_field_zero_proven"]


def test_input_validation():
    with pytest.raises(ValueError):
        Layer("", 0.01, 0)

    with pytest.raises(ValueError):
        Layer("x", 0, 0)

    with pytest.raises(ValueError):
        Layer("x", 0.01, -1)

    with pytest.raises(ValueError):
        axial_slab_variational(
            [Layer("a", 1, 0)], 1, 1000
        )

    with pytest.raises(ValueError):
        axial_slab_variational(
            [
                Layer("a", 1, 0),
                Layer("b", 1, 2),
            ],
            1,
            -1,
        )


def test_r3b_provenance_and_lift_fail_closed():
    fit = physical_r3b_axial_b(0.05)

    assert math.isclose(
        fit["r3b_preloaded_energy_j"],
        1.5429162116460216,
        rel_tol=0,
        abs_tol=5e-8,
    )

    assert fit["fitted_normal_b_r3b_units"] > 0

    import importlib.util
    import sys
    from pathlib import Path

    simulation = (
        Path(__file__).resolve().parents[2]
        / "simulations"
        / "032h17a12d1r3x3b17_m2_variational_earth_layer.py"
    )

    spec = importlib.util.spec_from_file_location(
        "b17_m2", simulation
    )

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    result = module.run(0.05)

    assert result["whole_craft_force_n"] is None
    assert result["earth_down_force_n"] is None
    assert result["pure_field_lift"] is None

    assert not result[
        "complete_energy_under_10mj_certified"
    ]

    assert not result["006d_replaced"]
