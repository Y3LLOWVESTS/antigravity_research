"""BETA1-1B0: PH15-P10 local reciprocal magnetic-health obstruction.

Scope:
    Flat space, FY=0, BX=0, actual discrete PH15-P10 X source.
    Scalar amplitudes and X background are frozen.
    Local scalar phase momenta are Legendre-eliminated.

Hamiltonian:
    H(B) = B²/2 + T exp(-2 sigma)
           + G exp(2 sigma) + U exp(4 sigma)

    sigma = alpha E B - beta (E B)²

    T = sum(f_i² W_i²)
    G = sum(|grad f_i|²)
    U = complete PH15 source potential

No full PH16 mode-health, metric, gravity, SI or craft-force claim.
"""

from __future__ import annotations

import math
import numpy as np
import sympy as sp

from scipy.linalg import eigh

from antigravity_research.agminer.hook17_ph15_p10_free_space import (
    CoulombSource,
    Spec,
)


def exact_variation():
    e, b, al, be, t, g, u = sp.symbols(
        "e b alpha beta T G U",
        real=True,
    )

    sigma = al * e * b - be * (e * b)**2

    H = (
        b*b/2
        + t*sp.exp(-2*sigma)
        + g*sp.exp(2*sigma)
        + u*sp.exp(4*sigma)
    )

    curvature = sp.simplify(
        sp.diff(H, b, 2).subs(b, 0)
    )

    expected = (
        1
        - 4*be*e**2*(g-t+2*u)
        + 4*al**2*e**2*(g+t+4*u)
    )

    assert sp.simplify(curvature-expected) == 0

    # Independent two-phase Lagrangian/Legendre derivation.

    v1, v2, s1, s2 = sp.symbols(
        "v1 v2 s1 s2",
        positive=True,
    )

    L = (
        -b*b/2
        + sp.exp(2*sigma)
        *(s1*v1*v1+s2*v2*v2-g)
        - sp.exp(4*sigma)*u
    )

    Lbb = sp.diff(L, b, 2).subs(b, 0)

    Lvb = sp.Matrix([
        sp.diff(L, b, v).subs(b, 0)
        for v in (v1, v2)
    ])

    Lvv = sp.diag(
        *[
            sp.diff(L, v, 2).subs(b, 0)
            for v in (v1, v2)
        ]
    )

    schur = sp.simplify(
        -Lbb + (Lvb.T*Lvv.inv()*Lvb)[0]
    )

    expected_phase = expected.subs(
        t,
        s1*v1**2+s2*v2**2,
    )

    assert sp.simplify(
        schur-expected_phase
    ) == 0

    # Positivity of PH15's polynomial self-potential.

    s = sp.symbols(
        "s",
        nonnegative=True,
    )

    assert sp.expand(
        s*((1-s)**2+s**2)
        -(s-2*s**2+2*s**3)
    ) == 0

    return {
        "phase_fixed_local_H_BB": str(
            sp.factor(curvature)
        ),
        "canonical_2phase_Schur_equals_H_BB": True,
        "U_polynomial_nonnegative_for_s>=0_gcontact>=0": True,
        "beta0_alpha_any_nonnegative_source_curvature": True,
        "electric_velocity_block":
            "Maxwell unit coefficients at BX=BY=0; "
            "not the complete principal symbol",
    }


def source_arrays(nr=18, L=12.0):
    model = CoulombSource(
        Spec(nr=nr, L=L),
        self_order=8,
    )

    info, fields = model.solve(350)

    if (
        max(info["scalar_equation_weighted_L2"]) >= 1e-4
        or abs(info["net_X_charge"]) >= 1e-7
    ):
        raise RuntimeError(
            "PH15-P10 source EOM/neutrality failed"
        )

    shape = (model.nr, model.nz)

    F = fields["F"].reshape(2, *shape)
    W = fields["W"].reshape(2, *shape)
    A = fields["A"].reshape(shape)

    h = model.h

    dr = lambda x: np.gradient(
        x, h, axis=-2, edge_order=2
    )
    dz = lambda x: np.gradient(
        x, h, axis=-1, edge_order=2
    )

    G = np.sum(
        dr(F)**2 + dz(F)**2,
        axis=0,
    )

    T = np.sum(
        W**2 * F**2,
        axis=0,
    )

    ss = F*F

    U = (
        np.sum(
            ss-2*ss**2+2*ss**3,
            axis=0,
        )
        + model.s.g*ss[0]*ss[1]
    )

    Er = -dr(A)
    Ez = -dz(A)

    E2 = Er*Er + Ez*Ez

    # Reproduce the actual PH15 first-order Y source,
    # preserving its no-backreaction limitation.

    y1 = model.induced_Y_free_space(
        fields, alpha=1.0
    )
    yh = model.induced_Y_free_space(
        fields, alpha=0.5
    )
    y0 = model.induced_Y_free_space(
        fields, alpha=0.0
    )

    info["Y_first_order_alpha1_current_L2"] = (
        y1["Y_current_L2"]
    )
    info["Y_first_order_alpha_half_current_L2"] = (
        yh["Y_current_L2"]
    )
    info["Y_first_order_alpha0_current_L2"] = (
        y0["Y_current_L2"]
    )

    if min(np.min(G), np.min(T), np.min(U)) < -1e-12:
        raise RuntimeError(
            "Source energy decomposition inconsistent"
        )

    return model, info, {
        "G": G,
        "T": T,
        "U": U,
        "Er": Er,
        "Ez": Ez,
        "E2": E2,
    }


