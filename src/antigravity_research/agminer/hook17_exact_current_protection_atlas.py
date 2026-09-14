"""032H17A11A — exact-current / Higgs protection rescue atlas.

PURPOSE
-------
A10F2 produced a sharp result:

    STRICT REDUCED-EFT 1g / 1m PAYLOAD:
        SURVIVES

    CURRENT ORDINARY-DIRAC WHEELER -> MARZO MICROSCOPIC REALIZATION:
        BLOCKED ON ULTRALIGHT SOURCE NATURALNESS

Do not continue expensive finite-payload or nonlinear simulations on that
specific implementation.

Instead test the three lowest-complexity ways of removing the F2
naturalness/longitudinal obstruction.

LANE 1
------
Perturbative Abelian-Higgs completion.

For the standard normalization

    m_V = g v

    m_h = sqrt(2 lambda_H) v

and a conservative perturbativity ceiling

    lambda_H <= 4 pi,

requiring the radial mode to reach at least the electron threshold gives

    g <= sqrt(8 pi) m_V / m_e.

Compare this with the minimum microscopic coupling allowed by the strict
sub-10-MJ source-rest-energy floor.

This closes only the simple perturbative heavy-radial completion.

A very light radial mode, strong coupling, composite Higgs, or a different
Noether completion is NOT closed by this gate.

LANE 2
------
Gauge-invariant dimension-five derivative / Pauli current.

Consider

    L_int
      =
    (1/M) F_V^{mu nu} bar(psi) sigma_{mu nu} psi.

Variation gives an identically conserved current

    J^nu
      ~
    (2/M) partial_mu
    [bar(psi) sigma^{mu nu} psi].

For characteristic source momentum q, give this lane the optimistic effective
coupling

    g_eff <= 2 q/M.

Demanding that the local operator remain valid through the electron threshold
requires

    M >= m_e.

This lane has a useful exact geometry property: the A10F1 compact azimuthal
source profile

    J_phi
      ~
    (rho/R) (1-r^2/R^2)^2

is exactly the curl of the compact magnetization profile

    M_z
      ~
    (R/6) (1-r^2/R^2)^3.

Thus if the lane fails, it fails because of source-strength/EFT scale, not
because the desired transverse source morphology cannot be written as an
identically conserved derivative current.

This closes only the simple local dimension-five portal valid through the
electron threshold.

LANE 3
------
Renormalizable exact ordinary-matter vector current.

For direct vector charges q_e, q_p, q_n, an electrically neutral atom with Z
protons, Z electrons, and N neutrons has

    Q_atom
      =
    Z(q_p + q_e) + N q_n.

If the extra direct vector force must vanish for arbitrary neutral
compositions, then identically

    q_n = 0
    q_p = -q_e.

Thus the one-dimensional ordinary e/p/n conserved-current solution is
electromagnetic-like, up to normalization.

For

    L
      =
    e epsilon V_mu J_EM^mu

the 2026 electron g-2 analysis gives

    Delta a_e
      =
    alpha epsilon^2/(2 pi) F_V(m_V/m_e).

At the one-metre HOOK17 vector mass,

    m_V << m_e

so F_V=1 to extraordinary accuracy.

Use the paper's Rb and Cs electron residuals as separate inputs:

    Rb:
      (35 +/- 16) * 1e-14

    Cs:
      (-100 +/- 26) * 1e-14.

They are inconsistent alternatives and are NOT combined.

The gate derives independent one-sided 95% bounds for both.

ENERGY FLOOR
------------
The A10F2 strict payload result already fixes the required macroscopic field.

If the microscopic source coupling is rescaled from its current constituent
lower-bound value g=1 to a hypothetical exact-current coupling g, the required
source number and source rest energy scale as 1/g while the already-required
classical field energy stays fixed.

Therefore the optimistic source-energy condition is

    E_field + E_e,rest(g=1)/g < 10 MJ.

Solving gives the smallest microscopic coupling compatible with even this
incomplete energy floor.

This is optimistic:

    confinement
    support
    activation
    reaction
    radiation
    UV completion
    nonlinear backreaction

remain omitted.

Therefore failure is meaningful; success would not certify a model.

NEXT FAMILY
-----------
If all three easy repairs fail, do NOT tune them.

Promote a genuinely distinct source/carrier family.

Highest-value immediate target:

    BMS K2 massless protected torsion-vector family
    +
    Wheeler full torsion source
    +
    A10 spin-state engineering.

Reason:

    no ultralight vector mass is required

and therefore the specific A10F2 m_V << m_e mass-naturalness obstruction is
absent at the carrier level.

K3 is NOT automatically reopened: the historical direct clean V24 -> K3 Ward
route is already closed.

K2 must receive its own exact same-action source/Ward/projector test.

CLAIM CLASSIFICATION
--------------------
SCOPED_ANALYTIC_CLOSEOUT_OF_THREE_MINIMAL_SOURCE_PROTECTION_REPAIRS
"""

