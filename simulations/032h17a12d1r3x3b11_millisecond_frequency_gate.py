"""R3X3B11-M1: millisecond-cycle two-U(1) frequency preflight.

PURPOSE
-------
Test whether millisecond-period field cycling can overcome
interface suppression in a smooth finite-width matter slab.

ACTION / CONVENTIONS
--------------------
L = 1/2 sum_I (E_I^2 - B_I^2)
    + theta(x)*(E_X.B_Y + E_Y.B_X)

D_I = E_I + theta*B_other
H_I = B_I - theta*E_other

For fixed theta(x), tangential E and H are continuous.
Within each constant-theta layer, E obeys the vacuum wave
equation. Transfer matrices give the exact harmonic response.

The smooth profile is approximated by finite layers and
tested for spatial convergence.

The waveform is periodic:

    sin^2(pi*t/T)*sin(6*pi*t/T)

Its nonzero positive Fourier harmonics have frequencies
2/T, 3/T and 4/T, with power weights 1:4:1.

IMPORTANT LIMITATIONS
---------------------
This is a steady-periodic frequency-response calculation,
not a finite-time startup or fully sourced toroidal pulse.

The matter profile is fixed, not mechanically evolved.
No microscopic pulse source is constructed.
The chosen theta values are diagnostic and are NOT the
spatially varying R3B toroidal loading coefficients.

The radiation impulse calculation is a one-pass control.
It does NOT bound near-field or universal-metric forces.

No claim of physical antigravity or spacecraft lift.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np


C = 299792458.0
G = 9.80665

MASS_KG = 1.0

B7_FIELD_CAPACITY_J = 1.5473042949759672

THETA_COMPARATOR = 18987.283771593688

L_M = 0.4
RAMP_M = 0.1
PULSE_CYCLES = 3

R = np.kron(
    np.eye(2),
    np.array([[0., -1.], [1., 0.]])
)

Q = np.kron(
    np.array([[0., 1.], [1., 0.]]),
    np.eye(2)
)

I4 = np.eye(4)
I8 = np.eye(8)

WPLUS = np.vstack((I4, R))
WMINUS = np.vstack((I4, -R))


def smoothstep(u):
    """C2 transition with zero endpoint derivatives."""
    x = min(1., max(0., u))
    return x*x*x*(10. + x*(-15. + 6.*x))


def theta_at(x, amplitude):
    """Smooth compact material coupling."""
    left = smoothstep(x/RAMP_M)
    right = smoothstep((L_M-x)/RAMP_M)

    return amplitude*left*right


def homogeneous_transfer(theta, frequency_hz, dx):
    """Exact Lorentzian two-carrier layer propagator.

    The physical state contains transverse E and H.

    K^2 = identity analytically.

    Consequently:

        exp(i*k*dx*K)
          = cos(k*dx)*I + i*sin(k*dx)*K
    """
    kdx = 2.*math.pi*frequency_hz*dx/C

    K = np.block([
        [-theta*(R@Q), -R],
        [(1.+theta*theta)*R, theta*(R@Q)],
    ])

    return (
        np.cos(kdx)*I8
        + 1j*np.sin(kdx)*K
    )


def response(frequency_hz, amplitude, n_cells=128):
    """Scattering for four carrier/polarization basis states."""
    if frequency_hz < 0 or n_cells < 8:
        raise ValueError("Invalid frequency or grid")

    dx = L_M/n_cells

    transfer = I8.astype(complex)

    for cell in range(n_cells):
        theta = theta_at(
            (cell+.5)*dx,
            amplitude
        )

        transfer = (
            homogeneous_transfer(
                theta, frequency_hz, dx
            ) @ transfer
        )

    # Incoming forward wave from the left.
    # Unknown reflected and transmitted amplitudes.
    left = transfer@WMINUS
    right = -WPLUS

    solution = np.linalg.solve(
        np.concatenate((left, right), axis=1),
        -transfer@WPLUS
    )

    reflected = solution[:4, :]
    transmitted = solution[4:, :]

    reflectance = np.sum(
        abs(reflected)**2,
        axis=0
    ).real

    transmittance = np.sum(
        abs(transmitted)**2,
        axis=0
    ).real

    balance_error = float(
        np.max(
            abs(
                reflectance + transmittance - 1.
            )
        )
    )

    return {
        "reflectance":
            float(np.mean(reflectance)),

        "transmittance":
            float(np.mean(transmittance)),

        "conservation_residual":
            balance_error,

        "polarization_spread":
            float(
                max(reflectance)-min(reflectance)
            ),
    }


def periodic_pulse_response(
    period_s,
    amplitude,
    n_cells=128
):
    """Exact harmonic response for a repeated smooth pulse."""
    harmonic_indices = (
        PULSE_CYCLES-1,
        PULSE_CYCLES,
        PULSE_CYCLES+1
    )

    weights = (
        1./6.,
        4./6.,
        1./6.
    )

    rows = [
        response(k/period_s, amplitude, n_cells)
        for k in harmonic_indices
    ]

    average_r = sum(
        w*r["reflectance"]
        for w, r in zip(weights, rows)
    )

    average_t = sum(
        w*r["transmittance"]
        for w, r in zip(weights, rows)
    )

    worst_error = max(
        r["conservation_residual"]
        for r in rows
    )

    # HYPOTHETICAL one-pass incident radiation energy.
    # Not the actual B7 generator's operating energy.
    incident_j = B7_FIELD_CAPACITY_J

    radiation_impulse = (
        2.*average_r*incident_j/C
    )

    radiation_acceleration = (
        radiation_impulse
        /(MASS_KG*period_s)
    )

    # Perfect-reflection, one-pass photon momentum limit.
    required_j = (
        MASS_KG*G*period_s*C/2.
    )

    return {
        "period_ms":
            period_s*1000.,

        "carrier_hz":
            PULSE_CYCLES/period_s,

        "coupling_theta_control":
            amplitude,

        "mean_power_reflectance":
            average_r,

        "mean_power_transmittance":
            average_t,

        "power_balance_residual":
            worst_error,

        "one_pass_radiation_impulse_if_incident_energy_eq_b7_capacity_kg_m_s":
            radiation_impulse,

        "one_pass_radiation_acceleration_if_incident_energy_eq_b7_capacity_m_s2":
            radiation_acceleration,

        "one_pass_ideal_perfect_mirror_energy_required_for_1g_j":
            required_j,

        "one_pass_ideal_perfect_mirror_power_required_for_1g_w":
            required_j/period_s,

        "one_pass_1g_with_strictly_less_than_10mj_even_ideal_mirror_possible":
            required_j < 10e6,

        "harmonics_hz": [
            k/period_s
            for k in harmonic_indices
        ],

        "harmonic_results":
            rows,
    }


def main():
    # Analytical propagator identity.
    # Relative normalization prevents large-theta
    # floating-point cancellation from causing a
    # spurious failure in the K^2 identity.
    for theta in (
        0.,
        20.,
        THETA_COMPARATOR
    ):
        K = np.block([
            [-theta*(R@Q), -R],
            [
                (1.+theta*theta)*R,
                theta*(R@Q)
            ],
        ])

        relative_error = (
            np.linalg.norm(K@K-I8)
            /max(1., np.linalg.norm(K)**2)
        )

        assert relative_error < 1e-12

    # Vacuum control: no artificial reflection.
    for frequency in (
        100.,
        1000.,
        10000.
    ):
        check = response(frequency, 0.)

        assert check["reflectance"] < 1e-18
        assert check["conservation_residual"] < 1e-9

    results = []

    for period_ms in (
        0.1,
        1.0,
        10.0
    ):
        for theta in (
            0.,
            20.,
            THETA_COMPARATOR
        ):
            row = periodic_pulse_response(
                period_ms/1000.,
                theta
            )

            assert (
                row["power_balance_residual"] < 1e-8
            ), row

            assert abs(
                row["mean_power_reflectance"]
                + row["mean_power_transmittance"]
                - 1.
            ) < 1e-8

            results.append(row)

            print(
                f"T={period_ms:5g} ms "
                f"theta={theta:12.4f} "
                f"R={row['mean_power_reflectance']:.9g} "
                f"a_rad="
                f"{row['one_pass_radiation_acceleration_if_incident_energy_eq_b7_capacity_m_s2']:.9g} "
                f"m/s² "
                f"E_1g_min="
                f"{row['one_pass_ideal_perfect_mirror_energy_required_for_1g_j']:.6g} J",
                flush=True
            )

    # Independent smooth-interface grid refinement.
    refinement = []

    for theta in (
        20.,
        THETA_COMPARATOR
    ):
        coarse = periodic_pulse_response(
            .001, theta, 128
        )

        fine = periodic_pulse_response(
            .001, theta, 256
        )

        r128 = coarse["mean_power_reflectance"]
        r256 = fine["mean_power_reflectance"]

        absolute_diff = abs(r128-r256)

        relative_diff = (
            absolute_diff/max(r256, 1e-30)
        )

        refinement.append({
            "theta": theta,
            "R128": r128,
            "R256": r256,
            "absolute_diff": absolute_diff,
            "relative_diff": relative_diff,
        })

        print(
            f"REFINEMENT theta={theta:.4f} "
            f"R128={r128:.12g} "
            f"R256={r256:.12g} "
            f"rel={relative_diff:.3e}"
        )

        assert absolute_diff < 0.005

    # Light propagation is far faster than the
    # chosen millisecond pulse period.
    gap_light_time_s = 1.0/C

    assert gap_light_time_s < 4e-9

    output = {
        "branch":
            "032H17A12D1R3X3B11_M1",

        "classification":
            "MILLISECOND_PERIODIC_TWO_U1_FIXED_MATTER_PLANAR_FREQUENCY_GATE",

        "periods_ms":
            [0.1, 1., 10.],

        "pulse_shape":
            "periodic sin^2(pi t/T) sin(6 pi t/T)",

        "harmonic_power_weights":
            [1./6., 4./6., 1./6.],

        "source_payload_light_travel_time_ns":
            1e9/C,

        "B7_preloaded_field_energy_reference_j":
            B7_FIELD_CAPACITY_J,

        "radiative_budget_energy_is_hypothetical_not_B7_source":
            True,

        "planar_theta20_is_illustrative":
            True,

        "large_theta_is_historical_spherical_comparator_not_toroid":
            True,

        "microscopic_millisecond_source_realized":
            False,

        "one_actual_R3B_toroidal_pulse_simulated":
            False,

        "full_loaded_motion_simulated":
            False,

        "closed_whole_craft_lift":
            False,

        "complete_operating_energy_certified":
            False,

        "one_pass_energy_bound_does_not_apply_to_recirculating_or_near_fields":
            True,

        "results":
            results,

        "refinement":
            refinement,
    }

    path = Path(
        "results/data/"
        "032h17a12d1r3x3b11_millisecond_frequency_gate_summary.json"
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    path.write_text(
        json.dumps(
            output,
            indent=2,
            sort_keys=True
        ) + "\n",
        encoding="utf8"
    )

    print("RESULT=", path)
    print("MILLISECOND_PERIODIC_SCATTERING=PASS_SCOPED")
    print("LOADED_R3B_TOROIDAL_PULSE=NOT_TESTED")


if __name__ == "__main__":
    main()
