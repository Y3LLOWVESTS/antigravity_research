#!/usr/bin/env python3
"""024B — spatiotemporal virial/kernel rectification and wall-pulse rerank gate.

PURPOSE
-------
Execute the first post-024A4R rerank slice without launching another large PDE
scan. The run asks whether nonperiodic/pulsed pure-GR operation can exploit the
same kernel-placement principle that made 006D efficient, while respecting the
full-cycle consequences of stress-energy conservation.

SCIENTIFIC QUESTION
-------------------
Can a conserved transient stress cycle place a negative-active-stress phase near
the payload and its compulsory positive/reset stress farther away strongly
enough to improve finite-payload impulse per peak source energy, and do known
wall-like scalar configurations provide a credible microscopic seed?

PHYSICAL MODEL
--------------
The run combines four deliberately separated levels:

1. STATIC ANCHOR
   Re-run 006D and protect its finite stand-off coefficient.

2. EXACT STRESS ARCHETYPES
   Canonical topological wall, Nambu string, and the exactly solvable Q-wall of
   MacKenzie & Paranjape, arXiv:hep-th/0104084.

3. RELAXED PULSE TEACHER
   A globally virial-closed two-phase DEC-saturating scalar-stress cycle with
   the repulsive phase at z=0 and reset at z=-d.

4. PRACTICALITY LEDGER
   Peak energy, causal lifetime scaling, fractional cycle loss, and power per
   average acceleration.

EQUATIONS
---------
For an isolated source with

    partial_mu T^{mu nu} = 0

and vanishing boundary flux,

    I_ij(t) = integral x_i x_j T^{00} d^3x

obeys

    d^2 I_ij / dt^2
        =
    2 integral T^{ij} d^3x.

Taking the trace,

    integral (T^{00} + T^{ii}) d^3x
        =
    E + 0.5 I''.

A closed cycle has Delta I'=0, hence

    integral_cycle dt integral T^{ii} d^3x
        =
    0.

Thus a negative-active phase requires compensating positive stress over the
full cycle. The possible loophole is spatial kernel leverage, not free DC
gravity.

For a canonical scalar in 3+1 dimensions,

    rho
        =
    0.5 phidot^2 + 0.5 |grad phi|^2 + V

and

    S
        =
    rho + sum_i p_i
        =
    2 phidot^2 - 2 V.

Spatial gradients cancel from S.

Potential-dominated regions can approach

    S/rho = -2

while homogeneous kinetic-dominated regions can approach

    S/rho = +4.

Both saturate the type-I DEC bounds.

The relaxed two-phase cycle uses equal stored energy E and equal hold times:

    near:
        p_i = -rho
        q = sum p_i = -3E
        S = -2E
        z = 0

    far:
        p_i = +rho
        q = +3E
        S = +4E
        z = -d

so the integrated virial stress closes exactly.

With a point-payload axial kernel and

    delta = d/h,

the relaxed cycle efficiency is

    eta_cycle
        =
    1 - 2/(1+delta)^2

and

    C_cycle
        =
    1/eta_cycle

when eta_cycle > 0.

THIS IS AN OPTIMISTIC RELAXED BOUND.

Transport, formation, local conservation, T^{0i}, retardation, radiation,
reaction momentum and reset are not solved.

For a thin topological domain-wall disk of radius

    R = x h,

with surface energy sigma and surface active source

    S_surface = -sigma,

the quasistatic point-payload coefficient is

    C_wall(x)
        =
    x^2 / [2(1 - 1/sqrt(1+x^2))]

which is algebraically identical to

    C_wall(x)
        =
    0.5 sqrt(1+x^2)
        [sqrt(1+x^2)+1].

If an unsupported wall patch lives for

    tau ~ xi R/c

before collapse, then the source-energy-per-impulse throughput factor is
proportional to

    C_wall / (xi x).

Its exact xi-independent minimum occurs at

    x_*
        =
    sqrt((1+sqrt(5))/2).

For a cycle losing fraction ell of peak stored energy,

    P_loss / a_avg
        =
    ell (C/x/xi) c^3 h / G.

The 1/G burden therefore survives pulsing.

FIELD CONTENT / REPRESENTATIONS
-------------------------------
- 006D:
    project-defined type-I stress tensor, re-run as an external anchor.

- Topological wall:
    canonical real scalar wall stress archetype.

- Q-wall:
    two real scalars with SO(2) charge and

        phi1 + i phi2
            =
        exp(i omega t) varphi.

- Relaxed rectifier:
    local DEC-extreme scalar stress phases, not a solved field.

SIGN CONVENTIONS
----------------
The payload lies at z=+h and all source phases satisfy z<=0.

Positive reported payload acceleration means upward/outward, away from the
source side.

For a source below the payload, negative active source S is productive.

UNITS
-----
Dimensionless geometry uses h=1.

SI conversion uses:

    c  = 299792458 m/s
    G  = 6.67430e-11 SI
    g0 = 9.80665 m/s^2.

INPUTS / OUTPUTS
----------------
Input:
    simulations/006d_finite_thickness_conserved_source.py

Audited comparator:
    B7 C = 422.222070908309

Outputs:
    results/data/
        024b_spatiotemporal_virial_kernel_rectification_summary.json

    results/data/
        024b_spatiotemporal_virial_kernel_rectification_scan.csv

The shell harness separately stores a timestamped stdout log.

ASSUMPTIONS / APPROXIMATION LEVEL
---------------------------------
- Weak-field/quasistatic axial kernel for instantaneous wall/rectifier scoring.
- Flat-background exact conservation identity for the virial theorem.
- Exact flat-space Q-wall stress audit for the cited analytic profile.
- No claim that the relaxed two-phase teacher is a local field solution.
- No static source multiplied by an arbitrary time envelope.
- Dynamic GR retardation is NOT treated as solved.
- Formation/reset/support/environment/reaction sectors remain mandatory.

BOUNDARY CONDITIONS
-------------------
The relaxed source phases are strict stand-off:

    z <= 0.

The Q-wall is the infinite planar analytic profile used only for
constitutive/stability screening.

The finite wall disk intentionally omits a stabilizing rim because it is a
collapse-pulse prefilter, not a static device.

CONSERVATION
------------
The exact integrated virial identity is the central conservation gate.

The relaxed two-phase model closes the cycle-integrated stress trace but does
NOT establish local spacetime conservation during transport, formation or
reset.

STABILITY / NATURALNESS
-----------------------
MacKenzie & Paranjape find the analytic Q-wall has a long-wavelength beading
instability, although its lifetime can become arbitrarily long near the
stability threshold.

This run first determines whether its stress is gravitationally useful before
considering lifetime as an engineering feature.

NUMERICAL METHOD
----------------
- Re-run and parse 006D.
- High-resolution 1D quadrature of the exact Q-wall profile.
- Compare Q-wall quadrature with analytic integrals.
- Closed-form wall-disk and rectifier calculations.
- Independent dense optimization cross-check of the wall optimum.
- Explicit SI energy and loss/recovery ledger.
- Separate physically motivated and blind-wildcard geometry scans.

VALIDATION
----------
006D must reproduce

    C = 23.591586299249

and its green conservation/DEC/outward-field labels.

The Q-wall must reproduce

    E/A
        =
    12/5

and

    integral S dx
        =
    4/15.

Pointwise Q-wall DEC must pass.

The two algebraic forms of C_wall must agree.

The dense wall optimum must reproduce the analytic golden-ratio optimum.

The two-phase virial stress must close exactly.

FALSIFICATION
-------------
The pulsed pure-GR route is NOT promoted to a physical field candidate if:

- no meaningful source-level headroom over 006D survives;
- candidate wall stress has the wrong active sign;
- apparent gain relies only on omitted transport/reset/local conservation;
- the complete cycle cannot close;
- absolute scaling remains proportional to 1/G;
- required energy recovery is prohibitive.

PROMOTION CONDITION
-------------------
A later expensive dynamic-field solve is authorized only if this prefilter
finds >=10x instantaneous/source-level headroom versus 006D in a strict
stand-off wall architecture AND identifies a literature-backed microscopic
transient whose stress sign is compatible with outward gravity.

This still does not constitute full-cycle promotion.

STOP RULE
---------
Do not launch another generalized-Skyrme, sextic, omega or isorotation scan
from this slice.

If no credible wall pulse survives:

- keep 006D as static source anchor;
- keep 023C as actual-field fallback;
- activate Analogue Antigravity in the practicality rerank.

LITERATURE ANCHORS
------------------
A. Vilenkin,
Phys. Rev. D 23, 852 (1981),
DOI 10.1103/PhysRevD.23.852.

J. Ipser and P. Sikivie,
Phys. Rev. D 30, 712 (1984),
DOI 10.1103/PhysRevD.30.712.

R.B. MacKenzie and M.B. Paranjape,
JHEP 08 (2001) 003,
arXiv:hep-th/0104084.

T. Hiramatsu et al.,
Phys. Rev. D 85, 105020 (2012),
arXiv:1202.5851.

RELATED FILES
-------------
simulations/006d_finite_thickness_conserved_source.py

simulations/int15_static_pulse_successor_blueprint_synthesis.py

simulations/024a4_true_standoff_teacher_reconstruction.py

simulations/024a4r_standoff_feasibility_decomposition.py

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_024B_ANALYTIC_NUMERICAL_PULSE_PREFILTER_AND_RERANK_GATE

This run does NOT establish:

- a conserved pulse field solution;
- dynamic or nonlinear GR certification;
- a practical energy source;
- experimental antigravity;
- a device.
"""

