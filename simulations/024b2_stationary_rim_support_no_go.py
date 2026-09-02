#!/usr/bin/env python3
"""024B2 — stationary local-rim support no-go and pulse rerank.

PURPOSE
-------
Close the missing-support loophole left by 024B1 before any expensive
microscopic dynamic-field simulation.

024B1 found:

- unsupported outer-edge collapse is dynamically wrong-sign;
- center-out hole expansion has a large positive impulse if the outer rim is
  artificially held fixed;
- a freely moving outer rim again makes the response wrong-sign.

The remaining question is therefore:

    Can a physical local stationary rim hold the outer wall boundary while
    retaining the very low active-source cost assumed by the held-rim model?

This run shows that local stress balance plus the dominant energy condition
already impose a much stronger lower bound.

SCIENTIFIC QUESTION
-------------------
Can a stationary circular local line source supporting a positive-tension
domain wall preserve the >=10x source-efficiency region found by 024B1?

CHEAPEST DECISIVE TEST
----------------------
Use local radial force balance and DEC before introducing another microscopic
vorton PDE.

For a circular wall boundary of radius R and wall tension sigma,

    P_line = sigma R

is required for stationary radial support.

This is the same balance condition used by the project's promoted 018B-0H
source-level stationary-loop code.

For a type-I/elastic line satisfying DEC,

    E_line >= |P_line|.

Since the required support pressure is positive,

    E_line >= P_line = sigma R.

The minimum-energy DEC-saturating support therefore has

    E_line,min = sigma R.

Its gravitoelectric active line source is

    Lambda_active
        =
    E_line + P_line,

so

    Lambda_active,min
        =
    2 sigma R.

Thus the complete physical support cannot simultaneously be:

    stationary,
    local,
    wall-supporting,
    DEC-compatible,

and have the near-zero active source provisionally assigned to the held rim in
024B1.

024B1 HELD-RIM PARAMETERIZATION
-------------------------------
024B1 used

    x = R/h,

    q = mu/(sigma R),

    r0 = kappa mu/sigma
       = kappa q R.

With h=sigma=1,

    mu = q x.

The provisional static outer Nambu rim had line energy

    E_line,old = mu = q x

and zero static active source.

But a stationary wall-supporting rim requires

    P_line = x.

Keeping the old rim energy would therefore require

    P_line/E_line,old
        =
    1/q.

Every 024B1 held-rim scan point has q<1.

Consequently the unchanged-energy support would violate DEC.

The minimum DEC repair replaces the outer rim energy by

    E_line,new = x

and gives active line source

    Lambda_active,new = 2x.

This run applies that repair independently to every 024B1 held-rim scan point.

INITIAL HELD-HOLE LEDGER
------------------------
Let

    y = r0/h = kappa q x.

The static wall-annulus energy is

    E_wall
        =
    pi (x^2-y^2).

The inner nucleating string initially has energy

    E_inner
        =
    2 pi (q x) y.

The provisional 024B1 outer rim energy was

    E_outer,old
        =
    2 pi q x^2.

The minimum DEC stationary support has instead

    E_outer,DEC
        =
    2 pi x^2.

The initial thin-wall outward kernel moment is

    A_wall
        =
    2 pi
    [
        1/sqrt(1+y^2)
        -
        1/sqrt(1+x^2)
    ].

The compulsory stationary outer-support attraction is

    A_support
        =
    4 pi x^2
    /
    (1+x^2)^(3/2).

Therefore

    A_corrected
        =
    A_wall - A_support.

The corrected coefficient is

    C_corrected
        =
    E_corrected/A_corrected

when A_corrected>0.

RESET-STAGE CORRECTION
----------------------
024B1 stored the original stage duration tau and normalized integrated impulse

    eta_old = J_old/E_old.

Hence

    J_old = eta_old E_old.

A stationary support is present throughout the center-out hole-expansion stage.

Its time-independent kernel contribution is

    J_support
        =
    A_support tau.

Therefore the best-case corrected stage impulse is

    J_corrected
        =
    J_old - J_support.

This still omits formation, release, reformation, radiation and control.

SUPPORTED FULL-DISK LIMIT
-------------------------
For y=0 and the minimum DEC stationary rim:

    E_total
        =
    3 pi x^2.

The outward kernel moment is

    A
        =
    2 pi
    [
        1 - 1/sqrt(1+x^2)
    ]
    -
    4 pi x^2/(1+x^2)^(3/2).

Thus

    C_disk,DEC(x)
        =
    E_total/A.

The run independently minimizes this expression and compares it with the
project's existing

    uniform_disk_ring_mass_coefficient(x).

The expected optimum is the historical 005B result:

    R/h approximately 4.00614967

    C approximately 79.753148116012.

This is an important cross-era consistency check:

    physicalizing the 024B1 held rim by local stationary DEC support
    reconstructs the old supported-wall problem.

ANNULAR HOLE CHECK
------------------
The run additionally scans a wider optimistic annular family.

For this particular check the inner-hole string energy is deliberately set to
zero, which makes the test more favorable than any real string-bounded hole.

If even this optimistic annular-hole family does not beat the intact supported
disk, adding the inner string cannot rescue it.

RELATION TO 006B / 006D
-----------------------
This is NOT a universal no-go against efficient conserved support.

006B and 006D already demonstrated that a distributed radial stress-transfer
architecture can improve dramatically over a single local support rim:

    C_005B approximately 79.753

    C_006B approximately 23.427

    C_006D approximately 23.592.

The lesson tested here is narrower:

    SINGLE_LOCAL_STATIONARY_RIM
    IS NOT
    THE LOW-ACTIVE SUPPORT REQUIRED BY 024B1.

A pulse successor must instead exploit genuinely nonlocal or outward-moving
support/reset stress if it is to outperform the static distributed-support
architecture.

INPUTS
------
results/data/
    024b1_directional_wall_reset_support_summary.json

results/data/
    024b1_directional_wall_reset_support_scan.csv

Project source:
    antigravity_research.geometry.axisymmetric_thin_stress

OUTPUTS
-------
results/data/
    024b2_stationary_rim_support_no_go_summary.json

results/data/
    024b2_stationary_rim_support_corrected_scan.csv

ASSUMPTIONS
-----------
- thin wall / thin line;
- flat-background linearized-GR kernel;
- local circular stationary outer support;
- positive wall tension;
- DEC applied to the outer supporting line;
- axisymmetric payload point kernel with h=1;
- 024B1 center-out inner-string dynamics inherited only through its stored
  integrated impulse and duration;
- no claim that every possible nonlocal support obeys the local-rim bound.

FALSIFIER
---------
The local stationary-rim no-go is falsified if either:

1. the project 018B stationary balance does not require P_line approximately
   sigma R; or

2. a DEC-compatible local stationary support has E_line < |P_line|; or

3. after applying the minimum DEC support to the 024B1 scan, a robust compact
   >=10x outward pulse candidate survives.

PROMOTION CONDITION
-------------------
Do not promote a local stationary-rim pulse architecture unless a physical
support beats this bound without violating local conservation or DEC.

If the bound closes the class, rerank the pulse branch toward:

    outward-propagating support stress,
    co-expanding support,
    or remote/distributed stress transfer,

with formation and reset included from the outset.

STOP RULE
---------
Do not rerun the old KLS/vorton PDE merely to search for a lower active rim
after this gate if the required stationary local support is already excluded
by conservation plus DEC.

The old 018B field-existence result remains valid.

The old 018C instability result remains valid for that specific microscopic
implementation.

This run does not establish a generic vorton instability or generic vorton
no-go.

LITERATURE CONTEXT
------------------
Modern field simulations show that stable vortons can exist in suitable
superconducting-string regimes.

The point of this gate is therefore not:

    VORTONS_CANNOT_EXIST.

It is:

    A_LOCAL_STATIONARY_WALL_SUPPORTING_RIM_HAS_AN_UNAVOIDABLE
    ENERGY_AND_ACTIVE_STRESS_LEDGER.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_ANALYTIC_NUMERICAL_LOCAL_SUPPORT_BOUND_AND_PULSE_RERANK

DOES NOT ESTABLISH
------------------
- a universal theorem against nonlocal support;
- a microscopic new pulse field;
- a complete formation/reset cycle;
- nonlinear GR;
- practical scaling;
- experimental antigravity;
- a practical device.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.optimize import minimize_scalar

from antigravity_research.geometry.axisymmetric_thin_stress import (
    uniform_disk_ring_mass_coefficient,
)


ROOT = Path(__file__).resolve().parents[1]

INPUT_SUMMARY = (
    ROOT
    / "results/data/"
    "024b1_directional_wall_reset_support_summary.json"
)

INPUT_SCAN = (
    ROOT
    / "results/data/"
    "024b1_directional_wall_reset_support_scan.csv"
)

OUT_SUMMARY = (
    ROOT
    / "results/data/"
    "024b2_stationary_rim_support_no_go_summary.json"
)

OUT_SCAN = (
    ROOT
    / "results/data/"
    "024b2_stationary_rim_support_corrected_scan.csv"
)


C006D = 23.591586299249
C006B = 23.426710175391
C005B = 79.753148116012

X005B = 4.006149670781


def finite(value: str | float | int) -> float:
    """Convert one CSV scalar to finite float."""

    out = float(value)

    if not math.isfinite(out):
        raise RuntimeError(
            f"Nonfinite required input: {value!r}"
        )

    return out


def supported_disk_dec_coefficient(
    x: float,
) -> float:
    """Independent minimum-DEC stationary supported disk coefficient."""

    if x <= 0.0:
        return math.inf

    energy = (
        3.0
        * math.pi
        * x
        * x
    )

    wall_outward = (
        2.0
        * math.pi
        * (
            1.0
            - 1.0
            / math.sqrt(
                1.0
                + x
                * x
            )
        )
    )

    support_inward = (
        4.0
        * math.pi
        * x
        * x
        / (
            1.0
            + x
            * x
        ) ** 1.5
    )

    net = (
        wall_outward
        - support_inward
    )

    if net <= 0.0:
        return math.inf

    return (
        energy
        / net
    )


def optimistic_supported_annulus(
    x: float,
    y: float,
) -> tuple[
    float,
    float,
    float,
]:
    """Stationary DEC outer rim plus zero-energy inner-hole boundary.

    This intentionally gives the hole an unphysical advantage by omitting
    its string energy entirely.
    """

    if (
        x <= 0.0
        or y < 0.0
        or y >= x
    ):
        return (
            math.inf,
            -math.inf,
            math.inf,
        )

    wall_energy = (
        math.pi
        * (
            x * x
            - y * y
        )
    )

    outer_support_energy = (
        2.0
        * math.pi
        * x
        * x
    )

    energy = (
        wall_energy
        + outer_support_energy
    )

    wall_outward = (
        2.0
        * math.pi
        * (
            1.0
            / math.sqrt(
                1.0
                + y * y
            )
            - 1.0
            / math.sqrt(
                1.0
                + x * x
            )
        )
    )

    support_inward = (
        4.0
        * math.pi
        * x
        * x
        / (
            1.0
            + x
            * x
        ) ** 1.5
    )

    net = (
        wall_outward
        - support_inward
    )

    coefficient = (
        energy
        / net
        if net > 0.0
        else math.inf
    )

    return (
        coefficient,
        net,
        energy,
    )


def reconstruct_held_row(
    row: dict[str, str],
) -> dict[str, Any]:
    """Apply minimum physical stationary DEC support to one 024B1 row."""

    x = finite(
        row["x0"]
    )

    q = finite(
        row["ratio"]
    )

    kappa = finite(
        row["kappa"]
    )

    c_old = finite(
        row["C_initial"]
    )

    eta_old = finite(
        row["eta_J"]
    )

    tau = finite(
        row["tau"]
    )

    if (
        x <= 0.0
        or q <= 0.0
        or kappa <= 1.0
    ):
        raise RuntimeError(
            "Invalid held-hole row geometry."
        )

    y = (
        kappa
        * q
        * x
    )

    if y >= x:
        raise RuntimeError(
            "024B1 held-hole row has r0 >= R."
        )

    mu = (
        q
        * x
    )

    wall_energy = (
        math.pi
        * (
            x * x
            - y * y
        )
    )

    inner_string_energy = (
        2.0
        * math.pi
        * mu
        * y
    )

    outer_old_energy = (
        2.0
        * math.pi
        * mu
        * x
    )

    old_energy = (
        wall_energy
        + inner_string_energy
        + outer_old_energy
    )

    wall_outward = (
        2.0
        * math.pi
        * (
            1.0
            / math.sqrt(
                1.0
                + y * y
            )
            - 1.0
            / math.sqrt(
                1.0
                + x * x
            )
        )
    )

    old_c_reconstructed = (
        old_energy
        / wall_outward
    )

    c_relerr = (
        abs(
            old_c_reconstructed
            - c_old
        )
        / c_old
    )

    if c_relerr > 2.0e-10:
        raise RuntimeError(
            "024B1 held-row energy/force reconstruction "
            f"failed: relerr={c_relerr}"
        )

    # Actual wall support requires:
    #
    # P_line = sigma R = x
    #
    # while old provisional line energy was:
    #
    # E_line_old = mu = q x.
    #
    # Same-energy support therefore requires P/E=1/q.

    required_p_over_old_e = (
        1.0
        / q
    )

    same_energy_dec_pass = (
        required_p_over_old_e
        <= 1.0
        + 1.0e-14
    )

    # Minimum DEC repair:
    #
    # E_line_new = P_line = x.
    #
    # Around circumference 2 pi x:
    #
    # E_outer_new = 2 pi x^2.
    #
    # active line = E+P = 2x,
    #
    # Q_active,total = 4 pi x^2.

    outer_dec_energy = (
        2.0
        * math.pi
        * x
        * x
    )

    outer_energy_multiplier = (
        outer_dec_energy
        / outer_old_energy
    )

    support_active_total = (
        4.0
        * math.pi
        * x
        * x
    )

    outer_kernel = (
        1.0
        / (
            1.0
            + x
            * x
        ) ** 1.5
    )

    support_inward = (
        support_active_total
        * outer_kernel
    )

    corrected_initial_outward = (
        wall_outward
        - support_inward
    )

    corrected_energy = (
        wall_energy
        + inner_string_energy
        + outer_dec_energy
    )

    corrected_c = (
        corrected_energy
        / corrected_initial_outward
        if corrected_initial_outward > 0.0
        else math.inf
    )

    old_impulse = (
        eta_old
        * old_energy
    )

    support_impulse = (
        support_inward
        * tau
    )

    corrected_impulse = (
        old_impulse
        - support_impulse
    )

    corrected_eta = (
        corrected_impulse
        / corrected_energy
    )

    return {
        "x0":
            x,

        "q":
            q,

        "kappa":
            kappa,

        "r0_over_h":
            y,

        "old_C":
            c_old,

        "old_eta":
            eta_old,

        "old_tau":
            tau,

        "required_P_over_old_E_line":
            required_p_over_old_e,

        "same_energy_DEC_pass":
            same_energy_dec_pass,

        "outer_energy_multiplier_to_DEC_support":
            outer_energy_multiplier,

        "minimum_DEC_support_active_over_new_E":
            2.0,

        "minimum_support_active_over_old_outer_E":
            2.0
            / q,

        "wall_outward":
            wall_outward,

        "minimum_support_inward":
            support_inward,

        "corrected_initial_outward":
            corrected_initial_outward,

        "corrected_initial_outward_yes":
            corrected_initial_outward
            > 0.0,

        "corrected_energy":
            corrected_energy,

        "corrected_C":
            corrected_c,

        "corrected_beats_006D":
            corrected_c
            < C006D,

        "corrected_ge10x_vs_006D":
            corrected_c
            <= C006D
            / 10.0,

        "old_stage_impulse":
            old_impulse,

        "minimum_support_stage_impulse":
            support_impulse,

        "corrected_stage_impulse":
            corrected_impulse,

        "corrected_eta":
            corrected_eta,

        "corrected_positive_stage_impulse":
            corrected_eta
            > 0.0,
    }


def main() -> None:
    """Execute 024B2."""

    if not INPUT_SUMMARY.is_file():
        raise RuntimeError(
            f"Missing {INPUT_SUMMARY}"
        )

    if not INPUT_SCAN.is_file():
        raise RuntimeError(
            f"Missing {INPUT_SCAN}"
        )

    source_summary = json.loads(
        INPUT_SUMMARY.read_text(
            encoding="utf-8"
        )
    )

    if (
        source_summary[
            "decisions"
        ][
            "PULSE_BRANCH"
        ]
        !=
        "YELLOW_HELD_RIM_TARGET_ONLY"
    ):
        raise RuntimeError(
            "Unexpected 024B1 pulse-branch input."
        )

    if (
        source_summary[
            "decisions"
        ][
            "PULSE_EFFECTIVE_FIELD_PROMOTION"
        ]
        != "NO"
    ):
        raise RuntimeError(
            "024B1 promotion state changed."
        )

    c006d_input = float(
        source_summary[
            "006D"
        ][
            "c"
        ]
    )

    if (
        abs(
            c006d_input
            - C006D
        )
        > 5.0e-13
    ):
        raise RuntimeError(
            "006D input regression."
        )

    # ------------------------------------------------------------
    # 1. Independent supported-disk reconstruction.
    # ------------------------------------------------------------

    independent = minimize_scalar(
        supported_disk_dec_coefficient,
        bounds=(
            2.0,
            8.0,
        ),
        method="bounded",
        options={
            "xatol":
                1.0e-13,
        },
    )

    if not independent.success:
        raise RuntimeError(
            "Independent supported-disk optimization failed."
        )

    x_independent = float(
        independent.x
    )

    c_independent = float(
        independent.fun
    )

    library = minimize_scalar(
        uniform_disk_ring_mass_coefficient,
        bounds=(
            2.0,
            8.0,
        ),
        method="bounded",
        options={
            "xatol":
                1.0e-13,
        },
    )

    if not library.success:
        raise RuntimeError(
            "Project 005B reconstruction failed."
        )

    x_library = float(
        library.x
    )

    c_library = float(
        library.fun
    )

    if (
        abs(
            c_library
            - C005B
        )
        / C005B
        > 2.0e-12
    ):
        raise RuntimeError(
            "005B coefficient regression."
        )

    if (
        abs(
            c_independent
            - c_library
        )
        / c_library
        > 2.0e-11
    ):
        raise RuntimeError(
            "New support theorem does not reconstruct "
            "the project 005B baseline."
        )

    # ------------------------------------------------------------
    # 2. Apply stationary DEC support to every held 024B1 case.
    # ------------------------------------------------------------

    held_rows: list[
        dict[
            str,
            Any,
        ]
    ] = []

    with INPUT_SCAN.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as handle:

        reader = csv.DictReader(
            handle
        )

        for row in reader:

            if (
                row[
                    "branch"
                ]
                !=
                "HELD_RIM_CENTER_OUT_HOLE"
            ):
                continue

            held_rows.append(
                reconstruct_held_row(
                    row
                )
            )

    if len(
        held_rows
    ) != 8405:
        raise RuntimeError(
            "Expected 8405 held-rim rows, got "
            f"{len(held_rows)}"
        )

    same_energy_dec_pass = sum(
        bool(
            row[
                "same_energy_DEC_pass"
            ]
        )
        for row
        in held_rows
    )

    corrected_outward = sum(
        bool(
            row[
                "corrected_initial_outward_yes"
            ]
        )
        for row
        in held_rows
    )

    corrected_beats_006d = sum(
        bool(
            row[
                "corrected_beats_006D"
            ]
        )
        for row
        in held_rows
    )

    corrected_ge10 = sum(
        bool(
            row[
                "corrected_ge10x_vs_006D"
            ]
        )
        for row
        in held_rows
    )

    corrected_positive_impulse = sum(
        bool(
            row[
                "corrected_positive_stage_impulse"
            ]
        )
        for row
        in held_rows
    )

    max_corrected_eta = max(
        float(
            row[
                "corrected_eta"
            ]
        )
        for row
        in held_rows
    )

    min_required_p_over_old_e = min(
        float(
            row[
                "required_P_over_old_E_line"
            ]
        )
        for row
        in held_rows
    )

    max_required_p_over_old_e = max(
        float(
            row[
                "required_P_over_old_E_line"
            ]
        )
        for row
        in held_rows
    )

    # Fixed reference from 024B1.
    #
    # IMPORTANT:
    # The fixed reference was evaluated independently of the dense scan.
    # Its x=2/3, q=0.18, kappa=1.02 coordinates therefore need not appear
    # as an exact row in the CSV grid. Reconstruct it from the authoritative
    # fixed_reference object stored in the 024B1 summary instead.

    reference_source = (
        source_summary[
            "held_rim_center_out_hole"
        ][
            "fixed_reference"
        ]
    )

    reference = reconstruct_held_row({
        "x0":
            str(
                reference_source[
                    "x0"
                ]
            ),

        "ratio":
            str(
                reference_source[
                    "q"
                ]
            ),

        "kappa":
            str(
                reference_source[
                    "kappa"
                ]
            ),

        "C_initial":
            str(
                reference_source[
                    "c_initial_chi0"
                ]
            ),

        "eta_J":
            str(
                reference_source[
                    "eta_total_chi0"
                ]
            ),

        "tau":
            str(
                reference_source[
                    "tau_reset"
                ]
            ),
    })

    if (
        abs(
            float(
                reference[
                    "x0"
                ]
            )
            - 2.0 / 3.0
        )
        > 1.0e-12
        or
        abs(
            float(
                reference[
                    "q"
                ]
            )
            - 0.18
        )
        > 1.0e-12
        or
        abs(
            float(
                reference[
                    "kappa"
                ]
            )
            - 1.02
        )
        > 1.0e-12
    ):
        raise RuntimeError(
            "024B1 fixed-reference provenance check failed."
        )

    # ------------------------------------------------------------
    # 3. Optimistic annular-hole extension.
    #
    # Inner-hole string energy is omitted deliberately.
    # ------------------------------------------------------------

    x_grid = np.linspace(
        0.25,
        8.0,
        1201,
    )

    fraction_grid = np.linspace(
        0.0,
        0.95,
        381,
    )

    best_annular = (
        math.inf,
        math.nan,
        math.nan,
        math.nan,
    )

    best_nonzero_hole = (
        math.inf,
        math.nan,
        math.nan,
        math.nan,
    )

    outward_annular_cases = 0

    for x in x_grid:

        for fraction in fraction_grid:

            y = (
                fraction
                * x
            )

            (
                coefficient,
                net,
                _energy,
            ) = (
                optimistic_supported_annulus(
                    float(
                        x
                    ),
                    float(
                        y
                    ),
                )
            )

            if net <= 0.0:
                continue

            outward_annular_cases += 1

            candidate = (
                coefficient,
                float(
                    x
                ),
                float(
                    y
                ),
                float(
                    fraction
                ),
            )

            if (
                candidate[
                    0
                ]
                <
                best_annular[
                    0
                ]
            ):
                best_annular = (
                    candidate
                )

            if (
                fraction
                >= 0.01
                and
                candidate[
                    0
                ]
                <
                best_nonzero_hole[
                    0
                ]
            ):
                best_nonzero_hole = (
                    candidate
                )

    if not math.isfinite(
        best_annular[
            0
        ]
    ):
        raise RuntimeError(
            "Optimistic annular scan found no outward cases."
        )

    # Grid only needs to confirm that the best annular point approaches
    # the independently optimized intact disk and not a dramatically
    # lower hole solution.

    if (
        best_annular[
            0
        ]
        <
        C005B
        * (
            1.0
            - 2.0e-4
        )
    ):
        raise RuntimeError(
            "Unexpected annular-hole improvement below 005B."
        )

    # ------------------------------------------------------------
    # Output corrected scan.
    # ------------------------------------------------------------

    fieldnames = [
        "x0",
        "q",
        "kappa",
        "r0_over_h",
        "old_C",
        "old_eta",
        "old_tau",
        "required_P_over_old_E_line",
        "same_energy_DEC_pass",
        "outer_energy_multiplier_to_DEC_support",
        "minimum_DEC_support_active_over_new_E",
        "minimum_support_active_over_old_outer_E",
        "wall_outward",
        "minimum_support_inward",
        "corrected_initial_outward",
        "corrected_initial_outward_yes",
        "corrected_energy",
        "corrected_C",
        "corrected_beats_006D",
        "corrected_ge10x_vs_006D",
        "old_stage_impulse",
        "minimum_support_stage_impulse",
        "corrected_stage_impulse",
        "corrected_eta",
        "corrected_positive_stage_impulse",
    ]

    with OUT_SCAN.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        for row in held_rows:
            writer.writerow(
                row
            )

    local_stationary_support_closed = (
        same_energy_dec_pass
        == 0
        and
        corrected_outward
        == 0
        and
        corrected_positive_impulse
        == 0
    )

    if local_stationary_support_closed:

        pulse_decision = (
            "RED_LOCAL_STATIONARY_RIM_SUPPORT"
        )

        next_pulse = (
            "024B3_OUTWARD_PROPAGATING_OR_REMOTE_"
            "SUPPORT_STRESS_FULL_CYCLE_PREFILTER"
        )

    else:

        pulse_decision = (
            "YELLOW_REQUIRES_CASE_REVIEW"
        )

        next_pulse = (
            "024B2R_REVIEW_SURVIVING_STATIONARY_SUPPORT_CASES"
        )

    summary = {
        "claim_classification":
            (
                "PROJECT_DERIVED_ANALYTIC_NUMERICAL_"
                "LOCAL_SUPPORT_BOUND_AND_PULSE_RERANK"
            ),

        "006D": {
            "C":
                C006D,
        },

        "006B": {
            "C":
                C006B,
        },

        "stationary_support_theorem": {
            "balance":
                "P_line=sigma*R",

            "DEC":
                "E_line>=abs(P_line)",

            "minimum_E_line":
                "sigma*R",

            "minimum_active_line":
                "2*sigma*R",

            "same_energy_024B1_requires":
                "P_over_E=1/q",
        },

        "005B_independent_reconstruction": {
            "x_R_over_h":
                x_independent,

            "C":
                c_independent,

            "library_x_R_over_h":
                x_library,

            "library_C":
                c_library,

            "reference_C":
                C005B,

            "C_over_006D":
                c_independent
                / C006D,

            "better_than_006D":
                c_independent
                < C006D,
        },

        "024B1_held_scan_physicalization": {
            "total_cases":
                len(
                    held_rows
                ),

            "same_energy_DEC_pass_cases":
                same_energy_dec_pass,

            "corrected_initial_outward_cases":
                corrected_outward,

            "corrected_beats_006D_cases":
                corrected_beats_006d,

            "corrected_ge10x_vs_006D_cases":
                corrected_ge10,

            "corrected_positive_stage_impulse_cases":
                corrected_positive_impulse,

            "max_corrected_eta":
                max_corrected_eta,

            "minimum_required_P_over_old_E":
                min_required_p_over_old_e,

            "maximum_required_P_over_old_E":
                max_required_p_over_old_e,
        },

        "fixed_reference": {
            **reference,
        },

        "optimistic_annular_hole_scan": {
            "inner_hole_string_energy_included":
                False,

            "outward_grid_cases":
                outward_annular_cases,

            "best_C":
                best_annular[
                    0
                ],

            "best_x":
                best_annular[
                    1
                ],

            "best_y":
                best_annular[
                    2
                ],

            "best_y_over_x":
                best_annular[
                    3
                ],

            "best_nonzero_hole_C":
                best_nonzero_hole[
                    0
                ],

            "best_nonzero_hole_x":
                best_nonzero_hole[
                    1
                ],

            "best_nonzero_hole_y":
                best_nonzero_hole[
                    2
                ],

            "best_nonzero_hole_y_over_x":
                best_nonzero_hole[
                    3
                ],

            "hole_beats_005B":
                best_annular[
                    0
                ]
                <
                C005B
                * (
                    1.0
                    - 2.0e-4
                ),
        },

        "decisions": {
            "024B1_HELD_RIM_WITHOUT_SUPPORT":
                "RETAIN_AS_RELAXED_TARGET_ONLY",

            "SAME_ENERGY_LOCAL_STATIONARY_SUPPORT":
                "RED_DEC",

            "MINIMUM_DEC_LOCAL_STATIONARY_SUPPORT":
                (
                    "RED_IN_024B1_COMPACT_SCAN"
                    if local_stationary_support_closed
                    else
                    "REVIEW"
                ),

            "LOCAL_STATIONARY_VORTON_RIM_AS_LOW_ACTIVE_SUPPORT":
                (
                    "RED_FOR_THIS_PULSE_ROLE"
                    if local_stationary_support_closed
                    else
                    "REVIEW"
                ),

            "GENERIC_VORTON_EXISTENCE":
                "NOT_FALSIFIED",

            "GENERIC_VORTON_STABILITY":
                "NOT_FALSIFIED_BY_THIS_GATE",

            "PULSE_BRANCH":
                pulse_decision,

            "NEXT_PULSE":
                next_pulse,

            "NEXT_STATIC":
                (
                    "KEEP_006D_DISTRIBUTED_STRESS_TRANSFER_"
                    "AS_STATIC_DESIGN_ANCHOR_AND_CONTINUE_"
                    "GENUINELY_NEW_MICROSCOPIC_RERANK"
                ),

            "ANALOGUE_ANTIGRAVITY":
                "ACTIVE_IN_TANDEM",

            "PRACTICAL_ANTIGRAVITY_DEVICE":
                "NO",
        },

        "claim_limits": [
            "NO_GENERIC_VORTON_NO_GO",
            "NO_NONLOCAL_SUPPORT_NO_GO",
            "NO_NEW_MICROSCOPIC_PULSE_FIELD",
            "NO_COMPLETE_FORMATION_RESET_CYCLE",
            "NO_NONLINEAR_GR",
            "NO_PRACTICAL_DEVICE",
        ],
    }

    OUT_SUMMARY.write_text(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "=== 024B2 STATIONARY LOCAL-RIM "
        "SUPPORT NO-GO ==="
    )

    print(
        "C_006D="
        f"{C006D:.15f}"
    )

    print(
        "C_006B="
        f"{C006B:.15f}"
    )

    print()

    print(
        "=== LOCAL SUPPORT IDENTITY ==="
    )

    print(
        "STATIONARY_RING_BALANCE="
        "P_LINE_EQUALS_SIGMA_R"
    )

    print(
        "DEC_REQUIRES="
        "E_LINE_GE_ABS_P_LINE"
    )

    print(
        "MINIMUM_DEC_SUPPORT="
        "E_LINE_EQUALS_P_LINE_EQUALS_SIGMA_R"
    )

    print(
        "MINIMUM_DEC_ACTIVE_LINE="
        "2_SIGMA_R"
    )

    print()

    print(
        "=== 005B CROSS-ERA RECONSTRUCTION ==="
    )

    print(
        "SUPPORTED_DISK_X_OPT_INDEPENDENT="
        f"{x_independent:.15f}"
    )

    print(
        "SUPPORTED_DISK_C_INDEPENDENT="
        f"{c_independent:.15f}"
    )

    print(
        "SUPPORTED_DISK_X_OPT_PROJECT_LIBRARY="
        f"{x_library:.15f}"
    )

    print(
        "SUPPORTED_DISK_C_PROJECT_LIBRARY="
        f"{c_library:.15f}"
    )

    print(
        "SUPPORTED_DISK_MATCHES_005B="
        + (
            "YES"
            if abs(
                c_independent
                - C005B
            )
            / C005B
            < 2.0e-11
            else
            "NO"
        )
    )

    print(
        "SUPPORTED_DISK_C_OVER_006D="
        f"{c_independent / C006D:.12f}"
    )

    print(
        "LOCAL_STATIONARY_SUPPORTED_DISK_"
        "BEATS_006D="
        + (
            "YES"
            if c_independent
            < C006D
            else
            "NO"
        )
    )

    print()

    print(
        "=== 024B1 HELD-RIM PHYSICALIZATION ==="
    )

    print(
        "HELD_CASES="
        f"{len(held_rows)}"
    )

    print(
        "HELD_SAME_ENERGY_DEC_PASS_CASES="
        f"{same_energy_dec_pass}"
    )

    print(
        "HELD_MINIMUM_DEC_SUPPORT_"
        "INITIAL_OUTWARD_CASES="
        f"{corrected_outward}"
    )

    print(
        "HELD_MINIMUM_DEC_SUPPORT_"
        "BEATS_006D_CASES="
        f"{corrected_beats_006d}"
    )

    print(
        "HELD_MINIMUM_DEC_SUPPORT_"
        "GE10X_CASES="
        f"{corrected_ge10}"
    )

    print(
        "HELD_MINIMUM_DEC_SUPPORT_"
        "POSITIVE_STAGE_IMPULSE_CASES="
        f"{corrected_positive_impulse}"
    )

    print(
        "HELD_MINIMUM_REQUIRED_P_OVER_OLD_E="
        f"{min_required_p_over_old_e:.12f}"
    )

    print(
        "HELD_MAXIMUM_REQUIRED_P_OVER_OLD_E="
        f"{max_required_p_over_old_e:.12f}"
    )

    print(
        "HELD_MAX_CORRECTED_ETA="
        f"{max_corrected_eta:.15f}"
    )

    print()

    print(
        "=== FIXED 024B1 REFERENCE ==="
    )

    print(
        "REFERENCE_OLD_C="
        f"{float(reference['old_C']):.15f}"
    )

    print(
        "REFERENCE_OLD_ETA="
        f"{float(reference['old_eta']):.15f}"
    )

    print(
        "REFERENCE_REQUIRED_P_OVER_OLD_E="
        f"{float(reference['required_P_over_old_E_line']):.15f}"
    )

    print(
        "REFERENCE_OUTER_ENERGY_MULTIPLIER="
        f"{float(reference['outer_energy_multiplier_to_DEC_support']):.15f}"
    )

    print(
        "REFERENCE_MINIMUM_SUPPORT_"
        "ACTIVE_OVER_OLD_OUTER_E="
        f"{float(reference['minimum_support_active_over_old_outer_E']):.15f}"
    )

    print(
        "REFERENCE_WALL_OUTWARD="
        f"{float(reference['wall_outward']):+.15f}"
    )

    print(
        "REFERENCE_MINIMUM_SUPPORT_INWARD="
        f"{float(reference['minimum_support_inward']):+.15f}"
    )

    print(
        "REFERENCE_CORRECTED_INITIAL_OUTWARD="
        f"{float(reference['corrected_initial_outward']):+.15f}"
    )

    print(
        "REFERENCE_CORRECTED_ETA="
        f"{float(reference['corrected_eta']):+.15f}"
    )

    print(
        "REFERENCE_PHYSICAL_LOCAL_SUPPORT_SIGN="
        + (
            "OUTWARD"
            if bool(
                reference[
                    "corrected_initial_outward_yes"
                ]
            )
            else
            "INWARD"
        )
    )

    print()

    print(
        "=== OPTIMISTIC ANNULAR-HOLE CHECK ==="
    )

    print(
        "ANNULAR_BEST_C="
        f"{best_annular[0]:.15f}"
    )

    print(
        "ANNULAR_BEST_X="
        f"{best_annular[1]:.15f}"
    )

    print(
        "ANNULAR_BEST_Y_OVER_X="
        f"{best_annular[3]:.15f}"
    )

    print(
        "ANNULAR_BEST_NONZERO_HOLE_C="
        f"{best_nonzero_hole[0]:.15f}"
    )

    print(
        "ANNULAR_HOLE_BEATS_005B="
        + (
            "YES"
            if best_annular[
                0
            ]
            <
            C005B
            * (
                1.0
                - 2.0e-4
            )
            else
            "NO"
        )
    )

    print(
        "INNER_HOLE_STRING_ENERGY_IN_"
        "ANNULAR_BOUND=OMITTED_OPTIMISTICALLY"
    )

    print()

    print(
        "=== 024B2 DECISION ==="
    )

    print(
        "024B1_HELD_RIM_TARGET="
        "RELAXED_ONLY"
    )

    print(
        "SAME_ENERGY_LOCAL_STATIONARY_SUPPORT="
        "RED_DEC"
    )

    print(
        "LOCAL_STATIONARY_RIM_LOW_ACTIVE_"
        "SUPPORT="
        + (
            "RED"
            if local_stationary_support_closed
            else
            "REVIEW"
        )
    )

    print(
        "GENERIC_VORTON_NO_GO=NO"
    )

    print(
        "PULSE_BRANCH="
        f"{pulse_decision}"
    )

    print(
        "NEXT_PULSE="
        f"{next_pulse}"
    )

    print(
        "NEXT_STATIC="
        "KEEP_006D_DISTRIBUTED_STRESS_TRANSFER_"
        "AS_STATIC_DESIGN_ANCHOR_AND_CONTINUE_"
        "GENUINELY_NEW_MICROSCOPIC_RERANK"
    )

    print(
        "ANALOGUE_ANTIGRAVITY="
        "ACTIVE_IN_TANDEM"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )

    print(
        "SUMMARY_JSON="
        f"{OUT_SUMMARY.relative_to(ROOT)}"
    )

    print(
        "SCAN_CSV="
        f"{OUT_SCAN.relative_to(ROOT)}"
    )

    print(
        "024B2_RUN_COMPLETE=YES"
    )


if __name__ == "__main__":
    main()
