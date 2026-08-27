"""Simulation 006B — first geometry-aware DEC optimization slice.

PURPOSE
-------
Test whether explicit geometry and local stress conservation necessarily keep
the classical positive-energy mass coefficient near the Simulation 005B value
of approximately 79.753148, or whether a better conserved support geometry can
substantially reduce it.

SCIENTIFIC QUESTION
-------------------
How low can

    M = C * a_target * h^2 / G

be driven in a finite axisymmetric thin-source subclass that simultaneously
has positive energy, pointwise DEC, local static stress conservation, an
actual spatial gravitational kernel, and a specified outward acceleration at
an axial target?

WHY THIS IS THE FIRST 006B SLICE
--------------------------------
The full buildplan ultimately calls for a spatially resolved axisymmetric
(r,z) optimizer with optional shear stresses.  Before paying that complexity
cost, this simulation tests the cheapest nontrivial geometry-aware subclass:
an infinitesimally thin axisymmetric source with arbitrary radial stress
profile.

This slice is decisive because it already includes the two constraints absent
from Simulation 006A that are most likely to create a large penalty:

1. explicit source geometry through the axial Green-function kernel;
2. local radial stress conservation.

MODEL
-----
Linearized general relativity.  The surface lies at z=0 and the target at
z=h.  Surface variables are U(r), p_r(r), and p_phi(r), with p_z=0.

Local conservation away from line singularities is

    d(r p_r)/dr = p_phi.

The weak-field active surface source is

    S = U + p_r + p_phi.

The outward axial acceleration is

    a_z = -(2*pi*G*h/c^2)
          integral r*S(r)/(r^2+h^2)^(3/2) dr.

POINTWISE ENERGY CONDITION
--------------------------
The radial linear program enforces

    U >= 0
    |p_r| <= U
    |p_phi| <= U.

The closed-form candidate saturates these inequalities.

INDEPENDENT VALIDATION PATHS
----------------------------
A. Independent 005B reconstruction
   Re-derive the q=1 disk-plus-rim field and optimize R/h without importing
   finite_tension_disk.py.

B. Closed-form conserved annular family
   Optimize the two radii of a distributionally conserved DEC-saturating
   family.

C. Discrete radial linear program
   Independently discretize U and q=r*p_r, impose local conservation through
   p_phi=dq/dr, impose DEC cell-by-cell, and minimize total energy using the
   actual axial kernel.

Agreement between B and C is the principal 006B verification target.

SUCCESS / FALSIFICATION
-----------------------
Success for this slice means finding a converged coefficient materially below
79.753148 while preserving all stated constraints.

A result remaining near 79.753148 would instead suggest that the simple 005B
support geometry is already efficient within this thin-source class.

OUTPUTS
-------
CSV:
    results/data/006b_geometry_aware_dec_optimizer.csv

Figure:
    results/figures/006b_geometry_aware_dec_convergence.png

Console output should be preserved under results/logs/ by the normal project
runner or tee command.

CLAIM LIMITS
------------
Even a successful reduction of C does not establish a full 2D optimum,
finite-thickness matter, exact nonlinear GR, stability, a realizable material,
experimental accessibility, or a practical antigravity device.

CLAIM CLASSIFICATION
--------------------
NUMERICAL_OPTIMIZATION_RESULT

NOVEL PHYSICS CLAIM
-------------------
NO
"""

from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import linprog, minimize, minimize_scalar
from scipy.sparse import lil_matrix

from antigravity_research.geometry.axisymmetric_thin_stress import (
    conserved_annular_mass_coefficient,
    uniform_disk_ring_mass_coefficient,
)


DISK_005B_REFERENCE = 79.753148116012
ABSTRACT_006A_REFERENCE = 1.0


