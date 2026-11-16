"""PH15-P2/P5: a restricted neutral counterwinding source experiment.

Purpose
-------
Solve a finite-box stationary two-complex-scalar/X-Maxwell problem and test
whether its on-shell X-sector fields can source a first-order Y response.

Also inspect a nonaxisymmetric, fixed-charge, fixed-total-J energy direction
which may destabilize the candidate.

Model
-----
Metric signature: (-,+,+,+).
Scalar charges: (+e, -e).
Scalar windings: (+n, -n).
Potential:
    U_i(s) = m_i**2*s - 2*s**2 + 2*s**3

Stationary ansatz:
    psi_i = f_i(rho,z)*exp(i*(omega_i*t+n_i*phi))
    A_X = A0(rho,z)*dt + rho*v(rho,z)*dphi

Computational region:
    rho >= 0, z >= 0, reflection-even source fields.

This is a numerical finite-box calculation in a hypothetical classical
source-sector theory. It does not establish full reciprocal X/Y solutions,
dynamical stability, free-space continuum convergence, physical source
particles, an SI energy scale, general relativity, or spacecraft lift.

All energies are canonical and are not joules.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from scipy.optimize import minimize
from scipy.sparse import diags, identity, kron, lil_matrix
from scipy.sparse.linalg import eigsh, spsolve


@dataclass(frozen=True)
class Spec:
    """Numerical and physical parameters in canonical units."""

    n: int = 36
    L: float = 18.0
    N: float = 800.0
    e: float = 0.05
    mminus: float = 1.0
    wind: int = 1


class Source:
    """Finite-volume scalar/X solver with fixed individual Noether charges."""

    def __init__(self, s: Spec):
        assert s.n >= 12
        assert s.L > 0
        assert s.N > 0
        assert s.e > 0
        assert s.mminus > 0
        assert abs(s.wind) <= 2

        self.s = s
        self.h = s.L / s.n

        n = s.n
        r = (np.arange(n) + 0.5) * self.h

        rho, z = np.meshgrid(r, r, indexing="ij")

        self.rho = rho.ravel()
        self.z = z.ravel()

        # Full-space azimuthal integration and z-reflection.
        self.w = 4 * np.pi * self.rho * self.h**2

        self.cells = n * n
        self.ang = 1 / self.rho**2

        # Positive spatial operator L = -Laplacian.
        # Outer boundary is Dirichlet; symmetry boundaries have zero
        # normal derivative for the even source variables.
        R = lil_matrix((n, n))
        Z = lil_matrix((n, n))

        for i in range(n):
            d = 0.0

            if i > 0:
                a = (r[i] - self.h / 2) / (r[i] * self.h**2)
                R[i, i - 1] = -a
                d += a

            if i < n - 1:
                a = (r[i] + self.h / 2) / (r[i] * self.h**2)
                R[i, i + 1] = -a
                d += a
            else:
                d += 2 * (r[i] + self.h / 2) / (r[i] * self.h**2)

            R[i, i] = d

        for j in range(n):
            d = 0.0

            if j > 0:
                Z[j, j - 1] = -1 / self.h**2
                d += 1 / self.h**2

            if j < n - 1:
                Z[j, j + 1] = -1 / self.h**2
                d += 1 / self.h**2
            else:
                d += 2 / self.h**2

            Z[j, j] = d

        I = identity(n, format="csr")

        self.L = (
            kron(R.tocsr(), I)
            + kron(I, Z.tocsr())
        ).tocsr()

        self.q = np.array([s.e, -s.e])
        self.spin = np.array([s.wind, -s.wind])
        self.mass = np.array([1.0, s.mminus])

    def seed(self):
        """Regular winding-compatible trial scalar profiles."""

        r2 = self.rho**2 + self.z**2
        ans = []

        for m in self.mass:
            width = 3.7 if self.s.wind else 4.6

            f = (
                (self.rho if self.s.wind else 1.0)
                * np.exp(-r2 / (2 * width**2))
            )

            f *= math.sqrt(
                self.s.N
                / (2 * m * np.dot(self.w, f * f))
                * 1.1
            )

            ans.append(f)

        return np.array(ans)

    def fields(self, F):
        """Solve the electrostatic and azimuthal X-Maxwell constraints."""

        f2 = F**2
        I = f2 @ self.w

        if np.min(I) < 1e-12:
            raise ArithmeticError("Degenerate scalar norm")

        massvec = 2 * (self.q**2 @ f2)

        D = (self.L + diags(massvec)).tocsc()

        omega = np.array([
            self.s.N / (2 * I[i])
            for i in range(2)
        ])

        # Frequencies and electric potential are determined together
        # by the individual Noether constraints and Gauss equation.
        for _ in range(60):
            A = spsolve(
                D,
                2 * ((self.q * omega) @ f2),
            )

            nxt = (
                self.s.N / 2
                + self.q * (f2 @ (self.w * A))
            ) / I

            if np.max(abs(nxt - omega)) < 2e-13:
                omega = nxt
                break

            omega = nxt
        else:
            raise ArithmeticError(
                "Noether/Gauss fixed point failed"
            )

        A = spsolve(
            D,
            2 * ((self.q * omega) @ f2),
        )

        W = omega[:, None] - self.q[:, None] * A

        # v is the physical azimuthal component:
        # A_X,phi = rho*v.
        v = spsolve(
            (
                self.L
                + diags(self.ang + massvec)
            ).tocsc(),
            2 * ((self.q * self.spin) @ f2) / self.rho,
        )

        V = (
            self.spin[:, None] / self.rho
            - self.q[:, None] * v
        )

        return A, v, omega, W, V

    def evaluation(self, x, details=False):
        """Fixed-charge energy and its constrained scalar derivative."""

        F = np.asarray(x).reshape(2, self.cells)

        A, v, omega, W, V = self.fields(F)
        f2 = F * F

        Ee = 0.5 * np.dot(
            self.w * A,
            self.L @ A,
        )

        Eb = 0.5 * np.dot(
            self.w * v,
            self.L @ v + self.ang * v,
        )

        E = Ee + Eb

        grad = []
        numbers = []
        scalar_res = []

        for k in range(2):
            f = F[k]
            ff = f2[k]

            U = (
                self.mass[k]**2 * ff
                - 2 * ff**2
                + 2 * ff**3
            )

            E += np.dot(
                self.w,
                W[k]**2 * ff
                + f * (self.L @ f)
                + V[k]**2 * ff
                + U,
            )

            r = (
                self.L @ f
                + (
                    self.mass[k]**2
                    - W[k]**2
                    + V[k]**2
                    - 4 * ff
                    + 6 * ff**2
                ) * f
            )

            grad.append(2 * self.w * r)

            scalar_res.append(
                float(np.sqrt(np.dot(self.w, r * r)))
            )

            numbers.append(
                float(2 * np.dot(self.w, W[k] * ff))
            )

        if not details:
            return float(E), np.concatenate(grad)

        rhoX = 2 * np.sum(
            self.q[:, None] * W * f2,
            axis=0,
        )

        jX = 2 * np.sum(
            self.q[:, None] * V * f2,
            axis=0,
        )

        result = {
            "spec": asdict(self.s),
            "energy": float(E),
            "Noether": numbers,
            "electric_charge": float(self.q @ numbers),
            "Jz": float(self.spin @ numbers),
            "omega": omega.tolist(),
            "electric_field_energy": float(Ee),
            "magnetic_field_energy": float(Eb),
            "Gauss_L2": float(
                np.linalg.norm(self.L @ A - rhoX)
            ),
            "Ampere_L2": float(
                np.linalg.norm(
                    (self.L @ v + self.ang * v) - jX
                )
            ),
            "scalar_EOM_weighted_L2": scalar_res,
            "max_abs_A0": float(np.max(abs(A))),
            "max_abs_v": float(np.max(abs(v))),
            "free_quanta_energy": float(
                self.s.N * sum(self.mass)
            ),
            "scope": "STATIONARY_FINITE_BOX_DISCRETE_X_ONLY",
        }

        return result, {
            "F": F,
            "A": A,
            "v": v,
            "W": W,
            "V": V,
            "jX": jX,
        }

    def solve(self, steps=240):
        """Minimize the constrained X-sector stationary energy."""

        rootw = np.sqrt(self.w)

        def fun(y):
            f = (
                y.reshape(2, self.cells) / rootw
            ).ravel()

            E, dE = self.evaluation(f)

            return E, (
                dE.reshape(2, self.cells) / rootw
            ).ravel()

        opt = minimize(
            fun,
            (self.seed() * rootw).ravel(),
            jac=True,
            method="L-BFGS-B",
            bounds=[(0.0, None)] * (2 * self.cells),
            options={
                "maxiter": steps,
                "ftol": 0.0,
                "gtol": 5e-9,
                "maxcor": 25,
                "maxls": 40,
            },
        )

        out, fields = self.evaluation(
            (
                opt.x.reshape(2, self.cells) / rootw
            ).ravel(),
            True,
        )

        out["optimizer"] = {
            "success": bool(opt.success),
            "iterations": int(opt.nit),
            "scaled_gradient_inf": float(
                np.max(abs(opt.jac))
            ),
            "message": str(opt.message),
        }

        f = fields["F"][0].reshape(
            self.s.n, self.s.n
        )

        r = (
            np.arange(self.s.n) + 0.5
        ) * self.h

        out["axis_u_ratio_f0_over_rho"] = (
            float(
                (f[0, 0] / r[0])
                / (f[1, 0] / r[1])
            )
            if self.s.wind
            else None
        )

        return out, fields

    def first_order_Y(self, fields, alpha=1.0):
        """Calculate linear induced Y on a fixed X-sector background.

        This is an O(alpha) calculation, not a simultaneous reciprocal
        X/Y/scalar solution.

        The Y potential uses odd z-reflection, as demanded by the
        parity of these source configurations.
        """

        n = self.s.n
        h = self.h

        F = fields["F"].reshape(2, n, n)
        v = fields["v"].reshape(n, n)
        A = fields["A"].reshape(n, n)

        W = fields["W"].reshape(2, n, n)
        V = fields["V"].reshape(2, n, n)

        rho = self.rho.reshape(n, n)

        def d(f, axis):
            return np.gradient(
                f,
                h,
                axis=axis,
                edge_order=2,
            )

        f2 = F * F

        K = np.sum(
            d(F, 1)**2
            + d(F, 2)**2
            + (V * F)**2
            - (W * F)**2,
            axis=0,
        )

        U = np.sum(
            self.mass[:, None, None]**2 * f2
            - 2 * f2**2
            + 2 * f2**3,
            axis=0,
        )

        lam = -2 * alpha * (K + 2 * U)

        lr = d(lam, 0)
        lz = d(lam, 1)

        Br = -d(v, 1)
        Bz = d(v, 0) + v / rho

        Er = -d(A, 0)
        Ez = -d(A, 1)

        # PH15-P1 constitutive signs.
        rhoY = -(lr * Br + lz * Bz)

        jY = (
            lr * d(A, 1)
            - lz * d(A, 0)
        )

        at_z0 = np.tile(
            np.arange(n) == 0,
            (n, 1),
        ).ravel()

        # Odd z parity: Dirichlet condition at the equator.
        Lodd = (
            self.L
            + diags(2 / h**2 * at_z0)
        ).tocsc()

        phi = spsolve(
            Lodd,
            rhoY.ravel(),
        ).reshape(n, n)

        vy = spsolve(
            (
                Lodd + diags(self.ang)
            ).tocsc(),
            jY.ravel(),
        ).reshape(n, n)

        EYr = -d(phi, 0)
        EYz = -d(phi, 1)

        BYr = -d(vy, 1)
        BYz = d(vy, 0) + vy / rho

        P = (
            Er * BYr
            + Ez * BYz
            + EYr * Br
            + EYz * Bz
        )

        w = self.w.reshape(n, n)
        z = self.z.reshape(n, n)

        mu = float(
            0.5 * np.dot(
                self.w,
                self.rho * fields["jX"],
            )
        )

        p = float(np.sum(w * lam * Bz))

        pvol = float(
            np.sum(w * z * rhoY)
        )

        eY = float(
            0.5 * np.sum(w * rhoY * phi)
        )

        bY = float(
            0.5 * np.sum(w * jY * vy)
        )

        actioncheck = float(
            np.sum(w * lam * P)
        )

        return {
            "Y_rho_L2": float(
                np.sqrt(np.sum(w * rhoY**2))
            ),
            "Y_jphi_L2": float(
                np.sqrt(np.sum(w * jY**2))
            ),
            "Y_electric_energy": eY,
            "Y_magnetic_energy": bY,
            "mu_X": mu,
            "p_Y": p,
            "p_Y_by_volume": pvol,
            "dipole_product_p_mu": float(mu * p),
            "dipole_axis_sigma_alphaP_coefficient": (
                float(alpha * mu * p / (4 * np.pi**2))
            ),
            "positive_beta_leading_farfield_can_reverse_sign": (
                False if alpha * mu * p < 0 else None
            ),
            "constitutive_identity_rel_error": float(
                abs(actioncheck - 2 * (bY - eY))
                / max(abs(actioncheck), 1e-15)
            ),
            "dipole_identity_rel_error": float(
                abs(pvol - p)
                / max(abs(p), abs(pvol), 1e-15)
            ),
            "P_abs_integral": float(
                np.sum(w * np.abs(P))
            ),
            "P_max_abs": float(
                np.max(abs(P))
            ),
            "Y_response": (
                "O(alpha)_FIXED_X_NOT_FULL_RECIPROCAL"
            ),
            "exterior_boundary": (
                "FINITE_BOX_DIRICHLET_NOT_FREE_SPACE_CERTIFIED"
            ),
        }

    def m0_energetic_saddle(self, fields, eps=0.01):
        """Test one physical charge-preserving energy-decrease path.

        This perturbation mixes an azimuthally independent scalar
        component into each winding species.

        Individual Noether charges remain fixed.
        Total angular momentum remains zero.
        Electric X charge cancels pointwise.

        The X magnetic potential is held fixed for this trial.
        A negative direction is an energetic warning, not a proof
        of a fully developed dynamical instability.
        """

        if self.s.mminus != 1.0 or abs(self.s.wind) != 1:
            raise ValueError(
                "Only symmetric counterwinding m0 perturbation"
            )

        f = fields["F"][0]
        w = self.w
        v = fields["v"]
        rho = self.rho

        assert (
            np.max(
                abs(
                    fields["F"][0]
                    - fields["F"][1]
                )
            ) < 1e-8
        )

        assert np.max(abs(fields["A"])) < 1e-8

        I0 = float(np.dot(w, f * f))

        rw = np.sqrt(w)
        omega = self.s.N / (2 * I0)

        M = (
            diags(rw)
            @ self.L
            @ diags(1 / rw)
            + diags(
                1
                - 8 * f * f
                + 18 * f**4
                - omega**2
                + (self.s.e * v)**2
            )
        ).tocsr()

        eig, vec = eigsh(
            M,
            k=1,
            which="SA",
            tol=1e-9,
            maxiter=30000,
        )

        g = vec[:, 0] / rw

        g *= math.sqrt(
            I0 / np.dot(w, g * g)
        )

        def E(t):
            a = math.sqrt(
                I0
                / (
                    I0
                    + t * t * np.dot(w, g * g)
                )
            )

            x = a * f
            y = a * t * g

            xx = x * x
            yy = y * y

            total = xx + yy

            gradient = np.dot(
                w,
                x * (self.L @ x)
                + y * (self.L @ y),
            )

            angle = np.dot(
                w,
                (
                    self.s.wind / rho
                    - self.s.e * v
                )**2 * xx
                + (self.s.e * v)**2 * yy,
            )

            # Analytic azimuthal average of the nonlinear
            # scalar self-interaction.
            U = (
                total
                - 2 * (
                    total**2
                    + 2 * xx * yy
                )
                + 2 * (
                    total**3
                    + 6 * total * xx * yy
                )
            )

            return 2 * (
                self.s.N**2 / (4 * I0)
                + gradient
                + angle
                + np.dot(w, U)
            )

        E0 = E(0)
        E1 = E(eps)

        return {
            "lowest_frozen_m0_eigenvalue": float(
                eig[0]
            ),
            "energy_delta_at_eps": float(
                E1 - E0
            ),
            "quadratic_coefficient": float(
                (
                    E(eps)
                    + E(-eps)
                    - 2 * E0
                ) / (2 * eps**2)
            ),
            "eps": eps,
            "Noether_each_fixed": float(self.s.N),
            "total_Jz": 0.0,
            "pointwise_electric_charge_zero": True,
            "classification": (
                "NEGATIVE_STATIC_ENERGY_DIRECTION_"
                "NOT_DYNAMICAL_SPECTRUM"
            ),
        }


def run(root: Path, mode="full"):
    """Execute registered finite-box sources and controls."""

    cases = [
        ("sym24", Spec(n=24)),
        ("sym36", Spec(n=36)),
        ("sym48", Spec(n=48)),
        ("sym36_L24", Spec(n=36, L=24)),
        ("sym48_L32", Spec(n=48, L=32)),
        (
            "asym28",
            Spec(n=28, mminus=1.08),
        ),
        (
            "asym40",
            Spec(n=40, mminus=1.08),
        ),
        (
            "nonwind36",
            Spec(n=36, wind=0),
        ),
        (
            "reverse36",
            Spec(n=36, wind=-1),
        ),
    ]

    if mode == "quick":
        cases = [
            cases[1],
            cases[5],
            cases[7],
        ]

    out = {}

    for name, s in cases:
        solver = Source(s)

        source, fields = solver.solve()

        source["linearY"] = solver.first_order_Y(
            fields
        )

        if name.startswith("sym"):
            source["m0Saddle"] = (
                solver.m0_energetic_saddle(fields)
            )

        out[name] = source

        print(
            name,
            "E",
            round(source["energy"], 5),
            "Yrho",
            round(
                source["linearY"]["Y_rho_L2"],
                7,
            ),
            "Yjphi",
            round(
                source["linearY"]["Y_jphi_L2"],
                7,
            ),
            "saddle",
            source.get(
                "m0Saddle", {}
            ).get("lowest_frozen_m0_eigenvalue"),
            flush=True,
        )

    d = {
        "branch": (
            "PH15-P2P5-FINITE_BOX_X_SOURCE_"
            "LINEAR_Y_NEGATIVE_ENERGY_MODE"
        ),
        "utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "model_scope": (
            "HYPOTHETICAL_FIXED_MINKOWSKI_"
            "SCALAR_X_PLUS_FIRST_ORDER_Y"
        ),
        "cases": out,
        "full_reciprocal": "NOT_SOLVED",
        "full_spectral_stability": "NOT_CERTIFIED",
        "source_realization": "NOT_IDENTIFIED",
        "SI_energy": "NOT_AVAILABLE",
        "Earth_craft_force": "NOT_DERIVED",
        "006D_replaced": False,
        "M5V_status": "FROZEN",
    }

    sourcefile = Path(__file__)

    d["source_SHA256"] = hashlib.sha256(
        sourcefile.read_bytes()
    ).hexdigest()

    stamp = datetime.now(
        timezone.utc
    ).strftime("%Y%m%dT%H%M%S%fZ")

    dest = (
        root
        / "results"
        / "data"
        / f"032h17_ph15_p2p5_{stamp}.json"
    )

    dest.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with dest.open("x") as fp:
        json.dump(
            d,
            fp,
            sort_keys=True,
            indent=2,
            allow_nan=False,
        )

    print("RESULT_PATH=" + str(dest))
    print(
        "RESULT_SHA256="
        + hashlib.sha256(
            dest.read_bytes()
        ).hexdigest()
    )

    return d


if __name__ == "__main__":
    if (
        len(sys.argv) > 1
        and sys.argv[1] not in ("quick", "full")
    ):
        raise SystemExit("Use quick or full")

    run(
        Path.cwd(),
        sys.argv[1] if len(sys.argv) > 1 else "full",
    )
