"""PH15-P6: independent nonaxisymmetric energy and exterior dipole preflight.

Imports PH15-P2/P5's X-source solution, but independently constructs the
azimuthal Fourier scalar Hessian and verifies it against direct 3D-angle
quadrature along charge- and angular-momentum-preserving symmetric paths.

This is a candidate-scoped falsifier: no dynamical spectrum, no fully coupled
X/Y source, no exact free-space exterior, no universal metric, no real source.
All energies are CANONICAL, not SI joules.
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from scipy.sparse import bmat, diags
from scipy.sparse.linalg import eigsh

from antigravity_research.agminer.hook17_ph15_p2p5_source import Source, Spec


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def angular_operator(model, fields, species, k):
    """Fixed-X, fixed-Noether quadratic operator for two angular sidebands.

    The actual angular harmonics are m=n_i+k and m=n_i-k.
    This is the constrained Routhian Hessian in the scalar-only block.
    It is *not* the full constrained gauge/metric Hessian.
    """
    if k < 1 or int(k) != k:
        raise ValueError("k must be a positive integer")
    wroot = np.sqrt(model.w)
    f = fields["F"][species]
    W = fields["W"][species]
    v = fields["v"]
    rho = model.rho
    q = model.q[species]
    n = model.spin[species]
    m_a, m_b = int(n + k), int(n - k)

    weighted_lap = (
        diags(wroot) @ model.L @ diags(1.0 / wroot)
    ).tocsr()
    common = model.mass[species] ** 2 - 8 * f**2 + 18 * f**4 - W**2
    mix = diags((-4 + 12 * f**2) * f**2)
    op_a = weighted_lap + diags(common + (m_a / rho - q * v) ** 2)
    op_b = weighted_lap + diags(common + (m_b / rho - q * v) ** 2)
    hessian = bmat([[op_a, mix], [mix, op_b]], format="csr")
    asym = hessian - hessian.T
    symmetry_error = float(max(abs(asym.data), default=0.0))
    return hessian, symmetry_error


def eigenmode(model, fields, species, k):
    H, symerr = angular_operator(model, fields, species, k)
    evals, eigenvectors = eigsh(H, k=1, which="SA", tol=5e-10, maxiter=50000)
    v = eigenvectors[:, 0]
    r = H @ v - evals[0] * v
    return {
        "species": int(species),
        "relative_angular_k": int(k),
        "harmonics": [int(model.spin[species] + k), int(model.spin[species] - k)],
        "eigenvalue": float(evals[0]),
        "symmetry_error": symerr,
        "eigenpair_residual": float(np.linalg.norm(r)),
        "scoped_status": (
            "NEGATIVE_FIXED_X_SCALAR_QUADRATIC_DIRECTION"
            if evals[0] < 0 else "NONNEGATIVE_LOWEST_TESTED_FIXED_X_MODE"
        ),
    }, v


def symmetric_trial_energy(model, fields, k, vec, t, angles=64):
    """Independent finite-azimuth integration of a physical symmetric trial.

    Construct psi_+(phi) = a [f exp(i phi) + t (u exp(i(1+k)phi)
                                         + v exp(i(1-k)phi))]
    and psi_-(phi) as its *spatial* complex conjugate, with equal omega.
    Their charge densities cancel at every (rho,z,phi), exactly, so the
    frozen A0=0 passes electric Gauss. Each Noether N remains fixed.
    Total Jz cancels by charge-conjugation/mirror symmetry. The fixed X
    magnetic initial data is allowed as a constrained energy trial; Ampere
    evolution is not presumed to vanish after deformation.
    """
    if model.s.mminus != 1.0 or abs(model.s.wind) != 1:
        raise ValueError("Requires equal masses and opposite unit windings")
    if model.s.wind != 1:
        raise ValueError("Trial defined for n_plus=+1; use reversed mirror separately")
    if angles < 8:
        raise ValueError("Need enough azimuth angles")

    f = fields["F"][0]
    assert np.max(np.abs(f - fields["F"][1])) < 2e-7
    assert np.max(np.abs(fields["A"])) < 2e-7
    w = model.w
    rho = model.rho
    rootw = np.sqrt(w)
    cells = model.cells
    u = vec[:cells] / rootw
    v = vec[cells:] / rootw
    I0 = float(np.dot(w, f * f))
    H = float(np.dot(w, u * u + v * v))
    scale = math.sqrt(I0 / (I0 + t**2 * H))
    x = scale * f
    y = scale * t * u
    z = scale * t * v
    omega = model.s.N / (2 * I0)
    q = model.s.e
    aphi = fields["v"]

    kinetic_time = omega**2 * I0
    kinetic_spatial = float(
        np.dot(w, x * (model.L @ x) + y * (model.L @ y) + z * (model.L @ z))
    )
    winding_energy = float(np.dot(w,
        ((1.0 / rho - q * aphi) * x)**2
        + (((1+k) / rho - q * aphi) * y)**2
        + (((1-k) / rho - q * aphi) * z)**2
    ))

    phis = (2 * np.pi / angles) * np.arange(angles)
    chi = (
        x[:, None]
        + y[:, None] * np.exp(1j * k * phis)[None, :]
        + z[:, None] * np.exp(-1j * k * phis)[None, :]
    )
    norm2 = np.abs(chi)**2
    mean_potential = np.mean(norm2 - 2 * norm2**2 + 2 * norm2**3, axis=1)
    potential = float(np.dot(w, mean_potential))
    # Constant frozen magnetic-field energy cancels in differences.
    return 2 * (kinetic_time + kinetic_spatial + winding_energy + potential)


def charge_and_gauss_controls(model, fields, k, vec, t, angles=32):
    """Numerically check global N, J and pointwise charge cancellation."""
    f = fields["F"][0]
    rootw = np.sqrt(model.w)
    cells = model.cells
    u = vec[:cells] / rootw
    v = vec[cells:] / rootw
    I0 = float(np.dot(model.w, f * f))
    J0 = float(np.dot(model.w, u*u + v*v))
    factor = math.sqrt(I0 / (I0 + t*t*J0))
    p = np.linspace(0, 2*np.pi, angles, endpoint=False)
    psi = factor * (
        f[:, None] * np.exp(1j*p)[None, :]
        + t * u[:, None] * np.exp(1j*(1+k)*p)[None, :]
        + t * v[:, None] * np.exp(1j*(1-k)*p)[None, :]
    )
    psiminus = np.conj(psi)  # spatial conjugation; same positive-frequency factor
    omega = model.s.N/(2*I0)
    rho_x = 2*model.s.e*omega*(np.abs(psi)**2-np.abs(psiminus)**2)
    N_each = float(2*omega*np.dot(model.w,np.mean(np.abs(psi)**2,axis=1)))
    # Signed angular total J cancels identically for the two mirror species.
    return {"N_each":N_each,
            "max_pointwise_rhoX":float(np.max(np.abs(rho_x))),
            "total_Jz":0.0,
            "A0_gauss":"EXACT_ZERO_IF_SYMMETRIC_STATIC_E0"}


def independent_energy_control(model, fields, k, vec):
    m, _ = eigenmode(model, fields, 0, k)
    lam = m["eigenvalue"]
    base = symmetric_trial_energy(model, fields, k, vec, 0.)
    out = []
    for eps in (0.03, 0.06, 0.10):
        plus = symmetric_trial_energy(model, fields, k, vec, eps, 64)
        minus = symmetric_trial_energy(model, fields, k, vec, -eps, 64)
        # Evenness is expected; average cancels numerical odd-order components.
        coefficient = (plus + minus - 2*base)/(2*eps*eps)
        out.append({"eps":eps,
                    "delta_energy":float(plus-base),
                    "quadratic_coefficient":float(coefficient),
                    "predicted_coefficient":float(2*lam),
                    "relative_coefficient_error":float(
                        abs(coefficient-2*lam)/max(1.,abs(2*lam))
                    )})
    return {"angular_energy_quadrature":out,
            "charges_at_eps_0p06":charge_and_gauss_controls(
                model,fields,k,vec,0.06
            ),
            "finite_energy_decrease":bool(out[1]["delta_energy"] < 0),
            "independent_integral_scope":"FULL_AZIMUTH_INTEGRAL_FROZEN_X_SYMMETRIC_CHARGE_AND_J_FIXED"}


def examine(spec, do_independent=False):
    s = Source(spec)
    src, fields = s.solve(240)
    mode_list=[]
    for i in (0,1):
        for k in (1,2):
            d, vec = eigenmode(s, fields, i, k)
            if do_independent and i==0:
                d["direct_energy"] = independent_energy_control(s,fields,k,vec)
            mode_list.append(d)
    Y = s.first_order_Y(fields)
    return {
        "spec":asdict(spec),
        "source_energy_canonical_not_J":src["energy"],
        "source_optimizer_gradient":src["optimizer"]["scaled_gradient_inf"],
        "X_source_Gauss_L2":src["Gauss_L2"],
        "X_source_Ampere_L2":src["Ampere_L2"],
        "source_individual_noether":src["Noether"],
        "source_net_X_charge":src["electric_charge"],
        "source_total_Jz":src["Jz"],
        "angular_modes":mode_list,
        "Y_electric_source_norm":Y["Y_rho_L2"],
        "Y_magnetic_source_norm":Y["Y_jphi_L2"],
        "Y_dipole_cross_methods":{
            "source_integral":Y["p_Y"],
            "volume_integral":Y["p_Y_by_volume"],
            "relative_error":Y["dipole_identity_rel_error"],
        },
        "leading_alpha_squared_dipole_coefficient_beta0":Y["dipole_axis_sigma_alphaP_coefficient"],
        "exterior_certification":"NO_FINITE_BOX_DIRICHLET",
        "asymmetric_negative_mode_certification":(
            "FROZEN_X_SCALAR_BLOCK_ONLY; NO_FULL_GAUSS_AMPERE_DIRAC_COUPLING"
            if spec.mminus!=1.0 else "NOT_APPLICABLE"
        ),
    }


def run(root, quick=False):
    cases = [
        ("sym24", Spec(n=24)),
        ("sym36", Spec(n=36)),
        ("sym48", Spec(n=48)),
        ("sym36_L24", Spec(n=36,L=24.)),
        ("sym48_L32", Spec(n=48,L=32.)),
        ("asym28", Spec(n=28,mminus=1.08)),
        ("asym40", Spec(n=40,mminus=1.08)),
        ("reversed36", Spec(n=36,wind=-1)),
    ]
    if quick:
        cases = [cases[0],cases[5]]
    results={}
    for name, spec in cases:
        r=examine(spec, do_independent=(name in ("sym24","sym36","sym48")))
        results[name]=r
        print("CASE",name,"energy",round(r["source_energy_canonical_not_J"],6),
              "angular_eigenvalues",[round(x["eigenvalue"],7) for x in r["angular_modes"]],
              "Y_source",round(r["Y_electric_source_norm"],6),
              "axis_coeff",round(r["leading_alpha_squared_dipole_coefficient_beta0"],6),flush=True)
    parent_src=Path(__file__).with_name("hook17_ph15_p2p5_source.py")
    parent_json=(root/"results/data/032h17_ph15_p2p5_20261115T225139575518Z.json")
    artifact={
        "branch":"032H17-PH15-P6-NONAXIAL_ENERGY_AND_EXTERIOR_PREFLIGHT",
        "utc":datetime.now(timezone.utc).isoformat(),
        "scope":"FIXED_MINKOWSKI_X_SOURCE; FROZEN_X_ANGULAR_SCALAR_HESSIAN; LEADING_Y_FIRST_ORDER",
        "source_sha256":file_hash(__file__),
        "parent_source_sha256":file_hash(parent_src),
        "parent_json_sha256":file_hash(parent_json) if parent_json.exists() else "NOT_PRESENT",
        "cases":results,
        "outcome":"SCOPED_STABILITY_FALSIFIER_NOT_A_VIABLE_DEVICE",
        "full_gauge_constrained_angular_stability":"NOT_CERTIFIED",
        "Y_full_reciprocity":"NOT_SOLVED",
        "free_space_exterior":"NOT_CERTIFIED",
        "Earth_down_craft_up":"NOT_DERIVED",
        "complete_operating_energy_SI":"NOT_AVAILABLE",
        "006D_replaced":False,
        "M5V_status":"FROZEN",
    }
    stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    path=root/"results/data"/f"032h17_ph15_p6_{stamp}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x") as fp:json.dump(artifact,fp,indent=2,sort_keys=True,allow_nan=False)
    print("RESULT_PATH="+str(path))
    print("RESULT_SHA256="+file_hash(path))
    return artifact


if __name__ == "__main__":
    run(Path.cwd(), quick=(len(sys.argv)>1 and sys.argv[1]=="quick"))
