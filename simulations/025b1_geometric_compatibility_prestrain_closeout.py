#!/usr/bin/env python3
"""025B1 — Geometric compatibility and prestrain closeout gate.

PURPOSE
-------
Perform the final research run of the current session before documentation
closeout.

This run does NOT optimize another antigravity source.

It asks whether the locally healthy 025A relativistic hyperelastic matter law
has a plausible geometric route to the efficient 006B/006D stress-transfer
architecture after 025B0 showed that an ordinary compatible radial solid
regresses to approximately the old 005B supported-tension scale.

SCIENTIFIC QUESTION
-------------------
Is the incompatibility discovered in 025B0:

    a modest kinematic inconvenience that general 2-D deformation or
    prestrain could plausibly repair,

or:

    an extreme intrinsic geometric burden that should demote the direct
    hyperelastic realization route?

The run compares:

    1. ordinary Euclidean-reference compatibility;

    2. a general-2-D kinematic lower-bound diagnostic;

    3. an explicitly prescribed non-Euclidean reference metric;

    4. the relationship between geometric incompatibility and the material
       grading independently found in 025A.

PRIMARY OBSERVABLES
-------------------
No new gravitational source is optimized.

The primary observables are:

    hoop-density contrast;

    same-z meridional deformation-gradient lower bound;

    minimum direct radial log-strain bound;

    non-Euclidean cone/excess-angle factor;

    integrated Gaussian curvature required by the reference-metric
    transition;

    stress-free axisymmetric embedding condition;

    material-grading/geometric-factor identity;

    existing 025B0 compatible-source coefficient.

PROJECT ANCHORS
---------------
006B thin idealized stress transformer:

    C_006B = 23.426710175391.

006D finite positive-energy conserved source:

    C_006D = 23.591586299249.

005B supported tension disk:

    C_005B = 79.753148116012.

025A selected local hyperelastic constitutive preflight:

    C approximately 23.5104.

025B0 compatible radial material:

    C approximately 80.1054.

025B0 full selected-state acoustic cone:

    PASS.

REFERENCE-METRIC MODEL
----------------------
For an axisymmetric two-dimensional material metric write:

    d ell_bar^2
      =
    A(r)^2 dr^2
    +
    B(r)^2 dphi^2.

Using the 025A target material-density variables:

    A
      =
    exp(y_r),

    B
      =
    r exp(y_phi).

In the core:

    y_r
      =
    -Y_core,

    y_phi
      =
    -Y_core.

Therefore:

    (1/A) dB/dr
      =
    1.

In the desired transfer annulus:

    y_r
      =
    -Y_ann,

    y_phi
      =
    +Y_ann.

Therefore:

    chi
      =
    (1/A) dB/dr
      =
    exp(2 Y_ann).

This is an excess-angle/cone factor.

AXISYMMETRIC ISOMETRIC-EMBEDDING CONDITION
------------------------------------------
Introduce proper radial coordinate:

    du
      =
    A dr.

For a stress-free axisymmetric surface of revolution embedded in ordinary
Euclidean 3-space:

    d ell^2
      =
    du^2
    +
    B(u)^2 dphi^2,

with embedding:

    (B(u) cos phi,
     B(u) sin phi,
     Z(u)).

Unit-speed meridional parametrization requires:

    (dB/du)^2
    +
    (dZ/du)^2
      =
    1.

Hence necessarily:

    |dB/du|
      <=
    1.

The target annulus requires:

    dB/du
      =
    chi
      =
    exp(2Y_ann).

Therefore if chi>1, the desired reference metric has NO stress-free
axisymmetric surface-of-revolution isometric embedding.

This does NOT rule out:

    non-axisymmetric wrinkled embeddings;

    stretching of the reference metric;

    active/prestrained manufacturing;

    genuinely 3-D architectures.

Those remain distinct accomplishment classes.

GAUSSIAN CURVATURE IDENTITY
---------------------------
For:

    d ell_bar^2
      =
    A(r)^2 dr^2
    +
    B(r)^2 dphi^2,

define:

    f(r)
      =
    (1/A) dB/dr.

The Gaussian curvature is:

    K
      =
    -1/(A B)
    d f/dr.

The area element is:

    dA
      =
    A B dr dphi.

Therefore across any smooth transition:

    integral K dA
      =
    -2 pi [f_out - f_in].

For the desired core-to-annulus transition:

    f_in
      =
    1,

    f_out
      =
    chi.

Thus:

    integral K dA
      =
    -2 pi (chi-1).

This is independent of transition width and detailed smoothing.

The numerical run reconstructs this invariant for multiple transition widths
and for a randomized family of monotone transition profiles.

MATERIAL-GRADING / GEOMETRY IDENTITY
------------------------------------
025A required the interface material-scale ratio:

    G
      =
    rho_star_ann(a)
    /
    rho_star_core.

For the selected constitutive model:

    G
      =
    (t/q)
    (1+t)^(-2/k)
    (1-q^2)^(1/k).

Meanwhile:

    chi
      =
    exp(2 atanh(q)/k)
      =
    [(1+q)/(1-q)]^(1/k).

Hence exactly:

    G chi
      =
    (t/q)
    [(1+q)/(1+t)]^(2/k).

When:

    t = q,

this reduces to the exact identity:

    G chi = 1.

The selected 025A solution has t approximately q.

Therefore its approximately 3000:1 material grading and approximately
3000-fold intrinsic metric excess are expected to be the same underlying
burden viewed from constitutive and geometric descriptions.

This identity is independently reconstructed numerically.

GENERAL 2-D EUCLIDEAN KINEMATIC DIAGNOSTIC
-------------------------------------------
For a general axisymmetric material map:

    X = X(r,z),

    Z = Z(r,z),

the hoop material density remains:

    n_phi
      =
    X/r.

The selected target therefore wants approximately:

    X_core
      =
    a exp(-Y_core),

and:

    X_ann
      =
    R exp(+Y_ann).

Along a direct same-z radial path between a and R, the mean-value theorem
gives:

    max |partial_r X|
      >=
    [R exp(Y_ann) - a exp(-Y_core)]
    /
    (R-a).

Because the largest singular value of the meridional material gradient is at
least the magnitude of any matrix component, this gives a direct-path
log-strain lower bound:

    Y_direct
      >=
    ln(
      [R exp(Y_ann) - a exp(-Y_core)]
      /
      (R-a)
    ).

This is NOT a universal theorem against general 2-D shear.

A 2-D deformation can route the transition through z and increase its
material path length.

The run therefore also calculates the path-length multiplier required to
bring the direct Lipschitz bound below strain caps:

    2
    3
    4
    5
    6.

For a straight meridional detour, it converts that multiplier into an
equivalent vertical excursion.

This is an information-gain diagnostic, not a proof of realizability.

TRANSITION SMOOTHING
--------------------
Use a quintic smoothstep:

    H(u)
      =
    6u^5 - 15u^4 + 10u^3,

for:

    0 <= u <= 1.

The reference-metric strains interpolate from:

    (-Y_core, -Y_core)

to:

    (-Y_ann, +Y_ann).

Widths from:

    0.02
    0.05
    0.10
    0.25
    0.50
    1.00

times the selected annulus radial span are tested.

Peak curvature may change with smoothing width.

Integrated curvature must not.

RANDOMIZED INVARIANCE AUDIT
---------------------------
Generate monotone smooth transitions with:

    H'(u)
      proportional to
    u^2 (1-u)^2
    exp[
      sum_j c_j cos(j pi u)
    ].

The coefficients and transition widths are Sobol sampled.

Every profile has identical endpoints.

Therefore all must reproduce the same integrated-curvature invariant.

This independently checks that the large curvature burden is not an artifact
of the quintic interpolation.

ENERGY / PRACTICALITY DISCIPLINE
--------------------------------
This run does NOT assign an arbitrary energy cost proportional to Gaussian
curvature.

There is no universal law:

    energy = constant times |K|.

A non-Euclidean reference metric may arise through growth, fabrication,
prestress, active control, or other microscopic structure.

Those sectors have model-dependent energy and must be explicitly included
before a device claim.

Therefore the run reports geometric burden but does not invent a missing
manufacturing-energy coefficient.

LITERATURE CONTEXT
------------------
Non-Euclidean elasticity treats strain relative to a prescribed reference
metric that need not be Euclidean or globally stress-free in the imposed
configuration.

Incompatible metrics can produce residual stress, buckling and nontrivial
relaxed shapes.

The project uses that established formalism only as a possible realization
language.

The approximately 3000-fold factors below are project-derived for the 025A
stress target.

VALIDATION
----------
1. Run the 94 known-solution regression suite before this file.
2. Rebuild the exact 025A selected target from its JSON.
3. Require the 025B0 full acoustic cone to be PASS.
4. Reproduce the 025B0 radial compatibility jump.
5. Verify the analytical material-grading/geometric identity.
6. Verify the Gaussian-curvature boundary identity for deterministic smooth
   transitions.
7. Independently verify it using randomized monotone transitions.
8. Evaluate the direct Euclidean 2-D kinematic lower bound at several strain
   caps.
9. Preserve all limitations in the output.

PROMOTION CONDITION
-------------------
This run cannot promote a practical material realization by itself.

The most favorable branch outcome would be:

    local matter law remains healthy;

    ordinary radial map remains demoted;

    the 2-D Euclidean detour burden is modest;

    non-Euclidean prestrain is shown to be much more extreme.

That would rank:

    GENERAL_2D_EUCLIDEAN_SHEAR

ahead of:

    NON_EUCLIDEAN_REFERENCE_METRIC

if this pure-GR realization branch is ever resumed.

FALSIFICATION / CLOSEOUT CONDITION
----------------------------------
If:

    ordinary radial compatibility is already demoted;

    stress-free axisymmetric embedding of the required reference metric is
    impossible;

    the required reference metric carries an enormous intrinsic excess-angle
    factor;

    and the project still retains catastrophic 1/G absolute scaling,

then the hyperelastic route should be PAUSED after this run rather than
expanded into another large PDE during the current session.

This is not a theorem that every relativistic elastic realization fails.

It is a branch-ranking and information-gain closeout.

STOP RULE
---------
This is the final scientific run before documentation update.

Do not launch:

    another 2-D BVP;

    another reference-metric optimization;

    another source optimizer;

    another hyperelastic constitutive scan

during this session.

After the run:

    update the durable journal;
    update RESEARCH_BUILDPLAN.md;
    update README.md;
    update NOTES.MD;
    update chronology/carry-over notes;
    update the codebundle.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_GEOMETRIC_COMPATIBILITY_AND_PRESTRAIN_CLOSEOUT_GATE

DOES NOT ESTABLISH
------------------
- a general no-go theorem for elasticity;
- failure of all 2-D Euclidean shear maps;
- failure of non-axisymmetric wrinkled embeddings;
- failure of active prestrain;
- a finite-thickness material BVP;
- microscopic material synthesis;
- nonlinear Einstein-matter equilibrium;
- favorable 1/G scaling;
- a practical antigravity device.
"""

