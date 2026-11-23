"""GRAVITY2 immutable transactional registration catalog.

Patch 5 scope:
- Complete prospective DAG validation
- Independently reviewed gate authorization
- Producer and verifier SHA-256 pins
- Atomic generation publication
- Locked compare-and-swap activation
- Historical runner isolation

This registry is NOT connected to v1-v5 campaign execution.
New scientific-provider execution requires a separately reviewed
versioned runner.

No gravitational lift or physical source is certified.
"""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile

from . import campaign_v4 as native
from . import campaign_science as science
from . import review_contracts_v4 as contracts

SCHEMA = "gravity2.registry.snapshot.v6"
POINTER_SCHEMA = "gravity2.registry.pointer.v6"
PROPOSAL_SCHEMA = "gravity2.registry.proposal.v6"

ROOT = native.ROOT
BASE = ROOT / "results/gravity2/registry_v6"

HEX = re.compile(r"[0-9a-f]{64}\Z")
ZERO = "0" * 64


def canonical(obj):
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pack(obj):
    return (
        json.dumps(
            obj,
            sort_keys=True,
            indent=2,
            allow_nan=False,
        ) + "\n"
    ).encode()


def _regular(path, cap=262144):
    if (
        path.is_symlink()
        or not path.is_file()
        or path.stat().st_size > cap
    ):
        raise ValueError(
            "UNSAFE_REGISTRY_FILE:" + path.name
        )

    return path.read_bytes()


def _directory(path):
    if path.exists() and (
        path.is_symlink()
        or not path.is_dir()
    ):
        raise ValueError(
            "UNSAFE_REGISTRY_DIRECTORY"
        )


def _baseline():
    # Historical v4 task list: read-only.
    return native.jobs()


def graph(baseline, extras, validator=None):
    """Validate every task in the prospective combined graph."""

    if (
        not isinstance(baseline, list)
        or not isinstance(extras, list)
        or len(extras) > 32
    ):
        raise ValueError("REGISTRY_GRAPH_LIMIT")

    validator = validator or native.validate_job
    tasks = [*baseline, *extras]

    if len(tasks) > 40:
        raise ValueError("REGISTRY_TOTAL_TASK_LIMIT")

    ids = set()
    actions = {}

    for task in tasks:
        validator(task)
        ident = task["id"]

        if ident in ids:
            raise ValueError(
                "DUPLICATE_TASK_ID:" + ident
            )

        ids.add(ident)

        candidate = task["candidate"]
        action_sig = science.signature(
            task["action"]
        )

        if (
            candidate in actions
            and actions[candidate] != action_sig
        ):
            raise ValueError(
                "SAME_CANDIDATE_ACTION_COLLISION"
            )

        actions[candidate] = action_sig

    if len(actions) > 2:
        raise ValueError(
            "MORE_THAN_TWO_CANDIDATES"
        )

    lookup = {
        task["id"]: task
        for task in tasks
    }

    for task in tasks:
        req = task["requires"]

        if (
            len(req) != len(set(req))
            or task["id"] in req
        ):
            raise ValueError(
                "SELF_OR_DUPLICATE_DEPENDENCY"
            )

        for ident in req:
            if ident not in lookup:
                raise ValueError(
                    "MISSING_DEPENDENCY:" + ident
                )

            if (
                int(lookup[ident]["level"][1:])
                > int(task["level"][1:])
            ):
                raise ValueError(
                    "UPWARD_FIDELITY_DEPENDENCY"
                )

    ordered = native.dispatch_order(tasks)

    if len(ordered) != len(tasks):
        raise ValueError(
            "INVALID_GRAPH_ORDER"
        )

    return ordered


def _gen_path(base, checksum):
    if (
        not isinstance(checksum, str)
        or not HEX.fullmatch(checksum)
    ):
        raise ValueError(
            "BAD_GENERATION_ID"
        )

    return (
        base / "generations"
        / (checksum + ".json")
    )


