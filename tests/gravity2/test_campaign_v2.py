"""GRAVITY2 v2: reviewed scientific dependency and cache tests.

These tests certify software controls, not antigravity physics.
"""
import json
from types import SimpleNamespace

import pytest

from antigravity_research.gravity2 import campaign_v2 as c


def test_versioned_paths():
    assert c.BASE.name == "campaign_v2_runs"
    assert c.locate(
        "g2camp2_20261121T120000Z_00000001"
    ).parent == c.BASE

    with pytest.raises(ValueError):
        c.locate("g2camp_20261121T120000Z_00000001")

    assert "campaign.py" in c.CORE_FILES
    assert "campaign_v2.py" in c.CORE_FILES


def test_reviewed_dependency():
    parent = {
        "id": "PARENT",
        "status": "PASS_SCOPED",
        "scientific_verdict": "PASS_SCOPED",
        "verification_status": "VERIFIED",
        "cache_origin": "FRESH",
        "review_checks": {"independent": True},
    }

    assert c.parent_ready([parent], "PARENT")

    cached = {
        **parent,
        "status": "REUSED_VERIFIED",
        "cache_origin": "REUSED",
    }
    assert c.parent_ready([cached], "PARENT")

    for mutation in (
        {"scientific_verdict": "FAIL_SCOPED"},
        {"scientific_verdict": "BLOCKED_ACTION_INCOMPLETE"},
        {"verification_status": "UNVERIFIED"},
        {"review_checks": {}},
        {"review_checks": {"independent": False}},
        {"review_checks": {"independent": 1}},
    ):
        assert not c.parent_ready(
            [{**parent, **mutation}], "PARENT"
        )

    assert not c.parent_ready([parent], "WRONG_PARENT")


def test_independent_reviewer_contract(monkeypatch):
    job = {"independent": "campaign_check"}

    def install(result):
        monkeypatch.setattr(
            c.importlib,
            "import_module",
            lambda *a: SimpleNamespace(
                independent_check=lambda *args: result
            ),
        )

    install({"checked": True})
    assert c.reviewed_checks(
        job, {"status": "PASS_SCOPED"}
    ) == {"checked": True}

    for bad in (
        {},
        {"checked": False},
        {"checked": 1},
        {"checked": None},
    ):
        install(bad)
        with pytest.raises(ValueError):
            c.reviewed_checks(job, {"status": "PASS_SCOPED"})

    with pytest.raises(ValueError):
        c.reviewed_checks(
            job, {"status": "CERTIFIED_GRAVITY"}
        )


def test_certified_cache_rejects_tampering(tmp_path, monkeypatch):
    root = tmp_path
    base = root / "results/gravity2/campaign_v2_runs"
    folder = base / "g2camp2_20261121T120000Z_00000001"
    folder.mkdir(parents=True)

    task = c.science.default_tasks()[0]
    fp = "test-fingerprint"
    ev = {"status": "PASS_SCOPED"}

    artifact = folder / (task["id"] + ".json")
    artifact.write_text(json.dumps(ev))

    ref = {
        "path": str(artifact.relative_to(root)),
        "sha256": c.digest(artifact),
        "from_run": folder.name,
    }

    code = {"campaign_v2.py": "test"}
    parents = {"parent": {"match": True}}

    entry = {
        "id": task["id"],
        "fingerprint": fp,
        "evidence": ref,
        "status": "PASS_SCOPED",
        "scientific_verdict": "PASS_SCOPED",
        "verification_status": "VERIFIED",
        "cache_origin": "FRESH",
        "review_checks": {"checked": True},
    }

    science = {
        "run_id": folder.name,
        "state": "COMPLETED",
        "registered_tasks": [task],
        "jobs": [entry],
        "parent_locks": parents,
    }

    manifest = {
        "run_id": folder.name,
        "code_sha256": code,
        "tasks_sha256": c.science.signature([task]),
    }

    def write_json(name, obj):
        (folder / name).write_text(json.dumps(obj))

    def seal():
        (folder / "hashes.sha256").write_text(
            "".join(
                c.digest(folder / name) + "  " + name + "\n"
                for name in ("science.json", "manifest.json")
            )
        )

    def seal_verification(v):
        write_json("verification.json", v)
        (folder / "verification.sha256").write_text(
            c.digest(folder / "verification.json")
            + "  verification.json\n"
        )

    write_json("science.json", science)
    write_json("manifest.json", manifest)
    seal()

    verification = {
        "status": "PASS_SCOPED_CAMPAIGN_NO_LIFT",
        "science_sha256": c.digest(folder / "science.json"),
        "checks": {"complete": True},
    }
    seal_verification(verification)

    monkeypatch.setattr(c, "ROOT", root)
    monkeypatch.setattr(c, "BASE", base)
    monkeypatch.setattr(c, "core_hashes", lambda: code)
    monkeypatch.setattr(c, "parent_locks", lambda: parents)
    monkeypatch.setattr(
        c,
        "reviewed_checks",
        lambda *_: {"checked": True},
    )

    assert c.verified_cache(task, fp) == (
        ref, ev, {"checked": True}
    )

    artifact.write_text('{"status":"FAIL_SCOPED"}')
    assert c.verified_cache(task, fp) is None

    artifact.write_text(json.dumps(ev))
    verification["checks"] = {"complete": False}
    seal_verification(verification)
    assert c.verified_cache(task, fp) is None

    verification["checks"] = {"complete": True}
    seal_verification(verification)

    science["jobs"][0]["verification_status"] = "UNVERIFIED"
    write_json("science.json", science)
    seal()

    verification["science_sha256"] = c.digest(
        folder / "science.json"
    )
    seal_verification(verification)

    assert c.verified_cache(task, fp) is None


