"""ALPHA-1R5 / B17-M5J: source-to-solver contract audit.

Reproduce the historical R3B on-shell interactions and extract the
current live solver source interfaces before attempting to deposit
the new M5I continuum current into the coupled operator.

No M5I source is coupled here. Historical code is not modified.
No metric force, Noether identity or operating energy is certified.
"""

from __future__ import annotations

import argparse
import importlib
import inspect
import json
import math
from pathlib import Path

import numpy as np


BRANCH = "032H17A12D1R3X3B17-ALPHA1R5-M5J"

REQUIRED = (
    (
        "hook17_r3b_m4b1_source_recovery",
        "assemble_original_aligned_source",
    ),
    (
        "hook17_r3b_m5b_compact_transfer",
        "compact_shaped_source",
    ),
    (
        "hook17_r3b_m4b4_paired_translation",
        "pair_action",
    ),
    (
        "hook17_r3b_m4b4_paired_translation",
        "source_support_check",
    ),
    (
        "hook17_r3b_m5i_continuum_source",
        "continuum_current",
    ),
    (
        "hook17_r3b_m5i_continuum_source",
        "deposit",
    ),
)

OPTIONAL = (
    (
        "hook17_r3b_m4b_sparse_earth_loading",
        "_solve_fixed_sources",
    ),
    (
        "hook17_r3b_m4b_sparse_earth_loading",
        "_on_shell_action",
    ),
    (
        "hook17_r3b_m4b_sparse_earth_loading",
        "_weights",
    ),
    (
        "hook17_r3b_m4b4_paired_translation",
        "shifted_source",
    ),
    (
        "hook17_r3b_m4b4_paired_translation",
        "shifted_material",
    ),
)


def describe(value):
    if isinstance(value, np.ndarray):
        result = {
            "type": "ndarray",
            "shape": list(value.shape),
            "dtype": str(value.dtype),
        }

        if value.dtype.kind in "iufc":
            result["finite"] = bool(
                np.all(np.isfinite(value))
            )
            result["nonzero_count"] = int(
                np.count_nonzero(value)
            )

        return result

    if isinstance(
        value,
        (int, float, str, bool, type(None)),
    ):
        return {
            "type": type(value).__name__,
            "value": value,
        }

    if isinstance(value, dict):
        return {
            "type": "dict",
            "keys": sorted(map(str, value.keys())),
        }

    if isinstance(value, (list, tuple)):
        return {
            "type": type(value).__name__,
            "length": len(value),
        }

    return {
        "type": type(value).__name__,
        "class_module": type(value).__module__,
    }


def function_contract(module_name, method, parts):
    source = inspect.getsource(method)

    name = f"{module_name}.{method.__name__}"

    parts.append(
        "\n"
        + "=" * 78
        + "\n"
        + name
        + "\n"
        + "=" * 78
        + "\n"
        + source
    )

    return {
        "name": name,
        "signature": str(
            inspect.signature(method)
        ),
        "file": inspect.getsourcefile(method),
        "source_line_count": len(
            source.splitlines()
        ),
    }


