"""Simulation 018A-1 — nonthermal string-wall topology and scale preflight.

PURPOSE
-------
Perform the cheapest decisive first slice of Buildplan phase 018A before any
large 2D/3D coupled drum-vorton PDE solve.

SCIENTIFIC QUESTION
-------------------
Can a zero-temperature microscopic wall sector be attached consistently to the
literature-backed 017P gauged-vorton rim, with finite wall tension/thickness and
finite charge/winding/radius scales, without reintroducing a thermal support
bath?

THIS FILE TESTS THREE INCREASINGLY GENERAL TOPOLOGY CLASSES
----------------------------------------------------------
1. The exact 017P field content.
2. A naive second Higgs field charged under the same single Abelian U(1), with
   a wall potential for the gauge-invariant relative phase.
3. A separate approximate-global-U(1) complex scalar A whose explicit breaking
   gives an N_DW=1 pseudo-Goldstone wall, locally bound to the 017P vortex core
   by a gauge-invariant magnitude-overlap interaction.

KEY ANALYTICAL TOPOLOGY RESULT
------------------------------
For two fields phi_1, phi_2 with nonzero asymptotic VEVs and charges q_1, q_2
under one Abelian gauge field, finite local-string energy requires

    D_theta phi_i -> 0

at large radius. If phi_i ~ exp(i n_i theta), this gives

    n_1 / q_1 = n_2 / q_2 = common gauge flux parameter.

The gauge-invariant relative phase is

    Theta = q_2 arg(phi_1) - q_1 arg(phi_2),

so its winding is

    Delta Theta / (2 pi) = q_2 n_1 - q_1 n_2 = 0.

Therefore the ordinary finite-energy local vortex in this naive same-U(1)
class cannot be the boundary of a relative-phase wall. Forcing nonzero relative
winding leaves an uncancelled covariant phase gradient and exits the same
finite-local-energy string class.

SURVIVING NONTHERMAL CANDIDATE
------------------------------
Introduce a separate canonical complex scalar

    A = rho exp(i theta) / sqrt(2)

with an approximate global U(1) broken explicitly to a unique vacuum. A simple
renormalizable zero-temperature potential can be written

    V_A = lambda_A/4 (rho^2 - F0^2)^2
          - m_A^2 F rho cos(theta)
          + C,

with F0 chosen so rho=F, theta=0 is the exact vacuum. In the controlled
m_A << m_r limit the phase sector becomes sine-Gordon:

    L_theta = F^2/2 (partial theta)^2
              - m_A^2 F^2 (1 - cos theta).

A unit global string carries one 2 pi phase winding, and the explicit breaking
confines that winding into one N_DW=1 wall. The string-wall composite is not a
stable isolated topological defect: wall tension tries to collapse it. That is
compatible with the vorton program because the 017P current/charge is precisely
what must provide the opposing radial support.

The frozen-radial sine-Gordon estimates are

    sigma_W = 8 m_A F^2
    delta_W ~ 1 / m_A.

The straight global-string logarithmic line-energy contribution is included at
leading order as

    mu_A,log = pi F^2 ln(m_r / m_A).

This term is mandatory bookkeeping, not optional support energy.

JUNCTION MODEL
--------------
A local gauge-invariant core-overlap interaction with the 017P gauged vortex
field phi can be chosen schematically as

    V_J = -kappa_J/2
          (|phi|^2 - eta_phi^2)
          (|A|^2 - F^2/2).

For positive kappa_J it lowers the energy when both cores overlap. Together
with positive quartics it remains bounded for an appropriate coupling matrix,
for example kappa_J^2 < lambda_phi lambda_A in the stated normalization.

The junction is NOT solved in this file. Its full energy/stress and its effect
on the 017P straight-string BVP are the next decisive subgate.

017P MATCHING
-------------
The current journaled 017P selected point supplies

    q = Q/N
    ell = L/Q
    w_stat = sigma_W Q

for the effective wall-only stationarity condition.

If a separate boundary string contributes extra line energy mu_A L, then at
fixed Q,N the radial derivative acquires +mu_A. In the same thin-worldsheet
normalization the wall load available after this mandatory line-energy term is

    w_eff = w_stat - 2 pi mu_A / ell

for one added boundary string. This is an analytical stationarity correction,
not a full composite stability proof.

Then

    Q_req = w_eff / sigma_W
    N_req = Q_req / q
    R_req = Q_req ell / (2 pi).

The strong thin-worldsheet preflight diagnostic is

    R_req / max(delta_W, delta_core) >= 10.

OPERATIONAL OBSERVABLE
----------------------
This first subgate does not recompute the complete gravitational field. It tests
whether the microscopic wall topology and scale matching survive cheaply enough
to justify the next thin-composite gravity/junction calculation.

UNITS AND NORMALIZATION
-----------------------
Natural units and the dimensionless 017P field normalization are used. F is
therefore a dimensionless symmetry-breaking scale relative to the 017P vortex
scale. Absolute SI scaling is not inferred here.

NUMERICAL METHOD
----------------
- Analytic topology/integrability proofs for classes 1 and 2.
- scipy.solve_bvp for a 1D planar wall profile in class 3.
- Domain-size convergence of the wall tension and active source.
- A 5^5 = 3125 point +/-10% robustness lattice for the cheapest scale-matching
  quantities using the conservative frozen-radial wall-tension upper bound.

VALIDATION
----------
The 1D solution is checked against:
- the sine-Gordon tension 8 m_A F^2;
- the first-integral/virial relation integrated across the wall;
- the canonical planar-wall active-source identity.

For a static 1D canonical wall,

    p_x = p_y = -epsilon
    p_z = K - V

so

    S = epsilon + p_x + p_y + p_z = -2 V.

At a stationary wall with degenerate endpoint vacuum values,

    integral K = integral V

and therefore

    integral S = -sigma_W.

FALSIFICATION STRATEGY
----------------------
Reject this candidate class before a 2D PDE if any of the following occurs:
- no converged 1D wall saddle in the controlled hierarchy regime;
- nonfinite/negative required wall load after mandatory line energy;
- divergent or noninteger-compatible Q,N matching;
- R/core or R/wall scale separation below the preflight threshold throughout
  a reasonable neighborhood;
- the explicit junction cannot bind the cores without destabilizing the vacuum;
- the next complete thin-composite gravity calculation loses finite-payload
  outward acceleration or positive far-field active mass.

LIMITATIONS
-----------
This file does NOT establish:
- the full 018A green gate;
- a solved 017P-plus-wall junction BVP;
- complete gauge/junction stress-energy bookkeeping;
- full finite-payload gravity after adding the junction;
- full composite dynamic stability;
- a 2D finite-thickness Euler-Lagrange drum solution;
- nonlinear Einstein-matter consistency;
- practical energy scaling or a practical antigravity device.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_018A_TOPOLOGY_AND_1D_WALL_PREFLIGHT
"""

