"""R3X3B12 — Frozen R3B intensity and displaced axial source preflight.

OBJECTIVE
---------
1. Separate doubling/tripling the canonical *energy* from doubling/
   tripling the electromagnetic *amplitude*. Verify quadratic scaling.
2. Test coherent two-source combinations with different axial centers
   and relative sign choices for the two source sectors.
3. Compare unloaded and reciprocally loaded finite-torus force, energy,
   inward acceleration, 1-meter standoff and grid sensitivity.

PHYSICAL LIMITS
---------------
The 2D axisymmetric solver supports axial displacements, not arbitrary
3D tilts. Shifted sources are grid-shifted R3B potential backgrounds,
with zero extension at the distant outer numerical boundary.

They are NOT new certified microscopic sources. Overlapping source
spheres are not two independently housed devices. Boundary-source
artifacts are not independently eliminated here.

No new time evolution, source reaction, complete energy, propulsion
or certified antigravity is claimed.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from antigravity_research.agminer.hook17_concurrent_u1_fieldstrength_metric import (
    C_LIGHT_M_S,
    EV_J,
    HBAR_C_EV_M,
    PAYLOAD_MAJOR_RADIUS_M,
    PAYLOAD_MINOR_RADIUS_M,
    REFERENCE_PORTAL_SCALE_EV,
    SOURCE_RADIUS_M,
    TARGET_ACCELERATION_M_S2,
    payload_center_z_m,
)
from antigravity_research.agminer.hook17_fdual_f_r3c1_validation import (
    _build_baseline_and_prep,
)
from antigravity_research.agminer.hook17_fdual_f_r3x1_lorentzian_sign_audit import (
    _solve_loaded,
)
from antigravity_research.agminer.hook17_fdual_f_loaded_payload_homotopy import (
    _fields_from_potentials,
    _vectors_to_full_potentials,
)

BRANCH = "032H17A12D1R3X3B12"
GRIDS_M = (0.075, 0.05, 0.04)
OFFSETS_M = (-0.6, -1.2, -4.2)

REFERENCE_R3B_J = 1.5429162116460216

KAPPA = (
    -2.0 * HBAR_C_EV_M**2
    / REFERENCE_PORTAL_SCALE_EV**4
)


def translated(array, dz, h):
    """Translate a source potential by exact integer grid cells."""
    cells_float = dz / h
    cells = int(round(cells_float))

    if not math.isclose(
        cells_float, cells, abs_tol=1e-8
    ):
        raise ValueError("Non-grid-aligned shift")

    if cells >= 0:
        raise ValueError("Only negative axial shifts allowed")

    n = -cells

    result = np.zeros_like(array)
    result[:-n, :] = array[n:, :]

    return result


def stand_off(dz):
    """Minimum sphere-to-toroidal-payload surface gap."""
    return (
        math.hypot(
            PAYLOAD_MAJOR_RADIUS_M,
            payload_center_z_m() - dz,
        )
        - PAYLOAD_MINOR_RADIUS_M
        - SOURCE_RADIUS_M
    )


def diagnostics(setup, phi, a):
    """Recompute metric acceleration and canonical field inventory."""
    f = setup["field"]
    h = float(f["h"])

    em = _fields_from_potentials(
        phi, a, f["rho_grid"], h
    )

    sigma = KAPPA * (
        em["e_rho"] * em["b_rho"]
        + em["e_z"] * em["b_z"]
    )

    acceleration = (
        -C_LIGHT_M_S**2
        * np.gradient(
            sigma, h, axis=0, edge_order=2
        )
    )

    volume = (
        2.0 * math.pi
        * f["rho_grid"] * h*h
    )

    weights = volume * setup["density"]
    mass = float(np.sum(weights))

    positive = float(np.sum(
        weights * np.maximum(acceleration, 0.0)
    ))

    negative = float(np.sum(
        weights * np.minimum(acceleration, 0.0)
    ))

    energy_density_twice = sum(
        em[key]**2
        for key in (
            "e_rho", "e_z", "b_rho", "b_z"
        )
    )

    energy = (
        0.5
        * float(np.sum(
            volume * energy_density_twice
        ))
        * EV_J / HBAR_C_EV_M
    )

    mask = f["payload"]

    return {
        "energy_j": float(energy),
        "com_m_s2": (positive + negative)/mass,
        "minimum_m_s2":
            float(np.min(acceleration[mask])),
        "maximum_m_s2":
            float(np.max(acceleration[mask])),
        "positive_force_n": positive,
        "negative_force_n": negative,
        "negative_sample_count": int(
            np.count_nonzero(acceleration[mask] < 0)
        ),
        "mass_kg": mass,
        "payload_sample_count": int(
            np.count_nonzero(mask)
        ),
    }


def loaded_solve(setup, phi0, a0):
    """Solve corrected Lorentzian reciprocal static loading.

    Reuse the original density-dependent operator and its
    precomputed Green blocks; update both background source
    vectors and the associated coupling right-hand sides.
    """
    base = setup["prep"]
    prep = dict(base)

    prep["phi0_vec"] = (
        phi0[1:-1, :-1].reshape(-1)
    )

    prep["a0_vec"] = (
        a0[1:-1, 1:-1].reshape(-1)
    )

    prep["c_a0"] = np.asarray(
        base["c_active"] @ prep["a0_vec"]
    ).reshape(-1)

    prep["d_phi0"] = np.asarray(
        base["d_active"] @ prep["phi0_vec"]
    ).reshape(-1)

    solution = _solve_loaded(
        prep, 1.0, 1.0
    )

    if (
        not solution["success"]
        or solution["relative_residual"] > 1e-8
    ):
        raise RuntimeError(
            f"Loaded solve failed: {solution}"
        )

    phi, a = _vectors_to_full_potentials(
        prep,
        setup["field"],
        phi0,
        a0,
        solution,
    )

    return {
        "pre": diagnostics(setup, phi0, a0),
        "loaded": diagnostics(setup, phi, a),
        "relative_residual": float(
            solution["relative_residual"]
        ),
        "condition_number": float(
            solution["condition_number"]
        ),
    }


def dual_case(setup, shift, e_sign, b_sign):
    h = float(setup["field"]["h"])

    phi2 = translated(
        setup["phi0"], shift, h
    )

    a2 = translated(
        setup["a0"], shift, h
    )

    second_energy = diagnostics(
        setup, phi2, a2
    )["energy_j"]

    combined_phi = (
        setup["phi0"] + e_sign*phi2
    )

    combined_a = (
        setup["a0"] + b_sign*a2
    )

    result = loaded_solve(
        setup, combined_phi, combined_a
    )

    return {
        "shift_m": shift,
        "second_electric_sign": e_sign,
        "second_magnetic_sign": b_sign,
        "second_source_preloaded_energy_j":
            second_energy,
        "first_gap_m": stand_off(0.0),
        "second_gap_m": stand_off(shift),
        "source_support_spheres_overlap":
            abs(shift) < 2*SOURCE_RADIUS_M,
        "finite_box_zero_extension":
            True,
        "pre": result["pre"],
        "loaded": result["loaded"],
        "relative_residual":
            result["relative_residual"],
        "condition_number":
            result["condition_number"],
    }


def main():
    results = []

    for h in GRIDS_M:

        setup = _build_baseline_and_prep(h)

        baseline = loaded_solve(
            setup,
            setup["phi0"],
            setup["a0"],
        )

        pre = baseline["pre"]
        loaded = baseline["loaded"]

        print(
            f"BASE h={h:.3f} "
            f"preCOM={pre['com_m_s2']:+.8f} "
            f"loadedCOM={loaded['com_m_s2']:+.8f} "
            f"loadedMIN={loaded['minimum_m_s2']:+.5f} "
            f"Eloaded={loaded['energy_j']:.8f}J",
            flush=True,
        )

        assert math.isclose(
            pre["energy_j"],
            REFERENCE_R3B_J,
            rel_tol=0.15,
        )

        assert loaded["minimum_m_s2"] < 0

        # Direct validation of 2x amplitude:
        # energy, COM force and local force must scale 4x.
        twice = loaded_solve(
            setup,
            2*setup["phi0"],
            2*setup["a0"],
        )

        for state in ("pre", "loaded"):
            for metric in (
                "energy_j",
                "com_m_s2",
                "minimum_m_s2",
                "positive_force_n",
                "negative_force_n",
            ):
                assert np.isclose(
                    twice[state][metric],
                    4*baseline[state][metric],
                    atol=5e-6,
                    rtol=5e-8,
                ), (h, state, metric)

        intensity_rows = []

        for label, amp in (
            ("energy_1x", 1.0),
            ("energy_2x", math.sqrt(2)),
            ("energy_3x", math.sqrt(3)),
            ("amplitude_2x", 2.0),
            ("amplitude_3x", 3.0),
        ):

            factor = amp*amp

            intensity_rows.append({
                "label": label,
                "amplitude_factor": amp,
                "energy_factor": factor,
                "preloaded_energy_j":
                    factor*pre["energy_j"],
                "loaded_energy_j":
                    factor*loaded["energy_j"],
                "loaded_COM_m_s2":
                    factor*loaded["com_m_s2"],
                "loaded_minimum_m_s2":
                    factor*loaded["minimum_m_s2"],
                "loaded_to_preloaded_COM_ratio":
                    loaded["com_m_s2"]/pre["com_m_s2"],
                "everywhere_1g":
                    bool(
                        factor*loaded["minimum_m_s2"]
                        >= TARGET_ACCELERATION_M_S2
                    ),
            })

        dual_rows = []

        for shift in OFFSETS_M:

            assert stand_off(shift) >= 1.0-1e-9

            for esign, bsign in (
                (1, 1),
                (1, -1),
                (-1, 1),
            ):

                case = dual_case(
                    setup, shift, esign, bsign
                )

                p = case["pre"]
                l = case["loaded"]

                # Fair comparison: scale each combined
                # field to the SINGLE loaded-field energy.
                energy_ratio = (
                    loaded["energy_j"]/l["energy_j"]
                )

                case[
                    "equal_energy_loaded_COM_m_s2"
                ] = l["com_m_s2"]*energy_ratio

                case[
                    "equal_energy_loaded_minimum_m_s2"
                ] = l["minimum_m_s2"]*energy_ratio

                case[
                    "equal_energy_preloaded_minimum_m_s2"
                ] = p["minimum_m_s2"]*energy_ratio

                case[
                    "loaded_to_preloaded_COM_ratio"
                ] = (
                    l["com_m_s2"]/p["com_m_s2"]
                    if abs(p["com_m_s2"]) > 1e-12
                    else None
                )

                case["everywhere_1g"] = bool(
                    l["minimum_m_s2"]
                    >= TARGET_ACCELERATION_M_S2
                )

                dual_rows.append(case)

                print(
                    f"DUAL h={h:.3f} "
                    f"dz={shift:+.1f}m "
                    f"E2={esign:+d} B2={bsign:+d} "
                    f"preCOM={p['com_m_s2']:+.5f} "
                    f"loadedCOM={l['com_m_s2']:+.5f} "
                    f"min={l['minimum_m_s2']:+.4f} "
                    f"Eloaded={l['energy_j']:.6f}J "
                    f"gap2={case['second_gap_m']:.3f}m",
                    flush=True,
                )

        results.append({
            "grid_m": h,
            "baseline_pre": pre,
            "baseline_loaded": loaded,
            "intensities": intensity_rows,
            "dual_sources": dual_rows,
        })

    output = {
        "branch": BRANCH,
        "scope":
            "AXISYMMETRIC_STATIC_RECIPROCAL_LOADING",
        "actual_3d_tilt_angles_tested": False,
        "physical_dual_sources_certified": False,
        "shifted_source_boundary_audit_completed": False,
        "exact_grid_aligned_translations": True,
        "all_intensity_cases_fail_everywhere_1g":
            all(
                not r["everywhere_1g"]
                for grid in results
                for r in grid["intensities"]
            ),
        "all_dual_cases_fail_everywhere_1g":
            all(
                not r["everywhere_1g"]
                for grid in results
                for r in grid["dual_sources"]
            ),
        "complete_operating_energy_certified":
            False,
        "whole_craft_lift": False,
        "006D_replaced": False,
        "grids": results,
    }

    path = Path(
        "results/data/"
        "032h17a12d1r3x3b12_dual_source_intensity_summary.json"
    )

    path.parent.mkdir(
        parents=True, exist_ok=True
    )

    path.write_text(
        json.dumps(
            output, indent=2, sort_keys=True
        ) + "\n",
        encoding="utf8",
    )

    print("INTENSITY_SCALING_EXACT=PASS_SCOPED")
    print("ALL_DUAL_SOURCE_EVERYWHERE_1G=FAIL_SCOPED")
    print("AXIAL_DUAL_SOURCE_SOLVES=COMPLETED_SCOPED")
    print("ARBITRARY_TILT_ANGLES=NOT_TESTED_REQUIRES_3D")
    print("SUMMARY=", path)


if __name__ == "__main__":
    main()
