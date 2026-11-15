"""HOOK17-PH3: mixed-P universal-metric causal-characteristic falsifier.

SCIENCE
-------
Local fixed-background positive-density dust control for two canonical
massless U(1) fields. Units c=1; signature (-,+,+,+). The candidate
universal metric is gtilde=exp(2*sigma(P))*g, with
P=E_X dot B_Y + E_Y dot B_X in the declared R3X1-compatible
orientation (overall Hodge sign is absorbed in the portal coefficient).

For fixed local rest-density rho>0, choose L=-1/4*(F_X^2+F_Y^2)
-rho*exp(sigma(P)). The matter term represents an immobile supported
dust background; its missing support, metric/gravity, and charged source
modes make this a NECESSARY restricted preflight, not a physical model.

Around aligned constant E_X=E zhat, B_Y=B zhat, other backgrounds zero,
propagation along x, and perturbations a=A_X,z cos(kx), b=A_Y,y sin(kx),
constant theta=-rho*exp(sigma)*sigma' is a boundary/topological term.
The quadratic propagating sector is
    L2 ~ (Adot^2+bdot^2-k^2*(A^2+b^2)
          -chi*(Bbar*Adot+Ebar*k*b)^2)/4,
where Bbar and Ebar are the background magnetic/electric fields;
A and b are distinct gauge perturbation amplitudes. The material
curvature is chi=rho*exp(sigma)*(sigma''+sigma'^2).

The exact transverse characteristic polynomial is
    (s^2-1)*[(1-chi*mag^2)*s^2-(1+chi*elec^2)] = 0,
where s=omega/k, and the companion luminal modes remain omitted from
this two-polarization block. The extraordinary speed squared is
    v^2 = (1+chi*elec^2)/(1-chi*mag^2).

A linear sigma=kappa*P has chi=rho*kappa^2*exp(kappa*P)>0 for
rho>0 and nonzero kappa. Therefore, when the restricted kinetic
and gradient coefficients are positive and E or B is nonzero,
this subsystem has a faster-than-physical-metric-null characteristic.
If the kinetic coefficient is nonpositive, its quadratic kinetic mode
is degenerate or negative. This is a conditional restriction of this
frozen-dust candidate, not a universal no-go theorem and not a
complete gauge/gravity/material characteristic classification.

A negative quadratic parity-even sigma=-lambda*P^2 is shown only as a
mathematical comparison; it is not a certified rescue and has distinct
source, response, UV and empirical obligations.

CLAIMS PROHIBITED
-----------------
No stable microscopic source, Earth interaction, lift, propulsion,
1g/1m physically loaded response, B11-M6 pulse or <10MJ device.
Historic ALPHA-1 M5V remains frozen and untouched.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
import math

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

BRANCH = "032H17A12D1R3X3B17-PH3"

HISTORIC = {
    "m5v_module": (
        "src/antigravity_research/agminer/"
        "hook17_r3b_m5v_unified_exterior_action.py",
        "ea193cd163b2fc87e6973878c77e27c761f0625f6c5de3f38594587ef6cdb80f",
    ),
    "ph1_module": (
        "src/antigravity_research/agminer/"
        "hook17_ph1_physicalization_preflight.py",
        "47281ea38e40351944bc194375b4732b28c58960d7acf644f6d040b82fd0aa52",
    ),
    "ph2_module": (
        "src/antigravity_research/agminer/"
        "hook17_ph2_source_causal_audit.py",
        "b3747d1f2d5f094721e068fce06c2331eb5400a4485777604cfdb53a8de723d5",
    ),
    "m5v_result": (
        "results/data/b17_m5v_unified_20261114T203555409373Z_full_bundle.json",
        "53f63f93fe9f525302f516b6376fa227d4b46027e6a0f75ae4dd35404da8c52b",
    ),
    "ph2_latest_uploaded_result": (
        "results/data/032h17_ph2_source_causal_20261115T000042956569Z.json",
        "d35ec4f834517a31f334aa5a3e0e11bd3f2f1e19eef50fa392d1f95d7db104ce",
    ),
}


@dataclass(frozen=True)
class Background:
    label: str
    law: str
    rho: float
    coupling: float
    electric: float
    magnetic: float


def portal_derivatives(
    law: str,
    coupling: float,
    p: float,
) -> tuple[float, float, float]:
    """sigma, sigma', sigma'' at fixed P; no fitted C2 coefficient."""
    if law == "linear":
        return coupling*p, coupling, 0.0
    if law == "even_negative":
        return -coupling*p*p, -2*coupling*p, -2*coupling
    if law == "even_positive":
        return coupling*p*p, 2*coupling*p, 2*coupling
    raise ValueError("Unknown portal law")


