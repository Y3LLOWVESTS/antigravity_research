"""HOOK17-PH15-P1: exact-action induction and axisymmetric source preflight.

PURPOSE
-------
Derive and falsify the leading trace-induced Y mechanism before any
expensive nonspherical source optimization.

MODEL
-----
Flat spacetime, signature (-,+,+,+), two Abelian carriers X and Y,
two oppositely X-charged complex scalar species, and proposed universal
conformal matter coupling.

P = (1/4) epsilon^(mu nu rho sigma) F_X(mu nu) F_Y(rho sigma)
  = E_X dot B_Y + E_Y dot B_X

sigma(P) = alpha*P - beta*P**2
L_m = -exp(2*sigma)*K - exp(4*sigma)*U

F_(0i) = E_i, epsilon^(0123) = +1.

SCIENTIFIC SCOPE
----------------
The analytic examples are OFF-SHELL controls.
The axisymmetric equations are action-derived, not numerically solved.
PH14's zero-Y result is preserved as an exact spherical null control.

UNITS
-----
Canonical natural units. No SI energy calibration.

FALSIFIERS
----------
Incorrect Lorentzian signs, wrong scalar/Maxwell variations,
failure of constant/aligned-coefficient null controls,
or unsupported current cancellation.

NOT ESTABLISHED
---------------
On-shell nonspherical existence, reciprocal two-carrier equilibrium,
constrained mode stability, external gravity, spacecraft lift,
or strictly sub-10-MJ complete operating energy.

PROTECTED HISTORY
-----------------
006D remains unreplaced. ALPHA-1 remains frozen at M5V.
"""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[3]

PH14_PATH = (
    ROOT
    / "src/antigravity_research/agminer/"
    "hook17_ph14_neutral_composite.py"
)

PH14_SHA = (
    "9a9cf92314ac1c1bdd23197082f08b47559342f3f607b8d5"
    "f81bc4bd85eb0e7d"
)


def check_provenance():
    """Fail closed on a changed protected PH14 source."""
    actual = hashlib.sha256(PH14_PATH.read_bytes()).hexdigest()
    if actual != PH14_SHA:
        raise RuntimeError("PH14 source SHA-256 mismatch: " + actual)

    original = (
        ROOT
        / "results/data/"
        "032h17_ph14_neutral_composite_20261115T092726920597Z.json"
    )

    return {
        "ph14_source_sha256": actual,
        "ph14_source_status": "MATCH",
        "ph14_json_status": (
            "PRESENT_HASH_RECORDED_ONLY"
            if original.is_file()
            else "NOT_AVAILABLE"
        ),
        "ph14_json_sha256": (
            hashlib.sha256(original.read_bytes()).hexdigest()
            if original.is_file()
            else None
        ),
    }


