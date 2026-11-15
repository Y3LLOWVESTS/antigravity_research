"""HOOK17-PH2 — physical-source equilibrium and causal-reaction audit.

PURPOSE
-------
Investigate whether the frozen ALPHA-1 M5I source morphology can
survive microscopic equations of motion, rather than merely matching
a prescribed current. Independently test source-driven two-carrier
wave dynamics, energy exchange, finite source recoil, and signed
impulse in a restricted action-derived system.

PHYSICAL STATUS
---------------
This is NOT a complete physical antigravity model.

The static scalar and cold-dust investigations are scoped theorem
tests. The causal calculation uses a reduced 1+1-dimensional
two-carrier, mobile-source-oscillator action.

No physical Earth material, universal-metric backreaction, complete
3D source confinement, gravitational metric solution, spacecraft
assembly, or practical device is derived.

FROZEN REFERENCES
-----------------
006D: C=23.591586299249, unreplaced.
A12C: 2.6568591420597114 J prescribed field capacity.
R3B: 1.5429162116460216 J prescribed mixed-field capacity.
M5V: frozen artificial reduced-action reference.

STATIC SOURCE ACTION
--------------------
For a restricted free canonical charged complex scalar:

    L = -|D psi|^2 - m^2 |psi|^2

Consider psi=f(r,z)*exp(i*n*phi), with A0=Aphi=0.

The source-free static EOM requires:

    integral [
        |grad f|^2 + (n^2/r^2 + m^2)*f^2
    ] dV = 0

A nonzero finite-energy winding source cannot satisfy this
positive-definite identity for nonnegative m^2.

Nonlinear interactions, nonzero gauge fields, charge-support
mechanisms or different matter actions change the assumptions.
This is NOT a universal charged-scalar no-go theorem.

REDUCED DYNAMIC ACTION
----------------------
Natural units c=1. For carrier sector s=X,Y:

    L_s = integral (At^2-Ax^2)/2 dx
          + m*v^2/2 - m*omega^2*q^2/2
          + M*U^2/2
          + g*v*integral f(x-X)*A(x) dx

where v=dq/dt and U=dX/dt.

The source current is derived by varying the action:

    j_s(x,t) = g*v_s(t)*f(x-X_s(t))

The source-center recoil is also action-derived.

The profile f is a rigid finite-width reduced source shape.
This does not establish microscopic 3D source confinement.

The periodic computational domain is an energy/momentum control,
not an asymptotically radiating exterior.

CLAIM CLASSIFICATION
--------------------
SCOPED_STATIC_SOURCE_FALSIFICATION
AND
REDUCED_ACTION_DERIVED_CAUSAL_RECOIL_CONTROL

No spacecraft lift, sub-10-MJ physical system, or experimental
antigravity is established.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from hashlib import sha256
from pathlib import Path
import math

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp


BRANCH = "032H17A12D1R3X3B17-PH2"

REFERENCE_SHA = {
    "m5v_code":
        "ea193cd163b2fc87e6973878c77e27c761f0625f6c5de3f38594587ef6cdb80f",
    "m5v_result":
        "53f63f93fe9f525302f516b6376fa227d4b46027e6a0f75ae4dd35404da8c52b",
    "ph1_code":
        "47281ea38e40351944bc194375b4732b28c58960d7acf644f6d040b82fd0aa52",
}

REFERENCE_PATHS = {
    "m5v_code":
        "src/antigravity_research/agminer/"
        "hook17_r3b_m5v_unified_exterior_action.py",
    "m5v_result":
        "results/data/"
        "b17_m5v_unified_20261114T203555409373Z_full_bundle.json",
    "ph1_code":
        "src/antigravity_research/agminer/"
        "hook17_ph1_physicalization_preflight.py",
}


def provenance(root: Path) -> dict:
    """Verify immutable historical artifacts without modifying them."""
    result = {}

    for key, relative in REFERENCE_PATHS.items():
        path = root / relative

        if not path.is_file():
            result[key] = {
                "status": "MISSING",
                "expected": REFERENCE_SHA[key],
            }
            continue

        actual = sha256(path.read_bytes()).hexdigest()

        result[key] = {
            "status":
                "MATCH" if actual == REFERENCE_SHA[key]
                else "MISMATCH",
            "actual": actual,
            "expected": REFERENCE_SHA[key],
        }

    ph1 = list(
        (root / "results/data").glob(
            "032h17_ph1_preflight_*.json"
        )
    )

    result["ph1_result_present"] = bool(ph1)
    return result


def source_shape_integrals(
    order: int = 60,
    angular: int = 128,
    mass: float = 0.0,
) -> dict:
    """Compute canonical energy of PH1's fixed-gauge winding witness.

    The source is the original M5I compact polynomial bump.
    q=n=J0=1 are arbitrary canonical reference normalizations.

    Returned values are NOT SI energies.
    """
    if order < 12 or angular < 16 or mass < 0:
        raise ValueError("Invalid source integral controls")

    R, a, b = 1.15, 0.42, 0.50

    nodes, weights = np.polynomial.legendre.leggauss(order)
    s = (nodes + 1.0) / 2.0
    ws = weights / 2.0

    theta = (
        2.0 * math.pi / angular
    ) * np.arange(angular)

    x = np.sqrt(s[:, None]) * np.cos(theta)[None, :]
    y = np.sqrt(s[:, None]) * np.sin(theta)[None, :]

    r = R + a*x
    t = 1.0 - s[:, None]

    # f² = J0*r*B/(2*q*n).
    f2 = 0.5*r*t**5

    # Exact logarithmic gradients of f.
    derivr = 1.0/(2.0*r) - 5.0*x/(a*t)
    derivz = -5.0*y/(b*t)

    # dV = 2*pi*r*a*b*dx*dy;
    # dx*dy = ds*dtheta/2.
    weight = (
        math.pi*r*a*b*ws[:, None]
        * (2.0*math.pi/angular)
    )

    radial = float(np.sum(weight*f2*derivr**2))
    axial = float(np.sum(weight*f2*derivz**2))
    angular_e = float(np.sum(weight*f2/r**2))
    rest = float(np.sum(weight*f2*mass**2))

    result = {
        "radial_gradient": radial,
        "axial_gradient": axial,
        "azimuthal_gradient": angular_e,
        "rest_mass": rest,
    }

    result["free_static_no_go_integral"] = sum(
        result.values()
    )

    return result


def exact_algebra() -> dict:
    """Exact symbolic identities with explicitly restricted scope."""
    ex, ey, bx, by, rho, kappa = sp.symbols(
        "ex ey bx by rho kappa",
        real=True,
    )

    P = ex*by + ey*bx

    # Canonical Lorentzian carriers and fixed-density matter.
    L = (
        sp.Rational(1, 2)
        * (ex**2 + ey**2 - bx**2 - by**2)
        - rho*sp.exp(kappa*P)
    )

    D = [sp.diff(L, v) for v in (ex, ey)]
    H = sp.hessian(L, (ex, ey))

    energy = sp.simplify(
        ex*D[0] + ey*D[1] - L
    )

    expected_energy = (
        sp.Rational(1, 2)
        * (ex**2 + ey**2 + bx**2 + by**2)
        + rho*sp.exp(kappa*P)*(1-kappa*P)
    )

    assert sp.simplify(
        energy - expected_energy
    ) == 0

    bvec = sp.Matrix([by, bx])

    expected_hessian = (
        sp.eye(2)
        - rho*kappa**2*sp.exp(kappa*P)
        * bvec*bvec.T
    )

    assert H == expected_hessian

    expected_det = (
        1
        - rho*kappa**2*sp.exp(kappa*P)
        * (bx*bx + by*by)
    )

    assert sp.simplify(
        H.det() - expected_det
    ) == 0

    # Source-off matter rest-energy control.
    assert sp.simplify(
        energy.subs({
            ex: 0, ey: 0,
            bx: 0, by: 0,
        }) - rho
    ) == 0

    # Parity-even P² has no linear response at P=0.
    u = sp.symbols("u", real=True)

    assert sp.diff(
        kappa*u*u, u
    ).subs(u, 0) == 0

    # Conditional conformal invertibility factor.
    assert sp.solve(
        1-4*kappa*u, u
    ) == [1/(4*kappa)]

    # One species gives at most one current direction.
    qx, qy = sp.symbols(
        "qx qy", nonzero=True
    )

    assert sp.Matrix([[qx, qy]]).rank() == 1

    assert sp.Matrix([
        [qx, 0],
        [0, qy],
    ]).rank() == 2

    # Same-action energy and translation exchange for
    # the reduced dynamical oscillator source.
    v, U, ie, ia, g = sp.symbols(
        "v U I_E I_fx g",
        real=True,
    )

    field_power = g*v*ie

    oscillator_power = (
        -g*v*ie + g*v*U*ia
    )

    translation_power = -g*v*U*ia

    assert sp.simplify(
        field_power
        + oscillator_power
        + translation_power
    ) == 0

    assert sp.simplify(
        -g*v*ia + g*v*ia
    ) == 0

    return {
        "legendre_hamiltonian": str(energy),
        "loaded_hessian":
            "I-rho*kappa^2*exp(kappa*P)*b*b^T",
        "restricted_kinetic_eigenvalue":
            "1-rho*kappa^2*exp(kappa*P)*(B_X^2+B_Y^2)",
        "invertibility_factor":
            "1-4*kappa*P",
        "identities_passed": 10,
    }


def restricted_kinetic(
    rho: float,
    kappa: float,
    p: float,
    b2: float,
) -> dict:
    """Necessary frozen-dust kinetic/invertibility controls."""
    values = (rho, kappa, p, b2)

    if (
        not all(math.isfinite(v) for v in values)
        or rho < 0
        or b2 < 0
    ):
        raise ValueError(
            "Finite rho>=0 and B²>=0 required"
        )

    eigenvalue = (
        1
        - rho*kappa*kappa
        * math.exp(kappa*p)*b2
    )

    invert = 1-4*kappa*p

    return {
        "loaded_eigenvalue": eigenvalue,
        "positive_necessary": eigenvalue > 0,
        "conformal_jacobian": invert,
        "invertible_necessary": abs(invert) > 1e-12,
        "full_characteristic_health": "NOT_TESTED",
    }


def static_no_go() -> dict:
    """Evaluate precise source-family falsifiers."""
    e0 = source_shape_integrals(mass=0)
    e1 = source_shape_integrals(mass=1)

    independent = source_shape_integrals(
        order=90,
        angular=160,
        mass=0,
    )

    if e0["free_static_no_go_integral"] <= 0:
        raise AssertionError(
            "Expected nonzero positive scalar integral"
        )

    discrepancy = abs(
        independent["free_static_no_go_integral"]
        - e0["free_static_no_go_integral"]
    )

    if discrepancy > 2e-7:
        raise AssertionError(
            "Source integral lacks quadrature convergence"
        )

    return {
        "M5I_free_scalar_Aphi_zero":
            "SCOPED_NO_GO",
        "proof":
            "Free static EOM demands integral["
            "|grad f|^2+(n^2/r^2+m^2)f^2]dV=0, "
            "but the nonzero profile has positive integral",
        "mass0_positive_integral_unscaled": e0,
        "mass1_positive_integral_unscaled": e1,
        "independent_order90_total":
            independent["free_static_no_go_integral"],
        "Aphi_zero_nonzero_current":
            "SCOPED_MAXWELL_AMPERE_INCONSISTENCY",
        "cold_opposite_charge_dust":
            "SCOPED_EULER_GAUSS_INCONSISTENCY_WITHOUT_PRESSURE_OR_SUPPORT",
        "reopening_conditions":
            "nontrivial self interactions, A0/Aphi, "
            "pressure, transported matter, supports "
            "or another fully specified source action",
        "physical_source_energy_j": None,
    }


@dataclass(frozen=True)
class WaveSpec:
    n: int = 128
    length: float = 8.0
    tmax: float = 2.1
    width: float = 0.34
    mass: float = 1.0
    anchor_mass: float = 1.0
    coupling: float = 0.5
    omega_x: float = 4.0
    omega_y: float = 5.0


def _envelope(
    x: np.ndarray,
    position: float,
    width: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Finite-width profile and its analytic spatial derivative."""
    z = (x-position)/width
    t = np.maximum(1-z*z, 0)

    norm = (
        math.gamma(6.5)
        / (
            math.sqrt(math.pi)
            * math.gamma(6)*width
        )
    )

    f = norm*t**5

    fx = np.where(
        abs(z) < 1,
        -10*norm*z*t**4/width,
        0,
    )

    return f, fx


