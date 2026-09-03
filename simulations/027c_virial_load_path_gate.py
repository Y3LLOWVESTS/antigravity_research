#!/usr/bin/env python3
"""027C — true-antigravity virial/load-path closure gate.

PURPOSE
-------
Test whether the corrected genuine-transfer 027B canonical-scalar shuttle can
retain true stand-off outward gravity after accounting for the missing
subvolume virial/stress-closure burden.

SCIENTIFIC QUESTION
-------------------
027B showed a reduced-source genuine-transfer witness near C ~ 3.08 when the
front/high-kernel cell could carry a strongly negative cycle-averaged active
source while global Laue compensation was placed at low kernel.

Can that advantage survive once the front cell's stress deficit must be
closed either locally or exported through a finite load path whose own
positive energy and active gravity are included?

MODEL
-----
The endpoint scalar waveform and causal transfer ledger are reconstructed
independently from 027B.

Only genuine transfer cases are admitted:

    delta_f >= 0.25
    N_tail = 2
    q_link = 2

For the front cell:

    E_H = <f_H>
    S_H = <q f_H>
    D_H = E_H - S_H

A periodic localized subvolume with no boundary stress flux cannot freely
retain D_H > 0.

Two closure controls are therefore tested.

LOCAL FRONT CLOSURE
-------------------
The most favorable local type-I DEC positive-pressure closure has

    q = S/E = 4

so full local closure requires

    E_close = D_H / 3

It is placed at the high-kernel cell.

REMOTE LOAD-PATH CLOSURE
------------------------
If the virial deficit is exported to the rear, use the direct axial load-path
proxy

    E_path = g_path D_H L / R

The g_path = 1 normalization follows the direct-member DEC estimate:
longitudinal stress magnitude cannot exceed energy density, combined with
characteristic front lever arm R and path length L.

g_path remains an explicit architecture parameter because a real distributed
field geometry may transmit traction differently.

The run solves for the largest g_path compatible with the established source
benchmarks instead of pretending the proxy is a universal theorem.

The primary path active-source benchmark is

    q_path = 2

GLOBAL LAUE CLOSURE
-------------------
After endpoint, causal-link, and local/path contributions are included, any
remaining positive Laue deficit is closed with minimum DEC-saturating

    q = 4

compensation placed at a lower-kernel rear location.

Promotion forbids helpful q = -2 compensation.

FINITE PAYLOAD
--------------
Search candidates are ranked at payload center.

Promotion candidates then undergo dense axisymmetric surface audits at

    R_payload/h = 0.25
    R_payload/h = 0.50

with 17 polar samples per radius plus payload center.

Source cells are represented by spherically symmetric exterior point fields.
Transfer and load channels are uniform axial line sources.

For a line extending from d_H to d_L,

    K_line(rho,z)
      =
    [1/R_H - 1/R_L] / (d_L-d_H)

for its exact z-component kernel.

Promotion requires outward sign at every sampled payload location.

C_payload is defined from the weakest sampled outward field.

PROMOTION
---------
MAJOR_GREEN:

    g_path = 1
    and
    C_payload < C_024D

on BOTH independent Sobol campaigns.

GREEN:

    g_path = 1
    and
    C_payload < C_006D

on BOTH campaigns.

YELLOW:

    zero-cost export survives,
    but g_path = 1 fails.

Report the maximum allowed g_path and require a concrete distributed stress
geometry capable of realizing it before any expensive PDE.

RED:

    even zero-cost virial export cannot beat 006D after finite-payload audit.

LIMITATIONS
-----------
This is a reduced conservation/load-path gate.

It does NOT establish:

- microscopic field realization;
- pointwise d_mu T^{mu nu}=0;
- a transfer-field Lagrangian;
- reaction momentum closure;
- radiation lifetime;
- unrestricted stability;
- nonlinear GR;
- escape from 1/G scaling;
- a practical antigravity device.

CLAIM CLASSIFICATION
--------------------
REDUCED_SOURCE_CONSERVATION_FALSIFICATION_GATE

NOVEL PHYSICS CLAIM
-------------------
NO
"""

from __future__ import annotations

import csv
import json
import math
import os
from pathlib import Path

import numpy as np
from scipy.stats import qmc


C_006D = 23.591586299249
C_024D = 6.610457607426174

B7_NEG = 0.051465043743791114

EXPECTED_027B_GENUINE_CENTER = 3.08075881130598

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "results" / "data"

LINEAGE = DATA / "027b_causal_field_state_shuttle_summary.json"

OUT_JSON = DATA / "027c_virial_load_path_gate_summary.json"
OUT_CSV = DATA / "027c_virial_load_path_seed_summary.csv"
OUT_WILDCARD = DATA / "027c_virial_load_path_wildcard_audit.csv"


M_EXP = int(
    os.environ.get(
        "AG027C_SOBOL_M",
        "14",
    )
)

SEEDS = (
    2703,
    2704,
)

TOP_PER_BATCH = 3

DENSE_KEEP = 1200

Q_LINK = 2.0
Q_PATH = 2.0

PAYLOAD_RADII = (
    0.25,
    0.50,
)

PAYLOAD_MU = np.linspace(
    -1.0,
    1.0,
    17,
)

BLIND_WILDCARD_G = (
    0.625,
    1.6,
    1.875,
    3.125,
    5.0,
)