from __future__ import annotations

import itertools
import math

import numpy as np
from scipy.integrate import simpson, solve_bvp


# ---------------------------------------------------------------------------
# Journaled 017P selected-point anchors.
# ---------------------------------------------------------------------------

Q_OVER_N_017P = 6.628230560688
ELL_017P = 0.4257542346286
WALL_LOAD_017P = 12.66497926067


# ---------------------------------------------------------------------------
# Selected nonthermal wall preflight point.
# ---------------------------------------------------------------------------

F_PHASE = 0.075
MASS_HIERARCHY = 10.0
BOUNDARY_STRING_COUNT = 1


# ---------------------------------------------------------------------------
# Strong preflight thresholds.
# ---------------------------------------------------------------------------

MIN_SCALE_SEPARATION = 10.0
MAX_INTEGER_LOAD_MISMATCH = 1.0e-3


def same_u1_relative_phase_winding(
    q1: int,
    q2: int,
    flux_units: int,
) -> int:
    """Return relative-phase winding forced by finite-energy local winding."""

    n1 = q1 * flux_units
    n2 = q2 * flux_units

    return q2 * n1 - q1 * n2


def wall_parameters(
    F: float,
    hierarchy: float,
) -> dict[str, float]:
    """Construct an exact polynomial-potential parameter point."""

    m_a = F / hierarchy
    m_r = F

    lam = (
        m_r * m_r - m_a * m_a
    ) / (
        2.0 * F * F
    )

    if lam <= 0.0:
        raise ValueError(
            "Need hierarchy > 1 so lambda_A > 0"
        )

    F0_sq = (
        F * F
        -
        m_a * m_a / lam
    )

    if F0_sq <= 0.0:
        raise ValueError(
            "Chosen parameters do not give positive F0^2"
        )

    C = (
        m_a * m_a * F * F
        -
        (m_a**4) / (4.0 * lam)
    )

    return {
        "F": F,
        "m_a": m_a,
        "m_r": m_r,
        "lambda_A": lam,
        "F0_sq": F0_sq,
        "C": C,
    }


