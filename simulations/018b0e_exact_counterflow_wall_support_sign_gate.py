#!/usr/bin/env python3
"""Simulation 018B-0E — exact-counterflow wall-support sign gate.

PURPOSE
-------
Test whether the exact momentum-cancelled, literature-backed two-current
string selected by 018B-0D can serve as the static compressive rim required
by the validated nonthermal KLS wall architecture.

SCIENTIFIC QUESTION
-------------------
018B-0D established a healthy two-current microscopic string state with:

    two localized condensates;
    exact integer-compatible 3:-4 counterwinding;
    essentially zero integrated longitudinal momentum flux;
    positive energy per length U;
    positive physical string tension T;
    transverse and longitudinal stability;
    a robust local elastic neighborhood.

Can that exact-counterflow state provide the positive tangential compression
required to hold the KLS membrane in static radial equilibrium?

MODEL / SIGN CONVENTION
-----------------------
For an elastic string in its zero-momentum eigenframe,

    worldsheet stress = diag(U, -T),

where:

    U > 0 is energy per unit length;
    T > 0 is physical string tension.

Thus the longitudinal pressure is

    P_parallel = -T.

The KLS membrane has positive wall tension sigma_W. At a circular boundary of
radius R, its inward line load has magnitude

    sigma_W R.

The established drum/rim convention requires the boundary rim to provide
positive azimuthal compression:

    P_parallel = +sigma_W R

for a static zero-momentum rim.

Therefore if exact momentum cancellation puts the string in its eigenframe
and transverse stability requires T > 0, the signs are incompatible:

    P_parallel = -T < 0
    sigma_W R > 0.

This is a sign obstruction, not a precision optimization.

INPUTS
------
Read directly from existing project logs:

018B-0D:
    ENERGY_PER_LENGTH_U
    TENSION_T
    CT2=T_OVER_U
    COUNTERFLOW_C_RELATIVE
    LOOP_RADIUS_FROM_NPHI_3
    LOOP_RADIUS_FROM_NSIGMA_4

018A-8:
    WALL_TENSION

VALIDATION
----------
- Verify the two integer radius reconstructions agree.
- Verify c_T^2 agrees independently with T/U.
- Verify momentum cancellation is numerically negligible.
- Verify U > 0, T > 0, sigma_W > 0, R > 0.
- Evaluate the explicit selected-point wall load.
- Evaluate the formal static balance radius

      R_balance = -T / sigma_W.

  A negative R_balance proves that no positive-radius static solution exists
  for the exact-counterflow state.

GENERALIZED RESULT
------------------
For any exact zero-momentum elastic state satisfying

    U > 0
    c_T^2 = T/U > 0

one has

    T > 0

and hence

    P_parallel = -T < 0.

Consequently it cannot statically balance a positive-tension membrane requiring

    P_parallel = +sigma_W R > 0

without an additional support mechanism.

STOP RULE
---------
If the sign obstruction is confirmed:

    DO NOT

run the KLS-wall junction/gravity revalidation using the exact-counterflow
018B-0D point.

Instead search the same literature-backed two-current microscopic model for a
STATIONARY nonzero-momentum state with:

    T_tphi != 0;
    positive laboratory-frame P_parallel;
    wall balance;
    integer winding;
    two localized currents;
    elastic stability;
    finite-payload outward gravity.

Any such state must carry angular momentum and therefore requires the planned
stationary/frame-dragging bookkeeping.

CLAIM LIMITS
------------
This gate does not reject:

- the Lilley-Martin-Peter two-current string model;
- two-current vortons;
- nonzero-momentum stationary states;
- the validated 018A-8 source-level result;
- the KLS wall;
- gravitational repulsion.

It rejects only the exact zero-momentum 018B-0D state as the static compressive
boundary of the KLS membrane.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_018B0E_EXACT_COUNTERFLOW_STATIC_WALL_SUPPORT_SIGN_GATE
"""

from __future__ import annotations

import math
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]

D_LOG = (
    ROOT
    / "results/logs"
    / "018b0d_literature_two_current_counterflow_gate.log"
)

