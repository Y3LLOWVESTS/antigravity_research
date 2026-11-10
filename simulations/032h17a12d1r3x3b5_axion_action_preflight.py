"""R3X3B5: minimal-axion action screen and prior-result audit."""
from __future__ import annotations

import json
from pathlib import Path

from antigravity_research.agminer.hook17_r3x3b5_axion_action_gate import (
    all_gates,
)


def run():
    result = all_gates()

    prior = Path(
        "results/data/"
        "032h17a12d1r3x3b4_directional_com_summary.json"
    )

    result["r3x3b4_provenance_available"] = prior.exists()

    if prior.exists():
        data = json.loads(prior.read_text())

        if data.get("branch") != "032H17A12D1R3X3B4":
            raise ValueError("Unexpected R3X3B4 artifact")

        result["r3x3b4_grid_check"] = []

        for grid in data["grids"]:
            record = {
                "h_m": float(grid["h_m"]),
                "preloaded_com_m_s2": float(
                    grid["preloaded"]["com_acceleration_m_s2"]
                ),
                "fully_loaded_com_m_s2": float(
                    grid["fully_loaded"]["com_acceleration_m_s2"]
                ),
                "force_identity_relative_error": float(
                    grid["fully_loaded"][
                        "force_identity_relative_error"
                    ]
                ),
            }

            assert record["fully_loaded_com_m_s2"] < 9.80665
            result["r3x3b4_grid_check"].append(record)

    path = Path(
        "results/data/"
        "032h17a12d1r3x3b5_axion_action_preflight_summary.json"
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n"
    )

    print(
        "R3X3B5_DET_F_IDENTITY=",
        result["tensor"]["det_equals_E_dot_B_squared"],
    )
    print(
        "BARE_AXION_EXACT_MIRROR=",
        result["exact_mirror"][
            "bare_gamma_nonzero_varying_P_exact_mirror"
        ],
    )
    print(
        "NO_BARE_AXION_INTERFACE=",
        result["exact_mirror"][
            "no_bare_gamma_strict_interface_silence"
        ],
    )
    print(
        "R3X3B4_JSON_FOUND=",
        result["r3x3b4_provenance_available"],
    )
    print(
        "NEW_COMPENSATOR_CERTIFIED=",
        result["new_compensator_certified"],
    )
    print("RESULT_PATH=", path)

    return result


if __name__ == "__main__":
    run()