def characteristic(case: Background) -> dict:
    """Aligned two-sector transverse characteristic, local dust control."""
    values = (
        case.rho, case.coupling, case.electric, case.magnetic
    )
    if not all(math.isfinite(float(v)) for v in values):
        raise ValueError("Nonfinite physical input")
    if case.rho < 0 or case.coupling < 0:
        raise ValueError("rho and portal magnitude must be nonnegative")

    p = case.electric*case.magnetic
    sigma, first, second = portal_derivatives(
        case.law, case.coupling, p
    )

    try:
        f = math.exp(sigma)
    except OverflowError as exc:
        raise ValueError("Uncontrolled exponential portal") from exc

    if not math.isfinite(f) or f == 0:
        raise ValueError("Nonfinite or underflowed metric factor")

    curvature = case.rho*f*(second+first*first)
    kinetic = 1-curvature*case.magnetic**2
    gradient = 1+curvature*case.electric**2
    metric_jacobian = 1-4*p*first

    if not all(math.isfinite(v) for v in (
        curvature, kinetic, gradient, metric_jacobian
    )):
        raise ValueError("Nonfinite constitutive/characteristic result")

    speed_sq = (
        gradient/kinetic
        if kinetic > 0 and gradient > 0
        else None
    )
    speed = math.sqrt(speed_sq) if speed_sq is not None else None

    if abs(metric_jacobian) <= 1e-12:
        status = "RED_NONINVERTIBLE_CONFORMAL_MAP"
    elif kinetic <= 0:
        status = "RED_KINETIC_DEGENERATE_OR_NEGATIVE"
    elif gradient <= 0:
        status = "RED_GRADIENT_DEGENERATE_OR_NEGATIVE"
    elif speed > 1+1e-12:
        status = "RED_SUPERLUMINAL_RESTRICTED_DUST"
    elif speed < 1-1e-12:
        status = "PASS_SCOPED_SUBLUMINAL_NOT_FULL_MODEL"
    else:
        status = (
            "PASS_SCOPED_LUMINAL_NO_NONTRIVIAL_RESPONSE_CERTIFIED"
        )

    return {
        "input": asdict(case),
        "p_background": p,
        "sigma": sigma,
        "sigma_prime": first,
        "sigma_double_prime": second,
        "theta_matter": -case.rho*f*first,
        "material_curvature_chi": curvature,
        "electric_kinetic_coefficient": kinetic,
        "gradient_coefficient": gradient,
        "conformal_trace_jacobian": metric_jacobian,
        "extraordinary_speed_squared_over_physical_c_squared":
            speed_sq,
        "extraordinary_speed_over_physical_c": speed,
        "verdict": status,
        "lawful_source_eom_and_support": "NOT_DERIVED",
        "all_constraint_and_material_modes": "NOT_TESTED",
    }


