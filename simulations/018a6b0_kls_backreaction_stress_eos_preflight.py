#!/usr/bin/env python3
"""Simulation 018A-6B0 — KLS junction backreaction/stress/EOS preflight.

PURPOSE
-------
Interrogate the successful 018A-6A fixed-background two-dimensional KLS
wall/string junction before paying the substantially larger numerical cost of
a fully coupled Phi/A/sigma/gauge relaxation.

018A-6A established, at fixed reconstructed 017P background:

    - a true complex two-dimensional A-field solution;
    - one-sided wall termination on the 017P vortex;
    - finite junction excess energy;
    - domain convergence of that excess;
    - resolution convergence;
    - far-wall tension reconstruction;
    - gauge-invariant relative-phase locking;
    - exact lattice gauge-covariance check.

The remaining microscopic question is no longer whether the wall can end on
the string.

It is whether the new sector perturbs the already successful 017P string EOS
and support/gravity bookkeeping weakly enough that a fully coupled nonlinear
junction solve has high expected value.

SCIENTIFIC QUESTION
-------------------
Given the converged fixed-background 2D junction, how large are:

    1. the new Euler-Lagrange source acting on Phi;
    2. the new gauge-current source;
    3. the chi dependence of the localized junction line energy;
    4. the resulting fixed-background modification of c_T and c_L;
    5. the modification of the published thin-string extrinsic stability gate;
    6. the localized junction contribution to active gravitational line source;
    7. the mandatory stationarity correction from junction line energy?

This is a CHEAP DECISIVE BACKREACTION PREFLIGHT.

It is not a substitute for the fully coupled 2D junction.

MODEL
-----
The 018A-6A field theory is reused without alteration.

The added same-gauge potential is

    V_ext
      =
      lambda_A/4 (|A|^2-F^2)^2

      - h [
          Phi^* A^2
          +
          Phi (A^*)^2
        ]

      + c_Phi (|Phi|^2-v^2)

      + c_A (|A|^2-F^2)

      + C.

The added Phi Euler-Lagrange source is

    R_Phi^(A)
      =
      -h A^2
      +
      c_Phi Phi.

Because

    c_Phi = h F^2 / v,

this vanishes exactly in the locked asymptotic vacuum.

Therefore a successful 018A-6A solution should generate a LOCALIZED Phi
backreaction source rather than an infrared forcing term.

SIGMA BACKREACTION
------------------
The new A sector has no direct coupling to the superconducting sigma field.

Therefore

    R_sigma^(A),direct = 0.

Sigma can still change indirectly after Phi and the gauge field relax.

That effect belongs to the fully coupled solve.

GAUGE BACKREACTION
------------------
The charge-1 field contributes an additional gauge current.

On the gauge-covariant lattice used in 018A-6A, for one x link,

    E_A,link
      =
      |A_q - U A_p|^2.

Differentiation with respect to the fundamental link angle gives a source
proportional to

    J_A
      =
      2 Im[A_q^* U A_p].

For the charge-2 Phi field the corresponding source is

    J_Phi
      =
      4 Im[Phi_q^* U^2 Phi_p].

The L2 norm ratio

    ||J_A|| / ||J_Phi||

is used only as a BACKREACTION-SIZE DIAGNOSTIC.

It is not itself a proof that the gauge field may remain frozen.

FIXED-BACKGROUND ACTIVE SOURCE
------------------------------
For a static canonical scalar sector depending only on the two transverse
coordinates x,z, the gradient terms cancel from

    S
      =
      epsilon
      +
      p_x
      +
      p_y
      +
      p_z.

Thus the added fixed-background scalar-sector active density is

    S_ext
      =
      -2 V_ext.

The one-sided asymptotic wall contributes

    S_wall / length
      =
      -sigma_W.

After integrating the whole 2D box, define the localized junction active
excess by

    Lambda_J,active
      =
      integral S_ext d^2x
      +
      sigma_W L.

If the wall-subtracted endpoint behaves like an isolated static string-like
defect, transverse Laue balance predicts a small integrated active line source.

This is measured, not assumed.

CHI DEPENDENCE AND EOS
----------------------
The 017P straight-string quantities obey

    dA_string/dchi
      =
      -Sigma_2.

The successful 018A-6A endpoint adds a localized line energy

    mu_J(chi).

At fixed background define

    A_eff(chi)
      =
      A_string(chi)
      +
      mu_J(chi).

The transverse speed estimate becomes

    c_T^2
      =
      1 /
      [
        1
        +
        2 chi Sigma_2/A_eff
      ].

The longitudinal characteristic estimate remains

    c_L^2
      =
      1 /
      [
        1
        +
        2 chi Sigma_2'/Sigma_2
      ]

at this fixed-background stage because A carries no longitudinal current.

The derivative

    dA_eff/dchi + Sigma_2

is explicitly measured.

A significant failure of the variational identity is evidence that frozen
background backreaction is no longer perturbative and the fully coupled solve
must not be predicted from the reduced EOS.

EXTRINSIC STABILITY
-------------------
The published thin-string cubic used in 017P is repeated for m=2,...,40.

With c_T^2 and c_L^2 define

    a0 =
      2(c_L^2-c_T^2)(m^2-1)m

    a1 =
      4 c_T^2(1-c_L^2)(m^2-1)
      -
      (1+c_T^2)(c_L^2-c_T^2)(m^2+1)

    a2 =
      2 c_T^2
      [
        c_L^2-c_T^2
        -
        2(1-c_L^2 c_T^2)
      ] m

    a3 =
      c_T^2(1+c_T^2)(1-c_L^2 c_T^2).

The discriminant and direct root-imaginary-part checks are both required.

STATIONARITY BOOKKEEPING
------------------------
The microscopic junction line energy changes the effective wall load.

For junction multiplicity n_J,

    w_eff
      =
      w_stat
      -
      2 pi n_J mu_J / ell.

Then

    Q_req
      =
      w_eff / sigma_W

    N_req
      =
      Q_req / (Q/N)

    R_req
      =
      Q_req ell / (2 pi).

Both n_J=1 and an intentionally conservative n_J=2 interpretation are
reported.

The n_J=2 case is NOT asserted to be the actual microscopic topology.
It is an adversarial bookkeeping control for the counterrotating-pair
architecture.

PRIMARY NUMERICAL RUNS
----------------------
1. High-resolution selected endpoint:

       chi = 0.00475
       N = 141
       L = 100.

2. Fixed-discretization chi continuation:

       chi =
         0.00425
         0.00450
         0.00475

       N = 81
       L = 100.

The common discretization makes numerical derivative cancellation much cleaner
than mixing resolutions.

PASS CONDITIONS
---------------
The gate is green only if:

    SELECTED_2D_OPTIMIZER=PASS

    PHI_BACKREACTION_SOURCE_PREFLIGHT=PASS

    GAUGE_BACKREACTION_SOURCE_PREFLIGHT=PASS

    FIXED_BACKGROUND_VARIATIONAL_IDENTITY=PASS

    FIXED_BACKGROUND_EOS_HEALTH=PASS

    FIXED_BACKGROUND_M2_TO_M40_STABILITY=PASS

    JUNCTION_ACTIVE_SOURCE_PREFLIGHT=PASS

    ONE_JUNCTION_STATIONARITY=PASS

    TWO_JUNCTION_ADVERSARIAL_STATIONARITY=PASS.

Thresholds are intentionally conservative.

FALSIFICATION / STOP RULE
-------------------------
If the new field creates order-one Phi/gauge forcing, destroys the straight
string variational identity, drives the selected EOS outside the stable
thin-string basin, or consumes the stationarity budget, do NOT proceed directly
to a large fully coupled solve.

Instead identify which field sector caused the failure.

If all backreaction diagnostics remain small, proceed directly to:

    018A6B_FULLY_COUPLED_2D_KLS_JUNCTION

where Phi, A, sigma, and the gauge field must all be released.

UNITS
-----
Natural units and the existing dimensionless 017P normalization.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_018A_KLS_BACKREACTION_STRESS_EOS_PREFLIGHT

LIMITATIONS
-----------
A green result does not establish:

    - fully coupled junction existence;
    - complete perturbed 017P EOS;
    - full local T_munu after background relaxation;
    - full 018A gravity closeout;
    - full finite-thickness drum field solution;
    - nonlinear Einstein-matter consistency;
    - practical energy scaling;
    - a practical antigravity device.
"""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]

