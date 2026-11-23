"""GRAVITY2-08: same-discrete-action off-shell source/X/Y audit.

This is a theorem-first audit of the already sealed GRAVITY2-07 periodic
(x,z) field archive, not a re-solve. The single charged complex scalar has
amplitude f>0, frequency omega, X charge q>0 and no independent neutralizer.
The Y potential b was solved; the X potential a and f were prescribed.

IMPORTANT ACTION PROVENANCE ERRATUM:
  GRAVITY2-07 bridge07_core.action() actually has NO X Maxwell term,
  although its science JSON 'L' summary says +|grad a|^2/2.
  We audit both the actual 07 functional, L07, and the specifically named
  augmented candidate L08=L07+|grad a|^2/2. This is not a silent correction
  of the archived 07 action. The added X term leaves Y EOM unchanged.

All integrals are canonical per unmodeled y-length. The periodic domain is
not a finite craft/exterior. No source action for a compensator, supports,
Earth, gravity or SI energy is claimed.
"""
from __future__ import annotations

import numpy as np

GRIDS=(9,15,23,31)
ALPHA=.08
BETA=.005
Q=.4
OMEGA=1.25
M2=.8
LAMBDA=.4


def D(v,h,axis):
    return (np.roll(v,-1,axis=axis)-np.roll(v,1,axis=axis))/(2*h)


def pieces(a,f,b,h, *, alpha=ALPHA,beta=BETA,q=Q,omega=OMEGA):
    ax,az=D(a,h,0),D(a,h,1)
    bx,bz=D(b,h,0),D(b,h,1)
    fx,fz=D(f,h,0),D(f,h,1)
    P=ax*bz-az*bx
    sigma=alpha*P-beta*P*P
    w=np.exp(2*sigma)
    z=np.exp(4*sigma)
    Omega=omega-q*a
    K=Omega**2*f*f-fx*fx-fz*fz
    V=M2*f*f/2+LAMBDA*f**4/4
    Pi=(w*K-4*z*V)*(alpha-2*beta*P)
    rho=q*w*Omega*f*f
    return locals()


def action(a,f,b,h, *, include_x):
    """Full DISCRETE periodic 2D functional; include_x is explicit."""
    p=pieces(a,f,b,h)
    density=(-.5*(p['bx']**2+p['bz']**2)
             +.5*p['w']*p['K']-p['z']*p['V'])
    if include_x:
        density=density+.5*(p['ax']**2+p['az']**2)
    return float(h*h*np.sum(density))


def euler(a,f,b,h, *, include_x=True):
    """Gradient of discrete action divided by h² for a, f and b.

    Periodic centered-difference D^T=-D gives exact discrete
    variational derivatives; these are not continuum-only equations.
    """
    p=pieces(a,f,b,h)
    ax,az,bx,bz,fx,fz=[p[k] for k in ('ax','az','bx','bz','fx','fz')]
    Pi=p['Pi']; w=p['w'];z=p['z'];Omega=p['Omega'];rho=p['rho']
    Da_x=Pi*bz+(ax if include_x else 0)
    Da_z=-Pi*bx+(az if include_x else 0)
    Ea=-rho-D(Da_x,h,0)-D(Da_z,h,1)
    Ef=(w*Omega**2*f-z*(M2*f+LAMBDA*f**3)
        +D(w*fx,h,0)+D(w*fz,h,1))
    Eb=D(bx,h,0)+D(bz,h,1)+D(Pi*az,h,0)-D(Pi*ax,h,1)
    return {'a':Ea,'f':Ef,'b':Eb}


