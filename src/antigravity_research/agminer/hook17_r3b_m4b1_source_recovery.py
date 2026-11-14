"""B17-M4B1: compact R3B-aligned source recovery, coupled Earth control.

The original R3B global mirror is the target. Its magnetic A12C
current is projected onto the onboard 2m source region. Its dominant
electric l=1 moment is reconstructed with a smooth, net-neutral
volume charge, entirely inside the same source region.

The amplitude is matched at one exterior axial reference point.
No free Earth-side source is added.

This is NOT an exact reconstruction of all original R3B multipoles,
the B7 10cm source layer, or microscopic source hardware.

Uses R3X1 Lorentzian coupled carrier equations with prescribed,
frozen-density Earth/air material. The coupled fields respond, but
complete source and matter stress-energy is not solved.
"""

from __future__ import annotations

import math
import numpy as np
from scipy.sparse.linalg import spsolve

from .hook17_concurrent_u1_fieldstrength_metric import (
    C_LIGHT_M_S,
    EV_J,
    HBAR_C_EV_M,
    SOURCE_RADIUS_M,
    TARGET_ACCELERATION_M_S2,
)
from .hook17_fdual_f_global_mirror_prefight import (
    fit_exterior_multipoles,
    PRIMARY_FIT_RADIUS_M,
    PRIMARY_LMAX,
)
from .hook17_fdual_f_loaded_payload_homotopy import (
    _a12c_potential_field,
    _construct_global_mirror_phi,
    _build_elliptic_operators,
    _fields_from_potentials,
    _state_diagnostics,
)
from .hook17_f2_strong_payload_loading_rescue import (
    loading_coefficient_z,
)
from .hook17_r3b_m4b_sparse_earth_loading import (
    MaterialGeometry,
    material_density,
    _solve_fixed_sources,
)

BRANCH = "032H17A12D1R3X3B17-M4B1"


def _field_energy(em, field):
    rho = field["rho_grid"]
    h = field["h"]
    squared = sum(
        em[key]**2
        for key in ("e_rho", "e_z", "b_rho", "b_z")
    )
    return (
        0.5 * EV_J / HBAR_C_EV_M
        * float(np.sum(2 * math.pi * rho * h*h * squared))
    )


def _metric_sigma(em, scale_ev):
    dot = (
        em["e_rho"] * em["b_rho"]
        + em["e_z"] * em["b_z"]
    )
    return -2 * HBAR_C_EV_M**2 * dot / scale_ev**4


def _ground_tracer_force(sigma, field, density):
    h = field["h"]
    rho = field["rho_grid"]
    accel = (
        -C_LIGHT_M_S**2
        * np.gradient(sigma, h, axis=0, edge_order=2)
    )
    return float(
        np.sum(2 * math.pi * rho * h*h * density * accel)
    )


def _relative_fields(em, target, selector):
    keys = ("e_rho", "e_z", "b_rho", "b_z")
    lhs = np.stack([em[k][selector] for k in keys])
    rhs = np.stack([target[k][selector] for k in keys])

    electric = (
        np.linalg.norm(lhs[:2] - rhs[:2])
        / np.linalg.norm(rhs[:2])
    )
    magnetic = (
        np.linalg.norm(lhs[2:] - rhs[2:])
        / np.linalg.norm(rhs[2:])
    )
    return float(electric), float(magnetic)