from __future__ import annotations

import json
import math
from functools import lru_cache
from pathlib import Path
from typing import Any

import sympy as sp


STRICT_COMPLETE_OPERATING_TARGET_J = 1.0e7

ELECTRON_MASS_EV = 510998.95

HBAR_C_EV_M = 1.973269804e-7

ALPHA_EM = 1.0 / 137.035999084

E_EM = math.sqrt(
    4.0
    *
    math.pi
    *
    ALPHA_EM
)

Z95 = 1.645

RB_DELTA_A_E = 35.0e-14
RB_SIGMA_A_E = 16.0e-14

CS_DELTA_A_E = -100.0e-14
CS_SIGMA_A_E = 26.0e-14


def _repo_root() -> Path:
    """Return repository root from src/antigravity_research/agminer."""

    return (
        Path(
            __file__
        )
        .resolve()
        .parents[
            3
        ]
    )


@lru_cache(
    maxsize=1
)
def f2_artifact() -> dict[str, Any]:
    """Load the durable A10F2 result without rerunning its BVP."""

    path = (
        _repo_root()
        /
        "results"
        /
        "data"
        /
        "032h17a10f2_hook17_marzo_source_naturalness_closeout_summary.json"
    )

    if not path.exists():
        raise FileNotFoundError(
            str(
                path
            )
        )

    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


@lru_cache(
    maxsize=1
)
def f2_provenance_gate() -> dict[str, Any]:
    """Require the exact A10F2 scientific state."""

    result = f2_artifact()

    passed = bool(
        result[
            "branch"
        ]
        ==
        "032H17A10F2"

        and

        result[
            "strict_reduced_eft_1g_1m_payload_performance_survives"
        ]
        is True

        and

        result[
            "current_ordinary_dirac_wheeler_marzo_realization_blocked"
        ]
        is True

        and

        result[
            "current_ordinary_dirac_source_technical_naturalness_certified"
        ]
        is False

        and

        result[
            "hook17_closed"
        ]
        is False
    )

    return {
        "pass":
            passed,

        "decision":
            result[
                "decision"
            ],

        "current_full_regression":
            995,

        "strict_reduced_eft_payload_survives":
            result[
                "strict_reduced_eft_1g_1m_payload_performance_survives"
            ],

        "current_wheeler_marzo_realization_blocked":
            result[
                "current_ordinary_dirac_wheeler_marzo_realization_blocked"
            ],

        "hook17_open":
            not result[
                "hook17_closed"
            ],
    }


@lru_cache(
    maxsize=1
)
def optimistic_energy_coupling_floor() -> dict[str, Any]:
    """Return minimum source coupling allowed by the incomplete 10-MJ floor."""

    result = f2_artifact()

    strict = result[
        "strict_payload_floor"
    ]

    field_energy_j = float(
        strict[
            "strict_field_loading_energy_j"
        ]
    )

    electron_rest_at_g1_j = float(
        strict[
            "strict_electron_positron_rest_floor_j"
        ]
    )

    available_source_rest_budget_j = (
        STRICT_COMPLETE_OPERATING_TARGET_J
        -
        field_energy_j
    )

    if available_source_rest_budget_j <= 0.0:
        raise ValueError(
            "field energy alone exhausts the strict energy target"
        )

    minimum_coupling = (
        electron_rest_at_g1_j
        /
        available_source_rest_budget_j
    )

    return {
        "strict_field_energy_j":
            field_energy_j,

        "electron_source_rest_energy_at_constituent_g1_j":
            electron_rest_at_g1_j,

        "available_rest_energy_budget_j":
            available_source_rest_budget_j,

        "minimum_effective_constituent_coupling_for_partial_sub10mj":
            minimum_coupling,

        "exactly_10mj_passes":
            False,

        "complete_energy_established":
            False,

        "floor_is_optimistic":
            True,
    }


