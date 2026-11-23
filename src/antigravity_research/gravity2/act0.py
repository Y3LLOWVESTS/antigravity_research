"""GRAVITY2-ACT0: R3C/PH16 same-action transfer preflight.

Exact source-expression/curvature theorem, not a physical source,
Einstein exterior, stability, payload lift, or SI energy certificate.
Historical sources are read-only and require SHA-256 provenance.
"""
from __future__ import annotations

import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import secrets
import sympy as sp

ROOT = Path(__file__).resolve().parents[3]

SOURCES = {
    'R3C': (
        'src/antigravity_research/agminer/'
        'hook17_fdual_f_loaded_payload_homotopy.py',
        'a0368a7163e1f392745fd47c7c2e79fd54adce5e666362e51dc5c980c87a0fee'
    ),
    'PH16': (
        'src/antigravity_research/ph16/'
        'ph16_04_joint_stationary.py',
        'b5468671f6418fad7b6ed01d916ea65a95a1d59252b84d4411beed9709f86df0'
    ),
}


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def assignment(node, name):
    found = [
        n.value for n in ast.walk(node)
        if isinstance(n, ast.Assign)
        and len(n.targets) == 1
        and isinstance(n.targets[0], ast.Name)
        and n.targets[0].id == name
    ]
    if len(found) != 1:
        raise RuntimeError('ACTION_EXPRESSION_NOT_UNIQUE:' + name)
    return ast.unparse(found[0])


def run():
    trees = {}

    for key, (rel, expected) in SOURCES.items():
        p = ROOT / rel
        if not p.is_file() or p.is_symlink() or sha(p) != expected:
            raise RuntimeError('SOURCE_SHA_HOLD:' + key)
        trees[key] = ast.parse(p.read_text())

    rfunc = next(
        n for n in trees['R3C'].body
        if isinstance(n, ast.FunctionDef)
        and n.name == '_state_diagnostics'
    )

    cls = next(
        n for n in trees['PH16'].body
        if isinstance(n, ast.ClassDef)
        and n.name == 'JointAction'
    )

    pfunc = next(
        n for n in cls.body
        if isinstance(n, ast.FunctionDef)
        and n.name == 'evaluate'
    )

    settings = next(
        n for n in trees['PH16'].body
        if isinstance(n, ast.ClassDef)
        and n.name == 'Settings'
    )

    vals = {
        n.target.id: ast.literal_eval(n.value)
        for n in settings.body
        if isinstance(n, ast.AnnAssign)
        and isinstance(n.target, ast.Name)
        and n.target.id in ('alpha', 'beta')
    }

    if vals != {'alpha': 0.05, 'beta': 40.0}:
        raise RuntimeError('PH16_PORTAL_DRIFT')

    rexp = assignment(rfunc, 'sigma')
    pexp = assignment(pfunc, 'sigma')

    d, P, s = sp.symbols('dot_eb P s', real=True)
    a, b = sp.symbols('alpha beta', real=True)

    r = sp.sympify(rexp, locals={'dot_eb': d})
    p = sp.sympify(
        pexp.replace('s.alpha', 'alpha').replace('s.beta', 'beta'),
        locals={'P': P, 'alpha': a, 'beta': b}
    )

    if not (
        sp.diff(r, d, 2) == 0
        and sp.diff(r, d) != 0
        and sp.simplify(sp.diff(p, P, 2) + 2*b) == 0
    ):
        raise RuntimeError('PORTAL_IDENTITY_DRIFT')

    curvature = sp.simplify(
        sp.diff(
            p.subs({P: s*d, a: sp.Rational(1, 20), b: 40}),
            d, 2
        ) - sp.diff(r, d, 2)
    )

    if sp.simplify(curvature + 80*s*s) != 0:
        raise RuntimeError('CURVATURE_PROOF_FAILED')

    controls = {
        'nonzero_rescaling': bool(curvature.subs(s, 1) != 0),
        'orientation_flip': bool(curvature.subs(s, -1) != 0),
        'zero_scale_trivial': bool(curvature.subs(s, 0) == 0),
        'beta_zero_curvature_only': bool(
            sp.diff(p.subs(b, 0), P, 2) == 0
        )
    }

    if not all(controls.values()):
        raise RuntimeError('NEGATIVE_CONTROL_FAILED')

    evidence = {
        'schema': 'gravity2.act0.science.v1',
        'classification': 'DIRECT_PORTAL_TRANSFER_OBSTRUCTED_SCOPED',
        'parents': {
            k: {'path': v[0], 'sha256': v[1]}
            for k, v in SOURCES.items()
        },
        'R3C_sigma_expression': rexp,
        'PH16_sigma_expression': pexp,
        'PH16_alpha': vals['alpha'],
        'PH16_beta': vals['beta'],
        'curvature_difference': str(curvature),
        'negative_controls': controls,
        'source_action_equivalence': 'NOT_PROVED',
        'constrained_loaded_Hessian_transfer': 'BLOCKED',
        'Earth_craft_force': 'NOT_DERIVED',
        'complete_SI_energy': 'NOT_CERTIFIED',
        'real_physical_maturity_increase': 'NOT_EARNED'
    }

    base = ROOT / 'results/gravity2/act0_runs'
    base.mkdir(parents=True, exist_ok=True)

    folder = base / (
        datetime.now(timezone.utc).strftime(
            'g2act0_%Y%m%dT%H%M%SZ_'
        ) + secrets.token_hex(4)
    )
    folder.mkdir(mode=0o700)

    out = folder / 'science.json'
    with out.open('x') as f:
        f.write(
            json.dumps(
                evidence, indent=2, sort_keys=True, allow_nan=False
            ) + '\n'
        )

    with (folder / 'science.json.sha256').open('x') as f:
        f.write(sha(out) + '  science.json\n')

    print('ACT0_RUN=' + folder.name)
    print('ACT0_CLASSIFICATION=' + evidence['classification'])
    print('CURVATURE_DIFFERENCE=' + str(curvature))
    print('SCIENCE_SHA256=' + sha(out))


if __name__ == '__main__':
    run()
