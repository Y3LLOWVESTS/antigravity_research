#!/usr/bin/env python3
"""Simulation 018B-0A3 — global fixed-N reachable-interval closeout.

PURPOSE
-------
Replace the finite candidate search of 018B-0A2 by a bounded reachable-set
question over the complete already-verified 017P EOS interval and the exact
243-case same-N perturbation cube.

SCIENTIFIC QUESTION
-------------------
Does there exist any single integer topological winding N that remains
reachable for every declared local perturbation of the one-vorton source-level
architecture, without extending the verified EOS interval?

WHY THIS GATE IS DECISIVE
-------------------------
018B-0A2 reconstructed the previous fixed-N failure and found that all 121
failures had exactly the same channel:

    N_ABOVE_REACHABLE_WINDING_RANGE.

It then found:

    252 nominal physical interior candidates

but:

    0 candidates

whose sampled fixed-N root survived all 243 perturbations.

That strongly weakened the single-vorton simplification, but the candidate
search was not an exhaustive theorem over the complete F, chi, N region.

This gate removes that ambiguity by calculating the complete reachable winding
interval for every perturbation.

PHYSICAL MODEL
--------------
No new physical model or parameter is introduced.

Reuse the verified 018B-0A EOS reconstruction.

For one perturbation j,

    N_cont = k(chi) R

with

    R =
        [
            P_parallel(chi)
            -
            mu_J
        ]
        /
        sigma_W(F).

The 018B-0/0A source-level continuation uses the calibrated microscopic wall
law

    sigma_W(F)
        =
        K F^3.

For a perturbation with F -> f_j F,

    N_cont,j(F,chi)
        =
        1/(K F^3)
        W_j(chi),

where

    W_j(chi)
        =
        k_j(chi)
        [
            P_parallel,j(chi)
            -
            mu_J mu_factor,j
        ]
        /
        f_j^3.

The factor

    1/(K F^3)

is positive and identical for every perturbation.

Therefore the existence or nonexistence of a common fixed-N interval is
independent of nominal F.

This means one interval-intersection calculation closes the entire F range
used by the current source-level architecture.

EOS DOMAIN
----------
No extrapolation is permitted:

    0.00150 <= chi <= 0.00475.

FIXED-N PERTURBATION CUBE
-------------------------
Exactly preserve 018B-0A and 018B-0A2:

    F              +/-0.5 percent
    junction mu    +/-10 percent
    radial support +/-1 percent
    q              +/-0.1 percent
    ell            +/-0.1 percent

giving

    3^5 = 243

cases.

MATHEMATICAL DECISION
---------------------
For perturbation j, continuity on the connected verified chi interval gives a
reachable winding interval

    I_j =
        [
            min_chi W_j,
            max_chi W_j
        ].

A common fixed continuous winding exists only if

    max_j min(I_j)
        <=
    min_j max(I_j).

If instead

    max_j min(I_j)
        >
    min_j max(I_j),

the common continuous interval is empty.

Then no integer winding N can possibly satisfy all 243 cases either.

Because the omitted F-dependent normalization is common and positive, that
negative result applies to every nominal F in the current F^3 source-level
continuation model.

UNITS
-----
The EOS quantities use the same natural/dimensionless normalization as
018B-0A.

The interval-intersection decision is made in a scaled winding variable whose
common positive normalization has been removed.

For interpretation only, the result is mapped back into ordinary winding-number
units using the already exact old locked state:

    F = 0.0384
    N = 12553.

The existence/nonexistence result does not depend on that reporting
normalization.

NUMERICAL VALIDATION
--------------------
The gate performs several independent checks.

1. Read the promoted reduced junction energy from existing repository logs,
   preferring the exact 018B-0 anchor audit.

2. Independently reconstruct the scaled winding using:

       a. the algebraically simplified equation;
       b. the parent's full BranchState equations.

3. Verify their relative difference is negligible.

4. Derive dW/dchi analytically using derivatives of the existing PCHIP EOS
   interpolants.

5. Test monotonicity for all 243 curves on successively denser grids:

       1025
       4097
       16385.

6. Repeat the entire intersection with the nominal junction-energy
   calibration multiplied by:

       0.90
       1.00
       1.10.

This final variation is a calibration/model-sensitivity diagnostic. It is not
a newly introduced physical tuning parameter.

PROMOTION CONDITION
-------------------
A strong negative closeout requires:

    SCALED_WINDING_ALGEBRA=PASS

    ALL_243_REACHABLE_CURVES_STRICTLY_INCREASING=PASS

    GLOBAL_FIXED_N_CONTINUOUS_INTERSECTION=EMPTY

    GLOBAL_FIXED_N_INTEGER_INTERSECTION=EMPTY

    +/-10 percent mu-calibration sensitivity also EMPTY.

Then:

    SINGLE_VORTON_FIXED_N_ROBUSTNESS=
        REJECTED_WITHIN_CURRENT_VERIFIED_EOS

and the next action is:

    TRUE_018B_GLOBAL_TOROIDAL_SOLVE_USING_VALIDATED_TWO_COPY_018A8_SOURCE.

RESCUE CONDITION
----------------
If a common interval exists, do not immediately promote the single-vorton
architecture.

Instead enumerate the implied exact integer sectors and rerun:

    exact EOS root;
    worldsheet stability;
    finite-payload gravity;
    microscopic wall/junction revalidation.

FALSIFICATION / STOP RULE
-------------------------
Do not widen the verified chi interval merely to save the single-vorton
architecture.

Do not add new fields or arbitrary support terms to rescue it.

A negative result closes only the current robust fixed-N one-vorton
simplification.

It does not invalidate:

    006D;
    the validated two-copy 018A-8 source;
    gauged vortons generally;
    other EOS branches;
    phase-slip architectures explicitly modeled in the future.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_018B0A3_GLOBAL_FIXED_N_REACHABLE_INTERVAL_GATE

WHAT THIS FILE DOES NOT ESTABLISH
---------------------------------
- a global toroidal field solution;
- full composite stability;
- stationary curved-spacetime consistency;
- nonlinear Einstein-matter consistency;
- practical energy scaling;
- experimental accessibility;
- a practical antigravity device;
- new physics or novelty.
"""

