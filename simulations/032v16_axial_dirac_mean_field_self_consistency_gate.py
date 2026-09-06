"""032V16 axial Dirac mean-field self-consistency gate.

This run repairs the central V15 source assumption. Instead of prescribing a
fully polarized free Fermi gas, it solves the occupied positive Dirac bands in
the self-generated spacelike axial background. The exact local bands are

    E_s^2 = p_perp^2 + (sqrt(p_z^2+m_psi^2) + s b)^2.

Self-consistency requires

    J5 = q f_psi M^2,
    b = N_z J5/f_psi^2.

With r=m/b and u=mu/b, flavor multiplicity cancels from the tree-level energy
and loop proxy. It only improves the NDA hard-scale margin as sqrt(N_f).

The renormalized Dirac sea is not included. Relativistic survivors are partial
oracles until one-loop vacuum, scalar canonical normalization, Wilson matching,
and finite-payload matter backreaction are reconstructed.
"""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

from scipy.optimize import differential_evolution

from antigravity_research.agminer.axial_dirac_meanfield import (
    EV_J,
    HBARC_EV_M,
    fixed_density_current_susceptibility_hat,
    meanfield_scaling_metrics,
    minimum_loop_for_nr_stoner,
    payload_trace_load,
    physicalize_dimensionless_state,
    solve_mu_for_current,
    spheroid_demag_z,
    spheroid_volume_m3,
    stoner_parameter_nr,
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

V15 = (
    ROOT
    / "results"
    / "data"
    / "032v15_axial_shift_source_morphology_summary.json"
)

OUT = (
    ROOT
    / "results"
    / "data"
    / "032v16_axial_dirac_meanfield_self_consistency_summary.json"
)

SCAN_OUT = (
    ROOT
    / "results"
    / "data"
    / "032v16_axial_dirac_loop_energy_pareto.csv"
)

PAYLOAD_OUT = (
    ROOT
    / "results"
    / "data"
    / "032v16_payload_trace_load_scout.csv"
)

DB = (
    ROOT
    / "results"
    / "agminer"
    / "agminer.sqlite3"
)

TARGET_J = 1.0e7
PAYLOAD_MASS_KG = 1.0
PAYLOAD_RADIUS_M = 0.10
MAX_FLAVORS = 256


policy = current_energy_policy()

assert float(
    policy[
        "limit_j"
    ]
) == TARGET_J

assert str(
    policy[
        "comparison"
    ]
) == "LT"

assert str(
    policy[
        "policy_id"
    ]
) == "ENERGY_ab8c16e45c837ffc"

assert V15.exists()

v15 = json.loads(
    V15.read_text(
        encoding="utf-8"
    )
)

assert (
    v15[
        "decision"
    ]
    ==
    (
        "GREEN_MICROSCOPIC_SOURCE_INVENTORY_CORRIDOR_NOT_PHYSICAL_MODEL_"
        "SUPPORT_CONFINEMENT_STABILITY_EMPIRICAL_OPEN"
    )
)

morph = v15[
    "optimized_morphology"
]

inv = v15[
    "primary_100kev_inventory"
]

q = float(
    morph[
        "q"
    ]
)

a_m = float(
    morph[
        "a_m"
    ]
)

c_m = float(
    morph[
        "c_m"
    ]
)

metric_scale_ev = float(
    inv[
        "metric_scale_ev"
    ]
)

volume_m3 = (
    spheroid_volume_m3(
        a_m,
        c_m,
    )
)

demag_z = (
    spheroid_demag_z(
        a_m,
        c_m,
    )
)

volume_nat = (
    volume_m3
    / HBARC_EV_M**3
)


# ============================================================
# 1. OLD V15 STATE AFTER EXACT FERMION RESPONSE
# ============================================================

old_f_ev = float(
    inv[
        "f_psi_ev"
    ]
)

old_m_ev = float(
    inv[
        "m_psi_ev"
    ]
)

old_cutoff_ev = float(
    inv[
        "nda_cutoff_ev"
    ]
)

old_b_ev = (
    demag_z
    * q
    * metric_scale_ev**2
    / old_f_ev
)

old_target_j5 = (
    q
    * old_f_ev
    * metric_scale_ev**2
)

old = solve_mu_for_current(
    mass_ev=
        old_m_ev,

    axial_b_ev=
        old_b_ev,

    target_current_ev3=
        old_target_j5,

    flavors=
        1,

    order=
        96,
)

old_mu_ev = float(
    old[
        "chemical_potential_ev"
    ]
)

old_hard_margin = (
    old_cutoff_ev
    / max(
        old_mu_ev,
        old_m_ev,
        old_b_ev,
    )
)

old_particles = (
    float(
        old[
            "number_density_ev3"
        ]
    )
    * volume_nat
)

old_band_j = (
    float(
        old[
            "energy_density_ev4"
        ]
    )
    * volume_nat
    * EV_J
)

old_p_perp_j = (
    float(
        old[
            "pressure_perp_ev4"
        ]
    )
    * volume_nat
    * EV_J
)

old_p_z_j = (
    float(
        old[
            "pressure_z_ev4"
        ]
    )
    * volume_nat
    * EV_J
)

old_p_mean_j = (
    2.0
    * old_p_perp_j
    + old_p_z_j
) / 3.0

old_field_j = float(
    inv[
        "scalar_total_energy_j"
    ]
)

old_support_j = abs(
    old_p_mean_j
    - old_field_j
)

# The exact occupied-band eigenvalues already contain the axial interaction.
# Add the positive scalar-field energy once.

old_partial_j = (
    old_band_j
    + old_field_j
    + old_support_j
)

assert (
    old_hard_margin
    < 1.0
)

assert (
    old_partial_j
    > 1.0e10
)


# ============================================================
# 2. CONTROLLED NR STONER / LOOP THEOREM
# ============================================================

# In the controlled nonrelativistic limit:
#
#     S
#       =
#       4 N_z (p_F/m) L.
#
# For:
#
#     p_F/m <= 0.5
#
# and
#
#     L <= 0.5
#
# the current morphology cannot reach S>1.

nr_ratio_cap = 0.5
nr_loop_cap = 0.5

nr_stoner_max = (
    stoner_parameter_nr(
        demag_z=
            demag_z,

        p_f_over_m=
            nr_ratio_cap,

        loop_proxy=
            nr_loop_cap,
    )
)

nr_loop_required = (
    minimum_loop_for_nr_stoner(
        demag_z=
            demag_z,

        p_f_over_m=
            nr_ratio_cap,
    )
)

assert (
    nr_stoner_max
    < 1.0
)

assert (
    nr_loop_required
    > 0.8
)


# ============================================================
# 3. EXACT POSITIVE-BAND LOOP / ENERGY PARETO
# ============================================================

def optimize_cap(
    cap: float,
) -> dict[str, object]:
    """Minimize the positive-band partial floor under one loop-proxy cap."""

    def objective(
        log_values,
    ) -> float:
        r = (
            10.0
            ** float(
                log_values[
                    0
                ]
            )
        )

        u = (
            10.0
            ** float(
                log_values[
                    1
                ]
            )
        )

        try:
            metrics = (
                meanfield_scaling_metrics(
                    q=
                        q,

                    metric_scale_ev=
                        metric_scale_ev,

                    volume_m3=
                        volume_m3,

                    demag_z=
                        demag_z,

                    r_mass_over_b=
                        r,

                    u_mu_over_b=
                        u,

                    order=
                        40,
                )
            )

        except (
            ValueError,
            RuntimeError,
            FloatingPointError,
        ):
            return 1.0e99

        v_loop = max(
            0.0,
            float(
                metrics[
                    "loop_proxy"
                ]
            )
            / cap
            - 1.0,
        )

        v_nf = max(
            0.0,
            float(
                metrics[
                    "minimum_flavors_continuous_for_margin5"
                ]
            )
            / MAX_FLAVORS
            - 1.0,
        )

        return (
            float(
                metrics[
                    "partial_conservative_floor_j"
                ]
            )
            * (
                1.0
                + 1.0e7
                * (
                    v_loop**2
                    + v_nf**2
                )
            )
        )

    result = differential_evolution(
        objective,
        bounds=(
            (
                -0.7,
                0.8,
            ),
            (
                -0.1,
                1.2,
            ),
        ),
        seed=
            16000
            + int(
                round(
                    cap
                    * 10000.0
                )
            ),
        popsize=
            10,
        maxiter=
            65,
        tol=
            1.0e-9,
        polish=
            True,
        workers=
            1,
        updating=
            "immediate",
    )

    r = (
        10.0
        ** float(
            result.x[
                0
            ]
        )
    )

    u = (
        10.0
        ** float(
            result.x[
                1
            ]
        )
    )

    metrics = meanfield_scaling_metrics(
        q=
            q,

        metric_scale_ev=
            metric_scale_ev,

        volume_m3=
            volume_m3,

        demag_z=
            demag_z,

        r_mass_over_b=
            r,

        u_mu_over_b=
            u,

        order=
            96,
    )

    nf_cont = float(
        metrics[
            "minimum_flavors_continuous_for_margin5"
        ]
    )

    flavors = max(
        1,
        int(
            math.ceil(
                nf_cont
            )
        ),
    )

    if flavors > MAX_FLAVORS:
        raise RuntimeError(
            "optimized state exceeds flavor cap"
        )

    physical = (
        physicalize_dimensionless_state(
            q=
                q,

            metric_scale_ev=
                metric_scale_ev,

            demag_z=
                demag_z,

            r_mass_over_b=
                r,

            u_mu_over_b=
                u,

            flavors=
                flavors,

            order=
                96,
        )
    )

    susceptibility = (
        fixed_density_current_susceptibility_hat(
            r_mass_over_b=
                r,

            u_mu_over_b=
                u,

            order=
                80,
        )
    )

    particles = (
        float(
            physical[
                "number_density_ev3"
            ]
        )
        * volume_nat
    )

    return {
        "loop_cap":
            cap,

        "r":
            r,

        "u":
            u,

        "metrics":
            metrics,

        "physical":
            physical,

        "susceptibility":
            susceptibility,

        "particles":
            particles,
    }


states = [
    optimize_cap(
        cap
    )
    for cap in (
        0.20,
        0.25,
        0.30,
        0.50,
    )
]

rows: list[
    dict[str, object]
] = []

for state in states:
    met = state[
        "metrics"
    ]

    phy = state[
        "physical"
    ]

    sus = state[
        "susceptibility"
    ]

    rows.append(
        {
            "loop_cap":
                state[
                    "loop_cap"
                ],

            "r_mass_over_b":
                state[
                    "r"
                ],

            "u_mu_over_b":
                state[
                    "u"
                ],

            "loop_proxy":
                met[
                    "loop_proxy"
                ],

            "partial_conservative_floor_j":
                met[
                    "partial_conservative_floor_j"
                ],

            "under_strict_10mj_partial_only":
                float(
                    met[
                        "partial_conservative_floor_j"
                    ]
                )
                < TARGET_J,

            "minimum_flavors_continuous_for_margin5":
                met[
                    "minimum_flavors_continuous_for_margin5"
                ],

            "selected_integer_flavors":
                phy[
                    "flavors"
                ],

            "hard_scale_margin":
                phy[
                    "hard_scale_margin"
                ],

            "f_psi_ev":
                phy[
                    "f_psi_ev"
                ],

            "axial_b_ev":
                phy[
                    "axial_b_ev"
                ],

            "m_psi_ev":
                phy[
                    "m_psi_ev"
                ],

            "chemical_potential_ev":
                phy[
                    "chemical_potential_ev"
                ],

            "particle_number":
                state[
                    "particles"
                ],

            "fixed_density_susceptibility_hat":
                sus[
                    "susceptibility_hat"
                ],

            "susceptibility_to_current_ratio":
                sus[
                    "susceptibility_to_current_ratio"
                ],

            "renormalized_dirac_sea_included":
                False,
        }
    )


state_025 = states[
    1
]

selected = states[
    2
]

state_050 = states[
    3
]

assert (
    float(
        state_025[
            "metrics"
        ][
            "partial_conservative_floor_j"
        ]
    )
    > TARGET_J
)

assert (
    float(
        selected[
            "metrics"
        ][
            "partial_conservative_floor_j"
        ]
    )
    < TARGET_J
)

assert (
    float(
        selected[
            "susceptibility"
        ][
            "susceptibility_hat"
        ]
    )
    > 0.0
)

# The aggressive L=0.50 point already develops a negative occupied-band
# fixed-density curvature proxy. Do not promote it.

assert (
    float(
        state_050[
            "susceptibility"
        ][
            "susceptibility_hat"
        ]
    )
    < 0.0
)


sel_met = selected[
    "metrics"
]

sel_phy = selected[
    "physical"
]

sel_sus = selected[
    "susceptibility"
]

sel_partial_j = float(
    sel_met[
        "partial_conservative_floor_j"
    ]
)

sel_headroom_j = (
    TARGET_J
    - sel_partial_j
)


# ============================================================
# 4. FLAVOR-SCALING NO-SHORTCUT RECONSTRUCTION
# ============================================================

nf = int(
    sel_phy[
        "flavors"
    ]
)

phy_4nf = (
    physicalize_dimensionless_state(
        q=
            q,

        metric_scale_ev=
            metric_scale_ev,

        demag_z=
            demag_z,

        r_mass_over_b=
            float(
                selected[
                    "r"
                ]
            ),

        u_mu_over_b=
            float(
                selected[
                    "u"
                ]
            ),

        flavors=
            4
            * nf,

        order=
            96,
    )
)

hard_margin_ratio = (
    float(
        phy_4nf[
            "hard_scale_margin"
        ]
    )
    / float(
        sel_phy[
            "hard_scale_margin"
        ]
    )
)

assert math.isclose(
    hard_margin_ratio,
    2.0,
    rel_tol=2.0e-10,
)


# ============================================================
# 5. PAYLOAD MATTER-TRACE BACKREACTION SCOUT
# ============================================================

payload_rows: list[
    dict[str, object]
] = []

for scale_ev in (
    1.0e5,
    8.0e4,
    5.0e4,
    3.0e4,
    1.0e4,
):
    trace = payload_trace_load(
        payload_mass_kg=
            PAYLOAD_MASS_KG,

        payload_radius_m=
            PAYLOAD_RADIUS_M,

        metric_scale_ev=
            scale_ev,
    )

    transmission = float(
        trace[
            "uniform_sphere_transmission_scout"
        ]
    )

    naive_j = (
        sel_partial_j
        * (
            scale_ev
            / metric_scale_ev
        ) ** 4
    )

    payload_rows.append(
        {
            "metric_scale_ev":
                scale_ev,

            "epsilon_trace_load":
                trace[
                    "epsilon_trace_load"
                ],

            "uniform_sphere_transmission_scout":
                transmission,

            "naive_m4_partial_j":
                naive_j,

            "transmission_corrected_scout_j":
                naive_j
                / transmission**2,

            "trusted_energy_oracle":
                False,
        }
    )


trace_100 = (
    payload_trace_load(
        payload_mass_kg=
            PAYLOAD_MASS_KG,

        payload_radius_m=
            PAYLOAD_RADIUS_M,

        metric_scale_ev=
            metric_scale_ev,
    )
)

epsilon_100 = float(
    trace_100[
        "epsilon_trace_load"
    ]
)

# With:
#
#     epsilon proportional M^-4,
#
# and:
#
#     T=3/(3+epsilon),
#
# the simple transmission-corrected scout has its analytic minimum at
#
#     epsilon=3.
#
# This is only a target for V17. It is not an energy oracle.

scout_opt_scale_ev = (
    metric_scale_ev
    * (
        epsilon_100
        / 3.0
    ) ** 0.25
)

scout_opt_energy_j = (
    sel_partial_j
    * 4.0
    * epsilon_100
    / 3.0
)


# ============================================================
# 6. AGMINER MEMORY
# ============================================================

storage = Storage(
    DB
)


old_candidate = Candidate(
    family_id=
        "032_KINETIC_CONFORMAL_HIDDEN_AXIAL_SHIFT_SOURCE",

    family_version=
        "V16_OLD_V15_FREE_SINGLE_FLAVOR_RESPONSE_V1",

    params={
        "f_psi_ev":
            old_f_ev,

        "m_psi_ev":
            old_m_ev,
    },

    physical_model_version=
        "OLD_V15_STATE_WITH_SELFCONSISTENT_FERMION_RESPONSE",

    energy_ledger_version=
        "POSITIVE_BANDS_PLUS_FIELD_PLUS_LAUE_SCOUT_V1",
)

storage.record_candidate(
    old_candidate,
    state=
        "TIER0_RUNNING",
    tier=
        0,
    run_id=
        "032V16",
)

storage.reject(
    old_candidate.candidate_id,
    state=
        "REJECTED_EFT",
    failure_code=
        "N004",
    gate=
        "axial_dirac_selfconsistent_source_cutoff_margin",
    energy_j=
        old_partial_j,
    run_id=
        "032V16",
)


nr_candidate = Candidate(
    family_id=
        "032_KINETIC_CONFORMAL_HIDDEN_AXIAL_SHIFT_SOURCE",

    family_version=
        "V16_CONTROLLED_NR_SPONTANEOUS_POLARIZATION_V1",

    params={
        "p_f_over_m_cap":
            nr_ratio_cap,

        "loop_proxy_cap":
            nr_loop_cap,
    },

    physical_model_version=
        "NR_STONER_LOOP_ANALYTIC_GATE",

    energy_ledger_version=
        "ANALYTIC_PREFLIGHT_ONLY_V1",
)

storage.record_candidate(
    nr_candidate,
    state=
        "TIER0_RUNNING",
    tier=
        0,
    run_id=
        "032V16",
)

storage.reject(
    nr_candidate.candidate_id,
    state=
        "REJECTED_NATURALNESS",
    failure_code=
        "N005",
    gate=
        "controlled_nr_stoner_loop_conflict",
    energy_j=
        None,
    run_id=
        "032V16",
)


selected_candidate = Candidate(
    family_id=
        "032_KINETIC_CONFORMAL_AXIAL_DIRAC_MEANFIELD",

    family_version=
        "V16_POSITIVE_BAND_LOOP030_V1",

    params={
        "metric_scale_ev":
            metric_scale_ev,

        "r_mass_over_b":
            float(
                selected[
                    "r"
                ]
            ),

        "u_mu_over_b":
            float(
                selected[
                    "u"
                ]
            ),

        "flavors":
            nf,

        "loop_proxy":
            float(
                sel_met[
                    "loop_proxy"
                ]
            ),
    },

    physical_model_version=
        "SELFCONSISTENT_POSITIVE_DIRAC_BANDS_NO_VACUUM_DETERMINANT",

    energy_ledger_version=
        "BAND_PLUS_SCALAR_PLUS_LAUE_DEC_SUPPORT_FLOOR_V1",
)

storage.record_candidate(
    selected_candidate,
    state=
        "PREFIELD_MEANFIELD_UNTRUSTED",
    tier=
        0,
    run_id=
        "032V16",
)


canonical_id = (
    canonical_invariant_fingerprint(
        family_id=
            selected_candidate.family_id,

        family_version=
            selected_candidate.family_version,

        invariants={
            "tree_scalar_z":
                1.0,

            "metric_operator":
                "A_EQUALS_1_PLUS_Y",

            "source_operator":
                "DPHI_J5_OVER_F",

            "loop_proxy":
                float(
                    sel_met[
                        "loop_proxy"
                    ]
                ),

            "vacuum_determinant_included":
                False,
        },
    )
)


oracle = ActionOracle(
    canonical_invariant_id=
        canonical_id,

    proof_reference=
        "032V16_POSITIVE_BAND_DIMENSIONLESS_MEANFIELD_LOOP030",

    relaxed_complete_energy_j=
        sel_partial_j,

    ledger_scope=
        LEDGER_PARTIAL_OPTIMISTIC,

    # Loop canonicalization remains open.
    normalization_invariant=
        False,

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
    selected_candidate.candidate_id,
    oracle,
)

reporting = rebuild_summaries(
    storage,
    ROOT
    / "results"
    / "agminer",
)

storage.close()


# ============================================================
# 7. OUTPUTS
# ============================================================

with SCAN_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=
            list(
                rows[
                    0
                ].keys()
            ),
    )

    writer.writeheader()
    writer.writerows(
        rows
    )