A8_LOG = (
    ROOT
    / "results/logs"
    / "018a8_finite_thickness_payload_kernel_closeout.log"
)


def read_scalar(path: Path, label: str) -> float:
    """Read one finite floating-point result from an existing project log."""

    text = path.read_text(errors="replace")

    pattern = (
        re.escape(label)
        +
        r"([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)"
    )

    match = re.search(pattern, text)

    if match is None:
        raise RuntimeError(
            f"Could not find {label!r} in {path}"
        )

    value = float(match.group(1))

    if not math.isfinite(value):
        raise RuntimeError(
            f"Nonfinite {label!r} in {path}"
        )

    return value


def main() -> None:
    """Run the exact-counterflow wall-support sign closeout."""

    print(
        "=== 018B-0E — EXACT COUNTERFLOW STATIC WALL SUPPORT SIGN GATE ==="
    )

    if not D_LOG.exists():
        raise RuntimeError(
            f"Missing 018B-0D log: {D_LOG}"
        )

    if not A8_LOG.exists():
        raise RuntimeError(
            f"Missing 018A-8 log: {A8_LOG}"
        )

    u = read_scalar(
        D_LOG,
        "ENERGY_PER_LENGTH_U=",
    )

    tension = read_scalar(
        D_LOG,
        "TENSION_T=",
    )

    ct2_reported = read_scalar(
        D_LOG,
        "CT2=T_OVER_U=",
    )

    counterflow_relative = read_scalar(
        D_LOG,
        "COUNTERFLOW_C_RELATIVE=",
    )

    r_phi = read_scalar(
        D_LOG,
        "LOOP_RADIUS_FROM_NPHI_3=",
    )

    r_sigma = read_scalar(
        D_LOG,
        "LOOP_RADIUS_FROM_NSIGMA_4=",
    )

    sigma_wall = read_scalar(
        A8_LOG,
        "WALL_TENSION=",
    )

    radius_relerr = (
        abs(r_phi - r_sigma)
        /
        max(
            abs(r_phi),
            abs(r_sigma),
            1.0e-30,
        )
    )

    radius = 0.5 * (
        r_phi
        +
        r_sigma
    )

    ct2_direct = (
        tension
        /
        u
    )

    ct2_relerr = (
        abs(
            ct2_direct
            -
            ct2_reported
        )
        /
        max(
            abs(ct2_reported),
            1.0e-30,
        )
    )

    # Exact-counterflow state is in its integrated zero-momentum frame.
    #
    # Positive T is string tension, so longitudinal pressure is -T.
    p_parallel = (
        -tension
    )

    required_wall_compression = (
        sigma_wall
        *
        radius
    )

    equilibrium_residual = (
        p_parallel
        -
        required_wall_compression
    )

    formal_balance_radius = (
        p_parallel
        /
        sigma_wall
    )

    print(
        "\n=== RECONSTRUCTED 018B-0D STATE ==="
    )

    print(
        f"ENERGY_PER_LENGTH_U={u:+.15e}"
    )

    print(
        f"STRING_TENSION_T={tension:+.15e}"
    )

    print(
        f"CT2_REPORTED={ct2_reported:+.15e}"
    )

    print(
        f"CT2_DIRECT_T_OVER_U={ct2_direct:+.15e}"
    )

    print(
        f"CT2_RECONSTRUCTION_RELERR={ct2_relerr:.15e}"
    )

    print(
        f"COUNTERFLOW_C_RELATIVE={counterflow_relative:.15e}"
    )

    print(
        f"RADIUS_FROM_NPHI={r_phi:.15e}"
    )

    print(
        f"RADIUS_FROM_NSIGMA={r_sigma:.15e}"
    )

    print(
        f"INTEGER_RADIUS_RELERR={radius_relerr:.15e}"
    )

    print(
        "\n=== KLS WALL LOAD ==="
    )

    print(
        f"WALL_TENSION_SIGMA_W={sigma_wall:+.15e}"
    )

    print(
        f"SELECTED_LOOP_RADIUS={radius:+.15e}"
    )

    print(
        "REQUIRED_POSITIVE_RIM_COMPRESSION="
        f"{required_wall_compression:+.15e}"
    )

    print(
        "\n=== EXACT-COUNTERFLOW LONGITUDINAL STRESS ==="
    )

    print(
        "ZERO_MOMENTUM_FRAME_LONGITUDINAL_PRESSURE="
        f"{p_parallel:+.15e}"
    )

    print(
        "STATIC_BALANCE_RESIDUAL_PPAR_MINUS_SIGMA_R="
        f"{equilibrium_residual:+.15e}"
    )

    print(
        "FORMAL_STATIC_BALANCE_RADIUS_PPAR_OVER_SIGMA="
        f"{formal_balance_radius:+.15e}"
    )

    numerical_reconstruction = (
        radius_relerr
        <
        1.0e-12
        and
        ct2_relerr
        <
        1.0e-12
        and
        counterflow_relative
        <
        1.0e-12
    )

    physical_sign_inputs = (
        u > 0.0
        and
        tension > 0.0
        and
        ct2_direct > 0.0
        and
        sigma_wall > 0.0
        and
        radius > 0.0
    )

    selected_sign_obstruction = (
        p_parallel < 0.0
        and
        required_wall_compression > 0.0
        and
        formal_balance_radius < 0.0
    )

    generalized_obstruction = (
        u > 0.0
        and
        ct2_direct > 0.0
        and
        tension > 0.0
        and
        sigma_wall > 0.0
    )

    print(
        "\n=== VALIDATION ==="
    )

    print(
        "NUMERICAL_RECONSTRUCTION="
        + (
            "PASS"
            if numerical_reconstruction
            else "FAIL"
        )
    )

    print(
        "POSITIVE_U_T_SIGMA_AND_RADIUS="
        + (
            "PASS"
            if physical_sign_inputs
            else "FAIL"
        )
    )

    print(
        "SELECTED_COUNTERFLOW_STATIC_SUPPORT_SIGN="
        + (
            "FAIL"
            if selected_sign_obstruction
            else "NOT_REJECTED"
        )
    )

    print(
        "GENERAL_STABLE_ZERO_MOMENTUM_STATIC_SUPPORT="
        + (
            "REJECTED_FOR_POSITIVE_TENSION_WALL"
            if generalized_obstruction
            else "NOT_ESTABLISHED"
        )
    )

    print(
        "\n=== DECISION ==="
    )

    green_negative = (
        numerical_reconstruction
        and
        physical_sign_inputs
        and
        selected_sign_obstruction
        and
        generalized_obstruction
    )

    if green_negative:

        print(
            "018B0E_EXACT_COUNTERFLOW_WALL_SUPPORT_GATE="
            "GREEN_NEGATIVE_RESULT"
        )

        print(
            "EXACT_COUNTERFLOW_TWO_CURRENT_RIM_AS_STATIC_KLS_BOUNDARY="
            "REJECTED"
        )

        print(
            "018B0D_TWO_CURRENT_MICROSCOPIC_STRING_RESULT="
            "PRESERVED"
        )

        print(
            "TWO_CURRENT_ROUTE="
            "PRESERVED_FOR_STATIONARY_NONZERO_MOMENTUM_STATES"
        )

        print(
            "NEXT="
            "018B0F_STATIONARY_TWO_CURRENT_POSITIVE_PPAR_"
            "INTEGER_WALL_BALANCE_SEARCH"
        )

    else:

        print(
            "018B0E_EXACT_COUNTERFLOW_WALL_SUPPORT_GATE="
            "RED_OR_UNRESOLVED"
        )

        print(
            "NEXT="
            "AUDIT_SIGN_CONVENTIONS_BEFORE_ESCALATION"
        )

    print(
        "CURRENT_HEURISTIC="
        "APPROXIMATELY_66_PERCENT_NOT_A_PROBABILITY"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )

    print(
        "NEW_PHYSICS_DISCOVERY=NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_018B0E_EXACT_COUNTERFLOW_"
        "STATIC_WALL_SUPPORT_SIGN_GATE"
    )


if __name__ == "__main__":
    main()
