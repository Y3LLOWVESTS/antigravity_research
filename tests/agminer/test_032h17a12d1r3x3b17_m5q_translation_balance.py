"""M5Q source translation and stationary variational checks."""
import json
import sys

import numpy as np
import pytest

from antigravity_research.agminer import (
    hook17_r3b_m5q_translation_balance as m,
)
from antigravity_research.agminer import (
    hook17_r3b_m5o_fixed_box as m5o,
)
from antigravity_research.agminer import (
    hook17_r3b_m5p_exterior_boundary as m5p,
)


@pytest.mark.parametrize(
    "h,order,phase",
    [
        (.25, 6, 0),
        (.2, 6, -.25),
        (.2, 6, 0),
        (.2, 6, .25),
        (.125, 4, .25),
        (.1, 6, .5),
        (.0625, 6, 0),
    ],
)
def test_analytic_deposition_derivative(h, order, phase):
    field = m5o.mesh(
        h, m5p.BOUNDS["compact"]
    )

    ops, _ = m5p.robin_operators(
        field, "dipole_trace"
    )

    shift = h*phase
    step = 1.e-4

    analytic, _ = m.analytic_source_translation(
        field, shift, order
    )

    plus, _ = m5o.source_rhs(
        field, ops, shift+step, order=order
    )

    minus, _ = m5o.source_rhs(
        field, ops, shift-step, order=order
    )

    finite = (plus-minus)/(2.*step)

    defect = (
        np.linalg.norm(analytic-finite)
        / max(np.linalg.norm(analytic), 1.)
    )

    assert defect < 5.e-6


@pytest.mark.parametrize(
    "closure",
    ("dirichlet", "dipole_robin", "dipole_trace"),
)
def test_stationary_partition_and_resolved_derivatives(closure):
    row = m.evaluate(
        h=.25,
        closure=closure,
        resolve=True,
    )

    terms = row["derivative_terms_j_m"]
    solved = row["on_shell_derivative_re_solved"]

    assert abs(
        terms["common_minus_earth_plus_craft"]
    ) < .002

    assert abs(
        terms["source_explicit_total"]
        - terms["source_explicit_scalar"]
        - terms["source_explicit_vector"]
    ) < 1.e-8

    assert abs(
        terms["source_explicit_scalar_raw"]
        + terms["source_explicit_scalar_projection"]
        - terms["source_explicit_scalar"]
    ) < 1.e-8

    assert abs(
        solved["earth_j_m"]
        - terms["earth_operator_analytic"]
    ) < .005

    assert abs(
        solved["common_j_m"]
        - terms["common_total"]
    ) < .005

    assert abs(
        solved["craft_j_m"]
        - terms["craft_earth_fixed_direct"]
    ) < .005

    assert row["stationarity_residual"] < 1.e-8


@pytest.mark.parametrize(
    "profile,width",
    (("c1", .25), ("c2", .5)),
)
def test_prescribed_profile_not_physical_certification(
    profile, width
):
    row = m.evaluate(
        h=.125,
        profile=profile,
        width=width,
    )

    assert (
        row["physical_earth_craft_reciprocity_certified"]
        is False
    )

    assert row["complete_device_energy_j"] is None

    assert abs(
        row["derivative_terms_j_m"][
            "earth_operator_analytic"
        ]
    ) > 1.


@pytest.mark.parametrize("phase", (-.25, .25))
def test_coarse_phase_artifact_retained(phase):
    row = m.evaluate(
        h=.2,
        phase=phase,
        direct_craft=False,
    )

    terms = row["derivative_terms_j_m"]

    assert abs(terms["common_total"]) > 5.
    assert abs(
        terms["source_explicit_scalar_raw"]
    ) > 5.

    assert abs(
        terms["source_explicit_scalar_projection"]
    ) < .01

    assert row["whole_spacecraft_lift_certified"] is False


def test_negative_controls():
    zero = m.evaluate(
        h=.25,
        zero_source=True,
    )

    assert abs(
        zero["derivative_terms_j_m"]["common_total"]
    ) < 1.e-12

    noearth = m.evaluate(
        h=.25,
        earth_present=False,
    )

    assert abs(
        noearth["derivative_terms_j_m"][
            "earth_operator_analytic"
        ]
    ) < 1.e-12


def test_m5p_earth_reference():
    row = m.evaluate(h=.2)

    assert row["derivative_terms_j_m"][
        "earth_operator_analytic"
    ] == pytest.approx(
        m.REFERENCE["compact", .2],
        abs=1.e-8,
    )


def test_registration_and_fail_closed_summary():
    quick = m.jobs("quick")
    full = m.jobs("full")

    assert len(quick) == 6
    assert len(full) == 41

    assert len(set(name for name, _ in full)) == 41

    assert m.summarize(
        quick, {}
    )["gates"]["Q1_stationary_quadratic_action"] == (
        "FAIL_OR_INCOMPLETE"
    )


def test_single_bundle_checkpoint_resume(tmp_path, monkeypatch):
    tasks = [
        ("a", {"h": .2}),
        ("b", {"h": .1}),
    ]

    calls = []

    required = (
        "Q0_m5p_Earth_derivative_reproduction",
        "Q1_stationary_quadratic_action",
        "Q2_Hellmann_Feynman_resolved",
        "Q3_total_source_enclosure_Earth_partition",
        "Q4_negative_controls",
    )

    gates = {key: "PASS" for key in required}

    def fake_evaluate(**kwargs):
        calls.append(kwargs["h"])
        return {
            "derivative_terms_j_m": {
                "earth_operator_analytic": 0.,
                "craft_earth_fixed_inferred": 0.,
                "common_total": 0.,
            }
        }

    monkeypatch.setattr(
        m, "jobs", lambda mode: tasks
    )
    monkeypatch.setattr(
        m, "evaluate", fake_evaluate
    )
    monkeypatch.setattr(
        m, "summarize", lambda *_: {"gates": gates}
    )

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "m5q",
            "--mode", "quick",
            "--results-dir", str(tmp_path),
            "--max-new-cases", "1",
        ],
    )

    assert m.main() == 2

    files = list(tmp_path.iterdir())
    assert len(files) == 1

    partial = json.loads(files[0].read_text())
    assert partial["status"] == "PARTIAL_NOT_CERTIFIED"

    monkeypatch.setattr(
        sys,
        "argv",
        [
            "m5q",
            "--mode", "quick",
            "--resume", str(files[0]),
        ],
    )

    assert m.main() == 0
    assert calls == [.2, .1]

    finished = json.loads(files[0].read_text())
    assert len(finished["results"]) == 2
    assert finished["status"] == "COMPLETE_NUMERICAL_ONLY"
    assert len(list(tmp_path.iterdir())) == 1