with PAYLOAD_OUT.open(
    "w",
    newline="",
    encoding="utf-8",
) as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=
            list(
                payload_rows[
                    0
                ].keys()
            ),
    )

    writer.writeheader()
    writer.writerows(
        payload_rows
    )


decision = (
    "RED_V15_MINIMAL_SINGLE_FLAVOR_MEANFIELD_"
    "RED_CONTROLLED_NR_SPONTANEOUS_POLARIZATION_"
    "GREEN_RELATIVISTIC_POSITIVE_BAND_LOOP030_PARTIAL_CORRIDOR_"
    "VACUUM_CANONICALIZATION_REQUIRED"
)

next_step = (
    "032V17_AXIAL_VACUUM_CANONICALIZATION_AND_PAYLOAD_BACKREACTION_GATE"
)


summary = {
    "branch":
        "032V16_AXIAL_DIRAC_MEAN_FIELD_SELF_CONSISTENCY_GATE",

    "claim_class":
        "TREE_LEVEL_POSITIVE_BAND_MEANFIELD_AND_ANALYTIC_FALSIFICATION",

    "energy_policy_id":
        str(
            policy[
                "policy_id"
            ]
        ),

    "v15_old_state_exact_response": {
        "axial_b_ev":
            old_b_ev,

        "chemical_potential_ev":
            old_mu_ev,

        "nda_cutoff_ev":
            old_cutoff_ev,

        "actual_hard_scale_margin":
            old_hard_margin,

        "particle_number":
            old_particles,

        "band_energy_j":
            old_band_j,

        "field_energy_j":
            old_field_j,

        "pressure_perp_inventory_j":
            old_p_perp_j,

        "pressure_z_inventory_j":
            old_p_z_j,

        "laue_support_floor_j":
            old_support_j,

        "partial_meanfield_floor_j":
            old_partial_j,

        "decision":
            "RED_OLD_V15_FREE_SINGLE_FLAVOR_AFTER_SELF_RESPONSE",
    },

    "controlled_nr_stoner_gate": {
        "p_f_over_m_cap":
            nr_ratio_cap,

        "loop_proxy_cap":
            nr_loop_cap,

        "maximum_stoner_parameter":
            nr_stoner_max,

        "minimum_loop_proxy_for_stoner_at_ratio_cap":
            nr_loop_required,

        "flavor_multiplicity_evades_bound":
            False,

        "decision":
            "RED_CONTROLLED_NR_SPONTANEOUS_POLARIZATION",
    },

    "flavor_scaling": {
        "energy_depends_on_flavor_at_fixed_dimensionless_state":
            False,

        "loop_proxy_depends_on_flavor_at_fixed_dimensionless_state":
            False,

        "hard_margin_scales_as_sqrt_flavor":
            True,

        "fourfold_flavor_hard_margin_ratio":
            hard_margin_ratio,

        "decision":
            "FLAVOR_ENERGY_SHORTCUT_CLOSED",
    },

    "loop_energy_pareto":
        rows,

    "selected_positive_band_partial_corridor": {
        "loop_cap":
            selected[
                "loop_cap"
            ],

        "r_mass_over_b":
            selected[
                "r"
            ],

        "u_mu_over_b":
            selected[
                "u"
            ],

        "loop_proxy":
            sel_met[
                "loop_proxy"
            ],

        "flavors":
            nf,

        "f_psi_ev":
            sel_phy[
                "f_psi_ev"
            ],

        "axial_b_ev":
            sel_phy[
                "axial_b_ev"
            ],

        "m_psi_ev":
            sel_phy[
                "m_psi_ev"
            ],

        "chemical_potential_ev":
            sel_phy[
                "chemical_potential_ev"
            ],

        "nda_cutoff_ev":
            sel_phy[
                "nda_cutoff_ev"
            ],

        "hard_scale_margin":
            sel_phy[
                "hard_scale_margin"
            ],

        "particle_number":
            selected[
                "particles"
            ],

        "field_energy_j":
            sel_met[
                "field_energy_j"
            ],

        "occupied_band_energy_j":
            sel_met[
                "band_energy_j"
            ],

        "pressure_mean_inventory_j":
            sel_met[
                "pressure_mean_inventory_j"
            ],

        "laue_support_floor_j":
            sel_met[
                "support_floor_j"
            ],

        "partial_conservative_floor_j":
            sel_partial_j,

        "remaining_to_strict_10mj_j":
            sel_headroom_j,

        "fixed_density_susceptibility_hat":
            sel_sus[
                "susceptibility_hat"
            ],

        "susceptibility_to_current_ratio":
            sel_sus[
                "susceptibility_to_current_ratio"
            ],

        "renormalized_dirac_sea_included":
            False,

        "scalar_loop_canonicalization_included":
            False,

        "complete_operating_ledger":
            False,

        "trusted_for_reachability":
            False,
    },

    "payload_trace_backreaction_scout": {
        "epsilon_at_100kev":
            epsilon_100,

        "transmission_at_100kev":
            trace_100[
                "uniform_sphere_transmission_scout"
            ],

        "naive_m4_scaling_valid_to_arbitrarily_low_M":
            False,

        "analytic_uniform_sphere_scout_optimum_scale_ev":
            scout_opt_scale_ev,

        "analytic_uniform_sphere_scout_optimum_energy_j":
            scout_opt_energy_j,

        "scout_is_energy_oracle":
            False,

        "finite_payload_nonlinear_pde_required":
            True,
    },

    "quantum_status": {
        "occupied_positive_bands":
            "INCLUDED",

        "renormalized_negative_energy_sea":
            "OPEN",

        "one_loop_axial_effective_action":
            "OPEN",

        "scalar_wavefunction_renormalization":
            "OPEN",

        "outward_metric_wilson_sign_after_matching":
            "OPEN",

        "naturalness_screened":
            False,
    },

    "agminer": {
        "old_v15_rejection_candidate_id":
            old_candidate.candidate_id,

        "controlled_nr_rejection_candidate_id":
            nr_candidate.candidate_id,

        "selected_partial_oracle_candidate_id":
            selected_candidate.candidate_id,

        "selected_oracle_priority":
            assessment.priority,

        "selected_oracle_trusted_for_reachability":
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
    "=== 032V16 RESULT ==="
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
    "DEMAG_Z="
    + format(
        demag_z,
        ".12e",
    )
)

print(
    "OLD_V15_EXACT_MU_EV="
    + format(
        old_mu_ev,
        ".12e",
    )
)

print(
    "OLD_V15_EXACT_HARD_MARGIN="
    + format(
        old_hard_margin,
        ".12e",
    )
)

print(
    "OLD_V15_EXACT_PARTIAL_GJ="
    + format(
        old_partial_j
        / 1.0e9,
        ".12e",
    )
)

print(
    "OLD_V15_MINIMAL_SINGLE_FLAVOR_MEANFIELD=RED"
)

print(
    "NR_STONER_MAX_AT_PF_OVER_M_0P5_LOOP_0P5="
    + format(
        nr_stoner_max,
        ".12e",
    )
)

print(
    "NR_MIN_LOOP_FOR_STONER="
    + format(
        nr_loop_required,
        ".12e",
    )
)

print(
    "CONTROLLED_NR_SPONTANEOUS_POLARIZATION=RED"
)

print(
    "FLAVOR_ENERGY_SHORTCUT=CLOSED"
)

print(
    "LOOP025_PARTIAL_MJ="
    + format(
        float(
            state_025[
                "metrics"
            ][
                "partial_conservative_floor_j"
            ]
        )
        / 1.0e6,
        ".12e",
    )
)

print(
    "LOOP030_PARTIAL_MJ="
    + format(
        sel_partial_j
        / 1.0e6,
        ".12e",
    )
)

print(
    "LOOP030_REMAINING_TO_10MJ_MJ="
    + format(
        sel_headroom_j
        / 1.0e6,
        ".12e",
    )
)

print(
    "LOOP030_NF="
    + str(
        nf
    )
)

print(
    "LOOP030_F_PSI_EV="
    + format(
        float(
            sel_phy[
                "f_psi_ev"
            ]
        ),
        ".12e",
    )
)

print(
    "LOOP030_B_EV="
    + format(
        float(
            sel_phy[
                "axial_b_ev"
            ]
        ),
        ".12e",
    )
)

print(
    "LOOP030_M_PSI_EV="
    + format(
        float(
            sel_phy[
                "m_psi_ev"
            ]
        ),
        ".12e",
    )
)

print(
    "LOOP030_MU_EV="
    + format(
        float(
            sel_phy[
                "chemical_potential_ev"
            ]
        ),
        ".12e",
    )
)

print(
    "LOOP030_NDA_CUTOFF_EV="
    + format(
        float(
            sel_phy[
                "nda_cutoff_ev"
            ]
        ),
        ".12e",
    )
)

print(
    "LOOP030_HARD_MARGIN="
    + format(
        float(
            sel_phy[
                "hard_scale_margin"
            ]
        ),
        ".12e",
    )
)

print(
    "LOOP030_SUSCEPTIBILITY_GAIN="
    + format(
        float(
            sel_sus[
                "susceptibility_to_current_ratio"
            ]
        ),
        ".12e",
    )
)

print(
    "LOOP050_SUSCEPTIBILITY_HAT="
    + format(
        float(
            state_050[
                "susceptibility"
            ][
                "susceptibility_hat"
            ]
        ),
        ".12e",
    )
)

print(
    "PAYLOAD_EPSILON_100KEV="
    + format(
        epsilon_100,
        ".12e",
    )
)

print(
    "PAYLOAD_TRANSMISSION_100KEV="
    + format(
        float(
            trace_100[
                "uniform_sphere_transmission_scout"
            ]
        ),
        ".12e",
    )
)

print(
    "PAYLOAD_SCOUT_OPTIMUM_SCALE_KEV="
    + format(
        scout_opt_scale_ev
        / 1.0e3,
        ".12e",
    )
)

print(
    "PAYLOAD_SCOUT_OPTIMUM_ENERGY_KJ="
    + format(
        scout_opt_energy_j
        / 1.0e3,
        ".12e",
    )
)

print(
    "PAYLOAD_SCOUT_IS_ENERGY_ORACLE=False"
)

print(
    "RENORMALIZED_DIRAC_SEA_INCLUDED=False"
)

print(
    "SCALAR_LOOP_CANONICALIZATION_INCLUDED=False"
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
