"""PH1 analytic run. Historic source/results are read-only.

Run from repository root with PYTHONPATH=src.
Creates one timestamped JSON result, never overwriting an old result.
Not a complete source-driven physical action or propulsion simulation.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import platform
import sys

from antigravity_research.agminer.hook17_ph1_physicalization_preflight import (
    run_preflight, sha_file
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args()
    root = args.root.resolve()

    result = run_preflight(root)
    result["execution"] = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "physical_module_sha256": sha_file(
            Path(
                sys.modules[
                    "antigravity_research.agminer."
                    "hook17_ph1_physicalization_preflight"
                ].__file__
            )
        ),
        "execution_repo": str(root),
    }

    out = args.out
    if out is None:
        stamp = datetime.now(timezone.utc).strftime(
            "%Y%m%dT%H%M%S%fZ"
        )
        out = root/"results/data"/f"032h17_ph1_preflight_{stamp}.json"

    out = out.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("x", encoding="utf-8") as f:
        json.dump(result, f, indent=2, sort_keys=True, allow_nan=False)
        f.write("\n")

    print("RUN=" + result["branch"])
    print("EXACT_CHECKS=" + str(result["analytic_check_count"]))
    print("PH1_VERDICT=" + result["verdict"])
    print(
        "P0_ARCHIVAL="
        + result["gates"]["PH1_P0_HISTORICAL_REFERENCE_PROVENANCE"]
    )
    print("B11_M6_FULL_RUN=NOT_RUN")
    print("PHYSICAL_WHOLE_CRAFT_LIFT=NOT_DERIVED")
    print("JSON=" + str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
