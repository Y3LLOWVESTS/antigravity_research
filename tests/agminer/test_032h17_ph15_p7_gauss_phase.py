"""PH15-P7 independent Gauss/Noether/J, energy and mode regression."""

import numpy as np
import pytest

from antigravity_research.agminer.hook17_ph15_p2p5_source import Spec

from antigravity_research.agminer.hook17_ph15_p7_gauss_phase import (
    GeneralWinding,
    neutral_weights,
    mode,
    direct_energy,
    conserved,
    q_density,
    q_phase,
    q_cross,
    portal,
)


@pytest.fixture(scope='module')
def asym():
    s=GeneralWinding(
        Spec(n=24,mminus=1.08),
        (1,-1)
    )
    r,f=s.solve(300)
    return s,r,f


@pytest.fixture(scope='module')
def nonzeroJ():
    s=GeneralWinding(
        Spec(n=24,mminus=1.08),
        (2,-1)
    )
    r,f=s.solve(300)
    return s,r,f


def test_source_equations_and_neutrality(asym,nonzeroJ):
    for s,r,f in (asym,nonzeroJ):
        assert r['Gauss_L2']<1e-9
        assert r['Ampere_L2']<1e-9
        assert max(r['scalar_EOM_weighted_L2'])<1e-4
        assert abs(r['electric_charge'])<1e-9
        assert np.max(abs(
            np.sum(
                s.q[:,None]
                *f['W']
                *f['F']**2
                *neutral_weights(s,f),
                axis=0
            )
        ))<1e-12


def test_fixed_local_gauss_N_and_J(asym,nonzeroJ):
    for s,r,f in (asym,nonzeroJ):
        for k in (1,2):
            d,h,b=mode(s,f,k)

            for t in (.04,.08,.12):
                c=conserved(s,f,k,h,b,t)

                assert np.max(abs(
                    np.array(c['N'])-800
                ))<1e-8

                assert abs(
                    c['total_Jz_matter_canonical']-r['Jz']
                )<1e-7

                assert c['max_pointwise_Gauss_delta']<1e-10


def test_density_only_survivor_fails_coupled_phase(nonzeroJ):
    s,r,f=nonzeroJ
    d,h,b=mode(s,f,1)

    assert r['Jz']==pytest.approx(800,abs=1e-7)
    assert d['density_eigen']>0
    assert d['phase_eigen']>0
    assert d['coupled_eigen']<0
    assert d['schur_eigen']<0

    assert d['Q_density']>0
    assert d['Q_phase']>0
    assert d['Q_cross']<0
    assert d['Q_total']<0
    assert d['eigen_residual']<1e-7


def test_direct_3D_energy_matches_quadratic_for_both(
    asym,nonzeroJ
):
    for s,r,f in (asym,nonzeroJ):
        d,h,b=mode(s,f,1)
        E0=direct_energy(s,f,1,h,b,0)

        for t in (.04,.08,.12):
            diff=(
                direct_energy(s,f,1,h,b,t)
                -E0
            )

            assert diff<0
            assert abs(
                diff/t**2-d['Q_total']
            )<.025


def test_full_azimuth_resolution(nonzeroJ):
    s,r,f=nonzeroJ
    d,h,b=mode(s,f,2)

    e32=direct_energy(
        s,f,2,h,b,.12,32
    )
    e64=direct_energy(
        s,f,2,h,b,.12,64
    )

    assert abs(e32-e64)<1e-9


def test_phase_reversal_cross_symmetry(nonzeroJ):
    s,r,f=nonzeroJ
    d,h,b=mode(s,f,1)

    assert q_phase(s,f,1,b)==pytest.approx(
        q_phase(s,f,1,-b),
        abs=1e-10
    )

    assert q_cross(s,f,1,h,b)==pytest.approx(
        -q_cross(s,f,1,h,-b),
        abs=1e-10
    )

    assert d['Q_total']==pytest.approx(
        q_density(s,f,1,h)
        +q_phase(s,f,1,b)
        +q_cross(s,f,1,h,b)
    )


def test_k3_scoped_positive_not_global_stability(nonzeroJ):
    s,r,f=nonzeroJ
    d,h,b=mode(s,f,3)

    assert d['coupled_eigen']>0
    assert d['H_symmetry']<1e-8


def test_nonzero_winding_induces_Y_both_channels(nonzeroJ):
    s,r,f=nonzeroJ
    y=s.first_order_Y(f)

    assert y['Y_rho_L2']>.05
    assert y['Y_jphi_L2']>.15


def test_null_nonwinding_control():
    s=GeneralWinding(
        Spec(n=18),
        (0,0)
    )

    r,f=s.solve(300)
    y=s.first_order_Y(f)

    assert y['Y_rho_L2']<1e-12
    assert y['Y_jphi_L2']<1e-12


def test_portal_beta_and_alpha_signs():
    p=portal()

    assert 'alpha**2' in p['dlambda_dP_0']
    assert 'beta' in p['dlambda_dP_0']
    assert p['Earth_craft_force']=='NOT_DERIVED'
