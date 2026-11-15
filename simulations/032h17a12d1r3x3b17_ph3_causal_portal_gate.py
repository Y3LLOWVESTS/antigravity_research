"""Execute PH3 causal-characteristic preflight; write unique JSON only."""

from datetime import datetime, timezone
from pathlib import Path
from hashlib import sha256
import json
import sys

from antigravity_research.agminer import (
    hook17_ph3_causal_portal_gate as ph3
)


def main():
    root = Path.cwd()
    data = ph3.run(root)
    timestamp = datetime.now(timezone.utc)

    data["execution"] = {
        "utc": timestamp.isoformat(),
        "python": sys.version,
        "module_sha256":
            sha256(Path(ph3.__file__).read_bytes()).hexdigest(),
        "sim_sha256":
            sha256(Path(__file__).read_bytes()).hexdigest(),
    }

    target = root/"results/data"/(
        "032h17_ph3_causal_portal_"
        +timestamp.strftime("%Y%m%dT%H%M%S%fZ")
        +".json"
    )

    target.parent.mkdir(parents=True, exist_ok=True)

    with target.open("x", encoding="utf-8") as f:
        json.dump(
            data, f,
            sort_keys=True,
            indent=2,
            allow_nan=False,
        )
        f.write("\n")

    print("RUN="+data["branch"])
    print(
        "P0_PROVENANCE="
        +data["gates"]["P0_PRIOR_SOURCE_RESULTS"]
    )

    atlas = data[
        "pre_registered_12_case_characteristic_atlas"
    ]

    for label, record in atlas.items():
        print(
            "CASE="+label
            +" VERDICT="+record["verdict"]
            +" V_OVER_C="+str(
                record["extraordinary_speed_over_physical_c"]
            )
        )

    for label, record in data[
        "independent_fourier_evolution"
    ].items():
        print(
            "DYNAMICAL_CHECK="+label
            +" FREQUENCIES="+str(
                record["numeric_speeds_over_c"]
            )
            +" ENERGY_DRIFT="+str(
                record["max_quadratic_energy_drift_shape_units"]
            )
        )

    print("PH3_VERDICT="+data["verdict"])
    print("WHOLE_CRAFT_LIFT=NOT_DERIVED")
    print("B11_M6=NOT_RUN")
    print("JSON="+str(target))

    return (
        0 if data["gates"]["P0_PRIOR_SOURCE_RESULTS"]
        == "PASS_ARCHIVAL_SHA"
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(main())