SOURCE = (
    ROOT
    / "simulations"
    / "018a6a_fixed_background_2d_kls_junction.py"
)


def load_module(
    name: str,
    path: Path,
):
    """Load the already locally verified 018A-6A implementation."""

    spec = importlib.util.spec_from_file_location(
        name,
        path,
    )

    if (
        spec is None
        or spec.loader is None
    ):
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


m = load_module(
    "ag018a6a_backreaction",
    SOURCE,
)


# ============================================================================
# Declared numerical gates.
# ============================================================================

CHI_VALUES = np.array(
    [
        0.00425,
        0.00450,
        0.00475,
    ],
    dtype=float,
)

CHI_SELECTED = 0.00475

HIGH_N = 141
HIGH_L = 100.0

CHI_N = 81
CHI_L = 100.0

MAX_PHI_SOURCE = 1.0e-3
MAX_GAUGE_CURRENT_RATIO = 5.0e-2

MAX_VARIATIONAL_RELERR = 1.0e-2

MAX_ACTIVE_LINE_PERTURBATION_FRACTION = 1.0e-2

MIN_SCALE_SEPARATION = 10.0
MAX_INTEGER_MISMATCH = 1.0e-3

WALL_WIDTH90 = 78.534118560778

Q_OVER_N = 6.628230560688
ELL = 0.4257542346286
W_STAT = 12.66497926067

