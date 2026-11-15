"""PH7 executor: one timestamped result and read-only provenance checks."""

from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import sys

from antigravity_research.agminer import (
    hook17_ph7_noether_spectral_health as ph7
)


def main():
    root = Path.cwd()
    result = ph7.run(root)
    now = datetime.now(timezone.utc)

    result["execution"] = {
        "utc": now.isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "source_sha256": sha256(
            Path(ph7.__file__).read_bytes()
        ).hexdigest(),
        "simulation_sha256": sha256(
            Path(__file__).read_bytes()
        ).hexdigest(),
    }

    target = root/"results/data"/(
        "032h17_ph7_noether_spectral_health_"
        + now.strftime("%Y%m%dT%H%M%S%fZ")
        + ".json"
    )

    target.parent.mkdir(parents=True, exist_ok=True)

    with target.open("x", encoding="utf-8") as stream:
        json.dump(
            result,
            stream,
            sort_keys=True,
            indent=2,
            allow_nan=False,
        )
        stream.write("\n")

    print("RUN=" + result["branch"])

    print(
        "P0_PROVENANCE="
        + result["gates"]["P0_PH6_PROVENANCE"]
    )

    print(
        "JOINT_KINETIC_COUNTEREXAMPLE="
        + str(result["kinetic_counterexample"])
    )

    for label, row in result["spectral_resolution_series"].items():
        print(
            "CASE=" + label
            + " NEUTRAL_DP="
            + str(row["neutral_signed_momentum_change"])
            + " ENERGY_DRIFT="
            + str(row["max_energy_drift"])
            + " MOMENTUM_DRIFT="
            + str(row["max_momentum_drift"])
            + " FULL_S_MIN="
            + str(row["min_full_S"])
        )

    for label, row in result["independent_controls"].items():
        print(
            "CONTROL=" + label
            + " NEUTRAL_DP="
            + str(row["neutral_signed_momentum_change"])
        )

    for label, value in result[
        "negative_even_coarse_grid_erratum"
    ].items():
        print(
            "NEGATIVE_EVEN_ERRATUM="
            + label
            + " DP=" + str(value)
        )

    print("PH7_VERDICT=" + result["verdict"])
    print("FULL_B11_M6=NOT_RUN")
    print("WHOLE_SPACECRAFT_LIFT=NOT_DERIVED")
    print("STRICT_COMPLETE_LT10MJ=NOT_CERTIFIED")
    print("JSON=" + str(target))

    return (
        0 if result["gates"]["P0_PH6_PROVENANCE"] == "PASS"
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(main())
