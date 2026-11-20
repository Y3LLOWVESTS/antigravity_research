"""DELTA1-01: exact nonlinear charged shell + canonical scalar energy test.

SCIENTIFIC QUESTION
-------------------
Can positive exponential gauge kinetic Z(phi)=exp(eta phi), without the
DELTA1-00 small-eta-phi expansion, produce >=1g outward neutral scalar
acceleration at >=1m real source-matter standoff below 10 MJ?

PHYSICAL SUBCLASS
-----------------
Massless canonical scalar; flat static Einstein-frame space; universal
physical matter metric exp(2 alpha phi)*g. Idealized conducting charged
sphere of radius 0.5m. Its hypothetical charged skin has ZERO scalar
matter charge and no support cost (deliberately optimistic, not real).
The electrostatic X field extends outside the shell. Charge Q is fixed,
Maxwell permittivity is EPS0 as a conventional SI normalization.

No bare shell matter, Earth, stresses, photon loops or metric backreaction
are included. Real charged matter universally coupled to phi would add
an extra source. The source radius is 0.5m; point radii 1.5..1.7m thus
have 1.0..1.2m matter standoff. This is NOT a 1kg torus geometry.

EXACT REDUCTION
---------------
Let s=R/r and y=eta*phi. At fixed electric Q,

    E_X(r)=Q/[4*pi*eps0*r^2*exp(y)]

    y_ss= -(G*Q^2*eta^2/(8*pi*eps0*c^4*R^2))*exp(-y)

with y(0)=0 (infinity) and y_s(1)=0 (no bare shell scalar charge).

For 0<t<pi/2 the exact solution is

    y(s)=2 log(cos[t*(1-s)]/cos[t]).

The equation relates Q,eta and t; both scalar and Maxwell profiles
are sourced from that same fixed-charge static energy functional.

Energy includes the complete *exterior* scalar gradient and X-electric
field energy in this idealized radial sector, not supports, shell rest
energy, switching/off-state, UV, Earth or gravitational backreaction.

Optimization is over exact radial solutions, not field prescriptions.
Claim: SCOPED_RADIAL_SUBCLASS_ONLY; never whole-craft lift.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
import sympy as sp

G = 6.67430e-11
C = 299792458.0
EPS0 = 8.8541878128e-12
GRAVITY = 9.80665
CEILING = 10_000_000.0
R = 0.5
TARGET_NEAR = 1.5
TARGET_FAR = 1.7

PARENTS = {
    "DELTA00_science": (
        "results/data/delta1_00_20261120T002934122046Z.json",
        "5e4202f310b303fda04156905625c97e31bcdf15b4a29bfbdc4c3e18cfef1aed",
    ),
    "DELTA00_verify": (
        "results/data/delta1_00_verification_20261120T004255846689Z.json",
        "594a2aefdb0bfbb247db0b8173acf64462d57fe21e8600efefc30ef29f6bfb0f",
    ),
    "N1_science": (
        "results/data/gamma1_n1_20261119T220556272564Z.json",
        "fb246ecf729d4c55382e9bb6589f469400849af1aab81b3612067799d1e066fc",
    ),
    "PH16_source": (
        "src/antigravity_research/ph16/ph16_04_joint_stationary.py",
        "b5468671f6418fad7b6ed01d916ea65a95a1d59252b84d4411beed9709f86df0",
    ),
}


def sha(path):
    p = Path(path)
    return (
        hashlib.sha256(p.read_bytes()).hexdigest()
        if p.is_file() else "MISSING"
    )


def parents(root):
    out = {}
    for key, (rel, expected) in PARENTS.items():
        path = Path(root) / rel
        if sha(path) != expected:
            raise RuntimeError(
                f"PARENT_SHA_DRIFT:{key}:{sha(path)}"
            )
        if path.suffix == ".json":
            side = path.with_name(path.name + ".sha256")
            if not side.is_file() or (
                side.read_text().strip()
                != expected + "  " + path.name
            ):
                raise RuntimeError(
                    f"PARENT_SIDECAR_DRIFT:{key}"
                )
        out[key] = {"path": rel, "sha256": expected}

    prev = json.loads(
        (Path(root) / PARENTS["DELTA00_science"][0]).read_text()
    )
    if prev["classification"] != (
        "SCOPED_RED_LONG_RANGE_UNSCREENED_SCALAR_F2"
    ):
        raise RuntimeError(
            "DELTA00_CLASSIFICATION_DRIFT"
        )
    return out


def exact_ensemble():
    """Check fixed-charge and battery-inclusive fixed-voltage variations.

    Treating fixed electric-field energy alone as a thermodynamic
    potential can produce a spurious source-sign inference.
    """
    z, e, cc, q, v = sp.symbols(
        "z e C Q V", positive=True, real=True
    )
    cap = cc * sp.exp(e*z)

    Uq = q*q / (2*cap)
    Gv = -cap*v*v / 2

    if sp.simplify(sp.diff(Uq,z)+e*Uq) != 0:
        raise AssertionError("FIXED_CHARGE_SIGN_FAIL")

    if sp.simplify(
        sp.diff(Gv,z)+e*cap*v*v/2
    ) != 0:
        raise AssertionError(
            "FIXED_VOLTAGE_BATTERY_SIGN_FAIL"
        )

    a = sp.diff(Uq,z).subs({q:cc*v,z:0})
    b = sp.diff(Gv,z).subs(z,0)

    if sp.simplify(a-b) != 0:
        raise AssertionError(
            "ENSEMBLE_SOURCE_SIGN_DRIFT"
        )

    return {
        "fixed_Q_energy":
            "Q^2/(2 C0 exp(eta phi))",
        "fixed_V_with_battery_potential":
            "-C0 exp(eta phi) V^2/2",
        "matched_background_force_sign":
            "IDENTICAL_NEGATIVE",
        "positive_gauge_kinetic":
            "Z=exp(eta phi)>0",
    }


def profile(t, s):
    """Return y, dy/ds, d2y/ds2 where s=R/r, y=eta*phi."""
    if not (0 < t < math.pi/2 and 0 <= s <= 1):
        raise ValueError("invalid t or s")

    theta = t*(1-s)
    y = 2*math.log(
        math.cos(theta)/math.cos(t)
    )
    yp = 2*t*math.tan(theta)
    ypp = -2*t*t/(math.cos(theta)**2)
    return y, yp, ypp


def shape(t, r):
    """Radial factor in m^-1: a=alpha*c^2*shape/eta."""
    if r <= R:
        raise ValueError("exterior only")

    return (
        2*t*R*math.tan(t*(1-R/r))/r**2
    )


def state(t, alpha=1.0):
    """An exact, sourced radial solution normalized to 1g.

    The radial acceleration has one maximum, hence the minimum
    over the specified closed interval is at an endpoint.
    """
    if not (0 < t < math.pi/2 and alpha > 0):
        raise ValueError(
            "positive alpha and valid exact branch required"
        )

    kn = shape(t, TARGET_NEAR)
    kf = shape(t, TARGET_FAR)
    kmin = min(kn, kf)

    eta = alpha*C*C*kmin/GRAVITY
    pref = 2*C**4*R/(G*eta*eta)

    e_em = pref*t*math.tan(t)
    e_scalar = pref*(t*math.tan(t)-t*t)
    e0 = pref*t*t/(math.cos(t)**2)

    q = math.sqrt(
        8*math.pi*EPS0*R*e0
    )
    yR = profile(t,1.0)[0]

    return {
        "t": float(t),
        "alpha": float(alpha),
        "eta": float(eta),
        "min_acceleration_m_s2":
            float(alpha*C*C*kmin/eta),
        "near_acceleration_m_s2":
            float(alpha*C*C*kn/eta),
        "far_acceleration_m_s2":
            float(alpha*C*C*kf/eta),
        "E_X_exterior_J": float(e_em),
        "E_scalar_exterior_J": float(e_scalar),
        "E_total_exterior_J":
            float(e_em+e_scalar),
        "E_unloaded_Coulomb_J":
            float(e0),
        "Q_C_conventional_X_normalization":
            float(q),
        "eta_phi_shell": float(yR),
        "Z_shell": float(math.exp(yR)),
        "electric_surface_field_V_m_if_EM_normalized":
            float(
                q/(4*math.pi*EPS0*R*R*math.exp(yR))
            ),
        "conservative_complete_energy":
            "NOT_CALCULATED",
    }


def quadrature_check(t, alpha=1.0):
    """Numerically reintegrate both positive exterior energies."""
    z = state(t,alpha)
    eta = z["eta"]
    q = z["Q_C_conventional_X_normalization"]
    U = 1/R

    e_em = q*q/(8*math.pi*EPS0)*quad(
        lambda u: math.exp(-profile(t,R*u)[0]),
        0,U,epsrel=1e-11
    )[0]

    e_phi = C**4/(2*G*eta*eta)*quad(
        lambda u: (
            R*profile(t,R*u)[1]
        )**2,
        0,U,epsrel=1e-11
    )[0]

    error = max(
        abs(e_em-z["E_X_exterior_J"])/e_em,
        abs(e_phi-z["E_scalar_exterior_J"])/e_phi,
    )
    if error > 1e-9:
        raise AssertionError(
            "EXTERIOR_ENERGY_QUADRATURE_MISMATCH"
        )

    return {
        "EM_numeric_J": float(e_em),
        "scalar_numeric_J": float(e_phi),
        "max_relative_error": float(error),
    }


def exact_ode_and_boundary(t):
    """Verify nonlinear coupled equation and both scalar boundaries."""
    AA = 2*t*t/(math.cos(t)**2)
    errs = []

    for s in np.linspace(0,1,31):
        y,yp,ypp = profile(t,float(s))
        errs.append(
            abs(ypp+AA*math.exp(-y))
        )

    if (
        max(errs) > 1e-11
        or abs(profile(t,0)[0]) > 1e-14
        or abs(profile(t,1)[1]) > 1e-14
    ):
        raise AssertionError(
            "NONLINEAR_SCALAR_MAXWELL_BVP_FAIL"
        )

    return float(max(errs))


def optimize():
    """Optimize over the exact nonlinear radial family.

    A dense independent sampling of the one-dimensional parameter
    prevents acceptance of an obviously inferior optimizer basin.
    This is a numerical minimum within the declared branch.
    """
    objective = lambda t: state(
        t,1.0
    )["E_total_exterior_J"]

    out = minimize_scalar(
        objective,
        bounds=(.015,math.pi/2-1e-5),
        method="bounded",
        options={"xatol":1e-12,"maxiter":500},
    )

    if not out.success:
        raise RuntimeError(
            "EXACT_RADIAL_OPTIMIZER_FAIL"
        )

    sample = np.linspace(
        .015,math.pi/2-1e-5,2001
    )
    grid_best = min(
        objective(float(t)) for t in sample
    )

    if out.fun > grid_best*(1+1e-9):
        raise RuntimeError(
            "RADIAL_GLOBAL_SCAN_DISAGREES"
        )

    return float(out.x),float(out.fun)


def science(root):
    locked = parents(root)
    ens = exact_ensemble()

    t,e = optimize()
    z = state(t,1.0)
    ode = exact_ode_and_boundary(t)
    q = quadrature_check(t)

    alpha_crit = math.sqrt(e/CEILING)
    a_long = math.sqrt(1e-4/(2-1e-4))

    samples = {
        str(a):float(e/a**2)
        for a in (a_long,1,10,100,1000,2000)
    }

    if not (
        1700 < alpha_crit < 1800
        and z["E_total_exterior_J"] > CEILING
        and samples["1000"] > CEILING
        and samples["2000"] < CEILING
    ):
        raise RuntimeError(
            "SCOPED_FIELD_ENERGY_DECISION_FAIL"
        )

    if z["far_acceleration_m_s2"] < GRAVITY*(1-1e-12):
        raise RuntimeError(
            "TARGET_FAR_ACCELERATION_FAIL"
        )

    return {
        "classification":
            "SCOPED_EXACT_NONLINEAR_SHELL_FAMILY_ENERGY_GATE",
        "parents": locked,
        "ensemble": ens,
        "exact_radial_nonperturbative_solution": z,
        "nonlinear_ODE_residual_max": ode,
        "independent_quadrature": q,
        "optimal_dimensionless_t": t,
        "optimistic_exterior_energy_times_alpha_squared_J": e,
        "strict_10MJ_exterior_only_alpha_threshold":
            alpha_crit,
        "representative_exterior_energy_J_by_alpha":
            samples,
        "illustrative_massless_PPN_alpha": a_long,
        "fixed_radius_m": R,
        "target_radial_distance_m":
            [TARGET_NEAR,TARGET_FAR],
        "minimum_matter_standoff_m":
            TARGET_NEAR-R,
        "source_charge_support":
            "IDEALIZED_ZERO_SCALAR_CHARGE_MASSLESS_SHELL_NOT_REAL_MATERIAL",
        "gates": {
            "SAME_STATIC_GAUSS_SCALAR_VARIATIONAL_ENERGY":
                "PASS_EXACT_RADIAL",
            "POSITIVE_GAUGE_KINETIC_Z":
                "PASS_EXACT",
            "POSITIVE_SCALAR_GRADIENT_ENERGY":
                "PASS_EXACT",
            "CONSTRAINED_RADIAL_STATIC_SCALAR_CURVATURE":
                "POSITIVE_FIXED_Q_RESTRICTED",
            "REQUIRED_SCALAR_ACCELERATION_RADIAL_INTERVAL":
                "PASS_MODEL_ONLY",
            "OPTIMIZED_EXTERIOR_EM_PLUS_SCALAR_ENERGY":
                "RED_IF_ALPHA_LE_1000_FOR_THIS_SUBCLASS",
            "METER_RANGE_MASSIVE_SCALAR":
                "NOT_SOLVED",
            "FULL_REAL_CHARGE_SHELL_AND_SUPPORTS":
                "NOT_DERIVED",
            "FULL_EINSTEIN_EARTH_CRAFT_ACTION":
                "NOT_DERIVED",
            "FULL_LORENTZIAN_CONSTRAINED_MODES":
                "NOT_CERTIFIED",
            "REAL_1KG_NEUTRAL_TORUS_ALL_VOXELS":
                "NOT_TESTED",
            "EMPIRICAL_UV_AND_COMPLETE_OPERATING_ENERGY":
                "NOT_CERTIFIED",
        },
        "qualified_gravity_bridge_survivors": [],
        "006D_replaced": False,
        "GAMMA1_01_authorized": False,
        "PH16_05_authorized": False,
        "PH17_authorized": False,
        "whole_craft_up": "NOT_DERIVED",
        "complete_operating_energy_lt_10MJ":
            "NOT_CERTIFIED",
        "DELTA1_02_authorized": False,
        "next_decision":
            "MASSIVE_OR_SCREENED_HEALTHY_ACTION_REQUIRES_NEW_DERIVATION_NOT_AUTOMATIC_PDE",
    }
