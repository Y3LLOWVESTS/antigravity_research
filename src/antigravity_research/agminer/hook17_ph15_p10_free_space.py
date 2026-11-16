"""PH15-P10: self-consistent free-space Coulomb source and Y preflight.

This experiment replaces the zero-Dirichlet electrostatic boundary of
PH15-P8 with a reciprocal, discrete free-space Coulomb Green operator.

The scalar profiles, electrostatic potential and both stationary scalar
frequencies are optimized together at fixed individual Noether charges.

The Y field is separately evaluated using a free-space azimuthal
Biot-Savart Green operator, at leading order in the trace coupling.

Both kernels approximate finite source cells using axisymmetric rings.
Diagonal cell self-interactions are treated using Gauss quadrature.

A discretely self-consistent Coulomb solution is NOT a continuum
free-space existence theorem. The scalar domain remains truncated.

No nonlinear X/Y reciprocity, dynamical spectrum, universal metric,
neutral Earth response, spacecraft force, or SI energy is established.
"""

from __future__ import annotations

import hashlib
import json
import sys

from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from scipy.linalg import eigh
from scipy.optimize import minimize
from scipy.special import ellipk, ellipe

from antigravity_research.agminer.hook17_ph15_p8_electric_dipole import (
    Dipole,
    Spec,
)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


