#!/usr/bin/env python3
"""Simulation 018A-4 — same-gauge discrete-remnant string-wall preflight.

PURPOSE
-------
Test a higher-ranked microscopic wall realization after the separate
approximate-global wall sector reached a declared radial-convergence stop rule.

The candidate is the literature-backed two-stage Abelian breaking pattern

    U(1)_X -> Z_2 -> 1

implemented by a charge-2 string-forming field and a charge-1 lower-scale
field with a gauge-invariant trilinear phase-locking interaction.

SCIENTIFIC QUESTION
-------------------
Can the already-successful 017P gauged superconducting string be embedded as
the charge-2 string of a same-gauge discrete-remnant theory so that the
microscopic wall is topologically attached to the SAME rim, all long-range
phase gradients are gauge screened, and the resulting wall scale is compatible
with the existing 017P weak-wall equilibrium before any expensive 2D PDE?

WHY THIS MODEL IS TESTED NOW
----------------------------
The previous separate-wall candidate produced:

- a converged positive-energy microscopic planar wall;
- energetic core binding to the 017P string;
- a healthy 017P EOS/stability basin;
- restoring force exceeding wall pull throughout the healthy basin.

However, three increasingly careful radial infrared audits failed to make the
separate global-string amplitude profile quantitatively domain independent.
The project stop rule therefore forbids additional radial-boundary repairs.

The present candidate removes that structural weakness rather than tuning it.
Both wall/string fields are charged under one local U(1), and the relative
phase is locked. There is therefore no massless global phase producing the
logarithmic string tail that contaminated the previous reduction.

LITERATURE-ANCHORED TOPOLOGY
----------------------------
The relevant established construction uses two complex scalar fields with
charges 1 and 2 and the sequential breaking

    U(1) -> Z_2 -> 1.

A trilinear interaction of the schematic form

    Phi^* A^2 + h.c.

locks the gauge-invariant relative phase

    delta = 2 arg(A) - arg(Phi).

Here the existing 017P vortex-forming field Phi is assigned charge

    q_Phi = 2

under a fundamental coupling g_X chosen so that

    q_Phi g_X = g_017P.

Thus

    g_X = g_017P / 2.

This preserves the LOCAL 017P Phi/gauge equations when the new field is
absent, although the addition of a minimally charged field changes the global
gauge-group structure and is therefore a genuine extension rather than a mere
notation change.

For unit winding of Phi,

    Phi ~ exp(i theta),

finite covariant-gradient energy fixes the gauge flux to

    g_X integral X.dl = 2 pi / q_Phi = pi.

A charge-1 field transported around that vortex therefore obtains the Wilson
phase

    exp(i q_A g_X integral X.dl) = exp(i pi) = -1.

Equivalently, a smooth asymptotic charge-1 field would require winding 1/2.
That is impossible for a single-valued everywhere-nonzero complex field.
The field must therefore leave its vacuum manifold on a branch surface ending
on the Phi string. In the Z_2 remnant language, that surface is the wall.

This explicitly bypasses, rather than contradicts, the earlier same-U(1)
relative-phase obstruction: the earlier obstruction assumed both fields were
smooth and nonzero around the complete asymptotic loop. Here the required
branch wall is precisely where that assumption fails.

ATTACHMENT NUMBER
-----------------
For q_Phi=2, q_A=1 and unit Phi winding, one crossing of the residual Z_2
branch changes A by the required sign. Thus one branch sheet per minimal Phi
string is sufficient. A closed Phi string can therefore serve as the boundary
of one wall disk at the topology-preflight level.

This remains to be demonstrated by a true 2D field solution; this file does
not claim that topology alone proves a stationary drum.

NO-GLOBAL-TAIL TEST
-------------------
After both fields condense:

- the common U(1) phase is gauged/eaten;
- the gauge-invariant relative phase delta is given a mass by the trilinear
  phase-locking interaction.

Therefore no continuous massless phase remains in this minimal scalar/gauge
sector. The logarithmic global-string energy used in 018A-1 is absent.

The new charge-1 condensate does perturb the gauge mass. In the same field
normalization the fractional gauge-mass-squared shift is

    Delta m_X^2 / m_X,old^2 = F^2 / 4

for eta_Phi=1. This file requires that perturbation to remain small in the
preflight basin; the full straight-string EOS must still be recomputed later.

TARGET-PRESERVING RENORMALIZABLE POTENTIAL
------------------------------------------
For amplitude f=|Phi|, a=|A| and gauge-invariant relative phase delta, use the
zero-temperature potential

    V = lambda_Phi/4 (f^2-v^2)^2
        + lambda_A/4 (a^2-F^2)^2
        - 2 h f a^2 cos(delta)
        + c_Phi (f^2-v^2)
        + c_A (a^2-F^2)
        + C.

The quadratic counterterms are ordinary renormalizable mass shifts chosen so
that the desired vacuum

    f=v, a=F, delta=0

is an exact stationary point despite the trilinear interaction:

    c_Phi = h F^2 / v
    c_A   = 2 h v
    C     = 2 h v F^2.

The amplitude Hessian at the target vacuum is checked explicitly, and a
multi-start numerical minimization searches for a deeper competing homogeneous
vacuum.

GAUGE-INVARIANT PHASE-WALL TRIAL ESTIMATE
-----------------------------------------
At fixed asymptotic amplitudes, minimize the phase-gradient energy over the
common gauge direction.

For

    delta = 2 theta_A - theta_Phi

the physical relative-phase gradient coefficient is

    C_delta = v^2 F^2 / (4 v^2 + F^2).

The phase-locking potential is

    B_delta [1-cos(delta)]

with

    B_delta = 2 h v F^2.

The reduced fixed-amplitude sine-Gordon functional is

    E = C_delta (delta')^2 + B_delta [1-cos(delta)].

Its characteristic inverse thickness and tension are

    m_delta^2 = B_delta / (2 C_delta)

    delta_W = 1/m_delta

    sigma_trial = 8 sqrt(2 C_delta B_delta).

This is a CONTROLLED TRIAL-PATH estimate, not the final microscopic wall
tension. Amplitude and gauge relaxation in the true string-wall junction can
change it. It is used only to determine whether the model closes at finite
scales strongly enough to justify the next field solve.

017P SCALE MATCH
----------------
Use the journaled 017P selected-point anchors

    Q/N = 6.628230560688
    ell = L/Q = 0.4257542346286
    w_stat = 12.66497926067.

Because this candidate has no mandatory global-string logarithmic line energy,
the first topology/scale preflight uses

    Q_req = w_stat / sigma_trial
    N_req = Q_req / (Q/N)
    R_req = Q_req ell / (2 pi).

The new charge-1 string-core/junction energy is NOT omitted from the final
physics claim: it is explicitly marked unsolved and assigned a stationarity
budget

    mu_extra,max = w_stat ell / (2 pi)

above which the weak-wall stationarity load would be exhausted.

A natural comparison scale pi F^2 is reported, but is not substituted for the
actual future junction energy.

PRELIGHT PASS CONDITIONS
-------------------------
A scanned point passes this specific model-selection preflight only if:

- target homogeneous vacuum is locally stable;
- no deeper homogeneous amplitude vacuum is found by the declared search;
- relative phase is massive;
- gauge mass perturbation is below 1 percent in m^2;
- hierarchy v/F >= 5;
- R/delta_W >= 10;
- R/max(new amplitude core, inherited gauge-core proxy) >= 10;
- required Q and N are finite and positive;
- the extra-line-energy budget is positive.

These conditions DO NOT make full 018A green.

ROBUSTNESS
----------
The selected point is tested on a 5^3 lattice of simultaneous +/-10 percent
variations in

    F,
    h,
    lambda_A.

The user's blind wildcard numbers

    1.6, 1.875, 3.125, 0.625, 5

are applied only afterward as multiplicative h checks. They carry no physical
priority and cannot determine model selection.

FALSIFICATION
-------------
Reject or demote this candidate before a large PDE if:

- the charge/winding arithmetic does not force a wall branch;
- more than one uncontrolled wall is necessarily attached to the minimal rim;
- a massless relative phase remains;
- healthy vacuum structure requires large deformation of the 017P gauge
  sector;
- finite microscopic scale closure fails over a neighborhood;
- the eventual 2D junction has no regular finite-energy solution;
- complete added stress-energy destroys finite-payload repulsion.

NEXT IF GREEN
-------------
A green result promotes this model only to a TRUE 2D KLS JUNCTION DIAGNOSTIC.

That solve must include the existing 017P vortex field, its gauge field, the
current-carrying sigma condensate, the new charge-1 field, and the trilinear
phase-locking interaction.

LIMITATIONS
-----------
This file does NOT establish:

- the full 2D string-wall junction;
- the relaxed microscopic wall tension;
- the complete new string/junction line energy;
- the perturbed 017P EOS;
- full T_munu;
- finite-payload gravity with every new stress included;
- full stability;
- nonlinear Einstein-matter consistency;
- practical energy scaling;
- a practical antigravity device.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_018A_SAME_GAUGE_DISCRETE_REMNANT_MODEL_SELECTION_PREFLIGHT
"""

