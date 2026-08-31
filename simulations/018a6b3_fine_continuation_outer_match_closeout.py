#!/usr/bin/env python3
"""018A-6B3 — fine continuation and outer-match junction closeout.

PURPOSE
-------
Close the remaining numerical/gating ambiguities left by 018A-6B2 without
opening another physical model or performing a premature global drum solve.

018A-6B2 established that after matched subtraction the physically relevant
KLS corrections were already strongly converged:

    energy correction;
    Sigma2 correction;
    active-source correction;
    variational identity;
    EOS;
    m=2..40 stability;
    stationarity.

Its formal RED came from:

    - several marginal optimizer residual flags;
    - applying an asymptotic global morphology criterion inside a deliberately
      small microscopic refinement patch.

This gate corrects both issues.

SCIENTIFIC QUESTION
-------------------
After explicitly continuing every marginal optimizer to the declared
stationarity tolerance, is the fine matched microscopic correction converged,
and does it preserve the already established large-domain one-sided wall
topology?

NO NEW PHYSICS PARAMETERS ARE INTRODUCED.

OUTER / INNER MATCHING
----------------------
The large-domain fixed-background 018A-6A solve establishes the asymptotic
wall geometry.

The fine 018A-6B2 patch establishes the coupled microscopic core correction.

A local patch whose half-width is smaller than the complete wall thickness is
not required to reach the global vacuum on its own.

Instead require:

    OUTER_GLOBAL_WALL_TERMINATION=PASS

and, inside the fine patch,

    LOCAL_ONE_SIDED_CONTRAST=PASS

with

    |A|_negative / |A|_positive < 0.2.

Also require local gauge-invariant phase locking.

OPTIMIZER CONTINUATION
----------------------
Every full/base lattice state is restarted from its previous optimized field
configuration using tighter L-BFGS-B tolerances.

No pass threshold is relaxed.

FULL required residuals:

    gradient RMS < 3e-6
    gradient max < 3e-5.

BASE required residuals:

    gradient RMS < 2e-6
    gradient max < 3e-4.

MATCHED CONVERGENCE
-------------------
Repeat the same fine resolution and patch sequences as 018A-6B2.

Resolution:

    N=51,65,81 at L=20.

Patch:

    (N,L) =
      (65,16)
      (81,20)
      (97,24).

Require the already declared KLS-specific ranges:

    Delta E range < 5e-4
    Delta Sigma2 range < 5e-4.

GLOBAL GRAVITY CLAIM
--------------------
This gate does NOT compute finite-payload gravity.

Even a complete green result only closes the local microscopic junction
preflight and authorizes:

    018A7_COMPLETE_MICROSCOPIC_GRAVITY_CLOSEOUT.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_018A_FINE_COUPLED_JUNCTION_CLOSEOUT
"""

from __future__ import annotations

import importlib.util
import math
from pathlib import Path
import sys

import numpy as np
from scipy.optimize import minimize


ROOT = Path(__file__).resolve().parents[1]

SOURCE = (
    ROOT
    / "simulations"
    / "018a6b2_fine_local_multiscale_junction.py"
)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(
        name,
        path,
    )

    if spec is None or spec.loader is None:
        raise RuntimeError(
            f"Cannot import {path}"
        )

    module = importlib.util.module_from_spec(
        spec
    )

    sys.modules[name] = module

    try:
        spec.loader.exec_module(
            module
        )
    except Exception:
        sys.modules.pop(
            name,
            None,
        )
        raise

    return module


b2 = load_module(
    "ag018a6b2_closeout",
    SOURCE,
)

fc = b2.fc
audit = b2.audit
m = b2.m


CHI_SELECTED = 0.00475

RESOLUTION_CASES = (
    (51, 20.0),
    (65, 20.0),
    (81, 20.0),
)

PATCH_CASES = (
    (65, 16.0),
    (81, 20.0),
    (97, 24.0),
)

CHI_VALUES = (
    0.00425,
    0.00450,
    0.00475,
)

CHI_CASE = (
    65,
    20.0,
)

