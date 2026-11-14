"""B17-M4B4: paired Earth/source variational audit, not propulsion."""

import argparse
import json
from pathlib import Path

from antigravity_research.agminer.hook17_r3b_m4b4_paired_translation import (
    BRANCH,
    evaluate,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--grid",
        type=float,
        choices=(0.3, 0.25, 0.2),
        default=0.25,
    )
    parser.add_argument(
        "--portal-ev",
        type=float,
        choices=(1000.0, 21147.0),
        default=21147.0,
    )
    parser.add_argument(
        "--step",
        type=float,
        default=2e-4,
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
    )

    args = parser.parse_args()

    result = evaluate(
        args.grid,
        args.portal_ev,
        args.step,
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
        "branch": BRANCH,
        "grid_m": args.grid,
        "portal_ev": args.portal_ev,
        "step_m": args.step,

        "earth_action_slope_j_m":
            result["earth_action_slope_j_m"],

        "craft_action_slope_j_m":
            result["craft_action_slope_j_m"],

        "reciprocity_defect_fraction":
            result["paired_translation_defect_fraction"],

        "earth_envelope_error":
            result["earth_envelope_relative_error"],

        "craft_envelope_error":
            result["craft_envelope_relative_error"],

        "common_shift_slope_j_m":
            result["common_shift_finite_difference_j_m"],

        "source_inside_enclosure_both_shifts":
            (
                result["source_support_plus"][
                    "inside_enclosure_radius"
                ]
                and
                result["source_support_minus"][
                    "inside_enclosure_radius"
                ]
            ),

        "whole_craft_force_n": None,
        "warning": result["warning"],
    }, indent=2))


if __name__ == "__main__":
    main()