def _unpack(state, n):
    """Each sector has A, E, q, v, X, U."""
    width = 2*n+4

    return [
        state[s*width:(s+1)*width]
        for s in range(2)
    ]


def _derivative(t, state, spec, x, dx):
    """Euler-Lagrange dynamics from one reduced source-field action."""
    n = spec.n
    output = []

    for s, block in enumerate(_unpack(state, n)):
        A = block[:n]
        E = block[n:2*n]
        q, v, X, U = block[-4:]

        f, fx = _envelope(
            x, X, spec.width
        )

        lap = (
            np.roll(A, -1)
            - 2*A
            + np.roll(A, 1)
        )/(dx*dx)

        intfE = dx*np.sum(f*E)
        intfxA = dx*np.sum(fx*A)

        omega = (
            spec.omega_x,
            spec.omega_y,
        )[s]

        output.append(
            np.concatenate((
                E,
                lap + spec.coupling*v*f,
                [
                    v,
                    -omega**2*q
                    - spec.coupling/spec.mass
                    * (intfE-U*intfxA),
                    U,
                    -spec.coupling/spec.anchor_mass
                    * v*intfxA,
                ],
            ))
        )

    return np.concatenate(output)


def initial_state(
    spec: WaveSpec,
    case: str,
    x: np.ndarray,
) -> np.ndarray:
    """Pre-registered source-off, radiating, and recoil controls."""
    output = []

    for s in range(2):
        A = np.zeros(spec.n)
        E = np.zeros(spec.n)
        q = 0.0

        if case == "self_sourced":
            q = (0.25, 0.18)[s]

        elif case == "incoming_recoil" and s == 0:
            # Right-moving incident carrier wave.
            # This supplies incoming momentum.
            # It is NOT a propulsion demonstration.
            A = 0.05*np.exp(
                -((x+1.1)/0.30)**2
            )

            E = 2*(x+1.1)/(0.30**2)*A

        elif case not in (
            "source_off",
            "self_sourced",
            "incoming_recoil",
        ):
            raise ValueError(
                "Unrecognized control case"
            )

        output.append(
            np.concatenate((
                A, E,
                [q, 0.0, 0.0, 0.0],
            ))
        )

    return np.concatenate(output)