@lru_cache(
    maxsize=1
)
def perturbative_heavy_radial_higgs_gate() -> dict[str, Any]:
    """Test standard perturbative Abelian-Higgs protection."""

    f2 = f2_artifact()

    energy = (
        optimistic_energy_coupling_floor()
    )

    vector_mass_ev = abs(
        float(
            f2[
                "stueckelberg_protection"
            ][
                "one_metre_carrier_mass_ev"
            ]
        )
    )

    energy_min_g = float(
        energy[
            "minimum_effective_constituent_coupling_for_partial_sub10mj"
        ]
    )

    lambda_h_max = (
        4.0
        *
        math.pi
    )

    # Standard Abelian-Higgs normalization:
    #
    # mV = g v
    #
    # mh = sqrt(2 lambda_H) v.
    #
    # Requiring mh >= me gives
    #
    # g <= sqrt(2 lambda_H) mV / me.
    higgs_g_max = (
        math.sqrt(
            2.0
            *
            lambda_h_max
        )
        *
        vector_mass_ev
        /
        ELECTRON_MASS_EV
    )

    maximum_radial_mass_at_energy_floor_ev = (
        math.sqrt(
            2.0
            *
            lambda_h_max
        )
        *
        vector_mass_ev
        /
        energy_min_g
    )

    gap = (
        energy_min_g
        /
        higgs_g_max
    )

    overlap = bool(
        higgs_g_max
        >=
        energy_min_g
    )

    return {
        "completion":
            "STANDARD_PERTURBATIVE_ABELIAN_HIGGS",

        "vector_mass_ev":
            vector_mass_ev,

        "quartic_perturbativity_ceiling":
            "lambda_H<=4*pi",

        "lambda_H_max":
            lambda_h_max,

        "radial_threshold_requirement":
            "m_h>=m_e",

        "electron_mass_ev":
            ELECTRON_MASS_EV,

        "maximum_g_with_perturbative_radial_at_or_above_electron_threshold":
            higgs_g_max,

        "energy_minimum_effective_g":
            energy_min_g,

        "energy_to_higgs_coupling_gap":
            gap,

        "maximum_radial_mass_at_energy_floor_g_ev":
            maximum_radial_mass_at_energy_floor_ev,

        "heavy_radial_energy_overlap_exists":
            overlap,

        "simple_perturbative_heavy_radial_higgs_closed":
            not overlap,

        "light_radial_higgs_completion_closed":
            False,

        "strongly_coupled_higgs_completion_closed":
            False,

        "composite_higgs_completion_closed":
            False,
    }


@lru_cache(
    maxsize=1
)
def pauli_source_shape_identity() -> dict[str, Any]:
    """Prove exact curl representation of the finite A10F1 source shape."""

    rho, z, radius = sp.symbols(
        "rho z R",
        positive=True,
        real=True,
    )

    s = (
        rho**2
        +
        z**2
    ) / radius**2

    magnetization_z = (
        radius
        /
        sp.Integer(
            6
        )
        *
        (
            1
            -
            s
        ) ** 3
    )

    curl_phi = sp.factor(
        -sp.diff(
            magnetization_z,
            rho,
        )
    )

    target = sp.factor(
        rho
        /
        radius
        *
        (
            1
            -
            s
        ) ** 2
    )

    identity = bool(
        sp.simplify(
            curl_phi
            -
            target
        )
        ==
        0
    )

    return {
        "magnetization_profile":
            "M_z=(R/6)*(1-r^2/R^2)^3",

        "curl_phi_exact":
            str(
                curl_phi
            ),

        "target_source_shape":
            str(
                target
            ),

        "source_shape_identity_pass":
            identity,

        "derivative_current_identically_conserved":
            True,
    }