def solve_planar_wall(
    F: float,
    hierarchy: float,
    domain_widths: float,
) -> dict[str, float]:
    """Solve the coupled radial/phase 1D wall BVP."""

    pars = wall_parameters(
        F,
        hierarchy,
    )

    m_a = pars["m_a"]
    lam = pars["lambda_A"]
    F0_sq = pars["F0_sq"]
    C = pars["C"]

    half_extent = domain_widths / m_a

    z = np.linspace(
        -half_extent,
        half_extent,
        900,
    )

    theta_guess = (
        4.0
        *
        np.arctan(
            np.exp(m_a * z)
        )
    )

    theta_prime_guess = (
        2.0
        *
        m_a
        /
        np.cosh(m_a * z)
    )

    rho_guess = (
        F
        *
        (
            1.0
            -
            0.05
            /
            np.cosh(m_a * z) ** 2
        )
    )

    rho_prime_guess = np.gradient(
        rho_guess,
        z,
    )

    y_guess = np.vstack(
        [
            rho_guess,
            rho_prime_guess,
            theta_guess,
            theta_prime_guess,
        ]
    )

    def ode(
        _: np.ndarray,
        y: np.ndarray,
    ) -> np.ndarray:
        rho = np.maximum(
            y[0],
            1.0e-14,
        )

        rho_prime = y[1]
        theta = y[2]
        theta_prime = y[3]

        dV_drho = (
            lam
            *
            rho
            *
            (
                rho * rho
                -
                F0_sq
            )
            -
            m_a
            *
            m_a
            *
            F
            *
            np.cos(theta)
        )

        dV_dtheta = (
            m_a
            *
            m_a
            *
            F
            *
            rho
            *
            np.sin(theta)
        )

        rho_second = (
            rho
            *
            theta_prime
            *
            theta_prime
            +
            dV_drho
        )

        theta_second = (
            dV_dtheta
            /
            (
                rho * rho
            )
            -
            2.0
            *
            rho_prime
            *
            theta_prime
            /
            rho
        )

        return np.vstack(
            [
                rho_prime,
                rho_second,
                theta_prime,
                theta_second,
            ]
        )

    def boundary(
        ya: np.ndarray,
        yb: np.ndarray,
    ) -> np.ndarray:
        return np.array(
            [
                ya[0] - F,
                ya[2],
                yb[0] - F,
                yb[2] - 2.0 * math.pi,
            ]
        )

    solution = solve_bvp(
        ode,
        boundary,
        z,
        y_guess,
        tol=1.0e-7,
        max_nodes=30000,
    )

    if solution.status != 0:
        raise RuntimeError(
            "Wall BVP failed: "
            f"{solution.message}"
        )

    z_eval = np.linspace(
        -half_extent,
        half_extent,
        8000,
    )

    (
        rho,
        rho_prime,
        theta,
        theta_prime,
    ) = solution.sol(z_eval)

    potential = (
        lam
        /
        4.0
        *
        (
            rho * rho - F0_sq
        ) ** 2
        -
        m_a
        *
        m_a
        *
        F
        *
        rho
        *
        np.cos(theta)
        +
        C
    )

    kinetic = (
        0.5
        *
        rho_prime
        *
        rho_prime
        +
        0.5
        *
        rho
        *
        rho
        *
        theta_prime
        *
        theta_prime
    )

    energy_density = (
        kinetic
        +
        potential
    )

    tension = float(
        simpson(
            energy_density,
            x=z_eval,
        )
    )

    kinetic_int = float(
        simpson(
            kinetic,
            x=z_eval,
        )
    )

    potential_int = float(
        simpson(
            potential,
            x=z_eval,
        )
    )

    active_integral = float(
        simpson(
            -2.0 * potential,
            x=z_eval,
        )
    )

    frozen_sine_gordon_tension = (
        8.0
        *
        m_a
        *
        F
        *
        F
    )

    virial_residual = (
        kinetic_int
        -
        potential_int
    ) / tension

    return {
        "domain_widths": domain_widths,
        "nodes": float(solution.x.size),
        "tension": tension,
        "tension_over_sg": (
            tension
            /
            frozen_sine_gordon_tension
        ),
        "rho_min_over_F": float(
            np.min(rho) / F
        ),
        "active_over_tension": (
            active_integral
            /
            tension
        ),
        "virial_residual": virial_residual,
        "min_potential": float(
            np.min(potential)
        ),
        "min_energy_density": float(
            np.min(energy_density)
        ),
        "max_rms_residual": float(
            np.max(
                solution.rms_residuals
            )
        ),
    }


