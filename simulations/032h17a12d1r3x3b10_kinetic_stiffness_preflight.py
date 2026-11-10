"""R3X3B10 — positive kinetic-stiffness spherical preflight."""
import json
from pathlib import Path

from antigravity_research.agminer.hook17_fdual_f_r3x3b10_kinetic_gate import (
    evaluate,
)


def run():
    prior_path = Path(
        "results/data/"
        "032h17a12d1r3x3b9_reciprocity_preflight_summary.json"
    )

    if not prior_path.is_file():
        raise FileNotFoundError(
            "R3X3B9 provenance missing"
        )

    prior = json.loads(prior_path.read_text())

    if prior["branch"] != "032H17A12D1R3X3B9":
        raise ValueError("Unexpected prior branch")

    theta = float(
        prior["comparison_to_r3b"][
            "one_keV_peak_dimensionless_beta_magnitude"
        ]
    )

    result = evaluate(theta)

    result["r3x3b9_prior_verified"] = True
    result["theta_used_as_spherical_comparator_only"] = True

    path = Path(
        "results/data/"
        "032h17a12d1r3x3b10_kinetic_stiffness_summary.json"
    )

    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )

    print("R3X3B10_REFERENCE_THETA=", theta)

    print(
        "UNIFORM_TRANSMISSION_BOUND=",
        result["all_positive_Z_all_ell_bound"]
    )

    for row in result["modes"]:
        if row["ell"] == 1 and row["interior_Z"] in (
            1.0, 10000.0, 1e6
        ):
            print(
                "ELL=1",
                "Z=", row["interior_Z"],
                "NORM=", row["transmission_norm"]
            )

    print("R3X3B10_RESULT_PATH=", path)


if __name__ == "__main__":
    run()
