"""PH15-P9: independent electrostatic exterior and angular Gauss-response audit.

Operates on PH15-P8 fixed-Minkowski X-only stationary backgrounds. All source
energies and lengths are canonical (NOT SI). The elliptic-integral free-space
boundary evaluation is a one-shot field diagnostic, not an on-shell free-space
source solve. The angular Hessian includes both scalar density species and the
linearized electrostatic Gauss response; it is not full dynamic gauge/metric
stability. No 50% certification, physical matter realization, Earth-craft force.
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
from scipy.special import ellipk
from scipy.sparse import diags, eye, kron, csr_matrix
from scipy.sparse.linalg import splu, spsolve

from antigravity_research.agminer.hook17_ph15_p8_electric_dipole import Dipole, Spec


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def free_ring_potential(model, charge, rb, zb):
    """Free-space potential of axisymmetric cell-center charge rings.

    Includes the Maxwell Coulomb normalization 1/(4*pi).
    A cell is approximated by a ring at its center.
    Grid convergence remains necessary.
    """
    rb = np.asarray(rb, dtype=float).ravel()
    zb = np.asarray(zb, dtype=float).ravel()

    if rb.shape != zb.shape:
        raise ValueError("Boundary point coordinates mismatch")

    rp = model.rho[None, :]
    zp = model.z[None, :]
    dx = rb[:, None]
    dz = zb[:, None] - zp

    den2 = (dx + rp)**2 + dz**2

    if np.min(den2) <= 0:
        raise ValueError("Evaluation coincides with a source ring")

    den = np.sqrt(den2)
    m = np.clip(4*dx*rp/den2, 0, 1-1e-15)

    # w=2*pi*rho*h^2.
    # Azimuthal Coulomb integral is 4*K(m)/den.
    kernel = ellipk(m)/(2*np.pi**2*den)

    return kernel @ (model.w*charge)


def boundary_audit(model, fields):
    """One-shot free-space Coulomb boundary correction.

    At the P8 source's fixed charge distribution, find the free-space
    ring-potential values at the outer faces, then solve the homogeneous
    interior Laplace correction.

    The scalar source, omega and charge density are NOT re-solved.
    Hence this is NOT an on-shell free-space configuration.
    """
    n = model.nr
    nz = model.nz
    h = model.h

    r = (np.arange(n)+.5)*h
    z = (np.arange(nz)+.5)*h-model.s.L

    charge = fields["charge"]

    if abs(np.dot(model.w, charge)) > 1e-7:
        raise ArithmeticError("Source is not sufficiently neutral")

    rface = np.full(nz, model.s.L)

    gr = free_ring_potential(model, charge, rface, z)
    gt = free_ring_potential(
        model, charge, r, np.full(n, model.s.L)
    )
    gb = free_ring_potential(
        model, charge, r, np.full(n, -model.s.L)
    )

    boundary_rhs = np.zeros((n, nz))

    boundary_rhs[-1, :] += (
        2*model.s.L/(r[-1]*h*h)*gr
    )
    boundary_rhs[:, 0] += 2*gb/(h*h)
    boundary_rhs[:, -1] += 2*gt/(h*h)

    delta = spsolve(
        model.L.tocsc(),
        boundary_rhs.ravel()
    )

    a0 = fields["A"]
    p = float(np.dot(model.w*model.z, charge))

    def dipole_approx(radial, axial):
        return p*axial / (
            4*np.pi*(radial**2+axial**2)**1.5
        )

    prediction = np.concatenate((
        dipole_approx(rface, z),
        dipole_approx(r, np.full(n, model.s.L)),
        dipole_approx(r, np.full(n, -model.s.L))
    ))

    exact = np.concatenate((gr, gt, gb))

    dipole_error = (
        np.linalg.norm(prediction-exact)
        / max(np.linalg.norm(exact), 1e-15)
    )

    E0 = float(.5*np.dot(model.w*charge, a0))
    dE = float(.5*np.dot(model.w*charge, delta))

    residual = float(np.linalg.norm(
        model.L @ delta-boundary_rhs.ravel()
    ))

    return {
        "net_X_charge": float(np.dot(model.w, charge)),
        "dipole_X_canonical": p,
        "E_dirichlet_electric_CANONICAL": E0,
        "E_one_shot_free_space_ring_boundary_correction_CANONICAL": dE,
        "E_one_shot_corrected_electric_CANONICAL": E0+dE,
        "relative_electrostatic_correction": float(
            dE/max(E0, 1e-14)
        ),
        "boundary_free_ring_potential_L2": float(
            np.linalg.norm(exact)
        ),
        "boundary_dipole_only_approx_rel_L2": float(
            dipole_error
        ),
        "boundary_harmonic_solver_residual_L2": residual,
        "scope": "FROZEN_DENSITIES_FIXED_OMEGA_ONE_SHOT_RING_QUADRATURE",
        "free_space_source_stationarity": "NOT_CERTIFIED",
        "full_exterior_Y": "NOT_CERTIFIED",
    }


def angular_basis(model, fields, k):
    """Twelve regular density harmonics, six for each scalar species."""
    if k < 1 or int(k) != k:
        raise ValueError("Positive integral harmonic required")

    centers = np.array([
        np.dot(model.w*model.z, fields["F"][i]**2)
        / np.dot(model.w, fields["F"][i]**2)
        for i in (0, 1)
    ])

    result = []

    for i in (0, 1):
        for rc in (1.5, 4.0):
            for offset in (-2.5, 0., 2.5):
                envelope = (
                    (model.rho/3.)**k
                    * np.exp(-(
                        (model.rho-rc)**2
                        + (model.z-centers[i]-offset)**2
                    )/(2*3.3**2))
                )

                a = np.zeros((2, model.cells))
                a[i] = envelope
                result.append(a)

    return np.array(result)


def density_quadratic(model, fields, k, a, solver=None):
    """Fixed-Noether density second variation with responsive X Gauss field.

    Scalar densities:
        s_i(t)=s_i*(1+t*a_i*cos(k*phi)).

    Derive from H-sum(omega_i*N_i), and eliminate the linearized
    electrostatic harmonic from the same X-only action.

    The first-order individual Noether variations integrate to zero.
    Second-order frequency adjustments cancel from the constrained
    second variation by background stationarity.
    """
    F = fields["F"]
    W = fields["W"]
    s = F*F
    w = model.w
    a = np.asarray(a).reshape(2, model.cells)

    Q = 0.

    for i in (0, 1):
        b = F[i]*a[i]/2.
        d = -F[i]*a[i]**2/8.

        Q += .5*(
            np.dot(w*b, model.L @ b)
            + 2*np.dot(w*d, model.L @ F[i])
            + k*k*np.dot(w*b*b, 1/model.rho**2)
        )

        Q += np.dot(
            w,
            (-1+3*s[i])*s[i]**2*a[i]**2
        )

    Q += .5*model.s.g*np.dot(
        w,
        s[0]*s[1]*a[0]*a[1]
    )

    # Linearized electric X charge source.
    source = 2*np.sum(
        model.q[:, None]*W*s*a,
        axis=0
    )

    D = model.L + diags(
        k*k/model.rho**2
        + 2*np.sum(
            model.q[:, None]**2*s,
            axis=0
        )
    )

    if solver is None:
        response = spsolve(D.tocsc(), source)
    else:
        response = solver(source)

    # Correct Gauss-relaxed positive Coulomb term.
    Qelectro = .25*np.dot(
        w*source,
        response
    )

    Q += Qelectro

    residual = float(np.linalg.norm(
        D @ response-source
    ))

    return float(Q), {
        "Q_electric_positive": float(Qelectro),
        "gauss_k_L2": residual,
        "linear_electric_source_L2": float(
            np.sqrt(np.dot(w, source*source))
        ),
    }


def density_modes(model, fields, k):
    """Gauss-relaxed generalized Hessian in a 12-dimensional scalar basis."""
    B = angular_basis(model, fields, k)
    n = len(B)

    F = fields["F"]
    s = F*F
    w = model.w

    def gram(a, b):
        return float(
            np.sum(w[None, :]*s*a*b)
        )

    G = np.array([
        [gram(B[i], B[j]) for j in range(n)]
        for i in range(n)
    ])

    D = (
        model.L
        + diags(
            k*k/model.rho**2
            + 2*np.sum(
                model.q[:, None]**2*s,
                axis=0
            )
        )
    ).tocsc()

    LU = splu(D)

    def quad(v):
        return density_quadratic(
            model, fields, k, v, solver=LU.solve
        )[0]

    H = np.zeros((n, n))

    for i in range(n):
        H[i, i] = quad(B[i])

        for j in range(i+1, n):
            hij = .25*(
                quad(B[i]+B[j])
                - quad(B[i]-B[j])
            )
            H[i, j] = hij
            H[j, i] = hij

    H = (H+H.T)/2

    eig, vectors = eigh(H, G)

    v = np.tensordot(
        vectors[:, 0], B, axes=1
    )

    Q, detail = density_quadratic(
        model, fields, k, v, solver=LU.solve
    )

    norm = gram(v, v)

    eigen_residual = float(np.linalg.norm(
        H @ vectors[:, 0]
        - eig[0]*(G @ vectors[:, 0])
    ))

    return {
        "k": k,
        "basis_dimension": n,
        "lowest_density_mode": float(eig[0]),
        "highest_density_mode": float(eig[-1]),
        "lowest_mode_Q": Q,
        "lowest_mode_norm": norm,
        "lowest_mode_gauss_L2": detail["gauss_k_L2"],
        "lowest_mode_Q_electric": detail["Q_electric_positive"],
        "lowest_mode_source_L2": detail["linear_electric_source_L2"],
        "gram_condition": float(np.linalg.cond(G)),
        "eigenpair_residual": eigen_residual,
        "phase_amplitude_cross": (
            "EXACT_ZERO_AT_QUADRATIC_ORDER_"
            "NO_BACKGROUND_SPATIAL_CURRENT"
        ),
        "phase_sector": (
            "NONNEGATIVE_STATIC_SPATIAL_GRADIENT_ENERGY"
        ),
        "dynamic_constraint_stability": "NOT_CERTIFIED",
        "angular_basis_scope": (
            "12_ENVELOPES_TWO_SPECIES_k_HARMONIC"
        ),
    }, v


def matched_fd_check(model, fields, k, h, t=.03):
    """Independent P8 azimuthal quadrature, Gauss-matched scalar deformation."""
    f = fields["F"]
    W = fields["W"]
    s = f*f

    m = W*s
    den = m.sum(axis=0)

    a = np.stack((
        m[1]/den*h,
        m[0]/den*h
    ))

    q, detail = density_quadratic(
        model, fields, k, a
    )

    E0 = model.matched_angular_trial(
        fields, k, h, 0., angles=32
    )
    Ep = model.matched_angular_trial(
        fields, k, h, +t, angles=32
    )
    Em = model.matched_angular_trial(
        fields, k, h, -t, angles=32
    )

    fd = (Ep+Em-2*E0)/(2*t*t)

    return {
        "analytic_Q": q,
        "finite_angle_Q": float(fd),
        "abs_error": float(abs(fd-q)),
        "relative_error": float(
            abs(fd-q)/max(1e-12, abs(q))
        ),
        "Gauss_source_L2": detail["linear_electric_source_L2"],
    }


def independent_3d_energy(model, fields, k, a, t, angles=16):
    """Independent nonlinear 3D angular Gauss + individual Noether solve.

    Re-solves X Gauss and both source frequencies after deforming the
    scalar densities in phi. Uses a Fourier-spectral azimuthal
    Laplacian and P8's radial/z finite-volume operator.

    This is an independent finite-box energy verification, not a
    three-dimensional stationary source or a dynamical simulation.
    """
    if angles < 4*k+8 or angles % 2:
        raise ValueError("Insufficient even azimuthal resolution")

    a = np.asarray(a).reshape(2, model.cells)

    phis = 2*np.pi*np.arange(angles)/angles
    cosine = np.cos(k*phis)

    base = fields["F"]**2

    s3 = base[:, :, None]*(
        1+t*a[:, :, None]*cosine[None, None, :]
    )

    if np.min(s3) <= 0:
        raise ValueError("Nonpositive perturbed scalar density")

    f3 = np.sqrt(s3)

    w3 = np.broadcast_to(
        model.w[:, None]/angles,
        (model.cells, angles)
    ).ravel()

    freqs = np.fft.fftfreq(
        angles,
        d=1./angles
    )

    identity = np.eye(angles)

    Lphi = np.fft.ifft(
        freqs[:, None]**2
        * np.fft.fft(identity, axis=0),
        axis=0
    ).real

    L3 = (
        kron(model.L, eye(angles))
        + kron(
            diags(1/model.rho**2),
            csr_matrix(Lphi)
        )
    ).tocsr()

    sflat = s3.reshape(2, -1)

    D = (
        L3
        + diags(
            2*np.sum(
                model.q[:, None]**2*sflat,
                axis=0
            )
        )
    ).tocsc()

    LU = splu(D)

    I = np.asarray([
        np.dot(w3, sflat[i])
        for i in (0, 1)
    ])

    omega = model.s.N/(2*I)

    for _ in range(100):
        A = LU.solve(
            2*np.sum(
                model.q[:, None]
                * omega[:, None]
                * sflat,
                axis=0
            )
        )

        nxt = (
            model.s.N/2
            + model.q*np.asarray([
                np.dot(w3, sflat[i]*A)
                for i in (0, 1)
            ])
        )/I

        if np.max(abs(nxt-omega)) < 2e-12:
            omega = nxt
            break

        omega = nxt
    else:
        raise ArithmeticError("3D Gauss/Noether iteration failed")

    A = LU.solve(
        2*np.sum(
            model.q[:, None]
            * omega[:, None]
            * sflat,
            axis=0
        )
    )

    W = (
        omega[:, None]
        - model.q[:, None]*A
    )

    rho = 2*np.sum(
        model.q[:, None]*W*sflat,
        axis=0
    )

    gauss = float(np.linalg.norm(
        L3 @ A-rho
    ))

    Noether = [
        float(2*np.dot(w3, W[i]*sflat[i]))
        for i in (0, 1)
    ]

    E = .5*np.dot(
        w3*A,
        L3 @ A
    )

    for i in (0, 1):
        f = f3[i].ravel()
        s = sflat[i]

        E += np.dot(
            w3,
            W[i]**2*s
            + f*(L3 @ f)
            + s-2*s*s+2*s**3
        )

    E += model.s.g*np.dot(
        w3,
        sflat[0]*sflat[1]
    )

    return {
        "energy": float(E),
        "Noether": Noether,
        "gauss_L2": gauss,
        "quadrature_angles": angles,
        "scope": "NONLINEAR_3D_FINITE_BOX_GAUSS_AND_NOETHER",
    }


def independent_3d_hessian_check(
    model, fields, k, a, t=.035, angles=16
):
    """Compare the analytic quadratic to a nonlinear three-dimensional solve."""
    q, info = density_quadratic(
        model, fields, k, a
    )

    zero = independent_3d_energy(
        model, fields, k, a, 0., angles
    )
    up = independent_3d_energy(
        model, fields, k, a, t, angles
    )
    dn = independent_3d_energy(
        model, fields, k, a, -t, angles
    )

    estimate = (
        up["energy"]+dn["energy"]
        - 2*zero["energy"]
    )/(2*t*t)

    for case in (zero, up, dn):
        if (
            case["gauss_L2"] > 1e-7
            or max(abs(
                np.array(case["Noether"])-model.s.N
            )) > 1e-7
        ):
            raise ArithmeticError(
                "Independent 3D Gauss/Noether failure"
            )

    return {
        "analytic_Q": q,
        "independent_3D_Q": float(estimate),
        "rel_error": float(
            abs(q-estimate)/max(abs(q), 1e-12)
        ),
        "direct_energy_delta_plus": float(
            up["energy"]-zero["energy"]
        ),
        "direct_energy_delta_minus": float(
            dn["energy"]-zero["energy"]
        ),
        "Noether_up": up["Noether"],
        "Gauss_up_L2": up["gauss_L2"],
        "Q_electric_from_linearized_Gauss": (
            info["Q_electric_positive"]
        ),
        "scope": (
            "INDEPENDENT_3D_NONLINEAR_GAUSS_"
            "FIXED_N_FINITE_BOX"
        ),
    }


def check_background(model, info):
    """Fail closed on an unconverged or nonneutral source."""
    if (
        abs(info["net_X_charge"]) > 1e-8
        or info["gauss_L2"] > 1e-8
        or max(info["scalar_EOM_weighted_L2"]) > 2e-4
        or info["optimizer"]["gradient_inf"] > 1e-4
    ):
        raise ArithmeticError(
            "P8 background failed its stationary X gates"
        )


def examine(spec, full=True):
    """Run the complete scoped diagnostics for one stationary P8 source."""
    model = Dipole(spec)
    info, fields = model.solve(400)

    check_background(model, info)

    exterior = boundary_audit(model, fields)

    modes = []

    if full:
        for k in (1, 2, 3):
            result, _ = density_modes(
                model, fields, k
            )
            modes.append(result)

    h = (
        (model.rho/3)
        * np.exp(-(
            (model.rho-2.5)**2+model.z**2
        )/(2*3.**2))
    )

    cross = matched_fd_check(
        model, fields, 1, h
    )

    if (
        cross["relative_error"] > .02
        or cross["Gauss_source_L2"] > 1e-10
    ):
        raise ArithmeticError(
            "Independent angular energy verification failed"
        )

    three_d = "NOT_RUN_THIS_CONFIGURATION"

    if spec.nr == 18 and spec.L == 12.:
        amp = np.zeros((2, model.cells))
        amp[0] = (
            .35*(model.rho/3)
            * np.exp(-(
                (model.rho-2.5)**2
                + (model.z-2.)**2
            )/(2*3.**2))
        )

        three_d = independent_3d_hessian_check(
            model, fields, 1, amp
        )

        if three_d["rel_error"] > .03:
            raise ArithmeticError(
                "Independent nonlinear 3D energy mismatch"
            )

    return {
        "spec": asdict(spec),
        "X_source_energy_CANONICAL_NOT_J": (
            info["energy_CANONICAL_NOT_J"]
        ),
        "source_separation": info["source_separation"],
        "X_dipole": info["electric_dipole_X"],
        "net_charge": info["net_X_charge"],
        "X_Gauss_L2": info["gauss_L2"],
        "X_scalar_residuals": info["scalar_EOM_weighted_L2"],
        "electrostatic_exterior": exterior,
        "angular_gauss_response_modes": modes,
        "matched_independent_fd": cross,
        "independent_3D_Gauss_variation": three_d,
        "full_reciprocal_X_Y_matter": "NOT_SOLVED",
        "free_space_source_onshell": "NOT_SOLVED",
        "full_mode_stability": "NOT_CERTIFIED",
    }


def run(root: Path, quick=False):
    """Execute fresh finite-box sources and immutable JSON provenance."""
    cases = [
        ("base18_L12", Spec(nr=18, L=12)),
        ("refine27_L12", Spec(nr=27, L=12)),
        ("larger24_L16", Spec(nr=24, L=16)),
        ("larger30_L20", Spec(nr=30, L=20)),
    ]

    if quick:
        cases = cases[:1]

    out = {}

    for name, spec in cases:
        result = examine(
            spec,
            full=(name != "refine27_L12")
        )

        out[name] = result

        eig = [
            round(x["lowest_density_mode"], 8)
            for x in result["angular_gauss_response_modes"]
        ]

        print(
            "CASE", name,
            "separation", round(
                result["source_separation"], 8
            ),
            "exterior_E_correction", round(
                result["electrostatic_exterior"][
                    "E_one_shot_free_space_ring_boundary_correction_CANONICAL"
                ], 7
            ),
            "angular_eigenvalues", eig,
            "matched_FD_rel", round(
                result["matched_independent_fd"]["relative_error"], 8
            ),
            flush=True
        )

    artifact = {
        "branch": "PH15-P9-EXTERIOR_GAUSS_RESPONSE_DENSITY_HESSIAN",
        "utc": datetime.now(timezone.utc).isoformat(),
        "source_sha256": sha256(__file__),
        "parent_source_sha256": sha256(
            Path(__file__).with_name(
                "hook17_ph15_p8_electric_dipole.py"
            )
        ),
        "cases": out,
        "physics_scope": (
            "X_ONLY_STATIONARY_FINITE_BOX_P8; "
            "ONE_SHOT_FREE_SPACE_FIELD; "
            "GAUSS_RELAXED_STATIC_DENSITY_MODES"
        ),
        "phase_amplitude_cross_theorem": (
            "ZERO_STATIC_QUADRATIC_UNDER_"
            "ZERO_BACKGROUND_SPATIAL_CURRENT"
        ),
        "kinetic_and_dynamic_mode_health": "NOT_CERTIFIED",
        "on_shell_free_space_X": "NOT_SOLVED",
        "fully_reciprocal_X_Y_matter": "NOT_SOLVED",
        "full_physical_metric": "NOT_SOLVED",
        "Earth_down_craft_up": "NOT_DERIVED",
        "SI_operating_energy": "NOT_AVAILABLE",
        "50_percent_theory_gate": "NOT_MET",
        "006D_replaced": False,
        "M5V_status": "FROZEN",
    }

    stamp = datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%S%fZ"
    )

    target = (
        root / "results" / "data"
        / f"032h17_ph15_p9_{stamp}.json"
    )

    target.parent.mkdir(parents=True, exist_ok=True)

    with target.open("x") as stream:
        json.dump(
            artifact, stream,
            indent=2,
            sort_keys=True,
            allow_nan=False
        )

    print("RESULT_PATH=" + str(target))
    print("RESULT_SHA256=" + sha256(target))
    print("PH15_P9_EXECUTION=PASS_SCOPED")

    return artifact


if __name__ == "__main__":
    if (
        len(sys.argv) > 1
        and sys.argv[1] not in ("quick", "full")
    ):
        raise SystemExit("Usage: python source.py [quick|full]")

    run(
        Path.cwd(),
        quick=(
            len(sys.argv) > 1
            and sys.argv[1] == "quick"
        )
    )