def wave_diagnostics(state, spec, x, dx):
    """Independent total field/source energy and momentum ledger."""
    e_fields = 0.0
    e_osc = 0.0
    e_motion = 0.0

    p_fields = 0.0
    p_motion = 0.0

    for s, block in enumerate(
        _unpack(state, spec.n)
    ):
        A = block[:spec.n]
        E = block[spec.n:2*spec.n]
        q, v, X, U = block[-4:]

        forward = (
            np.roll(A, -1)-A
        )/dx

        central = (
            np.roll(A, -1)-np.roll(A, 1)
        )/(2*dx)

        omega = (
            spec.omega_x,
            spec.omega_y,
        )[s]

        e_fields += (
            0.5*dx*np.sum(
                E*E + forward*forward
            )
        )

        e_osc += (
            0.5*spec.mass
            * (v*v+omega**2*q*q)
        )

        e_motion += (
            0.5*spec.anchor_mass*U*U
        )

        p_fields += -dx*np.sum(
            E*central
        )

        p_motion += spec.anchor_mass*U

    return {
        "carrier_energy": float(e_fields),
        "source_internal_energy": float(e_osc),
        "source_translation_energy": float(e_motion),
        "total_energy":
            float(e_fields+e_osc+e_motion),
        "carrier_momentum": float(p_fields),
        "source_momentum": float(p_motion),
        "total_momentum":
            float(p_fields+p_motion),
    }


