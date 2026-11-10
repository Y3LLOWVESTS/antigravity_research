"""R3X3B2 — exact charge, mass and anomaly regression tests."""
from fractions import Fraction
import importlib.util
import json
from pathlib import Path

import pytest

from antigravity_research.agminer.hook17_r3x3b2_exact_source_gate import (
    anomaly_polynomials,
    massive_dirac_gate,
    nullspace,
)


def load_runner():
    path = (
        Path(__file__).resolve().parents[2]
        / "simulations"
        / "032h17a12d1r3x3b2_exact_source_protection_gate.py"
    )

    spec = importlib.util.spec_from_file_location(
        "r3x3b2_runner", path
    )

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_single_unbroken_u1():
    assert nullspace([], 1) == ((Fraction(1),),)


def test_mixed_unbroken_u1():
    assert nullspace([[1, -1]], 2) == (
        (Fraction(1), Fraction(1)),
    )


def test_full_rank_higgs_breaks_all():
    assert not nullspace([[1, 0], [0, 1]], 2)


@pytest.mark.parametrize(
    "ql,qr",
    [(1, -1), (2, -2), (1, 0)],
)
def test_axial_hard_mass_forbidden(ql, qr):
    result = massive_dirac_gate([ql], [qr], [])

    assert not result[
        "mass_term_gauge_invariant_and_vev_realized"
    ]
    assert not result[
        "massive_dirac_axial_source_on_unbroken_u1_allowed"
    ]


def test_higgs_mass_breaks_axial_u1():
    result = massive_dirac_gate(
        [1], [-1], [[2]], [2]
    )

    assert result[
        "mass_term_gauge_invariant_and_vev_realized"
    ]
    assert result["number_of_unbroken_u1"] == 0


def test_mixed_higgs_leaves_vectorlike_u1():
    result = massive_dirac_gate(
        [1, 0], [0, 1],
        [[1, -1]], [1, -1],
    )

    assert result[
        "mass_term_gauge_invariant_and_vev_realized"
    ]
    assert result["unbroken_massive_dirac_vectorlike"]
    assert result["axial_charges_on_unbroken_basis"] == ["0"]


def test_vectorlike_source_allowed_algebraically():
    result = massive_dirac_gate([3], [3], [])
    assert result["unbroken_massive_dirac_vectorlike"]


def test_single_axial_dirac_anomalous():
    result = anomaly_polynomials([([1], [-1])])

    assert result["mixed_gravitational_numerators"] == ["2"]
    assert result["abelian_cubic_numerators"]["0,0,0"] == "2"
    assert not result["these_abelian_anomalies_cancel"]


def test_opposite_axial_anomalies_cancel_but_not_physics():
    result = anomaly_polynomials([
        ([1], [-1]),
        ([-1], [1]),
    ])

    assert result["these_abelian_anomalies_cancel"]
    assert not result[
        "full_microscopic_anomaly_completion_certified"
    ]


def test_multicharge_vectorlike_anomaly_zero():
    result = anomaly_polynomials([
        ([1, 2], [1, 2]),
        ([-1, 3], [-1, 3]),
    ])

    assert result["these_abelian_anomalies_cancel"]


def test_charge_dimensions_rejected():
    with pytest.raises(ValueError):
        massive_dirac_gate([1, 2], [1], [])


def test_missing_prior_data_is_explicit(tmp_path):
    runner = load_runner()

    assert not runner.previous_portal_scale_audit(
        tmp_path / "missing.json"
    )["available"]


def test_prior_evidence_not_promoted_to_device(tmp_path):
    runner = load_runner()
    path = tmp_path / "scale.json"

    path.write_text(json.dumps({
        "branch":
            "032H17A12D1R3X3B1_LINKED_PORTAL_SCALE_PREFLIGHT",
        "grids": [
            {
                "h_m": 0.075,
                "rows": [{
                    "t": 5e-6,
                    "M_X_keV": 21.147,
                    "outward_everywhere_sampled": True,
                    "canonical_field_energy_1g_j": 275000,
                    "required_source_amplitude_vs_1keV": 450,
                }],
            },
            {
                "h_m": 0.05,
                "rows": [{
                    "t": 5e-6,
                    "M_X_keV": 21.147,
                    "outward_everywhere_sampled": True,
                    "canonical_field_energy_1g_j": 301000,
                    "required_source_amplitude_vs_1keV": 470,
                }],
            },
        ],
    }))

    audit = runner.previous_portal_scale_audit(path)
    row = audit["by_loading_ratio"]["5e-06"]

    assert row["field_energy_max_J"] == 301000
    assert row["source_amplitude_max_vs_reference"] == 470
    assert row["largest_field_only_budget_remainder_J"] == 9699000
    assert not row["complete_operating_energy_certified"]
