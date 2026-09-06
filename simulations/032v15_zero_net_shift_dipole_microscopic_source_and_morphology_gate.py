"""032V15 — zero-net shift dipole microscopic-source and morphology gate.

PURPOSE
-------
Turn the V14 zero-net derivative dipole from an abstract source distribution
into a concrete microscopic source EFT and determine whether unavoidable
source inventory already kills the strict <10-MJ objective.

The source EFT is a hidden polarized fermion Psi with

    L_src
        =
        (1/f_psi)
        partial_mu(phi)
        bar(Psi) gamma^mu gamma^5 Psi.

The interaction preserves exact scalar shift symmetry.

The source morphology is a uniformly polarized spheroid placed below the
finite payload. The optimizer varies transverse and axial source dimensions.

ENERGY LEDGER INCLUDED HERE
---------------------------
This run includes:

1. the complete all-space canonical scalar-gradient energy;
2. exact zero-temperature relativistic hidden-fermion energy;
3. relativistic reduction in axial-current efficiency;
4. an NDA source-EFT hard-scale margin;
5. a Laue/DEC pressure-support lower bound.

ENERGY LEDGER STILL OPEN
------------------------
The run does NOT yet contain:

- a constructed confinement field or wall;
- polarization/activation energy;
- source formation/reset energy;
- nonlinear source stability;
- source radiation;
- a UV completion of the outward j=0 metric coefficient;
- complete Einstein/Jordan backreaction;
- full empirical stellar/cosmological closure.

Therefore even a value below 10 MJ remains a PARTIAL OPTIMISTIC oracle.

PRIMARY BENCHMARK
-----------------
Metric scale:

    M = 100 keV

Hidden source:

    m_psi / p_F = 1

NDA source hard-scale safety:

    Lambda_src / max(p_F,m_psi) = 5.

Payload:

    mass = 1 kg
    radius = 0.10 m
    minimum surface acceleration = 1g.

CLAIM CLASSIFICATION
--------------------
MICROSCOPIC_SOURCE_EFT_INVENTORY_AND_MORPHOLOGY_PREFLIGHT
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import differential_evolution

from antigravity_research.agminer.axial_shift_source import (
    axial_accelerations_m_s2,
    hidden_fermion_inventory_floor,
    ordinary_electron_rest_energy_floor_j,
    required_q2_for_surface,
    spheroid_surface_kernel,
    spheroid_total_scalar_energy_j,
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
from antigravity_research.agminer.policy import (
    current_energy_policy,
)
from antigravity_research.agminer.reporting import (
    rebuild_summaries,
)
from antigravity_research.agminer.storage import Storage


ROOT = Path(__file__).resolve().parents[1]

V14 = (
    ROOT
    / "results"
    / "data"
    / "032v14_outward_wilson_sign_and_shift_source_preflight_summary.json"
)

OUT = (
    ROOT
    / "results"
    / "data"
    / "032v15_axial_shift_source_morphology_summary.json"
)

CSV_OUT = (
    ROOT
    / "results"
    / "data"
    / "032v15_axial_shift_source_scan.csv"
)

DB = (
    ROOT
    / "results"
    / "agminer"
    / "agminer.sqlite3"
)


TARGET_J = 1.0e7
G = 9.80665

METRIC_SCALE_EV = 1.0e5

PAYLOAD_MASS_KG = 1.0
PAYLOAD_RADIUS_M = 0.10

SOURCE_PAYLOAD_GAP_M = 0.10

# Source top is z=0.
PAYLOAD_CENTER_Z_M = (
    SOURCE_PAYLOAD_GAP_M
    + PAYLOAD_RADIUS_M
)

MASS_OVER_PF = 1.0
PRIMARY_HARD_MARGIN = 5.0


# ============================================================
# 0. POLICY / PROVENANCE
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

assert V14.exists()

v14 = json.loads(
    V14.read_text(
        encoding="utf-8"
    )
)

assert (
    v14["decision"]
    ==
    "GREEN_OUTWARD_J0_WILSON_SIGN_NOT_FORWARD_POSITIVITY_KILLED_RED_REGULAR_STATIC_NET_MONOPOLE_GREEN_ZERO_NET_DERIVATIVE_DIPOLE_PREFIELD"
)


# ============================================================
# 1. PAYLOAD GEOMETRY
# ============================================================

def payload_surface_points(
    count: int,
) -> np.ndarray:
    """Return axisymmetric finite-payload surface samples."""

    u = np.linspace(
        -1.0,
        1.0,
        int(count),
    )

    rho = (
        PAYLOAD_RADIUS_M
        * np.sqrt(
            np.maximum(
                0.0,
                1.0 - u**2,
            )
        )
    )

    z = (
        PAYLOAD_CENTER_Z_M
        + PAYLOAD_RADIUS_M
        * u
    )

    return np.stack(
        (
            rho,
            np.zeros_like(rho),
            z,
        ),
        axis=1,
    )


def geometry_metrics(
    a_m: float,
    c_m: float,
    *,
    n_t: int,
    n_phi: int,
    n_surface: int,
    hard_margin: float,
) -> dict[str, object]:
    """Evaluate finite payload and source-energy floor for one spheroid."""

    surface = payload_surface_points(
        n_surface
    )

    gradient, hessian = (
        spheroid_surface_kernel(
            surface,
            a_m=a_m,
            c_m=c_m,
            n_t=n_t,
            n_phi=n_phi,
        )
    )

    q2 = required_q2_for_surface(
        gradient,
        hessian,
        target_acceleration_m_s2=G,
    )

    if not math.isfinite(
        q2
    ):
        return {
            "valid":
                False,
        }

    q = math.sqrt(
        q2
    )

    acceleration = (
        axial_accelerations_m_s2(
            gradient,
            hessian,
            q2=q2,
        )
    )

    scalar_energy = (
        spheroid_total_scalar_energy_j(
            q2=q2,
            metric_scale_ev=METRIC_SCALE_EV,
            a_m=a_m,
            c_m=c_m,
        )
    )

    source = (
        hidden_fermion_inventory_floor(
            q=q,
            metric_scale_ev=METRIC_SCALE_EV,
            a_m=a_m,
            c_m=c_m,
            hard_scale_margin=hard_margin,
            mass_over_pf=MASS_OVER_PF,
        )
    )

    partial_floor = (
        scalar_energy
        + source[
            "fermion_energy_j"
        ]
        + source[
            "laue_dec_pressure_support_floor_j"
        ]
    )

    return {
        "valid":
            True,

        "a_m":
            float(
                a_m
            ),

        "c_m":
            float(
                c_m
            ),

        "q":
            q,

        "q2":
            q2,

        "scalar_energy_j":
            scalar_energy,

        "source":
            source,

        "partial_conservative_floor_j":
            partial_floor,

        "surface_min_m_s2":
            float(
                np.min(
                    acceleration
                )
            ),

        "surface_max_m_s2":
            float(
                np.max(
                    acceleration
                )
            ),

        "surface_nonuniformity":
            float(
                np.max(
                    acceleration
                )
                /
                np.min(
                    acceleration
                )
            ),
    }


# ============================================================
# 2. MORPHOLOGY OPTIMIZATION
# ============================================================

# Optimize logarithmic source dimensions.
#
# Search domain:
#
#     0.08 m <= a <= 0.80 m
#     0.03 m <= c <= 0.40 m.
#
# The source remains entirely below z=0, while the payload begins at z=0.10 m.

log_bounds = [
    (
        math.log(
            0.08
        ),
        math.log(
            0.80
        ),
    ),
    (
        math.log(
            0.03
        ),
        math.log(
            0.40
        ),
    ),
]


def objective(
    log_dimensions: np.ndarray,
) -> float:
    """Return coarse partial conservative floor."""

    a_m = math.exp(
        float(
            log_dimensions[
                0
            ]
        )
    )

    c_m = math.exp(
        float(
            log_dimensions[
                1
            ]
        )
    )

    result = geometry_metrics(
        a_m,
        c_m,
        n_t=20,
        n_phi=32,
        n_surface=41,
        hard_margin=PRIMARY_HARD_MARGIN,
    )

    if not bool(
        result[
            "valid"
        ]
    ):
        return 1.0e99

    return float(
        result[
            "partial_conservative_floor_j"
        ]
    )


optimization = differential_evolution(
    objective,
    bounds=log_bounds,
    seed=15015,
    popsize=10,
    maxiter=28,
    tol=1.0e-6,
    polish=True,
    workers=1,
    updating="immediate",
)

best_a_m = math.exp(
    float(
        optimization.x[
            0
        ]
    )
)

best_c_m = math.exp(
    float(
        optimization.x[
            1
        ]
    )
)


# ============================================================
# 3. INDEPENDENT QUADRATURE RECONSTRUCTION
# ============================================================

medium = geometry_metrics(
    best_a_m,
    best_c_m,
    n_t=48,
    n_phi=72,
    n_surface=201,
    hard_margin=PRIMARY_HARD_MARGIN,
)

fine = geometry_metrics(
    best_a_m,
    best_c_m,
    n_t=64,
    n_phi=96,
    n_surface=201,
    hard_margin=PRIMARY_HARD_MARGIN,
)

assert bool(
    medium[
        "valid"
    ]
)

assert bool(
    fine[
        "valid"
    ]
)

energy_convergence_relerr = (
    abs(
        float(
            fine[
                "partial_conservative_floor_j"
            ]
        )
        -
        float(
            medium[
                "partial_conservative_floor_j"
            ]
        )
    )
    /
    abs(
        float(
            fine[
                "partial_conservative_floor_j"
            ]
        )
    )
)

q_convergence_relerr = (
    abs(
        float(
            fine[
                "q"
            ]
        )
        -
        float(
            medium[
                "q"
            ]
        )
    )
    /
    abs(
        float(
            fine[
                "q"
            ]
        )
    )
)

assert (
    energy_convergence_relerr
    <
    1.0e-8
)

assert (
    q_convergence_relerr
    <
    1.0e-8
)


# ============================================================
# 4. FINITE-PAYLOAD VOLUME AVERAGE
# ============================================================

def payload_volume_average(
    *,
    a_m: float,
    c_m: float,
    q2: float,
    order: int,
) -> float:
    """Return volume-averaged +z acceleration."""

    radial_nodes, radial_weights = (
        np.polynomial.legendre.leggauss(
            int(order)
        )
    )

    angular_nodes, angular_weights = (
        np.polynomial.legendre.leggauss(
            int(order)
        )
    )

    local_radius = (
        0.5
        * PAYLOAD_RADIUS_M
        * (
            radial_nodes
            + 1.0
        )
    )

    local_weight = (
        0.5
        * PAYLOAD_RADIUS_M
        * radial_weights
    )

    points: list[
        list[float]
    ] = []

    weights: list[
        float
    ] = []

    for (
        radius,
        weight_r,
    ) in zip(
        local_radius,
        local_weight,
    ):
        for (
            u,
            weight_u,
        ) in zip(
            angular_nodes,
            angular_weights,
        ):

            rho = (
                radius
                * math.sqrt(
                    max(
                        0.0,
                        1.0 - u**2,
                    )
                )
            )

            z = (
                PAYLOAD_CENTER_Z_M
                + radius * u
            )

            points.append(
                [
                    rho,
                    0.0,
                    z,
                ]
            )

            weights.append(
                float(
                    weight_r
                    * weight_u
                    * radius**2
                )
            )

    gradient, hessian = (
        spheroid_surface_kernel(
            np.asarray(
                points,
                dtype=float,
            ),
            a_m=a_m,
            c_m=c_m,
            n_t=48,
            n_phi=72,
        )
    )

    acceleration = (
        axial_accelerations_m_s2(
            gradient,
            hessian,
            q2=q2,
        )
    )

    integral = float(
        np.dot(
            np.asarray(
                weights,
                dtype=float,
            ),
            acceleration,
        )
    )

    return (
        3.0
        * integral
        /
        (
            2.0
            * PAYLOAD_RADIUS_M**3
        )
    )


payload_cm_16 = (
    payload_volume_average(
        a_m=best_a_m,
        c_m=best_c_m,
        q2=float(
            fine[
                "q2"
            ]
        ),
        order=16,
    )
)

payload_cm_20 = (
    payload_volume_average(
        a_m=best_a_m,
        c_m=best_c_m,
        q2=float(
            fine[
                "q2"
            ]
        ),
        order=20,
    )
)

payload_cm_relerr = (
    abs(
        payload_cm_20
        -
        payload_cm_16
    )
    /
    abs(
        payload_cm_20
    )
)

assert (
    payload_cm_relerr
    <
    1.0e-8
)


# ============================================================
# 5. SOURCE-EFT SAFETY SCAN
# ============================================================

safety_rows: list[
    dict[str, object]
] = []

for hard_margin in (
    3.0,
    4.0,
    5.0,
    5.25,
    5.5,
    6.0,
):
    result = geometry_metrics(
        best_a_m,
        best_c_m,
        n_t=48,
        n_phi=72,
        n_surface=201,
        hard_margin=hard_margin,
    )

    source = result[
        "source"
    ]

    partial = float(
        result[
            "partial_conservative_floor_j"
        ]
    )

    safety_rows.append(
        {
            "record_type":
                "SOURCE_EFT_MARGIN_SCAN",

            "hard_scale_margin":
                hard_margin,

            "partial_conservative_floor_j":
                partial,

            "under_strict_10mj":
                partial < TARGET_J,

            "f_psi_ev":
                source[
                    "f_psi_ev"
                ],

            "p_f_ev":
                source[
                    "p_f_ev"
                ],

            "m_psi_ev":
                source[
                    "m_psi_ev"
                ],

            "nda_cutoff_ev":
                source[
                    "nda_cutoff_ev"
                ],

            "particle_number":
                source[
                    "particle_number"
                ],

            "gp_equivalent":
                source[
                    "gp_equivalent"
                ],

            "loop_proxy":
                source[
                    "loop_proxy_gp2_over_16pi2"
                ],
        }
    )


# ============================================================
# 6. METRIC-SCALE SCAN
# ============================================================

# For fixed dimensionless geometry, q, mass/pF ratio, and hard-scale margin,
# every included energy in this preflight scales as M^4.

reference_partial = float(
    fine[
        "partial_conservative_floor_j"
    ]
)

scale_rows: list[
    dict[str, object]
] = []

for scale_ev in (
    1.0e4,
    3.0e4,
    5.0e4,
    8.0e4,
    1.0e5,
):
    scaled_energy = (
        reference_partial
        * (
            scale_ev
            / METRIC_SCALE_EV
        ) ** 4
    )

    scale_rows.append(
        {
            "record_type":
                "METRIC_SCALE_SCAN",

            "metric_scale_ev":
                scale_ev,

            "partial_conservative_floor_j":
                scaled_energy,

            "under_strict_10mj":
                scaled_energy < TARGET_J,

            "empirical_closure":
                False,
        }
    )

metric_scale_exact_10mj_ev = (
    METRIC_SCALE_EV
    * (
        TARGET_J
        / reference_partial
    ) ** 0.25
)


# ============================================================
# 7. ORDINARY-ELECTRON NEGATIVE CONTROL
# ============================================================

electron_control = (
    ordinary_electron_rest_energy_floor_j(
        q=float(
            fine[
                "q"
            ]
        ),
        metric_scale_ev=METRIC_SCALE_EV,
        a_m=best_a_m,
        c_m=best_c_m,
        hard_scale_margin=PRIMARY_HARD_MARGIN,
    )
)

ordinary_electron_closed = (
    electron_control[
        "optimistic_rest_energy_floor_j"
    ]
    >
    TARGET_J
)

assert ordinary_electron_closed


# ============================================================
# 8. ENERGY ANATOMY
# ============================================================

source = fine[
    "source"
]

scalar_energy_j = float(
    fine[
        "scalar_energy_j"
    ]
)

fermion_energy_j = float(
    source[
        "fermion_energy_j"
    ]
)

support_floor_j = float(
    source[
        "laue_dec_pressure_support_floor_j"
    ]
)

partial_floor_j = float(
    fine[
        "partial_conservative_floor_j"
    ]
)

remaining_to_10mj_j = (
    TARGET_J
    -
    partial_floor_j
)

partial_under_target = (
    partial_floor_j
    <
    TARGET_J
)

source_plus_field_fraction = (
    scalar_energy_j
    +
    fermion_energy_j
) / partial_floor_j


# ============================================================
# 9. AGMINER MEMORY
# ============================================================

storage = Storage(
    DB
)


# Ordinary electron implementation is analytically rejected.

electron_candidate = Candidate(
    family_id=
        "032_KINETIC_CONFORMAL_SM_ELECTRON_AXIAL_SOURCE",

    family_version=
        "V15_OPTIMISTIC_REST_FLOOR_V1",

    params={
        "metric_scale_ev":
            METRIC_SCALE_EV,

        "a_m":
            best_a_m,

        "c_m":
            best_c_m,

        "hard_margin":
            PRIMARY_HARD_MARGIN,
    },

    physical_model_version=
        "SM_ELECTRON_POLARIZED_SPHEROID",

    energy_ledger_version=
        "OPTIMISTIC_REST_ONLY_FLOOR_V1",
)

storage.record_candidate(
    electron_candidate,

    state=
        "TIER0_RUNNING",

    tier=
        0,

    run_id=
        "032V15",
)

storage.reject(
    electron_candidate.candidate_id,

    state=
        "REJECTED_ENERGY",

    failure_code=
        "E003",

    gate=
        "ordinary_electron_microscopic_source_rest_energy_floor",

    energy_j=
        float(
            electron_control[
                "optimistic_rest_energy_floor_j"
            ]
        ),

    run_id=
        "032V15",
)


# Hidden source remains an untrusted partial oracle.

hidden_candidate = Candidate(
    family_id=
        "032_KINETIC_CONFORMAL_HIDDEN_AXIAL_SHIFT_SOURCE",

    family_version=
        "V15_SPHEROID_SOURCE_FLOOR_V1",

    params={
        "metric_scale_ev":
            METRIC_SCALE_EV,

        "a_m":
            best_a_m,

        "c_m":
            best_c_m,

        "mass_over_pf":
            MASS_OVER_PF,

        "hard_margin":
            PRIMARY_HARD_MARGIN,

        "source_action":
            "DERIVATIVE_AXIAL_CURRENT",
    },

    physical_model_version=
        "HIDDEN_POLARIZED_FERMION_SPHEROID_PREFIELD",

    energy_ledger_version=
        "FIELD_PLUS_FERMI_PLUS_LAUE_DEC_SUPPORT_FLOOR_V1",
)

storage.record_candidate(
    hidden_candidate,

    state=
        "PREFIELD_MICROSCOPIC_SOURCE_UNTRUSTED",

    tier=
        0,

    run_id=
        "032V15",
)

canonical_id = (
    canonical_invariant_fingerprint(
        family_id=
            hidden_candidate.family_id,

        family_version=
            hidden_candidate.family_version,

        invariants={
            "canonical_scalar_kinetic_z":
                1.0,

            "physical_metric":
                "A=1+Y",

            "metric_scale_ev":
                METRIC_SCALE_EV,

            "source_operator":
                "dphi_J5_over_f",

            "mass_over_pf":
                MASS_OVER_PF,

            "hard_margin":
                PRIMARY_HARD_MARGIN,
        },
    )
)

oracle = ActionOracle(
    canonical_invariant_id=
        canonical_id,

    proof_reference=
        "032V15_HIDDEN_AXIAL_SOURCE_SPHEROID_FLOOR",

    relaxed_complete_energy_j=
        partial_floor_j,

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

storage.record_action_oracle(
    hidden_candidate.candidate_id,
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
# 10. DECISION
# ============================================================

if partial_under_target:
    decision = (
        "GREEN_MICROSCOPIC_SOURCE_INVENTORY_CORRIDOR_"
        "NOT_PHYSICAL_MODEL_"
        "SUPPORT_CONFINEMENT_STABILITY_EMPIRICAL_OPEN"
    )

    next_step = (
        "032V16_HIDDEN_AXIAL_SOURCE_SELF_BINDING_SUPPORT_"
        "AND_MULTISOURCE_UNIFORMITY_GATE"
    )

else:
    decision = (
        "RED_SINGLE_SPECIES_HIDDEN_AXIAL_SOURCE_"
        "PARTIAL_FLOOR_GE_10MJ"
    )

    next_step = (
        "032V16_SOURCE_CARRIER_RERANK"
    )


# ============================================================
# 11. CSV
# ============================================================

rows = (
    safety_rows
    + scale_rows
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
        fieldnames=fieldnames,
    )

    writer.writeheader()
    writer.writerows(
        rows
    )


# ============================================================
# 12. SUMMARY
# ============================================================

summary = {
    "branch":
        "032V15_ZERO_NET_SHIFT_DIPOLE_MICROSCOPIC_SOURCE_AND_MORPHOLOGY_GATE",

    "claim_class":
        "MICROSCOPIC_SOURCE_EFT_INVENTORY_AND_MORPHOLOGY_PREFLIGHT",

    "energy_policy_id":
        str(
            policy[
                "policy_id"
            ]
        ),

    "source_action": {
        "interaction":
            "dphi_mu_J5_mu_over_fpsi",

        "exact_shift_symmetric":
            True,

        "source_field":
            "HIDDEN_DIRAC_FERMION",

        "uniform_polarization":
            True,

        "net_scalar_monopole":
            0.0,

        "leading_exterior_multipole":
            "DIPOLE",

        "self_bound_solution":
            False,
    },

    "optimized_morphology": {
        "a_m":
            best_a_m,

        "c_m":
            best_c_m,

        "full_axial_length_m":
            2.0
            * best_c_m,

        "source_top_to_payload_near_surface_gap_m":
            SOURCE_PAYLOAD_GAP_M,

        "q":
            float(
                fine[
                    "q"
                ]
            ),

        "surface_min_m_s2":
            float(
                fine[
                    "surface_min_m_s2"
                ]
            ),

        "surface_max_m_s2":
            float(
                fine[
                    "surface_max_m_s2"
                ]
            ),

        "surface_nonuniformity":
            float(
                fine[
                    "surface_nonuniformity"
                ]
            ),

        "payload_cm_volume_average_m_s2":
            payload_cm_20,

        "payload_cm_quadrature_relerr":
            payload_cm_relerr,

        "energy_convergence_relerr":
            energy_convergence_relerr,

        "q_convergence_relerr":
            q_convergence_relerr,
    },

    "primary_100kev_inventory": {
        "metric_scale_ev":
            METRIC_SCALE_EV,

        "hard_scale_margin":
            PRIMARY_HARD_MARGIN,

        "mass_over_pf":
            MASS_OVER_PF,

        "axial_efficiency":
            source[
                "axial_efficiency"
            ],

        "f_psi_ev":
            source[
                "f_psi_ev"
            ],

        "p_f_ev":
            source[
                "p_f_ev"
            ],

        "m_psi_ev":
            source[
                "m_psi_ev"
            ],

        "nda_cutoff_ev":
            source[
                "nda_cutoff_ev"
            ],

        "particle_number":
            source[
                "particle_number"
            ],

        "gp_equivalent":
            source[
                "gp_equivalent"
            ],

        "loop_proxy_gp2_over_16pi2":
            source[
                "loop_proxy_gp2_over_16pi2"
            ],

        "scalar_total_energy_j":
            scalar_energy_j,

        "hidden_fermion_energy_j":
            fermion_energy_j,

        "laue_dec_pressure_support_floor_j":
            support_floor_j,

        "partial_conservative_floor_j":
            partial_floor_j,

        "remaining_to_strict_10mj_j":
            remaining_to_10mj_j,

        "source_plus_field_fraction":
            source_plus_field_fraction,

        "complete_operating_ledger":
            False,
    },

    "metric_scale_scan": {
        "exact_10mj_partial_floor_scale_ev":
            metric_scale_exact_10mj_ev,

        "empirical_lower_bound_mapped_to_this_exact_operator":
            False,

        "empirical_closure":
            False,
    },

    "ordinary_electron_control": {
        **electron_control,

        "closed_for_10mj":
            ordinary_electron_closed,
    },

    "open_costs": [
        "CONFINEMENT_ABOVE_LAUE_DEC_LOWER_BOUND",
        "POLARIZATION_OR_ACTIVATION",
        "FORMATION_AND_RESET",
        "NONLINEAR_SOURCE_STABILITY",
        "RADIATION",
        "OUTWARD_J0_UV_COMPLETION",
        "FULL_EMPIRICAL_STELLAR_COSMOLOGY",
        "FULL_METRIC_BACKREACTION",
    ],

    "agminer": {
        "electron_rejection_candidate_id":
            electron_candidate.candidate_id,

        "hidden_partial_oracle_candidate_id":
            hidden_candidate.candidate_id,

        "hidden_oracle_priority":
            assessment.priority,

        "hidden_oracle_trusted_for_reachability":
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


# ============================================================
# 13. TERMINAL RESULT
# ============================================================

print(
    "=== 032V15 RESULT ==="
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
    "SOURCE_ACTION=SHIFT_SYMMETRIC_HIDDEN_FERMION_AXIAL_CURRENT"
)

print(
    "OPTIMIZED_A_M="
    + format(
        best_a_m,
        ".12e",
    )
)

print(
    "OPTIMIZED_C_M="
    + format(
        best_c_m,
        ".12e",
    )
)

print(
    "Q="
    + format(
        float(
            fine[
                "q"
            ]
        ),
        ".12e",
    )
)

print(
    "PAYLOAD_SURFACE_MIN_M_S2="
    + format(
        float(
            fine[
                "surface_min_m_s2"
            ]
        ),
        ".12e",
    )
)

print(
    "PAYLOAD_SURFACE_MAX_M_S2="
    + format(
        float(
            fine[
                "surface_max_m_s2"
            ]
        ),
        ".12e",
    )
)

print(
    "PAYLOAD_SURFACE_NONUNIFORMITY="
    + format(
        float(
            fine[
                "surface_nonuniformity"
            ]
        ),
        ".12e",
    )
)

print(
    "PAYLOAD_CM_VOLUME_AVERAGE_M_S2="
    + format(
        payload_cm_20,
        ".12e",
    )
)

print(
    "FIELD_TOTAL_KJ="
    + format(
        scalar_energy_j
        / 1.0e3,
        ".12e",
    )
)

print(
    "HIDDEN_FERMION_MJ="
    + format(
        fermion_energy_j
        / 1.0e6,
        ".12e",
    )
)

print(
    "LAUE_DEC_SUPPORT_FLOOR_MJ="
    + format(
        support_floor_j
        / 1.0e6,
        ".12e",
    )
)

print(
    "PARTIAL_CONSERVATIVE_FLOOR_MJ="
    + format(
        partial_floor_j
        / 1.0e6,
        ".12e",
    )
)

print(
    "REMAINING_TO_10MJ_MJ="
    + format(
        remaining_to_10mj_j
        / 1.0e6,
        ".12e",
    )
)

print(
    "SOURCE_NDA_HARD_MARGIN="
    + format(
        source[
            "hard_scale_margin"
        ],
        ".12e",
    )
)

print(
    "F_PSI_EV="
    + format(
        source[
            "f_psi_ev"
        ],
        ".12e",
    )
)

print(
    "P_F_EV="
    + format(
        source[
            "p_f_ev"
        ],
        ".12e",
    )
)

print(
    "M_PSI_EV="
    + format(
        source[
            "m_psi_ev"
        ],
        ".12e",
    )
)

print(
    "N_HIDDEN_FERMIONS="
    + format(
        source[
            "particle_number"
        ],
        ".12e",
    )
)

print(
    "GP_EQUIVALENT="
    + format(
        source[
            "gp_equivalent"
        ],
        ".12e",
    )
)

print(
    "LOOP_PROXY="
    + format(
        source[
            "loop_proxy_gp2_over_16pi2"
        ],
        ".12e",
    )
)

print(
    "ORDINARY_ELECTRON_REST_FLOOR_TJ="
    + format(
        electron_control[
            "optimistic_rest_energy_floor_j"
        ]
        / 1.0e12,
        ".12e",
    )
)

print(
    "EXACT_10MJ_PARTIAL_SCALE_KEV="
    + format(
        metric_scale_exact_10mj_ev
        / 1.0e3,
        ".12e",
    )
)

print(
    "QUADRATURE_ENERGY_RELERR="
    + format(
        energy_convergence_relerr,
        ".12e",
    )
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
