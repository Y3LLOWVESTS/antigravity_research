"""R3X3B11-M3 — Quasistatic R3B source-polarity gate.

Re-solve the corrected R3X1 loaded toroidal equations after
reversing either the electric or magnetic source potential.

The field force is reconstructed AFTER solving. No artificial
force-sign reversal is applied.

A 100-us sin^2 pulse repeats every 1 ms.

This is a fixed-density quasistatic test, not time-dependent
Maxwell evolution or a microscopic source realization.
The B7 finite-width source is not inserted in the loaded BVP.
"""

from __future__ import annotations

import json
import math
import runpy
from pathlib import Path

import numpy as np

m2_path = Path(
    "simulations/"
    "032h17a12d1r3x3b11_m2_r3b_pulse_envelope.py"
)

if not m2_path.is_file():
    raise SystemExit("M2_SCRIPT_REQUIRED")

m2 = runpy.run_path(str(m2_path))

PERIOD_S = 1e-3
WIDTH_S = 100e-6
WEIGHT = 3 * WIDTH_S / (8 * PERIOD_S)
G = 9.80665


def signed(setup, electric_sign, magnetic_sign):
    original = setup["prep"]
    prep = dict(original)

    for name, sign in (
        ("phi0_vec", electric_sign),
        ("d_phi0", electric_sign),
        ("a0_vec", magnetic_sign),
        ("c_a0", magnetic_sign),
    ):
        prep[name] = sign * original[name]

    solution = m2["_solve_loaded"](prep, 1., 1.)

    assert solution["success"]
    assert solution["relative_residual"] < 1e-8

    phi0 = electric_sign * setup["phi0"]
    a0 = magnetic_sign * setup["a0"]

    phi, a = m2["_vectors_to_full_potentials"](
        prep, setup["field"], phi0, a0, solution
    )

    field = setup["field"]
    h = float(field["h"])

    em = m2["_fields_from_potentials"](
        phi, a, field["rho_grid"], h
    )

    kappa = (
        -2 * m2["HBAR_C_EV_M"]**2
        / m2["REFERENCE_PORTAL_SCALE_EV"]**4
    )

    sigma = kappa * (
        em["e_rho"] * em["b_rho"]
        + em["e_z"] * em["b_z"]
    )

    acc = -(m2["C_LIGHT_M_S"]**2) * np.gradient(
        sigma, h, axis=0, edge_order=2
    )

    weights = (
        2 * math.pi * field["rho_grid"]
        * h*h * setup["density"]
    )

    mass = float(weights.sum())
    positive = float(np.sum(weights * np.maximum(acc, 0)))
    negative = float(np.sum(weights * np.minimum(acc, 0)))

    energy = m2["_state"](
        dict(setup, prep=prep, phi0=phi0, a0=a0),
        solution
    )["canonical_field_energy_j"]

    com = (positive + negative) / mass

    return {
        "signs": [electric_sign, magnetic_sign],
        "loaded_peak_energy_j": float(energy),
        "loaded_peak_com_m_s2": com,
        "loaded_min_local_m_s2":
            float(acc[field["payload"]].min()),
        "positive_peak_force_n": positive,
        "negative_peak_force_n": negative,
        "pulse_100us_cycle_avg_m_s2": com * WEIGHT,
        "pulse_100us_net_impulse_kg_m_s":
            (positive + negative) * WIDTH_S * 3 / 8,
        "payload_acceleration": acc[field["payload"]],
    }


def main():
    results = []

    historical = {
        .075: .0797075974,
        .05: .1545419009,
        .04: -.0917423637,
    }

    for h in (.075, .05, .04):
        setup = m2["_build_baseline_and_prep"](h)

        states = {
            "++": signed(setup, 1, 1),
            "+-": signed(setup, 1, -1),
            "-+": signed(setup, -1, 1),
            "--": signed(setup, -1, -1),
        }

        original = states["++"]
        flipped = states["+-"]

        assert abs(
            original["loaded_peak_com_m_s2"]
            - historical[h]
        ) < 1e-5

        # Simultaneous inversion must preserve force.
        # The two single-sector inversions are equivalent.
        for first, second in (
            ("++", "--"),
            ("+-", "-+"),
        ):
            for key in (
                "loaded_peak_com_m_s2",
                "loaded_min_local_m_s2",
                "loaded_peak_energy_j",
            ):
                assert np.isclose(
                    states[first][key],
                    states[second][key],
                    rtol=1e-8,
                    atol=1e-8,
                )

            assert np.allclose(
                states[first]["payload_acceleration"],
                states[second]["payload_acceleration"],
                rtol=1e-8,
                atol=1e-6,
            )

        common_inward = np.logical_and(
            original["payload_acceleration"] < 0,
            flipped["payload_acceleration"] < 0,
        )

        count = int(np.count_nonzero(common_inward))
        assert count > 0

        best_peak = max(
            original["loaded_peak_com_m_s2"],
            flipped["loaded_peak_com_m_s2"],
        )

        assert best_peak < G

        best_avg = WEIGHT * best_peak

        alternating_avg = WEIGHT * (
            original["loaded_peak_com_m_s2"]
            + flipped["loaded_peak_com_m_s2"]
        ) / 2

        print(
            f"h={h:.3f}m "
            f"original={original['loaded_peak_com_m_s2']:+.9f} "
            f"one_flip={flipped['loaded_peak_com_m_s2']:+.9f} "
            f"best_100us={best_avg:+.9f} "
            f"alternating={alternating_avg:+.9f} "
            f"inward_both={count} "
            f"flipped_energy={flipped['loaded_peak_energy_j']:.9f}J",
            flush=True,
        )

        clean_states = {}

        for label, state in states.items():
            clean_states[label] = {
                key: value
                for key, value in state.items()
                if key != "payload_acceleration"
            }

        results.append({
            "grid_m": h,
            "states": clean_states,
            "common_inward_payload_samples": count,
            "sampled_payload_cells":
                int(original["payload_acceleration"].size),
            "alternating_two_cycle_avg_m_s2":
                alternating_avg,
            "best_polarity_100us_cycle_avg_m_s2":
                best_avg,
            "any_1g_com": False,
            "any_1g_everywhere": False,
        })

    out = Path(
        "results/data/"
        "032h17a12d1r3x3b11_m3_polarity_gate_summary.json"
    )

    out.parent.mkdir(parents=True, exist_ok=True)

    summary = {
        "branch": "032H17A12D1R3X3B11_M3",
        "scope":
            "QUASISTATIC_FIXED_DENSITY_LOADED_TORUS_SOURCE_POLARITY",
        "period_ms": 1.,
        "pulse_width_us": 100.,
        "actual_time_domain_current_and_field_evolution":
            False,
        "b7_finite_width_source_inserted": False,
        "polarity_switching_work_and_radiation_included":
            False,
        "complete_operating_energy_certified": False,
        "whole_craft_lift": False,
        "replaced_006d": False,
        "grids": results,
    }

    out.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf8",
    )

    print("POLARITY_RELOADED_STATIC_SOLVES=PASS_SCOPED")
    print("BOTH_SOURCE_REVERSAL_FORCE_INVARIANCE=PASS")
    print("ORIGINAL_EVERYWHERE_1G=FAIL_SCOPED")
    print("ACTUAL_TIME_DEPENDENT_POLARITY_SWITCH=NOT_TESTED")
    print("SUMMARY=", out)


if __name__ == "__main__":
    main()