from __future__ import annotations

import csv
import json
import math
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results/data"

S006D = (
    SIM
    / "006d_finite_thickness_conserved_source.py"
)

OUT_JSON = (
    DATA
    / "024b_spatiotemporal_virial_kernel_rectification_summary.json"
)

OUT_CSV = (
    DATA
    / "024b_spatiotemporal_virial_kernel_rectification_scan.csv"
)


G = 6.67430e-11
C_LIGHT = 299_792_458.0
G0 = 9.80665

C006D_REFERENCE = 23.591586299249
CB7_REFERENCE = 422.222070908309


# User-requested blind wildcard values.
# These are explicitly diagnostics only and are not physics priors,
# optimization targets or evidence.
WILDCARDS = [
    0.625,
    1.6,
    1.875,
    3.125,
    5.0,
]


def trapz(
    y: np.ndarray,
    x: np.ndarray,
) -> float:
    """Version-tolerant trapezoidal integration."""

    if hasattr(
        np,
        "trapezoid",
    ):
        return float(
            np.trapezoid(
                y,
                x,
            )
        )

    return float(
        np.trapz(
            y,
            x,
        )
    )


def parse_float(
    text: str,
    labels: list[str],
) -> float:
    """Parse the first matching scalar label."""

    for label in labels:

        match = re.search(
            rf"^{re.escape(label)}="
            r"([+\-0-9.eE]+)$",
            text,
            flags=re.MULTILINE,
        )

        if match:

            return float(
                match.group(1)
            )

    raise RuntimeError(
        "None of the labels were found: "
        f"{labels}"
    )