@lru_cache(
    maxsize=1
)
def pauli_derivative_current_gate() -> dict[str, Any]:
    """Test optimistic dimension-five exactly conserved derivative source."""

    f2 = f2_artifact()

    energy = (
        optimistic_energy_coupling_floor()
    )

    shape = (
        pauli_source_shape_identity()
    )

    f_ev = abs(
        float(
            f2[
                "stueckelberg_protection"
            ][
                "stueckelberg_f_abs_ev"
            ]
        )
    )

    q_over_f = float(
        f2[
            "longitudinal_diagnostic"
        ][
            "macroscopic_device_source_q_over_f"
        ]
    )

    characteristic_q_ev = (
        q_over_f
        *
        f_ev
    )

    minimum_operator_scale_ev = (
        ELECTRON_MASS_EV
    )

    # Optimistic coefficient for
    #
    # J^nu ~ (2/M) partial_mu Tensor^{mu nu}.
    effective_g_max = (
        2.0
        *
        characteristic_q_ev
        /
        minimum_operator_scale_ev
    )

    energy_min_g = float(
        energy[
            "minimum_effective_constituent_coupling_for_partial_sub10mj"
        ]
    )

    gap = (
        energy_min_g
        /
        effective_g_max
    )

    overlap = bool(
        effective_g_max
        >=
        energy_min_g
    )

    required_operator_scale_for_energy_ev = (
        2.0
        *
        characteristic_q_ev
        /
        energy_min_g
    )

    return {
        "portal":
            "F_V_mn*bar(psi)*sigma^mn*psi/M",

        "source_shape":
            shape,

        "characteristic_source_q_ev":
            characteristic_q_ev,

        "minimum_operator_scale_for_electron_threshold_validity_ev":
            minimum_operator_scale_ev,

        "optimistic_effective_g_max":
            effective_g_max,

        "energy_minimum_effective_g":
            energy_min_g,

        "energy_to_pauli_coupling_gap":
            gap,

        "operator_scale_required_to_reach_energy_floor_ev":
            required_operator_scale_for_energy_ev,

        "operator_scale_required_to_reach_energy_floor_over_electron_mass":
            (
                required_operator_scale_for_energy_ev
                /
                ELECTRON_MASS_EV
            ),

        "energy_eft_overlap_exists":
            overlap,

        "simple_dimension5_pauli_current_valid_through_electron_threshold_closed":
            not overlap,

        "explicit_uv_completion_below_electron_threshold_closed":
            False,
    }


@lru_cache(
    maxsize=1
)
def neutral_ordinary_vector_current_theorem() -> dict[str, Any]:
    """Solve direct-charge silence for arbitrary neutral ordinary matter."""

    q_e, q_p, q_n = sp.symbols(
        "q_e q_p q_n",
        real=True,
    )

    z_number, n_number = sp.symbols(
        "Z N",
        integer=True,
        nonnegative=True,
    )

    atom_charge = sp.expand(
        z_number
        *
        (
            q_p
            +
            q_e
        )
        +
        n_number
        *
        q_n
    )

    # Requiring the polynomial to vanish for arbitrary independent Z,N:
    coefficient_z = sp.expand(
        q_p
        +
        q_e
    )

    coefficient_n = q_n

    solution = {
        str(
            q_n
        ):
            "0",

        str(
            q_p
        ):
            "-q_e",
    }

    return {
        "neutral_atom_charge":
            str(
                atom_charge
            ),

        "coefficient_Z":
            str(
                coefficient_z
            ),

        "coefficient_N":
            str(
                coefficient_n
            ),

        "all_neutral_compositions_directly_silent_requires":
            solution,

        "q_n_zero":
            True,

        "q_p_equals_minus_q_e":
            True,

        "ordinary_e_p_n_solution_dimension":
            1,

        "solution_em_like_up_to_overall_normalization":
            True,

        "non_em_like_direct_charge_silent_for_all_neutral_atoms":
            False,

        "theorem_scope":
            (
                "RENORMALIZABLE_VECTOR_CHARGE_ON_ORDINARY_"
                "ELECTRON_PROTON_NEUTRON_NUMBER_CURRENTS"
            ),
    }