def coefficients(data, alpha=1.0, beta=0.0):
    E2 = data["E2"]
    G = data["G"]
    T = data["T"]
    U = data["U"]

    return (
        1
        - 4*beta*E2*(G-T+2*U)
        + 4*alpha**2*E2*(G+T+4*U)
    )


def threshold(data, alpha=1.0):
    slope = 4*data["E2"]*(
        data["G"]-data["T"]+2*data["U"]
    )

    intercept = coefficients(
        data, alpha=alpha, beta=0.0
    )

    mask = slope > 1e-14

    if not np.any(mask):
        return None

    ratio = np.full(
        slope.shape, np.inf
    )

    ratio[mask] = (
        intercept[mask]/slope[mask]
    )

    index = tuple(
        int(i)
        for i in np.unravel_index(
            np.argmin(ratio),
            ratio.shape,
        )
    )

    return {
        "value": float(ratio[index]),
        "cell_indices": index,
        "positive_slope_cell_fraction":
            float(np.mean(mask)),
        "slope_at_cell": float(slope[index]),
        "intercept_at_cell":
            float(intercept[index]),
    }


def vector_potential_basis(model):
    r = model.rho.reshape(
        model.nr, model.nz
    )
    z = model.z.reshape(
        model.nr, model.nz
    )

    # Smooth, axis-regular A_Y_phi ~ rho.
    # Deliberately finite set of localized modes.

    specs = [
        (0.9, 1.1, -2.0),
        (0.9, 1.1,  0.0),
        (0.9, 1.1,  2.0),
        (1.5, 1.5, -1.5),
        (1.5, 1.5,  0.0),
        (1.5, 1.5,  1.5),
        (2.5, 2.0,  0.0),
        (3.5, 2.5,  0.0),
    ]

    dr = lambda x: np.gradient(
        x, model.h, axis=0, edge_order=2
    )
    dz = lambda x: np.gradient(
        x, model.h, axis=1, edge_order=2
    )

    output = []

    for rw, zw, zc in specs:
        v = r*np.exp(
            -0.5*(
                (r/rw)**2
                + ((z-zc)/zw)**2
            )
        )

        Br = -dz(v)
        Bz = dr(v)+v/r

        output.append(
            np.stack((Br, Bz), axis=0)
        )

    return np.asarray(output), specs


def rayleigh_modes(
    model,
    data,
    alpha=1.0,
    beta=0.0,
    with_vector=False,
):
    fields, specs = vector_potential_basis(model)

    Er = data["Er"]
    Ez = data["Ez"]

    w = model.w.reshape(
        model.nr, model.nz
    )

    coupling = (
        -4*beta*(
            data["G"]-data["T"]+2*data["U"]
        )
        +4*alpha**2*(
            data["G"]+data["T"]+4*data["U"]
        )
    )

    flat = fields.reshape(
        len(fields), 2, -1
    )

    E_dot_B = (
        fields[:, 0]*Er
        + fields[:, 1]*Ez
    )

    gram = np.einsum(
        "icn,jcn,n->ij",
        flat,
        flat,
        model.w,
        optimize=True,
    )

    correction = np.einsum(
        "in,jn,n->ij",
        E_dot_B.reshape(len(fields), -1),
        E_dot_B.reshape(len(fields), -1),
        (w*coupling).ravel(),
        optimize=True,
    )

    stiffness = gram+correction

    gram = (gram+gram.T)/2
    stiffness = (stiffness+stiffness.T)/2

    eigenvalues, eigenvectors = eigh(gram)

    keep = (
        eigenvalues
        > 1e-9*max(eigenvalues)
    )

    if np.count_nonzero(keep) < 4:
        raise RuntimeError(
            "Rayleigh basis rank deficient"
        )

    whiten = (
        eigenvectors[:, keep]
        / np.sqrt(eigenvalues[keep])[None, :]
    )

    H = whiten.T@stiffness@whiten

    ev, vectors = np.linalg.eigh(
        (H+H.T)/2
    )

    result = {
        "minimum": float(ev[0]),
        "maximum": float(ev[-1]),
        "retained_basis": int(sum(keep)),
        "gram_condition_kept": float(
            max(eigenvalues)
            / min(eigenvalues[keep])
        ),
        "basis_size": len(specs),
        "scope":
            "AXISYMMETRIC_GAUSSIAN_Y_MAGNETIC_RITZ_"
            "FIXED_X_AND_LOCAL_PHASE_MOMENTA",
    }

    if with_vector:
        mode = np.tensordot(
            whiten@vectors[:, 0],
            fields,
            axes=(0, 0),
        )

        result["normalized_B_mode"] = mode

    return result


