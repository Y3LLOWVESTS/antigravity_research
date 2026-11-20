"""GAMMA1 post-R12 D0: M0 local proxy-action variational preflight.

A testable charged-source / X / Y / neutral scalar proxy subsector.
Not PH16 stationary matching, real Earth/support/fluid matter, full
Lorentzian Einstein gravity, or a physical antigravity certificate.
"""
from __future__ import annotations

from itertools import permutations
from pathlib import Path
import hashlib
import json

import numpy as np
import sympy as sp

EPS = np.zeros((4, 4, 4, 4), dtype=int)
for perm in permutations(range(4)):
    EPS[perm] = (-1) ** sum(
        perm[i] > perm[j]
        for i in range(4)
        for j in range(i + 1, 4)
    )

PARENTS = {
    "R12_science": (
        "results/data/gamma1_00r12_20261119T201141220587Z.json",
        "7ebddf22bd718dc9729b1d63cb72943d75e379c12ce68420399edaafcf99bad6",
    ),
    "R12_verification": (
        "results/data/gamma1_00r12_verification_20261119T202521821183Z.json",
        "583ffee14d177af47628d2759a5b61a124f7ec968e83de7cad430b4575860b92",
    ),
    "R11_science": (
        "results/data/gamma1_00r11_20261119T074039011670Z.json",
        "ac7050c648959ee0daa21bed994d8cdc34abb261d08433f302d4362af163acef",
    ),
    "PH16_R2_source": (
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
    result = {}
    for name, (rel, expected) in PARENTS.items():
        p = Path(root) / rel
        actual = sha(p)
        if actual != expected:
            raise RuntimeError(
                f"{name}_HASH_DRIFT:{actual}"
            )
        if p.suffix == ".json":
            sidecar = p.with_name(p.name + ".sha256")
            if not sidecar.is_file() or (
                sidecar.read_text().strip()
                != expected + "  " + p.name
            ):
                raise RuntimeError(
                    name + "_SIDECAR_DRIFT"
                )
        result[name] = {
            "path": rel,
            "sha256": actual,
        }

    original = json.loads(
        (Path(root) / PARENTS["R12_science"][0]).read_text()
    )
    assert original["classification"] == (
        "INSUFFICIENT_UNIQUE_COVARIANT_ACTION"
    )
    assert original["GAMMA1_01_authorized"] is False
    return result


def specimen():
    """Fixed off-shell jets, not an actual sourced spacetime solution."""
    g = np.array([
        [-1.14, .02, 0, 0],
        [.02, 1.2, .03, 0],
        [0, .03, 1.1, .01],
        [0, 0, .01, .9],
    ])
    fx = np.array([
        [0, .03, -.01, .02],
        [-.03, 0, .01, -.015],
        [.01, -.01, 0, .018],
        [-.02, .015, -.018, 0],
    ])
    fy = np.array([
        [0, -.025, .02, .013],
        [.025, 0, .011, -.022],
        [-.02, -.011, 0, .021],
        [-.013, .022, -.021, 0],
    ])
    ax = np.array([.1, -.03, .02, .04])
    psi = np.array([.45 + .11j, .36 - .08j])
    dpsi = np.array([
        [.08 + .02j, .01 + .03j, -.02 + .01j, .02 - .02j],
        [.07 - .01j, .03 - .02j, .02 + .01j, -.01 + .03j],
    ])
    chi = np.array([.12, -.16, .21])
    dchi = np.array([
        [.06, .01, .03, -.01],
        [.04, -.02, .01, .03],
        [.03, .02, -.02, .04],
    ])
    return {
        "g": g, "FX": fx, "FY": fy, "AX": ax,
        "psi": psi, "dpsi": dpsi,
        "q": np.array([.05, -.05]),
        "chi": chi, "dchi": dchi,
    }


def action(z, alpha=.05, beta=40.):
    """One local algebraic action density with universal scalar proxies.

    Source species: two charged complex scalars, q=+/-0.05.
    Neutral species: three REAL scalar proxies. The latter are not
    a genuine neutral fluid, Earth model, or elastic support.
    """
    g = z["g"]
    gi = np.linalg.inv(g)
    volume = float(np.sqrt(-np.linalg.det(g)))
    fx, fy = z["FX"], z["FY"]

    p = float(
        np.einsum("abcd,ab,cd->", EPS, fx, fy)
        / (4 * volume)
    )
    sig = alpha*p - beta*p*p
    ds = alpha - 2*beta*p
    e2 = np.exp(2*sig)
    e4 = e2*e2

    D = (
        z["dpsi"]
        - 1j*z["q"][:, None]
        * z["AX"][None, :]
        * z["psi"][:, None]
    )

    kcharged = np.real(
        np.einsum("sa,ab,sb->", D.conj(), gi, D)
    )
    kneutral = .5*np.einsum(
        "sa,ab,sb->", z["dchi"], gi, z["dchi"]
    )
    K = float(kcharged + kneutral)

    amplitude = np.abs(z["psi"])**2
    source_U = np.sum(
        np.array([1., 1.08])**2 * amplitude
        - 2*amplitude**2 + 2*amplitude**3
    )
    neutral_U = .5*np.sum(
        np.array([.6, .7, .8])**2*z["chi"]**2
    )
    U = float(source_U + neutral_U)

    matter_L = -volume*(e2*K + e4*U)
    field_L = -volume/4*(
        np.sum(fx*(gi@fx@gi))
        + np.sum(fy*(gi@fy@gi))
    )
    total_L = float(matter_L + field_L)

    # Derivative (1/volume) * d matter_L / dP.
    lam = float(-(2*e2*K + 4*e4*U)*ds)

    gtinv = np.exp(-2*sig)*gi
    Draised = np.einsum("ab,sb->sa", gtinv, D)
    chraised = np.einsum(
        "ab,sb->sa", gtinv, z["dchi"]
    )

    Ttilde = (
        2*np.real(
            np.einsum("sa,sb->ab", Draised.conj(), Draised)
        )
        + np.einsum("sa,sb->ab", chraised, chraised)
        - gtinv*(np.exp(-2*sig)*K + U)
    )
    trace = float(
        np.sum(np.exp(2*sig)*g*Ttilde)
    )

    Tg = (
        np.exp(6*sig)*Ttilde
        - e4*ds*p*trace*gi
    )

    # Functional derivative of matter L with respect to AX_mu.
    # The sign of the Maxwell source in the EOM is the opposite.
    j = 2*volume*e2*np.sum(
        z["q"][:, None]
        * np.imag(
            z["psi"].conj()[:, None]
            * np.einsum("ab,sb->sa", gi, D)
        ),
        axis=0,
    )

    return {
        "P": p, "L": total_L, "Lm": float(matter_L),
        "lambda": lam, "K": K, "U": U,
        "Tg": Tg, "trace": trace, "j": j,
        "volume": volume, "gi": gi,
    }


def perturb(z, name, index, amount):
    result = {
        k: v.copy() if isinstance(v, np.ndarray) else v
        for k, v in z.items()
    }
    if name in ("FX", "FY"):
        i, j = index
        result[name][i, j] += amount
        result[name][j, i] -= amount
    elif name == "g":
        result[name] += amount*index
    else:
        result[name][index] += amount
    return result


def variational_checks():
    z = specimen()
    c = action(z)
    h = 1e-5
    errors = {}

    dg = np.array([
        [.02, -.01, 0, 0],
        [-.01, .03, .02, 0],
        [0, .02, -.01, .015],
        [0, 0, .015, .025],
    ])

    numeric = (
        action(perturb(z, "g", dg, h))["Lm"]
        - action(perturb(z, "g", dg, -h))["Lm"]
    )/(2*h)

    expected = (
        .5*c["volume"]*np.sum(c["Tg"]*dg)
    )
    errors["metric_stress"] = abs(numeric-expected)

    for name, pair in (("FX", (0, 1)), ("FY", (2, 3))):
        a, b = pair
        other = z["FY"] if name == "FX" else z["FX"]

        # Variation of an independent antisymmetric field component.
        epsilon_other = .5*np.einsum(
            "cd,cd->", EPS[a, b], other
        )
        predicted_matter = c["lambda"]*epsilon_other

        numerical_matter = (
            action(perturb(z, name, pair, h))["Lm"]
            - action(perturb(z, name, pair, -h))["Lm"]
        )/(2*h)

        predicted_total = (
            predicted_matter
            - c["volume"]*(c["gi"]@z[name]@c["gi"])[a, b]
        )
        numerical_total = (
            action(perturb(z, name, pair, h))["L"]
            - action(perturb(z, name, pair, -h))["L"]
        )/(2*h)

        errors[name+"_matter_variation"] = abs(
            numerical_matter-predicted_matter
        )
        errors[name+"_total_variation"] = abs(
            numerical_total-predicted_total
        )

    for index in range(4):
        measured = (
            action(perturb(z, "AX", index, h))["Lm"]
            - action(perturb(z, "AX", index, -h))["Lm"]
        )/(2*h)
        errors[f"source_current_{index}"] = abs(
            measured-c["j"][index]
        )

    sig = .05*c["P"] - 40*c["P"]**2
    ds = .05 - 80*c["P"]
    errors["matter_trace_lambda"] = abs(
        c["lambda"] - np.exp(4*sig)*ds*c["trace"]
    )

    errors = {
        k: float(v) for k, v in errors.items()
    }
    if max(errors.values()) >= 1e-8:
        raise AssertionError(
            "LOCAL_VARIATIONAL_IDENTITY_FAILED: " + str(errors)
        )
    return errors, c


def exact_gauge_and_bianchi():
    """Scalar off-shell U(1) jet plus exact dF=0 for each carrier."""
    q, theta, dtheta, A, x, y, dx, dy = sp.symbols(
        "q theta dtheta A x y dx dy", real=True
    )

    Dr = dx + q*A*y
    Di = dy - q*A*x
    K = Dr**2 + Di**2

    change = {
        x: -q*theta*y,
        y: q*theta*x,
        dx: -q*(theta*dy+dtheta*y),
        dy: q*(theta*dx+dtheta*x),
        A: dtheta,
    }
    variation = sp.expand(
        sum(sp.diff(K, variable)*delta
            for variable, delta in change.items())
    )
    if sp.simplify(variation) != 0:
        raise AssertionError("SOURCE_U1_JET_WARD_FAIL")

    # Symmetry of partial derivatives proves the two Abelian Bianchi
    # identities and the constant mixed-multiplier bulk null.
    second = {
        (i, j, a): sp.Symbol(f"h{i}{j}{a}")
        for i in range(4)
        for j in range(i, 4)
        for a in range(4)
    }
    def dd(mu, nu, a):
        return second[min(mu, nu), max(mu, nu), a]

    for nu in range(4):
        expression = sum(
            int(EPS[mu, nu, r, s])
            * (dd(mu, r, s)-dd(mu, s, r))
            for mu in range(4)
            for r in range(4)
            for s in range(4)
        )
        if sp.simplify(expression) != 0:
            raise AssertionError("ABELIAN_BIANCHI_FAIL")
    return True


def negative_controls():
    z = specimen()
    original = action(z)

    yzero = specimen()
    yzero["FY"][:] = 0
    xzero = specimen()
    xzero["FX"][:] = 0

    ay = action(yzero)
    ax = action(xzero)

    epsilon_x = .5*np.einsum(
        "cd,cd->", EPS[2, 3], z["FX"]
    )
    first_order_y = ay["lambda"]*epsilon_x

    controls = {
        "X_OFF_P_ZERO": bool(ax["P"] == 0),
        "Y_OFF_P_ZERO": bool(ay["P"] == 0),
        "PORTAL_COUPLING_OFF_LAMBDA_ZERO": bool(
            action(z, alpha=0, beta=0)["lambda"] == 0
        ),
        "ALPHA_ZERO_Y_LINEAR_SOURCE_NULL": bool(
            action(yzero, alpha=0, beta=40)["lambda"] == 0
        ),
        "Y_ZERO_DOES_NOT_FORCE_Y_EULER_NULL": bool(
            abs(first_order_y) > 1e-8
        ),
        "SYMMETRIC_FIELD_NULL": bool(abs(
            np.einsum(
                "abcd,ab,cd->",
                EPS, z["FX"]+np.eye(4), z["FY"]
            )/4 - original["P"]*original["volume"]
        ) < 1e-12),
    }

    if not all(controls.values()):
        raise AssertionError(
            "NEGATIVE_CONTROL_FAILED: " + str(controls)
        )
    return controls, float(first_order_y)


def science(root):
    parent = parents(root)
    errors, c = variational_checks()

    if exact_gauge_and_bianchi() is not True:
        raise AssertionError("WARD_IDENTITY_FAILED")

    controls, first_y = negative_controls()

    return {
        "parents": parent,
        "errors": errors,
        "off_shell_charged_U1_jet_and_Bianchi": "PASS_SCOPED",
        "charged_X_source_current_variation": "PASS_SCOPED",
        "both_carrier_variations": "PASS_SCOPED",
        "neutral_source_earth_support_proxies":
            "CANONICAL_SCALARS_NOT_REAL_FLUID_OR_SOLID",
        "portal_P": c["P"],
        "portal_lambda": c["lambda"],
        "negative_controls": controls,
        "Y_zero_portal_euler_derivative": first_y,
        "scientific_discriminant":
            "Y_FIELD_ZERO_DOES_NOT_IMPLY_Y_EOM_ZERO",
        "classification":
            "SCOPED_LOCAL_PROXY_ACTION_WARDS_PASS_"
            "PHYSICAL_BRIDGE_NOT_ESTABLISHED",
        "gates": {
            "LOCAL_PROXY_ACTION_SPECIFIED": "PASS_SCOPED",
            "TWO_CARRIER_VARIATIONS": "PASS_SCOPED",
            "CHARGED_CURRENT_AND_GAUGE_WARD": "PASS_SCOPED",
            "FULL_EARTH_SUPPORT_FLUID_GR_ACTION": "NOT_DERIVED",
            "PH16_R11_MATCHED_AS_STATIC_REDUCTION": "NOT_DERIVED",
            "FULL_LORENTZIAN_CONSTRAINED_HEALTH": "NOT_CERTIFIED",
            "TRUE_EXTERIOR_EINSTEIN_FORCE": "NOT_DERIVED",
            "SI_UV_EFT_ENERGY": "NOT_CERTIFIED",
        },
        "qualified_survivors": [],
        "GAMMA1_01_authorized": False,
        "PH16_05_authorized": False,
        "PH17_authorized": False,
        "006D_replaced": False,
        "whole_craft_up": "NOT_DERIVED",
        "complete_energy": "ENERGY_UNDETERMINED",
    }