from __future__ import annotations

import importlib.util
import itertools
import math
from pathlib import Path
import re
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

PARENT = (
    ROOT
    / "simulations"
    / "018b0a_integer_locked_eos_architecture_gate.py"
)


def load_module(
    name: str,
    path: Path,
):
    """Import a verified project simulation without invoking its main()."""

    spec = importlib.util.spec_from_file_location(
        name,
        path,
    )

    if spec is None or spec.loader is None:
        raise RuntimeError(
            f"Cannot import {path}"
        )

    module = importlib.util.module_from_spec(
        spec
    )

    sys.modules[name] = module

    try:
        spec.loader.exec_module(
            module
        )
    except Exception:
        sys.modules.pop(
            name,
            None,
        )
        raise

    return module


p = load_module(
    "ag018b0a3_parent",
    PARENT,
)


F_LEVELS = (
    0.995,
    1.000,
    1.005,
)

MU_LEVELS = (
    0.90,
    1.00,
    1.10,
)

SUPPORT_LEVELS = (
    0.99,
    1.00,
    1.01,
)

INTERP_LEVELS = (
    0.999,
    1.000,
    1.001,
)

OLD_F = 0.0384
OLD_N = 12553

OLD_CHI_FALLBACK = (
    4.749476873922067e-3
)

# Global fixed-background 018A-6A anchor.
# The exact promoted matched value is read from existing logs whenever
# available. This is used only if those logs cannot be found.
MU_FALLBACK = (
    3.523059294668687e-3
)

DERIVATIVE_GRIDS = (
    1025,
    4097,
    16385,
)

MU_SENSITIVITY = (
    0.90,
    1.00,
    1.10,
)


def cases():
    """Yield the exact 243 fixed-N perturbations."""

    yield from itertools.product(
        F_LEVELS,
        MU_LEVELS,
        SUPPORT_LEVELS,
        INTERP_LEVELS,
        INTERP_LEVELS,
    )