def test_v2_verifier_compatibility(tmp_path, monkeypatch):
    from antigravity_research.gravity2 import (
        campaign_check_v2 as verifier
    )

    root = tmp_path
    base = root / "results/gravity2/campaign_v2_runs"
    folder = base / "g2camp2_20261121T130000Z_12345678"
    folder.mkdir(parents=True)

    task = c.science.default_tasks()[0]
    ev = c.science.completeness(task["action"])
    checks = c.reviewed_checks(task, ev)

    artifact = folder / (task["id"] + ".json")
    artifact.write_text(json.dumps(ev))

    ref = {
        "path": str(artifact.relative_to(root)),
        "sha256": c.digest(artifact),
        "from_run": folder.name,
    }

    code = {"test": "versioned"}
    parents = {}

    monkeypatch.setattr(c, "ROOT", root)
    monkeypatch.setattr(c, "BASE", base)
    monkeypatch.setattr(c, "core_hashes", lambda: code)
    monkeypatch.setattr(c, "parent_locks", lambda: parents)
    monkeypatch.setattr(verifier, "ROOT", root)

    fp = c.fingerprint(task, parents, code)

    entry = {
        "id": task["id"],
        "gate": task["gate"],
        "candidate": task["candidate"],
        "status": ev["status"],
        "scientific_verdict": ev["status"],
        "verification_status": "VERIFIED",
        "cache_origin": "FRESH",
        "review_checks": checks,
        "fingerprint": fp,
        "evidence": ref,
        "worker_peak_rss_mib": None,
    }

    science = {
        "run_id": folder.name,
        "state": "COMPLETED",
        "parent_locks": parents,
        "registered_tasks": [task],
        "jobs": [entry],
        "remaining": [],
        "skipped": [],
        "qualified_physical_survivors": 0,
        "whole_craft_lift": "NOT_DERIVED",
        "energy_J": "NOT_CERTIFIED",
        "006D_replaced": False,
        "full_repository_regression": "NOT_RUN",
        "scope": "FINITE_REGISTERED_GATES_NO_SELF_INVENTED_ACTION",
    }

    manifest = {
        "run_id": folder.name,
        "code_sha256": code,
        "tasks_sha256": c.science.signature([task]),
        "level": "L0",
        "workers": 1,
        "AGMINER": "NOT_EXECUTED",
        "L2_L4": "LOCKED",
    }

    for name, obj in (
        ("science.json", science),
        ("manifest.json", manifest),
    ):
        (folder / name).write_text(json.dumps(obj))

    (folder / "hashes.sha256").write_text(
        "".join(
            c.digest(folder / name) + "  " + name + "\n"
            for name in ("science.json", "manifest.json")
        )
    )

    assert verifier.verify(folder) == 0
    assert c.certified_entry(folder, task, fp) == (
        ref, ev, checks
    )
