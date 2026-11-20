"""Focused D0 scalar-proxy variational and negative-control tests."""
import numpy as np

from antigravity_research.gamma1 import (
    gamma1_d0_m0_local_action_gate as d
)


def test_metric_stress():
    errors, _ = d.variational_checks()
    assert errors["metric_stress"] < 1e-8


def test_portal_variations_both_carriers():
    errors, _ = d.variational_checks()
    assert errors["FX_matter_variation"] < 1e-8
    assert errors["FY_matter_variation"] < 1e-8


def test_full_carrier_variations():
    errors, _ = d.variational_checks()
    assert errors["FX_total_variation"] < 1e-8
    assert errors["FY_total_variation"] < 1e-8


def test_charged_source_currents():
    errors, _ = d.variational_checks()
    assert max(
        value for key, value in errors.items()
        if key.startswith("source_current_")
    ) < 1e-8


def test_exact_u1_and_bianchi():
    assert d.exact_gauge_and_bianchi() is True


def test_negative_controls():
    controls, _ = d.negative_controls()
    assert len(controls) == 6
    assert all(v is True for v in controls.values())


def test_Y_off_is_not_automatically_stationary():
    controls, first_y = d.negative_controls()
    assert controls["Y_OFF_P_ZERO"]
    assert first_y < -1e-8


def test_R12_immutable_parent_contract():
    assert d.PARENTS["R12_science"][1].startswith("7ebddf22")
    assert d.PARENTS["R12_verification"][1].startswith("583ffee1")
    assert d.PARENTS["R11_science"][1].startswith("ac7050")
