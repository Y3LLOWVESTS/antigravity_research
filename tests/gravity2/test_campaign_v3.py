"""GRAVITY2 Patch 2: scientific-input provenance tests."""
import json

import pytest

from antigravity_research.gravity2 import scientific_inputs_v3 as inputs
from antigravity_research.gravity2 import campaign_v3 as c
from antigravity_research.gravity2 import campaign_science as science


def fixture_root(tmp_path, monkeypatch):
    monkeypatch.setattr(
        inputs, "PACKAGE_SOURCE_NAMES",
        ("one.py", "campaign_science.py", "campaign_check.py")
    )
    pkg = tmp_path / "src/antigravity_research/gravity2"
    pkg.mkdir(parents=True)
    (pkg / "one.py").write_text("VALUE = 1\n")
    (pkg / "campaign_science.py").write_text("MODULE = 1\n")
    (pkg / "campaign_check.py").write_text("MODULE = 2\n")
    return tmp_path, pkg


def test_capture_rejects_path_escape_and_symlinks(tmp_path):
    p = tmp_path / "science.dat"
    p.write_bytes(b"data")
    assert inputs.capture(tmp_path, "science.dat")["present"]

    with pytest.raises(ValueError):
        inputs.capture(tmp_path, "../science.dat")
    with pytest.raises(ValueError):
        inputs.capture(tmp_path, "/science.dat")

    (tmp_path / "linked").symlink_to(p)
    with pytest.raises(ValueError):
        inputs.capture(tmp_path, "linked")


def test_source_changes_fingerprint(tmp_path, monkeypatch):
    root, pkg = fixture_root(tmp_path, monkeypatch)
    job = science.default_tasks()[0]
    one = inputs.manifest(root, job)

    assert one["action_sha256"] == science.signature(
        job["action"]
    )

    (pkg / "one.py").write_text("VALUE = 2\n")
    two = inputs.manifest(root, job)

    assert one != two
    assert science.signature(one) != science.signature(two)


def test_science_data_change_invalidates(tmp_path, monkeypatch):
    root, pkg = fixture_root(tmp_path, monkeypatch)
    job = science.default_tasks()[1]

    name = "results/mock/fields.npz"
    file = root / name
    file.parent.mkdir(parents=True)
    file.write_bytes(b"first")

    monkeypatch.setattr(science, "FIELDS_PARENT", name)
    monkeypatch.setattr(
        inputs, "G07_EXPECTED", inputs._sha(file)
    )

    old = inputs.manifest(root, job)
    file.write_bytes(b"second")

    with pytest.raises(
        ValueError, match="INPUT_PIN_MISMATCH"
    ):
        inputs.manifest(root, job)

    assert old["files"][name]["sha256"] != inputs._sha(file)


def test_new_or_altered_action_holds(tmp_path, monkeypatch):
    root, pkg = fixture_root(tmp_path, monkeypatch)
    job = science.default_tasks()[0]

    bad = dict(job)
    bad["action"] = dict(
        job["action"], Earth_action="FAKE"
    )
    with pytest.raises(ValueError):
        inputs.manifest(root, bad)

    bad = dict(job, module="unregistered_provider")
    with pytest.raises(
        ValueError, match="UNDECLARED_SCIENTIFIC_INPUT"
    ):
        inputs.manifest(root, bad)


def test_f0_external_pins_and_optional_hash(
    tmp_path, monkeypatch
):
    from antigravity_research.gravity2 import (
        delta_f0_provider as p,
        delta_f0_review as r,
    )

    root, pkg = fixture_root(tmp_path, monkeypatch)
    rel = "science/data.json"
    file = root / rel
    file.parent.mkdir(parents=True)
    file.write_text("{}")

    pins = {"CONTROL": (rel, inputs._sha(file))}
    monkeypatch.setattr(p, "PINS", pins)
    monkeypatch.setattr(r, "PINS", pins)
    monkeypatch.setattr(
        p, "R3C_SUMMARY", "science/optional.json"
    )

    job = {
        "candidate": p.CANDIDATE,
        "gate": "F0_PARENT_STATE_AUDIT",
        "level": "L0",
        "requires": [],
        "action": p.ACTION,
        "module": "delta_f0_provider",
        "independent": "delta_f0_review",
    }

    first = inputs.manifest(root, job)
    assert not first["files"][
        "science/optional.json"
    ]["present"]

    (root / "science/optional.json").write_text(
        '{"new": 1}'
    )
    second = inputs.manifest(root, job)
    assert second != first

    file.write_text('{"tampered": 1}')
    with pytest.raises(
        ValueError, match="INPUT_PIN_MISMATCH"
    ):
        inputs.manifest(root, job)


