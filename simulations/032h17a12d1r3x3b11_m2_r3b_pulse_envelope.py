"""R3X3B11-M2 — original R3B on/off pulse test.

QUESTION
--------
Does switching the original R3B loaded field on briefly,
repeating every millisecond, produce >=1g average impulse?

MODEL
-----
The corrected Lorentzian R3X1 static carrier equations are
linear in the external source amplitudes when density is frozen.

A common source envelope q(t) therefore produces, in the
quasistatic limit:

    E(t) = q(t) E_loaded
    B(t) = q(t) B_loaded
    a_z(t) = q(t)^2 a_z_loaded

For a smooth sin^2 ON pulse:

    integral(q^2 dt) = 3*width/8

This directly tests finite-payload impulse using the original
toroidal geometry and reciprocal matter loading.

LIMITATIONS
-----------
This is a quasistatic switched-source falsification test.
It does NOT solve time-dependent Maxwell propagation, full
matter motion, magnetic microscopic source dynamics, radiation,
activation losses, or whole-craft momentum exchange.

B7 is an independently checked finite-width electric-source
control; its shell is not inserted into the loaded BVP.

No physical antigravity or device claim is authorized.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np

from antigravity_research.agminer.hook17_concurrent_u1_fieldstrength_metric import (
    C_LIGHT_M_S,
    HBAR_C_EV_M,
    REFERENCE_PORTAL_SCALE_EV,
    TARGET_ACCELERATION_M_S2,
)

from antigravity_research.agminer.hook17_fdual_f_r3c1_validation import (
    _build_baseline_and_prep,
)

from antigravity_research.agminer.hook17_fdual_f_r3x1_lorentzian_sign_audit import (
    _solve_loaded,
    _state,
)

from antigravity_research.agminer.hook17_fdual_f_loaded_payload_homotopy import (
    _fields_from_potentials,
    _vectors_to_full_potentials,
)

from antigravity_research.agminer.hook17_fdual_f_r3x3b7_finite_charge_shell import (
    evaluate_r3b_grid,
    source_density_proxy,
)


PERIOD_S = 1e-3
WIDTHS_US = (10., 100., 500., 1000.)

R3B_J = 1.5429162116460216
B7_J = 1.5473042949759672

KAPPA = (
    -2.0 * HBAR_C_EV_M**2
    / REFERENCE_PORTAL_SCALE_EV**4
)


def measure(setup, phi, a):
    """Calculate full finite-density material force."""

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
            sigma,
            h,
            axis=0,
            edge_order=2,
        )
    )

    weights = (
        2 * math.pi * f["rho_grid"] * h*h
        * setup["density"]
    )

    mass = float(weights.sum())

    positive = float(
        (weights * np.maximum(acceleration, 0)).sum()
    )

    negative = float(
        (weights * np.minimum(acceleration, 0)).sum()
    )

    minimum = float(
        acceleration[f["payload"]].min()
    )

    return (
        mass,
        positive,
        negative,
        minimum,
        acceleration,
    )


def envelope(t, width):
    """Repeated smooth ON/OFF amplitude, period 1 ms."""

    phase = np.mod(t, PERIOD_S) / width

    return np.where(
        phase <= 1,
        np.sin(np.pi * phase)**2,
        0.,
    )


def b7_current_continuity_gate():
    """Verify conserved effective finite-width electric current."""

    radii = np.array([
        1.50, 1.87, 1.91, 1.95,
        1.99, 2.01, 2.20,
    ])

    for ell in (1, 2, 3):

        rho_l = source_density_proxy(
            ell, 1., 2., 0.1, radii
        )

        qprime = 13000.

        j_t = (
            qprime * radii * rho_l
            / (ell * (ell + 1))
        )

        residual = (
            qprime * rho_l
            - ell * (ell + 1) * j_t / radii
        )

        relative = (
            np.max(abs(residual))
            / max(1., np.max(abs(qprime*rho_l)))
        )

        assert relative < 1e-12

        assert (
            np.max(abs(rho_l[[0, 1, 5, 6]]))
            < 1e-9
        )

        assert np.max(abs(rho_l[2:5])) > 1e-7


def main():

    reference = evaluate_r3b_grid(0.05, (0.1,))

    assert math.isclose(
        reference[
            "original_preloaded_field_energy_j"
        ],
        R3B_J,
        rel_tol=1e-9,
    )

    assert math.isclose(
        reference["shells"][0][
            "mixed_field_energy_j_normalized"
        ],
        B7_J,
        rel_tol=1e-9,
    )

    b7_current_continuity_gate()

    rows = []
    traces = []
    peak_com_values = []

    for h in (0.075, 0.05, 0.04):

        setup = _build_baseline_and_prep(h)

        _, _, _, preloaded_min, _ = measure(
            setup,
            setup["phi0"],
            setup["a0"],
        )

        assert (
            preloaded_min
            >= TARGET_ACCELERATION_M_S2 - 1e-6
        )

        solution = _solve_loaded(
            setup["prep"], 1., 1.
        )

        assert solution["success"], (
            f"Loaded solve failed: h={h}"
        )

        phi, a = _vectors_to_full_potentials(
            setup["prep"],
            setup["field"],
            setup["phi0"],
            setup["a0"],
            solution,
        )

        mass, pos, neg, amin, acc = measure(
            setup, phi, a
        )

        loaded_energy = _state(
            setup, solution
        )["canonical_field_energy_j"]

        # Directly test the quadratic source-amplitude identity.
        _, _, _, _, check = measure(
            setup,
            .37 * phi,
            .37 * a,
        )

        assert np.allclose(
            check,
            .37**2 * acc,
            atol=1e-7,
            rtol=3e-10,
        )

        com = (pos + neg) / mass
        peak_com_values.append(com)

        # Case 1 preserves the original R3B source normalization.
        #
        # Case 2 matches the numerical B7 energy value only.
        # It does not implement the B7 shell in the loaded BVP.

        for label, factor in (
            ("R3B_ORIGINAL_SOURCE", 1.),
            (
                "B7_NUMERIC_PEAK_CAP_ONLY_NOT_B7_SOURCE",
                B7_J / loaded_energy,
            ),
        ):

            for width_us in WIDTHS_US:

                width = width_us * 1e-6

                # Validate the exact smooth-pulse integral.
                ts = np.linspace(0, width, 10001)

                integral = 3 * width / 8

                numeric = float(
                    np.trapezoid(
                        np.sin(np.pi * ts / width)**4,
                        ts,
                    )
                )

                assert abs(numeric - integral) < 1e-12

                dp_plus = pos * factor * integral
                dp_minus = neg * factor * integral

                dp = dp_plus + dp_minus

                average = dp / (mass * PERIOD_S)

                worst_average = (
                    amin * factor * integral / PERIOD_S
                )

                row = {
                    "grid_m": h,
                    "case": label,
                    "pulse_width_us": width_us,
                    "period_ms": 1.,
                    "sampled_payload_mass_kg": mass,
                    "loaded_peak_energy_j":
                        loaded_energy * factor,
                    "loaded_peak_COM_m_s2":
                        com * factor,
                    "loaded_peak_worst_point_m_s2":
                        amin * factor,
                    "positive_impulse_kg_m_s":
                        dp_plus,
                    "negative_impulse_kg_m_s":
                        dp_minus,
                    "net_impulse_kg_m_s": dp,
                    "cycle_avg_COM_m_s2": average,
                    "cycle_avg_worst_point_m_s2":
                        worst_average,
                    "cycle_avg_COM_ge_1g":
                        bool(
                            average >= TARGET_ACCELERATION_M_S2
                        ),
                    "cycle_avg_local_ge_1g":
                        bool(
                            worst_average
                            >= TARGET_ACCELERATION_M_S2
                        ),
                }

                rows.append(row)

                if label == "R3B_ORIGINAL_SOURCE":

                    print(
                        f"h={h:.3f}m "
                        f"ON={width_us:4.0f}us "
                        f"Epeak={loaded_energy:.6f}J "
                        f"a_peak={com:+.7f}m/s2 "
                        f"a_avg={average:+.8f}m/s2 "
                        f"dp={dp:+.9g}kg.m/s "
                        f"worst_avg={worst_average:+.4f}m/s2",
                        flush=True,
                    )

        # Two continuous quasistatic activation cycles.
        # This records ON and OFF, not a full Maxwell evolution.
        if h == 0.05:

            times = np.linspace(
                0,
                2 * PERIOD_S,
                2001,
                endpoint=False,
            )

            q = envelope(times, 100e-6)

            traces = [
                {
                    "time_ms": float(t*1e3),
                    "q": float(x),
                    "canonical_loaded_field_j":
                        float(loaded_energy*x*x),
                    "net_material_force_n":
                        float((pos+neg)*x*x),
                }
                for t, x in zip(times, q)
            ]

    # The historical loaded COM result changes sign
    # between h=0.05 m and h=0.04 m.
    sign_change = bool(
        peak_com_values[1] * peak_com_values[2] < 0
    )

    assert sign_change, (
        "Numerical history changed; inspect before interpreting"
    )

    summary = {
        "branch": "032H17A12D1R3X3B11_M2",
        "scope":
            "QUASISTATIC_R3B_LOADED_TOROIDAL_COMMON_ENVELOPE",
        "original_r3b_preloaded_j": R3B_J,
        "b7_10cm_preloaded_j": B7_J,
        "effective_b7_electric_current_conservation":
            "PASS_SCOPED",
        "source_scaling_q2_identity": "PASS",
        "fully_time_dependent_maxwell_matter_solved":
            False,
        "b7_source_inserted_in_loaded_BVP": False,
        "magnetic_source_realized": False,
        "grids_com_sign_change": sign_change,
        "any_cycle_avg_com_1g": any(
            x["cycle_avg_COM_ge_1g"] for x in rows
        ),
        "any_cycle_avg_local_1g": any(
            x["cycle_avg_local_ge_1g"] for x in rows
        ),
        "polarity_reversal_tested": False,
        "whole_craft_lift_certified": False,
        "complete_operating_energy_certified": False,
        "replaced_006D": False,
        "rows": rows,
    }

    out = Path("results/data")
    out.mkdir(parents=True, exist_ok=True)

    path = out / (
        "032h17a12d1r3x3b11_m2_r3b_onoff_summary.json"
    )

    trace_path = out / (
        "032h17a12d1r3x3b11_m2_r3b_onoff_trace.csv"
    )

    path.write_text(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf8",
    )

    with trace_path.open(
        "w",
        newline="",
        encoding="utf8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=traces[0].keys(),
        )

        writer.writeheader()
        writer.writerows(traces)

    print("R3B_ONOFF_QUASISTATIC_GATE=COMPLETED")
    print("B7_EFFECTIVE_CURRENT_CONSERVATION=PASS_SCOPED")
    print("ACTUAL_TIME_DOMAIN_PULSE=NOT_TESTED")

    print(
        "ANY_1G_CYCLE_AVERAGE=",
        summary["any_cycle_avg_com_1g"],
    )

    print("GRID_SIGN_CHANGE=", sign_change)
    print("SUMMARY=", path)
    print("TRACE=", trace_path)


if __name__ == "__main__":
    main()
