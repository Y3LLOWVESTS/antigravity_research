"""B15-M2A — 3D toroidal inverse-loading source-support preflight.

PURPOSE
-------
Use the original R3B exterior multipoles and the actual 1 kg
OPTIMISTIC_FLAT_C1 torus density to determine the incremental
source currents required to hold the preloaded fields fixed.

THEORY
------
Static two-U(1) crossed topological action:

    L = (E_X² + E_Y² - B_X² - B_Y²)/2
        + theta(E_X.B_Y + E_Y.B_X)

R3B mirror: E_X = -grad(phi_X), B_Y = curl(A_Y).

    theta = -beta = 2 rho c² / M⁴

with rho converted to eV^4 and M = 1000 eV.

Incremental Euler-Lagrange source demands, up to overall
source-sign conventions:

    delta_j_phi = div(theta B_Y)
    delta_j_A   = curl(theta E_X)

METHOD
------
Three-dimensional padded Cartesian torus-local box.
Centered periodic differences applied only to compact products
theta*B and theta*E. Those products vanish on every box face.

This avoids spurious nonzero-boundary residuals of the kind
corrected in R3X3B6.

Each eligible orientation is scaled to the SAME sampled
preloaded 1g minimum before current-demand comparison.

OUTPUTS
-------
- Numerically integrated torus mass
- Loading coefficient magnitude
- Incremental charge-current and magnetic-current L2 norms
- Current conservation and integrated net charge
- Relative inverse-loading demand against aligned R3B
- Exact geometric source-to-payload clearance

LIMITATIONS
-----------
Frozen leading-order loading, not full nonlinear matter.
Fitted 3D exterior fields, not the original complete 2D field.
No physical microscopic source realization.
No actual 3D loaded solution.
No source reaction or complete energy.
No loaded repulsion claim.

CLAIM CLASSIFICATION
--------------------
FINITE_TORUS_FROZEN_LOADING_INVERSE_SOURCE_PREFLIGHT
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np

from antigravity_research.agminer.hook17_f2_strong_payload_loading_rescue import (
    PRIMARY_DENSITY_MODEL,
    one_ev4_j_m3,
    payload_density_profile_kg_m3,
)

BRANCH = "032H17A12D1R3X3B15-M2A"
GRAVITY = 9.80665

ROOT = Path(__file__).resolve().parents[1]

M0_FILE = (
    ROOT
    / "simulations"
    / "032h17a12d1r3x3b15_orientation_preflight.py"
)


def load_m0():
    """Load the earlier B15-M0 original-source reconstruction."""
    spec = importlib.util.spec_from_file_location(
        "b15m0_for_m2a",
        M0_FILE,
    )

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    return module


def grid(h: float):
    """Return a padded source-free Cartesian box around the torus."""
    if h <= 0.0 or h > 0.15:
        raise ValueError("0 < h <= 0.15 m required")

    m0 = load_m0()

    nx = math.ceil(1.50 / h)
    nz = math.ceil(0.50 / h)

    x = np.arange(-nx, nx + 1, dtype=float) * h
    y = x.copy()

    z = (
        m0.TORUS_Z
        + np.arange(-nz, nz + 1, dtype=float) * h
    )

    X, Y, Z = np.meshgrid(
        x, y, z,
        indexing="ij",
    )

    return np.stack((X, Y, Z), axis=-1)


def dperiodic(f, axis, h):
    """Centered periodic discrete derivative."""
    return (
        np.roll(f, -1, axis=axis)
        - np.roll(f, 1, axis=axis)
    ) / (2.0 * h)


def div(v, h):
    return sum(
        dperiodic(v[..., a], a, h)
        for a in range(3)
    )


def curl(v, h):
    return np.stack(
        (
            dperiodic(v[..., 2], 1, h)
            - dperiodic(v[..., 1], 2, h),

            dperiodic(v[..., 0], 2, h)
            - dperiodic(v[..., 2], 0, h),

            dperiodic(v[..., 1], 0, h)
            - dperiodic(v[..., 0], 1, h),
        ),
        axis=-1,
    )


def torus_theta(coords):
    """Use the original R3C/R3X1 finite-payload matter normalization."""
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
        * 299792458.0**2
        / one_ev4_j_m3()
        / 1000.0**4
    )

    # Essential boundary-artifact control:
    # the material coefficient is compactly supported
    # away from the padded-box boundary.
    for axis in range(3):
        if np.any(
            theta.take([0, -1], axis=axis)
        ):
            raise ValueError(
                "matter coupling touches padded-box boundary"
            )

    return density, theta


def current_demand(theta, e, b, h):
    """Incremental source RHS from the frozen Lorentzian action."""
    theta_e = theta[..., None] * e
    theta_b = theta[..., None] * b

    return (
        div(theta_b, h),
        curl(theta_e, h),
    )


def l2(values, h):
    """Three-dimensional volume-weighted discrete L2 norm."""
    return float(
        np.sqrt(
            np.sum(np.square(values)) * h**3
        )
    )


def evaluate(h, amplitudes, provenance, modes=None):
    m0 = load_m0()

    coordinates = grid(h)
    density, theta = torus_theta(coordinates)

    payload_samples = m0.torus_points()
    configurations = m0.configurations()

    selected = modes or (
        "aligned_original",
        "relative_tilt_30deg",
        "relative_tilt_60deg",
        "relative_tilt_90deg",
        "sector_only_electric_90deg",
        "two_sources_perpendicular",
    )

    results = {}

    for name in selected:
        sources = configurations[name]

        for source in sources:
            if (
                m0.exact_support_gap(source.center)
                < 1.0 - 1e-10
            ):
                raise RuntimeError(
                    "source-to-payload gap violated"
                )

        preloaded_min = float(
            np.min(
                m0.acceleration_z(
                    payload_samples,
                    sources,
                    amplitudes,
                    step=0.002,
                )
            )
        )

        admissible = preloaded_min > 0.0

        # The field response is quadratic in amplitude.
        # Only positive-everywhere configurations can be
        # rescaled to the same positive sampled 1g floor.
        scale = (
            math.sqrt(GRAVITY / preloaded_min)
            if admissible
            else 1.0
        )

        electric, magnetic = m0.fields(
            coordinates,
            sources,
            amplitudes,
        )

        electric = scale * electric
        magnetic = scale * magnetic

        induced_charge, induced_current = current_demand(
            theta,
            electric,
            magnetic,
            h,
        )

        charge_l2 = l2(induced_charge, h)
        current_l2 = l2(induced_current, h)

        total = math.hypot(
            charge_l2,
            current_l2,
        )

        net_charge_rel = (
            abs(float(np.sum(induced_charge)))
            / max(
                float(np.sum(np.abs(induced_charge))),
                1e-300,
            )
        )

        conserved_current = div(
            induced_current,
            h,
        )

        current_div_rel = (
            l2(conserved_current, h)
            / max(current_l2 / h, 1e-300)
        )

        results[name] = {
            "minimum_preloaded_sampled_axial_acceleration_m_s2":
                preloaded_min,

            "amplitude_scale_to_equal_preloaded_1g":
                scale if admissible else None,

            "equal_preloaded_1g_normalization_admissible":
                admissible,

            "induced_charge_L2_nonnormalized_units":
                charge_l2,

            "induced_current_L2_nonnormalized_units":
                current_l2,

            "combined_induced_E_L_rhs_L2_nonnormalized_units":
                total,

            "incremental_net_charge_relative":
                net_charge_rel,

            "incremental_magnetic_current_divergence_relative":
                current_div_rel,

            "source_support_gap_min_m": min(
                m0.exact_support_gap(s.center)
                for s in sources
            ),

            "physical_external_current_constructed": False,
            "loaded_3d_solved": False,
            "loaded_force_certified": False,
        }

    reference = (
        results.get("aligned_original", {}).get(
            "combined_induced_E_L_rhs_L2_nonnormalized_units"
        )
    )

    if reference and reference > 0.0:
        for item in results.values():
            if item[
                "equal_preloaded_1g_normalization_admissible"
            ]:
                item[
                    "induced_rhs_ratio_to_aligned_at_equal_1g"
                ] = (
                    item[
                        "combined_induced_E_L_rhs_L2_nonnormalized_units"
                    ]
                    / reference
                )
            else:
                item[
                    "induced_rhs_ratio_to_aligned_at_equal_1g"
                ] = None

    return {
        "branch": BRANCH,
        "scope":
            "3D_TORUS_ACTUAL_DENSITY_FROZEN_BETA_INVERSE_LOADING_ONLY",
        "h_m": h,
        "shape": list(coordinates.shape),
        "model_provenance": provenance,

        "payload_mass_numeric_kg": float(
            np.sum(density) * h**3
        ),
        "payload_mass_analytic_kg": 1.0,

        "theta_max_dimensionless": float(
            np.max(theta)
        ),
        "theta_boundary_zero": True,

        "exterior_source_gap_ge_1m": all(
            row["source_support_gap_min_m"] >= 1.0 - 1e-10
            for row in results.values()
        ),

        "incremental_residual_is_frozen_unloaded_field_demand":
            True,

        "source_support_realization": False,
        "loaded_3d_solved": False,
        "same_action_nonlinear_matter_completion": False,
        "complete_energy_certified": False,
        "006d_replaced": False,

        "modes": results,
    }


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--h",
        type=float,
        default=0.075,
    )

    parser.add_argument(
        "--reference-h",
        type=float,
        default=0.05,
    )

    parser.add_argument(
        "--reconstruct",
        action="store_true",
    )

    args = parser.parse_args()
    m0 = load_m0()

    if args.reconstruct:
        amplitudes, provenance = m0.r3b_amplitudes(
            args.reference_h
        )
    else:
        amplitudes = np.array(
            [1.0, 0.25, -0.1]
        )
        provenance = {
            "kind": "SYNTHETIC_TEST_NOT_R3B"
        }

    result = evaluate(
        args.h,
        amplitudes,
        provenance,
    )

    tag = (
        f"h{round(args.h * 1000):03d}_"
        + ("r3b" if args.reconstruct else "synthetic")
    )

    output = (
        ROOT
        / "results"
        / "data"
        / f"032h17a12d1r3x3b15_m2a_torus_rhs_{tag}_summary.json"
    )

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output.write_text(
        json.dumps(
            result,
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )

    print(
        "B15_M2A_MASS_KG",
        result["payload_mass_numeric_kg"],
    )

    print(
        "B15_M2A_THETA_MAX",
        result["theta_max_dimensionless"],
    )

    for name, row in result["modes"].items():
        print(
            f"{name:35s} "
            f"accel="
            f"{row['minimum_preloaded_sampled_axial_acceleration_m_s2']:+.6f} "
            f"rhs_ratio="
            f"{row['induced_rhs_ratio_to_aligned_at_equal_1g']} "
            f"charge_div="
            f"{row['incremental_net_charge_relative']:.2e} "
            f"current_div="
            f"{row['incremental_magnetic_current_divergence_relative']:.2e}"
        )

    print("B15_M2A_LOADED_3D_SOLVED=NO")
    print("RESULT=", output)


if __name__ == "__main__":
    main()
