"""R3X2 source-Ward, quadratic-response and decision regressions."""

from __future__ import annotations

import numpy as np

from antigravity_research.agminer.hook17_fdual_f_r3x2_source_cone import (
    BRANCH,
    GRIDS_M,
    SHELL_ORDERS,
    source_ward_gate,
    shell_multipole,
    direct_quadratic_check,
    quadratic_payload_matrices,
    cross_grid_common_source,
    final_decision,
)


def test_branch_and_grid_scope():
    assert BRANCH == "032H17A12D1R3X2"
    assert GRIDS_M == (0.075, 0.050)
    assert SHELL_ORDERS == (1, 2, 3)


def test_shell_net_electric_charge_vanishes():
    gate = source_ward_gate()

    assert gate["net_charge_zero_pass"] is True

    assert all(
        value < 1.0e-12
        for value in gate[
            "net_electric_charge_multipole_flux_residuals"
        ].values()
    )


def test_solenoidal_surface_current_ward():
    gate = source_ward_gate()

    assert gate[
        "azimuthal_surface_current_divergence_zero_by_axisymmetry"
    ] is True

    assert gate[
        "zero_electric_and_magnetic_monopole_source"
    ] is True


def test_microscopic_sources_and_noether_remain_open():
    gate = source_ward_gate()

    assert gate["shell_surface_source_microphysicalized"] is False

    assert gate[
        "independent_axial_gauge_source_and_anomaly_canceled"
    ] is False

    assert gate[
        "full_matter_metric_noether_ward_proven"
    ] is False


def test_shell_multipoles_regular_and_continuous():
    from antigravity_research.agminer.hook17_concurrent_u1_fieldstrength_metric import (
        SOURCE_RADIUS_M,
    )

    radius = float(SOURCE_RADIUS_M)

    coordinates = np.array([
        radius - 1.0e-8,
        radius,
        radius + 1.0e-8,
    ])

    rho, z = np.meshgrid(
        coordinates,
        [0.0, 0.1, 0.2],
    )

    field = {
        "rho_grid": rho,
        "z_grid": z,
    }

    for ell in SHELL_ORDERS:
        phi, a_phi = shell_multipole(
            field,
            ell,
        )

        assert np.isfinite(phi).all()
        assert np.isfinite(a_phi).all()

        assert abs(phi[0, 0] - phi[0, 2]) < 1.0e-6

        assert abs(a_phi[0, 0] - a_phi[0, 2]) < 1.0e-6


def test_legendre_charge_orthogonality():
    nodes, weights = np.polynomial.legendre.leggauss(64)

    for ell in SHELL_ORDERS:
        p = np.polynomial.legendre.Legendre.basis(ell)(
            nodes
        )

        assert abs(np.dot(p, weights)) < 1.0e-12


def test_quadratic_acceleration_and_energy_reconstruction():
    shape = (5, 7)

    rho = np.broadcast_to(
        np.linspace(0.5, 1.0, 7),
        shape,
    )

    z = np.broadcast_to(
        np.linspace(3.0, 3.4, 5)[:, None],
        shape,
    )

    field = {
        "h": 0.1,
        "rho_grid": rho,
        "payload": np.ones(
            shape,
            dtype=bool,
        ),
    }

    setup = {
        "field": field,
    }

    response = {
        "e_r": np.stack([rho, z * 0.1]),
        "e_z": np.stack([z, rho]),
        "b_r": np.stack([0.2 * z, rho]),
        "b_z": np.stack([rho, 0.3 * z]),
    }

    a, energy = quadratic_payload_matrices(
        setup,
        response,
    )

    coeff = np.array([0.4, -0.3])

    result = direct_quadratic_check(
        setup,
        response,
        a,
        energy,
        coeff,
    )

    assert result["pass"] is True

    assert (
        np.linalg.eigvalsh(energy).min()
        > -1.0e-12
    )


def test_cross_grid_requires_actual_candidate():
    grids = [
        {
            "grid_h_m": h,
            "catalogs": {
                "shell_only": {
                    "two_lane_constructive_pass": False,
                },
            },
        }
        for h in GRIDS_M
    ]

    assert cross_grid_common_source(grids)["pass"] is False


def test_no_false_promotion_from_unverified_relaxation():
    grids = [
        {
            "grid_h_m": h,
            "baseline_matches_r3x1": True,
            "physical_sign_loaded_residual": 0.0,
            "catalogs": {
                "shell_only": {
                    "two_lane_constructive_pass": False,
                },
            },
        }
        for h in GRIDS_M
    ]

    outcome = final_decision(
        {"pass": True},
        source_ward_gate(),
        grids,
    )

    assert outcome["decision"].startswith("YELLOW_SCOPED")
    assert outcome["physical_antigravity_model_found"] is False
    assert outcome["006d_replaced"] is False


def test_failed_provenance_requires_hold():
    grids = [
        {
            "baseline_matches_r3x1": True,
            "physical_sign_loaded_residual": 0.0,
        }
        for _ in GRIDS_M
    ]

    outcome = final_decision(
        {"pass": False},
        source_ward_gate(),
        grids,
    )

    assert outcome["decision"].startswith("RED_HOLD")


def test_one_g_and_complete_energy_are_separate_gates():
    grids = [
        {
            "grid_h_m": h,
            "baseline_matches_r3x1": True,
            "physical_sign_loaded_residual": 0.0,
            "catalogs": {
                "shell_only": {
                    "two_lane_constructive_pass": False,
                },
            },
        }
        for h in GRIDS_M
    ]

    outcome = final_decision(
        {"pass": True},
        source_ward_gate(),
        grids,
    )

    assert outcome["complete_energy_established"] is False
    assert outcome["certified_sub10mj_model_found"] is False
    assert outcome["cross_u1_parity_anomaly_completed"] is False
