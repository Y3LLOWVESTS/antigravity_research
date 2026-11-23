"""Independent DELTA1-F0 action/response prerequisite verifier.

Uses independent symbolic differentiation, finite differences, source
inspection and SHA hashing. Never promotes an unsourced R3B force.
"""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp


PINS = {
    "R3B_SOURCE": (
        "src/antigravity_research/agminer/"
        "hook17_fdual_f_global_mirror_prefight.py",
        "aa8f196fcae6a63405181ca62674e22ac67e5da88303759bdd99d25716fa2263",
    ),
    "R3C_LOADED_SOURCE": (
        "src/antigravity_research/agminer/"
        "hook17_fdual_f_loaded_payload_homotopy.py",
        "a0368a7163e1f392745fd47c7c2e79fd54adce5e666362e51dc5c980c87a0fee",
    ),
    "DELTA1_02_OPERATOR": (
        "src/antigravity_research/delta1/"
        "delta1_02_r3b_portal_rank.py",
        "04d8d669adb1e4b067e75a285dd13f0fbaa6bbd879090b88e850a277baca9395",
    ),
    "R3B_CAPACITY": (
        "results/data/"
        "032h17a12d1r3b_hook17_fdual_f_global_mirror_prefight_summary.json",
        "9474b6782104abb5bd8dd5e893137621b30ad96109e3e52c5a01268794810b11",
    ),
    "DELTA1_02_SCIENCE": (
        "results/data/"
        "delta1_02_20261120T172005211391Z.json",
        "3bd142aacf1b068268e0a4322274382f66c7f249035db0c25a8710d690774fc3",
    ),
    "DELTA1_02_REVIEW": (
        "results/data/"
        "delta1_02_verification_20261120T173340330519Z.json",
        "db7be8e1399e0bf04db1ca21f87fd0ed5c8e2807cfcb438c278fa817993c8ded",
    ),
}


def sha(path):
    if not path.is_file() or path.is_symlink():
        return None

    h = hashlib.sha256()

    with path.open("rb") as stream:
        for piece in iter(
            lambda: stream.read(131072),
            b"",
        ):
            h.update(piece)

    return h.hexdigest()