from __future__ import annotations

from dataclasses import dataclass
import itertools
import math

import numpy as np
from scipy.optimize import minimize


# ---------------------------------------------------------------------------
# Existing 017P selected-point anchors.
# ---------------------------------------------------------------------------

G_017P = 0.1414213562373095
ETA_PHI = 1.0
LAMBDA_PHI = 1.0

Q_OVER_N = 6.628230560688
ELL = 0.4257542346286
W_STAT = 12.66497926067

# Reinterpret the existing Phi field as charge 2 under a fundamental U(1)_X.
Q_PHI = 2
Q_A = 1
G_X = G_017P / Q_PHI
N_PHI = 1

# Representative point, chosen to retain the previous F scale for a clean
# model comparison rather than optimize after seeing the answer.
F_SELECTED = 0.075
H_SELECTED = 0.010
LAMBDA_A_SELECTED = 1.0

# Physically motivated coarse model-selection scan.
F_SCAN = (
    0.050,
    0.075,
    0.100,
    0.125,
    0.150,
)

H_SCAN = (
    0.0025,
    0.0050,
    0.0100,
    0.0200,
    0.0400,
    0.0800,
)

ROBUST_FACTORS = (
    0.90,
    0.95,
    1.00,
    1.05,
    1.10,
)

WILDCARD_VALUES = (
    1.6,
    1.875,
    3.125,
    0.625,
    5.0,
)