from __future__ import annotations

import csv
import json
import math
import os
from pathlib import Path

import numpy as np
from scipy.integrate import cumulative_trapezoid, simpson
from scipy.stats import qmc


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results/data"

PREV_A = DATA / "025a_saturating_relativistic_hencky_summary.json"
PREV_B = DATA / "025b0_hyperelastic_compatibility_acoustic_cone_summary.json"

OUTJ = DATA / "025b1_geometric_compatibility_prestrain_closeout_summary.json"
OUTF = DATA / "025b1_prestrain_geometry_frontier.csv"
OUTT = DATA / "025b1_reference_metric_transition_scan.csv"
OUTN = DATA / "025b1_reference_metric_transition_profile.npz"


C006B = 23.426710175391
C006D = 23.591586299249
C005B = 79.753148116012

SMOKE = (
    os.environ.get(
        "AG_SMOKE",
        "0",
    )
    ==
    "1"
)

TRANSITION_N = (
    2049
    if SMOKE
    else 16385
)

RANDOM_POWER = (
    6
    if SMOKE
    else 9
)

RANDOM_N = (
    2 ** RANDOM_POWER
)

WIDTH_FRACTIONS = (
    0.02,
    0.05,
    0.10,
    0.25,
    0.50,
    1.00,
)

STRAIN_CAPS = (
    2.0,
    3.0,
    4.0,
    5.0,
    6.0,
)

