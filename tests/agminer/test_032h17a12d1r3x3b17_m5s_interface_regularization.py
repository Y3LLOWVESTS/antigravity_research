"""B17-M5S interface integration and checkpoint tests."""
import json

import pytest
from numpy.polynomial.legendre import leggauss

from antigravity_research.agminer import (
    hook17_r3b_m5s_interface_regularization as m,
)


def test_manifest_is_deterministic():
    quick = m.manifest("quick")
    full = m.manifest("full")

    assert len(quick) == 4
    assert len(full) == 34

    assert {
        r["name"] for r in quick
    }.issubset({
        r["name"] for r in full
    })

    assert len({
        r["name"] for r in full
    }) == len(full)


@pytest.mark.parametrize("profile", ["c1", "c2"])
@pytest.mark.parametrize(
    "center",
    [-.63, -.25, -.13, 0., .13, .25, .63],
)
def test_exact_cell_integral_matches_gauss(profile, center):
    width = .25
    h = .125

    left = center-h/2
    right = center+h/2

    cuts = sorted({
        left,
        right,
        *[
            x for x in (-width, width)
            if left < x < right
        ],
    })

    nodes, weights = leggauss(6)
    independent = 0.

    for a, b in zip(cuts[:-1], cuts[1:]):
        x = .5*(a+b)+.5*(b-a)*nodes

        independent += .5*(b-a)*sum(
            float(w)*m.smooth_below(
                float(xi), 0., width, profile
            )
            for xi, w in zip(x, weights)
        )

    assert m.cell_average(
        center, 0., width, h, profile
    ) == pytest.approx(
        independent/h,
        abs=3.e-13,
    )


@pytest.mark.parametrize("profile", ["c1", "c2"])
@pytest.mark.parametrize(
    "center",
    [-.35, -.25, -.125, -.05, 0., .05, .125, .25, .35],
)
def test_exact_cell_derivative_matches_difference(
    profile, center
):
    delta = 1.e-5

    predicted = m.cell_derivative_edge(
        center, 0., .25, .125, profile
    )

    measured = (
        m.cell_average(
            center, delta, .25, .125, profile
        )
        -m.cell_average(
            center, -delta, .25, .125, profile
        )
    )/(2*delta)

    assert measured == pytest.approx(
        predicted,
        abs=1.e-7,
    )


def test_reference_is_not_a_carrier_certificate():
    audit = m.analytic_cell_audit()

    assert audit["max_derivative_defect"] < 2.e-5
    assert audit["max_flux_defect"] < 2.e-12
    assert audit[
        "point_sampling_differs_from_integrated_profile"
    ]
    assert "NOT_COUPLED_TO_CARRIER" in audit["scope"]


def fake_parent():
    return {
        "results": {
            "c1_original_h0.05": {
                "interaction_only": {
                    "common_derivative_j_m": .22,
                },
            },
            "c2_extended_h0.05": {
                "interaction_only": {
                    "common_derivative_j_m": .00096,
                    "earth_derivative_j_m": -11.42,
                },
            },
        },
    }


def test_no_premature_completion_certificate():
    row = {
        "parameters": m.manifest("quick")[0]["parameters"],
        "earth_analytic_j_m": -9.,
        "common_j_m": .2,
        "earth_difference_fd_minus_analytic_j_m": -.002,
        "max_stationarity_residual": 1.e-14,
        "max_source_fd_relative_defect": 1.e-7,
        "resolved_minus_envelope": {
            "common_j_m": 1.e-7,
        },
    }

    summary = m.summarize(
        {"one": row},
        m.manifest("full"),
        m.analytic_cell_audit(),
        fake_parent(),
    )

    assert summary[
        "artificial_model_100_percent_complete"
    ] is False

    assert summary["gates"][
        "S4_C1_discrete_operator_subcell_reassembly"
    ] == "NOT_IMPLEMENTED"


def test_restart_in_same_bundle(tmp_path, monkeypatch):
    jobs = [
        {
            "name": "first",
            "parameters": {"step": .001},
        },
        {
            "name": "second",
            "parameters": {"step": .0001},
        },
    ]

    monkeypatch.setattr(
        m,
        "manifest",
        lambda _: jobs,
    )

    monkeypatch.setattr(
        m,
        "load_parent",
        lambda _: (fake_parent(), "fixedhash", None),
    )

    calls = []

    def fake_run(parameters, carrier):
        calls.append(parameters["step"])

        return {
            "parameters": {
                "profile": "c1",
                "domain": "compact",
                "h": .125,
                "width": .25,
                "phase": 0.,
                "step": parameters["step"],
            },
            "earth_analytic_j_m": -9.,
            "craft_inferred_j_m": 9.2,
            "common_j_m": .2,
            "earth_difference_fd_minus_analytic_j_m": .001,
            "matched_self_translation_j_m": 0.,
            "max_stationarity_residual": 1.e-14,
            "max_source_fd_relative_defect": 1.e-7,
            "resolved_minus_envelope": {
                "common_j_m": 0.,
            },
        }

    monkeypatch.setattr(
        m,
        "run_case",
        fake_run,
    )

    args = [
        "--mode", "quick",
        "--parent-bundle",
        str(tmp_path/"parent.json"),
    ]

    assert m.main([
        *args,
        "--results-dir",
        str(tmp_path),
        "--max-new-cases", "1",
    ]) == 2

    bundles = list(
        tmp_path.glob(
            "b17_m5s_interface_*_quick_bundle.json"
        )
    )

    assert len(bundles) == 1

    assert m.main([
        *args,
        "--resume",
        str(bundles[0]),
    ]) == 0

    record = json.loads(
        bundles[0].read_text()
    )

    assert record["processed"] == 2
    assert record["status"] == (
        "COMPLETE_NUMERICAL_DIAGNOSTIC_ONLY"
    )
    assert calls == [.001, .0001]
