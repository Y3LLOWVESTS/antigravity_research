"""Simulation 008B — distributed field-theory representability gate.

PURPOSE
-------
Interrogate the finite 006D stress tensor as candidate canonical scalar-field
stress-energy before constructing an expensive microscopic PDE model.

SCIENTIFIC QUESTIONS
--------------------
1. Is the 006D stress tensor locally compatible with positive-sign canonical
   scalar gradient energy?

2. How many independent scalar gradient directions are required in its core,
   transfer annulus, and finite support collar?

3. Can strictly axisymmetric scalar fields reproduce the required azimuthal
   stress?

4. If an arbitrary canonical multi-scalar model reproduces the stress tensor,
   can the resulting static localized configuration be stable under Derrick
   dilation?

METHOD
------
The 006D radial stress profile is independently reconstructed from its
documented q=r*p_r construction.

At each radius,

    M_ii = epsilon + p_i

is interpreted as the diagonal kinetic Gram matrix required of canonical
scalar fields.

The integrated Laue pressure trace is independently evaluated.

The implied canonical scalar gradient and potential energies are reconstructed
and inserted into the standard three-dimensional Derrick scaling relation.

DECISION RULE
-------------
If:

- the Gram matrix is PSD;
- nonzero M_phiphi occurs;
- the collar reaches rank three;
- Laue balance gives a stationary scalar virial;
- the Derrick second variation is negative;

then:

- local algebraic scalar representability survives;
- strictly axisymmetric scalar fields are insufficient;
- a pure static canonical multi-scalar stabilization route is rejected;
- a new stabilizing sector is required before a full field simulation has
  scientific value.

APPROXIMATION LEVEL
-------------------
Static flat-background canonical-field representability analysis applied to the
linearized-GR 006D stress tensor.

This is not a nonlinear Einstein-matter solution.

CLAIM CLASSIFICATION
--------------------
ANALYTICAL_FIELD_THEORY_REPRESENTABILITY_AND_STABILITY_GATE
"""

from __future__ import annotations

import csv
from pathlib import Path

from antigravity_research.geometry.canonical_scalar_representability import (
    ALPHA_006D,
    BETA_006D,
    FINEST_SCALE_006D,
    canonical_scalar_derrick_diagnostics,
    integrated_006d_energy_and_pressure_trace,
    regularized_006d_surface_stress,
    strictly_axisymmetric_scalars_sufficient,
)


ROOT = Path(__file__).resolve().parents[1]

OUTPUT_CSV = (
    ROOT
    / "results"
    / "data"
    / "008b_distributed_field_representability_gate.csv"
)