def rerun_006d() -> dict[str, Any]:
    """Re-run the trusted static source anchor."""

    if not S006D.is_file():

        raise RuntimeError(
            "Missing required 006D source: "
            f"{S006D}"
        )

    env = dict(
        os.environ
    )

    env["PYTHONPATH"] = str(
        ROOT
        / "src"
    )

    proc = subprocess.run(
        [
            sys.executable,
            str(
                S006D
            ),
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    if proc.returncode != 0:

        raise RuntimeError(
            "006D subprocess failed:\n"
            + proc.stdout
            + "\n"
            + proc.stderr
        )

    text = proc.stdout

    c006d = parse_float(
        text,
        [
            "C_FINITE_BEST_TESTED",
            "FINEST_FINITE_C",
        ],
    )

    required = [
        "LOCAL_CONSERVATION=PASS",
        "DEC=PASS",
        "POSITIVE_FAR_FIELD_ACTIVE_MASS=YES",
        "SIMULATION_006D=GREEN",
    ]

    for item in required:

        if item not in text:

            raise RuntimeError(
                "006D missing required label: "
                f"{item}"
            )

    outward_ok = (
        "OUTWARD_GRAVITATIONAL_FIELD=YES"
        in text
        or
        "OUTWARD_LOCAL_FIELD_GL64=YES"
        in text
        or
        "OUTWARD_LOCAL_FIELD_NESTED=YES"
        in text
    )

    if not outward_ok:

        raise RuntimeError(
            "006D did not report "
            "an outward local field."
        )

    relative_error = (
        abs(
            c006d
            - C006D_REFERENCE
        )
        / C006D_REFERENCE
    )

    if (
        relative_error
        > 5.0e-10
    ):

        raise RuntimeError(
            "006D coefficient regression: "
            f"got {c006d}, "
            "expected "
            f"{C006D_REFERENCE}"
        )

    return {
        "c": c006d,
        "returncode":
            proc.returncode,
        "relative_error_vs_reference":
            relative_error,
    }


def wall_disk_c(
    x: float,
) -> float:
    """Stable closed-form wall-disk coefficient."""

    if x <= 0.0:

        raise ValueError(
            "x=R/h must be positive."
        )

    root = math.sqrt(
        1.0
        + x * x
    )

    return (
        0.5
        * root
        * (
            root
            + 1.0
        )
    )


def wall_disk_c_direct(
    x: float,
) -> float:
    """Independent direct wall coefficient."""

    return (
        x * x
        /
        (
            2.0
            * (
                1.0
                - 1.0
                / math.sqrt(
                    1.0
                    + x * x
                )
            )
        )
    )


def rectifier_c(
    delta: float,
) -> tuple[
    float,
    float,
]:
    """Return eta and C for relaxed virial rectifier."""

    if delta < 0.0:

        raise ValueError(
            "delta=d/h must be nonnegative."
        )

    eta = (
        1.0
        - 2.0
        / (
            1.0
            + delta
        ) ** 2
    )

    coefficient = (
        math.inf
        if eta <= 0.0
        else
        1.0 / eta
    )

    return (
        eta,
        coefficient,
    )


def qwall_audit() -> dict[
    str,
    float | str,
]:
    """Audit exact MacKenzie-Paranjape Q-wall."""

    # Dimensionless:
    #
    # omega = 1
    # phi0 = 1
    #
    # varphi = sech^2(x)

    coordinate = np.linspace(
        -14.0,
        14.0,
        400_001,
    )

    varphi = (
        1.0
        / np.cosh(
            coordinate
        ) ** 2
    )

    # V
    # =
    # (5/2) varphi^2
    # -
    # 2 varphi^3

    potential = (
        2.5
        * varphi**2
        - 2.0
        * varphi**3
    )

    k_time = (
        0.5
        * varphi**2
    )

    # Exact first integral:
    #
    # 0.5 varphi'^2
    # =
    # V
    # -
    # 0.5 varphi^2

    k_normal = (
        2.0
        * varphi**2
        - 2.0
        * varphi**3
    )

    rho = (
        k_time
        + k_normal
        + potential
    )

    p_normal = (
        k_time
        + k_normal
        - potential
    )

    p_tangent = (
        k_time
        - k_normal
        - potential
    )

    active = (
        rho
        + p_normal
        + 2.0
        * p_tangent
    )

    energy = trapz(
        rho,
        coordinate,
    )

    active_integral = trapz(
        active,
        coordinate,
    )

    gross_positive = trapz(
        np.maximum(
            active,
            0.0,
        ),
        coordinate,
    )

    gross_negative = trapz(
        np.minimum(
            active,
            0.0,
        ),
        coordinate,
    )

    dec_violation = max(
        float(
            np.max(
                np.abs(
                    p_normal
                )
                - rho
            )
        ),
        float(
            np.max(
                np.abs(
                    p_tangent
                )
                - rho
            )
        ),
        0.0,
    )

    normal_pressure_residual = float(
        np.max(
            np.abs(
                p_normal
            )
        )
    )

    # Analytic integrals:
    #
    # integral sech^4 x dx = 4/3
    # integral sech^6 x dx = 16/15
    #
    # rho
    # =
    # 5 sech^4
    # -
    # 4 sech^6
    #
    # S
    # =
    # -3 sech^4
    # +
    # 4 sech^6

    exact_energy = (
        12.0
        / 5.0
    )

    exact_active = (
        4.0
        / 15.0
    )

    if (
        abs(
            energy
            - exact_energy
        )
        > 2.0e-9
    ):

        raise RuntimeError(
            "Q-wall energy quadrature failed: "
            f"{energy}"
        )

    if (
        abs(
            active_integral
            - exact_active
        )
        > 2.0e-9
    ):

        raise RuntimeError(
            "Q-wall active-source quadrature "
            f"failed: {active_integral}"
        )

    if (
        dec_violation
        > 2.0e-12
    ):

        raise RuntimeError(
            "Q-wall DEC failed: "
            f"{dec_violation}"
        )

    if (
        normal_pressure_residual
        > 2.0e-12
    ):

        raise RuntimeError(
            "Q-wall normal-pressure "
            "first-integral residual: "
            f"{normal_pressure_residual}"
        )

    # Large-Q Q-wall inference:
    #
    # E_total ~ Q^(1/2) A^(1/2)
    #
    # at fixed Q:
    #
    # p_t
    # =
    # -dE/dA
    # =
    # -0.5 E/A
    #
    # therefore:
    #
    # S_surface / sigma
    # =
    # 1 + 2 p_t/sigma
    # =
    # 0.

    large_q_active_ratio = 0.0

    return {
        "energy_numeric":
            energy,

        "energy_exact":
            exact_energy,

        "active_numeric":
            active_integral,

        "active_exact":
            exact_active,

        "active_over_energy":
            active_integral
            / energy,

        "gross_positive_active":
            gross_positive,

        "gross_negative_active":
            gross_negative,

        "dec_violation":
            dec_violation,

        "normal_pressure_residual":
            normal_pressure_residual,

        "large_q_active_over_energy_inference":
            large_q_active_ratio,

        "direct_standoff_repulsion":
            "NO",

        "constitutive_classification":
            (
                "NET_ACTIVE_ATTRACTIVE_AT_"
                "FINITE_ANALYTIC_PROFILE_"
                "AND_ACTIVE_NEUTRAL_"
                "ASYMPTOTICALLY"
            ),
    }


def main() -> None:

    DATA.mkdir(
        parents=True,
        exist_ok=True,
    )

    anchor = (
        rerun_006d()
    )

    c006d = float(
        anchor["c"]
    )

    headroom_b7_to_006d = (
        CB7_REFERENCE
        / c006d
    )

    if (
        abs(
            headroom_b7_to_006d
            - 17.8971462772
        )
        > 5.0e-9
    ):

        raise RuntimeError(
            "B7/006D headroom regression."
        )

    qwall = (
        qwall_audit()
    )

    # Exact type-I DEC stress archetypes.

    archetypes = {

        "vacuum_like_scalar_phase": {
            "p_over_rho": [
                -1.0,
                -1.0,
                -1.0,
            ],
            "S_over_rho":
                -2.0,
        },

        "topological_domain_wall": {
            "p_over_rho": [
                0.0,
                -1.0,
                -1.0,
            ],
            "S_over_rho":
                -1.0,
        },

        "nambu_string": {
            "p_over_rho": [
                -1.0,
                0.0,
                0.0,
            ],
            "S_over_rho":
                0.0,
        },

        "stiff_scalar_reset": {
            "p_over_rho": [
                1.0,
                1.0,
                1.0,
            ],
            "S_over_rho":
                4.0,
        },
    }

    for (
        name,
        item,
    ) in archetypes.items():

        pressures = (
            item[
                "p_over_rho"
            ]
        )

        active_ratio = (
            1.0
            + sum(
                pressures
            )
        )

        if (
            abs(
                active_ratio
                - item[
                    "S_over_rho"
                ]
            )
            > 1.0e-15
        ):

            raise RuntimeError(
                "Archetype algebra failed: "
                f"{name}"
            )

        if (
            max(
                abs(
                    value
                )
                for value
                in pressures
            )
            > 1.0
        ):

            raise RuntimeError(
                "Archetype violates DEC: "
                f"{name}"
            )

    # Dynamic virial-closed two-phase cycle.

    q_near_over_e = (
        -3.0
    )

    q_far_over_e = (
        +3.0
    )

    s_near_over_e = (
        -2.0
    )

    s_far_over_e = (
        +4.0
    )

    cycle_q_over_e = (
        0.5
        * (
            q_near_over_e
            + q_far_over_e
        )
    )

    cycle_s_over_e = (
        0.5
        * (
            s_near_over_e
            + s_far_over_e
        )
    )

    if (
        abs(
            cycle_q_over_e
        )
        > 1.0e-15
    ):

        raise RuntimeError(
            "Virial two-phase stress "
            "failed to close."
        )

    if (
        abs(
            cycle_s_over_e
            - 1.0
        )
        > 1.0e-15
    ):

        raise RuntimeError(
            "Cycle-average global active "
            "source should equal E."
        )

    # Independent algebraic wall checks.

    for x_control in [
        0.25,
        0.5,
        1.0,
        1.6,
        3.125,
        5.0,
    ]:

        c_stable = (
            wall_disk_c(
                x_control
            )
        )

        c_direct = (
            wall_disk_c_direct(
                x_control
            )
        )

        relative_error = (
            abs(
                c_stable
                - c_direct
            )
            / c_stable
        )

        if (
            relative_error
            > 2.0e-13
        ):

            raise RuntimeError(
                "Wall coefficient dual-form "
                "check failed at "
                f"x={x_control}"
            )

    golden_ratio = (
        0.5
        * (
            1.0
            + math.sqrt(
                5.0
            )
        )
    )

    x_opt = math.sqrt(
        golden_ratio
    )

    c_wall_opt = (
        wall_disk_c(
            x_opt
        )
    )

    throughput_opt = (
        c_wall_opt
        / x_opt
    )

    # Dense independent optimum check.

    x_dense_grid = np.linspace(
        0.05,
        8.0,
        250_000,
    )

    roots = np.sqrt(
        1.0
        + x_dense_grid
        * x_dense_grid
    )

    c_dense_grid = (
        0.5
        * roots
        * (
            roots
            + 1.0
        )
    )

    objective_dense = (
        c_dense_grid
        / x_dense_grid
    )

    minimum_index = int(
        np.argmin(
            objective_dense
        )
    )

    x_dense = float(
        x_dense_grid[
            minimum_index
        ]
    )

    objective_dense_min = float(
        objective_dense[
            minimum_index
        ]
    )

    if (
        abs(
            x_dense
            - x_opt
        )
        > 5.0e-5
    ):

        raise RuntimeError(
            "Wall throughput optimum x "
            "failed dense cross-check."
        )

    if (
        abs(
            objective_dense_min
            - throughput_opt
        )
        > 2.0e-9
    ):

        raise RuntimeError(
            "Wall throughput objective "
            "failed dense cross-check."
        )

    wall_gain_vs_006d = (
        c006d
        / c_wall_opt
    )

    wall_ge10 = (
        wall_gain_vs_006d
        >= 10.0
    )

    delta_threshold = (
        math.sqrt(
            2.0
        )
        - 1.0
    )

    scan_rows: list[
        dict[
            str,
            Any,
        ]
    ] = []

    main_x_values = [
        0.25,
        0.5,
        0.75,
        1.0,
        x_opt,
        1.5,
        2.0,
        3.0,
        4.0,
    ]

    for x_value in (
        main_x_values
    ):

        coefficient = (
            wall_disk_c(
                x_value
            )
        )

        scan_rows.append({
            "section":
                "WALL_DISK_MAIN",

            "parameter":
                x_value,

            "parameter_name":
                "x_R_over_h",

            "C":
                coefficient,

            "gain_vs_006D":
                c006d
                / coefficient,

            "throughput_C_over_x":
                coefficient
                / x_value,

            "label":
                (
                    "PHYSICALLY_MOTIVATED_"
                    "GEOMETRY_SCAN"
                ),
        })

    for x_value in (
        WILDCARDS
    ):

        coefficient = (
            wall_disk_c(
                x_value
            )
        )

        scan_rows.append({
            "section":
                "WALL_DISK_WILDCARD",

            "parameter":
                x_value,

            "parameter_name":
                "x_R_over_h",

            "C":
                coefficient,

            "gain_vs_006D":
                c006d
                / coefficient,

            "throughput_C_over_x":
                coefficient
                / x_value,

            "label":
                (
                    "BLIND_WILDCARD_"
                    "NOT_PHYSICS_PRIOR"
                ),
        })

    main_delta_values = [
        0.45,
        0.5,
        0.75,
        1.0,
        1.5,
        2.0,
        3.0,
        4.0,
    ]

    rectifier_results: dict[
        str,
        dict[
            str,
            float,
        ],
    ] = {}

    for delta_value in (
        main_delta_values
    ):

        (
            eta_value,
            coefficient,
        ) = rectifier_c(
            delta_value
        )

        gain = (
            0.0
            if not math.isfinite(
                coefficient
            )
            else
            c006d
            / coefficient
        )

        rectifier_results[
            f"delta_{delta_value:g}"
        ] = {
            "eta":
                eta_value,

            "C":
                coefficient,

            "gain_vs_006D":
                gain,
        }

        scan_rows.append({
            "section":
                "RECTIFIER_MAIN",

            "parameter":
                delta_value,

            "parameter_name":
                (
                    "delta_reset_"
                    "depth_over_h"
                ),

            "C":
                coefficient,

            "gain_vs_006D":
                gain,

            "throughput_C_over_x":
                "",

            "label":
                (
                    "RELAXED_GLOBAL_"
                    "VIRIAL_CLOSED_"
                    "NO_TRANSPORT"
                ),
        })

    for delta_value in (
        WILDCARDS
    ):

        (
            eta_value,
            coefficient,
        ) = rectifier_c(
            delta_value
        )

        gain = (
            0.0
            if not math.isfinite(
                coefficient
            )
            else
            c006d
            / coefficient
        )

        scan_rows.append({
            "section":
                "RECTIFIER_WILDCARD",

            "parameter":
                delta_value,

            "parameter_name":
                (
                    "delta_reset_"
                    "depth_over_h"
                ),

            "C":
                coefficient,

            "gain_vs_006D":
                gain,

            "throughput_C_over_x":
                "",

            "label":
                (
                    "BLIND_WILDCARD_"
                    "NOT_PHYSICS_PRIOR"
                ),
        })

    (
        eta_delta_1,
        c_rect_delta_1,
    ) = rectifier_c(
        1.0
    )

    gain_rect_delta_1 = (
        c006d
        / c_rect_delta_1
    )

    # Absolute energy scale.

    coefficient_one_energy_1g_1m = (
        G0
        * C_LIGHT**2
        / G
    )

    e006d_1g_1m = (
        c006d
        * coefficient_one_energy_1g_1m
    )

    e_wall_opt_1g_1m = (
        c_wall_opt
        * coefficient_one_energy_1g_1m
    )

    # xi=1:
    #
    # tau = R/c = x h/c
    #
    # at h=1 m.

    tau_wall_opt_1m = (
        x_opt
        / C_LIGHT
    )

    delta_v_per_1g_pulse = (
        G0
        * tau_wall_opt_1m
    )

    # P_loss/a_avg
    # =
    # ell * throughput * c^3 h/G.
    #
    # Evaluate ell=1, h=1 m, a_avg=g.

    p_loss_1g_1m_ell1 = (
        throughput_opt
        * C_LIGHT**3
        / G
        * G0
    )

    power_caps = [
        1.0e3,
        1.0e6,
        1.0e9,
        1.0e12,
    ]

    ell_required_1m = {
        f"{power:.0e}_W":
            power
            / p_loss_1g_1m_ell1

        for power
        in power_caps
    }

    ell_required_1cm = {
        f"{power:.0e}_W":
            power
            /
            (
                0.01
                * p_loss_1g_1m_ell1
            )

        for power
        in power_caps
    }

    pulse_removes_inverse_g = (
        False
    )

    qwall_direct_repulsion = (
        qwall[
            "direct_standoff_repulsion"
        ]
        == "YES"
    )

    wall_pulse_prefilter = (
        "YELLOW_PROMOTE_ONE_"
        "FOCUSED_DYNAMIC_FIELD_GATE"
        if wall_ge10
        else
        "RED"
    )

    analogue_rerank = (
        "ACTIVATE_IN_TANDEM"
        if not pulse_removes_inverse_g
        else
        "DEFER"
    )

    with OUT_CSV.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "section",
                "parameter",
                "parameter_name",
                "C",
                "gain_vs_006D",
                "throughput_C_over_x",
                "label",
            ],
        )

        writer.writeheader()

        writer.writerows(
            scan_rows
        )

    summary: dict[
        str,
        Any,
    ] = {

        "claim_classification":
            (
                "PROJECT_DERIVED_024B_"
                "ANALYTIC_NUMERICAL_"
                "PULSE_PREFILTER_AND_"
                "RERANK_GATE"
            ),

        "006D": {
            **anchor,

            "B7_C_reference":
                CB7_REFERENCE,

            "B7_to_006D_headroom":
                headroom_b7_to_006d,
        },

        "stress_archetypes":
            archetypes,

        "dynamic_virial": {

            "identity":
                (
                    "I_ddot="
                    "2*integral_trace_Tij"
                ),

            "closed_cycle_integral_"
            "trace_stress":
                "ZERO",

            "two_phase_q_cycle_over_E":
                cycle_q_over_e,

            "two_phase_global_active_"
            "cycle_over_E":
                cycle_s_over_e,

            "scalar_active_identity":
                (
                    "S=2*phidot^2-2*V"
                ),
        },

        "qwall":
            qwall,

        "domain_wall_disk": {

            "x_opt_exact":
                x_opt,

            "x_opt_dense":
                x_dense,

            "C_opt":
                c_wall_opt,

            "throughput_C_over_x_opt":
                throughput_opt,

            "gain_vs_006D_at_C_opt":
                wall_gain_vs_006d,

            "source_level_ge10x_vs_006D":
                wall_ge10,

            "boundary_support_included":
                False,

            "classification":
                (
                    "TRANSIENT_COLLAPSE_"
                    "PREFILTER_ONLY"
                ),
        },

        "relaxed_spatiotemporal_rectifier": {

            "outward_threshold_delta":
                delta_threshold,

            "delta_1_eta":
                eta_delta_1,

            "delta_1_C":
                c_rect_delta_1,

            "delta_1_gain_vs_006D":
                gain_rect_delta_1,

            "global_virial_closed":
                True,

            "local_conservation_solved":
                False,

            "transport_T0i_included":
                False,

            "retarded_gravity_included":
                False,

            "field_solution":
                False,

            "main_scan":
                rectifier_results,
        },

        "absolute_scaling": {

            "coefficient_one_E_1g_1m_J":
                coefficient_one_energy_1g_1m,

            "006D_E_1g_1m_J":
                e006d_1g_1m,

            "wall_opt_E_1g_1m_J":
                e_wall_opt_1g_1m,

            "wall_opt_tau_1m_xi1_s":
                tau_wall_opt_1m,

            "wall_opt_delta_v_"
            "per_1g_pulse_m_per_s":
                delta_v_per_1g_pulse,

            "wall_opt_P_loss_"
            "1g_1m_ell1_W":
                p_loss_1g_1m_ell1,

            "ell_required_for_"
            "power_caps_1m":
                ell_required_1m,

            "ell_required_for_"
            "power_caps_1cm":
                ell_required_1cm,

            "inverse_G_scaling_removed":
                pulse_removes_inverse_g,
        },

        "decisions": {

            "QWALL_DIRECT_ROUTE":
                (
                    "GREEN"
                    if qwall_direct_repulsion
                    else
                    "RED"
                ),

            "TOPOLOGICAL_COLLAPSING_"
            "WALL_PULSE":
                wall_pulse_prefilter,

            "PULSE_FULL_CYCLE_"
            "FIELD_PROMOTION":
                "NO",

            "PULSE_REMOVES_1_OVER_G":
                "NO",

            "STATIC_006D":
                (
                    "KEEP_AS_STRONGEST_"
                    "CERTIFIED_TRUE_"
                    "STANDOFF_SOURCE"
                ),

            "STATIC_023C":
                (
                    "KEEP_AS_ACTUAL_"
                    "FIELD_PROOF_STACK_"
                    "FALLBACK"
                ),

            "ANALOGUE_ANTIGRAVITY_RERANK":
                analogue_rerank,

            "NEXT_PULSE":
                (
                    "024B1_CONSERVED_"
                    "AXISYMMETRIC_"
                    "STRING_BOUNDED_"
                    "DOMAIN_WALL_"
                    "COLLAPSE_WITH_"
                    "RETARDED_"
                    "LINEARIZED_GR"
                ),

            "NEXT_STATIC":
                (
                    "RERANK_ONLY_"
                    "GENUINELY_NEW_"
                    "006D_MICROSCOPIC_"
                    "REALIZATION_"
                    "ARCHITECTURES"
                ),
        },

        "claim_limits": [
            "NO_CONSERVED_PULSE_FIELD_SOLUTION",
            "NO_DYNAMIC_GR_CERTIFICATION",
            "NO_NONLINEAR_GR",
            "NO_PRACTICAL_ENERGY_SOURCE",
            "NO_EXPERIMENTAL_ANTIGRAVITY",
            "NO_DEVICE",
        ],
    }

    OUT_JSON.write_text(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "=== 024B SPATIOTEMPORAL "
        "VIRIAL / KERNEL "
        "RECTIFICATION RERANK ==="
    )

    print(
        "C_006D="
        f"{c006d:.15f}"
    )

    print(
        "C_B7="
        f"{CB7_REFERENCE:.15f}"
    )

    print(
        "B7_TO_006D_HEADROOM="
        f"{headroom_b7_to_006d:.12f}"
    )

    print(
        "STATIC_006D_ANCHOR=PASS"
    )

    print()

    print(
        "=== DYNAMIC CONSERVATION "
        "IDENTITY ==="
    )

    print(
        "VIRIAL_IDENTITY="
        "I_DDOT_EQUALS_"
        "2_INTEGRAL_TII"
    )

    print(
        "TWO_PHASE_CYCLE_Q_OVER_E="
        f"{cycle_q_over_e:.12e}"
    )

    print(
        "TWO_PHASE_CYCLE_GLOBAL_"
        "ACTIVE_OVER_E="
        f"{cycle_s_over_e:.12f}"
    )

    print(
        "CLOSED_CYCLE_REQUIRES_"
        "COMPENSATING_STRESS=YES"
    )

    print(
        "CANONICAL_SCALAR_ACTIVE_"
        "IDENTITY="
        "S_EQUALS_2_PHIDOT2_"
        "MINUS_2V"
    )

    print()

    print(
        "=== EXACT Q-WALL "
        "CONSTITUTIVE AUDIT ==="
    )

    print(
        "QWALL_E_NUMERIC="
        f"{qwall['energy_numeric']:.15f}"
    )

    print(
        "QWALL_ACTIVE_NUMERIC="
        f"{qwall['active_numeric']:.15f}"
    )

    print(
        "QWALL_ACTIVE_OVER_E="
        f"{qwall['active_over_energy']:.15f}"
    )

    print(
        "QWALL_GROSS_ACTIVE_POSITIVE="
        f"{qwall['gross_positive_active']:.15f}"
    )

    print(
        "QWALL_GROSS_ACTIVE_NEGATIVE="
        f"{qwall['gross_negative_active']:.15f}"
    )

    print(
        "QWALL_DEC_VIOLATION="
        f"{qwall['dec_violation']:.3e}"
    )

    print(
        "QWALL_LARGE_Q_ACTIVE_"
        "OVER_E_INFERENCE="
        f"{qwall['large_q_active_over_energy_inference']:.12f}"
    )

    print(
        "QWALL_DIRECT_STANDOFF_"
        "REPULSION=NO"
    )

    print(
        "QWALL_LONG_LIFETIME_DOES_"
        "NOT_FIX_ACTIVE_SIGN=YES"
    )

    print()

    print(
        "=== TOPOLOGICAL DOMAIN-WALL "
        "COLLAPSE PULSE PREFILTER ==="
    )

    print(
        "WALL_THROUGHPUT_X_OPT="
        f"{x_opt:.15f}"
    )

    print(
        "WALL_C_AT_X_OPT="
        f"{c_wall_opt:.15f}"
    )

    print(
        "WALL_C_OVER_X_OPT="
        f"{throughput_opt:.15f}"
    )

    print(
        "WALL_PEAK_GAIN_VS_006D="
        f"{wall_gain_vs_006d:.12f}"
    )

    print(
        "WALL_SOURCE_LEVEL_GE10X_"
        "VS_006D="
        + (
            "YES"
            if wall_ge10
            else
            "NO"
        )
    )

    print(
        "WALL_FINITE_BOUNDARY_"
        "SUPPORT_INCLUDED=NO"
    )

    print(
        "WALL_CLASSIFICATION="
        "TRANSIENT_COLLAPSE_"
        "PREFILTER_ONLY"
    )

    print()

    print(
        "=== RELAXED SPATIOTEMPORAL "
        "RECTIFIER ==="
    )

    print(
        "RECTIFIER_OUTWARD_"
        "THRESHOLD_DELTA="
        f"{delta_threshold:.15f}"
    )

    print(
        "RECTIFIER_DELTA1_C="
        f"{c_rect_delta_1:.15f}"
    )

    print(
        "RECTIFIER_DELTA1_GAIN_"
        "VS_006D="
        f"{gain_rect_delta_1:.12f}"
    )

    print(
        "RECTIFIER_GLOBAL_"
        "VIRIAL_CLOSED=YES"
    )

    print(
        "RECTIFIER_LOCAL_"
        "CONSERVATION_SOLVED=NO"
    )

    print(
        "RECTIFIER_TRANSPORT_"
        "T0I_INCLUDED=NO"
    )

    print(
        "RECTIFIER_RETARDED_"
        "GRAVITY_INCLUDED=NO"
    )

    print(
        "RECTIFIER_FIELD_SOLUTION=NO"
    )

    print()

    print(
        "=== ABSOLUTE ENERGY / "
        "LOSS LEDGER ==="
    )

    print(
        "COEFFICIENT_ONE_E_1G_1M_J="
        f"{coefficient_one_energy_1g_1m:.12e}"
    )

    print(
        "E_006D_1G_1M_J="
        f"{e006d_1g_1m:.12e}"
    )

    print(
        "E_WALL_OPT_1G_1M_J="
        f"{e_wall_opt_1g_1m:.12e}"
    )

    print(
        "WALL_OPT_TAU_1M_XI1_S="
        f"{tau_wall_opt_1m:.12e}"
    )

    print(
        "WALL_OPT_DELTA_V_PER_"
        "1G_PULSE="
        f"{delta_v_per_1g_pulse:.12e}"
    )

    print(
        "WALL_OPT_P_LOSS_1G_"
        "1M_ELL1_W="
        f"{p_loss_1g_1m_ell1:.12e}"
    )

    print(
        "ELL_REQUIRED_1MW_1G_1M="
        f"{ell_required_1m['1e+06_W']:.12e}"
    )

    print(
        "ELL_REQUIRED_1GW_1G_1M="
        f"{ell_required_1m['1e+09_W']:.12e}"
    )

    print(
        "ELL_REQUIRED_1MW_1G_1CM="
        f"{ell_required_1cm['1e+06_W']:.12e}"
    )

    print(
        "PULSE_REMOVES_1_OVER_G_"
        "SCALING=NO"
    )

    print()

    print(
        "=== 024B DECISION ==="
    )

    print(
        "QWALL_DIRECT_ROUTE=RED"
    )

    print(
        "TOPOLOGICAL_COLLAPSING_"
        "WALL_PULSE="
        f"{wall_pulse_prefilter}"
    )

    print(
        "PULSE_FULL_CYCLE_"
        "CONSERVED_FIELD_SOLUTION=NO"
    )

    print(
        "STATIC_006D="
        "KEEP_AS_STRONGEST_CERTIFIED_"
        "TRUE_STANDOFF_SOURCE"
    )

    print(
        "STATIC_023C="
        "KEEP_AS_ACTUAL_FIELD_"
        "PROOF_STACK_FALLBACK"
    )

    print(
        "ANALOGUE_ANTIGRAVITY_RERANK="
        f"{analogue_rerank}"
    )

    print(
        "NEXT_PULSE="
        "024B1_CONSERVED_"
        "AXISYMMETRIC_"
        "STRING_BOUNDED_"
        "DOMAIN_WALL_COLLAPSE_"
        "WITH_RETARDED_"
        "LINEARIZED_GR"
    )

    print(
        "NEXT_STATIC="
        "RERANK_ONLY_GENUINELY_"
        "NEW_006D_MICROSCOPIC_"
        "REALIZATION_ARCHITECTURES"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )

    print(
        "SUMMARY_JSON="
        f"{OUT_JSON.relative_to(ROOT)}"
    )

    print(
        "SCAN_CSV="
        f"{OUT_CSV.relative_to(ROOT)}"
    )

    print(
        "024B_RUN_COMPLETE=YES"
    )


if __name__ == "__main__":
    main()