def _low_mass_vector_electron_gminus2_bound(
    *,
    delta_a: float,
    sigma_a: float,
) -> float:
    """Return one-sided 95% |epsilon_e| bound in F_V(0)=1 limit."""

    coefficient = (
        ALPHA_EM
        /
        (
            2.0
            *
            math.pi
        )
    )

    if delta_a >= 0.0:
        q_best = (
            delta_a
            /
            coefficient
        )

        q_upper = (
            (
                delta_a
                +
                Z95
                *
                sigma_a
            )
            /
            coefficient
        )

        if q_upper < q_best:
            raise AssertionError(
                "positive-residual upper bound below best fit"
            )

    else:
        # With physical q=epsilon^2>=0, q_best=0.
        #
        # Solve:
        #
        # [(delta-C q)^2-delta^2]/sigma^2 = z^2.
        y = (
            delta_a
            +
            math.sqrt(
                delta_a**2
                +
                (
                    Z95
                    *
                    sigma_a
                ) ** 2
            )
        )

        q_upper = (
            y
            /
            coefficient
        )

    if q_upper <= 0.0:
        raise AssertionError(
            "nonpositive g-2 q upper limit"
        )

    return math.sqrt(
        q_upper
    )


@lru_cache(
    maxsize=1
)
def em_like_exact_current_gminus2_gate() -> dict[str, Any]:
    """Test the unique neutral-composition-silent ordinary vector current."""

    energy = (
        optimistic_energy_coupling_floor()
    )

    theorem = (
        neutral_ordinary_vector_current_theorem()
    )

    minimum_direct_electron_coupling = float(
        energy[
            "minimum_effective_constituent_coupling_for_partial_sub10mj"
        ]
    )

    epsilon_energy_min = (
        minimum_direct_electron_coupling
        /
        E_EM
    )

    epsilon_rb_95 = (
        _low_mass_vector_electron_gminus2_bound(
            delta_a=
                RB_DELTA_A_E,

            sigma_a=
                RB_SIGMA_A_E,
        )
    )

    epsilon_cs_95 = (
        _low_mass_vector_electron_gminus2_bound(
            delta_a=
                CS_DELTA_A_E,

            sigma_a=
                CS_SIGMA_A_E,
        )
    )

    direct_g_rb_95 = (
        E_EM
        *
        epsilon_rb_95
    )

    direct_g_cs_95 = (
        E_EM
        *
        epsilon_cs_95
    )

    rb_gap = (
        epsilon_energy_min
        /
        epsilon_rb_95
    )

    cs_gap = (
        epsilon_energy_min
        /
        epsilon_cs_95
    )

    rb_overlap = bool(
        epsilon_energy_min
        <=
        epsilon_rb_95
    )

    cs_overlap = bool(
        epsilon_energy_min
        <=
        epsilon_cs_95
    )

    return {
        "ordinary_current_theorem":
            theorem,

        "interaction":
            "e*epsilon*V_mu*J_EM^mu",

        "vector_mass_over_electron_mass":
            (
                HBAR_C_EV_M
                /
                ELECTRON_MASS_EV
            ),

        "low_mass_loop_function_FV":
            1.0,

        "low_mass_approximation_error_material":
            False,

        "electron_vector_coupling_energy_min":
            minimum_direct_electron_coupling,

        "electromagnetic_coupling_e":
            E_EM,

        "epsilon_energy_min":
            epsilon_energy_min,

        "rb_delta_a_e":
            RB_DELTA_A_E,

        "rb_sigma_a_e":
            RB_SIGMA_A_E,

        "cs_delta_a_e":
            CS_DELTA_A_E,

        "cs_sigma_a_e":
            CS_SIGMA_A_E,

        "rb_cs_treated_as_alternative_inputs_not_combined":
            True,

        "epsilon_rb_95":
            epsilon_rb_95,

        "epsilon_cs_95":
            epsilon_cs_95,

        "direct_electron_g_rb_95":
            direct_g_rb_95,

        "direct_electron_g_cs_95":
            direct_g_cs_95,

        "energy_to_rb_bound_gap":
            rb_gap,

        "energy_to_cs_bound_gap":
            cs_gap,

        "rb_energy_overlap_exists":
            rb_overlap,

        "cs_energy_overlap_exists":
            cs_overlap,

        "minimal_em_like_exact_current_rescue_closed_by_electron_gminus2":
            bool(
                not rb_overlap
                and
                not cs_overlap
            ),

        "source_only_hidden_current_closed":
            False,

        "nonstandard_noether_current_closed":
            False,
    }


