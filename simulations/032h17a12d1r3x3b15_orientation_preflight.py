"""032H17A12D1R3X3B15-M0 — 3D source-orientation preflight.

PURPOSE
-------
Test whether rotating the complete R3B mixed electric/magnetic source
relative to the fixed 1 kg neutral torus introduces physical modes
missing from the original axisymmetric solver.

THEORY
------
Outside the spherical source, use the original R3B multipole field:

    Psi = sum_l a_l (Rs/r)^(l+1) P_l(axis dot rhat)
    B = -grad(Psi)

The aligned mirror has E = -B. The tested physical-metric convention is

    sigma = KAPPA E dot B
    KAPPA = -2 (hbar c)^2 / M^4
    a_z = -c^2 d_z sigma

Only proper SO(3) rotations are used. The source support remains
inside a sphere of radius 2 m. B7's 10 cm electric charge layer
preserves the same exterior field under proper rotation.

METHOD
------
1. Prove/test rigid rotational covariance.
2. Check exact finite-torus source clearance.
3. Test simultaneous and single-sector polarity reversals.
4. Rotate the source relative to the fixed torus.
5. Evaluate independent opposed, perpendicular and oblique sources.
6. Track three-dimensional azimuthal modes and finite-difference error.
7. Optionally reconstruct the actual R3B multipole amplitudes.

LIMITATIONS
-----------
This is a static preloaded exterior calculation, NOT a loaded 3D
Maxwell/matter solution. No fully coupled source reaction, microscopic
realization, stability, complete field energy or device is certified.

A sampled local acceleration is not a continuum everywhere-force
certificate. All reported units follow the repository's R3B convention.

CLAIM CLASSIFICATION
--------------------
THEOREM_AND_PRELOADED_GEOMETRY_PREFLIGHT_ONLY
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import Legendre

C_LIGHT = 299792458.0
HBAR_C_EV_M = 1.973269804e-7
M_EV = 1000.0
KAPPA = -2.0 * HBAR_C_EV_M**2 / M_EV**4

SOURCE_RADIUS = 2.0
MAJOR_RADIUS = 1.0
MINOR_RADIUS = 0.2
GRAVITY = 9.80665

TORUS_Z = math.sqrt(
    (SOURCE_RADIUS + 1.0 + MINOR_RADIUS)**2
    - MAJOR_RADIUS**2
)

BRANCH = "032H17A12D1R3X3B15-M0"


def unit(vector):
    vector = np.asarray(vector, dtype=float)
    norm = float(np.linalg.norm(vector))

    if vector.shape != (3,) or not np.isfinite(norm) or norm <= 0:
        raise ValueError("Invalid source axis")

    return vector / norm


def rodrigues(axis, angle_deg):
    axis = unit(axis)
    x, y, z = axis

    skew = np.array([
        [0.0, -z, y],
        [z, 0.0, -x],
        [-y, x, 0.0],
    ])

    angle = np.deg2rad(angle_deg)

    return (
        np.eye(3)
        + math.sin(angle) * skew
        + (1.0 - math.cos(angle)) * (skew @ skew)
    )


@dataclass(frozen=True)
class Source:
    center: tuple[float, float, float]
    e_axis: tuple[float, float, float]
    b_axis: tuple[float, float, float]
    e_gain: float = 1.0
    b_gain: float = 1.0


def exterior_b(points, center, axis, amplitudes):
    """Evaluate exact exterior magnetic multipoles in Cartesian 3D."""
    points = np.asarray(points, dtype=float)
    center = np.asarray(center, dtype=float)
    axis = unit(axis)

    relative = points - center
    radius = np.linalg.norm(relative, axis=-1)

    if np.any(radius <= SOURCE_RADIUS):
        raise ValueError(
            "Exterior multipole evaluated inside source support"
        )

    rhat = relative / radius[..., None]
    cosine = np.clip(
        np.sum(rhat * axis, axis=-1),
        -1.0,
        1.0,
    )

    result = np.zeros_like(points)

    for ell, amplitude in enumerate(amplitudes, start=1):
        polynomial = Legendre.basis(ell)

        coefficient = (
            float(amplitude)
            * (SOURCE_RADIUS / radius)**(ell + 1)
            / radius
        )

        radial_part = (
            (ell + 1)
            * polynomial(cosine)[..., None]
            * rhat
        )

        angular_part = (
            polynomial.deriv()(cosine)[..., None]
            * (axis - cosine[..., None] * rhat)
        )

        result += (
            coefficient[..., None]
            * (radial_part - angular_part)
        )

    return result


def fields(points, sources, amplitudes):
    points = np.asarray(points, dtype=float)

    electric = np.zeros_like(points)
    magnetic = np.zeros_like(points)

    for source in sources:
        electric -= source.e_gain * exterior_b(
            points,
            source.center,
            source.e_axis,
            amplitudes,
        )

        magnetic += source.b_gain * exterior_b(
            points,
            source.center,
            source.b_axis,
            amplitudes,
        )

    return electric, magnetic


def sigma(points, sources, amplitudes):
    electric, magnetic = fields(
        points,
        sources,
        amplitudes,
    )

    return KAPPA * np.sum(
        electric * magnetic,
        axis=-1,
    )


def acceleration_z(
    points,
    sources,
    amplitudes,
    step=0.004,
):
    displacement = np.array([0.0, 0.0, step])

    return -C_LIGHT**2 * (
        sigma(points + displacement, sources, amplitudes)
        - sigma(points - displacement, sources, amplitudes)
    ) / (2.0 * step)


def torus_points():
    """Sample finite torus interior and boundary in three dimensions."""
    azimuth = np.arange(48) * 2.0 * math.pi / 48
    theta = np.arange(24) * 2.0 * math.pi / 24

    fractions = np.array([
        0.0,
        0.25,
        0.50,
        0.75,
        0.95,
        1.00,
    ])

    fraction, angle, phi = np.meshgrid(
        fractions,
        theta,
        azimuth,
        indexing="ij",
    )

    rho = (
        MAJOR_RADIUS
        + MINOR_RADIUS * fraction * np.cos(angle)
    )

    return np.stack([
        rho * np.cos(phi),
        rho * np.sin(phi),
        TORUS_Z + MINOR_RADIUS * fraction * np.sin(angle),
    ], axis=-1)


def exact_support_gap(center):
    """Analytical minimum gap between a source ball and entire torus."""
    center = np.asarray(center, dtype=float)

    center_rho = math.hypot(
        center[0],
        center[1],
    )

    distance_to_centerline = math.hypot(
        center_rho - MAJOR_RADIUS,
        center[2] - TORUS_Z,
    )

    return (
        distance_to_centerline
        - MINOR_RADIUS
        - SOURCE_RADIUS
    )


def make_source(
    center=(0, 0, 0),
    axis=(0, 0, 1),
    e_gain=1.0,
    b_gain=1.0,
):
    direction = tuple(unit(axis))

    return Source(
        tuple(float(value) for value in center),
        direction,
        direction,
        float(e_gain),
        float(b_gain),
    )


def covariance_check(amplitudes):
    rng = np.random.default_rng(15)

    points = (
        rng.normal(size=(64, 3)) * 0.35
        + np.array([0.7, 0.0, 3.6])
    )

    axis = unit([0.23, -0.61, 0.81])
    rotation = rodrigues([1, 2, 3], 67.0)

    original = Source(
        (0.0, 0.0, 0.0),
        tuple(axis),
        tuple(axis),
    )

    rotated = Source(
        tuple(rotation @ np.zeros(3)),
        tuple(rotation @ axis),
        tuple(rotation @ axis),
    )

    electric, magnetic = fields(
        points,
        [original],
        amplitudes,
    )

    electric_rot, magnetic_rot = fields(
        points @ rotation.T,
        [rotated],
        amplitudes,
    )

    error = max(
        np.max(np.abs(electric_rot - electric @ rotation.T)),
        np.max(np.abs(magnetic_rot - magnetic @ rotation.T)),
    )

    normalizer = max(
        np.max(np.abs(electric)),
        np.max(np.abs(magnetic)),
        1e-15,
    )

    scalar_error = np.max(np.abs(
        sigma(points @ rotation.T, [rotated], amplitudes)
        - sigma(points, [original], amplitudes)
    ))

    scalar_normalizer = max(
        np.max(np.abs(sigma(points, [original], amplitudes))),
        1e-30,
    )

    return {
        "vector_relative_error": float(error / normalizer),
        "scalar_relative_error": float(
            scalar_error / scalar_normalizer
        ),
        "pass": bool(
            error / normalizer < 1e-11
            and scalar_error / scalar_normalizer < 1e-11
        ),
    }


def configurations():
    configurations = {
        "aligned_original": [make_source()],
    }

    for angle in (30, 60, 90, 135, 180):
        axis = (
            rodrigues([0, 1, 0], angle)
            @ np.array([0, 0, 1])
        )

        configurations[f"relative_tilt_{angle}deg"] = [
            make_source(axis=axis),
        ]

    # Electric and magnetic source sectors physically rotated
    # relative to one another, rather than a coordinate rotation.
    configurations["sector_only_electric_90deg"] = [
        Source(
            (0.0, 0.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.0, 0.0, 1.0),
        ),
    ]

    # Two disjoint source balls; both retain >=1 m clearance.
    configurations["two_sources_opposed"] = [
        make_source(e_gain=0.5, b_gain=0.5),
        make_source(
            center=(0, 0, 6.5),
            axis=(0, 0, -1),
            e_gain=0.5,
            b_gain=0.5,
        ),
    ]

    configurations["two_sources_perpendicular"] = [
        make_source(e_gain=0.5, b_gain=0.5),
        make_source(
            center=(0, 0, 6.5),
            axis=(1, 0, 0),
            e_gain=0.5,
            b_gain=0.5,
        ),
    ]

    configurations["two_sources_oblique"] = [
        make_source(e_gain=0.5, b_gain=0.5),
        make_source(
            center=(0, 0, 6.5),
            axis=(1, 1, 1),
            e_gain=0.5,
            b_gain=0.5,
        ),
    ]

    return configurations


def source_dict(source):
    return {
        "center_m": list(source.center),
        "electric_axis": list(source.e_axis),
        "magnetic_axis": list(source.b_axis),
        "e_gain": source.e_gain,
        "b_gain": source.b_gain,
        "exact_support_gap_m": exact_support_gap(source.center),
    }


def analyze(amplitudes, provenance):
    points = torus_points()
    covariance = covariance_check(amplitudes)

    if not covariance["pass"]:
        raise AssertionError("SO(3) covariance failure")

    results = {}

    for name, sources in configurations().items():
        gaps = [
            exact_support_gap(source.center)
            for source in sources
        ]

        if min(gaps) < 1.0 - 1e-10:
            raise AssertionError((name, gaps))

        metric = sigma(
            points,
            sources,
            amplitudes,
        )

        accel_coarse = acceleration_z(
            points,
            sources,
            amplitudes,
            step=0.004,
        )

        accel_fine = acceleration_z(
            points,
            sources,
            amplitudes,
            step=0.002,
        )

        derivative_error = (
            np.max(np.abs(accel_coarse - accel_fine))
            / max(np.max(np.abs(accel_fine)), 1e-15)
        )

        azimuthal_modulation = (
            np.sqrt(np.mean(
                (metric - metric.mean(axis=-1, keepdims=True))**2
            ))
            / max(np.sqrt(np.mean(metric**2)), 1e-30)
        )

        results[name] = {
            "source_support": [
                source_dict(source)
                for source in sources
            ],
            "preloaded_min_az_m_s2": float(np.min(accel_fine)),
            "preloaded_max_az_m_s2": float(np.max(accel_fine)),
            "preloaded_mean_sample_az_m_s2": float(
                np.mean(accel_fine)
            ),
            "preloaded_every_sample_1g": bool(
                np.min(accel_fine) >= GRAVITY
            ),
            "sigma_azimuthal_modulation_fraction": float(
                azimuthal_modulation
            ),
            "central_difference_step_relative_delta": float(
                derivative_error
            ),
            "nonaxisymmetric_source_relative_to_torus": bool(
                azimuthal_modulation > 1e-9
            ),
            "fully_loaded_3d_solved": False,
            "full_field_energy_j": None,
            "source_reaction_certified": False,
        }

    return {
        "branch": BRANCH,
        "model": "vacuum_exterior_3d_preloaded_orientation_ONLY",
        "source_data_provenance": provenance,
        "proper_rotation_covariance": covariance,
        "global_rigid_rotation_control": "EXACT_SYMMETRY_NO_GAIN",
        "joint_sign_flip_control": "E_DOT_B_UNCHANGED_EXACT",
        "single_sector_sign_flip_control":
            "E_DOT_B_SIGN_REVERSES_EXACT",
        "toroidal_payload_center_z_m": TORUS_Z,
        "sample_shape": list(points.shape),
        "entries": results,
        "loaded_1g_established": False,
        "full_microscopic_action_established": False,
        "006d_replaced": False,
        "certified_sub10mj_device": False,
        "decision":
            "3D_M_NONZERO_POSSIBLE_BUT_LOADED_3D_ACTION_BVP_REQUIRED",
    }


def r3b_amplitudes(h):
    """Recompute the original R3B finite-grid normalization and energy."""
    from antigravity_research.agminer.hook17_concurrent_u1_fieldstrength_metric import (
        REFERENCE_PORTAL_SCALE_EV,
    )

    from antigravity_research.agminer.hook17_fdual_f_global_mirror_prefight import (
        PRIMARY_FIT_RADIUS_M,
        PRIMARY_LMAX,
        fit_exterior_multipoles,
        mirror_global_energy_gate,
        mirror_payload_reconstruction,
        reconstruct_a12c_field,
    )

    if REFERENCE_PORTAL_SCALE_EV != M_EV:
        raise AssertionError("Reference portal mismatch")

    field = reconstruct_a12c_field(h)

    fit = fit_exterior_multipoles(
        field,
        PRIMARY_FIT_RADIUS_M,
        PRIMARY_LMAX,
    )

    energy = mirror_global_energy_gate(
        field,
        fit,
    )

    reconstructed = mirror_payload_reconstruction(
        field,
        fit,
        energy,
    )

    normalization = reconstructed[
        "amplitude_squared_normalization_to_1g"
    ]

    if normalization is None:
        raise RuntimeError("R3B original outward sign lost")

    scale = math.sqrt(normalization)

    amplitudes = (
        np.asarray(fit["boundary_amplitudes"], dtype=float)
        * scale
        / math.sqrt(2.0)
    )

    provenance = {
        "kind": "actual_original_R3B_reconstruction",
        "h_m": h,
        "R3B_original_axisymmetric_preloaded_min_az_m_s2": float(
            reconstructed[
                "normalized_payload_acceleration_min_m_s2"
            ]
        ),
        "R3B_original_axisymmetric_canonical_preloaded_energy_j": float(
            reconstructed[
                "normalized_mixed_global_field_energy_j"
            ]
        ),
        "R3B_original_unscaled_min_az_m_s2": float(
            reconstructed[
                "payload_acceleration_min_before_renormalization_m_s2"
            ]
        ),
        "fit_rms_error": float(
            fit["relative_rms_field_residual"]
        ),
        "fitted_exterior_magnetic_energy_relative_error": float(
            fit["exterior_energy_relative_error"]
        ),
        "note": (
            "3D exterior uses the fitted multipoles for both sectors; "
            "original 2D R3B retains an independently solved magnetic field "
            "and its complete preloaded interior/exterior energy"
        ),
    }

    return amplitudes, provenance


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--reconstruct",
        action="store_true",
        help="Recompute original R3B multipoles and energy",
    )

    parser.add_argument(
        "--h",
        type=float,
        default=0.05,
    )

    args = parser.parse_args()

    if args.reconstruct:
        amplitudes, provenance = r3b_amplitudes(args.h)
    else:
        amplitudes = np.array([1.0] + [0.0] * 11)

        provenance = {
            "kind": "synthetic_ell1_ONLY",
            "not_R3B_normalized": True,
        }

    result = analyze(
        amplitudes,
        provenance,
    )

    root = Path(__file__).resolve().parents[1]

    tag = (
        f"h{round(args.h * 1000):03d}_"
        + ("r3b" if args.reconstruct else "synthetic")
    )

    path = (
        root
        / "results"
        / "data"
        / f"032h17a12d1r3x3b15_orientation_{tag}_summary.json"
    )

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print("B15-M0", provenance["kind"])
    print(
        "SO3_COVARIANCE_PASS=",
        result["proper_rotation_covariance"]["pass"],
    )

    for name, row in result["entries"].items():
        gap = min(
            item["exact_support_gap_m"]
            for item in row["source_support"]
        )

        print(
            f"{name:35s} "
            f"min_a={row['preloaded_min_az_m_s2']:+.6g} "
            f"m_mode={row['sigma_azimuthal_modulation_fraction']:.5g} "
            f"gap={gap:.6g}"
        )

    print("LOADED_3D_SOLUTION=NO")
    print("RESULT=", path)


if __name__ == "__main__":
    main()