MAX_GAUGE_MASS_SQ_SHIFT = 0.01
MIN_HIGH_LOW_VEV_HIERARCHY = 5.0
MIN_SCALE_SEPARATION = 10.0

VACUUM_ENERGY_TOL = 1.0e-9
VACUUM_LOCATION_TOL = 2.0e-5

INHERITED_GAUGE_CORE_PROXY = (
    1.0
    /
    (
        math.sqrt(2.0)
        *
        G_017P
    )
)


@dataclass(frozen=True)
class PointResult:
    """Diagnostics for one discrete-remnant candidate point."""

    F: float
    h: float
    lambda_a: float

    vacuum_hessian_min_eig: float
    vacuum_search_energy: float
    vacuum_search_distance: float

    phase_mass: float
    wall_thickness: float
    wall_tension_trial: float

    q_req: float
    n_req: float
    n_integer: int
    radius_req: float

    radius_over_wall: float
    radius_over_core: float

    gauge_mass_sq_shift: float
    hierarchy: float

    extra_line_budget: float
    budget_over_pi_f2: float

    passed: bool


def topology_diagnostics() -> dict[str, float | bool]:
    """Compute exact charge, flux, holonomy, and branch-wall arithmetic."""

    effective_phi_coupling = (
        Q_PHI
        *
        G_X
    )

    reduced_flux_holonomy = (
        N_PHI
        /
        Q_PHI
    )

    required_a_winding = (
        Q_A
        *
        reduced_flux_holonomy
    )

    fractional_winding = (
        required_a_winding
        -
        math.floor(
            required_a_winding
        )
    )

    a_wilson_phase = (
        2.0
        *
        math.pi
        *
        required_a_winding
    )

    branch_jump = (
        2.0
        *
        math.pi
        *
        fractional_winding
    )

    local_017p_preserved = (
        math.isclose(
            effective_phi_coupling,
            G_017P,
            rel_tol=0.0,
            abs_tol=1.0e-15,
        )
    )

    requires_branch = not math.isclose(
        required_a_winding,
        round(
            required_a_winding
        ),
        rel_tol=0.0,
        abs_tol=1.0e-15,
    )

    one_z2_branch_suffices = (
        requires_branch
        and
        math.isclose(
            branch_jump,
            math.pi,
            rel_tol=0.0,
            abs_tol=1.0e-15,
        )
    )

    return {
        "effective_phi_coupling":
            effective_phi_coupling,

        "reduced_flux_holonomy":
            reduced_flux_holonomy,

        "required_a_winding":
            required_a_winding,

        "a_wilson_phase":
            a_wilson_phase,

        "branch_jump":
            branch_jump,

        "local_017p_preserved":
            local_017p_preserved,

        "requires_branch":
            requires_branch,

        "one_z2_branch_suffices":
            one_z2_branch_suffices,
    }


