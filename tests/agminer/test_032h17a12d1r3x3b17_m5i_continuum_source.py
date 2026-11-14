"""ALPHA-1R4/M5I source-conservation regressions."""

import math

import numpy as np
import pytest

from antigravity_research.agminer.hook17_r3b_m5i_continuum_source import (
    SourceSpec,
    assess,
    continuum_current,
    deposit,
    reference_moments,
)


def test_analytic_parity_and_compact_support():
    spec = SourceSpec()

    r = np.asarray([0.8, 1.15, 1.5])

    qpos, jpos = continuum_current(r, 0.12, spec)
    qneg, jneg = continuum_current(r, -0.12, spec)

    assert np.allclose(qpos, -qneg, atol=1e-15)
    assert np.allclose(jpos, jneg, atol=1e-15)

    assert np.allclose(
        continuum_current(0.0, 0.0, spec),
        (0, 0),
    )

    assert np.allclose(
        continuum_current(2.5, 0.0, spec),
        (0, 0),
    )


@pytest.mark.parametrize(
    "h",
    [0.25, 0.2, 0.125, 0.1],
)
def test_source_charge_neutrality_by_odd_parity(h):
    for sub in (1, 2, 4):
        row = deposit(SourceSpec(), h, sub)

        assert row["relative_net_charge"] < 1e-12
        assert row["source_continuity_exact_analytically"]
        assert not row[
            "dynamical_source_sector_Ward_certified"
        ]


def test_independent_integrals_converge_both_grids():
    spec = SourceSpec()
    ref = reference_moments(spec)

    assert abs(ref["net_charge_integral"]) < 1e-12

    for h in (0.25, 0.2):
        value = deposit(spec, h, 4)

        for key in (
            "electric_dipole_z_integral",
            "magnetic_dipole_z_integral",
        ):
            relative_error = (
                abs(value[key] - ref[key])
                / abs(ref[key])
            )

            assert relative_error < 1e-4


def test_refinement_improves_dipole_approximation():
    spec = SourceSpec()
    ref = reference_moments(spec)

    for h in (0.25, 0.2):
        coarse = deposit(spec, h, 1)
        fine = deposit(spec, h, 4)

        for key in (
            "electric_dipole_z_integral",
            "magnetic_dipole_z_integral",
        ):
            assert (
                abs(fine[key] - ref[key])
                < abs(coarse[key] - ref[key])
            )


def test_source_mismatch_negative_control():
    original = SourceSpec()
    changed = SourceSpec(radial_center_m=1.30)

    a = reference_moments(original)
    b = reference_moments(changed)

    for key in (
        "electric_dipole_z_integral",
        "magnetic_dipole_z_integral",
    ):
        difference = (
            abs(a[key] - b[key])
            / abs(a[key])
        )

        assert difference > 0.05


@pytest.mark.parametrize(
    "spec",
    [
        SourceSpec(radial_center_m=0.1),
        SourceSpec(radial_halfwidth_m=-0.1),
        SourceSpec(radial_center_m=1.9),
        SourceSpec(density_amplitude=math.inf),
    ],
)
def test_bad_sources_fail_closed(spec):
    with pytest.raises(ValueError):
        reference_moments(spec)


def test_scope_flags_not_overclaimed():
    result = assess()

    assert all(
        result["diagnostic_gates"].values()
    )

    assert not result[
        "same_action_field_solver_replaced_with_matched_source"
    ]

    assert result["whole_craft_force_n"] is None

    assert not result[
        "gravity_metric_and_exterior_transmission_derived"
    ]

    assert result[
        "complete_operating_energy_j"
    ] is None

    assert not result["006d_replaced"]
