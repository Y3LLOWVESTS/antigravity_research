"""B17-M5P boundary, variational, source and output controls."""

import json
import math
import sys

import numpy as np
import pytest

from antigravity_research.agminer import (
    hook17_r3b_m5p_exterior_boundary as m5p,
)
from antigravity_research.agminer import (
    hook17_r3b_m5o_fixed_box as m5o,
)


@pytest.mark.parametrize("sector", ("phi", "a"))
@pytest.mark.parametrize("side", ("r", "z"))
@pytest.mark.parametrize("z", (-7.0, 3.5))
def test_exact_dipole_trace_ratio(sector, side, z):
    r = 7.0

    if side == "r":
        ri, zi, rb, zb = r - 0.2, z, r, z
    else:
        ri, zi, rb, zb = (
            r,
            z + (-0.2 if z < 0 else 0.2),
            r,
            z,
        )

    def dipole(rr, zz):
        radius = math.hypot(rr, zz)
        numerator = zz if sector == "phi" else rr
        return numerator / radius**3

    actual = dipole(rb, zb) / dipole(ri, zi)
    calculated = m5p.dipole_trace_scale(
        ri, zi, rb, zb, sector
    )

    assert calculated == pytest.approx(
        actual, rel=1e-13
    )


@pytest.mark.parametrize("sector", ("phi", "a"))
@pytest.mark.parametrize("side", ("r", "z"))
def test_robin_alpha_against_dipole_derivative(
    sector, side
):
    r, z = 7.0, 3.0
    delta = 1e-5

    def dipole(rr, zz):
        numerator = zz if sector == "phi" else rr
        return numerator / (rr*rr + zz*zz)**1.5

    if side == "r":
        numerical = -(
            dipole(r + delta, z)
            - dipole(r - delta, z)
        ) / (
            2 * delta * dipole(r, z)
        )
    else:
        numerical = -(
            dipole(r, z + delta)
            - dipole(r, z - delta)
        ) / (
            2 * delta * dipole(r, z)
        )

    calculated = m5p.dipole_robin_alpha(
        r, z, side, sector
    )

    assert calculated == pytest.approx(
        numerical, abs=1e-10
    )


def test_dipole_trace_is_not_exact_for_quadrupole():
    ri, rb, z = 6.8, 7.0, 3.2

    def quadrupole(r, z):
        radius = math.hypot(r, z)
        return (2*z*z - r*r) / radius**5

    actual = (
        quadrupole(rb, z)
        / quadrupole(ri, z)
    )

    extrapolated = m5p.dipole_trace_scale(
        ri, z, rb, z, "phi"
    )

    assert abs(actual - extrapolated) > 1e-3


@pytest.mark.parametrize(
    "closure",
    ("dipole_robin", "dipole_trace"),
)
def test_boundary_modification_is_diagonal_only(
    closure
):
    field = m5o.mesh(
        0.25, m5p.BOUNDS["compact"]
    )

    original, _ = m5p.robin_operators(
        field, "dirichlet"
    )
    modified, audit = m5p.robin_operators(
        field, closure
    )

    assert (
        audit["elimination_min_denominator"]
        > 0.1
    )

    for key in ("k_phi", "k_a"):
        delta = (
            modified[key] - original[key]
        ).tocsr()

        assert np.max(
            np.abs(delta.diagonal())
        ) > 0

        delta.setdiag(0.0)
        delta.eliminate_zeros()

        assert delta.nnz == 0

    j0, _ = m5o.source_rhs(
        field, original, 0.0
    )
    j1, _ = m5o.source_rhs(
        field, modified, 0.0
    )

    np.testing.assert_array_equal(j0, j1)


def test_m5o_reproduction_and_m5p_action():
    old = m5o.evaluate(
        h=0.25,
        domain=m5p.BOUNDS["compact"],
        do_resolve=False,
    )
    new = m5p.evaluate(
        h=0.25,
        domain=m5p.BOUNDS["compact"],
        closure="dirichlet",
        do_resolve=True,
    )

    assert new["derivative_analytic_j_m"] == (
        pytest.approx(
            old["derivative_analytic_j_m"],
            abs=1e-10,
        )
    )

    dipole = m5p.evaluate(
        h=0.25,
        domain=m5p.BOUNDS["compact"],
        closure="dipole_trace",
        do_resolve=True,
    )

    assert (
        dipole["weighted_operator_asymmetry"]
        < 1e-10
    )
    assert (
        dipole["stationarity_residual"]
        < 1e-9
    )
    assert abs(
        dipole["derivative_H_difference_error_j_m"]
    ) < 0.001
    assert abs(
        dipole["derivative_resolve_difference_error_j_m"]
    ) < 0.001

    assert dipole["physical_force_certified"] is False