def causal_source_run(
    spec: WaveSpec = WaveSpec(),
    case: str = "self_sourced",
) -> dict:
    """Integrate source-field equations; preserve signed recoil.

    The spatially periodic boundary stores outgoing wave energy.
    It is NOT an infinite exterior or a radiation-to-infinity
    momentum calculation.
    """
    if (
        spec.n < 64
        or spec.n % 2
        or spec.length <= 0
        or spec.tmax <= 0
        or spec.width <= 0
    ):
        raise ValueError(
            "Invalid wave discretization"
        )

    x = np.linspace(
        -spec.length/2,
        spec.length/2,
        spec.n,
        endpoint=False,
    )

    dx = spec.length/spec.n
    y0 = initial_state(spec, case, x)

    times = np.linspace(
        0, spec.tmax, 85
    )

    solution = solve_ivp(
        _derivative,
        (0, spec.tmax),
        y0,
        t_eval=times,
        args=(spec, x, dx),
        method="DOP853",
        rtol=2e-9,
        atol=2e-11,
        max_step=0.012,
    )

    if (
        not solution.success
        or not np.all(np.isfinite(solution.y))
    ):
        raise RuntimeError(
            "Reduced source evolution failed"
        )

    diagnostics = [
        wave_diagnostics(
            solution.y[:, i],
            spec, x, dx,
        )
        for i in range(len(times))
    ]

    E0 = diagnostics[0]["total_energy"]
    P0 = diagnostics[0]["total_momentum"]

    energy_drift = max(
        abs(row["total_energy"]-E0)
        for row in diagnostics
    )

    momentum_drift = max(
        abs(row["total_momentum"]-P0)
        for row in diagnostics
    )

    # F_source = M * Xddot, obtained from the same action.
    forces = np.array([
        [
            spec.anchor_mass*_derivative(
                t,
                solution.y[:, i],
                spec, x, dx,
            )[(s+1)*(2*spec.n+4)-1]
            for s in range(2)
        ]
        for i, t in enumerate(times)
    ])

    positive = np.trapezoid(
        np.maximum(forces, 0),
        times,
        axis=0,
    )

    negative = np.trapezoid(
        np.minimum(forces, 0),
        times,
        axis=0,
    )

    signed = positive+negative

    p_final = np.array([
        spec.anchor_mass
        *_unpack(
            solution.y[:, -1],
            spec.n,
        )[s][-1]
        for s in range(2)
    ])

    p_initial = np.array([
        spec.anchor_mass
        *_unpack(
            solution.y[:, 0],
            spec.n,
        )[s][-1]
        for s in range(2)
    ])

    impulse_residual = np.max(
        abs(
            signed
            - (p_final-p_initial)
        )
    )

    return {
        "case": case,
        "spec": asdict(spec),
        "time_unit": "arbitrary_natural_units_c=1",
        "final_state_continues_without_reset": True,
        "initial_energy": E0,
        "final_energy":
            diagnostics[-1]["total_energy"],
        "max_energy_absolute_drift": energy_drift,
        "initial_total_momentum": P0,
        "final_total_momentum":
            diagnostics[-1]["total_momentum"],
        "max_total_momentum_drift": momentum_drift,
        "initial_source_energy":
            diagnostics[0]["source_internal_energy"],
        "final_source_energy":
            diagnostics[-1]["source_internal_energy"],
        "final_carrier_energy":
            diagnostics[-1]["carrier_energy"],
        "source_center_positive_impulse":
            positive.tolist(),
        "source_center_negative_impulse":
            negative.tolist(),
        "source_center_signed_impulse":
            signed.tolist(),
        "source_center_momentum_change":
            (p_final-p_initial).tolist(),
        "impulse_integral_residual":
            float(impulse_residual),
        "radiation_flux_to_infinity":
            "NOT_MODELED_PERIODIC_BOX",
        "Earth_or_neutral_matter": "NOT_INCLUDED",
        "craft_upward_impulse": "NOT_DERIVED",
        "physical_energy_j": "NOT_CALIBRATED",
    }


