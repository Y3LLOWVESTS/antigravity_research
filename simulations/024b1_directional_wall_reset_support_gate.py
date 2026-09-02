#!/usr/bin/env python3
"""024B1 — directional wall-reset and boundary-support gate.

PURPOSE
-------
Test the first physical consequence of 024B's spatiotemporal-kernel idea before
launching a microscopic PDE evolution.

The run compares three thin-defect processes derived from Nambu-Goto-type
worldvolume actions:

1. a finite wall disk whose outer string contracts inward;
2. a central string-bounded hole that expands outward while the outer rim is
   held fixed;
3. the same annular wall with both inner and outer boundaries free.

The central question is whether the sign of the time-integrated finite-standoff
payload source is controlled by the direction in which compensating positive
kinetic stress moves.

SCIENTIFIC QUESTION
-------------------
Does natural collapse realize the useful 024B pulse rectifier, or is a
low-active stabilized outer rim required so that wall destruction proceeds
center-out and moves reset stress toward lower payload kernel?

MODEL
-----
Use c=h=sigma=1 for the dimensionless effective calculation.

A flat domain wall has surface stress

    T00 = sigma,
    p_x = p_y = -sigma,
    p_z = 0,

so its active surface source is

    S_wall = -sigma.

A Nambu-Goto string moving transversely with speed beta has, per physical
length,

    S_string
        =
    T00 + sum_i Tii
        =
    2 mu gamma beta^2.

Thus a moving string is a positive active source even though a static
Nambu string has S=0.

OUTER-EDGE COLLAPSE
-------------------
The symmetry-reduced action is

    L_out
        =
    -2 pi mu R sqrt(1-Rdot^2)
    - pi sigma R^2.

The conserved energy is

    E
        =
    2 pi mu R gamma
    + pi sigma R^2.

Define

    lambda
        =
    sigma R0 / (2 mu).

Then with y=R/R0,

    gamma(y)
        =
    (1 + lambda - lambda y^2)/y.

The instantaneous outward axial kernel moment at h=1 is

    A_out
        =
    2 pi sigma [1 - 1/sqrt(1+R^2)]
    - Q_string/(1+R^2)^(3/2),

with

    Q_string
        =
    4 pi mu R gamma beta^2.

In the most wall-dominated limit lambda -> infinity, the collapse-stage
kernel-time integral is exactly

    J_infinity
        =
    2 pi sigma R0
    [1 - sqrt(1+R0^2)]
        <
    0

for every R0>0.

Therefore even the optimistic vanishing-rest-energy outer string produces an
inward collapse-stage contribution: wall energy is converted into positive
kinetic active stress while the boundary moves toward higher payload kernel.

CENTER-OUT HOLE
---------------
For a string-bounded hole of radius r in a wall, the reduced action is

    L_hole
        =
    -2 pi mu r sqrt(1-rdot^2)
    + pi sigma r^2.

Relative to the intact wall,

    E_hole
        =
    2 pi mu r gamma
    - pi sigma r^2.

The critical radius is

    r_c
        =
    mu/sigma.

A hole initialized at

    r0
        =
    kappa r_c,

with

    kappa > 1,

expands and eats the wall.

If the outer rim is held fixed at R0, the remaining negative-active wall is an
annulus while the positive kinetic string moves outward toward lower kernel.

The run then releases the outer rim.

The outer and inner reduced actions separate, so the outer boundary contracts
while the inner boundary expands. Evolution stops when the two boundaries meet.

RETARDED LINEARIZED-GR IMPULSE IDENTITY
---------------------------------------
In harmonic gauge, on the payload symmetry axis,

    h00(t,x)
        =
    (2G/c^4)
    integral d^3x'
    S(t-D/c,x')/D.

For a slow payload, a compact complete source history, and vanishing endpoint
h0z,

    Delta v_z
        =
    (G/c^2)
    partial_z
    integral d^3x'/D
    integral dt S(t,x').

At fixed Eulerian source point x', retardation is only the constant time shift

    D/c.

Therefore retardation changes the time waveform but does not alter the
complete time-integrated impulse.

For the present axisymmetric in-plane defect motion,

    T0z = 0

on the symmetry axis.

This is why the run evaluates the kernel-weighted time integral directly
instead of performing an unnecessary retarded waveform simulation.

IMPORTANT:

The collapse and hole stages are not complete formation-reset cycles.

Formation, annihilation radiation, control, reset and all mandatory support
sectors remain unresolved.

OBSERVABLES
-----------
For each effective trajectory report:

    C_initial

peak stored-energy coefficient at the initial turning configuration;

    gain_vs_006D

equal to C_006D/C_initial;

    eta_J

dimensionless kernel-time integral per peak source energy;

    tau

duration in units h/c.

Positive eta_J is outward for the tested stage.

For a source initially normalized to 1 g at h=1 m,

    Delta v_stage
        =
    C_initial
    g h/c
    eta_J.

HELD-RIM SUPPORT DIAGNOSTICS
----------------------------
The held-rim hole calculation initially assigns the outer Nambu string

    chi = 0,

where chi is the static active ratio

    chi
        =
    Q_active/E_rim.

This is a support lower bound, not a physical stabilization.

For selected cases the run computes:

    extra inert support-energy margin before the initial gain falls below 10x;

    chi_max_gain10;

    chi_max_positive_reset.

A later physical rim must include its complete energy, tension, current,
charge, fields, equilibrium and stability ledger.

VALIDATION
----------
- 006D must reproduce C=23.591586299249.
- The 024B wall coefficient at x*=sqrt(phi) must reproduce
  2.118033988749895.
- The lambda->infinity numerical collapse must reproduce the exact negative
  impulse.
- The final collapsing-string active source must approach 2E.
- Held-rim results must not be promoted as free-boundary results.

PROMOTION CONDITION
-------------------
A physical free-boundary pulse is promoted only if a free conserved defect
system has both

    gain_vs_006D >= 10

and

    eta_J > 0.

If only the held-rim center-out hole survives, the result is YELLOW and the
next gate is a low-active stabilized-rim EOS/stability intersection using
existing vorton infrastructure.

No microscopic PDE solve is authorized solely by a held-rim result.

LITERATURE ANCHORS
------------------
R. Gregory, D. Haws, D. Garfinkle,
Phys. Rev. D 42, 343 (1990).

T. Hiramatsu, M. Kawasaki, K. Saikawa, T. Sekiguchi,
arXiv:1202.5851.

D. I. Dunsky et al.,
Phys. Rev. D 106, 075030 (2022).

J. J. Blanco-Pillado et al.,
Phys. Rev. D 111, 056007 (2025).

Z. Zhao, L. Bian, J. Shu,
Phys. Rev. D 114, 023539 (2026).

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_024B1_THIN_DEFECT_DYNAMIC_IMPULSE_AND_SUPPORT_PREFILTER

DOES NOT ESTABLISH
------------------
- microscopic field evolution;
- annihilation/particle-radiation ledger;
- full formation-reset cycle;
- finite-payload dynamic averaging;
- nonlinear GR;
- practical energy scaling;
- an experiment;
- a practical antigravity device.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import csv
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results/data"

S006D = SIM / "006d_finite_thickness_conserved_source.py"

OUT_JSON = (
    DATA
    / "024b1_directional_wall_reset_support_summary.json"
)

OUT_CSV = (
    DATA
    / "024b1_directional_wall_reset_support_scan.csv"
)

C_LIGHT = 299_792_458.0
G0 = 9.80665

C006D_REFERENCE = 23.591586299249
C10_TARGET = C006D_REFERENCE / 10.0

GOLDEN_RATIO = (
    0.5
    * (
        1.0
        + math.sqrt(5.0)
    )
)

X_024B = math.sqrt(
    GOLDEN_RATIO
)

C_WALL_024B = (
    2.118033988749895
)

# Blind diagnostics only.
# These values are not physics priors,
# evidence, or optimization targets.
WILDCARDS = (
    0.625,
    1.6,
    1.875,
    3.125,
    5.0,
)


@dataclass(frozen=True)
class CollapseMetrics:
    x0: float
    lam: float
    c_initial: float
    gain_vs_006d: float
    tau_collapse: float
    eta_total: float
    eta_wall: float
    eta_string_attraction: float
    min_force_per_energy: float
    max_force_per_energy: float
    final_string_active_over_energy: float


@dataclass(frozen=True)
class HeldHoleMetrics:
    x0: float
    q: float
    kappa: float
    r0_over_h: float
    c_initial_chi0: float
    gain_vs_006d_chi0: float
    tau_reset: float
    eta_total_chi0: float
    eta_wall: float
    eta_inner_string_attraction: float
    outer_rim_energy_fraction: float
    outer_kernel: float
    extra_inert_energy_margin_for_10x: float
    chi_max_gain10: float
    chi_max_positive_reset: float


@dataclass(frozen=True)
class FreeAnnulusMetrics:
    x0: float
    q_outer: float
    q_inner: float
    kappa: float
    c_initial: float
    gain_vs_006d: float
    tau_to_meeting: float
    meeting_radius_over_h: float
    eta_total: float
    eta_wall: float
    eta_outer_string_attraction: float
    eta_inner_string_attraction: float


def parse_float(
    text: str,
    labels: tuple[str, ...],
) -> float:

    for label in labels:

        match = re.search(
            rf"^{re.escape(label)}="
            r"([+\-0-9.eE]+)$",
            text,
            flags=re.MULTILINE,
        )

        if match:

            return float(
                match.group(1)
            )

    raise RuntimeError(
        f"Missing labels: {labels}"
    )


def rerun_006d() -> dict[str, Any]:

    if not S006D.is_file():

        raise RuntimeError(
            "Missing required source: "
            f"{S006D}"
        )

    env = dict(
        os.environ
    )

    env["PYTHONPATH"] = str(
        ROOT
        / "src"
    )

    proc = subprocess.run(
        [
            sys.executable,
            str(
                S006D
            ),
        ],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    if proc.returncode != 0:

        raise RuntimeError(
            proc.stdout
            + "\n"
            + proc.stderr
        )

    text = proc.stdout

    c006d = parse_float(
        text,
        (
            "C_FINITE_BEST_TESTED",
            "FINEST_FINITE_C",
        ),
    )

    for label in (
        "LOCAL_CONSERVATION=PASS",
        "DEC=PASS",
        "POSITIVE_FAR_FIELD_ACTIVE_MASS=YES",
        "SIMULATION_006D=GREEN",
    ):

        if label not in text:

            raise RuntimeError(
                "006D missing required label: "
                f"{label}"
            )

    relative_error = (
        abs(
            c006d
            - C006D_REFERENCE
        )
        / C006D_REFERENCE
    )

    if relative_error > 5.0e-10:

        raise RuntimeError(
            "006D coefficient regression: "
            f"{c006d}"
        )

    return {
        "c":
            c006d,

        "relative_error":
            relative_error,

        "returncode":
            proc.returncode,
    }


def wall_c(
    x: float,
) -> float:

    root = math.sqrt(
        1.0
        + x * x
    )

    return (
        0.5
        * root
        * (
            root
            + 1.0
        )
    )


def wall_c_direct(
    x: float,
) -> float:

    return (
        x * x
        /
        (
            2.0
            * (
                1.0
                - 1.0
                / math.sqrt(
                    1.0
                    + x * x
                )
            )
        )
    )


def collapse_metrics(
    x0: float,
    lam: float,
    n: int = 4001,
) -> CollapseMetrics:

    if (
        x0 <= 0.0
        or lam <= 0.0
    ):

        raise ValueError(
            "x0 and lambda must be positive"
        )

    # y=R/R0=1-s^2 removes the
    # integrable beta=0 turning-point singularity.
    s = np.linspace(
        0.0,
        1.0,
        n,
    )

    y = (
        1.0
        - s * s
    )

    a = (
        1.0
        + lam
        - lam
        * y
        * y
    )

    inv_gamma_sq = (
        y
        / a
    ) ** 2

    beta_sq = np.maximum(
        0.0,
        1.0
        - inv_gamma_sq,
    )

    beta = np.sqrt(
        beta_sq
    )

    dtauds = np.empty_like(
        s
    )

    dtauds[1:] = (
        2.0
        * x0
        * s[1:]
        / beta[1:]
    )

    dtauds[0] = (
        math.sqrt(2.0)
        * x0
        / math.sqrt(
            1.0
            + 2.0
            * lam
        )
    )

    radius = (
        x0
        * y
    )

    wall = (
        2.0
        * math.pi
        * (
            1.0
            - 1.0
            / np.sqrt(
                1.0
                + radius
                * radius
            )
        )
    )

    # sigma=h=c=1.
    # lambda=sigma*R0/(2mu).
    mu = (
        x0
        / (
            2.0
            * lam
        )
    )

    # R*gamma = R0*a exactly.
    q_string = (
        4.0
        * math.pi
        * mu
        * x0
        * a
        * beta_sq
    )

    string_attr = (
        q_string
        /
        (
            1.0
            + radius
            * radius
        ) ** 1.5
    )

    outward = (
        wall
        - string_attr
    )

    energy = (
        math.pi
        * x0
        * x0
        * (
            1.0
            + 1.0
            / lam
        )
    )

    j_wall = float(
        np.trapezoid(
            wall
            * dtauds,
            s,
        )
    )

    j_string = float(
        np.trapezoid(
            string_attr
            * dtauds,
            s,
        )
    )

    j_total = float(
        np.trapezoid(
            outward
            * dtauds,
            s,
        )
    )

    tau = float(
        np.trapezoid(
            dtauds,
            s,
        )
    )

    c_initial = (
        wall_c(
            x0
        )
        * (
            1.0
            + 1.0
            / lam
        )
    )

    return CollapseMetrics(
        x0=x0,
        lam=lam,

        c_initial=
            c_initial,

        gain_vs_006d=
            C006D_REFERENCE
            / c_initial,

        tau_collapse=
            tau,

        eta_total=
            j_total
            / energy,

        eta_wall=
            j_wall
            / energy,

        eta_string_attraction=
            j_string
            / energy,

        min_force_per_energy=
            float(
                np.min(
                    outward
                    / energy
                )
            ),

        max_force_per_energy=
            float(
                np.max(
                    outward
                    / energy
                )
            ),

        final_string_active_over_energy=
            float(
                q_string[-1]
                / energy
            ),
    )


def collapse_ultra_eta(
    x0: float,
) -> float:

    return (
        2.0
        * (
            1.0
            - math.sqrt(
                1.0
                + x0
                * x0
            )
        )
        / x0
    )


def held_hole_metrics(
    x0: float,
    q: float,
    kappa: float,
    n: int = 4001,
) -> HeldHoleMetrics | None:

    if (
        x0 <= 0.0
        or q <= 0.0
        or kappa <= 1.0
    ):

        raise ValueError(
            "Require x0>0, q>0, kappa>1"
        )

    # q=mu/(sigma R0), sigma=1.
    mu = (
        q
        * x0
    )

    r0 = (
        kappa
        * mu
    )

    if r0 >= x0:

        return None

    s = np.linspace(
        0.0,
        1.0,
        n,
    )

    radius = (
        r0
        + (
            x0
            - r0
        )
        * s
        * s
    )

    e_rel = (
        2.0
        * math.pi
        * mu
        * r0
        - math.pi
        * r0
        * r0
    )

    gamma = (
        e_rel
        + math.pi
        * radius
        * radius
    ) / (
        2.0
        * math.pi
        * mu
        * radius
    )

    if (
        float(
            np.min(
                gamma
            )
        )
        < 1.0
        - 5.0e-11
    ):

        return None

    beta_sq = np.maximum(
        0.0,
        1.0
        - 1.0
        / (
            gamma
            * gamma
        ),
    )

    beta = np.sqrt(
        beta_sq
    )

    dtauds = np.empty_like(
        s
    )

    dtauds[1:] = (
        2.0
        * (
            x0
            - r0
        )
        * s[1:]
        / beta[1:]
    )

    dtauds[0] = (
        dtauds[1]
    )

    wall = (
        2.0
        * math.pi
        * (
            1.0
            / np.sqrt(
                1.0
                + radius
                * radius
            )
            - 1.0
            / math.sqrt(
                1.0
                + x0
                * x0
            )
        )
    )

    q_inner = (
        4.0
        * math.pi
        * mu
        * radius
        * gamma
        * beta_sq
    )

    inner_attr = (
        q_inner
        /
        (
            1.0
            + radius
            * radius
        ) ** 1.5
    )

    e_wall = (
        math.pi
        * (
            x0
            * x0
            - r0
            * r0
        )
    )

    e_inner = (
        2.0
        * math.pi
        * mu
        * r0
    )

    e_outer = (
        2.0
        * math.pi
        * mu
        * x0
    )

    energy = (
        e_wall
        + e_inner
        + e_outer
    )

    a0 = float(
        wall[0]
    )

    if a0 <= 0.0:

        return None

    tau = float(
        np.trapezoid(
            dtauds,
            s,
        )
    )

    j_wall = float(
        np.trapezoid(
            wall
            * dtauds,
            s,
        )
    )

    j_inner = float(
        np.trapezoid(
            inner_attr
            * dtauds,
            s,
        )
    )

    c0 = (
        energy
        / a0
    )

    eta0 = (
        j_wall
        - j_inner
    ) / energy

    k_outer = (
        1.0
        / (
            1.0
            + x0
            * x0
        ) ** 1.5
    )

    outer_fraction = (
        e_outer
        / energy
    )

    extra_inert_margin = (
        C10_TARGET
        / c0
        - 1.0
    )

    numerator = (
        a0
        - energy
        / C10_TARGET
    )

    denominator = (
        e_outer
        * k_outer
    )

    chi_max_gain10 = (
        numerator
        / denominator
        if denominator > 0.0
        else math.inf
    )

    denominator_impulse = (
        outer_fraction
        * k_outer
        * tau
    )

    chi_max_positive = (
        eta0
        / denominator_impulse
        if denominator_impulse > 0.0
        else math.inf
    )

    return HeldHoleMetrics(
        x0=x0,
        q=q,
        kappa=kappa,

        r0_over_h=
            r0,

        c_initial_chi0=
            c0,

        gain_vs_006d_chi0=
            C006D_REFERENCE
            / c0,

        tau_reset=
            tau,

        eta_total_chi0=
            eta0,

        eta_wall=
            j_wall
            / energy,

        eta_inner_string_attraction=
            j_inner
            / energy,

        outer_rim_energy_fraction=
            outer_fraction,

        outer_kernel=
            k_outer,

        extra_inert_energy_margin_for_10x=
            extra_inert_margin,

        chi_max_gain10=
            chi_max_gain10,

        chi_max_positive_reset=
            chi_max_positive,
    )


def outer_trajectory(
    x0: float,
    q_outer: float,
    n: int,
) -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
]:

    mu = (
        q_outer
        * x0
    )

    lam = (
        x0
        / (
            2.0
            * mu
        )
    )

    s = np.linspace(
        0.0,
        1.0,
        n,
    )

    y = (
        1.0
        - s
        * s
    )

    a = (
        1.0
        + lam
        - lam
        * y
        * y
    )

    beta_sq = np.maximum(
        0.0,
        1.0
        - (
            y
            / a
        ) ** 2,
    )

    beta = np.sqrt(
        beta_sq
    )

    dtauds = np.empty_like(
        s
    )

    dtauds[1:] = (
        2.0
        * x0
        * s[1:]
        / beta[1:]
    )

    dtauds[0] = (
        math.sqrt(2.0)
        * x0
        / math.sqrt(
            1.0
            + 2.0
            * lam
        )
    )

    tau = np.concatenate(
        (
            [0.0],
            np.cumsum(
                0.5
                * (
                    dtauds[1:]
                    + dtauds[:-1]
                )
                * np.diff(
                    s
                )
            ),
        )
    )

    radius = (
        x0
        * y
    )

    q_active = (
        4.0
        * math.pi
        * mu
        * x0
        * a
        * beta_sq
    )

    return (
        tau,
        radius,
        q_active,
    )


def inner_trajectory(
    x0: float,
    q_inner: float,
    kappa: float,
    n: int,
) -> tuple[
    np.ndarray,
    np.ndarray,
    np.ndarray,
    float,
] | None:

    mu = (
        q_inner
        * x0
    )

    r0 = (
        kappa
        * mu
    )

    if r0 >= x0:

        return None

    s = np.linspace(
        0.0,
        1.0,
        n,
    )

    radius = (
        r0
        + (
            x0
            - r0
        )
        * s
        * s
    )

    e_rel = (
        2.0
        * math.pi
        * mu
        * r0
        - math.pi
        * r0
        * r0
    )

    gamma = (
        e_rel
        + math.pi
        * radius
        * radius
    ) / (
        2.0
        * math.pi
        * mu
        * radius
    )

    beta_sq = np.maximum(
        0.0,
        1.0
        - 1.0
        / (
            gamma
            * gamma
        ),
    )

    beta = np.sqrt(
        beta_sq
    )

    dtauds = np.empty_like(
        s
    )

    dtauds[1:] = (
        2.0
        * (
            x0
            - r0
        )
        * s[1:]
        / beta[1:]
    )

    dtauds[0] = (
        dtauds[1]
    )

    tau = np.concatenate(
        (
            [0.0],
            np.cumsum(
                0.5
                * (
                    dtauds[1:]
                    + dtauds[:-1]
                )
                * np.diff(
                    s
                )
            ),
        )
    )

    q_active = (
        4.0
        * math.pi
        * mu
        * radius
        * gamma
        * beta_sq
    )

    return (
        tau,
        radius,
        q_active,
        r0,
    )


def free_annulus_metrics(
    x0: float,
    q_outer: float,
    q_inner: float,
    kappa: float,
    n: int = 1601,
    nt: int = 1601,
) -> FreeAnnulusMetrics | None:

    outer = outer_trajectory(
        x0,
        q_outer,
        n,
    )

    inner = inner_trajectory(
        x0,
        q_inner,
        kappa,
        n,
    )

    if inner is None:

        return None

    (
        t_outer,
        r_outer,
        qact_outer,
    ) = outer

    (
        t_inner,
        r_inner,
        qact_inner,
        r0,
    ) = inner

    tmax = min(
        float(
            t_outer[-1]
        ),
        float(
            t_inner[-1]
        ),
    )

    tau = np.linspace(
        0.0,
        tmax,
        nt,
    )

    ro = np.interp(
        tau,
        t_outer,
        r_outer,
    )

    ri = np.interp(
        tau,
        t_inner,
        r_inner,
    )

    crossing = np.flatnonzero(
        ro <= ri
    )

    if crossing.size == 0:

        return None

    stop = int(
        crossing[0]
    )

    if stop < 2:

        return None

    tau = tau[
        : stop + 1
    ]

    ro = ro[
        : stop + 1
    ]

    ri = ri[
        : stop + 1
    ]

    qo = np.interp(
        tau,
        t_outer,
        qact_outer,
    )

    qi = np.interp(
        tau,
        t_inner,
        qact_inner,
    )

    wall = (
        2.0
        * math.pi
        * (
            1.0
            / np.sqrt(
                1.0
                + ri
                * ri
            )
            - 1.0
            / np.sqrt(
                1.0
                + ro
                * ro
            )
        )
    )

    outer_attr = (
        qo
        /
        (
            1.0
            + ro
            * ro
        ) ** 1.5
    )

    inner_attr = (
        qi
        /
        (
            1.0
            + ri
            * ri
        ) ** 1.5
    )

    outward = (
        wall
        - outer_attr
        - inner_attr
    )

    mu_outer = (
        q_outer
        * x0
    )

    mu_inner = (
        q_inner
        * x0
    )

    e_wall = (
        math.pi
        * (
            x0
            * x0
            - r0
            * r0
        )
    )

    e_outer = (
        2.0
        * math.pi
        * mu_outer
        * x0
    )

    e_inner = (
        2.0
        * math.pi
        * mu_inner
        * r0
    )

    energy = (
        e_wall
        + e_outer
        + e_inner
    )

    a0 = float(
        wall[0]
    )

    if a0 <= 0.0:

        return None

    j_wall = float(
        np.trapezoid(
            wall,
            tau,
        )
    )

    j_outer = float(
        np.trapezoid(
            outer_attr,
            tau,
        )
    )

    j_inner = float(
        np.trapezoid(
            inner_attr,
            tau,
        )
    )

    j_total = float(
        np.trapezoid(
            outward,
            tau,
        )
    )

    c0 = (
        energy
        / a0
    )

    return FreeAnnulusMetrics(
        x0=x0,

        q_outer=
            q_outer,

        q_inner=
            q_inner,

        kappa=
            kappa,

        c_initial=
            c0,

        gain_vs_006d=
            C006D_REFERENCE
            / c0,

        tau_to_meeting=
            float(
                tau[-1]
            ),

        meeting_radius_over_h=
            0.5
            * float(
                ro[-1]
                + ri[-1]
            ),

        eta_total=
            j_total
            / energy,

        eta_wall=
            j_wall
            / energy,

        eta_outer_string_attraction=
            j_outer
            / energy,

        eta_inner_string_attraction=
            j_inner
            / energy,
    )


def main() -> None:

    DATA.mkdir(
        parents=True,
        exist_ok=True,
    )

    anchor = (
        rerun_006d()
    )

    if (
        abs(
            wall_c(
                X_024B
            )
            - C_WALL_024B
        )
        > 2.0e-14
    ):

        raise RuntimeError(
            "024B wall coefficient regression"
        )

    if (
        abs(
            wall_c(
                X_024B
            )
            - wall_c_direct(
                X_024B
            )
        )
        > 2.0e-13
    ):

        raise RuntimeError(
            "wall coefficient dual-form mismatch"
        )

    ultra_exact = (
        collapse_ultra_eta(
            X_024B
        )
    )

    ultra_numeric = (
        collapse_metrics(
            X_024B,
            1.0e7,
            n=12001,
        )
    )

    if (
        abs(
            ultra_numeric.eta_total
            - ultra_exact
        )
        > 1.0e-6
    ):

        raise RuntimeError(
            "lambda->infinity collapse limit failed"
        )

    if (
        abs(
            ultra_numeric.final_string_active_over_energy
            - 2.0
        )
        > 2.0e-12
    ):

        raise RuntimeError(
            "final string active-source identity failed"
        )

    collapse_rows: list[
        dict[
            str,
            Any,
        ]
    ] = []

    collapse_positive = 0
    collapse_ge10 = 0
    collapse_ge10_positive = 0

    best_collapse_eta = (
        -math.inf
    )

    best_collapse: (
        CollapseMetrics
        | None
    ) = None

    for x0 in np.geomspace(
        0.05,
        5.0,
        51,
    ):

        for lam in np.geomspace(
            0.1,
            1.0e5,
            51,
        ):

            item = collapse_metrics(
                float(
                    x0
                ),
                float(
                    lam
                ),
                n=1201,
            )

            if (
                item.eta_total
                > 0.0
            ):

                collapse_positive += 1

            if (
                item.gain_vs_006d
                >= 10.0
            ):

                collapse_ge10 += 1

                if (
                    item.eta_total
                    > 0.0
                ):

                    collapse_ge10_positive += 1

            if (
                item.eta_total
                > best_collapse_eta
            ):

                best_collapse_eta = (
                    item.eta_total
                )

                best_collapse = (
                    item
                )

            collapse_rows.append({
                "branch":
                    "FREE_OUTER_EDGE_COLLAPSE",

                "x0":
                    item.x0,

                "ratio":
                    item.lam,

                "kappa":
                    "",

                "C_initial":
                    item.c_initial,

                "gain_vs_006D":
                    item.gain_vs_006d,

                "eta_J":
                    item.eta_total,

                "tau":
                    item.tau_collapse,

                "support_margin":
                    "",

                "chi_max_gain10":
                    "",

                "label":
                    "PHYSICALLY_MOTIVATED_DENSE_SCAN",
            })

    if collapse_positive != 0:

        raise RuntimeError(
            "unexpected positive free-collapse case"
        )

    held_rows: list[
        dict[
            str,
            Any,
        ]
    ] = []

    held_positive = 0
    held_ge10_positive = 0
    held_ge10_support20_positive = 0

    best_held_eta = (
        -math.inf
    )

    best_held: (
        HeldHoleMetrics
        | None
    ) = None

    best_support20_eta = (
        -math.inf
    )

    best_support20: (
        HeldHoleMetrics
        | None
    ) = None

    x_values = np.linspace(
        0.30,
        2.00,
        41,
    )

    q_values = np.geomspace(
        0.003,
        0.30,
        41,
    )

    kappa_values = (
        1.01,
        1.05,
        1.10,
        1.20,
        1.40,
    )

    for x0 in x_values:

        for q in q_values:

            for kappa in kappa_values:

                item = held_hole_metrics(
                    float(
                        x0
                    ),
                    float(
                        q
                    ),
                    float(
                        kappa
                    ),
                    n=1201,
                )

                if item is None:

                    continue

                positive = (
                    item.eta_total_chi0
                    > 0.0
                )

                ge10 = (
                    item.gain_vs_006d_chi0
                    >= 10.0
                )

                margin20 = (
                    item.extra_inert_energy_margin_for_10x
                    >= 0.20
                )

                if positive:

                    held_positive += 1

                if (
                    positive
                    and ge10
                ):

                    held_ge10_positive += 1

                if (
                    positive
                    and ge10
                    and margin20
                ):

                    held_ge10_support20_positive += 1

                if (
                    positive
                    and ge10
                    and item.eta_total_chi0
                    > best_held_eta
                ):

                    best_held_eta = (
                        item.eta_total_chi0
                    )

                    best_held = (
                        item
                    )

                if (
                    positive
                    and ge10
                    and margin20
                    and item.eta_total_chi0
                    > best_support20_eta
                ):

                    best_support20_eta = (
                        item.eta_total_chi0
                    )

                    best_support20 = (
                        item
                    )

                held_rows.append({
                    "branch":
                        "HELD_RIM_CENTER_OUT_HOLE",

                    "x0":
                        item.x0,

                    "ratio":
                        item.q,

                    "kappa":
                        item.kappa,

                    "C_initial":
                        item.c_initial_chi0,

                    "gain_vs_006D":
                        item.gain_vs_006d_chi0,

                    "eta_J":
                        item.eta_total_chi0,

                    "tau":
                        item.tau_reset,

                    "support_margin":
                        item.extra_inert_energy_margin_for_10x,

                    "chi_max_gain10":
                        item.chi_max_gain10,

                    "label":
                        "HELD_RIM_SUPPORT_LOWER_BOUND",
                })

    if (
        best_held is None
        or best_support20 is None
    ):

        raise RuntimeError(
            "held-rim positive target not reconstructed"
        )

    # Fixed reference prevents optimizer-only promotion.
    reference = held_hole_metrics(
        2.0 / 3.0,
        0.18,
        1.02,
        n=12001,
    )

    if reference is None:

        raise RuntimeError(
            "reference held-hole case missing"
        )

    if not (
        reference.eta_total_chi0
        > 0.20
        and reference.gain_vs_006d_chi0
        > 12.0
        and reference.extra_inert_energy_margin_for_10x
        > 0.20
    ):

        raise RuntimeError(
            "reference held-hole target regressed"
        )

    free_reference = free_annulus_metrics(
        2.0 / 3.0,
        0.18,
        0.18,
        1.02,
        n=8001,
        nt=8001,
    )

    if free_reference is None:

        raise RuntimeError(
            "free annulus reference failed"
        )

    free_rows: list[
        dict[
            str,
            Any,
        ]
    ] = []

    free_positive = 0
    free_ge10_positive = 0

    for x0 in np.linspace(
        0.40,
        1.80,
        15,
    ):

        for q in np.geomspace(
            0.005,
            0.25,
            15,
        ):

            for kappa in (
                1.01,
                1.10,
                1.25,
            ):

                item = free_annulus_metrics(
                    float(
                        x0
                    ),
                    float(
                        q
                    ),
                    float(
                        q
                    ),
                    float(
                        kappa
                    ),
                    n=701,
                    nt=701,
                )

                if item is None:

                    continue

                if (
                    item.eta_total
                    > 0.0
                ):

                    free_positive += 1

                    if (
                        item.gain_vs_006d
                        >= 10.0
                    ):

                        free_ge10_positive += 1

                free_rows.append({
                    "branch":
                        "FREE_TWO_BOUNDARY_ANNULUS",

                    "x0":
                        item.x0,

                    "ratio":
                        item.q_outer,

                    "kappa":
                        item.kappa,

                    "C_initial":
                        item.c_initial,

                    "gain_vs_006D":
                        item.gain_vs_006d,

                    "eta_J":
                        item.eta_total,

                    "tau":
                        item.tau_to_meeting,

                    "support_margin":
                        "",

                    "chi_max_gain10":
                        "",

                    "label":
                        "INDEPENDENT_FREE_BOUNDARY_SCAN",
                })

    wildcard_rows: list[
        dict[
            str,
            Any,
        ]
    ] = []

    for x0 in WILDCARDS:

        item = collapse_metrics(
            float(
                x0
            ),
            100.0,
            n=3001,
        )

        wildcard_rows.append({
            "branch":
                "BLIND_WILDCARD_COLLAPSE",

            "x0":
                item.x0,

            "ratio":
                item.lam,

            "kappa":
                "",

            "C_initial":
                item.c_initial,

            "gain_vs_006D":
                item.gain_vs_006d,

            "eta_J":
                item.eta_total,

            "tau":
                item.tau_collapse,

            "support_margin":
                "",

            "chi_max_gain10":
                "",

            "label":
                "BLIND_WILDCARD_NOT_PHYSICS_PRIOR",
        })

    free_physical_pulse_promoted = (
        free_ge10_positive
        > 0
    )

    held_target_exists = (
        held_ge10_support20_positive
        > 0
    )

    if free_physical_pulse_promoted:

        pulse_decision = (
            "GREEN_EFFECTIVE_FREE_BOUNDARY_PROMOTION"
        )

        next_pulse = (
            "024B2_MICROSCOPIC_DYNAMIC_FIELD_EVOLUTION"
        )

    elif held_target_exists:

        pulse_decision = (
            "YELLOW_HELD_RIM_TARGET_ONLY"
        )

        next_pulse = (
            "024B2_LOW_ACTIVE_STABILIZED_RIM_"
            "EOS_AND_TRANSIENT_STABILITY_INTERSECTION"
        )

    else:

        pulse_decision = (
            "RED_WALL_PULSE_CLASS"
        )

        next_pulse = (
            "RERANK_PULSE_ARCHITECTURES"
        )

    reference_dv_1g_1m = (
        reference.c_initial_chi0
        * G0
        / C_LIGHT
        * reference.eta_total_chi0
    )

    collapse_xopt = collapse_metrics(
        X_024B,
        1.0e5,
        n=12001,
    )

    collapse_dv_1g_1m = (
        collapse_xopt.c_initial
        * G0
        / C_LIGHT
        * collapse_xopt.eta_total
    )

    rows = (
        collapse_rows
        + held_rows
        + free_rows
        + wildcard_rows
    )

    with OUT_CSV.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:

        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "branch",
                "x0",
                "ratio",
                "kappa",
                "C_initial",
                "gain_vs_006D",
                "eta_J",
                "tau",
                "support_margin",
                "chi_max_gain10",
                "label",
            ],
        )

        writer.writeheader()

        writer.writerows(
            rows
        )

    summary = {

        "claim_classification":
            (
                "PROJECT_DERIVED_024B1_"
                "THIN_DEFECT_DYNAMIC_"
                "IMPULSE_AND_SUPPORT_PREFILTER"
            ),

        "006D":
            anchor,

        "retarded_impulse_identity": {

            "full_cycle_retardation_changes_"
            "waveform_not_integrated_impulse":
                True,

            "requires_compact_complete_history":
                True,

            "requires_endpoint_h0z_term_to_vanish":
                True,

            "axisymmetric_in_plane_defect_"
            "has_T0z_on_axis":
                0.0,

            "formation_reset_still_mandatory":
                True,
        },

        "outer_edge_collapse": {

            "x_024b":
                X_024B,

            "C_wall_024b":
                C_WALL_024B,

            "ultra_eta_exact":
                ultra_exact,

            "ultra_eta_numeric":
                ultra_numeric.eta_total,

            "analytic_ultra_impulse_negative_"
            "for_every_x_positive":
                True,

            "dense_cases":
                len(
                    collapse_rows
                ),

            "positive_eta_cases":
                collapse_positive,

            "ge10_cases":
                collapse_ge10,

            "ge10_positive_eta_cases":
                collapse_ge10_positive,

            "best_eta_case":
                (
                    asdict(
                        best_collapse
                    )
                    if best_collapse
                    else None
                ),

            "xopt_lambda1e5":
                asdict(
                    collapse_xopt
                ),

            "delta_v_stage_1g_1m_m_per_s":
                collapse_dv_1g_1m,

            "decision":
                "RED_AS_NATURAL_RESET",
        },

        "held_rim_center_out_hole": {

            "dense_cases":
                len(
                    held_rows
                ),

            "positive_eta_cases":
                held_positive,

            "ge10_positive_eta_cases":
                held_ge10_positive,

            "ge10_support20_positive_eta_cases":
                held_ge10_support20_positive,

            "best_ge10_eta_case":
                asdict(
                    best_held
                ),

            "best_ge10_support20_eta_case":
                asdict(
                    best_support20
                ),

            "fixed_reference":
                asdict(
                    reference
                ),

            "fixed_reference_delta_v_"
            "stage_1g_1m_m_per_s":
                reference_dv_1g_1m,

            "outer_rim_physically_stabilized":
                False,

            "decision":
                "YELLOW_SUPPORT_DEPENDENT_TARGET",
        },

        "free_two_boundary_annulus": {

            "reference":
                asdict(
                    free_reference
                ),

            "coarse_cases":
                len(
                    free_rows
                ),

            "positive_eta_cases":
                free_positive,

            "ge10_positive_eta_cases":
                free_ge10_positive,

            "decision":
                (
                    "GREEN"
                    if free_physical_pulse_promoted
                    else
                    "RED_IN_TESTED_FREE_CLASS"
                ),
        },

        "decisions": {

            "NATURAL_INWARD_COLLAPSE":
                "RED",

            "HELD_RIM_OUTWARD_HOLE":
                (
                    "YELLOW_TARGET_EXISTS"
                    if held_target_exists
                    else
                    "RED"
                ),

            "FREE_TWO_BOUNDARY_"
            "HOLE_ANNIHILATION":
                (
                    "GREEN"
                    if free_physical_pulse_promoted
                    else
                    "RED_IN_TESTED_CLASS"
                ),

            "PULSE_EFFECTIVE_FIELD_PROMOTION":
                (
                    "YES"
                    if free_physical_pulse_promoted
                    else
                    "NO"
                ),

            "PULSE_BRANCH":
                pulse_decision,

            "NEXT_PULSE":
                next_pulse,

            "NEXT_STATIC":
                (
                    "CONTINUE_GENUINELY_NEW_006D_"
                    "MICROSCOPIC_REALIZATION_"
                    "RERANK_IN_PARALLEL"
                ),

            "PRACTICAL_ANTIGRAVITY_DEVICE":
                "NO",
        },

        "claim_limits": [
            "NO_MICROSCOPIC_DYNAMIC_FIELD",
            "NO_COMPLETE_FORMATION_RESET_CYCLE",
            "NO_ANNIHILATION_RADIATION_LEDGER",
            "NO_FINITE_PAYLOAD_DYNAMIC_AVERAGING",
            "NO_NONLINEAR_GR",
            "NO_PRACTICAL_DEVICE",
        ],
    }

    OUT_JSON.write_text(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "=== 024B1 DIRECTIONAL WALL "
        "RESET / SUPPORT GATE ==="
    )

    print(
        "C_006D="
        f"{anchor['c']:.15f}"
    )

    print(
        "STATIC_006D_ANCHOR=PASS"
    )

    print()

    print(
        "=== RETARDED FULL-CYCLE "
        "IMPULSE IDENTITY ==="
    )

    print(
        "RETARDATION_CHANGES_WAVEFORM_"
        "NOT_COMPLETE_IMPULSE=YES"
    )

    print(
        "AXIAL_T0Z_FOR_IN_PLANE_"
        "AXISYMMETRIC_DEFECT=ZERO"
    )

    print(
        "FORMATION_RESET_STILL_MANDATORY=YES"
    )

    print()

    print(
        "=== NATURAL OUTER-EDGE COLLAPSE ==="
    )

    print(
        "COLLAPSE_ULTRA_ETA_EXACT_XOPT="
        f"{ultra_exact:.15f}"
    )

    print(
        "COLLAPSE_ULTRA_ETA_NUMERIC_XOPT="
        f"{ultra_numeric.eta_total:.15f}"
    )

    print(
        "COLLAPSE_ULTRA_IMPULSE_NEGATIVE_"
        "FOR_ALL_X_POSITIVE=YES"
    )

    print(
        "COLLAPSE_DENSE_CASES="
        f"{len(collapse_rows)}"
    )

    print(
        "COLLAPSE_POSITIVE_ETA_CASES="
        f"{collapse_positive}"
    )

    print(
        "COLLAPSE_GE10_CASES="
        f"{collapse_ge10}"
    )

    print(
        "COLLAPSE_GE10_POSITIVE_ETA_CASES="
        f"{collapse_ge10_positive}"
    )

    print(
        "COLLAPSE_XOPT_LAM1E5_C="
        f"{collapse_xopt.c_initial:.15f}"
    )

    print(
        "COLLAPSE_XOPT_LAM1E5_GAIN="
        f"{collapse_xopt.gain_vs_006d:.12f}"
    )

    print(
        "COLLAPSE_XOPT_LAM1E5_ETA="
        f"{collapse_xopt.eta_total:.15f}"
    )

    print(
        "COLLAPSE_XOPT_LAM1E5_"
        "FINAL_STRING_ACTIVE_OVER_E="
        f"{collapse_xopt.final_string_active_over_energy:.15f}"
    )

    print(
        "COLLAPSE_XOPT_LAM1E5_"
        "DV_1G_1M_M_PER_S="
        f"{collapse_dv_1g_1m:.12e}"
    )

    print(
        "NATURAL_INWARD_COLLAPSE=RED"
    )

    print()

    print(
        "=== HELD-RIM CENTER-OUT HOLE ==="
    )

    print(
        "HELD_HOLE_DENSE_CASES="
        f"{len(held_rows)}"
    )

    print(
        "HELD_HOLE_POSITIVE_ETA_CASES="
        f"{held_positive}"
    )

    print(
        "HELD_HOLE_GE10_POSITIVE_ETA_CASES="
        f"{held_ge10_positive}"
    )

    print(
        "HELD_HOLE_GE10_SUPPORT20_"
        "POSITIVE_ETA_CASES="
        f"{held_ge10_support20_positive}"
    )

    print(
        "HELD_REFERENCE_X="
        f"{reference.x0:.15f}"
    )

    print(
        "HELD_REFERENCE_Q="
        f"{reference.q:.15f}"
    )

    print(
        "HELD_REFERENCE_KAPPA="
        f"{reference.kappa:.15f}"
    )

    print(
        "HELD_REFERENCE_C="
        f"{reference.c_initial_chi0:.15f}"
    )

    print(
        "HELD_REFERENCE_GAIN="
        f"{reference.gain_vs_006d_chi0:.12f}"
    )

    print(
        "HELD_REFERENCE_ETA="
        f"{reference.eta_total_chi0:.15f}"
    )

    print(
        "HELD_REFERENCE_EXTRA_INERT_"
        "SUPPORT_MARGIN_FOR_10X="
        f"{reference.extra_inert_energy_margin_for_10x:.12f}"
    )

    print(
        "HELD_REFERENCE_CHI_MAX_GAIN10="
        f"{reference.chi_max_gain10:.12f}"
    )

    print(
        "HELD_REFERENCE_CHI_MAX_"
        "POSITIVE_RESET="
        f"{reference.chi_max_positive_reset:.12f}"
    )

    print(
        "HELD_REFERENCE_DV_1G_1M_M_PER_S="
        f"{reference_dv_1g_1m:.12e}"
    )

    print(
        "HELD_OUTER_RIM_PHYSICAL_"
        "STABILIZATION_INCLUDED=NO"
    )

    print(
        "HELD_RIM_OUTWARD_HOLE="
        "YELLOW_SUPPORT_DEPENDENT_TARGET"
    )

    print()

    print(
        "=== FREE TWO-BOUNDARY ANNULUS ==="
    )

    print(
        "FREE_REFERENCE_C="
        f"{free_reference.c_initial:.15f}"
    )

    print(
        "FREE_REFERENCE_GAIN="
        f"{free_reference.gain_vs_006d:.12f}"
    )

    print(
        "FREE_REFERENCE_ETA="
        f"{free_reference.eta_total:.15f}"
    )

    print(
        "FREE_REFERENCE_TAU_MEET="
        f"{free_reference.tau_to_meeting:.15f}"
    )

    print(
        "FREE_ANNULUS_COARSE_CASES="
        f"{len(free_rows)}"
    )

    print(
        "FREE_ANNULUS_POSITIVE_ETA_CASES="
        f"{free_positive}"
    )

    print(
        "FREE_ANNULUS_GE10_POSITIVE_ETA_CASES="
        f"{free_ge10_positive}"
    )

    print(
        "FREE_TWO_BOUNDARY_HOLE_ANNIHILATION="
        + (
            "GREEN"
            if free_physical_pulse_promoted
            else
            "RED_IN_TESTED_CLASS"
        )
    )

    print()

    print(
        "=== 024B1 DECISION ==="
    )

    print(
        "PULSE_BRANCH="
        f"{pulse_decision}"
    )

    print(
        "PULSE_EFFECTIVE_FIELD_PROMOTION="
        + (
            "YES"
            if free_physical_pulse_promoted
            else
            "NO"
        )
    )

    print(
        "NEXT_PULSE="
        f"{next_pulse}"
    )

    print(
        "NEXT_STATIC="
        "CONTINUE_GENUINELY_NEW_006D_"
        "MICROSCOPIC_REALIZATION_"
        "RERANK_IN_PARALLEL"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO"
    )

    print(
        "SUMMARY_JSON="
        f"{OUT_JSON.relative_to(ROOT)}"
    )

    print(
        "SCAN_CSV="
        f"{OUT_CSV.relative_to(ROOT)}"
    )

    print(
        "024B1_RUN_COMPLETE=YES"
    )


if __name__ == "__main__":
    main()