if not LINEAGE.exists():
    raise FileNotFoundError(
        f"Required 027B lineage missing: {LINEAGE}"
    )

with LINEAGE.open(
    "r",
    encoding="utf-8",
) as f:
    lineage_json = json.load(f)


def potential_v(
    x: np.ndarray,
    a: float,
    b: float,
) -> np.ndarray:
    """Return normalized quadratic-quartic-sextic scalar potential."""
    return (
        (1.0 + a + b) * x**2
        - (a + 2.0 * b) * x**4
        + b * x**6
    )


def waveform_metrics(
    a: float,
    b: float,
    n: int = 32768,
) -> dict | None:
    """Reconstruct one 027A canonical-scalar periodic waveform."""
    u = (
        np.arange(
            n,
            dtype=float,
        )
        + 0.5
    ) * (
        0.5
        * math.pi
        / n
    )

    du = (
        0.5
        * math.pi
        / n
    )

    x = np.sin(u)
    c = np.cos(u)

    v = potential_v(
        x,
        a,
        b,
    )

    one_minus = (
        1.0
        - v
    )

    if (
        np.min(v)
        < -1.0e-10
        or
        np.min(one_minus)
        <= 0.0
    ):
        return None

    w = (
        c
        / np.sqrt(
            2.0
            * one_minus
        )
        * du
    )

    tq = float(
        np.sum(w)
    )

    w /= np.sum(w)

    q = (
        4.0
        - 6.0
        * v
    )

    omega = (
        math.pi
        / (
            2.0
            * tq
        )
    )

    mass = math.sqrt(
        2.0
        * (
            1.0
            + a
            + b
        )
    )

    chi = (
        omega
        / mass
    )

    if not (
        0.0
        < chi
        < 1.0
    ):
        return None

    return {
        "a": float(a),
        "b": float(b),
        "chi": float(chi),
        "q": q,
        "w": w,
        "qbar": float(
            np.sum(
                w
                * q
            )
        ),
        "negative_duty": float(
            np.sum(
                w[
                    q < 0.0
                ]
            )
        ),
    }


POTENTIALS = [
    (
        "027A_rank1",
        0.9884588225092739,
        1.1226674255818845,
    ),
    (
        "027A_rank2",
        0.99178865,
        1.05650720,
    ),
    (
        "027A_rank3",
        0.9943639179505408,
        0.9764195133049375,
    ),
    (
        "027A_rank4",
        0.96766212,
        1.31771112,
    ),
    (
        "027A_rank5",
        0.98736931,
        1.09825616,
    ),
    (
        "027A_rank6",
        0.98522712,
        1.12658802,
    ),
    (
        "027A_rank7",
        0.97569150,
        1.23550641,
    ),
    (
        "027A_rank8",
        0.98080928,
        1.17179208,
    ),
    (
        "027A_rank9",
        0.99091627,
        1.00932340,
    ),
    (
        "027A_rank10",
        0.97098871,
        1.26800795,
    ),
    (
        "027A_point_survivor",
        0.7703859870461747,
        0.1542352065658195,
    ),
]


WAVES = []

for name, a, b in POTENTIALS:
    m = waveform_metrics(
        a,
        b,
    )

    if m is not None:
        m["name"] = name
        WAVES.append(m)


if not WAVES:
    raise RuntimeError(
        "No valid 027A scalar waveforms"
    )


QCUTS = np.linspace(
    -1.75,
    3.50,
    15,
)


ROUTINGS = [
    (
        0.00,
        0.25,
    ),
    (
        0.25,
        0.25,
    ),
    (
        0.50,
        0.25,
    ),
    (
        0.75,
        0.25,
    ),
    (
        0.00,
        0.50,
    ),
    (
        0.25,
        0.50,
    ),
    (
        0.50,
        0.50,
    ),
    (
        0.00,
        0.75,
    ),
    (
        0.25,
        0.75,
    ),
    (
        0.00,
        1.00,
    ),
]


def point_kernel(
    rho: float,
    z: float,
    d: float,
) -> float:
    """Return positive z-kernel magnitude for an axial point source."""
    dz = (
        z
        + d
    )

    return (
        dz
        / (
            rho
            * rho
            + dz
            * dz
        )
        ** 1.5
    )


def line_kernel(
    rho: float,
    z: float,
    d_high: float,
    d_low: float,
) -> float:
    """Return exact z-kernel for a uniform axial line source."""
    length = (
        d_low
        - d_high
    )

    rh = math.sqrt(
        rho
        * rho
        + (
            z
            + d_high
        )
        ** 2
    )

    rl = math.sqrt(
        rho
        * rho
        + (
            z
            + d_low
        )
        ** 2
    )

    return (
        1.0
        / rh
        - 1.0
        / rl
    ) / length


def append_extrema(
    store: list,
    score: np.ndarray,
    meta_fn,
    n: int,
    largest: bool,
) -> None:
    """Retain a few extrema from one vectorized geometry batch."""
    inds = np.flatnonzero(
        np.isfinite(
            score
        )
    )

    if inds.size == 0:
        return

    n = min(
        n,
        inds.size,
    )

    vals = score[
        inds
    ]

    if largest:
        pick = np.argpartition(
            vals,
            -n,
        )[
            -n:
        ]
    else:
        pick = np.argpartition(
            vals,
            n - 1,
        )[
            :n
        ]

    for j in inds[
        pick
    ]:
        store.append(
            (
                float(
                    score[
                        j
                    ]
                ),
                meta_fn(
                    int(j)
                ),
            )
        )


