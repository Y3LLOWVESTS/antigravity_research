"""GAMMA1-00R12 L0 Hodge/metric and R11 fixed-charge audit.

Purpose: independently check necessary covariant variation identities and
fixed-Noether nonlocality against immutable PH16/R3/R11 evidence.
Model: signature (-+++), [0123]=+1; F_X=dA_X, F_Y=dA_Y.
Scope: not a complete Lorentzian parent, physical source, Einstein solution,
Earth/support action, stable modes, lift, SI operating energy or UV theory.
"""
from __future__ import annotations
import hashlib
import json
from itertools import permutations
from pathlib import Path

import numpy as np
import sympy as sp

PARENTS = {
    "PH16_R2": (
        "src/antigravity_research/ph16/ph16_04_joint_stationary.py",
        "b5468671f6418fad7b6ed01d916ea65a95a1d59252b84d4411beed9709f86df0"),
    "R3_native": (
        "results/data/gamma1_00r3_20261119T001454764826Z_native_12_L12.npz",
        "94d3763a8d7705ab3dc8774310cf3b8bba96557a0b80d2c34aa110d00b840d54"),
    "R11_source": (
        "src/antigravity_research/gamma1/gamma1_00r11_constrained_symbol.py",
        "f58d9f0a35baa1b0a53f491c6c5426d8603c371c0ec0a53f4fe352cc941f7378"),
    "R11_result": (
        "results/data/gamma1_00r11_20261119T074039011670Z.json",
        "ac7050c648959ee0daa21bed994d8cdc34abb261d08433f302d4362af163acef"),
    "R11_archive": (
        "results/data/gamma1_00r11_20261119T074039011670Z_Noether_Schur_12_L12.npz",
        "d5d0de1f5614be104d28c4fe51b157cb1f26815b905a14495791e7a049fa46fd"),
    "R11_verify": (
        "results/data/gamma1_00r11_verification_20261119T075421177672Z.json",
        "c9ff19031424c27a9da541f4aa0e0d064b158b2b16610d0f147e62eb5769d6ca"),
}

EPS = np.zeros((4, 4, 4, 4), dtype=int)
for perm in permutations(range(4)):
    EPS[perm] = (-1) ** sum(perm[i] > perm[j] for i in range(4)
                          for j in range(i + 1, 4))


def sha(path):
    """Return exact raw byte SHA256; missing inputs fail closed."""
    p = Path(path)
    return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else "MISSING"


def volume(g):
    """Return sqrt(-det g) for a real symmetric Lorentzian metric."""
    if not np.allclose(g, g.T) or np.sum(np.linalg.eigvalsh(g) < 0) != 1:
        raise ValueError("metric must be symmetric with signature -+++")
    return float(np.sqrt(-np.linalg.det(g)))


def wedge(F, G):
    """Independent wedge coefficient in positively oriented coordinates."""
    return float(F[0, 1]*G[2, 3] - F[0, 2]*G[1, 3]
                 + F[0, 3]*G[1, 2] + F[2, 3]*G[0, 1]
                 - F[1, 3]*G[0, 2] + F[1, 2]*G[0, 3])


def density(F, G):
    """Quarter-epsilon mixed field contraction; independent of metric."""
    return float(np.einsum("abcd,ab,cd->", EPS, F, G) / 4)


def pseudoscalar(F, G, g):
    return density(F, G) / volume(g)


def sigma(p):
    return .05 * p - 40 * p*p


def neutral_action(F, G, g, grad):
    """Scoped neutral scalar example, NOT Earth's physical matter model.

    Returns action density and background covariant-metric stress T_g^{mu nu}.
    The Hodge dependence of P is explicitly included in this stress.
    """
    p = pseudoscalar(F, G, g)
    s = sigma(p)
    ds = .05 - 80*p
    gt = np.exp(2*s)*g
    inv = np.linalg.inv(gt)
    L = .5 * grad @ inv @ grad + .5 * .9**2 * .6**2
    Tt = np.outer(inv @ grad, inv @ grad) - inv*L
    tr = float(np.sum(gt*Tt))
    Tg = np.exp(6*s)*Tt - np.exp(4*s)*ds*p*tr*np.linalg.inv(g)
    return float(-volume(gt)*L), Tg, tr


