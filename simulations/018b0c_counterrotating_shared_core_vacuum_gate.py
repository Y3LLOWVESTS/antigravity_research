#!/usr/bin/env python3
"""Simulation 018B-0C — counterrotating shared-core microscopic composition gate.

PURPOSE
-------
Resolve the first microscopic ambiguity exposed when moving from the validated
018A-8 source-level construction toward a true 018B Euler-Lagrange field solve.

018A-8 uses two equal counterrotating 017P superconducting-string/vorton rim
copies. At the effective stress-energy level their opposite longitudinal
momenta cancel while their diagonal energy and active-source contributions add.
A full microscopic PDE cannot simply say "two copies"; it must specify actual
local field degrees of freedom.

This gate tests the minimal coincident/shared-core interpretation:

    one published set-G vortex-forming phi/gauge core
    + two independent copies sigma_+, sigma_- of the published 017P current
      condensate sector
    + opposite worldsheet currents so T_tz cancels.

ACTIVE SCIENTIFIC QUESTION
--------------------------
Can two independent 017P sigma sectors occupy one shared vortex core while the
published set-G exterior vacuum remains the true bulk vacuum?

This question is cheaper and more fundamental than attempting a large toroidal
BVP first. If duplicating the local condensate sector already makes a different
homogeneous phase lower in energy, the intended localized string is only a
local/metastable vacuum against bulk phase conversion and this minimal
composition must not be used as the 018B matter model.

PHYSICAL MODEL
--------------
The published/project 017P potential for one current condensate is

    V = lambda_phi/4 (|phi|^2-eta_phi^2)^2
        + lambda_sigma/4 (|sigma|^2-eta_sigma^2)^2
        + beta |phi|^2 |sigma|^2.

For M independent identical sigma sectors sharing the same phi core, subtract
the constant that normalizes the intended exterior vacuum

    |phi| = eta_phi,
    sigma_i = 0

to zero. Along the explicit competing homogeneous configuration

    phi = 0,
    |sigma_i| = eta_sigma  for every i,

the relative bulk potential is exactly

    Delta V_core(M)
      = lambda_phi eta_phi^4/4
        - M lambda_sigma eta_sigma^4/4.

Therefore the exhibited core phase becomes lower than the intended exterior
vacuum whenever

    M > M_crit

with

    M_crit
      = lambda_phi eta_phi^4
        / (lambda_sigma eta_sigma^4).

For the actual 017P set-G parameters this is a direct algebraic test.

GLOBAL-MINIMUM CROSSCHECK
-------------------------
Write x=|phi|^2 and y=|sigma|^2 for the equal-sigma branch. The normalized
homogeneous potential is a quadratic polynomial in x,y on x>=0,y>=0. Its
candidate minima are therefore exhausted by:

1. the intended exterior boundary minimum y=0, x=eta_phi^2;
2. the condensate-core boundary minimum x=0, y=eta_sigma^2;
3. the origin;
4. any nonnegative interior stationary point.

Because the duplicated sectors are independent and identical, at fixed x each
sigma sector minimizes the same one-variable function. A global minimum can
therefore be represented on the equal-sigma branch.

The script evaluates all homogeneous candidates analytically and independently
checks the ordering on a dense numerical x-y grid containing the exact special
points. The negative result does not depend on optimizer convergence.

IMPORTANT SCOPE
---------------
This gate tests ONLY the naive coincident construction made by duplicating the
entire independent sigma Mexican-hat sector while sharing one phi/gauge core.

It does NOT reject:

- gauged vortons generally;
- two spatially separated vorton/string cores;
- literature multi-current strings with a different joint condensate
  potential or internal symmetry;
- non-Abelian current carriers;
- a future explicitly re-derived two-current EOS;
- the validated 018A-8 source-level gravitational result.

The existing KLS wall sector is not used as an undocumented rescue term here.
If the naive duplicated 017P sector fails, any alternative combined
multi-current/KLS field theory must be specified and re-derived explicitly
before a full toroidal solve.

UNITS
-----
The test uses the same dimensionless natural-unit normalization as the 017P
set-G straight-string BVP and 018A-2 core-binding preflight.

SIGN CONVENTION
---------------
Delta V < 0 means the exhibited homogeneous competing phase has lower bulk
potential energy density than the intended exterior vacuum.

ASSUMPTIONS
-----------
- two sigma sectors are independent identical copies of the 017P sigma
  potential and beta coupling;
- both share one phi/gauge core;
- the exterior vacuum is required to remain |phi|=eta_phi, sigma_i=0;
- no new stabilizing interaction is added after observing the result;
- zero-temperature field theory;
- this is a microscopic matter-potential gate, not a gravity calculation.

VALIDATION STRATEGY
-------------------
1. Import the actual set-G constants from repository Simulation 018A-2.
2. Derive M_crit analytically.
3. Evaluate the exact competing-phase energy at M=1 and M=2.
4. Exhaust the homogeneous stationary/boundary candidates analytically.
5. Independently reproduce the ordering on a dense numerical x-y grid.
6. Verify the intended exterior vacuum remains a local minimum by checking its
   phi and sigma curvature masses.
7. Report how much eta_sigma or lambda_sigma would have to change merely to
   restore bulk ordering at M=2. These are diagnostics, not rescue knobs.

FALSIFIER / STOP RULE
---------------------
If

    Delta V_core(2) < 0

while the one-sigma model has the correct exterior ordering and the intended
vacuum has positive local curvatures, classify the naive shared-core
independent-two-sigma construction as rejected by bulk-vacuum ordering.

Do not launch a full toroidal PDE for that microscopic model and do not retune
published set-G parameters simply to rescue it.

If instead Delta V_core(2) >= 0, this gate is not sufficient for promotion;
the next step would be continuation of the actual shared-core straight-string
BVP to multiplicity two, EOS identity checks, and m=2..40 stability.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_018B0C_SHARED_CORE_COUNTERROTATION_VACUUM_GATE

WHAT THIS FILE DOES NOT ESTABLISH
---------------------------------
- a true 018B global toroidal field solution;
- complete composite dynamical stability;
- nonlinear Einstein-matter consistency;
- practical energy scaling;
- experimental accessibility;
- a practical antigravity device;
- new physics or novelty.
"""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PARENT = (
    ROOT
    / "simulations"
    / "018a2_nonthermal_core_binding_preflight.py"
)


