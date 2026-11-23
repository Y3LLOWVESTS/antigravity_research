"""GRAVITY2 v3 scientific-input provenance.

Review-bounded coverage for the two accepted L0/L1 gate families.
Captures a fixed Python-source superset, declared source/data parents,
action identity and runtime versions.

Not a complete physical action, source realization or gravity certificate.
"""
from __future__ import annotations

import hashlib
import platform
from pathlib import Path
import sys

import numpy as np
import scipy
import sympy as sp

from . import campaign_science, delta_f0_provider, delta_f0_review

SCHEMA = "gravity2.scientific_inputs.v3"
G07_EXPECTED = "ee9c9557d6d30897d8ed3a4872b11bc464c17af37d98f87c4047884bb0bcc46d"
PACKAGE_SOURCE_NAMES = ('__init__.py', '__main__.py', 'act0.py', 'action01.py', 'action01_core.py', 'action01_verify.py', 'action02.py', 'action02_core.py', 'action02_verify.py', 'bridge03a.py', 'bridge03a_verify.py', 'bridge05.py', 'bridge05_check.py', 'bridge05_core.py', 'bridge06.py', 'bridge06_check.py', 'bridge06_core.py', 'bridge07.py', 'bridge07_check.py', 'bridge07_core.py', 'bridge08.py', 'bridge08_check.py', 'bridge08_core.py', 'campaign.py', 'campaign_check.py', 'campaign_check_v2.py', 'campaign_check_v3.py', 'campaign_science.py', 'campaign_v2.py', 'campaign_v3.py', 'delta_f0_provider.py', 'delta_f0_review.py', 'engine.py', 'independent.py', 'miner.py', 'miner2.py', 'miner2_check.py', 'miner2_math.py', 'miner_cases.py', 'miner_verify.py', 'policy.py', 'scientific_inputs_v3.py')


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(131072), b""):
            h.update(block)
    return h.hexdigest()


def capture(root: Path, relative: str, *,
            expected: str | None = None,
            required: bool = True) -> dict:
    root = Path(root).resolve(strict=True)
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise ValueError("INPUT_PATH_UNSAFE")
    rel = Path(relative)
    if rel.is_absolute() or any(
        x in ("", ".", "..") for x in rel.parts
    ):
        raise ValueError("INPUT_PATH_UNSAFE")

    node = root
    for part in rel.parts:
        node = node / part
        if node.is_symlink():
            raise ValueError("INPUT_SYMLINK_HOLD:" + relative)

    if not node.exists():
        if required:
            raise ValueError("REQUIRED_INPUT_MISSING:" + relative)
        return {"present": False, "sha256": None}

    if not node.is_file() or not node.resolve().is_relative_to(root):
        raise ValueError("INPUT_NOT_REGULAR:" + relative)

    actual = _sha(node)
    if expected is not None and actual != expected:
        raise ValueError("INPUT_PIN_MISMATCH:" + relative)

    return {"present": True, "sha256": actual}


def manifest(root: Path, job: dict) -> dict:
    """Conservative manifest for current registered scientific gates."""
    root = Path(root).resolve(strict=True)
    pair = (
        job.get("module"),
        job.get("independent"),
        job.get("gate"),
    )
    jpair = ("campaign_science", "campaign_check")
    f0pair = ("delta_f0_provider", "delta_f0_review")
    files = {}

    if pair[:2] == jpair and pair[2] in (
        "ACTION_COMPLETENESS", "CHARGE_BALANCE_CONTROL"
    ):
        campaign_science.validate_task(job)
        if pair[2] == "CHARGE_BALANCE_CONTROL":
            rel = campaign_science.FIELDS_PARENT
            files[rel] = capture(
                root, rel, expected=G07_EXPECTED
            )

    elif pair[:2] == f0pair and pair[2] in (
        "F0_PARENT_STATE_AUDIT", "F0_LOADED_RECIPROCITY"
    ):
        delta_f0_provider.validate(job)

        if delta_f0_provider.PINS != delta_f0_review.PINS:
            raise ValueError(
                "PRODUCER_REVIEW_PARENT_DISAGREEMENT"
            )

        for name, (rel, pin) in sorted(
            delta_f0_provider.PINS.items()
        ):
            files[rel] = capture(root, rel, expected=pin)

        optional = delta_f0_provider.R3C_SUMMARY
        files[optional] = capture(
            root, optional, required=False
        )
    else:
        raise ValueError(
            "UNDECLARED_SCIENTIFIC_INPUT_FAMILY:" + repr(pair)
        )

    package = root / "src/antigravity_research/gravity2"
    if not package.is_dir() or package.is_symlink():
        raise ValueError("INPUT_PACKAGE_MISSING")

    if (
        not isinstance(PACKAGE_SOURCE_NAMES, tuple)
        or not PACKAGE_SOURCE_NAMES
    ):
        raise ValueError("INPUT_SOURCE_SET_UNDECLARED")

    for name in PACKAGE_SOURCE_NAMES:
        path = package / name
        rel = path.relative_to(root).as_posix()
        files[rel] = capture(root, rel)

    return {
        "schema": SCHEMA,
        "coverage":
            "REVIEWED_L0_L1_DECLARED_INPUTS_AND_PACKAGE_PYTHON_SUPERSET",
        "gate": job["gate"],
        "candidate": job["candidate"],
        "action_sha256": campaign_science.signature(
            job["action"]
        ),
        "runtime": {
            "python": (
                platform.python_implementation()
                + " "
                + platform.python_version()
            ),
            "platform": sys.platform,
            "machine": platform.machine(),
            "numpy": np.__version__,
            "sympy": sp.__version__,
            "scipy": scipy.__version__,
        },
        "files": dict(sorted(files.items())),
    }