MAX_FULL_GRAD_RMS = 3.0e-6
MAX_FULL_GRAD_MAX = 3.0e-5

MAX_BASE_GRAD_RMS = 2.0e-6
MAX_BASE_GRAD_MAX = 3.0e-4

MAX_DELTA_E_RANGE = 5.0e-4
MAX_DELTA_SIGMA2_RANGE = 5.0e-4

MAX_LOCAL_NEGATIVE_TO_POSITIVE_RATIO = 0.20
MAX_LOCAL_PHASE_LOCK_RMS = 2.0e-3

MAX_ACTIVE_PAIR_FRACTION = 0.01
MAX_VARIATIONAL_RELERR = 0.02

GLOBAL_FIXED_JUNCTION_ACTIVE = (
    b2.GLOBAL_FIXED_JUNCTION_ACTIVE
)


def pack_full_state(result):
    """Pack an already optimized full state back into optimizer ordering."""

    p = result.problem

    values_a = result.a[
        p.a_free
    ]

    return np.concatenate(
        [
            result.f[
                p.f_free
            ],

            result.s[
                p.s_free
            ],

            values_a.real,
            values_a.imag,

            result.ax[
                p.ax_free
            ],

            result.az[
                p.az_free
            ],
        ]
    )


def pack_base_state(result):
    """Pack an already optimized base-control state."""

    p = result.problem

    return np.concatenate(
        [
            result.f[
                p.f_free
            ],

            result.s[
                p.s_free
            ],

            result.ax[
                p.ax_free
            ],

            result.az[
                p.az_free
            ],
        ]
    )


def refined_full_case(
    chi,
    n,
    box_half,
):
    """Continue one full solution from its previous optimized state."""

    initial = fc.solve_full_case(
        chi,
        n,
        box_half,
    )

    p = initial.problem

    x = pack_full_state(
        initial
    )

    last = None

    for stage in range(3):

        last = minimize(
            lambda vector: fc.objective_and_gradient(
                p,
                vector,
            ),
            x,
            method="L-BFGS-B",
            jac=True,
            bounds=fc.optimizer_bounds(
                p
            ),
            options={
                "maxiter":
                    2500,

                "ftol":
                    1.0e-15,

                "gtol":
                    1.0e-10,

                "maxls":
                    100,

                "maxcor":
                    30,
            },
        )

        x = np.array(
            last.x,
            copy=True,
        )

        _, gradient = (
            fc.objective_and_gradient(
                p,
                x,
            )
        )

        grad_rms = float(
            np.linalg.norm(
                gradient
            )
            /
            math.sqrt(
                gradient.size
            )
        )

        grad_max = float(
            np.max(
                np.abs(
                    gradient
                )
            )
        )

        if (
            grad_rms
            <
            MAX_FULL_GRAD_RMS

            and
            grad_max
            <
            MAX_FULL_GRAD_MAX
        ):
            break

    (
        f,
        s,
        a,
        ax,
        az,
    ) = fc.unpack(
        p,
        x,
    )

    energy, gradient = (
        fc.objective_and_gradient(
            p,
            x,
        )
    )

    grad_rms = float(
        np.linalg.norm(
            gradient
        )
        /
        math.sqrt(
            gradient.size
        )
    )

    grad_max = float(
        np.max(
            np.abs(
                gradient
            )
        )
    )

    delta_energy = (
        energy
        -
        initial.energy_reference
    )

    mu_full = (
        initial.mu_fixed
        +
        delta_energy
    )

    measure = (
        p.weights
        *
        p.dx
        *
        p.dx
    )

    delta_sigma2 = float(
        np.sum(
            measure
            *
            (
                s
                *
                s

                -
                p.s0
                *
                p.s0
            )
        )
    )

    sigma2_full = (
        initial.sigma2_background
        +
        delta_sigma2
    )

    success = (
        grad_rms
        <
        MAX_FULL_GRAD_RMS

        and
        grad_max
        <
        MAX_FULL_GRAD_MAX
    )

    return fc.FullResult(
        chi=float(
            chi
        ),

        n=n,
        box_half=box_half,
        dx=p.dx,

        success=success,

        optimizer_message=(
            ""
            if last is None
            else str(
                last.message
            )
        ),

        iterations=(
            0
            if last is None
            else int(
                last.nit
            )
        ),

        energy_reference=(
            initial.energy_reference
        ),

        energy_full=float(
            energy
        ),

        relaxation_delta_energy=float(
            delta_energy
        ),

        mu_fixed=float(
            initial.mu_fixed
        ),

        mu_full=float(
            mu_full
        ),

        sigma2_background=float(
            initial.sigma2_background
        ),

        sigma2_full=float(
            sigma2_full
        ),

        delta_sigma2=float(
            delta_sigma2
        ),

        grad_rms=grad_rms,
        grad_max=grad_max,

        f=f,
        s=s,
        a=a,
        ax=ax,
        az=az,

        problem=p,
    )