class CoulombSource(Dipole):
    """PH15-P8 matter action with reciprocal free-space X/Y kernels."""

    def __init__(self, spec, self_order=8):
        super().__init__(spec)

        if self_order not in (4, 8, 12):
            raise ValueError("Unsupported self quadrature order")

        self.order = self_order

        n = self.cells
        r = self.rho
        z = self.z
        h = self.h

        G = np.empty((n, n), dtype=float)

        for start in range(0, n, 96):
            sl = slice(start, min(n, start + 96))

            a = r[sl, None]
            b = r[None, :]
            dz = z[sl, None] - z[None, :]

            den2 = (a + b)**2 + dz**2
            m = np.clip(4*a*b/den2, 0, 1-1e-14)

            G[sl] = (
                ellipk(m)
                / (2*np.pi**2*np.sqrt(den2))
            )

        # Finite-cell source integral for the diagonal self terms.
        roots, weights = np.polynomial.legendre.leggauss(
            self_order
        )
        offsets = .5*h*roots

        for j in range(n):
            source_r = r[j] + offsets
            source_z = z[j] + offsets

            p = source_r[:, None]
            zz = source_z[None, :]

            den2 = (
                (r[j] + p)**2
                + (z[j] - zz)**2
            )

            m = np.clip(
                4*r[j]*p/den2,
                0,
                1-1e-14,
            )

            point = (
                ellipk(m)
                / (2*np.pi**2*np.sqrt(den2))
            )

            weighted = (
                p*point
                * weights[:, None]
                * weights[None, :]
            )

            G[j, j] = float(
                np.sum(weighted)/(4*r[j])
            )

        self.kernel = G
        self.kernel_symmetry_inf = float(
            np.max(abs(G-G.T))
        )
        self.wkernel = G*self.w[None, :]

        # k=1 azimuthal Fourier component of the Coulomb Green
        # function. This also gives the orthonormal A_phi response
        # to a stationary azimuthal Y current.
        M = np.empty_like(G)

        for start in range(0, n, 96):
            sl = slice(start, min(n, start+96))

            a = r[sl, None]
            b = r[None, :]
            dz = z[sl, None] - z[None, :]

            den2 = (a+b)**2 + dz**2
            den = np.sqrt(den2)
            m = np.clip(4*a*b/den2, 0, 1-1e-14)

            calc = (
                ((2-m)*ellipk(m)-2*ellipe(m))
                / (2*np.pi**2*m*den)
            )

            M[sl] = np.where(
                m < 1e-3,
                m/(32*np.pi*den),
                calc,
            )

        for j in range(n):
            source_r = r[j]+offsets
            source_z = z[j]+offsets

            p = source_r[:, None]
            zz = source_z[None, :]

            den2 = (
                (r[j]+p)**2
                + (z[j]-zz)**2
            )
            den = np.sqrt(den2)

            m = np.clip(
                4*r[j]*p/den2,
                0,
                1-1e-14,
            )

            val = (
                ((2-m)*ellipk(m)-2*ellipe(m))
                / (2*np.pi**2*m*den)
            )

            val = np.where(
                m < 1e-3,
                m/(32*np.pi*den),
                val,
            )

            M[j, j] = float(
                np.sum(
                    p*val
                    * weights[:, None]
                    * weights[None, :]
                )/(4*r[j])
            )

        self.magkernel = M
        self.wmagkernel = M*self.w[None, :]
        self.mag_kernel_symmetry_inf = float(
            np.max(abs(M-M.T))
        )

    def fields(self, F):
        """Joint stationary X Coulomb and Noether-frequency iteration."""
        F = np.asarray(F).reshape(2, self.cells)

        s = F*F
        I = s@self.w

        if min(I) < 1e-12:
            raise ArithmeticError("Degenerate scalar norm")

        omega = self.s.N/(2*I)
        A = np.zeros(self.cells)

        for iteration in range(90):
            W = omega[:, None]-self.q[:, None]*A

            rho = 2*np.sum(
                self.q[:, None]*s*W,
                axis=0,
            )

            nextA = self.wkernel@rho

            nextOmega = (
                self.s.N/2
                + self.q*(s@(self.w*nextA))
            )/I

            delta = max(
                np.max(abs(nextA-A)),
                np.max(abs(nextOmega-omega)),
            )

            A = nextA
            omega = nextOmega

            if delta < 2e-12:
                break
        else:
            raise ArithmeticError(
                "Free-space Coulomb/Noether iteration failed"
            )

        W = omega[:, None]-self.q[:, None]*A

        rho = 2*np.sum(
            self.q[:, None]*s*W,
            axis=0,
        )

        residual = A-self.wkernel@rho

        return (
            A,
            W,
            omega,
            rho,
            float(np.max(abs(residual))),
            iteration+1,
        )

    def evaluation(self, y, details=False):
        """Fixed-Noether energy and independently differentiable residual."""
        F = (
            np.asarray(y).reshape(2, self.cells)
            / np.sqrt(self.w)
        )

        A, W, omega, rho, rmax, iterations = self.fields(F)
        ss = F*F

        # Using the solved Gauss constraint, total field plus
        # time-kinetic energy equals sum(omega_i*N_i/2).
        E = float(.5*self.s.N*sum(omega))

        grad = []
        eom = []

        for i in range(2):
            f = F[i]
            s = ss[i]

            E += np.dot(
                self.w,
                f*(self.L@f)
                + s-2*s*s+2*s**3,
            )

            residual = (
                self.L@f
                + (
                    1-W[i]**2
                    -4*s+6*s*s
                    +self.s.g*ss[1-i]
                )*f
            )

            grad.append(
                2*np.sqrt(self.w)*residual
            )

            eom.append(
                float(np.sqrt(
                    np.dot(
                        self.w,
                        residual**2,
                    )
                ))
            )

        E += self.s.g*np.dot(
            self.w,
            ss[0]*ss[1],
        )

        g = np.concatenate(grad)

        if not details:
            return E, g

        numbers = 2*(W*ss)@self.w
        charge = float(np.dot(self.w, rho))

        centers = [
            float(
                np.dot(self.w*self.z, ss[i])
                /np.dot(self.w, ss[i])
            )
            for i in range(2)
        ]

        outer = (
            np.sqrt(self.rho**2+self.z**2)
            > .8*self.s.L
        )

        tail = float(
            np.dot(
                self.w*outer,
                ss.sum(axis=0),
            )
            /np.dot(
                self.w,
                ss.sum(axis=0),
            )
        )

        electric = float(
            .5*np.dot(self.w*rho, A)
        )

        result = {
            "canonical_energy_NOT_J": E,
            "free_coulomb_field_energy": electric,
            "omega": omega.tolist(),
            "individual_Noether": numbers.tolist(),
            "net_X_charge": charge,
            "source_separation": centers[0]-centers[1],
            "centers": centers,
            "electric_dipole": float(
                np.dot(self.w*self.z, rho)
            ),
            "free_coulomb_residual_inf": rmax,
            "gauss_iterations": iterations,
            "scalar_equation_weighted_L2": eom,
            "outer_80pct_scalar_tail": tail,
            "kernel_symmetry_inf": self.kernel_symmetry_inf,
            "self_quadrature_order": self.order,
            "free_space_status": (
                "SELF_CONSISTENT_DISCRETE_COULOMB_"
                "BUT_SCALAR_TRUNCATED_AND_SELF_QUADRATURE_APPROXIMATE"
            ),
        }

        return result, {
            "F": F,
            "W": W,
            "A": A,
            "rho": rho,
        }

    def solve(self, iterations=300):
        """Vary both scalar profiles with X field re-solved at each step."""
        x = (
            self.seed()*np.sqrt(self.w)
        ).ravel()

        opt = minimize(
            self.evaluation,
            x,
            jac=True,
            method="L-BFGS-B",
            bounds=[(0, None)]*len(x),
            options={
                "maxiter": iterations,
                "ftol": 0.,
                "gtol": 4e-7,
                "maxls": 40,
                "maxcor": 20,
            },
        )

        out, fields = self.evaluation(opt.x, True)

        out["optimizer"] = {
            "success": bool(opt.success),
            "steps": int(opt.nit),
            "gradient_inf": float(np.max(abs(opt.jac))),
            "message": str(opt.message),
        }

        return out, fields

    def fd_gradient(self):
        """Independent central-difference audit of source energy."""
        y = (
            self.seed()*np.sqrt(self.w)
        ).ravel()

        _, g = self.evaluation(y)
        checks = []

        indices = (
            7,
            self.cells//2,
            self.cells+12,
            2*self.cells-15,
        )

        for i in indices:
            dy = 2e-5

            yp = y.copy()
            ym = y.copy()

            yp[i] += dy
            ym[i] -= dy

            numerical = (
                self.evaluation(yp)[0]
                - self.evaluation(ym)[0]
            )/(2*dy)

            checks.append({
                "index": i,
                "analytic": float(g[i]),
                "finite_difference": float(numerical),
                "abs_error": float(abs(numerical-g[i])),
            })

        return checks

    def induced_Y_free_space(self, fields, alpha=1.0):
        """First-order Y field from the self-sourced stationary X source.

        The Y field is solved with a free-space magnetic ring kernel.
        This does not backreact on X or matter at O(alpha**2).
        """
        shape = (self.nr, self.nz)
        h = self.h

        F = fields["F"].reshape(2, *shape)
        W = fields["W"].reshape(2, *shape)
        A = fields["A"].reshape(shape)

        rho = self.rho.reshape(shape)
        w = self.w.reshape(shape)

        def dr(x):
            return np.gradient(
                x, h, axis=-2, edge_order=2
            )

        def dz(x):
            return np.gradient(
                x, h, axis=-1, edge_order=2
            )

        ss = F*F

        K = np.sum(
            dr(F)**2
            + dz(F)**2
            - (W*F)**2,
            axis=0,
        )

        U = (
            np.sum(
                ss-2*ss**2+2*ss**3,
                axis=0,
            )
            +self.s.g*ss[0]*ss[1]
        )

        lam = -2*alpha*(K+2*U)

        # PH15-P1 exact stationary constitutive sign:
        # jY_phi = lambda_r*A0_z - lambda_z*A0_r.
        jphi = (
            dr(lam)*dz(A)
            -dz(lam)*dr(A)
        )

        v = (
            self.wmagkernel@jphi.ravel()
        ).reshape(shape)

        Br = -dz(v)
        Bz = dr(v)+v/rho

        Er = -dr(A)
        Ez = -dz(A)

        P = Er*Br+Ez*Bz

        energy = float(
            .5*np.dot(
                self.w*jphi.ravel(),
                v.ravel(),
            )
        )

        mu = float(
            .5*np.sum(w*rho*jphi)
        )

        outer = (
            np.sqrt(
                rho**2+self.z.reshape(shape)**2
            ) > .8*self.s.L
        )

        return {
            "Y_current_L2": float(np.sqrt(
                np.sum(w*jphi**2)
            )),
            "Y_magnetic_energy_CANONICAL_NOT_J": energy,
            "Y_magnetic_dipole": mu,
            "portal_P_abs_integral": float(
                np.sum(w*abs(P))
            ),
            "portal_alpha_P_max_abs_beta0": float(
                np.max(abs(alpha*P))
            ),
            "Y_field_outer_shell_max_abs": float(
                max(
                    np.max(abs(Br[outer])),
                    np.max(abs(Bz[outer])),
                )
            ),
            "Y_kernel_symmetry_inf": (
                self.mag_kernel_symmetry_inf
            ),
            "Y_response_status": (
                "FIRST_ORDER_FREE_SPACE_BIOT_SAVART_"
                "RING_QUADRATURE_NO_RECIPROCITY"
            ),
        }

    def free_density_quadratic(self, fields, k, a):
        """Static fixed-N density Hessian with k=1 free X-Gauss response.

        This is not the full dynamical scalar/gauge/metric spectrum.
        """
        if k != 1:
            raise ValueError(
                "Only k=1 has an audited angular Coulomb kernel"
            )

        F = fields["F"]
        W = fields["W"]
        s = F*F
        w = self.w

        a = np.asarray(a).reshape(2, self.cells)

        Q = 0.

        for i in range(2):
            b = F[i]*a[i]/2
            d = -F[i]*a[i]**2/8

            Q += .5*(
                np.dot(w*b, self.L@b)
                +2*np.dot(w*d, self.L@F[i])
                +k*k*np.dot(
                    w*b*b,
                    1/self.rho**2,
                )
            )

            Q += np.dot(
                w,
                (-1+3*s[i])*s[i]**2*a[i]**2,
            )

        Q += .5*self.s.g*np.dot(
            w,
            s[0]*s[1]*a[0]*a[1],
        )

        source = 2*np.sum(
            self.q[:, None]*W*s*a,
            axis=0,
        )

        mass = 2*np.sum(
            self.q[:, None]**2*s,
            axis=0,
        )

        # k=1 scalar Coulomb Green function equals the
        # cos(phi) Fourier component of the magnetic kernel.
        kern = self.wmagkernel

        x = np.zeros(self.cells)

        for _ in range(80):
            next_x = kern@(source-mass*x)

            if np.max(abs(next_x-x)) < 1e-12:
                x = next_x
                break

            x = next_x
        else:
            raise ArithmeticError(
                "Perturbed Gauss iteration failed"
            )

        Q += .25*np.dot(
            w*source,
            x,
        )

        return float(Q)

    def rotation_ward(self, fields):
        """Approximate rigid spatial rotation tangent and energy curvature."""
        F = fields["F"].reshape(
            2, self.nr, self.nz
        )

        rho = self.rho.reshape(
            self.nr, self.nz
        )
        z = self.z.reshape(
            self.nr, self.nz
        )

        dfr = np.gradient(
            F, self.h, axis=1, edge_order=2
        )
        dfz = np.gradient(
            F, self.h, axis=2, edge_order=2
        )

        tangent = (
            z[None, :, :]*dfr
            -rho[None, :, :]*dfz
        )

        norm = float(np.sum(
            self.w[None, :]
            * tangent.reshape(2, -1)**2
        ))

        if norm < 1e-10:
            return {
                "rotation_Q": 0.,
                "rotation_normalized_curvature": None,
                "rotation_tangent_norm": norm,
                "classification": (
                    "ROTATION_UNBROKEN_ZERO_TANGENT"
                ),
            }

        a = (
            2*tangent/np.maximum(F, 1e-25)
        )

        Q = self.free_density_quadratic(
            fields, 1, a
        )

        return {
            "rotation_Q": Q,
            "rotation_normalized_curvature": float(Q/norm),
            "rotation_tangent_norm": norm,
            "classification": (
                "FINITE_GRID_K1_ROTATION_WARD_"
                "NOT_CONTINUUM_CERTIFIED"
            ),
        }

    def k1_density_screen(self, fields, include_rotation=True):
        """12 density envelopes plus the rigid-rotation tangent."""
        F = fields["F"]
        ss = F*F

        zcenters = [
            np.dot(
                self.w*self.z,
                ss[i],
            )/np.dot(self.w, ss[i])
            for i in range(2)
        ]

        basis = []

        for i in range(2):
            for rc in (1.5, 4.):
                for offset in (-2.5, 0., 2.5):
                    envelope = (
                        (self.rho/3)
                        *np.exp(-(
                            (self.rho-rc)**2
                            +(self.z-zcenters[i]-offset)**2
                        )/(2*3.3**2))
                    )

                    b = np.zeros((2, self.cells))
                    b[i] = envelope
                    basis.append(b)

        if include_rotation:
            FF = F.reshape(2, self.nr, self.nz)

            dfr = np.gradient(
                FF, self.h, axis=1, edge_order=2
            )
            dfz = np.gradient(
                FF, self.h, axis=2, edge_order=2
            )

            tan = (
                self.z.reshape(
                    self.nr, self.nz
                )[None, :, :]*dfr
                -self.rho.reshape(
                    self.nr, self.nz
                )[None, :, :]*dfz
            )

            basis.append(
                (
                    2*tan/np.maximum(FF, 1e-25)
                ).reshape(2, -1)
            )

        basis = np.array(basis)
        n = len(basis)

        H = np.zeros((n, n))
        G = np.zeros((n, n))

        def quad(v):
            return self.free_density_quadratic(
                fields, 1, v
            )

        for i in range(n):
            H[i, i] = quad(basis[i])

            for j in range(i+1, n):
                hij = .25*(
                    quad(basis[i]+basis[j])
                    -quad(basis[i]-basis[j])
                )
                H[i, j] = hij
                H[j, i] = hij

            for j in range(n):
                G[i, j] = np.sum(
                    self.w[None, :]
                    *ss*basis[i]*basis[j]
                )

        eig = eigh(
            H,
            (G+G.T)/2,
            eigvals_only=True,
        )

        return {
            "basis": n,
            "min_mode": float(eig[0]),
            "second_mode": float(eig[1]),
            "gram_condition": float(np.linalg.cond(G)),
            "included_rigid_rotation": bool(include_rotation),
            "scope": (
                "FREE_SPACE_GAUSS_K1_12_ENVELOPES_"
                "PLUS_ROTATION_STATIC_DENSITY_ONLY"
            ),
        }

    def translation_ward(self, fields):
        """Numerical k=0 common-translation Hessian-tangent diagnostic."""
        f = fields["F"].reshape(
            2, self.nr, self.nz
        )

        dz = np.gradient(
            f, self.h, axis=2, edge_order=2
        )

        tangent = (
            (-dz).ravel()
            *np.tile(np.sqrt(self.w), 2)
        )

        y = (
            f.reshape(2, -1)
            *np.sqrt(self.w)
        ).ravel()

        eps = (
            .003/max(1., np.max(abs(tangent)))
        )

        E0, g0 = self.evaluation(y)

        Ep, gp = self.evaluation(
            y+eps*tangent
        )

        Em, gm = self.evaluation(
            y-eps*tangent
        )

        htan = (
            gp-gm
        )/(2*eps)

        curvature = (
            (Ep+Em-2*E0)
            /(eps**2*np.dot(tangent, tangent))
        )

        return {
            "translation_tangent_rayleigh": float(curvature),
            "H_tangent_norm_ratio": float(
                np.linalg.norm(htan)
                /np.linalg.norm(tangent)
            ),
            "stationary_gradient_norm": float(
                np.linalg.norm(g0)
            ),
            "epsilon": float(eps),
            "scope": (
                "DISCRETE_TRANSLATION_TANGENT_"
                "ZERO_MODE_APPROXIMATION"
            ),
        }