def _pointer(base):
    _directory(base)
    _directory(base / "generations")

    path = base / "active.json"

    if not path.exists():
        if path.is_symlink():
            raise ValueError(
                "UNSAFE_ACTIVE_SYMLINK"
            )
        return None

    data = json.loads(
        _regular(path, 2048)
    )

    if (
        set(data) != {
            "schema",
            "generation_sha256",
        }
        or data["schema"] != POINTER_SCHEMA
    ):
        raise ValueError(
            "INVALID_ACTIVE_POINTER"
        )

    _gen_path(
        base,
        data["generation_sha256"],
    )

    return data["generation_sha256"]


def _snapshot(base, baseline):
    active = _pointer(base)

    if active is None:
        empty = {
            "schema": SCHEMA,
            "sequence": 0,
            "previous_sha256": ZERO,
            "baseline_signature":
                science.signature(baseline),
            "tasks": [],
        }

        return empty, sha(pack(empty))

    gen = _gen_path(base, active)
    raw = _regular(gen)

    if sha(raw) != active:
        raise ValueError(
            "GENERATION_HASH_MISMATCH"
        )

    doc = json.loads(raw)

    expected_keys = {
        "schema",
        "sequence",
        "previous_sha256",
        "baseline_signature",
        "tasks",
    }

    if set(doc) != expected_keys:
        raise ValueError(
            "GENERATION_SCHEMA_HOLD"
        )

    if (
        doc["schema"] != SCHEMA
        or type(doc["sequence"]) is not int
        or doc["sequence"] < 1
    ):
        raise ValueError(
            "GENERATION_SCHEMA_HOLD"
        )

    baseline_sig = science.signature(
        baseline
    )

    if (
        doc["baseline_signature"]
        != baseline_sig
    ):
        raise ValueError(
            "HISTORICAL_BASELINE_DRIFT"
        )

    if (
        not isinstance(doc["tasks"], list)
        or len(doc["tasks"]) > 32
    ):
        raise ValueError(
            "GENERATION_TASKS_INVALID"
        )

    prev = doc["previous_sha256"]

    genesis = {
        "schema": SCHEMA,
        "sequence": 0,
        "previous_sha256": ZERO,
        "baseline_signature": baseline_sig,
        "tasks": [],
    }

    genesis_sha = sha(pack(genesis))

    if doc["sequence"] == 1:
        if prev != genesis_sha:
            raise ValueError(
                "BROKEN_GENESIS_LINK"
            )

    else:
        seen = {active}
        expected_sequence = (
            doc["sequence"] - 1
        )
        cursor = prev

        while expected_sequence > 0:
            if (
                not isinstance(cursor, str)
                or not HEX.fullmatch(cursor)
                or cursor in seen
            ):
                raise ValueError(
                    "GENERATION_LINEAGE_CYCLE"
                )

            seen.add(cursor)
            previous = _gen_path(
                base,
                cursor,
            )

            prior_raw = _regular(previous)

            if sha(prior_raw) != cursor:
                raise ValueError(
                    "PREVIOUS_GENERATION_HASH_DRIFT"
                )

            prior = json.loads(prior_raw)

            if (
                prior.get("schema") != SCHEMA
                or prior.get("sequence")
                    != expected_sequence
                or prior.get("baseline_signature")
                    != baseline_sig
            ):
                raise ValueError(
                    "PREVIOUS_GENERATION_LINEAGE_HOLD"
                )

            cursor = prior.get(
                "previous_sha256"
            )
            expected_sequence -= 1

        if cursor != genesis_sha:
            raise ValueError(
                "GENERATION_GENESIS_HOLD"
            )

    if doc["tasks"] != sorted(
        doc["tasks"],
        key=lambda j: j["id"],
    ):
        raise ValueError(
            "NONCANONICAL_TASK_ORDER"
        )

    graph(
        baseline,
        doc["tasks"],
    )

    for task in doc["tasks"]:
        producer = native.digest(
            native.provider_file(
                task["module"]
            )
        )

        reviewer = native.digest(
            native.provider_file(
                task["independent"]
            )
        )

        if (
            task.get("provider_sha256")
            != producer
        ):
            raise ValueError(
                "REGISTERED_PROVIDER_SHA_DRIFT"
            )

        if (
            task.get("independent_sha256")
            != reviewer
        ):
            raise ValueError(
                "REGISTERED_REVIEWER_SHA_DRIFT"
            )

        contracts.authorize_registration(
            task
        )

    return doc, active


