"""Focused DELTA1-F0 autonomous-provider regression."""

from pathlib import Path

import pytest

from antigravity_research.gravity2 import (
    delta_f0_provider as producer,
    delta_f0_review as reviewer,
)


def task(gate):
    return {
        "schema": "gravity2.campaign.task.v1",
        "id": "TEST_" + gate,
        "candidate": producer.CANDIDATE,
        "gate": gate,
        "level": producer.GATES[gate],
        "action": producer.ACTION,
        "requires": [],
        "priority": 60,
        "module": "delta_f0_provider",
        "independent": "delta_f0_review",
    }


def test_exact_variation():
    evidence = producer.reciprocity(Path("."))

    assert evidence["status"] == "SCOPED_CONTROL_ONLY"

    assert all(
        reviewer.independent_check(
            task("F0_LOADED_RECIPROCITY"),
            evidence,
            {},
        ).values()
    )


def test_missing_parent_fail_closed(tmp_path):
    evidence = producer.inventory(tmp_path)

    assert evidence["status"] == "UNDERDETERMINED"
    assert not evidence["all_pins_match"]
    assert evidence["constraint_projected_JVP"] == "NOT_DEFINED"

    assert all(
        reviewer.independent_check(
            task("F0_PARENT_STATE_AUDIT"),
            evidence,
            {"root": str(tmp_path)},
        ).values()
    )


def test_l2_not_promoted():
    from antigravity_research.gravity2 import campaign

    job = task("F0_LOADED_RECIPROCITY")
    campaign.validate_job(job)

    with pytest.raises(ValueError):
        campaign.validate_job({
            **job,
            "level": "L2",
        })


def test_action_mutation_refused():
    job = task("F0_LOADED_RECIPROCITY")

    with pytest.raises(ValueError):
        producer.validate({
            **job,
            "action": {"force": "desired"},
        })


def test_wrong_gate_level_refused():
    job = task("F0_PARENT_STATE_AUDIT")

    with pytest.raises(ValueError):
        producer.validate({
            **job,
            "level": "L1",
        })


def test_negative_controls():
    evidence = producer.reciprocity(Path("."))

    assert (
        evidence["controls"]["uniform_trace_transverse_wedge"]
        == "ZERO"
    )

    assert (
        evidence["R11_fixed_Nonlocal_Schur"]
        == "NOT_IMPORTED_TO_UNPROVED_R3B_ACTION"
    )


def test_required_physics_not_invented():
    evidence = producer.inventory(
        Path("/unobtainable_gravity2_f0_fixture")
    )

    assert "same-action residual" in (
        evidence["next_minimal_inputs"][0]
    )

    assert (
        evidence["sourceable_control_map"]
        == "NOT_DERIVED"
    )


def test_no_legacy_execution_imports():
    import ast

    for path in (
        Path(producer.__file__),
        Path(reviewer.__file__),
    ):
        tree = ast.parse(path.read_text())

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                assert all(
                    "agminer" not in item.name.lower()
                    for item in node.names
                )

            if (
                isinstance(node, ast.ImportFrom)
                and node.module
            ):
                assert (
                    "agminer"
                    not in node.module.lower()
                )
