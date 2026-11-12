"""032H17A12D1R3X3B13: physically supported axisymmetric basis atlas.

Goals: static 1-kg loaded torus, canonical field energy, finite 1-m gap,
source-compact electric B7 finite shell (net neutral) and magnetic azimuthal
currents (divergence-free), independent sources on *opposite sides* of payload.

Use corrected R3X1 Lorentzian two-U(1) reciprocity. Linear-field reduction
builds a quadratic accelerator and energy Gram matrix from exact loaded solves.

TESTED source family: three spherical 2m source regions centered at z=0,-4.2,
+6.5m; each with independently adjustable E-shell and B-current strength.
Do NOT interpret this as exhaustive 3D orientations, microscopic source cost,
or full coupled physical action. Near-payload discretization is not certified.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import platform
import time
import sys
from datetime import datetime, timezone
from pathlib import Path
import numpy as np
import scipy
from scipy.linalg import eigh
from scipy.optimize import minimize
from scipy.sparse.linalg import splu
from scipy.special import eval_legendre
from antigravity_research.agminer.hook17_concurrent_u1_fieldstrength_metric import (
    C_LIGHT_M_S, EV_J, HBAR_C_EV_M, REFERENCE_PORTAL_SCALE_EV,
    SOURCE_RADIUS_M, PAYLOAD_MAJOR_RADIUS_M, PAYLOAD_MINOR_RADIUS_M,
    TARGET_ACCELERATION_M_S2, payload_center_z_m, _source_profile,
)
from antigravity_research.agminer.hook17_fdual_f_r3c1_validation import _build_baseline_and_prep
from antigravity_research.agminer.hook17_fdual_f_r3x1_lorentzian_sign_audit import _solve_loaded
from antigravity_research.agminer.hook17_fdual_f_loaded_payload_homotopy import (
    _fields_from_potentials, _vectors_to_full_potentials,
)
from antigravity_research.agminer.hook17_fdual_f_r3x3b7_finite_charge_shell import source_density_proxy, radial_profile
from antigravity_research.agminer.hook17_fdual_f_loaded_payload_homotopy import _prepare_low_rank_loaded_system
from antigravity_research.agminer.hook17_f2_strong_payload_loading_rescue import loading_coefficient_z
from antigravity_research.agminer.hook17_fdual_f_r3x1_lorentzian_sign_audit import _state, _direct_compare

ROOT = Path(__file__).resolve().parents[1]
G = float(TARGET_ACCELERATION_M_S2)
KAPPA = -2.0 * HBAR_C_EV_M**2 / REFERENCE_PORTAL_SCALE_EV**4
CAP_J = 1.5473042949759672
CENTERS = (0.0, -4.2, 6.5)
SHELL_WIDTH_M = 0.10

def support_gap(center):
    return math.hypot(PAYLOAD_MAJOR_RADIUS_M, payload_center_z_m()-center) - PAYLOAD_MINOR_RADIUS_M - SOURCE_RADIUS_M

def anchor_parameters():
    ref=_build_baseline_and_prep(0.05)
    f=ref['field'];rho=f['rho_grid'];z=f['z_grid'];r=np.hypot(rho,z)
    # Fit uses *unscaled* amplitudes. Recover reference R3B 1-g scale by
    # reproducing the original phi0 shape outside its compact source.
    amps=np.asarray(ref['fit']['boundary_amplitudes'],float)
    unscaled=np.zeros_like(r)
    xx=np.divide(z, r, out=np.ones_like(r), where=r>0)
    for ell,a in enumerate(amps,1):
        fr,_,_=radial_profile(ell,float(a),SOURCE_RADIUS_M,SHELL_WIDTH_M,r)
        unscaled += fr*eval_legendre(ell,np.clip(xx,-1,1))
    mask=(r>2.3)&(r<4.0)
    scale=np.sum(ref['phi0'][mask]*unscaled[mask])/np.sum(unscaled[mask]**2)
    rel=float(np.linalg.norm(ref['phi0'][mask]-scale*unscaled[mask])/np.linalg.norm(ref['phi0'][mask]))
    if rel > 1e-5:raise AssertionError(('R3B exterior reproduction failed',rel))
    # Use compact A12C current profile to calibrate the original R3B B source.
    ops=ref['prep']['operators'];core=_source_profile(rho[1:-1,1:-1],z[1:-1,1:-1]).ravel()
    jref=np.asarray(ops['k_a']@ref['a0'][1:-1,1:-1].ravel()).ravel()
    j_amp=float(np.dot(jref,core)/np.dot(core,core))
    current_fit=float(np.linalg.norm(jref-j_amp*core)/np.linalg.norm(jref))
    print(f'ANCHOR: electric_multipoles={len(amps)} R3B_exterior_rel={rel:.3e} '
          f'magnetic_discrete_source_profile_error={current_fit:.3e}',flush=True)
    return {'electric_amplitudes':amps*scale,'magnetic_current_amplitude':j_amp,
            'original_exterior_relative_error':rel,'magnetic_current_fit_relative_error':current_fit}

def source_bases(setup, anchor, family='expanded'):
    """Return compact, discrete-conserved source shapes with fixed normalization.

    compact: original B7 electric multipole combination + original current.
    expanded: 5 electric multipoles + 3 independent azimuthal currents,
              at each of the 3 nonoverlapping allowed center positions.
    """
    f=setup['field'];h=float(f['h']);rho=f['rho_grid'];z=f['z_grid']
    kphi=setup['prep']['operators']['k_phi'];ka=setup['prep']['operators']['k_a']
    solve_phi=splu(kphi.tocsc()).solve
    solve_a=splu(ka.tocsc()).solve
    vol=2*math.pi*rho*h*h
    bases=[];supports=[]

    def make_charge(ell_amplitudes, center):
        # Tensor Gauss subcell integration is crucial for the narrow 10cm
        # shell: midpoint sampling produces artificial >10% monopoles on
        # 7.5cm grids. Charge is a volume-cell-averaged continuum source.
        radius=np.hypot(rho,z-center)
        shell_near=(radius>=SOURCE_RADIUS_M-SHELL_WIDTH_M-h)&(radius<=SOURCE_RADIUS_M+h)
        # Only evaluate quadrature in the annular region.
        charge=np.zeros_like(radius)
        nodes,qweights=np.polynomial.legendre.leggauss(3)
        local_r=rho[shell_near]
        local_z=z[shell_near]
        numer=np.zeros_like(local_r)
        denom=np.zeros_like(local_r)
        for ir,wr in zip(nodes,qweights):
            for iz,wz in zip(nodes,qweights):
                rr=np.abs(local_r+0.5*h*ir)
                zz=local_z+0.5*h*iz-center
                radial=np.hypot(rr,zz)
                x=np.divide(zz,radial,out=np.ones_like(radial),where=radial>0)
                inside=(radial>=SOURCE_RADIUS_M-SHELL_WIDTH_M)&(radial<=SOURCE_RADIUS_M)
                q_at=np.zeros_like(radial)
                for ell,amp in ell_amplitudes:
                    safe_r=np.where(inside,np.maximum(radial,1e-12),SOURCE_RADIUS_M+1)
                    q_l=source_density_proxy(int(ell),float(amp),SOURCE_RADIUS_M,SHELL_WIDTH_M,safe_r)
                    q_at+=np.where(inside,q_l*eval_legendre(int(ell),np.clip(x,-1,1)),0)
                weight=wr*wz*rr
                numer+=weight*q_at
                denom+=weight
        charge[shell_near]=np.divide(numer,denom,out=np.zeros_like(numer),where=denom>0)
        shell=shell_near & (np.abs(charge)>0)
        q_total=float(np.sum(vol*charge))
        q_abs_before=float(np.sum(vol*np.abs(charge)))
        shellvol=float(np.sum(vol*shell))
        if shellvol<=0:raise RuntimeError('Electric source shell unresolved')
        charge[shell]-=q_total/shellvol
        q_total_after=float(np.sum(vol*charge))
        assert abs(q_total_after) < 1e-10*max(q_abs_before,1)
        phi=np.zeros_like(rho)
        phi[1:-1,:-1]=solve_phi(charge[1:-1,:-1].reshape(-1)).reshape(phi[1:-1,:-1].shape)
        return phi, {'net_charge_zero_discrete':True,
                     'monopole_correction_fraction':abs(q_total)/max(q_abs_before,1e-100),
                     'resolved_layer_grid_cells':int(np.count_nonzero(shell)),
                     'source_subcell_gauss_order':3,
                     'relative_monopole_residual':abs(q_total_after)/max(q_abs_before,1e-100)}

    def make_current(center, kind):
        original=_source_profile(rho,z-center)
        if kind=='original': shape=original
        elif kind=='annular':shape=original*(rho/SOURCE_RADIUS_M)**2
        elif kind=='odd_z':shape=original*((z-center)/SOURCE_RADIUS_M)
        else:raise ValueError(kind)
        current=shape*anchor['magnetic_current_amplitude']
        a=np.zeros_like(rho)
        a[1:-1,1:-1]=solve_a(current[1:-1,1:-1].reshape(-1)).reshape(a[1:-1,1:-1].shape)
        return a,{'axisymmetric_azimuthal_current_divergence_exact':True,
                  'current_support_within_radius_m':SOURCE_RADIUS_M,
                  'morphology':kind}

    unit_amp=math.sqrt(1.0/(math.pi*SOURCE_RADIUS_M*EV_J/HBAR_C_EV_M))
    for center in CENTERS:
        if family=='compact':
            electric_modes=[('mirror_all',list(enumerate(anchor['electric_amplitudes'],1)))]
            magnetic_modes=['original']
        elif family=='expanded':
            electric_modes=[(f'multipole_l{ell}',[(ell,unit_amp)]) for ell in (1,2,3,4,5)]
            magnetic_modes=['original','annular','odd_z']
        else:raise ValueError(f'Unsupported source family: {family}')
        for label, modes in electric_modes:
            phi, audit=make_charge(modes,center)
            bases.append((f'z{center:+.1f}_E_{label}',phi,np.zeros_like(phi)))
            supports.append({'center_z_m':center,'sector':'electric','name':label,
                             'gap_m':support_gap(center),'electric_shell_width_m':SHELL_WIDTH_M,
                             'support_radius_m':SOURCE_RADIUS_M,**audit})
        for label in magnetic_modes:
            a,audit=make_current(center,label)
            bases.append((f'z{center:+.1f}_B_{label}',np.zeros_like(a),a))
            supports.append({'center_z_m':center,'sector':'magnetic','name':label,
                             'gap_m':support_gap(center),'support_radius_m':SOURCE_RADIUS_M,**audit})
    return bases,supports

def field_arrays(setup, phi,a):
    f=setup['field'];return _fields_from_potentials(phi,a,f['rho_grid'],float(f['h']))

def loaded_basis(setup, name,phi0,a0):
    prep=dict(setup['prep']);prep['phi0_vec']=phi0[1:-1,:-1].reshape(-1)
    prep['a0_vec']=a0[1:-1,1:-1].reshape(-1)
    prep['c_a0']=np.asarray(prep['c_active']@prep['a0_vec']).reshape(-1)
    prep['d_phi0']=np.asarray(prep['d_active']@prep['phi0_vec']).reshape(-1)
    sol=_solve_loaded(prep,1.0,1.0)
    if not sol['success'] or sol['relative_residual']>1e-8:raise RuntimeError((name,sol))
    ph,a=_vectors_to_full_potentials(prep,setup['field'],phi0,a0,sol)
    return field_arrays(setup,phi0,a0),field_arrays(setup,ph,a),{
        'name':name,'relative_loaded_residual':float(sol['relative_residual']),
        'condition_number':float(sol['condition_number'])}

def quadratic_response(setup, field_states):
    f=setup['field'];h=float(f['h']);mask=f['payload']
    n=len(field_states)
    volume=2*math.pi*f['rho_grid']*h*h
    weights=(volume*setup['density'])[mask]
    mass=float(weights.sum())
    # Source vector q -> E=sum q_i Ei, B=sum q_i Bi.
    ee=[np.stack([d['e_rho'],d['e_z']],axis=0) for d in field_states]
    bb=[np.stack([d['b_rho'],d['b_z']],axis=0) for d in field_states]
    p=mask.sum();acc=np.empty((p,n,n),float);energy=np.empty((n,n),float)
    for i in range(n):
        for j in range(i,n):
            sigma=KAPPA*0.5*(np.sum(ee[i]*bb[j],axis=0)+np.sum(ee[j]*bb[i],axis=0))
            ai=(-C_LIGHT_M_S**2*np.gradient(sigma,h,axis=0,edge_order=2))[mask]
            acc[:,i,j]=acc[:,j,i]=ai
            en=0.5*EV_J/HBAR_C_EV_M*float(np.sum(volume*(np.sum(ee[i]*ee[j],axis=0)+np.sum(bb[i]*bb[j],axis=0))))
            energy[i,j]=energy[j,i]=en
    ac=np.einsum('p,pij->ij',weights,acc)/mass
    return acc,energy,ac,mass

def choose_witness(acc,energy,acc_pre,cap,seed=17,seeds=128,starts=10):
    n=energy.shape[0]
    evecs=np.linalg.eigvalsh(energy)
    if min(evecs)<-1e-8*max(evecs):raise RuntimeError('Negative canonical energy matrix')
    # eig floor only for numerical normalization if rank nearly deficient.
    eigfloor=max(float(max(evecs))*1e-10,1e-24)
    def en(x):return float(x@energy@x)
    def aa(q,x):return np.einsum('i,pij,j->p',x,q,x)
    rng=np.random.default_rng(seed)
    dirs=[]
    for k in range(n):
        for sign in (-1,1):
            v=np.zeros(n);v[k]=sign;dirs.append(v)
    for _ in range(seeds):dirs.append(rng.standard_normal(n))
    initial=[]
    for d in dirs:
        e=en(d)
        if e<=eigfloor:continue
        x=np.asarray(d)*math.sqrt(cap/e)
        aft=aa(acc,x);pre=aa(acc_pre,x)
        initial.append((float(np.min(aft)),float(np.min(pre)),x))
    initial.sort(key=lambda z:z[0],reverse=True)
    best=initial[0]
    local_stats=[]
    # Optimize min local acceleration with slack t and a physically necessary
    # preloaded everywhere-outward >=1g gate. Nonconvex: no global claim.
    for v in initial[:starts]+sorted(initial,key=lambda z:z[1],reverse=True)[:3]:
        x0=v[2]
        def obj(y):return -y[-1]
        def objjac(y):return np.r_[np.zeros(n),-1.0]
        def constraints(y):
            x=y[:n];t=y[-1]
            return np.r_[cap-en(x),aa(acc,x)-t,aa(acc_pre,x)-G]
        def jac(y):
            x=y[:n]
            return np.vstack([np.r_[-2*energy@x,0.0],
                             np.column_stack([2*np.einsum('pij,j->pi',acc,x),-np.ones(acc.shape[0])]),
                             np.column_stack([2*np.einsum('pij,j->pi',acc_pre,x),np.zeros(acc_pre.shape[0])])])
        res=minimize(obj,np.r_[x0,v[0]],jac=objjac,method='SLSQP',
                     constraints=[{'type':'ineq','fun':constraints,'jac':jac}],
                     options={'maxiter':180,'ftol':1e-8})
        x=res.x[:n]
        actual_min=float(np.min(aa(acc,x)))
        minpre=float(np.min(aa(acc_pre,x)))
        enow=en(x)
        valid=(enow<=cap*(1+1e-6) and minpre>=G-1e-4 and np.isfinite(actual_min))
        local_stats.append({'valid':bool(valid),'message':str(res.message),
                            'optimized_min_m_s2':actual_min,'preloaded_min_m_s2':minpre,'energy_j':enow})
        if valid and (best[1]<G or actual_min>best[0]):best=(actual_min,minpre,x.copy())
    x=best[2]
    return {'coefficients':x.tolist(),'energy_j':en(x),
            'min_loaded_m_s2':float(np.min(aa(acc,x))),
            'com_loaded_m_s2':float(np.mean(aa(acc,x))),
            'min_preloaded_m_s2':float(np.min(aa(acc_pre,x))),
            'energy_eigenvalues':evecs.tolist(),
            'preloaded_1g':bool(np.min(aa(acc_pre,x))>=G-1e-4),
            'loaded_1g_everywhere':bool(np.min(aa(acc,x))>=G),
            'optimizer':'rank_one_multistart_SLSQP_nonconvex',
            'local_starts_attempted':len(local_stats),
            'successful_feasible_local_starts':int(sum(v['valid'] for v in local_stats))}

def per_point_relaxed_bound(acc,energy,cap):
    # Every local achievable acceleration is <= its independent Rayleigh
    # maximum under same positive energy form. min_i of maxima is an upper
    # bound for any one coherent common source amplitude vector.
    eigen=np.linalg.eigvalsh(energy)
    if eigen[0]<=0:return {'status':'energy_gram_singular','min_eigen_j':float(eigen[0])}
    pointcaps=[]
    for q in acc:
        pointcaps.append(cap*max(eigh(q,energy,eigvals_only=True)))
    return {'status':'valid_local_independent_upper_bound','upper_bound_everywhere_m_s2':float(min(pointcaps)),
            'bottleneck_payload_index':int(np.argmin(pointcaps)),
            'single_point_energy_eigen_min':float(eigen[0])}

def check_reconstruction(setup,bases,loaded_fields):
    # Linear source superposition must reproduce a direct loaded BVP;
    # check with signed mixed coefficients, unlike reused quadratics alone.
    x=np.linspace(-.3,.5,len(bases))
    pp=sum(w*v[1] for w,v in zip(x,bases));aa=sum(w*v[2] for w,v in zip(x,bases))
    _,combined,_=loaded_basis(setup,'direct_mixed_source',pp,aa)
    for key in ('e_rho','e_z','b_rho','b_z'):
        expected=sum(w*state[key] for w,state in zip(x,loaded_fields))
        residual=np.linalg.norm(combined[key]-expected)/max(np.linalg.norm(combined[key]),1e-80)
        if residual>1e-8:raise AssertionError(('direct source superposition failed',key,residual))

def run_grid(h,anchor,budgets,seed,seeds,starts,family,direct_all=False):
    t=time.monotonic();setup=_build_baseline_and_prep(h)
    bs,support=source_bases(setup,anchor,family)
    pre=[];loaded=[];cert=[]
    for name,phi,a in bs:
        ep,el,c=loaded_basis(setup,name,phi,a)
        pre.append(ep);loaded.append(el);cert.append(c)
    check_reconstruction(setup,bs,loaded)
    preA,preE,preC,mass=quadratic_response(setup,pre)
    loadA,loadE,loadC,_=quadratic_response(setup,loaded)
    # Sanity: compare preloaded physical source baseline to original R3B.
    orig=setup['baseline']
    unit=np.zeros(len(bs))
    if family=='compact': unit[:2]=1.
    else: unit[0]=1.;unit[5]=1.  # l1 electric plus first current only
    original_b7_pre=float(np.min(np.einsum('i,pij,j->p',unit,preA,unit)))
    orig_loaded=float((unit@loadC@unit))
    baseline_R3B=orig.get('minimum_payload_acceleration_m_s2')
    rows=[]
    payload_indices=np.argwhere(setup['field']['payload'])
    for cap in budgets:
        bound=per_point_relaxed_bound(loadA,loadE,cap)
        if 'bottleneck_payload_index' in bound:
            jj,ii=payload_indices[bound['bottleneck_payload_index']]
            bound['bottleneck_rho_m']=float(setup['field']['rho_grid'][jj,ii])
            bound['bottleneck_z_m']=float(setup['field']['z_grid'][jj,ii])
        # AGMINER theorem-first: once the independent local upper bound
        # excludes 1g, do not spend hours optimizing a closed static family.
        # A small constructive witness is retained for force diagnostics.
        excluded=bound.get('upper_bound_everywhere_m_s2',float('inf'))<G
        witness=choose_witness(loadA,loadE,preA,cap,seed,
                               min(seeds,24) if excluded else seeds,
                               min(starts,3) if excluded else starts)
        witness['com_loaded_m_s2']=float(np.array(witness['coefficients'])@loadC@np.array(witness['coefficients']))
        witness['com_preloaded_m_s2']=float(np.array(witness['coefficients'])@preC@np.array(witness['coefficients']))
        # An upper bound below 1g is a scoped, exact-quadratic discrete exclusion.
        rows.append({'cap_j':cap,'upper_bound':bound,'best_rank_one_witness':witness})
        print(f'h={h:.3f} Ecap={cap:.4f}J '
              f'RANK1 loaded_min={witness["min_loaded_m_s2"]:+.5f} '
              f'COM={witness["com_loaded_m_s2"]:+.5f} '
              f'pre_min={witness["min_preloaded_m_s2"]:+.5f} '
              f'POINT_UPPER={bound.get("upper_bound_everywhere_m_s2",float("nan")):+.5f}',flush=True)
    # Independent full sparse solve for the few-joule witness on every grid.
    main_choice=min(rows,key=lambda b:abs(b['cap_j']-CAP_J))
    sparse_certificate=(direct_sparse_witness_check(setup,bs,main_choice['best_rank_one_witness']['coefficients'])
                        if direct_all or abs(h-.05)<1e-10 else {'status':'skipped_default_only_h0p05_verified'})
    return {'grid_m':h,'elapsed_s':round(time.monotonic()-t,3),
            'independent_full_sparse_witness_comparison':sparse_certificate,
            'mass_kg':mass,'source_labels':[b[0] for b in bs],
            'source_support':support,'basis_residuals':cert,
            'r3b_original_preloaded_min':float(baseline_R3B),
            'chosen_unit_pair_preloaded_min_m_s2':original_b7_pre,
            'chosen_unit_pair_loaded_COM_m_s2':orig_loaded,
            'chosen_unit_pair_loaded_energy_j':float(unit@loadE@unit),
            'chosen_unit_pair_preloaded_energy_j':float(unit@preE@unit),
            'budgets':rows}


def direct_sparse_witness_check(setup,bases,coeff):
    """Compare the reduced Woodbury solution with full coupled sparse solve."""
    x=np.asarray(coeff,float)
    phi0=sum(c*b[1] for c,b in zip(x,bases))
    a0=sum(c*b[2] for c,b in zip(x,bases))
    prep=dict(setup['prep'])
    prep['phi0_vec']=phi0[1:-1,:-1].reshape(-1)
    prep['a0_vec']=a0[1:-1,1:-1].reshape(-1)
    prep['c_a0']=np.asarray(prep['c_active']@prep['a0_vec']).reshape(-1)
    prep['d_phi0']=np.asarray(prep['d_active']@prep['phi0_vec']).reshape(-1)
    sol=_solve_loaded(prep,1.,1.)
    if not sol['success']:raise RuntimeError('Direct sparse witness prep failed')
    comparison=_direct_compare(dict(setup,prep=prep,phi0=phi0,a0=a0),sol,1.0,1.0)
    if not comparison['pass']:raise AssertionError(('full sparse direct check',comparison))
    return comparison


def matter_profile(base,field,name):
    """Redistribute existing neutral toroidal mass without moving its support.

    These are hypothesis morphologies, NOT certified matter with a stable EOS.
    The discretely integrated mass is held exactly equal to the baseline grid.
    """
    if name=='original':return base.copy()
    rho,z=field['rho_grid'],field['z_grid']
    dr=(rho-PAYLOAD_MAJOR_RADIUS_M)/PAYLOAD_MINOR_RADIUS_M
    dz=(z-payload_center_z_m())/PAYLOAD_MINOR_RADIUS_M
    rr=dr*dr+dz*dz
    if name=='inner_heavy': trial=base*np.exp(-1.5*np.clip(dr,-1,1))
    elif name=='outer_heavy':trial=base*np.exp(+1.5*np.clip(dr,-1,1))
    elif name=='top_heavy':trial=base*np.exp(+1.5*np.clip(dz,-1,1))
    elif name=='bottom_heavy':trial=base*np.exp(-1.5*np.clip(dz,-1,1))
    elif name=='edge_heavy':trial=base*(0.15+4.0*rr)
    elif name=='core_heavy':trial=base*(1+3.0*np.maximum(1-rr,0)**2)
    else:raise ValueError(name)
    assert np.all(trial>=0) and np.all(trial[base==0]==0)
    vol=2*math.pi*rho*float(field['h'])**2
    trial*=float(np.sum(vol*base))/float(np.sum(vol*trial))
    assert abs(float(np.sum(vol*(trial-base))))<1e-10
    return trial


def transfer_and_matter_gate(h,anchor,family,candidates,profiles):
    """Retest FIXED h=.05 witness amplitudes on each mesh and material.

    The expensive density-dependent reciprocal operator is built ONCE
    per (grid, material profile), then reused for every source candidate.
    """
    setup=_build_baseline_and_prep(h)
    bs,_=source_bases(setup,anchor,family)
    f=setup['field'];base=setup['density'];gridh=float(f['h'])
    vol=2*math.pi*f['rho_grid']*gridh**2
    cand=[]
    for label,coeffs,cap in candidates:
        if coeffs is None:
            phi0=setup['phi0'];a0=setup['a0'];fixed_across_mesh=False
        else:
            xx=np.asarray(coeffs,float)
            assert xx.size==len(bs)
            phi0=sum(c*b[1] for c,b in zip(xx,bs))
            a0=sum(c*b[2] for c,b in zip(xx,bs))
            fixed_across_mesh=True
        pre=field_arrays(setup,phi0,a0)
        sigpre=KAPPA*(pre['e_rho']*pre['b_rho']+pre['e_z']*pre['b_z'])
        apre=-C_LIGHT_M_S**2*np.gradient(sigpre,gridh,axis=0,edge_order=2)
        pre_min=float(np.min(apre[f['payload']]))
        cand.append((label,phi0,a0,cap,pre_min,fixed_across_mesh))
    results=[]
    for name in profiles:
        density=matter_profile(base,f,name)
        if name=='original':shared=setup['prep']
        else:
            beta=-(loading_coefficient_z(density,REFERENCE_PORTAL_SCALE_EV)-1.)
            shared=_prepare_low_rank_loaded_system(f,setup['phi0'],setup['a0'],beta)
        for label,phi0,a0,cap,pre_min,fixed_across_mesh in cand:
            prep=dict(shared)
            prep['phi0_vec']=phi0[1:-1,:-1].reshape(-1)
            prep['a0_vec']=a0[1:-1,1:-1].reshape(-1)
            prep['c_a0']=np.asarray(prep['c_active']@prep['a0_vec']).reshape(-1)
            prep['d_phi0']=np.asarray(prep['d_active']@prep['phi0_vec']).reshape(-1)
            sol=_solve_loaded(prep,1.0,1.0)
            if not sol['success'] or sol['relative_residual']>1e-8:raise RuntimeError((name,h,sol))
            state=dict(setup,prep=prep,phi0=phi0,a0=a0,density=density)
            metric=_state(state,sol)
            phi,a=_vectors_to_full_potentials(prep,f,phi0,a0,sol)
            em=field_arrays(setup,phi,a)
            sigma=KAPPA*(em['e_rho']*em['b_rho']+em['e_z']*em['b_z'])
            acceleration=-C_LIGHT_M_S**2*np.gradient(sigma,gridh,axis=0,edge_order=2)
            mass=float(np.sum(vol*density))
            com=float(np.sum(vol*density*acceleration)/mass)
            force_by_parts=float(C_LIGHT_M_S**2*np.sum(vol*sigma*np.gradient(density,gridh,axis=0,edge_order=2)))
            force_direct=mass*com
            rel_identity=abs(force_direct-force_by_parts)/max(abs(force_direct),abs(force_by_parts),
                     float(np.sum(np.abs(vol*density*acceleration))),1e-90)
            if rel_identity>0.03:raise AssertionError(('force identity failed',label,name,h,rel_identity))
            row={'grid_m':h,'candidate':label,'material_profile':name,
                 'same_fixed_source_coefficients_across_grid':fixed_across_mesh,
                 'field_energy_budget_j':cap,'preloaded_min_m_s2':pre_min,
                 'loaded_energy_j':float(metric['canonical_field_energy_j']),
                 'loaded_min_m_s2':float(metric['minimum_payload_acceleration_m_s2']),
                 'loaded_com_m_s2':com,'discrete_mass_kg':mass,
                 'field_energy_within_cap':bool(metric['canonical_field_energy_j']<=cap*(1+1e-6)),
                 'whole_payload_1g':bool(metric['minimum_payload_acceleration_m_s2']>=G),
                 'center_of_mass_1g':bool(com>=G),'reciprocal_force_identity_error':rel_identity,
                 'weak_sigma_check':bool(metric['weak_sigma_self_consistency']),
                 'relative_loaded_residual':float(sol['relative_residual'])}
            if label=='candidate_1p547j' and name=='original':
                independent=_direct_compare(state,sol,1.0,1.0)
                if not independent['pass']:raise AssertionError(('full sparse independent solve mismatch',h,independent))
                row['direct_sparse_comparison']=independent
            results.append(row)
            print(f'MATTER h={h:.3f} {label:18s} {name:13s} '
                  f'E={row["loaded_energy_j"]:.4f}J '
                  f'COM={com:+.6f} MIN={row["loaded_min_m_s2"]:+.5f} '
                  f'identity={rel_identity:.2e}',flush=True)
    return results

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--grids',nargs='+',type=float,default=[.075,.05,.04,.03])
    parser.add_argument('--caps',nargs='+',type=float,default=[CAP_J,5.,20.])
    parser.add_argument('--seeds',type=int,default=160)
    parser.add_argument('--starts',type=int,default=12)
    parser.add_argument('--family',choices=('compact','expanded'),default='expanded')
    parser.add_argument('--shell-width',type=float,default=.10,help='B7-inspired finite electric layer, meters')
    parser.add_argument('--with-matter-check',action='store_true',help='Add fixed-mass geometry/material full loaded BVP')
    parser.add_argument('--direct-all-grids',action='store_true',help='Run expensive independent full sparse check on every grid')
    parser.add_argument('--material-profiles',nargs='+',default=['original','inner_heavy','outer_heavy','top_heavy','bottom_heavy','core_heavy','edge_heavy'])
    args=parser.parse_args()
    global SHELL_WIDTH_M
    SHELL_WIDTH_M=float(args.shell_width)
    if not 0.02<=SHELL_WIDTH_M<=0.30:raise SystemExit('Shell width out of declared 0.02-0.30 m range')
    if args.with_matter_check and not all(any(abs(c-req)<1e-7 for c in args.caps) for req in (CAP_J,20.)):
        raise SystemExit('Matter gate requires the default 1.547304 J and 20 J caps')
    for center in CENTERS:
        if support_gap(center)<1-1e-9:raise AssertionError('external 1m standoff violated')
    for i,c1 in enumerate(CENTERS):
        for c2 in CENTERS[i+1:]:
            if abs(c1-c2)<2*SOURCE_RADIUS_M-1e-9:raise AssertionError('source regions overlap')
    anchor=anchor_parameters()
    grids=[]
    for h in args.grids:
        grids.append(run_grid(h,anchor,args.caps,17,args.seeds,args.starts,args.family,args.direct_all_grids))
    # Transfer the SAME 0.05-m optimized source amplitudes across all grids,
    # then vary fixed-mass neutral density with unchanged external sources.
    matter=[]
    if args.with_matter_check:
        h05=next((g for g in grids if abs(g['grid_m']-.05)<1e-9),None)
        if h05 is None:raise SystemExit('Matter gate requires --grids to contain 0.05')
        choices=[]
        for cap,label in ((CAP_J,'candidate_1p547j'),(20.,'candidate_20j')):
            choice=min(h05['budgets'],key=lambda b:abs(b['cap_j']-cap))
            choices.append((label,choice['best_rank_one_witness']['coefficients'],float(choice['cap_j'])))
        choices.append(('original_R3B_control',None,100.0))
        for h in args.grids:
            matter.extend(transfer_and_matter_gate(h,anchor,args.family,choices,
                          args.material_profiles))

    allfail=all(not (row['best_rank_one_witness']['loaded_1g_everywhere']
                      and row['best_rank_one_witness']['preloaded_1g']
                      and row['best_rank_one_witness']['energy_j']<=row['cap_j']*(1+1e-6))
                for g in grids for row in g['budgets'])
    all_bound_excluded=all(row['upper_bound'].get('upper_bound_everywhere_m_s2',float('inf'))<G
                         for g in grids for row in g['budgets'])
    out={'branch':'032H17A12D1R3X3B13','family':'FIXED_MORPHOLOGY_COMPACT_EXTERNAL_SOURCE_BASIS',
         'source_centers_m':CENTERS,'source_family':args.family,'fixed_multipole_amplitudes_from_0p05_grid':anchor['electric_amplitudes'].tolist(),
         'fixed_azimuthal_magnetic_source_amplitude':anchor['magnetic_current_amplitude'],
         'anchor':{k:v for k,v in anchor.items() if k!='electric_amplitudes'},
         'grids':grids,'matter_cross_grid':matter,
         'all_tested_discrete_local_independent_upper_bounds_exclude_1g':all_bound_excluded,
         'optimization_theorem_first_stopped_when_upper_bound_below_1g':True,
         'all_tested_rank_one_witnesses_fail_1g':allfail,
         'arbitrary_3d_angles_tested':False,'microscopic_sources_realized':False,
         'finite_electric_source_layer_used':True,'electric_shell_width_m':SHELL_WIDTH_M,
         'B7_exact_exterior_solution_preserved_numerically':False,
         'electric_source_from_B7_inspired_finite_layer_discrete_Poisson':True,'net_electric_source_monopole_zero_discretely':True,
         'physical_magnetic_current_microscopic_cost_certified':False,
         'finite_box_boundary_audit_completed':False,'fixed_mass_material_stability_EOS_certified':False,
         'material_morphology_cross_grid_checked':args.with_matter_check,
         'full_action_noether_energy_momentum_certified':False,
         'field_energy_not_complete_operating_energy':True,
         'field_redefinition_invariance_certified':False,'stability_uv_empirical_certified':False,
         'full_regression_1283_rerun':False,'whole_craft_lift_certified':False,'006D_replaced':False,
         'numpy_version':np.__version__,'scipy_version':scipy.__version__,
         'python_version':sys.version,'platform':platform.platform(),
         'direct_sparse_verification_every_grid_requested':args.direct_all_grids,
         'random_seed':17,'random_initializations':args.seeds,
         'multistart_local_optimizations':args.starts,
         'requested_caps_j':args.caps,
         'source_snapshot_sha256':{
             name:hashlib.sha256((ROOT/'src/antigravity_research/agminer'/name).read_bytes()).hexdigest()
             for name in (
                 'hook17_fdual_f_r3c1_validation.py',
                 'hook17_fdual_f_r3x1_lorentzian_sign_audit.py',
                 'hook17_fdual_f_r3x3b7_finite_charge_shell.py',
             )},
         'this_simulation_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    grid_tag='_'.join(str(round(h*1000)) for h in args.grids)
    path=ROOT/'results/data'/(
        f'032h17a12d1r3x3b13_{args.family}_shell{int(round(SHELL_WIDTH_M*1000))}_'
        f'h{grid_tag}_{stamp}_summary.json')
    path.parent.mkdir(exist_ok=True,parents=True)
    if path.exists():raise SystemExit('Refusing to overwrite immutable run summary')
    path.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print('B13_SOURCE_BASIS=COMPLETED_SCOPED')
    print('B13_FIXED_MASS_MORPHOLOGY=COMPLETED_SCOPED' if args.with_matter_check else 'B13_FIXED_MASS_MORPHOLOGY=SKIPPED')
    print('ALL_TESTED_RANK_ONE_1G=',not allfail)
    print('ALL_TESTED_DISCRETE_UPPER_BOUNDS_EXCLUDE_1G=',all_bound_excluded)
    print('SOURCE_MICROSCOPIC_AND_FULL_ACTION=NOT_CERTIFIED')
    print('FINITE_BOX_AND_3D_CONVERGENCE=NOT_CERTIFIED')
    print('REAL_3D_TILTS=NOT_TESTED')
    print('SUMMARY=',path)
if __name__=='__main__':main()