def _proposal(path):
    p = Path(path)
    raw = _regular(p, 65536)
    data = json.loads(raw)

    if (
        not isinstance(data, dict)
        or set(data) != {"schema", "tasks"}
        or data["schema"] != PROPOSAL_SCHEMA
    ):
        raise ValueError(
            "PROPOSAL_SCHEMA_INVALID"
        )

    proposed = data["tasks"]

    if (
        not isinstance(proposed, list)
        or not proposed
        or len(proposed) > 16
    ):
        raise ValueError(
            "PROPOSAL_SIZE_INVALID"
        )

    normalized = []

    for source in proposed:
        if not isinstance(source, dict):
            raise ValueError(
                "PROPOSED_TASK_NOT_OBJECT"
            )

        job = dict(source)

        for field, name in (
            ("provider_sha256", "module"),
            ("independent_sha256", "independent"),
        ):
            value = native.digest(
                native.provider_file(
                    job[name]
                )
            )

            if (
                field in job
                and job[field] != value
            ):
                raise ValueError(
                    "PROPOSED_SOURCE_PIN_DRIFT"
                )

            job[field] = value

        contracts.authorize_registration(
            job
        )

        if job["module"] == "delta_f0_provider":
            from . import delta_f0_provider as f0
            f0.validate(job)

        native.validate_job(job)
        normalized.append(job)

    return normalized


def prepare(base, filepath):
    baseline = _baseline()

    existing, old_hash = _snapshot(
        base,
        baseline,
    )

    proposed = _proposal(filepath)

    merged = [
        *existing["tasks"],
        *proposed,
    ]

    graph(
        baseline,
        merged,
    )

    candidate = {
        "schema": SCHEMA,
        "sequence":
            existing["sequence"] + 1,
        "previous_sha256": old_hash,
        "baseline_signature":
            science.signature(baseline),
        "tasks": sorted(
            merged,
            key=lambda j: j["id"],
        ),
    }

    return old_hash, candidate


def _write_immutable(path, raw):
    fd, tmpname = tempfile.mkstemp(
        prefix=".pending_",
        dir=path.parent,
    )

    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())

        os.link(
            tmpname,
            path,
        )

        dirfd = os.open(
            str(path.parent),
            os.O_RDONLY,
        )

        try:
            os.fsync(dirfd)
        finally:
            os.close(dirfd)

    finally:
        Path(tmpname).unlink(
            missing_ok=True
        )


def _replace_pointer(base, checksum):
    path = base / "active.json"

    if path.is_symlink():
        raise ValueError(
            "ACTIVE_POINTER_SYMLINK"
        )

    raw = pack({
        "schema": POINTER_SCHEMA,
        "generation_sha256": checksum,
    })

    fd, tmpname = tempfile.mkstemp(
        prefix=".new_active_",
        dir=base,
    )

    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())

        os.replace(
            tmpname,
            path,
        )

        dirfd = os.open(
            str(base),
            os.O_RDONLY,
        )

        try:
            os.fsync(dirfd)
        finally:
            os.close(dirfd)

    finally:
        Path(tmpname).unlink(
            missing_ok=True
        )