def refined_base_case(
    chi,
    n,
    box_half,
):
    """Continue one base-string lattice control to the declared residuals."""

    initial = audit.solve_base_case(
        chi,
        n,
        box_half,
    )

    p = initial.problem

    x = pack_base_state(
        initial
    )

    last = None

    for stage in range(3):

        last = minimize(
            lambda vector: audit.base_objective_and_gradient(
                p,
                vector,
            ),
            x,
            method="L-BFGS-B",
            jac=True,
            bounds=audit.base_bounds(
                p
            ),
            options={
                "maxiter":
                    2500,

                "ftol":
                    1.0e-15,

                "gtol":
                    1.0e-10,

                "maxls":
                    100,

                "maxcor":
                    30,
            },
        )

        x = np.array(
            last.x,
            copy=True,
        )

        _, gradient = (
            audit.base_objective_and_gradient(
                p,
                x,
            )
        )

        grad_rms = float(
            np.linalg.norm(
                gradient
            )
            /
            math.sqrt(
                gradient.size
            )
        )

        grad_max = float(
            np.max(
                np.abs(
                    gradient
                )
            )
        )

        if (
            grad_rms
            <
            MAX_BASE_GRAD_RMS

            and
            grad_max
            <
            MAX_BASE_GRAD_MAX
        ):
            break

    (
        f,
        s,
        ax,
        az,
    ) = audit.unpack_base(
        p,
        x,
    )

    energy, gradient = (
        audit.base_objective_and_gradient(
            p,
            x,
        )
    )

    grad_rms = float(
        np.linalg.norm(
            gradient
        )
        /
        math.sqrt(
            gradient.size
        )
    )

    grad_max = float(
        np.max(
            np.abs(
                gradient
            )
        )
    )

    measure = (
        p.weights
        *
        p.dx
        *
        p.dx
    )

    sigma2 = float(
        np.sum(
            measure
            *
            s
            *
            s
        )
    )

    active = (
        audit.base_active_source(
            p,
            f,
            s,
            ax,
            az,
        )
    )

    delta_energy = (
        energy
        -
        initial.energy_initial
    )

    delta_sigma2 = (
        sigma2
        -
        initial.sigma2_initial_grid
    )

    delta_active = (
        active
        -
        initial.active_initial
    )

    success = (
        grad_rms
        <
        MAX_BASE_GRAD_RMS

        and
        grad_max
        <
        MAX_BASE_GRAD_MAX
    )

    return audit.BaseResult(
        chi=float(
            chi
        ),

        n=n,
        box_half=box_half,
        dx=p.dx,

        success=success,

        iterations=(
            0
            if last is None
            else int(
                last.nit
            )
        ),

        message=(
            ""
            if last is None
            else str(
                last.message
            )
        ),

        energy_initial=float(
            initial.energy_initial
        ),

        energy_relaxed=float(
            energy
        ),

        delta_energy=float(
            delta_energy
        ),

        sigma2_initial_grid=float(
            initial.sigma2_initial_grid
        ),

        sigma2_relaxed_grid=float(
            sigma2
        ),

        delta_sigma2=float(
            delta_sigma2
        ),

        active_initial=float(
            initial.active_initial
        ),

        active_relaxed=float(
            active
        ),

        delta_active=float(
            delta_active
        ),

        grad_rms=grad_rms,
        grad_max=grad_max,

        f=f,
        s=s,

        ax=ax,
        az=az,

        problem=p,
    )


