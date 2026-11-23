"""GRAVITY2-03A: exact 4D necessary identities, not a loaded solver.

The actual GRAVITY2-03 loaded-response experiment requires a
complete finite source/support action and a justified stationary
reduction. C1 currently has only a formal source-action template.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys
from datetime import datetime, timezone

import sympy as s

from .engine import (
    ROOT,
    atomic_json,
    atomic_text,
    bytes_under,
    digest,
)
from .action01 import supervise
from .action01_core import read_pinned
from .policy import PRESETS, GLOBAL_MIB


BASE = ROOT / "results/gravity2/bridge03a_runs"
RUN_RE = re.compile(r"g203a_\d{8}T\d{6}Z_[0-9a-f]{8}\Z")

PARENT_ID = "g202_20261121T042518Z_9a7f5402"

PARENT_SCIENCE = (
    "f87f925417b36f8a9b319eb4fb3c54547d9d13e1e106e9c26fcf7e997895fe61"
)

PARENT_VERIFY = (
    "b2c91f6be46c532154e5dec211af7bbd942c6c720ba0afd9fac1f184843e2b28"
)

SOURCES = (
    "bridge03a.py",
    "bridge03a_verify.py",
)

MIB = 1024 * 1024


def sha_sources():
    folder = Path(__file__).resolve().parent

    return {
        name: digest(folder / name)
        for name in SOURCES
    }


def exact_4d():
    """Exact 4D component algebra and off-shell source identities.

    No PDE, fixed-current fitting, Einstein solution or source
    existence claim is performed here.
    """

    # Convention: signature (-,+,+,+),
    # epsilon^0123 = +1/sqrt(-g).
    metric = s.diag(-1, 1, 1, 1)

    fx = s.zeros(4)
    fy = s.zeros(4)

    fx[0, 1] = 1
    fx[1, 0] = -1

    fy[2, 3] = 2
    fy[3, 2] = -2

    # P = 1/4 epsilon^{mu nu rho sigma}
    #             F_X[mu nu] F_Y[rho sigma].
    numer = s.Rational(1, 4) * sum(
        s.LeviCivita(i, j, k, l)
        * fx[i, j]
        * fy[k, l]
        for i in range(4)
        for j in range(4)
        for k in range(4)
        for l in range(4)
    )

    assert numer == 2

    t = s.symbols("t", real=True)

    # Perturb the full 4D metric, including an off-diagonal term.
    H = s.Matrix([
        [s.Rational(1, 7), s.Rational(1, 11), 0, 0],
        [s.Rational(1, 11), s.Rational(1, 5), 0, 0],
        [0, 0, -s.Rational(1, 13), 0],
        [0, 0, 0, s.Rational(1, 17)],
    ])

    g = metric + t * H

    # Fixed fundamental two-form components.
    # The volume-density dependence is NOT frozen.
    p = numer / s.sqrt(-g.det())
    p0 = numer

    alpha = s.Rational(1, 100)
    beta = s.Rational(1, 500)

    def sigma(z):
        return alpha*z - beta*z*z

    sigma_p0 = alpha - 2*beta*p0

    # Fixed F_X and F_Y imply:
    # delta P = -P/2 g^{mu nu} delta g_mu nu.
    volume_variation = s.simplify(
        s.diff(p, t).subs(t, 0)
        + p0 * s.Rational(1, 2)
        * sum(
            metric[i, j] * H[i, j]
            for i in range(4)
            for j in range(4)
        )
    )

    assert volume_variation == 0

    # An independent test stress tensor.
    # This is mathematical test data, not an actual source.
    matterT = s.Matrix([
        [2, s.Rational(1, 3), 0, 0],
        [s.Rational(1, 3), s.Rational(1, 2), 0, 0],
        [0, 0, s.Rational(1, 5), 0],
        [0, 0, 0, s.Rational(1, 7)],
    ])

    physical_t = s.exp(2*sigma(p)) * g
    physical0 = s.exp(2*sigma(p0)) * metric

    trace = sum(
        physical0[i, j] * matterT[i, j]
        for i in range(4)
        for j in range(4)
    )

    # Direct physical-metric variation.
    dphysical = physical_t.diff(t).subs(t, 0)

    direct = (
        s.Rational(1, 2)
        * s.exp(4*sigma(p0))
        * sum(
            matterT[i, j] * dphysical[i, j]
            for i in range(4)
            for j in range(4)
        )
    )

    # Independently assembled Einstein-frame matter stress:
    #
    # T_E^{mu nu} =
    #   e^{6sigma} T_tilde^{mu nu}
    #   - e^{4sigma} P sigma_P Ttilde_trace g^{mu nu}.
    #
    # This is only the contribution of the universally
    # coupled matter sector to the metric variation.
    hilbert = s.Rational(1, 2) * sum(
        (
            s.exp(6*sigma(p0)) * matterT[i, j]
            - s.exp(4*sigma(p0))
            * p0
            * sigma_p0
            * trace
            * metric[i, j]
        ) * H[i, j]
        for i in range(4)
        for j in range(4)
    )

    assert s.simplify(direct - hilbert) == 0

    # Deliberately omit metric dependence of P.
    # This wrong variation MUST fail.
    wrong_no_hodge = (
        s.Rational(1, 2)
        * s.exp(6*sigma(p0))
        * sum(
            matterT[i, j] * H[i, j]
            for i in range(4)
            for j in range(4)
        )
    )

    assert s.simplify(direct - wrong_no_hodge) != 0

    # Two independent charged-scalar U(1) sectors.
    # For each complex scalar psi=a+ib:
    #
    # u_mu = partial_mu a + q A_mu b
    # v_mu = partial_mu b - q A_mu a
    #
    # L = -1/2(u^2+v^2)-V(a^2+b^2)
    #
    # j^mu = q(b u^mu - a v^mu)
    #
    # The off-shell source identity is tested using local
    # jets in all four spacetime directions.

    identities = {}

    for sector in ("X", "Y"):
        a, b, q, m, l = s.symbols(
            f"a{sector} b{sector} q{sector} "
            f"m{sector} l{sector}",
            real=True,
        )

        A = s.symbols(f"A{sector}0:4")
        da = s.symbols(f"da{sector}0:4")
        db = s.symbols(f"db{sector}0:4")

        d2a = s.symbols(f"d2a{sector}0:4")
        d2b = s.symbols(f"d2b{sector}0:4")
        dA = s.symbols(f"dA{sector}0:4")

        sign = (-1, 1, 1, 1)

        u = [
            da[i] + q*A[i]*b
            for i in range(4)
        ]

        v = [
            db[i] - q*A[i]*a
            for i in range(4)
        ]

        du = [
            d2a[i] + q*(dA[i]*b + A[i]*db[i])
            for i in range(4)
        ]

        dv = [
            d2b[i] - q*(dA[i]*a + A[i]*da[i])
            for i in range(4)
        ]

        potential = (
            m*m*(a*a+b*b)/2
            + l*(a*a+b*b)**2/4
        )

        Ea = (
            sum(
                sign[i]*(du[i]+q*A[i]*v[i])
                for i in range(4)
            )
            - s.diff(potential, a)
        )

        Eb = (
            sum(
                sign[i]*(dv[i]-q*A[i]*u[i])
                for i in range(4)
            )
            - s.diff(potential, b)
        )

        divergence_j = q*sum(
            sign[i]*(
                db[i]*u[i]
                + b*du[i]
                - da[i]*v[i]
                - a*dv[i]
            )
            for i in range(4)
        )

        # Off-shell Noether/Ward source identity.
        assert s.expand(
            divergence_j - q*(b*Ea-a*Eb)
        ) == 0

        # Sign-flipped identity must be rejected.
        assert s.expand(
            divergence_j + q*(b*Ea-a*Eb)
        ) != 0

        identities[sector] = (
            "ZERO_OFF_SHELL_FULL_4D_SOURCE_JET"
        )

    return {
        "metric_signature": "(-,+,+,+)",
        "epsilon_convention":
            "epsilon^0123=+1/sqrt(-g)",
        "P_definition":
            "P=1/4 epsilon^{munurhosigma} "
            "F_X_munu F_Y_rhosigma",
        "P_minkowski_control": str(numer),
        "dP_fixed_F":
            "delta P=-P/2*g^{munu} delta g_munu",
        "dP_metric_variation_residual":
            str(volume_variation),
        "matter_Einstein_stress":
            "T_E^{munu}=e^{6sigma}T_tilde^{munu}"
            "-e^{4sigma}P*sigma_P*Ttilde_trace*g^{munu}",
        "metric_Hodge_chain_variation_residual":
            str(s.simplify(direct-hilbert)),
        "wrong_no_Hodge_negative_control":
            "NONZERO",
        "source_ward": identities,
        "Maxwell_field_equations":
            "nabla_mu(F_I^{munu}-lambda *F_J^{munu})"
            "=j_I^nu; lambda=e^{4sigma}"
            "*Ttilde_trace*sigma_P; J=-delta Lsrc/dA",
        "Ward_relation":
            "nabla_mu j_I^mu="
            "q_I(b_I E_aI-a_I E_bI) (off shell)",
        "gauge_Bianchi":
            "nabla_[mu F_I_nurho]=0; divergence of "
            "antisymmetric Euler tensor vanishes identically",
        "scope":
            "EXACT_LOCAL_4D_COMPONENT_AND_SOURCE_WARD; "
            "NO_GRAVITY_SOLUTION",
    }


def audit():
    parent = (
        ROOT / "results/gravity2/action02_runs"
        / PARENT_ID
    )

    files = {
        "G02_SCIENCE": (
            parent / "science.json",
            PARENT_SCIENCE,
        ),
        "G02_VERIFICATION": (
            parent / "verification.json",
            PARENT_VERIFY,
        ),
    }

    locks = {
        name: {
            "relative_path":
                str(path.relative_to(ROOT)),
            "expected_sha256": expected,
            "actual_sha256":
                digest(path) if path.is_file() else None,
        }
        for name, (path, expected) in files.items()
    }

    pinned, _ = read_pinned(ROOT)

    if not (
        all(
            v["actual_sha256"] == v["expected_sha256"]
            for v in locks.values()
        )
        and all(
            v["status"] == "MATCH"
            for v in pinned.values()
        )
    ):
        return {
            "decision": "PARENT_HOLD",
            "parent_locks": locks,
            "historical_locks": pinned,
            "gates": {"G00_PARENT": "HOLD"},
            "qualified_survivors": 0,
        }

    algebra = exact_4d()

    return {
        "decision":
            "BLOCKED_FOR_LOADED_SOLVER_"
            "INCOMPLETE_SOURCE_SUPPORT_AND_EARTH_ACTION",
        "parent_locks": locks,
        "historical_locks": pinned,
        "candidate": "C1_TWO_CHARGED_SCALARS",
        "candidate_status":
            "FORMAL_COVARIANT_SECTOR_NOT_REALIZED_SOURCE",
        "derived": algebra,
        "action_terms": {
            "EH":
                "Mpl^2/2 int sqrt(-g) R "
                "plus prescribed gravitational boundary term",
            "X_Y":
                "-1/4 int sqrt(-g)(F_X^2+F_Y^2)",
            "source":
                "int sqrt(-g) sum[-1/2 "
                "((D a_I)^2+(D b_I)^2)"
                "-V_I(a_I^2+b_I^2)]",
            "D_real":
                "u_I_mu=partial_mu a_I+q_I A_I_mu b_I; "
                "v_I_mu=partial_mu b_I-q_I A_I_mu a_I",
            "neutral":
                "S_neutral[e^{2sigma(P)}g,psi_n] UNEXPANDED",
            "Earth":
                "S_Earth[e^{2sigma(P)}g,psi_E] UNEXPANDED",
            "supports":
                "S_support[g,xi,Psi_X,Psi_Y] UNEXPANDED",
            "sigma": "sigma(P)=alpha P-beta P^2",
        },
        "gates": {
            "G00_PARENT": "PASS_SCOPED",
            "G01_ACTION":
                "ACTION_INCOMPLETE_SUPPORT_EARTH_BOUNDARY",
            "G02_VARIATION":
                "PASS_SCOPED_4D_METRIC_SOURCE_EQUATIONS",
            "G03_WARD":
                "PASS_SCOPED_4D_U1_OFFSHELL_ONLY",
            "G04_HEALTH":
                "NOT_RUN_FULL_MODE_SPECTRUM",
            "G05_SOURCE":
                "UNDERDETERMINED_FINITE_STABLE_CURRENT",
            "G06_LOAD":
                "NOT_AUTHORIZED_MISSING_STATIONARY_SOURCE_AND_SUPPORT",
            "G07_METRIC": "NOT_RUN_FULL_EINSTEIN",
            "G08_ENERGY": "NOT_CERTIFIED",
            "G09_EXTERIOR": "NOT_RUN",
            "G10_REACTION": "NOT_DERIVED",
            "G11_REALISM": "NOT_CERTIFIED",
        },
        "missing_prerequisites": [
            "One specified and stationary 4D support action "
            "with boundary tractions",
            "Earth and neutral matter equations, finite torus "
            "and source geometry",
            "Finite stable compact C1 charged source "
            "from its own equations",
            "Metric-compatible full constrained "
            "source/field/neutral Hessian",
            "Converged original R3B loaded negative control "
            "from same action",
            "Physical exterior Einstein stress and "
            "Earth/whole-craft force",
            "Complete SI energy and empirical/quantum/UV "
            "constraints",
        ],
        "original_R3B_prescribed_capacity_J":
            1.5429162116460216,
        "original_R3B_historical_loaded_min_m_s2":
            -129.67185782242464,
        "historical_values":
            "REFERENCE_ONLY_NOT_RECOMPUTED",
        "loaded_PDE_executed": False,
        "qualified_survivors": 0,
        "complete_covariant_action": "NOT_DERIVED",
        "Einstein_and_diffeomorphism_Bianchi":
            "NOT_FULLY_DERIVED",
        "complete_energy": "NOT_CERTIFIED",
        "whole_craft_lift": "NOT_DERIVED",
        "full_regression": "NOT_RUN",
    }


def run(args):
    if args.level != "L0" or args.workers != 1:
        raise ValueError(
            "03A: L0 one worker only; "
            "no loaded solver authorization"
        )

    cap, ram, disk = PRESETS[args.preset]
    seconds = 60 * args.minutes

    if not math.isfinite(seconds) or not 0 < seconds <= cap:
        raise ValueError("invalid time budget")

    if args.dry_run:
        print(json.dumps({
            "program": "GRAVITY2-03A",
            "seconds": seconds,
            "level": "L0",
            "worker_count": 1,
            "rss_soft_mib": ram,
            "disk_mib": disk,
            "legacy_AGMINER": "READ_ONLY_HASH",
            "loaded_PDE": "DISABLED",
            "scope":
                "4D_SOURCE_METRIC_ACTION_PRECONDITION_ONLY",
        }, indent=2))
        return 0

    if bytes_under(
        ROOT / "results/gravity2"
    ) > (GLOBAL_MIB-disk)*MIB:
        raise ValueError(
            "GRAVITY2 global storage budget exceeded; "
            "no automatic pruning"
        )

    BASE.mkdir(
        parents=True,
        exist_ok=True,
        mode=0o700,
    )

    run_id = (
        datetime.now(timezone.utc).strftime(
            "g203a_%Y%m%dT%H%M%SZ_"
        )
        + secrets.token_hex(4)
    )

    folder = BASE / run_id
    folder.mkdir(mode=0o700)

    manifest = {
        "program": "GRAVITY2-03A",
        "run_id": run_id,
        "preset": args.preset,
        "seconds": seconds,
        "workers": 1,
        "level": "L0",
        "rss_soft_mib": ram,
        "disk_soft_mib": disk,
        "producer_sha256": sha_sources(),
        "legacy_AGMINER_access":
            "READ_ONLY_SHA_NO_IMPORT",
        "older_GRAVITY2_modules_modified": False,
        "sympy_version": s.__version__,
    }

    atomic_json(
        folder / "manifest.json",
        manifest,
    )

    env = os.environ.copy()
    env.update({
        "PYTHONPATH": str(ROOT / "src"),
        "PYTHONDONTWRITEBYTECODE": "1",
        "OPENBLAS_NUM_THREADS": "1",
        "OMP_NUM_THREADS": "1",
        "MKL_NUM_THREADS": "1",
        "VECLIB_MAXIMUM_THREADS": "1",
    })

    child = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "antigravity_research.gravity2.bridge03a",
            "_worker",
            "--output",
            str(folder / "_worker.json"),
        ],
        cwd=ROOT,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        start_new_session=True,
        env=env,
    )

    reason, exit_code, elapsed, peak, monitor = supervise(
        child,
        folder,
        seconds,
        ram,
        disk,
    )

    result = None

    if reason == "COMPLETED" and exit_code == 0:
        try:
            result = json.loads(
                (folder / "_worker.json").read_text()
            )
        except (OSError, ValueError):
            reason = "WORKER_BAD_JSON"

    elif reason == "COMPLETED":
        reason = "WORKER_ERROR"

    (folder / "_worker.json").unlink(
        missing_ok=True
    )

    if result is None:
        result = {
            "decision": "INCOMPLETE_NO_NEW_SCIENCE",
            "gates": {},
            "qualified_survivors": 0,
        }

    science = {
        "program": "GRAVITY2-03A",
        "run_id": run_id,
        "execution_status": reason,
        "evidence": result,
        "physical_lift": "NOT_DERIVED",
        "complete_energy": "NOT_CERTIFIED",
        "qualified_survivors": 0,
        "complete_action": "NOT_DERIVED",
        "006D_replaced": False,
        "full_regression": "NOT_RUN",
        "resource": {
            "elapsed_s": elapsed,
            "worker_peak_rss_mib": peak,
            "memory_monitor": monitor,
            "monitor_kind": "SOFT_WATCHDOG",
            "worker_exit_code": exit_code,
        },
    }

    atomic_json(
        folder / "science.json",
        science,
    )

    atomic_text(
        folder / "hashes.sha256",
        digest(folder / "manifest.json")
        + "  manifest.json\n"
        + digest(folder / "science.json")
        + "  science.json\n",
    )

    print("GRAVITY2_03A_RUN=" + run_id)
    print("EXECUTION=" + reason)
    print("DECISION=" + result["decision"])
    print("LOADED_SOLVER=NOT_AUTHORIZED")
    print(
        "SCIENCE_SHA256="
        + digest(folder / "science.json")
    )

    return (
        0 if (
            reason == "COMPLETED"
            and result["decision"].startswith(
                "BLOCKED_FOR_LOADED"
            )
        ) else 3
    )


def main():
    parser = argparse.ArgumentParser(
        prog="gravity2.bridge03a"
    )
    sub = parser.add_subparsers(
        dest="cmd",
        required=True,
    )

    p = sub.add_parser("run")
    p.add_argument(
        "--level",
        choices=("L0", "L1", "L2", "L3", "L4"),
        default="L0",
    )
    p.add_argument(
        "--preset",
        choices=tuple(PRESETS),
        default="quick",
    )
    p.add_argument(
        "--minutes",
        type=float,
        default=1.0,
    )
    p.add_argument(
        "--workers",
        type=int,
        default=1,
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
    )

    worker = sub.add_parser("_worker")
    worker.add_argument("--output", required=True)

    verify_parser = sub.add_parser("verify")
    verify_parser.add_argument("--run-id", required=True)

    report = sub.add_parser("report")
    report.add_argument("--run-id", required=True)

    args = parser.parse_args()

    try:
        if args.cmd == "run":
            return run(args)

        if args.cmd == "_worker":
            out = Path(args.output)

            if (
                out.name != "_worker.json"
                or out.parent.parent.resolve() != BASE.resolve()
                or not RUN_RE.fullmatch(out.parent.name)
            ):
                raise ValueError(
                    "worker path outside GRAVITY2-03A"
                )

            atomic_json(out, audit())
            return 0

        if not RUN_RE.fullmatch(args.run_id):
            raise ValueError("invalid run ID")

        folder = BASE / args.run_id

        if args.cmd == "verify":
            from .bridge03a_verify import verify
            return verify(folder)

        sci = json.loads(
            (folder / "science.json").read_text()
        )

        evidence = sci["evidence"]

        print(json.dumps({
            "run_id": args.run_id,
            "decision": evidence["decision"],
            "gates": evidence.get("gates", {}),
            "derived": evidence.get("derived", {}),
            "missing_prerequisites":
                evidence.get("missing_prerequisites", []),
            "qualified_survivors": 0,
        }, indent=2))

        return 0

    except (
        OSError,
        ValueError,
        KeyError,
        AssertionError,
    ) as exc:
        print(
            "GRAVITY2_03A_HOLD=" + repr(exc),
            file=sys.stderr,
        )
        return 2

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