@lru_cache(
    maxsize=1
)
def h17a11a_summary() -> dict[str, Any]:
    """Return scoped three-lane exact-current protection closeout."""

    provenance = (
        f2_provenance_gate()
    )

    energy = (
        optimistic_energy_coupling_floor()
    )

    higgs = (
        perturbative_heavy_radial_higgs_gate()
    )

    pauli = (
        pauli_derivative_current_gate()
    )

    em_like = (
        em_like_exact_current_gminus2_gate()
    )

    three_easy_repairs_closed = bool(
        provenance[
            "pass"
        ]
        and
        higgs[
            "simple_perturbative_heavy_radial_higgs_closed"
        ]
        and
        pauli[
            "simple_dimension5_pauli_current_valid_through_electron_threshold_closed"
        ]
        and
        em_like[
            "minimal_em_like_exact_current_rescue_closed_by_electron_gminus2"
        ]
    )

    decision = (
        (
            "RED_SCOPED_A11A_THREE_MINIMAL_SOURCE_PROTECTION_REPAIRS_CLOSED__"
            "PROMOTE_GENUINELY_NEW_MASSLESS_K2_TORSION_VECTOR_SOURCE_GATE"
        )
        if three_easy_repairs_closed
        else
        "YELLOW_A11A_ONE_OR_MORE_MINIMAL_PROTECTION_LANES_REMAIN_OPEN"
    )

    return {
        "branch":
            "032H17A11A",

        "decision":
            decision,

        "current_full_regression_before_a11a":
            995,

        "a10f2_provenance":
            provenance,

        "optimistic_energy_coupling_floor":
            energy,

        "perturbative_heavy_radial_higgs":
            higgs,

        "pauli_derivative_exact_current":
            pauli,

        "em_like_exact_ordinary_current":
            em_like,

        "three_minimal_source_protection_repairs_closed":
            three_easy_repairs_closed,

        "ordinary_dirac_wheeler_marzo_realization_remains_closed":
            True,

        "all_higgsed_noether_completions_closed":
            False,

        "all_exact_conserved_current_completions_closed":
            False,

        "all_derivative_composite_currents_closed":
            False,

        "all_standard_model_source_currents_closed":
            False,

        "k3_historical_direct_clean_source_route_reopened":
            False,

        "k2_massless_torsion_vector_previously_tested_as_exact_a10_source_gate":
            False,

        "k2_specific_ultralight_mass_naturalness_obstruction_present":
            False,

        "k2_source_ward_projector_overlap_established":
            False,

        "k2_same_action_quadratic_metric_established":
            False,

        "hook17_mechanism_knowledge_preserved":
            True,

        "hook17_closed":
            False,

        "physical_antigravity_model_found":
            False,

        "certified_sub10mj_model_found":
            False,

        "complete_energy_established":
            False,

        "expensive_payload_run_authorized":
            False,

        "next":
            (
                "032H17A11B_K2_MASSLESS_TORSION_VECTOR_"
                "ENGINEERED_DIRAC_EXACT_SOURCE_WARD_PROJECTOR_GATE"
                if three_easy_repairs_closed
                else
                "REVIEW_SURVIVING_A11A_PROTECTION_LANE"
            ),

        "stop_rule":
            (
                "DO_NOT_REOPEN_K3_CLEAN_ROUTE;_"
                "IF_K2_EXACT_SOURCE_WARD_OR_HEALTHY_PROJECTOR_IS_ZERO_"
                "CLOSE_K2_DIRECT_ROUTE_BEFORE_ANY_METRIC_OR_PAYLOAD_WORK"
            ),
    }
