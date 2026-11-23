"""GRAVITY2 broad scoped screening. Full pytest is opt-in.

Mathematical toy screening is not a sourced gravitational experiment.
Historical evidence is read-only; every new batch has its own directory.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import shutil
import subprocess
import sys
import tarfile
import traceback

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from antigravity_research.gravity2 import response_v7, response_check_v7

BASE = ROOT / "results/gravity2/big_runs"

SOURCE_SHA = {
    "src/antigravity_research/gravity2/campaign_v4.py":
        "a3785e5bf8bce670af73f4e7b5bbfb2e330f74cb08682e37cf6294292ebe2ef5",
    "src/antigravity_research/gravity2/campaign_v5.py":
        "92ca8c97a610420daf45ad5cdc69fc8b1c75a8eb70645c6814ba50484378675a",
    "src/antigravity_research/gravity2/registry_v6.py":
        "c1232e82ab657b66a5667b17a0a68938e8cf5b16651c3b66c8e8de9cca2ae76f",
    "src/antigravity_research/gravity2/response_v7.py":
        "d2feeee61d1355c5feeb3a40b6af0aeb503a650fed1b29496fa87aa5b6f247bf",
    "src/antigravity_research/gravity2/response_check_v7.py":
        "705af3f64c70a98a20551b36e14014e6fb9d89fc2c4cdf97c5d485543a716c1d",
    "src/antigravity_research/gravity2/planner_v8.py":
        "5fcedfacac7742e002929b4b270f1a70fe299741cc0891a3d5ab292397b8b244",
    "src/antigravity_research/gravity2/research_v8.py":
        "2dd0af8538a8e6675d96b57d9d172a110890b94139d4a1f9e895a47304bf764b",
    "tests/gravity2/test_registry_v6.py":
        "4135f064c4175e87988dada38e3205727cb03b10ddad607ff7c8ca602d17d56f",
    "tests/gravity2/test_research_v8.py":
        "9d547ef448d0ade3f9725bac083317e99556e6f44bce080b85cefea2798c8c21",
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, data):
    if path.exists() or path.is_symlink():
        raise RuntimeError("IMMUTABLE_OUTPUT_EXISTS:" + str(path))
    path.write_text(
        json.dumps(data, indent=2, sort_keys=True, allow_nan=False) + "\n"
    )


def call(out, steps, label, args):
    logfile = out / (label + ".log")
    env = dict(os.environ)
    env["PYTHONPATH"] = str(ROOT / "src")

    for key in (
        "OPENBLAS_NUM_THREADS",
        "OMP_NUM_THREADS",
        "MKL_NUM_THREADS",
        "VECLIB_MAXIMUM_THREADS",
    ):
        env[key] = "1"

    print("\n=== " + label + " ===", flush=True)

    with logfile.open("x") as stream:
        proc = subprocess.Popen(
            [sys.executable, *args],
            cwd=ROOT,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
            bufsize=1,
        )

        for line in proc.stdout:
            print(line, end="", flush=True)
            stream.write(line)

        rc = proc.wait()

    steps.append({
        "name": label,
        "exit_code": rc,
        "log": logfile.name,
        "log_sha256": sha(logfile),
    })

    print(
        "STEP_" + label.upper() + "="
        + ("PASS" if rc == 0 else "FAIL"),
        flush=True,
    )

    if rc:
        raise RuntimeError(label + "_FAILED_EXIT_" + str(rc))

    return logfile.read_text()


def run_id(text, pattern, label):
    matches = re.findall(pattern, text, re.MULTILINE)

    if len(matches) != 1:
        raise RuntimeError("RUN_ID_MISSING_OR_AMBIGUOUS:" + label)

    return matches[0]


def stress(out, n=2048):
    rng = np.random.default_rng(20261121)
    records = []
    families = []

    for nf in (1, 2):
        for band in ("weak", "strong"):
            flips = 0
            positives = 0
            negatives = 0
            largest_shift = 0.0
            max_schur = 0.0
            max_stationarity = 0.0
            smallest_eig = float("inf")

            for i in range(n):
                av = rng.uniform(2, 6, 2)
                cv = rng.uniform(2, 6, nf)

                u = rng.normal(size=(2, nf))
                u /= max(
                    float(np.linalg.svd(u, compute_uv=False)[0]),
                    1e-12,
                )

                factor = (
                    rng.uniform(.03, .3)
                    if band == "weak"
                    else rng.uniform(.6, .91)
                )

                b = (
                    np.sqrt(av)[:, None]
                    * u
                    * np.sqrt(cv)[None, :]
                    * factor
                )

                spec = response_v7.example()
                spec.update(
                    A=np.diag(av).tolist(),
                    B=b.tolist(),
                    C=np.diag(cv).tolist(),
                    j_source=rng.normal(size=2).tolist(),
                    j_field=rng.normal(size=nf).tolist(),
                    translation_source=rng.normal(size=2).tolist(),
                    translation_field=rng.normal(size=nf).tolist(),
                    relative_displacement=float(
                        rng.uniform(-.5, .5)
                    ),
                )

                result = response_v7.compute(spec)
                checks = response_check_v7.review(spec, result)

                if (
                    not all(checks.values())
                    or result["whole_craft_lift"] != "NOT_DERIVED"
                ):
                    raise RuntimeError(
                        "TOY_INDEPENDENT_REVIEW_FAILED"
                    )

                z = np.asarray(
                    result["loaded_field_response_toy"]
                )
                f = np.asarray(
                    result["frozen_field_response_toy"]
                )

                changed = (
                    abs(z[0]) > 1e-10
                    and abs(f[0]) > 1e-10
                    and z[0] * f[0] < 0
                )

                flips += bool(changed)
                force = result["craft_coordinate_force_toy"]

                positives += force > 0
                negatives += force < 0

                shift = float(np.max(np.abs(z - f)))

                largest_shift = max(largest_shift, shift)
                max_schur = max(
                    max_schur, result["schur_error"]
                )
                max_stationarity = max(
                    max_stationarity,
                    result["stationary_residual"],
                )
                smallest_eig = min(
                    smallest_eig,
                    result["min_hessian_eigenvalue"],
                )

                records.append({
                    "family": f"field{nf}_{band}",
                    "case": i,
                    "loaded_first": z[0],
                    "frozen_first": f[0],
                    "sign_change": int(changed),
                    "max_shift": shift,
                    "toy_coordinate_force": force,
                    "min_hessian_eig":
                        result["min_hessian_eigenvalue"],
                    "schur_error": result["schur_error"],
                    "stationary_residual":
                        result["stationary_residual"],
                })

            if nf == 1 and flips:
                raise RuntimeError(
                    "ONE_FIELD_POSITIVE_SCHUR_SIGN_FAILURE"
                )

            fam = {
                "name": f"field{nf}_{band}",
                "cases": n,
                "sign_changes": flips,
                "positive_toy_coordinate_forces": positives,
                "negative_toy_coordinate_forces": negatives,
                "max_response_shift": largest_shift,
                "max_schur_error": max_schur,
                "max_stationary_residual": max_stationarity,
                "min_hessian_eigenvalue": smallest_eig,
            }

            families.append(fam)

            print(
                f"STRESS={fam['name']} "
                f"CASES={n} "
                f"COMPONENT_SIGN_CHANGES={flips}",
                flush=True,
            )

    controls = []

    for name, edit, expected in (
        (
            "asymmetric_action",
            lambda s: s["A"][0].__setitem__(1, .7),
            "NO_COMMON_QUADRATIC_ACTION",
        ),
        (
            "negative_hessian",
            lambda s: s["A"][0].__setitem__(0, -1.),
            "UNHEALTHY_TOY_MODE",
        ),
        (
            "claimed_source",
            lambda s: s.__setitem__(
                "source_kind", "PHYSICAL"
            ),
            "PHYSICAL_SOURCE_OR_SI_NOT_DERIVED",
        ),
        (
            "nonfinite_translation",
            lambda s: s["translation_source"].__setitem__(
                0, float("nan")
            ),
            "NONFINITE_OR_UNBOUNDED_TOY",
        ),
    ):
        spec = response_v7.example()
        edit(spec)
        observed = "NOT_REJECTED"

        try:
            response_v7.compute(spec)
        except ValueError as err:
            observed = str(err)

        if observed != expected:
            raise RuntimeError(
                "ADVERSARIAL_CONTROL_FAILED:"
                + name + ":" + observed
            )

        controls.append({
            "name": name,
            "expected": expected,
            "observed": observed,
            "pass": True,
        })

    uncoupled = response_v7.example()
    uncoupled["B"] = [[0.], [0.]]

    zr = response_v7.compute(uncoupled)

    if (
        not all(
            response_check_v7.review(
                uncoupled, zr
            ).values()
        )
        or abs(
            zr["loaded_field_response_toy"][0]
            - zr["frozen_field_response_toy"][0]
        ) > 1e-12
    ):
        raise RuntimeError(
            "ZERO_COUPLING_NEGATIVE_CONTROL_FAIL"
        )

    controls.append({
        "name": "zero_coupling",
        "expected": "LOADED_EQ_FROZEN",
        "pass": True,
    })

    with (
        out / "toy_stress_cases.csv"
    ).open("x", newline="") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=list(records[0]),
        )
        writer.writeheader()
        writer.writerows(records)

    result = {
        "schema": "gravity2.broad_toy_stress.v1",
        "seed": 20261121,
        "total_cases": len(records),
        "families": families,
        "negative_controls": controls,
        "verdict": "PASS_SCOPED_TOY_NO_GRAVITY",
        "source_action_new": False,
        "physical_survivors": 0,
        "Einstein_metric": "NOT_DERIVED",
        "whole_craft_lift": "NOT_DERIVED",
        "complete_SI_energy": "NOT_CERTIFIED",
        "next_gate": "G01_ACTION",
    }

    save(out / "toy_stress_summary.json", result)
    return result


def f0_inventory(out):
    data = ROOT / "results/data"
    index = []

    if data.is_dir() and not data.is_symlink():
        for p in sorted(data.rglob("*.json")):
            if len(index) >= 5000:
                break

            rel = p.relative_to(ROOT)
            key = str(rel).lower()

            if (
                "f0" not in key
                or "delta" not in key
                or p.is_symlink()
                or not p.is_file()
                or p.stat().st_size > 10_000_000
            ):
                continue

            index.append({
                "path": str(rel),
                "sha256": sha(p),
                "bytes": p.stat().st_size,
            })

    copied = []
    cumulative = 0

    for item in index[-80:]:
        if cumulative + item["bytes"] > 12_000_000:
            continue

        source = ROOT / item["path"]
        dest = (
            out / "evidence/historical_f0"
            / source.relative_to(data)
        )

        dest.parent.mkdir(
            parents=True, exist_ok=True
        )
        shutil.copyfile(source, dest)

        if sha(source) != sha(dest):
            raise RuntimeError(
                "HISTORICAL_F0_COPY_DRIFT"
            )

        cumulative += item["bytes"]
        copied.append(str(dest.relative_to(out)))

    save(
        out / "f0_result_index.json",
        {
            "index": index,
            "copied": copied,
            "scope":
                "RAW_INVENTORY_ONLY_NOT_INDEPENDENT_PHYSICS_VALIDATION",
        },
    )

    print(
        f"F0_INDEX={len(index)} "
        f"F0_COPIED={len(copied)}",
        flush=True,
    )


def evidence(out, name, relative, rid):
    source = ROOT / relative / rid

    if not source.is_dir() or source.is_symlink():
        raise RuntimeError(
            "MISSING_EVIDENCE:" + name
        )

    dest = out / "evidence" / name
    dest.mkdir(parents=True)

    count = 0

    for p in source.rglob("*"):
        if (
            not p.is_file()
            or p.is_symlink()
            or p.stat().st_size > 8_000_000
            or p.name.startswith("_")
            or p.name.endswith(".lock")
        ):
            continue

        target = dest / p.relative_to(source)

        target.parent.mkdir(
            parents=True, exist_ok=True
        )
        shutil.copyfile(p, target)

        if sha(p) != sha(target):
            raise RuntimeError(
                "EVIDENCE_COPY_DRIFT:" + name
            )

        count += 1

    print(
        f"EVIDENCE_{name.upper()}_FILES={count}",
        flush=True,
    )


def finish(out, steps, runs, stress_result, errors, full):
    if not full:
        regression_status = "NOT_RUN_DEFAULT"
    elif any(
        x["name"] == "full_repository_regression"
        and x["exit_code"] == 0
        for x in steps
    ):
        regression_status = "PASS"
    else:
        regression_status = "FAIL_OR_NOT_REACHED"

    summary = {
        "schema": "gravity2.big_scoped_batch.v1",
        "run_id": out.name,
        "generated_utc":
            datetime.now(timezone.utc).isoformat(),
        "run_ids": runs,
        "steps": steps,
        "stress_status":
            stress_result["verdict"]
            if stress_result else "NOT_COMPLETED",
        "full_regression": regression_status,
        "status":
            "PASS_SCOPED" if not errors else "HOLD",
        "errors": errors,
        "physics_experiments_new": 0,
        "physical_survivors": 0,
        "006D_replaced": False,
        "Earth_down_craft_up": "NOT_DERIVED",
        "whole_craft_lift": "NOT_DERIVED",
        "complete_energy": "NOT_CERTIFIED",
        "next_scientific_gate": "G01_ACTION",
    }

    save(out / "summary.json", summary)

    lines = []

    for p in sorted(out.rglob("*")):
        if (
            p.is_file()
            and not p.is_symlink()
            and p.name != "SHA256SUMS.txt"
            and not p.name.endswith(".tar.gz")
        ):
            lines.append(
                sha(p) + "  "
                + str(p.relative_to(out))
            )

    (
        out / "SHA256SUMS.txt"
    ).write_text("\n".join(lines) + "\n")

    archive = out / (out.name + "_UPLOAD.tar.gz")

    with tarfile.open(
        archive, "w:gz"
    ) as tf:
        for p in sorted(out.rglob("*")):
            if (
                p.is_file()
                and not p.is_symlink()
                and p != archive
            ):
                tf.add(
                    p,
                    arcname=str(
                        Path(out.name)
                        / p.relative_to(out)
                    ),
                    recursive=False,
                )

    print("\n=== UPLOAD RESULTS ===", flush=True)
    print("BROAD_STATUS=" + summary["status"])
    print(
        "FULL_REGRESSION="
        + summary["full_regression"]
    )
    print("UPLOAD_ARCHIVE=" + str(archive))
    print("UPLOAD_ARCHIVE_SHA256=" + sha(archive))
    print(
        "SUMMARY_JSON="
        + str(out / "summary.json")
    )
    print(
        "STRESS_JSON="
        + str(out / "toy_stress_summary.json")
    )
    print(
        "SHA256SUMS="
        + str(out / "SHA256SUMS.txt")
    )


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__
    )

    parser.add_argument(
        "--full-regression",
        action="store_true",
        help="Explicitly run the full slow pytest suite",
    )

    parser.add_argument(
        "--cases-per-family",
        type=int,
        default=2048,
        help="Default 2048 x 4 = 8192 toy cases",
    )

    args = parser.parse_args(argv)

    if not 1 <= args.cases_per_family <= 16384:
        parser.error(
            "cases-per-family must be 1 to 16384"
        )

    if BASE.is_symlink():
        raise SystemExit("UNSAFE_OUTPUT_BASE")

    BASE.mkdir(
        parents=True, exist_ok=True
    )

    rid = (
        datetime.now(timezone.utc).strftime(
            "g2big_%Y%m%dT%H%M%SZ_"
        )
        + secrets.token_hex(4)
    )

    out = BASE / rid
    out.mkdir(mode=0o700)

    print("BROAD_RUN=" + rid, flush=True)
    print("RUN_DIR=" + str(out), flush=True)
    print(
        "FULL_REGRESSION_POLICY="
        + (
            "OPTED_IN"
            if args.full_regression
            else "SKIPPED_DEFAULT"
        ),
        flush=True,
    )

    steps, runs, errors = [], {}, []
    stress_result = None

    try:
        for rel, wanted in SOURCE_SHA.items():
            p = ROOT / rel

            if (
                not p.is_file()
                or p.is_symlink()
                or sha(p) != wanted
            ):
                raise RuntimeError(
                    "SOURCE_SHA_HOLD:" + rel
                )

        save(
            out / "source_locks.json",
            {
                **SOURCE_SHA,
                "scripts/gravity2_big_scoped_v1.py":
                    sha(Path(__file__)),
            },
        )

        call(
            out, steps, "focused_tests",
            [
                "-m", "pytest", "-q",
                "tests/gravity2/test_campaign_v2.py",
                "tests/gravity2/test_campaign_v3.py",
                "tests/gravity2/test_campaign_v4.py",
                "tests/gravity2/test_campaign_v5.py",
                "tests/gravity2/test_registry_v6.py",
                "tests/gravity2/test_research_v8.py",
            ],
        )

        call(
            out, steps, "registry_audit",
            [
                "-m",
                "antigravity_research.gravity2.registry_v6",
                "audit",
            ],
        )

        historical = (
            (
                "historical_v4_fresh",
                "campaign_v4",
                "g2camp4_20261121T184146Z_73cb7751",
            ),
            (
                "historical_v4_cache",
                "campaign_v4",
                "g2camp4_20261121T184153Z_05423ae3",
            ),
            (
                "historical_v5_recovered",
                "campaign_v5",
                "g2camp5_20261121T195147Z_adec6224",
            ),
        )

        for label, module, rid in historical:
            call(
                out, steps, label,
                [
                    "-m",
                    "antigravity_research.gravity2."
                    + module,
                    "verify",
                    "--run-id", rid,
                ],
            )

        print(
            "\n=== MATHEMATICAL RESPONSE STRESS ===",
            flush=True,
        )

        stress_result = stress(
            out, args.cases_per_family
        )

        f0_inventory(out)

        v5text = call(
            out, steps, "fresh_v5",
            [
                "-m",
                "antigravity_research.gravity2.campaign_v5",
                "run",
                "--level", "L1",
                "--preset", "short",
                "--minutes", "2",
                "--workers", "1",
            ],
        )

        runs["v5"] = run_id(
            v5text,
            r"^GRAVITY2_CHECKPOINT_V5_RUN=(g2camp5_[^\s]+)$",
            "v5",
        )

        v8text = call(
            out, steps, "fresh_v8",
            [
                "-m",
                "antigravity_research.gravity2.research_v8",
                "run",
            ],
        )

        runs["v8"] = run_id(
            v8text,
            r"^GRAVITY2_V8_RUN=(g2research8_[^\s]+)$",
            "v8",
        )

        call(
            out, steps, "verify_v5",
            [
                "-m",
                "antigravity_research.gravity2.campaign_v5",
                "verify",
                "--run-id", runs["v5"],
            ],
        )

        call(
            out, steps, "verify_v8",
            [
                "-m",
                "antigravity_research.gravity2.research_v8",
                "verify",
                "--run-id", runs["v8"],
            ],
        )

        evidence(
            out, "v5",
            "results/gravity2/campaign_v5_runs",
            runs["v5"],
        )

        evidence(
            out, "v8",
            "results/gravity2/research_v8_runs",
            runs["v8"],
        )

        if args.full_regression:
            call(
                out, steps,
                "full_repository_regression",
                ["-m", "pytest", "-q"],
            )
        else:
            print(
                "FULL_REPOSITORY_REGRESSION="
                "SKIPPED_BY_DEFAULT",
                flush=True,
            )

    except BaseException as error:
        traceback.print_exc()
        errors.append(repr(error))

    finally:
        finish(
            out, steps, runs,
            stress_result, errors,
            args.full_regression,
        )

    return 3 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