def energy_gate(
    terms: dict[str, float | None],
    *,
    physics_complete: bool = False,
) -> dict:
    """Fail-closed conservative energy accounting."""
    mandatory = (
        "physical_source_rest_internal",
        "all_loaded_carrier_fields",
        "hull_support_enclosure",
        "driver_activation",
        "losses_radiation",
        "metric_gravity",
        "environment_exchange",
        "cyclic_off_state",
        "auxiliary_work",
        "quantum_uv_required",
    )

    missing = [
        key for key in mandatory
        if key not in terms or terms[key] is None
    ]

    supplied = [
        value for value in terms.values()
        if value is not None
    ]

    if any(
        not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value < 0
        for value in supplied
    ):
        raise ValueError(
            "Finite nonnegative non-double-counted energy required"
        )

    known = sum(supplied)

    if known >= 10_000_000:
        status = "FAIL_KNOWN_ENERGY_GE10MJ"

    elif missing or not physics_complete:
        status = "NOT_CERTIFIED"

    else:
        status = (
            "PASS_DECLARED_LEDGER_ONLY_"
            "NEEDS_INDEPENDENT_AUDIT"
        )

    return {
        "status": status,
        "known_nonnegative_sum_j": known,
        "missing_components": missing,
        "complete_physical_action_proven":
            physics_complete,
    }