def dense_payload_audit(
    meta: dict,
    mode: str,
    g_path: float = 0.0,
) -> dict | None:
    """Audit a retained candidate over the full finite-payload sample set."""
    d_high = meta[
        "d_high"
    ]

    d_low = meta[
        "d_low"
    ]

    d_comp = meta[
        "d_comp"
    ]

    separation = meta[
        "separation"
    ]

    radius = meta[
        "radius"
    ]

    qbar = meta[
        "qbar"
    ]

    s_high = meta[
        "S_high"
    ]

    d_high_virial = meta[
        "D_high"
    ]

    e_link = meta[
        "E_link"
    ]

    d0 = meta[
        "D0"
    ]

    neg_duty = meta[
        "negative_duty"
    ]

    e_extra = 0.0
    m_local = 0.0
    m_path = 0.0

    if mode == "GLOBAL_CONTROL":
        d_remaining = d0

    elif mode == "LOCAL_FRONT_CLOSURE":
        e_extra = (
            d_high_virial
            / 3.0
        )

        m_local = (
            4.0
            * e_extra
        )

        d_remaining = (
            d0
            - d_high_virial
        )

    elif mode == "REMOTE_PATH":
        load_coeff = (
            d_high_virial
            * separation
            / radius
        )

        e_extra = (
            g_path
            * load_coeff
        )

        m_path = (
            Q_PATH
            * e_extra
        )

        d_remaining = (
            d0
            - (
                Q_PATH
                - 1.0
            )
            * e_extra
        )

    else:
        raise ValueError(
            mode
        )

    if (
        d_remaining
        < -1.0e-13
    ):
        return None

    d_remaining = max(
        d_remaining,
        0.0,
    )

    e_comp = (
        d_remaining
        / 3.0
    )

    e_total = (
        1.0
        + e_link
        + e_extra
        + e_comp
    )

    if (
        neg_duty
        / e_total
        <= B7_NEG
    ):
        return None

    if (
        e_link
        / e_total
        >= 0.50
    ):
        return None

    if (
        mode
        == "REMOTE_PATH"
        and
        e_extra
        / e_total
        >= 0.50
    ):
        return None

    samples = [
        (
            "CENTER",
            0.0,
            0.0,
        )
    ]

    for payload_radius in PAYLOAD_RADII:
        for mu in PAYLOAD_MU:
            rho = (
                payload_radius
                * math.sqrt(
                    max(
                        0.0,
                        1.0
                        - float(mu)
                        ** 2,
                    )
                )
            )

            z = (
                payload_radius
                * float(mu)
            )

            samples.append(
                (
                    (
                        f"R{payload_radius:.2f}"
                        f"_MU{mu:+.4f}"
                    ),
                    rho,
                    z,
                )
            )

    ledger = []

    for label, rho, z in samples:
        k_high = point_kernel(
            rho,
            z,
            d_high,
        )

        k_low = point_kernel(
            rho,
            z,
            d_low,
        )

        k_comp = point_kernel(
            rho,
            z,
            d_comp,
        )

        k_line = line_kernel(
            rho,
            z,
            d_high,
            d_low,
        )

        a_out = -(
            s_high
            * k_high

            + (
                qbar
                - s_high
            )
            * k_low

            + Q_LINK
            * e_link
            * k_line

            + m_local
            * k_high

            + m_path
            * k_line

            + 4.0
            * e_comp
            * k_comp
        )

        ledger.append(
            (
                label,
                a_out,
            )
        )

    min_label, min_a = min(
        ledger,
        key=lambda item: item[
            1
        ],
    )

    if (
        min_a
        <= 0.0
    ):
        return None

    return {
        "C_payload": (
            e_total
            / min_a
        ),
        "A_payload_min": min_a,
        "payload_min_location": min_label,
        "E_total": e_total,
        "E_link": e_link,
        "E_extra": e_extra,
        "E_comp": e_comp,
        "link_fraction": (
            e_link
            / e_total
        ),
        "extra_fraction": (
            e_extra
            / e_total
        ),
        "negative_active_participation": (
            neg_duty
            / e_total
        ),
        "g_path": g_path,
        "mode": mode,
        "meta": meta,
    }


def dense_gmax(
    meta: dict,
    target_c: float,
    center_upper: float,
) -> tuple[
    float,
    dict | None,
]:
    """Refine the maximum path factor allowed by dense payload audit."""
    a0 = dense_payload_audit(
        meta,
        "REMOTE_PATH",
        0.0,
    )

    if (
        a0 is None
        or
        a0[
            "C_payload"
        ]
        >= target_c
    ):
        return (
            -math.inf,
            None,
        )

    lo = 0.0

    hi = max(
        0.0,
        min(
            center_upper,
            2.0,
        ),
    )

    if hi <= 0.0:
        return (
            0.0,
            a0,
        )

    ahi = dense_payload_audit(
        meta,
        "REMOTE_PATH",
        hi,
    )

    if (
        ahi is not None
        and
        ahi[
            "C_payload"
        ]
        < target_c
    ):
        return (
            hi,
            ahi,
        )

    for _ in range(
        48
    ):
        mid = (
            0.5
            * (
                lo
                + hi
            )
        )

        am = dense_payload_audit(
            meta,
            "REMOTE_PATH",
            mid,
        )

        if (
            am is not None
            and
            am[
                "C_payload"
            ]
            < target_c
        ):
            lo = mid

        else:
            hi = mid

    return (
        lo,
        dense_payload_audit(
            meta,
            "REMOTE_PATH",
            lo,
        ),
    )


