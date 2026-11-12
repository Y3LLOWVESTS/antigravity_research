"""R3X3B11-M5 — biased R3B source-support and induction preflight.

PURPOSE
-------
At a 1-ms period, test energy floors of 0%, 25%, 50%, 75%,
90%, and 100% on the original fully loaded R3B torus.

Compare original (++), and one-sector reversed (+-) sources.

This is an exact Maxwell-residual test of a specified trial
field history, NOT a physically sourced time-domain solution.

LEADING LORENTZIAN TWO-U(1) ACTION
----------------------------------
L = (EX^2 + EY^2 - BX^2 - BY^2)/2
    + theta*(EX.BY + EY.BX)

DX = EX + theta*BY
HX = BX - theta*EY

DY = EY + theta*BX
HY = BY - theta*EX

Take theta=-beta_full, tau=c*t, and a common source envelope q:

EX=q EX0
BY=q BY0
EY_phi=-q' AY0
BX_phi=0

The induced EY_phi satisfies Faraday's law for BY.

To maintain these particular field shapes exactly,
Ampere's equations require ADDITIONAL currents:

delta jX = q'*(curl(theta*AY0*e_phi) - DX0)
         = q'*(AY0*grad(theta) cross e_phi - EX0)

delta jY_phi = q''*AY0

The required currents extend through the neutral payload.
Thus these imposed field shapes are not exactly obtainable
from the original external sources alone.

This does NOT exclude real dynamic fields, which may develop
additional components in response to external currents.

For independently varying source amplitudes qE and qB,
the unchanged field shapes also require extra Gauss charge:

delta rhoX = (qB-qE)*grad(theta).BY0

WAVEFORM
--------
q(t)=(1+sqrt(f))/2
    +(1-sqrt(f))*cos(2*pi*t/T)/2

T=1 ms and f is the minimum-to-maximum FIELD ENERGY ratio.

The field amplitude is smooth, including at f=0.
The field energy is proportional to q(t)^2.

LIMITATIONS
-----------
Fixed-density R3X1 source family only.
B7 finite-width charge is a reference, not inserted in BVP.
No physical current driver, radiation, moving matter,
full time-domain Maxwell solution, device or lift claim.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np

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
from antigravity_research.agminer.hook17_concurrent_u1_fieldstrength_metric import (
    C_LIGHT_M_S,
    HBAR_C_EV_M,
    REFERENCE_PORTAL_SCALE_EV,
)
from antigravity_research.agminer.hook17_fdual_f_r3x3b7_finite_charge_shell import (
    evaluate_r3b_grid,
)

PERIOD_S = 1.0e-3
FLOORS = (0.0, 0.25, 0.50, 0.75, 0.90, 1.0)
GRIDS_M = (0.075, 0.05, 0.04)

SIGMA_COEFF = (
    -2.0 * HBAR_C_EV_M**2
    / REFERENCE_PORTAL_SCALE_EV**4
)

REF_R3B_J = 1.5429162116460216
REF_B7_J = 1.5473042949759672


def waveform(floor, phase):
    """Amplitude and two tau=c*t derivatives."""
    a = math.sqrt(floor)
    b = (1+a)/2
    d = (1-a)/2

    omega_tau = (
        2*math.pi
        / (PERIOD_S*C_LIGHT_M_S)
    )

    return (
        b+d*math.cos(phase),
        -d*omega_tau*math.sin(phase),
        -d*omega_tau**2*math.cos(phase),
    )


def loaded_state(setup, magnetic_sign):
    """Re-solve the coupled loaded R3X1 source problem."""
    prep = dict(setup["prep"])

    if magnetic_sign == -1:
        for name in ("a0_vec", "c_a0"):
            prep[name] = -prep[name]

    solution = _solve_loaded(prep, 1.0, 1.0)

    if (
        not solution["success"]
        or solution["relative_residual"] > 1e-8
    ):
        raise RuntimeError("Loaded R3X1 solve failed")

    phi0 = setup["phi0"]
    a0 = magnetic_sign*setup["a0"]

    field = setup["field"]
    h = float(field["h"])

    phi, a = _vectors_to_full_potentials(
        prep, field, phi0, a0, solution
    )

    em = _fields_from_potentials(
        phi, a, field["rho_grid"], h
    )

    sigma = SIGMA_COEFF*(
        em["e_rho"]*em["b_rho"]
        + em["e_z"]*em["b_z"]
    )

    acceleration = (
        -C_LIGHT_M_S**2
        * np.gradient(
            sigma, h, axis=0, edge_order=2
        )
    )

    weights = (
        2*math.pi*field["rho_grid"]
        * h*h*setup["density"]
    )

    com = float(
        np.sum(weights*acceleration)
        / np.sum(weights)
    )

    energy = _state(
        dict(setup, prep=prep, a0=a0),
        solution,
    )["canonical_field_energy_j"]

    return {
        "a_phi": a,
        "fields": em,
        "energy_j": float(energy),
        "com_m_s2": com,
        "worst_m_s2": float(
            np.min(acceleration[field["payload"]])
        ),
    }


def rms(values, weights, mask):
    return math.sqrt(
        float(
            np.sum(values[mask]**2*weights[mask])
            / np.sum(weights[mask])
        )
    )


def ward_bianchi_gate(setup, state):
    """Check trial Ward and Faraday identities with one curl."""
    field = setup["field"]
    h = float(field["h"])
    r = field["rho_grid"]
    rr = np.where(r > 0, r, 1.0)
    mask = field["payload"]

    theta = -setup["beta_full"]
    a = state["a_phi"]
    er = state["fields"]["e_rho"]
    ez = state["fields"]["e_z"]

    def curl_phi(v):
        return (
            -np.gradient(
                v, h, axis=0, edge_order=2
            ),
            np.gradient(
                r*v, h, axis=1, edge_order=2
            )/rr,
        )

    def div_poloidal(vr, vz):
        return (
            np.gradient(
                r*vr, h, axis=1, edge_order=2
            )/rr
            + np.gradient(
                vz, h, axis=0, edge_order=2
            )
        )

    br, bz = curl_phi(a)
    cr, cz = curl_phi(theta*a)

    dr = er+theta*br
    dz = ez+theta*bz

    qprime = waveform(0.5, math.pi/2)[1]

    jr = qprime*(cr-dr)
    jz = qprime*(cz-dz)

    charge = div_poloidal(dr, dz)

    continuity = (
        div_poloidal(jr, jz)
        + qprime*charge
    )

    relative_ward = float(
        np.linalg.norm(continuity[mask])
        / max(
            np.linalg.norm(
                (qprime*charge)[mask]
            ),
            1e-90,
        )
    )

    # Faraday: d_tau BY + curl(EY_phi) = 0.
    fr, fz = curl_phi(-qprime*a)

    relative_faraday = float(
        np.linalg.norm(
            np.hypot(
                qprime*br+fr,
                qprime*bz+fz,
            )[mask]
        )
        / max(
            np.linalg.norm(
                (qprime*np.hypot(br, bz))[mask]
            ),
            1e-90,
        )
    )

    assert relative_ward < 1e-8
    assert relative_faraday < 1e-10

    return relative_ward, relative_faraday


def grid_run(h):
    setup = _build_baseline_and_prep(h)
    field = setup["field"]
    mask = field["payload"]

    weights = (
        2*math.pi*field["rho_grid"]
        * h*h*setup["density"]
    )

    theta = -setup["beta_full"]

    theta_z, theta_r = np.gradient(
        theta, h, edge_order=2
    )

    rows = []

    for polarity, sign in (
        ("++", 1),
        ("+-", -1),
    ):
        state = loaded_state(setup, sign)
        ward, faraday = ward_bianchi_gate(
            setup, state
        )

        em = state["fields"]
        a = state["a_phi"]

        er = em["e_rho"]
        ez = em["e_z"]
        br = em["b_rho"]
        bz = em["b_z"]

        e_rms = rms(
            np.hypot(er, ez), weights, mask
        )

        b_rms = rms(
            np.hypot(br, bz), weights, mask
        )

        a_rms = rms(a, weights, mask)

        # Exact continuum X-Ampere residual coefficient
        # of the imposed globally scaled field.
        jx_r = -er-a*theta_z
        jx_z = -ez+a*theta_r

        jx_coeff = rms(
            np.hypot(jx_r, jx_z),
            weights, mask,
        )

        gauss_coeff = rms(
            theta_r*br+theta_z*bz,
            weights, mask,
        )

        for floor in FLOORS:
            qtop, dtop, ddtop = waveform(
                floor, 0.0
            )

            qbottom, _, _ = waveform(
                floor, math.pi
            )

            qquarter, dquarter, ddquarter = waveform(
                floor, math.pi/2
            )

            assert abs(qtop-1.0) < 1e-14
            assert abs(qbottom*qbottom-floor) < 1e-14
            assert abs(dtop) < 1e-15
            assert abs(ddquarter) < 1e-15

            a_floor = math.sqrt(floor)

            mean_q2 = (
                ((1+a_floor)/2)**2
                + 0.5*((1-a_floor)/2)**2
            )

            # Extra interior current required if the
            # original static field shapes are imposed.
            jx_over_e = (
                abs(dquarter)*jx_coeff
                / max(e_rms, 1e-80)
            )

            jy_over_b = (
                abs(ddtop)*a_rms
                / max(b_rms, 1e-80)
            )

            # A 90-degree independent amplitude-phase
            # shift gives a Gauss-law mismatch unless
            # the actual coupled fields are re-solved.
            phase_difference = abs(
                qquarter-qtop
            )

            rows.append({
                "grid_m": h,
                "polarity": polarity,
                "energy_floor_fraction": floor,
                "period_ms": 1.0,
                "loaded_peak_field_energy_j":
                    state["energy_j"],
                "loaded_floor_field_energy_j":
                    state["energy_j"]*floor,
                "loaded_mean_field_energy_j":
                    state["energy_j"]*mean_q2,
                "mean_q_squared": mean_q2,
                "quasistatic_com_average_m_s2":
                    state["com_m_s2"]*mean_q2,
                "quasistatic_worst_average_m_s2":
                    state["worst_m_s2"]*mean_q2,
                "missing_payload_jx_rms_over_loaded_e_per_m":
                    jx_over_e,
                "missing_payload_jy_rms_over_loaded_b_per_m":
                    jy_over_b,
                "induced_ephi_over_b_at_quarter_cycle":
                    abs(dquarter)*a_rms
                    / max(b_rms, 1e-80),
                "independent_phase_shift_gauss_residual_over_b_per_m":
                    phase_difference*gauss_coeff
                    / max(b_rms, 1e-80),
                "trial_ward_relative_residual": ward,
                "trial_faraday_relative_residual": faraday,
                "instantaneous_envelope_requires_internal_current":
                    bool(
                        jx_over_e > 1e-13
                        or jy_over_b > 1e-13
                    ),
            })

        print(
            f"h={h:.3f} polarity={polarity} "
            f"Epeak={state['energy_j']:.9f}J "
            f"COM={state['com_m_s2']:+.9f}m/s2 "
            f"worst={state['worst_m_s2']:+.4f}m/s2",
            flush=True,
        )

    return rows


def main():
    reference = evaluate_r3b_grid(0.05, (0.1,))

    e_r3b = reference[
        "original_preloaded_field_energy_j"
    ]

    e_b7 = reference["shells"][0][
        "mixed_field_energy_j_normalized"
    ]

    assert math.isclose(
        e_r3b, REF_R3B_J, rel_tol=1e-9
    )

    assert math.isclose(
        e_b7, REF_B7_J, rel_tol=1e-9
    )

    rows = []

    for h in GRIDS_M:
        rows.extend(grid_run(h))

    for row in rows:
        floor = row["energy_floor_fraction"]

        if floor < 1.0:
            assert row[
                "instantaneous_envelope_requires_internal_current"
            ]
        else:
            assert not row[
                "instantaneous_envelope_requires_internal_current"
            ]

        assert (
            row["quasistatic_worst_average_m_s2"]
            < 0.0
        )

    for h in GRIDS_M:
        row = next(
            x for x in rows
            if x["grid_m"] == h
            and x["polarity"] == "++"
            and x["energy_floor_fraction"] == 0.5
        )

        print(
            f"M5 h={h:.3f} f=.50 "
            f"mean_E={row['loaded_mean_field_energy_j']:.8f}J "
            f"quasi_a={row['quasistatic_com_average_m_s2']:+.8f}m/s2 "
            f"missing_Jx_over_E="
            f"{row['missing_payload_jx_rms_over_loaded_e_per_m']:.6g}/m",
            flush=True,
        )

    output = Path(
        "results/data/"
        "032h17a12d1r3x3b11_m5_biased_induction_source_support_summary.json"
    )

    output.parent.mkdir(
        parents=True, exist_ok=True
    )

    result = {
        "branch": "032H17A12D1R3X3B11_M5",
        "classification":
            "MAXWELL_RESIDUAL_OF_IMPOSED_BIASED_TOROIDAL_FIELD",
        "scope":
            "FIXED_DENSITY_TRIAL_FIELD_SOURCE_SUPPORT_PREFLIGHT",
        "period_ms": 1.0,
        "r3b_preloaded_reference_j": e_r3b,
        "b7_preloaded_reference_j": e_b7,
        "b7_source_inserted": False,
        "physically_sourced_time_domain_maxwell_solved": False,
        "full_matter_dynamics_solved": False,
        "whole_craft_lift": False,
        "complete_operating_energy_certified": False,
        "006d_replaced": False,
        "rows": rows,
    }

    output.write_text(
        json.dumps(
            result, indent=2, sort_keys=True
        )+"\n",
        encoding="utf8",
    )

    csv_path = output.with_suffix(".csv")

    with csv_path.open(
        "w", newline="", encoding="utf8"
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(rows[0]),
        )
        writer.writeheader()
        writer.writerows(rows)

    print(
        "NONZERO_FLOORS_TESTED=0%,25%,50%,75%,90%,100%"
    )
    print(
        "INSTANTANEOUS_ENVELOPE_NEEDS_INTERNAL_CURRENTS=YES_SCOPED"
    )
    print(
        "FLOOR_RESCUES_QUASISTATIC_EVERYWHERE_1G=NO_SCOPED"
    )
    print(
        "ACTUAL_DRIVEN_R3B_TIME_DOMAIN=NOT_TESTED"
    )
    print("SUMMARY=", output)
    print("CSV=", csv_path)


if __name__ == "__main__":
    main()
