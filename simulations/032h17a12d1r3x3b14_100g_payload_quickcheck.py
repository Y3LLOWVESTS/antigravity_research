"""B14 — 100 g payload, original R3B reciprocal static loading.

Compare:
1. Original 1 kg torus.
2. Same torus at 100 g (one-tenth density).
3. Compact ~100 g torus at original material density.

Keep the original R3B external field and portal scale fixed.
Compact-torus results are underresolved on these grids.
No dynamic impulse, source reaction, or device certification.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

from antigravity_research.agminer.hook17_fdual_f_r3c1_validation import (
    _build_baseline_and_prep,
)
from antigravity_research.agminer.hook17_fdual_f_loaded_payload_homotopy import (
    _prepare_low_rank_loaded_system,
    _vectors_to_full_potentials,
    _fields_from_potentials,
)
from antigravity_research.agminer.hook17_fdual_f_r3x1_lorentzian_sign_audit import (
    _solve_loaded,
    _state,
)
from antigravity_research.agminer.hook17_f2_strong_payload_loading_rescue import (
    loading_coefficient_z,
    _flat_c1_profile,
    FLAT_C1_CROSS_SECTION_MEAN,
)
from antigravity_research.agminer.hook17_concurrent_u1_fieldstrength_metric import (
    PAYLOAD_MAJOR_RADIUS_M,
    PAYLOAD_MINOR_RADIUS_M,
    payload_center_z_m,
    SOURCE_RADIUS_M,
    C_LIGHT_M_S,
    REFERENCE_PORTAL_SCALE_EV,
    HBAR_C_EV_M,
)

KAPPA = -2 * HBAR_C_EV_M**2 / REFERENCE_PORTAL_SCALE_EV**4
TARGET_G = 9.80665


def acceleration(fields, h):
    sigma = KAPPA * (
        fields["e_rho"] * fields["b_rho"]
        + fields["e_z"] * fields["b_z"]
    )
    return -C_LIGHT_M_S**2 * np.gradient(
        sigma, h, axis=0, edge_order=2
    )


def run_case(h, mode, setup):
    field = dict(setup["field"])
    rho = field["rho_grid"]
    z = field["z_grid"]

    major = PAYLOAD_MAJOR_RADIUS_M
    minor = PAYLOAD_MINOR_RADIUS_M
    center_z = payload_center_z_m()

    density = setup["density"]
    mask = field["payload"]
    radius = minor
    prep = None

    if mode == "1kg_control":
        prep = setup["prep"]

    elif mode == "100g_same_geometry":
        density = density * 0.1

    elif mode == "100g_compact_same_material_density":
        radius = minor * math.sqrt(0.1)

        s = np.hypot(
            rho - major, z - center_z
        ) / radius

        peak = (
            1.0
            / (2 * math.pi**2 * major * minor**2)
            / FLAT_C1_CROSS_SECTION_MEAN
        )
        density = peak * _flat_c1_profile(s)
        mask = s <= 1.0

    else:
        raise ValueError(mode)

    field["payload"] = mask

    if prep is None:
        beta = -(
            loading_coefficient_z(
                density, REFERENCE_PORTAL_SCALE_EV
            ) - 1.0
        )
        prep = _prepare_low_rank_loaded_system(
            field, setup["phi0"], setup["a0"], beta
        )
    else:
        beta = setup["beta_full"]

    state = dict(
        setup, field=field, prep=prep, density=density
    )

    solution = _solve_loaded(prep, 1.0, 1.0)

    if (
        not solution["success"]
        or solution["relative_residual"] > 1e-8
    ):
        raise RuntimeError(
            f"Loaded solve failed: {mode} h={h}"
        )

    diagnostics = _state(state, solution)

    phi, a = _vectors_to_full_potentials(
        prep, field, setup["phi0"], setup["a0"],
        solution,
    )

    loaded_fields = _fields_from_potentials(
        phi, a, rho, h
    )
    original_fields = _fields_from_potentials(
        setup["phi0"], setup["a0"], rho, h
    )

    loaded_a = acceleration(loaded_fields, h)
    original_a = acceleration(original_fields, h)

    volume = 2 * math.pi * rho * h*h
    mass = float(np.sum(volume * density))
    active = mask & (density > 0)

    com = float(
        np.sum(volume * density * loaded_a) / mass
    )
    pre_com = float(
        np.sum(volume * density * original_a) / mass
    )

    worst = float(np.min(loaded_a[active]))
    gap = (
        math.hypot(major, center_z)
        - radius - SOURCE_RADIUS_M
    )

    return {
        "grid_m": h,
        "case": mode,
        "mass_kg": mass,
        "minor_radius_m": radius,
        "stand_off_m": gap,
        "payload_samples": int(np.count_nonzero(mask)),
        "peak_loading": float(np.max(np.abs(beta))),
        "preloaded_min_m_s2": float(
            np.min(original_a[active])
        ),
        "preloaded_com_m_s2": pre_com,
        "loaded_min_m_s2": worst,
        "loaded_com_m_s2": com,
        "negative_samples": int(
            np.count_nonzero((loaded_a < 0) & active)
        ),
        "field_energy_j": float(
            diagnostics["canonical_field_energy_j"]
        ),
        "loaded_solver_residual": float(
            solution["relative_residual"]
        ),
        "everywhere_1g": bool(worst >= TARGET_G),
        "underresolved_compact_cross_section": bool(
            mode == "100g_compact_same_material_density"
            and radius / h < 3.0
        ),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--grids",
        nargs="+",
        type=float,
        default=[0.075, 0.05, 0.04],
    )
    parser.add_argument(
        "--compact",
        action="store_true",
    )
    args = parser.parse_args()

    results = []

    for h in args.grids:
        # Build the expensive original R3B background ONCE.
        setup = _build_baseline_and_prep(h)

        cases = [
            "1kg_control",
            "100g_same_geometry",
        ]

        if args.compact:
            cases.append(
                "100g_compact_same_material_density"
            )

        for case in cases:
            row = run_case(h, case, setup)
            results.append(row)

            print(
                f"h={h:.3f} {case} "
                f"mass={row['mass_kg']:.5f}kg "
                f"COM={row['loaded_com_m_s2']:+.6f} "
                f"worst={row['loaded_min_m_s2']:+.6f} "
                f"E={row['field_energy_j']:.6f}J "
                f"samples={row['payload_samples']}",
                flush=True,
            )

    path = Path(
        "results/data/"
        "032h17a12d1r3x3b14_100g_payload_quickcheck.json"
    )
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(
            {
                "branch": "032H17A12D1R3X3B14",
                "scope": "STATIC_RECIPROCAL_LOADED_R3B",
                "physical_device_certified": False,
                "results": results,
            },
            indent=2,
        ) + "\n",
        encoding="utf-8",
    )

    print("SUMMARY=", path)


if __name__ == "__main__":
    main()
