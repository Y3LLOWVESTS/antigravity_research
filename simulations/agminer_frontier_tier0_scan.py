"""AGMINER multi-family Tier-0 frontier campaign.

This scanner discovers implemented theory-family plugins dynamically.
It performs cheap theory, naturalness, EFT, and energy-lower-bound gates.
It does not certify antigravity and does not perform expensive field solves.
"""

from __future__ import annotations

import argparse
import importlib
import inspect
import json
import math
import pkgutil
from numbers import Number
from pathlib import Path
from typing import Any

from antigravity_research.agminer.candidate import Candidate
from antigravity_research.agminer.control import StopController
from antigravity_research.agminer.energy import hard_energy_gate
from antigravity_research.agminer.policy import current_energy_policy
from antigravity_research.agminer.sampler import SobolSampler
from antigravity_research.agminer.storage import Storage
import antigravity_research.agminer.families as families_package


SCANNER_VERSION = "FRONTIER_TIER0_V1"

SKIP_MODULE_PARTS = (
    "base",
    "mock",
    "031_control",
)

REQUIRED_TIER0_METHODS = (
    "sample_bounds",
    "analytic_precheck",
    "energy_lower_bound",
    "naturalness_precheck",
    "eft_precheck",
)


def scalar_attribute(
    obj: Any,
    name: str,
    fallback: str,
) -> str:
    value = getattr(obj, name, None)

    if value is None:
        return fallback

    if callable(value):
        try:
            value = value()
        except TypeError:
            return fallback

    return str(value)


def invoke(
    obj: Any,
    name: str,
    params: dict[str, float],
    config: dict[str, Any],
) -> Any:
    function = getattr(obj, name)
    signature = inspect.signature(function)

    positional = [
        parameter
        for parameter in signature.parameters.values()
        if parameter.kind in (
            inspect.Parameter.POSITIONAL_ONLY,
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
        )
    ]

    if len(positional) <= 1:
        return function(params)

    return function(params, config)


def gate_status(value: Any) -> tuple[bool | None, str | None]:
    if value is None:
        return None, None

    if isinstance(value, bool):
        return value, None

    if isinstance(value, dict):
        for key in ("passed", "pass", "ok", "valid"):
            if key in value:
                code = value.get("failure_code")
                return bool(value[key]), None if code is None else str(code)

        boolean_values = [
            item
            for item in value.values()
            if isinstance(item, bool)
        ]

        if boolean_values and len(boolean_values) == len(value):
            return all(boolean_values), None

        if value.get("failure_code") is not None:
            return False, str(value["failure_code"])

        return None, None

    if isinstance(value, (tuple, list)) and value:
        if isinstance(value[0], bool):
            code = None
            if len(value) > 1 and value[1] is not None:
                code = str(value[1])
            return bool(value[0]), code

    for key in ("passed", "ok", "valid"):
        if hasattr(value, key):
            passed = bool(getattr(value, key))
            code = getattr(value, "failure_code", None)
            return passed, None if code is None else str(code)

    return None, None


def extract_energy_j(value: Any) -> float | None:
    if isinstance(value, Number) and not isinstance(value, bool):
        result = float(value)
        return result if math.isfinite(result) else None

    if isinstance(value, dict):
        for key in (
            "energy_lower_bound_j",
            "lower_bound_j",
            "lower_j",
            "energy_j",
            "value_j",
        ):
            if key in value and value[key] is not None:
                try:
                    result = float(value[key])
                except (TypeError, ValueError):
                    continue
                if math.isfinite(result):
                    return result

    for key in (
        "energy_lower_bound_j",
        "lower_bound_j",
        "lower_j",
        "energy_j",
        "value_j",
    ):
        if hasattr(value, key):
            try:
                result = float(getattr(value, key))
            except (TypeError, ValueError):
                continue
            if math.isfinite(result):
                return result

    return None


def normalized_bounds(raw: Any) -> dict[str, tuple[float, float]]:
    if not isinstance(raw, dict):
        raise ValueError("sample_bounds must return a dictionary")

    result: dict[str, tuple[float, float]] = {}

    for name, value in raw.items():
        low = None
        high = None

        if isinstance(value, (tuple, list)) and len(value) == 2:
            low = value[0]
            high = value[1]
        elif isinstance(value, dict):
            low = value.get("low", value.get("min"))
            high = value.get("high", value.get("max"))

        if low is None or high is None:
            raise ValueError("invalid bound for " + str(name))

        low_f = float(low)
        high_f = float(high)

        if not math.isfinite(low_f) or not math.isfinite(high_f):
            raise ValueError("nonfinite bound for " + str(name))

        if high_f <= low_f:
            raise ValueError("reversed bound for " + str(name))

        result[str(name)] = (low_f, high_f)

    if not result:
        raise ValueError("empty parameter domain")

    return result