def perform(spec, order=8):
    """One source with conservation, Y, Ward and variation diagnostics."""
    model = CoulombSource(spec, order)
    result, fields = model.solve(350)

    if (
        max(result["scalar_equation_weighted_L2"]) > 1e-4
        or abs(result["net_X_charge"]) > 1e-7
    ):
        raise ArithmeticError(
            "Source EOM or neutrality gate failed"
        )

    result["spec"] = asdict(spec)
    result["gradient_audit"] = model.fd_gradient()
    result["translation_ward"] = model.translation_ward(fields)
    result["rotation_ward"] = model.rotation_ward(fields)
    result["k1_density_screen"] = model.k1_density_screen(fields)
    result["free_space_Y_first_order"] = (
        model.induced_Y_free_space(fields)
    )

    rot = result["rotation_ward"][
        "rotation_normalized_curvature"
    ]

    print(
        "CASE",
        spec.nr,
        spec.L,
        "sep",
        round(result["source_separation"], 7),
        "E",
        round(result["canonical_energy_NOT_J"], 7),
        "tail",
        round(result["outer_80pct_scalar_tail"], 9),
        "tmode",
        round(
            result["translation_ward"][
                "translation_tangent_rayleigh"
            ], 8
        ),
        "Y",
        round(
            result["free_space_Y_first_order"][
                "Y_current_L2"
            ], 7
        ),
        "rot",
        round(rot, 8) if rot is not None else None,
        "k1min",
        round(
            result["k1_density_screen"]["min_mode"], 8
        ),
        flush=True,
    )

    return result