def scale_match(
    F: float,
    hierarchy: float,
    w_stat: float,
    ell: float,
    q_over_n: float,
    boundary_string_count: int,
    use_tension: float | None = None,
) -> dict[str, float | bool]:
    """Match the microscopic wall to 017P with line-energy bookkeeping."""

    m_a = F / hierarchy
    m_r = F

    sigma_sg = (
        8.0
        *
        m_a
        *
        F
        *
        F
    )

    if use_tension is None:
        sigma = sigma_sg
    else:
        sigma = use_tension

    mu_log_one = (
        math.pi
        *
        F
        *
        F
        *
        math.log(hierarchy)
    )

    mu_log_total = (
        boundary_string_count
        *
        mu_log_one
    )

    w_eff = (
        w_stat
        -
        2.0
        *
        math.pi
        *
        mu_log_total
        /
        ell
    )

    if w_eff <= 0.0:
        return {
            "pass": False,
            "w_eff": w_eff,
            "sigma": sigma,
            "mu_log_total": mu_log_total,
        }

    Q_req = (
        w_eff
        /
        sigma
    )

    N_req = (
        Q_req
        /
        q_over_n
    )

    N_integer = max(
        1,
        int(
            round(N_req)
        ),
    )

    Q_integer = (
        N_integer
        *
        q_over_n
    )

    radius = (
        Q_req
        *
        ell
        /
        (
            2.0
            *
            math.pi
        )
    )

    delta_wall = (
        1.0
        /
        m_a
    )

    delta_core = (
        1.0
        /
        m_r
    )

    integer_load_mismatch = (
        abs(
            sigma
            *
            Q_integer
            -
            w_eff
        )
        /
        w_eff
    )

    remaining_positive_line_budget = (
        w_eff
        *
        ell
        /
        (
            2.0
            *
            math.pi
        )
    )

    scale_pass = (
        radius / delta_wall
        >=
        MIN_SCALE_SEPARATION
        and
        radius / delta_core
        >=
        MIN_SCALE_SEPARATION
        and
        integer_load_mismatch
        <=
        MAX_INTEGER_LOAD_MISMATCH
    )

    return {
        "pass": scale_pass,
        "sigma": sigma,
        "sigma_sg": sigma_sg,
        "mu_log_one": mu_log_one,
        "mu_log_total": mu_log_total,
        "w_eff": w_eff,
        "Q_req": Q_req,
        "N_req": N_req,
        "N_integer": float(N_integer),
        "R_req": radius,
        "R_over_delta_wall": (
            radius
            /
            delta_wall
        ),
        "R_over_delta_core": (
            radius
            /
            delta_core
        ),
        "integer_load_mismatch": (
            integer_load_mismatch
        ),
        "remaining_positive_line_budget": (
            remaining_positive_line_budget
        ),
    }


