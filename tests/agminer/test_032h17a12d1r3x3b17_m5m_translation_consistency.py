"""ALPHA-1R8/M5M action conversion and source translation tests."""

from types import SimpleNamespace

import numpy as np
import pytest

from antigravity_research.agminer.hook17_r3b_m5i_continuum_source import (
    SourceSpec,
)
from antigravity_research.agminer.hook17_r3b_m5k_matched_coupling import (
    build_matched_source,
)
from antigravity_research.agminer.hook17_r3b_m5m_translation_consistency import (
    carrier_action_conversion_j_per_native,
    redeposit_shifted_source,
)


def fake_base(h):
    rhos = np.arange(
        0.0, 3.0+h/2, h
    )

    zs = np.arange(
        -3.0, 3.0+h/2, h
    )

    n_phi = (
        (len(zs)-2)*(len(rhos)-1)
    )

    n_a = (
        (len(zs)-2)*(len(rhos)-2)
    )

    return {
        "field": {
            "h": h,
            "rhos": rhos,
            "zs": zs,
        },
        "operators": {
            "nz_inner": len(zs)-2,
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


@pytest.mark.parametrize(
    "h,native,expected",
    [
        (
            0.25,
            -24286069720261.0,
            -7.74356675721674,
        ),
        (
            0.2,
            -34900617769646.0,
            -7.121916830326882,
        ),
        (
            0.25,
            -24470971533051.0,
            -7.802522345642956,
        ),
    ],
)
def test_native_action_conversion(
    h, native, expected
):
    actual = (
        native
        * carrier_action_conversion_j_per_native(h)
    )

    assert actual == pytest.approx(
        expected, abs=1e-8
    )


@pytest.mark.parametrize(
    "h", (0.25, 0.2)
)
def test_zero_shift_reproduces_M5K_rhs(h):
    base = fake_base(h)

    original, _ = build_matched_source(
        base, SourceSpec(), order=6
    )

    moved, audit = redeposit_shifted_source(
        base, SourceSpec(), 0.0
    )

    for key in ("j_phi", "j_a"):
        assert np.allclose(
            moved[key],
            original[key],
            rtol=1e-12,
            atol=1e-9,
        )

    assert audit[
        "projected_relative_net_charge"
    ] < 1e-12


@pytest.mark.parametrize(
    "h", (0.25, 0.2)
)
def test_redeposit_moves_continuum_source(h):
    base = fake_base(h)

    centered, _ = redeposit_shifted_source(
        base, SourceSpec(), 0.0
    )

    plus, a = redeposit_shifted_source(
        base, SourceSpec(), 0.002
    )

    minus, b = redeposit_shifted_source(
        base, SourceSpec(), -0.002
    )

    assert a["raw_relative_net_charge"] > 0

    assert a[
        "projected_relative_net_charge"
    ] < 1e-12

    assert b[
        "projected_relative_net_charge"
    ] < 1e-12

    assert a[
        "quadrature_correction_relative_to_density_amplitude"
    ] < 1e-4

    assert not np.array_equal(
        centered["j_phi"], plus["j_phi"]
    )

    assert not np.array_equal(
        centered["j_phi"], minus["j_phi"]
    )

    assert a[
        "electric_dipole_before_projection"
    ] == pytest.approx(
        b["electric_dipole_before_projection"],
        rel=1e-8,
    )


def test_magnetic_reversal():
    base = fake_base(0.25)

    normal, _ = redeposit_shifted_source(
        base, SourceSpec(), 0.001
    )

    reversed_source, _ = redeposit_shifted_source(
        base,
        SourceSpec(
            azimuthal_current_amplitude=-1.0
        ),
        0.001,
    )

    assert np.allclose(
        normal["j_phi"],
        reversed_source["j_phi"],
    )

    assert np.allclose(
        normal["j_a"],
        -reversed_source["j_a"],
    )


@pytest.mark.parametrize(
    "shift",
    (0.011, -0.011, float("nan")),
)
def test_invalid_translation_fails_closed(shift):
    with pytest.raises(ValueError):
        redeposit_shifted_source(
            fake_base(0.25),
            SourceSpec(),
            shift,
        )


@pytest.mark.parametrize(
    "h",
    (0.0, -1.0, float("nan")),
)
def test_invalid_action_conversion_fails_closed(h):
    with pytest.raises(ValueError):
        carrier_action_conversion_j_per_native(h)
