"""B17-M5U-X manifest, fail-closed status, and restart tests."""

import json

from antigravity_research.agminer import (
    hook17_r3b_m5u_final_decision as m,
)


def fake_parents():
    return {
        "m5r": {
            "data": {
                "results": {},
                "summary": {"gates": {}},
            }
        },
        "m5s": {
            "data": {
                "results": {},
                "summary": {
                    "gates": {
                        "S5_C2_extended_fine_phase_screen":
                            "PASS_SCREEN_ONLY"
                    }
                },
            }
        },
        "m5t": {
            "data": {
                "results": {},
                "summary": {
                    "gates": {
                        "T5_C2_quadrature_screen":
                            "PASS_SCREEN_ONLY"
                    }
                },
            }
        },
    }


def test_registered_cases_are_unique():
    quick = m.make_manifest("quick")
    full = m.make_manifest("full")

    assert len(quick) == 5
    assert len(full) == 42

    assert all(
        item in full for item in quick
    )

    assert len({
        item["name"] for item in full
    }) == 42

    assert len({
        (
            item["backend"],
            json.dumps(
                item["parameters"],
                sort_keys=True,
            ),
        )
        for item in full
    }) == 42


def test_missing_evidence_fails_closed():
    report = m.analyze(
        {
            "manifest": m.make_manifest("full"),
            "results": {},
            "errors": {},
        },
        fake_parents(),
    )

    assert report["gates"][
        "X4_smooth_C2_finer_mesh_domain_phase"
    ] == "BLOCKED_OR_INCOMPLETE"

    assert report["gates"][
        "X7_artificial_source_enclosure_support_hull_action"
    ] == "NOT_DERIVED"

    assert report["decision"] == (
        "RUN_INCOMPLETE_NO_RESEARCH_VERDICT"
    )

    assert report[
        "unverified_physical_and_assembly_claims"
    ]["artificial_model_complete"] is False

    assert report[
        "unverified_physical_and_assembly_claims"
    ]["whole_craft_lift"] is False


def test_checkpoint_resume_one_bundle(
    tmp_path, monkeypatch
):
    parents = fake_parents()

    parent_info = {
        name: {
            "path": name,
            "sha256": name,
            "cases": 0,
        }
        for name in parents
    }

    monkeypatch.setattr(
        m,
        "parents_and_code",
        lambda _: (
            parents,
            {},
            {"m5r": "fake"},
            parent_info,
        ),
    )

    calls = []

    def fake_run(job, modules):
        calls.append(job["name"])

        if job["backend"] == "m5r":
            p = job["parameters"]
            zero = p.get("zero_source", False)

            return {
                "profile": p.get("profile", "c2"),
                "width_m": p.get("width", .5),
                "closure": p.get(
                    "closure", "dipole_trace"
                ),
                "zero_source": zero,
                "domain": p.get(
                    "domain", "original"
                ),
                "phase_cells": p.get("phase", 0.),
                "mesh_h_m": p.get("h", .05),
                "derivative_step_m": p.get(
                    "step", 1.e-4
                ),
                "interaction_action_difference_j":
                    0. if zero else -1.,
                "interaction_only": {
                    "earth_derivative_j_m":
                        0. if zero else -11.,
                    "craft_derivative_j_m":
                        0. if zero else 11.,
                    "common_derivative_j_m": 0.,
                },
                "resolved_interaction_derivative":
                    None,
            }

        return {
            "h": job["parameters"]["h"],
            "profile": "c2",
            "order": job["parameters"]["order"],
            "step": job["parameters"]["step"],
            "zero_source": False,
            "same_functional_analytic_j_m": {
                "earth": -11.,
            },
            "maximum_abs_disagreement_j_m":
                1.e-6,
        }

    monkeypatch.setattr(
        m, "run_one", fake_run
    )

    args = [
        "--mode", "quick",
        "--results-dir", str(tmp_path),
    ]

    assert m.main([
        *args,
        "--max-new-cases", "1",
    ]) == 2

    bundles = list(
        tmp_path.glob(
            "b17_m5u_decision_*_quick_bundle.json"
        )
    )

    assert len(bundles) == 1

    assert m.main([
        *args,
        "--resume",
        str(bundles[0]),
    ]) == 0

    result = json.loads(
        bundles[0].read_text()
    )

    assert result["status"] == (
        "COMPLETE_NUMERICAL_DECISION_ONLY"
    )

    assert len(result["results"]) == 5
    assert len(calls) == 5

    assert result["summary"][
        "unverified_physical_and_assembly_claims"
    ]["physical_antigravity"] is False
