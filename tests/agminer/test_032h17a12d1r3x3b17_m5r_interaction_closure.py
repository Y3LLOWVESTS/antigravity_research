"""B17-M5R tests: matched subtraction and fail-closed certificates."""
import json

import pytest

from antigravity_research.agminer import (
    hook17_r3b_m5r_interaction_closure as m,
)


def test_manifest_determinism_and_no_duplicate_names():
    quick = m.tasks("quick")
    full = m.tasks("full")

    assert len(quick) == 7
    assert len(full) == 55

    assert {
        name for name, _ in quick
    }.issubset({
        name for name, _ in full
    })

    assert len({
        name for name, _ in full
    }) == len(full)

    summary = m.analyze(full, {})

    assert summary["gates"][
        "R0_M5Q_reference_preserved"
    ] == "FAIL_OR_INCOMPLETE"

    assert (
        summary["stationary_artificial_model_complete"]
        is False
    )


def test_parent_provenance_fingerprint_preserved():
    hashes = m.provenance()

    for key, expected in (
        m.EXPECTED_PARENT_SHA256.items()
    ):
        assert hashes[key] == expected


def test_matched_noearth_self_response_not_ignored():
    row = m.run_case(h=.25, domain="compact")
    x = row["interaction_only"]

    assert x[
        "noearth_earth_derivative_j_m"
    ] == pytest.approx(0., abs=1.e-12)

    assert x[
        "matched_self_translation_j_m"
    ] == pytest.approx(
        .0008001128689634473,
        abs=1.e-8,
    )

    assert x[
        "translation_partition_error_j_m"
    ] == pytest.approx(0., abs=1.e-9)

    assert row[
        "interaction_action_difference_j"
    ] != 0.

    assert (
        row["whole_spacecraft_lift_certified"]
        is False
    )


def test_source_zero_control_matches_both_actions():
    row = m.run_case(
        h=.25,
        zero_source=True,
    )

    x = row["interaction_only"]

    assert row[
        "interaction_action_difference_j"
    ] == pytest.approx(0., abs=1.e-12)

    for key in (
        "common_derivative_j_m",
        "earth_derivative_j_m",
        "craft_derivative_j_m",
    ):
        assert x[key] == pytest.approx(
            0., abs=1.e-12
        )


def test_independent_re_solved_interaction_derivative():
    row = m.run_case(
        h=.25,
        domain="compact",
        resolve=True,
    )

    resolved = row[
        "resolved_interaction_derivative"
    ]

    assert resolved is not None

    for key in (
        "common_minus_analytic_j_m",
        "earth_minus_analytic_j_m",
        "craft_minus_inferred_j_m",
    ):
        assert abs(resolved[key]) < .005


def test_parent_reproduction_single_case():
    row = m.run_case(
        h=.2,
        domain="compact",
    )

    assert row["earth_on"][
        "earth_j_m"
    ] == pytest.approx(
        -12.7882913449623,
        abs=1.e-8,
    )

    assert row["earth_on"][
        "common_j_m"
    ] == pytest.approx(
        .41078212848375095,
        abs=1.e-8,
    )


def test_c1_not_promoted_to_physical_certification():
    row = m.run_case(
        h=.125,
        profile="c1",
        width=.25,
    )

    assert abs(
        row["interaction_only"][
            "earth_derivative_j_m"
        ]
    ) > 1.

    assert (
        row["whole_spacecraft_lift_certified"]
        is False
    )

    assert (
        row["physical_reciprocity_certified"]
        is False
    )


def test_summary_does_not_certify_one_favorable_case():
    jobs = m.tasks("full")
    row = m.run_case(h=.25)

    summary = m.analyze(
        jobs,
        {"one_favorable_case": row},
    )

    assert summary["gates"][
        "R1_matched_background_and_stationary_checks"
    ] == "FAIL_OR_INCOMPLETE"

    assert summary["gates"][
        "R4_c1_interface_screen"
    ] == "BLOCKED_OR_INCOMPLETE"

    assert summary["gates"][
        "R5_phase_mesh_continuum_uniqueness"
    ] == "NOT_CERTIFIED"

    assert (
        summary["whole_craft_lift_certified"]
        is False
    )


def test_resumable_single_bundle(tmp_path, monkeypatch):
    calls = []

    mock_jobs = [
        ("case_a", {"h": .2}),
        ("case_b", {"h": .1}),
    ]

    monkeypatch.setattr(
        m,
        "tasks",
        lambda _: mock_jobs,
    )

    monkeypatch.setattr(
        m,
        "provenance",
        lambda: {
            **m.EXPECTED_PARENT_SHA256,
            "m5r": "unchanged",
        },
    )

    def fake_case(**kw):
        calls.append(kw["h"])
        return {
            "interaction_only": {
                "earth_derivative_j_m": -1.,
                "craft_derivative_j_m": 1.,
                "common_derivative_j_m": 0.,
                "matched_self_translation_j_m": 0.,
            }
        }

    monkeypatch.setattr(
        m,
        "run_case",
        fake_case,
    )

    required = {
        "R0_M5Q_reference_preserved": "PASS",
        "R1_matched_background_and_stationary_checks": "PASS",
        "R2_independently_resolved_interaction_derivatives": "PASS",
    }

    monkeypatch.setattr(
        m,
        "analyze",
        lambda *_: {"gates": required},
    )

    assert m.main([
        "--mode", "quick",
        "--results-dir", str(tmp_path),
        "--max-new-cases", "1",
    ]) == 2

    files = list(tmp_path.glob("*.json"))

    assert len(files) == 1

    partial = json.loads(
        files[0].read_text()
    )

    assert partial["status"] == (
        "PARTIAL_NOT_CERTIFIED"
    )

    assert m.main([
        "--mode", "quick",
        "--resume", str(files[0]),
    ]) == 0

    finished = json.loads(
        files[0].read_text()
    )

    assert finished["status"] == (
        "COMPLETE_NUMERICAL_DIAGNOSTIC_ONLY"
    )

    assert calls == [.2, .1]
    assert len(
        list(tmp_path.glob("*.json"))
    ) == 1
