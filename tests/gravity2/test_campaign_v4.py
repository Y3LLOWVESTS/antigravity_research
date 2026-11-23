"""GRAVITY2 v4 exact review-contract adversarial tests."""
from types import SimpleNamespace
import inspect

import pytest

from antigravity_research.gravity2 import campaign_v4 as run
from antigravity_research.gravity2 import campaign_check_v4 as check
from antigravity_research.gravity2 import review_contracts_v4 as contracts
from antigravity_research.gravity2 import campaign_science as science
from antigravity_research.gravity2 import delta_f0_provider as f0


def cases():
    pair = science.default_tasks()

    joint = [
        {
            "schema": "gravity2.campaign.task.v1",
            "id": "TEST_" + gate,
            "candidate": f0.CANDIDATE,
            "gate": gate,
            "level": f0.GATES[gate],
            "action": f0.ACTION,
            "requires": [],
            "priority": 60,
            "module": "delta_f0_provider",
            "independent": "delta_f0_review",
        }
        for gate in (
            "F0_PARENT_STATE_AUDIT",
            "F0_LOADED_RECIPROCITY",
        )
    ]

    return pair + joint


def evidence_for(job):
    gate = job["gate"]

    if gate == "ACTION_COMPLETENESS":
        ev = science.completeness(job["action"])

    elif gate == "CHARGE_BALANCE_CONTROL":
        ev = {
            "status": "SCOPED_CONTROL_ONLY",
            "full_Einstein_support": "NOT_DERIVED",
            "zero_mode_tuning":
                "PRESCRIBED_FREQUENCY_CONTROL_NOT_AN_EOM_SOLUTION",
            "rows": [
                {
                    "grid": n,
                    "scalar_and_X_stationary": "NOT_TESTED",
                }
                for n in (9, 15, 23, 31)
            ],
        }

    elif gate == "F0_PARENT_STATE_AUDIT":
        ev = {
            "status": "UNDERDETERMINED",
            "constraint_projected_JVP": "NOT_DEFINED",
            "sourceable_control_map": "NOT_DERIVED",
            "on_shell_loaded_state_for_differentiation":
                "NOT_CERTIFIED",
            "R3B_field_only_J": 1.5429162116460216,
            "historical_failure_m_s2": -129.67185782242464,
        }

    else:
        ev = {
            "status": "SCOPED_CONTROL_ONLY",
            "response_projection":
                "NO_NEW_SOURCEABLE_OPERATOR_OR_JVP_TO_TEST",
            "complete_SI_energy": "NOT_CERTIFIED",
            "Earth_and_craft": "NOT_DERIVED",
            "R3B_loaded_failure_m_s2": -129.67185782242464,
        }

    checks = {
        key: True
        for key in contracts.CONTRACTS[gate]["checks"]
    }

    return ev, checks


def test_registered_contracts_and_positive_cases():
    jobs = cases()

    assert set(contracts.CONTRACTS) == {
        j["gate"] for j in jobs
    }

    for job in jobs:
        ev, checks = evidence_for(job)

        assert contracts.enforce(
            job, ev, checks
        ) == checks

        assert run.validate_job(job) == job


def test_review_set_required_not_subset():
    for job in cases():
        ev, checks = evidence_for(job)

        missing = dict(checks)
        missing.pop(next(iter(missing)))

        with pytest.raises(ValueError, match="KEYSET"):
            contracts.enforce(job, ev, missing)

        extra = {
            **checks,
            "irrelevant": True,
        }

        with pytest.raises(ValueError, match="KEYSET"):
            contracts.enforce(job, ev, extra)


def test_non_boolean_or_false_fails():
    for job in cases():
        ev, checks = evidence_for(job)
        key = next(iter(checks))

        for bad in (False, 1, None):
            copied = {
                **checks,
                key: bad,
            }

            with pytest.raises(
                ValueError,
                match="FALSE_OR_NONBOOLEAN",
            ):
                contracts.enforce(job, ev, copied)


def test_bad_verdict_or_provider_or_level_fails():
    for job in cases():
        ev, checks = evidence_for(job)

        with pytest.raises(ValueError, match="VERDICT"):
            contracts.enforce(
                job,
                {**ev, "status": "PASS_SCOPED"},
                checks,
            )

        for change in (
            {"module": "alien"},
            {"independent": "alien"},
            {"candidate": "ALIEN"},
            {"level": "L4"},
        ):
            with pytest.raises(
                ValueError,
                match="PROVIDER_OR_LEVEL",
            ):
                contracts.enforce(
                    {**job, **change},
                    ev,
                    checks,
                )


def test_cannot_promote_unproved_physics():
    for job in cases():
        ev, checks = evidence_for(job)
        gate = job["gate"]

        if gate == "ACTION_COMPLETENESS":
            ev["complete_covariant_action"] = "DERIVED"

        elif gate == "CHARGE_BALANCE_CONTROL":
            ev["rows"][0][
                "scalar_and_X_stationary"
            ] = "SOLVED"

        elif gate == "F0_PARENT_STATE_AUDIT":
            ev[
                "on_shell_loaded_state_for_differentiation"
            ] = "CERTIFIED"

        else:
            ev["Earth_and_craft"] = "DERIVED"

        with pytest.raises(
            ValueError,
            match="UNSUPPORTED_PHYSICAL_PROMOTION",
        ):
            contracts.enforce(job, ev, checks)


def test_runner_rejects_incomplete_independent_review(
    monkeypatch,
):
    job = cases()[0]
    ev, _ = evidence_for(job)

    monkeypatch.setattr(
        run.importlib,
        "import_module",
        lambda name: SimpleNamespace(
            independent_check=lambda *args: {
                "fake": True
            }
        ),
    )

    with pytest.raises(ValueError, match="KEYSET"):
        run.reviewed_checks(job, ev)


def test_runner_rejects_nonboolean_independent_review(
    monkeypatch,
):
    job = cases()[0]
    ev, checks = evidence_for(job)
    k = next(iter(checks))

    monkeypatch.setattr(
        run.importlib,
        "import_module",
        lambda name: SimpleNamespace(
            independent_check=lambda *args: {
                **checks,
                k: 1,
            }
        ),
    )

    with pytest.raises(
        ValueError,
        match="REVIEW_NON_BOOLEAN",
    ):
        run.reviewed_checks(job, ev)


def test_version_and_reviewer_provenance():
    source = inspect.getsource(check.verify)

    assert "glob('g2camp4_*')" in source
    assert "glob('g2camp2_*')" not in source

    assert all(
        n in run.CORE_FILES
        for n in (
            "campaign_v2.py",
            "campaign_check_v2.py",
            "campaign_v3.py",
            "campaign_check_v3.py",
            "campaign_v4.py",
            "campaign_check_v4.py",
            "review_contracts_v4.py",
        )
    )

    assert run.BASE.name == "campaign_v4_runs"
    assert run._make_id().startswith("g2camp4_")