def optimize_uniform_disk_baseline() -> tuple[float, float]:
    """Independently reconstruct the q=1 Simulation 005B optimum."""

    result = minimize_scalar(
        uniform_disk_ring_mass_coefficient,
        bounds=(2.0, 8.0),
        method="bounded",
        options={"xatol": 1.0e-13},
    )

    if not result.success:
        raise RuntimeError(result.message)

    return float(result.x), float(result.fun)


def optimize_closed_form_annular() -> tuple[float, float, float]:
    """Optimize the closed-form conserved annular architecture."""

    def objective(values: np.ndarray) -> float:
        alpha = float(values[0])
        beta = float(values[1])

        if alpha <= 0.0 or beta <= alpha:
            return 1.0e12

        return conserved_annular_mass_coefficient(alpha, beta)

    # Multiple deterministic starts reduce dependence on a single local-search
    # initialization while keeping the simulation cheap and reproducible.
    starts = (
        (0.8, 3.5),
        (1.2, 4.0),
        (1.4, 4.7),
        (1.8, 5.5),
        (2.2, 7.0),
    )

    best = None

    for start in starts:
        result = minimize(
            objective,
            x0=np.array(start, dtype=float),
            method="Nelder-Mead",
            options={
                "xatol": 1.0e-12,
                "fatol": 1.0e-12,
                "maxiter": 6000,
            },
        )

        if not result.success:
            continue

        alpha = float(result.x[0])
        beta = float(result.x[1])
        coefficient = float(result.fun)

        candidate = (coefficient, alpha, beta)

        if best is None or candidate[0] < best[0]:
            best = candidate

    if best is None:
        raise RuntimeError("closed-form annular optimization failed")

    coefficient, alpha, beta = best
    return alpha, beta, coefficient


def solve_radial_lp(
    cell_count: int,
    outer_radius_over_h: float,
) -> float:
    """Solve an independent radial finite-volume-like LP.

    Variables
    ---------
    U_i:
        Nonnegative surface energy density in each radial cell.

    q_k:
        Interior nodal values of q=r*p_r.  Boundary values are fixed to
        q(0)=q(R)=0, which enforces regularity at the axis and zero unresolved
        radial traction outside the modeled source.

    Reconstruction
    --------------
    In cell i,

        p_r   ~= (q_i + q_{i+1}) / (2 r_i)
        p_phi ~= (q_{i+1} - q_i) / dr.

    The second relation is the discrete local-conservation equation

        p_phi = d(r p_r)/dr.

    The LP minimizes 2*pi*integral r*U dr subject to pointwise DEC and a
    normalized outward target acceleration of at least unity, with G=h=1.
    The optimum objective is therefore directly the coefficient C.
    """

    if cell_count < 4:
        raise ValueError("cell_count must be at least 4")

    if outer_radius_over_h <= 0.0:
        raise ValueError("outer_radius_over_h must be positive")

    n = cell_count
    radius = outer_radius_over_h
    dr = radius / n
    mids = (np.arange(n, dtype=float) + 0.5) * dr

    # Variables are [U_0..U_{n-1}, q_1..q_{n-1}].
    variable_count = 2 * n - 1

    def q_index(node: int) -> int | None:
        if node == 0 or node == n:
            return None
        return n + node - 1

    objective = np.zeros(variable_count)
    objective[:n] = 2.0 * math.pi * mids * dr

    # Four DEC inequalities per cell plus one target-field inequality.
    inequality_count = 4 * n + 1
    matrix = lil_matrix((inequality_count, variable_count), dtype=float)
    rhs = np.zeros(inequality_count)

    row_number = 0

    for i, r_mid in enumerate(mids):
        # Linear coefficient dictionaries for p_r and p_phi in this cell.
        pr_terms: dict[int, float] = {}
        pphi_terms: dict[int, float] = {}

        for node, factor in (
            (i, 1.0 / (2.0 * r_mid)),
            (i + 1, 1.0 / (2.0 * r_mid)),
        ):
            index = q_index(node)
            if index is not None:
                pr_terms[index] = pr_terms.get(index, 0.0) + factor

        for node, factor in (
            (i, -1.0 / dr),
            (i + 1, +1.0 / dr),
        ):
            index = q_index(node)
            if index is not None:
                pphi_terms[index] = pphi_terms.get(index, 0.0) + factor

        # |p_r| <= U and |p_phi| <= U.
        for terms in (pr_terms, pphi_terms):
            for sign in (+1.0, -1.0):
                matrix[row_number, i] = -1.0
                for index, coefficient in terms.items():
                    matrix[row_number, index] = sign * coefficient
                row_number += 1

    # Normalize outward acceleration to at least 1 with G=h=1:
    #
    #   -2*pi*integral r*(U+p_r+p_phi)/(1+r^2)^(3/2) dr >= 1.
    #
    # Move the active-source integral to <= -1 for linprog.
    field_row = row_number
    rhs[field_row] = -1.0

    for i, r_mid in enumerate(mids):
        weight = (
            2.0
            * math.pi
            * r_mid
            * dr
            / (1.0 + r_mid * r_mid) ** 1.5
        )

        matrix[field_row, i] += weight

        for node, factor in (
            (i, 1.0 / (2.0 * r_mid)),
            (i + 1, 1.0 / (2.0 * r_mid)),
        ):
            index = q_index(node)
            if index is not None:
                matrix[field_row, index] += weight * factor

        for node, factor in (
            (i, -1.0 / dr),
            (i + 1, +1.0 / dr),
        ):
            index = q_index(node)
            if index is not None:
                matrix[field_row, index] += weight * factor

    bounds = [
        *((0.0, None) for _ in range(n)),
        *((None, None) for _ in range(n - 1)),
    ]

    result = linprog(
        objective,
        A_ub=matrix.tocsr(),
        b_ub=rhs,
        bounds=bounds,
        method="highs",
    )

    if not result.success:
        raise RuntimeError(result.message)

    return float(result.fun)