def potential_coefficients(
    F: float,
    h: float,
) -> tuple[float, float, float]:
    """Return target-vacuum-preserving mass shifts and vacuum constant."""

    c_phi = (
        h
        *
        F
        *
        F
        /
        ETA_PHI
    )

    c_a = (
        2.0
        *
        h
        *
        ETA_PHI
    )

    constant = (
        2.0
        *
        h
        *
        ETA_PHI
        *
        F
        *
        F
    )

    return (
        c_phi,
        c_a,
        constant,
    )


def amplitude_potential(
    amplitudes: np.ndarray,
    *,
    F: float,
    h: float,
    lambda_a: float,
) -> float:
    """Evaluate the homogeneous potential at the phase-minimizing direction."""

    f = float(
        amplitudes[0]
    )

    a = float(
        amplitudes[1]
    )

    (
        c_phi,
        c_a,
        constant,
    ) = potential_coefficients(
        F,
        h,
    )

    return float(
        LAMBDA_PHI
        /
        4.0
        *
        (
            f
            *
            f
            -
            ETA_PHI
            *
            ETA_PHI
        ) ** 2

        +
        lambda_a
        /
        4.0
        *
        (
            a
            *
            a
            -
            F
            *
            F
        ) ** 2

        -
        2.0
        *
        h
        *
        f
        *
        a
        *
        a

        +
        c_phi
        *
        (
            f
            *
            f
            -
            ETA_PHI
            *
            ETA_PHI
        )

        +
        c_a
        *
        (
            a
            *
            a
            -
            F
            *
            F
        )

        +
        constant
    )


def amplitude_hessian(
    F: float,
    h: float,
    lambda_a: float,
) -> np.ndarray:
    """Return the homogeneous amplitude Hessian at the target vacuum."""

    h_ff = (
        2.0
        *
        LAMBDA_PHI
        *
        ETA_PHI
        *
        ETA_PHI

        +
        2.0
        *
        h
        *
        F
        *
        F
        /
        ETA_PHI
    )

    h_aa = (
        2.0
        *
        lambda_a
        *
        F
        *
        F
    )

    h_fa = (
        -4.0
        *
        h
        *
        F
    )

    return np.array(
        [
            [
                h_ff,
                h_fa,
            ],
            [
                h_fa,
                h_aa,
            ],
        ],
        dtype=float,
    )


def search_homogeneous_vacuum(
    F: float,
    h: float,
    lambda_a: float,
) -> tuple[float, float]:
    """Search numerically for a deeper homogeneous amplitude minimum."""

    target = np.array(
        [
            ETA_PHI,
            F,
        ],
        dtype=float,
    )

    bounds = (
        (
            0.0,
            4.0,
        ),
        (
            0.0,
            4.0,
        ),
    )

    starts = []

    for f0 in np.linspace(
        0.0,
        2.0,
        5,
    ):
        for a0 in np.linspace(
            0.0,
            max(
                0.5,
                4.0
                *
                F,
            ),
            5,
        ):
            starts.append(
                np.array(
                    [
                        f0,
                        a0,
                    ],
                    dtype=float,
                )
            )

    starts.append(
        target
    )

    best_energy = math.inf
    best_location = None

    for start in starts:

        result = minimize(
            lambda x: amplitude_potential(
                x,
                F=F,
                h=h,
                lambda_a=lambda_a,
            ),
            start,
            method="L-BFGS-B",
            bounds=bounds,
            options={
                "ftol": 1.0e-15,
                "gtol": 1.0e-12,
                "maxiter": 3000,
            },
        )

        if (
            result.fun
            <
            best_energy
        ):
            best_energy = float(
                result.fun
            )

            best_location = np.array(
                result.x,
                dtype=float,
            )

    if best_location is None:
        raise RuntimeError(
            "Homogeneous vacuum search produced no result"
        )

    distance = float(
        np.linalg.norm(
            best_location
            -
            target
        )
    )

    return (
        best_energy,
        distance,
    )