def plugin_objects() -> list[tuple[str, Any]]:
    discovered: list[tuple[str, Any]] = []

    for info in pkgutil.iter_modules(families_package.__path__):
        module_name = info.name

        if not module_name.startswith("family_"):
            continue

        if any(part in module_name for part in SKIP_MODULE_PARTS):
            continue

        module = importlib.import_module(
            families_package.__name__ + "." + module_name
        )

        module_candidates: list[Any] = []

        for _, candidate_class in inspect.getmembers(
            module,
            inspect.isclass,
        ):
            if candidate_class.__module__ != module.__name__:
                continue

            try:
                candidate_object = candidate_class()
            except Exception:
                continue

            if all(
                callable(getattr(candidate_object, method, None))
                for method in REQUIRED_TIER0_METHODS
            ):
                module_candidates.append(candidate_object)

        if not module_candidates:
            if all(
                callable(getattr(module, method, None))
                for method in REQUIRED_TIER0_METHODS
            ):
                module_candidates.append(module)

        for candidate_object in module_candidates:
            discovered.append((module_name, candidate_object))

    return discovered


def set_model_state(
    storage: Storage,
    candidate_id: str,
    state: str,
    energy_j: float | None = None,
) -> None:
    if energy_j is None:
        storage.connection.execute(
            "UPDATE models SET state=?, tier=0 WHERE candidate_id=?",
            (state, candidate_id),
        )
    else:
        storage.connection.execute(
            "UPDATE models SET state=?, tier=0, energy_j=? WHERE candidate_id=?",
            (state, float(energy_j), candidate_id),
        )

    storage.connection.commit()