OMEGA_SELECTED = 2.227569443362
K_SELECTED = 2.226503003591

CT2_017P = 0.9990018050154
CL2_017P = 0.9930155006037


def integrated_extension_stress(
    result,
) -> dict[str, float]:
    """Integrate extension potential and its fixed-background active source."""

    problem = result.problem
    field = result.field

    potential = m.extension_potential(
        problem,
        field,
    )

    potential_integral = float(
        problem.dx
        *
        problem.dx
        *
        np.sum(
            problem.weights
            *
            potential
        )
    )

    total_energy = float(
        result.total_extension_energy
    )

    gradient_energy = (
        total_energy
        -
        potential_integral
    )

    active_total = (
        -2.0
        *
        potential_integral
    )

    wall_energy = (
        m.SIGMA_W_RELAXED_018A5
        *
        result.box_half
    )

    wall_active = (
        -wall_energy
    )

    junction_energy = (
        total_energy
        -
        wall_energy
    )

    junction_active = (
        active_total
        -
        wall_active
    )

    return {
        "potential_integral":
            potential_integral,

        "gradient_energy":
            gradient_energy,

        "total_energy":
            total_energy,

        "active_total":
            active_total,

        "wall_energy":
            wall_energy,

        "wall_active":
            wall_active,

        "junction_energy":
            junction_energy,

        "junction_active":
            junction_active,
    }


def phi_backreaction_source(
    result,
) -> tuple[float, float]:
    """Measure the extension source in the previously frozen Phi equation."""

    problem = result.problem
    field = result.field

    source = (
        -problem.h_lock
        *
        field
        *
        field

        +
        problem.c_phi
        *
        problem.phi
    )

    interior_source = (
        source[
            problem.interior
        ]
    )

    source_max = float(
        np.max(
            np.abs(
                interior_source
            )
        )
    )

    source_rms = float(
        np.sqrt(
            np.mean(
                np.abs(
                    interior_source
                ) ** 2
            )
        )
    )

    return (
        source_max,
        source_rms,
    )


def gauge_current_ratio(
    result,
) -> tuple[float, float, float]:
    """Compare new charge-1 link current with existing charge-2 Phi current."""

    problem = result.problem

    A = result.field
    Phi = problem.phi

    j_a_x = (
        2.0
        *
        np.imag(
            np.conj(
                A[
                    1:,
                    :,
                ]
            )
            *
            problem.ux
            *
            A[
                :-1,
                :,
            ]
        )
    )

    j_a_z = (
        2.0
        *
        np.imag(
            np.conj(
                A[
                    :,
                    1:,
                ]
            )
            *
            problem.uz
            *
            A[
                :,
                :-1,
            ]
        )
    )

    # Phi carries charge 2 with respect to the same fundamental link phase.
    j_phi_x = (
        4.0
        *
        np.imag(
            np.conj(
                Phi[
                    1:,
                    :,
                ]
            )
            *
            (
                problem.ux
                *
                problem.ux
            )
            *
            Phi[
                :-1,
                :,
            ]
        )
    )

    j_phi_z = (
        4.0
        *
        np.imag(
            np.conj(
                Phi[
                    :,
                    1:,
                ]
            )
            *
            (
                problem.uz
                *
                problem.uz
            )
            *
            Phi[
                :,
                :-1
            ]
        )
    )

    norm_a = float(
        math.sqrt(
            np.sum(
                j_a_x
                *
                j_a_x
            )
            +
            np.sum(
                j_a_z
                *
                j_a_z
            )
        )
    )

    norm_phi = float(
        math.sqrt(
            np.sum(
                j_phi_x
                *
                j_phi_x
            )
            +
            np.sum(
                j_phi_z
                *
                j_phi_z
            )
        )
    )

    ratio = (
        norm_a
        /
        max(
            norm_phi,
            1.0e-30,
        )
    )

    return (
        norm_a,
        norm_phi,
        ratio,
    )