def ritz_critical_beta(
    model,
    data,
    alpha=0.0,
    upper=100.0,
):
    """Bracket the first Ritz sign change; no force optimization."""

    lo = 0.0
    hi = upper

    flo = rayleigh_modes(
        model, data, alpha, lo
    )["minimum"]

    fhi = rayleigh_modes(
        model, data, alpha, hi
    )["minimum"]

    if not (flo > 0 and fhi < 0):
        raise RuntimeError(
            "Ritz zero not bracketed"
        )

    for _ in range(25):
        mid = (lo+hi)/2

        fmid = rayleigh_modes(
            model, data, alpha, mid
        )["minimum"]

        if fmid > 0:
            lo = mid
        else:
            hi = mid

    return float((lo+hi)/2)


def magnetic_energy_fd(
    model,
    data,
    mode,
    alpha=0.0,
    beta=100.0,
    eps=0.01,
):
    """Independent full-exponential Hamiltonian finite difference."""

    w = model.w.reshape(
        model.nr, model.nz
    )

    T = data["T"]
    G = data["G"]
    U = data["U"]

    dot = (
        data["Er"]*mode[0]
        + data["Ez"]*mode[1]
    )

    B2 = mode[0]**2+mode[1]**2

    def energy(amplitude):
        P = amplitude*dot

        sigma = (
            alpha*P-beta*P*P
        )

        density = (
            0.5*amplitude**2*B2
            + T*np.exp(-2*sigma)
            + G*np.exp(2*sigma)
            + U*np.exp(4*sigma)
        )

        return float(
            np.sum(w*density)
        )

    base = energy(0.0)

    fd = (
        energy(eps)
        + energy(-eps)
        - 2*base
    )/(eps**2)

    derived = float(
        np.sum(
            w*(
                B2
                + (
                    -4*beta*(G-T+2*U)
                    +4*alpha**2*(G+T+4*U)
                )*dot**2
            )
        )
    )

    return {
        "epsilon": eps,
        "derived_quadratic": derived,
        "central_fd": fd,
        "absolute_error": abs(derived-fd),
        "odd_energy_error":
            abs(energy(eps)-energy(-eps)),
    }


def bianchi_divergence(model, mode):
    r = model.rho.reshape(
        model.nr, model.nz
    )

    h = model.h

    return float(
        np.max(
            abs(
                np.gradient(
                    mode[0], h,
                    axis=0,
                    edge_order=2,
                )
                + mode[0]/r
                + np.gradient(
                    mode[1], h,
                    axis=1,
                    edge_order=2,
                )
            )
        )
    )


def fd_phase_energy(
    unused,
    e,
    t,
    g,
    u,
    alpha,
    beta,
    step,
):
    def energy(B):
        sigma = (
            alpha*e*B
            - beta*(e*B)**2
        )

        return (
            B*B/2
            + t*math.exp(-2*sigma)
            + g*math.exp(2*sigma)
            + u*math.exp(4*sigma)
        )

    return (
        energy(step)
        +energy(-step)
        -2*energy(0)
    )/step**2