PAIR_CACHE = {}


def matched_pair(
    chi,
    n,
    box_half,
):
    """Return one fully refined matched full/base pair."""

    key = (
        round(
            float(
                chi
            ),
            9,
        ),
        int(
            n
        ),
        float(
            box_half
        ),
    )

    if key in PAIR_CACHE:
        return PAIR_CACHE[
            key
        ]

    full = refined_full_case(
        chi,
        n,
        box_half,
    )

    base = refined_base_case(
        chi,
        n,
        box_half,
    )

    delta_e = (
        full.relaxation_delta_energy
        -
        base.delta_energy
    )

    delta_sigma2 = (
        full.delta_sigma2
        -
        base.delta_sigma2
    )

    sigma2 = (
        full.sigma2_background
        +
        delta_sigma2
    )

    active_full = (
        fc.active_source_diagnostics(
            full
        )
    )

    delta_active = (
        active_full[
            "active_relaxation_delta"
        ]

        -
        base.delta_active
    )

    endpoint_active = (
        GLOBAL_FIXED_JUNCTION_ACTIVE
        +
        delta_active
    )

    pair_active = (
        4.0
        *
        full.sigma2_background
        *
        (
            b2.OMEGA**2
            +
            b2.K_LONG**2
        )
    )

    active_fraction = (
        2.0
        *
        abs(
            endpoint_active
        )
        /
        pair_active
    )

    record = {
        "full":
            full,

        "base":
            base,

        "delta_e":
            float(
                delta_e
            ),

        "delta_sigma2":
            float(
                delta_sigma2
            ),

        "sigma2":
            float(
                sigma2
            ),

        "endpoint_active":
            float(
                endpoint_active
            ),

        "active_fraction":
            float(
                active_fraction
            ),
    }

    PAIR_CACHE[
        key
    ] = record

    return record


def numerical_range(values):
    array = np.asarray(
        values,
        dtype=float,
    )

    return float(
        np.max(
            array
        )
        -
        np.min(
            array
        )
    )


def local_contrast(full):
    """Measure one-sided contrast without demanding local asymptotic vacuum."""

    p = full.problem

    x = (
        p.fixed_result.problem.x
    )

    center = int(
        np.argmin(
            np.abs(
                x
            )
        )
    )

    L = full.box_half

    negative = (
        (
            x
            >
            -0.75
            *
            L
        )
        &
        (
            x
            <
            -0.45
            *
            L
        )
    )

    positive = (
        (
            x
            >
            0.45
            *
            L
        )
        &
        (
            x
            <
            0.75
            *
            L
        )
    )

    negative_a = float(
        np.max(
            np.abs(
                full.a[
                    negative,
                    center,
                ]
            )
        )
        /
        m.F_A
    )

    positive_a = float(
        np.min(
            np.abs(
                full.a[
                    positive,
                    center,
                ]
            )
        )
        /
        m.F_A
    )

    ratio = (
        negative_a
        /
        max(
            positive_a,
            1.0e-30,
        )
    )

    morph = (
        b2.local_morphology(
            full
        )
    )

    return {
        "negative":
            negative_a,

        "positive":
            positive_a,

        "ratio":
            ratio,

        "phase_lock":
            float(
                morph[
                    "phase_lock"
                ]
            ),
    }


def global_outer_morphology():
    """Reconstruct the verified large-domain 018A-6A outer solution."""

    m.CHI_SELECTED = (
        CHI_SELECTED
    )

    radial = (
        m.solve_017p_background()
    )

    result = (
        m.run_case(
            radial,
            n=141,
            box_half=100.0,
        )
    )

    metrics = (
        m.morphology_metrics(
            result
        )
    )

    passed = (
        result.optimizer_success

        and
        metrics[
            "negative_wall_max"
        ]
        <
        0.02

        and
        metrics[
            "positive_recovery_min"
        ]
        >
        0.95

        and
        metrics[
            "phase_lock_rms"
        ]
        <
        1.0e-3
    )

    return (
        result,
        metrics,
        passed,
    )


