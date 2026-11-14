"""ALPHA-1R6/M5K source-adapter unit tests.

These tests establish numerical deposition only. The actual coupled
field and Earth-loading runs are executed by the M5K simulation.
"""

from types import SimpleNamespace

import numpy as np
import pytest

from antigravity_research.agminer.hook17_r3b_m5i_continuum_source import (
    SourceSpec,
)

from antigravity_research.agminer.hook17_r3b_m5k_matched_coupling import (
    build_matched_source,
)


def fake_operator_base(h):
    rhos = np.arange(0.0, 3.0 + 0.5*h, h)
    zs = np.arange(-3.0, 3.0 + 0.5*h, h)
    rho_grid, z_grid = np.meshgrid(rhos, zs)

    n_phi = (len(zs) - 2) * (len(rhos) - 1)
    n_a = (len(zs) - 2) * (len(rhos) - 2)

    return {
        "field": {
            "h": h,
            "rhos": rhos,
            "zs": zs,
            "rho_grid": rho_grid,
            "z_grid": z_grid,
        },
        "operators": {
            "nz_inner": len(zs) - 2,
            "k_phi": SimpleNamespace(
                shape=(n_phi, n_phi)
            ),
            "k_a": SimpleNamespace(
                shape=(n_a, n_a)
            ),
        },
        "j_phi": np.zeros(n_phi),
        "j_a": np.zeros(n_a),
    }


@pytest.mark.parametrize("h", (0.25, 0.2))
def test_matched_native_dimensions_and_neutrality(h):
    base = fake_operator_base(h)
    source, audit = build_matched_source(base)

    assert source["j_phi"].shape == base["j_phi"].shape
    assert source["j_a"].shape == base["j_a"].shape
    assert audit["relative_net_charge_residual"] < 1e-10
    assert audit["electric_dipole_reference_relative_error"] < 1e-4
    assert audit["magnetic_dipole_reference_relative_error"] < 1e-4


@pytest.mark.parametrize("h", (0.25, 0.2))
def test_fixed_amplitude_is_linear(h):
    base = fake_operator_base(h)

    first, _ = build_matched_source(
        base, amplitude=1.0e6
    )

    second, _ = build_matched_source(
        base, amplitude=2.0e6
    )

    assert np.allclose(
        second["j_phi"],
        2 * first["j_phi"],
    )

    assert np.allclose(
        second["j_a"],
        2 * first["j_a"],
    )


@pytest.mark.parametrize("h", (0.25, 0.2))
def test_magnetic_reversal_preserves_electric_source(h):
    base = fake_operator_base(h)

    original, _ = build_matched_source(
        base, SourceSpec()
    )

    reversed_source, _ = build_matched_source(
        base,
        SourceSpec(
            azimuthal_current_amplitude=-1.0
        ),
    )

    assert np.allclose(
        original["j_phi"],
        reversed_source["j_phi"],
    )

    assert np.allclose(
        original["j_a"],
        -reversed_source["j_a"],
    )


def test_different_continuum_geometry_is_detected():
    base = fake_operator_base(0.25)

    original, _ = build_matched_source(
        base, SourceSpec()
    )

    altered, _ = build_matched_source(
        base,
        SourceSpec(radial_center_m=1.30),
    )

    assert not np.allclose(
        original["j_phi"],
        altered["j_phi"],
    )

    assert not np.allclose(
        original["j_a"],
        altered["j_a"],
    )


@pytest.mark.parametrize(
    "amplitude",
    (0.0, -1.0, float("nan")),
)
def test_invalid_amplitudes_rejected(amplitude):
    with pytest.raises(ValueError):
        build_matched_source(
            fake_operator_base(0.25),
            amplitude=amplitude,
        )


def test_test_source_carries_no_physical_certification():
    _, audit = build_matched_source(
        fake_operator_base(0.25)
    )

    assert audit[
        "rhs_not_fitted_to_inverse_R3B_target"
    ]

    assert not audit[
        "discrete_dynamical_Ward_certified"
    ]

    assert not audit[
        "physical_source_unit_conversion_certified"
    ]