def test_v3_versioned_contract_and_input_guard(
    monkeypatch, tmp_path
):
    root, pkg = fixture_root(tmp_path, monkeypatch)
    job = science.default_tasks()[0]

    monkeypatch.setattr(c, "ROOT", root)
    monkeypatch.setattr(c, "PKG", pkg)
    monkeypatch.setattr(
        c, "BASE",
        root / "results/gravity2/campaign_v3_runs"
    )
    monkeypatch.setattr(
        c, "core_hashes", lambda: {"core": "x"}
    )

    before = c.fingerprint(job, {}, c.core_hashes())
    (pkg / "one.py").write_text("VALUE = 200\n")
    after = c.fingerprint(job, {}, c.core_hashes())

    assert before != after
    assert "g2camp3_" in c._make_id()
    assert c.BASE.name == "campaign_v3_runs"

    with pytest.raises(ValueError):
        c.locate("g2camp2_20261121T180843Z_a352cd7a")


def test_certified_cache_rejects_changed_science_file(
    tmp_path, monkeypatch
):
    from antigravity_research.gravity2 import (
        campaign_v3 as runner
    )

    root, pkg = fixture_root(tmp_path, monkeypatch)
    job = science.default_tasks()[0]
    code = {"test_code": "sha"}
    parents = {"test_parent": {"match": True}}

    base = root / "results/gravity2/campaign_v3_runs"
    folder = base / "g2camp3_20261121T120000Z_abcdef12"
    folder.mkdir(parents=True)

    monkeypatch.setattr(runner, "ROOT", root)
    monkeypatch.setattr(runner, "PKG", pkg)
    monkeypatch.setattr(runner, "BASE", base)
    monkeypatch.setattr(
        runner, "core_hashes", lambda: code
    )
    monkeypatch.setattr(
        runner, "parent_locks", lambda: parents
    )
    monkeypatch.setattr(
        runner, "reviewed_checks",
        lambda *a: {"scoped_independent": True}
    )

    inputs_before = inputs.manifest(root, job)
    fp = runner.fingerprint(job, parents, code)
    ev = science.completeness(job["action"])

    evidence_file = folder / (job["id"] + ".json")
    evidence_file.write_text(json.dumps(ev))

    evidence_ref = {
        "path": evidence_file.relative_to(root).as_posix(),
        "sha256": runner.digest(evidence_file),
        "from_run": folder.name,
    }
    entry = {
        "id": job["id"],
        "status": ev["status"],
        "scientific_verdict": ev["status"],
        "verification_status": "VERIFIED",
        "cache_origin": "FRESH",
        "review_checks": {"scoped_independent": True},
        "scientific_input_manifest": inputs_before,
        "fingerprint": fp,
        "evidence": evidence_ref,
    }
    science_record = {
        "run_id": folder.name,
        "state": "COMPLETED",
        "registered_tasks": [job],
        "jobs": [entry],
        "parent_locks": parents,
    }
    manifest_record = {
        "run_id": folder.name,
        "code_sha256": code,
        "tasks_sha256": science.signature([job]),
    }

    (folder / "science.json").write_text(
        json.dumps(science_record)
    )
    (folder / "manifest.json").write_text(
        json.dumps(manifest_record)
    )
    (folder / "hashes.sha256").write_text(
        "".join(
            runner.digest(folder / name)
            + "  "
            + name
            + "\n"
            for name in ("science.json", "manifest.json")
        )
    )
    (folder / "verification.json").write_text(
        json.dumps({
            "status": "PASS_SCOPED_CAMPAIGN_NO_LIFT",
            "science_sha256": runner.digest(
                folder / "science.json"
            ),
            "checks": {"completeness": True},
        })
    )
    (folder / "verification.sha256").write_text(
        runner.digest(folder / "verification.json")
        + "  verification.json\n"
    )

    assert runner.verified_cache(job, fp) is not None

    (pkg / "one.py").write_text("VALUE = 999\n")
    assert runner.verified_cache(job, fp) is None