def main():
    original_chi = float(
        m.CHI_SELECTED
    )

    print(
        "=== ANTIGRAVITY_RESEARCH 018A-6B3 ==="
    )

    print(
        "QUESTION="
        "DOES_FINE_CONTINUATION_CLOSE_THE_LOCAL_KLS_JUNCTION_WHILE_MATCHING_THE_VERIFIED_GLOBAL_OUTER_WALL"
    )

    print(
        "\n=== LARGE-DOMAIN OUTER WALL RECONSTRUCTION ==="
    )

    (
        outer,
        outer_metrics,
        outer_pass,
    ) = global_outer_morphology()

    print(
        "OUTER_NEGATIVE_WALL_A_OVER_F="
        f"{outer_metrics['negative_wall_max']:.15e}"
    )

    print(
        "OUTER_POSITIVE_RECOVERY_A_OVER_F="
        f"{outer_metrics['positive_recovery_min']:.15e}"
    )

    print(
        "OUTER_PHASE_LOCK_RMS="
        f"{outer_metrics['phase_lock_rms']:.15e}"
    )

    print(
        "OUTER_GLOBAL_WALL_TERMINATION="
        f"{'PASS' if outer_pass else 'FAIL'}"
    )

    print(
        "\n=== REFINED MATCHED RESOLUTION SEQUENCE ==="
    )

    resolution = []

    for (
        n,
        L,
    ) in RESOLUTION_CASES:

        record = matched_pair(
            CHI_SELECTED,
            n,
            L,
        )

        resolution.append(
            record
        )

        full = record[
            "full"
        ]

        base = record[
            "base"
        ]

        print(
            "REFINED_RESOLUTION "
            f"N={n} "
            f"L={L:.3f} "
            f"DX={full.dx:.12f} "
            f"FULL_SOLVER={'PASS' if full.success else 'FAIL'} "
            f"BASE_SOLVER={'PASS' if base.success else 'FAIL'} "
            f"KLS_DELTA_E={record['delta_e']:+.15e} "
            f"KLS_DELTA_SIGMA2={record['delta_sigma2']:+.15e} "
            f"ACTIVE_PAIR_FRACTION={record['active_fraction']:.15e} "
            f"FULL_GRAD_RMS={full.grad_rms:.15e} "
            f"FULL_GRAD_MAX={full.grad_max:.15e} "
            f"BASE_GRAD_RMS={base.grad_rms:.15e} "
            f"BASE_GRAD_MAX={base.grad_max:.15e}"
        )

    solver_resolution_pass = all(
        record[
            "full"
        ].success
        and
        record[
            "base"
        ].success
        for record
        in resolution
    )

    de_resolution_range = numerical_range(
        [
            record[
                "delta_e"
            ]
            for record
            in resolution
        ]
    )

    ds_resolution_range = numerical_range(
        [
            record[
                "delta_sigma2"
            ]
            for record
            in resolution
        ]
    )

    matched_resolution_pass = (
        de_resolution_range
        <
        MAX_DELTA_E_RANGE

        and
        ds_resolution_range
        <
        MAX_DELTA_SIGMA2_RANGE
    )

    print(
        "REFINED_KLS_DELTA_E_RESOLUTION_RANGE="
        f"{de_resolution_range:.15e}"
    )

    print(
        "REFINED_KLS_DELTA_SIGMA2_RESOLUTION_RANGE="
        f"{ds_resolution_range:.15e}"
    )

    print(
        "REFINED_RESOLUTION_SOLVERS="
        f"{'PASS' if solver_resolution_pass else 'FAIL'}"
    )

    print(
        "REFINED_MATCHED_RESOLUTION_CONVERGENCE="
        f"{'PASS' if matched_resolution_pass else 'FAIL'}"
    )

    print(
        "\n=== REFINED MATCHED PATCH SEQUENCE ==="
    )

    patches = []

    for (
        n,
        L,
    ) in PATCH_CASES:

        record = matched_pair(
            CHI_SELECTED,
            n,
            L,
        )

        patches.append(
            record
        )

        print(
            "REFINED_PATCH "
            f"N={n} "
            f"L={L:.3f} "
            f"DX={record['full'].dx:.12f} "
            f"FULL_SOLVER={'PASS' if record['full'].success else 'FAIL'} "
            f"BASE_SOLVER={'PASS' if record['base'].success else 'FAIL'} "
            f"KLS_DELTA_E={record['delta_e']:+.15e} "
            f"KLS_DELTA_SIGMA2={record['delta_sigma2']:+.15e}"
        )

    solver_patch_pass = all(
        record[
            "full"
        ].success
        and
        record[
            "base"
        ].success
        for record
        in patches
    )

    de_patch_range = numerical_range(
        [
            record[
                "delta_e"
            ]
            for record
            in patches
        ]
    )

    ds_patch_range = numerical_range(
        [
            record[
                "delta_sigma2"
            ]
            for record
            in patches
        ]
    )

    matched_patch_pass = (
        de_patch_range
        <
        MAX_DELTA_E_RANGE

        and
        ds_patch_range
        <
        MAX_DELTA_SIGMA2_RANGE
    )

    print(
        "REFINED_KLS_DELTA_E_PATCH_RANGE="
        f"{de_patch_range:.15e}"
    )

    print(
        "REFINED_KLS_DELTA_SIGMA2_PATCH_RANGE="
        f"{ds_patch_range:.15e}"
    )

    print(
        "REFINED_PATCH_SOLVERS="
        f"{'PASS' if solver_patch_pass else 'FAIL'}"
    )

    print(
        "REFINED_MATCHED_PATCH_CONVERGENCE="
        f"{'PASS' if matched_patch_pass else 'FAIL'}"
    )

    selected = matched_pair(
        CHI_SELECTED,
        81,
        20.0,
    )

    contrast = local_contrast(
        selected[
            "full"
        ]
    )

    local_contrast_pass = (
        contrast[
            "ratio"
        ]
        <
        MAX_LOCAL_NEGATIVE_TO_POSITIVE_RATIO
    )

    local_phase_pass = (
        contrast[
            "phase_lock"
        ]
        <
        MAX_LOCAL_PHASE_LOCK_RMS
    )

    print(
        "\n=== OUTER + INNER TOPOLOGY MATCH ==="
    )

    print(
        "LOCAL_NEGATIVE_A_OVER_F="
        f"{contrast['negative']:.15e}"
    )

    print(
        "LOCAL_POSITIVE_A_OVER_F="
        f"{contrast['positive']:.15e}"
    )

    print(
        "LOCAL_NEGATIVE_TO_POSITIVE_RATIO="
        f"{contrast['ratio']:.15e}"
    )

    print(
        "LOCAL_PHASE_LOCK_RMS="
        f"{contrast['phase_lock']:.15e}"
    )

    print(
        "LOCAL_ONE_SIDED_CONTRAST="
        f"{'PASS' if local_contrast_pass else 'FAIL'}"
    )

    print(
        "LOCAL_RELATIVE_PHASE_LOCKING="
        f"{'PASS' if local_phase_pass else 'FAIL'}"
    )

    topology_match_pass = (
        outer_pass
        and
        local_contrast_pass
        and
        local_phase_pass
    )

    print(
        "FINE_CORE_PLUS_GLOBAL_OUTER_TOPOLOGY="
        f"{'PASS' if topology_match_pass else 'FAIL'}"
    )

    active_pass = (
        selected[
            "active_fraction"
        ]
        <
        MAX_ACTIVE_PAIR_FRACTION
    )

    print(
        "REFINED_SELECTED_ACTIVE_PAIR_FRACTION="
        f"{selected['active_fraction']:.15e}"
    )

    print(
        "REFINED_ACTIVE_SOURCE_BUDGET="
        f"{'PASS' if active_pass else 'FAIL'}"
    )

    print(
        "\n=== REFINED COMMON-GRID CHI CONTINUATION ==="
    )

    records = []

    for chi in CHI_VALUES:

        local = matched_pair(
            chi,
            CHI_CASE[
                0
            ],
            CHI_CASE[
                1
            ],
        )

        fixed_global, diag = (
            b2.global_fixed_case(
                chi
            )
        )

        mu = (
            fixed_global.junction_excess_energy
            +
            local[
                "delta_e"
            ]
        )

        a_eff = (
            diag.a_string
            +
            mu
        )

        sigma2 = (
            diag.sigma2
            +
            local[
                "delta_sigma2"
            ]
        )

        records.append(
            (
                float(
                    chi
                ),
                float(
                    a_eff
                ),
                float(
                    sigma2
                ),
            )
        )

        print(
            "REFINED_CHI "
            f"CHI={chi:.9f} "
            f"MU={mu:+.15e} "
            f"A_EFF={a_eff:.15e} "
            f"SIGMA2={sigma2:.15e}"
        )

    chi_array = np.array(
        [
            x[
                0
            ]
            for x
            in records
        ]
    )

    a_array = np.array(
        [
            x[
                1
            ]
            for x
            in records
        ]
    )

    sigma_array = np.array(
        [
            x[
                2
            ]
            for x
            in records
        ]
    )

    ap = np.polyfit(
        chi_array,
        a_array,
        2,
    )

    sp = np.polyfit(
        chi_array,
        sigma_array,
        2,
    )

    da = float(
        np.polyval(
            np.polyder(
                ap
            ),
            CHI_SELECTED,
        )
    )

    ds = float(
        np.polyval(
            np.polyder(
                sp
            ),
            CHI_SELECTED,
        )
    )

    sigma_selected = float(
        sigma_array[
            -1
        ]
    )

    a_selected = float(
        a_array[
            -1
        ]
    )

    variational_error = (
        abs(
            da
            +
            sigma_selected
        )
        /
        sigma_selected
    )

    variational_pass = (
        variational_error
        <
        MAX_VARIATIONAL_RELERR
    )

    print(
        "REFINED_VARIATIONAL_RELERR="
        f"{variational_error:.15e}"
    )

    print(
        "REFINED_VARIATIONAL_IDENTITY="
        f"{'PASS' if variational_pass else 'FAIL'}"
    )

    ct2 = (
        1.0
        /
        (
            1.0
            +
            2.0
            *
            CHI_SELECTED
            *
            sigma_selected
            /
            a_selected
        )
    )

    cl2 = (
        1.0
        /
        (
            1.0
            +
            2.0
            *
            CHI_SELECTED
            *
            ds
            /
            sigma_selected
        )
    )

    eos_pass = (
        0.0
        <
        ct2
        <=
        1.0

        and
        0.0
        <
        cl2
        <=
        1.0
    )

    (
        stability_pass,
        min_disc,
        max_imag,
        worst_mode,
    ) = fc.extrinsic_stability(
        ct2,
        cl2,
    )

    print(
        "REFINED_CT2="
        f"{ct2:.15e}"
    )

    print(
        "REFINED_CL2="
        f"{cl2:.15e}"
    )

    print(
        "REFINED_EOS_HEALTH="
        f"{'PASS' if eos_pass else 'FAIL'}"
    )

    print(
        "REFINED_MIN_M2_TO_M40_DISCRIMINANT="
        f"{min_disc:+.15e}"
    )

    print(
        f"REFINED_WORST_MODE={worst_mode}"
    )

    print(
        "REFINED_MAX_ROOT_IMAG="
        f"{max_imag:.15e}"
    )

    print(
        "REFINED_M2_TO_M40_STABILITY="
        f"{'PASS' if stability_pass else 'FAIL'}"
    )

    selected_mu = (
        outer.junction_excess_energy
        +
        selected[
            "delta_e"
        ]
    )

    one = fc.stationarity(
        selected_mu,
        1,
    )

    two = fc.stationarity(
        selected_mu,
        2,
    )

    print(
        "REFINED_GLOBAL_MU_ESTIMATE="
        f"{selected_mu:+.15e}"
    )

    print(
        "REFINED_ONE_JUNCTION_STATIONARITY="
        f"{'PASS' if one['passed'] else 'FAIL'}"
    )

    print(
        "REFINED_TWO_JUNCTION_STATIONARITY="
        f"{'PASS' if two['passed'] else 'FAIL'}"
    )

    overall = (
        solver_resolution_pass
        and
        solver_patch_pass
        and
        matched_resolution_pass
        and
        matched_patch_pass
        and
        topology_match_pass
        and
        active_pass
        and
        variational_pass
        and
        eos_pass
        and
        stability_pass
        and
        bool(
            one[
                "passed"
            ]
        )
        and
        bool(
            two[
                "passed"
            ]
        )
    )

    print(
        "\n=== 018A-6B3 DECISION ==="
    )

    print(
        "REFINED_RESOLUTION_SOLVERS="
        f"{'PASS' if solver_resolution_pass else 'FAIL'}"
    )

    print(
        "REFINED_PATCH_SOLVERS="
        f"{'PASS' if solver_patch_pass else 'FAIL'}"
    )

    print(
        "REFINED_MATCHED_RESOLUTION_CONVERGENCE="
        f"{'PASS' if matched_resolution_pass else 'FAIL'}"
    )

    print(
        "REFINED_MATCHED_PATCH_CONVERGENCE="
        f"{'PASS' if matched_patch_pass else 'FAIL'}"
    )

    print(
        "FINE_CORE_PLUS_GLOBAL_OUTER_TOPOLOGY="
        f"{'PASS' if topology_match_pass else 'FAIL'}"
    )

    print(
        "REFINED_ACTIVE_SOURCE_BUDGET="
        f"{'PASS' if active_pass else 'FAIL'}"
    )

    print(
        "REFINED_VARIATIONAL_IDENTITY="
        f"{'PASS' if variational_pass else 'FAIL'}"
    )

    print(
        "REFINED_EOS_HEALTH="
        f"{'PASS' if eos_pass else 'FAIL'}"
    )

    print(
        "REFINED_M2_TO_M40_STABILITY="
        f"{'PASS' if stability_pass else 'FAIL'}"
    )

    print(
        "REFINED_ONE_JUNCTION_STATIONARITY="
        f"{'PASS' if one['passed'] else 'FAIL'}"
    )

    print(
        "REFINED_TWO_JUNCTION_STATIONARITY="
        f"{'PASS' if two['passed'] else 'FAIL'}"
    )

    print(
        "018A6B3_FINE_COUPLED_JUNCTION_CLOSEOUT="
        f"{'GREEN' if overall else 'RED'}"
    )

    if overall:

        print(
            "FULLY_COUPLED_LOCAL_2D_KLS_JUNCTION="
            "SUPPORTED_WITH_FINE_CORE_PLUS_MATCHED_GLOBAL_OUTER_SOLUTION"
        )

        print(
            "LOCAL_MICROSCOPIC_JUNCTION_ESCALATION="
            "STOP"
        )

        print(
            "NEXT="
            "018A7_COMPLETE_MICROSCOPIC_GRAVITY_CLOSEOUT"
        )

    else:

        print(
            "FULLY_COUPLED_LOCAL_2D_KLS_JUNCTION="
            "NOT_YET_ESTABLISHED"
        )

        print(
            "NEXT="
            "IDENTIFY_REMAINING_NUMERICAL_CHANNEL_ONLY"
        )

    print(
        "POSITIVE_TOTAL_ACTIVE_MASS_WITH_COMPLETE_NEW_SECTOR="
        "NOT_YET_TESTED"
    )

    print(
        "FINITE_PAYLOAD_GRAVITY_WITH_COMPLETE_NEW_SECTOR="
        "NOT_YET_TESTED"
    )

    print(
        "FULL_018A_GATE="
        "NOT_YET_GREEN"
    )

    print(
        "018B_FULL_FINITE_THICKNESS_DRUM="
        "NOT_YET_AUTHORIZED"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE="
        "NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "PROJECT_DERIVED_018A_FINE_COUPLED_JUNCTION_CLOSEOUT"
    )

    m.CHI_SELECTED = (
        original_chi
    )


if __name__ == "__main__":
    main()