def register(
    base,
    filepath,
    expected_current,
):
    """Validate and atomically activate one immutable generation."""

    if (
        not isinstance(expected_current, str)
        or not HEX.fullmatch(
            expected_current
        )
    ):
        raise ValueError(
            "EXPECTED_GENERATION_SHA_REQUIRED"
        )

    _directory(base)

    base.mkdir(
        parents=True,
        exist_ok=True,
        mode=0o700,
    )

    generations = base / "generations"
    _directory(generations)
    generations.mkdir(
        exist_ok=True,
        mode=0o700,
    )

    lockfile = (
        base / ".registration.lock"
    )

    if lockfile.is_symlink():
        raise ValueError(
            "UNSAFE_REGISTRATION_LOCK"
        )

    with lockfile.open("a+b") as lock:
        fcntl.flock(
            lock.fileno(),
            fcntl.LOCK_EX,
        )

        try:
            current, candidate = prepare(
                base,
                filepath,
            )

            if expected_current != current:
                raise ValueError(
                    "STALE_REGISTRY_GENERATION"
                )

            raw = pack(candidate)
            checksum = sha(raw)

            target = _gen_path(
                base,
                checksum,
            )

            if (
                target.exists()
                or target.is_symlink()
            ):
                raise ValueError(
                    "IMMUTABLE_GENERATION_EXISTS"
                )

            _write_immutable(
                target,
                raw,
            )

            _replace_pointer(
                base,
                checksum,
            )

            doc, published = _snapshot(
                base,
                _baseline(),
            )

            if (
                published != checksum
                or doc != candidate
            ):
                raise ValueError(
                    "PUBLISHED_GENERATION_MISMATCH"
                )

            return (
                current,
                checksum,
                len(doc["tasks"]),
            )

        finally:
            fcntl.flock(
                lock.fileno(),
                fcntl.LOCK_UN,
            )


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="gravity2.registry_v6"
    )

    sub = parser.add_subparsers(
        dest="cmd",
        required=True,
    )

    sub.add_parser("audit")

    check = sub.add_parser("check")
    check.add_argument(
        "--file",
        required=True,
    )

    commit = sub.add_parser("register")
    commit.add_argument(
        "--file",
        required=True,
    )
    commit.add_argument(
        "--expected-current",
        required=True,
    )

    args = parser.parse_args(argv)

    try:
        if args.cmd == "audit":
            current, checksum = _snapshot(
                BASE,
                _baseline(),
            )

            print("REGISTRY_V6_AUDIT=PASS")
            print(
                "ACTIVE_GENERATION_SHA256="
                + checksum
            )
            print(
                "REGISTERED_TASKS="
                + str(len(current["tasks"]))
            )
            print(
                "HISTORICAL_CAMPAIGNS_CHANGED=NO"
            )

        elif args.cmd == "check":
            current, candidate = prepare(
                BASE,
                args.file,
            )

            print(
                "REGISTRY_V6_PRECHECK=PASS"
            )
            print(
                "EXPECTED_CURRENT_SHA256="
                + current
            )
            print(
                "PROPOSED_GENERATION_SHA256="
                + sha(pack(candidate))
            )
            print("WRITES=NONE")

        else:
            previous, checksum, count = register(
                BASE,
                args.file,
                args.expected_current,
            )

            print(
                "REGISTRY_V6_ATOMIC_COMMIT=PASS"
            )
            print(
                "PREVIOUS_GENERATION_SHA256="
                + previous
            )
            print(
                "ACTIVE_GENERATION_SHA256="
                + checksum
            )
            print(
                "REGISTERED_TASKS="
                + str(count)
            )
            print(
                "V1_V5_RUNNER_INTEGRATION=NOT_ENABLED"
            )

        return 0

    except (
        OSError,
        ValueError,
        TypeError,
        KeyError,
        json.JSONDecodeError,
    ) as exc:
        print(
            "REGISTRY_V6_HOLD=" + repr(exc),
            file=sys.stderr,
        )
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
