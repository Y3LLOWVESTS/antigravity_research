"""GAMMA1-00R6: exact restricted trace bridge and Green/local Maxwell fork.

Only a necessary static Weyl reduction and finite-grid operator comparison.
The result cannot certify a covariant physical stress, Lorentzian modes,
continuum Maxwell convergence, Einstein geometry, or Earth/craft force.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
from scipy import sparse

PH16_SHA = 'b5468671f6418fad7b6ed01d916ea65a95a1d59252b84d4411beed9709f86df0'
R3_PROFILE_SHA = '94d3763a8d7705ab3dc8774310cf3b8bba96557a0b80d2c34aa110d00b840d54'
R5_MULTIPLIER_SHA = '2b9217ef9b36758ef675eeb47796198adf1be2ff6b5764b316a2e312bc82c883'


def sha(path):
    path = Path(path)
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else 'MISSING'


def read_lock(path, expected):
    if sha(path) != expected:
        raise RuntimeError('IMMUTABLE_SHA_MISMATCH: ' + str(path))
    with np.load(path, allow_pickle=False) as archive:
        result = {k: np.asarray(archive[k]).copy() for k in archive.files}
    if any(not np.all(np.isfinite(x)) for x in result.values()):
        raise RuntimeError('NONFINITE_PARENT')
    return result


def best_single_scale(K, L, rows=None):
    """Exact Frobenius least-squares scalar and relative mismatch."""
    if rows is not None:
        K = K[np.ix_(rows, rows)]
        L = L[np.ix_(rows, rows)]
    denom = float(np.sum(L*L))
    if denom <= 0:
        raise ValueError('Degenerate local quadratic')
    scale = float(np.sum(K*L)/denom)
    relative = float(np.linalg.norm(K-scale*L)/np.linalg.norm(K))
    return {'best_scale': scale, 'relative_frobenius_mismatch': relative}


def analyze(profile, multiplier):
    from antigravity_research.ph16.ph16_04_joint_stationary import (
        CoulombSource, Spec, Settings, JointAction,
    )

    m = CoulombSource(Spec(nr=12, L=12.0), self_order=8)
    o = JointAction(m, Settings(nr=12, L=12.0))
    N = o.N
    if N != 288 or m.nz != 24 or any(profile[k].shape != (N,) for k in
      ('F_plus','F_minus','A_X','A_Y','P','sigma','neutral_n','weights')):
        raise RuntimeError('NATIVE_MESH_SHAPE_DRIFT')
    if multiplier['lambda_Routhian'].shape != (N,):
        raise RuntimeError('MULTIPLIER_SHAPE_DRIFT')

    F = np.stack((profile['F_plus'], profile['F_minus']))
    A, Y = profile['A_X'], profile['A_Y']
    x = o.pack(F, A, Y)
    R, g, details = o.evaluate(x, True)
    if abs(R-2401.472107471401) > 1e-7 or np.linalg.norm(g) >= 1e-6:
        raise RuntimeError('ORIGINAL_PH16_ACTION_NOT_STATIONARY')
    if np.max(abs(g-profile['joint_gradient'])) > 1e-10:
        raise RuntimeError('ARCHIVED_GRADIENT_MISMATCH')

    w = o.w
    P = profile['P']; sigma = profile['sigma']
    sp = o.s.alpha-2*o.s.beta*P
    if np.max(abs(sp-multiplier['sigma_prime'])) > 1e-12:
        raise RuntimeError('PORTAL_DERIVATIVE_PARENT_MISMATCH')
    e2 = np.exp(2*sigma); e4=e2*e2
    f2=F*F
    U=np.sum(f2-2*f2**2+2*f2**3,axis=0)+m.s.g*f2[0]*f2[1]
    I=f2@(w*e2)
    omega=(m.s.N/2 + o.q*np.sum(f2*(w*e2*A)[None,:],axis=1))/I
    W=omega[:,None]-o.q[:,None]*A[None,:]

    # Independently distribute the candidate charged-scalar spatial
    # gradient density to the same cells as the original edge Routhian.
    # Each edge receives half its energy at each endpoint.
    spatial=np.zeros(N)
    for i in range(2):
        edge_sq=o.edge_c*(F[i,o.edge_i]-F[i,o.edge_j])**2
        np.add.at(spatial,o.edge_i,.5*e2[o.edge_i]*edge_sq)
        np.add.at(spatial,o.edge_j,.5*e2[o.edge_j]*edge_sq)
        spatial+=o.boundary*e2*f2[i]
    nlabel=profile['neutral_n']*np.exp(3*sigma)
    source_trace_density = (
       -2*spatial/w
       +2*e2*np.sum(W*W*f2,axis=0)
       -4*e4*U
    )
    fluid_trace_density = (
       -o.s.mass*nlabel*np.exp(sigma)
       +o.s.kappa*nlabel*nlabel*np.exp(-2*sigma)
    )
    einstein_volume_trace = source_trace_density+fluid_trace_density
    candidate_lam=sp*einstein_volume_trace
    saved_lam=multiplier['lambda_Routhian']
    diff=float(np.max(abs(candidate_lam-saved_lam)))
    if diff > 3e-12:
        raise RuntimeError('STATIC_MATTER_TRACE_REDUCTION_MISMATCH')
    # This equality is conditional on the above static matter ansatz,
    # edge allocation and fixed conserved-number labels, NOT a full
    # covariant source/Earth/support variation.

    Wx = sparse.diags(w)
    Lx=(o.Dr.T@Wx@o.Dr + o.Dz.T@Wx@o.Dz).toarray()
    Ly=(o.BR.T@Wx@o.BR + o.BZ.T@Wx@o.BZ).toarray()
    idx=np.arange(N).reshape(12,24)[1:-1,1:-1].ravel()
    kernel={}
    for sector,K,L,v in (
       ('X_electric',o.Kx,Lx,A),
       ('Y_magnetic',o.Ky,Ly,Y),
    ):
        global_fit=best_single_scale(K,L)
        interior_fit=best_single_scale(K,L,idx)
        Lv=L@v; Kv=K@v
        sv=float(np.dot(Kv,Lv)/np.dot(Lv,Lv))
        profile_error=float(np.linalg.norm(Kv-sv*Lv)/np.linalg.norm(Kv))
        if global_fit['relative_frobenius_mismatch'] < .1 or interior_fit['relative_frobenius_mismatch'] < .1:
            raise RuntimeError('EXPECTED_GRID_OPERATOR_FORK_NOT_PRESENT')
        if abs(float(np.max(abs(K-K.T)))) > 1e-8:
            raise RuntimeError('NONRECIPROCAL_ORIGINAL_GREEN_KERNEL')
        if abs(float(np.max(abs(L-L.T)))) > 1e-8:
            raise RuntimeError('NONRECIPROCAL_LOCAL_QUADRATIC')
        kernel[sector]={
          'whole_grid':global_fit,
          'interior_220x220':interior_fit,
          'on_archived_field_best_scale':sv,
          'on_archived_field_relative_gradient_mismatch':profile_error,
          'original_green_kernel_nonzero_entries':int(np.count_nonzero(K)),
          'local_nodal_matrix_nonzero_entries':int(np.count_nonzero(L)),
          'local_definition': 'Dr.T W Dr + Dz.T W Dz' if sector=='X_electric'
                              else 'BR.T W BR + BZ.T W BZ',
        }

    # Independent, honest positive controls of best-fit metric: rescaling
    # or comparing a local operator to itself produces zero mismatch.
    ctrl={k:best_single_scale(L,L) for k,L in (('X',Lx),('Y',Ly))}
    ctrl_scaled={k:best_single_scale(7*L,L) for k,L in (('X',Lx),('Y',Ly))}
    if any(abs(v['relative_frobenius_mismatch'])>1e-14 for v in [*ctrl.values(),*ctrl_scaled.values()]):
        raise RuntimeError('OPERATOR_FIT_POSITIVE_CONTROL_FAILED')

    return {
      'numbers':{
        'Routhian_NOT_J':float(R),
        'stationary_gradient_L2':float(np.linalg.norm(g)),
        'restricted_matter_trace_lambda_max_abs_error':diff,
        'trace_portal_multiplier_negative_cells':int(np.count_nonzero(candidate_lam<0)),
        'trace_portal_multiplier_positive_cells':int(np.count_nonzero(candidate_lam>0)),
        'full_source_canonical_action_and_fixed_N':'YES_WITHIN_PH16_LATTICE',
      },
      'kernel_comparison':kernel,
      'controls':{
        'local_self_frobenius':ctrl,
        'local_scaled_seven_frobenius':ctrl_scaled,
        'source_off_coupling_off':'FORMAL_OPERATOR_NULL_ONLY_NOT_SELF_CONSISTENT',
        'nonlocal_vs_local':'NOT_A_CONTINUUM_NO_GO',
      },
      'arrays':{
        'candidate_restricted_lambda':np.asarray(candidate_lam,dtype='<f8'),
        'candidate_matter_trace_undressed':np.asarray(einstein_volume_trace/e4,dtype='<f8'),
        'charged_source_trace_density':np.asarray(source_trace_density,dtype='<f8'),
        'neutral_fluid_trace_density':np.asarray(fluid_trace_density,dtype='<f8'),
        'trace_minus_R5_lambda':np.asarray(candidate_lam-saved_lam,dtype='<f8'),
      },
      'interpretation':{
         'restricted_static_trace_match':'PASS_CONDITIONAL_ON_CANDIDATE_MATTER_QUADRATURE',
         'same_nodal_stencil_local_Maxwell_operator_match':'FAIL_BOTH_CARRIERS_EVEN_OPTIMAL_CONSTANT_SCALING',
         'exact_full_covariant_reduction':'NOT_ESTABLISHED',
         'nonlocal_Green_Galerkin_continuum':'NOT_TESTED',
         'full_Lorentzian_constraints':'NOT_DERIVED',
         'Einstein_stress_and_metric':'NOT_DERIVED',
         'Earth_down_whole_craft_up':'NOT_DERIVED',
         'SI_complete_energy_lt10MJ':'NOT_CERTIFIED',
      },
    }