def run_seed(
    seed: int,
) -> dict:
    """Run one independent Sobol geometry campaign."""
    print(
        (
            f"027C_SEED_START={seed} "
            f"SOBOL_M={M_EXP}"
        ),
        flush=True,
    )

    u = qmc.Sobol(
        d=3,
        scramble=True,
        seed=seed,
    ).random_base2(
        M_EXP
    )

    radius = (
        0.03
        + u[
            :,
            0,
        ]
        * (
            0.40
            - 0.03
        )
    )

    clearance = (
        u[
            :,
            1,
        ]
        * 0.50
    )

    separation = np.exp(
        math.log(
            0.20
        )
        + u[
            :,
            2,
        ]
        * (
            math.log(
                10.0
            )
            - math.log(
                0.20
            )
        )
    )

    d_high = (
        1.0
        + radius
        + clearance
    )

    d_low = (
        d_high
        + separation
    )

    d_comp = (
        d_low
        + 0.50
        * separation
    )

    k_high = (
        1.0
        / d_high
        ** 2
    )

    k_low = (
        1.0
        / d_low
        ** 2
    )

    k_line = (
        (
            1.0
            / d_high
        )
        - (
            1.0
            / d_low
        )
    ) / separation

    k_comp = (
        1.0
        / d_comp
        ** 2
    )

    global_rows = []
    local_rows = []
    direct_rows = []

    threshold_rows = {
        C_006D: [],
        C_024D: [],
    }

    best_center_control = (
        math.inf,
        None,
    )

    for wi, m in enumerate(
        WAVES,
        start=1,
    ):
        print(
            (
                f"027C_SEED={seed} "
                f"POTENTIAL={wi}/{len(WAVES)} "
                f"NAME={m['name']}"
            ),
            flush=True,
        )

        q = m[
            "q"
        ]

        w = m[
            "w"
        ]

        qbar = m[
            "qbar"
        ]

        chi = m[
            "chi"
        ]

        omega_min = (
            chi
            * 2.0
            / (
                radius
                * math.sqrt(
                    1.0
                    - chi
                    * chi
                )
            )
        )

        for qcut in QCUTS:
            mask = (
                q
                <= qcut
            )

            qmask = float(
                np.sum(
                    w[
                        mask
                    ]
                    * q[
                        mask
                    ]
                )
            )

            route_duty = float(
                np.sum(
                    w[
                        mask
                    ]
                )
            )

            for f_lo, delta_f in ROUTINGS:
                if (
                    f_lo
                    + delta_f
                    > 1.0
                    + 1.0e-12
                ):
                    continue

                if (
                    delta_f
                    < 0.25
                    - 1.0e-12
                ):
                    raise AssertionError(
                        "Zero/near-zero transfer entered 027C promotion scan"
                    )

                e_high = (
                    f_lo
                    + delta_f
                    * route_duty
                )

                s_high = (
                    f_lo
                    * qbar
                    + delta_f
                    * qmask
                )

                d_high_virial = max(
                    e_high
                    - s_high,
                    0.0,
                )

                a_endpoint = -(
                    k_high
                    * s_high
                    + k_low
                    * (
                        qbar
                        - s_high
                    )
                )

                e_link = (
                    2.0
                    / math.pi
                    * delta_f
                    * omega_min
                    * separation
                )

                a_link = -(
                    Q_LINK
                    * e_link
                    * k_line
                )

                e_pre = (
                    1.0
                    + e_link
                )

                s_pre = (
                    qbar
                    + Q_LINK
                    * e_link
                )

                d0 = (
                    e_pre
                    - s_pre
                )

                positive_comp = (
                    d0
                    >= 0.0
                )

                e_comp0 = np.where(
                    positive_comp,
                    d0
                    / 3.0,
                    np.nan,
                )

                e_base = (
                    e_pre
                    + e_comp0
                )

                a_base = (
                    a_endpoint
                    + a_link
                    - 4.0
                    * e_comp0
                    * k_comp
                )

                neg_part_base = (
                    m[
                        "negative_duty"
                    ]
                    / e_base
                )

                valid_base = (
                    positive_comp
                    & (
                        a_base
                        > 0.0
                    )
                    & (
                        neg_part_base
                        > B7_NEG
                    )
                    & (
                        e_link
                        / e_base
                        < 0.50
                    )
                )

                c_base = np.where(
                    valid_base,
                    e_base
                    / a_base,
                    np.inf,
                )

                def meta_at(
                    j: int,
                ) -> dict:
                    return {
                        "seed": seed,
                        "potential": m[
                            "name"
                        ],
                        "pot_a": m[
                            "a"
                        ],
                        "pot_b": m[
                            "b"
                        ],
                        "chi": chi,
                        "qbar": qbar,
                        "qcut": float(
                            qcut
                        ),
                        "qmask": qmask,
                        "route_duty": route_duty,
                        "negative_duty": m[
                            "negative_duty"
                        ],
                        "f_lo": f_lo,
                        "f_hi": (
                            f_lo
                            + delta_f
                        ),
                        "delta_f": delta_f,
                        "E_high": e_high,
                        "S_high": s_high,
                        "D_high": d_high_virial,
                        "radius": float(
                            radius[
                                j
                            ]
                        ),
                        "clearance": float(
                            clearance[
                                j
                            ]
                        ),
                        "separation": float(
                            separation[
                                j
                            ]
                        ),
                        "d_high": float(
                            d_high[
                                j
                            ]
                        ),
                        "d_low": float(
                            d_low[
                                j
                            ]
                        ),
                        "d_comp": float(
                            d_comp[
                                j
                            ]
                        ),
                        "K_ratio": float(
                            k_high[
                                j
                            ]
                            / k_low[
                                j
                            ]
                        ),
                        "E_link": float(
                            e_link[
                                j
                            ]
                        ),
                        "D0": float(
                            d0[
                                j
                            ]
                        ),
                        "C_center_global_control": float(
                            c_base[
                                j
                            ]
                        ),
                    }

                finite_inds = np.flatnonzero(
                    np.isfinite(
                        c_base
                    )
                )

                if finite_inds.size:
                    j0 = int(
                        finite_inds[
                            np.argmin(
                                c_base[
                                    finite_inds
                                ]
                            )
                        ]
                    )

                    if (
                        c_base[
                            j0
                        ]
                        < best_center_control[
                            0
                        ]
                    ):
                        best_center_control = (
                            float(
                                c_base[
                                    j0
                                ]
                            ),
                            meta_at(
                                j0
                            ),
                        )

                append_extrema(
                    global_rows,
                    c_base,
                    meta_at,
                    TOP_PER_BATCH,
                    False,
                )

                e_close = (
                    d_high_virial
                    / 3.0
                )

                d_local = (
                    d0
                    - d_high_virial
                )

                local_positive_comp = (
                    d_local
                    >= 0.0
                )

                e_local_comp = np.where(
                    local_positive_comp,
                    d_local
                    / 3.0,
                    np.nan,
                )

                e_local_total = (
                    1.0
                    + e_link
                    + e_close
                    + e_local_comp
                )

                a_local = (
                    a_endpoint
                    + a_link
                    - 4.0
                    * e_close
                    * k_high
                    - 4.0
                    * e_local_comp
                    * k_comp
                )

                c_local = np.where(
                    local_positive_comp
                    & (
                        a_local
                        > 0.0
                    )
                    & (
                        m[
                            "negative_duty"
                        ]
                        / e_local_total
                        > B7_NEG
                    ),
                    e_local_total
                    / a_local,
                    np.inf,
                )

                append_extrema(
                    local_rows,
                    c_local,
                    meta_at,
                    TOP_PER_BATCH,
                    False,
                )

                load_coeff = (
                    d_high_virial
                    * separation
                    / radius
                )

                e_slope = (
                    2.0
                    / 3.0
                    * load_coeff
                )

                a_slope = (
                    load_coeff
                    * (
                        -Q_PATH
                        * k_line
                        + (
                            4.0
                            / 3.0
                        )
                        * k_comp
                    )
                )

                with np.errstate(
                    divide="ignore",
                    invalid="ignore",
                ):
                    g_comp = np.where(
                        load_coeff
                        > 0.0,
                        d0
                        / load_coeff,
                        np.inf,
                    )

                    g_a = np.where(
                        a_slope
                        < 0.0,
                        a_base
                        / (
                            -a_slope
                        ),
                        np.inf,
                    )

                    g_neg = np.where(
                        e_slope
                        > 0.0,
                        (
                            m[
                                "negative_duty"
                            ]
                            / B7_NEG
                            - e_base
                        )
                        / e_slope,
                        np.inf,
                    )

                    frac_den = (
                        load_coeff
                        - 0.5
                        * e_slope
                    )

                    g_fraction = np.where(
                        frac_den
                        > 0.0,
                        0.5
                        * e_base
                        / frac_den,
                        np.inf,
                    )

                for target in (
                    C_006D,
                    C_024D,
                ):
                    margin = (
                        target
                        * a_base
                        - e_base
                    )

                    denom = (
                        e_slope
                        - target
                        * a_slope
                    )

                    with np.errstate(
                        divide="ignore",
                        invalid="ignore",
                    ):
                        g_c = np.where(
                            (
                                margin
                                > 0.0
                            )
                            & (
                                denom
                                > 0.0
                            ),
                            margin
                            / denom,
                            np.where(
                                (
                                    margin
                                    > 0.0
                                )
                                & (
                                    denom
                                    <= 0.0
                                ),
                                np.inf,
                                -np.inf,
                            ),
                        )

                    gmax = np.minimum.reduce(
                        (
                            g_comp,
                            g_a,
                            g_neg,
                            g_fraction,
                            g_c,
                        )
                    )

                    gmax = np.where(
                        valid_base
                        & (
                            d_high_virial
                            > 0.0
                        ),
                        gmax,
                        -np.inf,
                    )

                    append_extrema(
                        threshold_rows[
                            target
                        ],
                        gmax,
                        meta_at,
                        TOP_PER_BATCH
                        + 1,
                        True,
                    )

                g = 1.0

                e_direct = (
                    e_base
                    + e_slope
                    * g
                )

                a_direct = (
                    a_base
                    + a_slope
                    * g
                )

                direct_valid = (
                    valid_base
                    & (
                        g
                        <= g_comp
                    )
                    & (
                        g
                        <= g_neg
                    )
                    & (
                        g
                        <= g_fraction
                    )
                    & (
                        a_direct
                        > 0.0
                    )
                )

                c_direct = np.where(
                    direct_valid,
                    e_direct
                    / a_direct,
                    np.inf,
                )

                append_extrema(
                    direct_rows,
                    c_direct,
                    meta_at,
                    TOP_PER_BATCH,
                    False,
                )

    def best_dense(
        rows: list,
        mode: str,
        g: float = 0.0,
    ) -> dict | None:
        best = None

        for _, meta in sorted(
            rows,
            key=lambda item: item[
                0
            ],
        )[
            :DENSE_KEEP
        ]:
            audit = dense_payload_audit(
                meta,
                mode,
                g,
            )

            if (
                audit is not None
                and
                (
                    best is None
                    or
                    audit[
                        "C_payload"
                    ]
                    < best[
                        "C_payload"
                    ]
                )
            ):
                best = audit

        return best

    best_global = best_dense(
        global_rows,
        "GLOBAL_CONTROL",
    )

    best_local = best_dense(
        local_rows,
        "LOCAL_FRONT_CLOSURE",
    )

    best_direct = best_dense(
        direct_rows,
        "REMOTE_PATH",
        1.0,
    )

    thresholds = {}

    for target in (
        C_006D,
        C_024D,
    ):
        best_g = -math.inf
        best_audit = None

        candidates = sorted(
            threshold_rows[
                target
            ],
            key=lambda item: item[
                0
            ],
            reverse=True,
        )[
            :DENSE_KEEP
        ]

        for center_gmax, meta in candidates:
            g_dense, audit = dense_gmax(
                meta,
                target,
                center_gmax,
            )

            if (
                g_dense
                > best_g
            ):
                best_g = g_dense
                best_audit = audit

        thresholds[
            str(
                target
            )
        ] = {
            "g_path_max": (
                best_g
                if math.isfinite(
                    best_g
                )
                else None
            ),
            "audit": best_audit,
        }

    wildcard_rows = []

    wildcard_meta = None

    if best_global is not None:
        wildcard_meta = best_global[
            "meta"
        ]

    if wildcard_meta is not None:
        for g in BLIND_WILDCARD_G:
            a = dense_payload_audit(
                wildcard_meta,
                "REMOTE_PATH",
                g,
            )

            wildcard_rows.append(
                {
                    "seed": seed,
                    "g_path": g,
                    "status": (
                        "OUTWARD"
                        if a is not None
                        else "NO_STRICT_SURVIVOR"
                    ),
                    "C_payload": (
                        None
                        if a is None
                        else a[
                            "C_payload"
                        ]
                    ),
                    "selection_role":
                        "BLIND_NON_EVIDENTIARY_EXCLUDED",
                }
            )

    result = {
        "seed": seed,
        "sobol_points": (
            2
            ** M_EXP
        ),
        "best_center_global_control": (
            best_center_control[
                0
            ]
            if math.isfinite(
                best_center_control[
                    0
                ]
            )
            else None
        ),
        "best_center_global_control_meta":
            best_center_control[
                1
            ],
        "best_dense_global_control":
            best_global,
        "best_dense_local_front_closure":
            best_local,
        "best_dense_direct_g1":
            best_direct,
        "thresholds":
            thresholds,
        "wildcards":
            wildcard_rows,
    }

    print(
        f"027C_SEED_COMPLETE={seed}",
        flush=True,
    )

    print(
        (
            f"SEED_{seed}"
            f"_BEST_CENTER_CONTROL="
            f"{result['best_center_global_control']}"
        ),
        flush=True,
    )

    print(
        (
            f"SEED_{seed}"
            f"_BEST_PAYLOAD_GLOBAL="
        )
        + (
            "NONE"
            if best_global is None
            else (
                f"{best_global['C_payload']:.12e}"
            )
        ),
        flush=True,
    )

    print(
        (
            f"SEED_{seed}"
            f"_BEST_PAYLOAD_LOCAL="
        )
        + (
            "NONE"
            if best_local is None
            else (
                f"{best_local['C_payload']:.12e}"
            )
        ),
        flush=True,
    )

    print(
        (
            f"SEED_{seed}"
            f"_BEST_PAYLOAD_G1="
        )
        + (
            "NONE"
            if best_direct is None
            else (
                f"{best_direct['C_payload']:.12e}"
            )
        ),
        flush=True,
    )

    print(
        (
            f"SEED_{seed}"
            f"_GMAX_006D="
            f"{thresholds[str(C_006D)]['g_path_max']}"
        ),
        flush=True,
    )

    print(
        (
            f"SEED_{seed}"
            f"_GMAX_024D="
            f"{thresholds[str(C_024D)]['g_path_max']}"
        ),
        flush=True,
    )

    return result