def run_cases():
    symbolic = exact_variation()

    cases = {}

    fixed_cases = [
        ("coarse12_L12", 12, 12.0),
        ("base18_L12", 18, 12.0),
        ("fixed_h24_L16", 24, 16.0),
        ("fixed_h30_L20", 30, 20.0),
        ("refine36_L16", 36, 16.0),
    ]

    for name, nr, L in fixed_cases:
        model, info, data = source_arrays(nr, L)

        thresholds = {
            str(alpha): threshold(
                data, alpha=alpha
            )
            for alpha in (0.0, 1.0)
        }

        c0 = coefficients(
            data, alpha=1.0, beta=0.0
        )

        c100 = coefficients(
            data, alpha=1.0, beta=100.0
        )

        a1_b0 = rayleigh_modes(
            model, data, 1.0, 0.0
        )
        a1_b100 = rayleigh_modes(
            model, data, 1.0, 100.0
        )
        a1_b300 = rayleigh_modes(
            model, data, 1.0, 300.0
        )

        a0_b0 = rayleigh_modes(
            model, data, 0.0, 0.0
        )
        a0_b75 = rayleigh_modes(
            model, data, 0.0, 75.0
        )

        a0_b100 = rayleigh_modes(
            model, data,
            0.0, 100.0,
            with_vector=True,
        )

        mode = a0_b100.pop(
            "normalized_B_mode"
        )

        root = ritz_critical_beta(
            model, data,
            alpha=0.0,
            upper=100.0,
        )

        fd_magnetic = magnetic_energy_fd(
            model, data, mode,
            alpha=0.0,
            beta=100.0,
            eps=0.01,
        )

        bianchi = bianchi_divergence(
            model, mode
        )

        if (
            fd_magnetic["absolute_error"] > 2e-4
            or bianchi > 2e-11
        ):
            raise RuntimeError(
                "Independent Hamiltonian/Bianchi check failed"
            )

        if np.min(c0) <= 0:
            raise RuntimeError(
                "Beta-zero positive control failed"
            )

        site = tuple(
            thresholds["1.0"]["cell_indices"]
        )

        electric = float(
            np.sqrt(data["E2"][site])
        )

        T = float(data["T"][site])
        G = float(data["G"][site])
        U = float(data["U"][site])

        analytic = float(c0[site])

        steps = (1e-2, 3e-3, 1e-3)

        phase_fd = [
            fd_phase_energy(
                0.0, electric,
                T, G, U, 1.0, 0.0, step
            )
            for step in steps
        ]

        phase_error = abs(
            phase_fd[-1]-analytic
        )

        if phase_error > 3e-6:
            raise RuntimeError(
                "Phase Hamiltonian FD failed"
            )

        if a1_b0["minimum"] < 0.99:
            raise RuntimeError(
                "Beta-zero Ritz control failed"
            )

        cases[name] = {
            "nr": nr,
            "L_canonical": L,
            "h_canonical": model.h,

            "source_energy_CANONICAL_NOT_J":
                info["canonical_energy_NOT_J"],

            "source_sep":
                info["source_separation"],

            "source_eom_L2":
                info["scalar_equation_weighted_L2"],

            "source_net_X_charge":
                info["net_X_charge"],

            "Y_current_first_order_alpha1":
                info["Y_first_order_alpha1_current_L2"],

            "Y_current_first_order_alpha_half":
                info["Y_first_order_alpha_half_current_L2"],

            "Y_current_first_order_alpha0":
                info["Y_first_order_alpha0_current_L2"],

            "max_E2":
                float(np.max(data["E2"])),

            "min_G":
                float(np.min(data["G"])),

            "min_T":
                float(np.min(data["T"])),

            "min_U":
                float(np.min(data["U"])),

            "K_plus_2U_min":
                float(np.min(
                    data["G"]-data["T"]+2*data["U"]
                )),

            "beta_thresholds_local":
                thresholds,

            "alpha1_beta0_local_min":
                float(np.min(c0)),

            "alpha1_beta100_local_min":
                float(np.min(c100)),

            "rayleigh_alpha1_beta0": a1_b0,
            "rayleigh_alpha1_beta100": a1_b100,
            "rayleigh_alpha1_beta300": a1_b300,

            "rayleigh_alpha0_beta0": a0_b0,
            "rayleigh_alpha0_beta75": a0_b75,
            "rayleigh_alpha0_beta100": a0_b100,

            "alpha0_Ritz_beta_critical_fixed_basis":
                root,

            "alpha0_beta100_full_exponential_H_fd":
                fd_magnetic,

            "alpha0_beta100_Bianchi_divergence_inf":
                bianchi,

            "phase_hamiltonian_FD": {
                "site": list(site),
                "analytic": analytic,
                "fd_steps": list(steps),
                "values": phase_fd,
                "last_error": phase_error,
            },

            "source_status":
                "RECOMPUTED_P10_DISCRETE_X_SOURCE;"
                "Y_NOT_BACKREACTED",
        }

    c24 = cases["fixed_h24_L16"]
    c30 = cases["fixed_h30_L20"]
    c36 = cases["refine36_L16"]

    b24 = c24["beta_thresholds_local"]["1.0"]["value"]
    b30 = c30["beta_thresholds_local"]["1.0"]["value"]

    gates = {
        "source_eom_neutrality": all(
            max(r["source_eom_L2"]) < 1e-4
            and abs(r["source_net_X_charge"]) < 1e-7
            for r in cases.values()
        ),

        "PH15_first_order_Y_alpha_scaling": all(
            r["Y_current_first_order_alpha1"] > 1e-5
            and abs(
                r["Y_current_first_order_alpha_half"]
                -0.5*r["Y_current_first_order_alpha1"]
            ) < 1e-11
            and r["Y_current_first_order_alpha0"] < 1e-13
            for r in cases.values()
        ),

        "positive_beta0_all_grids": all(
            r["alpha1_beta0_local_min"] > 0
            and r["rayleigh_alpha1_beta0"]["minimum"] > 0.99
            for r in cases.values()
        ),

        "beta100_local_sign_change_all_grids": all(
            r["alpha1_beta100_local_min"] < 0
            for r in cases.values()
        ),

        "fixed_h_domain_beta_threshold_rel_below_2pct":
            abs(b24-b30)/b30 < 0.02,

        "phase_fd_cross_check": all(
            r["phase_hamiltonian_FD"]["last_error"] < 3e-6
            for r in cases.values()
        ),

        "alpha0_beta100_negative_ritz_all_grids": all(
            r["rayleigh_alpha0_beta100"]["minimum"] < -0.05
            for r in cases.values()
        ),

        "alpha0_beta75_negative_ritz_refined": all(
            cases[k]["rayleigh_alpha0_beta75"]["minimum"] < 0
            for k in (
                "fixed_h24_L16",
                "fixed_h30_L20",
                "refine36_L16",
            )
        ),

        "alpha0_beta0_free_maxwell": all(
            abs(
                r["rayleigh_alpha0_beta0"]["minimum"]-1
            ) < 1e-8
            for r in cases.values()
        ),

        "alpha0_beta100_finite_amplitude_H_matches": all(
            r["alpha0_beta100_full_exponential_H_fd"][
                "absolute_error"
            ] < 2e-4
            and r["alpha0_beta100_full_exponential_H_fd"][
                "central_fd"
            ] < 0
            for r in cases.values()
        ),

        "alpha0_beta100_Bianchi": all(
            r["alpha0_beta100_Bianchi_divergence_inf"] < 2e-11
            for r in cases.values()
        ),

        "alpha0_critical_Ritz_beta_fixed_h_domain_agreement":
            abs(
                c24["alpha0_Ritz_beta_critical_fixed_basis"]
                -c30["alpha0_Ritz_beta_critical_fixed_basis"]
            ) < 1.0,

        "alpha0_critical_Ritz_beta_L16_grid_agreement":
            abs(
                c24["alpha0_Ritz_beta_critical_fixed_basis"]
                -c36["alpha0_Ritz_beta_critical_fixed_basis"]
            ) < 3.0,
    }

    return {
        "symbolic": symbolic,
        "cases": cases,
        "gates": gates,

        "classification":
            "NECESSARY_CONDITION_DERIVED",

        "verdict":
            "YELLOW_ALPHA0_BETA100_DISCRETE_NEGATIVE_"
            "MAGNETIC_MODE_FULL_PH16_OPEN",

        "physical_claim":
            "NO_FULL_PH16_STABILITY_OR_EARTH_FORCE",

        "scope":
            "P10_DISCRETE_FREE_X_SOURCE; FY_ZERO; BX_ZERO; "
            "FROZEN_X_AND_SCALAR_AMPLITUDES; "
            "LOCAL_PHASE_MOMENTUM_ELIMINATION; NO_GRAVITY",

        "limitations": [
            "Alpha=0,Y=0 is stationary within the restricted "
            "two-carrier flat action; alpha-nonzero Y=0 is "
            "not generally stationary",

            "Local phase Legendre transformation; "
            "global Noether/longitudinal constraints not fully solved",

            "Ritz Gaussian basis incompletely spans "
            "Maxwell/phase/source modes",

            "B coefficient at finite coupling is not "
            "the full dynamical characteristic",

            "Finite-difference E,G are not continuum certified",

            "No real neutral matter, support, Earth, SI or UV",
        ],
    }