def evaluate_point(
    F: float,
    h: float,
    lambda_a: float,
) -> PointResult:
    """Evaluate one model point against the cheap 018A-4 gates."""

    if (
        F <= 0.0
        or
        h <= 0.0
        or
        lambda_a <= 0.0
    ):
        raise ValueError(
            "F, h, and lambda_a must all be positive"
        )

    hessian = amplitude_hessian(
        F,
        h,
        lambda_a,
    )

    min_eig = float(
        np.min(
            np.linalg.eigvalsh(
                hessian
            )
        )
    )

    (
        vacuum_energy,
        vacuum_distance,
    ) = search_homogeneous_vacuum(
        F,
        h,
        lambda_a,
    )

    # Physical relative-phase gradient after minimizing the common gauge
    # direction.
    c_delta = (
        ETA_PHI
        *
        ETA_PHI
        *
        F
        *
        F
        /
        (
            4.0
            *
            ETA_PHI
            *
            ETA_PHI
            +
            F
            *
            F
        )
    )

    b_delta = (
        2.0
        *
        h
        *
        ETA_PHI
        *
        F
        *
        F
    )

    phase_mass_sq = (
        b_delta
        /
        (
            2.0
            *
            c_delta
        )
    )

    phase_mass = (
        math.sqrt(
            phase_mass_sq
        )
    )

    wall_thickness = (
        1.0
        /
        phase_mass
    )

    wall_tension_trial = (
        8.0
        *
        math.sqrt(
            2.0
            *
            c_delta
            *
            b_delta
        )
    )

    q_req = (
        W_STAT
        /
        wall_tension_trial
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

    radius_req = (
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

    new_a_core = (
        1.0
        /
        (
            math.sqrt(
                lambda_a
            )
            *
            F
        )
    )

    max_core = max(
        INHERITED_GAUGE_CORE_PROXY,
        new_a_core,
    )

    radius_over_wall = (
        radius_req
        /
        wall_thickness
    )

    radius_over_core = (
        radius_req
        /
        max_core
    )

    gauge_mass_sq_shift = (
        F
        *
        F
        /
        (
            4.0
            *
            ETA_PHI
            *
            ETA_PHI
        )
    )

    hierarchy = (
        ETA_PHI
        /
        F
    )

    extra_line_budget = (
        W_STAT
        *
        ELL
        /
        (
            2.0
            *
            math.pi
        )
    )

    budget_over_pi_f2 = (
        extra_line_budget
        /
        (
            math.pi
            *
            F
            *
            F
        )
    )

    vacuum_local_pass = (
        min_eig
        >
        0.0
    )

    vacuum_global_pass = (
        vacuum_energy
        >=
        -VACUUM_ENERGY_TOL

        and

        vacuum_distance
        <=
        VACUUM_LOCATION_TOL
    )

    passed = (
        vacuum_local_pass

        and
        vacuum_global_pass

        and
        phase_mass > 0.0

        and
        gauge_mass_sq_shift
        <=
        MAX_GAUGE_MASS_SQ_SHIFT

        and
        hierarchy
        >=
        MIN_HIGH_LOW_VEV_HIERARCHY

        and
        radius_over_wall
        >=
        MIN_SCALE_SEPARATION

        and
        radius_over_core
        >=
        MIN_SCALE_SEPARATION

        and
        q_req > 0.0

        and
        n_req > 0.0

        and
        extra_line_budget > 0.0
    )

    return PointResult(
        F=F,
        h=h,
        lambda_a=lambda_a,

        vacuum_hessian_min_eig=min_eig,
        vacuum_search_energy=vacuum_energy,
        vacuum_search_distance=vacuum_distance,

        phase_mass=phase_mass,
        wall_thickness=wall_thickness,
        wall_tension_trial=wall_tension_trial,

        q_req=q_req,
        n_req=n_req,
        n_integer=n_integer,
        radius_req=radius_req,

        radius_over_wall=radius_over_wall,
        radius_over_core=radius_over_core,

        gauge_mass_sq_shift=gauge_mass_sq_shift,
        hierarchy=hierarchy,

        extra_line_budget=extra_line_budget,
        budget_over_pi_f2=budget_over_pi_f2,

        passed=passed,
    )


def print_point(
    label: str,
    point: PointResult,
) -> None:
    """Print one compact point report."""

    print(
        f"{label} "
        f"F={point.F:.9f} "
        f"H={point.h:.9f} "
        f"LAMBDA_A={point.lambda_a:.9f} "
        f"HESSIAN_MIN={point.vacuum_hessian_min_eig:.12e} "
        f"VAC_E={point.vacuum_search_energy:+.6e} "
        f"VAC_DIST={point.vacuum_search_distance:.6e} "
        f"M_DELTA={point.phase_mass:.9e} "
        f"SIGMA_TRIAL={point.wall_tension_trial:.12e} "
        f"DELTA_W={point.wall_thickness:.9f} "
        f"Q_REQ={point.q_req:.9f} "
        f"N_REQ={point.n_req:.9f} "
        f"N_INT={point.n_integer} "
        f"R_REQ={point.radius_req:.9f} "
        f"R_OVER_WALL={point.radius_over_wall:.9f} "
        f"R_OVER_CORE={point.radius_over_core:.9f} "
        f"GAUGE_M2_SHIFT={point.gauge_mass_sq_shift:.9e} "
        f"VEV_HIERARCHY={point.hierarchy:.9f} "
        f"LINE_BUDGET_OVER_PI_F2={point.budget_over_pi_f2:.9f} "
        f"PASS={'YES' if point.passed else 'NO'}"
    )


def main() -> None:
    """Execute topology, model-selection, scale, and robustness gates."""

    print(
        "=== ANTIGRAVITY_RESEARCH 018A-4 ==="
    )

    print(
        "QUESTION="
        "CAN_A_SAME_GAUGE_U1_TO_Z2_TO_1_DISCRETE_REMNANT_WALL_BE_EMBEDDED_IN_017P"
    )

    print(
        "\n=== EXACT CHARGE / HOLONOMY TOPOLOGY ==="
    )

    topo = topology_diagnostics()

    print(
        f"Q_PHI={Q_PHI}"
    )

    print(
        f"Q_A={Q_A}"
    )

    print(
        f"G_017P={G_017P:.15e}"
    )

    print(
        f"G_X={G_X:.15e}"
    )

    print(
        "Q_PHI_TIMES_G_X="
        f"{float(topo['effective_phi_coupling']):.15e}"
    )

    print(
        "LOCAL_017P_PHI_GAUGE_COUPLING_PRESERVED="
        f"{'YES' if topo['local_017p_preserved'] else 'NO'}"
    )

    print(
        "UNIT_PHI_REDUCED_FLUX_HOLONOMY="
        f"{float(topo['reduced_flux_holonomy']):.15e}"
    )

    print(
        "SMOOTH_A_REQUIRED_WINDING="
        f"{float(topo['required_a_winding']):.15e}"
    )

    print(
        "A_WILSON_PHASE_AROUND_UNIT_PHI_STRING="
        f"{float(topo['a_wilson_phase']):.15e}"
    )

    print(
        "A_WILSON_FACTOR="
        f"{math.cos(float(topo['a_wilson_phase'])):+.1f}"
    )

    print(
        "ASYMPTOTIC_SMOOTH_A_WITHOUT_WALL="
        f"{'NO' if topo['requires_branch'] else 'YES'}"
    )

    print(
        "REQUIRED_BRANCH_PHASE_JUMP="
        f"{float(topo['branch_jump']):.15e}"
    )

    print(
        "ONE_Z2_BRANCH_SHEET_PER_MINIMAL_STRING_SUFFICES="
        f"{'YES' if topo['one_z2_branch_suffices'] else 'NO'}"
    )

    topology_pass = (
        bool(
            topo[
                "local_017p_preserved"
            ]
        )

        and

        bool(
            topo[
                "requires_branch"
            ]
        )

        and

        bool(
            topo[
                "one_z2_branch_suffices"
            ]
        )
    )

    print(
        "SAME_GAUGE_DISCRETE_REMNANT_TOPOLOGY="
        f"{'PASS' if topology_pass else 'FAIL'}"
    )

    print(
        "COMMON_PHASE=GAUGED"
    )

    print(
        "RELATIVE_PHASE=TRILINEAR_LOCKED"
    )

    print(
        "MANDATORY_GLOBAL_STRING_LOG_TAIL="
        "ABSENT_IN_THIS_LOCAL_MODEL"
    )

    print(
        "\n=== SELECTED MODEL POINT ==="
    )

    selected = evaluate_point(
        F_SELECTED,
        H_SELECTED,
        LAMBDA_A_SELECTED,
    )

    print_point(
        "SELECTED",
        selected,
    )

    print(
        "SELECTED_FIXED_AMPLITUDE_WALL_TENSION_STATUS="
        "TRIAL_PATH_ESTIMATE_NOT_FINAL_RELAXED_TENSION"
    )

    print(
        "SELECTED_EXTRA_LINE_ENERGY_BUDGET="
        f"{selected.extra_line_budget:.15e}"
    )

    print(
        "SELECTED_NEW_STRING_JUNCTION_LINE_ENERGY="
        "NOT_YET_SOLVED"
    )

    print(
        "\n=== PHYSICALLY MOTIVATED COARSE SCAN ==="
    )

    coarse_results = []

    for (
        F,
        h,
    ) in itertools.product(
        F_SCAN,
        H_SCAN,
    ):
        point = evaluate_point(
            F,
            h,
            LAMBDA_A_SELECTED,
        )

        coarse_results.append(
            point
        )

        print_point(
            "SCAN",
            point,
        )

    coarse_pass = [
        point
        for point
        in coarse_results
        if point.passed
    ]

    print(
        f"COARSE_TOTAL={len(coarse_results)}"
    )

    print(
        f"COARSE_PASS={len(coarse_pass)}"
    )

    if coarse_pass:
        print(
            "COARSE_MIN_R_OVER_WALL="
            f"{min(point.radius_over_wall for point in coarse_pass):.12f}"
        )

        print(
            "COARSE_MIN_R_OVER_CORE="
            f"{min(point.radius_over_core for point in coarse_pass):.12f}"
        )

        print(
            "COARSE_MAX_GAUGE_M2_SHIFT="
            f"{max(point.gauge_mass_sq_shift for point in coarse_pass):.12e}"
        )

    print(
        "\n=== SELECTED +/-10 PERCENT 5^3 ROBUSTNESS ==="
    )

    robust_results = []

    for (
        f_mult,
        h_mult,
        lambda_mult,
    ) in itertools.product(
        ROBUST_FACTORS,
        ROBUST_FACTORS,
        ROBUST_FACTORS,
    ):

        point = evaluate_point(
            F_SELECTED
            *
            f_mult,

            H_SELECTED
            *
            h_mult,

            LAMBDA_A_SELECTED
            *
            lambda_mult,
        )

        robust_results.append(
            point
        )

    robust_pass = [
        point
        for point
        in robust_results
        if point.passed
    ]

    print(
        f"ROBUST_TOTAL={len(robust_results)}"
    )

    print(
        f"ROBUST_PASS={len(robust_pass)}"
    )

    if robust_pass:
        print(
            "ROBUST_MIN_HESSIAN_EIG="
            f"{min(point.vacuum_hessian_min_eig for point in robust_pass):.15e}"
        )

        print(
            "ROBUST_MIN_R_OVER_WALL="
            f"{min(point.radius_over_wall for point in robust_pass):.12f}"
        )

        print(
            "ROBUST_MIN_R_OVER_CORE="
            f"{min(point.radius_over_core for point in robust_pass):.12f}"
        )

        print(
            "ROBUST_MAX_GAUGE_M2_SHIFT="
            f"{max(point.gauge_mass_sq_shift for point in robust_pass):.15e}"
        )

        print(
            "ROBUST_MIN_LINE_BUDGET_OVER_PI_F2="
            f"{min(point.budget_over_pi_f2 for point in robust_pass):.12f}"
        )

    robustness_green = (
        len(
            robust_pass
        )
        ==
        len(
            robust_results
        )
    )

    print(
        "SELECTED_ROBUSTNESS="
        f"{'PASS' if robustness_green else 'FAIL'}"
    )

    print(
        "\n=== BLIND WILDCARD h MULTIPLIERS ==="
    )

    for raw in WILDCARD_VALUES:

        point = evaluate_point(
            F_SELECTED,
            H_SELECTED
            *
            raw,
            LAMBDA_A_SELECTED,
        )

        print_point(
            f"WILDCARD[RAW={raw:.9f}]",
            point,
        )

        print(
            "WILDCARD_INTERPRETATION="
            "BLIND_AUXILIARY_CHECK_NOT_PHYSICS_PRIOR"
        )

    print(
        "\n=== MODEL-SELECTION COMPARISON ==="
    )

    print(
        "PREVIOUS_SEPARATE_GLOBAL_WALL_TOPOLOGY="
        "SUPPORTED"
    )

    print(
        "PREVIOUS_SEPARATE_GLOBAL_WALL_CORE_BINDING="
        "SUPPORTED"
    )

    print(
        "PREVIOUS_SEPARATE_GLOBAL_WALL_RADIAL_FORCE_CONVERGENCE="
        "FAILED_STOP_RULE_AFTER_THREE_IR_AUDITS"
    )

    print(
        "NEW_SAME_GAUGE_WALL_ENDPOINT="
        "TOPOLOGICALLY_TIED_TO_EXISTING_017P_VORTEX"
    )

    print(
        "NEW_SAME_GAUGE_GLOBAL_LOG_TAIL="
        "ABSENT"
    )

    print(
        "NEW_FIELDS_ADDED_BEYOND_017P="
        "ONE_CHARGE1_COMPLEX_SCALAR"
    )

    model_selection_green = (
        topology_pass
        and
        selected.passed
        and
        robustness_green
        and
        len(
            coarse_pass
        )
        >
        0
    )

    print(
        "\n=== 018A-4 DECISION ==="
    )

    print(
        "SAME_GAUGE_DISCRETE_REMNANT_TOPOLOGY="
        f"{'PASS' if topology_pass else 'FAIL'}"
    )

    print(
        "SELECTED_VACUUM_AND_SCALE_PREFLIGHT="
        f"{'PASS' if selected.passed else 'FAIL'}"
    )

    print(
        "SELECTED_ROBUSTNESS="
        f"{'PASS' if robustness_green else 'FAIL'}"
    )

    print(
        "018A4_SAME_GAUGE_KLS_MODEL_SELECTION_PREFLIGHT="
        f"{'GREEN' if model_selection_green else 'RED'}"
    )

    print(
        "PREFERRED_018A_MICROSCOPIC_CLASS="
        +
        (
            "SAME_GAUGE_DISCRETE_REMNANT_KLS_STYLE"
            if model_selection_green
            else
            "UNRESOLVED"
        )
    )

    print(
        "FULL_RELAXED_MICROSCOPIC_WALL_TENSION="
        "NOT_YET_SOLVED"
    )

    print(
        "TRUE_2D_STRING_WALL_JUNCTION="
        "NOT_YET_SOLVED"
    )

    print(
        "PERTURBED_017P_EOS_WITH_CHARGE1_FIELD="
        "NOT_YET_SOLVED"
    )

    print(
        "COMPLETE_JUNCTION_STRESS_ENERGY="
        "NOT_YET_SOLVED"
    )

    print(
        "FINITE_PAYLOAD_GRAVITY_WITH_NEW_SECTOR="
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
        "PROJECT_DERIVED_018A_SAME_GAUGE_DISCRETE_REMNANT_MODEL_SELECTION_PREFLIGHT"
    )

    if model_selection_green:
        print(
            "NEXT="
            "018A5_MINIMAL_TRUE_2D_KLS_STRING_WALL_JUNCTION_DIAGNOSTIC_WITH_017P_FIELDS"
        )
    else:
        print(
            "NEXT="
            "AUDIT_DISCRETE_REMNANT_EMBEDDING_OR_RERANK_TO_2HDM_PROTECTED_ALTERNATIVE"
        )


if __name__ == "__main__":
    main()