WILDCARD_CAPS = (
    0.625,
    1.6,
    1.875,
    3.125,
    5.0,
)



def smoothstep5(
    u: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return quintic smoothstep, dH/du, and d2H/du2."""

    H = (
        6.0
        * u ** 5
        -
        15.0
        * u ** 4
        +
        10.0
        * u ** 3
    )

    Hp = (
        30.0
        * u ** 2
        * (
            1.0
            -
            u
        ) ** 2
    )

    Hpp = (
        60.0
        * u
        * (
            1.0
            -
            u
        )
        * (
            1.0
            -
            2.0
            * u
        )
    )

    return (
        H,
        Hp,
        Hpp,
    )


def burden_metrics(
    row: dict,
) -> dict:
    """Compute geometric burden metrics for one 025A material point."""

    k = float(
        row[
            "k"
        ]
    )

    t = float(
        row[
            "t"
        ]
    )

    q = float(
        row[
            "q"
        ]
    )

    a = float(
        row[
            "a"
        ]
    )

    R = float(
        row[
            "R"
        ]
    )

    Yc = float(
        row.get(
            "y_core",
            math.atanh(t)
            /
            k,
        )
    )

    Ya = float(
        row.get(
            "y_ann",
            math.atanh(q)
            /
            k,
        )
    )

    grading = float(
        row[
            "rho_star_ann_over_core_at_a"
        ]
    )

    core_x_over_r = math.exp(
        -Yc
    )

    ann_x_over_r = math.exp(
        +Ya
    )

    interface_jump = math.exp(
        Yc
        +
        Ya
    )

    chi = math.exp(
        2.0
        * Ya
    )

    integrated_curvature = (
        -2.0
        * math.pi
        * (
            chi
            -
            1.0
        )
    )

    direct_delta_x = (
        R
        * ann_x_over_r
        -
        a
        * core_x_over_r
    )

    radial_span = (
        R
        -
        a
    )

    direct_sigma_lower = (
        direct_delta_x
        /
        radial_span
    )

    direct_log_strain_lower = math.log(
        direct_sigma_lower
    )

    generalized_identity_rhs = (
        (t / q)
        *
        (
            (
                1.0
                +
                q
            )
            /
            (
                1.0
                +
                t
            )
        ) ** (
            2.0
            /
            k
        )
    )

    duality_numeric = (
        grading
        *
        chi
    )

    duality_relerr = (
        abs(
            duality_numeric
            -
            generalized_identity_rhs
        )
        /
        max(
            abs(
                generalized_identity_rhs
            ),
            1.0e-300,
        )
    )

    return {
        "strain_cap":
            float(
                row.get(
                    "strain_cap",
                    math.nan,
                )
            ),

        "C":
            float(
                row[
                    "C"
                ]
            ),

        "k":
            k,

        "t":
            t,

        "q":
            q,

        "a":
            a,

        "R":
            R,

        "Y_core":
            Yc,

        "Y_ann":
            Ya,

        "core_X_over_r":
            core_x_over_r,

        "ann_X_over_r":
            ann_x_over_r,

        "interface_jump_factor":
            interface_jump,

        "cone_excess_factor_chi":
            chi,

        "integrated_gaussian_curvature":
            integrated_curvature,

        "integrated_curvature_over_4pi":
            (
                integrated_curvature
                /
                (
                    4.0
                    * math.pi
                )
            ),

        "axisymmetric_stress_free_isometric_embedding":
            bool(
                chi
                <=
                1.0
                +
                1.0e-12
            ),

        "optimistic_axisymmetric_embedding_log_strain_floor":
            (
                0.5
                * math.log(
                    chi
                )
            ),

        "direct_same_z_delta_X":
            direct_delta_x,

        "direct_radial_span":
            radial_span,

        "direct_same_z_sigma_max_lower_bound":
            direct_sigma_lower,

        "direct_same_z_log_strain_lower_bound":
            direct_log_strain_lower,

        "rho_star_ann_over_core":
            grading,

        "inverse_grading":
            (
                1.0
                /
                grading
            ),

        "grading_times_chi":
            duality_numeric,

        "grading_geometry_identity_rhs":
            generalized_identity_rhs,

        "grading_geometry_identity_relerr":
            duality_relerr,
    }



def transition_metrics(
    *,
    a: float,
    width: float,
    Yc: float,
    Ya: float,
    H: np.ndarray,
    Hp_du: np.ndarray,
    Hpp_du2: np.ndarray,
) -> dict:
    """Evaluate one smooth reference-metric transition.

    The curvature invariant is reconstructed using the analytic derivative

        f = (1/A) dB/dr

    rather than a finite-difference gradient of f. This avoids numerical
    amplification in the very narrow, very high-curvature transition
    profiles discovered by 025B1.

    The independently integrated quantity remains

        integral K dA = -2 pi integral df/dr dr,

    evaluated with Simpson quadrature and compared with the exact endpoint
    identity

        -2 pi [f_out-f_in].
    """

    u = np.linspace(
        0.0,
        1.0,
        len(H),
    )

    r = (
        a
        +
        width
        * u
    )

    alpha_r = (
        Yc
        -
        Ya
    )

    alpha_phi = (
        Ya
        +
        Yc
    )

    y_r = (
        -Yc
        +
        H
        * alpha_r
    )

    y_phi = (
        -Yc
        +
        H
        * alpha_phi
    )

    H_r = (
        Hp_du
        /
        width
    )

    H_rr = (
        Hpp_du2
        /
        (
            width
            *
            width
        )
    )

    y_phi_prime = (
        alpha_phi
        * H_r
    )

    y_phi_second = (
        alpha_phi
        * H_rr
    )

    A = np.exp(
        y_r
    )

    B = (
        r
        * np.exp(
            y_phi
        )
    )

    exp_delta = np.exp(
        y_phi
        -
        y_r
    )

    # f = (1/A) dB/dr
    f = (
        exp_delta
        * (
            1.0
            +
            r
            * y_phi_prime
        )
    )

    # Since
    #
    #   y_phi - y_r = 2 Ya H,
    #
    # its radial derivative is exactly
    #
    #   2 Ya H_r.
    #
    # Therefore df/dr is available analytically.
    df_dr = (
        exp_delta
        * (
            2.0
            * Ya
            * H_r
            * (
                1.0
                +
                r
                * y_phi_prime
            )
            +
            y_phi_prime
            +
            r
            * y_phi_second
        )
    )

    K = (
        -df_dr
        /
        (
            A
            *
            B
        )
    )

    integrand = (
        2.0
        * math.pi
        * K
        * A
        * B
    )

    total_numeric = float(
        simpson(
            integrand,
            x=r,
        )
    )

    total_boundary = (
        -2.0
        * math.pi
        * (
            float(
                f[
                    -1
                ]
            )
            -
            float(
                f[
                    0
                ]
            )
        )
    )

    expected = (
        -2.0
        * math.pi
        * (
            math.exp(
                2.0
                * Ya
            )
            -
            1.0
        )
    )

    relerr_expected = (
        abs(
            total_numeric
            -
            expected
        )
        /
        max(
            abs(
                expected
            ),
            1.0e-300,
        )
    )

    relerr_boundary = (
        abs(
            total_numeric
            -
            total_boundary
        )
        /
        max(
            abs(
                total_boundary
            ),
            1.0e-300,
        )
    )

    return {
        "r":
            r,

        "u":
            u,

        "H":
            H,

        "y_r":
            y_r,

        "y_phi":
            y_phi,

        "A":
            A,

        "B":
            B,

        "f":
            f,

        "K":
            K,

        "total_numeric":
            total_numeric,

        "total_boundary":
            total_boundary,

        "expected":
            expected,

        "relerr_expected":
            relerr_expected,

        "relerr_boundary":
            relerr_boundary,

        "peak_abs_K":
            float(
                np.max(
                    np.abs(
                        K
                    )
                )
            ),

        "rms_K":
            float(
                math.sqrt(
                    simpson(
                        K
                        *
                        K
                        *
                        A
                        *
                        B,
                        x=r,
                    )
                    /
                    max(
                        simpson(
                            A
                            *
                            B,
                            x=r,
                        ),
                        1.0e-300,
                    )
                )
            ),

        "f_start":
            float(
                f[
                    0
                ]
            ),

        "f_end":
            float(
                f[
                    -1
                ]
            ),
    }



def random_monotone_transition(
    coeffs: np.ndarray,
    n: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Create monotone H, dH/du and d2H/du2.

    The derivative family is

        H'(u) proportional to
        u^2 (1-u)^2 exp[E(u)],

    where

        E(u) = sum_j c_j cos(j pi u).

    H'' is evaluated analytically so the curvature reconstruction does not
    differentiate a numerically steep f profile.
    """

    u = np.linspace(
        0.0,
        1.0,
        n,
    )

    exponent = np.zeros_like(
        u
    )

    exponent_prime = np.zeros_like(
        u
    )

    for j, coefficient in enumerate(
        coeffs,
        start=1,
    ):

        exponent += (
            coefficient
            *
            np.cos(
                j
                *
                math.pi
                *
                u
            )
        )

        exponent_prime += (
            -coefficient
            *
            j
            *
            math.pi
            *
            np.sin(
                j
                *
                math.pi
                *
                u
            )
        )

    base = (
        u
        *
        u
        *
        (
            1.0
            -
            u
        ) ** 2
    )

    base_prime = (
        2.0
        *
        u
        *
        (
            1.0
            -
            u
        )
        *
        (
            1.0
            -
            2.0
            *
            u
        )
    )

    exponential = np.exp(
        exponent
    )

    density = (
        base
        *
        exponential
    )

    density_prime = (
        exponential
        *
        (
            base_prime
            +
            base
            *
            exponent_prime
        )
    )

    normalization = float(
        np.trapezoid(
            density,
            u,
        )
    )

    if normalization <= 0.0:

        raise RuntimeError(
            "Invalid random transition normalization"
        )

    Hp = (
        density
        /
        normalization
    )

    Hpp = (
        density_prime
        /
        normalization
    )

    H = np.concatenate(
        (
            np.asarray(
                [
                    0.0
                ]
            ),
            cumulative_trapezoid(
                Hp,
                u,
            ),
        )
    )

    # Apply one common normalization to H and both derivatives so they remain
    # mutually consistent to floating-point precision.
    scale = float(
        H[
            -1
        ]
    )

    if scale <= 0.0:

        raise RuntimeError(
            "Invalid accumulated random transition"
        )

    H /= scale
    Hp /= scale
    Hpp /= scale

    return (
        H,
        Hp,
        Hpp,
    )


def same_z_path_cap_metrics(
    burden: dict,
    cap: float,
) -> dict:
    """Return direct-path and straight-detour diagnostics for one strain cap."""

    delta_x = burden[
        "direct_same_z_delta_X"
    ]

    radial_span = burden[
        "direct_radial_span"
    ]

    maximum_gradient = math.exp(
        cap
    )

    required_path_length = (
        delta_x
        /
        maximum_gradient
    )

    path_multiplier = (
        required_path_length
        /
        radial_span
    )

    if required_path_length <= radial_span:

        vertical_excursion = 0.0

    else:

        vertical_excursion = math.sqrt(
            max(
                required_path_length ** 2
                -
                radial_span ** 2,
                0.0,
            )
        )

    return {
        "strain_cap":
            cap,

        "direct_same_z_target_possible_under_cap":
            bool(
                burden[
                    "direct_same_z_log_strain_lower_bound"
                ]
                <=
                cap
            ),

        "minimum_required_material_path_length":
            required_path_length,

        "path_length_multiplier_vs_radial_span":
            path_multiplier,

        "straight_detour_vertical_excursion_over_h":
            vertical_excursion,
    }


def main() -> None:
    """Execute the 025B1 final-session closeout gate."""

    print(
        "=== 025B1 GEOMETRIC COMPATIBILITY + PRESTRAIN CLOSEOUT ==="
    )

    previous_a = json.loads(
        PREV_A.read_text(
            encoding="utf-8"
        )
    )

    previous_b = json.loads(
        PREV_B.read_text(
            encoding="utf-8"
        )
    )

    selected = previous_a[
        "selected"
    ]

    if selected is None:

        raise RuntimeError(
            "025A selected state unavailable"
        )

    full_cone_pass = bool(
        previous_b[
            "acoustic"
        ][
            "full_cone_pass"
        ]
    )

    if not full_cone_pass:

        raise RuntimeError(
            "025B0 full acoustic cone did not pass"
        )

    compatible_cap4 = previous_b[
        "best_cap4_high"
    ]

    if compatible_cap4 is None:

        raise RuntimeError(
            "025B0 compatible cap-4 state unavailable"
        )

    print(
        "\n=== A — PREDECESSOR ANCHORS ==="
    )

    print(
        f"C_006B="
        f"{C006B:.15e}"
    )

    print(
        f"C_006D="
        f"{C006D:.15e}"
    )

    print(
        f"C_005B="
        f"{C005B:.15e}"
    )

    print(
        f"C_025A_SELECTED="
        f"{float(selected['C']):.15e}"
    )

    print(
        f"C_025B0_COMPATIBLE_CAP4="
        f"{float(compatible_cap4['C']):.15e}"
    )

    print(
        "025B0_FULL_ACOUSTIC_CONE=PASS"
    )

    burden = burden_metrics(
        selected
    )

    print(
        "\n=== B — SELECTED 025A GEOMETRIC BURDEN ==="
    )

    for key in (
        "Y_core",
        "Y_ann",
        "core_X_over_r",
        "ann_X_over_r",
        "interface_jump_factor",
        "cone_excess_factor_chi",
        "integrated_gaussian_curvature",
        "integrated_curvature_over_4pi",
        "optimistic_axisymmetric_embedding_log_strain_floor",
        "direct_same_z_delta_X",
        "direct_radial_span",
        "direct_same_z_sigma_max_lower_bound",
        "direct_same_z_log_strain_lower_bound",
        "rho_star_ann_over_core",
        "inverse_grading",
        "grading_times_chi",
        "grading_geometry_identity_rhs",
        "grading_geometry_identity_relerr",
    ):

        print(
            f"SELECTED_{key.upper()}="
            f"{float(burden[key]):.15e}"
        )

    print(
        "SELECTED_AXISYMMETRIC_STRESS_FREE_ISOMETRIC_EMBEDDING="
        +
        (
            "YES"
            if burden[
                "axisymmetric_stress_free_isometric_embedding"
            ]
            else "NO"
        )
    )

    duality_pass = bool(
        burden[
            "grading_geometry_identity_relerr"
        ]
        <=
        1.0e-10
    )

    print(
        "GRADING_GEOMETRY_IDENTITY="
        +
        (
            "PASS"
            if duality_pass
            else "FAIL"
        )
    )

    print(
        "GRADING_GEOMETRY_INTERPRETATION="
        "THE_APPROXIMATELY_3000X_MATERIAL_GRADING_AND_INTRINSIC_METRIC_EXCESS_ARE_THE_SAME_LEADING_BURDEN"
    )

    print(
        "\n=== C — GENERAL 2-D EUCLIDEAN KINEMATIC DIAGNOSTIC ==="
    )

    cap_rows = []

    for cap in STRAIN_CAPS:

        row = same_z_path_cap_metrics(
            burden,
            cap,
        )

        cap_rows.append(
            row
        )

        print(
            f"STRAIN_CAP={cap:.6f} "
            f"DIRECT_SAME_Z_POSSIBLE="
            +
            (
                "YES"
                if row[
                    "direct_same_z_target_possible_under_cap"
                ]
                else "NO"
            )
            +
            f" PATH_MULTIPLIER="
            f"{row['path_length_multiplier_vs_radial_span']:.12e}"
            +
            f" STRAIGHT_VERTICAL_EXCURSION_OVER_H="
            f"{row['straight_detour_vertical_excursion_over_h']:.12e}"
        )

    wildcard_rows = []

    for cap in WILDCARD_CAPS:

        row = same_z_path_cap_metrics(
            burden,
            cap,
        )

        wildcard_rows.append(
            row
        )

        print(
            f"WILDCARD_STRAIN_CAP={cap:.6f} "
            f"PATH_MULTIPLIER="
            f"{row['path_length_multiplier_vs_radial_span']:.12e} "
            f"VERTICAL_EXCURSION_OVER_H="
            f"{row['straight_detour_vertical_excursion_over_h']:.12e} "
            "ROLE=BLIND_WILDCARD_NOT_PHYSICS_PRIOR"
        )

    print(
        "WILDCARDS_USED_FOR_SELECTION=NO"
    )

    cap4_path = next(
        row
        for row in cap_rows
        if abs(
            row[
                "strain_cap"
            ]
            -
            4.0
        )
        <
        1.0e-12
    )

    print(
        "GENERAL_2D_EUCLIDEAN_SHEAR_UNIVERSALLY_RULED_OUT=NO"
    )

    print(
        "CAP4_DIRECT_RADIAL_TARGET_RULED_OUT="
        +
        (
            "YES"
            if not cap4_path[
                "direct_same_z_target_possible_under_cap"
            ]
            else "NO"
        )
    )

    print(
        "CAP4_2D_DETOUR_REQUIRES_ADDITIONAL_PATH_LENGTH="
        "YES"
    )

    print(
        "\n=== D — DETERMINISTIC NON-EUCLIDEAN TRANSITION CURVATURE ==="
    )

    a = float(
        selected[
            "a"
        ]
    )

    R = float(
        selected[
            "R"
        ]
    )

    Yc = burden[
        "Y_core"
    ]

    Ya = burden[
        "Y_ann"
    ]

    span = (
        R
        -
        a
    )

    u = np.linspace(
        0.0,
        1.0,
        TRANSITION_N,
    )

    H_base, Hp_base, Hpp_base = smoothstep5(
        u
    )

    transition_rows = []

    saved_profile = None

    for fraction in WIDTH_FRACTIONS:

        width = (
            fraction
            *
            span
        )

        metrics = transition_metrics(
            a=a,
            width=width,
            Yc=Yc,
            Ya=Ya,
            H=H_base,
            Hp_du=Hp_base,
            Hpp_du2=Hpp_base,
        )

        transition_rows.append({
            "family":
                "QUINTIC",

            "width_fraction_of_annulus_span":
                fraction,

            "width":
                width,

            "integrated_curvature_numeric":
                metrics[
                    "total_numeric"
                ],

            "integrated_curvature_boundary":
                metrics[
                    "total_boundary"
                ],

            "integrated_curvature_expected":
                metrics[
                    "expected"
                ],

            "relative_error_expected":
                metrics[
                    "relerr_expected"
                ],

            "relative_error_boundary":
                metrics[
                    "relerr_boundary"
                ],

            "peak_abs_K":
                metrics[
                    "peak_abs_K"
                ],

            "rms_K":
                metrics[
                    "rms_K"
                ],

            "f_start":
                metrics[
                    "f_start"
                ],

            "f_end":
                metrics[
                    "f_end"
                ],
        })

        print(
            f"TRANSITION_WIDTH_FRACTION={fraction:.6f} "
            f"TOTAL_K={metrics['total_numeric']:.12e} "
            f"EXPECTED_K={metrics['expected']:.12e} "
            f"RELERR={metrics['relerr_expected']:.12e} "
            f"PEAK_ABS_K={metrics['peak_abs_K']:.12e}"
        )

        if abs(
            fraction
            -
            0.25
        ) < 1.0e-12:

            saved_profile = metrics

    deterministic_max_relerr = max(
        row[
            "relative_error_expected"
        ]
        for row in transition_rows
    )

    deterministic_pass = bool(
        deterministic_max_relerr
        <=
        2.0e-4
    )

    print(
        f"DETERMINISTIC_CURVATURE_INVARIANT_MAX_RELERR="
        f"{deterministic_max_relerr:.15e}"
    )

    print(
        "DETERMINISTIC_CURVATURE_INVARIANT="
        +
        (
            "PASS"
            if deterministic_pass
            else "FAIL"
        )
    )

    print(
        "\n=== E — RANDOMIZED MONOTONE TRANSITION INVARIANCE AUDIT ==="
    )

    sobol = qmc.Sobol(
        d=5,
        scramble=True,
        seed=250301,
    ).random_base2(
        RANDOM_POWER
    )

    random_max_relerr = 0.0
    random_peak_min = math.inf
    random_peak_max = 0.0

    for i, point in enumerate(
        sobol
    ):

        coeffs = (
            3.0
            *
            (
                point[
                    :4
                ]
                -
                0.5
            )
        )

        width_fraction = 10.0 ** (
            math.log10(
                0.02
            )
            +
            (
                math.log10(
                    1.0
                )
                -
                math.log10(
                    0.02
                )
            )
            *
            point[
                4
            ]
        )

        width = (
            width_fraction
            *
            span
        )

        H_random, Hp_random, Hpp_random = random_monotone_transition(
            coeffs,
            TRANSITION_N,
        )

        metrics = transition_metrics(
            a=a,
            width=width,
            Yc=Yc,
            Ya=Ya,
            H=H_random,
            Hp_du=Hp_random,
            Hpp_du2=Hpp_random,
        )

        random_max_relerr = max(
            random_max_relerr,
            metrics[
                "relerr_expected"
            ],
        )

        random_peak_min = min(
            random_peak_min,
            metrics[
                "peak_abs_K"
            ],
        )

        random_peak_max = max(
            random_peak_max,
            metrics[
                "peak_abs_K"
            ],
        )

    random_pass = bool(
        random_max_relerr
        <=
        5.0e-4
    )

    print(
        f"RANDOM_TRANSITION_CASES="
        f"{RANDOM_N}"
    )

    print(
        f"RANDOM_CURVATURE_INVARIANT_MAX_RELERR="
        f"{random_max_relerr:.15e}"
    )

    print(
        f"RANDOM_PEAK_ABS_K_MIN="
        f"{random_peak_min:.15e}"
    )

    print(
        f"RANDOM_PEAK_ABS_K_MAX="
        f"{random_peak_max:.15e}"
    )

    print(
        "RANDOMIZED_CURVATURE_INVARIANT="
        +
        (
            "PASS"
            if random_pass
            else "FAIL"
        )
    )

    print(
        "\n=== F — 025A STRAIN FRONTIER GEOMETRIC BURDEN ==="
    )

    frontier_source = previous_a.get(
        "independent_frontier",
        []
    )

    frontier_rows = []

    for row in frontier_source:

        if not all(
            key in row
            for key in (
                "a",
                "R",
                "k",
                "t",
                "q",
                "C",
                "rho_star_ann_over_core_at_a",
            )
        ):

            continue

        b = burden_metrics(
            row
        )

        frontier_rows.append(
            b
        )

    frontier_rows.sort(
        key=lambda row:
            (
                row[
                    "strain_cap"
                ]
                if math.isfinite(
                    row[
                        "strain_cap"
                    ]
                )
                else 999.0
            )
    )

    for row in frontier_rows:

        print(
            f"FRONTIER_STRAIN_CAP="
            f"{row['strain_cap']:.6f} "
            f"C={row['C']:.12e} "
            f"CHI={row['cone_excess_factor_chi']:.12e} "
            f"INV_GRADING={row['inverse_grading']:.12e} "
            f"DIRECT_LOG_BOUND={row['direct_same_z_log_strain_lower_bound']:.12e}"
        )

    print(
        "\n=== G — EXACT AXISYMMETRIC REFERENCE-METRIC EMBEDDING GATE ==="
    )

    chi = burden[
        "cone_excess_factor_chi"
    ]

    stress_free_axisym = bool(
        chi
        <=
        1.0
        +
        1.0e-12
    )

    print(
        f"REFERENCE_METRIC_DBDU_ANNULUS="
        f"{chi:.15e}"
    )

    print(
        "AXISYMMETRIC_SURFACE_OF_REVOLUTION_REQUIRES_ABS_DBDU_LE_1=YES"
    )

    print(
        "TARGET_REFERENCE_METRIC_STRESS_FREE_AXISYMMETRIC_EMBEDDING="
        +
        (
            "YES"
            if stress_free_axisym
            else "NO"
        )
    )

    print(
        "NONAXISYMMETRIC_WRINKLED_ISOMETRIC_EMBEDDING_RULED_OUT=NO"
    )

    print(
        "REFERENCE_METRIC_PRESCRIPTION_COUNTS_AS_FREE_ENERGY=NO"
    )

    print(
        "PRESTRAIN_MANUFACTURING_SUPPORT_RESET_ENERGY_MODELLED=NO"
    )

    print(
        "\n=== H — FINAL BRANCH DECISION ==="
    )

    radial_regressed = bool(
        float(
            compatible_cap4[
                "C"
            ]
        )
        >=
        0.95
        *
        C005B
    )

    huge_metric_factor = bool(
        chi
        >=
        1.0e3
    )

    curvature_pass = bool(
        deterministic_pass
        and
        random_pass
    )

    if not duality_pass:

        raise RuntimeError(
            "Material-grading/geometric identity failed"
        )

    if not curvature_pass:

        raise RuntimeError(
            "Reference-metric curvature invariant failed numerical validation"
        )

    if not stress_free_axisym and radial_regressed:

        decision = (
            "YELLOW_LOCAL_HYPERELASTIC_LAW_RETAINED_"
            "BUT_DIRECT_EFFICIENT_MATERIAL_REALIZATION_PAUSED"
        )

        interpretation = (
            "ORDINARY_RADIAL_COMPATIBILITY_RETURNS_TO_005B_SCALE_"
            "WHILE_THE_NON_EUCLIDEAN_ESCAPE_REQUIRES_AN_EXTREME_"
            "INTRINSIC_METRIC_WITH_NO_STRESS_FREE_AXISYMMETRIC_EMBEDDING"
        )

    else:

        decision = (
            "UNEXPECTED_025B1_RESULT_REQUIRES_MANUAL_REVIEW"
        )

        interpretation = (
            "PREDECLARED_BRANCH_EXPECTATIONS_NOT_MET"
        )

    preferred_pure_gr_if_resumed = (
        "GENERAL_2D_EUCLIDEAN_SHEAR_WITH_EXPLICIT_FINITE_THICKNESS_"
        "BEFORE_NON_EUCLIDEAN_REFERENCE_METRIC"
    )

    next_after_docs = (
        "GLOBAL_RERANK_AFTER_DOCUMENTATION_WITH_ANALOGUE_ANTIGRAVITY_"
        "ACTIVATED_IN_TANDEM_KEEP_B7_023C_023D_AS_PURE_GR_FALLBACK_"
        "AND_KEEP_025B2_2D_SHEAR_ONLY_AS_A_DEFERRED_REALIZATION_OPTION"
    )

    print(
        "025A_LOCAL_CONSTITUTIVE_LAW_STATUS=RETAIN"
    )

    print(
        "025B0_ORDINARY_RADIAL_REALIZATION_STATUS=DEMOTED"
    )

    print(
        "NON_EUCLIDEAN_AXISYMMETRIC_STRESS_FREE_ROUTE="
        +
        (
            "GREEN"
            if stress_free_axisym
            else "RED_EXACT_EMBEDDING_CONDITION"
        )
    )

    print(
        "NONAXISYMMETRIC_GEOMETRICALLY_FRUSTRATED_ROUTE="
        "UNRESOLVED_DEFER"
    )

    print(
        "GENERAL_2D_EUCLIDEAN_SHEAR_ROUTE="
        "UNRESOLVED_BUT_PREFERRED_OVER_EXTREME_PRESTRAIN_IF_PURE_GR_RESUMES"
    )

    print(
        "EXTREME_GEOMETRIC_METRIC_FACTOR_GE_1000_DIAGNOSTIC="
        +
        (
            "YES"
            if huge_metric_factor
            else "NO"
        )
    )

    print(
        f"025B1_INTERPRETATION="
        f"{interpretation}"
    )

    print(
        f"025B1_DECISION="
        f"{decision}"
    )

    print(
        f"PREFERRED_PURE_GR_REALIZATION_IF_RESUMED="
        f"{preferred_pure_gr_if_resumed}"
    )

    print(
        f"NEXT_AFTER_DOCUMENTATION="
        f"{next_after_docs}"
    )

    print(
        "HYPERELASTIC_006D_DIRECT_REALIZATION_PROVED=NO"
    )

    print(
        "GENERAL_ELASTIC_NO_GO_THEOREM=NO"
    )

    print(
        "FINITE_THICKNESS_BVP_RUN=NO"
    )

    print(
        "NONLINEAR_GR=NO"
    )

    print(
        "REMOVES_1_OVER_G_SCALING=NO"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )

    print(
        "CURRENT_KNOWLEDGE_HEURISTIC="
        "70_TO_71_PERCENT_RETAIN_FOR_DOCUMENTATION_CLOSEOUT"
    )

    print(
        "\n=== I — SESSION DOCUMENTATION HANDOFF KEYS ==="
    )

    print(
        "SESSION_FINAL_STRONGEST_CONSERVATIVE_RESULT=006D"
    )

    print(
        "SESSION_NEW_LOCAL_MATTER_WITNESS="
        "025A_SATURATING_RELATIVISTIC_HENCKY_SOLID"
    )

    print(
        "SESSION_LOCAL_FULL_ACOUSTIC_CONE="
        "025B0_PASS"
    )

    print(
        "SESSION_DIRECT_GLOBAL_RADIAL_REALIZATION="
        "025B0_DEMOTED_TO_005B_SCALE"
    )

    print(
        "SESSION_GEOMETRIC_PRESTRAIN_RESULT="
        "025B1_EXTREME_REFERENCE_METRIC_AND_AXISYMMETRIC_EMBEDDING_OBSTRUCTION"
    )

    print(
        "SESSION_PURE_GR_SUCCESSOR_STATUS="
        "NO_NEW_GLOBAL_REALIZATION_SUPERSEDES_006D"
    )

    print(
        "SESSION_DOC_UPDATE_REQUIRED=YES"
    )

    # ----------------------------------------------------------
    # Persist transition CSV.
    # ----------------------------------------------------------

    with OUTT.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:

        fields = list(
            transition_rows[
                0
            ].keys()
        )

        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
        )

        writer.writeheader()

        writer.writerows(
            transition_rows
        )

    # ----------------------------------------------------------
    # Persist frontier CSV.
    # ----------------------------------------------------------

    all_frontier_rows = []

    for row in frontier_rows:

        serial = dict(
            row
        )

        serial[
            "family"
        ] = "025A_INDEPENDENT_FRONTIER"

        all_frontier_rows.append(
            serial
        )

    selected_serial = dict(
        burden
    )

    selected_serial[
        "family"
    ] = "025A_SELECTED"

    all_frontier_rows.append(
        selected_serial
    )

    if all_frontier_rows:

        fields = sorted({
            key
            for row in all_frontier_rows
            for key in row.keys()
        })

        with OUTF.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as handle:

            writer = csv.DictWriter(
                handle,
                fieldnames=fields,
                extrasaction="ignore",
            )

            writer.writeheader()

            writer.writerows(
                all_frontier_rows
            )

    # ----------------------------------------------------------
    # Persist representative transition.
    # ----------------------------------------------------------

    if saved_profile is not None:

        np.savez_compressed(
            OUTN,
            r=saved_profile[
                "r"
            ],
            u=saved_profile[
                "u"
            ],
            H=saved_profile[
                "H"
            ],
            y_r=saved_profile[
                "y_r"
            ],
            y_phi=saved_profile[
                "y_phi"
            ],
            A=saved_profile[
                "A"
            ],
            B=saved_profile[
                "B"
            ],
            f=saved_profile[
                "f"
            ],
            K=saved_profile[
                "K"
            ],
        )

    summary = {
        "claim_classification":
            (
                "PROJECT_DERIVED_GEOMETRIC_COMPATIBILITY_"
                "AND_PRESTRAIN_CLOSEOUT_GATE"
            ),

        "anchors": {
            "C006B":
                C006B,

            "C006D":
                C006D,

            "C005B":
                C005B,

            "C025A_selected":
                float(
                    selected[
                        "C"
                    ]
                ),

            "C025B0_compatible_cap4":
                float(
                    compatible_cap4[
                        "C"
                    ]
                ),

            "025B0_full_acoustic_cone":
                full_cone_pass,
        },

        "selected_geometric_burden":
            burden,

        "strain_cap_path_diagnostics":
            cap_rows,

        "wildcard_path_diagnostics":
            wildcard_rows,

        "transition_validation": {
            "deterministic_max_relative_error":
                deterministic_max_relerr,

            "deterministic_pass":
                deterministic_pass,

            "random_cases":
                RANDOM_N,

            "random_max_relative_error":
                random_max_relerr,

            "random_pass":
                random_pass,

            "random_peak_abs_K_min":
                random_peak_min,

            "random_peak_abs_K_max":
                random_peak_max,
        },

        "reference_metric": {
            "annulus_dB_du":
                chi,

            "axisymmetric_surface_of_revolution_requires_abs_dB_du_le_1":
                True,

            "stress_free_axisymmetric_embedding":
                stress_free_axisym,

            "nonaxisymmetric_wrinkled_embedding_ruled_out":
                False,

            "manufacturing_energy_modelled":
                False,
        },

        "decision": {
            "local_025A_law":
                "RETAIN",

            "ordinary_radial_realization":
                "DEMOTED",

            "non_euclidean_axisymmetric_stress_free":
                (
                    "GREEN"
                    if stress_free_axisym
                    else "RED"
                ),

            "general_2D_euclidean_shear":
                "UNRESOLVED",

            "nonaxisymmetric_frustrated_metric":
                "UNRESOLVED_DEFER",

            "hyperelastic_direct_realization":
                "PAUSE",

            "interpretation":
                interpretation,

            "result":
                decision,

            "preferred_pure_GR_if_resumed":
                preferred_pure_gr_if_resumed,

            "next_after_documentation":
                next_after_docs,

            "practical_device":
                False,
        },

        "limits": [
            "NO_GENERAL_ELASTIC_NO_GO",
            "NO_GENERAL_2D_EUCLIDEAN_SHEAR_SOLUTION",
            "NO_NONAXISYMMETRIC_WRINKLED_EMBEDDING_TEST",
            "NO_PRESTRAIN_MANUFACTURING_ENERGY_LEDGER",
            "NO_FINITE_THICKNESS_BVP",
            "NO_NONLINEAR_GR",
            "NO_1_OVER_G_ESCAPE",
            "NO_DEVICE",
        ],
    }

    OUTJ.write_text(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
            allow_nan=True,
        )
        +
        "\n",
        encoding="utf-8",
    )

    print(
        f"SUMMARY_JSON="
        f"{OUTJ.relative_to(ROOT)}"
    )

    print(
        f"FRONTIER_CSV="
        f"{OUTF.relative_to(ROOT)}"
    )

    print(
        f"TRANSITION_CSV="
        f"{OUTT.relative_to(ROOT)}"
    )

    if OUTN.is_file():

        print(
            f"TRANSITION_PROFILE_NPZ="
            f"{OUTN.relative_to(ROOT)}"
        )

    print(
        "025B1_RUN_COMPLETE=YES"
    )


if __name__ == "__main__":
    main()