def load_module(
    name: str,
    path: Path,
):
    """Import a project simulation without invoking its main function."""

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
    "ag018b0c_parent",
    PARENT,
)


GRID_POINTS = 1201


def normalized_potential_xy(
    x,
    y,
    multiplicity: float,
):
    """Return the normalized homogeneous potential in x and y.

    Parameters
    ----------
    x:
        Squared shared vortex-forming amplitude,

            x = |phi|^2.

    y:
        Squared amplitude of each identical current-carrier field,

            y = |sigma|^2.

    multiplicity:
        Number of independent identical sigma sectors.

    Returns
    -------
    float or numpy.ndarray
        Potential density relative to the intended exterior vacuum.

    Notes
    -----
    The constant subtraction changes no Euler-Lagrange equation. It only makes

        |phi| = eta_phi
        sigma_i = 0

    have exactly zero reference potential.
    """

    return (
        0.25
        *
        p.LAMBDA_PHI
        *
        (
            x
            -
            p.ETA_PHI**2
        ) ** 2

        +

        multiplicity
        *
        (
            0.25
            *
            p.LAMBDA_SIGMA
            *
            (
                y
                -
                p.ETA_SIGMA**2
            ) ** 2

            +

            p.BETA
            *
            x
            *
            y

            -

            0.25
            *
            p.LAMBDA_SIGMA
            *
            p.ETA_SIGMA**4
        )
    )


def competing_core_delta_v(
    multiplicity: float,
) -> float:
    """Return exact energy of the homogeneous condensate-core phase.

    The explicit configuration is

        phi = 0
        |sigma_i| = eta_sigma

    for every independent current-carrier sector.
    """

    return float(
        0.25
        *
        p.LAMBDA_PHI
        *
        p.ETA_PHI**4

        -

        multiplicity
        *
        0.25
        *
        p.LAMBDA_SIGMA
        *
        p.ETA_SIGMA**4
    )