def reject(
    storage: Storage,
    candidate: Candidate,
    state: str,
    failure_code: str,
    gate: str,
    energy_j: float | None,
    run_id: str,
) -> None:
    storage.reject(
        candidate.candidate_id,
        state=state,
        failure_code=failure_code,
        gate=gate,
        energy_j=energy_j,
        run_id=run_id,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    parser.add_argument("--budget-per-family", type=int, default=20000)
    parser.add_argument("--audit-only", action="store_true")
    parser.add_argument("--include-family", action="append", default=[])
    arguments = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    config_path = root / "config" / "agminer_032a.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    policy = current_energy_policy()

    plugins = plugin_objects()

    print("=== AGMINER FRONTIER PLUGIN AUDIT ===")
    print("POLICY_ID=" + str(policy["policy_id"]))
    print("ENERGY_TARGET_J=" + str(policy["limit_j_text"]))
    print("COMPARISON=" + str(policy["comparison"]))
    print("DISCOVERED_FRONTIER_PLUGINS=" + str(len(plugins)))

    audited: list[tuple[str, Any, str, str, dict[str, tuple[float, float]]]] = []

    for module_name, plugin in plugins:
        family_id = scalar_attribute(
            plugin,
            "family_id",
            module_name,
        )
        family_version = scalar_attribute(
            plugin,
            "family_version",
            "1",
        )

        try:
            bounds = normalized_bounds(plugin.sample_bounds())
        except Exception as error:
            print(
                "PLUGIN_SKIP module="
                + module_name
                + " family="
                + family_id
                + " reason=INVALID_BOUNDS detail="
                + type(error).__name__
            )
            continue

        print(
            "PLUGIN_READY module="
            + module_name
            + " family="
            + family_id
            + " version="
            + family_version
            + " dimensions="
            + str(len(bounds))
        )

        audited.append(
            (
                module_name,
                plugin,
                family_id,
                family_version,
                bounds,
            )
        )

    if arguments.include_family:
        selected = set(arguments.include_family)
        audited = [row for row in audited if row[2] in selected]
        print("SELECTED_FRONTIER_PLUGINS=" + str(len(audited)))

    print("AUDITED_FRONTIER_PLUGINS=" + str(len(audited)))

    if arguments.audit_only:
        return

    if not audited:
        print("AGMINER_SCAN=NO_FRONTIER_PLUGIN_READY")
        print("SCIENTIFIC_DISCOVERY_CLAIM=NONE")
        return

    storage = Storage(Path(arguments.db))
    storage.clear_stop()

    controller = StopController(storage)

    def signal_callback() -> None:
        storage.set_metadata("frontier_stop_source", "signal")
        print("AGMINER_SIGNAL_STOP=REQUESTED", flush=True)

    controller.install_signal_handlers(signal_callback)

    run_id = (
        "FRONTIER_TIER0_"
        + str(__import__("time").time_ns())
    )

    storage.start_run(
        run_id=run_id,
        family="MULTI_FAMILY_FRONTIER_TIER0",
        family_version=SCANNER_VERSION,
        config_fingerprint=str(policy["policy_id"]),
        sampler_seed=int(config.get("sampler_seed", 3201)),
    )

    physical_model_version = str(
        config.get(
            "physical_model_version",
            "032A_INFRASTRUCTURE_ONLY",
        )
    )

    ledger_version = str(
        config.get(
            "energy_ledger_version",
            "CONSERVATIVE_COMPLETE_V1",
        )
    )

    total_evaluated = 0
    total_known_skips = 0
    total_survivors = 0
    total_unresolved = 0
    family_summaries: list[dict[str, Any]] = []
    survivor_records: list[dict[str, Any]] = []
    stopped = False

    for (
        module_name,
        plugin,
        family_id,
        family_version,
        bounds,
    ) in audited:
        if controller.requested():
            stopped = True
            break

        metadata_key = (
            "frontier_index:"
            + family_id
            + ":"
            + family_version
            + ":"
            + str(policy["policy_id"])
        )

        start_index = int(
            storage.get_metadata(metadata_key, "0")
        )

        sampler = SobolSampler(
            bounds,
            index=start_index,
        )

        samples = sampler.sample(arguments.budget_per_family)

        counts = {
            "evaluated": 0,
            "known_skips": 0,
            "analytic_fail": 0,
            "naturalness_fail": 0,
            "eft_fail": 0,
            "energy_fail": 0,
            "unresolved": 0,
            "headroom_only": 0,
            "tier0_survivors": 0,
        }

        print("")
        print(
            "=== FAMILY_START "
            + family_id
            + " version="
            + family_version
            + " start_index="
            + str(start_index)
            + " budget="
            + str(arguments.budget_per_family)
            + " ==="
        )

        for offset, raw_params in enumerate(samples):
            if controller.requested():
                stopped = True
                break

            current_index = start_index + offset

            params = {
                str(key): float(value)
                for key, value in raw_params.items()
            }

            canonicalizer = getattr(
                plugin,
                "canonicalize_params",
                None,
            )

            if callable(canonicalizer):
                try:
                    params = canonicalizer(params)
                except Exception:
                    counts["unresolved"] += 1
                    total_unresolved += 1
                    storage.set_metadata(
                        metadata_key,
                        str(current_index + 1),
                    )
                    continue

            candidate = Candidate(
                family_id=family_id,
                family_version=family_version,
                params=params,
                physical_model_version=physical_model_version,
                energy_ledger_version=ledger_version,
            )

            existing_state = storage.candidate_state(
                candidate.candidate_id
            )

            if storage.is_terminal(candidate.candidate_id):
                counts["known_skips"] += 1
                total_known_skips += 1
                storage.set_metadata(
                    metadata_key,
                    str(current_index + 1),
                )
                continue

            if existing_state == "TIER0_SURVIVOR":
                counts["known_skips"] += 1
                total_known_skips += 1
                storage.set_metadata(
                    metadata_key,
                    str(current_index + 1),
                )
                continue

            storage.record_candidate(
                candidate,
                state="TIER0_RUNNING",
                tier=0,
                run_id=run_id,
            )

            counts["evaluated"] += 1
            total_evaluated += 1

            try:
                analytic_result = invoke(
                    plugin,
                    "analytic_precheck",
                    params,
                    config,
                )
                analytic_pass, analytic_code = gate_status(
                    analytic_result
                )
            except Exception:
                analytic_pass = None
                analytic_code = None

            if analytic_pass is False:
                reject(
                    storage,
                    candidate,
                    "REJECTED_ANALYTIC_PREFLIGHT",
                    analytic_code or "T000",
                    "analytic_precheck",
                    None,
                    run_id,
                )
                counts["analytic_fail"] += 1
                storage.set_metadata(metadata_key, str(current_index + 1))
                continue

            if analytic_pass is None:
                set_model_state(
                    storage,
                    candidate.candidate_id,
                    "TIER0_UNRESOLVED_ANALYTIC",
                )
                counts["unresolved"] += 1
                total_unresolved += 1
                storage.set_metadata(metadata_key, str(current_index + 1))
                continue

            try:
                naturalness_result = invoke(
                    plugin,
                    "naturalness_precheck",
                    params,
                    config,
                )
                naturalness_pass, naturalness_code = gate_status(
                    naturalness_result
                )
            except Exception:
                naturalness_pass = None
                naturalness_code = None

            if naturalness_pass is False:
                reject(
                    storage,
                    candidate,
                    "REJECTED_NATURALNESS",
                    naturalness_code or "N003",
                    "naturalness",
                    None,
                    run_id,
                )
                counts["naturalness_fail"] += 1
                storage.set_metadata(metadata_key, str(current_index + 1))
                continue

            if naturalness_pass is None:
                set_model_state(
                    storage,
                    candidate.candidate_id,
                    "TIER0_UNRESOLVED_NATURALNESS",
                )
                counts["unresolved"] += 1
                total_unresolved += 1
                storage.set_metadata(metadata_key, str(current_index + 1))
                continue

            try:
                eft_result = invoke(
                    plugin,
                    "eft_precheck",
                    params,
                    config,
                )
                eft_pass, eft_code = gate_status(eft_result)
            except Exception:
                eft_pass = None
                eft_code = None

            if eft_pass is False:
                reject(
                    storage,
                    candidate,
                    "REJECTED_EFT",
                    eft_code or "T001",
                    "eft",
                    None,
                    run_id,
                )
                counts["eft_fail"] += 1
                storage.set_metadata(metadata_key, str(current_index + 1))
                continue

            if eft_pass is None:
                set_model_state(
                    storage,
                    candidate.candidate_id,
                    "TIER0_UNRESOLVED_EFT",
                )
                counts["unresolved"] += 1
                total_unresolved += 1
                storage.set_metadata(metadata_key, str(current_index + 1))
                continue

            try:
                energy_result = invoke(
                    plugin,
                    "energy_lower_bound",
                    params,
                    config,
                )
                energy_lower_j = extract_energy_j(energy_result)
            except Exception:
                energy_lower_j = None

            if energy_lower_j is None or energy_lower_j < 0.0:
                set_model_state(
                    storage,
                    candidate.candidate_id,
                    "TIER0_UNRESOLVED_ENERGY_BOUND",
                )
                counts["unresolved"] += 1
                total_unresolved += 1
                storage.set_metadata(metadata_key, str(current_index + 1))
                continue

            energy_decision = hard_energy_gate(
                energy_lower_j,
                lower_j=energy_lower_j,
                reliable_estimate=False,
            )

            if not energy_decision.passed:
                reject(
                    storage,
                    candidate,
                    str(energy_decision.state),
                    str(energy_decision.failure_code),
                    "analytic_energy_lower_bound",
                    energy_lower_j,
                    run_id,
                )
                counts["energy_fail"] += 1
                storage.set_metadata(metadata_key, str(current_index + 1))
                continue

            energy_scope = str(
                getattr(
                    plugin,
                    "energy_bound_scope",
                    "UNDECLARED",
                )
            )

            if energy_scope == "PARTIAL_REJECTION_ONLY" or energy_scope == "UNDECLARED":
                set_model_state(
                    storage,
                    candidate.candidate_id,
                    "TIER0_HEADROOM_ONLY_INCOMPLETE_LEDGER",
                    energy_lower_j,
                )
                counts["headroom_only"] += 1
                storage.set_metadata(
                    metadata_key,
                    str(current_index + 1),
                )
                continue

            if energy_scope == "COMPLETE_OPERATING_LOWER_BOUND":
                set_model_state(
                    storage,
                    candidate.candidate_id,
                    "TIER0_ELIGIBLE_LOWER_BOUND",
                    energy_lower_j,
                )
                counts["tier0_survivors"] += 1
                total_survivors += 1
                survivor_records.append(
                    {
                        "candidate_id": candidate.candidate_id,
                        "family_id": family_id,
                        "family_version": family_version,
                        "energy_lower_bound_j": energy_lower_j,
                        "params": params,
                    }
                )
                storage.set_metadata(
                    metadata_key,
                    str(current_index + 1),
                )
                continue

            set_model_state(
                storage,
                candidate.candidate_id,
                "TIER0_SURVIVOR",
                energy_lower_j,
            )

            counts["tier0_survivors"] += 1
            total_survivors += 1

            survivor_records.append(
                {
                    "candidate_id": candidate.candidate_id,
                    "family_id": family_id,
                    "family_version": family_version,
                    "energy_lower_bound_j": energy_lower_j,
                    "params": params,
                }
            )

            storage.set_metadata(
                metadata_key,
                str(current_index + 1),
            )

            if (offset + 1) % 1000 == 0:
                print(
                    "PROGRESS family="
                    + family_id
                    + " processed="
                    + str(offset + 1)
                    + " survivors="
                    + str(counts["tier0_survivors"])
                    + " energy_fail="
                    + str(counts["energy_fail"])
                    + " naturalness_fail="
                    + str(counts["naturalness_fail"])
                    + " unresolved="
                    + str(counts["unresolved"]),
                    flush=True,
                )

        family_summaries.append(
            {
                "module": module_name,
                "family_id": family_id,
                "family_version": family_version,
                "start_index": start_index,
                "next_index": int(
                    storage.get_metadata(metadata_key, str(start_index))
                ),
                **counts,
            }
        )

        print(
            "FAMILY_DONE family="
            + family_id
            + " evaluated="
            + str(counts["evaluated"])
            + " survivors="
            + str(counts["tier0_survivors"])
            + " analytic_fail="
            + str(counts["analytic_fail"])
            + " naturalness_fail="
            + str(counts["naturalness_fail"])
            + " eft_fail="
            + str(counts["eft_fail"])
            + " energy_fail="
            + str(counts["energy_fail"])
            + " unresolved="
            + str(counts["unresolved"])
        )

        if stopped:
            break

    survivors_sorted = sorted(
        survivor_records,
        key=lambda row: row["energy_lower_bound_j"],
    )

    summary = {
        "run_id": run_id,
        "scanner_version": SCANNER_VERSION,
        "policy_id": str(policy["policy_id"]),
        "energy_target_j": float(policy["limit_j"]),
        "comparison": str(policy["comparison"]),
        "budget_per_family": arguments.budget_per_family,
        "frontier_plugins": len(audited),
        "evaluated": total_evaluated,
        "known_skips": total_known_skips,
        "tier0_survivors": total_survivors,
        "unresolved": total_unresolved,
        "stopped": stopped,
        "family_summaries": family_summaries,
        "best_tier0_survivors": survivors_sorted[:25],
        "claim": (
            "TIER0_SCREENING_ONLY_NOT_FIELD_SOLUTION_NOT_CERTIFICATION"
        ),
    }

    output = (
        root
        / "results"
        / "agminer"
        / "frontier_tier0_summary.json"
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    storage.finish_run(
        run_id,
        status="STOPPED" if stopped else "COMPLETED",
    )
    storage.checkpoint_wal()
    storage.close()

    print("")
    print("=== AGMINER FRONTIER TIER-0 SUMMARY ===")
    print("RUN_ID=" + run_id)
    print("FRONTIER_PLUGINS=" + str(len(audited)))
    print("EVALUATED=" + str(total_evaluated))
    print("KNOWN_SKIPS=" + str(total_known_skips))
    print("TIER0_SURVIVORS=" + str(total_survivors))
    print("UNRESOLVED=" + str(total_unresolved))
    print("STOPPED=" + str(stopped))

    if survivors_sorted:
        best = survivors_sorted[0]
        print("BEST_TIER0_FAMILY=" + str(best["family_id"]))
        print("BEST_TIER0_CANDIDATE=" + str(best["candidate_id"]))
        print(
            "BEST_ANALYTIC_ENERGY_LOWER_BOUND_J="
            + format(best["energy_lower_bound_j"], ".12e")
        )
    else:
        print("BEST_TIER0_CANDIDATE=NONE")

    print("SCIENTIFIC_CLAIM=TIER0_SCREENING_ONLY")
    print("SUB10MJ_TIER0_SURVIVOR_IS_CERTIFIED_ANTIGRAVITY=NO")


if __name__ == "__main__":
    main()
