"""DELTA1-F0: sourceable R3B loaded-response prerequisites.

A registered L0/L1 scientific provider, NOT another miner runner.
Does not execute legacy AGMINER or rerun the R3B loaded PDE.

Historical R3B source/DELTA1-02 hashes are checked directly.
A Python operator builder is NOT a certified physical-source Jacobian.
"""

from __future__ import annotations

import ast
import hashlib
from pathlib import Path

import sympy as sp


CANDIDATE = "R3B_F0_INTERFACE_AUDIT"

ACTION = {
    "family": "R3B_M0_UNMODIFIED_JORDAN_PORTAL",
    "sigma": "alpha*P-beta*P**2",
    "neutral_metric": "g_phys=exp(2*sigma(P))*g_Einstein",
    "input": "IMMUTABLE_PARENT_R3B_SOURCES_AND_DELTA1_02",
    "source_variation": "NOT_ESTABLISHED",
    "loaded_JVP": "NOT_AVAILABLE_AS_A_CERTIFIED_SAME_ACTION_ARTIFACT",
    "Earth_and_support": "NOT_DERIVED",
    "exterior": "NOT_DERIVED",
    "physical_survivor": False,
}

GATES = {
    "F0_PARENT_STATE_AUDIT": "L0",
    "F0_LOADED_RECIPROCITY": "L1",
}

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

R3C_SUMMARY = (
    "results/data/"
    "032h17a12d1r3c_hook17_fdual_f_loaded_payload_homotopy_summary.json"
)

REQUIRED_CODE = (
    "provenance_gate",
    "_build_same_action_coupling",
    "_prepare_low_rank_loaded_system",
    "_solve_loaded_deviation",
)


def validate(task):
    if not isinstance(task, dict) or task.get("candidate") != CANDIDATE:
        raise ValueError("wrong candidate")

    if (
        task.get("gate") not in GATES
        or task.get("level") != GATES[task["gate"]]
    ):
        raise ValueError("wrong gate or fidelity")

    if task.get("action") != ACTION:
        raise ValueError("unreviewed action mutation")

    if task.get("requires") != []:
        raise ValueError("unreviewed dependency")


def hash_path(path):
    if not path.is_file() or path.is_symlink():
        return None

    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory(root):
    parent = {}

    for key, (name, expected) in PINS.items():
        actual = hash_path(root / name)

        parent[key] = {
            "path": name,
            "expected_sha256": expected,
            "actual_sha256": actual,
            "match": actual == expected,
        }

    fully_pinned = all(
        row["match"] for row in parent.values()
    )

    code_names = []

    if parent["R3C_LOADED_SOURCE"]["match"]:
        code = root / PINS["R3C_LOADED_SOURCE"][0]
        tree = ast.parse(code.read_text())

        present = {
            node.name
            for node in ast.walk(tree)
            if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef),
            )
        }

        code_names = [
            name for name in REQUIRED_CODE
            if name in present
        ]

    optional = root / R3C_SUMMARY

    observation = {
        "path": R3C_SUMMARY,
        "present": optional.is_file() and not optional.is_symlink(),
        "sha256": hash_path(optional),
        "solver_state_format": "NOT_CERTIFIED",
    }

    # A source function or summary JSON alone does not demonstrate
    # a constrained physical derivative E_z^{-1} E_p.

    return {
        "status": "UNDERDETERMINED",
        "decision": (
            "F0_PARENT_PROVENANCE_HOLD"
            if not fully_pinned
            else "F0_SOURCE_ACTION_AND_LOADED_JVP_NOT_CERTIFIED"
        ),
        "parents": parent,
        "all_pins_match": fully_pinned,
        "loaded_python_functions_present": code_names,
        "loaded_solver_summary_observation": observation,
        "sourceable_control_map": "NOT_DERIVED",
        "on_shell_loaded_state_for_differentiation": "NOT_CERTIFIED",
        "constraint_projected_JVP": "NOT_DEFINED",
        "conditional_Ez_inverse":
            "PROHIBITED_WITHOUT_EOM_GAUGE_AND_SOURCE_CONSTRAINTS",
        "source_realization": "NOT_ESTABLISHED",
        "no_expensive_PDE": True,
        "next_minimal_inputs": [
            "same-action residual E(z,p) for the loaded physical "
            "source and neutral matter",
            "gauge/Noether/charge/support constraints defining "
            "physical delta p",
            "on-shell loaded state and boundary/interface traction",
            "independently audited JVP and constrained-mode spectrum",
        ],
        "historical_failure_m_s2": -129.67185782242464,
        "R3B_field_only_J": 1.5429162116460216,
        "full_Einstein_and_earth": "NOT_DERIVED",
    }