def symbolic_checks() -> dict:
    """Independent exact second variations, dispersion, and signs."""
    s, e, b, chi = sp.symbols("s e b chi", real=True)
    u, v, k, theta = sp.symbols("u v k theta", real=True)

    mode_matrix = sp.Matrix([
        [(1-chi*b*b)*s*s-1, -chi*e*b*s],
        [-chi*e*b*s, s*s-(1+chi*e*e)],
    ])
    factored = (
        (s*s-1)*(
            (1-chi*b*b)*s*s-(1+chi*e*e)
        )
    )
    assert sp.simplify(mode_matrix.det()-factored) == 0

    # Fixed theta cancels from the bulk principal symbol.
    assert sp.expand(
        theta*(s*u*k*v+s*v*(-k*u))
    ) == 0

    rho, kap, p = sp.symbols(
        "rho kap p", real=True, positive=True
    )
    F = rho*sp.exp(kap*p)

    assert sp.simplify(
        sp.diff(F, p, 2)-rho*kap**2*sp.exp(kap*p)
    ) == 0
    assert sp.simplify(
        sp.diff(F, p)-rho*kap*sp.exp(kap*p)
    ) == 0
    assert sp.simplify(
        1-4*p*sp.diff(kap*p, p)-(1-4*kap*p)
    ) == 0

    lam = sp.symbols("lam", positive=True)
    even = -lam*p*p

    assert sp.diff(even, p).subs(p, 0) == 0
    assert sp.diff(even, p, 2) == -2*lam
    assert sp.simplify(
        sp.diff(sp.exp(even), p, 2).subs(p, 0)+2*lam
    ) == 0
    assert sp.simplify(
        1-4*p*sp.diff(even, p)-(1+8*lam*p*p)
    ) == 0

    # Canonical quadratic-mode Hamiltonian.
    adot, bdot, amag, bmode = sp.symbols(
        "adot bdot amag bmode", real=True
    )
    quad = sp.Rational(1, 4)*(
        adot**2+bdot**2-k**2*(amag**2+bmode**2)
        -chi*(b*adot+e*k*bmode)**2
    )

    momenta = [
        sp.diff(quad, adot),
        sp.diff(quad, bdot),
    ]
    ham = sp.expand(
        adot*momenta[0]+bdot*momenta[1]-quad
    )
    expected_ham = sp.Rational(1, 4)*(
        (1-chi*b*b)*adot**2+bdot**2
        +k*k*(amag**2+(1+chi*e*e)*bmode**2)
    )

    assert sp.simplify(ham-expected_ham) == 0
    assert sp.simplify(
        sp.diff(quad, adot, 2)-(1-chi*b*b)/2
    ) == 0
    assert sp.simplify(
        sp.diff(quad, bdot, 2)-sp.Rational(1, 2)
    ) == 0

    # For linear positive-density loading,
    # speed²-1 = chi*(E²+B²)/(1-chi*B²).
    difference = (
        (1+chi*e**2)/(1-chi*b**2)-1
    )
    assert sp.simplify(
        difference-chi*(e**2+b**2)/(1-chi*b*b)
    ) == 0

    return {
        "scoped_exact_identity_checks": 13,
        "dispersion":
            "(s^2-1)*((1-chi*B^2)*s^2-(1+chi*E^2))=0",
        "chi":
            "rho*exp(sigma)*(sigma_second+sigma_first^2)",
        "hamiltonian":
            "positive_in_selected_modes_only_if_K>0_and_G>0",
        "fixed_theta_bulk_cancellation": "VERIFIED",
        "full_gravitational_noether": "NOT_DERIVED",
    }


def integrate_mode(
    case: Background,
    k: float = 1.7,
    duration: float = 5.0,
) -> dict:
    """Independently evolve the exact quadratic Fourier mode.

    This is a constant-material-background polarization reduction,
    not B11-M6 or a physical source/spacecraft impulse.
    """
    if k <= 0 or duration <= 0:
        raise ValueError(
            "Positive Fourier wavenumber and duration required"
        )

    rec = characteristic(case)
    K = rec["electric_kinetic_coefficient"]
    G = rec["gradient_coefficient"]

    if K <= 0 or G <= 0:
        raise ValueError(
            "Refuse evolution of unhealthy quadratic background"
        )

    chi = rec["material_curvature_chi"]
    E = case.electric
    B = case.magnetic
    coupling = chi*E*B*k

    generator = np.array([
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [-k*k/K, 0, 0, coupling/K],
        [0, -k*k*G, -coupling, 0],
    ], dtype=float)

    eig = np.linalg.eigvals(generator)

    measured = sorted(
        abs(z.imag)/k
        for z in eig
        if z.imag > 1e-10
    )
    expected = sorted([
        1.0,
        rec["extraordinary_speed_over_physical_c"],
    ])

    if (
        len(measured) != 2
        or not np.allclose(
            measured, expected,
            rtol=2e-11, atol=2e-11
        )
    ):
        raise AssertionError(
            f"Independent generator mismatch: {measured} vs {expected}"
        )

    y0 = np.array([0.21, -0.14, 0.07, 0.12])

    def energy(y):
        a, b, va, vb = y
        return (
            K*va*va+vb*vb
            +k*k*(a*a+G*b*b)
        )/4

    sol = solve_ivp(
        lambda t, y: generator@y,
        (0, duration),
        y0,
        t_eval=np.linspace(0, duration, 129),
        method="DOP853",
        rtol=3e-11,
        atol=3e-13,
    )

    if not sol.success:
        raise RuntimeError("Fourier evolution failed")

    energies = np.asarray([
        energy(sol.y[:, i])
        for i in range(sol.y.shape[1])
    ])
    drift = float(
        np.max(np.abs(energies-energies[0]))
    )

    if drift > 2e-9:
        raise AssertionError(
            f"Quadratic energy not conserved: {drift}"
        )

    return {
        "case": case.label,
        "numeric_speeds_over_c": measured,
        "independent_analytic_speeds_over_c": expected,
        "initial_quadratic_energy_shape_units":
            float(energies[0]),
        "max_quadratic_energy_drift_shape_units": drift,
        "time_window_dimensionless": duration,
        "static_background_supported_by_full_source": "NO",
    }


