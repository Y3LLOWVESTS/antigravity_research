"""PH6 executor. Save a uniquely timestamped scientific result."""
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import json
import platform
import sys

from antigravity_research.agminer import (
    hook17_ph6_same_action_bridge as ph6
)


def main():
    root = Path.cwd()
    result = ph6.run(root)
    now = datetime.now(timezone.utc)

    result["execution"] = {
        "utc": now.isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "source_sha256": sha256(
            Path(ph6.__file__).read_bytes()
        ).hexdigest(),
        "sim_sha256": sha256(
            Path(__file__).read_bytes()
        ).hexdigest(),
    }

    path = root/"results/data"/(
        "032h17_ph6_same_action_bridge_"
        + now.strftime("%Y%m%dT%H%M%S%fZ")
        + ".json"
    )

    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("x", encoding="utf-8") as stream:
        json.dump(
            result, stream,
            indent=2, sort_keys=True, allow_nan=False
        )
        stream.write("\n")

    print("RUN="+result["branch"])
    print("PROVENANCE="+result["gates"]["P0_PROVENANCE"])

    for name, case in result["cases"].items():
        print(
            "CASE="+name
            +" NEUTRAL_DP="+str(
                case["neutral_exact_momentum_change"]
            )
            +" J_POS="+str(
                case["neutral_positive_impulse"]
            )
            +" J_NEG="+str(
                case["neutral_negative_impulse"]
            )
            +" ENERGY_DRIFT="+str(
                case["max_energy_drift"]
            )
            +" MOMENTUM_DRIFT="+str(
                case["max_total_momentum_drift"]
            )
            +" CHI_MAX="+str(
                case["maximum_chi_neutral"]
            )
        )

    print("PH6_VERDICT="+result["verdict"])
    print("WHOLE_CRAFT_LIFT=NOT_DERIVED")
    print("FULL_B11_M6_IMPULSE=NOT_RUN")
    print("PHYSICAL_ENERGY_LT10MJ=NOT_CERTIFIED")
    print("JSON="+str(path))

    return (
        0 if result["gates"]["P0_PROVENANCE"] == "PASS"
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(main())
