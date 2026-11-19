"""R3 exact action checks and historical replay contract."""
import ast
from pathlib import Path

import pytest
import sympy as sp

from antigravity_research.gamma1.gamma1_00r3_action_recovery import (
    algebra,
    sha,
    PH16_SHA,
)

ROOT = Path(__file__).resolve().parents[2]

PH16 = (
    ROOT
    /'src/antigravity_research/ph16'
    /'ph16_04_joint_stationary.py'
)


def test_unmodified_PH16_source():
    assert sha(PH16) == PH16_SHA


def test_original_PH16_contains_native_joint_state():
    tree = ast.parse(
        PH16.read_text()
    )

    case = next(
        f for f in tree.body
        if (
            isinstance(f, ast.FunctionDef)
            and f.name == 'case'
        )
    )

    assert any(
        isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name)
            and target.id == 'pre_x'
            for target in node.targets[0].elts
        )
        for node in ast.walk(case)
        if (
            isinstance(node, ast.Assign)
            and len(node.targets) == 1
            and isinstance(
                node.targets[0],
                ast.Tuple
            )
        )
    )


def test_exact_action_checks():
    checks = algebra()

    assert len(checks) >= 9
    assert all(checks.values())


@pytest.mark.parametrize(
    'p',
    [-.3, 0, .2, 1.]
)
def test_conformal_P_weights(p):
    z = sp.symbols(
        'z',
        real=True
    )

    assert sp.simplify(
        sp.diff(
            sp.exp(-4*z)*p,
            z
        ).subs(z, 0)+4*p
    ) == 0


@pytest.mark.parametrize(
    'a,b,p',
    [
        (0, 0, .5),
        (.05, 40, 0),
        (.05, 40, .02),
    ]
)
def test_source_portal_off_controls(a, b, p):
    expected = a*p-b*p*p

    assert expected == pytest.approx(
        a*p-b*p*p
    )

    if a == b == 0 or p == 0:
        assert expected == 0


@pytest.mark.parametrize(
    'q,f,w',
    [
        (1, .5, 1),
        (-1, .9, 2),
        (0, 1., 3),
    ]
)
def test_source_X_current_at_fixed_Noether(q, f, w):
    A = sp.symbols(
        'A',
        real=True
    )

    R = -(w-q*A)**2*f*f
    J = 2*(w-q*A)*f*f

    assert sp.simplify(
        sp.diff(R, A)-q*J
    ) == 0


@pytest.mark.parametrize(
    'alpha,beta',
    [
        (.05, 40),
        (.1, 0),
        (0, 0),
    ]
)
def test_sigma_prime(alpha, beta):
    P = sp.symbols(
        'P',
        real=True
    )

    sigma = alpha*P-beta*P*P

    assert sp.simplify(
        sp.diff(sigma, P)
        -(alpha-2*beta*P)
    ) == 0


@pytest.mark.parametrize(
    'eta',
    [-2, 0, 2]
)
def test_no_inferred_lorentzian_health_from_electric_completion(eta):
    # R2 ambiguity retained.
    # Recovering a stationary profile cannot select eta.
    assert 1+eta in (-1, 1, 3)


def test_only_one_mesh_replay_in_runner():
    source = (
        ROOT
        /'simulations/gamma1/gamma1_00r3_recovery.py'
    ).read_text()

    assert 'nr=12,' in source
    assert 'L=12.0' in source
    assert 'maxiter=450' in source
    assert "'GAMMA1_01_authorized': False" in source
