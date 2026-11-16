"""PH15-P2/P5 restricted axisymmetric source regression controls."""

import numpy as np

from antigravity_research.agminer.hook17_ph15_p2p5_source import (
    Source,
    Spec,
)


def test_symmetric_charge_gauss_ampere_and_y():
    s = Source(Spec(n=24))
    r, f = s.solve(200)
    y = s.first_order_Y(f)

    assert abs(r["electric_charge"]) < 1e-10
    assert abs(r["Jz"]) < 1e-10
    assert r["Gauss_L2"] < 1e-9
    assert r["Ampere_L2"] < 1e-9

    assert y["Y_rho_L2"] > 0.1
    assert y["Y_jphi_L2"] < 1e-10
    assert y["dipole_product_p_mu"] < 0


def test_asymmetric_induction_has_both_channels():
    s = Source(Spec(n=24, mminus=1.08))
    r, f = s.solve(200)
    y = s.first_order_Y(f)

    assert abs(r["electric_charge"]) < 1e-9
    assert y["Y_rho_L2"] > 0.1
    assert y["Y_jphi_L2"] > 0.01


def test_nonwinding_symmetry_control():
    s = Source(Spec(n=24, wind=0))
    r, f = s.solve(200)
    y = s.first_order_Y(f)

    assert r["magnetic_field_energy"] < 1e-15
    assert y["Y_rho_L2"] < 1e-12
    assert y["Y_jphi_L2"] < 1e-12


def test_exact_constrained_discrete_gradient_by_FD():
    s = Source(
        Spec(
            n=12,
            L=12,
            N=300,
            mminus=1.08,
        )
    )

    f = s.seed().ravel()
    _, g = s.evaluation(f)

    for k in (7, 18, 39, 99):
        h = 2e-5

        up = f.copy()
        dn = f.copy()

        up[k] += h
        dn[k] -= h

        fd = (
            s.evaluation(up)[0]
            - s.evaluation(dn)[0]
        ) / (2 * h)

        assert abs(fd - g[k]) < 5e-5


def test_mzero_energy_saddle_fixed_noether_and_zero_total_J():
    s = Source(Spec(n=24))
    _, f = s.solve(200)

    q = s.m0_energetic_saddle(f)

    assert q["pointwise_electric_charge_zero"]
    assert q["total_Jz"] == 0

    assert q["lowest_frozen_m0_eigenvalue"] < -0.01
    assert q["energy_delta_at_eps"] < 0
    assert q["quadratic_coefficient"] < -10


def test_negative_saddle_refines():
    vals = []

    for n in (18, 28):
        s = Source(Spec(n=n))
        _, f = s.solve(200)

        vals.append(
            s.m0_energetic_saddle(f)[
                "lowest_frozen_m0_eigenvalue"
            ]
        )

    assert vals[1] < vals[0] < -0.01


def test_far_metric_sign_invariant_under_alpha_reversal():
    s = Source(Spec(n=24))
    _, f = s.solve(200)

    plus = s.first_order_Y(f, alpha=1)
    minus = s.first_order_Y(f, alpha=-1)

    assert (
        plus["dipole_axis_sigma_alphaP_coefficient"]
        < 0
    )

    assert (
        minus["dipole_axis_sigma_alphaP_coefficient"]
        < 0
    )

    assert np.isclose(
        plus["dipole_axis_sigma_alphaP_coefficient"],
        minus["dipole_axis_sigma_alphaP_coefficient"],
    )


def test_winding_axis_regularity_improves_on_refinement():
    ratios = []

    for n in (24, 36):
        s = Source(Spec(n=n))
        r, _ = s.solve(200)

        ratios.append(
            abs(
                1
                - r["axis_u_ratio_f0_over_rho"]
            )
        )

    assert ratios[1] < ratios[0]
    assert ratios[1] < 0.03