def assemble_original_aligned_source(h):
    """Recover a compact source approximating the original R3B mirror.

    The electric source uses one fixed dipolar radial profile,
    not a source-basis optimization or exact B7 synthesis.
    """

    if not isinstance(h, (int, float)) or not 0.15 <= h <= 0.3:
        raise ValueError("M4B1 uses 0.15m through 0.30m grids")

    field = _a12c_potential_field(float(h))
    h = field["h"]
    rho = field["rho_grid"]
    z = field["z_grid"]
    radius = np.hypot(rho, z)

    fit = fit_exterior_multipoles(
        field, PRIMARY_FIT_RADIUS_M, PRIMARY_LMAX
    )

    phi_reference = _construct_global_mirror_phi(field, fit)
    a_reference = field["a_phi"] / math.sqrt(2.0)

    target_gate = _state_diagnostics(
        phi_reference,
        a_reference,
        field,
        np.zeros_like(rho),
    )

    minimum = float(
        target_gate["minimum_payload_acceleration_m_s2"]
    )
    if minimum <= 0:
        raise ArithmeticError("R3B target outward sign failed")

    factor = math.sqrt(TARGET_ACCELERATION_M_S2 / minimum)
    phi_reference *= factor
    a_reference *= factor

    target_fields = _fields_from_potentials(
        phi_reference, a_reference, rho, h
    )

    operators = _build_elliptic_operators(
        field["rhos"], field["zs"], h
    )

    # Original A12C magnetic shape, with onboard current support.
    magnetic_mask = (
        radius[1:-1, 1:-1] <= SOURCE_RADIUS_M
    ).ravel()

    j_a = (
        operators["k_a"]
        @ a_reference[1:-1, 1:-1].ravel()
    ) * magnetic_mask

    a_recovered = np.zeros_like(rho)
    a_recovered[1:-1, 1:-1] = spsolve(
        operators["k_a"], j_a
    ).reshape(a_recovered[1:-1, 1:-1].shape)

    # Finite-width net-neutral electric dipolar charge.
    rr = radius[1:-1, :-1]
    zz = z[1:-1, :-1]

    shell = (rr >= 1.1) & (rr <= SOURCE_RADIUS_M)
    radial = np.exp(-((rr - 1.62) / 0.28)**2) * shell

    j_phi = (
        zz / np.maximum(rr, 1e-9) * radial
    ).ravel()

    nz = operators["nz_inner"]
    weights = np.tile(
        np.r_[h / 8.0, field["rhos"][1:-1]],
        nz,
    )

    monopole = float(weights @ j_phi)
    correction = radial.ravel()

    j_phi -= (
        monopole / float(weights @ correction)
    ) * correction

    phi_unit = np.zeros_like(rho)
    phi_unit[1:-1, :-1] = spsolve(
        operators["k_phi"], j_phi
    ).reshape(phi_unit[1:-1, :-1].shape)

    electric_unit = _fields_from_potentials(
        phi_unit, np.zeros_like(rho), rho, h
    )

    axis_row = int(
        np.argmin(abs(field["zs"] + 3.0))
    )

    unit_e = float(electric_unit["e_z"][axis_row, 0])
    target_e = float(target_fields["e_z"][axis_row, 0])

    if abs(unit_e) <= 1e-20:
        raise ArithmeticError("Zero axial electric response")

    electric_scale = target_e / unit_e

    j_phi *= electric_scale
    phi_recovered = phi_unit * electric_scale

    recovered_fields = _fields_from_potentials(
        phi_recovered, a_recovered, rho, h
    )

    outer = (
        (radius > 2.4)
        & (radius < 8.5)
        & (rho < 7.0)
    )

    electric_error, magnetic_error = _relative_fields(
        recovered_fields,
        target_fields,
        outer,
    )

    neutrality = (
        abs(float(weights @ j_phi))
        / max(float(weights @ abs(j_phi)), 1e-300)
    )

    if neutrality > 1e-10:
        raise ArithmeticError("Source charge neutrality failed")

    if np.any(j_phi[~shell.ravel()] != 0):
        raise ArithmeticError("Electric source escaped onboard region")

    if np.any(j_a[~magnetic_mask] != 0):
        raise ArithmeticError("Magnetic source escaped onboard region")

    return {
        "field": field,
        "operators": operators,
        "j_phi": j_phi,
        "j_a": j_a,
        "phi0": phi_recovered,
        "a0": a_recovered,
        "target_phi": phi_reference,
        "target_a": a_reference,
        "target_em": target_fields,
        "recovered_em": recovered_fields,
        "fit_rms": float(fit["relative_rms_field_residual"]),
        "original_mirror_target_energy_j":
            _field_energy(target_fields, field),
        "recovered_unloaded_energy_j":
            _field_energy(recovered_fields, field),
        "exterior_electric_relative_l2_error": electric_error,
        "exterior_magnetic_relative_l2_error": magnetic_error,
        "electric_relative_net_charge": neutrality,
        "magnetic_outside_source_count":
            int(np.count_nonzero(j_a[~magnetic_mask])),
        "electric_outside_source_count":
            int(np.count_nonzero(j_phi[~shell.ravel()])),
        "source_electric_npoints": int(np.count_nonzero(j_phi)),
        "source_magnetic_npoints": int(np.count_nonzero(j_a)),
        "synthesized_source_exact_original_r3b": False,
        "synthesized_source_exact_b7_shell": False,
        "source_is_onboard": True,
    }


