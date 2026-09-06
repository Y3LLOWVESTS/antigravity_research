"""032V17 axial vacuum/canonicalization and finite-payload backreaction gate.

This run performs four corrections to the V16 prefield state:

1. repair the scalar contribution to the Laue trace support lower bound;
2. match the outward kinetic-conformal target to the published j=0 C1 operator;
3. replace the uniform-sphere transmission scout with an exact spherical-payload
   multipole solution for the actual V15 spheroidal source geometry;
4. quantify whether fixed-order axial-source wavefunction running is small enough
   to justify canonicalizing the source EFT without UV matching.

The low-M payload result is a partial scaling corridor, not a complete energy
oracle. The renormalized Dirac sea, UV matching, confinement, activation,
nonlinear stability, and full empirical closure remain open.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from scipy.optimize import minimize_scalar

from antigravity_research.agminer.axial_dirac_meanfield import (
    payload_trace_load,
    physicalize_dimensionless_state,
    spheroid_demag_z,
)
from antigravity_research.agminer.c1_payload_matching import (
    axial_leading_log_wavefunction_proxy,
    c1_from_metric_scale_ev,
    corrected_laue_trace_support_floor_j,
    jiang_nda_scale_from_c1_ev,
    payload_surface_acceleration_metrics,
    payload_volume_average_acceleration_m_s2,
    required_q2_for_payload_surface,
    source_feedback_metrics,
    spheroid_incident_legendre_coefficients,
    static_outward_metric_sign_from_c1,
)
from antigravity_research.agminer.candidate import Candidate
from antigravity_research.agminer.normalization import (
    canonical_invariant_fingerprint,
)
from antigravity_research.agminer.oracle import (
    ActionOracle,
    LEDGER_PARTIAL_OPTIMISTIC,
    assess_oracle,
)
from antigravity_research.agminer.policy import current_energy_policy
from antigravity_research.agminer.reporting import rebuild_summaries
from antigravity_research.agminer.storage import Storage


ROOT = Path(__file__).resolve().parents[1]

V15 = (
    ROOT
    / "results"
    / "data"
    / "032v15_axial_shift_source_morphology_summary.json"
)

V16 = (
    ROOT
    / "results"
    / "data"
    / "032v16_axial_dirac_meanfield_self_consistency_summary.json"
)

OUT = (
    ROOT
    / "results"
    / "data"
    / "032v17_c1_payload_quantum_control_summary.json"
)

SCALE_OUT = (
    ROOT
    / "results"
    / "data"
    / "032v17_exact_payload_scale_scan.csv"
)

LOOP_OUT = (
    ROOT
    / "results"
    / "data"
    / "032v17_axial_leading_log_scan.csv"
)

DB = ROOT / "results" / "agminer" / "agminer.sqlite3"

TARGET_J = 1.0e7
G = 9.80665

PAYLOAD_MASS_KG = 1.0
PAYLOAD_RADIUS_M = 0.10
PAYLOAD_CENTER_Z_M = 0.20

DIRECT_C1_CONTEXT_BOUND_EV_M4 = 1.0e-10
REFERENCE_SCALE_EV = 1.0e5


policy = current_energy_policy()

assert float(policy["limit_j"]) == TARGET_J
assert str(policy["comparison"]) == "LT"
assert str(policy["policy_id"]) == "ENERGY_ab8c16e45c837ffc"

assert V15.exists()
assert V16.exists()

v15 = json.loads(V15.read_text(encoding="utf-8"))
v16 = json.loads(V16.read_text(encoding="utf-8"))

assert (
    v16["decision"]
    ==
    "RED_V15_MINIMAL_SINGLE_FLAVOR_MEANFIELD_"
    "RED_CONTROLLED_NR_SPONTANEOUS_POLARIZATION_"
    "GREEN_RELATIVISTIC_POSITIVE_BAND_LOOP030_PARTIAL_CORRIDOR_"
    "VACUUM_CANONICALIZATION_REQUIRED"
)

morph = v15["optimized_morphology"]
selected = v16["selected_positive_band_partial_corridor"]

source_a_m = float(morph["a_m"])
source_c_m = float(morph["c_m"])
q_reference = float(morph["q"])

demag_z = spheroid_demag_z(source_a_m, source_c_m)

assert math.isclose(
    demag_z,
    0.6050030448888295,
    rel_tol=2.0e-13,
)

field_reference_j = float(selected["field_energy_j"])
band_reference_j = float(selected["occupied_band_energy_j"])
pressure_mean_reference_j = float(selected["pressure_mean_inventory_j"])
old_support_reference_j = float(selected["laue_support_floor_j"])
old_partial_reference_j = float(selected["partial_conservative_floor_j"])

corrected_support_reference_j = corrected_laue_trace_support_floor_j(
    fermion_mean_pressure_inventory_j=pressure_mean_reference_j,
    scalar_field_energy_j=field_reference_j,
)

corrected_vacuum_partial_reference_j = (
    band_reference_j
    + field_reference_j
    + corrected_support_reference_j
)

ledger_correction_j = (
    corrected_vacuum_partial_reference_j
    - old_partial_reference_j
)

assert corrected_support_reference_j > old_support_reference_j
assert corrected_vacuum_partial_reference_j < TARGET_J

c1_reference = c1_from_metric_scale_ev(REFERENCE_SCALE_EV)

assert static_outward_metric_sign_from_c1(c1_reference)

c1_operator_status = {
    "published_dimension8_operator": True,
    "sector": "J0_SCALAR",
    "leading_forward_s2_positivity_constrains_c1": False,
    "one_loop_qed_c1_generates_c3": False,
    "positive_c1_outward_static_sign": True,
    "complete_uv_matching_for_pure_c1": False,
    "known_positive_c1_uv_sign_example": True,
    "known_example_has_c2_over_c1": 12.0,
    "known_example_has_c4_over_c1": -12.0,
    "known_spin2_example_promoted": False,
}

loop_rows = []

for row in v16["loop_energy_pareto"]:
    loop_proxy = float(row["loop_proxy"])
    f_ev = float(row["f_psi_ev"])
    mass_ev = float(row["m_psi_ev"])
    cutoff_ev = 4.0 * math.pi * f_ev

    leading_log = axial_leading_log_wavefunction_proxy(
        loop_proxy=loop_proxy,
        cutoff_ev=cutoff_ev,
        mass_ev=mass_ev,
    )

    loop_rows.append(
        {
            "loop_cap": float(row["loop_cap"]),
            "loop_proxy": loop_proxy,
            "f_psi_ev": f_ev,
            "mass_ev": mass_ev,
            "cutoff_ev": cutoff_ev,
            "leading_log_delta_z_proxy": leading_log,
            "fixed_order_small_lt1": leading_log < 1.0,
            "renormalized_physical_z": False,
        }
    )

selected_loop_proxy = float(selected["loop_proxy"])
selected_cutoff_ev = float(selected["nda_cutoff_ev"])
selected_mass_ev = float(selected["m_psi_ev"])

selected_leading_log = axial_leading_log_wavefunction_proxy(
    loop_proxy=selected_loop_proxy,
    cutoff_ev=selected_cutoff_ev,
    mass_ev=selected_mass_ev,
)

fixed_order_quantum_control = selected_leading_log < 1.0

assert fixed_order_quantum_control is False
assert all(
    float(row["leading_log_delta_z_proxy"]) > 1.0
    for row in loop_rows
)

coefficients = spheroid_incident_legendre_coefficients(
    a_m=source_a_m,
    c_m=source_c_m,
    payload_center_z_m=PAYLOAD_CENTER_Z_M,
    fit_radius_m=PAYLOAD_RADIUS_M,
    lmax=20,
    n_t=56,
    n_phi=84,
    fit_order=180,
)

vacuum_requirement = required_q2_for_payload_surface(
    coefficients=coefficients,
    epsilon_trace_load=0.0,
    payload_radius_m=PAYLOAD_RADIUS_M,
    target_acceleration_m_s2=G,
    surface_count=1601,
)

vacuum_q_reconstructed = math.sqrt(float(vacuum_requirement["q2"]))

vacuum_q_relerr = abs(
    vacuum_q_reconstructed
    - q_reference
) / q_reference

assert vacuum_q_relerr < 1.0e-8


def exact_partial_energy_for_scale(
    metric_scale_ev: float,
    *,
    coefficient_array=coefficients,
    surface_count: int = 1001,
):
    scale = float(metric_scale_ev)

    trace = payload_trace_load(
        payload_mass_kg=PAYLOAD_MASS_KG,
        payload_radius_m=PAYLOAD_RADIUS_M,
        metric_scale_ev=scale,
    )

    epsilon = float(trace["epsilon_trace_load"])

    requirement = required_q2_for_payload_surface(
        coefficients=coefficient_array,
        epsilon_trace_load=epsilon,
        payload_radius_m=PAYLOAD_RADIUS_M,
        target_acceleration_m_s2=G,
        surface_count=surface_count,
    )

    q2_required = float(requirement["q2"])
    q2_factor = q2_required / q_reference**2

    partial_energy_j = (
        corrected_vacuum_partial_reference_j
        * (scale / REFERENCE_SCALE_EV) ** 4
        * q2_factor
    )

    return {
        "metric_scale_ev": scale,
        "epsilon_trace_load": epsilon,
        "q2_required": q2_required,
        "q2_factor_from_vacuum_source": q2_factor,
        "partial_energy_j": partial_energy_j,
        "limiting_surface_cosine": float(
            requirement["limiting_surface_cosine"]
        ),
    }


optimization = minimize_scalar(
    lambda scale: exact_partial_energy_for_scale(
        scale,
        surface_count=801,
    )["partial_energy_j"],
    bounds=(1.0e4, 1.0e5),
    method="bounded",
    options={
        "xatol": 1.0e-5,
    },
)

optimal_scale_ev = float(optimization.x)

optimal = exact_partial_energy_for_scale(
    optimal_scale_ev,
    surface_count=1601,
)

optimal_q2 = float(optimal["q2_required"])
optimal_q = math.sqrt(optimal_q2)
optimal_energy_j = float(optimal["partial_energy_j"])
optimal_epsilon = float(optimal["epsilon_trace_load"])

assert optimal_energy_j < TARGET_J

optimal_l16 = exact_partial_energy_for_scale(
    optimal_scale_ev,
    coefficient_array=coefficients[:17],
    surface_count=1601,
)

multipole_q2_relerr = abs(
    float(optimal_l16["q2_required"])
    - optimal_q2
) / optimal_q2

assert multipole_q2_relerr < 1.0e-5

surface_metrics = payload_surface_acceleration_metrics(
    coefficients=coefficients,
    epsilon_trace_load=optimal_epsilon,
    payload_radius_m=PAYLOAD_RADIUS_M,
    q2=optimal_q2,
    surface_count=1601,
)

payload_cm_20 = payload_volume_average_acceleration_m_s2(
    coefficients=coefficients,
    epsilon_trace_load=optimal_epsilon,
    payload_radius_m=PAYLOAD_RADIUS_M,
    q2=optimal_q2,
    order=20,
)

payload_cm_24 = payload_volume_average_acceleration_m_s2(
    coefficients=coefficients,
    epsilon_trace_load=optimal_epsilon,
    payload_radius_m=PAYLOAD_RADIUS_M,
    q2=optimal_q2,
    order=24,
)

payload_cm_relerr = abs(
    payload_cm_24
    - payload_cm_20
) / payload_cm_24

assert float(surface_metrics["surface_min_m_s2"]) >= G * (1.0 - 2.0e-12)
assert payload_cm_24 >= G
assert payload_cm_relerr < 1.0e-9

feedback = source_feedback_metrics(
    coefficients=coefficients,
    epsilon_trace_load=optimal_epsilon,
    payload_radius_m=PAYLOAD_RADIUS_M,
    payload_center_z_m=PAYLOAD_CENTER_Z_M,
    source_a_m=source_a_m,
    source_c_m=source_c_m,
    source_demag_z=demag_z,
    surface_count=401,
)

assert float(feedback["source_surface_max_feedback_ratio"]) < 0.05

optimal_c1 = c1_from_metric_scale_ev(optimal_scale_ev)
optimal_jiang_nda_scale_ev = jiang_nda_scale_from_c1_ev(optimal_c1)

direct_context_ratio = (
    DIRECT_C1_CONTEXT_BOUND_EV_M4
    / abs(optimal_c1)
)

assert optimal_c1 < DIRECT_C1_CONTEXT_BOUND_EV_M4

r_mass_over_b = float(selected["r_mass_over_b"])
u_mu_over_b = float(selected["u_mu_over_b"])
flavors = int(selected["flavors"])

optimal_physical_source = physicalize_dimensionless_state(
    q=optimal_q,
    metric_scale_ev=optimal_scale_ev,
    demag_z=demag_z,
    r_mass_over_b=r_mass_over_b,
    u_mu_over_b=u_mu_over_b,
    flavors=flavors,
    order=96,
)

optimal_leading_log = axial_leading_log_wavefunction_proxy(
    loop_proxy=selected_loop_proxy,
    cutoff_ev=float(optimal_physical_source["nda_cutoff_ev"]),
    mass_ev=float(optimal_physical_source["m_psi_ev"]),
)

assert math.isclose(
    optimal_leading_log,
    selected_leading_log,
    rel_tol=2.0e-10,
)

scale_rows = []

for scale_ev in (
    1.0e5,
    8.0e4,
    5.0e4,
    4.0e4,
    3.0e4,
    optimal_scale_ev,
    2.0e4,
    1.5e4,
    1.0e4,
):
    state = exact_partial_energy_for_scale(
        scale_ev,
        surface_count=1201,
    )

    local_feedback = source_feedback_metrics(
        coefficients=coefficients,
        epsilon_trace_load=float(state["epsilon_trace_load"]),
        payload_radius_m=PAYLOAD_RADIUS_M,
        payload_center_z_m=PAYLOAD_CENTER_Z_M,
        source_a_m=source_a_m,
        source_c_m=source_c_m,
        source_demag_z=demag_z,
        surface_count=201,
    )

    scale_rows.append(
        {
            **state,
            "c1_ev_m4": c1_from_metric_scale_ev(scale_ev),
            "jiang_nda_scale_ev": jiang_nda_scale_from_c1_ev(
                c1_from_metric_scale_ev(scale_ev)
            ),
            "source_center_feedback_ratio": local_feedback[
                "source_center_feedback_ratio"
            ],
            "source_surface_max_feedback_ratio": local_feedback[
                "source_surface_max_feedback_ratio"
            ],
            "under_strict_10mj_partial_only": float(
                state["partial_energy_j"]
            ) < TARGET_J,
            "trusted_complete_energy_oracle": False,
        }
    )

storage = Storage(DB)

fixed_order_candidate = Candidate(
    family_id="032_KINETIC_CONFORMAL_AXIAL_DIRAC_MEANFIELD",
    family_version="V17_FIXED_ORDER_LOOP030_CANONICALIZATION_V1",
    params={
        "loop_proxy": selected_loop_proxy,
        "delta_z_ll_proxy": selected_leading_log,
    },
    physical_model_version="AXIAL_DIRAC_FIXED_ORDER_RUNNING_INTERPRETATION",
    energy_ledger_version="QUANTUM_CONTROL_GATE_ONLY_V1",
)

storage.record_candidate(
    fixed_order_candidate,
    state="TIER0_RUNNING",
    tier=0,
    run_id="032V17",
)

storage.reject(
    fixed_order_candidate.candidate_id,
    state="REJECTED_NATURALNESS",
    failure_code="N006",
    gate="axial_fixed_order_wavefunction_running_control",
    energy_j=optimal_energy_j,
    run_id="032V17",
)

low_m_candidate = Candidate(
    family_id="032_KINETIC_CONFORMAL_C1_EXACT_PAYLOAD_CORRIDOR",
    family_version="V17_L20_PAYLOAD_MATCH_V1",
    params={
        "metric_scale_ev": optimal_scale_ev,
        "c1_ev_m4": optimal_c1,
        "q": optimal_q,
        "epsilon_trace_load": optimal_epsilon,
        "source_feedback_surface_max": feedback[
            "source_surface_max_feedback_ratio"
        ],
    },
    physical_model_version="PUBLISHED_C1_LINEAR_MATCH_WITH_EXACT_SPHERICAL_PAYLOAD",
    energy_ledger_version="CORRECTED_TRACE_PARTIAL_SCALING_LEDGER_V1",
)

storage.record_candidate(
    low_m_candidate,
    state="PREFIELD_UV_MATCHING_BLOCKED",
    tier=0,
    run_id="032V17",
)

canonical_id = canonical_invariant_fingerprint(
    family_id=low_m_candidate.family_id,
    family_version=low_m_candidate.family_version,
    invariants={
        "published_operator": "JIANG_O1_J0",
        "metric_matching": "C1_EQUALS_1_OVER_2M4",
        "payload_multipole_lmax": 20,
        "loop_proxy": selected_loop_proxy,
        "renormalized_canonical_z_fixed": False,
    },
)

oracle = ActionOracle(
    canonical_invariant_id=canonical_id,
    proof_reference="032V17_EXACT_PAYLOAD_PARTIAL_CORRIDOR",
    relaxed_complete_energy_j=optimal_energy_j,
    ledger_scope=LEDGER_PARTIAL_OPTIMISTIC,
    normalization_invariant=False,
    naturalness_screened=False,
    universal_metric_screened=True,
)

assessment = assess_oracle(oracle)

assert oracle.trusted_for_reachability is False

storage.record_action_oracle(
    low_m_candidate.candidate_id,
    oracle,
)

reporting = rebuild_summaries(
    storage,
    ROOT / "results" / "agminer",
)

storage.close()

with SCALE_OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=list(scale_rows[0].keys()),
    )
    writer.writeheader()
    writer.writerows(scale_rows)

with LOOP_OUT.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=list(loop_rows[0].keys()),
    )
    writer.writeheader()
    writer.writerows(loop_rows)

decision = (
    "GREEN_PUBLISHED_C1_OUTWARD_EFT_MATCH_"
    "GREEN_EXACT_FINITE_PAYLOAD_LOWM_PARTIAL_CORRIDOR_"
    "RED_FIXED_ORDER_AXIAL_CANONICALIZATION_CONTROL_"
    "UV_MATCHING_REQUIRED"
)

next_step = (
    "032V18_C1_UV_MATCHING_RG_AND_COMPLETE_SOURCE_SUPPORT_GATE"
)

summary = {
    "branch":
        "032V17_AXIAL_VACUUM_CANONICALIZATION_AND_PAYLOAD_BACKREACTION_GATE",

    "claim_class":
        "PUBLISHED_OPERATOR_MATCH_EXACT_LINEAR_PAYLOAD_AND_QUANTUM_CONTROL_GATE",

    "energy_policy_id":
        str(policy["policy_id"]),

    "v16_ledger_repair": {
        "old_support_floor_j": old_support_reference_j,
        "corrected_scalar_trace_support_floor_j": corrected_support_reference_j,
        "ledger_correction_j": ledger_correction_j,
        "old_partial_reference_j": old_partial_reference_j,
        "corrected_vacuum_partial_reference_j": corrected_vacuum_partial_reference_j,
        "reason": "CANONICAL_STATIC_SCALAR_SPATIAL_TRACE_EQUALS_MINUS_FIELD_ENERGY",
    },

    "published_c1_matching": {
        **c1_operator_status,
        "reference": "Jiang_et_al_JHEP08_2024_114_arXiv2404.17636",
        "c1_at_100kev_ev_m4": c1_reference,
        "metric_match": "A_EQUALS_1_MINUS_C1_DPHI2",
        "static_match": "A_EQUALS_1_PLUS_GRADPHI2_OVER_2M4",
        "direct_c1_context_bound_ev_m4": DIRECT_C1_CONTEXT_BOUND_EV_M4,
        "direct_bound_assumption_matches_engineered_source": False,
    },

    "axial_quantum_control": {
        "selected_loop_proxy": selected_loop_proxy,
        "selected_leading_log_delta_z_proxy": selected_leading_log,
        "fixed_order_delta_z_small_lt1": fixed_order_quantum_control,
        "renormalized_physical_z_computed": False,
        "dirac_sea_finite_effective_action_computed": False,
        "rg_resummation_or_uv_matching_required": True,
        "leading_log_is_energy_multiplier": False,
    },

    "exact_payload": {
        "multipole_lmax": 20,
        "vacuum_q_reconstruction_relerr": vacuum_q_relerr,
        "l16_l20_q2_relerr_at_optimum": multipole_q2_relerr,
        "optimal_metric_scale_ev": optimal_scale_ev,
        "optimal_epsilon_trace_load": optimal_epsilon,
        "optimal_q": optimal_q,
        "optimal_q2_factor_from_vacuum_source": optimal[
            "q2_factor_from_vacuum_source"
        ],
        "partial_energy_j": optimal_energy_j,
        "complete_operating_energy": False,
        "surface_min_m_s2": surface_metrics["surface_min_m_s2"],
        "surface_max_m_s2": surface_metrics["surface_max_m_s2"],
        "surface_nonuniformity": surface_metrics["surface_nonuniformity"],
        "payload_cm_volume_average_m_s2": payload_cm_24,
        "payload_cm_quadrature_relerr": payload_cm_relerr,
        "source_center_feedback_ratio": feedback[
            "source_center_feedback_ratio"
        ],
        "source_surface_max_feedback_ratio": feedback[
            "source_surface_max_feedback_ratio"
        ],
        "full_coupled_source_payload_solution": False,
    },

    "optimal_eft_context": {
        "c1_ev_m4": optimal_c1,
        "jiang_nda_scale_ev": optimal_jiang_nda_scale_ev,
        "direct_context_bound_to_candidate_ratio": direct_context_ratio,
        "direct_context_excludes_candidate": False,
        "direct_context_is_exact_engineered_constraint": False,
        "flavors": flavors,
        "f_psi_ev": optimal_physical_source["f_psi_ev"],
        "axial_b_ev": optimal_physical_source["axial_b_ev"],
        "m_psi_ev": optimal_physical_source["m_psi_ev"],
        "chemical_potential_ev": optimal_physical_source[
            "chemical_potential_ev"
        ],
        "nda_cutoff_ev": optimal_physical_source["nda_cutoff_ev"],
        "hard_scale_margin": optimal_physical_source["hard_scale_margin"],
        "leading_log_delta_z_proxy": optimal_leading_log,
    },

    "known_uv_example_status": {
        "positive_c1_sign_example_exists": True,
        "example_generates_c2_equals_12c1": True,
        "example_generates_c4_equals_minus12c1": True,
        "example_implementation_used_here": False,
        "reason_not_promoted":
            "COMPANION_J2_OPERATORS_AND_CLOSED_MASSIVE_SPIN2_IMPLEMENTATION_CLASS",
    },

    "open_gates": [
        "RENORMALIZED_AXIAL_DIRAC_VACUUM",
        "RG_RESUMMED_OR_UV_MATCHED_SCALAR_CANONICAL_NORMALIZATION",
        "C1_UV_MATCH_WITHOUT_FATAL_COMPANION_OPERATORS",
        "FULL_COUPLED_SOURCE_PAYLOAD_REACTION",
        "CONSTRUCTED_POSITIVE_ENERGY_SUPPORT_AND_CONFINEMENT",
        "ACTIVATION_CONTROL_AND_RESET",
        "NONLINEAR_STABILITY",
        "FULL_EMPIRICAL_EP_FIFTH_FORCE_ASTRO_COSMO",
        "FULL_METRIC_BACKREACTION",
    ],

    "agminer": {
        "fixed_order_rejection_candidate_id":
            fixed_order_candidate.candidate_id,
        "low_m_partial_oracle_candidate_id":
            low_m_candidate.candidate_id,
        "low_m_oracle_priority":
            assessment.priority,
        "trusted_for_reachability":
            False,
        "mechanism_metrics_recorded":
            False,
        "reporting":
            reporting,
    },

    "physical_antigravity_model_found":
        False,

    "certified_sub10mj_model_found":
        False,

    "decision":
        decision,

    "next":
        next_step,
}

OUT.write_text(
    json.dumps(
        summary,
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
)

print("=== 032V17 RESULT ===")
print("ENERGY_POLICY_ID=" + str(policy["policy_id"]))
print("PUBLISHED_C1_J0_OPERATOR=YES")
print("C1_POSITIVE_STATIC_OUTWARD_SIGN=YES")
print("C1_LEADING_FORWARD_POSITIVITY_KILL=False")
print("C1_ONELOOP_QED_GENERATES_C3=False")
print("PURE_C1_UV_COMPLETION_PROVED=False")

print(
    "V16_OLD_SUPPORT_KJ="
    + format(
        old_support_reference_j / 1.0e3,
        ".12e",
    )
)

print(
    "V16_CORRECTED_TRACE_SUPPORT_KJ="
    + format(
        corrected_support_reference_j / 1.0e3,
        ".12e",
    )
)

print(
    "V16_CORRECTED_VACUUM_PARTIAL_MJ="
    + format(
        corrected_vacuum_partial_reference_j / 1.0e6,
        ".12e",
    )
)

print(
    "SELECTED_LEADING_LOG_DELTAZ_PROXY="
    + format(
        selected_leading_log,
        ".12e",
    )
)

print("FIXED_ORDER_ONELOOP_CANONICALIZATION_CONTROL=RED")
print("LEADING_LOG_IS_ENERGY_MULTIPLIER=False")

print(
    "EXACT_PAYLOAD_OPTIMUM_SCALE_KEV="
    + format(
        optimal_scale_ev / 1.0e3,
        ".12e",
    )
)

print(
    "EXACT_PAYLOAD_OPTIMUM_EPSILON="
    + format(
        optimal_epsilon,
        ".12e",
    )
)

print(
    "EXACT_PAYLOAD_Q2_FACTOR="
    + format(
        float(
            optimal["q2_factor_from_vacuum_source"]
        ),
        ".12e",
    )
)

print(
    "EXACT_PAYLOAD_PARTIAL_KJ="
    + format(
        optimal_energy_j / 1.0e3,
        ".12e",
    )
)

print(
    "PAYLOAD_SURFACE_MIN_M_S2="
    + format(
        float(
            surface_metrics["surface_min_m_s2"]
        ),
        ".12e",
    )
)

print(
    "PAYLOAD_SURFACE_MAX_M_S2="
    + format(
        float(
            surface_metrics["surface_max_m_s2"]
        ),
        ".12e",
    )
)

print(
    "PAYLOAD_SURFACE_NONUNIFORMITY="
    + format(
        float(
            surface_metrics["surface_nonuniformity"]
        ),
        ".12e",
    )
)

print(
    "PAYLOAD_CM_VOLUME_AVERAGE_M_S2="
    + format(
        payload_cm_24,
        ".12e",
    )
)

print(
    "PAYLOAD_CM_QUADRATURE_RELERR="
    + format(
        payload_cm_relerr,
        ".12e",
    )
)

print(
    "MULTIPOLE_L16_L20_Q2_RELERR="
    + format(
        multipole_q2_relerr,
        ".12e",
    )
)

print(
    "SOURCE_CENTER_FEEDBACK_RATIO="
    + format(
        float(
            feedback["source_center_feedback_ratio"]
        ),
        ".12e",
    )
)

print(
    "SOURCE_SURFACE_MAX_FEEDBACK_RATIO="
    + format(
        float(
            feedback["source_surface_max_feedback_ratio"]
        ),
        ".12e",
    )
)

print(
    "OPTIMAL_C1_EV_M4="
    + format(
        optimal_c1,
        ".12e",
    )
)

print(
    "OPTIMAL_JIANG_NDA_SCALE_KEV="
    + format(
        optimal_jiang_nda_scale_ev / 1.0e3,
        ".12e",
    )
)

print(
    "DIRECT_CONTEXT_BOUND_TO_CANDIDATE_RATIO="
    + format(
        direct_context_ratio,
        ".12e",
    )
)

print(
    "OPTIMAL_F_PSI_EV="
    + format(
        float(
            optimal_physical_source["f_psi_ev"]
        ),
        ".12e",
    )
)

print(
    "OPTIMAL_M_PSI_EV="
    + format(
        float(
            optimal_physical_source["m_psi_ev"]
        ),
        ".12e",
    )
)

print(
    "OPTIMAL_MU_PSI_EV="
    + format(
        float(
            optimal_physical_source["chemical_potential_ev"]
        ),
        ".12e",
    )
)

print(
    "OPTIMAL_SOURCE_CUTOFF_EV="
    + format(
        float(
            optimal_physical_source["nda_cutoff_ev"]
        ),
        ".12e",
    )
)

print(
    "OPTIMAL_SOURCE_HARD_MARGIN="
    + format(
        float(
            optimal_physical_source["hard_scale_margin"]
        ),
        ".12e",
    )
)

print("EXACT_PAYLOAD_LOW_M_RESULT_IS_COMPLETE_ORACLE=False")
print("RENORMALIZED_DIRAC_SEA_INCLUDED=False")
print("RG_RESUMMED_CANONICAL_MATCHING_INCLUDED=False")
print("PHYSICAL_ANTIGRAVITY_MODEL_FOUND=NO")
print("CERTIFIED_SUB10MJ_MODEL_FOUND=NO")
print("DECISION=" + decision)
print("NEXT=" + next_step)