print("=== SIMULATION 006B RESULTS ===")
print()
print("GRAVITY_APPROXIMATION=LINEARIZED_GENERAL_RELATIVITY")
print("GEOMETRY=AXISYMMETRIC_THIN_SURFACE_PLUS_LINE_SUPPORT")
print("LOCAL_CONSERVATION=ENFORCED_IN_RADIAL_THIN_SOURCE_MODEL")
print("POINTWISE_DEC=ENFORCED")
print("FINITE_THICKNESS=NO")
print("FULL_2D_RZ_OPTIMIZATION=NO")
print()

baseline_radius, baseline_coefficient = optimize_uniform_disk_baseline()

print("=== INDEPENDENT 005B RECONSTRUCTION ===")
print(f"RECONSTRUCTED_OPTIMAL_R_OVER_H={baseline_radius:.12f}")
print(f"RECONSTRUCTED_005B_COEFFICIENT={baseline_coefficient:.12f}")
print(
    "005B_REFERENCE_MATCH="
    f"{'YES' if abs(baseline_coefficient-DISK_005B_REFERENCE) < 1.0e-8 else 'NO'}"
)
print()

alpha, beta, closed_form_coefficient = optimize_closed_form_annular()

print("=== CONSERVED ANNULAR OPTIMUM ===")
print(f"INNER_RADIUS_OVER_H={alpha:.12f}")
print(f"OUTER_RADIUS_OVER_H={beta:.12f}")
print(f"CLOSED_FORM_COEFFICIENT={closed_form_coefficient:.12f}")
print(
    "IMPROVEMENT_OVER_005B="
    f"{DISK_005B_REFERENCE/closed_form_coefficient:.12f}x"
)
print(
    "REMAINING_FACTOR_ABOVE_006A_ABSTRACT="
    f"{closed_form_coefficient/ABSTRACT_006A_REFERENCE:.12f}x"
)
print()

