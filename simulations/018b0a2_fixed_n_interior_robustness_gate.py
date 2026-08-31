#!/usr/bin/env python3
"""Simulation 018B-0A2 — fixed-N failure classification and interior-basin gate.

PURPOSE
-------
Resolve the only scientific failure left by Simulation 018B-0A before spending
large computational effort on a new microscopic wall/junction solve or a full
global toroidal PDE.

018B-0A found a promising single-stationary-vorton + one-KLS-wall source-level
architecture, but its selected minimum-energy state sat essentially on the
upper edge of the already verified 017P EOS interval.  Exact integer locking,
worldsheet stability, family-level integer-relocked robustness, direct 017P
BVP reconstruction, and finite-payload gravity all passed.  The lone blocking
gate was same-N local continuity: only 122/243 small perturbations retained a
passing state at the same integer winding N=12553.

SCIENTIFIC QUESTION
-------------------
Is the 018B-0A fixed-N failure merely a boundary-headroom artifact of choosing
the highest-chi / minimum-energy state, or does the verified 017P EOS interval
contain no robust same-topological-sector single-vorton operating point?

This distinction is decisive:

1. If a robust interior same-N basin exists, select it robustness-first even if
   its source-level energy coefficient is modestly worse.  Then the next gate
   is microscopic revalidation of the KLS wall/junction at the new F, chi, N.

2. If no such basin exists inside the *already verified* EOS interval, reject
   the single-vorton simplification and return immediately to the validated
   two-copy 018A-8 architecture for the true global 018B toroidal field solve.

PHYSICAL MODEL
--------------
This file does not introduce a new physical model.  It imports and reuses the
verified equations, interpolated 017P EOS, integer-locking relation, KLS wall
scaling, complete source bookkeeping, finite-payload kernel, worldsheet
stability test, and direct-BVP verifier from:

    simulations/018b0a_integer_locked_eos_architecture_gate.py

The integer winding relation is

    k(chi) R(chi,F) = N,

where N is an integer topological winding.  A real device cannot continuously
change N without a phase slip, so a selected operating point should possess a
local basin at fixed N.

PRIMARY OBSERVABLES
-------------------
The decisive observables are:

- existence of a fixed-N EOS root throughout the declared 3^5 local
  perturbation cube;
- finite-payload center-of-mass outward acceleration for every surviving root;
- positive total active mass;
- kernel-leverage margin > 1;
- microscopic scale separation;
- 017P worldsheet stability;
- direct-BVP integer-lock reconstruction at the selected interior point;
- high-precision finite-payload gravity from the direct BVP stresses.

EOS DOMAIN / NO EXTRAPOLATION
-----------------------------
The search is strictly confined to the already verified 017P branch:

    0.00150 <= chi <= 0.00475.

The script MUST NOT expand this interval to rescue the architecture.

FIXED-N PERTURBATION CUBE
-------------------------
Exactly preserve the 018B-0A local-continuity test:

    F              +/-0.5 percent
    junction mu    +/-10 percent
    radial support +/-1 percent
    q              +/-0.1 percent
    ell            +/-0.1 percent

for 3^5 = 243 cases at one fixed integer N.

SEARCH POLICY
-------------
Robustness first, not minimum C first.

The script first classifies all 121 failures of the old selected point.  It
then generates integer-locked candidates near a set of *interior* target chi
values for the already-vetted 018B-0A finalist F values.  A cheap bracket
preflight rejects states whose same N cannot remain inside the verified EOS
band under the 243 perturbations.  Only bracket-surviving candidates undergo
full exact root solving and physical gravity checks.

The selected interior candidate is the lowest-C state among candidates that
pass the exact fixed-N 243/243 gate.  It then undergoes the existing 6561-case
integer-relocked deterministic family stress, 20,000-case random family stress,
direct 017P BVP integer lock, direct-BVP EOS stability reconstruction, and
high-precision direct-BVP gravity.

This is intentionally stricter than merely finding one interior root.

UNITS AND SIGN CONVENTIONS
--------------------------
Use the same natural/dimensionless normalization as 018B-0A.  Positive point
and payload accelerations mean outward.  SI 1g/1m equivalents are reported only
through the already established scaling helper.

ASSUMPTIONS / APPROXIMATION LEVEL
---------------------------------
- flat-background microscopic matter/EOS reconstruction inherited from 017P;
- linearized-GR passive-payload gravity inherited from 018A-8/018B-0A;
- stationary worldsheet source, not yet a global curved toroidal field solve;
- no payload backreaction;
- no nonlinear Einstein-matter solve;
- no full composite dynamical stability proof;
- no claim that a factor-of-two energy improvement is practical.

VALIDATION
----------
- Reconstruct the old N=12553 selected state and reproduce its fixed-N failure
  pattern before searching for a replacement.
- Use the exact existing solve_fixed_integer/root machinery rather than a new
  approximate integer-lock equation.
- Preserve the existing finite-payload kernel and physical pass criteria.
- Re-run the published-model direct 017P BVP only for the final selected state.
- Reconstruct direct-BVP characteristic speeds and m=2..40 stability.

FALSIFICATION / STOP RULE
-------------------------
If no candidate inside the established healthy EOS interval passes the exact
243/243 same-N gate plus the inherited physical/stability checks, then:

    SINGLE_VORTON_SIMPLIFICATION = REJECTED_FOR_CURRENT_VERIFIED_EOS_BAND

and the next action is:

    TRUE_018B_GLOBAL_TOROIDAL_SOLVE_USING_VALIDATED_TWO_COPY_018A8_SOURCE

Do not widen the EOS interval and do not add arbitrary sectors to save the
single-vorton simplification.

PROMOTION CONDITION
-------------------
This gate is GREEN only if the selected interior state passes:

    OLD_FAILURE_CLASSIFIED
    FIXED_N_LOCAL_CONTINUITY = 243/243
    LOCKED_WORLD_SHEET_STABILITY
    INTEGER_RELOCKED_DETERMINISTIC_STRESS
    INTEGER_RELOCKED_RANDOM_STRESS
    DIRECT_BVP_INTEGER_LOCK
    DIRECT_BVP_EOS_STABILITY
    HIGH_PRECISION_LOCKED_GRAVITY

Even GREEN does NOT promote the lower energy coefficient to validated physical
status.  The required next step remains:

    018B0B_MICROSCOPIC_REVALIDATION_AT_INTERIOR_INTEGER_LOCKED_F_CHI

because the wall and fully coupled junction must be re-solved at the new
operating point before replacing the validated 018A-8 energy ledger.

CLAIM CLASSIFICATION
--------------------
PROJECT_DERIVED_018B0A2_FIXED_N_INTERIOR_ROBUSTNESS_GATE

WHAT THIS FILE DOES NOT ESTABLISH
---------------------------------
- a new microscopic wall solution;
- a new fully coupled junction solution;
- a global toroidal field solution;
- full composite stability;
- nonlinear Einstein-matter consistency;
- practical energy scaling;
- experimental accessibility;
- a practical antigravity device;
- new physics or novelty.
"""