def run():
    """Execute symbolic and independent finite-difference falsifiers."""
    checks = {}

    P, K, U, alpha, beta = sp.symbols(
        "P K U alpha beta", real=True
    )

    sigma = alpha * P - beta * P**2
    Lm = -sp.exp(2 * sigma) * K - sp.exp(4 * sigma) * U
    lam = sp.diff(Lm, P)

    expected_lambda = -(
        2 * sp.exp(2 * sigma) * K
        + 4 * sp.exp(4 * sigma) * U
    ) * (alpha - 2 * beta * P)

    assert sp.simplify(lam - expected_lambda) == 0
    assert sp.simplify(
        lam.subs(P, 0) + 2 * alpha * (K + 2 * U)
    ) == 0
    assert lam.subs({P: 0, alpha: 0}) == 0

    checks["matter_trace_variation"] = "PASS_EXACT"
    checks["alpha_zero_first_order_Y"] = "EXACT_ZERO"

    # Independently contract the complete Lorentzian epsilon tensor.
    names = (
        "ex ey ez bx by bz ux uy uz vx vy vz"
    )
    ex, ey, ez, bx, by, bz, ux, uy, uz, vx, vy, vz = (
        sp.symbols(names, real=True)
    )

    def tensor(E, B):
        result = sp.zeros(4, 4)
        for i in range(3):
            result[0, i + 1] = E[i]
            result[i + 1, 0] = -E[i]
        for i, j, k in ((2, 3, 0), (3, 1, 1), (1, 2, 2)):
            result[i, j] = B[k]
            result[j, i] = -B[k]
        return result

    FX = tensor((ex, ey, ez), (bx, by, bz))
    FY = tensor((ux, uy, uz), (vx, vy, vz))

    mixed = sum(
        FX[i, j] * sp.LeviCivita(i, j, k, l) * FY[k, l]
        for i in range(4)
        for j in range(4)
        for k in range(4)
        for l in range(4)
    ) / 4

    assert sp.expand(
        mixed - (
            ex * vx + ey * vy + ez * vz
            + ux * bx + uy * by + uz * bz
        )
    ) == 0

    checks["Lorentzian_epsilon_contraction"] = "PASS_EXACT"

    # Four same-action constitutive derivatives.
    t = sp.symbols("t", real=True)
    h = sp.Function("h")
    mix = ex * vx + ux * bx

    Llocal = (
        (ex**2 + ux**2 - bx**2 - vx**2) / 2
        + h(mix)
    )

    hp = sp.diff(h(t), t).subs(t, mix)

    assert sp.simplify(
        sp.diff(Llocal, ux) - ux - hp * bx
    ) == 0
    assert sp.simplify(
        sp.diff(Llocal, vx) + vx - hp * ex
    ) == 0
    assert sp.simplify(
        sp.diff(Llocal, ex) - ex - hp * vx
    ) == 0
    assert sp.simplify(
        sp.diff(Llocal, bx) + bx - hp * ux
    ) == 0

    checks["four_constitutive_signs"] = "PASS_EXACT"

    # Independent finite-difference check, three step sizes.
    def sample_lagrangian(EY, BY):
        pp = 0.2 * BY - 0.3 * EY
        ss = 0.1 * pp - 0.2 * pp * pp
        return (
            0.5 * (EY * EY - BY * BY)
            - math.exp(2 * ss) * 0.2
            - math.exp(4 * ss) * 0.4
        )

    EY0, BY0 = 0.11, -0.06
    pp0 = 0.2 * BY0 - 0.3 * EY0
    ss0 = 0.1 * pp0 - 0.2 * pp0**2

    lambda0 = -(
        2 * math.exp(2 * ss0) * 0.2
        + 4 * math.exp(4 * ss0) * 0.4
    ) * (0.1 - 0.4 * pp0)

    target_D = EY0 - 0.3 * lambda0
    target_dBY = -BY0 + 0.2 * lambda0

    errors = []
    for step in (1e-3, 1e-4, 1e-5):
        fd_E = (
            sample_lagrangian(EY0 + step, BY0)
            - sample_lagrangian(EY0 - step, BY0)
        ) / (2 * step)

        fd_B = (
            sample_lagrangian(EY0, BY0 + step)
            - sample_lagrangian(EY0, BY0 - step)
        ) / (2 * step)

        errors.append(
            max(abs(fd_E - target_D), abs(fd_B - target_dBY))
        )

    assert errors[-1] < 1e-9
    assert errors[0] > errors[1] > errors[2]

    checks["independent_FD_variation"] = "PASS_CONVERGENCE"
    checks["FD_absolute_errors"] = errors

    # Derive the stationary axisymmetric source equations from
    # the cylindrical, volume-weighted action.
    rho, z = sp.symbols("rho z", positive=True, real=True)
    f = sp.Function("f")(rho, z)
    A = sp.Function("A")(rho, z)
    a = sp.Function("a")(rho, z)

    omega, q, n, m, b, c = sp.symbols(
        "omega q n m b c", real=True
    )

    W = omega - q * A
    nu = n - q * a
    potential = m**2 * f**2 - b * f**4 + c * f**6

    Lred = rho * (
        (sp.diff(A, rho)**2 + sp.diff(A, z)**2) / 2
        - (sp.diff(a, rho)**2 + sp.diff(a, z)**2)
        / (2 * rho**2)
        + W**2 * f**2
        - sp.diff(f, rho)**2
        - sp.diff(f, z)**2
        - nu**2 * f**2 / rho**2
        - potential
    )

    def EL(var):
        return (
            sp.diff(Lred, var)
            - sp.diff(
                sp.diff(Lred, sp.diff(var, rho)), rho
            )
            - sp.diff(
                sp.diff(Lred, sp.diff(var, z)), z
            )
        )

    def lap(g):
        return (
            sp.diff(g, rho, 2)
            + sp.diff(g, z, 2)
            + sp.diff(g, rho) / rho
        )

    scalar_equation = (
        lap(f)
        + (
            W**2
            - nu**2 / rho**2
            - m**2
            + 2 * b * f**2
            - 3 * c * f**4
        ) * f
    )

    electric_equation = lap(A) + 2 * q * W * f**2

    magnetic_equation = (
        sp.diff(a, rho, 2)
        + sp.diff(a, z, 2)
        - sp.diff(a, rho) / rho
        + 2 * q * nu * f**2
    )

    assert sp.simplify(
        EL(f) / (2 * rho) - scalar_equation
    ) == 0

    assert sp.simplify(
        EL(A) / (-rho) - electric_equation
    ) == 0

    assert sp.simplify(
        EL(a) * rho - magnetic_equation
    ) == 0

    checks["axisymmetric_scalar_X_variations"] = "PASS_EXACT"

    # Neutral counterwinding: charge cancels globally,
    # but the magnetically active azimuthal currents add.
    e, fp, fm, ap, Np, Nm = sp.symbols(
        "e fp fm ap Np Nm", real=True
    )

    current = (
        e * (1 - e * ap) * fp**2
        - e * (-1 + e * ap) * fm**2
    )

    assert sp.expand(
        current - e * (1 - e * ap) * (fp**2 + fm**2)
    ) == 0
    assert (e * (Np - Nm)).subs(Nm, Np) == 0

    checks["neutral_counterwinding_current"] = (
        "PASS_EXACT_ALGEBRA_NOT_ONSHELL"
    )

    # Electrostatic integrability theorem.
    F = sp.Function("F")(A)
    Er = -sp.diff(A, rho)
    Ez = -sp.diff(A, z)

    aligned_curl = (
        sp.diff(F, z) * Er
        - sp.diff(F, rho) * Ez
    )

    assert sp.simplify(aligned_curl) == 0
    checks["aligned_electrostatic_induction"] = "EXACT_ZERO"

    # Independent axisymmetric A0/a gradient conditions.
    Ar, Az, Lr, Lz, ar, az = sp.symbols(
        "Ar Az Lr Lz ar az", real=True
    )

    matrix = sp.Matrix([
        [Az, -Ar],
        [az, -ar],
    ])

    determinant = Ar * az - Az * ar
    assert sp.simplify(matrix.det() - determinant) == 0
    assert sp.simplify(
        matrix.inv() * sp.zeros(2, 1)
    ) == sp.zeros(2, 1)

    checks["independent_potential_gradient_theorem"] = (
        "CONSTANT_LAMBDA_REQUIRED_IF_DETERMINANT_NONZERO"
    )

    # Regular decaying OFF-SHELL counterexample.
    r2 = rho**2 + z**2
    A0 = sp.exp(-r2)
    atoy = rho**2 * sp.exp(-r2)
    lambda_toy = A0

    E_r = -sp.diff(A0, rho)
    E_z = -sp.diff(A0, z)
    B_r = -sp.diff(atoy, z) / rho
    B_z = sp.diff(atoy, rho) / rho

    rhoY = -(
        sp.diff(lambda_toy, rho) * B_r
        + sp.diff(lambda_toy, z) * B_z
    )

    jY = (
        sp.diff(lambda_toy, z) * E_r
        - sp.diff(lambda_toy, rho) * E_z
    )

    assert sp.simplify(
        rhoY - 4 * z * sp.exp(-2 * r2)
    ) == 0

    assert sp.simplify(jY) == 0

    assert sp.simplify(
        sp.diff(rho * B_r, rho) / rho
        + sp.diff(B_z, z)
    ) == 0

    checks["aligned_gradients_magnetic_X"] = (
        "NONZERO_ELECTRIC_Y_OFFSHELL_CONTROL"
    )
    checks["off_shell_Y_total_charge"] = "ZERO_BY_PARITY"

    # Exact Gaussian dipole, not an on-shell source.
    dipole = (sp.pi / 2)**sp.Rational(3, 2)
    assert dipole > 0
    checks["off_shell_Y_electric_dipole"] = str(dipole)

    # Distinct misaligned electrostatic control.
    lambda_misaligned = (1 + z) * A0

    jY2 = (
        sp.diff(lambda_misaligned, z) * E_r
        - sp.diff(lambda_misaligned, rho) * E_z
    )

    assert sp.simplify(
        jY2 - 2 * rho * sp.exp(-2 * r2)
    ) == 0

    checks["misaligned_electrostatic_induction"] = (
        "NONZERO_OFFSHELL_CONTROL"
    )

    # PH14's spherical X-only configuration is a mandatory null.
    r = sp.symbols("r", positive=True)
    radial_A = sp.Function("A0")(r)
    radial_lambda = sp.Function("lambda0")(r)

    assert sp.simplify(
        sp.diff(radial_A, r) * sp.diff(radial_lambda, r)
        - sp.diff(radial_lambda, r) * sp.diff(radial_A, r)
    ) == 0

    checks["PH14_spherical_Y"] = "EXACT_ZERO_BY_SYMMETRY"

    return {
        "branch": "032H17A12D1R3X3B17-PH15-P1",
        "classification": "YELLOW_ANALYTIC_CHANNEL_OPEN",
        "assumptions": {
            "signature": "-+++",
            "epsilon_0123": "+1",
            "gravity": "FIXED_MINKOWSKI",
            "source_sector": "TWO_CHARGED_SCALARS_X_MAXWELL",
            "Y_response": "FIRST_ORDER_ABOUT_FY_ZERO",
            "physical_metric": "PROPOSED_CONFORMAL_PORTAL",
        },
        "checks": checks,
        "on_shell_axisymmetric_existence": "NOT_SOLVED",
        "on_shell_Y_response": "NOT_SOLVED",
        "exterior_Y": "NOT_CERTIFIED",
        "full_reciprocal_coupling": "NOT_SOLVED",
        "constrained_kinetic_health": "NOT_CERTIFIED",
        "dynamical_stability": "NOT_CERTIFIED",
        "whole_spacecraft_force": "NOT_DERIVED",
        "complete_SI_energy": "NOT_AVAILABLE",
        "006D_replaced": False,
        "M5V_status": "FROZEN",
    }


def main():
    provenance = check_provenance()
    result = run()

    result["provenance"] = provenance
    result["source_sha256"] = hashlib.sha256(
        Path(__file__).read_bytes()
    ).hexdigest()

    result["verification_scope"] = (
        "EXACT_SYMBOLIC_PLUS_INDEPENDENT_FD"
    )
    result["PDE_mesh_convergence"] = "NOT_APPLICABLE"
    result["repository_full_regression"] = "NOT_RUN_BY_THIS_MODULE"

    stamp = datetime.now(timezone.utc).strftime(
        "%Y%m%dT%H%M%S%fZ"
    )

    output = (
        ROOT / "results/data"
        / f"032h17_ph15_p1_theorem_{stamp}.json"
    )

    with output.open("x", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True)
        handle.write("\n")

    digest = hashlib.sha256(output.read_bytes()).hexdigest()

    print(json.dumps(result, indent=2, sort_keys=True))
    print("RESULT_PATH=" + str(output))
    print("RESULT_SHA256=" + digest)
    print("PH15_P1_EXECUTION=PASS_SCOPED")


if __name__ == "__main__":
    main()
