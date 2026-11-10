"""R3X3B2 — theorem-first source gate and R3X3B1 evidence audit.

Does not change the earlier field results. No BVP is performed.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from antigravity_research.agminer.hook17_r3x3b2_exact_source_gate import (
    declared_source_atlas,
)


def previous_portal_scale_audit(path):
    """Read actual R3X3B1 output; never invent source-energy claims."""
    if not path.exists():
        return {
            "available": False,
            "status": "R3X3B1_JSON_NOT_FOUND",
        }

    data = json.loads(path.read_text())

    if data.get("branch") != (
        "032H17A12D1R3X3B1_LINKED_PORTAL_SCALE_PREFLIGHT"
    ):
        raise ValueError("Unexpected portal-scale source artifact")

    groups = defaultdict(list)

    for grid in data["grids"]:
        for row in grid["rows"]:
            if not row["outward_everywhere_sampled"]:
                continue

            energy = row.get("canonical_field_energy_1g_j")
            amplitude = row.get(
                "required_source_amplitude_vs_1keV"
            )

            if (
                energy is None
                or amplitude is None
                or energy <= 0
                or amplitude <= 0
            ):
                raise ValueError("Invalid field or source scale")

            groups[str(row["t"])].append((
                grid["h_m"],
                energy,
                amplitude,
                row["M_X_keV"],
            ))

    result = {}

    for ratio, points in sorted(
        groups.items(),
        key=lambda kv: float(kv[0]),
    ):
        energies = [p[1] for p in points]
        amplitudes = [p[2] for p in points]

        result[ratio] = {
            "grid_count": len(points),
            "portal_keV": points[0][3],
            "field_energy_min_J": min(energies),
            "field_energy_max_J": max(energies),
            "energy_spread_fraction_of_mean":
                (max(energies) - min(energies))
                / (sum(energies) / len(energies)),
            "source_amplitude_min_vs_reference":
                min(amplitudes),
            "source_amplitude_max_vs_reference":
                max(amplitudes),
            "largest_field_only_budget_remainder_J":
                10_000_000 - max(energies),
            "field_only_under_10MJ_on_listed_grids":
                max(energies) < 10_000_000,
            "microscopic_source_cost_known": False,
            "complete_operating_energy_certified": False,
            "continuum_certified": False,
        }

    return {
        "available": True,
        "by_loading_ratio": result,
    }


def run():
    scale_path = Path(
        "results/data/"
        "032h17a12d1r3x3b1_portal_scale_physical_preflight.json"
    )

    result = {
        "branch": "032H17A12D1R3X3B2",
        "decision":
            "CLOSE_MINIMAL_MASSIVE_DIRAC_AXIAL_U1_SOURCE_ONLY",
        "proof_scope":
            "UNBROKEN_ABELIAN_GAUGE_SYMMETRY_AND_LOCAL_DIRAC_MASS",
        "theorem": declared_source_atlas(),
        "portal_scale_evidence":
            previous_portal_scale_audit(scale_path),
        "new_loaded_bvp_authorized": False,
        "further_physical_source_action_required": True,
        "complete_energy_certified": False,
        "physical_antigravity_model_found": False,
        "006d_replaced": False,
    }

    path = Path(
        "results/data/"
        "032h17a12d1r3x3b2_exact_source_protection_summary.json"
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )

    mixed = result["theorem"][
        "two_u1_chiral_higgs_mass_unbroken_vectorlike"
    ]

    anomaly = result["theorem"][
        "single_axial_dirac_anomaly"
    ]

    print("R3X3B2_DECISION=", result["decision"])
    print(
        "VECTORLIKE_UNBROKEN_THEOREM=",
        mixed["unbroken_massive_dirac_vectorlike"],
    )
    print(
        "AXIAL_SINGLE_DIRAC_ANOMALY_PASS=",
        anomaly["these_abelian_anomalies_cancel"],
    )
    print(
        "PREVIOUS_SCALE_JSON_FOUND=",
        result["portal_scale_evidence"]["available"],
    )
    print("RESULT_PATH=", path)

    return result


if __name__ == "__main__":
    run()
