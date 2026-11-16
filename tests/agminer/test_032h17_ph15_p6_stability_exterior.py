"""PH15-P6 independent analytic and direct-angular controls."""

import math
import numpy as np
from antigravity_research.agminer.hook17_ph15_p2p5_source import Source,Spec
from antigravity_research.agminer.hook17_ph15_p6_stability_exterior import (
    angular_operator, eigenmode, symmetric_trial_energy,
    independent_energy_control, charge_and_gauss_controls,
)


def test_source_symmetry_normalization_and_operator_selfadjoint():
    s=Source(Spec(n=18));info,f=s.solve(240)
    assert info['Gauss_L2']<1e-9
    H, err=angular_operator(s,f,0,1)
    assert err<1e-10
    assert H.shape==(2*s.cells,2*s.cells)
    assert np.max(abs(f['F'][0]-f['F'][1]))<1e-8


def test_nonaxisymmetric_k1_and_k2_negative_independent():
    s=Source(Spec(n=24));info,f=s.solve(240)
    d1,v1=eigenmode(s,f,0,1)
    d2,v2=eigenmode(s,f,0,2)
    assert d1['eigenvalue']< -0.05
    assert d2['eigenvalue']< -0.01
    assert d1['eigenpair_residual']<1e-7
    assert d2['eigenpair_residual']<1e-7


def test_exact_charge_and_mirror_J_and_gauss_under_mode():
    s=Source(Spec(n=18));_,f=s.solve(240)
    _,v=eigenmode(s,f,0,1)
    conserved=charge_and_gauss_controls(s,f,1,v,0.07)
    assert abs(conserved['N_each']-800)<1e-9
    assert conserved['max_pointwise_rhoX']<1e-12
    assert conserved['total_Jz']==0


def test_independent_angle_integral_energy_lowers_at_fixed_N():
    s=Source(Spec(n=24));_,f=s.solve(240)
    d,vec=eigenmode(s,f,0,1)
    q=independent_energy_control(s,f,1,vec)
    assert q['finite_energy_decrease']
    assert q['angular_energy_quadrature'][1]['delta_energy']<0
    assert q['angular_energy_quadrature'][0]['relative_coefficient_error']<1e-3
    assert q['angular_energy_quadrature'][1]['relative_coefficient_error']<1e-3


def test_ang_phi_quadrature_stability_32_64():
    s=Source(Spec(n=18));_,f=s.solve(240)
    _,vec=eigenmode(s,f,0,2)
    a=symmetric_trial_energy(s,f,2,vec,0.1,32)
    b=symmetric_trial_energy(s,f,2,vec,0.1,64)
    assert abs(a-b)<1e-9


def test_asymmetric_has_frozen_X_negative_directions_only():
    s=Source(Spec(n=24,mminus=1.08));r,f=s.solve(240)
    assert abs(r['electric_charge'])<1e-9
    assert s.first_order_Y(f)['Y_jphi_L2']>0.005
    for i in (0,1):
        d,_=eigenmode(s,f,i,1)
        assert d['eigenvalue']< -0.05
    # No assertion that a fully constrained asymmetric mode exists.


def test_winding_reversal_and_alpha_reversal_are_sign_controls():
    a=Source(Spec(n=18));_,f=a.solve(240)
    b=Source(Spec(n=18,wind=-1));_,g=b.solve(240)
    y=a.first_order_Y(f,alpha=1.0)
    z=a.first_order_Y(f,alpha=-1.0)
    rev=b.first_order_Y(g,alpha=1.0)
    assert np.isclose(y['mu_X'],-rev['mu_X'],rtol=1e-9)
    assert np.isclose(y['p_Y'],-rev['p_Y'],rtol=1e-9)
    assert np.isclose(y['dipole_axis_sigma_alphaP_coefficient'],z['dipole_axis_sigma_alphaP_coefficient'],rtol=1e-9)
    assert np.isclose(y['dipole_axis_sigma_alphaP_coefficient'],rev['dipole_axis_sigma_alphaP_coefficient'],rtol=1e-9)
