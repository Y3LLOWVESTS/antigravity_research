"""Focused analytical regression of the R3X3B3 source-energy bound."""

import importlib.util
import math
from pathlib import Path

import pytest


PATH = (
    Path(__file__).resolve().parents[2]
    / "simulations"
    / "032h17a12d1r3x3b3_dipole_source_energy_gate.py"
)

SPEC = importlib.util.spec_from_file_location(
    "r3x3b3_energy_gate",
    PATH,
)

MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


@pytest.mark.parametrize(
    "b",
    [0.0, 1e-8, 1e-3, 0.012, 2.0],
)
def test_nonnegative_bound(b):
    result = MOD.dipole_source_bound(b)

    assert result[
        "electron_sized_dipole_rest_energy_floor_j"
    ] >= 0

    expected = (
        b / (2.0 * MOD.mu_0 / (4.0 * math.pi))
    )

    assert math.isclose(
        result["required_total_dipole_moment_a_m2"],
        expected,
        rel_tol=1e-12,
        abs_tol=1e-12,
    )


@pytest.mark.parametrize(
    "b",
    [-1.0, float("inf"), float("nan")],
)
def test_invalid_field_rejected(b):
    with pytest.raises(ValueError):
        MOD.dipole_source_bound(b)


def test_gap_cubic_scaling():
    a = MOD.dipole_source_bound(0.01, gap_m=1.0)
    b = MOD.dipole_source_bound(0.01, gap_m=2.0)

    ratio = (
        b["electron_sized_dipole_rest_energy_floor_j"]
        / a["electron_sized_dipole_rest_energy_floor_j"]
    )

    assert math.isclose(ratio, 8.0)


def test_electron_sized_source_fails_10mj():
    result = MOD.dipole_source_bound(0.012)

    assert not result[
        "electron_sized_dipole_source_passes_10mj"
    ]

    assert result[
        "required_moment_per_mass_energy_enhancement"
    ] > 1e7

    assert not result[
        "other_microscopic_source_families_excluded"
    ]