def critical_multiplicity() -> float:
    """Return multiplicity where the explicit competing phase is degenerate."""

    return float(
        p.LAMBDA_PHI
        *
        p.ETA_PHI**4

        /

        (
            p.LAMBDA_SIGMA
            *
            p.ETA_SIGMA**4
        )
    )


def exterior_vacuum_curvatures() -> tuple[
    float,
    float,
]:
    """Return local radial curvatures at the intended exterior vacuum.

    Around

        |phi| = eta_phi
        sigma = 0

    the radial-amplitude second derivatives are

        m_phi^2
          =
          2 lambda_phi eta_phi^2

    and

        m_sigma,eff^2
          =
          -lambda_sigma eta_sigma^2
          +
          2 beta eta_phi^2.

    Positive values mean the intended exterior vacuum remains a local minimum
    even if a lower phase exists elsewhere in field space.
    """

    phi_curvature = (
        2.0
        *
        p.LAMBDA_PHI
        *
        p.ETA_PHI**2
    )

    sigma_curvature = (
        -p.LAMBDA_SIGMA
        *
        p.ETA_SIGMA**2

        +

        2.0
        *
        p.BETA
        *
        p.ETA_PHI**2
    )

    return (
        float(
            phi_curvature
        ),
        float(
            sigma_curvature
        ),
    )


def interior_stationary_point(
    multiplicity: float,
):
    """Return the nonnegative interior stationary point if it exists.

    In

        x = |phi|^2
        y = |sigma|^2

    stationarity gives

        lambda_phi/2 (x-eta_phi^2)
        + M beta y
        = 0

    and

        lambda_sigma/2 (y-eta_sigma^2)
        + beta x
        = 0.

    This is a two-by-two linear system.
    """

    matrix = np.array(
        [
            [
                0.5
                *
                p.LAMBDA_PHI,

                multiplicity
                *
                p.BETA,
            ],
            [
                p.BETA,

                0.5
                *
                p.LAMBDA_SIGMA,
            ],
        ],
        dtype=float,
    )

    rhs = np.array(
        [
            0.5
            *
            p.LAMBDA_PHI
            *
            p.ETA_PHI**2,

            0.5
            *
            p.LAMBDA_SIGMA
            *
            p.ETA_SIGMA**2,
        ],
        dtype=float,
    )

    determinant = float(
        np.linalg.det(
            matrix
        )
    )

    if abs(
        determinant
    ) < 1.0e-14:
        return None

    x, y = np.linalg.solve(
        matrix,
        rhs,
    )

    if (
        x < 0.0
        or
        y < 0.0
    ):
        return None

    return {
        "x": float(
            x
        ),
        "y": float(
            y
        ),
        "v": float(
            normalized_potential_xy(
                x,
                y,
                multiplicity,
            )
        ),
    }


def exact_candidate_minimum(
    multiplicity: float,
) -> dict[
    str,
    float | str,
]:
    """Exhaust the homogeneous boundary and stationary candidates.

    The potential is coercive in the nonnegative x-y quadrant.

    Boundary minima are:

        y = 0:
            x = eta_phi^2

        x = 0:
            y = eta_sigma^2

    The origin and any nonnegative interior stationary point are also checked.

    Because every independent sigma sector contributes the same function at
    fixed x, the multi-sector global minimum can be represented with equal
    sigma amplitudes.
    """

    candidates = [
        (
            "INTENDED_EXTERIOR",
            p.ETA_PHI**2,
            0.0,
            float(
                normalized_potential_xy(
                    p.ETA_PHI**2,
                    0.0,
                    multiplicity,
                )
            ),
        ),
        (
            "CONDENSATE_CORE",
            0.0,
            p.ETA_SIGMA**2,
            float(
                normalized_potential_xy(
                    0.0,
                    p.ETA_SIGMA**2,
                    multiplicity,
                )
            ),
        ),
        (
            "ORIGIN",
            0.0,
            0.0,
            float(
                normalized_potential_xy(
                    0.0,
                    0.0,
                    multiplicity,
                )
            ),
        ),
    ]

    interior = (
        interior_stationary_point(
            multiplicity
        )
    )

    if interior is not None:
        candidates.append(
            (
                "INTERIOR_STATIONARY",
                interior[
                    "x"
                ],
                interior[
                    "y"
                ],
                interior[
                    "v"
                ],
            )
        )

    best = min(
        candidates,
        key=lambda row: row[
            3
        ],
    )

    return {
        "label": best[
            0
        ],
        "x": float(
            best[
                1
            ]
        ),
        "y": float(
            best[
                2
            ]
        ),
        "v": float(
            best[
                3
            ]
        ),
    }