def test_negative_controls():
    for change in (
        {"earth_present": False},
        {"zero_source": True},
    ):
        case = m5p.evaluate(
            h=0.25,
            domain=m5p.BOUNDS["compact"],
            **change,
        )

        assert abs(
            case["derivative_analytic_j_m"]
        ) < 1e-12


def test_exterior_trace_exact_for_pure_dipoles():
    field = m5o.mesh(
        0.25, m5p.BOUNDS["outer21"]
    )
    ops, _ = m5p.robin_operators(
        field, "dirichlet"
    )

    nrp = ops["nr_phi"]
    nra = ops["nr_a"]
    nz = ops["nz_inner"]

    z = field["zs"][1:-1, None]
    rp = field["rhos"][None, :-1]
    ra = field["rhos"][None, 1:-1]

    radius_phi = np.hypot(rp, z)
    radius_a = np.hypot(ra, z)

    phi = np.divide(
        z,
        radius_phi**3,
        out=np.zeros((nz, nrp)),
        where=radius_phi > 0,
    )
    a = ra / radius_a**3

    u = np.r_[phi.ravel(), a.ravel()]

    audit = m5p.exterior_trace_probe(
        field,
        ops,
        u,
        ("compact", "original"),
    )

    for target in audit.values():
        for key, value in target.items():
            if "dipole_trace" in key:
                assert value < 1e-12


def test_single_file_writer(tmp_path, monkeypatch):
    jobs = [
        ("a", {"h": 0.2}),
        ("b", {"h": 0.1}),
    ]

    def fake_evaluate(**kwargs):
        return {
            "derivative_analytic_j_m": -kwargs["h"]
        }

    def fake_summary(*_):
        return {
            "gates": {
                "P0_m5o_dirichlet_reproduction": "PASS",
                "P1_stationarity_and_derivative": "PASS",
                "P1a_source_moments": "PASS",
                "P2_negative_controls": "PASS",
                "P3_domain_sensitivity_reduced": "PASS",
                "P4a_exterior_trace_reference": "PASS",
            }
        }

    monkeypatch.setattr(
        m5p, "_jobs", lambda mode: jobs
    )
    monkeypatch.setattr(
        m5p, "evaluate", fake_evaluate
    )
    monkeypatch.setattr(
        m5p, "_diagnose", fake_summary
    )
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "m5p",
            "--mode",
            "quick",
            "--results-dir",
            str(tmp_path),
        ],
    )

    assert m5p.main() == 0

    files = list(tmp_path.iterdir())
    assert len(files) == 1

    data = json.loads(
        files[0].read_text()
    )

    assert data["registered"] == 2
    assert data["processed"] == 2
    assert len(data["results"]) == 2
    assert data["status"] == (
        "COMPLETE_NUMERICAL_ONLY"
    )
    assert data["physical_claims"]["lift"] is False


def test_resume_without_repeating_cases(
    tmp_path, monkeypatch
):
    jobs = [
        ("a", {"h": 0.2}),
        ("b", {"h": 0.1}),
    ]
    calls = []

    def fake_evaluate(**kwargs):
        calls.append(kwargs["h"])
        return {
            "derivative_analytic_j_m": -kwargs["h"]
        }

    def fake_summary(*_):
        return {
            "gates": {
                "P0_m5o_dirichlet_reproduction": "PASS",
                "P1_stationarity_and_derivative": "PASS",
                "P1a_source_moments": "PASS",
                "P2_negative_controls": "PASS",
                "P3_domain_sensitivity_reduced": "PASS",
                "P4a_exterior_trace_reference": "PASS",
            }
        }

    monkeypatch.setattr(
        m5p, "_jobs", lambda mode: jobs
    )
    monkeypatch.setattr(
        m5p, "evaluate", fake_evaluate
    )
    monkeypatch.setattr(
        m5p, "_diagnose", fake_summary
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "m5p",
            "--mode",
            "quick",
            "--results-dir",
            str(tmp_path),
            "--max-new-cases",
            "1",
        ],
    )

    assert m5p.main() == 2

    bundles = list(
        tmp_path.glob("*.json")
    )
    assert len(bundles) == 1

    first = json.loads(
        bundles[0].read_text()
    )
    assert first["status"] == (
        "PARTIAL_CHECKPOINT_NOT_CERTIFIED"
    )
    assert list(first["results"]) == ["a"]

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "m5p",
            "--mode",
            "quick",
            "--resume",
            str(bundles[0]),
        ],
    )

    assert m5p.main() == 0
    assert calls == [0.2, 0.1]

    final = json.loads(
        bundles[0].read_text()
    )

    assert final["status"] == (
        "COMPLETE_NUMERICAL_ONLY"
    )
    assert list(final["results"]) == [
        "a", "b"
    ]
    assert len(list(tmp_path.iterdir())) == 1