def robustness_lattice() -> dict[str, float]:
    """Run the conservative +/-10 percent 5^5 scale-matching lattice."""

    levels = (
        0.90,
        0.95,
        1.00,
        1.05,
        1.10,
    )

    total = 0
    passed = 0

    min_w_eff = math.inf
    min_r_over_wall = math.inf
    min_r_over_core = math.inf
    max_integer_mismatch = 0.0
    min_n_req = math.inf

    for (
        f_mult,
        h_mult,
        w_mult,
        ell_mult,
        q_mult,
    ) in itertools.product(
        levels,
        levels,
        levels,
        levels,
        levels,
    ):
        result = scale_match(
            F=F_PHASE * f_mult,
            hierarchy=MASS_HIERARCHY * h_mult,
            w_stat=WALL_LOAD_017P * w_mult,
            ell=ELL_017P * ell_mult,
            q_over_n=Q_OVER_N_017P * q_mult,
            boundary_string_count=BOUNDARY_STRING_COUNT,
        )

        total += 1

        if result["w_eff"] > 0.0:
            min_w_eff = min(
                min_w_eff,
                float(
                    result["w_eff"]
                ),
            )

        if result["pass"]:
            passed += 1

            min_r_over_wall = min(
                min_r_over_wall,
                float(
                    result[
                        "R_over_delta_wall"
                    ]
                ),
            )

            min_r_over_core = min(
                min_r_over_core,
                float(
                    result[
                        "R_over_delta_core"
                    ]
                ),
            )

            max_integer_mismatch = max(
                max_integer_mismatch,
                float(
                    result[
                        "integer_load_mismatch"
                    ]
                ),
            )

            min_n_req = min(
                min_n_req,
                float(
                    result["N_req"]
                ),
            )

    return {
        "total": float(total),
        "passed": float(passed),
        "min_w_eff": min_w_eff,
        "min_r_over_wall": (
            min_r_over_wall
        ),
        "min_r_over_core": (
            min_r_over_core
        ),
        "max_integer_mismatch": (
            max_integer_mismatch
        ),
        "min_n_req": min_n_req,
    }