def dense_grid_minimum(
    multiplicity: float,
) -> dict[
    str,
    float,
]:
    """Independently reconstruct the ordering on a dense x-y grid.

    Exact exterior/core values are explicitly inserted into the coordinate
    arrays so the numerical grid cannot miss either decisive boundary point.

    The grid is only an independent verification layer. The central result is
    algebraic.
    """

    x_max = (
        1.35
        *
        p.ETA_PHI**2
    )

    y_max = (
        2.25
        *
        p.ETA_SIGMA**2
    )

    x = np.unique(
        np.concatenate(
            [
                np.linspace(
                    0.0,
                    x_max,
                    GRID_POINTS,
                ),
                np.array(
                    [
                        p.ETA_PHI**2
                    ]
                ),
            ]
        )
    )

    y = np.unique(
        np.concatenate(
            [
                np.linspace(
                    0.0,
                    y_max,
                    GRID_POINTS,
                ),
                np.array(
                    [
                        p.ETA_SIGMA**2
                    ]
                ),
            ]
        )
    )

    best_v = math.inf
    best_x = math.nan
    best_y = math.nan

    # Row-wise vectorized evaluation avoids allocating a very large 2D mesh.
    for xv in x:

        values = (
            normalized_potential_xy(
                xv,
                y,
                multiplicity,
            )
        )

        index = int(
            np.argmin(
                values
            )
        )

        value = float(
            values[
                index
            ]
        )

        if value < best_v:
            best_v = value
            best_x = float(
                xv
            )
            best_y = float(
                y[
                    index
                ]
            )

    return {
        "x": best_x,
        "y": best_y,
        "v": best_v,
    }


def threshold_diagnostics() -> dict[
    str,
    float,
]:
    """Return parameter shifts required only to restore M=2 ordering.

    These are not proposed parameter choices.

    Any real parameter change would invalidate the inherited 017P EOS and
    therefore require complete reconstruction of:

    - straight-string BVP;
    - EOS identity;
    - worldsheet stability;
    - integer matching;
    - microscopic wall/junction;
    - gravity;
    - robustness.
    """

    eta_sigma_max_m2 = (
        p.LAMBDA_PHI
        *
        p.ETA_PHI**4

        /

        (
            2.0
            *
            p.LAMBDA_SIGMA
        )
    ) ** 0.25

    lambda_sigma_max_m2 = (
        p.LAMBDA_PHI
        *
        p.ETA_PHI**4

        /

        (
            2.0
            *
            p.ETA_SIGMA**4
        )
    )

    return {
        "eta_sigma_max_m2":
            float(
                eta_sigma_max_m2
            ),

        "eta_sigma_fraction_of_current":
            float(
                eta_sigma_max_m2
                /
                p.ETA_SIGMA
            ),

        "lambda_sigma_max_m2":
            float(
                lambda_sigma_max_m2
            ),

        "lambda_sigma_fraction_of_current":
            float(
                lambda_sigma_max_m2
                /
                p.LAMBDA_SIGMA
            ),
    }


