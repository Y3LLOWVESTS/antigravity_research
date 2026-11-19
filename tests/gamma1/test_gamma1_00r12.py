"""Eight R12 focused checks; no device or Lorentzian completion inference."""
from pathlib import Path
import numpy as np
import pytest
from antigravity_research.gamma1 import gamma1_00r12_offshell_fork as r

ROOT = Path(__file__).resolve().parents[2]


def test_metric_hodge_variation():
    assert max(r.metric_audit().values())<1e-8


def test_one_scalar_offshell_U1():
    assert r.gauge_jet() is True


def test_all_negative_controls():
    assert len(r.negative_controls())==5
    assert all(v is True for v in r.negative_controls().values())


def test_orientation_and_invalid_signature():
    g = np.diag([-1., 1., 1., 1.])
    f = np.zeros((4, 4))
    h = f.copy()
    f[0, 1], f[1, 0] = 1., -1.
    h[2, 3], h[3, 2] = 2., -2.
    assert r.pseudoscalar(f, h, g)==2.
    with pytest.raises(ValueError):
        r.pseudoscalar(f, h, np.eye(4))


def test_conformal_weight_minus_four():
    g = np.diag([-1., 1., 1., 1.])
    f = np.zeros((4, 4))
    h = f.copy()
    f[0, 1], f[1, 0] = .02, -.02
    h[2, 3], h[3, 2] = .03, -.03
    assert abs(r.pseudoscalar(f, h, 1.2**2*g)
               -1.2**-4*r.pseudoscalar(f, h, g))<1e-12


def test_immutable_parent_hashes():
    assert len(r.check_parents(ROOT))==6


def test_native_fixed_N_rank_two():
    d = r.r11_reclose(ROOT)
    assert d["rank"]==2
    assert d["archive_max_error"]<1e-10
    assert d["charge_reclosure_error"]<1e-9
    assert d["nonlocal_offdiag_max"]>.05


def test_historical_controls_not_promoted():
    d = r.negative_controls()
    assert d["X_off_P_zero"] and d["Y_off_P_zero"]
    assert r.PARENTS["R11_result"][1].startswith("ac7050")