def cubic_discriminant(
    a0: float,
    a1: float,
    a2: float,
    a3: float,
) -> float:
    """Return the discriminant of a3*x^3+a2*x^2+a1*x+a0."""

    return (
        a1
        *
        a1
        *
        a2
        *
        a2

        -
        4.0
        *
        a1
        *
        a1
        *
        a1
        *
        a3

        -
        4.0
        *
        a0
        *
        a2
        *
        a2
        *
        a2

        -
        27.0
        *
        a0
        *
        a0
        *
        a3
        *
        a3

        +
        18.0
        *
        a0
        *
        a1
        *
        a2
        *
        a3
    )


def extrinsic_stability(
    ct2: float,
    cl2: float,
) -> tuple[
    bool,
    float,
    float,
    int,
]:
    """Repeat the 017P m=2..40 discriminant and direct-root checks."""

    min_disc = math.inf
    max_imag = 0.0
    worst_m = -1

    passed = True

    for mode in range(
        2,
        41,
    ):

        m2 = float(
            mode
            *
            mode
        )

        a0 = (
            2.0
            *
            (
                cl2
                -
                ct2
            )
            *
            (
                m2
                -
                1.0
            )
            *
            mode
        )

        a1 = (
            4.0
            *
            ct2
            *
            (
                1.0
                -
                cl2
            )
            *
            (
                m2
                -
                1.0
            )

            -
            (
                1.0
                +
                ct2
            )
            *
            (
                cl2
                -
                ct2
            )
            *
            (
                m2
                +
                1.0
            )
        )

        a2 = (
            2.0
            *
            ct2
            *
            (
                cl2
                -
                ct2

                -
                2.0
                *
                (
                    1.0
                    -
                    cl2
                    *
                    ct2
                )
            )
            *
            mode
        )

        a3 = (
            ct2
            *
            (
                1.0
                +
                ct2
            )
            *
            (
                1.0
                -
                cl2
                *
                ct2
            )
        )

        disc = cubic_discriminant(
            a0,
            a1,
            a2,
            a3,
        )

        roots = np.roots(
            [
                a3,
                a2,
                a1,
                a0,
            ]
        )

        root_imag = float(
            np.max(
                np.abs(
                    np.imag(
                        roots
                    )
                )
            )
        )

        if disc < min_disc:
            min_disc = disc
            worst_m = mode

        max_imag = max(
            max_imag,
            root_imag,
        )

        if (
            disc
            <=
            0.0

            or
            root_imag
            >
            1.0e-8
        ):
            passed = False

    return (
        passed,
        min_disc,
        max_imag,
        worst_m,
    )


def stationarity_case(
    mu_junction: float,
    junction_count: int,
) -> dict[str, float | bool]:
    """Apply mandatory junction line energy to 017P wall stationarity."""

    w_eff = (
        W_STAT

        -
        2.0
        *
        math.pi
        *
        junction_count
        *
        mu_junction
        /
        ELL
    )

    if w_eff <= 0.0:
        return {
            "passed": False,
            "w_eff": w_eff,
        }

    q_req = (
        w_eff
        /
        m.SIGMA_W_RELAXED_018A5
    )

    n_req = (
        q_req
        /
        Q_OVER_N
    )

    n_integer = max(
        1,
        int(
            round(
                n_req
            )
        ),
    )

    q_integer = (
        n_integer
        *
        Q_OVER_N
    )

    radius = (
        q_req
        *
        ELL
        /
        (
            2.0
            *
            math.pi
        )
    )

    mismatch = (
        abs(
            m.SIGMA_W_RELAXED_018A5
            *
            q_integer
            -
            w_eff
        )
        /
        w_eff
    )

    radius_over_wall = (
        radius
        /
        WALL_WIDTH90
    )

    radius_over_a_core = (
        radius
        /
        m.A_CORE_WIDTH
    )

    passed = (
        radius_over_wall
        >=
        MIN_SCALE_SEPARATION

        and
        radius_over_a_core
        >=
        MIN_SCALE_SEPARATION

        and
        mismatch
        <=
        MAX_INTEGER_MISMATCH
    )

    return {
        "passed":
            passed,

        "w_eff":
            w_eff,

        "q_req":
            q_req,

        "n_req":
            n_req,

        "n_integer":
            float(
                n_integer
            ),

        "radius":
            radius,

        "mismatch":
            mismatch,

        "radius_over_wall":
            radius_over_wall,

        "radius_over_a_core":
            radius_over_a_core,
    }