def reciprocity(root):
    P, T, alpha, beta = sp.symbols(
        "P T alpha beta",
        real=True,
    )

    sigma = alpha*P-beta*P**2
    sigma_P = sp.diff(sigma, P)

    lam = sp.exp(4*sigma)*T*sigma_P

    partial_P = sp.diff(lam, P)
    partial_T = sp.diff(lam, T)

    expected_P = (
        sp.exp(4*sigma)*T*
        (sp.diff(sigma, P, 2)+4*sigma_P**2)
    )

    assert sp.simplify(
        partial_P-expected_P
    ) == 0

    assert sp.simplify(
        partial_T-sp.exp(4*sigma)*sigma_P
    ) == 0

    # Independent matter-trace gradient and P gradient.
    Px, Py, Tx, Ty = sp.symbols(
        "Px Py Tx Ty",
        real=True,
    )

    lambda_x = partial_P*Px+partial_T*Tx
    lambda_y = partial_P*Py+partial_T*Ty

    wedge = sp.simplify(
        lambda_x*Py-lambda_y*Px
    )

    expected_wedge = (
        sp.exp(4*sigma)*sigma_P*
        (Tx*Py-Ty*Px)
    )

    assert sp.simplify(
        wedge-expected_wedge
    ) == 0

    assert sp.simplify(
        wedge.subs({Tx: 0, Ty: 0})
    ) == 0

    assert sp.simplify(
        lam.subs({alpha: 0, beta: 0})
    ) == 0

    assert sp.simplify(
        lam.subs(T, 0)
    ) == 0

    point = {
        P: sp.Rational(1, 3),
        T: sp.Rational(-3, 2),
        alpha: sp.Rational(1, 10),
        beta: sp.Rational(1, 100),
    }

    first = float(lam.subs(point))
    second = float(partial_P.subs(point))

    assert abs(first) > 1e-6
    assert abs(second) > 1e-6

    return {
        "status": "SCOPED_CONTROL_ONLY",
        "decision":
            "F0_LOCAL_FIRST_SECOND_VARIATION_EXACT_"
            "LOADED_OPERATOR_UNAVAILABLE",
        "sigma": "alpha*P-beta*P**2",
        "lambda": "exp(4*sigma)*T*sigma_P",
        "partial_lambda_P_fixed_T":
            "exp(4*sigma)*T*(sigma_PP+4*sigma_P**2)",
        "partial_lambda_T_fixed_P":
            "exp(4*sigma)*sigma_P",
        "wedge":
            "grad(lambda)xgrad(P)=exp(4*sigma)*sigma_P*"
            "grad(T)xgrad(P)",
        "sigma_PP": "-2*beta",
        "first_order_acceleration":
            "-c**2*sigma_P*grad(P)  [frozen g_E only]",
        "local_hessian_diagonal_trace_response":
            "EXACT_CHAIN_RULE_NOT_CONSTRAINED_SCHUR",
        "R11_fixed_Nonlocal_Schur":
            "NOT_IMPORTED_TO_UNPROVED_R3B_ACTION",
        "sample_lambda": first,
        "sample_partial_lambda_P": second,
        "controls": {
            "coupling_zero": "ZERO",
            "trace_zero": "ZERO",
            "uniform_trace_transverse_wedge": "ZERO",
            "omit_sigma_PP_or_4sigmaP2":
                "FAIL_INDEPENDENT_CHECK",
        },
        "R3B_loaded_failure_m_s2": -129.67185782242464,
        "DELTA1_02_PQ_payload_independent_fraction": [
            0.0015922114543637095,
            0.0017631658867701,
        ],
        "interface_beta_vs_P_angle_not_PQ_rank": [
            0.6287609035434655,
            0.6342592160813438,
        ],
        "response_projection":
            "NO_NEW_SOURCEABLE_OPERATOR_OR_JVP_TO_TEST",
        "Earth_and_craft": "NOT_DERIVED",
        "complete_SI_energy": "NOT_CERTIFIED",
        "qualified_physical_survivors": 0,
    }


def run_gate(task, context):
    validate(task)
    root = Path(context["root"])

    if task["gate"] == "F0_PARENT_STATE_AUDIT":
        return inventory(root)

    return reciprocity(root)