def metric_audit():
    """Covariant Hodge/metric identities vs independent centered differences."""
    F = np.array([[0, .03, -.02, .01],[-.03, 0, .04, .02],
                  [.02, -.04, 0, -.03],[-.01, -.02, .03, 0.]])
    G = np.array([[0, -.02, .01, .04],[.02, 0, -.01, .02],
                  [-.01, .01, 0, .015],[-.04, -.02, -.015, 0.]])
    g = np.array([[-1.2, .011, 0, 0],[.011, 1.1, .012, 0],
                  [0, .012, 1.3, .014],[0, 0, .014, .9]])
    dg = np.array([[.02, -.01, .01, 0],[-.01, -.04, 0, .005],
                   [.01, 0, .03, 0],[0, .005, 0, .01]])
    h = 2e-5
    grad = np.array([.4, -.1, .05, .2])
    p = pseudoscalar(F, G, g)
    _, Tg, trace = neutral_action(F, G, g, grad)
    dp = (pseudoscalar(F, G, g+h*dg)-pseudoscalar(F, G, g-h*dg))/(2*h)
    dS = (neutral_action(F, G, g+h*dg, grad)[0]
          - neutral_action(F, G, g-h*dg, grad)[0])/(2*h)
    errors = {
        "forms_tensor": abs(wedge(F, G)-density(F, G)),
        "density_metric_independence": abs(
            volume(g+h*dg)*pseudoscalar(F, G, g+h*dg)
            -volume(g-h*dg)*pseudoscalar(F, G, g-h*dg)),
        "P_cov_metric_derivative": abs(dp+.5*p*np.trace(np.linalg.solve(g, dg))),
        "matter_metric_stress_FD": abs(dS-.5*volume(g)*np.sum(Tg*dg)),
        "matter_stress_trace": abs(np.sum(g*Tg)-np.exp(4*sigma(p))
                                   *(1-4*p*(.05-80*p))*trace),
    }
    errors = {k: float(v) for k, v in errors.items()}
    if max(errors.values()) > 1e-8:
        raise AssertionError("METRIC_HODGE_FAILURE: " + str(errors))
    return errors


def gauge_jet():
    """Off-shell U(1) jet identity for one charged scalar kinetic term only."""
    a, q, f, fs, df, dfs, z, dz = sp.symbols("a q f fs df dfs z dz")
    L = -(dfs+sp.I*q*a*fs)*(df-sp.I*q*a*f)
    delta = {a: dz, f: sp.I*q*z*f, fs: -sp.I*q*z*fs,
             df: sp.I*q*(z*df+dz*f),
             dfs: -sp.I*q*(z*dfs+dz*fs)}
    variation = sp.expand(sum(sp.diff(L, v)*change
                              for v, change in delta.items()))
    if sp.simplify(variation) != 0:
        raise AssertionError("CHARGED_SCALAR_U1_OFFSHELL_JET_FAIL")
    return True


def check_parents(root):
    """Match raw parents and sidecars; do not repair or rewrite history."""
    root = Path(root)
    result = {}
    for label, (rel, expected) in PARENTS.items():
        path = root/rel
        actual = sha(path)
        if actual != expected:
            raise RuntimeError(f"{label}_HASH_DRIFT: {actual} != {expected}")
        if path.suffix in (".npz", ".json"):
            side = path.with_name(path.name+".sha256")
            if not side.is_file() or side.read_text().strip() != expected+"  "+path.name:
                raise RuntimeError(f"{label}_SIDECAR_DRIFT")
        result[label] = {"path": rel, "sha256": actual}
    old = json.loads((root/PARENTS["R11_result"][0]).read_text())
    if old.get("classification") != (
        "PASS_RANK_TWO_NONLOCAL_NOETHER_HESSIAN_"
        "AND_CONDITIONAL_FROZEN_U1_SYMBOL"
    ) or old.get("GAMMA1_01_authorized") is not False:
        raise RuntimeError("R11_SCIENTIFIC_CONTRACT_DRIFT")
    return result


def r11_reclose(root):
    """Independently rebuild R11's nonlocal fixed-N Schur term (not dynamics)."""
    from antigravity_research.ph16.ph16_04_joint_stationary import (
        CoulombSource, Spec, JointAction, Settings)
    with np.load(Path(root)/PARENTS["R3_native"][0], allow_pickle=False) as z:
        f = np.stack((z["F_plus"], z["F_minus"]))
        a = z["A_X"].copy()
        p = z["P"].copy()
    model = CoulombSource(Spec(nr=12, L=12.), self_order=8)
    j = JointAction(model, Settings(nr=12, L=12.))
    w, f2 = j.w, f*f
    e2 = np.exp(2*sigma(p))
    I = f2@(w*e2)
    freq = (model.s.N/2 + j.q*np.sum(f2*(w*e2*a)[None, :], axis=1))/I
    C = -4*f2*(freq[:, None]-j.q[:, None]*a[None, :])*(w*e2*(.05-80*p))[None, :]
    H = C.T@(C/(2*I[:, None]))
    with np.load(Path(root)/PARENTS["R11_archive"][0], allow_pickle=False) as z:
        target = z["rank_two_Schur_correction"]
        error = float(np.max(abs(H-target)))
    # Two nonzero singular values are more efficiently checked through 2x2 Gram.
    B = C/np.sqrt(2*I[:, None])
    eig2 = np.linalg.eigvalsh(B@B.T)[::-1]
    off = float(np.max(abs(H-np.diag(np.diag(H)))))
    shifted = p.copy()
    shifted[11] += .002
    shifted[35] -= .003
    e_new = np.exp(2*sigma(shifted))
    Inew = f2@(w*e_new)
    newfreq = (model.s.N/2 + j.q*np.sum(f2*(w*e_new*a)[None, :], axis=1))/Inew
    numbers = 2*np.sum(f2*(newfreq[:, None]-j.q[:, None]*a[None, :])
                       *(w*e_new)[None, :], axis=1)
    charge_error = float(np.max(abs(numbers-model.s.N)))
    if not (min(I)>0 and error<1e-10 and eig2[1]>1e-9
            and off>.05 and charge_error<1e-9):
        raise AssertionError("R11_FIXED_CHARGE_SCHUR_DRIFT")
    return {"rank": 2, "archive_max_error": error,
            "singular_values": [float(v) for v in eig2],
            "nonlocal_offdiag_max": off, "charge_reclosure_error": charge_error}


