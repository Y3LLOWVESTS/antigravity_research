"""PH16-04 same-lattice Routhian, Noether, Ward and scope tests."""
from functools import lru_cache

import numpy as np
import pytest

from antigravity_research.ph16.ph16_04_joint_stationary import (
    report,
    exact_atlas,
    JointAction,
    Settings,
    independent_fd
)
from antigravity_research.agminer.hook17_ph15_p10_free_space import (
    CoulombSource,Spec
)


@lru_cache(maxsize=1)
def R():
    return report()


EXACT=tuple(exact_atlas())

GATES=(
    'exact_action_identities',
    'three_independent_mesh_domain_reconstructions',
    'protected_P10_seed_EOM',
    'symmetric_positive_reciprocal_ring_operators',
    'independent_F_X_Y_finite_difference',
    'initial_individual_Noether_fixed',
    'postsolve_individual_Noether_fixed',
    'neutral_integrated_number_conserved',
    'neutral_hydrostatic_chemical_balance',
    'finite_Y_nonzero',
    'joint_F_X_Y_residual_small',
    'joint_F_X_Y_individual_residual_small',
    'joint_solver_reported_convergence',
    'mimetic_magnetic_Bianchi',
    'mimetic_electric_curl_zero',
    'frozen_beta40_magnetic_margin_positive',
    'frozen_beta40_no_negative_cells',
    'both_initializations_reported_without_uniqueness_claim',
    'metric_force_not_claimed'
)

CASES=(
    '12_L12',
    '18_L12',
    '12_L16'
)


@pytest.mark.parametrize('name',EXACT)
def test_01_symbolic_identity(name):
    assert exact_atlas()[name]


@pytest.mark.parametrize('name',GATES)
def test_02_scoped_gate(name):
    assert R()['gates'][name]


@pytest.mark.parametrize('key',CASES)
def test_03_preserved_P10_seed(key):
    r=R()['cases'][key]

    assert r['P10']['source_eom_max']<5e-5

    np.testing.assert_allclose(
        r['P10']['N'],
        [400,400],
        atol=1e-8
    )


@pytest.mark.parametrize('key',CASES)
def test_04_noether_both_and_neutral(key):
    r=R()['cases'][key]

    np.testing.assert_allclose(
        r['Y_preconditioned_joint']['N'],
        [400,400],
        atol=1e-8
    )

    assert abs(
        r['Y_preconditioned_joint']['neutralN']
        -r['initial']['neutralN']
    )<1e-7

    assert abs(
        r['Y_preconditioned_joint']['X_Noether_charge']
    )<1e-8


@pytest.mark.parametrize('key',CASES)
def test_05_independent_F_X_Y_derivatives(key):
    rows=R()['cases'][key]['finite_difference']

    assert len(rows)==7
    assert max(c['error'] for c in rows)<5e-5

    n=(
        R()['cases'][key]['mesh']['nr']
        *2
        *R()['cases'][key]['mesh']['nr']
    )

    assert any(
        row['index']<2*n
        for row in rows
    )
    assert any(
        2*n<=row['index']<3*n
        for row in rows
    )
    assert any(
        3*n<=row['index']
        for row in rows
    )


@pytest.mark.parametrize('key',CASES)
def test_06_joint_saddle_convergence(key):
    a=R()['cases'][key]['Y_preconditioned_joint']

    assert a['final_residual_L2']<1e-6

    assert max(
        a['F_grad_norm'],
        a['X_grad_norm'],
        a['Y_grad_norm']
    )<1e-6

    assert a['root_success']


@pytest.mark.parametrize('key',CASES)
def test_07_mimetic_Bianchi_and_curl(key):
    a=R()['cases'][key]['Y_preconditioned_joint']

    assert a['discrete_mimetic_divB_inf']<1e-10
    assert a['discrete_curlE_inf']<1e-10


@pytest.mark.parametrize('key',CASES)
def test_08_beta40_frozen_magnetic_necessary_condition(key):
    a=R()['cases'][key]['Y_preconditioned_joint']

    assert a['frozen_magnetic_margin_min']>0
    assert a['frozen_negative_cells']==0


@pytest.mark.parametrize('key',CASES)
def test_09_recursion_source_X_and_induced_Y(key):
    a=R()['cases'][key]['Y_preconditioned_joint']

    assert a['Y_norm']>1e-5
    assert a['portal_X_variation_L2']>0
    assert a['Y_source_norm']>0
    assert a['min_n']>0


@pytest.mark.parametrize('key',CASES)
def test_10_scope_and_basin_reported(key):
    r=R()['cases'][key]

    assert r['physical_earth_metric']=='NOT_SOLVED'

    assert r['discrete_exterior'].endswith(
        'NOT_CONTINUUM_PROOF'
    )

    assert r['initialization_sensitivity'][
        'same_lattice_action'
    ]

    assert (
        'root_success'
        in r['direct_weak_seed']
    )
    assert (
        'root_success'
        in r['Y_preconditioned_joint']
    )


@lru_cache(maxsize=1)
def small_model():
    m=CoulombSource(
        Spec(nr=12,L=12),
        self_order=8
    )
    info,f=m.solve(350)
    return m,info,f


def test_11_zero_portal_reconstructs_P10_Routhian():
    m,info,f=small_model()

    o=JointAction(
        m,
        Settings(alpha=0,beta=40)
    )

    x=o.pack(
        f['F'],
        f['A'],
        np.zeros(m.cells)
    )

    R,g,d=o.evaluate(x,True)

    neutral=(
        .15+.5*.5*.15**2
    )*float(np.sum(m.w))

    assert abs(
        R-info['canonical_energy_NOT_J']-neutral
    )<1e-7

    assert d['Y_grad_norm']<1e-12


def test_12_discrete_inverse_kernel_reciprocity():
    m,_,_=small_model()
    o=JointAction(m,Settings())

    for K in (o.Kx,o.Ky):
        assert np.max(abs(K-K.T))<1e-9
        assert np.min(
            np.linalg.eigvalsh(K)
        )>0


def test_13_independent_mixed_A_Y_hessian_reciprocity():
    m,info,f=small_model()
    o=JointAction(m,Settings())

    x=o.initialize(info,f)
    n=o.N

    ia=2*n+n//2
    iy=3*n+n//3
    step=1e-4

    xp=x.copy()
    xm=x.copy()
    xp[iy]+=step
    xm[iy]-=step

    H_AY=(
        o.evaluate(xp)[1][ia]
        -o.evaluate(xm)[1][ia]
    )/(2*step)

    xp=x.copy()
    xm=x.copy()
    xp[ia]+=step
    xm[ia]-=step

    H_YA=(
        o.evaluate(xp)[1][iy]
        -o.evaluate(xm)[1][iy]
    )/(2*step)

    assert abs(H_AY-H_YA)<1e-7


def test_14_beta60_necessary_warning_not_full_no_go():
    m,info,f=small_model()

    o=JointAction(
        m,
        Settings(beta=60)
    )

    x=o.initialize(info,f)
    _,_,diag=o.evaluate(x,True)

    assert diag['frozen_magnetic_margin_min']<0
    assert diag['frozen_negative_cells']>0


def test_15_no_physical_promotion():
    r=R()

    assert r['physical_promotion']=='NO'
    assert r['full_constrained_modes']=='NOT_CERTIFIED'
    assert r['Earth_down_craft_up']=='NOT_DERIVED'
    assert r['complete_SI_energy_lt10MJ']=='NOT_CERTIFIED'
    assert r['continuum_and_true_exterior']=='NOT_CERTIFIED'


# 12 exact + 19 gates + 8*3 case tests + 5 controls = 60.