results = [
    run_seed(
        seed
    )
    for seed in SEEDS
]


center_vals = [
    r[
        "best_center_global_control"
    ]
    for r in results
    if r[
        "best_center_global_control"
    ]
    is not None
]


center_lineage_relerr = None

if center_vals:
    center_lineage_relerr = min(
        abs(
            v
            - EXPECTED_027B_GENUINE_CENTER
        )
        / EXPECTED_027B_GENUINE_CENTER
        for v in center_vals
    )


g1_rows = [
    r[
        "best_dense_direct_g1"
    ]
    for r in results
]


g1_both = all(
    row is not None
    for row in g1_rows
)


g1_worst_c = (
    max(
        row[
            "C_payload"
        ]
        for row in g1_rows
    )
    if g1_both
    else math.inf
)


robust_g006 = None
robust_g024 = None


if all(
    r[
        "thresholds"
    ][
        str(
            C_006D
        )
    ][
        "g_path_max"
    ]
    is not None
    for r in results
):
    robust_g006 = min(
        r[
            "thresholds"
        ][
            str(
                C_006D
            )
        ][
            "g_path_max"
        ]
        for r in results
    )


if all(
    r[
        "thresholds"
    ][
        str(
            C_024D
        )
    ][
        "g_path_max"
    ]
    is not None
    for r in results
):
    robust_g024 = min(
        r[
            "thresholds"
        ][
            str(
                C_024D
            )
        ][
            "g_path_max"
        ]
        for r in results
    )


