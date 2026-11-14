"""ALPHA-1R4 / B17-M5I: matched continuum source preflight.

Replace independent grid source arrays with one explicit smooth,
compact, axisymmetric stationary four-current. Deposit the same
source on multiple cylindrical meshes and compare its moments
against independent high-order numerical integration.

The source amplitudes are arbitrary test normalizations.
This run does not solve the loaded field equations, certify
a dynamical source action, produce gravitational lift, or
establish physically available operating energy.

Source:
    B = max(1-((r-R)/a)^2-(z/b)^2, 0)^5
    rho_e = (z/b)*B
    J_phi = B
    J_r = J_z = 0

For a stationary axisymmetric current,
    partial_t rho_e = 0
    div(J) = (1/r)*partial_phi(J_phi) = 0.

The net charge vanishes by odd-z parity. This conservation
identity is not a complete matter-sector Ward certificate.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss


BRANCH = "032H17A12D1R3X3B17-ALPHA1R4-M5I"


@dataclass(frozen=True)
class SourceSpec:
    radial_center_m: float = 1.15
    radial_halfwidth_m: float = 0.42
    axial_halfwidth_m: float = 0.50
    density_amplitude: float = 1.0
    azimuthal_current_amplitude: float = 1.0


def _check_spec(spec):
    values = tuple(asdict(spec).values())

    if not all(math.isfinite(v) for v in values):
        raise ValueError("Nonfinite continuum source")

    if spec.radial_center_m <= spec.radial_halfwidth_m:
        raise ValueError("Source intersects symmetry axis")

    if min(
        spec.radial_halfwidth_m,
        spec.axial_halfwidth_m,
    ) <= 0:
        raise ValueError("Invalid source support")

    bound = math.hypot(
        spec.radial_center_m + spec.radial_halfwidth_m,
        spec.axial_halfwidth_m,
    )

    if bound >= 2.0:
        raise ValueError("Source support exceeds 2 m radius")


def continuum_current(r, z, spec):
    """Evaluate one continuum current at physical coordinates."""
    _check_spec(spec)

    r = np.asarray(r, dtype=float)
    z = np.asarray(z, dtype=float)

    u = (
        (r - spec.radial_center_m)
        / spec.radial_halfwidth_m
    ) ** 2

    v = (z / spec.axial_halfwidth_m) ** 2

    bump = np.maximum(1.0 - u - v, 0.0) ** 5

    rho_e = (
        spec.density_amplitude
        * z / spec.axial_halfwidth_m
        * bump
    )

    j_phi = spec.azimuthal_current_amplitude * bump

    return rho_e, j_phi


def reference_moments(spec, order=160):
    """Independent Gauss integration over physical source support."""
    _check_spec(spec)

    if type(order) is not int or order < 32:
        raise ValueError("Invalid Gauss order")

    nodes, weights = leggauss(order)

    r = (
        spec.radial_center_m
        + spec.radial_halfwidth_m * nodes[:, None]
    )

    z = spec.axial_halfwidth_m * nodes[None, :]

    w = (
        spec.radial_halfwidth_m
        * spec.axial_halfwidth_m
        * weights[:, None]
        * weights[None, :]
    )

    rho_e, j_phi = continuum_current(r, z, spec)

    return {
        "net_charge_integral": float(
            np.sum(2.0 * math.pi * r * rho_e * w)
        ),
        "electric_dipole_z_integral": float(
            np.sum(2.0 * math.pi * r * z * rho_e * w)
        ),
        "magnetic_dipole_z_integral": float(
            np.sum(math.pi * r * r * j_phi * w)
        ),
    }


def deposit(spec, h, subcells=1):
    """Integrate a common source into cylindrical grid cells.

    The cylindrical volume element is 2*pi*r*dr*dz.
    Subcells provide numerical quadrature, not new sources.
    All grids use the same physical domain:
        0 <= r <= 3 m, -3 m <= z <= 3 m.
    """
    _check_spec(spec)

    if h not in (0.25, 0.2, 0.125, 0.1):
        raise ValueError("Unregistered grid spacing")

    if type(subcells) is not int or subcells not in (1, 2, 4):
        raise ValueError("Unregistered cell quadrature")

    nr = int(round(3.0 / h))
    nz = int(round(6.0 / h))

    if (
        abs(nr * h - 3.0) > 1e-12
        or abs(nz * h - 6.0) > 1e-12
    ):
        raise ArithmeticError("Inconsistent physical domain")

    charge_cells = np.zeros((nr, nz), dtype=float)
    current_cells = np.zeros_like(charge_cells)

    absolute_charge = 0.0
    electric_dipole = 0.0
    magnetic_dipole = 0.0
    support_count = 0

    ds = h / subcells

    for i in range(subcells):
        r = (
            np.arange(nr, dtype=float)
            + (i + 0.5) / subcells
        ) * h

        for j in range(subcells):
            z = -3.0 + (
                np.arange(nz, dtype=float)
                + (j + 0.5) / subcells
            ) * h

            rr = r[:, None]
            zz = z[None, :]

            rho_e, j_phi = continuum_current(rr, zz, spec)

            dV = 2.0 * math.pi * rr * ds * ds

            dq = rho_e * dV
            dj = j_phi * dV

            charge_cells += dq
            current_cells += dj

            absolute_charge += float(np.abs(dq).sum())

            electric_dipole += float((zz * dq).sum())

            magnetic_dipole += float(
                (0.5 * rr * dj).sum()
            )

            support_count += int(
                np.count_nonzero(j_phi)
            )

    net_charge = float(charge_cells.sum())

    return {
        "grid_m": h,
        "subcells_per_axis": subcells,
        "source_definition": asdict(spec),
        "coarse_cell_shape": [nr, nz],
        "net_charge_integral": net_charge,
        "absolute_charge_integral": absolute_charge,
        "relative_net_charge": (
            abs(net_charge) / max(absolute_charge, 1e-30)
        ),
        "electric_dipole_z_integral": electric_dipole,
        "magnetic_dipole_z_integral": magnetic_dipole,
        "nonzero_subcell_samples": support_count,
        "azimuthal_current_is_divergence_free_by_symmetry": True,
        "source_continuity_exact_analytically": True,
        "dynamical_source_sector_Ward_certified": False,
    }


def assess(spec=SourceSpec(), provenance=None):
    """Compare a single source on independent grids."""
    _check_spec(spec)

    reference = reference_moments(spec)

    grids = {
        f"h{h}_sub{sub}": deposit(spec, h, sub)
        for h in (0.25, 0.2, 0.125, 0.1)
        for sub in (1, 2, 4)
    }

    for row in grids.values():
        for key, label in (
            (
                "electric_dipole_z_integral",
                "electric_dipole_relative_error",
            ),
            (
                "magnetic_dipole_z_integral",
                "magnetic_dipole_relative_error",
            ),
        ):
            row[label] = (
                abs(row[key] - reference[key])
                / max(abs(reference[key]), 1e-30)
            )

    a = grids["h0.25_sub4"]
    b = grids["h0.2_sub4"]

    comparisons = {}

    for key in (
        "electric_dipole_z_integral",
        "magnetic_dipole_z_integral",
    ):
        comparisons[key] = {
            "relative_crossgrid_difference": (
                abs(a[key] - b[key])
                / max(abs(a[key]), abs(b[key]), 1e-30)
            ),
            "reference_value": reference[key],
            "h0.25_sub4": a[key],
            "h0.2_sub4": b[key],
        }

    historical = None

    if provenance is not None:
        old = json.loads(
            Path(provenance).read_text(encoding="utf-8")
        )

        if old.get("branch") != (
            "032H17A12D1R3X3B17-ALPHA1R3-M5H"
        ):
            raise ValueError("Incorrect M5H provenance input")

        fingerprints = old["source_fingerprints"]

        historical = {
            "historical_original_source_reused": False,
            "historical_raw_precompensation_by_grid": {
                k: fingerprints[k][
                    "compensation_charge_before_raw"
                ]
                for k in (
                    "original_h025",
                    "original_h020",
                )
            },
            "historical_current_weighted_norm_comparison_not_physical": {
                key: {
                    "h0.25_h3weighted_l1": (
                        fingerprints["original_h025"][
                            "array_fingerprints"
                        ][key]["h3_weighted_l1_diagnostic"]
                    ),
                    "h0.2_h3weighted_l1": (
                        fingerprints["original_h020"][
                            "array_fingerprints"
                        ][key]["h3_weighted_l1_diagnostic"]
                    ),
                }
                for key in ("j_phi", "j_a")
            },
        }

    gates = {
        "analytical_net_charge_zero": (
            abs(reference["net_charge_integral"]) < 1e-12
        ),
        "all_deposits_net_neutral_within_1e_minus_12": all(
            row["relative_net_charge"] < 1e-12
            for row in grids.values()
        ),
        "common_source_moments_both_coarse_grids_within_1e_minus_4": all(
            row[key] < 1e-4
            for row in (a, b)
            for key in (
                "electric_dipole_relative_error",
                "magnetic_dipole_relative_error",
            )
        ),
        "coarse_mesh_source_moments_crossgrid_within_1e_minus_4": all(
            comparison["relative_crossgrid_difference"] < 1e-4
            for comparison in comparisons.values()
        ),
        "compact_support_inside_nominal_2m_sphere": True,
        "stationary_axisymmetric_source_continuity_analytic": True,
    }

    return {
        "branch": BRANCH,
        "status": "ANALYTIC_STATIONARY_SOURCE_PREFLIGHT_ONLY",
        "continuum_spec": asdict(spec),
        "source_radial_max_m": (
            spec.radial_center_m + spec.radial_halfwidth_m
        ),
        "conservative_bounding_spherical_radius_m": math.hypot(
            spec.radial_center_m + spec.radial_halfwidth_m,
            spec.axial_halfwidth_m,
        ),
        "reference_high_order_cylindrical_integrals": reference,
        "crossgrid_matching": comparisons,
        "deposits": grids,
        "m5h_provenance_context": historical,
        "diagnostic_gates": gates,
        "same_action_field_solver_replaced_with_matched_source": False,
        "same_action_electromagnetic_matter_energy_certified": False,
        "loaded_payload_response_tested": False,
        "gravity_metric_and_exterior_transmission_derived": False,
        "Earth_craft_reaction_derived": False,
        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
        "original_1g_at_1m_benchmark_reproduced_by_new_source": False,
        "006d_replaced": False,
    }


def main():
    parser = argparse.ArgumentParser(
        description=__doc__
    )

    parser.add_argument(
        "--provenance",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--output",
        type=Path,
        required=True,
    )

    args = parser.parse_args()

    result = assess(provenance=args.provenance)

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    args.output.write_text(
        json.dumps(
            result,
            indent=2,
            allow_nan=False,
        ) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "branch": result["branch"],
        "continuum_spec": result["continuum_spec"],
        "reference": result[
            "reference_high_order_cylindrical_integrals"
        ],
        "crossgrid_matching": result["crossgrid_matching"],
        "diagnostic_gates": result["diagnostic_gates"],
        "same_action_field_solver_replaced_with_matched_source": False,
        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
    }, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
