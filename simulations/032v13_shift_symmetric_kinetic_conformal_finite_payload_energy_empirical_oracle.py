"""032V13 — kinetic-conformal finite-payload and source-existence oracle.

PURPOSE
-------
Test the V12 shift-symmetric kinetic-conformal operator frontier before any
large PDE search. The run separates four questions that must not be conflated:

1. Does an explicit kinetic-conformal coupling have the correct static sign?
2. Is the metric transformation locally invertible in the tested regime?
3. Can a regular isolated exact-shift-symmetric static configuration actually
   support a nonzero spatial scalar gradient while the spatial current
   coefficient remains positive?
4. If a legitimate source-evasion mechanism were later supplied, how small
   could the bare exterior canonical scalar-gradient energy be in a simple
   spherical finite-payload benchmark?

SCIENTIFIC CLAIM LIMITS
-----------------------
The exterior-gradient energy is a PARTIAL_OPTIMISTIC counterfactual oracle.

It excludes:

- the microscopic source;
- support;
- activation;
- control;
- empirical closure;
- naturalness closure;
- backreaction;
- stability.

It therefore cannot certify or even count as

    E_CONSERVATIVE_COMPLETE_OPERATING.

The static no-source result is conditional. It applies only to the regular,
isolated, asymptotically constant, zero-boundary-flux branch with a positive
effective spatial shift-current coefficient.

It does not close:

- finite shift-current sources;
- imposed boundary flux;
- defects/topology;
- time-dependent shift backgrounds;
- separately healthy kinetic-critical branches.

CLAIM CLASSIFICATION
--------------------
ANALYTIC_PREFIELD_FALSIFICATION_AND_PARTIAL_COUNTERFACTUAL_ORACLE
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np

from antigravity_research.agminer.candidate import Candidate
from antigravity_research.agminer.kinetic_conformal import (
    C_LIGHT,
    StaticShiftCurrentGate,
    counterfactual_spherical_exterior_energy_j,
    goldstone_linear_dlnc_dy,
    goldstone_linear_jacobian_kinetic_eigenvalue,
    required_ln_a_gradient_per_m,
    required_ln_c_gradient_per_m,
    scale_ev_for_counterfactual_energy,
    sign_flipped_linear_dlnc_dy,
    sign_flipped_linear_jacobian_kinetic_eigenvalue,
    static_acceleration_m_s2,
    static_shift_current_no_source,
    zgb_exponential_dlnc_dy,
    zgb_exponential_jacobian_kinetic_eigenvalue,
    zgb_gaussian_dlnc_dy,
    zgb_gaussian_jacobian_kinetic_eigenvalue,
)
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

DB = (
    ROOT
    / "results"
    / "agminer"
    / "agminer.sqlite3"
)

V12 = (
    ROOT
    / "results"
    / "data"
    / "032v12_local_metric_active_operator_atlas_summary.json"
)

OUT = (
    ROOT
    / "results"
    / "data"
    / "032v13_shift_symmetric_kinetic_conformal_oracle_summary.json"
)

CSV_OUT = (
    ROOT
    / "results"
    / "data"
    / "032v13_kinetic_conformal_reference_and_energy_scan.csv"
)

TARGET_J = 1.0e7
STRETCH_J = 1.0e6

G = 9.80665

PAYLOAD_MASS_KG = 1.0
RP = 0.10

RS = 0.10
GAP = 0.10

D = RS + GAP + RP


# ============================================================
# 0. POLICY / PROVENANCE GUARD
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

assert V12.exists()

v12 = json.loads(
    V12.read_text(
        encoding="utf-8",
    )
)

assert (
    v12["decision"]
    ==
    "GREEN_OPERATOR_ATLAS_KINETIC_CONFORMAL_X_METRIC_TOP_PREFIELD_CLASS"
)


# ============================================================
# 1. STATIC SIGN / LOCAL INVERTIBILITY AUDIT
# ============================================================

# For a localized static spacelike profile define
#
#     Y >= 0
#
# with
#
#     dY/dr < 0
#
# and
#
#     g_phys = C(Y) g.
#
# In the weak static limit:
#
#     a_r
#     =
#     -(c^2/2) d_r ln C
#
# and therefore:
#
#     a_r
#     =
#     -(c^2/2)
#     (d ln C/dY)
#     (dY/dr).
#
# Thus:
#
#     d ln C/dY > 0
#
# is the outward-sign requirement in this convention.

y_probe = 1.0e-6
dy_probe = -1.0e-6

references = [
    (
        "BV_GOLDSTONE_LINEAR_A",
        "Brax_Valageas_PRD95_043515_2017_arXiv1611.08279",
        "A(chi)=1+chi; static chi=-Y gives C=(1-Y)^2",
        goldstone_linear_dlnc_dy(
            y_probe
        ),
        goldstone_linear_jacobian_kinetic_eigenvalue(
            y_probe
        ),
        True,
    ),
    (
        "ZGB_EXPONENTIAL_TRANSFORMATION_PROBE",
        "Zumalacarregui_GarciaBellido_PRD89_064046_2014_arXiv1308.4685",
        "derivative-conformal probe C=exp(-Y)",
        zgb_exponential_dlnc_dy(
            y_probe
        ),
        zgb_exponential_jacobian_kinetic_eigenvalue(
            y_probe
        ),
        False,
    ),
    (
        "ZGB_GAUSSIAN_TRANSFORMATION_PROBE",
        "Zumalacarregui_GarciaBellido_PRD89_064046_2014_arXiv1308.4685",
        "derivative-conformal probe C=exp(-Y^2/2)",
        zgb_gaussian_dlnc_dy(
            y_probe
        ),
        zgb_gaussian_jacobian_kinetic_eigenvalue(
            y_probe
        ),
        False,
    ),
    (
        "OUTWARD_SIGN_TARGET",
        "V13_ACTION_MATCH_TARGET_NOT_UV_CERTIFIED",
        "A(chi)=1-chi; static chi=-Y gives C=(1+Y)^2",
        sign_flipped_linear_dlnc_dy(
            y_probe
        ),
        sign_flipped_linear_jacobian_kinetic_eigenvalue(
            y_probe
        ),
        False,
    ),
]

reference_rows: list[
    dict[str, object]
] = []

for (
    model_id,
    reference,
    coupling,
    slope,
    eigenvalue,
    complete_action,
) in references:

    outward = (
        static_acceleration_m_s2(
            slope,
            dy_probe,
        )
        > 0.0
    )

    reference_rows.append(
        {
            "record_type":
                "OPERATOR_SIGN_AUDIT",

            "model_id":
                model_id,

            "reference":
                reference,

            "coupling":
                coupling,

            "dlnc_dy":
                slope,

            "jacobian_kinetic_eigenvalue":
                eigenvalue,

            "static_outward":
                outward,

            "complete_action_provenance":
                complete_action,
        }
    )

assert [
    row["static_outward"]
    for row in reference_rows
] == [
    False,
    False,
    False,
    True,
]

assert all(
    float(
        row[
            "jacobian_kinetic_eigenvalue"
        ]
    )
    > 0.0
    for row in reference_rows
)


# ============================================================
# 2. REGULAR STATIC SHIFT-CURRENT UNIQUENESS GATE
# ============================================================

# In the declared minimal branch the exact shift symmetry gives
# a conserved current.
#
# If the static spatial equation reduces to
#
#     div[
#         Z_eff grad(phi)
#     ]
#     =
#     0
#
# with
#
#     Z_eff > 0,
#
# multiply by
#
#     phi - phi_infinity
#
# and integrate.
#
# Regularity, localization, and zero imposed boundary flux
# remove the boundary term and give
#
#     integral
#     Z_eff |grad(phi)|^2 dV
#     =
#     0.
#
# Positive Z_eff therefore forces
#
#     grad(phi)=0
#
# throughout this declared branch.

shift_gate = StaticShiftCurrentGate(
    current_coefficient_min=0.10,
)

no_source = (
    static_shift_current_no_source(
        shift_gate
    )
)

assert no_source is True


# ============================================================
# 3. COUNTERFACTUAL EXTERIOR ENERGY ORACLE
# ============================================================

# This does NOT assert that OUTWARD_SIGN_TARGET is sourceable.
#
# Instead:
#
# IF later physics supplies a legitimate finite shift charge,
# what bare canonical exterior-gradient energy accompanies the
# simplest massless spherical exterior?
#
# For a canonical exterior field with
#
#     phi approximately proportional to 1/r,
#
# we have
#
#     Y = K/r^4.
#
# For
#
#     C=(1+Y)^2,
#
# the radial physical-metric acceleration is
#
#     a
#     =
#     4 c^2 Y
#     /
#     [r(1+Y)].

scan_rows: list[
    dict[str, object]
] = []

for scale_ev in (
    1.0e-3,
    1.0,
    1.0e3,
    1.0e4,
    1.0e5,
    3.0e5,
    1.0e6,
    1.0e9,
):

    profile = (
        counterfactual_spherical_exterior_energy_j(
            scale_ev=scale_ev,
            source_radius_m=RS,
            payload_center_m=D,
            payload_radius_m=RP,
            target_acceleration_m_s2=G,
        )
    )

    scan_rows.append(
        {
            "record_type":
                "COUNTERFACTUAL_EXTERIOR_ENERGY",

            "model_id":
                "OUTWARD_SIGN_TARGET",

            "reference":
                "V13_HARMONIC_EXTERIOR_ONLY",

            "scale_ev":
                scale_ev,

            "exterior_scalar_energy_j":
                profile[
                    "exterior_scalar_energy_j"
                ],

            "y_source_surface":
                profile[
                    "y_source_surface"
                ],

            "jacobian_kinetic_eigenvalue":
                profile[
                    "jacobian_kinetic_eigenvalue_min"
                ],

            "under_10mj_bare_only":
                profile[
                    "exterior_scalar_energy_j"
                ]
                < TARGET_J,

            "physical_energy_prediction":
                False,
        }
    )


m_10mj_ev = (
    scale_ev_for_counterfactual_energy(
        target_energy_j=TARGET_J,
        source_radius_m=RS,
        payload_center_m=D,
        payload_radius_m=RP,
        target_acceleration_m_s2=G,
    )
)

m_1mj_ev = (
    scale_ev_for_counterfactual_energy(
        target_energy_j=STRETCH_J,
        source_radius_m=RS,
        payload_center_m=D,
        payload_radius_m=RP,
        target_acceleration_m_s2=G,
    )
)

benchmark = (
    counterfactual_spherical_exterior_energy_j(
        scale_ev=1.0e5,
        source_radius_m=RS,
        payload_center_m=D,
        payload_radius_m=RP,
        target_acceleration_m_s2=G,
    )
)


# ============================================================
# 4. FINITE-PAYLOAD SURFACE RECONSTRUCTION
# ============================================================

r_far = D + RP

k_m4 = (
    benchmark[
        "y_far_payload"
    ]
    * r_far**4
)


def axial_acceleration_at_source_coordinates(
    r_m: float,
    z_m: float,
) -> float:
    """Return +z acceleration for the spherical oracle profile."""

    radius = float(
        r_m
    )

    z = float(
        z_m
    )

    y = (
        k_m4
        /
        radius**4
    )

    radial = (
        4.0
        * C_LIGHT**2
        * y
        /
        (
            radius
            * (1.0 + y)
        )
    )

    return (
        radial
        * z
        /
        radius
    )


surface_values: list[
    float
] = []

for i in range(
    4001
):

    u = (
        -1.0
        + 2.0
        * i
        / 4000.0
    )

    radius = math.sqrt(
        D**2
        + RP**2
        + 2.0
        * D
        * RP
        * u
    )

    z = (
        D
        + RP
        * u
    )

    surface_values.append(
        axial_acceleration_at_source_coordinates(
            radius,
            z,
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
    /
    surface_min
)

assert (
    surface_min
    >=
    G
    * (
        1.0
        - 1.0e-12
    )
)


# ============================================================
# 5. FINITE-PAYLOAD VOLUME-AVERAGED ACCELERATION
# ============================================================

def payload_volume_average(
    order: int,
) -> float:
    """Reconstruct the payload volume-average +z acceleration.

    A tensor-product Gauss-Legendre quadrature is used over local payload
    radius and polar cosine.

    Axisymmetry removes the azimuthal integral analytically.
    """

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

    radii_local = (
        0.5
        * RP
        * (
            nodes_s
            + 1.0
        )
    )

    weights_local = (
        0.5
        * RP
        * weights_s
    )

    integral = 0.0

    for (
        s_local,
        weight_s,
    ) in zip(
        radii_local,
        weights_local,
    ):

        source_r = np.sqrt(
            D**2
            + s_local**2
            + 2.0
            * D
            * s_local
            * nodes_u
        )

        source_z = (
            D
            + s_local
            * nodes_u
        )

        y = (
            k_m4
            /
            source_r**4
        )

        radial = (
            4.0
            * C_LIGHT**2
            * y
            /
            (
                source_r
                * (
                    1.0
                    + y
                )
            )
        )

        axial = (
            radial
            * source_z
            /
            source_r
        )

        integral += float(
            weight_s
            * s_local**2
            * np.dot(
                weights_u,
                axial,
            )
        )

    return (
        3.0
        * integral
        /
        (
            2.0
            * RP**3
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
    payload_cm_96
    >=
    G
)

assert (
    payload_cm_relerr
    <
    1.0e-10
)


# ============================================================
# 6. AGMINER REJECTION MEMORY
# ============================================================

storage = Storage(
    DB
)


# ------------------------------------------------------------
# P002
# ------------------------------------------------------------
#
# The explicit BV linear branch is locally invertible in the
# small-Y regime tested here but has the wrong static external
# sign under the V13 localized-spacelike convention.

bv = Candidate(
    family_id=
        "032_KINETIC_CONFORMAL_GOLDSTONE",

    family_version=
        "V13_BV_LINEAR_A_V1",

    params={
        "A_chi":
            "1+chi",

        "source_class":
            "regular_static_isolated",
    },

    physical_model_version=
        "BV_LINEAR_STATIC_SPACELIKE",

    energy_ledger_version=
        "SIGN_GATE_BEFORE_ENERGY_V1",
)

storage.record_candidate(
    bv,
    state=
        "TIER0_RUNNING",
    tier=
        0,
    run_id=
        "032V13",
)

storage.reject(
    bv.candidate_id,

    state=
        "REJECTED_PAYLOAD",

    failure_code=
        "P002",

    gate=
        "kinetic_conformal_static_external_sign",

    energy_j=
        None,

    run_id=
        "032V13",
)


# ------------------------------------------------------------
# P003
# ------------------------------------------------------------
#
# The desired sign-flipped operator has the correct local sign
# but cannot realize a nonzero regular isolated static gradient
# inside the declared positive-current no-source class.

regular_target = Candidate(
    family_id=
        "032_KINETIC_CONFORMAL_SIGN_FLIPPED_TARGET",

    family_version=
        "V13_REGULAR_STATIC_V1",

    params={
        "A_chi":
            "1-chi",

        "source_class":
            "regular_static_isolated",
    },

    physical_model_version=
        "OUTWARD_SIGN_TARGET_REGULAR_STATIC_SOURCE",

    energy_ledger_version=
        "NO_SOURCE_THEOREM_BEFORE_ENERGY_V1",
)

storage.record_candidate(
    regular_target,
    state=
        "TIER0_RUNNING",
    tier=
        0,
    run_id=
        "032V13",
)

storage.reject(
    regular_target.candidate_id,

    state=
        "REJECTED_TIER0",

    failure_code=
        "P003",

    gate=
        "regular_static_shift_current_no_source",

    energy_j=
        None,

    run_id=
        "032V13",
)


# ============================================================
# 7. V6 ACTION-ORACLE INTEGRATION
# ============================================================

# This record is explicitly NOT promoted as a physical model.
#
# It exists so AGMINER remembers that the bare-field corridor is
# numerically interesting while simultaneously remembering that
# source existence, naturalness, and Wilson/operator provenance
# remain unresolved.

oracle_target = Candidate(
    family_id=
        "032_KINETIC_CONFORMAL_SIGN_FLIPPED_TARGET",

    family_version=
        "V13_SHIFT_CHARGE_ORACLE_V1",

    params={
        "A_chi":
            "1-chi",

        "scale_ev":
            1.0e5,

        "source_radius_m":
            RS,

        "payload_center_m":
            D,

        "payload_radius_m":
            RP,

        "source_class":
            "UNREALIZED_SHIFT_CHARGE_EVASION_REQUIRED",
    },

    physical_model_version=
        "OUTWARD_SIGN_HARMONIC_PREFIELD_ORACLE",

    energy_ledger_version=
        "PARTIAL_EXTERIOR_SCALAR_ONLY_V1",
)

storage.record_candidate(
    oracle_target,

    state=
        "PREFIELD_ACTION_TARGET_UNTRUSTED",

    tier=
        0,

    run_id=
        "032V13",
)


canonical_id = (
    canonical_invariant_fingerprint(
        family_id=
            oracle_target.family_id,

        family_version=
            oracle_target.family_version,

        invariants={
            "canonical_scalar_kinetic_z":
                1.0,

            "A_chi":
                "1-chi",

            "chi":
                "X/M^4",

            "scale_ev":
                1.0e5,
        },
    )
)


oracle = ActionOracle(
    canonical_invariant_id=
        canonical_id,

    proof_reference=
        "032V13_HARMONIC_EXTERIOR_ONLY",

    relaxed_complete_energy_j=
        benchmark[
            "exterior_scalar_energy_j"
        ],

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
    oracle_target.candidate_id,
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


# Do not write MechanismMetrics here.
#
# A true mechanism-factorization record requires a self-consistent
# physical source. The current outward profile is only a
# counterfactual exterior/source-evasion target.


# ============================================================
# 8. WRITE ARTIFACTS
# ============================================================

CSV_OUT.parent.mkdir(
    parents=True,
    exist_ok=True,
)

rows = (
    reference_rows
    + scan_rows
)

fieldnames = sorted(
    {
        key
        for row in rows
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
        rows
    )


decision = (
    "RED_MINIMAL_REGULAR_STATIC_KINETIC_CONFORMAL_SOURCE_"
    "GREEN_OUTWARD_SIGN_TARGET_ONLY"
)

next_step = (
    "032V14_OUTWARD_WILSON_SIGN_AND_FINITE_SHIFT_CHARGE_SOURCE_PREFLIGHT"
)


result = {
    "branch":
        (
            "032V13_SHIFT_SYMMETRIC_KINETIC_CONFORMAL_"
            "FINITE_PAYLOAD_ENERGY_EMPIRICAL_ORACLE"
        ),

    "claim_class":
        (
            "ANALYTIC_PREFIELD_FALSIFICATION_AND_"
            "PARTIAL_COUNTERFACTUAL_ORACLE"
        ),

    "energy_policy_id":
        str(
            policy[
                "policy_id"
            ]
        ),

    "published_and_reference_static_signs":
        {
            str(
                row[
                    "model_id"
                ]
            ):
            bool(
                row[
                    "static_outward"
                ]
            )
            for row
            in reference_rows
        },

    "static_positive_shift_current_no_source_theorem":
        no_source,

    "theorem_assumptions": {
        "regular":
            True,

        "isolated_asymptotically_constant":
            True,

        "effective_spatial_current_coefficient_positive":
            True,

        "explicit_shift_current_source":
            False,

        "boundary_flux":
            False,

        "topological_or_defect_sector":
            False,

        "time_dependent_shift_background":
            False,
    },

    "theorem_evasions_to_test": [
        "FINITE_LOCAL_SHIFT_CURRENT_SOURCE",
        "IMPOSED_BOUNDARY_FLUX",
        "TOPOLOGICAL_OR_DEFECT_SECTOR",
        "TIME_DEPENDENT_SHIFT_BACKGROUND",
        "KINETIC_CRITICAL_SURFACE_WITH_SEPARATE_HEALTH_GATE",
    ],

    "finite_payload_counterfactual": {
        "payload_mass_kg":
            PAYLOAD_MASS_KG,

        "payload_radius_m":
            RP,

        "source_radius_m":
            RS,

        "source_payload_gap_m":
            GAP,

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

        "required_abs_grad_ln_A_per_m":
            required_ln_a_gradient_per_m(
                G
            ),

        "required_abs_grad_ln_C_per_m":
            required_ln_c_gradient_per_m(
                G
            ),

        "bare_exterior_100kev_j":
            benchmark[
                "exterior_scalar_energy_j"
            ],

        "bare_exterior_scale_at_10mj_ev":
            m_10mj_ev,

        "bare_exterior_scale_at_1mj_ev":
            m_1mj_ev,

        "y_source_surface":
            benchmark[
                "y_source_surface"
            ],

        "jacobian_kinetic_eigenvalue_min":
            benchmark[
                "jacobian_kinetic_eigenvalue_min"
            ],

        "complete_operating_ledger":
            False,

        "physical_energy_prediction":
            False,
    },

    "agminer": {
        "p002_wrong_sign_candidate_id":
            bv.candidate_id,

        "p003_no_source_candidate_id":
            regular_target.candidate_id,

        "partial_oracle_candidate_id":
            oracle_target.candidate_id,

        "partial_oracle_priority":
            assessment.priority,

        "partial_oracle_trusted_for_reachability":
            False,

        "mechanism_metrics_recorded":
            False,

        "reporting":
            reporting,
    },

    "closures": {
        "minimal_bv_linear_static_spacelike_branch":
            True,

        "regular_static_positive_shift_current_branch_under_stated_assumptions":
            True,

        "full_kinetic_conformal_operator_class":
            False,

        "time_dependent_or_finite_shift_charge_evasions":
            False,
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
        result,
        indent=2,
        sort_keys=True,
    )
    + "\n",
    encoding="utf-8",
)


print(
    "=== 032V13 RESULT ==="
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
    "BV_LINEAR_STATIC_OUTWARD="
    + str(
        reference_rows[
            0
        ][
            "static_outward"
        ]
    )
)

print(
    "ZGB_EXP_STATIC_OUTWARD="
    + str(
        reference_rows[
            1
        ][
            "static_outward"
        ]
    )
)

print(
    "ZGB_GAUSS_STATIC_OUTWARD="
    + str(
        reference_rows[
            2
        ][
            "static_outward"
        ]
    )
)

print(
    "OUTWARD_SIGN_TARGET_STATIC_OUTWARD="
    + str(
        reference_rows[
            3
        ][
            "static_outward"
        ]
    )
)

print(
    "STATIC_POSITIVE_SHIFT_CURRENT_NO_SOURCE_THEOREM="
    + str(
        no_source
    )
)

print(
    "PAYLOAD_SURFACE_MIN_OUTWARD_M_S2="
    + format(
        surface_min,
        ".12e",
    )
)

print(
    "PAYLOAD_SURFACE_MAX_OUTWARD_M_S2="
    + format(
        surface_max,
        ".12e",
    )
)

print(
    "PAYLOAD_SURFACE_NONUNIFORMITY_RATIO="
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
    "PAYLOAD_CM_QUADRATURE_RELERR_64_96="
    + format(
        payload_cm_relerr,
        ".12e",
    )
)

print(
    "BARE_EXTERIOR_100KEV_KJ="
    + format(
        benchmark[
            "exterior_scalar_energy_j"
        ]
        / 1.0e3,
        ".12e",
    )
)

print(
    "BARE_EXTERIOR_SCALE_AT_10MJ_KEV="
    + format(
        m_10mj_ev
        / 1.0e3,
        ".12e",
    )
)

print(
    "BARE_EXTERIOR_SCALE_AT_1MJ_KEV="
    + format(
        m_1mj_ev
        / 1.0e3,
        ".12e",
    )
)

print(
    "BARE_EXTERIOR_ORACLE_IS_COMPLETE=False"
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