def main() -> None:
    """Run the shared-core counterrotation bulk-vacuum gate."""

    print(
        "=== 018B-0C — SHARED-CORE COUNTERROTATION "
        "MICROSCOPIC VACUUM GATE ==="
    )

    print(
        "\n=== IMPORTED 017P / 018A-2 SET-G CONSTANTS ==="
    )

    print(
        f"LAMBDA_PHI="
        f"{p.LAMBDA_PHI:.15e}"
    )

    print(
        f"LAMBDA_SIGMA="
        f"{p.LAMBDA_SIGMA:.15e}"
    )

    print(
        f"ETA_PHI="
        f"{p.ETA_PHI:.15e}"
    )

    print(
        f"ETA_SIGMA="
        f"{p.ETA_SIGMA:.15e}"
    )

    print(
        f"BETA="
        f"{p.BETA:.15e}"
    )

    print(
        f"CHI_SELECTED="
        f"{p.CHI_SELECTED:.15e}"
    )

    mcrit = (
        critical_multiplicity()
    )

    delta1 = (
        competing_core_delta_v(
            1.0
        )
    )

    delta2 = (
        competing_core_delta_v(
            2.0
        )
    )

    print(
        "\n=== EXACT BULK VACUUM ORDERING ==="
    )

    print(
        "CRITICAL_INDEPENDENT_SIGMA_MULTIPLICITY="
        f"{mcrit:.15e}"
    )

    print(
        "ONE_SIGMA_COMPETING_CORE_DELTA_V="
        f"{delta1:+.15e}"
    )

    print(
        "TWO_SIGMA_COMPETING_CORE_DELTA_V="
        f"{delta2:+.15e}"
    )

    print(
        "M2_MINUS_MCRIT="
        f"{2.0 - mcrit:+.15e}"
    )

    ordering_reversal = (
        delta1 > 0.0
        and
        delta2 < 0.0
        and
        1.0 < mcrit < 2.0
    )

    print(
        "ONE_SIGMA_INTENDED_VACUUM_BEATS_"
        "EXHIBITED_CORE_PHASE="
        +
        (
            "YES"
            if delta1 > 0.0
            else "NO"
        )
    )

    print(
        "TWO_SIGMA_EXHIBITED_CORE_PHASE_BEATS_"
        "INTENDED_VACUUM="
        +
        (
            "YES"
            if delta2 < 0.0
            else "NO"
        )
    )

    print(
        "DUPLICATION_FLIPS_BULK_VACUUM_ORDERING="
        +
        (
            "PASS"
            if ordering_reversal
            else "FAIL"
        )
    )

    (
        phi_curvature,
        sigma_curvature,
    ) = exterior_vacuum_curvatures()

    print(
        "\n=== LOCAL EXTERIOR-VACUUM CURVATURE ==="
    )

    print(
        "PHI_RADIAL_CURVATURE="
        f"{phi_curvature:+.15e}"
    )

    print(
        "SIGMA_RADIAL_CURVATURE_PER_SECTOR="
        f"{sigma_curvature:+.15e}"
    )

    local_minimum = (
        phi_curvature > 0.0
        and
        sigma_curvature > 0.0
    )

    print(
        "INTENDED_EXTERIOR_VACUUM_LOCAL_MINIMUM="
        +
        (
            "YES"
            if local_minimum
            else "NO"
        )
    )

    print(
        "\n=== EXACT HOMOGENEOUS CANDIDATE EXHAUSTION ==="
    )

    exact1 = (
        exact_candidate_minimum(
            1.0
        )
    )

    exact2 = (
        exact_candidate_minimum(
            2.0
        )
    )

    for (
        multiplicity,
        result,
    ) in (
        (
            1,
            exact1,
        ),
        (
            2,
            exact2,
        ),
    ):

        print(
            f"M={multiplicity} "
            f"EXACT_GLOBAL_CANDIDATE="
            f"{result['label']} "
            f"X="
            f"{float(result['x']):.15e} "
            f"Y="
            f"{float(result['y']):.15e} "
            f"V="
            f"{float(result['v']):+.15e}"
        )

    exact_crosscheck = (
        exact1[
            "label"
        ]
        ==
        "INTENDED_EXTERIOR"

        and

        abs(
            float(
                exact1[
                    "v"
                ]
            )
        )
        <
        1.0e-14

        and

        exact2[
            "label"
        ]
        ==
        "CONDENSATE_CORE"

        and

        abs(
            float(
                exact2[
                    "v"
                ]
            )
            -
            delta2
        )
        <
        1.0e-14
    )

    print(
        "EXACT_STATIONARY_BOUNDARY_EXHAUSTION="
        +
        (
            "PASS"
            if exact_crosscheck
            else "CHECK"
        )
    )

    print(
        "\n=== INDEPENDENT DENSE GRID CROSSCHECK ==="
    )

    grid1 = (
        dense_grid_minimum(
            1.0
        )
    )

    grid2 = (
        dense_grid_minimum(
            2.0
        )
    )

    for (
        multiplicity,
        result,
    ) in (
        (
            1,
            grid1,
        ),
        (
            2,
            grid2,
        ),
    ):

        print(
            f"M={multiplicity} "
            f"GRID_MIN_V="
            f"{result['v']:+.15e} "
            f"GRID_MIN_X="
            f"{result['x']:.15e} "
            f"GRID_MIN_Y="
            f"{result['y']:.15e}"
        )

    grid_crosscheck = (
        abs(
            grid1[
                "v"
            ]
        )
        <
        1.0e-12

        and

        abs(
            grid2[
                "v"
            ]
            -
            delta2
        )
        <
        1.0e-12
    )

    print(
        "DENSE_GRID_BULK_ORDERING_CROSSCHECK="
        +
        (
            "PASS"
            if grid_crosscheck
            else "CHECK"
        )
    )

    thresholds = (
        threshold_diagnostics()
    )

    print(
        "\n=== ORDERING-RESTORATION DIAGNOSTICS — "
        "NOT RESCUE PARAMETERS ==="
    )

    print(
        "ETA_SIGMA_MAX_FOR_M2_ORDERING_ONLY="
        f"{thresholds['eta_sigma_max_m2']:.15e}"
    )

    print(
        "ETA_SIGMA_MAX_OVER_CURRENT="
        f"{thresholds['eta_sigma_fraction_of_current']:.15e}"
    )

    print(
        "LAMBDA_SIGMA_MAX_FOR_M2_ORDERING_ONLY="
        f"{thresholds['lambda_sigma_max_m2']:.15e}"
    )

    print(
        "LAMBDA_SIGMA_MAX_OVER_CURRENT="
        f"{thresholds['lambda_sigma_fraction_of_current']:.15e}"
    )

    print(
        "RETUNING_PUBLISHED_SET_G_TO_RESCUE_THIS_GATE="
        "NOT_AUTHORIZED"
    )

    print(
        "\n=== DECISION ==="
    )

    decisive_negative = (
        ordering_reversal
        and
        local_minimum
        and
        exact_crosscheck
        and
        grid_crosscheck
    )

    if decisive_negative:

        print(
            "NAIVE_COINCIDENT_INDEPENDENT_TWO_SIGMA_SHARED_CORE="
            "REJECTED_BY_BULK_VACUUM_ORDERING"
        )

        print(
            "018B0C_SHARED_CORE_COUNTERROTATION_GATE="
            "GREEN_NEGATIVE_RESULT"
        )

        print(
            "FULL_TOROIDAL_PDE_FOR_THIS_NAIVE_MICROSCOPIC_MODEL="
            "DO_NOT_RUN"
        )

        print(
            "VALIDATED_018A8_SOURCE_LEVEL_RESULT="
            "UNCHANGED"
        )

        print(
            "GAUGED_VORTONS_IN_GENERAL="
            "NOT_REJECTED"
        )

        print(
            "KLS_OR_ALTERNATIVE_MULTI_CURRENT_RESCUE="
            "REQUIRES_EXPLICIT_REDERIVATION"
        )

        print(
            "NEXT="
            "018B0D_LITERATURE_BACKED_MULTI_CURRENT_OR_"
            "SEPARATED_CORE_MICROSCOPIC_RERANK"
        )

    else:

        print(
            "NAIVE_COINCIDENT_INDEPENDENT_TWO_SIGMA_SHARED_CORE="
            "NOT_DECISIVELY_REJECTED"
        )

        print(
            "018B0C_SHARED_CORE_COUNTERROTATION_GATE="
            "RED_OR_OPEN"
        )

        print(
            "NEXT="
            "SHARED_CORE_STRAIGHT_STRING_MULTIPLICITY_"
            "CONTINUATION_AND_EOS_STABILITY"
        )

    print(
        "CURRENT_HEURISTIC="
        "APPROXIMATELY_66_PERCENT_NOT_A_PROBABILITY"
    )

    print(
        "HEURISTIC_INCREASE_FROM_THIS_GATE="
        "NO_MICROSCOPIC_COMPOSITION_CLOSEOUT_ONLY"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )

    print(
        "NEW_PHYSICS_DISCOVERY=NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_018B0C_SHARED_CORE_"
        "COUNTERROTATION_VACUUM_GATE"
    )


if __name__ == "__main__":
    main()