def run(root, quick=False):
    """Execute fixed, auditable research cases and immutable results."""
    cases = [
        ("base18_L12", Spec(nr=18, L=12), 8),
        ("refine27_L12", Spec(nr=27, L=12), 8),
        ("large24_L16", Spec(nr=24, L=16), 8),
        ("large30_L20", Spec(nr=30, L=20), 8),
        ("fine36_L16", Spec(nr=36, L=16), 8),
        ("coarse12_L12", Spec(nr=12, L=12), 8),
        ("seed0_overlap18", Spec(
            nr=18, L=12, seed_separation=0
        ), 8),
        ("seed0p5_18", Spec(
            nr=18, L=12, seed_separation=.5
        ), 8),
        ("seed6_18", Spec(
            nr=18, L=12, seed_separation=6
        ), 8),
        ("control_g0", Spec(
            nr=18, L=12, g=0
        ), 8),
        ("control_e0p14", Spec(
            nr=18, L=12, e=.14
        ), 8),
        ("selfquad4", Spec(nr=18, L=12), 4),
        ("selfquad12", Spec(nr=18, L=12), 12),
    ]

    if quick:
        cases = cases[:1]

    out = {
        name: perform(spec, order)
        for name, spec, order in cases
    }

    guards = {}

    if not quick:
        a = out["large24_L16"]
        b = out["large30_L20"]

        guards["fixed_h_separation_rel_below_0p2pct"] = (
            abs(
                a["source_separation"]
                -b["source_separation"]
            )/abs(b["source_separation"]) < .002
        )

        guards["fixed_h_Y_current_delta_below_0p005"] = (
            abs(
                a["free_space_Y_first_order"]["Y_current_L2"]
                -b["free_space_Y_first_order"]["Y_current_L2"]
            ) < .005
        )

        guards["finer_mesh_translation_softens"] = (
            out["fine36_L16"]["translation_ward"][
                "translation_tangent_rayleigh"
            ]
            <a["translation_ward"][
                "translation_tangent_rayleigh"
            ]
        )

        guards["finer_mesh_rotation_softens"] = (
            out["fine36_L16"]["rotation_ward"][
                "rotation_normalized_curvature"
            ]
            <a["rotation_ward"][
                "rotation_normalized_curvature"
            ]
        )

        guards["separation_lowers_same_action_energy"] = (
            out["seed0_overlap18"]["canonical_energy_NOT_J"]
            -out["base18_L12"]["canonical_energy_NOT_J"]
            > .2
        )

        guards["g0_null_channel"] = (
            abs(out["control_g0"]["source_separation"]) < .005
            and
            out["control_g0"]["free_space_Y_first_order"][
                "Y_current_L2"
            ] < 1e-4
        )

        guards["selfquad8_to12_separation_delta_below_0p002"] = (
            abs(
                out["base18_L12"]["source_separation"]
                -out["selfquad12"]["source_separation"]
            ) < .002
        )

        guards["source_gradient_FD_below_3e_minus7"] = (
            max(
                x["abs_error"]
                for x in out["base18_L12"]["gradient_audit"]
            ) < 3e-7
        )

    # Convert NumPy booleans to JSON-native values.
    guards = {
        name: bool(value)
        for name, value in guards.items()
    }

    successful = bool(
        guards and all(guards.values())
    )

    artifact = {
        "branch": (
            "032H17_PH15_P10_SELFCONSISTENT_DISCRETE_"
            "FREE_COULOMB_AND_FREE_Y"
        ),
        "timestamp_utc": datetime.now(
            timezone.utc
        ).isoformat(),
        "source_sha256": sha(__file__),
        "parent_source_sha256": sha(
            Path(__file__).with_name(
                "hook17_ph15_p8_electric_dipole.py"
            )
        ),
        "cases": out,
        "physical_gates": guards,
        "candidate_status": (
            "YELLOW_NEW_PARTIAL_EXTERIOR_CLOSURE"
            if successful
            else "RED_OR_INCOMPLETE"
        ),
        "free_space_status": (
            "SELF_CONSISTENT_DISCRETE_COULOMB_KERNEL;"
            " NOT_CONTINUUM_CERTIFIED"
        ),
        "Y_status": (
            "FIRST_ORDER_FREE_SPACE_BIOT_SAVART;"
            " X_Y_BACKREACTION_OPEN"
        ),
        "full_gauge_and_dynamic_spectral_stability": (
            "NOT_CERTIFIED"
        ),
        "physical_metric_and_earth_response": (
            "NOT_DERIVED"
        ),
        "complete_energy_SI": "NOT_AVAILABLE",
        "fifty_percent_theory_gate": "NOT_MET",
        "006D_replaced": False,
        "M5V_status": "FROZEN",
    }

    stamp = datetime.now(
        timezone.utc
    ).strftime("%Y%m%dT%H%M%S%fZ")

    target = (
        root
        /"results"
        /"data"
        /f"032h17_ph15_p10_{stamp}.json"
    )

    target.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with target.open("x") as stream:
        json.dump(
            artifact,
            stream,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )

    print("RESULT_PATH="+str(target))
    print("RESULT_SHA256="+sha(target))
    print(
        "PH15_P10_RESULT="
        +artifact["candidate_status"]
    )

    if not quick and not successful:
        raise SystemExit(
            "PH15-P10 numerical gates did not all pass"
        )

    return artifact


if __name__ == "__main__":
    if (
        len(sys.argv) > 1
        and sys.argv[1] not in ("quick", "full")
    ):
        raise SystemExit(
            "Usage: python module.py quick|full"
        )

    run(
        Path.cwd(),
        quick=(
            len(sys.argv) > 1
            and sys.argv[1] == "quick"
        ),
    )
