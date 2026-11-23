"""GRAVITY2-01 read-only provenance and action-completeness inventory.

Never imports or executes historical AGMINER; parses pinned files as data.
"""
from __future__ import annotations

import ast
import hashlib
from pathlib import Path
from fractions import Fraction as F


# The F2 loading model is A12C, not the R3B mixed-field loader.
PINS = {
    "R3B_PRELOADED": (
        "src/antigravity_research/agminer/"
        "hook17_fdual_f_global_mirror_prefight.py",
        "aa8f196fcae6a63405181ca62674e22ac67e5da88303759bdd99d25716fa2263",
    ),
    "R3B_MIXED_LOADED": (
        "src/antigravity_research/agminer/"
        "hook17_fdual_f_loaded_payload_homotopy.py",
        "a0368a7163e1f392745fd47c7c2e79fd54adce5e666362e51dc5c980c87a0fee",
    ),
    "R3X1_LORENTZ_SIGN": (
        "src/antigravity_research/agminer/"
        "hook17_fdual_f_r3x1_lorentzian_sign_audit.py",
        "6f1bf0922712a81e860075a71201af49c7870fa18fe2c21e7f576bb46da97531",
    ),
    "A12C_F2_LOAD_NOT_R3B": (
        "src/antigravity_research/agminer/"
        "hook17_f2_strong_payload_loading_rescue.py",
        "e1296794c25a4d0e4d5634c7e7d543a0b488b8d2a1963afcf7878bea1c1b99e7",
    ),
    "DELTA1_02_RECIPROCITY": (
        "src/antigravity_research/delta1/"
        "delta1_02_r3b_portal_rank.py",
        "04d8d669adb1e4b067e75a285dd13f0fbaa6bbd879090b88e850a277baca9395",
    ),
}

# Previously executed and independently verified on the user's Mac.
G00_ID = "g2_20261121T040745Z_3efae76f"
G00_SHA = (
    "d863290c37145b65d584915147e586d087f88d327a1a5f648f9e0e2447e1f890"
)
G00_VERIFY_SHA = (
    "6f13463781dc1a6c75ea4d2a41ea0328b7ec433923608eafe8e572f19545a3c4"
)

WITNESSES = {
    "R3B_PRELOADED": [
        "mirror_global_energy_gate",
        "surface_charge_diagnostics",
        "mirror_payload_reconstruction",
    ],
    "R3B_MIXED_LOADED": [
        "_build_same_action_coupling",
        "_prepare_low_rank_loaded_system",
        "_solve_loaded_deviation",
        "_run_grid",
    ],
    "R3X1_LORENTZ_SIGN": [
        "constitutive_action_gate",
        "weighted_sign_certificate",
        "run_grid",
    ],
    "A12C_F2_LOAD_NOT_R3B": [
        "solve_strong_payload_loading",
        "payload_density_profile_kg_m3",
    ],
    "DELTA1_02_RECIPROCITY": [
        "theorem",
        "perfect_mirror_control",
    ],
}

# Scoped to the five audited historical Python modules.
# This is a missing-evidence inventory, not a global no-go proof.
MISSING = {
    "einstein_hilbert_and_metric_variation":
        "NOT_IDENTIFIED_AS_COMPLETE_COVARIANT_VARIATION",
    "X_and_Y_complete_canonical_covariant_EOM":
        "NOT_IDENTIFIED_AS_COMPLETE_DYNAMICAL_SYSTEM",
    "finite_real_source_matter_action_and_JX_JY":
        "NOT_IDENTIFIED_IN_AUDITED_FILES",
    "source_boundary_and_support_stress_action":
        "NOT_IDENTIFIED_IN_AUDITED_FILES",
    "neutral_material_euler_and_interface_tractions":
        "NOT_IDENTIFIED_AS_DERIVED_FULL_ACTION",
    "Earth_matter_and_whole_craft_force_action":
        "NOT_IDENTIFIED_IN_AUDITED_FILES",
    "metric_Hodge_chain_rule_for_P":
        "NOT_INDEPENDENTLY_DERIVED_HERE",
    "off_shell_Ward_Noether_Bianchi":
        "NOT_DERIVED_FOR_COMPLETE_ACTION",
    "healthy_constrained_dynamic_modes":
        "NOT_DERIVED_FOR_COMPLETE_ACTION",
    "complete_SI_source_and_operating_energy":
        "NOT_CERTIFIED",
}


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def read_pinned(root: Path):
    out = {}
    trees = {}

    for name, (rel, expected) in PINS.items():
        p = root / rel
        actual = (
            sha(p)
            if p.is_file() and not p.is_symlink()
            else None
        )

        verdict = (
            "MATCH" if actual == expected
            else "MISSING" if actual is None
            else "DRIFT"
        )

        out[name] = {
            "relative_path": rel,
            "expected_sha256": expected,
            "actual_sha256": actual,
            "status": verdict,
        }

        if verdict == "MATCH":
            trees[name] = ast.parse(
                p.read_text(encoding="utf-8"),
                filename=rel,
            )

    return out, trees


def function_inventory(tree, names):
    funcs = {
        n.name: n
        for n in tree.body
        if isinstance(
            n, (ast.FunctionDef, ast.AsyncFunctionDef)
        )
    }

    out = []

    for name in names:
        n = funcs.get(name)

        out.append({
            "function": name,
            "status": "FOUND" if n else "MISSING",
            "start_line": n.lineno if n else None,
            "end_line": n.end_lineno if n else None,
        })

    return out


