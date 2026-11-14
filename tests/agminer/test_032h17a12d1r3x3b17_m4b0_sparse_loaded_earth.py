"""B17-M4B0: source-fixed coupled Earth-loading regression."""

import numpy as np
import pytest

from antigravity_research.agminer.hook17_r3b_m4b_sparse_earth_loading import (
    MaterialGeometry,
    _assemble_baseline,
    _solve_fixed_sources,
    material_density,
    run_case,
)
from antigravity_research.agminer.hook17_r3b_exterior_transmission import (
    normalized_r3b_fit,
)
from antigravity_research.agminer.hook17_f2_strong_payload_loading_rescue import (
    loading_coefficient_z,
)


@pytest.fixture(scope="module")
def baseline():
    return _assemble_baseline(
        0.25,
        normalized_r3b_fit(0.05),
    )


def test_source_compact_and_net_neutral(baseline):
    assert baseline["charge_neutrality_relative"] < 1e-12
    assert not np.any(
        baseline["j_phi"][~baseline["source_mask_phi"]]
    )
    assert not np.any(
        baseline["j_a"][~baseline["source_mask_a"]]
    )
    assert baseline["source_npoints_phi"] > 0
    assert baseline["source_npoints_a"] > 0


def test_source_reconstructs_decoupled_solution(baseline):
    zero = np.zeros_like(baseline["field"]["rho_grid"])
    solved = _solve_fixed_sources(baseline, zero, 0.0)

    np.testing.assert_allclose(
        solved["phi"][1:-1, :-1].ravel(),
        baseline["phi0"],
        rtol=1e-9,
        atol=1e-4,
    )
    np.testing.assert_allclose(
        solved["a"][1:-1, 1:-1].ravel(),
        baseline["a0"],
        rtol=1e-9,
        atol=1e-4,
    )
    assert solved["residual"] < 1e-9


def test_zero_source_yields_zero_fields(baseline):
    source_off = {
        **baseline,
        "j_phi": np.zeros_like(baseline["j_phi"]),
        "j_a": np.zeros_like(baseline["j_a"]),
    }

    density, _ = material_density(
        baseline["field"],
        MaterialGeometry(),
        True,
        True,
    )

    theta = 1.0 - loading_coefficient_z(density, 1000.0)

    state = _solve_fixed_sources(source_off, theta, 1.0)

    assert state["carrier_energy_j"] == 0
    assert np.max(np.abs(state["dot"])) == 0


def test_weighted_correct_lorentzian_action(baseline):
    density, _ = material_density(
        baseline["field"],
        MaterialGeometry(),
        True,
        True,
    )

    theta = 1.0 - loading_coefficient_z(density, 1000.0)
    state = _solve_fixed_sources(baseline, theta, 1.0)

    assert state["relative_weighted_reciprocity"] < 1e-12
    assert state["residual"] < 1e-8


def test_material_geometry_nonoverlap():
    with pytest.raises(ValueError):
        MaterialGeometry(ground_top_relative_z_m=-2)

    with pytest.raises(ValueError):
        MaterialGeometry(ground_depth_m=0)

    with pytest.raises(ValueError):
        MaterialGeometry(enclosure_radius_m=2.03)


def test_material_domains_and_vacuum_enclosure(baseline):
    field = baseline["field"]
    geometry = MaterialGeometry()

    density, fraction = material_density(
        field,
        geometry,
        True,
        True,
    )

    assert np.all(density >= 0)
    assert np.any(density > 1000)
    assert np.any((density > 0.01) & (density < 2))
    assert np.any(fraction > 0.5)

    source_region = (
        np.hypot(
            field["rho_grid"],
            field["z_grid"],
        )
        <= 2.0
    )
    assert np.max(density[source_region]) == 0

    vacuum, _ = material_density(
        field,
        geometry,
        False,
        True,
    )

    assert np.any(vacuum == 0)
    assert np.all(density >= vacuum - 1e-9)


def test_field_flip_redefinition_invariance(baseline):
    density, _ = material_density(
        baseline["field"],
        MaterialGeometry(),
        True,
        True,
    )

    theta = 1.0 - loading_coefficient_z(density, 21147.0)

    original = _solve_fixed_sources(baseline, theta, 1.0)

    flipped = {
        **baseline,
        "j_phi": -baseline["j_phi"],
        "j_a": -baseline["j_a"],
    }

    reversed_state = _solve_fixed_sources(
        flipped,
        theta,
        1.0,
    )

    np.testing.assert_allclose(
        original["dot"],
        reversed_state["dot"],
        rtol=1e-8,
        atol=1e-4,
    )


def test_air_and_ground_are_distinct(baseline):
    field = baseline["field"]
    geometry = MaterialGeometry()

    air, _ = material_density(field, geometry, True, True)
    vacuum, _ = material_density(field, geometry, False, True)

    assert np.max(np.abs(air - vacuum)) > 1


def test_ground_loading_suppresses_tracer_force():
    result = run_case(
        0.25,
        include_air=True,
        portal_scale_ev=1000.0,
    )

    before = result["states"]["0.0"]
    after = result["states"]["1.0"]

    ratio = (
        after["ground_frozen_tracer_force_n"]
        / before["ground_frozen_tracer_force_n"]
    )

    assert abs(ratio) < 1e-3
    assert after["loaded_solve_residual"] < 1e-8
    assert result["constructed_source_is_original_r3b"] is False
    assert result["whole_craft_force_n"] is None


def test_higher_portal_control_does_not_certify_lift():
    result = run_case(
        0.25,
        include_air=True,
        portal_scale_ev=21147.0,
    )

    before = result["states"]["0.0"]
    after = result["states"]["1.0"]

    ratio = (
        after["ground_frozen_tracer_force_n"]
        / before["ground_frozen_tracer_force_n"]
    )

    assert 0.001 < ratio < 0.05
    assert after["carrier_energy_j"] > 1e6
    assert result["gravity_cancellation"] is None
    assert result["pure_antigravity_lift"] is None
    assert result["complete_energy_j"] is None


def test_full_simulation_claims_fail_closed():
    import importlib.util
    import sys
    from pathlib import Path

    path = (
        Path(__file__).resolve().parents[2]
        / "simulations"
        / "032h17a12d1r3x3b17_m4b0_sparse_loaded_earth.py"
    )

    spec = importlib.util.spec_from_file_location(
        "b17_m4b0_sim",
        path,
    )

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    result = module.run(0.25)

    assert result["source_electric_net_charge_relative_residual"] < 1e-12
    assert result["whole_craft_force_n"] is None
    assert result["gravity_cancellation"] is None
    assert result["pure_field_lift"] is None
    assert result["complete_operating_energy_j"] is None
    assert result["loaded_force_grid_convergence_certified"] is False
    assert result["new_control_source_is_exact_r3b"] is False
    assert result["006d_replaced"] is False
