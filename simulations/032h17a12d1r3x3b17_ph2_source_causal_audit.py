"""PH2 executor: physical-source falsifiers and causal source controls.

Historical files are read-only. Every output has a unique timestamp.
No physical spacecraft impulse or device claim is permitted.
"""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import platform
import sys

from antigravity_research.agminer import (
    hook17_ph2_source_causal_audit as ph2,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=None,
    )

    args = parser.parse_args()
    root = args.root.resolve()

    record = ph2.execute(root)
    now = datetime.now(timezone.utc)

    record["executed_at_utc"] = now.isoformat()

    record["environment"] = {
        "python": sys.version,
        "platform": platform.platform(),
        "source_sha256": sha256(
            Path(ph2.__file__).read_bytes()
        ).hexdigest(),
        "sim_sha256": sha256(
            Path(__file__).read_bytes()
        ).hexdigest(),
        "executed_root": str(root),
    }

    out = args.out or (
        root/"results/data"/(
            "032h17_ph2_source_causal_"
            + now.strftime("%Y%m%dT%H%M%S%fZ")
            + ".json"
        )
    )

    out = out.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    with out.open("x", encoding="utf8") as stream:
        json.dump(
            record,
            stream,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
        stream.write("\n")

    print("BRANCH=" + record["branch"])

    for key, value in record["gates"].items():
        print(key + "=" + value)

    print(
        "FREE_SCALAR_EOM_INTEGRAL_UNSCALED="
        + str(
            record["static_falsifiers"][
                "mass0_positive_integral_unscaled"
            ]["free_static_no_go_integral"]
        )
    )

    for key in (
        "self_sourced",
        "incoming_recoil",
        "incoming_recoil_h384",
    ):
        result = record["source_driven_dynamics"][key]

        print(
            key.upper()+"_ENERGY_DRIFT="
            + str(result["max_energy_absolute_drift"])
        )

        print(
            key.upper()+"_MOMENTUM_DRIFT="
            + str(result["max_total_momentum_drift"])
        )

        print(
            key.upper()+"_SIGNED_SOURCE_IMPULSE="
            + str(result["source_center_signed_impulse"])
        )

    print("PH2_VERDICT=" + record["verdict"])
    print("JSON=" + str(out))

    if record["gates"]["PH2_PROVENANCE"] != "PASS_SCOPED":
        print(
            "PH2_ARCHIVAL_PROVENANCE_FAILED_CANNOT_PROMOTE"
        )
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