def main() -> None:
    """Run the 008B representability and Derrick-stability gate."""

    OUTPUT_CSV.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    inner_width = (
        FINEST_SCALE_006D / 4.0
    )

    representative_points = {
        "core": (
            ALPHA_006D
            - 2.0 * inner_width
        ),
        "inner_transition": ALPHA_006D,
        "transfer_annulus": (
            0.5
            * (
                ALPHA_006D
                + BETA_006D
            )
        ),
        "outer_collar": (
            BETA_006D
            + 0.5 * FINEST_SCALE_006D
        ),
    }

    print(
        "=== SIMULATION 008B — DISTRIBUTED FIELD REPRESENTABILITY ==="
    )

    print(
        "TARGET_STRESS=006D_FINEST_REGULARIZED_PROFILE"
    )

    print(
        f"006D_SCALE={FINEST_SCALE_006D:.8f}"
    )

    print()
    print(
        "=== REPRESENTATIVE LOCAL DECOMPOSITIONS ==="
    )

    rows = []

    all_psd = True
    max_rank = 0
    azimuthal_required = False

    for region, radius in representative_points.items():
        stress = regularized_006d_surface_stress(
            radius
        )

        decomposition = (
            stress.scalar_decomposition()
        )

        rank = decomposition.rank(
            tolerance=1.0e-10
        )

        psd = decomposition.is_positive_semidefinite(
            tolerance=1.0e-10
        )

        axisymmetric_sufficient = (
            strictly_axisymmetric_scalars_sufficient(
                decomposition,
                tolerance=1.0e-10,
            )
        )

        all_psd = all_psd and psd
        max_rank = max(max_rank, rank)

        if not axisymmetric_sufficient:
            azimuthal_required = True

        rows.append(
            {
                "region": region,
                "radius": radius,
                "epsilon": stress.epsilon,
                "p_r": stress.p_r,
                "p_phi": stress.p_phi,
                "gram_r": decomposition.gram_r,
                "gram_phi": decomposition.gram_phi,
                "gram_z": decomposition.gram_z,
                "potential": decomposition.potential,
                "gram_rank": rank,
                "gram_psd": psd,
                "strict_axisymmetric_scalars_sufficient": (
                    axisymmetric_sufficient
                ),
            }
        )

        print(
            f"REGION={region} "
            f"R={radius:.12f} "
            f"EPS={stress.epsilon:.12e} "
            f"PR={stress.p_r:.12e} "
            f"PPHI={stress.p_phi:.12e} "
            f"MR={decomposition.gram_r:.12e} "
            f"MPHI={decomposition.gram_phi:.12e} "
            f"MZ={decomposition.gram_z:.12e} "
            f"V={decomposition.potential:.12e} "
            f"RANK={rank} "
            f"PSD={'YES' if psd else 'NO'}"
        )

    # Dense independent PSD / symmetry scan.
    outer_radius = (
        BETA_006D
        + FINEST_SCALE_006D
    )

    minimum_gram = float("inf")
    maximum_rank = 0
    azimuthal_positive_count = 0
    sample_count = 8001

    for index in range(sample_count):
        radius = (
            outer_radius
            * index
            / (sample_count - 1)
        )

        decomposition = (
            regularized_006d_surface_stress(
                radius
            ).scalar_decomposition()
        )

        minimum_gram = min(
            minimum_gram,
            decomposition.gram_r,
            decomposition.gram_phi,
            decomposition.gram_z,
        )

        maximum_rank = max(
            maximum_rank,
            decomposition.rank(
                tolerance=1.0e-10
            ),
        )

        if decomposition.gram_phi > 1.0e-10:
            azimuthal_positive_count += 1

    dense_psd = (
        minimum_gram >= -1.0e-10
    )

    azimuthal_required = (
        azimuthal_required
        or azimuthal_positive_count > 0
    )

    max_rank = max(
        max_rank,
        maximum_rank,
    )

    print()
    print(
        "=== GLOBAL CANONICAL-SCALAR VIRIAL ==="
    )

    energy, pressure_trace = (
        integrated_006d_energy_and_pressure_trace()
    )

    diagnostics = (
        canonical_scalar_derrick_diagnostics(
            energy,
            pressure_trace,
        )
    )

    pressure_ratio = (
        pressure_trace / energy
    )

    gradient_ratio = (
        diagnostics.gradient_energy / energy
    )

    potential_ratio = (
        diagnostics.potential_energy / energy
    )

    second_ratio = (
        diagnostics.second_scaling_derivative
        / energy
    )

    print(
        f"TOTAL_ENERGY_NORMALIZED={energy:.12e}"
    )

    print(
        f"INTEGRATED_PRESSURE_TRACE={pressure_trace:.12e}"
    )

    print(
        f"PRESSURE_TRACE_OVER_E={pressure_ratio:.12e}"
    )

    print(
        f"CANONICAL_GRADIENT_ENERGY_OVER_E={gradient_ratio:.12f}"
    )

    print(
        f"CANONICAL_POTENTIAL_ENERGY_OVER_E={potential_ratio:.12f}"
    )

    print(
        f"DERRICK_FIRST_DERIVATIVE_OVER_E="
        f"{diagnostics.first_scaling_derivative / energy:.12e}"
    )

    print(
        f"DERRICK_SECOND_DERIVATIVE_OVER_E={second_ratio:.12f}"
    )

    stationary = (
        diagnostics.stationary(
            relative_tolerance=1.0e-10
        )
    )

    derrick_stable = (
        diagnostics.stable_against_uniform_scaling()
    )

    with OUTPUT_CSV.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(
                rows[0].keys()
            ),
        )

        writer.writeheader()
        writer.writerows(rows)

    gate_green = (
        all_psd
        and dense_psd
        and max_rank == 3
        and azimuthal_required
        and stationary
        and not derrick_stable
        and abs(gradient_ratio - 1.5) < 1.0e-9
        and abs(potential_ratio + 0.5) < 1.0e-9
        and abs(second_ratio + 3.0) < 1.0e-9
    )

    print()
    print(
        "=== SCIENTIFIC DECISION ==="
    )

    print(
        "006D_CANONICAL_SCALAR_KINETIC_GRAM_PSD="
        f"{'YES' if all_psd and dense_psd else 'NO'}"
    )

    print(
        f"MINIMUM_LOCAL_REAL_SCALAR_COMPONENTS_LOWER_BOUND="
        f"{max_rank}"
    )

    print(
        "STRICTLY_AXISYMMETRIC_REAL_SCALARS_SUFFICIENT="
        f"{'NO' if azimuthal_required else 'YES'}"
    )

    print(
        "ANGULAR_WINDING_OR_NONSYMMETRIC_FIELD_SECTOR_REQUIRED="
        f"{'YES' if azimuthal_required else 'NO'}"
    )

    print(
        "006D_SCALAR_VIRIAL_STATIONARY="
        f"{'YES' if stationary else 'NO'}"
    )

    print(
        "PURE_STATIC_CANONICAL_MULTI_SCALAR_DERRICK_STABLE="
        f"{'YES' if derrick_stable else 'NO'}"
    )

    print(
        "PURE_STATIC_CANONICAL_SCALAR_STABLE_REALIZATION="
        "REJECTED_UNDER_STANDARD_DERRICK_ASSUMPTIONS"
        if gate_green
        else "UNRESOLVED"
    )

    print(
        "LOCAL_ALGEBRAIC_FIELD_REPRESENTABILITY="
        f"{'YES' if all_psd and dense_psd else 'NO'}"
    )

    print(
        "GLOBAL_EXPLICIT_LAGRANGIAN_REALIZATION="
        "NOT_ESTABLISHED"
    )

    print(
        "STABILIZING_EXTRA_SECTOR_REQUIRED="
        f"{'YES' if gate_green else 'UNRESOLVED'}"
    )

    print(
        "CANDIDATE_EXTRA_SECTORS="
        "CONSERVED_CHARGE_CURRENT_GAUGE_TIME_DEPENDENCE_OR_HIGHER_DERIVATIVES"
    )

    print(
        "NONLINEAR_GR_REALIZATION="
        "NOT_ESTABLISHED"
    )

    print(
        "PRACTICAL_ANTIGRAVITY_DEVICE="
        "NO"
    )

    print(
        "CLAIM_CLASSIFICATION="
        "ANALYTICAL_FIELD_THEORY_REPRESENTABILITY_AND_STABILITY_GATE"
    )

    print(
        "NEXT="
        "CHARGED_OR_GAUGED_DISTRIBUTED_COLLAR_GATE_OR_CLASSICAL_BRANCH_STOP"
    )

    print(
        f"OUTPUT_CSV={OUTPUT_CSV}"
    )

    print(
        "SIMULATION_008B=GREEN"
        if gate_green
        else "SIMULATION_008B=REVIEW"
    )


if __name__ == "__main__":
    main()