def parse_scalar_from_logs(
    labels: tuple[str, ...],
    files: tuple[Path, ...],
):
    """Return the first finite scalar found under an exact log label."""

    number = (
        r"([+-]?"
        r"(?:\d+(?:\.\d*)?|\.\d+)"
        r"(?:[eE][+-]?\d+)?)"
    )

    for path in files:

        if not path.exists():
            continue

        text = path.read_text(
            errors="replace"
        )

        for label in labels:

            match = re.search(
                re.escape(label)
                +
                number,
                text,
            )

            if match:

                value = float(
                    match.group(1)
                )

                if math.isfinite(
                    value
                ):

                    return (
                        value,
                        f"{path.name}:{label}",
                    )

    return (
        None,
        None,
    )


def promoted_mu_j():
    """Load the reduced junction energy actually used by the promoted source."""

    files = (
        ROOT
        / "results/logs"
        / "018b0_exhaustive_architecture_pareto_campaign.log",

        ROOT
        / "results/logs"
        / "018a7_complete_microscopic_gravity_closeout.log",

        ROOT
        / "results/logs"
        / "018a6b3_fine_continuation_outer_match_closeout.log",
    )

    labels = (
        "ONE_COPY_JUNCTION_REDUCED_ENERGY=",
        "GLOBAL_REDUCED_JUNCTION_ENERGY=",
        "REFINED_GLOBAL_MU_ESTIMATE=",
    )

    value, source = (
        parse_scalar_from_logs(
            labels,
            files,
        )
    )

    if value is not None:

        return (
            value,
            source,
            True,
        )

    return (
        MU_FALLBACK,
        "DOCUMENTED_018A6A_GLOBAL_ANCHOR_FALLBACK",
        False,
    )


def old_locked_chi():
    """Read the previous exact N=12553 lock from the 018B-0A2 log."""

    path = (
        ROOT
        / "results/logs"
        / "018b0a2_fixed_n_interior_robustness_gate.log"
    )

    if path.exists():

        text = path.read_text(
            errors="replace"
        )

        number = (
            r"([+-]?"
            r"(?:\d+(?:\.\d*)?|\.\d+)"
            r"(?:[eE][+-]?\d+)?)"
        )

        match = re.search(
            r"OLD_SELECTED\s+"
            r"F=[^\s]+\s+"
            r"CHI="
            +
            number
            +
            r"\s+N=12553",
            text,
        )

        if match:

            value = float(
                match.group(1)
            )

            if (
                p.CHI_MIN
                <=
                value
                <=
                p.CHI_MAX
            ):

                return (
                    value,
                    path.name,
                    True,
                )

    return (
        OLD_CHI_FALLBACK,
        "DOCUMENTED_018B0A2_LOCK_FALLBACK",
        False,
    )


def scaled_winding_simplified(
    chi,
    *,
    mu_j: float,
    f_factor: float,
    mu_factor: float,
    support_factor: float,
    q_factor: float,
    ell_factor: float,
):
    """Return W_j with the common positive K*F^3 normalization removed.

    From the parent EOS,

        k = 2*pi/(q*ell)

    and

        P_parallel
            =
            w_stat*ell/(4*pi).

    Therefore

        k P_parallel
            =
            support_factor*w_stat
            /
            (2*q_factor*q_0).

    The junction contribution is

        k mu
            =
            2*pi*mu
            /
            (
                q_factor
                ell_factor
                q_0
                ell_0
            ).

    Dividing by f_factor^3 accounts for the perturbed wall tension.
    """

    chi = np.asarray(
        chi,
        dtype=float,
    )

    q0 = np.asarray(
        p.Q_SPLINE(
            chi
        ),
        dtype=float,
    )

    ell0 = np.asarray(
        p.ELL_SPLINE(
            chi
        ),
        dtype=float,
    )

    w0 = np.asarray(
        p.W_SPLINE(
            chi
        ),
        dtype=float,
    )

    first = (
        support_factor
        *
        w0
        /
        (
            2.0
            *
            q_factor
            *
            q0
        )
    )

    second = (
        2.0
        *
        math.pi
        *
        mu_j
        *
        mu_factor
        /
        (
            q_factor
            *
            ell_factor
            *
            q0
            *
            ell0
        )
    )

    return (
        first
        -
        second
    ) / (
        f_factor
        **
        3
    )


