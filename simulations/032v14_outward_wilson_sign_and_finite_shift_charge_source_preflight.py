"""032V14 — outward Wilson sign and finite shift-source preflight.

PURPOSE
-------
Close the immediate source-realization question left by 032V13.

V13 established:

    OUTWARD_SIGN_TARGET_STATIC_OUTWARD = True

but also:

    STATIC_POSITIVE_SHIFT_CURRENT_NO_SOURCE_THEOREM = True.

This run asks:

1. Is the outward derivative-conformal Wilson sign automatically excluded by
   known forward-limit positivity bounds?

2. Can a regular isolated static exact-shift source carry nonzero scalar
   monopole charge?

3. If not, does a compact zero-net derivative source provide a mathematically
   consistent static exterior multipole?

4. What is the canonical exterior energy of the leading dipole for the actual
   finite-payload benchmark?

5. How does the required EFT scale compare with currently published empirical
   scales, without treating model-dependent bounds as universal theorems?

LITERATURE INPUTS
-----------------
Jiang et al., JHEP 08 (2024) 114, arXiv:2404.17636:

- dimension-8 quadratic shift-symmetric matter operators;
- j=0 scalar sector and j=2 traceless sector;
- leading forward positivity constrains C2 >= 0 and C4 <= 0;
- the j=0 operators O1 and O3 do not contribute at order s^2 and are not
  constrained by that positivity bound;
- direct OFC/LV sensitivities correspond roughly to keV scales;
- indirect astrophysical/cosmological constraints can reach roughly
  0.1-100 GeV but are model dependent and can be altered by environmental
  effects.

Brax, van de Bruck & Trojanowski, Phys. Rev. D 105, 103015 (2022),
arXiv:2112.12264:

- derivative conformal interaction of schematic form

      (partial phi)^2 T / M^4;

- a particular collider interpretation reaches approximately 200 GeV;
- the authors explicitly note UV-completion/EFT-validity dependence.

Ikeda, Iyonaga & Kobayashi, Phys. Rev. D 104, 104009 (2021),
arXiv:2107.13804:

- shift-symmetric scalar-tensor stars with scalar field linearly dependent on
  time exist as a separate route and therefore time dependence is a genuine
  theorem evasion rather than an ad-hoc invention.

CLAIM LIMITS
------------
The zero-net dipole remains a PREFIELD exterior-source oracle.

No microscopic source has been established.

The 10-MJ objective cannot be passed using the exterior energy alone.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np

from antigravity_research.agminer.candidate import Candidate
from antigravity_research.agminer.normalization import (
    canonical_invariant_fingerprint,
)
from antigravity_research.agminer.oracle import (
    ActionOracle,
    LEDGER_PARTIAL_OPTIMISTIC,
    assess_oracle,
)
from antigravity_research.agminer.policy import (
    current_energy_policy,
)
from antigravity_research.agminer.reporting import (
    rebuild_summaries,
)
from antigravity_research.agminer.shift_source import (
    compact_derivative_source_net_monopole,
    dipole_axial_acceleration_m_s2,
    dipole_b_m6_for_axis_target,
    dipole_exterior_energy_j,
    dipole_y,
    m4_energy_rescale,
    regular_static_monopole_requires_evasion,
    scale_ev_for_m4_energy,
)
from antigravity_research.agminer.storage import Storage


ROOT = Path(__file__).resolve().parents[1]

V13 = (
    ROOT
    / "results"
    / "data"
    / "032v13_shift_symmetric_kinetic_conformal_oracle_summary.json"
)

OUT = (
    ROOT
    / "results"
    / "data"
    / "032v14_outward_wilson_sign_and_shift_source_preflight_summary.json"
)

CSV_OUT = (
    ROOT
    / "results"
    / "data"
    / "032v14_shift_source_route_and_scale_scan.csv"
)

DB = (
    ROOT
    / "results"
    / "agminer"
    / "agminer.sqlite3"
)


TARGET_J = 1.0e7
STRETCH_J = 1.0e6

G = 9.80665

PAYLOAD_MASS_KG = 1.0
PAYLOAD_RADIUS_M = 0.10

SOURCE_RADIUS_M = 0.10
SOURCE_PAYLOAD_GAP_M = 0.10

PAYLOAD_CENTER_M = (
    SOURCE_RADIUS_M
    + SOURCE_PAYLOAD_GAP_M
    + PAYLOAD_RADIUS_M
)

FAR_PAYLOAD_RADIUS_M = (
    PAYLOAD_CENTER_M
    + PAYLOAD_RADIUS_M
)

REFERENCE_SCALE_EV = 1.0e5


# ============================================================
# 0. PROVENANCE / POLICY
# ============================================================

policy = current_energy_policy()

assert float(
    policy["limit_j"]
) == TARGET_J

assert str(
    policy["comparison"]
) == "LT"

assert str(
    policy["policy_id"]
) == "ENERGY_ab8c16e45c837ffc"

assert V13.exists()

v13 = json.loads(
    V13.read_text(
        encoding="utf-8"
    )
)

assert (
    v13["decision"]
    ==
    "RED_MINIMAL_REGULAR_STATIC_KINETIC_CONFORMAL_SOURCE_GREEN_OUTWARD_SIGN_TARGET_ONLY"
)

assert (
    v13[
        "static_positive_shift_current_no_source_theorem"
    ]
    is True
)

assert (
    v13[
        "published_and_reference_static_signs"
    ][
        "OUTWARD_SIGN_TARGET"
    ]
    is True
)


# ============================================================
# 1. WILSON-SIGN PREFLIGHT
# ============================================================

# The desired derivative-conformal trace coupling belongs to the scalar
# j=0 type of dimension-8 sector.
#
# Jiang et al. explicitly find that the leading forward s^2 positivity
# constraints act on their j=2 coefficients C2 and C4, whereas O1 and O3 in
# the scalar j=0 sector do not contribute at that order.
#
# Therefore:
#
#     NO POSITIVITY SIGN KILL AT THIS ORDER
#
# is allowed.
#
# This does NOT mean:
#
#     UV COMPLETION PROVED.

wilson_sign = {
    "operator_sector":
        "J0_SCALAR_TRACE_DERIVATIVE_CONFORMAL",

    "leading_forward_positivity_sign_constraint":
        False,

    "j2_reference_constraints":
        "C2>=0_AND_C4<=0",

    "outward_sign_uv_completion_proved":
        False,

    "decision":
        "NO_STANDARD_FORWARD_POSITIVITY_SIGN_KILL_FOUND",
}


# ============================================================
# 2. STATIC MONOPOLE CLOSEOUT
# ============================================================

static_monopole_requires_evasion = (
    regular_static_monopole_requires_evasion()
)

assert (
    static_monopole_requires_evasion
    is True
)

zero_net_source_charge = (
    compact_derivative_source_net_monopole()
)

assert (
    zero_net_source_charge
    == 0.0
)


# ============================================================
# 3. ZERO-NET DIPOLE EXTERIOR ORACLE
# ============================================================

dipole_reference = (
    dipole_exterior_energy_j(
        scale_ev=
            REFERENCE_SCALE_EV,

        source_radius_m=
            SOURCE_RADIUS_M,

        far_axis_radius_m=
            FAR_PAYLOAD_RADIUS_M,

        target_acceleration_m_s2=
            G,
    )
)

dipole_energy_100kev_j = (
    dipole_reference[
        "exterior_scalar_energy_j"
    ]
)

assert (
    dipole_energy_100kev_j
    <
    TARGET_J
)

headroom_to_10mj = (
    TARGET_J
    / dipole_energy_100kev_j
)

scale_at_exact_10mj_ev = (
    scale_ev_for_m4_energy(
        target_energy_j=
            TARGET_J,

        reference_energy_j=
            dipole_energy_100kev_j,

        reference_scale_ev=
            REFERENCE_SCALE_EV,
    )
)

scale_at_exact_1mj_ev = (
    scale_ev_for_m4_energy(
        target_energy_j=
            STRETCH_J,

        reference_energy_j=
            dipole_energy_100kev_j,

        reference_scale_ev=
            REFERENCE_SCALE_EV,
    )
)


# ============================================================
# 4. FINITE PAYLOAD — SURFACE
# ============================================================

b_m6 = (
    dipole_reference[
        "b_m6"
    ]
)

surface_values: list[
    float
] = []

for index in range(
    8001
):

    u = (
        -1.0
        + 2.0
        * index
        / 8000.0
    )

    local_rho = (
        PAYLOAD_RADIUS_M
        * math.sqrt(
            max(
                0.0,
                1.0 - u**2,
            )
        )
    )

    local_z = (
        PAYLOAD_CENTER_M
        + PAYLOAD_RADIUS_M
        * u
    )

    surface_values.append(
        dipole_axial_acceleration_m_s2(
            b_m6,
            local_rho,
            local_z,
        )
    )

surface_min = min(
    surface_values
)

surface_max = max(
    surface_values
)

surface_nonuniformity = (
    surface_max
    / surface_min
)

assert (
    surface_min
    >=
    G
    * (
        1.0
        - 2.0e-12
    )
)

assert all(
    value > 0.0
    for value in surface_values
)


# ============================================================
# 5. FINITE PAYLOAD — VOLUME AVERAGE
# ============================================================

def payload_volume_average(
    order: int,
) -> float:
    """Return volume-averaged +z acceleration of spherical payload."""

    nodes_s, weights_s = (
        np.polynomial.legendre.leggauss(
            order
        )
    )

    nodes_u, weights_u = (
        np.polynomial.legendre.leggauss(
            order
        )
    )

    local_radii = (
        0.5
        * PAYLOAD_RADIUS_M
        * (
            nodes_s
            + 1.0
        )
    )

    local_weights = (
        0.5
        * PAYLOAD_RADIUS_M
        * weights_s
    )

    integral = 0.0

    for (
        local_radius,
        local_weight,
    ) in zip(
        local_radii,
        local_weights,
    ):

        rho = (
            local_radius
            * np.sqrt(
                1.0
                - nodes_u**2
            )
        )

        z = (
            PAYLOAD_CENTER_M
            + local_radius
            * nodes_u
        )

        axial = np.array(
            [
                dipole_axial_acceleration_m_s2(
                    b_m6,
                    float(rho_value),
                    float(z_value),
                )
                for (
                    rho_value,
                    z_value,
                )
                in zip(
                    rho,
                    z,
                )
            ],
            dtype=float,
        )

        integral += float(
            local_weight
            * local_radius**2
            * np.dot(
                weights_u,
                axial,
            )
        )

    return (
        3.0
        * integral
        / (
            2.0
            * PAYLOAD_RADIUS_M**3
        )
    )


payload_cm_64 = (
    payload_volume_average(
        64
    )
)

payload_cm_96 = (
    payload_volume_average(
        96
    )
)

payload_cm_relerr = (
    abs(
        payload_cm_96
        -
        payload_cm_64
    )
    /
    abs(
        payload_cm_96
    )
)

assert (
    payload_cm_relerr
    <
    1.0e-10
)

assert (
    payload_cm_96
    >=
    G
)


# ============================================================
# 6. EMPIRICAL / EFT SCALE CORRIDOR
# ============================================================

# These values are deliberately classified by provenance.
#
# Do not turn model-dependent astrophysical or collider numbers into a
# universal theorem against every derivative-conformal completion.

scale_inputs = [
    {
        "label":
            "JHEP2024_DIRECT_LOW",

        "scale_ev":
            1.0e3,

        "status":
            "CONTEXTUAL_DIRECT_SENSITIVITY",

        "universal_hard_bound":
            False,
    },
    {
        "label":
            "JHEP2024_DIRECT_HIGH",

        "scale_ev":
            1.0e4,

        "status":
            "CONTEXTUAL_DIRECT_SENSITIVITY",

        "universal_hard_bound":
            False,
    },
    {
        "label":
            "V14_REFERENCE",

        "scale_ev":
            1.0e5,

        "status":
            "PREFIELD_REFERENCE",

        "universal_hard_bound":
            False,
    },
    {
        "label":
            "V14_EXACT_10MJ_DIPOLE_SCALE",

        "scale_ev":
            scale_at_exact_10mj_ev,

        "status":
            "EXACT_EQUALITY_DOES_NOT_PASS_STRICT_LT",

        "universal_hard_bound":
            True,
    },
    {
        "label":
            "JHEP2024_INDIRECT_LOW",

        "scale_ev":
            1.0e8,

        "status":
            "MODEL_DEPENDENT_ASTRO_COSMO",

        "universal_hard_bound":
            False,
    },
    {
        "label":
            "JHEP2024_BBN_ORDER",

        "scale_ev":
            1.0e9,

        "status":
            "MODEL_DEPENDENT_THERMAL_HISTORY",

        "universal_hard_bound":
            False,
    },
    {
        "label":
            "JHEP2024_INDIRECT_HIGH",

        "scale_ev":
            1.0e11,

        "status":
            "MODEL_DEPENDENT_ASTRO_COSMO",

        "universal_hard_bound":
            False,
    },
    {
        "label":
            "PRD2022_COLLIDER_CONTEXT",

        "scale_ev":
            2.0e11,

        "status":
            "SPECIFIC_MODEL_UV_DEPENDENT_COLLIDER_CONTEXT",

        "universal_hard_bound":
            False,
    },
]

scale_rows: list[
    dict[str, object]
] = []

for item in scale_inputs:

    scale_ev = float(
        item[
            "scale_ev"
        ]
    )

    energy_j = (
        m4_energy_rescale(
            dipole_energy_100kev_j,
            REFERENCE_SCALE_EV,
            scale_ev,
        )
    )

    scale_rows.append(
        {
            "record_type":
                "SCALE_CONTEXT",

            "label":
                item[
                    "label"
                ],

            "scale_ev":
                scale_ev,

            "partial_dipole_energy_j":
                energy_j,

            "under_strict_10mj_partial_only":
                energy_j
                < TARGET_J,

            "status":
                item[
                    "status"
                ],

            "universal_hard_bound":
                item[
                    "universal_hard_bound"
                ],

            "complete_operating_energy":
                False,
        }
    )


# ============================================================
# 7. SOURCE-EVASION RANKING
# ============================================================

route_rows = [
    {
        "record_type":
            "SOURCE_ROUTE",

        "label":
            "REGULAR_STATIC_NET_MONOPOLE",

        "rank":
            99,

        "status":
            "CLOSED_UNDER_V13_V14_ASSUMPTIONS",

        "reason":
            "EXACT_SHIFT_CURRENT_FLUX_PLUS_REGULARITY",
    },
    {
        "record_type":
            "SOURCE_ROUTE",

        "label":
            "STATIC_COMPACT_ZERO_NET_DERIVATIVE_MULTIPOLE",

        "rank":
            1,

        "status":
            "GREEN_PREFIELD",

        "reason":
            "EXACT_SHIFT_SYMMETRY_AND_ZERO_NET_CHARGE_ALLOW_DIPOLE",
    },
    {
        "record_type":
            "SOURCE_ROUTE",

        "label":
            "TIME_LINEAR_SHIFT_BACKGROUND",

        "rank":
            2,

        "status":
            "OPEN_SECONDARY",

        "reason":
            "PUBLISHED_THEOREM_EVASION_BUT_BACKGROUND_ENERGY_REQUIRED",
    },
    {
        "record_type":
            "SOURCE_ROUTE",

        "label":
            "PHYSICAL_BOUNDARY_FLUX",

        "rank":
            3,

        "status":
            "OPEN_WITH_SOURCE_SURFACE_LEDGER",

        "reason":
            "INNER_BOUNDARY_EVASION_REQUIRES_PHYSICAL_SUPPORT",
    },
    {
        "record_type":
            "SOURCE_ROUTE",

        "label":
            "TOPOLOGICAL_OR_DEFECT_SECTOR",

        "rank":
            4,

        "status":
            "LOW_PRIORITY_OPEN",

        "reason":
            "TAIL_AND_SCAFFOLD_COST_EXPECTED",
    },
    {
        "record_type":
            "SOURCE_ROUTE",

        "label":
            "KINETIC_CRITICAL_Z_ZERO",

        "rank":
            98,

        "status":
            "RED_UNLESS_INDEPENDENT_HEALTH_PROOF",

        "reason":
            "DEGENERACY_STRONG_COUPLING_HYPERBOLICITY_RISK",
    },
]


# ============================================================
# 8. AGMINER PARTIAL ACTION ORACLE
# ============================================================

storage = Storage(
    DB
)

candidate = Candidate(
    family_id=
        "032_KINETIC_CONFORMAL_ZERO_NET_SHIFT_DIPOLE",

    family_version=
        "V14_EXTERNAL_DIPOLE_ORACLE_V1",

    params={
        "scale_ev":
            REFERENCE_SCALE_EV,

        "source_radius_m":
            SOURCE_RADIUS_M,

        "payload_center_m":
            PAYLOAD_CENTER_M,

        "payload_radius_m":
            PAYLOAD_RADIUS_M,

        "source_class":
            "COMPACT_DERIVATIVE_ZERO_NET_UNREALIZED",

        "physical_metric":
            "A_EQUALS_1_PLUS_Y",
    },

    physical_model_version=
        "ZERO_NET_SHIFT_DIPOLE_PREFIELD",

    energy_ledger_version=
        "PARTIAL_EXTERIOR_SCALAR_ONLY_V1",
)

storage.record_candidate(
    candidate,

    state=
        "PREFIELD_ACTION_TARGET_UNTRUSTED",

    tier=
        0,

    run_id=
        "032V14",
)

canonical_id = (
    canonical_invariant_fingerprint(
        family_id=
            candidate.family_id,

        family_version=
            candidate.family_version,

        invariants={
            "canonical_scalar_kinetic_z":
                1.0,

            "physical_metric":
                "A=1+Y",

            "Y":
                "|grad_phi|^2/(2*M^4)",

            "scale_ev":
                REFERENCE_SCALE_EV,

            "exterior_multipole":
                "L1_DIPOLE",
        },
    )
)

oracle = ActionOracle(
    canonical_invariant_id=
        canonical_id,

    proof_reference=
        "032V14_ZERO_NET_SHIFT_DIPOLE_EXTERIOR",

    relaxed_complete_energy_j=
        dipole_energy_100kev_j,

    ledger_scope=
        LEDGER_PARTIAL_OPTIMISTIC,

    normalization_invariant=
        True,

    naturalness_screened=
        False,

    universal_metric_screened=
        True,
)

assessment = (
    assess_oracle(
        oracle
    )
)

assert (
    oracle.trusted_for_reachability
    is False
)

assert (
    assessment.priority
    ==
    "ORACLE_PROVENANCE_INCOMPLETE"
)

storage.record_action_oracle(
    candidate.candidate_id,
    oracle,
)

reporting = (
    rebuild_summaries(
        storage,
        ROOT
        / "results"
        / "agminer",
    )
)

storage.close()


# ============================================================
# 9. OUTPUTS
# ============================================================

all_rows = (
    route_rows
    + scale_rows
)

fieldnames = sorted(
    {
        key
        for row in all_rows
        for key in row
    }
)

with CSV_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:

    writer = csv.DictWriter(
        handle,
        fieldnames=
            fieldnames,
    )

    writer.writeheader()

    writer.writerows(
        all_rows
    )


decision = (
    "GREEN_OUTWARD_J0_WILSON_SIGN_NOT_FORWARD_POSITIVITY_KILLED_"
    "RED_REGULAR_STATIC_NET_MONOPOLE_"
    "GREEN_ZERO_NET_DERIVATIVE_DIPOLE_PREFIELD"
)

next_step = (
    "032V15_ZERO_NET_SHIFT_DIPOLE_MICROSCOPIC_SOURCE_AND_MORPHOLOGY_GATE"
)


summary = {
    "branch":
        "032V14_OUTWARD_WILSON_SIGN_AND_FINITE_SHIFT_CHARGE_SOURCE_PREFLIGHT",

    "claim_class":
        "ANALYTIC_SOURCE_TOPOLOGY_AND_PARTIAL_DIPOLE_ORACLE",

    "energy_policy_id":
        str(
            policy[
                "policy_id"
            ]
        ),

    "wilson_sign": {
        **wilson_sign,

        "literature_reference":
            "Jiang_et_al_JHEP08_2024_114_arXiv2404.17636",
    },

    "static_source_theorem": {
        "regular_static_net_monopole_requires_evasion":
            static_monopole_requires_evasion,

        "compact_derivative_source_net_monopole":
            zero_net_source_charge,

        "regular_static_net_monopole_closed":
            True,

        "zero_net_static_multipoles_allowed_by_charge_accounting":
            True,
    },

    "dipole_counterfactual": {
        "scale_ev":
            REFERENCE_SCALE_EV,

        "source_radius_m":
            SOURCE_RADIUS_M,

        "source_payload_gap_m":
            SOURCE_PAYLOAD_GAP_M,

        "payload_mass_kg":
            PAYLOAD_MASS_KG,

        "payload_radius_m":
            PAYLOAD_RADIUS_M,

        "payload_center_m":
            PAYLOAD_CENTER_M,

        "far_payload_radius_m":
            FAR_PAYLOAD_RADIUS_M,

        "exterior_scalar_energy_j":
            dipole_energy_100kev_j,

        "headroom_to_strict_10mj":
            headroom_to_10mj,

        "scale_at_exact_10mj_ev":
            scale_at_exact_10mj_ev,

        "exact_10mj_passes":
            False,

        "scale_at_exact_1mj_ev":
            scale_at_exact_1mj_ev,

        "surface_min_outward_m_s2":
            surface_min,

        "surface_max_outward_m_s2":
            surface_max,

        "surface_nonuniformity_ratio":
            surface_nonuniformity,

        "payload_cm_volume_average_m_s2":
            payload_cm_96,

        "payload_cm_quadrature_relerr_64_96":
            payload_cm_relerr,

        "y_far_axis":
            dipole_reference[
                "y_far_axis"
            ],

        "y_source_axis":
            dipole_reference[
                "y_source_axis"
            ],

        "microscopic_source_realized":
            False,

        "complete_operating_ledger":
            False,

        "physical_energy_prediction":
            False,
    },

    "empirical_context": {
        "direct_j0_j2_experimental_scale_order_ev":
            [
                1.0e3,
                1.0e4,
            ],

        "direct_bounds_are_exact_match_to_engineered_static_source":
            False,

        "indirect_model_dependent_scale_range_ev":
            [
                1.0e8,
                1.0e11,
            ],

        "environmental_evasion_required_if_indirect_bounds_apply":
            True,

        "specific_prd2022_collider_context_ev":
            2.0e11,

        "collider_number_is_universal_hard_bound":
            False,

        "empirical_closure":
            False,
    },

    "source_route_ranking":
        route_rows,

    "agminer": {
        "partial_oracle_candidate_id":
            candidate.candidate_id,

        "partial_oracle_priority":
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


print(
    "=== 032V14 RESULT ==="
)

print(
    "ENERGY_POLICY_ID="
    + str(
        policy[
            "policy_id"
        ]
    )
)

print(
    "J0_OUTWARD_SIGN_FORWARD_POSITIVITY_KILL=False"
)

print(
    "OUTWARD_SIGN_UV_COMPLETION_PROVED=False"
)

print(
    "REGULAR_STATIC_NET_MONOPOLE_CLOSED=True"
)

print(
    "COMPACT_DERIVATIVE_SOURCE_NET_MONOPOLE="
    + format(
        zero_net_source_charge,
        ".12e",
    )
)

print(
    "ZERO_NET_STATIC_DIPOLE_PREFIELD=GREEN"
)

print(
    "DIPOLE_100KEV_EXTERIOR_KJ="
    + format(
        dipole_energy_100kev_j
        / 1.0e3,
        ".12e",
    )
)

print(
    "DIPOLE_HEADROOM_TO_10MJ_X="
    + format(
        headroom_to_10mj,
        ".12e",
    )
)

print(
    "DIPOLE_EXACT_10MJ_SCALE_KEV="
    + format(
        scale_at_exact_10mj_ev
        / 1.0e3,
        ".12e",
    )
)

print(
    "DIPOLE_EXACT_1MJ_SCALE_KEV="
    + format(
        scale_at_exact_1mj_ev
        / 1.0e3,
        ".12e",
    )
)

print(
    "PAYLOAD_SURFACE_MIN_M_S2="
    + format(
        surface_min,
        ".12e",
    )
)

print(
    "PAYLOAD_SURFACE_MAX_M_S2="
    + format(
        surface_max,
        ".12e",
    )
)

print(
    "PAYLOAD_SURFACE_NONUNIFORMITY="
    + format(
        surface_nonuniformity,
        ".12e",
    )
)

print(
    "PAYLOAD_CM_VOLUME_AVERAGE_M_S2="
    + format(
        payload_cm_96,
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
    "DIRECT_EMPIRICAL_KEV_SCALE_CONTEXT_NOT_AUTOMATIC_KILL=True"
)

print(
    "INDIRECT_ASTRO_COSMO_EMPIRICAL_CLOSURE=OPEN"
)

print(
    "PARTIAL_ORACLE_TRUSTED_FOR_REACHABILITY=False"
)

print(
    "PHYSICAL_ANTIGRAVITY_MODEL_FOUND=NO"
)

print(
    "CERTIFIED_SUB10MJ_MODEL_FOUND=NO"
)

print(
    "DECISION="
    + decision
)

print(
    "NEXT="
    + next_step
)