def main() -> None:
    """Execute topology, microscopic-wall, and scale preflight gates."""

    print(
        "=== ANTIGRAVITY_RESEARCH 018A-1 ==="
    )

    print(
        "QUESTION="
        "NONTHERMAL_STRING_WALL_TOPOLOGY_AND_1D_WALL_PREFLIGHT"
    )

    print(
        "\n=== TOPOLOGY AUDIT ==="
    )

    print(
        "EXACT_017P_BULK_WALL_DEGREE_OF_FREEDOM=ABSENT"
    )

    print(
        "EXACT_017P_FIELD_CONTENT_ALONE_CAN_SUPPLY_MEMBRANE=NO"
    )

    relative_winding_checks = []

    for (
        q1,
        q2,
        flux,
    ) in (
        (1, 1, 1),
        (1, 2, 1),
        (2, 3, 2),
        (3, 5, 4),
    ):
        relative_winding_checks.append(
            same_u1_relative_phase_winding(
                q1,
                q2,
                flux,
            )
        )

    assert all(
        value == 0
        for value
        in relative_winding_checks
    )

    print(
        "NAIVE_SAME_U1_FINITE_ENERGY_RELATIVE_PHASE_WINDING=ZERO"
    )

    print(
        "NAIVE_SAME_U1_RELATIVE_PHASE_WALL_BOUNDARY=REJECTED"
    )

    print(
        "SEPARATE_NDW1_PSEUDOGOLDSTONE_WALL_TOPOLOGY="
        "SUPPORTED_AT_PREFLIGHT"
    )

    print(
        "\n=== 1D MICROSCOPIC WALL BVP ==="
    )

    wall_results = [
        solve_planar_wall(
            F_PHASE,
            MASS_HIERARCHY,
            widths,
        )
        for widths
        in (
            8.0,
            10.0,
            12.0,
            16.0,
        )
    ]

    reference = wall_results[2]

    for result in wall_results:
        print(
            "DOMAIN_WIDTHS={:.0f} "
            "SIGMA={:.15e} "
            "SIGMA_OVER_SG={:.12f} "
            "RHO_MIN_OVER_F={:.12f} "
            "ACTIVE_OVER_SIGMA={:+.12f} "
            "VIRIAL_RESIDUAL={:+.3e} "
            "MAX_RMS_RESIDUAL={:.3e}".format(
                result[
                    "domain_widths"
                ],
                result[
                    "tension"
                ],
                result[
                    "tension_over_sg"
                ],
                result[
                    "rho_min_over_F"
                ],
                result[
                    "active_over_tension"
                ],
                result[
                    "virial_residual"
                ],
                result[
                    "max_rms_residual"
                ],
            )
        )

    sigma_spread = (
        max(
            result["tension"]
            for result
            in wall_results[1:]
        )
        -
        min(
            result["tension"]
            for result
            in wall_results[1:]
        )
    )

    sigma_rel_spread = (
        sigma_spread
        /
        reference["tension"]
    )

    assert (
        sigma_rel_spread
        <
        1.0e-5
    )

    assert (
        abs(
            reference[
                "active_over_tension"
            ]
            +
            1.0
        )
        <
        1.0e-5
    )

    assert (
        abs(
            reference[
                "virial_residual"
            ]
        )
        <
        1.0e-5
    )

    assert (
        reference[
            "min_potential"
        ]
        >
        -1.0e-12
    )

    assert (
        reference[
            "min_energy_density"
        ]
        >
        -1.0e-12
    )

    print(
        "WALL_TENSION_DOMAIN_REL_SPREAD="
        f"{sigma_rel_spread:.12e}"
    )

    print(
        "PLANAR_WALL_BVP=PASS"
    )

    print(
        "PLANAR_WALL_INTEGRATED_ACTIVE_SOURCE_EQUALS_MINUS_TENSION=PASS"
    )

    print(
        "\n=== 017P MICROSCOPIC SCALE MATCH ==="
    )

    matched = scale_match(
        F=F_PHASE,
        hierarchy=MASS_HIERARCHY,
        w_stat=WALL_LOAD_017P,
        ell=ELL_017P,
        q_over_n=Q_OVER_N_017P,
        boundary_string_count=BOUNDARY_STRING_COUNT,
        use_tension=reference[
            "tension"
        ],
    )

    for key in (
        "sigma",
        "mu_log_one",
        "mu_log_total",
        "w_eff",
        "Q_req",
        "N_req",
        "N_integer",
        "R_req",
        "R_over_delta_wall",
        "R_over_delta_core",
        "integer_load_mismatch",
        "remaining_positive_line_budget",
    ):
        print(
            f"{key.upper()}="
            f"{float(matched[key]):.15e}"
        )

    assert matched["pass"]

    print(
        "SELECTED_SCALE_MATCH=PASS"
    )

    print(
        "\n=== +/-10 PERCENT ANALYTIC SCALE ROBUSTNESS ==="
    )

    robustness = (
        robustness_lattice()
    )

    print(
        "ROBUST_TOTAL="
        f"{int(robustness['total'])}"
    )

    print(
        "ROBUST_PASS="
        f"{int(robustness['passed'])}"
    )

    print(
        "ROBUST_MIN_W_EFF="
        f"{robustness['min_w_eff']:.15e}"
    )

    print(
        "ROBUST_MIN_R_OVER_WALL="
        f"{robustness['min_r_over_wall']:.12f}"
    )

    print(
        "ROBUST_MIN_R_OVER_CORE="
        f"{robustness['min_r_over_core']:.12f}"
    )

    print(
        "ROBUST_MAX_INTEGER_LOAD_MISMATCH="
        f"{robustness['max_integer_mismatch']:.15e}"
    )

    print(
        "ROBUST_MIN_N_REQ="
        f"{robustness['min_n_req']:.12f}"
    )

    assert (
        int(
            robustness["passed"]
        )
        ==
        int(
            robustness["total"]
        )
    )

    print(
        "SCALE_ROBUSTNESS_3125_OF_3125=PASS"
    )

    print(
        "\n=== DECISION ==="
    )

    print(
        "EXACT_017P_ONLY_WALL_COMPLETION=RED"
    )

    print(
        "NAIVE_SAME_U1_RELATIVE_PHASE_EXTENSION=RED"
    )

    print(
        "SEPARATE_ZERO_T_NDW1_WALL_PLUS_CORE_BINDING_CLASS="
        "NOT_FALSIFIED"
    )

    print(
        "MANDATORY_GLOBAL_STRING_LOG_ENERGY="
        "INCLUDED_AT_LEADING_LOWER_BOUND"
    )

    print(
        "MICROSCOPIC_JUNCTION_BVP=NOT_YET_SOLVED"
    )

    print(
        "COMPLETE_JUNCTION_GAUGE_STRESS_BOOKKEEPING="
        "NOT_YET_SOLVED"
    )

    print(
        "FINITE_PAYLOAD_GRAVITY_AFTER_JUNCTION="
        "NOT_YET_TESTED"
    )

    print(
        "FULL_018A_GATE=NOT_YET_GREEN"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_018A_TOPOLOGY_AND_1D_WALL_PREFLIGHT"
    )

    print(
        "NEXT="
        "018A_JUNCTION_BVP_AND_COMPLETE_THIN_COMPOSITE_GRAVITY_WITH_017P_EOS"
    )


if __name__ == "__main__":
    main()