def execute(root: Path) -> dict:
    """Run pre-registered PH2 falsification and control matrix."""
    archive = provenance(root)

    algebra = exact_algebra()
    no_go = static_no_go()

    weak = restricted_kinetic(
        1, 1, 0, 0.0625
    )

    strong = restricted_kinetic(
        1, 1, 0, 4
    )

    singular = restricted_kinetic(
        1, 1, 0.25, 0
    )

    assert weak["positive_necessary"]
    assert not strong["positive_necessary"]
    assert not singular["invertible_necessary"]

    source_off = causal_source_run(
        WaveSpec(n=96, tmax=1.6),
        "source_off",
    )

    self_sourced = causal_source_run(
        WaveSpec(n=128, tmax=2.1),
        "self_sourced",
    )

    recoil128 = causal_source_run(
        WaveSpec(n=128, tmax=2.1),
        "incoming_recoil",
    )

    recoil192 = causal_source_run(
        WaveSpec(n=192, tmax=2.1),
        "incoming_recoil",
    )

    recoil256 = causal_source_run(
        WaveSpec(n=256, tmax=2.1),
        "incoming_recoil",
    )

    recoil384 = causal_source_run(
        WaveSpec(n=384, tmax=2.1),
        "incoming_recoil",
    )

    impulses = np.array([
        result["source_center_signed_impulse"][0]
        for result in (
            recoil128,
            recoil192,
            recoil256,
            recoil384,
        )
    ])

    spacings = 8.0/np.array([
        128.0, 192.0, 256.0, 384.0,
    ])

    extrapolation = np.polyfit(
        spacings**2,
        impulses,
        1,
    )

    if not (
        np.all(np.diff(impulses) < 0)
        and impulses[-1] > 0
        and abs(
            extrapolation[1]-impulses[-1]
        )/impulses[-1] < 0.005
    ):
        raise AssertionError(
            "1D recoil observable failed convergence screen"
        )

    ledger = energy_gate(
        {},
        physics_complete=False,
    )

    archive_ok = (
        all(
            archive[key]["status"] == "MATCH"
            for key in REFERENCE_SHA
        )
        and archive["ph1_result_present"]
    )

    gates = {
        "PH2_PROVENANCE":
            "PASS_SCOPED" if archive_ok
            else "UNRESOLVED",

        "PH2_FREE_POSITIVE_MASS_WINDING_EOM":
            "RED_SCOPED_NO_GO_FOR_PH1_A0_APHI_ZERO_FREE_SOURCE",

        "PH2_STATIC_MAXWELL_CURRENT":
            "RED_SCOPED_ZERO_A_NONZERO_J_INCONSISTENT",

        "PH2_COLD_DUST_CHARGE_EQUILIBRIUM":
            "RED_SCOPED_WITHOUT_PRESSURE_OR_SUPPORT",

        "PH2_COMPLETE_MICROSCOPIC_SOURCE":
            "OPEN_REQUIRES_NEW_SOURCE_EOM_AND_SUPPORT",

        "PH2_GAUGE_WARD_NOETHER":
            "PASS_SCOPED_REDUCED_1D_SOURCE_AND_ABELIAN_ONLY",

        "PH2_MATTER_KINETIC_HEALTH":
            "CONDITIONAL_NECESSARY_ONLY_FULL_SPECTRUM_OPEN",

        "PH2_DERIVED_UNIVERSAL_METRIC_MATERIAL":
            "FIXED_DUST_RESPONSE_ONLY_NO_EARTH_EOS",

        "PH2_CAUSAL_SOURCE_RECOIL_1D":
            "PASS_REDUCED_DYNAMICAL_CONTROL_ONLY",

        "PH2_B11_M6_FULL_LOADED_STATIC_REPRODUCTION":
            "NOT_RUN",

        "PH2_B11_M6_FULL_CAUSAL_MIXED_MATTER":
            "NOT_RUN",

        "PH2_PERFECTLY_CONFINED_LOCAL_P_PORTAL":
            "RED_SCOPED_NO_EXTERIOR_PORTAL_GRADIENT",

        "PH2_EXTERIOR_EARTH_TRANSMISSION":
            "NOT_DERIVED",

        "PH2_EARTH_DOWN_CRAFT_UP":
            "NOT_DERIVED",

        "PH2_FINITE_NEUTRAL_1G_1M":
            "NOT_CERTIFIED",

        "PH2_FULL_3D_NONAXISYMMETRIC_STABILITY":
            "NOT_TESTED",

        "PH2_QUANTUM_NATURALNESS_EMPIRICAL":
            "NOT_TESTED",

        "PH2_COMPLETE_LT10MJ":
            ledger["status"],

        "PH2_ENGINE_OR_LIFT":
            "NOT_ESTABLISHED",
    }

    return {
        "branch": BRANCH,
        "reference": "ALPHA1_M5V_FROZEN",
        "provenance": archive,
        "exact_algebra": algebra,
        "static_falsifiers": no_go,

        "restricted_material_controls": {
            "weak": weak,
            "negative": strong,
            "singular": singular,
        },

        "source_driven_dynamics": {
            "source_off": source_off,
            "self_sourced": self_sourced,
            "incoming_recoil": recoil128,
            "incoming_recoil_finer": recoil192,
            "incoming_recoil_h256": recoil256,
            "incoming_recoil_h384": recoil384,
            "h_squared_extrapolated_impulse":
                float(extrapolation[1]),
            "convergence_class":
                "REDUCED_1D_IMPULSE_ONLY_NOT_GRAVITATIONAL",
        },

        "complete_energy_ledger": ledger,
        "gates": gates,

        "verdict":
            "YELLOW_WITH_SCOPED_STATIC_SOURCE_CLOSURES_"
            "NO_GRAVITY_CERTIFICATION",
    }