def one_row(a,f,b,n):
    h=2*np.pi/n
    if any(arr.shape!=(n,n) or not np.isfinite(arr).all() for arr in (a,f,b)):
        raise ValueError('wrong shape or nonfinite parent field')
    p=pieces(a,f,b,h)
    grad=euler(a,f,b,h)
    grad07=euler(a,f,b,h,include_x=False)
    rho=p['rho']
    qtotal=float(h*h*np.sum(rho))
    mean_rho=float(np.mean(rho))
    x_displacement_div=(
        D(p['ax']+p['Pi']*p['bz'],h,0)
        +D(p['az']-p['Pi']*p['bx'],h,1))
    x_without_maxwell=(
        D(p['Pi']*p['bz'],h,0)-D(p['Pi']*p['bx'],h,1))
    x_addition=.5*h*h*np.sum(p['ax']**2+p['az']**2)

    result={
        'n':n, 'h':float(h), 'f_min':float(f.min()),
        'Omega_min':float(p['Omega'].min()),
        'w_min':float(p['w'].min()),
        'rho_min':float(rho.min()),
        'charge_integral_canonical':qtotal,
        'charge_density_mean_canonical':mean_rho,
        'charge_nonzero_sign':'POSITIVE_EVERY_CELL' if float(rho.min())>0 else 'NOT_PROVED',
        'X_euler_mean':float(np.mean(grad['a'])),
        'Gauss_integral_residual':float(h*h*np.sum(grad['a'])),
        'periodic_divergence_integral':float(h*h*np.sum(x_displacement_div)),
        'periodic_portal_divergence_integral':float(h*h*np.sum(x_without_maxwell)),
        'X_euler_rms':float(np.sqrt(np.mean(grad['a']**2))),
        'scalar_euler_rms':float(np.sqrt(np.mean(grad['f']**2))),
        'Y_euler_rms':float(np.sqrt(np.mean(grad['b']**2))),
        'X_euler_rms_parent_action':float(np.sqrt(np.mean(grad07['a']**2))),
        'X_maxwell_term_missing_in_parent_action':float(x_addition),
        'parent_action_value':action(a,f,b,h,include_x=False),
        'augmented_action_value':action(a,f,b,h,include_x=True),
        'uniform_compensator_required_density':-mean_rho,
        'after_uniform_compensator_X_rms':float(np.sqrt(np.mean((grad['a']+mean_rho)**2))),
    }

    if not (result['charge_nonzero_sign']=='POSITIVE_EVERY_CELL' and qtotal>0):
        raise AssertionError('expected positive-charge sector is not realized')
    if not abs(result['Gauss_integral_residual']+qtotal)<1e-10:
        raise AssertionError('zero-mode Gauss identity failed')
    if abs(result['periodic_divergence_integral'])>1e-10:
        raise AssertionError('periodic divergence identity failed')
    if not abs(result['augmented_action_value']-result['parent_action_value']-x_addition)<1e-10:
        raise AssertionError('source L provenance correction mismatch')
    return result


def scientific_evidence(archive):
    rows=[]
    for n in GRIDS:
        a,f,b=[archive[f'{name}_{n}'] for name in ('a','f','b')]
        rows.append(one_row(a,f,b,n))
    return {
        'decision':'PARENT_07_X_GAUSS_ZERO_MODE_OBSTRUCTED_NO_COMPENSATOR',
        'physical_causal_scope':'PERIODIC_2D_SINGLE_CHARGED_SCALAR_ONLY',
        'periodic_zero_mode_theorem':'integral(Div D_X)=0 forces integral(rho_X)=0; parent integral(rho_X)>0',
        'parent_action_erratum':'ACTUAL_07_ACTION_OMITS_X_MAXWELL_DESPITE_SCIENCE_L_SUMMARY',
        'augmented_candidate_action':'L08=L07+1/2*|grad_a|**2; Y EOM unchanged',
        'gauss':'Euler_a= -rho_X-Dx(a_x+Pi*b_z)-Dz(a_z-Pi*b_x)',
        'rho_X':'q*exp(2*sigma)*(omega-q*a)*f**2',
        'scalar_euler':'div(w*grad_f)+w*(omega-q*a)**2*f-z*(m2*f+lambda*f**3)',
        'Y_euler':'Lap_b+Dx(Pi*a_z)-Dz(Pi*a_x)',
        'control_uniform_background':'-mean(rho) cancels only net charge; UNSOURCED, not permitted physical completion',
        'potential_escape':'JUSTIFIED_OPPOSITE_CHARGE_SECTOR_OR_OPEN_FINITE_EXTERIOR; not constructed',
        'rows':rows,
        'convergence':'NUMERICAL_DIAGNOSTIC_ONLY_NO_CONTINUUM_CLAIM',
        'healthy_modes':'NOT_DERIVED',
        'physical_source':'NOT_ESTABLISHED',
        'complete_action':'NOT_DERIVED',
        'Einstein_sign':'NOT_DERIVED',
        'whole_craft':'NOT_DERIVED',
        'complete_SI_energy':'NOT_CERTIFIED',
        'physical_survivors':0,
        'L2_source_solve_authorized':False,
    }