def independent_check(task, evidence, context):
    checks = {}
    gate = task["gate"]

    expected_levels = {
        "F0_PARENT_STATE_AUDIT": "L0",
        "F0_LOADED_RECIPROCITY": "L1",
    }

    checks["registered gate and level"] = (
        gate in expected_levels
        and task["level"] == expected_levels[gate]
    )

    checks["candidate is source audit"] = (
        task["candidate"] == "R3B_F0_INTERFACE_AUDIT"
    )

    checks["no physical promotion"] = (
        evidence.get("status")
        in ("UNDERDETERMINED", "SCOPED_CONTROL_ONLY")
    )

    if gate == "F0_PARENT_STATE_AUDIT":
        root = Path(context["root"])
        parent = evidence["parents"]
        matches = []

        for name, (relative, expected) in PINS.items():
            actual = sha(root / relative)

            checks["live parent " + name] = (
                parent[name] == {
                    "path": relative,
                    "expected_sha256": expected,
                    "actual_sha256": actual,
                    "match": actual == expected,
                }
            )

            matches.append(actual == expected)

        checks["parent status honest"] = (
            evidence["all_pins_match"] == all(matches)
        )

        checks["no automatic inverse"] = (
            evidence["constraint_projected_JVP"]
            == "NOT_DEFINED"
        )

        checks["no invented controls"] = (
            evidence["sourceable_control_map"]
            == "NOT_DERIVED"
        )

        checks["no certified loaded state"] = (
            evidence[
                "on_shell_loaded_state_for_differentiation"
            ] == "NOT_CERTIFIED"
        )

        source = root / PINS["R3C_LOADED_SOURCE"][0]

        if source.is_file():
            tree = ast.parse(source.read_text())

            functions = {
                node.name
                for node in ast.walk(tree)
                if isinstance(node, ast.FunctionDef)
            }
        else:
            functions = set()

        expected_functions = [
            name
            for name in (
                "provenance_gate",
                "_build_same_action_coupling",
                "_prepare_low_rank_loaded_system",
                "_solve_loaded_deviation",
            )
            if name in functions
        ]

        checks["loaded function inventory"] = (
            evidence["loaded_python_functions_present"]
            == expected_functions
        )

        checks["R3B loaded failure preserved"] = (
            evidence["historical_failure_m_s2"]
            == -129.67185782242464
        )

        checks["field capacity not device energy"] = (
            evidence["R3B_field_only_J"]
            == 1.5429162116460216
        )

    elif gate == "F0_LOADED_RECIPROCITY":
        p, t, A, B = sp.symbols(
            "p t A B",
            real=True,
        )

        slope = A-2*B*p
        curvature = -2*B
        s = A*p-B*p**2

        lam = t*slope*sp.exp(4*s)
        dp = sp.diff(lam, p)

        checks["second derivative with curvature"] = (
            sp.simplify(
                dp
                -t*sp.exp(4*s)*
                (curvature+4*slope*slope)
            ) == 0
        )

        checks["trace derivative"] = (
            sp.simplify(
                sp.diff(lam, t)-sp.exp(4*s)*slope
            ) == 0
        )

        vx, vy, ux, uy = sp.symbols(
            "vx vy ux uy",
            real=True,
        )

        wedge = (
            (dp*vx+sp.diff(lam, t)*ux)*vy
            -(dp*vy+sp.diff(lam, t)*uy)*vx
        )

        checks["transverse trace identity"] = (
            sp.simplify(
                wedge-sp.exp(4*s)*slope*
                (ux*vy-uy*vx)
            ) == 0
        )

        point = {
            p: sp.Rational(1, 3),
            t: sp.Rational(-3, 2),
            A: sp.Rational(1, 10),
            B: sp.Rational(1, 100),
        }

        value = float(lam.subs(point))
        derivative = float(dp.subs(point))

        checks["independent lambda sample"] = (
            abs(
                evidence["sample_lambda"]-value
            ) < 1e-14
        )

        checks["independent second variation"] = (
            abs(
                evidence["sample_partial_lambda_P"]
                -derivative
            ) < 1e-14
        )

        epsilon = sp.Rational(1, 100000)

        forward = float(
            lam.subs({
                **point,
                p: point[p]+epsilon,
            })
        )

        backward = float(
            lam.subs({
                **point,
                p: point[p]-epsilon,
            })
        )

        numeric = (forward-backward)/(2e-5)

        checks["independent finite difference"] = (
            abs(numeric-derivative) < 1e-8
        )

        checks["coupling-off null"] = (
            sp.simplify(
                lam.subs({A: 0, B: 0})
            ) == 0
        )

        checks["trace-off null"] = (
            sp.simplify(
                lam.subs(t, 0)
            ) == 0
        )

        wrong = float(
            (
                t*sp.exp(4*s)*4*slope**2
            ).subs(point)
        )

        checks["omitted curvature rejected"] = (
            abs(derivative-wrong) > 1e-5
        )

        checks["no sourceable JVP promotion"] = (
            evidence["response_projection"]
            == "NO_NEW_SOURCEABLE_OPERATOR_OR_JVP_TO_TEST"
        )

        checks["no energy or craft promotion"] = (
            evidence["complete_SI_energy"]
            == "NOT_CERTIFIED"
            and evidence["Earth_and_craft"]
            == "NOT_DERIVED"
        )

        checks["R3B loaded sign preserved"] = (
            evidence["R3B_loaded_failure_m_s2"]
            == -129.67185782242464
        )

    else:
        raise ValueError("unreviewed gate")

    if not all(checks.values()):
        raise AssertionError([
            name for name, valid in checks.items()
            if not valid
        ])

    return checks