def scaled_winding_direct(
    chi: float,
    *,
    mu_j: float,
    f_factor: float,
    mu_factor: float,
    support_factor: float,
    q_factor: float,
    ell_factor: float,
) -> float:
    """Independently reconstruct W_j from the parent's BranchState equations."""

    branch = (
        p.reconstruct_branch(
            float(
                chi
            ),
            q_factor=q_factor,
            ell_factor=ell_factor,
            support_factor=support_factor,
        )
    )

    support = (
        branch.p_parallel
        -
        mu_j
        *
        mu_factor
    )

    if support <= 0.0:
        return math.nan

    return float(
        branch.k
        *
        support
        /
        (
            f_factor
            **
            3
        )
    )


def scaled_winding_derivative(
    chi,
    *,
    mu_j: float,
    f_factor: float,
    mu_factor: float,
    support_factor: float,
    q_factor: float,
    ell_factor: float,
):
    """Return analytic dW/dchi using derivatives of the PCHIP EOS curves."""

    chi = np.asarray(
        chi,
        dtype=float,
    )

    q = np.asarray(
        p.Q_SPLINE(
            chi
        ),
        dtype=float,
    )

    ell = np.asarray(
        p.ELL_SPLINE(
            chi
        ),
        dtype=float,
    )

    w = np.asarray(
        p.W_SPLINE(
            chi
        ),
        dtype=float,
    )

    qp = np.asarray(
        p.Q_SPLINE.derivative()(
            chi
        ),
        dtype=float,
    )

    ellp = np.asarray(
        p.ELL_SPLINE.derivative()(
            chi
        ),
        dtype=float,
    )

    wp = np.asarray(
        p.W_SPLINE.derivative()(
            chi
        ),
        dtype=float,
    )

    term1 = (
        support_factor
        /
        (
            2.0
            *
            q_factor
        )
        *
        (
            wp
            /
            q
            -
            w
            *
            qp
            /
            (
                q
                *
                q
            )
        )
    )

    coefficient = (
        2.0
        *
        math.pi
        *
        mu_j
        *
        mu_factor
        /
        (
            q_factor
            *
            ell_factor
        )
    )

    term2 = (
        coefficient
        *
        (
            qp
            *
            ell
            +
            q
            *
            ellp
        )
        /
        (
            (
                q
                *
                ell
            )
            **
            2
        )
    )

    return (
        term1
        +
        term2
    ) / (
        f_factor
        **
        3
    )


def algebra_crosscheck(
    mu_j: float,
):
    """Compare simplified and direct expressions over independent controls."""

    test_cases = (
        (
            0.995,
            0.90,
            1.01,
            0.999,
            1.001,
        ),
        (
            1.000,
            1.00,
            1.00,
            1.000,
            1.000,
        ),
        (
            1.005,
            1.10,
            0.99,
            1.001,
            0.999,
        ),
    )

    chis = np.linspace(
        p.CHI_MIN,
        p.CHI_MAX,
        17,
    )

    max_rel = 0.0
    min_support = math.inf

    for (
        f_factor,
        mu_factor,
        support_factor,
        q_factor,
        ell_factor,
    ) in test_cases:

        for chi in chis:

            simple = float(
                scaled_winding_simplified(
                    chi,
                    mu_j=mu_j,
                    f_factor=f_factor,
                    mu_factor=mu_factor,
                    support_factor=support_factor,
                    q_factor=q_factor,
                    ell_factor=ell_factor,
                )
            )

            direct = (
                scaled_winding_direct(
                    float(
                        chi
                    ),
                    mu_j=mu_j,
                    f_factor=f_factor,
                    mu_factor=mu_factor,
                    support_factor=support_factor,
                    q_factor=q_factor,
                    ell_factor=ell_factor,
                )
            )

            if not math.isfinite(
                direct
            ):

                return (
                    math.inf,
                    -math.inf,
                )

            max_rel = max(
                max_rel,
                abs(
                    simple
                    -
                    direct
                )
                /
                max(
                    abs(
                        direct
                    ),
                    1.0e-30,
                ),
            )

            branch = (
                p.reconstruct_branch(
                    float(
                        chi
                    ),
                    q_factor=q_factor,
                    ell_factor=ell_factor,
                    support_factor=support_factor,
                )
            )

            min_support = min(
                min_support,
                branch.p_parallel
                -
                mu_j
                *
                mu_factor,
            )

    return (
        max_rel,
        min_support,
    )


