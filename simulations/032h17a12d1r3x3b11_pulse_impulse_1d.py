"""R3X3B11 — sourced two-U(1) pulse and impulse control.

PURPOSE
-------
Test whether source-driven pulses across a smooth reciprocal
matter interface produce positive NET neutral-payload impulse.

PHYSICAL SCOPE
--------------
A one-dimensional fixed-matter, two-carrier reduction of the
Lorentzian topological same-action equations.

This is NOT the fully coupled toroidal R3B geometry.

The R3B/B7 original field energies are reproduced independently.
B7's 3D electrostatic charge source is NOT the transverse
pulse driver used in this 1D calculation.

The dimensionless theta=20 is diagnostic, not the actual
spatially varying R3B loading coefficient.

ACTION
------
Canonical coordinates: tau=c*t; fields in sqrt(J/m^3).

L = (E_X^2+E_Y^2-B_X^2-B_Y^2)/2 + theta*C
C = E_X.B_Y + E_Y.B_X

D_X = E_X + theta*B_Y
H_X = B_X - theta*E_Y

The Y equations follow by X/Y exchange.

For a fixed material profile, the exact carrier evolution is:

d_tau E = R*d_x B - theta' * R*swap(E) - j
d_tau B = -R*d_x E

R(a_y,a_z) = (-a_z,a_y).

Matter action, at leading metric-coupling order:

L_m = -rho*c^2 - rho*c^2*lambda*C
theta = -rho*c^2*lambda

The net material force per transverse area is:

F_m = -integral(theta' * C) dx

The source force and field momentum are also integrated.
The carrier energy is 0.5*(E^2+B^2).

VALIDATION
----------
Independent U(1) constraints in the transverse 1D sector,
zero-charge conserved external current, field-energy balance,
total momentum balance, zero-coupling control, three-grid
convergence, positive/negative/net impulse accounting.

All pulses evolve continuously from zero initial field.
There are no artificial resets between pulses.

LIMITATIONS
-----------
Fixed material; no mechanical displacement feedback.
No microscopic B7 pulse source or toroidal R3B dynamic field.
No complete gravity/metric evolution, radiation-loss ledger,
whole-craft propulsion, or complete operating-energy claim.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np

from antigravity_research.agminer.hook17_fdual_f_r3x3b7_finite_charge_shell import (
    evaluate_r3b_grid,
)

C = 299792458.0
G = 9.80665

R3B_ENERGY_J = 1.5429162116460216
B7_ENERGY_J = 1.5473042949759672

END_TAU_M = 6.25

# Illustrative planar reduction, NOT R3B torus geometry.
AREA_M2 = 1.0
PAYLOAD_MASS_KG = 1.0

SOURCE_RIGHT_M = 0.0
PAYLOAD_LEFT_M = 1.0
PAYLOAD_RIGHT_M = 1.4
TRANSITION_M = 0.15


def rotate(v):
    """Transverse 90-degree rotation."""
    return np.stack(
        (-v[:, 1, :], v[:, 0, :]),
        axis=1,
    )


def smoothstep(u):
    """C2-smooth transition from zero to one."""
    z = np.clip(u, 0.0, 1.0)
    return z**3 * (10.0 + z*(-15.0 + 6.0*z))


def medium(dx_requested, theta_peak):
    """Finite matter interface and external current support."""
    length = 15.0
    n = int(round(length/dx_requested))
    dx = length/n

    x = -6.0 + (np.arange(n)+0.5)*dx

    left = smoothstep(
        (x-PAYLOAD_LEFT_M)/TRANSITION_M
    )
    right = smoothstep(
        (PAYLOAD_RIGHT_M-x)/TRANSITION_M
    )

    theta = theta_peak*left*right

    grad_theta = (
        np.roll(theta, -1)-np.roll(theta, 1)
    )/(2.0*dx)

    # Conserved transverse-current source,
    # confined to -0.6 m < x < 0 m.
    r = (x+0.3)/0.3
    source = np.zeros_like(x)
    sel = abs(r) < 1.0

    source[sel] = np.exp(
        1.0-1.0/(1.0-r[sel]**2)
    )
    source /= np.sum(source)*dx

    assert np.max(x[source > 0]) < SOURCE_RIGHT_M

    if theta_peak:
        assert np.min(x[theta > 0]) >= PAYLOAD_LEFT_M
        assert np.max(x[theta > 0]) <= PAYLOAD_RIGHT_M

    return x, dx, theta, grad_theta, source


def drive(tau, pulses):
    """Smooth finite-duration drive; no field reset."""
    starts = (
        (0.20,)
        if pulses == 1
        else (0.20, 1.70, 3.20)
    )

    width = 0.78
    total = 0.0

    for start in starts:
        z = (tau-start)/width

        if 0.0 < z < 1.0:
            total += (
                math.sin(math.pi*z)**2
                * math.sin(3.0*math.pi*z)
            )

    return total


def simulate(dx_requested, theta_peak, pulses):
    x, dx, theta, grad_theta, source = medium(
        dx_requested, theta_peak
    )
    n = len(x)

    # Explicit wave-CFL and gyrotropic stability controls.
    step_max = min(
        0.15*dx,
        0.75*dx/(1.0+np.max(abs(grad_theta))*dx),
    )

    nstep = math.ceil(END_TAU_M/step_max)
    dt = END_TAU_M/nstep

    # First 8*n entries: electric and magnetic fields.
    # Final 5: material impulse, source impulse,
    # driver work, positive and negative material impulse.
    y = np.zeros(8*n+5)

    max_field_energy = 0.0
    trace = []

    def rhs(t, state):
        eb = state[:8*n].reshape(2, 2, 2, n)
        e, b = eb

        de = (
            np.roll(e, -1, axis=-1)
            - np.roll(e, 1, axis=-1)
        )/(2.0*dx)

        db = (
            np.roll(b, -1, axis=-1)
            - np.roll(b, 1, axis=-1)
        )/(2.0*dx)

        j = np.zeros_like(e)
        j[0, 0] = drive(t, pulses)*source

        deriv = np.empty_like(state)
        deb = np.empty_like(eb)

        # Corrected Lorentzian same-action dynamics.
        deb[0] = (
            rotate(db)
            - grad_theta*rotate(e[::-1])
            - j
        )

        deb[1] = -rotate(de)
        deriv[:8*n] = deb.reshape(-1)

        invariant = np.sum(
            e[0]*b[1]+e[1]*b[0],
            axis=0,
        )

        # Reciprocal force from the matter interaction.
        payload_force = -dx*np.dot(
            grad_theta, invariant
        )

        # Equal bookkeeping for physical source reaction.
        source_force = -dx*np.sum(
            j*rotate(b)
        )

        driver_work_rate = -dx*np.sum(e*j)

        deriv[8*n:] = (
            payload_force,
            source_force,
            driver_work_rate,
            max(0.0, payload_force),
            min(0.0, payload_force),
        )

        return deriv

    # RK4 time evolution. The evolving field is never reset.
    for step in range(nstep):
        t = step*dt

        k1 = rhs(t, y)
        k2 = rhs(t+dt/2.0, y+k1*(dt/2.0))
        k3 = rhs(t+dt/2.0, y+k2*(dt/2.0))
        k4 = rhs(t+dt, y+k3*dt)

        y += (dt/6.0)*(
            k1+2.0*k2+2.0*k3+k4
        )

        eb = y[:8*n].reshape(2, 2, 2, n)

        field_energy = (
            0.5*dx*np.sum(eb**2)*AREA_M2
        )

        max_field_energy = max(
            max_field_energy, field_energy
        )

        if step % 40 == 0 or step == nstep-1:
            trace.append((
                (t+dt)/C*1e9,
                float(field_energy),
                float(y[8*n]),
                float(y[8*n+3]),
                float(y[8*n+4]),
            ))

    e, b = y[:8*n].reshape(2, 2, 2, n)

    end_energy = float(
        0.5*dx*np.sum(e**2+b**2)*AREA_M2
    )

    field_momentum_natural = float(
        dx*np.sum(
            e[:, 0]*b[:, 1]
            - e[:, 1]*b[:, 0]
        )*AREA_M2
    )

    p, s, w, pp, pn = map(float, y[8*n:])

    energy_err = abs(end_energy-w)/max(
        abs(end_energy), abs(w), 1e-15
    )

    momentum_err = abs(
        field_momentum_natural+p+s
    )/max(
        abs(field_momentum_natural),
        abs(p), abs(s), 1e-15
    )

    # Valid homogeneous quadratic scaling in this
    # FIXED-THETA linearized planar control only.
    #
    # This does not establish that B7's field/source
    # configuration can generate these pulses.
    scale = B7_ENERGY_J/max_field_energy

    impulse = p*scale/C
    physical_time = END_TAU_M/C

    result = {
        "dx_m": dx,
        "theta_peak_diagnostic_not_r3b": theta_peak,
        "pulses": pulses,
        "time_window_ns": physical_time*1e9,
        "time_steps": nstep,

        "field_energy_max_normalized_j":
            B7_ENERGY_J,

        "field_energy_end_normalized_j":
            end_energy*scale,

        "driver_work_normalized_j":
            w*scale,

        "net_payload_impulse_kg_m_s":
            impulse,

        "positive_payload_impulse_kg_m_s":
            pp*scale/C,

        "negative_payload_impulse_kg_m_s":
            pn*scale/C,

        "net_source_impulse_kg_m_s":
            s*scale/C,

        "final_field_momentum_kg_m_s":
            field_momentum_natural*scale/C,

        "average_payload_acceleration_m_s2":
            impulse/(PAYLOAD_MASS_KG*physical_time),

        "energy_relative_residual":
            energy_err,

        "momentum_relative_residual":
            momentum_err,

        "payload_1g_average_pass":
            bool(
                impulse/(PAYLOAD_MASS_KG*physical_time)
                >= G
            ),

        "no_field_resets": True,
        "source_support_max_x_m": SOURCE_RIGHT_M,
        "payload_support_min_x_m": PAYLOAD_LEFT_M,
    }

    return result, trace


def main():
    # Reproduce the actual frozen R3B and B7 reference
    # from the existing repository modules first.
    control = evaluate_r3b_grid(0.05, (0.10,))

    frozen = control[
        "original_preloaded_field_energy_j"
    ]
    b7 = control[
        "shells"
    ][0]["mixed_field_energy_j_normalized"]

    assert abs(frozen-R3B_ENERGY_J) < 1e-8
    assert abs(b7-B7_ENERGY_J) < 1e-8

    cases = (
        (0.0125, 0.0, 1),
        (0.0125, 0.0, 3),
        (0.0125, 20.0, 1),
        (0.00625, 20.0, 1),
        (0.0125, 20.0, 3),
        (0.00625, 20.0, 3),
        (0.003125, 20.0, 3),
    )

    results = []
    traces = {}

    for dx, theta, pulses in cases:
        result, history = simulate(dx, theta, pulses)
        results.append(result)

        key = (
            f"theta_{theta:g}_"
            f"pulses_{pulses}_dx_{dx:g}"
        )
        traces[key] = history

        print(
            f"theta={theta:4g} "
            f"dx={dx:.6f} "
            f"pulses={pulses} "
            f"a_avg="
            f"{result['average_payload_acceleration_m_s2']:.9f} "
            f"I_net="
            f"{result['net_payload_impulse_kg_m_s']:.8e} "
            f"Eerr="
            f"{result['energy_relative_residual']:.2e} "
            f"Perr="
            f"{result['momentum_relative_residual']:.2e}",
            flush=True,
        )

        assert result["energy_relative_residual"] < 2e-5

        if theta > 0:
            assert result["momentum_relative_residual"] < 2e-5

        if theta == 0:
            assert result["net_payload_impulse_kg_m_s"] == 0

        assert abs(
            result["net_payload_impulse_kg_m_s"]
            - result["positive_payload_impulse_kg_m_s"]
            - result["negative_payload_impulse_kg_m_s"]
        ) < 1e-15

    fine = [
        r for r in results
        if r["theta_peak_diagnostic_not_r3b"] == 20
        and r["pulses"] == 3
    ]

    a_coarse, a_mid, a_fine = [
        r["average_payload_acceleration_m_s2"]
        for r in fine
    ]

    convergence = abs(a_mid-a_fine)/max(
        abs(a_fine), 1e-30
    )

    assert convergence < 0.05
    assert not fine[-1]["payload_1g_average_pass"]

    summary = {
        "branch": "032H17A12D1R3X3B11",

        "classification":
            "SCOPED_1D_FIXED_MATTER_PULSE_FAILS_1G",

        "R3B_frozen_energy_reproduced_j":
            frozen,

        "B7_frozen_energy_reproduced_j":
            b7,

        "b7_source_used_for_pulse_current":
            False,

        "actual_toroidal_r3b_dynamic_source_used":
            False,

        "actual_toroidal_payload_loading":
            False,

        "fixed_matter_1d_same_action_reduction":
            True,

        "counterfactual_theta_peak_not_r3b":
            20,

        "convergence_refined_relative":
            convergence,

        "cases": results,

        "this_pulse_slab_case_passes_1g":
            False,

        "all_pulse_mechanisms_falsified":
            False,

        "whole_craft_lift":
            False,

        "complete_operating_energy_certified":
            False,

        "006d_replaced":
            False,
    }

    out = Path(
        "results/data/"
        "032h17a12d1r3x3b11_pulse_impulse_1d_summary.json"
    )

    out.parent.mkdir(
        parents=True, exist_ok=True
    )

    out.write_text(
        json.dumps(
            summary, indent=2, sort_keys=True
        )+"\n",
        encoding="utf8",
    )

    tracefile = out.with_name(
        "032h17a12d1r3x3b11_pulse_impulse_1d_traces.csv"
    )

    with tracefile.open(
        "w", newline="", encoding="utf8"
    ) as fh:
        writer = csv.writer(fh)
        writer.writerow((
            "case",
            "time_ns",
            "unscaled_energy",
            "unscaled_payload_impulse",
            "unscaled_positive_impulse",
            "unscaled_negative_impulse",
        ))

        for key, series in traces.items():
            writer.writerows(
                (key, *row)
                for row in series
            )

    print(
        "FINAL_THREE_PULSE_ACCELERATION="
        f"{a_fine:.9f} m/s^2"
    )
    print(
        "FRACTION_OF_1G="
        f"{a_fine/G:.6f}"
    )
    print(
        "REFINEMENT_RELATIVE="
        f"{convergence:.6g}"
    )
    print(f"SUMMARY={out}")
    print(f"TRACES={tracefile}")
    print("TOROIDAL_R3B_FULLY_LOADED_PULSE=NOT_TESTED")


if __name__ == "__main__":
    main()