if (
    g1_both
    and
    g1_worst_c
    < C_024D
):
    decision = (
        "MAJOR_GREEN_DIRECT_DEC_LOAD_PATH_"
        "BEATS_024D_BOTH_SEEDS"
    )

    next_step = (
        "AUTHORIZE_EXPLICIT_LOCALLY_CONSERVED_"
        "SHUTTLE_FIELD_PDE"
    )

    source_80 = True

elif (
    g1_both
    and
    g1_worst_c
    < C_006D
):
    decision = (
        "GREEN_DIRECT_DEC_LOAD_PATH_"
        "BEATS_006D_BOTH_SEEDS"
    )

    next_step = (
        "AUTHORIZE_MINIMAL_TRANSFER_FIELD_PDE_"
        "WITH_STRICT_SUPPORT_LEDGER"
    )

    source_80 = False

elif (
    robust_g006 is not None
    and
    robust_g006
    > 0.0
):
    decision = (
        "YELLOW_ZERO_COST_EXPORT_SURVIVES_"
        "BUT_DIRECT_LOAD_PATH_FAILS"
    )

    next_step = (
        "DERIVE_EXPLICIT_DISTRIBUTED_STRESS_GEOMETRY_"
        "BEATING_REQUIRED_G_PATH_BEFORE_PDE"
    )

    source_80 = False

