"""HOOK17-PH6: action-derived carrier, source, and neutral-matter dynamics.

SCIENTIFIC PURPOSE
------------------
Bridge PH5's local prescribed-background compatibility result toward
actual source-driven matter response. All dynamical quantities below
follow from one explicitly declared reduced semidiscrete action.

MODEL
-----
Two transverse U(1) carrier potentials a=A_X,z and b=A_Y,y
depend on x,t in a 1+1D reduction, with c=1:

    E_X,z=-a_t, B_X,y=-a_x
    E_Y,y=-b_t, B_Y,z=+b_x
    P=b_t*a_x-a_t*b_x

The centered periodic difference D satisfies D.T=-D.

The action is the integral over time of

    L = dx sum [
        (a_t²+b_t²-(Da)²-(Db)²)/2
        -rho(x-Z)*exp(alpha*P-beta*P²)*sqrt(1-Z_t²)
    ]
    +sum_s [
        m*(qdot_s²-omega_s²*q_s²)/2
        +M*Xdot_s²/2
        +g*qdot_s*dx*sum f(x-X_s)*A_s
    ]

Here rho is normalized neutral rest-mass density and f is a
normalized compact source-current profile.

The neutral body's inertial momentum comes from the SAME portal
action as its rest energy. It is not an independently assigned mass.

The carrier canonical momenta are

    pi_a=a_t+rho*h*F'(P)*Db
    pi_b=b_t-rho*h*F'(P)*Da

where h=sqrt(1-Z_t²), F=exp(alpha*P-beta*P²).

Their inversion is nonlinear and includes the restricted kinetic
condition K=1-rho*h*F''(P)*[(Da)²+(Db)²]>0.

LIMITATIONS
-----------
The source oscillators are finite-width phenomenological transverse
current controls, NOT genuine finite 3D microscopic charged matter.
The smeared neutral worldline is not fully Lorentz-covariant at finite
velocity. The domain is 1D and periodic. Source supports, hull,
gravity, Earth, full gauge constraints, UV physics and SI-scale
energies are absent.

No complete B11-M6 pulse, Earth-down/craft-up force, spacecraft lift,
true 1m stand-off or sub-10-MJ device is claimed.
006D remains unreplaced. ALPHA-1 M5V remains frozen.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, replace
from hashlib import sha256
from pathlib import Path
import math

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp


BRANCH = "032H17A12D1R3X3B17-PH6"


@dataclass(frozen=True)
class Spec:
    n: int = 96
    length: float = 12.0
    tmax: float = 3.4
    width: float = .38
    density_width: float = .46
    density_mass: float = .35
    source_mass: float = 5.0
    oscillator_mass: float = 1.0
    coupling: float = .7
    omega_x: float = 3.6
    omega_y: float = 4.4
    alpha: float = .3
    beta: float = .4
    neutral_center: float = .9
    source_center_x: float = -1.8
    source_center_y: float = -1.2
    q0_x: float = .4
    q0_y: float = -.3


def validate(spec):
    nums = asdict(spec)

    if spec.n < 48 or spec.n % 2:
        raise ValueError("Even n>=48 required")

    if any(not math.isfinite(v) for v in nums.values()):
        raise ValueError("Nonfinite setup")

    positive = (
        spec.length, spec.tmax, spec.width, spec.density_width,
        spec.source_mass, spec.oscillator_mass,
        spec.omega_x, spec.omega_y,
    )

    if min(positive) <= 0:
        raise ValueError("Positive geometry, masses and frequencies required")

    if min(
        spec.density_mass, spec.alpha, spec.beta, spec.coupling
    ) < 0:
        raise ValueError("Nonnegative density and couplings required")

    if 2 * max(spec.width, spec.density_width) >= spec.length / 2:
        raise ValueError("Periodic profile support too broad")


def shape(x, center, width, dx):
    """Normalized compact C4 source with exact center derivative."""
    delta = x - center
    w = (
        (delta + len(x) * dx / 2) % (len(x) * dx)
        - len(x) * dx / 2
    )
    z = w / width
    t = np.maximum(1 - z*z, 0.)
    raw = t**5
    raw_x = np.where(
        np.abs(z) < 1, -10*z*t**4 / width, 0.
    )

    norm = dx * np.sum(raw)

    if norm <= 0:
        raise ValueError("Underresolved finite-support source")

    norm_x = dx * np.sum(raw_x)
    f = raw / norm
    fx = raw_x / norm - raw * norm_x / norm**2

    return f, fx


def D(a, dx):
    """Antisymmetric centered periodic derivative."""
    return (
        np.roll(a, -1) - np.roll(a, 1)
    ) / (2 * dx)


def split(y, n):
    """Carrier fields/momenta and ten source/matter coordinates."""
    a, b, pa, pb = (
        y[i*n:(i+1)*n] for i in range(4)
    )
    return a, b, pa, pb, y[4*n:]


def initial(spec):
    validate(spec)

    tail = np.array([
        spec.neutral_center, 0.,
        spec.q0_x, 0.,
        spec.source_center_x, 0.,
        spec.q0_y, 0.,
        spec.source_center_y, 0.,
    ])

    return np.r_[np.zeros(4*spec.n), tail]


def constitutive(spec, pa, pb, ga, gb, rho, h):
    """Invert carrier canonical momenta; reject unhealthy branches."""
    p0 = pb*ga - pa*gb
    b2 = ga*ga + gb*gb
    P = p0.copy()

    for _ in range(22):
        sigma = spec.alpha*P - spec.beta*P*P

        if np.max(np.abs(sigma)) > 50:
            raise ValueError("Portal outside controlled range")

        F = np.exp(sigma)
        first = spec.alpha - 2*spec.beta*P
        theta = rho*h*F*first
        chi = rho*h*F*(first*first - 2*spec.beta)
        K = 1 - chi*b2

        if not np.all(np.isfinite(K)) or np.min(K) <= 1e-6:
            raise ValueError("Unhealthy local temporal kinetic coefficient")

        correction = (P - p0 - theta*b2) / K
        P = P - correction

        if np.max(np.abs(correction)) < 3e-13:
            break
    else:
        raise ValueError("Constitutive inversion did not converge")

    sigma = spec.alpha*P - spec.beta*P*P
    F = np.exp(sigma)
    first = spec.alpha - 2*spec.beta*P
    theta = rho*h*F*first
    chi = rho*h*F*(first*first - 2*spec.beta)
    K = 1 - chi*b2

    if np.min(K) <= 1e-6:
        raise ValueError("Unhealthy kinetic coefficient")

    ua = pa - theta*gb
    ub = pb + theta*ga

    if np.max(np.abs(ub*ga - ua*gb - P)) > 2e-10:
        raise AssertionError("Canonical momentum inversion residual")

    return ua, ub, P, F, first, theta, chi, K


def state_data(y, spec):
    """Jointly invert carrier and neutral-body canonical momenta."""
    n = spec.n
    dx = spec.length / n
    x = np.arange(n)*dx - spec.length/2

    a, b, pa, pb, tail = split(y, n)
    Z, pZ, qx, vx, X, Ux, qy, vy, Y, Uy = tail

    ga, gb = D(a, dx), D(b, dx)

    neutral, neutral_x = shape(
        x, Z, spec.density_width, dx
    )

    rho = spec.density_mass * neutral
    rho_x = spec.density_mass * neutral_x

    if spec.density_mass == 0:
        V = 0.
        ua, ub, P, F, spr, theta, chi, K = constitutive(
            spec, pa, pb, ga, gb, rho, 1.
        )
    else:
        V = float(
            pZ / math.sqrt(spec.density_mass**2 + pZ**2)
        )

        for _ in range(15):
            h = math.sqrt(max(1 - V*V, 1e-12))

            ua, ub, P, F, spr, theta, chi, K = constitutive(
                spec, pa, pb, ga, gb, rho, h
            )

            rest = dx * np.sum(rho*F)
            newV = float(
                pZ / math.sqrt(rest**2 + pZ**2)
            )

            if abs(V-newV) < 2e-13:
                V = newV
                break

            V = newV
        else:
            raise ValueError("Coupled matter Legendre inversion failed")

        h = math.sqrt(max(1 - V*V, 1e-12))

        ua, ub, P, F, spr, theta, chi, K = constitutive(
            spec, pa, pb, ga, gb, rho, h
        )

    h = math.sqrt(max(1 - V*V, 1e-12))

    fa, fax = shape(x, X, spec.width, dx)
    fb, fbx = shape(x, Y, spec.width, dx)

    return {
        "n": n, "dx": dx,
        "a": a, "b": b,
        "pa": pa, "pb": pb,
        "ga": ga, "gb": gb,
        "tail": tail, "V": V, "h": h,
        "rho": rho, "rho_x": rho_x,
        "ua": ua, "ub": ub, "P": P,
        "F": F, "spr": spr,
        "theta": theta, "chi": chi, "K": K,
        "fa": fa, "fax": fax,
        "fb": fb, "fbx": fbx,
    }


def action_lagrangian(
    a, b, ua, ub, Z, V, qx, vx, X, Ux,
    qy, vy, Y, Uy, spec
):
    """Evaluate the semidiscrete action independently of EOM."""
    if abs(V) >= 1:
        raise ValueError("Neutral packet must be timelike")

    n = spec.n
    dx = spec.length/n
    x = np.arange(n)*dx - spec.length/2

    ga, gb = D(a, dx), D(b, dx)
    P = ub*ga - ua*gb

    rho = spec.density_mass * shape(
        x, Z, spec.density_width, dx
    )[0]

    sigma = spec.alpha*P - spec.beta*P*P
    fa = shape(x, X, spec.width, dx)[0]
    fb = shape(x, Y, spec.width, dx)[0]

    field_matter = dx*np.sum(
        .5*(ua*ua+ub*ub-ga*ga-gb*gb)
        - rho*np.exp(sigma)*math.sqrt(1-V*V)
    )

    oscillator = .5*spec.oscillator_mass*(
        vx*vx + vy*vy
        - spec.omega_x**2*qx*qx
        - spec.omega_y**2*qy*qy
    )

    translation = .5*spec.source_mass*(
        Ux*Ux + Uy*Uy
    )

    source_coupling = spec.coupling*dx*(
        vx*np.sum(fa*a) + vy*np.sum(fb*b)
    )

    return float(
        field_matter + oscillator + translation + source_coupling
    )


def rhs(t, y, spec):
    """Euler-Lagrange equations of the same semidiscrete action."""
    d = state_data(y, spec)

    dx = d["dx"]
    a, b = d["a"], d["b"]
    ga, gb = d["ga"], d["gb"]
    ua, ub = d["ua"], d["ub"]
    theta = d["theta"]

    Z, pZ, qx, vx, X, Ux, qy, vy, Y, Uy = d["tail"]
    V = d["V"]

    fa, fax = d["fa"], d["fax"]
    fb, fbx = d["fb"], d["fbx"]

    pa_t = (
        D(ga+theta*ub, dx)
        + spec.coupling*vx*fa
    )
    pb_t = (
        D(gb-theta*ua, dx)
        + spec.coupling*vy*fb
    )

    dvx = (
        -spec.omega_x**2*qx
        - spec.coupling/spec.oscillator_mass
        * (
            dx*np.sum(fa*ua)
            - Ux*dx*np.sum(fax*a)
        )
    )

    dvy = (
        -spec.omega_y**2*qy
        - spec.coupling/spec.oscillator_mass
        * (
            dx*np.sum(fb*ub)
            - Uy*dx*np.sum(fbx*b)
        )
    )

    dUx = (
        -spec.coupling*vx*dx*np.sum(fax*a)
        / spec.source_mass
    )
    dUy = (
        -spec.coupling*vy*dx*np.sum(fbx*b)
        / spec.source_mass
    )

    dpZ = d["h"]*dx*np.sum(d["rho_x"]*d["F"])

    return np.r_[
        ua, ub, pa_t, pb_t,
        [V, dpZ, vx, dvx, Ux, dUx, vy, dvy, Uy, dUy]
    ]


def diagnostics(y, spec):
    """Independent canonical energy and total momentum ledger."""
    d = state_data(y, spec)

    dx = d["dx"]
    ua, ub = d["ua"], d["ub"]
    ga, gb = d["ga"], d["gb"]
    F, P, spr, rho = (
        d["F"], d["P"], d["spr"], d["rho"]
    )
    h = d["h"]

    Z, pZ, qx, vx, X, Ux, qy, vy, Y, Uy = d["tail"]

    field_energy = .5*dx*np.sum(
        ua*ua+ub*ub+ga*ga+gb*gb
    )

    # Matter energy includes kinetic and portal rest energy.
    matter_energy = dx*np.sum(
        rho*F*(1/h-h*spr*P)
    )

    oscillator_energy = .5*spec.oscillator_mass*(
        vx*vx + vy*vy
        + spec.omega_x**2*qx*qx
        + spec.omega_y**2*qy*qy
    )

    source_translation_energy = .5*spec.source_mass*(
        Ux*Ux + Uy*Uy
    )

    field_momentum = -dx*np.sum(
        ua*ga+ub*gb
    )
    neutral_momentum = pZ
    source_momentum = spec.source_mass*(Ux+Uy)

    chi = d["chi"]
    e2 = ua*ua+ub*ub
    largest_R = np.maximum(
        ua*ua+gb*gb,
        ub*ub+ga*ga
    )

    frozen_D = np.where(
        chi <= 0,
        1+chi*e2,
        1+chi*(e2-largest_R)
    )

    mask = (
        rho > rho.max()*.1
        if rho.max() > 0
        else np.zeros_like(rho, dtype=bool)
    )

    total_energy = (
        field_energy + matter_energy
        + oscillator_energy + source_translation_energy
    )

    total_momentum = (
        field_momentum
        + neutral_momentum
        + source_momentum
    )

    return {
        "field_energy": float(field_energy),
        "matter_energy_including_kinetic": float(matter_energy),
        "oscillator_energy": float(oscillator_energy),
        "source_translation_energy": float(source_translation_energy),
        "total_energy": float(total_energy),

        "field_momentum": float(field_momentum),
        "neutral_momentum": float(neutral_momentum),
        "source_momentum": float(source_momentum),
        "total_momentum": float(total_momentum),

        "neutral_position": float(Z),
        "neutral_velocity": float(d["V"]),
        "source_centers": [float(X), float(Y)],

        "P_min": float(np.min(P)),
        "P_max": float(np.max(P)),
        "K_min": float(np.min(d["K"])),

        "chi_min_neutral": (
            float(np.min(chi[mask])) if rho.max() > 0 else 0.
        ),
        "chi_max_neutral": (
            float(np.max(chi[mask])) if rho.max() > 0 else 0.
        ),
        "frozen_D_min_neutral": (
            float(np.min(frozen_D[mask])) if rho.max() > 0 else 1.
        ),
        "sigma_prime_min_neutral": (
            float(np.min(spr[mask])) if rho.max() > 0 else 0.
        ),
        "support_gap": float(
            min(abs(Z-X), abs(Z-Y))
            - spec.width - spec.density_width
        ),
    }


def action_legendre_residual(y, spec):
    """Independent action Legendre energy compared with diagnostics."""
    d = state_data(y, spec)

    Z, pZ, qx, vx, X, Ux, qy, vy, Y, Uy = d["tail"]

    ia = d["dx"]*np.sum(d["fa"]*d["a"])
    ib = d["dx"]*np.sum(d["fb"]*d["b"])

    L = action_lagrangian(
        d["a"], d["b"], d["ua"], d["ub"],
        Z, d["V"], qx, vx, X, Ux, qy, vy, Y, Uy, spec
    )

    canonical = d["dx"]*np.sum(
        d["pa"]*d["ua"] + d["pb"]*d["ub"]
    )

    canonical += pZ*d["V"]

    canonical += spec.source_mass*(
        Ux*Ux + Uy*Uy
    )

    canonical += (
        spec.oscillator_mass*vx + spec.coupling*ia
    )*vx

    canonical += (
        spec.oscillator_mass*vy + spec.coupling*ib
    )*vy

    return float(
        canonical - L - diagnostics(y, spec)["total_energy"]
    )


def run_case(spec=Spec(), samples=121):
    """Evolve one action-derived source configuration without resets."""
    validate(spec)

    y0 = initial(spec)
    times = np.linspace(0, spec.tmax, samples)

    sol = solve_ivp(
        rhs,
        (0., spec.tmax),
        y0,
        args=(spec,),
        t_eval=times,
        method="DOP853",
        rtol=3e-9,
        atol=3e-11,
        max_step=.016,
    )

    if not sol.success:
        raise RuntimeError("PH6 reduced source evolution failed")

    records = [
        diagnostics(sol.y[:, i], spec)
        for i in range(len(times))
    ]

    E0 = records[0]["total_energy"]
    P0 = records[0]["total_momentum"]

    e_drift = max(
        abs(r["total_energy"]-E0)
        for r in records
    )

    p_drift = max(
        abs(r["total_momentum"]-P0)
        for r in records
    )

    force = np.array([
        rhs(times[i], sol.y[:, i], spec)[4*spec.n+1]
        for i in range(len(times))
    ])

    positive = float(
        np.trapezoid(np.maximum(force, 0), times)
    )
    negative = float(
        np.trapezoid(np.minimum(force, 0), times)
    )

    delta_neutral = (
        records[-1]["neutral_momentum"]
        - records[0]["neutral_momentum"]
    )

    return {
        "spec": asdict(spec),
        "initial": records[0],
        "final": records[-1],

        "max_energy_drift": e_drift,
        "max_total_momentum_drift": p_drift,

        "neutral_positive_impulse": positive,
        "neutral_negative_impulse": negative,
        "neutral_signed_impulse": positive+negative,
        "neutral_exact_momentum_change": delta_neutral,
        "impulse_quadrature_error": abs(
            positive+negative-delta_neutral
        ),

        "minimum_field_P": min(r["P_min"] for r in records),
        "maximum_field_P": max(r["P_max"] for r in records),

        "minimum_K": min(r["K_min"] for r in records),
        "minimum_frozen_D": min(
            r["frozen_D_min_neutral"] for r in records
        ),
        "maximum_chi_neutral": max(
            r["chi_max_neutral"] for r in records
        ),
        "minimum_sigma_prime_neutral": min(
            r["sigma_prime_min_neutral"] for r in records
        ),

        "maximum_neutral_speed": max(
            abs(r["neutral_velocity"]) for r in records
        ),
        "minimum_support_gap": min(
            r["support_gap"] for r in records
        ),

        "no_artificial_state_resets": True,
        "dimensionless_source_and_matter": True,
        "full_3d_gauge_and_gravity": "NOT_DERIVED",
        "B11_M6_complete_pulse": "NOT_RUN",
        "whole_craft_lift": "NOT_DERIVED",
    }


def symbolic_checks():
    """Exact first variations of the reduced matter/carrier action."""
    ea, eb, ga, gb, a, b, rho, h = sp.symbols(
        "ea eb ga gb alpha beta rho h",
        real=True
    )

    P = eb*ga-ea*gb
    sigma = a*P-b*P*P
    F = sp.exp(sigma)

    L = (
        (ea**2+eb**2-ga**2-gb**2)/2
        -rho*h*F
    )

    theta = rho*h*F*(a-2*b*P)

    assert sp.simplify(
        sp.diff(L, ea)-(ea+theta*gb)
    ) == 0

    assert sp.simplify(
        sp.diff(L, eb)-(eb-theta*ga)
    ) == 0

    assert sp.simplify(
        sp.diff(L, ga)-(-ga-theta*eb)
    ) == 0

    assert sp.simplify(
        sp.diff(L, gb)-(-gb+theta*ea)
    ) == 0

    p = sp.symbols("p", real=True)
    fp = sp.exp(a*p-b*p*p)

    assert sp.simplify(
        sp.diff(fp, p, 2)
        - fp*((a-2*b*p)**2-2*b)
    ) == 0

    assert sp.simplify(
        sp.diff(L, ea)*ga
        + sp.diff(L, eb)*gb
        - (ea*ga+eb*gb)
    ) == 0

    return {
        "first_variations": 4,
        "matter_curvature": "PASS_EXACT",
        "canonical_translation_cross_cancellation": "PASS_EXACT",
        "full_3d_gauge_Ward": "NOT_DERIVED",
        "full_metric_Einstein_equations": "NOT_DERIVED",
    }


def provenance(root):
    """Read-only evidence verification; never alter frozen results."""
    expected = {
        "m5v_source": (
            "src/antigravity_research/agminer/"
            "hook17_r3b_m5v_unified_exterior_action.py",
            "ea193cd163b2fc87e6973878c77e27c761f0625f6c5de3f38594587ef6cdb80f",
        ),
        "m5v_result": (
            "results/data/"
            "b17_m5v_unified_20261114T203555409373Z_full_bundle.json",
            "53f63f93fe9f525302f516b6376fa227d4b46027e6a0f75ae4dd35404da8c52b",
        ),
        "ph5_source": (
            "src/antigravity_research/agminer/"
            "hook17_ph5_concavity_escape_audit.py",
            "05e234290e894b7a0c444c26b09fc169546bc5fbb49852f8d610b0fc94197876",
        ),
        "ph5_result": (
            "results/data/"
            "032h17_ph5_concavity_escape_20261115T005215182946Z.json",
            "49c9934b317221537f1163bc7538e18b3d5a5d2329945fa82ed9db5b0359a293",
        ),
    }

    result = {}

    for name, (relative, expected_sha) in expected.items():
        path = Path(root)/relative

        if not path.is_file():
            result[name] = {"status": "MISSING"}
            continue

        actual = sha256(path.read_bytes()).hexdigest()

        result[name] = {
            "status": (
                "MATCH" if actual == expected_sha
                else "HASH_MISMATCH"
            ),
            "actual_sha256": actual,
            "expected_sha256": expected_sha,
        }

    return result


def run(root):
    """Pre-registered PH6 matrix; no artificial parameter optimization."""
    base = Spec()

    cases = {
        "mixed_odd": run_case(base),
        "no_portal": run_case(
            replace(base, alpha=0, beta=0)
        ),
        "one_source_off": run_case(
            replace(base, q0_y=0)
        ),
        "no_neutral_matter": run_case(
            replace(base, density_mass=0)
        ),
        "even_only": run_case(
            replace(base, alpha=0)
        ),
        "linear_only": run_case(
            replace(base, beta=0)
        ),
        "finer_n256": run_case(
            replace(base, n=256)
        ),
        "finest_n384": run_case(
            replace(base, n=384)
        ),
    }

    assert all(
        c["max_energy_drift"] < 1e-9
        for c in cases.values()
    )

    assert abs(
        cases["no_portal"]["neutral_exact_momentum_change"]
    ) < 1e-10

    assert (
        cases["no_neutral_matter"]["neutral_exact_momentum_change"]
        == 0
    )

    assert cases["mixed_odd"]["neutral_exact_momentum_change"] > 0
    assert cases["even_only"]["neutral_exact_momentum_change"] < 0

    assert cases["mixed_odd"]["maximum_chi_neutral"] < 0
    assert cases["mixed_odd"]["minimum_K"] > 0
    assert cases["mixed_odd"]["minimum_frozen_D"] > 0
    assert cases["mixed_odd"]["minimum_sigma_prime_neutral"] > 0
    assert cases["mixed_odd"]["minimum_support_gap"] > 0
    assert cases["mixed_odd"]["maximum_neutral_speed"] < .1

    assert (
        cases["finest_n384"]["max_total_momentum_drift"]
        < .55*cases["finer_n256"]["max_total_momentum_drift"]
    )

    assert abs(
        cases["finest_n384"]["neutral_exact_momentum_change"]
        - cases["finer_n256"]["neutral_exact_momentum_change"]
    ) < .02*abs(
        cases["finest_n384"]["neutral_exact_momentum_change"]
    )

    assert max(
        c["impulse_quadrature_error"] for c in cases.values()
    ) < 1e-5

    # Pre-return light-travel margin in declared c=1 model.
    boundary_margin = (
        min(base.source_center_x, base.source_center_y)
        - base.width
        + base.length/2
        - base.tmax
    )

    assert boundary_margin > 0

    history = provenance(root)
    history_ok = all(
        item["status"] == "MATCH"
        for item in history.values()
    )

    return {
        "branch": BRANCH,
        "frozen_reference": "ALPHA1_M5V_UNMODIFIED",
        "action_checks": symbolic_checks(),
        "historical_provenance": history,
        "cases": cases,
        "pre_return_boundary_margin": boundary_margin,

        "gates": {
            "P0_PROVENANCE": (
                "PASS" if history_ok else "UNRESOLVED"
            ),
            "P1_ONE_ACTION_VARIATIONS":
                "PASS_REDUCED_1D",
            "P1_NEUTRAL_INERTIA_FROM_SAME_PORTAL":
                "PASS_SMEARED_WORLDLINE_ONLY",
            "P1_MIXED_PORTAL_RESTRICTED_CONE":
                "PASS_SAMPLED_FROZEN_MATTER_SCREEN",
            "P2_SOURCE_DRIVEN_NEUTRAL_RESPONSE":
                "PASS_REDUCED_1D",
            "P2_TOTAL_MOMENTUM":
                "GRID_DEFECT_DECREASES_UNDER_REFINEMENT",
            "P2_SIGNED_IMPULSE":
                "BOTH_SIGNS_IN_DISTINCT_CONTROLS_NOT_COMPLETE_CYCLE",
            "P2_REAL_MICROSCOPIC_3D_SOURCE":
                "NOT_DERIVED",
            "P3_COMPLETE_MATERIAL_GRAVITY_MODES":
                "NOT_DERIVED",
            "P3_PARITY_CP_UV_EMPIRICAL":
                "NOT_CERTIFIED",
            "P3_EARTH_DOWN_WHOLE_CRAFT_UP":
                "NOT_DERIVED",
            "B11_M6_LOADED_COMPLETE_CAUSAL_IMPULSE":
                "NOT_RUN",
            "FINITE_NEUTRAL_1G_AT_1M":
                "NOT_CERTIFIED",
            "STRICT_COMPLETE_LT10MJ":
                "NOT_CERTIFIED",
            "006D_REPLACED": "NO",
        },

        "verdict":
            "YELLOW_REDUCED_SAME_ACTION_NEUTRAL_RESPONSE_NO_ENGINE",
    }
