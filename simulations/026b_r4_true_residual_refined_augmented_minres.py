#!/usr/bin/env python3
"""026B — true-antigravity B7 N=81 stationary companion + force convergence.

PURPOSE
-------
Advance the strongest actual true-antigravity field stack:

    B = 7
    eta = 0.4
    m = 8

from the GREEN strict-stationary N=73 result of 026A to an independently
re-solved N=81 companion field.

026A established at N=73:

    strict unrestricted stationarity
    |B| = 7 topology
    pointwise DEC
    positive total active mass
    negative active region
    active-trace consistency
    independently reconstructed cubic/quintic outward finite-payload force

but the N65 -> N73 continuous-force mean changed by approximately 90.4%.

Therefore force magnitude is NOT continuum converged.

SCIENTIFIC QUESTION
-------------------
When the SAME physical model and SAME unrestricted field equations are solved
on N=81:

1. does strict stationarity survive?
2. do topology, DEC, active-mass structure and smoothness survive?
3. do the previously predeclared companion-resolution local observables
   converge?
4. is the finite-payload continuous force still independently certified
   OUTWARD?
5. does the N73 -> N81 force change shrink enough to indicate genuine approach
   toward the continuum?

WHY N=81 BEFORE THE FULL HESSIAN
--------------------------------
A full physical Hessian is meaningful only at a trustworthy stationary source.
026A certified N=73 itself but did not establish force-resolution convergence.

The project already established the required ordering:

    strict fine stationary field
    ->
    continuous finite-payload force resolution
    ->
    companion-grid convergence
    ->
    dense orientation robustness
    ->
    full physical tangent Hessian
    ->
    direct curvature / fission tests
    ->
    nonlinear Einstein-Skyrme continuation

This run therefore does NOT compute the full Hessian.

N=81 DEFECT-CORRECTION STRATEGY
-------------------------------
The final N=73 field is a numerical approximation to the continuum field.
Prolongating that solution onto N=81 creates primarily a discretization defect.

Rather than restarting hundreds of generic quasi-Newton iterations, solve the
new discrete Euler-Lagrange defect directly with the 026A coupled method:

    (H + mu I) delta = -g

using residual-informed augmentation and deflated/Schur-complement MINRES.

Only the exact three global pion-isorotation zero modes are projected out.
Translations, spatial rotations, deformations, splitting modes, shear, twist,
and arbitrary local perturbations remain physical.

The N73 L-BFGS history is deliberately NOT required as a persisted
preconditioner.  The compact 026A audit found that all secants had positive
curvature but that the displacement history was strongly directionally
redundant.  N=81 therefore starts from the actual residual-informed augmented
space rather than assuming the old quasi-Newton memory is transferable.

STRICT STATIONARITY
-------------------
Unchanged:

    GRAD_RMS <= 1.5e-3
    GRAD_MAX <= 5.0e-2

No tolerance is weakened.

PREDECLARED LOCAL COMPANION-GRID TOLERANCES
-------------------------------------------
Inherited from the earlier 023C2A resolution gate:

    continuum-energy relative change <= 1.5e-2
    min-active-fraction absolute change <= 3.0e-3
    topology4 absolute change <= 1.0e-2

Both N=73 and N=81 must independently satisfy the physical gates.

CONTINUOUS FORCE
----------------
Only after strict N=81 stationarity and the local companion gate:

    S = rho + p1 + p2 + p3 = 2(e4 - V)

is reconstructed independently from normalized cubic and quintic tensor
splines.

For the same uniform spherical payload and historically weakest direction:

    A_n = integral S(x)
                 n.(x-c) / max(|x-c|^3, R^3)
                 d^3x.

Positive A_n means outward acceleration in the inherited linearized-GR
convention.

Each representation uses:

    q = 2, 3, 4 far-cell Gauss cubature
    aggressive near-payload subdivision
    normalized-spline derivative validation
    constant-source analytic-prism validation

Sign certification remains:

    min(|F_cubic|,|F_quintic|)
      > 5 * max(
            cubic internal error,
            quintic internal error,
            cubic/quintic spread
          )

and cubic/quintic must agree in sign.

N73 -> N81 FORCE-CONVERGENCE PREFILTER
--------------------------------------
A strong prefilter requires:

    N81 sign certified OUTWARD

    abs(F81_mean - F73_mean)
    -------------------------------- <= 0.10
    max(abs(F81_mean),abs(F73_mean))

and:

    N81 representation spread
    ------------------------- <= 1
    N73 representation spread

The 10% condition is deliberately strict and corresponds to the old
predeclared worst-direction L-infinity scale.  It is NOT by itself a complete
continuum proof.

The run additionally reports the shrinkage ratio

    |F81-F73| / |F73-F65|

as a diagnostic only.

PROMOTION
---------
GREEN here means only:

    STRICT_N81_STATIONARY_COMPANION
    +
    LOCAL_N73_N81_FIELD_CONVERGENCE
    +
    CERTIFIED_OUTWARD_N81_SENTINEL
    +
    STRONG_N73_N81_SENTINEL_CONVERGENCE_PREFILTER

It authorizes the next dense continuous-force robustness gate.

FALSIFIERS / STOP RULES
-----------------------
* Loss of |B|=7 or physical-field conditions: stop.
* Failure to reach strict N81 stationarity: checkpoint and rerun 026B.
* Local companion-grid tolerances fail: do not run expensive force integration.
* Certified inward N81 force: preserve result and require one further
  resolution before declaring a continuum sign reversal.
* Outward but >10% N73->N81 change: do not run Hessian; move to N89.
* Never weaken stationarity, topology, DEC, or force thresholds.

CLAIM LIMITS
------------
This run does NOT establish:

    dense 320-direction continuous-force convergence
    full unrestricted Hessian stability
    finite-amplitude fission stability
    nonlinear Einstein-Skyrme consistency
    escape from the 1/G energy scale
    a material realization
    an experiment
    a practical antigravity device
    discovery of new physics

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_026B_TRUE_ANTIGRAVITY_B7_N81_FORCE_CONVERGENCE_GATE
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SIM = ROOT / "simulations"
DATA = ROOT / "results/data"

A26_SOURCE = (
    SIM
    / "026a_true_antigravity_b7_n73_augmented_deflated_minres_gate.py"
)

N73_FIELD = (
    DATA
    / "026a_true_antigravity_strict_stationary_b7_n73.npz"
)

N73_SUMMARY = (
    DATA
    / "026a_true_antigravity_n73_augmented_minres_summary.json"
)

CHECKPOINT = (
    DATA
    / "026b_true_antigravity_n81_augmented_minres_checkpoint.npz"
)

FINAL = (
    DATA
    / "026b_true_antigravity_strict_stationary_b7_n81.npz"
)

SUMMARY = (
    DATA
    / "026b_true_antigravity_n81_force_convergence_summary.json"
)


EXPECTED_A26_SHA256 = "1023bcafde9aabd3fd432834b6ae2f4cd89fdf4e80ce5fc422a56e929dc09508"
EXPECTED_N73_FIELD_SHA256 = "6da8b702802b2fb14a92d708f1fdd05ec59134ab3d80f34487837b1f6744c747"
EXPECTED_N73_SUMMARY_SHA256 = "d5bbf41306e23113570821b3b67eef570c68e8940657d327d2b9242fee95cc8a"


B = 7
ETA = 0.4
MASS = 8.0

N73 = 73
N81 = 81

GRAD_RMS_TOL = 1.5e-3
GRAD_MAX_TOL = 5.0e-2

MAX_NEIGHBOR_ANGLE = 0.70
MAX_TOPOLOGY_RELERR = 3.0e-2

MIN_NEGATIVE_ACTIVE_FRACTION = 1.0e-2
MIN_DEC_SCALED_MARGIN = -1.0e-9
MAX_ACTIVE_TRACE_SCALED = 1.0e-10

MAX_PAIR_ENERGY_RELCHANGE = 1.5e-2
MAX_PAIR_ACTIVE_FRACTION_ABSCHANGE = 3.0e-3
MAX_PAIR_TOPOLOGY_ABSCHANGE = 1.0e-2

MAX_FORCE_MEAN_RELCHANGE = 1.0e-1
MAX_REPRESENTATION_SPREAD_RATIO = 1.0

MAX_OUTER = max(
    1,
    int(
        os.environ.get(
            "AG_026B_MAX_OUTER",
            "12",
        )
    ),
)

MINRES_MAXITER = max(
    16,
    int(
        os.environ.get(
            "AG_026B_MINRES_MAXITER",
            "64",
        )
    ),
)

MINRES_RTOL = float(
    os.environ.get(
        "AG_026B_MINRES_RTOL",
        "0.02",
    )
)

MAX_LINEAR_RELRES = float(
    os.environ.get(
        "AG_026B_MAX_LINEAR_RELRES",
        "0.35",
    )
)

MAX_AUGMENT_DIM = max(
    10,
    int(
        os.environ.get(
            "AG_026B_MAX_AUGMENT_DIM",
            "18",
        )
    ),
)

HVP_POINT_ANGLE = float(
    os.environ.get(
        "AG_026B_HVP_POINT_ANGLE",
        "2e-4",
    )
)

DAMPING_FACTORS = tuple(
    float(x)
    for x in os.environ.get(
        "AG_026B_DAMPING_FACTORS",
        "0,0.02,0.10,0.50,2.0",
    ).split(",")
)


def sha256(path: Path) -> str:
    """Return a streaming SHA-256 digest."""

    h = hashlib.sha256()

    with path.open("rb") as fh:
        for block in iter(
            lambda: fh.read(
                8 * 1024 * 1024
            ),
            b"",
        ):
            h.update(
                block
            )

    return h.hexdigest()


def require(path: Path) -> None:
    """Fail closed on a missing artifact."""

    if not path.is_file():
        raise RuntimeError(
            f"Required artifact missing: {path}"
        )


def load_module(
    name: str,
    path: Path,
):
    """Import one repository module without executing main()."""

    spec = importlib.util.spec_from_file_location(
        name,
        path,
    )

    if (
        spec is None
        or spec.loader is None
    ):
        raise RuntimeError(
            f"Cannot import {path}"
        )

    module = importlib.util.module_from_spec(
        spec
    )

    sys.modules[
        name
    ] = module

    spec.loader.exec_module(
        module
    )

    return module


def json_default(x):
    """Serialize NumPy values for the audit summary."""

    if isinstance(
        x,
        np.generic,
    ):
        return x.item()

    if isinstance(
        x,
        np.ndarray,
    ):
        return x.tolist()

    raise TypeError(
        type(x).__name__
    )


def relchange(
    a: float,
    b: float,
) -> float:
    """Symmetric scale-aware relative change."""

    return abs(
        float(a)
        - float(b)
    ) / max(
        abs(
            float(a)
        ),
        abs(
            float(b)
        ),
        1e-300,
    )


def merit(
    rms: float,
    gmax: float,
) -> float:
    """Unchanged normalized stationarity merit."""

    return max(
        rms
        / GRAD_RMS_TOL,
        gmax
        / GRAD_MAX_TOL,
    )


def audit_inputs() -> dict:
    """Require the exact green 026A lineage used to create this file."""

    for path in (
        A26_SOURCE,
        N73_FIELD,
        N73_SUMMARY,
    ):
        require(
            path
        )

    actual = {
        "a26_source":
            sha256(
                A26_SOURCE
            ),

        "n73_field":
            sha256(
                N73_FIELD
            ),

        "n73_summary":
            sha256(
                N73_SUMMARY
            ),
    }

    expected = {
        "a26_source":
            EXPECTED_A26_SHA256,

        "n73_field":
            EXPECTED_N73_FIELD_SHA256,

        "n73_summary":
            EXPECTED_N73_SUMMARY_SHA256,
    }

    print(
        "026B_A26_SOURCE_SHA256="
        + actual[
            "a26_source"
        ],
        flush=True,
    )

    print(
        "026B_N73_FIELD_SHA256="
        + actual[
            "n73_field"
        ],
        flush=True,
    )

    print(
        "026B_N73_SUMMARY_SHA256="
        + actual[
            "n73_summary"
        ],
        flush=True,
    )

    if actual != expected:
        raise RuntimeError(
            "026B fail-closed input hash audit failed"
        )

    summary = json.loads(
        N73_SUMMARY.read_text(
            encoding="utf-8"
        )
    )

    if (
        summary.get(
            "decision"
        )
        !=
        "GREEN_STRICT_N73_CONTINUOUS_OUTWARD_SENTINEL"
    ):
        raise RuntimeError(
            "026A summary is not the green N73 result"
        )

    force = summary.get(
        "force"
    )

    if (
        not isinstance(
            force,
            dict,
        )
        or not force.get(
            "certified",
            False,
        )
        or force.get(
            "sign"
        )
        != "OUTWARD"
    ):
        raise RuntimeError(
            "026A N73 outward force certificate missing"
        )

    if not summary.get(
        "final",
        {},
    ).get(
        "stationary",
        False,
    ):
        raise RuntimeError(
            "026A strict N73 stationarity missing"
        )

    print(
        "026B_026A_GREEN_LINEAGE_AUDIT=PASS",
        flush=True,
    )

    return summary


def load_modules():
    """Load the audited 026A machinery and its physical model."""

    a26 = load_module(
        "026b_a26",
        A26_SOURCE,
    )

    r5 = a26.load_module(
        "026b_r5",
        a26.R5_SOURCE,
    )

    r4 = r5.load_module(
        "026b_r4",
        r5.R4_SOURCE,
    )

    r3 = r4.load_module(
        "026b_r3",
        r4.R3_SOURCE,
    )

    r2 = r3.load_module(
        "026b_r2",
        r3.R2_SOURCE,
    )

    r = r3.load_module(
        "026b_r",
        r2.R_SOURCE,
    )

    qs2 = r3.load_module(
        "026b_qs2",
        r.QS2_SOURCE,
    )

    c2a = r3.load_module(
        "026b_c2a",
        r.C2A_SOURCE,
    )

    c2ar = qs2.load_module(
        "026b_c2ar",
        qs2.C2AR_SOURCE,
    )

    c2aqs = qs2.load_module(
        "026b_c2aqs",
        qs2.C2AQS_SOURCE,
    )

    cr2 = c2ar.load_module(
        "026b_cr2",
        c2ar.CR2_SOURCE,
    )

    cr3 = c2ar.load_module(
        "026b_cr3",
        c2ar.CR3_SOURCE,
    )

    cr4r = c2ar.load_module(
        "026b_cr4r",
        c2ar.CR4R_SOURCE,
    )

    cr3r = cr4r.load_module(
        "026b_cr3r",
        cr4r.CR3R_SOURCE,
    )

    # Reuse the successful 026A coupled method on N=81.
    # These are numerical-solver controls only.
    a26.N = N81
    a26.MINRES_MAXITER = MINRES_MAXITER
    a26.MINRES_RTOL = MINRES_RTOL
    a26.MAX_LINEAR_RELRES = (
        MAX_LINEAR_RELRES
    )
    a26.MAX_AUGMENT_DIM = (
        MAX_AUGMENT_DIM
    )
    a26.HVP_POINT_ANGLE = (
        HVP_POINT_ANGLE
    )
    a26.DAMPING_FACTORS = (
        DAMPING_FACTORS
    )

    # ---------------------------------------------------------------
    # N=81 inherited-helper grid binding.
    #
    # Several audited 023C stationarity modules were authored
    # specifically for N=73.  Their physical operators are shape-
    # driven, but a small number of numerical diagnostics retain a
    # module-global N used only for tangent-array reshaping.
    #
    # Example:
    #
    #     r5.residual_metrics(...)
    #
    # reshapes the full tangent residual using
    #
    #     (N-2, N-2, N-2, 3).
    #
    # For this N=81 companion calculation those inherited numerical
    # globals must therefore be bound to N81.  This changes no action,
    # gradient, boundary condition, topology criterion, stress tensor,
    # force observable, or promotion threshold.
    #
    # Do NOT apply this mutation to the continuous-force module or the
    # N65 reference loader; only the N-specific stationarity helper
    # lineage is rebound.
    # ---------------------------------------------------------------

    grid_bound_modules = (
        ("026A", a26),
        ("R5", r5),
        ("R4", r4),
        ("R3", r3),
        ("R2", r2),
        ("R", r),
    )

    for grid_label, grid_module in grid_bound_modules:

        if hasattr(
            grid_module,
            "N",
        ):
            old_n = int(
                grid_module.N
            )

            grid_module.N = N81

            print(
                "026B_GRID_BIND "
                f"MODULE={grid_label} "
                f"OLD_N={old_n} "
                f"NEW_N={grid_module.N}",
                flush=True,
            )

    # Fail closed on the exact tangent-space size expected for N=81.
    expected_ndof = (
        3
        * (N81 - 2) ** 3
    )

    if expected_ndof != 1_479_117:
        raise RuntimeError(
            "Internal N81 tangent-space dimension audit failed"
        )

    print(
        "026B_N81_INTERIOR_TANGENT_DOF="
        f"{expected_ndof}",
        flush=True,
    )

    print(
        "026B_N81_GRID_BINDING_REPAIR=PASS",
        flush=True,
    )

    # ---------------------------------------------------------------
    # 026B local-curvature damping repair.
    #
    # Previous N=73 work already established that the positive-
    # curvature L-BFGS secant scale is valuable for PRECONDITIONING
    # but can exceed the actual current Hessian curvature by orders
    # of magnitude and therefore must not set the Newton shift.
    #
    # Preserve the exact L-BFGS inverse preconditioner and all secant
    # augmentation vectors.  Neutralize only the use of the secant
    # scale inside a26.coupled_solve's damping-scale calculation.
    #
    # The actual secant scale is still printed as a diagnostic.
    # ---------------------------------------------------------------

    _026b_original_curvature_scale = (
        r.curvature_scale_from_pairs
    )

    def _026b_preconditioner_only_curvature_scale(
        pairs,
    ):
        actual = float(
            _026b_original_curvature_scale(
                pairs
            )
        )

        print(
            "026B_SECANT_CURVATURE_SCALE_DIAGNOSTIC="
            f"{actual:.15e}",
            flush=True,
        )

        print(
            "026B_NEWTON_DAMPING_SCALE="
            "CURRENT_AUGMENTED_HESSIAN_NOT_SECANT_HISTORY",
            flush=True,
        )

        # Returning zero removes the old secant scale from
        #
        #     max(coarse_scale, pair_scale, ...)
        #
        # while leaving the pairs themselves untouched.
        return 0.0

    r.curvature_scale_from_pairs = (
        _026b_preconditioner_only_curvature_scale
    )

    print(
        "026B_SECANT_PRECONDITIONER_PRESERVED=YES",
        flush=True,
    )

    print(
        "026B_SECANT_DAMPING_SCALE_DISABLED=YES",
        flush=True,
    )

    print(
        "026B_DAMPING_LADDER="
        + ",".join(
            f"{x:g}"
            for x in DAMPING_FACTORS
        ),
        flush=True,
    )

    # ---------------------------------------------------------------
    # 026B-R3 ADAPTIVE FULL-NEWTON TRUST GLOBALIZATION
    #
    # The N81 continuation has now established:
    #
    #   * repeated unshifted Newton directions are descent directions;
    #   * MINRES linear residuals are small and falling;
    #   * topology and link smoothness survive every accepted step;
    #   * every candidate at the old 1.5e-3 point-rotation cap was
    #     accepted immediately at LS=0;
    #   * the old cap, inherited from the near-root N73 repair, is now
    #     the dominant restriction on progress.
    #
    # Restore an adaptive Riemannian trust radius similar to the
    # previously validated N73 Newton solver, while retaining every
    # exact nonlinear acceptance gate.
    #
    # We deliberately cap the N81 scout at 1e-2 rad rather than the
    # older 2e-2 rad N73 ceiling.
    #
    # If the full Newton step lies inside that radius, alpha0=1.
    # If it fails any exact nonlinear gate, ordinary factor-two
    # backtracking automatically returns toward the previous safe
    # step sizes.
    #
    # This changes ONLY solver globalization.  It changes no action,
    # field equation, stress tensor, topology criterion, DEC gate,
    # stationarity threshold, payload operator, or force criterion.
    # ---------------------------------------------------------------

    def _026b_adaptive_full_candidate(
        r4_arg,
        r_arg,
        qs2_arg,
        c2a_arg,
        cr2_arg,
        cr3_arg,
        state_arg,
        g_arg,
        E_arg,
        rms_arg,
        gmax_arg,
        direction_arg,
        label,
        frequency_guard,
        old_metrics,
    ):
        phi = state_arg.phi
        dx = state_arg.dx

        merit0 = r5.stationarity_merit(
            rms_arg,
            gmax_arg,
        )

        direction = cr3_arg.project_tangent(
            phi,
            direction_arg,
        )

        gd = cr3_arg.tangent_inner(
            g_arg,
            direction,
            dx,
        )

        g2 = max(
            cr3_arg.tangent_inner(
                g_arg,
                g_arg,
                dx,
            ),
            1e-300,
        )

        print(
            f"{label}_G_DOT_DELTA="
            f"{gd:.15e}",
            flush=True,
        )

        if (
            (not math.isfinite(gd))
            or gd
            >= -1e-12 * g2
        ):
            print(
                f"{label}_DESCENT=NO",
                flush=True,
            )
            return None

        print(
            f"{label}_DESCENT=YES",
            flush=True,
        )

        max_point = float(
            np.max(
                np.linalg.norm(
                    direction[
                        1:-1,
                        1:-1,
                        1:-1,
                    ],
                    axis=-1,
                )
            )
        )

        # Residual-adaptive trust radius.
        #
        # Current large N81 defects are permitted to test the full
        # Newton correction, up to a conservative 1e-2-radian maximum
        # per-site rotation.  Near the root the radius contracts
        # automatically toward 5e-4.
        trust_angle = min(
            1.0e-2,
            max(
                5.0e-4,
                0.25
                * rms_arg,
            ),
        )

        alpha = min(
            1.0,
            trust_angle
            / max(
                max_point,
                1e-300,
            ),
        )

        print(
            f"{label}_MAX_POINT="
            f"{max_point:.15e} "
            f"TRUST_ANGLE="
            f"{trust_angle:.15e} "
            f"ALPHA0="
            f"{alpha:.15e}",
            flush=True,
        )

        print(
            "026B_ADAPTIVE_TRUST "
            f"LABEL={label} "
            f"RMS={rms_arg:.15e} "
            f"MAX_POINT={max_point:.15e} "
            f"TRUST={trust_angle:.15e} "
            f"ALPHA0={alpha:.15e}",
            flush=True,
        )

        for ls in range(
            r5.MAX_LINESEARCH
        ):

            cand = (
                cr3_arg.exp_map_update(
                    phi,
                    direction,
                    alpha,
                )
            )

            Etrial = (
                cr3_arg.high_order_energy_gradient(
                    cand,
                    dx,
                    False,
                )[0]
            )

            if (
                (not math.isfinite(Etrial))
                or Etrial
                >
                E_arg
                + r5.ARMIJO_C1
                * alpha
                * gd
            ):
                print(
                    f"{label}_LS={ls} "
                    "ENERGY_ACCEPT=NO "
                    f"ALPHA={alpha:.15e}",
                    flush=True,
                )

                alpha *= 0.5
                continue

            ok, reason, _ = (
                qs2_arg.candidate_admissible(
                    cr3_arg,
                    cr2_arg,
                    cand,
                    dx,
                    state_arg.accepted_total
                    + 1,
                )
            )

            if not ok:

                print(
                    f"{label}_LS={ls} "
                    "ADMISSIBLE=NO "
                    f"REASON={reason} "
                    f"ALPHA={alpha:.15e}",
                    flush=True,
                )

                alpha *= 0.5
                continue

            pack = (
                r_arg.strict_stationarity(
                    cr3_arg,
                    cand,
                    dx,
                )
            )

            (
                Enew,
                _e2,
                _e4,
                _e0,
                gnew,
                rmsnew,
                gmaxnew,
                stationnew,
            ) = pack

            merit_new = (
                r5.stationarity_merit(
                    rmsnew,
                    gmaxnew,
                )
            )

            merit_ok = bool(
                stationnew
                or merit_new
                <=
                r5.HALFSTEP_MERIT_FACTOR
                * merit0
            )

            new_metrics = (
                r5.residual_metrics(
                    c2a_arg,
                    cand,
                    gnew,
                )
            )

            freq_ok = True

            if (
                frequency_guard
                and not stationnew
            ):

                high_cap = max(
                    0.35,
                    1.5
                    * old_metrics[
                        "high_frac"
                    ],
                )

                rough_cap = max(
                    1.50,
                    1.5
                    * old_metrics[
                        "rough"
                    ],
                )

                freq_ok = bool(
                    new_metrics[
                        "high_frac"
                    ]
                    <= high_cap
                    and new_metrics[
                        "rough"
                    ]
                    <= rough_cap
                )

            reduction = (
                merit0
                / max(
                    merit_new,
                    1e-300,
                )
            )

            print(
                f"{label}_LS={ls} "
                f"ALPHA={alpha:.15e} "
                f"ENERGY={Enew:.15e} "
                f"GRAD_RMS={rmsnew:.15e} "
                f"GRAD_MAX={gmaxnew:.15e} "
                f"STATIONARITY_MERIT="
                f"{merit_new:.15e} "
                f"MERIT_REDUCTION="
                f"{reduction:.15e} "
                f"HIGH_FRACTION="
                f"{new_metrics['high_frac']:.15e} "
                f"ROUGHNESS="
                f"{new_metrics['rough']:.15e} "
                "MERIT_ACCEPT="
                + (
                    "YES"
                    if merit_ok
                    else "NO"
                )
                + " FREQUENCY_ACCEPT="
                + (
                    "YES"
                    if freq_ok
                    else "NO"
                ),
                flush=True,
            )

            if merit_ok and freq_ok:

                print(
                    "026B_ADAPTIVE_TRUST_ACCEPT "
                    f"LABEL={label} "
                    f"LS={ls} "
                    f"ALPHA={alpha:.15e} "
                    f"MERIT_REDUCTION="
                    f"{reduction:.15e}",
                    flush=True,
                )

                return {
                    "cand":
                        cand,

                    "E":
                        Enew,

                    "g":
                        gnew,

                    "rms":
                        rmsnew,

                    "gmax":
                        gmaxnew,

                    "station":
                        stationnew,

                    "merit":
                        merit_new,

                    "metrics":
                        new_metrics,

                    "direction":
                        direction,

                    "alpha":
                        alpha,
                }

            alpha *= 0.5

        print(
            "026B_ADAPTIVE_TRUST_DIRECTION="
            "REJECTED_AFTER_FULL_BACKTRACK",
            flush=True,
        )

        return None

    r5.full_candidate = (
        _026b_adaptive_full_candidate
    )

    print(
        "026B_ADAPTIVE_FULL_NEWTON_TRUST=ENABLED",
        flush=True,
    )

    print(
        "026B_ADAPTIVE_TRUST_CAP_RAD="
        "1.000000000000000e-02",
        flush=True,
    )

    print(
        "026B_ADAPTIVE_TRUST_FLOOR_RAD="
        "5.000000000000000e-04",
        flush=True,
    )

    print(
        "026B_ADAPTIVE_TRUST_BACKTRACK="
        "FACTOR_TWO",
        flush=True,
    )

    # ---------------------------------------------------------------
    # 026B-R4 — TRUE-RESIDUAL ITERATIVE-REFINEMENT CLOSURE
    #
    # SCIENTIFIC / NUMERICAL MOTIVATION
    # ---------------------------------
    # 026B-R3 reached the near-root regime but reproduced a failure
    # already diagnosed by the project's N73 R3 solver:
    #
    #     MINRES INFO=0
    #
    # can coexist with an independently restored Newton-model
    # residual too large to certify the direction.
    #
    # For an inexact Newton step we require the actual linear model:
    #
    #     A x = b
    #
    # to satisfy a true Euclidean residual criterion
    #
    #     ||b - A x|| / ||b|| <= eta.
    #
    # This wrapper therefore:
    #
    #   1. runs the inherited symmetric MINRES solve;
    #   2. explicitly reconstructs b-Ax;
    #   3. if necessary solves A e = b-Ax;
    #   4. updates x <- x+e;
    #   5. repeats in a bounded iterative-refinement loop;
    #   6. returns INFO=0 only when the TRUE residual passes.
    #
    # The outer 026A/026B coupled solver independently reconstructs
    # the RESTORED FULL Newton residual after Schur back-substitution.
    #
    # Thus two separate gates remain:
    #
    #     SCHUR_TRUE_RELRES <= 0.05
    #
    # and
    #
    #     RESTORED_FULL_RELRES <= configured 026B threshold.
    #
    # If the preconditioned correction ceases to improve the true
    # residual, one bounded unpreconditioned correction is tried as
    # an independent numerical control.
    #
    # NO PHYSICS IS CHANGED:
    # action, field equations, topology, DEC, payload observable,
    # force sign convention, stationarity thresholds and physical
    # parameters are untouched.
    # ---------------------------------------------------------------

    _026b_r4_parent_sha256 = "ca0f0d4a29d5857cfc443a12f32536f41441f1de5a85b30ce9ce323af261178c"

    _026b_r4_original_minres = (
        r.minres_compat
    )

    _026b_r4_true_target = (
        5.0e-2
    )

    _026b_r4_primary_rtol = (
        2.0e-3
    )

    _026b_r4_refine_rtol = (
        1.0e-3
    )

    _026b_r4_maxiter = 96

    _026b_r4_max_refinements = 3


    def _026b_r4_apply(
        A,
        vector,
    ):
        value = A.matvec(
            vector
        )

        return np.asarray(
            value,
            dtype=float,
        ).reshape(-1)


    def _026b_r4_relres(
        A,
        b,
        x,
    ):
        residual = (
            b
            - _026b_r4_apply(
                A,
                x,
            )
        )

        bnorm = max(
            float(
                np.linalg.norm(
                    b
                )
            ),
            1.0e-300,
        )

        rel = float(
            np.linalg.norm(
                residual
            )
            / bnorm
        )

        return (
            rel,
            residual,
        )


    def _026b_r4_refined_minres(
        A,
        b,
        M,
        rtol,
        maxiter,
        callback,
    ):
        b = np.asarray(
            b,
            dtype=float,
        ).reshape(-1)

        requested_rtol = float(
            rtol
        )

        use_rtol = min(
            requested_rtol,
            _026b_r4_primary_rtol,
        )

        use_maxiter = max(
            int(
                maxiter
            ),
            _026b_r4_maxiter,
        )

        x, info = (
            _026b_r4_original_minres(
                A,
                b,
                M,
                use_rtol,
                use_maxiter,
                callback,
            )
        )

        x = np.asarray(
            x,
            dtype=float,
        ).reshape(-1)

        if not np.all(
            np.isfinite(
                x
            )
        ):
            print(
                "026B_R4_SCHUR_NONFINITE_PRIMARY=YES",
                flush=True,
            )

            return (
                x,
                97,
            )

        rel, residual = (
            _026b_r4_relres(
                A,
                b,
                x,
            )
        )

        print(
            "026B_R4_SCHUR_TRUE_RELRES "
            "ROUND=0 "
            f"RELRES={rel:.15e} "
            f"MINRES_INFO={info} "
            f"REQUESTED_RTOL={requested_rtol:.15e} "
            f"USED_RTOL={use_rtol:.15e} "
            f"MAXITER={use_maxiter} "
            "PRECONDITIONER="
            + (
                "YES"
                if M is not None
                else "NO"
            ),
            flush=True,
        )

        best_x = x
        best_rel = rel
        best_residual = residual

        for refinement in range(
            1,
            _026b_r4_max_refinements
            + 1,
        ):

            if (
                best_rel
                <=
                _026b_r4_true_target
            ):
                break

            prior_rel = best_rel

            correction, corr_info = (
                _026b_r4_original_minres(
                    A,
                    best_residual,
                    M,
                    min(
                        use_rtol,
                        _026b_r4_refine_rtol,
                    ),
                    use_maxiter,
                    callback,
                )
            )

            correction = np.asarray(
                correction,
                dtype=float,
            ).reshape(-1)

            if not np.all(
                np.isfinite(
                    correction
                )
            ):
                print(
                    "026B_R4_REFINEMENT_NONFINITE "
                    f"ROUND={refinement} "
                    "PRECONDITIONER=YES",
                    flush=True,
                )

                break

            candidate = (
                best_x
                + correction
            )

            candidate_rel, candidate_residual = (
                _026b_r4_relres(
                    A,
                    b,
                    candidate,
                )
            )

            print(
                "026B_R4_SCHUR_REFINEMENT "
                f"ROUND={refinement} "
                f"RELRES={candidate_rel:.15e} "
                f"PREVIOUS={prior_rel:.15e} "
                f"CORRECTION_INFO={corr_info} "
                "PRECONDITIONER="
                + (
                    "YES"
                    if M is not None
                    else "NO"
                ),
                flush=True,
            )

            if candidate_rel < best_rel:

                best_x = candidate
                best_rel = candidate_rel
                best_residual = (
                    candidate_residual
                )

            # -------------------------------------------------------
            # If the preconditioned correction did not reduce the
            # true residual by at least 15%, run ONE independent
            # unpreconditioned correction from the same best point.
            #
            # This is not a second physical solver.  It is a bounded
            # numerical control on whether the L-BFGS preconditioner
            # is responsible for residual stagnation.
            # -------------------------------------------------------

            weak_improvement = bool(
                M is not None
                and best_rel
                >
                0.85
                * prior_rel
                and best_rel
                >
                _026b_r4_true_target
            )

            if weak_improvement:

                control_rhs = (
                    best_residual
                )

                control, control_info = (
                    _026b_r4_original_minres(
                        A,
                        control_rhs,
                        None,
                        min(
                            use_rtol,
                            5.0e-4,
                        ),
                        max(
                            use_maxiter,
                            128,
                        ),
                        callback,
                    )
                )

                control = np.asarray(
                    control,
                    dtype=float,
                ).reshape(-1)

                if np.all(
                    np.isfinite(
                        control
                    )
                ):

                    control_candidate = (
                        best_x
                        + control
                    )

                    (
                        control_rel,
                        control_residual,
                    ) = _026b_r4_relres(
                        A,
                        b,
                        control_candidate,
                    )

                    print(
                        "026B_R4_SCHUR_CONTROL "
                        f"ROUND={refinement} "
                        f"RELRES={control_rel:.15e} "
                        f"PREVIOUS={best_rel:.15e} "
                        f"CONTROL_INFO={control_info} "
                        "PRECONDITIONER=NO",
                        flush=True,
                    )

                    if control_rel < best_rel:

                        best_x = (
                            control_candidate
                        )

                        best_rel = (
                            control_rel
                        )

                        best_residual = (
                            control_residual
                        )

            # Stop spending HVPs on a particular damping value if
            # the true residual is essentially not moving.
            if (
                best_rel
                >=
                0.98
                * prior_rel
            ):

                print(
                    "026B_R4_REFINEMENT_STAGNATION "
                    f"ROUND={refinement} "
                    f"RELRES={best_rel:.15e}",
                    flush=True,
                )

                break

        certified = bool(
            math.isfinite(
                best_rel
            )
            and best_rel
            <=
            _026b_r4_true_target
        )

        print(
            "026B_R4_SCHUR_TRUE_RESIDUAL_CERTIFICATE "
            f"RELRES={best_rel:.15e} "
            f"TARGET={_026b_r4_true_target:.15e} "
            "PASS="
            + (
                "YES"
                if certified
                else "NO"
            ),
            flush=True,
        )

        return (
            best_x,
            0
            if certified
            else 98,
        )


    r.minres_compat = (
        _026b_r4_refined_minres
    )

    print(
        "026B_R4_PARENT_SOURCE_SHA256="
        + _026b_r4_parent_sha256,
        flush=True,
    )

    print(
        "026B_R4_TRUE_RESIDUAL_REFINEMENT=ENABLED",
        flush=True,
    )

    print(
        "026B_R4_SCHUR_TRUE_RELRES_TARGET="
        f"{_026b_r4_true_target:.15e}",
        flush=True,
    )

    print(
        "026B_R4_PRIMARY_MINRES_RTOL="
        f"{_026b_r4_primary_rtol:.15e}",
        flush=True,
    )

    print(
        "026B_R4_REFINEMENT_MINRES_RTOL="
        f"{_026b_r4_refine_rtol:.15e}",
        flush=True,
    )

    print(
        "026B_R4_MINRES_MAXITER="
        f"{_026b_r4_maxiter}",
        flush=True,
    )

    print(
        "026B_R4_MAX_REFINEMENTS="
        f"{_026b_r4_max_refinements}",
        flush=True,
    )

    print(
        "026B_R4_INDEPENDENT_FULL_RELRES_GATE=PRESERVED",
        flush=True,
    )

    return {
        "a26":
            a26,

        "r5":
            r5,

        "r4":
            r4,

        "r3":
            r3,

        "r2":
            r2,

        "r":
            r,

        "qs2":
            qs2,

        "c2a":
            c2a,

        "c2ar":
            c2ar,

        "c2aqs":
            c2aqs,

        "cr2":
            cr2,

        "cr3":
            cr3,

        "cr4r":
            cr4r,

        "cr3r":
            cr3r,
    }


def load_n73_field():
    """Load the authoritative strict N=73 physical field."""

    with np.load(
        N73_FIELD,
        allow_pickle=False,
    ) as d:

        phi = np.asarray(
            d["phi"],
            dtype=float,
        )

        axis = np.asarray(
            d["axis"],
            dtype=float,
        )

        dx = float(
            d["dx"]
        )

        b = int(
            d["B"]
        )

        eta = float(
            d["eta"]
        )

        mass = float(
            d["mass"]
        )

        source = str(
            d["source"]
        )

    if (
        phi.shape
        != (
            N73,
            N73,
            N73,
            4,
        )
    ):
        raise RuntimeError(
            f"Unexpected N73 field shape {phi.shape}"
        )

    if (
        b != B
        or abs(
            eta - ETA
        )
        > 1e-14
        or abs(
            mass - MASS
        )
        > 1e-14
    ):
        raise RuntimeError(
            "N73 physical metadata mismatch"
        )

    if (
        source
        !=
        "026A_TRUE_ANTIGRAVITY_STRICT_N73"
    ):
        raise RuntimeError(
            f"Unexpected N73 source tag {source}"
        )

    normerr = float(
        np.max(
            np.abs(
                np.linalg.norm(
                    phi,
                    axis=-1,
                )
                - 1.0
            )
        )
    )

    if normerr > 5e-10:
        raise RuntimeError(
            f"N73 S3 norm failure {normerr}"
        )

    print(
        "026B_N73_FIELD_NORM_MAXERR="
        f"{normerr:.15e}",
        flush=True,
    )

    return (
        phi,
        axis,
        dx,
    )


def save_checkpoint(
    state,
    E: float,
    rms: float,
    gmax: float,
):
    """Persist the N81 field without enormous optimizer-history tensors."""

    DATA.mkdir(
        parents=True,
        exist_ok=True,
    )

    np.savez(
        CHECKPOINT,
        phi=state.phi,
        axis=state.axis,
        dx=np.array(
            state.dx
        ),
        B=np.array(
            B
        ),
        eta=np.array(
            ETA
        ),
        mass=np.array(
            MASS
        ),
        accepted_total=np.array(
            state.accepted_total
        ),
        energy=np.array(
            E
        ),
        grad_rms=np.array(
            rms
        ),
        grad_max=np.array(
            gmax
        ),
        source=np.array(
            "026B_TRUE_ANTIGRAVITY_N81_AUGMENTED_MINRES"
        ),
    )

    print(
        "026B_CHECKPOINT="
        f"{CHECKPOINT.relative_to(ROOT)}",
        flush=True,
    )


def load_or_prolongate_n81(
    cr3,
    cr3r,
    cr4r,
    phi73,
    axis73,
):
    """Resume N81 or prolongate the strict N73 solution onto the finer grid."""

    if CHECKPOINT.is_file():

        with np.load(
            CHECKPOINT,
            allow_pickle=False,
        ) as d:

            phi = np.asarray(
                d["phi"],
                dtype=float,
            )

            axis = np.asarray(
                d["axis"],
                dtype=float,
            )

            dx = float(
                d["dx"]
            )

            accepted = int(
                d["accepted_total"]
            )

            b = int(
                d["B"]
            )

            eta = float(
                d["eta"]
            )

            mass = float(
                d["mass"]
            )

        source = (
            "026B_N81_CHECKPOINT"
        )

        if (
            b != B
            or abs(
                eta - ETA
            )
            > 1e-14
            or abs(
                mass - MASS
            )
            > 1e-14
        ):
            raise RuntimeError(
                "026B checkpoint physical metadata mismatch"
            )

    else:

        phi, axis, dx = (
            cr3r.interpolate_field(
                phi73,
                axis73,
                N81,
                cr3,
            )
        )

        accepted = 0

        source = (
            "LINEAR_PROLONGATION_FROM_GREEN_026A_N73"
        )

    if (
        phi.shape
        != (
            N81,
            N81,
            N81,
            4,
        )
    ):
        raise RuntimeError(
            f"Unexpected N81 shape {phi.shape}"
        )

    normerr = float(
        np.max(
            np.abs(
                np.linalg.norm(
                    phi,
                    axis=-1,
                )
                - 1.0
            )
        )
    )

    if normerr > 5e-10:
        raise RuntimeError(
            f"N81 S3 norm violation {normerr}"
        )

    state = cr4r.State(
        phi=phi,
        axis=axis,
        dx=dx,
        accepted_total=accepted,
    )

    return (
        state,
        source,
        normerr,
    )


def continuous_force_gate_n81(
    c2aqs,
    aqr,
    cr3,
    phi,
    axis,
    dx,
):
    """Run the validated cubic/quintic continuous-field force certificate."""

    c2aq = c2aqs.load_module(
        "026b_c2aq",
        aqr.C2AQ_SOURCE,
    )

    payload_center = float(
        c2aq.PAYLOAD_CENTER
    )

    payload_radius = float(
        c2aq.PAYLOAD_RADIUS
    )

    direction = np.asarray(
        c2aq.KNOWN_WORST_DIRECTION,
        dtype=float,
    )

    direction /= np.linalg.norm(
        direction
    )

    center = (
        payload_center
        * direction
    )

    print(
        "\n=== 026B N81 CONTINUOUS-FIELD FORCE PRECOMPUTE ===",
        flush=True,
    )

    print(
        f"N81_FORCE_DX={dx:.15e}",
        flush=True,
    )

    print(
        "N81_PAYLOAD_RADIUS_OVER_DX="
        f"{payload_radius/dx:.15e}",
        flush=True,
    )

    print(
        "N81_FORCE_DIRECTION="
        + ",".join(
            f"{x:.15e}"
            for x in direction
        ),
        flush=True,
    )

    lowers = c2aqs.cell_lowers(
        axis
    )

    dmin = c2aqs.min_distance_to_cells(
        lowers,
        dx,
        center,
    )

    near_radius = (
        c2aqs.NEAR_RADIUS_DX
        * dx
    )

    near_mask = (
        dmin
        < near_radius
    )

    near_lowers = lowers[
        near_mask
    ]

    far_lowers = lowers[
        ~near_mask
    ]

    print(
        f"N81_TOTAL_FIELD_CELLS={len(lowers)}",
        flush=True,
    )

    print(
        f"N81_NEAR_FIELD_CELLS={len(near_lowers)}",
        flush=True,
    )

    offsets = {
        "far2":
            c2aqs.composite_gauss_offsets(
                dx,
                2,
                1,
            ),

        "far3":
            c2aqs.composite_gauss_offsets(
                dx,
                3,
                1,
            ),

        "far4":
            c2aqs.composite_gauss_offsets(
                dx,
                4,
                1,
            ),

        "near_coarse":
            c2aqs.composite_gauss_offsets(
                dx,
                c2aqs.NEAR_GAUSS_ORDER,
                c2aqs.NEAR_COARSE_SUBDIV,
            ),

        "near_fine":
            c2aqs.composite_gauss_offsets(
                dx,
                c2aqs.NEAR_GAUSS_ORDER,
                c2aqs.NEAR_FINE_SUBDIV,
            ),
    }

    const_err = (
        c2aqs.constant_source_validation(
            aqr,
            axis,
            dx,
            far_lowers,
            near_lowers,
            center,
            direction,
            payload_radius,
            *offsets[
                "far3"
            ],
            *offsets[
                "near_fine"
            ],
        )
    )

    if (
        const_err
        >
        c2aqs.FORCE_CONST_VALIDATION_REL_TOL
    ):
        raise RuntimeError(
            "N81 constant-source cubature validation failed"
        )

    print(
        "\n=== 026B N81 CUBIC / QUINTIC CONTINUOUS FIELDS ===",
        flush=True,
    )

    interps = {}

    for method in (
        "cubic",
        "quintic",
    ):

        print(
            f"N81_BUILDING_{method.upper()}_TENSOR_SPLINE=START",
            flush=True,
        )

        interp = (
            c2aqs.build_interpolator(
                axis,
                phi,
                method,
            )
        )

        interps[
            method
        ] = interp

        print(
            f"N81_BUILDING_{method.upper()}_TENSOR_SPLINE=DONE",
            flush=True,
        )

        nodal = (
            c2aqs.nodal_reproduction_check(
                interp,
                phi,
                axis,
                method,
            )
        )

        deriv = (
            c2aqs.finite_difference_derivative_check(
                interp,
                axis,
                dx,
                method,
            )
        )

        if (
            nodal
            > c2aqs.NODAL_REPRO_ABS_TOL
            or deriv
            > c2aqs.DERIVATIVE_REL_TOL
        ):
            raise RuntimeError(
                f"N81 {method} continuous-field validation failed"
            )

        c2aqs.central_source_diagnostic(
            cr3,
            phi,
            axis,
            dx,
            interp,
            method,
        )

    print(
        "\n=== 026B N81 HEAVY q=2/3/4 CONTINUOUS FORCE ===",
        flush=True,
    )

    cubic = c2aqs.run_method(
        "cubic",
        interps[
            "cubic"
        ],
        far_lowers,
        near_lowers,
        offsets,
        center,
        direction,
        payload_radius,
        use_q4=True,
    )

    quintic = c2aqs.run_method(
        "quintic",
        interps[
            "quintic"
        ],
        far_lowers,
        near_lowers,
        offsets,
        center,
        direction,
        payload_radius,
        use_q4=True,
    )

    spread = abs(
        cubic.best.force
        - quintic.best.force
    )

    error_bound = max(
        cubic.internal_error,
        quintic.internal_error,
        spread,
    )

    margin = min(
        abs(
            cubic.best.force
        ),
        abs(
            quintic.best.force
        ),
    )

    same_sign = bool(
        np.sign(
            cubic.best.force
        )
        ==
        np.sign(
            quintic.best.force
        )
        and cubic.best.force
        != 0.0
    )

    certified = bool(
        same_sign
        and margin
        >
        c2aqs.SIGN_SAFETY_FACTOR
        * error_bound
    )

    if (
        certified
        and cubic.best.force
        > 0.0
    ):
        sign = "OUTWARD"

    elif (
        certified
        and cubic.best.force
        < 0.0
    ):
        sign = "INWARD"

    else:
        sign = "UNRESOLVED"

    l1 = max(
        cubic.best.l1,
        quintic.best.l1,
    )

    mean_abs = (
        0.5
        * (
            abs(
                cubic.best.force
            )
            + abs(
                quintic.best.force
            )
        )
    )

    cancellation = (
        l1
        / max(
            mean_abs,
            1e-300,
        )
    )

    print(
        "\n=== 026B N81 CONTINUOUS FORCE CERTIFICATE ===",
        flush=True,
    )

    print(
        "N81_CUBIC_CONTINUOUS_BEST_FORCE="
        f"{cubic.best.force:.15e}",
        flush=True,
    )

    print(
        "N81_QUINTIC_CONTINUOUS_BEST_FORCE="
        f"{quintic.best.force:.15e}",
        flush=True,
    )

    print(
        "N81_CONTINUOUS_REPRESENTATION_SPREAD="
        f"{spread:.15e}",
        flush=True,
    )

    print(
        "N81_CONTINUOUS_FORCE_ERROR_BOUND="
        f"{error_bound:.15e}",
        flush=True,
    )

    print(
        "N81_CONTINUOUS_FORCE_SIGN_MARGIN="
        f"{margin:.15e}",
        flush=True,
    )

    print(
        "N81_CUBIC_QUINTIC_SAME_SIGN="
        + (
            "YES"
            if same_sign
            else "NO"
        ),
        flush=True,
    )

    print(
        "N81_CONTINUOUS_FORCE_SIGN_CERTIFIED="
        + (
            "YES"
            if certified
            else "NO"
        ),
        flush=True,
    )

    print(
        f"N81_CONTINUOUS_FORCE_SIGN={sign}",
        flush=True,
    )

    print(
        "N81_CONTINUOUS_FORCE_CANCELLATION_FACTOR="
        f"{cancellation:.15e}",
        flush=True,
    )

    return {
        "cubic":
            float(
                cubic.best.force
            ),

        "quintic":
            float(
                quintic.best.force
            ),

        "spread":
            float(
                spread
            ),

        "error":
            float(
                error_bound
            ),

        "margin":
            float(
                margin
            ),

        "same_sign":
            same_sign,

        "certified":
            certified,

        "sign":
            sign,

        "cancellation":
            float(
                cancellation
            ),

        "cubic_internal_error":
            float(
                cubic.internal_error
            ),

        "quintic_internal_error":
            float(
                quintic.internal_error
            ),
    }


def main() -> None:
    """Execute the N=81 true-antigravity convergence gate."""

    print(
        "=== 026B TRUE ANTIGRAVITY "
        "B7 N81 FORCE CONVERGENCE GATE ===",
        flush=True,
    )

    summary73 = audit_inputs()

    mods = load_modules()

    a26 = mods[
        "a26"
    ]

    r5 = mods[
        "r5"
    ]

    r4 = mods[
        "r4"
    ]

    r = mods[
        "r"
    ]

    qs2 = mods[
        "qs2"
    ]

    c2a = mods[
        "c2a"
    ]

    c2aqs = mods[
        "c2aqs"
    ]

    cr2 = mods[
        "cr2"
    ]

    cr3 = mods[
        "cr3"
    ]

    cr4r = mods[
        "cr4r"
    ]

    cr3r = mods[
        "cr3r"
    ]

    phi73, axis73, dx73 = (
        load_n73_field()
    )

    diag73 = (
        cr3.continuum_local_diagnostics(
            phi73,
            axis73,
            dx73,
            cr2,
        )
    )

    E73, _e2, _e4, _e0, g73, rms73, gmax73, station73 = (
        r.strict_stationarity(
            cr3,
            phi73,
            dx73,
        )
    )

    if not station73:
        raise RuntimeError(
            "Authoritative 026A N73 field no longer passes strict stationarity"
        )

    print(
        "\n=== 026B N73 REFERENCE AUDIT ===",
        flush=True,
    )

    print(
        f"N73_REFERENCE_ENERGY={E73:.15e}",
        flush=True,
    )

    print(
        "N73_REFERENCE_CONTINUUM_ENERGY="
        f"{diag73.energy_continuum:.15e}",
        flush=True,
    )

    print(
        "N73_REFERENCE_MIN_ACTIVE_FRACTION="
        f"{diag73.min_active_fraction:.15e}",
        flush=True,
    )

    print(
        f"N73_REFERENCE_TOPOLOGY4={diag73.topology4:.15e}",
        flush=True,
    )

    state, start_source, normerr = (
        load_or_prolongate_n81(
            cr3,
            cr3r,
            cr4r,
            phi73,
            axis73,
        )
    )

    (
        E,
        _e2,
        _e4,
        _e0,
        g,
        rms,
        gmax,
        station,
    ) = r.strict_stationarity(
        cr3,
        state.phi,
        state.dx,
    )

    deg_ok, degrees = (
        cr3.geometric_guard(
            state.phi,
            cr2,
            True,
        )
    )

    if not deg_ok:
        raise RuntimeError(
            "Initial N81 field lost B=7"
        )

    print(
        "\n=== 026B N81 START ===",
        flush=True,
    )

    print(
        f"026B_N81_START_SOURCE={start_source}",
        flush=True,
    )

    print(
        f"026B_N81_START_NORM_MAXERR={normerr:.15e}",
        flush=True,
    )

    print(
        f"026B_N81_DX={state.dx:.15e}",
        flush=True,
    )

    print(
        f"026B_N81_START_ENERGY={E:.15e}",
        flush=True,
    )

    print(
        f"026B_N81_START_GRAD_RMS={rms:.15e}",
        flush=True,
    )

    print(
        f"026B_N81_START_GRAD_MAX={gmax:.15e}",
        flush=True,
    )

    print(
        f"026B_N81_START_MERIT={merit(rms,gmax):.15e}",
        flush=True,
    )

    print(
        "026B_N81_START_DEGREES="
        + ",".join(
            str(x)
            for x in degrees
        ),
        flush=True,
    )

    cr4r.residual_localization(
        cr3,
        state,
        g,
    )

    r5.print_metrics(
        "026B_N81_START",
        r5.residual_metrics(
            c2a,
            state.phi,
            g,
        ),
    )

    history = []
    outer_reports = []
    accepted = 0

    for outer in range(
        1,
        MAX_OUTER + 1,
    ):

        if station:
            break

        print(
            f"\n=== 026B N81 DEFECT-CORRECTION OUTER {outer} ===",
            flush=True,
        )

        old_phi = (
            state.phi.copy()
        )

        old_g = (
            g.copy()
        )

        old_merit = merit(
            rms,
            gmax,
        )

        pack, diagnostics = (
            a26.coupled_solve(
                r4,
                r5,
                r,
                qs2,
                c2a,
                cr2,
                cr3,
                state,
                history,
                E,
                g,
                rms,
                gmax,
                outer == 1,
            )
        )

        diagnostics[
            "outer"
        ] = outer

        if pack is None:

            diagnostics[
                "accepted"
            ] = False

            outer_reports.append(
                diagnostics
            )

            print(
                "026B_N81_COUPLED_DIRECTION=UNRESOLVED",
                flush=True,
            )

            break

        history = (
            r.transport_history_after_step(
                cr3,
                cr4r,
                old_phi,
                pack[
                    "cand"
                ],
                pack[
                    "direction"
                ],
                pack[
                    "alpha"
                ],
                old_g,
                pack[
                    "g"
                ],
                history,
            )
        )

        state.phi = pack[
            "cand"
        ]

        state.accepted_total += 1

        E = pack[
            "E"
        ]

        g = pack[
            "g"
        ]

        rms = pack[
            "rms"
        ]

        gmax = pack[
            "gmax"
        ]

        station = pack[
            "station"
        ]

        accepted += 1

        new_merit = merit(
            rms,
            gmax,
        )

        t4_now = cr3.topology4(
            state.phi,
            state.dx,
        )

        deg_ok_now, degrees_now = (
            cr3.geometric_guard(
                state.phi,
                cr2,
                True,
            )
        )

        angle_now = (
            cr3.max_neighbor_angle(
                state.phi
            )
        )

        if not deg_ok_now:
            raise RuntimeError(
                "Accepted N81 Newton correction lost B=7"
            )

        diagnostics.update(
            {
                "accepted":
                    True,

                "alpha":
                    pack[
                        "alpha"
                    ],

                "end_merit":
                    new_merit,

                "topology4":
                    t4_now,

                "angle":
                    angle_now,
            }
        )

        outer_reports.append(
            diagnostics
        )

        print(
            "026B_N81_STEP_ACCEPTED=YES "
            f"ALPHA={pack['alpha']:.15e} "
            "MERIT_REDUCTION="
            f"{old_merit/max(new_merit,1e-300):.15e} "
            f"GRAD_RMS={rms:.15e} "
            f"GRAD_MAX={gmax:.15e} "
            f"TOPOLOGY4={t4_now:.15e} "
            f"ANGLE={angle_now:.15e}",
            flush=True,
        )

        save_checkpoint(
            state,
            E,
            rms,
            gmax,
        )

        if (
            old_merit
            / max(
                new_merit,
                1e-300,
            )
            < 1.002
            and not station
        ):
            print(
                "026B_N81_STAGNATION_STOP=YES",
                flush=True,
            )

            break

    print(
        "\n=== 026B N81 FINAL STATIONARITY AUDIT ===",
        flush=True,
    )

    t4 = cr3.topology4(
        state.phi,
        state.dx,
    )

    deg_ok, degrees = (
        cr3.geometric_guard(
            state.phi,
            cr2,
            True,
        )
    )

    angle = cr3.max_neighbor_angle(
        state.phi
    )

    top_rel = (
        abs(
            abs(
                t4
            )
            - B
        )
        / B
    )

    print(
        f"026B_N81_ACCEPTED_THIS_RUN={accepted}",
        flush=True,
    )

    print(
        f"026B_N81_FINAL_ENERGY={E:.15e}",
        flush=True,
    )

    print(
        f"026B_N81_FINAL_GRAD_RMS={rms:.15e}",
        flush=True,
    )

    print(
        f"026B_N81_FINAL_GRAD_MAX={gmax:.15e}",
        flush=True,
    )

    print(
        f"026B_N81_FINAL_MERIT={merit(rms,gmax):.15e}",
        flush=True,
    )

    print(
        "026B_STRICT_N81_STATIONARITY="
        + (
            "PASS"
            if station
            else "FAIL"
        ),
        flush=True,
    )

    print(
        f"026B_N81_FINAL_TOPOLOGY4={t4:.15e}",
        flush=True,
    )

    print(
        "026B_N81_FINAL_DEGREES="
        + ",".join(
            str(x)
            for x in degrees
        ),
        flush=True,
    )

    print(
        f"026B_N81_MAX_NEIGHBOR_ANGLE={angle:.15e}",
        flush=True,
    )

    print(
        f"026B_N81_TOPOLOGY_RELERR={top_rel:.15e}",
        flush=True,
    )

    physical_gate = False
    local_resolution_gate = False

    diag81 = None

    local_compare = None

    force81 = None

    force_compare = None

    if station:

        diag81 = (
            cr3.continuum_local_diagnostics(
                state.phi,
                state.axis,
                state.dx,
                cr2,
            )
        )

        physical_gate = bool(
            deg_ok
            and top_rel
            <= MAX_TOPOLOGY_RELERR
            and angle
            <= MAX_NEIGHBOR_ANGLE
            and diag81.active_total
            > 0.0
            and diag81.min_active_fraction
            <= -MIN_NEGATIVE_ACTIVE_FRACTION
            and diag81.min_dec_scaled_margin
            >= MIN_DEC_SCALED_MARGIN
            and diag81.max_active_trace_scaled
            <= MAX_ACTIVE_TRACE_SCALED
        )

        print(
            "\n=== 026B N81 PHYSICAL FIELD AUDIT ===",
            flush=True,
        )

        print(
            "026B_N81_CONTINUUM_ENERGY="
            f"{diag81.energy_continuum:.15e}",
            flush=True,
        )

        print(
            "026B_N81_ACTIVE_TOTAL="
            f"{diag81.active_total:.15e}",
            flush=True,
        )

        print(
            "026B_N81_MIN_ACTIVE_FRACTION="
            f"{diag81.min_active_fraction:.15e}",
            flush=True,
        )

        print(
            "026B_N81_MIN_DEC_SCALED_MARGIN="
            f"{diag81.min_dec_scaled_margin:.15e}",
            flush=True,
        )

        print(
            "026B_N81_MAX_ACTIVE_TRACE_SCALED="
            f"{diag81.max_active_trace_scaled:.15e}",
            flush=True,
        )

        print(
            "026B_N81_PHYSICAL_FIELD_GATE="
            + (
                "PASS"
                if physical_gate
                else "FAIL"
            ),
            flush=True,
        )

        energy_rel = relchange(
            diag73.energy_continuum,
            diag81.energy_continuum,
        )

        active_fraction_change = abs(
            float(
                diag81.min_active_fraction
            )
            - float(
                diag73.min_active_fraction
            )
        )

        topology_change = abs(
            float(
                diag81.topology4
            )
            - float(
                diag73.topology4
            )
        )

        local_resolution_gate = bool(
            physical_gate
            and energy_rel
            <= MAX_PAIR_ENERGY_RELCHANGE
            and active_fraction_change
            <= MAX_PAIR_ACTIVE_FRACTION_ABSCHANGE
            and topology_change
            <= MAX_PAIR_TOPOLOGY_ABSCHANGE
        )

        local_compare = {
            "energy_relchange":
                energy_rel,

            "min_active_fraction_abschange":
                active_fraction_change,

            "topology4_abschange":
                topology_change,

            "pass":
                local_resolution_gate,
        }

        print(
            "\n=== 026B N73 -> N81 LOCAL RESOLUTION ===",
            flush=True,
        )

        print(
            "N73_N81_CONTINUUM_ENERGY_RELCHANGE="
            f"{energy_rel:.15e}",
            flush=True,
        )

        print(
            "N73_N81_MIN_ACTIVE_FRACTION_ABSCHANGE="
            f"{active_fraction_change:.15e}",
            flush=True,
        )

        print(
            "N73_N81_TOPOLOGY4_ABSCHANGE="
            f"{topology_change:.15e}",
            flush=True,
        )

        print(
            "N73_N81_LOCAL_FIELD_CONVERGENCE="
            + (
                "PASS"
                if local_resolution_gate
                else "FAIL"
            ),
            flush=True,
        )

        if physical_gate:

            np.savez(
                FINAL,
                phi=state.phi,
                axis=state.axis,
                dx=np.array(
                    state.dx
                ),
                B=np.array(
                    B
                ),
                eta=np.array(
                    ETA
                ),
                mass=np.array(
                    MASS
                ),
                energy=np.array(
                    E
                ),
                grad_rms=np.array(
                    rms
                ),
                grad_max=np.array(
                    gmax
                ),
                topology4=np.array(
                    t4
                ),
                active_total=np.array(
                    diag81.active_total
                ),
                min_active_fraction=np.array(
                    diag81.min_active_fraction
                ),
                min_dec_scaled_margin=np.array(
                    diag81.min_dec_scaled_margin
                ),
                max_active_trace_scaled=np.array(
                    diag81.max_active_trace_scaled
                ),
                source=np.array(
                    "026B_TRUE_ANTIGRAVITY_STRICT_N81"
                ),
            )

            print(
                f"026B_STRICT_N81_FIELD={FINAL.relative_to(ROOT)}",
                flush=True,
            )

    if (
        station
        and physical_gate
        and local_resolution_gate
    ):

        print(
            "\n=== 026B FORCE KERNEL AUDIT ===",
            flush=True,
        )

        aqr = c2aqs.load_module(
            "026b_aqr",
            c2aqs.AQR_SOURCE,
        )

        aqr.validate_analytic_formulae()

        print(
            "026B_ANALYTIC_FORCE_KERNEL_AUDIT=PASS",
            flush=True,
        )

        force81 = (
            continuous_force_gate_n81(
                c2aqs,
                aqr,
                cr3,
                state.phi,
                state.axis,
                state.dx,
            )
        )

        n65ref = (
            qs2.load_n65_force_reference()
        )

        n73force = summary73[
            "force"
        ]

        mean65 = (
            0.5
            * (
                float(
                    n65ref[
                        "cubic"
                    ]
                )
                + float(
                    n65ref[
                        "quintic"
                    ]
                )
            )
        )

        mean73 = (
            0.5
            * (
                float(
                    n73force[
                        "cubic"
                    ]
                )
                + float(
                    n73force[
                        "quintic"
                    ]
                )
            )
        )

        mean81 = (
            0.5
            * (
                float(
                    force81[
                        "cubic"
                    ]
                )
                + float(
                    force81[
                        "quintic"
                    ]
                )
            )
        )

        change65_73 = abs(
            mean73
            - mean65
        )

        change73_81 = abs(
            mean81
            - mean73
        )

        rel73_81 = (
            change73_81
            / max(
                abs(
                    mean73
                ),
                abs(
                    mean81
                ),
                1e-300,
            )
        )

        delta_shrink_ratio = (
            change73_81
            / max(
                change65_73,
                1e-300,
            )
        )

        spread_ratio = (
            float(
                force81[
                    "spread"
                ]
            )
            / max(
                float(
                    n73force[
                        "spread"
                    ]
                ),
                1e-300,
            )
        )

        convergence_prefilter = bool(
            force81[
                "certified"
            ]
            and force81[
                "sign"
            ]
            == "OUTWARD"
            and rel73_81
            <= MAX_FORCE_MEAN_RELCHANGE
            and spread_ratio
            <= MAX_REPRESENTATION_SPREAD_RATIO
        )

        force_compare = {
            "n65_mean":
                mean65,

            "n73_mean":
                mean73,

            "n81_mean":
                mean81,

            "n65_to_n73_abschange":
                change65_73,

            "n73_to_n81_abschange":
                change73_81,

            "n73_to_n81_mean_relchange":
                rel73_81,

            "delta_shrink_ratio":
                delta_shrink_ratio,

            "n81_over_n73_representation_spread_ratio":
                spread_ratio,

            "strong_convergence_prefilter":
                convergence_prefilter,
        }

        print(
            "\n=== 026B THREE-RESOLUTION FORCE TREND ===",
            flush=True,
        )

        print(
            f"N65_CONTINUOUS_FORCE_MEAN={mean65:.15e}",
            flush=True,
        )

        print(
            f"N73_CONTINUOUS_FORCE_MEAN={mean73:.15e}",
            flush=True,
        )

        print(
            f"N81_CONTINUOUS_FORCE_MEAN={mean81:.15e}",
            flush=True,
        )

        print(
            "N65_N73_FORCE_ABSCHANGE="
            f"{change65_73:.15e}",
            flush=True,
        )

        print(
            "N73_N81_FORCE_ABSCHANGE="
            f"{change73_81:.15e}",
            flush=True,
        )

        print(
            "N73_N81_FORCE_MEAN_RELCHANGE="
            f"{rel73_81:.15e}",
            flush=True,
        )

        print(
            "FORCE_REFINEMENT_DELTA_SHRINK_RATIO="
            f"{delta_shrink_ratio:.15e}",
            flush=True,
        )

        print(
            "N81_OVER_N73_REPRESENTATION_SPREAD_RATIO="
            f"{spread_ratio:.15e}",
            flush=True,
        )

        print(
            "N73_N81_CONTINUOUS_FORCE_CONVERGENCE_PREFILTER="
            + (
                "PASS"
                if convergence_prefilter
                else "FAIL"
            ),
            flush=True,
        )

    else:

        convergence_prefilter = False

    if not station:

        decision = (
            "INCOMPLETE_N81_STATIONARITY"
        )

        nxt = (
            "RERUN_026B_FROM_CHECKPOINT"
        )

    elif not physical_gate:

        decision = (
            "RED_N81_PHYSICAL_FIELD_GATE"
        )

        nxt = (
            "INSPECT_N81_FIELD_BEFORE_FURTHER_REFINEMENT"
        )

    elif not local_resolution_gate:

        decision = (
            "N81_LOCAL_FIELD_RESOLUTION_NOT_CONVERGED"
        )

        nxt = (
            "026C_N89_OR_DOMAIN_DISCRETIZATION_DIAGNOSTIC"
        )

    elif force81 is None:

        decision = (
            "N81_FORCE_NOT_EVALUATED"
        )

        nxt = (
            "INSPECT_026B_FORCE_STAGE"
        )

    elif (
        force81[
            "certified"
        ]
        and force81[
            "sign"
        ]
        == "INWARD"
    ):

        decision = (
            "RED_N81_CERTIFIED_INWARD_SENTINEL"
        )

        nxt = (
            "026C_N89_SIGN_REVERSAL_CONFIRMATION"
        )

    elif not force81[
        "certified"
    ]:

        decision = (
            "N81_CONTINUOUS_FORCE_SIGN_UNRESOLVED"
        )

        nxt = (
            "026C_N89_OR_CONTINUOUS_REPRESENTATION_REFINEMENT"
        )

    elif convergence_prefilter:

        decision = (
            "GREEN_N73_N81_CONTINUOUS_OUTWARD_FORCE_CONVERGENCE_PREFILTER"
        )

        nxt = (
            "026C_DENSE_CONTINUOUS_FORCE_ROBUSTNESS_N73_N81"
        )

    else:

        decision = (
            "N81_OUTWARD_BUT_FORCE_MAGNITUDE_NOT_YET_CONVERGED"
        )

        nxt = (
            "026C_N89_CONTINUOUS_FORCE_CONVERGENCE"
        )

    result = {
        "simulation":
            "026B",

        "branch":
            "TRUE_ANTIGRAVITY",

        "field":
            {
                "B":
                    B,

                "eta":
                    ETA,

                "m":
                    MASS,

                "N":
                    N81,
            },

        "provenance":
            {
                "a26_source_sha256":
                    EXPECTED_A26_SHA256,

                "n73_field_sha256":
                    EXPECTED_N73_FIELD_SHA256,

                "n73_summary_sha256":
                    EXPECTED_N73_SUMMARY_SHA256,
            },

        "n73_reference":
            {
                "energy":
                    E73,

                "continuum_energy":
                    float(
                        diag73.energy_continuum
                    ),

                "grad_rms":
                    rms73,

                "grad_max":
                    gmax73,

                "min_active_fraction":
                    float(
                        diag73.min_active_fraction
                    ),

                "topology4":
                    float(
                        diag73.topology4
                    ),

                "force":
                    summary73[
                        "force"
                    ],
            },

        "n81":
            {
                "start_source":
                    start_source,

                "accepted_this_run":
                    accepted,

                "energy":
                    E,

                "grad_rms":
                    rms,

                "grad_max":
                    gmax,

                "stationary":
                    station,

                "topology4":
                    t4,

                "geometric_degrees":
                    list(
                        degrees
                    ),

                "max_neighbor_angle":
                    angle,

                "physical_gate":
                    physical_gate,
            },

        "outer_reports":
            outer_reports,

        "local_resolution":
            local_compare,

        "n81_force":
            force81,

        "force_convergence":
            force_compare,

        "decision":
            decision,

        "next":
            nxt,

        "full_physical_hessian":
            (
                "DEFERRED_UNTIL_DENSE_CONTINUOUS_FORCE_ROBUSTNESS"
                if convergence_prefilter
                else "DEFERRED_FORCE_CONVERGENCE_NOT_COMPLETE"
            ),

        "nonlinear_einstein_skyrme":
            "NOT_AUTHORIZED",

        "claims":
            {
                "practical_antigravity_device":
                    False,

                "new_physics_discovery":
                    False,

                "heuristic_increase_authorized":
                    False,
            },
    }

    SUMMARY.write_text(
        json.dumps(
            result,
            indent=2,
            sort_keys=True,
            default=json_default,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "\n=== 026B DECISION ===",
        flush=True,
    )

    print(
        f"026B_DECISION={decision}",
        flush=True,
    )

    print(
        f"NEXT={nxt}",
        flush=True,
    )

    print(
        "FULL_PHYSICAL_HESSIAN="
        + result[
            "full_physical_hessian"
        ],
        flush=True,
    )

    print(
        "NONLINEAR_EINSTEIN_SKYRME=NOT_AUTHORIZED",
        flush=True,
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE=NO",
        flush=True,
    )

    print(
        "NEW_PHYSICS_DISCOVERY=NO",
        flush=True,
    )

    print(
        "HEURISTIC_INCREASE_AUTHORIZED=NO",
        flush=True,
    )

    print(
        f"OUT_SUMMARY={SUMMARY}",
        flush=True,
    )

    if CHECKPOINT.is_file():

        print(
            f"OUT_CHECKPOINT={CHECKPOINT}",
            flush=True,
        )

    if FINAL.is_file():

        print(
            f"OUT_STRICT_FIELD={FINAL}",
            flush=True,
        )


if __name__ == "__main__":
    main()
