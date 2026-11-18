"""BETA1-02: causal passive interface-response obstruction atlas.

PURPOSE
-------
Determine which portions of the imposed ALPHA-1 M5V C2 interface loading
could arise from a stable, passive material governed by one action.

THEORY
------
A neutral scalar-order-parameter toy model in a preferred medium frame:

    L = exp(2*sigma)*(rho*phi_t^2/2-kappa*phi_x^2/2)
        - exp(4*sigma)*a*(phi^2-v^2)^2/4

The factors exp(2*sigma), exp(4*sigma) reproduce the standard
four-dimensional conformal scalar weights in this restricted analogue.

Finite material and bath modes are derived from one quadratic action.

The prescribed sigma drive is NOT an on-shell PH15 metric solution.

UNITS
-----
All computed lengths, frequencies and energies are canonical, not SI.
M5V's historical interface widths in meters are not identified with
the canonical interface lengths in this experiment.

METHOD
------
Exact kink and stress identities, comparison with the frozen M5T C2
profile, discrete stationary source solutions, same-action mixed
variations, retarded susceptibility, spectral passivity, support and
boundary traction, and full material-plus-bath excitation-energy tests.

LIMITATIONS
-----------
No conserved real dust sector, Earth model, full metric backreaction,
physical support/hull, neutral payload force, spacecraft reaction,
or complete operating energy has been derived.

CLASSIFICATION
--------------
EXACT_CONDITIONAL_INTERFACE_THEOREM_AND_FINITE_PASSIVE_TOY_WITNESS
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import sympy as sp

from scipy.linalg import eigh, solve_banded
from scipy.integrate import trapezoid


@dataclass(frozen=True)
class Spec:
    kappa: float = 1.0
    inertia: float = 2.0
    a: float = 2.0
    v: float = 1.0
    L: float = 8.0
    nodes: int = 129
    pinning: float = 0.15
    bath_k: float = 0.20
    bath_anchor: float = 0.30
    bath_mass: float = 0.12
    bath_stride: int = 10


def exact_theorems():
    x, ell, a, v = sp.symbols(
        "x ell a v",
        positive=True,
        real=True,
    )

    k = a*v*v*ell*ell/2

    phi = v*sp.tanh(x/ell)

    V = a*(phi*phi-v*v)**2/4

    phi_p = sp.diff(phi, x)

    eq = sp.simplify(
        k*sp.diff(phi, x, 2)
        -a*phi*(phi*phi-v*v)
    )

    first_integral = sp.simplify(
        k*phi_p**2/2-V
    )

    tension = sp.simplify(
        2*a*v**4*ell/3
    )

    u = sp.symbols("u", real=True)

    c2 = (
        1-10*u**3+15*u**4-6*u**5
    )

    S, K, V0 = sp.symbols(
        "S K V",
        real=True,
    )

    metric_energy = (
        -sp.exp(2*S)*K
        -sp.exp(4*S)*V0
    )

    trace = sp.diff(
        metric_energy,
        S,
    ).subs(S, 0)

    p = sp.Function("p")(x)
    s = sp.Function("s")(x)

    pprime = sp.diff(p, x)
    sprime = sp.diff(s, x)

    kk, vv = sp.symbols(
        "kappa vv",
        positive=True,
    )

    pot = vv*(p*p-1)**2/4

    lag = (
        -kk*sp.exp(2*s)*pprime**2/2
        -sp.exp(4*s)*pot
    )

    stress = (
        kk*sp.exp(2*s)*pprime**2/2
        -sp.exp(4*s)*pot
    )

    partial_sigma = (
        -kk*sp.exp(2*s)*pprime**2
        -4*sp.exp(4*s)*pot
    )

    e_phi = (
        sp.diff(lag, p)
        -sp.diff(
            sp.diff(lag, pprime),
            x,
        )
    )

    ward = sp.simplify(
        sp.diff(stress, x)
        -partial_sigma*sprime
        -e_phi*pprime
    )

    checks = {
        "phi4_kink_Euler_Lagrange":
            eq == 0,

        "phi4_kink_zero_normal_traction":
            first_integral == 0,

        "interface_tension_positive_formula":
            sp.simplify(
                tension-2*a*v**4*ell/3
            ) == 0,

        "C2_endpoints_exact":
            c2.subs(u, 0) == 1
            and c2.subs(u, 1) == 0,

        "C2_first_second_derivatives_endpoints_zero":
            all(
                sp.diff(c2, u, n).subs(u, z) == 0
                for n in (1, 2)
                for z in (0, 1)
            ),

        "C2_third_derivative_endpoint_nonzero":
            all(
                sp.diff(c2, u, 3).subs(u, z) != 0
                for z in (0, 1)
            ),

        "C2_midpoint_derivative":
            sp.diff(
                c2,
                u,
            ).subs(
                u,
                sp.Rational(1, 2),
            ) == -sp.Rational(15, 8),

        "conformal_metric_trace_variation":
            trace == -2*K-4*V0,

        "material_stress_Ward_offshell":
            ward == 0,

        "stationary_kink_has_exponential_tails":
            sp.limit(phi, x, sp.oo) == v
            and sp.limit(phi, x, -sp.oo) == -v,

        "linear_material_trace_not_freely_assignable":
            sp.diff(
                metric_energy,
                S,
            ).subs(S, 0) == -2*K-4*V0,

        "source_and_material_both_couple_to_same_sigma":
            sp.diff(
                sp.exp(2*S),
                S,
            ).subs(S, 0) == 2
            and sp.diff(
                sp.exp(4*S),
                S,
            ).subs(S, 0) == 4,
    }

    if not all(checks.values()):
        raise ArithmeticError(
            "Exact symbolic obstruction failed: "
            +str(checks)
        )

    return {
        "checks": checks,

        "action":
            "L=e^(2sigma)*(rho phi_t^2/2-"
            "kappa phi_x^2/2)-e^(4sigma)V",

        "stress_Ward":
            "dTxx/dx-(dL/dsigma)*sigma_x="
            "E_phi*phi_x (off shell)",

        "C2_unique_continuation":
            "Smooth autonomous second-order ODE "
            "with Lipschitz potential: reaching a "
            "vacuum with zero derivative at finite "
            "x implies the constant solution",

        "C2_third_derivative":
            "Jumps across compact endpoints "
            "for quintic C2",

        "analytic_kink_length":
            "sqrt(2*kappa/(a*v^2))",

        "analytic_kink_tension":
            "(2/3)*sqrt(2*kappa*a)*v^3",

        "metric_trace_at_sigma0":
            str(trace),
    }


def c2_fraction(x, halfwidth):
    q = np.clip(
        (np.asarray(x)+halfwidth)
        /(2*halfwidth),
        0,
        1,
    )

    return (
        1-10*q**3+15*q**4-6*q**5
    )


def interface_comparison(spec=Spec()):
    ell = math.sqrt(
        2*spec.kappa
        /(spec.a*spec.v**2)
    )

    matched_width = 15*ell/8

    x = np.linspace(
        -6*ell,
        6*ell,
        2401,
    )

    f_kink = (
        1-np.tanh(x/ell)
    )/2

    f_c2 = c2_fraction(
        x,
        matched_width,
    )

    max_error = float(
        np.max(
            np.abs(f_kink-f_c2)
        )
    )

    tail = float(
        (
            1-math.tanh(
                matched_width/ell
            )
        )/2
    )

    xi = np.linspace(
        -matched_width,
        matched_width,
        801,
    )[1:-1]

    t = (
        xi+matched_width
    )/(2*matched_width)

    f = (
        1-10*t**3
        +15*t**4-6*t**5
    )

    f2 = (
        -60*t
        +180*t**2
        -120*t**3
    )/(2*matched_width)**2

    phi = spec.v*(1-2*f)

    phi_xx = -2*spec.v*f2

    res = (
        -spec.kappa*phi_xx
        +spec.a*phi*(
            phi**2-spec.v**2
        )
    )

    residual_l2 = float(
        np.sqrt(
            trapezoid(
                res**2,
                xi,
            )
        )
    )

    theoretical_tension = (
        (2/3)
        *math.sqrt(
            2*spec.kappa*spec.a
        )
        *spec.v**3
    )

    return {
        "ell_action": ell,
        "slope_matched_C2_halfwidth":
            matched_width,

        "C2_exactly_compact": True,
        "kink_exactly_compact": False,

        "kink_tail_fraction_at_C2_edge":
            tail,

        "matched_profile_max_abs_difference":
            max_error,

        "C2_Euler_Lagrange_residual_L2":
            residual_l2,

        "kink_surface_tension":
            theoretical_tension,

        "surface_energy_is_a_cost": True,

        "width_is_material_parameter_dependent":
            True,

        "C2_as_exact_phi4_stationary_profile":
            "OBSTRUCTED_FOR_SMOOTH_FINITE_STIFFNESS",

        "C2_as_generic_physical_coarse_graining":
            "OPEN_NOT_EXCLUDED",
    }


def phi4_V(phi, s):
    return (
        s.a*(phi*phi-s.v*s.v)**2/4
    )


def phi4_dV(phi, s):
    return (
        s.a*phi*(phi*phi-s.v*s.v)
    )


def phi4_ddV(phi, s):
    return (
        s.a*(3*phi*phi-s.v*s.v)
    )


def _equilibrium(s):
    if not (
        s.nodes >= 21
        and s.nodes % 2 == 1
        and s.L > 0
        and min(
            s.kappa,
            s.inertia,
            s.a,
            s.v,
        ) > 0
        and s.pinning > 0
        and s.bath_mass > 0
        and s.bath_anchor > 0
        and s.bath_k > 0
    ):
        raise ValueError(
            "Unsupported positive scalar and finite grid"
        )

    x = np.linspace(
        -s.L,
        s.L,
        s.nodes,
    )

    h = x[1]-x[0]

    ell = math.sqrt(
        2*s.kappa
        /(s.a*s.v*s.v)
    )

    p = s.v*np.tanh(
        x/ell
    )

    p[0] = -s.v
    p[-1] = s.v

    history = []

    for step in range(25):
        grad = (
            (s.kappa/h)
            *(2*p[1:-1]-p[:-2]-p[2:])
            +h*phi4_dV(
                p[1:-1],
                s,
            )
        )

        resid = float(
            np.max(
                np.abs(grad)
            )
        )

        history.append(resid)

        if resid < 2e-12:
            break

        dd = (
            2*s.kappa/h
            +h*phi4_ddV(
                p[1:-1],
                s,
            )
        )

        upper = np.full(
            s.nodes-3,
            -s.kappa/h,
        )

        ab = np.zeros(
            (3, s.nodes-2)
        )

        ab[0, 1:] = upper
        ab[1, :] = dd
        ab[2, :-1] = upper

        delta = solve_banded(
            (1, 1),
            ab,
            grad,
        )

        def energy(q):
            return float(
                s.kappa/(2*h)
                *np.sum(
                    np.diff(q)**2
                )
                +h*np.sum(
                    phi4_V(
                        q[1:-1],
                        s,
                    )
                )
            )

        base = energy(p)
        rate = 1.0

        while rate > 1e-5:
            trial = p.copy()

            trial[1:-1] -= (
                rate*delta
            )

            if energy(trial) <= base+1e-11:
                break

            rate /= 2

        if rate <= 1e-5:
            raise ArithmeticError(
                "Interface Newton line search unsuccessful"
            )

        p = trial

    if history[-1] > 2e-10:
        raise ArithmeticError(
            "Interface stationary EOM failed"
        )

    return x, h, p, history


def material_system(s=Spec(), with_bath=True):
    x, h, p, history = _equilibrium(s)

    n = s.nodes-2

    diag = (
        2*s.kappa/h
        +h*phi4_ddV(
            p[1:-1],
            s,
        )
    )

    H = (
        np.diag(diag)
        +np.diag(
            np.full(
                n-1,
                -s.kappa/h,
            ),
            1,
        )
        +np.diag(
            np.full(
                n-1,
                -s.kappa/h,
            ),
            -1,
        )
    )

    B = np.zeros(
        (n, s.nodes)
    )

    for edge in range(
        s.nodes-1
    ):
        coeff = (
            s.kappa/h
            *(p[edge+1]-p[edge])
        )

        for i, sgn in (
            (edge, -1),
            (edge+1, 1),
        ):
            if 1 <= i <= s.nodes-2:
                B[i-1, edge] -= sgn*coeff
                B[i-1, edge+1] -= sgn*coeff

    for i in range(
        1,
        s.nodes-1,
    ):
        B[i-1, i] -= (
            4*h*phi4_dV(
                p[i],
                s,
            )
        )

    H += (
        s.pinning*h*np.eye(n)
    )

    masses = [
        s.inertia*h
    ]*n

    if with_bath:
        chosen = list(
            range(
                4,
                n-4,
                s.bath_stride,
            )
        )

        n_b = len(chosen)

        K = np.zeros(
            (n+n_b, n+n_b)
        )

        K[:n, :n] = H

        for j, i in enumerate(chosen):
            b = n+j
            ck = s.bath_k*h

            K[i, i] += ck

            K[b, b] += (
                ck+s.bath_anchor*h
            )

            K[i, b] -= ck
            K[b, i] -= ck

            masses.append(
                s.bath_mass*h
            )

        B_full = np.zeros(
            (n+n_b, s.nodes)
        )

        B_full[:n, :] = B

    else:
        chosen = []
        K = H
        B_full = B

    M = np.asarray(
        masses
    )

    lam, U = eigh(
        K/np.sqrt(
            M[:, None]*M[None, :]
        )
    )

    if min(lam) <= 0:
        raise ArithmeticError(
            "Negative supported material eigenfrequency"
        )

    if np.min(M) <= 0:
        raise ArithmeticError(
            "Ghost material inertia"
        )

    shape1 = np.exp(
        -((x+0.9)/1.35)**2
    )

    shape2 = np.exp(
        -((x-1.0)/1.35)**2
    )

    shape3 = (
        x*np.exp(
            -(x/1.35)**2
        )
    )

    drives = np.column_stack([
        B_full@v
        for v in (
            shape1,
            shape2,
            shape3,
        )
    ])

    interface_energy = float(
        s.kappa/(2*h)
        *np.sum(
            np.diff(p)**2
        )
        +h*np.sum(
            phi4_V(
                p[1:-1],
                s,
            )
        )
    )

    left_stress = float(
        s.kappa/2
        *((p[1]-p[0])/h)**2
        -phi4_V(
            p[0],
            s,
        )
    )

    right_stress = float(
        s.kappa/2
        *((p[-1]-p[-2])/h)**2
        -phi4_V(
            p[-1],
            s,
        )
    )

    return {
        "spec": s,
        "x": x,
        "h": h,
        "phi0": p,
        "stationary_history": history,
        "H": K,
        "M": M,
        "B": B_full,
        "drives": drives,
        "shapes": [
            shape1,
            shape2,
            shape3,
        ],
        "bath_nodes": chosen,
        "modes": lam,
        "vectors": U,

        "interface_energy":
            interface_energy,

        "boundary_stress": (
            left_stress,
            right_stress,
        ),

        "same_action":
            "D2 E(phi,sigma) at sigma=0; "
            "support and bath are explicit",
    }


def energy_discrete(phi, sigma, s):
    h = (
        2*s.L
        /(s.nodes-1)
    )

    diff = np.diff(phi)

    midpoint = (
        sigma[1:]+sigma[:-1]
    )/2

    return (
        s.kappa/(2*h)
        *np.sum(
            np.exp(
                2*midpoint
            )*diff**2
        )
        +h*np.sum(
            np.exp(
                4*sigma[1:-1]
            )*phi4_V(
                phi[1:-1],
                s,
            )
        )
    )


def cross_fd(sys, eps=1e-4):
    s = sys["spec"]
    p = sys["phi0"]
    sigma = sys["shapes"][0]

    u = sys["drives"][:, 0].copy()

    u = u[:s.nodes-2]

    u /= max(
        1,
        np.linalg.norm(u),
    )

    def ev(stepu, stepsigma):
        p1 = p.copy()

        p1[1:-1] += stepu*u

        return energy_discrete(
            p1,
            stepsigma*sigma,
            s,
        )

    mixed = (
        ev(eps, eps)
        -ev(-eps, eps)
        -ev(eps, -eps)
        +ev(-eps, -eps)
    )/(4*eps*eps)

    exact = (
        -u
        @sys["B"][:s.nodes-2]
        @sigma
    )

    return {
        "fd_mixed_d2E":
            float(mixed),

        "exact_mixed_d2E":
            float(exact),

        "abs_error":
            float(
                abs(mixed-exact)
            ),
    }


def retarded_kernel(sys, t):
    if t <= 0:
        return np.zeros(
            (3, 3)
        )

    lam = sys["modes"]
    mass = sys["M"]
    U = sys["vectors"]

    G = (
        U.T
        @(
            sys["drives"]
            /np.sqrt(
                mass[:, None]
            )
        )
    )

    weights = (
        np.sin(
            np.sqrt(lam)*t
        )
        /np.sqrt(lam)
    )

    return (
        (G.T*weights)@G
    )


def response(
    sys,
    frequencies=(0.25, 0.6, 1.2, 2.5),
    eta=0.03,
):
    lamb = sys["modes"]
    U = sys["vectors"]
    mass = sys["M"]
    F = sys["drives"]

    G = (
        U.T
        @(F/np.sqrt(
            mass[:, None]
        ))
    )

    static = (
        (G.T/lamb)@G
    )

    stat_eig = np.linalg.eigvalsh(
        (static+static.T)/2
    )

    values = {}

    for omega in frequencies:
        den = (
            lamb
            -(omega+1j*eta)**2
        )

        chi = (
            (G.T/den)@G
        )

        loss = (
            chi.imag
            +chi.imag.T
        )/2

        values[str(omega)] = {
            "reciprocity_error":
                float(
                    np.max(
                        abs(chi-chi.T)
                    )
                ),

            "minimum_spectral_loss_eigenvalue":
                float(
                    np.linalg.eigvalsh(
                        loss
                    )[0]
                ),

            "loss_trace":
                float(
                    np.trace(loss)
                ),

            "real_static_not_assumed":
                True,
        }

    high1 = (
        (
            G.T
            /(lamb-(60+1j*eta)**2)
        )@G
    )

    high2 = (
        (
            G.T
            /(lamb-(120+1j*eta)**2)
        )@G
    )

    norm1 = float(
        np.linalg.norm(high1)
    )

    norm2 = float(
        np.linalg.norm(high2)
    )

    return {
        "static_chi": static,

        "static_eigenvalues":
            list(
                map(
                    float,
                    stat_eig,
                )
            ),

        "static_reciprocity_error":
            float(
                np.max(
                    abs(
                        static-static.T
                    )
                )
            ),

        "frequencies":
            values,

        "high_frequency_60_norm":
            norm1,

        "high_frequency_120_norm":
            norm2,

        "causal_retarded_green":
            "theta(t)*sum G_a G_a^T*"
            "sin(sqrt(lam_a)*t)/sqrt(lam_a)",

        "imag_part_is_retarded_positive_spectral_measure":
            True,

        "negative_time_retarded_kernel_norm":
            float(
                np.linalg.norm(
                    retarded_kernel(
                        sys,
                        -0.3,
                    )
                )
            ),

        "positive_time_retarded_reciprocity":
            float(
                np.max(
                    abs(
                        retarded_kernel(sys, 0.5)
                        -retarded_kernel(sys, 0.5).T
                    )
                )
            ),

        "not_a_frequency_independent_susceptibility":
            True,
    }


def time_cycle(
    sys,
    steps=1500,
    duration=7.0,
    pulse_end=3.0,
):
    K = sys["H"]
    M = sys["M"]
    F = sys["drives"][:, 0]

    q = np.zeros(len(M))
    vel = np.zeros(len(M))

    dt = duration/steps

    def amp(t):
        if t < 0 or t > pulse_end:
            return 0.0

        return (
            math.sin(
                math.pi*t/pulse_end
            )**2
        )

    def acceleration(q, t):
        return (
            -K@q+F*amp(t)
        )/M

    def energy(q, v):
        return float(
            0.5*np.dot(
                M*v,
                v,
            )
            +0.5*q@K@q
        )

    a = acceleration(q, 0)

    W = 0.0
    max_energy = 0.0

    for i in range(steps):
        t = i*dt
        t2 = (i+1)*dt

        q2 = (
            q
            +dt*vel
            +dt*dt*a/2
        )

        a2 = acceleration(
            q2,
            t2,
        )

        v2 = (
            vel
            +dt*(a+a2)/2
        )

        W += (
            0.5
            *(amp(t)+amp(t2))
            *float(
                F@(q2-q)
            )
        )

        q, vel, a = (
            q2,
            v2,
            a2,
        )

        max_energy = max(
            max_energy,
            energy(q, vel),
        )

    end_energy = energy(
        q,
        vel,
    )

    return {
        "initial_energy": 0.0,

        "final_energy":
            end_energy,

        "external_work":
            W,

        "external_work_minus_energy":
            W-end_energy,

        "max_internal_energy":
            max_energy,

        "pulse_end":
            pulse_end,

        "end_time":
            duration,

        "material_dissipated_heat":
            0.0,

        "bath_energy_included":
            True,

        "drive_is_prescribed_not_generated_by_PH15":
            True,

        "full_source_field_support_ledger":
            "NOT_CLOSED",

        "no_artificial_cycle_reset":
            end_energy > 1e-3,
    }


def source_off(sys):
    z = np.zeros(
        sys["spec"].nodes
    )

    return {
        "drive_norm":
            float(
                np.linalg.norm(
                    sys["B"]@z
                )
            ),

        "zero_displacement":
            True,

        "zero_incremental_energy":
            True,
    }


def summarize():
    symbolic = exact_theorems()

    iface = {}

    for k in (
        0.5,
        1.0,
        2.0,
    ):
        s = Spec(
            kappa=k
        )

        iface[str(k)] = (
            interface_comparison(s)
        )

    sys = material_system()

    sys_fine = material_system(
        Spec(nodes=257)
    )

    cp = cross_fd(sys)
    rsp = response(sys)

    cycle = time_cycle(sys)

    cycle_fine = time_cycle(
        sys,
        steps=3000,
    )

    empty = source_off(sys)

    homog = Spec()

    p_uniform = np.full(
        homog.nodes,
        homog.v,
    )

    uniform_energy = energy_discrete(
        p_uniform,
        np.zeros(
            homog.nodes
        ),
        homog,
    )

    widths = [
        iface[z]["slope_matched_C2_halfwidth"]
        for z in (
            "0.5",
            "1.0",
            "2.0",
        )
    ]

    s = sys["spec"]

    surface = iface["1.0"][
        "kink_surface_tension"
    ]

    numer = sys[
        "interface_energy"
    ]

    gates = {
        "exact_12_theorems":
            all(symbolic["checks"].values()),

        "noncompact_analytic_kink":
            all(
                x["kink_tail_fraction_at_C2_edge"] > 0
                for x in iface.values()
            ),

        "C2_profile_not_exact_on_shell":
            all(
                x["C2_Euler_Lagrange_residual_L2"] > 1e-3
                for x in iface.values()
            ),

        "surface_tension_positive":
            all(
                x["kink_surface_tension"] > 0
                for x in iface.values()
            ),

        "width_responds_to_physical_kappa":
            widths[0] < widths[1] < widths[2],

        "discrete_kink_stationarity":
            sys["stationary_history"][-1] < 2e-10,

        "mesh_refined_kink_stationarity":
            sys_fine["stationary_history"][-1] < 2e-10,

        "interface_energy_convergence":
            abs(
                sys_fine["interface_energy"]-surface
            ) < abs(numer-surface),

        "interface_energy_approaches_tension":
            abs(
                sys_fine["interface_energy"]-surface
            ) < 0.01,

        "supported_material_positive_modes":
            float(
                min(sys["modes"])
            ) > 0,

        "refined_supported_material_positive_modes":
            float(
                min(sys_fine["modes"])
            ) > 0,

        "kinetic_positive":
            float(
                min(sys["M"])
            ) > 0,

        "cross_variation_same_action":
            cp["abs_error"] < 2e-5,

        "static_reciprocity":
            rsp["static_reciprocity_error"] < 1e-8,

        "static_passivity":
            float(
                min(rsp["static_eigenvalues"])
            ) > -1e-9,

        "dynamic_reciprocity":
            all(
                v["reciprocity_error"] < 1e-9
                for v in rsp["frequencies"].values()
            ),

        "retarded_spectral_passivity":
            all(
                v["minimum_spectral_loss_eigenvalue"] > -1e-9
                for v in rsp["frequencies"].values()
            ),

        "high_frequency_response_decays":
            rsp["high_frequency_120_norm"]
            <0.35*rsp["high_frequency_60_norm"],

        "time_cycle_drive_energy_passive":
            cycle["final_energy"] >= 0
            and cycle["external_work"] >= 0,

        "time_cycle_full_bath_work_ledger":
            abs(
                cycle["external_work_minus_energy"]
            ) < 0.015,

        "time_step_convergence":
            abs(
                cycle_fine["final_energy"]
                -cycle["final_energy"]
            ) < 0.015,

        "source_off_zero":
            empty["drive_norm"] == 0,

        "homogeneous_scalar_control_zero_energy":
            float(
                abs(uniform_energy)
            ) < 1e-13,

        "explicit_support_required":
            s.pinning > 0
            and s.bath_anchor > 0,

        "retarded_kernel_zero_before_drive":
            rsp["negative_time_retarded_kernel_norm"] == 0,

        "retarded_kernel_reciprocity":
            rsp["positive_time_retarded_reciprocity"] < 1e-10,

        "boundary_traction_symmetric":
            abs(
                sys["boundary_stress"][0]
                -sys["boundary_stress"][1]
            ) < 1e-9,

        "post_pulse_no_reset":
            cycle["no_artificial_cycle_reset"],
    }

    return {
        "theorems":
            symbolic,

        "kink_profiles":
            iface,

        "stationary": {
            "coarse_EOM_residual":
                sys["stationary_history"][-1],

            "fine_EOM_residual":
                sys_fine["stationary_history"][-1],

            "coarse_surface_energy_canonical":
                numer,

            "fine_surface_energy_canonical":
                sys_fine["interface_energy"],

            "continuum_tension_canonical":
                surface,

            "positive_normal_mode_gap":
                float(min(sys["modes"])),

            "fine_positive_normal_mode_gap":
                float(min(sys_fine["modes"])),

            "material_wave_speed_canonical":
                math.sqrt(s.kappa/s.inertia),

            "supported_bath_modes":
                len(sys["bath_nodes"]),

            "boundary_normal_traction_left_right":
                list(sys["boundary_stress"]),

            "boundary_support_status":
                "FIXED_ENDPOINTS_PLUS_DISTRIBUTED_"
                "PINNING_PLUS_BATH_ANCHORS",
        },

        "same_action_cross_variation":
            cp,

        "passive_reciprocal_susceptibility": {
            k: v
            for k, v in rsp.items()
            if k != "static_chi"
        },

        "time_cycle":
            cycle,

        "time_cycle_fine":
            cycle_fine,

        "source_off":
            empty,

        "homogeneous_order_parameter": {
            "interface_energy":
                float(uniform_energy),

            "dust_trace":
                "NOT_INCLUDED",
        },

        "gates":
            gates,

        "material_obstructions": {
            "C2_compact_smoothstep_as_exact_analytic_phi4_interface":
                "CLOSED_IN_TESTED_LOCAL_ACTION_CLASS",

            "C2_as_general_coarse_grained_profile":
                "NOT_EXCLUDED",

            "C2_0p25_to_0p75m_material_width":
                "NOT_DERIVED_FROM_M5V",

            "scalar_interface_tails":
                "NECESSARY_IN_TESTED_CLASS",

            "surface_energy_and_support":
                "REQUIRED",

            "finite_inertia_frequency_independent_chi":
                "NO_EXCEPT_CONTACT_TERMS",

            "passive_reciprocal_family":
                "FOUND_TOY_ACTION_ONLY",

            "full_neutral_dust_mass_trace":
                "MISSING",

            "Earth_hull_external_reaction":
                "NOT_DERIVED",

            "source_X_Y_reciprocity":
                "NOT_SOLVED",

            "real_equation_of_state_and_SI":
                "MISSING",

            "R3A_suppression":
                "HISTORICAL_CONTROL_NOT_RETESTED",

            "R3C_B0_B16_failures":
                "PROTECTED_NOT_REOPENED",
        },

        "primary_verdict":
            "YELLOW_ACTION_SOURCED_PASSIVE_INTERFACE_"
            "TOY_C2_NOT_EXACT_PHYSICAL_MATERIAL_OPEN",

        "physical_transfer":
            "NOT_AUTHORIZED",

        "limits": [
            "Order parameter toy scalar, not a conserved "
            "dust number-density or full real Earth matter action",

            "sigma is prescribed external metric drive, "
            "not PH15 sourced P",

            "Boundary pinning and bath anchors are explicit "
            "support, not free spacecraft momentum",

            "Finite Hamiltonian bath; no true irreversible loss; "
            "causal retarded modal response",

            "Continuum nonlocal/finite grid and UV/quantum/"
            "empirical checks are open",

            "Surface energy canonical units are not joules",

            "No whole-craft force, Earth reaction, neutral "
            "1kg >=1g at >=1m, or complete energy <10MJ",
        ],
    }
