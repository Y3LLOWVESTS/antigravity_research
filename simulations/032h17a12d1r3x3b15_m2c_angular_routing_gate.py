"""B15-M2C — 3D angular interface and momentum-routing preflight.

Uses R3B fitted exterior multipoles, the finite 1 kg torus,
B15-M0 external source geometries, and B15-M2A equal-preloaded-1g
normalizations. This is NOT a fully loaded matter solution.

For the Lorentzian two-U(1) mixed action, in source-free static
space, up to the source-current sign convention:

    j_phi = div(theta B) = grad(theta).B
    j_A = curl(theta E) = grad(theta) x E

For the interface unit normal n:

    E = E_n*n + E_t
    B = B_n*n + B_t

    |grad(theta)| |E.B| <=
        sqrt(E_n**2 + |B_t|**2)
        * sqrt(j_phi**2 + |j_A|**2)

In particular, E=B implies

    j_phi**2 + |j_A|**2 =
        |grad(theta)|**2 * |E|**2

at fixed local field magnitude, regardless of incidence angle.

The topological cross-sector E_X x B_Y is not the canonical
Poynting vector. The original static E_X/B_Y-only construction
has zero same-sector kinetic Poynting flux.

This simulation does not model curved wave propagation,
physical source recoil, 3D reciprocal relaxation, dynamic
stability, or complete operating energy.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
from scipy.special import eval_legendre

from antigravity_research.agminer.hook17_fdual_f_global_mirror_prefight import (
    fit_exterior_multipoles,
    mirror_global_energy_gate,
    mirror_payload_reconstruction,
    reconstruct_a12c_field,
)
from antigravity_research.agminer.hook17_f2_strong_payload_loading_rescue import (
    PRIMARY_DENSITY_MODEL,
    one_ev4_j_m3,
    payload_density_profile_kg_m3,
)
from antigravity_research.agminer.hook17_concurrent_u1_fieldstrength_metric import (
    C_LIGHT_M_S,
    SOURCE_RADIUS_M,
    payload_center_z_m,
)

ROOT = Path(__file__).resolve().parents[1]
BRANCH = "032H17A12D1R3X3B15-M2C"

CONFIG_FILE = (
    ROOT
    / "results/data"
    / "032h17a12d1r3x3b15_orientation_h050_r3b_summary.json"
)

M2A_STEM = "032h17a12d1r3x3b15_m2a_torus_rhs_h"

CONFIGS = (
    "aligned_original",
    "relative_tilt_30deg",
    "relative_tilt_60deg",
    "relative_tilt_90deg",
    "sector_only_electric_90deg",
    "two_sources_perpendicular",
)


def derivative(f, axis, h):
    return (
        np.roll(f, -1, axis=axis)
        - np.roll(f, 1, axis=axis)
    ) / (2.0 * h)


def divergence(v, h):
    return sum(
        derivative(v[..., a], a, h)
        for a in range(3)
    )


def curl(v, h):
    return np.stack(
        (
            derivative(v[..., 2], 1, h)
            - derivative(v[..., 1], 2, h),

            derivative(v[..., 0], 2, h)
            - derivative(v[..., 2], 0, h),

            derivative(v[..., 1], 0, h)
            - derivative(v[..., 0], 1, h),
        ),
        axis=-1,
    )


def gradient(f, h):
    return np.stack(
        [derivative(f, a, h) for a in range(3)],
        axis=-1,
    )


def dot(a, b):
    return np.sum(a * b, axis=-1)


def grid(h):
    if not 0.025 <= h <= 0.15:
        raise ValueError("Require 0.025 <= h <= 0.15 m")

    nx = math.ceil(1.5 / h)
    nz = math.ceil(0.5 / h)

    x = np.arange(-nx, nx + 1) * h
    z = (
        payload_center_z_m()
        + np.arange(-nz, nz + 1) * h
    )

    X, Y, Z = np.meshgrid(
        x, x, z, indexing="ij"
    )

    return np.stack((X, Y, Z), axis=-1)


def material(coords):
    rho = np.hypot(
        coords[..., 0],
        coords[..., 1],
    )

    density = payload_density_profile_kg_m3(
        rho,
        coords[..., 2],
        PRIMARY_DENSITY_MODEL,
    )

    theta = (
        2.0
        * density
        * C_LIGHT_M_S**2
        / one_ev4_j_m3()
        / 1000.0**4
    )

    for axis in range(3):
        boundary = theta.take(
            [0, -1], axis=axis
        )
        if np.any(boundary != 0):
            raise AssertionError(
                "Matter support touches box boundary"
            )

    return density, theta


def legendre_derivative(ell, mu):
    p = eval_legendre(ell, mu)
    prev = eval_legendre(ell - 1, mu)

    result = np.empty_like(mu)
    normal = np.abs(mu) < 1.0 - 1e-10

    result[normal] = (
        ell
        * (prev[normal] - mu[normal] * p[normal])
        / (1.0 - mu[normal] ** 2)
    )

    result[~normal] = (
        ell
        * (ell + 1)
        * 0.5
        * np.where(
            mu[~normal] >= 0,
            1.0,
            (-1.0) ** (ell + 1),
        )
    )

    return result


def multipole_field(coords, coeffs, center, axis):
    """Exterior harmonic field from a rotated net-zero monopole fit."""
    relative = coords - center
    r = np.linalg.norm(relative, axis=-1)

    if np.any(r <= SOURCE_RADIUS_M + 1e-8):
        raise ValueError(
            "Attempted interior source-field evaluation"
        )

    rhat = relative / r[..., None]

    axis = np.asarray(axis, dtype=float)
    axis = axis / np.linalg.norm(axis)

    mu = np.clip(dot(rhat, axis), -1.0, 1.0)
    total = np.zeros_like(coords)

    for ell, amplitude in enumerate(
        coeffs, start=1
    ):
        p = eval_legendre(ell, mu)
        dp = legendre_derivative(ell, mu)

        factor = (
            float(amplitude)
            * (SOURCE_RADIUS_M / r) ** (ell + 1)
            / r
        )

        total += factor[..., None] * (
            ((ell + 1) * p + mu * dp)[..., None]
            * rhat
            - dp[..., None] * axis
        )

    return total


def exterior_fields(coords, sources, coeffs):
    electric = np.zeros_like(coords)
    magnetic = np.zeros_like(coords)

    for source in sources:
        center = np.asarray(
            source["center_m"], dtype=float
        )

        electric += float(source["e_gain"]) * multipole_field(
            coords,
            coeffs,
            center,
            np.asarray(source["electric_axis"], dtype=float),
        )

        magnetic += float(source["b_gain"]) * multipole_field(
            coords,
            coeffs,
            center,
            np.asarray(source["magnetic_axis"], dtype=float),
        )

    return electric, magnetic


def original_amplitudes(reference_h):
    """Recover R3B and its canonical two-sector 1/sqrt(2) split."""
    field = reconstruct_a12c_field(reference_h)

    fitted = fit_exterior_multipoles(
        field, 2.4, 12
    )

    energy = mirror_global_energy_gate(
        field, fitted
    )

    payload = mirror_payload_reconstruction(
        field,
        fitted,
        energy,
    )

    factor = payload[
        "amplitude_squared_normalization_to_1g"
    ]

    if factor is None or factor <= 0:
        raise RuntimeError(
            "R3B normalization not available"
        )

    # The 1/sqrt(2) split is essential. Omitting it
    # makes the M2A norm larger by exactly sqrt(2).
    coeffs = (
        np.asarray(
            fitted["boundary_amplitudes"],
            dtype=float,
        )
        * math.sqrt(factor / 2.0)
    )

    provenance = {
        "reference_h_m": reference_h,
        "original_normalization_amplitude_squared": float(factor),
        "two_sector_amplitude_factor": 1.0 / math.sqrt(2.0),
        "original_r3b_preloaded_field_energy_j": float(
            payload["normalized_mixed_global_field_energy_j"]
        ),
        "exterior_fit_rms": float(
            fitted["relative_rms_field_residual"]
        ),
    }

    return coeffs, provenance


def interface_metrics(theta, electric, magnetic, h):
    g = gradient(theta, h)
    gnorm = np.linalg.norm(g, axis=-1)

    active = gnorm > max(
        float(gnorm.max()) * 1e-7,
        0.0,
    )

    n = np.divide(
        g,
        gnorm[..., None],
        out=np.zeros_like(g),
        where=active[..., None],
    )

    e_normal = dot(electric, n)
    b_normal = dot(magnetic, n)

    e_tangent_squared = np.maximum(
        dot(electric, electric) - e_normal**2,
        0.0,
    )

    b_tangent_squared = np.maximum(
        dot(magnetic, magnetic) - b_normal**2,
        0.0,
    )

    overlap = dot(electric, magnetic)

    projected_phi = dot(g, magnetic)
    projected_a = np.cross(g, electric)

    q_squared = (
        projected_phi**2
        + dot(projected_a, projected_a)
    )

    q_squared = np.where(
        active, q_squared, 0.0
    )

    # Exact Cauchy-Schwarz interface bound.
    lhs = np.abs(gnorm * overlap)

    rhs = (
        np.sqrt(e_normal**2 + b_tangent_squared)
        * np.sqrt(q_squared)
    )

    bound_violation = (
        float(np.max(
            np.maximum(
                lhs[active] - rhs[active],
                0.0,
            )
        ))
        / max(float(np.max(rhs)), 1.0)
        if np.any(active)
        else 0.0
    )

    equal_field_target = (
        gnorm**2
        * dot(electric, electric)
    )

    identity_residual = (
        float(np.sqrt(np.sum(
            (
                q_squared[active]
                - equal_field_target[active]
            )**2
        )))
        / max(
            float(np.sqrt(np.sum(
                equal_field_target[active]**2
            ))),
            1e-300,
        )
    )

    equal_field_residual = (
        float(np.linalg.norm(
            (electric - magnetic)[active]
        ))
        / max(
            float(np.linalg.norm(
                electric[active]
            )),
            1e-300,
        )
    )

    projected_l2 = float(
        np.sqrt(np.sum(q_squared) * h**3)
    )

    # Independently rebuild the M2A discrete
    # Euler-Lagrange inverse-loading current.
    full_phi = divergence(
        theta[..., None] * magnetic,
        h,
    )

    full_a = curl(
        theta[..., None] * electric,
        h,
    )

    full_l2 = float(np.sqrt(
        (
            np.sum(full_phi**2)
            + np.sum(full_a**2)
        ) * h**3
    ))

    product_rule_error = (
        float(np.sqrt(
            np.sum(
                (full_phi - projected_phi)**2
            )
            + np.sum(
                (full_a - projected_a)**2
            )
        ) * h**1.5)
        / max(full_l2, 1e-300)
    )

    net_charge_relative = (
        abs(float(np.sum(full_phi)))
        / max(
            float(np.sum(np.abs(full_phi))),
            1e-300,
        )
    )

    current_div_relative = (
        float(np.linalg.norm(
            divergence(full_a, h)
        ))
        / max(
            float(np.linalg.norm(full_a)) / h,
            1e-300,
        )
    )

    b_normal_part = float(
        np.sum((gnorm * b_normal)**2) * h**3
    )

    e_tangent_part = float(
        np.sum(
            gnorm**2 * e_tangent_squared
        ) * h**3
    )

    normal_fraction = (
        b_normal_part
        / max(
            b_normal_part + e_tangent_part,
            1e-300,
        )
    )

    return {
        "active_interface_cells": int(
            np.count_nonzero(active)
        ),
        "continuum_projector_l2": projected_l2,
        "discrete_inverse_loading_rhs_l2": full_l2,
        "projector_discrete_product_rule_relative_error":
            product_rule_error,
        "current_conservation_relative_residual":
            current_div_relative,
        "net_incremental_charge_relative":
            net_charge_relative,
        "bound_violation_relative":
            bound_violation,
        "equal_field_magnitude_identity_relative_residual":
            identity_residual,
        "electric_equals_magnetic_field_relative_residual":
            equal_field_residual,
        "Bnormal_fraction_of_projected_rhs_squared":
            normal_fraction,
        "Etangent_fraction_of_projected_rhs_squared":
            1.0 - normal_fraction,
        "metric_interface_overlap_weighted_l1":
            float(np.sum(
                gnorm * np.abs(overlap)
            ) * h**3),
        "metric_interface_overlap_signed_z_weighted":
            float(np.sum(
                g[..., 2] * overlap
            ) * h**3),
        "canonical_static_same_sector_poynting_flux":
            0.0,
    }


def evaluate(h, coeffs, geometry, prior_m2a):
    coords = grid(h)
    density, theta = material(coords)

    entries = {}

    for name in CONFIGS:
        sources = geometry[
            "entries"
        ][name]["source_support"]

        if any(
            float(s["exact_support_gap_m"]) < 1.0 - 1e-10
            for s in sources
        ):
            raise AssertionError(
                "Source-support gap below 1 m"
            )

        previous = prior_m2a["modes"][name]

        amplitude_scale = previous[
            "amplitude_scale_to_equal_preloaded_1g"
        ]

        electric, magnetic = exterior_fields(
            coords, sources, coeffs
        )

        if amplitude_scale is not None:
            electric *= float(amplitude_scale)
            magnetic *= float(amplitude_scale)

        row = interface_metrics(
            theta,
            electric,
            magnetic,
            h,
        )

        previous_norm = float(
            previous[
                "combined_induced_E_L_rhs_L2_nonnormalized_units"
            ]
        )

        row[
            "reproduced_m2a_discrete_rhs_relative_error"
        ] = (
            abs(
                row["discrete_inverse_loading_rhs_l2"]
                - previous_norm
            )
            / previous_norm
        )

        row[
            "preloaded_equal_1g_positive_scaling_valid"
        ] = amplitude_scale is not None

        row[
            "minimum_preloaded_az_m_s2_from_m0"
        ] = geometry[
            "entries"
        ][name]["preloaded_min_az_m_s2"]

        row["source_support_gap_m_min"] = min(
            s["exact_support_gap_m"]
            for s in sources
        )

        entries[name] = row

    aligned = entries[
        "aligned_original"
    ]["continuum_projector_l2"]

    for row in entries.values():
        row[
            "angular_projector_ratio_to_aligned"
        ] = (
            row["continuum_projector_l2"]
            / max(aligned, 1e-300)
        )

    return {
        "branch": BRANCH,
        "scope":
            "R3B_EXTERIOR_FROZEN_THETA_INTERFACE_ANGLE_THEOREM_AND_PROJECTOR",
        "h_m": h,
        "payload_mass_numeric_kg": float(
            np.sum(density) * h**3
        ),
        "theta_max": float(np.max(theta)),
        "entries": entries,
        "interface_no_go_local":
            "j_phi=0 and j_A=0 with grad(theta)!=0 implies E.B=0",
        "equal_joint_sector_orientation_no_go_local":
            "for E=B, j_phi^2+|j_A|^2=|grad(theta)|^2|E|^2",
        "local_field_energy_lower_bound_at_fixed_overlap":
            "I^2<=q^2*(S-q^2), q^2=B_n^2+|E_t|^2, S=E^2+B^2",
        "local_energy_premium_lower_bounds_for_angular_loading_reduction": {
            f"{f:.2f}x_current": (
                f**2 + f**(-2)
            ) / 2.0
            for f in (0.5, 0.25, 0.1)
        },
        "mixed_sector_E_cross_B_is_not_physical_poynting_flux":
            True,
        "true_curved_propagation_tested": False,
        "fully_loaded_3d_solved": False,
        "microscopic_source_certified": False,
        "complete_operating_energy_certified": False,
        "006d_replaced": False,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--h", type=float, default=0.075
    )
    parser.add_argument(
        "--reference-h", type=float, default=0.05
    )
    args = parser.parse_args()

    tag = f"{round(args.h * 1000):03d}"

    m2a_path = (
        ROOT
        / "results/data"
        / f"{M2A_STEM}{tag}_r3b_summary.json"
    )

    geometry = json.loads(
        CONFIG_FILE.read_text(encoding="utf-8")
    )

    previous = json.loads(
        m2a_path.read_text(encoding="utf-8")
    )

    coeffs, provenance = original_amplitudes(
        args.reference_h
    )

    result = evaluate(
        args.h, coeffs, geometry, previous
    )

    result[
        "original_r3b_reconstruction_provenance"
    ] = provenance

    output = (
        ROOT
        / "results/data"
        / f"032h17a12d1r3x3b15_m2c_angular_h{tag}_r3b_summary.json"
    )

    output.parent.mkdir(
        parents=True, exist_ok=True
    )

    output.write_text(
        json.dumps(
            result, indent=2, sort_keys=True
        ) + "\n",
        encoding="utf-8",
    )

    print(
        "B15_M2C_INTERFACE_NO_GO=EXACT_LOCAL_ALGEBRA"
    )
    print(
        "B15_M2C_EQUAL_FIELD_ANGLE_NO_GO=EXACT_LOCAL_ALGEBRA"
    )
    print(
        f"PAYLOAD_MASS_KG="
        f"{result['payload_mass_numeric_kg']:.12f}"
    )

    for name, row in result["entries"].items():
        print(
            f"{name:34s} "
            f"ratio={row['angular_projector_ratio_to_aligned']:.8f} "
            f"Bn_fraction="
            f"{row['Bnormal_fraction_of_projected_rhs_squared']:.5f} "
            f"EB_equal_error="
            f"{row['electric_equals_magnetic_field_relative_residual']:.2e} "
            f"M2A_error="
            f"{row['reproduced_m2a_discrete_rhs_relative_error']:.3e} "
            f"product_error="
            f"{row['projector_discrete_product_rule_relative_error']:.4f}"
        )

    print("STATIC_CURVED_REACTION_ROUTING_TESTED=NO")
    print("FULLY_LOADED_3D_SOLVED=NO")
    print("RESULT=", output)


if __name__ == "__main__":
    main()
