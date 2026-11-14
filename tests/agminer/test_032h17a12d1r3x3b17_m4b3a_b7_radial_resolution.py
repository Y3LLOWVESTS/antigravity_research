"""B17-M4B3A: guard against unresolved B7 source sampling.

Passing these tests does not establish an Earth-loaded carrier
solution, whole-craft lift or complete operating energy.
"""

import math

import numpy as np
import pytest

from antigravity_research.agminer.hook17_r3b_m4b3a_b7_radial_resolution import (
    expected_moment,
    boundary_moment,
    exact_shell_quadrature,
    split_cell_moment,
    midpoint_moment,
    evaluate,
)
from antigravity_research.agminer.hook17_fdual_f_r3x3b7_finite_charge_shell import (
    radial_profile,
    source_density_proxy,
)


def test_moment_boundary_identity_all_multipoles():
    for ell in range(1, 13):
        assert boundary_moment(ell) == pytest.approx(
            expected_moment(ell), rel=3e-13
        )


def test_direct_charge_quadrature_identity_all_multipoles():
    for ell in range(1, 13):
        assert exact_shell_quadrature(ell) == pytest.approx(
            expected_moment(ell), rel=3e-13
        )


def test_signed_amplitude_redefinition_symmetry():
    for ell in (1, 3, 12):
        a = exact_shell_quadrature(ell, 3.25)
        b = exact_shell_quadrature(ell, -3.25)
        assert a == pytest.approx(-b, rel=1e-12)


def test_source_localization_and_endpoint_matching():
    for ell in (1, 3, 12):
        r = np.array([0.7, 1.8, 2.2, 3.0])

        charge = source_density_proxy(
            ell, 1.0, 2.0, 0.1, r
        )
        assert max(abs(charge)) < 1e-10

        f, fp, _ = radial_profile(
            ell, 1.0, 2.0, 0.1,
            np.array([1.9, 2.0]),
        )

        c = -1 / math.sqrt(2)

        assert f[0] == pytest.approx(
            c * (1.9 / 2)**ell
        )
        assert f[1] == pytest.approx(c)
        assert fp[0] == pytest.approx(
            c * ell / 2 * (.95)**(ell-1)
        )
        assert fp[1] == pytest.approx(
            -c * (ell+1) / 2
        )


def test_coarse_midpoint_misses_shell():
    assert abs(
        midpoint_moment(1, .25) / expected_moment(1)
    ) < 1e-10


def test_grid_phase_alias_is_severe():
    result = evaluate(
        grids=(.30, .25, .05),
        multipoles=(1,),
        phases=(0., .125, .25, .375, .5, .625, .75, .875),
    )

    assert all(
        row["midpoint_max_phase_relative_error"] > .9
        for row in result["rows"]
    )


def test_conservative_moment_across_grids():
    for ell in (1, 3, 12):
        for h in (.30, .25, .20, .10, .05, .025, .02):
            for phase in (0., .125, .375, .625):
                moment, count = split_cell_moment(
                    ell, h, phase
                )

                assert count >= 1
                assert moment == pytest.approx(
                    expected_moment(ell),
                    rel=2e-12,
                )


def test_moment_matching_not_local_convergence():
    result = evaluate(
        grids=(.25, .02),
        multipoles=(1,),
        phases=(0., .5),
    )

    assert all(
        row["source_local_profile_converged"] is False
        for row in result["rows"]
    )
    assert result["source_local_profile_convergence_certified"] is False
    assert result["whole_craft_force_n"] is None


def test_phase_sweep_more_severe_than_one_alignment():
    result = evaluate(
        grids=(.05,),
        multipoles=(1,),
    )

    row = result["rows"][0]
    zero_error = abs(
        row["phases"][0]["midpoint_exterior_moment_ratio"] - 1
    )

    assert zero_error < (
        row["midpoint_max_phase_relative_error"] / 10
    )


def test_invalid_inputs():
    for args in (
        (0, 1., 2., .1),
        (1, 0., 2., .1),
        (1, 1., 2., 0),
        (1, 1., 2., 2.1),
    ):
        with pytest.raises(ValueError):
            boundary_moment(*args)

    for h, phase in (
        (-1, 0),
        (.1, -.1),
        (.1, 1.),
    ):
        with pytest.raises(ValueError):
            midpoint_moment(1, h, phase)


def test_all_device_claims_fail_closed():
    result = evaluate(
        grids=(.25,),
        multipoles=(1, 3),
    )

    assert result["exact_R3B_global_fields_loaded"] is False
    assert result["b7_microscopic_source_realized"] is False
    assert result["whole_craft_force_n"] is None
    assert result["complete_operating_energy_j"] is None
    assert result["006d_replaced"] is False