else:
    decision = (
        "RED_VIRIAL_EXPORT_CANNOT_BEAT_006D_"
        "AFTER_FINITE_PAYLOAD_GATE"
    )

    next_step = (
        "CLOSE_THIS_SHUTTLE_CLOSURE_CLASS_"
        "AND_RERANK_SOURCE_ENGINE"
    )

    source_80 = False


summary = {
    "branch":
        "TRUE_ANTIGRAVITY",

    "simulation":
        "027C",

    "question":
        (
            "Does genuine 027B field-state shuttling survive "
            "subvolume virial closure and DEC-limited stress "
            "transport at true stand-off for a finite payload?"
        ),

    "lineage": {
        "027b_saved_decision_known_to_include_zero_transfer_gate_bug":
            lineage_json.get(
                "decision"
            ),

        "corrected_027b_genuine_center_reference_C":
            EXPECTED_027B_GENUINE_CENTER,

        "closest_independent_center_reconstruction_relerr":
            center_lineage_relerr,

        "C_006D":
            C_006D,

        "C_024D":
            C_024D,

        "B7_negative_active_fraction":
            B7_NEG,
    },

    "controls": {
        "genuine_transfer_min_delta_f":
            0.25,

        "N_tail":
            2,

        "q_link":
            Q_LINK,

        "q_path":
            Q_PATH,

        "payload_radii_h":
            list(
                PAYLOAD_RADII
            ),

        "payload_mu_samples_per_radius":
            int(
                len(
                    PAYLOAD_MU
                )
            ),

        "direct_path_normalization":
            (
                "E_path = g_path D_H L/R; "
                "g_path=1 is direct axial DEC "
                "load-member benchmark"
            ),
    },

    "seeds":
        results,

    "robust": {
        "direct_g1_both_seeds":
            g1_both,

        "direct_g1_worst_C_payload":
            (
                None
                if not math.isfinite(
                    g1_worst_c
                )
                else g1_worst_c
            ),

        "g_path_max_beating_006D_both_seeds":
            robust_g006,

        "g_path_max_beating_024D_both_seeds":
            robust_g024,
    },

    "decision":
        decision,

    "next":
        next_step,

    "source_engine_80_heuristic_authorized":
        source_80,

    "overall_practical_antigravity_80_heuristic_authorized":
        False,

    "mandatory_parallel_credibility_branch":
        "026C_N89_FORCE_CONVERGENCE",

    "claims": {
        "microscopic_field_realization":
            False,

        "pointwise_local_Tmunu_conservation":
            False,

        "reaction_momentum_closed":
            False,

        "radiation_lifetime_closed":
            False,

        "full_stability":
            False,

        "nonlinear_GR":
            False,

        "removes_1_over_G_scaling":
            False,

        "practical_antigravity_device":
            False,
    },
}


with OUT_JSON.open(
    "w",
    encoding="utf-8",
) as f:
    json.dump(
        summary,
        f,
        indent=2,
        sort_keys=True,
    )