def evaluate(m5d_paths, m5i_path, source_output):
    m5i = json.loads(
        Path(m5i_path).read_text(
            encoding="utf-8"
        )
    )

    if (
        m5i.get("branch")
        != "032H17A12D1R3X3B17-ALPHA1R4-M5I"
        or not all(
            m5i["diagnostic_gates"].values()
        )
    ):
        raise ValueError(
            "M5I source preflight did not pass"
        )

    prefix = "antigravity_research.agminer."

    parts = [
        "ALPHA-1R5/M5J SOURCE-TO-SOLVER CONTRACT",
        "Read-only extraction from the live research implementation.",
        "These functions are evidence for constructing a compatible",
        "source adapter, not a physical certification.",
    ]

    contracts = {}
    missing_optional = []

    for module_name, symbol in REQUIRED + OPTIONAL:
        try:
            module = importlib.import_module(
                prefix + module_name
            )

            method = getattr(module, symbol)

            contracts[
                f"{module_name}.{symbol}"
            ] = function_contract(
                module_name,
                method,
                parts,
            )

        except (
            ImportError,
            AttributeError,
            OSError,
            TypeError,
        ) as exc:
            if (
                module_name,
                symbol,
            ) in REQUIRED:
                raise RuntimeError(
                    "Missing required API: "
                    f"{module_name}.{symbol}"
                ) from exc

            missing_optional.append({
                "module": module_name,
                "symbol": symbol,
                "error": str(exc),
            })

    m4b1 = importlib.import_module(
        prefix
        + "hook17_r3b_m4b1_source_recovery"
    )

    m5b = importlib.import_module(
        prefix
        + "hook17_r3b_m5b_compact_transfer"
    )

    paired = importlib.import_module(
        prefix
        + "hook17_r3b_m4b4_paired_translation"
    )

    continuum = importlib.import_module(
        prefix
        + "hook17_r3b_m5i_continuum_source"
    )

    deposited = continuum.deposit(
        continuum.SourceSpec(),
        0.25,
        4,
    )

    deposit_has_rhs = any(
        isinstance(value, np.ndarray)
        for value in deposited.values()
    )

    historical = {}

    for label, h in (
        ("h0.25", 0.25),
        ("h0.2", 0.2),
    ):
        old = json.loads(
            Path(m5d_paths[label]).read_text(
                encoding="utf-8"
            )
        )

        if (
            old.get("branch")
            != "032H17A12D1R3X3B17-M5D"
            or abs(old["h_m"] - h) > 1e-12
            or abs(old["source_bias"]) > 1e-12
            or bool(old["magnetic_reversed"])
        ):
            raise ValueError(
                "M5D reference mismatch: "
                + label
            )

        source, audit = m5b.compact_shaped_source(
            m4b1.assemble_original_aligned_source(h),
            0.0,
        )

        state = paired.pair_action(
            source,
            21147.0,
            0.0,
            0.0,
        )

        loaded = float(
            state["loaded"]["action_j"]
        )

        free = float(
            state["air_only"]["action_j"]
        )

        center = next(
            row
            for row in old[
                "common_shift_phase_samples"
            ]
            if abs(row["shift_m"]) < 1e-12
        )

        error = max(
            abs(
                loaded
                - center["earth_present_action_j"]
            ),
            abs(
                free
                - center["earth_absent_action_j"]
            ),
            abs(
                (loaded - free)
                - center["interaction_action_j"]
            ),
        )

        if (
            not math.isfinite(error)
            or error > 1e-6
        ):
            raise ArithmeticError(
                "Historical on-shell action changed: "
                + label
            )

        historical[label] = {
            "grid_m": h,
            "M5D_reproduction_max_error_j":
                error,
            "earth_present_action_j":
                loaded,
            "earth_absent_action_j":
                free,
            "interaction_action_j":
                loaded - free,
            "source_layout": {
                str(k): describe(v)
                for k, v in sorted(
                    source.items()
                )
            },
            "source_audit_keys":
                sorted(
                    map(
                        str,
                        audit.keys(),
                    )
                ),
            "M5I_source_was_used":
                False,
        }

    result = {
        "branch": BRANCH,
        "scope":
            "SOLVER_INTERFACE_AND_HISTORICAL_ACTION_REPRODUCTION",
        "M5I_continuum_source_preflight_passed":
            True,
        "M5I_deposition_return_keys":
            sorted(deposited.keys()),
        "M5I_deposition_exposes_nodal_rhs_arrays":
            deposit_has_rhs,
        "solver_function_contracts":
            contracts,
        "optional_interfaces_unavailable":
            missing_optional,
        "historical_reproduction":
            historical,
        "M5I_continuum_source_coupled_to_R3B":
            False,
        "dual_mesh_source_normalization_certified":
            False,
        "same_action_source_Ward_identity_certified":
            False,
        "physical_source_energy_certified":
            False,
        "exterior_metric_transmission_derived":
            False,
        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
        "006d_replaced": False,
    }

    source_output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    source_output.write_text(
        "\n".join(parts) + "\n",
        encoding="utf-8",
    )

    return result


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--m5d-h025",
        required=True,
        type=Path,
    )

    parser.add_argument(
        "--m5d-h020",
        required=True,
        type=Path,
    )

    parser.add_argument(
        "--m5i",
        required=True,
        type=Path,
    )

    parser.add_argument(
        "--output",
        required=True,
        type=Path,
    )

    parser.add_argument(
        "--interface-source",
        required=True,
        type=Path,
    )

    args = parser.parse_args()

    result = evaluate(
        {
            "h0.25": args.m5d_h025,
            "h0.2": args.m5d_h020,
        },
        args.m5i,
        args.interface_source,
    )

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    args.output.write_text(
        json.dumps(
            result,
            indent=2,
            allow_nan=False,
        ) + "\n",
        encoding="utf-8",
    )

    print(json.dumps({
        "branch": result["branch"],
        "M5I_source_preflight": "PASS",
        "M5I_exposes_solver_RHS":
            result[
                "M5I_deposition_exposes_nodal_rhs_arrays"
            ],
        "historical_reproduction_errors_j": {
            k: v["M5D_reproduction_max_error_j"]
            for k, v in result[
                "historical_reproduction"
            ].items()
        },
        "required_solver_contracts":
            len(REQUIRED),
        "optional_interfaces_unavailable":
            result[
                "optional_interfaces_unavailable"
            ],
        "M5I_source_coupled": False,
        "whole_craft_force_n": None,
        "complete_operating_energy_j": None,
    }, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