def provenance(root: Path) -> dict:
    result = {}

    for name, (rel, expected) in HISTORIC.items():
        path = root/rel

        if not path.is_file():
            result[name] = {
                "status": "MISSING",
                "expected_sha256": expected,
            }
        else:
            actual = sha256(path.read_bytes()).hexdigest()
            result[name] = {
                "status":
                    "MATCH" if actual == expected
                    else "HASH_MISMATCH",
                "actual_sha256": actual,
                "expected_sha256": expected,
            }

    return result


def run(root: Path) -> dict:
    symbols = symbolic_checks()

    # Pre-registered controls, not an optimization search.
    cases = [
        Background("linear_mixed_weak", "linear",
                   .7, .45, .35, .8),
        Background("linear_electric_only", "linear",
                   .7, .45, .35, 0),
        Background("linear_magnetic_only", "linear",
                   .7, .45, 0, .8),
        Background("linear_zero_coupling", "linear",
                   .7, 0, .35, .8),
        Background("linear_no_matter", "linear",
                   0, .45, .35, .8),
        Background("linear_kinetic_failure", "linear",
                   2, 1, .15, 1),
        Background("linear_conformal_singular", "linear",
                   .01, 1, .5, .5),
        Background("linear_critical_kinetic", "linear",
                   1, 1, 0, 1),
        Background("even_negative_mixed", "even_negative",
                   .35, .4, .35, .8),
        Background("even_negative_zero_linear_response",
                   "even_negative", .35, .4, 0, .8),
        Background("even_negative_gradient_failure",
                   "even_negative", 1, 1, 2, .1),
        Background("even_positive_mixed", "even_positive",
                   .35, .4, .35, .8),
    ]

    results = {
        case.label: characteristic(case)
        for case in cases
    }

    assert results["linear_mixed_weak"]["verdict"] == (
        "RED_SUPERLUMINAL_RESTRICTED_DUST"
    )
    assert results["even_negative_mixed"]["verdict"] == (
        "PASS_SCOPED_SUBLUMINAL_NOT_FULL_MODEL"
    )

    dynamic_labels = (
        "linear_mixed_weak",
        "linear_zero_coupling",
        "even_negative_mixed",
    )

    dynamics = {
        label: integrate_mode(
            next(x for x in cases if x.label == label)
        )
        for label in dynamic_labels
    }

    history = provenance(root)
    passed = all(
        x["status"] == "MATCH"
        for x in history.values()
    )

    return {
        "branch": BRANCH,
        "frozen_branch":
            "ALPHA1_M5V_NO_REOPTIMIZATION",
        "historic_provenance": history,
        "exact_algebra": symbols,
        "pre_registered_12_case_characteristic_atlas":
            results,
        "independent_fourier_evolution": dynamics,
        "gates": {
            "P0_PRIOR_SOURCE_RESULTS":
                "PASS_ARCHIVAL_SHA" if passed
                else "UNRESOLVED",
            "P1_LINEAR_P_POSITIVE_DUST_CAUSALITY":
                "RED_SCOPED_SUPERLUMINAL_OR_KINETIC_FAILURE",
            "P1_LINEAR_P_PORTAL_GLOBALLY_CLOSED":
                "NO_FULL_MATTER_DYNAMICS_UNTESTED",
            "P1_EVEN_P_SQUARED_COMPARISON":
                "CONDITIONAL_SUBLUMINAL_NO_SOURCE_OR_FORCE",
            "P1_CONFORMAL_INVERTIBILITY":
                "SCREENED_NOT_FULL_METRIC_SOLVER",
            "P1_GAUSS_WARD_FULL_MATTER":
                "NOT_DERIVED",
            "P2_FINITE_MICROSCOPIC_SOURCE_EOM":
                "OPEN_PH2_FREE_SOURCE_CLOSED_ONLY",
            "P2_EARTH_ELASTIC_EOS_INTERFACE":
                "NOT_DERIVED",
            "P3_EARTH_DOWN_CRAFT_UP":
                "NOT_DERIVED",
            "P3_COMPLETE_FIELD_BOUNDARY_MOMENTUM":
                "NOT_DERIVED",
            "B11_M6_FULL_CAUSAL_LOADED_IMPULSE":
                "NOT_RUN",
            "B11_M6_ORIGINAL_STATIC_FAIL_REPRODUCTION":
                "NOT_RUN",
            "FIN_NEUTRAL_1G_1M":
                "NOT_CERTIFIED",
            "COMPLETE_LT10MJ":
                "NOT_CERTIFIED",
            "WHOLE_CRAFT_LIFT":
                "NOT_ESTABLISHED",
        },
        "verdict":
            "YELLOW_WITH_NEW_SCOPED_LINEAR_PORTAL_CAUSAL_OBSTRUCTION",
    }