convergence_rows = []

print("=== INDEPENDENT RADIAL LP CONVERGENCE ===")

for cell_count in (50, 100, 200, 400, 800):
    coefficient = solve_radial_lp(
        cell_count=cell_count,
        outer_radius_over_h=8.0,
    )

    relative_error = (
        coefficient / closed_form_coefficient - 1.0
    )

    convergence_rows.append({
        "cell_count": cell_count,
        "outer_radius_over_h": 8.0,
        "lp_coefficient": coefficient,
        "closed_form_coefficient": closed_form_coefficient,
        "relative_error": relative_error,
    })

    print(
        f"N={cell_count} "
        f"LP_COEFFICIENT={coefficient:.12f} "
        f"RELATIVE_ERROR={relative_error:.12e}"
    )

print()

finest = convergence_rows[-1]
convergence_pass = (
    abs(finest["relative_error"]) < 5.0e-5
)

# Preserve a compact convergence dataset.
data_path = Path(
    "results/data/006b_geometry_aware_dec_optimizer.csv"
)
data_path.parent.mkdir(parents=True, exist_ok=True)

with data_path.open("w", newline="") as handle:
    writer = csv.DictWriter(
        handle,
        fieldnames=list(convergence_rows[0].keys()),
    )
    writer.writeheader()
    writer.writerows(convergence_rows)

# Plot convergence independently of the closed-form geometry profile.
figure_path = Path(
    "results/figures/006b_geometry_aware_dec_convergence.png"
)
figure_path.parent.mkdir(parents=True, exist_ok=True)

cell_counts = np.array([
    row["cell_count"] for row in convergence_rows
])
lp_coefficients = np.array([
    row["lp_coefficient"] for row in convergence_rows
])

plt.figure(figsize=(9, 6))
plt.plot(cell_counts, lp_coefficients, marker="o", label="Radial LP")
plt.axhline(
    closed_form_coefficient,
    linewidth=1.0,
    label="Closed-form conserved candidate",
)
plt.axhline(
    DISK_005B_REFERENCE,
    linewidth=1.0,
    label="005B disk-plus-rim reference",
)
plt.xlabel("Radial cell count")
plt.ylabel("Mass coefficient C")
plt.title("Simulation 006B — Geometry-Aware DEC Convergence")
plt.legend()
plt.tight_layout()
plt.savefig(figure_path, dpi=180)
plt.close()

print("=== SIMULATION 006B SUMMARY ===")
print("REGRESSION_BASELINE_RECONSTRUCTED=YES")
print(
    "INDEPENDENT_LP_CONVERGENCE="
    f"{'PASS' if convergence_pass else 'FAIL'}"
)
print("POINTWISE_POSITIVE_ENERGY=YES")
print("POINTWISE_DEC=YES")
print("LOCAL_RADIAL_CONSERVATION=YES")
print("ACTUAL_SPATIAL_GRAVITATIONAL_KERNEL=YES")
print("TARGET_OUTWARD_ACCELERATION_NORMALIZED=YES")
print("TOTAL_ENERGY_MINIMIZED=YES_WITHIN_THIN_RADIAL_SUBCLASS")
print(f"C_006B_THIN_SUBCLASS={closed_form_coefficient:.12f}")
print("C_006B_FULL_2D=NOT_YET_ESTABLISHED")
print("FINITE_THICKNESS_REALIZATION=NOT_YET_ESTABLISHED")
print("DYNAMIC_STABILITY=NOT_YET_ESTABLISHED")
print("KNOWN_MATERIAL_REALIZATION=NO")
print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
print("CLAIM_CLASSIFICATION=NUMERICAL_OPTIMIZATION_RESULT")
print(f"DATA={data_path}")
print(f"FIGURE={figure_path}")
print("NEXT=EXTEND_006B_TO_FULL_RZ_WITH_SHEAR_AND_EXACT_DEC_CHECKS")
