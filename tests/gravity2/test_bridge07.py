"""GRAVITY2-07 focused geometric, numerical and safety tests."""

import ast
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest

from antigravity_research.gravity2 import (
    bridge07_core as core,
    bridge07 as runner,
    bridge07_check as check,
)


def test_nonzero_2d_mixed_invariant():
    h, a, f = core.prescribed_background(15)

    x = np.arange(15)*h
    X, Z = np.meshgrid(x, x, indexing="ij")
    b = np.sin(X)*np.cos(2*Z)

    P, _, _, _ = core.source_parts(
        b, a, f, h
    )

    assert np.max(np.abs(P)) > 1e-2


def test_magnetic_bianchi():
    h, a, f = core.prescribed_background(15)
    b = a*f

    Bx = -core.dz(b, h)
    Bz = core.dx(b, h)

    assert np.max(
        abs(core.dx(Bx, h)+core.dz(Bz, h))
    ) < 1e-12


def test_nonlinear_y_solver():
    result, fields = core.solve(15)

    assert (
        result["equation_residual_relative"]
        < 1e-10
    )

    assert result["y_field_max_abs"] > 1e-5
    assert fields["a"].shape == (15, 15)


def test_portal_off():
    result, _ = core.solve(
        15, alpha=0, beta=0
    )

    assert result["y_field_max_abs"] == 0


def test_scope_restrictions():
    evidence, _ = core.scientific_run()

    assert (
        evidence["geometry"]
        == "2D_PERIODIC_FLAT_XZ_PATCH_NOT_FINITE_EXTERIOR"
    )

    assert evidence["physical_survivors"] == 0
    assert evidence["L2_authorized"] is False


def test_collinear_control():
    h, a, f = core.prescribed_background(15)

    aa = np.broadcast_to(
        a[:, 0, None], a.shape
    )

    ff = np.broadcast_to(
        f[:, 0, None], f.shape
    )

    zero = core.portal_force(
        np.zeros_like(a),
        aa, ff, h
    )

    assert np.max(abs(zero)) < 1e-12


def test_constant_coefficient_topological():
    h, a, f = core.prescribed_background(15)

    commutator = (
        core.dx(core.dz(a, h), h)
        -core.dz(core.dx(a, h), h)
    )

    assert np.max(abs(commutator)) < 1e-12


def test_same_action_gradient():
    _, fields = core.solve(15)

    error, signal = check.finite_difference_action(
        fields["a"],
        fields["f"],
        fields["b"],
        2*np.pi/15,
    )

    assert error < 1e-7
    assert signal > 1e-5


def test_four_grids():
    evidence, archive = core.scientific_run()

    assert tuple(
        row["n"]
        for row in evidence["rows"]
    ) == core.GRIDS

    assert all(
        row["equation_residual_relative"] < 1e-10
        for row in evidence["rows"]
    )


def test_dry_run(capsys):
    args = SimpleNamespace(
        level="L1",
        workers=1,
        preset="quick",
        minutes=.5,
        dry_run=True,
    )

    assert runner.run(args) == 0

    assert "2D_PORTAL_Y_EULER_ONLY" in (
        capsys.readouterr().out
    )


def test_l2_refused():
    with pytest.raises(ValueError):
        runner.run(SimpleNamespace(
            level="L2",
            workers=1,
            preset="quick",
            minutes=.5,
            dry_run=True,
        ))


def test_path_traversal_refused():
    with pytest.raises(ValueError):
        runner.owned("../agminer")


def test_no_legacy_miner_imports():
    for name in runner.SOURCE_FILES[:3]:
        tree = ast.parse(
            (runner.ROOT/name).read_text()
        )

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                assert all(
                    "agminer" not in item.name.lower()
                    for item in node.names
                )

            if (
                isinstance(node, ast.ImportFrom)
                and node.module
            ):
                assert (
                    "agminer"
                    not in node.module.lower()
                )
