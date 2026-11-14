"""B17-M4B1 source recovery and claim limits."""

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

from antigravity_research.agminer.hook17_r3b_m4b1_source_recovery import (
    assemble_original_aligned_source,
    run_case,
)


@pytest.fixture(scope="module")
def source():
    return assemble_original_aligned_source(0.25)


def test_compact_net_neutral_source(source):
    assert source["electric_relative_net_charge"] < 1e-12
    assert source["electric_outside_source_count"] == 0
    assert source["magnetic_outside_source_count"] == 0
    assert source["source_electric_npoints"] > 0
    assert source["source_magnetic_npoints"] > 0


def test_exterior_field_reproduction(source):
    assert source["exterior_electric_relative_l2_error"] < 0.05
    assert source["exterior_magnetic_relative_l2_error"] < 0.03
    assert source["fit_rms"] < 0.05


def test_original_r3b_not_falsely_replaced(source):
    assert 0.5 < source["recovered_unloaded_energy_j"] < 3.0
    assert source["original_mirror_target_energy_j"] > 0
    assert source["synthesized_source_exact_original_r3b"] is False
    assert source["synthesized_source_exact_b7_shell"] is False


def test_source_off_gives_zero_fields(source):
    from antigravity_research.agminer.hook17_r3b_m4b_sparse_earth_loading import (
        _solve_fixed_sources,
        MaterialGeometry,
        material_density,
    )
    from antigravity_research.agminer.hook17_f2_strong_payload_loading_rescue import (
        loading_coefficient_z,
    )

    density, _ = material_density(
        source["field"],
        MaterialGeometry(),
        True,
        True,
    )

    theta = 1.0 - loading_coefficient_z(density, 1000.0)

    off = {
        **source,
        "j_phi": np.zeros_like(source["j_phi"]),
        "j_a": np.zeros_like(source["j_a"]),
    }

    result = _solve_fixed_sources(off, theta, 1.0)

    assert result["carrier_energy_j"] == 0
    assert np.max(abs(result["dot"])) == 0


def test_original_frozen_tracer_recovered():
    result = run_case(0.25, 1000.0, True)

    assert abs(
        result["recovered_vs_r3b_frozen_tracer_ratio"] - 1
    ) < 0.03

    assert result["source_is_exact_r3b"] is False


def test_1kev_loaded_earth_suppression():
    result = run_case(0.25, 1000.0, True)
    loaded = result["states"]["1.0"]

    assert abs(
        result["loaded_to_unloaded_tracer_force_ratio"]
    ) < 1e-3

    assert loaded["coupled_solver_relative_residual"] < 1e-8
    assert loaded["weighted_reciprocity_residual"] < 1e-12
    assert result["whole_craft_force_n"] is None


def test_higher_scale_does_not_certify_propulsion():
    result = run_case(0.25, 21147.0, True)

    assert (
        result["states"]["1.0"]["canonical_carrier_energy_j"]
        > 1e4
    )

    assert result["gravity_cancellation"] is None
    assert result["pure_field_lift"] is None
    assert result["total_operating_energy_j"] is None


def test_three_grid_source_reconstruction():
    for h in (0.3, 0.25, 0.2):
        source = assemble_original_aligned_source(h)

        assert source["exterior_electric_relative_l2_error"] < 0.06
        assert source["exterior_magnetic_relative_l2_error"] < 0.035
        assert source["electric_relative_net_charge"] < 1e-12


def test_common_source_sign_flip(source):
    from antigravity_research.agminer.hook17_r3b_m4b_sparse_earth_loading import (
        _solve_fixed_sources,
    )

    beta = np.zeros_like(source["field"]["rho_grid"])

    original = _solve_fixed_sources(source, beta, 0.0)

    reversed_source = {
        **source,
        "j_phi": -source["j_phi"],
        "j_a": -source["j_a"],
    }

    reversed_result = _solve_fixed_sources(
        reversed_source, beta, 0.0
    )

    np.testing.assert_allclose(
        original["dot"],
        reversed_result["dot"],
        rtol=1e-9,
        atol=1e-6,
    )


def test_simulation_fails_closed():
    path = (
        Path(__file__).resolve().parents[2]
        / "simulations"
        / "032h17a12d1r3x3b17_m4b1_source_recovery.py"
    )

    spec = importlib.util.spec_from_file_location(
        "b17_m4b1_sim", path
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    result = module.run(0.25)

    assert result["exact_r3b_source_recovered"] is False
    assert result["10cm_b7_shell_resolved"] is False
    assert result["whole_craft_force_n"] is None
    assert result["gravity_cancellation"] is None
    assert result["propellantless_lift"] is None
    assert result["loaded_force_grid_convergence_certified"] is False
    assert result["complete_operating_energy_below_10mj_certified"] is False
    assert result["006d_replaced"] is False