with OUT_CSV.open(
    "w",
    newline="",
    encoding="utf-8",
) as f:
    fields = [
        "seed",
        "best_center_global_control",
        "best_dense_global_control_C",
        "best_dense_local_front_closure_C",
        "best_dense_direct_g1_C",
        "g_path_max_006D",
        "g_path_max_024D",
    ]

    writer = csv.DictWriter(
        f,
        fieldnames=fields,
    )

    writer.writeheader()

    for r in results:
        writer.writerow(
            {
                "seed":
                    r[
                        "seed"
                    ],

                "best_center_global_control":
                    r[
                        "best_center_global_control"
                    ],

                "best_dense_global_control_C":
                    (
                        None
                        if r[
                            "best_dense_global_control"
                        ]
                        is None
                        else r[
                            "best_dense_global_control"
                        ][
                            "C_payload"
                        ]
                    ),

                "best_dense_local_front_closure_C":
                    (
                        None
                        if r[
                            "best_dense_local_front_closure"
                        ]
                        is None
                        else r[
                            "best_dense_local_front_closure"
                        ][
                            "C_payload"
                        ]
                    ),

                "best_dense_direct_g1_C":
                    (
                        None
                        if r[
                            "best_dense_direct_g1"
                        ]
                        is None
                        else r[
                            "best_dense_direct_g1"
                        ][
                            "C_payload"
                        ]
                    ),

                "g_path_max_006D":
                    r[
                        "thresholds"
                    ][
                        str(
                            C_006D
                        )
                    ][
                        "g_path_max"
                    ],

                "g_path_max_024D":
                    r[
                        "thresholds"
                    ][
                        str(
                            C_024D
                        )
                    ][
                        "g_path_max"
                    ],
            }
        )


with OUT_WILDCARD.open(
    "w",
    newline="",
    encoding="utf-8",
) as f:
    fields = [
        "seed",
        "g_path",
        "status",
        "C_payload",
        "selection_role",
    ]

    writer = csv.DictWriter(
        f,
        fieldnames=fields,
    )

    writer.writeheader()

    for r in results:
        writer.writerows(
            r[
                "wildcards"
            ]
        )


print(
    "=== 027C VIRIAL / LOAD-PATH GATE ==="
)

print(
    f"SOBOL_M={M_EXP}"
)

print(
    f"SOBOL_POINTS_PER_SEED={2**M_EXP}"
)

print(
    f"POTENTIALS={len(WAVES)}"
)

print(
    "GENUINE_TRANSFER_ONLY=YES"
)

print(
    "DELTA_F_MIN=0.25"
)

print(
    "N_TAIL=2"
)

print(
    "Q_LINK=2"
)

print(
    "Q_PATH=2"
)

print(
    (
        "CORRECTED_027B_REFERENCE_C="
        f"{EXPECTED_027B_GENUINE_CENTER:.15e}"
    )
)

print(
    (
        "CENTER_LINEAGE_CLOSEST_RELERR="
        f"{center_lineage_relerr}"
    )
)

print()

for r in results:
    print(
        f"SEED={r['seed']}"
    )

    print(
        (
            "  BEST_CENTER_GLOBAL_CONTROL="
            f"{r['best_center_global_control']}"
        )
    )

    print(
        (
            "  BEST_PAYLOAD_GLOBAL_CONTROL="
        )
        + (
            "NONE"
            if r[
                "best_dense_global_control"
            ]
            is None
            else (
                f"{r['best_dense_global_control']['C_payload']:.15e}"
            )
        )
    )

    print(
        (
            "  BEST_PAYLOAD_LOCAL_FRONT_CLOSURE="
        )
        + (
            "NONE"
            if r[
                "best_dense_local_front_closure"
            ]
            is None
            else (
                f"{r['best_dense_local_front_closure']['C_payload']:.15e}"
            )
        )
    )

    print(
        (
            "  BEST_PAYLOAD_DIRECT_G1="
        )
        + (
            "NONE"
            if r[
                "best_dense_direct_g1"
            ]
            is None
            else (
                f"{r['best_dense_direct_g1']['C_payload']:.15e}"
            )
        )
    )

    print(
        (
            "  G_PATH_MAX_006D="
            f"{r['thresholds'][str(C_006D)]['g_path_max']}"
        )
    )

    print(
        (
            "  G_PATH_MAX_024D="
            f"{r['thresholds'][str(C_024D)]['g_path_max']}"
        )
    )


print()

print(
    (
        "ROBUST_G_PATH_MAX_006D="
        f"{robust_g006}"
    )
)

print(
    (
        "ROBUST_G_PATH_MAX_024D="
        f"{robust_g024}"
    )
)

print(
    f"027C_DECISION={decision}"
)

print(
    f"NEXT={next_step}"
)

print(
    (
        "SOURCE_ENGINE_80_HEURISTIC_AUTHORIZED="
        + (
            "YES"
            if source_80
            else "NO"
        )
    )
)

print(
    "OVERALL_PRACTICAL_ANTIGRAVITY_80_HEURISTIC_AUTHORIZED=NO"
)

print(
    "026C_N89_STILL_REQUIRED=YES"
)

print(
    "MICROSCOPIC_FIELD_REALIZATION=NO"
)

print(
    "POINTWISE_LOCAL_TMUNU_CONSERVATION=NO"
)

print(
    "REMOVES_1_OVER_G_SCALING=NO"
)

print(
    "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
)

print(
    f"SUMMARY_JSON={OUT_JSON}"
)

print(
    f"SEED_CSV={OUT_CSV}"
)

print(
    f"WILDCARD_CSV={OUT_WILDCARD}"
)

print(
    "027C_RUN_COMPLETE=YES"
)