from __future__ import annotations

from collections import Counter
import importlib.util
import itertools
import math
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "simulations" / "018b0a_integer_locked_eos_architecture_gate.py"


def load_module(name: str, path: Path):
    """Import a project simulation without invoking its main function."""

    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot import {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return module


p = load_module("ag018b0a2_parent", SOURCE)


F_LEVELS = (0.995, 1.000, 1.005)
MU_LEVELS = (0.90, 1.00, 1.10)
SUPPORT_LEVELS = (0.99, 1.00, 1.01)
INTERP_LEVELS = (0.999, 1.000, 1.001)

# Explicitly interior target states.  The top point deliberately leaves much
# more headroom than the failed chi ~= 0.00474948 state.
TARGET_CHI = (
    0.00450,
    0.00425,
    0.00400,
    0.00375,
    0.00350,
    0.00325,
    0.003125,
    0.00300,
    0.00275,
    0.00250,
    0.00225,
    0.00200,
)

# Nearest-integer target plus immediate neighbors protects against a target
# lying just across an integer boundary.
INTEGER_OFFSETS = (-1, 0, 1)

# Cheap bracket scan used only as a prefilter.  Exact survivors are always
# checked later with the parent's full brentq-based solve.
BRACKET_GRID = np.linspace(p.CHI_MIN, p.CHI_MAX, 65)

# Limit expensive family/direct-BVP verification to the best exact same-N
# survivors.  Robustness still dominates because every finalist here has
# already passed the exact 243/243 gate.
MAX_EXPENSIVE_FINALISTS = 4


def perturbation_cases():
    """Yield the exact 243 fixed-N perturbations used by 018B-0A."""

    yield from itertools.product(
        F_LEVELS,
        MU_LEVELS,
        SUPPORT_LEVELS,
        INTERP_LEVELS,
        INTERP_LEVELS,
    )


def residual_samples(
    anchors,
    nominal_locked,
    *,
    f_factor: float,
    mu_factor: float,
    support_factor: float,
    q_factor: float,
    ell_factor: float,
):
    """Sample kR-N across the verified EOS interval for failure diagnosis."""

    f_value = nominal_locked.f_value * f_factor
    n_integer = nominal_locked.n_integer

    values = []
    for chi in BRACKET_GRID:
        winding, _, _ = p.winding_continuous(
            anchors,
            f_value,
            float(chi),
            mu_factor=mu_factor,
            q_factor=q_factor,
            ell_factor=ell_factor,
            support_factor=support_factor,
        )
        values.append(float(winding - n_integer))

    return values


def sampled_bracket_exists(values) -> bool:
    """Return True when the sampled residuals contain or bracket zero."""

    last = None
    for value in values:
        if not math.isfinite(value):
            last = None
            continue
        if value == 0.0:
            return True
        if last is not None and last * value < 0.0:
            return True
        last = value
    return False


def no_root_channel(values) -> str:
    """Classify why an integer is unreachable in the verified chi interval."""

    finite = [value for value in values if math.isfinite(value)]
    if not finite:
        return "NO_FINITE_WINDING_BRANCH"

    if max(finite) < 0.0:
        return "N_ABOVE_REACHABLE_WINDING_RANGE"

    if min(finite) > 0.0:
        return "N_BELOW_REACHABLE_WINDING_RANGE"

    # The sampled range straddles zero but no adjacent bracket was found.
    # The exact parent solver samples more finely and is authoritative; this
    # label flags a nonmonotonic/discretization case rather than guessing.
    return "STRADDLES_ZERO_WITHOUT_SAMPLED_BRACKET"


def physical_failure_channels(result) -> list[str]:
    """Explain a root that exists but fails the inherited physical gate."""

    channels = []
    if result["point_outward"] <= 0.0:
        channels.append("POINT_NOT_OUTWARD")
    if result["payload_outward"] <= 0.0:
        channels.append("PAYLOAD_NOT_OUTWARD")
    if result["active_mass_per_r"] <= 0.0:
        channels.append("NONPOSITIVE_ACTIVE_MASS")
    if result["leverage_margin"] <= 1.0:
        channels.append("KERNEL_LEVERAGE_FAIL")
    if result["min_scale"] <= p.MIN_SCALE:
        channels.append("SCALE_SEPARATION_FAIL")
    if not channels:
        channels.append("TOPOLOGY_OR_INTEGER_TOLERANCE_FAIL")
    return channels


def classify_fixed_n_cube(anchors, locked, gravity):
    """Classify every fixed-N perturbation, including all no-root failures."""

    channels = Counter()
    total = 0
    root_count = 0
    physical_pass_count = 0
    min_payload = math.inf
    min_chi = math.inf
    max_chi = -math.inf

    for (
        f_factor,
        mu_factor,
        support_factor,
        q_factor,
        ell_factor,
    ) in perturbation_cases():
        total += 1

        perturbed = p.solve_same_n_perturbed(
            anchors,
            locked,
            f_factor=f_factor,
            mu_factor=mu_factor,
            support_factor=support_factor,
            q_factor=q_factor,
            ell_factor=ell_factor,
        )

        if perturbed is None:
            values = residual_samples(
                anchors,
                locked,
                f_factor=f_factor,
                mu_factor=mu_factor,
                support_factor=support_factor,
                q_factor=q_factor,
                ell_factor=ell_factor,
            )
            channels[no_root_channel(values)] += 1
            continue

        root_count += 1
        result = p.evaluate_locked(anchors, perturbed, gravity["x"])
        min_payload = min(min_payload, result["payload_outward"])
        min_chi = min(min_chi, perturbed.branch.chi)
        max_chi = max(max_chi, perturbed.branch.chi)

        if result["pass"]:
            physical_pass_count += 1
            channels["PASS"] += 1
        else:
            for channel in physical_failure_channels(result):
                channels[channel] += 1

    return {
        "total": total,
        "root_count": root_count,
        "physical_pass_count": physical_pass_count,
        "pass": physical_pass_count == total,
        "min_payload": min_payload,
        "min_chi": min_chi,
        "max_chi": max_chi,
        "channels": channels,
    }


def cheap_fixed_n_bracket_fraction(anchors, locked):
    """Cheaply prefilter candidates by sampled root existence over all 243 cases."""

    total = 0
    bracketed = 0

    for (
        f_factor,
        mu_factor,
        support_factor,
        q_factor,
        ell_factor,
    ) in perturbation_cases():
        total += 1
        values = residual_samples(
            anchors,
            locked,
            f_factor=f_factor,
            mu_factor=mu_factor,
            support_factor=support_factor,
            q_factor=q_factor,
            ell_factor=ell_factor,
        )
        if sampled_bracket_exists(values):
            bracketed += 1

    return bracketed, total


def candidate_locks(anchors):
    """Generate unique interior integer locks near target chi values."""

    seen = set()
    candidates = []

    for f_value in p.FINALIST_F:
        for chi_target in TARGET_CHI:
            winding, _, _ = p.winding_continuous(
                anchors,
                float(f_value),
                float(chi_target),
            )
            if not math.isfinite(winding):
                continue

            center_n = int(round(winding))

            for offset in INTEGER_OFFSETS:
                n_integer = center_n + offset
                key = (round(float(f_value), 10), n_integer)
                if key in seen:
                    continue
                seen.add(key)

                locked = p.solve_fixed_integer(
                    anchors,
                    float(f_value),
                    n_integer,
                )
                if locked is None:
                    continue

                # Enforce genuine interiority at the nominal point.  This is
                # only a search policy, not a new physics bound.  Exact fixed-N
                # continuity remains the promotion criterion.
                headroom = min(
                    locked.branch.chi - p.CHI_MIN,
                    p.CHI_MAX - locked.branch.chi,
                )
                if headroom <= 5.0e-5:
                    continue

                stability = p.stability_metrics(locked)
                if not stability["pass"]:
                    continue

                gravity = p.optimize_height(anchors, locked)
                if gravity is None or not gravity["pass"]:
                    continue

                candidates.append((locked, gravity, stability, headroom))

    return candidates


def direct_bvp_eos_stability(direct_lock):
    """Reconstruct the same direct-BVP EOS stability checks used by 018B-0A."""

    chi = float(direct_lock["chi"])
    center = direct_lock["state"]
    step = 2.0e-6

    left_chi = max(p.CHI_MIN, chi - step)
    right_chi = min(p.CHI_MAX, chi + step)
    left = p.direct_bvp_state(left_chi)
    right = p.direct_bvp_state(right_chi)

    d_sigma = (right["sigma2"] - left["sigma2"]) / (right_chi - left_chi)

    ct2 = 1.0 / (
        1.0
        + 2.0 * chi * center["sigma2"] / center["a_string"]
    )
    cl2 = 1.0 / (
        1.0
        + 2.0 * chi * d_sigma / center["sigma2"]
    )

    stable, min_disc, max_imag, worst_mode = p.fc.extrinsic_stability(ct2, cl2)

    # Reconstruct the 017P variational identity dA/dchi = -Sigma2 from direct
    # neighboring BVP states.  Use the same 0.2% tolerance as 018B-0A.
    d_a = (right["a_string"] - left["a_string"]) / (right_chi - left_chi)
    variational_relerr = abs(d_a + center["sigma2"]) / max(abs(center["sigma2"]), 1.0e-30)

    passed = (
        variational_relerr < 2.0e-3
        and 0.0 < ct2 <= 1.0
        and 0.0 < cl2 <= 1.0
        and stable
    )

    return {
        "pass": bool(passed),
        "ct2": float(ct2),
        "cl2": float(cl2),
        "variational_relerr": float(variational_relerr),
        "min_disc": float(min_disc),
        "max_imag": float(max_imag),
        "worst_mode": int(worst_mode),
    }


def print_candidate(prefix, locked, gravity, headroom, fixed_n=None):
    """Print a concise candidate summary."""

    extra = ""
    if fixed_n is not None:
        extra = (
            f" FIXED_N={fixed_n['physical_pass_count']}/{fixed_n['total']}"
            f" FIXED_N_MIN_PAYLOAD={fixed_n['min_payload']:+.9e}"
        )

    print(
        f"{prefix} "
        f"F={locked.f_value:.9f} "
        f"CHI={locked.branch.chi:.15e} "
        f"N={locked.n_integer} "
        f"HEADROOM={headroom:.15e} "
        f"PAYLOAD={gravity['payload_outward']:+.15e} "
        f"LEVERAGE={gravity['leverage_margin']:.15e} "
        f"MIN_SCALE={gravity['min_scale']:.12f} "
        f"C={gravity['c_eff']:.15e}"
        f"{extra}"
    )


def reconstruct_old_selected(anchors):
    """Reconstruct the exact previous selected state without hard-coding chi."""

    locked = p.solve_fixed_integer(anchors, 0.0384, 12553)
    if locked is None:
        raise RuntimeError("Could not reconstruct old selected F=0.0384 N=12553 state")

    gravity = p.optimize_height(anchors, locked)
    if gravity is None:
        raise RuntimeError("Old selected state no longer has a feasible gravity optimum")

    return locked, gravity


def main() -> None:
    """Run the failure classification, interior search, and decisive stop rule."""

    print("=== 018B-0A2 — FIXED-N FAILURE CLASSIFICATION + INTERIOR BASIN GATE ===")

    anchors = p.b0.reconstruct_anchors()

    # ------------------------------------------------------------------
    # 1. Reproduce and classify the old failure.
    # ------------------------------------------------------------------
    old_locked, old_gravity = reconstruct_old_selected(anchors)
    old = classify_fixed_n_cube(anchors, old_locked, old_gravity)

    print("\n=== OLD SELECTED POINT RECONSTRUCTION ===")
    print_candidate(
        "OLD_SELECTED",
        old_locked,
        old_gravity,
        min(old_locked.branch.chi - p.CHI_MIN, p.CHI_MAX - old_locked.branch.chi),
        old,
    )
    print(f"OLD_FIXED_N_ROOT_COUNT={old['root_count']}")
    print(f"OLD_FIXED_N_PASSING={old['physical_pass_count']}/{old['total']}")
    for channel, count in sorted(old["channels"].items()):
        print(f"OLD_FAILURE_CHANNEL {channel}={count}")

    old_failure_classified = (
        old["physical_pass_count"] == 122
        and old["total"] == 243
    )
    print(
        "OLD_FAILURE_CLASSIFIED="
        + ("PASS" if old_failure_classified else "CHECK_CHANGED_BASELINE")
    )

    # ------------------------------------------------------------------
    # 2. Generate interior candidates and cheap root-existence prefilter.
    # ------------------------------------------------------------------
    print("\n=== INTERIOR INTEGER-LOCKED CANDIDATE SEARCH ===")
    generated = candidate_locks(anchors)
    print(f"INTERIOR_NOMINAL_PHYSICAL_CANDIDATES={len(generated)}")

    prefiltered = []
    for locked, gravity, stability, headroom in generated:
        bracketed, total = cheap_fixed_n_bracket_fraction(anchors, locked)
        if bracketed == total:
            prefiltered.append((locked, gravity, stability, headroom))

    print(f"INTERIOR_243_OF_243_SAMPLED_BRACKET_CANDIDATES={len(prefiltered)}")

    if not prefiltered:
        print("ROBUST_INTERIOR_SAME_N_BASIN=NO_IN_SEARCHED_VERIFIED_REGION")
        print("018B0A2_FIXED_N_INTERIOR_ROBUSTNESS_GATE=RED")
        print("SINGLE_VORTON_SIMPLIFICATION=DO_NOT_PROMOTE")
        print("NEXT=TRUE_018B_GLOBAL_TOROIDAL_SOLVE_USING_VALIDATED_TWO_COPY_018A8_SOURCE")
        print("CURRENT_HEURISTIC=APPROXIMATELY_66_PERCENT_NOT_A_PROBABILITY")
        print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
        return

    # Rank only after root-existence robustness has been established.
    prefiltered.sort(key=lambda item: item[1]["c_eff"])

    # ------------------------------------------------------------------
    # 3. Exact 243/243 root + physical gate for all prefiltered candidates.
    # ------------------------------------------------------------------
    exact = []
    for locked, gravity, stability, headroom in prefiltered:
        fixed_n = classify_fixed_n_cube(anchors, locked, gravity)
        if fixed_n["pass"]:
            exact.append((locked, gravity, stability, headroom, fixed_n))
            print_candidate(
                "FIXED_N_EXACT_SURVIVOR",
                locked,
                gravity,
                headroom,
                fixed_n,
            )

    print(f"INTERIOR_EXACT_FIXED_N_243_OF_243_CANDIDATES={len(exact)}")

    if not exact:
        print("ROBUST_INTERIOR_SAME_N_BASIN=NO_IN_SEARCHED_VERIFIED_REGION")
        print("018B0A2_FIXED_N_INTERIOR_ROBUSTNESS_GATE=RED")
        print("SINGLE_VORTON_SIMPLIFICATION=DO_NOT_PROMOTE")
        print("NEXT=TRUE_018B_GLOBAL_TOROIDAL_SOLVE_USING_VALIDATED_TWO_COPY_018A8_SOURCE")
        print("CURRENT_HEURISTIC=APPROXIMATELY_66_PERCENT_NOT_A_PROBABILITY")
        print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
        return

    # Lowest C is considered only after exact same-N robustness has passed.
    exact.sort(key=lambda item: item[1]["c_eff"])

    # ------------------------------------------------------------------
    # 4. Re-run the expensive inherited family stress on a few best exact
    #    survivors.  Select the first state that remains deep-robust.
    # ------------------------------------------------------------------
    finalists = []
    for record in exact[:MAX_EXPENSIVE_FINALISTS]:
        locked, gravity, stability, headroom, fixed_n = record
        stress = p.deterministic_relocked_stress(anchors, locked, gravity)

        print(
            "INTERIOR_DETERMINISTIC_STRESS "
            f"F={locked.f_value:.9f} CHI={locked.branch.chi:.15e} N={locked.n_integer} "
            f"PASSING={stress['passed']}/{stress['total']} "
            f"ALL_PASS={'YES' if stress['all_pass'] else 'NO'} "
            f"DEEP_PASS={'YES' if stress['deep_pass'] else 'NO'} "
            f"MIN_PAYLOAD={stress['min_payload']:+.15e} "
            f"MIN_LEVERAGE={stress['min_leverage']:.15e} "
            f"MIN_SCALE={stress['min_scale']:.15e}"
        )

        if stress["all_pass"] and stress["deep_pass"]:
            finalists.append((*record, stress))

    print(f"INTERIOR_DEEP_FAMILY_ROBUST_FINALISTS={len(finalists)}")

    if not finalists:
        print("ROBUST_INTERIOR_SAME_N_BASIN=NO_AFTER_FAMILY_STRESS")
        print("018B0A2_FIXED_N_INTERIOR_ROBUSTNESS_GATE=RED")
        print("SINGLE_VORTON_SIMPLIFICATION=DO_NOT_PROMOTE")
        print("NEXT=TRUE_018B_GLOBAL_TOROIDAL_SOLVE_USING_VALIDATED_TWO_COPY_018A8_SOURCE")
        print("CURRENT_HEURISTIC=APPROXIMATELY_66_PERCENT_NOT_A_PROBABILITY")
        print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
        return

    # Robustness-first pool is now established; among it choose minimum C.
    selected = min(finalists, key=lambda item: item[1]["c_eff"])
    locked, gravity, stability, headroom, fixed_n, stress = selected

    print("\n=== SELECTED ROBUST INTERIOR SAME-N STATE ===")
    print_candidate("SELECTED_INTERIOR", locked, gravity, headroom, fixed_n)
    print(f"SELECTED_CT2={stability['ct2']:.15e}")
    print(f"SELECTED_CL2={stability['cl2']:.15e}")
    print(f"SELECTED_WORLD_SHEET_STABILITY={'PASS' if stability['pass'] else 'FAIL'}")

    # ------------------------------------------------------------------
    # 5. Random family stress.  This is inherited, not a new criterion.
    # ------------------------------------------------------------------
    random = p.randomized_relocked_stress(anchors, locked, gravity)
    print("\n=== RANDOM INTEGER-RELOCKED FAMILY STRESS ===")
    print(f"INTEGER_RELOCKED_RANDOM_PASSING={random['passed']}/{random['total']}")
    print(f"INTEGER_RELOCKED_RANDOM_MIN_PAYLOAD={random['min_payload']:+.15e}")
    print(f"INTEGER_RELOCKED_RANDOM_MIN_LEVERAGE={random['min_leverage']:.15e}")
    print(f"INTEGER_RELOCKED_RANDOM_MIN_SCALE={random['min_scale']:.15e}")
    print(f"INTEGER_RELOCKED_RANDOM_STRESS={'PASS' if random['pass'] else 'FAIL'}")

    # ------------------------------------------------------------------
    # 6. Independent direct 017P BVP integer lock + EOS stability.
    # ------------------------------------------------------------------
    print("\n=== DIRECT 017P BVP INTERIOR INTEGER LOCK ===")
    direct_lock = p.direct_integer_lock(anchors, locked)
    direct_lock_pass = direct_lock is not None
    print(f"DIRECT_BVP_INTEGER_LOCK={'PASS' if direct_lock_pass else 'FAIL'}")

    if direct_lock is None:
        direct_eos = {"pass": False}
        direct_gravity = None
    else:
        print(f"DIRECT_LOCK_CHI={direct_lock['chi']:.15e}")
        print(f"DIRECT_LOCK_N={direct_lock['n']}")
        print(f"DIRECT_LOCK_RESIDUAL={direct_lock['residual']:+.15e}")

        direct_eos = direct_bvp_eos_stability(direct_lock)
        print(f"DIRECT_BVP_VARIATIONAL_RELERR={direct_eos['variational_relerr']:.15e}")
        print(f"DIRECT_BVP_CT2={direct_eos['ct2']:.15e}")
        print(f"DIRECT_BVP_CL2={direct_eos['cl2']:.15e}")
        print(f"DIRECT_BVP_MIN_M2_TO_M40_DISCRIMINANT={direct_eos['min_disc']:+.15e}")
        print(f"DIRECT_BVP_WORST_MODE={direct_eos['worst_mode']}")
        print(f"DIRECT_BVP_MAX_ROOT_IMAG={direct_eos['max_imag']:.15e}")
        print(f"DIRECT_BVP_EOS_STABILITY={'PASS' if direct_eos['pass'] else 'FAIL'}")

        direct_gravity = p.direct_locked_gravity(anchors, direct_lock, locked.f_value)

    high_precision_pass = (
        direct_gravity is not None
        and direct_gravity["point"] > 0.0
        and direct_gravity["payload"] > 0.0
        and math.isfinite(direct_gravity["c_eff"])
    )

    if direct_gravity is not None:
        print("\n=== HIGH-PRECISION DIRECT-BVP GRAVITY ===")
        print(f"DIRECT_LOCK_X={direct_gravity['x']:.15e}")
        print(f"DIRECT_LOCK_POINT={direct_gravity['point']:+.15e}")
        print(f"DIRECT_LOCK_PAYLOAD={direct_gravity['payload']:+.15e}")
        print(f"DIRECT_LOCK_C={direct_gravity['c_eff']:.15e}")
        print(f"DIRECT_LOCK_SCOUT_WALL_POINT_RELERR={direct_gravity['scout_wall_point_relerr']:.15e}")
        print(f"DIRECT_LOCK_SCOUT_WALL_PAYLOAD_RELERR={direct_gravity['scout_wall_payload_relerr']:.15e}")

    print(f"HIGH_PRECISION_LOCKED_GRAVITY={'PASS' if high_precision_pass else 'FAIL'}")

    # ------------------------------------------------------------------
    # 7. Energy ledger remains PROJECTED until 018B-0B microscopic revalidation.
    # ------------------------------------------------------------------
    projected_c = (
        direct_gravity["c_eff"]
        if high_precision_pass
        else gravity["c_eff"]
    )
    projected_mass, projected_energy = p.energy_scaling(projected_c)

    print("\n=== PROJECTED ENERGY LEDGER ===")
    print(f"INTERIOR_PROJECTED_C={projected_c:.15e}")
    print(f"INTERIOR_PROJECTED_ONE_G_ONE_M_MASS_KG={projected_mass:.15e}")
    print(f"INTERIOR_PROJECTED_ONE_G_ONE_M_ENERGY_J={projected_energy:.15e}")
    print(f"VALIDATED_018A8_C={p.CURRENT_VALIDATED_C:.15e}")
    print(f"VALIDATED_018A8_ONE_G_ONE_M_ENERGY_J={p.CURRENT_VALIDATED_ENERGY_J:.15e}")
    print(
        "PROJECTED_IMPROVEMENT_VS_VALIDATED_018A8="
        f"{p.CURRENT_VALIDATED_C / projected_c:.15e}"
    )
    print("ENERGY_MODEL_STATUS=PROJECTED_UNTIL_INTERIOR_F_CHI_MICROSCOPIC_WALL_AND_JUNCTION_ARE_RESOLVED")

    overall = (
        old_failure_classified
        and fixed_n["pass"]
        and stability["pass"]
        and stress["all_pass"]
        and stress["deep_pass"]
        and random["pass"]
        and direct_lock_pass
        and direct_eos["pass"]
        and high_precision_pass
    )

    print("\n=== 018B-0A2 DECISION ===")
    print(f"OLD_FAILURE_CLASSIFIED={'PASS' if old_failure_classified else 'FAIL'}")
    print(f"INTERIOR_FIXED_N_LOCAL_CONTINUITY={'PASS' if fixed_n['pass'] else 'FAIL'}")
    print(f"INTERIOR_WORLD_SHEET_STABILITY={'PASS' if stability['pass'] else 'FAIL'}")
    print(f"INTERIOR_INTEGER_RELOCKED_DETERMINISTIC_STRESS={'PASS' if stress['all_pass'] and stress['deep_pass'] else 'FAIL'}")
    print(f"INTERIOR_INTEGER_RELOCKED_RANDOM_STRESS={'PASS' if random['pass'] else 'FAIL'}")
    print(f"INTERIOR_DIRECT_BVP_INTEGER_LOCK={'PASS' if direct_lock_pass else 'FAIL'}")
    print(f"INTERIOR_DIRECT_BVP_EOS_STABILITY={'PASS' if direct_eos['pass'] else 'FAIL'}")
    print(f"INTERIOR_HIGH_PRECISION_LOCKED_GRAVITY={'PASS' if high_precision_pass else 'FAIL'}")
    print(f"018B0A2_FIXED_N_INTERIOR_ROBUSTNESS_GATE={'GREEN' if overall else 'RED'}")

    if overall:
        print("ROBUST_INTERIOR_SAME_N_BASIN=YES")
        print("SINGLE_VORTON_ARCHITECTURE=SOURCE_LEVEL_ROBUST_INTERIOR_CANDIDATE")
        print("NEW_SINGLE_VORTON_MICROSCOPIC_REVALIDATION=NOT_YET_COMPLETE")
        print("NEXT=018B0B_MICROSCOPIC_REVALIDATION_AT_INTERIOR_INTEGER_LOCKED_F_CHI")
    else:
        print("ROBUST_INTERIOR_SAME_N_BASIN=NOT_PROMOTED")
        print("SINGLE_VORTON_SIMPLIFICATION=DO_NOT_PROMOTE")
        print("NEXT=TRUE_018B_GLOBAL_TOROIDAL_SOLVE_USING_VALIDATED_TWO_COPY_018A8_SOURCE")

    print("FULL_018A_GATE=GREEN_INHERITED_FOR_VALIDATED_TWO_COPY_SOURCE")
    print("TRUE_018B_GLOBAL_TOROIDAL_FIELD_SOLUTION=NOT_YET_RUN")
    print("CURRENT_HEURISTIC=APPROXIMATELY_66_PERCENT_NOT_A_PROBABILITY")
    print("HEURISTIC_INCREASE_FROM_THIS_GATE=NO_FULL_FIELD_SOLUTION_YET")
    print("PRACTICAL_ENERGY_SCALING=CATASTROPHIC")
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
    print("NEW_PHYSICS_DISCOVERY=NO")
    print("CLAIM_CLASSIFICATION=PROJECT_DERIVED_018B0A2_FIXED_N_INTERIOR_ROBUSTNESS_GATE")


if __name__ == "__main__":
    main()