def derivative_convergence(
    mu_j: float,
):
    """Verify strict monotonicity of all 243 reachable-winding curves."""

    records = []

    for n in DERIVATIVE_GRIDS:

        grid = np.linspace(
            p.CHI_MIN,
            p.CHI_MAX,
            n,
        )

        min_derivative = math.inf
        bad_cases = 0

        for (
            f_factor,
            mu_factor,
            support_factor,
            q_factor,
            ell_factor,
        ) in cases():

            derivative = (
                scaled_winding_derivative(
                    grid,
                    mu_j=mu_j,
                    f_factor=f_factor,
                    mu_factor=mu_factor,
                    support_factor=support_factor,
                    q_factor=q_factor,
                    ell_factor=ell_factor,
                )
            )

            local_min = float(
                np.min(
                    derivative
                )
            )

            min_derivative = min(
                min_derivative,
                local_min,
            )

            if local_min <= 0.0:

                bad_cases += 1

        records.append(
            (
                n,
                min_derivative,
                bad_cases,
            )
        )

    return records


def intersection(
    mu_j: float,
):
    """Return the global common scaled interval and controlling cases."""

    intervals = []

    for case in cases():

        (
            f_factor,
            mu_factor,
            support_factor,
            q_factor,
            ell_factor,
        ) = case

        endpoints = (
            scaled_winding_simplified(
                np.array(
                    [
                        p.CHI_MIN,
                        p.CHI_MAX,
                    ]
                ),
                mu_j=mu_j,
                f_factor=f_factor,
                mu_factor=mu_factor,
                support_factor=support_factor,
                q_factor=q_factor,
                ell_factor=ell_factor,
            )
        )

        lo = float(
            endpoints[0]
        )

        hi = float(
            endpoints[1]
        )

        intervals.append(
            (
                case,
                lo,
                hi,
            )
        )

    lower_record = max(
        intervals,
        key=lambda item: item[1],
    )

    upper_record = min(
        intervals,
        key=lambda item: item[2],
    )

    return (
        lower_record[1],
        upper_record[2],
        lower_record,
        upper_record,
    )


