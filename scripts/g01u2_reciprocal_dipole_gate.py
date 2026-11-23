"""G01-U2: reciprocal Maxwell-axion radial dipole gate.

Static gauge-sector action:
 L = (E_X^2-B_Y^2)/2 + theta(phi)*E_X.B_Y + sources

 D_X = E_X + theta B_Y
 H_Y = B_Y - theta E_X

Retains radial theta_0(r) and l=1 Maxwell dipoles.
The G01-U1 theta_2 angular mode is NOT included.

The surface X charge and Y current are prescribed.
No complete material-source action is established.

Constant theta must produce no bulk Maxwell response.
Magnetic divergence is projected to zero discretely.
Scalar roots are projected necessary conditions, NOT
solutions of the complete scalar field equation.

No full Einstein gravity, neutral-fluid stationarity,
Lorentzian health or whole-craft force is certified.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math

from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve

R = 2.0
C = 299792458.0
G = 6.67430e-11
TARGET = 9.80665

U1_HASH = (
    "0f5b138a22d9da0088cdb9d6c2bfdcfbb046603845447"
    "d250878809c454616c3"
)

RADIAL_HASH = (
    "cfe54027edcd6a33532faa5eec138455bc35a89193f9b3"
    "af1d4cd4f5bf727999"
)


def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()


class Problem:
    def __init__(self, radial, source, L, h):
        self.L = float(L)
        self.nr = int(round(L / h)) + 1

        self.r = np.linspace(0, L, self.nr)
        self.h = self.r[1] - self.r[0]
        self.N = self.nr - 2

        shell_index = int(round(R / self.h))

        if abs(self.r[shell_index] - R) > 1e-10:
            raise RuntimeError("SHELL_NOT_GRID_ALIGNED")

        self.f0 = PchipInterpolator(
            radial["r"],
            radial["f0"],
        )

        self.theta_coefficient = (
            C**4 / (8 * math.pi * G)
            * source[
                "source_kappa_m_per_J_assuming_illustrative_dipole_calibration"
            ]
            * source["source_axion_amplitude_A"]
        )

        self.basephi = lambda r: (
            -(1 / R)
            * (
                r if r <= R
                else R**3 / (r * r)
            )
        )

        def br(r):
            return (
                (1 / R)
                * (
                    1 if r <= R
                    else R**3 / r**3
                )
            )

        def magpsi(r, inside):
            return (
                (1 / R)
                * (
                    -r if inside
                    else R**3 / (2 * r * r)
                )
            )

        edges = []
        angles = []

        # Radial stiffness and source fluxes.
        for i in range(self.nr - 1):
            rmid = (self.r[i] + self.r[i + 1]) / 2

            weight = (
                4 * math.pi / 3
                * rmid * rmid / self.h
            )

            dphi = (
                self.basephi(self.r[i + 1])
                - self.basephi(self.r[i])
            )

            db = -br(rmid) * self.h

            edges.append([
                i, i + 1,
                weight, rmid,
                dphi, db,
            ])

        # Angular dipole stiffness.
        for i in range(1, self.nr - 1):
            ri = self.r[i]
            weight = 8 * math.pi / 3 * self.h

            if abs(ri - R) < 1e-10:
                bm = 0.5 * (
                    magpsi(ri, True)
                    + magpsi(ri, False)
                )
            else:
                bm = magpsi(ri, ri < R)

            angles.append([
                i, weight, ri,
                self.basephi(ri),
                bm,
            ])

        def idx(i):
            if 0 < i < self.nr - 1:
                return i - 1
            return None

        # Hodge-project the reference magnetic field
        # to an exactly conserved discrete source.
        lr, lc, lv = [], [], []
        rhs = np.zeros(self.N)

        for i, k, w, _, de, db in edges:
            for ii, s1 in ((i, -1), (k, 1)):
                row = idx(ii)

                if row is None:
                    continue

                rhs[row] -= w * db * s1

                for jj, s2 in ((i, -1), (k, 1)):
                    col = idx(jj)

                    if col is not None:
                        lr.append(row)
                        lc.append(col)
                        lv.append(w * s1 * s2)

        for i, w, _, de, db in angles:
            row = idx(i)

            rhs[row] -= w * db

            lr.append(row)
            lc.append(row)
            lv.append(w)

        lap = coo_matrix(
            (lv, (lr, lc)),
            shape=(self.N, self.N),
        ).tocsr()

        xi = spsolve(lap, rhs)

        for edge in edges:
            i, k = edge[:2]

            correction = (
                xi[idx(k)]
                if idx(k) is not None
                else 0
            ) - (
                xi[idx(i)]
                if idx(i) is not None
                else 0
            )

            edge[5] += correction

        for a in angles:
            a[4] += xi[idx(a[0])]

        self.edges = edges
        self.angles = angles

        self.energy0 = (
            sum(
                w * (de * de + db * db) / 2
                for i, k, w, _, de, db in edges
            )
            + sum(
                w * (de * de + db * db) / 2
                for i, w, _, de, db in angles
            )
        )

        # Independent discrete divergence evaluation.
        divergence = np.zeros(self.N)

        for i, k, w, _, de, db in edges:
            if idx(i) is not None:
                divergence[idx(i)] -= w * db

            if idx(k) is not None:
                divergence[idx(k)] += w * db

        for i, w, _, de, db in angles:
            divergence[idx(i)] += w * db

        self.bdiv = float(
            np.linalg.norm(divergence)
            / (self.energy0 + 1)
        )

        if self.bdiv > 1e-8:
            raise RuntimeError(
                "DISCRETE_MAGNETIC_WARD_FAILED"
            )

    def evaluate(self, t, constant=False):
        n = self.N

        def th(r):
            if constant:
                return float(1000 * t)

            return float(
                t * self.theta_coefficient
                * self.f0(r)
            )

        def boundary(i, k):
            if i == self.nr - 1 and k == 1:
                return float(
                    -th(self.L)
                    * self.basephi(self.L)
                )

            return 0.0

        def ix(i, k):
            if 0 < i < self.nr - 1:
                return k * n + i - 1
            return None

        rows, cols, vals = [], [], []
        rhs = np.zeros(2 * n)

        def insert(ids, w, theta, de, db, loc):
            H = (
                (1 + theta * theta, theta),
                (theta, 1.0),
            )

            source = (
                -w * (
                    theta * theta * de
                    + theta * db
                ),
                -w * theta * de,
            )

            for a in (0, 1):
                for e, s in enumerate((-1, 1)):
                    row = ids[a][e]

                    if row is None:
                        continue

                    rhs[row] += s * source[a]

                    for b in (0, 1):
                        for f, s2 in enumerate((-1, 1)):
                            col = ids[b][f]

                            value = (
                                w * H[a][b] * s * s2
                            )

                            if col is None:
                                rhs[row] -= (
                                    value
                                    * boundary(loc[f], b)
                                )
                            else:
                                rows.append(row)
                                cols.append(col)
                                vals.append(value)

        for i, k, w, rad, de, db in self.edges:
            ids = [
                [ix(i, a), ix(k, a)]
                for a in (0, 1)
            ]

            insert(
                ids, w, th(rad),
                de, db, (i, k),
            )

        for i, w, rad, de, db in self.angles:
            theta = th(rad)

            H = (
                (1 + theta * theta, theta),
                (theta, 1.0),
            )

            source = (
                -w * (
                    theta * theta * de
                    + theta * db
                ),
                -w * theta * de,
            )

            for a in (0, 1):
                row = ix(i, a)
                rhs[row] += source[a]

                for b in (0, 1):
                    rows.append(row)
                    cols.append(ix(i, b))
                    vals.append(w * H[a][b])

        matrix = coo_matrix(
            (vals, (rows, cols)),
            shape=(2 * n, 2 * n),
        ).tocsr()

        solution = spsolve(matrix, rhs)

        if not np.all(np.isfinite(solution)):
            raise RuntimeError(
                "NONFINITE_RECIPROCAL_MAXWELL_SOLUTION"
            )

        residual = float(
            np.linalg.norm(
                matrix @ solution - rhs
            )
            / max(
                1.0,
                np.linalg.norm(rhs),
            )
        )

        if residual > 1e-7:
            raise RuntimeError(
                "RECIPROCAL_MAXWELL_EOM_RESIDUAL"
            )

        energy = 0.0
        mixed = 0.0
        reference = 0.0

        for i, k, w, rad, de, db in self.edges:
            differences = []

            for a in (0, 1):
                low = (
                    solution[ix(i, a)]
                    if ix(i, a) is not None
                    else boundary(i, a)
                )

                high = (
                    solution[ix(k, a)]
                    if ix(k, a) is not None
                    else boundary(k, a)
                )

                differences.append(high - low)

            theta = th(rad)

            electric = de + differences[0]

            magnetic = (
                db + differences[1]
                + theta * electric
            )

            energy += (
                0.5 * w
                * (
                    electric**2
                    + magnetic**2
                )
            )

            mixed += (
                w * theta
                * electric * magnetic
            )

            reference += (
                w * theta * de * db
            )

        for i, w, rad, de, db in self.angles:
            theta = th(rad)

            electric = (
                de + solution[ix(i, 0)]
            )

            magnetic = (
                db + solution[ix(i, 1)]
                + theta * electric
            )

            energy += (
                0.5 * w
                * (
                    electric**2
                    + magnetic**2
                )
            )

            mixed += (
                w * theta
                * electric * magnetic
            )

            reference += (
                w * theta * de * db
            )

        ratio = (
            mixed / reference
            if abs(reference) > 1e-100
            else None
        )

        return {
            "t": t,
            "constant_theta": constant,
            "em_shape_energy": energy,
            "baseline_shape_energy": self.energy0,
            "mixed_weighted_integral": mixed,
            "reference_mixed_weighted_integral":
                reference,
            "scalar_source_projection_ratio": ratio,
            "relative_maxwell_residual": residual,
            "discrete_b_divergence": self.bdiv,
        }

    def roots(self, sign, scan=56):
        amplitudes = (
            sign * np.geomspace(
                1e-10, 1.0, scan
            )
        )

        cache = {}

        def equation(t):
            if t not in cache:
                cache[t] = self.evaluate(t)

            return (
                cache[t][
                    "scalar_source_projection_ratio"
                ]
                - t
            )

        values = [
            equation(float(t))
            for t in amplitudes
        ]

        roots = []

        for i in range(len(amplitudes) - 1):
            if values[i] * values[i + 1] < 0:
                root = float(
                    brentq(
                        equation,
                        float(amplitudes[i]),
                        float(amplitudes[i + 1]),
                        xtol=1e-15,
                        rtol=1e-10,
                    )
                )

                result = self.evaluate(root)

                result["projected_eom_error"] = (
                    float(equation(root))
                )

                roots.append(result)

        scan_record = {
            "scan_min_t": float(
                min(amplitudes)
            ),
            "scan_max_t": float(
                max(amplitudes)
            ),
            "number_of_samples": scan,
            "bracketed_root_count": len(roots),
            "global_uniqueness_proved": False,
        }

        return roots, scan_record


def main():
    ap = argparse.ArgumentParser()

    ap.add_argument("--u1", required=True)
    ap.add_argument("--radial", required=True)
    ap.add_argument("--out", required=True)

    args = ap.parse_args()

    if (
        sha(args.u1) != U1_HASH
        or sha(args.radial) != RADIAL_HASH
    ):
        raise RuntimeError(
            "PARENT_PROVENANCE_SHA_FAILED"
        )

    document = json.loads(
        Path(args.u1).read_bytes()
    )

    source = document[
        "selected_conditional_law"
    ]

    if (
        document["physical_survivors"] != 0
        or document["experiment"]
        != "G01-U1-AXION_MIXED_SOURCE_SCREENED_METRIC_FORK"
    ):
        raise RuntimeError(
            "INVALID_G01U1_PARENT_CLASSIFICATION"
        )

    radial = np.load(
        args.radial,
        allow_pickle=False,
    )

    for key in ("r", "f0", "f2", "mu"):
        if key not in radial.files:
            raise RuntimeError(
                "MISSING_RADIAL_PARENT_" + key
            )

    if abs(
        float(radial["mu"]) - 1.0
    ) > 1e-12:
        raise RuntimeError(
            "WRONG_MEDIATOR_RANGE"
        )

    configurations = (
        (8.0, 0.04),
        (16.0, 0.04),
        (32.0, 0.04),
        (48.0, 0.04),
        (48.0, 0.02),
    )

    cases = []

    for box, h in configurations:
        problem = Problem(
            radial, source, box, h
        )

        zero = problem.evaluate(0)
        null = problem.evaluate(
            1, constant=True
        )
        full = problem.evaluate(1)

        if abs(
            zero["em_shape_energy"]
            / problem.energy0 - 1
        ) > 1e-11:
            raise RuntimeError(
                "THETA_ZERO_BASELINE_DRIFT"
            )

        if abs(
            null["em_shape_energy"]
            / problem.energy0 - 1
        ) > 5e-5:
            raise RuntimeError(
                "CONSTANT_THETA_NULL_ENERGY_DRIFT"
            )

        if abs(
            null[
                "scalar_source_projection_ratio"
            ] - 1
        ) > 5e-5:
            raise RuntimeError(
                "CONSTANT_THETA_NULL_MIXED_DRIFT"
            )

        positive, pos_scan = problem.roots(1)
        negative, neg_scan = problem.roots(-1)

        case = {
            "box_radius_m": box,
            "grid_h_m": problem.h,
            "radial_nodes": problem.nr,
            "theta_strength_at_r1":
                problem.theta_coefficient
                * float(problem.f0(1)),
            "theta_strength_at_r3":
                problem.theta_coefficient
                * float(problem.f0(3)),
            "baseline": zero,
            "constant_theta_null": null,
            "full_G01U1_amplitude": full,
            "projected_positive_amplitude_roots":
                positive,
            "projected_negative_amplitude_roots":
                negative,
            "positive_scan": pos_scan,
            "negative_scan": neg_scan,
        }

        cases.append(case)

        print(
            "BOX", box,
            "H", problem.h,
            "MAXWELL_RESIDUAL",
            full["relative_maxwell_residual"],
            "FROZEN_SOURCE_RATIO",
            full[
                "scalar_source_projection_ratio"
            ],
            "ROOTS_POSITIVE",
            [v["t"] for v in positive],
            "ROOTS_NEGATIVE",
            [v["t"] for v in negative],
            flush=True,
        )

    finest = cases[-1]

    roots = (
        finest[
            "projected_positive_amplitude_roots"
        ]
        + finest[
            "projected_negative_amplitude_roots"
        ]
    )

    rootmax = (
        max(abs(row["t"]) for row in roots)
        if roots else None
    )

    # A separate source-shape negative control.
    # f0 alone is not the complete f0+f2 G01-U1 field.
    minor = np.linspace(
        0, 0.2, 81
    )[:, None]

    angle = (
        np.arange(1024)[None, :]
        * (2 * math.pi / 1024)
    )

    rho = (
        1 + minor * np.cos(angle)
    )

    height = (
        math.sqrt(3.2**2 - 1)
        + minor * np.sin(angle)
    )

    rr = np.hypot(rho, height)

    f0 = PchipInterpolator(
        radial["r"],
        radial["f0"],
    )

    acceleration_f0 = (
        -C**2
        * source["beta_dimensionless"]
        * source["source_axion_amplitude_A"]**2
        * f0(rr)
        * f0.derivative()(rr)
        * height / rr
    )

    # The G01-U1 Maxwell calibration was illustrative,
    # not a sourced equality to the historical R3B field.
    p_scale = (
        source["source_axion_amplitude_A"]
        / source[
            "source_kappa_m_per_J_assuming_illustrative_dipole_calibration"
        ]
    )

    illustrative_maxwell_energy = (
        6 * math.pi * p_scale
    )

    implied_ratio = (
        document[
            "historical_R3B_prescribed_capacity_j"
        ]
        / illustrative_maxwell_energy
    )

    if not roots:
        classification = (
            "NO_PROJECTED_ROOT_FOUND_"
            "NOT_A_NO_GO"
        )
    elif rootmax < 1e-3:
        classification = (
            "ONLY_SMALL_PROJECTED_ROOTS_"
            "IN_SCANNED_RANGE"
        )
    else:
        classification = (
            "LARGE_PROJECTED_ROOT_"
            "REQUIRES_FULL_EOM"
        )

    def mesh_change(key, index):
        old = cases[-2][key]
        new = cases[-1][key]

        if not old or not new:
            return None

        return abs(
            new[index]["t"]
            / old[index]["t"] - 1
        )

    gates = {
        "positive_small_root_relative_mesh_change":
            mesh_change(
                "projected_positive_amplitude_roots",
                0,
            ),
        "large_negative_root_relative_mesh_change":
            mesh_change(
                "projected_negative_amplitude_roots",
                -1,
            ),
        "strong_t1_source_ratio_relative_box_converged":
            False,
        "strong_t1_source_ratio_within_1e_7":
            all(
                abs(
                    row["full_G01U1_amplitude"][
                        "scalar_source_projection_ratio"
                    ]
                ) < 1e-7
                for row in cases[-3:]
            ),
        "projected_roots_are_not_full_scalar_EOM":
            True,
    }

    report = {
        "experiment":
            "G01-U2-RECIPROCAL-MAXWELL-RADIAL-DIPOLE-FORK",
        "utc":
            datetime.now(timezone.utc).isoformat(),
        "producer_sha256": sha(__file__),
        "parent_u1_sha256": U1_HASH,
        "parent_radial_sha256": RADIAL_HASH,
        "same_action_static_variation":
            "L=0.5 E_X^2-0.5 B_Y^2+theta(phi) E_X.dot.B_Y+sources; D_X=E_X+theta B_Y; H_Y=B_Y-theta E_X",
        "covariant_current_conservation":
            "U(1) Ward identities follow antisymmetry; X surface charge is net-zero dipolar, Y surface current is azimuthal divergence-free",
        "constant_theta_topological_null":
            "Explicitly tested on every grid",
        "static_gauge_Hessian":
            "[[1+theta^2,theta],[theta,1]], determinant 1",
        "full_Lorentzian_healthy_modes_certified":
            False,
        "source_shell_radius_m": R,
        "r3b_capacity_prescribed_j":
            document[
                "historical_R3B_prescribed_capacity_j"
            ],
        "G01U1_illustrative_dipole_maxwell_energy_j":
            illustrative_maxwell_energy,
        "G01U1_dipole_to_R3B_capacity_ratio":
            implied_ratio,
        "G01U1_field_normalization_independently_sourced":
            False,
        "theta2_angular_mode_included": False,
        "f0_radial_mode_included": True,
        "prescribed_shell_current_not_material_EOM":
            True,
        "fixed_shape_scalar_projected_amplitude_only":
            True,
        "projected_amplitude_equation":
            "scalar_source_projection_ratio(t)=t at fixed f0 shape; necessary but not sufficient scalar EOM",
        "results": cases,
        "mesh_domain_gates": gates,
        "largest_absolute_projected_root":
            rootmax,
        "root_classification":
            classification,
        "radial_f0_only_torus_min_m_s2_at_t1":
            float(np.min(acceleration_f0)),
        "radial_f0_only_torus_max_m_s2_at_t1":
            float(np.max(acceleration_f0)),
        "full_G01U1_f2_needed_for_positive_torus_sign":
            True,
        "best_projected_root_radial_f0_only_min_m_s2":
            (
                None if rootmax is None
                else float(
                    np.min(acceleration_f0)
                    * rootmax**2
                )
            ),
        "reached_full_outward_torus_1g": False,
        "fully_coupled_phi_X_Y_Einstein_solved": False,
        "current_microphysics": None,
        "whole_craft_force": None,
        "complete_operating_energy_j": None,
        "physical_survivors": 0,
        "full_regression": "NOT_RUN",
        "overall_heuristic_previous_percent": 37,
        "blocker_resolution_previous_percent": 33,
        "blocker_resolution_after_percent":
            "ASSESS_AFTER_INDEPENDENT_ANALYSIS",
        "scope":
            "Radial theta0, dipole X/Y Maxwell, prescribed surface currents, fixed scalar f0; no theta2, full scalar EOM, fluid or Einstein force",
    }

    out = Path(args.out)

    out.mkdir(
        parents=True,
        exist_ok=False,
    )

    raw = (
        json.dumps(
            report,
            sort_keys=True,
            indent=2,
            allow_nan=False,
        )
        + "\n"
    ).encode()

    with (out / "science.json").open("xb") as f:
        f.write(raw)

    (out / "science.json.sha256").write_text(
        hashlib.sha256(raw).hexdigest()
        + "  science.json\n"
    )

    print("G01U2_STATIC_GAUGE_WARD=PASS_REDUCED")
    print("G01U2_CONSTANT_THETA_NULL=PASS")
    print("G01U2_BOX_AND_MESH_CONVERGENCE=REPORTED")
    print("G01U2_FULL_SCALAR_AND_EINSTEIN=NOT_SOLVED")
    print("G01U2_PHYSICAL_SURVIVORS=0")
    print(
        "G01U2_SCIENCE_SHA256",
        hashlib.sha256(raw).hexdigest(),
    )
    print("G01U2_RESULT_DIR", out)


if __name__ == "__main__":
    main()