def main() -> None:
    """Run the complete backreaction/stress/EOS preflight."""

    print(
        "=== ANTIGRAVITY_RESEARCH 018A-6B0 ==="
    )

    print(
        "QUESTION="
        "IS_THE_018A6A_KLS_JUNCTION_BACKREACTION_SMALL_ENOUGH_TO_JUSTIFY_FULL_COUPLING"
    )

    original_chi = float(
        m.CHI_SELECTED
    )

    # ========================================================================
    # High-resolution selected junction.
    # ========================================================================

    print(
        "\n=== HIGH-RESOLUTION SELECTED JUNCTION ==="
    )

    m.CHI_SELECTED = (
        CHI_SELECTED
    )

    radial_selected = (
        m.solve_017p_background()
    )

    diag_selected = (
        m.diagnose_017p(
            radial_selected
        )
    )

    selected = (
        m.run_case(
            radial_selected,
            n=HIGH_N,
            box_half=HIGH_L,
        )
    )

    print(
        "SELECTED_2D_OPTIMIZER="
        f"{'PASS' if selected.optimizer_success else 'FAIL'}"
    )

    print(
        "SELECTED_MU_JUNCTION="
        f"{selected.junction_excess_energy:+.15e}"
    )

    print(
        "SELECTED_GRAD_RMS="
        f"{selected.gradient_rms:.15e}"
    )

    print(
        "SELECTED_GRAD_MAX="
        f"{selected.gradient_max:.15e}"
    )

    stress = (
        integrated_extension_stress(
            selected
        )
    )

    print(
        "\n=== FIXED-BACKGROUND EXTENSION STRESS ==="
    )

    for key in (
        "potential_integral",
        "gradient_energy",
        "total_energy",
        "active_total",
        "wall_energy",
        "wall_active",
        "junction_energy",
        "junction_active",
    ):
        print(
            f"{key.upper()}="
            f"{float(stress[key]):+.15e}"
        )

    junction_active_over_mu = (
        abs(
            float(
                stress[
                    "junction_active"
                ]
            )
        )
        /
        max(
            abs(
                float(
                    stress[
                        "junction_energy"
                    ]
                )
            ),
            1.0e-30,
        )
    )

    print(
        "ABS_JUNCTION_ACTIVE_OVER_MU="
        f"{junction_active_over_mu:.15e}"
    )

    # Original counterrotating-pair active line source.
    active_pair_017p = (
        4.0
        *
        diag_selected.sigma2
        *
        (
            OMEGA_SELECTED
            *
            OMEGA_SELECTED

            +
            K_SELECTED
            *
            K_SELECTED
        )
    )

    # Adversarially allow two copies of the measured localized active excess.
    pair_active_perturbation_fraction = (
        2.0
        *
        abs(
            float(
                stress[
                    "junction_active"
                ]
            )
        )
        /
        active_pair_017p
    )

    print(
        "ACTIVE_LINE_017P_PAIR="
        f"{active_pair_017p:.15e}"
    )

    print(
        "TWO_COPY_ABS_JUNCTION_ACTIVE_OVER_017P_ACTIVE_LINE="
        f"{pair_active_perturbation_fraction:.15e}"
    )

    active_source_pass = (
        pair_active_perturbation_fraction
        <
        MAX_ACTIVE_LINE_PERTURBATION_FRACTION
    )

    print(
        "JUNCTION_ACTIVE_SOURCE_PREFLIGHT="
        f"{'PASS' if active_source_pass else 'FAIL'}"
    )

    # ========================================================================
    # Direct frozen-sector backreaction sources.
    # ========================================================================

    print(
        "\n=== FROZEN-FIELD EULER-LAGRANGE SOURCE AUDIT ==="
    )

    (
        phi_source_max,
        phi_source_rms,
    ) = (
        phi_backreaction_source(
            selected
        )
    )

    print(
        "PHI_EXTENSION_SOURCE_MAX="
        f"{phi_source_max:.15e}"
    )

    print(
        "PHI_EXTENSION_SOURCE_RMS="
        f"{phi_source_rms:.15e}"
    )

    phi_source_pass = (
        phi_source_max
        <
        MAX_PHI_SOURCE
    )

    print(
        "PHI_BACKREACTION_SOURCE_PREFLIGHT="
        f"{'PASS' if phi_source_pass else 'FAIL'}"
    )

    print(
        "SIGMA_DIRECT_EXTENSION_SOURCE="
        "0"
    )

    print(
        "SIGMA_DIRECT_BACKREACTION="
        "ABSENT_BY_LAGRANGIAN"
    )

    (
        j_a_norm,
        j_phi_norm,
        gauge_ratio,
    ) = (
        gauge_current_ratio(
            selected
        )
    )

    print(
        "A_GAUGE_CURRENT_L2="
        f"{j_a_norm:.15e}"
    )

    print(
        "PHI_GAUGE_CURRENT_L2="
        f"{j_phi_norm:.15e}"
    )

    print(
        "A_TO_PHI_GAUGE_CURRENT_L2_RATIO="
        f"{gauge_ratio:.15e}"
    )

    gauge_source_pass = (
        gauge_ratio
        <
        MAX_GAUGE_CURRENT_RATIO
    )

    print(
        "GAUGE_BACKREACTION_SOURCE_PREFLIGHT="
        f"{'PASS' if gauge_source_pass else 'FAIL'}"
    )

    print(
        "ASYMPTOTIC_GAUGE_MASS_SQ_SHIFT="
        f"{m.F_A * m.F_A / 4.0:.15e}"
    )

    # ========================================================================
    # Chi continuation.
    # ========================================================================

    print(
        "\n=== FIXED-DISCRETIZATION CHI CONTINUATION ==="
    )

    records = []

    for chi in CHI_VALUES:

        m.CHI_SELECTED = float(
            chi
        )

        radial = (
            m.solve_017p_background()
        )

        diag = (
            m.diagnose_017p(
                radial
            )
        )

        result = (
            m.run_case(
                radial,
                n=CHI_N,
                box_half=CHI_L,
            )
        )

        a_eff = (
            diag.a_string
            +
            result.junction_excess_energy
        )

        records.append(
            {
                "chi":
                    float(
                        chi
                    ),

                "sigma2":
                    float(
                        diag.sigma2
                    ),

                "a_string":
                    float(
                        diag.a_string
                    ),

                "mu":
                    float(
                        result.junction_excess_energy
                    ),

                "a_eff":
                    float(
                        a_eff
                    ),

                "optimizer":
                    bool(
                        result.optimizer_success
                    ),
            }
        )

        print(
            "CHI_RECORD "
            f"CHI={chi:.9f} "
            f"SIGMA2={diag.sigma2:.15e} "
            f"A_STRING={diag.a_string:.15e} "
            f"MU_J={result.junction_excess_energy:+.15e} "
            f"A_EFF={a_eff:.15e} "
            f"OPT={'PASS' if result.optimizer_success else 'FAIL'}"
        )

    chi_array = np.array(
        [
            record[
                "chi"
            ]
            for record
            in records
        ],
        dtype=float,
    )

    sigma_array = np.array(
        [
            record[
                "sigma2"
            ]
            for record
            in records
        ],
        dtype=float,
    )

    a_array = np.array(
        [
            record[
                "a_string"
            ]
            for record
            in records
        ],
        dtype=float,
    )

    mu_array = np.array(
        [
            record[
                "mu"
            ]
            for record
            in records
        ],
        dtype=float,
    )

    a_eff_array = (
        a_array
        +
        mu_array
    )

    poly_sigma = np.polyfit(
        chi_array,
        sigma_array,
        2,
    )

    poly_a_eff = np.polyfit(
        chi_array,
        a_eff_array,
        2,
    )

    poly_mu = np.polyfit(
        chi_array,
        mu_array,
        2,
    )

    d_sigma = float(
        np.polyval(
            np.polyder(
                poly_sigma
            ),
            CHI_SELECTED,
        )
    )

    d_a_eff = float(
        np.polyval(
            np.polyder(
                poly_a_eff
            ),
            CHI_SELECTED,
        )
    )

    d_mu = float(
        np.polyval(
            np.polyder(
                poly_mu
            ),
            CHI_SELECTED,
        )
    )

    sigma_sel = float(
        sigma_array[
            -1
        ]
    )

    a_sel = float(
        a_array[
            -1
        ]
    )

    mu_sel_low = float(
        mu_array[
            -1
        ]
    )

    a_eff_sel = (
        a_sel
        +
        mu_sel_low
    )

    print(
        "\n=== FIXED-BACKGROUND VARIATIONAL / EOS CHECK ==="
    )

    print(
        "DMU_DCHI="
        f"{d_mu:+.15e}"
    )

    print(
        "DA_EFF_DCHI="
        f"{d_a_eff:+.15e}"
    )

    print(
        "SIGMA2_SELECTED="
        f"{sigma_sel:.15e}"
    )

    variational_relerr = (
        abs(
            d_a_eff
            +
            sigma_sel
        )
        /
        sigma_sel
    )

    print(
        "DA_EFF_DCHI_PLUS_SIGMA2_RELERR="
        f"{variational_relerr:.15e}"
    )

    variational_pass = (
        variational_relerr
        <
        MAX_VARIATIONAL_RELERR
    )

    print(
        "FIXED_BACKGROUND_VARIATIONAL_IDENTITY="
        f"{'PASS' if variational_pass else 'FAIL'}"
    )

    ct2_eff = (
        1.0
        /
        (
            1.0
            +
            2.0
            *
            CHI_SELECTED
            *
            sigma_sel
            /
            a_eff_sel
        )
    )

    cl2_eff = (
        1.0
        /
        (
            1.0
            +
            2.0
            *
            CHI_SELECTED
            *
            d_sigma
            /
            sigma_sel
        )
    )

    ct2_base_reconstructed = (
        1.0
        /
        (
            1.0
            +
            2.0
            *
            CHI_SELECTED
            *
            sigma_sel
            /
            a_sel
        )
    )

    print(
        "CT2_BASE_RECONSTRUCTED="
        f"{ct2_base_reconstructed:.15e}"
    )

    print(
        "CT2_WITH_JUNCTION="
        f"{ct2_eff:.15e}"
    )

    print(
        "CT2_SHIFT="
        f"{ct2_eff - ct2_base_reconstructed:+.15e}"
    )

    print(
        "CL2_FIXED_BACKGROUND="
        f"{cl2_eff:.15e}"
    )

    print(
        "CL2_REFERENCE_017P="
        f"{CL2_017P:.15e}"
    )

    eos_health_pass = (
        0.0
        <
        ct2_eff
        <=
        1.0

        and
        0.0
        <
        cl2_eff
        <=
        1.0
    )

    print(
        "FIXED_BACKGROUND_EOS_HEALTH="
        f"{'PASS' if eos_health_pass else 'FAIL'}"
    )

    (
        stability_pass,
        min_disc,
        max_root_imag,
        worst_mode,
    ) = (
        extrinsic_stability(
            ct2_eff,
            cl2_eff,
        )
    )

    print(
        "FIXED_BACKGROUND_MIN_M2_TO_M40_DISCRIMINANT="
        f"{min_disc:+.15e}"
    )

    print(
        f"FIXED_BACKGROUND_WORST_MODE={worst_mode}"
    )

    print(
        "FIXED_BACKGROUND_MAX_ROOT_IMAG="
        f"{max_root_imag:.15e}"
    )

    print(
        "FIXED_BACKGROUND_M2_TO_M40_STABILITY="
        f"{'PASS' if stability_pass else 'FAIL'}"
    )

    # ========================================================================
    # Mandatory stationarity correction.
    # ========================================================================

    print(
        "\n=== MANDATORY JUNCTION STATIONARITY BOOKKEEPING ==="
    )

    mu_high = float(
        selected.junction_excess_energy
    )

    print(
        "HIGH_RES_MU_JUNCTION="
        f"{mu_high:+.15e}"
    )

    print(
        "MU_OVER_A_STRING="
        f"{mu_high / diag_selected.a_string:.15e}"
    )

    print(
        "MU_OVER_DECLARED_LINE_BUDGET="
        f"{mu_high / m.EXTRA_LINE_BUDGET:.15e}"
    )

    stationarity_results = {}

    for count in (
        1,
        2,
    ):

        result = stationarity_case(
            mu_high,
            count,
        )

        stationarity_results[
            count
        ] = result

        print(
            "STATIONARITY "
            f"JUNCTION_COUNT={count} "
            f"W_EFF={float(result['w_eff']):.15e} "
            f"Q_REQ={float(result.get('q_req', math.nan)):.15e} "
            f"N_REQ={float(result.get('n_req', math.nan)):.15e} "
            f"N_INT={int(result.get('n_integer', 0.0))} "
            f"R_REQ={float(result.get('radius', math.nan)):.15e} "
            f"R_OVER_WALL90={float(result.get('radius_over_wall', math.nan)):.12f} "
            f"R_OVER_A_CORE={float(result.get('radius_over_a_core', math.nan)):.12f} "
            f"INTEGER_MISMATCH={float(result.get('mismatch', math.nan)):.15e} "
            f"PASS={'YES' if result['passed'] else 'NO'}"
        )

    one_stationarity_pass = bool(
        stationarity_results[
            1
        ][
            "passed"
        ]
    )

    two_stationarity_pass = bool(
        stationarity_results[
            2
        ][
            "passed"
        ]
    )

    print(
        "ONE_JUNCTION_STATIONARITY="
        f"{'PASS' if one_stationarity_pass else 'FAIL'}"
    )

    print(
        "TWO_JUNCTION_ADVERSARIAL_STATIONARITY="
        f"{'PASS' if two_stationarity_pass else 'FAIL'}"
    )

    # ========================================================================
    # Decision.
    # ========================================================================

    continuation_optimizer_pass = all(
        bool(
            record[
                "optimizer"
            ]
        )
        for record
        in records
    )

    overall_green = (
        selected.optimizer_success

        and
        continuation_optimizer_pass

        and
        phi_source_pass

        and
        gauge_source_pass

        and
        variational_pass

        and
        eos_health_pass

        and
        stability_pass

        and
        active_source_pass

        and
        one_stationarity_pass

        and
        two_stationarity_pass
    )

    print(
        "\n=== 018A-6B0 DECISION ==="
    )

    print(
        "SELECTED_2D_OPTIMIZER="
        f"{'PASS' if selected.optimizer_success else 'FAIL'}"
    )

    print(
        "CHI_CONTINUATION_OPTIMIZERS="
        f"{'PASS' if continuation_optimizer_pass else 'FAIL'}"
    )

    print(
        "PHI_BACKREACTION_SOURCE_PREFLIGHT="
        f"{'PASS' if phi_source_pass else 'FAIL'}"
    )

    print(
        "GAUGE_BACKREACTION_SOURCE_PREFLIGHT="
        f"{'PASS' if gauge_source_pass else 'FAIL'}"
    )

    print(
        "FIXED_BACKGROUND_VARIATIONAL_IDENTITY="
        f"{'PASS' if variational_pass else 'FAIL'}"
    )

    print(
        "FIXED_BACKGROUND_EOS_HEALTH="
        f"{'PASS' if eos_health_pass else 'FAIL'}"
    )

    print(
        "FIXED_BACKGROUND_M2_TO_M40_STABILITY="
        f"{'PASS' if stability_pass else 'FAIL'}"
    )

    print(
        "JUNCTION_ACTIVE_SOURCE_PREFLIGHT="
        f"{'PASS' if active_source_pass else 'FAIL'}"
    )

    print(
        "ONE_JUNCTION_STATIONARITY="
        f"{'PASS' if one_stationarity_pass else 'FAIL'}"
    )

    print(
        "TWO_JUNCTION_ADVERSARIAL_STATIONARITY="
        f"{'PASS' if two_stationarity_pass else 'FAIL'}"
    )

    print(
        "018A6B0_BACKREACTION_STRESS_EOS_PREFLIGHT="
        f"{'GREEN' if overall_green else 'RED'}"
    )

    if overall_green:
        print(
            "BACKREACTION_EXPECTATION="
            "PERTURBATIVE_AT_FIXED_BACKGROUND_PREFLIGHT_LEVEL"
        )

        print(
            "NEXT="
            "018A6B_FULLY_COUPLED_2D_KLS_JUNCTION_PHI_A_SIGMA_GAUGE_RELAXATION"
        )
    else:
        print(
            "BACKREACTION_EXPECTATION="
            "NONPERTURBATIVE_OR_UNRESOLVED_IN_AT_LEAST_ONE_DECLARED_CHANNEL"
        )

        print(
            "NEXT="
            "IDENTIFY_FAILED_BACKREACTION_CHANNEL_BEFORE_FULL_COUPLED_SOLVE"
        )

    print(
        "FULLY_COUPLED_2D_JUNCTION="
        "NOT_YET_SOLVED"
    )

    print(
        "COMPLETE_RELAXED_JUNCTION_T_MUNU="
        "NOT_YET_SOLVED"
    )

    print(
        "FINITE_PAYLOAD_GRAVITY_WITH_COMPLETE_NEW_SECTOR="
        "NOT_YET_TESTED"
    )

    print(
        "FULL_018A_GATE="
        "NOT_YET_GREEN"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE="
        "NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_018A_KLS_BACKREACTION_STRESS_EOS_PREFLIGHT"
    )

    m.CHI_SELECTED = (
        original_chi
    )


if __name__ == "__main__":
    main()
