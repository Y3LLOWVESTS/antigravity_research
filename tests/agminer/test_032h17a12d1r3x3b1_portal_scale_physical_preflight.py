"""Linked portal-scale identity and conservative-claims tests."""
import importlib.util
import math
from pathlib import Path

import pytest

PATH = (
    Path(__file__).resolve().parents[2]
    / "simulations"
    / "032h17a12d1r3x3b1_portal_scale_physical_preflight.py"
)

SPEC = importlib.util.spec_from_file_location("r3x3b1_portal", PATH)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


@pytest.mark.parametrize("t", [1e-7, 1e-6, 5e-6, 1e-5, 1.0])
def test_parameter_identity(t):
    d = MOD.linked_scale(t)
    assert math.isclose(
        d["preloaded_metric_invariant_ratio"],
        1.0, rel_tol=1e-12
    )


@pytest.mark.parametrize("t", [-1.0, 0.0, 2.0, float("nan")])
def test_invalid_scale(t):
    with pytest.raises(ValueError):
        MOD.linked_scale(t)


def test_parity_bulk_restriction():
    result = MOD.parity_bulk_gate()
    assert result["nonlinear_even_sigma_restores_bulk_loading"]
    assert not result["new_compensator_certified"]


def test_loaded_field_not_device():
    result = MOD.run((0.075,), (5e-6,))
    row = result["grids"][0]["rows"][0]

    assert row["outward_everywhere_sampled"]
    assert row["field_only_under_10MJ"]
    assert not result["microscopic_source_realized"]
    assert not result["complete_operating_energy_certified"]
    assert not result["physical_antigravity_model_found"]
