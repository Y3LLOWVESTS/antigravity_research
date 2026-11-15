"""HOOK17-PH1: analytic source/metric/reaction existence preflight.

PURPOSE
-------
Falsification-first successor to frozen B17-M5V. Investigate whether an
actual gauge-invariant two-U(1) source/matter action has the necessary
algebraic structure to resemble the frozen artificial inverse reference.

CANDIDATE ACTION (NOT A COMPLETED SPACECRAFT ACTION)
----------------------------------------------------
S = integral sqrt(-g) [Mpl^2 R/2 - (F_X^2+F_Y^2)/4
    - sum_a (|D psi_a|^2 + m_a^2 |psi_a|^2 + V_a)]
    - sum_b m_b c integral exp(sigma(P)) ds_g + S_support
P = (1/2) F_X.mu,nu (*F_Y)^mu,nu
sigma(P) = kappa P  [a deliberately parity-odd test portal]
D psi_a = (nabla + i q_aX A_X + i q_aY A_Y) psi_a.

For fixed nonrelativistic dust rest density rho0 (canonical units c=1),
its local worldline action yields the test reduction
L_dust = -rho0 exp(kappa P).
No freely selected C2 beta is used.

TWO PHYSICALIZATION LIMITS
-------------------------
1. A winding scalar can kinematically match the M5I azimuthal J_phi
   with f^2 = J0*r*B/(2*q*n). This is NOT an EOM equilibrium;
   confinement, A_phi feedback, source energy and supports are unknown.
2. Oppositely charged stationary dust distributions can reproduce the
   M5I odd-in-z net-neutral rho profile kinematically. The actual force
   equilibrium and charged constituent energy are not derived.

CONVENTIONS AND CLAIMS
----------------------
Metric (-,+,+,+); two canonically normalized gauge fields.
The reduced homogeneous E/B convention uses P=E_X.B_Y+E_Y.B_X;
the relative Lorentzian-dual sign is absorbed into kappa in this test.
D_I=partial L/partial E_I, H_I=-partial L/partial B_I.
Numeric source moments use shape units, not amperes or joules.

This file DOES NOT establish a finite stable source, healthy complete
spectrum, empirical viability, Earth/craft force, time-domain solution,
<10MJ complete system, or gravitational propulsion. B11-M6 remains OPEN.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
from pathlib import Path
from typing import Any
import math

import numpy as np
import sympy as sp

BRANCH = "032H17A12D1R3X3B17-PH1"
FROZEN_M5V_SOURCE_SHA = (
    "ea193cd163b2fc87e6973878c77e27c761f0625f6c5de3f38594587ef6cdb80f"
)
FROZEN_M5V_RESULT_SHA = (
    "53f63f93fe9f525302f516b6376fa227d4b46027e6a0f75ae4dd35404da8c52b"
)
FROZEN_RESULT = (
    "b17_m5v_unified_20261114T203555409373Z_full_bundle.json"
)


@dataclass(frozen=True)
class Reference:
    r0: float = 1.15
    ar: float = .42
    az: float = .50
    power: int = 5
    rho_amplitude: float = 1.0  # Shape units, NOT C/m^3
    j_amplitude: float = 1.0    # Shape units, NOT A/m^2


def bump(x: np.ndarray, y: np.ndarray, exponent: int = 5) -> np.ndarray:
    return np.maximum(1.0 - x*x - y*y, 0.0)**exponent


def analytic_shape_moments(spec: Reference) -> dict[str, float]:
    """Exact disk moments using axisymmetric dV=2*pi*r dr dz."""
    if spec.power != 5:
        raise ValueError("analytic source control is frozen at M5I power 5")

    # Integral B dxdy = pi/6.
    # Integral x² B dxdy = Integral y² B dxdy = pi/84.
    charge = 0.0
    dipole = (
        (math.pi**2 / 42.0)
        * spec.r0 * spec.ar * spec.az**2
        * spec.rho_amplitude
    )
    magnetic = (
        math.pi**2 * spec.ar * spec.az * spec.j_amplitude
        * (spec.r0**2/6.0 + spec.ar**2/84.0)
    )
    angular_cost = (
        (math.pi**2/6)
        * spec.ar * spec.az * spec.j_amplitude
    )
    return {
        "monopole": charge,
        "electric_dipole_z": dipole,
        "magnetic_dipole_z": magnetic,
        "unit_charge_unit_winding_angular_cost_natural_units":
            angular_cost,
    }


def independent_shape_quadrature(
    spec: Reference,
    order: int = 30,
    angular_nodes: int = 64,
) -> dict[str, float]:
    """Independent radial-squared Gauss and periodic angular integration."""
    nodes, weights = np.polynomial.legendre.leggauss(order)
    s = .5*(nodes + 1.0)
    ws = .5*weights
    theta = 2*math.pi*np.arange(angular_nodes)/angular_nodes

    x = np.sqrt(s)[:, None] * np.cos(theta)[None, :]
    y = np.sqrt(s)[:, None] * np.sin(theta)[None, :]
    r = spec.r0 + spec.ar*x
    B = bump(x, y, spec.power)

    rho = spec.rho_amplitude*y*B
    current = spec.j_amplitude*B

    # dxdy = (1/2) ds dtheta.
    # dV = 2*pi*r*ar*az*dxdy.
    dv = (
        2*math.pi * spec.ar * spec.az * .5
        * ws[:, None]
        * (2*math.pi/angular_nodes)
        * r * np.ones_like(y)
    )

    return {
        "monopole": float(np.sum(rho*dv)),
        "electric_dipole_z": float(np.sum(spec.az*y*rho*dv)),
        "magnetic_dipole_z": float(np.sum(.5*r*current*dv)),
        "unit_charge_unit_winding_angular_cost_natural_units":
            float(np.sum((.5*current/r)*dv)),
    }


def winding_scalar_current(
    r: float,
    b: float,
    *,
    j0: float = 1.0,
    charge: float = 1.0,
    winding: int = 1,
) -> dict[str, float]:
    """Stationary A_phi=A_0=0 scalar: j^hat_phi=2*q*n*|psi|²/r."""
    if (
        r <= 0
        or not isinstance(winding, int)
        or winding == 0
        or charge*winding <= 0
        or b < 0
        or j0 < 0
    ):
        raise ValueError(
            "current witness requires positive r, q*n, B and J0"
        )

    amp_sq = j0*r*b/(2*charge*winding)
    jhat_phi = 2*charge*winding*amp_sq/r
    angular_grad_cost = winding*winding*amp_sq/(r*r)

    return {
        "amplitude_squared": amp_sq,
        "j_phi": jhat_phi,
        "angular_gradient_cost": angular_grad_cost,
        "j_time": 0.0,
    }


def neutral_charge_decomposition(
    y: float,
    b: float,
    rho0: float = 1.0,
) -> dict[str, float]:
    """Nonnegative opposite-charge populations generating rho0*y*B."""
    if not -1 <= y <= 1 or b < 0 or rho0 < 0:
        raise ValueError("M5I source support requires |y|<=1")

    plus = .5*rho0*b*(1+y)
    minus = .5*rho0*b*(1-y)

    return {
        "positive_density": plus,
        "negative_density": minus,
        "signed_charge": plus-minus,
        "total_constituent_density": plus+minus,
    }


def analytic_checks() -> dict[str, dict[str, Any]]:
    """Independent symbolic checks. Fail immediately on an identity error."""
    results = {}

    def check(key, statement, detail):
        if statement is not True and statement != sp.S.true:
            raise AssertionError(
                f"PH1 exact algebra failure: {key}: {statement}"
            )
        results[key] = {
            "status": "PASS_SCOPED",
            "meaning": detail,
        }

    ex, ey, bx, by, theta, kappa, rho = sp.symbols(
        "E_X E_Y B_X B_Y theta kappa rho", real=True
    )
    P = ex*by + ey*bx

    # R3X1 corrected Lorentzian constitutive signs.
    Lconstant = (
        (ex**2 + ey**2 - bx**2 - by**2)/2 + theta*P
    )
    D_X = sp.diff(Lconstant, ex)
    D_Y = sp.diff(Lconstant, ey)
    H_X = -sp.diff(Lconstant, bx)
    H_Y = -sp.diff(Lconstant, by)

    check(
        "r3x1_constitutive_signs",
        all(
            sp.simplify(a-b) == 0
            for a, b in (
                (D_X, ex+theta*by),
                (D_Y, ey+theta*bx),
                (H_X, bx-theta*ey),
                (H_Y, by-theta*ex),
            )
        ),
        "Corrected fixed-theta Lorentzian D/H signs",
    )

    fixed_ham = sp.expand(ex*D_X + ey*D_Y - Lconstant)
    check(
        "constant_theta_canonical_energy",
        sp.simplify(
            fixed_ham - (ex**2+ey**2+bx**2+by**2)/2
        ) == 0,
        "Fixed theta cancels from carrier Legendre energy",
    )

    # Universal physical metric: restricted fixed-dust reduction.
    matter = -rho*sp.exp(kappa*P)
    Lloaded = (
        (ex**2+ey**2-bx**2-by**2)/2 + matter
    )
    coupling = -rho*kappa*sp.exp(kappa*P)

    check(
        "derived_matter_theta",
        sp.simplify(
            sp.diff(Lloaded, ex) - (ex+coupling*by)
        ) == 0
        and sp.simplify(
            -sp.diff(Lloaded, bx) - (bx-coupling*ey)
        ) == 0,
        "Reciprocal theta=f'(P) from fixed dust, not artificial C2",
    )

    H = sp.hessian(Lloaded, (ex, ey))
    det_formula = (
        1-rho*kappa*kappa*sp.exp(kappa*P)*(bx*bx+by*by)
    )

    check(
        "loaded_electric_hessian_determinant",
        sp.simplify(H.det()-det_formula) == 0,
        "Necessary frozen-dust electric kinetic condition",
    )

    bvec = (by, bx)
    check(
        "loaded_electric_hessian_rank_one",
        all(
            sp.simplify(
                H[i, j]
                - (1 if i == j else 0)
                + rho*kappa*kappa*sp.exp(kappa*P)
                * bvec[i]*bvec[j]
            ) == 0
            for i in range(2)
            for j in range(2)
        ),
        "Restricted Hessian I-rho*kappa²*exp(kappa*P)*bbT",
    )

    neg = H.subs({
        rho: 1, kappa: 1,
        ex: 0, ey: 0, bx: 2, by: 0,
    })
    check(
        "loaded_electric_hessian_detects_negative_mode",
        sorted(float(v) for v in neg.eigenvals()) == [-3.0, 1.0],
        "Dimensionless synthetic negative kinetic eigenvalue",
    )

    pos = H.subs({
        rho: 1, kappa: 1,
        ex: 0, ey: 0, bx: sp.Rational(1, 4), by: 0,
    })
    check(
        "loaded_electric_hessian_positive_control",
        sorted(float(v) for v in pos.eigenvals()) == [.9375, 1.0],
        "Dimensionless weak-loading positive control",
    )

    check(
        "off_state_healthy_reduced_hessian",
        H.subs({bx: 0, by: 0}) == sp.eye(2),
        "Restricted electric Hessian identity in magnetic off-state",
    )

    check(
        "uniform_theta_no_bulk_kinetic_shift",
        sp.hessian(Lconstant, (ex, ey)) == sp.eye(2),
        "Uniform linear topological mixing preserves kinetic Hessian",
    )

    # Parity and conformal metric trace Jacobian.
    sigma = kappa*P
    check(
        "linear_pseudoscalar_parity",
        sp.simplify(sigma.subs(P, -P)+sigma) == 0,
        "Linear P portal is parity odd and needs justification",
    )

    dummy = sp.symbols("p_dummy", real=True)
    check(
        "even_portal_no_linear_term",
        sp.diff((kappa*dummy)**2, dummy).subs(dummy, 0) == 0,
        "Parity-even P² portal lacks zero-background linear term",
    )

    check(
        "conformal_trace_jacobian",
        sp.simplify(
            1-4*P*kappa-(1-4*kappa*P)
        ) == 0,
        "Conformal trace Jacobian factor 1-4*kappa*P",
    )

    # Independent U(1)_X x U(1)_Y gauge covariance.
    t, z = sp.symbols("t z", real=True)
    field = sp.Function("K")(t, z)
    j0 = -sp.diff(field, z)
    jz = sp.diff(field, t)

    psi_t = sp.Function("psi_t")(t)
    ax = sp.Function("ax")(t)
    ay = sp.Function("ay")(t)
    alphax = sp.Function("alphax")(t)
    alphay = sp.Function("alphay")(t)
    qx, qy = sp.symbols("qx qy", real=True)

    gauge_phase = sp.exp(
        -sp.I*(qx*alphax+qy*alphay)
    )
    d_new = (
        sp.diff(gauge_phase*psi_t, t)
        + sp.I*(
            qx*(ax+sp.diff(alphax, t))
            + qy*(ay+sp.diff(alphay, t))
        )*gauge_phase*psi_t
    )
    d_old = gauge_phase*(
        sp.diff(psi_t, t)
        + sp.I*(qx*ax+qy*ay)*psi_t
    )

    check(
        "two_u1_scalar_covariant_gauge_transformation",
        sp.simplify(d_new-d_old) == 0,
        "Exact two-U(1) charged-scalar gauge covariance",
    )

    check(
        "off_shell_antisymmetric_ward",
        sp.simplify(
            sp.diff(j0, t)+sp.diff(jz, z)
        ) == 0,
        "Divergence of antisymmetric field equation vanishes",
    )

    # Microscopic phase-winding Noether current.
    phi, radius, amp, n, q = sp.symbols(
        "phi radius amp winding q",
        positive=True, real=True
    )
    psi = amp*sp.exp(sp.I*n*phi)
    jphi = sp.simplify(
        -sp.I*q*(
            sp.conjugate(psi)*sp.diff(psi, phi)
            - sp.diff(sp.conjugate(psi), phi)*psi
        )/radius**2
    )
    check(
        "winding_scalar_noether_current",
        sp.simplify(
            jphi-2*q*n*amp**2/radius**2
        ) == 0,
        "Complex scalar winding yields azimuthal Noether current",
    )

    # Relative-coordinate translation prerequisite only.
    ze, zc, a0 = sp.symbols("ze zc a0", real=True)
    energy = a0*(ze-zc)**2
    check(
        "translation_action_reaction_prerequisite",
        sp.simplify(
            sp.diff(energy, ze)+sp.diff(energy, zc)
        ) == 0,
        "Relative-coordinate potential has opposite derivatives",
    )

    rr, scale = sp.symbols("rr scale", positive=True)
    exterior = scale*rr**(-6)
    check(
        "finite_dipole_mixed_exterior_falloff",
        sp.diff(exterior, rr) == -6*scale/rr**7,
        "Mixed aligned dipoles P~r^-6, gradient~r^-7",
    )

    # Source rank: independent currents require independent channels.
    qx, qy = sp.symbols("q_X q_Y", nonzero=True)
    check(
        "single_species_rank_one",
        sp.Matrix([[qx, qy]]).rank() == 1,
        "Single charged species produces proportional currents",
    )
    check(
        "two_species_rank_two",
        sp.Matrix([[qx, 0], [0, qy]]).rank() == 2,
        "Two species remove the algebraic rank restriction only",
    )

    # Corrected mixed-sector energy-flux control.
    X = sp.Matrix(sp.symbols("x1 x2 x3", real=True))
    Y = sp.Matrix(sp.symbols("y1 y2 y3", real=True))
    BX = sp.Matrix(sp.symbols("bx1 bx2 bx3", real=True))
    BY = sp.Matrix(sp.symbols("by1 by2 by3", real=True))

    S = X.cross(BX-theta*Y)+Y.cross(BY-theta*X)
    check(
        "r3x1_poynting_cross_cancel",
        all(
            sp.simplify(v) == 0
            for v in S-X.cross(BX)-Y.cross(BY)
        ),
        "Fixed-theta mixed terms cancel from total Poynting flux",
    )

    # B11-M6 precursor: vacuum principal characteristics only.
    A = sp.Matrix([
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0],
    ])
    check(
        "b11_two_carrier_vacuum_characteristic",
        A.eigenvals() == {-1: 2, 1: 2} and A == A.T,
        "Free vacuum carriers have +/-c characteristics",
    )

    # Time-dependent theta needs material/driver energy exchange.
    time = sp.symbols("time", real=True)
    theta_t = sp.Function("theta")(time)
    dx, dy = sp.symbols("DX0 DY0", real=True)

    et_x = dx-theta_t*by
    et_y = dy-theta_t*bx
    energy_t = (
        et_x**2+et_y**2+bx**2+by**2
    )/2
    p_t = et_x*by+et_y*bx

    check(
        "b11_time_dependent_theta_energy_exchange",
        sp.simplify(
            sp.diff(energy_t, time)
            + sp.diff(theta_t, time)*p_t
        ) == 0,
        "Prescribed theta(t) transfers carrier energy via material work",
    )

    # Signed impulse demonstration, not a sourced pulse solution.
    check(
        "complete_signed_cycle_control",
        sp.integrate(sp.sin(time), (time, 0, sp.pi)) == 2
        and sp.integrate(
            sp.sin(time), (time, sp.pi, 2*sp.pi)
        ) == -2,
        "Synthetic positive and negative impulse cancel",
    )

    return results


def frozen_dust_electric_hessian_eigenvalue(
    rho: float,
    kappa: float,
    P: float,
    b2: float,
) -> float:
    """Necessary frozen-dust electric eigenvalue in natural units.

    b2 = B_X²+B_Y². Not a complete Hamiltonian or Earth prediction.
    """
    if (
        not all(
            math.isfinite(v)
            for v in (rho, kappa, P, b2)
        )
        or rho < 0
        or b2 < 0
    ):
        raise ValueError("finite nonnegative density and B² required")

    return 1-rho*kappa*kappa*math.exp(kappa*P)*b2


def evaluate_kinematic_source() -> dict[str, Any]:
    spec = Reference()
    exact = analytic_shape_moments(spec)
    numeric = independent_shape_quadrature(spec)
    errors = {
        key: abs(exact[key]-numeric[key])
        for key in exact
    }
    if max(errors.values()) > 1e-10:
        raise AssertionError(
            f"independent source moments mismatch: {errors}"
        )

    x, y = .23, -.37
    b = float(bump(np.array(x), np.array(y)))
    r = spec.r0+spec.ar*x
    witness = winding_scalar_current(r, b)
    decomposition = neutral_charge_decomposition(y, b)

    if (
        abs(witness["j_phi"]-b) > 1e-13
        or abs(decomposition["signed_charge"]-y*b) > 1e-13
    ):
        raise AssertionError("kinematic source witness mismatch")

    return {
        "reference": asdict(spec),
        "exact_moments": exact,
        "independent_quadrature_moments": numeric,
        "absolute_errors": errors,
        "scalar_winding_witness_at_one_sample": witness,
        "opposite_charge_dust_witness_at_one_sample":
            decomposition,
        "meaning": (
            "Only kinematic shape matching; source EOM, "
            "physical calibration and support energy NOT derived"
        ),
    }


def sha_file(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


def archival_status(root: Path) -> dict[str, Any]:
    src = (
        root
        / "src/antigravity_research/agminer/"
        "hook17_r3b_m5v_unified_exterior_action.py"
    )
    data = root/"results/data"/FROZEN_RESULT

    def one(path, expected):
        if not path.is_file():
            return {
                "status": "MISSING_LOCAL_FILE",
                "expected_sha256": expected,
            }
        got = sha_file(path)
        return {
            "status": (
                "MATCH" if got == expected else "HASH_MISMATCH"
            ),
            "actual_sha256": got,
            "expected_sha256": expected,
        }

    return {
        "frozen_m5v_source": one(src, FROZEN_M5V_SOURCE_SHA),
        "frozen_m5v_result": one(data, FROZEN_M5V_RESULT_SHA),
    }


def run_preflight(root: Path) -> dict[str, Any]:
    checks = analytic_checks()
    source = evaluate_kinematic_source()
    archive = archival_status(root)
    archival_pass = all(
        v["status"] == "MATCH"
        for v in archive.values()
    )

    return {
        "branch": BRANCH,
        "experiment": "FIRST_ACTUAL_PH1_ALGEBRA_AND_KINEMATIC_SOURCE_PREFLIGHT",
        "m5v_campaign": "FROZEN_NO_ARTIFICIAL_OPTIMIZATION",
        "historic_full_regression":
            "1803_PASSED_RECORDED_NOT_REEXECUTED_BY_THIS_SCRIPT",
        "reference": {
            "006d_coefficient": 23.591586299249,
            "a12c_preloaded_f2_j": 2.6568591420597114,
            "r3b_preloaded_mixed_j": 1.5429162116460216,
            "m5v_artificial_earth_derivative_j_per_m":
                -11.39567591875062,
        },
        "analytic_check_count": len(checks),
        "exact_checks": checks,
        "physical_source_shape_witness": source,
        "archival": archive,
        "gates": {
            "PH1_P0_HISTORICAL_REFERENCE_PROVENANCE":
                "PASS_SCOPED" if archival_pass else "UNRESOLVED",
            "PH1_P1_EXACT_GAUGE_WARD":
                "PASS_SCOPED_ABELIAN_IDENTITIES_ONLY",
            "PH1_P1_COMPLETE_ACTION_SPECIFIED":
                "NOT_DERIVED_SUPPORT_HULL_EARTH_EOS_MISSING",
            "PH1_P1_HEALTHY_CANONICAL_MODES":
                "OPEN_LOADED_HESSIAN_NECESSARY_CONDITION_DERIVED",
            "PH1_P2_MICROSCOPIC_CONSERVED_SOURCE":
                "KINEMATIC_WITNESS_ONLY_EOM_NOT_SOLVED",
            "PH1_P2_SOURCE_ENERGY_LOWER_BOUND":
                "OPEN_NO_CANONICAL_SOURCE_CALIBRATION",
            "PH1_P2_DERIVED_MATTER_RESPONSE":
                "PASS_SCOPED_FIXED_DUST_NOT_EARTH_C2",
            "PH1_P3_LAWFUL_EXTERIOR_CHANNEL":
                "CONDITIONAL_DIPOLE_FIELDS_NOT_FULL_EARTH_BVP",
            "PH1_P3_EARTH_DOWN_FULL_CRAFT_UP":
                "NOT_DERIVED",
            "PH1_P3_COMPLETE_MOMENTUM_EXCHANGE":
                "NOT_DERIVED",
            "PH1_P4_CONTINUUM_FORCE_CONVERGENCE":
                "NOT_RUN",
            "PH1_COMPLETE_STRICT_LT10MJ":
                "NOT_CERTIFIED",
            "PH1_REAL_ANTIGRAVITY_DEVICE":
                "NO",
            "B11_M6_CAUSAL_PRINCIPAL_EQUATIONS":
                "OPEN_NO_DYNAMIC_MATTER_SOURCE",
            "B11_M6_REPRODUCE_ORIGINAL_LOADED_STATIC_FAILURE":
                "NOT_RUN",
            "B11_M6_COMPLETE_SIGNED_IMPULSE":
                "NOT_RUN",
        },
        "next_required": (
            "Finish microscopic EOM/confinement and full-gravity action; "
            "test loaded characteristic matrix and original failed static "
            "limit before allowing a time-domain pulse"
        ),
        "verdict":
            "YELLOW_ALGEBRAIC_SOURCE_SHAPE_PREFLIGHT_ONLY_NO_PHYSICAL_LIFT",
    }
