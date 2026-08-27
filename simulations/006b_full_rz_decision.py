"""Simulation 006B — decisive finite-volume r-z stress-energy optimizer.

PURPOSE
-------
Run the smallest scientifically useful two-dimensional extension of the
verified 006B thin-source result.  The simulation tests whether finite z
structure and r-z shear can materially change the current restricted
coefficient C = 23.426710175391 while retaining positive energy, exact
pointwise dominant energy condition (DEC), finite support, and discrete local
stress conservation.

SCIENTIFIC QUESTION
-------------------
For a static axisymmetric source in linearized general relativity, what total
positive mass-energy is required to produce unit outward axial acceleration at
a target one stand-off unit above the nearest source boundary when local
conservation and exact shear-inclusive DEC are enforced?

MODEL
-----
The source occupies

    0 <= r <= R_max
    -D <= z <= 0

and the target is at (r,z) = (0,1), so h=1.  Dimensionless units G=c=1 are
used.  Cell energy e therefore has mass-density units, and the minimum total
mass directly equals C in

    M = C * a_target * h^2 / G.

The static active weak-field density is

    s = e + p_r + p_z + p_phi.

The axial Green kernel is integrated analytically over each complete annular
cell; no point-cell or center-of-cell gravity approximation is used.

STAGGERED FINITE-VOLUME STRESS GRID
-----------------------------------
To avoid cell-centered checkerboard modes, normal tractions live on the faces
where they physically act:

    p_r     radial faces
    p_z     horizontal z faces
    T_rz    cell vertices
    p_phi   cell centers
    e       cell centers

Cell-centered p_r, p_z, and T_rz used by DEC and gravity are reconstructed by
averaging their surrounding face/vertex values.

LOCAL CONSERVATION
------------------
The continuum equations are

    (1/r) d(r p_r)/dr + d(T_rz)/dz - p_phi/r = 0

    (1/r) d(r T_rz)/dr + d(p_z)/dz = 0.

They are enforced as integrated force balances for every annular cell.
Traction-free source boundaries are imposed explicitly.  Axis regularity uses
T_rz=0 and p_r=p_phi at r=0.

DOMINANT ENERGY CONDITION
-------------------------
The cell spatial stress matrix is

    [[p_r,  T_rz, 0],
     [T_rz, p_z,  0],
     [0,    0, p_phi]].

Exact type-I DEC requires every principal stress eigenvalue to satisfy
|lambda| <= e.  The r-z eigenvalue condition is imposed exactly with
second-order-cone constraints, and |p_phi| <= e is imposed linearly.

VALIDATION
----------
Every solve is post-checked using direct NumPy eigenvalues, reconstructed
finite-volume conservation residuals, target acceleration, and global Laue
stress integrals.  Several grids/domains are solved in one run so that a gross
mesh or finite-domain artifact is visible immediately.

CLAIM LIMITS
------------
This is an exploratory convergence/decision slice.  It does not establish a
continuum optimum, exact nonlinear Einstein solution, dynamic stability,
material realization, experimental accessibility, or practical antigravity
device.  Until dedicated convergence is demonstrated its strongest permitted
classification is NUMERICAL_OBSERVATION.
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path

import cvxpy as cp
import numpy as np

THIN_REFERENCE_C = 23.426710175391


@dataclass(frozen=True)
class Case:
    name: str
    nr: int
    nz: int
    radius: float
    depth: float


def exact_cell_axial_kernel(
    r0: float,
    r1: float,
    z0: float,
    z1: float,
    target_z: float = 1.0,
) -> float:
    """Return exact axial acceleration weight for unit active mass density."""

    d_near = target_z - z1
    d_far = target_z - z0

    def radial_difference(distance: float) -> float:
        return math.sqrt(r0 * r0 + distance * distance) - math.sqrt(
            r1 * r1 + distance * distance
        )

    # Positive active density below the target must accelerate inward, hence
    # this weight is negative.  Negative active density contributes outward.
    return -2.0 * math.pi * (
        radial_difference(d_far) - radial_difference(d_near)
    )


def solve_case(case: Case) -> dict[str, float | int | str]:
    nr, nz = case.nr, case.nz
    r_edges = np.linspace(0.0, case.radius, nr + 1)
    z_edges = np.linspace(-case.depth, 0.0, nz + 1)

    volumes = np.zeros((nr, nz), dtype=float)
    kernels = np.zeros((nr, nz), dtype=float)

    for i in range(nr):
        r0, r1 = r_edges[i], r_edges[i + 1]
        annulus_area = math.pi * (r1 * r1 - r0 * r0)
        for j in range(nz):
            z0, z1 = z_edges[j], z_edges[j + 1]
            volumes[i, j] = annulus_area * (z1 - z0)
            kernels[i, j] = exact_cell_axial_kernel(r0, r1, z0, z1)

    # Cell-centered positive mass-energy and azimuthal stress.
    e = cp.Variable((nr, nz), nonneg=True, name="e")
    pphi = cp.Variable((nr, nz), name="pphi")

    # Staggered normal tractions and symmetric shear field.
    pr_face = cp.Variable((nr + 1, nz), name="pr_face")
    pz_face = cp.Variable((nr, nz + 1), name="pz_face")
    trz_vertex = cp.Variable((nr + 1, nz + 1), name="trz_vertex")

    constraints: list[cp.Constraint] = []

    # Traction-free finite source boundaries and axis regularity.
    constraints.extend(
        [
            pr_face[nr, :] == 0.0,
            pz_face[:, 0] == 0.0,
            pz_face[:, nz] == 0.0,
            trz_vertex[0, :] == 0.0,
            trz_vertex[nr, :] == 0.0,
            trz_vertex[:, 0] == 0.0,
            trz_vertex[:, nz] == 0.0,
            pr_face[0, :] == pphi[0, :],
        ]
    )

    pr_cell: list[list[cp.Expression]] = [[None for _ in range(nz)] for _ in range(nr)]  # type: ignore[list-item]
    pz_cell: list[list[cp.Expression]] = [[None for _ in range(nz)] for _ in range(nr)]  # type: ignore[list-item]
    trz_cell: list[list[cp.Expression]] = [[None for _ in range(nz)] for _ in range(nr)]  # type: ignore[list-item]

    # Cell-centered stresses and exact pointwise DEC.
    for i in range(nr):
        for j in range(nz):
            prc = 0.5 * (pr_face[i, j] + pr_face[i + 1, j])
            pzc = 0.5 * (pz_face[i, j] + pz_face[i, j + 1])
            trzc = 0.25 * (
                trz_vertex[i, j]
                + trz_vertex[i + 1, j]
                + trz_vertex[i, j + 1]
                + trz_vertex[i + 1, j + 1]
            )

            pr_cell[i][j] = prc
            pz_cell[i][j] = pzc
            trz_cell[i][j] = trzc

            mean = 0.5 * (prc + pzc)
            half_difference = 0.5 * (prc - pzc)
            spectral_radius = cp.norm(
                cp.hstack([half_difference, trzc]),
                2,
            )

            constraints.extend(
                [
                    spectral_radius <= e[i, j] - mean,
                    spectral_radius <= e[i, j] + mean,
                    pphi[i, j] <= e[i, j],
                    -pphi[i, j] <= e[i, j],
                ]
            )

    # Exact integrated finite-volume local conservation.
    for i in range(nr):
        r0, r1 = r_edges[i], r_edges[i + 1]
        dr = r1 - r0
        annular_radial_factor = 0.5 * (r1 * r1 - r0 * r0)

        for j in range(nz):
            z0, z1 = z_edges[j], z_edges[j + 1]
            dz = z1 - z0

            # Shear traction on horizontal faces is the radial average of the
            # two vertices bounding that face.
            trz_south = 0.5 * (trz_vertex[i, j] + trz_vertex[i + 1, j])
            trz_north = 0.5 * (
                trz_vertex[i, j + 1] + trz_vertex[i + 1, j + 1]
            )

            # Shear traction on radial faces is the vertical average of the
            # two vertices bounding that face.
            trz_west = 0.5 * (trz_vertex[i, j] + trz_vertex[i, j + 1])
            trz_east = 0.5 * (
                trz_vertex[i + 1, j] + trz_vertex[i + 1, j + 1]
            )

            radial_balance = (
                dz * (r1 * pr_face[i + 1, j] - r0 * pr_face[i, j])
                + annular_radial_factor * (trz_north - trz_south)
                - dr * dz * pphi[i, j]
            )

            vertical_balance = (
                2.0 * dz * (r1 * trz_east - r0 * trz_west)
                + (r1 * r1 - r0 * r0)
                * (pz_face[i, j + 1] - pz_face[i, j])
            )

            constraints.extend(
                [radial_balance == 0.0, vertical_balance == 0.0]
            )

    # Assemble cell-centered stresses into CVXPY matrices.
    pr_matrix = cp.vstack(
        [cp.hstack([pr_cell[i][j] for j in range(nz)]) for i in range(nr)]
    )
    pz_matrix = cp.vstack(
        [cp.hstack([pz_cell[i][j] for j in range(nz)]) for i in range(nr)]
    )

    # Necessary Laue identities for a complete static localized source.
    volume_constant = cp.Constant(volumes)
    constraints.extend(
        [
            cp.sum(cp.multiply(volume_constant, pr_matrix + pphi)) == 0.0,
            cp.sum(cp.multiply(volume_constant, pz_matrix)) == 0.0,
        ]
    )

    active_density = e + pr_matrix + pz_matrix + pphi
    target_acceleration = cp.sum(
        cp.multiply(cp.Constant(kernels), active_density)
    )
    total_mass = cp.sum(cp.multiply(volume_constant, e))
    constraints.append(target_acceleration >= 1.0)

    problem = cp.Problem(cp.Minimize(total_mass), constraints)

    installed = cp.installed_solvers()
    solver = "CLARABEL" if "CLARABEL" in installed else "SCS"

    try:
        problem.solve(solver=solver, verbose=False)
    except Exception:
        if solver != "SCS" and "SCS" in installed:
            solver = "SCS"
            problem.solve(
                solver=solver,
                verbose=False,
                eps=2.0e-5,
                max_iters=100000,
            )
        else:
            raise

    if problem.status not in (cp.OPTIMAL, cp.OPTIMAL_INACCURATE):
        return {
            "name": case.name,
            "nr": nr,
            "nz": nz,
            "radius": case.radius,
            "depth": case.depth,
            "status": problem.status,
            "solver": solver,
            "coefficient": math.nan,
        }

    e_v = np.asarray(e.value, dtype=float)
    pphi_v = np.asarray(pphi.value, dtype=float)
    prf_v = np.asarray(pr_face.value, dtype=float)
    pzf_v = np.asarray(pz_face.value, dtype=float)
    trzv_v = np.asarray(trz_vertex.value, dtype=float)

    pr_v = 0.5 * (prf_v[:-1, :] + prf_v[1:, :])
    pz_v = 0.5 * (pzf_v[:, :-1] + pzf_v[:, 1:])
    trz_v = 0.25 * (
        trzv_v[:-1, :-1]
        + trzv_v[1:, :-1]
        + trzv_v[:-1, 1:]
        + trzv_v[1:, 1:]
    )

    active_v = e_v + pr_v + pz_v + pphi_v
    mass_v = float(np.sum(volumes * e_v))
    acceleration_v = float(np.sum(kernels * active_v))

    max_dec_violation = 0.0
    for i in range(nr):
        for j in range(nz):
            stress = np.array(
                [
                    [pr_v[i, j], trz_v[i, j], 0.0],
                    [trz_v[i, j], pz_v[i, j], 0.0],
                    [0.0, 0.0, pphi_v[i, j]],
                ]
            )
            largest = float(np.max(np.abs(np.linalg.eigvalsh(stress))))
            max_dec_violation = max(
                max_dec_violation,
                largest - e_v[i, j],
            )

    # Independent reconstruction of every finite-volume conservation equation.
    max_conservation_residual = 0.0
    for i in range(nr):
        r0, r1 = r_edges[i], r_edges[i + 1]
        dr = r1 - r0
        annular_radial_factor = 0.5 * (r1 * r1 - r0 * r0)
        for j in range(nz):
            dz = z_edges[j + 1] - z_edges[j]
            trz_south = 0.5 * (trzv_v[i, j] + trzv_v[i + 1, j])
            trz_north = 0.5 * (
                trzv_v[i, j + 1] + trzv_v[i + 1, j + 1]
            )
            trz_west = 0.5 * (trzv_v[i, j] + trzv_v[i, j + 1])
            trz_east = 0.5 * (
                trzv_v[i + 1, j] + trzv_v[i + 1, j + 1]
            )

            rr = (
                dz * (r1 * prf_v[i + 1, j] - r0 * prf_v[i, j])
                + annular_radial_factor * (trz_north - trz_south)
                - dr * dz * pphi_v[i, j]
            )
            zz = (
                2.0 * dz * (r1 * trz_east - r0 * trz_west)
                + (r1 * r1 - r0 * r0)
                * (pzf_v[i, j + 1] - pzf_v[i, j])
            )
            max_conservation_residual = max(
                max_conservation_residual,
                abs(float(rr)),
                abs(float(zz)),
            )

    radial_laue = float(np.sum(volumes * (pr_v + pphi_v)))
    vertical_laue = float(np.sum(volumes * pz_v))
    trace_integral = radial_laue + vertical_laue

    return {
        "name": case.name,
        "nr": nr,
        "nz": nz,
        "radius": case.radius,
        "depth": case.depth,
        "status": problem.status,
        "solver": solver,
        "coefficient": mass_v,
        "acceleration": acceleration_v,
        "max_dec_violation": max_dec_violation,
        "max_conservation_residual": max_conservation_residual,
        "radial_laue": radial_laue,
        "vertical_laue": vertical_laue,
        "trace_integral": trace_integral,
        "active_mass_integral": float(np.sum(volumes * active_v)),
        "max_energy_density": float(np.max(e_v)),
        "occupied_fraction": float(
            np.mean(e_v > 1.0e-7 * max(float(np.max(e_v)), 1.0e-30))
        ),
    }


def main() -> None:
    # The first three cases test mesh refinement at a compact domain.  The last
    # two test whether allowing support to spread farther in r and z materially
    # changes the answer.  They are intentionally small enough to finish fast.
    cases = [
        Case("A_COARSE_COMPACT", 6, 4, 5.0, 1.0),
        Case("B_MEDIUM_COMPACT", 8, 6, 5.0, 1.0),
        Case("C_FINE_COMPACT", 10, 8, 5.0, 1.0),
        Case("D_MEDIUM_EXPANDED", 8, 6, 7.0, 2.0),
        Case("E_FINE_EXPANDED", 10, 8, 7.0, 2.0),
    ]

    print("=== 006B FULL-RZ DECISION SLICE ===")
    print(f"CVXPY_VERSION={cp.__version__}")
    print("INSTALLED_SOLVERS=" + ",".join(cp.installed_solvers()))
    print(f"THIN_REFERENCE_C={THIN_REFERENCE_C:.12f}")
    print("TARGET_STANDOFF_H=1")
    print("TARGET_ACCELERATION=1")
    print("KERNEL=EXACT_ANNULAR_CELL_INTEGRAL")
    print("STRESS_GRID=STAGGERED_FINITE_VOLUME")
    print("LOCAL_CONSERVATION=EXACT_CELL_FORCE_BALANCE")
    print("DEC=EXACT_EIGENVALUE_SOC")
    print()

    rows: list[dict[str, float | int | str]] = []
    for case in cases:
        result = solve_case(case)
        rows.append(result)
        print(
            f"CASE={case.name} GRID={case.nr}x{case.nz} "
            f"RMAX={case.radius:.3f} DEPTH={case.depth:.3f} "
            f"STATUS={result['status']} SOLVER={result['solver']}"
        )
        if math.isfinite(float(result["coefficient"])):
            print(f"  C={float(result['coefficient']):.12f}")
            print(f"  ACCELERATION={float(result['acceleration']):.12f}")
            print(
                "  MAX_DEC_VIOLATION="
                f"{float(result['max_dec_violation']):.3e}"
            )
            print(
                "  MAX_CONSERVATION_RESIDUAL="
                f"{float(result['max_conservation_residual']):.3e}"
            )
            print(
                "  STRESS_TRACE_INTEGRAL="
                f"{float(result['trace_integral']):.3e}"
            )
            print(
                "  RATIO_TO_THIN_REFERENCE="
                f"{float(result['coefficient']) / THIN_REFERENCE_C:.9f}"
            )
        print()

    finite_rows = [
        row for row in rows if math.isfinite(float(row["coefficient"]))
    ]
    if not finite_rows:
        raise SystemExit("NO_FEASIBLE_FULL_RZ_CASE=YES")

    best = min(finite_rows, key=lambda row: float(row["coefficient"]))

    output_path = Path("results/data/006b_full_rz_decision.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = sorted({key for row in rows for key in row})
    with output_path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    max_dec = max(float(row["max_dec_violation"]) for row in finite_rows)
    max_cons = max(
        float(row["max_conservation_residual"]) for row in finite_rows
    )
    numerics_green = max_dec < 2.0e-6 and max_cons < 2.0e-6

    best_c = float(best["coefficient"])
    ratio = best_c / THIN_REFERENCE_C

    print("=== 006B FULL-RZ DECISION SUMMARY ===")
    print(f"BEST_CASE={best['name']}")
    print(f"BEST_C={best_c:.12f}")
    print(f"THIN_REFERENCE_C={THIN_REFERENCE_C:.12f}")
    print(f"BEST_RATIO_TO_THIN={ratio:.12f}")
    print(
        "NUMERICAL_CONSTRAINT_CHECK="
        + ("PASS" if numerics_green else "REVIEW")
    )

    if ratio < 0.95:
        decision = "FULL_RZ_SHOWS_MATERIAL_IMPROVEMENT_CONTINUE_CONVERGENCE"
    elif ratio <= 1.10:
        decision = "FULL_RZ_NEAR_THIN_REFERENCE_CONVERGENCE_REQUIRED"
    else:
        decision = "CURRENT_FINITE_VOLUME_FULL_RZ_COSTLIER_THAN_THIN_REFERENCE"

    print(f"DECISION={decision}")
    print("CLAIM_CLASSIFICATION=NUMERICAL_OBSERVATION")
    print("CONTINUUM_OPTIMUM=NOT_ESTABLISHED")
    print("FINITE_THICKNESS_PHYSICAL_REALIZATION=NOT_ESTABLISHED")
    print("DYNAMIC_STABILITY=NOT_ESTABLISHED")
    print("KNOWN_MATERIAL_REALIZATION=NO")
    print("PRACTICAL_ANTIGRAVITY_DEVICE=NO")
    print(f"DATA={output_path}")
    print("NEXT=INTERPRET_GRID_AND_DOMAIN_TREND_BEFORE_MORE_COMPLEXITY")


if __name__ == "__main__":
    main()