def run_case(
    h=0.25,
    portal_scale_ev=1000.0,
    include_air=True,
):
    if not math.isfinite(portal_scale_ev) or portal_scale_ev <= 0:
        raise ValueError("Invalid portal scale")

    source = assemble_original_aligned_source(float(h))
    field = source["field"]
    geometry = MaterialGeometry()

    density, earth_fraction = material_density(
        field, geometry, include_air, True
    )

    ground_density = (
        geometry.ground_density_kg_m3 * earth_fraction
    )

    atmosphere_density = (
        density - ground_density
        if include_air
        else np.zeros_like(density)
    )

    theta = 1.0 - loading_coefficient_z(
        density, portal_scale_ev
    )

    # Match UNLOADED metric sigma for the higher-scale comparator.
    # No microscopic current-generation claim follows.
    amplitude = (portal_scale_ev / 1000.0)**2

    base = {
        **source,
        "j_phi": source["j_phi"] * amplitude,
        "j_a": source["j_a"] * amplitude,
    }

    states = {}

    for fraction in (0.0, 1.0):
        state = _solve_fixed_sources(
            base, theta, fraction
        )

        sigma = _metric_sigma(
            state["em"], portal_scale_ev
        )

        states[str(fraction)] = {
            "earth_ground_tracer_force_n":
                _ground_tracer_force(
                    sigma, field, ground_density
                ),
            "atmospheric_tracer_force_n":
                _ground_tracer_force(
                    sigma, field, atmosphere_density
                ),
            "canonical_carrier_energy_j":
                state["carrier_energy_j"],
            "coupled_solver_relative_residual":
                state["residual"],
            "weighted_reciprocity_residual":
                state["relative_weighted_reciprocity"],
            "max_abs_sigma_ground":
                float(np.max(abs(sigma[earth_fraction > 0.3]))),
        }

    unloaded = states["0.0"]["earth_ground_tracer_force_n"]
    loaded = states["1.0"]["earth_ground_tracer_force_n"]

    reference_sigma = _metric_sigma(
        source["target_em"], 1000.0
    )

    reference_force = _ground_tracer_force(
        reference_sigma,
        field,
        ground_density,
    )

    source_keys = (
        "fit_rms",
        "original_mirror_target_energy_j",
        "recovered_unloaded_energy_j",
        "exterior_electric_relative_l2_error",
        "exterior_magnetic_relative_l2_error",
        "electric_relative_net_charge",
        "magnetic_outside_source_count",
        "electric_outside_source_count",
        "source_electric_npoints",
        "source_magnetic_npoints",
        "source_is_onboard",
    )

    return {
        "branch": BRANCH,
        "classification":
            "APPROX_R3B_COMPACT_SOURCE_FIXED_EARTH_BVP_CONTROL",
        "h_m": h,
        "portal_scale_ev": portal_scale_ev,
        "include_air": include_air,
        "source_is_exact_r3b": False,
        "source_is_original_b7": False,
        "source": {
            key: source[key] for key in source_keys
        },
        "r3b_unloaded_target_ground_tracer_n":
            reference_force,
        "recovered_vs_r3b_frozen_tracer_ratio":
            unloaded / reference_force if reference_force else None,
        "states": states,
        "loaded_to_unloaded_tracer_force_ratio":
            loaded / unloaded if unloaded else None,
        "dense_earth_coupled": True,
        "atmosphere_coupled": include_air,
        "source_current_held_fixed": True,
        "complete_source_hardware_realized": False,
        "whole_craft_force_n": None,
        "earth_reaction_stress_derived": False,
        "field_momentum_ledger_closed": False,
        "full_halfspace_solved": False,
        "finite_box_convergence_certified": False,
        "interface_convergence_certified": False,
        "total_operating_energy_j": None,
        "gravity_cancellation": None,
        "pure_field_lift": None,
        "006d_replaced": False,
    }
