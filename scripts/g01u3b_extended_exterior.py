"""G01-U3B: extended-exterior axion-Maxwell reciprocity gate.

PURPOSE
-------
Test whether the missing angular f2 scalar mode changes the
reciprocal X/Y Maxwell response previously restricted to f0
in G01-U2.

MODEL
-----
Fixed G01-U1 scalar:
    theta(r,mu) = t*K*(f0(r) + f2(r)*P2(mu))

Static gauge action:
    L = (E_X^2-B_Y^2)/2 + theta E_X.dot(B_Y)

Axisymmetric gauge potentials:
    E_X = -grad(V)
    B_Y = curl(A_phi e_phi)
    Psi = r*sin(polar_angle)*A_phi

The constant-theta interaction is a boundary term.
Integrating by parts exposes gradients of theta and
avoids the theta^2 constitutive stiffness used in U2.

The reference fields have prescribed electric dipole
surface charge and azimuthal magnetic shell current
on the radius-2-m spherical shell.

LIMITATIONS
-----------
The scalar f0+f2 profile remains frozen.
Charged source matter, neutral-fluid dynamics,
scalar Euler-Lagrange equations, metric Einstein
equations, Lorentzian constraints and whole-craft
forces are NOT solved.

Shape energies converted to joules use the original
illustrative U1 Maxwell calibration, NOT physical
source-energy certification.

A tiny algebraic linear-solver residual does not
establish angular, mesh or exterior convergence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math

from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from numpy.polynomial.legendre import Legendre, leggauss
from scipy.interpolate import PchipInterpolator
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve

R = 2.0
G = 6.67430e-11
C = 299792458.0

U1_SHA = (
    "0f5b138a22d9da0088cdb9d6c2bfdcfbb046603845447"
    "d250878809c454616c3"
)

RAD_SHA = (
    "cfe54027edcd6a33532faa5eec138455bc35a89193f9b3"
    "af1d4cd4f5bf727999"
)


def sha(path):
    return hashlib.sha256(
        Path(path).read_bytes()
    ).hexdigest()


def ref(r, m):
    """Exact theta-zero dipole shell field derivatives."""
    if r < R:
        v = -r / R
        dv = -1 / R
        psi = r * r / (2 * R)
        dpsi = r / R
    else:
        v = -R * R / (r * r)
        dv = 2 * R * R / (r**3)
        psi = R * R / (2 * r)
        dpsi = -R * R / (2 * r * r)

    vr = dv * m
    vmu = v
    qr = dpsi * (1 - m * m)
    qmu = -2 * m * psi

    return v*m, vr, vmu, psi*(1-m*m), qr, qmu


class Problem:
    def __init__(self, radial, source, L, h, ells, nmu=20):
        self.L = float(L)
        self.h = float(h)
        self.ells = tuple(ells)

        # Uniform resolution through 8 m, followed by a
        # geometric exterior mesh reaching 64 or 80 m.
        # Preserve exact shell alignment at R=2 m.
        inner_end = 8.0

        if (
            self.L <= inner_end
            or abs(round(R/h)*h-R) > 1e-9
            or abs(round(inner_end/h)*h-inner_end) > 1e-9
        ):
            raise ValueError("INVALID_RADIAL_GRID")

        inner = np.linspace(
            0, inner_end,
            int(round(inner_end/h))+1
        )

        outer = np.geomspace(
            inner_end, self.L, 97
        )[1:]

        self.rs = np.r_[inner, outer]
        self.nr = len(self.rs)-1
        self.nell = len(ells)
        self.nunknown = (self.nr-1) * self.nell
        self.n = 2*self.nunknown

        self.mu, self.mw = leggauss(nmu)

        self.poly = np.stack([
            Legendre.basis(l)(self.mu)
            for l in ells
        ])

        self.dpoly = np.stack([
            Legendre.basis(l).deriv()(self.mu)
            for l in ells
        ])

        self.qpoly = (
            (1-self.mu[None, :]**2)*self.dpoly
        )

        self.dqpoly = np.stack([
            -l*(l+1)*self.poly[k]
            for k, l in enumerate(ells)
        ])

        self.pp = (3*self.mu*self.mu-1)/2

        self.f0 = PchipInterpolator(
            radial["r"], radial["f0"]
        )
        self.f2 = PchipInterpolator(
            radial["r"], radial["f2"]
        )

        kappa = source[
            "source_kappa_m_per_J_assuming_illustrative_dipole_calibration"
        ]
        amplitude = source["source_axion_amplitude_A"]

        self.theta_scale = (
            C**4/(8*math.pi*G)*kappa*amplitude
        )
        self.illustrative_j = (
            6*math.pi*amplitude/kappa
        )

    def field(self, t, constant=False):
        rows, cols, vals = [], [], []
        rhs = np.zeros(self.n)
        cells = []

        for i in range(self.nr):
            r = (self.rs[i]+self.rs[i+1])/2
            dr = self.rs[i+1]-self.rs[i]

            f0 = float(self.f0(r))
            f2 = float(self.f2(r))
            df0 = float(self.f0.derivative()(r))
            df2 = float(self.f2.derivative()(r))

            ids, ends = [], []

            for side, s in ((i, -1), (i+1, 1)):
                if side in (0, self.nr):
                    continue

                for k in range(self.nell):
                    ids.append(
                        (side-1)*self.nell+k
                    )
                    ends.append((s, k))

            ids = np.array(ids, dtype=int)
            vid = ids
            qid = ids+self.nunknown

            for j, m in enumerate(self.mu):
                ang = self.pp[j]

                if constant:
                    theta = 1000*t
                    tr = 0.0
                    tm = 0.0
                else:
                    theta = (
                        t*self.theta_scale*(f0+f2*ang)
                    )
                    tr = (
                        t*self.theta_scale*(df0+df2*ang)
                    )
                    tm = (
                        t*self.theta_scale*f2*3*m
                    )

                vv = np.array([
                    .5*self.poly[k, j]
                    for s, k in ends
                ])
                vr = np.array([
                    s/dr*self.poly[k, j]
                    for s, k in ends
                ])
                vm = np.array([
                    .5*self.dpoly[k, j]
                    for s, k in ends
                ])
                qr = np.array([
                    s/dr*self.qpoly[k, j]
                    for s, k in ends
                ])
                qm = np.array([
                    .5*self.dqpoly[k, j]
                    for s, k in ends
                ])

                v0, vr0, vm0, p0, qr0, qm0 = ref(r, m)
                w = 2*math.pi*dr*self.mw[j]

                ke = w*(
                    r*r*np.outer(vr, vr)
                    +(1-m*m)*np.outer(vm, vm)
                )

                kb = -w*(
                    np.outer(qm, qm)/(r*r)
                    +np.outer(qr, qr)/(1-m*m)
                )

                cross = w*np.outer(
                    vv, tm*qr-tr*qm
                )

                local = np.block([
                    [ke, cross],
                    [cross.T, kb]
                ])

                local_ids = np.r_[vid, qid]
                length = len(local_ids)

                rows.extend(
                    np.repeat(local_ids, length).tolist()
                )
                cols.extend(
                    np.tile(local_ids, length).tolist()
                )
                vals.extend(local.ravel().tolist())

                rhs[vid] -= (
                    w*vv*(tm*qr0-tr*qm0)
                )
                rhs[qid] -= (
                    w*v0*(tm*qr-tr*qm)
                )

                cells.append((
                    r, m, w, theta,
                    vr0, vm0, qr0, qm0,
                    vid, qid, vr, vm, qr, qm
                ))

        matrix = coo_matrix(
            (vals, (rows, cols)),
            shape=(self.n, self.n)
        ).tocsr()

        solution = spsolve(matrix, rhs)

        residual = float(
            np.linalg.norm(matrix@solution-rhs)
            / max(1, np.linalg.norm(rhs))
        )

        if (
            not np.all(np.isfinite(solution))
            or residual > 1e-6
        ):
            raise RuntimeError(
                "STATIC_MAXWELL_EOM_RESIDUAL_FAILED:"
                +str(residual)
            )

        energy0 = energy1 = 0.0
        overlap0 = overlap1 = 0.0
        diff2 = norm2 = 0.0
        theta_max = 0.0

        source_changes = {
            l: 0.0 for l in (0, 2, 4, 6)
        }

        for (
            r, m, w, theta,
            vr0, vm0, qr0, qm0,
            vid, qid, vr, vm, qr, qm
        ) in cells:

            vr1 = vr0+float(np.dot(vr, solution[vid]))
            vm1 = vm0+float(np.dot(vm, solution[vid]))
            qr1 = qr0+float(np.dot(qr, solution[qid]))
            qm1 = qm0+float(np.dot(qm, solution[qid]))

            eb0 = (
                vr0*qm0-vm0*qr0
            )/(r*r)

            eb1 = (
                vr1*qm1-vm1*qr1
            )/(r*r)

            phi = float(
                self.f0(r)
                +self.f2(r)*(3*m*m-1)/2
            )

            energy0 += .5*w*(
                r*r*vr0**2
                +(1-m*m)*vm0**2
                +qm0**2/(r*r)
                +qr0**2/(1-m*m)
            )

            energy1 += .5*w*(
                r*r*vr1**2
                +(1-m*m)*vm1**2
                +qm1**2/(r*r)
                +qr1**2/(1-m*m)
            )

            overlap0 += w*r*r*phi*eb0
            overlap1 += w*r*r*phi*eb1

            diff2 += w*r*r*(eb1-eb0)**2
            norm2 += w*r*r*eb0**2

            theta_max = max(
                theta_max, abs(theta)
            )

            for l in source_changes:
                source_changes[l] += (
                    w*r*r*(eb1-eb0)
                    *float(Legendre.basis(l)(m))
                )

        return {
            "t": t,
            "constant_theta_null": constant,
            "angular_f2_included": True,
            "angular_modes": list(self.ells),
            "box_m": self.L,
            "grid_h_m": self.h,
            "static_maxwell_relative_residual": residual,
            "theta_abs_max_sampled": theta_max,
            "u2_H_log10_condition_estimate": (
                4*math.log10(theta_max)
                if theta_max > 10 else None
            ),
            "em_shape_energy_reference": energy0,
            "em_shape_energy": energy1,
            "illustrative_em_energy_j": (
                energy1/energy0*self.illustrative_j
            ),
            "scalar_source_projection_ratio": (
                overlap1/overlap0
            ),
            "source_L2_relative_difference": (
                math.sqrt(diff2/norm2)
            ),
            "multipole_source_changes": source_changes,
            "physical_survivors": 0,
        }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--u1", required=True)
    ap.add_argument("--radial", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()

    if (
        sha(args.u1) != U1_SHA
        or sha(args.radial) != RAD_SHA
    ):
        raise RuntimeError("PARENT_SHA_LOCK_FAILED")

    doc = json.loads(Path(args.u1).read_text())

    if doc["physical_survivors"] != 0:
        raise RuntimeError(
            "PARENT_PHYSICAL_CLASSIFICATION_DRIFT"
        )

    with np.load(
        args.radial, allow_pickle=False
    ) as archive:
        radial = {
            k: archive[k]
            for k in ("r", "f0", "f2", "mu")
        }

    if abs(float(radial["mu"])-1) > 1e-12:
        raise RuntimeError("PARENT_MEDIATOR_DRIFT")

    if args.quick:
        setups = [
            (64., .2, (1, 3, 5)),
            (80., .2, (1, 3, 5)),
            (80., .1, (1, 3, 5)),
            (80., .1, (1, 3, 5, 7)),
        ]
    else:
        setups = [
            (64., .1, (1, 3, 5, 7)),
            (80., .1, (1, 3, 5, 7)),
            (80., .05, (1, 3, 5, 7, 9)),
        ]

    results = []

    for L, h, ells in setups:
        problem = Problem(
            radial,
            doc["selected_conditional_law"],
            L, h, ells
        )

        f0b = float(problem.f0(L))
        f2b = float(problem.f2(L))

        boundary_theta = problem.theta_scale * max(
            abs(f0b+f2b),
            abs(f0b-f2b/2)
        )

        zero = problem.field(0)
        null = problem.field(1, constant=True)
        weak = problem.field(1e-8)
        medium = problem.field(1e-5)
        full = problem.field(1)

        if abs(
            null["em_shape_energy"]
            /zero["em_shape_energy"]-1
        ) > 1e-11:
            raise RuntimeError(
                "CONSTANT_AXION_NULL_FAILED"
            )

        if (
            zero["source_L2_relative_difference"]
            > 1e-12
        ):
            raise RuntimeError(
                "ZERO_COUPLING_NULL_FAILED"
            )

        results.append({
            "L": L,
            "h": h,
            "ells": list(ells),
            "outer_boundary_theta_max": boundary_theta,
            "radial_grid":
                "UNIFORM_TO_8M_GEOMETRIC_96_CELLS_OUTSIDE",
            "baseline": zero,
            "constant_theta": null,
            "weak": weak,
            "medium": medium,
            "full": full,
        })

        print(
            "BOX", L,
            "H", h,
            "ELL_MAX", max(ells),
            "THETA_MAX",
            full["theta_abs_max_sampled"],
            "SOURCE_RATIO",
            full["scalar_source_projection_ratio"],
            "EM_ENERGY_SHAPE",
            full["em_shape_energy"],
            "SOURCE_L2_DRIFT",
            full["source_L2_relative_difference"],
            "EOM_RELRES",
            full["static_maxwell_relative_residual"],
            "BOUNDARY_THETA",
            boundary_theta,
            flush=True,
        )

    report = {
        "experiment":
            "G01-U3B-EXTENDED-EXTERIOR-RECIPROCITY-GATE",
        "utc":
            datetime.now(timezone.utc).isoformat(),
        "producer_sha256": sha(__file__),
        "parent_u1_sha256": U1_SHA,
        "parent_radial_sha256": RAD_SHA,
        "action_static":
            "L=.5 E_X^2-.5 B_Y^2+theta(phi) E_X.B_Y",
        "angular_source":
            "theta=scale*(f0+f2*P2)",
        "constant_theta_exact_topological_null": True,
        "source_action":
            "PRESCRIBED_CHARGE_AND_CURRENT_ONLY",
        "scalar_EOM":
            "NOT_SOLVED_LOCAL_EOM",
        "gravity_and_earthcraft":
            "NOT_SOLVED",
        "full_regression":
            "NOT_RUN_BY_USER_POLICY",
        "physical_survivors": 0,
        "boundary_condition":
            "ZERO_CORRECTION_AT_EXTENDED_OUTER_RADIUS",
        "transparent_boundary_certified": False,
        "full_scalar_EOM_solved": False,
        "full_lorentzian_health_certified": False,
        "results": results,
    }

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=False)

    raw = (
        json.dumps(
            report,
            sort_keys=True,
            indent=2,
            allow_nan=False,
        )+"\n"
    ).encode()

    with (out/"science.json").open("xb") as f:
        f.write(raw)

    (out/"science.json.sha256").write_text(
        hashlib.sha256(raw).hexdigest()
        +"  science.json\n"
    )

    print(
        "SCIENCE_SHA256="
        +hashlib.sha256(raw).hexdigest()
    )
    print("PHYSICAL_SURVIVORS=0")
    print("FULL_REGRESSION=NOT_RUN")


if __name__ == "__main__":
    main()