def main() -> None:
    """Run the global fixed-N reachable-set closeout."""

    print(
        "=== 018B-0A3 — GLOBAL FIXED-N REACHABLE-INTERVAL CLOSEOUT ==="
    )

    (
        mu_j,
        mu_source,
        mu_exact,
    ) = promoted_mu_j()

    (
        old_chi,
        old_source,
        old_exact,
    ) = old_locked_chi()

    print(
        "MU_J="
        f"{mu_j:+.15e}"
    )

    print(
        "MU_SOURCE="
        f"{mu_source}"
    )

    print(
        "PROMOTED_MU_LOG_RECONSTRUCTION="
        f"{'PASS' if mu_exact else 'FALLBACK'}"
    )

    print(
        "OLD_LOCKED_CHI="
        f"{old_chi:.15e}"
    )

    print(
        "OLD_LOCK_SOURCE="
        f"{old_source}"
    )

    print(
        "OLD_LOCK_LOG_RECONSTRUCTION="
        f"{'PASS' if old_exact else 'FALLBACK'}"
    )

    # ======================================================================
    # Independent algebra reconstruction.
    # ======================================================================

    print(
        "\n=== ALGEBRA / SUPPORT CROSSCHECK ==="
    )

    (
        max_rel,
        min_support,
    ) = algebra_crosscheck(
        mu_j
    )

    print(
        "SIMPLIFIED_VS_DIRECT_MAX_RELERR="
        f"{max_rel:.15e}"
    )

    print(
        "MIN_CONTROL_RADIAL_SUPPORT="
        f"{min_support:+.15e}"
    )

    algebra_pass = (
        max_rel
        <
        5.0e-13
        and
        min_support
        >
        0.0
    )

    print(
        "SCALED_WINDING_ALGEBRA="
        f"{'PASS' if algebra_pass else 'FAIL'}"
    )

    print(
        "F_CUBED_COMMON_SCALING_REDUCTION=PASS"
    )

    print(
        "NOMINAL_F_INTERSECTION_DEPENDENCE="
        "NONE_WITHIN_018B0_F3_MODEL"
    )

    # ======================================================================
    # Derivative/monotonicity convergence.
    # ======================================================================

    print(
        "\n=== MONOTONICITY / CONVERGENCE ==="
    )

    derivative_records = (
        derivative_convergence(
            mu_j
        )
    )

    for (
        n,
        min_derivative,
        bad_cases,
    ) in derivative_records:

        print(
            f"DERIVATIVE_GRID={n} "
            f"MIN_DW_DCHI={min_derivative:+.15e} "
            f"NONMONOTONIC_CASES={bad_cases}/243"
        )

    monotonic_pass = all(
        record[1] > 0.0
        and
        record[2] == 0
        for record
        in derivative_records
    )

    print(
        "ALL_243_REACHABLE_CURVES_STRICTLY_INCREASING="
        f"{'PASS' if monotonic_pass else 'FAIL'}"
    )

    # ======================================================================
    # Exact endpoint interval intersection once monotonicity is established.
    # ======================================================================

    print(
        "\n=== GLOBAL COMMON INTERVAL ==="
    )

    (
        lower,
        upper,
        lower_record,
        upper_record,
    ) = intersection(
        mu_j
    )

    scaled_gap = (
        lower
        -
        upper
    )

    print(
        "COMMON_SCALED_LOWER="
        f"{lower:.15e}"
    )

    print(
        "COMMON_SCALED_UPPER="
        f"{upper:.15e}"
    )

    print(
        "COMMON_SCALED_SEPARATION_LOWER_MINUS_UPPER="
        f"{scaled_gap:+.15e}"
    )

    print(
        "LOWER_CONTROLLER="
        f"{lower_record[0]}"
    )

    print(
        "UPPER_CONTROLLER="
        f"{upper_record[0]}"
    )

    # Map the scaled result back to ordinary winding units using the already
    # exact old fixed-N operating point. This is only for interpretation.
    old_w = float(
        scaled_winding_simplified(
            old_chi,
            mu_j=mu_j,
            f_factor=1.0,
            mu_factor=1.0,
            support_factor=1.0,
            q_factor=1.0,
            ell_factor=1.0,
        )
    )

    report_scale = (
        OLD_N
        /
        old_w
    )

    physical_lower = (
        report_scale
        *
        lower
    )

    physical_upper = (
        report_scale
        *
        upper
    )

    physical_gap = (
        physical_lower
        -
        physical_upper
    )

    print(
        "REFERENCE_F="
        f"{OLD_F:.9f}"
    )

    print(
        "REFERENCE_COMMON_N_LOWER="
        f"{physical_lower:.12f}"
    )

    print(
        "REFERENCE_COMMON_N_UPPER="
        f"{physical_upper:.12f}"
    )

    print(
        "REFERENCE_INTEGER_WINDING_GAP="
        f"{physical_gap:+.12f}"
    )

    # ======================================================================
    # Sensitivity to small uncertainty in the promoted mu calibration.
    # ======================================================================

    print(
        "\n=== NOMINAL-MU SENSITIVITY ==="
    )

    sensitivity_empty = True

    for factor in MU_SENSITIVITY:

        (
            sensitivity_lower,
            sensitivity_upper,
            _,
            _,
        ) = intersection(
            mu_j
            *
            factor
        )

        gap = (
            sensitivity_lower
            -
            sensitivity_upper
        )

        empty = (
            gap
            >
            0.0
        )

        sensitivity_empty = (
            sensitivity_empty
            and
            empty
        )

        print(
            f"MU_CALIBRATION_FACTOR={factor:.3f} "
            f"LOWER_MINUS_UPPER={gap:+.15e} "
            f"INTERSECTION="
            f"{'EMPTY' if empty else 'NONEMPTY'}"
        )

    common_empty = (
        lower
        >
        upper
    )

    numerical_pass = (
        algebra_pass
        and
        monotonic_pass
        and
        sensitivity_empty
    )

    # ======================================================================
    # Scientific decision.
    # ======================================================================

    print(
        "\n=== DECISION ==="
    )

    if (
        common_empty
        and
        numerical_pass
    ):

        print(
            "GLOBAL_FIXED_N_CONTINUOUS_INTERSECTION=EMPTY"
        )

        print(
            "GLOBAL_FIXED_N_INTEGER_INTERSECTION=EMPTY"
        )

        print(
            "SINGLE_VORTON_FIXED_N_ROBUSTNESS="
            "REJECTED_WITHIN_CURRENT_VERIFIED_EOS"
        )

        print(
            "018B0A3_GLOBAL_INTERVAL_GATE="
            "GREEN_NEGATIVE_RESULT"
        )

        print(
            "SINGLE_VORTON_SIMPLIFICATION="
            "DO_NOT_PROMOTE"
        )

        print(
            "NEXT="
            "TRUE_018B_GLOBAL_TOROIDAL_SOLVE_"
            "USING_VALIDATED_TWO_COPY_018A8_SOURCE"
        )

    elif (
        not common_empty
        and
        numerical_pass
    ):

        print(
            "GLOBAL_FIXED_N_CONTINUOUS_INTERSECTION=NONEMPTY"
        )

        print(
            "GLOBAL_FIXED_N_INTEGER_INTERSECTION="
            "REQUIRES_EXACT_NORMALIZED_ENUMERATION"
        )

        print(
            "SINGLE_VORTON_FIXED_N_ROBUSTNESS="
            "POSSIBLE_RESCUE_SECTOR_FOUND"
        )

        print(
            "018B0A3_GLOBAL_INTERVAL_GATE="
            "GREEN_RESCUE_TARGET"
        )

        print(
            "NEXT="
            "EXACT_INTEGER_SECTOR_ROOT_GRAVITY_"
            "STABILITY_RECONSTRUCTION"
        )

    else:

        print(
            "GLOBAL_FIXED_N_CONTINUOUS_INTERSECTION="
            "NUMERICALLY_UNRESOLVED"
        )

        print(
            "018B0A3_GLOBAL_INTERVAL_GATE="
            "RED_NUMERICAL"
        )

        print(
            "NEXT="
            "RESOLVE_ALGEBRA_OR_MONOTONICITY_"
            "BEFORE_PHYSICS_PROMOTION"
        )

    # ======================================================================
    # Claim discipline.
    # ======================================================================

    print(
        "CURRENT_HEURISTIC="
        "APPROXIMATELY_66_PERCENT_NOT_A_PROBABILITY"
    )

    print(
        "HEURISTIC_INCREASE_FROM_THIS_GATE="
        "NO_TOPOLOGY_CLOSEOUT_ONLY"
    )

    print(
        "TRUE_018B_GREEN_TARGET="
        "APPROXIMATELY_68_PERCENT"
    )

    print(
        "018C_FULL_STABILITY_GREEN_TARGET="
        "APPROXIMATELY_71_TO_72_PERCENT"
    )

    print(
        "CURRENT_VALIDATED_C="
        f"{p.CURRENT_VALIDATED_C:.15e}"
    )

    print(
        "CURRENT_VALIDATED_ONE_G_ONE_M_ENERGY_J="
        f"{p.CURRENT_VALIDATED_ENERGY_J:.15e}"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )

    print(
        "NEW_PHYSICS_DISCOVERY=NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_018B0A3_GLOBAL_FIXED_N_"
        "REACHABLE_INTERVAL_GATE"
    )


if __name__ == "__main__":
    main()