def static_action_sign():
    """Exact rational check of the R3X1-type static sign structure.

    This is a finite-dimensional algebraic negative control,
    NOT the full R3B field/matter action.
    """
    e, a, k, je, ja = (
        F(3, 5),
        F(-2, 7),
        F(4, 3),
        F(1, 4),
        F(-3, 8),
    )

    def q(x, y):
        return (
            (x*x-y*y)/2
            + k*x*y
            - je*x
            - ja*y
        )

    h = F(1, 100000)

    de = (q(e+h, a)-q(e-h, a))/(2*h)
    da = (q(e, a+h)-q(e, a-h))/(2*h)

    expected_de = e+k*a-je
    expected_da = -a+k*e-ja

    assert de == expected_de
    assert da == expected_da
    assert k == -(-k) and k != (-k)

    return {
        "status": "PASS_EXACT_SCOPED_STATIC_QUADRATIC",
        "not_the_full_R3B_action": True,
        "dQ_de_exact": str(de),
        "dQ_da_exact": str(da),
        "positive_K_cross_blocks_exact": [
            str(k), str(-k)
        ],
        "independent_central_difference_rational_exact": True,
    }


def audit(root: Path) -> dict:
    parents, trees = read_pinned(root)

    g0path = (
        root / "results" / "gravity2"
        / "runs" / G00_ID
    )

    previous = {
        "run_id": G00_ID,
        "science_sha256_expected": G00_SHA,
        "science_sha256_actual": (
            sha(g0path/"science.json")
            if (g0path/"science.json").is_file()
            else None
        ),
        "verification_sha256_expected": G00_VERIFY_SHA,
        "verification_sha256_actual": (
            sha(g0path/"independent_verification.json")
            if (g0path/"independent_verification.json").is_file()
            else None
        ),
    }

    previous["status"] = (
        "MATCH"
        if (
            previous["science_sha256_actual"] == G00_SHA
            and previous["verification_sha256_actual"]
                == G00_VERIFY_SHA
        )
        else "HOLD"
    )

    all_locked = (
        all(
            p["status"] == "MATCH"
            for p in parents.values()
        )
        and previous["status"] == "MATCH"
    )

    observations = {
        name: function_inventory(
            trees[name], WITNESSES[name]
        )
        for name in trees
    }

    witnesses_complete = (
        all(
            all(w["status"] == "FOUND" for w in xs)
            for xs in observations.values()
        )
        if len(observations) == len(PINS)
        else False
    )

    gates = {
        "G00_PARENT": (
            "PASS_SCOPED" if all_locked else "HOLD"
        ),
        "G01_ACTION": (
            "UNDERDETERMINED_IN_AUDITED_CODE"
            if all_locked and witnesses_complete
            else "NOT_RUN"
        ),
        "G02_VARIATION": "NOT_RUN_FULL_VARIATION_MISSING",
        "G03_WARD": "NOT_RUN",
        "G04_HEALTH": "NOT_RUN",
        "G05_SOURCE": "NOT_RUN",
        "G06_LOAD": "NOT_RUN",
        "G07_METRIC": "NOT_RUN",
        "G08_ENERGY": "NOT_RUN",
        "G09_EXTERIOR": "NOT_RUN",
        "G10_REACTION": "NOT_RUN",
        "G11_REALISM": "NOT_RUN",
    }

    return {
        "program": "GRAVITY2-01_ACTION_PROVENANCE_COMPILER",
        "parents": parents,
        "gravity2_00_parent": previous,
        "witnesses": observations,
        "method":
            "READ_ONLY_AST_WITH_PINNED_SHA; "
            "NO_LEGACY_IMPORT_EXECUTION",
        "sector_inventory": {
            "mixed_E_B_preloaded_geometry":
                "PRESCRIBED_AND_RECONSTRUCTED_R3B",
            "static_mixed_potentials":
                "NUMERICALLY_SOLVED_IN_FROZEN_BETA_REDUCTION_R3C_R3X1",
            "finite_torus_density":
                "PRESCRIBED_PROFILE_NOT_DYNAMICAL_MATERIAL",
            "source_current":
                "FROZEN_OR_RECONSTRUCTED_NOT_MICROSCOPIC_ACTION_DERIVED",
            "Einstein_metric": "NOT_SOLVED",
            "universal_conformal_metric":
                "DECLARED_AS_ASSUMPTION_NOT_COMPLETE_EINSTEIN_SOLUTION",
            "source_support_material": "NOT_DERIVED",
            "Earth_craft_system": "NOT_DERIVED",
        },
        "action_terms": MISSING,
        "historical_classification_correction": {
            "F2_strong_payload_rescue":
                "A12C_F2_SECTOR_NOT_R3B_MIXED_LOADED",
            "actual_R3B_mixed_loading":
                "R3B_MIXED_LOADED_AND_R3X1_LORENTZ_SIGN",
            "mutated_prior_evidence": False,
        },
        "sign_negative_control": static_action_sign(),
        "historical_loaded_min_acceleration_m_s2":
            -129.67185782242464,
        "historical_loaded_result":
            "RECORDED_NOT_RERUN",
        "historical_prescribed_capacity_J":
            1.5429162116460216,
        "capacity_result":
            "RECORDED_NOT_RECOMPUTED",
        "gates": gates,
        "qualified_source_actions": 0,
        "physical_lift": "NOT_DERIVED",
        "complete_energy": "NOT_CERTIFIED",
        "decision": (
            "ACTION_COMPLETENESS_ATLAS_NO_PHYSICAL_PROMOTION"
            if all_locked and witnesses_complete
            else "PARENT_OR_WITNESS_HOLD"
        ),
    }