def negative_controls():
    """All booleans become Python bool, never silently skip np.bool_."""
    g = np.diag([-1., 1., 1., 1.])
    f = np.zeros((4, 4))
    h = f.copy()
    f[0, 1], f[1, 0] = 1., -1.
    h[2, 3], h[3, 2] = 2., -2.
    return {
        "X_off_P_zero": bool(pseudoscalar(np.zeros_like(f), h, g)==0),
        "Y_off_P_zero": bool(pseudoscalar(f, np.zeros_like(h), g)==0),
        "symmetric_tensor_null": bool(abs(density(f+np.eye(4), h)-density(f, h))<1e-14),
        "coupling_off_null": bool(0.*pseudoscalar(f, h, g)==0),
        "orientation_correct": bool(pseudoscalar(f, h, g)==2.),
    }


def science(root):
    p = check_parents(root)
    errors = metric_audit()
    ward = gauge_jet()
    rank = r11_reclose(root)
    controls = negative_controls()
    if not all(controls.values()):
        raise AssertionError("NEGATIVE_CONTROL_FAIL: " + str(controls))
    return {
        "parents": p,
        "hodge_metric_errors": errors,
        "scalar_U1_offshell_jet": ward,
        "r11_fixed_N": rank,
        "negative_controls": controls,
        "conditional_controls": {
            "constant_multiplier_topological_bulk_null": "CONDITIONAL_dF_EQUALS_ZERO",
            "PH14_spherical_Y_null": "HISTORICAL_NOT_REEXECUTED",
            "R2_static_invisible_operator": "GAUGE_INVARIANT_TERM_CHANGES_DYNAMICS_NOT_TESTED_HEALTHY"},
        "classification": "INSUFFICIENT_UNIQUE_COVARIANT_ACTION",
        "gates": {
            "METRIC_HODGE_DERIVED": "PASS_SCOPED",
            "FIXED_N_RECOVERED": "PASS_SCOPED",
            "ONE_SCALAR_OFFSHELL_U1": "PASS_SCOPED",
            "COMPLETE_ACTION": "NOT_DERIVED",
            "FULL_WARD_NOETHER_BIANCHI": "NOT_DERIVED",
            "HEALTHY_CONSTRAINED_LORENTZIAN": "NOT_CERTIFIED",
            "SOURCE_TO_EINSTEIN_EXTERIOR": "NOT_DERIVED",
            "EARTH_CRAFT_FORCE": "NOT_DERIVED",
            "SI_EMPIRICAL_UV_ENERGY": "NOT_CERTIFIED"},
        "missing": [
            "full PH16 Green / continuum Maxwell matching",
            "same-action charged source and fluid current variations",
            "Einstein/Hodge/metric and boundary terms",
            "Earth, hull and support offshell EOM/interface stress",
            "complete gauge/Noether/Bianchi Ward exchange",
            "full constrained scalar/fluid/gauge/gravity spectrum",
            "retarded physical exterior and finite neutral target",
            "Earth-down/whole-craft-up reaction and momentum ledger",
            "SI normalization, empirical/UV and conservative energy"],
        "Earth_down": "NOT_DERIVED",
        "whole_craft_up": "NOT_DERIVED",
        "complete_energy": "ENERGY_UNDETERMINED",
        "full_Lorentzian_health": "NOT_CERTIFIED",
        "GAMMA1_01_authorized": False,
        "PH16_05_authorized": False,
        "PH17_authorized": False,
        "006D_replaced": False,
        "qualified_gravity_bridge_survivors": [],
    }
